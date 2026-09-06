# -*- coding: utf-8 -*-
"""COP31 informational guides: participant guide, dates, programme, venue."""

from cop31_links import A, L
from cop31_render import (
    cards,
    checklist,
    facts,
    lede,
    para,
    plain_list,
    section,
    steps,
    table,
)

INFO_CTA = L(
    "/cop31-event-services/", "/cop31-exhibition-services/", "/cop31-printing-services/",
    "/cop31-av-equipment-rental/", "/cop31-event-staff/", "/cop31-private-transfers/",
    "/cop31-last-minute-services/",
)


# --- Participant guide -------------------------------------------------------

PARTICIPANT_GUIDE = {
    "slug": "cop31-antalya-participant-guide",
    "breadcrumb": "Participant Guide",
    "title": "COP31 Antalya Participant Guide 2026 | Practical A–Z for Attendees",
    "description": (
        "A practical COP31 Antalya participant guide: dates, venue, registration, badges, "
        "hotels, transport, dining, interpretation and local support for delegates, "
        "exhibitors and event teams."
    ),
    "h1": "COP31 Antalya Participant Guide 2026",
    "answer": (
        "COP31 runs from 9 to 20 November 2026 at the Antalya EXPO Center in Antalya, "
        "Türkiye. Registration and badges are handled by UNFCCC through its Online "
        "Registration System; accommodation, movement and local services are your own "
        "logistics to plan."
    ),
    "lede": (
        "A practical, plain-language guide to attending COP31 in Antalya — what is fixed by "
        "the official process, what you have to organise yourself, and where the usual "
        "problems come from. Written for delegates, observers, exhibitors, pavilion teams "
        "and the agencies supporting them."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Participant Support",
    "service_name": "COP31 Antalya Participant Support",
    "update_sensitive": True,
    "sources": ["ifp", "unfccc", "observers", "tr", "programme", "contact"],
    "sections": [
        section(
            "The Five Things to Settle First",
            lede(
                "Almost every COP31 planning conversation reduces to the same five items. "
                "Settle these and the rest becomes scheduling."
            ),
            steps([
                ("Accreditation",
                 "You cannot attend the formal sessions without being nominated and approved through the UNFCCC process. This is not something a travel supplier can arrange for you — see the " + A("/cop31-antalya-registration/", "registration guide") + "."),
                ("Dates on the ground",
                 "Your working dates are rarely the conference dates. Build, install and rehearsal days sit before 9 November; dismantling sits after 20 November. See the " + A("/cop31-antalya-dates/", "COP31 dates and planning timeline") + "."),
                ("Where you sleep",
                 "Hotel choice determines your daily commute and whether you can use complimentary shuttles at all. See " + A("/cop31-antalya-hotels/", "COP31 hotels") + "."),
                ("How you move",
                 "Shuttle, taxi or a dedicated vehicle. The right answer depends on group size, schedule density and how much of your day is off-site. See " + A("/cop31-antalya-transport/", "COP31 transport") + "."),
                ("What you need physically present",
                 "Printed material, stand elements, screens, furniture, staff, interpreters. Anything shipped internationally needs a fallback; anything produced locally needs a lead time."),
            ]),
        ),
        section(
            "Conference Basics",
            facts([
                ("Conference", "COP31 — 2026 UN Climate Change Conference"),
                ("Dates", "9–20 November 2026"),
                ("City", "Antalya, Türkiye"),
                ("Venue", "Antalya EXPO Center"),
                ("Host / Presidency", "Türkiye"),
                ("President of Negotiations", "Australia"),
                ("Leaders Summit", "11–12 November 2026"),
                ("Registration platform", "UNFCCC Online Registration System (ORS)"),
            ]),
            para(
                "The host-and-presidency split is unusual and occasionally causes confusion in "
                "planning documents: Türkiye hosts the conference in Antalya and shapes the "
                "public programme, while Australia presides over the formal negotiations. For "
                "operational purposes it changes nothing about where you need to be."
            ),
        ),
        section(
            "Registration, Badges and Access",
            lede(
                "Registration is run entirely by UNFCCC. Participants are nominated by their "
                "Party, observer organisation, UN body or accredited media organisation, and "
                "approved through the Online Registration System before a badge is issued."
            ),
            para(
                "In outline, the process moves through organisation registration, participant "
                "nomination, UNFCCC approval and notification of approval. Nominated delegates "
                "receive a notification from the system and are asked to confirm their personal "
                "details and upload a photograph. UNFCCC states that registration and badge "
                "issuance for duly nominated participants are free of charge — treat any offer "
                "to sell you accreditation with suspicion."
            ),
            para(
                "Nomination and confirmation deadlines differ by participant category and are "
                "published by UNFCCC. Because those dates move, this guide does not restate "
                "them as fixed: check the official participant information page before relying "
                "on any deadline. The " + A("/cop31-antalya-registration/", "registration guide")
                + " explains the categories and where each rule is published."
            ),
        ),
        section(
            "The Venue and Getting There",
            lede(
                "COP31 is held at the Antalya EXPO Center, east of Antalya city centre in the "
                "Aksu area, close to Antalya Airport. Most participants arrive through Antalya "
                "Airport (AYT) and stay along the Lara–Kundu–Belek corridor or in the city."
            ),
            para(
                "Two practical consequences follow. First, arrival is usually easy — the airport "
                "is near the venue and near much of the accommodation. Second, the corridor "
                "between the venue and the resort hotels carries the entire conference twice a "
                "day, so the difference between a 20-minute and a 60-minute journey is traffic "
                "and departure time, not distance. Build slack into anything with a fixed start."
            ),
            para(
                "The " + A("/cop31-antalya-venue/", "venue guide") + " covers location and access; "
                + A("/cop31-antalya-expo-center/", "the Antalya EXPO Center page")
                + " goes deeper on exhibitor and build considerations."
            ),
        ),
        section(
            "Accommodation",
            lede(
                "There is an official COP31 accommodation platform, and there is everything "
                "else. The distinction matters more than usual this year because shuttle access "
                "is tied to it."
            ),
            table(
                "Choosing where to stay for COP31",
                ["Area", "Character", "Practical note"],
                [
                    ["Aksu / venue area", "Closest to the EXPO Center", "Shortest commute; limited inventory, so it fills first"],
                    ["Lara / Kundu", "Large resort hotels with meeting space", "The main delegation corridor; good for groups needing meeting rooms"],
                    ["Belek", "Resort and golf hotels, larger conference facilities", "Further out; strong for large delegations that will run their own transport"],
                    ["Antalya city centre / Konyaaltı", "City hotels, restaurants, walkable", "Better for smaller teams and evening programmes; longer venue commute"],
                    ["Airport area", "Convenient for short stays", "Useful for crew and late arrivals rather than delegations"],
                ],
            ),
            para(
                "UNFCCC has indicated that complimentary shuttle services will operate in the "
                "Antalya region, with shuttle stops at hotels listed on the official COP31 "
                "accommodation platform. If you book outside that platform, plan your own "
                "transfer to the nearest stop — or plan your own vehicle. See "
                + A("/cop31-antalya-hotels/", "COP31 hotels") + " for area-by-area detail and "
                + A("/cop31-antalya-accommodation/", "group accommodation")
                + " if you are placing a delegation rather than a person."
            ),
        ),
        section(
            "Moving Around During the Conference",
            lede(
                "Three options, and most teams end up using a mix: complimentary shuttles, "
                "taxis and ride apps, and dedicated vehicles."
            ),
            table(
                "Transport options during COP31",
                ["Option", "Works well for", "Limitation"],
                [
                    ["Official complimentary shuttles", "Individual participants staying at official-platform hotels", "Fixed routes and stops; no flexibility for off-schedule movements"],
                    ["Taxi / ride apps", "Ad-hoc single journeys", "Availability and journey times degrade sharply at peak conference hours"],
                    ["Dedicated vehicle with driver", "Delegations, executives, camera crews, anything with a fixed appointment", "Needs to be booked ahead for the conference window"],
                ],
            ),
            para(
                "For arrivals, " + A("/cop31-antalya-airport-transfer/", "airport transfers")
                + " are worth pre-booking because arrival peaks are concentrated in the days "
                "before the opening. For programme movement, "
                + A("/cop31-private-transfers/", "private transfers") + " and the broader "
                + A("/cop31-antalya-transport/", "transport guide") + " cover the options."
            ),
        ),
        section(
            "Food, Dining and Evening Programmes",
            para(
                "Antalya has enough restaurant capacity for the conference, but the specific "
                "things delegations want — a private room for twenty, a quiet table for a "
                "bilateral, a venue that can hold a hundred for a side-event dinner — are "
                "finite and get booked early. If your programme includes hosted dinners, treat "
                "November restaurant capacity as a booking problem rather than a decision you "
                "make on the day. See " + A("/cop31-antalya-restaurants/", "COP31 restaurants and private dining") + "."
            ),
        ),
        section(
            "Language and Interpretation",
            para(
                "Formal UNFCCC sessions have their own official language arrangements. What "
                "delegations usually need locally is different: Turkish–English support for "
                "meetings with local suppliers, authorities or media, and consecutive "
                "interpretation for bilaterals and site visits. Those are sourced locally and "
                "should be booked ahead for the conference window — see "
                + A("/cop31-interpreters/", "COP31 interpreters and language support") + "."
            ),
        ),
        section(
            "Practical Notes for Türkiye",
            checklist([
                "Currency is the Turkish lira; cards are widely accepted, but keep some cash for taxis and small vendors.",
                "November in Antalya is mild but genuinely wet at times — the region gets rain in autumn, so plan for outdoor waiting and covered transitions.",
                "Power is 230V with European two-pin sockets; visiting production teams should confirm connector and power requirements rather than assume.",
                "Turkish mobile networks are good; a local eSIM is usually cheaper than roaming for a two-week stay.",
                "Visa requirements depend on nationality and are separate from conference accreditation — check them early, not after your badge is confirmed.",
                "Emergency number in Türkiye is 112.",
            ]),
            para(
                "None of this is conference-specific, but all of it turns up in the first week "
                "of a badly planned trip."
            ),
        ),
        section(
            "Where Things Usually Go Wrong",
            lede(
                "From the operational side, the recurring COP failures are predictable — which "
                "is the good news, because they are all preventable."
            ),
            cards([
                ("Shipping arrives late or not at all",
                 "International freight into a peak-period destination is the single most common failure. Have a local production fallback identified before you need it."),
                ("Print quantities were underestimated",
                 "Delegation material runs out by day three almost every time. Local reprinting is fast if a supplier is already briefed; see " + A("/cop31-printing-services/", "printing services") + "."),
                ("Nobody on the ground can enter the venue",
                 "Access is badge-controlled. Plan who physically carries items in, and when, rather than assuming a courier can reach your stand."),
                ("Furniture and AV assumptions",
                 "Teams assume the stand package includes chairs, screens or power. Confirm what is actually included and rent the gap — " + A("/cop31-furniture-rental/", "furniture") + " and " + A("/cop31-av-equipment-rental/", "AV") + "."),
                ("Transport planned per journey, not per day",
                 "Booking individual transfers works until the schedule slips. A vehicle on disposal for the day absorbs changes; single bookings do not."),
                ("No local contact after hours",
                 "Problems appear during build nights and early mornings. Having a briefed local contact in advance is what makes them solvable — see " + A("/cop31-emergency-event-support/", "emergency event support") + "."),
            ]),
        ),
    ],
    "cta_services": INFO_CTA,
    "cta_heading": "Need Local Support During COP31?",
    "faqs": [
        ("When is COP31 and where is it held?",
         "COP31 takes place from 9 to 20 November 2026 at the Antalya EXPO Center in Antalya, Türkiye."),
        ("Do I need a badge to attend COP31?",
         "Yes. Access to the conference requires accreditation through the UNFCCC process, where participants are nominated by their Party, observer organisation, UN body or accredited media organisation and approved through the Online Registration System."),
        ("Can DmcTurkeyPartner register me for COP31?",
         "No. Registration and accreditation are managed exclusively by UNFCCC and the official COP31 bodies. We support the local logistics around your attendance — accommodation sourcing, transport, production, staffing and equipment."),
        ("Which airport should I fly into?",
         "Antalya Airport (AYT) is the practical arrival point for COP31, and is close to both the venue and the main accommodation corridor."),
        ("Are shuttles provided between hotels and the venue?",
         "UNFCCC has indicated that complimentary shuttle services will operate in the Antalya region, with stops at hotels listed on the official COP31 accommodation platform. Participants staying elsewhere should plan their own transport to a stop, or arrange a dedicated vehicle."),
        ("What is the weather like in Antalya in November?",
         "Mild by European standards but with real rainfall — autumn is one of the wetter periods in Antalya. Plan for covered transitions and wet-weather contingency for anything outdoors."),
        ("Can we arrange printing or equipment after we arrive?",
         "Often yes, subject to local availability at the time. It is significantly faster if a supplier has already been briefed before the conference, which is why we recommend registering an urgent-support contact in advance."),
        ("We are an agency supporting a client at COP31 — can you work behind us?",
         "Yes. Agencies typically retain the client relationship and creative direction and use us as the local Antalya execution layer, including white-label delivery."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-dates/", "/cop31-antalya-venue/",
        "/cop31-antalya-registration/", "/cop31-antalya-hotels/", "/cop31-antalya-transport/",
        "/cop31-antalya-restaurants/", "/cop31-event-services/", "/cop31-printing-services/",
        "/cop31-interpreters/", "/cop31-private-transfers/", "/cop31-last-minute-services/",
    ),
}


# --- Dates -------------------------------------------------------------------

DATES = {
    "slug": "cop31-antalya-dates",
    "breadcrumb": "Dates 2026",
    "title": "COP31 Antalya Dates 2026 | 9–20 November 2026 Conference Dates",
    "description": (
        "COP31 takes place from 9 to 20 November 2026 in Antalya, Türkiye. Conference start "
        "and end dates, the Leaders Summit window, and a planning timeline for agencies, "
        "delegations and exhibitors."
    ),
    "h1": "COP31 Antalya Dates 2026",
    "answer": (
        "COP31 will take place in Antalya, Türkiye, from 9 to 20 November 2026. The World "
        "Leaders Climate Action Summit is scheduled for 11–12 November 2026."
    ),
    "lede": (
        "The conference dates are fixed, but they are not the dates most teams actually work "
        "to. This page gives the official dates, then the planning timeline that sits around "
        "them for anyone building, shipping, staffing or moving people in Antalya."
    ),
    "hero_facts": [
        ("Conference dates", "9–20 November 2026"),
        ("Duration", "12 conference days"),
        ("Leaders Summit", "11–12 November 2026"),
        ("Location", "Antalya EXPO Center, Türkiye"),
    ],
    "page_type": "informational",
    "service_interest": "COP31 Planning Support",
    "service_name": "COP31 Antalya Planning Support",
    "update_sensitive": True,
    "sources": ["unfccc", "programme", "ifp", "tr"],
    "sections": [
        section(
            "Official COP31 Dates",
            lede(
                "COP31 — the 2026 United Nations Climate Change Conference — runs from Monday "
                "9 November to Friday 20 November 2026 in Antalya, Türkiye, at the Antalya "
                "EXPO Center. Türkiye hosts the conference; Australia serves as President of "
                "Negotiations."
            ),
            table(
                "COP31 Antalya 2026 key dates",
                ["Date", "What happens"],
                [
                    ["Mon 9 November 2026", "Conference opens; first thematic day (announced as Food, Agriculture and Health)"],
                    ["Tue 10 November 2026", "Thematic day announced as Energy and Transport"],
                    ["Wed 11 November 2026", "World Leaders Climate Action Summit, day 1 (alongside the Zero Waste theme)"],
                    ["Thu 12 November 2026", "World Leaders Climate Action Summit, day 2 (alongside Resilient Cities and Built Environment)"],
                    ["Fri 13 – Thu 19 November 2026", "Remaining thematic days and negotiation programme"],
                    ["Fri 20 November 2026", "Scheduled close of the conference"],
                ],
            ),
            para(
                "The thematic day sequence is set by the COP31 Presidency and is summarised on "
                "the " + A("/cop31-antalya-program/", "COP31 programme page") + ". Because "
                "programme detail is still being published, confirm any date-specific plan "
                "against the official conference programme before committing budget to it."
            ),
        ),
        section(
            "The Dates You Actually Work To",
            lede(
                "For agencies, exhibitors and delegation teams, 9–20 November is the middle of "
                "the project, not the whole of it. The operational window is wider at both ends."
            ),
            table(
                "Working timeline around the conference",
                ["Phase", "Typical window", "What it contains"],
                [
                    ["Specification", "Now → early October 2026", "Stand and pavilion design, service scope, budget approval, supplier selection"],
                    ["Production", "Mid-October → early November 2026", "Manufacturing, print, graphics, equipment reservation, staff booking"],
                    ["Build and install", "Days immediately before 9 November", "Delivery, installation, technical setup, testing, dressing"],
                    ["Live conference", "9–20 November 2026", "Daily operation, restocking, reprints, staffing, transport, urgent fixes"],
                    ["Dismantle", "From 20 November 2026", "Breakdown, removal, storage or disposal, equipment return"],
                ],
            ),
            para(
                "Two of these compress badly if left late. Production capacity in Antalya is "
                "finite and will be shared across every exhibitor and pavilion in the same "
                "fortnight; so are vehicles, drivers and event staff. Late requests are still "
                "workable — that is what "
                + A("/cop31-last-minute-services/", "last-minute services") + " exist for — but "
                "they are workable at whatever is left, not at whatever you would have chosen."
            ),
        ),
        section(
            "A Practical Booking Order",
            steps([
                ("Accreditation first",
                 "Nothing else is worth spending on until the people you are planning for can actually get in. See " + A("/cop31-antalya-registration/", "registration") + "."),
                ("Rooms second",
                 "Antalya has large capacity, but the useful rooms — near the venue, with meeting space, in blocks — go first. See " + A("/cop31-antalya-accommodation/", "group accommodation") + "."),
                ("Vehicles third",
                 "Drivers and coaches for a two-week peak are a finite pool. Delegations that book late end up with split fleets. See " + A("/cop31-private-transfers/", "private transfers") + "."),
                ("Build and production fourth",
                 "Stands, pavilions and AV need drawings and approvals before manufacturing, so the real deadline is the design freeze, not the delivery date. See " + A("/cop31-exhibition-stands/", "exhibition stands") + "."),
                ("Staffing and print last — but not too late",
                 "Hostesses, crew and interpreters can be confirmed later than production, but the good bilingual profiles are gone first. Print can be genuinely last-minute; artwork approval usually cannot."),
            ]),
        ),
        section(
            "Why the Dates Matter Commercially",
            para(
                "COP31 is not simply a busy fortnight in Antalya — it concentrates demand for "
                "the same finite resources across the whole region at once. Hotel rates, "
                "vehicle availability, crew rates and production lead times all respond to that "
                "concentration. Teams that lock their requirements early are not just buying "
                "certainty; they are buying at a different point on the availability curve."
            ),
            para(
                "If your dates are still moving, the useful thing to lock first is the shape of "
                "the requirement — how many people, how much stand, how many vehicle days — "
                "rather than the exact schedule. That is enough to hold capacity."
            ),
        ),
        section(
            "Planning Your COP31 Operations?",
            lede(
                "The pages below cover the decisions that follow from the dates."
            ),
            cards([
                ("COP31 Hotels", "/cop31-antalya-hotels/", "Where to stay, area by area, and how hotel choice affects the daily commute."),
                ("Group Accommodation", "/cop31-antalya-accommodation/", "Room blocks, delegation placement and staff accommodation for teams rather than individuals."),
                ("COP31 Transport", "/cop31-antalya-transport/", "Official shuttles, airport arrivals and when a dedicated vehicle is the right call."),
                ("Private Transfers", "/cop31-private-transfers/", "Chauffeured vehicles and delegation movement for the conference period."),
                ("COP31 Event Services", "/cop31-event-services/", "The broad local operations scope for agencies, delegations and exhibitors."),
                ("Exhibition Services", "/cop31-exhibition-services/", "Build, graphics, furniture, AV, storage and on-site exhibitor support."),
            ]),
        ),
    ],
    "cta_services": INFO_CTA,
    "cta_heading": "Planning Your COP31 Operations?",
    "faqs": [
        ("What are the COP31 dates?",
         "COP31 runs from 9 to 20 November 2026."),
        ("Where is COP31 2026 held?",
         "In Antalya, Türkiye, at the Antalya EXPO Center."),
        ("When is the COP31 Leaders Summit?",
         "The World Leaders Climate Action Summit is scheduled for 11–12 November 2026, on the third and fourth days of the conference."),
        ("How long does COP31 last?",
         "Twelve conference days, from Monday 9 November to Friday 20 November 2026."),
        ("When should we book hotels and transport for COP31?",
         "As early as the requirement is known. Demand across Antalya is concentrated into the same fortnight, so availability rather than price is usually the binding constraint for rooms near the venue, vehicles and drivers."),
        ("When do stands and pavilions need to be finalised?",
         "The practical deadline is the design freeze rather than the delivery date, because manufacturing, graphics and approvals all sit behind it. Mid-October is a realistic outer limit for a straightforward build; complex pavilions need longer."),
        ("Can you still help if our dates are not confirmed?",
         "Yes. Send the shape of the requirement — approximate group size, stand size, vehicle days — and we can check feasibility and hold capacity while the schedule firms up."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-program/", "/cop31-antalya-participant-guide/",
        "/cop31-antalya-venue/", "/cop31-antalya-hotels/", "/cop31-antalya-transport/",
        "/cop31-event-services/", "/cop31-exhibition-stands/", "/cop31-private-transfers/",
    ),
}

PAGES = [PARTICIPANT_GUIDE, DATES]
