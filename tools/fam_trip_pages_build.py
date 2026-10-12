#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Fam Trip search-intent pages.

Usage: python3 tools/fam_trip_pages_build.py   (then: python3 tools/sitemaps.py)

Writes:
  antalya-fam-trips/index.html       permanent service page (agencies that want a fam trip organised)
  antalya-fam-trip-2027/index.html   2027 programme, eligibility and review process
The invitation/application page stays /agency-fam-trip-2027/ (tools/fam_trip_build.py).
Idempotent. Only facts already on the site are used: credentials from the footer, the
reply/proposal timings used on /dmc-turkey-uk-agencies/, published cost pages, and the
campaign's "proposed, subject to written confirmation" programme. No dates, hotel names,
prices, participant numbers, testimonials or a 2026 programme.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from market_pages_build import assemble, cards, crumbs_html, faq_html, head, schema, steps, write_page  # noqa: E402

HUB_PATH = "/antalya-fam-trips/"
PROGRAMME_PATH = "/antalya-fam-trip-2027/"
APPLY_PATH = "/agency-fam-trip-2027/"

HUB_FAQ = [
    ("What is a fam trip?",
     "A familiarisation (fam) trip lets agency and corporate buyers see hotels, venues and suppliers in person before "
     "they recommend a destination to clients. A local DMC builds the itinerary and runs the logistics on the ground."),
    ("Can you organise a fam trip for our own agency or client group?",
     "Yes. Send us the destination, the number of guests and the dates you have in mind. We reply within 24 hours and "
     "send an itemised proposal within 3–5 business days. Scope, inclusions and costs are agreed in writing before "
     "anything is booked."),
    ("Which destinations can a fam trip cover?",
     "Antalya and Belek are the focus of this page. We also operate in Istanbul, Cappadocia and Bodrum, so a "
     "multi-destination itinerary is possible."),
    ("Is the 2027 fam trip the same thing?",
     "No. This page describes fam trips we organise for your group. The 2027 Antalya and Belek programme is a separate, "
     "invitation-based trip for agencies, described on its own page, and its details remain subject to written "
     "confirmation."),
    ("Can the fam trip run under our agency’s brand?",
     "Where appropriate, yes. We can work white-label: your agency keeps the relationship with its guests and we "
     "handle local execution."),
]

PROGRAMME_FAQ = [
    ("Who is the 2027 fam trip for?",
     "Incentive and MICE agencies, corporate event and group travel planners, and agency owners, directors and "
     "senior decision-makers who manage international group programmes. Priority goes to agencies that organise at "
     "least two international group programmes a year."),
    ("Are flights included?",
     "No. International flights are expected to be arranged by participants. The proposed hosted elements are "
     "accommodation, local transfers and scheduled programme activities."),
    ("When does it take place?",
     "The proposed period is January–March 2027. Exact dates have not been confirmed; they will be shared with "
     "shortlisted applicants."),
    ("How are applications reviewed?",
     "Individually. Our team reviews each application and contacts shortlisted applicants with further information. "
     "Registering your interest does not guarantee a place."),
    ("Is there a 2026 programme?",
     "No 2026 fam trip programme is published by DMC Turkey Partner. If you need a fam trip sooner, we can plan one "
     "for your own group; see our Antalya fam trips service page."),
]


def hub():
    title = "Antalya Fam Trips for Agencies | DMC Turkey Partner"
    description = ("Plan a fam trip in Antalya and Belek with a local DMC: hotel and venue inspections, transfers "
                   "and supplier meetings for agencies and MICE planners.")
    crumbs = [("Home", "/"), ("Antalya Fam Trips", HUB_PATH)]
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Antalya Fam Trips for Agencies &amp; MICE Planners</h1>",
        '      <p class="reviewed-note">Last updated: <time datetime="2026-10">October 2026</time></p>',
        '      <p class="page-section__lede">A fam trip lets you see the hotels, venues and people behind a destination '
        "before you recommend it to a client. DMC Turkey Partner has operated in Turkey since 2006 and can plan and run "
        "a fam trip for your agency or client group in Antalya and Belek, with one local team handling the logistics.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="/request-proposal/?src=antalya-fam-trips">'
        'Plan a Fam Trip</a><a class="btn btn--ghost" href="%s">See the 2027 Programme</a></div>' % PROGRAMME_PATH,
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Who a Fam Trip Is For</h2>",
        "      <ul><li>Incentive and MICE agencies choosing a destination for upcoming client programmes.</li>"
        "<li>Corporate event and group travel planners who want to inspect venues first-hand.</li>"
        "<li>Overseas agencies that need a local partner to host their own buyers or key clients.</li></ul>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>What We Can Arrange</h2>",
        "      " + cards([
            ("Hotel &amp; venue inspections", "Site visits to resorts, meeting hotels and event venues in Antalya and Belek, scheduled around your questions."),
            ("Supplier meetings", "Introductions to the teams behind transport, production, staffing and on-site coordination."),
            ("Transfers &amp; logistics", "Airport transfers and ground transport for the whole itinerary."),
            ("Evening &amp; incentive experiences", "Dinners and group activities that show how a programme would feel for your guests."),
        ]),
        '      <p class="section-more">Need your agency to keep the client relationship? See '
        '<a href="/white-label-dmc-turkey/">white-label DMC support</a>.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Antalya and Belek at a Glance</h2>",
        "      <p>Antalya offers city hotels, conference venues and a major airport; Belek concentrates large "
        "5-star resorts used for incentive travel and corporate retreats. Read the destination guides for "
        'venues, transfers and seasonality: <a href="/destinations/antalya/">Antalya</a> and '
        '<a href="/destinations/belek/">Belek</a>. For budgeting, see the published '
        '<a href="/event-costs/">event cost ranges</a> and the '
        '<a href="/event-cost-calculator/">event budget calculator</a>.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>How It Works</h2>",
        "      " + steps([
            ("Send Your Brief", "Destination, number of guests and the dates you have in mind."),
            ("Reply Within 24 Hours", "We confirm what is possible and ask the right questions."),
            ("Itemised Proposal", "Within 3–5 business days, with inclusions and costs in writing."),
            ("Coordinator &amp; Delivery", "Once you confirm, a named coordinator runs the trip on the ground."),
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Looking for the 2027 Fam Trip?</h2>",
        '      <p>We are also planning an invitation-based Antalya and Belek fam trip for agencies in 2027. Read the '
        '<a href="%s">2027 programme and eligibility</a>, or go straight to the '
        '<a href="%s?src=fam-hub">application page</a>.</p>' % (PROGRAMME_PATH, APPLY_PATH),
        "    </section>",
        faq_html("Frequently Asked Questions", HUB_FAQ),
        '    <section class="page-section"><div class="cta-banner"><h2>Plan a Fam Trip for Your Agency</h2>'
        '<div class="cta-banner__actions"><a class="btn btn--primary" href="/request-proposal/?src=antalya-fam-trips">'
        'Send Your Brief</a></div></div></section>',
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="/incentive-travel-turkey/">Incentive travel in Turkey</a><a href="/mice-turkey/">MICE Turkey</a>'
        '<a href="/dmc-turkey/">DMC Turkey</a><a href="/agency-partners/">Agency partners</a>'
        '<a href="/destinations/">Destinations</a></p></section>',
    ])
    return assemble(head("en", title, description, HUB_PATH, "Fam Trip Guide", "Fam Trip",
                         schema("en", "Antalya Fam Trips for Agencies", HUB_PATH, description, crumbs, HUB_FAQ)), body)


def programme():
    title = "Antalya & Belek Fam Trip 2027: Programme | DMC Turkey Partner"
    description = ("Proposed 3-night Antalya and Belek fam trip for agencies in 2027: itinerary outline, "
                   "eligibility and how applications are reviewed.")
    crumbs = [("Home", "/"), ("Antalya Fam Trips", HUB_PATH), ("2027 Programme", PROGRAMME_PATH)]
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>Antalya &amp; Belek Fam Trip 2027: Programme and Eligibility</h1>",
        '      <p class="reviewed-note">Last updated: <time datetime="2026-10">October 2026</time></p>',
        '      <p class="page-section__lede">DMC Turkey Partner is planning a familiarisation trip to Antalya and Belek for '
        "agencies in 2027. This page outlines the proposed programme, who should apply and how applications are "
        "reviewed. Everything below is proposed and subject to written confirmation.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="%s?src=fam-2027-guide">Register Your Interest</a>'
        "</div>" % APPLY_PATH,
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Proposed Programme at a Glance</h2>",
        '      <p class="page-section__lede">Proposed period: January–March 2027. Exact dates are not confirmed.</p>',
        "      <ul><li><strong>Length:</strong> three nights in Antalya and Belek.</li>"
        "<li><strong>Focus:</strong> hotel and venue inspections, meeting our local operations team and networking.</li>"
        "<li><strong>Format:</strong> a small group of agency decision-makers; applications are reviewed individually.</li></ul>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Indicative Itinerary</h2>",
        '      <ol class="fam-programme"><li><strong>Day 1</strong>Arrival, hotel check-in and welcome dinner.</li>'
        "<li><strong>Day 2</strong>Hotel and venue inspections across Antalya and Belek.</li>"
        "<li><strong>Day 3</strong>Incentive experience, operations presentation and networking dinner.</li>"
        "<li><strong>Day 4</strong>Breakfast, airport transfer and departure.</li></ol>",
        '      <p class="price-note">Indicative programme, subject to confirmation.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>What Is Proposed to Be Hosted</h2>",
        "      <ul><li>Accommodation</li><li>Local transfers</li><li>Scheduled programme activities</li></ul>",
        "      <p>International flights are expected to be arranged by participants. All inclusions, exclusions, dates, "
        "eligibility and cancellation conditions remain subject to written confirmation.</p>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Eligibility</h2>",
        "      <p>The invitation is aimed at incentive and MICE agencies, corporate event and group travel planners, and "
        "agency owners, directors and senior decision-makers who manage international group programmes. Priority goes "
        "to agencies that organise at least two international group programmes a year.</p>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>How to Apply</h2>",
        "      " + steps([
            ("Register Your Interest", "Complete the short application on the invitation page."),
            ("Individual Review", "Our team reviews every application."),
            ("Shortlisted Applicants", "We contact shortlisted applicants with dates, inclusions and conditions in writing."),
        ]),
        '      <p><a class="btn btn--primary" href="%s?src=fam-2027-guide">Go to the Application Page</a></p>' % APPLY_PATH,
        "    </section>",
        faq_html("Frequently Asked Questions", PROGRAMME_FAQ),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="%s">Antalya fam trips for your own group</a><a href="/destinations/antalya/">Antalya</a>'
        '<a href="/destinations/belek/">Belek</a><a href="/agency-partners/">Agency partners</a></p></section>' % HUB_PATH,
    ])
    page_head = head("en", title, description, PROGRAMME_PATH, "Fam Trip Guide", "Fam Trip 2027",
                     schema("en", "Antalya & Belek Fam Trip 2027: Programme", PROGRAMME_PATH, description, crumbs,
                            PROGRAMME_FAQ))
    # The itinerary list reuses the .fam-programme styles from the campaign stylesheet.
    page_head = page_head.replace('<link rel="stylesheet" href="/assets/css/forms.css">',
                                  '<link rel="stylesheet" href="/assets/css/forms.css">\n'
                                  '  <link rel="stylesheet" href="/assets/css/fam-trip.css">', 1)
    return assemble(page_head, body)


def main():
    write_page("antalya-fam-trips/index.html", hub())
    write_page("antalya-fam-trip-2027/index.html", programme())


if __name__ == "__main__":
    main()
