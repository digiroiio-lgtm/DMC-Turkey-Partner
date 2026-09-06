"""Shared constants, URL builders and HTML fragments for the COP31 cluster.

Every fact in FACTS below is taken from an official COP31/UNFCCC source and is
re-checked before LAST_UPDATED is bumped. Nothing in this module may assert an
affiliation between DmcTurkeyPartner and UNFCCC or the COP31 organising bodies.
"""

SITE = "https://dmcturkeypartner.com"
WHATSAPP_NUMBER = "905353998999"
LAST_UPDATED = "2026-09-06"
LAST_UPDATED_LABEL = "6 September 2026"

# --- Verified official facts -------------------------------------------------
CONFERENCE_DATES = "9–20 November 2026"
CONFERENCE_DATES_PLAIN = "9 to 20 November 2026"
VENUE = "Antalya EXPO Center"
CITY = "Antalya, Türkiye"

# --- Official sources --------------------------------------------------------
SRC_UNFCCC = "https://unfccc.int/cop31"
SRC_IFP = "https://unfccc.int/cop31/ifp"
SRC_ROAD = "https://unfccc.int/cop31/the-road-to-antalya"
SRC_OBSERVERS = "https://unfccc.int/cop31/observer-organizations"
SRC_TR = "https://cop31.tr/"
SRC_TR_PROGRAMME = "https://cop31.tr/tr/cop31-konferans-programi"
SRC_TR_CONTACT = "https://cop31.tr/tr/iletisim"

OFFICIAL_LINKS = {
    "unfccc": (SRC_UNFCCC, "UNFCCC – COP31"),
    "ifp": (SRC_IFP, "UNFCCC – Information for COP31 Participants"),
    "road": (SRC_ROAD, "UNFCCC – The Road to Antalya"),
    "observers": (SRC_OBSERVERS, "UNFCCC – Observer Organizations"),
    "tr": (SRC_TR, "COP31 Türkiye – Official Website"),
    "programme": (SRC_TR_PROGRAMME, "COP31 Türkiye – Official Conference Programme"),
    "contact": (SRC_TR_CONTACT, "COP31 Türkiye – Official Contact Channels"),
}

DISCLAIMER = (
    "DmcTurkeyPartner is an independent destination management and event services provider. "
    "We are not affiliated with, endorsed by, or part of UNFCCC or the official COP31 organising "
    "bodies. Official conference information, registration and accreditation are managed by the "
    "relevant COP31 and UNFCCC authorities."
)


def esc(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def urlenc(value):
    from urllib.parse import quote

    return quote(str(value), safe="")


def proposal_url(slug, service_interest, page_type):
    """Existing Request a Proposal form, carrying COP31 attribution in the URL.

    main.js copies these parameters into the form's hidden attribution fields
    and pre-selects the destination / project type dropdowns.
    """
    params = [
        ("source", slug),
        ("lead_source", "COP31"),
        ("campaign", "COP31 Antalya 2026"),
        ("service_interest", service_interest),
        ("page_type", page_type),
        ("destination", "Antalya"),
        ("project_type", "COP31 Antalya"),
    ]
    return "/request-proposal/?" + "&amp;".join(
        "%s=%s" % (k, urlenc(v)) for k, v in params
    )


def whatsapp_url(message):
    return "https://wa.me/%s?text=%s" % (WHATSAPP_NUMBER, urlenc(message))


def wa_link(label, message, ghost=True):
    cls = "btn btn--ghost" if ghost else "btn btn--primary"
    return (
        '<a class="%s" href="%s" target="_blank" rel="noopener" '
        'data-track="cop31_whatsapp_click">%s</a>' % (cls, whatsapp_url(message), label)
    )


def cta_link(label, slug, service_interest, page_type, primary=True):
    cls = "btn btn--primary" if primary else "btn btn--ghost"
    return '<a class="%s" href="%s" data-track="cop31_proposal_cta_click">%s</a>' % (
        cls,
        proposal_url(slug, service_interest, page_type),
        label,
    )
