"""Design tokens: day and dusk palettes, grid, timing, easing."""

W = 1280                    # plate width
NARROW = 560                # rendered-width breakpoint (px)
G = 32                      # grid unit (px): one iso step along x is (G, G/2)

EASE = dict(
    settle="cubic-bezier(.22,1,.36,1)",
    travel="cubic-bezier(.65,0,.35,1)",
    land="cubic-bezier(.34,1.56,.64,1)",
    linear="linear",
)
LOOPS = dict(hero=14, chronicle=18, inference=16, raft=18, assistant=16, work=14, activity=12, footer=12, post=8)

PALETTES = {
    "day": dict(
        name="day", bg="#F4EEE3", cream="#F4EEE3", sand="#E6CFA6", sage="#9DB4A0", deep="#6F8E78",
        terra="#D8775A", teal="#24505A", ink="#23201C", sun="#E58B6A",
        cloud="#FBF7EF", water="#BCD2C6", ripple="#8FB0A8", glow="#F2C27A", wood="#B98A5A",
        mount="#B7C7B5", mount2="#9DB4A0", face="#F7E6C9", shade=(.14, 0, -.16), board="#F2E3C4",
        night=0,
    ),
    "dusk": dict(
        name="dusk", bg="#1E2A33", cream="#A8A08C", sand="#8E8068", sage="#4A655B", deep="#35504A",
        terra="#D47A58", teal="#3B7886", ink="#EFE6D4", sun="#E9E2C8",
        cloud="#33444F", water="#2A4350", ripple="#3F6370", glow="#F4B860", wood="#8A6A48",
        mount="#2F4A4C", mount2="#3A5A54", face="#E9D9B8", shade=(.12, -.02, -.22), board="#4A4538",
        night=1,
    ),
}


def _rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


def shade(h, f):
    """f>0 mixes toward white, f<0 toward black."""
    r = _rgb(h)
    t = 255 if f > 0 else 0
    f = abs(f)
    return "#%02X%02X%02X" % tuple(round(c + (t - c) * f) for c in r)


def mix(a, b, f):
    ra, rb = _rgb(a), _rgb(b)
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * f) for x, y in zip(ra, rb))


def lum(h):
    c = [x / 255 for x in _rgb(h)]
    c = [x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4 for x in c]
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2]


def contrast(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + .05) / (lb + .05)
