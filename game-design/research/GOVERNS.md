# What governs the next asset

STATUS: LIVE, verified 2026-09-21. Reads `game-design/research/` (7 files, all
on main) and the 8 approved concept sheets (on `origin/art/atlas-01`, not on
main). Covers the 17 street-level asset families named below. Everything this
page does not cover is stated in its own section near the end, not left for a
reader to discover by absence.

## Why this page exists

Jafar, 2026-09-21: "Every authored asset's brief names the concept sheet and
the research that govern it, and follows them. This is the second time a
design question was debated that the research and the concept art had already
answered, and the facades must not be the third." The immediate case is
recorded in full, with an independent 3x-crop check of the Hook sheet's two
lamps, in the decision record dated 2026-09-21 under `game-design/` whose
filename starts `decision-2026-09-21-ruling-the-sheet-and-the-research`. This
page generalises that one incident into a lookup: for a family about to be
authored, which sheet, which panel, which research line, and what it
actually says.

## How to use this table

Find the asset family. Open the named concept sheet at the named panel or
swatch. Read the named research line. If your own general knowledge of "what
this sort of thing usually looks like" disagrees with either, the sheet and
the research win, not your priors, by the ruling above.

**WHERE `hook.png` MEANS, IN EVERY ROW BELOW:
`production/reference/hook-sheet.png`.** On `main`, in a plain checkout. Not
`production/art/atlas-01/concepts/hook.png` - that is Codex's sheet, RETIRED
on 9 September, and it still resolves on the art branch, which is how a week
of comparisons went to the wrong picture with nothing failing. This page sent
all seventeen families there until 22 September. The rows were measured off
the retired sheet, so **treat every "crop-verified" claim below as unverified
until it is re-read on the live sheet**; the ones already re-read are marked.

AND THE SHEET IS HALF THE REFERENCE. It governs mood, palette and
composition; the period photographs at `production/reference/photographs.md`
govern what things actually looked like, and where they disagree the
photographs win (Jafar 2026-09-22). Before using a row below, check it against
`production/reference/hook-sheet-audit.md`: **the shopfront, window and door
rows are affected** - the sheet has no metal shopfront anywhere, and D01/D06
require one.

The other seven district sheets (copper, exchange, fairview, gullwing,
ironside, mickeys, parade) are on the art branch and NONE of them has been
re-approved as a reference. A row that cites one is citing an unapproved
picture; it needs a ruling before it is followed.

## Coverage, counted

17 families attempted, all 17 landed a row below (0 skipped). Of those:
- 13 have BOTH a concept-sheet hit and a solid research citation: street
  lighting column, road surface, kerb, terrace facade, shopfront, window,
  door, roof, chimney, drainpipe, railings, dustbin, road markings.
- 4 have only one side solid, named as such in their row and again in "Thin
  or partial coverage" below: wall bracket lamp (sheet solid, research thin),
  pavement surface (sheet solid, research thin), telephone box (research
  solid, no sheet hit), pillar box (research present but generic, no sheet
  hit).
- 0 have nothing on both sides.

Sources actually opened for this pass: all 7 files under
`game-design/research/` (art-direction.md, content-sourcing.md,
imagegen-licence-check.md, inhabited-street.md, performance-budget.md,
procedural-density.md, water.md), read with `grep -n` across the whole set
plus targeted reads of the hits; all 8 approved sheets, viewed in full and,
for the two lamp rows only, cropped and re-viewed at 3x. No other branch and
no `game-design/decision-*.md` beyond the one named above was read for this
table; that is a stated exclusion, not an oversight, see "What this page does
not cover".

## The table

| Asset family | Concept sheet (file, panel or swatch) | Research (file, line) | What it actually says |
|---|---|---|---|
| Street lighting column | `hook.png` bottom panel: slender near-black steel column, a shallow long swan-neck arc, small flat canopy head aimed down the street, no fluting, no ladder bar, no scroll, no finial (crop-verified at 3x; also present in every other sheet's street panel) | `art-direction.md:346-347` | "sodium lanterns on swan-neck steel columns" |
| Wall bracket lamp | `hook.png` top panel: dark conical bracket lamp under the Harbour Office eaves, short curved arm off the roof/wall junction, wire-cage guard over a warm bulb (crop-verified at 3x) | `content-sourcing.md:322-323` | "the ones procedural geometry does badly (a crane's lattice, a Victorian bracket lamp)" |
| Road surface | `hook.png` bottom panel, Quay Street carriageway (scene only, no dedicated swatch) | `procedural-density.md:545` | "GTA V used separate tiling textures for kerb, road and pavement as submesh materials" |
| Pavement surface | `hook.png` bottom panel, stone flags either side of the carriageway (scene only, no dedicated swatch) | `content-sourcing.md:168` | "categories we never swept: corrugated steel, paving, kerbs, roof tiles, rust, wet asphalt" |
| Kerb | `copper.png` bottom panel, kerb edge under the double yellow line, Weighhouse Lane (scene only, no dedicated swatch) | `procedural-density.md:162` (§3.2) | "kerb line \| edge centreline ± Width/2 \| lamps, bollards, gullies, parked cars, double yellows, cones" |
| Terrace facade | `mickeys.png` top panel, full elevation from Quay Street | `procedural-density.md:607-608` (§7.2) | "terrace frontage 4.5–6 m typically, 3 m at the smallest, 7 m+ at the largest" |
| Shopfront | `mickeys.png` top panel, the Harbour Fish and Mickey's fascias side by side | `procedural-density.md:675` (§7.5) | "shopfront recess (door set back between two windows) \| 0.3–0.6 m" |
| Window | `mickeys.png` top panel, the upstairs sash windows with net curtains | `procedural-density.md:677` (§7.5) | "window reveal \| 0.10–0.15 m" |
| Door | `mickeys.png` top panel, Mickey's maroon double doors with etched glass | `procedural-density.md:676` (§7.5) | "door reveal in a terrace \| 0.12–0.20 m" |
| Roof | `hook.png` swatch strip, the SLATE swatch (2nd of 4 material swatches) | `art-direction.md:305` (§4) | "Roofs are Welsh slate, dark grey to black." |
| Chimney | `copper.png` top panel, three chimney pots in the foreground | `art-direction.md:345-346` | "chimney stacks with pots" |
| Drainpipe | `mickeys.png` top panel, the black downpipe on the party wall between the two shopfronts | `art-direction.md:345` | "drainpipes (the vertical line on every rear elevation)" |
| Railings | `exchange.png` bottom panel, the black spiked railings in front of the solicitor's window | `procedural-density.md:354-355` | "Rust streaks get the same treatment under every metal fixing: brackets, downpipe clips, railings, signage bolts." |
| Dustbin | `hook.png` object-study swatch, GALVANISED DUSTBIN | `art-direction.md:347` | "wheelie-less metal dustbins" |
| Telephone box | nothing found in the 8 approved sheets (checked all 8: copper, exchange, fairview, gullwing, hook, ironside, mickeys, parade; the Parade sheet's "PAPER TELEPHONE NOTICE" object study is a paper notice, not a kiosk) | `art-direction.md:310-311` | "the commonest British kiosk, introduced 1935, painted BS381C red 538" |
| Pillar box | nothing found in the 8 approved sheets (same 8 checked as above) | `art-direction.md:316` | "800 types, each carrying the reigning monarch's cypher" |
| Road markings | `copper.png` bottom panel, the double yellow line along the kerb, Weighhouse Lane | `procedural-density.md:554` (§6.4) | "double yellow lines \| 75 mm wide at ≤ 40 mph (100 mm above, 50 mm in sensitive areas); laid ~250 mm from the carriageway edge; the gap between the two lines equals the line width" |

## One word in the research that must not be read across, 2026-09-21

`content-sourcing.md:322` contains the phrase "a Victorian bracket lamp", and
it is quoted in the WALL BRACKET LAMP row above because it is the only research
line that names that fixture at all. READ WHAT THAT CLAUSE IS ABOUT: it lists
assets "procedural geometry does badly" as an argument for a single-image-to-3D
route. It is a difficulty note, not a form spec, and the row says so.

IT IS NOT LICENCE TO MAKE THE STREET COLUMN VICTORIAN, and the two are
different fixtures. Jafar ruled on 2026-09-21 that a 1990 working port has
swan-neck columns with sodium lanterns and not Victorian heritage lamps, the
research at `art-direction.md:346` independently names "swan-neck steel
columns", and the Hook sheet shows a plain slender dark column with no
ornament. All three agree about the COLUMN. The bracket lamp on the Harbour
Office is a separate wall fixture whose form comes from the sheet, where it
reads as a dark conical shade with a wire-cage guard.

Added by the director on the day the page was written, because a reader
skimming for the word "lamp" would find that clause first and it is the one
line here that could send the next asset the wrong way.

## Thin or partial coverage, named rather than hidden

- **Wall bracket lamp.** The sheet hit is strong and crop-verified. The
  research hit is one clause about 3D-reconstruction difficulty, not a
  period or form specification; nothing in the 7 files sets its size, colour
  or mounting height the way R-B3 to R-B5 do for the street column. Treat the
  sheet as the primary source for this family until research says more.
- **Pavement surface.** The sheet shows it in every street panel but carries
  no dedicated swatch the way SLATE or QUAY STONE does. The research hit is a
  sourcing note ("categories we never swept") about where to fetch a paving
  texture, not what British paving should look like beyond the
  kerb/road/pavement submesh split noted under Road surface.
- **Telephone box.** Research is strong and specific (BS381C red 538, 1935).
  No K6 box appears on any of the 8 approved sheets. An author working from
  the sheets alone would not know one is wanted here at all.
- **Pillar box.** Research names the family but not a specific form for
  Meridian's box ("800 types"). No pillar box appears on any of the 8
  approved sheets. `procedural-density.md:167` places both this and the phone
  box at "junction corner", which is a placement rule, not a form spec.

## What this page does not cover

- Only these 17 families. The full street kit is larger; a family not
  listed here was not checked and its absence is not a claim that nothing
  governs it.
- Only the 7 files on `game-design/research/` and the 8 sheets named above.
  The 48 `research/*` branches that queue 394 names are a separate lane, not
  read into this table. Their SUMMARY.md / RECHECK.md / BRIEF.md files were
  copied onto main under `production/research/` in the same session as this
  page (57 of 57 files found, across 47 of 48 branches; see the session
  report and queue 394 for the count and the one branch with neither file).
  None of that material is indexed here yet: it is a different research
  lane (crime fiction tone, policing, clothing, conversation model, and
  so on), not a second source for the 17 families above, and none of its
  47 topics named itself as being about street furniture or facades.
- Only one `game-design/decision-*.md` was read (2026-09-21, cited above).
  Other rulings may bear on individual families (a railing ruling and a lamp
  ruling both exist in that directory) and were not searched for this pass;
  a decision record can overrule a research line the way Jafar's own reply
  was overruled tonight, so treat this table as necessary, not sufficient,
  and check `game-design/decision-*.md` for the family you are authoring
  before you build.
- No swatch or panel coordinates in pixels are given beyond "top panel" /
  "bottom panel" / the swatch's printed caption. Cropping closer than that,
  the way the two lamp rows were checked tonight, is on whoever authors the
  asset.
