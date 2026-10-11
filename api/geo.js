// Returns the visitor's country (and IANA timezone) as seen by Vercel's edge
// (x-vercel-ip-country / x-vercel-ip-timezone). Nothing is stored or logged. Used only
// to decide whether to show the Fam Trip pop-up. An unknown country returns null and
// requests from obvious bots/crawlers are flagged, so the pop-up is never shown for them.
// The edge exposes no ASN or data-centre information, so VPN/data-centre filtering is
// best-effort (the client also compares the IP timezone with the browser timezone).
const BOT = /bot|crawl|spider|slurp|headless|lighthouse|pagespeed|phantom|puppeteer|playwright|selenium|curl|wget|python-requests|axios|go-http|java\/|httpclient|monitor|uptime|preview|facebookexternalhit|embedly|scrapy/i;

function first(value) {
  return (Array.isArray(value) ? value[0] : value || "").toString();
}

module.exports = function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.setHeader("Allow", "GET, HEAD");
    res.status(405).json({ ok: false, error: "Method not allowed" });
    return;
  }
  const country = first(req.headers["x-vercel-ip-country"]).toUpperCase();
  const zone = decodeURIComponent(first(req.headers["x-vercel-ip-timezone"]));
  const agent = first(req.headers["user-agent"]);
  res.status(200).json({
    country: /^[A-Z]{2}$/.test(country) ? country : null,
    timezone: /^[A-Za-z_]+\/[A-Za-z_\/+-]+$/.test(zone) ? zone : null,
    bot: !agent || BOT.test(agent)
  });
};
