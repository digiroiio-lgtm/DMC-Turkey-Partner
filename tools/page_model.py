# -*- coding: utf-8 -*-
"""Read facts back out of a page's own markup. Pure functions; never writes.

Schema is derived from the rendered HTML rather than from a registry keyed by
URL. That choice matters. This site has no build step — content is edited
directly in the .html files — so a registry becomes a second copy of the truth
and goes stale the first time someone corrects a venue name in a <dd>. Google
treats structured data that asserts something the page does not say as spam,
and it is precisely the agreement between the two that makes FAQ and breadcrumb
markup eligible at all. Derived schema cannot drift by construction.

The cost is silent breakage if the markup changes shape. That is paid for in
tools/seo_check.py, which fails when a page in a known family does not yield
the fields its family needs, so a patcher never quietly emits a degraded node.

The markup turns out to be far more structured than "hand-written" suggests:

    /selected-works/*  <dl class="work-info"> with a stable dt vocabulary
    /event-costs/*     data-* attributes on <main>, including data-budget-range
    /events/*          data-event-card with year, country, city, category
    everywhere         one <h1>, .breadcrumbs ol, .faq-item h3+p, .page-section__lede
"""

import html as htmllib
import os
import re
from html.parser import HTMLParser

SITE = "https://dmcturkeypartner.com"


def _text(markup):
    return re.sub(r"\s+", " ", htmllib.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()


class _Definitions(HTMLParser):
    """Collect <dt>/<dd> pairs.

    Uses the stdlib parser rather than a regex because the case-study <dd>
    values contain raw unescaped ampersands ("Custom Decor & Branding"), which
    regexes handle inconsistently.
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pairs = []
        self._tag = None
        self._buf = []

    def handle_starttag(self, tag, attrs):
        if tag in ("dt", "dd"):
            self._flush()
            self._tag = tag

    def handle_endtag(self, tag):
        if tag in ("dt", "dd"):
            self._flush()

    def handle_data(self, data):
        if self._tag:
            self._buf.append(data)

    def _flush(self):
        if self._tag:
            self.pairs.append((self._tag, " ".join(self._buf).strip()))
            self._tag, self._buf = None, []

    def close(self):
        super().close()
        self._flush()


def definitions(markup):
    parser = _Definitions()
    parser.feed(markup)
    parser.close()
    out, key = {}, None
    for tag, value in parser.pairs:
        if tag == "dt":
            key = value
        elif key is not None:
            out[key] = value
            key = None
    return out


def url_for(rel):
    directory = os.path.dirname(rel)
    return "/" + directory + "/" if directory else "/"


# Listing markup settled into three shapes as the site grew. All three are a
# heading and a link to a page on this site, so ItemList is derived from any
# of them rather than requiring the templates be unified first.
_CARD_PATTERNS = (
    # <h3><a href="…">Label</a></h3>            services, destinations, events grid
    re.compile(r'<h3[^>]*>\s*<a href="(/[^"#?]*)"[^>]*>(.*?)</a>', re.S),
    # <a class="…-card" href="…"> … <h3>Label</h3> … </a>   selected works grid
    re.compile(r'<a[^>]+class="[^"]*card[^"]*"[^>]*href="(/[^"#?]*)"[^>]*>(.*?)</a>', re.S),
    # <p class="cluster-links"><a href="…">Label</a>        taxonomy link rows
    re.compile(r'<p class="cluster-links">(.*?)</p>', re.S),
)


def cards(body):
    """(absolute url, label) for every listing entry, in document order."""
    found, seen = [], set()

    for href, inner in _CARD_PATTERNS[0].findall(body):
        label = _text(inner)
        if label and href not in seen:
            seen.add(href)
            found.append((SITE + href, label))

    for href, inner in _CARD_PATTERNS[1].findall(body):
        heading = re.search(r"<h3[^>]*>(.*?)</h3>", inner, re.S)
        label = _text(heading.group(1)) if heading else _text(inner)
        if label and href not in seen:
            seen.add(href)
            found.append((SITE + href, label))

    for row in _CARD_PATTERNS[2].findall(body):
        for href, inner in re.findall(r'<a href="(/[^"#?]*)"[^>]*>(.*?)</a>', row, re.S):
            label = _text(inner)
            if label and href not in seen:
                seen.add(href)
                found.append((SITE + href, label))

    return found


def classify(url):
    """Which content family a URL belongs to. Drives which nodes get emitted."""
    parts = [p for p in url.strip("/").split("/") if p]
    if not parts:
        return "home"
    head = parts[0]
    depth = len(parts)

    if head == "services":
        return "service_hub" if depth == 1 else "service"
    if head == "destinations":
        return "destination_hub" if depth == 1 else "destination"
    if head == "selected-works":
        return "works_hub" if depth == 1 else "case_study"
    if head == "events":
        if depth == 1:
            return "events_hub"
        return "event" if re.search(r"-20\d\d$", parts[1]) else "event_taxonomy"
    if head == "event-costs":
        return "cost_hub" if depth <= 2 else "cost_scenario"
    if head == "cop31-news":
        return "cop31_news_hub" if depth == 1 else "cop31_news"
    if head.startswith("cop31"):
        return "cop31"
    if head == "guides":
        return "guides_hub" if depth == 1 else "guide"
    if head == "insights":
        return "insights_hub"
    if head in ("privacy-policy", "terms", "cookie-policy"):
        return "legal"
    if head in ("about", "contact", "agency-partners", "request-proposal", "why-turkey"):
        return "company"
    if head == "event-cost-calculator":
        return "tool"
    return "solution"


def read(path, root):
    """Everything the schema patcher needs from one page."""
    with open(path, encoding="utf-8") as handle:
        html = handle.read()

    rel = os.path.relpath(path, root)
    url = url_for(rel)
    main = html[html.index("<main") :] if "<main" in html else html
    body = re.sub(r"(?s)<header.*?</header>|<footer.*?</footer>", "", main)

    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    title = re.search(r"<title>(.*?)</title>", html, re.S)
    lede = re.search(r'<p class="[^"]*page-section__lede[^"]*">(.*?)</p>', body, re.S)
    if not lede:
        lede = re.search(r'<p class="[^"]*(?:cop31-answer|work-lede|hero-lede)[^"]*">(.*?)</p>', body, re.S)

    breadcrumbs = []
    crumbs = re.search(r'<nav class="breadcrumbs".*?<ol>(.*?)</ol>', html, re.S)
    if crumbs:
        for item in re.findall(r"<li[^>]*>(.*?)</li>", crumbs.group(1), re.S):
            link = re.search(r'href="([^"]*)"', item)
            breadcrumbs.append((_text(item), link.group(1) if link else None))

    faqs = []
    for block in re.findall(r'<div class="faq-item"[^>]*>(.*?)</div>', body, re.S):
        question = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.S)
        answers = re.findall(r"<p[^>]*>(.*?)</p>", block, re.S)
        if question and answers:
            faqs.append((_text(question.group(1)), " ".join(_text(a) for a in answers)))

    main_tag = re.search(r"<main([^>]*)>", html)
    attrs = dict(re.findall(r'(data-[a-z-]+)="([^"]*)"', main_tag.group(1))) if main_tag else {}

    return {
        "path": path,
        "rel": rel,
        "url": url,
        "absolute": SITE + url,
        "family": classify(url),
        "html": html,
        "title": _text(title.group(1)) if title else "",
        "h1": _text(h1.group(1)) if h1 else "",
        "lede": _text(lede.group(1)) if lede else "",
        "description": (
            re.search(r'<meta name="description" content="([^"]*)"', html).group(1)
            if re.search(r'<meta name="description" content="([^"]*)"', html)
            else ""
        ),
        "noindex": bool(re.search(r'name="robots" content="noindex', html)),
        "breadcrumbs": breadcrumbs,
        "faqs": faqs,
        "definitions": definitions(body),
        "main_attrs": attrs,
        "cards": cards(body),
        "word_count": len(_text(body).split()),
    }


def budget_range(page):
    """(low, high, currency) from data-budget-range, e.g. "140000-190000-eur"."""
    raw = page["main_attrs"].get("data-budget-range")
    if not raw:
        return None
    match = re.match(r"(\d+)-(\d+)-([a-z]{3})$", raw)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), match.group(3).upper()
