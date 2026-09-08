# -*- coding: utf-8 -*-
"""Fenced regions of generated markup inside otherwise hand-written pages.

Most of this site is hand-authored HTML. A handful of things have to be
identical across all 137 pages, so scripts inject them. Each such script owns
one fence:

    <!-- page-schema:begin -->  ...generated...  <!-- page-schema:end -->

and rewrites only between its own markers. That is what makes re-running a
patcher a no-op instead of an append.

Two rules this module exists to enforce:

1. **Deterministic placement.** site_seo.py originally did
   `html.replace("</head>", block + "</head>", 1)`. With one patcher that is
   fine. With three, whichever ran last ends up nearest `</head>`, so the
   output bytes depend on run order and re-running in a different order
   produces a diff for no reason. Each fence declares an anchor instead, so a
   block always lands in the same place.

2. **Nothing scans across a fence.** site_seo.drop_legacy_entity_nodes()
   sweeps the whole document deleting JSON-LD by @type. Today it spares the
   page-schema block only because that block happens to be a @graph with no
   top-level @type — luck, not design. outside_fences() gives a patcher the
   unmanaged spans only, so it structurally cannot delete another patcher's
   output.
"""

import glob
import json
import os
import re

# Anchors are tried in order; the first one found wins. Placing page-schema
# above the identity fence keeps the per-page graph and the site graph
# adjacent and in a stable order regardless of which patcher ran first.
FENCES = {
    "head-meta": ("</head>",),
    "page-schema": ("<!-- site-identity:begin -->", "</head>"),
    "site-identity": ("</head>",),
    "answer-capsule": ("</h1>",),
}


def begin(name):
    return "<!-- %s:begin -->" % name


def end(name):
    return "<!-- %s:end -->" % name


def strip(html, name):
    """Remove a fence and its contents, so the patcher can re-emit it.

    The indentation on the opening marker's line is consumed too. Without
    that, a block rendered with indentation leaves its own leading spaces
    behind on every strip, and re-running the patcher walks the following line
    further right each time — silently, since the page still renders.
    """
    return re.sub(
        r"[ \t]*" + re.escape(begin(name)) + r".*?" + re.escape(end(name)) + r"\n?",
        "",
        html,
        flags=re.S,
    )


def spans(html):
    """(start, end) of every fenced region present, in document order."""
    found = []
    for name in FENCES:
        for match in re.finditer(
            re.escape(begin(name)) + r".*?" + re.escape(end(name)), html, re.S
        ):
            found.append(match.span())
    return sorted(found)


def outside_fences(html):
    """(start, end) of the regions no patcher owns.

    Anything that removes or rewrites nodes must restrict itself to these, or
    it will eventually eat another patcher's block.
    """
    cursor, regions = 0, []
    for start, stop in spans(html):
        if start > cursor:
            regions.append((cursor, start))
        cursor = stop
    if cursor < len(html):
        regions.append((cursor, len(html)))
    return regions


def insert(html, name, block, path="<unknown>"):
    """Place a rendered block at its fence's first available anchor."""
    for anchor in FENCES[name]:
        if anchor in html:
            if anchor == "</h1>":  # body fence: after the anchor, not before
                return html.replace(anchor, anchor + "\n" + block, 1)
            return html.replace(anchor, block + anchor, 1)
    raise SystemExit(
        "No anchor for fence %r in %s (tried %s)" % (name, path, ", ".join(FENCES[name]))
    )


def iter_pages(root, pattern="**/*.html"):
    for path in sorted(glob.glob(os.path.join(root, pattern), recursive=True)):
        if os.sep + ".git" + os.sep in path:
            continue
        yield path


LD = re.compile(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', re.S)


def write_if_changed(path, original, updated):
    """Write only on a real change, and only if the result is still sane.

    These asserts are cheap and catch essentially every way a patcher can
    corrupt a hand-written page. A patcher raises here rather than writing
    something broken.
    """
    if updated == original:
        return False

    for tag in ("</head>", "<main", "</html>", "<h1"):
        if updated.count(tag) != original.count(tag):
            raise SystemExit(
                "%s: %r count changed %d -> %d; refusing to write"
                % (path, tag, original.count(tag), updated.count(tag))
            )

    if "&amp;amp;" in updated and "&amp;amp;" not in original:
        raise SystemExit("%s: introduced a double-escaped entity" % path)

    for raw in LD.findall(updated):
        try:
            json.loads(raw)
        except ValueError as exc:
            raise SystemExit("%s: produced invalid JSON-LD: %s" % (path, exc))

    with open(path, "w", encoding="utf-8") as handle:
        handle.write(updated)
    return True
