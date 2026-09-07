# -*- coding: utf-8 -*-
"""Accommodation cluster, registration guide, EXPO Center guide and restaurants."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", covering dates, venue, participant information and local services."
)


HOTELS = {
    "slug": "cop31-antalya-hotels",
    "breadcrumb": "Hotels",
    "title": "COP31 Antalya Hotels 2026 | Where to Stay for COP31",
    "description": (
        "Where to stay for COP31 Antalya 2026: hotels near the venue in Aksu, plus Lara, "
        "Kundu, Belek, the airport area and Antalya city centre, with the trade-off between "
        "distance, shuttle access and service."
    ),
    "h1": "COP31 Antalya Hotels – Where to Stay for COP31 2026",
    "answer": (
        "COP31 accommodation is concentrated in Aksu near the venue, the Lara and Kundu resort "
        "corridor, Belek, the airport area and Antalya city centre. Official complimentary "
        "shuttle stops are tied to hotels listed on the official COP31 accommodation platform."
    ),
    "lede": (
        "Antalya has a great deal of hotel capacity, but not all of it is useful for a "
        "conference. This is an area-by-area view of where COP31 participants actually stay "
        "and what each choice costs you in daily commute, shuttle access and meeting space."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Hotel Enquiry",
    "service_name": "COP31 Antalya Hotel Sourcing",
    "update_sensitive": True,
    "sources": ["ifp", "tr", "contact", "unfccc"],
    "sections": [
        section(
            "Official Accommodation vs Independent Booking",
            lede(
                "This distinction is the most important thing on the page, because it affects "
                "how you travel every single day."
            ),
            table(
                "Two ways to book for COP31",
                ["", "Official COP31 accommodation platform", "Independent booking or DMC sourcing"],
                [
                    ["Who runs it", "The official COP31 organisers and their appointed partner", "Hotels directly, online agents, or a local DMC such as us"],
                    ["Shuttle access", "Shuttle stops are provided at hotels on the official list", "Not covered — plan your own transport to a stop or your own vehicles"],
                    ["Best for", "Individual participants who want the simplest arrangement", "Groups, delegations, teams needing meeting space, crew and late bookers"],
                    ["Where to enquire", "The official COP31 website and its accommodation and contact channels", "Directly with us, with a written scope covering rooms and transport together"],
                ],
            ),
            para(
                "Official accommodation arrangements and enquiries should go through the "
                "official COP31 channels linked at the bottom of this page. DmcTurkeyPartner is "
                "not part of the official accommodation programme; what we do is independent "
                "hotel sourcing and group placement — see "
                + A("/cop31-antalya-accommodation/", "COP31 accommodation for delegations and event teams")
                + "."
            ),
        ),
        section(
            "Where COP31 Participants Stay",
            lede(
                "Five areas cover almost all conference accommodation. They differ less in "
                "quality than in commute and in what they can do for a group."
            ),
            cards([
                ("Aksu — the venue area", "Closest to the Antalya EXPO Center and the shortest daily commute. Inventory is limited relative to demand, so it commits earliest."),
                ("Lara &amp; Kundu", "The main resort corridor toward the city, with large hotels, meeting rooms and event space. The default choice for delegations that need to host as well as sleep."),
                ("Belek", "Resort and golf hotels east along the coast, with substantial conference facilities. Further from the venue, which suits groups running their own transport."),
                ("Antalya city centre &amp; Konyaaltı", "City hotels, walkable restaurants and evening life. Better for smaller teams and evening programmes; the longest venue commute."),
                ("Airport area", "Practical for short stays, crew, late arrivals and early departures rather than for delegation accommodation."),
                ("Side &amp; Kemer", "Further out in either direction. Viable overflow if the corridor is full, but only with dedicated transport planned from the start."),
            ]),
        ),
        section(
            "The Trade-Off That Matters",
            lede(
                "Distance is the obvious variable, but it is rarely the deciding one. Three "
                "others usually matter more."
            ),
            checklist([
                "Shuttle eligibility — a hotel on the official platform's list has a stop; one outside it does not, whatever its distance from the venue.",
                "Meeting space — a delegation that needs to host bilaterals or brief its team daily needs a hotel that can provide a room, not just beds.",
                "Concentration — splitting a delegation across two hotels doubles the transport plan and halves the coordination.",
                "Restaurant and evening access — city hotels win on walkable dining; resort hotels win on being able to host a dinner in-house.",
                "Late availability — as the fortnight approaches, the binding constraint stops being preference and becomes what is left.",
            ]),
            para(
                "Note that we do not describe any hotel as official unless it appears on the "
                "official COP31 accommodation list. Where official accommodation is concerned, "
                "the official COP31 channels are the authority."
            ),
        ),
        section(
            "Booking for a Group Rather Than a Person",
            para(
                "If you are placing more than a handful of people, the questions change "
                "entirely: room blocks, rooming lists, meeting-room access, staff accommodation "
                "at a different rate point, and transport integrated with the hotel choice "
                "rather than bolted on afterwards. That is a different job from choosing where "
                "to stay, and it has its own page — "
                + A("/cop31-antalya-accommodation/", "COP31 accommodation for delegations and event teams")
                + "."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-antalya-accommodation/", "/cop31-private-transfers/",
        "/cop31-antalya-airport-transfer/", "/cop31-event-services/",
        "/cop31-antalya-restaurants/", "/cop31-event-staff/", "/cop31-last-minute-services/",
    ),
    "cta_heading": "Need Help Placing a Group in Antalya?",
    "faqs": [
        ("Where should I stay for COP31 Antalya?",
         "Aksu is closest to the venue; Lara and Kundu form the main delegation corridor with meeting space; Belek suits large groups running their own transport; the city centre suits smaller teams and evening programmes."),
        ("Are there official COP31 hotels?",
         "There is an official COP31 accommodation platform, and complimentary shuttle stops are tied to the hotels listed on it. Official accommodation enquiries should go through the official COP31 channels."),
        ("Can we stay outside the official accommodation platform?",
         "Yes, but you should plan your own transport, since shuttle stops follow the official hotel list rather than the badge."),
        ("How far are the hotels from the COP31 venue?",
         "Aksu hotels are closest, Lara and Kundu are a short drive, Belek and the city centre are further. During the conference, journey time depends more on departure timing than on distance."),
        ("Is DmcTurkeyPartner an official COP31 accommodation provider?",
         "No. We provide independent hotel sourcing and group placement. Official accommodation arrangements are managed through the official COP31 platform and channels."),
        ("When will hotels sell out for COP31?",
         "The useful inventory — near the venue, with meeting space, available in blocks — commits well before general availability disappears. Treat it as an availability problem rather than a price problem."),
        ("Can you source hotels for a delegation?",
         "Yes. Group sourcing, room blocks, delegation placement and staff accommodation are covered on our COP31 accommodation page."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-accommodation/", "/cop31-antalya-transport/",
        "/cop31-antalya-participant-guide/", "/cop31-antalya-venue/",
        "/cop31-antalya-airport-transfer/", "/cop31-antalya-restaurants/",
        "/cop31-private-transfers/",
    ),
}


ACCOMMODATION = {
    "slug": "cop31-antalya-accommodation",
    "breadcrumb": "Group Accommodation",
    "title": "COP31 Antalya Accommodation for Delegations & Event Teams | 2026",
    "description": (
        "COP31 Antalya accommodation for groups: hotel sourcing, room blocks, delegation and "
        "agency coordination, staff accommodation, meeting rooms and transport integration "
        "for November 2026."
    ),
    "h1": "COP31 Antalya Accommodation for Delegations &amp; Event Teams",
    "answer": (
        "We provide independent group accommodation support in Antalya for COP31: hotel "
        "sourcing, room blocks, delegation and agency coordination, staff accommodation, "
        "meeting-room requirements and transport integration."
    ),
    "lede": (
        "Not “where should I stay?” but “how do I place forty people, keep them together, give "
        "them somewhere to meet, and move them to the venue every morning?” This is the "
        "operational side of accommodation."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Group Accommodation",
    "service_name": "COP31 Antalya Group Accommodation Sourcing",
    "cta_label": "Request Accommodation Support",
    "sources": ["ifp", "contact", "tr"],
    "sections": [
        section(
            "What Group Accommodation Actually Involves",
            lede(
                "Placing a group is a coordination problem more than a booking problem. The "
                "hotel is roughly a third of the work."
            ),
            cards([
                ("Group hotel sourcing", "Identifying hotels that can take your numbers, in the right area, with the facilities the group actually needs."),
                ("Room blocks", "Holding inventory as a block rather than as individual reservations that disappear one at a time."),
                ("Rooming lists and changes", "Managing names, room types, arrival and departure variation, and the inevitable late changes."),
                ("Delegation planning", "Keeping a delegation together, or deliberately splitting it by function, with the transport consequences understood."),
                ("Agency accommodation coordination", "Working behind an agency that holds the client relationship, including white-label delivery."),
                ("Staff and crew accommodation", "Different requirement, different rate point — crew working build days need proximity and early breakfast, not a sea view."),
                ("Meeting rooms", "Securing meeting and briefing space within the hotel, which is frequently the harder half of the booking."),
                ("Transport integration", "Choosing the hotel with the vehicle plan in mind rather than discovering the commute afterwards — see " + A("/cop31-private-transfers/", "private transfers") + "."),
                ("Hospitality coordination", "Welcome desks, hosted breakfasts, delegation dinners and the hotel-side arrangements around them."),
            ]),
        ),
        section(
            "How This Differs from Choosing a Hotel",
            table(
                "Individual booking vs group placement",
                ["", "Choosing where to stay", "Placing a group"],
                [
                    ["Main question", "Which hotel and which area?", "How do we hold enough of the right rooms together?"],
                    ["Constraint", "Preference and price", "Block availability, meeting space and transport"],
                    ["Failure mode", "A longer commute than expected", "A split delegation, no meeting room and a doubled transport plan"],
                    ["Timing", "Can be decided late", "Needs to be held early, with names filled in later"],
                    ["Where to read more", A("/cop31-antalya-hotels/", "COP31 hotels — where to stay"), "This page"],
                ],
            ),
        ),
        section(
            "How We Work",
            steps([
                ("Send the shape of the group", "Numbers, dates, arrival pattern, room types, meeting requirements, budget guidance and how much they need to stay together. Names are not needed yet."),
                ("Options with the trade-offs stated", "Two or three realistic options, with the commute, meeting space and transport implications of each set out rather than buried."),
                ("Hold the block", "Inventory held while the group firms up, on terms we set out in writing."),
                ("Rooming list management", "Names, room types, special requirements and changes handled as they come."),
                ("Integrate transport and hospitality", "Vehicles, arrival handling and any hosted elements planned against the final hotel choice."),
                ("On-site support", "A local contact during the conference for the accommodation-side problems that always appear."),
            ]),
        ),
        section(
            "Official Arrangements",
            para(
                "There is an official COP31 accommodation platform, and complimentary shuttle "
                "stops are tied to the hotels listed on it. If official accommodation suits "
                "your group, that route should be pursued through the official COP31 channels, "
                "and we will say so. Independent sourcing is the better answer when you need "
                "blocks, meeting space, staff accommodation at a different rate point, or "
                "hotels the official list does not cover — and it means planning your own "
                "transport, which we would do alongside the rooms."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-private-transfers/", "/cop31-antalya-airport-transfer/", "/cop31-event-services/",
        "/cop31-antalya-restaurants/", "/cop31-event-staff/", "/cop31-hostess-staff/",
        "/cop31-antalya-hotels/",
    ),
    "cta_heading": "Placing a Delegation or Team in Antalya?",
    "faqs": [
        ("Can you arrange accommodation for a COP31 delegation?",
         "Yes — group hotel sourcing, room blocks, rooming-list management, delegation placement, staff accommodation, meeting rooms and integrated transport."),
        ("How is this different from your hotels page?",
         "The hotels page answers where to stay. This page is about placing a group: holding blocks, securing meeting space, keeping people together and integrating transport."),
        ("Are you part of the official COP31 accommodation programme?",
         "No. We provide independent sourcing. Official accommodation arrangements are handled through the official COP31 platform and channels, and we will point you there when that is the better route."),
        ("Can you hold rooms before we have names?",
         "Yes. Blocks are held on the shape of the group — numbers, dates and room types — with the rooming list completed later."),
        ("Can you find meeting rooms as well as bedrooms?",
         "Yes, and it is often the harder half of the booking. Meeting space during the conference fortnight is more constrained than bedrooms."),
        ("Can you arrange separate crew accommodation?",
         "Yes. Crew and production staff usually need proximity, early breakfast and a different rate point rather than delegation-standard rooms."),
        ("Will our group get shuttle access?",
         "Only if the hotel appears on the official COP31 accommodation list. Where it does not, we plan dedicated transport alongside the accommodation so the commute is solved from the start."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-hotels/", "/cop31-antalya-transport/",
        "/cop31-private-transfers/", "/cop31-antalya-airport-transfer/",
        "/cop31-event-services/", "/cop31-antalya-restaurants/", "/cop31-event-staff/",
    ),
}

PAGES = [HOTELS, ACCOMMODATION]
