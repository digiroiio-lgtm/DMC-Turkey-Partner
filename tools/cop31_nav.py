#!/usr/bin/env python3
"""Insert the COP31 mega menu and footer column into every page on the site.

The site has no build step, so global chrome lives duplicated in each
index.html. This script performs that edit idempotently: running it twice is a
no-op, and re-running it after a nav change updates every page.

Usage: python3 tools/cop31_nav.py
"""

import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_links import PLAN, SERVICES, URGENT  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

NAV_ANCHOR = (
    '          <li class="nav-group">\n'
    '            <button type="button" class="nav-group__trigger" aria-expanded="false"'
    ' aria-controls="nav-company">Company</button>'
)

FOOTER_ANCHOR = (
    '        <div class="site-footer__col">\n'
    '          <h2 class="site-footer__heading">Company</h2>'
)

MARKER = 'aria-controls="nav-cop31"'
NAV_BEGIN = "<!-- cop31-nav:begin -->"
NAV_END = "<!-- cop31-nav:end -->"
# Matches a nav block injected before the begin/end markers existed.
LEGACY_NAV = re.compile(
    r'[ \t]*<li class="nav-group nav-group--mega">.*?\n[ \t]*</li>\n', re.S
)


def _menu_column(title, links, panel_id, first=False):
    """One group of the mega menu.

    The heading is a real <button> controlling its list. On desktop the list is
    always visible and the button is inert; on mobile it is the accordion
    control that keeps a 30-link menu from opening as one unusable wall of
    links. Rendering the button in both cases keeps the markup identical across
    breakpoints, so nothing has to be rebuilt on resize.
    """
    items = "".join(
        '\n                    <li%s><a href="%s">%s</a></li>'
        % (' class="nav-mega__feature"' if first and idx == 0 else "", href, label)
        for idx, (href, label) in enumerate(links)
    )
    return (
        '\n                <div class="nav-mega__col">'
        '\n                  <button type="button" class="nav-mega__heading"'
        ' aria-expanded="false" aria-controls="%s">%s</button>'
        '\n                  <ul class="nav-mega__panel" id="%s">%s'
        "\n                  </ul>"
        "\n                </div>" % (panel_id, title, panel_id, items)
    )


def nav_block():
    columns = (
        _menu_column("Plan Your COP31", PLAN, "nav-cop31-plan", first=True)
        + _menu_column("Local Services", SERVICES, "nav-cop31-services")
        + _menu_column("Urgent Support", URGENT, "nav-cop31-urgent")
    )
    return (
        "          " + NAV_BEGIN + "\n"
        '          <li class="nav-group nav-group--mega">\n'
        '            <button type="button" class="nav-group__trigger"'
        ' aria-expanded="false" aria-controls="nav-cop31">COP31</button>\n'
        '            <div class="nav-group__menu nav-group__menu--mega" id="nav-cop31">\n'
        '              <div class="nav-mega">' + columns + "\n"
        "              </div>\n"
        "            </div>\n"
        "          </li>\n"
        "          " + NAV_END + "\n"
    )


def footer_block():
    items = "".join(
        '\n          <li><a href="%s">%s</a></li>' % (href, label)
        for href, label in [PLAN[0]] + PLAN[1:5] + SERVICES[:4] + [URGENT[0]]
    )
    return (
        '        <div class="site-footer__col">\n'
        '          <h2 class="site-footer__heading">COP31 Antalya</h2>\n'
        "          <ul>%s\n"
        "          </ul>\n"
        "        </div>\n" % items
    )


def strip_nav(html):
    """Remove a previously injected nav block, marked or legacy.

    Lets the block be replaced when its markup changes, rather than merely
    skipped because some form of it is already present.
    """
    if NAV_BEGIN in html and NAV_END in html:
        return re.sub(
            r"[ \t]*" + re.escape(NAV_BEGIN) + r".*?" + re.escape(NAV_END) + r"\n",
            "",
            html,
            flags=re.S,
        )
    return LEGACY_NAV.sub("", html)


def patch(path, nav, footer):
    with open(path, encoding="utf-8") as handle:
        original = handle.read()
    if NAV_ANCHOR not in original or FOOTER_ANCHOR not in original:
        raise SystemExit("Unexpected chrome in %s — anchors not found" % path)

    html = strip_nav(original).replace(NAV_ANCHOR, nav + NAV_ANCHOR, 1)
    if 'site-footer__heading">COP31 Antalya' not in html:
        html = html.replace(FOOTER_ANCHOR, footer + FOOTER_ANCHOR, 1)

    if html == original:
        return False
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(html)
    return True


def main():
    nav = nav_block()
    footer = footer_block()
    changed = 0
    total = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "**", "*.html"), recursive=True)):
        if os.sep + ".git" + os.sep in path:
            continue
        total += 1
        if patch(path, nav, footer):
            changed += 1
    print("patched %d of %d HTML files" % (changed, total))


if __name__ == "__main__":
    main()
