// Locale -> WhatsApp Business number routing. Server side only (files starting with "_" are not served as
// endpoints). The number is chosen by the locale of the PAGE that asks for it, never by the visitor's IP.
//
// Each entry: env = environment variable that overrides the default, fallback = number used when the variable
// is not set, page = the landing page the locale belongs to. The main-site number is not part of this map.
"use strict";

const ROUTES = {
  cs: { label: "Czech", page: "/cs/dmc-turecko/", env: "WHATSAPP_NUMBER_CS", fallback: "420774018359" }
};

function digits(value) {
  const only = String(value == null ? "" : value).replace(/[^0-9]/g, "");
  return only.length >= 8 && only.length <= 15 ? only : "";
}

function routeFor(locale) {
  const key = String(locale == null ? "" : locale).toLowerCase();
  if (!Object.prototype.hasOwnProperty.call(ROUTES, key)) { return null; }
  const route = ROUTES[key];
  const number = digits(process.env[route.env]) || digits(route.fallback);
  return { locale: key, label: route.label, page: route.page, number: number };
}

module.exports = { routeFor: routeFor, ROUTES: ROUTES };
