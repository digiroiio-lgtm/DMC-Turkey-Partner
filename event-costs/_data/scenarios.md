# Event Costs — Scenario Data Model & Register

This file is the authoring source-of-truth for the `/event-costs/` system. It
is documentation, not a runtime data layer — the site has no CMS or build
step, so every published page is still a hand-authored static
`index.html` file under `/event-costs/`. This register exists so that:

1. Every published page has a clear, auditable set of underlying assumptions.
2. Future scenarios can be added consistently, without re-deriving the model.
3. `indexStatus` is tracked explicitly and centrally, so a scenario can never
   become indexable simply because a record exists here.

## Data model

Each scenario/hub record has the following fields:

| Field | Description |
| --- | --- |
| `slug` | URL path under `/event-costs/`. |
| `destination` | `antalya`, `istanbul`, `belek`, `cappadocia`, `bodrum`, or none (event-type hub / pillar). |
| `eventType` | `corporate-events`, `incentive-travel`, `conferences`, `corporate-retreats`, `product-launches`, `gala-dinners`, or none (destination hub / pillar). |
| `groupSize` | Integer guest count, or none (hub page). |
| `duration` | Nights, or none (hub page). |
| `hotelCategory` | e.g. `5-star all-inclusive resort`, `5-star city hotel`. |
| `roomConfiguration` | e.g. `twin/double occupancy`. |
| `programmeLevel` | `standard` or `premium`. |
| `meetingDays` | Number of business/plenary days, where relevant. |
| `budgetLow` / `budgetHigh` | Indicative total programme budget range (EUR). |
| `perGuestLow` / `perGuestHigh` | Indicative per-guest range (EUR). |
| `currency` | `EUR`. |
| `programmeSummary` | One-sentence scenario definition (used as the page lede). |
| `costBreakdown[]` | Category → approximate % share of total spend. |
| `priceDrivers[]` | What could change the budget. |
| `costReductionOptions[]` | What would reduce the budget. |
| `premiumUpgradeOptions[]` | What would make the programme more premium. |
| `relevantSelectedWorks[]` | 2–4 `/selected-works/` slugs shown on the page. |
| `seoTitle` | `<title>` / `og:title`. |
| `metaDescription` | `<meta name="description">`. |
| `h1` | Page H1 (must be unique across the whole `/event-costs/` set). |
| `intro` | Extended intro paragraph beyond `programmeSummary`, where used. |
| `lastReviewed` | `Month Year`, shown on-page and used to trigger content review. |
| `indexStatus` | `draft` \| `noindex` \| `index`. **Governs publication — see below.** |

## `indexStatus` rule (mandatory)

- `index` — page exists at its slug with full content, `robots: index, follow`,
  a self-referencing canonical, and **is** listed in `sitemap-event-costs.xml`.
- `noindex` — page may exist (e.g. for internal QA) but must carry
  `robots: noindex, follow` and **must not** be listed in
  `sitemap-event-costs.xml`.
- `draft` — record exists in this file only. **No `index.html` is created.**
  The URL does not exist yet.

A record moving from `draft`/`noindex` to `index` requires: (a) a defensible,
non-fabricated budget range with documented assumptions in `costBreakdown[]`
and the Programme Snapshot fields, and (b) — from Phase 2 onward — evidence
of search demand (see "Phase 2" below). A record must never be published
because it exists here; publication is a deliberate, separate action.

## Phase 1 register (12 approved, `indexStatus: index`)

| # | slug | destination | eventType | groupSize | budget (EUR) | last reviewed |
| - | --- | --- | --- | --- | --- | --- |
| 01 | `/event-costs/` | — | — (pillar) | — | — | September 2026 |
| 02 | `/event-costs/antalya/` | antalya | — (hub) | — | — | September 2026 |
| 03 | `/event-costs/istanbul/` | istanbul | — (hub) | — | — | September 2026 |
| 04 | `/event-costs/belek/` | belek | — (hub) | — | — | September 2026 |
| 05 | `/event-costs/corporate-events/` | — | corporate-events (hub) | — | — | September 2026 |
| 06 | `/event-costs/incentive-travel/` | — | incentive-travel (hub) | — | — | September 2026 |
| 07 | `/event-costs/conferences/` | — | conferences (hub) | — | — | September 2026 |
| 08 | `/event-costs/antalya/60-person-corporate-event/` | antalya | corporate-events | 60 | 60,000–80,000 | September 2026 |
| 09 | `/event-costs/antalya/100-person-incentive-trip/` | antalya | incentive-travel | 100 | 140,000–190,000 | September 2026 |
| 10 | `/event-costs/antalya/200-person-conference/` | antalya | conferences | 200 | 220,000–300,000 | September 2026 |
| 11 | `/event-costs/istanbul/100-person-corporate-event/` | istanbul | corporate-events | 100 | 150,000–210,000 | September 2026 |
| 12 | `/event-costs/belek/100-person-corporate-retreat/` | belek | corporate-retreats | 100 | 130,000–175,000 | September 2026 |

Full per-scenario `costBreakdown[]`, `priceDrivers[]`, `costReductionOptions[]`,
`premiumUpgradeOptions[]` and `relevantSelectedWorks[]` are published directly
on each page (see "Programme Snapshot" / "Example Budget Breakdown" sections)
rather than duplicated here, so there is a single place to keep them current.

**Budget assumption basis:** ranges are built from general, publicly
observable Turkey MICE market benchmarks (5-star resort/city hotel rate
bands, typical AV/production day rates, standard group-transfer and
staffing ratios), not from confidential supplier net rates, negotiated
pricing, markup or margin. They are indicative planning ranges only — see
the "Planning Estimate Disclaimer" on each page. If confidence in an
assumption is ever too low to defend publicly, the record must move back to
`draft`/`noindex` rather than remain published with a guessed number.

## Non-Phase-1 records (`indexStatus: draft` — no page, no sitemap entry)

These exist here as placeholders for the taxonomy so future work does not
need to re-derive scope. None should be published until either (a) a
validated cost model exists, or (b) Search Console demonstrates demand
(see below).

- `destination`: `cappadocia`, `bodrum`
- `eventType`: `corporate-retreats` (hub), `product-launches` (hub), `gala-dinners` (hub)
- Any `[destination]/[eventType]` or `[destination]/[groupSize]-person-*`
  combination not listed in the Phase 1 register above (e.g. Cappadocia
  scenarios, Bodrum scenarios, product-launch scenarios, gala-dinner
  scenarios, or 50/60/70/80/500-person variants of an intent already
  covered by an existing page).

## Phase 2 — data-led expansion process (not built yet)

After Phase 1 pages are indexed, review Google Search Console
(Search Console → Performance, filtered to `/event-costs/`) for:

- Impressions, clicks, CTR and average position per URL.
- Query clusters landing on each hub (destination demand, event-type demand,
  long-tail and emerging group-size queries).

Only create a new `index.html` (and move its record's `indexStatus` to
`index`) when either:

1. Search Console shows meaningful, sustained impressions/clicks for a
   query cluster not yet served by an existing page, **and** a validated,
   genuinely useful cost model can be produced for it; or
2. Strong independent commercial justification exists (e.g. a confirmed
   pipeline of enquiries for a destination/event type).

Do not create mechanical group-size variants (e.g. 50/60/70/80-person
versions of the same intent) purely to increase URL count — each new page
must target a distinct, defensible search intent (avoid keyword
cannibalisation between hub and scenario pages).
