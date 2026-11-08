#!/usr/bin/env python3
"""Consolidate the COP31 cluster: fold thin satellite pages into strong pages.

Why: Search Console shows Google stopped crawling most of the 35-page COP31
cluster in mid-September and dropped it from search in October. Many pages
covered near-identical intent (stands vs booth builder, hotels vs group
accommodation, venue vs EXPO Center, ...). Fewer, deeper pages are a stronger
quality signal than many overlapping ones.

What it does (one-off, but safe to re-run — it is a no-op once applied):
  1. Moves the distinctive sections of each merged page into its target page,
     under an anchor named after the old slug, and merges new FAQs into the
     target's FAQ list and FAQPage schema.
  2. Adds a "Local proof" section (TÜRSAB licence + delivered Antalya projects
     from /selected-works/) to every remaining COP31 evergreen page.
  3. Updates titles where the target now covers the merged scope.
  4. Deletes the merged pages, adds 301 redirects (vercel.json + _redirects),
     removes them from nav/footer menus and rewrites every internal link.
  5. Updates llms.txt / llms-full.txt.

The live HTML is the source of truth here: the cop31_pages_* generators drifted
from it in October (title/description fixes were made in the HTML), so this
works on the HTML directly rather than regenerating.

Usage: python3 tools/cop31_consolidate.py
"""

import glob
import html
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_merge_map import MERGES, MERGED_TO, PROOF, RETITLE  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"

BACK_RE = re.compile(r"\s*<p>This page is part of the <a [^>]*>[^<]*</a>[^<]*</p>")
FAQ_ITEM_RE = re.compile(r'<div class="faq-item"><h3>(.*?)</h3>(.*?)</div>', re.S)
MAX_FAQS_FROM_SOURCE = 2
MAX_FAQS_ADDED = 6
PROOF_BEGIN = "<!-- cop31-proof:begin -->"
PROOF_END = "<!-- cop31-proof:end -->"


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as handle:
        handle.write(text)


def page(slug):
    return slug + "/index.html"


def strip_tags(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text)).strip()


# --- 1. content -------------------------------------------------------------

def extract_section(src_html, heading):
    """The full <section> whose first <h2> is `heading`."""
    pattern = re.compile(
        r'(?:<!-- transfer-prices:[\w-]+:begin -->\n)?<section class="page-section[^"]*">\s*<h2>%s</h2>'
        r'.*?</section>(?:\n<!-- transfer-prices:[\w-]+:end -->)?' % re.escape(heading), re.S
    )
    match = pattern.search(src_html)
    if not match:
        raise SystemExit("Section not found: %r" % heading)
    return match.group(0)


def insertion_point(target_html):
    """Index just before the conversion banner / FAQ / related block."""
    for marker in (
        "<h2>Planning Context for COP31 Antalya</h2>",
        '<section class="page-section cop31-cta">',
        "<h2>Frequently Asked Questions</h2>",
        "<h2>Continue Planning for COP31 Antalya</h2>",
        '<section class="page-section cop31-sources">',
    ):
        idx = target_html.find(marker)
        if idx != -1:
            if marker.startswith("<h2>"):
                idx = target_html.rfind("<section", 0, idx)
            return idx
    raise SystemExit("No insertion point found")


def merged_block(source_slug, spec):
    src = read(page(source_slug))
    parts = []
    for i, item in enumerate(spec["sections"]):
        heading, new_heading = item if isinstance(item, tuple) else (item, item)
        block = extract_section(src, heading)
        block = BACK_RE.sub("", block)
        if new_heading != heading:
            block = block.replace("<h2>%s</h2>" % heading, "<h2>%s</h2>" % new_heading, 1)
        if i == 0:
            block = block.replace('<section class="', '<section id="%s" class="' % source_slug, 1)
        parts.append(block)
    faqs = FAQ_ITEM_RE.findall(src)
    return "\n".join(parts) + "\n", faqs


def merge_faqs(target_html, new_faqs):
    existing = {strip_tags(q).lower() for q, _ in FAQ_ITEM_RE.findall(target_html)}
    added = []
    for q, a in new_faqs:
        if len(added) >= MAX_FAQS_ADDED:
            break
        if strip_tags(q).lower() not in existing:
            existing.add(strip_tags(q).lower())
            added.append((q, a))
    if not added:
        return target_html
    items = "".join('<div class="faq-item"><h3>%s</h3>%s</div>' % qa for qa in added)
    target_html = target_html.replace(
        '<div class="faq-list">', '<div class="faq-list">' + "", 1
    )
    # Append after the last existing item of the visible list.
    list_start = target_html.find('<div class="faq-list">')
    if list_start == -1:
        return target_html
    last_end = None
    for m in FAQ_ITEM_RE.finditer(target_html, list_start):
        last_end = m.end()
    target_html = target_html[:last_end] + items + target_html[last_end:]

    # FAQPage schema in <head>.
    def patch_schema(match):
        data = json.loads(match.group(2))
        if data.get("@type") != "FAQPage":
            return match.group(0)
        for q, a in added:
            data["mainEntity"].append({
                "@type": "Question",
                "name": strip_tags(q),
                "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)},
            })
        return match.group(1) + json.dumps(data, ensure_ascii=False) + match.group(3)

    target_html = re.sub(
        r'(<script type="application/ld\+json">\s*)(\{"@context": ?"https://schema.org", ?"@type": ?"FAQPage".*?\})(\s*</script>)',
        patch_schema,
        target_html,
        count=1,
        flags=re.S,
    )
    return target_html


def proof_section(slug):
    spec = PROOF[slug]
    items = "".join(
        '<li><a href="/selected-works/%s/">%s</a> — %s</li>' % (w, title, where)
        for w, title, where in spec["works"]
    )
    return (
        PROOF_BEGIN + "\n"
        '<section class="page-section" id="local-proof">\n'
        "            <h2>%s</h2>\n"
        '            <p class="page-section__lede">%s</p>\n'
        "            <ul>%s</ul>\n"
        "            <p>DMC Turkey Partner operates under ANTALYA GOLF MCD TRAVEL "
        "(PMR Turizm İnşaat Ticaret Ltd. Şti.), TÜRSAB-registered travel agency no. 12434, "
        "with its office in Muratpaşa, Antalya. Every project above is documented with photos "
        'and scope on <a href="/selected-works/">Selected Works</a>.</p>\n'
        "          </section>\n" + PROOF_END + "\n"
    ) % (spec["heading"], spec["lede"], items)


def build_target(target, sources):
    rel = page(target)
    text = read(rel)
    if '<section id="%s"' % sources[0][0] in text:
        return False  # already applied
    blocks, faqs = [], []
    for source_slug, spec in sources:
        block, src_faqs = merged_block(source_slug, spec)
        blocks.append(block)
        faqs.extend(src_faqs[:MAX_FAQS_FROM_SOURCE])
    at = insertion_point(text)
    text = text[:at] + "".join(blocks) + text[at:]
    text = merge_faqs(text, faqs)
    write(rel, text)
    return True


def add_proof(slug):
    rel = page(slug)
    text = read(rel)
    text = re.sub(re.escape(PROOF_BEGIN) + r".*?" + re.escape(PROOF_END) + r"\n", "", text, flags=re.S)
    at = insertion_point(text)
    text = text[:at] + proof_section(slug) + text[at:]
    write(rel, text)


def retitle(slug, spec):
    rel = page(slug)
    text = read(rel)
    old_title = re.search(r"<title>(.*?)</title>", text).group(1)
    old_plain = html.unescape(old_title)
    new_plain = html.unescape(spec["title"])
    text = text.replace("<title>%s</title>" % old_title, "<title>%s</title>" % spec["title"])
    text = text.replace('content="%s"' % old_title, 'content="%s"' % spec["title"])
    text = text.replace('"name": "%s"' % old_plain, '"name": "%s"' % new_plain)
    text = text.replace('"name":"%s"' % old_plain, '"name":"%s"' % new_plain)
    if spec.get("description"):
        old_desc = re.search(r'<meta name="description" content="([^"]*)"', text).group(1)
        text = text.replace('content="%s"' % old_desc, 'content="%s"' % spec["description"])
        text = text.replace('"description": "%s"' % html.unescape(old_desc), '"description": "%s"' % html.unescape(spec["description"]))
        text = text.replace('"description":"%s"' % html.unescape(old_desc), '"description":"%s"' % html.unescape(spec["description"]))
    if spec.get("h1"):
        text = re.sub(r"<h1>.*?</h1>", "<h1>%s</h1>" % spec["h1"], text, count=1)
    write(rel, text)


# --- 2. links ---------------------------------------------------------------

def new_href(old_slug):
    return "/%s/#%s" % (MERGED_TO[old_slug], old_slug)


def rewrite_links(text, own_slug=None):
    # Menu entries (nav + footer) for merged pages are removed outright.
    for old in MERGED_TO:
        text = re.sub(r'[ \t]*<li><a href="/%s/">[^<]*</a></li>\n' % re.escape(old), "", text)
    # Remaining in-content links point at the section that now holds the content.
    for old in MERGED_TO:
        for prefix in ("", SITE):
            text = text.replace('href="%s/%s/"' % (prefix, old), 'href="%s"' % new_href(old))
    # Cluster link rows and CTA service lists: drop duplicates and self-links.
    def dedupe_links(container_html, sep=""):
        links = re.findall(r'<a href="([^"]+)"[^>]*>.*?</a>', container_html)
        seen, keep = set(), []
        for m in re.finditer(r'<a href="([^"]+)"[^>]*>.*?</a>', container_html):
            href = m.group(1)
            path = href.split("#")[0]
            if own_slug and path == "/%s/" % own_slug:
                continue
            if href in seen or path in seen:
                continue
            seen.add(href)
            seen.add(path)
            keep.append(m.group(0))
        del links
        return sep.join(keep)

    def fix_cluster(m):
        return m.group(1) + dedupe_links(m.group(2)) + m.group(3)

    text = re.sub(r'(<div class="cluster-links">)(.*?)(</div>)', fix_cluster, text, flags=re.S)

    def fix_services(m):
        return m.group(1) + dedupe_links(m.group(2), " · ") + m.group(3)

    text = re.sub(r'(<p class="cop31-cta__services">)(.*?)(</p>)', fix_services, text, flags=re.S)
    return text


def all_html():
    for path in glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True):
        if "/node_modules/" in path or "/.git/" in path:
            continue
        yield os.path.relpath(path, ROOT)


# --- 3. redirects -----------------------------------------------------------

def add_redirects():
    rel = "vercel.json"
    data = json.loads(read(rel))
    existing = {r["source"] for r in data["redirects"]}
    for old, target in MERGED_TO.items():
        for source in ("/%s" % old, "/%s/:path*" % old):
            if source not in existing:
                data["redirects"].append(
                    {"source": source, "destination": "/%s/" % target, "statusCode": 301}
                )
    write(rel, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    rel = "_redirects"
    text = read(rel)
    if "COP31 cluster consolidation" not in text:
        lines = ["", "# COP31 cluster consolidation (Nov 2026): satellite pages folded into their main page."]
        for old, target in MERGED_TO.items():
            lines.append("/%s/* /%s/ 301!" % (old, target))
            lines.append("/%s /%s/ 301!" % (old, target))
        text = text.rstrip("\n") + "\n" + "\n".join(lines) + "\n"
        write(rel, text)


# --- 4. llms ----------------------------------------------------------------

def llms_txt():
    text = read("llms.txt")
    for old in MERGED_TO:
        text = re.sub(r"^- \[[^\]]*\]\(%s/%s/\)[^\n]*\n" % (re.escape(SITE), re.escape(old)), "", text, flags=re.M)
    write("llms.txt", text)


def page_to_text(rel):
    """Plain-text rendering of <main>, in the llms-full.txt house style."""
    src = read(rel)
    title = html.unescape(re.search(r"<title>(.*?)</title>", src).group(1))
    main = re.search(r'<main id="main-content">(.*?)</main>', src, re.S).group(1)
    main = re.sub(r'<nav class="breadcrumbs".*?</nav>', "", main, flags=re.S)
    main = re.sub(r"<!--.*?-->", "", main, flags=re.S)
    out = []
    for m in re.finditer(r"<(h1|h2|h3|p|li|tr|caption)\b[^>]*>(.*?)</\1>", main, re.S):
        tag, inner = m.group(1), m.group(2)
        if tag == "tr":
            cells = [strip_tags(c) for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", inner, re.S)]
            line = " ".join(c for c in cells if c)
        else:
            line = strip_tags(re.sub(r"<(ul|ol|table)\b.*?</\1>", "", inner, flags=re.S))
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        prefix = {"h1": "\n## ", "h2": "\n### ", "h3": "#### "}.get(tag, "")
        out.append(prefix + line)
    url = SITE + "/" + os.path.dirname(rel) + "/"
    return "## %s\nURL: %s\n\n%s\n" % (title, url, "\n".join(out))


def llms_full(targets):
    text = read("llms-full.txt")
    blocks = text.split("\n---\n\n")
    out = []
    for block in blocks:
        url = re.search(r"^URL: %s/([^\n]*)/$" % re.escape(SITE), block, re.M)
        slug = url.group(1) if url else None
        if slug in MERGED_TO:
            continue
        if slug in targets:
            block = page_to_text(page(slug))
        out.append(block)
    write("llms-full.txt", "\n---\n\n".join(out).rstrip("\n") + "\n")


# --- main -------------------------------------------------------------------

def main():
    missing = [old for old in MERGED_TO if not os.path.exists(os.path.join(ROOT, page(old)))]
    if missing and len(missing) != len(MERGED_TO):
        raise SystemExit("Partially applied; missing: %s" % ", ".join(missing))
    first_run = not missing

    if first_run:
        for target, sources in MERGES.items():
            build_target(target, sources)
            print("merged into %s: %s" % (target, ", ".join(s for s, _ in sources)))
    for slug, spec in RETITLE.items():
        retitle(slug, spec)
    for slug in PROOF:
        add_proof(slug)
    print("local proof added to %d pages" % len(PROOF))

    if first_run:
        for old in MERGED_TO:
            shutil.rmtree(os.path.join(ROOT, old))
        print("removed %d merged pages" % len(MERGED_TO))

    changed = 0
    for rel in all_html():
        text = read(rel)
        own = os.path.dirname(rel) or None
        new = rewrite_links(text, own)
        if new != text:
            write(rel, new)
            changed += 1
    print("rewrote links in %d files" % changed)

    add_redirects()
    llms_txt()
    llms_full(set(PROOF))
    print("redirects and llms files updated")


if __name__ == "__main__":
    main()
