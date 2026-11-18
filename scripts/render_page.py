"""Render README.md the way GitHub does, for review.

    python scripts/render_page.py CSS_DIR OUT_DIR

CSS_DIR holds github-markdown-dark.css and github-markdown-light.css (github-markdown-css). HTML comes from
GitHub's own renderer (`gh api markdown`). GitHub swaps <picture> sources and hides #gh-dark-mode-only /
#gh-light-mode-only images itself; both are emulated here. Writes readme-{theme}-{width}.png.
"""
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
css_dir, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
payload = json.dumps({"text": (ROOT / "README.md").read_text(encoding="utf-8"), "mode": "gfm", "context": "Chaitanaya25/Chaitanaya25"})
html = subprocess.run(["gh", "api", "markdown", "--input", "-"], input=payload, capture_output=True, text=True,
                      encoding="utf-8", check=True).stdout
(out / "readme.html").write_text(html, encoding="utf-8")

with sync_playwright() as p:
    br = p.chromium.launch()
    for theme in ("dark", "light"):
        body = html
        if theme == "light":   # GitHub's themed-picture swaps the <source media=light> in
            body = re.sub(r'<img src="assets/([a-z-]+?)-dusk\.svg"(?!#)', r'<img src="assets/\1-day.svg"', body)
        css = (css_dir / f"github-markdown-{theme}.css").read_text(encoding="utf-8")
        bg, fg = ("#0d1117", "#e6edf3") if theme == "dark" else ("#ffffff", "#1f2328")
        hide = "dark" if theme == "light" else "light"
        for width, pad in ((1012, 32), (860, 24), (400, 16)):
            page = (f'<html><head><meta charset="utf-8"><base href="{ROOT.as_uri()}/"><style>{css}'
                    f'img[src$="#gh-{hide}-mode-only"]{{display:none}}body{{background:{bg};margin:0}}'
                    f'.markdown-body{{color:{fg};box-sizing:border-box;width:{width}px;padding:{pad}px}}'
                    f'.markdown-body table td,.markdown-body table th{{color:{fg}}}</style></head>'
                    f'<body><article class="markdown-body">{body}</article></body></html>')
            f = out / f"_{theme}_{width}.html"
            f.write_text(page, encoding="utf-8")
            pg = br.new_page(viewport={"width": width, "height": 8000}, color_scheme=theme)
            pg.goto(f.as_uri())
            pg.wait_for_timeout(int(os.environ.get("WAIT_MS", "9000")))
            h = pg.evaluate("document.querySelector('article').scrollHeight")
            pg.set_viewport_size({"width": width, "height": h})
            pg.screenshot(path=str(out / f"readme-{theme}-{width}.png"), clip={"x": 0, "y": 0, "width": width, "height": h})
            pg.close()
            f.unlink()
    br.close()
print("ok")
