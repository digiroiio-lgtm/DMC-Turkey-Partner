# -*- coding: utf-8 -*-
"""The COP31 urgent-support cluster: last-minute, rapid response and emergency.

RAPID (/cop31-rapid-response-services/) and EMERGENCY (/cop31-emergency-event-support/)
have been retired with 301 redirects to LAST_MINUTE. Their content has been merged
into LAST_MINUTE below.
"""

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
                "Most urgent COP31 requests are not exotic. They are ordinary items that were "
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
            ]),
        ),
        section(
            "Planned Procurement vs Rapid Response",
            lede(
                "Rapid response is not a faster version of a quotation process. It is a "
                "different process: availability first, specification second, paperwork last "
                "but never skipped."
            ),
            table(
                "Standard procurement vs rapid response at COP31",
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
            "How to Make a Request Work",
            checklist([
                "Send a photo. It removes more ambiguity in one message than several paragraphs.",
                "State the hard deadline and what happens if it is missed — it changes which options are worth pursuing.",
                "Give the delivery location precisely, including whether it is inside a badge-controlled area.",
                "Say whether a substitute is acceptable, and what would not be acceptable.",
                "Name one decision-maker who can approve cost immediately.",
                "Tell us if this is one of several related problems — solving them together is usually faster.",
            ]),
        ),
        section(
            "What We Can and Cannot Do",
            lede(
                "Being clear about the boundary is more useful in an emergency than an "
                "open-ended promise."
            ),
            table(
                "Scope of last-minute and emergency support at COP31",
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
            "Reducing the Chance You Need This",
            steps([
                ("Register a local contact before the conference", "A five-minute briefing in October is worth hours in November. We keep a note of who you are and what you are running."),
                ("Identify a local production fallback for anything shipped", "Especially graphics and print, which are the easiest to reproduce and the most likely to be needed."),
                ("Confirm what your stand or space actually includes", "Furniture, power, screens and lighting are the most commonly assumed inclusions."),
                ("Over-order printed material", "Running out mid-conference is close to universal. Local reprinting is fast, but not free."),
                ("Plan a communication route that works at 06:00", "One WhatsApp thread with the right people in it beats an email chain every time."),
            ]),
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
        ("What is the difference between last-minute services and rapid response?",
         "They describe the same operational capability from two angles. Last-minute services is the catalogue of what can be sourced or produced at short notice; rapid response is the way of working: availability-first sourcing, substitution, immediate delivery and on-site coordination. This page covers both."),
        ("Can you take over from a supplier who has not performed?",
         "Yes. Replacing a non-performing supplier and taking over coordination is a routine part of this work during a conference."),
        ("Do you charge a premium for emergency or out-of-hours work?",
         "Urgent sourcing, out-of-hours crew and immediate delivery generally cost more than planned procurement. Cost is confirmed in writing before we commit spend so there are no surprises afterwards."),
        ("Can you come to the venue to handle a problem on site?",
         "We can attend on site within the limits of venue access and accreditation rules, and coordinate with your accredited team for anything inside a badge-controlled area."),
        ("Should we contact you before the conference even if nothing is wrong?",
         "Yes. Teams that register a contact in advance are substantially faster to help during the event, because we already know what they are running and where."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-printing-services/", "/cop31-av-equipment-rental/",
        "/cop31-furniture-rental/", "/cop31-branding-signage/", "/cop31-exhibition-services/",
        "/cop31-event-staff/", "/cop31-private-transfers/", "/cop31-event-production/",
    ),
}


PAGES = [LAST_MINUTE]
