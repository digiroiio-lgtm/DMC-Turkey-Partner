# -*- coding: utf-8 -*-
"""Antalya transfer prices — the single source of truth.

Every transfer price on the site is rendered from this file: the
/antalya-transfer-prices/ page and the price blocks on the COP31 transfer
pages, /event-costs/ and /services/transportation-logistics/. Change a figure
here, then run `python3 tools/transfer_prices_build.py`.

Prices are indicative, in EUR, per vehicle (never per person), excluding
applicable taxes. None means the service is quoted on request.
"""

CURRENCY = "EUR"

# Date the figures below were last reviewed. Change it only after a review.
PRICES_REVIEWED = "2026-10-09"
PRICES_REVIEWED_LABEL = "9 October 2026"

# Airport transfer: one way. Daily shuttle: one outbound + one return.
# Full day: vehicle and driver dedicated for the programme day.
VEHICLES = [
    {
        "key": "sedan", "label": "Sedan", "capacity": "up to 3 passengers", "max_pax": 3,
        "airport": 70, "shuttle": None, "full_day": None,
        "extra_hour": 20, "extra_km": 1.00,
    },
    {
        "key": "van", "label": "Van", "capacity": "up to 6 passengers", "max_pax": 6,
        "airport": 90, "shuttle": None, "full_day": None,
        "extra_hour": 20, "extra_km": 1.00,
    },
    {
        "key": "minibus", "label": "Minibus", "capacity": "up to 19 passengers", "max_pax": 19,
        "airport": 160, "shuttle": 260, "full_day": 380,
        "extra_hour": 25, "extra_km": 1.00,
    },
    {
        "key": "midibus", "label": "Midibus", "capacity": "up to 27 passengers", "max_pax": 27,
        "airport": 240, "shuttle": 330, "full_day": 480,
        "extra_hour": 30, "extra_km": 1.20,
    },
    {
        "key": "coach", "label": "Coach", "capacity": "up to 50 passengers*", "max_pax": 50,
        "airport": 320, "shuttle": 450, "full_day": 650,
        "extra_hour": 40, "extra_km": 1.50,
    },
]

# Extra-charge rows: sedan and van share one rate.
EXTRA_GROUPS = [
    ("Sedan / van", ("sedan", "van")),
    ("Minibus", ("minibus",)),
    ("Midibus", ("midibus",)),
    ("Coach", ("coach",)),
]

SERVICES = [
    {
        "key": "airport",
        "label": "Airport transfer",
        "column": "Airport transfer, one way",
        "unit": "per vehicle, one way",
        "inclusion": (
            "One way, one drop-off point, up to 35 km; meet &amp; greet and up to 60 "
            "minutes' waiting after landing."
        ),
    },
    {
        "key": "shuttle",
        "label": "Daily shuttle",
        "column": "Daily shuttle, out and back",
        "unit": "per vehicle, per day",
        "inclusion": (
            "One outbound and one return run; 100 km and 4 active working hours in total. "
            "The vehicle does not wait between runs."
        ),
    },
    {
        "key": "full_day",
        "label": "Full-day vehicle with driver",
        "column": "Full-day vehicle with driver",
        "unit": "per vehicle, per day",
        "inclusion": (
            "10 consecutive working hours and 150 km; the vehicle is dedicated to your "
            "programme for the whole day."
        ),
    },
]

CAPACITY_NOTE = (
    "*Final capacity is confirmed against luggage and any seat needed for a coordinator."
)

ALTERNATIVES_NOTE = (
    "The daily shuttle and the full-day vehicle are alternatives for the same day; "
    "they are not charged together."
)

EXTRA_HOURS_NOTE = (
    "Sedan and van hourly rates apply to extra airport waiting time. For other vehicles, "
    "the hourly rate applies once the time included in the service is exceeded."
)

DISCLAIMER = (
    "Indicative prices per vehicle in EUR, excluding applicable taxes. Final pricing "
    "depends on confirmed routes, dates, luggage requirements and vehicle availability."
)


def vehicle(key):
    return next(v for v in VEHICLES if v["key"] == key)


def lowest(service_key):
    """Lowest published price for a service, for 'from €…' summaries."""
    return min(v[service_key] for v in VEHICLES if v[service_key] is not None)
