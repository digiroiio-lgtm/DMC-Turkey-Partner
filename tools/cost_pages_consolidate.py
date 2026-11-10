#!/usr/bin/env python3
"""Fold the event-cost cluster from 13 pages to 5 (November 2026).

The scenario pages (60/100/200-person examples) and the programme-type pages
(conferences, corporate events, incentive travel) were ~400 words each and
shared 35–47% of their text with each other. Their distinctive sections — the
programme snapshot and budget breakdown, the per-person ranges and cost
drivers — move onto the city pages and the hub under an anchor named after
the old slug. The old URLs 301 to that anchor.

Kept: /event-costs/, /event-costs/antalya/, /event-costs/belek/,
/event-costs/istanbul/ and /event-cost-calculator/.

Usage: python3 tools/cost_pages_consolidate.py   (no-op once applied)
"""

import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"

SCENARIO = ["Programme Snapshot", "Example Budget Breakdown"]
TYPE = ["Published Per-Person Ranges", "What Drives the Budget"]

# target page -> [(source path, sections to move, heading prefix)]
MERGES = {
    "event-costs/antalya": [
        ("event-costs/antalya/60-person-corporate-event", SCENARIO, "60-Person Corporate Event"),
        ("event-costs/antalya/100-person-incentive-trip", SCENARIO, "100-Person Incentive Trip"),
        ("event-costs/antalya/200-person-conference", SCENARIO, "200-Person Conference"),
    ],
    "event-costs/belek": [
        ("event-costs/belek/100-person-corporate-retreat", SCENARIO, "100-Person Corporate Retreat"),
    ],
    "event-costs/istanbul": [
        ("event-costs/istanbul/100-person-corporate-event", SCENARIO, "100-Person Corporate Event"),
    ],
    "event-costs": [
        ("event-costs/corporate-events", TYPE, "Corporate Event Costs"),
        ("event-costs/incentive-travel", TYPE, "Incentive Trip Costs"),
        ("event-costs/conferences", TYPE, "Conference Costs"),
    ],
}

# Sections are inserted before the first of these headings on the target.
BEFORE = ["Relevant Selected Works", "Why Budgets Vary", "Build a Programme Around My Budget"]


def anchor(src):
    return src.rsplit("/", 1)[1]


MOVED = {src: "/%s/#%s" % (target, anchor(src)) for target, items in MERGES.items() for src, _, _ in items}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as handle:
        return handle.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as handle:
        handle.write(text)


def section(src_html, heading):
    m = re.search(
        r'[ \t]*<section class="page-section">\s*<h2>%s</h2>.*?</section>\n' % re.escape(heading),
        src_html, re.S,
    )
    if not m:
        raise SystemExit("Section %r not found" % heading)
    return m.group(0)


def merge(target, items):
    rel = target + "/index.html"
    text = read(rel)
    if 'id="%s"' % anchor(items[0][0]) in text:
        return
    blocks = []
    for src, headings, prefix in items:
        src_html = read(src + "/index.html")
        for i, heading in enumerate(headings):
            block = section(src_html, heading)
            block = block.replace("<h2>%s</h2>" % heading, "<h2>%s: %s</h2>" % (prefix, heading), 1)
            if i == 0:
                block = block.replace('<section class="page-section">', '<section class="page-section" id="%s">' % anchor(src), 1)
            blocks.append(block)
    for heading in BEFORE:
        m = re.search(r'[ \t]*<section class="page-section[^"]*">\s*<h2>%s</h2>' % re.escape(heading), text)
        if m:
            text = text[:m.start()] + "".join(blocks) + text[m.start():]
            break
    else:
        raise SystemExit("No insertion point on %s" % rel)
    write(rel, text)


def rewrite_links(text, own):
    for src, dest in MOVED.items():
        page, frag = dest.split("#")
        new = ("#" + frag) if page == own else dest
        for prefix in ("", SITE):
            text = text.replace('href="%s/%s/"' % (prefix, src), 'href="%s"' % new)
    return text


def html_files():
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for name in files:
            if name.endswith(".html"):
                yield os.path.relpath(os.path.join(base, name), ROOT)


def redirects():
    data = json.loads(read("vercel.json"))
    have = {r["source"] for r in data["redirects"]}
    for src, dest in MOVED.items():
        for source in ("/" + src, "/%s/:path*" % src):
            if source not in have:
                data["redirects"].append({"source": source, "destination": dest, "statusCode": 301})
    write("vercel.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    text = read("_redirects")
    if "Event cost consolidation" not in text:
        lines = ["", "# Event cost consolidation (Nov 2026): scenario and programme-type pages folded in."]
        for src, dest in MOVED.items():
            lines += ["/%s/* %s 301!" % (src, dest), "/%s %s 301!" % (src, dest)]
        write("_redirects", text.rstrip("\n") + "\n" + "\n".join(lines) + "\n")


def llms_full():
    text = read("llms-full.txt")
    blocks = text.split("\n---\n\n")
    gone = {SITE + "/" + src + "/" for src in MOVED}
    kept = [b for b in blocks if not any("\nURL: %s\n" % u in "\n" + b + "\n" for u in gone)]
    write("llms-full.txt", "\n---\n\n".join(kept))


def main():
    first_run = all(os.path.exists(os.path.join(ROOT, src, "index.html")) for src in MOVED)
    if first_run:
        for target, items in MERGES.items():
            merge(target, items)
        for src in MOVED:
            shutil.rmtree(os.path.join(ROOT, src))
    changed = 0
    for rel in html_files():
        own = "/" + os.path.dirname(rel) + "/"
        text = read(rel)
        new = rewrite_links(text, own)
        if new != text:
            write(rel, new)
            changed += 1
    redirects()
    llms_full()
    print("folded %d cost pages; rewrote links in %d files" % (len(MOVED), changed))


if __name__ == "__main__":
    main()
