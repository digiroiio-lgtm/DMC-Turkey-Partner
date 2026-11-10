#!/usr/bin/env python3
"""Keep the sitemaps complete and stamped with accurate lastmod dates.

Two jobs:

1. Coverage — every indexable page must appear in exactly one sitemap, and no
   sitemap may list a page that is noindex or missing. Search Console reports
   both as errors.
2. Freshness — <lastmod> is the page's own dateModified / "Last updated"
   date, omitted when the page carries no date, so it only moves when content
   changes (commit dates move on every site-wide nav/footer patch). Google uses it to prioritise
   recrawls; a stamp that is invented or always "today" is worse than none.

Usage: python3 tools/sitemaps.py [--check]
"""

import glob
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"

# Pages that are indexable but belong in no topical sitemap go here.
DEFAULT_SITEMAP = "sitemap-pages.xml"


def _shallow_roots():
    """Commits at the edge of a shallow clone. Their dates say nothing about
    when a file last changed, so a file whose last commit is one of them has
    no trustworthy git date."""
    path = os.path.join(ROOT, ".git", "shallow")
    if not os.path.exists(path):
        return set()
    with open(path) as handle:
        return {line.strip() for line in handle if line.strip()}


SHALLOW_ROOTS = _shallow_roots()
# Pages carrying a date before the site launched are placeholders, not edits.
EARLIEST = "2026-08-01"


def git_lastmod(rel_path):
    """Last commit date for a file, or None if unknown or not committed yet."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%H %cs", "--", rel_path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except subprocess.CalledProcessError:
        return None
    if not out:
        return None
    sha, date = out.split()
    return None if sha in SHALLOW_ROOTS else date


MONTHS = {m: i for i, m in enumerate(
    "January February March April May June July August September October November December".split(), 1)}


def page_lastmod(rel_path):
    """The page's own modification date: JSON-LD dateModified, else a visible
    "Last updated: 6 September 2026" line."""
    with open(os.path.join(ROOT, rel_path), encoding="utf-8") as handle:
        text = handle.read()
    dates = re.findall(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})', text)
    for day, month, year in re.findall(r"Last updated:?\s*(?:<[^>]+>\s*)*(\d{1,2}) ([A-Z][a-z]+) (\d{4})", text):
        if month in MONTHS:
            dates.append("%s-%02d-%02d" % (year, MONTHS[month], int(day)))
    dates = [d for d in dates if d >= EARLIEST]
    return max(dates) if dates else None


def lastmod_for(rel_path):
    """The page's own date, or no <lastmod> at all.

    Commit dates over-report freshness: site-wide nav/footer patches touch
    every file, which stamped 120+ pages with the same day, and search engines
    learn to ignore lastmod that moves without content changes. A missing
    lastmod is harmless; a misleading one is not. git_lastmod is kept for
    callers that want the raw commit date."""
    return page_lastmod(rel_path)


def url_for(path):
    directory = os.path.dirname(path)
    return "/" + directory + "/" if directory else "/"


def indexable_pages():
    pages = {}
    for path in sorted(glob.glob("**/index.html", recursive=True, root_dir=ROOT)):
        with open(os.path.join(ROOT, path), encoding="utf-8") as handle:
            html = handle.read()
        if re.search(r'name="robots" content="noindex', html):
            continue
        pages[url_for(path)] = path
    return pages


def sitemap_urls(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as handle:
        return re.findall(r"<loc>" + re.escape(SITE) + r"([^<]*)</loc>", handle.read())


def write_sitemap(name, urls, pages):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url in urls:
        lines.append("  <url>")
        lines.append("    <loc>%s%s</loc>" % (SITE, url))
        source = pages.get(url)
        lastmod = lastmod_for(source) if source else None
        if lastmod:
            lines.append("    <lastmod>%s</lastmod>" % lastmod)
        lines.append("  </url>")
    lines.append("</urlset>")
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def main():
    check_only = "--check" in sys.argv
    pages = indexable_pages()
    sitemaps = sorted(
        os.path.basename(p) for p in glob.glob(os.path.join(ROOT, "sitemap-*.xml"))
    )

    listed = {}
    for name in sitemaps:
        for url in sitemap_urls(name):
            listed.setdefault(url, []).append(name)

    stale = sorted(url for url in listed if url not in pages)
    missing = sorted(url for url in pages if url not in listed)
    duplicated = sorted(url for url, names in listed.items() if len(names) > 1)

    for label, values in (
        ("listed but not indexable", stale),
        ("indexable but unlisted", missing),
        ("listed in more than one sitemap", duplicated),
    ):
        print("%s: %s" % (label, ", ".join(values) if values else "none"))

    if check_only:
        return 1 if (stale or missing or duplicated) else 0

    for url in missing:
        listed.setdefault(url, []).append(DEFAULT_SITEMAP)

    for name in sitemaps:
        urls = [u for u in sitemap_urls(name) if u in pages]
        urls += [u for u in missing if DEFAULT_SITEMAP == name]
        # Preserve the existing order, appending anything new at the end.
        seen = set()
        ordered = [u for u in urls if not (u in seen or seen.add(u))]
        write_sitemap(name, ordered, pages)
        print("  %-30s %d urls" % (name, len(ordered)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
