# A street that holds up beside KCD2: the method, and the proof frame to build first (research summary, 1 October 2026)

**The question (Jafar, 1 October).** Quay Street in Unreal 5.8 follows its concept sheet's layout, but it is far from the realism of a current AAA game. The bar is a frame that holds up beside the two Kingdom Come: Deliverance 2 frames (production/reference/kcd2-town-arcades.jpg, kcd2-town-fountain.jpg).

The research covered:
- how AAA teams build a realistic street in Unreal 5, from start to finish;
- how much of that one person directing AI can do;
- what is free, and on what licence;
- the light;
- 1990 vehicles and street furniture;
- what one view needs, item by item.

**How it was done.**
- Five separate helpers each took one question. Each was given the problem, not a theory, and spent about thirty minutes reading only, with dated sources. Their notes are beside this file:
  1. `1-PIPELINE.md`: the environment-art pipeline, and what agents can do at each step.
  2. `2-EPIC-FREE-CONTENT.md`: what Epic and others give away, and on what licence.
  3. `3-LIGHT-AND-GRADE.md`: a damp overcast day, a sodium night, the grade, and the cost on the RX 6700.
  4. `4-VEHICLES-AND-FURNITURE.md`: 1990 cars, vans and street furniture: sources, precedent and law.
  5. `5-PROOF-FRAME.md`: one view of Quay Street item by item, with effort.
- This session then read the deciding sources itself, and the game's own files and frames ("Checked here", below).
- **D** marks what a source says; **I** marks inference.

**Limits.**
- Most of the web was blocked to all six of us: Fab, unrealengine.com and its forums, 80.lv, ArtStation, GDC Vault, Polycount, Poly Haven, CG Channel and most news sites.
- The session's shared search budget ran out near the end.
- **Read in full:** Epic's 5.8 documentation (dev.epicgames.com), the Unreal EULA, Wikipedia, and this repository.
- **Everything else** comes from search-engine summaries, and is marked as such in each note.

## The answer in short

1. **The gap is not engine features.** The PS5 corner of 23 September switched every feature on and changed 2.4% of pixels, at more than twice the cost. What AAA teams spend their time on is:
   - a kit of real architectural parts, with trims;
   - a brick material that does not visibly repeat;
   - wear and grime laid over everything;
   - dense set dressing;
   - light set by values (light levels, exposure, sky brightness) and judged in the game's camera.

   Light falling on clean, uniform surfaces cannot look real, so switching on features changed little (I, from notes 1, 3 and 5).
2. **The professional pipeline**, in order (note 1):
   - a target frame and one "beautiful corner" polished to final quality first;
   - a blockout;
   - a modular kit on a grid, with trim sheets (shared strips for sills, lintels and copings, with bevelled edges baked in);
   - assembly by rules, with variety;
   - real depth where the camera sees it;
   - wear by decals and paint;
   - set dressing in three tiers;
   - light and grade;
   - then a loop against the target frame until it holds.
3. **One person directing agents can do most of the making.** Agents can write the kit, the rules, the decal placement and the scatter by script. What they cannot do is judge. Each step still needs an eye: the builder's against the references, then a fresh reviewer's, then Jafar's on whole frames (note 1, I).
   - **New, free and documented in 5.8:** Unreal's procedural tools can assemble facades from kit pieces by rule (shape grammar). Epic ships a skill "designed to guide a LLM through the process of building a shape grammar from scratch" (D, read here).
4. **No free Epic city content fits a 1990 northern English street** (note 2):
   - City Sample: American buildings, cars and furniture, and Unreal-only.
   - Electric Dreams: a jungle.
   - Fab's giveaways this month: nothing for us.

   What does fit is scanned *surfaces*: kerbs, drains, covers, wet asphalt, concrete, and decals for stains and cracks. These come from Megascans (some free since 2025) and from Poly Haven and ambientCG (CC0). The buildings, cars and furniture stay ours. For the cars, canon decides: every vehicle is fictional, and no real car model may appear (note 4).
5. **The night's "one flat orange" has a likely cause in the game's own settings** (read, not run; note 3):
   - The street gets the same sky light at night as on the overcast day.
   - Under that light is a fog five times denser, coloured orange-brown.
   - The exposure is held fixed.

   Real sodium pools fall off by about four stops between lamps. Here, broad fill and orange haze fill those gaps.
6. **The proof frame:**
   - the hook camera's view by day, brought to the bar in a fixed order;
   - about a week for the steps that change the whole frame, and three to five weeks for the near half at the bar;
   - about 30 to 50 builder-days for the whole view, night included;
   - every figure is an estimate (note 5, I).

## Where the street stands (today's frames, checked here)

Today's frames are production/approvals/2026-10-01/street-hook-day.webp, -night, and street-A and street-B. Against the Hook sheet and the KCD2 frames, by eye and in the files.

**Composition**
- **The sides are canon's, not a mistake.** The sheet has Mickey's and the parade on the left; the game has them on the right. Canon rules the parade to be the east side (Jafar, 22 September), and the hook camera stands at the quay end looking north, so the game is right and the image-made sheet has the sides the other way round.
- **What the game lacks is the sheet's depth.** The sheet's road bends and rises, and the street opens onto the hillside in mist. The game's road runs straight into a flat block whose windows are black holes.

**Facades**
- **The reveals exist but do not read.** The generator already sets windows 102.5 mm back (production/specs/vignette-scene.json, reveal_depth_m), as real sashes are. They look flush because nothing darkens them: no dirt in the reveal, no stain under the sill, and soft, even light.
- **The wear layer was never built.** Jafar ruled on 21 September that "grime is the strategy" (D53), with wear as a separate layer. The street generator says plainly that the wear layer "is not this station" (tools/art-recipes/terrace-front.py), and no wear pass exists. This is the street "too clean" of his verdict.
- **The brick repeats.** One brick texture at one saturation repeats about every 2 m on the near corner. Every bay in the parade is identical: the same windows, chimneys and pots.

**Ground**
- **The decals are flat picture quads,** lifted 1 cm off the surface (ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp), not Unreal's projected decals. That is the likely reason the puddles read as stickers (read, not run).
- **The road reads dry, light and new.** The sheet's is dark, wet and reflective.

**The rest of the frame**
- **Cars and props:** the cars are boxes. The phone box, skip and pallets are stand-ins.
- **Clutter:** there are about ten props, against forty or more in the KCD2 arcades frame.
- **The hillside:** stepped boxes at the same contrast as the foreground.
- **The day:** the sky is flat white, with no haze between near and far.

## 1. How AAA teams build it, and what agents can do (note 1)

- **The target first.**
  - Studios polish one small area to final quality before anything else, Tim Cain's "beautiful corner" (D).
  - Blockout screenshots are painted over to plan the art pass, and values are checked under game light from the start (D, I).
- **The kit.**
  - **Studio kits on a grid:** Skyrim used 512-unit pieces; The Division's tool picks a panel per wall tile; City Sample has 2,000+ modules split into corner, wall and entrance per storey; Warhorse built kits so few pieces make many buildings (D, summaries).
  - **For an 1880s terrace (I):**
    - a grid of one brick plus joint (225 mm across, 75 mm a course), so brick lines run across seams;
    - 25 to 40 pieces per style: shopfront parts, sash bay with lintel, sill and reveal, corner, string course, eaves and gutter, slate roof, chimney and pots, downpipe, yard wall, ginnel arch.
- **Trim sheets** (Insomniac's "Ultimate Trim", GDC 2015):
  - one shared strip layout, with bevels baked in on every edge so edges catch the light;
  - each material comes as a trim and a plain tiling version (D, summary);
  - we have only the tiling half.
- **Assembly with variety.** Every large city in the sources is built by rules from kits, then polished by hand: The Matrix Awakens' 7,000 buildings, Spider-Man's Manhattan (D, summaries). Unreal 5.8's shape grammar does this for free (D, read here).
- **Depth where the camera sees it.** At the game's resolution a pixel is about 5 mm at 10 m. So the order of value is (I, arithmetic checked here):
  1. silhouettes against the sky (chimneys, pots, ridges, gutters);
  2. reveals, sills, lintels, cornices and kerbs as real geometry;
  3. brick relief by Nanite displacement, only on the walls nearest the player.

  Nanite cannot take mesh decals (D, read).
- **Wear.** Projected decals for leaks, streaks and grime; dirt blended in by material decals; painted masks (D). Rules a script can apply (I):
  - splash-back on the lowest 300 mm of wall;
  - streaks under sills and gutter joints;
  - soot above flues;
  - algae under downpipes;
  - oil and gum on the ground;
  - worn paint on doors;
  - puddles in the dips.
- **Set dressing in three tiers.**
  - **Primary:** signs, blinds, A-boards and stalls, built by hand as about ten assemblies.
  - **Secondary:** bins, posts, bollards and covers.
  - **Tertiary:** litter, leaves and cigarette ends.

  The secondary and tertiary tiers are scattered by rule along the pavement (D, I).
- **Scale and time.**
  - KCD2: Warhorse grew from about 100 to 250 staff over about seven years (D, summary).
  - Solo portfolio streets: one to four months each (D, summaries).
  - A Venice street: about 1,000 hours over a year (D, summary).

## 2. What is free, and on what licence (note 2; the EULA clause checked here)

- **Megascans.**
  - Free to all until the end of 2024, and anything claimed then stays free forever (D, summaries).
  - Paid since 2025: single assets from $0.99, packs from $24.99. A starter set of about 1,500 is still free under the Fab Standard licence, which is on our allowlist (D, summaries). Its contents could not be listed: Fab was blocked.
  - **Whether Jafar's Epic account claimed the library in 2024 decides how much is already ours.** Only he can look, signed in, and it costs nothing.
- **City Sample, The Matrix Awakens and Electric Dreams.** All are "UE-Only Content".
  - The Unreal EULA allows UE-only content in "a Product that requires the Engine Code to operate" (§1(B)(i), re-read here), so in law an Unreal game may ship it.
  - Our allowlist admits Epic's Unreal-only content for animation only (entry 8, 30 September). None of these fits the period anyway: American high-rises, cars and furniture, and a jungle.
  - **No licence change is needed.** What is worth taking from them is *method*: how City Sample's procedural buildings and Electric Dreams' spline tools are set up, read in the docs.
- **CC0, already allowed:**
  - Poly Haven: used for the shop rooms; also its barrels and crates, and a 16K overcast London sky image, for light only, since modern cars are in it.
  - ambientCG: 2,000+ materials. Its bricks and paving lean continental, so check the bond and size against UK photographs.
- **Not on our allowlist; would need a ruling:** Textures.com, TurboSquid, BlenderKit, KitBash3D and the Unity Asset Store. None is needed.
- **To avoid:** ue3dfree, unityunreal, 3d-model.org and gfx-hub. They are piracy mirrors.

## 3. Light, atmosphere and grade on the RX 6700 (note 3; the game's settings checked here)

**Overcast day**
- **Sky:** an unclipped overcast sky image on a distant dome, lighting one sky light. Epic calls this "the most common technique used in linear games" (D, summary).
- **Exposure:** fixed, at EV100 10 to 12 (heavy overcast is EV100 12 in the ANSI tables; D, read).
- **Sun:** a faint, soft directional light.
- **Fog:** low height fog starting 10 to 20 m out, so the far roofs separate from the street (I).
- **Wet:** Lagarde's physically based wet surfaces: porous brick and asphalt darken to 0.5–0.7 of their colour and their roughness falls to about 0.15–0.35; puddles fill the dips, driven by a height map (D, summary; values I).
- **Reflections:** software Lumen is enough for damp asphalt, which blurs them anyway (I).

**Sodium night**
- **The lamps:**
  - lamps that fall off as real light does, using a cut-off lantern's light profile;
  - every lamp may cast shadows (there are only three to five);
  - lit shop windows with a light aimed at the pavement;
  - houses warm behind curtains;
  - exposure held at EV100 3 to 4, so pools sit a little under mid-grey and the gaps near black (I, to be settled with a grey card in the game's camera).
- **The arithmetic** (checked): a 35 W lamp's 4,550 lumens on a 6 m column gives about 10 lux beneath and 0.5 lux midway to the next, which is 4.3 stops.
- **The game's own night** (unreal-look.json and the wet_night row, read here, not run):
  - **The sky light.** The street gets 0.35 × 1.0 of the sky light at night against 0.70 × 0.5 by day: the same.
  - **The fog.** Density 0.022 against 0.004, up to 45% opacity against 10%, coloured orange-brown on purpose.
  - **The lamps.** 300 lumens of glow plus a 1,200-lumen cone, look numbers.
  - **The first test:** Unreal's lighting-only view in the game's camera, with the sky light and then the fog switched off one at a time.

**Grade**
- **Tonemapper:** keep Unreal's filmic tonemapper.
- **Order:** set mid-grey on a grey card first, then white balance (daylight balance kept at night so the sodium stays deep orange), contrast and saturation.
- **Last:** grain, a slight vignette, and lens effects nearly off (D, read; I).

**Cost on the RX 6700, the card in Jafar's PC**
- **The card:** about a PS5's graphics chip (D, summary).
- **Settings for 60 frames a second (I):**
  - software Lumen at High;
  - virtual shadow maps on Nanite meshes, cached;
  - no hardware ray tracing;
  - volumetric fog at night only;
  - contact shadows on characters only;
  - upscaling (TSR or FSR 3.1) from 58–67% of full resolution.
- **KCD2's own path:** its CryEngine bounced light with no ray tracing runs above 60 at 1440p Medium on the same class of card (D, summary).
- **What brought it to the bar** was art, values and grade (I).

## 4. Period vehicles and street furniture (note 4; canon checked here)

- **Canon decides the main question.** "Every brand, band, club, product, weapon and vehicle is fictional. No real ... logos ... car models" (canon.md, Brands and law). So every bought model of a Sierra, Volvo 240, Transit or Routemaster is out, whatever its licence.
- **No free, allowlisted, British period car, van, bus, kiosk or pillar box was found.**
  - The only generic paid pack: lyoshko's "1980s Cars Pack" on Fab, $124.99 (hatchback alone $34.99). Partly American, not seen by eye.
  - Dekogon's street props (made for The Matrix) are American, and "British - City Pack" is modern London (D, summaries).
- **How others did it.**
  - The Getaway licensed about fifty real cars.
  - GTA, Watch Dogs: Legion and Driver invent makers and blend several cars of one class.
  - Mafia follows single cars closely, which is the riskiest practice.
  - Everybody's Gone to the Rapture (1984 Shropshire) built its vehicles in-house (D, summaries).
- **The rule for ours (I):**
  - an invented maker;
  - each car blended from three or more cars of its class, with the lamps, grille, window line and rear pillar changed;
  - class dimensions from blueprints as ranges, never traced;
  - no Mini, Defender, black cab or Beetle shapes;
  - cars kept off the key art;
  - one line of provenance per vehicle.

  UK design rights on any car sold before about 2001 have expired (D, summary). That is not legal advice.
- **AI 3D generators** give a rough shell at best: wheels melt, arches close, panel gaps blur (D, vendors' own blogs). TRELLIS needs an NVIDIA card. Hunyuan3D is banned by our allowlist.
- **What it means:**
  - Keep the scripted route already started (tools/art-recipes/car-model.py), brought up to the bar: stance, glossy paint with reflections, glass with an interior behind it, wear.
  - Script the street furniture too.
  - The kiosk's operator mark and the pillar box's cypher are still owed by canon's brand bible (canon.md, Brands and law).

## 5. What one view needs, item by item (note 5)

The hook camera's view by day, in the order that gains the most realism per hour. Effort is in builder-days, with agents scripting Blender and Unreal and the builder judging; every figure is an estimate (I).

| # | Item | Done looks like | Days |
|---|---|---|---|
| 1 | **Depth of composition**: road bending and rising, the closing block opened to the hillside, canon's sides kept | Laid over the sheet, the far end opens as the sheet's does | 0.5–1 (more if the layout moves) |
| 2 | **Atmosphere**: height fog, haze, a structured overcast sky, a few chimney smokes | Hillside clearly paler than the street; sky not flat white | 0.5–1 |
| 3 | **Wet street**: darker, glossier road and pavement; soft puddle mask; darker wall bases | Road dark and reflective as the sheet's | 1–2 |
| 4 | **Brick breakup**: no visible repeat; two or three brick sets tinted per house; soot, streaks, algae, splash band, repairs | No repeat at the near corner at 2560×1440; each house distinct | 3–5 |
| 5 | **Facade variety and trims**: arch heads, sills with a drip, sash detail, nets, plinth, varied doors, heights and pots, one stone and one painted house as the sheet has | The parade no longer reads as copy and paste | 4–7 |
| 6 | **Shopfronts in view**: pilasters, consoles, cornice, recessed doors, tiled thresholds, blind boxes, posters; interiors (the pawnbroker's method) | No black window in the frame; Mickey's holds up at 2 m | 3–5 |
| 7 | **Ground**: separate kerb blocks, drain grates, gutter grime, varied grey flags, cracks, patches, gum, covers, oil, worn lines, all as projected decals | The bottom third of the frame holds up | 3–5 |
| 8 | **Clutter**: from about 10 to 40–60 objects in three tiers | Two to four objects at every doorway | 4–7 |
| 9 | **Hillside**: the street's kit reused at distance, gardens, retaining walls, trees, in haze | A town in mist, not stacked boxes | 2–4 |
| 10 | **Cars at the bar** | Stance, reflections, interior, wear | 3–5 |
| 11 | **People posed**: walking, looking in windows, contact shadows (clothes are their own track) | No one standing rigid facing the camera | 2–4 |
| 12 | **Night**: pools and dark gaps, lit windows, sky glow, wet streaks | Not one orange wash | 2–3 |
| 13 | **Grade**: tonemapper checked, exposure fixed per light, faint grain and vignette | Midtones and highlights read as a photograph | 0.5 |

**What the table adds up to (I)**
- **First week:** items 1 to 4, plus the light values in section 3, change the whole frame at once.
- **The bulk:** items 5 to 8, about three weeks.
- **The whole view:** about 30 to 50 builder-days.
- **Two cautions:**
  - The sameness comes from the generator, so the variety and wear masks must be made by the generator, not painted by hand.
  - The proof only proves a method if items 4 to 8 are made as reusable kit pieces and materials.

## The recommended method

1. **Keep the street's own generator, and give it what AAA kits have** (items 4 to 6; V4's "stains and wear").
   - **Variety:** a variation seed per house (brick set, tint, door, pots, height).
   - **Trims:** a trim sheet for sills, lintels, copings, fascias and gutters.
   - **Brick:** a brick material that breaks its repeat at large scale.
   - **Wear masks:** written by the generator for each surface, as D53 asked on 21 September.

   Blender stays the modelling tool, and nothing is bought.
2. **Build the wear pass as real projected decals, placed by rule** (V4).
   - Replace the flat picture quads with Unreal's projected decals: splash-back, streaks under sills, soot, algae, oil, gum, cracks and puddles in the dips.
   - The pictures come from Megascans' free set and from CC0 scans, re-checked against UK photographs.
   - Wear coverage is printed per surface, as D53 already specifies.
3. **Set light by values, not switches** (V5 and the day).
   - **First the night test:** the sky light and fog switched off one at a time, in the game's camera.
   - **Then the values:** fixed exposure by day and by night; the sky image on a dome; the fog's start distance; lamps with real falloff and a cut-off profile; a grey card in the scene.
   - **Then the costs:** software Lumen, virtual shadow maps, and no hardware ray tracing, measured on the RX 6700 as a frame time beside each frame.
4. **Dress in three tiers** (V2, V4).
   - Ten hand-made primary assemblies.
   - Secondary and tertiary objects scattered by rule along the pavement.
   - Cars, kiosk, skip and pallets scripted to the bar from dimensions, with invented makers (canon), or removed, as V2 already allows.
5. **Gate every step as the rules already say.**
   - First the builder's check against the Hook sheet, the KCD2 frames and the 1990 photographs.
   - Then a fresh reviewer.
   - Then whole frames on Jafar's page, with their shortfalls named first.
   - The two-tries rule applies to each item.
6. **Later, for the town, not for the proof:** try Unreal 5.8's shape grammar, with Epic's LLM skill, on one terrace style. It would assemble facades from the same kit by rule inside Unreal, the way City Sample's 26-plus styles are built. It is worth a trial only once the kit and materials have passed in the proof frame.

## The proof frame to build first

**Which view**
- The hook camera's view by day, from the quay end.
- Mickey's and the next two frontages, the pavement, kerb and road in front of them, and the far end opened onto the hillside in haze.
- Judged in the game's own camera and exposure, against the Hook sheet and the KCD2 arcades frame.

**In this order**
1. Items 1 to 4, the light values, and the night test from section 3: about a week.
   - Show this stage as a whole frame, with its shortfalls named.
   - Its point is to prove the order of work, not to pass.
2. Items 5 to 8 on the three near frontages: about three weeks.
   - This is the first frame that should be able to stand beside KCD2.
3. Items 9 to 13 and the night frame, only after Jafar's yes on stage 2.

**Timing and size**
- **When it starts:** the list decides. Today's order puts the interface before the visual bar (NOW.md), and V1, the pawnbroker's window, is already on its way to his page. This frame is how V2 to V5 would be done.
- **Size:** about six to ten weeks of builder work in all, by estimate. This is much bigger than the list's lines look, so it is said plainly here.
- **The first week's stage is the cheap test of the method.**

## Decisions for Jafar

1. **Megascans.**
   - **One thing only he can do:** sign in to Fab, and look whether his library already holds the Megascans claimed in 2024.
   - **Then:** use the free ones and the CC0 libraries, and buy nothing until the proof frame names a gap (recommended). At most a one-off of about $20 for named surfaces.
2. **Unreal-only content from Epic beyond animation:** no change to the allowlist is needed; nothing of it fits (recommended: leave entry 8 as it is).
3. **The paid 1980s car pack ($35–125, one-off):** no (recommended). It is partly American and unseen, and canon's fictional cars are better scripted.
4. **Scope:** the proof frame in two stages, the first week shown before the rest is built (recommended), or the whole near half straight through.

## Checked here

- **The UE-only clause** of the Unreal EULA for Creators, §1(B)(i), re-read from the PDF.
- **Epic's 5.8 documentation:**
  - The City Sample PCG page: the shape grammar LLM skill, quoted exactly; shape grammar not marked Experimental (its cross-section node is).
  - The shape grammar page: the rule `<A,B,C>` is a fallback, not a random pick, which corrects note 1.
- **canon.md:**
  - "Brands and law" (fictional vehicles; the owed kiosk and pillar-box marks).
  - The ruling that the parade is the east side, which corrects note 5's "mirror".
- **The game's own files:**
  - reveal depth (0.1025 m);
  - the night sky light, fog and lamp values;
  - the flat decal quads;
  - the generator's own note that the wear layer is not built;
  - D53.
- **The helpers' arithmetic:** lamp falloff, EV100, pixel size.
- **One correction to note 4:** TRELLIS needs an NVIDIA card with 16 GB, per this repository's own note, not 24 GB.

## Not verified

**Marketplaces and licences**
- Every Fab, Sketchfab, TurboSquid and CGTrader listing, price and licence label was seen only as a search summary.
- The contents of the free 1,500 Megascans, and whether brick, slate, flagstones, kerbs or decals are among them.
- Whether Jafar's account claimed Megascans in 2024.
- The current full Fab EULA. The Unreal EULA read here is undated.
- The licences of Old West, Cropout, Project Titan and the Megascans sample scenes. What is in Industrial Infrastructure. The reported sale of Sketchfab in August 2026.

**Method and time**
- Every breakdown article (Venice, London, Japanese street, Spider-Man, Skyrim, The Division, The Matrix, Ultimate Trim): durations, piece counts and kit sizes come from summaries and may be paraphrased wrongly.
- How Warhorse built KCD2's towns: team size, scanning, dirt layering. No source with hours for a British terraced street at this standard.
- Whether Nanite displacement is still experimental in 5.8.
- Every effort figure in this summary. They are estimates, not measurements.

**Light and cost**
- Every benchmark, none measured on an RX 6700.
- The cost of volumetric clouds, rain particles and bloom.
- The night exposure: EV100 3 to 4 here against 2 to 3 in evening-light-1990. A grey card in the game's camera settles it.
- That the sky light and the fog cause the flat orange night. It is a reading of the settings, not a test.

**Vehicles and law**
- How lyoshko's cars look.
- Hum3D prices.
- EU copyright in car shapes after Cofemel (2019).
- Any 2023–24 ruling after the Humvee case.
- The quality of AI-made cars, beyond the vendors' own claims.
