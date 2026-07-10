#!/usr/bin/env python3
"""
add_email_nav.py — Inserts the mobile "Email us" nav button after the header-cta
link in every HTML file. Safe to run multiple times (idempotent).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
EMAIL_BTN = '\n      <a href="mailto:tahir@sagehealth.partners" class="nav-email-btn">Email us</a>'
MARKER = 'class="nav-email-btn"'

# Matches the header-cta anchor and everything up to its closing </a>
PATTERN = re.compile(
    r'(<a [^>]*class="header-cta"[^>]*>.*?</a>)',
    re.DOTALL,
)

def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False  # already added
    new_text, n = PATTERN.subn(lambda m: m.group(0) + EMAIL_BTN, text, count=1)
    if n:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False

def main():
    html_files = [
        f for f in ROOT.glob("**/*.html")
        if "_scripts" not in f.parts
    ]
    changed = 0
    for f in sorted(html_files):
        if process(f):
            print(f"  updated  {f.relative_to(ROOT)}")
            changed += 1
    print(f"\n{changed} file(s) updated.")

if __name__ == "__main__":
    main()
