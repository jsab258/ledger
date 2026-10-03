# Asset plan, note 4: signage and posters; decals and wear

Research helper, 3 October 2026. About thirty minutes, read only. 25 web searches.

**Marks:**
- **[READ]** read at the source. "[READ, repo]" means read in this repository.
- **[SS]** search summary only.
- **[I]** my inference.
- **UNREACHED** the page refused me. An unreached page is never evidence.

## Read this first: six things found on the way

1. **The image model cannot be trusted with words, even short ones.** [READ, repo: I looked at the pictures]
   - The 3 September batch (ledger/Assets/StreamingAssets/Decals/generated, Z-Image-Turbo Q4_K, all still "review=pending") printed:
     - "BRITHH WORIKER" under RITA'S;
     - "LIGHTS LIGHTS" and "AAMISSION 2 POUNDS" on the gig bill (a 1990 bill would say £2);
     - lines of fake text on the election poster.
   - FISH MARKET is spelled right, but as a modern blue tiled panel, not a 1990 fascia.
   - The published claim is about 0.93 accuracy for English words, reliable at 1 to 5 words, and weak on longer lines [SS, 17]. Ours is a quantised model on a Radeon, and it failed below that.
   - **Rule: every word on every sign is our own text layer. The image model makes only pictures with no words in them.**
2. **The same batch breaks canon in four places.** [READ, repo]
   - `poster_bingo`: gambling. The brand bible itself refuses bingo.
   - `sign_marquee`: "MARQUEE" is a nightclub sign. The Marquee was a real London music club [I, from memory].
   - `interior_bar_back`: a pub's back bar, so drink.
   - `poster_darts`: "a British pub darts league sheet".

   The scene file still names three of the batch's fascias (fish market, Rita's, Steam Laundry; production/specs/vignette-scene.json, lines 680 to 698). Only Mickey's is overridden (terrace-front.py `SIGN_OVERRIDE`). Check whether "BRITHH WORIKER" stands in the frames he has seen. **Recommended:** retire every picture in the batch that carries words.
3. **The Megascans decals in his library have no NoAI check on record.** [READ, repo]
   - production/specs/fab-free-megascans.md lists 18 surfaces. Ten are the wear layer's decals and masks (Leakage ×4, Concrete Leakage ×2, Oil Stain ×2, Grunge ×2), plus Stains.
   - No file in the repository records whether any of them carries Fab's NoAI tag.
   - The natural-idles note records that Epic's own Game Animation Sample listing carries the NoAI flag (production/research/natural-idles/NOTE.md, line 67). So Epic's first-party listings can carry it.
   - **Each listing must be opened and checked before any of them is used.** If one is tagged, it is never used, under today's rule. Fab was UNREACHED from here.
   - That same line puts GASP itself in conflict with the 3 October rule. GASP is not in my families, but it should be raised.
4. **The brand bible is stale in two places.** [READ, repo] content/brands/brand-bible-v1.json still says "MICKEY'S IS A PUB AND STAYS A PUB" and gives Mickey's `kind: pub`. Canon made Mickey's a minicab office on 14 September (D19). It also puts the football scarves "in pub windows".
5. **The game's Mickey's fascia is not the Hook sheet's.** [READ, repo: both pictures]
   - The sheet: gilt capitals with flared serifs, standing out from a slate-blue board.
   - The game: flat PT Sans in gold on a flat board (production/assets/vignette/decals2d/fascia_mickeys_plain.png), clean, with no relief and no wear.
   - Marcellus SC (OFL, already in production/fonts and ruled on 30 September) is far closer to the sheet's letter [I].
6. **The graffiti tags are no longer blocked.** The bill of materials still calls G7 "HELD", and tools/props/make_vignette_2d.py says it is "blocked on canon minting crew names". Canon minted the five tags on 2 September (canon.md, lines 47 to 51) [READ, repo].

---

# Family A: signage and posters

## A1. How professional games make it

| Studio / game | What is known | Mark |
|---|---|---|
| Rockstar (GTA, RDR2) | In-house graphic designers "create brands and assets for a variety of 2D graphics applied throughout in-game worlds" (a job listing). A named lead 2D/UI designer at Rockstar North, 2005 to 2014. GTA 6's trailer is full of logos for invented companies. | [SS, 1-3] |
| RDR2 | Signs and shopfronts use antique slab serifs, Tuscans and condensed gothics, to mimic the printing of the period. | [SS, 4] (a design blog, weak) |
| Naughty Dog | Outsourced its "one-offs such as signs, branding, and unique assets", and kept them in a tagged library. | [READ, repo: GOODS-2026-10-03.md, citing 80.lv, 8 December 2020] |
| Mafia: Definitive Edition | Environment artists credit themselves with "decals and prop placement". Collectible magazines spoof the period's comics. | [SS, 7] |
| Watch Dogs: Legion | A Design Art Director owned the visual identity. Real and invented station names are mixed. Joke signage. | [SS, 5] |
| Everybody's Gone to the Rapture (Shropshire, 1984) | Faded fête posters and period labels, made in-house. | [SS, 6] |
| KCD2 | Few signs, each weathered into the wall: in the reference frame, a painted board hangs from a forged bracket. | [READ, repo: by eye, kcd2-town-arcades.jpg] |

**What this adds up to [I]:**
- A small graphic team writes a brand bible and a type palette for the period.
- Most signs are variations on a few dozen templates, laid down as decals or atlas tiles.
- A handful of hero signs are made by hand.
- **GTA parodies real brands. We cannot:** canon forbids real brands, and a parody that borrows a real trade dress is still that brand in spirit. Ours are invented from nothing.
- No source with a pipeline or numbers for "thousands of signs" was reached.

**Typography of 1990 Britain**

1. **Shopfronts mixed three generations.** [SS, 22]
   - Older family shops kept painted timber fascias: romans, Egyptians, shaded block letters, and gilt on dark grounds.
   - "By the 1980s the backlit Perspex sign was increasingly replacing the old fascias."
   - "By the end of the decade computer-cut vinyl lettering was beginning to appear."
   - Glass was hand-lettered. A dated photograph of 25 August 1990 shows a dark fascia sign-written in red, and white "whitewash" lettering on the glass (Picture Sheffield t13138, looked at by the builder) [READ, repo].
2. **Letraset.** Dry-transfer lettering was "used extensively ... in the 1960s, 1970s, and 1980s" and was "replaced by desktop publishing" in the late 1980s. Punk took it up for its cheapness [READ, 21]. So a 1990 gig bill or a jumble-sale notice is Letraset, photocopy or two-colour screen print. It is not laser-printed.
3. **Road signs.**
   - Worboys signs, introduced 1 January 1965. The 1981 Traffic Signs Regulations were in force in 1990 [READ, 25].
   - Lettering: Transport (Kinneir and Calvert, 1957 to 1963), Medium for light letters on dark grounds and Heavy for dark letters on light [READ, 9].
4. **Street name plates.**
   - Black capitals on white. Kindersley's MOT serif was recommended in 1952, and was dominant outside London [READ, repo: street-clutter-1990; SS, 13].
   - Ours are ruled: Marcellus SC (licence allowlist, entry 7).
5. **Cinema.** The British quad is 30 by 40 inches, landscape; double crown is 20 by 30 inches, portrait [READ, 24]. The Tivoli's own front is "plastic letters on a rail, some missing, changed on Thursdays" (brand bible) [READ, repo].
6. **Poll tax, 1990.**
   - Community Charge began in Scotland in 1989 and in England and Wales in 1990. The Trafalgar Square riot was on 31 March 1990. Non-payment was led by the All Britain Anti-Poll Tax Federation. "Can't pay won't pay" came from Dario Fo's play. Local groups were named like "Luton Against The Poll Tax", and printed stickers and placards [READ, 18].
   - Hackney Museum holds dated leaflets, stickers and window bills from 1990 [SS, 19; UNREACHED]. So does the People's History Museum [SS, 20; UNREACHED].
7. **Graffiti.**
   - Hip-hop tags reached British walls in the early 1980s, written freehand [SS, 26].
   - Wikipedia adds only "since the 1980s ... hip hop and electro ... brought ... graffiti to the UK on a large scale" [READ, 26].
   - In a small northern port in 1990 I expect marker and spray tags, painted political slogans (poll tax), football, names and initials [I].
   - Racist and far-right slogans were real in 1990. Recommended: none (see Needs a ruling).

## A2. Free sources without AI restrictions

**Fonts.** Every licence below was read in Google's own fonts repository, METADATA.pb, on GitHub [READ, 15]. OFL 1.1 is on the allowlist (entry 7). OFL has no AI clause.

| 1990 letter it stands in for | OFL font (in repo: †) | Use |
|---|---|---|
| Classical roman, gilt or signwritten | Marcellus SC †, Libre Caslon Display, Playfair Display, Libre Bodoni, Old Standard † | fascias, glass gilding, street plates (Marcellus SC by ruling) |
| Egyptian and slab (signwriters' block letters) | Alfa Slab One, Zilla Slab, Coustard | trade fascias, harbour notices |
| Cooper Black, Souvenir, Windsor (1970s and 80s refits) | Fraunces (its designers: "inspired by ... Windsor, Souvenir, and the Cooper Series" [READ, 16]), Bagel Fat One | café, launderette, hairdresser |
| Helvetica and Arial (Perspex box signs, vinyl) | Arimo (now OFL, metric-matched to Arial), Inter, Archivo, Hanken Grotesk, Work Sans | box signs, door vinyl, council notices |
| Futura and Avant Garde | Jost, Questrial | 1980s refits, adverts |
| Eurostile | Michroma | garage, taxi, electrical |
| Condensed gothic capitals (news bills, gig bills) | League Gothic †, Oswald, Anton, Bebas Neue | Argus bills, posters, the Tivoli's letters |
| Blackletter masthead | UnifrakturMaguntia † | the Argus |
| Scripts | Yesteryear, Lobster, Pacifico, Damion, Mr Dafoe | café and "Open" signs |
| Typewriter | Courier Prime | notices, lost-cat sheets |
| Stencil | Stardos Stencil, Black Ops One | harbour crates, quay markings |
| Hand-marked tickets and bills | Caveat Brush, Kalam, Gochi Hand | price tickets, star cards, hand-marked bills |
| Spray and graffiti (seed only) | Sedgwick Ave Display, Rubik Spray Paint | starting shapes; real tags are drawn as strokes (A3) |

- **Apache-licensed fonts** (Permanent Marker, Special Elite, Ultra) are not OFL. They need a ruling, but are not needed.
- **Fonts are a starting point, not the look.** Signwriters drew every letter. The agent varies each glyph's outline slightly, plus weight, spacing and baseline, and adds the trade's shading, outline and drop-shadow [I].
- **Avoid letters that date themselves.** Comic Sans (1994 or 1995) never appears [I, from memory; check].

**Road-sign lettering: nothing free and allowed.**
- The Transport fonts at roads.org.uk are "only intended for private non-commercial use": **never** [SS, 10; UNREACHED by fetch].
- The DfT's working drawings of the alphabets (TM 1-3, TH 1-3) are Crown copyright under the Open Government Licence [SS, 12].
- A faithful Transport Heavy on GitHub is "derived from those drawings", with no licence file in the repository [READ, 11].
- The OGL is not on the allowlist, so either route **needs a ruling**. K-Type's Transport New is paid, so money.
- Kindersley's MOT serif has a "free digital version" (Kindersley Grand Arcade), licence unknown [SS, 14]. Not needed: Marcellus SC is ruled.

**Substrates (what the sign is painted or printed on):**
- CC0 tiling surfaces for painted wood, enamel, rust, paper and card: ambientCG and Poly Haven (allowlist). Both were UNREACHED from here; they are already in use in this project.
- The free Megascans "Grunge" and "Stains" masks are in his library, if they carry no NoAI tag (finding 3).

**Not usable:**
- **Sketchfab "[CC0] Decal - Graffiti Textures"** [SS, 35]: photographed real walls, so other writers' tags, and not canon's.
- **Any scanned shop sign or poster:** a real business or design.
- **The period photographs:** links only, never textures (production/reference/photographs.md).

**There is no free set of 1990 British signs, posters or brands in any allowed licence. They are ours to make.**

## A3. The kit we make

**Parts: geometry, made in Blender by script** (tools/art-recipes; shop-room.py already makes extruded text with `text()`):
- a fascia board with moulding (fascia-cornice-elevation.py exists);
- a projecting sign: bracket and double-sided board, or a hanging board on a forged bracket;
- a Perspex box sign: aluminium box, translucent face, tube banding at night;
- cut or raised letters: OFL fonts as Blender text, extruded and bevelled, the way Mickey's sheet letters stand out;
- an enamel plate with a rolled edge (the Harbour Board's "blue and white enamel signage");
- a cast street plate;
- a road-sign plate on posts;
- the Argus's wire-fronted A-board, and a timber A-board;
- a timber hoarding for fly-posting;
- the Harbour Board's glass notice case ("drawing-pinned and curling");
- the Tivoli's letter rail with loose plastic letters.

**Parts: graphic templates,** rendered by script from data. A **sign spec** in JSON gives:
- the board's size in mm;
- the ground colour;
- the lines of text, and the font from the table above;
- the colours;
- the style (signwritten, gilt, shaded block, vinyl, box sign, print, hand-marked);
- the trade;
- the year it was last painted;
- a seed.

The templates:
- fascia;
- glass lettering (whitewash hand, gold leaf, vinyl hours);
- window card and price ticket (fluorescent star card, white card hand-marked);
- door stickers;
- council, police and harbour notices;
- the Argus bill, printed and hand-marked;
- the gig bill (Letraset and photocopy, two-colour screen print);
- the poll-tax window bill and fly-poster;
- the cinema quad;
- the graffiti tag and the slogan.

**How graffiti is drawn.** A tag is a few continuous strokes, drawn as centre-line paths, one style per "writer": slant, joins, flourishes, underline. It is rendered with a brush model:
- **spray:** a soft core, an overspray halo, and drips that run down where the hand slowed;
- **marker:** a hard nib, and ink pooling where a stroke starts.

Older tags fade under newer ones, and buffed patches are painted over in a colour that does not match. Each crew writes in its own district and is crossed out in a rival's (canon's tags and districts) [I].

**Ageing, by material** [I]. Each is driven by the same house seed as tools/street_wear.py's `wear`, so a worn house has worn signs:
- **paper:** wet-paste wrinkles, torn edges, layers of older bills under newer, glue stains, reds fading to pink before blues;
- **paint on timber:** chalking, cracks along the grain, chips at edges, the ghost of the last trade's letters showing through a repaint (the brand bible: Mickey's sign "repainted a shade off each time");
- **enamel:** chips to black iron with a rust halo;
- **Perspex:** yellowing, a cracked panel, a dead tube at night;
- **vinyl:** corners lifting, letters missing;
- **everywhere:** top-down grime, dirt under ledges, and gull droppings on top edges (a port).

**Variation:** seeds pick the template, the font from the trade's era, the palette (the existing FASCIA_PAINT "waves"), the layout, the wear and the refit year. A minted name list gives the words.

**Tools:**
- **Python:** Pillow, already used at 1 mm per pixel by make_vignette_2d.py; fontTools (MIT) for glyph outlines. The renderer writes colour, alpha, a height map for raised letters, chips and paper relief, and roughness (gloss paint against matte paper).
- **Blender:** for relief.
- **Z-Image-Turbo (Apache 2.0, local):** only for pictures with no words: a poster's photograph or illustration, a film's key art, a news bill's halftone. Its own rules forbid faces and likenesses (ATTRIBUTION.json), so key art uses places, objects and silhouettes.
- **In Unreal:**
  - **Posters:** DBuffer decals on walls, so the brick's mortar shows through the paper. A peeling corner or layered bills that lift away are thin bent meshes.
  - **Lettering on glass:** goes in the glass material, since decals do not draw on translucent surfaces (CLOSE-RANGE-2026-10-03.md, item 6) [READ, repo].
  - **Atlases:** posters and stickers are packed into atlases, one tile picked per instance.

**How the agent drives it, and its checks:**
1. Spec, then render, then automatic gates:
   - tools/content-gate.py and tools/canon-gate.py;
   - the real-world name list (ledger/Assets/Scripts/Core/RealWorld.cs);
   - a period list: £ and p prices from 1990; no National Lottery (1994); no www, email or mobiles; no "ROYAL MAIL" on boxes and no Piper BT mark before 1991 (street-clutter-1990); phone numbers in the 1990 form (my memory: PhONEday was 1995; check) [I].
2. Then placement, and a render through the hook camera.

Spelling is right by construction, because the text is ours.

**Where a human eye must judge:**
- each template's look, once;
- legibility and density through the game camera;
- whether a sign sits in its wall or reads as stuck on.

Anything with story or canon in it goes to his page under his rules: newly minted names, headlines that tell the plot. New names are minted within canon by the session, one line in DECISIONS.md, his to overturn, as the kiosk and pillar-box marks were on 29 September.

**Owed before the town can be signed:** the bible holds 8 names and still owes the kiosk mark and the pillar-box cypher. The street also needs:
- the council's name and crest;
- the police force's name;
- national newspapers;
- cigarette and sweet makers (tobacco is allowed);
- soap powders for the launderette;
- a bus operator;
- card-acceptance marks for the door stickers;
- the Tivoli's films;
- bands and venues for the gig bills;
- candidates' names.

That is about 40 to 60 names [I].

## A4. The reference that sets the bar

- **Hook sheet** (production/reference/hook-sheet.png):
  - Signage is sparse and calm.
  - Mickey's is gilt flared-serif capitals on slate blue.
  - A second white fascia, dark ones further on, paper cards taped inside windows, and one blue road sign far off.
  - **The bar is not "many signs". It is signs that belong to their walls.**
- **KCD2 arcades frame:** one hanging painted board on a forged bracket, as weathered as the plaster round it.
- **Dated photographs, links only** (production/reference/photographs.md and the fishmonger note):
  - Peter Marshall's Hull, 1989: metal shopfronts, a letting board, painted fascias;
  - Picture Sheffield t13138, 25 August 1990: a red sign-written fascia and whitewash glass lettering;
  - Steve Thornton, Grimsby, 1990;
  - Hackney Museum's poll-tax leaflets and stickers of 1990 [SS, 19; UNREACHED].
- **Signs date quickly.** Use photographs dated 1986 to 1992 for any sign. Geograph is mostly after 1996 (UNREACHED here).

## A5. The variety the town needs, and the one proof

| Kind | Quay Street (the proof view) | Whole town [I] | Why |
|---|---|---|---|
| Fascias | 12 | 60 to 80, from 6 styles | Every shop. The style says when it was last refitted. |
| Projecting and hanging signs | 3 to 4 | 20 | The silhouette from down the street. |
| Glass lettering | 12 | 60 | Every shop window. |
| Window cards, tickets, stickers | about 40 | about 300, from about 25 templates | Close-range believability. |
| Street plates | 3 (minted) | about 20 | Needs canon names. |
| Road signs and plates | about 8 types | about 25 types | No waiting, one way, 30, give way, crossing, bus flag. |
| Notices (council, police, harbour) | 6 | 30, from about 12 templates | The town's institutions. |
| Argus bills | 2 boards | changes daily | The simulation's events could write the headlines (a scope idea for him, not to build now). |
| Fly-posters and gig bills | 8 | 40, from about 10 templates | Layered walls. |
| Poll-tax and election bills | 4 | 15 | 1990 itself. |
| Cinema | the Tivoli front: 3 to 4 quads and the letter rail | the same | Minted. |
| Graffiti | 6 to 10 tags, 2 to 3 slogans | 5 tags × about 6 hands, about 100 placements | Canon's five crews by district. |

**The proof: Mickey's and the next two fronts, signed to the bar.** It belongs to the proof frame's item 6.
1. Mickey's fascia remade to the sheet: Marcellus SC capitals, gilt, standing out from the board, grimed by its house seed.
2. The fishmonger's fascia sign-written, with whitewash lettering and ticketed prices on the glass.
3. One wall in view (the nearest gable, or the empty unit's stallriser without changing its ruled look) fly-posted:
   - three bills from three templates (gig, poll tax, a Tivoli quad), shown with two seeds each, to prove the kit;
   - one QUAY FIRM tag and one buffed patch.

**Judged** in the hook camera at 2560 by 1440, beside the Hook sheet and the KCD2 frame.
- Mickey's reads at the sheet's distance and weight.
- Nothing reads as printed on.
- Each sign is as worn as its wall.
- A fresh reviewer then reads every word for spelling, real names, period and the content rule, and looks for any repeated poster.

**Effort:** about 3 to 4 builder-days. The renderer and its templates take 1 to 2, the ageing 1, the Unreal materials and placement 1, judging half a day [I].

---

# Family B: decals and wear

## B1. How professional games make it

- **Layers in the material.**
  - Two or three material layers (clean, dirty, damaged) are blended by vertex paint, mixed with a grunge mask and a height blend.
  - Leaks and dirt are painted to break up the tiling and tell the place's story [SS, 29].
- **Decals.**
  - Material-blend decals lay dirt through the DBuffer [SS, 30; repo 1-PIPELINE.md].
  - Projected decals carry leaks, streaks and grime.
  - Decal sheets of 70 or more pieces share one master material [SS, 31].
- **Engine limits (Epic's own pages).**
  - Mesh decals do not work on Nanite.
  - Nanite cannot take per-instance vertex colour. Texture Color painting, which needs virtual textures, replaces it [READ, repo: aaa-street/1-PIPELINE.md, Epic's pages].
- **Runtime Virtual Texturing, Unreal 5.8:** "efficiently blend decals, splines, and other meshes into landscapes". It "caches shading data over large areas", so the cost stops growing with every stain. Static objects only. Page uploads are throttled (8 a frame in the game) [READ, 27].
- **KCD2, by eye:**
  - dark streaks fall from every crenel and window;
  - dirt rises from the foot of every wall;
  - cracks and patches in the plaster;
  - wear placed by the building's own shapes, not sprinkled [READ, repo: the frame].

  No Warhorse breakdown was reached [SS, 38].

## B2. What exists here, and what is missing

**Built** [READ, repo]: tools/street_wear.py places 159 decals by rule over 13 houses, in 8 kinds:

| Kind | Count | Where |
|---|---|---|
| puddle | 37 | |
| streak | 32 | under sills |
| algae | 18 | at downpipes |
| splash | 17 | 0.6 m band |
| wash | 17 | |
| damp | 17 | the lowest metre |
| oil | 16 | |
| soot | 5 | |

- Each house has a seed, a brick set, a tint and a wear level, and coverage is printed per wall (D53).
- The pictures are our own masks (tools/make_wear_masks.py, seeded numpy noise).
- **There is one picture per kind, and three for puddles,** so repeats will show at the scale of a town.
- His verdict of 2 October: "wear that reads at a glance across every facade, not faint marks".

**Missing,** by the street research's own list and the two references:
- **On walls:**
  - rust runs under brackets, railings and gutters;
  - gull droppings on sills, fascia tops and ledges;
  - salt bloom on low brick by the quay;
  - peeling and flaking paint on sills, doors, fascias and render;
  - worn paint on door kick-plates and handles;
  - patch repairs (the sheet's render patch; repointing in fresher mortar; odd replacement bricks);
  - cracks stepping out from window and door corners;
  - ghost marks of removed signs and brackets;
  - poster residue and glue on hoardings;
  - buffed graffiti.
- **On the ground:**
  - chewing gum (the dark spots on the sheet's right pavement);
  - rectangular trench reinstatement patches in tarmac and flags;
  - cracked and rocking flags;
  - tyre marks at the kerb;
  - broken yellow lines;
  - grime halos round drains.

## B3. Free sources without AI restrictions

| Source | Licence | AI tag or clause | Fits? | Mark |
|---|---|---|---|---|
| ambientCG decals already staged: Leaking005, RoadLines ×6, ManholeCover011, AsphaltDamageSet001, Sticker001, SurfaceImperfections ×4, Scratches003, Moss001 | CC0 1.0 (THIRD-PARTY.md beside them) | none (CC0 waives everything) [I] | yes: road lines, damage, imperfections, moss | [READ, repo]; site UNREACHED (403) |
| ambientCG's other decals (graffiti, gum, splatter?) | CC0 | none | unknown | UNREACHED; not evidence |
| Megascans in his library: Leakage ×4, Concrete Leakage ×2, Oil Stain ×2, Grunge ×2, Stains | Fab Standard License, price 0 | **unchecked**: Epic's own GASP listing carries NoAI (repo note) | yes, if untagged | UNREACHED |
| Fab packs found by search: "Decals of Stains, Cracks and Plaster" Vol. 1 and 3; "30 Decal Pack: Dirt, Cracks, and Holes"; "Paint and papers decals ... Torn paper"; "Decals VOL.8 Urban Decay" | unknown | unknown | maybe | [SS, 31]; UNREACHED. Leads only. Price and NoAI to be read on each page. |
| Poly Haven | CC0 | none | its tiling plaster, painted wood and rust as blend layers; no decal category found | [SS, 33]; UNREACHED |
| TextureCan, 3DTexel ("280+ CC0 decals"), TextureMax | "CC0" by their own claim | unknown | maybe | [SS, 34]; UNREACHED. **Not named on the allowlist: a ruling is needed. Not needed.** |
| Sketchfab "[CC0] Decal - Graffiti Textures" | CC0 | — | **no:** real writers' work, not canon's tags | [SS, 35] |

**What this means.** Free scans help on the ground: lines, cracks, covers, moss. Our own seeded masks already carry the walls, and can carry every missing kind. If the Megascans prove tagged, nothing essential is lost.

## B4. The kit we make

**Four layers, broadest first** [I, on B1's sources]:

1. **L0, in the materials (no decals).** Brick, render, paint, stone, asphalt and flags each get:
   - a height gradient: splash from the ground, rain-wash from the top;
   - dirt in cavities from baked ambient occlusion and curvature: mortar, reveals, mouldings;
   - large-scale variation by world position, to break the tiling;
   - wetness (exists);
   - the per-house tint (exists).

   This is the cheapest broad wear, and what makes the bricks stop looking new.
2. **L1, rule-placed wall decals** (street_wear.py, extended). Rules that follow the physics:
   - streaks only fall downward, and are as long as the sill or the coping;
   - algae where water is: downpipe shoes, leaking gutter joints, north faces, low walls;
   - soot over flues;
   - rust under every piece of iron;
   - droppings under the ledges gulls use;
   - cracks at the corners of openings;
   - peeling scaled by the house's "last painted" year;
   - salt within reach of the quay.
3. **L2, the ground in a Runtime Virtual Texture.** Gum is densest at shop doors, the bus stop, the crossing and the newsagent. Then oil where cars stand, trench patches, cracked flags, worn lines, drain halos and puddles (exist). Written once into the ground's virtual texture, so a thousand marks cost about what ten do [READ, 27; I].
4. **L3, a few hero decals** placed by hand at the near frontages only.

**Variation:**
- 4 to 6 masks a kind, which is about 100 masks in all, made by make_wear_masks.py with new seeds and shapes.
- Rotation only where physics allows it: a streak never turns.
- Scale, and strength from the house's wear.
- Colour by substrate: rust orange-brown, soot black, algae green-black, salt white.

**Tools:**
- numpy and Pillow (exist);
- Blender, baking ambient occlusion and curvature masks for each kit piece by script;
- Unreal: DBuffer decals spawned from street-wear.json (VignetteShot.cpp `SpawnWear` exists); a ground RVT; 5.8's PCG to scatter gum and litter by density maps; material instances with each house's parameters.

**How the agent drives it, and where an eye judges:**
- **The agent:** writes the rules, makes the masks, and prints coverage and decal count. It renders the hook camera and the frame time on the RX 6700.
- **The eye:** density and strength, judged only in the game's camera and exposure.
- **A proxy that may help [I]:** compare each facade's local contrast in the game frame with the same measure taken off the Hook sheet. A number to argue with, never the gate.

## B5. The reference that sets the bar

- **Hook sheet:**
  - a pale render patch high on the left gable;
  - dark staining at every wall foot;
  - darker, wetter joints in the flags;
  - dark spots (gum) on the right pavement;
  - worn double yellow lines;
  - grimed drain covers.
- **KCD2 arcades:** streaks under every ledge, reading at a glance; dirt rising at the wall foot.
- **Period photographs:** Marshall's Newtown Square, Hull, 1989: "contrasting wall repairs" (photographs.md R07).
- **Weathering does not date the way signs do.** Recent photographs of old northern terraces are fair references for streaks, soot, algae and salt: Geograph, CC BY-SA, links only (UNREACHED here). They are not fair for the ground, which now has tactile paving, wheeled bins and modern lines.

## B6. The variety, and the one proof

**Variety:** about 18 kinds (the existing 8 plus 10 missing), 4 to 6 masks each, coloured by substrate, placed by rule over every house the town builds. The rules need no handwork, so the town costs no more than the street [I].

**The proof: the same three near frontages** (Mickey's and the next two) with their pavement and gutter.
- L0 dirt in their materials;
- L1 with the new kinds and 4 or more masks each;
- L2 ground in a virtual texture.

It belongs to the proof frame's items 4 and 7.

**Judged:**
- in the hook camera, wet, beside the Hook sheet: the wall feet, the patch, the pavement spots and the lines;
- beside KCD2: streaks under every ledge, at a glance;
- by his words of 2 October;
- a fresh reviewer then hunts for any mask repeated twice in the frame, and checks the frame time and decal count on the RX 6700.

**Effort:** about 3 to 5 builder-days [I].

---

# Per family, in one line

- **Signage and posters.**
  - **Free:** about 40 OFL fonts (read), and CC0 surfaces for boards and paper.
  - **We make:** every sign, poster, notice, sticker, ticket and tag, from data-driven templates with our own text layer; the image model only for pictures with no words.
  - **Impossible without a ruling:**
    - Transport lettering for road signs: no OFL version exists, and the DfT drawings and fonts derived from them are under the OGL;
    - real party names and real slogans on the poll-tax bills;
    - far-right and racist graffiti: recommended none;
    - Apache-licensed fonts, which can be avoided.
- **Decals and wear.**
  - **Free:** ambientCG's CC0 decals (16 sets already staged), and the Megascans decals in his library only once each listing is read free of NoAI.
  - **We make:** about 18 kinds of rule-placed wear from our own seeded masks, dirt in the materials, and the ground in a virtual texture.
  - **Impossible without a ruling:** CC0 sites not named on the allowlist (TextureCan, 3DTexel); any paid decal pack, which is money.

**Canon question for Jafar (one, with my recommendation):**
- On the 1990 poll-tax bills:
  - (a) no party names: generic "NO POLL TAX" and "CAN'T PAY WON'T PAY" from an invented "Meridian Against the Poll Tax", and no real person (Thatcher is one) **[recommended]**;
  - (b) real party names;
  - (c) no political posters at all.

# What I could not reach or verify

- **Fab:** every listing, price and NoAI tag, including the 18 Megascans in his library. **This is the one that matters most.**
- **ambientCG, Poly Haven, TextureCan, 3DTexel:** catalogues and licence pages refused here (403 or blocked).
- **Picture Sheffield, Geograph, Hackney Museum, the People's History Museum, roads.org.uk, signpainting.co.uk:** blocked.
- **Epic's mesh-painting and decal-actor pages:** came back empty.
- **No studio breakdown of a signage pipeline** (Rockstar, Hangar 13, Ubisoft, Warhorse) was read. Everything in A1 but the repository's own note is a search summary.
- **Z-Image-Turbo's 0.93 English accuracy** is the vendor's paper, by summary. The repository's own pictures show worse.
- **The dates of the shift from signwriting to Perspex and vinyl** come from a sign-makers' summary only.
- **Unverified points from memory:** the Marquee as a real club; PhONEday's date; Comic Sans' date.
- **Every count and effort figure** in A5 and B6 is an estimate.

# Sources

All read or searched on 3 October 2026.

1. Rockstar Games, Graphic Designer job listing. https://job-boards.greenhouse.io/rockstargames/jobs/6617567003. Undated. [SS]
2. PC Gamer, "The latest GTA 6 trailer confirmed its most exciting feature: A bunch of logos for pretend companies". https://www.pcgamer.com/games/grand-theft-auto/the-latest-gta-6-trailer-confirmed-its-most-exciting-feature-a-bunch-of-logos-for-pretend-companies/. Undated. [SS]
3. GTA Wiki, "Steven Walsh". https://gta.fandom.com/wiki/Steven_Walsh. Undated. [SS]
4. Made Good Designs, "What Font Does Red Dead Redemption Use? (2026)". https://madegooddesigns.com/red-dead-redemption-font/. 2026. [SS]
5. Watch Dogs Wiki, "London Underground". https://watchdogs.fandom.com/wiki/London_Underground. Undated. [SS]
6. TechRadar, "Everybody's Gone to the Rapture, and you're stuck in an English suburb". https://www.techradar.com/news/gaming/everybody-s-gone-to-the-rapture-and-you-re-stuck-in-an-english-suburb-1301921. Undated. [SS]
7. Jakub Vaja, "Mafia Definitive Edition", ArtStation. https://conflig.artstation.com/projects/nY8NB4. Undated. [SS]
8. Naughty Dog's outsourced signs: 80.lv, 8 December 2020, as read in production/research/shop-window-interiors/GOODS-2026-10-03.md. [READ, repo]
9. Wikipedia, "Transport (typeface)". https://en.wikipedia.org/wiki/Transport_(typeface). Undated. [READ]
10. roads.org.uk, "Fonts". https://www.roads.org.uk/fonts. Undated. [SS]; UNREACHED by fetch.
11. smugpie, "uk-ire-road-sign-fonts", README. https://github.com/smugpie/uk-ire-road-sign-fonts. Undated. [READ]
12. Department for Transport, Traffic Signs Manual, chapter 7 (2018). https://assets.publishing.service.gov.uk/media/5c78f8c7e5274a0ebfec719c/traffic-signs-manual-chapter-07.pdf. 2018. [SS]
13. The Beauty of Transport, "How Serifs Lost the Road War but Won the Streets". https://thebeautyoftransport.com/2021/11/03/how-serifs-lost-the-road-war-but-won-the-streets/. 3 November 2021. [SS]
14. Typography.Guru, "Digital version of MoT serif available?". https://typography.guru/forums/topic/61301-digital-version-of-mot-serif-available/. Undated. [SS]
15. Google Fonts repository, METADATA.pb for each font named (ofl/… and apache/…). https://github.com/google/fonts. Read 3 October 2026. [READ]
16. Google Fonts, Fraunces DESCRIPTION.en_us.html. https://github.com/google/fonts/tree/main/ofl/fraunces. Undated. [READ]
17. Z-Image paper. https://arxiv.org/pdf/2511.22699. November 2025. And SiliconFlow, "Z-Image-Turbo ... Bilingual Text Rendering". https://www.siliconflow.com/blog/z-image-turbo-now-on-siliconflow-photorealistic-bilingual-text-rendering. Undated. [SS]
18. Wikipedia, "Poll Tax Riots". https://en.wikipedia.org/wiki/Poll_Tax_Riots. Undated. [READ]
19. Hackney Museum, poll-tax objects (for example 1990-399, 1991-115). https://museum-collection.hackney.gov.uk/object-1990-399. Undated. [SS]; UNREACHED.
20. People's History Museum, "Can't pay, won't pay! The Poll Tax 35 years on". https://phm.org.uk/blogposts/cant-pay-wont-pay-the-poll-tax-35-years-on/. 2025. [SS]; UNREACHED.
21. Wikipedia, "Letraset". https://en.wikipedia.org/wiki/Letraset. Undated. [READ]
22. Designing Buildings, "Shop signs" (https://www.designingbuildings.co.uk/wiki/Shop_signs), and signpainting.co.uk, "Letters Potent: The Modern Age" (https://www.signpainting.co.uk/lettering/modern-age.htm). Undated. [SS]; the second UNREACHED.
23. Wikipedia, "Signwriter". https://en.wikipedia.org/wiki/Signwriter. Undated. [READ] (no dates in it)
24. Wikipedia, "Film poster". https://en.wikipedia.org/wiki/Film_poster. Undated. [READ]
25. Wikipedia, "Road signs in the United Kingdom". https://en.wikipedia.org/wiki/Road_signs_in_the_United_Kingdom. Undated. [READ]
26. Wikipedia, "Graffiti in the United Kingdom" (https://en.wikipedia.org/wiki/Graffiti_in_the_United_Kingdom) [READ]; UP Magazine, "Bristol Street Art History" (https://upmag.com/bristol-history/) [SS]. Both undated.
27. Epic Games, "Runtime Virtual Texturing in Unreal Engine 5.8". https://dev.epicgames.com/documentation/en-us/unreal-engine/runtime-virtual-texturing-in-unreal-engine. 5.8. [READ]
28. Epic Games, mesh painting and decal actor pages. https://dev.epicgames.com/documentation/en-us/unreal-engine/mesh-painting-in-unreal-engine and …/decal-actor-in-unreal-engine. Returned empty; not evidence.
29. 80.lv, "Modular Scene in UE4: Blockout, Vertex Paint, Decals". https://80.lv/articles/001agt-004adk-005cg-modular-scene-in-ue4-blockout-vertex-paint-decals. Undated. [SS]
30. a-maze.games, "Material Blend Decal". https://www.a-maze.games/blog/material-blend-decal. Undated. [SS]
31. Fab listings:
    - https://www.fab.com/listings/04d9fea2-1619-4218-87da-41e105846d7e
    - https://www.fab.com/listings/6cb359eb-b5da-4d91-a1ef-8c84574fd95b
    - https://www.fab.com/listings/8a917a97-2285-46ee-b5fe-c8850e1a4730
    - https://www.fab.com/listings/5dea5581-20be-4e00-9a03-488e9c836687
    - https://www.fab.com/listings/b74989f3-2f36-424d-a147-1bb16ef8dd2d

    Undated. [SS]; UNREACHED.
32. ambientCG, Sticker001 (https://ambientcg.com/view?id=Sticker001) and licence (https://docs.ambientcg.com/license/). Undated. [SS]; UNREACHED (403).
33. Poly Haven licence. https://polyhaven.com/license. Undated. [SS]; UNREACHED.
34. TextureCan (https://www.texturecan.com/category/Decals/) and 3DTexel (https://3dtexel.com/decals/). Undated. [SS]; UNREACHED.
35. karlwirbelwind, "[CC0] Decal - Graffiti Textures", Sketchfab. https://sketchfab.com/3d-models/cco-decal-graffiti-textures-4af449f78bec4c55807350773ceb5e5b. Undated. [SS]
36. Fab support, "Introducing NoAI meta tags and Created with AI self-declaration", January 2025, as cited in production/research/wardrobe-at-scale/3-METAHUMAN-AND-FAB.md. [SS there]
37. GameFromScratch, "Epic Games Make Massive FAB Announcements". https://gamefromscratch.com/epic-games-make-massive-fab-announcements/. Undated. [SS]
38. Game Informer, "Kingdom Come: Deliverance II Preview". https://gameinformer.com/preview/2024/04/18/here-comes-the-kingdom. 18 April 2024. [SS]

**Read in this repository, 3 October 2026:**
- the brief;
- CLAUDE.md;
- DECISIONS.md (the last forty lines, and D53's lines);
- canon.md (lines 40 to 60 and Brands and law);
- content/brands/brand-bible-v1.json;
- ledger-v2/research/license-allowlist.md;
- production/research/aaa-street/SUMMARY.md and 1-PIPELINE.md (the decal lines);
- street-clutter-1990/SUMMARY-2026-09-29.md;
- shop-window-interiors/GOODS-2026-10-03.md, FISHMONGER-2026-10-03.md and CLOSE-RANGE-2026-10-03.md;
- natural-idles/NOTE.md (line 67);
- production/specs/fab-free-megascans.md and street-wear.json;
- production/reference/photographs.md, hook-sheet.png and kcd2-town-arcades.jpg (looked at);
- tools/street_wear.py, make_wear_masks.py and decal-ink.py (heads), props/make_vignette_2d.py (head), art-recipes/terrace-front.py (the fascia section);
- ledger/Assets/StreamingAssets/Decals/THIRD-PARTY.md, and generated/ATTRIBUTION.json, PROGRESS.txt, imagegen-verdict.txt and manifest.json, with four of its pictures looked at;
- production/assets/vignette/decals2d/fascia_mickeys_plain.png (looked at).
