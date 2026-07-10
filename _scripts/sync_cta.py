#!/usr/bin/env python3
"""
sync_cta.py — Replaces all .cta-block sections with the canonical "Let's build together"
CTA from the home page. Safe to run multiple times (idempotent).
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent

CTA_HTML = """  <section class="cta-block">
    <div class="container">
      <h2 class="cta-headline reveal">Let's build <span class="grad">together.</span></h2>
      <p class="cta-sub reveal">Independent practices deserve intelligent practice operations. Get started with a quick conversation.</p>
      <div class="cta-actions reveal">
        <a href="https://calendly.com/sagehealth-consultation/sage-health-consultation" target="_blank" rel="noopener" class="btn">
        Schedule a Discovery Call
          <svg width="16" height="16"><use href="#i-arrow"/></svg>
        </a>
        <a href="mailto:tahir@sagehealth.partners" class="btn-secondary">Email Us</a>
      </div>
    </div>
  </section>"""

PATTERN = re.compile(
    r'  <section class="cta-block">.*?</section>',
    re.DOTALL,
)

def process(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new_text, n = PATTERN.subn(CTA_HTML, text, count=1)
    if n and new_text != text:
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
