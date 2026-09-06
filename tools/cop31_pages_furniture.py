# -*- coding: utf-8 -*-
"""Furniture rental, hospitality equipment and the staffing cluster."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", covering participant information and the full local service range."
)


FURNITURE = {
    "slug": "cop31-furniture-rental",
    "breadcrumb": "Furniture Rental",
    "title": "COP31 Event &amp; Exhibition Furniture Rental | Antalya 2026",
    "description": (
        "COP31 furniture rental in Antalya: tables, chairs, stools, counters, lounge and "
        "meeting furniture, exhibition and hospitality furniture, delivered, installed and "
        "collected for November 2026."
    ),
    "h1": "COP31 Event &amp; Exhibition Furniture Rental",
    "answer": (
        "We rent event and exhibition furniture in Antalya for COP31 — tables, chairs, "
        "stools, counters, lounge, meeting, exhibition and hospitality furniture — with "
        "delivery, placement and collection across the conference period."
    ),
    "lede": (
        "The furniture nobody budgets for and everybody needs. Stand counters, meeting tables, "
        "seating for a session, lounge pieces for a pavilion — delivered, placed and collected "
        "in Antalya."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Furniture Rental",
    "service_name": "COP31 Furniture Rental in Antalya",
    "cta_label": "Request Furniture",
    "sources": ["ifp"],
    "sections": [
        section(
            "What We Rent",
            cards([
                ("Tables", "Meeting tables, cocktail and poseur tables, display tables and working tables in the sizes a stand actually fits."),
                ("Chairs", "Conference, meeting, visitor and stacking chairs for stands, sessions and hospitality areas."),
                ("Stools", "Bar and counter stools for stand counters, coffee points and informal meeting positions."),
                ("Counters", "Reception, information and demonstration counters, brandable with graphics — see " + A("/cop31-branding-signage/", "branding and signage") + "."),
                ("Lounge furniture", "Sofas, armchairs, low tables and soft seating for pavilion lounges and delegation meeting areas."),
                ("Meeting furniture", "Boardroom and meeting sets for private discussions inside a stand, pavilion or hotel room."),
                ("Exhibition furniture", "Display plinths, shelving, brochure stands, literature racks and storage units."),
                ("Hospitality furniture", "Buffet and service tables, coffee-point furniture and standing areas — see " + A("/cop31-coffee-machine-rental/", "coffee and hospitality equipment") + "."),
            ]),
        ),
        section(
            "How Much Furniture Do You Actually Need?",
            lede(
                "The two recurring errors are opposite: renting a full set for a stand that "
                "needs three pieces, and renting nothing because the space was assumed to "
                "include it."
            ),
            table(
                "A working starting point by space type",
                ["Space", "Usually needs", "Often forgotten"],
                [
                    ["Small stand (up to ~12 m²)", "A counter, two stools, a literature stand", "Somewhere to put bags and stock"],
                    ["Medium stand", "Counter, seating group, display plinths, storage", "Storage furniture; stock ends up on the floor"],
                    ["Meeting-focused stand", "Enclosed table and four chairs, storage", "A second table — one is always occupied"],
                    ["Pavilion", "Session seating, lounge area, meeting set, counters, storage", "Enough seating for the busiest session, not the average one"],
                    ["Hotel meeting room", "Whatever the hotel does not include", "Confirm the hotel's inclusions before renting anything"],
                    ["Reception or dinner", "Poseur tables, service tables, some seating", "Seating for people who cannot stand for three hours"],
                ],
            ),
            para(
                "We quote against the space and its use rather than a package, so you can see "
                "and adjust each line."
            ),
        ),
        section(
            "Delivery, Placement and Collection",
            checklist([
                "Delivery is scheduled to the venue's or hotel's access windows, not to a convenient hour.",
                "Placement is included — furniture is positioned to your layout rather than left in a stack.",
                "Additional pieces can usually be added during the conference, subject to remaining local stock.",
                "Collection happens after the conference closes, coordinated with your dismantle schedule.",
                "Damage and loss are assessed against the rental agreement; expect a straightforward written condition note rather than a surprise later.",
                "Book for the whole period rather than day by day — repeated delivery and collection costs more than leaving items in place.",
            ]),
            para(
                "Furniture is one of the most common last-minute requests during a conference, "
                "and one of the more likely to be available — see "
                + A("/cop31-last-minute-services/", "last-minute services") + "."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-exhibition-stands/", "/cop31-pavilion-services/", "/cop31-av-equipment-rental/",
        "/cop31-coffee-machine-rental/", "/cop31-exhibition-services/", "/cop31-event-services/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Need Furniture in Antalya for COP31?",
    "faqs": [
        ("What furniture can we rent for COP31?",
         "Meeting and display tables, conference and visitor chairs, bar and counter stools, reception and demonstration counters, lounge furniture, meeting sets, exhibition display furniture and hospitality furniture."),
        ("Do you deliver and set the furniture up?",
         "Yes. Delivery, placement to your layout and collection after the conference are part of the rental scope."),
        ("Can we add furniture during the conference?",
         "Usually yes, subject to what remains uncommitted in local stock. Extra chairs and tables are among the more commonly available last-minute items."),
        ("Should we rent for the whole period or day by day?",
         "For the whole period. Repeated delivery and collection costs more than leaving the furniture in place, and adds a failure point each time."),
        ("Does our stand package already include furniture?",
         "Frequently not, or not as much as assumed. Confirm exactly what the shell scheme or space allocation includes before renting, so you fill the gap rather than duplicating."),
        ("Can counters be branded?",
         "Yes. Counter fronts and display furniture can carry printed graphics produced alongside the rest of your signage."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-exhibition-stands/", "/cop31-pavilion-services/",
        "/cop31-av-equipment-rental/", "/cop31-coffee-machine-rental/",
        "/cop31-exhibition-services/", "/cop31-last-minute-services/",
    ),
}


COFFEE = {
    "slug": "cop31-coffee-machine-rental",
    "breadcrumb": "Coffee &amp; Hospitality",
    "title": "COP31 Coffee Machine &amp; Coffee Station Rental | Antalya 2026",
    "description": (
        "COP31 coffee machine and coffee station rental in Antalya: machines, stations, "
        "barista service, cups and supplies, water stations, refrigerators and hospitality "
        "equipment for stands and pavilions."
    ),
    "h1": "COP31 Coffee Machine &amp; Coffee Station Rental",
    "answer": (
        "We rent coffee machines, coffee stations, water stations, refrigeration and "
        "hospitality equipment in Antalya for COP31 stands, pavilions and delegation spaces, "
        "with supplies and barista service subject to availability."
    ),
    "lede": (
        "A working coffee point is the most reliable way to keep people in a stand or pavilion "
        "for more than ninety seconds. Machines, stations, supplies and service, arranged "
        "locally in Antalya."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Coffee &amp; Hospitality Equipment",
    "service_name": "COP31 Coffee and Hospitality Equipment Rental in Antalya",
    "cta_label": "Request Hospitality Equipment",
    "sources": ["ifp"],
    "sections": [
        section(
            "What Can Be Arranged",
            lede(
                "Availability of specific machines, supplies and staff is confirmed for your "
                "dates rather than promised in advance — local hospitality stock is finite "
                "during the conference fortnight."
            ),
            cards([
                ("Coffee machines", "Automatic and semi-automatic machines sized to the expected footfall rather than to the space available."),
                ("Coffee stations", "A complete point: machine, counter, supplies, waste and the layout that keeps a queue from blocking your stand."),
                ("Barista service", "Trained staff operating the station during peak hours, subject to availability."),
                ("Cups and supplies", "Cups, lids, stirrers, sugar, milk and the consumables that run out on day two if nobody owns them."),
                ("Water stations", "Dispensers and bottled water for stands, pavilions and meeting areas."),
                ("Refrigeration", "Under-counter and upright fridges for drinks, milk and catering items."),
                ("Hospitality equipment", "Service tables, trays, waste units and the counter furniture a service point needs — see " + A("/cop31-furniture-rental/", "furniture rental") + "."),
            ]),
        ),
        section(
            "Planning a Coffee Point That Works",
            checklist([
                "Size the machine to peak footfall, not average. A queue that forms during a session break is what people remember.",
                "Confirm power and water before specifying — stand power is routinely underestimated, and plumbed machines need a supply.",
                "Decide who restocks. A station with nobody responsible for supplies stops working by mid-conference.",
                "Plan waste. Cups accumulate faster than anyone expects and a full bin undoes the impression instantly.",
                "Check the venue's rules. Catering, hospitality and beverage service inside a venue are governed by the venue's own regulations, which take precedence.",
                "Position the station so the queue runs along your space rather than across the aisle.",
            ]),
        ),
        section(
            "Where This Fits",
            table(
                "Hospitality equipment by space",
                ["Space", "Typical setup"],
                [
                    ["Exhibition stand", "One machine, counter, supplies, small fridge, waste"],
                    ["Pavilion", "Full station with barista at peaks, water, refrigeration, restocking routine"],
                    ["Delegation meeting room", "Machine or served coffee, water, refrigeration for a small group"],
                    ["Side event or reception", "Usually catered rather than equipment-based; coordinated with the venue"],
                    ["Team back-of-house", "A simple machine and fridge for staff working long build and live days"],
                ],
            ),
            para(
                "For pavilions, hospitality is best planned alongside furniture, staffing and "
                "the daily reset routine rather than as an isolated rental — see "
                + A("/cop31-pavilion-services/", "pavilion services") + "."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-pavilion-services/", "/cop31-furniture-rental/", "/cop31-event-staff/",
        "/cop31-exhibition-services/", "/cop31-event-services/", "/cop31-last-minute-services/",
        "/cop31-branding-signage/",
    ),
    "cta_heading": "Need a Coffee Station for Your COP31 Space?",
    "faqs": [
        ("Can we rent a coffee machine for our COP31 stand?",
         "Yes, subject to availability for your dates. Machines, counters, supplies, water stations and refrigeration can be arranged as a complete coffee point."),
        ("Do you provide baristas?",
         "Barista service can be arranged subject to staff availability during the conference period. For high-footfall pavilions it is usually worth it at peak hours."),
        ("Are supplies included?",
         "Cups, lids, stirrers, sugar, milk and coffee can be included and restocked. We recommend agreeing who owns restocking before the conference starts."),
        ("What power and water do we need?",
         "It depends on the machine. Confirm your stand's available power and whether a water supply exists before specifying, since both are commonly underestimated."),
        ("Are there venue restrictions on serving coffee?",
         "Yes. Catering, hospitality and beverage service inside a venue are governed by the venue's own rules, which take precedence over any rental arrangement."),
        ("Can you deliver hospitality equipment at short notice?",
         "Sometimes, depending on what remains available locally at that point in the conference. We confirm before accepting rather than promise in advance."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-pavilion-services/", "/cop31-furniture-rental/",
        "/cop31-event-services/", "/cop31-exhibition-services/", "/cop31-event-staff/",
        "/cop31-last-minute-services/",
    ),
}

PAGES = [FURNITURE, COFFEE]
