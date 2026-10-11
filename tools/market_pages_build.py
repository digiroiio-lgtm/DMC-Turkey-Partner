#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the market landing pages: a UK-agency page and a German page.

Usage: python3 tools/market_pages_build.py

Writes:
  dmc-turkey-uk-agencies/index.html   (English, UK agencies and planners)
  de/dmc-tuerkei/index.html           (German, DMC Türkei)
Idempotent. Only facts that already appear elsewhere on the site are used
(flight times and carriers from /why-turkey/ and the destination guides,
reference ranges from /event-costs/, credentials from the footer). No new
prices, discounts or promises. The German copy should be reviewed by a native
speaker before it is promoted. hreflang: de <-> en (/dmc-turkey/) + x-default;
the reciprocal tags live in dmc-turkey/index.html.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import SITE, esc  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT, table  # noqa: E402
import site_seo  # noqa: E402

UPDATED_ISO = "2026-10-11"
UK_PATH = "/dmc-turkey-uk-agencies/"
DE_PATH = "/de/dmc-tuerkei/"
EN_PEER = "/dmc-turkey/"


# --- shared pieces ---------------------------------------------------------------

def head(lang, title, description, path, lead_source, service_interest, schema_blocks, hreflang=""):
    url = SITE + path
    locale = '  <meta property="og:locale" content="de_DE">' if lang == "de" else ""
    return "\n".join(filter(None, [
        "<!DOCTYPE html>", '<html lang="%s">' % lang, "<head>",
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '  <link rel="icon" href="/favicon.ico" sizes="any">',
        '  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">',
        '  <link rel="manifest" href="/site.webmanifest">',
        "  <title>%s</title>" % esc(title),
        '  <meta name="description" content="%s">' % esc(description),
        '  <link rel="canonical" href="%s">' % url,
        hreflang,
        '  <meta name="robots" content="index, follow">',
        '  <meta property="og:type" content="website">',
        '  <meta property="og:title" content="%s">' % esc(title),
        '  <meta property="og:description" content="%s">' % esc(description),
        '  <meta property="og:url" content="%s">' % url,
        '  <meta property="og:site_name" content="DMC Turkey Partner">',
        locale,
        '  <meta property="og:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="dmc:lead-source" content="%s">' % lead_source,
        '  <meta name="dmc:service-interest" content="%s">' % service_interest,
        '  <meta name="dmc:page-type" content="market-landing">',
        '  <link rel="stylesheet" href="/assets/css/main.css">',
        '  <link rel="stylesheet" href="/assets/css/forms.css">',
        schema_blocks, "</head>",
    ]))


def schema(lang, name, path, description, crumbs, faqs):
    url = SITE + path
    web = {"@context": "https://schema.org", "@type": "WebPage", "name": name, "url": url,
           "description": description, "inLanguage": lang, "dateModified": UPDATED_ISO,
           "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                              for i, (n, p) in enumerate(crumbs)]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                         for q, a in faqs]}
    return "\n".join('  <script type="application/ld+json">\n  %s\n  </script>'
                     % json.dumps(d, ensure_ascii=False, separators=(",", ":")) for d in (web, bc, fq))


def crumbs_html(items):
    lis = "".join('<li><a href="%s">%s</a></li>' % (p, n) for n, p in items[:-1])
    lis += '<li aria-current="page">%s</li>' % items[-1][0]
    return '      <nav class="breadcrumbs" aria-label="Breadcrumb"><ol>%s</ol></nav>' % lis


def faq_html(heading, items):
    body = "".join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (esc(q), esc(a)) for q, a in items)
    return ('    <section class="page-section">\n      <h2>%s</h2>\n'
            '      <div class="faq-list">%s</div>\n    </section>' % (heading, body))


def cards(items):
    return '<div class="card-grid">%s</div>' % "".join(
        '<article class="card"><h3>%s</h3><p>%s</p></article>' % (h, p) for h, p in items)


def steps(items):
    return '<ol class="steps-list">%s</ol>' % "".join(
        "<li><h3>%s</h3><p>%s</p></li>" % (h, p) for h, p in items)


def assemble(head_html, body):
    return head_html + "\n" + HEADER + '<main id="main-content">\n' + body + "\n  </main>" + FOOTER


def form_html(L, prefix):
    """Proposal form. Field names and option values are the same in every language
    so /api/request-proposal and the success modal behave identically."""
    sizes = [("Under 20", L["s0"]), ("20–50", "20–50"), ("51–100", "51–100"), ("101–250", "101–250"),
             ("251–500", "251–500"), ("500+", "500+"), ("Not Confirmed Yet", L["s_nc"])]
    dests = [("Istanbul", "Istanbul"), ("Antalya", "Antalya"), ("Belek", "Belek"), ("Bodrum", "Bodrum"),
             ("Cappadocia", L["cappadocia"]), ("Multiple Destinations", L["multi"]), ("Not Decided Yet", L["nd"])]
    types = [("Meeting / Conference", L["t_conf"]), ("Incentive Travel", L["t_inc"]), ("Corporate Event", L["t_corp"]),
             ("Group Travel", L["t_grp"]), ("White-Label DMC Support", L["t_wl"]), ("Other", L["t_oth"])]
    opt = lambda pairs: "".join('<option value="%s">%s</option>' % (v, esc(t)) for v, t in pairs)
    return '''    <section class="page-section" id="anfrage">
      <h2>%(h2)s</h2>
      <p class="page-section__lede">%(lede)s</p>
      <form name="%(name)s" method="POST" action="/api/request-proposal" data-proposal-form>
        <p class="sr-only"><label>Company website <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
        <input type="hidden" name="source_page"><input type="hidden" name="landing_page"><input type="hidden" name="submission_page"><input type="hidden" name="timestamp">
        <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_content"><input type="hidden" name="utm_term">
        <input type="hidden" name="lead_source"><input type="hidden" name="campaign"><input type="hidden" name="service_interest"><input type="hidden" name="page_type">
        <div class="form-grid">
          <div class="form-field"><label for="%(p)s-name">%(name_l)s</label><input type="text" id="%(p)s-name" name="name" autocomplete="name" required></div>
          <div class="form-field"><label for="%(p)s-company">%(company_l)s</label><input type="text" id="%(p)s-company" name="company" autocomplete="organization" required></div>
          <div class="form-field"><label for="%(p)s-email">%(email_l)s</label><input type="email" id="%(p)s-email" name="email" autocomplete="email" inputmode="email" required></div>
          <div class="form-field"><label for="%(p)s-dest">%(dest_l)s</label>
            <select id="%(p)s-dest" name="destination" required><option value="">%(dest_ph)s</option>%(dests)s</select></div>
          <div class="form-field"><label for="%(p)s-group">%(group_l)s</label>
            <select id="%(p)s-group" name="group_size" required><option value="">%(group_ph)s</option>%(sizes)s</select></div>
          <div class="form-field"><label for="%(p)s-type">%(type_l)s</label>
            <select id="%(p)s-type" name="project_type"><option value="">%(type_ph)s</option>%(types)s</select></div>
          <fieldset class="form-field"><legend>%(dates_l)s</legend>
            <div class="date-range"><label for="%(p)s-ds" class="sr-only">%(start)s</label><input type="date" id="%(p)s-ds" name="date_start">
              <label for="%(p)s-de" class="sr-only">%(end)s</label><input type="date" id="%(p)s-de" name="date_end"></div>
            <label class="form-check"><input type="checkbox" name="dates_unconfirmed" value="Yes"> %(unconf)s</label></fieldset>
          <div class="form-field form-field--full"><label for="%(p)s-brief">%(brief_l)s <span class="field-optional">(%(optional)s)</span></label>
            <textarea id="%(p)s-brief" name="brief" placeholder="%(brief_ph)s"></textarea></div>
          <p class="form-note form-field--full">%(privacy)s</p>
          <p class="form-error" data-proposal-error role="alert" hidden></p>
          <div class="form-actions"><button type="submit" class="btn btn--primary">%(submit)s</button></div>
        </div>
      </form>
      <section class="proposal-success" data-proposal-success hidden aria-live="polite">
        <h2>%(ok_h)s</h2>
        <p>%(ok_p)s</p>
      </section>
      <ul class="cta-expect">%(expect)s</ul>
    </section>''' % dict(L, p=prefix, dests=opt(dests), sizes=opt(sizes), types=opt(types))


# --- UK page ---------------------------------------------------------------------

UK_FAQ = [
    ("What does a DMC in Turkey do for a UK agency?",
     "We run the local side of the programme so the agency does not have to manage each supplier directly: hotel and "
     "venue sourcing, airport transfers and ground transport, event production, staffing and on-site coordination in "
     "Istanbul, Antalya, Belek, Cappadocia and Bodrum."),
    ("Can you work white-label for our agency?",
     "Yes, where appropriate. The agency keeps the client relationship and we handle local execution, with "
     "communication kept agency-oriented."),
    ("How quickly will we get a proposal?",
     "We reply within 24 hours and send an itemised proposal within 3–5 business days. Once you confirm, a named "
     "coordinator is assigned."),
    ("How do UK groups get to Turkey?",
     "From London there are daily flights to Istanbul (about 3.5–4 hours) with Turkish Airlines, British Airways and "
     "easyJet. Direct flights to Antalya run seasonally, May to October, and Bodrum has scheduled routes from London "
     "(about 3.5 hours). Schedules change by season, so check carriers for your dates."),
]


def render_uk():
    title = "DMC Turkey for UK Agencies | Local MICE & Incentive Partner"
    description = ("Local DMC partner in Turkey for UK agencies and MICE planners: hotels, venues, transfers and "
                   "event production across five destinations. White-label available.")
    crumbs = [("Home", "/"), ("DMC Turkey", EN_PEER), ("UK Agencies", UK_PATH)]
    flights = table("Getting to Turkey from the UK", ["Destination", "Main airport", "From London", "Airport to hotels"], [
        ["Istanbul", "Istanbul Airport (IST); Sabiha Gökçen (SAW)", "Daily flights, about 3.5–4 hours (Turkish Airlines, British Airways, easyJet)", "IST: 40–60 minutes by road"],
        ["Antalya and Belek", "Antalya Airport (AYT)", "Direct flights, seasonal (May–October)", "Antalya city: 15–30 minutes; Belek: 30–45 minutes"],
        ["Bodrum", "Milas-Bodrum Airport (BJV)", "Scheduled routes, about 3.5 hours", "30–45 minutes"],
        ["Cappadocia", "Nevşehir Kapadokya (NAV); Kayseri (ASR)", "See the Cappadocia destination guide", "NAV: 45–60 minutes; ASR: 75–90 minutes"],
    ])
    L = dict(h2="Send Your Brief", lede="Tell us the destination, group size and dates. We reply within 24 hours.",
             name="uk-agency-brief", name_l="Your Name", company_l="Company", email_l="Work Email", dest_l="Destination",
             dest_ph="Select a destination", group_l="Approx. Group Size", group_ph="Select an approximate size",
             type_l="Project Type", type_ph="Select a project type", dates_l="Travel / Event Dates", start="Start date",
             end="End date", unconf="Dates Not Confirmed", brief_l="Tell us briefly about your project", optional="optional",
             brief_ph="3-night incentive programme for approximately 120 guests in Antalya...",
             privacy='We use your contact details to respond to this enquiry, as explained in our <a href="/privacy-policy/">Privacy Policy</a>. A proposal is not a booking. Please do not include passport, payment card or sensitive personal details.',
             submit="Send My Brief", ok_h="Thank you — we’ve received your brief.",
             ok_p="We will reply within 24 hours and send your itemised proposal within 3–5 business days.",
             s0="Under 20", s_nc="Not Confirmed Yet", cappadocia="Cappadocia", multi="Multiple Destinations", nd="Not Decided Yet",
             t_conf="Meeting / Conference", t_inc="Incentive Travel", t_corp="Corporate Event", t_grp="Group Travel",
             t_wl="White-Label DMC Support", t_oth="Other",
             expect="<li>Reply within 24 hours</li><li>Itemised proposal in 3–5 business days</li><li>Named coordinator once you confirm</li>")
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>DMC Turkey for UK Agencies &amp; MICE Planners</h1>",
        '      <p class="reviewed-note">Last updated: <time datetime="2026-10">October 2026</time></p>',
        '      <p class="page-section__lede">DMC Turkey Partner is the local execution partner in Turkey for UK agencies, '
        "incentive houses and corporate planners. We have operated in Turkey since 2006 and run programmes across "
        "Istanbul, Antalya, Belek, Cappadocia and Bodrum: hotels, venues, ground transport, event production and "
        "on-site coordination, with one local team behind your brief.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="#anfrage">Send Your Brief</a>'
        '<a class="btn btn--ghost" href="/event-cost-calculator/">Estimate Your Event Budget</a></div>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>What We Handle for UK Agencies</h2>",
        "      " + cards([
            ("Hotels &amp; venues", "Group accommodation, room blocks, meeting hotels, resorts, conference spaces and dinner venues."),
            ("Ground transport", "Airport transfers, private vehicles, coaches, group shuttles and VIP transfers where required."),
            ("Event production", "Audio, lighting, video, stage, rigging and technical coordination, plus staffing and interpreters."),
            ("On-site coordination", "Arrival and departure support, supplier coordination and a named coordinator once you confirm."),
        ]),
        '      <p class="section-more">Prefer to keep the client relationship with your agency? See '
        '<a href="/white-label-dmc-turkey/">white-label DMC support</a> or become an <a href="/agency-partners/">agency partner</a>.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Getting to Turkey from the UK</h2>",
        "      " + flights,
        '      <p class="price-note">Flight information is taken from our <a href="/why-turkey/">Why Turkey</a> and destination guides. Schedules change by season; check carriers for your dates.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Budget Reference</h2>",
        "      <p>Published per-person ranges, flights excluded, for the shoulder season (April–June, September–November):</p>",
        "      <ul><li>4-night incentive trip, 5-star all-inclusive resort in Antalya (50–150 guests): €500–750 — "
        '<a href="/event-costs/antalya/">Antalya event costs</a></li>'
        "<li>4-night corporate retreat, 5-star all-inclusive resort in Belek (50–150 guests): €500–750 — "
        '<a href="/event-costs/belek/">Belek event costs</a></li>'
        "<li>3-night conference, 5-star Bosphorus hotel in Istanbul (50–150 guests): €500–650 — "
        '<a href="/event-costs/istanbul/">Istanbul event costs</a></li></ul>',
        '      <p class="price-note">Indicative, non-binding planning ranges. Peak July–August carries a 15–25% premium. '
        'Use the <a href="/event-cost-calculator/">event budget calculator</a> to explore your own brief, or see '
        '<a href="/off-season-events-turkey/">off-season planning windows</a> if your dates are flexible.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>How a Project Runs</h2>",
        "      " + steps([
            ("Send Your Brief", "Destination, dates, group size and project type."),
            ("Reply Within 24 Hours", "We confirm what is possible and ask the right questions."),
            ("Itemised Proposal", "Within 3–5 business days."),
            ("Coordinator &amp; Delivery", "Once you confirm, a named coordinator runs the programme on the ground."),
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Who You Are Working With</h2>",
        "      <p>DMC Turkey Partner is operated by ANTALYA GOLF MCD TRAVEL (PMR TURİZM İNŞAAT TİCARET LİMİTED ŞİRKETİ), "
        "Güzeloba, 2268 Sok No:33, 07230 Muratpaşa, Antalya. TÜRSAB agency number 12434. See "
        '<a href="/selected-works/">selected works</a> and <a href="/about/">about us</a>.</p>',
        "    </section>",
        faq_html("Frequently Asked Questions", UK_FAQ),
        form_html(L, "uk"),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="/dmc-turkey/">DMC Turkey</a><a href="/mice-turkey/">MICE Turkey</a>'
        '<a href="/incentive-travel-turkey/">Incentive travel in Turkey</a>'
        '<a href="/corporate-events-turkey/">Corporate event management</a>'
        '<a href="/destinations/">Destinations</a></p></section>',
    ])
    return assemble(head("en", title, description, UK_PATH, "UK Agencies", "UK Agency Landing",
                         schema("en", "DMC Turkey for UK Agencies", UK_PATH, description, crumbs, UK_FAQ)), body)


# --- German page -----------------------------------------------------------------

DE_FAQ = [
    ("Was übernimmt eine DMC in der Türkei?",
     "Eine DMC organisiert den lokalen Teil eines Projekts: Hotel- und Venue-Beschaffung, Transfers und Bodentransport, "
     "Eventproduktion, Personal und die Betreuung vor Ort. Die Agentur oder das Unternehmen muss die einzelnen Lieferanten "
     "nicht selbst koordinieren."),
    ("In welchen Zielorten arbeiten Sie?",
     "In Istanbul, Antalya, Belek, Kappadokien und Bodrum. Wir sind seit 2006 in der Türkei tätig."),
    ("Wie schnell erhalten wir ein Angebot?",
     "Wir melden uns innerhalb von 24 Stunden und senden ein detailliertes Angebot innerhalb von 3–5 Werktagen. Nach "
     "Ihrer Bestätigung übernimmt eine feste Ansprechperson die Betreuung."),
    ("Können Sie als White-Label-Partner für unsere Agentur arbeiten?",
     "Ja, wo es passt. Die Agentur behält die Kundenbeziehung, wir übernehmen die lokale Umsetzung in der Türkei."),
]


def render_de():
    title = "DMC Türkei | Eventmanagement, Incentives & Firmenevents"
    description = ("DMC Türkei: Eventmanagement, Incentive-Reisen und Firmenevents in Istanbul, Antalya, Belek, "
                   "Kappadokien und Bodrum. Lokale Umsetzung seit 2006.")
    crumbs = [("Startseite", "/"), ("DMC Türkei", DE_PATH)]
    hreflang = "\n".join([
        '  <link rel="alternate" hreflang="de" href="%s%s">' % (SITE, DE_PATH),
        '  <link rel="alternate" hreflang="en" href="%s%s">' % (SITE, EN_PEER),
        '  <link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, EN_PEER),
    ])
    flights = table("Anreise aus dem deutschsprachigen Raum", ["Abflugort", "Istanbul", "Antalya", "Fluggesellschaften"], [
        ["Frankfurt", "Täglich, 3–4 Flüge, rund 3 Stunden", "Direktflüge, saisonal", "Turkish Airlines, Lufthansa, SunExpress"],
        ["Zürich", "Täglich", "Direktflüge, saisonal", "Turkish Airlines, SWISS"],
    ])
    L = dict(h2="Anfrage senden", lede="Nennen Sie uns Zielort, Gruppengröße und Reisedaten. Wir melden uns innerhalb von 24 Stunden.",
             name="de-landing-brief", name_l="Ihr Name", company_l="Unternehmen", email_l="Geschäftliche E-Mail", dest_l="Zielort",
             dest_ph="Zielort auswählen", group_l="Ungefähre Gruppengröße", group_ph="Größe auswählen",
             type_l="Projektart", type_ph="Projektart auswählen", dates_l="Reise- / Veranstaltungsdaten", start="Startdatum",
             end="Enddatum", unconf="Termine noch nicht bestätigt", brief_l="Kurze Projektbeschreibung", optional="optional",
             brief_ph="3-tägiges Incentive-Programm für rund 120 Gäste in Antalya ...",
             privacy='Wir verwenden Ihre Kontaktdaten, um Ihre Anfrage zu beantworten, wie in unserer <a href="/privacy-policy/">Datenschutzerklärung</a> (Englisch) beschrieben. Ein Angebot ist keine Buchung. Bitte senden Sie keine Pass-, Zahlungskarten- oder sensiblen personenbezogenen Daten.',
             submit="Anfrage senden", ok_h="Vielen Dank – wir haben Ihre Anfrage erhalten.",
             ok_p="Wir melden uns innerhalb von 24 Stunden und senden Ihr detailliertes Angebot innerhalb von 3–5 Werktagen.",
             s0="Unter 20", s_nc="Noch nicht bestätigt", cappadocia="Kappadokien", multi="Mehrere Zielorte", nd="Noch nicht entschieden",
             t_conf="Meeting / Konferenz", t_inc="Incentive-Reise", t_corp="Firmenevent", t_grp="Gruppenreise",
             t_wl="White-Label-DMC-Unterstützung", t_oth="Sonstiges",
             expect="<li>Antwort innerhalb von 24 Stunden</li><li>Detailliertes Angebot in 3–5 Werktagen</li><li>Feste Ansprechperson nach Bestätigung</li>")
    body = "\n".join([
        crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>DMC Türkei: Eventmanagement, Incentives und Firmenevents vor Ort</h1>",
        '      <p class="reviewed-note">Stand: <time datetime="2026-10">Oktober 2026</time></p>',
        '      <p class="page-section__lede">DMC Turkey Partner ist eine Destination-Management-Company mit Sitz in Antalya '
        "und seit 2006 in der Türkei tätig. Wir setzen MICE-Programme, Incentive-Reisen, Firmenevents und Gruppenreisen "
        "für internationale Agenturen, Incentive-Häuser und Unternehmen in Istanbul, Antalya, Belek, Kappadokien und "
        "Bodrum um: von der Hotel- und Venue-Beschaffung über Transfers und Eventproduktion bis zur Betreuung vor Ort.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="#anfrage">Anfrage senden</a></div>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Was eine DMC in der Türkei übernimmt</h2>",
        "      " + cards([
            ("Hotels", "Gruppenunterkünfte, Zimmerkontingente, Tagungshotels und Resorts."),
            ("Transfers und Bodentransport", "Flughafentransfers, Privatfahrzeuge, Busse, Gruppen-Shuttles und VIP-Transfers."),
            ("Veranstaltungsorte", "Tagungsorte, Eventlocations, Dinner-Venues und besondere Locations."),
            ("MICE und Events", "Meetings, Incentives, Konferenzen, Firmenevents und Galadinner."),
            ("Eventproduktion", "Ton, Licht, Video, Bühne, Traversen und technische Koordination."),
            ("Personal und Akkreditierung", "Hostessen, Registrierung und auf Wunsch Dolmetscher."),
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Unsere Zielorte</h2>",
        "      " + cards([
            ('<a href="/destinations/istanbul/">Istanbul</a>', "Meetings, Konferenzen, Firmenevents, Incentives und Premium-Gruppen."),
            ('<a href="/destinations/antalya/">Antalya</a>', "Große Gruppen, Konferenzen, Incentives, Resorts und Corporate Hospitality."),
            ('<a href="/destinations/belek/">Belek</a>', "Resort-Meetings, Konferenzen, Golf-Incentives und große Unterkunftsbedarfe."),
            ('<a href="/destinations/cappadocia/">Kappadokien</a>', "Incentives, Führungsgruppen und besondere Erlebnisprogramme."),
            ('<a href="/destinations/bodrum/">Bodrum</a>', "Premium-Incentives, Corporate Hospitality und private Gruppen."),
        ]),
        '      <p class="section-more">Die verlinkten Zielort-Seiten sind auf Englisch.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Anreise aus dem deutschsprachigen Raum</h2>",
        "      " + flights,
        '      <p class="price-note">Angaben aus unseren Zielort-Informationen (<a href="/why-turkey/">Why Turkey</a>, Englisch). Flugpläne ändern sich je nach Saison; bitte prüfen Sie die Verbindungen für Ihre Termine.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Orientierungswerte für das Budget</h2>",
        "      <p>Veröffentlichte Richtwerte pro Person, ohne Flüge, für die Zwischensaison (April–Juni, September–November):</p>",
        "      <ul><li>Incentive-Reise, 4 Nächte, 5-Sterne-All-inclusive-Resort in Antalya (50–150 Gäste): €500–750 — "
        '<a href="/event-costs/antalya/">Antalya (Englisch)</a></li>'
        "<li>Firmen-Retreat, 4 Nächte, 5-Sterne-All-inclusive-Resort in Belek (50–150 Gäste): €500–750 — "
        '<a href="/event-costs/belek/">Belek (Englisch)</a></li>'
        "<li>Konferenz, 3 Nächte, 4-Sterne-Stadthotel in Istanbul (50–150 Gäste): €350–500 — "
        '<a href="/event-costs/istanbul/">Istanbul (Englisch)</a></li></ul>',
        '      <p class="price-note">Unverbindliche Planungswerte. In der Hochsaison (Juli–August) gilt ein Aufschlag von 15–25 %. '
        'Eigene Szenarien können Sie mit dem <a href="/event-cost-calculator/">Budgetrechner</a> (Englisch) durchspielen.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>So läuft ein Projekt ab</h2>",
        "      " + steps([
            ("Anfrage", "Zielort, Termine, Gruppengröße und Projektart."),
            ("Antwort in 24 Stunden", "Wir klären, was möglich ist, und stellen die richtigen Fragen."),
            ("Detailliertes Angebot", "Innerhalb von 3–5 Werktagen."),
            ("Ansprechperson und Umsetzung", "Nach Ihrer Bestätigung betreut eine feste Ansprechperson das Programm vor Ort."),
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Ihr Partner vor Ort</h2>",
        "      <p>DMC Turkey Partner wird betrieben von ANTALYA GOLF MCD TRAVEL (PMR TURİZM İNŞAAT TİCARET LİMİTED ŞİRKETİ), "
        "Güzeloba, 2268 Sok No:33, 07230 Muratpaşa, Antalya. TÜRSAB-Agenturnummer 12434. Referenzen finden Sie unter "
        '<a href="/selected-works/">Selected Works</a> (Englisch).</p>',
        "    </section>",
        faq_html("Häufige Fragen", DE_FAQ),
        form_html(L, "de"),
        '    <section class="page-section"><h2>Mehr auf Englisch</h2><p class="cluster-links">'
        '<a href="/dmc-turkey/">DMC Turkey (English)</a><a href="/mice-turkey/">MICE Turkey</a>'
        '<a href="/incentive-travel-turkey/">Incentive travel</a>'
        '<a href="/corporate-events-turkey/">Corporate events</a></p></section>',
    ])
    return assemble(head("de", title, description, DE_PATH, "DE Landing", "DMC Tuerkei",
                         schema("de", "DMC Türkei", DE_PATH, description, crumbs, DE_FAQ), hreflang), body)


def write_page(rel, html):
    path = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html + "\n")
    site_seo.patch(path, site_seo.identity_block())
    print("wrote /%s" % os.path.dirname(rel))


def main():
    write_page("dmc-turkey-uk-agencies/index.html", render_uk())
    write_page("de/dmc-tuerkei/index.html", render_de())


if __name__ == "__main__":
    main()
