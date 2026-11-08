# -*- coding: utf-8 -*-
"""Which COP31 pages were folded into which, and what each target now carries.

Single source of truth for the November 2026 consolidation. Used by
cop31_consolidate.py (one-off migration), cop31_build.py (so the generators
never recreate a merged page) and cop31_links.py (menus).
"""

# target slug -> [(source slug, {"sections": [h2 or (old h2, new h2), ...]})]
MERGES = {
    "cop31-antalya": [
        ("cop31-antalya-dates", {"sections": [
            ("The Dates You Actually Work To", "COP31 Dates You Actually Work To"),
            ("A Practical Booking Order", "A Practical Booking Order for COP31"),
        ]}),
        ("cop31-antalya-program", {"sections": [
            "How the COP31 Programme Is Structured",
            "What Programme Days Mean Operationally",
        ]}),
        ("cop31-antalya-registration", {"sections": [
            "Who Manages COP31 Registration",
            ("Badges and Access", "COP31 Badges and Access"),
        ]}),
    ],
    "cop31-antalya-venue": [
        ("cop31-antalya-expo-center", {"sections": [
            ("Event Logistics and Exhibitor Considerations",
             "Antalya EXPO Center: Event Logistics for Exhibitors"),
        ]}),
    ],
    "cop31-antalya-hotels": [
        ("cop31-antalya-accommodation", {"sections": [
            "What Group Accommodation Actually Involves",
            ("How We Work", "How We Place Delegations and Event Teams"),
        ]}),
    ],
    "cop31-antalya-transport": [
        ("cop31-antalya-airport-transfer", {"sections": [
            ("Routes We Cover", "Airport Transfer Routes We Cover"),
            ("Vehicle Types", "Vehicle Types and Capacities"),
            "Airport Transfer Prices",
            "Meet &amp; Greet and Group Arrivals",
        ]}),
        ("cop31-private-transfers", {"sections": [
            ("What We Provide", "Private Transfers and Vehicles with Driver"),
            "Transfer or Disposal?",
            "Daily Shuttle and Vehicle-with-Driver Prices",
        ]}),
    ],
    "cop31-antalya-participant-guide": [
        ("cop31-antalya-restaurants", {"sections": [
            "Dining Formats for a Delegation",
            "Group Dining and Private Event Options",
        ]}),
    ],
    "cop31-exhibition-services": [
        ("cop31-exhibition-stands", {"sections": [
            ("Modular or Custom?", "Exhibition Stands: Modular or Custom?"),
            "Stand Sizes and Typical Cost Ranges",
            "What a Stand Scope Includes",
            "The Timeline That Actually Governs a Stand",
        ]}),
        ("cop31-booth-builder-antalya", {"sections": [
            ("What to Send for a Quote", "What to Send for a Booth Quote"),
            "Booth Types We Build",
        ]}),
        ("cop31-pavilion-services", {"sections": [
            "Why Pavilions Are a Different Operation",
            ("What We Provide", "Pavilion Services We Provide"),
            "A Realistic Pavilion Timeline",
        ]}),
        ("cop31-furniture-rental", {"sections": [
            ("What We Rent", "Exhibition Furniture Rental"),
            ("Delivery, Placement and Collection", "Furniture Delivery, Placement and Collection"),
        ]}),
        ("cop31-coffee-machine-rental", {"sections": [
            ("What Can Be Arranged", "Coffee Stations and Stand Hospitality"),
        ]}),
        ("cop31-branding-signage", {"sections": [
            ("What We Produce and Install", "Branding and Signage We Produce and Install"),
            "Signage That Works at a Conference",
        ]}),
        ("cop31-printing-services", {"sections": [
            ("What We Print", "Event Printing and Collateral"),
            ("Turnaround", "Print Turnaround"),
        ]}),
    ],
    "cop31-event-production": [
        ("cop31-av-equipment-rental", {"sections": [
            ("Equipment We Supply", "AV Equipment We Supply"),
            ("Typical Hire Ranges", "Typical AV Hire Ranges"),
            "Specifying AV Without Over-Ordering",
            "Rental Availability During COP31",
        ]}),
    ],
    "cop31-event-staff": [
        ("cop31-hostess-staff", {"sections": [
            "Where Hostess Staff Are Used",
            "How Many Hostesses?",
            ("Briefing Makes the Difference", "Hostess Briefing Makes the Difference"),
        ]}),
        ("cop31-interpreters", {"sections": [
            ("What We Can Source", "Interpreters We Can Source"),
            "Language Availability and Rate Guidance",
            ("Choosing the Right Kind of Support", "Choosing the Right Kind of Language Support"),
        ]}),
    ],
}

MERGED_TO = {src: target for target, items in MERGES.items() for src, _ in items}

# Titles of pages whose scope widened.
RETITLE = {
    "cop31-antalya-hotels": {
        "title": "COP31 Antalya Hotels &amp; Group Accommodation 2026",
        "h1": "COP31 Antalya Hotels and Group Accommodation 2026",
    },
    "cop31-antalya-transport": {
        "title": "COP31 Antalya Transport 2026 | Airport Transfers &amp; Prices",
        "h1": "COP31 Antalya Transport, Airport Transfers and Private Vehicles",
        "description": (
            "COP31 Antalya transport: official shuttles, airport transfers, private vehicles "
            "with driver and per-vehicle prices from €70, for delegations and event teams."
        ),
    },
    "cop31-antalya-venue": {
        "title": "COP31 Venue: Antalya EXPO Center 2026 | Location &amp; Access",
        "h1": "COP31 Venue – Antalya EXPO Center Location, Access and Logistics",
    },
    "cop31-exhibition-services": {
        "title": "COP31 Exhibition Services Antalya | Stands, Pavilions &amp; Print",
        "h1": "COP31 Exhibition Services in Antalya – Stands, Pavilions, Furniture and Print",
        "description": (
            "COP31 exhibition services in Antalya: modular and custom stands, pavilions, "
            "furniture, coffee stations, branding, signage and print, built and run locally."
        ),
    },
    "cop31-event-production": {
        "title": "Event Production &amp; AV Rental Antalya | COP31 &amp; Corporate",
        "h1": "COP31 Event Production and AV Rental in Antalya",
        "description": (
            "Event production and AV rental in Antalya for COP31 side events and corporate "
            "events: staging, LED screens, sound, lighting, technicians and hire ranges."
        ),
    },
    "cop31-event-staff": {
        "title": "Event Staff Antalya | Hostesses, Interpreters &amp; Crew for COP31",
        "h1": "COP31 Event Staff in Antalya – Crew, Hostesses and Interpreters",
        "description": (
            "Event staff in Antalya for COP31 and corporate events: crew, hostesses, "
            "registration desks and interpreters, with staffing ratios and day-rate guidance."
        ),
    },
}

# "Local proof" — only facts that are published elsewhere on the site
# (Selected Works pages and the registered agency details in site_config.py).
_CONGRESS = [
    ("23rd-national-surgery-congress", "23rd National Surgery Congress", "meetings &amp; conferences, Susesi Luxury Resort, Belek"),
    ("turkiye-is-bankasi-aktob-conference", "Türkiye İş Bankası AKTOB Conference", "conference, Cosmos Theatre, Antalya"),
    ("tusas-management-summit-fayrap-2026", "TUSAŞ Management Summit — FAYRAP 2026", "corporate summit, Antalya"),
]
_CORPORATE = [
    ("turk-telekom-business-partners-meeting", "Türk Telekom Business Partners Meeting", "corporate event, Rixos Sungate, Kemer"),
    ("vakifbank-management-summit-titanic-belek", "VakıfBank Management Summit", "corporate event, Titanic Deluxe Golf Belek"),
    ("eksim-holding-management-summit", "Eksim Holding Management Summit", "corporate event, Calista Luxury Resort, Belek"),
]
_PRODUCTION = [
    ("anadolu-sigorta-100th-anniversary", "Anadolu Sigorta 100th Anniversary", "corporate event, Kremlin Palace, Antalya"),
    ("ets-holiday-concerts-rixos-sungate", "ETS Holiday Concerts", "entertainment, Rixos Sungate, Kemer"),
    ("5g-technology-event-sueno-belek", "5G Technology Event", "brand &amp; experiential, Sueno Belek"),
]
_BUILD = [
    ("555th-year-interactive-museum", "555th Year Interactive Museum", "special project, Antalya"),
    ("dosso-dossi-fashion-show", "Dosso Dossi Fashion Show", "entertainment, The Land of Legends, Belek"),
    ("5g-technology-event-sueno-belek", "5G Technology Event", "brand &amp; experiential, Sueno Belek"),
]
_STAFF = [
    ("international-artist-celebration-performance-staffing", "International Artist Celebration", "performance staffing"),
    ("23rd-national-surgery-congress", "23rd National Surgery Congress", "meetings &amp; conferences, Susesi Luxury Resort, Belek"),
    ("turkiye-is-bankasi-corporate-hospitality", "Türkiye İş Bankası Corporate Hospitality", "corporate hospitality, Antalya"),
]
_GROUPS = [
    ("vakifbank-management-summit-titanic-belek", "VakıfBank Management Summit", "corporate event, Titanic Deluxe Golf Belek"),
    ("temsa-corporate-event-calista-belek", "TEMSA Corporate Event", "corporate event, Calista Luxury Resort, Belek"),
    ("eksim-holding-management-summit", "Eksim Holding Management Summit", "corporate event, Calista Luxury Resort, Belek"),
]
_HOSPITALITY = [
    ("turkiye-is-bankasi-corporate-hospitality", "Türkiye İş Bankası Corporate Hospitality", "corporate hospitality, Antalya"),
    ("sunexpress-corporate-meeting-antalya", "SunExpress Corporate Meeting", "corporate meeting, Antalya"),
    ("mapfre-sigorta-corporate-event", "MAPFRE Sigorta Corporate Event", "brand &amp; experiential, Antalya"),
]


def _proof(heading, lede, works):
    return {"heading": heading, "lede": lede, "works": works}


PROOF = {
    "cop31-antalya": _proof(
        "Our Local Track Record in Antalya",
        "Recent conferences and corporate programmes our Antalya team delivered locally:",
        _CONGRESS + _CORPORATE[:1],
    ),
    "cop31-antalya-venue": _proof(
        "Events We Have Delivered Around Antalya",
        "Recent projects our Antalya team delivered at venues across Antalya and Belek:",
        _CONGRESS,
    ),
    "cop31-antalya-hotels": _proof(
        "Resort Programmes We Have Delivered in Belek",
        "Resort-based corporate programmes in Belek delivered by our Antalya team:",
        _GROUPS,
    ),
    "cop31-antalya-transport": _proof(
        "Resort Programmes We Have Delivered Around Antalya",
        "Resort-based corporate programmes our Antalya team delivered across the region:",
        _GROUPS,
    ),
    "cop31-antalya-participant-guide": _proof(
        "Hospitality Programmes We Have Delivered in Antalya",
        "Dinners, receptions and hosted programmes for corporate clients in Antalya:",
        _HOSPITALITY,
    ),
    "cop31-exhibition-services": _proof(
        "Special Projects Our Antalya Production Network Delivered",
        "Recent special projects and experiential events produced locally in Antalya and Belek:",
        _BUILD,
    ),
    "cop31-event-production": _proof(
        "Productions We Have Delivered in Antalya",
        "Recent corporate events and shows our Antalya production network delivered:",
        _PRODUCTION,
    ),
    "cop31-event-staff": _proof(
        "Recent Antalya Projects Our Team Delivered",
        "Recent Antalya programmes delivered by our team and local network:",
        _STAFF,
    ),
    "cop31-event-services": _proof(
        "Recent Antalya Events We Delivered",
        "Recent corporate programmes our Antalya team delivered:",
        _CORPORATE + _PRODUCTION[:1],
    ),
    "cop31-last-minute-services": _proof(
        "Why We Can Source Fast in Antalya",
        "Fast sourcing depends on a standing local network. The same Antalya production network delivered:",
        _PRODUCTION[:2] + _CONGRESS[:1],
    ),
}
