# Site tooling

The site is hand-written static HTML with no build step. These scripts cover
the parts that must stay identical across all 131 pages — the COP31 cluster, the
global navigation, the entity/measurement block and the sitemaps — where
hand-editing every file would guarantee drift.

All scripts are idempotent: re-running them is a no-op when nothing changed.

## Running it

```
python3 tools/cop31_build.py
```

Regenerates every COP31 page and then runs the nav patcher, so the whole site
converges regardless of the order the scripts are run in. Both are idempotent.

```
python3 tools/cop31_nav.py
```

Inserts the COP31 mega menu and footer column into every `*.html` on the site.
Safe to re-run; it skips files that already carry the menu.

## Layout

| File | Purpose |
| --- | --- |
| `cop31_common.py` | Verified official facts, official source URLs, CTA/WhatsApp URL builders, the disclaimer |
| `cop31_links.py` | The single source of truth for every cluster URL and its label — used by the pages, the mega menu, the footer and the sitemap |
| `cop31_render.py` | Page shell, content helpers (`section`, `cards`, `table`, `facts`, …) and JSON-LD |
| `cop31_pages_*.py` | Page content. Each module exports `PAGES`; the builder discovers them by glob |
| `cop31_build.py` | Writes `<slug>/index.html` for every page |
| `cop31_nav.py` | Patches the global nav and footer across the site |

The shared header and footer are lifted at build time from
`services/event-production/index.html`, so generated pages stay byte-identical
to the rest of the site whenever the global chrome changes.

## Updating the facts

COP31 information changes as November 2026 approaches. Before bumping
`LAST_UPDATED` in `cop31_common.py`, re-check the official sources listed in
that file — UNFCCC for dates, venue, registration and participant logistics; the
COP31 Türkiye Presidency for the programme. Never leave outdated registration,
transport or programme information in place simply because it was published
before.

Nothing in this cluster may assert an affiliation with UNFCCC or the official
COP31 organising bodies. The disclaimer in `cop31_common.py` renders on every
page.


## Site-wide identity, analytics and verification

### Shared footer

```
python3 tools/site_footer.py          # synchronize the footer on all pages
python3 tools/site_footer.py --check  # audit without writing
```

`site_footer.py` owns the five-column navigation and separate registered agency
band. Link labels point to existing category pages; identity and contact values
come from `site_config.py`. It updates only the footer, preserving page content,
metadata and scripts. `site_seo.py` and `cop31_nav.py` use the same renderer, and generated pages
inherit it from the event-production reference page.

```
python3 tools/site_seo.py
```

Reads `tools/site_config.py` and applies to every page:

- **One canonical Organization + WebSite `@graph`** with a stable `@id`
  (`/#organization`). This replaced three different Organization names that
  previously appeared on a handful of pages and none on the rest. Google's
  Knowledge Graph and AI answer engines resolve an entity by consistent naming
  plus a stable `@id`; competing variants split one business into several weak
  entities. Per-page `Service`/`WebPage` schema references that `@id` rather
  than restating the organisation.
- **Consent-controlled GA4 or GTM**: a first-party loader receives configured IDs; Google tags are requested only after analytics acceptance. Refusal leaves the site and form usable. Advertising consent stays denied.
- **Search Console / Bing verification tags**, when tokens are set.

`trackEvent` in `assets/js/main.js` and `calculator.js` delegates to the
consent-aware dispatcher in `privacy.js`. No events are queued before consent.
Optional proposal-attribution storage is gated too; calculator session state
remains available as a requested feature. Every footer includes Cookie Settings.

## Privacy, cookies and website terms

```
python3 tools/legal_pages.py
python3 tools/site_seo.py
```

`legal_pages.py` renders the three legal pages using the registered agency and
company identity in `site_config.py`. Review the text when providers, contracts,
processing purposes or retention practices change. The explicit review date
must only change after an actual review. Provider contracts and international
transfer arrangements require account-level verification; publishing a policy
does not establish those arrangements. The proposal form links the privacy
notice without bundling the enquiry with marketing permission.

Note that the CSP in `_headers` and `vercel.json` explicitly allows
`googletagmanager.com` and the `google-analytics.com` endpoints. Without those
allowances the analytics beacon is blocked silently — the tag appears installed
and no data arrives.

## Sitemaps

```
python3 tools/sitemaps.py          # rewrite with fresh lastmod
python3 tools/sitemaps.py --check  # audit only; non-zero exit on a problem
```

Verifies that every indexable page appears in exactly one sitemap and that no
sitemap lists a noindex or missing page — both are Search Console errors — then
stamps `<lastmod>` from each file's last git commit date. The dates are taken
from git rather than invented, because a `lastmod` that is always "today"
teaches Google to ignore the signal.

## Order of operations

`cop31_build.py` regenerates COP31 pages from scratch, so it re-runs
`cop31_nav.py` and `site_seo.py` afterwards automatically. After any content
change, run `tools/sitemaps.py` last so `lastmod` reflects the final state.

## Antalya transfer prices

```
python3 tools/transfer_prices_build.py
```

Every transfer price on the site comes from `tools/transfer_prices.py`: vehicles,
the three services (airport one way, daily shuttle, full-day vehicle with
driver), what each includes, extra hours/kilometres and the disclaimer. Prices
are per vehicle in EUR — never per person.

To change a price, edit `transfer_prices.py`, bump `PRICES_REVIEWED`, then run
the script. It rewrites `/antalya-transfer-prices/` and refreshes the
`<!-- transfer-prices:NAME:begin/end -->` blocks on `/event-costs/`,
`/services/transportation-logistics/`, `/cop31-antalya-airport-transfer/`,
`/cop31-private-transfers/` and `/cop31-antalya-transport/` (see `TARGETS`).
`transfer_pricing.py` renders the fragments; the COP31 page sources include the
same blocks so a full `cop31_build.py` keeps them.

The script deliberately does not regenerate the COP31 cluster: several of those
pages were edited directly after generation, and a full rebuild would revert
those edits. Run `tools/sitemaps.py` afterwards for fresh `lastmod` dates.

## Production showcase

```
python3 tools/production_showcase_build.py
```

`tools/production_showcase_data.py` lists the categories and every showcase
photo (file name, category, alt text, caption). The script writes
`/production-showcase/` and refreshes the homepage "What We Build" section
between `<!-- production-showcase:begin/end -->` in `index.html`.

To add a photo: save it as `assets/img/showcase/<descriptive-name>.webp` (about
1024 px wide) plus a `-640.webp` copy, add a `PHOTOS` entry, and run the script.
Use English, descriptive file names, and alt text that describes what is
visible. Name a city only when the venue or campaign confirms it; otherwise say
Türkiye. `HOMEPAGE` picks the six homepage cards; the first one is the large
card.

## Off-season hub

```
python3 tools/off_season_build.py
```

`tools/off_season_data.py` holds the destinations, their off-peak windows, the
season label and last-updated date. The script writes
`/off-season-events-turkey/`, `/off-season-events-turkey/belek/`,
`/off-season-events-turkey/antalya/`, `/off-season-events-turkey/istanbul/` and
`/off-season-events-turkey/bodrum/` and `/off-season-events-turkey/cappadocia/` and rewrites
the pop-up's `OFFPEAK` block in `assets/js/main.js` between
`/* offseason-data:begin/end */`, so the pop-up, the hub table and the pages
cannot drift apart.

**Saving claim rule:** a percentage is published only when `QUOTE_COMPARISONS`
contains real like-for-like quotes (same scope, group size and nights; one
off-peak, one peak). While it is empty every page and the pop-up use the
percentage-free message. No saving is derived from the event-costs reference
ranges.

To add a destination page: set its `page` in `DESTINATIONS`, add a render
function modelled on `render_belek()` with its own content, and list it in
`sitemap-destinations.xml`.

## Market pages (UK agencies, German)

```
python3 tools/market_pages_build.py
```

Writes `/dmc-turkey-uk-agencies/` (English) and `/de/dmc-tuerkei/` (German,
`lang="de"`). Only facts that already exist on the site are used. The German page is
linked with hreflang (de / en / x-default) to `/dmc-turkey/`, which carries the
reciprocal tags. Have a native speaker review the German copy before promoting it.

Form and success-modal copy is English by default; a form can override it with a JSON
object in `data-i18n` (keys in `FORM_TEXT_DEFAULTS`, `assets/js/main.js`). The German page
uses this for the button states, validation/error messages, the modal and the WhatsApp message.

The German page also has a translated header and footer (`CHROME_DE` in the generator) and a
German cookie banner (`assets/js/privacy.js`, chosen by `<html lang="de">`). `tools/site_footer.py`,
`tools/cop31_nav.py` and `tools/site_seo.py` skip the chrome of `lang="de"` pages, so re-running
them will not overwrite it. Adding a nav item means adding its German label to `CHROME_DE`.

## Homepage reference cards

The Selected Works cards on `index.html` show category, venue, city and a scope line
(`work-card__services`). Participant numbers, outcomes and client quotes are not stored
anywhere in the repository; add them as a short `<p class="work-card__scale">` line (and
quote text on the project page) only once the client has approved them.

## Agency Fam Trip 2027 campaign (Europe + US)

Disabled by default. Settings live in `campaign/uk-fam-trip.json` (one file; the file name is kept for
history); after editing run `python3 tools/fam_trip_build.py && python3 tools/sitemaps.py`.

| Launch variable | JSON key | Default |
| --- | --- | --- |
| `CAMPAIGN_ENABLED` | `enabled` | `false` |
| `CAMPAIGN_NAME` | `campaignName` | `uk_fam_trip_2027` (kept so existing Formspree/GA4 reporting stays comparable) |
| `TARGET_COUNTRIES` | `targetCountries` | GB IE DE AT CH NL BE LU PL FR SE NO DK FI US |
| `POPUP_DELAY_MS` | `popupDelayMs` | `15000` |
| `POPUP_SCROLL_THRESHOLD` | `popupScrollThreshold` | `50` |
| `DISMISSAL_DAYS` | `dismissalDays` | `7` |
| `CAMPAIGN_PERIOD` | `campaignPeriod` | `January–March 2027 (proposed)` |
| `APPLICATION_STATUS` | `applicationStatus` | `Register Interest` |
| (Formspree form URL) | `formspreeEndpoint` | `https://formspree.io/f/mqpelgrv` |

* **Pop-up** (`assets/js/fam-trip-campaign.js`, loaded by `main.js` on every page): visitors from the target
  countries only, after a cookie choice, 15 s or 50% scroll, once per session, 7-day suppression after
  dismissal, permanent after an application, never on the landing page, COP31 pages, quotation/contact
  pages or while a field has focus. Pop-up is English, CTA "Register Your Interest".
* **Geo**: `/api/geo` returns Vercel's `x-vercel-ip-country` and `x-vercel-ip-timezone`. Unknown country =
  no automatic pop-up; the generic headline is shown on the landing page.
* **Bot / VPN / data-centre filtering is best-effort.** Filters in place: server-side bot user-agent list,
  `navigator.webdriver` and headless/bot user agents, and an IP-timezone vs browser-timezone continent
  mismatch (typical for VPNs). Vercel does not expose ASN/data-centre data, so data-centre IPs that
  present a normal browser cannot be recognised here. For stronger filtering enable Vercel Firewall /
  BotID (or put the site behind Cloudflare with bot score + ASN rules) and keep the same client logic.
* **Dynamic headline**: pop-up title and landing H1 read "Exclusive Invitation for [UK/Irish/German/…]
  MICE Agencies" (adjectives in `ADJECTIVE` in the JS), with the fixed sub-line "Experience Antalya &
  Belek in 2027. Discover Your Local DMC Partner." The server-rendered HTML (title, H1
  "Exclusive MICE Agency Fam Trip Invitation", canonical) is generic and identical for everybody; the swap
  is client-side only, so there are no per-country indexable pages. Unknown/untargeted/suspect geo = generic.
* **Landing page** `/agency-fam-trip-2027/` (old `/uk-agency-fam-trip` redirects here): `noindex` and absent
  from the sitemap while disabled.
* **Form**: submits to Formspree with `fetch`; success is shown only after Formspree answers 2xx. Hidden
  fields: `campaign_source`, `lead_status=New`, `submitted_at`, `consent_timestamp`, `landing_page`, UTM
  (only with analytics consent), `marketing_optin_status`, `visitor_country` (IP country, 2-letter code; not
  the same as the user-entered company `country`). Spam control: Formspree honeypot (`_gotcha`),
  a 3-second minimum fill time and Formspree's own filtering.
* **Lead lifecycle** (maintained in Formspree or an exported sheet; no CRM is built):
  New → Qualified → Invited → Confirmed → Attended → RFP → Won.
* **GA4 events**: `fam_popup_view`, `fam_popup_click`, `fam_popup_dismiss`, `fam_landing_view`,
  `fam_form_start`, `fam_form_submit`, `fam_lead_success`, all with `campaign_name` and `visitor_country`
  (no personal data). Register `visitor_country` as an event-scoped custom dimension and mark
  `fam_lead_success` as a key event in GA4 admin (not configured by this repo).
* **Launch checklist**: submit one real test application and check the Formspree dashboard and the
  notification email; set `enabled` to `true`; run the two commands above; confirm hosted arrangements,
  eligibility wording for the broadened audience, privacy wording and the pop-up image licence; verify the
  events in GA4 DebugView and real geo on the Vercel deployment from a few target countries.
* The pop-up/landing image is an owned event photo (`assets/img/mapfre-sigorta-antalya-gala-dinner*.webp`);
  replace it with a licensed Antalya/Belek resort photo when available.

## COP31 news layer

```
python3 tools/cop31_news.py             # hub + articles
python3 tools/cop31_evergreen_link.py   # news -> evergreen loop
```

Both run automatically as part of `cop31_build.py`, in that order — the build
regenerates the guide pages from scratch, so the evergreen linker has to run
after it or its edits are discarded.

`cop31_news_data.py` holds the sources and the articles. The rules it exists to
enforce, in order of importance:

1. **Never reproduce third-party text.** Read the source, extract and verify the
   facts, then write the article fresh. No sentence-level rewriting of someone
   else's copy, no copied headlines — the headline is written from the
   development, not from the source's title.
2. **Every article names its sources**, listed and linked at the foot of the
   page and attributed in the body where a specific claim rests on one.
   `S[...]` marks each source `official` or `media`, which drives the "Official"
   badge; official bodies outrank media for dates, venue, registration,
   programme, transport and accommodation.
3. **Separate fact from interpretation.** `changed` is what was reported;
   `means` is our own operational reading and is rendered under a heading that
   says so. Never let inference read as fact.
4. **No affiliation.** Nothing may imply UNFCCC or COP31-organiser status, and
   the independent-provider disclaimer renders on every article.

Where a figure could not be verified against an official publication — attendance
estimates, the EXPO renovation budget — the articles say that explicitly rather
than repeating a number from secondary coverage.

### Adding an update

Prefer editing an existing article and bumping its `updated` date over creating
a near-duplicate URL; a new URL is only justified by genuinely independent
search intent. One story gets one article however many outlets carry it. Each
article declares the `evergreen` guides it feeds, and the linker points those
guides at the newest article feeding them and refreshes their Last updated date.
