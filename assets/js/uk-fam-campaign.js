/*
 * UK Agency Fam Trip 2027 campaign: pop-up (every page) and application form
 * (/uk-agency-fam-trip/). Disabled by default: with enabled=false this file does
 * nothing except fill the landing page's "applications open soon" state.
 *
 * Settings live in campaign/uk-fam-trip.json; `python3 tools/fam_trip_build.py`
 * writes them into the block below. Do not edit the block by hand.
 */
(function () {
  "use strict";

  /* uk-fam-config:begin */
  var CONFIG = {
      "enabled": false,
      "campaignName": "uk_fam_trip_2027",
      "targetCountry": "GB",
      "popupDelayMs": 15000,
      "popupScrollThreshold": 50,
      "dismissalDays": 7,
      "campaignPeriod": "January–March 2027 (proposed)",
      "applicationStatus": "Register Interest",
      "formspreeEndpoint": ""
  };
  /* uk-fam-config:end */

  window.DMC_UK_FAM = CONFIG;

  var LANDING = "/uk-agency-fam-trip/";
  var STATE_KEY = "dmc_fam_state_v1";
  var SHOWN_KEY = "dmc_fam_shown";
  var GEO_KEY = "dmc_fam_geo";
  var CSS_HREF = "/assets/css/uk-fam.css";
  var IMAGE = "/assets/img/mapfre-sigorta-antalya-gala-dinner";
  var onLanding = location.pathname.indexOf(LANDING) === 0 || location.pathname === "/uk-agency-fam-trip";

  function track(name, extra) {
    if (!window.dmcPrivacy) { return; }
    window.dmcPrivacy.trackEvent(name, Object.assign({ campaign_name: CONFIG.campaignName }, extra || {}));
  }

  function readState() {
    try { return JSON.parse(localStorage.getItem(STATE_KEY)) || {}; } catch (error) { return {}; }
  }

  function writeState(patch) {
    try { localStorage.setItem(STATE_KEY, JSON.stringify(Object.assign(readState(), patch))); }
    catch (error) { /* Storage can be unavailable; the pop-up is then limited to the session. */ }
  }

  function markApplied() { writeState({ applied: true, appliedAt: Date.now() }); }

  // --- Landing page: application form ---------------------------------------------

  function initLanding() {
    var root = document.querySelector("[data-fam-apply]");
    if (!root) { return; }
    var closed = root.querySelector("[data-fam-closed]");
    var form = root.querySelector("[data-fam-form]");
    var success = root.querySelector("[data-fam-success]");
    var error = root.querySelector("[data-fam-error]");
    track("fam_landing_view");

    // The form opens only when the campaign is enabled AND a Formspree endpoint is set.
    // Otherwise the page stays in its "applications open soon" state and nothing is submitted.
    if (!CONFIG.enabled || !/^https:\/\/formspree\.io\/f\/[A-Za-z0-9]+$/.test(CONFIG.formspreeEndpoint || "")) { return; }
    if (closed) { closed.hidden = true; }
    form.hidden = false;

    var loadedAt = Date.now();
    var started = false;
    var submitting = false;
    var done = false;
    var button = form.querySelector('button[type="submit"]');
    var label = button.textContent;
    var params = new URLSearchParams(location.search);
    form.elements.campaign_source.value = CONFIG.campaignName;
    form.elements.landing_page.value = location.origin + location.pathname;
    if (window.dmcPrivacy && window.dmcPrivacy.analyticsAllowed()) {
      ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
        form.elements[key].value = params.get(key) || "";
      });
    }
    form.elements.submission_source.value = params.get("src") || "direct";

    form.addEventListener("focusin", function () {
      if (!started) { started = true; track("fam_form_start"); }
    });

    function fail(message, field) {
      error.textContent = message;
      error.hidden = false;
      if (field) { field.focus(); }
    }

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (submitting || done) { return; }
      error.hidden = true;
      var required = form.querySelectorAll("[required]");
      for (var i = 0; i < required.length; i++) {
        var field = required[i];
        var empty = field.type === "checkbox" ? !field.checked : !String(field.value).trim();
        if (empty) { fail("Please complete the required fields (" + (field.getAttribute("data-label") || field.name) + ").", field); return; }
      }
      var email = form.elements.email;
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim())) { fail("Please enter a valid business email address.", email); return; }
      var website = form.elements.website.value.trim();
      if (website && !/^(https?:\/\/)?[^\s.]+\.[^\s]{2,}$/i.test(website)) { fail("Please enter a valid website address or leave it blank.", form.elements.website); return; }
      // Bots fill the honeypot or submit within moments of loading the page.
      if (form.elements._gotcha.value || Date.now() - loadedAt < 3000) { fail("Please review your details and try again.", null); return; }

      form.elements.submitted_at.value = new Date().toISOString();
      form.elements.consent_timestamp.value = form.elements.submitted_at.value;
      form.elements.marketing_optin_status.value = form.elements.marketing_optin.checked ? "Yes" : "No";
      track("fam_form_submit");
      submitting = true;
      button.disabled = true;
      button.setAttribute("aria-busy", "true");
      button.textContent = "Sending…";

      fetch(CONFIG.formspreeEndpoint, {
        method: "POST",
        headers: { Accept: "application/json" },
        body: new FormData(form)
      }).then(function (response) {
        return response.json().catch(function () { return {}; }).then(function (data) {
          if (!response.ok || data.ok === false || data.error) {
            var failure = new Error("Submission failed");
            failure.detail = data && data.errors && data.errors[0] && data.errors[0].message;
            throw failure;
          }
        });
      }).then(function () {
        // Reached only after Formspree confirmed the submission.
        done = true;
        submitting = false;
        markApplied();
        track("fam_lead_success");
        form.hidden = true;
        success.hidden = false;
        var heading = success.querySelector("h2");
        if (heading) { heading.focus({ preventScroll: false }); }
      }).catch(function (failure) {
        submitting = false;
        button.disabled = false;
        button.removeAttribute("aria-busy");
        button.textContent = label;
        fail((failure && failure.detail) || "We could not send your application. Your details are still here: please try again or email hello@dmcturkeypartner.com.", null);
      });
    });
  }

  // --- Pop-up ------------------------------------------------------------------------

  function excludedPage() {
    var path = location.pathname;
    if (onLanding) { return true; }
    if (/^\/(cop31|request-proposal|contact|antalya-transfer-prices)/.test(path)) { return true; }
    if (document.querySelector("[data-proposal-form], [data-fam-form]")) { return true; }
    var lead = document.querySelector('meta[name="dmc:lead-source"]');
    if (lead && lead.getAttribute("content") === "COP31") { return true; }
    try {
      var campaign = JSON.parse(sessionStorage.getItem("proposal_campaign"));
      if (campaign && campaign.lead_source === "COP31") { return true; }
    } catch (error) { /* ignore */ }
    return false;
  }

  function suppressed() {
    try { if (sessionStorage.getItem(SHOWN_KEY)) { return true; } } catch (error) { /* ignore */ }
    var state = readState();
    if (state.applied) { return true; }
    return Boolean(state.dismissedAt && Date.now() - state.dismissedAt < CONFIG.dismissalDays * 86400000);
  }

  function whenConsentChosen(callback) {
    if (!window.dmcPrivacy || typeof window.dmcPrivacy.hasChoice !== "function") { return; }
    if (window.dmcPrivacy.hasChoice()) { callback(); return; }
    window.addEventListener("dmc:consent-choice", function once() {
      window.removeEventListener("dmc:consent-choice", once);
      callback();
    });
  }

  function isTargetCountry() {
    try {
      var cached = sessionStorage.getItem(GEO_KEY);
      if (cached) { return Promise.resolve(cached === CONFIG.targetCountry); }
    } catch (error) { /* ignore */ }
    return fetch("/api/geo", { cache: "no-store", credentials: "omit" })
      .then(function (response) { return response.ok ? response.json() : {}; })
      .then(function (data) {
        var country = data && typeof data.country === "string" ? data.country : "";
        try { if (country) { sessionStorage.setItem(GEO_KEY, country); } } catch (error) { /* ignore */ }
        return country === CONFIG.targetCountry;
      })
      .catch(function () { return false; });
  }

  function loadStyles() {
    return new Promise(function (resolve) {
      if (document.querySelector('link[href="' + CSS_HREF + '"]')) { resolve(); return; }
      var link = document.createElement("link");
      link.rel = "stylesheet";
      link.href = CSS_HREF;
      link.onload = resolve;
      link.onerror = resolve;
      document.head.appendChild(link);
      setTimeout(resolve, 2000);
    });
  }

  var CHECK = '<svg class="fam-popup__tick" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><circle cx="10" cy="10" r="8.5" fill="none" stroke="#1f9d55" stroke-width="1.5"/><path d="M6 10.3l2.8 2.8L14 7.6" fill="none" stroke="#1f9d55" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  var PLANE = '<svg class="fam-popup__tick" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M2.5 10.5l15-7-4 13-3.2-4.2-3.3 2.2.5-3.6z" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/></svg>';

  function buildDialog() {
    var dialog = document.createElement("dialog");
    dialog.className = "fam-popup";
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "fam-popup-title");
    dialog.setAttribute("aria-describedby", "fam-popup-desc");
    dialog.innerHTML =
      '<div class="fam-popup__panel">' +
        '<div class="fam-popup__top"><p class="fam-popup__eyebrow">Exclusive UK Agency Invitation</p>' +
          '<button type="button" class="fam-popup__close" aria-label="Close" data-fam-dismiss="close_button">' +
            '<svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M4 4l12 12M16 4L4 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg></button></div>' +
        '<img class="fam-popup__image" src="' + IMAGE + '-640.webp" srcset="' + IMAGE + '-640.webp 640w, ' + IMAGE + '.webp 1179w" sizes="(max-width: 640px) 100vw, 712px" width="1179" height="798" alt="Gala dinner with stage lighting and LED screens at a corporate event in Antalya">' +
        '<h2 id="fam-popup-title" class="fam-popup__title" tabindex="-1">Experience Antalya &amp; Belek. Become Our UK Agency Partner.</h2>' +
        '<p id="fam-popup-desc" class="fam-popup__text">Join a curated familiarisation trip for UK incentive and MICE decision-makers. Discover venues, meet our local operations team and explore white-label delivery opportunities.</p>' +
        '<ul class="fam-popup__badges"><li>3 Nights</li><li>2027</li><li>Limited Applications</li></ul>' +
        '<ul class="fam-popup__benefits"><li>' + CHECK + 'Hosted accommodation and local programme</li><li>' + CHECK + 'Hotel inspections and DMC networking</li><li>' + PLANE + 'Flights arranged by participants</li></ul>' +
        '<div class="fam-popup__actions"><a class="btn fam-popup__cta" href="' + LANDING + '?src=fam-popup" data-fam-cta>Apply for an Invitation <span aria-hidden="true">→</span></a>' +
          '<button type="button" class="fam-popup__later" data-fam-dismiss="maybe_later">Maybe Later</button></div>' +
        '<p class="fam-popup__note">Applications are reviewed individually. Participation is subject to confirmation.</p>' +
      '</div>';
    return dialog;
  }

  function show(trigger) {
    loadStyles().then(function () {
      var dialog = buildDialog();
      document.body.appendChild(dialog);
      var method = "dismiss";
      var scrollbar = window.innerWidth - document.documentElement.clientWidth;
      document.documentElement.classList.add("has-fam-popup");
      if (scrollbar > 0) { document.body.style.paddingRight = scrollbar + "px"; }
      var opener = document.activeElement;

      dialog.addEventListener("click", function (event) {
        var closer = event.target.closest ? event.target.closest("[data-fam-dismiss]") : null;
        if (closer) { method = closer.getAttribute("data-fam-dismiss"); dialog.close(); return; }
        if (event.target.closest && event.target.closest("[data-fam-cta]")) {
          method = "cta";
          track("fam_popup_click", { trigger: trigger });
          return;
        }
        if (event.target === dialog) { method = "backdrop"; dialog.close(); }
      });
      dialog.addEventListener("cancel", function () { method = "escape"; });
      dialog.addEventListener("keydown", function (event) {
        if (event.key !== "Tab") { return; }
        var items = Array.prototype.filter.call(dialog.querySelectorAll("a[href], button:not([disabled])"), function (node) { return node.offsetParent !== null; });
        if (!items.length) { return; }
        var first = items[0];
        var last = items[items.length - 1];
        var active = document.activeElement;
        if (event.shiftKey && (active === first || active === dialog.querySelector("#fam-popup-title"))) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && active === last) { event.preventDefault(); first.focus(); }
      });
      dialog.addEventListener("close", function () {
        document.documentElement.classList.remove("has-fam-popup");
        document.body.style.paddingRight = "";
        if (method !== "cta") {
          writeState({ dismissedAt: Date.now() });
          track("fam_popup_dismiss", { method: method });
          if (opener && opener.focus && document.contains(opener)) { opener.focus({ preventScroll: true }); }
        }
        dialog.remove();
      });

      try { sessionStorage.setItem(SHOWN_KEY, "1"); } catch (error) { /* ignore */ }
      dialog.showModal();
      dialog.querySelector("#fam-popup-title").focus({ preventScroll: true });
      track("fam_popup_view", { trigger: trigger });
    });
  }

  function blocked() {
    if (document.querySelector("dialog[open]")) { return true; }
    var banner = document.querySelector(".cookie-banner");
    if (banner && !banner.hidden) { return true; }
    var active = document.activeElement;
    return Boolean(active && /^(INPUT|TEXTAREA|SELECT)$/.test(active.tagName));
  }

  function armTriggers() {
    var fired = false;
    var timer;
    function fire(trigger) {
      if (fired) { return; }
      if (blocked()) { timer = setTimeout(function () { fire(trigger); }, 3000); return; }
      fired = true;
      clearTimeout(timer);
      window.removeEventListener("scroll", onScroll);
      show(trigger);
    }
    function onScroll() {
      if (fired) { return; }
      var scrollable = document.documentElement.scrollHeight - window.innerHeight;
      var percent = scrollable > 0 ? (window.scrollY / scrollable) * 100 : 0;
      if (percent >= CONFIG.popupScrollThreshold) { fire("scroll"); }
    }
    timer = setTimeout(function () { fire("delay"); }, CONFIG.popupDelayMs);
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  function initPopup() {
    if (!CONFIG.enabled || excludedPage() || suppressed()) { return; }
    whenConsentChosen(function () {
      if (suppressed()) { return; }
      isTargetCountry().then(function (isTarget) {
        if (isTarget) { armTriggers(); }
      });
    });
  }

  if (onLanding) {
    if (document.readyState === "loading") { document.addEventListener("DOMContentLoaded", initLanding); } else { initLanding(); }
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initPopup);
  } else {
    initPopup();
  }
})();
