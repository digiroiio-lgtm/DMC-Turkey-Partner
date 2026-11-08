"""Canonical labels for every URL in the COP31 cluster.

Used so internal links and the mega menu stay in sync with one source of truth.
"""

HUB = "/cop31-antalya/"

PLAN = [
    ("/cop31-antalya/", "COP31 Antalya 2026"),
    ("/cop31-news/", "News &amp; Latest Updates"),
    ("/cop31-antalya-participant-guide/", "Participant Guide"),
    ("/cop31-antalya-dates/", "Dates &amp; Programme"),
    ("/cop31-antalya-program/", "Conference Programme"),
    ("/cop31-antalya-venue/", "Venue &amp; Location"),
    ("/cop31-antalya-expo-center/", "Antalya EXPO Center"),
    ("/cop31-antalya-registration/", "Registration"),
    ("/cop31-antalya-hotels/", "Hotels"),
    ("/cop31-antalya-accommodation/", "Group Accommodation"),
    ("/cop31-antalya-transport/", "Transport"),
    ("/cop31-antalya-restaurants/", "Restaurants &amp; Dining"),
]

SERVICES = [
    ("/cop31-event-services/", "Event Services"),
    ("/cop31-exhibition-services/", "Exhibition Services"),
    ("/cop31-exhibition-stands/", "Exhibition Stands"),
    ("/cop31-booth-builder-antalya/", "Booth Builder"),
    ("/cop31-pavilion-services/", "Pavilion Services"),
    ("/cop31-event-production/", "Event Production"),
    ("/cop31-printing-services/", "Printing &amp; Collateral"),
    ("/cop31-branding-signage/", "Branding &amp; Signage"),
    ("/cop31-av-equipment-rental/", "AV &amp; Equipment Rental"),
    ("/cop31-furniture-rental/", "Furniture Rental"),
    ("/cop31-coffee-machine-rental/", "Coffee &amp; Hospitality"),
    ("/cop31-event-staff/", "Event Staff"),
    ("/cop31-hostess-staff/", "Hostesses"),
    ("/cop31-interpreters/", "Interpreters"),
    ("/cop31-private-transfers/", "Private Transfers"),
    ("/cop31-antalya-airport-transfer/", "Airport Transfers"),
]

URGENT = [
    ("/cop31-last-minute-services/", "Last-Minute Services"),
]

# Labels stay defined for merged pages so older page modules still import;
# menus below only list pages that still exist (see cop31_merge_map.py).
LABEL = dict(PLAN + SERVICES + URGENT)

from cop31_merge_map import MERGED_TO  # noqa: E402


def _live(items):
    return [(href, label) for href, label in items if href.strip("/") not in MERGED_TO]


PLAN = _live(PLAN)
SERVICES = _live(SERVICES)
ALL = PLAN + SERVICES + URGENT


def _href(path):
    slug = path.strip("/")
    if slug in MERGED_TO:
        return "/%s/#%s" % (MERGED_TO[slug], slug)
    return path


def L(*paths):
    """Build a list of (href, label) pairs for the given cluster paths."""
    out, seen = [], set()
    for p in paths:
        page = _href(p).split("#")[0]
        if page not in seen:
            seen.add(page)
            out.append((_href(p), LABEL[p]))
    return out


def A(path, text=None):
    """Inline anchor to a cluster page."""
    return '<a href="%s">%s</a>' % (_href(path), text or LABEL[path])
