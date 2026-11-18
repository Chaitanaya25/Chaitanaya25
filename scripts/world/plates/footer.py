"""P8 footer: the lighthouse shore. 12 s loop."""
from ..doc import Doc
from ..iso import Iso
from ..props import bird, bush, cloud, ripples, sun, tree
from ..rig import character, idle, pose
from ..tokens import LOOPS, shade

H = 520


def build(theme):
    L = LOOPS["footer"]
    d = Doc("f", theme, L, H)
    m, t, p = d.m, d.t, d.pal
    out = sun(d, 930, 190, 62)
    out += cloud(d, 520, 80, .9, 50, 2) + cloud(d, 1130, 120, .8, 40, 7) + cloud(d, 240, 150, .7, 60, 11)
    out += bird(d, -120, 1400, 120, 1, 1.0) + bird(d, -120, 1400, 190, 7, .9)
    # sea
    out += f'<rect x="0" y="330" width="1280" height="190" fill="{p["water"]}"/>'
    out += ripples(d, 420, 372, 4, 90, 0) + ripples(d, 820, 392, 4, 100, 1)
    # waves lapping at the cliff
    wv = m.cycle([(0, "transform:translateX(-10px)"), (1.5, "transform:translateX(10px)"), (3.0, "transform:translateX(-10px)")], 3.0,
                 base="transform:translateX(-10px)")
    out += (f'<path d="M220,350 q40,-14 80,0 t80,0 t80,0 t80,0" fill="none" stroke="{p["cloud"]}" stroke-width="5" stroke-linecap="round" style="{wv}"/>'
            f'<path d="M80,382 q40,-12 80,0 t80,0 t80,0" fill="none" stroke="{p["cloud"]}" stroke-width="4" stroke-linecap="round" opacity=".8" style="{wv}"/>')
    # distant mountains
    out += (f'<polygon points="620,336 780,250 900,320 1010,270 1180,336" fill="{p["mount"]}"/>'
            f'<polygon points="780,250 900,320 840,336 760,336" fill="{shade(p["mount"], -.08)}"/>')
    # cliff + lighthouse
    iso = Iso(d, 200, 250, 40)
    out += iso.island(-1.2, -2.6, 5.4, 3.6, "cream", layers=4, side="sage")
    out += tree(d, 90, 355, 1.2) + bush(d, 300, 330, 1.0)
    lx, ly = iso.p(.6, -.7, 0)
    out += (f'<g transform="translate({lx:.1f} {ly:.1f})"><ellipse cx="0" cy="3" rx="42" ry="12" fill="{p["ink"]}" opacity=".16"/>'
            f'<path d="M-36,0 L-20,-20 H20 L36,0Z" fill="{p["deep"]}"/>'
            f'<path d="M-18,-18 L-11,-170 H11 L18,-18Z" fill="{p["sand"]}"/>'
            f'<path d="M-18,-18 L-11,-170 H-3 L-4,-18Z" fill="{shade(p["cream"] if not p["night"] else p["sand"], .1)}" opacity=".6"/>'
            f'<rect x="-15" y="-96" width="30" height="16" fill="{p["terra"]}"/><rect x="-13" y="-140" width="26" height="14" fill="{p["terra"]}"/>'
            f'<rect x="-15" y="-176" width="30" height="10" rx="3" fill="{p["terra"]}"/>'
            f'<rect x="-9" y="-208" width="18" height="32" rx="3" fill="{p["glow"]}" style="{m.cycle([(0, "opacity:.85"), (1.5, "opacity:1"), (3, "opacity:.85")], 3.0, base="opacity:.95")}"/>'
            f'<path d="M-14,-208 L0,-228 L14,-208Z" fill="{p["terra"]}"/></g>')
    # a tiny figure on the cliff edge, reading a book
    fx, fy = iso.p(2.6, .6, 0)
    st = {**idle(m, L / 2), **pose(-60, -55, 0, 0)}
    out += character(d, fx, fy, "teal", 2.2, False, st=st, scarf=True)
    out += (f'<g transform="translate({fx + 21:.1f} {fy - 68:.1f}) rotate(-14) scale(1.3)"><path d="M0,0 L-12,3 V16 L0,13Z" fill="{p["cloud"]}" stroke="{p["terra"]}" stroke-width="1.6" stroke-linejoin="round"/>'
            f'<path d="M0,0 L12,3 V16 L0,13Z" fill="{shade(p["cloud"], -.06)}" stroke="{p["terra"]}" stroke-width="1.6" stroke-linejoin="round"/></g>')
    # the line
    out += f'<rect class="w" x="290" y="430" width="700" height="60" rx="30" fill="{p["board"]}" stroke="{p["wood"]}" stroke-width="2"/>'
    out += t.text("Backend systems  ·  AI infrastructure  ·  ML", 640, 470, 30, "body", p["ink"], 0, "middle", attrs='class="w"')
    out += t.text("Backend · AI infrastructure · ML", 640, 470, 44, "body", p["ink"], 0, "middle", attrs='class="n"')
    return d.render(out, "The lighthouse shore", "A lighthouse on a cliff, small waves, a sun by day and a moon at dusk. A tiny hooded figure sits on the cliff "
                    "edge reading a book. Text: Backend systems, AI infrastructure, ML.")
