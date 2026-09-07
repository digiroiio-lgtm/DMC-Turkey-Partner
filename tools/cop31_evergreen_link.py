#!/usr/bin/env python3
"""Close the news -> evergreen loop.

Each news article names the evergreen guides it feeds. This inserts a "Latest
update" strip into those guides pointing at the newest article that feeds them,
and refreshes the guide's Last updated date to the article's date.

The strip is marker-delimited so re-running replaces it rather than stacking
copies, and the whole thing is derived from cop31_news_data — there is no
second list to keep in sync.

Usage: python3 tools/cop31_evergreen_link.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_news import NEWS_ROOT, human_date  # noqa: E402
from cop31_news_data import ARTICLES  # noqa: E402
from cop31_render import ROOT  # noqa: E402

BEGIN = "<!-- cop31-latest:begin -->"
END = "<!-- cop31-latest:end -->"
# Anchor: the strip goes directly after the hero section's CTA row.
HERO_ACTIONS = re.compile(r'(<div class="hero-actions">.*?</div>\n)', re.S)


def newest_by_guide():
    """guide path -> the most recently updated article feeding it."""
    latest = {}
    for article in sorted(ARTICLES, key=lambda a: a["updated"]):
        for path, _ in article["evergreen"]:
            latest[path] = article
    return latest


def strip_html(article):
    return (
        "      " + BEGIN + "\n"
        '      <aside class="news-latest">\n'
        '        <p class="news-latest__label">Latest COP31 update</p>\n'
        '        <p><a href="%s%s/">%s</a></p>\n'
        '        <p class="reviewed-note">Reported %s. Sources are listed on the update.</p>\n'
        "      </aside>\n"
        "      " + END + "\n"
    ) % (NEWS_ROOT, article["slug"], article["title"], human_date(article["updated"]))


def patch(path, article):
    full = os.path.join(ROOT, path.strip("/"), "index.html")
    if not os.path.exists(full):
        raise SystemExit("Missing evergreen page: %s" % path)
    with open(full, encoding="utf-8") as handle:
        original = handle.read()

    # One pass that also eats the leading indent, so re-running is a true no-op
    # rather than leaving whitespace behind and rewriting the file every time.
    html = re.sub(
        r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n",
        "",
        original,
        flags=re.S,
    )

    match = HERO_ACTIONS.search(html)
    if not match:
        raise SystemExit("No hero actions block in %s" % path)
    html = html[: match.end()] + strip_html(article) + html[match.end():]

    # Freshness: the guide now carries information dated by the update.
    html = re.sub(
        r'(Last updated: <time datetime=")[0-9-]+(">)[^<]+(</time>)',
        lambda m: m.group(1) + article["updated"] + m.group(2)
        + human_date(article["updated"]) + m.group(3),
        html,
    )

    if html == original:
        return False
    with open(full, "w", encoding="utf-8") as handle:
        handle.write(html)
    return True


def main():
    latest = newest_by_guide()
    changed = 0
    for path, article in sorted(latest.items()):
        if patch(path, article):
            changed += 1
        print("  %-38s <- %s" % (path, article["slug"]))
    print("evergreen pages linked to news: %d of %d changed" % (changed, len(latest)))


if __name__ == "__main__":
    main()
