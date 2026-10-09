#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build /antalya-transfer-prices/ and refresh every transfer price block.

Usage: python3 tools/transfer_prices_build.py

Prices live in tools/transfer_prices.py. This script:
1. writes antalya-transfer-prices/index.html from that data;
2. replaces the content between `<!-- transfer-prices:NAME:begin/end -->`
   markers on the pages listed in TARGETS.

It does not regenerate the COP31 cluster: those pages carry hand edits made
after generation, so only their marker blocks are touched here. The same
blocks are referenced from the cop31_pages_* sources so a future full build
keeps them.

Idempotent: re-running with unchanged data changes nothing.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import SITE, esc  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT  # noqa: E402
import site_seo  # noqa: E402
import transfer_pricing as tp  # noqa: E402
from transfer_prices import (  # noqa: E402
    ALTERNATIVES_NOTE,
    CURRENCY,
    DISCLAIMER,
    PRICES_REVIEWED,
    PRICES_REVIEWED_LABEL,
    SERVICES,
    VEHICLES,
)

SLUG = "antalya-transfer-prices"
URL = SITE + "/" + SLUG + "/"
TITLE = "Antalya Transfer Prices | Airport, Shuttle &amp; Driver"
H1 = "Antalya Airport and Group Transfer Prices"
DESCRIPTION = (
    "Indicative Antalya transfer prices per vehicle in EUR: airport transfers, daily "
    "conference shuttles and full-day vehicles with driver, from sedans to 50-seat coaches."
)

# Pages carrying marker blocks, and which blocks each one carries.
TARGETS = {
    "event-costs/index.html": ["event-costs"],
    "services/transportation-logistics/index.html": ["transport-logistics"],
    "cop31-antalya-airport-transfer/index.html": ["airport"],
    "cop31-private-transfers/index.html": ["shuttle-full-day"],
    "cop31-antalya-transport/index.html": ["cop31-transport"],
}

FAQS = [
    ("Are these prices per person or per vehicle?",
     "Per vehicle. The price is the same whether a minibus carries 8 or 19 passengers, "
     "so the right vehicle size matters more than the headcount."),
    ("How much luggage fits?",
     "Capacities assume normal suitcases. Oversized items, equipment cases or a seat for a "
     "group coordinator can mean a larger vehicle — tell us the luggage when you ask for a quote."),
    ("Our group arrives on different flights. How is that priced?",
     "Each vehicle movement is priced separately. Where flights land close together we can "
     "combine passengers into one vehicle; where they do not, waiting beyond the included 60 "
     "minutes is charged per hour, or a second vehicle is usually cheaper."),
    ("Is a return airport transfer double the one-way price?",
     "Yes — the airport price is one way, so arrival and departure are two transfers. Book "
     "both together so the return is reserved."),
    ("What is the difference between the daily shuttle and a full-day vehicle?",
     "The daily shuttle is one run out and one run back, with the vehicle released in "
     "between. A full-day vehicle stays with your group for 10 hours and can make as many "
     "movements as the programme needs. They are alternatives, not combined."),
]


# --- page --------------------------------------------------------------------

def _form():
    services = "".join(
        "<option>%s</option>" % s["label"] for s in SERVICES
    ) + "<option>Not sure yet</option>"
    return """<section class="page-section transfer-quote" id="transfer-quote">
      <h2>Request a Transfer Quote</h2>
      <p class="page-section__lede">Send the dates, passengers, luggage and route. We confirm vehicles and a firm price.</p>
      <form name="transfer-quote" method="POST" action="/api/request-proposal" data-proposal-form>
        <p class="sr-only"><label>Company website <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
        <input type="hidden" name="source_page">
        <input type="hidden" name="landing_page">
        <input type="hidden" name="submission_page">
        <input type="hidden" name="timestamp">
        <input type="hidden" name="utm_source">
        <input type="hidden" name="utm_medium">
        <input type="hidden" name="utm_campaign">
        <input type="hidden" name="utm_content">
        <input type="hidden" name="utm_term">
        <input type="hidden" name="lead_source">
        <input type="hidden" name="campaign">
        <input type="hidden" name="service_interest">
        <input type="hidden" name="page_type">
        <input type="hidden" name="destination" value="Antalya">
        <input type="hidden" name="project_type" value="Transfer">
        <div class="form-grid">
          <div class="form-field">
            <label for="transfer-name">Your Name</label>
            <input type="text" id="transfer-name" name="name" autocomplete="name" required>
          </div>
          <div class="form-field">
            <label for="transfer-company">Company</label>
            <input type="text" id="transfer-company" name="company" autocomplete="organization" required>
          </div>
          <div class="form-field">
            <label for="transfer-email">Work Email</label>
            <input type="email" id="transfer-email" name="email" autocomplete="email" inputmode="email" required>
          </div>
          <div class="form-field">
            <label for="transfer-service">Service</label>
            <select id="transfer-service" name="service_type" required>
              <option value="">Select a service</option>%s
            </select>
          </div>
          <fieldset class="form-field">
            <legend>Transfer Dates</legend>
            <div class="date-range">
              <label for="transfer-date-start" class="sr-only">First transfer date</label>
              <input type="date" id="transfer-date-start" name="date_start">
              <label for="transfer-date-end" class="sr-only">Last transfer date</label>
              <input type="date" id="transfer-date-end" name="date_end">
            </div>
            <label class="form-check"><input type="checkbox" id="transfer-dates-unconfirmed" name="dates_unconfirmed" value="Yes"> Dates Not Confirmed</label>
          </fieldset>
          <div class="form-field">
            <label for="transfer-passengers">Passengers</label>
            <input type="number" id="transfer-passengers" name="group_size" min="1" max="2000" inputmode="numeric" required>
          </div>
          <div class="form-field">
            <label for="transfer-luggage">Luggage</label>
            <input type="text" id="transfer-luggage" name="luggage" placeholder="e.g. 1 suitcase each, 4 equipment cases">
          </div>
          <div class="form-field">
            <label for="transfer-pickup">Pick-up Point</label>
            <input type="text" id="transfer-pickup" name="pickup" placeholder="e.g. Antalya Airport (AYT)">
          </div>
          <div class="form-field">
            <label for="transfer-dropoff">Drop-off Point</label>
            <input type="text" id="transfer-dropoff" name="dropoff" placeholder="e.g. hotel name, Belek">
          </div>
          <div class="form-field form-field--full">
            <label for="transfer-brief">Flights, times or anything else <span class="field-optional">(optional)</span></label>
            <textarea id="transfer-brief" name="brief" placeholder="Flight numbers, programme times, return journeys..."></textarea>
          </div>
          <p class="form-note form-field--full">We use your contact details to respond to this enquiry, as explained in our <a href="/privacy-policy/">Privacy Policy</a>. A quote request is not a booking. Please do not include passport, payment card or sensitive personal details.</p>
          <p class="form-error" data-proposal-error role="alert" hidden></p>
          <div class="form-actions"><button type="submit" class="btn btn--primary">Request a Transfer Quote</button></div>
        </div>
      </form>
      <section class="proposal-success" data-proposal-success hidden aria-live="polite">
        <h2>Thank you — we’ve received your request.</h2>
        <p>Our Antalya operations team will confirm vehicles and pricing by email.</p>
      </section>
    </section>""" % services


def _faq():
    items = "".join(
        '<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (q, a) for q, a in FAQS
    )
    return (
        '<section class="page-section">\n'
        "      <h2>Frequently Asked Questions</h2>\n"
        '      <div class="faq-list">%s</div>\n'
        "    </section>" % items
    )


def _offers():
    offers = []
    for s in SERVICES:
        for v in VEHICLES:
            price = v[s["key"]]
            spec = {"@type": "UnitPriceSpecification", "priceCurrency": CURRENCY,
                    "unitText": s["unit"], "valueAddedTaxIncluded": False}
            if price is None:
                spec["description"] = "Price on request"
            else:
                spec["price"] = price
            offers.append({
                "@type": "Offer",
                "name": "%s — %s, %s" % (s["label"], v["label"], v["capacity"].rstrip("*")),
                "description": s["inclusion"].replace("&amp;", "&"),
                "priceSpecification": spec,
            })
    return offers


def _schema():
    org = {"@id": SITE + "/#organization"}
    service = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": "Antalya airport transfers, shuttles and vehicles with driver",
        "serviceType": "Ground transportation",
        "url": URL,
        "provider": org,
        "areaServed": {"@type": "City", "name": "Antalya",
                       "address": {"@type": "PostalAddress", "addressLocality": "Antalya",
                                   "addressCountry": "TR"}},
        "description": DISCLAIMER,
        "hasOfferCatalog": {"@type": "OfferCatalog",
                            "name": "Antalya transfer prices per vehicle",
                            "itemListElement": _offers()},
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQS
        ],
    }
    crumbs = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE + path}
            for i, (name, path) in enumerate([
                ("Home", "/"), ("Services", "/services/"),
                ("Transportation & Logistics", "/services/transportation-logistics/"),
                ("Antalya Transfer Prices", "/" + SLUG + "/"),
            ])
        ],
    }
    return "\n".join(
        '  <script type="application/ld+json">\n  %s\n  </script>'
        % json.dumps(d, ensure_ascii=False, separators=(",", ":"))
        for d in (service, faq, crumbs)
    )


def render_page():
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
        '  <meta name="robots" content="index, follow">',
        '  <meta property="og:type" content="website">',
        '  <meta property="og:title" content="%s">' % TITLE,
        '  <meta property="og:description" content="%s">' % esc(DESCRIPTION),
        '  <meta property="og:url" content="%s">' % URL,
        '  <meta property="og:site_name" content="DMC Turkey Partner">',
        '  <meta property="og:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s/assets/img/social-preview.png">' % SITE,
        # Read by main.js so the quote form and header CTAs carry the source.
        '  <meta name="dmc:lead-source" content="Antalya Transfer Prices">',
        '  <meta name="dmc:service-interest" content="Antalya Transfers">',
        '  <meta name="dmc:page-type" content="pricing">',
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        '  <link rel="stylesheet" href="/assets/css/forms.css">',
        _schema(),
        "</head>",
    ])

    body = "\n".join([
        '      <nav class="breadcrumbs" aria-label="Breadcrumb">',
        "        <ol>",
        '          <li><a href="/">Home</a></li>',
        '          <li><a href="/services/">Services</a></li>',
        '          <li><a href="/services/transportation-logistics/">Transportation &amp; Logistics</a></li>',
        '          <li aria-current="page">Antalya Transfer Prices</li>',
        "        </ol>",
        "      </nav>",
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>%s</h1>" % H1,
        '      <p class="page-section__lede">Indicative prices per vehicle for the three ways groups '
        "move around Antalya: airport transfers, daily conference and hotel shuttles, and a "
        "vehicle with driver dedicated to your programme for the day. Sedans to 50-seat coaches, "
        "operated by our Antalya team.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="#transfer-quote">'
        "Request a Transfer Quote</a></div>",
        '      <p class="reviewed-note">Prices reviewed: <time datetime="%s">%s</time>.</p>'
        % (PRICES_REVIEWED, PRICES_REVIEWED_LABEL),
        "    </section>",
        '    <section class="page-section transfer-prices">',
        "      <h2>Transfer Prices by Vehicle</h2>",
        "      " + tp.main_table(),
        "    </section>",
        '    <section class="page-section transfer-prices">',
        "      <h2>What Each Price Includes</h2>",
        "      " + tp.inclusions_table(),
        "      " + tp._note(ALTERNATIVES_NOTE),
        "    </section>",
        '    <section class="page-section transfer-prices">',
        "      <h2>Extra Hours and Kilometres</h2>",
        "      " + tp.extras_table(),
        "      " + tp.disclaimer(),
        "    </section>",
        "    " + _faq(),
        "    " + _form(),
        '    <section class="page-section">',
        "      <h2>Related</h2>",
        '      <div class="cluster-links"><a href="/services/transportation-logistics/">'
        "Group Transportation in Turkey</a><a href=\"/cop31-antalya-airport-transfer/\">COP31 "
        "Airport Transfers</a><a href=\"/cop31-private-transfers/\">COP31 Private Transfers</a>"
        '<a href="/destinations/antalya/">Antalya DMC</a><a href="/event-costs/antalya/">'
        "Antalya Event Costs</a></div>",
        "    </section>",
    ])

    return head + "\n" + HEADER + '<main id="main-content">\n' + body + "\n  </main>" + FOOTER


# --- marker blocks ------------------------------------------------------------

def refresh_blocks(rel_path, names):
    path = os.path.join(ROOT, rel_path)
    with open(path, encoding="utf-8") as handle:
        original = handle.read()
    html = original
    for name in names:
        pattern = re.compile(re.escape(tp.begin(name)) + r".*?" + re.escape(tp.end(name)), re.S)
        if not pattern.search(html):
            raise SystemExit("Missing transfer-prices:%s markers in %s" % (name, rel_path))
        html = pattern.sub(lambda _m: tp.block(name), html, count=1)
    if html == original:
        return False
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html)
    return True


def main():
    directory = os.path.join(ROOT, SLUG)
    os.makedirs(directory, exist_ok=True)
    page = os.path.join(directory, "index.html")
    with open(page, "w", encoding="utf-8") as handle:
        handle.write(render_page() + "\n")
    # Identity schema and the consent-aware analytics loader, as on every page.
    site_seo.patch(page, site_seo.identity_block())
    print("wrote /%s/" % SLUG)

    for rel_path, names in TARGETS.items():
        changed = refresh_blocks(rel_path, names)
        print("%s %s" % ("updated" if changed else "unchanged", rel_path))


if __name__ == "__main__":
    main()
