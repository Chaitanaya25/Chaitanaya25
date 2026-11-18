"""P2 Chronicle: the aqueduct conveyor. 18 s loop; the key frame is the hold after the replay.

 0.0-1.4  the first blocks settle in; a worker steps out of the storeroom
 2.6-5.0  worker 1 puts a block on the belt; it rides to the row and settles        (sign 1)
 8.4-9.9  worker 2 trips; the block flies off and hangs in the air; he is fenced out  (sign 2)
 9.0-12.2 the hourglass flips and drains over 3 s                                     (sign 3)
12.0-15.5 the terracotta worker runs in, leaps, catches the block, places it          (sign 4)
15.6-16.8 the rewind wheel turns back; a ghost path runs back along the blocks
17.0-18.0 fenced worker walks off, everything fades; fresh blocks settle in at 0
"""
from ..doc import Doc
from ..iso import Iso
from ..props import bush, crate, lantern, tree
from ..rig import character, idle, pose, walk
from ..signs import engraved, signpost, status_plaque
from ..tokens import LOOPS, shade
from .common import sky, travel

H = 800


def build(theme):
    L = LOOPS["chronicle"]
    d = Doc("c", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    m.key = .88
    ink = p["ink"]
    iso = Iso(d, 330, 250, 44)
    P = iso.p
    wp = .9                       # walk period (divides 18)
    out = ""
    out += sky(d, [(1010, 110, 1.0, 50, 2), (240, 70, .8, 40, 8), (700, 60, .7, 60, 12), (1150, 420, .9, 50, 5), (110, 640, .8, 40, 3)],
               [(-150, 1450, 150, 0, 1.1), (-150, 1450, 260, 6.5, .9), (-150, 1450, 90, 12, 1)])

    zb = 2.6   # bridge height below the deck
    # ---- left island with the storeroom ------------------------------------------------------
    out += iso.island(-3.4, -1.4, 5.2, 5.6, "cream", layers=3)
    out += tree(d, 100, 330, 1.2) + bush(d, 168, 392, 1.0)
    out += iso.stairs(-3.0, 4.2, 0, 14, "y", 1.5, .55, .4)
    out += house(d, iso)
    # crates stacked by the door
    for (cx, cy, z) in ((-1.2, -1.1, 0), (-.4, -1.1, 0), (-.8, -1.05, .9)):
        out += iso.box(cx, cy, z, .8, .8, .85, "sand")

    # ---- bridge body (aqueduct) ---------------------------------------------------------------
    bx0, bx1, by0, by1 = 0, 11.8, 0, 2.0
    t_, l_, r_ = d.faces("sage")
    out += iso.box(bx0, by0, -zb, bx1 - bx0, by1 - by0, zb, cols=(d.faces("cream")[0], l_, r_))
    arches = ""
    g, hp = iso.g, iso.h
    n_arch = 5
    fw = (bx1 - bx0) * g
    aw = fw / n_arch * .6
    for i in range(n_arch):
        u = fw / n_arch * (i + .2)
        arches += (f'<path d="M{u:.1f},0 V{-hp * 1.25 + aw / 2:.1f} A{aw / 2:.1f},{aw / 2:.1f} 0 0 1 {u + aw:.1f},{-hp * 1.25 + aw / 2:.1f} V0Z" '
                   f'fill="{shade(d.c("sage"), -.28)}"/>')
    out += iso.on_face(bx0, by0, -zb, bx1 - bx0, by1 - by0, "L", arches)
    out += engraved(d, iso, bx0, by0, -zb + 1.62, bx1 - bx0, by1 - by0, "CHRONICLE", "L", 38, .3)
    # deck lip
    out += iso.box(bx0, by0, -.18, bx1 - bx0, by1 - by0, .18, cols=(d.faces("cream")[0], d.faces("cream")[1], d.faces("cream")[2]))

    # ---- right island: pedestal with hourglass -----------------------------------------------
    out += iso.island(11.8, -.8, 5.4, 3.6, "cream", layers=3)
    out += tree(d, 1085, 548, 1.2) + bush(d, 905, 585, 1.0) + bush(d, 1150, 520, .8)
    ped = iso.box(14.9, 0.9, 0, 1.4, 1.4, .55, "sand")
    out += ped
    out += engraved(d, iso, 14.9, .9, 0, 1.4, 1.4, "3 s", "L", 32, .1)

    # ---- signposts (behind the belt) ------------------------------------------------------------
    out += signpost(d, iso, 3.0, -.4, 1, "logged", 5.0)
    out += signpost(d, iso, 6.6, -.4, 2, "crash", 8.9)
    out += signpost(d, iso, 9.3, -.4, 3, "lease 3 s", 9.6)
    out += signpost(d, iso, 12.7, -.3, 4, "resume", 15.4)

    # ---- belt ----------------------------------------------------------------------------------------
    bx_a, bx_b, bw0, bw1 = 2.2, 11.4, .2, 1.2
    bt, bl, br_ = d.faces("teal")
    out += iso.box(bx_a, bw0, 0, bx_b - bx_a, bw1 - bw0, .34, cols=(shade(d.c("teal"), .06), bl, br_))
    # moving dashes on the belt top (flat plane), advance while blocks travel
    dash = 14
    off = [(0, 0), (3.2, 0), (5.0, -dash * 2), (14.8, -dash * 2), (15.6, -dash * 2), (16.8, -dash * 3), (L, -dash * 3)]
    dst = m.loop([(t0, f"stroke-dashoffset:{o}") for t0, o in off], "linear", base=f"stroke-dashoffset:{-dash * 3}")
    belt_top = (f'<g transform="{iso.top_matrix(bx_a, bw0, .34)}"><path d="M0,{(bw1 - bw0) * .5:.2f} H{bx_b - bx_a:.2f}" fill="none" '
                f'stroke="{shade(d.c("teal"), .28)}" stroke-width=".07" stroke-dasharray=".18 .26" style="{dst}"/></g>')
    out += belt_top
    # rollers on the belt face
    rl = ""
    n_r = 28
    fw2 = (bx_b - bx_a) * g
    for i in range(n_r):
        rl += f'<circle cx="{fw2 / n_r * (i + .5):.1f}" cy="{-hp * .17:.1f}" r="{hp * .09:.1f}" fill="{shade(d.c("teal"), .32)}"/>'
    out += iso.on_face(bx_a, bw0, 0, bx_b - bx_a, bw1 - bw0, "L", rl)

    # ---- block row ----------------------------------------------------------------------------------------
    by_blk = .3
    def slot(j):
        return 10.4 - 1.15 * j
    z0 = .34
    for j, tt in ((0, .2), (1, .5), (2, .8)):
        st = m.loop([(0, "opacity:0;transform:translateY(-18px)"), (tt, "opacity:0;transform:translateY(-18px)"),
                     (tt + .6, "opacity:1;transform:translateY(0);animation-timing-function:cubic-bezier(.34,1.56,.64,1)"),
                     (L - 1.1, "opacity:1;transform:translateY(0)"), (L - .5, "opacity:0;transform:translateY(0)"), (L, "opacity:0;transform:translateY(-18px)")], "settle")
        out += f'<g style="{st}">{iso.box(slot(j), by_blk, z0, .95, .95, .8, "sand")}</g>'
    # block A rides from the belt start to slot 3
    ax0, ax3 = 2.7, slot(3)
    A_style, (aX, aY) = travel(m, iso, [
        (0, ax0 + .475, by_blk + .475, z0 + 1.7, "opacity:0"), (2.55, ax0 + .175, by_blk + .475, z0 + 1.7, "opacity:0"),
        (2.7, ax0 + .475, by_blk + .475, z0 + 1.7, "opacity:1"),
        (3.2, ax0 + .475, by_blk + .475, z0, "opacity:1", "land"), (5.0, ax3 + .475, by_blk + .475, z0, "opacity:1", "linear"),
        (L - 1.1, ax3 + .475, by_blk + .475, z0, "opacity:1"), (L - .5, ax3 + .475, by_blk + .475, z0, "opacity:0"), (L, ax0 + .475, by_blk + .475, z0 + 1.7, "opacity:0")])
    from ..iso import Iso as _I
    out += f'<g style="{A_style}"><g transform="translate({aX:.1f} {aY:.1f})">{_I(d, 0, 0, iso.g).box(-.475, -.475, 0, .95, .95, .8, "sand")}</g></g>'
    # block A drawn relative to Iso origin: re-anchor (box coords are absolute, so translate inverse)
    # ---- hourglass ---------------------------------------------------------------------------------------------
    out += hourglass(d, iso, 15.6, 1.6, .55)

    # ---- characters ---------------------------------------------------------------------------------------------
    lane1, lane2 = 1.45, 1.78
    # worker 1: steps out of the storeroom, walks to the belt start, puts the block on, then stands by
    w1_root, (w1x, w1y) = travel(m, iso, [
        (0, -.7, lane1, 0, "opacity:0"), (.3, -.7, lane1, 0, "opacity:1"), (2.6, 2.0, lane1, 0, "opacity:1"),
        (L - 1.1, 2.0, lane1, 0, "opacity:1"), (L - .5, 2.0, lane1, 0, "opacity:0"), (L, -.7, lane1, 0, "opacity:0")])
    carried1 = f'<g style="{m.windows([(0, 3.0)], .2)}">{crate(d, 16, -18, 10.5)}</g>'
    out += character(d, w1x, w1y, "teal", 2.1, False, st=walk(m, wp, carry=True), rest={**pose(), **idle(m, L / 6)},
                     moving=[(.3, 2.7)], root=w1_root, carried=carried1)
    # worker 2: the tripper
    ft = 8.4
    w2_pts = [(0, -.7, lane2, 0, "opacity:0"), (1.9, -.7, lane2, 0, "opacity:0"), (2.2, -.7, lane2, 0, "opacity:1"),
              (ft, 6.6, lane2, 0, "opacity:1"), (ft + .5, 7.0, lane2, 0, "opacity:1", "settle"),
              (10.0, 7.0, lane2, 0, "opacity:.45"), (16.5, 7.0, lane2, 0, "opacity:.45"),
              (17.3, 3.5, lane2, 0, "opacity:.2", "settle"), (17.8, 0, lane2, 0, "opacity:0"), (L, -.7, lane2, 0, "opacity:0")]
    w2_root, (w2x, w2y) = travel(m, iso, w2_pts)
    lean = m.loop([(0, "transform:rotate(0deg)"), (ft - .15, "transform:rotate(0deg)"),
                   (ft + .25, "transform:rotate(26deg)"), (ft + .65, "transform:rotate(78deg);animation-timing-function:cubic-bezier(.34,1.56,.64,1)"),
                   (10.2, "transform:rotate(8deg) scaleY(.78)"), (16.5, "transform:rotate(8deg) scaleY(.78)"),
                   (17.0, "transform:rotate(0deg) scaleY(1)"), (L, "transform:rotate(0deg)")], "settle", origin="50% 100%")
    carried2 = f'<g style="{m.windows([(0, ft + .3)], .1)}">{crate(d, 16, -18, 10.5)}</g>'
    out += character(d, w2x, w2y, "teal", 2.1, False, st=walk(m, wp, carry=True, delay=.2), rest=pose(0, 0, 0, 0) | idle(m, L / 6),
                     moving=[(2.2, ft + .15)], root=w2_root, carried=carried2, lean=lean)
    fx_, fy_ = iso.p(7.0, lane2, 0)
    fence = m.loop([(0, "opacity:0"), (9.6, "opacity:0"), (10.1, "opacity:.9"), (16.3, "opacity:.9"), (16.8, "opacity:0"), (L, "opacity:0")])
    out += (f'<ellipse cx="{fx_:.1f}" cy="{fy_:.1f}" rx="40" ry="17" fill="none" stroke="{p["deep"]}" stroke-width="2.4" '
            f'stroke-dasharray="6 6" style="{fence}"/>')
    out += dazed(d, iso, 7.0, lane2, 9.4)
    # the block that flies off, hangs in the air, and is caught
    out += flying_block(d, iso, ft)
    # terracotta runner
    out += runner(d, iso, 1.2, wp)
    # ghost path + wheel
    out += rewind(d, iso, slot)
    # status
    out += status_plaque(d, 1250, 24, "LIVE", "LIVE")
    return d.render(out, "Chronicle: the aqueduct conveyor", DESC)


DESC = ("An aqueduct bridge carries a conveyor belt: the append-only event log. Teal workers put numbered blocks on the belt "
        "and they settle in an ordered row. One worker trips and his block flies off and hangs in the air; he is fenced out. "
        "An hourglass drains over three seconds, then a terracotta worker runs in, catches the block and places it as the next "
        "step, with no gap and no duplicate. A rewind wheel turns back and a ghost path runs back along the blocks. Status: LIVE.")


def house(d, iso):
    from ..props import house as hs
    return hs(d, iso, -2.6, -.8, 0, 2.4, 2.0, 2.0, "terra", 1.0, "sand", windows=1, door=True, lit=True)


def hourglass(d, iso, x, y, z):
    m, p = d.m, d.pal
    L = m.L
    X, Y = iso.p(x, y, z)
    wd, hh = 30, 62
    glass = d.c("cloud") if not p["night"] else shade(p["sand"], .1)
    frame = shade(p["wood"], -.25)
    sand = p["terra"]
    topb = f"M{-wd / 2},{-hh} H{wd / 2} Q{wd / 2},{-hh * .5} 4,0 Q{wd / 2},{hh * .5} {wd / 2},{hh} H{-wd / 2} Q{-wd / 2},{hh * .5} -4,0 Q{-wd / 2},{-hh * .5} {-wd / 2},{-hh}Z"
    d.add_def("hgl", f'<clipPath id="c-hg"><path d="{topb}"/></clipPath>')
    # sand A (bottom half in group space, full at the start), sand B (top half, empty at start)
    a_fill = m.loop([(0, "transform:scaleY(1)"), (9.0, "transform:scaleY(1)"), (9.7, "transform:scaleY(1)"), (12.2, "transform:scaleY(0)"),
                     (17.4, "transform:scaleY(0)"), (17.6, "transform:scaleY(1)"), (L, "transform:scaleY(1)")], "linear", origin="50% 100%")
    b_fill = m.loop([(0, "transform:scaleY(0)"), (9.7, "transform:scaleY(0)"), (12.2, "transform:scaleY(1)"),
                     (17.4, "transform:scaleY(1)"), (17.6, "transform:scaleY(0)"), (L, "transform:scaleY(0)")], "linear", origin="50% 0%")
    flip = m.loop([(0, "transform:rotate(0deg)"), (9.0, "transform:rotate(0deg)"),
                   (9.7, "transform:rotate(180deg);animation-timing-function:cubic-bezier(.34,1.56,.64,1)"),
                   (17.3, "transform:rotate(180deg)"), (17.4, "transform:rotate(0deg)"), (L, "transform:rotate(0deg)")], "settle", origin="50% 50%")
    fade = m.loop([(0, "opacity:1"), (17.0, "opacity:1"), (17.3, "opacity:0"), (17.7, "opacity:0"), (L - .2, "opacity:1"), (L, "opacity:1")], "settle")
    body = (f'<g style="{flip}"><path d="{topb}" fill="{glass}" opacity=".55"/><g clip-path="url(#c-hg)">'
            f'<rect x="{-wd / 2}" y="{-hh}" width="{wd}" height="{hh}" fill="{sand}" style="{b_fill}"/>'
            f'<rect x="{-wd / 2}" y="0" width="{wd}" height="{hh}" fill="{sand}" style="{a_fill}"/></g>'
            f'<path d="{topb}" fill="none" stroke="{frame}" stroke-width="2.4"/>'
            f'<rect x="{-wd / 2 - 6}" y="{-hh - 8}" width="{wd + 12}" height="9" rx="3" fill="{frame}"/>'
            f'<rect x="{-wd / 2 - 6}" y="{hh - 1}" width="{wd + 12}" height="9" rx="3" fill="{frame}"/></g>')
    return f'<g transform="translate({X:.1f} {Y - hh - 12:.1f})"><g style="{fade}">{body}</g></g>'


def dazed(d, iso, x, y, t_on):
    """Little spinning stars above the fenced-out worker (three small dots, slow)."""
    m, p = d.m, d.pal
    X, Y = iso.p(x, y, 0)
    per = m.L / 6
    spin = m.cycle([(0, "transform:rotate(0deg)"), (per, "transform:rotate(360deg)")], per, "linear", origin="50% 50%", base="transform:rotate(0deg)")
    vis = m.loop([(0, "opacity:0"), (t_on, "opacity:0"), (t_on + .4, "opacity:.9"), (16.0, "opacity:.9"), (16.6, "opacity:0"), (m.L, "opacity:0")])
    dots = "".join(f'<circle cx="{14 * __import__("math").cos(a):.1f}" cy="{5 * __import__("math").sin(a):.1f}" r="2.3" fill="{p["terra"]}"/>'
                   for a in (0, 2.1, 4.2))
    return f'<g transform="translate({X:.1f} {Y - 70:.1f})"><g style="{vis}"><g style="{spin}">{dots}</g></g></g>'


def flying_block(d, iso, ft):
    """The block thrown from the tripping worker's hands: arc, hover (frozen), caught, carried, placed as the next step."""
    m, p = d.m, d.pal
    L = m.L
    y = 2.15
    z0 = .34
    slot4 = 10.4 - 1.15 * 4
    o = .475
    pts = [(0, 7.9, y, 1.2, "opacity:0"), (ft + .2, 7.9, y, 1.2, "opacity:0"),
           (ft + .3, 7.3, y, 1.3, "opacity:1"), (ft + 1.1, 8.3, 1.0, 4.0, "opacity:1", "settle"),
           (10.4, 8.3, 1.0, 3.85, "opacity:1", "settle"), (11.4, 8.3, 1.0, 4.1, "opacity:1", "settle"), (12.6, 8.3, 1.0, 3.9, "opacity:1", "settle"),
           (13.7, 8.3, 1.0, 4.0, "opacity:1", "settle"), (14.2, 8.6, 1.2, 1.6, "opacity:1", "land"),
           (14.9, 7.3, 1.2, 1.6, "opacity:1", "settle"), (15.5, slot4 + o, .3 + o, z0, "opacity:1", "land"),
           (L - 1.1, slot4 + o, .3 + o, z0, "opacity:1"), (L - .5, slot4 + o, .3 + o, z0, "opacity:0"), (L, 7.9, y, 1.2, "opacity:0")]
    from .common import travel
    st, (X, Y) = travel(m, iso, pts)
    blk = f'<g style="{st}"><g transform="translate({X:.1f} {Y:.1f})">{crate_iso(d, iso)}</g></g>'
    glow = m.loop([(0, "opacity:0"), (15.4, "opacity:0"), (15.7, "opacity:.9"), (16.8, "opacity:.9"), (17.2, "opacity:0"), (L, "opacity:0")])
    gx, gy = iso.p(slot4 + .475, .3 + .475, z0 + .4)
    ring = f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="42" ry="30" fill="{p["terra"]}" opacity="0" style="{glow}"/>'
    return ring + blk


def crate_iso(d, iso):
    """Terracotta block drawn around the local origin (its bottom-centre)."""
    from ..iso import Iso
    mini = Iso(d, 0, 0, iso.g)
    return mini.box(-.475, -.475, 0, .95, .95, .8, cols=d.faces("terra"))


def runner(d, iso, lane, wp):
    m, p = d.m, d.pal
    L = m.L
    pts = [(0, 16.2, lane, 0, "opacity:0"), (11.8, 16.2, lane, 0, "opacity:0"), (12.0, 16.0, lane, 0, "opacity:1"),
           (13.15, 9.6, lane, 0, "opacity:1", "linear"), (13.55, 8.9, lane, 1.6, "opacity:1", "settle"),
           (14.2, 8.6, lane, 0, "opacity:1", "land"), (15.4, 6.6, lane, 0, "opacity:1", "linear"),
           (L - 1.1, 6.6, lane, 0, "opacity:1"), (L - .5, 6.6, lane, 0, "opacity:0"), (L, 16.2, lane, 0, "opacity:0")]
    root, (X, Y) = travel(m, iso, pts)
    rp = .45
    run_st = walk(m, rp, amp=40, bob=2.4, arms=40)
    leap = {**pose(-165, -150, 38, -28)}
    carry_pose = {**pose(-78, -70, 0, 0)}
    holdb = f'<g style="{m.windows([(14.2, 15.2)], .1)}">{crate_iso_small(d)}</g>'
    lean = m.loop([(0, "transform:rotate(8deg)"), (13.3, "transform:rotate(8deg)"), (13.6, "transform:rotate(-8deg)"),
                   (14.2, "transform:rotate(0deg)"), (L, "transform:rotate(0deg)")], "settle", origin="50% 100%")
    st_run = {**run_st}
    # run (12.0-13.3), leap (13.3-14.0), then walk (14.3-15.4) and stand
    ch = character(d, X, Y, "terra", 2.2, True, st=st_run, rest=carry_pose | idle(m, L / 6), moving=[(12.0, 13.3), (14.3, 15.4)],
                   root=root, carried=holdb, lean=lean)
    air = character(d, X, Y, "terra", 2.2, True, st=leap, root=root.replace("animation:", "animation:"), carried="", lean=lean,
                    shadow=False)
    air = f'<g style="{m.windows([(13.3, 14.15)], .08)}">{air}</g>'
    return ch + air


def crate_iso_small(d):
    from ..iso import Iso
    mini = Iso(d, 14, -17, 8.5)
    return mini.box(-.5, -.5, 0, 1, 1, .9, cols=d.faces("terra"))


def rewind(d, iso, slot):
    m, p = d.m, d.pal
    L = m.L
    X, Y = iso.p(1.7, -.75, 0)
    spin = m.loop([(0, "transform:rotate(0deg)"), (15.6, "transform:rotate(0deg)"), (16.8, "transform:rotate(-360deg);animation-timing-function:cubic-bezier(.65,0,.35,1)"),
                   (L, "transform:rotate(-360deg)")], "travel", origin="50% 50%")
    wheel = ""
    for k in range(6):
        import math
        a = math.pi * k / 3
        wheel += f'<line x1="0" y1="0" x2="{15 * math.cos(a):.1f}" y2="{15 * math.sin(a):.1f}" stroke="{p["wood"]}" stroke-width="2.4" stroke-linecap="round"/>'
    out = (f'<g transform="translate({X:.1f} {Y:.1f})"><rect x="-2" y="-46" width="4" height="46" fill="{shade(p["wood"], -.2)}"/>'
           f'<g transform="translate(0 -50)"><circle r="18" fill="none" stroke="{p["terra"]}" stroke-width="3"/><g style="{spin}">{wheel}</g></g></g>')
    # ghost path along the tops of the blocks
    x_start, x_end = slot(0) + .5, slot(4) - .2
    pts = " ".join("%.1f,%.1f" % iso.p(x, .3 + .475, 1.25) for x in (x_start, x_end))
    draw = m.loop([(0, "stroke-dashoffset:100;opacity:0"), (15.6, "stroke-dashoffset:100;opacity:0"), (15.7, "stroke-dashoffset:100;opacity:.8"),
                   (16.8, "stroke-dashoffset:0;opacity:.8"), (17.2, "stroke-dashoffset:0;opacity:0"), (L, "stroke-dashoffset:100;opacity:0")], "travel")
    out += (f'<polyline points="{pts}" fill="none" stroke="{p["terra"]}" stroke-width="3" stroke-dasharray="6 7" stroke-linecap="round" '
            f'pathLength="100" style="{draw}"/>')
    return out
