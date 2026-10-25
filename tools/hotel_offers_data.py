# -*- coding: utf-8 -*-
"""Group hotel offer windows: the single source for /group-hotel-offers-turkey/
and its area and hotel pages (built by tools/hotel_offers_build.py).

Rules
-----
* No prices, discounts or percentages are published here. Pages say "request
  rates"; rate validity and availability are confirmed per request.
* Only confirmed facts go into HOTELS. `area` is flagged `area_confirmed=False`
  until the site owner confirms it. Optional fact fields (stars, rooms, meeting
  capacity) stay empty until supplied; the build skips empty fields.
* Windows are listed exactly as supplied by the site owner (2026).
"""

import datetime as dt

HUB = "/group-hotel-offers-turkey/"
SEASON_LABEL = "Oct – Dec 2026"
UPDATED_ISO = "2026-10-25"
UPDATED_LABEL = "October 2026"

# COP31 Antalya (9–20 November 2026): used only to flag windows that overlap it.
COP31_START = dt.date(2026, 11, 9)
COP31_END = dt.date(2026, 11, 20)

AREAS = {
    "lara": {"name": "Lara", "slug": "lara",
             "blurb": "Antalya's city-side resort coast, close to Antalya Airport."},
    "belek": {"name": "Belek", "slug": "belek",
              "blurb": "Turkey's resort-based meetings district, 30–45 minutes from Antalya Airport."},
}

# slug, display name, area key, area_confirmed, optional verified facts
HOTELS = [
    {"slug": "trendy-lara", "name": "Trendy Lara", "area": "lara", "area_confirmed": True},
    {"slug": "adalya-elit", "name": "Adalya Elit", "area": "lara", "area_confirmed": False},
    {"slug": "adam-eve-belek", "name": "Adam & Eve Belek", "area": "belek", "area_confirmed": True},
    {"slug": "titanic-deluxe-lara", "name": "Titanic Deluxe Lara", "area": "lara", "area_confirmed": True},
    {"slug": "ducale-lara", "name": "Ducale Lara", "area": "lara", "area_confirmed": True},
    {"slug": "voyage-lara", "name": "Voyage Lara", "area": "lara", "area_confirmed": True},
    {"slug": "voyage-belek", "name": "Voyage Belek", "area": "belek", "area_confirmed": True},
    {"slug": "mardan-palace", "name": "Mardan Palace", "area": "lara", "area_confirmed": False,
     "alt": "Titanic Mardan Palace"},
    {"slug": "titanic-deluxe-belek", "name": "Titanic Deluxe Belek", "area": "belek", "area_confirmed": True},
]

# (hotel slug, start, end), in start-date order, as supplied.
WINDOWS = [
    ("trendy-lara", "2026-10-29", "2026-11-01"),
    ("adalya-elit", "2026-11-04", "2026-11-08"),
    ("adam-eve-belek", "2026-11-06", "2026-11-16"),
    ("titanic-deluxe-lara", "2026-11-15", "2026-11-19"),
    ("adalya-elit", "2026-11-20", "2026-11-24"),
    ("ducale-lara", "2026-11-22", "2026-11-26"),
    ("ducale-lara", "2026-11-30", "2026-12-04"),
    ("voyage-lara", "2026-12-03", "2026-12-09"),
    ("voyage-belek", "2026-12-03", "2026-12-07"),
    ("mardan-palace", "2026-12-04", "2026-12-07"),
    ("titanic-deluxe-belek", "2026-12-07", "2026-12-09"),
    ("trendy-lara", "2026-12-16", "2026-12-19"),
    ("titanic-deluxe-belek", "2026-12-20", "2026-12-24"),
]

MONTHS = ["", "January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]
MON3 = [m[:3] for m in MONTHS]


def hotel(slug):
    return next(h for h in HOTELS if h["slug"] == slug)


def windows(today=None):
    """All windows with computed fields. `today` is a date (build date)."""
    today = today or dt.date.today()
    out = []
    for n, (slug, s, e) in enumerate(WINDOWS, 1):
        start, end = dt.date.fromisoformat(s), dt.date.fromisoformat(e)
        if end < today:
            status, days = "closed", None
        elif start <= today:
            status, days = "open", 0
        else:
            status, days = "upcoming", (start - today).days
        h = hotel(slug)
        out.append({
            "n": n, "hotel": h, "start": start, "end": end, "nights": (end - start).days,
            "status": status, "days_until": days,
            "cop31": start <= COP31_END and end >= COP31_START,
            "label": date_range(start, end),
        })
    return out


def date_range(start, end, year=True):
    if start.month == end.month:
        text = "%d–%d %s" % (start.day, end.day, MONTHS[start.month])
    else:
        text = "%d %s – %d %s" % (start.day, MONTHS[start.month], end.day, MONTHS[end.month])
    return text + (" %d" % end.year if year else "")


def short_range(start, end):
    if start.month == end.month:
        return "%d–%d %s" % (start.day, end.day, MON3[start.month])
    return "%d %s – %d %s" % (start.day, MON3[start.month], end.day, MON3[end.month])
