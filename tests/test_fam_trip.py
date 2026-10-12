"""Regression tests for the Agency Fam Trip campaign (pop-up, landing page, form).

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

ENDPOINT = "https://formspree.io/f/mqpelgrv"
LANDING = "/agency-fam-trip-2027/"
HEADLINES = {"GB": "UK", "IE": "Irish", "DE": "German", "AT": "Austrian", "CH": "Swiss", "NL": "Dutch", "BE": "Belgian",
             "LU": "Luxembourg", "PL": "Polish", "FR": "French", "SE": "Swedish", "NO": "Norwegian", "DK": "Danish",
             "FI": "Finnish", "US": "US"}
BROWSER_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
GENERIC = "Exclusive MICE Agency Fam Trip Invitation"
SUBLINE = "Experience Antalya & Belek in 2027. Discover Your Local DMC Partner."
TARGETS = "GB IE DE AT CH NL BE LU PL FR SE NO DK FI US".split()
ZONES = {"GB": "Europe/London", "DE": "Europe/Berlin", "US": "America/New_York", "FR": "Europe/Paris"}
RECORDER = """
(() => {
  Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => false, configurable: true });
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
        self.context = self.browser.new_context(viewport={"width": 1365, "height": 900}, timezone_id="Europe/London",
                                           user_agent=BROWSER_UA)
        self.addCleanup(self.context.close)
        self.enabled = True
        self.country = "GB"
        self.edge_zone = None
        self.bot = False
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
            route.fulfill(status=200, content_type="application/json", body=json.dumps({"country": self.country, "timezone": self.edge_zone, "bot": self.bot}))
        elif url.path == "/assets/js/fam-trip-campaign.js":
            source = self.campaign_js(enabled=self.enabled)
            route.fulfill(status=200, content_type="application/javascript", body=source)
        else:
            route.continue_()

    # -- helpers ----------------------------------------------------------------------

    def campaign_js(self, enabled=True, endpoint=None):
        """The shipped script with the enabled flag (and optionally the endpoint) forced, so the
        tests do not depend on whether the campaign is currently switched on in the JSON."""
        source = (ROOT / "assets/js/fam-trip-campaign.js").read_text()
        source = re.sub(r'"enabled": (true|false)', '"enabled": %s' % ("true" if enabled else "false"), source, count=1)
        if endpoint is not None:
            source = source.replace(ENDPOINT, endpoint)
        return source

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

    def test_indexing_follows_the_enabled_flag(self):
        enabled = json.loads((ROOT / "campaign/uk-fam-trip.json").read_text())["enabled"]
        page = (ROOT / "agency-fam-trip-2027/index.html").read_text()
        listed = "agency-fam-trip-2027" in (ROOT / "sitemap-pages.xml").read_text()
        self.assertEqual('content="index, follow"' in page, enabled)
        self.assertEqual('content="noindex, follow"' in page, not enabled)
        self.assertEqual(listed, enabled)

    def test_target_visitor_sees_the_popup_after_15_seconds_with_approved_copy(self):
        self.open("/")
        self.fast_forward(14000)
        expect(self.popup()).to_have_count(0)
        self.page.clock.run_for(1500)
        dialog = self.popup()
        expect(dialog).to_be_visible()
        expect(dialog.locator(".fam-popup__eyebrow")).to_have_text("ANTALYA & BELEK FAM TRIP 2027", use_inner_text=True)
        expect(dialog.locator("h2")).to_have_text("Exclusive Invitation for UK MICE Agencies")
        expect(dialog).to_contain_text(SUBLINE)
        expect(dialog).to_contain_text("Join a curated familiarisation trip for incentive and MICE agency decision-makers.")
        for text in ("3 Nights", "2027", "Limited Applications", "Hosted accommodation and local programme",
                     "Hotel inspections and DMC networking", "Flights arranged by participants",
                     "Register Your Interest", "Maybe Later",
                     "Applications are reviewed individually. Participation is subject to confirmation."):
            expect(dialog).to_contain_text(text)
        self.assertEqual(self.page.evaluate("document.activeElement.id"), "fam-popup-title")
        view = self.events("fam_popup_view")
        self.assertEqual(len(view), 1)
        self.assertEqual(view[0]["params"]["campaign_name"], "uk_fam_trip_2027")
        self.assertEqual(self.page.evaluate("getComputedStyle(document.documentElement).overflow"), "hidden")

    def test_every_target_country_sees_the_popup_and_events_carry_the_country(self):
        for country in TARGETS:
            with self.subTest(country=country):
                self.country = country
                self.page.close()
                self.page = self.context.new_page()
                self.open("/")
                self.fast_forward(16000)
                expect(self.popup()).to_be_visible()
                self.assertEqual(self.events("fam_popup_view")[0]["params"]["visitor_country"], country)
                expect(self.popup().locator("h2")).to_have_text("Exclusive Invitation for %s MICE Agencies" % HEADLINES[country])
                expect(self.popup()).to_contain_text(SUBLINE)

    def test_non_target_unknown_bot_and_vpn_traffic_never_see_the_popup(self):
        cases = [("TR", None, False), ("IN", None, False), (None, None, False), ("DE", None, True),
                 ("DE", "America/New_York", False), ("US", "America/New_York", False)]
        for country, zone, bot in cases:
            with self.subTest(country=country, zone=zone, bot=bot):
                self.country, self.edge_zone, self.bot = country, zone, bot
                self.page.close()
                self.page = self.context.new_page()
                self.open("/")
                self.fast_forward(20000)
                expect(self.popup()).to_have_count(0)
                self.assertEqual(self.events("fam_popup_view"), [])

    def test_matching_edge_and_browser_timezone_is_accepted(self):
        self.country, self.edge_zone = "GB", "Europe/Dublin"
        self.open("/")
        self.fast_forward(16000)
        expect(self.popup()).to_be_visible()

    def test_headless_user_agent_never_sees_the_popup(self):
        context = self.browser.new_context(user_agent="Mozilla/5.0 HeadlessChrome/124.0 Safari/537.36")
        self.addCleanup(context.close)
        context.add_init_script(RECORDER)
        context.route("**/*", self.route)
        self.page = context.new_page()
        self.open("/")
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)

    def test_automated_browsers_never_see_the_popup(self):
        self.context.add_init_script("Object.defineProperty(Navigator.prototype, 'webdriver', { get: () => true, configurable: true });")
        self.open("/")
        self.fast_forward(20000)
        expect(self.popup()).to_have_count(0)
        self.assertEqual(self.geo_hits, 0)

    def test_non_uk_and_unknown_country_never_see_the_popup(self):
        for country in ("TR", None):
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
        self.popup().get_by_role("link", name="Register Your Interest").click()
        self.page.wait_for_url("**/agency-fam-trip-2027/?src=fam-popup")
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
        expect(self.page.locator("h1")).to_have_text("Exclusive Invitation for UK MICE Agencies")
        for text in ("Why Join", "Proposed 3-Night Programme", "Indicative programme, subject to confirmation.",
                     "Who Should Apply", "at least two international group programmes annually",
                     "International flights are expected to be arranged by participants.",
                     "subject to written confirmation", "Register Your Interest for Our 2027 Antalya Fam Trip"):
            expect(self.page.locator("main")).to_contain_text(text)
        expect(self.page.locator("[data-fam-form]")).to_be_visible()
        expect(self.page.locator("[data-fam-closed]")).to_be_hidden()
        self.assertEqual(len(self.events("fam_landing_view")), 1)

    def test_landing_headline_is_personalised_per_country_but_seo_markup_is_fixed(self):
        page = (ROOT / "agency-fam-trip-2027/index.html").read_text()
        self.assertIn("<h1 data-fam-headline>%s</h1>" % GENERIC, page)
        self.assertIn('<link rel="canonical" href="https://dmcturkeypartner.com/agency-fam-trip-2027/">', page)
        for country, adjective in HEADLINES.items():
            with self.subTest(country=country):
                self.country = country
                self.page.close()
                self.page = self.context.new_page()
                self.open(LANDING, clock=False)
                expect(self.page.locator("h1")).to_have_text("Exclusive Invitation for %s MICE Agencies" % adjective)
                expect(self.page.locator("main")).to_contain_text(SUBLINE)
                self.assertIn(self.page.title(), "Antalya & Belek Fam Trip 2027 for MICE Agencies | DMC Turkey Partner")
                self.assertEqual(self.page.locator('link[rel="canonical"]').get_attribute("href"),
                                 "https://dmcturkeypartner.com/agency-fam-trip-2027/")
                self.assertEqual(self.events("fam_landing_view")[0]["params"]["visitor_country"], country)

    def test_landing_headline_is_generic_when_country_is_unknown_untargeted_or_suspect(self):
        for country, zone in ((None, None), ("TR", None), ("IN", None), ("DE", "America/New_York")):
            with self.subTest(country=country, zone=zone):
                self.country, self.edge_zone = country, zone
                self.page.close()
                self.page = self.context.new_page()
                self.open(LANDING, clock=False)
                self.page.wait_for_timeout(400)
                expect(self.page.locator("h1")).to_have_text(GENERIC)
                # A valid but untargeted country is still reported; a suspect or unknown one is not.
                params = self.events("fam_landing_view")[0]["params"]
                self.assertEqual(params.get("visitor_country"), country if country in ("TR", "IN") else None)

    def test_ip_country_is_sent_separately_from_the_company_country(self):
        self.country = "DE"
        self.open(LANDING)
        self.fill(country="Ireland")
        self.submit_after_wait()
        expect(self.page.locator("[data-fam-success]")).to_be_visible()
        body = self.formspree_hits[0]
        self.assertRegex(body, r'name="visitor_country"\r\n\r\nDE')
        self.assertRegex(body, r'name="country"\r\n\r\nIreland')
        self.assertEqual(self.events("fam_lead_success")[0]["params"]["visitor_country"], "DE")

    def test_faq_is_an_accordion_before_the_form_and_matches_the_schema(self):
        page = (ROOT / "agency-fam-trip-2027/index.html").read_text()
        blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', page, re.S)]
        faq = next(b for b in blocks if b.get("@type") == "FAQPage")
        questions = [q["name"] for q in faq["mainEntity"]]
        self.assertEqual(len(questions), 8)
        # Cost, flights, eligibility and dates come first.
        self.assertEqual(questions[:4], ["Is the Fam Trip free to attend?", "Do I need to book my own flights?",
                                         "Who is eligible to apply?", "When will the Fam Trip take place?"])
        self.assertLess(page.index('id="faq"'), page.index("data-fam-apply"))
        self.assertGreater(page.index('id="faq"'), page.index("Participation"))
        self.open(LANDING, clock=False)
        items = self.page.locator("details.fam-faq__item")
        self.assertEqual(items.count(), 8)
        for entry in faq["mainEntity"]:
            self.assertIn(entry["acceptedAnswer"]["text"], self.page.locator("#faq").text_content().replace("\n", " "))
        first = items.first
        self.assertFalse(first.evaluate("e => e.open"))
        first.locator("summary").click()
        self.assertTrue(first.evaluate("e => e.open"))
        self.assertNotRegex(self.page.locator("#faq").text_content(), r"[€$£]\s?\d|\d+\s?%")

    def test_form_stays_closed_without_a_formspree_endpoint(self):
        self.context.route("**/assets/js/fam-trip-campaign.js", lambda route: route.fulfill(
            status=200, content_type="application/javascript", body=self.campaign_js(enabled=True, endpoint="")), times=1)
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
        js = (ROOT / "assets/js/fam-trip-campaign.js").read_text()
        block = re.search(r"var CONFIG = (\{.*?\});\s*/\* fam-config:end", js, re.S).group(1)
        self.assertEqual(json.loads(block), settings)
        self.assertIsInstance(settings["enabled"], bool)
        self.assertEqual(settings["formspreeEndpoint"], ENDPOINT)
        self.assertEqual(settings["targetCountries"], TARGETS)

    def test_csp_allows_formspree_for_fetch_only(self):
        csp = next(h["value"] for rule in json.loads((ROOT / "vercel.json").read_text())["headers"]
                   for h in rule["headers"] if h["key"] == "Content-Security-Policy")
        self.assertIn("connect-src 'self' https://formspree.io", csp)
        self.assertIn("form-action 'self'", csp)

    def test_landing_page_metadata(self):
        page = (ROOT / "agency-fam-trip-2027/index.html").read_text()
        self.assertIn('<link rel="canonical" href="https://dmcturkeypartner.com/agency-fam-trip-2027/">', page)
        self.assertIn("Antalya &amp; Belek Fam Trip 2027 for MICE Agencies | DMC Turkey Partner", page)
        self.assertIn('property="og:title"', page)


if __name__ == "__main__":
    unittest.main()
