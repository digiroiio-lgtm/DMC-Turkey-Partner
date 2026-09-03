/*
 * DmcTurkeyPartner.com — Turkey Event Budget Calculator
 *
 * Self-contained, embeddable indicative planning tool. Mounts on any element
 * carrying [data-calculator] and reads optional pre-population from
 * data attributes (e.g. data-destination="antalya").
 *
 * All pricing assumptions live in CONFIG below — destination coefficients,
 * event-type structures, programme levels, accommodation, transport, F&B,
 * production, activity, gala and operational cost bands. Pricing can be
 * recalibrated centrally without touching the UI code.
 *
 * Figures are deliberately presented as rounded planning ranges, never as
 * false-precision quotations.
 *
 * Session state: calculator input/result (no personal data) is kept in
 * sessionStorage under "dtp_calculator_state" so it survives page
 * navigation within the browser session, and is carried into the
 * /request-proposal/ form when the user converts.
 */
(function () {
  "use strict";

  var SESSION_KEY = "dtp_calculator_state";

  /* =======================================================================
   * 1. Central pricing configuration
   *
   * Convention: rates are [low, high] EUR per-guest-per-night ("pppn"),
   * per-guest-per-programme ("pp") or per-programme lump sums ("perProgramme").
   * =======================================================================
   */
  var CONFIG = {
    currency: "EUR",

    // Destination coefficients — relative cost level of the same programme.
    // hotel multiplies accommodation; ground multiplies transport, F&B,
    // activities, entertainment, meeting facilities and production.
    destinations: {
      antalya:    { label: "Antalya",    coefficient: 1.00, hotel: 1.00, ground: 1.00 },
      istanbul:   { label: "Istanbul",   coefficient: 1.15, hotel: 1.50, ground: 1.15 },
      bodrum:     { label: "Bodrum",     coefficient: 1.20, hotel: 1.25, ground: 1.10 },
      cappadocia: { label: "Cappadocia", coefficient: 1.10, hotel: 1.15, ground: 1.05 }
    },

    eventTypes: {
      "corporate-event":   { label: "Corporate Event" },
      "incentive":         { label: "Incentive Programme" },
      "conference":        { label: "Conference" },
      "congress":          { label: "Congress / Association Event" },
      "corporate-retreat": { label: "Corporate Retreat / Offsite" },
      "product-launch":    { label: "Product Launch" },
      "brand-experience":  { label: "Brand Experience" },
      "gala-event":        { label: "Gala / Special Event" }
    },

    // Per-guest-per-night hotel package: room (twin/double share) + breakfast,
    // plus coffee breaks and basic meeting-room use for business programmes.
    accommodation: {
      "4-star": { label: "4-Star",  pppn: [75, 95] },
      "5-star": { label: "5-Star",  pppn: [100, 130] },
      "luxury": { label: "Luxury",  pppn: [170, 230] }
    },

    // Programme level multipliers applied to the flexible cost components
    // (transport, F&B, meeting, activities, production, gala, entertainment).
    programmeLevels: {
      essential: {
        label: "Essential",
        description: "Efficient programme with quality accommodation, transport and core event requirements.",
        multipliers: { transportation: 0.8, foodBeverage: 0.8, meeting: 0.8, activities: 0.7, production: 0.7, gala: 0.8, entertainment: 0.8 }
      },
      premium: {
        label: "Premium",
        description: "Enhanced venues, experiences, F&B and production.",
        multipliers: { transportation: 1.0, foodBeverage: 1.0, meeting: 1.0, activities: 1.0, production: 1.0, gala: 1.0, entertainment: 1.0 }
      },
      signature: {
        label: "Signature",
        description: "High-end programme with premium venues, experiences, production and hospitality.",
        multipliers: { transportation: 1.3, foodBeverage: 1.4, meeting: 1.3, activities: 1.5, production: 1.6, gala: 1.5, entertainment: 1.5 }
      }
    },

    components: {
      // Private airport return transfer + in-programme transport allowance per guest.
      transportation: { pp: [100, 130] },
      // Hosted lunches, dinners and receptions, per guest per night.
      foodBeverage:   { pppn: [70, 95] },
      // Meeting / conference facilities, per guest per conference day.
      meeting:        { ppDay: [35, 55] },
      // Group experiences per guest per experience day (entry, logistics, hosting).
      activities:     { ppDay: [80, 120] },
      // Core AV / production: plenary day rate per delegate or base package + per guest.
      production:     { ppDay: [50, 85], base: [9000, 14000], pp: [25, 40] },
      // Gala / special event evening: private venue, full catering, production.
      gala:           { pp: [160, 240], base: [9000, 14000] },
      // Entertainment add-on: live acts, performers, hosted moments.
      entertainment:  { perProgramme: [5000, 9000] }
    },

    // How many conference / experience days each programme type assumes, and
    // which components it leans on. This is what makes a conference price
    // differently to an incentive or a product launch.
    eventTypeStructure: {
      "corporate-event":   { conferenceDays: 1,   experienceDays: 0.5, hostedFnsPerNight: 0.45, meeting: true,  production: false, entertainment: false },
      "incentive":         { conferenceDays: 0,   experienceDays: 1.5, hostedFnsPerNight: 0.7,  meeting: false, production: false, entertainment: false },
      "conference":        { conferenceDays: 1.5, experienceDays: 0.5, hostedFnsPerNight: 0.6,  meeting: true,  production: true,  entertainment: false },
      "congress":          { conferenceDays: 2,   experienceDays: 0,   hostedFnsPerNight: 0.5,  meeting: true,  production: true,  entertainment: false },
      "corporate-retreat": { conferenceDays: 1,   experienceDays: 1,   hostedFnsPerNight: 0.6,  meeting: true,  production: false, entertainment: false },
      "product-launch":    { conferenceDays: 0.5, experienceDays: 0.5, hostedFnsPerNight: 0.7,  meeting: true,  production: true,  entertainment: true },
      "brand-experience":  { conferenceDays: 0.5, experienceDays: 1,   hostedFnsPerNight: 0.7,  meeting: true,  production: true,  entertainment: true },
      "gala-event":        { conferenceDays: 0,   experienceDays: 0.5, hostedFnsPerNight: 0.85, meeting: false, production: true,  entertainment: true }
    },

    // Local DMC operations & coordination: on-site staffing, planning and
    // supplier management, calculated as a share of the running subtotal.
    operations: {
      share: { "corporate-event": 0.10, "incentive": 0.10, "conference": 0.10, "corporate-retreat": 0.10,
               "congress": 0.12, "product-launch": 0.13, "brand-experience": 0.13, "gala-event": 0.12 }
    },

    // Scale factor applied to fixed (per-programme) costs as headcount grows:
    // 100 guests => 1.0, 20 => 0.7, 500 => 1.25, 1000+ => 1.4 (capped).
    scale: { min: 0.7, max: 1.4, exponent: 0.3, referenceGuests: 100 },

    // Final planning range expressed as ±10% around the computed midpoint,
    // then rounded to presentable figures (never false precision).
    rangeSpread: 0.10,

    limits: { guestsMin: 10, guestsMax: 1000, nightsMin: 1, nightsMax: 10 },

    defaults: { destination: "antalya", eventType: "corporate-event", guests: 100, nights: 4, accommodation: "5-star", programmeLevel: "premium", gala: false },

    // Optional "Refine estimate" add-ons, layered on top of the base estimate.
    refinements: [
      { id: "meetingFacilities", label: "Meeting / conference facilities", kind: "component", component: "meeting" },
      { id: "avProduction",      label: "AV / production",                 kind: "component", component: "production" },
      { id: "gala",              label: "Gala / special event",            kind: "gala" },
      { id: "privateDining",     label: "Private dining",                  kind: "pp",   low: 35,  high: 60,  applies: "flexible" },
      { id: "groupActivities",   label: "Group activities",                kind: "pp",   low: 60,  high: 100, applies: "flexible" },
      { id: "entertainment",     label: "Entertainment",                   kind: "fixed", low: 5000, high: 9000, applies: "flexible", scales: true },
      { id: "vipTransport",      label: "VIP transportation",              kind: "pp",   low: 40,  high: 70,  applies: "flexible" },
      { id: "exclusiveVenue",    label: "Exclusive venue",                 kind: "fixed", low: 6000, high: 12000, applies: "flexible", scales: true },
      { id: "airportTransfers",  label: "Airport transfers (premium fleet)", kind: "pp", low: 15,  high: 25,  applies: "flexible" },
      { id: "branding",          label: "Branding / event production",     kind: "fixed", low: 4000, high: 8000, applies: "flexible", scales: true }
    ],

    // Selected Works proof, mapped to calculator destinations/event types.
    // Only works matching the current programme are shown beneath a result.
    works: [
      { slug: "cw-enerji-dealer-sales-meeting",        title: "CW Enerji Dealer & Sales Meeting",        meta: "Dealer incentive meeting, Nirvana Cosmopolitan, Antalya.",       destinations: ["antalya"],    eventTypes: ["incentive"] },
      { slug: "bellona-dealer-meeting",                title: "Bellona Dealer Meeting",                  meta: "Dealer incentive meeting, Belek.",                            destinations: ["antalya"],    eventTypes: ["incentive", "corporate-event"] },
      { slug: "anadolu-sigorta-100th-anniversary",     title: "Anadolu Sigorta 100th Anniversary",       meta: "Corporate anniversary event, Kremlin Palace, Antalya.",       destinations: ["antalya"],    eventTypes: ["corporate-event", "gala-event", "incentive"] },
      { slug: "turkiye-is-bankasi-aktob-conference",   title: "Türkiye İş Bankası AKTOB Conference",     meta: "Corporate conference, Antalya.",                              destinations: ["antalya"],    eventTypes: ["conference", "congress"] },
      { slug: "23rd-national-surgery-congress",        title: "23rd National Surgery Congress",          meta: "Association congress, Susesi Luxury Resort, Belek.",           destinations: ["antalya"],    eventTypes: ["conference", "congress"] },
      { slug: "swarovski-meeting-akra-antalya",        title: "Swarovski Meeting",                       meta: "Corporate meeting, Akra Antalya.",                             destinations: ["antalya"],    eventTypes: ["corporate-event", "conference", "corporate-retreat"] },
      { slug: "vakifbank-management-summit-titanic-belek", title: "VakıfBank Management Summit",         meta: "Corporate management summit, Titanic Deluxe Golf Belek.",      destinations: ["antalya"],    eventTypes: ["corporate-event", "corporate-retreat"] },
      { slug: "eksim-holding-management-summit",       title: "Eksim Holding Management Summit",         meta: "Management summit, Calista Luxury Resort, Belek.",             destinations: ["antalya"],    eventTypes: ["corporate-retreat", "corporate-event"] },
      { slug: "pierre-fabre-titanic-belek",            title: "Pierre Fabre Corporate Event",            meta: "Corporate event, Titanic Belek.",                             destinations: ["antalya"],    eventTypes: ["corporate-retreat", "corporate-event", "incentive"] },
      { slug: "dosso-dossi-fashion-show",              title: "Dosso Dossi Fashion Show",                meta: "Fashion show production, The Land of Legends, Antalya.",       destinations: ["antalya"],    eventTypes: ["product-launch", "brand-experience", "gala-event"] },
      { slug: "altin-kiraz-festival-press-launch",     title: "Altın Kiraz Festival — Press Launch",     meta: "Festival press launch, Korkuteli, Antalya.",                   destinations: ["antalya"],    eventTypes: ["product-launch", "brand-experience"] },
      { slug: "mapfre-sigorta-corporate-event",        title: "MAPFRE Sigorta Corporate Event",          meta: "Corporate event production, Antalya.",                         destinations: ["antalya"],    eventTypes: ["brand-experience", "corporate-event", "gala-event"] },
      { slug: "turk-telekom-business-partners-meeting", title: "Türk Telekom Business Partners Meeting", meta: "Business partners meeting, Rixos Sungate, Kemer.",             destinations: ["antalya"],    eventTypes: ["corporate-event", "conference"] },
      { slug: "temsa-corporate-event-calista-belek",   title: "TEMSA Corporate Event",                   meta: "Corporate event, Calista Luxury Resort, Belek.",               destinations: ["antalya"],    eventTypes: ["corporate-event"] }
    ],

    copy: {
      changeDrivers: [
        "Travel dates and season",
        "Hotel availability and room occupancy",
        "Venue selection",
        "Production complexity",
        "Entertainment",
        "Exclusive-use requirements",
        "Transportation requirements",
        "Programme customisation"
      ],
      disclaimer: "Indicative planning estimate only. Final programme pricing depends on travel dates, availability, hotel and venue selection, programme scope, production requirements and supplier confirmation."
    }
  };

  /* =======================================================================
   * 2. Analytics
   * =======================================================================
   */
  function trackEvent(name, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params || {}));
  }

  /* =======================================================================
   * 3. Session state (no personal data is ever stored here)
   * =======================================================================
   */
  function readState() {
    try {
      var raw = sessionStorage.getItem(SESSION_KEY);
      if (!raw) { return null; }
      var parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : null;
    } catch (err) {
      return null;
    }
  }

  function writeState(state) {
    try {
      sessionStorage.setItem(SESSION_KEY, JSON.stringify(state));
    } catch (err) { /* storage unavailable — state simply won't persist */ }
  }

  function clearState() {
    try {
      sessionStorage.removeItem(SESSION_KEY);
    } catch (err) { /* noop */ }
  }

  function groupSizeBand(guests) {
    if (guests < 50) { return "10-49"; }
    if (guests <= 100) { return "50-100"; }
    if (guests <= 250) { return "101-250"; }
    if (guests <= 500) { return "251-500"; }
    return "500+";
  }

  function analyticsContext(state) {
    return {
      calculator_destination: state.destination,
      calculator_event_type: state.eventType,
      calculator_group_size: groupSizeBand(state.guests),
      calculator_nights: state.nights,
      calculator_accommodation: state.accommodation,
      calculator_programme_level: state.programmeLevel
    };
  }

  /* =======================================================================
   * 4. Calculation engine
   * =======================================================================
   */
  function scaleFactor(guests) {
    var s = CONFIG.scale;
    var raw = Math.pow(Math.max(guests, 1) / s.referenceGuests, s.exponent);
    return Math.min(s.max, Math.max(s.min, raw));
  }

  function programmeMultiplier(state, key) {
    var level = CONFIG.programmeLevels[state.programmeLevel];
    return (level && level.multipliers[key]) || 1;
  }

  function computeEstimate(state) {
    var dest = CONFIG.destinations[state.destination];
    var structure = CONFIG.eventTypeStructure[state.eventType];
    var acc = CONFIG.accommodation[state.accommodation];
    var guests = state.guests;
    var nights = state.nights;
    var fixedScale = scaleFactor(guests);
    var confDays = Math.max(0, Math.min(structure.conferenceDays, nights));
    var expDays = Math.max(0, Math.min(structure.experienceDays, nights));

    function band(rate, qty, mult, ground) {
      return [rate[0] * qty * mult * ground, rate[1] * qty * mult * ground];
    }

    var components = [];

    // Accommodation — hotel coefficient applies.
    components.push({ key: "accommodation", label: "Accommodation",
      band: band(acc.pppn, guests * nights, 1, dest.hotel) });

    // Airport transfers & local transportation.
    components.push({ key: "transportation", label: "Transportation & Airport Transfers",
      band: band(CONFIG.components.transportation.pp, guests, programmeMultiplier(state, "transportation"), dest.ground) });

    // Food & beverage / hosted functions.
    components.push({ key: "foodBeverage", label: "Food & Beverage / Hosted Functions",
      band: band(CONFIG.components.foodBeverage.pppn, guests * nights * structure.hostedFnsPerNight, programmeMultiplier(state, "foodBeverage"), dest.ground) });

    // Meeting / conference facilities.
    if (structure.meeting && confDays > 0) {
      components.push({ key: "meeting", label: "Meeting / Conference Facilities",
        band: band(CONFIG.components.meeting.ppDay, guests * confDays, programmeMultiplier(state, "meeting"), dest.ground) });
    }

    // AV / production.
    if (structure.production && confDays > 0) {
      var pm = programmeMultiplier(state, "production") * dest.ground;
      var dayBand = band(CONFIG.components.production.ppDay, guests * confDays, pm, 1);
      var prodBase = CONFIG.components.production.base;
      components.push({ key: "production", label: "AV / Production",
        band: [dayBand[0] + prodBase[0] * fixedScale * pm, dayBand[1] + prodBase[1] * fixedScale * pm] });
    }

    // Activities & experiences.
    if (expDays > 0) {
      components.push({ key: "activities", label: "Activities & Experiences",
        band: band(CONFIG.components.activities.ppDay, guests * expDays, programmeMultiplier(state, "activities"), dest.ground) });
    }

    // Gala / special event.
    if (state.gala) {
      var gm = programmeMultiplier(state, "gala") * dest.ground;
      var galaBand = band(CONFIG.components.gala.pp, guests, gm, 1);
      var galaBase = CONFIG.components.gala.base;
      components.push({ key: "gala", label: "Gala / Special Event",
        band: [galaBand[0] + galaBase[0] * fixedScale * gm, galaBand[1] + galaBase[1] * fixedScale * gm] });
    }

    // Entertainment included in the base structure for launch/brand/gala types.
    if (structure.entertainment) {
      var em = programmeMultiplier(state, "entertainment") * dest.ground;
      var ent = CONFIG.components.entertainment.perProgramme;
      components.push({ key: "entertainment", label: "Entertainment",
        band: [ent[0] * fixedScale * em, ent[1] * fixedScale * em] });
    }

    // "Refine estimate" add-ons.
    (state.refinements || []).forEach(function (id) {
      var ref = null;
      CONFIG.refinements.forEach(function (candidate) {
        if (candidate.id === id) { ref = candidate; }
      });
      if (!ref) { return; }
      var mult = ref.applies === "flexible" ? programmeMultiplier(state, ref.component || ref.id) * dest.ground : 1;
      if (ref.kind === "component" && ref.component === "meeting") {
        var days = Math.max(confDays, Math.min(1, nights));
        components.push({ key: "ref-meeting", label: "Meeting / Conference Facilities",
          band: band(CONFIG.components.meeting.ppDay, guests * days, programmeMultiplier(state, "meeting"), dest.ground) });
      } else if (ref.kind === "component" && ref.component === "production") {
        var days2 = Math.max(confDays, Math.min(1, nights));
        var pm2 = programmeMultiplier(state, "production") * dest.ground;
        var dBand = band(CONFIG.components.production.ppDay, guests * days2, pm2, 1);
        var base2 = CONFIG.components.production.base;
        components.push({ key: "ref-production", label: "AV / Production",
          band: [dBand[0] + base2[0] * fixedScale * pm2, dBand[1] + base2[1] * fixedScale * pm2] });
      } else if (ref.kind === "pp") {
        components.push({ key: "ref-" + ref.id, label: ref.label,
          band: band([ref.low, ref.high], guests, mult, 1) });
      } else if (ref.kind === "fixed") {
        var qty = ref.scales ? fixedScale : 1;
        components.push({ key: "ref-" + ref.id, label: ref.label,
          band: [ref.low * qty * mult, ref.high * qty * mult] });
      }
    });

    // Merge components that share the same label (base + refinement).
    var merged = [];
    components.forEach(function (component) {
      var existing = null;
      merged.forEach(function (candidate) {
        if (candidate.label === component.label) { existing = candidate; }
      });
      if (existing) {
        existing.band[0] += component.band[0];
        existing.band[1] += component.band[1];
      } else {
        merged.push({ label: component.label, band: component.band });
      }
    });

    var subtotal = merged.reduce(function (acc2, component) {
      return [acc2[0] + component.band[0], acc2[1] + component.band[1]];
    }, [0, 0]);

    var opsShare = CONFIG.operations.share[state.eventType] || 0.10;
    merged.push({ label: "Local Operations & DMC Coordination", band: [subtotal[0] * opsShare, subtotal[1] * opsShare] });
    var total = [subtotal[0] * (1 + opsShare), subtotal[1] * (1 + opsShare)];

    // Collapse to a single midpoint then spread to the planning range, so the
    // published range is a consistent ±spread around the modelled midpoint.
    var midpoint = (total[0] + total[1]) / 2;
    var low = roundBandTotal(midpoint * (1 - CONFIG.rangeSpread));
    var high = roundBandTotal(midpoint * (1 + CONFIG.rangeSpread));
    var perGuest = [roundBandPerGuest(low / guests), roundBandPerGuest(high / guests)];

    return {
      total: [low, high],
      perGuest: perGuest,
      components: merged.map(function (component) {
        var componentMid = (component.band[0] + component.band[1]) / 2;
        return {
          label: component.label,
          band: [roundBandTotal(componentMid * (1 - CONFIG.rangeSpread)), roundBandTotal(componentMid * (1 + CONFIG.rangeSpread))]
        };
      })
    };
  }

  function roundBandTotal(value) {
    if (value >= 100000) { return Math.round(value / 1000) * 1000; }
    if (value >= 10000) { return Math.round(value / 500) * 500; }
    return Math.round(value / 250) * 250;
  }

  function roundBandPerGuest(value) {
    if (value >= 1000) { return Math.round(value / 10) * 10; }
    return Math.round(value / 5) * 5;
  }

  function formatMoney(value) {
    return "€" + Math.round(value).toLocaleString("en-US");
  }

  function formatRange(band) {
    return formatMoney(band[0]) + " – " + formatMoney(band[1]);
  }

  /* =======================================================================
   * 5. Proposal handoff (sessionStorage, never the URL)
   * =======================================================================
   */
  function summaryLines(state) {
    return [
      state.guests + " guests",
      CONFIG.destinations[state.destination].label,
      state.nights + (state.nights === 1 ? " night" : " nights"),
      CONFIG.accommodation[state.accommodation].label + " accommodation",
      CONFIG.programmeLevels[state.programmeLevel].label + " programme",
      state.gala ? "Gala / special event included" : "No gala / special event"
    ];
  }

  function assumptionBullets(state) {
    var structure = CONFIG.eventTypeStructure[state.eventType];
    var bullets = [
      state.guests + " guests",
      state.nights + (state.nights === 1 ? "-night stay" : "-night stay"),
      CONFIG.accommodation[state.accommodation].label + " accommodation, twin/double occupancy",
      CONFIG.programmeLevels[state.programmeLevel].label + " programme level",
      "Private airport transfers"
    ];
    if (structure.meeting) { bullets.push("Meeting / conference facilities"); }
    if (structure.production) { bullets.push("Core AV / production"); }
    if (structure.experienceDays > 0) { bullets.push(structure.experienceDays >= 1.5 ? "Two hosted group experiences" : "One hosted group experience"); }
    if (state.gala) { bullets.push("Gala dinner with production"); }
    if (structure.entertainment) { bullets.push("Entertainment programme"); }
    if ((state.refinements || []).length) {
      bullets.push("Additional requirements: " + state.refinements.map(function (id) {
        var label = id;
        CONFIG.refinements.forEach(function (ref) {
          if (ref.id === id) { label = ref.label; }
        });
        return label.toLowerCase();
      }).join(", "));
    }
    bullets.push("Standard local DMC coordination");
    return bullets;
  }

  function buildLeadBrief(state, result) {
    var lines = [
      "Destination: " + CONFIG.destinations[state.destination].label,
      "Programme: " + CONFIG.eventTypes[state.eventType].label,
      "Guests: " + state.guests,
      "Duration: " + state.nights + (state.nights === 1 ? " night" : " nights"),
      "Accommodation: " + CONFIG.accommodation[state.accommodation].label,
      "Programme Level: " + CONFIG.programmeLevels[state.programmeLevel].label,
      "Gala: " + (state.gala ? "Yes" : "No")
    ];
    if ((state.refinements || []).length) {
      lines.push("Additional Requirements: " + state.refinements.map(function (id) {
        var label = id;
        CONFIG.refinements.forEach(function (ref) {
          if (ref.id === id) { label = ref.label; }
        });
        return label;
      }).join(", "));
    }
    lines.push("Indicative Calculator Range: " + formatRange(result.total));
    lines.push("Estimated Cost Per Guest: " + formatRange(result.perGuest));
    return lines.join("\n");
  }

  /* =======================================================================
   * 6. Calculator UI
   * =======================================================================
   */
  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) { node.className = className; }
    if (text != null) { node.textContent = text; }
    return node;
  }

  function normalizeState(raw) {
    var d = CONFIG.defaults;
    var state = {
      destination: CONFIG.destinations[raw && raw.destination] ? raw.destination : d.destination,
      eventType: CONFIG.eventTypes[raw && raw.eventType] ? raw.eventType : d.eventType,
      guests: d.guests,
      nights: d.nights,
      accommodation: CONFIG.accommodation[raw && raw.accommodation] ? raw.accommodation : d.accommodation,
      programmeLevel: CONFIG.programmeLevels[raw && raw.programmeLevel] ? raw.programmeLevel : d.programmeLevel,
      gala: Boolean(raw && raw.gala),
      refinements: []
    };
    if (raw && raw.guests != null && isFinite(Number(raw.guests))) {
      state.guests = Math.max(CONFIG.limits.guestsMin, Math.min(CONFIG.limits.guestsMax, Math.round(Number(raw.guests))));
    }
    if (raw && raw.nights != null && isFinite(Number(raw.nights))) {
      state.nights = Math.max(CONFIG.limits.nightsMin, Math.min(CONFIG.limits.nightsMax, Math.round(Number(raw.nights))));
    }
    if (raw && Array.isArray(raw.refinements)) {
      state.refinements = raw.refinements.filter(function (id) {
        var known = false;
        CONFIG.refinements.forEach(function (ref) {
          if (ref.id === id && ref.kind !== "gala") { known = true; }
        });
        return known;
      });
    }
    return state;
  }

  function readStateFromForm(root) {
    var refinements = [];
    root.querySelectorAll("[data-calc-refinement]:checked").forEach(function (input) {
      refinements.push(input.value);
    });
    return normalizeState({
      destination: root.querySelector("[data-calc-destination]").value,
      eventType: root.querySelector("[data-calc-event-type]").value,
      guests: root.querySelector("[data-calc-guests]").value,
      nights: root.querySelector("[data-calc-nights]").value,
      accommodation: root.querySelector("[data-calc-accommodation]").value,
      programmeLevel: root.querySelector("[data-calc-programme]").value,
      gala: root.querySelector("[data-calc-gala]").checked,
      refinements: refinements
    });
  }

  function writeStateToForm(root, state) {
    root.querySelector("[data-calc-destination]").value = state.destination;
    root.querySelector("[data-calc-event-type]").value = state.eventType;
    root.querySelector("[data-calc-guests]").value = state.guests;
    root.querySelector("[data-calc-nights]").value = state.nights;
    root.querySelector("[data-calc-accommodation]").value = state.accommodation;
    root.querySelector("[data-calc-programme]").value = state.programmeLevel;
    root.querySelector("[data-calc-gala]").checked = state.gala;
    root.querySelectorAll("[data-calc-refinement]").forEach(function (input) {
      input.checked = state.refinements.indexOf(input.value) !== -1;
    });
  }

  function optionList(select, map, current) {
    Object.keys(map).forEach(function (key) {
      var option = document.createElement("option");
      option.value = key;
      option.textContent = map[key].label;
      if (key === current) { option.selected = true; }
      select.appendChild(option);
    });
  }

  function field(labelText, control) {
    var wrapper = el("div", "calc__field");
    var label = el("label", "calc__label", labelText);
    var id = "calc-" + Math.random().toString(36).slice(2, 9);
    control.id = id;
    label.setAttribute("for", id);
    wrapper.appendChild(label);
    wrapper.appendChild(control);
    return wrapper;
  }

  function makeSelect(attr) {
    var select = el("select", "calc__input");
    select.setAttribute(attr, "");
    return select;
  }

  function renderResults(root, state, result) {
    var container = root.querySelector("[data-calc-results]");
    container.textContent = "";

    // Headline range.
    var summary = el("div", "calc__summary");
    summary.appendChild(el("p", "calc__summary-label", "Your Indicative Programme Budget"));
    summary.appendChild(el("p", "calc__figure", formatRange(result.total)));
    summary.appendChild(el("p", "calc__summary-label", "Estimated Cost Per Guest"));
    summary.appendChild(el("p", "calc__subfigure", formatRange(result.perGuest) + " per guest"));
    var params = el("p", "calc__params", summaryLines(state).join(" · "));
    summary.appendChild(params);
    container.appendChild(summary);

    // Breakdown.
    var breakdown = el("div", "calc__breakdown");
    breakdown.appendChild(el("h3", "calc__heading", "Estimated Budget Breakdown"));
    var list = el("dl", "calc__breakdown-list");
    result.components.forEach(function (component) {
      var row = el("div", "calc__breakdown-row");
      row.appendChild(el("dt", null, component.label));
      row.appendChild(el("dd", null, formatRange(component.band)));
      list.appendChild(row);
    });
    breakdown.appendChild(list);
    container.appendChild(breakdown);

    // Assumptions.
    var assumptions = el("div", "calc__assumptions");
    assumptions.appendChild(el("h3", "calc__heading", "What This Estimate Assumes"));
    var ul = el("ul", "calc__assumption-list");
    assumptionBullets(state).forEach(function (item) {
      ul.appendChild(el("li", null, item));
    });
    assumptions.appendChild(ul);
    container.appendChild(assumptions);

    // Budget drivers.
    var drivers = el("div", "calc__drivers");
    drivers.appendChild(el("h3", "calc__heading", "What Could Change the Budget?"));
    var chips = el("ul", "calc__driver-list");
    CONFIG.copy.changeDrivers.forEach(function (item) {
      chips.appendChild(el("li", null, item));
    });
    drivers.appendChild(chips);
    container.appendChild(drivers);

    // Relevant Selected Works (destination + event-type match only).
    var works = CONFIG.works.filter(function (work) {
      return work.destinations.indexOf(state.destination) !== -1 && work.eventTypes.indexOf(state.eventType) !== -1;
    }).slice(0, 3);
    if (works.length) {
      var worksSection = el("div", "calc__works");
      worksSection.appendChild(el("h3", "calc__heading", "Relevant Work in Turkey"));
      var grid = el("div", "card-grid");
      works.forEach(function (work) {
        var link = el("a", "card", null);
        link.setAttribute("href", "/selected-works/" + work.slug + "/");
        link.setAttribute("data-track", "calculator_selected_work_click");
        link.appendChild(el("h3", null, work.title));
        link.appendChild(el("p", null, work.meta));
        grid.appendChild(link);
      });
      worksSection.appendChild(grid);
      container.appendChild(worksSection);
    }

    // Conversion CTA — shown only after the estimate has been delivered.
    var cta = el("div", "calc__cta");
    cta.appendChild(el("h3", "calc__heading", "Planning Something Like This?"));
    cta.appendChild(el("p", null, "Turn this estimate into an actual programme. Share your dates and a few project details and our local Turkey team can prepare a tailored programme and proposal."));
    var actions = el("div", "cta-banner__actions");
    var primary = el("a", "btn btn--primary", "Request a Detailed Proposal");
    primary.setAttribute("href", "/request-proposal/");
    primary.setAttribute("data-calc-proposal-cta", "");
    var secondary = el("a", "btn btn--ghost", "Book a Partner Call");
    secondary.setAttribute("href", "/contact/");
    secondary.setAttribute("data-track", "calculator_partner_call_click");
    actions.appendChild(primary);
    actions.appendChild(secondary);
    cta.appendChild(actions);
    container.appendChild(cta);

    // Disclaimer — directly beneath the estimate, per the brief.
    container.appendChild(el("p", "calc__disclaimer", CONFIG.copy.disclaimer));
  }

  function buildCalculator(root) {
    // Pre-population: data attributes (page context) override session state,
    // which overrides defaults.
    var preset = {
      destination: root.getAttribute("data-destination") || undefined,
      eventType: root.getAttribute("data-event-type") || undefined,
      guests: root.getAttribute("data-guests") || undefined,
      nights: root.getAttribute("data-nights") || undefined,
      accommodation: root.getAttribute("data-accommodation") || undefined,
      programmeLevel: root.getAttribute("data-programme-level") || undefined
    };
    var stored = readState();
    var state = normalizeState(Object.assign({}, stored || {}, preset));
    // Restore the previous in-session result only when the effective inputs
    // still match what produced it — a scenario page's pre-populated defaults
    // must never silently re-display a stale estimate for a different setup.
    var hasResult = false;
    if (stored && stored.result) {
      hasResult = ["destination", "eventType", "guests", "nights", "accommodation", "programmeLevel", "gala"].every(function (key) {
        return String(stored[key]) === String(state[key]);
      });
    }

    var wrap = el("div", "calc");

    /* --- Inputs --- */
    var formWrap = el("div", "calc__inputs");
    var grid = el("div", "calc__grid");

    var destinationSelect = makeSelect("data-calc-destination");
    optionList(destinationSelect, CONFIG.destinations, state.destination);
    grid.appendChild(field("Destination", destinationSelect));

    var eventTypeSelect = makeSelect("data-calc-event-type");
    optionList(eventTypeSelect, CONFIG.eventTypes, state.eventType);
    grid.appendChild(field("Event / Programme Type", eventTypeSelect));

    var guestsInput = el("input", "calc__input");
    guestsInput.setAttribute("type", "number");
    guestsInput.setAttribute("min", String(CONFIG.limits.guestsMin));
    guestsInput.setAttribute("max", String(CONFIG.limits.guestsMax));
    guestsInput.setAttribute("step", "10");
    guestsInput.setAttribute("inputmode", "numeric");
    guestsInput.setAttribute("data-calc-guests", "");
    guestsInput.value = state.guests;
    grid.appendChild(field("Number of Guests", guestsInput));

    var nightsInput = el("input", "calc__input");
    nightsInput.setAttribute("type", "number");
    nightsInput.setAttribute("min", String(CONFIG.limits.nightsMin));
    nightsInput.setAttribute("max", String(CONFIG.limits.nightsMax));
    nightsInput.setAttribute("step", "1");
    nightsInput.setAttribute("inputmode", "numeric");
    nightsInput.setAttribute("data-calc-nights", "");
    nightsInput.value = state.nights;
    grid.appendChild(field("Number of Nights", nightsInput));

    var accommodationSelect = makeSelect("data-calc-accommodation");
    optionList(accommodationSelect, CONFIG.accommodation, state.accommodation);
    grid.appendChild(field("Accommodation Level", accommodationSelect));

    var programmeSelect = makeSelect("data-calc-programme");
    Object.keys(CONFIG.programmeLevels).forEach(function (key) {
      var level = CONFIG.programmeLevels[key];
      var option = document.createElement("option");
      option.value = key;
      option.textContent = level.label + " — " + level.description;
      if (key === state.programmeLevel) { option.selected = true; }
      programmeSelect.appendChild(option);
    });
    grid.appendChild(field("Programme Level", programmeSelect));

    formWrap.appendChild(grid);

    var galaLabel = el("label", "calc__toggle");
    var galaInput = el("input", "calc__toggle-input");
    galaInput.setAttribute("type", "checkbox");
    galaInput.setAttribute("data-calc-gala", "");
    galaInput.checked = state.gala;
    galaLabel.appendChild(galaInput);
    galaLabel.appendChild(el("span", null, "Include a gala / special event (venue, F&B and production)"));
    formWrap.appendChild(galaLabel);

    var actions = el("div", "calc__actions");
    var calculateBtn = el("button", "btn btn--primary calc__calculate", "Calculate My Budget");
    calculateBtn.setAttribute("type", "button");
    actions.appendChild(calculateBtn);
    formWrap.appendChild(actions);
    wrap.appendChild(formWrap);

    /* --- Refine panel --- */
    var refine = el("div", "calc__refine");
    refine.hidden = true;
    refine.appendChild(el("h3", "calc__heading", "Refine Estimate"));
    refine.appendChild(el("p", "calc__refine-intro", "Add any known requirements — the estimate updates immediately."));
    var refineGrid = el("div", "calc__refine-grid");
    CONFIG.refinements.forEach(function (ref) {
      var label = el("label", "calc__refine-option");
      var input = el("input", "calc__refine-input");
      input.setAttribute("type", "checkbox");
      input.setAttribute("value", ref.id);
      if (ref.kind === "gala") {
        input.setAttribute("data-calc-refinement-gala", "");
        input.checked = state.gala;
      } else {
        input.setAttribute("data-calc-refinement", "");
        input.checked = state.refinements.indexOf(ref.id) !== -1;
      }
      label.appendChild(input);
      label.appendChild(el("span", null, ref.label));
      refineGrid.appendChild(label);
    });
    refine.appendChild(refineGrid);
    wrap.appendChild(refine);

    /* --- Results --- */
    var results = el("div", "calc__results");
    results.setAttribute("data-calc-results", "");
    results.setAttribute("aria-live", "polite");
    results.hidden = true;
    wrap.appendChild(results);

    root.appendChild(wrap);

    var started = false;

    function syncRefineGala() {
      var galaRefineInput = refine.querySelector("[data-calc-refinement-gala]");
      if (galaRefineInput) { galaRefineInput.checked = galaInput.checked; }
    }

    function update() {
      state = readStateFromForm(root);
      var result = computeEstimate(state);
      writeState(Object.assign({}, state, { result: { total: result.total, perGuest: result.perGuest }, brief: buildLeadBrief(state, result), updatedAt: new Date().toISOString() }));
      renderResults(root, state, result);
      results.hidden = false;
      refine.hidden = false;
      calculateBtn.textContent = "Recalculate";
      return result;
    }

    root.addEventListener("focusin", function () {
      if (!started) {
        started = true;
        trackEvent("calculator_started", analyticsContext(readStateFromForm(root)));
      }
    });

    // Live recalculation once the first result exists.
    root.addEventListener("change", function (event) {
      var target = event.target;
      if (!target || !target.getAttribute) { return; }
      if (target.hasAttribute("data-calc-refinement-gala")) {
        galaInput.checked = target.checked;
      }
      if (target.hasAttribute("data-calc-gala")) { syncRefineGala(); }
      if (!results.hidden) {
        var before = results.querySelector(".calc__figure");
        update();
        var after = results.querySelector(".calc__figure");
        if (target.hasAttribute("data-calc-destination")) {
          trackEvent("calculator_destination_changed", analyticsContext(state));
        } else if (target.hasAttribute("data-calc-event-type")) {
          trackEvent("calculator_event_type_changed", analyticsContext(state));
        } else if (before && after && before.textContent !== after.textContent) {
          trackEvent("calculator_refined", analyticsContext(state));
        }
      }
    });

    root.addEventListener("input", function (event) {
      var target = event.target;
      if (!target || !target.getAttribute) { return; }
      if ((target.hasAttribute("data-calc-guests") || target.hasAttribute("data-calc-nights")) && !results.hidden) {
        update();
      }
    });

    calculateBtn.addEventListener("click", function () {
      update();
      trackEvent("calculator_completed", analyticsContext(state));
      if (!hasResult) {
        results.scrollIntoView({ behavior: "smooth", block: "start" });
      }
      hasResult = true;
    });

    // Proposal CTA: stamp state into the session (belt-and-braces — update()
    // already wrote it) and track the conversion click.
    wrap.addEventListener("click", function (event) {
      var link = event.target && event.target.closest ? event.target.closest("[data-calc-proposal-cta]") : null;
      if (link) {
        update();
        trackEvent("calculator_proposal_clicked", analyticsContext(state));
      }
    });

    // Restore a previous in-session result so returning visitors see their
    // last estimate without re-entering anything.
    if (hasResult) {
      writeStateToForm(root, state);
      update();
      hasResult = true;
    }
  }

  /* =======================================================================
   * 7. Proposal page integration
   * =======================================================================
   */
  function initProposalIntegration() {
    var form = document.querySelector("[data-proposal-form]");
    var summary = document.querySelector("[data-calculator-summary]");
    if (!form || !summary) { return; }
    var stored = readState();
    if (!stored || !stored.result) { return; }
    var state = normalizeState(stored);

    var dl = summary.querySelector("dl");
    if (dl) {
      summaryLines(state).forEach(function (line) {
        var row = el("div", null);
        var dt = document.createElement("dt");
        dt.textContent = "•";
        dt.setAttribute("aria-hidden", "true");
        var dd = document.createElement("dd");
        dd.textContent = line;
        row.appendChild(dt);
        row.appendChild(dd);
        dl.appendChild(row);
      });
      var budgetRow = el("div", null);
      var budgetDt = document.createElement("dt");
      budgetDt.textContent = "Indicative budget";
      var budgetDd = document.createElement("dd");
      budgetDd.textContent = formatRange(stored.result.total);
      budgetRow.appendChild(budgetDt);
      budgetRow.appendChild(budgetDd);
      dl.appendChild(budgetRow);
    }

    var band = groupSizeBand(state.guests);
    var groupSelect = form.elements.group_size;
    if (groupSelect) {
      var groupValue = { "10-49": "20–50", "50-100": "51–100", "101-250": "101–250", "251-500": "251–500", "500+": "500+" }[band];
      if (state.guests < 20) { groupValue = "Under 20"; }
      if (groupValue) {
        for (var i = 0; i < groupSelect.options.length; i++) {
          if (groupSelect.options[i].text === groupValue) {
            groupSelect.value = groupSelect.options[i].value || groupSelect.options[i].text;
            break;
          }
        }
      }
    }

    var destinationSelect = form.elements.destination;
    if (destinationSelect) {
      var destinationLabel = CONFIG.destinations[state.destination].label;
      for (var j = 0; j < destinationSelect.options.length; j++) {
        if (destinationSelect.options[j].text === destinationLabel) {
          destinationSelect.value = destinationSelect.options[j].value || destinationSelect.options[j].text;
          break;
        }
      }
    }

    var projectSelect = form.elements.project_type;
    if (projectSelect) {
      var projectMap = {
        "corporate-event": "Corporate Event",
        "incentive": "Incentive Travel",
        "conference": "Meeting / Conference",
        "congress": "Congress / Exhibition",
        "corporate-retreat": "Corporate Event",
        "product-launch": "Corporate Event",
        "brand-experience": "Corporate Event",
        "gala-event": "Gala / Special Event"
      };
      var projectLabel = projectMap[state.eventType];
      if (projectLabel) {
        for (var k = 0; k < projectSelect.options.length; k++) {
          if (projectSelect.options[k].text === projectLabel) {
            projectSelect.value = projectSelect.options[k].value || projectSelect.options[k].text;
            break;
          }
        }
      }
    }

    // Hidden structured calculator brief — read by /api/request-proposal and
    // merged into the lead email as a "Calculator Lead" block.
    var briefField = document.createElement("input");
    briefField.setAttribute("type", "hidden");
    briefField.setAttribute("name", "calculator_brief");
    briefField.value = stored.brief || "";
    form.appendChild(briefField);

    summary.hidden = false;
    trackEvent("calculator_proposal_form_view", analyticsContext(state));

    form.addEventListener("submit", function () {
      trackEvent("calculator_proposal_submitted", analyticsContext(state));
      clearState();
    });
  }

  /* =======================================================================
   * 8. Boot
   * =======================================================================
   */
  document.addEventListener("DOMContentLoaded", function () {
    var roots = document.querySelectorAll("[data-calculator]");
    if (roots.length) {
      trackEvent("calculator_view", {
        calculator_destination: roots[0].getAttribute("data-destination") || undefined,
        calculator_event_type: roots[0].getAttribute("data-event-type") || undefined
      });
    }
    roots.forEach(buildCalculator);
    initProposalIntegration();
  });

  // Expose a minimal read API for future pages/tests without leaking internals.
  window.DTPCalculator = {
    version: "1.0.0",
    clearState: clearState
  };
})();
