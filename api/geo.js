// Returns the visitor's country as seen by Vercel's edge (x-vercel-ip-country).
// Nothing is stored or logged. Used only to decide whether to show the UK Fam Trip
// pop-up; an unknown country returns null and the pop-up is not shown.
module.exports = function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "GET" && req.method !== "HEAD") {
    res.setHeader("Allow", "GET, HEAD");
    res.status(405).json({ ok: false, error: "Method not allowed" });
    return;
  }
  const header = req.headers["x-vercel-ip-country"];
  const country = (Array.isArray(header) ? header[0] : header || "").toString().toUpperCase();
  res.status(200).json({ country: /^[A-Z]{2}$/.test(country) ? country : null });
};
