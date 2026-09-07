# -*- coding: utf-8 -*-
"""Staffing cluster: event staff, hostesses, interpreters."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", covering participant information and the full local service range."
)

STAFF_CTA = L(
    "/cop31-hostess-staff/", "/cop31-interpreters/", "/cop31-event-services/",
    "/cop31-exhibition-services/", "/cop31-pavilion-services/", "/cop31-event-production/",
    "/cop31-last-minute-services/",
)


EVENT_STAFF = {
    "slug": "cop31-event-staff",
    "breadcrumb": "Event Staff",
    "title": "COP31 Event Staff in Antalya | Crew, Setup Teams & Operational Support",
    "description": (
        "COP31 event staff in Antalya: event crew, runners, setup and dismantling teams, "
        "registration support, operational and logistics staff and technicians for the "
        "November 2026 conference period."
    ),
    "h1": "COP31 Event Staff in Antalya",
    "answer": (
        "We supply local event staff in Antalya for COP31 — event crew, runners, setup and "
        "dismantling teams, registration support, logistics and operational staff, and "
        "technicians — for build days, live days and breakdown."
    ),
    "lede": (
        "Local hands for the parts of a conference that do not run themselves: build, "
        "restocking, movement, registration desks, breakdown and the general operational work "
        "that keeps a stand or programme functioning."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Event Staff",
    "service_name": "COP31 Event Staffing in Antalya",
    "cta_label": "Request Event Staff",
    "sources": ["ifp"],
    "sections": [
        section(
            "Staff Profiles We Supply",
            cards([
                ("Event crew", "General operational staff for stands, pavilions and side events across build, live and derig phases."),
                ("Runners", "Movement of stock, materials and messages between store, stand, hotel and off-site locations."),
                ("Setup and build teams", "Assembly, graphics application, furniture placement and finishing during the build window."),
                ("Registration and desk support", "Staffing your own registration or welcome desk at a side event or hotel — distinct from official COP31 accreditation, which is handled by UNFCCC."),
                ("Logistics crew", "Loading, unloading, storage handling and delivery coordination."),
                ("Operational staff", "Restocking, daily reset, tidying and the routine work that keeps a two-week space presentable."),
                ("Technicians", "AV and technical crew where required — see " + A("/cop31-event-production/", "event production") + " for full production crewing."),
                ("Supervisors", "A shift lead who reports to your team, so you are not supervising staff yourself."),
            ]),
        ),
        section(
            "How Staffing Is Usually Structured",
            table(
                "Typical COP31 staffing patterns",
                ["Phase", "Common requirement", "Notes"],
                [
                    ["Build days", "Setup crew, sometimes overnight", "The heaviest crew requirement, concentrated into a few days"],
                    ["Opening days", "Full complement, front and back of house", "Days one to three are the busiest of the conference"],
                    ["Mid-conference", "Reduced crew, restocking focus", "Where teams most often over-staff or under-staff"],
                    ["Leaders Summit window", "Peak coverage, longer hours", "11–12 November; plan this separately from the rest"],
                    ["Closing and derig", "Dismantle crew", "Frequently forgotten until the last afternoon"],
                ],
            ),
            para(
                "Booking by phase rather than as a flat daily number usually costs less and "
                "covers better. Tell us the shape of the fortnight and we will propose a "
                "pattern rather than a headcount."
            ),
        ),
        section(
            "Practical Notes on Staffing",
            checklist([
                "Specify language requirements explicitly — English-speaking crew is standard, other languages depend on availability and should be requested early.",
                "Name a single point of contact on your side. Staff working to three different instructions is the most common staffing failure.",
                "Decide whether you need a supervisor. For anything above about four staff, it usually pays for itself.",
                "Brief in advance where possible. Crew who understand what the space is for perform noticeably better than crew given tasks only.",
                "Plan shift lengths realistically. Twelve-hour days across two weeks degrade performance and increase turnover.",
                "Confirm what access your staff need. Anything inside a badge-controlled area depends on accreditation you hold, not on us.",
            ]),
            BACK,
        ),
    ],
    "cta_services": STAFF_CTA,
    "cta_heading": "Need Staff in Antalya for COP31?",
    "faqs": [
        ("What kind of event staff can you provide for COP31?",
         "Event crew, runners, setup and dismantling teams, registration and welcome desk staff, logistics crew, operational and restocking staff, technicians and shift supervisors."),
        ("Do your staff speak English?",
         "English-speaking crew is the standard supply for an international conference. Other language combinations depend on availability and should be requested as early as possible."),
        ("Can staff work inside the venue?",
         "Only with appropriate accreditation, which is issued through the official COP31 process and depends on passes you hold. We work with your accredited team for anything inside a controlled area."),
        ("How far in advance should we book staff?",
         "General crew can be added later than most services, but the better profiles — bilingual, experienced, supervisory — are committed early. Build-day crew is the tightest category."),
        ("Can we increase staff numbers during the conference?",
         "Usually yes, subject to availability at the time. Adding a day or two of extra crew mid-conference is a common and generally workable request."),
        ("Do you provide a supervisor?",
         "Yes, and we recommend one for teams above roughly four staff. A shift lead reporting to you removes the supervision burden from your own team."),
        ("Is registration staffing the same as COP31 accreditation?",
         "No. We staff your own registration or welcome desks at side events and hotels. Official COP31 accreditation and badges are issued exclusively by UNFCCC."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-hostess-staff/", "/cop31-interpreters/",
        "/cop31-exhibition-services/", "/cop31-pavilion-services/", "/cop31-event-production/",
        "/cop31-event-services/", "/cop31-last-minute-services/",
    ),
}


HOSTESS = {
    "slug": "cop31-hostess-staff",
    "breadcrumb": "Hostesses",
    "title": "COP31 Hostess & Registration Staff in Antalya | Guest Welcome 2026",
    "description": (
        "COP31 hostess and registration staff in Antalya: guest welcome, registration desks, "
        "directional support, meeting assistance and multilingual profiles where available "
        "for the November 2026 conference."
    ),
    "h1": "COP31 Hostess &amp; Registration Staff in Antalya",
    "answer": (
        "We supply hostesses and registration staff in Antalya for COP31 — guest welcome, "
        "registration and welcome desks, directional support and meeting assistance — with "
        "multilingual profiles where available."
    ),
    "lede": (
        "Front-of-house staff for stands, pavilions, side events and delegation hotels. The "
        "people your visitors actually interact with, which makes profile and briefing matter "
        "more than headcount."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Hostess Staff",
    "service_name": "COP31 Hostess and Registration Staffing in Antalya",
    "cta_label": "Request Hostess Staff",
    "sources": ["ifp"],
    "sections": [
        section(
            "Where Hostess Staff Are Used",
            cards([
                ("Stand and booth hosting", "Greeting visitors, qualifying interest, handing over to your specialists and keeping the space presentable."),
                ("Pavilion reception", "Welcoming delegations, managing session entry and directing visitors within a larger space."),
                ("Registration and welcome desks", "Your own side-event or delegation desks — distinct from official COP31 accreditation, which UNFCCC handles."),
                ("Guest welcome at hotels", "Meeting arriving delegations, staffing a welcome point and answering the first practical questions."),
                ("Directional support", "Guiding guests between entrances, rooms and venues at a side event."),
                ("Meeting assistance", "Managing a meeting schedule, escorting visitors and keeping bilaterals running to time."),
                ("Reception and dinner hosting", "Welcoming guests, managing seating and supporting an evening programme."),
            ]),
        ),
        section(
            "Choosing the Right Profile",
            lede(
                "Hostess requirements are almost never about numbers. They are about language, "
                "presentation and how much judgement the role requires."
            ),
            table(
                "Matching profile to role",
                ["Role", "What matters most"],
                [
                    ["Stand hosting", "Confidence, English, ability to qualify a visitor rather than just greet them"],
                    ["Pavilion reception", "Composure with senior visitors, session-schedule awareness"],
                    ["Registration desk", "Accuracy, patience and clear process under queue pressure"],
                    ["Delegation welcome", "Language match with the delegation, discretion, local knowledge"],
                    ["Meeting assistance", "Timekeeping, discretion and comfort escorting senior individuals"],
                ],
            ),
            para(
                "Language combinations beyond English are the most constrained variable during "
                "a conference fortnight and should be requested as early as possible. For "
                "actual interpretation rather than language-capable hosting, see "
                + A("/cop31-interpreters/", "COP31 interpreters") + "."
            ),
        ),
        section(
            "Briefing Makes the Difference",
            checklist([
                "Send a short brief: what your organisation does, what the space is for, and what a good visitor interaction looks like.",
                "Provide a one-page FAQ. Hosts who can answer the five most common questions look far more credible than hosts who fetch someone.",
                "Name the handover point — when a host should bring in one of your own people.",
                "Confirm dress expectations in advance rather than on the first morning.",
                "Agree break coverage. A desk that is unstaffed for twenty minutes at a peak is worse than one host fewer.",
                "Say what is confidential. Front-of-house staff hear a great deal at a conference like this.",
            ]),
            BACK,
        ),
    ],
    "cta_services": STAFF_CTA,
    "cta_heading": "Need Hostesses or Desk Staff in Antalya?",
    "faqs": [
        ("What do COP31 hostess staff do?",
         "Guest welcome, stand and pavilion hosting, registration and welcome desk staffing, directional support, meeting assistance and reception hosting."),
        ("Do you provide multilingual hostesses?",
         "English-speaking staff is standard. Additional language combinations depend on availability during the conference period and should be requested early."),
        ("Is this the same as COP31 registration?",
         "No. We staff your own registration and welcome desks at side events, stands and hotels. Official COP31 accreditation and badge issuance are managed exclusively by UNFCCC."),
        ("How many hostesses do we need?",
         "It depends on footfall, opening hours and break coverage rather than on space size. Two hosts on a small stand usually outperforms three on a rota that leaves gaps."),
        ("Can hostesses work inside the venue?",
         "Only with appropriate accreditation, which depends on passes issued through the official process and held by your organisation."),
        ("How early should we book?",
         "Early for specific language or presentation requirements; later is workable for general English-speaking hosting. The constrained variable is profile, not availability in general."),
        ("Can we brief the staff before the conference?",
         "Yes, and it makes a visible difference. A short brief and a one-page FAQ turn a greeter into someone who represents you properly."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-event-staff/", "/cop31-interpreters/",
        "/cop31-pavilion-services/", "/cop31-exhibition-services/", "/cop31-event-services/",
        "/cop31-antalya-participant-guide/",
    ),
}


INTERPRETERS = {
    "slug": "cop31-interpreters",
    "breadcrumb": "Interpreters",
    "title": "COP31 Interpreters in Antalya | Turkish–English Language Support",
    "description": (
        "COP31 interpreters and language support in Antalya: Turkish–English and other "
        "combinations where available, consecutive interpreting, meeting and delegation "
        "support for the November 2026 conference."
    ),
    "h1": "COP31 Interpreters &amp; Language Support in Antalya",
    "answer": (
        "We source interpreters in Antalya for COP31 — Turkish–English as standard and other "
        "combinations subject to availability — for consecutive interpreting at meetings, "
        "bilaterals, site visits, media interactions and delegation support."
    ),
    "lede": (
        "Language support for the meetings that happen around the conference rather than "
        "inside the formal sessions: supplier meetings, bilaterals, site visits, local media "
        "and delegation hosting."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Interpreters",
    "service_name": "COP31 Interpretation and Language Support in Antalya",
    "cta_label": "Request an Interpreter",
    "sources": ["ifp", "unfccc"],
    "sections": [
        section(
            "What We Can Source",
            lede(
                "We list only what is actually available or sourceable locally. If a "
                "combination cannot be covered for your dates, we will say so rather than take "
                "the booking."
            ),
            cards([
                ("Turkish ↔ English", "The core combination and the one most delegations need in Antalya — for suppliers, authorities, venues, local media and hosting."),
                ("Other combinations", "Additional language pairs can be sourced subject to availability during the conference period; request as early as possible."),
                ("Consecutive interpreting", "The standard mode for meetings, bilaterals, site visits and small groups."),
                ("Meeting interpretation", "Support for structured meetings, negotiations with local counterparts and supplier discussions."),
                ("Delegation support", "An interpreter attached to a delegation for a day or for the conference period, rather than booked per meeting."),
                ("Event support", "Interpretation at side events, receptions and briefings, coordinated with " + A("/cop31-event-production/", "event production") + " where equipment is involved."),
            ]),
        ),
        section(
            "Choosing the Right Kind of Support",
            table(
                "Interpretation modes and when each fits",
                ["Mode", "Fits", "Practical note"],
                [
                    ["Consecutive", "Meetings, bilaterals, site visits, interviews", "No equipment needed; roughly doubles meeting duration"],
                    ["Whispered", "One or two listeners in a larger meeting", "Works for small numbers only"],
                    ["Simultaneous with equipment", "Conference sessions and larger audiences", "Requires booths or portable systems and usually two interpreters per language"],
                    ["Language-capable hosting", "Welcoming and directing guests", "Not interpretation — see " + A("/cop31-hostess-staff/", "hostess staff")],
                ],
            ),
            para(
                "Note that formal UNFCCC sessions have their own official language "
                "arrangements. What we provide is independent local support for meetings and "
                "events around the conference, not interpretation of the official proceedings."
            ),
        ),
        section(
            "Booking Notes",
            checklist([
                "Book early. Interpreter availability during a two-week international conference is the most constrained staffing category we handle.",
                "Send subject matter in advance. Climate, energy and policy terminology benefits enormously from preparation material.",
                "Allow for meeting length. Consecutive interpretation roughly doubles the time a meeting takes — plan the schedule accordingly.",
                "For long days or simultaneous work, two interpreters per language is the professional standard, not an upsell.",
                "Confirm the location and whether venue access is required, since that depends on accreditation you hold.",
                "Tell us if the content is sensitive so that appropriate confidentiality arrangements are in place.",
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-event-services/", "/cop31-hostess-staff/", "/cop31-event-staff/",
        "/cop31-event-production/", "/cop31-private-transfers/", "/cop31-antalya-restaurants/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Need an Interpreter in Antalya?",
    "faqs": [
        ("What languages can you cover at COP31?",
         "Turkish–English is the core combination. Other language pairs can be sourced subject to availability during the conference period — we confirm before accepting a booking rather than promise in advance."),
        ("Do you interpret the official COP31 sessions?",
         "No. Formal UNFCCC sessions have their own official language arrangements. We provide independent local interpretation for meetings, bilaterals, site visits, media interactions and events around the conference."),
        ("What is consecutive interpreting?",
         "The interpreter speaks after the speaker, in segments. It needs no equipment and suits meetings, bilaterals and site visits, but roughly doubles the time a meeting takes."),
        ("Can you provide simultaneous interpretation with equipment?",
         "Simultaneous interpretation requires booths or portable systems and normally two interpreters per language. It can be arranged subject to interpreter and equipment availability."),
        ("How early should we book an interpreter?",
         "As early as possible. Interpreters are the most constrained staffing category during the conference fortnight, particularly for language pairs other than Turkish–English."),
        ("Can an interpreter accompany our delegation for several days?",
         "Yes. Attaching an interpreter to a delegation for a period is usually more effective and better value than booking per meeting."),
        ("Will you tell us if a language cannot be covered?",
         "Yes. We only list combinations that are genuinely available or sourceable, and we will decline rather than take a booking we cannot staff."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-hostess-staff/", "/cop31-event-staff/",
        "/cop31-antalya-participant-guide/", "/cop31-event-services/",
        "/cop31-event-production/", "/cop31-antalya-restaurants/",
    ),
}

PAGES = [EVENT_STAFF, HOSTESS, INTERPRETERS]
