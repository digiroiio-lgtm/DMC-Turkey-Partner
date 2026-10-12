// Returns the WhatsApp Business number for a locale-specific landing page (GET /api/whatsapp?locale=cs).
//
// The number is chosen by the locale the PAGE asks for, never by the visitor's IP address. It lives only in
// api/_whatsapp-config.js (server side) and in the WHATSAPP_NUMBER_<LOCALE> environment variable, so it is not
// part of any static HTML/JS/CSS file and cannot appear on pages that never call this endpoint. The main-site
// number is not served from here.
"use strict";

const { routeFor } = require("./_whatsapp-config");

module.exports = function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.setHeader("Allow", "GET, HEAD");
    res.status(405).json({ ok: false, error: "Method not allowed" });
    return;
  }
  const raw = req.query && req.query.locale;
  const route = routeFor(Array.isArray(raw) ? raw[0] : raw);
  if (!route) {
    res.status(404).json({ ok: false, error: "Unknown locale" });
    return;
  }
  if (!route.number) {
    res.status(404).json({ ok: false, error: "Not configured" });
    return;
  }
  res.status(200).json({ ok: true, locale: route.locale, number: route.number });
};
