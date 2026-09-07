# -*- coding: utf-8 -*-
"""Print, branding, AV, furniture and hospitality equipment pages."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", covering participant information and the full local service range."
)


PRINTING = {
    "slug": "cop31-printing-services",
    "breadcrumb": "Printing & Collateral",
    "title": "COP31 Printing Services in Antalya | Urgent Event Printing 2026",
    "description": (
        "Local COP31 printing in Antalya: brochures, flyers, roll-ups, banners, posters, "
        "foam board, badges, stickers, decals, desk graphics, signage and event collateral, "
        "including short-notice reprints during the conference."
    ),
    "h1": "COP31 Printing Services in Antalya",
    "answer": (
        "We produce print locally in Antalya for COP31 — brochures, flyers, roll-ups, "
        "banners, posters, foam board, badges, stickers, decals, desk graphics and signage — "
        "including short-notice reprints during 9–20 November 2026."
    ),
    "lede": (
        "Print is the one thing every COP31 team runs out of, and the one thing that is "
        "fastest to replace locally. Produced in Antalya, delivered to your hotel, stand or "
        "pavilion."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Printing",
    "service_name": "COP31 Printing Services in Antalya",
    "cta_label": "Request a Print Quote",
    "wa_label": "Need Printing Today? WhatsApp Us",
    "wa_message": "COP31 Antalya — printing request. Item, quantity, size and deadline:",
    "sources": ["ifp"],
    "sections": [
        section(
            "What We Print",
            cards([
                ("Brochures and flyers", "Delegation material, programme leaflets, position papers, reports and handouts in the quantities a two-week conference actually consumes."),
                ("Roll-ups and banners", "Pull-up stands, X-banners, printed fabric and PVC banners for stands, sessions and hotel spaces."),
                ("Posters and foam board", "Mounted posters, foam board panels and lightweight display boards for pavilions and side events."),
                ("Business cards", "Standard and short-run cards, including replacements when a delegation runs out mid-conference."),
                ("Badges and lanyard cards", "Internal team badges, guest passes and event-specific identification — separate from official COP31 accreditation."),
                ("Stickers and decals", "Vinyl stickers, branded labels and applied decals for surfaces, cases and equipment."),
                ("Desk and counter graphics", "Reception counters, information desks, table branding and stand furniture graphics."),
                ("Directional and wayfinding signage", "Arrows, room signs, floor graphics and event direction — see also " + A("/cop31-branding-signage/", "branding and signage") + "."),
                ("Menus and table material", "Printed menus, place cards and table collateral for delegation dinners and receptions."),
                ("Event collateral", "Notepads, folders, certificates, name cards and the general printed matter an event generates."),
            ]),
        ),
        section(
            "Turnaround",
            lede(
                "Print is the fastest category to produce locally, but the honest answer is "
                "conditional rather than a headline number."
            ),
            table(
                "What governs print turnaround during COP31",
                ["Factor", "Effect"],
                [
                    ["Artwork status", "Approved print-ready artwork is the single biggest accelerator. Artwork still in revision is the usual bottleneck, not the press."],
                    ["Item type", "Digital short-run items are quickest; large-format, mounted and finished items take longer."],
                    ["Quantity", "Small and medium runs are fast; very large runs are scheduled work."],
                    ["Finishing", "Lamination, mounting, cutting and assembly add real time to an otherwise quick job."],
                    ["Day of the conference", "Local print capacity is progressively committed as the fortnight proceeds."],
                    ["Delivery point", "A hotel is straightforward; a badge-controlled area needs an accredited person to carry items in."],
                ],
            ),
            para(
                "We will not publish a guaranteed same-day promise, because during COP31 it "
                "would not be reliable. Send the item, quantity, size and deadline and we will "
                "confirm what is achievable for that specific job."
            ),
        ),
        section(
            "Getting Print Right for a Conference",
            checklist([
                "Over-order delegation material. Running out by day three is close to universal, and reprinting costs more than printing.",
                "Send print-ready files with bleed and outlined fonts — file problems cause more delay than production does.",
                "Decide who approves artwork before you need an urgent reprint, not during one.",
                "Keep a set of source files accessible locally, so a reprint does not depend on someone in another timezone.",
                "Plan delivery to a location you can actually receive at, and name the person who will accept it.",
                "For anything going inside a controlled venue area, confirm who carries it in and when.",
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-branding-signage/", "/cop31-exhibition-services/", "/cop31-pavilion-services/",
        "/cop31-exhibition-stands/", "/cop31-event-services/", "/cop31-last-minute-services/",
        "/cop31-emergency-event-support/",
    ),
    "cta_heading": "Need Printing for COP31 Antalya?",
    "cta_copy": (
        "Send the item, size, quantity, deadline and delivery point. For anything urgent, "
        "WhatsApp with the artwork attached is the fastest route."
    ),
    "faqs": [
        ("What can you print for COP31 in Antalya?",
         "Brochures, flyers, business cards, roll-ups, banners, posters, foam board, badges, stickers, decals, desk and counter graphics, directional signage, menus and general event collateral."),
        ("Can you print during the conference itself?",
         "Yes. Reprints and additional material during 9–20 November are one of the most common requests we handle, subject to local capacity at the time."),
        ("How fast can you print?",
         "It depends on the item, the finishing, the quantity and the day. Approved print-ready artwork is the biggest accelerator. Send the job and we will confirm what is achievable rather than promise a blanket turnaround."),
        ("What file format should we send?",
         "Print-ready PDF with bleed and outlined fonts is ideal. We will flag any file issue before production rather than after it."),
        ("Can you deliver to our stand at the venue?",
         "We deliver to the point venue access rules allow, and coordinate with your accredited team for anything that must be carried into a controlled area."),
        ("Do you print official COP31 badges?",
         "No. Conference accreditation and badges are issued by UNFCCC through the official registration process. We print internal team badges, guest passes and event-specific identification only."),
        ("Can you hold our artwork for reprints?",
         "Yes, and we recommend it. Having approved files already with us removes the slowest step from an urgent reprint."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-branding-signage/", "/cop31-exhibition-services/",
        "/cop31-pavilion-services/", "/cop31-last-minute-services/",
        "/cop31-emergency-event-support/", "/cop31-event-services/",
    ),
}


BRANDING = {
    "slug": "cop31-branding-signage",
    "breadcrumb": "Branding & Signage",
    "title": "COP31 Branding & Signage in Antalya | Wayfinding 2026",
    "description": (
        "COP31 branding and signage in Antalya: directional signs, venue dressing, wall and "
        "floor graphics, counters, desk branding, banners, sponsor boards, backdrops and "
        "wayfinding, produced and installed locally."
    ),
    "h1": "COP31 Branding &amp; Signage Services in Antalya",
    "answer": (
        "We produce and install branding and signage locally in Antalya for COP31 — "
        "directional and wayfinding signs, venue dressing, wall and floor graphics, counters, "
        "desk branding, banners, sponsor boards and backdrops."
    ),
    "lede": (
        "Signage does two jobs at a conference: it tells people where to go, and it makes a "
        "space look finished. Both are produced and installed locally in Antalya, which means "
        "corrections are possible after day one."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Branding & Signage",
    "service_name": "COP31 Branding and Signage in Antalya",
    "cta_label": "Request Signage Support",
    "sources": ["ifp"],
    "sections": [
        section(
            "What We Produce and Install",
            cards([
                ("Directional and wayfinding signage", "Arrows, room identification, floor plans and route signage for delegates who have never been in the building."),
                ("Venue and space dressing", "Turning a plain hotel room or exhibition space into something that reads as your event."),
                ("Wall graphics", "Applied vinyl, printed panels and full-wall graphics for stands, pavilions and meeting spaces."),
                ("Floor graphics", "Applied floor vinyl for direction, zoning and branding, in materials suited to heavy footfall."),
                ("Counters and desk branding", "Reception counters, information desks and branded furniture fronts."),
                ("Banners", "Fabric and PVC banners, pull-up stands, hanging banners and outdoor formats where permitted."),
                ("Sponsor and partner boards", "Multi-logo boards, partner walls and recognition panels with the layout discipline that implies."),
                ("Backdrops", "Press backdrops, panel backdrops, step-and-repeat and photo walls."),
                ("Event signage", "Session boards, schedule displays, agenda panels and information stands."),
            ]),
        ),
        section(
            "Signage That Works at a Conference",
            checklist([
                "Design for people who do not know the building — the sign that makes sense to you is often the one that does not work at 25 metres.",
                "Read distance drives size, not aesthetics. A 40mm cap height reads at a few metres; a room name across a hall does not.",
                "Contrast matters more than colour accuracy. Brand-perfect signage that is unreadable in venue lighting has failed.",
                "Confirm what can be attached to what. Venues and hotels have rules about walls, glass, floors and rigging, and they take precedence.",
                "Plan for corrections. Room changes and schedule shifts are normal, and locally produced signage can be reprinted; shipped signage cannot.",
                "Removal is part of the job. Adhesive residue and damage charges are avoidable with the right materials and the right crew.",
            ]),
        ),
        section(
            "Where Signage Is Usually Needed",
            table(
                "COP31 signage by location",
                ["Location", "Typical requirement"],
                [
                    ["Exhibition stand or booth", "Fascia, wall panels, counter fronts, product or message graphics"],
                    ["Pavilion", "Identity, session boards, partner walls, wayfinding within the space"],
                    ["Hotel meeting room", "Room identification, agenda boards, backdrops, welcome signage"],
                    ["Side-event venue", "Route signage from entrance to room, registration desk branding, backdrops"],
                    ["Delegation hotel", "Welcome desk, meeting point signage, internal direction"],
                    ["Dinner or reception", "Table signage, welcome boards, photo backdrops"],
                ],
            ),
            para(
                "Signage is usually specified alongside print and stand production rather than "
                "on its own — see " + A("/cop31-printing-services/", "printing services")
                + " and " + A("/cop31-exhibition-stands/", "exhibition stands") + "."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-printing-services/", "/cop31-exhibition-stands/", "/cop31-pavilion-services/",
        "/cop31-event-production/", "/cop31-exhibition-services/", "/cop31-last-minute-services/",
        "/cop31-event-services/",
    ),
    "cta_heading": "Need Branding or Signage in Antalya?",
    "faqs": [
        ("What signage can you produce for COP31?",
         "Directional and wayfinding signage, venue dressing, wall and floor graphics, counters and desk branding, banners, sponsor and partner boards, backdrops and session signage."),
        ("Do you install as well as produce?",
         "Yes. Production and installation are quoted together, along with removal after the event."),
        ("Can signage be changed during the conference?",
         "Yes — that is the main advantage of producing locally. Room changes, schedule shifts and corrections can be reprinted and reinstalled during the conference period."),
        ("Can you produce signage for a hotel meeting room?",
         "Yes. Hotel and off-site venues are where most COP31 side programmes happen, and they typically need more wayfinding than the organisers provide."),
        ("Are there restrictions on what can be installed?",
         "Yes, and they are set by the venue or hotel — surfaces, adhesives, rigging and outdoor placement are all governed by their rules, which take precedence over any supplier's advice."),
        ("Do you remove signage afterwards?",
         "Yes. Removal is part of the scope, using materials and methods that avoid damage or residue charges."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-printing-services/", "/cop31-exhibition-stands/",
        "/cop31-pavilion-services/", "/cop31-event-production/", "/cop31-exhibition-services/",
        "/cop31-last-minute-services/",
    ),
}


AV = {
    "slug": "cop31-av-equipment-rental",
    "breadcrumb": "AV & Equipment Rental",
    "title": "COP31 AV Equipment Rental in Antalya | Screens, Sound & Crew",
    "description": (
        "COP31 AV equipment rental in Antalya: LED screens, TVs, projectors, sound systems, "
        "microphones, lighting, presentation equipment and technicians with on-site setup, "
        "November 2026."
    ),
    "h1": "COP31 AV Equipment Rental in Antalya",
    "answer": (
        "We rent AV equipment locally in Antalya for COP31 — LED screens, monitors, "
        "projectors, sound systems, microphones, lighting and presentation equipment — with "
        "delivery, setup and technicians where required."
    ),
    "lede": (
        "Screens, sound and presentation equipment for stands, pavilions, meeting rooms and "
        "side events, delivered and set up in Antalya. Equipment only, or equipment with a "
        "technician who stays."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 AV Rental",
    "service_name": "COP31 AV Equipment Rental in Antalya",
    "cta_label": "Request AV Equipment",
    "sources": ["ifp"],
    "sections": [
        section(
            "Equipment We Supply",
            cards([
                ("LED screens and video walls", "Indoor LED for stands, pavilions and stage backdrops, sized and specified to the space and viewing distance."),
                ("Monitors and TVs", "Screens on floor stands, wall mounts or built into stand structures for looping content and demonstrations."),
                ("Projectors and projection", "Projection with screens or surfaces for meeting rooms and session spaces where LED is not warranted."),
                ("Sound systems", "PA appropriate to room size, from a single speaker for a stand to a full system for a reception."),
                ("Microphones", "Wired and wireless handhelds, lapel and headset microphones, lectern and panel table setups."),
                ("Lighting", "Stage, functional and atmospheric lighting for sessions, receptions and stand illumination."),
                ("Presentation equipment", "Switching, clickers, cabling, adapters, monitors for presenters and the connection kit that is always missing."),
                ("Laptops and playback", "Playback machines and presentation laptops where required, subject to availability."),
                ("Technicians", "Operators for the live event and crew for setup and derig — see " + A("/cop31-event-production/", "event production") + " for full production."),
                ("On-site setup", "Delivery, installation, testing and collection, scheduled around venue and hotel access windows."),
            ]),
        ),
        section(
            "Specifying AV Without Over-Ordering",
            lede(
                "AV is the category where teams most often pay for capability they never use, "
                "or discover on the morning that something obvious is missing."
            ),
            checklist([
                "Start from the room and the audience, not from an equipment list. Room size and ceiling height decide screen size and sound.",
                "Name the sources. What is being played, from what device, with what connector — most AV failures are connection failures.",
                "Decide whether you need an operator. Unattended equipment is cheaper until something needs changing mid-session.",
                "Confirm power. Screen and sound loads have to be within what the space provides, and stand power is frequently underestimated.",
                "Book for the whole period, not per day. Equipment removed and redelivered costs more than equipment left in place.",
                "Ask what the venue or hotel already provides. Paying twice for a room's built-in system is a common and avoidable cost.",
            ]),
        ),
        section(
            "Rental Availability During COP31",
            para(
                "Local AV stock is finite and is progressively committed across the conference "
                "fortnight. Standard items — monitors, small PA, handheld microphones — remain "
                "available longer than specific models, large LED and specialist equipment. If "
                "you know you will need something, reserving it early costs nothing and removes "
                "the risk entirely."
            ),
            para(
                "For equipment needed at short notice during the conference, see "
                + A("/cop31-last-minute-services/", "last-minute services") + " and "
                + A("/cop31-emergency-event-support/", "emergency event support")
                + ". We will tell you what is genuinely available rather than take an order we "
                "cannot fill."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-event-production/", "/cop31-furniture-rental/", "/cop31-exhibition-stands/",
        "/cop31-pavilion-services/", "/cop31-event-services/", "/cop31-last-minute-services/",
        "/cop31-event-staff/",
    ),
    "cta_heading": "Need AV Equipment in Antalya for COP31?",
    "faqs": [
        ("What AV equipment can we rent for COP31?",
         "LED screens and video walls, monitors and TVs, projectors, sound systems, wired and wireless microphones, lighting, presentation and switching equipment, playback machines, and technicians where required."),
        ("Do you provide a technician with the equipment?",
         "Optionally. Equipment-only rental is available for simple setups; for sessions and live events an operator is usually worth the cost."),
        ("Can you deliver and set up on our stand?",
         "Yes — delivery, installation, testing and collection are part of the rental scope, scheduled around venue access windows."),
        ("How early should we reserve AV for COP31?",
         "As early as the requirement is known. Local stock is progressively committed across the fortnight, and specific models and large LED go first."),
        ("Can you supply AV at short notice during the conference?",
         "Often yes, for standard items, subject to what remains uncommitted at that moment. We confirm availability before accepting the order."),
        ("Should we rent locally or use the venue's supplier?",
         "Check what the venue or hotel already includes first — paying twice for a built-in system is a common error. We quote the gap rather than duplicating what you already have."),
        ("Can you cover several rooms at once?",
         "Yes. Repeatable small-room kits with a technician covering multiple rooms is a standard arrangement for multi-session days."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-event-production/", "/cop31-furniture-rental/",
        "/cop31-exhibition-services/", "/cop31-pavilion-services/", "/cop31-exhibition-stands/",
        "/cop31-last-minute-services/", "/cop31-emergency-event-support/",
    ),
}

PAGES = [PRINTING, BRANDING, AV]
