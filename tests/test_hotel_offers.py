"""Regression tests for the group hotel offers cluster (/group-hotel-offers-turkey/)."""

import html as htmllib
import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import hotel_offers_data as data  # noqa: E402

SITE = "https://dmcturkeypartner.com"
SLUGS = [""] + [a["slug"] + "/" for a in data.AREAS.values()] + [h["slug"] + "/" for h in data.HOTELS]


def read(sub):
    return (ROOT / "group-hotel-offers-turkey" / sub / "index.html").read_text(encoding="utf-8")


def main_html(page):
    return re.search(r"<main.*?</main>", page, re.S).group(0)


def visible_text(page):
    return htmllib.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", main_html(page))))


def jsonld(page):
    return [json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S)]


class HotelOfferTests(unittest.TestCase):
    def test_data_has_thirteen_windows_for_nine_hotels(self):
        self.assertEqual(len(data.WINDOWS), 13)
        self.assertEqual(len({w[0] for w in data.WINDOWS}), 9)
        self.assertEqual({w[0] for w in data.WINDOWS}, {h["slug"] for h in data.HOTELS})
        for _, start, end in data.WINDOWS:
            self.assertLess(start, end)

    def test_each_page_has_one_h1_canonical_and_page_type(self):
        for sub in SLUGS:
            page = read(sub)
            self.assertEqual(page.count("<h1"), 1, sub)
            self.assertIn('<link rel="canonical" href="%s%s%s">' % (SITE, data.HUB, sub), page)
            self.assertIn('content="hotel-offer"', page)
            self.assertIn('name="robots" content="index, follow"', page)

    def test_no_prices_or_percentages_are_published(self):
        for sub in SLUGS:
            text = visible_text(read(sub))
            self.assertNotRegex(text, r"[€$£]|\bEUR\b|\d\s?%", sub)
            for block in jsonld(read(sub)):
                self.assertNotIn('"price"', json.dumps(block), sub)
                self.assertNotIn("aggregateRating", json.dumps(block), sub)

    def test_faq_schema_matches_visible_text(self):
        for sub in SLUGS:
            page = read(sub)
            faq = next(b for b in jsonld(page) if b["@type"] == "FAQPage")
            text = visible_text(page)
            for item in faq["mainEntity"]:
                self.assertIn(item["name"], text, sub)
                self.assertIn(item["acceptedAnswer"]["text"], text, sub)

    def test_hotel_pages_list_exactly_their_windows(self):
        for h in data.HOTELS:
            page = read(h["slug"] + "/")
            text = visible_text(page)
            mine = [w for w in data.windows() if w["hotel"] is h]
            for w in mine:
                self.assertIn(data.date_range(w["start"], w["end"]), text, h["slug"])
            graph = next(b for b in jsonld(page) if "@graph" in b)["@graph"]
            self.assertTrue(any(n["@type"] == "Hotel" and n["name"] == h["name"] for n in graph))

    def test_hub_lists_all_windows_and_hotels(self):
        page = read("")
        for w in data.windows():
            self.assertIn('href="%s%s/"' % (data.HUB, w["hotel"]["slug"]), page)
            self.assertIn(htmllib.escape(w["label"]), page.replace("&#x27;", "'"))
        self.assertEqual(len(re.findall(r'<td><span class="offer-badge[^>]*>', page)) >= 13, True)

    def test_every_page_is_in_the_offers_sitemap(self):
        sitemap = (ROOT / "sitemap-offers.xml").read_text(encoding="utf-8")
        for sub in SLUGS:
            self.assertIn("<loc>%s%s%s</loc>" % (SITE, data.HUB, sub), sitemap)
        self.assertIn("sitemap-offers.xml", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn("sitemap-offers.xml", (ROOT / "robots.txt").read_text(encoding="utf-8"))
        self.assertIn("/sitemap-offers.xml", (ROOT / "_headers").read_text(encoding="utf-8"))

    def test_hub_is_linked_from_footer_home_and_llms(self):
        for rel in ("index.html", "services/hotel-sourcing/index.html", "destinations/antalya/index.html"):
            page = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn('href="%s"' % data.HUB, page, rel)
            self.assertEqual(page.count("<!-- hotel-offers:begin -->"), 1, rel)
        self.assertIn("%s%s" % (SITE, data.HUB), (ROOT / "llms.txt").read_text(encoding="utf-8"))

    def test_closed_windows_leave_offer_schema(self):
        ws = data.windows(__import__("datetime").date(2026, 11, 2))
        self.assertEqual(ws[0]["status"], "closed")
        self.assertEqual(sum(w["status"] != "closed" for w in ws), 12)


if __name__ == "__main__":
    unittest.main()
