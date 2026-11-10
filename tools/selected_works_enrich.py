#!/usr/bin/env python3
"""Answer-ready blocks for the Selected Works project pages.

The internal SEO/GEO/AEO audit (Nov 2026) scored the 28 project pages ~59/100:
150–210 words, no FAQ, no date, 1–2 internal links in. This adds three blocks
to each page, built only from facts the page already publishes (its project
table, narrative and photo descriptions):

  * an FAQ (where, for whom, what was delivered, what was built on site) with
    matching FAQPage JSON-LD;
  * "Services on This Project", linking each delivered service to the page
    that describes it;
  * "Related Projects": three other projects of the same type.

Marker-delimited and idempotent; re-running refreshes the blocks.

Usage: python3 tools/selected_works_enrich.py
"""

import glob
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"
TODAY = ("2026-11-10", "10 November 2026")
BEGIN, END = "<!-- work-enrich:begin -->", "<!-- work-enrich:end -->"
LD_BEGIN, LD_END = "<!-- work-faq-schema:begin -->", "<!-- work-faq-schema:end -->"
ANCHOR = '<section class="page-section">\n      <div class="cta-banner">'

SERVICE_PAGES = {
    "Event Production": "/services/event-production/",
    "Technical Production": "/services/event-production/",
    "Stage Production": "/services/event-production/",
    "Transportation & Logistics": "/services/transportation-logistics/",
    "Ground Handling": "/services/ground-handling/",
    "Venue Styling": "/production-showcase/",
    "Décor & Branding": "/production-showcase/",
    "Hotel Sourcing": "/services/hotel-sourcing/",
    "Venue Sourcing": "/services/venue-sourcing/",
    "Meetings & Conferences": "/services/meetings-conferences/",
    "Incentive Programs": "/services/incentive-programs/",
}


def plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def facts(text):
    table = re.search(r"<h2>What We Delivered</h2>(.*?)</table>", text, re.S).group(1)
    rows = {plain(k): plain(v) for k, v in re.findall(r"<tr><td><strong>(.*?)</strong></td><td>(.*?)</td></tr>", table, re.S)}
    narrative = {h: plain(p) for h, p in re.findall(r"<h2>(Overview|Scope|Execution)</h2>\s*<p>(.*?)</p>", text, re.S)}
    name = plain(re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S).group(1))
    photos = [html.unescape(a) for a in re.findall(r'<img[^>]*class="[^"]*"[^>]*alt="([^"]+)"|<figure class="work-photo"><img[^>]*alt="([^"]+)"', text) for a in a if a]
    photos = list(dict.fromkeys(p for p in photos if p != "DMC Turkey Partner"))
    return dict(name=name, rows=rows, narrative=narrative, photos=photos)


def sentence(text):
    return re.split(r"(?<=[.!?])\s", text.strip())[0]


def faqs_for(f):
    r, n, name = f["rows"], f["narrative"], f["name"].split(" — ")[0]
    out = []
    dest = r.get("Destination", "").replace("Turkey, Turkey", "Türkiye")
    if r.get("Venue") and dest:
        out.append(("Where was %s held?" % name, "At %s, %s." % (r["Venue"], dest)))
    elif dest:
        out.append(("Where did %s take place?" % name, "In %s." % dest))
    if r.get("Year / Date"):
        out.append(("When did %s take place?" % name, "In %s." % r["Year / Date"]))
    if r.get("Client / Organiser") and r["Client / Organiser"] != "Private client":
        note = (": " + r["Programme Note"][0].lower() + r["Programme Note"][1:].rstrip(".")) if r.get("Programme Note") else ""
        out.append(("Who was %s for?" % name, "%s%s." % (r["Client / Organiser"], note)))
    elif r.get("Programme Note"):
        out.append(("What kind of event was %s?" % name, r["Programme Note"].rstrip(".") + "."))
    if r.get("DMC Services Delivered"):
        tail = (" " + sentence(n["Execution"])) if n.get("Execution") else ""
        out.append(("What did DMC Turkey Partner deliver for %s?" % name, r["DMC Services Delivered"] + "." + tail))
    if len(f["photos"]) >= 3:
        built = "; ".join(p.rstrip(".") for p in f["photos"][:3])
        out.append(("What was built on site for %s?" % name, "The project photos show: %s." % built))
    return out


def services_html(f):
    names = [s.strip() for s in f["rows"].get("DMC Services Delivered", "").split(",") if s.strip()]
    items = []
    for s in names:
        href = SERVICE_PAGES.get(s)
        label = html.escape(s, quote=False)
        items.append('<li><a href="%s">%s</a></li>' % (href, label) if href else "<li>%s</li>" % label)
    return "<ul>%s</ul>" % "".join(items) if items else ""


def related(slug, f, all_facts):
    cat = f["rows"].get("Event Category")
    same = [(s, g) for s, g in all_facts.items() if s != slug and g["rows"].get("Event Category") == cat]
    dest = f["rows"].get("Destination", "")
    same.sort(key=lambda sg: (sg[1]["rows"].get("Destination", "") != dest, sg[0]))
    others = [(s, g) for s, g in all_facts.items() if s != slug and (s, g) not in same]
    pick = (same + others)[:3]
    return "".join('<a href="/selected-works/%s/">%s</a>' % (s, html.escape(g["name"], quote=False)) for s, g in pick)


def block(slug, f, all_facts, faqs):
    faq = "".join('<div class="faq-item"><h3>%s</h3><p>%s</p></div>' % (html.escape(q, quote=False), html.escape(a, quote=False))
                  for q, a in faqs)
    return (
        "    %s\n"
        '    <section class="page-section" id="services">\n'
        "      <h2>Services on This Project</h2>\n      %s\n    </section>\n"
        '    <section class="page-section" id="faq">\n'
        "      <h2>Frequently Asked Questions</h2>\n"
        '      <div class="faq-list">%s</div>\n'
        '      <p class="reviewed-note">Last updated: <time datetime="%s">%s</time></p>\n'
        "    </section>\n"
        '    <section class="page-section" id="related-projects">\n'
        "      <h2>Related Projects</h2>\n"
        '      <div class="cluster-links">%s</div>\n'
        "    </section>\n    %s\n"
    ) % (BEGIN, services_html(f), faq, TODAY[0], TODAY[1], related(slug, f, all_facts), END)


def schema(slug, faqs):
    data = {
        "@context": "https://schema.org", "@type": "FAQPage",
        "@id": "%s/selected-works/%s/#faq" % (SITE, slug), "dateModified": TODAY[0],
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs],
    }
    return '  %s\n  <script type="application/ld+json">%s</script>\n  %s\n' % (LD_BEGIN, json.dumps(data, ensure_ascii=False), LD_END)


def strip(text):
    for b, e in ((BEGIN, END), (LD_BEGIN, LD_END)):
        text = re.sub(r"[ \t]*" + re.escape(b) + r".*?" + re.escape(e) + r"\n", "", text, flags=re.S)
    return text


def main():
    pages = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "selected-works", "*", "index.html"))):
        slug = os.path.basename(os.path.dirname(path))
        with open(path, encoding="utf-8") as handle:
            pages[slug] = strip(handle.read())
    all_facts = {slug: facts(text) for slug, text in pages.items()}
    for slug, text in pages.items():
        f = all_facts[slug]
        faqs = faqs_for(f)
        if len(faqs) < 3:
            raise SystemExit("Too few facts for an FAQ on %s" % slug)
        if ANCHOR not in text:
            raise SystemExit("No CTA anchor on %s" % slug)
        at = text.index(ANCHOR)
        at = text.rfind("\n", 0, at) + 1  # insert whole lines, keeping the anchor's indentation
        text = text[:at] + block(slug, f, all_facts, faqs) + text[at:]
        text = text.replace("</head>", schema(slug, faqs) + "</head>", 1)
        with open(os.path.join(ROOT, "selected-works", slug, "index.html"), "w", encoding="utf-8") as handle:
            handle.write(text)
    print("enriched %d project pages" % len(pages))


if __name__ == "__main__":
    main()
