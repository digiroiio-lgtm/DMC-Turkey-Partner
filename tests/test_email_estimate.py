"""Regressions for the calculator "Email me this estimate" lead magnet.

1. Browser: the form posts only allowlisted selections and computed numbers,
   requires consent, reports success, and never calls an external host.
2. Server (api/email-estimate.js, run with node): rejects missing consent,
   bad email, unknown labels and out-of-range numbers; honeypot is silently
   accepted; a valid request sends exactly two emails through a mocked Resend.

Run with: python3 -m unittest discover -s tests -v
"""

import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

from playwright.sync_api import expect

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_calculator_proposal as _calc  # noqa: E402

# Keep the base class out of this module's namespace so test discovery does
# not run the calculator suite a second time.
_base = _calc.CalculatorProposalTests
ROOT = _calc.ROOT


class EmailEstimateBrowserTests(unittest.TestCase):
    # Reuse the calculator test harness (static server with the deployed CSP,
    # Playwright browser, external-request guard) without re-running its tests.
    setUpClass = classmethod(_base.setUpClass.__func__)
    setUp = _base.setUp
    tearDown = _base.tearDown
    calculate = _base.calculate
    stored_estimate = _base.stored_estimate
    fulfill_proposal = staticmethod(_base.fulfill_proposal)

    def route_request(self, route):
        if route.request.url.endswith("/api/email-estimate"):
            self.api_requests.append(route.request.post_data_json)
            route.fulfill(status=self.api_status, content_type="application/json",
                          body=json.dumps({"ok": self.api_status == 200,
                                           "error": "We could not send the email. Please try again."}))
            return
        _base.route_request(self, route)

    def form(self):
        return self.page.locator("form.calc__email")

    def test_estimate_email_sends_allowlisted_payload(self):
        self.calculate()
        form = self.form()
        expect(form).to_be_visible()
        form.locator('input[name="email"]').fill("planner@example.com")
        form.get_by_role("button", name="Email Me the Estimate").click()
        expect(form.locator(".form-note")).to_contain_text("tick the box")
        self.assertEqual(self.api_requests, [])

        form.locator('input[name="consent"]').check()
        form.get_by_role("button", name="Email Me the Estimate").click()
        expect(form.locator(".form-note")).to_contain_text("Sent.")
        self.assertEqual(len(self.api_requests), 1)
        sent = self.api_requests[0]
        self.assertEqual(sent["email"], "planner@example.com")
        self.assertIs(sent["consent"], True)
        self.assertEqual(sent["state"]["destination"], "antalya")
        self.assertEqual(sent["state"]["guests"], 100)
        self.assertEqual(sent["estimate"]["total"], [66000, 80500])
        self.assertEqual(set(sent), {"email", "consent", "company-website", "state", "estimate"})

    def test_failed_send_allows_retry(self):
        self.calculate()
        self.api_status = 502
        form = self.form()
        form.locator('input[name="email"]').fill("planner@example.com")
        form.locator('input[name="consent"]').check()
        form.get_by_role("button", name="Email Me the Estimate").click()
        expect(form.locator(".form-note")).to_contain_text("could not send")
        expect(form.get_by_role("button", name="Email Me the Estimate")).to_be_enabled()


NODE_HARNESS = r"""
const handler = require(process.argv[1]);
const calls = [];
global.fetch = async (url, opts) => { calls.push(JSON.parse(opts.body)); return { ok: true, text: async () => "" }; };
process.env.RESEND_API_KEY = "test";
const base = {
  email: "planner@example.com", consent: true,
  state: { destination: "antalya", eventType: "corporate-event", accommodation: "5-star",
           programmeLevel: "premium", guests: 100, nights: 3, gala: false },
  estimate: { total: [66000, 80500], perGuest: [660, 805],
              components: [{ label: "Accommodation", band: [30000, 36000] }] }
};
async function run(body, ip) {
  let status = 0, payload = null;
  const res = { setHeader() {}, status(s) { status = s; return this; }, json(p) { payload = p; } };
  await handler({ method: "POST", body, headers: { "x-forwarded-for": ip || "1.1.1.1" } }, res);
  return { status, ok: payload && payload.ok };
}
(async () => {
  const out = {};
  out.valid = await run(base);
  out.validCalls = calls.length;
  out.subjects = calls.map(c => c.subject);
  out.visitorTo = calls[0] && calls[0].to;
  out.noConsent = await run({ ...base, consent: false });
  out.badEmail = await run({ ...base, email: "a@b.c\nbcc:x@y.z" });
  out.badLabel = await run({ ...base, estimate: { ...base.estimate, components: [{ label: "Buy now at spam.example", band: [1, 2] }] } });
  out.badDest = await run({ ...base, state: { ...base.state, destination: "<script>" } });
  out.hugeGuests = await run({ ...base, state: { ...base.state, guests: 10 ** 9 } });
  const before = calls.length;
  out.honeypot = await run({ ...base, "company-website": "http://spam" });
  out.honeypotSent = calls.length - before;
  const limited = [];
  for (let i = 0; i < 7; i++) { limited.push((await run(base, "9.9.9.9")).status); }
  out.rate = limited;
  console.log(JSON.stringify(out));
})();
"""


@unittest.skipUnless(shutil.which("node"), "node is required for the API test")
class EmailEstimateApiTests(unittest.TestCase):
    def test_validation_and_abuse_controls(self):
        result = subprocess.run(
            ["node", "-e", NODE_HARNESS, str(ROOT / "api" / "email-estimate.js")],
            capture_output=True, text=True, check=True, timeout=30,
        )
        out = json.loads(result.stdout.strip().splitlines()[-1])
        self.assertEqual(out["valid"], {"status": 200, "ok": True})
        self.assertEqual(out["validCalls"], 2)
        self.assertEqual(out["visitorTo"], ["planner@example.com"])
        self.assertTrue(out["subjects"][1].startswith("Calculator Estimate Lead"))
        for key in ("noConsent", "badEmail", "badLabel", "badDest", "hugeGuests"):
            self.assertEqual(out[key]["status"], 400, key)
        self.assertEqual(out["honeypot"], {"status": 200, "ok": True})
        self.assertEqual(out["honeypotSent"], 0)
        self.assertEqual(out["rate"], [200] * 5 + [429, 429])


if __name__ == "__main__":
    unittest.main()
