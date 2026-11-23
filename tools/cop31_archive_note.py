#!/usr/bin/env python3
"""Archive note on the COP31 guides after the conference (20 November 2026).

COP31 is over. The hub, participant guide, venue, hotels, event-services and
news pages stay online as an information archive; this adds one short note
directly under each page's H1 saying the conference has taken place, and
pointing to the permanent Antalya service pages.

Marker-delimited and idempotent. Noindex pages are skipped.

Usage: python3 tools/cop31_archive_note.py
"""

import glob
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- cop31-archive:begin -->", "<!-- cop31-archive:end -->"
PAGES = re.compile(r"^(cop31-[^/]+(/[^/]+)?|insights/cop31-[^/]+)$")

NOTE = (
    '<p class="reviewed-note"><strong>COP31 took place in Antalya from 9 to 20 November 2026.</strong> '
    "This page is kept as a reference archive and is no longer updated. For event support in Antalya now, see "
    '<a href="/antalya-event-production/">event production</a>, '
    '<a href="/exhibition-stands-antalya/">exhibition stands</a>, '
    '<a href="/event-staff-antalya/">event staff</a> and '
    '<a href="/antalya-airport-transfers-group-transport/">airport transfers &amp; group transport</a>.</p>'
)


def main():
    changed = total = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(path), ROOT)
        if not PAGES.match(rel):
            continue
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        if 'name="robots" content="noindex' in original:
            continue
        total += 1
        text = re.sub(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", "", original, flags=re.S)
        m = re.search(r"</h1>\n?", text)
        if not m:
            raise SystemExit("no <h1> on %s" % rel)
        text = text[:m.end()] + ("" if text[m.end() - 1] == "\n" else "\n") + \
            "      %s\n      %s\n      %s\n" % (BEGIN, NOTE, END) + text[m.end():]
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("archive note on %d COP31 pages (%d changed)" % (total, changed))


if __name__ == "__main__":
    main()
