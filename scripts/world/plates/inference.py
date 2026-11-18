"""P3 inference: the workshop. 16 s loop; key frame at 75 %.

 0.0-1.0  set A waits in the queue; shelves of last loop empty out under a fade
 1.0-3.0  A walks in together (a batch of three)                                   (sign 1 queue, sign 2 batch)
 3.2-5.0  set B walks up and waits at the door
 4.4-5.6  shelves fill with small blocks as the requests work                      (sign 3 cache)
 6.0-6.6  the first paper plane leaves the window, then one every ~1.2 s            (sign 4 tokens)
 7.6-8.4  a fourth request slips in mid-way (continuous batching)
10.0-11.2 two requests finish: their shelf slots empty
13.2-15.0 set B walks in; 15.0-16.0 set A walks up to the door for the next loop
"""
from ..doc import Doc
from ..iso import Iso
from ..props import bush, tree
from ..signs import chip, legend, marker, status_plaque
from ..tokens import LOOPS, shade
from .common import mailbox, paper_plane, sky, travel, walker

H = 810


def build(theme):
    L = LOOPS["inference"]
    d = Doc("i", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    iso = Iso(d, 470, 300, 50)
    out = sky(d, [(1050, 90, 1.0, 50, 2), (200, 70, .8, 40, 9), (700, 40, .7, 55, 12), (140, 560, .9, 50, 5), (1180, 600, 1.0, 60, 7)],
              [(-150, 1450, 130, 2, 1.1), (-150, 1450, 230, 9, .9)])
    out += iso.island(0, 0, 10.6, 6.2, "cream", layers=3)
    out += iso.stairs(.8, 6.2, 0, 14, "y", 1.6, .55, .4)
    out += tree(d, 100, 360, 1.3) + bush(d, 150, 420, 1.1) + tree(d, 1150, 500, 1.1)

    # ---- the workshop -----------------------------------------------------------------------------------------
    wx, wy, ww, wd, wh = 2.6, .4, 5.4, 3.2, 3.2
    wt, wl, wr = d.faces("sand")
    rt, rl, rr = d.faces("terra")
    out += iso.shadow(wx, wy, ww, wd, 0)
    out += iso.box(wx, wy, 0, ww, wd, wh, cols=(wt, wl, wr), top=False)
    out += iso.poly([(wx + ww, wy, wh), (wx + ww, wy + wd, wh), (wx + ww, wy + wd / 2, wh + 1.5)], wr)
    ov = .3
    out += iso.poly([(wx - ov, wy - ov, wh - .05), (wx + ww + ov, wy - ov, wh - .05), (wx + ww + ov, wy + wd / 2, wh + 1.5), (wx - ov, wy + wd / 2, wh + 1.5)], rl)
    out += iso.poly([(wx - ov, wy + wd + ov, wh - .05), (wx + ww + ov, wy + wd + ov, wh - .05), (wx + ww + ov, wy + wd / 2, wh + 1.5), (wx - ov, wy + wd / 2, wh + 1.5)], rt)
    g, hp = iso.g, iso.h
    # opening with shelves (face space)
    ou, oww, ohh = g * .7, g * 2.3, hp * 2.35
    inner = f'<path d="M{ou:.1f},0 V{-ohh + oww / 2:.1f} A{oww / 2:.1f},{oww / 2:.1f} 0 0 1 {ou + oww:.1f},{-ohh + oww / 2:.1f} V0Z" fill="{shade(d.c("sand"), -.5)}"/>'
    slots = []
    for r_, vy in enumerate((-hp * .78, -hp * 1.46)):
        inner += f'<rect x="{ou + 8:.1f}" y="{vy:.1f}" width="{oww - 16:.1f}" height="4" fill="{d.c("wood")}"/>'
        for c_ in range(3):
            slots.append((ou + 14 + c_ * (oww - 28) / 3, vy - 20))
    sl = list(zip(slots, [4.4, 4.8, 5.2, 5.5, 8.0, 5.9]))
    # blocks fill at the given time, and two of them empty out when requests finish
    fin = {1: 10.2, 4: 10.8, 0: 11.2}
    for idx, ((u, v), tf) in enumerate(sl):
        wins_ = [(tf, fin[idx])] if idx in fin else [(tf, L * .93)]
        st = m.windows(wins_, .35, "land")
        col = p["terra"] if idx == 4 else p["sand"]
        inner += (f'<g style="{st}"><rect x="{u:.1f}" y="{v:.1f}" width="{(oww - 28) / 3 - 6:.1f}" height="19" rx="2" fill="{col}"/>'
                  f'<rect x="{u:.1f}" y="{v:.1f}" width="{(oww - 28) / 3 - 6:.1f}" height="6" rx="2" fill="{shade(col, .15)}"/></g>')
    # lantern at the door
    inner += f'<g transform="translate({ou - 14:.1f} {-ohh * .62:.1f})"><circle r="11" fill="{p["glow"]}" opacity=".34"/><rect x="-4" y="-6" width="8" height="12" rx="2" fill="{shade(p["teal"], -.35)}"/><rect x="-2.6" y="-4" width="5.2" height="8" rx="1.3" fill="{p["glow"]}"/></g>'
    # small window (the paper planes leave through it)
    wu = g * 3.9
    inner += (f'<path d="M{wu:.1f},{-hp * 1.1:.1f} V{-hp * 1.72:.1f} A{g * .3:.1f},{g * .3:.1f} 0 0 1 {wu + g * .6:.1f},{-hp * 1.72:.1f} V{-hp * 1.1:.1f}Z" fill="{shade(d.c("sand"), -.5)}"/>')
    out += iso.on_face(wx, wy, 0, ww, wd, "L", inner)
    out += iso.on_face(wx, wy, 0, ww, wd, "L", f'<rect x="{g * 3.6:.1f}" y="{-hp * 1.1 + 2:.1f}" width="{g * 1.2:.1f}" height="4" fill="{d.c("wood")}"/>')
    # ---- signposts (front edge) -------------------------------------------------------------------------------
    for k, (x, y, t_on) in enumerate([(8.4, 4.9, 1.0), (4.3, 4.6, 3.0), (2.2, 3.9, 4.6), (9.9, 2.6, 6.2)]):
        out += marker(d, iso, x, y, k + 1, t_on)
    out += legend(d, 40, 70, [(1, "requests queue", 1.0), (2, "batch shares the GPU", 3.0), (3, "cache fills & frees", 4.6), (4, "tokens stream out", 6.2)])
    out += chip(d, 40, 24, "schematic")

    # ---- mailboxes (three clients) --------------------------------------------------------------------------------
    mb = [iso.p(9.0, 1.0, 0), iso.p(9.5, 2.1, 0), iso.p(8.9, 3.3, 0)]
    for k, (mx, my) in enumerate(mb):
        out += mailbox(d, mx, my, 1.25, 7.0 + k * 1.6)

    # ---- characters -------------------------------------------------------------------------------------------------
    qpos = [(5.4, 4.15), (6.25, 4.25), (7.1, 4.35)]
    door = (4.7, 3.95)
    def block_in_hands():
        return f'<g transform="translate(14 -16)">{_blk(d)}</g>'
    sets = {}
    for i, (qx, qy) in enumerate(qpos):
        # set A: waits at t=0, enters 1.0-3.0 (staggered), vanishes at the door; re-appears walking in 15.0-16.0
        ta = 1.0 + i * .5
        pts = [(0, qx, qy, 0, "opacity:1"), (ta, qx, qy, 0, "opacity:1"), (ta + 1.7, door[0], door[1], 0, "opacity:1"),
               (ta + 1.9, door[0], door[1] - .3, 0, "opacity:0"), (14.4, door[0], door[1] - .3, 0, "opacity:0"),
               (14.5, 10.2, qy + .6, 0, "opacity:0"), (14.6, 10.2, qy + .6, 0, "opacity:1"), (L - .05 + .05, qx, qy, 0, "opacity:1")]
        out += walker(d, iso, pts, "teal", 1.9, True, carry=block_in_hands(), wp=.8, delay=i * .2)
        # set B: arrives 3.4-5.0 and waits; enters 13.2-15.0
        tb = 13.2 + i * .45
        ptsb = [(0, 10.2, qy + .6, 0, "opacity:0"), (3.4 + i * .3, 10.2, qy + .6, 0, "opacity:0"), (3.5 + i * .3, 10.2, qy + .6, 0, "opacity:1"),
                (5.2 + i * .3, qx, qy, 0, "opacity:1"), (tb, qx, qy, 0, "opacity:1"), (tb + 1.5, door[0], door[1], 0, "opacity:1"),
                (tb + 1.7, door[0], door[1] - .3, 0, "opacity:0"), (L, door[0], door[1] - .3, 0, "opacity:0")]
        out += walker(d, iso, ptsb, "teal", 1.9, True, carry=block_in_hands(), wp=.8, delay=.1 + i * .2)
    # the fourth request, in terracotta, slips in mid-way
    pts4 = [(0, 10.2, 4.9, 0, "opacity:0"), (6.4, 10.2, 4.9, 0, "opacity:0"), (6.5, 10.2, 4.9, 0, "opacity:1"), (8.0, 4.7, 3.95, 0, "opacity:1"),
            (8.2, 4.7, 3.65, 0, "opacity:0"), (L, 4.7, 3.65, 0, "opacity:0")]
    out += walker(d, iso, pts4, "terra", 1.9, True, carry=block_in_hands(), wp=.8, delay=.3)

    # ---- paper planes ------------------------------------------------------------------------------------------------------
    wxp, wyp = wx + 3.9 + .3, wy + wd + .05
    for k in range(5):
        tt = 6.2 + k * 1.25
        tgt = mb[k % 3]
        # world-space arc via iso points from the window to a mailbox slot
        tx, ty = [(9.0, 1.0), (9.5, 2.1), (8.9, 3.3)][k % 3]
        pts = [(0, wxp, wyp, 2.0, "opacity:0"), (tt, wxp, wyp, 2.0, "opacity:0"), (tt + .05, wxp, wyp, 2.0, "opacity:1"),
               (tt + .5, (wxp + tx) / 2, (wyp + ty) / 2 + .6, 3.2, "opacity:1", "settle"),
               (tt + 1.35, tx, ty, 1.35, "opacity:1", "travel"), (tt + 1.5, tx, ty, 1.2, "opacity:0"), (L, tx, ty, 1.2, "opacity:0")]
        st, (X, Y) = travel(m, iso, pts)
        out += f'<g style="{st}"><g transform="translate({X:.1f} {Y:.1f})">{paper_plane(d, 1.15)}</g></g>'
    out += status_plaque(d, 1250, 24, "IN PROGRESS", "IN PROGRESS")
    return d.render(out, "Inference: the workshop", DESC)


def _blk(d):
    from ..iso import Iso
    mini = Iso(d, 0, 0, 7.5)
    return mini.box(-.5, -.5, 0, 1, 1, .9, cols=d.faces("sand"))


DESC = ("Schematic, in progress. A terracotta-roofed workshop with open shelves, the cache. Workers carrying blocks queue at its door: "
        "requests. Three go in together as a batch and a fourth slips in mid-way as a slot frees. Shelves fill with small blocks as "
        "each request works and empty when it finishes. Paper planes fly out of the window to three mailboxes: tokens streaming out. "
        "Numbered signposts: queue, batch, cache, tokens.")
