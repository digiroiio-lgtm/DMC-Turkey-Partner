#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Agency Fam Trip 2027 landing page and apply the campaign settings.

Usage: python3 tools/fam_trip_build.py   (then: python3 tools/sitemaps.py)

Reads campaign/uk-fam-trip.json (single source of settings) and:
  * writes agency-fam-trip-2027/index.html (noindex while enabled=false),
  * rewrites the config block in assets/js/fam-trip-campaign.js.
Idempotent. While the campaign is disabled the page is noindex and tools/sitemaps.py
does not list it; set "enabled": true and a Formspree endpoint to launch.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import SITE, esc  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT  # noqa: E402
import site_seo  # noqa: E402

PATH = "/agency-fam-trip-2027/"
URL = SITE + PATH
SETTINGS = os.path.join(ROOT, "campaign", "uk-fam-trip.json")
JS = os.path.join(ROOT, "assets", "js", "fam-trip-campaign.js")
JS_BEGIN = "/* fam-config:begin */"
JS_END = "/* fam-config:end */"

TITLE = "Antalya & Belek Fam Trip 2027 for MICE Agencies | DMC Turkey Partner"
DESCRIPTION = ("Register your interest in a curated Antalya and Belek familiarisation trip for incentive and MICE "
               "agencies. Explore venues, local operations and white-label partnerships.")
IMAGE = "/assets/img/mapfre-sigorta-antalya-gala-dinner"


def load():
    with open(SETTINGS, encoding="utf-8") as handle:
        data = json.load(handle)
    return {k: v for k, v in data.items() if not k.startswith("_")}


def write_js_config(cfg):
    with open(JS, encoding="utf-8") as handle:
        source = handle.read()
    body = json.dumps(cfg, ensure_ascii=False, indent=4).replace("\n", "\n  ")
    block = "%s\n  var CONFIG = %s;\n  %s" % (JS_BEGIN, body, JS_END)
    updated = re.sub(re.escape(JS_BEGIN) + r".*?" + re.escape(JS_END), lambda _m: block, source, count=1, flags=re.S)
    if updated != source:
        with open(JS, "w", encoding="utf-8") as handle:
            handle.write(updated)
    return updated != source


def head(cfg):
    robots = "index, follow" if cfg["enabled"] else "noindex, follow"
    web = {"@context": "https://schema.org", "@type": "WebPage", "name": TITLE, "url": URL, "description": DESCRIPTION,
           "inLanguage": "en", "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                                  {"@type": "ListItem", "position": 2, "name": "Agency Fam Trip 2027", "item": URL}]}
    ld = "\n".join('  <script type="application/ld+json">\n  %s\n  </script>' % json.dumps(d, ensure_ascii=False, separators=(",", ":"))
                   for d in (web, crumbs))
    return "\n".join([
        "<!DOCTYPE html>", '<html lang="en">', "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '  <link rel="icon" href="/favicon.ico" sizes="any">',
        '  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
        '  <link rel="manifest" href="/site.webmanifest">',
        "  <title>%s</title>" % esc(TITLE),
        '  <meta name="description" content="%s">' % esc(DESCRIPTION),
        '  <link rel="canonical" href="%s">' % URL,
        '  <meta name="robots" content="%s">' % robots,
        '  <meta property="og:type" content="website">',
        '  <meta property="og:title" content="%s">' % esc(TITLE),
        '  <meta property="og:description" content="%s">' % esc(DESCRIPTION),
        '  <meta property="og:url" content="%s">' % URL,
        '  <meta property="og:site_name" content="DMC Turkey Partner">',
        '  <meta property="og:locale" content="en">',
        '  <meta property="og:image" content="%s%s.webp">' % (SITE, IMAGE),
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s%s.webp">' % (SITE, IMAGE),
        '  <meta name="dmc:lead-source" content="Agency Fam Trip">',
        '  <meta name="dmc:page-type" content="campaign-landing">',
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        '  <link rel="stylesheet" href="/assets/css/forms.css">',
        '  <link rel="stylesheet" href="/assets/css/fam-trip.css">',
        ld, "</head>",
    ])


def field(label, name, kind="text", required=False, extra="", autocomplete=""):
    req = " required" if required else ""
    ac = ' autocomplete="%s"' % autocomplete if autocomplete else ""
    opt = "" if required else ' <span class="field-optional">(optional)</span>'
    return ('<div class="form-field"><label for="fam-%s">%s%s</label>'
            '<input type="%s" id="fam-%s" name="%s" data-label="%s"%s%s%s></div>'
            % (name, label, opt, kind, name, name, label, req, ac, extra))


def select(label, name, options, required=False, placeholder="Select an option"):
    req = " required" if required else ""
    opt = "" if required else ' <span class="field-optional">(optional)</span>'
    items = "".join('<option value="%s">%s</option>' % (esc(o), esc(o)) for o in options)
    return ('<div class="form-field"><label for="fam-%s">%s%s</label>'
            '<select id="fam-%s" name="%s" data-label="%s"%s><option value="">%s</option>%s</select></div>'
            % (name, label, opt, name, name, label, req, placeholder, items))


def form_section(cfg):
    hidden = "".join('<input type="hidden" name="%s"%s>' % (n, ' value="%s"' % v if v else "") for n, v in [
        ("campaign_source", ""), ("lead_status", "New"), ("submitted_at", ""), ("consent_timestamp", ""),
        ("landing_page", ""), ("submission_source", ""), ("marketing_optin_status", ""),
        ("utm_source", ""), ("utm_medium", ""), ("utm_campaign", ""), ("utm_content", ""), ("utm_term", ""), ("visitor_country", ""),
        ("_subject", "Agency Fam Trip 2027 application")])
    return '''    <section class="page-section fam-apply" id="apply" data-fam-apply>
      <h2>Apply for the 2027 Fam Trip</h2>
      <p class="page-section__lede">Status: %(status)s. Proposed period: %(period)s. Applications are reviewed individually.</p>
      <div class="fam-closed" data-fam-closed>
        <p><strong>Applications are not open yet.</strong> We will open the application form once the programme and hosted arrangements are confirmed. To be told when it opens, email <a href="mailto:hello@dmcturkeypartner.com">hello@dmcturkeypartner.com</a>.</p>
      </div>
      <form class="fam-form" name="fam-trip-application" method="POST" novalidate data-fam-form hidden>
        <p class="sr-only"><label>Leave this field empty <input name="_gotcha" tabindex="-1" autocomplete="off"></label></p>
        %(hidden)s
        <div class="form-grid">
          %(name)s
          %(email)s
          %(agency)s
          %(job)s
          %(country)s
          %(programmes)s
          %(role)s
          %(website)s
          %(group)s
          %(period_field)s
          <div class="form-field form-field--full"><label for="fam-comments">Additional comments <span class="field-optional">(optional)</span></label>
            <textarea id="fam-comments" name="comments" maxlength="1500"></textarea></div>
          <label class="fam-form__check form-field--full"><input type="checkbox" name="privacy_ack" value="Yes" required data-label="privacy acknowledgement">
            <span>I have read the <a href="/privacy-policy/">Privacy Policy</a> and agree that my application details are used to assess my application and contact me about it.</span></label>
          <label class="fam-form__check form-field--full"><input type="checkbox" name="marketing_optin" value="Yes">
            <span>Optional: I would also like to receive occasional DMC Turkey Partner updates by email. I can unsubscribe at any time.</span></label>
          <p class="form-note form-field--full">Please do not include passport, payment card or other sensitive personal details.</p>
          <p class="form-error" data-fam-error role="alert" hidden></p>
          <div class="form-actions"><button type="submit" class="btn btn--primary">Submit Application</button></div>
        </div>
      </form>
      <section class="fam-success" data-fam-success hidden aria-live="polite">
        <h2 tabindex="-1">Thank You for Your Interest!</h2>
        <p>Your application has been received. Our team will review your details and contact shortlisted applicants with further information.</p>
      </section>
    </section>''' % dict(
        status=esc(cfg["applicationStatus"]), period=esc(cfg["campaignPeriod"]), hidden=hidden,
        name=field("Full name", "full_name", required=True, autocomplete="name"),
        email=field("Business email", "email", "email", True, ' inputmode="email"', "email"),
        agency=field("Agency / company name", "agency", required=True, autocomplete="organization"),
        job=field("Job title", "job_title", required=True, autocomplete="organization-title"),
        country=field("Country", "country", required=True, autocomplete="country-name"),
        programmes=select("International group programmes per year", "programmes_per_year", ["0–1", "2–5", "6–10", "11+"], True),
        role=select("Decision-making role", "decision_role", ["Decision Maker", "Influencer", "Other"], True),
        website=field("Company website", "website", "text", False, ' inputmode="url" autocomplete="url"'),
        group=field("Estimated group size", "group_size", "text", False, ' inputmode="numeric"'),
        period_field=select("Preferred travel period", "travel_period", ["January", "February", "March 2027", "Flexible"], False))


def page_body(cfg):
    img = ('<img class="fam-hero-image" src="%s-640.webp" srcset="%s-640.webp 640w, %s.webp 1179w" '
           'sizes="(max-width: 900px) 100vw, 760px" width="1179" height="798" '
           'alt="Gala dinner with stage lighting and LED screens at a corporate event in Antalya" fetchpriority="high">'
           % (IMAGE, IMAGE, IMAGE))
    card = lambda h, p: '<article class="card"><h3>%s</h3><p>%s</p></article>' % (h, p)
    return "\n".join([
        '      <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
        '<li aria-current="page">Agency Fam Trip 2027</li></ol></nav>',
        '    <section class="page-section" data-cta-location="hero">',
        '      <p class="fam-eyebrow">Agency Fam Trip 2027</p>',
        '      <h1 data-fam-headline>Exclusive MICE Agency Fam Trip Invitation</h1>',
        '      <p class="fam-subline"><strong>Experience Antalya &amp; Belek in 2027. Discover Your Local DMC Partner.</strong></p>',
        '      <p class="page-section__lede">Experience the destination, meet the people behind the operations and explore how '
        "DMC Turkey Partner can support your agency’s programmes in Türkiye.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="#apply">Register Your Interest</a></div>',
        "      " + img,
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Why Join</h2>",
        '      <div class="card-grid">' + "".join([
            card("Hotels &amp; venues", "Explore Antalya and Belek hotels and event venues."),
            card("Local team", "Meet the local operations and destination team."),
            card("Experiences", "Discover incentive activities and group experiences."),
            card("White-label delivery", "Explore white-label programme delivery and RFP collaboration."),
        ]) + "</div>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Proposed 3-Night Programme</h2>",
        '      <p class="page-section__lede">Indicative programme, subject to confirmation.</p>',
        '      <ol class="fam-programme">'
        "<li><strong>Day 1</strong>Arrival, hotel check-in and welcome dinner.</li>"
        "<li><strong>Day 2</strong>Hotel and venue inspections across Antalya and Belek.</li>"
        "<li><strong>Day 3</strong>Incentive experience, operations presentation and networking dinner.</li>"
        "<li><strong>Day 4</strong>Breakfast, airport transfer and departure.</li></ol>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Who Should Apply</h2>",
        "      <ul><li>Incentive and MICE agencies based in Europe and the United States.</li><li>Corporate event and group travel planners.</li>"
        "<li>Agency owners, directors and senior decision-makers.</li>"
        "<li>Professionals managing international group programmes.</li></ul>",
        "      <p>Priority is given to applicants whose agencies organise at least two international group programmes annually.</p>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Participation</h2>",
        "      <p>Proposed hosted elements:</p>",
        "      <ul><li>Accommodation</li><li>Local transfers</li><li>Scheduled programme activities</li></ul>",
        "      <p>International flights are expected to be arranged by participants.</p>",
        '      <p>Read the <a href="/antalya-fam-trip-2027/">2027 programme and eligibility details</a>, or see our '
        '<a href="/antalya-fam-trips/">Antalya fam trip service</a> if you want a fam trip for your own group.</p>',
        '      <p class="price-note">All inclusions, exclusions, dates, eligibility and cancellation conditions remain subject to written confirmation.</p>',
        "    </section>",
        form_section(cfg),
        '    <section class="page-section">',
        '      <div class="cta-banner"><h2>Register Your Interest for Our 2027 Antalya Fam Trip</h2>'
        '<div class="cta-banner__actions"><a class="btn btn--primary" href="#apply">Register Your Interest</a></div></div>',
        "    </section>",
    ])


def render(cfg):
    return head(cfg) + "\n" + HEADER + '<main id="main-content">\n' + page_body(cfg) + "\n  </main>" + FOOTER


def main():
    cfg = load()
    path = os.path.join(ROOT, "agency-fam-trip-2027", "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(render(cfg) + "\n")
    site_seo.patch(path, site_seo.identity_block())
    print("wrote /agency-fam-trip-2027/ (%s)" % ("ENABLED" if cfg["enabled"] else "disabled, noindex"))
    print("%s assets/js/fam-trip-campaign.js" % ("updated" if write_js_config(cfg) else "unchanged"))
    if cfg["enabled"] and not cfg["formspreeEndpoint"]:
        print("WARNING: enabled but formspreeEndpoint is empty; the form stays closed.")


if __name__ == "__main__":
    main()
