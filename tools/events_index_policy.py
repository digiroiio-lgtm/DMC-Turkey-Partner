#!/usr/bin/env python3
"""Withhold the index request from /events/ facets that have nothing to list.

Search Console reported 15 URLs as "Discovered - currently not indexed", which
means Google knows the URL and decided it was not worth crawling. The facet
pages are the clearest cause. /events/berlin/ is 121 words, lists exactly one
event, and carries fifteen words that are not already on the /events/ hub. That
event has its own page. There is nothing there for Google that it cannot get
better elsewhere, so asking for it to be indexed spends crawl budget on a URL
that will be declined anyway.

The rule is a threshold rather than a hand-kept list, because a list would be a
second copy of the truth and would rot. A facet listing fewer than MINIMUM
events gets "noindex, follow"; one listing MINIMUM or more gets "index,
follow". When IMEX Frankfurt 2028 is added, /events/frankfurt/ crosses the line
and re-enters the index on the next build with no one having to remember.

"follow" matters: the pages stay in the nav and keep passing link equity to the
event pages they list. Only the index request is withdrawn, not the page.

The rest of the toolchain then does the right thing for free — sitemaps.py
drops noindex pages from the sitemap, page_schema.py and answer_capsule.py skip
them and clear any block they left behind, and llms_txt.py leaves them out.

Usage: python3 tools/events_index_policy.py [--dry-run]
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import page_model as pm  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Two listed events is the point at which a facet starts saying something the
# hub does not: it groups. One is a pointer to a page that already exists.
MINIMUM = 3

ROBOTS = re.compile(r'<meta name="robots" content="[^"]*">')


def main():
    dry_run = "--dry-run" in sys.argv
    changed = 0
    rows = []

    for path in mb.iter_pages(ROOT, "events/*/index.html"):
        page = pm.read(path, ROOT)
        if page["family"] != "event_taxonomy":
            continue

        listed = len(page["cards"])
        wanted = "index, follow" if listed >= MINIMUM else "noindex, follow"
        rows.append((page["url"], listed, wanted))

        original = page["html"]
        html = ROBOTS.sub('<meta name="robots" content="%s">' % wanted, original, count=1)

        if dry_run:
            if html != original:
                changed += 1
            continue
        if mb.write_if_changed(path, original, html):
            changed += 1

    for url, listed, wanted in sorted(rows):
        print("  %-34s %2d listed  %s" % (url, listed, wanted))
    print(
        "events index policy: %d of %d facets changed (threshold: %d listed events)"
        % (changed, len(rows), MINIMUM)
    )


if __name__ == "__main__":
    main()
