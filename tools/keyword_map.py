#!/usr/bin/env python3
"""One primary keyword = one page.

NightWatch tracks these keywords (UK + US). Each has exactly one page that owns
it: the only page whose <title> starts with the keyword. Other pages may
mention it, but should link to the owner rather than compete with it.

Usage:
    python3 tools/keyword_map.py   # non-zero exit if another page's title leads with an owned keyword
"""

import glob
import html
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OWNER = {
    "dmc turkey": "dmc-turkey/",
    "dmc antalya": "destinations/antalya/",
    "dmc istanbul": "destinations/istanbul/",
    "dmc bodrum": "destinations/bodrum/",
    "dmc cappadocia": "destinations/cappadocia/",
    "mice turkey": "mice-turkey/",
    "incentive travel turkey": "incentive-travel-turkey/",
    "corporate event management turkey": "corporate-events-turkey/",
    "event production turkey": "services/event-production/",
    "group travel turkey": "group-travel-turkey/",
    "white label dmc turkey": "white-label-dmc-turkey/",
}


def title(path):
    with open(path, encoding="utf-8") as handle:
        m = re.search(r"<title>(.*?)</title>", handle.read(), re.S)
    return html.unescape(m.group(1)).strip().lower() if m else ""


def main():
    problems = []
    pages = glob.glob(os.path.join(ROOT, "**", "index.html"), recursive=True)
    for path in pages:
        rel = os.path.relpath(os.path.dirname(path), ROOT)
        rel = "" if rel == "." else rel + "/"
        lead = re.split(r"\s[|:–—-]\s", title(path))[0]
        for keyword, owner in OWNER.items():
            if lead == keyword and rel != owner:
                problems.append("%s: title leads with %r, owned by /%s" % (rel or "/", keyword, owner))
    for keyword, owner in OWNER.items():
        if not os.path.exists(os.path.join(ROOT, owner, "index.html")):
            problems.append("owner page missing for %r: /%s" % (keyword, owner))
    for p in problems:
        print(p)
    print("%d keyword conflicts" % len(problems))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
