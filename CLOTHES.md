# Clothes: the clothing session's list

The third session (Jafar, 29 September): clothes for the people of a British port town in 1990, made in Blender only, in C:\Users\Jafar\ledger-clothes on the branch clothes, pushed to main. Bodies come from the builder in F:\LedgerTools\bodies ("Handovers to clothing" in NOW.md); finished garments go to F:\LedgerTools\garments with a line under Handovers in NOW.md. Worked in order; when an item is done, take the next. All free: nothing bought (Jafar, 30 September: not Marvelous Designer).

## How the work is done (Jafar, 30 September)

- THE METHOD FIRST. Before a new kind of work, research how professionals do it from start to finish, the whole pipeline, with dated sources; only then specific problems. When something fails, ask first whether the method is wrong, before fixing the symptom. (The first list researched symptoms, sleeves dragging and seats sinking, and that cost the clothes.)
- GAME CLOTHES ARE SKINNED MESHES, NOT SIMULATED CLOTH. A garment is a skeletal mesh skinned to the MetaHuman skeleton, its weights transferred from the body and fixed by hand at the joints; only loose parts (a hem, a skirt, coat tails) are simulated. The garments set aside on the first list were judged as simulated cloth, which is where the armpits and the bagging came from.
- The builder tests the poses in Unreal; I watch "Handovers to clothing" in NOW.md for his results.

## The list, in order (Jafar, 30 September, after an outside audit; it replaces the one before)

ONE GARMENT PROVEN ON TWO BODIES BEFORE ANY WARDROBE. STOPPED: new garment families, and accepting anything judged standing only.

- [ ] 1. One properly skinned jacket, Ron's donkey jacket, by the whole game pipeline. SET ASIDE 30 September under the two-tries rule: three blind reviews of the game-way jacket (production/art/clothing/donkey-jacket-game: review 1 passed Ron and failed Darren; reviews 2 and 3 failed both, the last after research). The pipeline works (a clean game mesh from the flat pattern, the bake, skinning with the joints corrected, the carry to Darren; tools/meshgen/blender/hang_drape.py, retopo_garment.py, skin_garment.py, carry_garment.py, look_garment.py); the shape the cloth drape gives does not (a rolled hem, full sleeves, the bodies' forms). WAITING ON JAFAR (scope): one last try at the shape, or park clothing until the builder can test in Unreal, or buy a ready-made jacket. The builder's own list stops visual work until his playable route runs, so no in-engine test is possible before then.
- [ ] 2. Proven on two approved bodies, Ron's (MH_RoccoP2) and Darren's (MH_SamC5), walking, sitting and with arms raised in Unreal, which the builder tests; I watch "Handovers to clothing". Every handover names the exact version of the body it fits (its file and checksum).
- [ ] 3. Only then the principals' outfits, by that proven pipeline.

Kept from the earlier list, not worked until 3: the MakeHuman CC0 suits (tools/meshgen/blender/fit_mhclo.py; a suit sits on Darren with gaps at the wrists and shins) and the garments set aside below.

## Done on the first list (29 and 30 September)

- Handed to the builder, each through a blind review (production/art/clothing/footwear, accessories, darren-tshirt, sheila): Ron's work boots; Darren's belt, pager and white T-shirt; Sheila's pleated skirt, cream blouse, handbag, and spectacles with their chain (refitted to her S4 head); her tights as a skin material.
- Set aside under the two-tries rule, waiting for item 3: the donkey jacket and its builds (production/art/clothing/donkey-jacket-sewn), Ron's work trousers and the flat cap (work-trousers, flat-cap-sewn), Sheila's cardigan (sheila), Ron's jumper (ron-jumper), Darren's shell-suit jacket (darren-shellsuit), trainers and jeans (footwear, darren-jeans), Sheila's shoes (footwear). Their best candidates are kept in F:\LedgerTools\tmp\clothes.

## Status

- 30 September, morning: the first list finished (handed over or set aside); the pipeline researched.
- 30 September, afternoon: the game-way jacket set aside after its third blind review; Jafar asked how to go on.
- 30 September, 10:00: an outside audit narrowed the list to one jacket proven on Ron and Darren; the eased sewn jacket failed its second blind review (the yoke's edges); retopology, bake and skinning researched before the remake.
- Bodies: Ron (MH_RoccoP2), Darren (MH_SamC5), Sheila (MH_LenaC1, and MH_LenaS4 with her approved head for anything on her face) in F:\LedgerTools\bodies; the slim, average and heavy builds are set aside by the builder. The next principals wait on his exports.
- Tools: Blender 4.5.13 headless (tools/meshgen/blender); scratch on F:. Blender scripts and these records set off nothing on push; records under production/ run the free Core tests; production/specs and production/assets would start the Unreal build, so garments never go there.
