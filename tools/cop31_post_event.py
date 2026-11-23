#!/usr/bin/env python3
"""After COP31 (9–20 November 2026): move the five COP31 service pages to
permanent Antalya URLs.

COP31 is over. The business decided not to claim it delivered COP31 work, so
the service pages lose every conference-specific sentence and become general
Antalya service pages; prices, project cards, process notes and FAQs stay.
The COP31 hub, participant guide, venue, hotels, event-services and news pages
stay as an information archive (see tools/cop31_archive_note.py).

What this script does, once:
  1. Copies each old page to its new folder, rewrites head, breadcrumb,
     JSON-LD, proposal links and the conference-specific copy (OLD_NEW and
     DROP_SECTIONS below), regenerates the FAQPage JSON-LD from the visible
     FAQ, and deletes the old folder.
  2. Rewrites every internal link to the old URLs, in pages, llms*.txt,
     sitemaps and the tools that generate pages.
  3. Adds 301s (vercel.json and _redirects) and points older redirects that
     ended on an old URL straight at the new one, so there are no chains.

It refuses to finish if a moved page still mentions COP31, UNFCCC or the
conference dates.

Usage: python3 tools/cop31_post_event.py
"""

import glob
import html as htmllib
import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://dmcturkeypartner.com"
TODAY = "21 November 2026"
TODAY_ISO = "2026-11-21"

MOVES = {
    "cop31-event-production": "antalya-event-production",
    "cop31-exhibition-services": "exhibition-stands-antalya",
    "cop31-event-staff": "event-staff-antalya",
    "cop31-antalya-transport": "antalya-airport-transfers-group-transport",
    "cop31-last-minute-services": "last-minute-event-services-antalya",
}

META = {
    "cop31-event-production": dict(
        title="Event Production &amp; AV Rental Antalya | Staging, LED, Sound",
        description="Event production and AV rental in Antalya for conferences, corporate events and "
                    "receptions: staging, LED screens, sound, lighting, technicians and hire ranges.",
        h1="Event Production and AV Rental in Antalya",
        service="Event Production Antalya",
    ),
    "cop31-exhibition-services": dict(
        title="Exhibition Stands Antalya | Stands, Pavilions, Furniture &amp; Print",
        description="Exhibition stands and exhibitor services in Antalya: modular and custom stands, "
                    "pavilions, furniture, coffee stations, branding, signage and print, built locally.",
        h1="Exhibition Stands and Exhibitor Services in Antalya – Stands, Pavilions, Furniture and Print",
        service="Exhibition Stands Antalya",
    ),
    "cop31-event-staff": dict(
        title="Event Staff Antalya | Hostesses, Interpreters &amp; Crew",
        description="Event staff in Antalya for conferences, exhibitions and corporate events: crew, "
                    "hostesses, registration desks and interpreters, with staffing ratios and day rates.",
        h1="Event Staff in Antalya – Crew, Hostesses and Interpreters",
        service="Event Staff Antalya",
    ),
    "cop31-antalya-transport": dict(
        title="Antalya Airport Transfers &amp; Group Transport | Prices per Vehicle",
        description="Antalya airport transfers and group transport for conferences, incentives and event "
                    "teams: routes, vehicle types, meet &amp; greet and per-vehicle prices from €70.",
        h1="Antalya Airport Transfers, Group Transport and Private Vehicles",
        service="Airport Transfers &amp; Group Transport Antalya",
    ),
    "cop31-last-minute-services": dict(
        title="Last-Minute Event Services Antalya | Urgent Print, AV, Staff",
        description="Urgent event support in Antalya: printing, signage, furniture, screens, staff, "
                    "interpreters and vehicles for conferences and exhibitions already under way.",
        h1="Last-Minute Event Services in Antalya",
        service="Last-Minute Event Services Antalya",
    ),
}

# Whole sections (by their <h2>) that only made sense around the conference.
DROP_SECTIONS = [
    "Planning Context for COP31 Antalya",
    "Continue Planning for COP31 Antalya",
    "Official COP31 Resources",
    "Official Shuttle Services",
    "Rental Availability During COP31",
]

# Related links that replace "Continue Planning for COP31 Antalya".
RELATED = [
    ("/destinations/antalya/", "Antalya DMC"),
    ("/antalya-event-production/", "Event Production"),
    ("/exhibition-stands-antalya/", "Exhibition Stands"),
    ("/event-staff-antalya/", "Event Staff"),
    ("/antalya-airport-transfers-group-transport/", "Airport Transfers &amp; Group Transport"),
    ("/last-minute-event-services-antalya/", "Last-Minute Services"),
    ("/antalya-transfer-prices/", "Antalya Transfer Prices"),
    ("/event-costs/antalya/", "Antalya Event Costs"),
]

# Exact (old, new) text replacements, applied to the whole file. Each old
# string must be found at least once, so a silent miss cannot leave COP31 copy
# behind. Shared ones first, then per page.
from cop31_post_event_copy import COMMON, PAGES  # noqa: E402


def drop_section(text, heading):
    pos = text.find("<h2>%s</h2>" % heading)
    if pos == -1:
        pos = text.find(">%s</h2>" % heading)
        if pos == -1:
            return text, False
    start = text.rfind("<section", 0, pos)
    end = text.find("</section>", pos) + len("</section>")
    line_start = text.rfind("\n", 0, start) + 1
    if text[line_start:start].strip() == "":
        start = line_start
    if text[end:end + 1] == "\n":
        end += 1
    return text[:start] + text[end:], True


def drop_toc_entries(text):
    """Remove "On this page" entries whose target section no longer exists."""
    def keep(m):
        target = m.group(1)
        return m.group(0) if ('id="%s"' % target) in text else ""
    return re.sub(r'<li><a href="#([^"]+)">[^<]*</a></li>', keep, text)


def related_section():
    links = "".join('<a href="%s">%s</a>' % pair for pair in RELATED)
    return ('    <section class="page-section">\n      <h2>Related Antalya Services</h2>\n'
            '      <div class="cluster-links">%s</div>\n    </section>\n' % links)


def faq_jsonld(text):
    items = re.findall(r'<div class="faq-item"><h3>(.*?)</h3>(.*?)</div>', text, re.S)

    def plain(s):
        return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", "", s))).strip()

    data = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": plain(q), "acceptedAnswer": {"@type": "Answer", "text": plain(a)}}
        for q, a in items]}
    return json.dumps(data, ensure_ascii=False)


def rewrite_page(old, new, text):
    meta = META[old]
    url = "%s/%s/" % (SITE, new)

    for heading in DROP_SECTIONS:
        text, _ = drop_section(text, heading)
    text = re.sub(r"[ \t]*<!-- cop31-latest:begin -->.*?<!-- cop31-latest:end -->\n", "", text, flags=re.S)
    # The independence disclaimer only existed to separate us from the
    # official organisers; the page no longer mentions them.
    text = re.sub(r'<section class="page-section"><p class="disclaimer">.*?</section>\n?', "", text, flags=re.S)
    text = drop_toc_entries(text)

    # Head.
    text = re.sub(r"<title>.*?</title>", "<title>%s</title>" % meta["title"], text, count=1)
    for attr in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        text = re.sub(r'(<meta %s content=")[^"]*(")' % attr, r"\g<1>%s\g<2>" % meta["description"], text)
    for attr in ('property="og:title"', 'name="twitter:title"'):
        text = re.sub(r'(<meta %s content=")[^"]*(")' % attr, r"\g<1>%s\g<2>" % meta["title"], text)
    text = re.sub(r'<meta name="dmc:lead-source" content="[^"]*">', '<meta name="dmc:lead-source" content="Website">', text)
    text = re.sub(r'<meta name="dmc:campaign" content="[^"]*">', '<meta name="dmc:campaign" content="Antalya Event Services">', text)
    text = re.sub(r'<meta name="dmc:service-interest" content="[^"]*">',
                  '<meta name="dmc:service-interest" content="%s">' % meta["service"], text)

    # Proposal links carry the lead source in the query string.
    def proposal(m):
        q = m.group(1)
        q = re.sub(r"src=[^&\"]*", "src=" + new, q)
        q = re.sub(r"lead_source=[^&\"]*", "lead_source=Website", q)
        q = re.sub(r"campaign=[^&\"]*", "campaign=Antalya%20Event%20Services", q)
        q = re.sub(r"service_interest=[^&\"]*", "service_interest=" + meta["service"].replace(" ", "%20").replace("&amp;", "%26"), q)
        q = re.sub(r"project_type=COP31[^&\"]*", "project_type=Conference", q)
        return "/request-proposal/?" + q
    text = re.sub(r"/request-proposal/\?([^\"]*)", proposal, text)

    # Breadcrumb: Home › Antalya › page.
    text = re.sub(r'<li><a href="/cop31-antalya/">COP31 Antalya 2026</a></li>',
                  '<li><a href="/destinations/antalya/">Antalya</a></li>', text)
    text = text.replace('"name":"COP31 Antalya 2026","item":"https://dmcturkeypartner.com/cop31-antalya/"',
                        '"name":"Antalya","item":"https://dmcturkeypartner.com/destinations/antalya/"')
    text = re.sub(r"<h1>.*?</h1>", "<h1>%s</h1>" % meta["h1"], text, count=1)

    for old_s, new_s in COMMON + PAGES[old]:
        if isinstance(old_s, re.Pattern):
            text = old_s.sub(new_s, text)
        elif old_s in text:
            text = text.replace(old_s, new_s)
        elif old_s not in [o for o, _ in COMMON]:
            raise SystemExit("%s: copy not found: %r" % (old, old_s[:90]))

    # Service JSON-LD.
    def service(m):
        data = json.loads(m.group(1))
        if data.get("@type") != "Service":
            return m.group(0)
        data["name"] = htmllib.unescape(meta["h1"].split(" – ")[0])
        data["serviceType"] = htmllib.unescape(meta["service"])
        data["url"] = url
        data["description"] = htmllib.unescape(meta["description"])
        return '<script type="application/ld+json">\n  %s\n  </script>' % json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    text = re.sub(r'<script type="application/ld\+json">\s*(\{"@context":"https://schema.org","@type":"Service".*?\})\s*</script>',
                  service, text, flags=re.S)
    text = re.sub(r'(<script type="application/ld\+json">\s*)\{"@context":\s*"https://schema.org",\s*"@type":\s*"FAQPage".*?\}(\s*</script>)',
                  lambda m: m.group(1) + faq_jsonld(text) + m.group(2), text, count=1, flags=re.S)

    text = re.sub(r"Last updated: \d{1,2} [A-Z][a-z]+ 2026", "Last updated: " + TODAY, text)
    text = re.sub(r'Last updated: <time datetime="[\d-]+">[^<]*</time>',
                  'Last updated: <time datetime="%s">%s</time>' % (TODAY_ISO, TODAY), text)
    text = re.sub(r'"dateModified":\s*"\d{4}-\d{2}-\d{2}"', '"dateModified":"%s"' % TODAY_ISO, text)
    return text


OLD_RE = re.compile(r"(?<![\w-])(%s)(?![\w-])" % "|".join(map(re.escape, MOVES)))


def relink(text):
    return OLD_RE.sub(lambda m: MOVES[m.group(1)], text)


def link_files():
    files = glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)
    # vercel.json/_redirects are handled in add_redirects: a blind rewrite
    # would turn the new "old -> new" rules into "new -> new" loops on re-runs.
    files += [os.path.join(ROOT, n) for n in ("llms.txt", "llms-full.txt")]
    files += glob.glob(os.path.join(ROOT, "sitemap-*.xml"))
    files += [p for p in glob.glob(os.path.join(ROOT, "tools", "*.py"))
              if not p.endswith(("cop31_post_event.py", "cop31_post_event_copy.py"))]
    return [f for f in files if os.sep + ".git" + os.sep not in f and "node_modules" not in f]


def add_redirects():
    path = os.path.join(ROOT, "vercel.json")
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    # Older rules that ended on an old URL now go straight to the new one.
    for rule in data["redirects"]:
        rule["destination"] = relink(rule["destination"])
    have = {r["source"] for r in data["redirects"]}
    for old, new in MOVES.items():
        for src, dst in (("/" + old, "/%s/" % new), ("/%s/:path*" % old, "/%s/" % new)):
            if src not in have:
                data["redirects"].append({"source": src, "destination": dst, "statusCode": 301})
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    path = os.path.join(ROOT, "_redirects")
    with open(path, encoding="utf-8") as handle:
        lines = handle.read().rstrip("\n").split("\n")
    lines = [" ".join([ln.split()[0], relink(ln.split()[1])] + ln.split()[2:])
             if ln.strip() and not ln.startswith("#") and len(ln.split()) >= 2 else ln for ln in lines]
    sources = {ln.split()[0] for ln in lines if ln.strip() and not ln.startswith("#")}
    for old, new in MOVES.items():
        for src in ("/%s" % old, "/%s/*" % old):
            if src not in sources:
                lines.append("%s /%s/ 301!" % (src, new))
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


LEFTOVER = re.compile(r"COP ?31|UNFCCC|Blue Zone|Green Zone|Leaders Summit|9.20 Nov|[Aa]ccredit|11.12 Nov|"
                      r"Presidency|[Oo]fficial (?:shuttle|transport|COP|accommodation|participant)|\b(?:9|20) November|"
                      r"EXPO Center|[Ss]ide[- ]event|conference period|conference fortnight|[Dd]elegates?\b|bilaterals")


def refresh_llms_full():
    """Re-render the moved pages' blocks in llms-full.txt from their new HTML."""
    from cop31_consolidate import page_to_text
    path = os.path.join(ROOT, "llms-full.txt")
    with open(path, encoding="utf-8") as handle:
        blocks = handle.read().split("\n---\n\n")
    out = []
    for block in blocks:
        url = re.search(r"^URL: %s/([^\n]*)/$" % re.escape(SITE), block, re.M)
        if url and url.group(1) in MOVES.values():
            block = page_to_text(url.group(1) + "/index.html")
        out.append(block)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n---\n\n".join(out).rstrip("\n") + "\n")


def main():
    for old, new in MOVES.items():
        src = os.path.join(ROOT, old, "index.html")
        if not os.path.exists(src):
            print("already moved: /%s/" % old)
            continue
        with open(src, encoding="utf-8") as handle:
            text = rewrite_page(old, new, handle.read())
        text = text.replace('data-track="cop31_proposal_cta_click"', 'data-track="service_proposal_cta_click"')
        text = text.replace('data-track="cop31_whatsapp_click"', 'data-track="service_whatsapp_click"')
        text = relink(text).replace("COP31 Antalya 2026 local event services",
                                    "Antalya conference and exhibition services")
        main_html = re.search(r'<main id="main-content">.*?</main>', text, re.S).group(0)
        head = text[:text.index("<body")]
        visible = re.sub(r'<!--.*?-->|(?:href|id|class|data-track|src|aria-controls)="[^"]*"', "", main_html + head, flags=re.S)
        left = [m.group(0) for m in LEFTOVER.finditer(visible)]
        if left:
            raise SystemExit("%s still mentions: %s" % (old, sorted(set(left))))
        # The "Continue planning" block is gone; add plain related links
        # just before the closing CTA note / end of main.
        anchor = "  </main>"
        text = text.replace(anchor, related_section() + anchor, 1)
        os.makedirs(os.path.join(ROOT, new), exist_ok=True)
        with open(os.path.join(ROOT, new, "index.html"), "w", encoding="utf-8") as handle:
            handle.write(text)
        shutil.rmtree(os.path.join(ROOT, old))
        print("moved /%s/ -> /%s/" % (old, new))

    changed = 0
    for path in link_files():
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        # Organisation JSON-LD (tools/site_config.py and every page) listed
        # COP31 among the services; describe the evergreen service instead.
        text = relink(original).replace("COP31 Antalya 2026 local event services",
                                        "Antalya conference and exhibition services")
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    add_redirects()
    refresh_llms_full()
    print("links rewritten in %d files; redirects added" % changed)


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    main()
