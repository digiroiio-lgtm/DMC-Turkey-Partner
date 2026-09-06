# -*- coding: utf-8 -*-
"""Stand construction cluster: exhibition stands, booth builder, event production."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page sits within the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", which covers conference dates, venue information and the full local service range."
)


STANDS = {
    "slug": "cop31-exhibition-stands",
    "breadcrumb": "Exhibition Stands",
    "title": "COP31 Exhibition Stands in Antalya | Modular &amp; Custom Stand Build 2026",
    "description": (
        "Modular and custom COP31 exhibition stands built in Antalya: design production, "
        "graphics, furniture, AV, installation, on-site support and dismantling for the "
        "Antalya EXPO Center, November 2026."
    ),
    "h1": "COP31 Exhibition Stands in Antalya",
    "answer": (
        "We produce modular, custom and branded exhibition stands locally in Antalya for "
        "COP31, including graphics, furniture, AV integration, installation, on-site support "
        "and dismantling across 9–20 November 2026."
    ),
    "lede": (
        "Stand production delivered from Antalya rather than shipped into it. Modular systems "
        "for straightforward spaces, custom builds where the space has to do more, and the "
        "graphics, furniture and AV that turn a structure into a working stand."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Exhibition Stand",
    "service_name": "COP31 Exhibition Stand Construction in Antalya",
    "cta_label": "Request a Stand Quote",
    "wa_message": "COP31 Antalya — exhibition stand enquiry. Our space size and dates are:",
    "sources": ["ifp"],
    "sections": [
        section(
            "Modular or Custom?",
            lede(
                "The first decision, and the one that determines cost, lead time and how much "
                "the design can change later."
            ),
            table(
                "Choosing a stand approach for COP31",
                ["", "Modular system", "Custom build"],
                [
                    ["Best for", "Straightforward spaces up to medium size, standard shapes", "Distinctive spaces, unusual footprints, heavy branding or built-in features"],
                    ["Lead time", "Shorter — the system exists, the graphics are new", "Longer — drawings, approvals and manufacturing"],
                    ["Cost profile", "Lower and more predictable", "Higher, driven by materials and complexity"],
                    ["Flexibility late on", "High — panels and graphics can be adjusted", "Low after the design freeze"],
                    ["Reuse", "System reused; graphics replaced", "Usually a one-off unless designed for reuse"],
                ],
            ),
            para(
                "For a conference like COP31, where many exhibitors are working to a fixed "
                "budget and a compressed timeline, modular covers more requirements well than "
                "people expect. Custom earns its cost where the stand has a job beyond presence "
                "— hosting sessions, demonstrating equipment, or carrying a strong brand system."
            ),
        ),
        section(
            "What a Stand Scope Includes",
            cards([
                ("Structure and build", "Walls, fascia, storage rooms, counters, raised areas and meeting spaces, produced and assembled locally."),
                ("Graphics", "Printed panels, fascia branding, backdrops, floor graphics and applied vinyl from your artwork."),
                ("Furniture", "Counters, seating, tables, stools and display furniture — see " + A("/cop31-furniture-rental/", "furniture rental") + "."),
                ("Lighting and power", "Stand lighting and power distribution planned to the venue's rules rather than assumed."),
                ("AV integration", "Screens, mounts, sound and presentation equipment built into the structure — see " + A("/cop31-av-equipment-rental/", "AV rental") + "."),
                ("Installation", "Delivery and build during the pre-conference window, with testing and finishing before opening."),
                ("On-site support", "A local contact across the live days for adjustments, faults and restocking."),
                ("Dismantling", "Breakdown, removal, equipment return and disposal after the conference closes."),
            ]),
        ),
        section(
            "The Timeline That Actually Governs a Stand",
            steps([
                ("Brief", "Space size and type, whether it is shell scheme or space only, intended use, brand assets and budget range."),
                ("Concept and layout", "A workable layout for the footprint, with visuals sufficient to approve direction."),
                ("Design freeze", "The real deadline. Manufacturing, graphics production and venue approvals all sit behind this date, not behind the delivery date."),
                ("Production", "Structure manufactured, graphics printed, furniture and AV reserved for the full conference period."),
                ("Installation", "Build during the pre-conference window, to the venue's access schedule."),
                ("Live and dismantle", "Daily support through the conference, then breakdown and removal."),
            ]),
            para(
                "Exhibitors regularly plan backwards from 9 November and discover the freeze "
                "date has already passed. If your design is not yet fixed, tell us — a modular "
                "route often remains viable long after a custom one has closed."
            ),
        ),
        section(
            "Why Build Locally for COP31",
            checklist([
                "Freight into a peak-demand destination is the most common single point of failure at a COP — local production removes it.",
                "Graphics can be corrected or reprinted during the conference, which is impossible with shipped panels.",
                "Local build avoids customs, transit damage and the storage problem of shipping crates you then have to keep for two weeks.",
                "Installation crews are already in Antalya and are not dependent on travel schedules.",
                "Anything that fails during the conference can be replaced from the same local supply chain that built it.",
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-booth-builder-antalya/", "/cop31-exhibition-services/", "/cop31-branding-signage/",
        "/cop31-furniture-rental/", "/cop31-av-equipment-rental/", "/cop31-printing-services/",
        "/cop31-event-staff/",
    ),
    "cta_heading": "Need a Stand Built in Antalya for COP31?",
    "faqs": [
        ("Do you build custom exhibition stands for COP31?",
         "Yes — modular systems, custom builds and branded stands, all produced locally in Antalya with graphics, furniture, AV, installation and dismantling."),
        ("What do you need to quote a stand?",
         "Space size and shape, whether it is shell scheme or space only, intended use, brand assets and any budget guidance. A floor plan speeds things up considerably."),
        ("How late can we order a stand for COP31?",
         "It depends on the route. Custom builds need drawings, approvals and manufacturing time; modular systems remain viable much later. Send your dates and we will tell you what is still realistic."),
        ("Is a locally built stand cheaper than shipping ours?",
         "Usually, once freight, customs, transit insurance, crate storage and the risk of delay are counted. It is also far easier to fix mid-conference."),
        ("Do you handle installation and dismantling?",
         "Yes. Build, on-site support during the live days, and breakdown and removal after the conference are all part of the scope."),
        ("Can you work from our existing stand design?",
         "Yes. We can produce from your drawings and specification, or adapt a design to what is practical to build and approve in Antalya."),
        ("Does the stand price include furniture and screens?",
         "Only if specified. Furniture, AV and lighting are quoted as named line items rather than assumed, so you can see exactly what is included."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-booth-builder-antalya/", "/cop31-exhibition-services/",
        "/cop31-pavilion-services/", "/cop31-antalya-expo-center/", "/cop31-antalya-venue/",
        "/cop31-furniture-rental/", "/cop31-branding-signage/", "/cop31-last-minute-services/",
    ),
}


BOOTH = {
    "slug": "cop31-booth-builder-antalya",
    "breadcrumb": "Booth Builder",
    "title": "COP31 Booth Builder in Antalya | Local Exhibition Booth Supplier 2026",
    "description": (
        "Local COP31 booth builder in Antalya. Modular and custom exhibition booths with "
        "graphics, furniture, AV, installation and dismantling. Send your booth size and "
        "dates for a quote."
    ),
    "h1": "COP31 Booth Builder in Antalya",
    "answer": (
        "We are a local exhibition booth builder in Antalya, producing modular and custom "
        "booths for COP31 with graphics, furniture, AV, installation, on-site support and "
        "dismantling. Send your booth size and dates for a quote."
    ),
    "lede": (
        "If you already know your booth size and your dates, this is the fastest route to a "
        "number. Local production in Antalya, one point of contact, and a written scope that "
        "shows exactly what is included."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Booth Build",
    "service_name": "COP31 Booth Builder in Antalya",
    "cta_label": "Request a Booth Quote",
    "wa_message": "COP31 Antalya booth quote request. Booth size, dates and requirements:",
    "sources": ["ifp"],
    "sections": [
        section(
            "What to Send for a Quote",
            lede(
                "Six lines is usually enough for a real number rather than a range. Anything "
                "you do not know yet, mark as unknown — it is more useful than a guess."
            ),
            checklist([
                "Booth size in metres and whether it is shell scheme or space only.",
                "Open sides — corner, peninsula, island or single frontage.",
                "What the booth has to do: display, meetings, demonstrations, hospitality, or a mix.",
                "Whether you need furniture, screens, lighting and storage, or only the structure.",
                "Your build and dismantle dates, and the conference days you are operating.",
                "Brand assets, artwork status, and any budget guidance you can share.",
            ]),
            para(
                "Send it through the quote form or on WhatsApp with a photo of the floor plan. "
                "We come back with a written scope: what is included, what is excluded, and "
                "what depends on venue approvals you hold."
            ),
        ),
        section(
            "What You Get",
            cards([
                ("Local manufacturing", "The booth is built in Antalya, not shipped to it — no freight, customs or transit-damage exposure."),
                ("One contact", "Structure, graphics, furniture, AV and crew under a single scope rather than five suppliers to coordinate."),
                ("Written inclusions", "Furniture, screens, lighting and power appear as named line items, so nothing is assumed on either side."),
                ("Installation and testing", "Built and finished during the pre-conference window, tested before opening rather than on the first morning."),
                ("Live-day support", "A local contact during the conference for adjustments, faults, restocking and reprints."),
                ("Dismantle included", "Breakdown, removal, equipment return and disposal quoted up front rather than negotiated on the last day."),
            ]),
        ),
        section(
            "Booth Types We Build",
            table(
                "Common COP31 booth requirements",
                ["Type", "Typical use", "Notes"],
                [
                    ["Shell-scheme upgrade", "Small exhibitors with an allocated shell", "Graphics, furniture, lighting and screens added to the supplied structure"],
                    ["Modular booth", "Standard footprints, straightforward layouts", "Fastest route; system structure with fully custom graphics"],
                    ["Custom booth", "Distinctive brand presence or unusual footprint", "Needs drawings, approvals and a longer lead time"],
                    ["Meeting-focused booth", "Delegations and B2B programmes", "Enclosed or semi-enclosed meeting space, storage, seating"],
                    ["Demonstration booth", "Technology and equipment exhibitors", "Power, screens, technical crew and equipment integration"],
                ],
            ),
            para(
                "If your requirement extends beyond a booth into a two-week hosting space, the "
                + A("/cop31-pavilion-services/", "pavilion services page")
                + " is the better fit. For build support around a booth you already have, see "
                + A("/cop31-exhibition-services/", "exhibition services") + "."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-exhibition-stands/", "/cop31-exhibition-services/", "/cop31-furniture-rental/",
        "/cop31-av-equipment-rental/", "/cop31-branding-signage/", "/cop31-printing-services/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Send Your Booth Size and Dates",
    "cta_copy": (
        "Six lines is enough to quote from: size, open sides, what the booth has to do, what "
        "you need included, your build dates and your artwork status."
    ),
    "faqs": [
        ("Are you a booth builder in Antalya?",
         "Yes. We produce modular and custom exhibition booths locally in Antalya, including graphics, furniture, AV, installation, on-site support and dismantling."),
        ("How do I get a booth quote for COP31?",
         "Send your booth size, whether it is shell scheme or space only, the number of open sides, what the booth needs to do, your build dates and your artwork status. That is enough for a written scope and price."),
        ("How much does a COP31 booth cost?",
         "It depends on size, whether it is modular or custom, and how much furniture, AV and lighting is included. We quote against a written scope rather than publishing a headline figure that would not survive contact with your actual requirement."),
        ("Can you upgrade a shell-scheme booth?",
         "Yes. Graphics, furniture, lighting, screens and storage added to a supplied shell is one of the most common requests, and one of the fastest to deliver."),
        ("What is the latest we can order?",
         "Modular booths remain viable considerably later than custom ones. Send your dates and we will tell you honestly what is still achievable rather than take an order we cannot deliver."),
        ("Do you handle dismantling as well?",
         "Yes, and it is quoted up front. Breakdown, removal, rented-equipment return and disposal are included in the scope rather than negotiated at the end."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-exhibition-stands/", "/cop31-exhibition-services/",
        "/cop31-pavilion-services/", "/cop31-antalya-expo-center/", "/cop31-furniture-rental/",
        "/cop31-av-equipment-rental/", "/cop31-branding-signage/",
    ),
}


PRODUCTION = {
    "slug": "cop31-event-production",
    "breadcrumb": "Event Production",
    "title": "COP31 Event Production in Antalya | Staging, Sound &amp; Crew",
    "description": (
        "COP31 event production in Antalya: staging, sound, screens, lighting, technical "
        "crew, setup and on-site operations for side events, receptions, briefings, "
        "conferences and breakout sessions."
    ),
    "h1": "COP31 Event Production Services in Antalya",
    "answer": (
        "We deliver local event production in Antalya for COP31 side events, receptions, "
        "briefings and sessions — staging, sound, screens, lighting, technical crew, setup "
        "and on-site operations across 9–20 November 2026."
    ),
    "lede": (
        "Technical production for everything that happens around the conference: side events, "
        "panels, press moments, receptions and delegation sessions, delivered by crew who are "
        "already in Antalya."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Event Production",
    "service_name": "COP31 Event Production in Antalya",
    "cta_label": "Request Production Support",
    "sources": ["ifp"],
    "sections": [
        section(
            "What We Produce",
            cards([
                ("Staging and set", "Stages, risers, backdrops, lecterns, panel setups and presentation areas sized to the room rather than to a catalogue."),
                ("Sound", "PA, mixing, wired and wireless microphones, panel and lectern setups, playback and recording feeds."),
                ("Screens and projection", "LED walls, monitors, projection and presentation switching for panels, keynotes and demonstrations."),
                ("Lighting", "Stage, functional and atmospheric lighting for sessions and receptions."),
                ("Technical crew", "Sound engineers, screen operators, lighting technicians and stage crew for setup, live and derig."),
                ("Setup and derig", "Load-in, build, testing, rehearsal support and breakdown scheduled around the venue's access windows."),
                ("Event coordination", "Running order, cue management, speaker handling and on-site coordination during the event."),
                ("Recording and streaming support", "Capture and feed provision where required, coordinated with your own media team."),
            ]),
        ),
        section(
            "Formats We Support",
            table(
                "COP31 event formats and what they typically need",
                ["Format", "Typical production scope"],
                [
                    ["Side event or panel", "Sound, microphones, a screen, basic lighting, an operator"],
                    ["Press briefing", "Clean audio, a branded backdrop, a media feed, tight timing"],
                    ["Reception", "Sound and lighting for a room, a microphone for remarks, atmosphere over technicality"],
                    ["Conference or multi-session day", "Full staging, screen switching, multiple microphone setups, crew across the day"],
                    ["Breakout sessions", "Repeatable small-room kits and a technician covering several rooms"],
                    ["Gala or hosted dinner", "Room lighting, sound for speeches, staging for awards or presentations"],
                ],
            ),
            para(
                "Most COP31 production requests are the first three, run in hotel meeting rooms "
                "along the Lara and Belek corridor rather than at the venue itself. That is "
                "usually good news: hotel rooms are easier to load into and easier to schedule."
            ),
        ),
        section(
            "How Production Is Planned",
            steps([
                ("Format and room", "What the event is, how many people, in what room. Room dimensions and ceiling height change the answer more than the guest count does."),
                ("Technical scope", "Sound, screens, lighting and staging specified to the format rather than over-specified to be safe."),
                ("Schedule", "Load-in, build, testing, rehearsal, live and derig, fitted to the venue's access windows."),
                ("Crew plan", "Who is on site, when, and what each person covers."),
                ("Delivery", "Setup, testing before doors rather than on the hour, and crew present throughout the live event."),
            ]),
            para(
                "Production is usually planned alongside the rest of the programme rather than "
                "on its own — see " + A("/cop31-event-services/", "COP31 event services")
                + " for the combined scope, and " + A("/cop31-av-equipment-rental/", "AV rental")
                + " if you need equipment without crew."
            ),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-event-services/", "/cop31-av-equipment-rental/", "/cop31-furniture-rental/",
        "/cop31-branding-signage/", "/cop31-event-staff/", "/cop31-interpreters/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Producing an Event Around COP31?",
    "faqs": [
        ("What event production do you provide for COP31?",
         "Staging, sound, screens and projection, lighting, technical crew, setup and derig, and on-site event coordination for side events, briefings, receptions, conferences and breakout sessions."),
        ("Can you produce events at hotels rather than the venue?",
         "Yes — most COP31 side programmes run in hotel meeting rooms and private venues across Lara, Kundu, Belek and Antalya city, and those are generally easier to schedule than venue spaces."),
        ("Do you provide crew as well as equipment?",
         "Yes. Sound engineers, screen operators, lighting technicians and stage crew are quoted as part of the production scope. Equipment-only rental is also available."),
        ("How much notice do you need for a side event?",
         "Less than most people assume, but the binding constraint is room and crew availability during the conference fortnight rather than our capacity. Send the date and we will tell you what is still possible."),
        ("Can you support recording or streaming?",
         "We can provide capture and feed support and coordinate with your own media team. Full broadcast production is scoped separately."),
        ("Can production be combined with staffing and transport?",
         "Yes, and it usually should be. A single scope covering production, staffing and guest movement avoids the gaps that appear when separate suppliers each deliver correctly but not together."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-event-services/", "/cop31-av-equipment-rental/",
        "/cop31-pavilion-services/", "/cop31-antalya-program/", "/cop31-antalya-restaurants/",
        "/cop31-event-staff/", "/cop31-interpreters/",
    ),
}

PAGES = [STANDS, BOOTH, PRODUCTION]
