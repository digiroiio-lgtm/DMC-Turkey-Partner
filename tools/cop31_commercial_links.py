#!/usr/bin/env python3
"""Add visible commercial routes to COP31 pages, preserving authored content.

Marker replacement makes this safe after every COP31 regeneration.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
BEGIN = "<!-- cop31-commercial:begin -->"
END = "<!-- cop31-commercial:end -->"
SERVICES = [
    ("cop31-antalya-accommodation", "COP31 Group Accommodation", "Plan room blocks and stays for delegations and event teams."),
    ("cop31-private-transfers", "COP31 Private Transfers", "Coordinate vehicles for delegation movements and daily journeys."),
    ("cop31-hostess-staff", "COP31 Hostess &amp; Registration Staff", "Brief reception teams for registration desks and guest support."),
    ("cop31-interpreters", "COP31 Interpreters", "Scope language pairs and interpreting support for your meetings."),
    ("cop31-antalya-restaurants", "COP31 Group Dining", "Plan delegation dinners, menus and private dining requirements."),
    ("cop31-booth-builder-antalya", "COP31 Booth Builder", "Discuss stand design, build scope and installation requirements."),
]
LABELS = {slug: label for slug, label, _ in SERVICES}
LABELS.update({"cop31-antalya-airport-transfer": "COP31 Airport Transfers", "cop31-exhibition-services": "COP31 Exhibition Services"})
RELATED = {
    "cop31-antalya-accommodation": ["cop31-antalya-airport-transfer", "cop31-private-transfers", "cop31-antalya-restaurants"],
    "cop31-private-transfers": ["cop31-antalya-accommodation", "cop31-antalya-airport-transfer", "cop31-interpreters"],
    "cop31-antalya-airport-transfer": ["cop31-antalya-accommodation", "cop31-private-transfers", "cop31-hostess-staff"],
    "cop31-hostess-staff": ["cop31-interpreters", "cop31-private-transfers", "cop31-exhibition-services"],
    "cop31-interpreters": ["cop31-hostess-staff", "cop31-private-transfers", "cop31-antalya-accommodation"],
    "cop31-antalya-restaurants": ["cop31-private-transfers", "cop31-antalya-accommodation", "cop31-interpreters"],
    "cop31-booth-builder-antalya": ["cop31-exhibition-services", "cop31-hostess-staff", "cop31-interpreters"],
    "cop31-exhibition-services": ["cop31-booth-builder-antalya", "cop31-hostess-staff", "cop31-interpreters"],
}


def block(slug):
    if slug in ("", "cop31-antalya"):
        cards = "".join('<article class="card"><h3><a href="/%s/">%s</a></h3><p>%s</p></article>' % item for item in SERVICES)
        content = '<h2>Plan Your COP31 Delegation Services</h2><p>Choose the service you need to review the scope and send your requirements to our Antalya team.</p><div class="card-grid">%s</div>' % cards
    else:
        links = "".join('<li><a href="/%s/">%s</a></li>' % (target, LABELS[target]) for target in RELATED[slug])
        content = '<h2>Coordinate Related COP31 Services</h2><p>Planning this service as part of a wider delegation or exhibitor brief? Review the related requirements before requesting a proposal.</p><ul>%s</ul>' % links
    return BEGIN + '\n<section class="page-section">' + content + '</section>\n' + END + '\n'


def main():
    for slug in ["", "cop31-antalya", *RELATED]:
        path = ROOT / slug / "index.html"
        original = path.read_text()
        html = re.sub((r"\n?" if slug else "") + re.escape(BEGIN) + r".*?" + re.escape(END) + r"\n?", "", original, flags=re.S)
        if not slug:
            anchor = '    <!-- 9. ANTALYA / COP31 COMMERCIAL ENTRY POINT -->'
            if anchor not in html:
                raise ValueError("Missing homepage commercial anchor")
            html = html.replace(anchor, block(slug) + anchor, 1)
        else:
            main_start = html.index('<main id="main-content">')
            hero_end = html.index('</section>', main_start) + len('</section>')
            html = html[:hero_end] + '\n' + block(slug) + html[hero_end:]
        if html != original:
            path.write_text(html)
            print('Updated', path.relative_to(ROOT))


if __name__ == "__main__":
    main()
