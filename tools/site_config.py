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
