# -*- coding: utf-8 -*-
"""Single source of truth for site-wide identity, measurement and crawl config.

Everything here is injected into all pages by tools/site_seo.py. Change a value
here and re-run that script rather than editing 131 files.
"""

SITE = "https://dmcturkeypartner.com"

# --- Measurement -------------------------------------------------------------
# GA4 Measurement ID, e.g. "G-XXXXXXXXXX". While this is empty no analytics
# script is emitted at all, so the site stays clean until a real ID is set.
GA4_MEASUREMENT_ID = ""

# Optional Google Tag Manager container, e.g. "GTM-XXXXXXX". If both are set,
# GTM loads and GA4 is expected to be configured inside the container instead.
GTM_CONTAINER_ID = ""

# --- Search Console / webmaster verification ---------------------------------
# The token from Search Console's "HTML tag" verification method: just the
# content value, not the whole tag. Empty means no tag is emitted.
GOOGLE_SITE_VERIFICATION = ""
BING_SITE_VERIFICATION = ""

# --- IndexNow ----------------------------------------------------------------
# Key for instant Bing/Yandex/Seznam submission. tools/site_seo.py writes the
# matching key file at the site root when this is set.
INDEXNOW_KEY = ""

# --- Entity ------------------------------------------------------------------
# The canonical Organization node. A single stable @id referenced from every
# page is what lets Google and AI search engines resolve all of these pages to
# one entity rather than treating each variant name as a separate business.
ORG_NAME = "DMC Turkey Partner"
ORG_ALTERNATE_NAMES = [
    "DMC Partner Turkey",
    "DmcTurkeyPartner",
    "DmcTurkeyPartner.com",
    "DMC Turkey",
]
ORG_EMAIL = "hello@dmcturkeypartner.com"

# Published in visible HTML on 36 pages as the Antalya operations WhatsApp
# desk, so this is disclosed information rather than something invented here.
ORG_TELEPHONE = "+905353998999"

# /about/ states "Operating since 2006" in both its body copy and its meta
# description. Year only — never invent a month or a day.
ORG_FOUNDING_YEAR = "2006"
ORG_DESCRIPTION = (
    "Turkey-based destination management company (DMC) and local event operations "
    "partner for international agencies, MICE planners, incentive houses and group "
    "travel buyers, covering hotel sourcing, venue sourcing, transportation, event "
    "production, ground handling and white-label DMC support across Türkiye."
)

# Public profiles that corroborate the entity. Only add URLs that genuinely
# belong to the business — a wrong sameAs actively harms entity resolution.
ORG_SAME_AS = []

ORG_AREA_SERVED = ["Türkiye", "Istanbul", "Antalya", "Belek", "Bodrum", "Cappadocia"]

# --- Owner input still outstanding -------------------------------------------
# Each of these is a real-world fact this repository does not contain. Every
# emitting site is guarded by "if cfg.X", so leaving one empty suppresses the
# property rather than shipping a guess. tools/seo_check.py reports what is
# still unset on every run, so the gap stays visible instead of rotting in a
# checklist. A wrong value here is worse than no value: a sameAs pointing at
# the wrong profile merges this business with someone else's entity, and a
# fabricated address produces a weak LocalBusiness that competes with the
# correct Organization.

# Postal address of the registered office. Nothing on the site publishes one
# today. LocalBusiness and TravelAgency both require an address to earn a
# local rich result, so the @type stays Organization until this is filled in;
# see site_seo.organization(). Shape:
#   {"streetAddress": "...", "addressLocality": "Antalya",
#    "postalCode": "07...", "addressRegion": "Antalya", "addressCountry": "TR"}
ORG_ADDRESS = None

# {"latitude": 36.8..., "longitude": 30.7...} — only alongside ORG_ADDRESS.
ORG_GEO = None

# e.g. ["Mo-Fr 09:00-18:00"] in schema.org opening-hours syntax.
ORG_OPENING_HOURS = []

# The /event-costs/ scenario pages publish indicative budget ranges and state
# in the same breath that they are non-binding and not a quotation. Turning
# that into machine-readable price markup makes a claim the page disclaims, so
# it is the owner's call, not a default. When enabled, tools/page_schema.py
# emits a PriceSpecification with minPrice/maxPrice from data-budget-range.
EMIT_COST_PRICE_SPEC = False

ORG_KNOWS_ABOUT = [
    "Destination management",
    "MICE travel",
    "Incentive travel",
    "Corporate events",
    "Conference and congress operations",
    "Exhibition and pavilion services",
    "Group travel operations",
    "COP31 Antalya 2026 local event services",
]
