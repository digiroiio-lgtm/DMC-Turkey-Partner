#!/usr/bin/env python3
"""Title and heading wording for queries already ranking 10–30 (Sprint 1, Nov 2026).

Search Console, 24 Aug – 22 Nov 2026:
  conference equipment rental antalya (pos 10), meeting equipment rental
  antalya (14), event technology rental antalya (18), conference av antalya
  (19), av rental antalya (25), technical event production antalya (29)
  -> /antalya-event-production/
  dmc bodrum (12), bodrum incentive travel (18) -> /destinations/bodrum/
  turkey incentive travel (22, 129 impressions) -> /incentive-travel-turkey/

Each (old, new) pair is replaced where found; re-running is a no-op.
Each page keeps its keyword_map.py lead keyword.

Usage: python3 tools/gsc_quickwins.py
"""

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EP_TITLE_OLD = "Event Production &amp; AV Rental Antalya | Staging, LED, Sound"
EP_TITLE_NEW = "Event Production &amp; AV Equipment Rental Antalya | Conference AV"
EP_DESC_OLD = ("Event production and AV rental in Antalya for conferences, corporate events and receptions: "
               "staging, LED screens, sound, lighting, technicians and hire ranges.")
EP_DESC_NEW = ("Event production and conference AV equipment rental in Antalya: staging, LED screens, sound "
               "and lighting rental, event technology and technicians, with day-rate hire ranges.")
BD_OLD = "DMC Bodrum | Incentives, Retreats &amp; Corporate Groups"
BD_NEW = "DMC Bodrum | Incentive Travel, Retreats &amp; Corporate Groups"
IN_OLD = "Incentive Travel Turkey | Reward Trips &amp; Programme Execution"
IN_NEW = "Incentive Travel Turkey | Incentive Trips &amp; Programme Execution"

EDITS = {
    "antalya-event-production": [
        (EP_TITLE_OLD, EP_TITLE_NEW),
        (EP_DESC_OLD, EP_DESC_NEW),
        ("<h2>AV Equipment We Supply</h2>", "<h2>Conference AV and Event Equipment Rental</h2>"),
        ('>AV Equipment We Supply</a>', '>Conference AV and Event Equipment Rental</a>'),
        ("<h2>Typical AV Hire Ranges</h2>", "<h2>AV, Sound and Lighting Rental Prices in Antalya</h2>"),
        ('>Typical AV Hire Ranges</a>', '>AV, Sound and Lighting Rental Prices in Antalya</a>'),
    ],
    "destinations/bodrum": [(BD_OLD, BD_NEW)],
    "incentive-travel-turkey": [(IN_OLD, IN_NEW)],
}


def main():
    changed = 0
    for rel, pairs in EDITS.items():
        path = os.path.join(ROOT, rel, "index.html")
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        text = original
        for old, new in pairs:
            text = text.replace(old, new)
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("quick-win titles: %d pages changed" % changed)


if __name__ == "__main__":
    main()
