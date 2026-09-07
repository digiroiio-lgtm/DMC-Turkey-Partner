#!/usr/bin/env python3
"""Apply site-wide identity, measurement and crawl settings to every page.

Three jobs, all idempotent:

1. Entity consolidation. The site previously carried three different
   Organization names across a handful of pages and none at all on the rest.
   Google and AI answer engines resolve entities by a stable @id plus
   consistent naming, so this replaces every top-level Organization/WebSite
   node with one canonical @graph emitted on all pages.
2. Measurement. Emits the GA4 (or GTM) snippet when an ID is configured.
3. Verification. Emits Search Console / Bing verification tags when set.

Usage: python3 tools/site_seo.py
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import site_config as cfg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BEGIN = "<!-- site-identity:begin -->"
END = "<!-- site-identity:end -->"
HEAD_CLOSE = "</head>"
LD_BLOCK = re.compile(
    r'[ \t]*<script type="application/ld\+json">\s*(.*?)\s*</script>\n?', re.S
)


def area_served():
    """Service area as a country with the cities placed inside it.

    A flat list of six names leaves an engine to guess that "Belek" is in
    Türkiye and not in one of the other places with that name. containedInPlace
    states it.
    """
    country, *cities = cfg.ORG_AREA_SERVED
    turkiye = {"@type": "Country", "@id": cfg.SITE + "/#turkiye", "name": country}
    return [turkiye] + [
        {"@type": "City", "name": name, "containedInPlace": {"@id": turkiye["@id"]}}
        for name in cities
    ]


def organization():
    # Stays Organization until a real postal address exists. LocalBusiness and
    # its TravelAgency subtype both need an address to earn a local result;
    # emitting an addressless one just puts a weak duplicate entity into
    # competition with this node.
    types = "Organization"
    if cfg.ORG_ADDRESS:
        types = ["Organization", "TravelAgency"]

    node = {
        "@type": types,
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
        "description": cfg.ORG_DESCRIPTION,
        "areaServed": area_served(),
        "knowsAbout": cfg.ORG_KNOWS_ABOUT,
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "customer service",
                "email": cfg.ORG_EMAIL,
                "availableLanguage": ["en", "tr"],
            }
        ],
    }

    if cfg.ORG_TELEPHONE:
        node["telephone"] = cfg.ORG_TELEPHONE
        node["contactPoint"].append(
            {
                "@type": "ContactPoint",
                "contactType": "sales",
                "telephone": cfg.ORG_TELEPHONE,
                "email": cfg.ORG_EMAIL,
                "availableLanguage": ["en", "tr"],
                "areaServed": "TR",
            }
        )
    if cfg.ORG_FOUNDING_YEAR:
        node["foundingDate"] = cfg.ORG_FOUNDING_YEAR
    if cfg.ORG_ADDRESS:
        node["address"] = dict({"@type": "PostalAddress"}, **cfg.ORG_ADDRESS)
    if cfg.ORG_GEO:
        node["geo"] = dict({"@type": "GeoCoordinates"}, **cfg.ORG_GEO)
    if cfg.ORG_OPENING_HOURS:
        node["openingHours"] = cfg.ORG_OPENING_HOURS
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

    if cfg.GTM_CONTAINER_ID:
        parts.append(
            "  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':"
            "new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],"
            "j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src="
            "'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);"
            "})(window,document,'script','dataLayer','%s');</script>" % cfg.GTM_CONTAINER_ID
        )
    elif cfg.GA4_MEASUREMENT_ID:
        # gtag.js loads async so it never blocks render. Page views are sent
        # automatically; custom events reach GA4 through trackEvent in main.js.
        parts.append(
            '  <script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
            % cfg.GA4_MEASUREMENT_ID
        )
        parts.append(
            "  <script>window.dataLayer=window.dataLayer||[];"
            "function gtag(){dataLayer.push(arguments);}gtag('js',new Date());"
            "gtag('config','%s');</script>" % cfg.GA4_MEASUREMENT_ID
        )

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

    Restricted to the unmanaged spans of the document. This used to sweep the
    whole file and spared tools/page_schema.py's block only because that block
    is a @graph with no top-level @type — luck rather than design. Scanning
    outside the fences makes it structurally unable to delete another
    patcher's output.
    """

    def replace(match):
        try:
            data = json.loads(match.group(1))
        except ValueError:
            return match.group(0)
        if isinstance(data, dict) and data.get("@type") in ("Organization", "WebSite"):
            return ""
        return match.group(0)

    out, cursor = [], 0
    for start, stop in mb.outside_fences(html):
        out.append(html[cursor:start])
        out.append(LD_BLOCK.sub(replace, html[start:stop]))
        cursor = stop
    out.append(html[cursor:])
    return "".join(out)


def patch(path, block):
    with open(path, encoding="utf-8") as handle:
        original = handle.read()
    html = drop_legacy_entity_nodes(strip_managed(original))
    if HEAD_CLOSE not in html:
        raise SystemExit("No </head> in %s" % path)
    html = html.replace(HEAD_CLOSE, block + HEAD_CLOSE, 1)
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
