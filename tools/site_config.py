# -*- coding: utf-8 -*-
"""Single source of truth for site-wide identity, measurement and crawl config.

Everything here is injected into all pages by tools/site_seo.py. Change a value
here and re-run that script rather than editing 131 files.
"""

SITE = "https://dmcturkeypartner.com"

# --- Measurement -------------------------------------------------------------
# GTM is the intended architecture: the container is the single tag on the
# page, and GA4 (plus anything added later, such as Ads) is configured inside
# it. The site's own event layer only pushes to window.dataLayer, which is
# what a GTM custom-event trigger reads, so no redeploy is needed to add or
# retire a tag. Set GTM_CONTAINER_ID to a real "GTM-XXXXXXX" and re-run
# tools/site_seo.py to turn measurement on across all pages.
GTM_CONTAINER_ID = ""

# Direct GA4 alternative, e.g. "G-XXXXXXXXXX". Only used when no GTM container
# is set — never set both, or every event configured in the container would
# also be counted by gtag.js and the site would double-count. While both are
# empty no measurement script is emitted at all, so the site stays clean.
GA4_MEASUREMENT_ID = ""

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
