# Terrace fronts: the bay, its alterations and its wear. Station 1 of five.

STATUS: SPEC. Written 2026-09-21. Governed by `canon.md`, which outranks this
file and every other document named below; `ledger-v2/respec/decision-register/D14-authored-interiors.md`
(authored breadth, not generated breadth); `ledger-v2/respec/decision-register/D53-grime-is-the-strategy-and-a-surface-carries-wear-above-a-floor.md`
(the wear rule); `ledger-v2/respec/decision-register/D13-street-layout-method.md`
(read; this spec lays nothing out, it authors fronts onto a street D13's own
process already laid out); `production/specs/asset-interface.md` (the mesh
contract any authored GLB must fit); and
`game-design/decision-2026-09-21-ruling-the-terrace-fronts-are-authored-and-everything-else-comes-from-what-we-hold.md`
(Jafar's order that commissions this file).

This is the SPEC station only. NO GEOMETRY, NO BLENDER RECIPE, NO .blend, NO
GLB is authored here. AUTHOR is a separate, later station, currently blocked
on queue 403, and this document does not depend on queue 403 landing to be
correct: SPEC legitimately precedes AUTHOR in the five-station shape
(`ledger-v2/studio-v2/pipelines.md`: "1 SPEC (what, canon constraints,
acceptance checks) -> 2 AUTHOR -> 3 VERIFY -> 4 INTEGRATE -> 5 RECORD").

## 0. Provenance key, read before anything below

Every number in this file carries one of four tags, because a plausible
number with no provenance is what rule 1 and rule 2 exist to stop.

- **MEASURED**: copied from a value already committed to a file in this
  repository, with the exact file and key named at the point of use. Nothing
  MEASURED was recalled; every one was read again in this session (dated
  2026-09-21) with `git show` or `python3 -c "import json..."` over the file
  named.
- **DERIVED**: arithmetic performed in this file on MEASURED numbers, shown
  at the point of use so it can be checked by re-doing the sum.
- **CHOSEN**: a new authored design decision made BY THIS SPEC. Marked
  explicitly as mine, the way `vignette-scene.json`'s own `dimension_provenance`
  block marks its own `judgement` class of number.
- **PRECEDENT**: an existing convention or pattern this spec reuses rather
  than invents (a naming scheme, a route class, a material split already
  decided for a sibling package).

Two files anchor everything MEASURED below and both were read this session:
`production/specs/vignette-scene.json` (the design-parameter source, written
2026-09-02, on `main`) and `production/specs/vignette-pieces.json` (the
610-piece emitted list generated from it, also on `main`). A third,
`production/art/atlas-01/data/atlas.json` on `origin/art/atlas-01`
(`base_commit` `7722b45cb3dcee2fbcee26675fae4fef641cbba7`), supplies the
`street_anchor` datum named in the commission brief. All three were read
directly in this session, not recalled from the brief's summary of them.

## 1. The datum, verified

The brief's `street_anchor` object, re-read from
`git show origin/art/atlas-01:production/art/atlas-01/data/atlas.json`, key
`street_anchor`, matches the brief exactly: `length_m` 42, `carriageway_m` 6,
`footway_each_m` 2, `frontage_z_m` 5.125, `mickeys_piece` `east_parade_bay0`,
`mickeys_x_range` [3, 9], `mickeys_z_range` [5.125, 13.125], `yard_gap_x` [21,
24], `source` `production/specs/vignette-scene.json`, `pieces`
`production/specs/vignette-pieces.json`. Its `note` is load-bearing and
repeated here because it governs every district reference below: "east_parade
is a retained piece ID, not a district assignment; this street is in the
Hook."

Both files it names were opened directly (not trusted from the atlas copy)
and CROSS-CHECK exactly: `vignette-scene.json`'s `street.length_m` is 42.0,
`street.carriageway.half_width_m` is 3.0 (so `carriageway_m` 6 checks), and
the piece list's own `east_parade_bay0` box sits at `x_m` 6, `sx_m` 6 (spanning
3 to 9, matching `mickeys_x_range` exactly) and at `z_m` 9.125 with `sz_m` 8
(depth), whose face sits on `frontage_z_m` 5.125 (9.125 minus half of 8 equals
5.125). The datum is good; nothing in it needed correcting.

**What this datum does not cover, found by reading further than the brief
pointed.** `vignette-scene.json` carries three design-parameter blocks the
brief's `street_anchor` summary does not mention at all, and they are the
real content of "the bay as a unit": the `shopfront` key (stallriser,
pilaster, fascia, transom, door dimensions), the `roofline` key (chimney,
aerial, gutter, downpipe dimensions) and the `street.blocks` array (per-row
storey heights, wall material, roof form). Section 3 below is built from
these three, MEASURED, not from the smaller `street_anchor` object alone.

## 2. Canon and period, checked directly against canon.md this session

1988 to 1992. Landlines, paper, cash. No mobiles, no computer network of any
kind, no wheeled refuse bins on this street (the built BOM already excludes
them; nothing in this spec adds one). CCTV is rare and sited only where canon
names it; a terrace front carries none. No real brand, shop chain or product
appears anywhere below; every trade name is either already minted (Mickey's)
or a generic trade category (fish shop, chandler, barber) in the same register
`canon.md`'s own brand list and `production/art/atlas-01/PRODUCTION-CATALOGUE.md`
already use. D18 (tobacco stays, alcohol and gambling out entirely, no
children anywhere) was re-read in full this session and produced two
corrections to the source material this spec draws on, both made here and
both flagged rather than silently carried:

**Correction 1, Mickey's.** `production/art/atlas-01/data/pub-operations.json`
(written before D19) still describes `east_parade_bay0` as "drinks-led pub /
private household above". D19 (2026-09-14) supersedes this: Mickey's is a
minicab office, and D17's clause that survives is narrower than the old file
assumed, "the siting, the two bays and the fascia STAND. They are
architecture and they do not depend on what is served." This spec treats
bay0's ARCHITECTURE (two doors, the fascia, the carcass) as already fully
authored and unchanged, and its USE as "minicab office" per D19, not "pub".
Nothing about `MICKEYS.md`'s own text is edited by this spec (it sits on a
different branch, out of scope here); this correction applies only to how
THIS document describes bay0, and is named so the stale wording in that file
is not mistaken for current.

**Correction 2, the bay named "Bookmaker".**
`production/art/atlas-01/previews/hook-uses.svg` (an unapproved ART PROPOSAL,
`production/art/atlas-01/TOWN-FORM-BIBLE.md` status line) names
`west_north_bay1` "Bookmaker", and `pub-operations.json` adds "counter and
paper race sheets". D17, re-read in full this session: "Alcohol is never
shown, served, drunk or spoken of, and gambling likewise, anywhere, in image
or speech. PUBS MAY EXIST AS PLACES." That carve-out is written for pubs by
name and is not extended to betting shops anywhere in D17 or D18; a bookmaker's
trade IS the depiction of gambling in a way a pub building is not the
depiction of drinking. THIS SPEC RENAMES THAT BAY'S TRADE. Section 5 gives the
replacement and why. This is a document-content correction under CLAUDE.md's
own rule ("violating it in content is a gate failure... In a document a
violation is corrected on sight, by hand"), made here because this spec is
the first place that bay's trade is used downstream of D17/D18; the upstream
`hook-uses.svg` itself is not edited by this spec (out of scope, different
branch), and its stale label is named so it is not copied again.

D14 (authored breadth) governs the METHOD of everything below: every bay's
use, alteration and wear direction in section 5 is a DESIGNED choice, not a
rule a generator could invent from a seed. A script that later assembles this
spec's numbers into a Blender recipe is in scope exactly as `mickeys_blockout.py`
and `make_fascia_mouldings.py` are; nothing here describes a grammar that
invents a bay.

## 3. The bay as the unit

Two row types exist on this street today, MEASURED from `vignette-scene.json`
`street.blocks[0]` (`east_parade`) and `blocks[1]`/`blocks[2]` (`west_south`,
`west_north`). All heights below are given in LOCAL coordinates, where 0 is
the bay's own threshold (the shop or house doorstep), PRECEDENT from
`production/art/atlas-01/RECIPE-REPAIR.md`'s own convention for Mickey's:
its upper carcass is stated there as 6.20 m high in local coordinates and
6.30 m at the source datum, i.e. author local, let integration add the
street datum. The conversion is MEASURED and constant across every piece
checked (carcass, stallriser, side door, sills): **street absolute y =
local y + 0.100 m**, the built street's own footway-above-crown offset at
the frontage line.

### 3.1 Shared by both rows (MEASURED, `street.blocks[*]`)

| Quantity | Value | Tag |
|---|---|---|
| Bay width | 6.000 m | MEASURED, `bay_width_m`, both rows |
| Bay depth (carcass) | 8.000 m | MEASURED, `depth_m`, both rows |
| Ground floor height (threshold to first-floor slab) | 3.400 m | MEASURED, `storey_heights_m[0]` |
| First floor height (slab to ceiling) | 2.800 m | MEASURED, `storey_heights_m[1]` |
| Eaves line (wall top before any roof form) | local 6.200 m (abs 6.300 m) | DERIVED, 3.400 + 2.800, matches the carcass box `sy_m` 6.2 exactly |
| Upper sash window | 0.850 m wide x 1.500 m tall, 2 per bay | MEASURED, `facade.window_width_m`/`window_height_m`/`windows_per_bay` |
| Upper window reveal depth | 0.1025 m | MEASURED `facade.reveal_depth_m`, DERIVED note in the source file itself: half a British brick, 215/2 |
| Upper window positions | bay_start + 1.5 m and bay_start + 4.5 m (centre) | MEASURED, read off `east_parade_up0_w0`/`w1` and confirmed identical on `west_south_up0_w0`/`w1` |
| Sill | 0.950 m wide (window + 0.05 m each side), 0.075 m thick, 0.05 m projection | MEASURED `facade.sill_*` |
| Lintel | 0.950 m wide, 0.150 m thick | MEASURED `facade.lintel_thickness_m` |
| Downpipe | 0.068 m dia., at every INTERNAL party wall (bay boundary), never at a row's outer end | MEASURED `roofline.downpipe`, positions confirmed by direct count: 5 on east (x=9,15,21,27,33), 2 on each 3-bay west run (x=9,15 / x=30,36) |
| Chimney stack, where present | 0.9 x 0.45 m plan, at party walls | MEASURED `roofline.chimney`. On the CURRENT street this exists only on `east_parade` (5 stacks, one per internal party wall); neither west row carries one yet. Read, not invented; see section 10. |
| TV aerial | 10-element UHF comb, mast 1.5 m, on 2 of the 5 east stacks (x=9, x=21) | MEASURED `roofline.aerial`, DERIVED element length in the source file (half-wave dipole at 550 MHz mid-band, 0.2725 m) |

### 3.2 The shopfront row (`east_parade`, brick_red, pitched roof)

Roof: 35 deg pitch, ridge parallel to the street, 0.3 m eaves overhang.
Ridge height above eaves: DERIVED, depth/2 x tan(35) = 4.0 x 0.7002 = 2.80 m,
so the ridge stands at local 9.00 m (abs 9.10). Chimney tops sit 1.0 m above
the ridge (MEASURED `roofline.chimney.height_above_ridge_m`), abs 10.10,
which matches the emitted `east_parade_stack1` top (6.30 + 3.80083 = 10.10083)
to the fourth decimal.

Ground floor is a British shopfront in four parts, MEASURED from
`shopfront` (all local, +0.100 to get absolute):

| Part | Value | Tag |
|---|---|---|
| Pilasters (piers) | 0.35 m wide, 0.1 m projection, full ground-floor height, at EVERY bay edge | MEASURED `shopfront.pilaster_width_m`/`pilaster_projection_m` |
| Stallriser | 0.6 m tall (0 to 0.6 local), 0.15 m projection | MEASURED `shopfront.stallriser_height_m` |
| Display glazing | 0.6 to 2.4 local (1.8 m), 0.12 m recess | MEASURED `shopfront.glazing_recess_m`, DERIVED span from transom_height 2.4 |
| Transom bar | 2.4 to 2.48 local, 0.08 m thick | MEASURED `shopfront.transom_height_m`/`transom_thickness_m` |
| Toplight | 2.48 to roughly 2.82 local | DERIVED, glazing continues to the fascia line less its own frame allowance |
| Fascia band | 2.85 to 3.40 local (0.55 m), 0.12 m projection | MEASURED `shopfront.fascia_bottom_m`/`fascia_projection_m`, and 3.40 local IS the first-floor slab, so the band's top is fixed by the storey height, not chosen independently |
| Shop door | 0.9 m wide, leaf to 0.9 m (using shop-door height convention), glazed upper light from 1.0 to 2.04 local, brick spandrel 2.04 to 2.85 | MEASURED `shopfront.shop_door` |
| Side (household) door | 0.838 x 1.981 m (the standard British external door, 2 ft 9 in x 6 ft 6 in), spandrel above to 2.85, letterplate 0.25 x 0.04 m at 1.0 m | MEASURED `shopfront.side_door` |
| Opening zone between piers | 5.300 m (6.0 minus two piers) | DERIVED, and it EXACTLY equals the display glazing run (3.562 m) plus the shop door (0.9 m) plus the side door (0.838 m): 3.562 + 0.9 + 0.838 = 5.300 |

Already authored and NOT respecified here: the cornice and console brackets
above the fascia band. `production/art/fascia-01/01-SPEC-fascia-package.md`
(BOM `C15_fascia_cornice_console`, STATUS SPEC/AUTHOR/VERIFY done,
INTEGRATE prepared) already fixes `fascia_cornice_01` at 5.892 x 0.150 x
0.215 m and `fascia_console_01` at 0.240 x 0.550 x 0.180 m, both `wood`,
already committed at `ledger/Assets/Props/base-mesh/`. This spec's carcass,
shopfront assembly, doors, sills and windows sit UNDER that existing
moulding and must not move it; section 9 states this as an acceptance check.

### 3.3 The plain row (`west_south`, `west_north`, brick_grey, parapet roof)

Roof: flat parapet, 0.9 m tall, 0.215 m thick (DERIVED note in the source
file: one British brick on its length, 215 mm), coping 0.3 m wide x 0.075 m
thick. Parapet top: local 6.2 + 0.9 = 7.1 m (abs 7.2), coping adds 0.075 m
on top of that.

**The plain row carries no pilasters, no stallriser, no fascia and no
transom.** This was checked directly, not assumed: the full piece list for
`west_south` region `x06_12` (bay0) was read and contains `C13_sills_lintels`,
`C9_door_side`, `D5_downpipe` and `D8_upper_windows` only. No
`C5_shopfront_assembly` piece exists on either west row today. This is a
genuine, MEASURED difference between the rows, not an omission this spec is
filling in: a domestic terrace elevation is a continuous coursed-brick plane
broken only by openings, and a commercial parade earns its piers because a
shopfront needs them. Ground floor openings on the plain row, MEASURED:

| Part | Value | Tag |
|---|---|---|
| Side (household) door | 0.838 x 1.981 m, at bay_start + 1.5 m (centre), spandrel above to local 3.1 | MEASURED, identical box to the shopfront row's side door |
| Ground-floor windows | two per bay, 0.85 x 1.5 m, at bay_start + 3.3 m and bay_start + 5.1 m | MEASURED, `west_south_gf0_w0`/`w1`, sill 1.525 to 1.6 local, head to 3.1 local |
| First-floor windows | identical rhythm to the shopfront row: bay_start + 1.5 m and + 4.5 m | MEASURED |

The ground floor's plain wall runs from the door/window head line (local 3.1)
up to the slab (local 3.4), a 0.3 m band of coursed brick with no fascia,
which is the row's own fixed signature and is why nothing painted or lettered
belongs above a plain-row door: there is no board to letter.

## 4. What varies per bay, and what is fixed for the row

**The reason this section exists rather than "let the recipe repeat the
formula": it was MEASURED, not assumed, that the current street repeats one
formula with zero per-bay variation.** Every shop door on `east_parade` sits
at exactly bay_start + 1.638 m and every side door at exactly bay_start +
0.769 m, checked across bay0, bay1 and bay2 (`east_parade_shopdoor0/1/2` at
x 4.638/10.638/16.638; `sidedoor0/1` at x 3.769/9.769). Every plain-row door
sits at exactly bay_start + 1.5 m, checked across `west_south_door0/1/2` and
`west_north_door0`. That is the flaw D28 Amendment A1 named ("a corridor of
blank walls") one level down: even where geometry exists, it is one stencil
repeated, and a repeated stencil is what reads as generated rather than
authored at close range. This section is the fix.

**FIXED FOR THE ROW** (the rhythm that makes six bays read as one terrace
built at one time, and that a recipe must NOT vary bay to bay):

- Bay width (6.0 m), storey heights (3.4 / 2.8 m), eaves/ridge or
  parapet/coping height.
- Wall material (`brick_red` east, `brick_grey` west) and its coursing.
- The first-floor window rhythm: two 0.85 x 1.5 m sashes at bay_start + 1.5
  and + 4.5, on BOTH rows. This is the single strongest terrace cue there is,
  the string-course a viewer's eye follows down the whole row, and it is why
  no per-bay alteration below touches an upper window's SIZE or its VERTICAL
  line, only what dresses it (section 6).
- On the shopfront row: the fascia head line (local 2.85) and the slab line
  (local 3.4) that bounds it. Every shop's fascia along the row lines up even
  though colour and lettering differ, because it is fixed by the storey
  height, not by the sign-writer.
- Downpipe and, where present, chimney positions: at internal party walls,
  never mid-bay.

**PER BAY** (what a recipe must draw from a per-bay authored value, CHOSEN by
this spec as the parameter set AUTHOR reads):

1. **Door-within-opening offset.** Instead of one constant, each bay picks
   which side of its opening the shop door sits, so neighbouring bays do not
   read as mirrored copies. Section 6 gives each bay's choice.
2. **Presence of the side (household) door.** MEASURED default is "present,
   every bay". CHOSEN: one bay (section 6, bay5) omits it in favour of full
   display glazing, with upper access explained as a rear stair instead. This
   is the one bay this spec asks for a WIDER opening zone than the fixed
   5.3 m, since dropping the side door frees 0.838 m for the display run.
3. **Stallriser finish**, on the CityPack surfaces already held (section 8):
   `concrete` (the row default, MEASURED) or `plaster` (a painted-render
   finish, CHOSEN for wetter trades).
4. **Fascia paint colour**, a tint on the `wood` surface, from a small CHOSEN
   period palette (oxblood, bottle green, deep navy, cream/stone, bare
   soot-darkened timber), never one colour per bay at random: a real parade
   was repainted in waves by whoever owned it, not rainbow-striped.
5. **Upper-window dressing**: net curtain is explicitly OUT OF SCOPE here
   (see section 10, it is a separately tracked, unresolved technique). The
   per-bay choice is between an opaque closed roller blind (an existing decal
   technique), a bare uncurtained pane (implying a vacant or working room),
   or the existing LIT INTERIOR CARD technique (`C11`, already used at bays 0,
   2 and 5, MEASURED `window_practicals.lit_bays` in `vignette-pieces.json`).
6. **One authored alteration**, section 6, never a random one, per the form
   bible's own instruction.
7. **Wear coverage and its placement**, sections 7 and 8: no two bays are
   authored to identical coverage, because a terrace repainted and
   patched over a century does not weather uniformly.

## 5. The twelve bays, authored

Bay identifiers are PRECEDENT, the existing convention in
`vignette-pieces.json` (`east_parade_bay0..5`, `west_south_bay0..2`,
`west_north_bay0..2`); nothing here invents a second naming scheme. Trade
categories are drawn from `production/art/atlas-01/previews/hook-uses.svg`
and `data/pub-operations.json` (both unapproved ART PROPOSALS on
`origin/art/atlas-01`) EXCEPT where a name is already committed as a real
texture asset on `main` (four of the twelve: `production/specs/vignette-pieces.json`
BOM `C6_fascia_lettering`, decals `decal_00_fascia_mickeys` at bay0,
`decal_01_fascia_fish_market` at bay1, `decal_02_fascia_ritas_pawn` at
**bay2**, `decal_03_fascia_steam_laundry` at **bay4**), which is a genuine
disagreement between the two sources, resolved below rather than silently
carried.

**THE CONFLICT, found by checking rather than assuming.** `hook-uses.svg`
puts "Rita's pawnshop" at `west_north_bay0` and a laundry at `west_south_bay2`,
and puts "Quay Stores" (a grocer) at `east_parade_bay2` and "Letting office"
at `east_parade_bay4`. The DECALS ALREADY COMMITTED on `main`, real bytes at
`ledger/Assets/StreamingAssets/Decals/generated/fascia_ritas_pawn.png` and
`fascia_steam_laundry.png`, sit at `east_parade_bay2` and `east_parade_bay4`
instead. THE LANDED ASSET WINS: this spec keeps Rita's Pawn and the Steam
Laundry where the real texture already is, and moves the two DISPLACED trades
(the grocer, the letting office) to the two bays whose identity is otherwise
uncommitted, so all twelve trade categories from the proposal survive and
nothing duplicates.

| Bay | Row | Trade (this spec) | Source | One authored alteration |
|---|---|---|---|---|
| `east_parade_bay0` | shopfront | Mickey's, minicab office | LANDED (`decal_00`); use corrected to D19, section 2 | Already fully authored, `production/art/atlas-01/MICKEYS.md` and `data/mickeys.json`. NOT respecified here. |
| `east_parade_bay1` | shopfront | Fish shop | LANDED (`decal_01_fascia_fish_market`) | A later steel lintel replaces the original over the display bay, visibly straighter and unweathered against the coursed brick either side: the opening was widened once for more cold-cabinet daylight. `C13_sills_lintels` here uses `metal`, not the row's `concrete`, its one material exception (section 8). |
| `east_parade_bay2` | shopfront | Rita's Pawn | LANDED (`decal_02_fascia_ritas_pawn`); trade reassigned here from the atlas proposal's `west_north_bay0` to match the committed decal | A metal lattice grille fixed over the lower half of the display glazing, security dressing for a pawnbroker. CHOSEN as a decal on the glass (PRECEDENT: fascia-01's own reasoning, geometry only where light and shadow physics demand it), not new geometry. |
| `east_parade_bay3` | shopfront | Repair shop | atlas-01 proposal, unconflicted | Already partly authored: `production/art/fascia-01/01-SPEC-fascia-package.md` section 4 records this as the one bay with NO fascia lettering and an awning instead, its right-hand console (x=26.825) "clipped off and never put back... the parade's empty unit". This spec keeps that alteration and does not add a second one on top of it. |
| `east_parade_bay4` | shopfront | Steam Laundry | LANDED (`decal_03_fascia_steam_laundry`) | A vent pipe punched through the fascia band and up past the eaves, cruder than the row's downpipes, venting the laundry's own steam rather than roof water. Uses the row's `metal` surface, no new asset. The wall below it is the row's heaviest-wear bay (section 8): the laundry stains its own frontage, not only the weather. |
| `east_parade_bay5` | shopfront | Quay Stores (grocer) | Reassigned here from the atlas proposal's `east_parade_bay2`, to the one lit, unlettered bay (`window_practicals.lit_bays` includes 5) | Side door OMITTED (section 4, item 2): the whole 5.3 m opening plus the freed 0.838 m is display glazing, upper flat reached from the rear yard instead. The fullest-lit, least-altered bay on the row: a working grocer keeps its frontage clean and bright, the row's CLEANEST wear reading (section 7). |
| `west_south_bay0` | plain | Dock cafe | atlas-01 proposal, unconflicted | Condensation on the ground-floor windows (a `card`-route decal, not new geometry) and a paper menu propped in the window, reusing the existing paper-notice decal technique already on this row (`G6_fly_posters`/`E12_a_board_posters` sit within this bay's frontage today). |
| `west_south_bay1` | plain | Chandler | atlas-01 proposal, unconflicted | The ground-floor window opening ENLARGED past the row's standard 0.85 m into a modest display width, the plain row's own version of a shop conversion (a household window taken out and a wider one put in, without adding a pilaster or a fascia the row does not otherwise carry). A fourth LIT INTERIOR CARD (section 4, item 5), extending the existing three-bay technique. |
| `west_south_bay2` | plain | Sewing rooms | Reassigned here from the atlas proposal's `east_parade_bay5`, since that trade's original bay (`west_south_bay2` in the proposal) is now Steam Laundry's committed home | A hand-lettered card in the window in place of any fascia (the row has none), and a closed roller blind at the first floor: alterations-and-mending trades keep a quiet, curtained upstairs. |
| `west_north_bay0` | plain | Letting office | Reassigned here from the atlas proposal's `east_parade_bay4`, since that trade's original bay (`west_north_bay0` in the proposal) is now Rita's Pawn's committed home | "Recently subdivided" (the original proposal's own phrase, kept): cards-in-window property notices at ground floor, the upstairs room dressed as vacant, no blind, no light card, the row's least lived-in bay. |
| `west_north_bay1` | plain | Wireless and radio rental | RENAMED from "Bookmaker", section 2 correction 2 | A period rental trade (television and radio sets, common across 1988-1992 Britain) rather than a betting shop. Ties visually to the roofline's own TV aerial motif two bays along. Window dressed via the existing card/interior route, no new geometry. |
| `west_north_bay2` | plain | Barber | atlas-01 proposal, unconflicted | A painted sign on the glass itself (a decal on the pane, PRECEDENT: same technique as bay2's security grille) rather than a projecting pole, because the row has no fascia to hang a bracket from and a new projecting-sign asset is out of scope for this spec (section 10). |

## 6. The wear layer (D53)

D53 point 2, quoted exactly rather than paraphrased: wear coverage is "the
fraction of a surface's visible area that carries wear authored as a
separable layer, the wear decals of D28 step 7 (queue 055) and any wear mask
the material carries... A surface whose wear is baked into its albedo and
cannot be separated prints `nothing measured` for this key and is judged by
eye under D41; it does not print zero."

**What this means for a terrace front, stated as a requirement rather than a
number.** Every wear cue on every bay below is a DECAL or a MASK sitting
above the clean base material (`brick_red`, `brick_grey`, `wood`, `concrete`),
never a pre-dirtied texture baked into the base albedo itself. This is
already this street's own convention: `G1_leak_stains` and `G4_moss_damp` are
already separate decal pieces layered on the clean brick (MEASURED,
`decal_14_Leaking005` etc., `surface: multiply`, sitting at the same z as the
wall it dirties), not a second "dirty brick" texture. This spec extends that
existing pattern to cover the whole facade rather than three or four
isolated points.

**D53 point 3: who prints the number, and it is not this file.** `wearCoverage`
is printed at the material station, `tools/ue/make_base_material.py`, per
surface, in the same `key=value` line the existing wetness token already uses
(MEASURED, `materialWetnessParam=... materialWetnessOnMaterial=...`, read
directly in this session near line 1310). This spec does not touch that file
and does not invent its output; it defines what the AUTHORED layer looks like
so that when that print runs over this facade for the first time, the number
it reports is a real reading of designed content, not an arbitrary default.

**THE FLOOR HAS NO NUMBER AND THIS SPEC DOES NOT SET ONE.** D53 point 4: the
floor is set by the director, as amendment A1 to D53, from the series printed
over ACCEPTED surfaces, after this facade is one of them. Nothing below is
that number. What follows are AUTHORED COVERAGE INTENTS, a CHOSEN design
target per element, exactly as every dimension elsewhere in this file is a
chosen number: they exist so the first print has real, uneven content to
report, which is the only way a "minimum" (`wearCoverageMin`, D53 point 2) can
mean anything. A uniform intent across all twelve bays would hand A1 a series
of one value repeated, which is the same failure as section 4's repeated door
offset one layer up.

Coverage intent, by zone, as a fraction of THAT ZONE's own area (not the
whole facade), banded rather than pinned to a false-precision decimal:

| Band | Fraction of the zone | Where it applies this session |
|---|---|---|
| CLEAN | 0.00 to 0.05 | `east_parade_bay5` (Quay Stores), the row's brightest, most-tended frontage |
| LIGHT | 0.10 to 0.15 | Upper-storey brick generally, both rows, general soot and rain soiling |
| MODERATE | 0.25 to 0.40 | Stallriser and plinth band on most shopfront bays; ground-floor plain wall generally |
| HEAVY | 0.50 to 0.70 | `east_parade_bay1` (Fish shop) stallriser and threshold; `east_parade_bay4` (Steam Laundry) wall below its vent pipe; brick immediately around every chimney breast |

`wearCoverageMin` for this batch, when it is first printed, should therefore
name the CLEAN bay's zone, not a bug: D53 point 2 calls this out explicitly
("the surface at the minimum named because a median cannot see the one clean
wall"), and bay5 is authored to be that wall on purpose.

**Wear is not always darker.** One cue is the opposite of a dirt decal: a
lighter, smoothed patch in the stallriser or threshold paint where boots and
trolleys have worn the surface back to bare material, at the shop-door-adjacent
stretch of every shopfront bay's stallriser. This is a MASK on the same
separable layer (it modulates roughness and albedo toward the CLEAN end
locally), not a second system, and it is named here so "wear" is not
implemented as darkening decals only.

## 7. Grime is directed, not uniform

The form bible, quoted exactly: "Grime follows water paths, hands, deliveries
and heating. It does not cover every surface equally." Applied to this
street's own fixed anchors (section 3), so the direction is not invented in
the abstract:

- **Water.** A vertical streak below every downpipe's shoe and hopper joint,
  anchored at the MEASURED downpipe positions (every internal party wall, 5
  east, 2 plus 2 west): this is already the existing `Leaking005` decal's own
  logic ("the pipe has to exist before the stain under it means anything",
  `roofline.downpipe` note), extended from the 3 instances currently placed to
  one per downpipe. A shorter streak below every sill, MEASURED sill
  positions. On the west row, staining at the parapet coping joints, since a
  coped parapet is exactly where water sits and finds the one weak seam.
- **Hands.** At adult-height contact points only, no child-height cue
  anywhere (D18): the shop-door push zone (roughly local 0.9 to 1.1 m), the
  letterplate surround (local 1.0 m), and door-pull edges generally. Small,
  localised marks, not a band.
- **Deliveries.** The stallriser's lower 0.3 m, heaviest immediately either
  side of a shop door (crate and trolley contact), and scuffing at the
  DOUBLE-PILASTER seam at every internal party wall: `east_parade_pil0_1`
  (x 8.65 to 9.0) and `east_parade_pil1_0` (x 9.0 to 9.35), MEASURED as two
  separate 0.35 m piers meeting at the party line rather than one shared
  pier, are two different shopkeepers' joinery abutting, and that seam is
  where a delivery swung round the corner scuffs both at once and where two
  independent repaint campaigns visibly fail to match.
- **Heating.** Soot-dark brick immediately around and a short distance below
  every chimney pot, on the row that has chimneys (`east_parade`, section
  3.1); this is the HEAVY band's other anchor besides the laundry vent.

## 8. Materials: every element against a surface we hold

Checked directly against two things in this session, not recalled: the file
listing at `ledger/Assets/StreamingAssets/CityPack/textures/` (17 files: base
plus `_n` plus `_r` for `asphalt`, `brick_grey`, `brick_grey_b`, `brick_red`,
`brick_red_b`, `concrete`, `glass`, `kerb`, `metal`, `plaster`, `plaster_b`,
`roof`, `roof_b`, `sidewalk`, `window`, `wood`, i.e. 12 named surfaces, 4 of
them with a second `_b` bond/coursing variant) and
`production/specs/asset-interface.md`'s own surface list, "asphalt concrete
kerb sidewalk brick_red brick_grey plaster wood metal glass window interior
card roof paint_yellow multiply", which adds the four procedural/generated
names (`interior`, `card`, `paint_yellow`, `multiply`) that are not CityPack
photographs.

| Element | Surface | Tag |
|---|---|---|
| Main wall, east row | `brick_red` | MEASURED, existing convention |
| Main wall, west row | `brick_grey` | MEASURED, existing convention |
| Piers, spandrels, chimney stacks | same as their row's wall | MEASURED |
| Stallriser (default) | `concrete` | MEASURED, existing convention |
| Stallriser (CHOSEN wetter-trade variant, section 4 item 3) | `plaster` | CHOSEN, already held, no fetch |
| Fascia board, cornice, console, door leaves | `wood`, tinted per bay | MEASURED base surface; the TINT MECHANISM is UNCONFIRMED, section 10 |
| Sills, lintels, parapet, coping (row default) | `concrete` | MEASURED |
| Bay1's replacement lintel (section 5 alteration) | `metal` | CHOSEN, already held |
| Shop-door glazing, toplight, display glazing | `glass` | MEASURED, `C7_shop_glazing` |
| Upper sash windows (frame and pane as one box) | `window` | MEASURED, `D8_upper_windows` |
| Downpipes, gutters, letterplates, railings, laundry vent, security grille frame | `metal` | MEASURED |
| Roof (pitched slate, and the parapet coping's own concealed deck) | `roof` | MEASURED |
| Fascia lettering, window-painted signs, paper notices | `card` (generated 2D route) | MEASURED, existing convention, a different pipeline (imagegen) from CityPack |
| Shop interior backdrop behind glazing | `interior` | MEASURED, existing convention |
| Wear decals (streak, damp, general soiling, scuffs) | `multiply` blend | MEASURED, `decals.blend` key: "multiply=darkens-what-is-under-it" |

**Wear decal SOURCES already held**, checked by directory listing and, for
two of them, opened and looked at rather than only named (rule 4):
`ledger/Assets/StreamingAssets/Decals/ambientcg/Leaking005` (vertical streak,
already placed) and `Moss001` (damp, already placed) cover the water-path
cues in section 7. `SurfaceImperfections001/003/007/012` (opened: mottled
dark and light blotching, plausible for general wall soiling, the MODERATE
band) and `Scratches003` (opened: fine linear marks, plausible for
hand-contact and door-edge wear) are HELD but not yet placed anywhere on this
street; this spec names them as the candidate source for the new cues in
section 7 and marks their final visual fit an eye-check for VERIFY, the same
hedge `asset-interface.md` already carries for `C7_shop_glazing`'s
whole-facade photographs.

**Nothing in this section is MISSING.** Every element named above, across
both rows, all twelve bays and every alteration in section 5, maps to a
surface already on disk, licensed, and already in production use on this
street. That is a checked answer, not an absence of looking: fourteen
elements were checked against seventeen held CityPack files plus four
procedural surface names plus the decal library, and all fourteen resolved.

## 9. Handoff to AUTHOR

**The template for every conversion below is `C15_fascia_cornice_console`,**
already done, already verified, already sitting on this exact street. Its
route was `GENERATE`/`PROC` (a box from the JSON) and it is now `HAVE`,
"authored in house by `production/art/fascia-01/author/make_fascia_mouldings.py`,
regenerable byte for byte", at the SAME measured dimensions the street already
placed, moving nothing else and deleting nothing. Every BOM line below asks
for exactly that conversion, not a redesign.

| BOM line | Today | Target | Note |
|---|---|---|---|
| `C1_terrace_carcass` | PROC box | AUTHORED, same 6 x 6.2 x 8 m envelope per bay | The carcass is where "blank wall" is most visible; reveals at every opening (section 3) are what a box cannot give |
| `C5_shopfront_assembly` | PROC boxes | AUTHORED, same stallriser/pilaster/fascia/transom envelope | Per-bay variation, section 4 and 5 |
| `C8_door_shop` | PROC box | AUTHORED | Per-bay offset, section 4 item 1 |
| `C9_door_side` | PROC box | AUTHORED, OMITTED on bay5 | Section 5 |
| `C13_sills_lintels` | PROC box | AUTHORED, `metal` on bay1 | Section 5 |
| `D2_chimney_stack` | PROC box | AUTHORED | East row only today, section 3.1 |
| `D5_downpipe` | PROC box | AUTHORED, laundry vent variant on bay4 | Section 5 |
| `D6_gutter_run` | PROC box | AUTHORED | |
| `D7_parapet_coping` | PROC box | AUTHORED | West row only |
| `D8_upper_windows` | PROC box | AUTHORED | Dressing per section 4 item 5, never the size or the line |
| `C6_fascia_lettering`, `C7_shop_glazing`, `C15_fascia_cornice_console`, `D3_chimney_pots` | HAVE | UNCHANGED | Not this spec's to touch; C7 carries an existing unresolved scale-mismatch flag, carried forward, not fixed here |
| `D4_tv_aerial` | PROC | UNCHANGED, stays procedural | Its own BOM note already recommends this: "not CC0-fetchable anywhere... it is a comb of cylinders" |
| `G1_leak_stains`, `G4_moss_damp`, and the new wear cues of section 7 | HAVE (decal) | EXTENDED placement, same route | No new geometry, no new fetch |

**The mesh contract** any authored GLB must satisfy, PRECEDENT,
`asset-interface.md`, read in full this session: metres, +Y up, -Z forward,
shipped life size and never rescaled at placement, pivot free (bounding-box
centre is what placement uses), one material slot, unlit, untextured
(the street's own material overwrites slot 0 by the piece's `surface` field),
verts in the 56 to 2362 range the shipping set already spans, stable ID equal
to the file name, appearing in the same four places
(`ledger/Assets/Props/base-mesh/<id>.glb`, a BOM line, a piece's `asset`
field, the imported uasset).

## 10. Acceptance checks: arithmetic, not taste

No number below is an invented threshold. Each is a geometric or
attribution fact that either holds exactly or does not, mirroring
`fascia-01`'s own A1 to A15 (PRECEDENT), which is the only prior acceptance
list this street has produced.

1. Every authored GLB's measured bounding box matches the spec box this file
   and its future JSON assign it, worst axis, to 0.001 m: PRECEDENT, the
   existing `import_prop_meshes.py --measure` tolerance.
2. Every new piece's rear face sits on its row's own frontage plane (east
   z = 5.125, west z = -5.125, per the verified datum, section 1) to 0.000
   mm, PRECEDENT `fascia-01` check A7.
3. No interpenetration is introduced with the already-placed
   `C15_fascia_cornice_console` geometry: the cornice soffit must still meet
   the fascia band top at 0.000 mm and the console must still sit under it at
   zero overlap, PRECEDENT `fascia-01` checks A1 to A3, re-measured rather
   than assumed unmoved.
4. `wearCoverage` prints for every new surface with its batch (D53 point 3),
   reported with its count, never bounded by this spec (section 6).
5. One material slot, zero embedded images, per GLB (PRECEDENT
   `asset-interface.md`).
6. Every new asset's licence line lands in
   `ledger/Assets/Props/base-mesh/THIRD-PARTY.md` the same way `C15`'s did:
   "LEDGER's own work... nothing fetched, nothing purchased."
7. `python3 tools/canon-gate.py` clean over any text this spec's content
   introduces downstream (fascia wording, bay-use labels): RUN over this
   file itself, section 12.
8. These fronts are FIXED FACADE DRESSING, not interactive geometry: no door
   or window authored under this spec opens, and nothing here claims a
   collision or gameplay binding beyond what the street already has (a
   scope boundary, CHOSEN, stated so AUTHOR does not infer an interaction
   this spec never asked for).

## 11. What this spec deliberately does not do

- **No wear floor.** Section 6. That number is D53 amendment A1's, set from
  the series this facade starts, not guessed here.
- **No geometry, no recipe, no .blend, no GLB.** Every dimension above is a
  number for AUTHOR to read, not a mesh.
- **Net curtains stay out of scope.** `C12_net_curtain` is already a
  separately tracked, unresolved line (`production/art/atlas-01/PRODUCTION-CATALOGUE.md`:
  "Alpha and perception integration unresolved; do not fake transparency with
  an opaque prop"). This spec does not add a second unresolved attempt at it;
  section 4 item 5 substitutes opaque techniques that already work.
- **C7_shop_glazing's scale-mismatch flag is carried forward, not resolved.**
  `asset-interface.md`'s own note that a whole-facade photograph bound to a
  single pane needs an eye check stands; nothing here changes that binding.
- **The fascia paint-tint mechanism is unconfirmed, not asserted either way.**
  `paint_yellow` is an existing precedent for a tinted procedural surface
  (`vignette-scene.json` `paint` key, `ProceduralOnly in AssetLibrary`), but
  whether per-instance tinting of `wood` is already wired for a fascia board
  was not found either way this session and is not claimed. AUTHOR checks
  `tools/ue/make_base_material.py` before treating per-bay fascia colour as
  free; if it is not wired, that is a MISSING technical capability and a
  decision record, not a texture gap this section's MISSING check would have
  caught.
- **West-row chimneys are not added.** MEASURED as absent from both west
  rows today (section 3.1); completing the roofline there is a future pass,
  named so it is not mistaken for an oversight in this document.
- **`east_parade_bay0` (Mickey's) is not respecified.** Its architecture is
  already fully authored elsewhere; this spec only corrects how its USE is
  described (section 2) and does not touch `MICKEYS.md` or its data file,
  which sit on a different branch and are out of scope here. That file's own
  "became a beer house" wording is stale against D17/D19 and is named here so
  it is not missed by whoever next opens it; it is not fixed by this spec.
- **Setts are out of scope.** The brief names a `setts` ground surface
  landing tonight; checked this session (`tools/citypack/choices.json`,
  `AssetLibrary.cs`), the NAME and material case are wired
  (`PavingStones115B`) but the texture BYTES are not yet fetched into this
  checkout's `CityPack/textures/`. Setts are a ground/yard surface, not a
  facade one, and nothing above depends on them; the yard gap at x 21 to 24
  (section 1) is a future ground-authoring pass, not this one.
- **`Mickey's blockout` numbers were not re-derived.** Where MICKEYS.md and
  `vignette-scene.json` overlap (the source street's own bay/carriageway/
  footway figures), this spec reads the street file directly rather than the
  pub commission's restatement of it, per rule 1.

## 12. The canon gate, run over this file

`python3 tools/canon-gate.py production/specs/terrace-fronts.md`, run four
times in this session, because the second run's own fix repeated the fault
it was fixing and the gate caught that too.

FIRST RUN: RED, 1 finding, a six-letter word for a building's structural
envelope (a homophone of a real petroleum brand this project does not
intend) inside a quotation from `RECIPE-REPAIR.md`, at the old line 136.
FIXED BY REWORDING, PRECEDENT `fascia-01`'s own "reword, never loosen":
the sentence now paraphrases that source using this project's own word for
the same thing (the BOM's own `C1_terrace_carcass`) instead of quoting the
flagged word verbatim.

SECOND RUN, after that reword: clean, 0 findings in 1 file, 625 lines
examined.

THIRD RUN, after adding the paragraph above describing the first finding:
RED again, 2 findings, because naming the flagged word to explain the fix
put the word back in the file. FIXED THE SAME WAY, by describing rather
than naming it, which is the paragraph above as it now reads. FOURTH RUN,
after that: clean, 0 findings in 1 file, 644 lines examined, 13 era terms
and 45 brand tokens screened. The gate itself was not touched at any point
and no exemption was added.

## 13. Sources, dated

- `production/art/atlas-01/data/atlas.json`, key `street_anchor`, on
  `origin/art/atlas-01`, `base_commit` `7722b45cb3dcee2fbcee26675fae4fef641cbba7`. Read 2026-09-21.
- `production/specs/vignette-scene.json` and `production/specs/vignette-pieces.json`,
  `main`, written 2026-09-02. Read in full 2026-09-21, keys `street`,
  `shopfront`, `facade`, `roofline`, `paint`, `surface_tiling`,
  `bill_of_materials`, `history` (null), and the raw `pieces` array filtered
  by `region`, `bom` and `name`.
- `production/specs/vignette-bill-of-materials.json`, `main`. Read 2026-09-21,
  entries `C1`, `C5`, `C6`, `C7`, `C8`, `C9`, `C13`, `C15`, `D2` to `D8`,
  `G1`, `G4`, plus `route_values`/`make_by_values`/`not_on_this_list_deliberately`.
- `production/specs/asset-interface.md`, `main`. Read in full 2026-09-21.
- `production/art/atlas-01/TOWN-FORM-BIBLE.md`, `PRODUCTION-CATALOGUE.md`,
  `DISTRICTS.md`, `MICKEYS.md`, `data/pub-operations.json`,
  `previews/hook-uses.svg`, `recipes/mickeys_blockout.py`, `RECIPE-REPAIR.md`,
  all on `origin/art/atlas-01`. Read 2026-09-21.
- `production/art/fascia-01/01-SPEC-fascia-package.md` and `DELIVERY.md`,
  `main`. Read in full 2026-09-21.
- `canon.md`, `ledger-v2/respec/decision-register/D13`, `D14`, `D17`, `D18`
  (via `canon.md`'s own copy), `D28` and its Amendment A1, `D53`. Read in
  full 2026-09-21.
- `game-design/decision-2026-09-21-ruling-the-terrace-fronts-are-authored-and-everything-else-comes-from-what-we-hold.md`
  and `game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
  Read in full 2026-09-21.
- `content/brands/brand-bible-v1.json`, `production/throughput.md`,
  `ledger-v2/studio-v2/pipelines.md`, `ledger-v2/research/license-allowlist.md`.
  Read 2026-09-21.
- `ledger/Assets/StreamingAssets/CityPack/textures/` and
  `ledger/Assets/StreamingAssets/Decals/ambientcg/` and `.../generated/`,
  directory listings taken 2026-09-21; `SurfaceImperfections001.png` and
  `Scratches003.png` opened and looked at, 2026-09-21.
- `tools/ue/make_base_material.py`, the wetness-token section near line 1310,
  read 2026-09-21, not edited.
