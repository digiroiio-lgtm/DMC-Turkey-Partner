"""Regression tests for the Fam Trip 2027 header call-to-action."""

import glob
import json
import os
import re
import shutil
import sys
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright

from test_calculator_proposal import ROOT, StaticHandler

sys.path.insert(0, str(ROOT / "tools"))
import site_header_cta  # noqa: E402

RECORDER = """
(() => {
  let current;
  Object.defineProperty(window, 'dmcPrivacy', {
    configurable: true,
    get() { return current; },
    set(value) {
      current = value;
      window.__events = [];
      value.trackEvent = (name, params) => window.__events.push({ name, params: params || {} });
    }
  });
})();
"""
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"


class HeaderCtaStaticTests(unittest.TestCase):
    def test_header_is_in_sync_on_every_page(self):
        on = json.loads((ROOT / "campaign/uk-fam-trip.json").read_text())["enabled"]
        pages = site_header_cta.pages()
        self.assertGreater(len(pages), 100)
        for path in pages:
            source = open(path, encoding="utf-8").read()
            current = os.path.relpath(path, ROOT) == "agency-fam-trip-2027/index.html"
            self.assertEqual(site_header_cta.sync(source, on, current), source, path)

    def test_order_in_the_bar_and_first_item_in_the_menu(self):
        for rel in ("index.html", "destinations/antalya/index.html", "de/dmc-tuerkei/index.html"):
            page = (ROOT / rel).read_text(encoding="utf-8")
            bar = re.search(r'<div class="site-header__cta">(.*?)</div>', page, re.S).group(1)
            hrefs = re.findall(r'href="([^"]+)"', bar)
            self.assertEqual([h.split("?")[0] for h in hrefs], ["/contact/", "/agency-fam-trip-2027/", "/request-proposal/"], rel)
            menu = re.search(r'id="primary-nav">\s*(.*?)</li>', page, re.S).group(1)
            self.assertIn('class="nav-fam-item"', menu, rel)

    def test_disabling_the_campaign_removes_the_cta(self):
        source = (ROOT / "index.html").read_text(encoding="utf-8")
        stripped = site_header_cta.sync(source, False)
        self.assertNotIn("fam-header", stripped)
        self.assertNotIn("fam-nav", stripped)
        self.assertNotIn("agency-fam-trip-2027", stripped)
        self.assertEqual(site_header_cta.sync(stripped, True), source)

    def test_landing_page_marks_the_current_page_and_is_not_tracked(self):
        page = (ROOT / "agency-fam-trip-2027/index.html").read_text(encoding="utf-8")
        self.assertIn('class="btn btn--fam" href="/agency-fam-trip-2027/" aria-current="page"', page)
        self.assertNotIn("data-fam-header", page)


class HeaderCtaBrowserTests(unittest.TestCase):
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

    def open(self, width, path="/", consent="reject"):
        context = self.browser.new_context(viewport={"width": width, "height": 800}, user_agent=UA)
        self.addCleanup(context.close)
        context.add_init_script(RECORDER)
        self.external = []

        def route(r):
            url = urlsplit(r.request.url)
            if url.netloc != urlsplit(self.base_url).netloc:
                self.external.append(r.request.url)
                r.abort()
            elif url.path == "/api/geo":
                r.fulfill(status=200, content_type="application/json", body=json.dumps({"country": "DE", "timezone": None, "bot": False}))
            else:
                r.continue_()

        context.route("**/*", route)
        page = context.new_page()
        page.goto(self.base_url + path, wait_until="networkidle")
        if page.locator("[data-cookie-reject]").is_visible():
            page.locator("[data-cookie-reject]").click()
        return page

    def test_bar_layout_and_no_overflow_at_every_width(self):
        for width in (1440, 1100, 900, 721, 720, 430, 390, 375, 361, 360, 320):
            with self.subTest(width=width):
                page = self.open(width)
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width)
                fam = page.locator(".site-header__cta .btn--fam")
                primary = page.locator(".site-header__cta .btn--primary")
                expect(primary).to_be_visible()
                if width <= 360:
                    expect(fam).to_be_hidden()
                else:
                    expect(fam).to_be_visible()
                    fam_box, primary_box = fam.bounding_box(), primary.bounding_box()
                    self.assertLess(fam_box["x"], primary_box["x"])  # sits left of the green CTA
                    self.assertLessEqual(fam_box["x"] + fam_box["width"], primary_box["x"])
                    # One row on phones: the bar must not wrap.
                    if width <= 720:
                        logo = page.locator(".site-header .site-logo").bounding_box()
                        self.assertLess(abs(fam_box["y"] - logo["y"]), 40)

    def test_desktop_label_and_phone_accessible_name(self):
        page = self.open(1440)
        expect(page.locator(".site-header__cta .btn--fam")).to_have_text(re.compile(r"Fam Trip 2027"))
        page = self.open(390)
        link = page.locator(".site-header__cta .btn--fam")
        # The label is visually hidden on phones but still gives the icon button its accessible name.
        expect(page.locator(".site-header").get_by_role("link", name="Fam Trip 2027", exact=True)).to_have_attribute(
            "href", "/agency-fam-trip-2027/?src=header")
        self.assertLess(link.bounding_box()["width"], 60)

    def test_drawer_item_is_first_and_the_drawer_still_works(self):
        page = self.open(390)
        toggle = page.locator(".site-nav__toggle")
        toggle.click()
        first = page.locator("#primary-nav > li").first
        expect(first).to_have_class("nav-fam-item")
        expect(first).to_be_visible()
        self.assertEqual(first.locator("a").get_attribute("href"), "/agency-fam-trip-2027/?src=header-menu")
        page.keyboard.press("Escape")
        expect(toggle).to_have_attribute("aria-expanded", "false")
        # Desktop never shows the drawer item.
        page = self.open(1440)
        expect(page.locator(".nav-fam-item")).to_be_hidden()

    def test_click_is_tracked_once_with_placement_and_country(self):
        # The link navigates away, so the click is intercepted to read the event from the same document.
        page = self.open(1440)
        page.evaluate("sessionStorage.setItem('dmc_fam_geo', 'DE')")
        page.locator(".site-header__cta .btn--fam").evaluate(
            "e => { e.addEventListener('click', ev => ev.preventDefault()); e.click(); }")
        events = [e for e in page.evaluate("window.__events") if e["name"] == "fam_header_click"]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["params"], {"campaign_name": "uk_fam_trip_2027", "visitor_country": "DE", "placement": "bar"})

    def test_menu_click_reports_the_menu_placement(self):
        page = self.open(390)
        page.locator(".site-nav__toggle").click()
        page.locator(".nav-fam").evaluate("e => { e.addEventListener('click', ev => ev.preventDefault()); e.click(); }")
        events = [e for e in page.evaluate("window.__events") if e["name"] == "fam_header_click"]
        self.assertEqual([e["params"]["placement"] for e in events], ["menu"])

    def test_landing_page_does_not_track_its_own_header_link(self):
        page = self.open(1440, "/agency-fam-trip-2027/")
        link = page.locator(".site-header__cta .btn--fam")
        expect(link).to_have_attribute("aria-current", "page")
        link.evaluate("e => { e.addEventListener('click', ev => ev.preventDefault()); e.click(); }")
        self.assertEqual([e for e in page.evaluate("window.__events") if e["name"] == "fam_header_click"], [])

    def test_no_external_requests(self):
        self.open(1440)
        self.assertEqual(self.external, [])


if __name__ == "__main__":
    unittest.main()
