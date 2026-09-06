# COP31 cluster generator

The site is hand-written static HTML with no build step. The COP31 cluster is
the exception: 30 pages sharing one page shell, one conversion component and one
set of verified facts, which is more than is sensible to maintain by hand.

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
