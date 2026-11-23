#!/usr/bin/env python3
"""After COP31: past tense and no COP31 service claims on non-COP31 pages.

Companion to tools/cop31_post_event.py (which moved the five service pages).
The business decided not to claim it delivered COP31 work, so forward-looking
"we provide COP31 services" copy on evergreen pages becomes general Antalya
event-services copy, and dates become past tense. Factual references (the
EXPO Center hosted COP31) stay.

Each (old, new) pair must be found once on its page; re-running is a no-op
because the old text is gone.

Usage: python3 tools/cop31_sitewide_after.py
"""

import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SERVICES_P = (
    '<a href="/antalya-event-production/">event production and AV</a>, '
    '<a href="/exhibition-stands-antalya/">exhibition stands and pavilions</a>, '
    '<a href="/event-staff-antalya/">event staff and interpreters</a>, '
    '<a href="/antalya-airport-transfers-group-transport/">airport transfers and group transport</a> and '
    '<a href="/last-minute-event-services-antalya/">last-minute support</a>'
)

EDITS = {
    "destinations/antalya": [
        ("<h2>COP31 Antalya 2026 — Local Event Services</h2>", "<h2>Conference and Exhibition Services in Antalya</h2>"),
        (re.compile(r"<p>COP31 \(the 31st UN Climate Change Conference\) takes place 9–20 November 2026 at Antalya EXPO Center\. "
                    r"DMC Turkey Partner is providing local event services for organisations exhibiting, presenting, and operating at COP31\.</p>"),
         "<p>Antalya hosts international conferences, congresses and exhibitions at the Antalya EXPO Center and in the "
         "resort conference hotels of Lara and Belek; the EXPO Center was the venue of COP31 in November 2026.</p>"),
        (re.compile(r"<p>Available COP31 services include: .*?</p>", re.S),
         "<p>Our local services for conferences and exhibitions in Antalya: " + SERVICES_P + ".</p>"),
        ('<p><a class="btn btn--primary" href="/cop31-antalya/">View all COP31 services →</a></p>',
         '<p><a class="btn btn--primary" href="/request-proposal/?src=destinations-antalya">Request an Antalya Proposal</a> '
         '<a href="/cop31-antalya/">COP31 2026 archive</a></p>'),
        ("COP31 dates</td><td>9–20 November 2026, Antalya EXPO Center</td>",
         "COP31 (past host)</td><td>9–20 November 2026, Antalya EXPO Center</td>"),
        ("and is the host venue for COP31 in November 2026.", "and hosted COP31 in November 2026."),
        ("and is the COP31 2026 host venue.", "and hosted COP31 in November 2026."),
        ("and full COP31 local support services at Antalya EXPO Center.", "and conference and exhibition support at Antalya EXPO Center."),
        ("and full COP31 local support at Antalya EXPO Center.", "and conference and exhibition support at Antalya EXPO Center."),
        (re.compile(r',?\{"@type":"Question","name":"What is COP31 and when does it take place in Antalya\?".*?\}\}'), ""),
    ],
    "destinations": [
        ("For November 2026 (COP31 Antalya), mild weather remains suitable for large-scale operations.",
         "November remains mild in Antalya and suitable for large-scale operations."),
        ("For November 2026 (COP31), Antalya offers mild weather suitable for large-scale operations.",
         "In November, Antalya offers mild weather suitable for large-scale operations."),
    ],
    "destinations/belek": [
        ("For the Antalya city region including EXPO Center and COP31, see", "For the Antalya city region including the EXPO Center, see"),
    ],
    "events": [
        (re.compile(r'and, for November 2026,\s*the <a href="/cop31-antalya/">COP31 Antalya local services guide</a>'),
         'and the <a href="/antalya-event-production/">Antalya event services</a> pages'),
    ],
    "events/imex-frankfurt": [
        ("COP31 Antalya local services briefing (applicable until November 2026)", "Antalya conference and exhibition services briefing"),
    ],
    "insights/incentive-travel-turkey-destination-guide": [
        ("COP31 2026 profile raising", "COP31 host city in 2026"),
    ],
    "dmc-turkey": [
        ("Planning Operations in Antalya Around COP31?</a>", "Planning Operations in Antalya?</a>"),
        ("Planning Operations in Antalya Around COP31?</h2>", "Planning Operations in Antalya?</h2>"),
        ('<p><a class="btn btn--ghost" href="/cop31-antalya/">Explore COP31 Antalya Services</a></p>',
         '<p><a class="btn btn--ghost" href="/destinations/antalya/">Explore Antalya DMC Services</a></p>'),
    ],
    "corporate-events-turkey": [
        ('<li><a href="#corporate-events-around-cop31-in-antalya">Corporate Events Around COP31 in Antalya</a></li>',
         '<li><a href="#corporate-events-around-cop31-in-antalya">Corporate Events in Antalya</a></li>'),
        ('<h2 id="corporate-events-around-cop31-in-antalya">Corporate Events Around COP31 in Antalya</h2>',
         '<h2 id="corporate-events-around-cop31-in-antalya">Corporate Events in Antalya</h2>'),
        (re.compile(r"<p>If your team is travelling to Antalya for COP31 \(9–20 November 2026\).*?full list of local services\.</p>", re.S),
         "<p>For conferences, exhibitions and corporate events in Antalya we provide " + SERVICES_P +
         ', alongside <a href="/destinations/antalya/">hotel and venue sourcing</a>.</p>'),
        ('<li><a href="#how-can-a-corporate-event-connect-with-cop31-activities">How can a corporate event connect with COP31 activities?</a></li>', ""),
        (re.compile(r'[ \t]*<section class="page-section qa-block">(?:(?!</section>).)*?id="how-can-a-corporate-event-connect-with-cop31-activities".*?</section>\n', re.S), ""),
    ],
    "request-proposal": [
        (re.compile(r'\s*<option[^>]*>COP31 Antalya</option>'), ""),
    ],
}


def main():
    changed = 0
    for rel, edits in EDITS.items():
        path = os.path.join(ROOT, rel, "index.html")
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        text = original
        for old, new in edits:
            if isinstance(old, re.Pattern):
                text = old.sub(new, text)
            elif old in text:
                text = text.replace(old, new)
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("post-COP31 copy updated on %d pages" % changed)


if __name__ == "__main__":
    main()
