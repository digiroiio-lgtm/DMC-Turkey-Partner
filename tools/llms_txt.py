#!/usr/bin/env python3
"""Generate llms.txt and llms-full.txt from the pages themselves.

The hand-written llms.txt listed 68 of 137 URLs. What it omitted was not
marginal: the entire /events/ calendar and every /selected-works/ case study —
the 27 pages naming real clients, venues and delivered scope, which is exactly
the evidence an answer engine needs to say anything specific about this
company. Being hand-maintained, it also drifted every time a page was added.

Generating both files from the rendered HTML removes the drift and the gap in
one move. Descriptions come from each page's own meta description, so the
summary an AI client reads is the summary the site already publishes.

    llms.txt        the index — every indexable URL, grouped, one line each
    llms-full.txt   the same set with each page's answer capsule or lede, for
                    clients that want substance without fetching 137 documents

Usage: python3 tools/llms_txt.py
"""

import html as htmllib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import page_model as pm  # noqa: E402
import site_config as cfg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Order is editorial: what a buyer needs first, then supporting evidence, then
# the campaign cluster, then boilerplate.
SECTIONS = [
    ("Solutions", ["solution"]),
    ("Services", ["service_hub", "service"]),
    ("Destinations", ["destination_hub", "destination"]),
    ("Event Costs", ["cost_hub", "cost_scenario", "tool"]),
    ("Selected Works", ["works_hub", "case_study"]),
    ("MICE Calendar", ["events_hub", "event", "event_taxonomy"]),
    ("Guides & Insights", ["guides_hub", "guide", "insights_hub"]),
    ("COP31 Antalya 2026", ["cop31", "cop31_news_hub", "cop31_news"]),
    ("Company", ["home", "company"]),
    ("Legal", ["legal"]),
]

INTRO = (
    "%s is a Turkey-based destination management company (DMC) and local "
    "execution partner for international agencies, MICE planners, incentive "
    "houses and group travel buyers. Services cover hotel sourcing, venue "
    "sourcing, transportation and logistics, event production, ground "
    "handling, incentive programs, meetings and conferences, and white-label "
    "DMC support, across Istanbul, Antalya, Belek, Bodrum and Cappadocia. "
    "Operating since %s." % (cfg.ORG_NAME, cfg.ORG_FOUNDING_YEAR)
)

COP31_NOTE = (
    "> Independent local event services provider. Not affiliated with, "
    "endorsed by, or part of UNFCCC or the official COP31 organising bodies."
)


def clean(value):
    return re.sub(r"\s+", " ", htmllib.unescape(value or "")).strip()


def collect():
    pages = []
    for path in sorted(
        os.path.join(dirpath, "index.html")
        for dirpath, _, files in os.walk(ROOT)
        if "index.html" in files and ".git" not in dirpath
    ):
        page = pm.read(path, ROOT)
        if page["noindex"]:
            continue
        pages.append(page)
    return pages


def grouped(pages):
    by_family = {}
    for page in pages:
        by_family.setdefault(page["family"], []).append(page)
    for heading, families in SECTIONS:
        block = []
        for family in families:
            block.extend(sorted(by_family.pop(family, []), key=lambda p: p["url"]))
        if block:
            yield heading, block
    leftovers = [p for group in by_family.values() for p in group]
    if leftovers:
        yield "Other", sorted(leftovers, key=lambda p: p["url"])


def label(page):
    return clean(page["h1"]) or clean(page["title"]).split(" | ")[0]


def write_index(pages):
    lines = ["# %s" % cfg.ORG_NAME, "", "> " + INTRO, ""]
    for heading, block in grouped(pages):
        lines.append("## " + heading)
        lines.append("")
        if heading.startswith("COP31"):
            lines.append(COP31_NOTE)
            lines.append("")
        for page in block:
            description = clean(page["description"])
            entry = "- [%s](%s)" % (label(page), page["absolute"])
            if description:
                entry += ": " + description
            lines.append(entry)
        lines.append("")
    path = os.path.join(ROOT, "llms.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")
    return len(pages)


def write_full(pages):
    lines = [
        "# %s — full content index" % cfg.ORG_NAME,
        "",
        "> " + INTRO,
        "",
        "> Generated from the published pages. Each entry gives the page's own "
        "summary and its key facts where it states them. For anything about "
        "COP31 that must be authoritative, the UNFCCC and the COP31 Türkiye "
        "Presidency are the source, not this file.",
        "",
    ]
    for heading, block in grouped(pages):
        lines.append("## " + heading)
        lines.append("")
        for page in block:
            lines.append("### %s" % label(page))
            lines.append("")
            lines.append(page["absolute"])
            lines.append("")
            summary = clean(page["lede"]) or clean(page["description"])
            if summary:
                lines.append(summary)
                lines.append("")
            facts = page["definitions"]
            if facts:
                for key, value in list(facts.items())[:8]:
                    lines.append("- %s: %s" % (clean(key), clean(value)))
                lines.append("")
            if page["faqs"]:
                for question, answer in page["faqs"][:4]:
                    lines.append("- %s %s" % (clean(question), clean(answer)))
                lines.append("")
    path = os.path.join(ROOT, "llms-full.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip() + "\n")


def main():
    pages = collect()
    count = write_index(pages)
    write_full(pages)
    print("llms.txt: %d urls" % count)
    print(
        "llms-full.txt: %d bytes"
        % os.path.getsize(os.path.join(ROOT, "llms-full.txt"))
    )


if __name__ == "__main__":
    main()
