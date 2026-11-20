# Clothes and hair in Unreal: a different method, ready for when Unreal resumes

Written 20 to 21 November 2026 (Swiss time) for his decision of 22:01, 20 November: Unreal's look work stays paused until the browser prototype proves the game; this note keeps the biggest risk visible. Nothing here starts work now. Web sources were read on 20 November 2026; "estimate" marks this note's own reading.

## In short

- First route, clothes: stop making layers meet while the game runs. Each named character gets one fixed outfit as one skinned mesh, the inner layer cut away where hidden. Folds come from drapes already made (the Marvelous export, Kiln's drapes); collars are modelled to the drafted pattern, not simulated. Cost: nothing new.
- First route, hair: make each period cut as a groom in Blender (free), export it to Unreal as strands for close-ups and turn it into cards with Epic's free Hair Card Generator for the 3.1 m camera. Start with one short men's cut and test it in the packaged game on day one.
- Second routes: Marvelous Designer to MetaHuman by Epic's documented route (Marvelous Individual, about US$39 a month or US$280 a year), and Houdini Indie with Epic's MetaHuman for Houdini hair kit (US$299 a year).
- Judge at talking distance against KCD2 frames, on the clothing floor and the hair pass list, in the packaged build.
- 1 February: one page, one character, showing whether the bar is in reach.

## 1. Where LEDGER stuck

- Clothes. Kiln v1 passes 0 of 6 garment lines; the jacket over the jumper, the coat's collar and the blouse's underarm fail (19 Nov state: layered set aside). Earlier, a tailored jacket draped in Blender read as "a loose smock" and its lapel never held (lab, 7 Oct); plain clothes modelled to a pattern without draping looked like skin and tracksuit bottoms (lab, 8 Oct). Marvelous Designer lapses on 26 November after an export to F:.
- The engine. Unreal's Outfit Asset warps one stored size to a new body; a saved MetaHuman character bakes every outfit into a plain skinned mesh and drops cloth movement (read in the 5.8.2 code, lab notes).
- Hair. No character's hair has passed. Strands were kept over cards on 8 November because cards gave a flat helmet and white blotches at Tom's camera; Tom's crown stays too pale, and the sky light was ruled out as the cause on 9 November (direct light or highlights on thin roots are the suspects). Houdini's free licence cooks hair but cannot export it to Unreal.

The common thread: the hard parts (two layers touching, a collar's roll, a crown's density) were left to a simulation or a stock preset to get right on their own, and each failed in its own way.

## 2. How it is done professionally, late 2026

### Clothes

- Draping. Studios and skilled solo artists drape in Marvelous Designer or CLO, which handle layers by layer order natively. Marvelous prices on its own page: Individual (Personal) US$39 a month or US$280 for a prepaid year; Enterprise US$199 a seat a month. An indie tier was added in January 2026 with no published price.
- Unreal 5.6 to 5.8. Epic's parametric clothing: an Outfit Asset holds cloth assets and warps them from a source body to a target body; a simulation mesh is optional; a USD export from Marvelous or CLO brings one. Epic warns the warp is worst for realistic, detailed clothing far from the source and encourages several outfits for several source bodies. Marvelous publishes the route step by step (USD into Unreal, a Cloth Asset in the Dataflow editor with skin-weight transfer and remesh, an Outfit Asset from the resizable template, then MetaHuman Creator), needing Marvelous 2025.2 and Unreal 5.6 or later. A forum report (April 2026, one reply asking for details, no fix) finds simulation lost after assembly, matching LEDGER's code reading.
- Layering in practice. On 5.8, separate Fab trousers still poke through shirts (September 2026, unresolved; advice: inflate the outer layer in Blender). An October 2026 reply on fitting clothes to MetaHumans gives the working method: fit the garment to each body in Blender before skinning, through a low cage shrink-wrapped to the body with a small offset; copy skin weights from the body (at most four bones a point), copy the border weights at shoulders and waist from the nearest body point; hide the body under the garment with a mask, not by deleting faces; add pose correctives for the two or three worst poses. Epic's preset outfits do delete body faces under clothing.
- KCD2, from outside: Warhorse's only public clothing talk found is from the first game (GDC Europe 2015), on adjusting layers the player mixes so they do not overlap; nothing for KCD2.
- Time: no source reached. Estimate: a few days for one close-up outfit, one to two days for a short cut, several for a perm, for a skilled artist; LEDGER's agents slower the first time.

### Hair

- MetaHuman 5.7 (shipped November 2025) added MetaHuman for Houdini (guide-driven: preset styles, a hairline generator, clumping) and a Groom Advanced Kit, both on Fab, and a Maya XGen route. The 5.8 notes add only Dataflow nodes and Creator fixes; nothing says grooms can be authored inside MetaHuman Creator.
- Epic's Hair Card Generator, a plugin enabled in the editor and run through a Dataflow graph, makes cards and their detail levels from a groom (ships with the engine: not confirmed).
- Getting a groom in: Unreal reads Alembic curves with lowercase attributes beginning groom_ (version 1.5 required; root UV, width, guides, group and colour optional). Epic names Maya, Ornatrix, Yeti and Houdini, not Blender, but Blender add-ons write the same file: GroomForge (US$25 one user, lists Unreal 5.7 and 5.8, Blender 4.5 to 5.2) and a free "Groom Exporter from Blender" add-on (forum thread; date and licence not checked).
- Houdini: Apprentice is free; Indie US$299 a year or US$449 for two years; FX US$4,495. An old SideFX forum answer (2018) says Apprentice cannot export Alembic and Indie exports any supported format; this matches what LEDGER found (current terms unverified).
- Known faults in 5.7 and 5.8: MetaHuman grooms "exploding" across detail levels, reproduced by Epic on AMD cards in March 2026, worked around by turning off Solve Simulation; a Blender-made groom with generated cards visible in the editor but invisible in standalone and packaged builds (5.8, October 2026, no fix posted); indirect light under Lumen turning hair over-bright or golden (2025, no confirmed fix; suggested: turn off Lumen reflections for hair, use shadow maps). Crowd people get card hair by Epic's design (July 2026).
- Bought grooms: KhitrovArt sells period-useful men's cuts on Fab (a short comb-over with a low fade, strands only, no cards); GroomLab's short cut is marked "Allows usage with AI: No". No 1980s perm or set curls were found.
- KCD2 and RDR2's hair methods: nothing reached.

## 3. What to try first when Unreal resumes

### Clothes: one fixed outfit, built as one piece

For each named character (Ron first, as the ruling's proof asks), in order:

1. Take the drape. Use the Marvelous export on F: or a Kiln drape of each garment on its own, in Ron's pose. No new drape software, no layers draped together.
2. Build the outfit, not the garments. In Blender, put the jacket on as made; then cut the jumper away wherever the jacket covers it, keeping a few centimetres beyond the jacket's edges (neck, cuffs, hem), and join them into one mesh. The jumper can no longer poke through the jacket, because there is nothing left of it underneath.
3. Collars by drawing. The lab showed the pattern drafting is exact (Thornton's lounge coat to 0.15 inch). Model the shirt collar, coat collar and lapel to the drafted pattern, then check the outline against the pattern, as the sash window was checked; never ask a simulation to roll a collar.
4. Folds as surface. Remake the drape as a clean low-detail mesh with its own UVs, give it a woven fabric material from photographs, and bake the drape's folds into its surface, as the trade does.
5. Skin to the body. Copy weights from Ron's MetaHuman body, four bones a point, borders copied from the nearest body point; hide the body under the outfit with a mask; add correctives at the shoulders and underarms, where the blouse failed.
6. Only loose parts move. The coat's tails and a skirt hem may simulate, as the ruling allows, on a cloth part placed outside MetaHuman's assembly (untested; test it on day one); nothing else.
7. Packaged on day one. Ron walks, sits, turns and raises his arms in the packaged build, with the body-through-garment count at zero (the lab's check).

Why this should not repeat the stuck state: Kiln's three failures came from layers and a collar left to a simulation. The lab's 8 October clothes were modelled to a pattern with no simulation and still read as skin and tracksuit, through thin ease and no folds. So here the drape supplies ease and folds, the pattern only checks the collar's outline, the jumper never meets the jacket at run time, and the underarm is a skinning fix with a named corrective. Fixed outfits mean no mixing for the principals, which the story does not need. It also fits the rulings: skinned meshes, only loose parts simulated, garments from Blender or Marvelous, Kiln's work used where it is good (the drape).

### Hair: a hand-made groom, strands near, cards at the camera

1. One short men's cut first (Ron's; Darren keeps Epic's short cut, part of his frozen face), made with Blender's free hair curves against period photographs.
2. Density at the crown by hand: more, slightly thicker roots and a painted scalp under the crown, so the pale patch cannot open (the 9 November finding points there).
3. Export with a free Blender groom exporter (or GroomForge, US$25, see section 5); import as strands for the talk close-up; generate cards with Epic's Hair Card Generator for the 3.1 m camera and beyond.
4. Test the packaged build first, before any polish: the October report of Blender-made cards vanishing in packaged builds is exactly the fault that would waste weeks. Then test Lumen's over-bright hair, with hair's Lumen reflections off as the first candidate.
5. Walk the hair pass list: crown, close-up, 1 to 25 m with no colour jump between strands and cards, day to wet night, no shimmer, no hard or grainy shadow on walls, collar or neck, no pale scalp, frame cost.

Women's 1980s and 1990s styles follow only after one men's cut passes, as the hair ruling requires.

## 4. The second route, if the first fails

- Clothes: Marvelous Designer to MetaHuman, Epic's way. Drape the whole outfit in Marvelous, where layer order handles the jacket over the jumper; export USD; build the Outfit Asset with one source size per principal (Ron, Darren, Sheila each their own), accept that the saved character bakes it to a plain skinned mesh, and add correctives as above. This needs Marvelous again after 26 November. Fallback: export the drape as one mesh and return to the cut-and-join step.
- Hair: Houdini Indie with Epic's MetaHuman for Houdini kit (price not shown), the guide-driven route Epic built for MetaHuman hair, which exports grooms Unreal reads. Needs Houdini Indie.
- If both fail for hair, the honest fallback is Epic's stock grooms closest to each casting sheet, with the crown fault listed, and the hair bar moved on his page.

## 5. Money decisions (his alone)

| What | Cost | What it buys | When |
|---|---|---|---|
| Marvelous Designer Individual | about US$39 a month, or US$280 a year prepaid (an indie tier exists, price unpublished) | New drapes after 26 Nov; the second clothes route | Only if the first route needs new drapes or fails |
| Houdini Indie | US$299 a year, or US$449 for two years (revenue under US$100,000, a third-party page) | Exporting grooms; Epic's MetaHuman for Houdini kit; the second hair route | Only if the Blender groom fails |
| GroomForge (Blender add-on) | US$25 one user | One-click groom export with root UV, guides and cards | Optional; a free exporter is tried first |

Not routes: bought garments (his ruling), other sellers' NoAI items, paid outsourcing. Bought grooms (KhitrovArt on Fab, price not read, the seller's licence to check) are allowed but not recommended: no period perms were found, and the crown fault would remain.

Licences, judged here by the allowlist's principles: Marvelous on his own plan is already allowed (allowlist item 9; Marvelous's own avatars and samples stay out). Blender and its output are ours; each add-on enters only by a decision record naming its licence, read before install; its output is ours. Houdini Indie is a commercial licence under a revenue ceiling; it needs a decision record naming its terms before install, read from his PC. Epic's MetaHuman for Houdini kit is Epic's own Fab content, allowed even if tagged NoAI.

## 6. How to judge it

- Clothes: the floor (plain, period-plausible, no modern giveaways, no clipping or holes, nobody frozen stiff); principals at talking distance on the 2026 bar against KCD2 frames, side by side at the same framing; walking, sitting, turning and arms raised on film; body-through-garment count zero; a fresh reviewer against period photographs; then his eye in the game's camera.
- Proof of method, not of one garment: the second outfit (Darren) should take about half the first's time, as the tailor ruling asks.

## 7. The one-page view for the 1 February check

The page shows one character, Ron, at talking distance beside a KCD2 frame at the same framing, in the packaged build, and three lines:

- Green, the bar is reachable: if Unreal has resumed, Ron's outfit passes the floor with zero body points through, walks and sits on film, and one men's cut passes at least the crown, close-up and 3.1 m rows of the hair list (a check, not a pass; the hair gate needs every row and his look); Darren's outfit started at under the first's time.
- Amber, the bar is reachable at a cost: the first route passes clothes but not hair (or the reverse), and the second route's money is the open question, priced as in section 5.
- Red, scope or bar must move: both routes have failed on the same fault, or Unreal has not resumed and no method has been tested since 20 November. Then the choices are: fewer close-up principals (talk framed wider), stock grooms with the crown fault accepted, or the clothing exception widened.

If Unreal is still paused, the page says so and shows the last real pictures (8 November hair, Kiln's latest).

## Sources

Project records (wip and lane-2026-11, read 20 Nov 2026): RULINGS.md (Clothes; Faces, hair and voices; Sources, licences and money); ledger-v2/research/license-allowlist.md; production/lab/LAB-REPORT.md; production/lab/1-unreal-source/OUTFIT-ASSET.md; production/research/hair/HAIR-TEST-RESULT-2026-11-08.md; production/research/hair/CROWN-STEP0-2026-11-09.md; production/art/hair-2026-09-29/PASS-LIST.md; production/research/lane/BOSSES-SCAN-SINCE-8-NOV-2026-11-18.md; production/research/lane/CAR-METHOD-LANDSCAPE-2026-11-17.md (Houdini Indie terms).

Web:

- Epic, creating parametric clothing for MetaHuman (5.8 docs, undated): https://dev.epicgames.com/documentation/metahuman/creating-parametric-clothing-for-metahuman
- Epic, getting started with parametric clothing (5.8 docs, undated): https://dev.epicgames.com/documentation/metahuman/getting-started-for-creating-parametric-clothing-in-metahuman
- Epic, building an Outfit Asset (overview only reached): https://dev.epicgames.com/documentation/metahuman/building-an-outfit-asset-in-unreal-engine
- Epic, MetaHuman 5.8 release notes (undated): https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine
- Marvelous Designer, MetaHuman USD garment workflow (undated): https://support.marvelousdesigner.com/hc/en-us/articles/52699135975705-Marvelous-Designer-to-MetaHuman-USD-Garment-Integration-Workflow
- Marvelous Designer licence prices (undated): https://support.marvelousdesigner.com/hc/en-us/articles/47358269350041
- Digital Production, Marvelous indie pricing (12 Jan 2026): https://digitalproduction.com/2026/01/12/marvelous-designer-adds-indie-pricing-quietly/
- Forum, parametric clothing loses simulation (24 Apr 2026): https://forums.unrealengine.com/t/parametric-metahuman-clothing-with-simulation/2717622
- Forum, trousers through shirt in 5.8 (21 Sep 2026): https://forums.unrealengine.com/t/pants-are-popping-through-shirt-in-metahuman-cant-fix/2833148
- Forum, fitting clothing to MetaHumans in 5.8.3 (12 to 13 Oct 2026, community reply): https://forums.unrealengine.com/t/fitting-armour-clothing-to-metahumans-in-ue-5-8-3-best-workflow-to-avoid-hours-of-manual-fitting-per-set/2839852
- GDC Vault, Adaptive Clothing System in Kingdom Come: Deliverance (2015): https://gdcvault.com/play/1022822/Adaptive-Clothing-System-in-Kingdom
- MetaHuman 5.7 release (Nov to Dec 2025): https://www.metahuman.com/releases/metahuman-5-7-is-now-available
- Epic, Alembic for grooms: https://dev.epicgames.com/documentation/unreal-engine/using-alembic-for-grooms-in-unreal-engine
- Epic, Hair Card Generator: https://dev.epicgames.com/documentation/unreal-engine/creating-hair-cards-and-lods-using-hair-card-generator
- Epic, Houdini groom exporter: https://dev.epicgames.com/documentation/metahuman/houdini-groom-exporter
- SideFX forum, Indie and Alembic export (Nov 2018): https://www.sidefx.com/forum/topic/59577
- GroomForge on Superhive (2026): https://superhivemarket.com/products/groomforge
- Forum, free Groom Exporter from Blender add-on (date not checked): https://forums.unrealengine.com/t/groom-exporter-from-blender-free-addon/686778
- Forum, MetaHuman groom explosions in 5.7 (Dec 2025 to Mar 2026): https://forums.unrealengine.com/t/metahuman-grooms-hair-explosions-in-ue-5-7/2684304
- Forum, Blender groom invisible in packaged 5.8 build (15 Oct 2026): https://forums.unrealengine.com/t/custom-groom-alembic-from-blender-renders-in-pie-but-is-completely-invisible-in-standalone-and-packaged-build-ue-5-8-metahuman/2841252
- Forum, indirect light too strong on groom hair (May to Nov 2025): https://forums.unrealengine.com/t/reflected-indirect-light-on-metahuman-hair-groom-is-too-strong/2533751
- Forum, crowd people get card hair (Jul 2026): https://forums.unrealengine.com/t/groom-hair-on-metahuman-crowd-high-res-actors-matching-iskm-hair-color-materials/2744949
- Forum, KhitrovArt short comb-over groom (31 Jul 2026): https://forums.unrealengine.com/t/khitrovart-classic-short-comb-over-with-low-skin-fade-metahuman-groom/2739650
- Fab, GroomLab short brush-up groom (marked NoAI): https://www.fab.com/listings/0b7d1386-4b2b-4d84-8e5b-6b1b6435543a

Not reached: Epic's layering sub-pages for the Outfit Asset; KCD2 and RDR2 clothing or hair talks; time per outfit or hairstyle from any source; CLO, Maya, Ornatrix prices; Marvelous's terms on work after a subscription ends (LEDGER's ruling already keeps what is made).
