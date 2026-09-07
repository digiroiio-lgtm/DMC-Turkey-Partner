#!/usr/bin/env python3
"""Fill in the head tags that were missing from every page.

Zero of 137 pages carried og:locale, twitter:title, twitter:description,
og:image dimensions or a theme-color meta, and on 136 of them the og and
twitter descriptions were byte-identical copies of the meta description — so a
shared link showed the same sentence the search result already showed.

Nothing here is invented. twitter:title comes from the page's <h1>, which is
shorter and more human than the pipe-stuffed <title>; twitter:description
comes from the page's own lede paragraph. Both are copy the owner already
wrote for that page, just not previously exposed to the social crawlers. The
theme colour is read from site.webmanifest rather than picked.

Titles and descriptions are deliberately NOT rewritten here. 69 titles run
long and 56 descriptions do, but those are content decisions with ranking
consequences; tools/seo_check.py reports them and a human edits them. A script
that silently rewrites titles is how you lose positions.

Usage: python3 tools/site_head.py [--dry-run]
"""

import html as htmllib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import page_model as pm  # noqa: E402
import site_config as cfg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = "head-meta"

OG_IMAGE_WIDTH = "1200"
OG_IMAGE_HEIGHT = "630"
OG_IMAGE_TYPE = "image/png"


def theme_color():
    """From the manifest, so the two can never disagree."""
    with open(os.path.join(ROOT, "site.webmanifest"), encoding="utf-8") as handle:
        return json.load(handle).get("theme_color")


def esc(value):
    """Escape for an attribute, idempotently — never re-escape an entity."""
    value = re.sub(r"&(?!(?:[A-Za-z][A-Za-z0-9]{1,31}|#\d{1,7}|#[xX][0-9A-Fa-f]{1,6});)", "&amp;", value)
    return value.replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def first_sentences(text, limit=200):
    """Trim to a sentence boundary rather than mid-word."""
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[:limit]
    for stop in (". ", "? ", "! "):
        index = cut.rfind(stop)
        if index > 80:
            return cut[: index + 1].strip()
    return cut[: cut.rfind(" ")].rstrip(",;:") + "…"


def already_present(html, tag_attr, name):
    """True if the page sets this tag outside every managed fence.

    Keeps a future hand-edit from ending up duplicated by this patcher.
    """
    pattern = re.compile(r'<meta\s+%s="%s"' % (tag_attr, re.escape(name)))
    return any(pattern.search(html[start:stop]) for start, stop in mb.outside_fences(html))


def build_block(page, html, colour):
    lines = [mb.begin(FENCE)]

    def add(attr, name, value):
        if value and not already_present(html, attr, name):
            lines.append('  <meta %s="%s" content="%s">' % (attr, name, esc(value)))

    # The site is English-only and says so in every inLanguage; x-default is
    # not emitted because there is no alternate to default away from.
    add("property", "og:locale", "en_GB")
    add("property", "og:image:width", OG_IMAGE_WIDTH)
    add("property", "og:image:height", OG_IMAGE_HEIGHT)
    add("property", "og:image:type", OG_IMAGE_TYPE)

    # A social card wants the page's own headline and standfirst, not the
    # SERP-tuned title and description repeated.
    add("name", "twitter:title", htmllib.unescape(page["h1"]) or None)
    lede = page["lede"] or page["description"]
    add("name", "twitter:description", first_sentences(htmllib.unescape(lede)) if lede else None)

    add("name", "theme-color", colour)
    add("name", "author", cfg.ORG_NAME)

    stamp = page["html"]
    published = re.search(r'"datePublished": ?"([\d-]+)"', stamp)
    modified = re.search(r'"dateModified": ?"([\d-]+)"', stamp)
    if published:
        add("property", "article:published_time", published.group(1))
    if modified:
        add("property", "article:modified_time", modified.group(1))

    lines.append("  " + mb.end(FENCE))
    return "\n".join(lines) + "\n"


def main():
    dry_run = "--dry-run" in sys.argv
    colour = theme_color()
    changed = total = 0

    for path in mb.iter_pages(ROOT):
        page = pm.read(path, ROOT)
        original = page["html"]
        total += 1

        stripped = mb.strip(original, FENCE)
        block = build_block(page, stripped, colour)
        html = mb.insert(stripped, FENCE, block, path)

        if dry_run:
            if html != original:
                changed += 1
                print("would change %s" % page["rel"])
            continue
        if mb.write_if_changed(path, original, html):
            changed += 1

    print("head meta: %d of %d pages changed" % (changed, total))


if __name__ == "__main__":
    main()
