# Clothes: the clothing session's list

The third session (Jafar, 29 September): clothes for the people of a British port town in 1990, made in Blender only, in C:\Users\Jafar\ledger-clothes on the branch clothes, pushed to main. Bodies come from the builder in F:\LedgerTools\bodies ("Handovers to clothing" in NOW.md); finished garments go to F:\LedgerTools\garments with a line under Handovers in NOW.md. Worked in order; when an item is done, take the next. All free: nothing bought (Jafar, 30 September: not Marvelous Designer).

## How the work is done (Jafar, 30 September)

- THE METHOD FIRST. Before a new kind of work, research how professionals do it from start to finish, the whole pipeline, with dated sources; only then specific problems. When something fails, ask first whether the method is wrong, before fixing the symptom. (The first list researched symptoms, sleeves dragging and seats sinking, and that cost the clothes.)
- GAME CLOTHES ARE SKINNED MESHES, NOT SIMULATED CLOTH. A garment is a skeletal mesh skinned to the MetaHuman skeleton, its weights transferred from the body and fixed by hand at the joints; only loose parts (a hem, a skirt, coat tails) are simulated. The garments set aside on the first list were judged as simulated cloth, which is where the armpits and the bagging came from.
- The builder tests the poses in Unreal; I watch "Handovers to clothing" in NOW.md for his results.

## The list, in order (Jafar, 30 September)

- [ ] 0. Research first: how game studios make clothing for realistic characters from start to finish, and how the MetaHuman pipeline expects it (production/research/clothing-pipeline/PIPELINE-2026-09-30.md). IN HAND.
- [ ] 1. Remake the set-aside garments by that method: shape from my drapes, sculpting or a free base, bound to the skeleton, joints fixed, only loose parts simulated. The jacket first (Ron's donkey jacket), then Ron's jumper and work trousers, Darren's shell-suit jacket and jeans, Sheila's cardigan, the flat cap, and the shoes. The builder tests them in Unreal.
- [ ] 2. Free ready-made tailored clothes (jackets, coats, suits) from MakeHuman's CC0 libraries and anything else free on the allowlist, altered and re-coloured to read as 1990 British working clothes, bound the same way.
- [ ] 3. Then the next principals' simple garments (Tom Nowak first, then in CASTING.md's order) as the builder exports their bodies.

## Done on the first list (29 and 30 September)

- Handed to the builder, each through a blind review (production/art/clothing/footwear, accessories, darren-tshirt, sheila): Ron's work boots; Darren's belt, pager and white T-shirt; Sheila's pleated skirt, cream blouse, handbag, and spectacles with their chain (refitted to her S4 head); her tights as a skin material.
- Set aside under the two-tries rule, now item 1 above: the donkey jacket and its builds (production/art/clothing/donkey-jacket-sewn), Ron's work trousers and the flat cap (work-trousers, flat-cap-sewn), Sheila's cardigan (sheila), Ron's jumper (ron-jumper), Darren's shell-suit jacket (darren-shellsuit), trainers and jeans (footwear, darren-jeans), Sheila's shoes (footwear). Their best candidates are kept in F:\LedgerTools\tmp\clothes.

## Status

- 30 September, morning: the first list finished (handed over or set aside); the new list started with the pipeline research.
- Bodies: Ron (MH_RoccoP2), Darren (MH_SamC5), Sheila (MH_LenaC1, and MH_LenaS4 with her approved head for anything on her face) in F:\LedgerTools\bodies; the slim, average and heavy builds are set aside by the builder. The next principals wait on his exports.
- Tools: Blender 4.5.13 headless (tools/meshgen/blender); scratch on F:. Blender scripts and these records set off nothing on push; records under production/ run the free Core tests; production/specs and production/assets would start the Unreal build, so garments never go there.
