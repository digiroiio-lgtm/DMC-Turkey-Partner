#!/usr/bin/env python3
"""Generate the COP31 cluster pages.

Usage: python3 tools/cop31_build.py
Writes <slug>/index.html for every page defined in the cop31_pages_* modules.
Re-running is safe: files are overwritten from the content definitions.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_render import ROOT, render  # noqa: E402


def collect():
    """Load every cop31_pages_*.py module in tools/ and concatenate its PAGES."""
    import glob
    import importlib

    here = os.path.dirname(os.path.abspath(__file__))
    pages = []
    for path in sorted(glob.glob(os.path.join(here, "cop31_pages_*.py"))):
        module = importlib.import_module(os.path.basename(path)[:-3])
        pages.extend(module.PAGES)
    return pages


# Keys whose values are plain text, not HTML. They are escaped on the way into
# the page and injected raw into JSON-LD, so an entity authored here would be
# double-escaped in one place and leak literally into structured data in the
# other. That is exactly the bug that once put "&amp;" in 21 page titles.
PLAIN_TEXT_KEYS = ("title", "description", "breadcrumb", "service_interest", "service_name")


def validate_pages(pages):
    bad = [
        (page["slug"], key, page[key])
        for page in pages
        for key in PLAIN_TEXT_KEYS
        if isinstance(page.get(key), str) and "&" in page[key] and ";" in page[key].split("&", 1)[1][:8]
    ]
    if bad:
        lines = "\n".join("  %s.%s: %s" % row for row in bad)
        raise SystemExit(
            "HTML entities found in plain-text page keys. These are escaped on "
            "the way into HTML and injected raw into JSON-LD, so they must be "
            "authored as literal characters:\n" + lines
        )


def main():
    pages = collect()
    slugs = [p["slug"] for p in pages]
    duplicates = {s for s in slugs if slugs.count(s) > 1}
    if duplicates:
        raise SystemExit("Duplicate slugs: %s" % ", ".join(sorted(duplicates)))
    validate_pages(pages)

    for page in pages:
        directory = os.path.join(ROOT, page["slug"])
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "index.html")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(render(page) + "\n")
        print("wrote %s/index.html" % page["slug"])
    print("%d COP31 pages generated" % len(pages))

    # Order matters below. Pages are regenerated from scratch, so anything that
    # patches them has to run afterwards or its edits are silently discarded.
    import cop31_evergreen_link
    import cop31_nav
    import cop31_news
    import llms_txt
    import page_schema
    import site_footer
    import site_head
    import sitemaps
    import site_seo

    # 1. News pages, which share the same chrome and must exist before the
    #    site-wide patchers sweep the tree.
    cop31_news.main()
    # 2. Footer normalisation first, because cop31_nav anchors on the
    #    Company column label and expects the <p> form.
    site_footer.main()
    # 3. Global nav/footer across every page, new ones included.
    cop31_nav.main()
    # 4. Identity and measurement, since generated pages build their own <head>.
    site_seo.main()
    # 5. The news -> evergreen loop, which edits the guides just regenerated.
    cop31_evergreen_link.main()
    # 6. Per-page schema. After the evergreen linker, because it derives the
    #    graph from the finished markup and the linker still edits headings
    #    and dates. Its own fence keeps it clear of the identity block.
    page_schema.main()
    # 7. Head meta, which reads the h1, lede and schema dates the steps above
    #    settled.
    site_head.main()
    # 8. The AI-client index, derived from the finished pages.
    llms_txt.main()
    # 9. Sitemap coverage and lastmod, last so it sees the final state.
    sitemaps.main()


if __name__ == "__main__":
    main()
