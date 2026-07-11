#!/usr/bin/env python3
"""
build_services.py — regenerates nav dropdowns and footer advisory links from services.json.
Run from the repo root: python3 _scripts/build_services.py
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SERVICES_FILE = ROOT / "_data" / "services.json"

# Matches the Services nav-dropdown block (6-space-indented), capturing optional "active" class.
NAV_PATTERN = re.compile(
    r'      <div class="nav-dropdown( active)?">.*?      </div>(?=\n      <a href)',
    re.DOTALL,
)

# Matches the Advisory footer col.
FOOTER_PATTERN = re.compile(
    r'\n\s*<div class="footer-col">\s*\n\s*<h5>Advisory</h5>.*?</div>',
    re.DOTALL,
)

# Finds any service-list block (used positionally for home page cards).
_SERVICE_LIST_PATTERN = re.compile(r'<ul class="service-list">.*?</ul>', re.DOTALL)


def file_to_url(base_url: str, html_file: Path) -> str:
    """Convert a root-relative URL to one relative to the given HTML file's directory."""
    target = ROOT / base_url
    return os.path.relpath(target, html_file.parent).replace(os.sep, "/")


def build_nav_dropdown(data: dict, html_file: Path, active: str) -> str:
    advisory = data["advisory"]
    ai = data["ai"]

    adv_items = ""
    for svc in advisory["services"]:
        adv_items += (
            f'            <div class="dd-item">\n'
            f'              <span class="dd-item-icon"><svg width="20" height="20"><use href="#{svc["icon"]}"/></svg></span>\n'
            f'              <span class="dd-item-text"><span class="dd-item-name">{svc["name"]}</span>'
            f'<span class="dd-item-sub">{svc["nav_desc"]}</span></span>\n'
            f'            </div>\n'
        )

    ai_items = ""
    for svc in ai["services"]:
        ai_items += (
            f'            <div class="dd-item-disabled">\n'
            f'              <span class="dd-item-icon"><svg width="20" height="20"><use href="#{svc["icon"]}"/></svg></span>\n'
            f'              <span class="dd-item-text"><span class="dd-item-name">{svc["name"]}</span>'
            f'<span class="dd-item-sub">{svc["nav_desc"]}</span></span>\n'
            f'            </div>\n'
        )

    return (
        f'      <div class="nav-dropdown{active}">\n'
        f'        <button class="nav-dropdown-trigger" type="button">Services '
        f'<svg class="chev" viewBox="0 0 24 24" fill="none" aria-hidden="true">'
        f'<polyline points="6 9 12 15 18 9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
        f'</svg></button>\n'
        f'        <div class="dropdown-content">\n'
        f'          <div class="dropdown-col">\n'
        f'            <h4>{advisory["label"]}</h4>\n'
        f'{adv_items}'
        f'          </div>\n'
        f'          <div class="dropdown-col">\n'
        f'            <h4>{ai["label"]}</h4>\n'
        f'            <span class="tag dd-coming-soon">Coming soon</span>\n'
        f'{ai_items}'
        f'          </div>\n'
        f'        </div>\n'
        f'      </div>'
    )


def build_footer_advisory(data: dict, html_file: Path) -> str:
    return ""  # Advisory footer column removed


def build_service_list(services: list) -> str:
    """Returns <ul class="service-list">...</ul> without leading indentation (caller provides it)."""
    items = ""
    for svc in services:
        items += (
            f'            <li class="service-item">\n'
            f'              <div class="service-icon"><svg width="20" height="20"><use href="#{svc["icon"]}"/></svg></div>\n'
            f'              <div><strong class="service-name">{svc["name"]}</strong>'
            f'<p class="service-desc">{svc["card_desc"]}</p></div>\n'
            f'            </li>\n'
        )
    return f'<ul class="service-list">\n{items}          </ul>'


def process_file(html_file: Path, data: dict, is_home: bool = False) -> bool:
    content = html_file.read_text(encoding="utf-8")
    original = content

    # Nav dropdown
    def replace_nav(m):
        active = m.group(1) or ""
        return build_nav_dropdown(data, html_file, active)

    content = NAV_PATTERN.sub(replace_nav, content)

    # Footer advisory links
    footer_replacement = build_footer_advisory(data, html_file)
    content = FOOTER_PATTERN.sub(footer_replacement, content)

    # Home-page cards (index.html only).
    # Replace service lists by ordinal: 1st = advisory, 2nd = AI agents.
    if is_home:
        matches = list(_SERVICE_LIST_PATTERN.finditer(content))
        if len(matches) >= 2:
            adv_list = build_service_list(data["advisory"]["services"])
            ai_list = build_service_list(data["ai"]["services"])
            # Replace 2nd first so 1st position stays valid.
            m2 = matches[1]
            content = content[: m2.start()] + ai_list + content[m2.end() :]
            m1 = matches[0]
            content = content[: m1.start()] + adv_list + content[m1.end() :]

    if content != original:
        html_file.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    data = json.loads(SERVICES_FILE.read_text(encoding="utf-8"))
    html_files = sorted(ROOT.glob("**/*.html"))
    # Exclude any build artifacts or vendored files
    html_files = [f for f in html_files if "_scripts" not in f.parts]

    changed = 0
    skipped = 0
    for f in html_files:
        is_home = f == ROOT / "index.html"
        if process_file(f, data, is_home=is_home):
            print(f"  updated  {f.relative_to(ROOT)}")
            changed += 1
        else:
            skipped += 1

    print(f"\n{changed} files updated, {skipped} unchanged.")


if __name__ == "__main__":
    main()
