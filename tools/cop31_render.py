"""Page renderer for the COP31 cluster.

The site is hand-written static HTML with no build step, so the shared chrome
(header, footer) is lifted from a reference page at build time rather than
duplicated here. That keeps generated COP31 pages byte-identical to the rest of
the site whenever the global header or footer changes.
"""

import json
import os

from cop31_common import (
    DISCLAIMER,
    LAST_UPDATED,
    LAST_UPDATED_LABEL,
    OFFICIAL_LINKS,
    SITE,
    cta_link,
    esc,
    proposal_url,
    wa_link,
)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCE_PAGE = os.path.join(ROOT, "services", "event-production", "index.html")

SOCIAL = SITE + "/assets/img/social-preview.png"
SOCIAL_ALT = "DMC Turkey Partner — Turkey DMC and MICE partner"


def _chrome():
    with open(REFERENCE_PAGE, encoding="utf-8") as handle:
        html = handle.read()
    body_start = html.index("<body>")
    main_start = html.index('<main id="main-content">')
    main_end = html.index("</main>") + len("</main>")
    header = html[body_start:main_start]
    footer = html[main_end:]
    return header, footer


HEADER, FOOTER = _chrome()


# --- content helpers ---------------------------------------------------------

def section(heading, *blocks, **kwargs):
    parts = ['<section class="page-section"%s>' % (
        ' id="%s"' % kwargs["anchor"] if kwargs.get("anchor") else ""
    )]
    if heading:
        parts.append("      <h2>%s</h2>" % heading)
    for block in blocks:
        if block:
            parts.append("      " + block.strip())
    parts.append("    </section>")
    return "\n      ".join(parts)


def lede(text):
    return '<p class="page-section__lede">%s</p>' % text


def para(text):
    return "<p>%s</p>" % text


def cards(items):
    """items: (title, body) or (title, href, body)."""
    out = ['<div class="card-grid">']
    for item in items:
        if len(item) == 3:
            title, href, body = item
            title_html = '<a href="%s">%s</a>' % (href, title)
        else:
            title, body = item
            title_html = title
        out.append(
            '<article class="card"><h3>%s</h3><p>%s</p></article>' % (title_html, body)
        )
    out.append("</div>")
    return "".join(out)


def checklist(items):
    return '<ul class="checklist">%s</ul>' % "".join("<li>%s</li>" % i for i in items)


def plain_list(items):
    return "<ul>%s</ul>" % "".join("<li>%s</li>" % i for i in items)


def facts(pairs):
    """Key/value block.

    Each term/definition pair is wrapped in a div (valid inside <dl>) so the
    .event-facts auto-fit grid places a label and its value in one cell.
    Without the wrapper every dt and dd becomes its own grid item and the
    pairing stops being readable once values wrap.
    """
    return '<dl class="event-facts">%s</dl>' % "".join(
        "<div><dt>%s</dt><dd>%s</dd></div>" % (dt, dd) for dt, dd in pairs
    )


def steps(items):
    return '<ol class="steps-list">%s</ol>' % "".join(
        "<li><h3>%s</h3><p>%s</p></li>" % (title, body) for title, body in items
    )


def table(caption, headers, rows):
    head = "".join("<th scope=\"col\">%s</th>" % h for h in headers)
    body = "".join(
        "<tr>%s</tr>"
        % "".join(
            ('<th scope="row">%s</th>' % cell) if idx == 0 else ("<td>%s</td>" % cell)
            for idx, cell in enumerate(row)
        )
        for row in rows
    )
    return (
        '<div class="comparison-table-wrap"><table class="comparison-table">'
        "<caption>%s</caption><thead><tr>%s</tr></thead><tbody>%s</tbody>"
        "</table></div>" % (caption, head, body)
    )


def cluster(links):
    return '<div class="cluster-links">%s</div>' % "".join(
        '<a href="%s">%s</a>' % (href, label) for href, label in links
    )


def answer(text):
    """Short extractable answer directly under the H1, for AI/AEO surfaces."""
    return '<p class="cop31-answer">%s</p>' % text


def updated():
    return (
        '<p class="reviewed-note">Last updated: <time datetime="%s">%s</time>. '
        "Official COP31 details can change — always confirm against the official "
        "sources linked on this page.</p>" % (LAST_UPDATED, LAST_UPDATED_LABEL)
    )


def official_resources(keys):
    items = []
    for key in keys:
        href, label = OFFICIAL_LINKS[key]
        items.append(
            # Followed links: these are the authoritative sources the page's
            # factual claims rest on, so the citation should count as one.
            '<li><a href="%s" target="_blank" rel="noopener">%s</a></li>'
            % (href, label)
        )
    return (
        '<section class="page-section cop31-sources">\n'
        "      <h2>Official COP31 Resources</h2>\n"
        '      <p class="page-section__lede">Formal conference information — dates, '
        "registration, accreditation, programme and official logistics — is published "
        "by UNFCCC and the COP31 Türkiye Presidency. Use these sources as the "
        "authority on anything official.</p>\n"
        "      <ul>%s</ul>\n"
        "    </section>" % "".join(items)
    )


def conversion_block(slug, service_interest, page_type, services, heading=None, copy=None):
    """The universal COP31 conversion component (section 21 of the brief)."""
    heading = heading or "Need Local Support During COP31 Antalya?"
    copy = copy or (
        "Our Antalya operations team supports international agencies, delegations, "
        "exhibitors, pavilions and event teams with local production, logistics, "
        "staffing, transportation and urgent requirements."
    )
    service_links = " · ".join(
        '<a href="%s">%s</a>' % (href, label) for href, label in services
    )
    return (
        '<section class="page-section cop31-cta">\n'
        '      <div class="cta-banner">\n'
        "        <h2>%s</h2>\n"
        "        <p>%s</p>\n"
        '        <div class="cta-banner__actions hero-actions">%s%s</div>\n'
        '        <p class="cop31-cta__services">%s</p>\n'
        "      </div>\n"
        "    </section>"
        % (
            heading,
            copy,
            cta_link("Request COP31 Support", slug, service_interest, page_type),
            wa_link(
                "WhatsApp Our Antalya Operations Desk",
                "Hello DmcTurkeyPartner — I need local support for COP31 Antalya (%s)."
                % service_interest,
            ),
            service_links,
        )
    )


DEFAULT_PLANNING_CONTEXT = [
    ("/cop31-antalya-dates/", "COP31 Dates 2026"),
    ("/cop31-antalya-venue/", "Venue &amp; Location"),
    ("/cop31-antalya-participant-guide/", "Participant Guide"),
]


def planning_context(links):
    """Route commercial pages back into the informational cluster.

    Keeps the topical architecture bidirectional: guides feed the service pages,
    and every service page links back to the guides a buyer still needs.
    """
    return section(
        "Planning Context for COP31 Antalya",
        lede(
            "COP31 runs from 9 to 20 November 2026 at the Antalya EXPO Center. If you are "
            "still working out the dates, the venue or how participation works, start with "
            "the guides below."
        ),
        cluster(links),
    )


def faq_section(faqs):
    if not faqs:
        return ""
    items = "".join(
        '<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in faqs
    )
    return (
        '<section class="page-section">\n'
        "      <h2>Frequently Asked Questions</h2>\n"
        '      <div class="faq-list">%s</div>\n'
        "    </section>" % items
    )


def disclaimer_block():
    return '<section class="page-section"><p class="disclaimer">%s</p></section>' % DISCLAIMER


# --- schema ------------------------------------------------------------------

def _ld(data):
    return (
        '  <script type="application/ld+json">\n  %s\n  </script>'
        % json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    )


# Reference, not a redefinition. The canonical Organization node is emitted on
# every page by tools/site_seo.py; restating it here with different values would
# split one entity into competing variants.
ORGANIZATION = {"@id": SITE + "/#organization"}


def _schema(page):
    url = SITE + "/" + page["slug"] + "/"
    blocks = []
    blocks.append(
        _ld(
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "COP31 Antalya 2026",
                        "item": SITE + "/cop31-antalya/",
                    },
                ]
                + (
                    []
                    if page["slug"] == "cop31-antalya"
                    else [
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": page["breadcrumb"],
                            "item": url,
                        }
                    ]
                ),
            }
        )
    )

    if page["page_type"] == "commercial":
        blocks.append(
            _ld(
                {
                    "@context": "https://schema.org",
                    "@type": "Service",
                    "name": page["service_name"],
                    "serviceType": page["service_interest"],
                    "url": url,
                    "provider": ORGANIZATION,
                    "areaServed": {
                        "@type": "City",
                        "name": "Antalya",
                        "address": {
                            "@type": "PostalAddress",
                            "addressLocality": "Antalya",
                            "addressCountry": "TR",
                        },
                    },
                    "description": page["description"],
                }
            )
        )
    else:
        blocks.append(
            _ld(
                {
                    "@context": "https://schema.org",
                    "@type": "WebPage",
                    "name": page["title"],
                    "url": url,
                    "description": page["description"],
                    "inLanguage": "en",
                    "dateModified": LAST_UPDATED,
                    "isPartOf": {"@id": SITE + "/#website"},
                    "publisher": ORGANIZATION,
                    "about": {
                        "@type": "Event",
                        "name": "COP31 — 2026 UN Climate Change Conference",
                        "startDate": "2026-11-09",
                        "endDate": "2026-11-20",
                        "eventStatus": "https://schema.org/EventScheduled",
                        "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                        "location": {
                            "@type": "Place",
                            "name": "Antalya EXPO Center",
                            "address": {
                                "@type": "PostalAddress",
                                "addressLocality": "Antalya",
                                "addressCountry": "TR",
                            },
                        },
                        "url": "https://unfccc.int/cop31",
                    },
                }
            )
        )

    if page.get("faqs"):
        blocks.append(
            _ld(
                {
                    "@context": "https://schema.org",
                    "@type": "FAQPage",
                    "mainEntity": [
                        {
                            "@type": "Question",
                            "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": _strip(a)},
                        }
                        for q, a in page["faqs"]
                    ],
                }
            )
        )
    return "\n".join(blocks)


def _strip(html):
    import re

    text = re.sub(r"<[^>]+>", "", html)
    return (
        text.replace("&amp;", "&")
        .replace("&nbsp;", " ")
        .replace("&quot;", '"')
        .strip()
    )


# --- page assembly -----------------------------------------------------------

def render(page):
    slug = page["slug"]
    url = SITE + "/" + slug + "/"
    title = esc(page["title"])
    description = esc(page["description"])

    breadcrumbs = [
        '        <ol>',
        '          <li><a href="/">Home</a></li>',
    ]
    if slug == "cop31-antalya":
        breadcrumbs.append('          <li aria-current="page">COP31 Antalya 2026</li>')
    else:
        breadcrumbs.append('          <li><a href="/cop31-antalya/">COP31 Antalya 2026</a></li>')
        breadcrumbs.append(
            '          <li aria-current="page">%s</li>' % esc(page["breadcrumb"])
        )
    breadcrumbs.append("        </ol>")

    hero = ['    <section class="page-section">', "      <h1>%s</h1>" % page["h1"]]
    if page.get("answer"):
        hero.append("      " + answer(page["answer"]))
    hero.append("      " + lede(page["lede"]))
    if page.get("hero_facts"):
        hero.append("      " + facts(page["hero_facts"]))
    hero.append(
        '      <div class="hero-actions">%s%s</div>'
        % (
            cta_link(
                page.get("cta_label", "Request COP31 Support"),
                slug,
                page["service_interest"],
                page["page_type"],
            ),
            wa_link(
                page.get("wa_label", "WhatsApp Our Antalya Operations Desk"),
                page.get(
                    "wa_message",
                    "Hello DmcTurkeyPartner — I need COP31 Antalya support (%s)."
                    % page["service_interest"],
                ),
            ),
        )
    )
    if page.get("update_sensitive"):
        hero.append("      " + updated())
    hero.append("    </section>")

    body = ["\n".join(hero)]
    body.extend(page["sections"])

    if page["page_type"] == "commercial":
        body.append(
            planning_context(page.get("planning_context", DEFAULT_PLANNING_CONTEXT))
        )

    body.append(
        conversion_block(
            slug,
            page["service_interest"],
            page["page_type"],
            page["cta_services"],
            heading=page.get("cta_heading"),
            copy=page.get("cta_copy"),
        )
    )

    if page.get("faqs"):
        body.append(faq_section(page["faqs"]))

    if page.get("related"):
        body.append(
            section(
                page.get("related_heading", "Continue Planning for COP31 Antalya"),
                lede(page["related_lede"]) if page.get("related_lede") else None,
                cluster(page["related"]),
            )
        )

    if page.get("sources"):
        body.append(official_resources(page["sources"]))

    body.append(disclaimer_block())

    head = [
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
        '  <meta property="og:type" content="website">',
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
        # Campaign attribution read by main.js, so a visitor who reaches the
        # proposal form through the generic header/footer CTA is still tagged
        # to COP31 and to the service page they came from.
        '  <meta name="dmc:lead-source" content="COP31">',
        '  <meta name="dmc:campaign" content="COP31 Antalya 2026">',
        '  <meta name="dmc:service-interest" content="%s">' % esc(page["service_interest"]),
        '  <meta name="dmc:page-type" content="%s">' % page["page_type"],
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        _schema(page),
        "</head>",
    ]

    return (
        "\n".join(head)
        + "\n"
        + HEADER
        + '<main id="main-content">\n'
        + '      <nav class="breadcrumbs" aria-label="Breadcrumb">\n'
        + "\n".join(breadcrumbs)
        + "\n      </nav>\n"
        + "\n".join(body)
        + "\n  </main>"
        + FOOTER
    )
