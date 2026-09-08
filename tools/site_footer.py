#!/usr/bin/env python3
"""Normalise the footer: real headings, and reachable contact details.

Two problems, both site-wide because the footer is duplicated into every file.

1. The five footer nav column labels were <h2>. Every page therefore carried
   five headings that say nothing about its content, sitting at the same level
   as its real sections. They look like structure to anything reading the
   outline — an accessibility tree, an AI summariser, a heading-based extractor
   — and on the thinner pages they outnumbered the genuine H2s. They are
   labels, so they become <p>; .site-footer__heading is styled by class, so
   nothing moves visually.

2. The footer carried no way to contact anyone. The email appears in body copy
   on many pages and the WhatsApp number on the COP31 pages, but neither was in
   the footer, and the phone number was never a tel: link anywhere on the site
   despite being published on 36 pages. A service-area business with no address
   has its contact details as its main local signal, so they belong on every
   page, in markup a parser can read.

Usage: python3 tools/site_footer.py [--dry-run]
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import site_config as cfg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

HEADING = re.compile(r'<h2 class="site-footer__heading">(.*?)</h2>')
CONTACT_BEGIN = "<!-- footer-contact:begin -->"
CONTACT_END = "<!-- footer-contact:end -->"

# Anchored to the end of the brand column's standfirst, so the contact block
# sits under the description rather than after the call-to-action button.
BRAND_ANCHOR = '          <a class="btn btn--primary" href="/request-proposal/">Request a Proposal</a>'


def pretty_phone(number):
    """+905353998999 -> +90 535 399 89 99"""
    digits = number.lstrip("+")
    if not digits.startswith("90") or len(digits) != 12:
        return number
    return "+90 %s %s %s %s" % (digits[2:5], digits[5:8], digits[8:10], digits[10:])


def contact_block():
    lines = [
        "          " + CONTACT_BEGIN,
        '          <address class="site-footer__contact">',
        '            <a href="mailto:%s">%s</a>' % (cfg.ORG_EMAIL, cfg.ORG_EMAIL),
    ]
    if cfg.ORG_TELEPHONE:
        lines.append(
            '            <a href="tel:%s">%s</a>'
            % (cfg.ORG_TELEPHONE, pretty_phone(cfg.ORG_TELEPHONE))
        )
    lines.append("          </address>")
    lines.append("          " + CONTACT_END)
    return "\n".join(lines) + "\n"


def patch(path, dry_run=False):
    with open(path, encoding="utf-8") as handle:
        original = handle.read()

    html = HEADING.sub(r'<p class="site-footer__heading">\1</p>', original)

    # Indentation goes with the block; see managed_blocks.strip for why
    # leaving it behind walks the next line right on every re-run.
    html = re.sub(
        r"[ \t]*" + re.escape(CONTACT_BEGIN) + r".*?" + re.escape(CONTACT_END) + r"\n?",
        "",
        html,
        flags=re.S,
    )
    if BRAND_ANCHOR in html:
        html = html.replace(BRAND_ANCHOR, contact_block() + BRAND_ANCHOR, 1)

    if dry_run:
        return html != original
    return mb.write_if_changed(path, original, html)


def main():
    dry_run = "--dry-run" in sys.argv
    changed = total = 0
    for path in mb.iter_pages(ROOT):
        total += 1
        if patch(path, dry_run):
            changed += 1
            if dry_run:
                print("would change %s" % os.path.relpath(path, ROOT))
    print("footer: %d of %d pages changed" % (changed, total))


if __name__ == "__main__":
    main()
