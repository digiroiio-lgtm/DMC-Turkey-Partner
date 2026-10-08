// Vercel Serverless Function — proposal form → Resend
//
// Handles POST /api/request-proposal, validates and sanitizes the submitted
// brief, and delivers it to hello@dmcturkeypartner.com via the Resend REST
// API. RESEND_API_KEY is read only from the server-side environment and is
// never logged, returned to the client, or otherwise exposed.
"use strict";

const TO_ADDRESS = "hello@dmcturkeypartner.com";
const FROM_ADDRESS = "DMC Turkey Partner <hello@dmcturkeypartner.com>";
const RESEND_ENDPOINT = "https://api.resend.com/emails";

const REQUIRED_FIELDS = ["name", "company", "email", "destination", "group_size"];
const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const MAX_BODY_BYTES = 24576;
const FIELD_LIMITS = {
  name: 120, company: 200, email: 254, destination: 120, group_size: 80,
  date_start: 32, date_end: 32, dates_unconfirmed: 16, project_type: 120,
  brief: 5000, calculator_brief: 6000, source_page: 1024,
  landing_page: 1024, submission_page: 1024, lead_source: 120,
  campaign: 120, service_interest: 120, page_type: 120
};

// Context URLs must be public pages on our site. Never forward query strings,
// fragments, credentials or arbitrary third-party URLs to the mail provider.
function cleanPageContext(value, allowSourceLabel) {
  if (allowSourceLabel && /^[a-z0-9_-]{1,120}$/i.test(value)) { return value; }
  try {
    if (!/^https:\/\//i.test(value) && !/^\/(?!\/)/.test(value)) { return ""; }
    const url = new URL(value, "https://dmcturkeypartner.com");
    if (url.protocol !== "https:" || url.username || url.password || url.port ||
        !["dmcturkeypartner.com", "www.dmcturkeypartner.com"].includes(url.hostname)) {
      return "";
    }
    return "https://dmcturkeypartner.com" + url.pathname;
  } catch (_) { return ""; }
}

function escapeHtml(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, function (char) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
  });
}

// Strips characters that could be used for header/CRLF injection in any
// value that ends up in an email header (e.g. reply-to).
function sanitizeHeaderValue(value) {
  return String(value == null ? "" : value).replace(/[\r\n]+/g, " ").trim();
}

function readField(body, name) {
  const value = body ? body[name] : undefined;
  return typeof value === "string" ? value.trim() : "";
}

function buildEmail(fields) {
  const rows = [
    ["Name", fields.name],
    ["Company", fields.company],
    ["Work Email", fields.email],
    ["Destination", fields.destination],
    ["Approx. Group Size", fields.group_size],
    ["Travel/Event Start", fields.date_start || "—"],
    ["Travel/Event End", fields.date_end || "—"],
    ["Dates Not Confirmed", fields.dates_unconfirmed || "No"],
    ["Project Type", fields.project_type || "—"],
    ["Lead Source", fields.lead_source || "—"],
    ["Campaign", fields.campaign || "—"],
    ["Service Interest", fields.service_interest || "—"],
    ["Page Type", fields.page_type || "—"],
    ["Source", fields.source_page || "—"],
    ["Landing Page", fields.landing_page || "—"],
    ["Submission Page", fields.submission_page || "—"],
    ["Submitted At", fields.timestamp || new Date().toISOString()]
  ];

  const html =
    "<h2>New Proposal Request</h2>" +
    "<table>" +
    rows
      .map(function (row) {
        return "<tr><td><strong>" + escapeHtml(row[0]) + "</strong></td><td>" + escapeHtml(row[1]) + "</td></tr>";
      })
      .join("") +
    "</table>" +
    (fields.calculator_brief
      ? "<h3>Calculator Lead</h3><p>" + escapeHtml(fields.calculator_brief).replace(/\n/g, "<br>") + "</p>"
      : "") +
    (fields.brief ? "<h3>Project Brief</h3><p>" + escapeHtml(fields.brief).replace(/\n/g, "<br>") + "</p>" : "");

  const text =
    rows.map(function (row) { return row[0] + ": " + row[1]; }).join("\n") +
    (fields.calculator_brief ? "\n\nCalculator Lead:\n" + fields.calculator_brief : "") +
    (fields.brief ? "\n\nProject Brief:\n" + fields.brief : "");

  return {
    // Keep identifying details out of searchable email header metadata.
    subject: fields.calculator_brief ? "New Calculator Proposal Request" : "New Proposal Request",
    html: html,
    text: text
  };
}

module.exports = async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.status(405).json({ ok: false, error: "Method not allowed" });
    return;
  }

  const contentType = String((req.headers || {})["content-type"] || "").split(";")[0].trim().toLowerCase();
  if (contentType !== "application/json") {
    res.status(415).json({ ok: false, error: "Please submit the form as JSON." });
    return;
  }
  const body = req.body;
  if (!body || typeof body !== "object" || Array.isArray(body)) {
    res.status(400).json({ ok: false, error: "Invalid form submission." });
    return;
  }
  if (Buffer.byteLength(JSON.stringify(body), "utf8") > MAX_BODY_BYTES) {
    res.status(413).json({ ok: false, error: "Your brief is too long. Please shorten it." });
    return;
  }

  // Honeypot: bots fill hidden fields. Report success without sending mail
  // or revealing that a trap was tripped.
  if (readField(body, "company-website")) {
    res.status(200).json({ ok: true });
    return;
  }

  const fields = {};
  const invalid = Object.keys(FIELD_LIMITS).some(function (name) {
    return body[name] != null && (typeof body[name] !== "string" || body[name].length > FIELD_LIMITS[name]);
  });
  if (invalid) {
    res.status(400).json({ ok: false, error: "A form field is invalid or too long. Please check your brief." });
    return;
  }
  Object.keys(FIELD_LIMITS).forEach(function (name) {
    fields[name] = readField(body, name);
  });
  fields.source_page = cleanPageContext(fields.source_page, true);
  fields.landing_page = cleanPageContext(fields.landing_page, false);
  fields.submission_page = cleanPageContext(fields.submission_page, false);
  fields.timestamp = new Date().toISOString();

  const missing = REQUIRED_FIELDS.filter(function (name) { return !fields[name]; });
  if (missing.length) {
    res.status(400).json({ ok: false, error: "Missing required field(s): " + missing.join(", ") });
    return;
  }

  if (!EMAIL_PATTERN.test(fields.email)) {
    res.status(400).json({ ok: false, error: "Please provide a valid email address." });
    return;
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error("request-proposal: RESEND_API_KEY is not configured");
    res.status(500).json({ ok: false, error: "Email delivery is not configured." });
    return;
  }

  const { subject, html, text } = buildEmail(fields);

  try {
    const resendResponse = await fetch(RESEND_ENDPOINT, {
      method: "POST",
      signal: AbortSignal.timeout(10000),
      headers: {
        Authorization: "Bearer " + apiKey,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        from: FROM_ADDRESS,
        to: [TO_ADDRESS],
        reply_to: sanitizeHeaderValue(fields.email),
        subject: subject,
        html: html,
        text: text
      })
    });

    if (!resendResponse.ok) {
      // Upstream error bodies can contain submitted data. Log only the status.
      console.error("request-proposal: Resend API error", resendResponse.status);
      res.status(502).json({ ok: false, error: "We could not send your brief. Please try again." });
      return;
    }

    res.status(200).json({ ok: true });
  } catch (err) {
    console.error("request-proposal: email delivery failed");
    res.status(500).json({ ok: false, error: "We could not send your brief. Please try again." });
  }
};
