#!/usr/bin/env python3
""""Planning Guides" links from service and destination pages to the guides.

Internal-link audit (Sprint 1, November 2026): guides linked to service pages,
but service pages linked back to almost no guide, and several guide pages
(off-season destinations, group hotel offers, trade-show pages, insights) had
only one or two in-content links. Each page below gets one short block of
3–6 relevant guide links, placed directly after its FAQ (or, without one,
before its closing call-to-action).

Marker-delimited and idempotent. Pages rebuilt in full by builders (hotel
offers, transfer prices, off-season, fam trip, market and Czech pages) are
not targets.

Usage: python3 tools/related_guides.py
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- related-guides:begin -->", "<!-- related-guides:end -->"

G = {
    "mice": ("/guides/mice-in-turkey/", "The Complete Guide to MICE in Turkey"),
    "cost": ("/insights/turkey-mice-cost-guide-2026/", "Turkey Corporate Event Costs 2026"),
    "costs": ("/event-costs/", "Turkey Event Cost Guide"),
    "cost-antalya": ("/event-costs/antalya/", "Antalya Event Costs"),
    "cost-belek": ("/event-costs/belek/", "Belek Event Costs"),
    "cost-istanbul": ("/event-costs/istanbul/", "Istanbul Event Costs"),
    "incentive": ("/insights/incentive-travel-turkey-destination-guide/", "Why Agencies Choose Turkey for Incentive Travel"),
    "offseason": ("/off-season-events-turkey/", "Off-Season Events in Turkey"),
    "os-antalya": ("/off-season-events-turkey/antalya/", "Off-Season Events in Antalya"),
    "os-belek": ("/off-season-events-turkey/belek/", "Off-Season Events in Belek"),
    "os-bodrum": ("/off-season-events-turkey/bodrum/", "Off-Season Events in Bodrum"),
    "os-cappadocia": ("/off-season-events-turkey/cappadocia/", "Off-Season Events in Cappadocia"),
    "os-istanbul": ("/off-season-events-turkey/istanbul/", "Off-Season Events in Istanbul"),
    "why": ("/why-turkey/", "Why Turkey for MICE"),
    "events": ("/events/", "MICE Events Calendar 2026–2027"),
    "wtm": ("/events/wtm-london-2026/", "WTM London 2026"),
    "ibtm": ("/events/ibtm-world-2026/", "IBTM World 2026"),
    "imex": ("/events/imex-frankfurt/", "IMEX Frankfurt"),
    "itb": ("/events/itb-berlin-2026/", "ITB Berlin 2026"),
    "transfers": ("/antalya-transfer-prices/", "Antalya Transfer Prices"),
    "hotels": ("/group-hotel-offers-turkey/", "Group Hotel Offers"),
    "hotels-lara": ("/group-hotel-offers-turkey/lara/", "Lara Group Hotel Offers"),
    "hotels-belek": ("/group-hotel-offers-turkey/belek/", "Belek Group Hotel Offers"),
    "calc": ("/event-cost-calculator/", "Event Cost Calculator"),
}

TARGETS = {
    "services": ["mice", "costs", "why", "offseason"],
    "services/event-production": ["mice", "cost", "costs", "events"],
    "services/ground-handling": ["mice", "transfers", "offseason"],
    "services/group-travel": ["hotels", "offseason", "transfers", "why"],
    "services/hotel-sourcing": ["hotels", "hotels-lara", "hotels-belek", "offseason"],
    "services/incentive-programs": ["incentive", "costs", "offseason", "os-bodrum"],
    "services/meetings-conferences": ["mice", "cost", "events", "offseason"],
    "services/transportation-logistics": ["transfers", "mice", "offseason"],
    "services/venue-sourcing": ["mice", "costs", "offseason", "why"],
    "mice-turkey": ["mice", "cost", "events", "wtm", "ibtm", "imex"],
    "incentive-travel-turkey": ["incentive", "costs", "offseason", "os-cappadocia", "os-bodrum"],
    "corporate-events-turkey": ["cost", "costs", "mice", "offseason"],
    "group-travel-turkey": ["hotels", "offseason", "transfers", "why"],
    "dmc-turkey": ["mice", "why", "costs", "incentive", "events"],
    "white-label-dmc-turkey": ["mice", "costs", "events", "itb"],
    "agency-partners": ["events", "wtm", "ibtm", "itb", "incentive"],
    "about": ["why", "mice", "events"],
    "destinations/antalya": ["cost-antalya", "os-antalya", "hotels-lara", "transfers"],
    "destinations/belek": ["cost-belek", "os-belek", "hotels-belek", "transfers"],
    "destinations/istanbul": ["cost-istanbul", "os-istanbul", "mice"],
    "destinations/bodrum": ["os-bodrum", "incentive", "costs"],
    "destinations/cappadocia": ["os-cappadocia", "incentive", "costs"],
    "antalya-event-production": ["cost-antalya", "mice", "calc"],
    "exhibition-stands-antalya": ["cost-antalya", "events", "mice"],
    "event-staff-antalya": ["cost-antalya", "mice", "calc"],
    "antalya-airport-transfers-group-transport": ["transfers", "hotels-lara", "hotels-belek", "os-antalya"],
    "last-minute-event-services-antalya": ["cost-antalya", "transfers", "mice"],
    "why-turkey": ["mice", "incentive", "offseason", "events"],
}


def block(rel):
    links = "".join('<a href="%s">%s</a>' % G[k] for k in TARGETS[rel] if G[k][0] != "/" + rel + "/")
    return ('    %s\n    <section class="page-section related-guides">\n      <h2>Planning Guides</h2>\n'
            '      <div class="cluster-links">%s</div>\n    </section>\n    %s\n') % (BEGIN, links, END)


def place(text, rel):
    text = re.sub(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", "", text, flags=re.S)
    start = text.index('<main id="main-content"')
    end = text.index("</main>", start)
    main = text[start:end]
    sections = [m.start() for m in re.finditer(r"[ \t]*<section\b", main)]
    at = None
    for i, pos in enumerate(sections):
        head = main[pos:pos + 600]
        if re.search(r"<h2[^>]*>[^<]*(FAQ|Frequently Asked Questions)[^<]*</h2>", head):
            close = main.index("</section>", pos) + len("</section>")
            at = start + close + (1 if main[close:close + 1] == "\n" else 0)
    if at is None:
        banners = [pos for pos in sections if 'class="cta-banner' in main[pos:pos + 300]]
        at = start + (banners[-1] if banners else len(main))
    return text[:at] + block(rel) + text[at:]


def main():
    changed = 0
    for rel in TARGETS:
        path = os.path.join(ROOT, rel, "index.html")
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        text = place(original, rel)
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("planning-guide links on %d pages (%d changed)" % (len(TARGETS), changed))


if __name__ == "__main__":
    main()
