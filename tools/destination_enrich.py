#!/usr/bin/env python3
"""Extra sections for the Cappadocia, Bodrum and incentive-travel pages.

NightWatch shows these ranked well before October ("dmc bodrum" best 1,
"dmc cappadocia" 3, "event production cappadocia" 4-6, "turkey incentive
travel" 4, "antalya incentive travel" 5). Each block below reuses figures the
site already publishes — the /event-costs/ ranges, the off-season windows in
tools/off_season_data.py, the destination facts tables and Selected Works —
and links to the page that carries them. No new claims.

Marker-delimited and idempotent.

Usage: python3 tools/destination_enrich.py
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import off_season_data as offseason  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEGIN, END = "<!-- destination-enrich:begin -->", "<!-- destination-enrich:end -->"


def window(slug):
    return next(d for d in offseason.DESTINATIONS if d["slug"] == slug)


def section(heading, body, sid):
    return ('    <section class="page-section" id="%s">\n      <h2>%s</h2>\n%s\n    </section>\n'
            % (sid, heading, body))


def cappadocia():
    w = window("cappadocia")
    return "".join([
        section("Budget for a Cappadocia Group Programme", (
            '      <p>Indicative all-in budget for a 3-night cave-hotel incentive: <strong>€800–1,200 per person</strong> '
            "for groups of 15–100, in April–June and September–October. See the "
            '<a href="/event-costs/">Turkey event cost guide</a> for other destinations, or '
            '<a href="/event-cost-calculator/">estimate your own programme</a>.</p>'), "budget"),
        section("Corporate Events in Cappadocia: What Fits", (
            "      <ul>"
            "<li><strong>Meetings:</strong> boardroom sessions for 10–30 people in cave-hotel meeting rooms. "
            "There is no convention centre for plenaries of 100+; for those, see "
            '<a href="/destinations/istanbul/">Istanbul</a> or <a href="/destinations/antalya/">Antalya</a>.</li>'
            "<li><strong>Group size:</strong> 15–100 guests is ideal; up to about 150 with rooms allocated across "
            "several cave hotels in Göreme, Ürgüp and Uçhisar.</li>"
            "<li><strong>Evenings and production:</strong> private cultural dinners and hosted evenings, with "
            'staging, sound and lighting scoped to the venue by our <a href="/services/event-production/">event '
            "production</a> team.</li>"
            "<li><strong>Movement:</strong> minibuses and small coaches; large 50+ seat coaches are impractical on "
            "the narrow valley roads of Old Göreme.</li>"
            "</ul>"), "corporate-events"),
        section("Winter Dates in Cappadocia", (
            "      <p>Off-peak window: <strong>%s</strong>. It suits %s, in %s. "
            "Balloon flights are less reliable in winter (see the table above), so plan an alternative "
            'morning. <a href="%s">Compare winter dates and event costs in Cappadocia</a>.</p>'
            % (w["window"], w["events"].lower(), w["scope"].lower(), w["page"])), "winter-dates"),
    ])


def bodrum():
    w = window("bodrum")
    return "".join([
        section("Corporate Events and Conferences in Bodrum", (
            "      <p>Bodrum works for executive meetings, corporate hospitality and incentive groups of 15–80 guests, "
            "and up to about 120 across several properties. The peninsula's largest resort, D-Maris Bay, has about "
            "350 rooms. For plenary conferences beyond that scale, "
            '<a href="/destinations/antalya/">Antalya</a> or <a href="/destinations/istanbul/">Istanbul</a> fit '
            "better, with Bodrum as a post-conference incentive.</p>"
            '      <p>Budget guide: <strong>€700–1,200 per person</strong> for a 4-night shoulder-season incentive '
            "(boutique hotel, gulet day, gala dinner). "
            '<a href="/event-cost-calculator/">Estimate your own programme</a>.</p>'), "corporate-events"),
        section("Off-Season Dates in Bodrum", (
            "      <p>Off-peak window: <strong>%s</strong>, for %s. %s. "
            '<a href="%s">Compare off-season dates and event costs in Bodrum</a>.</p>'
            % (w["window"], w["events"].lower(), w["scope"].rstrip("."), w["page"])), "off-season"),
    ])


def incentive():
    a, b = window("antalya"), window("belek")
    return section("Incentive Trips in Antalya &amp; Belek", (
        '      <p>Antalya and Belek are Türkiye\'s most used incentive bases: all-inclusive 5-star resorts make '
        "budgets predictable once hotel category, group size and programme level are set.</p>"
        '      <div class="table-scroll"><table class="data-table"><thead><tr><th>Programme</th><th>Nights</th>'
        "<th>Per person</th></tr></thead><tbody>"
        "<tr><td>Antalya incentive, 5-star all-inclusive resort</td><td>4</td><td>€500–750</td></tr>"
        "<tr><td>Antalya incentive with gala</td><td>4</td><td>€600–900</td></tr>"
        "<tr><td>Belek incentive, 5-star all-inclusive resort</td><td>4</td><td>€600–950</td></tr>"
        "<tr><td>Belek golf incentive</td><td>4</td><td>€750–1,100</td></tr>"
        "</tbody></table></div>\n"
        '      <p>Example: a 100-person incentive trip in Antalya is about €140,000–€190,000 for 4 nights. Ranges are '
        "shoulder season, groups of 50–150, flights excluded — see <a href=\"/event-costs/antalya/\">Antalya</a> and "
        '<a href="/event-costs/belek/">Belek</a> event costs.</p>'
        "      <p>Off-peak windows: Antalya %s, Belek %s — <a href=\"%s\">compare dates</a>. Recent dealer "
        'incentives we delivered: <a href="/selected-works/bellona-dealer-meeting/">Bellona Dealer Meeting</a> '
        '(Belek) and <a href="/selected-works/cw-enerji-dealer-sales-meeting/">CW Enerji Dealer &amp; Sales '
        "Meeting</a> (Antalya).</p>"
        % (a["window"], b["window"], offseason.HUB)), "antalya-belek")


TARGETS = {
    "destinations/cappadocia": (cappadocia, "<h2>Frequently Asked Questions</h2>"),
    "destinations/bodrum": (bodrum, "<h2>Frequently Asked Questions</h2>"),
    "incentive-travel-turkey": (incentive, "<h2>How Incentive Planning Works</h2>"),
}
H1 = {
    "destinations/cappadocia": ("Cappadocia Incentive Destination — What Works for Groups &amp; What Doesn’t",
                                "DMC Cappadocia — Incentives, Corporate Groups &amp; What Works for Groups"),
}


def main():
    changed = 0
    for rel, (build, anchor) in TARGETS.items():
        path = os.path.join(ROOT, rel, "index.html")
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        text = re.sub(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n", "", original, flags=re.S)
        if rel in H1:
            text = text.replace(H1[rel][0], H1[rel][1])
        idx = text.find(anchor)
        if idx == -1:
            raise SystemExit("anchor missing on %s" % rel)
        at = text.rfind("\n", 0, text.rfind("<section", 0, idx)) + 1
        text = text[:at] + "    " + BEGIN + "\n" + build() + "    " + END + "\n" + text[at:]
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("destination blocks on %d pages (%d changed)" % (len(TARGETS), changed))


if __name__ == "__main__":
    main()
