# -*- coding: utf-8 -*-
"""The COP31 urgent-support cluster: last-minute, rapid response, emergency."""

from cop31_common import wa_link
from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "Urgent support is one part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", alongside planned production, exhibition and pavilion services and participant "
    "information."
)

URGENT_CTA = L(
    "/cop31-printing-services/", "/cop31-av-equipment-rental/", "/cop31-furniture-rental/",
    "/cop31-branding-signage/", "/cop31-event-staff/", "/cop31-private-transfers/",
    "/cop31-event-production/",
)


LAST_MINUTE = {
    "slug": "cop31-last-minute-services",
    "breadcrumb": "Last-Minute Services",
    "title": "Last-Minute COP31 Services in Antalya | Urgent Local Sourcing 2026",
    "description": (
        "Urgent local sourcing, production and operational support during COP31 Antalya: "
        "printing, signage, furniture, screens, microphones, coffee equipment, staff, "
        "interpreters, vehicles and replacement equipment."
    ),
    "h1": "Last-Minute COP31 Services in Antalya",
    "answer": (
        "We provide urgent local sourcing, production and operational support in Antalya "
        "during COP31 — printing, signage, furniture, AV, hospitality equipment, staff, "
        "interpreters and vehicles — for requirements that appear during 9–20 November 2026."
    ),
    "lede": (
        "Fast local sourcing, production and operational support for delegations, exhibitors, "
        "pavilions and international agencies in Antalya. Send the requirement; we will tell "
        "you what is actually available and when."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Last-Minute Services",
    "service_name": "Last-Minute COP31 Services in Antalya",
    "cta_label": "Send Your Requirement",
    "wa_label": "WhatsApp Rapid Response Desk",
    "wa_message": "URGENT — COP31 Antalya. I need the following as soon as possible:",
    "sources": ["ifp", "unfccc"],
    "sections": [
        section(
            "Need Something Urgently During COP31?",
            lede(
                "Most urgent COP requests are not exotic. They are ordinary items that were "
                "assumed, shipped late, damaged in transit, under-ordered or never ordered at "
                "all — and are now needed today, in Antalya, by people who do not have a local "
                "supplier."
            ),
            cards([
                ("Print and collateral", "Reprints, additional brochures, flyers, name cards, session programmes, posters and foam board."),
                ("Missing signage", "Directional signs, fascia, panels, desk graphics, floor decals and replacement branded elements."),
                ("Furniture", "Extra chairs, tables, stools, counters and lounge pieces when the space turns out to be under-furnished."),
                ("Screens and AV", "Monitors, LED screens, projection, sound, microphones and presentation equipment, with a technician where needed."),
                ("Coffee and hospitality", "Coffee machines, water stations, refrigeration, cups and supplies for a space that is hosting more people than planned."),
                ("Branded materials", "Replacement graphics, backdrops, roll-ups and sponsor boards produced from approved artwork."),
                ("Staff", "Additional crew, hosts, hostesses and runners for a day or for the rest of the conference."),
                ("Interpreters", "Turkish–English and other combinations, subject to availability at short notice."),
                ("Vehicles and transfers", "An extra car, a van for equipment, a coach for an unplanned movement, or a driver for the rest of the week."),
                ("Event supplies and replacements", "Cables, power distribution, consumables, tools and the small physical things that stop a stand working."),
            ]),
        ),
        section(
            "How We Handle an Urgent Request",
            steps([
                ("You send the requirement", "A message, a photo, a model number, a rough description. Photos are usually faster than descriptions."),
                ("We check what exists locally, now", "Live availability in Antalya for that item, that day — not a catalogue."),
                ("We come back with what is real", "What we can supply and when, what we can substitute, and what genuinely is not available. The third answer is given as readily as the first."),
                ("You confirm", "A short written confirmation of scope and cost before anything is produced or dispatched."),
                ("Delivery and installation", "Delivered to your location, with installation where the item needs it and where venue access rules allow."),
            ]),
            para(
                "We do not publish a guaranteed response or delivery time, because during a "
                "conference fortnight that promise would be worth nothing. What we commit to is "
                "an honest availability answer quickly, so you can act on it either way."
            ),
        ),
        section(
            "What Makes Urgent Requests Succeed or Fail",
            table(
                "Practical factors in a last-minute COP31 request",
                ["Factor", "Why it matters"],
                [
                    ["Approved artwork", "Print and graphics are the fastest category to replace — but only once artwork is final. Approval, not production, is usually the bottleneck."],
                    ["Venue access", "Materials can be produced quickly and still not reach a badge-controlled area. Plan who carries items in."],
                    ["Specificity", "“A screen” takes longer than “a 55-inch monitor on a floor stand, HDMI, by 14:00 tomorrow.”"],
                    ["Timing within the fortnight", "Local rental stock is progressively committed as the conference proceeds. Day two is easier than day nine."],
                    ["Substitution tolerance", "Teams that accept a near-equivalent get solved; teams that require an exact match sometimes cannot be."],
                    ["A prior briefing", "Clients who registered a contact before the conference are markedly faster to help than a cold request at 22:00."],
                ],
            ),
        ),
        section(
            "Who Uses This",
            plain_list([
                "Exhibitors whose freight has not arrived, or arrived damaged.",
                "Pavilion teams who have run out of printed material or hospitality supplies.",
                "Agencies whose client has added a requirement on site.",
                "Delegations who need an extra vehicle, an interpreter or a meeting room today.",
                "Production teams missing a specific piece of equipment.",
                "Anyone whose supplier has not turned up.",
            ]),
            BACK,
        ),
    ],
    "cta_services": URGENT_CTA,
    "cta_heading": "Send Your Requirement to the Antalya Operations Desk",
    "cta_copy": (
        "Tell us what you need, where you need it and by when. We will confirm what is "
        "genuinely available in Antalya for that timing — including when the answer is no."
    ),
    "faqs": [
        ("What counts as a last-minute COP31 request?",
         "Anything needed within the conference period or the days immediately before it: reprints, signage, furniture, screens, microphones, hospitality equipment, staff, interpreters, vehicles or replacement equipment."),
        ("How quickly can you deliver?",
         "It depends entirely on the item, the day and what remains available locally. We do not publish a guaranteed turnaround; we give an honest availability answer quickly so you can plan around it either way."),
        ("Can you deliver into the venue?",
         "We deliver to the point that venue access rules allow, and coordinate with your accredited team for anything that has to be carried into a badge-controlled area."),
        ("What is the fastest thing to replace locally?",
         "Print, graphics and signage, provided approved artwork exists. Rental furniture and standard AV are usually next."),
        ("What is hardest at short notice?",
         "Specific AV models, particular interpreter language combinations, and vehicles during the 11–12 November Leaders Summit window."),
        ("Can we register a contact before the conference, just in case?",
         "Yes, and we recommend it. A short pre-conference briefing about who you are and what you are running makes an urgent request materially faster to solve."),
        ("How should we send an urgent request?",
         "WhatsApp is fastest — send a photo, the deadline and the delivery location. The proposal form works for anything less immediate."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-rapid-response-services/", "/cop31-emergency-event-support/",
        "/cop31-printing-services/", "/cop31-av-equipment-rental/", "/cop31-furniture-rental/",
        "/cop31-exhibition-services/", "/cop31-event-staff/", "/cop31-private-transfers/",
    ),
}


RAPID = {
    "slug": "cop31-rapid-response-services",
    "breadcrumb": "Rapid Response Services",
    "title": "COP31 Rapid Response Services – Antalya | Fast Local Sourcing 2026",
    "description": (
        "Rapid local sourcing, production, delivery, replacement and on-site coordination in "
        "Antalya during COP31 2026, for teams that need a problem solved now rather than "
        "quoted next week."
    ),
    "h1": "COP31 Rapid Response Services – Antalya",
    "answer": (
        "Rapid response means a single Antalya contact who checks live local availability, "
        "sources or produces what is missing, delivers it and coordinates on site — for "
        "requirements that cannot wait for a normal procurement cycle."
    ),
    "lede": (
        "For the requests that begin with “we need this now.” Rapid local sourcing, "
        "production, delivery and on-site coordination in Antalya, run by people who can "
        "physically get to where the problem is."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Rapid Response",
    "service_name": "COP31 Rapid Response Services in Antalya",
    "cta_label": "Request Rapid Response",
    "wa_label": "WhatsApp the Rapid Response Desk",
    "wa_message": "COP31 Antalya — rapid response needed. Here is the situation:",
    "sources": ["ifp"],
    "sections": [
        section(
            "What Rapid Response Actually Means",
            lede(
                "It is not a faster version of a quotation process. It is a different process: "
                "availability first, specification second, paperwork last but never skipped."
            ),
            table(
                "Standard procurement vs rapid response",
                ["", "Standard request", "Rapid response"],
                [
                    ["First question", "What exactly do you want?", "What is available right now that solves this?"],
                    ["Specification", "Fixed before quoting", "Often converges during the call, with substitutions offered"],
                    ["Sourcing", "Best price across suppliers", "First workable source, then price"],
                    ["Delivery", "Scheduled", "Immediate or same-period, subject to access"],
                    ["Confirmation", "Formal quotation and approval", "Short written confirmation of scope and cost before we commit spend"],
                ],
            ),
            para(
                "The written confirmation matters even under pressure. It is what stops an "
                "urgent fix turning into a disputed invoice after the conference."
            ),
        ),
        section(
            "What We Can Move Quickly On",
            cards([
                ("Local sourcing", "Finding the item in Antalya — rental stock, retail, supplier inventory or a production route."),
                ("Local production", "Print, graphics, signage and simple fabricated elements produced locally rather than shipped."),
                ("Delivery", "Getting the item to your hotel, venue perimeter, pavilion or off-site location."),
                ("Replacement", "Swapping out failed or damaged equipment, graphics or furniture."),
                ("On-site coordination", "Someone physically present to install, test, hand over or supervise."),
                ("Problem solving", "Working out what will actually fix the situation when the original plan is no longer available."),
            ]),
        ),
        section(
            "How to Make a Rapid Request Work",
            checklist([
                "Send a photo. It removes more ambiguity in one message than several paragraphs.",
                "State the hard deadline and what happens if it is missed — it changes which options are worth pursuing.",
                "Give the delivery location precisely, including whether it is inside a badge-controlled area.",
                "Say whether a substitute is acceptable, and what would not be acceptable.",
                "Name one decision-maker who can approve cost immediately.",
                "Tell us if this is one of several related problems — solving them together is usually faster.",
            ]),
            para(
                "We do not promise a specific response or delivery time in advance. What we "
                "will do is come back quickly with what is real, including when the honest "
                "answer is that it cannot be done in your window — so you can move to plan B "
                "while there is still time for one."
            ),
            BACK,
        ),
    ],
    "cta_services": URGENT_CTA,
    "cta_heading": "Have a Problem That Cannot Wait?",
    "cta_copy": (
        "Send the situation, the deadline and the location. We will confirm what is "
        "achievable in Antalya within your window."
    ),
    "faqs": [
        ("What is the difference between rapid response and last-minute services?",
         "Last-minute services is the catalogue — the categories of item we can source or produce at short notice. Rapid response is the way of working: availability-first sourcing, substitution, immediate delivery and on-site coordination."),
        ("Do you guarantee a response time?",
         "No. During a conference fortnight a guaranteed time would not be credible. We commit to answering quickly with what is genuinely available, including a clear no when that is the honest answer."),
        ("Can you act on our behalf on site?",
         "Yes, within the limits of venue access rules. We can install, test, hand over and supervise, and coordinate with your accredited team for anything inside a controlled area."),
        ("Is rapid response more expensive?",
         "Urgent sourcing and out-of-hours delivery usually cost more than planned procurement. We confirm cost in writing before committing spend so there is no surprise afterwards."),
        ("Can you help outside normal working hours?",
         "Build nights and early mornings are when most of these requests arrive, and they are part of how the desk operates during the conference period."),
        ("What if you cannot solve it?",
         "We say so quickly and, where we can, suggest what would work instead. An early no is more useful than a late maybe."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-last-minute-services/", "/cop31-emergency-event-support/",
        "/cop31-event-services/", "/cop31-printing-services/", "/cop31-av-equipment-rental/",
        "/cop31-exhibition-services/", "/cop31-event-staff/",
    ),
}


EMERGENCY = {
    "slug": "cop31-emergency-event-support",
    "breadcrumb": "Emergency Event Support",
    "title": "COP31 Emergency Event Support in Antalya | On-Site Problem Solving 2026",
    "description": (
        "On-site emergency event support in Antalya during COP31: broken AV, missing "
        "furniture or print, staffing gaps, transport failures, damaged graphics, supplier "
        "no-shows and urgent replacement sourcing."
    ),
    "h1": "COP31 Emergency Event Support in Antalya",
    "answer": (
        "Emergency event support covers the failures that happen during a live event in "
        "Antalya — broken AV, missing furniture or print, staffing gaps, transport failures, "
        "damaged graphics and supplier no-shows — handled by a local team during COP31."
    ),
    "lede": (
        "Events fail in predictable ways. This page lists the ones that actually happen at a "
        "COP, and what a local operations team can do about each of them while the event is "
        "still running."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Emergency Event Support",
    "service_name": "COP31 Emergency Event Support in Antalya",
    "cta_label": "Contact the Antalya Operations Desk",
    "wa_label": "WhatsApp the Antalya Operations Desk",
    "wa_message": "COP31 Antalya — emergency event support needed. The problem is:",
    "sources": ["ifp"],
    "sections": [
        section(
            "The Failures That Actually Happen",
            lede(
                "None of these are unusual. Every one of them appears at every large "
                "conference, which is precisely why they are worth planning for."
            ),
            cards([
                ("Broken or missing AV", "A screen fails, a microphone does not arrive, a laptop will not output. Replacement equipment and a technician, subject to what remains available locally."),
                ("Missing furniture", "The space is under-furnished or a delivery is short. Additional chairs, tables and counters from local rental stock — see " + A("/cop31-furniture-rental/", "furniture rental") + "."),
                ("Print material has run out or is wrong", "Reprints and replacements produced in Antalya from approved artwork — see " + A("/cop31-printing-services/", "printing services") + "."),
                ("Damaged graphics", "Panels, fascia and backdrops damaged in transit or on site, reproduced and reinstalled — see " + A("/cop31-branding-signage/", "branding and signage") + "."),
                ("Staffing gaps", "Someone is ill, a shift is uncovered, or the space needs more hands than planned — see " + A("/cop31-event-staff/", "event staff") + "."),
                ("Transport failures", "A vehicle does not arrive, a schedule collapses, or an unplanned movement is needed — see " + A("/cop31-private-transfers/", "private transfers") + "."),
                ("Missing technical equipment", "Cables, power distribution, stands, adapters and the small items that stop everything else working."),
                ("Supplier no-show", "A booked supplier does not appear. We source a local replacement and take over coordination."),
                ("Urgent replacement sourcing", "Anything else that has to be found in Antalya today — see " + A("/cop31-last-minute-services/", "last-minute services") + "."),
            ]),
        ),
        section(
            "What We Can and Cannot Do",
            lede(
                "Being clear about the boundary is more useful in an emergency than an "
                "open-ended promise."
            ),
            table(
                "Scope of emergency support",
                ["We can", "We cannot"],
                [
                    ["Source and deliver replacement equipment, furniture, print and graphics from local supply", "Override venue access, accreditation or security rules"],
                    ["Provide crew, technicians, hosts and drivers subject to availability", "Guarantee that a specific item exists in Antalya at a given hour"],
                    ["Attend on site and coordinate a fix", "Enter badge-controlled areas without appropriate accreditation"],
                    ["Take over from a supplier who has not performed", "Resolve issues that are the venue's or the organisers' to resolve"],
                    ["Give you a fast, honest read on what is achievable", "Promise a fixed response time during the conference fortnight"],
                ],
            ),
        ),
        section(
            "Reducing the Chance You Need This",
            steps([
                ("Register a local contact before the conference", "A five-minute briefing in October is worth hours in November. We keep a note of who you are and what you are running."),
                ("Identify a local production fallback for anything shipped", "Especially graphics and print, which are the easiest to reproduce and the most likely to be needed."),
                ("Confirm what your stand or space actually includes", "Furniture, power, screens and lighting are the most commonly assumed inclusions."),
                ("Over-order printed material", "Running out mid-conference is close to universal. Local reprinting is fast, but not free."),
                ("Plan a communication route that works at 06:00", "One WhatsApp thread with the right people in it beats an email chain every time."),
            ]),
            BACK,
        ),
    ],
    "cta_services": URGENT_CTA,
    "cta_heading": "Something Has Gone Wrong at COP31?",
    "cta_copy": (
        "Tell us what has failed, where it is and when you need it fixed. We will come back "
        "with what can realistically be done from Antalya."
    ),
    "faqs": [
        ("What is COP31 emergency event support?",
         "On-site problem solving during the conference: replacing failed AV, sourcing missing furniture or print, covering staffing gaps, handling transport failures and taking over from suppliers who have not performed."),
        ("Can you come to the venue?",
         "We can attend on site within the limits of venue access and accreditation rules, and coordinate with your accredited team for anything inside a controlled area."),
        ("How fast can you fix a problem?",
         "It depends on the problem and what is available in Antalya at that moment. We give a fast, honest read on what is achievable rather than a fixed promise."),
        ("Do you charge a premium for emergency work?",
         "Urgent sourcing, out-of-hours crew and immediate delivery generally cost more than planned work. Cost is confirmed in writing before we commit spend."),
        ("Can you help if the failure is our supplier's fault, not ours?",
         "Yes. Replacing a non-performing supplier and taking over coordination is a routine part of this work."),
        ("Should we contact you before the conference even if nothing is wrong?",
         "Yes. Teams that register a contact in advance are substantially faster to help, because we already know what they are running and where."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-last-minute-services/", "/cop31-rapid-response-services/",
        "/cop31-event-services/", "/cop31-exhibition-services/", "/cop31-av-equipment-rental/",
        "/cop31-furniture-rental/", "/cop31-event-staff/", "/cop31-printing-services/",
    ),
}

PAGES = [LAST_MINUTE, RAPID, EMERGENCY]
