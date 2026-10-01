# Clothes: the clothing session's list

The third session (Jafar, 29 September): clothes for the people of a British port town in 1990, made in Blender only, in C:\Users\Jafar\ledger-clothes on the branch clothes, pushed to main. Bodies come from the builder in F:\LedgerTools\bodies ("Handovers to clothing" in NOW.md); finished garments go to F:\LedgerTools\garments with a line under Handovers in NOW.md. Worked in order; when an item is done, take the next. All free: nothing bought (Jafar, 30 September: not Marvelous Designer).

## How the work is done (Jafar, 30 September)

- THE METHOD FIRST. Before a new kind of work, research how professionals do it from start to finish, the whole pipeline, with dated sources; only then specific problems. When something fails, ask first whether the method is wrong, before fixing the symptom. (The first list researched symptoms, sleeves dragging and seats sinking, and that cost the clothes.)
- GAME CLOTHES ARE SKINNED MESHES, NOT SIMULATED CLOTH. A garment is a skeletal mesh skinned to the MetaHuman skeleton, its weights transferred from the body and fixed by hand at the joints; only loose parts (a hem, a skirt, coat tails) are simulated. The garments set aside on the first list were judged as simulated cloth, which is where the armpits and the bagging came from.
- The builder tests the poses in Unreal; I watch "Handovers to clothing" in NOW.md for his results.

## The list, in order (Jafar, 30 September, after an outside audit; it replaces the one before)

ONE GARMENT PROVEN ON TWO BODIES BEFORE ANY WARDROBE. STOPPED: new garment families, and accepting anything judged standing only.

- [ ] 1. One properly skinned jacket. SET ASIDE 30 September under the two-tries rule, twice: the donkey jacket made the game way (three blind reviews, production/art/clothing/donkey-jacket-game) and MakeHuman's CC0 suit jacket (three blind reviews, the last after research: Ron failed only on two small local breaks, Darren on shape; production/art/clothing/suit-jacket). The pipeline and its tools stay (retopo_garment.py, skin_garment.py, carry_garment.py, fit_mhclo.py with its jacket form, mh_garment.py, look_garment.py). WAITING ON JAFAR (scope, FOR-JAFAR.md Clothes): (A, recommended, carried on meanwhile) the builder tests the suit jacket in Unreal on Ron and Darren with its skirt as cloth, when his list allows (F:/LedgerTools/garments/suit_jacket_test); (B) park clothing until his route runs; (C) a paid Fab jacket.
- [ ] 2. Proven on two approved bodies, Ron's (MH_RoccoP2) and Darren's (MH_SamC5), walking, sitting and with arms raised in Unreal, which the builder tests; I watch "Handovers to clothing". Every handover names the exact version of the body it fits (its file and checksum). IN HAND 1 October: the builder filmed the suit jacket in the game (production/art/clothing/suit-jacket-ingame-2026-10-01): walking and arms raised clean on both men; sitting, the skirt followed the thighs at 4 cm, and the whole jacket as cloth tore because the shirt and tie simulated with it; answered with a shell-only cloth mesh, 12 cm for the skirt and its front on the pelvis (F:/LedgerTools/garments/suit_jacket_test), to be filmed again.
- [ ] 3. Only then the principals' outfits, by that proven pipeline. BROUGHT FORWARD by Jafar, 1 October (his no to Wednesday's looks, relayed by the builder: "The clothes read 2020s, slim jeans with contrast stitching and slip-on trainers, not 1990 Hull"): plain 1990 clothes for Ron (MH_RoccoP2), Sheila (MH_LenaS4) and Darren (MH_SamC5) before the friends' build, no contrast stitching, no trainers, each judged against the bar (production/reference/hook-sheet.png and the KCD2 frames). Agreed with the builder: I made Darren's plain black leather lace-up boots, which failed their blind review against the bar (production/art/clothing/footwear/darren-boots-review-1.md: they hold in every pose but read as a placeholder; footwear lofted from the skin cannot reach the bar), so Epic's plainest boots go to the builder as a swap; he fits my ready pieces (Sheila's blouse, skirt, tights, handbag, spectacles; Darren's T-shirt, belt, pager; Ron's boots are in) and swaps Epic's plainest for Ron's jumper and trousers, Darren's jeans and Sheila's cardigan and flats.

Kept from the earlier list, not worked until 3: the MakeHuman CC0 suits (tools/meshgen/blender/fit_mhclo.py; a suit sits on Darren with gaps at the wrists and shins) and the garments set aside below.

## Done on the first list (29 and 30 September)

- Handed to the builder, each through a blind review (production/art/clothing/footwear, accessories, darren-tshirt, sheila): Ron's work boots; Darren's belt, pager and white T-shirt; Sheila's pleated skirt, cream blouse, handbag, and spectacles with their chain (refitted to her S4 head); her tights as a skin material.
- Set aside under the two-tries rule, waiting for item 3: the donkey jacket and its builds (production/art/clothing/donkey-jacket-sewn), Ron's work trousers and the flat cap (work-trousers, flat-cap-sewn), Sheila's cardigan (sheila), Ron's jumper (ron-jumper), Darren's shell-suit jacket (darren-shellsuit), trainers and jeans (footwear, darren-jeans), Sheila's shoes (footwear). Their best candidates are kept in F:\LedgerTools\tmp\clothes.

## Status

- 30 September, morning: the first list finished (handed over or set aside); the pipeline researched.
- 30 September, afternoon: the game-way donkey jacket, then the MakeHuman suit jacket, each set aside after three blind reviews; Jafar asked how to go on (scope).
- 30 September, 10:00: an outside audit narrowed the list to one jacket proven on Ron and Darren; the eased sewn jacket failed its second blind review (the yoke's edges); retopology, bake and skinning researched before the remake.
- Bodies: Ron (MH_RoccoP2), Darren (MH_SamC5), Sheila (MH_LenaC1, and MH_LenaS4 with her approved head for anything on her face) in F:\LedgerTools\bodies; the slim, average and heavy builds are set aside by the builder. The next principals wait on his exports.
- Tools: Blender 4.5.13 headless (tools/meshgen/blender); scratch on F:. Blender scripts and these records set off nothing on push; records under production/ run the free Core tests; production/specs and production/assets would start the Unreal build, so garments never go there.
