"""Playwright regressions for the post-submission success modal.

Run with: python3 -m unittest discover -s tests -v
The static server is local and ephemeral; proposal API responses are mocked.
"""

import json
import os
import shutil
import threading
import unittest
from functools import partial
from http.server import ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import expect, sync_playwright

from test_calculator_proposal import ROOT, StaticHandler

WHATSAPP_NUMBER = "905353998999"
WHATSAPP_MESSAGE = (
    "Hello DMC Turkey Partner, I’ve just submitted an event proposal request "
    "through your website. I’d like to discuss my requirements with your team."
)
EMAIL = "modal-check@example.invalid"


class SuccessModalTests(unittest.TestCase):
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
        self.api_requests = []
        self.pending_routes = []
        self.external_requests = []
        self.javascript_errors = []
        self.api_status = 200
        self.defer_response = False
        self.context.route("**/*", self.route_request)
        self.page = self.context.new_page()
        self.page.set_default_timeout(5000)
        self.page.on("pageerror", lambda error: self.javascript_errors.append(str(error)))

    def tearDown(self):
        for route in self.pending_routes:
            route.abort()
        self.context.unroute_all(behavior="ignoreErrors")
        self.assertEqual(self.javascript_errors, [])
        self.assertEqual(self.external_requests, [])

    def route_request(self, route):
        request = route.request
        url = urlsplit(request.url)
        if (url.scheme, url.netloc) != ("http", urlsplit(self.base_url).netloc):
            self.external_requests.append(request.url)
            route.abort()
        elif url.path == "/api/request-proposal":
            self.api_requests.append(request.post_data_json)
            if self.defer_response:
                self.pending_routes.append(route)
            else:
                self.fulfill(route)
        else:
            route.continue_()

    def fulfill(self, route):
        ok = self.api_status == 200
        body = {"ok": True} if ok else {"ok": False, "error": "We could not send your brief. Please try again."}
        route.fulfill(status=self.api_status, content_type="application/json", body=json.dumps(body))

    # -- helpers --------------------------------------------------------------

    def open_form(self, path="/request-proposal/", width=None):
        if width:
            self.page.set_viewport_size({"width": width, "height": 800})
        self.page.goto(self.base_url + path, wait_until="networkidle")
        if self.page.locator("[data-cookie-reject]").is_visible():
            self.page.locator("[data-cookie-reject]").click()
        self.events = []
        self.page.evaluate("""() => {
            window.__events = [];
            window.dmcPrivacy.trackEvent = (name, params) => window.__events.push({ name, params: params || {} });
        }""")

    def fill_form(self):
        form = self.page.locator("[data-proposal-form]")
        form.locator('[name="name"]').fill("Modal Tester")
        form.locator('[name="company"]').fill("Modal Test Company")
        form.locator('[name="email"]').fill(EMAIL)
        if form.locator('[name="destination"]').evaluate("e => e.tagName") == "SELECT":
            form.locator('[name="destination"]').select_option("Antalya")
        form.locator('[name="group_size"]').select_option("51–100")
        form.locator('[name="dates_unconfirmed"]').check()

    def submit(self):
        self.page.locator("[data-proposal-form] button[type=submit]").click()

    def events_named(self, name):
        return [e for e in self.page.evaluate("window.__events") if e["name"] == name]

    # -- tests ------------------------------------------------------------------

    def test_success_opens_modal_in_place_with_approved_copy_and_whatsapp(self):
        self.open_form()
        self.fill_form()
        self.page.locator("[data-proposal-form] button[type=submit]").scroll_into_view_if_needed()
        before_scroll = self.page.evaluate("window.scrollY")
        url_before = self.page.url
        self.submit()
        dialog = self.page.locator("dialog.success-modal")
        expect(dialog).to_be_visible()
        self.assertEqual(self.page.url, url_before)
        self.assertEqual(self.page.evaluate("window.scrollY"), before_scroll)
        expect(dialog.locator("h2")).to_have_text("Thank you!")
        expect(dialog).to_contain_text("We’ve received your brief.")
        expect(dialog).to_contain_text(
            "We will reply within 24 hours and send your side-by-side proposal within 3–5 business days.")
        expect(dialog).to_contain_text("Need a faster response?")
        expect(dialog).to_contain_text(
            "For urgent requests or a quicker discussion, you can also reach our team directly on WhatsApp.")
        expect(dialog).to_contain_text("Your request has already been submitted. No need to send it again.")
        self.assertEqual(dialog.get_attribute("aria-modal"), "true")
        self.assertEqual(dialog.get_attribute("aria-labelledby"), "success-modal-title")
        self.assertEqual(self.page.evaluate("getComputedStyle(document.documentElement).overflow"), "hidden")
        self.assertEqual(self.page.evaluate("document.activeElement.id"), "success-modal-title")
        link = dialog.get_by_role("link", name="Continue on WhatsApp")
        parts = urlsplit(link.get_attribute("href"))
        self.assertEqual((parts.netloc, parts.path), ("wa.me", "/" + WHATSAPP_NUMBER))
        self.assertEqual(parse_qs(parts.query)["text"], [WHATSAPP_MESSAGE])
        self.assertNotIn(EMAIL, link.get_attribute("href"))
        self.assertEqual(link.get_attribute("target"), "_blank")
        self.assertIn("noopener", link.get_attribute("rel"))
        self.assertEqual(link.evaluate("e => getComputedStyle(e).backgroundColor"), "rgb(37, 211, 102)")
        self.assertEqual(len(self.api_requests), 1)

    def test_escape_closes_and_back_to_website_does_not_resubmit(self):
        self.open_form()
        self.fill_form()
        self.submit()
        dialog = self.page.locator("dialog.success-modal")
        expect(dialog).to_be_visible()
        self.page.keyboard.press("Escape")
        expect(dialog).to_be_hidden()
        self.assertEqual(self.page.evaluate("getComputedStyle(document.documentElement).overflow"), "visible")
        self.assertEqual(self.events_named("success_modal_close")[0]["params"]["method"], "escape")
        button = self.page.locator("[data-proposal-form] button[type=submit]")
        expect(button).to_have_text("Brief Sent")
        expect(button).to_be_disabled()
        self.assertEqual(self.page.evaluate("document.activeElement.type"), "submit")
        self.page.locator("[data-proposal-form]").dispatch_event("submit")
        self.assertEqual(len(self.api_requests), 1)

    def test_back_to_website_and_close_button_close_the_modal(self):
        self.open_form()
        self.fill_form()
        self.submit()
        dialog = self.page.locator("dialog.success-modal")
        dialog.get_by_role("button", name="Back to Website").click()
        expect(dialog).to_be_hidden()
        self.assertEqual(len(self.api_requests), 1)
        self.assertEqual(self.events_named("success_modal_close")[0]["params"]["method"], "back_to_website")

    def test_focus_is_trapped_in_the_modal(self):
        self.open_form()
        self.fill_form()
        self.submit()
        expect(self.page.locator("dialog.success-modal")).to_be_visible()
        for _ in range(8):
            self.page.keyboard.press("Tab")
            self.assertTrue(self.page.evaluate("!!document.activeElement.closest('dialog.success-modal')"))

    def test_api_failure_never_shows_success_and_retry_works(self):
        self.open_form()
        self.fill_form()
        self.api_status = 502
        self.submit()
        expect(self.page.locator("[data-proposal-error]")).to_be_visible()
        expect(self.page.locator("dialog.success-modal")).to_have_count(0)
        self.assertEqual(self.events_named("generate_lead"), [])
        self.assertEqual(self.page.locator('[name="email"]').input_value(), EMAIL)
        expect(self.page.locator("[data-proposal-form] button[type=submit]")).to_be_enabled()
        self.api_status = 200
        self.submit()
        expect(self.page.locator("dialog.success-modal")).to_be_visible()
        self.assertEqual(len(self.api_requests), 2)
        self.assertEqual(len(self.events_named("generate_lead")), 1)

    def test_double_click_sends_one_request(self):
        self.open_form()
        self.fill_form()
        self.defer_response = True
        button = self.page.locator("[data-proposal-form] button[type=submit]")
        button.dblclick()
        expect(button).to_have_text("Sending…")
        expect(button).to_be_disabled()
        self.page.locator("[data-proposal-form]").dispatch_event("submit")
        self.assertEqual(len(self.api_requests), 1)
        expect(self.page.locator("dialog.success-modal")).to_have_count(0)
        self.fulfill(self.pending_routes.pop())
        expect(self.page.locator("dialog.success-modal")).to_be_visible()
        self.assertEqual(len(self.api_requests), 1)
        self.assertEqual(len(self.events_named("generate_lead")), 1)

    def test_analytics_events_fire_once_and_carry_no_personal_data(self):
        self.open_form()
        self.fill_form()
        self.submit()
        dialog = self.page.locator("dialog.success-modal")
        expect(dialog).to_be_visible()
        dialog.get_by_role("link", name="Continue on WhatsApp").evaluate(
            "e => { e.addEventListener('click', ev => ev.preventDefault()); e.click(); }")
        dialog.get_by_role("button", name="Close").click()
        expect(dialog).to_be_hidden()
        self.page.wait_for_function("window.__events.some(e => e.name === 'success_modal_close')")
        events = self.page.evaluate("window.__events")
        names = [e["name"] for e in events]
        for name in ("generate_lead", "success_modal_view", "whatsapp_click_after_lead", "success_modal_close"):
            self.assertEqual(names.count(name), 1, name)
        serialized = json.dumps(events)
        for secret in (EMAIL, "Modal Tester", "Modal Test Company", WHATSAPP_NUMBER):
            self.assertNotIn(secret, serialized)

    def test_modal_fits_narrow_screens(self):
        for width in (320, 375, 390, 430):
            with self.subTest(width=width):
                self.api_requests.clear()
                self.open_form(width=width)
                self.fill_form()
                self.submit()
                dialog = self.page.locator("dialog.success-modal")
                expect(dialog).to_be_visible()
                box = dialog.bounding_box()
                self.assertGreaterEqual(box["x"], 0)
                self.assertLessEqual(box["x"] + box["width"], width)
                self.assertLessEqual(box["y"] + box["height"], 800)
                self.assertEqual(self.page.evaluate(
                    "document.documentElement.scrollWidth - document.documentElement.clientWidth"), 0)
                for selector in (".success-modal__whatsapp", ".success-modal__back", ".success-modal__close"):
                    target = dialog.locator(selector).bounding_box()
                    self.assertGreaterEqual(target["height"], 44, selector)
                    self.assertGreaterEqual(target["x"], box["x"])
                    self.assertLessEqual(target["x"] + target["width"], box["x"] + box["width"])
                    self.assertGreaterEqual(target["width"], 44, selector)
                self.assertGreater(dialog.locator(".success-modal__whatsapp").bounding_box()["width"], width * 0.6)

    def test_origin_page_param_is_src_and_legacy_source_still_works(self):
        for query, expected in (("?src=venue-sourcing", "venue-sourcing"), ("?source=hotel-sourcing", "hotel-sourcing"), ("", "direct")):
            with self.subTest(query=query):
                self.open_form("/request-proposal/" + query)
                self.assertEqual(self.page.locator('[name="source_page"]').input_value(), expected)
        self.page.goto(self.base_url + "/services/venue-sourcing/", wait_until="networkidle")
        href = self.page.locator('a[href^="/request-proposal/?"]').first.get_attribute("href")
        self.assertIn("src=", href)
        self.assertNotRegex(href, r"[?&]source=")

    def test_off_season_form_uses_the_modal(self):
        self.open_form("/off-season-events-turkey/belek/")
        self.page.locator('form[data-proposal-form] [name="name"]').fill("Modal Tester")
        self.page.locator('form[data-proposal-form] [name="company"]').fill("Modal Test Company")
        self.page.locator('form[data-proposal-form] [name="email"]').fill(EMAIL)
        self.page.locator('form[data-proposal-form] [name="group_size"]').select_option(index=2)
        self.page.locator('form[data-proposal-form] [name="dates_unconfirmed"]').check()
        self.page.locator("form[data-proposal-form] button[type=submit]").click()
        expect(self.page.locator("dialog.success-modal")).to_be_visible()
        self.assertEqual(self.api_requests[0]["destination"], "Belek")

    def test_inline_fallbacks_remain(self):
        # The transfer-quote form keeps its own inline thank-you.
        self.open_form("/antalya-transfer-prices/")
        expect(self.page.locator("[data-proposal-form]")).to_have_attribute("data-success-inline", "")
        # No dialog support: the inline thank-you section is used instead of a modal.
        self.context.add_init_script("delete HTMLDialogElement.prototype.showModal;")
        self.page = self.context.new_page()
        self.page.on("pageerror", lambda error: self.javascript_errors.append(str(error)))
        self.open_form()
        self.fill_form()
        self.submit()
        expect(self.page.locator("[data-proposal-success]")).to_be_visible()
        expect(self.page.locator("dialog.success-modal")).to_have_count(0)
        expect(self.page.locator("[data-proposal-form]")).to_be_hidden()
        self.assertEqual(len(self.events_named("generate_lead")), 1)


if __name__ == "__main__":
    unittest.main()
