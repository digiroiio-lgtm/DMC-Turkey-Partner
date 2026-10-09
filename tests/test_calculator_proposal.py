"""Playwright regressions for calculator navigation and proposal state lifetime.

Run with: python3 -m unittest discover -s tests -v
The static server is local and ephemeral. All proposal API responses are mocked;
these tests never send mail or require Vercel credentials.
"""

import json
import os
import re
import shutil
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SESSION_KEY = "dtp_calculator_state"
HEADERS = json.loads((ROOT / "vercel.json").read_text())["headers"]


class StaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def end_headers(self):
        # Keep the deployed CSP active, including its restriction on eval().
        for rule in HEADERS:
            if re.fullmatch(rule["source"], urlsplit(self.path).path):
                for header in rule["headers"]:
                    self.send_header(header["key"], header["value"])
        super().end_headers()


class CalculatorProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(
            ("127.0.0.1", 0), partial(StaticHandler, directory=str(ROOT))
        )
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
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
        self.pending_routes.clear()
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
            self.assertEqual(request.method, "POST")
            self.assertEqual(request.headers["content-type"], "application/json")
            self.api_requests.append(request.post_data_json)
            if self.defer_response:
                self.pending_routes.append(route)
            else:
                self.fulfill_proposal(route, self.api_status)
        else:
            route.continue_()

    @staticmethod
    def fulfill_proposal(route, status):
        body = {"ok": True} if status == 200 else {
            "ok": False, "error": "We could not send your brief. Please try again."
        }
        route.fulfill(status=status, content_type="application/json", body=json.dumps(body))

    def stored_estimate(self):
        return self.page.evaluate("key => JSON.parse(sessionStorage.getItem(key))", SESSION_KEY)

    def calculate(self):
        self.page.goto(self.base_url + "/event-cost-calculator/", wait_until="networkidle")
        if self.page.locator("[data-cookie-reject]").is_visible():
            self.page.locator("[data-cookie-reject]").click()
        for selector, value in [
            ("destination", "antalya"), ("event-type", "corporate-event"),
            ("accommodation", "5-star"), ("programme", "premium")
        ]:
            self.page.locator(f"[data-calc-{selector}]").select_option(value)
        self.page.locator("[data-calc-guests]").fill("100")
        self.page.locator("[data-calc-nights]").fill("3")
        self.page.locator("[data-calc-gala]").uncheck()
        self.page.get_by_role("button", name="Calculate My Budget", exact=True).click()
        expect(self.page.locator("[data-calc-results]")).to_be_visible()
        self.assertEqual(self.stored_estimate()["result"]["total"], [66000, 80500])

    def open_proposal(self):
        self.calculate()
        self.page.locator("[data-calc-proposal-cta]").click()
        self.page.wait_for_url(self.base_url + "/request-proposal/")
        expect(self.page.locator("[data-calculator-summary]")).to_be_visible()
        return self.stored_estimate()

    def fill_contact(self):
        self.page.locator('[name="name"]').fill("Regression check")
        self.page.locator('[name="company"]').fill("Local test company")
        self.page.locator('[name="email"]').fill("test@example.invalid")

    def assert_restored_estimate(self, estimate):
        self.assertEqual(self.stored_estimate(), estimate)
        self.page.reload(wait_until="networkidle")
        expect(self.page.locator("[data-calculator-summary]")).to_be_visible()
        self.assertEqual(self.stored_estimate(), estimate)
        self.assertEqual(self.page.locator('[name="calculator_brief"]').input_value(), estimate["brief"])
        self.assertEqual(self.page.locator('[name="destination"]').input_value(), "Antalya")
        self.assertEqual(self.page.locator('[name="group_size"]').input_value(), "51–100")
        expect(self.page.locator("[data-calculator-summary]")).to_contain_text("€66,000 – €80,500")

    def test_first_proposal_click_after_editing_guests(self):
        self.calculate()
        guests = self.page.locator("[data-calc-guests]")
        guests.fill("200")
        expect(guests).to_be_focused()
        expect(self.page.locator(".calc__figure")).to_have_text("€132,000 – €161,000")
        self.assertEqual(self.stored_estimate()["result"]["total"], [132000, 161000])

        # One real pointer click, with no pre-blur, retry or forced navigation.
        self.page.locator("[data-calc-proposal-cta]").click()
        self.page.wait_for_url(self.base_url + "/request-proposal/")
        expect(self.page.locator("[data-calculator-summary]")).to_be_visible()
        expect(self.page.locator("[data-calculator-summary]")).to_contain_text("200 guests")
        expect(self.page.locator("[data-calculator-summary]")).to_contain_text("€132,000 – €161,000")
        self.assertEqual(self.page.locator('[name="group_size"]').input_value(), "101–250")
        self.assertEqual(self.page.locator('[name="calculator_brief"]').input_value(), self.stored_estimate()["brief"])
        self.assertEqual(self.api_requests, [])

    def test_invalid_dates_preserve_estimate_after_reload(self):
        for reversed_dates in (False, True):
            with self.subTest(reversed_dates=reversed_dates):
                estimate = self.open_proposal()
                self.fill_contact()
                if reversed_dates:
                    self.page.locator('[name="date_start"]').fill("2026-11-03")
                    self.page.locator('[name="date_end"]').fill("2026-11-01")
                self.page.get_by_role("button", name="Send My Brief", exact=True).click()
                message = "End date must be on or after the start date." if reversed_dates else (
                    "Please enter your travel or event dates, or select Dates Not Confirmed."
                )
                expect(self.page.locator("[data-proposal-error]")).to_have_text(message)
                self.assertEqual(self.api_requests, [])
                self.assert_restored_estimate(estimate)

    def test_failed_delivery_preserves_estimate_for_successful_retry(self):
        estimate = self.open_proposal()
        self.fill_contact()
        self.page.locator('[name="dates_unconfirmed"]').check()
        self.api_status = 502
        self.page.get_by_role("button", name="Send My Brief", exact=True).click()
        expect(self.page.locator("[data-proposal-error]")).to_be_visible()
        expect(self.page.get_by_role("button", name="Send My Brief", exact=True)).to_be_enabled()
        self.assertEqual(len(self.api_requests), 1)
        self.assertEqual(self.api_requests[0]["calculator_brief"], estimate["brief"])
        self.assert_restored_estimate(estimate)

        self.fill_contact()
        self.page.locator('[name="dates_unconfirmed"]').check()
        self.api_status = 200
        self.page.get_by_role("button", name="Send My Brief", exact=True).click()
        expect(self.page.locator(".success-modal")).to_be_visible()
        expect(self.page.locator("[data-proposal-success]")).to_be_hidden()
        self.assertEqual(len(self.api_requests), 2)
        self.assertEqual(self.api_requests[1]["calculator_brief"], estimate["brief"])
        self.assertIsNone(self.stored_estimate())
        self.page.reload(wait_until="networkidle")
        expect(self.page.locator("[data-calculator-summary]")).to_be_hidden()

    def test_pending_delivery_preserves_estimate_until_success(self):
        estimate = self.open_proposal()
        self.fill_contact()
        self.page.locator('[name="dates_unconfirmed"]').check()
        self.defer_response = True
        self.page.get_by_role("button", name="Send My Brief", exact=True).click()
        expect(self.page.get_by_role("button", name="Sending…", exact=True)).to_be_disabled()
        expect(self.page.locator("[data-proposal-form]")).to_be_visible()
        expect(self.page.locator(".success-modal")).to_have_count(0)
        self.assertEqual(len(self.pending_routes), 1)
        self.assertEqual(self.stored_estimate(), estimate)
        self.fulfill_proposal(self.pending_routes.pop(), 200)
        expect(self.page.locator(".success-modal")).to_be_visible()
        self.assertIsNone(self.stored_estimate())


if __name__ == "__main__":
    unittest.main()
