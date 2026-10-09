/*
 * DmcTurkeyPartner.com — minimal global JS
 * Handles the mobile navigation toggle and desktop dropdown menus.
 * No frameworks, no dependencies.
 */
(function () {
  "use strict";

  var GA4_EVENT_MAP = {
    cop31_whatsapp_click:     "whatsapp_click",
    cop31_proposal_cta_click: "request_proposal_click"
  };

  document.addEventListener("DOMContentLoaded", function () {
    var yearEl = document.getElementById("year");
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }

    initNavigation();

    initEventFilters();
    initWorksFilters();
    initEventTracking();
    initEventCostPageView();
    initGuideToc();
    initProposalCtas();
    initProposalForm();
    initNewsFilters();
    initEmailTracking();
    initPhoneTracking();
    initBookCallTracking();
    initStickyCta();
    initOffPeakOffer();
  });

  // Category filter for the COP31 news hub. Progressive enhancement: without
  // JS every card is already in the DOM and visible, so the hub degrades to a
  // plain reverse-chronological list rather than an empty page.
  function initNewsFilters() {
    var container = document.querySelector("[data-news-filters]");
    var grid = document.querySelector("[data-news-grid]");
    if (!container || !grid) {
      return;
    }
    var chips = Array.prototype.slice.call(container.querySelectorAll(".news-chip"));
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".news-card"));
    var empty = document.querySelector("[data-news-empty]");

    function apply(filter) {
      var shown = 0;
      cards.forEach(function (card) {
        var match = filter === "all" || card.getAttribute("data-category") === filter;
        card.hidden = !match;
        if (match) { shown += 1; }
      });
      chips.forEach(function (chip) {
        chip.classList.toggle("is-active", chip.getAttribute("data-filter") === filter);
      });
      if (empty) { empty.hidden = shown !== 0; }
      trackEvent("cop31_news_filter", { filter: filter });
    }

    chips.forEach(function (chip) {
      chip.addEventListener("click", function () {
        apply(chip.getAttribute("data-filter"));
      });
    });

    // Article kickers link back as /cop31-news/?c=<category>, so arriving from
    // an article opens the hub already filtered to that category.
    var requested = new URLSearchParams(window.location.search).get("c");
    if (requested && chips.some(function (c) { return c.getAttribute("data-filter") === requested; })) {
      apply(requested);
    }
  }

  // Mobile breakpoint shared with the drawer rules in main.css. The drawer only
  // exists below it; above it the desktop mega menu is untouched.
  var MOBILE_QUERY = "(max-width: 720px)";

  function isMobileNav() {
    return window.matchMedia(MOBILE_QUERY).matches;
  }

  function initNavigation() {
    var header = document.querySelector(".site-header");
    var nav = document.querySelector(".site-nav");
    var navToggle = document.querySelector(".site-nav__toggle");
    var groups = Array.prototype.slice.call(document.querySelectorAll(".nav-group"));
    var megaHeadings = Array.prototype.slice.call(
      document.querySelectorAll(".nav-mega__heading")
    );
    if (!nav || !navToggle) {
      return;
    }

    var lockedScrollY = 0;

    function setExpanded(el, open) {
      if (el) {
        el.setAttribute("aria-expanded", String(open));
      }
    }

    // The bar is fixed while the drawer is open, so the drawer needs its real
    // height as top padding or the first link hides underneath it.
    function measureBar() {
      if (header) {
        document.documentElement.style.setProperty(
          "--nav-bar-height",
          header.offsetHeight + "px"
        );
      }
    }

    function closeGroups() {
      groups.forEach(function (group) {
        group.classList.remove("is-open");
        setExpanded(group.querySelector(".nav-group__trigger"), false);
      });
      closeMegaSections();
    }

    // Desktop keeps every COP31 panel open, so collapsing them there would only
    // report a state the user cannot see and cannot change.
    function closeMegaSections() {
      if (!isMobileNav()) {
        return;
      }
      megaHeadings.forEach(function (heading) {
        heading.parentNode.classList.remove("is-open");
        setExpanded(heading, false);
      });
    }

    function openDrawer() {
      measureBar();
      lockedScrollY = window.scrollY || window.pageYOffset || 0;
      // Taking the body out of flow collapses the document, and scroll
      // anchoring reacts by shifting the offset ~290px so the restore lands in
      // the wrong place. Suspend anchoring for the whole open/close cycle.
      document.documentElement.style.overflowAnchor = "none";
      document.body.style.top = -lockedScrollY + "px";
      document.body.classList.add("nav-open");
      nav.classList.add("is-open");
      setExpanded(navToggle, true);
      navToggle.setAttribute("aria-label", "Close menu");
    }

    function closeDrawer() {
      if (!document.body.classList.contains("nav-open")) {
        return;
      }
      document.body.classList.remove("nav-open");
      document.body.style.top = "";
      // The site sets html { scroll-behavior: smooth }. Left alone the restore
      // animates and the page visibly flies back, so it is suspended for this
      // one jump.
      var root = document.documentElement;
      var previousBehavior = root.style.scrollBehavior;
      root.style.scrollBehavior = "auto";
      window.scrollTo(0, lockedScrollY);
      root.style.scrollBehavior = previousBehavior;
      // Anchoring must stay off until the reflow from un-fixing the body has
      // actually been laid out and painted. A single rAF runs before that pass,
      // which is early enough for anchoring to still shift the offset, so this
      // waits for the frame after it.
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          root.style.overflowAnchor = "";
        });
      });
      nav.classList.remove("is-open");
      setExpanded(navToggle, false);
      navToggle.setAttribute("aria-label", "Open menu");
      closeGroups();
    }

    navToggle.setAttribute("aria-label", "Open menu");
    navToggle.addEventListener("click", function () {
      if (document.body.classList.contains("nav-open")) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    // Top-level groups: one open at a time, on both desktop and mobile.
    groups.forEach(function (group) {
      var trigger = group.querySelector(".nav-group__trigger");
      if (!trigger) {
        return;
      }
      trigger.addEventListener("click", function () {
        var willOpen = !group.classList.contains("is-open");
        closeGroups();
        if (willOpen) {
          group.classList.add("is-open");
          setExpanded(trigger, true);
        }
      });
    });

    // COP31 sub-groups. Mobile only: on desktop every panel is always visible,
    // so the heading stays an inert label and its state must not be toggled.
    megaHeadings.forEach(function (heading) {
      heading.addEventListener("click", function () {
        if (!isMobileNav()) {
          return;
        }
        var column = heading.parentNode;
        var willOpen = !column.classList.contains("is-open");
        closeMegaSections();
        if (willOpen) {
          column.classList.add("is-open");
          setExpanded(heading, true);
        }
      });
    });

    // Following a link should leave no drawer behind if navigation is cancelled
    // or the target is on the current page.
    nav.addEventListener("click", function (event) {
      if (event.target.closest && event.target.closest("a")) {
        closeDrawer();
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && document.body.classList.contains("nav-open")) {
        closeDrawer();
        navToggle.focus();
      }
    });

    // Outside-click closes desktop dropdowns. Inside the drawer everything is
    // "outside" some group, so it would collapse the accordion on every tap.
    document.addEventListener("click", function (event) {
      if (isMobileNav() || nav.contains(event.target)) {
        return;
      }
      closeGroups();
    });

    // Keep aria honest across breakpoints: desktop panels are always expanded.
    function syncAria() {
      var mobile = isMobileNav();
      megaHeadings.forEach(function (heading) {
        if (mobile) {
          setExpanded(heading, heading.parentNode.classList.contains("is-open"));
        } else {
          setExpanded(heading, true);
        }
      });
    }

    var mql = window.matchMedia(MOBILE_QUERY);
    var onBreakpointChange = function () {
      if (!isMobileNav()) {
        closeDrawer();
      }
      syncAria();
    };
    if (mql.addEventListener) {
      mql.addEventListener("change", onBreakpointChange);
    } else if (mql.addListener) {
      mql.addListener(onBreakpointChange);
    }
    window.addEventListener("resize", function () {
      if (document.body.classList.contains("nav-open")) {
        measureBar();
      }
    });

    syncAria();
  }

  // Lightweight active-section highlighting for the "On This Page" navigation
  // on long-form guide pages. Falls back silently if unsupported.
  function initGuideToc() {
    var toc = document.querySelector("[data-guide-toc]");
    if (!toc || !("IntersectionObserver" in window)) {
      return;
    }
    var links = toc.querySelectorAll("a[href^='#']");
    var sections = [];
    links.forEach(function (link) {
      var id = link.getAttribute("href").slice(1);
      var section = document.getElementById(id);
      if (section) {
        sections.push({ link: link, section: section });
      }
    });
    if (!sections.length) {
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          var match = sections.filter(function (item) {
            return item.section === entry.target;
          })[0];
          if (match && entry.isIntersecting) {
            links.forEach(function (link) {
              link.removeAttribute("aria-current");
            });
            match.link.setAttribute("aria-current", "true");
          }
        });
      },
      { rootMargin: "-40% 0px -50% 0px" }
    );
    sections.forEach(function (item) {
      observer.observe(item.section);
    });
  }

  // Off-peak opportunity pop-up, shown only on destination pages that carry
  // <body data-offpeak="slug">. Fires after 20 s of visible time or on exit
  // intent, never over the cookie banner, the mobile drawer or a form being
  // filled, and at most once per destination per 30 days.
  /* offseason-data:begin */
  var OFFPEAK = {
    belek: { name: "Belek", window: "December – February", page: "/off-season-events-turkey/belek/" },
    antalya: { name: "Antalya", window: "December – February", page: "/off-season-events-turkey/antalya/" },
    istanbul: { name: "Istanbul", window: "January – February", page: "/off-season-events-turkey/istanbul/" },
    cappadocia: { name: "Cappadocia", window: "December – February (excluding New Year week)", page: "/off-season-events-turkey/cappadocia/" },
    bodrum: { name: "Bodrum", window: "October – April", page: "/off-season-events-turkey/bodrum/" }
  };
  // Percentage shown in the pop-up only when backed by like-for-like quotes (tools/off_season_data.py).
  var OFFPEAK_SAVING = null;
  var OFFPEAK_PEAK = "March – June and September – November";
  /* offseason-data:end */
  // Verified company WhatsApp business number (same as tools/cop31_common.py WHATSAPP_NUMBER).
  var WHATSAPP_NUMBER = "905353998999";
  var OFFPEAK_WHATSAPP = WHATSAPP_NUMBER;
  var SUCCESS_WHATSAPP_MESSAGE = "Hello DMC Turkey Partner, I\u2019ve just submitted an event proposal request through your website. I\u2019d like to discuss my requirements with your team.";
  var OFFPEAK_DELAY = 20;
  var OFFPEAK_REPEAT_DAYS = 30;

  function initOffPeakOffer() {
    var slug = document.body.getAttribute("data-offpeak");
    var data = slug && OFFPEAK[slug];
    if (!data) { return; }
    var storeKey = "dmc_offpeak_" + slug;
    var shownThisLoad = false;

    function alreadyShown() {
      if (shownThisLoad) { return true; }
      try {
        var at = parseInt(localStorage.getItem(storeKey), 10);
        return at > 0 && Date.now() - at < OFFPEAK_REPEAT_DAYS * 864e5;
      } catch (error) { return false; }
    }
    function markShown() {
      shownThisLoad = true;
      try { localStorage.setItem(storeKey, String(Date.now())); } catch (error) { /* once per page load */ }
    }
    if (alreadyShown()) { return; }

    function blocked() {
      var banner = document.querySelector(".cookie-banner");
      if (banner && !banner.hidden) { return true; }
      if (document.body.classList.contains("nav-open")) { return true; }
      if (document.querySelector('[role="dialog"]:not([hidden])')) { return true; }
      var active = document.activeElement;
      return !!(active && /^(INPUT|TEXTAREA|SELECT)$/.test(active.tagName));
    }

    var elapsed = 0;
    var ticker = setInterval(function () {
      if (document.hidden || blocked()) { return; }
      elapsed += 1;
      if (elapsed >= OFFPEAK_DELAY) { open("timer"); }
    }, 1000);

    function onMouseOut(event) {
      if (!event.relatedTarget && event.clientY <= 0 && elapsed >= 3 && !blocked()) { open("exit"); }
    }
    document.addEventListener("mouseout", onMouseOut);

    var lastY = window.scrollY;
    var lastT = Date.now();
    function onScroll() {
      var now = Date.now();
      var y = window.scrollY;
      var depth = (y + window.innerHeight) / document.documentElement.scrollHeight;
      // A fast flick back up after reading half the page: leaving intent on touch.
      if (window.matchMedia("(max-width: 720px)").matches && depth < 0.9 && lastY - y > 600 &&
          now - lastT < 400 && lastY / document.documentElement.scrollHeight > 0.5 && elapsed >= 3 && !blocked()) {
        open("scroll");
      }
      if (now - lastT > 400) { lastY = y; lastT = now; }
    }
    window.addEventListener("scroll", onScroll, { passive: true });

    function stop() {
      clearInterval(ticker);
      document.removeEventListener("mouseout", onMouseOut);
      window.removeEventListener("scroll", onScroll);
    }

    function open(trigger) {
      if (alreadyShown()) { stop(); return; }
      stop();
      markShown();
      var message = "Hello DMC Turkey Partner — we're interested in off-peak dates in " + data.name +
        " (" + data.window + ") for a group event.\nCompany:\nGroup size:\nPreferred dates:";
      var whatsapp = "https://wa.me/" + OFFPEAK_WHATSAPP + "?text=" + encodeURIComponent(message);
      var title = OFFPEAK_SAVING
        ? "Run your " + data.name + " event for up to " + OFFPEAK_SAVING + "% less"
        : "Plan your " + data.name + " event in the off-peak window";
      var text = OFFPEAK_SAVING
        ? "<strong>" + data.window + "</strong> is " + data.name + "’s off-peak window. In like-for-like quotes, off-peak dates have come in up to " +
          OFFPEAK_SAVING + "% below peak-season rates (" + OFFPEAK_PEAK + "). Compare your dates side by side."
        : "<strong>" + data.window + "</strong> is " + data.name + "’s off-peak window. Hotels and venues have more availability and " +
          "room to negotiate, so agencies with flexible dates can price the same programme in more than one window. We show the dates side by side.";
      var note = OFFPEAK_SAVING
        ? "Indicative saving vs peak-season rates; final pricing depends on dates, group size and availability."
        : "Indicative; final pricing depends on dates, group size and availability.";
      var returnFocus = document.activeElement;
      var root = document.createElement("div");
      root.className = "offpeak";
      root.innerHTML =
        '<div class="offpeak__backdrop" data-offpeak-close="backdrop"></div>' +
        '<section class="offpeak__card" role="dialog" aria-modal="true" aria-labelledby="offpeak-title" aria-describedby="offpeak-text">' +
          '<button type="button" class="offpeak__close" data-offpeak-close="close" aria-label="Close">&times;</button>' +
          '<p class="offpeak__eyebrow">Off-peak opportunity · ' + data.name + '</p>' +
          '<h2 class="offpeak__title" id="offpeak-title">' + title + '</h2>' +
          '<p class="offpeak__text" id="offpeak-text">' + text + '</p>' +
          '<ul class="offpeak__points">' +
            '<li>Off-peak and peak dates compared side by side</li>' +
            '<li>Same hotels, venues and production</li>' +
            '<li>Limited dates — first confirmed, first held</li>' +
          '</ul>' +
          '<a class="btn btn--primary offpeak__cta" href="' + data.page + '">Compare Dates &amp; Event Costs</a>' +
          '<a class="offpeak__alt" href="' + whatsapp + '" target="_blank" rel="noopener">Prefer WhatsApp? Ask there</a>' +
          '<button type="button" class="offpeak__dismiss" data-offpeak-close="no_thanks">No thanks</button>' +
          '<p class="offpeak__note">' + note + '</p>' +
        '</section>';
      document.body.appendChild(root);
      document.body.classList.add("offpeak-open");
      var card = root.querySelector(".offpeak__card");
      requestAnimationFrame(function () { root.classList.add("is-visible"); });
      root.querySelector(".offpeak__cta").focus();
      trackEvent("offpeak_popup_view", { destination: slug, trigger: trigger });

      function close(method) {
        document.removeEventListener("keydown", onKey, true);
        document.body.classList.remove("offpeak-open");
        root.remove();
        if (returnFocus && returnFocus.focus) { returnFocus.focus(); }
        if (method) { trackEvent("offpeak_popup_dismiss", { destination: slug, method: method }); }
      }
      function onKey(event) {
        if (event.key === "Escape") { event.preventDefault(); close("esc"); return; }
        if (event.key !== "Tab") { return; }
        var items = card.querySelectorAll("a[href], button");
        var first = items[0];
        var last = items[items.length - 1];
        if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      }
      document.addEventListener("keydown", onKey, true);
      root.addEventListener("click", function (event) {
        var closer = event.target.closest("[data-offpeak-close]");
        if (closer) { close(closer.getAttribute("data-offpeak-close")); return; }
        if (event.target.closest(".offpeak__cta")) {
          trackEvent("offpeak_popup_compare_click", { destination: slug });
          close(null);
        } else if (event.target.closest(".offpeak__alt")) {
          trackEvent("offpeak_popup_whatsapp_click", { destination: slug });
          close(null);
        }
      });
    }
  }

  // Consent-aware analytics dispatch. Never queue events before permission.
  function trackEvent(name, params) {
    if (window.dmcPrivacy) { window.dmcPrivacy.trackEvent(name, params); }
  }

  // Client-side only filtering for the MICE Calendar hub. Deliberately does
  // not write filter state to the URL, so no parameter/crawl-trap pages are
  // generated for search engines.
  function initEventFilters() {
    var grid = document.querySelector("[data-event-grid]");
    var filters = document.querySelectorAll("[data-event-filter]");
    if (!grid || !filters.length) {
      return;
    }
    var cards = grid.querySelectorAll("[data-event-card]");

    function applyFilters() {
      var active = {};
      filters.forEach(function (select) {
        var key = select.getAttribute("data-event-filter");
        if (select.value) {
          active[key] = select.value;
        }
      });
      var visibleCount = 0;
      cards.forEach(function (card) {
        var matches = Object.keys(active).every(function (key) {
          return card.getAttribute("data-" + key) === active[key];
        });
        card.hidden = !matches;
        if (matches) {
          visibleCount += 1;
        }
      });
      var emptyState = document.querySelector("[data-event-empty]");
      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
      trackEvent("calendar_filter_use", { filters: active });
    }

    filters.forEach(function (select) {
      select.addEventListener("change", applyFilters);
    });
  }

  // Client-side category filtering for the Selected Works archive. Text/
  // underline button controls toggle visibility of project cards by
  // data-category; no filter state is written to the URL.
  function initWorksFilters() {
    var grid = document.querySelector("[data-works-grid]");
    var filters = document.querySelectorAll("[data-works-filter]");
    if (!grid || !filters.length) {
      return;
    }
    var cards = grid.querySelectorAll("[data-works-card]");

    function applyFilter(category) {
      var visibleCount = 0;
      cards.forEach(function (card) {
        var matches = !category || card.getAttribute("data-category") === category;
        card.hidden = !matches;
        if (matches) {
          visibleCount += 1;
        }
      });
      filters.forEach(function (btn) {
        var isActive = (btn.getAttribute("data-works-filter") || "") === (category || "");
        btn.classList.toggle("is-active", isActive);
        btn.setAttribute("aria-pressed", String(isActive));
      });
      var emptyState = document.querySelector("[data-works-empty]");
      if (emptyState) {
        emptyState.hidden = visibleCount !== 0;
      }
      trackEvent("selected_works_filter_use", { category: category || "all" });
    }

    filters.forEach(function (btn) {
      btn.addEventListener("click", function () {
        applyFilter(btn.getAttribute("data-works-filter"));
      });
    });
  }

  // Attaches lightweight click tracking to event-related outbound and
  // commercial-routing links, without exposing internal event names in
  // any public-facing page copy.
  function initEventTracking() {
    document.querySelectorAll("[data-track]").forEach(function (el) {
      el.addEventListener("click", function () {
        var params = { href: el.getAttribute("href") };
        var page = el.closest ? el.closest("[data-event-cost-page]") : null;
        if (page) {
          Object.assign(params, eventCostContext(page));
        }
        var rawName = el.getAttribute("data-track");
        trackEvent(GA4_EVENT_MAP[rawName] || rawName, params);
      });
    });
  }

  // Maps an Event Costs page's data-* attributes to the flat, snake_case
  // param names used by analytics (destination, event_type, group_size,
  // budget_range, page_slug).
  function eventCostContext(page) {
    var ctx = {};
    var map = {
      destination: "destination",
      eventType: "event_type",
      groupSize: "group_size",
      budgetRange: "budget_range",
      pageSlug: "page_slug"
    };
    Object.keys(map).forEach(function (key) {
      if (page.dataset[key]) {
        ctx[map[key]] = page.dataset[key];
      }
    });
    return ctx;
  }

  // Fires a page-view event for every Event Costs page, plus a more
  // specific view event depending on whether the page is a destination hub,
  // event-type hub or fully modelled scenario. Used alongside Search Console
  // data to decide Phase 2 expansion.
  function initEventCostPageView() {
    var page = document.querySelector("[data-event-cost-page]");
    if (!page) {
      return;
    }
    var ctx = eventCostContext(page);
    trackEvent("event_cost_page_view", ctx);
    var specificEvent = {
      destination: "event_cost_destination_view",
      type: "event_cost_type_view",
      scenario: "event_cost_scenario_view"
    }[page.getAttribute("data-event-cost-page")];
    if (specificEvent) {
      trackEvent(specificEvent, ctx);
    }
  }

  // Campaign fields carried from a landing page through to the proposal form.
  // COP31 pages declare them as <meta name="dmc:*"> so a visitor who reaches the
  // form via the generic header/footer CTA is still attributed to the campaign
  // and to the service page they came from.
  var CAMPAIGN_FIELDS = ["lead_source", "campaign", "service_interest", "page_type"];

  function campaignMeta() {
    var context = {};
    CAMPAIGN_FIELDS.forEach(function (field) {
      var meta = document.querySelector(
        'meta[name="dmc:' + field.replace(/_/g, "-") + '"]'
      );
      if (meta && meta.content) {
        context[field] = meta.content;
      }
    });
    return context;
  }

  // Campaign context survives an intermediate page (e.g. a COP31 guide -> the
  // services overview -> the form), so attribution is not lost mid-journey.
  function storedCampaign(context) {
    if (!window.dmcPrivacy || !window.dmcPrivacy.analyticsAllowed()) { return context || {}; }
    try {
      if (context && context.lead_source) {
        sessionStorage.setItem("proposal_campaign", JSON.stringify(context));
        return context;
      }
      var stored = sessionStorage.getItem("proposal_campaign");
      return stored ? JSON.parse(stored) : {};
    } catch (error) {
      return context || {};
    }
  }

  function proposalContext(pathname) {
    var parts = pathname.replace(/^\/|\/$/g, "").split("/");
    var source = parts.length ? parts.join("-") : "home";
    var context = { source: source };
    var destination = { istanbul: "Istanbul", antalya: "Antalya", belek: "Belek", bodrum: "Bodrum", cappadocia: "Cappadocia" };
    var projects = {
      "incentive-travel-turkey": "Incentive Travel",
      "corporate-events-turkey": "Corporate Event",
      "white-label-dmc-turkey": "White-Label DMC Support",
      "group-travel-turkey": "Group Travel",
      "mice-turkey": "Meeting / Conference"
    };
    if (parts[0] === "destinations" && destination[parts[1]]) {
      context.destination = destination[parts[1]];
    }
    if (projects[parts[0]]) {
      context.project_type = projects[parts[0]];
    }
    if (parts[0] === "event-costs" && destination[parts[1]]) {
      context.destination = destination[parts[1]];
    }
    var eventCostTypes = {
      "corporate-events": "Corporate Event",
      "incentive-travel": "Incentive Travel",
      conferences: "Meeting / Conference",
      "corporate-retreats": "Corporate Retreat"
    };
    if (parts[0] === "event-costs" && eventCostTypes[parts[1]]) {
      context.project_type = eventCostTypes[parts[1]];
    }
    var campaign = storedCampaign(campaignMeta());
    Object.keys(campaign).forEach(function (key) {
      context[key] = campaign[key];
    });
    if (campaign.lead_source === "COP31") {
      context.destination = "Antalya";
      context.project_type = "COP31 Antalya";
    }
    return context;
  }

  function detectCtaLocation(el) {
    var tagged = el.closest("[data-cta-location]");
    if (tagged)                       { return tagged.getAttribute("data-cta-location"); }
    if (el.closest(".site-header"))   { return "header"; }
    if (el.closest(".site-footer"))   { return "footer"; }
    if (el.closest(".hero"))          { return "hero"; }
    if (el.closest('[class*="cta"]')) { return "cta_banner"; }
    return "body";
  }

  function initProposalCtas() {
    document.querySelectorAll('a[href="/request-proposal/"]').forEach(function (link) {
      link.addEventListener("click", function () {
        var params = new URLSearchParams(proposalContext(window.location.pathname));
        ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
          var value = new URLSearchParams(window.location.search).get(key);
          if (value && window.dmcPrivacy && window.dmcPrivacy.analyticsAllowed()) { params.set(key, value); }
        });
        link.href = "/request-proposal/?" + params.toString();
        trackEvent("request_proposal_click", {
          source:        params.get("source"),
          cta_name:      link.textContent.trim(),
          cta_location:  detectCtaLocation(link),
          page_path:     window.location.pathname,
          page_location: window.location.href
        });
      });
    });
  }

  function initProposalForm() {
    var form = document.querySelector("[data-proposal-form]");
    if (!form) { return; }
    var params = new URLSearchParams(window.location.search);
    var analyticsAllowed = window.dmcPrivacy && window.dmcPrivacy.analyticsAllowed();
    var landingPage = window.location.origin + window.location.pathname;
    if (analyticsAllowed) {
      try {
        landingPage = sessionStorage.getItem("proposal_landing_page") || landingPage;
        sessionStorage.setItem("proposal_landing_page", landingPage);
      } catch (error) { /* Form remains usable when storage is disabled. */ }
    }
    form.elements.source_page.value = params.get("source") || "direct";
    form.elements.landing_page.value = landingPage;
    form.elements.submission_page.value = window.location.origin + window.location.pathname;
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
      form.elements[key].value = analyticsAllowed ? params.get(key) || "" : "";
    });
    var campaign = {};
    CAMPAIGN_FIELDS.forEach(function (key) {
      if (params.get(key)) { campaign[key] = params.get(key); }
    });
    // A form embedded on a landing page (e.g. /antalya-transfer-prices/)
    // takes its attribution from that page's dmc:* meta tags.
    if (!campaign.lead_source) {
      var meta = campaignMeta();
      if (meta.lead_source) { campaign = meta; }
    }
    campaign = storedCampaign(campaign);
    CAMPAIGN_FIELDS.forEach(function (key) {
      if (form.elements[key]) { form.elements[key].value = campaign[key] || ""; }
    });
    ["destination", "project_type"].forEach(function (key) {
      if (params.get(key) && form.elements[key]) { form.elements[key].value = params.get(key); }
    });
    // Carried-over campaign context still pre-selects the dropdowns when the
    // visitor arrived at the form without the query string.
    if (campaign.lead_source === "COP31") {
      if (!form.elements.destination.value) { form.elements.destination.value = "Antalya"; }
      if (!form.elements.project_type.value) { form.elements.project_type.value = "COP31 Antalya"; }
    }
    trackEvent("proposal_form_view", {
      source: form.elements.source_page.value,
      lead_source: campaign.lead_source || "",
      service_interest: campaign.service_interest || ""
    });
    var started = false;
    form.addEventListener("focusin", function () {
      if (!started) {
        started = true;
        trackEvent("form_start", {
          source:    form.elements.source_page.value,
          page_path: window.location.pathname
        });
      }
    });
    var datesUnconfirmed = form.elements.dates_unconfirmed;
    datesUnconfirmed.addEventListener("change", function () {
      ["date_start", "date_end"].forEach(function (name) {
        form.elements[name].disabled = datesUnconfirmed.checked;
        if (datesUnconfirmed.checked) { form.elements[name].value = ""; }
      });
    });
    var submitting = false;
    var sent = false;
    var button = form.querySelector('button[type="submit"]');
    var buttonLabel = button ? button.textContent : "";
    form.addEventListener("submit", function (event) {
      var error = document.querySelector("[data-proposal-error]");
      var start = form.elements.date_start.value;
      var end = form.elements.date_end.value;
      error.hidden = true;
      event.preventDefault();
      // One request at a time, and no second request for a brief already accepted.
      if (submitting || sent) { return; }
      if (!datesUnconfirmed.checked && (!start || !end)) {
        error.textContent = "Please enter your travel or event dates, or select Dates Not Confirmed.";
        error.hidden = false;
      } else if (start && end && end < start) {
        error.textContent = "End date must be on or after the start date.";
        error.hidden = false;
      } else {
        submitting = true;
        form.elements.timestamp.value = new Date().toISOString();
        trackEvent("proposal_form_submit", { source: form.elements.source_page.value });
        button.disabled = true;
        button.setAttribute("aria-busy", "true");
        button.textContent = "Sending\u2026";
        fetch(form.action, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(Object.fromEntries(new FormData(form).entries()))
        }).then(function (response) {
          return response.json().catch(function () { return {}; }).then(function (data) {
            if (!response.ok || !data.ok) {
              var failure = new Error((data && data.error) || "Submission failed");
              failure.validation = response.status === 400;
              throw failure;
            }
          });
        }).then(function () {
          sent = true;
          submitting = false;
          button.removeAttribute("aria-busy");
          trackEvent("generate_lead", {
            source:           form.elements.source_page.value,
            lead_source:      form.elements.lead_source      ? form.elements.lead_source.value      : "",
            campaign:         form.elements.campaign         ? form.elements.campaign.value         : "",
            service_interest: form.elements.service_interest ? form.elements.service_interest.value : "",
            utm_source:       form.elements.utm_source.value   || "",
            utm_medium:       form.elements.utm_medium.value   || "",
            utm_campaign:     form.elements.utm_campaign.value || "",
            utm_content:      form.elements.utm_content.value  || "",
            utm_term:         form.elements.utm_term.value     || "",
            page_path:        window.location.pathname,
            page_location:    form.elements.submission_page.value
          });
          var context = {
            page_path:        window.location.pathname,
            lead_source:      form.elements.lead_source ? form.elements.lead_source.value : "",
            service_interest: form.elements.service_interest ? form.elements.service_interest.value : ""
          };
          if (!form.hasAttribute("data-success-inline") && openSuccessModal(context, button)) {
            // The form stays where it is; it is locked so the same brief cannot be sent twice.
            // aria-disabled (not disabled) keeps the button focusable so focus can return to it.
            button.disabled = false;
            button.setAttribute("aria-disabled", "true");
            button.textContent = "Brief Sent";
          } else {
            // Fallback: inline thank-you section (no dialog support, or inline form).
            button.textContent = buttonLabel;
            form.hidden = true;
            document.querySelector("[data-proposal-success]").hidden = false;
          }
          form.dispatchEvent(new CustomEvent("proposal:success"));
        }).catch(function (failure) {
          submitting = false;
          button.disabled = false;
          button.removeAttribute("aria-busy");
          button.textContent = buttonLabel;
          error.textContent = failure && failure.validation && failure.message
            ? failure.message
            : "We could not send your brief. Your details are still here: please try again or email hello@dmcturkeypartner.com.";
          error.hidden = false;
          trackEvent("proposal_form_error", { source: form.elements.source_page.value });
        });
      }
      if (!error.hidden) {
        trackEvent("proposal_form_error", { source: form.elements.source_page.value });
      }
    });
  }

  // --- Post-submission success modal ------------------------------------------
  // Opened only after the API has confirmed acceptance. Native <dialog> gives
  // focus trapping, Escape and focus restoration; returns false when the
  // browser has no dialog support so the caller can use the inline fallback.
  var successDialog = null;

  function buildSuccessDialog() {
    var dialog = document.createElement("dialog");
    dialog.className = "success-modal";
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-labelledby", "success-modal-title");
    dialog.setAttribute("aria-describedby", "success-modal-desc");
    var whatsapp = "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(SUCCESS_WHATSAPP_MESSAGE);
    dialog.innerHTML =
      '<div class="success-modal__panel">' +
        '<button type="button" class="success-modal__close" aria-label="Close" data-success-close="close_button">' +
          '<svg width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" focusable="false"><path d="M4 4l12 12M16 4L4 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>' +
        '</button>' +
        '<svg class="success-modal__icon" width="56" height="56" viewBox="0 0 56 56" aria-hidden="true" focusable="false"><circle cx="28" cy="28" r="28" fill="#1f9d55"/><path d="M16 29l8 8 16-17" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>' +
        '<h2 id="success-modal-title" class="success-modal__title" tabindex="-1">Thank you!</h2>' +
        '<p class="success-modal__sub">We\u2019ve received your brief.</p>' +
        '<p id="success-modal-desc" class="success-modal__text">We will reply within 24 hours and send your side-by-side proposal within 3\u20135 business days.</p>' +
        '<hr class="success-modal__divider">' +
        '<h3 class="success-modal__heading">Need a faster response?</h3>' +
        '<p class="success-modal__text">For urgent requests or a quicker discussion, you can also reach our team directly on WhatsApp.</p>' +
        '<div class="success-modal__actions">' +
          '<a class="btn success-modal__whatsapp" href="' + whatsapp + '" target="_blank" rel="noopener" data-success-whatsapp>' +
            '<svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="#fff" d="M12.04 2a9.9 9.9 0 0 0-8.5 14.97L2 22l5.17-1.5A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 14.96l-.3-.19-3.07.89.92-3-.2-.31A8.1 8.1 0 0 1 12.04 3.8zm-3.1 3.9c-.2 0-.52.08-.8.38-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.07 3.3 5.1 4.5 2.53 1 3.04.8 3.59.75.55-.05 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35-.3-.15-1.77-.87-2.04-.97-.28-.1-.48-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.6.14-.13.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.2-.24-.58-.49-.5-.67-.5z"/></svg>' +
            '<span>Continue on WhatsApp</span></a>' +
          '<button type="button" class="btn btn--ghost success-modal__back" data-success-close="back_to_website">Back to Website</button>' +
        '</div>' +
        '<p class="success-modal__note">Your request has already been submitted. No need to send it again.</p>' +
      '</div>';
    return dialog;
  }

  function openSuccessModal(context, returnFocusTo) {
    var closeMethod = "dismiss";
    if (typeof HTMLDialogElement !== "function" || typeof HTMLDialogElement.prototype.showModal !== "function") { return false; }
    try {
      if (!successDialog) {
        successDialog = buildSuccessDialog();
        document.body.appendChild(successDialog);
      }
      var dialog = successDialog;
      var scrollbar = window.innerWidth - document.documentElement.clientWidth;
      document.documentElement.classList.add("has-success-modal");
      if (scrollbar > 0) { document.body.style.paddingRight = scrollbar + "px"; }
      var onClick = function (event) {
        var closer = event.target.closest ? event.target.closest("[data-success-close]") : null;
        if (closer) { closeMethod = closer.getAttribute("data-success-close"); dialog.close(); return; }
        if (event.target.closest && event.target.closest("[data-success-whatsapp]")) {
          trackEvent("whatsapp_click_after_lead", context);
          return;
        }
        if (event.target === dialog) { closeMethod = "backdrop"; dialog.close(); }
      };
      var onCancel = function () { closeMethod = "escape"; };
      // Keep Tab / Shift+Tab inside the dialog on every browser.
      var onKeydown = function (event) {
        if (event.key !== "Tab") { return; }
        var items = Array.prototype.filter.call(
          dialog.querySelectorAll("a[href], button:not([disabled])"),
          function (node) { return node.offsetParent !== null; }
        );
        if (!items.length) { return; }
        var first = items[0];
        var last = items[items.length - 1];
        var active = document.activeElement;
        if (event.shiftKey && (active === first || active === dialog.querySelector("#success-modal-title"))) {
          event.preventDefault();
          last.focus();
        } else if (!event.shiftKey && active === last) {
          event.preventDefault();
          first.focus();
        }
      };
      var onClose = function () {
        dialog.removeEventListener("click", onClick);
        dialog.removeEventListener("cancel", onCancel);
        dialog.removeEventListener("keydown", onKeydown);
        dialog.removeEventListener("close", onClose);
        document.documentElement.classList.remove("has-success-modal");
        document.body.style.paddingRight = "";
        // The submit button lost focus while it was disabled, so restore it explicitly.
        if (returnFocusTo && returnFocusTo.focus) { returnFocusTo.focus({ preventScroll: true }); }
        trackEvent("success_modal_close", Object.assign({ method: closeMethod }, context));
      };
      dialog.addEventListener("click", onClick);
      dialog.addEventListener("cancel", onCancel);
      dialog.addEventListener("keydown", onKeydown);
      dialog.addEventListener("close", onClose);
      dialog.showModal();
      var title = dialog.querySelector("#success-modal-title");
      if (title) { title.focus({ preventScroll: true }); }
      trackEvent("success_modal_view", context);
      return true;
    } catch (failure) {
      document.documentElement.classList.remove("has-success-modal");
      document.body.style.paddingRight = "";
      return false;
    }
  }

  function initEmailTracking() {
    document.querySelectorAll('a[href^="mailto:"]').forEach(function (link) {
      link.addEventListener("click", function () {
        trackEvent("email_click", {
          email_address: link.href.replace("mailto:", "").split("?")[0],
          cta_name:      link.textContent.trim().slice(0, 60),
          cta_location:  detectCtaLocation(link),
          page_path:     window.location.pathname
        });
      });
    });
  }

  function initPhoneTracking() {
    document.querySelectorAll('a[href^="tel:"]').forEach(function (link) {
      link.addEventListener("click", function () {
        trackEvent("phone_click", {
          phone_number: link.href.replace("tel:", ""),
          cta_location: detectCtaLocation(link),
          page_path:    window.location.pathname
        });
      });
    });
  }

  function initBookCallTracking() {
    document.querySelectorAll('a[href="/contact/"]').forEach(function (link) {
      var text = link.textContent.trim().toLowerCase();
      if (text.indexOf("book") === -1 && text.indexOf("call") === -1) { return; }
      link.addEventListener("click", function () {
        trackEvent("book_partner_call_click", {
          cta_name:     link.textContent.trim(),
          cta_location: detectCtaLocation(link),
          page_path:    window.location.pathname
        });
      });
    });
  }

  // Shown once the hero CTAs scroll out of view; hidden again from the final CTA onward.
  function initStickyCta() {
    var bar = document.querySelector("[data-sticky-cta]");
    var trigger = document.querySelector("[data-sticky-trigger]");
    if (!bar || !trigger || !("IntersectionObserver" in window)) {
      return;
    }
    var hide = document.querySelector("[data-sticky-hide]");
    var pastHero = false;
    var atEnd = false;
    function update() {
      bar.hidden = !pastHero || atEnd;
    }
    new IntersectionObserver(function (entries) {
      pastHero = !entries[0].isIntersecting && entries[0].boundingClientRect.top < 0;
      update();
    }).observe(trigger);
    if (hide) {
      // Huge top margin: "intersecting" means the final CTA has been reached or passed.
      new IntersectionObserver(function (entries) {
        atEnd = entries[0].isIntersecting;
        update();
      }, { rootMargin: "100000px 0px 0px 0px" }).observe(hide);
    }
  }
})();
