#!/usr/bin/env python3
"""Keep the sitemaps complete and stamped with accurate lastmod dates.

Two jobs:

1. Coverage — every indexable page must appear in exactly one sitemap, and no
   sitemap may list a page that is noindex or missing. Search Console reports
   both as errors.
2. Freshness — <lastmod> is taken from the file's last git commit date, so it
   reflects when the content actually changed. Google uses it to prioritise
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


def git_lastmod(rel_path):
    """Last commit date for a file, or None if it is not committed yet."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel_path],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        return out or None
    except subprocess.CalledProcessError:
        return None


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
        lastmod = git_lastmod(source) if source else None
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
