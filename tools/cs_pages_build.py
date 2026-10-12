#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the Czech landing page and the Czech privacy / cookie pages.

Usage: python3 tools/cs_pages_build.py   (then: python3 tools/sitemaps.py)

Writes:
  cs/dmc-turecko/index.html                         Czech copy of the German market page (DMC Turecko)
  cs/zasady-ochrany-osobnich-udaju/index.html       Czech privacy policy (translation, needs legal review)
  cs/zasady-cookies/index.html                      Czech cookie policy (translation, needs legal review)
Idempotent. Same architecture as the German page: shared header/footer lifted from an English page and
translated, the same proposal form and /api/request-proposal endpoint. Only facts that already appear on
the site are used. The Czech WhatsApp number is NOT in any generated file: the page asks /api/whatsapp?locale=cs
(server side) for it. The Czech copy should be reviewed by a native speaker before it is promoted.
"""

import html as htmllib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from cop31_common import SITE, esc  # noqa: E402
from cop31_render import FOOTER, HEADER, ROOT  # noqa: E402
import cs_legal_text as legal  # noqa: E402
import market_pages_build as mp  # noqa: E402
import site_header_cta  # noqa: E402
import site_seo  # noqa: E402

CS_PATH = mp.CS_PATH
UPDATED_ISO = "2026-10-12"
SOURCE_PAGE = CS_PATH

CHROME_CS = {
    "Skip to main content": "Přeskočit na hlavní obsah", "Menu": "Menu", "Solutions": "Řešení",
    "DMC Turkey": "DMC Turecko", "White-Label DMC": "White-label DMC", "MICE Turkey": "MICE Turecko",
    "Incentive Travel": "Incentivní cesty", "Corporate Events": "Firemní akce", "Group Travel": "Skupinové cesty",
    "Services": "Služby", "Services Overview": "Přehled služeb", "Hotel Sourcing": "Zajištění hotelů",
    "Transportation & Logistics": "Doprava a logistika", "Venue Sourcing": "Zajištění míst konání",
    "Event Production": "Produkce akcí", "Incentive Programs": "Incentivní programy",
    "Meetings & Conferences": "Schůzky a konference", "Destinations": "Destinace",
    "Destinations Overview": "Přehled destinací", "Cappadocia": "Kappadokie",
    "Plan Your COP31": "Plánování COP31", "News & Latest Updates": "Novinky a aktuality",
    "Participant Guide": "Průvodce pro účastníky", "Dates & Programme": "Termíny a program",
    "Conference Programme": "Program konference", "Venue & Location": "Místo konání a poloha",
    "Registration": "Registrace", "Group Accommodation": "Skupinové ubytování",
    "Restaurants & Dining": "Restaurace a stravování", "Local Services": "Místní služby",
    "Event Services": "Služby pro akce", "Exhibition Services": "Výstavní služby", "Exhibition Stands": "Výstavní stánky",
    "Booth Builder": "Stavba stánků", "Pavilion Services": "Služby pro pavilony", "Printing & Collateral": "Tisk a propagační materiály",
    "Branding & Signage": "Branding a značení", "AV & Equipment Rental": "Pronájem AV techniky a vybavení",
    "Furniture Rental": "Pronájem nábytku", "Coffee & Hospitality": "Káva a občerstvení", "Event Staff": "Personál akcí",
    "Hostesses": "Hostesky", "Interpreters": "Tlumočníci", "Private Transfers": "Soukromé transfery",
    "Airport Transfers": "Transfery z letiště", "Urgent Support": "Urgentní podpora",
    "Last-Minute Services": "Služby na poslední chvíli", "Company": "Společnost", "About": "O nás",
    "Agency Partners": "Partneři z řad agentur", "Selected Works": "Reference", "Why Turkey": "Proč Turecko",
    "Guides": "Průvodci", "Insights": "Poznatky", "MICE Calendar": "Kalendář MICE", "Contact": "Kontakt",
    "Book a Partner Call": "Domluvit hovor", "Request a Proposal": "Poptat nabídku",
    "Local DMC, MICE and white-label event execution across Turkey.": "Místní DMC, MICE a white-label realizace akcí po celém Turecku.",
    "Solutions & Services": "Řešení a služby", "All Services": "Všechny služby", "All Destinations": "Všechny destinace",
    "Event Costs": "Náklady na akce", "Guides & Insights": "Průvodci a poznatky", "COP31 Overview": "COP31 – přehled",
    "Venue & Dates": "Místo konání a termíny", "Exhibition & Pavilion Services": "Výstavní a pavilonové služby",
    "Last-Minute Support": "Podpora na poslední chvíli", "DMC Turkey Partner is operated by": "DMC Turkey Partner provozuje",
    "TÜRSAB Agency No:": "Číslo agentury TÜRSAB:", "Published TÜRSAB record": "Zveřejněný záznam TÜRSAB",
    "DmcTurkeyPartner.com. All rights reserved.": "DmcTurkeyPartner.com. Všechna práva vyhrazena.",
    "Privacy": "Ochrana soukromí", "Terms": "Podmínky", "Cookies": "Cookies", "Cookie Settings": "Nastavení cookies",
}
ARIA_CS = {"DMC Turkey Partner — home": "DMC Turkey Partner — úvodní stránka", "Primary": "Hlavní navigace",
           "Registered agency and contact details": "Registrované údaje agentury a kontakt"}


def localise_chrome_cs(fragment):
    # The Czech Republic is not a Fam Trip target country: no Fam Trip CTA in the Czech chrome.
    fragment = site_header_cta.sync(fragment, False)
    fragment = re.sub(r'(<a href=")/dmc-turkey/("[^>]*>)DMC Turkey(</a>)',
                      lambda m: m.group(1) + CS_PATH + m.group(2) + "DMC Turecko" + m.group(3), fragment)

    def text_node(match):
        raw = match.group(1)
        key = htmllib.unescape(raw.strip())
        if key in CHROME_CS:
            return ">" + raw.replace(raw.strip(), htmllib.escape(CHROME_CS[key], quote=False)) + "<"
        return match.group(0)

    fragment = re.sub(r">([^<>]+)<", text_node, fragment)
    for english, czech in ARIA_CS.items():
        fragment = fragment.replace('"%s"' % english, '"%s"' % czech)
    fragment = fragment.replace('href="/privacy-policy/"', 'href="%s"' % legal.PRIVACY_PATH)
    fragment = fragment.replace('href="/cookie-policy/"', 'href="%s"' % legal.COOKIES_PATH)
    return fragment.replace(
        '<li><a href="/terms/">Podmínky</a></li>',
        '<li><a href="/terms/">Podmínky</a></li>\n          <li><a href="%s" hreflang="en" lang="en">English</a></li>'
        '\n          <li><a href="%s" hreflang="de" lang="de">Deutsch</a></li>' % (mp.EN_PEER, mp.DE_PATH))


CS_FAQ = [
    ("Co v Turecku zajišťuje DMC?",
     "DMC zajišťuje místní část projektu: zajištění hotelů a míst konání, transfery a pozemní dopravu, produkci akcí, "
     "personál a podporu na místě. Agentura ani firma tak nemusí koordinovat jednotlivé dodavatele sama."),
    ("V jakých destinacích působíte?",
     "V Istanbulu, Antalyi, Beleku, Kappadokii a Bodrumu. V Turecku působíme od roku 2006."),
    ("Jak rychle dostaneme nabídku?",
     "Ozveme se Vám do 24 hodin a podrobnou nabídku zašleme do 3–5 pracovních dnů. Po Vašem potvrzení se projektu ujme "
     "stálá kontaktní osoba."),
    ("Můžete pro naši agenturu pracovat jako white-label partner?",
     "Ano, pokud to dává smysl. Agentura si ponechává vztah s klientem a my zajišťujeme místní realizaci v Turecku."),
]

WA_MESSAGE = ("Dobrý den, právě jsem prostřednictvím Vašeho webu odeslal(a) poptávku.\n"
              "Jméno: {name}\nSpolečnost: {company}\nPoptávka: {summary}\nReferenční číslo: {ref}\n"
              "Rád(a) bych s Vámi probral(a) své požadavky.")


def form_labels():
    phone = ('\n          <div class="form-field"><label for="cs-phone">Telefon <span class="field-optional">(nepovinné)</span></label>'
             '<input type="tel" id="cs-phone" name="phone" data-prefix="+420 " placeholder="+420 123 456 789" autocomplete="tel" '
             'inputmode="tel" pattern="^\\+?[0-9][0-9 \\-]{5,22}$" maxlength="24"></div>')
    return dict(
        anchor="poptavka", honeypot="Webová stránka společnosti (nevyplňujte)", h2="Odeslat poptávku",
        lede="Sdělte nám destinaci, velikost skupiny a termíny. Odpovíme do 24 hodin.",
        name="cs-landing-brief", name_l="Vaše jméno", company_l="Společnost", email_l="Pracovní e-mail", dest_l="Destinace",
        dest_ph="Vyberte destinaci", group_l="Přibližná velikost skupiny", group_ph="Vyberte velikost",
        type_l="Typ projektu", type_ph="Vyberte typ projektu", dates_l="Termín cesty / akce", start="Datum zahájení",
        end="Datum ukončení", unconf="Termíny zatím nejsou potvrzeny", brief_l="Stručný popis projektu", optional="nepovinné",
        brief_ph="Třídenní incentivní program pro přibližně 120 hostů v Antalyi ...",
        privacy=('Vaše kontaktní údaje použijeme k vyřízení poptávky, jak je popsáno v <a href="%s">Zásadách ochrany osobních údajů</a>. '
                 'Nabídka není rezervace. Neposílejte prosím kopie pasů, údaje o platebních kartách ani citlivé osobní údaje.' % legal.PRIVACY_PATH),
        submit="Odeslat poptávku", ok_h="Děkujeme – Vaši poptávku jsme přijali.",
        ok_p="Odpovíme do 24 hodin a podrobnou nabídku zašleme do 3–5 pracovních dnů.",
        s0="Do 20", s_nc="Zatím nepotvrzeno", cappadocia="Kappadokie", multi="Více destinací", nd="Zatím nerozhodnuto",
        t_conf="Schůzka / konference", t_inc="Incentivní cesta", t_corp="Firemní akce", t_grp="Skupinová cesta",
        t_wl="White-label podpora DMC", t_oth="Jiné",
        form_attrs=' data-source-page="%s" data-whatsapp-locale="cs" data-reference-prefix="CS"' % SOURCE_PAGE,
        hidden_extra='<input type="hidden" name="locale" value="cs"><input type="hidden" name="reference">',
        extra_fields=phone,
        i18n={
            "sending": "Odesílání…",
            "sent": "Poptávka odeslána",
            "error": "Poptávku se nepodařilo odeslat. Zadané údaje zůstaly zachovány: zkuste to prosím znovu nebo napište na hello@dmcturkeypartner.com.",
            "datesRequired": "Zadejte prosím termín cesty či akce, nebo zaškrtněte „Termíny zatím nejsou potvrzeny“.",
            "dateOrder": "Datum ukončení nesmí být dřívější než datum zahájení.",
            "modalClose": "Zavřít",
            "modalTitle": "Děkujeme!",
            "modalSub": "Vaši poptávku jsme přijali.",
            "modalDesc": "Odpovíme do 24 hodin a podrobnou nabídku zašleme do 3–5 pracovních dnů.",
            "modalFasterTitle": "Potřebujete rychlejší odpověď?",
            "modalFasterText": "Pro rychlejší vyřízení nás můžete okamžitě kontaktovat na WhatsApp.",
            "modalWhatsapp": "Napsat na WhatsApp",
            "modalBack": "Zpět na web",
            "modalNote": "Vaše poptávka již byla odeslána. Není třeba ji posílat znovu.",
            "whatsappMessage": WA_MESSAGE,
            "datesUnknown": "termíny zatím nepotvrzeny",
            "fieldRequired": "Vyplňte prosím toto pole.",
            "emailInvalid": "Zadejte prosím platnou e-mailovou adresu.",
            "phoneInvalid": "Zadejte prosím telefonní číslo ve tvaru +420 123 456 789.",
        },
        expect="<li>Odpověď do 24 hodin</li><li>Podrobná nabídka do 3–5 pracovních dnů</li><li>Stálá kontaktní osoba po potvrzení</li>")


def render_cs():
    title = "DMC Turecko | Incentivní cesty, MICE a firemní akce"
    description = ("DMC Turecko pro české agentury: incentivní cesty, MICE a firemní akce v Istanbulu, Antalyi, Beleku, "
                   "Kappadokii a Bodrumu. Místní realizace od roku 2006.")
    crumbs = [("Úvod", "/"), ("DMC Turecko", CS_PATH)]
    hreflang = "\n".join([
        '  <link rel="alternate" hreflang="cs" href="%s%s">' % (SITE, CS_PATH),
        '  <link rel="alternate" hreflang="de" href="%s%s">' % (SITE, mp.DE_PATH),
        '  <link rel="alternate" hreflang="en" href="%s%s">' % (SITE, mp.EN_PEER),
        '  <link rel="alternate" hreflang="x-default" href="%s%s">' % (SITE, mp.EN_PEER),
    ])
    L = form_labels()
    body = "\n".join([
        mp.crumbs_html(crumbs),
        '    <section class="page-section" data-cta-location="hero">',
        "      <h1>DMC Turecko: incentivní cesty, MICE a firemní akce na místě</h1>",
        '      <p class="reviewed-note">Naposledy aktualizováno: <time datetime="%s">12. 10. 2026</time></p>' % UPDATED_ISO,
        '      <p class="page-section__lede">DMC Turkey Partner je destinační management společnost se sídlem v Antalyi, která '
        "v Turecku působí od roku 2006. Pro mezinárodní agentury, incentivní společnosti a firmy zajišťujeme MICE programy, "
        "incentivní cesty, firemní akce a skupinové cesty v Istanbulu, Antalyi, Beleku, Kappadokii a Bodrumu: od zajištění "
        "hotelů a míst konání přes transfery a produkci akcí až po podporu na místě.</p>",
        '      <div class="hero-actions"><a class="btn btn--primary" href="#poptavka">Odeslat poptávku</a></div>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Co v Turecku zajišťuje DMC</h2>",
        "      " + mp.cards([
            ("Hotely", "Skupinové ubytování, kontingenty pokojů, kongresové hotely a resorty."),
            ("Transfery a pozemní doprava", "Transfery z letiště, soukromá vozidla, autobusy, skupinové kyvadlové linky a VIP transfery."),
            ("Místa konání", "Kongresová místa, prostory pro akce, místa pro večeře a neobvyklé lokace."),
            ("MICE a akce", "Schůzky, incentivní cesty, konference, firemní akce a galavečeře."),
            ("Produkce akcí", "Zvuk, světla, video, pódium, konstrukce a technická koordinace."),
            ("Personál a akreditace", "Hostesky, registrace a na přání tlumočníci."),
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Naše destinace</h2>",
        "      " + mp.cards([
            ('<a href="/destinations/istanbul/">Istanbul</a>', "Schůzky, konference, firemní akce, incentivní cesty a prémiové skupiny."),
            ('<a href="/destinations/antalya/">Antalya</a>', "Velké skupiny, konference, incentivní cesty, resorty a firemní hospitalita."),
            ('<a href="/destinations/belek/">Belek</a>', "Resortové schůzky, konference, golfové incentivy a velké nároky na ubytování."),
            ('<a href="/destinations/cappadocia/">Kappadokie</a>', "Incentivní cesty, vedoucí týmy a výjimečné zážitkové programy."),
            ('<a href="/destinations/bodrum/">Bodrum</a>', "Prémiové incentivní cesty, firemní hospitalita a soukromé skupiny."),
        ]),
        '      <p class="section-more">Odkazované stránky destinací jsou v angličtině.</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Orientační hodnoty rozpočtu</h2>",
        "      <p>Zveřejněné orientační hodnoty na osobu, bez letenek, pro mezisezónu (duben–červen, září–listopad):</p>",
        "      <ul><li>Incentivní cesta, 4 noci, 5* all-inclusive resort v Antalyi (50–150 hostů): 500–750 € — "
        '<a href="/event-costs/antalya/">Antalya (anglicky)</a></li>'
        "<li>Firemní retreat, 4 noci, 5* all-inclusive resort v Beleku (50–150 hostů): 500–750 € — "
        '<a href="/event-costs/belek/">Belek (anglicky)</a></li>'
        "<li>Konference, 3 noci, 4* městský hotel v Istanbulu (50–150 hostů): 350–500 € — "
        '<a href="/event-costs/istanbul/">Istanbul (anglicky)</a></li></ul>',
        '      <p class="price-note">Nezávazné plánovací hodnoty. Ve vrcholné sezóně (červenec–srpen) se uplatňuje příplatek 15–25 %. '
        'Vlastní scénáře si můžete projít v <a href="/event-cost-calculator/">kalkulačce rozpočtu</a> (anglicky).</p>',
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Jak projekt probíhá</h2>",
        "      " + mp.steps([
            ("Poptávka", "Destinace, termíny, velikost skupiny a typ projektu."),
            ("Odpověď do 24 hodin", "Upřesníme, co je možné, a položíme správné otázky."),
            ("Podrobná nabídka", "Do 3–5 pracovních dnů."),
            ("Kontaktní osoba a realizace", "Po Vašem potvrzení se programu na místě ujme stálá kontaktní osoba."),
        ]),
        "    </section>",
        '    <section class="page-section">',
        "      <h2>Váš partner na místě</h2>",
        "      <p>DMC Turkey Partner provozuje ANTALYA GOLF MCD TRAVEL (PMR TURİZM İNŞAAT TİCARET LİMİTED ŞİRKETİ), "
        "Güzeloba, 2268 Sok No:33, 07230 Muratpaşa, Antalya. Číslo agentury TÜRSAB 12434. Reference najdete v sekci "
        '<a href="/selected-works/">Selected Works</a> (anglicky).</p>',
        "    </section>",
        mp.faq_html("Časté dotazy", CS_FAQ),
        mp.form_html(L, "cs"),
        '    <section class="page-section"><h2>Více v angličtině</h2><p class="cluster-links">'
        '<a href="/dmc-turkey/">DMC Turkey (English)</a><a href="/mice-turkey/">MICE Turkey</a>'
        '<a href="/incentive-travel-turkey/">Incentive travel</a>'
        '<a href="/corporate-events-turkey/">Corporate events</a></p></section>',
    ])
    page_head = mp.head("cs", title, description, CS_PATH, "CS / Czech", "DMC Turecko",
                        mp.schema("cs", "DMC Turecko", CS_PATH, description, crumbs, CS_FAQ), hreflang)
    page = mp.assemble(page_head, body, localise_chrome_cs(HEADER), localise_chrome_cs(FOOTER))
    # The floating WhatsApp button exists on the Czech page only.
    return page.replace("</body>", '  <script src="/assets/js/cs-whatsapp.js" defer></script>\n</body>', 1)


def legal_page(slug, heading, description, content):
    path = "/cs/%s/" % slug
    url = SITE + path
    crumbs = [("Úvod", "/"), (heading, path)]
    web = {"@context": "https://schema.org", "@type": "WebPage", "name": heading, "url": url, "description": description,
           "inLanguage": "cs", "dateModified": legal.UPDATED_ISO, "isPartOf": {"@id": SITE + "/#website"},
           "publisher": {"@id": SITE + "/#organization"}}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                                      for i, (n, p) in enumerate(crumbs)]}
    ld = "\n".join('  <script type="application/ld+json">\n  %s\n  </script>' % json.dumps(d, ensure_ascii=False, separators=(",", ":"))
                   for d in (web, breadcrumb))
    title = "%s | DmcTurkeyPartner.com" % heading
    head = "\n".join([
        "<!DOCTYPE html>", '<html lang="cs">', "<head>", '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '  <link rel="icon" href="/favicon.svg" type="image/svg+xml">', '  <link rel="icon" href="/favicon.ico" sizes="any">',
        '  <link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">',
        '  <link rel="apple-touch-icon" href="/apple-touch-icon.png" sizes="180x180">', '  <link rel="manifest" href="/site.webmanifest">',
        "  <title>%s</title>" % esc(title), '  <meta name="description" content="%s">' % esc(description),
        '  <link rel="canonical" href="%s">' % url, '  <meta name="robots" content="index, follow">',
        '  <meta property="og:type" content="website">', '  <meta property="og:title" content="%s">' % esc(title),
        '  <meta property="og:description" content="%s">' % esc(description), '  <meta property="og:url" content="%s">' % url,
        '  <meta property="og:site_name" content="DMC Turkey Partner">', '  <meta property="og:locale" content="cs_CZ">',
        '  <meta property="og:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="twitter:card" content="summary_large_image">',
        '  <meta name="twitter:image" content="%s/assets/img/social-preview.png">' % SITE,
        '  <meta name="dmc:page-type" content="legal">', '  <link rel="stylesheet" href="/assets/css/main.css">', ld, "</head>",
    ])
    body = ('<main id="main-content" class="page--legal">\n    <nav class="breadcrumbs" aria-label="Breadcrumb"><ol><li><a href="/">Úvod</a></li>'
            '<li aria-current="page">%s</li></ol></nav>\n    <h1>%s</h1>\n    <p class="legal-updated">Naposledy zkontrolováno: '
            '<time datetime="%s">%s</time>. Česká verze je překladem anglického oznámení; v případě nejasností platí <a href="%s" '
            'hreflang="en" lang="en">anglická verze</a>.</p>\n    %s\n  </main>'
            % (esc(heading), esc(heading), legal.UPDATED_ISO, legal.UPDATED, "/privacy-policy/" if "ochrany" in slug else "/cookie-policy/", content))
    return mp.assemble(head, body, localise_chrome_cs(HEADER), localise_chrome_cs(FOOTER))


def main():
    mp.write_page("cs/dmc-turecko/index.html", render_cs())
    for slug, (heading, description, content) in legal.PAGES.items():
        mp.write_page("cs/%s/index.html" % slug, legal_page(slug, heading, description, content))


if __name__ == "__main__":
    main()
