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
import site_header_cta  # noqa: E402
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


# Ordered by what applicants ask first: cost, flights, eligibility, dates. Answers repeat only what the
# campaign already states as proposed and subject to written confirmation; nothing new is promised.
FAQ = [
    ("Is the Fam Trip free to attend?",
     "Selected participants are expected to receive hosted accommodation, local transfers and scheduled programme "
     "activities. International flights and personal expenses are not included. Final arrangements will be confirmed "
     "in writing."),
    ("Do I need to book my own flights?",
     "Yes. International flights are expected to be arranged and funded by participants. Proposed local transfers will "
     "be subject to the final participation terms."),
    ("Who is eligible to apply?",
     "Agency owners, directors, decision-makers and professionals responsible for international MICE, incentive and "
     "corporate group programmes. Priority is given to agencies organising at least two international group "
     "programmes per year."),
    ("When will the Fam Trip take place?",
     "The proposed period is January to March 2027. Exact dates have not yet been confirmed and will be communicated "
     "to shortlisted applicants."),
    ("What is the Antalya & Belek Fam Trip 2027?",
     "A proposed three-night familiarisation programme designed for international MICE and incentive travel agencies "
     "to explore hotels, event venues, local experiences and potential DMC partnerships in Antalya and Belek."),
    ("How many agencies will be selected?",
     "Participation is expected to be limited to a small group of selected international agency representatives. "
     "Final capacity and selection criteria are subject to confirmation."),
    ("What will the three-night programme include?",
     "The indicative programme includes hotel and venue inspections, meetings with the local DMC operations team, "
     "incentive experiences and networking opportunities. The final itinerary may change."),
    ("What happens after I submit my application?",
     "The DMC Turkey Partner team will review your agency profile and contact shortlisted applicants with further "
     "details. Submitting an application does not guarantee participation."),
]


def faq_section():
    items = "".join('<details class="fam-faq__item"><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a))
                    for q, a in FAQ)
    return ('    <section class="page-section fam-faq" id="faq">\n      <h2>Frequently Asked Questions</h2>\n'
            '      <div class="fam-faq__list">%s</div>\n    </section>' % items)


def period_label(cfg):
    """campaignPeriod without its '(proposed)' suffix; every place that prints it already says 'Proposed'."""
    return cfg["campaignPeriod"].replace(" (proposed)", "")


IMAGES = os.path.join(ROOT, "campaign", "fam-trip-images.json")


def load_images():
    with open(IMAGES, encoding="utf-8") as handle:
        return {k: v for k, v in json.load(handle).items() if not k.startswith("_")}


def picture(img, sizes, eager=False, css=""):
    """<img> with a 640 px and a full-size source, explicit dimensions (no layout shift) and lazy loading
    below the fold. Only the first hero image is eager."""
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return ('<img%s src="%s-640.webp" srcset="%s-640.webp 640w, %s.webp %dw" sizes="%s" width="%d" height="%d" '
            'alt="%s" %s>' % (' class="%s"' % css if css else "", img["src"], img["src"], img["src"], img["width"],
                              sizes, img["width"], img["height"], esc(img["alt"]), loading))


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
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in FAQ]}
    ld = "\n".join('  <script type="application/ld+json">\n  %s\n  </script>' % json.dumps(d, ensure_ascii=False, separators=(",", ":"))
                   for d in (web, crumbs, faq))
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
        status=esc(cfg["applicationStatus"]), period=esc(period_label(cfg)), hidden=hidden,
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


PLANE_ICON = ('<svg width="28" height="28" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M2.5 10.5l15-7-4 13-3.2-4.2'
              '-3.3 2.2.5-3.6z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>')
SUITCASE_ICON = ('<svg width="28" height="28" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4 8h16v11H4zM9 8V5h6v3" '
                 'fill="none" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/></svg>')


def page_body(cfg):
    im = load_images()
    hero = ('<div class="fam-hero-media"><figure class="fam-hero-media__main">%s<figcaption>%s</figcaption></figure>'
            '<figure class="fam-hero-media__side">%s<figcaption>%s</figcaption></figure></div>'
            % (picture(im["hero_a"], "(max-width: 900px) 100vw, 560px", eager=True), esc(im["hero_a"]["caption"]),
               picture(im["hero_b"], "280px"), esc(im["hero_b"]["caption"])))
    why = [("why_hotels", "Hotels &amp; venues", "Explore Antalya and Belek hotels and event venues, and see what they can offer your future client programmes."),
           ("why_team", "Local team", "Meet the local operations and destination team who would run those programmes on the ground."),
           ("why_experiences", "Experiences", "Discover incentive activities and group experiences for memorable client programmes."),
           ("why_whitelabel", "White-label delivery", "Explore white-label programme delivery and RFP collaboration with your agency in the lead.")]
    cards = "".join('<article class="fam-card">%s<div class="fam-card__body"><h3>%s</h3><p>%s</p></div></article>'
                    % (picture(im[k], "(max-width: 640px) 100vw, 360px"), h, t) for k, h, t in why)
    stage = lambda n, title, text, media: ('<li class="fam-stage"><div class="fam-stage__media">%s</div><div><span class="fam-stage__day">'
                                           'Day %d</span><h3>%s</h3><p>%s</p></div></li>' % (media, n, title, text))
    timeline = "".join([
        stage(1, "Arrival &amp; welcome", "Arrival, hotel check-in and welcome dinner.", '<span class="fam-stage__icon">%s</span>' % PLANE_ICON),
        stage(2, "Hotel &amp; venue inspections", "Hotel and venue inspections across Antalya and Belek.", picture(im["day2"], "96px")),
        stage(3, "Experiences &amp; networking", "Incentive experience, operations presentation and networking dinner.", picture(im["day3"], "96px")),
        stage(4, "Departure", "Breakfast, airport transfer and departure.", '<span class="fam-stage__icon">%s</span>' % SUITCASE_ICON),
    ])
    glance = (
        '    <section class="fam-glance" aria-labelledby="fam-glance-title">\n'
        '      <h2 id="fam-glance-title">Your Fam Trip at a Glance</h2>\n'
        '      <dl class="fam-glance__grid"><div><dt>Proposed period</dt><dd>%s</dd></div><div><dt>Duration</dt><dd>3 nights</dd></div>'
        '<div><dt>Destinations</dt><dd>Antalya &amp; Belek</dd></div><div><dt>Audience</dt><dd>MICE agencies</dd></div></dl>\n'
        '      <ul class="fam-glance__notes"><li>Proposed hosted accommodation and local programme</li>'
        '<li>International flights arranged by participants</li></ul>\n'
        '      <p class="fam-glance__fine">All arrangements are subject to written confirmation.</p>\n'
        '      <a class="btn btn--primary" href="#apply">Register Your Interest</a>\n'
        '    </section>' % esc(period_label(cfg)))
    return "\n".join([
        '      <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Home</a></li>'
        '<li aria-current="page">Agency Fam Trip 2027</li></ol></nav>',
        '    <section class="page-section" data-cta-location="hero">',
        '      <p class="fam-eyebrow">Agency Fam Trip 2027</p>',
        # Server-rendered H1 is the same for everybody and for search engines; the country-specific invitation
        # line below it is swapped client-side only (assets/js/fam-trip-campaign.js).
        '      <h1>Antalya &amp; Belek Fam Trip 2027 for MICE Agencies</h1>',
        '      <p class="fam-invite" data-fam-headline>Exclusive MICE Agency Fam Trip Invitation</p>',
        '      <p class="fam-subline"><strong>Experience Antalya &amp; Belek in 2027. Discover Your Local DMC Partner.</strong></p>',
        '      <p class="page-section__lede">Experience the destination, meet the people behind the operations and explore how '
        "DMC Turkey Partner can support your agency’s programmes in Türkiye.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="#apply">Register Your Interest</a></div>',
        "      " + hero,
        "    </section>",
        glance,
        '    <section class="page-section">',
        "      <h2>Why Join</h2>",
        '      <div class="fam-cards">' + cards + "</div>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Proposed 3-Night Programme</h2>",
        '      <p class="page-section__lede">Indicative programme, subject to confirmation.</p>',
        '      <ol class="fam-timeline">' + timeline + "</ol>",
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Who Should Apply</h2>",
        "      <ul><li>Incentive and MICE agencies based in Europe and the United States.</li><li>Corporate event and group travel planners.</li>"
        "<li>Agency owners, directors and senior decision-makers.</li>"
        "<li>Professionals managing international group programmes.</li></ul>",
        "      <p>Priority is given to applicants whose agencies organise at least two international group programmes annually.</p>",
        "    </section>",
        '    <section class="page-section fam-participation">',
        "      <h2>Participation</h2>",
        '      <div class="fam-participation__grid">'
        '<div class="fam-participation__col"><h3>Proposed hosted</h3><ul><li>Accommodation</li><li>Local transfers</li>'
        "<li>Scheduled programme activities</li></ul></div>"
        '<div class="fam-participation__col"><h3>Not included</h3><ul><li>International flights</li><li>Personal expenses</li></ul></div>'
        '<div class="fam-participation__col"><h3>Eligibility</h3><ul><li>Agency owners, directors and decision-makers</li>'
        "<li>Priority for agencies with at least two international group programmes a year</li></ul></div></div>",
        "      <p>International flights are expected to be arranged by participants.</p>",
        '      <p>Read the <a href="/antalya-fam-trip-2027/">2027 programme and eligibility details</a>, or see our '
        '<a href="/antalya-fam-trips/">Antalya fam trip service</a> if you want a fam trip for your own group.</p>',
        '      <p class="price-note">All inclusions, exclusions, dates, eligibility and cancellation conditions remain subject to written confirmation.</p>',
        "    </section>",
        faq_section(),
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
    on, changed = site_header_cta.run()
    print("header CTA %s: %d pages updated" % ("enabled" if on else "disabled", len(changed)))
    if cfg["enabled"] and not cfg["formspreeEndpoint"]:
        print("WARNING: enabled but formspreeEndpoint is empty; the form stays closed.")


if __name__ == "__main__":
    main()
