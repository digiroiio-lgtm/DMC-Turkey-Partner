#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the group hotel offers cluster.

Usage: python3 tools/hotel_offers_build.py [--today YYYY-MM-DD]

Writes:
  group-hotel-offers-turkey/index.html               (hub)
  group-hotel-offers-turkey/lara/index.html          (area)
  group-hotel-offers-turkey/belek/index.html         (area)
  group-hotel-offers-turkey/<hotel-slug>/index.html  (9 hotel pages)

Source of truth: tools/hotel_offers_data.py. Idempotent for a given --today.
No prices, discounts or percentages are published; rates are on request.
Window status (open / upcoming / closed) is computed from --today, so rebuild
regularly (closed windows drop out of the Offer schema).
"""

import datetime as dt
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import SITE, esc, whatsapp_url  # noqa: E402
from cop31_render import ROOT, table  # noqa: E402
import hotel_offers_data as data  # noqa: E402
import off_season_build as osb  # noqa: E402

HUB_URL = SITE + data.HUB
EXPECT = osb.EXPECT
DISCLAIMER = ("Windows are limited and availability and rate validity are confirmed per request. Hotel names are "
              "trademarks of their owners and are used only to identify the property. We are an independent DMC.")


# --- helpers -------------------------------------------------------------------

def hotel_path(h):
    return data.HUB + h["slug"] + "/"


def area_path(key):
    return data.HUB + data.AREAS[key]["slug"] + "/"


def hname(h):
    return esc(h["name"])


def link(h):
    return '<a href="%s">%s</a>' % (hotel_path(h), hname(h))


def badge(w):
    if w["status"] == "closed":
        return '<span class="offer-badge offer-badge--closed">Closed</span>'
    if w["status"] == "open":
        return '<span class="offer-badge offer-badge--open">Open now</span>'
    d = w["days_until"]
    return '<span class="offer-badge">Starts in %d day%s</span>' % (d, "" if d == 1 else "s")


def cop_note(w):
    return (' <span class="offer-badge offer-badge--note">Overlaps COP31 dates</span>' if w["cop31"] else "")


def live(ws):
    return [w for w in ws if w["status"] != "closed"]


def window_rows(ws, with_hotel=True, with_area=True):
    rows = []
    for w in ws:
        row = [esc(w["label"])]
        if with_hotel:
            row.append(link(w["hotel"]))
        if with_area:
            row.append(data.AREAS[w["hotel"]["area"]]["name"])
        row += ["%d" % w["nights"], badge(w) + cop_note(w)]
        rows.append(row)
    return rows


def faq_html(items):
    return osb.faq_html(items)


def wa_link(message, label="Ask on WhatsApp"):
    return ('<a class="btn btn--ghost" href="%s" target="_blank" rel="noopener" '
            'data-track="hotel_offer_whatsapp_click">%s</a>' % (whatsapp_url(message), label))


def head(title, description, url, service_interest, schema_blocks):
    html = osb.head_html(title, description, url, "Hotel Offers", service_interest, schema_blocks)
    return html.replace('content="off-season"', 'content="hotel-offer"')


def schema(name, url, desc, crumbs, faqs, kind="WebPage", extra=None):
    web = {"@context": "https://schema.org", "@type": kind, "name": name, "url": url, "description": desc,
           "inLanguage": "en", "dateModified": data.UPDATED_ISO,
           "isPartOf": {"@id": SITE + "/#website"}, "publisher": {"@id": SITE + "/#organization"}}
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                              for i, (n, p) in enumerate(crumbs)]}
    fq = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                         for q, a in faqs]}
    blocks = [web, bc, fq] + ([extra] if extra else [])
    return "\n".join('  <script type="application/ld+json">\n  %s\n  </script>'
                     % json.dumps(d, ensure_ascii=False, separators=(",", ":")) for d in blocks)


def item_list(entries):
    return {"@context": "https://schema.org", "@type": "ItemList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + p}
                                for i, (n, p) in enumerate(entries)]}


def offer_service(h, ws, url):
    """Service > OfferCatalog > Offer, the site's existing pattern. No price, no rating."""
    hotel_node = {"@type": "Hotel", "@id": url + "#hotel", "name": h["name"],
                  "address": {"@type": "PostalAddress", "addressRegion": "Antalya", "addressCountry": "TR"}}
    offers = [{"@type": "Offer", "name": "%s group offer window, %s" % (h["name"], w["label"]),
               "itemOffered": {"@id": url + "#hotel"}, "seller": {"@id": SITE + "/#organization"},
               "availabilityStarts": w["start"].isoformat(), "availabilityEnds": w["end"].isoformat(),
               "url": url}
              for w in live(ws)]
    service = {"@type": "Service", "@id": url + "#service", "name": "Group hotel rates at %s" % h["name"],
               "serviceType": "Group hotel accommodation sourcing",
               "provider": {"@id": SITE + "/#organization"}, "areaServed": {"@type": "Country", "name": "Turkey"},
               "hasOfferCatalog": {"@type": "OfferCatalog", "name": "%s offer windows" % h["name"],
                                   "itemListElement": offers}}
    return {"@context": "https://schema.org", "@graph": [hotel_node, service]}


# --- request form ----------------------------------------------------------------

def form_html(destination, brief="", date_start="", date_end="", note_hotel=None):
    if destination:
        dest = '<input type="hidden" name="destination" value="%s">' % destination
    else:
        dest = ('<div class="form-field"><label for="ho-destination">Destination</label>'
                '<select id="ho-destination" name="destination" required><option value="">Select a destination</option>'
                "<option>Antalya</option><option>Belek</option><option>Multiple Destinations</option></select></div>")
    what = esc(note_hotel) if note_hotel else "an offer window"
    return '''    <section class="page-section offseason-compare" id="request">
      <h2>Request Group Rates for %s</h2>
      <p class="page-section__lede">Tell us the group size and dates. We confirm availability and rate validity for the window and reply with an itemised proposal. Rates are not published.</p>
      <form name="hotel-offer-request" method="POST" action="/api/request-proposal" data-proposal-form>
        <p class="sr-only"><label>Company website <input name="company-website" tabindex="-1" autocomplete="off"></label></p>
        <input type="hidden" name="source_page"><input type="hidden" name="landing_page"><input type="hidden" name="submission_page"><input type="hidden" name="timestamp">
        <input type="hidden" name="utm_source"><input type="hidden" name="utm_medium"><input type="hidden" name="utm_campaign"><input type="hidden" name="utm_content"><input type="hidden" name="utm_term">
        <input type="hidden" name="lead_source"><input type="hidden" name="campaign"><input type="hidden" name="service_interest"><input type="hidden" name="page_type">
        %s
        <div class="form-grid">
          <div class="form-field"><label for="ho-name">Your Name</label><input type="text" id="ho-name" name="name" autocomplete="name" required></div>
          <div class="form-field"><label for="ho-company">Company</label><input type="text" id="ho-company" name="company" autocomplete="organization" required></div>
          <div class="form-field"><label for="ho-email">Work Email</label><input type="email" id="ho-email" name="email" autocomplete="email" inputmode="email" required></div>
          <div class="form-field"><label for="ho-group">Approx. Group Size</label>
            <select id="ho-group" name="group_size" required><option value="">Select an approximate size</option>
              <option>Under 20</option><option>20–50</option><option>51–100</option><option>101–250</option><option>251–500</option><option>500+</option><option>Not Confirmed Yet</option></select></div>
          <div class="form-field"><label for="ho-type">Event Type</label>
            <select id="ho-type" name="project_type"><option value="">Select an event type</option>
              <option>Meeting / Conference</option><option>Incentive Travel</option><option>Corporate Event</option><option>Group Travel</option><option>Other</option></select></div>
          <fieldset class="form-field"><legend>Preferred Dates</legend>
            <div class="date-range"><label for="ho-date-start" class="sr-only">Start date</label><input type="date" id="ho-date-start" name="date_start" value="%s">
              <label for="ho-date-end" class="sr-only">End date</label><input type="date" id="ho-date-end" name="date_end" value="%s"></div>
            <label class="form-check"><input type="checkbox" id="ho-dates-unconfirmed" name="dates_unconfirmed" value="Yes"> Dates Not Confirmed</label></fieldset>
          <div class="form-field form-field--full"><label for="ho-flex">How flexible are your dates?</label>
            <select id="ho-flex" name="date_flexibility" required>
              <option selected>These offer dates only</option>
              <option>Flexible by a few days</option>
              <option>Open to other offer windows</option></select></div>
          <div class="form-field form-field--full"><label for="ho-brief">Anything else we should know? <span class="field-optional">(optional)</span></label>
            <textarea id="ho-brief" name="brief" placeholder="Programme type, room count, meeting space needs...">%s</textarea></div>
          <p class="form-note form-field--full">We use your contact details to respond to this enquiry, as explained in our <a href="/privacy-policy/">Privacy Policy</a>. A proposal is not a booking. Please do not include passport, payment card or sensitive personal details.</p>
          <p class="form-error" data-proposal-error role="alert" hidden></p>
          <div class="form-actions"><button type="submit" class="btn btn--primary">Request Group Rates</button></div>
        </div>
      </form>
      <section class="proposal-success" data-proposal-success hidden aria-live="polite">
        <h2>Thank you — we’ve received your request.</h2>
        <p>We will reply within 24 hours and send your itemised proposal within 3–5 business days.</p>
      </section>
      %s
    </section>''' % (what, dest, date_start, date_end, esc(brief), EXPECT)


# --- FAQs (plain text, identical in schema and page) -------------------------------

def faq_hub(ws):
    n = len(ws)
    return [
        ("What are the group hotel offer windows in Turkey for %s?" % data.SEASON_LABEL,
         "We have %d limited accommodation windows at 9 hotels in Lara and Belek, Antalya, between %s and %s. "
         "Each window is a set of stay dates for which we are requesting advantageous group rates." %
         (n, data.date_range(ws[0]["start"], ws[0]["start"], year=False),
          data.date_range(ws[-1]["end"], ws[-1]["end"]))),
        ("Are the rates published?",
         "No. We do not publish rates. Send your group size and dates and we confirm availability and rate validity "
         "for the window, then reply with an itemised proposal."),
        ("Are the offer windows guaranteed?",
         "No. Windows are limited and availability changes. We confirm each window per request before you commit, "
         "and a proposal is not a booking."),
        ("Can we use dates outside an offer window?",
         "Yes, other dates can be quoted, but the offer basis may not apply. We tell you which dates sit inside a "
         "window and which do not."),
        ("Which groups are these offers for?",
         "Agencies, corporate planners and incentive organisers booking meetings, incentive trips and group stays "
         "in Antalya. Send the group size and event type and we recommend the best-fitting window."),
    ]


def faq_area(key, ws):
    a = data.AREAS[key]
    return [
        ("Which %s hotels have group offer windows in %s?" % (a["name"], data.SEASON_LABEL),
         "%s. Each hotel has its own stay dates." % ", ".join(sorted({w["hotel"]["name"] for w in ws}))),
        ("Are %s offer rates published?" % a["name"],
         "No. Rates are confirmed per request, with availability and rate validity, in an itemised proposal."),
        ("How do I choose between the %s windows?" % a["name"],
         "Send your dates, group size and event type. We compare the windows that fit and flag any that overlap "
         "other events in Antalya."),
    ]


def faq_hotel(h, ws):
    dates = "; ".join(w["label"] for w in ws)
    return [
        ("When are the group offer windows at %s?" % h["name"], "%s: %s." % (h["name"], dates)),
        ("Are %s rates published?" % h["name"],
         "No. We confirm availability and rate validity per request and reply with an itemised proposal."),
        ("Can we stay at %s outside these dates?" % h["name"],
         "Other dates can be requested, but the offer basis may not apply. We confirm what applies to your dates."),
        ("What should I send to request a quote?",
         "Group size, preferred dates, event type and whether you need meeting space. We reply within 24 hours."),
    ]


# --- page assembly -------------------------------------------------------------------

def page(head_html, body):
    return osb.assemble(head_html, body)


def hero(h1, lede, extra_btns="", sub=""):
    return "\n".join([
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>%s</h1>" % h1,
        '      <p class="reviewed-note">Offer windows: %s · Last updated: <time datetime="%s">%s</time></p>'
        % (data.SEASON_LABEL, data.UPDATED_ISO, data.UPDATED_LABEL),
        '      <p class="page-section__lede">%s</p>' % lede,
        '      <div class="hero-actions"><a class="btn btn--primary" href="#request">Request Group Rates</a>%s</div>' % extra_btns,
        "      " + EXPECT, sub, "    </section>"])


def cards(items):
    return '      <div class="card-grid">' + "".join(
        '<article class="card"><h3>%s</h3><p>%s</p></article>' % i for i in items) + "</div>"


def hotel_cards(ws_all, hotels):
    out = []
    for h in hotels:
        hws = [w for w in ws_all if w["hotel"] is h]
        dates = " · ".join(esc(data.short_range(w["start"], w["end"])) for w in hws)
        out.append(('<article class="card"><h3>%s</h3><p>%s · %s</p><p>%s</p></article>')
                   % (link(h), data.AREAS[h["area"]]["name"], dates, " ".join(badge(w) for w in hws[:1])))
    return '      <div class="card-grid">' + "".join(out) + "</div>"


def next_window(ws):
    nxt = live(ws)
    return nxt[0] if nxt else None


def render_hub(ws, today):
    title = "Group Hotel Offers Turkey 2026 | Limited Antalya Windows for MICE"
    desc = ("%d limited group hotel offer windows in Lara and Belek, Antalya, October to December 2026. "
            "Compare dates by hotel and request group rates for meetings and incentives." % len(ws))
    crumbs = [("Home", "/"), ("Group Hotel Offers", data.HUB)]
    faqs = faq_hub(ws)
    nxt = next_window(ws)
    if nxt:
        when = "open now" if nxt["status"] == "open" else "opens in %d day%s" % (nxt["days_until"], "" if nxt["days_until"] == 1 else "s")
        callout = ('<div class="offseason-callout"><h3>Next window</h3><p><strong>%s</strong>, %s (%s): %s. '
                   '<a href="#request">Request group rates</a> before it closes.</p></div>'
                   % (link(nxt["hotel"]), esc(nxt["label"]), data.AREAS[nxt["hotel"]["area"]]["name"], when))
    else:
        callout = ('<div class="offseason-callout"><h3>2026 windows have closed</h3><p>New offer windows are '
                   'announced here. <a href="#request">Ask us about upcoming dates</a>.</p></div>')
    months = []
    for m in sorted({w["start"].month for w in ws}):
        mws = [w for w in ws if w["start"].month == m]
        months.append('    <section class="page-section" id="%s">\n      <h3>%s %d</h3>\n      %s\n    </section>' % (
            data.MONTHS[m].lower(), data.MONTHS[m], 2026,
            table("%s 2026 offer windows" % data.MONTHS[m], ["Stay dates", "Hotel", "Area", "Nights", "Status"], window_rows(mws))))
    body = "\n".join([
        osb.crumbs_html(crumbs),
        hero("Group Hotel Offers in Antalya, Lara &amp; Belek: %d Limited Windows, Oct–Dec 2026" % len(ws),
             "We have secured %d limited stay windows at 9 hotels in Lara and Belek for agencies and corporate planners "
             "with flexible dates. Pick a hotel and window, tell us your group size, and we confirm availability and "
             "rate validity in an itemised proposal. Rates are on request." % len(ws),
             wa_link("Hi, I would like group rates for the Antalya hotel offer windows.")),
        '    <section class="page-section">\n      <h2>Next Window Opening</h2>\n      ' + callout + "\n    </section>",
        '    <section class="page-section">\n      <h2>Offer Calendar by Month</h2>\n'
        '      <p class="page-section__lede">All windows in date order. Stay dates are check-in to check-out.</p>\n    </section>',
        "\n".join(months),
        '    <section class="page-section">\n      <h2>Hotels with Offer Windows</h2>\n' + hotel_cards(ws, data.HOTELS) + "\n    </section>",
        '    <section class="page-section">\n      <h2>Lara or Belek for Your Group</h2>\n' + cards([
            ('<a href="%s">Lara</a>' % area_path("lara"), "City-side resort coast close to Antalya Airport: Trendy, Adalya Elit, Titanic Deluxe, Ducale, Voyage and Mardan Palace."),
            ('<a href="%s">Belek</a>' % area_path("belek"), "Resort-based meetings district, 30–45 minutes from the airport: Adam &amp; Eve, Titanic Deluxe and Voyage."),
        ]) + "\n    </section>",
        '    <section class="page-section">\n      <h2>How to Secure a Window</h2>\n'
        '      <ol class="steps-list"><li><h3>Choose a Window</h3><p>Pick the hotel and stay dates that fit your group.</p></li>'
        "<li><h3>Send Your Brief</h3><p>Group size, event type and meeting-space needs.</p></li>"
        "<li><h3>Confirmation Within 24 Hours</h3><p>We confirm availability and rate validity for the window.</p></li>"
        "<li><h3>Itemised Proposal</h3><p>Within 3–5 business days, with a named coordinator once you confirm.</p></li></ol>\n    </section>",
        '    <section class="page-section">\n      <h2>Why These Dates Matter for Groups</h2>\n'
        "      <p>Limited windows are the dates when a hotel is prepared to offer more favourable group terms. They close when "
        "the room block is committed, so planners who want to compare early should ask now. Pair a window with "
        'our <a href="/services/hotel-sourcing/">hotel sourcing</a>, <a href="/mice-turkey/">MICE</a> and '
        '<a href="/incentive-travel-turkey/">incentive travel</a> services, or compare off-peak planning in our '
        '<a href="/off-season-events-turkey/">off-season guide</a>.</p>\n'
        '      <p class="price-note">%s</p>\n    </section>' % DISCLAIMER,
        faq_html(faqs),
        form_html(None, brief="Interested in the group hotel offer windows. Hotel / window: "),
    ])
    extra = item_list([(h["name"], hotel_path(h)) for h in data.HOTELS])
    return page(head(title, desc, HUB_URL, "Hotel Offers Hub",
                     schema("Group Hotel Offers in Turkey", HUB_URL, desc, crumbs, faqs, "CollectionPage", extra)), body)


def render_area(key, ws, today):
    a = data.AREAS[key]
    aws = [w for w in ws if w["hotel"]["area"] == key]
    hotels = [h for h in data.HOTELS if h["area"] == key]
    url = SITE + area_path(key)
    title = "%s Group Hotel Offers 2026 | Limited Windows for MICE" % a["name"]
    desc = ("%d limited group hotel offer windows in %s, Antalya, Oct to Dec 2026: compare hotels and dates "
            "and request group rates for meetings and incentives." % (len(aws), a["name"]))
    crumbs = [("Home", "/"), ("Group Hotel Offers", data.HUB), (a["name"], area_path(key))]
    faqs = faq_area(key, aws)
    dest = "Belek" if key == "belek" else "Antalya"
    first = live(aws)[:1]
    body = "\n".join([
        osb.crumbs_html(crumbs),
        hero("%s Group Hotel Offers: %d Limited Windows, Oct–Dec 2026" % (a["name"], len(aws)),
             "%s %d limited stay windows across %d hotels for groups with flexible dates. Choose a hotel and window and "
             "we confirm availability and rate validity. Rates are on request." % (esc(a["blurb"]), len(aws), len(hotels)),
             wa_link("Hi, I would like group rates for the %s hotel offer windows." % a["name"])),
        '    <section class="page-section">\n      <h2>%s Offer Windows by Date</h2>\n      %s\n    </section>' % (
            a["name"], table("%s offer windows" % a["name"], ["Stay dates", "Hotel", "Nights", "Status"],
                             [[r[0], r[1], r[3], r[4]] for r in window_rows(aws)])),
        '    <section class="page-section">\n      <h2>%s Hotels with Offer Windows</h2>\n%s\n    </section>' % (a["name"], hotel_cards(ws, hotels)),
        '    <section class="page-section">\n      <h2>Planning a %s Group Stay</h2>\n' % a["name"]
        + "      <p>Send your group size, dates and event type and we recommend the best-fitting window, confirm "
          "availability, and add transfers, meeting space and programme. See also the "
          '<a href="/destinations/%s/">%s destination guide</a> and the <a href="%s">overview of all %d windows</a>.</p>\n'
          '      <p class="price-note">%s</p>\n    </section>'
          % ("belek" if key == "belek" else "antalya", "Belek" if key == "belek" else "Antalya", data.HUB, len(ws), DISCLAIMER),
        faq_html(faqs),
        form_html(dest, brief="Interested in %s group hotel offer windows. Hotel / window: " % a["name"],
                  date_start=first[0]["start"].isoformat() if first else "", date_end=first[0]["end"].isoformat() if first else ""),
    ])
    extra = item_list([(h["name"], hotel_path(h)) for h in hotels])
    return page(head(title, desc, url, "%s Hotel Offers" % a["name"],
                     schema("%s Group Hotel Offers" % a["name"], url, desc, crumbs, faqs, "CollectionPage", extra)), body)


def render_hotel(h, ws, today):
    hws = [w for w in ws if w["hotel"] is h]
    a = data.AREAS[h["area"]]
    url = SITE + hotel_path(h)
    nm = h["name"]
    lbls = " &amp; ".join(esc(data.short_range(w["start"], w["end"])) for w in live(hws)) or "2026 windows closed"
    title = "%s Group Rates 2026 | %s Hotel Offer Windows" % (esc(nm), a["name"])
    desc = ("%s group offer windows in %s, Antalya: %s 2026. Request group rates for meetings and incentives."
            % (nm, a["name"], "; ".join(w["label"] for w in live(hws)) or "dates on request"))
    crumbs = [("Home", "/"), ("Group Hotel Offers", data.HUB), (nm, hotel_path(h))]
    faqs = faq_hotel(h, hws)
    first = live(hws)[:1]
    others = [w for w in live(ws) if w["hotel"] is not h and any(
        w["start"] <= x["end"] and w["end"] >= x["start"] for x in live(hws))]
    alt = h.get("alt")
    lede = ("%s%s offers %d limited group stay window%s in %s. Send your group size and we confirm availability and "
            "rate validity for the dates. Rates are on request." %
            (esc(nm), " (%s)" % esc(alt) if alt else "", len(hws), "" if len(hws) == 1 else "s", a["name"]))
    body = "\n".join([
        osb.crumbs_html(crumbs),
        hero("%s Group Offer: %s 2026" % (hname(h), lbls), lede,
             wa_link("Hi, I would like group rates for %s." % nm)),
        '    <section class="page-section">\n      <h2>%s Offer Windows</h2>\n      %s\n    </section>' % (
            hname(h), table("%s offer windows" % esc(nm), ["Stay dates", "Nights", "Status"],
                            [[esc(w["label"]), "%d" % w["nights"], badge(w) + cop_note(w)] for w in hws])),
        '    <section class="page-section">\n      <h2>What Your Request Includes</h2>\n' + cards([
            ("Availability check", "We confirm the room block for your dates before you commit."),
            ("Rate validity", "Rates are confirmed per request and are not published."),
            ("Itemised proposal", "Accommodation, meeting space, transfers and programme, line by line."),
        ]) + "\n    </section>",
        '    <section class="page-section">\n      <h2>Compare Other Windows</h2>\n      '
        + ("<p>Other hotels with windows on the same dates:</p>\n      " + table(
            "Windows on overlapping dates", ["Stay dates", "Hotel", "Area", "Nights", "Status"], window_rows(others))
           if others else "<p>See all windows in the <a href=\"%s\">%d-window calendar</a> or the <a href=\"%s\">%s overview</a>.</p>" % (data.HUB, len(ws), area_path(h["area"]), a["name"]))
        + '\n      <p class="price-note">%s</p>\n    </section>' % DISCLAIMER,
        faq_html(faqs),
        form_html("Belek" if h["area"] == "belek" else "Antalya",
                  brief="Interested in %s. Window: %s. Group size and programme: " % (nm, "; ".join(w["label"] for w in live(hws))),
                  date_start=first[0]["start"].isoformat() if first else "",
                  date_end=first[0]["end"].isoformat() if first else "", note_hotel=nm),
        '    <section class="page-section"><h2>Related</h2><p class="cluster-links">'
        '<a href="%s">All group hotel offers</a><a href="%s">%s offers</a><a href="/services/hotel-sourcing/">Hotel sourcing</a>'
        '<a href="/destinations/%s/">%s destination guide</a></p></section>'
        % (data.HUB, area_path(h["area"]), a["name"], "belek" if h["area"] == "belek" else "antalya", "Belek" if h["area"] == "belek" else "Antalya"),
    ])
    extra = offer_service(h, hws, url)
    return page(head(title, desc, url, "Hotel Offer: %s" % nm,
                     schema("%s Group Offer Windows" % nm, url, desc, crumbs, faqs, extra=extra)), body)


# --- managed link blocks on existing pages --------------------------------------------

BEGIN, END = "<!-- hotel-offers:begin -->", "<!-- hotel-offers:end -->"


def strip_block(html):
    return re.sub(r"[ \t]*" + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S)


def link_blocks(ws):
    n = len(live(ws)) or len(ws)
    strip = lambda inner: ("    %s\n    <section class=\"page-section\" aria-label=\"Limited group hotel offers\">\n      %s\n    </section>\n    %s\n"
                           % (BEGIN, inner, END))
    home = strip('<h2>Limited Group Hotel Offers in Antalya</h2>\n      <p class="page-section__lede">%d limited stay windows at 9 hotels in Lara and Belek, %s. '
                 'Compare hotels and dates, then request group rates.</p>\n      <div class="hero-actions"><a class="btn btn--primary" href="%s">View Hotel Offers</a>'
                 '<a class="btn btn--ghost" href="%s">Lara</a><a class="btn btn--ghost" href="%s">Belek</a></div>'
                 % (n, data.SEASON_LABEL, data.HUB, area_path("lara"), area_path("belek")))

    def line(text):
        return strip('<p class="section-more">%s</p>' % text)

    generic = line('<strong>Limited group hotel offers, %s:</strong> %d stay windows at 9 hotels in Lara and Belek. '
                   '<a href="%s">Compare dates and request group rates</a>.' % (data.SEASON_LABEL, n, data.HUB))
    targets = {
        "index.html": (home, "<!-- production-showcase:end -->\n"),
        "services/hotel-sourcing/index.html": (generic, None),
        "mice-turkey/index.html": (generic, None),
        "incentive-travel-turkey/index.html": (generic, None),
        "off-season-events-turkey/index.html": (generic, None),
        "destinations/antalya/index.html": (line('<strong>Limited group hotel offers, %s:</strong> see the <a href="%s">Lara offer windows</a> or <a href="%s">all %d windows</a>.' % (data.SEASON_LABEL, area_path("lara"), data.HUB, n)), None),
        "destinations/belek/index.html": (line('<strong>Limited group hotel offers, %s:</strong> see the <a href="%s">Belek offer windows</a> or <a href="%s">all %d windows</a>.' % (data.SEASON_LABEL, area_path("belek"), data.HUB, n)), None),
    }
    for rel, (block, after) in targets.items():
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as handle:
            html = strip_block(handle.read())
        if after:
            if after not in html:
                raise SystemExit("anchor missing in %s" % rel)
            html = html.replace(after, after + block, 1)
        else:
            if "  </main>" not in html:
                raise SystemExit("no </main> in %s" % rel)
            html = html.replace("  </main>", block + "  </main>", 1)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(html)
        print("linked /%s" % rel)


def write_page(rel, html):
    osb.write_page(rel, html)


def main():
    today = dt.date.today()
    if "--today" in sys.argv:
        today = dt.date.fromisoformat(sys.argv[sys.argv.index("--today") + 1])
    ws = data.windows(today)
    write_page("group-hotel-offers-turkey/index.html", render_hub(ws, today))
    for key in data.AREAS:
        write_page("group-hotel-offers-turkey/%s/index.html" % data.AREAS[key]["slug"], render_area(key, ws, today))
    for h in data.HOTELS:
        write_page("group-hotel-offers-turkey/%s/index.html" % h["slug"], render_hotel(h, ws, today))
    link_blocks(ws)
    print("today=%s open/upcoming=%d closed=%d" % (today, len(live(ws)), len(ws) - len(live(ws))))


if __name__ == "__main__":
    main()
