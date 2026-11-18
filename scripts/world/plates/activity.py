"""P7 activity: the sea of days. 12 s loop. Real contribution data as an isometric field of small tiles."""
import math

from ..contributions import level_fn, weekday
from ..doc import Doc
from ..iso import Iso
from ..tokens import LOOPS, shade
from .common import sky

MONTHS = "JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC".split()


def placeholder_weeks():
    from datetime import date, timedelta
    end = date(2026, 11, 15)
    start = end - timedelta(days=end.weekday() + 1 + 52 * 7)
    weeks, dd = [], start
    while dd <= end:
        weeks.append([((dd + timedelta(i)).isoformat(), 0) for i in range(7) if dd + timedelta(i) <= end])
        dd += timedelta(7)
    return weeks


def build(theme, weeks=None):
    weeks = weeks or placeholder_weeks()
    awaiting = all(c == 0 for w in weeks for _, c in w)
    L = LOOPS["activity"]
    n = len(weeks)
    gx, gy = 10.0, 8.0
    H = 330
    d = Doc("v", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    x0, y0 = 120, 128
    out = sky(d, [(1100, 60, 1.0, 50, 2), (640, 46, .8, 40, 7), (300, 70, .9, 50, 4)], [(-150, 1450, 90, 3, 1.0)])
    lv = level_fn(weeks)
    roles = {0: "sage", 1: "sage", 2: "sand", 3: "terra", 4: "terra"}
    tint = {0: .0, 1: .0, 2: .0, 3: .35, 4: .0}
    for k in range(5):
        base = p[roles[k]] if k else shade(p["sage"], .38 if not p["night"] else -.18)
        tp, lf, rt = d.faces(shade(base, tint[k]))
        sym = (f'<polygon points="0,0 {gx},{gy} 0,{2 * gy} {-gx},{gy}" fill="{tp}"/>'
               f'<polygon points="{-gx},{gy} 0,{2 * gy} 0,{2 * gy + 2.5} {-gx},{gy + 2.5}" fill="{lf}"/>')
        d.add_def(f"t{k}", f'<g id="v-t{k}">{sym}</g>')

    def cell(wi, wd):
        return x0 + wi * 2 * gx + wd * gx, y0 + wd * gy
    # sea slab (parallelogram) with depth
    pad = 18
    a = (x0 - gx - pad, y0 - pad * .5)
    b = (x0 + n * 2 * gx + gx + pad, y0 - pad * .5)
    c2 = (x0 + n * 2 * gx + 7 * gx + pad, y0 + 8 * gy + pad * .5)
    d2 = (x0 + 7 * gx - gx * 2 - pad, y0 + 8 * gy + pad * .5)
    pts = lambda q: " ".join("%.1f,%.1f" % z for z in q)
    out += f'<polygon points="{pts([a, b, c2, d2])}" fill="{p["water"]}"/>'
    th = 16
    out += f'<polygon points="{d2[0]:.1f},{d2[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {c2[0]:.1f},{c2[1] + th:.1f} {d2[0]:.1f},{d2[1] + th:.1f}" fill="{shade(p["water"], -.12)}"/>'
    out += f'<polygon points="{c2[0]:.1f},{c2[1]:.1f} {b[0]:.1f},{b[1]:.1f} {b[0]:.1f},{b[1] + th:.1f} {c2[0]:.1f},{c2[1] + th:.1f}" fill="{shade(p["water"], -.2)}"/>'
    cols, months = "", ""
    last_mo, last_w = None, -9
    for wi, week in enumerate(weeks):
        cells = ""
        for ds, cnt in week:
            X, Y = cell(wi, weekday(ds))
            cells += f'<use href="#v-t{lv(cnt)}" x="{X:.1f}" y="{Y:.1f}"/>'
        per = L / 3
        wave = m.cycle([(0, "transform:translateY(0px)"), (per * .2, "transform:translateY(-3px)"), (per * .45, "transform:translateY(0px)"), (per, "transform:translateY(0px)")],
                       per, "ease-in-out", delay=(wi * .07) % per, base="transform:translateY(0px)")
        cols += f'<g style="{wave}">{cells}</g>'
        mo = int(week[0][0][5:7])
        if mo != last_mo and wi - last_w > 3 and wi < n - 3:
            X, Y = cell(wi, 7.2)
            months += f'<g class="w">{t.text(MONTHS[mo - 1], X - gx * 2, Y + 36, 20, "label", p["ink"], .2)}</g>'
            last_w = wi
        last_mo = mo
    out += cols + months
    # lighthouse on a rock at the left; its beam sweeps over the tiles
    lx, ly = 54, y0 + 6.2 * gy
    beam = m.loop([(0, "transform:rotate(-8deg)"), (L / 2, "transform:rotate(7deg)"), (L, "transform:rotate(-8deg)")], "ease-in-out", origin="0% 50%")
    out += (f'<g transform="translate({lx} {ly - 74})"><g style="{beam}"><path d="M0,0 L1180,-34 L1180,70Z" fill="{p["glow"]}" opacity="{.18 if not p["night"] else .2}"/></g></g>')
    out += (f'<g transform="translate({lx} {ly}) scale(1.25)"><ellipse cx="0" cy="3" rx="30" ry="9" fill="{p["ink"]}" opacity=".14"/>'
            f'<path d="M-30,0 L-18,-14 H18 L30,0Z" fill="{p["deep"]}"/><path d="M-13,-12 L-8,-86 H8 L13,-12Z" fill="{p["cream"] if not p["night"] else p["sand"]}"/>'
            f'<rect x="-10" y="-60" width="20" height="10" fill="{p["terra"]}"/><rect x="-11" y="-92" width="22" height="8" rx="2" fill="{p["terra"]}"/>'
            f'<rect x="-6" y="-108" width="12" height="17" rx="2" fill="{p["glow"]}"/><path d="M-10,-108 L0,-120 L10,-108Z" fill="{p["terra"]}"/></g>')
    if awaiting:
        out += t.text("awaiting first run", 640, H - 24, 22, "label", p["ink"], .2, "middle")
    return d.render(out, "Activity: the sea of days",
                    "A field of small isometric tiles, one per day of the past year, oldest week at the left. Quiet days are pale sage, "
                    "active days sand and the busiest terracotta. A lighthouse beam sweeps slowly across the tiles and a gentle ripple "
                    "passes through them from the oldest week to the newest.")
