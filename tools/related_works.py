#!/usr/bin/env python3
"""Cross-link the case studies to each other.

Each of the 27 /selected-works/ pages had exactly one contextual inbound link —
its own hub — and ended with the same two-link line: the MICE Turkey page and
back to the hub. So the cluster was 27 leaves hanging off one node, with no
path between them. A reader who found the Swarovski project had no route to the
other Belek work, and a crawler had no signal that those pages belong together.

Relatedness is derived from the project data the pages already publish in their
<dl class="work-info">: same event type first, then same destination. Nothing is
invented and nothing is hand-maintained — correct a venue or a category in the
markup and the links follow on the next build.

Usage: python3 tools/related_works.py [--dry-run]
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import page_model as pm  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = "related-works"
MAX_LINKS = 4

# The line every case study already ends with; the block goes above it.
ANCHOR = '<p class="work-related">'


def city(value):
    """"Belek, Antalya" and "Antalya" should match on the leading locality."""
    return (value or "").split(",")[0].strip().lower()


def score(a, b):
    """How related two projects are. Event type outranks destination."""
    points = 0
    if a["type"] and a["type"] == b["type"]:
        points += 2
    if a["city"] and a["city"] == b["city"]:
        points += 1
    return points


def collect():
    works = []
    for path in mb.iter_pages(ROOT, "selected-works/*/index.html"):
        page = pm.read(path, ROOT)
        if page["family"] != "case_study" or page["noindex"]:
            continue
        facts = page["definitions"]
        works.append(
            {
                "path": path,
                "url": page["url"],
                "name": page["h1"],
                "type": (facts.get("Event Type") or "").strip(),
                "city": city(facts.get("Destination")),
                "venue": (facts.get("Venue") or "").strip(),
            }
        )
    return works


def related(work, works):
    scored = [
        (score(work, other), other)
        for other in works
        if other["url"] != work["url"]
    ]
    scored = [(points, other) for points, other in scored if points > 0]
    # Sort by relatedness, then by name so the output is stable between runs.
    scored.sort(key=lambda pair: (-pair[0], pair[1]["name"]))
    return [other for _, other in scored[:MAX_LINKS]]


def render(work, picks):
    items = "".join(
        '\n        <li><a href="%s">%s</a>%s</li>'
        % (
            other["url"],
            other["name"],
            " <span>%s</span>" % other["venue"] if other["venue"] else "",
        )
        for other in picks
    )
    return (
        "      %s\n"
        '      <section class="page-section">\n'
        "        <h2>Related Work</h2>\n"
        '        <ul class="work-related-list">%s\n'
        "        </ul>\n"
        "      </section>\n"
        "      %s\n      " % (mb.begin(FENCE), items, mb.end(FENCE))
    )


def main():
    dry_run = "--dry-run" in sys.argv
    works = collect()
    changed = 0

    for work in works:
        picks = related(work, works)
        with open(work["path"], encoding="utf-8") as handle:
            original = handle.read()

        html = mb.strip(original, FENCE)
        if picks and ANCHOR in html:
            at = html.rindex("<section", 0, html.index(ANCHOR))
            html = html[:at] + render(work, picks).lstrip() + html[at:]

        if dry_run:
            if html != original:
                changed += 1
                print(
                    "%-52s -> %s"
                    % (work["url"], ", ".join(p["url"] for p in picks))
                )
            continue
        if mb.write_if_changed(work["path"], original, html):
            changed += 1

    print("related works: %d of %d case studies changed" % (changed, len(works)))


if __name__ == "__main__":
    main()
