# Research and decisions: the isometric world

## What to take from each reference
**Monument Valley.** A single light direction, three flat tones per solid, calm geometry and generous negative space.
Take: top / left / right faces at fixed lightness steps, no outlines, no blur, stairs and arches as the connective tissue
between objects, tiny figures against big quiet shapes.

**Alto's Odyssey.** Layered silhouettes, a palette that shifts with the time of day while the shapes stay the same, slow
ambient motion (clouds, birds) behind a simple foreground action. Take: the same geometry rendered as "day" and "dusk",
a sun that becomes a moon, drift on the sky layer only.

**Kurzgesagt.** Explanation first: a small cast, one idea per scene, labels that appear at the beat they refer to, rounded
forms and a restrained accent colour. Take: numbered signposts that light at the moment their step happens, terracotta
reserved for the thing that matters (the active block, the crown, the rescuer).

**Studio Ghibli background art.** Warmth in the neutrals (cream, sand, sage, never pure white or black), small acts of life
in every corner (flags, lanterns, birds), timing with anticipation and settle. Take: ambient loops that never stop but never
compete, characters with a visible reaction (the tripper sits up dazed, the rescuer overshoots her landing).

## Decisions that follow
- One grid unit, true 2:1 isometric projection, one `iso(x, y, z)` helper; every house, step and character uses it.
- No gradients and no blur filters: depth comes from three face colours and flat contact-shadow ellipses.
- The character is built from separately pivoting parts so one rig serves walking, carrying, running, tripping and catching.
- Each project plate is a seamless loop on one clock; the key frame sits inside the hold.
- Explanation lives twice: short numbered signposts inside the art, and the same steps as markdown under it.

## Fonts (SIL Open Font License 1.1)
| Use | Font | Source | Licence file |
|---|---|---|---|
| All in-scene lettering (display, spaced labels, signs) | Outfit SemiBold; Outfit Medium for body text | github.com/Outfitio/Outfit-Fonts via google/fonts | `scripts/fonts/OFL-Outfit.txt` |

Both weights are instanced from the variable font and subset to Latin. All lettering is converted to `<path>` outlines at
build time (each glyph defined once per SVG and reused with `<use>`, kerning from the font's GPOS table).

## Palette
Day: cream `#F4EEE3`, sand `#E6CFA6`, sage `#9DB4A0`, deep sage `#6F8E78`, terracotta `#D8775A`, deep teal `#24505A`,
ink `#23201C`, sun `#E58B6A`. Dusk: background `#1E2A33`, the same hues pulled toward muted sage-grey and warm stone,
lantern glow `#F4B860`, a moon in place of the sun. Text contrast is checked by `scripts/validate.py`
(lowest: ink on the dusk sign board, 7.7:1).

## GitHub constraints that shaped the build
- Everything moves inside self-hosted SVG referenced by `<img>`; each plate is its own file so text can sit between them.
- There is no scroll trigger, so every plate loops; only the hero has a short one-time intro.
- An `<img>` inside `<a><picture>` is pulled out of its link by GitHub, so linked images use the
  `#gh-dark-mode-only` / `#gh-light-mode-only` pair (checked in the rendered HTML).
- `@media (max-width: 560px)` inside each SVG responds to the rendered width: wide in-scene labels are hidden and large
  numbered badges, names and status plaques replace them.
