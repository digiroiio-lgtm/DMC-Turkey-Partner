#!/usr/bin/env python3
"""FAQ blocks for the event-cost and event pages (answer-engine readiness).

The internal SEO/GEO/AEO audit (Nov 2026) scored the event-cost pages 32/100
and the event pages 44/100 on answer readiness: no question headings, no
FAQPage schema, no dated content. This adds a visible FAQ plus matching
FAQPage JSON-LD to each page.

Every answer restates figures or facts already published on the same page —
cost ranges from its tables, or the dates, venue and organiser site of an
event — so no new claims are introduced. The FAQ is marker-delimited, the
schema carries a fixed @id, and re-running replaces both.

Usage: python3 tools/aeo_faqs.py
"""

import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"
TODAY = ("2026-11-10", "10 November 2026")
BEGIN, END = "<!-- aeo-faq:begin -->", "<!-- aeo-faq:end -->"
LD_BEGIN, LD_END = "<!-- aeo-faq-schema:begin -->", "<!-- aeo-faq-schema:end -->"

INCL = ("Ranges are all-in per person — hotel, venue, F&B, airport transfers, activities and DMC "
        "management — for groups of 50–150 in shoulder season, flights excluded.")

COSTS = {
    "event-costs": [
        ("How much does a corporate event in Turkey cost per person?",
         "Indicative all-in budgets for a 3–4 night programme run from about €400–600 per person for a "
         "resort conference in Antalya to €800–1,200 for a cave-hotel incentive in Cappadocia. " + INCL),
        ("Which Turkish destination is the most budget-friendly for a group event?",
         "Antalya: a 3-night resort conference at a 5-star all-inclusive resort is about €400–600 per "
         "person, and Istanbul city conferences start around €500–650. Cappadocia (€800–1,200) and Bodrum "
         "(€700–1,200) cost more per person."),
        ("How much more does peak season cost?",
         "Peak July–August typically adds 15–25% to the shoulder-season ranges on this page. April–June "
         "and September–November give better rates and availability for larger groups."),
        ("Are these figures quotations?",
         "No. They are indicative planning ranges to sense-check a budget. Every programme is priced "
         "individually once dates, hotel, group size and scope are confirmed."),
    ],
    "event-costs/antalya": [
        ("How much does a corporate event in Antalya cost per person?",
         "A 3-night corporate conference at a 5-star all-inclusive resort is about €400–600 per person "
         "(€300–450 at 4-star); a 4-night incentive trip is about €500–750, or €600–900 with a gala. " + INCL),
        ("What does a 100-person incentive trip in Antalya cost in total?",
         "About €140,000–€190,000 for 4 nights at an all-inclusive resort, in our example scenario on this page."),
        ("What does a 200-person conference in Antalya cost?",
         "About €220,000–€300,000 for 3 nights with full-day plenary sessions, in our example scenario on this page."),
        ("What is the cheapest time of year for an event in Antalya?",
         "Shoulder season, April–June and September–November. Peak July–August carries a 15–25% premium."),
    ],
    "event-costs/belek": [
        ("How much does a corporate retreat in Belek cost per person?",
         "A 4-night corporate retreat at a 5-star all-inclusive resort is about €500–750 per person; a "
         "4-night incentive trip is about €600–950. " + INCL),
        ("How much does a golf incentive in Belek cost?",
         "About €750–1,100 per person for 4 nights at a 5-star all-inclusive resort with golf, for groups of 30–80."),
        ("What does a 100-person corporate retreat in Belek cost in total?",
         "About €130,000–€175,000 for 4 nights, in our example scenario on this page."),
        ("Is venue hire included in Belek resort rates?",
         "Usually yes. Belek resorts price on all-inclusive packages, so venue hire and F&B are included in the hotel rate."),
    ],
    "event-costs/istanbul": [
        ("How much does a conference in Istanbul cost per person?",
         "A 3-night conference is about €350–500 per person at a 4-star city hotel and €500–650 at a 5-star "
         "Bosphorus hotel. " + INCL),
        ("What does a 100-person corporate event in Istanbul cost in total?",
         "About €150,000–€210,000 for 3 nights at a city hotel, in our example scenario on this page."),
        ("How much is an incentive trip in Istanbul?",
         "About €700–1,000 per person for 4 nights at a 5-star hotel including a Bosphorus cruise, for groups of 30–80."),
        ("Why are Istanbul budgets built line by line?",
         "Istanbul hotels are typically room-only or B&B, so meeting space, F&B and production are priced "
         "separately rather than bundled into an all-inclusive rate."),
    ],
}

EVENTS = ["events/wtm-london-2026", "events/ibtm-world-2026", "events/itb-berlin-2026", "events/imex-frankfurt"]


def read(rel):
    with open(os.path.join(ROOT, rel, "index.html"), encoding="utf-8") as handle:
        return handle.read()


def write(rel, text):
    with open(os.path.join(ROOT, rel, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(text)


def plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def event_faqs(text):
    """Questions answered from the event page's own facts."""
    name = plain(re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S).group(1))
    source = re.search(r'Official event source: <a[^>]*href="([^"]+)"', text)
    overview = re.search(r"<h2>Event Overview</h2>\s*<p>(.*?)</p>", text, re.S)
    facts = dict((plain(k), plain(v)) for k, v in re.findall(r"<dt>(.*?)</dt>\s*<dd>(.*?)</dd>", text, re.S))
    faqs = []
    if facts.get("Dates"):
        faqs.append(("When is %s?" % name, "%s runs %s." % (name, facts["Dates"].replace(" – ", " to "))))
    if facts.get("Venue"):
        faqs.append(("Where is %s held?" % name, "At %s, %s." % (facts["Venue"], facts.get("City / Country", ""))))
    if overview:
        first = re.split(r"(?<=[.!?])\s", plain(overview.group(1)))[0]
        faqs.append(("What is %s?" % name, first))
    if not facts:  # evergreen IMEX page: editions listed as cards
        editions = re.findall(
            r'<span class="event-card__date">([^<]+)</span>\s*<h3 class="event-card__name">([^<]+)</h3>', text)
        if editions:
            faqs.append(("When is IMEX Frankfurt?", " ".join(
                "%s: %s." % (n.strip(), d.strip().replace(" – ", " to ")) for d, n in editions)))
            faqs.append(("Where is IMEX Frankfurt held?", "At Messe Frankfurt in Frankfurt, Germany, every year."))
    if source:
        faqs.append(("Where can I find official %s information?" % name.split(" 20")[0],
                     "On the organiser's official website, %s. Dates and venue on this page were checked "
                     "against it." % source.group(1)))
    return faqs


def faq_html(faqs):
    items = "".join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (html.escape(q), html.escape(a))
                    for q, a in faqs)
    return ("    %s\n    <section class=\"page-section\" id=\"faq\">\n      <h2>Frequently Asked Questions</h2>\n"
            "      <div class=\"faq-list\">%s</div>\n"
            "      <p class=\"reviewed-note\">Last updated: <time datetime=\"%s\">%s</time></p>\n"
            "    </section>\n    %s\n") % (BEGIN, items, TODAY[0], TODAY[1], END)


def faq_schema(rel, faqs):
    data = {
        "@context": "https://schema.org", "@type": "FAQPage", "@id": "%s/%s/#faq" % (SITE, rel),
        "dateModified": TODAY[0],
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }
    return '  %s\n  <script type="application/ld+json">%s</script>\n  %s\n' % (
        LD_BEGIN, json.dumps(data, ensure_ascii=False), LD_END)


# Insert the FAQ before the first of these headings.
BEFORE = ["Related Events", "Source &amp; Verification", "Relevant Selected Works", "Planning Something Similar?",
          "Build a Programme Around My Budget"]


def apply(rel, faqs):
    text = read(rel)
    for b, e in ((BEGIN, END), (LD_BEGIN, LD_END)):
        text = re.sub(r"[ \t]*" + re.escape(b) + r".*?" + re.escape(e) + r"\n", "", text, flags=re.S)
    for heading in BEFORE:
        m = re.search(r'[ \t]*<section class="page-section[^"]*">\s*<h2>%s</h2>' % re.escape(heading), text)
        if m:
            break
    else:
        raise SystemExit("No insertion point on %s" % rel)
    text = text[:m.start()] + faq_html(faqs) + text[m.start():]
    text = text.replace("</head>", faq_schema(rel, faqs) + "</head>", 1)
    write(rel, text)


def main():
    for rel, faqs in COSTS.items():
        apply(rel, faqs)
    for rel in EVENTS:
        faqs = event_faqs(read(rel))
        if len(faqs) < 3:
            raise SystemExit("Too few facts for an FAQ on %s" % rel)
        apply(rel, faqs)
    print("FAQ blocks on %d pages" % (len(COSTS) + len(EVENTS)))


if __name__ == "__main__":
    main()
