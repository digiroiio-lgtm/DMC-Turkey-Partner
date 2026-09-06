# -*- coding: utf-8 -*-
"""COP31 venue pages and the official programme summary."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, section, steps, table

INFO_CTA = L(
    "/cop31-exhibition-services/", "/cop31-pavilion-services/", "/cop31-exhibition-stands/",
    "/cop31-event-production/", "/cop31-av-equipment-rental/", "/cop31-furniture-rental/",
    "/cop31-printing-services/",
)


VENUE = {
    "slug": "cop31-antalya-venue",
    "breadcrumb": "Venue &amp; Location",
    "title": "COP31 Antalya Venue 2026 | Antalya EXPO Center Location &amp; Access",
    "description": (
        "COP31 2026 takes place at the Antalya EXPO Center in Antalya, Türkiye. Venue "
        "location, airport access, surrounding areas, transport overview and logistics "
        "considerations for delegations and exhibitors."
    ),
    "h1": "COP31 Antalya Venue – Location &amp; Visitor Guide",
    "answer": (
        "COP31 takes place at the Antalya EXPO Center in Antalya, Türkiye, from 9 to 20 "
        "November 2026. The venue sits east of Antalya city centre, close to Antalya Airport."
    ),
    "lede": (
        "Where the COP31 venue is, how participants reach it, what surrounds it, and what its "
        "location means for accommodation, movement and exhibitor logistics."
    ),
    "hero_facts": [
        ("Venue", "Antalya EXPO Center"),
        ("City", "Antalya, Türkiye"),
        ("Nearest airport", "Antalya Airport (AYT)"),
        ("Conference dates", "9–20 November 2026"),
    ],
    "page_type": "informational",
    "service_interest": "COP31 Venue &amp; Exhibitor Support",
    "service_name": "COP31 Antalya Venue Support",
    "update_sensitive": False,
    "sources": ["ifp", "unfccc", "tr"],
    "sections": [
        section(
            "Where the COP31 Venue Is",
            lede(
                "UNFCCC identifies the Antalya EXPO Center as the COP31 venue. It sits east of "
                "Antalya city centre, in the Aksu area, on the side of the city closest to "
                "Antalya Airport and to the Lara–Kundu–Belek resort corridor."
            ),
            para(
                "That position is unusually convenient for a conference of this size. Arrivals "
                "come through one airport a short drive away; the bulk of large-format hotel "
                "capacity is on the same side of the city; and the venue is not embedded in the "
                "urban core, so vehicle access and load-in are not fighting city-centre traffic "
                "patterns."
            ),
            para(
                "The trade-off is concentration. Nearly everyone attending will use the same "
                "corridor between the same hotel belt and the same venue, at the same two times "
                "a day. Journey time is therefore governed by departure time, not by distance."
            ),
        ),
        section(
            "Getting There from Antalya Airport",
            lede(
                "Antalya Airport (AYT) is the practical arrival point for COP31 and is a short "
                "drive from the venue and from most delegation accommodation."
            ),
            checklist([
                "Arrivals concentrate in the days immediately before 9 November — pre-book transfers rather than queueing on arrival.",
                "Delegations arriving on multiple flights are easier to handle with a meet-and-greet point and staged vehicles than with individual bookings.",
                "Crew and production teams arriving with cases, screens or stand elements need vehicle types that actually take the volume, not a standard sedan.",
                "Late-evening arrivals are common on the pre-conference days; confirm that your transfer arrangement covers them.",
            ]),
            para(
                "See " + A("/cop31-antalya-airport-transfer/", "COP31 Antalya airport transfers")
                + " for how arrivals are usually structured, and "
                + A("/cop31-antalya-transport/", "the transport guide")
                + " for shuttle and daily movement."
            ),
        ),
        section(
            "What Surrounds the Venue",
            table(
                "Areas around the COP31 venue",
                ["Area", "Relationship to the venue", "Useful for"],
                [
                    ["Aksu", "The venue's own district", "The shortest commute; limited hotel inventory"],
                    ["Antalya Airport", "A short drive west of the venue", "Arrivals, departures, crew movements, freight collection"],
                    ["Lara / Kundu", "The main resort corridor toward the city", "Delegation hotels with meeting space and event capacity"],
                    ["Belek", "East along the coast", "Large resorts and conference facilities for sizeable delegations"],
                    ["Antalya city centre / Konyaaltı", "West of the venue", "Restaurants, evening programmes, smaller city hotels"],
                ],
            ),
            para(
                "Accommodation choice within this map is the single biggest determinant of how "
                "your days run. The " + A("/cop31-antalya-hotels/", "COP31 hotels guide")
                + " works through each area in detail."
            ),
        ),
        section(
            "Logistics Considerations for Exhibitors and Delegations",
            lede(
                "Venue-specific rules — access times, build regulations, rigging, power, "
                "deliveries and stand approvals — are set by the venue and the conference "
                "organisers, and are issued to confirmed exhibitors. This page does not "
                "restate specifications we cannot verify. What follows is the operating "
                "context that applies regardless of the detail."
            ),
            cards([
                ("Build windows are short and shared",
                 "Every exhibitor and pavilion installs in the same compressed period before the opening. Materials that arrive late do not simply arrive later — they arrive into a queue."),
                ("Access is badge-controlled",
                 "Your delivery plan needs to name who physically carries what, and when. Couriers generally cannot reach a stand inside a controlled venue."),
                ("Local production beats international freight for the small stuff",
                 "Graphics, print, signage and furniture are faster and cheaper to produce in Antalya than to ship. Reserve freight for what genuinely cannot be made locally."),
                ("Plan a fallback before you need one",
                 "The teams that cope with a delayed shipment are the ones who identified a local production route in advance — see " + A("/cop31-last-minute-services/", "last-minute services") + "."),
                ("Storage matters more than people expect",
                 "Stock, giveaways, spare graphics and empty cases all need somewhere to live for two weeks. Plan it rather than discovering it on build day."),
                ("Dismantling is a real project",
                 "Removal, disposal, equipment return and freight collection after 20 November need the same planning as the build."),
            ]),
        ),
        section(
            "Exhibiting or Organising an Event at COP31?",
            lede(
                "If you are responsible for a physical presence at the venue or a programme "
                "around it, these are the relevant service pages."
            ),
            cards([
                ("Exhibition Services", "/cop31-exhibition-services/", "Setup, dismantling, graphics, furniture, AV, storage, logistics and on-site troubleshooting for exhibitors."),
                ("Pavilion Services", "/cop31-pavilion-services/", "Production, branding, hospitality, staffing and technical support for country and organisation pavilions."),
                ("Event Production", "/cop31-event-production/", "Staging, sound, screens, lighting and technical crew for side events and briefings."),
                ("AV &amp; Equipment Rental", "/cop31-av-equipment-rental/", "Screens, sound, microphones, presentation equipment and technicians."),
                ("Furniture Rental", "/cop31-furniture-rental/", "Exhibition, meeting, lounge and hospitality furniture delivered to your schedule."),
                ("Printing &amp; Collateral", "/cop31-printing-services/", "Local print production for stands, delegations and short-notice reprints."),
            ]),
        ),
    ],
    "cta_services": INFO_CTA,
    "cta_heading": "Exhibiting or Organising an Event at COP31?",
    "faqs": [
        ("Where is COP31 2026 being held?",
         "At the Antalya EXPO Center in Antalya, Türkiye, from 9 to 20 November 2026."),
        ("How far is the COP31 venue from Antalya Airport?",
         "The Antalya EXPO Center sits on the airport side of the city, a short drive from Antalya Airport. Confirm exact access routes and timings through the official participant information, since conference-period traffic management can change them."),
        ("Which areas are closest to the COP31 venue?",
         "The Aksu area around the venue is closest, followed by the Lara and Kundu resort corridor. Belek sits further east and Antalya city centre further west."),
        ("Can you deliver materials to our stand at the venue?",
         "We coordinate local production and delivery up to the point that venue access rules allow, and work with your accredited team for anything that has to be carried inside a controlled area."),
        ("Do you publish the venue's technical specifications?",
         "No. Stand regulations, rigging rules, power specifications and build schedules are issued by the venue and the conference organisers to confirmed exhibitors, and we do not restate figures we cannot verify."),
        ("Can you support a side event held outside the venue?",
         "Yes. Off-site side events, receptions, dinners and briefings across Antalya, Lara and Belek are a large part of the COP31 workload — see our event services and event production pages."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-expo-center/", "/cop31-antalya-participant-guide/",
        "/cop31-antalya-transport/", "/cop31-antalya-hotels/", "/cop31-exhibition-services/",
        "/cop31-pavilion-services/", "/cop31-event-production/", "/cop31-exhibition-stands/",
    ),
}


PROGRAMME = {
    "slug": "cop31-antalya-program",
    "breadcrumb": "Conference Programme",
    "title": "COP31 Antalya Programme 2026 | Key Dates &amp; Thematic Days",
    "description": (
        "A scannable summary of the COP31 Antalya 2026 programme: conference dates, the "
        "World Leaders Climate Action Summit, announced thematic days, and what each theme "
        "typically means for agency and delegation operations."
    ),
    "h1": "COP31 Antalya Programme 2026 – Key Dates &amp; Thematic Days",
    "answer": (
        "The COP31 programme runs across twelve days from 9 to 20 November 2026, with the "
        "World Leaders Climate Action Summit on 11–12 November and each conference day "
        "dedicated to a thematic priority announced by the COP31 Presidency."
    ),
    "lede": (
        "The official programme is published by the COP31 Presidency and UNFCCC. This page "
        "summarises its structure in a form that is easy to scan, then — kept clearly separate "
        "— sets out the operational requirements each kind of programme day tends to generate "
        "for agencies and delegations."
    ),
    "page_type": "informational",
    "service_interest": "COP31 Programme Support",
    "service_name": "COP31 Antalya Programme Support",
    "update_sensitive": True,
    "sources": ["programme", "tr", "unfccc", "ifp"],
    "sections": [
        section(
            "How the COP31 Programme Is Structured",
            lede(
                "The COP31 Presidency has built the public programme around thematic days — "
                "twelve conference days, each dedicated to a priority area of climate action — "
                "running alongside the formal negotiation programme. Finance, technology and "
                "capacity building are treated as horizontal enablers that run across all "
                "themes rather than as a single day."
            ),
            table(
                "Announced COP31 programme structure",
                ["Date", "Programme element"],
                [
                    ["9 November 2026", "Conference opens — Food, Agriculture and Health"],
                    ["10 November 2026", "Energy and Transport"],
                    ["11 November 2026", "Zero Waste, alongside World Leaders Climate Action Summit day 1"],
                    ["12 November 2026", "Resilient Cities and Built Environment, alongside World Leaders Climate Action Summit day 2"],
                    ["13–20 November 2026", "Remaining thematic days, including themes announced around green transformation, climate literacy and education, science and green industrialisation"],
                ],
            ),
            para(
                "The Presidency has confirmed the full twelve-day thematic sequence, and "
                "individual day assignments beyond the opening block continue to be published "
                "and refined. Rather than restate a schedule that may move, this page names "
                "what has been confirmed and points to the official programme for the rest. "
                "Check the official conference programme before fixing anything date-specific."
            ),
        ),
        section(
            "World Leaders Climate Action Summit",
            lede(
                "The World Leaders Climate Action Summit convenes on 11–12 November 2026, the "
                "third and fourth days of the conference, bringing together heads of state and "
                "government with leaders' roundtable sessions on themes including resilient "
                "cities, climate finance, decarbonisation, circular economy and blue climate "
                "action."
            ),
            para(
                "Operationally, this is the peak of the fortnight. Delegation sizes are at "
                "their largest, security and traffic management are at their tightest, media "
                "presence is heaviest, and the demand for vehicles, meeting space, interpreters "
                "and private dining is concentrated into 48 hours. Anything you need on those "
                "two days should be secured well before they arrive — this is the part of the "
                "programme where late booking genuinely fails."
            ),
        ),
        section(
            "What Programme Days Mean Operationally",
            lede(
                "The section below is our own commercial reading of the programme, not official "
                "COP31 information. It maps the kinds of activity a theme tends to attract onto "
                "the local services that support them."
            ),
            cards([
                ("Finance and trade activity",
                 "Executive meetings, bilaterals and private dinners dominate. The recurring needs are meeting rooms, discreet dining, interpreters and vehicles on disposal rather than per-journey transfers. See " + A("/cop31-antalya-restaurants/", "private dining") + " and " + A("/cop31-private-transfers/", "private transfers") + "."),
                ("Science, industry and technology activity",
                 "Demonstration-heavy. Screens, power, technical crew, exhibition production and interpretation carry the weight — see " + A("/cop31-av-equipment-rental/", "AV rental") + " and " + A("/cop31-event-production/", "event production") + "."),
                ("Energy, transport and industrial themes",
                 "Larger stands and pavilions, physical exhibits, heavier build requirements and more logistics around delivery and installation — see " + A("/cop31-exhibition-stands/", "exhibition stands") + "."),
                ("Cities, built environment and resilience themes",
                 "Model-based and visual displays, panel formats and city-delegation hospitality. Furniture, branding and hosting staff matter more than heavy production."),
                ("Food, agriculture and health themes",
                 "Tasting, sampling and hospitality formats appear here more than anywhere else, which means hospitality equipment, coffee stations, catering coordination and staff — see " + A("/cop31-coffee-machine-rental/", "coffee and hospitality equipment") + "."),
                ("Education, literacy and civil-society themes",
                 "High volume of printed material, giveaways and public-facing collateral, with reprint demand mid-conference — see " + A("/cop31-printing-services/", "printing services") + "."),
            ]),
        ),
        section(
            "Planning Around the Programme",
            steps([
                ("Identify your peak days",
                 "Map your own commitments onto the programme and find the two or three days where everything happens at once. Those are the days to over-resource."),
                ("Separate fixed from flexible",
                 "Anything tied to a specific hour — a bilateral, a press moment, a panel — needs dedicated transport and a fallback. Everything else can flex."),
                ("Book the scarce things first",
                 "Meeting rooms, interpreters, vehicles with drivers and private dining rooms are the constrained resources during the Leaders Summit window."),
                ("Plan restock, not just launch",
                 "Print, giveaways and hospitality supplies run out mid-conference. Decide in advance who reorders and from where."),
                ("Keep one local contact briefed",
                 "Programme changes are normal. A local operations contact who already knows your scope can absorb them without a new briefing each time."),
            ]),
        ),
    ],
    "cta_services": L(
        "/cop31-event-services/", "/cop31-event-production/", "/cop31-av-equipment-rental/",
        "/cop31-interpreters/", "/cop31-private-transfers/", "/cop31-printing-services/",
        "/cop31-last-minute-services/",
    ),
    "cta_heading": "Building a Programme Around COP31?",
    "faqs": [
        ("How long is the COP31 programme?",
         "Twelve conference days, from 9 to 20 November 2026, with each day dedicated to a thematic priority alongside the formal negotiation programme."),
        ("When is the COP31 World Leaders Climate Action Summit?",
         "11–12 November 2026, on the third and fourth days of the conference."),
        ("What are the COP31 thematic days?",
         "The Presidency has announced twelve thematic days. The programme opens on 9 November with Food, Agriculture and Health, followed by Energy and Transport on 10 November, Zero Waste on 11 November and Resilient Cities and Built Environment on 12 November, with further themes across the remaining days. The official conference programme is the authority on the full sequence."),
        ("Is the COP31 programme final?",
         "Programme detail continues to be published and refined by the Presidency. Confirm any date-specific commitment against the official conference programme rather than a summary."),
        ("Which programme days are hardest to resource locally?",
         "The Leaders Summit window on 11–12 November. Vehicles, meeting rooms, interpreters and private dining are all at peak demand across those two days."),
        ("Can you help build a side-event programme around the thematic days?",
         "Yes. Side events, receptions, briefings, dinners and meeting-room programmes around the official schedule are a core part of our COP31 event services."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-dates/", "/cop31-antalya-participant-guide/",
        "/cop31-antalya-venue/", "/cop31-event-services/", "/cop31-event-production/",
        "/cop31-interpreters/", "/cop31-private-transfers/", "/cop31-antalya-restaurants/",
    ),
}

PAGES = [VENUE, PROGRAMME]
