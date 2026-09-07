# -*- coding: utf-8 -*-
"""Pavilion services, transport guide and the last-minute cluster entry point."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", covering conference dates, venue and participant information alongside the full "
    "local service range."
)


PAVILION = {
    "slug": "cop31-pavilion-services",
    "breadcrumb": "Pavilion Services",
    "title": "COP31 Pavilion Services in Antalya | Country & Organisation Pavilions",
    "description": (
        "Local COP31 pavilion services in Antalya for countries, international "
        "organisations, NGOs, corporations and climate initiatives: production, branding, "
        "furniture, AV, hospitality, staffing, printing and on-site operational support."
    ),
    "h1": "COP31 Pavilion Services in Antalya",
    "answer": (
        "We deliver local pavilion support in Antalya for COP31 — production and branding, "
        "furniture, AV, coffee and hospitality, staffing, printing, transport and daily "
        "on-site operations — for countries, organisations, NGOs and initiatives operating a "
        "pavilion from 9 to 20 November 2026."
    ),
    "lede": (
        "A pavilion is not a stand that happens to be larger. It is a two-week operating space "
        "that hosts sessions, receives visitors, runs hospitality and has to still look "
        "credible on day nine. These are the local services that keep one running in Antalya."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Pavilion Services",
    "service_name": "COP31 Pavilion Services in Antalya",
    "cta_label": "Request Pavilion Support",
    "sources": ["ifp", "unfccc", "tr"],
    "sections": [
        section(
            "Why Pavilions Are a Different Operation",
            lede(
                "Exhibition stands are largely a build problem. Pavilions are a build problem "
                "followed by twelve days of hosting, and it is the second half that usually "
                "goes wrong."
            ),
            table(
                "Stand vs pavilion, operationally",
                ["", "Exhibition stand", "Pavilion"],
                [
                    ["Primary purpose", "Presence and visibility", "Hosting sessions, meetings and delegations"],
                    ["Daily activity", "Staffed, largely static", "Programmed — sessions, panels, receptions, bilaterals"],
                    ["Consumables", "Collateral and giveaways", "Collateral, catering, coffee, water, printed session material"],
                    ["Staffing", "Hosts on the stand", "Hosts, technical crew, session support, sometimes interpreters"],
                    ["Failure mode", "Something is missing at build", "Something degrades by mid-conference — supplies, tidiness, AV reliability"],
                ],
            ),
            para(
                "Planning a pavilion around the build date alone reliably produces a space that "
                "opens well and deteriorates. Planning it around the daily cycle produces one "
                "that holds."
            ),
        ),
        section(
            "What We Provide",
            cards([
                ("Pavilion production", "Structure, walls, counters, meeting areas, storage and finishing, coordinated with your design or developed from a brief."),
                ("Branding and graphics", "Fascia, wall graphics, backdrops, sponsor and partner boards, floor graphics and wayfinding — see " + A("/cop31-branding-signage/", "branding and signage") + "."),
                ("Furniture", "Seating for sessions, meeting tables, lounge areas, counters and storage furniture — see " + A("/cop31-furniture-rental/", "furniture rental") + "."),
                ("AV and technical", "Screens, sound, microphones, presentation systems, recording support and a technician for session days — see " + A("/cop31-av-equipment-rental/", "AV rental") + "."),
                ("Hospitality", "Coffee machines and stations, water, refrigeration, cups and supplies, and catering coordination — see " + A("/cop31-coffee-machine-rental/", "coffee and hospitality equipment") + "."),
                ("Staffing", "Hosts, session support, technical crew and daily reset staff — see " + A("/cop31-event-staff/", "event staff") + " and " + A("/cop31-hostess-staff/", "hostesses") + "."),
                ("Printing", "Session programmes, signage, reports, name cards and reprints during the conference — see " + A("/cop31-printing-services/", "printing services") + "."),
                ("Transport", "Speaker and delegation movement to and from the pavilion, and supply runs — see " + A("/cop31-private-transfers/", "private transfers") + "."),
                ("Daily operational support", "A local contact who resets the space, restocks supplies, chases faults and reports each day."),
            ]),
        ),
        section(
            "Who Runs Pavilions at a COP",
            plain_list([
                "National governments and country delegations.",
                "International and intergovernmental organisations.",
                "NGOs, foundations and civil-society coalitions.",
                "Corporations, industry bodies and business associations.",
                "Climate initiatives, coalitions and multi-partner programmes.",
                "Regional, city and sub-national delegations.",
                "Agencies delivering a pavilion on behalf of any of the above.",
            ]),
            para(
                "The requirement differs less by category than by programme density. A pavilion "
                "running four sessions a day needs technical crew and a reset routine; one used "
                "mainly for meetings needs furniture, quiet and coffee."
            ),
        ),
        section(
            "A Realistic Pavilion Timeline",
            steps([
                ("Brief and concept", "Space size, intended use, session programme, hospitality expectations and branding requirements."),
                ("Design and specification", "Layout, production drawings, material and graphic specification, equipment list and staffing plan."),
                ("Approvals and freeze", "Design sign-off is the real deadline — manufacturing, print and equipment reservation all sit behind it."),
                ("Production and reservation", "Build elements manufactured, graphics printed, furniture, AV and hospitality equipment reserved for the full period."),
                ("Installation", "Build during the pre-conference window, with technical testing and dressing before opening."),
                ("Twelve operating days", "Daily reset, restocking, session support, AV checks and a running list of fixes."),
                ("Dismantle", "Removal, equipment return, disposal and storage or freight coordination."),
            ]),
        ),
        section(
            "Local Delivery in Antalya",
            checklist([
                "Graphics, print and signage are produced locally, which makes reprints and corrections practical mid-conference.",
                "Furniture, AV and hospitality equipment are rented from local stock, so the constraint is what remains uncommitted for the conference fortnight — reserve early.",
                "Staffing is sourced locally; English-speaking hosts are standard, other languages depend on availability.",
                "Consumables — coffee, water, cups, printed material — are restocked from Antalya rather than shipped, which is what keeps a pavilion running past day five.",
                "Anything specified but not yet reserved should be treated as unavailable until it is confirmed for your dates.",
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-event-production/", "/cop31-branding-signage/", "/cop31-furniture-rental/",
        "/cop31-av-equipment-rental/", "/cop31-coffee-machine-rental/", "/cop31-event-staff/",
        "/cop31-printing-services/",
    ),
    "cta_heading": "Running a Pavilion at COP31 Antalya?",
    "faqs": [
        ("What are COP31 pavilion services?",
         "Local production, branding, furniture, AV, hospitality equipment, staffing, printing, transport and daily operational support for a pavilion operating throughout the conference."),
        ("Can you build a pavilion to our existing design?",
         "Yes. We can produce from your drawings and specification, or develop a build from a brief if no design exists yet."),
        ("Do you handle the daily running of the pavilion, not just the build?",
         "Yes, and it is usually the more valuable half. Daily reset, restocking, session support, AV checks and fault handling are part of the scope for teams that want it."),
        ("Can you provide coffee and hospitality inside a pavilion?",
         "We can supply coffee machines, stations, water, refrigeration and supplies subject to local availability and to the venue's own catering and hospitality rules, which take precedence."),
        ("How early should a pavilion be confirmed?",
         "The design freeze is the deadline that matters, because manufacturing, graphics and equipment reservation all follow it. Complex pavilions need meaningfully longer than a straightforward stand."),
        ("Can you support a pavilion shared by several partner organisations?",
         "Yes. Multi-partner pavilions mainly need clear ownership of the schedule and the consumables; we work to whatever governance the partners agree."),
        ("Are you affiliated with the COP31 organisers?",
         "No. We are an independent local operations provider. Pavilion allocation, venue rules and accreditation are handled by the official COP31 and UNFCCC bodies."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-exhibition-services/", "/cop31-exhibition-stands/",
        "/cop31-event-production/", "/cop31-antalya-venue/", "/cop31-antalya-expo-center/",
        "/cop31-coffee-machine-rental/", "/cop31-event-staff/", "/cop31-last-minute-services/",
    ),
}


TRANSPORT = {
    "slug": "cop31-antalya-transport",
    "breadcrumb": "Transport",
    "title": "COP31 Antalya Transport Guide 2026 | Shuttles, Airport & Venue Travel",
    "description": (
        "How transport works at COP31 Antalya 2026: official complimentary shuttles, Antalya "
        "Airport arrivals, hotel-to-venue movement, local travel options and when a dedicated "
        "vehicle makes more sense."
    ),
    "h1": "COP31 Antalya Transport Guide 2026",
    "answer": (
        "Complimentary shuttle services are expected to operate across the Antalya region "
        "during COP31, with stops at hotels listed on the official COP31 accommodation "
        "platform. Participants staying elsewhere, or working to fixed appointments, "
        "generally need their own transport."
    ),
    "lede": (
        "A practical guide to moving around Antalya during COP31 — what the official transport "
        "arrangements cover, what they do not, and how to plan movement for a delegation "
        "rather than a person."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Transport Planning",
    "service_name": "COP31 Antalya Transport Support",
    "update_sensitive": True,
    "sources": ["ifp", "unfccc", "tr", "contact"],
    "sections": [
        section(
            "Official Shuttle Services",
            lede(
                "UNFCCC has indicated that complimentary shuttle services will operate "
                "throughout the Antalya region during the conference, with shuttle stops "
                "available at hotels listed on the official COP31 accommodation platform. "
                "Routes, stops and official hotels are published through the official COP31 "
                "channels."
            ),
            para(
                "The practical consequence is worth stating plainly, because it catches teams "
                "out every year: shuttle access follows the hotel, not the badge. If your "
                "accommodation was booked outside the official platform, you may need to reach "
                "a stop under your own arrangements, or plan not to use shuttles at all."
            ),
            para(
                "Shuttle routes, timings and stop lists are official information and change. "
                "Confirm them through the official participant information and the official "
                "COP31 website rather than relying on any third-party summary, this one "
                "included. DmcTurkeyPartner does not operate official COP31 shuttles."
            ),
        ),
        section(
            "Arriving at Antalya Airport",
            lede(
                "Antalya Airport (AYT) is the arrival point for the large majority of "
                "participants, and sits on the same side of the city as the venue and most "
                "delegation accommodation."
            ),
            checklist([
                "Arrivals cluster into the days immediately before 9 November — the airport is busiest exactly when everyone needs it.",
                "Group arrivals across several flights are far easier with a meet-and-greet point and staged vehicles than with individual bookings.",
                "Teams travelling with equipment need vehicles sized for the load, not the headcount.",
                "Late-evening and early-morning arrivals are common in the pre-conference window; confirm your arrangement covers them.",
                "Departures on 20 November and the following day are similarly concentrated — book return transport at the same time as arrival.",
            ]),
            para(
                A("/cop31-antalya-airport-transfer/", "COP31 Antalya airport transfers")
                + " covers arrival and departure movement specifically."
            ),
        ),
        section(
            "Hotel-to-Venue Movement",
            table(
                "Daily movement options during COP31",
                ["Option", "Best for", "Watch out for"],
                [
                    ["Official complimentary shuttle", "Individual participants at official-platform hotels with a flexible schedule", "Fixed routes and departure times; no help with off-schedule movements"],
                    ["Taxi or ride-hailing app", "One-off journeys outside peak hours", "Availability and journey times degrade sharply at conference peaks"],
                    ["Dedicated vehicle with driver", "Delegations, executives, media crews, anything with a fixed start time", "Needs booking ahead — the local driver pool is finite for the fortnight"],
                    ["Vehicle on daily disposal", "Programmes that change during the day", "More expensive per journey, far cheaper per problem avoided"],
                    ["Coach for a group", "Moving 25+ people on a repeating pattern", "Needs a parking and set-down plan, not just a booking"],
                ],
            ),
            para(
                "The distinction that matters most is between per-journey and per-day booking. "
                "Individual transfers work until the schedule slips; a vehicle on disposal "
                "absorbs the slip. For delegations with bilaterals or press commitments, per-day "
                "is almost always the right call — see "
                + A("/cop31-private-transfers/", "COP31 private transfers") + "."
            ),
        ),
        section(
            "Local and Public Transport",
            para(
                "Antalya has a tram and municipal bus network serving the city centre and the "
                "coastal areas, and it is genuinely useful for evenings in town. It is not a "
                "realistic primary route between resort-corridor hotels and the venue for "
                "delegates working to a schedule, particularly with luggage, equipment or a "
                "fixed appointment. Treat it as an option for personal time rather than as "
                "programme transport."
            ),
        ),
        section(
            "Planning Movement for a Group",
            steps([
                ("Map the fixed points first", "Sessions, bilaterals, press moments and hosted dinners. Everything else can flex around them."),
                ("Decide the unit of booking", "Per journey for simple patterns; per day for anything that changes. Mixing the two is usually cheapest."),
                ("Size vehicles to the real load", "Delegates plus luggage plus materials, not headcount alone."),
                ("Plan the Leaders Summit window separately", "11–12 November is the hardest period for vehicles, roads and timing. Over-resource it deliberately."),
                ("Name a single coordinator", "One person on your side and one locally, rather than several people booking against each other."),
                ("Book return transport with outbound", "Departure day is as concentrated as arrival day."),
            ]),
        ),
        section(
            "Need Dedicated Transport Instead?",
            lede(
                "Where official shuttles do not fit — off-platform hotels, fixed appointments, "
                "executive movement, equipment or unsociable hours — dedicated vehicles are the "
                "practical answer."
            ),
            cards([
                ("Private Transfers", "/cop31-private-transfers/", "Chauffeured cars, vans, minibuses and coaches for delegation movement throughout the conference, including hourly disposal."),
                ("Airport Transfers", "/cop31-antalya-airport-transfer/", "Arrivals and departures at Antalya Airport, including meet-and-greet and staged group arrivals."),
                ("Event Services", "/cop31-event-services/", "Transport planned together with the rest of your programme rather than as a separate track."),
            ]),
        ),
    ],
    "cta_services": L(
        "/cop31-private-transfers/", "/cop31-antalya-airport-transfer/", "/cop31-event-services/",
        "/cop31-event-staff/", "/cop31-antalya-accommodation/", "/cop31-last-minute-services/",
    ),
    "cta_heading": "Need Dedicated Transport for COP31?",
    "faqs": [
        ("Is there a free shuttle at COP31 Antalya?",
         "UNFCCC has indicated that complimentary shuttle services will operate across the Antalya region during COP31, with stops at hotels listed on the official COP31 accommodation platform. Confirm routes and timings through the official COP31 channels."),
        ("What if our hotel is not on the official accommodation platform?",
         "Shuttle stops are tied to the official platform's hotel list, so participants staying elsewhere should plan their own transport to a stop or arrange dedicated vehicles."),
        ("Does DmcTurkeyPartner operate the official COP31 shuttles?",
         "No. We are an independent provider and have no role in the official shuttle operation. We arrange private and group transport separately."),
        ("How do we get from Antalya Airport to our hotel?",
         "Pre-booked private transfers are the most reliable option during the conference peaks, particularly for groups arriving across multiple flights."),
        ("Can you provide vehicles for the whole conference period?",
         "Yes — cars, vans, minibuses and coaches with drivers, on transfer or daily-disposal basis. The local driver pool is finite for the fortnight, so early booking matters."),
        ("Is public transport usable during COP31?",
         "Antalya's tram and bus network is useful for city-centre travel and evenings out, but it is not a practical primary route between resort-corridor hotels and the venue for delegates on a schedule."),
        ("Which days are hardest for transport?",
         "11–12 November, during the World Leaders Climate Action Summit, when delegation numbers, security measures and traffic management are all at their peak."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-participant-guide/", "/cop31-antalya-venue/",
        "/cop31-antalya-hotels/", "/cop31-antalya-dates/", "/cop31-private-transfers/",
        "/cop31-antalya-airport-transfer/", "/cop31-event-services/",
    ),
}

PAGES = [PAVILION, TRANSPORT]
