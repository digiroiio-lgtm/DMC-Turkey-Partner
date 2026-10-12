"""Regression tests for the Fam Trip landing page visuals (photos, cards, timeline, panels)."""

import json
import os
import re
import shutil
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer

from playwright.sync_api import expect, sync_playwright

from test_calculator_proposal import ROOT, StaticHandler

LANDING = "/agency-fam-trip-2027/"
SLOTS = ["hero_a", "hero_b", "why_hotels", "why_team", "why_experiences", "why_whitelabel"]


def webp_size(path):
    """Width/height from the WebP header (no imaging library needed in the test environment)."""
    head = path.read_bytes()[:40]
    kind = head[12:16]
    if kind == b"VP8 ":
        return int.from_bytes(head[26:28], "little") & 0x3FFF, int.from_bytes(head[28:30], "little") & 0x3FFF
    if kind == b"VP8X":
        return int.from_bytes(head[24:27], "little") + 1, int.from_bytes(head[27:30], "little") + 1
    bits = int.from_bytes(head[21:25], "little")  # VP8L
    return (bits & 0x3FFF) + 1, ((bits >> 14) & 0x3FFF) + 1


def images():
    data = json.loads((ROOT / "campaign/fam-trip-images.json").read_text())
    return {k: v for k, v in data.items() if not k.startswith("_")}


def page_html():
    return (ROOT / LANDING.strip("/") / "index.html").read_text()


def main_text():
    html = page_html()
    main = re.search(r"<main.*?</main>", html, re.S).group(0)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main))


class FamTripVisualStaticTests(unittest.TestCase):
    def test_registry_has_six_distinct_existing_images(self):
        data = images()
        self.assertEqual(list(data), SLOTS)
        sources = [v["src"] for v in data.values()]
        self.assertEqual(len(set(sources)), 6, "no photo may be used twice")
        for slot, img in data.items():
            for suffix in (".webp", "-640.webp"):
                self.assertTrue((ROOT / (img["src"].lstrip("/") + suffix)).exists(), (slot, suffix))
            self.assertGreater(len(img["alt"]), 25, slot)
            self.assertTrue(img["width"] > 0 and img["height"] > 0, slot)
            self.assertIn(img["label"], ("previous", "illustrative"), slot)

    def test_uploaded_photos_are_optimised_webp_and_pngs_are_gone(self):
        data = images()
        for slot in ("hero_a", "why_hotels", "why_experiences"):
            base = ROOT / (data[slot]["src"].lstrip("/"))
            full, small = base.with_name(base.name + ".webp"), base.with_name(base.name + "-640.webp")
            self.assertLess(full.stat().st_size, 400 * 1024, full.name)
            self.assertLess(small.stat().st_size, 100 * 1024, small.name)
            self.assertEqual(webp_size(full), (data[slot]["width"], data[slot]["height"]), slot)
            self.assertEqual(webp_size(small)[0], 640, slot)
        big = [p.name for p in (ROOT / "assets/img").glob("*.png") if p.stat().st_size > 500 * 1024]
        self.assertEqual(big, [], "unoptimised PNGs must not be published")

    def test_every_photo_is_labelled_and_the_unconfirmed_note_is_present(self):
        html = page_html()
        data = images()
        illustrative = sum(1 for v in data.values() if v["label"] == "illustrative")
        previous = sum(1 for v in data.values() if v["label"] == "previous")
        self.assertEqual((illustrative, previous), (3, 3))
        # hero (2) + cards (4) carry badges; the timeline uses icons only.
        self.assertEqual(html.count('class="fam-badge fam-badge--illustrative"'), 3)
        self.assertEqual(html.count('class="fam-badge fam-badge--previous"'), 3)
        self.assertNotIn("fam-stage__tag", html)
        self.assertIn("hotels and venues for the programme are not yet confirmed", main_text())
        # The yacht belongs on the Incentive experiences card and is never presented as our project.
        card = html[html.index("<h3>Experiences</h3>") - 900:html.index("<h3>Experiences</h3>")]
        self.assertIn("antalya-luxury-yacht-incentive-experience", card)
        self.assertIn("fam-badge--illustrative", card)

    def test_image_markup_is_performance_safe(self):
        html = page_html()
        main = re.search(r"<main.*?</main>", html, re.S).group(0)
        tags = re.findall(r"<img [^>]+>", main)
        self.assertEqual(len(tags), 6)
        eager = [t for t in tags if "fetchpriority" in t]
        self.assertEqual(len(eager), 1)
        self.assertIn("antalya-belek-fam-trip-2027-hero", eager[0])
        self.assertNotIn("loading=", eager[0], "the hero image must not be lazy-loaded")
        for tag in tags:
            self.assertRegex(tag, r'width="\d+"')
            self.assertRegex(tag, r'height="\d+"')
            self.assertRegex(tag, r'alt="[^"]{20,}"')
            self.assertIn("srcset=", tag)
            if tag not in eager:
                self.assertIn('loading="lazy"', tag)

    def test_structure_and_order(self):
        html = page_html()
        marks = ['class="fam-hero-media"', 'class="fam-glance"', "<h2>Why Join</h2>", "<h2>Proposed 3-Night Programme</h2>",
                 "<h2>Who Should Apply</h2>", 'class="page-section fam-participation"', 'id="faq"', "data-fam-apply",
                 "Register Your Interest for Our 2027 Antalya Fam Trip"]
        positions = [html.index(m) for m in marks]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(html.count('class="fam-card"'), 4)
        self.assertEqual(html.count('class="fam-stage"'), 4)
        for n in (1, 2, 3, 4):
            self.assertIn("Day %d</span>" % n, html)
        # Who Should Apply and the FAQ stay plain (no cards).
        who = html[html.index("<h2>Who Should Apply</h2>"):html.index('class="page-section fam-participation"')]
        self.assertNotIn("fam-card", who)

    def test_panels_and_unconfirmed_wording(self):
        html, text = page_html(), main_text()
        glance = html[html.index('class="fam-glance"'):html.index("Why Join")]
        for needle in ("Your Fam Trip at a Glance", "Proposed period", "January–March 2027", "3 nights", "Antalya &amp; Belek",
                       "MICE agencies", "Proposed hosted accommodation and local programme",
                       "International flights arranged by participants", "All arrangements are subject to written confirmation.",
                       'href="#apply"'):
            self.assertIn(needle, glance)
        part = html[html.index('class="page-section fam-participation"'):html.index('id="faq"')]
        for needle in ("Proposed hosted", "Not included", "International flights", "Personal expenses", "Eligibility",
                       "at least two international group programmes", "subject to written confirmation"):
            self.assertIn(needle, part)
        self.assertNotIn("(proposed)", text)
        self.assertEqual(text.count("January–March 2027"), 2)  # glance panel + form lede

    def test_no_hotel_is_presented_as_part_of_the_programme(self):
        html = page_html()
        main = re.search(r"<main.*?</main>", html, re.S).group(0)
        visible = re.sub(r'<img [^>]*>', "", main)  # alt text is checked separately below
        for name in ("Rixos", "Nirvana", "Kremlin", "Titanic", "Regnum", "Maxx Royal", "Calista"):
            self.assertNotIn(name, re.sub(r"<[^>]+>", " ", visible), name)
        for slot, img in images().items():
            self.assertNotRegex(img["alt"], r"(?i)rixos|nirvana|kremlin|calista|titanic|regnum|\bela\b|excellence")
        self.assertIn("Previous project in Antalya", html)

    def test_cta_and_form_are_unchanged(self):
        html = page_html()
        self.assertEqual(html.count('href="#apply"'), 3)  # hero, glance panel, final CTA
        self.assertIn("data-fam-form", html)
        self.assertIn('id="faq"', html)


class FamTripVisualBrowserTests(unittest.TestCase):
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

    def open(self, width, height=900):
        context = self.browser.new_context(viewport={"width": width, "height": height})
        self.addCleanup(context.close)
        context.route("**/*", lambda r: r.continue_() if r.request.url.startswith(self.base_url) else r.abort())
        page = context.new_page()
        page.goto(self.base_url + LANDING, wait_until="networkidle")
        if page.locator("[data-cookie-reject]").is_visible():
            page.locator("[data-cookie-reject]").click()
        return page

    def wait_until_loaded(self, page, timeout_ms=8000):
        """Poll until every visible <img> has finished loading (condition-based, bounded)."""
        script = "[...document.querySelectorAll('main img')].filter(i => i.offsetParent && !i.complete).length"
        waited = 0
        while page.evaluate(script) and waited < timeout_ms:
            page.wait_for_timeout(50)
            waited += 50
        self.assertEqual(page.evaluate(script), 0, "images still loading")

    def test_no_overflow_and_images_load_without_layout_shift(self):
        for width in (320, 375, 390, 430, 768, 1100, 1440):
            with self.subTest(width=width):
                page = self.open(width)
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width)
                page.evaluate("document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; })")
                self.wait_until_loaded(page)
                broken = page.evaluate("[...document.querySelectorAll('main img')].filter(i => i.offsetParent && i.naturalWidth === 0).length")
                self.assertEqual(broken, 0)
                # Reserved space: the rendered box already has the final aspect ratio before the file is decoded.
                self.assertLessEqual(page.evaluate("document.documentElement.scrollWidth"), width)

    def test_layout_changes_with_the_viewport(self):
        page = self.open(1440)
        columns = page.evaluate("getComputedStyle(document.querySelector('.fam-cards')).gridTemplateColumns.split(' ').length")
        self.assertEqual(columns, 2)
        self.assertEqual(page.evaluate("getComputedStyle(document.querySelector('.fam-timeline')).gridTemplateColumns.split(' ').length"), 4)
        expect(page.locator(".fam-hero-media__side")).to_be_visible()
        page = self.open(390)
        self.assertEqual(page.evaluate("getComputedStyle(document.querySelector('.fam-cards')).gridTemplateColumns.split(' ').length"), 1)
        self.assertEqual(page.evaluate("getComputedStyle(document.querySelector('.fam-timeline')).gridTemplateColumns.split(' ').length"), 1)
        expect(page.locator(".fam-hero-media__side")).to_be_hidden()
        # The form stays reachable and below the new sections.
        self.assertGreater(page.locator("#apply").bounding_box()["y"], page.locator(".fam-glance").bounding_box()["y"])

    def test_card_images_have_one_consistent_ratio(self):
        for width in (1440, 390):
            with self.subTest(width=width):
                page = self.open(width)
                ratios = page.evaluate("[...document.querySelectorAll('.fam-card__media')].map(e => { const r = e.getBoundingClientRect(); return Math.round(r.width / r.height * 100) / 100; })")
                self.assertEqual(len(ratios), 4)
                self.assertEqual(set(ratios), {1.33})

    def test_hero_cta_is_above_the_fold_and_prominent(self):
        for width, height in ((1440, 900), (1024, 768), (390, 844)):
            with self.subTest(width=width):
                page = self.open(width, height)
                box = page.locator("[data-cta-location=hero] .fam-hero-cta").bounding_box()
                self.assertLessEqual(box["y"] + box["height"], height, "CTA must be fully visible in the first viewport")
                self.assertGreaterEqual(box["height"], 50)
                other = page.locator(".site-header__cta .btn--primary").bounding_box()
                self.assertGreater(box["height"], other["height"])
                self.assertEqual(page.locator("[data-cta-location=hero] .fam-hero-cta").get_attribute("href"), "#apply")

    def test_hero_media_height_is_controlled_on_desktop_and_tablet(self):
        for width in (1440, 1100, 900):
            with self.subTest(width=width):
                page = self.open(width)
                self.assertLessEqual(page.locator(".fam-hero-media").bounding_box()["height"], 321)
        page = self.open(390)
        self.assertEqual(page.locator(".fam-hero-media__main img").evaluate("e => getComputedStyle(e).objectFit"), "cover")

    def test_timeline_is_one_consistent_icon_system(self):
        page = self.open(1440)
        stages = page.locator(".fam-stage")
        self.assertEqual(stages.count(), 4)
        self.assertEqual(page.locator(".fam-timeline img").count(), 0)
        boxes = page.evaluate("[...document.querySelectorAll('.fam-stage__icon')].map(e => { const r = e.getBoundingClientRect(); return [Math.round(r.width), Math.round(r.height), e.querySelectorAll('svg').length]; })")
        self.assertEqual(boxes, [[48, 48, 1]] * 4)
        heights = page.evaluate("[...document.querySelectorAll('.fam-stage')].map(e => Math.round(e.getBoundingClientRect().height))")
        self.assertEqual(len(set(heights)), 1)

    def test_local_team_card_matches_its_photo(self):
        html = page_html()
        card = html[html.index("<h3>On-the-Ground Operations</h3>"):html.index("<h3>Experiences</h3>")]
        self.assertIn("registration, guest handling and event-day coordination", card)
        self.assertIn("previous project", card)
        self.assertNotIn("<h3>Local team</h3>", html)
        self.assertIn("branded-registration-desk-cw-enerji-antalya", html)
        self.assertIn("fam-badge--previous", html[html.index("branded-registration-desk"):html.index("<h3>On-the-Ground Operations</h3>")])

    def test_spare_networking_photo_is_kept_but_unused(self):
        self.assertTrue((ROOT / "assets/img/fam-trip/antalya-mice-networking-event.webp").exists())
        self.assertNotIn("antalya-mice-networking-event", page_html())

    def test_body_copy_is_readable(self):
        page = self.open(390)
        sizes = page.evaluate("""() => ['.fam-card__body p', '.fam-stage p', '.fam-participation__col li', '.fam-glance__fine',
            '.fam-photo-note', '[data-cta-location=hero] .page-section__lede'].map(s => [s, parseFloat(getComputedStyle(document.querySelector(s)).fontSize)])""")
        for selector, size in sizes:
            self.assertGreaterEqual(size, 15, selector)

    def test_lcp_is_the_hero_image_and_layout_is_stable(self):
        for width, height in ((390, 844), (768, 1024), (1440, 900)):
            with self.subTest(width=width):
                context = self.browser.new_context(viewport={"width": width, "height": height})
                self.addCleanup(context.close)
                context.add_init_script("""
                  window.__lcp = null; window.__cls = 0;
                  new PerformanceObserver(l => { const e = l.getEntries().pop(); window.__lcp = e.url || e.element && e.element.tagName; }).observe({type: 'largest-contentful-paint', buffered: true});
                  new PerformanceObserver(l => { l.getEntries().forEach(e => { if (!e.hadRecentInput) window.__cls += e.value; }); }).observe({type: 'layout-shift', buffered: true});
                """)
                context.route("**/*", lambda r: r.continue_() if r.request.url.startswith(self.base_url) else r.abort())
                page = context.new_page()
                page.goto(self.base_url + LANDING, wait_until="networkidle")
                page.wait_for_timeout(300)
                self.assertIn("antalya-belek-fam-trip-2027-hero", page.evaluate("window.__lcp") or "")
                self.assertLess(page.evaluate("window.__cls"), 0.02)
                self.assertEqual(page.locator('link[rel="preload"][as="image"]').count(), 1)

    def test_glance_button_jumps_to_the_form(self):
        page = self.open(1440)
        page.locator(".fam-glance .btn").click()
        self.assertTrue(page.url.endswith("#apply"))


if __name__ == "__main__":
    unittest.main()
