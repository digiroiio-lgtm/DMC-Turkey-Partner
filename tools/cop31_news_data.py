# -*- coding: utf-8 -*-
"""COP31 news layer: sources and articles.

EVERY article here is written from identified sources and attributes them. The
rules this file exists to enforce:

* No third-party text is reproduced. Sources are read, facts extracted and
  verified, then written fresh in our own words with our own practical context.
* Official bodies (UNFCCC, the COP31 Türkiye Presidency, Turkish ministries)
  outrank media for facts about dates, venue, registration, programme,
  transport and accommodation. Where a fact comes from regional media rather
  than an official body, the article says so in the body text.
* Our interpretation is always separated from the reported fact, so a reader
  can tell which is which.
* Nothing here may imply UNFCCC affiliation or official-provider status.

CATEGORIES maps to the hub filter. Each article declares the evergreen page it
feeds (`evergreen`) and only the commercial pages that genuinely fit the story.
"""

CATEGORIES = [
    ("venue", "Venue & EXPO"),
    ("programme", "Programme & Registration"),
    ("transport", "Transport & Infrastructure"),
    ("hotels", "Hotels & Accommodation"),
    ("pavilions", "Pavilions & Exhibitors"),
    ("side-events", "Side Events"),
    ("local", "Antalya Local Updates"),
]

# --- Sources ----------------------------------------------------------------
# (label, url, kind) — kind drives the "Official" badge in the sources block.
S = {
    "unfccc_ifp": ("UNFCCC — Information for COP31 Participants (A–Z)",
                   "https://unfccc.int/cop31/ifp", "official"),
    "unfccc_cop31": ("UNFCCC — COP31", "https://unfccc.int/cop31", "official"),
    "unfccc_road": ("UNFCCC — The Road to Antalya",
                    "https://unfccc.int/cop31/the-road-to-antalya", "official"),
    "unfccc_obs": ("UNFCCC — Observer Organizations",
                   "https://unfccc.int/cop31/observer-organizations", "official"),
    "tr_home": ("COP31 Türkiye — Official Website", "https://cop31.tr/", "official"),
    "tr_venue": ("COP31 Türkiye — Venue Map", "https://cop31.tr/venue", "official"),
    "tr_programme": ("COP31 Türkiye — Programme Overview",
                     "https://cop31.tr/programme-overview", "official"),
    "tr_thematic": ("COP31 Türkiye — Thematic Days",
                    "https://cop31.tr/thematic-days", "official"),
    "tr_thematic_news": ("COP31 Türkiye — “COP31 thematic days announced: 12 days, 12 priorities”",
                         "https://cop31.tr/news-detail/thematic-days-announced-2026", "official"),
    "tr_media_news": ("COP31 Türkiye — “Media registration for COP31 is now open”",
                      "https://cop31.tr/news-detail/media-registration-open-2026", "official"),
    "tr_accommodation": ("COP31 Türkiye — Accommodation",
                         "https://cop31.tr/accommodation", "official"),
    "tr_zones": ("COP31 Türkiye — The Difference Between the Green Zone and the Blue Zone",
                 "https://cop31.tr/blog/green-zone-vs-blue-zone", "official"),
    "tr_guide": ("COP31 Türkiye — When and Where Is COP31? A Participant Guide",
                 "https://cop31.tr/blog/when-and-where-is-cop31", "official"),
    "iklim_meeting": ("Republic of Türkiye, Ministry of Environment, Urbanisation and Climate Change — "
                      "“COP31 Hazırlık Toplantısı Antalya EXPO’da Düzenlendi”",
                      "https://iklim.gov.tr/cop31-hazirlik-toplantisi-antalya-expo-da-duzenlendi-haber-4754",
                      "official"),
    "unric": ("UN Regional Information Centre for Western Europe — UNFCCC: COP31, The Road to Antalya",
              "https://unric.org/en/unfccc-cop31-the-road-to-antalya/", "official"),
    "yenialanya_expo": ("Yeni Alanya — “Antalya EXPO alanı COP31 hazırlığına girdi”",
                        "https://www.yenialanya.com/antalyadaki-dev-expo-alani-cop31-zirvesine-hazirlaniyor",
                        "media"),
    "yenialanya_kurum": ("Yeni Alanya — “Antalya COP31’e hazırlanıyor: Kurum çalışmaları yerinde inceledi”",
                         "https://www.yenialanya.com/antalya-cop31e-hazirlaniyor-kurum-calismalari-yerinde-inceledi",
                         "media"),
    "yenialanya_roads": ("Yeni Alanya — “Antalya’da COP31 heyecanı: 38 kilometrelik yol hizmette!”",
                         "https://www.yenialanya.com/antalyada-cop31-heyecani-38-kilometrelik-yol-hizmette",
                         "media"),
    "korfez_expo": ("Antalya Körfez Gazetesi — “Murat Kurum açıkladı: Antalya’daki EXPO alanı COP31 sonrası ne olacak?”",
                    "https://www.antalyakorfez.com/murat-kurum-acikladi-antalyadaki-expo-alani-cop31-sonrasi-ne-olacak",
                    "media"),
    "istiklal_expo": ("İstiklal — “Bakan Kurum, Antalya EXPO Alanı’ndaki COP31 hazırlıklarını inceledi”",
                      "https://www.istiklal.com.tr/genel/bakan-kurum-antalya-expo-alanindaki-cop31-hazirliklarini-inceledi-1104335h",
                      "media"),
}


# --- Articles ---------------------------------------------------------------
# `summary`  : 2-3 original sentences — what happened, when, why it matters.
# `changed`  : the verified development, in our own words.
# `means`    : our practical reading for participants. Clearly our own, never
#              presented as reported fact.
# `evergreen`: (path, anchor text) pairs — the guides this story feeds.
# `services` : commercial pages only where they genuinely fit the story.

ARTICLES = [
    {
        "slug": "cop31-antalya-expo-preparations",
        "category": "venue",
        "title": "COP31 Antalya EXPO Preparations Advance Ahead of the November Conference",
        "seo_title": "COP31 Antalya EXPO Preparations Update | Venue Readiness 2026",
        "description": (
            "Renovation of the Antalya EXPO area, UN technical inspections and venue "
            "readiness ahead of COP31, with what the works mean for exhibitors, "
            "pavilion teams and delegations planning on-site operations."
        ),
        "published": "2026-09-06",
        "updated": "2026-09-06",
        "summary": (
            "Work to prepare the Antalya EXPO area for COP31 is well advanced, covering the "
            "congress centre, the EXPO tower, landscaping and site infrastructure. UN teams "
            "have carried out repeated technical inspections of the venue and the wider "
            "arrangements around it. For anyone building a stand, running a pavilion or "
            "planning delegation logistics, the practical takeaway is that the site is being "
            "handed over close to the conference, so build planning should assume a tight "
            "access window."
        ),
        "changed": [
            "The Ministry of Environment, Urbanisation and Climate Change has hosted COP31 "
            "preparation meetings at the Antalya EXPO site itself, with the venue treated as "
            "the working centre of the preparation programme.",
            "Turkish media covering the site report a large-scale renovation of the former "
            "EXPO 2016 grounds — the congress centre interior and seating, the EXPO tower and "
            "its surrounding walkways, landscaping and irrigation, and site infrastructure — "
            "carried out simultaneously by a substantial on-site workforce. Reported figures "
            "for the budget and headcount come from regional outlets rather than an official "
            "publication, so we have not repeated them as confirmed numbers.",
            "Regional coverage also describes technical inspections at the site by UNFCCC "
            "teams together with UN safety and security staff, assessing the venue alongside "
            "accommodation, transport and security arrangements for a very large "
            "participation volume.",
            "The official COP31 Türkiye website publishes a venue map for the site, which is "
            "the authoritative reference for how the grounds are laid out.",
        ],
        "means": [
            ("Assume a compressed build window",
             "A venue handed over close to the conference means exhibitor and pavilion access "
             "is likely to be tight and tightly scheduled. Build plans that depend on a long, "
             "flexible install period are the ones that fail; plans with a short critical path "
             "and locally sourced fallbacks are the ones that hold."),
            ("Treat official documentation as the only specification",
             "Renovation changes rooms, seating, access routes and technical provision. Any "
             "floor plan, capacity or rigging figure you are working from that predates the "
             "works may simply be wrong. Build only against the documentation issued to "
             "confirmed exhibitors."),
            ("Local production reduces your exposure",
             "The shorter the access window, the more expensive an international freight delay "
             "becomes. Graphics, print, signage and furniture produced in Antalya can be "
             "corrected or replaced during the conference; a crate stuck in transit cannot."),
            ("Expect movement restrictions around the site",
             "Security assessment at this scale usually results in controlled approaches and "
             "staged access. Deliveries, crew arrivals and vehicle movements should be planned "
             "around a controlled perimeter rather than kerbside access."),
        ],
        "evergreen": [
            ("/cop31-antalya-expo-center/", "COP31 Antalya EXPO Center guide"),
            ("/cop31-antalya-venue/", "COP31 venue and location guide"),
        ],
        "services": [
            ("/cop31-exhibition-services/", "Exhibition services"),
            ("/cop31-event-production/", "Event production"),
            ("/cop31-av-equipment-rental/", "AV equipment rental"),
        ],
        "sources": ["iklim_meeting", "tr_venue", "yenialanya_expo", "yenialanya_kurum",
                    "korfez_expo", "istiklal_expo"],
    },
    {
        "slug": "cop31-antalya-transport-infrastructure-update",
        "category": "transport",
        "title": "Antalya Opens New Road Links Ahead of COP31 — What It Changes for Delegations",
        "seo_title": "COP31 Antalya Transport & Road Infrastructure Update 2026",
        "description": (
            "New arterial and hotel connection roads, the Antray tram extension toward the "
            "EXPO area and the official COP31 shuttle arrangement — and what each means for "
            "delegation transport planning in Antalya."
        ),
        "published": "2026-09-06",
        "updated": "2026-09-06",
        "summary": (
            "Antalya has brought new road capacity into service as part of its COP31 "
            "preparations, alongside an existing rail link running toward the EXPO area and "
            "the airport. Complimentary official shuttles are expected to operate during the "
            "conference, but only from hotels on the official accommodation platform. For "
            "delegations, the useful conclusion is that access is improving while eligibility "
            "for the free shuttle still depends entirely on where you book."
        ),
        "changed": [
            "Regional coverage reports that roughly 38 kilometres of new road capacity has "
            "been put into service around Antalya for COP31, made up of several main arterial "
            "routes plus a set of hotel connection roads linking accommodation areas to the "
            "wider network.",
            "Antalya's Antray light-rail network already includes an extension running from "
            "the city toward the EXPO 2016 grounds, with a branch serving Antalya Airport.",
            "UNFCCC's participant information states that complimentary shuttle services will "
            "operate in the Antalya region during the conference, with shuttle stops at hotels "
            "listed on the official COP31 accommodation platform.",
            "The COP31 Türkiye Presidency has said dedicated hotel allocations and shuttle "
            "services are being arranged for accredited media.",
        ],
        "means": [
            ("Shuttle access follows the hotel, not the badge",
             "This is the single most consequential planning fact in the transport picture. A "
             "hotel booked outside the official platform may sit closer to the venue than one "
             "on it and still have no stop. Confirm eligibility before you confirm rooms."),
            ("New roads help capacity, not necessarily your timing",
             "Additional road capacity should ease the corridor overall. It does not remove "
             "the fact that the whole conference moves between the same hotel belt and the "
             "same venue at the same two times each day. Journey times on the peak days will "
             "still be governed by when you leave, and final timings should be checked closer "
             "to the event rather than assumed from these works."),
            ("Rail is useful for people, not for programmes",
             "The tram is a genuine asset for individual participants and evenings in the "
             "city. It is not a realistic way to move a delegation with luggage, equipment or "
             "a fixed appointment."),
            ("Plan 11–12 November separately",
             "The World Leaders Climate Action Summit falls on those two days. Security "
             "measures and traffic management around a leaders' segment routinely override "
             "normal routing, whatever the underlying road capacity."),
        ],
        "means_note": (
            "DmcTurkeyPartner is not part of the official COP31 shuttle operation. The "
            "services we provide are independent private and group transport, arranged "
            "separately from the official arrangements described above."
        ),
        "evergreen": [
            ("/cop31-antalya-transport/", "COP31 Antalya transport guide"),
            ("/cop31-antalya-hotels/", "COP31 hotels guide"),
        ],
        "services": [
            ("/cop31-private-transfers/", "Private transfers"),
            ("/cop31-antalya-airport-transfer/", "Antalya airport transfers"),
        ],
        "sources": ["unfccc_ifp", "tr_media_news", "yenialanya_roads", "tr_accommodation"],
    },
]

ARTICLES += [
    {
        "slug": "cop31-blue-zone-green-zone-exhibitor-guide",
        "category": "pavilions",
        "title": "COP31 Blue Zone and Green Zone: What the Split Means for Pavilions and Exhibitors",
        "seo_title": "COP31 Blue Zone vs Green Zone | Pavilion & Exhibitor Update 2026",
        "description": (
            "How the COP31 Blue Zone and Green Zone differ, what the Presidency's partnership "
            "and Türkiye Pavilion application rounds covered, and what the split means for "
            "organisations planning a physical presence in Antalya."
        ),
        "published": "2026-09-06",
        "updated": "2026-09-06",
        "summary": (
            "The COP31 Presidency has set out the distinction between the Blue Zone, where the "
            "formal negotiations take place, and the Green Zone, which is the conference's "
            "public-facing space. Application rounds for Green Zone partnerships and Türkiye "
            "Pavilion side events ran to a mid-August deadline. For organisations still "
            "planning a presence, which zone you are in determines your accreditation route, "
            "your audience and how your build has to be handled."
        ),
        "changed": [
            "The official COP31 Türkiye website explains the two-zone structure: the Blue Zone "
            "hosts the formal UNFCCC negotiation process and requires UNFCCC accreditation to "
            "enter, while the Green Zone is the publicly accessible side of the conference.",
            "Applications for Green Zone partnerships — covering panels, exhibition areas, "
            "thematic hubs and showcases — and for side events at the Türkiye Pavilion in the "
            "Blue Zone were opened by the Presidency with a deadline in mid-August 2026, "
            "publicised through Turkish diplomatic missions.",
            "Those application windows have now closed. Organisations that did not apply in "
            "that round are not, on the basis of the published information, able to submit "
            "through it now.",
        ],
        "means": [
            ("The zone decides the accreditation route",
             "A Blue Zone presence depends on UNFCCC accreditation held by your organisation, "
             "which no supplier can obtain for you. A Green Zone presence runs through the "
             "Presidency's own partnership process. Neither is something a build contractor "
             "can arrange, and any offer to sell you access should be treated with suspicion."),
            ("The zones attract different builds",
             "Blue Zone pavilions tend to be country delegations, UN and intergovernmental "
             "bodies and large NGO coalitions, and they operate as hosting spaces for twelve "
             "days. Green Zone space skews toward public-facing exhibits and corporate "
             "showcases. The first is a programme to run; the second is an audience to catch."),
            ("Access rules shape the build more than the design does",
             "In a badge-controlled area, the constraint is rarely the stand — it is who can "
             "physically carry what, and when. Decide early which of your own accredited "
             "people will move materials, because a contractor without a badge cannot."),
            ("If you missed the round, the side programme is still open",
             "Much of the commercially useful activity at any COP happens outside both zones — "
             "hotel meeting rooms, private venues, briefings and dinners along the Lara, Kundu "
             "and Belek corridor. That route needs no zone allocation at all."),
        ],
        "evergreen": [
            ("/cop31-antalya-participant-guide/", "COP31 participant guide"),
            ("/cop31-antalya-venue/", "COP31 venue and location guide"),
        ],
        "services": [
            ("/cop31-pavilion-services/", "Pavilion services"),
            ("/cop31-exhibition-services/", "Exhibition services"),
            ("/cop31-exhibition-stands/", "Exhibition stands"),
        ],
        "sources": ["tr_zones", "tr_home", "unfccc_ifp", "unfccc_obs"],
    },
    {
        "slug": "cop31-thematic-days-programme",
        "category": "programme",
        "title": "COP31 Antalya Thematic Days Programme Announced for November 2026",
        "seo_title": "COP31 Thematic Days Programme Announced | Antalya 2026 Update",
        "description": (
            "The COP31 Presidency has published a thematic day programme giving each "
            "conference day a priority area, alongside the World Leaders Climate Action "
            "Summit on 11–12 November 2026."
        ),
        "published": "2026-09-06",
        "updated": "2026-09-06",
        "summary": (
            "The COP31 Presidency has announced a thematic structure that gives each of the "
            "conference's twelve days a distinct climate priority. The programme opens on "
            "9 November with Food, Agriculture and Health, and the World Leaders Climate "
            "Action Summit convenes on 11–12 November. For agencies and delegations, the "
            "thematic calendar is the most useful planning tool published so far, because it "
            "indicates when your audience will actually be in the room."
        ),
        "changed": [
            "The Presidency has published the thematic day programme for COP31, with each of "
            "the twelve conference days dedicated to a distinct priority area of climate "
            "action.",
            "The announced opening sequence runs Food, Agriculture and Health on 9 November, "
            "followed by Energy and Transport on 10 November, with Zero Waste and Resilient "
            "Cities and Built Environment falling on 11 and 12 November.",
            "The World Leaders Climate Action Summit convenes on the third and fourth days of "
            "the conference, 11–12 November 2026, running alongside those themes.",
            "Finance, technology and capacity building are treated as cross-cutting enablers "
            "running through the whole programme rather than being given a single day.",
            "Separately, the Presidency has confirmed that media registration for COP31 is "
            "open through the UNFCCC Online Registration System.",
        ],
        "means": [
            ("Find your two or three real days",
             "Almost no organisation needs equal presence across twelve days. Map your "
             "objectives onto the themes, identify the days when the people you care about are "
             "in Antalya, and resource those days properly instead of spreading thinly."),
            ("The Leaders Summit window is the hard constraint",
             "11–12 November is when delegation sizes, security measures, media presence and "
             "demand for meeting rooms, interpreters, vehicles and private dining all peak "
             "together. Anything you need across those two days should already be held."),
            ("Different themes generate different operational needs",
             "This is our own reading rather than official guidance, but it holds across "
             "COPs: finance-weighted days drive meetings, bilaterals and private dining; "
             "industry and technology days drive demonstrations, screens and technical crew; "
             "public-facing days drive printed material and hospitality volume."),
            ("Confirm before you commit budget",
             "Programme detail is still being published and refined. Treat any summary, this "
             "one included, as a planning aid and check the official conference programme "
             "before fixing a date-specific spend."),
        ],
        "evergreen": [
            ("/cop31-antalya-program/", "COP31 Antalya programme guide"),
            ("/cop31-antalya-dates/", "COP31 dates and planning timeline"),
        ],
        "services": [
            ("/cop31-event-services/", "COP31 event services"),
            ("/cop31-interpreters/", "Interpreters and language support"),
        ],
        "sources": ["tr_thematic_news", "tr_thematic", "tr_programme", "tr_media_news",
                    "unfccc_cop31"],
    },
    {
        "slug": "cop31-antalya-hotels-accommodation-update",
        "category": "hotels",
        "title": "COP31 Antalya Accommodation: Official Platform, Shuttle Eligibility and Group Planning",
        "seo_title": "COP31 Antalya Hotels & Accommodation Update 2026",
        "description": (
            "How official COP31 accommodation works in Antalya, why shuttle access is tied to "
            "the official hotel list, and what delegations placing groups should settle before "
            "booking."
        ),
        "published": "2026-09-06",
        "updated": "2026-09-06",
        "summary": (
            "COP31 accommodation is being coordinated through an official platform, and "
            "UNFCCC has tied complimentary shuttle stops to the hotels listed on it. Antalya "
            "has substantial hotel capacity, but the rooms that matter for delegations — near "
            "the venue, in blocks, with meeting space — are a much smaller pool. The practical "
            "decision is not which hotel is nicest, but whether shuttle eligibility or group "
            "control matters more to you."
        ),
        "changed": [
            "The COP31 Türkiye Presidency publishes official accommodation information and "
            "directs participants to the official booking route for the conference.",
            "UNFCCC's participant information states that complimentary shuttle services will "
            "run in the Antalya region, with stops at hotels listed on the official COP31 "
            "accommodation platform.",
            "The Presidency has also indicated that dedicated hotel allocations and shuttle "
            "services are arranged for accredited media.",
            "Widely differing attendance estimates are circulating in commercial and media "
            "coverage. We have not repeated a figure here, because we could not verify one "
            "against an official publication.",
        ],
        "means": [
            ("Decide the trade-off consciously",
             "Booking on the official platform buys shuttle eligibility and simplicity. "
             "Booking independently buys control — blocks held together, meeting space, staff "
             "rooms at a different rate point — and costs you the free shuttle. Both are "
             "legitimate; picking by accident is not."),
            ("Meeting space is scarcer than bedrooms",
             "Delegations consistently underestimate this. A hotel that can sleep your group "
             "may have no room in which to brief them, and function space during the "
             "conference fortnight is committed well before bedroom inventory runs out."),
            ("Splitting a group doubles the transport plan",
             "Two hotels means two pickup patterns, two briefing points and two sets of "
             "things going wrong. If the group must split, split it by function rather than by "
             "whatever rooms were left."),
            ("Nothing is an official hotel unless the official list says so",
             "Treat any supplier describing a property as an official COP31 hotel with "
             "caution unless it appears on the official accommodation platform."),
        ],
        "evergreen": [
            ("/cop31-antalya-hotels/", "COP31 hotels guide"),
            ("/cop31-antalya-accommodation/", "COP31 group accommodation guide"),
        ],
        "services": [
            ("/cop31-antalya-accommodation/", "Delegation accommodation sourcing"),
            ("/cop31-private-transfers/", "Private transfers"),
        ],
        "sources": ["unfccc_ifp", "tr_accommodation", "tr_media_news", "tr_guide"],
    },
]
