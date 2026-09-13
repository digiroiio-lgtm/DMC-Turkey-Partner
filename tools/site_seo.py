#!/usr/bin/env python3
"""Apply site-wide identity, measurement and crawl settings to every page.

Four jobs, all idempotent:

1. Entity consolidation. The site previously carried three different
   Organization names across a handful of pages and none at all on the rest.
   Google and AI answer engines resolve entities by a stable @id plus
   consistent naming, so this replaces every top-level Organization/WebSite
   node with one canonical @graph emitted on all pages.
2. Measurement. Emits the GA4 (or GTM) snippet when an ID is configured,
   preceded by a Consent Mode v2 default that denies storage until the
   visitor accepts. The GTM <noscript> fallback goes into <body>.
3. Verification. Emits Search Console / Bing verification tags when set.
4. Page typing. Stamps data-page-type / data-page-slug on <body> so main.js
   can report a content-type view event for each section of the site.

Usage: python3 tools/site_seo.py
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import site_config as cfg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BEGIN = "<!-- site-identity:begin -->"
END = "<!-- site-identity:end -->"
BODY_BEGIN = "<!-- site-body:begin -->"
BODY_END = "<!-- site-body:end -->"
HEAD_CLOSE = "</head>"
LD_BLOCK = re.compile(
    r'[ \t]*<script type="application/ld\+json">\s*(.*?)\s*</script>\n?', re.S
)
BODY_OPEN = re.compile(r"<body\b([^>]*)>")
PAGE_ATTR = re.compile(r'\s+data-page-(?:type|slug)="[^"]*"')

# Sections whose pages get a content-type view event. The value is the
# data-page-type stamped on <body>; the directory name under it becomes the
# slug, and the section's own index page is typed "<type>_index".
#
# event-costs is deliberately absent: those pages already report
# event_cost_page_view from their own data-event-cost-page attributes
# (main.js), and a second view event per page would double-count the section.
PAGE_SECTIONS = {
    "selected-works": "selected_work",
    "services": "service",
    "destinations": "destination",
}

# Single pages that are funnel landmarks rather than one of a repeating set.
PAGE_SINGLES = {
    "index.html": ("home", "home"),
    os.path.join("request-proposal", "index.html"): ("proposal_form", "request-proposal"),
    os.path.join("contact", "index.html"): ("contact", "contact"),
}


def page_identity(rel_path):
    """Map a repo-relative HTML path to (data-page-type, data-page-slug).

    Returns None for pages outside the typed sections, which are then left
    without the attributes and report only GA4's automatic page_view.
    """
    if rel_path in PAGE_SINGLES:
        return PAGE_SINGLES[rel_path]
    parts = rel_path.split(os.sep)
    section = PAGE_SECTIONS.get(parts[0])
    if not section:
        return None
    if len(parts) == 2:  # <section>/index.html
        return (section + "_index", parts[0])
    if len(parts) == 3:  # <section>/<slug>/index.html
        return (section, parts[1])
    return None


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
        "description": cfg.ORG_DESCRIPTION,
        "areaServed": [{"@type": "Place", "name": name} for name in cfg.ORG_AREA_SERVED],
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

    if cfg.GTM_CONTAINER_ID or cfg.GA4_MEASUREMENT_ID:
        # Consent Mode v2 defaults. This must run before the tag itself, so
        # that nothing is written to storage until the visitor accepts in the
        # banner (main.js then issues the matching consent update). Without
        # it the tag would set cookies on first paint. wait_for_update gives
        # the banner's stored decision time to replay on a repeat visit.
        parts.append(
            "  <script>window.dataLayer=window.dataLayer||[];"
            "function gtag(){dataLayer.push(arguments);}"
            "gtag('consent','default',{"
            "'ad_storage':'denied','ad_user_data':'denied',"
            "'ad_personalization':'denied','analytics_storage':'denied',"
            "'functionality_storage':'granted','security_storage':'granted',"
            "'wait_for_update':500});</script>"
        )

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
            "gtag('config','%s');window.dmcGtagOnly=true;</script>"
            % cfg.GA4_MEASUREMENT_ID
        )

    parts.append("  " + END)
    return "\n".join(parts) + "\n"


def body_block():
    """The GTM <noscript> fallback, or an empty string when GTM is not set.

    gtag.js has no noscript equivalent, so this is GTM-only.
    """
    if not cfg.GTM_CONTAINER_ID:
        return ""
    return (
        "\n"
        + BODY_BEGIN
        + '\n<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=%s"'
        ' height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>\n'
        % cfg.GTM_CONTAINER_ID
        + BODY_END
    )


def strip_managed(html):
    """Remove previously injected blocks so the script can be re-run."""
    html = re.sub(
        re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", html, flags=re.S
    )
    return re.sub(
        r"\n?" + re.escape(BODY_BEGIN) + r".*?" + re.escape(BODY_END), "", html, flags=re.S
    )


def stamp_body(html, identity, block):
    """Rewrite the <body> tag with its page-type attributes and noscript.

    Existing attributes on the tag are preserved; only a previous stamp from
    this script is replaced, which is what keeps re-runs idempotent.
    """

    def replace(match):
        attrs = PAGE_ATTR.sub("", match.group(1))
        if identity:
            attrs += ' data-page-type="%s" data-page-slug="%s"' % identity
        return "<body%s>%s" % (attrs, block)

    return BODY_OPEN.sub(replace, html, count=1)


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


def patch(path, block, body):
    with open(path, encoding="utf-8") as handle:
        original = handle.read()
    html = drop_legacy_entity_nodes(strip_managed(original))
    if HEAD_CLOSE not in html:
        raise SystemExit("No </head> in %s" % path)
    if not BODY_OPEN.search(html):
        raise SystemExit("No <body> in %s" % path)
    html = html.replace(HEAD_CLOSE, block + HEAD_CLOSE, 1)
    html = stamp_body(html, page_identity(os.path.relpath(path, ROOT)), body)
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
    body = body_block()
    changed = 0
    total = 0
    typed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        if os.sep + ".git" + os.sep in path:
            continue
        total += 1
        if page_identity(os.path.relpath(path, ROOT)):
            typed += 1
        if patch(path, block, body):
            changed += 1
    print("identity/measurement applied: %d of %d pages changed" % (changed, total))
    print("  page-type stamped: %d of %d pages" % (typed, total))
    print("  GA4:  %s" % (cfg.GA4_MEASUREMENT_ID or "not configured (no script emitted)"))
    print("  GTM:  %s" % (cfg.GTM_CONTAINER_ID or "not configured"))
    print("  GSC:  %s" % (cfg.GOOGLE_SITE_VERIFICATION or "not configured"))
    key = write_indexnow_key()
    print("  IndexNow key file: %s" % (key or "not configured"))


if __name__ == "__main__":
    main()
