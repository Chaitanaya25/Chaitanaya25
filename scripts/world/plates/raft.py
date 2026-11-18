"""P4 raft: the ring village. 18 s loop; the key frame (13.5 s) shows the healed cluster with the new leader.

 1.0-3.0  letter-birds fly from the leader (A) to every house                          (sign 1)
 4.0-4.8  a dashed fence slides across the island: A and B on one side, C D E on the other   (sign 2)
 4.6-6.2  two birds bounce off the fence
 6.5-9.4  D's lantern blinks; vote requests to C and E, replies back                    (sign 3)
 9.2-10.6 the one crown hops from A to D (never two crowns)
11.5-12.1 the fence lifts
12.2-13.8 D's birds reach A and B; A's lantern settles to follower                       (sign 4)
16.2-17.6 the crown returns to A quietly for the next loop
"""
import math

from ..doc import Doc
from ..iso import Iso
from ..props import bush, house, lantern, tree
from ..signs import chip, legend, marker, status_plaque
from ..rig import character, idle
from ..tokens import LOOPS, shade
from .common import crown, letter_bird, sky, travel

H = 770
R = 3.6
POS = {k: (R * math.cos(math.radians(a)), R * math.sin(math.radians(a))) for k, a in zip("ABCDE", (200, 270, 340, 50, 120))}
ROOF = {"A": "teal", "B": "teal", "C": "teal", "D": "terra", "E": "teal"}


def build(theme):
    L = LOOPS["raft"]
    d = Doc("r", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    m.key = .75
    iso = Iso(d, 640, 352, 50)
    out = sky(d, [(1100, 100, 1.0, 50, 2), (170, 80, .9, 40, 9), (700, 40, .7, 55, 12), (1150, 600, 1.0, 60, 6), (130, 640, .8, 45, 4)],
              [(-150, 1450, 150, 1, 1.1), (-150, 1450, 240, 10, .9)])
    # island
    out += iso.round_island(0, 0, 6.4, "cream", layers=3)
    out += tree(d, 215, 540, 1.3) + tree(d, 1115, 540, 1.3) + bush(d, 255, 595, 1.0) + bush(d, 1070, 600, 1.0)
    # dotted ring path
    ring = " ".join("%.1f,%.1f" % iso.p(R * math.cos(a / 40 * math.tau), R * math.sin(a / 40 * math.tau), 0) for a in range(41))
    out += f'<polyline points="{ring}" fill="none" stroke="{p["deep"]}" stroke-width="3.4" stroke-linecap="round" stroke-dasharray="1 12" opacity=".7"/>'
    # ---- fence ---------------------------------------------------------------------------------------------------
    f0, f1 = (3.9, -3.5), (-4.1, 2.4)
    fpts = " ".join("%.1f,%.1f" % iso.p(x, y, 0) for x, y in (f0, f1))
    reveal = m.loop([(0, "stroke-dashoffset:100;opacity:0"), (3.9, "stroke-dashoffset:100;opacity:0"), (4.0, "stroke-dashoffset:100;opacity:1"),
                     (4.9, "stroke-dashoffset:0;opacity:1"), (11.5, "stroke-dashoffset:0;opacity:1"), (12.1, "stroke-dashoffset:0;opacity:0"),
                     (L, "stroke-dashoffset:100;opacity:0")], "travel")
    out += (f'<polyline points="{fpts}" fill="none" stroke="{p["terra"]}" stroke-width="4" stroke-dasharray="100" pathLength="100" '
            f'stroke-linecap="round" style="{reveal}"/>')
    posts = ""
    for j in range(7):
        x = f0[0] + (f1[0] - f0[0]) * j / 6
        y = f0[1] + (f1[1] - f0[1]) * j / 6
        X, Y = iso.p(x, y, 0)
        pst = m.loop([(0, "opacity:0"), (4.0 + j * .12, "opacity:0"), (4.3 + j * .12, "opacity:1"), (11.5, "opacity:1"), (12.1, "opacity:0"), (L, "opacity:0")], "settle")
        posts += (f'<g style="{pst}"><rect x="{X - 2:.1f}" y="{Y - 22:.1f}" width="4" height="22" rx="1.5" fill="{p["wood"]}"/>'
                  f'<path d="M{X + 2:.1f},{Y - 22:.1f} h9 v6 h-9z" fill="{p["terra"]}"/></g>')
    out += posts

    # houses, back to front
    order = sorted("ABCDE", key=lambda k: POS[k][0] + POS[k][1])
    crowns = {}
    for k in order:
        x, y = POS[k]
        out += house(d, iso, x - .8, y - .7, 0, 1.6, 1.4, 1.35, ROOF[k], 1.0, "sand", windows=1, door=True, lit=(k == "D" or k == "A"))
    # lanterns on the roofs' front corner; A dims while stale, D blinks while campaigning
    for k in "ABCDE":
        x, y = POS[k]
        lx, ly = iso.p(x + .72, y + .8, 1.0)
        if k == "A":
            br = m.loop([(0, "opacity:1"), (8.6, "opacity:1"), (9.6, "opacity:.35"), (11.0, "opacity:.35"), (12.4, "opacity:.6"),
                         (13.8, "opacity:.9"), (L - .5, "opacity:.9"), (L, "opacity:1")], "settle")
        elif k == "D":
            br = m.loop([(0, "opacity:.6"), (6.3, "opacity:.6"), (6.8, "opacity:1"), (7.3, "opacity:.5"), (7.8, "opacity:1"), (8.3, "opacity:.5"),
                         (8.8, "opacity:1"), (L - 1, "opacity:1"), (L, "opacity:.6")], "settle")
        else:
            br = f"opacity:.75"
        out += f'<g transform="translate({lx:.1f} {ly:.1f})"><g style="{br}">{lantern(d, 0, 0, 1.0, 0)}</g></g>'
    # the one crown
    ptsC = []
    def top(k):
        x, y = POS[k]
        return x, y
    ax, ay = top("A")
    dx, dy = top("D")
    zc = 2.65
    pts = [(0, ax, ay, zc, "opacity:1"), (9.2, ax, ay, zc, "opacity:1"), (9.8, (ax + dx) / 2, (ay + dy) / 2, zc + 3.2, "opacity:1", "settle"),
           (10.6, dx, dy, zc, "opacity:1", "land"), (16.1, dx, dy, zc, "opacity:1"), (16.4, dx, dy, zc, "opacity:0"),
           (16.6, ax, ay, zc, "opacity:0"), (17.3, ax, ay, zc, "opacity:1"), (L, ax, ay, zc, "opacity:1")]
    cst, (cx0, cy0) = travel(m, iso, pts)
    # base (key frame) is 13.5 s -> on D
    out += f'<g style="{cst}"><g transform="translate({cx0:.1f} {cy0:.1f})">{crown(d, 1.25)}</g></g>'

    # ---- letter birds -----------------------------------------------------------------------------------------------------
    def bird_run(src, dst, t0, t1, z=3.6, via=None, bounce=None, scale=1.15):
        sx, sy = POS[src]
        tx, ty = POS[dst]
        pts = [(0, sx, sy, 2.4, "opacity:0"), (t0, sx, sy, 2.4, "opacity:0"), (t0 + .12, sx, sy, 2.6, "opacity:1")]
        if bounce:
            mx, my = bounce
            tm = (t0 + t1) / 2
            pts += [(tm, mx, my, z, "opacity:1", "settle"), (t1, sx, sy, 2.6, "opacity:1", "settle"), (t1 + .15, sx, sy, 2.6, "opacity:0")]
        else:
            pts += [((t0 + t1) / 2, (sx + tx) / 2, (sy + ty) / 2, z, "opacity:1", "settle"), (t1, tx, ty, 2.6, "opacity:1", "settle"),
                    (t1 + .15, tx, ty, 2.5, "opacity:0")]
        pts += [(L, pts[-1][1], pts[-1][2], pts[-1][3], "opacity:0")]
        st, (X, Y) = travel(m, iso, pts)
        face = -1 if tx < sx else 1
        return f'<g style="{st}"><g transform="translate({X:.1f} {Y:.1f}) scale({face} 1)">{letter_bird(d, scale)}</g></g>'
    for k, dst in enumerate("BCDE"):
        out += bird_run("A", dst, 1.0 + k * .25, 2.6 + k * .25)
    mid = ((f0[0] + f1[0]) / 2 + .3, (f0[1] + f1[1]) / 2 + .3)
    out += bird_run("A", "C", 4.8, 6.0, 4.2, bounce=(-.4, -.7))
    out += bird_run("A", "E", 5.1, 6.4, 4.2, bounce=(-1.6, 1.4))
    out += bird_run("D", "C", 7.0, 8.2)
    out += bird_run("D", "E", 7.1, 8.3)
    out += bird_run("C", "D", 8.3, 9.4, scale=1.0)
    out += bird_run("E", "D", 8.4, 9.5, scale=1.0)
    out += bird_run("D", "A", 12.2, 13.7)
    out += bird_run("D", "B", 12.4, 13.9)

    # ---- signposts ---------------------------------------------------------------------------------------------------------
    for k, (x, y, t_on) in enumerate([(-4.6, -1.0, 1.0), (-1.4, 1.6, 4.0), (3.9, 4.0, 7.0), (5.0, 1.3, 12.2)]):
        out += marker(d, iso, x, y, k + 1, t_on)
    out += legend(d, 40, 70, [(1, "replicate", 1.0), (2, "split", 4.0), (3, "elect", 7.0), (4, "heal", 12.2)])
    vx, vy = iso.p(.3, .4, 0)
    out += character(d, vx, vy, "teal", 1.6, False, st=idle(m, L / 6))
    vx, vy = iso.p(1.5, -.9, 0)
    out += character(d, vx, vy, "terra", 1.5, True, st=idle(m, L / 6, 1.2))
    out += status_plaque(d, 1250, 24, "PLANNED", "PLANNED")
    # schematic tag
    out += chip(d, 40, 24, "schematic")
    return d.render(out, "Raft: the ring village", DESC)


DESC = ("Schematic, planned. Five houses stand in a ring on a round island; the leader's house wears the only crown. Letter-birds carry "
        "envelopes from the leader to every house: replication. A dashed fence slides across the island, cutting off the leader and one "
        "neighbour. On the majority side one house blinks its lantern and asks its neighbours for votes; two reply, and the crown hops to "
        "the new leader. The fence lifts, birds reach the old leader again and it settles back to follower. No results yet.")
