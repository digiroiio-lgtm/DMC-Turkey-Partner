# -*- coding: utf-8 -*-
"""Off-season (off-peak dates) content: the single source for
/off-season-events-turkey/, /off-season-events-turkey/belek/ and the
destination pop-up data block in assets/js/main.js.

Saving claim rule
-----------------
A percentage saving may be published only when it is backed by real,
like-for-like quote comparisons (same hotel category, scope, group size and
nights; one off-peak quote and one peak-season quote). Add those to
QUOTE_COMPARISONS. While the list is empty, saving_percent() returns None and
every page, and the pop-up, uses the percentage-free opportunity message.
No saving is ever derived from the published event-costs reference ranges.
"""

SEASON_LABEL = "Winter 2026/27"
UPDATED_ISO = "2026-10-09"
UPDATED_LABEL = "October 2026"

# Real comparisons, one dict each, e.g.:
# {"destination": "Belek", "scope": "4-night incentive, 5-star AI resort, 100 pax",
#  "offpeak_dates": "Jan 2027", "peak_dates": "May 2026",
#  "offpeak_total": 0, "peak_total": 0, "valid_until": "2026-12-31"}
QUOTE_COMPARISONS = []


def saving_percent():
    """Largest like-for-like saving, rounded down to the nearest 5 — or None."""
    values = []
    for q in QUOTE_COMPARISONS:
        if q.get("peak_total") and q.get("offpeak_total") and q["offpeak_total"] < q["peak_total"]:
            values.append(100.0 * (1 - q["offpeak_total"] / q["peak_total"]))
    if not values:
        return None
    return int(max(values) // 5 * 5) or None


# Windows come from the site owner. `page` is None until a destination page exists.
DESTINATIONS = [
    {
        "slug": "belek", "name": "Belek", "window": "December – February",
        "events": "Dealer and sales meetings, retreats, training programmes, golf incentives",
        "scope": "Resort-based: conference wings inside all-inclusive resorts, packaged rates",
        "page": "/off-season-events-turkey/belek/",
    },
    {
        "slug": "antalya", "name": "Antalya", "window": "December – February",
        "events": "Conferences, corporate events, city and resort incentives",
        "scope": "City and coast: city hotels, venues such as the EXPO Center, transfers",
        "page": "/off-season-events-turkey/antalya/",
    },
    {
        "slug": "istanbul", "name": "Istanbul", "window": "January – February and July – August",
        "events": "Meetings, conferences, corporate events, premium group programmes",
        "scope": "City: business hotels, city venues, short-stay programmes",
        "page": "/off-season-events-turkey/istanbul/",
    },
    {
        "slug": "cappadocia", "name": "Cappadocia", "window": "December – February (excluding New Year week)",
        "events": "Incentives, executive groups, destination experiences",
        "scope": "Boutique and cave-hotel stays, activity-led programmes",
        "page": None,
    },
    {
        "slug": "bodrum", "name": "Bodrum", "window": "October – April",
        "events": "Premium incentives, private groups, corporate hospitality",
        "scope": "Coastal: depends on which hotels stay open",
        "page": None,
    },
]

HUB = "/off-season-events-turkey/"
COMPARE_ANCHOR = "#compare"


def popup_link(slug):
    """Primary pop-up destination: the destination's own page, otherwise the
    hub with the destination preselected in the compare form."""
    for d in DESTINATIONS:
        if d["slug"] == slug and d["page"]:
            return d["page"]
    name = next(d["name"] for d in DESTINATIONS if d["slug"] == slug)
    return HUB + "?destination=" + name + COMPARE_ANCHOR
