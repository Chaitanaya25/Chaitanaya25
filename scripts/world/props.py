"""Hand-built props. Everything is flat shapes in the palette; no filters, no gradients."""
import math

from .iso import Iso
from .motion import smil
from .tokens import W, mix, shade


# ---- ambient life -----------------------------------------------------------------------
def sway_style(m, amp, delay=0.0, prop="translateX", unit="px", period=None):
    """Slow back-and-forth drift (sinusoidal) over one loop. Base = the value at the key frame."""
    L = m.L
    per = period or L
    ph = delay / per
    key = -amp * math.cos(2 * math.pi * (.75 * L / per + ph))
    fr = [(0, f"transform:{prop}({-amp}{unit})"), (per / 2, f"transform:{prop}({amp}{unit})"), (per, f"transform:{prop}({-amp}{unit})")]
    d = f"-{(per - delay) % per:.2f}s" if delay else "0s"
    return (f"transform:{prop}({key:.1f}{unit});animation:{m.frames(fr, per)} {per}s ease-in-out {d} infinite both")


def cloud(d, x, y, s=1.0, amp=60, delay=0.0, op=1.0):
    c = d.c("cloud")
    shp = (f'<g transform="translate({x} {y}) scale({s})" fill="{c}" opacity="{op}">'
           f'<ellipse cx="0" cy="0" rx="62" ry="15"/><circle cx="-14" cy="-12" r="18"/><circle cx="14" cy="-18" r="22"/>'
           f'<circle cx="38" cy="-8" r="14"/></g>')
    return f'<g class="deco" style="{sway_style(d.m, amp, delay)}">{shp}</g>'


def bird(d, x0, x1, y, delay=0.0, s=1.0):
    """Glides left to right across the plate once per loop (wraps off-screen), wings flapping."""
    m = d.m
    L = m.L
    ph = delay / L
    pos = ((.75 + ph) % 1)
    bx = x0 + (x1 - x0) * pos
    by = math.sin(pos * math.pi * 2) * 14
    fr = [(0, f"transform:translate({x0}px,0px)"), (L * .25, f"transform:translate({x0 + (x1 - x0) * .25:.0f}px,-14px)"),
          (L * .5, f"transform:translate({x0 + (x1 - x0) * .5:.0f}px,0px)"), (L * .75, f"transform:translate({x0 + (x1 - x0) * .75:.0f}px,14px)"),
          (L, f"transform:translate({x1}px,0px)")]
    dl = f"-{(L - delay) % L:.2f}s" if delay else "0s"
    st = f"transform:translate({bx:.0f}px,{by:.0f}px);animation:{m.frames(fr, L)} {L}s linear {dl} infinite both"
    per = L / 20
    fl = m.cycle([(0, "transform:scaleY(1)"), (per / 2, "transform:scaleY(-.55)"), (per, "transform:scaleY(1)")], per,
                 delay=(delay * 3) % per, origin="50% 100%", base="transform:scaleY(1)")
    k = d.c("ink")
    return (f'<g class="deco" style="{st}"><g transform="translate(0 {y}) scale({s})">'
            f'<g style="{fl}"><path d="M-12,0 Q-6,-8 0,0 Q6,-8 12,0" fill="none" stroke="{k}" stroke-width="2.6" stroke-linecap="round"/></g></g></g>')


def tree(d, x, y, s=1.0, delay=0.0, deep=True):
    m = d.m
    p = m.L / 4
    sw = m.cycle([(0, "transform:rotate(-1.2deg)"), (p / 2, "transform:rotate(1.4deg)"), (p, "transform:rotate(-1.2deg)")], p,
                 delay=delay % p, origin="50% 100%", base="transform:rotate(-1.2deg)")
    f = d.c("deep") if deep else d.c("sage")
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="1" rx="13" ry="4" fill="{d.c("ink")}" opacity=".14"/>'
            f'<g style="{sw}"><rect x="-2.2" y="-14" width="4.4" height="15" rx="1.6" fill="{shade(d.c("wood"), -.15)}"/>'
            f'<circle cx="0" cy="-30" r="16" fill="{f}"/><circle cx="-5" cy="-35" r="9" fill="{shade(f, .16)}"/>'
            f'<circle cx="8" cy="-24" r="7" fill="{shade(f, -.1)}"/></g></g>')


def bush(d, x, y, s=1.0, role="deep"):
    f = d.c(role)
    return (f'<g transform="translate({x} {y}) scale({s})"><ellipse cx="0" cy="1" rx="14" ry="4" fill="{d.c("ink")}" opacity=".12"/>'
            f'<circle cx="-7" cy="-6" r="8" fill="{f}"/><circle cx="5" cy="-8" r="10" fill="{shade(f, .12)}"/>'
            f'<circle cx="12" cy="-3" r="6" fill="{shade(f, -.1)}"/></g>')


def sun(d, cx, cy, r):
    """Sun by day, moon at dusk. Rises/sets a few px over the loop."""
    m = d.m
    L = m.L
    st = m.loop([(0, "transform:translateY(5px)"), (L / 2, "transform:translateY(-5px)"), (L, "transform:translateY(5px)")],
                "ease-in-out", base=f"transform:translateY({-5 * math.cos(2 * math.pi * .75):.1f}px)")
    if d.pal["night"]:
        body = (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{d.c("sun")}"/>'
                f'<circle cx="{cx + r * .42}" cy="{cy - r * .22}" r="{r * .86}" fill="{d.pal["bg"]}"/>')
    else:
        body = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{d.c("sun")}"/>'
    return f'<g style="{st}">{body}</g>'


def mountains(d, x, y, w, h):
    a, b = d.c("mount"), d.c("mount2")
    far = (f'<polygon points="{x},{y} {x + w * .3:.0f},{y - h:.0f} {x + w * .52:.0f},{y - h * .5:.0f} {x + w * .74:.0f},{y - h * .86:.0f} {x + w},{y}" fill="{a}"/>'
           f'<polygon points="{x + w * .3:.0f},{y - h:.0f} {x + w * .52:.0f},{y - h * .5:.0f} {x + w * .46:.0f},{y}" fill="{shade(a, -.07)}"/>'
           f'<polygon points="{x + w * .74:.0f},{y - h * .86:.0f} {x + w},{y} {x + w * .62:.0f},{y}" fill="{shade(a, -.08)}"/>')
    near = (f'<polygon points="{x + w * .1:.0f},{y} {x + w * .4:.0f},{y - h * .55:.0f} {x + w * .7:.0f},{y}" fill="{b}"/>'
            f'<polygon points="{x + w * .4:.0f},{y - h * .55:.0f} {x + w * .7:.0f},{y} {x + w * .48:.0f},{y}" fill="{shade(b, -.12)}"/>')
    return f'<g class="deco">{far}{near}</g>'


def lantern(d, x, y, s=1.0, delay=0.0, halo=True):
    m = d.m
    p = m.L / 4
    br = m.cycle([(0, "opacity:.72"), (p / 2, "opacity:1"), (p, "opacity:.72")], p, delay=delay % p, base="opacity:.9")
    k = shade(d.c("teal"), -.35)
    h = (f'<circle cx="0" cy="3" r="14" fill="{d.c("glow")}" style="{br}" opacity=".28"/>') if halo else ""
    return (f'<g transform="translate({x} {y}) scale({s})">{h}<path d="M-3,-6 Q0,-12 3,-6" fill="none" stroke="{k}" stroke-width="1.3"/>'
            f'<rect x="-4.5" y="-6" width="9" height="12" rx="2" fill="{k}"/><rect x="-2.8" y="-4" width="5.6" height="8" rx="1.3" fill="{d.c("glow")}"/></g>')


def flag(d, x, y, w=30, h=14, role="terra", periods=None):
    """Flag on a pole; the cloth ripples by SMIL path morph between same-structure paths."""
    m = d.m
    L = m.L
    k = max(2, round(L / 1.75))
    pa = f"M0,0 C{w * .3:.0f},-3 {w * .65:.0f},3 {w},0 L{w * .94:.0f},{h} C{w * .62:.0f},{h + 3} {w * .3:.0f},{h - 3} 0,{h}Z"
    pb = f"M0,0 C{w * .3:.0f},3 {w * .65:.0f},-3 {w},1 L{w * .94:.0f},{h - 1} C{w * .62:.0f},{h - 3} {w * .3:.0f},{h + 3} 0,{h}Z"
    pc = f"M0,0 C{w * .3:.0f},-1 {w * .65:.0f},1 {w * .96:.0f},-1 L{w * .9:.0f},{h + 1} C{w * .62:.0f},{h} {w * .3:.0f},{h + 1} 0,{h}Z"
    seq = [pa, pb, pc, pb] * k + [pa]
    vals = ";".join(seq)
    kts = [i / (len(seq) - 1) for i in range(len(seq))]
    col = d.c(role)
    return (f'<g transform="translate({x} {y})"><rect x="-1.2" y="-4" width="2.4" height="{h * 2.6:.0f}" rx="1" fill="{shade(d.c("wood"), -.2)}"/>'
            f'<path class="sm" d="{pa}" fill="{col}">{smil("d", vals, kts, L, ".45 0 .55 1")}</path>'
            f'<path class="rm" d="{pa}" fill="{col}"/></g>')


def crate(d, x, y, g=6.0, role="sand", extra="", z=0.0):
    """Small isometric block whose bottom-centre is at (x, y)."""
    iso = Iso(d, x, y, g)
    t, l, r = d.faces(role)
    out = iso.box(-.5, -.5, z, 1, 1, .95, cols=(t, l, r))
    return f"<g{extra}>{out}</g>" if extra else out


def win_fill(d, lit=False):
    return d.c("glow") if (d.pal["night"] or lit) else mix(d.c("teal"), "#000000", .25)


def arch_path(u, v, w, h):
    """Arched opening in face space, bottom-left at (u, v) (v is the base line)."""
    return f"M{u:.1f},{v:.1f} V{v - h + w / 2:.1f} A{w / 2:.1f},{w / 2:.1f} 0 0 1 {u + w:.1f},{v - h + w / 2:.1f} V{v:.1f}Z"


def house(d, iso, x, y, z, w, dd, h, roof="terra", rh=1.0, wall="sand", windows=2, door=True, lit=False, ov=.25):
    """Gabled house, ridge along x. Windows and door sit on the +y face."""
    wt, wl, wr = d.faces(wall)
    rt, rl, rr = d.faces(roof)
    out = iso.shadow(x, y, w, dd, z)
    out += iso.box(x, y, z, w, dd, h, cols=(wt, wl, wr), top=False)
    out += iso.poly([(x + w, y, z + h), (x + w, y + dd, z + h), (x + w, y + dd / 2, z + h + rh)], wr)
    # roof: back slope then front slope
    out += iso.poly([(x - ov, y - ov, z + h - .05), (x + w + ov, y - ov, z + h - .05), (x + w + ov, y + dd / 2, z + h + rh), (x - ov, y + dd / 2, z + h + rh)], rl)
    out += iso.poly([(x - ov, y + dd + ov, z + h - .05), (x + w + ov, y + dd + ov, z + h - .05), (x + w + ov, y + dd / 2, z + h + rh), (x - ov, y + dd / 2, z + h + rh)], rt)
    out += iso.poly([(x + w + ov, y + dd + ov, z + h - .05), (x + w + ov, y + dd + ov, z + h - .2), (x + w + ov, y + dd / 2, z + h + rh - .15), (x + w + ov, y + dd / 2, z + h + rh)], rr)
    # windows and door on the +y face (face space: u px along x, v px down)
    g, hp = iso.g, iso.h
    fw = w * g
    content = ""
    n = windows
    ww = g * .42
    wh = hp * .62
    for i in range(n):
        u = fw * (i + 1) / (n + 1 + (1 if door else 0)) - ww / 2
        content += f'<path d="{arch_path(u, -hp * (h * .35), ww, wh)}" fill="{win_fill(d, lit)}"/>'
    if door:
        dw, dh = g * .62, hp * .95
        u = fw - fw / (n + 2) - dw / 2
        content += f'<path d="{arch_path(u, 0, dw, dh)}" fill="{shade(d.c("wood"), -.35)}"/>'
    out += iso.on_face(x, y, z, w, dd, "L", content)
    return out


def tower(d, iso, x, y, z, w, dd, h, roof="terra", rh=2.0, windows=2, flagged=True):
    wt, wl, wr = d.faces("sand")
    rt, rl, rr = d.faces(roof)
    out = iso.shadow(x, y, w, dd, z)
    out += iso.box(x, y, z, w, dd, h, cols=(wt, wl, wr), top=False)
    ov = .25
    zt = z + h
    ap = (x + w / 2, y + dd / 2, zt + rh)
    out += iso.poly([(x + w + ov, y - ov, zt - .05), (x + w + ov, y + dd + ov, zt - .05), ap], rr)
    out += iso.poly([(x - ov, y + dd + ov, zt - .05), (x + w + ov, y + dd + ov, zt - .05), ap], rl)
    g, hp = iso.g, iso.h
    content = ""
    for i in range(windows):
        content += f'<path d="{arch_path(w * g * .3, -hp * (h * (.35 + .28 * i)), g * .34, hp * .56)}" fill="{win_fill(d)}"/>'
    out += iso.on_face(x, y, z, w, dd, "L", content)
    px, py = iso.p(*ap)
    return out, (px, py)


def ripples(d, x, y, n=3, w=60, delay=0.0):
    m = d.m
    p = m.L / 4
    out = ""
    for i in range(n):
        st = m.cycle([(0, "transform:translateX(-8px)"), (p / 2, "transform:translateX(8px)"), (p, "transform:translateX(-8px)")], p,
                     delay=(delay + i * .6) % p, base="transform:translateX(-8px)")
        out += (f'<path class="deco" d="M{x + i * 26},{y + i * 7} q{w * .15:.0f},-5 {w * .3:.0f},0 t{w * .3:.0f},0" fill="none" '
                f'stroke="{d.c("ripple")}" stroke-width="2.4" stroke-linecap="round" style="{st}"/>')
    return out
