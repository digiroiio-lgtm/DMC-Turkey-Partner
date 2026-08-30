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
  });
})();
