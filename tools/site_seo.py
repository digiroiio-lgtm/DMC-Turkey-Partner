#!/usr/bin/env python3
"""Apply site-wide identity, measurement and crawl settings to every page.

Three jobs, all idempotent:

1. Entity consolidation. The site previously carried three different
   Organization names across a handful of pages and none at all on the rest.
   Google and AI answer engines resolve entities by a stable @id plus
   consistent naming, so this replaces every top-level Organization/WebSite
   node with one canonical @graph emitted on all pages.
2. Measurement. Emits a first-party consent loader; Google tags wait for permission.
3. Verification. Emits Search Console / Bing verification tags when set.

Usage: python3 tools/site_seo.py
"""

import html as html_lib
import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import site_config as cfg  # noqa: E402
from site_footer import replace_footer  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BEGIN = "<!-- site-identity:begin -->"
END = "<!-- site-identity:end -->"
HEAD_CLOSE = "</head>"
LD_BLOCK = re.compile(
    r'[ \t]*<script type="application/ld\+json">\s*(.*?)\s*</script>\n?', re.S
)


def organization():
    node = {
        "@type": "Organization",
        "@id": cfg.SITE + "/#organization",
        "name": cfg.ORG_NAME,
        "alternateName": cfg.ORG_ALTERNATE_NAMES,
        "url": cfg.SITE + "/",
        "logo": {
            "@type": "ImageObject",
            "@id": cfg.SITE + "/#logo",
            "url": cfg.SITE + "/assets/img/dmcturkeypartner-logo.svg",
            "contentUrl": cfg.SITE + "/assets/img/dmcturkeypartner-logo.svg",
        },
        "image": {"@id": cfg.SITE + "/#logo"},
        "email": cfg.ORG_EMAIL,
        "telephone": cfg.ORG_PHONE,
        "address": cfg.ORG_ADDRESS,
        "parentOrganization": {"@type": "TravelAgency", "@id": cfg.SITE + "/#travel-agency", "name": cfg.ORG_AGENCY_NAME, "legalName": cfg.ORG_COMPANY_NAME, "telephone": cfg.ORG_PHONE, "address": cfg.ORG_ADDRESS, "identifier": {"@type": "PropertyValue", "propertyID": "TÜRSAB agency registration number", "value": cfg.ORG_TURSAB_NUMBER}},
        "description": cfg.ORG_DESCRIPTION,
        "areaServed": [{"@type": "Place", "name": name} for name in cfg.ORG_AREA_SERVED],
        "knowsAbout": cfg.ORG_KNOWS_ABOUT,
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "telephone": cfg.ORG_PHONE,
                "email": cfg.ORG_EMAIL,
                "availableLanguage": ["en", "tr"],
            }
        ],
    }
    if cfg.ORG_SAME_AS:
        node["sameAs"] = cfg.ORG_SAME_AS
    return node


def website():
    return {
        "@type": "WebSite",
        "@id": cfg.SITE + "/#website",
        "url": cfg.SITE + "/",
        "name": cfg.ORG_NAME,
        "alternateName": cfg.ORG_ALTERNATE_NAMES,
        "description": cfg.ORG_DESCRIPTION,
        "inLanguage": "en",
        "publisher": {"@id": cfg.SITE + "/#organization"},
    }


def identity_block():
    graph = {"@context": "https://schema.org", "@graph": [organization(), website()]}
    parts = [BEGIN]

    if cfg.GOOGLE_SITE_VERIFICATION:
        parts.append(
            '  <meta name="google-site-verification" content="%s">'
            % cfg.GOOGLE_SITE_VERIFICATION
        )
    if cfg.BING_SITE_VERIFICATION:
        parts.append('  <meta name="msvalidate.01" content="%s">' % cfg.BING_SITE_VERIFICATION)

    parts.append('  <script type="application/ld+json">')
    parts.append("  " + json.dumps(graph, ensure_ascii=False, separators=(",", ":")))
    parts.append("  </script>")

    # No Google tag is requested before optional analytics consent.
    parts.append('<script src="/assets/js/privacy.js" defer data-ga4="%s" data-gtm="%s"></script>' % (cfg.GA4_MEASUREMENT_ID, cfg.GTM_CONTAINER_ID))

    parts.append("  " + END)
    return "\n".join(parts) + "\n"


def strip_managed(html):
    """Remove a previously injected block so the script can be re-run."""
    return re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S
    )


def drop_legacy_entity_nodes(html):
    """Drop hand-written Organization/WebSite JSON-LD superseded by the graph.

    Leaves BreadcrumbList, FAQPage, WebPage, Service and everything else alone.
    """

    def replace(match):
        try:
            data = json.loads(match.group(1))
        except ValueError:
            return match.group(0)
        if isinstance(data, dict) and data.get("@type") in ("Organization", "WebSite"):
            return ""
        return match.group(0)

    return LD_BLOCK.sub(replace, html)


def agency_details():
    name = html_lib.escape(cfg.ORG_AGENCY_NAME)
    address = cfg.ORG_ADDRESS
    street = html_lib.escape(address["streetAddress"])
    location = html_lib.escape(address["postalCode"] + " " + address["addressLocality"] + "/" + address["addressRegion"])
    details = (
        f'<p>DMC Turkey Partner is operated by <strong>{name}</strong>.</p>\n'
        f'          <p>{html_lib.escape(cfg.ORG_COMPANY_NAME)}</p>\n'
        f'          <p>TÜRSAB Agency No: <strong>{cfg.ORG_TURSAB_NUMBER}</strong> · <a href="{cfg.ORG_AGENCY_RECORD_URL}" target="_blank" rel="noopener">Published TÜRSAB record</a></p>\n'
        f'          <p>{street}<br>{location}, Türkiye</p>\n'
        f'          <p><a href="tel:{cfg.ORG_PHONE}">{cfg.ORG_PHONE_DISPLAY}</a></p>'
    )
    return ('<!-- agency-section:begin -->\n    <section class="page-section"><div class="container">'
            '<h2>Registered Travel Agency &amp; Contact Details</h2>' + details +
            '</div></section>\n    <!-- agency-section:end -->\n')


def patch_agency_details(html, path):
    html = re.sub(r'<button type="button" class="cookie-settings-inline" data-cookie-settings>Cookie Settings</button>\n[ \t]*', "", html)
    for kind in ("footer", "section"):
        html = re.sub(r"[ \t]*<!-- agency-" + kind + r":begin -->.*?<!-- agency-" + kind + r":end -->\n?", "", html, flags=re.S)
    # The shared footer owns the agency band and Cookie Settings control.
    html = replace_footer(html)
    relative = os.path.relpath(path, ROOT).replace(os.sep, "/")
    if relative in ("about/index.html", "contact/index.html"):
        html = html.replace("  </main>", "    " + agency_details() + "  </main>", 1)
    return html


def patch(path, block):
    with open(path, encoding="utf-8") as handle:
        original = handle.read()
    html = drop_legacy_entity_nodes(strip_managed(original))
    if HEAD_CLOSE not in html:
        raise SystemExit("No </head> in %s" % path)
    html = html.replace(HEAD_CLOSE, block + HEAD_CLOSE, 1)
    html = patch_agency_details(html, path)
    if html == original:
        return False
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html)
    return True


def write_indexnow_key():
    if not cfg.INDEXNOW_KEY:
        return None
    path = os.path.join(ROOT, cfg.INDEXNOW_KEY + ".txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(cfg.INDEXNOW_KEY + "\n")
    return os.path.basename(path)


def main():
    block = identity_block()
    changed = 0
    total = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        if os.sep + ".git" + os.sep in path:
            continue
        total += 1
        if patch(path, block):
            changed += 1
    print("identity/measurement applied: %d of %d pages changed" % (changed, total))
    print("  GA4:  %s" % (cfg.GA4_MEASUREMENT_ID or "not configured (no script emitted)"))
    print("  GTM:  %s" % (cfg.GTM_CONTAINER_ID or "not configured"))
    print("  GSC:  %s" % (cfg.GOOGLE_SITE_VERIFICATION or "not configured"))
    key = write_indexnow_key()
    print("  IndexNow key file: %s" % (key or "not configured"))


if __name__ == "__main__":
    main()
