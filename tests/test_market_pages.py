"""Regression tests for the UK-agency and German landing pages."""

import html as htmllib
import json
import os
import re
import shutil
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

from test_calculator_proposal import ROOT, StaticHandler

SITE = "https://dmcturkeypartner.com"
PAGES = {"uk": "dmc-turkey-uk-agencies", "de": "de/dmc-tuerkei"}


def read(slug):
    return (ROOT / slug / "index.html").read_text(encoding="utf-8")


def visible_text(page_html):
    main = re.search(r"<main.*?</main>", page_html, re.S).group(0)
    return htmllib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main)))


class MarketPageStaticTests(unittest.TestCase):
    def test_language_and_hreflang_are_reciprocal(self):
        uk, de, en = read(PAGES["uk"]), read(PAGES["de"]), read("dmc-turkey")
        self.assertIn('<html lang="en">', uk)
        self.assertIn('<html lang="de">', de)
        for page, self_url in ((de, "/de/dmc-tuerkei/"), (en, "/dmc-turkey/")):
            self.assertIn('hreflang="de" href="%s/de/dmc-tuerkei/"' % SITE, page)
            self.assertIn('hreflang="en" href="%s/dmc-turkey/"' % SITE, page)
            self.assertIn('hreflang="x-default" href="%s/dmc-turkey/"' % SITE, page)
        self.assertIn('rel="canonical" href="%s/de/dmc-tuerkei/"' % SITE, de)
        self.assertIn('rel="canonical" href="%s/dmc-turkey-uk-agencies/"' % SITE, uk)

    def test_json_ld_parses_and_faq_matches_visible_text(self):
        for slug in PAGES.values():
            page = read(slug)
            blocks = [json.loads(b) for b in re.findall(
                r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S)]
            faq = next(b for b in blocks if b.get("@type") == "FAQPage")
            text = visible_text(page)
            for question in faq["mainEntity"]:
                self.assertIn(question["name"], text)
                self.assertIn(question["acceptedAnswer"]["text"], text)

    def test_no_new_price_or_saving_claims(self):
        allowed_euro = {"€500–750", "€500–650", "€350–500"}
        for slug in PAGES.values():
            text = visible_text(read(slug))
            self.assertTrue(set(re.findall(r"€\d[\d,–]*", text)) <= allowed_euro, slug)
            self.assertEqual(re.findall(r"\d+\s?%", text), ["25 %"] if slug.startswith("de") else ["25%"])

    def test_german_page_has_german_form_with_unchanged_field_values(self):
        page = read(PAGES["de"])
        for label in ("Anfrage senden", "Ihr Name", "Geschäftliche E-Mail", "Zielort"):
            self.assertIn(label, page)
        self.assertIn('<option value="Cappadocia">Kappadokien</option>', page)
        self.assertIn('<option value="Not Confirmed Yet">', page)

    def test_pages_are_in_sitemap_and_llms(self):
        sitemap = (ROOT / "sitemap-pages.xml").read_text()
        llms = (ROOT / "llms.txt").read_text()
        for path in ("/dmc-turkey-uk-agencies/", "/de/dmc-tuerkei/"):
            self.assertIn(SITE + path, sitemap)
            self.assertIn(SITE + path, llms)


class MarketPageBrowserTests(unittest.TestCase):
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

    def setUp(self):
        self.context = self.browser.new_context(viewport={"width": 1365, "height": 900})
        self.addCleanup(self.context.close)
        self.requests, self.external, self.errors = [], [], []
        self.context.route("**/*", self.route)
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.assertEqual(self.external, [])

    def route(self, route):
        url = urlsplit(route.request.url)
        if url.netloc != urlsplit(self.base_url).netloc:
            self.external.append(route.request.url)
            route.abort()
        elif url.path == "/api/request-proposal":
            self.requests.append(route.request.post_data_json)
            route.fulfill(status=200, content_type="application/json", body='{"ok": true}')
        else:
            route.continue_()

    def open(self, slug, width=1365):
        self.page.set_viewport_size({"width": width, "height": 800})
        self.page.goto("%s/%s/" % (self.base_url, slug), wait_until="networkidle")
        if self.page.locator("[data-cookie-reject]").is_visible():
            self.page.locator("[data-cookie-reject]").click()

    def test_no_horizontal_overflow(self):
        for slug in PAGES.values():
            for width in (320, 390, 820, 1440):
                with self.subTest(slug=slug, width=width):
                    self.open(slug, width)
                    self.assertEqual(self.page.evaluate(
                        "document.documentElement.scrollWidth - document.documentElement.clientWidth"), 0)

    def test_forms_submit_with_market_attribution_and_open_the_modal(self):
        for key, lead_source in (("uk", "UK Agencies"), ("de", "DE Landing")):
            with self.subTest(page=key):
                self.requests.clear()
                self.open(PAGES[key])
                form = self.page.locator("form[data-proposal-form]")
                form.locator('[name="name"]').fill("Market Tester")
                form.locator('[name="company"]').fill("Test Company")
                form.locator('[name="email"]').fill("market@example.invalid")
                form.locator('[name="destination"]').select_option("Antalya")
                form.locator('[name="group_size"]').select_option("51–100")
                form.locator('[name="dates_unconfirmed"]').check()
                form.locator("button[type=submit]").click()
                expect(self.page.locator("dialog.success-modal")).to_be_visible()
                self.assertEqual(self.requests[0]["lead_source"], lead_source)
                self.assertEqual(self.requests[0]["destination"], "Antalya")
                self.assertEqual(self.requests[0]["group_size"], "51–100")


if __name__ == "__main__":
    unittest.main()
