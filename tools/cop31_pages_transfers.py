# -*- coding: utf-8 -*-
"""Commercial transport pages: airport transfers and private transfers."""

from cop31_links import A, L
from cop31_render import cards, checklist, lede, para, plain_list, section, steps, table

BACK = para(
    "This page is part of the "
    + A("/cop31-antalya/", "COP31 Antalya 2026 guide and services hub")
    + ". For how official shuttles and general movement work, see the "
    + A("/cop31-antalya-transport/", "COP31 transport guide") + "."
)

TRANSPORT_CTA = L(
    "/cop31-private-transfers/", "/cop31-antalya-airport-transfer/", "/cop31-event-services/",
    "/cop31-antalya-accommodation/", "/cop31-event-staff/", "/cop31-antalya-restaurants/",
    "/cop31-last-minute-services/",
)


AIRPORT = {
    "slug": "cop31-antalya-airport-transfer",
    "breadcrumb": "Airport Transfers",
    "title": "COP31 Antalya Airport Transfers | Private &amp; Group Arrivals 2026",
    "description": (
        "COP31 Antalya airport transfers: private and group transport between Antalya "
        "Airport, hotels and the venue. VIP vehicles, minivans, minibuses, coaches, "
        "meet-and-greet and group arrival coordination for November 2026."
    ),
    "h1": "COP31 Antalya Airport Transfers",
    "answer": (
        "We provide private and group airport transfers in Antalya for COP31 — airport to "
        "hotel, airport to venue and hotel to venue — with VIP vehicles, minivans, minibuses, "
        "coaches, meet-and-greet and coordinated group arrivals."
    ),
    "lede": (
        "Arrivals for COP31 concentrate into a few days at a single airport. Pre-booked "
        "transfers, staged group arrivals and a meet-and-greet point are what keep that from "
        "becoming the first problem of your trip."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Airport Transfer",
    "service_name": "COP31 Antalya Airport Transfers",
    "cta_label": "Request Airport Transfer",
    "wa_label": "WhatsApp Operations Desk",
    "wa_message": "COP31 Antalya airport transfer request. Flight, date, passengers and destination:",
    "sources": ["ifp", "tr"],
    "sections": [
        section(
            "Routes We Cover",
            cards([
                ("Airport → hotel", "The standard arrival: met at arrivals, luggage handled, direct to your hotel in Aksu, Lara, Kundu, Belek, the city centre or Konyaaltı."),
                ("Airport → venue", "Direct to the Antalya EXPO Center for arrivals timed against a session or a build slot."),
                ("Hotel → venue", "Scheduled or on-demand movement between accommodation and the venue during the conference."),
                ("Hotel → airport", "Departures, which concentrate as heavily as arrivals around 20 November."),
                ("Inter-hotel and off-site", "Movement between delegation hotels, side-event venues and dinner locations."),
            ]),
        ),
        section(
            "Vehicle Types",
            table(
                "Choosing a vehicle for a COP31 arrival",
                ["Vehicle", "Typical capacity", "Suits"],
                [
                    ["VIP sedan", "Up to 3 passengers with luggage", "Executives, principals, delegation heads"],
                    ["Minivan", "Up to about 6 passengers", "Small teams, or 2–3 people with equipment"],
                    ["Minibus", "Roughly 10–20 passengers", "Delegations arriving together, crew teams"],
                    ["Coach", "25+ passengers", "Large group arrivals and repeating hotel–venue runs"],
                    ["Cargo van", "Equipment rather than people", "Stand elements, AV cases, print deliveries"],
                ],
            ),
            para(
                "Size to the real load — passengers plus luggage plus materials. Teams "
                "travelling with cases, screens or stand elements routinely book by headcount "
                "and then need a second vehicle at the kerb."
            ),
        ),
        section(
            "Meet &amp; Greet and Group Arrivals",
            lede(
                "For a delegation arriving across several flights, the arrival plan matters "
                "more than the vehicles."
            ),
            steps([
                ("Send the flight list", "Flight numbers, arrival times, passenger counts and luggage expectations for each."),
                ("We build the arrival plan", "A meeting point, staff on the ground, and vehicles staged rather than all waiting at once."),
                ("Meet and greet", "Named greeter at arrivals, luggage assistance, and a holding point for early arrivals waiting on a later flight."),
                ("Consolidated or individual departure", "Groups combined where flights are close together, split where they are not."),
                ("Live handling of delays", "Flight monitoring so a delayed arrival does not mean a vehicle that has already left."),
            ]),
            para(
                "For movement throughout the conference rather than arrivals alone, see "
                + A("/cop31-private-transfers/", "COP31 private transfers") + "."
            ),
        ),
        section(
            "Booking Notes",
            checklist([
                "Book arrival and departure together — 20 November and the following day are as concentrated as the pre-conference days.",
                "Send flight numbers rather than times, so delays can be tracked.",
                "Say if anyone is travelling with equipment, and roughly how much.",
                "Confirm the exact hotel, not just the area — the Lara–Belek corridor is long.",
                "For late-night arrivals, confirm the arrangement explicitly rather than assuming coverage.",
                "Tell us if a principal needs a discreet arrival, which changes the vehicle and the meeting point.",
            ]),
            BACK,
        ),
    ],
    "cta_services": TRANSPORT_CTA,
    "cta_heading": "Arriving in Antalya for COP31?",
    "cta_copy": (
        "Send your flight details, passenger numbers and destination and we will confirm "
        "vehicles and an arrival plan."
    ),
    "faqs": [
        ("Do you provide airport transfers for COP31?",
         "Yes — private and group transfers between Antalya Airport, hotels and the Antalya EXPO Center, with VIP vehicles, minivans, minibuses and coaches."),
        ("How far is Antalya Airport from the COP31 venue?",
         "The Antalya EXPO Center sits on the airport side of the city, a short drive from the terminal. Journey time during the conference depends more on departure timing and traffic management than on distance."),
        ("Can you meet a delegation arriving on several flights?",
         "Yes. Send the flight list and we will build an arrival plan with a meeting point, staged vehicles and a greeter, rather than booking each flight separately."),
        ("Do you monitor flight delays?",
         "Yes, when you provide flight numbers. That is why we ask for flight numbers rather than scheduled times."),
        ("Can you transport equipment as well as passengers?",
         "Yes. Cargo vans and larger vehicles can be included for stand elements, AV cases and materials — tell us the volume rather than the headcount."),
        ("Is this the same as the official COP31 shuttle?",
         "No. Complimentary official shuttles are operated under the official COP31 arrangements. We provide independent private and group transport, which is what participants staying outside the official accommodation platform generally need."),
        ("How early should we book?",
         "As early as your flights are confirmed. Vehicles and drivers across the arrival peak are a finite local pool."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-transport/", "/cop31-private-transfers/",
        "/cop31-antalya-hotels/", "/cop31-antalya-accommodation/",
        "/cop31-antalya-participant-guide/", "/cop31-antalya-venue/",
    ),
}


PRIVATE = {
    "slug": "cop31-private-transfers",
    "breadcrumb": "Private Transfers",
    "title": "COP31 Private Transfers in Antalya | Delegation Transport 2026",
    "description": (
        "COP31 private transfers in Antalya: chauffeured VIP vehicles, vans, minibuses and "
        "coaches for delegation movement, hotel-to-venue runs, executive dinners, side events "
        "and hourly disposal during November 2026."
    ),
    "h1": "COP31 Private Transfers in Antalya",
    "answer": (
        "We provide chauffeured private transport in Antalya throughout COP31 — VIP vehicles, "
        "vans, minibuses and coaches on transfer or hourly disposal — for delegation "
        "movements, hotel-to-venue runs, executive dinners and side events."
    ),
    "lede": (
        "Dedicated vehicles and drivers for the conference period, not just for arrivals. For "
        "delegations and executives whose day contains fixed appointments, this is the "
        "difference between a schedule and a hope."
    ),
    "page_type": "commercial",
    "service_interest": "COP31 Private Transfers",
    "service_name": "COP31 Private Transfers in Antalya",
    "cta_label": "Request Private Transport",
    "wa_message": "COP31 Antalya private transport request. Dates, group size and pattern:",
    "sources": ["ifp"],
    "sections": [
        section(
            "What We Provide",
            cards([
                ("Chauffeured vehicles", "Professional drivers with local knowledge of the Aksu, Lara, Kundu, Belek and city routes, and of how they behave under conference traffic management."),
                ("VIP vehicles", "Executive sedans and premium vehicles for principals, heads of delegation and senior guests."),
                ("Vans and minivans", "Small groups, working teams and passengers travelling with equipment."),
                ("Minibuses", "Delegations of roughly 10–20 moving together on a repeating pattern."),
                ("Coaches", "Larger groups and scheduled hotel–venue services run for your own delegation."),
                ("Hourly disposal", "A vehicle and driver assigned to you for a block of hours or a full day, absorbing schedule changes rather than breaking under them."),
                ("Hotel ↔ venue runs", "Scheduled daily movement between your accommodation and the Antalya EXPO Center."),
                ("Delegation movements", "Coordinated multi-vehicle movement for a group with different schedules."),
                ("Executive dinners and side events", "Evening movement to restaurants, receptions and off-site venues — see " + A("/cop31-antalya-restaurants/", "restaurants and private dining") + "."),
            ]),
        ),
        section(
            "Transfer or Disposal?",
            lede(
                "The single most consequential booking decision, and the one most often got "
                "wrong."
            ),
            table(
                "Per-journey transfers vs hourly disposal",
                ["", "Per-journey transfer", "Hourly / daily disposal"],
                [
                    ["How it works", "A vehicle booked for a specific A→B movement", "A vehicle and driver assigned to you for a period"],
                    ["Best for", "Predictable, well-spaced movements", "Dense schedules, bilaterals, press, anything that shifts"],
                    ["When the schedule slips", "The booking is wasted; a new vehicle must be found", "The driver waits; the day continues"],
                    ["Cost per journey", "Lower", "Higher"],
                    ["Cost per problem", "High — a missed meeting costs more than a vehicle", "Low"],
                    ["Typical COP31 use", "Arrivals, departures, one-off evening movements", "Delegation days, Leaders Summit window, executive programmes"],
                ],
            ),
            para(
                "Most delegations end up with a mix: disposal vehicles for principals and dense "
                "days, transfers for everything predictable. We will propose a pattern from "
                "your schedule rather than sell you the more expensive option by default."
            ),
        ),
        section(
            "Planning Transport for the Conference Period",
            checklist([
                "Plan 11–12 November separately. The Leaders Summit window has the heaviest traffic management and the tightest vehicle availability of the fortnight.",
                "Book the whole period rather than day by day — driver continuity is worth a great deal by day five.",
                "Give the driver the day's plan, not just the next journey. Drivers who know the shape of the day handle changes far better.",
                "Confirm set-down and pick-up points, particularly at the venue where access is controlled.",
                "Allow real buffers for fixed appointments. Journey time is governed by departure timing, not distance.",
                "Name one coordinator on your side, so vehicles are not being redirected by several people at once.",
            ]),
            para(
                "For arrivals and departures specifically, see "
                + A("/cop31-antalya-airport-transfer/", "COP31 airport transfers")
                + ". For how official shuttles fit alongside private vehicles, see the "
                + A("/cop31-antalya-transport/", "transport guide") + "."
            ),
            BACK,
        ),
    ],
    "cta_services": TRANSPORT_CTA,
    "cta_heading": "Need Dedicated Vehicles for COP31?",
    "faqs": [
        ("What private transport do you offer for COP31?",
         "Chauffeured VIP vehicles, vans, minivans, minibuses and coaches, on per-journey transfer or hourly and daily disposal, for delegation movement, hotel–venue runs, executive dinners and side events."),
        ("What is hourly disposal?",
         "A vehicle and driver assigned to you for a block of hours or a full day. The driver waits between movements, so a schedule change costs nothing rather than requiring a new booking."),
        ("Should we book transfers or disposal?",
         "Transfers for predictable, well-spaced movements; disposal for dense schedules, bilaterals, press commitments and anything that shifts. Most delegations use both."),
        ("Can you provide vehicles for the whole conference?",
         "Yes. Booking for the full period also gives you driver continuity, which is worth more than it sounds by the middle of the fortnight."),
        ("Which days are hardest for vehicles?",
         "11–12 November, during the World Leaders Climate Action Summit, when demand, security measures and traffic management all peak simultaneously."),
        ("Do your drivers speak English?",
         "English-speaking drivers can be requested and are the norm for delegation work. For meetings rather than movement, see our interpreters page."),
        ("Can we add a vehicle during the conference?",
         "Often yes, subject to what remains available at the time. It is materially easier if we are already running vehicles for you."),
    ],
    "related": L(
        "/cop31-antalya/", "/cop31-antalya-transport/", "/cop31-antalya-airport-transfer/",
        "/cop31-antalya-accommodation/", "/cop31-antalya-restaurants/",
        "/cop31-event-services/", "/cop31-antalya-participant-guide/", "/cop31-interpreters/",
    ),
}

PAGES = [AIRPORT, PRIVATE]
