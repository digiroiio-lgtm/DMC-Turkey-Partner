#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build /production-showcase/ and the homepage "What We Build" section.

Usage: python3 tools/production_showcase_build.py

Photos and categories live in tools/production_showcase_data.py. This script
writes production-showcase/index.html and replaces the content between the
`<!-- production-showcase:begin/end -->` markers in index.html.
Idempotent: re-running with unchanged data changes nothing.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PIL import Image  # noqa: E402

from cop31_common import SITE, esc  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT  # noqa: E402
from production_showcase_data import CATEGORIES, HOMEPAGE, PHOTOS  # noqa: E402
import site_seo  # noqa: E402

SLUG = "production-showcase"
URL = SITE + "/" + SLUG + "/"
IMG = "/assets/img/showcase/"
TITLE = "Event Production Showcase Türkiye | Stages, LED &amp; Branding"
H1 = "Event Production Showcase"
DESCRIPTION = (
    "Stages, LED walls, LED tunnels, registration desks, 3D lettering and venue branding "
    "built by DMC Turkey Partner for corporate events, dealer meetings and summits in "
    "Antalya and across Türkiye."
)
BEGIN = "<!-- production-showcase:begin -->"
END = "<!-- production-showcase:end -->"

PHOTO = {p[1]: p for p in PHOTOS}
CATEGORY = {c[0]: c for c in CATEGORIES}


def size(name):
    with Image.open(os.path.join(ROOT, IMG.strip("/"), name + ".webp")) as im:
        return im.size


def img(name, sizes, cls="", lazy=True):
    src, _, _, alt, _ = PHOTO[name]
    w, h = size(name)
    return (
        '<img%s src="%s%s.webp" srcset="%s%s-640.webp 640w, %s%s.webp %dw" sizes="%s" '
        'width="%d" height="%d" alt="%s"%s decoding="async">'
        % (' class="%s"' % cls if cls else "", IMG, name, IMG, name, IMG, name, w, sizes,
           w, h, esc(alt), ' loading="lazy"' if lazy else "")
    )


# --- homepage section ----------------------------------------------------------

def homepage_section():
    cards = []
    for i, (anchor, name) in enumerate(HOMEPAGE):
        _, title, line, _ = CATEGORY[anchor]
        large = i == 0
        cards.append(
            '        <a class="showcase-card%s" href="/%s/#%s">\n'
            "          %s\n"
            '          <span class="showcase-card__body">\n'
            '            <span class="showcase-card__title">%s</span>\n'
            '            <span class="showcase-card__text">%s</span>\n'
            "          </span>\n"
            "        </a>"
            % (" showcase-card--large" if large else "", SLUG, anchor,
               img(name, "(max-width: 640px) 80vw, (max-width: 900px) 50vw, %s"
                   % ("680px" if large else "480px"), "showcase-card__img"),
               title, line)
        )
    return (
        '    <section class="page-section showcase-home" aria-labelledby="showcase-home-title">\n'
        '      <div class="showcase-home__panel">\n'
        '        <div class="showcase-home__header">\n'
        '          <p class="showcase-home__eyebrow">Production Capabilities</p>\n'
        '          <h2 id="showcase-home-title">What We Build</h2>\n'
        '          <p class="showcase-home__lede">Stages, LED tunnels, show lighting and venue '
        "branding — designed, built and run on site by our team across Türkiye.</p>\n"
        "        </div>\n"
        '        <div class="showcase-grid">\n%s\n        </div>\n'
        '        <a class="showcase-home__all" href="/%s/">View the full production showcase &rarr;</a>\n'
        "      </div>\n"
        "    </section>" % ("\n".join(cards), SLUG)
    )


# --- gallery page --------------------------------------------------------------

def gallery_sections():
    out = []
    for anchor, title, _, intro in CATEGORIES:
        figures = []
        for _, name, cat, _, caption in PHOTOS:
            if cat != anchor:
                continue
            figures.append(
                '<figure class="showcase-figure">%s<figcaption>%s</figcaption></figure>'
                % (img(name, "(max-width: 640px) calc(100vw - 3rem), (max-width: 900px) 50vw, 380px"),
                   caption)
            )
        out.append(
            '    <section class="page-section showcase-category" id="%s">\n'
            "      <h2>%s</h2>\n"
            '      <p class="page-section__lede">%s</p>\n'
            '      <div class="showcase-gallery">\n        %s\n      </div>\n'
            "    </section>" % (anchor, title, intro, "\n        ".join(figures))
        )
    return "\n".join(out)


def schema():
    gallery = {
        "@context": "https://schema.org",
        "@type": "ImageGallery",
        "name": "Event Production Showcase — DMC Turkey Partner",
        "url": URL,
        "description": DESCRIPTION,
        "publisher": {"@id": SITE + "/#organization"},
        "about": [CATEGORY[a][1].replace("&amp;", "&") for a in CATEGORY],
        "associatedMedia": [
            {"@type": "ImageObject",
             "contentUrl": SITE + IMG + name + ".webp",
             "name": caption,
             "description": alt,
             "width": size(name)[0], "height": size(name)[1]}
            for _, name, _, alt, caption in PHOTOS
        ],
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
            for i, (n, p) in enumerate([("Home", "/"), ("Services", "/services/"),
                                        ("Event Production", "/services/event-production/"),
                                        ("Production Showcase", "/" + SLUG + "/")])
        ],
    }
    return "\n".join(
        '  <script type="application/ld+json">\n  %s\n  </script>'
        % json.dumps(d, ensure_ascii=False, separators=(",", ":")) for d in (gallery, crumbs)
    )


def render_page():
    hero_name = HOMEPAGE[0][1]
    og = SITE + IMG + hero_name + ".webp"
    head = "\n".join([
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
        "  <title>%s</title>" % TITLE,
        '  <meta name="description" content="%s">' % esc(DESCRIPTION),
        '  <link rel="canonical" href="%s">' % URL,
        '  <meta name="robots" content="index, follow, max-image-preview:large">',
        '  <meta property="og:type" content="website">',
        '  <meta property="og:title" content="%s">' % TITLE,
        '  <meta property="og:description" content="%s">' % esc(DESCRIPTION),
        '  <meta property="og:url" content="%s">' % URL,
        '  <meta property="og:site_name" content="DMC Turkey Partner">',
        '  <meta property="og:image" content="%s">' % og,
        '  <meta property="og:image:alt" content="%s">' % esc(PHOTO[hero_name][3]),
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s">' % og,
        '  <meta name="twitter:image:alt" content="%s">' % esc(PHOTO[hero_name][3]),
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        schema(),
        "</head>",
    ])
    jump = "".join('<a href="#%s">%s</a>' % (a, t) for a, t, _, _ in CATEGORIES)
    body = "\n".join([
        '      <nav class="breadcrumbs" aria-label="Breadcrumb">',
        "        <ol>",
        '          <li><a href="/">Home</a></li>',
        '          <li><a href="/services/">Services</a></li>',
        '          <li><a href="/services/event-production/">Event Production</a></li>',
        '          <li aria-current="page">Production Showcase</li>',
        "        </ol>",
        "      </nav>",
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>%s</h1>" % H1,
        '      <p class="page-section__lede">Stages, LED walls and tunnels, registration desks, '
        "3D lettering and full venue branding — a selection of what our production team has "
        "designed, built and operated for corporate events, dealer meetings, summits and "
        "ceremonies in Antalya and across Türkiye.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="/request-proposal/">'
        'Request a Proposal</a><a class="btn btn--ghost" href="/selected-works/">See Selected Works</a></div>',
        '      <div class="cluster-links showcase-jump">%s</div>' % jump,
        "    </section>",
        gallery_sections(),
        '    <section class="page-section">',
        '      <div class="cta-banner">',
        "        <h2>Planning a stage, entrance or full venue build in Türkiye?</h2>",
        "        <p>Send your brief and venue. Our production team will propose the build, "
        "materials and timeline.</p>",
        '        <div class="cta-banner__actions">',
        '          <a class="btn btn--primary" href="/request-proposal/">Request a Proposal</a>',
        '          <a class="btn btn--ghost" href="/services/event-production/">Event Production Services</a>',
        "        </div>",
        "      </div>",
        "    </section>",
    ])
    return head + "\n" + HEADER + '<main id="main-content">\n' + body + "\n  </main>" + FOOTER


def main():
    directory = os.path.join(ROOT, SLUG)
    os.makedirs(directory, exist_ok=True)
    page = os.path.join(directory, "index.html")
    with open(page, "w", encoding="utf-8") as handle:
        handle.write(render_page() + "\n")
    site_seo.patch(page, site_seo.identity_block())
    print("wrote /%s/ (%d photos)" % (SLUG, len(PHOTOS)))

    home = os.path.join(ROOT, "index.html")
    with open(home, encoding="utf-8") as handle:
        original = handle.read()
    pattern = re.compile(re.escape(BEGIN) + r".*?" + re.escape(END), re.S)
    if not pattern.search(original):
        raise SystemExit("Missing production-showcase markers in index.html")
    html = pattern.sub(lambda _m: BEGIN + "\n" + homepage_section() + "\n    " + END, original, count=1)
    if html != original:
        with open(home, "w", encoding="utf-8") as handle:
            handle.write(html)
    print("%s index.html" % ("updated" if html != original else "unchanged"))


if __name__ == "__main__":
    main()
