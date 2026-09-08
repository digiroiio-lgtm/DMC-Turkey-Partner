# Site tooling

The site is hand-written static HTML with no build step. These scripts cover
the parts that must stay identical across all 138 pages — the COP31 cluster, the
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
| `managed_blocks.py` | The fence primitive every site-wide patcher builds on |
| `page_model.py` | Reads facts back out of a page's markup. Pure; never writes |
| `page_schema.py` | Per-page JSON-LD graph, derived from that markup |
| `seo_check.py` | The audit CI runs. Read-only |
| `answer_data.py` | Hand-written answer capsules, keyed by URL |
| `answer_capsule.py` | Injects them under the `<h1>` |
| `site_head.py` | og/twitter/theme-color meta |
| `site_footer.py` | Footer headings and contact block |
| `llms_txt.py` | Generates `llms.txt` and `llms-full.txt` |
| `related_works.py` | Cross-links the case studies from their own project data |

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

## Per-page schema

```
python3 tools/page_schema.py --dry-run   # print what would change
python3 tools/page_schema.py             # apply
```

Gives every non-COP31 page one connected `@graph`: a `WebPage` node, the
`BreadcrumbList` and `FAQPage` regenerated from the visible DOM, and whatever
its family calls for — `Service` on `/services/` and `/event-costs/`,
`CreativeWork` on `/selected-works/`, `CollectionPage` + `ItemList` on the
hubs, `Place` on `/destinations/`.

Everything is **derived from the rendered HTML**, not from a registry keyed by
URL. The site has no build step, so content is edited directly in the `.html`
files; a registry would be a second copy of the truth and would go stale the
first time someone corrected a venue name in a `<dd>`. Structured data that
asserts something the page does not say is what Google's guidelines treat as
spam, and the agreement between the two is what makes FAQ and breadcrumb
markup eligible at all. Derived schema cannot drift.

The COP31 cluster is skipped — `cop31_render.py` already emits linked
`WebPage`/`Service`/`FAQPage` for it — as are the `Event`, `Article` and
`NewsArticle` nodes elsewhere, which this patcher only ever adds alongside.

`CreativeWork` rather than `Event` on the case studies is deliberate: those are
completed private programmes nobody can attend, and `Event` would court an
event rich result for something with no tickets. No `client` or `sponsor`
either. The brands are already named in the visible copy, but promoting them
into machine-readable triples materially widens reuse, and that needs the
contracts checked first.

### Fences

Each site-wide patcher owns one fenced region and rewrites only between its
own markers, which is what makes re-running it a no-op rather than an append:

| Fence | Owner |
| --- | --- |
| `<!-- site-identity:begin/end -->` | `site_seo.py` |
| `<!-- page-schema:begin/end -->` | `page_schema.py` |
| `<!-- cop31-nav:begin/end -->` | `cop31_nav.py` |

`managed_blocks.py` holds the primitive. Two rules it exists to enforce:
placement is anchored rather than "before `</head>`", so the output bytes do
not depend on which patcher ran last; and anything that *removes* nodes scans
`outside_fences()` only, so it cannot reach into another patcher's block.
`write_if_changed()` is the single write path, and it refuses to save a file
whose `</head>`, `<main>`, `<h1>` or `</html>` count changed, that gained a
double-escaped entity, or whose JSON-LD no longer parses.

## Checks

```
python3 tools/seo_check.py                     # report
python3 tools/seo_check.py --max-warnings 395  # what CI runs
python3 tools/seo_check.py --strict            # warnings fail too
```

Errors are things that are objectively broken or that Rich Results rejects.
Warnings are editorial calls a human may reasonably override, held down by a
ratchet: `--max-warnings` is seeded at the current count and lowered as content
work lands, so the number can fall but never grow. A gate that failed on day
one would just get switched off. `.github/workflows/seo.yml` runs this and
`sitemaps.py --check` on every push and pull request.

## Waiting on real-world data

`site_config.py` carries empty constants for facts this repository does not
contain: `ORG_SAME_AS`, `ORG_ADDRESS`, `ORG_GEO`, `ORG_OPENING_HOURS`, the GA4
and verification IDs, and `EMIT_COST_PRICE_SPEC`. Every emitting site is
guarded, so an empty value suppresses the property rather than shipping a
guess. A wrong `sameAs` merges this business with someone else's entity, and a
fabricated address produces a weak `LocalBusiness` competing with the correct
`Organization` — which is why the `@type` stays `Organization` until a real
address exists.


## Answer capsules

`tools/answer_data.py` holds a short, direct answer per URL; `answer_capsule.py`
renders it into a fence under the `<h1>`. This is the one thing on the site that
is deliberately **not** derived: the point of a capsule is to say what the page
does not already say in that form, so there is no source to derive it from. A
URL with no entry gets no capsule, and removing an entry removes the block.

The pattern is older than this module — `cop31_render.py` has emitted
`.cop31-answer` "for AI/AEO surfaces" since the COP31 cluster was built, on 30
pages. The CSS rule now covers `.answer-capsule` with `.cop31-answer` as an
alias, so those pages render unchanged. Pages carrying a capsule also get
`speakable` pointing at it and the heading.

A capsule earns its place only if it answers the question the title implies —
who it is for, what is and is not included, the constraint that actually
matters. Restating the lede makes the page longer and no clearer. Nothing in it
may assert a certification, client relationship, price or guarantee that the
page itself does not already make.

## Convergence

The generators are idempotent, so a clean checkout plus one `cop31_build.py`
must reproduce exactly what is committed. CI asserts this with `git diff
--quiet` after a build.

That gate exists because the weaker version of it missed a real bug. Comparing
`git status --short` compares the *list* of modified files, not their contents,
so it reported "no change" while `strip()` left each fence's indentation behind
and walked the following line six spaces further right on every run. Compare
content, not filenames.


## Related works

```
python3 tools/related_works.py --dry-run
python3 tools/related_works.py
```

Derives each case study's related links from the `<dl class="work-info">` the
page already publishes — same event type first, then same destination, four
links, ordered stably so repeat runs produce identical bytes. Same contract as
the schema: correct a venue or a category in the markup and the links follow on
the next build.

## Run order

`cop31_build.py` orchestrates everything and the order matters, because the
generators rewrite pages from scratch and the patchers derive from finished
markup:

```
cop31 pages -> cop31_news -> site_footer -> cop31_nav -> site_seo
  -> cop31_evergreen_link -> related_works -> page_schema -> answer_capsule
  -> site_head -> llms_txt -> sitemaps
```

`site_footer` runs before `cop31_nav` because the nav patcher anchors on the
footer's Company column label. `related_works` runs before `page_schema` so the
new links are in the markup the schema reads. `sitemaps` runs last so `lastmod`
sees the final state.
