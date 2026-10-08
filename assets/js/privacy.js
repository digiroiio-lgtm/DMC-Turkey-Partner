/* Optional analytics is blocked until the visitor accepts it. */
(function () {
  "use strict";
  var script = document.currentScript;
  var gaId = script.dataset.ga4 || "";
  var gtmId = script.dataset.gtm || "";
  var key = "dmc_cookie_choice_v1";
  var lifetime = 180 * 24 * 60 * 60 * 1000;
  var choice = null;
  var loaded = false;
  var banner;
  var returnFocus;

  function readChoice() {
    try {
      var saved = JSON.parse(localStorage.getItem(key));
      return saved && saved.version === 1 && typeof saved.analytics === "boolean" &&
        typeof saved.savedAt === "number" && saved.savedAt <= Date.now() &&
        Date.now() - saved.savedAt < lifetime ? saved.analytics : null;
    } catch (error) { return null; }
  }

  function clearOptionalStorage() {
    try {
      sessionStorage.removeItem("proposal_campaign");
      sessionStorage.removeItem("proposal_landing_page");
    } catch (error) { /* Storage may be disabled. */ }
    document.cookie.split(";").forEach(function (cookie) {
      var name = cookie.split("=")[0].trim();
      if (!/^_ga(?:_|$)|^_gid$|^_gat/.test(name)) { return; }
      var expiry = name + "=; Max-Age=0; path=/; SameSite=Lax";
      document.cookie = expiry;
      var host = location.hostname.split(".");
      for (var i = 0; i < host.length - 1; i++) {
        var domain = host.slice(i).join(".");
        document.cookie = expiry + "; domain=" + domain;
        document.cookie = expiry + "; domain=." + domain;
      }
    });
  }

  function safeUrl(value) {
    try { var url = new URL(value, location.origin); return url.origin + url.pathname; }
    catch (error) { return ""; }
  }

  function startAnalytics() {
    if (choice !== true || loaded || (!gaId && !gtmId)) { return; }
    loaded = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("consent", "default", { analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
    window.gtag("consent", "update", { analytics_storage: "granted" });
    var tag = document.createElement("script");
    tag.async = true;
    if (gtmId) {
      window.dataLayer.push({ "gtm.start": Date.now(), event: "gtm.js" });
      tag.src = "https://www.googletagmanager.com/gtm.js?id=" + encodeURIComponent(gtmId);
    } else {
      window["ga-disable-" + gaId] = false;
      window.gtag("js", new Date());
      window.gtag("config", gaId, { allow_google_signals: false, allow_ad_personalization_signals: false,
        page_location: safeUrl(location.href), page_referrer: safeUrl(document.referrer) });
      tag.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(gaId);
    }
    document.head.appendChild(tag);
  }

  function hideBanner() {
    banner.hidden = true;
    if (returnFocus) { returnFocus.focus(); returnFocus = null; }
  }

  function saveChoice(accepted) {
    choice = accepted;
    try { localStorage.setItem(key, JSON.stringify({ version: 1, analytics: accepted, savedAt: Date.now() })); }
    catch (error) { /* The current-page choice still applies. */ }
    if (accepted) { startAnalytics(); }
    else {
      window["ga-disable-" + gaId] = true;
      clearOptionalStorage();
      window.dataLayer = [];
      // Unload a tag that was already accepted on this page.
      if (loaded) { location.reload(); return; }
    }
    hideBanner();
  }

  window.dmcPrivacy = {
    analyticsAllowed: function () { return choice === true; },
    trackEvent: function (name, params) {
      if (choice !== true) { return; }
      var clean = Object.assign({}, params || {});
      ["page_location", "page_referrer", "landing_page", "submission_page"].forEach(function (field) {
        if (clean[field]) { clean[field] = safeUrl(clean[field]); }
      });
      if (gtmId) { window.dataLayer.push(Object.assign({ event: name }, clean)); }
      else if (typeof window.gtag === "function") { window.gtag("event", name, clean); }
    }
  };

  choice = readChoice();
  if (choice === true) { startAnalytics(); }
  else { clearOptionalStorage(); }

  banner = document.createElement("section");
  banner.className = "cookie-banner";
  banner.setAttribute("aria-labelledby", "cookie-banner-title");
  banner.hidden = choice !== null;
  banner.innerHTML = '<div><h2 id="cookie-banner-title">Your privacy choices</h2>' +
    '<p>We use essential storage for your preferences and requested features. With your permission, Google Analytics helps us understand site use. You can use the site and send a brief without analytics.</p>' +
    '<a href="/cookie-policy/">Cookie Policy</a> · <a href="/privacy-policy/">Privacy Policy</a></div>' +
    '<div class="cookie-banner__actions"><button type="button" class="btn btn--ghost" data-cookie-reject>Reject optional analytics</button>' +
    '<button type="button" class="btn btn--ghost" data-cookie-accept>Accept optional analytics</button></div>';
  document.body.appendChild(banner);
  banner.querySelector("[data-cookie-reject]").addEventListener("click", function () { saveChoice(false); });
  banner.querySelector("[data-cookie-accept]").addEventListener("click", function () { saveChoice(true); });
  document.querySelectorAll("[data-cookie-settings]").forEach(function (button) {
    button.addEventListener("click", function () {
      returnFocus = button;
      banner.hidden = false;
      banner.querySelector("[data-cookie-reject]").focus();
    });
  });
  banner.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && choice !== null) { hideBanner(); }
  });
  window.addEventListener("storage", function (event) {
    if (event.key !== key) { return; }
    var next = readChoice();
    if (choice === true && next !== true) {
      choice = next;
      window["ga-disable-" + gaId] = true;
      clearOptionalStorage();
      location.reload();
    } else {
      choice = next;
      banner.hidden = next !== null;
      if (next === true) { startAnalytics(); }
    }
  });
})();
