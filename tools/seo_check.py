#!/usr/bin/env python3
"""Audit every page for the SEO defects that have actually bitten this site.

Read-only. Nothing here writes a file, so it is safe as a required check on
pull requests from forks.

Two severities, and the split is deliberate:

- An ERROR is something objectively broken, or something Google / Rich Results
  will reject outright: JSON that does not parse, an entity leaking into
  structured data, a canonical that disagrees with og:url, a link to a page
  that does not exist. These block CI.
- A WARNING is an editorial judgement where a human may reasonably disagree
  with the rule: a 68-character title, a 240-word page. These do not block.

Making title length an error would fail the first run on 83 pages, and a gate
that fails on day one gets switched off in a week. Warnings are held down by a
ratchet instead: --max-warnings is seeded at today's count and lowered as
content work lands, so the number can never grow.

Usage:
    python3 tools/seo_check.py                 # report
    python3 tools/seo_check.py --strict        # warnings count as errors
    python3 tools/seo_check.py --max-warnings 120
    python3 tools/seo_check.py --json
"""

import argparse
import glob
import html as htmllib
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"

LD_BLOCK = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)
# Entities are HTML syntax. Inside a JSON-LD string they are not decoded, so
# "Venue &amp; Hotels" reaches Google with the "&amp;" intact.
ENTITY = re.compile(r"&(?:[A-Za-z][A-Za-z0-9]{1,31}|#\d{1,7}|#[xX][0-9A-Fa-f]{1,6});")
TAG = re.compile(r"(?s)<(script|style|nav|header|footer)\b.*?</\1>|<[^>]+>")

# Site-level nodes live in the identity graph on every page, so a reference to
# one of them is never dangling even though it is defined in another block.
SITE_IDS = {SITE + "/#organization", SITE + "/#website", SITE + "/#logo"}


def meta(html, key, attr="name"):
    m = re.search(
        r'<meta\s+%s=["\']%s["\']\s+content=["\'](.*?)["\']' % (attr, re.escape(key)),
        html,
        re.I,
    )
    return m.group(1) if m else None


def text_of(html):
    """Visible words in the page body, chrome removed."""
    body = html[html.index("<main") :] if "<main" in html else html
    return htmllib.unescape(TAG.sub(" ", body))


def glyphs(value):
    """Length as a SERP counts it: "&amp;" is one character, not five."""
    return len(htmllib.unescape(value or ""))


def url_for(rel):
    directory = os.path.dirname(rel)
    return "/" + directory + "/" if directory else "/"


def load_pages():
    pages = {}
    for rel in sorted(glob.glob("**/index.html", recursive=True, root_dir=ROOT)):
        with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
            pages[url_for(rel)] = (rel, handle.read())
    return pages


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, message):
        self.errors.append((where, message))

    def warn(self, where, message):
        self.warnings.append((where, message))


def check_page(url, rel, html, report, ids, refs):
    err = lambda m: report.error(rel, m)  # noqa: E731
    warn = lambda m: report.warn(rel, m)  # noqa: E731

    # --- structured data ---------------------------------------------------
    # @id is a global identifier, not a per-document one, so a reference is
    # resolved against every id on the site. That is what lets a case study
    # say isPartOf the works collection defined on the hub, the same way every
    # page references #organization without redefining it.
    for raw in LD_BLOCK.findall(html):
        try:
            data = json.loads(raw)
        except ValueError as exc:
            err("JSON-LD does not parse: %s" % exc)
            continue

        def walk(node):
            if isinstance(node, dict):
                for key, value in node.items():
                    if key == "@id" and isinstance(value, str):
                        (refs if set(node) == {"@id"} else ids).add((rel, value))
                    elif isinstance(value, str) and ENTITY.search(value):
                        err(
                            'HTML entity in JSON-LD value %s: "%s"'
                            % (key, value[:70])
                        )
                    walk(value)
            elif isinstance(node, list):
                for item in node:
                    walk(item)

        walk(data)

    if "&amp;amp;" in html:
        err("double-escaped entity (&amp;amp;) in the document")

    # --- head --------------------------------------------------------------
    canonicals = re.findall(r'<link rel="canonical" href="([^"]*)"', html)
    robots = meta(html, "robots") or ""
    noindex = "noindex" in robots

    if not canonicals:
        err("no canonical")
    elif len(canonicals) > 1:
        err("%d canonical tags" % len(canonicals))
    else:
        canonical = canonicals[0]
        if not canonical.startswith("https://"):
            err("canonical is not absolute: %s" % canonical)
        elif canonical != SITE + url and not noindex:
            err("canonical does not self-reference: %s (page is %s)" % (canonical, url))
        og_url = meta(html, "og:url", "property")
        if og_url and og_url != canonical:
            err("og:url %s disagrees with canonical %s" % (og_url, canonical))

    required = [
        ("title", re.search(r"<title>(.*?)</title>", html, re.S)),
        ("meta description", meta(html, "description")),
        ("meta robots", meta(html, "robots")),
        ("og:title", meta(html, "og:title", "property")),
        ("og:description", meta(html, "og:description", "property")),
        ("og:image", meta(html, "og:image", "property")),
        ("twitter:card", meta(html, "twitter:card")),
    ]
    for label, value in required:
        if not value:
            err("missing %s" % label)

    h1s = re.findall(r"<h1[ >]", html)
    if len(h1s) != 1:
        err("%d <h1> elements, expected exactly 1" % len(h1s))

    # --- editorial warnings ------------------------------------------------
    title_match = re.search(r"<title>(.*?)</title>", html, re.S)
    if title_match:
        n = glyphs(title_match.group(1))
        if n > 60:
            warn("title is %d characters, truncates in search results" % n)
        elif n < 30:
            warn("title is only %d characters" % n)

    description = meta(html, "description")
    if description:
        n = glyphs(description)
        if n > 160:
            warn("meta description is %d characters" % n)
        elif n < 70:
            warn("meta description is only %d characters" % n)

    # og:description mirroring the meta description is normal and harmless.
    # What is worth flagging is a page with no social-specific copy at all,
    # where a shared link repeats the search snippet verbatim.
    og_description = meta(html, "og:description", "property")
    twitter_description = meta(html, "twitter:description")
    if og_description == description and (
        not twitter_description or twitter_description == description
    ):
        warn("no social copy distinct from the meta description")

    words = len(text_of(html).split())
    if words < 250 and not noindex:
        warn("only %d words of body copy" % words)

    # Counted inside <main> only. The footer's nav column labels used to be
    # <h2> and had to be subtracted here; tools/site_footer.py made them <p>,
    # so every remaining h2 is real page structure.
    body = html[html.index("<main") :] if "<main" in html else html
    body = re.sub(r"(?s)<footer.*?</footer>", "", body)
    h2s = len(re.findall(r"<h2[ >]", body))
    if h2s < 3 and not noindex:
        warn("%d content <h2> headings" % h2s)


def check_site(pages, report):
    # Duplicate titles and descriptions across the site.
    for label, values in (
        ("title", {u: re.search(r"<title>(.*?)</title>", h, re.S) for u, (_, h) in pages.items()}),
        ("meta description", {u: meta(h, "description") for u, (_, h) in pages.items()}),
    ):
        seen = defaultdict(list)
        for url, value in values.items():
            if value is None:
                continue
            text = value.group(1) if hasattr(value, "group") else value
            seen[text.strip()].append(url)
        for text, urls in seen.items():
            if len(urls) > 1:
                report.error(
                    "site",
                    "%d pages share one %s (%s): %s"
                    % (len(urls), label, text[:50], ", ".join(sorted(urls)[:4])),
                )

    # Internal links that go nowhere.
    known = set(pages)
    for url, (rel, html) in pages.items():
        for href in sorted(set(re.findall(r'href="(/[^"#?]*)"', html))):
            if href in known:
                continue
            target = href.lstrip("/")
            if os.path.exists(os.path.join(ROOT, target)) or os.path.exists(
                os.path.join(ROOT, target, "index.html")
            ):
                continue
            report.error(rel, "internal link to a page that does not exist: %s" % href)

    # Orphans: reachable only through the nav and footer, if at all.
    inbound = Counter()
    for url, (_, html) in pages.items():
        body = re.sub(r"(?s)<header.*?</header>|<footer.*?</footer>", "", html)
        for href in set(re.findall(r'href="(/[^"#?]*)"', body)):
            if href in known and href != url:
                inbound[href] += 1
    for url in sorted(known):
        if inbound[url] == 0 and "noindex" not in (meta(pages[url][1], "robots") or ""):
            report.warn(pages[url][0], "no contextual inbound links, only nav and footer")

    # llms.txt coverage.
    llms_path = os.path.join(ROOT, "llms.txt")
    if os.path.exists(llms_path):
        listed = set(re.findall(re.escape(SITE) + r"(/[^)\s]*)", open(llms_path, encoding="utf-8").read()))
        for url in sorted(known - listed):
            if "noindex" not in (meta(pages[url][1], "robots") or ""):
                report.warn(pages[url][0], "not listed in llms.txt")

    # Sitemaps: reuse the existing checker rather than reimplementing it.
    result = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "sitemaps.py"), "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        report.error("sitemaps", "coverage drift:\n" + result.stdout.strip())

    for name in sorted(glob.glob(os.path.join(ROOT, "sitemap-*.xml"))):
        body = open(name, encoding="utf-8").read()
        entries = re.findall(r"<url>(.*?)</url>", body, re.S)
        missing = [e for e in entries if "<lastmod>" not in e]
        if missing:
            report.error(
                os.path.basename(name),
                "%d of %d <url> entries have no <lastmod>" % (len(missing), len(entries)),
            )

    for dead in ("_headers", "_redirects"):
        if os.path.exists(os.path.join(ROOT, dead)):
            report.error(
                dead,
                "Netlify-format config on a Vercel deployment; it is never read, "
                "so its rules are a second source of truth that does nothing",
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="treat warnings as errors")
    parser.add_argument("--max-warnings", type=int, default=None)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    pages = load_pages()
    report = Report()
    ids, refs = set(), set()
    for url, (rel, html) in pages.items():
        check_page(url, rel, html, report, ids, refs)

    defined = {value for _, value in ids} | SITE_IDS
    for rel, ref in sorted(refs):
        if ref not in defined:
            report.error(rel, "JSON-LD @id reference resolves to nothing: %s" % ref)

    check_site(pages, report)

    if args.as_json:
        print(
            json.dumps(
                {
                    "errors": [{"where": w, "message": m} for w, m in report.errors],
                    "warnings": [{"where": w, "message": m} for w, m in report.warnings],
                },
                indent=2,
            )
        )
    else:
        for label, items in (("ERROR", report.errors), ("WARNING", report.warnings)):
            for where, message in items:
                print("%-7s %-55s %s" % (label, where, message))
        print()
        print("%d pages, %d errors, %d warnings" % (len(pages), len(report.errors), len(report.warnings)))

    failed = bool(report.errors)
    if args.strict and report.warnings:
        failed = True
    if args.max_warnings is not None and len(report.warnings) > args.max_warnings:
        print(
            "warning budget exceeded: %d > %d"
            % (len(report.warnings), args.max_warnings)
        )
        failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
