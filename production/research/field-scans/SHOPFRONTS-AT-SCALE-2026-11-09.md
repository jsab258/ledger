# Shop fronts at scale: field scan, 9 November 2026

For phase 2 (about ten fronts, the fishmonger, the empty unit). All pages read 9 Nov 2026. Thin scan: the primary GDC material was not reachable (see the end), so most of the field is unverified.

## Our own baseline (read 9 Nov)

- Phase 1 front cost: Rita's pilot 10.5 h; latest (launderette) 3.58 h, ratio 0.34 of the pilot; against the first of six counted (ironmonger, 4.0 h) it is 0.90. Medium and low confidence (production/research/phase2-plan/SCOREBOARD-2026-11-08.md, table 1).
- Fishmonger plus empty unit, estimate only: 16 to 37 h for both (same file, section 3, from PD line 10).
- Method as proven: a front is kit joinery on the street's datum, with its own glass, signs, painted rows, baked wear, and a room picture behind glass (.claude/skills/shopfront/SKILL.md). Its room behind glass is already one projected picture per state; its near metre is real meshes (§3).

## What the sources say

**1. Shape grammar in Unreal's PCG (Epic, UE 5.8 docs).** A grammar string places modules along a spline or segment: `*` repeats to fill, `{A:2,B:1}` weighted random choice, `<A,B,C>` priority fallback, `[A,P]` groups, "Scalable" modules stretch to absorb leftover width. The page's example is a fence; it does not cover facades (facade use is an extrapolation). Limits stated: a grammar must fit its space, tight corners may be wrong, one cross-section node needs a Beta plugin off by default (mesh cap 2048 vertices by default). No production-ready statement and no cost figures anywhere in Epic's PCG overview. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-shape-grammar-with-pcg-in-unreal-engine and https://dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-framework-in-unreal-engine
Relevance: the grammar suits repeating bays (pilaster, window, door) along the 6 m parade. Phase 1's fronts are one-off joinery with measured sizes, so only the kit's reuse across bays is reached.

**2. Interior mapping (van Dongen's own write-up, 25 Sep 2018; method 2007, paper 2008).** One ray against three of six room planes per pixel, no extra geometry; "only a few steps and eats little performance", but no benchmark numbers given. Furniture needs extra texture layers at "additional performance cost". Rooms are flat squares; faults such as a door where a window should be. No licence stated; author says he would be honoured if used. He notes Unreal 4 shipped an InteriorCubeMap function; Epic's page for it showed no text, unverified. https://gamedeveloper.com/programming/interior-mapping-rendering-real-rooms-without-geometry
Whether Spider-Man used it: author has no official statement (same page).

**3. Interior mapping in other engines.** Gaijin's Dagor documentation: cubemap per room, tiling with random rotation, fade-out by distance, night self-illumination controls; limits: one material cannot suit windows of different proportions, identical geometry maps identically unless shifted, tiling seams visible. No licence stated (copyright notice only) so not usable as code. https://gaijinentertainment.github.io/DagorEngine/assets/shaders/rendinst_interior_mapping.html
Houdini Karma Room Map: cross-shaped map, up to four slices for furniture or curtains, per-window map variation by room ID; needs night maps, not only more emission. Proprietary SideFX software. https://www.sidefx.com/docs/houdini/solaris/support/karma_room_map.html

**4. Cost of interior mapping against real rooms.** No source read gives a measured frame cost or a comparison. Only the qualitative claim above. Unverified.

## Not confirmed

- Modular kits and trim sheets, vertex paint, per-instance data, decals for signage: no primary source was read for these; the in-house skill's own findings stand (Mafia's trim sheet at 26% of kit slots, from MAFIA-KIT as cited in the skill, not re-read).
- Houdini building tools in shipped games: no readable source.
- Licences: Epic docs and PCG are engine features under the engine licence (not checked on this scan). No fetched asset or code.

## Could not be reached

- GDC Vault, Spider-Man technical postmortem talk (slides members-only, login limit page) https://www.gdcvault.com/play/1026496
- 80.lv postmortem write-up: read, holds only the talk's description, nothing on buildings.
- Automaton article on Spider-Man windows: only the headline arrived.
- Epic pages on PCG overview, modular building and trim sheets, interior cube map function: headings only (script-rendered); the two PCG pages above did load.
- Spider-Man 2 procedural content talk (GDC 2024): abstract only, search result; not read.

## Recommendation

Keep the phase 1 method for each front's joinery and room picture (measured, with a falling cost), and run one bounded trial of PCG shape grammar for repeating bay modules plus per-front variation of paint row, sign and room picture, on one front. If the trial front costs under the phase 1 launderette's 3.58 h, use it for the remaining fronts; if not, record the result and stay with phase 1's method. Interior mapping is not recommended yet: the room picture already exists in the method and no cost against real rooms is confirmed. Next scan needed on trim sheets, decals and per-instance variation, with sources that load.
