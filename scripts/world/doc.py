"""SVG document shared by every plate."""
from xml.sax.saxutils import escape as esc

from .motion import Motion
from .tokens import NARROW, PALETTES, W, shade
from .typeset import Type


class Doc:
    def __init__(self, prefix, theme, L, h, w=W):
        self.p, self.theme, self.pal, self.L, self.w, self.h = prefix, theme, PALETTES[theme], L, w, h
        self.t = Type(prefix)
        self.m = Motion(L, prefix)
        self.defs, self._ids = [], set()
        self.n = 0

    # -- palette ---------------------------------------------------------------
    def c(self, role):
        return self.pal[role]

    def faces(self, role_or_hex):
        """(top, left, right) face colours, light from the top-left."""
        base = self.pal.get(role_or_hex, role_or_hex)
        a, b, c = self.pal["shade"]
        return shade(base, a), shade(base, b), shade(base, c)

    def uid(self, name):
        self.n += 1
        return f"{self.p}-{name}{self.n}"

    def add_def(self, key, markup):
        if key not in self._ids:
            self._ids.add(key)
            self.defs.append(markup)

    def render(self, body, title, desc, extra_css="", transparent=False):
        css = (".n,.rm{display:none}"
               f"@media (max-width:{NARROW}px){{.w,.deco{{display:none}}.n{{display:inline}}}}"
               + self.m.css() + extra_css +
               "@media (prefers-reduced-motion:reduce){*{animation:none!important}.sm{display:none}.rm{display:inline}}")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" '
                f'height="{self.h}" role="img" aria-labelledby="{self.p}-t {self.p}-d">'
                f'<title id="{self.p}-t">{esc(title)}</title><desc id="{self.p}-d">{esc(desc)}</desc>'
                f'<defs>{"".join(self.defs)}{self.t.defs()}</defs><style>{css}</style>'
                f'{"" if transparent else f"<rect width={chr(34)}{self.w}{chr(34)} height={chr(34)}{self.h}{chr(34)} fill={chr(34)}{self.pal[chr(98)+chr(103)]}{chr(34)}/>"}{body}</svg>')


def r1(v):
    return f"{v:.1f}"
