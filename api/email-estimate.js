// Vercel Serverless Function — "Email me this estimate" (event cost calculator)
//
// POST /api/email-estimate sends the visitor the indicative budget they just
// produced on /event-cost-calculator/, and notifies hello@ of the lead.
//
// Abuse resistance: this endpoint mails an address the visitor types, so it
// must never become a way to send arbitrary text from our domain. The email
// is built only from allowlisted labels (destinations, programme types,
// budget lines) and bounded integers; no free text from the request reaches
// it. Consent is required, a honeypot field silently drops bots, and each IP
// gets a small number of sends per warm instance.
"use strict";

const TO_ADDRESS = "hello@dmcturkeypartner.com";
const FROM_ADDRESS = "DMC Turkey Partner <hello@dmcturkeypartner.com>";
const RESEND_ENDPOINT = "https://api.resend.com/emails";
const SITE = "https://dmcturkeypartner.com";
const EMAIL_PATTERN = /^[^\s@]{1,64}@[^\s@]{1,190}\.[^\s@]{2,24}$/;

// Mirrors the CONFIG labels in assets/js/calculator.js.
const DESTINATIONS = { antalya: "Antalya", belek: "Belek", istanbul: "Istanbul", bodrum: "Bodrum", cappadocia: "Cappadocia" };
const EVENT_TYPES = {
  "corporate-event": "Corporate Event", incentive: "Incentive Programme", conference: "Conference",
  congress: "Congress / Association Event", "corporate-retreat": "Corporate Retreat / Offsite",
  "product-launch": "Product Launch", "brand-experience": "Brand Experience", "gala-event": "Gala / Special Event"
};
const ACCOMMODATION = { "4-star": "4-Star", "5-star": "5-Star", luxury: "Luxury" };
const LEVELS = { essential: "Essential", premium: "Premium", signature: "Signature" };
const LINE_LABELS = new Set([
  "Accommodation", "Transportation & Airport Transfers", "Food & Beverage / Hosted Functions",
  "Meeting / Conference Facilities", "Activities & Experiences", "AV / Production", "Gala / Special Event",
  "Entertainment", "Local Operations & DMC Coordination", "Private dining", "Group activities",
  "VIP transportation", "Exclusive venue", "Airport transfers (premium fleet)", "Branding / event production",
  "Meeting / conference facilities", "AV / production", "Gala / special event"
]);

const MAX_PER_IP = 5;
const WINDOW_MS = 60 * 60 * 1000;
const sends = new Map();

function escapeHtml(value) {
  return String(value == null ? "" : value).replace(/[&<>"']/g, function (char) {
    return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[char];
  });
}

function int(value, min, max) {
  const n = Number(value);
  return Number.isInteger(n) && n >= min && n <= max ? n : null;
}

function band(value, max) {
  if (!Array.isArray(value) || value.length !== 2) { return null; }
  const low = int(value[0], 0, max);
  const high = int(value[1], 0, max);
  return low !== null && high !== null && low <= high ? [low, high] : null;
}

function money(n) {
  return "€" + n.toLocaleString("en-US");
}

function range(b) {
  return money(b[0]) + " – " + money(b[1]);
}

// Returns a clean estimate, or null when anything is outside the allowlist.
function validate(body) {
  const s = body.state || {};
  const e = body.estimate || {};
  const est = {
    destination: DESTINATIONS[s.destination],
    eventType: EVENT_TYPES[s.eventType],
    accommodation: ACCOMMODATION[s.accommodation],
    level: LEVELS[s.programmeLevel],
    guests: int(s.guests, 1, 5000),
    nights: int(s.nights, 1, 30),
    gala: s.gala === true,
    total: band(e.total, 50000000),
    perGuest: band(e.perGuest, 1000000),
    lines: []
  };
  if (!est.destination || !est.eventType || !est.accommodation || !est.level ||
      est.guests === null || est.nights === null || !est.total || !est.perGuest) {
    return null;
  }
  const lines = Array.isArray(e.components) ? e.components.slice(0, 16) : [];
  for (const line of lines) {
    const b = band(line && line.band, 50000000);
    if (!line || !LINE_LABELS.has(line.label) || !b) { return null; }
    est.lines.push({ label: line.label, band: b });
  }
  return est;
}

function summary(est) {
  return [
    ["Destination", est.destination],
    ["Programme", est.eventType],
    ["Guests", String(est.guests)],
    ["Duration", est.nights + (est.nights === 1 ? " night" : " nights")],
    ["Accommodation", est.accommodation],
    ["Programme level", est.level],
    ["Gala / special event", est.gala ? "Included" : "Not included"]
  ];
}

function visitorEmail(est) {
  const proposal = SITE + "/request-proposal/?src=calculator-email&destination=" + encodeURIComponent(est.destination);
  const rows = summary(est);
  const html =
    "<p>Here is the indicative budget you created with the DMC Turkey Partner event cost calculator.</p>" +
    "<h2 style=\"margin:16px 0 4px\">" + escapeHtml(range(est.total)) + "</h2>" +
    "<p style=\"margin:0 0 16px\">" + escapeHtml(range(est.perGuest)) + " per guest</p>" +
    "<table cellpadding=\"4\">" + rows.map(function (r) {
      return "<tr><td><strong>" + escapeHtml(r[0]) + "</strong></td><td>" + escapeHtml(r[1]) + "</td></tr>";
    }).join("") + "</table>" +
    (est.lines.length ? "<h3>Estimated budget breakdown</h3><table cellpadding=\"4\">" + est.lines.map(function (l) {
      return "<tr><td>" + escapeHtml(l.label) + "</td><td>" + escapeHtml(range(l.band)) + "</td></tr>";
    }).join("") + "</table>" : "") +
    "<p>Indicative planning estimate only. Final programme pricing depends on travel dates, availability, hotel and " +
    "venue selection, programme scope, production requirements and supplier confirmation.</p>" +
    "<p><a href=\"" + escapeHtml(proposal) + "\">Turn this estimate into a tailored proposal</a> — we reply within 1 business day.</p>" +
    "<p>DMC Turkey Partner · ANTALYA GOLF MCD TRAVEL, TÜRSAB no. 12434 · Antalya, Türkiye</p>";
  const text =
    "Your indicative budget: " + range(est.total) + " (" + range(est.perGuest) + " per guest)\n\n" +
    rows.map(function (r) { return r[0] + ": " + r[1]; }).join("\n") +
    (est.lines.length ? "\n\nEstimated budget breakdown:\n" + est.lines.map(function (l) { return l.label + ": " + range(l.band); }).join("\n") : "") +
    "\n\nIndicative planning estimate only, not a quotation.\n" +
    "Turn it into a tailored proposal (we reply within 1 business day): " + proposal + "\n\n" +
    "DMC Turkey Partner · ANTALYA GOLF MCD TRAVEL, TÜRSAB no. 12434 · Antalya, Türkiye";
  return { subject: "Your event budget estimate: " + est.destination + ", " + est.guests + " guests", html: html, text: text };
}

function leadEmail(est, email, country) {
  const rows = [["Email", email]].concat(summary(est), [
    ["Estimate", range(est.total)], ["Per guest", range(est.perGuest)], ["Visitor country (IP)", country || "—"]
  ]);
  return {
    subject: "Calculator Estimate Lead — " + est.destination + ", " + est.guests + " guests",
    html: "<h2>Estimate emailed to visitor</h2><table>" + rows.map(function (r) {
      return "<tr><td><strong>" + escapeHtml(r[0]) + "</strong></td><td>" + escapeHtml(r[1]) + "</td></tr>";
    }).join("") + "</table><p>The visitor consented to one follow-up about this programme.</p>",
    text: rows.map(function (r) { return r[0] + ": " + r[1]; }).join("\n")
  };
}

function rateLimited(ip, now) {
  const recent = (sends.get(ip) || []).filter(function (t) { return now - t < WINDOW_MS; });
  if (recent.length >= MAX_PER_IP) { sends.set(ip, recent); return true; }
  recent.push(now);
  sends.set(ip, recent);
  return false;
}

async function send(apiKey, message) {
  const response = await fetch(RESEND_ENDPOINT, {
    method: "POST",
    headers: { Authorization: "Bearer " + apiKey, "Content-Type": "application/json" },
    body: JSON.stringify(message)
  });
  if (!response.ok) {
    const detail = await response.text().catch(function () { return ""; });
    throw new Error("Resend " + response.status + " " + detail.slice(0, 200));
  }
}

async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    res.status(405).json({ ok: false, error: "Method not allowed" });
    return;
  }
  const body = req.body && typeof req.body === "object" ? req.body : {};
  if (typeof body["company-website"] === "string" && body["company-website"].trim()) {
    res.status(200).json({ ok: true });
    return;
  }
  const email = typeof body.email === "string" ? body.email.trim() : "";
  if (!EMAIL_PATTERN.test(email) || /[\r\n,;]/.test(email)) {
    res.status(400).json({ ok: false, error: "Please provide a valid email address." });
    return;
  }
  if (body.consent !== true) {
    res.status(400).json({ ok: false, error: "Please confirm you would like us to email this estimate." });
    return;
  }
  const est = validate(body);
  if (!est) {
    res.status(400).json({ ok: false, error: "Please calculate an estimate first." });
    return;
  }
  const forwarded = String((req.headers && req.headers["x-forwarded-for"]) || "").split(",")[0].trim();
  if (rateLimited(forwarded || "unknown", Date.now())) {
    res.status(429).json({ ok: false, error: "Too many requests. Please try again later." });
    return;
  }
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    console.error("email-estimate: RESEND_API_KEY is not configured");
    res.status(500).json({ ok: false, error: "Email delivery is not configured." });
    return;
  }
  const countryHeader = req.headers && req.headers["x-vercel-ip-country"];
  const country = String(Array.isArray(countryHeader) ? countryHeader[0] : countryHeader || "").toUpperCase();
  try {
    const visitor = visitorEmail(est);
    await send(apiKey, { from: FROM_ADDRESS, to: [email], reply_to: TO_ADDRESS, subject: visitor.subject, html: visitor.html, text: visitor.text });
    const lead = leadEmail(est, email, /^[A-Z]{2}$/.test(country) ? country : "");
    await send(apiKey, { from: FROM_ADDRESS, to: [TO_ADDRESS], reply_to: email, subject: lead.subject, html: lead.html, text: lead.text })
      .catch(function (err) { console.error("email-estimate: lead notification failed", err && err.message); });
    res.status(200).json({ ok: true });
  } catch (err) {
    console.error("email-estimate: send failed", err && err.message);
    res.status(502).json({ ok: false, error: "We could not send the email. Please try again." });
  }
}

module.exports = handler;
module.exports._test = { validate: validate, visitorEmail: visitorEmail, sends: sends };
