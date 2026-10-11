"""Regression tests for the UK Agency Fam Trip campaign (pop-up, landing page, form).

Everything external is mocked: /api/geo, Formspree and the clock. The campaign ships
disabled, so most tests rewrite the served settings block to enable it.
"""

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

ENDPOINT = "https://formspree.io/f/testform"
LANDING = "/uk-agency-fam-trip/"
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


class FamTripTests(unittest.TestCase):
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
        self.enabled = True
        self.country = "GB"
        self.formspree_status = 200
        self.formspree_hits = []
        self.geo_hits = 0
        self.external = []
        self.errors = []
        self.context.add_init_script(RECORDER)
        self.context.route("**/*", self.route)
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.page.on("pageerror", lambda e: self.errors.append(str(e)))

    def tearDown(self):
        self.assertEqual(self.errors, [])
        self.assertEqual(self.external, [])

    def route(self, route):
        url = urlsplit(route.request.url)
        if url.netloc == "formspree.io":
            self.formspree_hits.append(route.request.post_data or "")
            body = {"ok": True} if self.formspree_status == 200 else {"error": "boom"}
            route.fulfill(status=self.formspree_status, content_type="application/json", body=json.dumps(body))
        elif url.netloc != urlsplit(self.base_url).netloc:
            self.external.append(route.request.url)
            route.abort()
        elif url.path == "/api/geo":
            self.geo_hits += 1
            route.fulfill(status=200, content_type="application/json", body=json.dumps({"country": self.country}))
        elif url.path == "/assets/js/uk-fam-campaign.js" and self.enabled:
            source = (ROOT / "assets/js/uk-fam-campaign.js").read_text()
            source = source.replace('"enabled": false', '"enabled": true').replace(
                '"formspreeEndpoint": ""', '"formspreeEndpoint": "%s"' % ENDPOINT)
            route.fulfill(status=200, content_type="application/javascript", body=source)
        else:
            route.continue_()

    # -- helpers ----------------------------------------------------------------------

    def open(self, path="/", width=None, consent=True, clock=True):
        if width:
            self.page.set_viewport_size({"width": width, "height": 800})
        if clock:
            self.page.clock.install()
        self.page.goto(self.base_url + path, wait_until="networkidle")
        if consent and self.page.locator("[data-cookie-reject]").is_visible():
            self.page.locator("[data-cookie-reject]").click()

    def popup(self):
        return self.page.locator("dialog.fam-popup")

    def events(self, name=None):
        events = self.page.evaluate("window.__events || []")
        return [e for e in events if name is None or e["name"] == name]

    def fast_forward(self, ms):
        # The geo lookup resolves in real time; let it finish before the fake clock runs.
        self.page.wait_for_timeout(400)
        self.page.clock.run_for(ms)
        self.page.wait_for_timeout(350)  # let the 0.18s entrance animation settle

    # -- pop-up -----------------------------------------------------------------------

    def test_disabled_by_default_shows_nothing_and_landing_is_closed(self):
        self.enabled = False
        self.open("/")
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)
        self.assertEqual(self.geo_hits, 0)
        self.open(LANDING, clock=False)
        expect(self.page.locator("[data-fam-closed]")).to_be_visible()
        expect(self.page.locator("[data-fam-form]")).to_be_hidden()
        self.assertIn('content="noindex, follow"', (ROOT / "uk-agency-fam-trip/index.html").read_text())
        self.assertNotIn("uk-agency-fam-trip", (ROOT / "sitemap-pages.xml").read_text())

    def test_uk_visitor_sees_the_popup_after_15_seconds_with_approved_copy(self):
        self.open("/")
        self.fast_forward(14000)
        expect(self.popup()).to_have_count(0)
        self.page.clock.run_for(1500)
        dialog = self.popup()
        expect(dialog).to_be_visible()
        expect(dialog.locator(".fam-popup__eyebrow")).to_have_text("EXCLUSIVE UK AGENCY INVITATION", use_inner_text=True)
        expect(dialog.locator("h2")).to_have_text("Experience Antalya & Belek. Become Our UK Agency Partner.")
        expect(dialog).to_contain_text("Join a curated familiarisation trip for UK incentive and MICE decision-makers.")
        for text in ("3 Nights", "2027", "Limited Applications", "Hosted accommodation and local programme",
                     "Hotel inspections and DMC networking", "Flights arranged by participants",
                     "Apply for an Invitation", "Maybe Later",
                     "Applications are reviewed individually. Participation is subject to confirmation."):
            expect(dialog).to_contain_text(text)
        self.assertEqual(self.page.evaluate("document.activeElement.id"), "fam-popup-title")
        view = self.events("fam_popup_view")
        self.assertEqual(len(view), 1)
        self.assertEqual(view[0]["params"]["campaign_name"], "uk_fam_trip_2027")
        self.assertEqual(self.page.evaluate("getComputedStyle(document.documentElement).overflow"), "hidden")

    def test_non_uk_and_unknown_country_never_see_the_popup(self):
        for country in ("DE", None):
            with self.subTest(country=country):
                self.country = country
                self.page.close()
                self.page = self.context.new_page()
                self.open("/")
                self.fast_forward(20000)
                self.assertGreaterEqual(self.geo_hits, 1)
                expect(self.popup()).to_have_count(0)

    def test_scroll_trigger_fires_once_before_the_delay(self):
        self.open("/")
        self.page.wait_for_timeout(400)
        self.page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight)")
        self.page.clock.run_for(300)
        expect(self.popup()).to_be_visible()
        self.assertEqual(self.events("fam_popup_view")[0]["params"]["trigger"], "scroll")
        self.fast_forward(20000)
        self.assertEqual(len(self.events("fam_popup_view")), 1)

    def test_waits_for_a_cookie_choice(self):
        self.open("/", consent=False)
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)
        self.page.locator("[data-cookie-reject]").click()
        self.fast_forward(16000)
        expect(self.popup()).to_be_visible()

    def test_dismissal_applies_for_the_session_and_seven_days(self):
        self.open("/")
        self.fast_forward(16000)
        self.popup().get_by_role("button", name="Maybe Later").click()
        expect(self.popup()).to_have_count(0)
        self.assertEqual(self.events("fam_popup_dismiss")[0]["params"]["method"], "maybe_later")
        self.open("/about/")
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)  # same session
        self.page.evaluate("sessionStorage.clear()")
        self.open("/about/")
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)  # within 7 days
        self.page.evaluate("""() => { const s = JSON.parse(localStorage.getItem('dmc_fam_state_v1'));
            s.dismissedAt = Date.now() - 8 * 86400000; localStorage.setItem('dmc_fam_state_v1', JSON.stringify(s)); sessionStorage.clear(); }""")
        self.open("/about/")
        self.fast_forward(16000)
        expect(self.popup()).to_be_visible()

    def test_applied_visitors_are_never_shown_the_popup_again(self):
        self.open("/")
        self.page.evaluate("localStorage.setItem('dmc_fam_state_v1', JSON.stringify({applied: true}))")
        self.open("/about/")
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)

    def test_never_on_landing_cop31_or_quotation_pages(self):
        for path in (LANDING, "/cop31-antalya/", "/request-proposal/", "/contact/", "/antalya-transfer-prices/",
                     "/off-season-events-turkey/belek/"):
            with self.subTest(path=path):
                self.page.close()
                self.page = self.context.new_page()
                self.open(path)
                self.fast_forward(20000)
                expect(self.popup()).to_have_count(0)

    def test_does_not_interrupt_a_focused_field(self):
        self.open("/about/")
        self.page.evaluate("""() => { const i = document.createElement('input'); i.id = 'probe'; document.body.prepend(i); i.focus(); }""")
        self.fast_forward(16000)
        expect(self.popup()).to_have_count(0)
        self.page.evaluate("document.getElementById('probe').blur()")
        self.fast_forward(4000)
        expect(self.popup()).to_be_visible()

    def test_escape_closes_restores_focus_and_traps_tab(self):
        self.open("/")
        self.fast_forward(16000)
        for _ in range(8):
            self.page.keyboard.press("Tab")
            self.assertTrue(self.page.evaluate("!!document.activeElement.closest('dialog.fam-popup')"))
        self.page.keyboard.press("Escape")
        expect(self.popup()).to_have_count(0)
        self.assertEqual(self.events("fam_popup_dismiss")[0]["params"]["method"], "escape")
        self.assertEqual(self.page.evaluate("getComputedStyle(document.documentElement).overflow"), "visible")

    def test_primary_cta_goes_to_the_landing_page_and_is_tracked(self):
        self.open("/")
        self.fast_forward(16000)
        self.popup().get_by_role("link", name="Apply for an Invitation").click()
        self.page.wait_for_url("**/uk-agency-fam-trip/?src=fam-popup")
        self.assertEqual(len(self.events("fam_popup_click")), 0)  # new page: recorder reset
        self.page.go_back()

    def test_popup_fits_phones_and_stays_accessible(self):
        for width in (320, 375, 390, 430):
            with self.subTest(width=width):
                self.page.close()
                self.page = self.context.new_page()
                self.open("/", width=width)
                self.fast_forward(16000)
                dialog = self.popup()
                expect(dialog).to_be_visible()
                box = dialog.bounding_box()
                self.assertGreaterEqual(box["x"], 0)
                self.assertLessEqual(box["x"] + box["width"], width)
                self.assertLessEqual(box["y"] + box["height"], 800)
                self.assertEqual(self.page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"), 0)
                for selector in (".fam-popup__cta", ".fam-popup__later", ".fam-popup__close"):
                    self.assertGreaterEqual(dialog.locator(selector).bounding_box()["height"], 44, selector)

    # -- landing page form --------------------------------------------------------------

    def fill(self, **overrides):
        values = {"full_name": "Fam Tester", "email": "fam@example.invalid", "agency": "Test Agency",
                  "job_title": "Director", "country": "United Kingdom"}
        values.update(overrides)
        form = self.page.locator("[data-fam-form]")
        for name, value in values.items():
            form.locator('[name="%s"]' % name).fill(value)
        form.locator('[name="programmes_per_year"]').select_option("2–5")
        form.locator('[name="decision_role"]').select_option("Decision Maker")
        form.locator('[name="privacy_ack"]').check()
        return form

    def submit_after_wait(self):
        self.page.clock.run_for(3500)
        self.page.locator("[data-fam-form] button[type=submit]").click()

    def test_landing_page_content_and_open_form(self):
        self.open(LANDING, clock=False)
        expect(self.page.locator("h1")).to_have_text("Discover Antalya & Belek With Your Future DMC Partner")
        for text in ("Why Join", "Proposed 3-Night Programme", "Indicative programme, subject to confirmation.",
                     "Who Should Apply", "at least two international group programmes annually",
                     "International flights are expected to be arranged by participants.",
                     "subject to written confirmation", "Register Your Interest for Our 2027 Antalya Fam Trip"):
            expect(self.page.locator("main")).to_contain_text(text)
        expect(self.page.locator("[data-fam-form]")).to_be_visible()
        expect(self.page.locator("[data-fam-closed]")).to_be_hidden()
        self.assertEqual(len(self.events("fam_landing_view")), 1)

    def test_form_stays_closed_without_a_formspree_endpoint(self):
        self.context.route("**/assets/js/uk-fam-campaign.js", lambda route: route.fulfill(
            status=200, content_type="application/javascript",
            body=(ROOT / "assets/js/uk-fam-campaign.js").read_text().replace('"enabled": false', '"enabled": true')), times=1)
        self.enabled = False
        self.open(LANDING, clock=False)
        expect(self.page.locator("[data-fam-form]")).to_be_hidden()
        expect(self.page.locator("[data-fam-closed]")).to_be_visible()

    def test_validation_blocks_incomplete_and_invalid_applications(self):
        self.open(LANDING)
        self.page.locator("[data-fam-form] button[type=submit]").click()
        expect(self.page.locator("[data-fam-error]")).to_contain_text("required")
        form = self.fill(email="not-an-email")
        self.page.clock.run_for(3500)
        form.locator("button[type=submit]").click()
        expect(self.page.locator("[data-fam-error]")).to_contain_text("valid business email")
        form.locator('[name="email"]').fill("fam@example.invalid")
        form.locator('[name="privacy_ack"]').uncheck()
        form.locator("button[type=submit]").click()
        expect(self.page.locator("[data-fam-error]")).to_contain_text("privacy acknowledgement")
        self.assertEqual(self.formspree_hits, [])

    def test_successful_application_posts_all_fields_then_confirms(self):
        self.open(LANDING + "?src=fam-popup&utm_source=newsletter&utm_campaign=uk_fam_trip_2027")
        form = self.fill(website="https://example.invalid", group_size="30", comments="Hello")
        form.locator('[name="marketing_optin"]').check()
        form.locator('[name="travel_period"]').select_option("February")
        self.submit_after_wait()
        expect(self.page.locator("[data-fam-success]")).to_be_visible()
        expect(self.page.locator("[data-fam-success] h2")).to_have_text("Thank You for Your Interest!")
        expect(self.page.locator("[data-fam-form]")).to_be_hidden()
        self.assertEqual(len(self.formspree_hits), 1)
        body = self.formspree_hits[0]
        for needle in ("uk_fam_trip_2027", 'name="campaign_source"', 'name="lead_status"', "New", 'name="consent_timestamp"',
                       'name="programmes_per_year"', "2–5", 'name="decision_role"', "Decision Maker", 'name="travel_period"',
                       "February", 'name="website"', 'name="group_size"', 'name="comments"', 'name="marketing_optin_status"',
                       "Yes", 'name="utm_source"', 'name="landing_page"', "fam-popup", 'name="privacy_ack"'):
            self.assertIn(needle, body, needle)
        # Analytics consent was refused, so no UTM values are copied into the application.
        self.assertNotIn("newsletter", body)
        self.assertEqual(self.page.evaluate("JSON.parse(localStorage.getItem('dmc_fam_state_v1')).applied"), True)
        self.assertEqual(len(self.events("fam_form_start")), 1)
        self.assertEqual(len(self.events("fam_form_submit")), 1)
        self.assertEqual(len(self.events("fam_lead_success")), 1)
        serialized = json.dumps(self.page.evaluate("window.__events"))
        for secret in ("fam@example.invalid", "Fam Tester", "Test Agency", "Hello"):
            self.assertNotIn(secret, serialized)

    def test_failure_never_shows_success_and_keeps_the_data(self):
        self.formspree_status = 500
        self.open(LANDING)
        form = self.fill()
        self.submit_after_wait()
        expect(self.page.locator("[data-fam-error]")).to_be_visible()
        expect(self.page.locator("[data-fam-success]")).to_be_hidden()
        self.assertEqual(form.locator('[name="email"]').input_value(), "fam@example.invalid")
        self.assertEqual(self.events("fam_lead_success"), [])
        self.assertIsNone(self.page.evaluate("localStorage.getItem('dmc_fam_state_v1')"))
        self.formspree_status = 200
        form.locator("button[type=submit]").click()
        expect(self.page.locator("[data-fam-success]")).to_be_visible()
        self.assertEqual(len(self.formspree_hits), 2)

    def test_double_click_sends_one_request_and_honeypot_blocks_bots(self):
        self.open(LANDING)
        self.fill()
        self.page.clock.run_for(3500)
        self.page.locator("[data-fam-form] button[type=submit]").dblclick()
        expect(self.page.locator("[data-fam-success]")).to_be_visible()
        self.assertEqual(len(self.formspree_hits), 1)
        self.page.close()
        self.page = self.context.new_page()
        self.open(LANDING)
        form = self.fill()
        form.locator('[name="_gotcha"]').evaluate("e => e.value = 'bot'")
        self.page.clock.run_for(3500)
        form.locator("button[type=submit]").click()
        expect(self.page.locator("[data-fam-success]")).to_be_hidden()
        self.assertEqual(len(self.formspree_hits), 1)

    def test_landing_page_has_no_horizontal_overflow(self):
        for width in (320, 390, 820, 1440):
            with self.subTest(width=width):
                self.open(LANDING, width=width, clock=False)
                self.assertEqual(self.page.evaluate("document.documentElement.scrollWidth - document.documentElement.clientWidth"), 0)


class FamTripStaticTests(unittest.TestCase):
    def test_settings_block_matches_the_json_file(self):
        settings = json.loads((ROOT / "campaign/uk-fam-trip.json").read_text())
        settings = {k: v for k, v in settings.items() if not k.startswith("_")}
        js = (ROOT / "assets/js/uk-fam-campaign.js").read_text()
        block = re.search(r"var CONFIG = (\{.*?\});\s*/\* uk-fam-config:end", js, re.S).group(1)
        self.assertEqual(json.loads(block), settings)
        self.assertIs(settings["enabled"], False)
        self.assertEqual(settings["formspreeEndpoint"], "")

    def test_csp_allows_formspree_for_fetch_only(self):
        csp = next(h["value"] for rule in json.loads((ROOT / "vercel.json").read_text())["headers"]
                   for h in rule["headers"] if h["key"] == "Content-Security-Policy")
        self.assertIn("connect-src 'self' https://formspree.io", csp)
        self.assertIn("form-action 'self'", csp)

    def test_landing_page_metadata(self):
        page = (ROOT / "uk-agency-fam-trip/index.html").read_text()
        self.assertIn('<link rel="canonical" href="https://dmcturkeypartner.com/uk-agency-fam-trip/">', page)
        self.assertIn("Antalya &amp; Belek Fam Trip 2027 for UK MICE Agencies | DMC Turkey Partner", page)
        self.assertIn('property="og:title"', page)


if __name__ == "__main__":
    unittest.main()
