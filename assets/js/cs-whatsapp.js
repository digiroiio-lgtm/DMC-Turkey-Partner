/*
 * Floating WhatsApp button for the Czech page (/cs/dmc-turecko/) only.
 * The number is fetched from /api/whatsapp?locale=cs (server side, env WHATSAPP_NUMBER_CS); it is not part of
 * this file or of any page. If the endpoint is unavailable the button is simply not shown.
 */
(function () {
  "use strict";
  var LOCALE = "cs";
  var LABEL = "Napsat na WhatsApp";
  var MESSAGE = "Dobrý den, zajímá mě spolupráce s DMC Turkey Partner na akci v Turecku. Rád(a) bych probral(a) své požadavky.";

  function show(number) {
    var link = document.createElement("a");
    link.className = "wa-float";
    link.href = "https://wa.me/" + number + "?text=" + encodeURIComponent(MESSAGE);
    link.target = "_blank";
    link.rel = "noopener";
    link.setAttribute("aria-label", LABEL);
    link.setAttribute("data-wa-float", LOCALE);
    link.innerHTML =
      '<svg width="26" height="26" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="#fff" d="M12.04 2a9.9 9.9 0 0 0-8.5 14.97L2 22l5.17-1.5A9.9 9.9 0 1 0 12.04 2zm0 1.8a8.1 8.1 0 1 1-4.3 14.96l-.3-.19-3.07.89.92-3-.2-.31A8.1 8.1 0 0 1 12.04 3.8zm-3.1 3.9c-.2 0-.52.08-.8.38-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15.2 2.07 3.3 5.1 4.5 2.53 1 3.04.8 3.59.75.55-.05 1.77-.72 2.02-1.42.25-.7.25-1.3.17-1.42-.07-.12-.27-.2-.57-.35-.3-.15-1.77-.87-2.04-.97-.28-.1-.48-.15-.67.15-.2.3-.77.97-.94 1.17-.17.2-.35.22-.65.07-.3-.15-1.27-.47-2.42-1.5-.9-.8-1.5-1.78-1.67-2.08-.17-.3-.02-.46.13-.6.14-.13.3-.35.45-.52.15-.18.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-.67-1.62-.92-2.2-.24-.58-.49-.5-.67-.5z"/></svg>' +
      '<span class="wa-float__label">' + LABEL + '</span>';
    document.body.appendChild(link);
  }

  fetch("/api/whatsapp?locale=" + LOCALE, { cache: "no-store", credentials: "omit" })
    .then(function (response) { return response.ok ? response.json() : null; })
    .then(function (data) { if (data && /^[0-9]{8,15}$/.test(data.number || "")) { show(data.number); } })
    .catch(function () { /* no number, no button */ });
})();
