# Quay Street's paper and small boards: the exact target

84 sheets, cards, boards and plates for Quay Street's paper and small boards: the poll-tax set, the chapel hall's two photocopied notices, the fights, the market, the Tivoli's quads, strips and programme (the named variants held, and the nameless ones too where they would read as stand-ins), 7 ferry and Harbour Board sheets, 5 police and council notices, 35 shop-window and newsagent cards, 5 letting boards (the default is the fascia target's), 6 street name plates (name only by default); the default street carries no unminted name and a BARE quay gable: 62 placements (46 default, 16 held), at most 8 fly-posters and 4 poll-tax bills as the asset plan says (5 and 3 carried), the street date Monday 29 October 1990, every item read glyph by glyph in its own pixels, 780 checks.

Cloud week 42, written 8 to 9 October 2026. **SECOND AND LAST TRY**, after `TARGET-REVIEW.md` (FAIL, 13 faults, all answered below); the re-review's four faults were then fixed **by Jafar's ruling of 9 October, exactly as the reviewer wrote them, and are not re-reviewed** (section A2). Three 2D units build from `target.json` and this page: 4.2 posters and notices, 4.3 "To Let" boards, 4.4 street name plates. Nothing is committed.

Plain summary. 84 sheets, cards, boards and plates, every word ours, listed and checked against the content rule, canon and the 1990 calendar; **the street's date is Monday 29 October 1990** and every placed item's age is checked against it. The default street carries **no name the town has not minted** and no bill that names nothing: the poll-tax bills say STAND TOGETHER, the dance LIVE MUSIC, the market bill needs no name, the empty unit's board is the fascia target's own TO LET (900 x 450, no agent, no number) and the flat above has no agent. The named versions are `-named` variants (and L01, L03, B01, G01, G02) marked proposed, not minted, and held; so are the nameless Tivoli quads and programme (A NEW THRILLER, A NEW COMEDY) and the wrestling bill with no ring names and no hall, which read as stand-ins. The paper is AT MOST the asset plan's amount, 8 fly-posters and 4 poll-tax bills (the default street carries 5 and 3): **the quay gable is bare, as the Hook sheet shows it** (the downpipe, the render patch and the damp foot, no paper and no plate), the empty unit's glass carries six sheets (a police appeal among them) as the proof sample, the plain west row one market bill on its poster pier and one poll-tax bill in a window, and two shop windows a notice each. The jumble-sale and dance notices are photocopied A3 sheets; the Tivoli's venue and dates are a separate pasted strip; the street name plates are name-only, QUAY STREET cast aluminium, none on the yard entrance. **The checks now read the pixels glyph by glyph** (section 12): the first try's checks passed a changed date, TEA for ALE and LUNCH for BINGO; these fail every one.

Files in this folder:

- `target.json`: the whole target (84 items, 62 placements of which 16 are held (the named twins, the nameless stand-ins and the gable's proof wall), 2 cases or boards, a card board, 6 piers, 8 shop fronts, 780 checks, the self-check result).
- `make_target.py`: the author tool that writes `target.json` (every width is measured on the real font files; every item's pixel scale is chosen by `glyphlib.py`).
- `glyphlib.py`: the glyph kernels shared by the author tool and the self-check (the per-glyph score F, the separation score SEP, the table that sets each item's scale).
- `target_drawing.py`: draws every item's boxes, baselines and clean lettering at 1 mm to the pixel, the surfaces' elevations (the gable with its downpipe, the empty unit's glass, the west piers, the plates' places) and the cases, from `target.json` alone, into a folder given on the command line, plus the polygons as JSON.
- `self_check.py`: its checks and their count are in section 15; it writes its result into `target.json` under `self_check`; `--fetch-fonts DIR` fetches the three font files not in `production/fonts`; `--groups 12,13` runs some groups only. It also holds the READER a builder's own checker must copy (section 12).
- `make_previews.py`, `make_doc.py`: rebuild the previews and this page.
- Previews, in `production/previews/cloud-week/refs/posters-boards-plates/`: `P1-urban-street-01-notice-case.jpg` (the one photograph measured, windows and the council crest masked), `P1-...-target-on-photo.jpg` (the proportions laid on it), `L1` to `L4` (layout sheets of every item), `L5` (the paste plan: gable, glass, piers, plates).

## A. The second try: thirteen faults, thirteen answers

The reviewer (a fresh target reviewer, 9 October) ran `self_check.py` (215 of 215 then), then rendered wrong items through the target's own reader and found the checks blind to a wrong word, date or price; found unminted names as the street's default dressing; and found placements, ages, cues and a ferry timetable that contradicted the project's own notes. Each fault and how this try answers it:

| # | Fault | Answer |
|---|---|---|
| 1 | the checks could not see a wrong word, date or price in the pixels | ITEM.glyphs reads one glyph at a time in its own cell (glyphlib.py, self_check.py group 12): F >= 0.85 at 0.5 mm against the glyph re-rendered from the manifest, and SEP >= 0.70 against every other glyph of the font and its own mirror, on the pixels where they differ; each item's pixel scale is chosen so that every non-twin pair differs by at least 8 pixels. Every wrong render the reviewer built (a changed date, a changed price or time, TEA for ALE, Teas for Beer, LUNCH for BINGO, a mirrored hand card, a misspelt plate) FAILS; a true render, jittered hand renders (20 seeds each of K01 and SA06, 8 each of K07a, K09a and SA15) and a true render turned 1.2 degrees and read in the placed street PASS. The reviewer's own harness, run unchanged, now also fails every PRINT wrong render (the line score includes the worst glyph); hand lines need the renderer's manifest, which is the review's own amendment (a). ART.eye, PLACE.built, ITEM.square and the square-on rule are added. (After the second review, by Jafar's ruling of 9 October: the true jittered renders of all 29 hand cards, 20 seeds each, and a true render of every item pass all pixel checks; ITEM.clean reads ink outside every block; a missing manifest fails.) |
| 2 | unminted placeholder names were the street's default dressing | the default street carries nameless items only where they read naturally (STAND TOGETHER, LIVE MUSIC, no agent); the named versions are -named variants and L01, L03, B01, G01, G02, each held_until_minted with its names; their placements are held twins; G.page.placeholders added and tested. (After the second review: the nameless T02, T03 and W01, which read as stand-ins, are held like their twins.) |
| 3 | the WEIGHHOUSE LANE plate named the yard entrance | the S02d placement and every 'proposed because canon does not name the opening' line are deleted; S02 is a kit plate like S03; the side opening is the yard entrance and carries no plate; C03 keeps DIVERSION VIA WEIGHHOUSE LANE. |
| 4 | the paste plan was far denser than the asset plan and covered the gable the sheet shows bare | at most eight fly-posters and four poll-tax bills (G.place.paper; the default street carries 5 and 3). First answer: SF1 carried one layer of three bills with the 75 mm cast-iron downpipe at u 0.30 and paper 150 mm clear. After the second review, by Jafar's ruling of 9 October, the gable is BARE as the Hook sheet shows it: the three bills, the strip and the second plate are held placements (G.place.gable: no paper and no plate on SF1; the downpipe, the render patch and the damp foot stay as fixtures). SF2 carries M01, P03, P02, J01, C02 and C01a; the west pier W1.0 (the scene's poster slot) takes M01 at class B; P02 is also an A3 window bill in the bay-1 window at x 12.3 (scale 0.585, top 1.90 m); no sticker on the gable, no bill on the other piers. |
| 5 | two targets gave two letting boards, and C02 used the wrong address | L02 is the fascia target's board exactly (900 x 450, TO LET, Libre Franklin 800 cap 130, vinyl red, no agent, no number) and is the default on SF5; L01 (1200 x 450 with an agent) is a held variant that would need the fascia target changed in the same batch; G.letting.mount compares size, font, weight, cap and colour with the fascia target; C02 reads 'Change of use of the ground floor, 7 Quay Street,'. |
| 6 | two proposed names collided with real ones | TIGER JIM LARKIN is TED HOLROYD (first BIG TED HOLROYD, withdrawn after the second review: 'Big Ted' is the bear of the BBC children's programme Play School; BIG TED is in real_marks) and THE SEA WOLF is THE HARPOONER (and MAD MAURICE and THE BARON, a television series, are SPANNER SMITH and THE STEVEDORE), all held and listed for the town to check; LARKIN, SEA WOLF and SEA WOLVES are in forbidden_patterns.real_marks, with the real wrestlers, soap powders, cinema chains and campaigns the probe listed. |
| 7 | period wording and process read as the wrong decade or country | D01 says SEQUENCE; W01 says PROFESSIONAL (Oswald 700 fitted to the 428 mm measure); the Tivoli's weeks start on Thursday (T01 from THURSDAY 18 OCTOBER, T02 from THURSDAY 25 OCTOBER, T03 four lines); the venue and date are a separate letterpress strip (T01s, T02s, 1016 x 90 mm, black on white, own class, 0.25 degrees off the quad's square) and the litho's top band is blank; J01 and D01 are photocopy A3 notices in shop windows; H03 reads NOTICE TO MARINERS. |
| 8 | no street date, so the age classes contradicted each other | calendar.street_date is Monday 29 October 1990; T03 and D01 are class B, J01 class B everywhere; G.dates.age checks every placed dated item against its class's days (event - 42 <= street date - age <= event; a notice at or after its date) and is tested on the first try's contradiction. |
| 9 | the mirror guard of the 29 hand cards contradicted their fixings | every SA card is taped (no pins); each hand card has ONE cue matching its fixing and nothing on the right half: one tab of yellowed tape across the top-LEFT corner (K05, K06c, K07a-d, K09a-f, SA01-SA15) or the knot and sucker at the top-LEFT (K01, K06a); every crease, tear and pin-hole cue is gone; G.mirror.cues reads the 25 mm top-left and top-right patches only and is tested on all 29 cards, true and mirrored; ITEM.glyphs also fails a mirrored hand card. |
| 10 | placements contradicted the brand bible and the items' own words | HC1 and FC1 are not placed (FC1 is a painted timber board, 600 x 800, F01 over F02, no glazing); C01a is inside the empty unit's glass (SF2, u 0.30, z 1.30, four tape tabs); K02 is unplaced; K05's bottom is 1.42 m (not 1.38: the fascia target's vinyl lettering on the same glass tops out at 1.385) at u 0.64, beside the assumed hours plate. |
| 11 | parts a script could not make from target.json alone | K04: ring 7 mm and a 7 mm bar at 45 degrees, polygon given; G02: a white ring 16 mm wide at 0.70 of the disc's radius; K02: ticks 2 x 8, hour hand 30 x 5, minute hand 40 x 4 (buff card), a 6 mm brass fastener; plates: 10 degrees of draft and a 0.8 mm top radius on raised letters and border, pressed aluminium rolled edge radius 3 mm, enamel rolled edge 6 mm, cast edge 6 mm with a 2 mm arris; HC1: rails 46 x 60 with a 4 mm chamfer, glass 4 mm in a 10 x 10 mm bead; also K03's hole and chain, and every enamel board's corner and roll radii. |
| 12 | the ferry stranded its one boat | the far-side column ends '9.45 10.45 / LAST CROSSING 11.15', so the boat is at the Hook at 11.30 each night and the street's 'last crossing's at eleven' holds from the Hook; G.ferry.schedule simulates the one vessel from the printed blocks and checks that each day ends where the next day's first sailing leaves (Monday to Saturday, Sunday, Monday). |
| 13 | name plates against the project's own note | the default and placed variant is `n` (name only); `d` stays a variant; S01p, S02p, S03p and MR1 are deleted; QUAY STREET is cast aluminium with letters and border raised 3 mm, painted white with black letters, the paint flaking at the raised edges; every plate is at least 200 mm deep; the relief, draft and edge radii are in numbers and G.plates.make checks the lettering against them (Marcellus SC's thinnest stroke at 90 mm capitals is thick enough for a cast or pressed letter). |

**Where this try differs from the reviewer's amendment, and why (each with its source).**

- **Fault 1(b), the glyph margin.** The review asks that each glyph out-score every other glyph of its font and its own mirror by at least 0.05 on F at 0.5 mm. F is a mean over the whole glyph, so glyphs that share most of their ink score alike. Measured by `self_check.py` (group 12, `f_margin_table`): in Oswald 700, 34 mm capitals, 2 px/mm, 11 of the 36 capitals and digits cannot meet 0.05 (O against D 0.013, 6 against 8 0.036). The check therefore keeps the review's own gate for the glyph itself (F >= 0.85 at 0.5 mm) and scores the separation from every alternative on the pixels where the two glyphs differ (SEP, section 12), gate 0.70, a margin of 0.40. Every wrong render the reviewer built fails it, and so do 8 for 6, 3 for 8, B for R and the other near pairs.
- **Fault 10, K05's bottom.** The review asks 1.38 m so that K05's centre is the 1.45 m its own words give. The fascia target's vinyl row `TOBACCONIST & CONFECTIONER` (cap 70 mm, z 1.35, tolerance 0.03) is on the same shop-door glass and tops out at 1.385 m (1.415 with the tolerance), so a card at 1.38 would stand on the lettering. K05's bottom is 1.42 m and its words now say so. Source: `production/cloud-week/targets/fascia-signs/target.json`, `glass_lettering`.
- **Fault 4, the quay gable (first try, since changed).** The Hook sheet's gable is bare old brick with a downpipe, a render patch high up and a damp foot, and the asset plan's own proof wants "one wall in view ... three bills from three templates". The first answer kept one layer of three bills with the downpipe added and flagged them `proof_wall`. The re-review then asked for the sheet's bare gable and Jafar's ruling of 9 October applied it: section A2. The five `proof_wall` placements are held, and nothing more goes anywhere until he has approved a sample in the assembled game.
- **Fault 4, the count (first try, since changed).** The reviewer's own placements added to 7 fly-posters, not the 8 he cited; the eighth was T03, the Tivoli's programme as a window bill. After the re-review the gable's three bills, T03 and W01 on the pier are off the default street and M01 stands on the pier: **the default street carries 5 fly-posters and 3 poll-tax bills (P03, P02 and P02's A3 window copy), and `G.place.paper` allows at most 8 and 4**.
- **Fault 6, other collisions found.** MAD MAURICE and THE BARON (a 1960s television series' title) went with the two the reviewer named: SPANNER SMITH and THE STEVEDORE. None was checked against real lists (the network is closed); all four are held and listed for the town. `real_marks` now holds LARKIN, SEA WOLF, SEA WOLVES, the real wrestlers, soap powders, cinema chains and campaigns the probe listed.
- **Notes taken.** The tide table peaks on Sunday 4 November (4.4 4.6 4.7 4.8 4.7 4.5 4.2); SA01's number is 960 471; cockles are 45p a TUB (the trade's unit, the pint, is a banned word in this project) and smoked haddock is £2.90, dearer than fresh; T01's art no longer asks for a telephone box (nor T02's for a pier: a beach, deckchairs and a breakwater) and every art slot forbids crowns, kiosk lettering, operator marks, bottles, glasses and arcade signs; the council crest is masked in the P1 previews; the forbidden lists gain plurals and near terms (SCHOOLS, BABYSITTER, PLAYGROUP, SCOUTS, CUBS, BROWNIES, INN, TAVERN, DARTS, QUIZ NIGHT) and the real names above; section 4b no longer says League Gothic is off the plan's table; the fonts off the table are removed (Libre Baskerville, Josefin Sans, the unused Abril Fatface) or recorded with a DECISIONS line (Libre Franklin, Patrick Hand); the drawing script draws the piers' and the plates' elevations.

## A2. Fixes applied after the second review, by Jafar's ruling of 9 October, not re-reviewed

The second review (9 October, `TARGET-REVIEW.md`, "Re-review (try 2)") found most of the first try right and four faults. Jafar ruled on 9 October that the target, set aside after its two tries, gets the reviewer's exact fixes applied. They are applied below as the reviewer wrote them, run against the reviewer's own scripts (try2_tests.py, try2_true.py, try2_allitems.py, try2_sa.py, try2_sq.py), and **no fresh reviewer has looked at them yet**.

| # | Fault | Fix |
|---|---|---|
| 1 | the checks failed correct items and never read ink outside the blocks | ITEM.square finds the angle against the render of the item's own glyph manifest (jitter included) and reports 0 unless F at the best angle beats F at 0 degrees by 0.02: exactly square P05, K04, K03a, K03b, K02, K08 and P06 read 0 and every jittered hand card reads 0; ONE tolerance, 0.3 degrees, in target.json and TARGET.md. The glyph reader gives a pixel a neighbour's ink explains and the glyph's does not to the neighbour, even where hand-lettered glyphs touch (SA01 and SA03 had failed 11 and 15 of 20 true seeds at 8 px/mm; both now pass 20 of 20), reads big capitals at a reduced scale with the same area rule that draws its reference, and counts a space's ink only where it lies beyond 0.6 mm of every glyph (T01-named's true render passes); a glyph whose mirror differs only by edge slivers (an M read at a reduced scale) is its own mirror. glyphlib.needed_ppm measures each hand pair over glyphs jittered to 3.5 sd of the block's hand style (size and rotation, four corners). ITEM.clean (new, per item): the ink-coloured pixels outside every block's glyph window, the item's own shapes, the cue patch and the art slots total at most 2 mm2; the reviewer's four planted lines (K01 BINGO TONIGHT, SA11 Babysitter, evenings., L02 ARMITAGE & STOBBS, C02 BETTING SHOP) and D01 + LICENSED BAR fail it. A missing or unreadable <ITEM>.glyphs.json fails .words and .glyphs and never crashes the reader (render contract). Group 12 reads a true render of EVERY item and 20 jittered seeds of all 29 hand cards through .pos, .mask, .glyphs, .square and .clean; any failure is a self-check failure. |
| 2 | the nameless defaults read as stand-ins | T01, T02, T03 and W01 (the nameless Tivoli quads and programme and the wrestling bill with no ring names and no hall) are HELD like their named twins (item.held, stand_in_of, waits_for): their placements are held_until_minted with the names the twin carries, so G.page.placeholders keeps them off the built street until DECISIONS.md mints the films, the hall and the ring names. Pier W1.0 (the scene's poster slot) takes M01 at class B, a bill that needs no unminted name. G.place.paper is 'at most 8 fly-posters and 4 poll-tax bills' (the default street carries 5 and 3). |
| 3 | BIG TED HOLROYD collides with a real children's programme | TED HOLROYD on the named wrestling bill, in PROPOSED and in every check; BIG TED is in forbidden_patterns.real_marks ('Big Ted' is the bear of the BBC children's programme Play School). |
| 4 | the quay gable is bare, as the Hook sheet shows it | P01, W01, T02 with its strip T02s and the second QUAY STREET plate (the five proof_wall placements) are held, not in the default street; the west corner pier keeps its plate at x 20.47. G.place.gable is now 'no paper and no plate on SF1' and still checks the downpipe, the render patch and the damp foot as fixtures; the check that demanded exactly three gable bills and the one that demanded exactly 8 and 4 are reworded. |

Smaller notes from the same review, taken: the held placement of L01 is sized 1.2 x 0.45 m (it had copied the 0.9 m board); the calendar note no longer cites H03 as a reason for the street date (H03 is not placed); the forbidden lists gain BABYSITTERS, INNS, PLAYGROUPS, TEENS, LAD, LASS and KIDDIES. Noted, not changed: the review's suggestion to render at check scale, check, and downsample for the game is open to the builder and costs the checks nothing; the scales here stay the checks' own (the largest render is 12.4 megapixels).

## 0. What this target rests on, in plain words

- **Photographs measured today: one, and it is not the period.** Poly Haven's Urban Street 01 (CC0, Andreas Mischok, 18 August 2019) shows four glazed notice cases, blue steel, 2000s. I measured their VERTICAL proportions (header 0.152 of the height, window 0.763, foot 0.085, side bands 0.205 of the apparent width, each with its error) and used them only as a cross-check of a glazed case's shape. Nothing else in this target is measured on a photograph. The reviewer's network was as closed as mine: no photograph of a plate, a letting board, a pasted wall or a notice was reached by either of us.
- **Photographs looked at and not used.** Eight other Poly Haven panoramas (London streets and docks, Cambridge, a Dublin quay): none shows a street name plate, a letting board or a poster hoarding that could be measured. Bethnal Green Entrance has a stickered modern pole plate and, in the same frame, a council byelaw sign about alcohol: nothing from it is kept, no crop, no file.
- **Earlier notes (they read period photographs and search summaries on the PC; read here, not re-measured):** the 1990 mix of Letraset, photocopy and two-colour print (asset-plan note 4); the 1952 Kindersley recommendation for name plates and the street-clutter note's plain plates and 20 to 25 cm depth; the winter timetable date of 1 October 1990 and the pasted-over summer sheet (transport-timetables note, the brand bible); cod at about 2.60 a lb in 1990 (the fishmonger note, ONS); the Harbour Board's blue and white enamel and glass case with notices drawing-pinned and curling (the brand bible); the Tivoli's programme 'changed on Thursdays' (the brand bible); the hours, the market's days and the chapel hall (`hook-cast.json`); the yard entrance (`vignette-scene.json`, atlas-01).
- **Search summaries (leads, never numbers):** modern street-plate specifications (90 mm capitals, 150 to 230 mm plates, 12 mm borders, 11 SWG aluminium), a Hull caption on 1920s to 1930s cast plates, a statement that there is no national plate design and that each council chose its own, a Hackney Museum 1990 'Pay No Poll Tax' sheet on yellow paper in red ink, the Double Crown sheet. The pages themselves were not fetched (DNS and 403).
- **Judgement:** every size, colour, wording, price, ageing number and placement not listed above. Section 1 says the kind of each class of number.
- **The honest summary:** this is the weakest of the family targets on its photographic side. It is strong where the project's own files decide: the streets and districts canon mints, the shops' hours and the market's days, the fascia target's positions, board and left-right rule, the plain row's bay layout, the 1990 calendar, the content rule and the lists of real names, and now where its checks are concerned: they read the pixels glyph by glyph. A fresh reviewer should look hardest at sizes and at ageing.

What I would read once the network opens (all unreached today):

- Geograph and Commons photographs of street name plates dated 1985 to 1995 in a northern English port or mill town: plate depth, letter height, border, fixings, whether a postal district or the council's name is on it (the biggest gap: nothing about plates is measured in this target)
- Photographs of estate agents' and commercial letting boards of 1988 to 1992 (Peter Marshall's Hull set; Picture Sheffield): size, layout, colours, how it is fixed to a fascia
- Photographs of fly-posted hoardings and gable walls, 1988 to 1992 (Hackney Museum and Picture Sheffield): the share of the wall covered, layer count, bill sizes in use, how torn and faded
- A 1990 provincial cinema bill and quad, and a 1990 wrestling or boxing bill (Sheffield's National Fairground and Circus Archive; V&A): type, colours, billing block
- 1990 council notices: planning notices, road closure orders, police appeal sheets (local archives, Hackney Archives 2020/26): layout, paper, how fixed to a column
- The Hackney 'Pay No Poll Tax' sheet and the Wandsworth screenprint (V&A O203232/3): colours, type, the imprint line
- The DfT circular 3/93 itself and Alistair Hall's London Street Signs (2020): plate sizes and postal districts
- Liberation Sans/Serif TTFs, if the builder wants them over Archivo and Libre Baskerville

## 1. Reading this file

- Units. Every item has its own frame: **x in millimetres from the viewer's LEFT edge as seen IN THE GAME, y UP from the item's bottom edge**; a block's `baseline_mm` is measured up from the bottom edge. Each item is rendered at its own `px_per_mm` (2 to 12 here, chosen so that every glyph can be told from every other: section 12); row 0 of an image is its top edge. Surfaces use metres: `u` from the surface's viewer's-left edge, `z` up from the pavement; street x is metres along Quay Street (0 at the quay end), the same in the recipe and the game.
- **Every texture is square-on.** No skew, rotation or perspective is baked into any picture: skew and rotation live only in the placement's `rot_deg`, a hand card's tilt included. `ITEM.square` fails a texture turned more than 0.3 degrees, **one tolerance for every item, print and hand-lettered alike**, found against the render of the item's own glyph manifest (jitter included); `PLACE.built` checks the placed decal's rotation to 0.3 degrees.
- Left and right are the VIEWER'S, in the game, by the fascia target's rule: the game mirrors the recipe, so low street x is on the viewer's RIGHT looking at the east parade and on the viewer's LEFT looking at the west block. Every sheet's x runs from the viewer's left; the quay gable is read looking +x, with the front corner at the viewer's left.
- Evidence kinds: Read (printed), Scaled (off a drawing or the game's files), Photo (measured on a photograph today), Derived (computed), Judgement (mine, to be overturned), Lead (a search summary, never a number).
- Colours are sRGB 0 to 255, contrast is WCAG, dE is CIE76. Aged colours are for four classes (section 4).
- **Named and nameless.** An item whose id ends `-named` (and L01, L03, B01, G01, G02) carries a proposed, unminted name in a block of cap 10 mm or more: it is HELD (`held_names`) and its placements are `held_until_minted` twins of the nameless default placements. The nameless Tivoli quads and programme (T01, T02, T03) and the wrestling bill W01 are HELD too (`stand_in_of`, `waits_for`): a bill that names no film, no hall and no ring names reads as a placeholder by another name, so it waits with its twin for the names. The `G.place.*` checks and the drawings use `held` (not in the default street, for any reason); `held_until_minted` is the reason of unminted names.

The kind of each class of number in this target:

| Numbers | Kind | Source |
|---|---|---|
| sheet sizes (crown, double crown, quad, four-sheet; A2 to A6) | Derived | imperial names x 25.4 mm; ISO 216 halving; the Double Crown name is also a Lead |
| ink width of every line, cap ratios, plate lengths, tide and ferry times, each item's pixel scale | Derived | measured on the real font files / computed in make_target.py and glyphlib.py, re-measured by self_check.py |
| the calendar: every weekday and date; the street date | Derived | datetime, 1990; 1 October 1990 was a Monday; 29 October was a Monday (the one day every dated placement allows) |
| street x of the shops, door ends, hanging signs, the fascia, the letting board (900 x 450, TO LET, Libre Franklin 800 cap 130, vinyl red), the empty unit's number 7 | Read | the fascia target, SCENE-SLOTS.md, vignette-scene.json |
| the six piers, the glass, the shop widths, the bay-1 window at x 12.3 | Derived | terrace-front.py's plain-row layout and the shopfront numbers (0.35, 3.562, 0.9, 0.838) |
| shop hours, the market's days and hours, the chapel hall, the yard entrance, the ferry's last crossing | Read | hook-cast.json, vignette-scene.json, atlas-01, tier2-batch-1.json, the brand bible |
| the cod price | Read (earlier note) | ONS series CZOL via FISHMONGER-2026-10-03.md |
| the case proportions (0.152, 0.763, 0.085, 0.205) | Photo | one 2019 modern case, with errors; NOT the period |
| 90 mm capitals, 200 to 240 mm plates, 12 mm border, 30 mm fixings, relief 3 and 1.5 mm, draft 10 degrees, radii | Judgement on a Lead | modern specifications in search summaries; the street-clutter note's 20 to 25 cm |
| the downpipe (75 mm, u 0.30), the render patch and the damp foot of the gable | Scaled by the reviewer | the Hook sheet (TARGET-REVIEW fault 4) |
| every other size, layout, colour, cap, ageing, wear and placement number; every price but the cod | Judgement | the writer's |

## 2. Where each piece goes on the street

Everything here is **Judgement on the scene's own numbers**: SCENE-SLOTS.md, `vignette-scene.json`, the recipe (`terrace-front.py`), atlas-01 and the fascia target. **The amount of paper is AT MOST the asset plan's (note 4, table A5, Quay Street, the proof view): 8 fly-posters and 4 poll-tax bills**; the default street carries 5 and 3 (`G.place.paper`), because the quay gable is bare.

| Surface | What it is | Frame and paste zone | What goes there |
|---|---|---|---|
| SF1 | the quay gable: the east parade's south end wall, plane x = 3.0 m, facing -x (the big brick wall at the right of the hook frame, `morning-hook-day-2026-10-08.jpg`) | u from the front corner into the block (viewer's left), 0 to 8.0 m; z 0 to 6.3 m; paste zone u 0.15 to 6.0, z 0.45 to 2.75 | **BARE, as the Hook sheet shows it: no paper and no plate** (`G.place.gable`). A 75 mm black cast-iron downpipe at u 0.30, full height; the render patch (z 3.6 to 5.0) and the damp foot (below 0.45) bare, as the sheet has them. The plan's proof wall (one layer of three bills, bottoms z 1.00: P01 u 0.70, W01 u 1.30, T02 u 1.90 with its strip T02s, and a QUAY STREET plate at u 1.0, centre z 2.63) is kept as HELD placements, paper 150 mm clear of the pipe, for the case that he chooses the gable for the sample. No cases, no stickers. |
| SF2 | the empty unit's whitened glass (bay 3, east, number 7, street x 21 to 27) | u from the glass's viewer's-left edge, 0 to 3.562 m; z 0.60 to 2.40; the glass is street x 23.088 to 26.65 (the recipe's `fx` counts from the viewer's RIGHT: u = 3.562 x (1 - fx)) | one layer, six sheets: C01a (police appeal, four tape tabs) u 0.30 z 1.30; M01 0.75; P03 1.35; P02 1.95; J01 (A3 photocopy) 2.60; C02 (planning notice, number 7) 3.01. Whitewash shows above 2.0 m |
| WEST_PIER | six brick piers of the plain west block (street x 3 to 21), each 0.95 to 0.956 m, computed from the plain row's layout | street x of the pier's centre; z from the pavement | W1.0 (x 11.4, the scene's own poster slot): W01; W2.0: the house letting board L04. No other bill on a pier or a house front. |
| SF9 | the plain row's bay-1 window at street x 12.3 (a cottage sash, sill 0.9 m, 0.85 m wide) | street x of the window's centre, z up from the pavement | P02 as an A3 window bill: P02 x 297/508 (0.585), 297 x 446 mm, taped inside the glass, top at 1.90 m |
| SF4 | the three lamp columns, street x 8, 28, 48 (SCENE-SLOTS: every 20 m, first at 8 m, 0.6 m back from the kerb, alternate sides) | the shaft 0.114 m across; a bill wraps it: the middle 0.17 m of an A3 shows face-on | C03 and a sticker at x 8; two stickers at x 28 |
| SF5 | the empty unit's fascia (0.55 m, z 2.85 to 3.40, 0.12 proud) | centre street x 24.0 = the fascia target's board x 2705; the board z 2.90 to 3.35 | L02, the fascia target's own board (L01, a named agent, is the held alternative) |
| SF6 | first-floor brick above bay 3's cornice (3.55) and below the upper sills (about 4.3), between the two upper windows (street x 22.93 to 25.07) | centre street x 24.0, z 3.70 to 4.10 | L03n, the no-agent flat board (L03 is the held alternative) |
| SF7 | name-plate walls: the west corner pier (street x 19.92 to 21.0, brick to 3.12 m); a second plate on the quay gable at u 1.0 is held | centre z 2.63 | S01n once (the pier's). The yard entrance (street x 21 to 24, dropped kerb at 22.5) carries NO plate: `vignette-scene.json` and atlas-01 (`yard_gap_x [21, 24]`) call it the yard entrance and canon does not name it. S02 and S03 are kit plates. |
| SF8 | a quay-edge post, street x about -0.6 (PROPOSED: SCENE-SLOTS has no quay geometry) | z 1.20 up | H02, DANGER DEEP WATER |
| SHOP | eight shop fronts: glass 3.562 m, shop door 0.9, side door 0.838, pilasters 0.35 (C5, C8, C9), the door order following the fascia target's door ends | u from the glass's (or the shop door's) viewer's-left edge | the cards: section 5.7; D01 in the grocer's glass, J01 in the newsagent's beside the card board (the Tivoli programme T03, held, would stand in the ironmonger's) |

Piers (street x of the clear brick, from the recipe's bay layout; bay 1 agrees with the scene file's note that the poster slot at x 11.4 lies between a door at 10.5 and a window at 12.3):

| Pier | x0 to x1 | centre | between | placed |
|---|---|---|---|---|
| W0.0 | 4.919 to 5.875 | 5.397 | door and window | none |
| W0.1 | 6.725 to 7.675 | 7.200 | window and window | none |
| W1.0 | 10.919 to 11.875 | 11.397 | door and window | M01 z 1.00 |
| W1.1 | 12.725 to 13.675 | 13.200 | window and window | none |
| W2.0 | 16.325 to 17.275 | 16.800 | window and window | L04 z 2.15 |
| W2.1 | 18.125 to 19.081 | 18.603 | window and door | none |

The scene file's two held props are stale: its poster at west x 11.4 is the pier W1.0 and stays; its glazed case at west x 26.4 would stand on the tea room's glass (the west block is shops, not plain, from x 24). Neither case is placed at all: the Harbour Board's belongs by the dock office and the ferry's board at a ramp, and neither is built (`unplaced`).

Not placed on Quay Street, with the reason (`unplaced` in `target.json`): P04 (a spare sheet for the town (the advice evening)); B01 (held (THE DRILL HALL); a spare for the town); G01 (held (WHITEWELL); a national four-sheet belongs in a contractor's panel); G02 (held (QUAYSIDE)); T01 (held: a nameless stand-in, with T01-named); T01s (the strip of T01, which is not placed); F01 (on FC1); F02 (under F01 on FC1); H01 (a gate or wall of the docks: not built); H03 (pinned in HC1); H04 (pinned in HC1); H05 (pinned in HC1); C01b (a slot filler: the simulation's other appeals); C01c (a slot filler); K01 (for a shop that shuts for lunch: none on the built street does (hook-cast hours)); K02 (the newsagent never closes at midday (hook-cast 6 to 17.30) and Hal's shop is not on the built street); K03b (the CLOSED face of K03a, shown when the shop is shut); S01d (a variant of S01n); S02n (a kit plate: no street plate on the yard entrance); S02d (a kit plate); S03n (a kit plate); S03d (a kit plate); HC1 (by the dock office (brand bible; hook-cast harbour_office): neither is built); FC1 (at each ramp (brand bible): the ramp is not built).

## 3. Sizes, stocks, processes and what they look like

British paper sizes of the period (Derived from the imperial names: 25.4 mm to the inch; the Double Crown 20 x 30 in is a Lead from a search summary).

| Name | mm | used for |
|---|---|---|
| crown | 381 x 508 | (none now: J01 is an A3 photocopy) |
| double_crown | 508 x 762 | the poll-tax, fight, market, tea and programme bills |
| quad_crown | 1016 x 762 | T01, T02 (landscape, 'the quad') |
| four_sheet | 1016 x 1524 | G01 (held, not placed) |
| A3 | 297 x 420 | police and road-closure notices; the jumble-sale and dance notices (photocopies) |
| A4 | 210 x 297 | the advice sheet, planning notice, three Harbour Board notices |
| A5 | 148 x 210 | (portrait, not used) |
| A6 | 105 x 148 | (portrait, not used) |
| A2 | 420 x 594 | F01, F02 (the ferry sheets) |
| A5L | 210 x 148 | cards K01, K05, K06 a and b, K08 |
| A6L | 148 x 105 | K06c, SA15 |

Processes, in plain words (the numbers are in `processes`):

- **screen_2col**: two-colour screen print on fluorescent stock; registration_offset_mm [0.3, 0.8]; lead: Hackney Museum holds a 1990 'Pay No Poll Tax' single sheet on yellow paper with red ink (search summary, unreached page): the colour way is the lead
- **screen_1col**: one-colour screen print on fluorescent stock
- **letterpress_2col**: two-colour letterpress from metal and wood type (a small jobbing printer); registration_offset_mm [0.3, 0.7]; impression_mm [0.1, 0.18]
- **litho_4col**: four-colour offset litho, a quad or four-sheet
- **litho_2col**: two-colour offset litho; registration_offset_mm [0.1, 0.3]
- **photocopy_a4**: photocopy on A4; toner_density 0.92
- **photocopy_a3**: photocopy on A3; toner_density 0.92
- **typed_carbon**: electric typewriter, then photocopied or used as the top copy; pitch Courier 10 characters to the inch (2.54 mm), 12 point; lead: by 1990 an office letter is a crisp daisy-wheel or golfball impression (period note PERIOD-PRINT-AND-FONTS, 1 Oct)
- **felt_pen**: felt-tip marker on card
- **ballpoint_card**: ballpoint on a record card, felt-tip heading
- **sticker_print**: printed self-adhesive label or sticker, die-cut
- **plastic_print**: screen-printed plastic card on a chain
- **enamel**: vitreous enamel on pressed steel; roughness 0.12; thickness_mm 1.6; edge_roll_radius_mm 6.0; lead: the Harbour Board's 'blue and white enamel signage on gates, cranes and the weighbridge' (content/brands/brand-bible-v1.json)
- **agent_board**: painted exterior plywood, sign-written or screen-printed vinyl; roughness 0.35
- **cast_aluminium_raised**: cast aluminium, letters and border raised 3 mm, painted white with black letters (by the 1950s raised plates were cast aluminium, not iron: TARGET-REVIEW fault 13); roughness 0.5; relief_mm 3.0; draft_deg 10.0; top_radius_mm 0.8; lead: Hull's cast plates of the 1920s were black on white and the paint faded or flaked, needing regular repainting (search summary of a Geograph caption); a Lead only: that was iron
- **pressed_aluminium_enamel**: die-pressed aluminium sheet, letters and border raised 1.5 mm, stove enamelled black on white; roughness 0.3; relief_mm 1.5; draft_deg 10.0; top_radius_mm 0.8; thickness_mm 2.0; edge_roll_radius_mm 3.0; lead: current specs: 11 SWG aluminium, die-pressed, stove-enamelled (South Kesteven, Charnwood: search summaries)
- **vitreous_enamel_steel**: vitreous enamel on pressed steel, rolled edge of 6 mm radius; roughness 0.12; edge_roll_radius_mm 6.0
- **letterpress_1col**: one-colour letterpress from metal type (a pasted venue strip); impression_mm [0.1, 0.18]

The look in one paragraph per kind (all Judgement unless a lead is named):

- **Fly-posters** are two-colour jobs from a small jobbing printer: black and one colour on cheap uncoated poster paper, white or tinted or fluorescent, set in a mixture of faces with thick rules and a printer's imprint in 7-point at the foot. Letterpress bills show a darker rim at the letter edges and a faint relief; screen-printed ones are flat and a little thick; the second colour sits 0.3 to 0.8 mm off register. The poll-tax bills use fluorescent yellow and orange stock because the one 1990 sheet found is yellow in red ink (a Lead).
- **Quads** are offset litho in full colour on uncoated paper and carry NO venue: the cinema pasted its own letterpress strip (black on white, 1016 x 90) across the top band. The halftone is not resolved at the item's scale, so they are drawn as continuous tone with grain; the image model makes the picture only (no words, no people, no crown, kiosk, bottle, glass or arcade sign: `ART.eye`), our text layer lays every letter, and a dark scrim guarantees the contrast of the lines on the art.
- **Photocopies** (the advice sheet, the jumble-sale and dance notices, the police appeals, the planning and road notices) are hard black toner on white or tinted copier paper: a grey band 3 to 6 mm along one edge, speckle, a crooked copy (the placement's rot_deg), a vertical streak or two. Planning and road notices sit in a clear polythene sleeve; the A3 notices in a window are taped by four tabs of yellowed tape.
- **Typed notices** (the Harbour Board's) are Courier Prime, 10 characters to the inch, an electric typewriter's even impression, pinned in a glass case with drawing pins, curling (held until the case is built).
- **Hand-lettered cards** are felt pen (a fat even line, a darker blob where the nib rested) in Patrick Hand capitals, and ballpoint (a thin line, lighter on the joins) on white or tinted record cards; each is TAPED by one tab at its top-left corner or hung on a string and a sucker, and slightly crooked.
- **Stickers** are printed paper labels, die-cut, edges lifting and scratched.
- **Enamel signs** are vitreous enamel on pressed steel: gloss, a rolled edge of 6 mm radius, chips to black steel with a rust halo at the corners and the bolts.

## 4. Stocks, inks, paints and ageing

Four classes by days on the wall: **A** fresh (0 to 7 days), **B** weeks (8 to 35), **C** months (36 to 120), **D** old (over 120). A colour fades by f = 1 - exp(-t / tau) (tau in days, per ink or stock) towards the paper, the paper yellows (30 per cent of the way to (214,200,168) at class D), and a grime film (62,58,52) mixes in at 0, 5, 12 and 22 per cent (35 per cent of that over ink). The order of fastness (Judgement) is fluorescent stock, then red, blue, black, toner.

**The street date is Monday 29 October 1990** (`calendar.street_date`): a day every placed dated item allows (GMT began on the 28th; the held proof wall's P01 and T02 allow it too: the meeting of the 25th is four days gone, the film started on Thursday 25). `G.dates.age` fails a placed dated item unless some age in its class's days posts it no more than 42 days before its event and no later than it (a notice: no earlier than its date). The ages that follow: P01 B (held; the 25 October meeting is four days gone: a stale bill), W01 A (held, on the gable), T02 A (held; up since the 25th), T03 B (held), D01 B, J01 B (the 20 October sale is nine days gone: stale), P03 B, C01a B (the night of 12 October), C02 A, M01 C on the glass and B on the pier. The first try's contradictions (T03 in class D under T01 in class A for the same week; D01 in class C for a 17 November dance) are tested and fail.

| Stock | fresh | A | B | C | D | tau |
|---|---|---|---|---|---|---|
| white poster paper | (236,235,228) | (236,235,228) | (226,224,215) | (212,209,199) | (192,187,175) | none |
| white copier paper, A4 or A3 | (240,240,234) | (240,240,234) | (229,229,221) | (215,213,203) | (195,191,178) | none |
| cream poster paper | (236,226,196) | (236,226,196) | (226,216,187) | (212,202,175) | (192,183,158) | none |
| fluorescent yellow poster paper | (250,238,52) | (249,237,57) | (235,224,80) | (215,206,117) | (192,183,131) | 60 |
| fluorescent orange poster paper | (255,120,52) | (254,123,56) | (240,135,77) | (218,152,107) | (195,155,120) | 60 |
| pale pink poster paper | (240,206,210) | (240,206,210) | (229,200,199) | (214,191,187) | (193,177,167) | 150 |
| pale green copier paper | (204,226,202) | (204,226,202) | (199,216,194) | (192,203,181) | (181,184,164) | 200 |
| pale yellow copier paper | (246,238,176) | (246,238,176) | (234,226,171) | (218,210,166) | (195,187,155) | 150 |
| pale blue poster paper | (204,220,238) | (204,220,238) | (199,212,224) | (192,200,205) | (181,183,178) | 200 |
| white card, about 250 gsm | (242,240,232) | (242,240,232) | (231,229,219) | (217,213,202) | (196,191,178) | none |
| buff card, about 250 gsm | (224,204,160) | (224,204,160) | (215,197,155) | (203,186,148) | (186,171,138) | none |
| white record card | (244,242,234) | (244,242,234) | (233,230,221) | (219,215,203) | (197,191,178) | none |
| pink record card | (240,196,204) | (240,196,204) | (229,191,195) | (214,186,183) | (193,173,165) | 150 |
| blue record card | (196,214,236) | (196,214,236) | (192,206,222) | (188,196,203) | (179,180,178) | 200 |
| yellow record card | (246,232,150) | (246,232,151) | (234,221,151) | (218,206,151) | (195,186,149) | 150 |
| green record card | (196,226,196) | (196,226,196) | (192,216,188) | (189,203,178) | (180,184,162) | 200 |
| fluorescent yellow star card | (252,240,40) | (251,239,46) | (237,225,75) | (216,205,114) | (194,183,126) | 50 |
| fluorescent pink star card | (255,92,140) | (254,97,142) | (238,122,148) | (217,151,154) | (194,155,147) | 45 |
| fluorescent orange star card | (255,130,40) | (254,133,45) | (239,144,72) | (217,159,109) | (194,157,121) | 50 |

| Ink | fresh | tau (days) |
|---|---|---|
| black ink | (24,24,27) | 1500 |
| poster red | (196,34,38) | 150 |
| poster blue | (28,58,138) | 400 |
| navy | (26,38,82) | 900 |
| photocopier toner | (30,30,33) | 4000 |
| typewriter ribbon, black | (34,34,38) | 1500 |
| felt pen, black | (30,30,36) | 900 |
| felt pen, red | (200,32,40) | 120 |
| felt pen, blue | (28,62,150) | 300 |
| felt pen, green | (24,110,60) | 300 |
| ballpoint, blue | (30,52,150) | 250 |
| ballpoint, black | (40,40,46) | 900 |

| Paint | fresh | B | D |
|---|---|---|---|
| vitreous enamel, white | (238,238,230) | (227,226,217) | (191,187,175) |
| vitreous enamel, Harbour Board blue | (24,68,140) | (36,74,136) | (70,91,124) |
| vitreous enamel, red | (176,30,34) | (172,39,42) | (156,69,64) |
| vitreous enamel, black | (20,20,22) | (32,31,30) | (67,63,57) |
| plate paint, white, oil gloss gone satin | (232,230,220) | (222,219,208) | (188,182,169) |
| plate paint, black | (22,22,26) | (34,32,34) | (68,64,60) |
| agent's board, white gloss | (236,236,230) | (225,224,217) | (189,186,175) |
| agent's navy | (28,46,94) | (38,54,95) | (71,78,97) |
| agent's red | (178,34,40) | (174,43,46) | (157,72,67) |
| OPEN face, green | (30,92,66) | (40,95,70) | (73,104,82) |
| lamplight orange, the Tivoli's title colour on dark art | (240,170,64) | (229,166,68) | (192,149,81) |
| varnished timber, dark | (74,50,34) | (80,58,42) | (98,81,64) |
| cork board | (176,138,96) | (172,136,97) | (156,131,99) |
| polythene sleeve highlight | (226,230,232) | (216,219,219) | (184,182,176) |
| printed adhesive vinyl, white | (238,238,232) | (227,226,219) | (191,187,176) |
| vinyl red (the fascia target's vinyl_red, 176,30,34) | (176,30,34) | (172,39,42) | (156,69,64) |
| brass paper-fastener | (176,140,60) | (172,138,64) | (156,132,79) |

Paper wear (numbers for the builder; Judgement): wrinkles of 0.4 to 1.5 mm, wavelength 12 to 40 mm, from wallpaper-paste cockling, strongest along the brush direction (vertical); corners lifting 0 to 3 of radius 15 to 60 mm (none at class A, three at D); tears 0 to 4 of width 20 to 140 mm from an edge; rain runs 2 to 8 a metre, 10 to 60 mm long, 0.4 to 1.5 mm wide, opacity 0.15 to 0.4, down from the top edge and from any lifted corner, the red and dye inks running first; a paste halo 2 to 10 mm at class C and D; share of the sheet lost 0 to 0.05 at B, 0.03 to 0.2 at C, 0.3 to 0.6 at D, the lower corners first; skew only in the placement (-1.5 to +1.5 degrees); the quay gable's bills are one layer (no overposting there). A wet wall darkens paper by 12 per cent and raises saturation by 10 per cent (a runtime hint).

Wear tables by kind (`wear_tables`): bill_pasted; glass_bill; notice_sleeve; card_felt; card_ballpoint; sticker; enamel_plate; cast_aluminium_plate; pressed_plate; letting_board; case.

## 4b. Type

13 font files from 10 families, **all SIL OFL 1.1, every family's OFL.txt read whole on raw.githubusercontent.com** (the first try also read UnifrakturMaguntia's, Arimo's, Libre Baskerville's, Josefin Sans's and Abril Fatface's and Liberation's LICENSE; none is used now). Letters are RENDERED into pictures: the OFL puts no restriction on a picture made with a font. The font files themselves are NOT copied into `production/fonts` here.

| Key | Family | Used for | In production/fonts | RFN |
|---|---|---|---|---|
| marcellus-sc | Marcellus SC | S01d, S01n, S02d, S02n, S03d, S03n | yes | Marcellus |
| oswald | Oswald | B01, D01, D01-named, F01, F02, G01, G02, J01 ... (26 items) | yes | none |
| jost | Jost | L01, L03, L03n, L04 | yes | none |
| libre-franklin | Libre Franklin | B01, D01, D01-named, F01, G01, G02, J01, L02 ... (19 items) | yes | none |
| alfa-slab-one | Alfa Slab One | B01, D01, D01-named, F01, F02, G01, G02, K02 ... (9 items) | yes | Alfa Slab |
| fraunces | Fraunces | G02, T01, T01-named, T02, T02-named | yes | none |
| old-standard-tt | Old Standard TT | D01, D01-named, H03, H04, H05, J01 | yes | none |
| old-standard-tt-regular | Old Standard TT | C02, C03, J01 | yes | none |
| old-standard-tt-italic | Old Standard TT | D01, D01-named, J01, W01-named | yes | none |
| archivo | Archivo | C01a, C01b, C01c, C02, C03, H01, H02, K03a ... (13 items) | NO: add with its OFL.txt | none |
| courier-prime | Courier Prime | H03, H04, H05, P04 | NO: add with its OFL.txt | none |
| courier-prime-bold | Courier Prime | H03, H04, H05 | NO: add with its OFL.txt | none |
| patrick-hand | Patrick Hand | K01, K05, K06a, K06c, K07a, K07b, K07c, K07d ... (29 items) | yes | none |

Three are not in `production/fonts` (Archivo, Courier Prime Regular and Bold); `self_check.py --fetch-fonts DIR` fetches them and the OFL texts. The old bills used League Gothic (in the repository, an OFL face, and on the asset plan's table): this target uses Oswald, also on the table, because its weight axis lets one file carry 500, 600 and 700. Overpass is never used. No UnifrakturMaguntia: a masthead would name a local paper, which canon owes.

**Fonts off the asset plan's table (note 4, A2), and the decision for each.** The second try removed Libre Baskerville (typeset notices now use Old Standard TT Regular and Bold, the table's 'Old Standard'), Josefin Sans (the Tivoli's strip and programme use Oswald, the table's 'the Tivoli's letters') and the never-used Abril Fatface. Two remain, each with the line to append to DECISIONS.md (the target may not edit it):

- **Libre Franklin**: not on asset-plan note 4's table (Helvetica and Arial stand-ins: Arimo, Inter, Archivo, Hanken Grotesk, Work Sans). Why: the fascia target (same batch) already sets the letting board's TO LET in Libre Franklin 800; this target compares L02 with it, and Libre Franklin is in production/fonts; Franklin Gothic is also the right 1990 newsagent and notice face. DECISIONS.md line: `9 Oct 2026 | Libre Franklin (OFL, already in production/fonts) is used for notice, card and bill copy and the letting board's TO LET, though not on asset-plan note 4's font table | the fascia target already does; Franklin Gothic is the period face | the cloud's target writer | production/cloud-week/targets/posters-boards-plates/TARGET.md`
- **Patrick Hand**: not on the table (Caveat Brush, Kalam, Gochi Hand are the 'hand-marked tickets and bills' faces). Why: Patrick Hand is a neat adult print capital with plain figures, which is what a shopkeeper's felt-pen ticket and a ballpoint record card are; Kalam and Caveat Brush are slanted and read as script, and the reviewer notes they look more like a felt marker; Patrick Hand is already in production/fonts. Judgement: the town may swap the hand face without touching the checks (they read whatever face the manifest names). DECISIONS.md line: `9 Oct 2026 | Patrick Hand (OFL, already in production/fonts) is the hand-lettering face for felt-pen cards and ballpoint record cards, though the asset plan's table names Caveat Brush, Kalam and Gochi Hand | neat print capitals and plain figures read as a shopkeeper's felt pen; the table's faces are scripts | the cloud's target writer | production/cloud-week/targets/posters-boards-plates/TARGET.md`

## 5. The items, word by word (unit 4.2)

Each line: the exact words, the font and weight, the cap height in millimetres, the anchor and x, the baseline y, the ink, and the contrast of ink on ground in class B. Anchors are of the INK, not the advance box. Every width is measured on the real font file; every box is in `target.json` (`ink_box_mm`). Each item shows its pixel scale and, if it is held, the names that hold it.

### 5.1 The poll-tax set

An INVENTED LOCAL CAMPAIGN (ruling 3 October): no party, no person, no real group, no real logo. The name `MERIDIAN AGAINST THE POLL TAX` is proposed, not minted, so the DEFAULT bills P01 to P03 carry the generic STAND TOGETHER where the held `-named` twins carry the campaign (21 to 24 mm capitals); the 2.4 mm imprint, the 3.6 to 6 mm lines on P04 to P06 and the printer's imprint (QUAY PRINT) stay: they are under the 10 mm line and illegible from across the street. The slogan CAN'T PAY - WON'T PAY is a common slogan (and the title of a 1974 play), not a party's mark: the reviewer says keep it. Autumn 1990 is the summons season, so the bills are about meetings, a march and what to do with a summons. Dates: Thursday 25 October (meeting), Tuesday 30 October (advice), Saturday 10 November (march).

#### P01  Poll tax: public meeting bill

- 508 x 762 mm (double_crown); 3 px/mm; stock: fluorescent yellow poster paper; process: screen_2col; event: THURSDAY 25 OCTOBER; dated: event 1990-10-25
- variants: 3 (age class A, B, C; red pass shifted 0.3 to 0.8 mm; one has a top corner torn 60 to 140 mm; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_top (rule): box [40, 420.5, 468, 425.5], fill black
- shape rule_mid (rule): box [40, 160.0, 468, 165.0], fill black
- shape footer_bar (rect): box [18, 30, 490, 82], fill black
  - `NO` | oswald 700 | cap 190 | centre 254 | base 548 | black | B 12.52
  - `POLL TAX` | oswald 700 | cap 97.5 | centre 254 | base 438.5 | red | B 3.84
  - `PUBLIC MEETING` | oswald 600 | cap 34 | centre 254 | base 374.5 | black | B 12.52
  - `THURSDAY 25 OCTOBER` | oswald 700 | cap 32.5 | centre 254 | base 328 | red | B 3.84
  - `7.30 PM` | oswald 700 | cap 76 | centre 254 | base 238 | black | B 12.52
  - `THE CHAPEL HALL` | oswald 600 | cap 38 | centre 254 | base 184 | black | B 12.52
  - `WHAT TO DO IF YOU GET A SUMMONS` | libre-franklin 800 | cap 14.5 | centre 254 | base 135.5 | black | B 12.52
  - `EVERYONE WELCOME` | libre-franklin 700 | cap 15 | centre 254 | base 112.5 | black | B 12.52
  - `STAND TOGETHER` | oswald 600 | cap 23.4 | centre 254 | base 44.3 | paper | B 12.52
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 20 | black | B 12.52

#### P01-named  Poll tax: public meeting bill (named campaign, held)

- 508 x 762 mm (double_crown); 3 px/mm; stock: fluorescent yellow poster paper; process: screen_2col; event: THURSDAY 25 OCTOBER; dated: event 1990-10-25; HELD until minted: MERIDIAN AGAINST THE POLL TAX
- variants: 3 (age class A, B, C; red pass shifted 0.3 to 0.8 mm; one has a top corner torn 60 to 140 mm; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_top (rule): box [40, 420.5, 468, 425.5], fill black
- shape rule_mid (rule): box [40, 160.0, 468, 165.0], fill black
- shape footer_bar (rect): box [18, 30, 490, 82], fill black
  - `NO` | oswald 700 | cap 190 | centre 254 | base 548 | black | B 12.52
  - `POLL TAX` | oswald 700 | cap 97.5 | centre 254 | base 438.5 | red | B 3.84
  - `PUBLIC MEETING` | oswald 600 | cap 34 | centre 254 | base 374.5 | black | B 12.52
  - `THURSDAY 25 OCTOBER` | oswald 700 | cap 32.5 | centre 254 | base 328 | red | B 3.84
  - `7.30 PM` | oswald 700 | cap 76 | centre 254 | base 238 | black | B 12.52
  - `THE CHAPEL HALL` | oswald 600 | cap 38 | centre 254 | base 184 | black | B 12.52
  - `WHAT TO DO IF YOU GET A SUMMONS` | libre-franklin 800 | cap 14.5 | centre 254 | base 135.5 | black | B 12.52
  - `EVERYONE WELCOME` | libre-franklin 700 | cap 15 | centre 254 | base 112.5 | black | B 12.52
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 23.4 | centre 254 | base 44.3 | paper | B 12.52
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 20 | black | B 12.52

#### P02  Poll tax: don't pay bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: fluorescent orange poster paper; process: screen_1col
- variants: 3 (age class A, B, C; one overposted by P03 over its lower third; skew is the PLACEMENT's rot_deg only: every texture is square-on; the A3 window version (placement scale 0.585: 297 x 446 mm, taped inside the glass) is this texture scaled by the placement, not a new item)
- shape rule_a (rule): box [30, 293.0, 478, 299.0], fill black
- shape footer_bar (rect): box [18, 30, 490, 82], fill black
  - `DON’T` | oswald 700 | cap 154 | centre 254 | base 584 | black | B 6.82
  - `PAY` | oswald 700 | cap 184 | centre 254 | base 390 | black | B 6.82
  - `THE POLL TAX` | oswald 700 | cap 61 | centre 254 | base 311 | black | B 6.82
  - `CAN’T PAY — WON’T PAY` | oswald 600 | cap 34.5 | centre 254 | base 242.5 | black | B 6.82
  - `JOIN US EVERY THURSDAY` | libre-franklin 800 | cap 19 | centre 254 | base 175.3 | black | B 6.82
  - `7.30 PM · THE CHAPEL HALL` | libre-franklin 800 | cap 19 | centre 254 | base 130 | black | B 6.82
  - `STAND TOGETHER` | oswald 600 | cap 23.4 | centre 254 | base 44.3 | paper | B 6.82
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 20 | black | B 6.82

#### P02-named  Poll tax: don't pay bill (named campaign, held)

- 508 x 762 mm (double_crown); 2 px/mm; stock: fluorescent orange poster paper; process: screen_1col; HELD until minted: MERIDIAN AGAINST THE POLL TAX
- variants: 3 (age class A, B, C; one overposted by P03 over its lower third; skew is the PLACEMENT's rot_deg only: every texture is square-on; the A3 window version (placement scale 0.585: 297 x 446 mm, taped inside the glass) is this texture scaled by the placement, not a new item)
- shape rule_a (rule): box [30, 293.0, 478, 299.0], fill black
- shape footer_bar (rect): box [18, 30, 490, 82], fill black
  - `DON’T` | oswald 700 | cap 154 | centre 254 | base 584 | black | B 6.82
  - `PAY` | oswald 700 | cap 184 | centre 254 | base 390 | black | B 6.82
  - `THE POLL TAX` | oswald 700 | cap 61 | centre 254 | base 311 | black | B 6.82
  - `CAN’T PAY — WON’T PAY` | oswald 600 | cap 34.5 | centre 254 | base 242.5 | black | B 6.82
  - `JOIN US EVERY THURSDAY` | libre-franklin 800 | cap 19 | centre 254 | base 175.3 | black | B 6.82
  - `7.30 PM · THE CHAPEL HALL` | libre-franklin 800 | cap 19 | centre 254 | base 130 | black | B 6.82
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 23.4 | centre 254 | base 44.3 | paper | B 6.82
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 20 | black | B 6.82

#### P03  Poll tax: march bill

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col; event: SATURDAY 10 NOVEMBER; dated: event 1990-11-10
- variants: 3 (age class A, B, C; ink density; overposted by P01 at the foot in one; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape bar_left (rect): box [18, 100, 46, 744], fill red
- shape footer_bar (rect): box [64, 30, 490, 82], fill black
  - `MARCH` | oswald 700 | cap 117 | left 64 | base 621 | red | B 3.99
  - `AGAINST THE` | oswald 600 | cap 40 | left 64 | base 569 | black | B 13.0
  - `POLL TAX` | oswald 700 | cap 92 | left 64 | base 469 | black | B 13.0
  - `SATURDAY` | oswald 700 | cap 62 | left 64 | base 367 | black | B 13.0
  - `10 NOVEMBER` | oswald 700 | cap 58.5 | left 64 | base 298.5 | black | B 13.0
  - `ASSEMBLE 11 AM` | oswald 600 | cap 37.5 | left 64 | base 237 | black | B 13.0
  - `THE EXCHANGE` | oswald 600 | cap 42 | left 64 | base 185 | black | B 13.0
  - `BRING YOUR NEIGHBOURS` | libre-franklin 800 | cap 20 | left 64 | base 141 | red | B 3.99
  - `BRING A BANNER` | libre-franklin 800 | cap 20 | left 64 | base 113 | red | B 3.99
  - `STAND TOGETHER` | oswald 600 | cap 23.4 | centre 277 | base 44.3 | paper | B 13.0
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 277 | base 20 | black | B 13.0

#### P03-named  Poll tax: march bill (named campaign, held)

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col; event: SATURDAY 10 NOVEMBER; dated: event 1990-11-10; HELD until minted: MERIDIAN AGAINST THE POLL TAX
- variants: 3 (age class A, B, C; ink density; overposted by P01 at the foot in one; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape bar_left (rect): box [18, 100, 46, 744], fill red
- shape footer_bar (rect): box [64, 30, 490, 82], fill black
  - `MARCH` | oswald 700 | cap 117 | left 64 | base 621 | red | B 3.99
  - `AGAINST THE` | oswald 600 | cap 40 | left 64 | base 569 | black | B 13.0
  - `POLL TAX` | oswald 700 | cap 92 | left 64 | base 469 | black | B 13.0
  - `SATURDAY` | oswald 700 | cap 62 | left 64 | base 367 | black | B 13.0
  - `10 NOVEMBER` | oswald 700 | cap 58.5 | left 64 | base 298.5 | black | B 13.0
  - `ASSEMBLE 11 AM` | oswald 600 | cap 37.5 | left 64 | base 237 | black | B 13.0
  - `THE EXCHANGE` | oswald 600 | cap 42 | left 64 | base 185 | black | B 13.0
  - `BRING YOUR NEIGHBOURS` | libre-franklin 800 | cap 20 | left 64 | base 141 | red | B 3.99
  - `BRING A BANNER` | libre-franklin 800 | cap 20 | left 64 | base 113 | red | B 3.99
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 21.5 | centre 277 | base 45.2 | paper | B 13.0
  - `Published by Meridian Against the Poll Tax. Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 277 | base 20 | black | B 13.0

#### P04  Poll tax: summons advice sheet (photocopy)

- 210 x 297 mm (A4); 12 px/mm; stock: pale green copier paper; process: photocopy_a4; event: TUESDAY 30 OCTOBER; dated: event 1990-10-30
- variants: 3 (paper: pale green, pale yellow, white; toner speckle and a copier edge shadow; skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape rule_a (rule): box [12, 184.0, 198, 185.6], fill toner
  - `GOT A POLL TAX` | archivo 900 | cap 14.5 | centre 105 | base 269.5 | toner | B 10.96
  - `SUMMONS?` | archivo 900 | cap 19.5 | centre 105 | base 232.8 | toner | B 10.96
  - `DON’T PANIC.` | archivo 900 | cap 14 | centre 105 | base 190 | toner | B 10.96
  - `ADVICE EVENING` | archivo 800 | cap 11 | left 16 | base 161 | toner | B 10.96
  - `TUESDAY 30 OCTOBER, 7 PM` | archivo 800 | cap 8.5 | left 16 | base 146.5 | toner | B 10.96
  - `THE CHAPEL HALL` | archivo 800 | cap 8.5 | left 16 | base 133 | toner | B 10.96
  - `Bring your summons and any letters you have had.` | courier-prime 400 | cap 2.455 | left 16 | base 115 | toner | B 10.96
  - `We will go through them with you.` | courier-prime 400 | cap 2.455 | left 16 | base 106.5 | toner | B 10.96
  - `Free and confidential. Come on your own` | courier-prime 400 | cap 2.455 | left 16 | base 98.1 | toner | B 10.96
  - `or bring a neighbour.` | courier-prime 400 | cap 2.455 | left 16 | base 89.6 | toner | B 10.96
  - `MERIDIAN AGAINST THE POLL TAX` | archivo 800 | cap 6 | centre 105 | base 22 | toner | B 10.96

#### P05  Poll tax: sticker, 95 x 60

- 95 x 60 mm (own size); 12 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (on a lamp column, pillar, kiosk or wall: corners lifting, one scratched, one half scraped)
- shape frame (frame): box [2, 2, 93, 58], fill red
  - `NO` | oswald 700 | cap 20 | centre 47.5 | base 34 | red | B 3.99
  - `POLL TAX` | oswald 700 | cap 15.5 | centre 47.5 | base 15.5 | black | B 13.0
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 3.6 | centre 47.5 | base 7 | black | B 13.0

#### P06  Poll tax: sticker, 148 x 52

- 148 x 52 mm (own size); 12 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (as P05)
- shape bar (rect): box [2, 2, 146, 50], fill black
  - `CAN’T PAY — WON’T PAY` | oswald 700 | cap 10 | centre 74 | base 24 | paper | B 13.0
  - `MERIDIAN AGAINST THE POLL TAX` | oswald 600 | cap 4 | centre 74 | base 10 | paper | B 13.0

### 5.2 The chapel hall (the game's `chapel_hall`)

`THE CHAPEL HALL` is the game's own place (`hook-cast.json`, Father Walsh's chapel and its hall); no street is minted for it, so the notices name none. Religion appears as part of life, never mocked: the jumble sale is in aid of the chapel roof fund. No raffle, no bingo, no drink (`TEA AND SANDWICHES`), no children (`ALL WELCOME`, never 'families'). **Both notices are photocopied A3 sheets** (asset-plan note 4: a 1990 jumble-sale notice 'is Letraset, photocopy or two-colour screen print'): J01 is taped inside the newsagent's glass beside the card board and on the empty unit's glass, D01 inside the grocer's glass. The dance is OLD TIME and SEQUENCE DANCING (not NEW VOGUE, the Australian name). The band, THE SANDERLING TRIO, is a placeholder: the default D01 says LIVE MUSIC.

#### J01  Jumble sale notice (chapel hall), A3 photocopy

- 297 x 420 mm (A3); 4 px/mm; stock: pale pink poster paper; process: photocopy_a3; event: SATURDAY 20 OCTOBER; dated: event 1990-10-20
- variants: 3 (age class A, B; toner density and edge shadow (processes.photocopy_a3); one half-covered by P03 or W01 (never placed so by default); skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape frame (frame): box [8, 8, 289, 412], fill toner - two rules photocopied from a printed original, 2.4 mm; hairline gaps at the corner joints
- shape rule_a (rule): box [24, 278.0, 273, 280.6], fill toner
  - `GRAND` | old-standard-tt 700 | cap 22 | centre 148.5 | base 380 | toner | B 10.48
  - `JUMBLE SALE` | oswald 700 | cap 36.5 | centre 148.5 | base 327.4 | toner | B 10.48
  - `THE CHAPEL HALL` | oswald 600 | cap 16 | centre 148.5 | base 290 | toner | B 10.48
  - `SATURDAY 20 OCTOBER` | oswald 700 | cap 18.5 | centre 148.5 | base 251.5 | toner | B 10.48
  - `DOORS OPEN 2 PM` | oswald 600 | cap 15 | centre 148.5 | base 210.1 | toner | B 10.48
  - `CLOTHING · BOOKS · BRIC-A-BRAC · HOUSEHOLD` | old-standard-tt-regular 400 | cap 6.5 | centre 148.5 | base 164 | toner | B 10.48
  - `Teas and cakes` | old-standard-tt-italic 400 | cap 10 | centre 148.5 | base 121 | toner | B 10.48
  - `ADMISSION 20p` | libre-franklin 800 | cap 11 | centre 148.5 | base 70.4 | toner | B 10.48
  - `IN AID OF THE CHAPEL ROOF FUND` | libre-franklin 700 | cap 8 | centre 148.5 | base 36 | toner | B 10.48
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 148.5 | base 17 | black | B 10.99

#### D01  Old-time and sequence dance notice (chapel hall), A3 photocopy

- 297 x 420 mm (A3); 4 px/mm; stock: pale yellow copier paper; process: photocopy_a3; event: SATURDAY 17 NOVEMBER; dated: event 1990-11-17
- variants: 3 (age class A, B; toner density and edge shadow; skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape frame (frame): box [8, 8, 289, 412], fill toner - a double-width rule photocopied from a printed original
  - `OLD TIME` | old-standard-tt 700 | cap 32 | centre 148.5 | base 370 | toner | B 12.47
  - `and` | old-standard-tt-italic 400 | cap 15 | centre 148.5 | base 350 | toner | B 12.47
  - `SEQUENCE` | old-standard-tt 700 | cap 29.5 | centre 148.5 | base 316.5 | toner | B 12.47
  - `DANCING` | alfa-slab-one 400 | cap 33.5 | centre 148.5 | base 269 | toner | B 12.47
  - `SATURDAY 17 NOVEMBER` | oswald 700 | cap 16.5 | centre 148.5 | base 228.5 | toner | B 12.47
  - `7.30 TO 11 PM` | oswald 600 | cap 24 | centre 148.5 | base 189.6 | toner | B 12.47
  - `THE CHAPEL HALL` | oswald 600 | cap 17 | centre 148.5 | base 155.7 | toner | B 12.47
  - `LIVE MUSIC` | old-standard-tt 700 | cap 18.5 | centre 148.5 | base 111.1 | toner | B 12.47
  - `TEA AND SANDWICHES` | libre-franklin 800 | cap 9.5 | centre 148.5 | base 75.4 | toner | B 12.47
  - `ADMISSION £1.50` | libre-franklin 800 | cap 9.5 | centre 148.5 | base 54.7 | toner | B 12.47
  - `ALL WELCOME` | libre-franklin 800 | cap 9.5 | centre 148.5 | base 34 | toner | B 12.47
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 148.5 | base 17 | black | B 13.04

#### D01-named  Old-time and sequence dance notice (chapel hall), A3 photocopy (named band, held)

- 297 x 420 mm (A3); 4 px/mm; stock: pale yellow copier paper; process: photocopy_a3; event: SATURDAY 17 NOVEMBER; dated: event 1990-11-17; HELD until minted: THE SANDERLING TRIO
- variants: 3 (age class A, B; toner density and edge shadow; skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape frame (frame): box [8, 8, 289, 412], fill toner - a double-width rule photocopied from a printed original
  - `OLD TIME` | old-standard-tt 700 | cap 32 | centre 148.5 | base 370 | toner | B 12.47
  - `and` | old-standard-tt-italic 400 | cap 15 | centre 148.5 | base 350 | toner | B 12.47
  - `SEQUENCE` | old-standard-tt 700 | cap 29.5 | centre 148.5 | base 316.5 | toner | B 12.47
  - `DANCING` | alfa-slab-one 400 | cap 33.5 | centre 148.5 | base 269 | toner | B 12.47
  - `SATURDAY 17 NOVEMBER` | oswald 700 | cap 16.5 | centre 148.5 | base 228.5 | toner | B 12.47
  - `7.30 TO 11 PM` | oswald 600 | cap 24 | centre 148.5 | base 191.3 | toner | B 12.47
  - `THE CHAPEL HALL` | oswald 600 | cap 17 | centre 148.5 | base 159.4 | toner | B 12.47
  - `Music by` | old-standard-tt-italic 400 | cap 11 | centre 148.5 | base 125.2 | toner | B 12.47
  - `THE SANDERLING TRIO` | old-standard-tt 700 | cap 11.5 | centre 148.5 | base 105.5 | toner | B 12.47
  - `TEA AND SANDWICHES` | libre-franklin 800 | cap 9.5 | centre 148.5 | base 72.8 | toner | B 12.47
  - `ADMISSION £1.50` | libre-franklin 800 | cap 9.5 | centre 148.5 | base 53.4 | toner | B 12.47
  - `ALL WELCOME` | libre-franklin 800 | cap 9.5 | centre 148.5 | base 34 | toner | B 12.47
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 148.5 | base 17 | black | B 13.04

### 5.3 The fights, the market and the goods

The wrestling bill W01 names no ring names and no hall (it reads PROFESSIONAL WRESTLING, a heavyweight contest, a tag team contest, support bouts; 'ALL-IN' was the 1930s name); a bill that names nothing reads as a placeholder by another name, so **W01 is HELD with its named twin** and built only once the town mints the hall and the ring names (second review, fault 3). The `-named` twin carries the proposed names: THE DRILL HALL (a generic building, no street given) and four invented ring names (THE HARPOONER, SPANNER SMITH, TED HOLROYD, THE STEVEDORE), renamed after the review found two of the first four real (a dock-union leader; Jack London's novel) and a third a television series, and after the re-review found the first rewrite, BIG TED HOLROYD, to be the name of the bear in the BBC children's programme Play School (BIG TED is now in `real_marks`). No odds, no stakes, no prize. The market bill matches `hook-cast.json`: Tuesday, Friday, Saturday, 8 to 4. The two goods are INVENTED brands (WHITEWELL washday powder, QUAYSIDE TEA), proposed, not minted, held and not placed (a national four-sheet belongs in a contractor's panel, not pasted under fly-posters); a cigarette bill is not drawn (a minted brand and the 1990 health-warning wording are both missing).

#### W01  Professional wrestling bill

- 508 x 762 mm (double_crown); 3 px/mm; stock: pale yellow copier paper; process: letterpress_2col; event: FRIDAY 2 NOVEMBER; dated: event 1990-11-02; HELD (a nameless stand-in; waits with W01-named for: THE DRILL HALL, THE HARPOONER, SPANNER SMITH, TED HOLROYD, THE STEVEDORE)
- variants: 3 (age class A, B; red pass shifted; one with the date line struck through by a hand-painted band (event over): a red felt-pen stripe, NO new words; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [40, 434.0, 468, 437.4], fill black
  - `PROFESSIONAL` | oswald 700 | cap 47 | centre 254 | base 691 | black | B 13.04
  - `WRESTLING` | oswald 700 | cap 82.5 | centre 254 | base 586.4 | red | B 3.97
  - `FRIDAY 2 NOVEMBER` | oswald 700 | cap 39.5 | centre 254 | base 508.1 | black | B 13.04
  - `BELL 7.30 PM` | oswald 600 | cap 34 | centre 254 | base 452 | red | B 3.97
  - `HEAVYWEIGHT CONTEST` | oswald 700 | cap 32.5 | centre 254 | base 389.5 | black | B 13.04
  - `TAG TEAM CONTEST` | oswald 700 | cap 39.5 | centre 254 | base 291.9 | black | B 13.04
  - `AND SUPPORT BOUTS` | oswald 600 | cap 20 | centre 254 | base 205.5 | black | B 13.04
  - `RINGSIDE £4 · UNRESERVED £2.50` | libre-franklin 800 | cap 17 | centre 254 | base 97.2 | red | B 3.97
  - `TICKETS AT THE DOOR` | libre-franklin 700 | cap 14 | centre 254 | base 50 | black | B 13.04
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.04

#### W01-named  Professional wrestling bill (ring names and venue named, held)

- 508 x 762 mm (double_crown); 3 px/mm; stock: pale yellow copier paper; process: letterpress_2col; event: FRIDAY 2 NOVEMBER; dated: event 1990-11-02; HELD until minted: THE DRILL HALL, THE HARPOONER, SPANNER SMITH, TED HOLROYD, THE STEVEDORE
- variants: 3 (age class A, B; red pass shifted; one with the date line struck through by a hand-painted band (event over): a red felt-pen stripe, NO new words; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [40, 433.99999999999994, 468, 437.3999999999999], fill black
  - `PROFESSIONAL` | oswald 700 | cap 47 | centre 254 | base 691 | black | B 13.04
  - `WRESTLING` | oswald 700 | cap 82.5 | centre 254 | base 599.2 | red | B 3.97
  - `THE DRILL HALL` | oswald 600 | cap 34 | centre 254 | base 548.8 | black | B 13.04
  - `FRIDAY 2 NOVEMBER` | oswald 700 | cap 39.5 | centre 254 | base 495.3 | black | B 13.04
  - `BELL 7.30 PM` | oswald 600 | cap 34 | centre 254 | base 452 | red | B 3.97
  - `THE HARPOONER` | oswald 700 | cap 45 | centre 254 | base 377 | black | B 13.04
  - `v` | old-standard-tt-italic 400 | cap 14 | centre 254 | base 356.9 | red | B 3.97
  - `SPANNER SMITH` | oswald 700 | cap 47.5 | centre 254 | base 303.2 | black | B 13.04
  - `TED HOLROYD` | oswald 700 | cap 43 | centre 254 | base 232.7 | black | B 13.04
  - `v` | old-standard-tt-italic 400 | cap 14 | centre 254 | base 212.5 | red | B 3.97
  - `THE STEVEDORE` | oswald 700 | cap 38 | centre 254 | base 168.4 | black | B 13.04
  - `AND SUPPORT BOUTS` | oswald 600 | cap 20 | centre 254 | base 127 | black | B 13.04
  - `RINGSIDE £4 · UNRESERVED £2.50` | libre-franklin 800 | cap 17 | centre 254 | base 76.3 | red | B 3.97
  - `TICKETS AT THE DOOR` | libre-franklin 700 | cap 14 | centre 254 | base 50 | black | B 13.04
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.04

#### B01  Boxing night bill (venue named, held)

- 508 x 762 mm (double_crown); 2 px/mm; stock: pale blue poster paper; process: letterpress_2col; event: FRIDAY 16 NOVEMBER; dated: event 1990-11-16; HELD until minted: THE DRILL HALL
- variants: 2 (age class A, B; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [40, 276.00000000000006, 468, 279.40000000000003], fill black
  - `BOXING` | alfa-slab-one 400 | cap 76.5 | centre 254 | base 661.5 | black | B 11.4
  - `TEN BOUTS` | oswald 700 | cap 66.5 | centre 254 | base 547.8 | red | B 3.58
  - `THE DRILL HALL` | oswald 600 | cap 44 | centre 254 | base 437 | black | B 11.4
  - `FRIDAY 16 NOVEMBER` | oswald 700 | cap 39.5 | centre 254 | base 366 | black | B 11.4
  - `FIRST BOUT 7.30 PM` | oswald 600 | cap 38.5 | centre 254 | base 300 | red | B 3.58
  - `RINGSIDE £3 · UNRESERVED £1.50` | libre-franklin 800 | cap 17.5 | centre 254 | base 240.5 | black | B 11.4
  - `TICKETS AT THE DOOR` | libre-franklin 700 | cap 18 | centre 254 | base 90 | black | B 11.4
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 11.4

#### M01  Market day bill

- 508 x 762 mm (double_crown); 3 px/mm; stock: white poster paper; process: letterpress_2col
- variants: 2 (age class B, D (the old one is mostly paste and one torn half); skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [40, 312.0, 468, 315.4], fill black
  - `COPPER ROW` | alfa-slab-one 400 | cap 46 | centre 254 | base 692 | blue | B 7.19
  - `MARKET` | alfa-slab-one 400 | cap 69 | centre 254 | base 588.2 | black | B 13.0
  - `TUESDAYS · FRIDAYS · SATURDAYS` | oswald 700 | cap 25.5 | centre 254 | base 475.6 | black | B 13.0
  - `8 AM TO 4 PM` | oswald 700 | cap 58.5 | centre 254 | base 330 | blue | B 7.19
  - `FRUIT · VEG · FISH · HOUSEHOLD · CLOTHING` | oswald 600 | cap 19 | centre 254 | base 271 | black | B 13.0
  - `NEW STALLS WELCOME` | libre-franklin 800 | cap 20 | centre 254 | base 125.8 | black | B 13.0
  - `ENQUIRIES: THE MARKET OFFICE` | libre-franklin 700 | cap 14 | centre 254 | base 70 | black | B 13.0
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.0

#### G01  Washday powder four-sheet (invented brand, held)

- 1016 x 1524 mm (four_sheet); 2 px/mm; stock: white poster paper; process: litho_4col; HELD until minted: WHITEWELL
- variants: 2 (age class C, D; one with the lower half pasted over by P03 and P01)
- shape title_band (rect): box [0, 0, 1016, 420], fill blue
- ART SLOT art [0, 420, 1016, 1524]: a washing line of white sheets and towels in a bright cold wind over a terraced back-yard wall, the sky pale blue; no people, no faces, no lettering anywhere in the picture. Forbidden: people, hands, faces, children, text, lettering, numerals, logos, crowns, kiosk lettering, operator marks, bottles, glasses, arcade or amusement signs, any real product. the sheets are the whitest area; the sky is behind the title
  - `WHITEWELL` | alfa-slab-one 400 | cap 97.5 | centre 508 | base 250 | paper | B 7.19
  - `WASHES WHITE` | oswald 700 | cap 70 | centre 508 | base 150 | paper | B 7.19
  - `FOR TWIN-TUB, AUTOMATIC AND HAND WASHING` | libre-franklin 700 | cap 24 | centre 508 | base 90 | paper | B 7.19
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 4 | centre 508 | base 40 | paper | B 7.19

#### G02  Tea bill (invented brand, held)

- 508 x 762 mm (double_crown); 2 px/mm; stock: cream poster paper; process: letterpress_2col; HELD until minted: QUAYSIDE
- variants: 2 (age class B, C; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape cup (roundel): box [134.0, 229.5, 374.0, 469.5], fill red - a flat red disc standing for a cup seen from above; our own drawing, no photograph
- shape cup_ring (ring): centre [254.0, 349.5], r 76.0 to 92.0 mm - the cup's white ring: 16 mm wide, centred on 0.70 of the disc's radius (TARGET-REVIEW fault 11)
  - `QUAYSIDE` | alfa-slab-one 400 | cap 61 | centre 254 | base 677 | red | B 3.72
  - `TEA` | alfa-slab-one 400 | cap 102.5 | centre 254 | base 564.5 | black | B 12.1
  - `A good strong cup` | fraunces 700 | cap 39 | centre 254 | base 503.5 | black | B 12.1
  - `80 BAGS · £1.35` | oswald 700 | cap 52 | centre 254 | base 100 | black | B 12.1
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 30 | black | B 12.1

### 5.4 The Tivoli

The Tivoli is minted (canon) and 'changes its programme on Thursdays' (brand bible): the films start on Thursdays (T01 from 18 October, T02 from 25 October). Its films are invented: the nameless bills (T01 'A NEW THRILLER', T02 'A NEW COMEDY', T03's programme that names no film) read as stand-ins and are HELD with their twins (second review, fault 3); the `-named` twins say THE FOURTH WITNESS and A WEEK AT GULLWING (Gullwing is a minted district) with a billing block (6 to 12 mm: a studio and three credits, placeholders); the BBFC certificate roundels are real marks and are NOT drawn. **A distributor's quad carried no venue**: the cinema pasted a strip across its top band, so the quad's own top 90 mm is blank and the strips T01s and T02s (1016 x 90 mm, letterpress black on white, 2 to 6 mm off square) carry THE TIVOLI and FROM THURSDAY ...  The quads' art comes from the image model with no words and no people (no telephone box, no pier: a lit window down a wet street; a beach with deckchairs); our text sits on a dark scrim (T01) or on a pale panel (T02). The Tivoli's own front (plastic letters on a rail, changed on Thursdays) is not this family's.

#### T01  Tivoli quad: a new thriller (no title minted)

- 1016 x 762 mm (quad_crown); 2 px/mm; stock: white poster paper; process: litho_4col; event: THURSDAY 18 OCTOBER; dated: event 1990-10-18; HELD (a nameless stand-in; waits with T01-named for: MARSHLAND PICTURES, A. VENN, R. CORLEY, H. MADDOX, THE FOURTH WITNESS)
- variants: 2 (age class B, C; one cut in half by a torn edge, the title half left; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape scrim_bottom (scrim): box [0, 0, 1016, 300], fill black - gradient, fully dark at the foot
- shape scrim_top (scrim): box [0, 672, 1016, 762], fill black - the top band is flat dark and BLANK: no lettering of any kind in the litho; the strip T01s is pasted over it
- ART SLOT art [0, 0, 1016, 762]: a narrow wet cobbled street at night seen from a first-floor window, lamplight in orange pools on the cobbles, one lit window far down the street, rain on the glass in the near corner; dark blue and black with orange; no people, no faces, no lettering, no signs, no telephone box. Forbidden: people, hands, faces, children, text, lettering, numerals, signs, crowns, kiosks or telephone boxes, operator marks, real brands, real places, vehicles with plates, bottles, glasses, arcade or amusement signs. the top 90 mm stays blank and dark (the venue strip T01s is pasted there); the lower third and the left must stay dark and low in detail: a scrim is laid there for the words
  - `Somebody saw. Somebody will pay.` | fraunces 600 | cap 30 | centre 508 | base 628 | agent_white | B 12.41
  - `A NEW` | oswald 700 | cap 128 | left 70 | base 250 | agent_white | B 12.41
  - `THRILLER` | oswald 700 | cap 128 | left 70 | base 98 | lamp_orange | B 7.72

#### T01-named  Tivoli quad: THE FOURTH WITNESS (named film, held)

- 1016 x 762 mm (quad_crown); 4 px/mm; stock: white poster paper; process: litho_4col; event: THURSDAY 18 OCTOBER; dated: event 1990-10-18; HELD until minted: MARSHLAND PICTURES, A. VENN, R. CORLEY, H. MADDOX, THE FOURTH WITNESS
- variants: 2 (age class B, C; one cut in half by a torn edge, the title half left; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape scrim_bottom (scrim): box [0, 0, 1016, 300], fill black - gradient, fully dark at the foot
- shape scrim_top (scrim): box [0, 672, 1016, 762], fill black - the top band is flat dark and BLANK: no lettering of any kind in the litho; the strip T01s is pasted over it
- ART SLOT art [0, 0, 1016, 762]: a narrow wet cobbled street at night seen from a first-floor window, lamplight in orange pools on the cobbles, one lit window far down the street, rain on the glass in the near corner; dark blue and black with orange; no people, no faces, no lettering, no signs, no telephone box. Forbidden: people, hands, faces, children, text, lettering, numerals, signs, crowns, kiosks or telephone boxes, operator marks, real brands, real places, vehicles with plates, bottles, glasses, arcade or amusement signs. the top 90 mm stays blank and dark (the venue strip T01s is pasted there); the lower third and the left must stay dark and low in detail: a scrim is laid there for the words
  - `Somebody saw. Somebody will pay.` | fraunces 600 | cap 30 | centre 508 | base 628 | agent_white | B 12.41
  - `THE FOURTH` | oswald 700 | cap 128 | left 70 | base 250 | agent_white | B 12.41
  - `WITNESS` | oswald 700 | cap 128 | left 70 | base 98 | lamp_orange | B 7.72
  - `A MARSHLAND PICTURES PRODUCTION · SCREENPLAY BY A. VENN` | oswald 500 | cap 12 | left 70 | base 62 | agent_white | B 12.41
  - `MUSIC BY R. CORLEY · DIRECTED BY H. MADDOX` | oswald 500 | cap 12 | left 70 | base 40 | agent_white | B 12.41

#### T02  Tivoli quad: a new comedy (no title minted)

- 1016 x 762 mm (quad_crown); 2 px/mm; stock: white poster paper; process: litho_4col; event: THURSDAY 25 OCTOBER; dated: event 1990-10-25; HELD (a nameless stand-in; waits with T02-named for: MARSHLAND PICTURES, H. MADDOX, A WEEK AT GULLWING)
- variants: 2 (age class A, B; one with the sky bleached to near white; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape title_panel (rect): box [110, 385, 906, 560], fill agent_white - a pale panel behind the red title so the red holds; the sky shows round it
- ART SLOT art [0, 0, 1016, 762]: a pale empty beach under a high pale-blue sky with a row of striped deckchairs lined up empty on the sand and a wooden breakwater running to a calm sea, bright flat colours like a saucy postcard; no buildings, no pier, no people, no faces, no lettering. Forbidden: people, hands, faces, children, text, lettering, numerals, signs, crowns, kiosks, operator marks, real brands, buildings, a pier, arcade or amusement signs, drink, bottles, glasses, gambling machines. the top 90 mm stays clear flat sky (the venue strip T02s is pasted there); the sky across the top 40 per cent stays clear and flat for the title
  - `A NEW` | fraunces 900 | cap 80 | centre 508 | base 585 | agent_white | B 4.4
  - `COMEDY` | fraunces 900 | cap 121 | centre 508 | base 415 | agent_red | B 4.98
  - `The funniest week of their lives.` | fraunces 600 | cap 30 | centre 508 | base 70 | agent_navy | B 7.47

#### T02-named  Tivoli quad: A WEEK AT GULLWING (named film, held)

- 1016 x 762 mm (quad_crown); 4 px/mm; stock: white poster paper; process: litho_4col; event: THURSDAY 25 OCTOBER; dated: event 1990-10-25; HELD until minted: MARSHLAND PICTURES, H. MADDOX, A WEEK AT GULLWING
- variants: 2 (age class A, B; one with the sky bleached to near white; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape title_panel (rect): box [110, 385, 906, 560], fill agent_white - a pale panel behind the red title so the red holds; the sky shows round it
- ART SLOT art [0, 0, 1016, 762]: a pale empty beach under a high pale-blue sky with a row of striped deckchairs lined up empty on the sand and a wooden breakwater running to a calm sea, bright flat colours like a saucy postcard; no buildings, no pier, no people, no faces, no lettering. Forbidden: people, hands, faces, children, text, lettering, numerals, signs, crowns, kiosks, operator marks, real brands, buildings, a pier, arcade or amusement signs, drink, bottles, glasses, gambling machines. the top 90 mm stays clear flat sky (the venue strip T02s is pasted there); the sky across the top 40 per cent stays clear and flat for the title
  - `A WEEK AT` | fraunces 900 | cap 80 | centre 508 | base 585 | agent_white | B 4.4
  - `GULLWING` | fraunces 900 | cap 95.5 | centre 508 | base 415 | agent_red | B 4.98
  - `The funniest week of their lives.` | fraunces 600 | cap 30 | centre 508 | base 70 | agent_navy | B 7.47
  - `A MARSHLAND PICTURES PRODUCTION · DIRECTED BY H. MADDOX` | oswald 500 | cap 12 | centre 508 | base 36 | agent_navy | B 7.47

#### T03  Tivoli programme bill (no titles minted)

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col; event: THURSDAY 18 OCTOBER; dated: event 1990-10-18; HELD (a nameless stand-in; waits with T03-named for: THE FOURTH WITNESS, A WEEK AT GULLWING)
- variants: 2 (age class A, B; one with the lower half torn away; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [40, 308.00000000000006, 468, 311.40000000000003], fill black
  - `THE TIVOLI` | oswald 700 | cap 68.5 | centre 254 | base 667.5 | red | B 3.99
  - `FROM THURSDAY 18 OCTOBER` | oswald 600 | cap 25.5 | centre 254 | base 595.9 | black | B 13.0
  - `A NEW THRILLER` | oswald 700 | cap 54 | centre 254 | base 516.4 | black | B 13.0
  - `FROM THURSDAY 25 OCTOBER` | oswald 600 | cap 25.5 | centre 254 | base 414.1 | black | B 13.0
  - `A NEW COMEDY` | oswald 700 | cap 58.5 | centre 254 | base 330 | black | B 13.0
  - `PERFORMANCES 5.15 AND 8.00` | oswald 600 | cap 26.5 | centre 254 | base 259.5 | black | B 13.0
  - `SATURDAY ALSO 2.30` | oswald 600 | cap 28.5 | centre 254 | base 200.9 | black | B 13.0
  - `ALL SEATS £2.80` | libre-franklin 800 | cap 23.5 | centre 254 | base 113 | red | B 3.99
  - `O.A.P. AND UNWAGED £1.50` | libre-franklin 800 | cap 21.5 | centre 254 | base 70 | red | B 3.99
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.0

#### T03-named  Tivoli programme bill (named films, held)

- 508 x 762 mm (double_crown); 2 px/mm; stock: white poster paper; process: letterpress_2col; event: THURSDAY 18 OCTOBER; dated: event 1990-10-18; HELD until minted: THE FOURTH WITNESS, A WEEK AT GULLWING
- variants: 2 (age class A, B; one with the lower half torn away; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [40, 308.0, 468, 311.4], fill black
  - `THE TIVOLI` | oswald 700 | cap 68.5 | centre 254 | base 667.5 | red | B 3.99
  - `FROM THURSDAY 18 OCTOBER` | oswald 600 | cap 25.5 | centre 254 | base 588 | black | B 13.0
  - `THE FOURTH WITNESS` | oswald 700 | cap 41 | centre 254 | base 517 | black | B 13.0
  - `FROM THURSDAY 25 OCTOBER` | oswald 600 | cap 25.5 | centre 254 | base 401.5 | black | B 13.0
  - `A WEEK AT GULLWING` | oswald 700 | cap 41.5 | centre 254 | base 330 | black | B 13.0
  - `PERFORMANCES 5.15 AND 8.00` | oswald 600 | cap 26.5 | centre 254 | base 259.5 | black | B 13.0
  - `SATURDAY ALSO 2.30` | oswald 600 | cap 28.5 | centre 254 | base 200.9 | black | B 13.0
  - `ALL SEATS £2.80` | libre-franklin 800 | cap 23.5 | centre 254 | base 113 | red | B 3.99
  - `O.A.P. AND UNWAGED £1.50` | libre-franklin 800 | cap 21.5 | centre 254 | base 70 | red | B 3.99
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 254 | base 24 | black | B 13.0

#### T01s  Tivoli venue strip for T01, 1016 x 90, letterpress black on white

- 1016 x 90 mm (own size); 2 px/mm; stock: white poster paper; process: letterpress_1col; event: THURSDAY 18 OCTOBER; dated: event 1990-10-18
- variants: 2 (age class B (the quad's own class) and A; set 2 to 6 mm off square on the quad's top band: the placement's rot_deg carries it; the strip's own texture is square-on)
  - `THE TIVOLI` | oswald 700 | cap 36 | left 30 | base 27 | black | B 13.0
  - `FROM THURSDAY 18 OCTOBER` | oswald 600 | cap 30 | right 986 | base 29 | black | B 13.0

#### T02s  Tivoli venue strip for T02, 1016 x 90, letterpress black on white

- 1016 x 90 mm (own size); 2 px/mm; stock: white poster paper; process: letterpress_1col; event: THURSDAY 25 OCTOBER; dated: event 1990-10-25
- variants: 2 (age class B (the quad's own class) and A; set 2 to 6 mm off square on the quad's top band: the placement's rot_deg carries it; the strip's own texture is square-on)
  - `THE TIVOLI` | oswald 700 | cap 36 | left 30 | base 27 | black | B 13.0
  - `FROM THURSDAY 25 OCTOBER` | oswald 600 | cap 30 | right 986 | base 29 | black | B 13.0

### 5.5 The ferry and the Harbour Board

Both are minted names (canon). The ferry sheet is the WINTER SERVICE from Monday 1 October 1990, pasted over the summer sheet on a painted timber board at a ramp (FC1, no glazing), as the brand bible says; the service is one a single boat can run (15-minute crossings; Hook sailings at :00 and :30 by day, the far side's 15 minutes later; **the far side's last crossing is 11.15 PM so the boat is at the Hook at 11.30**, and Sunday's 6.15 PM brings it home at 6.30) and its last Hook crossing, 11.00 PM, is the street's own line 'Last crossing's at eleven'. `G.ferry.schedule` simulates the one vessel from the printed blocks and checks that each day ends where the next day's first sailing leaves. The fares are foot passengers and cycles: no one is a child. The Harbour Board's notices are typed Courier on A4 in a glass case drawing-pinned and curling (the brand bible's own words), headed NOTICE TO MARINERS (not SHIPMASTERS); its blue and white enamel signs are 600 x 450 on a gate, post or quay edge. NONE of the case, the board or the notices is placed on Quay Street (no dock office, no ramp); H02 stands on a proposed quay-edge post. Board blue is Judgement: (24,68,140).

#### F01  Meridian Ferry winter timetable (A2 sheet for the ramp board)

- 420 x 594 mm (A2); 4 px/mm; stock: white poster paper; process: litho_2col; event: MONDAY 1 OCTOBER; dated: event 1990-10-01
- variants: 2 (PASTED over the summer sheet F02 (offset +14 mm right, -16 mm down) on the ramp board FC1 in both; age class B and C; the C one has two drawing-pin holes and a rain stain from the top)
- shape head_band (rect): box [0, 490, 420, 594], fill enamel_blue
- shape col_rule (rule): box [208.5, 130, 211.5, 440], fill blue
- shape fare_rule (rule): box [12, 150, 408, 152.4], fill blue
  - `MERIDIAN FERRY` | alfa-slab-one 400 | cap 29.5 | centre 210 | base 536 | enamel_white | B 6.7
  - `WINTER SERVICE` | oswald 700 | cap 24 | centre 210 | base 504 | enamel_white | B 6.7
  - `FROM MONDAY 1 OCTOBER` | oswald 600 | cap 17 | centre 210 | base 458 | blue | B 7.19
  - `FROM THE HOOK` | oswald 700 | cap 15 | centre 110 | base 425 | black | B 13.0
  - `FROM THE FAR SIDE` | oswald 700 | cap 15 | centre 310 | base 425 | black | B 13.0
  - `MONDAY TO SATURDAY` | oswald 700 | cap 13 | centre 210 | base 398 | blue | B 7.19
  - `6.30  7.00  7.30` | libre-franklin 700 | cap 10.5 | centre 110 | base 372 | black | B 13.0
  - `and every half hour` | libre-franklin 500 | cap 10.5 | centre 110 | base 351 | black | B 13.0
  - `until 5.30 PM` | libre-franklin 500 | cap 10.5 | centre 110 | base 330 | black | B 13.0
  - `then 6.30  7.30  8.30` | libre-franklin 700 | cap 10.5 | centre 110 | base 309 | black | B 13.0
  - `9.30  10.30` | libre-franklin 700 | cap 10.5 | centre 110 | base 288 | black | B 13.0
  - `LAST CROSSING 11.00` | libre-franklin 700 | cap 10.5 | centre 110 | base 267 | black | B 13.0
  - `6.45  7.15  7.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 372 | black | B 13.0
  - `and every half hour` | libre-franklin 500 | cap 10.5 | centre 310 | base 351 | black | B 13.0
  - `until 5.45 PM` | libre-franklin 500 | cap 10.5 | centre 310 | base 330 | black | B 13.0
  - `then 6.45  7.45  8.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 309 | black | B 13.0
  - `9.45  10.45` | libre-franklin 700 | cap 10.5 | centre 310 | base 288 | black | B 13.0
  - `LAST CROSSING 11.15` | libre-franklin 700 | cap 10.5 | centre 310 | base 267 | black | B 13.0
  - `SUNDAYS` | oswald 700 | cap 13 | centre 210 | base 236 | blue | B 7.19
  - `9.00 AM and hourly` | libre-franklin 700 | cap 10.5 | centre 110 | base 210 | black | B 13.0
  - `until 6.00 PM` | libre-franklin 500 | cap 10.5 | centre 110 | base 189 | black | B 13.0
  - `9.15 AM and hourly` | libre-franklin 700 | cap 10.5 | centre 310 | base 210 | black | B 13.0
  - `until 6.15 PM` | libre-franklin 500 | cap 10.5 | centre 310 | base 189 | black | B 13.0
  - `FARES · FOOT PASSENGERS` | oswald 700 | cap 13 | centre 210 | base 124 | blue | B 7.19
  - `SINGLE 60p · RETURN £1.00 · CYCLES 30p` | libre-franklin 700 | cap 11 | centre 210 | base 98 | black | B 13.0
  - `O.A.P. HALF FARE` | libre-franklin 700 | cap 11 | centre 210 | base 76 | black | B 13.0
  - `CROSSINGS MAY BE CANCELLED IN FOG OR HIGH WIND` | oswald 600 | cap 11 | centre 210 | base 40 | red | B 3.99
  - `Printed by Quay Print, Meridian.` | libre-franklin 500 | cap 2.4 | centre 210 | base 20 | black | B 13.0

#### F02  Meridian Ferry summer timetable (older sheet under F01)

- 420 x 594 mm (A2); 2 px/mm; stock: white poster paper; process: litho_2col
- variants: 1 (age class D: brown paste halo, loose at the left edge)
- shape head_band (rect): box [0, 490, 420, 594], fill enamel_blue
- shape col_rule (rule): box [208.5, 130, 211.5, 440], fill blue
  - `MERIDIAN FERRY` | alfa-slab-one 400 | cap 29.5 | centre 210 | base 536 | enamel_white | B 6.7
  - `SUMMER SERVICE` | oswald 700 | cap 24 | centre 210 | base 504 | enamel_white | B 6.7
  - `14 MAY TO 30 SEPTEMBER` | oswald 600 | cap 17 | centre 210 | base 458 | blue | B 7.19

#### H01  Harbour Board enamel sign: NO ADMITTANCE

- 600 x 450 mm (own size); 2 px/mm; process: enamel
- variants: 2 (clean to grimy (age classes B and D); one shot-peppered by the old catapult: six small chips in a loose group (a chip is not a bullet hole))
- shape face (rect): box [0, 0, 600, 450], fill enamel_blue - vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge of 6 mm radius
- shape border (frame): box [18, 18, 582, 432], fill enamel_white - white band 10 mm, 18 mm in from the edge
- shape rule (rule): box [70, 190, 530, 194], fill enamel_white
  - `NO ADMITTANCE` | archivo 900 | cap 33.5 | centre 300 | base 361.5 | enamel_white | B 6.7
  - `EXCEPT ON BUSINESS` | archivo 700 | cap 27 | centre 300 | base 312.5 | enamel_white | B 6.7
  - `MERIDIAN HARBOUR BOARD` | archivo 800 | cap 20.5 | centre 300 | base 140 | enamel_white | B 6.7

#### H02  Harbour Board enamel sign: DANGER DEEP WATER

- 600 x 450 mm (own size); 2 px/mm; process: enamel
- variants: 2 (age class B, D)
- shape face (rect): box [0, 0, 600, 450], fill enamel_white - vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge of 6 mm radius
- shape danger_band (rect): box [0, 300, 600, 450], fill enamel_red
- shape border (frame): box [14, 14, 586, 436], fill enamel_blue
  - `DANGER` | archivo 900 | cap 60.5 | centre 300 | base 332 | enamel_white | B 5.25
  - `DEEP WATER` | archivo 900 | cap 44.5 | centre 300 | base 220 | enamel_blue | B 6.7
  - `NO SWIMMING` | archivo 800 | cap 37 | centre 300 | base 130 | enamel_blue | B 6.7
  - `MERIDIAN HARBOUR BOARD` | archivo 800 | cap 17 | centre 300 | base 56 | enamel_blue | B 6.7

#### H03  Harbour Board notice: berths closed (typed A4)

- 210 x 297 mm (A4); 12 px/mm; stock: white copier paper, A4 or A3; process: typed_carbon; event: 26 OCTOBER 1990; dated: notice 1990-10-26
- variants: 2 (pinned in the case: four drawing pins; a tan tape tab; one curling top corner (held: the case HC1 is not built until the dock office is))
- shape rule_a (rule): box [20, 268, 190, 269.2], fill typed
  - `MERIDIAN HARBOUR BOARD` | old-standard-tt 700 | cap 7.5 | centre 105 | base 274 | typed | B 12.21
  - `NOTICE TO MARINERS` | courier-prime-bold 700 | cap 3.6 | centre 105 | base 255 | typed | B 12.21
  - `Berths 3 and 4 on the Hook quay will be closed to all` | courier-prime 400 | cap 2.455 | left 24 | base 238 | typed | B 12.21
  - `shipping from Monday 5 November until further notice,` | courier-prime 400 | cap 2.455 | left 24 | base 229.5 | typed | B 12.21
  - `for repairs to the quay wall.` | courier-prime 400 | cap 2.455 | left 24 | base 221.1 | typed | B 12.21
  - `Masters should apply to the Harbour Master's office` | courier-prime 400 | cap 2.455 | left 24 | base 204.1 | typed | B 12.21
  - `for other berths.` | courier-prime 400 | cap 2.455 | left 24 | base 195.7 | typed | B 12.21
  - `By order of the Board.` | courier-prime 400 | cap 2.455 | left 24 | base 178.7 | typed | B 12.21
  - `26 October 1990` | courier-prime 400 | cap 2.455 | left 24 | base 161.8 | typed | B 12.21

#### H04  Harbour Board notice: tide table (typed A4)

- 210 x 297 mm (A4); 12 px/mm; stock: white copier paper, A4 or A3; process: typed_carbon
- variants: 1 (pinned in the case, a corner curling (held: the case HC1 is not built until the dock office is))
- shape rule_a (rule): box [20, 268, 190, 269.2], fill typed
  - `MERIDIAN HARBOUR BOARD` | old-standard-tt 700 | cap 7.5 | centre 105 | base 274 | typed | B 12.21
  - `HIGH WATER, THE HOOK` | courier-prime-bold 700 | cap 3.6 | centre 105 | base 255 | typed | B 12.21
  - `NOVEMBER 1990` | courier-prime-bold 700 | cap 3.6 | centre 105 | base 247 | typed | B 12.21
  - `DAY       HW     m     HW     m` | courier-prime 400 | cap 2.455 | left 30 | base 232 | typed | B 12.21
  - `THU 1    0542 4.4   1807 4.3` | courier-prime 400 | cap 2.455 | left 30 | base 223.5 | typed | B 12.21
  - `FRI 2    0632 4.6   1857 4.5` | courier-prime 400 | cap 2.455 | left 30 | base 215.1 | typed | B 12.21
  - `SAT 3    0722 4.7   1947 4.6` | courier-prime 400 | cap 2.455 | left 30 | base 206.6 | typed | B 12.21
  - `SUN 4    0812 4.8   2037 4.7` | courier-prime 400 | cap 2.455 | left 30 | base 198.1 | typed | B 12.21
  - `MON 5    0902 4.7   2127 4.6` | courier-prime 400 | cap 2.455 | left 30 | base 189.7 | typed | B 12.21
  - `TUE 6    0952 4.5   2217 4.4` | courier-prime 400 | cap 2.455 | left 30 | base 181.2 | typed | B 12.21
  - `WED 7    1042 4.2   2307 4.1` | courier-prime 400 | cap 2.455 | left 30 | base 172.7 | typed | B 12.21
  - `Heights in metres above chart datum.` | courier-prime 400 | cap 2.455 | left 30 | base 155.8 | typed | B 12.21
  - `Times are Greenwich Mean Time.` | courier-prime 400 | cap 2.455 | left 30 | base 147.3 | typed | B 12.21

#### H05  Harbour Board notice: vacancy (typed A4)

- 210 x 297 mm (A4); 12 px/mm; stock: pale yellow copier paper; process: typed_carbon
- variants: 1 (pinned in the case (held: the case HC1 is not built until the dock office is))
- shape rule_a (rule): box [20, 268, 190, 269.2], fill typed
  - `MERIDIAN HARBOUR BOARD` | old-standard-tt 700 | cap 7.5 | centre 105 | base 274 | typed | B 11.76
  - `VACANCY` | courier-prime-bold 700 | cap 9 | centre 105 | base 244 | typed | B 11.76
  - `QUAY LABOURER` | courier-prime-bold 700 | cap 5.4 | centre 105 | base 224 | typed | B 11.76
  - `Applications in writing, giving age and experience,` | courier-prime 400 | cap 2.455 | left 24 | base 202 | typed | B 11.76
  - `to the Secretary, Meridian Harbour Board,` | courier-prime 400 | cap 2.455 | left 24 | base 193.5 | typed | B 11.76
  - `to arrive by Friday 16 November.` | courier-prime 400 | cap 2.455 | left 24 | base 185.1 | typed | B 11.76
  - `Wages by agreement.` | courier-prime 400 | cap 2.455 | left 24 | base 168.1 | typed | B 11.76

#### HC1  Harbour Board notice case (not placed until the dock office is built)

- outer 640 x 880 x 60 mm, frame left 46, right 46, top 52, bottom 52, window corner radius 6 mm; inside [548, 776] mm
- rails [46, 60] mm with a 4 mm chamfer on the outer arris of every rail; glass 4 mm in a [10, 10] mm bead
- construction: varnished timber frame (rails 46 x 60 mm, a 4 mm chamfer on the outer arris; dark, grain showing, varnish crazed and lifting at the lower rails), mitred corners, one glazed door hinged on the left with two brass butt hinges, a brass lock and escutcheon 20 mm across on the right stile at 0.5 of the height, a cork lining 8 mm thick, a drip rail on top 14 mm proud
- fixing: four 8 mm coach screws through the back rails at 40 mm in from the corners, on 20 mm timber battens; rust runs 40 to 180 mm below each screw
- wear: a crack across one lower corner of the glass (30 per cent of the cases), a brown water line inside the lower glass, flies and dead leaves on the cork foot, varnish lifted at the bottom rail, one hinge screw missing
- pinned or pasted inside: H03 at (24, 470) mm, 0.8 degrees; H04 at (300, 455) mm, -1.2 degrees; H05 at (160, 100) mm, 0.5 degrees
- NOT placed: by the dock office (brand bible; hook-cast harbour_office): neither is built
- photograph: the photographed case is blue steel with a 0.152 header and a 0.085 foot; the target is a 1990 timber case with 52 mm top and bottom rails (0.059 each of the height), 46 mm stiles (0.072 of the width each): the photograph's wide crest header and thick steel frame are replacement-stock features and are NOT taken (Judgement: photograph of a later object); the council crest on the photographed header is masked in the preview

#### FC1  Ferry timetable board at the ramp (painted timber, no glazing; not placed until the ramp is built)

- outer 600 x 800 x 22 mm, frame left 40, right 40, top 40, bottom 40, window corner radius 0 mm; inside [520, 720] mm
- construction: a 22 mm exterior plywood board, 600 x 800 mm, painted Board blue (24,68,140) with a 40 mm border all round and a 520 x 720 mm white panel; NO glazing, no frame lip; the winter sheet F01 pasted over the summer sheet F02 with wallpaper paste; two 60 x 40 mm timber battens on the back
- fixing: four 8 mm screws at the corners, 30 mm in, into plugs; a rust run under each lower screw
- wear: paste halo round both sheets, the older sheet's edge peeling at the left and the top, rain stains from the top edge, paint chipped at the lower corners, salt bloom along the foot, rust at the lower screws
- pinned or pasted inside: F02 at (50, 82) mm, 0.0 degrees; F01 at (64, 66) mm, 0.0 degrees
- NOT placed: at each ramp (brand bible): the ramp is not built
- photograph: a board, not a case: no photograph proportions apply

### 5.6 Police and council notices

The police force's name and the council's name are OWED by canon, so neither appears: POLICE, HIGHWAYS DEPARTMENT and the Planning Department are the generic words. A police appeal is an A3 photocopy taped inside a window or sleeved on a column (the one dated yellow appeal board found is from 2007; a 1990 board is a hole): C01a is taped inside the empty unit's glass with four tabs. The three samples are slots the simulation can fill (offence line, night, hours): a smashed shop window on Quay Street (matching the 29 September deed), a van stolen from the quay, a man assaulted near the quay. The planning notice is for the empty unit itself, **number 7** (shop to estate agent's office): a mundane hook, struck if the town prefers. The road closure sends traffic via WEIGHHOUSE LANE (minted; the atlas's Weighhouse Lane and Tannery Row make the way round; the side opening at x 21 to 24 is the yard entrance, not that lane).

#### C01a  Police appeal for witnesses (a)

- 297 x 420 mm (A3); 6 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a3; event: FRIDAY 12 OCTOBER; dated: notice 1990-10-12
- variants: 2 (photocopy: a grey edge band 3 to 6 mm at the left, toner speckle; taped inside a window with four tabs of yellowed tape (the empty unit's glass, SF2: C01a), or in a polythene sleeve cable-tied to a lamp column; skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape head_band (rect): box [12, 340, 285, 408], fill toner
  - `POLICE` | archivo 900 | cap 36 | centre 148.5 | base 358 | paper | B 12.95
  - `APPEAL FOR WITNESSES` | archivo 900 | cap 13.5 | centre 148.5 | base 300 | toner | B 12.95
  - `DID YOU SEE ANYTHING?` | archivo 800 | cap 14 | centre 148.5 | base 262 | toner | B 12.95
  - `ON THE NIGHT OF FRIDAY 12 OCTOBER,` | archivo 700 | cap 8 | left 24 | base 230 | toner | B 12.95
  - `BETWEEN 11 PM AND 1 AM,` | archivo 700 | cap 8 | left 24 | base 214.8 | toner | B 12.95
  - `A SHOP WINDOW ON QUAY STREET` | archivo 700 | cap 8 | left 24 | base 199.6 | toner | B 12.95
  - `WAS SMASHED.` | archivo 700 | cap 8 | left 24 | base 184.4 | toner | B 12.95
  - `IF YOU SAW OR HEARD ANYTHING,` | archivo 700 | cap 8 | left 24 | base 158.6 | toner | B 12.95
  - `HOWEVER SMALL, PLEASE TELEPHONE` | archivo 700 | cap 8 | left 24 | base 143.4 | toner | B 12.95
  - `THE INCIDENT ROOM ON 960 640,` | archivo 700 | cap 8 | left 24 | base 128.2 | toner | B 12.95
  - `OR CALL AT ANY POLICE STATION.` | archivo 700 | cap 8 | left 24 | base 113 | toner | B 12.95
  - `YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.` | archivo 600 | cap 6.5 | centre 148.5 | base 30 | toner | B 12.95

#### C01b  Police appeal for witnesses (b)

- 297 x 420 mm (A3); 6 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a3; event: SATURDAY 20 OCTOBER; dated: notice 1990-10-20
- variants: 2 (photocopy: a grey edge band 3 to 6 mm at the left, toner speckle; taped inside a window with four tabs of yellowed tape (the empty unit's glass, SF2: C01a), or in a polythene sleeve cable-tied to a lamp column; skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape head_band (rect): box [12, 340, 285, 408], fill toner
  - `POLICE` | archivo 900 | cap 36 | centre 148.5 | base 358 | paper | B 12.95
  - `APPEAL FOR WITNESSES` | archivo 900 | cap 13.5 | centre 148.5 | base 300 | toner | B 12.95
  - `DID YOU SEE ANYTHING?` | archivo 800 | cap 14 | centre 148.5 | base 262 | toner | B 12.95
  - `ON THE NIGHT OF SATURDAY 20 OCTOBER,` | archivo 700 | cap 8 | left 24 | base 230 | toner | B 12.95
  - `BETWEEN MIDNIGHT AND 6 AM,` | archivo 700 | cap 8 | left 24 | base 214.8 | toner | B 12.95
  - `A VAN WAS STOLEN FROM THE QUAY.` | archivo 700 | cap 8 | left 24 | base 199.6 | toner | B 12.95
  - `IF YOU SAW OR HEARD ANYTHING,` | archivo 700 | cap 8 | left 24 | base 173.8 | toner | B 12.95
  - `HOWEVER SMALL, PLEASE TELEPHONE` | archivo 700 | cap 8 | left 24 | base 158.6 | toner | B 12.95
  - `THE INCIDENT ROOM ON 960 640,` | archivo 700 | cap 8 | left 24 | base 143.4 | toner | B 12.95
  - `OR CALL AT ANY POLICE STATION.` | archivo 700 | cap 8 | left 24 | base 128.2 | toner | B 12.95
  - `YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.` | archivo 600 | cap 6.5 | centre 148.5 | base 30 | toner | B 12.95

#### C01c  Police appeal for witnesses (c)

- 297 x 420 mm (A3); 6 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a3; event: SUNDAY 28 OCTOBER; dated: notice 1990-10-28
- variants: 2 (photocopy: a grey edge band 3 to 6 mm at the left, toner speckle; taped inside a window with four tabs of yellowed tape (the empty unit's glass, SF2: C01a), or in a polythene sleeve cable-tied to a lamp column; skew is the PLACEMENT's rot_deg only: every texture is square-on (0.2 to 1.5 degrees))
- shape head_band (rect): box [12, 340, 285, 408], fill toner
  - `POLICE` | archivo 900 | cap 36 | centre 148.5 | base 358 | paper | B 12.95
  - `APPEAL FOR WITNESSES` | archivo 900 | cap 13.5 | centre 148.5 | base 300 | toner | B 12.95
  - `DID YOU SEE ANYTHING?` | archivo 800 | cap 14 | centre 148.5 | base 262 | toner | B 12.95
  - `ON THE NIGHT OF SUNDAY 28 OCTOBER,` | archivo 700 | cap 8 | left 24 | base 230 | toner | B 12.95
  - `BETWEEN 10 PM AND 11 PM,` | archivo 700 | cap 8 | left 24 | base 214.8 | toner | B 12.95
  - `A MAN WAS ASSAULTED NEAR THE QUAY.` | archivo 700 | cap 8 | left 24 | base 199.6 | toner | B 12.95
  - `IF YOU SAW OR HEARD ANYTHING,` | archivo 700 | cap 8 | left 24 | base 173.8 | toner | B 12.95
  - `HOWEVER SMALL, PLEASE TELEPHONE` | archivo 700 | cap 8 | left 24 | base 158.6 | toner | B 12.95
  - `THE INCIDENT ROOM ON 960 640,` | archivo 700 | cap 8 | left 24 | base 143.4 | toner | B 12.95
  - `OR CALL AT ANY POLICE STATION.` | archivo 700 | cap 8 | left 24 | base 128.2 | toner | B 12.95
  - `YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.` | archivo 600 | cap 6.5 | centre 148.5 | base 30 | toner | B 12.95

#### C02  Planning application notice (A4 in a sleeve)

- 210 x 297 mm (A4); 12 px/mm; stock: white copier paper, A4 or A3; process: photocopy_a4; event: FRIDAY 9 NOVEMBER; dated: event 1990-11-09
- variants: 2 (in a clear polythene sleeve, cable-tied to a lamp column or taped inside the empty unit's glass (SF2, number 7); water beads in the lower sleeve; a yellowing; skew is the PLACEMENT's rot_deg only: every texture is square-on)
- shape rule_a (rule): box [16, 262, 194, 264], fill toner
  - `PLANNING APPLICATION` | archivo 900 | cap 9 | centre 105 | base 270 | toner | B 12.95
  - `NOTICE` | archivo 700 | cap 6.5 | centre 105 | base 250 | toner | B 12.95
  - `PROPOSAL` | archivo 800 | cap 3.4 | left 22 | base 232 | toner | B 12.95
  - `Change of use of the ground floor, 7 Quay Street,` | old-standard-tt-regular 400 | cap 3.6 | left 22 | base 223.8 | toner | B 12.95
  - `from shop to estate agent's office.` | old-standard-tt-regular 400 | cap 3.6 | left 22 | base 215.6 | toner | B 12.95
  - `COMMENTS` | archivo 800 | cap 3.4 | left 22 | base 199.2 | toner | B 12.95
  - `Anyone wishing to comment may write to the Planning` | old-standard-tt-regular 400 | cap 3.6 | left 22 | base 191 | toner | B 12.95
  - `Officer by Friday 9 November.` | old-standard-tt-regular 400 | cap 3.6 | left 22 | base 182.8 | toner | B 12.95
  - `THE PLANS` | archivo 800 | cap 3.4 | left 22 | base 166.4 | toner | B 12.95
  - `may be seen at the Planning Department, Monday to` | old-standard-tt-regular 400 | cap 3.6 | left 22 | base 158.2 | toner | B 12.95
  - `Friday, 9 a.m. to 4.30 p.m.` | old-standard-tt-regular 400 | cap 3.6 | left 22 | base 150 | toner | B 12.95

#### C03  Temporary road closure notice (A3 in a sleeve)

- 297 x 420 mm (A3); 8 px/mm; stock: pale yellow copier paper; process: photocopy_a3; event: SUNDAY 4 NOVEMBER; dated: event 1990-11-04
- variants: 2 (cable-tied in a sleeve to a lamp column at 1.6 to 2.0 m, facing the street; the sleeve fogged inside, the notice yellowed, a cable tie tail left long)
- shape rule_a (rule): box [12, 352, 285, 355], fill toner
  - `HIGHWAYS DEPARTMENT` | archivo 800 | cap 9 | centre 148.5 | base 396 | toner | B 12.47
  - `NOTICE OF TEMPORARY ROAD CLOSURE` | archivo 900 | cap 8.5 | centre 148.5 | base 364 | toner | B 12.47
  - `QUAY STREET` | archivo 900 | cap 24.5 | centre 148.5 | base 300 | toner | B 12.47
  - `WILL BE CLOSED TO VEHICLES ON` | archivo 700 | cap 8.5 | centre 148.5 | base 262 | toner | B 12.47
  - `SUNDAY 4 NOVEMBER` | archivo 800 | cap 16 | centre 148.5 | base 235.5 | toner | B 12.47
  - `FROM 8 AM TO 6 PM` | archivo 800 | cap 14 | centre 148.5 | base 201.5 | toner | B 12.47
  - `FOR GAS MAIN RENEWAL.` | archivo 700 | cap 8.5 | centre 148.5 | base 169.5 | toner | B 12.47
  - `PEDESTRIAN ACCESS WILL BE MAINTAINED.` | archivo 700 | cap 8 | centre 148.5 | base 139 | toner | B 12.47
  - `DIVERSION VIA WEIGHHOUSE LANE.` | archivo 700 | cap 8 | centre 148.5 | base 117 | toner | B 12.47
  - `We apologise for any inconvenience.` | old-standard-tt-regular 400 | cap 6 | centre 148.5 | base 40 | toner | B 12.47

### 5.7 Shop-window cards and the newsagent's board

Cards are hand-lettered in Patrick Hand (felt pen and ballpoint) or printed. **Every hand-lettered card carries ONE cue matching its fixing, on its left half only** (a mirrored hand card cannot be told by its words at line level): a taped or stuck card has one tab of yellowed tape across its top-LEFT corner (K05, K06c, K07a-d, K09a-f, SA01-SA15); a string-hung card has the knot and sucker at its top-LEFT (K01, K06a). No crease, tear or pin-hole cue. Times and prices come from the world: LAST WASH 4.30 PM is an hour before the laundry's closing (8 to 5.30, `hook-cast.json`); cod 2.70 a lb is the ONS 1990 range (2.42 in January, 2.85 in December); smoked haddock is dearer than fresh; the other prices and the 20p-a-week advertising rate are Judgement. No card names a child, a pet shop, a drink, a pool or a lottery; no 'model' or 'companion' cards (tart cards are a content-rule line). Telephone numbers are the local six-figure form 960 xxx (the fictional range the cast's own 0632 960418 uses); none is Mickey's or one digit from it. K02 (BACK AT, Hal's break) is not placed: the newsagent never closes at midday.

#### K01  Closed for lunch card (felt pen)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 3 (the hour line is the one approved string 'BACK AT 2 O’CLOCK' (BACK AT 1.30 and 2.30 are not separate cards); hung on a string with a rubber sucker; slightly tilted (the placement's rot_deg); age class A to C)
- fixing and mirror cue: a string loop 220 mm long from a knot and a rubber sucker, at the card's top-LEFT only; the corner patches are [0.0, 123.0, 25.0, 148] (left) and [185.0, 123.0, 210.0, 148] (right)
  - `CLOSED FOR LUNCH` | patrick-hand 400 | cap 17 | centre 105 | base 92 | felt_red hand=felt | B 3.95
  - `BACK AT 2 O’CLOCK` | patrick-hand 400 | cap 14 | centre 105 | base 52 | felt_black hand=felt | B 12.53

#### K02  BACK AT clock card (printed; not placed)

- 130 x 170 mm (own size); 2 px/mm; stock: buff card, about 250 gsm; process: litho_2col
- variants: 2 (hands at 12 and at 2; hung on a string with a rubber sucker (NOT PLACED: hook-cast gives the newsagent no midday break, and Hal's shop is not on the built street))
- fixing and mirror cue: a string loop 220 mm long from a knot and a rubber sucker, at the card's top-LEFT only
- shape clock (roundel): box [20.0, 12.0, 110.0, 102.0], fill white - a printed clock face: white disc 90 mm across, black rim 2 mm
- shape ticks: 12 segments, 2.0 mm wide - twelve ticks 2 x 8 mm, from 35 to 43 mm out from the centre (no numerals: the hands would cover the 12)
- shape hand_hour (hand): centre [65.0, 57.0], 30.0 x 5.0 mm - hour hand, buff card, 30 x 5 mm, rounded end, set by the variant (12 or 2 o'clock)
- shape hand_min (hand): centre [65.0, 57.0], 40.0 x 4.0 mm - minute hand, buff card, 40 x 4 mm, pointing at 12
- shape fastener (roundel): box [62.0, 54.0, 68.0, 60.0], fill brass - a brass paper-fastener, 6 mm across, through both hands and the card
  - `BACK AT` | alfa-slab-one 400 | cap 17 | centre 65 | base 140 | red | B 3.18

#### K03a  OPEN / CLOSED hanging sign, face OPEN

- 200 x 110 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: plastic_print
- variants: 1 (one face outward at a time, from the shop's hours (hook-cast.json); the chain shows)
- shape face (rect): box [0, 0, 200, 110], fill agent_green - a plastic card, corners rounded 8 mm; a hole 5 mm across at the top centre, 8 mm down; a bead chain of 2.5 mm beads on a loop 60 mm long through the hole
- shape hole (roundel): box [97.5, 100.5, 102.5, 105.5], fill paper - the hanging hole, 5 mm across, centre 8 mm below the top edge
  - `OPEN` | archivo 800 | cap 40 | centre 100 | base 40 | agent_white | B 5.64

#### K03b  OPEN / CLOSED hanging sign, face CLOSED

- 200 x 110 mm (own size); 2 px/mm; stock: white card, about 250 gsm; process: plastic_print
- variants: 1 (one face outward at a time, from the shop's hours (hook-cast.json); the chain shows)
- shape face (rect): box [0, 0, 200, 110], fill agent_red - a plastic card, corners rounded 8 mm; a hole 5 mm across at the top centre, 8 mm down; a bead chain of 2.5 mm beads on a loop 60 mm long through the hole
- shape hole (roundel): box [97.5, 100.5, 102.5, 105.5], fill paper - the hanging hole, 5 mm across, centre 8 mm below the top edge
  - `CLOSED` | archivo 800 | cap 27 | centre 100 | base 40 | agent_white | B 4.98

#### K04  NO DOGS sticker, 150 x 105

- 150 x 105 mm (own size); 2 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (inside the glass of a shop door at 1.1 to 1.4 m, or outside on the door; one half peeled at a corner)
- shape roundel (ring): centre [43.0, 52.0], r 28.0 to 35.0 mm - a red ring 7 mm wide, 70 mm across; no dog silhouette (TARGET-REVIEW fault 11: the L3 sheet shows a bare ring)
- shape bar (poly): 4 points [[20.73, 69.32], [25.68, 74.27], [65.27, 34.68], [60.32, 29.73]], a bar 7 mm wide at 45 degrees from the ring's inside top-left to its inside bottom-right, same red
  - `NO` | archivo 900 | cap 12 | centre 112 | base 58 | black | B 13.0
  - `DOGS` | archivo 900 | cap 12 | centre 112 | base 36 | black | B 13.0

#### K05  PLEASE SHUT THE DOOR (felt pen)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped to a door's glass, bottom at 1.42 m (centre 1.494 m: just above the shop's vinyl trade lettering, which tops out at 1.385 m +- 0.03 on the fascia target); one with the second line underlined in red felt)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 123.0, 25.0, 148] (left) and [185.0, 123.0, 210.0, 148] (right)
  - `PLEASE SHUT` | patrick-hand 400 | cap 22 | centre 105 | base 96 | felt_black hand=felt | B 12.53
  - `THE DOOR` | patrick-hand 400 | cap 22 | centre 105 | base 56 | felt_black hand=felt | B 12.53

#### K06a  Launderette: LAST WASH (felt pen)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (the hour comes from the shop's closing time in hook-cast.json (laundry 8 to 5.30): LAST WASH is an hour before; hung inside the glass on a string and a rubber sucker)
- fixing and mirror cue: a string loop 220 mm long from a knot and a rubber sucker, at the card's top-LEFT only; the corner patches are [0.0, 123.0, 25.0, 148] (left) and [185.0, 123.0, 210.0, 148] (right)
  - `LAST WASH` | patrick-hand 400 | cap 22 | centre 105 | base 92 | felt_red hand=felt | B 3.95
  - `4.30 PM` | patrick-hand 400 | cap 26 | centre 105 | base 50 | felt_black hand=felt | B 12.53

#### K06b  Launderette: PLEASE DO NOT OVERLOAD (printed sticker)

- 210 x 148 mm (A5L); 3 px/mm; stock: white poster paper; process: sticker_print
- variants: 2 (stuck on the glass above a machine door)
  - `PLEASE DO NOT` | archivo 800 | cap 15 | centre 105 | base 119 | black | B 13.0
  - `OVERLOAD` | archivo 900 | cap 21 | centre 105 | base 90 | red | B 3.99
  - `THE MACHINES` | archivo 800 | cap 15 | centre 105 | base 67 | black | B 13.0

#### K06c  OUT OF ORDER (felt pen)

- 148 x 105 mm (A6L); 2 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 3 (taped on a machine door or the glass; the tab lifting at one end)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 80.0, 25.0, 105] (left) and [123.0, 80.0, 148.0, 105] (right)
  - `OUT OF` | patrick-hand 400 | cap 14 | centre 74 | base 66 | felt_red hand=felt | B 3.95
  - `ORDER` | patrick-hand 400 | cap 14 | centre 74 | base 38 | felt_red hand=felt | B 3.95

#### K07a  Grocer's star card

- 170 x 170 mm (own size); 6 px/mm; stock: fluorescent yellow star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [23.1, 132.2, 48.1, 157.2] (left) and [121.9, 132.2, 146.9, 157.2] (right)
- shape star (star): 28 points (see target.json), the card is cut to a 14-point burst (outer radius 84, inner 62); the stock colour is the star; outside it the card is transparent
  - `SPECIAL OFFER` | patrick-hand 400 | cap 9 | centre 85 | base 100 | felt_black hand=felt | B 11.69
  - `TEA BAGS` | patrick-hand 400 | cap 13 | centre 85 | base 77 | felt_black hand=felt | B 11.69
  - `80 FOR 99p` | patrick-hand 400 | cap 15 | centre 85 | base 55 | felt_red hand=felt | B 3.71

#### K07b  Grocer's star card

- 170 x 170 mm (own size); 6 px/mm; stock: fluorescent pink star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [23.1, 132.2, 48.1, 157.2] (left) and [121.9, 132.2, 146.9, 157.2] (right)
- shape star (star): 28 points (see target.json), the card is cut to a 14-point burst (outer radius 84, inner 62); the stock colour is the star; outside it the card is transparent
  - `NEW SEASON` | patrick-hand 400 | cap 9 | centre 85 | base 100 | felt_black hand=felt | B 6.02
  - `CABBAGE` | patrick-hand 400 | cap 14 | centre 85 | base 76.5 | felt_black hand=felt | B 6.02
  - `20p lb` | patrick-hand 400 | cap 15 | centre 85 | base 55 | felt_black hand=felt | B 6.02

#### K07c  Grocer's star card

- 170 x 170 mm (own size); 6 px/mm; stock: fluorescent orange star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [23.1, 132.2, 48.1, 157.2] (left) and [121.9, 132.2, 146.9, 157.2] (right)
- shape star (star): 28 points (see target.json), the card is cut to a 14-point burst (outer radius 84, inner 62); the stock colour is the star; outside it the card is transparent
  - `BIG SAVER` | patrick-hand 400 | cap 10 | centre 85 | base 99.5 | felt_black hand=felt | B 6.73
  - `TINNED PEARS` | patrick-hand 400 | cap 11 | centre 85 | base 78 | felt_black hand=felt | B 6.73
  - `2 FOR 69p` | patrick-hand 400 | cap 15 | centre 85 | base 55 | felt_black hand=felt | B 6.73

#### K07d  Grocer's star card

- 170 x 170 mm (own size); 4 px/mm; stock: fluorescent yellow star card; process: felt_pen
- variants: 2 (taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [23.1, 132.2, 48.1, 157.2] (left) and [121.9, 132.2, 146.9, 157.2] (right)
- shape star (star): 28 points (see target.json), the card is cut to a 14-point burst (outer radius 84, inner 62); the stock colour is the star; outside it the card is transparent
  - `FRESH EGGS` | patrick-hand 400 | cap 13 | centre 85 | base 87.5 | felt_black hand=felt | B 11.69
  - `85p DOZEN` | patrick-hand 400 | cap 15 | centre 85 | base 65.5 | felt_red hand=felt | B 3.71

#### K08  SORRY NO CREDIT GIVEN (printed card)

- 210 x 148 mm (A5L); 2 px/mm; stock: white card, about 250 gsm; process: letterpress_2col
- variants: 2 (on a shop counter's glass screen or the door)
  - `SORRY` | archivo 900 | cap 20 | centre 105 | base 108 | red | B 4.13
  - `NO CREDIT GIVEN` | archivo 900 | cap 12.5 | centre 105 | base 85.5 | black | B 13.62

#### K09a  Fish price ticket: COD FILLET

- 105 x 74 mm (own size); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped inside the glass at the slab's height, one tab at the top-left; a wet corner)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 49.0, 25.0, 74] (left) and [80.0, 49.0, 105.0, 74] (right)
  - `COD FILLET` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.70 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09b  Fish price ticket: HADDOCK

- 105 x 74 mm (own size); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped inside the glass at the slab's height, one tab at the top-left; a wet corner)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 49.0, 25.0, 74] (left) and [80.0, 49.0, 105.0, 74] (right)
  - `HADDOCK` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.50 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09c  Fish price ticket: PLAICE

- 105 x 74 mm (own size); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped inside the glass at the slab's height, one tab at the top-left; a wet corner)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 49.0, 25.0, 74] (left) and [80.0, 49.0, 105.0, 74] (right)
  - `PLAICE` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.30 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09d  Fish price ticket: KIPPERS

- 105 x 74 mm (own size); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped inside the glass at the slab's height, one tab at the top-left; a wet corner)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 49.0, 25.0, 74] (left) and [80.0, 49.0, 105.0, 74] (right)
  - `KIPPERS` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `95p PAIR` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09e  Fish price ticket: SMOKED HADDOCK

- 105 x 74 mm (own size); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped inside the glass at the slab's height, one tab at the top-left; a wet corner)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 49.0, 25.0, 74] (left) and [80.0, 49.0, 105.0, 74] (right)
  - `SMOKED HADDOCK` | patrick-hand 400 | cap 8.5 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `£2.90 lb` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

#### K09f  Fish price ticket: COCKLES

- 105 x 74 mm (own size); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 2 (taped inside the glass at the slab's height, one tab at the top-left; a wet corner)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 49.0, 25.0, 74] (left) and [80.0, 49.0, 105.0, 74] (right)
  - `COCKLES` | patrick-hand 400 | cap 13 | centre 52.5 | base 46 | felt_black hand=felt_fine | B 12.53
  - `45p TUB` | patrick-hand 400 | cap 15 | centre 52.5 | base 16 | felt_red hand=felt | B 3.95

**The newsagent's board SB1** (760 x 560 mm on the glass at u 1.95 m, z 0.90 m): fifteen cards of two sizes (127 x 76 record cards, 148 x 105 postcards), every one taped by a single tab at its top-left (pins are for a cork board).

| Card | at (x, y) mm | size | rot | fixing |
|---|---|---|---|---|
| SA15 | 23, 428 | 148 x 105 | -2.0 | tape: one tab across the top-left corner |
| SA01 | 205, 468 | 127 x 76 | 2.3 | tape: one tab across the top-left corner |
| SA02 | 364, 462 | 127 x 76 | -1.8 | tape: one tab across the top-left corner |
| SA03 | 514, 430 | 148 x 105 | -0.3 | tape: one tab across the top-left corner |
| SA04 | 21, 331 | 127 x 76 | 1.6 | tape: one tab across the top-left corner |
| SA05 | 183, 325 | 127 x 76 | 2.3 | tape: one tab across the top-left corner |
| SA06 | 348, 310 | 148 x 105 | -0.9 | tape: one tab across the top-left corner |
| SA07 | 537, 326 | 127 x 76 | -0.3 | tape: one tab across the top-left corner |
| SA08 | 19, 197 | 127 x 76 | 1.1 | tape: one tab across the top-left corner |
| SA09 | 188, 176 | 148 x 105 | -1.0 | tape: one tab across the top-left corner |
| SA10 | 364, 192 | 127 x 76 | 1.7 | tape: one tab across the top-left corner |
| SA11 | 522, 194 | 127 x 76 | 2.0 | tape: one tab across the top-left corner |
| SA12 | 14, 63 | 127 x 76 | -0.3 | tape: one tab across the top-left corner |
| SA13 | 189, 71 | 127 x 76 | -1.8 | tape: one tab across the top-left corner |
| SA14 | 356, 63 | 127 x 76 | 0.7 | tape: one tab across the top-left corner |

#### SA01  Newsagent window card 01

- 127 x 76 mm (own size); 12 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `ROOM TO LET` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.81
  - `Clean, quiet, gas fire.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_black hand=ballpoint | B 11.13
  - `£28 per week. No pets.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_black hand=ballpoint | B 11.13
  - `Ring 960 471 after 5.` | patrick-hand 400 | cap 4.4 | left 8 | base 31.6 | ballpoint_black hand=ballpoint | B 11.13

#### SA02  Newsagent window card 02

- 127 x 76 mm (own size); 12 px/mm; stock: blue record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `GENTS BICYCLE` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 9.97
  - `3-speed, good tyres.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 5.79
  - `£18 or nearest offer.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 5.79
  - `Tel. 960 233.` | patrick-hand 400 | cap 4.4 | left 8 | base 31.6 | ballpoint_blue hand=ballpoint | B 5.79

#### SA03  Newsagent window card 03

- 148 x 105 mm (own size); 12 px/mm; stock: yellow record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 80.0, 25.0, 105] (left) and [123.0, 80.0, 148.0, 105] (right)
  - `PIANO FOR SALE` | patrick-hand 400 | cap 7 | left 8 | base 89.5 | felt_black hand=felt_fine | B 11.54
  - `Upright, good tone.` | patrick-hand 400 | cap 4.4 | left 8 | base 78.6 | ballpoint_blue hand=ballpoint | B 6.74
  - `Buyer collects. £120.` | patrick-hand 400 | cap 4.4 | left 8 | base 69.6 | ballpoint_blue hand=ballpoint | B 6.74
  - `Ring 960 528.` | patrick-hand 400 | cap 4.4 | left 8 | base 60.6 | ballpoint_blue hand=ballpoint | B 6.74

#### SA04  Newsagent window card 04

- 127 x 76 mm (own size); 12 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `WINDOW CLEANER` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.81
  - `Reliable. Free estimates.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Tel. 960 361.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA05  Newsagent window card 05

- 127 x 76 mm (own size); 12 px/mm; stock: pink record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `DECORATING` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 9.56
  - `Indoor and out.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_black hand=ballpoint | B 8.4
  - `Fair prices. 960 774.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_black hand=ballpoint | B 8.4

#### SA06  Newsagent window card 06

- 148 x 105 mm (own size); 12 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 80.0, 25.0, 105] (left) and [123.0, 80.0, 148.0, 105] (right)
  - `LOST` | patrick-hand 400 | cap 7 | left 8 | base 89.5 | felt_black hand=felt_fine | B 12.68
  - `Black and white cat,` | patrick-hand 400 | cap 4.4 | left 8 | base 78.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `answers to Smudge.` | patrick-hand 400 | cap 4.4 | left 8 | base 69.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Last seen on Quay Street.` | patrick-hand 400 | cap 4.4 | left 8 | base 60.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Reward. 960 189.` | patrick-hand 400 | cap 4.4 | left 8 | base 51.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA07  Newsagent window card 07

- 127 x 76 mm (own size); 12 px/mm; stock: green record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `FOUND` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 5.69
  - `Bunch of keys on` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 6.12
  - `Quay Street. Enquire within.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 6.12

#### SA08  Newsagent window card 08

- 127 x 76 mm (own size); 12 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `TYPING DONE AT HOME` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 12.68
  - `Letters and CVs.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `960 842.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA09  Newsagent window card 09

- 148 x 105 mm (own size); 12 px/mm; stock: blue record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 80.0, 25.0, 105] (left) and [123.0, 80.0, 148.0, 105] (right)
  - `MAN WITH VAN` | patrick-hand 400 | cap 7 | left 8 | base 89.5 | felt_black hand=felt_fine | B 9.97
  - `Removals and house` | patrick-hand 400 | cap 4.4 | left 8 | base 78.6 | ballpoint_black hand=ballpoint | B 8.79
  - `clearance. Anywhere.` | patrick-hand 400 | cap 4.4 | left 8 | base 69.6 | ballpoint_black hand=ballpoint | B 8.79
  - `960 655.` | patrick-hand 400 | cap 4.4 | left 8 | base 60.6 | ballpoint_black hand=ballpoint | B 8.79

#### SA10  Newsagent window card 10

- 127 x 76 mm (own size); 12 px/mm; stock: yellow record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `GAS COOKER` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.32
  - `4 ring, hardly used.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 6.74
  - `£35. Ring 960 307.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 6.74

#### SA11  Newsagent window card 11

- 127 x 76 mm (own size); 12 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `WANTED` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 12.68
  - `Part-time help, mornings.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 7.31
  - `Apply within.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 7.31

#### SA12  Newsagent window card 12

- 127 x 76 mm (own size); 12 px/mm; stock: pink record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `SEWING MACHINE` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 9.56
  - `Electric. £25.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 5.6
  - `Tel. 960 912.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 5.6

#### SA13  Newsagent window card 13

- 127 x 76 mm (own size); 12 px/mm; stock: white record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `COLOUR TV` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_blue hand=felt_fine | B 6.81
  - `22 inch, working. £40.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_black hand=ballpoint | B 11.13
  - `Ring 960 483.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_black hand=ballpoint | B 11.13

#### SA14  Newsagent window card 14

- 127 x 76 mm (own size); 12 px/mm; stock: green record card; process: ballpoint_card
- variants: 1 (taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg))
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 51.0, 25.0, 76] (left) and [102.0, 51.0, 127.0, 76] (right)
  - `CHIMNEY SWEEP` | patrick-hand 400 | cap 7 | left 8 | base 60.5 | felt_black hand=felt_fine | B 10.4
  - `Clean and tidy.` | patrick-hand 400 | cap 4.4 | left 8 | base 49.6 | ballpoint_blue hand=ballpoint | B 6.12
  - `960 596.` | patrick-hand 400 | cap 4.4 | left 8 | base 40.6 | ballpoint_blue hand=ballpoint | B 6.12

#### SA15  Newsagent: ADVERTISE HERE card

- 148 x 105 mm (A6L); 4 px/mm; stock: white card, about 250 gsm; process: felt_pen
- variants: 1 (top of the board, taped by one tab at the top-left)
- fixing and mirror cue: one tab of yellowed adhesive tape across the card's top-LEFT corner only; the corner patches are [0.0, 80.0, 25.0, 105] (left) and [123.0, 80.0, 148.0, 105] (right)
  - `ADVERTISE HERE` | patrick-hand 400 | cap 12 | centre 74 | base 80 | felt_red hand=felt | B 3.95
  - `20p PER WEEK` | patrick-hand 400 | cap 14 | centre 74 | base 56 | felt_black hand=felt | B 12.53
  - `PAY AT THE COUNTER` | patrick-hand 400 | cap 8 | centre 74 | base 34 | felt_black hand=felt_fine | B 12.53

## 6. "To Let" boards (unit 4.3)

**The default board is the fascia target's board, exactly** (`small_panels.letting_board`): **900 x 450 mm, white face, TO LET alone in Libre Franklin 800, cap 130, vinyl red (176,30,34), no agent, no number**, four screws slightly askew, a rust run under each lower screw; `G.letting.mount` compares size, text, font, weight, cap and colour with the fascia target's file and fails the first try's 1200 x 450 board. 450 mm is the height a 0.55 m fascia takes with 50 mm clear above and below. The agent board L01 (1200 x 450, ARMITAGE & STOBBS, Chartered Surveyors, Estate Agents, a number) and the flat board L03 carry a PROPOSED agent (not minted; not checked against real firms, the network refusing the sources): they are held variants, and using L01 would need the fascia target's entry changed in the same batch with one DECISIONS line. The flat above the empty unit carries the no-agent L03n (the L04 layout at 600 x 400: TO LET, SELF-CONTAINED FLAT, ENQUIRIES 960 335); the house board L04 stays. A letting board is white gloss on 18 mm exterior plywood, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten at each end, four 8 mm dome-head coach screws 40 mm in from the corners with a rust run 40 to 140 mm under each lower one, hung 2 degrees askew (the placement's rot_deg). Colours: agent navy (28,46,94), red (178,34,40), white (236,236,230); at class D the white yellows to (214,206,184) and the red fades towards chalk-pink by 0.3. Fonts: Jost for the agent boards (the asset-plan table), Libre Franklin for L02 (the fascia target's).

#### L02  Letting board, empty unit (the fascia target's board: 900 x 450, TO LET)

- 900 x 450 mm (own size); 2 px/mm; process: agent_board
- variants: 3 (askew -2, 0, +2 degrees (the placement's rot_deg); age class B, C, D (the D board has the white yellowed and the red faded to rust-pink); four screws, a rust run under each lower one (fascia target))
- shape face (rect): box [0, 0, 900, 450], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end; no border, no band (the fascia target's board has none)
  - `TO LET` | libre-franklin 800 | cap 130 | centre 450 | base 160 | vinyl_red | B 5.15

- mounted on: the empty unit's fascia (bay 3, east, street x 21 to 27; number 7); centre street x 24.0 m; z 2.9 to 3.35 m; four 8 mm dome-head coach screws at 40 mm in from each corner; a rust run 40 to 140 mm under each lower screw; askew -2 to +2 degrees. the fascia is 0.55 m tall (2.85 to 3.40): the board leaves 50 mm above and below; its centre is the fascia target's own letting-board centre (board x 2705, y 275)

#### L01  Letting board, shop, with agent (1200 x 450; NOT the fascia target's board; named agent, held)

- 1200 x 450 mm (own size); 2 px/mm; process: agent_board; HELD until minted: ARMITAGE & STOBBS
- variants: 3 (askew -2, 0, +2 degrees; age class B, C, D (the D board has the white yellowed and the red faded to rust-pink); NOT used by default: it disagrees with the fascia target (900 x 450, TO LET only); using it needs the fascia target changed in the same batch with one DECISIONS line)
- shape face (rect): box [0, 0, 1200, 450], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape band (rect): box [0, 332, 1200, 450], fill agent_navy
  - `ARMITAGE & STOBBS` | jost 700 | cap 52 | centre 600 | base 384 | agent_white | B 8.94
  - `CHARTERED SURVEYORS · ESTATE AGENTS` | jost 500 | cap 18.7 | centre 600 | base 342 | agent_white | B 8.94
  - `TO LET` | jost 800 | cap 150 | centre 600 | base 164 | agent_red | B 4.98
  - `SHOP AND PREMISES · APPROX. 520 SQ. FT.` | jost 600 | cap 24 | centre 600 | base 127.4 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 46 | centre 600 | base 63.4 | agent_navy | B 8.94

- mounted on: the empty unit's fascia (bay 3, east, street x 21 to 27; number 7); centre street x 24.0 m; z 2.9 to 3.35 m; four 8 mm dome-head coach screws at 40 mm in from each corner; a rust run 40 to 140 mm under each lower screw; askew -2 to +2 degrees. the fascia is 0.55 m tall (2.85 to 3.40): the board leaves 50 mm above and below; its centre is the fascia target's own letting-board centre (board x 2705, y 275)

#### L03  Letting board, flat, with agent (600 x 400; named agent, held)

- 600 x 400 mm (own size); 3 px/mm; process: agent_board; HELD until minted: ARMITAGE & STOBBS
- variants: 2 (age class C, D; the agent's board has been up a long time: grime streaks from the top edge)
- shape face (rect): box [0, 0, 600, 400], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape band (rect): box [0, 316, 600, 400], fill agent_navy
  - `ARMITAGE & STOBBS` | jost 700 | cap 30 | centre 300 | base 356 | agent_white | B 8.94
  - `CHARTERED SURVEYORS · ESTATE AGENTS` | jost 500 | cap 10.8 | centre 300 | base 326 | agent_white | B 8.94
  - `TO LET` | jost 800 | cap 106 | centre 300 | base 182 | agent_red | B 4.98
  - `SELF-CONTAINED FLAT` | jost 600 | cap 24 | centre 300 | base 138.4 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 34 | centre 300 | base 76.4 | agent_navy | B 8.94

- mounted on: first-floor brick above the empty unit's cornice, between the two upper windows; centre street x 24.0 m; z 3.7 to 4.1 m; four 6 mm screws and plugs; askew -1.5 to +1.5 degrees. the cornice top is 3.55 m, the upper sill about 4.3 m (facade: head 0.4 below the ceiling, window 1.5 high): 0.75 m of plain brick; Rita's hanging sign is at street x 20.825 and the laundry's at 27.175, both outside bay 3

#### L03n  Letting board, flat, no agent (600 x 400)

- 600 x 400 mm (own size); 2 px/mm; process: agent_board
- variants: 2 (age class C, D; grime streaks from the top edge)
- shape face (rect): box [0, 0, 600, 400], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape hairline (frame): box [12, 12, 588, 388], fill agent_navy
  - `TO LET` | jost 800 | cap 104 | centre 300 | base 237.5 | agent_red | B 4.98
  - `SELF-CONTAINED FLAT` | jost 600 | cap 26 | centre 300 | base 178.9 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 32 | centre 300 | base 100.4 | agent_navy | B 8.94

- mounted on: first-floor brick above the empty unit's cornice, between the two upper windows; centre street x 24.0 m; z 3.7 to 4.1 m; four 6 mm screws and plugs; askew -1.5 to +1.5 degrees. the cornice top is 3.55 m, the upper sill about 4.3 m (facade: head 0.4 below the ceiling, window 1.5 high): 0.75 m of plain brick; Rita's hanging sign is at street x 20.825 and the laundry's at 27.175, both outside bay 3

#### L04  Letting board, house, no agent (600 x 400)

- 600 x 400 mm (own size); 2 px/mm; process: agent_board
- variants: 2 (age class B, D)
- shape face (rect): box [0, 0, 600, 400], fill agent_white - 18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end
- shape hairline (frame): box [12, 12, 588, 388], fill agent_navy
  - `TO LET` | jost 800 | cap 104 | centre 300 | base 238.5 | agent_red | B 4.98
  - `TWO BEDROOMS` | jost 600 | cap 30 | centre 300 | base 176.7 | agent_navy | B 8.94
  - `ENQUIRIES 960 335` | jost 700 | cap 32 | centre 300 | base 99.2 | agent_navy | B 8.94

- mounted on: the west terrace (bay 2 of the plain block, street x 15 to 21): the brick pier between the two windows; centre street x 16.8 m; z 2.15 to 2.55 m; four 6 mm screws and plugs; askew -1.5 to +1.5 degrees. pier 16.35 to 17.25 (window 15.9 and 17.7, 0.85 wide, from the plain row's bay layout, mirrored in bay 2); the board is 0.6 wide

## 7. Street name plates (unit 4.4)

**What 1990 British plates carried, as far as I could establish.** No photograph was reached. From search summaries (Leads): there was never a national design and each council chose its own style, colour, size and material; black capitals on white with a black border was the default the 1993 Department of Transport circular recommends and the usual look; the Ministry of Transport's alphabets date from the early 1930s, the Kindersley lettering was adopted in 1951 and recommended in 1952, by which time raised plates were cast aluminium, not iron; Hull's cast plates of the 1920s to 1930s were black on white and their paint faded or flaked; London plates carried the borough and the postal district. I found NO source that provincial plates of the 1980s carried a district line or a postal district, and the project's own street-clutter note describes a plain plate and lists postcodes as wrong for 1990. **What the target says (second try):** the default and the placed plate is `n`, the name only; `d` (the name and a district's name as a small line: THE HOOK, COPPER ROW, IRONSIDE) stays a variant until a dated photograph shows a district line; the postal-district variant (MR1) is deleted; no council, no crest (canon owes the council's name). **Letter style:** Marcellus SC capitals, 90 mm tall, tracking +0.04 em, ruled on 30 September for the street plates (it stands in for the Kindersley serif, which has no allowed free version).

**Sizes.** Plate length follows the name: ink width plus 2 x 62 mm (6 mm edge + 12 mm border + 44 mm clear), rounded up to 10 mm. **Depth at least 200 mm** (the street-clutter note's 20 to 25 cm; the first try's 170 mm `n` plates were too shallow): 200 mm for `n`, 220 or 240 mm with a district line (Quay Street's Q dips 36 mm below the baseline). The border band is 12 mm, 6 mm in from the edge; corners rounded 6 mm. Fixing: four screws 30 mm in from the corners (10 mm dome heads into fibre plugs; the cast plate has four 12 mm holes cast in). Mounting height: bottom edge at about 2.5 m, centre 2.63 m (the earlier note says 2.2 to 2.5 m, the existing plate hangs at 2.50 to 2.76).

**Makes, by street (Judgement), with numbers.** QUAY STREET: cast aluminium (by the 1950s raised plates were cast aluminium, not iron), a face 6 mm thick, letters and border raised 3 mm, painted white with black letters, the paint flaking first from the raised edges to bare grey aluminium; a plain cast edge 6 mm thick with a 2 mm arris radius. WEIGHHOUSE LANE: die-pressed aluminium 2 mm, letters and border raised 1.5 mm, stove enamel, a rolled edge of 3 mm radius. TANNERY ROW: vitreous enamel on pressed steel, flat, a rolled edge of 6 mm radius. **Raised letters and border: 10 degrees of draft each side and a 0.8 mm radius on the top edge.** **The lettering suits the make** (`lettering_suit`, Derived from the rendered glyphs' distance transform): Marcellus SC's thinnest stroke at 90 mm capitals is 6.0 mm and its thickest 12.1 mm; after 3 mm of relief at 10 degrees a cast hairline keeps a top width of 4.94 mm (1.5 mm needed to cast), a pressed 1.5 mm relief 5.47 mm. `G.plates.make` checks it.

| Plate | street | district | variant | plate (mm) | ink width | material |
|---|---|---|---|---|---|---|
| S01n | QUAY STREET | (none) | n | 980 x 200 | 855.0 | cast_aluminium_raised |
| S01d | QUAY STREET | THE HOOK | d | 980 x 240 | 855.0 | cast_aluminium_raised |
| S02n | WEIGHHOUSE LANE | (none) | n | 1360 x 200 | 1234.0 | pressed_aluminium_enamel |
| S02d | WEIGHHOUSE LANE | COPPER ROW | d | 1360 x 220 | 1234.0 | pressed_aluminium_enamel |
| S03n | TANNERY ROW | (none) | n | 1100 x 200 | 968.0 | vitreous_enamel_steel |
| S03d | TANNERY ROW | IRONSIDE | d | 1100 x 220 | 968.0 | vitreous_enamel_steel |

Placed: **S01n** at street x 20.47 on the west corner pier (x 19.92 to 21.0, brick to 3.12 m: the existing plate's place, kept, 80 mm of pier either side), centre z 2.63. **The quay gable carries no plate**: the Hook sheet shows none there, and one plate on a 48 m street is enough; a second S01n at u 1.0 (centre z 2.63) is a HELD placement. **NO plate stands on the yard entrance** (street x 21 to 24, the dropped kerb at 22.5): the scene file calls it the yard entrance and atlas-01 gives it as `yard_gap_x [21, 24]`; the atlas runs Weighhouse Lane about 200 m beyond the built 48 m, so naming the gap is a map fact the town has settled. **S02 (WEIGHHOUSE LANE) and S03 (TANNERY ROW)** are kit plates for the town and are not placed on Quay Street. The plate board's pictures: `L4` shows all six.

#### S01n  Street name plate: QUAY STREET (name only: the default)

- relief: raised 3.0 mm, draft 10.0 degrees, top radius 0.8 mm; edge: a plain cast edge 6 mm thick with a 2 mm arris radius; face 6 mm thick; letters and border raised 3 mm
  - `QUAY STREET` | marcellus-sc | cap 90 | centre 490 | base 66 | B 11.67

#### S01d  Street name plate: QUAY STREET (name and district line: a variant)

- relief: raised 3.0 mm, draft 10.0 degrees, top radius 0.8 mm; edge: a plain cast edge 6 mm thick with a 2 mm arris radius; face 6 mm thick; letters and border raised 3 mm
  - `QUAY STREET` | marcellus-sc | cap 90 | centre 490 | base 60 | B 11.67
  - `THE HOOK` | marcellus-sc | cap 30 | centre 490 | base 172 | B 11.67

#### S02n  Street name plate: WEIGHHOUSE LANE (name only: the default)

- relief: raised 1.5 mm, draft 10.0 degrees, top radius 0.8 mm; edge: rolled edge, radius 3 mm; 2 mm sheet; letters and border raised 1.5 mm by the press
  - `WEIGHHOUSE LANE` | marcellus-sc | cap 90 | centre 680 | base 57 | B 11.67

#### S02d  Street name plate: WEIGHHOUSE LANE (name and district line: a variant)

- relief: raised 1.5 mm, draft 10.0 degrees, top radius 0.8 mm; edge: rolled edge, radius 3 mm; 2 mm sheet; letters and border raised 1.5 mm by the press
  - `WEIGHHOUSE LANE` | marcellus-sc | cap 90 | centre 680 | base 41 | B 11.67
  - `COPPER ROW` | marcellus-sc | cap 30 | centre 680 | base 153 | B 11.67

#### S03n  Street name plate: TANNERY ROW (name only: the default)

- relief: none (flat enamel); edge: rolled edge, radius 6 mm; flat vitreous enamel, no relief
  - `TANNERY ROW` | marcellus-sc | cap 90 | centre 550 | base 57 | B 11.67

#### S03d  Street name plate: TANNERY ROW (name and district line: a variant)

- relief: none (flat enamel); edge: rolled edge, radius 6 mm; flat vitreous enamel, no relief
  - `TANNERY ROW` | marcellus-sc | cap 90 | centre 550 | base 41 | B 11.67
  - `IRONSIDE` | marcellus-sc | cap 30 | centre 550 | base 153 | B 11.67

## 8. The paste plan: placements

Layers run from the oldest (0) to the newest; age class A to D is the paper's age on the street date (section 4). Placements marked HELD are not in the default street: the named twins of a default placement and the nameless stand-ins (built only after the town mints their names: `G.page.placeholders`, section 12) and the five `proof_wall` placements of the quay gable (P01, W01, T02, T02s and a second QUAY STREET plate), which the bare gable holds back. The gable's `proof_wall` set is the plan's sample, kept for the case that he chooses the gable.

| Surface | Item | where | z bottom (m) | rot | layer | age | size (m) | notes |
|---|---|---|---|---|---|---|---|---|
| SF1 | P01 | u 0.700 | 1.00 | -0.6 | 0 | B | 0.508 x 0.762 | HELD (the bare gable); proof_wall |
| SF1 | W01 | u 1.300 | 1.00 | 0.5 | 0 | A | 0.508 x 0.762 | HELD (THE DRILL HALL, THE HARPOONER, SPANNER SMITH, TED HOLROYD, THE STEVEDORE); proof_wall |
| SF1 | T02 | u 1.900 | 1.00 | -0.4 | 0 | A | 1.016 x 0.762 | HELD (MARSHLAND PICTURES, H. MADDOX, A WEEK AT GULLWING); proof_wall |
| SF1 | T02s | u 1.903 | 1.68 | -0.15 | 1 | A | 1.016 x 0.090 | HELD (the bare gable); proof_wall |
| SF2 | C01a | u 0.300 | 1.30 | 0.3 | 1 | B | 0.297 x 0.420 |  |
| SF2 | M01 | u 0.750 | 0.80 | 0.8 | 0 | C | 0.508 x 0.762 |  |
| SF2 | P03 | u 1.350 | 0.85 | 1.2 | 0 | B | 0.508 x 0.762 |  |
| SF2 | P02 | u 1.950 | 0.82 | 0.6 | 0 | B | 0.508 x 0.762 |  |
| SF2 | J01 | u 2.600 | 1.05 | -0.8 | 0 | B | 0.297 x 0.420 |  |
| SF2 | C02 | u 3.010 | 1.50 | 0.0 | 1 | A | 0.210 x 0.297 |  |
| WEST_PIER | M01 | street x 11.397 pier W1.0 | 1.00 | 0.0 | 0 | B | 0.508 x 0.762 |  |
| WEST_PIER | L04 | street x 16.8 pier W2.0 | 2.15 | 0.0 | 2 | C | 0.600 x 0.400 |  |
| SF9 | P02 | street x 12.3 | 1.45 | 0.0 | 0 | A | 0.297 x 0.446 | scale 0.585 |
| SF4 | C03 | street x 8.0 | 1.55 | 0.0 | 1 | A | 0.297 x 0.420 |  |
| SF4 | P05 | street x 8.0 | 1.25 | 0.0 | 1 | C | 0.095 x 0.060 |  |
| SF4 | P06 | street x 28.0 | 1.45 | 0.0 | 1 | B | 0.148 x 0.052 |  |
| SF4 | P05 | street x 28.0 | 1.85 | 0.0 | 1 | D | 0.095 x 0.060 |  |
| SF5 | L02 | street x 24.0 | 2.90 | -1.5 | 0 | C | 0.900 x 0.450 |  |
| SF6 | L03n | street x 24.0 | 3.70 | 1.0 | 0 | C | 0.600 x 0.400 |  |
| SF7 | S01n | street x 20.47 | 2.53 | 0.0 | 0 | D | 0.980 x 0.200 |  |
| SF7 | S01n | u 0.510 | 2.53 | 0.0 | 0 | D | 0.980 x 0.200 | HELD (the bare gable); proof_wall |
| SF8 | H02 | street x -0.6 | 1.20 | 0.0 | 0 | C | 0.600 x 0.450 |  |
| SF1 | P01-named | u 0.700 | 1.00 | -0.6 | 0 | B | 0.508 x 0.762 | HELD (MERIDIAN AGAINST THE POLL TAX); proof_wall |
| SF1 | W01-named | u 1.300 | 1.00 | 0.5 | 0 | A | 0.508 x 0.762 | HELD (THE DRILL HALL, THE HARPOONER, SPANNER SMITH, TED HOLROYD, THE STEVEDORE); proof_wall |
| SF1 | T02-named | u 1.900 | 1.00 | -0.4 | 0 | A | 1.016 x 0.762 | HELD (MARSHLAND PICTURES, H. MADDOX, A WEEK AT GULLWING); proof_wall |
| SF2 | P03-named | u 1.350 | 0.85 | 1.2 | 0 | B | 0.508 x 0.762 | HELD (MERIDIAN AGAINST THE POLL TAX) |
| SF2 | P02-named | u 1.950 | 0.82 | 0.6 | 0 | B | 0.508 x 0.762 | HELD (MERIDIAN AGAINST THE POLL TAX) |
| SF9 | P02-named | street x 12.3 | 1.45 | 0.0 | 0 | A | 0.297 x 0.446 | HELD (MERIDIAN AGAINST THE POLL TAX); scale 0.585 |
| SF5 | L01 | street x 24.0 | 2.90 | -1.5 | 0 | C | 1.200 x 0.450 | HELD (ARMITAGE & STOBBS) |
| SF6 | L03 | street x 24.0 | 3.70 | 1.0 | 0 | C | 0.600 x 0.400 | HELD (ARMITAGE & STOBBS) |
| SHOP | K09a | fish_market glass u 0.30 | 0.66 | -2 | 1 | B | 0.105 x 0.074 |  |
| SHOP | K09b | fish_market glass u 0.95 | 0.66 | 3 | 1 | B | 0.105 x 0.074 |  |
| SHOP | K09c | fish_market glass u 1.60 | 0.66 | -1 | 1 | B | 0.105 x 0.074 |  |
| SHOP | K09d | fish_market glass u 2.25 | 0.66 | 2 | 1 | B | 0.105 x 0.074 |  |
| SHOP | K09e | fish_market glass u 2.80 | 0.66 | -3 | 1 | B | 0.105 x 0.074 |  |
| SHOP | K09f | fish_market glass u 3.30 | 0.66 | 1 | 1 | B | 0.105 x 0.074 |  |
| SHOP | K04 | fish_market door u 0.38 | 1.05 | 0.0 | 1 | B | 0.150 x 0.105 |  |
| SHOP | K03a | fish_market door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | K03a | ritas door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | K03a | steam_laundry door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | K06a | steam_laundry glass u 0.20 | 1.25 | 1.0 | 1 | B | 0.210 x 0.148 |  |
| SHOP | K06b | steam_laundry glass u 1.85 | 1.00 | -0.8 | 1 | B | 0.210 x 0.148 |  |
| SHOP | K06c | steam_laundry interior u 0.00 | 0.85 | 2.0 | 1 | B | 0.148 x 0.105 |  |
| SHOP | K07a | grocer glass u 0.20 | 1.55 | -3 | 1 | B | 0.170 x 0.170 |  |
| SHOP | K07b | grocer glass u 0.95 | 1.20 | 2 | 1 | B | 0.170 x 0.170 |  |
| SHOP | K07c | grocer glass u 1.70 | 1.60 | -2 | 1 | B | 0.170 x 0.170 |  |
| SHOP | K07d | grocer glass u 2.45 | 1.25 | 4 | 1 | B | 0.170 x 0.170 |  |
| SHOP | K08 | grocer glass u 3.00 | 0.95 | 0.0 | 1 | B | 0.210 x 0.148 |  |
| SHOP | D01 | grocer glass u 1.25 | 0.80 | 0.8 | 1 | B | 0.297 x 0.420 |  |
| SHOP | K04 | grocer door u 0.38 | 1.05 | 0.0 | 1 | B | 0.150 x 0.105 |  |
| SHOP | K03a | grocer door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | K03a | chandler door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | K03a | ironmonger door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | T03 | ironmonger glass u 1.20 | 0.80 | -0.6 | 1 | B | 0.508 x 0.762 | HELD (THE FOURTH WITNESS, A WEEK AT GULLWING) |
| SHOP | K03a | newsagent door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | K05 | newsagent door u 0.64 | 1.42 | 1.5 | 1 | B | 0.210 x 0.148 |  |
| SHOP | J01 | newsagent glass u 2.80 | 1.00 | 0.5 | 1 | B | 0.297 x 0.420 |  |
| SHOP | K04 | tea_rooms door u 0.38 | 1.05 | 0.0 | 1 | B | 0.150 x 0.105 |  |
| SHOP | K03a | tea_rooms door u 0.35 | 1.62 | 0.0 | 1 | B | 0.200 x 0.110 |  |
| SHOP | D01-named | grocer glass u 1.25 | 0.80 | 0.8 | 1 | B | 0.297 x 0.420 | HELD (THE SANDERLING TRIO) |
| SHOP | T03-named | ironmonger glass u 1.20 | 0.80 | -0.6 | 1 | B | 0.508 x 0.762 | HELD (THE FOURTH WITNESS, A WEEK AT GULLWING) |
| SHOP | SB1 | newsagent glass u 1.95 | 0.90 | 0.0 | 1 | B | 0.760 x 0.560 |  |

## 9. The words, as a list

311 approved strings (`approved_words`), 634 tokens (`approved_word_parts`). Every string is ours. Checked against: this file's forbidden lists (alcohol, gambling, children, real marks, names canon owes, things after 1992; extended in the second try with plurals, near terms and the real names the reviewer's probe listed); `tools/content-gate.py`'s 88 speech rules; `RealWorld.cs`'s names; imagegen's forbidden tokens; canon's streets and districts; the cast's surnames. **Proposed, unminted names** (placeholders, never on his page; a name in a block of cap 10 mm or more HOLDS its item):

| Name | what | on items | held items | largest cap (mm) |
|---|---|---|---|---|
| `MERIDIAN AGAINST THE POLL TAX` | the invented local anti-poll-tax campaign (ruling 3 Oct: an invented local campaign, never real parties or people). First proposed by the asset plan note 4, used by the 4 Oct bills. | P01, P01-named, P02, P02-named, P03, P03-named, P04, P05, P06 | P01-named, P02-named, P03-named | 23.400000000000002 |
| `QUAY PRINT` | the jobbing printer named in the imprint of every printed bill (an imprint was the custom and is expected on political and campaign matter); 2.4 mm, illegible, allowed on the default street | B01, D01, D01-named, F01, G01, G02, J01, M01, P01, P01-named, P02, P02-named, P03, P03-named, T03, T03-named, W01, W01-named | none (under 10 mm) | 4.0 |
| `ARMITAGE & STOBBS` | the estate agent on the named letting boards L01 and L03 (the brief asks for a proposed name, marked 'proposed, not minted') | L01, L03 | L01, L03 | 52 |
| `THE SANDERLING TRIO` | the dance band on the named chapel-hall dance bill | D01-named | D01-named | 11.5 |
| `THE HARPOONER` | a ring name on the named wrestling bill (renamed from the first try's THE SEA WOLF, which is Jack London's novel; not checked against real lists: the network is closed) | W01-named | W01-named | 45.0 |
| `TED HOLROYD` | a ring name on the named wrestling bill (TIGER JIM LARKIN carried a real dock-union leader's name; the first rewrite, BIG TED HOLROYD, is gone too: "Big Ted" is the teddy bear of the BBC children's programme Play School, a real programme's character and a child-coded name; not checked against real lists) | W01-named | W01-named | 43.0 |
| `SPANNER SMITH` | a ring name on the named wrestling bill (renamed from MAD MAURICE; not checked against real lists) | W01-named | W01-named | 47.5 |
| `THE STEVEDORE` | a ring name on the named wrestling bill (renamed from THE BARON, a real television series' title; not checked against real lists) | W01-named | W01-named | 38.0 |
| `THE FOURTH WITNESS` | an invented film at the Tivoli, on the named bills T01 and T03 (a film of that name was not checkable: the network is closed) | T03-named | T01-named, T03-named | 41.0 |
| `A WEEK AT GULLWING` | an invented film at the Tivoli, on the named bills T02 and T03 (Gullwing is a minted district) | T03-named | T02-named, T03-named | 41.5 |
| `WHITEWELL` | an invented washday powder on the four-sheet G01 | G01 | G01 | 97.5 |
| `QUAYSIDE` | an invented tea on the bill G02 | G02 | G02 | 61.0 |
| `MARSHLAND PICTURES` | the invented studio in the named films' billing block (6 to 12 mm) | T01-named, T02-named | T01-named, T02-named | 12.0 |
| `A. VENN` | an invented credit in the named films' billing block | T01-named | T01-named | 12.0 |
| `R. CORLEY` | an invented credit in the named films' billing block | T01-named | T01-named | 12.0 |
| `H. MADDOX` | an invented credit in the named films' billing block | T01-named, T02-named | T01-named, T02-named | 12.0 |
| `THE DRILL HALL` | the hall where the boxing and the named wrestling bills are held (a generic building, no street given) | B01, W01-named | B01, W01-named | 44 |

Names canon owes and this target therefore does NOT use: the football club, the local paper, the pirate radio station, the regional television channel, the telephone operator, the postal cypher, the council's name. The brand bible v1 carries proposals for four of them (Meridian Town AFC, The Meridian Argus, Radio Tideline, Coastway Television); canon.md still lists them as owed, so none is drawn here.

**The placeholder rule** (`placeholders`): A placement whose item carries a proposed (unminted) name in a block of cap 10 mm or more is HELD: held_until_minted true, `names` listing the names. G.page.placeholders fails while any held placement is in the built street and any of its names lacks a DECISIONS.md line of the form '- ... MINTED: <NAME> ...'. The placements of the four nameless stand-ins (T01, T02, T03, W01; `stand_in` true) carry the names of their named twin in `names` and are held the same way. `held` is true of every placement outside the default street, whatever the reason (unminted names; the bare gable's proof wall).

## 10. Variants the street needs

170 seeded variants over 84 items (a poster is built once, shown in the variants its entry names; nothing is multiplied before one complete sample is approved in the assembled game, CLAUDE.md: the empty unit's glass, six sheets in one layer, is the sample of the default street). The variants differ in: age class (always), ink registration and density, which corner is torn or lifting, tape positions, the second pass's shift, and the hours-driven face (OPEN or CLOSED, the LAST WASH hour). **Skew is never a variant of the texture**: it is the placement's rot_deg. The three police sheets are slot fillers: the same layout with another offence line. Dates move with the calendar: every event bill gives its date as computed words, so a build for another date in 1988 to 1992 re-computes the weekday (`G.dates`) and re-checks the ages (`G.dates.age`).

## 11. Where photographs, books, the reviewer and the ruling disagree, and what I chose

- **street plate lettering.** Wins: the 30 September ruling (Marcellus SC). Against it: the street-clutter note (Kindersley MOT serif, recommended 1952) and a search summary of a Hull caption (1920s to 1930s cast plates used the MOT SANS alphabets; Kindersley from 1951). Chosen: Marcellus SC capitals, 90 mm, tracking +0.04 em. No photograph reached: the ruling stands until one disagrees.
- **postal district and district line on a plate.** Wins: the project's own street-clutter note (a plain name plate; 'postcodes' wrong for 1990) and the absence of any source. Against it: a search summary: London plates carried the borough and the postal district; the first try's default carried the district's name as a small line. Chosen: the default and the placed plate is `n` (the name only); `d` (the name and a district line) stays as a variant until a dated photograph shows one; the postal-district variant (MR1) is deleted (TARGET-REVIEW fault 13)
- **the 4 October bills.** Wins: this target. Against it: tools/props/make_vignette_2d.py: clean flat bills, League Gothic, all four on one generic layout, a spring date (SATURDAY 31 MARCH), 'Admission 10p', 'WEIGHHOUSE LANE HALL', the bills' own fine print readable and straight. Chosen: autumn 1990 dates with computed weekdays, the chapel hall named as hook-cast.json names it, imprints, ageing in four classes, layered pasting, different processes and layouts
- **the letting board.** Wins: the fascia target (cloud week 42, same batch): 900 x 450, TO LET alone, Libre Franklin 800 cap 130, vinyl red, no agent, no number. Against it: the first try's 1200 x 450 board with an agent band and a number; the game's board_to_let.png (900 x 450, PT Sans, no agent, no number). Chosen: L02 IS the fascia target's board. The 1200 x 450 agent board L01 stays as a held variant that would need the fascia target changed in the same batch with one DECISIONS line (TARGET-REVIEW fault 5)
- **the poster prop's place.** Wins: the plain row's bay layout (terrace-front.py _plain_ground). Against it: vignette-scene.json's held-prop notes put a poster at west x 11.4 and a case at west x 26.4 'between a side door at 25.5 and a window at 27.3' (written before the west_north block became shops). Chosen: x 11.4 is the pier W1.0 (10.919 to 11.875) and stays; the case at 26.4 would stand on the tea room's glass: both cases move to the quay gable
- **the glyph check's margin.** Wins: the computation (glyph_table() in self_check.py; glyphlib.py's docstring). Against it: TARGET-REVIEW fault 1(b): each glyph must out-score every other glyph of its font and its own mirror by at least 0.05 on F at 0.5 mm. Chosen: F is a mean over the whole glyph, so glyphs that share most of their ink score alike: O against D in Oswald 700 at 34 mm capitals scores 0.987 against the true glyph's 1.000 (a margin of 0.013), 6 against 8 0.964, and 14 of the 36 capitals and digits cannot meet 0.05 even at that size. The check therefore keeps F >= 0.85 at 0.5 mm for the glyph itself and scores the separation from each alternative on the PIXELS WHERE THE TWO GLYPHS DIFFER (SEP, 0.70 to pass: a margin of 0.40), with every item's pixel scale chosen so that at least 8 such pixels exist for every pair that is not a shape twin. The reviewer's wrong renders all fail it
- **paper on the quay gable.** Wins: the asset plan's own proof wall and the Hook sheet together. Against it: the Hook sheet's gable is bare old brick with a downpipe, a render patch and a damp foot; the plan's proof wants 'three bills from three templates' on one wall (the nearest gable or the empty unit's stallriser). Chosen: THE GABLE IS BARE, as the sheet shows it (second review, by Jafar's ruling of 9 October): the three bills (P01, W01, T02 with its strip) and the second QUAY STREET plate are HELD placements flagged proof_wall; the downpipe, the render patch and the damp foot stand as fixtures; the proof sample is the empty unit's glass (six sheets in one layer). Nothing more until he has approved the sample in the assembled game
- **the one photograph measured.** Wins: judgement. Against it: the photographed notice case is a modern blue steel replacement with a wide crest header. Chosen: only its vertical fractions inform the glazed case's proportions; the 1990 case is a timber one with thinner rails (HC1)

## 12. The checks, and how the pixels are read

780 checks in `target.json` (`checks`). **Per item:** `.size` (image size), `.words` (the glyph manifest's characters equal the approved strings: a manifest check, NOT a pixel check; a missing or unreadable `<ITEM>.glyphs.json` FAILS it), `.pos` (each block's ink box read off the pixels, widened 8 mm along the line and 3 mm up and down, other blocks' glyphs not counted), `.cap` (letter heights at scale), `.mask` (the whole LINE re-rendered from its font compared with the ink: F at least 0.90 for printed lines, 0.85 for small print and typing, 0.78 for hand lettering, 0.55 for imprints; a PRINT line must also keep its worst single glyph at F 0.85 and pass the glyph check, so a changed word cannot hide in the mean; **a hand line's mask catches a wrong font or a shift, not a wrong word**: its jitter is only known from the manifest), `.glyphs` (the word check, below), `.square` (the texture is square-on within 0.3 degrees, ONE tolerance for print and hand cards alike, found against the render of the item's own glyph manifest, jitter included, and 0 unless F at the best angle beats F at 0 by 0.02), `.clean` (**ITEM.clean**: at most 2 mm2 of ink-coloured pixels outside every block's glyph window, the item's own shapes, the cue patch and the art slots, on the class-A render before wear), `.contrast` (WCAG on the aged render, class B), and for each art picture `ART.eye`. **Global:** `G.words.approved`, `G.forbidden`, `G.dates`, `G.dates.age`, `G.mirror`, `G.mirror.cues`, `G.fonts`, `G.proposed`, `G.page.placeholders`, `G.ferry.schedule`, `G.tides`, `G.place.inside`, `G.place.layers`, `G.place.piers`, `G.place.height`, `G.place.paper`, `G.place.gable`, `G.place.shops`, `PLACE.built`, `G.letting.mount`, `G.plates.length`, `G.plates.depth`, `G.plates.cap`, `G.plates.border`, `G.plates.make`, `G.glyph.scale`.

**`ITEM.glyphs`: reading one glyph at a time (TARGET-REVIEW fault 1).** The first try compared whole lines with a 1 mm (print) or 2.5 mm (hand) tolerance; a changed date, TEA for ALE, LUNCH for BINGO or a changed price scored F 0.94 to 1.00 and passed. A single glyph is a small part of a line. So:

1. **The glyph manifest.** Every render writes `<ITEM>.glyphs.json`: one entry per character of the approved string, spaces included, in order: `ch, font, weight, em_mm, ox_mm, baseline_mm, rot_deg, emb_mm` (the pen origin from the item's left edge, the baseline up from its bottom edge, the hand jitter and the pen's added stroke included). A manifest whose characters are not the approved string, or whose glyphs lie outside the block's envelope (print: 0.6 mm, 0.5 mm, 0.1 degree, 1 per cent; hand: 3.5 sd of the hand style plus a little), FAILS before any pixel is read (`G.words.approved` and `.words` read the same manifest). **A missing, empty or unreadable `<ITEM>.glyphs.json` FAILS `.words` and `.glyphs`**: the reader reports it and never crashes.
2. **The cell.** Each glyph is re-rendered from its manifest entry (glyph by glyph, the same function the renderer uses) and read in its own cell: the columns between its neighbours' ink, the block's window in rows. What the reader does not credit to it: the other blocks' glyphs as THEY manifest them, the item's rules, frames and bars, and its neighbours in the line (all dilated 1 mm), unless the glyph's own ink holds the pixel; and, where hand-lettered glyphs touch, **a pixel that a neighbour's ink explains and the glyph's own ink does not (within one pixel) is the neighbour's** (the first try credited it to the glyph, which failed true ballpoint cards). Big capitals are read at a reduced scale (an area rule that matches how their reference is drawn); a space carries no ink beyond 0.6 mm of every glyph of the line.
3. **F.** F = the mean of recall and precision of the read ink against the re-rendered glyph, each against the other dilated 0.5 mm: **at least 0.85** (the review's figure).
4. **SEP.** The glyph must be told from every other glyph of its font in A-Z a-z 0-9 £ . , ' ’ - — – & · ? : ! rendered at the same place, size and turn, and from its own mirror. Where the claimed glyph and the alternative differ, `A` is what only the claimed glyph inks and `B` what only the alternative inks (outside a 1-pixel tolerance); SEP is the share of the A and B pixels on which the read ink sides with the claimed glyph. **The gate is 0.70** (a margin of 0.40 where the review asked 0.05; see section A for why F itself cannot give a margin). Pairs that differ by fewer than 8 pixels are not told apart at that scale: the item's scale is raised until none is, so that every non-twin pair differs by at least 8 pixels at every item's own px/mm (`G.glyph.scale`, 169 font/weight/cap/stroke combinations tested). **Shape twins** (I and l, ' and ’, any pair differing by under 0.03 mm2 at 24 px/mm) and a glyph that is its own mirror (A, H, I, M, O, T, U, V, W, X, Y, 0, 8) or whose mirror differs from it only by edge slivers (nothing survives an erosion by one pixel but fewer than 8 pixels remain) are listed, not scored; a swap of one for the other changes no reading. Spaces must carry no ink. Imprints (cap 2.4 mm) are not read glyph by glyph: they are illegible by design and the line mask reads them at F 0.55.
5. **Each item's scale.** `px_per_mm` is not 2 for everything: it is the smallest of 2, 3, 4, 6, 8, 12 or 16 at which the table of step 4 holds for every block, from the font's cap and the glyphs it uses (`glyphlib.needed_ppm`); **for a hand-lettered block every pair is measured over glyphs jittered to 3.5 sd of its hand style (size and rotation, four corners), which raised the ballpoint cards SA01 to SA14 from 8 to 12 px/mm, K07a to K07c from 4 to 6 and K07d, K09a to K09f and SA15 by one step**, and group 12 reads 20 true jittered seeds of all 29 hand cards on top of it. In use: 2 px/mm: 35 items; 3 px/mm: 7 items (P01, P01-named, W01, W01-named, M01, K06b, L03); 4 px/mm: 14 items; 6 px/mm: 6 items (C01a, C01b, C01c, K07a, K07b, K07c); 8 px/mm: 1 items (C03); 12 px/mm: 21 items. No render is over 60 megapixels (the largest here is 12.4).

**The checks are tested** (`self_check.py`, groups 10 and 12 to 13), each on a true input and a wrong one:

- the reviewer's wrong renders: see group 12.
- **True renders pass:** a true render of EVERY item (54 print items) and 20 true jittered seeds of ALL 29 hand cards (580 renders) pass every pixel check (`.words` from the manifest, `.mask`, `.pos`, `.glyphs`, `.square`, `.clean`); any failure is a self-check failure. SA01 and SA03, which failed 11 and 15 of 20 seeds in the re-review, pass 20 of 20; the exactly square textures P05, K04, K03a, K03b, K02, K08 and P06 read 0 degrees; T01-named's true render passes.
- **A mirrored sheet fails,** hand cards included (K01, SA06, K07a: the old line mask was blind to them), and so does the mirrored plate, board and bill.
- **A tilt:** a true render turned 1.2 degrees (and 0.5) is found turned (`.square`, within 0.2 degrees for P01 and J01; jittered hand cards K01 and SA06 within 0.5) and fails `.square`, as it should (skew belongs to the placement); the same render read in the PLACED street, turned back by the placement's rot_deg, passes `ITEM.glyphs`.
- **`ITEM.clean`:** the true renders have no stray ink; the review's four planted lines (K01 + BINGO TONIGHT, SA11 + Babysitter, evenings., L02 + ARMITAGE & STOBBS at 46 mm, C02 + BETTING SHOP), drawn outside every block and left out of the manifest, and D01 + LICENSED BAR, which crosses a window, FAIL it.
- **A missing or unreadable manifest:** `glyph_check_block` returns a failure for none, an empty list, a truncated entry or a non-number (it no longer raises); `.words` fails for none, a block missing and a wrong character.
- **`PLACE.built`:** each placed decal (P03, M01, L02 tested) lies within 20 mm of the target's centre, is found within 0.3 degrees of its rot_deg and its largest block reads the right way round; a mirrored decal, a decal turned 1 degree off and a decal 40 mm off FAIL.
- **`G.mirror.cues`:** all 29 hand cards: the true render reads LEFT (the 25 mm top-left patch differs from the card's own colour on at least 20 per cent of its non-text pixels, the top-right on at most 3), the mirrored render RIGHT, a card with no cue neither.
- **`G.page.placeholders`:** the default street's placed-decals manifest passes; with one held placement and no minting line it FAILS; with '- ... MINTED: ARMITAGE & STOBBS' in DECISIONS.md the L01 and L03 placements pass.
- **`G.dates.age`**, **`G.ferry.schedule`**, **`G.letting.mount`**, **`G.place.paper`**, **`G.place.gable`**: each passes the target and fails the first try's input (T03 in class D; the far side's last crossing at 10.45; the 1200 x 450 board; a ninth fly-poster or a fifth poll-tax bill; a bill or a plate put on the bare gable, or the held proof wall made default; the held P01 moved to 0.4 m from the downpipe).

**The reference reader is in `self_check.py`** (`window_of`, `read_block`, `read_score`, `read_box`, `pos_ok` for the line level; `layout_glyphs`, `jitter_glyphs`, `render_item`, `glyph_check_block`, `manifest_problem`, `words_ok`, `square_estimate` (and `estimate_rotation`), `clean_ink_mm2` for the glyph and whole-item level; `glyphlib.py` for the kernels); the builder's own checker should do the same on its rendered item. The reviewer's `wrong_renders.py` still runs against it unchanged (the old names are kept): it now fails every PRINT wrong render, every mirrored plate, board and bill and every tilt, and passes all true jittered hand cards (0 of 20 seeds fail on each of the 29; `pos_ok` takes the hand style's own tolerances). It still passes a wrong word on a HAND line, because a hand line's jitter is known only from the manifest: the glyph check (`glyph_check_block` with the renderer's manifest) is what fails K01 LUNCH for BINGO, K07a GIN BAGS, SA11 and K09a. A manifest-free reading of hand lines was tried (each glyph aligned by correlation) and does not separate a true jittered glyph (F 0.55 to 0.75) from a wrong one (0.60 to 0.75): that is why the review's amendment (a) asks for the manifest.

**What no pixel check can do.** `ART.eye`: nothing in the pixels can tell a person, a hand, a face, lettering, a numeral, a crown, a kiosk mark, a bottle, a glass or an arcade sign in a generated picture from a picture without; a fresh reviewer looks at each art picture at 1:1 before any text is laid. G01, T01 and T02 (and the named twins) have one.

## 13. What the target could not settle

- No photograph of a 1990 street name plate, letting board, fly-posted wall or paper notice was reached. Every size of those is Judgement on search-summary leads (90 mm capitals, 150 to 230 mm plates, 12 mm borders: modern specs).
- Whether provincial plates of 1990 carried a postal district, a district line, the council's name or a crest: not found. The default plate is the name only.
- The side opening at street x 21 to 24 is the YARD ENTRANCE (vignette-scene.json, the dropped kerb at x 22.5) and atlas-01 gives it `yard_gap_x [21, 24]`: no plate names it, and the road closure sends traffic round by WEIGHHOUSE LANE and TANNERY ROW, which the atlas does name.
- Whether the scene has a quay-edge post, a hoarding, a gable wall at x = 3 that faces the hook camera with the geometry assumed here (8 m deep, eaves 6.3 m): read from vignette-scene.json and the recipe, not from the mesh.
- Tobacco bills (cigarettes were advertised on hoardings in 1990): omitted: they need a minted brand and the exact government health-warning wording, which was not read.
- The BBFC certificate roundels on film bills are real marks and are not drawn; the 1990 bills carried them.
- A police appeal board (the yellow A-board) in 1990: the only dated photograph found is from 2007; this target uses an A3 photocopy taped inside the empty unit's glass or sleeved on a column instead.
- The local paper's contents bill, the football club's bills and the radio station's stickers: the names are owed (canon), so none is drawn; the brand bible's proposals (Meridian Town AFC, the Argus, Radio Tideline, Coastway) are NOT used.
- Real-name coincidence: the network was closed, so NOTHING proposed was checked against real lists: QUAY PRINT, ARMITAGE & STOBBS, THE FOURTH WITNESS (a film of that name), the four ring names (renamed after TARGET-REVIEW found LARKIN and THE SEA WOLF real), MARSHLAND PICTURES and the three credits. Each is listed in proposed_names for the town to mint or strike, and none stands on the default street.
- Prices (cinema 2.80, wrestling 4 and 2.50, ferry 60p, tea 1.35) are Judgement except cod (ONS via the earlier note); smoked haddock 2.90 is dearer than fresh by Judgement.
- Texture size and mip: not checked in the 5.8.2 source; the builder checks whether bills need padding to powers of two (the fascia target has the same open question).

Unreached today: en.wikipedia.org (DNS and 403); commons.wikimedia.org, geograph.org.uk, flickr.com, archive.org (403); thebeautyoftransport.com (403); legislation.gov.uk, gov.uk (403); historicengland.org.uk, nationalarchives.gov.uk (403); www.west-norfolk.gov.uk and www.wigan.gov.uk PDFs (DNS); github.com file downloads for Liberation's TTFs (403).

## 14. The render contract and the fixings (for the builder)

- Texture: EVERY TEXTURE IS SQUARE-ON: no skew, no rotation and no perspective is baked into any base-colour image. Skew and rotation live ONLY in the placement's rot_deg (a hand card's tilt and the A3 sheet's crookedness too). ITEM.square fails a texture turned by more than 0.3 degrees (ONE tolerance, print and hand-lettered alike); the angle is found against the render of the item's own glyph manifest, jitter included, and is 0 unless F at the best angle beats F at 0 degrees by 0.02; PLACE.built checks the placed decal's rot_deg to 0.3 degrees.
- Scale: Each item is rendered at its own px_per_mm (items[].px_per_mm, chosen so that every glyph can be told from every other: glyphlib.needed_ppm). Row 0 of the image is the TOP edge; x runs from the viewer's left; y in the item frame runs up from the bottom edge.
- Ink mask: The reader's ink mask is the set of pixels nearer (CIE76) the block's aged ink colour than its aged ground colour. Imprints (role imprint, cap 2.4 mm) are not read glyph by glyph: they are illegible by design.
- Glyph manifest: file `<ITEM>.glyphs.json, written by the renderer beside every base-colour image (target_drawing.py and self_check.py show a reference writer)`; schema `{item, px_per_mm, size_px:[w,h], blocks:{<block id>:[{ch, font, weight, em_mm, ox_mm, baseline_mm, rot_deg, emb_mm}, ...]}}: ONE ENTRY PER CHARACTER OF THE APPROVED STRING, SPACES INCLUDED, IN ORDER. em_mm: the em of the glyph as drawn (mm, x the glyph's own size jitter); ox_mm: the pen origin from the item's left edge; baseline_mm: up from the item's bottom edge (the hand jitter included); rot_deg: counter-clockwise about the pen origin plus half the advance, on the baseline; emb_mm: the stroke added to the font's own (a felt pen), never over 0.6.`. The checker re-renders every glyph from the manifest and reads the pixels in the glyph's own cell. A manifest that is not the approved string, or whose glyphs lie outside the block's envelope, fails before any pixel is read. A MISSING, EMPTY OR UNREADABLE <ITEM>.glyphs.json FAILS .words and .glyphs (and the square estimate, which then reads the layout): the reader reports the failure and never crashes.
- Gate: F >= 0.85 at 0.5 mm; SEP >= 0.7; at least 8 pixels between any two non-twin glyphs; tolerance 1 px; alternatives A-Z a-z 0-9 £ . , ' ’ - — – & · ? : ! (the font's own glyphs only); shape twins (I and l, ' and ’, and any pair differing by under 0.03 mm2 at 24 px/mm) and a glyph that is its own mirror (or whose mirror differs only by edge slivers: nothing survives an erosion by a pixel but fewer than 8 pixels) are listed and not scored
- Placed street: PLACE.built: the builder writes placed_decals.json (item, surface, centre u and z or street x, rot_deg, scale); each decal lies within 20 mm of the placement's centre and 0.3 degrees of its rot_deg, and its largest block, read in a render of the surface at 1 px per mm after turning the decal back by rot_deg, passes the glyph check.
- Tape tab: a tab of yellowed adhesive tape, 38 x 16 mm at 40 degrees, rgb [196, 164, 84] opacity 0.85. lies across the corner on the 40-degree diagonal, centre 12 mm in from the top edge and 12 mm in from the left edge; part of it passes the card's edge. THE CUE of every taped or stuck hand card (K05, K06c, K07a-d, K09a-f, SA01-SA15): this ONE tab at the top-LEFT, nothing on the right half. (A sheet taped by its four corners, as the A3 notices are, carries four such tabs and no cue is needed: they are printed or photocopied, not hand-lettered.)
- String and sucker: a string loop and a rubber sucker: loop 220 mm, knot 8 mm, sucker 22 mm, rgb [150, 150, 146]. THE CUE of the string-hung hand cards (K01, K06a): the knot and the sucker at the top-LEFT, the loop rising from them past the card's top edge; nothing on the right half
- Four tabs (A3 and A4 sheets taped in a window): four tabs of yellowed tape, one at each corner of an A3 or A4 sheet, 38 x 16 mm, rgb [196, 164, 84] opacity 0.85
- The hours plate (the fascia target gives no horizontal place): the fascia target: a 300 x 190 plate centred 1.45 m up, on the shop door's glass or the pilaster; its horizontal place is not fixed there, so this target ASSUMES it centred on the door glass (u 0.30 to 0.60) and keeps door cards off that column in z 1.355 to 1.545

## 15. Self-check

(run `self_check.py` and then `make_doc.py` again to fill this in)

## 16. Sources

| Id | Kind | What | Read | Author and licence | Used |
|---|---|---|---|---|---|
| P1 | photograph | https://polyhaven.com/a/urban_street_01 ; file https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/urban_street_01.jpg ; info https://api.polyhaven.com/info/urban_street_01 | 8 October 2026 (tonemapped panorama 8192 x 4096, 10.6 MB) | Andreas Mischok; CC0 (polyhaven.com/license read 8 Oct: 'all licensed as CC0'); taken 18 August 2019 (info: date_taken 1566112140) | YES: proportions of a glazed case only (a 2000s replacement, not 1990) |
| P2 | photograph | https://polyhaven.com/a/bethnal_green_entrance | 8 October 2026 (tonemapped 8192 x 4096) | Andreas Mischok; CC0; taken 18 August 2019 | NO: nothing measured; the byelaw sign names alcohol, so NO crop of it is kept anywhere |
| P3 | photographs | https://polyhaven.com/hdris (urban_street_02, 03, 04, adams_place_bridge, birbeck_street_underpass, cambridge, docklands_02, limehouse; canary_wharf, docklands_01 and leadenhall_market were NOT looked at here) | 8 October 2026 (2048 x 1024 tonemapped previews in /home/user/cache/ph/scout) | Andreas Mischok and others (each page); CC0; taken 2019 to 2025 | NO |
| F1 | licence texts | https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/OFL.txt and https://raw.githubusercontent.com/liberationfonts/liberation-fonts/main/LICENSE | 8 October 2026, whole | each family's authors (copyright lines in fonts[].copyright); SIL OFL 1.1 (Liberation: OFL 1.1 with Reserved Font Name Liberation); taken n/a | YES: fonts (Liberation's font files were NOT reached: github.com file downloads return 403; its LICENSE was read; it is not used here) |
| R1 | repository | canon.md; RULINGS.md; production/cloud-week/targets/BRIEF.md and SCENE-SLOTS.md | 8 October 2026 | the project; project; taken n/a | YES |
| R2 | repository | production/specs/hook-cast.json; production/specs/vignette-scene.json; tools/art-recipes/terrace-front.py; tools/props/make_vignette_2d.py; production/assets/vignette/decals2d/ | 8 October 2026 | the project; project; taken n/a | YES |
| R3 | repository | production/cloud-week/targets/fascia-signs/TARGET.md and target.json | 8 October 2026 | the fascia target writer; project; taken n/a | YES: positions and the left-right rule |
| R4 | repository | production/research/asset-plan/4-SIGNAGE-AND-WEAR.md; production/research/ui-design/PERIOD-PRINT-AND-FONTS.md; production/research/street-clutter-1990/SUMMARY-2026-09-29.md; production/art/atlas-02/research/transport-timetables.md; production/research/shop-win | 8 October 2026 | earlier research helpers (they read period photographs and search summaries on the PC); project; taken n/a | YES, cited, not re-measured |
| L1 | search summaries (leads, never numbers) | WebSearch 8 Oct 2026: street name plate specs (South Kesteven https://www.southkesteven.gov.uk/sites/default/files/2023-09/STREET_NAME_PLATE_SPECIFICATIONv2.pdf; Charnwood; Fareham; Cotswold; Wigan), DfT circular 3/93 (west-norfolk.gov.uk copy), London street  | 8 October 2026: the pages themselves were NOT fetched (DNS or 403); only the search summaries were read | various; n/a; taken n/a | LEADS ONLY |

The licences of the previews: P1 is a crop of a CC0 panorama with the glazed interiors and the council crest painted out; the layout sheets are our own drawings. No preview shows a drink, a gambling mark or a person; the layout sheets show our invented placeholder names (ARMITAGE & STOBBS and the like), never a real business.
