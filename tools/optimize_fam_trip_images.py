#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert source photos to the WebP pairs used on /agency-fam-trip-2027/.

Usage: python3 tools/optimize_fam_trip_images.py SOURCE.png [SOURCE2.png ...]

For each source writes assets/img/fam-trip/<name>.webp (full size, max 1600 px wide for the hero,
otherwise 1200 px) and <name>-640.webp (640 px wide), RGB, no metadata, quality 80. Idempotent.
Point campaign/fam-trip-images.json at the result (src without the extension, with the printed
width/height of the full-size file).
"""

import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "fam-trip")


def convert(path):
    name = os.path.splitext(os.path.basename(path))[0]
    full_width = 1600 if "hero" in name else 1200
    with Image.open(path) as source:
        image = source.convert("RGB")
    os.makedirs(OUT, exist_ok=True)
    for suffix, width in (("", full_width), ("-640", 640)):
        target = image if image.width <= width else image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)
        out = os.path.join(OUT, "%s%s.webp" % (name, suffix))
        target.save(out, "WEBP", quality=80, method=6)
        print("%s  %dx%d  %d KB" % (os.path.relpath(out, ROOT), target.width, target.height, os.path.getsize(out) // 1024))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    for source in sys.argv[1:]:
        convert(source)
