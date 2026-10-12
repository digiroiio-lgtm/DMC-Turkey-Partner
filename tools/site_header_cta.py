#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Synchronize the Fam Trip 2027 header call-to-action on every page.

Usage: python3 tools/site_header_cta.py [--check]

The site has no build step, so the header is duplicated in each index.html. This
patches it idempotently:
  * desktop/tablet and phone bar: a dark "Fam Trip 2027" button between "Book a
    Partner Call" and the green "Request a Proposal" (inside .site-header__cta),
  * mobile drawer: a prominent first item in #primary-nav.
Both only exist while campaign/uk-fam-trip.json has "enabled": true; with the campaign
disabled the markers and links are removed. Run automatically by fam_trip_build.py.
"""

import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS = os.path.join(ROOT, "campaign", "uk-fam-trip.json")
LANDING = "/agency-fam-trip-2027/"

BAR_BEGIN, BAR_END = "<!-- fam-header:begin -->", "<!-- fam-header:end -->"
NAV_BEGIN, NAV_END = "<!-- fam-nav:begin -->", "<!-- fam-nav:end -->"
BAR_RE = re.compile(r"[ \t]*" + re.escape(BAR_BEGIN) + r".*?" + re.escape(BAR_END) + r"\n", re.S)
NAV_RE = re.compile(r"[ \t]*" + re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END) + r"\n", re.S)
CTA_PRIMARY = re.compile(r'([ \t]*)(<a class="btn btn--primary" href="/request-proposal/">[^<]*</a>)')
NAV_LIST = '        <ul class="site-nav__list" id="primary-nav">\n'

PLANE = ('<svg class="fam-cta__icon" width="18" height="18" viewBox="0 0 20 20" aria-hidden="true" focusable="false">'
         '<path d="M2.5 10.5l15-7-4 13-3.2-4.2-3.3 2.2.5-3.6z" fill="none" stroke="currentColor" stroke-width="1.5" '
         'stroke-linejoin="round"/></svg>')


def enabled():
    with open(SETTINGS, encoding="utf-8") as handle:
        return bool(json.load(handle).get("enabled"))


def bar_link(current):
    if current:
        attrs = 'href="%s" aria-current="page"' % LANDING
    else:
        attrs = 'href="%s?src=header" data-fam-header="bar"' % LANDING
    return ('<a class="btn btn--fam" %s>%s<span class="fam-cta__label">Fam Trip 2027</span>'
            '<span class="fam-cta__arrow" aria-hidden="true">&nearr;</span></a>' % (attrs, PLANE))


def nav_item(current):
    if current:
        attrs = 'href="%s" aria-current="page"' % LANDING
    else:
        attrs = 'href="%s?src=header-menu" data-fam-header="menu"' % LANDING
    return ('<li class="nav-fam-item"><a class="nav-fam" %s>%s<span class="nav-fam__text">'
            '<strong>Fam Trip 2027</strong><small>Invitation for MICE agencies</small></span>'
            '<span class="fam-cta__arrow" aria-hidden="true">&nearr;</span></a></li>' % (attrs, PLANE))


def sync(html, on, current=False):
    html = BAR_RE.sub("", NAV_RE.sub("", html))
    if not on:
        return html
    html = CTA_PRIMARY.sub(
        lambda m: "%s%s%s%s\n%s" % (m.group(1), BAR_BEGIN, bar_link(current), BAR_END, m.group(1) + m.group(2)), html, count=1)
    if NAV_LIST in html:
        indent = "          "
        html = html.replace(NAV_LIST, "%s%s%s%s%s\n" % (NAV_LIST, indent, NAV_BEGIN, nav_item(current), NAV_END), 1)
    return html


def pages():
    found = glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)
    def has_header(path):
        with open(path, encoding="utf-8") as handle:
            return 'class="site-header__cta"' in handle.read()

    return sorted(p for p in found if has_header(p))


def run(check=False):
    on = enabled()
    changed = []
    for path in pages():
        with open(path, encoding="utf-8") as handle:
            source = handle.read()
        current = os.path.relpath(path, ROOT) == os.path.join("agency-fam-trip-2027", "index.html")
        updated = sync(source, on, current)
        if updated != source:
            changed.append(os.path.relpath(path, ROOT))
            if not check:
                with open(path, "w", encoding="utf-8") as handle:
                    handle.write(updated)
    return on, changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    on, changed = run(check=args.check)
    state = "enabled" if on else "disabled"
    if args.check:
        print("%d pages out of date (header CTA %s)" % (len(changed), state))
        sys.exit(1 if changed else 0)
    print("header CTA %s: %d pages updated" % (state, len(changed)))


if __name__ == "__main__":
    main()
