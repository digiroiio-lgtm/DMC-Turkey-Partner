"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const handler = require("../api/request-proposal.js");

test("proposal endpoint minimises data and redacts failures", async (t) => {
  const originalFetch = global.fetch;
  const originalError = console.error;
  const originalKey = process.env.RESEND_API_KEY;
  process.env.RESEND_API_KEY = "mock-key-not-a-credential";
  let calls, logs;
  function reset(response = { ok: true, status: 200 }) {
    calls = []; logs = [];
    global.fetch = async (url, options) => { calls.push({ url, options }); return response; };
    console.error = (...args) => { logs.push(args); };
  }
  async function submit(overrides = {}, request = {}) {
    const response = {
      headers: {}, code: null, body: null,
      setHeader(key, value) { this.headers[key] = value; },
      status(code) { this.code = code; return this; },
      json(body) { this.body = body; return this; }
    };
    await handler({ method: "POST", headers: { "content-type": "application/json; charset=utf-8" },
      body: { name: "Example Person", company: "Example Company", email: "person@example.org",
        destination: "Antalya", group_size: "20", ...overrides }, ...request }, response);
    assert.equal(response.headers["Cache-Control"], "no-store");
    return response;
  }
  try {
    await t.test("retains the requested brief, drops unknown data and cleans context", async () => {
      reset();
      const res = await submit({ brief: "<script>example</script>",
        source_page: "https://dmcturkeypartner.com/services/?email=private#secret",
        landing_page: "https://outside.example.org/private",
        submission_page: "/request-proposal/?token=secret#private", timestamp: "untrusted-time",
        passport: "unknown-sensitive-field" });
      assert.equal(res.code, 200);
      assert.equal(calls.length, 1);
      const payload = JSON.parse(calls[0].options.body);
      assert.equal(calls[0].url, "https://api.resend.com/emails");
      assert.deepEqual(payload.to, ["hello@dmcturkeypartner.com"]);
      assert.equal(payload.reply_to, "person@example.org");
      assert.equal(payload.subject, "New Proposal Request");
      assert.match(payload.html, /&lt;script&gt;/);
      assert.match(payload.text, /https:\/\/dmcturkeypartner.com\/services\//);
      assert.match(payload.text, /https:\/\/dmcturkeypartner.com\/request-proposal\//);
      assert.doesNotMatch(calls[0].options.body, /email=private|secret|outside\.example|untrusted-time|unknown-sensitive-field/);
      assert.ok(calls[0].options.signal instanceof AbortSignal);
    });
    await t.test("keeps ordinary source labels and calculator routing", async () => {
      reset();
      assert.equal((await submit({ source_page: "cop31-antalya", calculator_brief: "Indicative budget" })).code, 200);
      const payload = JSON.parse(calls[0].options.body);
      assert.match(payload.text, /Source: cop31-antalya/);
      assert.equal(payload.subject, "New Calculator Proposal Request");
    });
    await t.test("rejects invalid fields before any provider request", async () => {
      for (const fields of [{ email: "email\r\nBcc: bad@example.org" }, { name: [] },
        { brief: "x".repeat(5001) }, { company: "" }]) {
        reset(); assert.equal((await submit(fields)).code, 400); assert.equal(calls.length, 0);
      }
    });
    await t.test("rejects non-JSON, arrays and oversized payloads", async () => {
      for (const [request, code] of [
        [{ headers: { "content-type": "text/plain" } }, 415],
        [{ body: [] }, 400], [{ body: { unknown: "x".repeat(25000) } }, 413]]) {
        reset(); assert.equal((await submit({}, request)).code, code); assert.equal(calls.length, 0);
      }
    });
    await t.test("honeypot returns success without delivering email", async () => {
      reset(); assert.equal((await submit({ "company-website": "bot" })).code, 200);
      assert.equal(calls.length, 0);
    });
    await t.test("does not read or log the provider error response", async () => {
      reset({ ok: false, status: 422, text() { throw new Error("must not read personal data"); } });
      assert.equal((await submit()).code, 502);
      assert.deepEqual(logs, [["request-proposal: Resend API error", 422]]);
    });
    await t.test("does not log arbitrary network error details", async () => {
      reset(); global.fetch = async () => { throw new Error("private-person@example.org mock-key-not-a-credential"); };
      assert.equal((await submit()).code, 500);
      assert.deepEqual(logs, [["request-proposal: email delivery failed"]]);
    });
    await t.test("rejects other methods without sending email", async () => {
      reset(); const res = await submit({}, { method: "GET" });
      assert.equal(res.code, 405); assert.equal(res.headers.Allow, "POST"); assert.equal(calls.length, 0);
    });
  } finally {
    global.fetch = originalFetch; console.error = originalError;
    if (originalKey === undefined) { delete process.env.RESEND_API_KEY; }
    else { process.env.RESEND_API_KEY = originalKey; }
  }
});
