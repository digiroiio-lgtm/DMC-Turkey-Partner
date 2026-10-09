#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the off-season hub, the Belek, Antalya, Istanbul and Bodrum off-season pages and the pop-up data.

Usage: python3 tools/off_season_build.py

Writes:
  off-season-events-turkey/index.html
  off-season-events-turkey/belek/index.html
  off-season-events-turkey/antalya/index.html
  off-season-events-turkey/istanbul/index.html
  off-season-events-turkey/bodrum/index.html
and rewrites the block between `/* offseason-data:begin */` and
`/* offseason-data:end */` in assets/js/main.js, so the pop-up and the pages
share one source (tools/off_season_data.py). Idempotent.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import SITE, esc  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT, table  # noqa: E402
import off_season_data as data  # noqa: E402
import site_seo  # noqa: E402

HUB_URL = SITE + data.HUB
BELEK_PATH = data.HUB + "belek/"
BELEK_URL = SITE + BELEK_PATH
ANTALYA_PATH = data.HUB + "antalya/"
ANTALYA_URL = SITE + ANTALYA_PATH
ISTANBUL_PATH = data.HUB + "istanbul/"
ISTANBUL_URL = SITE + ISTANBUL_PATH
BODRUM_PATH = data.HUB + "bodrum/"
BODRUM_URL = SITE + BODRUM_PATH
BODRUM_PEAK = "May – June, September and July – August"
PEAK = "March – June and September – November"

# Published Belek reference ranges, copied verbatim from /event-costs/belek/
# (reviewed September 2026). Never recomputed here.
BELEK_REFERENCE = [
    ("4-night corporate retreat (5-star AI resort)", "50–150", "4", "€500–750"),
    ("4-night incentive trip (5-star AI resort)", "50–150", "4", "€600–950"),
    ("4-night golf incentive (5-star AI resort + golf)", "30–80", "4", "€750–1,100"),
    ("3-night conference + team-building (5-star)", "100–300", "3", "€450–650"),
    ("5-night premium incentive (ultra-luxury AI resort)", "30–80", "5", "€1,000–1,500"),
]

# Published Antalya reference ranges, copied verbatim from /event-costs/antalya/
# (reviewed September 2026). Never recomputed here.
ANTALYA_REFERENCE = [
    ("3-night corporate conference (5-star AI resort)", "50–150", "3", "€400–600"),
    ("3-night corporate conference (4-star AI resort)", "50–150", "3", "€300–450"),
    ("4-night incentive trip (5-star AI resort)", "50–150", "4", "€500–750"),
    ("4-night incentive trip with gala (5-star AI resort)", "50–150", "4", "€600–900"),
    ("3-night dealer/partner meeting (5-star AI resort)", "100–300", "3", "€350–550"),
    ("5-night corporate event with programme (5-star AI resort)", "50–100", "5", "€700–1,100"),
]

# Published Istanbul reference ranges, copied verbatim from /event-costs/istanbul/
# (reviewed September 2026). Never recomputed here.
ISTANBUL_REFERENCE = [
    ("3-night conference (4-star city hotel)", "50–150", "3", "€350–500"),
    ("3-night conference (5-star Bosphorus hotel)", "50–150", "3", "€500–650"),
    ("3-night corporate event + hosted dinner (5-star)", "50–150", "3", "€550–750"),
    ("4-night incentive with Bosphorus cruise (5-star)", "30–80", "4", "€700–1,000"),
    ("2-night executive meeting (5-star)", "20–60", "2", "€400–600"),
]

# Published Bodrum figures, copied verbatim: the first row from the /event-costs/
# hub table, the other two from /destinations/bodrum/ (reviewed September 2026).
BODRUM_REFERENCE = [
    ("Boutique hotel incentive: boutique hotel, gulet day, gala dinner (May – June, October)", "15–80 (typical)", "4", "€700–1,200"),
    ("Executive retreat: private villa, superyacht charter, VIP programme", "Small executive groups", "3–4", "€1,500–3,000"),
]

EXPECT = (
    '<ul class="cta-expect" aria-label="What happens after you send a brief">'
    "<li>Reply within 24 hours</li>"
    "<li>Side-by-side proposal in 3–5 business days</li>"
    "<li>Named coordinator once you confirm</li></ul>"
)


# --- wording that depends on the saving claim ---------------------------------

def saving_sentence(peak=None):
    peak = peak or PEAK
    pct = data.saving_percent()
    if pct:
        return ("In like-for-like quotes for the same scope, off-peak dates have come in up to "
                "%d%% below peak-season rates (%s). Final pricing depends on dates, group size and availability." % (pct, peak))
    return ("Off-peak dates can lower hotel, resort and venue rates and improve availability. We quantify "
            "the difference in your proposal, line by line, for your own dates and group.")


# --- FAQ (plain text so the visible answer and the schema are identical) ------

def faq_hub():
    return [
        ("What are off-peak dates for events in Turkey?",
         "Off-peak dates are the weeks when demand from conferences and incentive groups is lowest, so hotels have "
         "conference capacity to spare. The window differs by destination: for example December – February in Belek "
         "and Antalya, October – April in Bodrum."),
        ("Can an off-season event cost less than one in peak season?",
         saving_sentence()),
        ("Are hotels and venues open in the off-season?",
         "Not all of them. Resorts and hotels close or reduce facilities at different times, so we confirm which "
         "properties, conference rooms and services are open for your exact dates before we quote."),
        ("Can we compare dates before committing?",
         "Yes. Choose “Compare off-peak and peak-season dates side by side” in the brief and we price the "
         "same programme in both windows. A proposal is not a booking."),
    ]


def faq_belek():
    return [
        ("When is the off-peak window for events in Belek?",
         "December – February is the core off-peak window. New Year week and public-holiday weeks can be priced "
         "differently, and March – June and September – November are the busiest MICE months."),
        ("Are Belek resorts open for meetings in winter?",
         "Some are, with their conference wings, but not every resort keeps every facility open from December to "
         "February. We confirm which resorts and rooms are available for your dates before quoting."),
        ("Can a golf incentive run in winter?",
         "Course availability and playing conditions vary in winter, so golf is confirmed per course and date and "
         "an indoor alternative is planned alongside it."),
        ("How do you calculate the difference between off-peak and peak dates?",
         "We price the same programme twice, in the off-peak window and in a peak-season window: same hotel "
         "category, scope, group size and nights. The difference is shown line by line in your proposal."),
    ]


def faq_antalya():
    return [
        ("When is the off-peak window for events in Antalya?",
         "December – February is the core off-peak window. New Year week and public-holiday weeks can be priced "
         "differently, and March – June and September – November are the busiest MICE months."),
        ("How is this different from the Belek off-season page?",
         "This page covers Antalya city and coast: city hotels, venues such as the Antalya EXPO Center and "
         "programmes that combine city and resort. Resort-based meetings and golf incentives in Belek are covered "
         "on the Belek page."),
        ("Are Antalya hotels and venues open in winter?",
         "Many city hotels operate all year, but resorts and venues differ in which facilities they keep open from "
         "December to February. We confirm availability for your exact dates before we quote."),
        ("How do you calculate the difference between off-peak and peak dates?",
         "We price the same programme twice, in the off-peak window and in a peak-season window: same hotel "
         "category, scope, group size and nights. The difference is shown line by line in your proposal."),
    ]


def faq_istanbul():
    return [
        ("When is the off-peak window for events in Istanbul?",
         "January – February is the core off-peak window for corporate and conference groups. July – August can "
         "also be quieter for business events, but it is peak leisure season for city hotels, so we compare it "
         "before assuming a saving. April – June and September – November are the busiest MICE months."),
        ("Is Istanbul priced differently from Antalya or Belek?",
         "Yes. Istanbul hotels are typically room-only or bed-and-breakfast, and meeting space, food and beverage "
         "and production are itemised, so the comparison between dates is shown line by line rather than as one "
         "all-inclusive rate."),
        ("Are hotels and venues open and available in winter?",
         "City hotels generally operate all year, but meeting rooms, venues and events calendars differ by date. "
         "We confirm availability for your exact dates before we quote."),
        ("How do you calculate the difference between off-peak and peak dates?",
         "We price the same programme twice, in the off-peak window and in a peak-season window: same hotel "
         "category, scope, group size and nights. The difference is shown line by line in your proposal."),
    ]


def faq_bodrum():
    return [
        ("When is the off-peak window for events in Bodrum?",
         "October – April is the planning window. October and April are the strongest months for small groups, "
         "because most boutique hotels are open and the weather is mild. From November to March many boutique "
         "hotels and gulet operators are closed, so the options are narrower."),
        ("Are Bodrum hotels and gulets open in winter?",
         "Many boutique hotels and gulet operators close from November to March, while city-centre properties "
         "stay open. We confirm exactly which properties and services are operating for your dates before we quote."),
        ("Can we still plan a gulet or yacht programme outside summer?",
         "Gulet and yacht programmes depend on operator availability and sea conditions, and they are best from "
         "May to October. Outside those months we plan hotel-based and indoor programmes instead."),
        ("How do you calculate the difference between off-peak and peak dates?",
         "We price the same programme twice, in the off-peak window and in a peak-season window: same hotel "
         "category, scope, group size and nights. The difference is shown line by line in your proposal."),
    ]


def faq_html(items):
    body = "".join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (esc(q), esc(a)) for q, a in items)
    return ('    <section class="page-section">\n      <h2>Frequently Asked Questions</h2>\n'
            '      <div class="faq-list">%s</div>\n    </section>' % body)


# --- form ---------------------------------------------------------------------

DESTINATION_OPTIONS = ["Istanbul", "Antalya", "Belek", "Bodrum", "Cappadocia", "Multiple Destinations", "Not Decided Yet"]


def form_html(fixed_destination=None):
    if fixed_destination:
        dest = '<input type="hidden" name="destination" value="%s">' % fixed_destination
    else:
        options = "".join("<option>%s</option>" % o for o in DESTINATION_OPTIONS)
        dest = ('<div class="form-field"><label for="os-destination">Destination</label>'
                '<select id="os-destination" name="destination" required><option value="">Select a destination</option>%s</select></div>' % options)
    return '''    <section class="page-section offseason-compare" id="compare">
      <h2>Compare Dates &amp; Event Costs</h2>
      <p class="page-section__lede">Tell us the destination, group size and how flexible your dates are. We price the off-peak window and a peak-season window for the same programme.</p>
      <form name="off-season-compare" method="POST" action="/api/request-proposal" data-proposal-form>
        <p class="sr-only"><label>Company website <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
        <input type="hidden" name="source_page"><input type="hidden" name="landing_page"><input type="hidden" name="submission_page"><input type="hidden" name="timestamp">
        <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_content"><input type="hidden" name="utm_term">
        <input type="hidden" name="lead_source"><input type="hidden" name="campaign"><input type="hidden" name="service_interest"><input type="hidden" name="page_type">
        %s
        <div class="form-grid">
          <div class="form-field"><label for="os-name">Your Name</label><input type="text" id="os-name" name="name" autocomplete="name" required></div>
          <div class="form-field"><label for="os-company">Company</label><input type="text" id="os-company" name="company" autocomplete="organization" required></div>
          <div class="form-field"><label for="os-email">Work Email</label><input type="email" id="os-email" name="email" autocomplete="email" inputmode="email" required></div>
          <div class="form-field"><label for="os-group">Approx. Group Size</label>
            <select id="os-group" name="group_size" required><option value="">Select an approximate size</option>
              <option>Under 20</option><option>20–50</option><option>51–100</option><option>101–250</option><option>251–500</option><option>500+</option><option>Not Confirmed Yet</option></select></div>
          <div class="form-field"><label for="os-type">Event Type</label>
            <select id="os-type" name="project_type"><option value="">Select an event type</option>
              <option>Meeting / Conference</option><option>Incentive Travel</option><option>Corporate Event</option><option>Group Travel</option><option>Other</option></select></div>
          <fieldset class="form-field"><legend>Preferred Dates</legend>
            <div class="date-range"><label for="os-date-start" class="sr-only">Start date</label><input type="date" id="os-date-start" name="date_start">
              <label for="os-date-end" class="sr-only">End date</label><input type="date" id="os-date-end" name="date_end"></div>
            <label class="form-check"><input type="checkbox" id="os-dates-unconfirmed" name="dates_unconfirmed" value="Yes"> Dates Not Confirmed</label></fieldset>
          <div class="form-field form-field--full"><label for="os-flex">How flexible are your dates?</label>
            <select id="os-flex" name="date_flexibility" required>
              <option selected>Compare off-peak and peak-season dates side by side</option>
              <option>Off-peak window only</option>
              <option>Open to any dates</option></select></div>
          <div class="form-field form-field--full"><label for="os-brief">Anything else we should know? <span class="field-optional">(optional)</span></label>
            <textarea id="os-brief" name="brief" placeholder="Programme type, hotel category, must-have dates..."></textarea></div>
          <p class="form-note form-field--full">We use your contact details to respond to this enquiry, as explained in our <a href="/privacy-policy/">Privacy Policy</a>. A proposal is not a booking. Please do not include passport, payment card or sensitive personal details.</p>
          <p class="form-error" data-proposal-error role="alert" hidden></p>
          <div class="form-actions"><button type="submit" class="btn btn--primary">Compare Dates &amp; Event Costs</button></div>
        </div>
      </form>
      <section class="proposal-success" data-proposal-success hidden aria-live="polite">
        <h2>Thank you — we’ve received your brief.</h2>
        <p>We will reply within 24 hours and send your side-by-side proposal within 3–5 business days.</p>
      </section>
      %s
    </section>''' % (dest, EXPECT)


# --- shared page pieces --------------------------------------------------------

def head_html(title, description, url, lead_source, service_interest, schema_blocks):
    return "\n".join([
        "<!DOCTYPE html>", '<html lang="en">', "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '  <link rel="icon" href="/favicon.ico" sizes="any">',
        '  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
        '  <link rel="manifest" href="/site.webmanifest">',
        "  <title>%s</title>" % title,
        '  <meta name="description" content="%s">' % esc(description),
        '  <link rel="canonical" href="%s">' % url,
        '  <meta name="robots" content="index, follow">',
        '  <meta property="og:type" content="website">',
        '  <meta property="og:title" content="%s">' % title,
        '  <meta property="og:description" content="%s">' % esc(description),
        '  <meta property="og:url" content="%s">' % url,
        '  <meta property="og:site_name" content="DMC Turkey Partner">',
        '  <meta property="og:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="dmc:lead-source" content="%s">' % lead_source,
        '  <meta name="dmc:service-interest" content="%s">' % service_interest,
        '  <meta name="dmc:page-type" content="off-season">',
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        '  <link rel="stylesheet" href="/assets/css/forms.css">',
        schema_blocks, "</head>",
    ])


def schema(name, url, description, crumbs, faqs):
    web = {"@context": "https://schema.org", "@type": "WebPage", "name": name, "url": url,
           "description": description, "inLanguage": "en", "dateModified": data.UPDATED_ISO,
           "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                              for i, (n, p) in enumerate(crumbs)]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                         for q, a in faqs]}
    return "\n".join('  <script type="application/ld+json">\n  %s\n  </script>'
                     % json.dumps(d, ensure_ascii=False, separators=(",", ":")) for d in (web, bc, fq))


def season_note():
    return ('<p class="reviewed-note">Current season: %s · Last updated: <time datetime="%s">%s</time></p>'
            % (data.SEASON_LABEL, data.UPDATED_ISO, data.UPDATED_LABEL))


def hero_buttons(extra=""):
    return ('<div class="hero-actions"><a class="btn btn--primary" href="#compare">Compare Dates &amp; Event Costs</a>%s</div>' % extra)


def crumbs_html(items):
    lis = "".join('<li><a href="%s">%s</a></li>' % (p, n) for n, p in items[:-1])
    lis += '<li aria-current="page">%s</li>' % items[-1][0]
    return '      <nav class="breadcrumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>' % lis


def assemble(head, body):
    return head + "\n" + HEADER + '<main id="main-content">\n' + body + "\n  </main>" + FOOTER


# --- hub page -------------------------------------------------------------------

def render_hub():
    title = "Off-Season Events in Turkey | Off-Peak Dates &amp; Event Costs"
    description = ("Plan group events in Turkey's off-peak dates. Compare planning windows by destination and request "
                   "a side-by-side proposal for off-peak and peak-season dates.")
    faqs = faq_hub()
    crumbs = [("Home", "/"), ("Off-Season Events", data.HUB)]
    rows = []
    for d in data.DESTINATIONS:
        link = ('<a href="%s">%s off-season guide</a>' % (d["page"], d["name"]) if d["page"]
                else '<a href="%s?destination=%s#compare">Dates &amp; options on request</a>' % (data.HUB, d["name"]))
        rows.append([d["name"], d["window"], d["events"], d["scope"], link])
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Off-Season Events in Turkey: Off-Peak Dates &amp; Planning Windows</h1>",
        "      " + season_note(),
        '      <p class="page-section__lede">Off-peak dates are the weeks when Turkey’s resort and city hotels have '
        "conference capacity to spare. For agencies and corporate planners with flexible dates, that can mean lower "
        "rates and better availability for the same programme. This page compares the planning windows by destination "
        "and shows how we price your dates side by side with peak-season options.</p>",
        "      " + hero_buttons('<a class="btn btn--ghost" href="%s">Off-season in Belek</a>' % BELEK_PATH),
        "      " + EXPECT,
        "    </section>",
        '    <section class="page-section">',
        "      <h2>How the Comparison Works</h2>",
        '      <ol class="steps-list">'
        "<li><h3>Send Your Brief</h3><p>Destination, group size and how flexible your dates are.</p></li>"
        "<li><h3>Reply Within 24 Hours</h3><p>We confirm what is open in the window and flag exceptions.</p></li>"
        "<li><h3>Side-by-Side Proposal</h3><p>Within 3–5 business days: off-peak and peak-season dates for the same programme, itemised.</p></li>"
        "<li><h3>Coordinator &amp; Delivery</h3><p>Once you confirm, a named coordinator runs the programme.</p></li></ol>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Off-Peak Planning Windows by Destination</h2>",
        "      " + table("Off-peak windows and scope by destination (%s)" % data.SEASON_LABEL,
                         ["Destination", "Off-peak window", "Suited programmes", "Scope", "Guide"], rows),
        '      <p class="price-note">Windows are planning guides, not guarantees. Individual hotels open and close on their own calendars, and holiday weeks can be priced differently.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Antalya and Belek: What Each Covers</h2>",
        '      <div class="card-grid">'
        '<article class="card"><h3><a href="%s">Belek</a></h3><p>Resort-based programmes: conference wings inside all-inclusive resorts, packaged rates, golf incentives, dealer meetings and retreats.</p></article>'
        '<article class="card"><h3><a href="%s">Antalya</a></h3><p>City and coast: city hotels, venues such as the Antalya EXPO Center, airport and city transfers, and programmes that combine city and resort. See the <a href="%s">Antalya off-season guide</a>.</p></article></div>' % (BELEK_PATH, ANTALYA_PATH, ANTALYA_PATH),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>How We Compare Costs</h2>",
        '      <p>We do not publish discounted prices. Indicative per-person ranges for each destination are on the <a href="/event-costs/">event costs pages</a>. For your brief we price the off-peak window and a peak-season window (%s) for the same programme, with the same hotel category, scope, group size and nights, and show the difference line by line.</p>' % PEAK,
        '      <div class="offseason-callout"><p>%s</p></div>' % esc(saving_sentence()),
        "    </section>",
        faq_html(faqs),
        form_html(),
    ])
    return assemble(head_html(title, description, HUB_URL, "Off-Season Events", "Off-Season Events Hub",
                              schema("Off-Season Events in Turkey", HUB_URL, description,
                                     [(n, p) for n, p in crumbs], faqs)), body)


# --- Belek page -----------------------------------------------------------------

def render_belek():
    title = "Off-Season Events in Belek | Off-Peak Resort Dates &amp; Costs"
    description = ("Off-peak dates for resort meetings, dealer meetings and golf incentives in Belek. See the planning "
                   "window, reference costs and operating conditions, and compare dates side by side.")
    faqs = faq_belek()
    crumbs = [("Home", "/"), ("Off-Season Events", data.HUB), ("Belek", BELEK_PATH)]
    ref_rows = [list(r) for r in BELEK_REFERENCE]
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Off-Season Events in Belek: Off-Peak Resort Dates &amp; Planning Windows</h1>",
        "      " + season_note(),
        '      <p class="page-section__lede">Belek is Turkey’s resort-based meetings district: conference wings inside '
        "all-inclusive resorts, 30–45 minutes from Antalya Airport. From December to February the resorts are at their "
        "quietest, which is when agencies with flexible dates can plan dealer meetings, retreats and golf incentives "
        "with better availability and lower rates than in the spring and autumn peaks.</p>",
        "      " + hero_buttons(),
        "      " + EXPECT,
        '      <div class="offseason-callout"><p><strong>Scope of this page:</strong> resort-based programmes in Belek. '
        'For city hotels, city venues and the EXPO Center see the <a href="%s">Antalya off-season page</a>; for the '
        'all-year overview of Belek see the <a href="/destinations/belek/">Belek destination guide</a>.</p></div>' % ANTALYA_PATH,
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Suitable Date Windows</h2>",
        "      " + table("Belek planning windows (%s)" % data.SEASON_LABEL, ["Window", "Role", "What to expect"], [
            ["December – February", "Core off-peak window", "Best availability and the most room to negotiate. Which resorts and conference wings are open is confirmed per brief."],
            ["New Year week and public holidays", "Exceptions", "Demand and rates can differ sharply; these weeks are usually priced separately."],
            [PEAK, "Peak MICE months", "The comparison baseline: the busiest conference and incentive months."],
            ["July – August", "Summer leisure peak", "Family and leisure demand; published rates carry a 15–25% premium."],
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Events That Fit the Off-Peak Window</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Dealer &amp; sales meetings</h3><p>Regional dealer conferences and sales kick-offs that need a ballroom, breakouts and a gala dinner under one roof.</p></article>"
        "<article class=\"card\"><h3>Training &amp; conferences</h3><p>Multi-day programmes of 100–300 delegates with team-building.</p></article>"
        "<article class=\"card\"><h3>Board &amp; leadership retreats</h3><p>Smaller executive groups that value quiet resorts and flexible meeting rooms.</p></article>"
        "<article class=\"card\"><h3>Golf incentives</h3><p>Groups of 30–80, subject to course conditions; an indoor alternative is planned alongside.</p></article></div>",
        '      <p class="section-more">Typical off-peak groups are 30–300 guests. Larger groups depend on which conference wings are open for your dates.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Cost Comparison</h2>",
        "      <p>Published reference ranges for Belek, shown for the spring and autumn programme season (April – June and September – November). They are the starting point for the comparison, not an off-peak price.</p>",
        "      " + table("Belek reference ranges, per person (reviewed September 2026)",
                         ["Programme type", "Group size (pax)", "Nights", "Budget range (€/pax)"], ref_rows),
        '      <p class="price-note">All-in per-person totals: hotel accommodation, venue hire or ballroom use, full-board F&amp;B (or equivalent), airport transfers, programme activities and DMC management fee. Flights excluded. Peak July – August carries a 15–25% premium. Source: <a href="/event-costs/belek/">Belek event costs</a>.</p>',
        '      <div class="offseason-callout"><h3>How the comparison works</h3>'
        "<p>For your dates we price the off-peak window and a peak-season window side by side for the same programme: same hotel category, scope, group size and nights. %s</p>"
        '<p><a class="btn btn--primary" href="#compare">Compare Dates &amp; Event Costs</a></p></div>' % esc(saving_sentence()),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Operating Conditions</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Hotel availability</h3><p>Not every resort keeps its conference wing and all facilities open from December to February. We confirm which properties and rooms are available for your dates before we quote.</p></article>"
        '<article class="card"><h3>Getting there</h3><p>Belek resorts are 30–45 minutes from Antalya Airport (30–40 km). Indicative vehicle prices are on the <a href="/antalya-transfer-prices/">Antalya transfer prices</a> page.</p></article>'
        "<article class=\"card\"><h3>Weather and indoor plan</h3><p>Days are cooler and shorter, so programmes are planned indoor-first (ballroom, spa, indoor team-building) with outdoor sessions as weather-dependent additions.</p></article></div>",
        "    </section>",
        faq_html(faqs),
        form_html(fixed_destination="Belek"),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="%s">Off-season events in Turkey</a><a href="/destinations/belek/">Belek destination guide</a>'
        '<a href="/event-costs/belek/">Belek event costs</a>'
        '<a href="/selected-works/vakifbank-management-summit-titanic-belek/">VakıfBank summit, Titanic Belek</a>'
        '<a href="%s">Antalya off-season guide</a><a href="/destinations/antalya/">Antalya destination guide</a></p></section>' % (data.HUB, ANTALYA_PATH),
    ])
    return assemble(head_html(title, description, BELEK_URL, "Off-Season Events", "Belek Off-Season",
                              schema("Off-Season Events in Belek", BELEK_URL, description,
                                     [(n, p) for n, p in crumbs], faqs)), body)


# --- Antalya page ---------------------------------------------------------------

def render_antalya():
    title = "Off-Season Events in Antalya | Off-Peak Dates &amp; Costs"
    description = ("Off-peak dates for conferences, corporate events and city-and-coast incentives in Antalya. See the "
                   "planning window, reference costs and operating conditions, and compare dates side by side.")
    faqs = faq_antalya()
    crumbs = [("Home", "/"), ("Off-Season Events", data.HUB), ("Antalya", ANTALYA_PATH)]
    ref_rows = [list(r) for r in ANTALYA_REFERENCE]
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Off-Season Events in Antalya: Off-Peak Dates &amp; Planning Windows</h1>",
        "      " + season_note(),
        '      <p class="page-section__lede">Antalya combines a city with a coastline: city hotels, the Antalya EXPO '
        "Center and resort hotels all within reach of Antalya Airport. From December to February demand from "
        "conference and incentive groups is lower, which gives agencies with flexible dates more availability "
        "and more room to negotiate for conferences, corporate events and city-and-coast programmes.</p>",
        "      " + hero_buttons('<a class="btn btn--ghost" href="%s">Off-season in Belek</a>' % BELEK_PATH),
        "      " + EXPECT,
        '      <div class="offseason-callout"><p><strong>Scope of this page:</strong> Antalya city and coast. '
        'Resort-based meetings and golf incentives in the Belek resort district are covered on the '
        '<a href="%s">Belek off-season page</a>; for an all-year overview see the '
        '<a href="/destinations/antalya/">Antalya destination guide</a>.</p></div>' % BELEK_PATH,
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Suitable Date Windows</h2>",
        "      " + table("Antalya planning windows (%s)" % data.SEASON_LABEL, ["Window", "Role", "What to expect"], [
            ["December – February", "Core off-peak window", "Best availability and the most room to negotiate. Which hotels and venues are open is confirmed per brief."],
            ["New Year week and public holidays", "Exceptions", "Demand and rates can differ sharply; these weeks are usually priced separately."],
            [PEAK, "Peak MICE months", "The comparison baseline: the busiest conference and incentive months."],
            ["July – August", "Summer leisure peak", "Published rates carry a 15–25% premium."],
        ]),
        '      <p class="section-more">Demand in Antalya is higher around COP31 (9–20 November 2026, Antalya EXPO Center). See the <a href="/cop31-antalya/">COP31 Antalya guide</a> before planning dates near it.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Events That Fit the Off-Peak Window</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Conferences &amp; corporate events</h3><p>City-hotel and resort conferences where meeting space, AV and a gala dinner are the core of the programme.</p></article>"
        "<article class=\"card\"><h3>Dealer &amp; partner meetings</h3><p>Groups of 100–300 that want a city or coastal hotel close to the airport.</p></article>"
        "<article class=\"card\"><h3>City-and-coast incentives</h3><p>Old City, hammam and Turquoise Coast experiences combined with a hotel base, with indoor alternatives planned alongside.</p></article>"
        "<article class=\"card\"><h3>Exhibitions &amp; large meetings</h3><p>Programmes that need a venue such as the Antalya EXPO Center rather than a hotel ballroom; availability is confirmed per brief.</p></article></div>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Cost Comparison</h2>",
        "      <p>Published reference ranges for Antalya, shown for the spring and autumn programme season (April – June and September – November). They are the starting point for the comparison, not an off-peak price.</p>",
        "      " + table("Antalya reference ranges, per person (reviewed September 2026)",
                         ["Programme type", "Group size (pax)", "Nights", "Budget range (€/pax)"], ref_rows),
        '      <p class="price-note">All-in per-person totals: hotel accommodation, venue hire or ballroom use, full-board F&amp;B (or equivalent), airport transfers, programme activities and DMC management fee. Flights excluded. Peak July – August carries a 15–25% premium. Source: <a href="/event-costs/antalya/">Antalya event costs</a>.</p>',
        '      <div class="offseason-callout"><h3>How the comparison works</h3>'
        "<p>For your dates we price the off-peak window and a peak-season window side by side for the same programme: same hotel category, scope, group size and nights. %s</p>"
        '<p><a class="btn btn--primary" href="#compare">Compare Dates &amp; Event Costs</a></p></div>' % esc(saving_sentence()),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Operating Conditions</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Hotel and venue availability</h3><p>Hotels and venues keep different facilities open from December to February. We confirm which properties, rooms and venues are available for your dates before we quote.</p></article>"
        '<article class="card"><h3>Getting around</h3><p>Antalya Airport is 13 km from the city centre (15–30 minutes). Indicative vehicle prices are on the <a href="/antalya-transfer-prices/">Antalya transfer prices</a> page.</p></article>'
        "<article class=\"card\"><h3>Weather and indoor plan</h3><p>Days are cooler and shorter, so programmes are planned indoor-first (ballroom, spa, hammam, city culture) with outdoor sessions as weather-dependent additions.</p></article></div>",
        "    </section>",
        faq_html(faqs),
        form_html(fixed_destination="Antalya"),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="%s">Off-season events in Turkey</a><a href="/destinations/antalya/">Antalya destination guide</a>'
        '<a href="/event-costs/antalya/">Antalya event costs</a>'
        '<a href="/antalya-transfer-prices/">Antalya transfer prices</a>'
        '<a href="%s">Belek off-season guide</a><a href="%s">Istanbul off-season guide</a></p></section>' % (data.HUB, BELEK_PATH, ISTANBUL_PATH),
    ])
    return assemble(head_html(title, description, ANTALYA_URL, "Off-Season Events", "Antalya Off-Season",
                              schema("Off-Season Events in Antalya", ANTALYA_URL, description,
                                     [(n, p) for n, p in crumbs], faqs)), body)


# --- Istanbul page --------------------------------------------------------------

def render_istanbul():
    title = "Off-Season Events in Istanbul | Off-Peak Dates &amp; Costs"
    description = ("Off-peak dates for conferences, executive meetings and corporate events in Istanbul. See the "
                   "planning window, reference costs and operating conditions, and compare dates side by side.")
    faqs = faq_istanbul()
    crumbs = [("Home", "/"), ("Off-Season Events", data.HUB), ("Istanbul", ISTANBUL_PATH)]
    ref_rows = [list(r) for r in ISTANBUL_REFERENCE]
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Off-Season Events in Istanbul: Off-Peak Dates &amp; Planning Windows</h1>",
        "      " + season_note(),
        '      <p class="page-section__lede">Istanbul is Turkey’s city destination for conferences, executive meetings '
        "and corporate events, with the largest concentration of meeting-capable city hotels. In January and "
        "February demand from conference groups is lower, which gives planners with flexible dates more "
        "availability and more room to negotiate. Because Istanbul is priced line by line, we show the date "
        "comparison the same way.</p>",
        "      " + hero_buttons('<a class="btn btn--ghost" href="%s">Off-season in Antalya</a>' % ANTALYA_PATH),
        "      " + EXPECT,
        '      <div class="offseason-callout"><p><strong>Scope of this page:</strong> city programmes in Istanbul: '
        'business hotels, city venues and short-stay groups. For resort-based programmes see '
        '<a href="%s">Belek</a>; for city and coast in the south see <a href="%s">Antalya</a>. For an all-year '
        'overview see the <a href="/destinations/istanbul/">Istanbul destination guide</a>.</p></div>' % (BELEK_PATH, ANTALYA_PATH),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Suitable Date Windows</h2>",
        "      " + table("Istanbul planning windows (%s)" % data.SEASON_LABEL, ["Window", "Role", "What to expect"], [
            ["January – February", "Core off-peak window", "Cooler weather (about 5–12°C) and the most room to negotiate. Meeting rooms and venues are confirmed per brief."],
            ["July – August", "Possible secondary window", "Quieter for business events, but peak leisure season for city hotels; published rates carry a 15–25% premium. We compare it before assuming a saving."],
            ["New Year week and public holidays", "Exceptions", "Demand and rates can differ sharply; these weeks are usually priced separately."],
            [PEAK, "Peak MICE months", "The comparison baseline: the busiest conference and incentive months."],
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Events That Fit the Off-Peak Window</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Conferences &amp; congresses</h3><p>Business sessions that need meeting rooms, AV and a hosted dinner in a city hotel or congress venue.</p></article>"
        "<article class=\"card\"><h3>Executive &amp; board meetings</h3><p>Short stays of 20–60 guests where hotel location and meeting-room quality matter most.</p></article>"
        "<article class=\"card\"><h3>Corporate events &amp; hosted dinners</h3><p>Company events combining a business day with a hosted dinner or an optional city experience.</p></article>"
        "<article class=\"card\"><h3>Premium city incentives</h3><p>Small groups of 30–80 with indoor-first cultural programmes and a Bosphorus experience where conditions allow.</p></article></div>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Cost Comparison</h2>",
        "      <p>Published reference ranges for Istanbul, shown for the spring and autumn programme season (April – June and September – November). They are the starting point for the comparison, not an off-peak price.</p>",
        "      " + table("Istanbul reference ranges, per person (reviewed September 2026)",
                         ["Programme type", "Group size (pax)", "Nights", "Budget range (€/pax)"], ref_rows),
        '      <p class="price-note">All-in per-person totals: hotel accommodation, venue hire or ballroom use, full-board F&amp;B (or equivalent), airport transfers, programme activities and DMC management fee. Flights excluded. Istanbul is priced as itemised line items: room, meeting space, F&amp;B and production. Peak July – August carries a 15–25% premium. Source: <a href="/event-costs/istanbul/">Istanbul event costs</a>.</p>',
        '      <div class="offseason-callout"><h3>How the comparison works</h3>'
        "<p>For your dates we price the off-peak window and a peak-season window side by side for the same programme: same hotel category, scope, group size and nights. %s</p>"
        '<p><a class="btn btn--primary" href="#compare">Compare Dates &amp; Event Costs</a></p></div>' % esc(saving_sentence()),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Operating Conditions</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Hotel and venue availability</h3><p>City hotels generally operate all year, but meeting rooms, venues and city events calendars differ by date. We confirm availability for your dates before we quote.</p></article>"
        "<article class=\"card\"><h3>Getting around</h3><p>Istanbul Airport is 35–45 km from the city centre (40–60 minutes by road). Traffic affects transfer timing, so group movements are kept to a minimum.</p></article>"
        "<article class=\"card\"><h3>Weather and indoor plan</h3><p>Winter days are cool (about 5–12°C), so programmes are planned indoor-first: hotel meeting rooms, museums, covered venues and dinners, with outdoor sessions as weather-dependent additions.</p></article></div>",
        "    </section>",
        faq_html(faqs),
        form_html(fixed_destination="Istanbul"),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="%s">Off-season events in Turkey</a><a href="/destinations/istanbul/">Istanbul destination guide</a>'
        '<a href="/event-costs/istanbul/">Istanbul event costs</a>'
        '<a href="%s">Antalya off-season guide</a><a href="%s">Belek off-season guide</a></p></section>' % (data.HUB, ANTALYA_PATH, BELEK_PATH),
    ])
    return assemble(head_html(title, description, ISTANBUL_URL, "Off-Season Events", "Istanbul Off-Season",
                              schema("Off-Season Events in Istanbul", ISTANBUL_URL, description,
                                     [(n, p) for n, p in crumbs], faqs)), body)


# --- Bodrum page ----------------------------------------------------------------

def render_bodrum():
    title = "Off-Season Events in Bodrum | Off-Peak Dates &amp; Costs"
    description = ("Off-peak dates for premium incentives, executive retreats and private group programmes in Bodrum. "
                   "See the planning window, reference costs and operating conditions, and compare dates side by side.")
    faqs = faq_bodrum()
    crumbs = [("Home", "/"), ("Off-Season Events", data.HUB), ("Bodrum", BODRUM_PATH)]
    ref_rows = [list(r) for r in BODRUM_REFERENCE]
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Off-Season Events in Bodrum: Off-Peak Dates &amp; Planning Windows</h1>",
        "      " + season_note(),
        '      <p class="page-section__lede">Bodrum is a small-group destination: boutique hotels, private villas and '
        "Aegean experiences for incentives and executive retreats of roughly 15–80 guests. The planning window runs "
        "from October to April. It is a different kind of off-season from Antalya’s: October and April are the "
        "strongest months for small groups, while from November to March many boutique hotels and gulet operators "
        "close, so availability is confirmed before anything is quoted.</p>",
        "      " + hero_buttons('<a class="btn btn--ghost" href="%s">Off-season in Istanbul</a>' % ISTANBUL_PATH),
        "      " + EXPECT,
        '      <div class="offseason-callout"><p><strong>Scope of this page:</strong> small-group and premium '
        'programmes in Bodrum. For resort conferences see <a href="%s">Belek</a> or <a href="%s">Antalya</a>; for an '
        'all-year overview see the <a href="/destinations/bodrum/">Bodrum destination guide</a>.</p></div>' % (BELEK_PATH, ANTALYA_PATH),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Suitable Date Windows</h2>",
        "      " + table("Bodrum planning windows (%s)" % data.SEASON_LABEL, ["Window", "Role", "What to expect"], [
            ["October", "Strong off-peak month", "Mild weather, hotels still fully operational and little leisure traffic; one of the best months for small groups."],
            ["April", "Strong off-peak month", "Quiet and mild; boutique hotels are reopening, which suits small executive retreats."],
            ["November – March", "Limited availability", "Cooler (about 10–18°C). Many boutique hotels and gulet operators are closed; city-centre properties stay open. Confirmed per brief."],
            ["May – June, September and July – August", "Comparison baseline", "May – June and September are the main shoulder months; July – August is peak leisure season with the highest rates."],
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Events That Fit the Off-Peak Window</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Executive retreats</h3><p>Small leadership groups in a boutique hotel or private villa with a private programme.</p></article>"
        "<article class=\"card\"><h3>Premium incentives</h3><p>Reward trips of 15–80 guests built around a boutique hotel, local gastronomy and cultural experiences.</p></article>"
        "<article class=\"card\"><h3>Private group programmes</h3><p>Corporate hospitality and private gatherings for groups that value privacy over scale.</p></article>"
        "<article class=\"card\"><h3>Hotel-based winter meetings</h3><p>Short meetings in properties that stay open year-round, planned indoor-first.</p></article></div>",
        '      <p class="section-more">Typical Bodrum groups are 15–80 guests, up to about 120 across several properties.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Cost Comparison</h2>",
        "      <p>Published reference figures for Bodrum, based on the shoulder season (May – June and October). They are the starting point for the comparison, not an off-peak price.</p>",
        "      " + table("Bodrum reference ranges, per person (reviewed September 2026)",
                         ["Programme type", "Group size (pax)", "Nights", "Budget range (€/pax)"], ref_rows),
        '      <p class="price-note">Planning ranges per person; flights excluded. Sources: the <a href="/event-costs/">Turkey event costs overview</a> and the <a href="/destinations/bodrum/">Bodrum destination guide</a>. Bodrum has no separate event-cost page yet.</p>',
        '      <div class="offseason-callout"><h3>How the comparison works</h3>'
        "<p>For your dates we price the off-peak window and a peak-season window side by side for the same programme: same hotel category, scope, group size and nights. %s</p>"
        '<p><a class="btn btn--primary" href="#compare">Compare Dates &amp; Event Costs</a></p></div>' % esc(saving_sentence(BODRUM_PEAK)),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Operating Conditions</h2>",
        '      <div class="card-grid">'
        "<article class=\"card\"><h3>Hotel and service availability</h3><p>Many boutique hotels and gulet operators close from November to March; city-centre properties stay open. We confirm what is operating for your dates before we quote.</p></article>"
        "<article class=\"card\"><h3>Getting there</h3><p>Milas-Bodrum Airport (BJV) is 30–45 minutes from Bodrum town and Yalıkavak marina.</p></article>"
        "<article class=\"card\"><h3>Weather and indoor plan</h3><p>Gulet and yacht programmes depend on operators and sea conditions and are best from May to October, so outside those months we plan hotel-based, indoor-first programmes.</p></article></div>",
        "    </section>",
        faq_html(faqs),
        form_html(fixed_destination="Bodrum"),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="%s">Off-season events in Turkey</a><a href="/destinations/bodrum/">Bodrum destination guide</a>'
        '<a href="/event-costs/">Turkey event costs</a>'
        '<a href="%s">Istanbul off-season guide</a><a href="%s">Antalya off-season guide</a></p></section>' % (data.HUB, ISTANBUL_PATH, ANTALYA_PATH),
    ])
    return assemble(head_html(title, description, BODRUM_URL, "Off-Season Events", "Bodrum Off-Season",
                              schema("Off-Season Events in Bodrum", BODRUM_URL, description,
                                     [(n, p) for n, p in crumbs], faqs)), body)


# --- pop-up data block ------------------------------------------------------------

JS_BEGIN = "/* offseason-data:begin */"
JS_END = "/* offseason-data:end */"


def js_block():
    lines = ["  var OFFPEAK = {"]
    items = []
    for d in data.DESTINATIONS:
        items.append('    %s: { name: %s, window: %s, page: %s }' % (
            d["slug"], json.dumps(d["name"]), json.dumps(d["window"], ensure_ascii=False),
            json.dumps(data.popup_link(d["slug"]))))
    lines.append(",\n".join(items))
    lines.append("  };")
    pct = data.saving_percent()
    lines.append("  // Percentage shown in the pop-up only when backed by like-for-like quotes (tools/off_season_data.py).")
    lines.append("  var OFFPEAK_SAVING = %s;" % (json.dumps(pct) if pct else "null"))
    lines.append("  var OFFPEAK_PEAK = %s;" % json.dumps(PEAK, ensure_ascii=False))
    return "\n".join(lines)


def write_js():
    p = os.path.join(ROOT, "assets", "js", "main.js")
    s = open(p, encoding="utf-8").read()
    pat = re.compile(re.escape(JS_BEGIN) + r".*?" + re.escape(JS_END), re.S)
    if not pat.search(s):
        raise SystemExit("Missing offseason-data markers in assets/js/main.js")
    t = pat.sub(lambda _m: JS_BEGIN + "\n" + js_block() + "\n  " + JS_END, s, count=1)
    if t != s:
        open(p, "w", encoding="utf-8").write(t)
    return t != s


def write_page(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html + "\n")
    site_seo.patch(path, site_seo.identity_block())
    print("wrote /%s" % os.path.dirname(rel))


def main():
    write_page("off-season-events-turkey/index.html", render_hub())
    write_page("off-season-events-turkey/belek/index.html", render_belek())
    write_page("off-season-events-turkey/antalya/index.html", render_antalya())
    write_page("off-season-events-turkey/istanbul/index.html", render_istanbul())
    write_page("off-season-events-turkey/bodrum/index.html", render_bodrum())
    print("%s assets/js/main.js" % ("updated" if write_js() else "unchanged"))
    print("saving claim: %s" % (("up to %d%%" % data.saving_percent()) if data.saving_percent() else "none (percentage-free)"))


if __name__ == "__main__":
    main()
