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
    initEventTracking();
  });

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

  // Attaches lightweight click tracking to event-related outbound and
  // commercial-routing links, without exposing internal event names in
  // any public-facing page copy.
  function initEventTracking() {
    document.querySelectorAll("[data-track]").forEach(function (el) {
      el.addEventListener("click", function () {
        trackEvent(el.getAttribute("data-track"), {
          href: el.getAttribute("href")
        });
      });
    });
  }
})();
