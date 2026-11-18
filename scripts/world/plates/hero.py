"""P1 hero: the tower. One-time intro, then a 14 s loop of ambient life."""
from ..doc import Doc
from ..iso import Iso
from ..props import bird, bush, cloud, flag, lantern, mountains, sun, tower, tree
from ..rig import character, idle
from .common import walker
from ..tokens import LOOPS

H = 640


def build(theme):
    L = LOOPS["hero"]
    d = Doc("h", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    ink, bg = p["ink"], p["bg"]
    out = ""
    # sky: sun, mountains, clouds, birds
    out += sun(d, 1100, 160, 66)
    out += mountains(d, 900, 380, 380, 120)
    out += cloud(d, 1000, 120, 1.0, 50, 2) + cloud(d, 330, 70, .8, 40, 7) + cloud(d, 850, 290, .7, 60, 11) + cloud(d, 150, 520, .9, 50, 5)
    out += cloud(d, 1130, 560, 1.1, 70, 9)
    out += bird(d, -120, 1400, 52, 0, 1.1) + bird(d, -120, 1400, 92, 3.2, .9) + bird(d, -120, 1400, 520, 8, 1)

    world = ""
    # island with the tower (back) and a lower terrace (front), stairs running off the bottom edge
    iso = Iso(d, 262, 292, 38)
    world += iso.island(0, 0, 5.6, 4.4, "cream", layers=3)
    # lower terrace to the right-front
    world += iso.stairs(.7, 4.4, 0, 16, "y", 1.5, .55, .4)
    world += tree(d, 120, 380, 1.1) + bush(d, 150, 405, 1.0)
    twr, apex = tower(d, iso, .5, .5, 0, 2.4, 2.4, 4.4, "terra", 2.2, 2)
    world += twr
    ax, ay = apex
    world += flag(d, ax, ay - 14, 34, 16, "terra")
    world += bush(d, 388, 400, .9)
    # lantern holder on the terrace beside the tower, waving a lantern
    px, py = iso.p(3.9, 2.9, 0)
    wave = m.cycle([(0, "transform:rotate(-8deg)"), (1, "transform:rotate(8deg)"), (2, "transform:rotate(-8deg)")], 2.0,
                   origin="50% 0%", base="transform:rotate(-8deg)")
    holder = character(d, px, py, "teal", 1.7, False, st={**idle(m, L / 4), "armN": "transform-box:fill-box;transform-origin:50% 8%;transform:rotate(-150deg)"})
    # lantern on the raised hand
    lx, ly = px + 19, py - 62
    world += holder
    world += f'<g transform="translate({lx} {ly})"><g style="{wave}">{lantern(d, 0, 12, 1.5, 0)}</g></g>'
    # banner hanging from the tower
    bx, by = iso.p(4.9, 1.2, 1.9)
    sway = m.cycle([(0, "transform:rotate(-2deg)"), (1.75, "transform:rotate(2deg)"), (3.5, "transform:rotate(-2deg)")], 3.5,
                   origin="50% 0%", base="transform:rotate(-2deg)")
    world += (f'<g transform="translate({bx - 4:.0f} {by - 6:.0f})"><g style="{sway}">'
            f'<rect x="-2" y="0" width="4" height="10" fill="{p["wood"]}"/>'
            f'<path d="M-52,10 H52 V58 L0,48 L-52,58Z" fill="{p["board"]}" stroke="{p["terra"]}" stroke-width="2"/>'
            f'{t.text("open to", 0, 30, 15, "body", ink, anchor="middle")}{t.text("internships", 0, 46, 15, "body", ink, anchor="middle")}</g></g>')

    # a second figure climbs the stairs carrying a block (step i: y = 4.4 + .55 i, top z = -.4 i)
    def st_(i):
        return (1.45, 4.4 + .55 * i + .27, -.4 * i)
    from ..props import crate
    pts = [(0, *st_(12), "opacity:0"), (.2, *st_(12), "opacity:1"), (7.0, *st_(1), "opacity:1"), (7.6, 1.45, 3.9, 0, "opacity:1"),
           (12.4, 1.45, 3.9, 0, "opacity:1"), (13.0, 1.45, 3.9, 0, "opacity:0"), (L, *st_(12), "opacity:0")]
    world += walker(d, iso, pts, "terra", 1.5, True, carry=f'<g transform="translate(14 -16)">{crate(d, 0, 0, 8.5)}</g>', wp=.7)
    out += f'<g style="{m.once("opacity:0;transform:translateY(38px)", "opacity:1;transform:translateY(0)", 1.5, .1)}">{world}</g>'
    # name, role
    name_y = 232
    def rise(row):
        return lambda k: m.once("opacity:0;transform:translateY(26px)", "opacity:1;transform:translateY(0)", .7, .35 + row * .25 + k * .045)
    out += t.text("Chaitanaya", 470, name_y, 100, "display", ink, -.01, gstyle=rise(0))
    out += t.text("Srivastava", 470, name_y + 98, 100, "display", ink, -.01, gstyle=rise(1))
    role = t.text("Backend systems  ·  AI infrastructure  ·  ML", 474, name_y + 160, 36, "body", ink)
    out += f'<g style="{m.once("opacity:0", "opacity:1", .6, 1.35)}">{role}</g>'
    # narrow layout: availability pill, large
    out += (f'<g class="n" style="{m.once("opacity:0", "opacity:1", .6, 1.5)}"><rect x="470" y="{name_y + 190}" width="700" height="66" rx="33" fill="{p["board"]}" stroke="{p["terra"]}" stroke-width="3"/>'
            f'<circle cx="505" cy="{name_y + 223}" r="11" fill="{p["terra"]}"/>{t.text("open to internships", 530, name_y + 236, 38, "body", ink)}</g>')
    return d.render(out, "Chaitanaya Srivastava", "A small floating island with a stone tower, a flag and a waving lantern-holder. "
                    "Name: Chaitanaya Srivastava. Backend systems, AI infrastructure, ML. A banner reads open to internships. "
                    "Stairs lead down to the next island.")
