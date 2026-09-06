# -*- coding: utf-8 -*-
"""Phase 1 commercial pages: event services, exhibition services, pavilion
services and last-minute services."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This is one strand of our wider "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", which covers the conference dates, venue, participant information and the full "
    "local service range."
)


EVENT_SERVICES = {
    "slug": "cop31-event-services",
    "breadcrumb": "Event Services",
    "title": "COP31 Event Services in Antalya | Local Operations Partner 2026",
    "description": (
        "Local COP31 event services in Antalya for international agencies, delegations, "
        "exhibitors, pavilions and NGOs: side events, production, staffing, AV, printing, "
        "transport, hospitality and urgent local sourcing."
    ),
    "h1": "COP31 Event Services in Antalya",
    "answer": (
        "We provide independent local event operations in Antalya for COP31 — side events, "
        "production, venue and meeting-room sourcing, staffing, AV, printing, hospitality, "
        "transport and urgent local sourcing — for international teams working in Türkiye "
        "between 9 and 20 November 2026."
    ),
    "lede": (
        "Local event support for international agencies, delegations, companies, NGOs, "
        "pavilions and exhibitors attending COP31 Antalya. One operations desk in Antalya "
        "instead of a list of suppliers you have never worked with."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Event Services",
    "service_name": "COP31 Event Services in Antalya",
    "cta_label": "Request COP31 Event Support",
    "sources": ["ifp", "unfccc", "tr"],
    "sections": [
        section(
            "What This Covers",
            lede(
                "COP31 brings thousands of organisations to a city where most of them have no "
                "supplier relationships, no local staff and no way to solve a physical problem "
                "quickly. Our role is straightforward: be the local operations layer, so an "
                "international team can run its programme in Antalya without building a supply "
                "chain from scratch."
            ),
            cards([
                ("Side events and receptions", "Format, venue, production, catering coordination, staffing and guest movement for events held around the conference schedule."),
                ("Venue and meeting-room sourcing", "Hotel meeting rooms, private spaces and event venues across Aksu, Lara, Belek and Antalya city for briefings, bilaterals and delegation sessions."),
                ("Delegation dinners and hospitality", "Private dining, group reservations and hosted evening programmes, including the constrained Leaders Summit window."),
                ("Local production and technical", "Staging, sound, screens, lighting and crew for anything from a panel session to a full reception — see " + A("/cop31-event-production/", "event production") + "."),
                ("Staffing", "Hostesses, registration staff, crew, runners and interpreters for build days and live days — see " + A("/cop31-event-staff/", "event staff") + "."),
                ("Print, branding and signage", "Collateral, roll-ups, wayfinding, backdrops and branded environments produced locally in Antalya."),
                ("Equipment rental", "AV, furniture, hospitality and coffee equipment delivered, installed and collected on your schedule."),
                ("Transport", "Airport arrivals, hotel–venue movement, executive vehicles and coach operations across the conference period."),
                ("Urgent sourcing", "Same-period local sourcing when something is missing, damaged, delayed or simply never ordered — see " + A("/cop31-last-minute-services/", "last-minute services") + "."),
            ]),
        ),
        section(
            "Who This Is For",
            table(
                "COP31 client types and what they usually need first",
                ["Who you are", "What usually comes first"],
                [
                    ["International event agency", "A local execution partner who can quote, produce and deliver in Antalya while you keep the client and the creative"],
                    ["National or organisational delegation", "Accommodation placement, vehicles, meeting rooms, interpreters and a hosting programme"],
                    ["Pavilion owner", "Production, furniture, AV, hospitality and staffing for a two-week operating space — see " + A("/cop31-pavilion-services/", "pavilion services")],
                    ["Exhibitor", "Stand build or stand support, graphics, furniture, storage and on-site help — see " + A("/cop31-exhibition-services/", "exhibition services")],
                    ["NGO or observer organisation", "Cost-controlled print, staffing and meeting space, often decided late"],
                    ["Corporate or media team", "Vehicles, crew support, equipment rental and a fixer-style local contact"],
                ],
            ),
        ),
        section(
            "Typical Use Cases",
            cards([
                ("A side event for 120 people three days before it happens",
                 "Venue, AV, staging, staffing, signage and transport pulled together inside a compressed window, with a written scope so nothing is assumed."),
                ("A delegation of 40 across two hotels",
                 "Room block coordination, a vehicle plan that survives schedule changes, an interpreter for local meetings and a hosting contact for the fortnight."),
                ("An agency running a client presence remotely",
                 "We quote, produce and deliver locally under the agency's direction, reporting to the agency rather than the end client."),
                ("A pavilion that needs to feel finished",
                 "Furniture, coffee station, screens, branded graphics, hosts and a daily reset so it still looks right on day nine."),
                ("A press and media operation",
                 "Vehicles at unsociable hours, equipment rental, a workspace, and someone locally who can solve a problem at 06:00."),
                ("A programme that keeps changing",
                 "A single briefed local contact who absorbs changes rather than requiring a fresh brief for every adjustment."),
            ]),
        ),
        section(
            "Turnaround and Local Delivery",
            lede(
                "We work to what is genuinely available rather than to a promise. That means "
                "the honest answer to “how fast?” depends on what and when."
            ),
            checklist([
                "Planned production — stands, pavilions, custom builds — is driven by design freeze and manufacturing time, so weeks rather than days.",
                "Rental items — furniture, AV, hospitality equipment — depend on what remains uncommitted in the local pool during the conference fortnight.",
                "Print and signage are the fastest category and are often achievable within the conference period, subject to artwork being approved.",
                "Staffing depends on profile: general crew is easier to find late than a specific language combination.",
                "Vehicles during the Leaders Summit window are the hardest single item to add at short notice.",
            ]),
            para(
                "We confirm feasibility before committing, and say no where a requirement is not "
                "realistically deliverable. That is more useful to an agency under pressure than "
                "an optimistic yes."
            ),
        ),
        section(
            "How to Request COP31 Event Support",
            steps([
                ("Send what you have", "A date, a headcount, a room size, a photo, a rough scope. Incomplete is fine — it is normal at this stage."),
                ("We check local feasibility", "Availability for your dates, any constraint we can see, and anything that will not work as described."),
                ("Written scope and quotation", "What is included, what is excluded, and what depends on venue access or approvals you hold."),
                ("Confirmation and scheduling", "Production, deliveries, staffing and vehicles are locked to the operating plan."),
                ("Delivery in Antalya", "A local contact for the build period and the live conference days."),
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-event-production/", "/cop31-exhibition-services/", "/cop31-pavilion-services/",
        "/cop31-printing-services/", "/cop31-av-equipment-rental/", "/cop31-event-staff/",
        "/cop31-private-transfers/",
    ),
    "cta_heading": "Tell Us What You Need in Antalya",
    "faqs": [
        ("What event services do you provide for COP31 in Antalya?",
         "Side events and receptions, venue and meeting-room sourcing, event production, staffing, AV and furniture rental, printing and signage, hospitality equipment, transport, and urgent local sourcing during the conference period."),
        ("Are you an official COP31 supplier?",
         "No. We are an independent destination management and event services provider. Official registration, accreditation, the conference programme, the official accommodation platform and complimentary shuttles are handled by the COP31 and UNFCCC authorities."),
        ("Can you work under an international agency's direction?",
         "Yes. Agencies commonly retain the client relationship and creative direction while we deliver locally, including on a white-label basis."),
        ("How late can we brief a side event?",
         "Later than most people expect, but the constraint is venue and vehicle availability rather than our capacity. Send the requirement and we will tell you honestly whether the date is still workable."),
        ("Do you cover events outside the venue?",
         "Yes — hotel meeting rooms, restaurants, private venues and off-site locations across Aksu, Lara, Kundu, Belek and Antalya city are where most COP31 side programmes actually happen."),
        ("Can one contract cover several services?",
         "Yes, and it is usually better that way. A single scope covering production, staffing, equipment and transport avoids the coordination gaps that appear when four suppliers each deliver correctly but not together."),
        ("What information do you need to quote?",
         "Dates, location or area, headcount, format, what already exists and what is missing, and any budget guidance. Anything unknown can be flagged as unknown."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-exhibition-services/", "/cop31-pavilion-services/",
        "/cop31-event-production/", "/cop31-antalya-participant-guide/",
        "/cop31-antalya-venue/", "/cop31-last-minute-services/", "/cop31-private-transfers/",
    ),
}


EXHIBITION_SERVICES = {
    "slug": "cop31-exhibition-services",
    "breadcrumb": "Exhibition Services",
    "title": "COP31 Exhibition Services in Antalya | Exhibitor Support 2026",
    "description": (
        "Local COP31 exhibition services in Antalya: stand setup and dismantling, graphics "
        "production, furniture, AV, storage and logistics, staffing and on-site "
        "troubleshooting for exhibitors at the Antalya EXPO Center."
    ),
    "h1": "COP31 Exhibition Services in Antalya",
    "answer": (
        "We provide local exhibitor support in Antalya for COP31: setup and dismantling, "
        "locally produced graphics and print, furniture and AV rental, storage and logistics, "
        "stand staffing and on-site troubleshooting during 9–20 November 2026."
    ),
    "lede": (
        "Exhibiting at COP31 means running a physical operation in a city most exhibitors do "
        "not work in, inside a compressed build window. These are the local services that "
        "make that manageable — whether you need a full build or just the parts that did not "
        "arrive."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Exhibition Services",
    "service_name": "COP31 Exhibition Services in Antalya",
    "cta_label": "Request Exhibitor Support",
    "sources": ["ifp", "unfccc"],
    "sections": [
        section(
            "What Exhibitor Support Covers",
            lede(
                "This page is about operating an exhibition presence, not only about building "
                "one. If you want stand construction specifically, see "
                + A("/cop31-exhibition-stands/", "COP31 exhibition stands") + " or the "
                + A("/cop31-booth-builder-antalya/", "booth builder page") + "."
            ),
            cards([
                ("Setup and installation", "Local crews for build days: assembly, graphics application, furniture placement, equipment installation and finishing."),
                ("Graphics and print production", "Panels, fascia, backdrops, foam board, roll-ups, desk graphics and floor decals produced in Antalya from your artwork."),
                ("Furniture", "Counters, tables, seating, stools, lounge and meeting furniture delivered, placed and collected — see " + A("/cop31-furniture-rental/", "furniture rental") + "."),
                ("AV and technical", "Screens, monitors, sound, presentation equipment and technicians for stand demonstrations — see " + A("/cop31-av-equipment-rental/", "AV rental") + "."),
                ("Storage and logistics", "Somewhere for stock, giveaways, spare graphics, empty cases and packaging, plus movement between store and stand."),
                ("Stand staffing", "Hosts, hostesses and support crew for the live days — see " + A("/cop31-hostess-staff/", "hostess staff") + "."),
                ("On-site troubleshooting", "A local contact for the failures that appear during build nights and live mornings."),
                ("Dismantling and removal", "Breakdown, equipment return, disposal and freight coordination after the conference closes."),
            ]),
        ),
        section(
            "Who This Is For",
            plain_list([
                "Exhibitors with a confirmed space and no local supply chain in Antalya.",
                "Exhibitors whose stand is being shipped internationally and who need a local fallback.",
                "Agencies delivering an exhibition presence on behalf of a client.",
                "Organisations with a modest space that need furniture, screens and graphics rather than a build.",
                "Teams whose freight is delayed and who need to replace elements locally, quickly.",
                "Anyone who needs someone physically in Antalya during the conference fortnight.",
            ]),
        ),
        section(
            "Typical Exhibitor Situations",
            cards([
                ("The shipment is late",
                 "The most common COP problem. We identify what can be reproduced locally, what has to be rented, and what genuinely has to wait — then produce and install it."),
                ("The stand package is thinner than expected",
                 "Space-only or shell-scheme allocations often exclude furniture, power distribution, screens and lighting. We fill the gap rather than rebuild the stand."),
                ("Graphics are wrong or damaged",
                 "Reprinting locally in Antalya is usually faster than any alternative, provided approved artwork exists."),
                ("Nobody local is available for build days",
                 "We supply the crew, and a supervisor who reports to your team rather than requiring your team to supervise."),
                ("Stock runs out mid-conference",
                 "Reprint and restock during the event, with delivery timed to venue access rules."),
                ("The dismantle has no plan",
                 "Removal, return of rented items, disposal and freight collection handled as a defined scope rather than improvised on the last afternoon."),
            ]),
        ),
        section(
            "Venue Context",
            para(
                "COP31 is held at the "
                + A("/cop31-antalya-expo-center/", "Antalya EXPO Center")
                + ". Build regulations, access windows, delivery routes, rigging and power "
                "rules are issued by the venue and the conference organisers to confirmed "
                "exhibitors, and they take precedence over anything a supplier tells you. We "
                "work inside those rules; we do not publish or reinterpret them."
            ),
            para(
                "Two practical points that hold regardless of the detail: venue access is "
                "badge-controlled, so plan who carries what and when; and the build window is "
                "shared by every exhibitor at once, so late deliveries join a queue rather than "
                "simply arriving later."
            ),
        ),
        section(
            "How to Request Exhibition Support",
            steps([
                ("Send your stand details", "Space size, whether it is shell scheme or space only, what is being shipped, and what you know is missing."),
                ("Share artwork and drawings if you have them", "Print-ready artwork and a layout let us quote accurately rather than in ranges."),
                ("We confirm local feasibility", "What can be produced or rented in Antalya for your build dates, and what cannot."),
                ("Scope, quotation, schedule", "A written scope with build-day timings, delivery windows and crew allocation."),
                ("Build, live days, dismantle", "One local contact across all three phases."),
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-exhibition-stands/", "/cop31-booth-builder-antalya/", "/cop31-printing-services/",
        "/cop31-furniture-rental/", "/cop31-av-equipment-rental/", "/cop31-event-staff/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Exhibiting at COP31 Antalya?",
    "faqs": [
        ("What exhibition services do you offer for COP31?",
         "Setup and installation, locally produced graphics and print, furniture and AV rental, storage and logistics, stand staffing, on-site troubleshooting, and dismantling and removal."),
        ("Can you help if our stand is arriving from another country?",
         "Yes — that is one of the most common requests. We can install shipped elements with local crew and produce or rent replacements for anything that arrives late or damaged."),
        ("Do you build stands as well as support them?",
         "Yes. Stand construction is covered on our exhibition stands page, and the quote-driven route for teams who already know their space is the booth builder page."),
        ("Can you reprint graphics during the conference?",
         "Usually yes, subject to local capacity at the time and to having approved artwork. Print is the fastest category to replace locally."),
        ("Do you provide storage near the venue?",
         "We coordinate storage and movement between store and stand as part of the exhibitor scope. Availability is confirmed for your specific dates rather than promised in advance."),
        ("Can you supply stand staff who speak English?",
         "Yes. English-speaking hosts and hostesses are the standard request for an international conference; other language combinations depend on availability and should be requested early."),
        ("What happens after the conference closes?",
         "Dismantling, removal of your materials, return of rented equipment, disposal of what is not travelling home, and coordination with your freight forwarder."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-exhibition-stands/", "/cop31-booth-builder-antalya/",
        "/cop31-pavilion-services/", "/cop31-antalya-expo-center/", "/cop31-antalya-venue/",
        "/cop31-furniture-rental/", "/cop31-printing-services/", "/cop31-last-minute-services/",
    ),
}

PAGES = [EVENT_SERVICES, EXHIBITION_SERVICES]
