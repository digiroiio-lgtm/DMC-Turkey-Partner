/* =========================================================================
 * DmcTurkeyPartner.com — Antalya Venue Matcher
 *
 * A decision-support tool, not a lead form. The planner describes the event
 * (format, group size, priorities, month); the matcher scores Antalya's
 * resort zones and venue archetypes against that brief and returns a
 * reasoned shortlist with the operational watch-outs that actually decide
 * a venue in this destination — transfer time, ballroom span, loading
 * access, rigging capability and seasonal availability.
 *
 * The resulting brief is held in sessionStorage under "dtp_venue_brief" so
 * that a planner who continues to /request-proposal/ never has to retype
 * what they just told us. It is never put in the URL.
 * ========================================================================= */
(function () {
  "use strict";

  var SESSION_KEY = "dtp_venue_brief";

  /* =======================================================================
   * 1. Destination model
   *
   * Zone facts (distance, transfer time) are published Antalya Airport (AYT)
   * road distances; transfer times are door-to-door coach estimates in
   * normal traffic and are deliberately given as ranges.
   * =======================================================================
   */
  var ZONES = {
    "lara-kundu": {
      label: "Lara & Kundu",
      transfer: "15–25 min from AYT (≈12–20 km)",
      transferMinutes: 20,
      profile: "Antalya's densest run of large-format five-star beach resorts, close enough to the airport that arrival day stays usable.",
      strengths: ["large ballrooms", "beachfront gala space", "shortest airport transfer", "single-property programmes"],
      watchOut: "The largest properties here run high occupancy through the summer leisure season — plenary-capable ballrooms are the first thing to go.",
      capacityCeiling: 1500
    },
    "belek": {
      label: "Belek",
      transfer: "30–45 min from AYT (≈34 km)",
      transferMinutes: 38,
      profile: "A purpose-built resort corridor of premium properties and championship golf courses, with the calmest logistics of any Antalya zone.",
      strengths: ["golf incentives", "premium resorts", "corporate retreats", "controlled single-site logistics"],
      watchOut: "Golf demand peaks in spring and autumn — exactly when MICE demand does. Course tee-time blocks need locking with the room block, not after it.",
      capacityCeiling: 1200
    },
    "antalya-city": {
      label: "Antalya City (Konyaaltı, Old Town & Glass Pyramid)",
      transfer: "25–40 min from AYT (traffic-dependent)",
      transferMinutes: 33,
      profile: "City-centre congress and business hotels alongside the Glass Pyramid Sabancı Congress and Exhibition Center, plus Kaleiçi's historic quarter for off-site evenings.",
      strengths: ["city congress infrastructure", "cultural off-site venues", "walkable delegate free time", "year-round operation"],
      watchOut: "City traffic is the variable nobody budgets for. Build a realistic transfer window into the run sheet rather than the map distance.",
      capacityCeiling: 2000
    },
    "aksu-expo": {
      label: "Aksu / Expo Centre corridor",
      transfer: "10–20 min from AYT",
      transferMinutes: 15,
      profile: "The ANFAŞ Antalya Expo Center sits on the airport side of the city: roughly 60,000 m² of space (about 40,000 m² indoor and 20,000 m² outdoor), 15 congress and seminar halls from 10 to 1,000 people, conference configurations to around 4,000, and parking for about 2,500 vehicles.",
      strengths: ["exhibition floor", "congress at scale", "vehicle and freight access", "airport proximity"],
      watchOut: "Delegates sleep elsewhere. An Expo Centre programme is a shuttle operation from day one, so the hotel block and the coach plan have to be designed together.",
      capacityCeiling: 4000
    },
    "side-manavgat": {
      label: "Side & Manavgat",
      transfer: "60–75 min from AYT",
      transferMinutes: 68,
      profile: "Large resort inventory at generally softer rates, with genuinely distinctive Greco-Roman settings for an off-site evening.",
      strengths: ["budget headroom", "large room blocks", "distinctive gala settings", "quieter resort feel"],
      watchOut: "The transfer is the trade-off. Over an hour each way costs you most of arrival and departure day, which matters more on a three-night programme than a six-night one.",
      capacityCeiling: 1000
    },
    "kemer": {
      label: "Kemer",
      transfer: "≈60 min from AYT (≈60 km)",
      transferMinutes: 60,
      profile: "Mountains meeting the sea along a narrow coastal strip, with smaller premium properties suited to groups that want scenery and seclusion over scale.",
      strengths: ["scenery", "exclusivity and buy-outs", "boutique incentives", "outdoor activity access"],
      watchOut: "The coast road is winding and slow for full-size coaches. Split larger groups across smaller vehicles and add contingency to every transfer leg.",
      capacityCeiling: 400
    }
  };

  var ARCHETYPES = {
    "resort-conference": {
      label: "Integrated resort conference hotel",
      summary: "Rooms, plenary ballroom, breakouts, F&B and a beachfront gala space on one property — the format that makes Antalya efficient.",
      bestFor: "Conferences, sales kick-offs, retreats and incentive programmes that want everything under one contract."
    },
    "convention-centre": {
      label: "Convention & exhibition centre",
      summary: "Purpose-built halls with flat floors, vehicle access and the ceiling height that rigging and exhibition builds actually need.",
      bestFor: "Congresses, exhibitions, large plenaries and any programme with an exhibition or sponsor floor."
    },
    "city-congress": {
      label: "City congress hotel",
      summary: "Business hotels in central Antalya with meeting floors, close to the Glass Pyramid congress centre and the old town.",
      bestFor: "City-format conferences, association meetings and programmes that want delegates able to walk out into a city."
    },
    "boutique-exclusive": {
      label: "Boutique or exclusive-use property",
      summary: "Smaller design-led properties where a full buy-out is realistic and the whole site becomes the event.",
      bestFor: "Executive offsites, leadership retreats, top-performer incentives and confidential meetings."
    },
    "destination-gala": {
      label: "Destination gala venue",
      summary: "Beach clubs, terraces and heritage settings used as a standalone evening rather than a hotel function room.",
      bestFor: "Awards nights, closing galas, product reveals and the one evening the programme is remembered for."
    },
    "golf-resort": {
      label: "Golf resort",
      summary: "Belek's championship courses attached to resorts with full conference infrastructure.",
      bestFor: "Golf incentives, client hospitality and mixed programmes pairing a meeting day with a tournament day."
    }
  };

  /* Seasonality is a real constraint in Antalya, not a footnote. */
  var MONTHS = {
    "1": { label: "January", band: "low", note: "Low season. Excellent value and wide availability; cool and wet enough that any outdoor element needs a covered alternative." },
    "2": { label: "February", band: "low", note: "Low season. Strong rates, but build every outdoor plan with an indoor fallback." },
    "3": { label: "March", band: "shoulder", note: "Shoulder season opening up. Rates still soft, weather variable, availability good." },
    "4": { label: "April", band: "peak-mice", note: "Prime MICE window. Comfortable temperatures and reliable outdoor evenings — and the heaviest competition for ballroom space." },
    "5": { label: "May", band: "peak-mice", note: "Prime MICE window and arguably the best month overall. Book plenary space 9–12 months out." },
    "6": { label: "June", band: "summer", note: "Hot, and leisure demand is climbing. Daytime outdoor programme needs shade and hydration planning." },
    "7": { label: "July", band: "summer", note: "Peak leisure season. Highest rates, tightest availability and daytime heat that rules out midday outdoor activity." },
    "8": { label: "August", band: "summer", note: "Peak leisure season. The hardest month to source well and the hardest to run an outdoor daytime programme in." },
    "9": { label: "September", band: "peak-mice", note: "Prime MICE window. Warm sea, comfortable evenings, heavy competition for space." },
    "10": { label: "October", band: "peak-mice", note: "Prime MICE window and the strongest month for outdoor galas. Book early." },
    "11": { label: "November", band: "shoulder", note: "Shoulder season. Good value, generally mild, with rain risk that an outdoor gala plan has to answer." },
    "12": { label: "December", band: "low", note: "Low season. Strong rates and availability; plan the social programme indoors." }
  };

  var FORMATS = {
    "conference": {
      label: "Conference / plenary",
      zoneWeights: { "lara-kundu": 8, "belek": 6, "antalya-city": 7, "aksu-expo": 6, "side-manavgat": 4, "kemer": 1 },
      archetypes: ["resort-conference", "city-congress", "convention-centre"],
      criteria: ["Plenary ballroom with a clear span and no pillars in sightlines", "Breakout rooms on the same floor as plenary", "Ceiling height for screen and rigging", "Catering capacity to turn lunch for the full room inside a session break"]
    },
    "incentive": {
      label: "Incentive programme",
      zoneWeights: { "lara-kundu": 7, "belek": 9, "antalya-city": 4, "aksu-expo": 0, "side-manavgat": 6, "kemer": 7 },
      archetypes: ["resort-conference", "boutique-exclusive", "destination-gala"],
      criteria: ["Room quality and suite ratio for top performers", "Beach, pool and terrace space the group can call its own", "Off-site experiences within a sensible coach leg", "A gala setting that does not look like a function room"]
    },
    "corporate-meeting": {
      label: "Corporate meeting",
      zoneWeights: { "lara-kundu": 7, "belek": 7, "antalya-city": 8, "aksu-expo": 2, "side-manavgat": 4, "kemer": 4 },
      archetypes: ["resort-conference", "city-congress", "boutique-exclusive"],
      criteria: ["Meeting rooms with daylight and proper ventilation", "Reliable, contended bandwidth for hybrid participants", "Private dining separate from the main restaurant", "Short transfer so a two-day meeting stays two days"]
    },
    "gala": {
      label: "Gala dinner / awards night",
      zoneWeights: { "lara-kundu": 9, "belek": 7, "antalya-city": 7, "aksu-expo": 3, "side-manavgat": 7, "kemer": 5 },
      archetypes: ["destination-gala", "resort-conference"],
      criteria: ["Banqueting capacity at round tables, not theatre-style headline numbers", "Power supply and generator backup for an outdoor build", "A credible wet-weather alternative on the same site", "Load-in window that does not collide with hotel service"]
    },
    "product-launch": {
      label: "Product launch",
      zoneWeights: { "lara-kundu": 8, "belek": 6, "antalya-city": 7, "aksu-expo": 8, "side-manavgat": 3, "kemer": 2 },
      archetypes: ["convention-centre", "resort-conference", "destination-gala"],
      criteria: ["Vehicle or freight access directly into the room", "Rigging points and confirmed point loads", "Exclusive use during build and rehearsal days", "Blackout capability for a controlled reveal"]
    },
    "congress-exhibition": {
      label: "Congress / exhibition",
      zoneWeights: { "lara-kundu": 5, "belek": 3, "antalya-city": 7, "aksu-expo": 10, "side-manavgat": 1, "kemer": 0 },
      archetypes: ["convention-centre", "city-congress"],
      criteria: ["Flat exhibition floor with published floor loading", "Dedicated loading bays and marshalling space", "Registration and circulation area outside the halls", "Hotel inventory reachable on a workable shuttle loop"]
    },
    "retreat": {
      label: "Corporate retreat / executive offsite",
      zoneWeights: { "lara-kundu": 5, "belek": 8, "antalya-city": 4, "aksu-expo": 0, "side-manavgat": 5, "kemer": 8 },
      archetypes: ["boutique-exclusive", "resort-conference", "golf-resort"],
      criteria: ["Exclusive use or a genuinely separated wing", "Meeting space that is not shared with other groups", "Discretion around arrivals, dining and public areas", "Activity options that work as a group, not as a queue"]
    },
    "kickoff": {
      label: "Sales kick-off",
      zoneWeights: { "lara-kundu": 9, "belek": 8, "antalya-city": 5, "aksu-expo": 3, "side-manavgat": 5, "kemer": 3 },
      archetypes: ["resort-conference", "destination-gala"],
      criteria: ["One plenary room that holds the entire field team at once", "Breakouts for regional and team sessions running in parallel", "An evening space that flips from session to celebration", "All-inclusive F&B to keep per-head cost predictable"]
    }
  };

  var PRIORITIES = {
    "short-transfer": {
      label: "Short airport transfer",
      score: function (zone) { return zone.transferMinutes <= 25 ? 6 : zone.transferMinutes <= 45 ? 3 : -3; },
      note: "Transfer time is programme time. Under 25 minutes keeps arrival day usable for a welcome session."
    },
    "beach-gala": {
      label: "Beachfront or outdoor gala",
      zones: { "lara-kundu": 6, "belek": 5, "side-manavgat": 5, "kemer": 4, "antalya-city": 2, "aksu-expo": 0 },
      archetype: "destination-gala",
      note: "Confirm the wet-weather alternative and the generator plan before the venue is signed, not after."
    },
    "golf": {
      label: "Golf programme",
      zones: { "belek": 10, "lara-kundu": 2, "side-manavgat": 1, "antalya-city": 0, "aksu-expo": 0, "kemer": 0 },
      archetype: "golf-resort",
      note: "Belek is where the championship courses are. Block tee times at the same moment as rooms."
    },
    "technical-production": {
      label: "Heavy technical production",
      zones: { "aksu-expo": 6, "lara-kundu": 4, "antalya-city": 4, "belek": 3, "side-manavgat": 1, "kemer": 0 },
      archetype: "convention-centre",
      note: "Ask for the rigging plot and point loads in writing at shortlist stage — it eliminates venues faster than any other question."
    },
    "exhibition-access": {
      label: "Exhibition or vehicle access",
      zones: { "aksu-expo": 8, "antalya-city": 3, "lara-kundu": 2, "belek": 1, "side-manavgat": 0, "kemer": 0 },
      archetype: "convention-centre",
      note: "Door dimensions, ramp gradient and floor loading decide this. Resort ballrooms rarely take a vehicle."
    },
    "city-culture": {
      label: "City & cultural access",
      zones: { "antalya-city": 8, "lara-kundu": 3, "side-manavgat": 3, "kemer": 2, "belek": 1, "aksu-expo": 1 },
      archetype: "city-congress",
      note: "Kaleiçi's old town gives delegates somewhere to go without a coach, which resort zones cannot offer."
    },
    "exclusivity": {
      label: "Exclusive use or buy-out",
      zones: { "kemer": 6, "belek": 5, "side-manavgat": 4, "lara-kundu": 2, "antalya-city": 2, "aksu-expo": 0 },
      archetype: "boutique-exclusive",
      note: "Buy-outs are most achievable in shoulder and low season, and least achievable in July and August."
    },
    "budget": {
      label: "Tight budget",
      zones: { "side-manavgat": 6, "kemer": 4, "lara-kundu": 2, "belek": 0, "antalya-city": 2, "aksu-expo": 1 },
      note: "The biggest lever in Antalya is not the venue — it is the month. Moving a programme out of peak season moves the budget more than any negotiation."
    }
  };

  /* =======================================================================
   * 2. Capacity model
   * =======================================================================
   */
  function capacityBand(guests) {
    if (guests < 60) { return { key: "xs", label: "Under 60", note: "Boardroom and small-meeting territory. Almost every five-star property in the destination can hold you, so select on quality, discretion and transfer time rather than capacity." }; }
    if (guests < 150) { return { key: "s", label: "60–150", note: "The most flexible band in Antalya. You will have real choice across every zone, which means you can optimise for programme quality instead of availability." }; }
    if (guests < 400) { return { key: "m", label: "150–400", note: "Still comfortable for a single resort property, but the shortlist narrows to hotels with a genuine plenary ballroom plus separate breakout space." }; }
    if (guests < 800) { return { key: "l", label: "400–800", note: "Now a large-format search. You need a resort with a ballroom that holds the full group in one sitting and enough rooms in one building to avoid splitting the group." }; }
    if (guests < 1500) { return { key: "xl", label: "800–1,500", note: "A small number of properties can do this on one site. Expect either a large Lara/Kundu or Belek resort, or a split between a convention centre and a hotel block." }; }
    return { key: "xxl", label: "1,500+", note: "Convention-centre territory. The ANFAŞ Antalya Expo Center handles conference configurations to around 4,000; accommodation becomes a multi-hotel block with a shuttle operation." };
  }

  /* =======================================================================
   * 3. Matching engine
   * =======================================================================
   */
  function scoreZones(state) {
    var format = FORMATS[state.format];
    var band = capacityBand(state.guests);
    var results = [];

    Object.keys(ZONES).forEach(function (key) {
      var zone = ZONES[key];
      var score = (format.zoneWeights[key] || 0) * 2;
      var reasons = [];
      var cautions = [];

      if (format.zoneWeights[key] >= 7) {
        reasons.push("Strong fit for a " + format.label.toLowerCase() + " programme.");
      }

      // Capacity realism: a zone that cannot hold the group is not a shortlist.
      // The penalty scales with how far over the ceiling the group is, so that a
      // zone marginally over it still outranks one several times over. A flat
      // penalty let a large resort zone beat the Expo corridor on a 5,000-delegate
      // congress, which is the opposite of the right answer.
      if (state.guests > zone.capacityCeiling) {
        var overshoot = state.guests / zone.capacityCeiling;
        score -= Math.min(30, 8 + (overshoot - 1) * 12);
        cautions.push("Single-site capacity for " + state.guests + " delegates is unlikely here; this would become a multi-property build.");
      } else if (state.guests > zone.capacityCeiling * 0.7) {
        score -= 3;
        cautions.push("At " + state.guests + " delegates you are near the practical single-site ceiling for this zone — the shortlist will be short.");
      }

      (state.priorities || []).forEach(function (id) {
        var priority = PRIORITIES[id];
        if (!priority) { return; }
        var delta = typeof priority.score === "function"
          ? priority.score(zone)
          : (priority.zones && priority.zones[key] != null ? priority.zones[key] : 0);
        score += delta;
        if (delta >= 5) { reasons.push(priority.label + ": one of the strongest zones in Antalya for this."); }
        if (delta < 0) { cautions.push(priority.label + ": this zone works against that requirement."); }
      });

      results.push({
        key: key,
        zone: zone,
        score: score,
        reasons: reasons,
        cautions: cautions,
        band: band
      });
    });

    results.sort(function (a, b) { return b.score - a.score; });
    return results.filter(function (r) { return r.score > 0; }).slice(0, 3);
  }

  function matchArchetypes(state) {
    var format = FORMATS[state.format];
    var keys = format.archetypes.slice();
    (state.priorities || []).forEach(function (id) {
      var priority = PRIORITIES[id];
      if (priority && priority.archetype && keys.indexOf(priority.archetype) === -1) {
        keys.push(priority.archetype);
      }
    });
    // A convention centre is not a sensible answer for a small group.
    if (state.guests < 400) {
      keys = keys.filter(function (k) { return k !== "convention-centre"; });
    }
    return keys.slice(0, 4).map(function (k) {
      return { key: k, archetype: ARCHETYPES[k] };
    });
  }

  function priorityNotes(state) {
    return (state.priorities || []).map(function (id) {
      return PRIORITIES[id] ? { label: PRIORITIES[id].label, note: PRIORITIES[id].note } : null;
    }).filter(Boolean);
  }

  function match(state) {
    return {
      band: capacityBand(state.guests),
      zones: scoreZones(state),
      archetypes: matchArchetypes(state),
      month: MONTHS[String(state.month)] || null,
      criteria: FORMATS[state.format].criteria,
      notes: priorityNotes(state)
    };
  }

  /* =======================================================================
   * 4. State
   * =======================================================================
   */
  var DEFAULTS = { format: "conference", guests: 150, month: "5", priorities: [] };

  function normalizeState(raw) {
    var state = {
      format: raw && FORMATS[raw.format] ? raw.format : DEFAULTS.format,
      guests: DEFAULTS.guests,
      month: raw && MONTHS[String(raw.month)] ? String(raw.month) : DEFAULTS.month,
      priorities: []
    };
    if (raw && raw.guests != null && isFinite(Number(raw.guests))) {
      state.guests = Math.max(10, Math.min(5000, Math.round(Number(raw.guests))));
    }
    if (raw && Array.isArray(raw.priorities)) {
      state.priorities = raw.priorities.filter(function (id) { return !!PRIORITIES[id]; });
    }
    return state;
  }

  function readStored() {
    try {
      var raw = sessionStorage.getItem(SESSION_KEY);
      return raw ? JSON.parse(raw) : null;
    } catch (err) {
      return null;
    }
  }

  function writeStored(payload) {
    try {
      sessionStorage.setItem(SESSION_KEY, JSON.stringify(payload));
    } catch (err) {
      /* Private browsing or blocked storage: the tool still works, the
         handoff just does not carry over. Never let this break the page. */
    }
  }

  function clearStored() {
    try {
      sessionStorage.removeItem(SESSION_KEY);
    } catch (err) { /* no-op */ }
  }

  function trackEvent(name, params) {
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push(Object.assign({ event: name }, params || {}));
      if (typeof window.gtag === "function") { window.gtag("event", name, params || {}); }
    } catch (err) { /* analytics must never break the tool */ }
  }

  /* =======================================================================
   * 5. Brief serialisation (what the DMC team actually receives)
   * =======================================================================
   */
  var SEASON_LABELS = {
    "low": "low season",
    "shoulder": "shoulder season",
    "peak-mice": "peak MICE season",
    "summer": "peak leisure season"
  };

  function summaryLines(state, result) {
    var lines = [
      FORMATS[state.format].label,
      state.guests + " delegates (" + result.band.label + " band)",
      result.month ? result.month.label + " (" + (SEASON_LABELS[result.month.band] || result.month.band) + ")" : "Month not set"
    ];
    if (result.zones.length) {
      lines.push("Suggested zones: " + result.zones.map(function (z) { return z.zone.label; }).join(", "));
    }
    if (state.priorities.length) {
      lines.push("Priorities: " + state.priorities.map(function (id) { return PRIORITIES[id].label; }).join(", "));
    }
    return lines;
  }

  function buildBrief(state, result) {
    var lines = [
      "Destination: Antalya",
      "Event format: " + FORMATS[state.format].label,
      "Delegates: " + state.guests + " (" + result.band.label + ")",
      "Target month: " + (result.month ? result.month.label : "not set")
    ];
    if (state.priorities.length) {
      lines.push("Priorities: " + state.priorities.map(function (id) { return PRIORITIES[id].label; }).join(", "));
    }
    if (result.zones.length) {
      lines.push("Matched zones: " + result.zones.map(function (z) {
        return z.zone.label + " (" + z.zone.transfer + ")";
      }).join(" | "));
    }
    if (result.archetypes.length) {
      lines.push("Matched venue types: " + result.archetypes.map(function (a) { return a.archetype.label; }).join(" | "));
    }
    return lines.join("\n");
  }

  /* =======================================================================
   * 6. Rendering
   * =======================================================================
   */
  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) { node.className = className; }
    if (text != null) { node.textContent = text; }
    return node;
  }

  function renderZone(entry, index) {
    var card = el("article", "vm-zone" + (index === 0 ? " vm-zone--lead" : ""));
    var head = el("header", "vm-zone__head");
    if (index === 0) { head.appendChild(el("span", "vm-zone__badge", "Best match")); }
    head.appendChild(el("h4", "vm-zone__title", entry.zone.label));
    head.appendChild(el("p", "vm-zone__transfer", entry.zone.transfer));
    card.appendChild(head);

    card.appendChild(el("p", "vm-zone__profile", entry.zone.profile));

    var tags = el("ul", "vm-zone__tags");
    entry.zone.strengths.forEach(function (s) { tags.appendChild(el("li", null, s)); });
    card.appendChild(tags);

    entry.reasons.slice(0, 2).forEach(function (reason) {
      card.appendChild(el("p", "vm-zone__reason", reason));
    });

    var caution = el("p", "vm-zone__caution");
    caution.appendChild(el("strong", null, "Watch out: "));
    caution.appendChild(document.createTextNode(entry.cautions.length ? entry.cautions[0] : entry.zone.watchOut));
    card.appendChild(caution);

    return card;
  }

  function renderResult(root, state, result) {
    var out = root.querySelector("[data-vm-result]");
    if (!out) { return; }
    out.innerHTML = "";

    var intro = el("div", "vm-result__intro");
    intro.appendChild(el("h3", null, "Your Antalya shortlist direction"));
    intro.appendChild(el("p", "vm-result__band", result.band.note));
    if (result.month) {
      var season = el("p", "vm-result__season");
      season.appendChild(el("strong", null, result.month.label + ": "));
      season.appendChild(document.createTextNode(result.month.note));
      intro.appendChild(season);
    }
    out.appendChild(intro);

    if (result.zones.length) {
      out.appendChild(el("h4", "vm-result__heading", "Where to look"));
      var zoneWrap = el("div", "vm-zones");
      result.zones.forEach(function (entry, i) { zoneWrap.appendChild(renderZone(entry, i)); });
      out.appendChild(zoneWrap);
    } else {
      out.appendChild(el("p", "vm-result__empty", "That combination of group size and requirements does not have an obvious single-zone answer in Antalya — which is useful to know early. Send us the brief and we will tell you honestly whether Antalya is the right destination for it."));
    }

    if (result.archetypes.length) {
      out.appendChild(el("h4", "vm-result__heading", "What kind of venue to ask for"));
      var typeList = el("ul", "vm-types");
      result.archetypes.forEach(function (item) {
        var li = el("li", "vm-types__item");
        li.appendChild(el("strong", null, item.archetype.label));
        li.appendChild(el("p", null, item.archetype.summary));
        li.appendChild(el("p", "vm-types__best", item.archetype.bestFor));
        typeList.appendChild(li);
      });
      out.appendChild(typeList);
    }

    out.appendChild(el("h4", "vm-result__heading", "What decides it for this format"));
    var criteria = el("ul", "checklist");
    result.criteria.forEach(function (c) { criteria.appendChild(el("li", null, c)); });
    out.appendChild(criteria);

    if (result.notes.length) {
      out.appendChild(el("h4", "vm-result__heading", "Notes on your priorities"));
      var notes = el("ul", "vm-notes");
      result.notes.forEach(function (n) {
        var li = el("li", null);
        li.appendChild(el("strong", null, n.label + ": "));
        li.appendChild(document.createTextNode(n.note));
        notes.appendChild(li);
      });
      out.appendChild(notes);
    }

    var cta = el("div", "vm-cta");
    cta.appendChild(el("h4", null, "Turn this into an actual shortlist"));
    cta.appendChild(el("p", null, "We will come back with named properties checked for availability on your dates, with capacities, transfer times and the operational caveats that matter. Your answers above carry across — you will not retype them."));
    var actions = el("div", "vm-cta__actions");
    var primary = el("a", "btn btn--primary", "Get a Venue Shortlist");
    primary.setAttribute("href", "/request-proposal/?source=venue-sourcing-antalya");
    primary.setAttribute("data-vm-proposal-cta", "");
    actions.appendChild(primary);
    var secondary = el("a", "btn btn--ghost", "Estimate the budget first");
    secondary.setAttribute("href", "/event-cost-calculator/");
    actions.appendChild(secondary);
    cta.appendChild(actions);
    out.appendChild(cta);

    out.hidden = false;
  }

  /* =======================================================================
   * 7. Tool boot
   * =======================================================================
   */
  function readStateFromForm(root) {
    var priorities = [];
    root.querySelectorAll("[data-vm-priority]:checked").forEach(function (input) {
      priorities.push(input.value);
    });
    return normalizeState({
      format: root.querySelector("[data-vm-format]").value,
      guests: root.querySelector("[data-vm-guests]").value,
      month: root.querySelector("[data-vm-month]").value,
      priorities: priorities
    });
  }

  function initMatcher(root) {
    var form = root.querySelector("[data-vm-form]");
    if (!form) { return; }

    function run(isInitial) {
      var state = readStateFromForm(root);
      var result = match(state);
      renderResult(root, state, result);
      writeStored({
        format: state.format,
        guests: state.guests,
        month: state.month,
        priorities: state.priorities,
        summary: summaryLines(state, result),
        brief: buildBrief(state, result)
      });
      if (!isInitial) {
        trackEvent("venue_matcher_run", {
          venue_format: state.format,
          venue_guests: state.guests,
          venue_month: state.month,
          venue_zone: result.zones.length ? result.zones[0].zone.label : "none"
        });
      }
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      run(false);
      var out = root.querySelector("[data-vm-result]");
      if (out && typeof out.scrollIntoView === "function") {
        out.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });

    form.addEventListener("change", function () { run(false); });

    root.addEventListener("click", function (event) {
      var link = event.target && event.target.closest ? event.target.closest("[data-vm-proposal-cta]") : null;
      if (link) {
        var state = readStateFromForm(root);
        trackEvent("venue_matcher_shortlist_clicked", {
          venue_format: state.format,
          venue_guests: state.guests
        });
      }
    });

    run(true);
  }

  /* =======================================================================
   * 8. Proposal page integration
   * =======================================================================
   */
  function initProposalIntegration() {
    var form = document.querySelector("[data-proposal-form]");
    var summary = document.querySelector("[data-venue-summary]");
    if (!form || !summary) { return; }
    var stored = readStored();
    if (!stored || !stored.brief) { return; }

    var dl = summary.querySelector("dl");
    if (dl) {
      (stored.summary || []).forEach(function (line) {
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
    }

    var destinationSelect = form.elements.destination;
    if (destinationSelect) {
      for (var i = 0; i < destinationSelect.options.length; i++) {
        if (destinationSelect.options[i].text === "Antalya") {
          destinationSelect.value = destinationSelect.options[i].value || destinationSelect.options[i].text;
          break;
        }
      }
    }

    var groupSelect = form.elements.group_size;
    if (groupSelect) {
      var guests = Number(stored.guests) || 0;
      var target = guests < 20 ? "Under 20"
        : guests <= 50 ? "20–50"
        : guests <= 100 ? "51–100"
        : guests <= 250 ? "101–250"
        : guests <= 500 ? "251–500"
        : "500+";
      for (var j = 0; j < groupSelect.options.length; j++) {
        if (groupSelect.options[j].text === target) {
          groupSelect.value = groupSelect.options[j].value || groupSelect.options[j].text;
          break;
        }
      }
    }

    var projectSelect = form.elements.project_type;
    if (projectSelect) {
      var projectMap = {
        "conference": "Meeting / Conference",
        "corporate-meeting": "Meeting / Conference",
        "congress-exhibition": "Congress / Exhibition",
        "incentive": "Incentive Travel",
        "gala": "Gala / Special Event",
        "product-launch": "Corporate Event",
        "retreat": "Corporate Event",
        "kickoff": "Corporate Event"
      };
      var label = projectMap[stored.format];
      if (label) {
        for (var k = 0; k < projectSelect.options.length; k++) {
          if (projectSelect.options[k].text === label) {
            projectSelect.value = projectSelect.options[k].value || projectSelect.options[k].text;
            break;
          }
        }
      }
    }

    // Structured brief read by /api/request-proposal and merged into the
    // lead email, same contract as the calculator's hidden field.
    var briefField = document.createElement("input");
    briefField.setAttribute("type", "hidden");
    briefField.setAttribute("name", "venue_brief");
    briefField.value = stored.brief;
    form.appendChild(briefField);

    summary.hidden = false;
    trackEvent("venue_matcher_proposal_form_view", { venue_format: stored.format });

    form.addEventListener("submit", function () {
      trackEvent("venue_matcher_proposal_submitted", { venue_format: stored.format });
      clearStored();
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var roots = document.querySelectorAll("[data-venue-matcher]");
    if (roots.length) {
      roots.forEach(function (root) { initMatcher(root); });
    }
    initProposalIntegration();
  });
}());
