# -*- coding: utf-8 -*-
"""Registration guide, Antalya EXPO Center venue guide and restaurants."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ", covering dates, venue, participant information and local services."
)


REGISTRATION = {
    "slug": "cop31-antalya-registration",
    "breadcrumb": "Registration",
    "title": "COP31 Antalya Registration Guide 2026 | How to Attend COP31",
    "description": (
        "How COP31 registration works: participant categories, the UNFCCC Online Registration "
        "System, nomination and confirmation, observer organisations and badges — with links "
        "to the official UNFCCC sources."
    ),
    "h1": "COP31 Antalya Registration Guide 2026",
    "answer": (
        "Registration for COP31 is managed officially by UNFCCC through its Online "
        "Registration System (ORS). Participants are nominated by their Party, observer "
        "organisation, UN body or accredited media organisation, approved by UNFCCC, and "
        "issued a badge free of charge."
    ),
    "lede": (
        "A practical summary of how COP31 accreditation works and where each official rule "
        "lives. DmcTurkeyPartner does not register participants and cannot obtain badges — "
        "this page exists to point you to the right place, then help with everything that "
        "happens after you are accredited."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Post-Registration Support",
    "service_name": "COP31 Antalya Local Support",
    "update_sensitive": True,
    "sources": ["ifp", "observers", "unfccc", "tr"],
    "sections": [
        section(
            "Who Manages COP31 Registration",
            lede(
                "Registration for COP31 is managed officially by UNFCCC through its Online "
                "Registration System (ORS). This page provides a practical summary and links "
                "users to the appropriate official information."
            ),
            para(
                "No travel company, DMC or event supplier can register you, nominate you or "
                "obtain a badge on your behalf. UNFCCC states that registration formalities, "
                "including badge issuance for duly nominated participants, are free of charge. "
                "Any offer to sell you COP31 accreditation should be treated as a warning sign."
            ),
        ),
        section(
            "Who Can Register",
            lede(
                "Access is by category, and every category is nominated by an organisation "
                "rather than by the individual."
            ),
            table(
                "COP31 participant categories",
                ["Category", "Nominated by"],
                [
                    ["Party delegates", "The Party's own competent authority or national focal point"],
                    ["Observer States", "The State's designated authority"],
                    ["United Nations bodies and specialised agencies", "The organisation itself"],
                    ["Admitted intergovernmental organisations (IGOs)", "The admitted organisation"],
                    ["Admitted non-governmental organisations (NGOs)", "The admitted organisation"],
                    ["Media", "The accredited media organisation, through the media accreditation process"],
                ],
            ),
            para(
                "If your organisation is not already admitted as an observer, admission is a "
                "separate process from registration and runs on its own cycle — the UNFCCC "
                "observer organisations page is the authority on eligibility and admission."
            ),
        ),
        section(
            "How the Process Works",
            steps([
                ("Organisation registration", "The nominating body — Party, observer organisation, UN body or media organisation — is set up in the system."),
                ("Participant nomination", "The organisation nominates individuals through the Online Registration System, within its own quota."),
                ("Confirmation by the nominee", "Nominated individuals receive an automated notification, then verify their personal details and upload a photograph."),
                ("UNFCCC approval", "UNFCCC reviews and approves nominations against the applicable rules."),
                ("Notification and badge", "Approved participants are notified, and badges are issued through the official process at no charge."),
            ]),
            para(
                "Nomination and confirmation deadlines differ by participant category and are "
                "published by UNFCCC. They also move. This page deliberately does not restate "
                "specific dates as fixed — check the official participant information page and "
                "the observer organisations page for the current deadlines that apply to you."
            ),
        ),
        section(
            "Badges and Access",
            checklist([
                "Badges are personal and non-transferable; access to conference zones follows the badge category.",
                "The photograph and personal details you confirm during nomination are what appear on the badge, so confirm them carefully.",
                "Lost badge procedures, collection points and zone rules are published by the organisers — follow those rather than third-party summaries.",
                "Venue access rules govern what suppliers, contractors and crew can do inside controlled areas, and depend on accreditation your organisation holds.",
                "Visa requirements are separate from accreditation and depend on nationality — start them early, not once your badge is confirmed.",
            ]),
        ),
        section(
            "Already Registered? Need Local Support in Antalya?",
            lede(
                "Accreditation is the one thing we cannot help with. Everything after it is what "
                "we do."
            ),
            cards([
                ("Accommodation and placement", "/cop31-antalya-accommodation/", "Group sourcing, room blocks, meeting rooms and staff accommodation once your team is confirmed."),
                ("Transport", "/cop31-private-transfers/", "Airport arrivals, hotel–venue movement and dedicated vehicles for the conference period."),
                ("Exhibition and pavilion support", "/cop31-exhibition-services/", "Build, graphics, furniture, AV, storage and on-site support for a physical presence."),
                ("Event services", "/cop31-event-services/", "Side events, meeting rooms, production, staffing and hospitality around the official programme."),
                ("Printing and collateral", "/cop31-printing-services/", "Delegation material produced locally, including reprints during the conference."),
                ("Urgent local support", "/cop31-last-minute-services/", "Fast local sourcing when something is missing, delayed or damaged."),
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-antalya-accommodation/", "/cop31-private-transfers/",
        "/cop31-exhibition-services/", "/cop31-event-services/", "/cop31-printing-services/",
        "/cop31-event-staff/", "/cop31-last-minute-services/",
    ),
    "cta_heading": "Already Registered? Need Local Support in Antalya?",
    "faqs": [
        ("How do I register for COP31?",
         "Registration is managed by UNFCCC through its Online Registration System. You are nominated by your Party, observer organisation, UN body or accredited media organisation, then confirm your details and are approved by UNFCCC."),
        ("Can DmcTurkeyPartner register us for COP31?",
         "No. Registration and accreditation are handled exclusively by UNFCCC and the official COP31 bodies. We support accommodation, transport, production, staffing and local logistics once you are accredited."),
        ("Does COP31 registration cost anything?",
         "UNFCCC states that registration formalities, including badge issuance for duly nominated participants, are free of charge. Treat any offer to sell accreditation as a warning sign."),
        ("What is the ORS?",
         "The UNFCCC Online Registration System — the platform through which organisations register, nominate participants, and through which nominees confirm their details and receive approval."),
        ("How do observer organisations register?",
         "Admitted intergovernmental and non-governmental organisations nominate participants through the ORS within their allocated quota. Admission as an observer organisation is a separate process from registration — the UNFCCC observer organisations page is the authority."),
        ("What are the registration deadlines?",
         "Deadlines differ by participant category and are published by UNFCCC. Because they change, this page does not restate them as fixed — check the official participant information and observer organisations pages for the current dates."),
        ("Do I need a visa as well as a badge?",
         "Visa requirements depend on your nationality and are entirely separate from conference accreditation. Check them early rather than after your badge is confirmed."),
        ("Can our contractors access the venue?",
         "Venue access for suppliers and crew is governed by the organisers' rules and depends on accreditation your organisation holds. We work within those rules and coordinate with your accredited team."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-participant-guide/", "/cop31-antalya-dates/",
        "/cop31-antalya-venue/", "/cop31-antalya-accommodation/", "/cop31-antalya-transport/",
        "/cop31-event-services/", "/cop31-exhibition-services/",
    ),
}


EXPO = {
    "slug": "cop31-antalya-expo-center",
    "breadcrumb": "Antalya EXPO Center",
    "title": "Antalya EXPO Center – COP31 Venue Guide 2026 | Access & Logistics",
    "description": (
        "A COP31 venue guide to the Antalya EXPO Center: where it is, access from Antalya "
        "Airport, surrounding districts, transportation, event logistics and exhibitor "
        "considerations for November 2026."
    ),
    "h1": "Antalya EXPO Center – COP31 Venue Guide",
    "answer": (
        "The Antalya EXPO Center is the COP31 venue, hosting the conference from 9 to 20 "
        "November 2026. It sits east of Antalya city centre in the Aksu area, close to Antalya "
        "Airport and the Lara–Kundu–Belek accommodation corridor."
    ),
    "lede": (
        "A venue-focused briefing for international participants, exhibitors and agencies: "
        "where the building sits in the city, how people and materials reach it, and what its "
        "location implies for build, movement and local operations."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Venue Logistics",
    "service_name": "COP31 Venue Logistics Support",
    "sources": ["ifp", "unfccc", "tr"],
    "sections": [
        section(
            "Where the Antalya EXPO Center Is",
            lede(
                "UNFCCC identifies the Antalya EXPO Center as the venue for COP31. It is "
                "located east of Antalya city centre in the Aksu area, on the airport side of "
                "the city and adjacent to the corridor where most large-format hotel capacity "
                "sits."
            ),
            para(
                "For an international participant, the useful mental model is a single line "
                "running west to east: Antalya city centre and Konyaaltı, then Lara and Kundu, "
                "then the airport and the venue in Aksu, then Belek further east. Almost every "
                "COP31 journey you make will be along that line."
            ),
            para(
                "We do not publish floor areas, hall specifications, rigging limits or "
                "capacities for the venue. Those are issued by the venue and the conference "
                "organisers to confirmed exhibitors, and are the only version worth planning "
                "against."
            ),
        ),
        section(
            "Access from Antalya Airport",
            checklist([
                "Antalya Airport (AYT) is the arrival point for the large majority of participants and sits close to the venue on the same side of the city.",
                "Arrival volume concentrates into the days immediately before 9 November, and departures into 20 November and the day after.",
                "Conference-period traffic management can change normal routes and timings — confirm access arrangements through the official participant information.",
                "Freight and equipment arriving by air need a vehicle sized to the load and a plan for where it goes before it reaches the venue.",
                "Pre-booked transfers are materially more reliable than arranging transport on arrival during the peak days.",
            ]),
            para(
                "See " + A("/cop31-antalya-airport-transfer/", "COP31 airport transfers")
                + " for arrivals, and the "
                + A("/cop31-antalya-transport/", "transport guide") + " for daily movement."
            ),
        ),
        section(
            "Surrounding Districts",
            table(
                "The venue's surroundings",
                ["Area", "Position", "What it offers participants"],
                [
                    ["Aksu", "The venue's district", "Closest accommodation; limited inventory"],
                    ["Antalya Airport", "Immediately west", "Arrivals, departures, freight, crew movement"],
                    ["Kundu", "West along the coast", "Large resort hotels with meeting and event capacity"],
                    ["Lara", "Further west", "The main delegation corridor; hotels, restaurants, event space"],
                    ["Belek", "East along the coast", "Large resorts and conference facilities for sizeable groups"],
                    ["Antalya city centre", "Furthest west", "Restaurants, evening programmes, city hotels, the old town"],
                ],
            ),
        ),
        section(
            "Event Logistics and Exhibitor Considerations",
            lede(
                "The venue's rules govern the detail. What follows is the operating context "
                "that applies whatever the detail turns out to be."
            ),
            cards([
                ("A shared build window", "Every exhibitor and pavilion installs in the same compressed period. Late materials join a queue rather than simply arriving late."),
                ("Badge-controlled access", "Plan who physically carries what into the venue and when. This is the single most commonly overlooked constraint in a delivery plan."),
                ("Deliveries need a named receiver", "A delivery with no one to accept it is a delivery that does not happen. Name the person and the window."),
                ("Local production reduces exposure", "Graphics, print, signage and furniture made in Antalya avoid freight risk entirely and can be replaced mid-conference — see " + A("/cop31-exhibition-stands/", "exhibition stands") + "."),
                ("Storage is a real requirement", "Stock, giveaways, spare graphics and empty cases need somewhere to live for two weeks."),
                ("Power and technical assumptions", "Confirm what your space actually provides rather than assuming — power is the most frequent stand-day surprise."),
                ("Dismantle is a project", "Breakdown, equipment return, disposal and freight collection after 20 November need planning, not improvisation."),
                ("Off-site is often easier", "Many side events run better in hotel meeting rooms along the corridor than in venue space — see " + A("/cop31-event-services/", "event services") + "."),
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-exhibition-services/", "/cop31-exhibition-stands/", "/cop31-pavilion-services/",
        "/cop31-event-production/", "/cop31-furniture-rental/", "/cop31-av-equipment-rental/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Operating at the Antalya EXPO Center?",
    "faqs": [
        ("Where is the Antalya EXPO Center?",
         "East of Antalya city centre in the Aksu area, on the airport side of the city and adjacent to the Lara–Kundu–Belek accommodation corridor."),
        ("Is the Antalya EXPO Center the COP31 venue?",
         "Yes. UNFCCC identifies the Antalya EXPO Center as the venue for COP31, held from 9 to 20 November 2026."),
        ("How do participants reach the venue?",
         "Most arrive through Antalya Airport, which is close by, and travel from hotels along the coastal corridor by official shuttle, taxi or dedicated vehicle."),
        ("What are the venue's hall sizes and technical specifications?",
         "Those are issued by the venue and the conference organisers to confirmed exhibitors. We do not publish venue specifications we cannot verify, and the official documentation is the only version worth planning against."),
        ("Can suppliers deliver directly to a stand?",
         "Venue access is badge-controlled, so delivery to a stand depends on the organisers' access rules and on accreditation your organisation holds. We coordinate with your accredited team for anything inside a controlled area."),
        ("Is it better to produce materials locally or ship them?",
         "For graphics, print, signage and furniture, local production in Antalya is faster, avoids freight risk entirely and can be replaced during the conference. Reserve shipping for what genuinely cannot be made locally."),
        ("Can side events be held away from the venue?",
         "Yes, and many are. Hotel meeting rooms and private venues along the Lara, Kundu and Belek corridor are often easier to schedule and load into than venue space."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-venue/", "/cop31-antalya-participant-guide/",
        "/cop31-antalya-transport/", "/cop31-antalya-hotels/", "/cop31-exhibition-services/",
        "/cop31-pavilion-services/", "/cop31-exhibition-stands/",
    ),
}


RESTAURANTS = {
    "slug": "cop31-antalya-restaurants",
    "breadcrumb": "Restaurants & Dining",
    "title": "COP31 Antalya Restaurants & Private Dining Guide 2026",
    "description": (
        "COP31 Antalya restaurants and private dining: business dinners, delegation dinners, "
        "group reservations, side-event dinners and private rooms across Lara, Belek and "
        "Antalya city centre."
    ),
    "h1": "COP31 Antalya Restaurants &amp; Private Dining Guide",
    "answer": (
        "Antalya has substantial restaurant capacity across Lara, Kundu, Belek and the city "
        "centre, but private rooms and group reservations during COP31 are finite and should "
        "be booked well before 9 November 2026."
    ),
    "lede": (
        "Where COP31 delegations actually eat, and how to secure the specific things that run "
        "out: private rooms, group tables and venues that can hold a hosted dinner during the "
        "busiest fortnight of Antalya's year."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Dining & Hospitality",
    "service_name": "COP31 Antalya Dining and Private Events",
    "sources": ["ifp", "tr"],
    "sections": [
        section(
            "The Areas, and What Each Is Good For",
            table(
                "Dining areas around COP31",
                ["Area", "Character", "Best for"],
                [
                    ["Antalya city centre &amp; Kaleiçi", "The old town, harbour and city restaurants", "Atmosphere, walkable evenings, smaller hosted dinners"],
                    ["Lara", "Resort hotels plus a strong independent restaurant scene", "Business dinners close to delegation hotels"],
                    ["Kundu", "Large hotels with in-house restaurants", "In-hotel delegation dining with no transport required"],
                    ["Belek", "Resort and golf hotel dining", "Groups already staying in Belek; large hosted dinners"],
                    ["Konyaaltı", "Seafront dining west of the centre", "Relaxed evenings, informal team dinners"],
                    ["Aksu / venue area", "Limited standalone dining", "Convenience rather than experience"],
                ],
            ),
            para(
                "The practical rule during a conference is that transport time is part of the "
                "dinner. A restaurant forty minutes away turns a two-hour dinner into a "
                "four-hour evening, which matters when the same people have an 08:00 start."
            ),
        ),
        section(
            "What Actually Runs Out",
            lede(
                "General restaurant capacity in Antalya is not the constraint. Five specific "
                "things are."
            ),
            checklist([
                "Private rooms — every delegation wants one, and there are far fewer than there are delegations.",
                "Tables for 10–30 at a fixed time, which most restaurants can do once an evening rather than repeatedly.",
                "Venues that can hold a hosted dinner for 80+ with a speech and a screen.",
                "Anything on 11 and 12 November, during the Leaders Summit window.",
                "Late-notice changes to a confirmed group booking, which are much harder in November than in any other month.",
            ]),
            para(
                "If your programme includes hosted dining, treat it as a booking problem to be "
                "solved in advance rather than a decision to be made on the day."
            ),
        ),
        section(
            "Dining Formats for a Delegation",
            cards([
                ("Business dinner", "Small numbers, a quiet table or private room, and a location that does not consume the evening in transport."),
                ("Delegation dinner", "A larger group, usually with a host, seating plan and sometimes remarks — which changes the venue requirement entirely."),
                ("Bilateral lunch or dinner", "Two delegations, privacy, discretion and an interpreter where needed — see " + A("/cop31-interpreters/", "interpreters") + "."),
                ("Side-event dinner", "A dinner attached to a programme item, needing AV, a backdrop and a run of show — see " + A("/cop31-event-production/", "event production") + "."),
                ("Reception", "Standing format, higher numbers, hospitality equipment and staff rather than a seating plan."),
                ("Team dinner", "Crew and staff after a build day — simple, close to the hotel, and genuinely appreciated."),
            ]),
        ),
        section(
            "Need a Group Dinner or Private Event?",
            lede(
                "We handle the booking, the negotiation, the menu, the transport and the "
                "on-the-night coordination as one scope rather than leaving you to assemble it "
                "across a language barrier and a time zone."
            ),
            steps([
                ("Tell us the shape", "Numbers, date, area, format, budget guidance, whether you need privacy and whether there will be remarks."),
                ("Options with trade-offs", "Two or three realistic venues, with the transport and timing implications of each stated."),
                ("Booking and menu", "Reservation held, menu agreed, dietary requirements captured, deposit terms set out in writing."),
                ("Transport and timing", "Vehicles planned around the evening rather than booked separately — see " + A("/cop31-private-transfers/", "private transfers") + "."),
                ("On the night", "A local contact present for anything that needs handling, from a late guest to a changed seating plan."),
            ]),
            BACK,
        ),
    ],
    "cta_services": L(
        "/cop31-event-services/", "/cop31-private-transfers/", "/cop31-event-production/",
        "/cop31-hostess-staff/", "/cop31-interpreters/", "/cop31-antalya-accommodation/",
        "/cop31-branding-signage/",
    ),
    "cta_heading": "Need a Group Dinner or Private Event?",
    "faqs": [
        ("Where should we host a business dinner during COP31?",
         "Lara and the city centre suit smaller business dinners; Belek and Kundu work well for groups already staying there. Factor transport time into the evening — a distant restaurant turns a two-hour dinner into a four-hour commitment."),
        ("Can you arrange private dining rooms in Antalya?",
         "Yes. Private rooms are among the first things to go during the conference fortnight, so early booking makes a real difference."),
        ("How far in advance should we book a delegation dinner?",
         "As early as the date is known, particularly for 11–12 November during the Leaders Summit window, when demand peaks across the whole region."),
        ("Can you handle a dinner with speeches and AV?",
         "Yes. A dinner with a run of show, a backdrop, sound and screens is an event rather than a reservation, and is scoped with our event production team."),
        ("Can you arrange transport to and from a dinner?",
         "Yes, and it should be planned together with the booking. Vehicles arranged around the evening rather than separately is what keeps the schedule intact."),
        ("Can you accommodate dietary requirements?",
         "Yes. Dietary requirements are captured at booking and confirmed with the venue in advance rather than raised on the night."),
        ("Do you cover restaurants near the venue?",
         "Standalone dining in the immediate venue area is limited. Most delegation dining happens in Lara, Kundu, Belek or the city centre, or in the hotels themselves."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-participant-guide/", "/cop31-antalya-hotels/",
        "/cop31-antalya-accommodation/", "/cop31-private-transfers/", "/cop31-event-services/",
        "/cop31-event-production/", "/cop31-interpreters/",
    ),
}

PAGES = [REGISTRATION, EXPO, RESTAURANTS]
