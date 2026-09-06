# -*- coding: utf-8 -*-
"""Phase 1 COP31 pages: the hub, the core informational guides and the two
broadest commercial service pages. Content is original; official facts are
sourced from UNFCCC and the COP31 Türkiye Presidency (see cop31_common)."""

from cop31_links import A, L
from cop31_render import (
    cards,
    checklist,
    cluster,
    facts,
    lede,
    para,
    plain_list,
    section,
    steps,
    table,
)

HERO_FACTS = [
    ("Conference", "COP31 — 2026 UN Climate Change Conference"),
    ("Dates", "9–20 November 2026"),
    ("Host city", "Antalya, Türkiye"),
    ("Venue", "Antalya EXPO Center"),
]

WHO_WE_SUPPORT = (
    "International event agencies, national delegations, pavilion owners, exhibitors, "
    "NGOs and observer organisations, corporate and media teams, and production "
    "companies arriving in Antalya without a local supply chain."
)

SERVICE_CARDS = cards([
    ("Printing &amp; Collateral", "/cop31-printing-services/",
     "Brochures, roll-ups, banners, foam board, desk graphics and event collateral produced locally in Antalya, including short-notice runs during the conference."),
    ("Exhibition Stands", "/cop31-exhibition-stands/",
     "Modular and custom stand production, graphics, installation, on-site support and dismantling for exhibitors at the venue and at side-event locations."),
    ("Event Production", "/cop31-event-production/",
     "Staging, sound, screens, lighting and technical crew for side events, receptions, briefings, press moments and breakout sessions."),
    ("Furniture Rental", "/cop31-furniture-rental/",
     "Meeting tables, chairs, stools, counters, lounge and exhibition furniture delivered, installed and collected to your schedule."),
    ("Coffee &amp; Hospitality", "/cop31-coffee-machine-rental/",
     "Coffee machines, coffee stations, water and hospitality equipment for pavilions, stands and delegation lounges, subject to availability."),
    ("Hostesses", "/cop31-hostess-staff/",
     "Welcome, registration desk and guest-direction staff, with multilingual profiles where available for international delegations."),
    ("Transportation", "/cop31-private-transfers/",
     "Chauffeured cars, vans, minibuses and coaches for delegation movements, hotel–venue runs, executive dinners and off-site meetings."),
    ("AV &amp; Equipment Rental", "/cop31-av-equipment-rental/",
     "LED screens, monitors, projection, sound, microphones, presentation equipment and technicians for stands, pavilions and meeting rooms."),
    ("Branding &amp; Signage", "/cop31-branding-signage/",
     "Wayfinding, venue dressing, counters, backdrops, sponsor boards and branded environments produced and installed locally."),
    ("Temporary Staff", "/cop31-event-staff/",
     "Setup crews, runners, logistics and operational staff for build days, live days and dismantling."),
    ("Last-Minute Production", "/cop31-last-minute-services/",
     "Fast local sourcing and production when a shipment is delayed, an item is missing or a requirement appears on site."),
    ("Rapid Support", "/cop31-rapid-response-services/",
     "A single Antalya contact for urgent replacement, delivery and problem-solving during the conference period."),
])


# --- 1. Power page -----------------------------------------------------------

HUB = {
    "slug": "cop31-antalya",
    "breadcrumb": "COP31 Antalya 2026",
    "title": "COP31 Antalya 2026 | Dates, Venue, Hotels, Transport &amp; Local Services",
    "description": (
        "Planning for COP31 Antalya 2026? Find dates, venue information, hotels, transport "
        "and local event services including exhibition stands, printing, AV, staffing and "
        "last-minute support."
    ),
    "h1": "COP31 Antalya 2026 – Complete Participant &amp; Local Services Guide",
    "answer": (
        "COP31, the 2026 UN Climate Change Conference, takes place in Antalya, Türkiye, "
        "from 9 to 20 November 2026 at the Antalya EXPO Center."
    ),
    "lede": (
        "Everything international agencies, delegations, exhibitors, pavilions and event teams "
        "need for COP31 in Antalya — from venue, transport and accommodation information to "
        "production, logistics and rapid-response local services."
    ),
    "hero_facts": HERO_FACTS,
    "page_type": "informational",
    "service_interest": "COP31 General Support",
    "service_name": "COP31 Antalya Local Operations Support",
    "update_sensitive": True,
    "sources": ["unfccc", "ifp", "road", "tr", "programme"],
    "sections": [
        section(
            "COP31 Antalya 2026 at a Glance",
            lede(
                "COP31 is the thirty-first Conference of the Parties to the UN Framework "
                "Convention on Climate Change. Türkiye hosts the conference and holds the "
                "COP31 Presidency, while Australia serves as President of Negotiations under "
                "the arrangement agreed between the two countries. For anyone planning to be "
                "in Antalya, the practical consequences are straightforward: a two-week "
                "conference, a single main venue east of the city, a very heavy demand period "
                "for hotels, vehicles and local suppliers, and a compressed build window before "
                "the opening day."
            ),
            table(
                "Key COP31 Antalya 2026 planning facts",
                ["Item", "Detail"],
                [
                    ["Conference", "COP31 — 2026 UN Climate Change Conference"],
                    ["Dates", "9–20 November 2026"],
                    ["City", "Antalya, Türkiye"],
                    ["Venue", "Antalya EXPO Center"],
                    ["Host / Presidency", "Türkiye"],
                    ["President of Negotiations", "Australia"],
                    ["World Leaders Climate Action Summit", "11–12 November 2026"],
                    ["Registration", "UNFCCC Online Registration System (ORS)"],
                ],
            ),
            para(
                "Detail on each of these sits on its own page: " + A("/cop31-antalya-dates/", "the full date and planning timeline")
                + ", " + A("/cop31-antalya-program/", "the official programme and thematic days")
                + ", " + A("/cop31-antalya-venue/", "the venue and how to reach it")
                + ", and " + A("/cop31-antalya-registration/", "how registration and accreditation work") + "."
            ),
        ),
        section(
            "Who This Guide Is For",
            lede(
                "This cluster is written for the people who have to make COP31 work "
                "operationally rather than diplomatically: " + WHO_WE_SUPPORT
            ),
            para(
                "If you are attending as an individual participant, the "
                + A("/cop31-antalya-participant-guide/", "COP31 participant guide")
                + " is the most useful starting point. If you are responsible for a stand, a "
                "pavilion, a delegation programme or a side event, the service pages below "
                "describe what can be produced, rented, staffed and moved locally in Antalya."
            ),
        ),
        section(
            "Plan Your COP31 — Informational Guides",
            lede(
                "Start with the factual questions. Each guide answers the question first, "
                "then connects it to the operational decisions that follow from it."
            ),
            cards([
                ("COP31 Participant Guide", "/cop31-antalya-participant-guide/",
                 "A practical A–Z for attendees: dates, venue, registration, badges, hotels, transport, dining, interpretation and local support."),
                ("COP31 Dates 2026", "/cop31-antalya-dates/",
                 "Conference start and end dates, the Leaders Summit window, and a working timeline for booking rooms, vehicles and production."),
                ("COP31 Programme &amp; Thematic Days", "/cop31-antalya-program/",
                 "How the official programme is structured, which themes have been announced, and what each usually implies for agency workloads."),
                ("COP31 Venue &amp; Location", "/cop31-antalya-venue/",
                 "Where the Antalya EXPO Center sits relative to the airport, the city, Lara and Belek, and what that means for movement planning."),
                ("Antalya EXPO Center Guide", "/cop31-antalya-expo-center/",
                 "A venue-focused briefing for exhibitors and delegation teams: access, surroundings, build logistics and local operating context."),
                ("COP31 Registration", "/cop31-antalya-registration/",
                 "Who can register, how the UNFCCC Online Registration System works, and where the official nomination and badge rules live."),
                ("COP31 Hotels", "/cop31-antalya-hotels/",
                 "Where to stay: the Aksu, Lara, Belek, airport and city-centre options, and the trade-off between distance and shuttle access."),
                ("COP31 Transport", "/cop31-antalya-transport/",
                 "How official shuttles, airport arrivals and hotel–venue movement work, and when a dedicated vehicle is the better answer."),
            ]),
        ),
        section(
            "Need Something in Antalya During COP31?",
            lede(
                "One local operations desk for planned and last-minute COP31 requirements. "
                "Every card below links to what is actually delivered, who it is for and how "
                "to request it."
            ),
            SERVICE_CARDS,
        ),
        section(
            "Planned Production and Last-Minute Requirements Are Not the Same Job",
            lede(
                "Most COP31 operational problems fall into two very different categories, and "
                "they need to be handled differently."
            ),
            table(
                "Two operating modes for COP31 Antalya",
                ["", "Planned production", "Last-minute requirement"],
                [
                    ["Typical trigger", "A confirmed stand, pavilion, side event or delegation programme", "A delayed shipment, a missing item, a damaged graphic, a supplier no-show"],
                    ["Lead time", "Weeks to months before 9 November", "Hours to a day, usually during 9–20 November"],
                    ["What matters most", "Specification, drawings, approvals, budget, build schedule", "Local availability, access to the venue, someone physically in Antalya"],
                    ["Where to start", A("/cop31-event-services/", "COP31 Event Services"), A("/cop31-last-minute-services/", "Last-Minute COP31 Services")],
                ],
            ),
            para(
                "The reason to name both is that international teams often plan the first and "
                "then discover they have no route to the second. Having a local operations "
                "contact already briefed before the conference opens is usually the difference "
                "between a fixable problem and a visible one. See also "
                + A("/cop31-rapid-response-services/", "rapid response services") + " and "
                + A("/cop31-emergency-event-support/", "emergency event support") + "."
            ),
        ),
        section(
            "Exhibiting, Running a Pavilion or Hosting a Side Event",
            cards([
                ("COP31 Event Services", "/cop31-event-services/",
                 "The broad local operations scope: side events, dinners, meeting spaces, staffing, AV, printing, transport and supplier coordination in one plan."),
                ("COP31 Exhibition Services", "/cop31-exhibition-services/",
                 "Exhibitor support across setup, graphics, furniture, AV, storage, on-site troubleshooting and dismantling."),
                ("COP31 Pavilion Services", "/cop31-pavilion-services/",
                 "Production, branding, furniture, AV, hospitality, staffing and technical support for country, organisation and initiative pavilions."),
                ("COP31 Booth Builder in Antalya", "/cop31-booth-builder-antalya/",
                 "A quote-driven route for teams that already know the stand size and need a local builder in Antalya."),
            ]),
        ),
        section(
            "How Working With a Local Operations Partner Works",
            steps([
                ("Send the requirement",
                 "A stand size, a delegation size, a delivery date, a photo of a damaged graphic — whatever you actually have. Incomplete briefs are normal at this stage."),
                ("Local feasibility check",
                 "We confirm what is realistically available in Antalya for your dates, flag anything that will not work, and say so plainly rather than quoting around it."),
                ("Scope and quotation",
                 "A written scope with what is included, what is excluded and what depends on venue access or approvals you hold."),
                ("Pre-conference coordination",
                 "Production, delivery windows, staffing, vehicles and installation timings are aligned before the build period starts."),
                ("On-site delivery",
                 "A local contact in Antalya during the conference, so a problem is handled by someone who can physically get to the venue."),
            ]),
        ),
        section(
            "Where DmcTurkeyPartner Fits — and Where It Does Not",
            lede(
                "We are an independent local operations provider. That distinction matters for "
                "anyone planning COP31 attendance, so it is worth being explicit."
            ),
            table(
                "Official COP31 arrangements vs. independent local services",
                ["", "Handled by the official COP31 / UNFCCC bodies", "Handled by DmcTurkeyPartner"],
                [
                    ["Registration and badges", "Yes — through the UNFCCC Online Registration System", "No"],
                    ["Conference programme and venue access rules", "Yes", "No"],
                    ["Official accommodation platform and complimentary shuttles", "Yes", "No"],
                    ["Independent hotel and group room sourcing", "No", "Yes"],
                    ["Private and delegation transport", "No", "Yes"],
                    ["Stands, pavilions, production, printing, AV, furniture, staffing", "No", "Yes"],
                    ["Last-minute local sourcing during the conference", "No", "Yes"],
                ],
            ),
            para(
                "For anything in the first column, use the official resources listed at the "
                "bottom of this page. For anything in the second, tell us the requirement."
            ),
        ),
    ],
    "cta_services": L(
        "/cop31-event-production/", "/cop31-exhibition-stands/", "/cop31-printing-services/",
        "/cop31-av-equipment-rental/", "/cop31-event-staff/", "/cop31-private-transfers/",
        "/cop31-last-minute-services/",
    ),
    "faqs": [
        ("When and where is COP31?",
         "COP31 takes place from 9 to 20 November 2026 in Antalya, Türkiye, at the Antalya EXPO Center."),
        ("Is DmcTurkeyPartner an official COP31 provider?",
         "No. We are an independent destination management and event services company based in Türkiye. Registration, accreditation, the official programme, the official accommodation platform and complimentary shuttle services are managed by the COP31 and UNFCCC authorities."),
        ("Can you help if we have already booked hotels and flights?",
         "Yes. Most requests reach us that way. Accommodation and travel are often already arranged, and what is missing is local execution: stand production, printing, AV, furniture, staffing, interpreters, vehicles or someone on the ground when something goes wrong."),
        ("How late can we request something during COP31?",
         "Requests during the conference itself are a normal part of the work. What can be delivered depends on local availability at that moment, so we confirm feasibility before committing rather than promising a fixed turnaround in advance."),
        ("Do you work with international agencies as a subcontracted local partner?",
         "Yes. Agencies commonly keep the client relationship, the creative direction and the programme, and use us as the Antalya execution layer. See our white-label DMC support for how that is normally structured."),
        ("Which areas around Antalya do you cover?",
         "The Antalya region, including Aksu and the venue area, Lara, Konyaaltı, Antalya city centre, Belek, Kundu, Side and Kemer."),
        ("Can you handle both a planned build and urgent items during the event?",
         "Yes, and they are usually best briefed together. Teams that give us the planned scope in advance are far easier to support when an unplanned requirement appears mid-conference."),
        ("How do we start?",
         "Send the requirement through the proposal form with COP31 selected, or message the Antalya operations desk on WhatsApp with what you need and the date you need it."),
    ],
    "related": L(
        "/cop31-antalya-participant-guide/", "/cop31-antalya-dates/", "/cop31-antalya-venue/",
        "/cop31-antalya-program/", "/cop31-antalya-registration/", "/cop31-antalya-hotels/",
        "/cop31-antalya-accommodation/", "/cop31-antalya-transport/",
        "/cop31-antalya-airport-transfer/", "/cop31-antalya-restaurants/",
        "/cop31-event-services/", "/cop31-exhibition-services/", "/cop31-exhibition-stands/",
        "/cop31-booth-builder-antalya/", "/cop31-pavilion-services/", "/cop31-event-production/",
        "/cop31-printing-services/", "/cop31-branding-signage/", "/cop31-av-equipment-rental/",
        "/cop31-furniture-rental/", "/cop31-coffee-machine-rental/", "/cop31-event-staff/",
        "/cop31-hostess-staff/", "/cop31-interpreters/", "/cop31-private-transfers/",
        "/cop31-last-minute-services/", "/cop31-rapid-response-services/",
        "/cop31-emergency-event-support/",
    ),
    "related_heading": "The Full COP31 Antalya Cluster",
    "related_lede": "Every page in this section, grouped from planning to execution to urgent support.",
}

PAGES = [HUB]
