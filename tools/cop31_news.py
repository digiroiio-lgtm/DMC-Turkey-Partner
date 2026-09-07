#!/usr/bin/env python3
"""Render the COP31 news hub and its articles.

Reuses the shared page shell from cop31_render so the news layer is visually
part of the site rather than a bolted-on blog. Everything specific to news —
the card grid, the article header, the sources block — is styled by the
.news-* classes in main.css.
"""

import json
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import DISCLAIMER, SITE, cta_link, esc, wa_link  # noqa: E402
from cop31_news_data import ARTICLES, CATEGORIES, S  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT, SOCIAL, SOCIAL_ALT  # noqa: E402

NEWS_ROOT = "/cop31-news/"
CATEGORY_LABEL = dict(CATEGORIES)


def human_date(iso):
    return date.fromisoformat(iso).strftime("%-d %B %Y")


def _head(title, description, url, extra_schema):
    return "\n".join([
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '  <link rel="icon" href="/favicon.ico" sizes="any">',
        '  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
        '  <link rel="manifest" href="/site.webmanifest">',
        "  <title>%s</title>" % title,
        '  <meta name="description" content="%s">' % description,
        '  <link rel="canonical" href="%s">' % url,
        '  <meta property="og:type" content="article">',
        '  <meta property="og:title" content="%s">' % title,
        '  <meta property="og:description" content="%s">' % description,
        '  <meta property="og:url" content="%s">' % url,
        '  <meta property="og:site_name" content="DMC Turkey Partner">',
        '  <meta property="og:image" content="%s">' % SOCIAL,
        '  <meta property="og:image:alt" content="%s">' % SOCIAL_ALT,
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s">' % SOCIAL,
        '  <meta name="twitter:image:alt" content="%s">' % SOCIAL_ALT,
        '  <meta name="robots" content="index, follow">',
        '  <meta name="dmc:lead-source" content="COP31">',
        '  <meta name="dmc:campaign" content="COP31 Antalya 2026">',
        '  <meta name="dmc:service-interest" content="COP31 News Reader">',
        '  <meta name="dmc:page-type" content="informational">',
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        extra_schema,
        "</head>",
    ])


def _ld(data):
    return ('  <script type="application/ld+json">\n  %s\n  </script>'
            % json.dumps(data, ensure_ascii=False, separators=(",", ":")))


def _breadcrumb(items):
    return _ld({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
            for i, (path, name) in enumerate(items)
        ],
    })


def _sources_block(keys):
    rows = []
    for key in keys:
        label, url, kind = S[key]
        badge = ('<span class="news-source__badge">Official</span>'
                 if kind == "official" else "")
        rows.append(
            '<li class="news-source">%s<a href="%s" target="_blank" rel="noopener">%s</a></li>'
            % (badge, url, label)
        )
    return (
        '    <section class="page-section news-sources">\n'
        "      <h2>Sources</h2>\n"
        '      <p class="page-section__lede">This article was written from the sources below. '
        "Facts are attributed where they appear in the text; the wording, structure and "
        "practical interpretation are our own.</p>\n"
        '      <ul class="news-source-list">%s</ul>\n'
        "    </section>" % "".join(rows)
    )


def _related_block(article):
    guides = "".join(
        '<li><a href="%s">%s</a></li>' % (path, text)
        for path, text in article["evergreen"]
    )
    out = (
        '    <section class="page-section">\n'
        "      <h2>Related COP31 Guide</h2>\n"
        '      <p class="page-section__lede">The evergreen guides this update feeds into, '
        "kept current as official information changes.</p>\n"
        '      <ul class="news-related">%s</ul>\n'
        "    </section>" % guides
    )
    if article.get("services"):
        services = "".join(
            '<li><a href="%s">%s</a></li>' % (path, text)
            for path, text in article["services"]
        )
        out += (
            '\n    <section class="page-section">\n'
            "      <h2>Related Local Services</h2>\n"
            '      <p class="page-section__lede">Only the services that actually fit this '
            "story. We are an independent local operations provider, not part of the official "
            "COP31 arrangements described above.</p>\n"
            '      <ul class="news-related">%s</ul>\n'
            "    </section>" % services
        )
    return out


def _cta(slug):
    return (
        '    <section class="page-section cop31-cta">\n'
        '      <div class="cta-banner">\n'
        "        <h2>Need Local Support During COP31 Antalya?</h2>\n"
        "        <p>DmcTurkeyPartner supports international agencies, delegations, exhibitors, "
        "pavilions and event teams with local production, logistics, staffing, transportation "
        "and rapid operational support in Antalya.</p>\n"
        '        <div class="cta-banner__actions hero-actions">%s%s</div>\n'
        "      </div>\n"
        "    </section>"
        % (
            cta_link("Request COP31 Support", "cop31-news-" + slug,
                     "COP31 News Enquiry", "informational"),
            wa_link("WhatsApp Our Antalya Operations Desk",
                    "Hello DmcTurkeyPartner — I read your COP31 Antalya update and need local support."),
        )
    )


def render_article(article):
    url = SITE + NEWS_ROOT + article["slug"] + "/"
    schema = "\n".join([
        _breadcrumb([
            ("/", "Home"),
            ("/cop31-antalya/", "COP31 Antalya 2026"),
            (NEWS_ROOT, "COP31 News"),
            (NEWS_ROOT + article["slug"] + "/", article["title"]),
        ]),
        _ld({
            "@context": "https://schema.org",
            "@type": "NewsArticle",
            "headline": article["title"],
            "description": article["description"],
            "url": url,
            "datePublished": article["published"],
            "dateModified": article["updated"],
            "inLanguage": "en",
            "articleSection": CATEGORY_LABEL[article["category"]].replace("&amp;", "&"),
            "author": {"@id": SITE + "/#organization"},
            "publisher": {"@id": SITE + "/#organization"},
            "isPartOf": {"@id": SITE + "/#website"},
            "mainEntityOfPage": url,
            "about": {
                "@type": "Event",
                "name": "COP31 — 2026 UN Climate Change Conference",
                "startDate": "2026-11-09",
                "endDate": "2026-11-20",
                "location": {"@type": "Place", "name": "Antalya EXPO Center",
                             "address": {"@type": "PostalAddress",
                                         "addressLocality": "Antalya", "addressCountry": "TR"}},
            },
            "citation": [{"@type": "CreativeWork", "name": S[k][0], "url": S[k][1]}
                         for k in article["sources"]],
        }),
    ])

    changed = "".join("<p>%s</p>" % p for p in article["changed"])
    means = "".join(
        '<article class="news-take"><h3>%s</h3><p>%s</p></article>' % (h, b)
        for h, b in article["means"]
    )
    note = ('<p class="callout news-note">%s</p>' % article["means_note"]
            if article.get("means_note") else "")

    body = [
        '    <article class="news-article">',
        '    <section class="page-section news-article__head">',
        '      <p class="news-kicker"><a href="%s?c=%s">%s</a></p>'
        % (NEWS_ROOT, article["category"], CATEGORY_LABEL[article["category"]]),
        "      <h1>%s</h1>" % article["title"],
        '      <p class="news-meta">Published <time datetime="%s">%s</time>'
        ' &middot; Last updated <time datetime="%s">%s</time></p>'
        % (article["published"], human_date(article["published"]),
           article["updated"], human_date(article["updated"])),
        '      <p class="news-summary">%s</p>' % article["summary"],
        "    </section>",
        '    <section class="page-section">\n      <h2>What Changed?</h2>\n      %s\n    </section>' % changed,
        '    <section class="page-section">\n      <h2>What This Means for COP31 Participants</h2>\n'
        '      <p class="page-section__lede">The section below is our own operational reading, '
        "not official COP31 guidance. It is separated deliberately so you can tell which is "
        "which.</p>\n      <div class=\"news-takes\">%s</div>\n      %s\n    </section>" % (means, note),
        _related_block(article),
        _cta(article["slug"]),
        _sources_block(article["sources"]),
        '    <section class="page-section"><p class="disclaimer">%s</p></section>' % DISCLAIMER,
        "    </article>",
    ]

    breadcrumbs = (
        '      <nav class="breadcrumbs" aria-label="Breadcrumb">\n        <ol>\n'
        '          <li><a href="/">Home</a></li>\n'
        '          <li><a href="/cop31-antalya/">COP31 Antalya 2026</a></li>\n'
        '          <li><a href="%s">News</a></li>\n'
        '          <li aria-current="page">%s</li>\n'
        "        </ol>\n      </nav>\n" % (NEWS_ROOT, esc(article["title"]))
    )

    return (
        _head(esc(article.get("seo_title", article["title"])), esc(article["description"]),
              url, schema)
        + "\n" + HEADER + '<main id="main-content">\n' + breadcrumbs
        + "\n".join(body) + "\n  </main>" + FOOTER
    )


def _card(article, featured=False):
    return (
        '<article class="news-card%s" data-category="%s">'
        '<p class="news-card__cat">%s</p>'
        '<h3 class="news-card__title"><a href="%s%s/">%s</a></h3>'
        '<p class="news-card__excerpt">%s</p>'
        '<p class="news-card__meta"><time datetime="%s">%s</time></p>'
        "</article>"
        % (
            " news-card--featured" if featured else "",
            article["category"],
            CATEGORY_LABEL[article["category"]],
            NEWS_ROOT, article["slug"], article["title"],
            article["summary"].split(". ")[0] + ".",
            article["updated"], human_date(article["updated"]),
        )
    )


def render_hub():
    url = SITE + NEWS_ROOT
    title = "COP31 Antalya News &amp; Latest Updates 2026"
    description = (
        "Latest COP31 Antalya 2026 updates: venue and EXPO preparations, programme and "
        "registration, transport, hotels, pavilions and exhibitor news — sourced, attributed "
        "and written for participants."
    )
    ordered = sorted(ARTICLES, key=lambda a: a["updated"], reverse=True)
    used = [c for c in CATEGORIES if any(a["category"] == c[0] for a in ARTICLES)]

    schema = "\n".join([
        _breadcrumb([("/", "Home"), ("/cop31-antalya/", "COP31 Antalya 2026"),
                     (NEWS_ROOT, "COP31 News")]),
        _ld({
            "@context": "https://schema.org",
            "@type": "CollectionPage",
            "name": "COP31 Antalya News & Latest Updates",
            "url": url,
            "description": description,
            "inLanguage": "en",
            "isPartOf": {"@id": SITE + "/#website"},
            "publisher": {"@id": SITE + "/#organization"},
            "mainEntity": {
                "@type": "ItemList",
                "itemListElement": [
                    {"@type": "ListItem", "position": i + 1,
                     "url": SITE + NEWS_ROOT + a["slug"] + "/", "name": a["title"]}
                    for i, a in enumerate(ordered)
                ],
            },
        }),
    ])

    chips = "".join(
        '<button type="button" class="news-chip" data-filter="%s">%s</button>' % (slug, label)
        for slug, label in used
    )
    cards = "".join(_card(a, featured=(i == 0)) for i, a in enumerate(ordered))

    body = [
        '    <section class="page-section">',
        "      <h1>COP31 Antalya News &amp; Latest Updates</h1>",
        '      <p class="page-section__lede">Latest official announcements, venue '
        "developments, transport updates, programme changes and practical COP31 Antalya 2026 "
        "news for participants, exhibitors, pavilions, agencies and event teams.</p>",
        '      <p class="news-policy">Every update here is written from identified sources, '
        "which are listed and linked at the foot of each article. We summarise and interpret "
        "verified developments in our own words rather than reproducing third-party "
        "reporting, and we separate official information from our own operational reading. "
        "For anything official — dates, registration, accreditation, the programme, transport "
        "or accommodation — the "
        '<a href="https://unfccc.int/cop31" target="_blank" rel="noopener">UNFCCC</a> and the '
        '<a href="https://cop31.tr/" target="_blank" rel="noopener">COP31 Türkiye Presidency</a>'
        " are the authority.</p>",
        "    </section>",
        '    <section class="page-section">',
        '      <div class="news-filters" data-news-filters>',
        '        <button type="button" class="news-chip is-active" data-filter="all">All updates</button>',
        "        " + chips,
        "      </div>",
        '      <div class="news-grid" data-news-grid>%s</div>' % cards,
        '      <p class="news-empty" data-news-empty hidden>No updates in this category yet.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Start With the Guides</h2>",
        '      <p class="page-section__lede">News tells you what changed. These guides tell '
        "you what to do about it.</p>",
        '      <div class="cluster-links">'
        '<a href="/cop31-antalya/">COP31 Antalya 2026</a>'
        '<a href="/cop31-antalya-participant-guide/">Participant Guide</a>'
        '<a href="/cop31-antalya-dates/">Dates</a>'
        '<a href="/cop31-antalya-program/">Programme</a>'
        '<a href="/cop31-antalya-venue/">Venue</a>'
        '<a href="/cop31-antalya-expo-center/">Antalya EXPO Center</a>'
        '<a href="/cop31-antalya-registration/">Registration</a>'
        '<a href="/cop31-antalya-hotels/">Hotels</a>'
        '<a href="/cop31-antalya-transport/">Transport</a></div>',
        "    </section>",
        _cta("hub"),
        '    <section class="page-section"><p class="disclaimer">%s</p></section>' % DISCLAIMER,
    ]

    breadcrumbs = (
        '      <nav class="breadcrumbs" aria-label="Breadcrumb">\n        <ol>\n'
        '          <li><a href="/">Home</a></li>\n'
        '          <li><a href="/cop31-antalya/">COP31 Antalya 2026</a></li>\n'
        '          <li aria-current="page">News</li>\n'
        "        </ol>\n      </nav>\n"
    )
    return (_head(title, esc(description), url, schema) + "\n" + HEADER
            + '<main id="main-content">\n' + breadcrumbs + "\n".join(body)
            + "\n  </main>" + FOOTER)


def main():
    written = []
    hub_dir = os.path.join(ROOT, "cop31-news")
    os.makedirs(hub_dir, exist_ok=True)
    with open(os.path.join(hub_dir, "index.html"), "w", encoding="utf-8") as handle:
        handle.write(render_hub() + "\n")
    written.append("/cop31-news/")

    slugs = [a["slug"] for a in ARTICLES]
    duplicates = {s for s in slugs if slugs.count(s) > 1}
    if duplicates:
        raise SystemExit("Duplicate news slugs: %s" % ", ".join(sorted(duplicates)))

    for article in ARTICLES:
        directory = os.path.join(hub_dir, article["slug"])
        os.makedirs(directory, exist_ok=True)
        with open(os.path.join(directory, "index.html"), "w", encoding="utf-8") as handle:
            handle.write(render_article(article) + "\n")
        written.append(NEWS_ROOT + article["slug"] + "/")

    for path in written:
        print("wrote %s" % path)
    print("%d news pages generated" % len(written))


if __name__ == "__main__":
    main()
