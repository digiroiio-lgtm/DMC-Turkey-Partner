#!/usr/bin/env python3
"""Synchronize the shared five-column footer without regenerating page content.

Usage: python3 tools/site_footer.py [--check]
"""

import argparse
from html import escape
from pathlib import Path
import re

import site_config as cfg

ROOT = Path(__file__).resolve().parent.parent
FOOTER = re.compile(r'<footer class="site-footer">.*?</footer>', re.S)

COLUMNS = (
    ("Solutions & Services", (
        ("/dmc-turkey/", "DMC Turkey"),
        ("/white-label-dmc-turkey/", "White-Label DMC"),
        ("/mice-turkey/", "MICE Turkey"),
        ("/services/event-production/", "Event Production"),
        ("/services/transportation-logistics/", "Transportation & Logistics"),
        ("/services/", "All Services"),
    )),
    ("Destinations", (
        ("/destinations/istanbul/", "Istanbul"),
        ("/destinations/antalya/", "Antalya"),
        ("/destinations/belek/", "Belek"),
        ("/destinations/cappadocia/", "Cappadocia"),
        ("/destinations/bodrum/", "Bodrum"),
        ("/destinations/", "All Destinations"),
    )),
    ("Company", (
        ("/about/", "About"),
        ("/selected-works/", "Selected Works"),
        ("/agency-partners/", "Agency Partners"),
        ("/event-costs/", "Event Costs"),
        ("/insights/", "Guides & Insights"),
        ("/contact/", "Contact"),
    )),
    ("COP31 Antalya", (
        ("/cop31-antalya/", "COP31 Overview"),
        ("/cop31-antalya-participant-guide/", "Participant Guide"),
        ("/cop31-antalya-venue/", "Venue & Dates"),
        ("/cop31-event-services/", "Event Services"),
        ("/cop31-exhibition-services/", "Exhibition & Pavilion Services"),
        ("/cop31-last-minute-services/", "Last-Minute Support"),
    )),
)


def render():
    columns = []
    for title, links in COLUMNS:
        items = "\n".join(
            f'            <li><a href="{escape(href)}">{escape(label)}</a></li>'
            for href, label in links
        )
        columns.append(
            '        <div class="site-footer__col">\n'
            f'          <h2 class="site-footer__heading">{escape(title)}</h2>\n'
            f'          <ul>\n{items}\n          </ul>\n'
            '        </div>'
        )
    address = cfg.ORG_ADDRESS
    location = f'{address["postalCode"]} {address["addressLocality"]}/{address["addressRegion"]}, Türkiye'
    return '''<footer class="site-footer">
    <div class="container">
      <div class="site-footer__grid">
        <div class="site-footer__col site-footer__col--brand">
          <a class="site-logo site-logo--footer" href="/" aria-label="DmcTurkeyPartner.com home">Dmc<span>Turkey</span>Partner</a>
          <p>Local DMC, MICE and white-label event execution across Turkey.</p>
          <a class="btn btn--primary" href="/request-proposal/">Request a Proposal</a>
        </div>
''' + "\n".join(columns) + f'''
      </div>
      <section class="site-footer__company" aria-label="Registered agency and contact details">
        <!-- agency-footer:begin -->
        <div class="agency-details">
          <div class="agency-details__identity">
            <p>DMC Turkey Partner is operated by <strong>{escape(cfg.ORG_AGENCY_NAME)}</strong>.</p>
            <p>{escape(cfg.ORG_COMPANY_NAME)}</p>
            <p>TÜRSAB Agency No: <strong>{escape(cfg.ORG_TURSAB_NUMBER)}</strong> · <a href="{escape(cfg.ORG_AGENCY_RECORD_URL)}" target="_blank" rel="noopener">Published TÜRSAB record</a></p>
          </div>
          <div class="agency-details__contact">
            <p>{escape(address["streetAddress"])}<br>{escape(location)}</p>
            <p><a href="tel:{escape(cfg.ORG_PHONE)}">{escape(cfg.ORG_PHONE_DISPLAY)}</a></p>
          </div>
        </div>
        <!-- agency-footer:end -->
      </section>
      <div class="site-footer__bottom">
        <p>&copy; <span id="year">2026</span> DmcTurkeyPartner.com. All rights reserved.</p>
        <ul class="site-footer__legal">
          <li><a href="/privacy-policy/">Privacy</a></li>
          <li><a href="/cookie-policy/">Cookies</a></li>
          <li class="cookie-settings-item"><button type="button" data-cookie-settings>Cookie Settings</button></li>
          <li><a href="/terms/">Terms</a></li>
        </ul>
      </div>
    </div>
  </footer>'''


def replace_footer(html):
    return FOOTER.sub(lambda _: render(), html, count=1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Report stale footers without writing files")
    args = parser.parse_args()
    changed = []
    total = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        original = path.read_text(encoding="utf-8")
        if not FOOTER.search(original):
            continue
        total += 1
        updated = replace_footer(original)
        if updated != original:
            changed.append(path.relative_to(ROOT))
            if not args.check:
                path.write_text(updated, encoding="utf-8")
    print(f'{len(changed)} stale footers out of {total}' if args.check else f'Updated {len(changed)} of {total} footers')
    if args.check and changed:
        for path in changed:
            print(path)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
