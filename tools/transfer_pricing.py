# -*- coding: utf-8 -*-
"""HTML fragments for Antalya transfer prices, rendered from transfer_prices.py.

Every page that shows a transfer price uses these functions, so a figure
changed in transfer_prices.py changes everywhere at once. Hand-written pages
carry the output between `<!-- transfer-prices:NAME:begin/end -->` markers,
which transfer_prices_build.py refreshes.
"""

from cop31_render import table
from transfer_prices import (
    ALTERNATIVES_NOTE,
    CAPACITY_NOTE,
    DISCLAIMER,
    EXTRA_GROUPS,
    EXTRA_HOURS_NOTE,
    SERVICES,
    VEHICLES,
    lowest,
    vehicle,
)

PAGE = "/antalya-transfer-prices/"
ON_REQUEST = "On request"


def eur(amount):
    if amount is None:
        return ON_REQUEST
    if float(amount).is_integer():
        return "€%d" % amount
    return "€%.2f" % amount


def _service(key):
    return next(s for s in SERVICES if s["key"] == key)


def _vehicle_cell(v):
    return "%s, %s" % (v["label"], v["capacity"])


def _note(text):
    return '<p class="price-note">%s</p>' % text


def _link(text="See all Antalya transfer prices"):
    return '<a href="%s">%s</a>' % (PAGE, text)


# --- tables ------------------------------------------------------------------

def main_table():
    return table(
        "Antalya transfer prices per vehicle (EUR)",
        ["Vehicle and capacity"] + [s["column"] for s in SERVICES],
        [[_vehicle_cell(v)] + [eur(v[s["key"]]) for s in SERVICES] for v in VEHICLES],
    ) + _note(CAPACITY_NOTE)


def inclusions_table(keys=None):
    services = [_service(k) for k in keys] if keys else SERVICES
    return table(
        "What each price includes",
        ["Service", "Included in the price"],
        [[s["label"], s["inclusion"]] for s in services],
    )


def extras_table():
    rows = []
    for label, keys in EXTRA_GROUPS:
        v = vehicle(keys[0])
        rows.append([label, eur(v["extra_hour"]), eur(v["extra_km"])])
    return table(
        "Extra charges per vehicle (EUR)",
        ["Vehicle", "Extra waiting / working hour", "Extra kilometre"],
        rows,
    ) + _note(EXTRA_HOURS_NOTE)


def airport_table():
    s = _service("airport")
    return table(
        "Antalya airport transfer prices per vehicle (EUR)",
        ["Vehicle and capacity", s["column"]],
        [[_vehicle_cell(v), eur(v["airport"])] for v in VEHICLES],
    ) + _note(CAPACITY_NOTE)


def shuttle_full_day_table():
    keys = ("shuttle", "full_day")
    return table(
        "Antalya daily shuttle and full-day vehicle prices (EUR)",
        ["Vehicle and capacity"] + [_service(k)["column"] for k in keys],
        [[_vehicle_cell(v)] + [eur(v[k]) for k in keys] for v in VEHICLES],
    ) + _note(CAPACITY_NOTE)


def disclaimer():
    return _note(DISCLAIMER)


# --- marker blocks for existing pages -----------------------------------------

def _section(heading, *parts):
    body = "\n      ".join(p for p in parts if p)
    return (
        '<section class="page-section transfer-prices">\n'
        "      <h2>%s</h2>\n"
        "      %s\n"
        "    </section>" % (heading, body)
    )


def _airport_block():
    airport = vehicle("sedan")
    return _section(
        "Airport Transfer Prices",
        '<p class="page-section__lede">Indicative one-way prices per vehicle between '
        "Antalya Airport and your hotel or venue.</p>",
        airport_table(),
        "<p><strong>Included:</strong> %s Extra waiting for a sedan or van is %s per "
        "hour.</p>" % (_service("airport")["inclusion"], eur(airport["extra_hour"])),
        disclaimer(),
        "<p>%s — including daily shuttles, full-day vehicles and extra charges.</p>" % _link(),
    )


def _shuttle_block():
    return _section(
        "Daily Shuttle and Vehicle-with-Driver Prices",
        '<p class="page-section__lede">Indicative prices per vehicle for a daily '
        "hotel–venue shuttle, or a vehicle and driver dedicated to you for the day.</p>",
        shuttle_full_day_table(),
        inclusions_table(("shuttle", "full_day")),
        _note(ALTERNATIVES_NOTE),
        extras_table(),
        disclaimer(),
        "<p>%s — including airport transfers.</p>" % _link(),
    )


def _summary():
    return (
        "Airport transfers from %s, daily shuttles from %s and a full-day vehicle with "
        "driver from %s — per vehicle, not per person."
        % (eur(lowest("airport")), eur(lowest("shuttle")), eur(lowest("full_day")))
    )


def _event_costs_block():
    return _section(
        "Antalya Transfer Prices",
        "<p>Ground transport is usually a separate line in an Antalya budget. %s</p>" % _summary(),
        disclaimer(),
        "<p>%s</p>" % _link("Antalya transfer prices by vehicle"),
    )


def _logistics_block():
    return _section(
        "Antalya Transfer Pricing",
        "<p>For Antalya we publish indicative per-vehicle rates. %s These rates apply to "
        "Antalya only; transport in other destinations is quoted per programme.</p>" % _summary(),
        "<p>%s</p>" % _link("Antalya transfer prices"),
    )


def _cop31_transport_block():
    return (
        "<p>Indicative per-vehicle prices for airport transfers, daily shuttles and "
        "vehicles with driver are published on %s. %s</p>"
        % (_link("Antalya transfer prices"), _summary())
    )


BLOCKS = {
    "airport": _airport_block,
    "shuttle-full-day": _shuttle_block,
    "event-costs": _event_costs_block,
    "transport-logistics": _logistics_block,
    "cop31-transport": _cop31_transport_block,
}


def begin(name):
    return "<!-- transfer-prices:%s:begin -->" % name


def end(name):
    return "<!-- transfer-prices:%s:end -->" % name


def block(name):
    """Marker-wrapped fragment, as it appears in a page."""
    return "%s\n%s\n%s" % (begin(name), BLOCKS[name](), end(name))
