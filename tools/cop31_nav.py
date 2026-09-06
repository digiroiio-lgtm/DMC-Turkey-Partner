#!/usr/bin/env python3
"""Insert the COP31 mega menu and footer column into every page on the site.

The site has no build step, so global chrome lives duplicated in each
index.html. This script performs that edit idempotently: running it twice is a
no-op, and re-running it after a nav change updates every page.

Usage: python3 tools/cop31_nav.py
"""

import glob
import os
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


def _menu_column(title, links, first=False):
    items = "".join(
        '\n                  <li%s><a href="%s">%s</a></li>'
        % (' class="nav-mega__feature"' if first and idx == 0 else "", href, label)
        for idx, (href, label) in enumerate(links)
    )
    return (
        '\n                <div class="nav-mega__col">'
        '\n                  <p class="nav-mega__heading">%s</p>'
        "\n                  <ul>%s"
        "\n                  </ul>"
        "\n                </div>" % (title, items)
    )


def nav_block():
    return (
        '          <li class="nav-group nav-group--mega">\n'
        '            <button type="button" class="nav-group__trigger" aria-expanded="false"'
        ' aria-controls="nav-cop31">COP31</button>\n'
        '            <div class="nav-group__menu nav-group__menu--mega" id="nav-cop31">\n'
        '              <div class="nav-mega">%s%s%s\n'
        "              </div>\n"
        "            </div>\n"
        "          </li>\n"
        % (
            _menu_column("Plan Your COP31", PLAN, first=True),
            _menu_column("Local Services", SERVICES),
            _menu_column("Urgent Support", URGENT),
        )
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


def patch(path, nav, footer):
    with open(path, encoding="utf-8") as handle:
        html = handle.read()
    if MARKER in html:
        return False
    if NAV_ANCHOR not in html or FOOTER_ANCHOR not in html:
        raise SystemExit("Unexpected chrome in %s — anchors not found" % path)
    html = html.replace(NAV_ANCHOR, nav + NAV_ANCHOR, 1)
    html = html.replace(FOOTER_ANCHOR, footer + FOOTER_ANCHOR, 1)
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
