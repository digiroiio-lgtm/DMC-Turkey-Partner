# -*- coding: utf-8 -*-
"""Single source of truth for site-wide identity, measurement and crawl config.

Everything here is injected into all pages by tools/site_seo.py. Change a value
here and re-run that script rather than editing 131 files.
"""

SITE = "https://dmcturkeypartner.com"

# --- Measurement -------------------------------------------------------------
# GA4 Measurement ID, e.g. "G-XXXXXXXXXX". Google tags are only loaded
# after optional analytics consent; an empty ID disables GA4.
GA4_MEASUREMENT_ID = "G-S23J4YMLTR"

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
INDEXNOW_KEY = "709df55c7d784cae9b54442e2dd67a81"

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
    "Turkey DMC",
    "Turkish DMC",
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
    "Ground handling Turkey",
    "White-label DMC services",
    "COP31 Antalya 2026 local event services",
]

# Registered travel agency operating the DMC Turkey Partner brand.
ORG_AGENCY_NAME = "ANTALYA GOLF MCD TRAVEL"
# Legal entity named alongside this agency in the TÜRSAB public record.
ORG_COMPANY_NAME = "PMR TURİZM İNŞAAT TİCARET LİMİTED ŞİRKETİ"
ORG_AGENCY_RECORD_URL = "https://www.tursab.org.tr/apps/Files/Content/71bb2e39-6a6f-456d-ac45-baa0a1bc0456.pdf"
ORG_TURSAB_NUMBER = "12434"
ORG_PHONE = "+905353998999"
ORG_PHONE_DISPLAY = "+90 535 399 89 99"
ORG_ADDRESS = {
    "@type": "PostalAddress",
    "streetAddress": "Güzeloba, 2268 Sok No:33",
    "postalCode": "07230",
    "addressLocality": "Muratpaşa",
    "addressRegion": "Antalya",
    "addressCountry": "TR",
}
