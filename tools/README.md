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
- **GA4 or GTM**, only when an ID is set in `site_config.py`. With both empty
  no analytics script is emitted at all.
- **Search Console / Bing verification tags**, when tokens are set.

`trackEvent` in `assets/js/main.js` pushes to `dataLayer` *and* calls `gtag`
directly, so the site's 20 custom events reach GA4 whether analytics arrives via
gtag.js or a GTM container.

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
