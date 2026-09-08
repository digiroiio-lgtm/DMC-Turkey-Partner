# -*- coding: utf-8 -*-
"""Answer capsules: the direct answer each page owes its reader, up front.

The COP31 generator has carried this pattern since it was built — a short,
self-contained paragraph immediately under the <h1>, marked in
tools/cop31_render.py as being "for AI/AEO surfaces". It renders on 30 pages.
Nothing else on the site had one, so on the other ~107 pages the first thing a
reader or an extractive engine met was a marketing lede.

A capsule earns its place only if it says something the lede does not. It
should answer the question the page title implies, in two or three sentences,
with the specifics — who it is for, what is and is not included, the
constraint that actually matters. Restating the lede in different words makes
the page longer and no clearer, which is why this is a hand-written registry
rather than something derived: the text does not exist anywhere on the page,
so there is nothing to derive it from.

Every claim here has to be supported by the page it sits on. Nothing may
assert a certification, a client relationship, a price or a guarantee that the
page itself does not already make.

Keyed by URL path. A page with no entry simply gets no capsule.
"""

ANSWERS = {
    # --- Solutions -----------------------------------------------------------
    "/": (
        "DMC Turkey Partner is a Türkiye-based destination management company "
        "that international agencies, MICE planners and corporate event teams "
        "use as their local execution layer. You keep the client and the "
        "creative direction; we handle hotels, venues, transport, production, "
        "staffing and on-site delivery on the ground."
    ),
    "/dmc-turkey/": (
        "A DMC in Türkiye is the local partner that turns a programme designed "
        "abroad into something that actually runs on the ground: contracted "
        "hotels, vetted suppliers, transport, permits, staffing and a single "
        "point of coordination during the event. We work as that layer for "
        "agencies and corporate teams, across Istanbul, Antalya, Belek, Bodrum "
        "and Cappadocia."
    ),
    "/white-label-dmc-turkey/": (
        "White-label means we operate under your brand and never approach your "
        "client. You keep the relationship, the pricing and the creative; we "
        "supply the Türkiye ground operation, and appear as your local team on "
        "site if that is how you want it presented."
    ),
    "/mice-turkey/": (
        "MICE work in Türkiye covers meetings, incentives, conferences and "
        "exhibitions. What varies most by destination is meeting capacity and "
        "airlift: Istanbul suits congresses and city programmes, while Antalya "
        "and Belek suit resort-based conferences and incentives where the whole "
        "group stays in one property."
    ),
    "/incentive-travel-turkey/": (
        "An incentive programme in Türkiye is built around a resort base plus "
        "experiences that could not be bought individually — private venues, "
        "closed sites, gala production. We handle the sourcing, the logistics "
        "between elements, and the delivery, so the reward reads as designed "
        "rather than assembled."
    ),
    "/corporate-events-turkey/": (
        "Corporate events here span conferences, product launches, dealer "
        "meetings, retreats and anniversaries. The local work is the same "
        "shape each time: venue and hotel contracting, technical production, "
        "transport, staffing and a single coordinator who owns delivery on the "
        "day."
    ),
    "/group-travel-turkey/": (
        "Group travel operations means the ground layer under a tour or "
        "corporate group: transfers, coaches, guides, hotel coordination and "
        "itinerary logistics. Tour operators and agencies use us where they "
        "have the booking but not a local operation to run it."
    ),
    "/why-turkey/": (
        "Türkiye competes on cost per delegate, direct airlift from most of "
        "Europe and the Gulf, and resort properties large enough to hold a "
        "whole programme in one place. The trade-off is that quality varies "
        "sharply by supplier, which is what a local partner is for."
    ),
    # --- Services ------------------------------------------------------------
    "/services/": (
        "We cover the operational side of a programme in Türkiye: hotel "
        "sourcing, venue sourcing, transportation and logistics, event "
        "production, meetings and conferences, incentive programmes, group "
        "travel operations and ground handling. Most clients use several "
        "together under one point of coordination rather than buying them "
        "separately."
    ),
    "/services/hotel-sourcing/": (
        "Hotel sourcing is more than a rate request. It means matching meeting "
        "space, room block, board basis and transfer time to the programme, "
        "then holding the contract terms — release dates, attrition, payment "
        "schedule — that decide what the booking actually costs you later."
    ),
    "/services/venue-sourcing/": (
        "Venue sourcing covers conference centres, hotel ballrooms, historic "
        "and unusual sites, and outdoor spaces. The constraints that decide "
        "the shortlist are usually capacity in the room set you need, load-in "
        "access for production, and whether the site permits the event you "
        "have in mind."
    ),
    "/services/transportation-logistics/": (
        "Group transport covers airport transfers, inter-city coaching, "
        "shuttle loops and VIP vehicles, with the schedule built around flight "
        "manifests rather than a fixed timetable. Equipment and freight "
        "movements are planned alongside passengers, not separately."
    ),
    "/services/event-production/": (
        "Event production covers stage, set, lighting, audio, video, rigging "
        "and simultaneous interpretation, coordinated as one technical process "
        "rather than as separate suppliers. Design, build and on-site "
        "operation stay with the same team."
    ),
    "/services/meetings-conferences/": (
        "Conference support runs from venue and room-set planning through AV, "
        "signage, registration and delegate flow to on-site coordination. For "
        "multi-stream programmes the limiting factor is usually breakout "
        "capacity and turnaround time between sessions, not the plenary."
    ),
    "/services/incentive-programs/": (
        "Incentive delivery covers the resort base, the experiences, the "
        "transport between them and the gala or closing event. The work that "
        "matters is sequencing: keeping a large group moving without dead time "
        "while the next element is being set."
    ),
    "/services/group-travel/": (
        "Group operations handle arrivals and departures, rooming, transport, "
        "guiding and the daily itinerary for groups travelling together. It is "
        "the layer that absorbs the changes — a delayed flight, a split "
        "manifest — without the programme losing shape."
    ),
    "/services/ground-handling/": (
        "Ground handling is the arrival-to-departure layer: meet and greet, "
        "transfers, hotel and supplier coordination, and a local contact "
        "reachable during the programme. Agencies use it where they need "
        "presence on the ground without contracting each supplier themselves."
    ),
    # --- Destinations --------------------------------------------------------
    "/destinations/": (
        "We operate across Istanbul, Antalya, Belek, Bodrum and Cappadocia. "
        "Istanbul suits congresses and city programmes, Antalya and Belek suit "
        "resort-based conferences and incentives, Bodrum suits smaller premium "
        "groups, and Cappadocia works as an experience leg rather than a "
        "conference base."
    ),
    "/destinations/istanbul/": (
        "Istanbul is the choice for congresses, city-based corporate "
        "programmes and anything needing wide international airlift. It has "
        "the largest venue capacity in Türkiye, and its main constraint is "
        "traffic: transfer times, not distances, drive the schedule."
    ),
    "/destinations/antalya/": (
        "Antalya suits resort-led conferences and incentives where the whole "
        "group stays in one property. Large all-inclusive resorts with their "
        "own meeting space remove most internal transport, and the airport is "
        "close enough that arrival day stays usable."
    ),
    "/destinations/belek/": (
        "Belek is a concentrated strip of large five-star resorts with "
        "conference facilities and golf, about 30 minutes from Antalya "
        "airport. It works when you want a self-contained programme with "
        "several hotels close enough to share transport and venues."
    ),
    "/destinations/bodrum/": (
        "Bodrum suits smaller premium incentives and executive programmes "
        "rather than large conferences. Properties are more design-led and "
        "more spread out, so transport planning matters more than it does in "
        "Belek."
    ),
    "/destinations/izmir/": (
        "Izmir is T\u00fcrkiye's third city and the gateway to the Aegean coast. "
        "It suits mid-sized conferences and dealer meetings that want a real "
        "city without Istanbul's scale and traffic, and it is the arrival "
        "point for programmes running at Cesme, Alacati or Kusadasi."
    ),
    "/destinations/cappadocia/": (
        "Cappadocia is an experience destination, not a conference base. It "
        "works best as a two- or three-night leg inside a longer programme, "
        "where the landscape, cave hotels and balloon flights are the point."
    ),
    # --- Event costs ---------------------------------------------------------
    "/event-costs/": (
        "These are indicative planning ranges for corporate events, incentives "
        "and conferences in Türkiye, built from observable market benchmarks "
        "rather than from supplier net rates. They are for shaping a budget "
        "before a brief exists. They are not quotations and are not binding."
    ),
    "/event-cost-calculator/": (
        "The calculator gives an indicative budget range from destination, "
        "group size, duration and programme type. It uses the same benchmark "
        "assumptions as the published cost guides, so it is a planning "
        "starting point rather than a quotation."
    ),
    # --- Evidence and company ------------------------------------------------
    "/selected-works/": (
        "These are programmes we have delivered in Türkiye — corporate events, "
        "congresses, dealer meetings, launches and productions — listed with "
        "the venue, the destination and the scope we handled on each."
    ),
    "/events/": (
        "An independent calendar of the international MICE, business travel "
        "and corporate event trade shows, with dates, venues and cities. It is "
        "a planning reference; we are not an organiser of any event listed."
    ),
    "/about/": (
        "We have operated since 2006, combining event production, DMC "
        "operations, technical production, creative services and field "
        "execution in one structure. That means a single team carries a "
        "programme from brief through build to on-site delivery."
    ),
    "/contact/": (
        "Send the destination, dates, group size and what you need executed. "
        "We come back with the local operating scope and next steps. For a "
        "priced proposal use the proposal form; for a partnership discussion "
        "email the team directly."
    ),
    "/agency-partners/": (
        "Agencies work with us as a subcontracted local partner: you keep the "
        "client, the creative and the margin, and we execute in Türkiye under "
        "your brand. Most partnerships start with one programme and continue "
        "as a standing arrangement."
    ),
    "/request-proposal/": (
        "A proposal needs the destination, the dates, the group size and the "
        "programme type. Anything else — hotel standard, meeting requirements, "
        "transport, production, budget parameters — sharpens the scope, but we "
        "can start without it."
    ),
    "/guides/": (
        "Planning references for running meetings, incentives and corporate "
        "events in Türkiye: how destinations differ, what drives cost, and "
        "what a local operation actually covers."
    ),
    "/insights/": (
        "A starting point into the planning material on this site — "
        "destination comparisons, cost guides and the Türkiye MICE guide — "
        "rather than an editorial archive."
    ),
}
