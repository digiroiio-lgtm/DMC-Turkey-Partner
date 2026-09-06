#!/usr/bin/env python3
"""Generate the COP31 cluster pages.

Usage: python3 tools/cop31_build.py
Writes <slug>/index.html for every page defined in the cop31_pages_* modules.
Re-running is safe: files are overwritten from the content definitions.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_render import ROOT, render  # noqa: E402


def collect():
    """Load every cop31_pages_*.py module in tools/ and concatenate its PAGES."""
    import glob
    import importlib

    here = os.path.dirname(os.path.abspath(__file__))
    pages = []
    for path in sorted(glob.glob(os.path.join(here, "cop31_pages_*.py"))):
        module = importlib.import_module(os.path.basename(path)[:-3])
        pages.extend(module.PAGES)
    return pages


def main():
    pages = collect()
    slugs = [p["slug"] for p in pages]
    duplicates = {s for s in slugs if slugs.count(s) > 1}
    if duplicates:
        raise SystemExit("Duplicate slugs: %s" % ", ".join(sorted(duplicates)))

    for page in pages:
        directory = os.path.join(ROOT, page["slug"])
        os.makedirs(directory, exist_ok=True)
        path = os.path.join(directory, "index.html")
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(render(page) + "\n")
        print("wrote %s/index.html" % page["slug"])
    print("%d COP31 pages generated" % len(pages))

    # Generated pages inherit their chrome from the reference page, which
    # already carries the COP31 nav. Running the patcher anyway keeps the whole
    # site convergent whatever order the two scripts are run in.
    import cop31_nav

    cop31_nav.main()


if __name__ == "__main__":
    main()
