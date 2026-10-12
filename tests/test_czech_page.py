"""Regression tests for the Czech landing page /cs/dmc-turecko/, its legal pages, the WhatsApp routing and the API."""

import html as htmllib
import json
import os
import re
import shutil
import subprocess
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

from playwright.sync_api import expect, sync_playwright

from test_calculator_proposal import ROOT, StaticHandler

SITE = "https://dmcturkeypartner.com"
CS = "/cs/dmc-turecko/"
PRIVACY = "/cs/zasady-ochrany-osobnich-udaju/"
COOKIES = "/cs/zasady-cookies/"
MOCK_NUMBER = "420111222333"  # test double, not the real number
MAIN_NUMBER = "905353998999"
# The real Czech number, assembled so that this file does not contain it in one piece.
REAL = "".join(["420", "774", "018", "359"])
REAL_FORMS = [REAL, "+" + REAL, "%s %s %s %s" % (REAL[:3], REAL[3:6], REAL[6:9], REAL[9:]),
              "+%s %s %s %s" % (REAL[:3], REAL[3:6], REAL[6:9], REAL[9:]), "%s %s %s" % (REAL[3:6], REAL[6:9], REAL[9:]),
              REAL[3:], "%s-%s-%s" % (REAL[3:6], REAL[6:9], REAL[9:])]
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


def read(path):
    return (ROOT / path.strip("/") / "index.html").read_text(encoding="utf-8")


def visible(page_html, region="body"):
    match = re.search(r"<%s.*?</%s>" % (region, region), page_html, re.S)
    text = re.sub(r"<script.*?</script>", " ", match.group(0), flags=re.S)
    return htmllib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", text)))


class CzechStaticTests(unittest.TestCase):
    def test_head_and_hreflang(self):
        page = read(CS)
        self.assertIn('<html lang="cs">', page)
        self.assertIn('property="og:locale" content="cs_CZ"', page)
        self.assertIn('<link rel="canonical" href="%s%s">' % (SITE, CS), page)
        self.assertIn('<meta name="robots" content="index, follow">', page)
        self.assertEqual(len(re.findall(r"<h1[ >]", page)), 1)
        title = htmllib.unescape(re.search(r"<title>(.*?)</title>", page).group(1))
        description = htmllib.unescape(re.search(r'<meta name="description" content="(.*?)">', page).group(1))
        self.assertLessEqual(len(title), 65)
        self.assertTrue(70 <= len(description) <= 160, len(description))
        expected = {"cs": CS, "de": "/de/dmc-tuerkei/", "en": "/dmc-turkey/", "x-default": "/dmc-turkey/"}
        for path in (CS, "/de/dmc-tuerkei/", "/dmc-turkey/"):
            html = read(path)
            for lang, target in expected.items():
                self.assertIn('hreflang="%s" href="%s%s"' % (lang, SITE, target), html, (path, lang))

    def test_sitemap_redirects_and_llms(self):
        sitemap = (ROOT / "sitemap-pages.xml").read_text()
        for path in (CS, PRIVACY, COOKIES):
            self.assertEqual(sitemap.count("<loc>%s%s</loc>" % (SITE, path)), 1, path)
        redirects = json.loads((ROOT / "vercel.json").read_text())["redirects"]
        found = {(r["source"], r["destination"]) for r in redirects}
        self.assertIn(("/cs", CS), found)
        self.assertIn(("/cs/", CS), found)
        self.assertIn(SITE + CS, (ROOT / "llms.txt").read_text())

    def test_json_ld_and_faq_parity(self):
        page = read(CS)
        blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S)]
        faq = next(b for b in blocks if b.get("@type") == "FAQPage")
        text = visible(page, "main")
        self.assertEqual(len(faq["mainEntity"]), 4)
        for entry in faq["mainEntity"]:
            self.assertIn(entry["name"], text)
            self.assertIn(entry["acceptedAnswer"]["text"], text)
        web = next(b for b in blocks if b.get("@type") == "WebPage")
        self.assertEqual(web["inLanguage"], "cs")

    def test_czech_text_quality(self):
        for path in (CS, PRIVACY, COOKIES):
            raw = (ROOT / path.strip("/") / "index.html").read_bytes()
            page = raw.decode("utf-8")  # raises on invalid UTF-8
            self.assertNotIn("�", page, path)
            for mojibake in ("Ã", "Å¡", "Ä›", "Ä\u008d", "â€", "Å™", "Å¾"):
                self.assertNotIn(mojibake, page, (path, mojibake))
            text = visible(page, "main")
            self.assertRegex(text, r"[ěščřžýáíéúůďťň]")
            # Formal address ("Vy"): no informal second person.
            self.assertNotRegex(text, r"(?i)\b(tvůj|tvoje|tvoji|tvým|tobě|tebe|ty jsi)\b", path)
        text = visible(read(CS), "main").lower()
        for word in ("odeslat poptávku", "kappadokie", "incentivní cesty", "firemní akce", "váš partner na místě", "časté dotazy"):
            self.assertIn(word, text, word)
        # Terminology is consistent: "incentivní", never the English word in running Czech text.
        self.assertNotIn("incentive ", text.replace("incentive travel", ""))

    def test_no_untranslated_ui_and_czech_formats(self):
        page = read(CS)
        shown = visible(page)
        for english in ("Request a Proposal", "Send Your", "Your Name", "Work Email", "Submit", "Thank you", "Privacy Policy",
                        "Skip to main content", "Cookie Settings", "Last updated", "Frequently Asked", "Book a Partner Call",
                        "Fam Trip", "Select a destination", "Dates Not Confirmed"):
            self.assertNotIn(english, shown, english)
        main = visible(page, "main")
        self.assertIn("12. 10. 2026", main)
        self.assertNotRegex(main, r"\b20\d\d-\d\d-\d\d\b")
        for amount in re.findall(r"\d[\d–]*\s?€|€\s?\d", main):
            self.assertRegex(amount, r"^\d+–\d+ €$", amount)
        self.assertIn("15–25 %", main)

    def test_form_markup_is_czech_and_has_the_extra_fields(self):
        page = read(CS)
        form = re.search(r"<form.*?</form>", page, re.S).group(0)
        for needle in ('data-whatsapp-locale="cs"', 'data-source-page="/cs/dmc-turecko/"', 'name="locale" value="cs"',
                       'name="reference"', 'name="phone"', 'type="tel"', 'data-prefix="+420 "', "Odeslat poptávku",
                       "Vaše jméno", "Pracovní e-mail", "Vyberte destinaci", "Termíny zatím nejsou potvrzeny"):
            self.assertIn(needle, form, needle)
        self.assertIn(PRIVACY, form)
        i18n = json.loads(htmllib.unescape(re.search(r'data-i18n="([^"]+)"', form).group(1)))
        for key in ("sending", "sent", "error", "datesRequired", "dateOrder", "modalTitle", "modalFasterText", "modalWhatsapp",
                    "whatsappMessage", "fieldRequired", "emailInvalid", "phoneInvalid"):
            self.assertTrue(i18n[key], key)
        self.assertIn("{name}", i18n["whatsappMessage"])
        self.assertIn("{ref}", i18n["whatsappMessage"])
        self.assertEqual(i18n["modalWhatsapp"], "Napsat na WhatsApp")
        # German and main forms are untouched.
        for other in ("/de/dmc-tuerkei/", "/dmc-turkey-uk-agencies/", "/request-proposal/"):
            html = read(other)
            for token in ('data-whatsapp-locale', 'name="phone"', 'name="locale"', 'name="reference"'):
                self.assertNotIn(token, html, (other, token))

    def test_czech_number_exists_only_on_the_server(self):
        offenders = []
        for base, dirs, files in os.walk(ROOT):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "tests", "__pycache__")]
            for name in files:
                path = os.path.join(base, name)
                relative = os.path.relpath(path, ROOT).replace(os.sep, "/")
                if relative == "api/_whatsapp-config.js" or name.endswith((".webp", ".png", ".ico", ".svg", ".pdf", ".jpg")):
                    continue
                try:
                    with open(path, encoding="utf-8") as handle:
                        content = handle.read()
                except UnicodeDecodeError:
                    continue
                if any(form in content for form in REAL_FORMS):
                    offenders.append(relative)
        self.assertEqual(offenders, [], "the Czech WhatsApp number must live only in api/_whatsapp-config.js (or the env var)")
        self.assertIn(REAL, (ROOT / "api/_whatsapp-config.js").read_text())

    def test_only_the_czech_page_uses_the_locale_whatsapp(self):
        for path in ROOT.glob("**/index.html"):
            relative = path.relative_to(ROOT).as_posix()
            if ".git/" in relative:
                continue
            page = path.read_text(encoding="utf-8")
            if relative.startswith("cs/"):
                continue
            self.assertNotIn("cs-whatsapp.js", page, relative)
            self.assertNotIn("data-whatsapp-locale", page, relative)
        self.assertIn("cs-whatsapp.js", read(CS))
        self.assertNotIn("cs-whatsapp.js", read("/de/dmc-tuerkei/"))
        for script in ("assets/js/main.js", "assets/js/cs-whatsapp.js", "assets/js/privacy.js"):
            self.assertFalse(any(form in (ROOT / script).read_text() for form in REAL_FORMS), script)

    def test_czech_pages_have_no_fam_trip_cta_and_german_keeps_the_main_number(self):
        for path in (CS, PRIVACY, COOKIES):
            page = read(path)
            self.assertNotIn("fam-header", page)
            self.assertNotIn("agency-fam-trip", page)
        self.assertIn('lang="cs"', read(CS))
        self.assertIn(MAIN_NUMBER, (ROOT / "assets/js/main.js").read_text())

    def test_legal_pages_are_complete(self):
        privacy = visible(read(PRIVACY), "main")
        for needle in ("Zásady ochrany osobních údajů", "Kdo odpovídá za Vaše údaje?", "Vaše práva a jak nás kontaktovat",
                       "Úřad pro ochranu osobních údajů", "WhatsApp", "Resend", "Vercel", "Google Analytics", "KVKK"):
            self.assertIn(needle, privacy, needle)
        cookies = visible(read(COOKIES), "main")
        for needle in ("dmc_cookie_choice_v1", "dtp_calculator_state", "Povolit volitelnou analytiku", "180 dní"):
            self.assertIn(needle, cookies, needle)
        english = visible(read("/privacy-policy/"), "main")
        self.assertEqual(len(re.findall(r"<h2>", re.search(r"<main.*?</main>", read(PRIVACY), re.S).group(0))),
                         len(re.findall(r"<h2>", re.search(r"<main.*?</main>", read("/privacy-policy/"), re.S).group(0))))
        self.assertGreater(len(privacy.split()), 0.7 * len(english.split()))


def node(script, env=None):
    result = subprocess.run(["node", "-e", script], cwd=str(ROOT), capture_output=True, text=True,
                            env=dict(os.environ, **(env or {})), timeout=60)
    if result.returncode != 0:
        raise AssertionError(result.stderr)
    return json.loads(result.stdout)


class CzechApiTests(unittest.TestCase):
    WHATSAPP = """
    const h = require('./api/whatsapp.js');
    const call = (query, method) => { const o = {headers: {}}; h({method: method || 'GET', query}, {setHeader(k, v) { o.headers[k] = v; },
      status(c) { o.status = c; return this; }, json(b) { o.body = b; }}); return o; };
    console.log(JSON.stringify({cs: call({locale: 'cs'}), upper: call({locale: 'CS'}), de: call({locale: 'de'}), none: call({}), post: call({locale: 'cs'}, 'POST')}));
    """

    def test_whatsapp_endpoint(self):
        default = node(self.WHATSAPP)
        self.assertEqual((default["cs"]["status"], default["cs"]["body"]["number"]), (200, REAL))
        self.assertEqual(default["cs"]["headers"]["Cache-Control"], "no-store")
        self.assertEqual(default["upper"]["status"], 200)
        self.assertEqual(default["de"]["status"], 404)
        self.assertEqual(default["none"]["status"], 404)
        self.assertEqual(default["post"]["status"], 405)
        for body in (default["de"]["body"], default["none"]["body"]):
            self.assertNotIn(REAL, json.dumps(body))
            self.assertNotIn(MAIN_NUMBER, json.dumps(body))
        override = node(self.WHATSAPP, {"WHATSAPP_NUMBER_CS": "+420 123 456 789"})
        self.assertEqual(override["cs"]["body"]["number"], "420123456789")
        broken = node(self.WHATSAPP, {"WHATSAPP_NUMBER_CS": "abc"})
        self.assertEqual(broken["cs"]["body"]["number"], REAL, "an invalid env value falls back to the default")

    PROPOSAL = """
    const sent = [];
    global.fetch = async (url, init) => { sent.push(JSON.parse(init.body)); return {ok: true, text: async () => ''}; };
    process.env.RESEND_API_KEY = 'test';
    const handler = require('./api/request-proposal.js');
    const run = async (body, headers) => { const o = {}; await handler({method: 'POST', body, headers: headers || {}},
      {setHeader() {}, status(c) { o.status = c; return this; }, json(b) { o.body = b; }}); return o; };
    (async () => {
      const base = {name: 'Jana Nováková', company: 'Acme Travel', email: 'jana@example.invalid', destination: 'Antalya', group_size: '51–100',
        source_page: '/cs/dmc-turecko/', timestamp: '2026-10-12T10:00:00Z'};
      const out = {};
      out.cs = await run(Object.assign({}, base, {lead_source: 'CS / Czech', locale: 'cs', reference: 'CS-261012-AB7K', phone: '+420 777 123 456'}), {'x-vercel-ip-country': 'DE'});
      out.de = await run(Object.assign({}, base, {lead_source: 'DE Landing', locale: 'de'}), {'x-vercel-ip-country': 'CZ'});
      out.plain = await run(base, {});
      out.mails = sent;
      console.log(JSON.stringify(out));
    })();
    """

    def test_request_proposal_email(self):
        out = node(self.PROPOSAL)
        self.assertEqual([out["cs"]["status"], out["de"]["status"], out["plain"]["status"]], [200, 200, 200])
        cs, de, plain = out["mails"]
        self.assertEqual(cs["subject"], "CS / Czech Lead — Acme Travel (Antalya)")
        for needle in ("Czech-language page /cs/dmc-turecko/", "Czech number +" + REAL, "CS-261012-AB7K", "+420 777 123 456",
                       "Visitor Country (IP, reporting only)", "DE", "Locale", "cs"):
            self.assertIn(needle, cs["text"], needle)
        self.assertIn("Czech-language page", cs["html"])
        # The IP country is reporting only: a German IP still gets the Czech route because the page is Czech,
        # and a Czech IP on a non-Czech page never gets the Czech number.
        self.assertIn("Visitor Country (IP, reporting only): CZ", de["text"])
        self.assertNotIn(REAL, de["text"] + de["html"])
        self.assertNotIn("Czech-language", de["text"])
        self.assertEqual(de["subject"], "DE Landing Lead — Acme Travel (Antalya)")
        self.assertNotIn(REAL, plain["text"])
        self.assertNotIn("Locale", plain["text"])
        self.assertNotIn("Visitor Country", plain["text"])


class CzechBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), partial(StaticHandler, directory=str(ROOT)))
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base_url = "http://127.0.0.1:" + str(cls.server.server_port)
        cls.addClassCleanup(cls.server.server_close)
        cls.addClassCleanup(cls.server.shutdown)
        cls.playwright = sync_playwright().start()
        cls.addClassCleanup(cls.playwright.stop)
        chromium = os.environ.get("DMC_CHROMIUM") or shutil.which("chromium")
        options = {"headless": True}
        if chromium:
            options["executable_path"] = chromium
        cls.browser = cls.playwright.chromium.launch(**options)
        cls.addClassCleanup(cls.browser.close)

    def open(self, path, width=1280, whatsapp_status=200, consent=True):
        self.posts, self.whatsapp_hits, self.external = [], [], []
        context = self.browser.new_context(viewport={"width": width, "height": 900}, user_agent=UA, locale="cs-CZ")
        self.addCleanup(context.close)

        def route(r):
            url = urlsplit(r.request.url)
            if url.netloc != urlsplit(self.base_url).netloc:
                self.external.append(r.request.url)
                r.abort()
            elif url.path == "/api/whatsapp":
                self.whatsapp_hits.append(url.query)
                if whatsapp_status == 200:
                    r.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True, "locale": "cs", "number": MOCK_NUMBER}))
                else:
                    r.fulfill(status=whatsapp_status, content_type="application/json", body=json.dumps({"ok": False}))
            elif url.path == "/api/request-proposal":
                self.posts.append(json.loads(r.request.post_data))
                r.fulfill(status=200, content_type="application/json", body=json.dumps({"ok": True}))
            else:
                r.continue_()

        context.route("**/*", route)
        page = context.new_page()
        page.goto(self.base_url + path, wait_until="networkidle")
        if consent and page.locator("[data-cookie-reject]").is_visible():
            page.locator("[data-cookie-reject]").click()
        return page

    def fill(self, page, phone=None):
        form = page.locator("[data-proposal-form]")
        form.locator('[name="name"]').fill("Jana Nováková")
        form.locator('[name="company"]').fill("Acme Travel s.r.o.")
        form.locator('[name="email"]').fill("jana@example.invalid")
        form.locator('[name="destination"]').select_option("Antalya")
        form.locator('[name="group_size"]').select_option("51–100")
        form.locator('[name="project_type"]').select_option("Incentive Travel")
        form.locator('[name="date_start"]').fill("2027-03-12")
        form.locator('[name="date_end"]').fill("2027-03-15")
        if phone:
            form.locator('[name="phone"]').fill(phone)
        return form

    def submit(self, page):
        page.locator("[data-proposal-form] button[type=submit]").click()

    def test_czech_submission_payload_and_whatsapp_thank_you(self):
        page = self.open(CS)
        form = self.fill(page, phone="+420 777 123 456")
        self.submit(page)
        dialog = page.locator("dialog.success-modal")
        expect(dialog).to_be_visible()
        self.assertEqual(len(self.posts), 1)
        payload = self.posts[0]
        self.assertEqual((payload["locale"], payload["source_page"], payload["lead_source"]), ("cs", CS, "CS / Czech"))
        self.assertRegex(payload["reference"], r"^CS-\d{6}-[A-HJ-NP-Z2-9]{4}$")
        self.assertEqual(payload["phone"], "+420 777 123 456")
        self.assertEqual(payload["submission_page"], self.base_url + CS)
        expect(dialog.locator("h2")).to_have_text("Děkujeme!")
        expect(dialog).to_contain_text("Pro rychlejší vyřízení nás můžete okamžitě kontaktovat na WhatsApp")
        link = dialog.get_by_role("link", name="Napsat na WhatsApp")
        parts = urlsplit(link.get_attribute("href"))
        self.assertEqual((parts.netloc, parts.path), ("wa.me", "/" + MOCK_NUMBER))
        message = parse_qs(parts.query)["text"][0]
        self.assertTrue(link.get_attribute("href").startswith("https://wa.me/%s?text=Dobr" % MOCK_NUMBER))
        for needle in ("Dobrý den", "Jméno: Jana Nováková", "Společnost: Acme Travel s.r.o.", "Antalya", "51–100",
                       "12. 3. 2027 – 15. 3. 2027", "Incentivní cesta", "Referenční číslo: " + payload["reference"]):
            self.assertIn(needle, message, needle)
        self.assertEqual(link.get_attribute("target"), "_blank")
        self.assertIn("noopener", link.get_attribute("rel"))
        # No automatic redirect or popup: only the visible button.
        url_before = page.url
        page.wait_for_timeout(1500)
        self.assertEqual(page.url, url_before)
        self.assertEqual(len(page.context.pages), 1)
        self.assertEqual(self.whatsapp_hits, ["locale=cs", "locale=cs"][:len(self.whatsapp_hits)])
        self.assertEqual(self.external, [])

    def test_untouched_phone_is_not_sent_and_prefix_behaves(self):
        page = self.open(CS)
        phone = page.locator('[name="phone"]')
        phone.focus()
        self.assertEqual(phone.input_value(), "+420 ")
        page.locator('[name="name"]').focus()
        self.assertEqual(phone.input_value(), "")
        self.fill(page)
        self.submit(page)
        expect(page.locator("dialog.success-modal")).to_be_visible()
        self.assertEqual(self.posts[0]["phone"], "")

    def test_czech_validation_messages(self):
        page = self.open(CS)
        messages = page.evaluate("""() => {
            const f = document.querySelector('[data-proposal-form]');
            const out = {};
            f.elements.name.checkValidity(); out.required = f.elements.name.validationMessage;
            f.elements.email.value = 'x'; f.elements.email.checkValidity(); out.email = f.elements.email.validationMessage;
            f.elements.phone.value = 'abc'; f.elements.phone.checkValidity(); out.phone = f.elements.phone.validationMessage;
            return out;
        }""")
        self.assertEqual(messages["required"], "Vyplňte prosím toto pole.")
        self.assertEqual(messages["email"], "Zadejte prosím platnou e-mailovou adresu.")
        self.assertEqual(messages["phone"], "Zadejte prosím telefonní číslo ve tvaru +420 123 456 789.")
        page.locator('[name="phone"]').fill("")
        self.fill(page)
        page.locator('[name="date_end"]').fill("2027-03-01")
        self.submit(page)
        expect(page.locator("[data-proposal-error]")).to_have_text("Datum ukončení nesmí být dřívější než datum zahájení.")
        self.assertEqual(self.posts, [])

    def test_modal_without_a_number_still_confirms_without_whatsapp(self):
        page = self.open(CS, whatsapp_status=404)
        self.fill(page)
        self.submit(page)
        dialog = page.locator("dialog.success-modal")
        expect(dialog).to_be_visible()
        expect(dialog.locator("h2")).to_have_text("Děkujeme!")
        self.assertEqual(dialog.locator("[data-success-whatsapp]").count(), 0)
        self.assertNotIn("WhatsApp", dialog.text_content())
        self.assertEqual(len(self.posts), 1)

    def test_floating_button_only_on_the_czech_page(self):
        page = self.open(CS)
        button = page.locator("a.wa-float")
        expect(button).to_have_count(1)
        self.assertTrue(button.get_attribute("href").startswith("https://wa.me/%s?text=" % MOCK_NUMBER))
        self.assertIn("Dobrý den", unquote(button.get_attribute("href")))
        self.assertEqual(button.get_attribute("aria-label"), "Napsat na WhatsApp")
        broken = self.open(CS, whatsapp_status=500)
        expect(broken.locator("a.wa-float")).to_have_count(0)
        for other in ("/de/dmc-tuerkei/", "/dmc-turkey/", "/"):
            page = self.open(other)
            page.wait_for_timeout(300)
            self.assertEqual(page.locator("a.wa-float").count(), 0, other)
            self.assertEqual(self.whatsapp_hits, [], other)

    def test_german_page_still_uses_the_main_number_and_never_the_czech_endpoint(self):
        page = self.open("/de/dmc-tuerkei/")
        form = page.locator("[data-proposal-form]")
        form.locator('[name="name"]').fill("Max Muster")
        form.locator('[name="company"]').fill("Muster GmbH")
        form.locator('[name="email"]').fill("max@example.invalid")
        form.locator('[name="destination"]').select_option("Antalya")
        form.locator('[name="group_size"]').select_option("51–100")
        form.locator('[name="dates_unconfirmed"]').check()
        self.submit(page)
        dialog = page.locator("dialog.success-modal")
        expect(dialog).to_be_visible()
        href = dialog.locator("[data-success-whatsapp]").get_attribute("href")
        self.assertTrue(href.startswith("https://wa.me/%s?text=" % MAIN_NUMBER), href)
        self.assertIn("Hallo DMC Turkey Partner", unquote(href))
        self.assertEqual(self.whatsapp_hits, [])
        self.assertEqual(self.posts[0].get("locale"), None)
        self.assertEqual(self.posts[0]["lead_source"], "DE Landing")
        self.assertNotIn(REAL, page.content())
        self.assertEqual(page.locator("a.wa-float").count(), 0)

    def test_cookie_banner_is_czech_and_links_to_czech_policies(self):
        page = self.open(CS, consent=False)
        banner = page.locator(".cookie-banner")
        expect(banner).to_be_visible()
        expect(banner.locator("h2")).to_have_text("Vaše nastavení soukromí")
        expect(banner.locator("[data-cookie-reject]")).to_have_text("Odmítnout volitelnou analytiku")
        expect(banner.locator("[data-cookie-accept]")).to_have_text("Povolit volitelnou analytiku")
        self.assertEqual(banner.get_by_role("link", name="Zásady cookies").get_attribute("href"), COOKIES)
        self.assertEqual(banner.get_by_role("link", name="Zásady ochrany osobních údajů").get_attribute("href"), PRIVACY)
        english = self.open("/dmc-turkey/", consent=False)
        self.assertEqual(english.locator(".cookie-banner h2").text_content(), "Your privacy choices")

    def test_chrome_is_czech_and_mobile_has_no_overflow(self):
        page = self.open(CS)
        self.assertEqual(page.locator(".site-header__cta .btn--primary").text_content().strip(), "Poptat nabídku")
        self.assertEqual(page.locator(".site-header__cta .btn--fam").count(), 0)
        footer = page.locator(".site-footer").text_content()
        self.assertIn("Ochrana soukromí", footer)
        self.assertEqual(page.locator('.site-footer a[href="%s"]' % PRIVACY).count(), 1)
        for path in (CS, PRIVACY, COOKIES):
            for width in (320, 375, 390, 768, 1440):
                with self.subTest(path=path, width=width):
                    page = self.open(path, width=width)
                    self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width)

    def test_czech_page_does_not_start_the_fam_trip_campaign(self):
        page = self.open(CS)
        self.assertEqual(page.evaluate("document.documentElement.lang"), "cs")
        page.wait_for_timeout(500)
        self.assertEqual(page.locator("dialog.fam-popup").count(), 0)


if __name__ == "__main__":
    unittest.main()
