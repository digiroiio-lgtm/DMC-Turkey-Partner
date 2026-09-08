#!/usr/bin/env python3
"""Give every page one connected structured-data graph.

Before this, 137 pages carried a site-level Organization + WebSite graph and
then a scatter of unlinked blobs: 135 BreadcrumbLists and 50 FAQPages that
referenced nothing, only 10 page-level WebPage nodes, and — the inversion that
mattered commercially — Service markup on 20 COP31 campaign pages while the 9
real /services/ pages had none, 27 case studies with nothing but a breadcrumb,
and cost pages publishing budget ranges with no price markup at all.

Everything here is derived from the page's own rendered markup. See
tools/page_model.py for why that beats a URL-keyed registry: content is edited
directly in the .html files, so a registry would go stale and start asserting
things the page does not say, which is the exact condition Google treats as
spam. Derived schema agrees with the visible page by construction, and that
agreement is what makes FAQ and breadcrumb markup eligible in the first place.

What it emits, per page:

    every page      WebPage, plus BreadcrumbList and FAQPage regenerated from
                    the visible DOM (verified byte-for-byte equivalent to the
                    hand-written ones on all 185 pages that had them)
    /services/*     Service, provider -> #organization, hasOfferCatalog
    /selected-works CreativeWork — not Event; these are completed private
                    programmes nobody can attend, and Event would court an
                    event rich result for something with no tickets
    hubs            CollectionPage + ItemList from the listing cards
    /destinations/* WebPage about a Place
    /event-costs/*  Service, and a PriceSpecification only behind a config
                    flag, because the pages state the range is non-binding

Left alone deliberately: the COP31 cluster, whose generator already emits
WebPage/Service/FAQPage with @id links, and the Event / Article / NewsArticle
nodes on /events/ and the editorial pages. This patcher is additive there.

Usage: python3 tools/page_schema.py [--dry-run]
"""

import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import page_model as pm  # noqa: E402
import site_config as cfg  # noqa: E402
from answer_data import ANSWERS  # noqa: E402
from site_seo import area_served  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = "page-schema"

ORG = {"@id": cfg.SITE + "/#organization"}
SITE_NODE = {"@id": cfg.SITE + "/#website"}

# The generator owns these; it already emits linked WebPage/Service/FAQPage.
SKIP_FAMILIES = {"cop31", "cop31_news", "cop31_news_hub"}

# Types this patcher regenerates from the DOM and therefore supersedes.
SUPERSEDED = {"BreadcrumbList", "FAQPage"}

_lastmod_cache = {}


def lastmod(rel):
    if rel not in _lastmod_cache:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=ROOT,
            capture_output=True,
            text=True,
        ).stdout.strip()
        _lastmod_cache[rel] = out or None
    return _lastmod_cache[rel]


def breadcrumb_node(page):
    if len(page["breadcrumbs"]) < 2:
        return None
    items = []
    for position, (name, href) in enumerate(page["breadcrumbs"], start=1):
        item = {"@type": "ListItem", "position": position, "name": name}
        if href:
            item["item"] = cfg.SITE + href if href.startswith("/") else href
        else:
            item["item"] = page["absolute"]
        items.append(item)
    return {
        "@type": "BreadcrumbList",
        "@id": page["absolute"] + "#breadcrumb",
        "itemListElement": items,
    }


def faq_node(page):
    if not page["faqs"]:
        return None
    return {
        "@type": "FAQPage",
        "@id": page["absolute"] + "#faq",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in page["faqs"]
        ],
    }


def item_list(page):
    if not page["cards"]:
        return None
    return {
        "@type": "ItemList",
        "@id": page["absolute"] + "#list",
        "numberOfItems": len(page["cards"]),
        "itemListOrder": "https://schema.org/ItemListOrderAscending",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "name": label, "url": url}
            for i, (url, label) in enumerate(page["cards"], start=1)
        ],
    }


def service_node(page, service_type=None):
    node = {
        "@type": "Service",
        "@id": page["absolute"] + "#service",
        "name": page["h1"] or page["title"],
        "url": page["absolute"],
        "provider": ORG,
        "areaServed": area_served(),
    }
    if page["lede"]:
        node["description"] = page["lede"]
    if service_type:
        node["serviceType"] = service_type
    offerings = [label for _, label in page["cards"]]
    if offerings:
        node["hasOfferCatalog"] = {
            "@type": "OfferCatalog",
            "name": (page["h1"] or page["title"]) + " scope",
            "itemListElement": [
                {"@type": "Offer", "itemOffered": {"@type": "Service", "name": label}}
                for label in offerings
            ],
        }
    return node


def case_study_node(page):
    facts = page["definitions"]
    node = {
        "@type": "CreativeWork",
        "@id": page["absolute"] + "#work",
        "name": page["h1"],
        "url": page["absolute"],
        "creator": ORG,
        "isPartOf": {"@id": cfg.SITE + "/selected-works/#list"},
        "mainEntityOfPage": {"@id": page["absolute"] + "#webpage"},
    }
    if page["lede"]:
        node["description"] = page["lede"]
    if facts.get("Event Type"):
        node["about"] = {"@type": "Thing", "name": facts["Event Type"]}
        node["genre"] = facts["Event Type"]
    if facts.get("Services"):
        node["keywords"] = [s.strip() for s in re.split(r"[,·]", facts["Services"]) if s.strip()]
    venue, destination = facts.get("Venue"), facts.get("Destination")
    if venue or destination:
        place = {"@type": "Place", "name": venue or destination}
        if destination:
            place["address"] = {
                "@type": "PostalAddress",
                "addressLocality": destination.split(",")[0].strip(),
                "addressCountry": "TR",
            }
        node["locationCreated"] = place
    if facts.get("Year", "").strip().isdigit():
        node["dateCreated"] = facts["Year"].strip()
    return node
    # Note: no "client"/"sponsor". The brands are already named in the visible
    # copy, but promoting them into machine-readable triples materially widens
    # reuse — AI answers would begin asserting the client list as fact — and
    # that needs the contracts checked first.


def place_node(page):
    city = page["breadcrumbs"][-1][0] if page["breadcrumbs"] else page["h1"]
    return {
        "@type": "Place",
        "@id": page["absolute"] + "#place",
        "name": city,
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city,
            "addressCountry": "TR",
        },
    }


def price_specification(page):
    """Only when the owner has opted in. See site_config.EMIT_COST_PRICE_SPEC."""
    parsed = pm.budget_range(page)
    if not parsed:
        return None
    low, high, currency = parsed
    spec = {
        "@type": "PriceSpecification",
        "minPrice": low,
        "maxPrice": high,
        "priceCurrency": currency,
        "valueAddedTaxIncluded": False,
        "description": (
            "Indicative planning range for the programme described on this page. "
            "It is not a quotation and is not binding."
        ),
    }
    group = page["main_attrs"].get("data-group-size")
    if group and group.isdigit():
        spec["eligibleQuantity"] = {
            "@type": "QuantitativeValue",
            "value": int(group),
            "unitText": "guests",
        }
    return spec


def build_graph(page):
    nodes = []

    web_page = {
        "@type": "WebPage",
        "@id": page["absolute"] + "#webpage",
        "url": page["absolute"],
        "name": page["h1"] or page["title"],
        "inLanguage": "en",
        "isPartOf": SITE_NODE,
        "publisher": ORG,
    }
    if page["description"]:
        web_page["description"] = page["description"]
    stamp = lastmod(page["rel"])
    if stamp:
        web_page["dateModified"] = stamp

    crumbs = breadcrumb_node(page)
    if crumbs:
        web_page["breadcrumb"] = {"@id": crumbs["@id"]}

    # Where the page carries an answer capsule, that paragraph and the heading
    # above it are the part worth reading aloud. See tools/answer_capsule.py.
    if page["url"] in ANSWERS:
        web_page["speakable"] = {
            "@type": "SpeakableSpecification",
            "cssSelector": [".answer-capsule", "h1"],
        }

    family = page["family"]
    primary = None

    if family == "service":
        leaf = page["breadcrumbs"][-1][0] if page["breadcrumbs"] else None
        primary = service_node(page, service_type=leaf)
    elif family == "case_study":
        primary = case_study_node(page)
    elif family == "destination":
        primary = place_node(page)
        web_page["about"] = {"@id": primary["@id"]}
    elif family == "cost_scenario":
        primary = service_node(page, service_type="Event programme budgeting")
        if cfg.EMIT_COST_PRICE_SPEC:
            spec = price_specification(page)
            if spec:
                primary["offers"] = {
                    "@type": "Offer",
                    "priceSpecification": spec,
                    "availability": "https://schema.org/LimitedAvailability",
                    "seller": ORG,
                }
    elif family in ("solution", "cost_hub"):
        primary = service_node(page)

    listing = item_list(page) if family.endswith("_hub") or family == "event_taxonomy" else None
    if listing:
        web_page["@type"] = ["WebPage", "CollectionPage"]
        web_page["mainEntity"] = {"@id": listing["@id"]}
    elif primary:
        web_page["mainEntity"] = {"@id": primary["@id"]}

    nodes.append(web_page)
    for node in (crumbs, faq_node(page), primary, listing):
        if node:
            nodes.append(node)
    return nodes


def drop_superseded(html):
    """Remove the standalone Breadcrumb/FAQ blocks this patcher regenerates.

    Restricted to the unmanaged spans, so it can never reach inside another
    patcher's fence — the failure mode site_seo.drop_legacy_entity_nodes()
    avoids only by accident today.
    """
    out, cursor = [], 0
    for start, stop in mb.outside_fences(html):
        out.append(html[cursor:start])

        def replace(match):
            try:
                data = json.loads(match.group(1))
            except ValueError:
                return match.group(0)
            if isinstance(data, dict) and data.get("@type") in SUPERSEDED:
                return ""
            return match.group(0)

        out.append(
            re.sub(
                r'[ \t]*<script type="application/ld\+json">\s*(.*?)\s*</script>\n?',
                replace,
                html[start:stop],
                flags=re.S,
            )
        )
        cursor = stop
    out.append(html[cursor:])
    return "".join(out)


def render(nodes):
    graph = {"@context": "https://schema.org", "@graph": nodes}
    return "\n".join(
        [
            mb.begin(FENCE),
            '  <script type="application/ld+json">',
            "  " + json.dumps(graph, ensure_ascii=False, separators=(",", ":")),
            "  </script>",
            "  " + mb.end(FENCE),
        ]
    ) + "\n"


def main():
    dry_run = "--dry-run" in sys.argv
    changed = total = skipped = 0

    for path in mb.iter_pages(ROOT):
        page = pm.read(path, ROOT)
        if page["family"] in SKIP_FAMILIES or page["noindex"]:
            # Skipping means this patcher owns no block here, so any block it
            # left behind on an earlier run has to go. Otherwise a page that
            # becomes noindex keeps asserting a stale graph forever — which is
            # how 404.html ended up claiming the homepage's @id.
            original = page["html"]
            if not dry_run:
                mb.write_if_changed(path, original, mb.strip(original, FENCE))
            skipped += 1
            continue
        total += 1

        original = page["html"]
        html = drop_superseded(mb.strip(original, FENCE))
        html = mb.insert(html, FENCE, render(build_graph(page)), path)

        if dry_run:
            if html != original:
                changed += 1
                print("would change %s" % page["rel"])
            continue
        if mb.write_if_changed(path, original, html):
            changed += 1

    print(
        "page schema: %d of %d pages changed (%d COP31 pages left to their generator)"
        % (changed, total, skipped)
    )


if __name__ == "__main__":
    main()
