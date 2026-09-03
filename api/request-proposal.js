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

  const isCalculatorLead = Boolean(fields.calculator_brief);

  return {
    subject: (isCalculatorLead ? "Calculator Lead — " : "New Proposal Request — ") + fields.company + " (" + fields.destination + ")",
    html: html,
    text: text
  };
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.status(405).json({ ok: false, error: "Method not allowed" });
    return;
  }

  const body = req.body && typeof req.body === "object" ? req.body : {};

  // Honeypot: bots fill hidden fields. Report success without sending mail
  // or revealing that a trap was tripped.
  if (readField(body, "company-website")) {
    res.status(200).json({ ok: true });
    return;
  }

  const fields = {};
  REQUIRED_FIELDS.concat([
    "date_start",
    "date_end",
    "dates_unconfirmed",
    "project_type",
    "brief",
    "source_page",
    "landing_page",
    "submission_page",
    "timestamp",
    "calculator_brief"
  ]).forEach(function (name) {
    fields[name] = readField(body, name);
  });

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
      const errorBody = await resendResponse.text().catch(function () { return ""; });
      console.error("request-proposal: Resend API error", resendResponse.status, errorBody);
      res.status(502).json({ ok: false, error: "We could not send your brief. Please try again." });
      return;
    }

    res.status(200).json({ ok: true });
  } catch (err) {
    console.error("request-proposal: unexpected error sending email", err && err.message);
    res.status(500).json({ ok: false, error: "We could not send your brief. Please try again." });
  }
};
