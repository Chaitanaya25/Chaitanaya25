"""P6 selected work: four small islands joined by arches. 14 s loop; the islands run on offset clocks."""
import math

from ..doc import Doc
from ..iso import Iso
from ..props import bush, tree
from ..tokens import LOOPS, shade
from .common import sky, travel

H = 540
CX = (200, 500, 800, 1100)
CY = 330
G = 36


def build(theme):
    L = LOOPS["work"]
    d = Doc("w", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    out = sky(d, [(260, 70, .9, 40, 2), (700, 50, .8, 50, 8), (1120, 90, 1.0, 40, 5), (100, 540, .8, 50, 11)],
              [(-150, 1450, 120, 4, 1.0), (-150, 1450, 210, 10, .85)])
    # arches between islands
    for a, b in zip(CX, CX[1:]):
        x0, x1 = a + 112, b - 112
        out += (f'<path d="M{x0},{CY + 58} Q{(x0 + x1) / 2},{CY + 6} {x1},{CY + 58}" fill="none" stroke="{d.faces("sand")[2]}" stroke-width="22" stroke-linecap="round"/>'
                f'<path d="M{x0},{CY + 52} Q{(x0 + x1) / 2},{CY} {x1},{CY + 52}" fill="none" stroke="{p["sand"]}" stroke-width="14" stroke-linecap="round"/>')
    isos = [Iso(d, cx, CY, G) for cx in CX]
    for iso in isos:
        out += iso.round_island(0, 0, 2.7, "cream", layers=3)
    out += sage(d, isos[0], 0.0) + resume(d, isos[1], 2.3) + plant(d, isos[2], 4.6) + sign(d, isos[3], 6.9)
    # name slabs on the island fronts (wide), big flat labels (narrow)
    names = ("SAGE", "ResumeIQ", "Plant CNN", "SignBridge")
    for iso, nm, cx in zip(isos, names, CX):
        w = t.width(nm, 24, "label", .08) + 40
        out += (f'<g class="w"><rect x="{cx - w / 2:.0f}" y="{CY + 118}" width="{w:.0f}" height="38" rx="8" fill="{p["board"]}" stroke="{p["wood"]}" stroke-width="2"/>'
                f'{t.text(nm, cx, CY + 145, 24, "label", p["ink"], .08, "middle")}</g>')
        out += f'<g class="n">{t.text(nm, cx, 500, 42, "label", p["ink"], .06, "middle")}</g>'
    return d.render(out, "Selected work: four small islands", DESC)


DESC = ("Four small islands joined by arches. SAGE: a round table with five chairs; a glowing token moves chair to chair, sometimes back "
        "between two, and a sound ripple runs above it. ResumeIQ: a scroll unrolls, its lines fly into a grid of 81 dots, then a four-part "
        "ring fills. Plant CNN: a magnifying glass slides over a leaf while layered squares stack and shrink and one of a row of bars lights; "
        "a tag reads 99.19%. SignBridge: a stone hand gains dots on its joints that join into a skeleton, a letter rises beside it, and one "
        "of 29 pips lights.")


def _off(d, tt):
    """Island clock offset: returns delay so the island's local 0 is at time tt."""
    return tt


def sage(d, iso, ph):
    m, p = d.m, d.pal
    L = m.L
    out = iso.shadow(-.9, -.9, 1.8, 1.8, 0, .1)
    out += iso.cylinder(0, 0, 0, .95, .55, "sand")
    ang = [-90 + 72 * k for k in range(5)]
    cp = [(1.85 * math.cos(math.radians(a)), 1.85 * math.sin(math.radians(a))) for a in ang]
    order = sorted(range(5), key=lambda k: cp[k][0] + cp[k][1])
    for k in order:
        x, y = cp[k]
        out += iso.box(x - .3, y - .3, 0, .6, .6, .5, "wood")
        out += iso.box(x - .3, y - .3, .5, .6, .12, .5, "wood") if y < 0 else ""
    # token hops chair to chair (1,2,3,2,3,4,5) then rests; base = key frame (chair 4)
    seq = [0, 1, 2, 1, 2, 3, 4, 0]
    pts = [(0, *cp[0], .95, "opacity:0")]
    tt = 1.2
    pts = [(0, cp[0][0], cp[0][1], 1.1, "opacity:0"), (.9, cp[0][0], cp[0][1], 1.1, "opacity:0")]
    for j, c in enumerate(seq):
        pts.append((tt, cp[c][0], cp[c][1], 1.1, "opacity:1", "land"))
        tt += 1.2
    pts += [(L - .9, cp[seq[-1]][0], cp[seq[-1]][1], 1.1, "opacity:1"), (L - .5, cp[seq[-1]][0], cp[seq[-1]][1], 1.1, "opacity:0"), (L, cp[0][0], cp[0][1], 1.1, "opacity:0")]
    # key frame: put the token on chair 3 (idx 3)
    st, (X, Y) = travel(m, iso, pts)
    out += (f'<g style="{st}"><g transform="translate({X:.1f} {Y:.1f})"><circle r="13" fill="{p["glow"]}" opacity=".45"/>'
            f'<circle r="7" fill="{p["terra"]}"/></g></g>')
    # sound ripple
    sx, sy = iso.p(0, 0, 2.2)
    for k in range(3):
        per = L / 7
        rp = m.cycle([(0, "opacity:0;transform:scale(.5)"), (per * .3, "opacity:.9;transform:scale(.8)"), (per, "opacity:0;transform:scale(1.5)")], per,
                     delay=(k * per / 3) % per, origin="50% 100%", base="opacity:.5;transform:scale(1)")
        out += (f'<path d="M{sx - 18 - k * 9:.1f},{sy - k * 7:.1f} Q{sx:.1f},{sy - 24 - k * 13:.1f} {sx + 18 + k * 9:.1f},{sy - k * 7:.1f}" fill="none" '
                f'stroke="{p["terra"]}" stroke-width="3" stroke-linecap="round" style="{rp}"/>')
    return out


def resume(d, iso, ph):
    m, p = d.m, d.pal
    L = m.L
    X, Y = iso.p(0, 0, 0)
    out = iso.shadow(-.8, -.8, 1.6, 1.6, 0, .1)
    out += iso.cylinder(-.4, .3, 0, .5, .2, "sand")
    out += f'<rect x="{X - 18:.1f}" y="{Y - 30:.1f}" width="6" height="30" fill="{d.c("wood")}" transform="translate(-14 -4)"/>'
    sx, sy = X - 48, Y - 126
    out += (f'<g transform="translate({sx:.1f} {sy:.1f})"><rect width="76" height="104" rx="9" fill="{p["cloud"]}" stroke="{p["wood"]}" stroke-width="3"/>'
            f'<rect x="-6" y="-8" width="88" height="16" rx="8" fill="{p["wood"]}"/><rect x="-6" y="96" width="88" height="16" rx="8" fill="{p["wood"]}"/>')
    for j in range(6):
        tt = 2.0 + j * .55
        out += (f'<rect x="12" y="{18 + j * 14}" width="{52 - (j % 3) * 8}" height="5" rx="2.5" fill="{p["sand"]}"/>'
                f'<rect x="12" y="{18 + j * 14}" width="{52 - (j % 3) * 8}" height="5" rx="2.5" fill="{p["terra"]}" style="{m.windows([(tt, tt + .8)], .2)}"/>')
    out += "</g>"
    # 81-dot taxonomy grid: dots fill in a stream as lines fly in
    gx, gy = X + 52, Y - 118
    for r_ in range(9):
        for c_ in range(9):
            k = r_ * 9 + c_
            tt = 2.4 + k * .06
            st = m.windows([(tt, L - 1.2)], .25)
            out += (f'<circle cx="{gx + c_ * 7.4:.1f}" cy="{gy + r_ * 7.4:.1f}" r="2.5" fill="{p["sand"]}"/>'
                    f'<circle cx="{gx + c_ * 7.4:.1f}" cy="{gy + r_ * 7.4:.1f}" r="2.5" fill="{p["terra"] if k % 11 == 0 else p["deep"]}" style="{st}"/>')
    # four-part score ring
    rx, ry = X + 83, Y - 38
    for k in range(4):
        tt = 7.4 + k * .55
        st = m.loop([(0, "stroke-dashoffset:25"), (tt, "stroke-dashoffset:25"), (tt + .5, "stroke-dashoffset:0"), (L - 1.2, "stroke-dashoffset:0"),
                     (L - .8, "stroke-dashoffset:25"), (L, "stroke-dashoffset:25")], "settle")
        a0 = k * 90 - 90
        out += (f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="16" fill="none" stroke="{p["sand"]}" stroke-width="6" stroke-dasharray="25 75" pathLength="100" '
                f'transform="rotate({a0 + 2} {rx:.1f} {ry:.1f})"/>'
                f'<circle cx="{rx:.1f}" cy="{ry:.1f}" r="16" fill="none" stroke="{p["terra"]}" stroke-width="6" stroke-dasharray="25 75" pathLength="100" '
                f'transform="rotate({a0 + 2} {rx:.1f} {ry:.1f})" style="{st}"/>')
    return out


def plant(d, iso, ph):
    m, p = d.m, d.pal
    L = m.L
    X, Y = iso.p(0, 0, 0)
    out = iso.shadow(-.9, -.9, 1.8, 1.8, 0, .1)
    # leaf
    lx, ly = X - 50, Y - 26
    out += (f'<g transform="translate({lx:.1f} {ly:.1f})"><path d="M0,0 Q34,-60 112,-34 Q96,34 6,18 Q-6,10 0,0Z" fill="{p["deep"]}"/>'
            f'<path d="M4,6 Q50,-14 108,-30" fill="none" stroke="{p["sage"]}" stroke-width="3" stroke-linecap="round"/>'
            f'<path d="M34,-4 l14,-18 M56,-12 l14,-22 M30,2 l10,16 M54,-8 l8,22" fill="none" stroke="{p["sage"]}" stroke-width="2"/></g>')
    # magnifier slides across the leaf
    sl = m.loop([(0, "transform:translateX(-26px)"), (1.5, "transform:translateX(-26px)"), (5.2, "transform:translateX(52px)"), (8.6, "transform:translateX(-14px)"),
                 (L - 1, "transform:translateX(-14px)"), (L, "transform:translateX(-26px)")], "travel")
    out += (f'<g transform="translate({X - 8:.1f} {Y - 70:.1f})"><g style="{sl}"><circle r="26" fill="{p["cloud"]}" fill-opacity=".35" stroke="{p["terra"]}" stroke-width="6"/>'
            f'<path d="M18,20 L42,46" stroke="{p["wood"]}" stroke-width="9" stroke-linecap="round"/></g></g>')
    # conv + pool stack: layered squares that shrink
    bx, by = X + 36, Y - 120
    for k, (w, tt) in enumerate(((34, 3.0), (26, 4.0), (18, 5.0), (10, 6.0))):
        st = m.windows([(tt, L - 1.2)], .3, "land")
        out += (f'<rect x="{bx + k * 16:.1f}" y="{by + k * 7 - w / 2:.1f}" width="{w}" height="{w}" rx="4" fill="{p["cloud"]}" stroke="{p["terra"] if k % 2 == 0 else p["deep"]}" stroke-width="3" style="{st}"/>')
    # row of thin bars: one lights; the lit one steps along
    for k in range(8):
        out += f'<rect x="{X - 56 + k * 12:.1f}" y="{Y + 18:.1f}" width="6" height="{12 + (k % 3) * 7}" rx="2" fill="{p["sand"]}" transform="translate(0 {-(12 + (k % 3) * 7) + 30})"/>'
    out += (f'<rect x="{X - 56:.1f}" y="{Y + 14:.1f}" width="6" height="30" rx="2" fill="{p["terra"]}" style="{m.loop([(0, "transform:translateX(0px)"), (7.0, "transform:translateX(0px);animation-timing-function:steps(7)"), (8.4, "transform:translateX(84px)"), (L, "transform:translateX(84px)")], "linear")}"/>')
    # tag 99.19 %
    tag = f'<g transform="translate({X + 20:.1f} {Y + 30:.1f})"><rect width="82" height="30" rx="15" fill="{p["board"]}" stroke="{p["terra"]}" stroke-width="2"/>{d.t.text("99.19%", 41, 21.5, 18, "label", p["ink"], .02, "middle")}</g>'
    out += f'<g style="{m.at(4.2)}">{tag}</g>'
    return out


def sign(d, iso, ph):
    m, p = d.m, d.pal
    L = m.L
    X, Y = iso.p(0, 0, 0)
    out = iso.shadow(-.85, -.85, 1.7, 1.7, 0, .1)
    hx, hy = X - 62, Y - 6
    hand = f'<g transform="translate({hx:.1f} {hy:.1f})">'
    hand += f'<rect x="0" y="-62" width="78" height="62" rx="16" fill="{p["sand"]}"/><rect x="40" y="-62" width="38" height="62" rx="16" fill="{shade(p["sand"], -.1)}" opacity=".5"/>'
    fingers = [(6, 54, 16), (24, 64, 16), (42, 60, 16), (60, 52, 15)]
    for fx, fh, fw in fingers:
        hand += f'<rect x="{fx}" y="{-62 - fh + 16}" width="{fw}" height="{fh}" rx="{fw / 2}" fill="{p["sand"]}"/>'
    hand += f'<path d="M-2,-26 q-16,-8 -14,-30 q2,-8 10,-2 q4,8 8,16z" fill="{p["sand"]}"/></g>'
    out += hand
    # landmark dots appear then link into a skeleton
    pts = [(hx + 14, hy - 100), (hx + 32, hy - 110), (hx + 50, hy - 106), (hx + 68, hy - 98),
           (hx + 14, hy - 78), (hx + 32, hy - 86), (hx + 50, hy - 84), (hx + 68, hy - 76), (hx + 39, hy - 40), (hx + 8, hy - 50), (hx - 12, hy - 66)]
    links = [(0, 4), (1, 5), (2, 6), (3, 7), (4, 8), (5, 8), (6, 8), (7, 8), (8, 9), (9, 10)]
    ldraw = m.loop([(0, "stroke-dashoffset:100"), (3.4, "stroke-dashoffset:100"), (4.6, "stroke-dashoffset:0"), (L - 1.4, "stroke-dashoffset:0"),
                    (L - .9, "stroke-dashoffset:100"), (L, "stroke-dashoffset:100")], "travel")
    for a, b in links:
        out += (f'<line x1="{pts[a][0]:.1f}" y1="{pts[a][1]:.1f}" x2="{pts[b][0]:.1f}" y2="{pts[b][1]:.1f}" stroke="{p["terra"]}" stroke-width="2.4" '
                f'stroke-linecap="round" stroke-dasharray="100" pathLength="100" style="{ldraw}"/>')
    for k, (x, y) in enumerate(pts):
        tt = 2.0 + k * .12
        out += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4.4" fill="{p["terra"]}" stroke="{p["board"]}" stroke-width="1.6" style="{m.windows([(tt, L - 1.2)], .2, "land")}"/>'
    # big letter rises beside the hand
    rise = m.loop([(0, "opacity:0;transform:translateY(20px)"), (5.0, "opacity:0;transform:translateY(20px)"), (5.8, "opacity:1;transform:translateY(0)"),
                   (L - 1.2, "opacity:1;transform:translateY(0)"), (L - .7, "opacity:0;transform:translateY(0)"), (L, "opacity:0;transform:translateY(20px)")], "land")
    out += f'<g style="{rise}">{d.t.text("A", X + 62, Y - 56, 100, "display", p["terra"], 0, "middle")}</g>'
    # 29 pips, one lit
    px0 = X - 82
    for k in range(29):
        out += f'<circle cx="{px0 + k * 5.7:.1f}" cy="{Y + 40}" r="2.1" fill="{p["sand"]}"/>'
    out += (f'<circle cx="{px0:.1f}" cy="{Y + 40}" r="3.3" fill="{p["terra"]}" style="{m.loop([(0, "transform:translateX(0px)"), (6.0, "transform:translateX(0px);animation-timing-function:steps(28)"), (9.8, "transform:translateX(159.6px)"), (L, "transform:translateX(159.6px)")], "linear")}"/>')
    return out
