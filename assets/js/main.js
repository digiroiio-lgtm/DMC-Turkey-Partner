/*
 * DmcTurkeyPartner.com — minimal global JS
 * Handles the mobile navigation toggle and desktop dropdown menus.
 * No frameworks, no dependencies.
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    var yearEl = document.getElementById("year");
    if (yearEl) {
      yearEl.textContent = new Date().getFullYear();
    }

    var navToggle = document.querySelector(".site-nav__toggle");
    var nav = document.querySelector(".site-nav");
    if (navToggle && nav) {
      navToggle.addEventListener("click", function () {
        var isOpen = nav.classList.toggle("is-open");
        navToggle.setAttribute("aria-expanded", String(isOpen));
      });
    }

    var groups = document.querySelectorAll(".nav-group");
    groups.forEach(function (group) {
      var trigger = group.querySelector(".nav-group__trigger");
      if (!trigger) {
        return;
      }
      trigger.addEventListener("click", function () {
        var isOpen = group.classList.toggle("is-open");
        trigger.setAttribute("aria-expanded", String(isOpen));
        groups.forEach(function (other) {
          if (other !== group) {
            other.classList.remove("is-open");
            var otherTrigger = other.querySelector(".nav-group__trigger");
            if (otherTrigger) {
              otherTrigger.setAttribute("aria-expanded", "false");
            }
          }
        });
      });
    });

    document.addEventListener("click", function (event) {
      groups.forEach(function (group) {
        if (!group.contains(event.target)) {
          group.classList.remove("is-open");
          var trigger = group.querySelector(".nav-group__trigger");
          if (trigger) {
            trigger.setAttribute("aria-expanded", "false");
          }
        }
      });
    });

    initEventFilters();
    initWorksFilters();
    initEventTracking();
    initEventCostPageView();
    initGuideToc();
    initProposalCtas();
    initProposalForm();
  });

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

  // Lightweight analytics dispatch. Pushes to window.dataLayer if a tag
  // manager is present; otherwise this is a silent no-op. No PII is sent.
  function trackEvent(name, params) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: name }, params || {}));
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
        trackEvent(el.getAttribute("data-track"), params);
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
    return context;
  }

  function initProposalCtas() {
    document.querySelectorAll('a[href="/request-proposal/"]').forEach(function (link) {
      link.addEventListener("click", function () {
        var params = new URLSearchParams(proposalContext(window.location.pathname));
        ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
          var value = new URLSearchParams(window.location.search).get(key);
          if (value) { params.set(key, value); }
        });
        link.href = "/request-proposal/?" + params.toString();
        trackEvent("proposal_cta_click", { source: params.get("source") });
      });
    });
  }

  function initProposalForm() {
    var form = document.querySelector("[data-proposal-form]");
    if (!form) { return; }
    var params = new URLSearchParams(window.location.search);
    var landingPage = sessionStorage.getItem("proposal_landing_page") || document.referrer || window.location.href;
    sessionStorage.setItem("proposal_landing_page", landingPage);
    form.elements.source_page.value = params.get("source") || "direct";
    form.elements.landing_page.value = landingPage;
    form.elements.submission_page.value = window.location.href;
    ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"].forEach(function (key) {
      form.elements[key].value = params.get(key) || "";
    });
    ["destination", "project_type"].forEach(function (key) {
      if (params.get(key) && form.elements[key]) { form.elements[key].value = params.get(key); }
    });
    trackEvent("proposal_form_view", { source: form.elements.source_page.value });
    var started = false;
    form.addEventListener("focusin", function () {
      if (!started) {
        started = true;
        trackEvent("proposal_form_start", { source: form.elements.source_page.value });
      }
    });
    var datesUnconfirmed = form.elements.dates_unconfirmed;
    datesUnconfirmed.addEventListener("change", function () {
      ["date_start", "date_end"].forEach(function (name) {
        form.elements[name].disabled = datesUnconfirmed.checked;
        if (datesUnconfirmed.checked) { form.elements[name].value = ""; }
      });
    });
    form.addEventListener("submit", function (event) {
      var error = document.querySelector("[data-proposal-error]");
      var start = form.elements.date_start.value;
      var end = form.elements.date_end.value;
      error.hidden = true;
      if (!datesUnconfirmed.checked && (!start || !end)) {
        event.preventDefault();
        error.textContent = "Please enter your travel or event dates, or select Dates Not Confirmed.";
        error.hidden = false;
      } else if (start && end && end < start) {
        event.preventDefault();
        error.textContent = "End date must be on or after the start date.";
        error.hidden = false;
      } else {
        event.preventDefault();
        form.elements.timestamp.value = new Date().toISOString();
        trackEvent("proposal_form_submit", { source: form.elements.source_page.value });
        var button = form.querySelector('button[type="submit"]');
        button.disabled = true;
        fetch(form.action, {
          method: "POST",
          headers: { "Content-Type": "application/x-www-form-urlencoded" },
          body: new URLSearchParams(new FormData(form)).toString()
        }).then(function (response) {
          if (!response.ok) { throw new Error("Submission failed"); }
          form.hidden = true;
          document.querySelector("[data-proposal-success]").hidden = false;
          trackEvent("proposal_form_success", { source: form.elements.source_page.value });
        }).catch(function () {
          button.disabled = false;
          error.textContent = "We could not send your brief. Please try again or email hello@dmcturkeypartner.com.";
          error.hidden = false;
          trackEvent("proposal_form_error", { source: form.elements.source_page.value });
        });
      }
      if (!error.hidden) {
        trackEvent("proposal_form_error", { source: form.elements.source_page.value });
      }
    });
  }
})();
