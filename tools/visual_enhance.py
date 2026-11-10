#!/usr/bin/env python3
"""Visual–text balance pass (November 2026).

An internal readability audit found 90 of 110 pages without a single image,
48 with two or more text-only sections in a row (mostly runs of planning
Q&A sections) and 19 with paragraphs over 80 words. This pass adds visual
structure without removing or rewording any copy:

1. Card icons — an original line icon (assets/img/icons.svg) before the
   heading of text cards whose topic it names (hotel, transport, stage...).
   Decorative: aria-hidden, the heading text carries the meaning.
2. Q&A blocks — sections whose H2 is a question get class "qa-block" and a
   question icon, styled as a separated two-column panel on desktop.
3. Project photos — one relevant photo from the company's own event
   photography (tools/production_showcase_data.py) on key pages that have
   none, with its existing descriptive alt text and caption, lazy-loaded,
   with width/height to prevent layout shift.
4. Long paragraphs — plain paragraphs over 80 words are split at the
   sentence boundary nearest their middle. Text is unchanged.

Fully generated pages (hotel offers, off-season, transfer prices, Fam Trip,
Czech/German, legal, showcase, calculator) are skipped: their builders own
the markup. Idempotent: re-running changes nothing.

Usage: python3 tools/visual_enhance.py
"""

import glob
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import production_showcase_data as showcase  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPRITE = "/assets/img/icons.svg"
FIG_BEGIN, FIG_END = "<!-- visual-photo:begin -->", "<!-- visual-photo:end -->"

SKIP = re.compile(
    r"^(group-hotel-offers-turkey|off-season-events-turkey|antalya-transfer-prices|agency-fam-trip-2027|"
    r"antalya-fam-trip-2027|antalya-fam-trips|cs|de|cookie-policy|privacy-policy|terms|production-showcase|"
    r"event-cost-calculator|request-proposal)(/|$)"
)

# First match wins; checked against the card heading text, lower-cased.
ICON_RULES = [
    ("question", r"\?$"),
    ("hotel", r"hotel|accommodation|room|resort|stay"),
    ("bus", r"transport|transfer|vehicle|shuttle|coach|van\b|minivan|driver|getting around|movement"),
    ("plane", r"airport|arrival|flight|getting there"),
    ("stage", r"stage|staging|\bav\b|audio|sound|lighting|led|screen|production|technical|technician|rigging|set\b"),
    ("venue", r"venue|ballroom|space|pavilion|expo|hall"),
    ("people", r"staff|crew|host|hostess|interpreter|supervisor|team|guide|people|delegat|guest"),
    ("euro", r"budget|cost|price|rate|€|fee|quote|invoice"),
    ("chair", r"furniture|table|stool|seating|chair|sofa|lounge"),
    ("sign", r"sign|graphic|branding|print|banner|decal|sticker|wayfinding|board|wrap"),
    ("weather", r"weather|season|climate|winter|summer"),
    ("mic", r"meeting|conference|congress|training|session|plenary|speaker"),
    ("dining", r"dinner|dining|lunch|catering|food|coffee|water|f&amp;b|beverage|gala|reception"),
    ("box", r"storage|shipping|shipment|logistics|stock|delivery|freight"),
    ("calendar", r"date|schedule|timeline|deadline|programme day|day "),
    ("trophy", r"incentive|reward|award"),
    ("handshake", r"partner|agency|white-label|white label|supplier|contract"),
    ("clipboard", r"plan|brief|checklist|scope|review|report|registration|accreditation"),
    ("pin", r"antalya|belek|istanbul|bodrum|cappadocia|kemer|side|lara|kundu|aksu|destination|city"),
]

# Page -> showcase photo (own event photography with published alt text).
PHOTOS = {
    "mice-turkey": "plenary-conference-setup-cw-enerji-antalya",
    "corporate-events-turkey": "led-wall-stage-light-show-corporate-event-turkey",
    "incentive-travel-turkey": "red-carpet-led-entrance-mapfre-sigorta-antalya",
    "white-label-dmc-turkey": "led-registration-desk-rixos-sungate-antalya",
    "group-travel-turkey": "branded-registration-desk-cw-enerji-antalya",
    "guides/mice-in-turkey": "classroom-conference-setup-led-screens-turkey",
    "services": "curved-led-wall-stage-viennalife-event-turkey",
    "services/meetings-conferences": "dealer-meeting-conference-stage-iveco-turkey",
    "services/venue-sourcing": "theatre-style-stage-led-screens-jti-meeting-turkey",
    "services/hotel-sourcing": "branded-hotel-entrance-vakifbank-summit-2025-turkey",
    "services/ground-handling": "welcome-desk-led-backdrop-iveco-50-years-turkey",
    "services/incentive-programs": "building-facade-wrap-bellona-dealer-meeting-turkey",
    "services/group-travel": "registration-counter-viennalife-event-turkey",
    "agency-partners": "lobby-branding-totems-jti-tek-ekip-turkey",
    "about": "led-tunnel-entrance-vakifbank-management-summit-turkey",
    "why-turkey": "open-air-ceremony-stage-istek-schools-antalya",
}


def icon(name, cls):
    return ('<svg class="%s" aria-hidden="true" focusable="false" width="24" height="24">'
            '<use href="%s#%s"></use></svg>') % (cls, SPRITE, name)


def plain(fragment):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def pick_icon(heading):
    t = plain(heading).lower()
    for name, pattern in ICON_RULES:
        if re.search(pattern, t):
            return name
    return None


def card_icons(text):
    def repl(m):
        art, h3 = m.group(1), m.group(2)
        if "card-icon" in art or "<img" in art:
            return m.group(0)
        name = pick_icon(h3)
        if not name or name == "question":
            return m.group(0)
        return art + icon(name, "card-icon") + h3
    # Card titles are either an <h3> or a leading <p><strong>…</strong>.
    text = re.sub(r'(<article class="card"[^>]*>)(<h3>.*?</h3>|<p><strong>.*?</strong>)', repl, text, flags=re.S)

    # Within one grid, either every text card has an icon or none does.
    def grid(m):
        block = m.group(0)
        cards = re.findall(r'<article class="card"[^>]*>(?:<h3>|<p><strong>)', block)
        with_icon = block.count('class="card-icon"')
        if not with_icon or with_icon >= len(re.findall(r'<article class="card"', block)):
            return block
        return re.sub(r'(<article class="card"[^>]*>)(?=<h3>|<p><strong>)', lambda a: a.group(1) + icon("clipboard", "card-icon"), block)
    return re.sub(r'<div class="card-grid[^"]*">(?:(?!<div class="card-grid).)*?</div>', grid, text, flags=re.S)


def qa_blocks(text):
    def repl(m):
        attrs, h2, body = m.group(1), m.group(2), m.group(3)
        if "qa-block" in attrs or not plain(h2).endswith("?"):
            return m.group(0)
        # Only plain answer sections: grids, tables, forms and cards keep the full width.
        if re.search(r'<(table|form|figure|section)\b|class="[^"]*(card|grid|cta)', body):
            return m.group(0)
        attrs = attrs.replace('class="page-section"', 'class="page-section qa-block"', 1)
        return "<section%s>%s%s%s</section>" % (attrs, icon("question", "qa-icon"), h2, body)
    return re.sub(r'<section( class="page-section"[^>]*)>(\s*<h2>.*?</h2>)(.*?)</section>', repl, text, flags=re.S)


PHOTO_INDEX = {p[1]: p for p in showcase.PHOTOS}


def photo_size(name):
    from PIL import Image
    with Image.open(os.path.join(ROOT, "assets/img/showcase", name + ".webp")) as im:
        return im.size


def figure(name):
    _src, slug, _cat, alt, caption = PHOTO_INDEX[name]
    w, h = photo_size(slug)
    return (
        "    %s\n"
        '    <figure class="content-figure">\n'
        '      <img src="/assets/img/showcase/%s-640.webp" srcset="/assets/img/showcase/%s-640.webp 640w, '
        '/assets/img/showcase/%s.webp %dw" sizes="(max-width: 900px) calc(100vw - 2.5rem), 860px" '
        'width="%d" height="%d" alt="%s" loading="lazy" decoding="async">\n'
        "      <figcaption>%s · <a href=\"/production-showcase/\">More of our event production</a></figcaption>\n"
        "    </figure>\n    %s\n"
    ) % (FIG_BEGIN, slug, slug, slug, w, w, h, html.escape(alt), html.escape(caption, quote=False), FIG_END)


def add_photo(text, rel):
    text = re.sub(r"[ \t]*" + re.escape(FIG_BEGIN) + r".*?" + re.escape(FIG_END) + r"\n", "", text, flags=re.S)
    name = PHOTOS.get(rel)
    if not name:
        return text
    main = text.find("<main")
    # After the first content section that follows the hero.
    sections = [m.start() for m in re.finditer(r'\n[ \t]*<section class="page-section', text[main:])]
    if len(sections) < 3:
        return text
    at = main + sections[2] + 1
    return text[:at] + figure(name) + text[at:]


SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9“\"(])")


def split_paragraphs(text):
    def repl(m):
        attrs, inner = m.group(1), m.group(2)
        if re.search(r"<(ul|ol|div|table|br|p)\b", inner) or len(plain(inner).split()) <= 80:
            return m.group(0)
        cuts = [c.start() for c in SENTENCE.finditer(inner)]
        if not cuts:
            return m.group(0)
        mid = len(inner) / 2
        cut = min(cuts, key=lambda c: abs(c - mid))
        # Never split inside a tag or an anchor.
        before = inner[:cut]
        if before.count("<a ") != before.count("</a>") or before.rfind("<") > before.rfind(">"):
            return m.group(0)
        return "<p%s>%s</p>\n      <p%s>%s</p>" % (attrs, inner[:cut].rstrip(), attrs, inner[cut:].lstrip())
    return re.sub(r"<p((?: class=\"[^\"]*\")?)>(.*?)</p>", repl, text, flags=re.S)


TOC_BEGIN, TOC_END = "<!-- visual-toc:begin -->", "<!-- visual-toc:end -->"


def slug(text_):
    s_ = re.sub(r"[^a-z0-9]+", "-", plain(text_).lower()).strip("-")
    return s_[:60].rstrip("-") or "section"


def toc(text, rel=""):
    """5. 'On this page' jump list for long pages (8+ H2 sections, 1,800+ words)."""
    text = re.sub(r"[ \t]*" + re.escape(TOC_BEGIN) + r".*?" + re.escape(TOC_END) + r"\n", "", text, flags=re.S)
    start, end = text.find("<main"), text.find("</main>")
    main_ = text[start:end]
    heads = list(re.finditer(r"<h2( id=\"[^\"]*\")?>(.*?)</h2>", main_, re.S))
    heads = [h for h in heads if not re.search(r"FAQ|Frequently Asked|Related|Planning a|Request|Continue", plain(h.group(2)))]
    if not rel or len(heads) < 8 or len(plain(main_).split()) < 1800:  # not on the homepage
        return text
    used, items, new_main = set(), [], main_
    for h in heads:
        hid = re.search(r'id="([^"]+)"', h.group(0))
        if hid:
            ident = hid.group(1)
        else:
            ident = base = slug(h.group(2))
            n = 2
            while ident in used or ('id="%s"' % ident) in text:
                ident = "%s-%d" % (base, n)
                n += 1
            new_main = new_main.replace(h.group(0), '<h2 id="%s">%s</h2>' % (ident, h.group(2)), 1)
        used.add(ident)
        items.append('<li><a href="#%s">%s</a></li>' % (ident, plain(h.group(2)).replace("&", "&amp;").replace("<", "&lt;")))
    block = ('    %s\n    <nav class="page-toc" aria-label="On this page">\n      <p class="page-toc__label">On this page</p>\n'
             '      <ol>%s</ol>\n    </nav>\n    %s\n') % (TOC_BEGIN, "".join(items), TOC_END)
    sections = [m.start() for m in re.finditer(r'\n[ \t]*<section class="page-section', new_main)]
    if len(sections) < 2:
        return text
    at = sections[1] + 1
    new_main = new_main[:at] + block + new_main[at:]
    return text[:start] + new_main + text[end:]


def main():
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)):
        rel = os.path.relpath(os.path.dirname(path), ROOT)
        rel = "" if rel == "." else rel
        if "node_modules" in path or SKIP.match(rel):
            continue
        with open(path, encoding="utf-8") as handle:
            original = handle.read()
        if 'name="robots" content="noindex' in original:
            continue
        start, end = original.find("<main"), original.find("</main>")
        if start == -1 or end == -1:
            continue
        head, main, tail = original[:start], original[start:end], original[end:]
        main = split_paragraphs(qa_blocks(card_icons(main)))
        text = toc(add_photo(head + main + tail, rel), rel)
        if text != original:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(text)
            changed += 1
    print("visual pass: %d pages changed" % changed)


if __name__ == "__main__":
    main()
