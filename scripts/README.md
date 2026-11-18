# Asset generator

All SVGs in `/assets` come from one deterministic generator (`scripts/world`).

```bash
pip install fonttools playwright pillow     # playwright and pillow only for the review scripts
python scripts/build_assets.py              # every plate and signpost, day and dusk
python scripts/build_assets.py activity     # contribution plates from the GitHub API (GITHUB_TOKEN, or a logged-in gh CLI)
python scripts/validate.py --rebuild        # XML, refs, sizes, contrast, links, numbers, determinism
```

Review tools:

```bash
python scripts/render_check.py OUT assets/raft-day.svg --t 2,6,13.5 --width 400 [--browser firefox] [--reduced]
python scripts/render_page.py CSS_DIR OUT   # README through `gh api markdown`, three widths, both themes
```

| Module | Role |
|---|---|
| `world/tokens.py` | palettes (day, dusk), grid unit, loop lengths, easing, shade and contrast helpers |
| `world/iso.py` | 2:1 projection, prisms, slabs, stairs, round islands, face and floor matrices |
| `world/typeset.py` | outlined lettering from `scripts/fonts` (Outfit, OFL) |
| `world/rig.py` | the hooded character: parts with pivots, walk / carry / idle / pose cycles |
| `world/props.py` | clouds, birds, trees, houses, towers, flag (SMIL morph), lanterns, sun or moon |
| `world/signs.py` | numbered signposts, engraved names, status plaques |
| `world/motion.py` | keyframe builder on one loop length; the base style is the reduced-motion key frame |
| `world/doc.py` | SVG document, narrow-width rules, reduced-motion rule |
| `world/plates/*.py` | one module per plate |
| `world/contributions.py` | GraphQL fetch with sanity checks |
