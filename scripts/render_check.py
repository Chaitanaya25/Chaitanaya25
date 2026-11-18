"""Frame capture for review.

    python scripts/render_check.py OUT SVG [SVG ...] [--t 0.3,1,2] [--width 1000] [--browser chromium] [--reduced]

Every frame is a fresh page whose viewport equals the rendered width, with the SVG inlined at 100% width,
so the SVG's own @media (max-width) rules see the width an <img> would. CSS animations are paused through
document.getAnimations(); SMIL through svg.pauseAnimations()/setCurrentTime().
"""
import argparse
import os

from PIL import Image, ImageDraw
from playwright.sync_api import sync_playwright

ap = argparse.ArgumentParser()
ap.add_argument("out")
ap.add_argument("svgs", nargs="+")
ap.add_argument("--t", default="0.3,1,2,3.5,6,8.5,11,13.9")
ap.add_argument("--width", type=int, default=1000)
ap.add_argument("--browser", default="chromium")
ap.add_argument("--reduced", action="store_true")
ap.add_argument("--cols", type=int, default=2)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
times = [float(x) for x in a.t.split(",")]

with sync_playwright() as p:
    br = getattr(p, a.browser).launch()
    for path in a.svgs:
        name = os.path.splitext(os.path.basename(path))[0]
        bg = "#F4EEE3" if "day" in name else "#1E2A33"
        svg = open(path, encoding="utf-8").read()
        ctx = br.new_context(viewport={"width": a.width, "height": 900},
                             reduced_motion="reduce" if a.reduced else "no-preference")
        shots = []
        for t in (times if not a.reduced else [0]):
            pg = ctx.new_page()
            pg.set_content(f"<style>html,body{{margin:0;background:{bg}}}svg{{width:100%;height:auto;display:block}}</style>{svg}")
            pg.evaluate("""t=>{const s=document.querySelector('svg');
                try{s.pauseAnimations();s.setCurrentTime(t)}catch(e){}
                document.getAnimations().forEach(an=>{an.pause();an.currentTime=t*1000})}""", t)
            pg.wait_for_timeout(120)
            f = os.path.join(a.out, f"_{name}_{t}.png")
            pg.query_selector("svg").screenshot(path=f)
            shots.append((t, f))
            pg.close()
        ctx.close()
        ims = [(t, Image.open(f)) for t, f in shots]
        cw, ch = ims[0][1].size
        cols = min(a.cols, len(ims))
        rows = (len(ims) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw + (cols + 1) * 6, rows * (ch + 20) + 6), "#777")
        dr = ImageDraw.Draw(sheet)
        for i, (t, im) in enumerate(ims):
            x, y = 6 + (i % cols) * (cw + 6), 6 + (i // cols) * (ch + 20)
            dr.text((x, y), f"{name}  t={t}s  w={a.width}  {a.browser}{'  reduced' if a.reduced else ''}", fill="#fff")
            sheet.paste(im, (x, y + 13))
        tag = f"{name}_{a.width}_{a.browser}{'_reduced' if a.reduced else ''}.png"
        sheet.save(os.path.join(a.out, tag))
        for _, f in shots:
            os.remove(f)
        print(tag)
    br.close()
