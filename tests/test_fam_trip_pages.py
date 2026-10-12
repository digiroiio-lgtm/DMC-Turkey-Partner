"""Regression tests for the Fam Trip search-intent pages and their internal links."""

import html as htmllib
import json
import os
import re
import shutil
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer

from playwright.sync_api import sync_playwright

from test_calculator_proposal import ROOT, StaticHandler

SITE = "https://dmcturkeypartner.com"
HUB = "antalya-fam-trips"
PROGRAMME = "antalya-fam-trip-2027"
APPLY = "agency-fam-trip-2027"
PAGES = {HUB: "/antalya-fam-trips/", PROGRAMME: "/antalya-fam-trip-2027/"}


def read(slug):
    return (ROOT / slug / "index.html").read_text(encoding="utf-8")


def visible_text(page_html):
    main = re.search(r"<main.*?</main>", page_html, re.S).group(0)
    return htmllib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main)))


class FamTripPageStaticTests(unittest.TestCase):
    def test_head_is_unique_and_indexable(self):
        seen = set()
        for slug, path in PAGES.items():
            page = read(slug)
            title = htmllib.unescape(re.search(r"<title>(.*?)</title>", page).group(1))
            description = htmllib.unescape(re.search(r'<meta name="description" content="(.*?)">', page).group(1))
            self.assertLessEqual(len(title), 65, title)
            self.assertTrue(70 <= len(description) <= 160, (slug, len(description)))
            self.assertEqual(len(re.findall(r"<h1[ >]", page)), 1)
            self.assertIn('<link rel="canonical" href="%s%s">' % (SITE, path), page)
            self.assertIn('<meta name="robots" content="index, follow">', page)
            self.assertNotIn((title, description), seen)
            seen.add((title, description))
        for other in (read(APPLY),):
            self.assertNotIn(title, other)

    def test_pages_are_listed_once_in_the_sitemap(self):
        sitemap = (ROOT / "sitemap-pages.xml").read_text()
        for path in PAGES.values():
            self.assertEqual(sitemap.count("<loc>%s%s</loc>" % (SITE, path)), 1)

    def test_json_ld_parses_and_faq_matches_visible_text(self):
        for slug in PAGES:
            page = read(slug)
            blocks = [json.loads(b) for b in re.findall(
                r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S)]
            faq = next(b for b in blocks if b.get("@type") == "FAQPage")
            text = visible_text(page)
            self.assertTrue(faq["mainEntity"])
            for question in faq["mainEntity"]:
                self.assertIn(question["name"], text)
                self.assertIn(question["acceptedAnswer"]["text"], text)

    def test_only_proven_facts_are_claimed(self):
        for slug in PAGES:
            text = visible_text(read(slug))
            self.assertEqual(re.findall(r"[€$£]\s?\d", text), [], slug)
            self.assertEqual(re.findall(r"\d+\s?%", text), [], slug)
            # 2026 may appear only in the freshness line and in the FAQ that says no 2026 programme exists.
            years = re.sub(r"Last updated:\s*October 2026|Is there a 2026 programme\?|No 2026 fam trip programme", "", text)
            self.assertEqual(re.findall(r"\b20(?:25|26)\b", years), [], slug)
            self.assertNotRegex(text, r"(?i)testimonial|guaranteed|past fam trips")
        programme = visible_text(read(PROGRAMME))
        for phrase in ("subject to confirmation", "subject to written confirmation", "January–March 2027",
                       "International flights are expected to be arranged by participants"):
            self.assertIn(phrase, programme)

    def test_internal_links_resolve_and_inbound_links_exist(self):
        for slug in PAGES:
            for href in re.findall(r'href="(/[^"#?]*)', read(slug)):
                if href.startswith("/assets/") or "." in os.path.basename(href.rstrip("/")):
                    continue
                self.assertTrue((ROOT / href.strip("/") / "index.html").exists() or href == "/", (slug, href))
        for source in ("incentive-travel-turkey", "destinations/antalya", "destinations/belek", "agency-partners",
                       "dmc-turkey-uk-agencies", "white-label-dmc-turkey"):
            self.assertIn('href="/antalya-fam-trips/"', read(source), source)
        for source in ("destinations/antalya", "destinations/belek", HUB, APPLY):
            self.assertIn('href="/antalya-fam-trip-2027/"', read(source), source)
        self.assertIn('href="/agency-fam-trip-2027/', read(PROGRAMME))
        self.assertIn('href="/agency-fam-trip-2027/', read(HUB))
        llms = (ROOT / "llms.txt").read_text()
        for path in list(PAGES.values()) + ["/agency-fam-trip-2027/"]:
            self.assertIn(SITE + path, llms)


class FamTripPageLayoutTests(unittest.TestCase):
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

    def test_no_horizontal_overflow(self):
        for path in PAGES.values():
            for width in (320, 390, 820, 1440):
                with self.subTest(path=path, width=width):
                    context = self.browser.new_context(viewport={"width": width, "height": 800})
                    self.addCleanup(context.close)
                    context.route("**/*", lambda r: r.continue_() if r.request.url.startswith(self.base_url) else r.abort())
                    page = context.new_page()
                    page.goto(self.base_url + path, wait_until="networkidle")
                    self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width)
                    self.assertEqual(page.locator("h1").count(), 1)


if __name__ == "__main__":
    unittest.main()
