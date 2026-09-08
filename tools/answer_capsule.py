#!/usr/bin/env python3
"""Put each page's direct answer immediately under its <h1>.

The COP31 generator has done this since it was built — tools/cop31_render.py
calls it "a short extractable answer directly under the H1, for AI/AEO
surfaces" — and it renders on 30 pages. Nothing else on the site had one, so
elsewhere the first thing a reader or an extractive engine met was a marketing
lede written to persuade rather than to answer.

The text comes from tools/answer_data.py, hand-written per URL. It cannot be
derived the way schema is: the whole point is to say something the page does
not already say in that form, so there is no source to derive it from. A page
with no entry gets no capsule.

Pages that carry one also get schema.org/speakable pointing at the capsule and
the <h1>, which is the part of the page worth reading aloud.

Usage: python3 tools/answer_capsule.py [--dry-run]
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import managed_blocks as mb  # noqa: E402
import page_model as pm  # noqa: E402
from answer_data import ANSWERS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FENCE = "answer-capsule"

# The COP31 pages render their own capsule through the generator. Injecting a
# second one here would put two answers under one heading.
SKIP_FAMILIES = {"cop31", "cop31_news", "cop31_news_hub"}


def esc(text):
    """Escape for a text node, idempotently."""
    return re.sub(
        r"&(?!(?:[A-Za-z][A-Za-z0-9]{1,31}|#\d{1,7}|#[xX][0-9A-Fa-f]{1,6});)",
        "&amp;",
        text,
    ).replace("<", "&lt;").replace(">", "&gt;")


def render(answer):
    return "\n".join(
        [
            "      " + mb.begin(FENCE),
            '      <p class="answer-capsule">%s</p>' % esc(answer),
            "      " + mb.end(FENCE),
        ]
    )


def main():
    dry_run = "--dry-run" in sys.argv
    changed = skipped = 0

    for path in mb.iter_pages(ROOT):
        page = pm.read(path, ROOT)
        answer = ANSWERS.get(page["url"])
        if not answer or page["noindex"] or page["family"] in SKIP_FAMILIES:
            # Same reason as page_schema: clear a block this patcher no longer
            # owns, so removing an entry from ANSWERS actually removes the
            # capsule from the page.
            if not dry_run:
                mb.write_if_changed(path, page["html"], mb.strip(page["html"], FENCE))
            continue

        original = page["html"]
        stripped = mb.strip(original, FENCE)
        if "</h1>" not in stripped:
            skipped += 1
            continue
        html = mb.insert(stripped, FENCE, render(answer), path)

        if dry_run:
            if html != original:
                changed += 1
                print("would change %s" % page["rel"])
            continue
        if mb.write_if_changed(path, original, html):
            changed += 1

    print(
        "answer capsules: %d of %d pages changed (%d COP31 pages render their own)"
        % (changed, len(ANSWERS), 30)
    )
    if skipped:
        print("  %d pages had no </h1> to anchor to" % skipped)


if __name__ == "__main__":
    main()
