# Ron's moustache swapping colour with distance (2 November 2026, 13:30)

Fault (film 2026-11-02-1237): a dark-brown handlebar in frames 1-10 and 61-89, a thin grey one in 11-60 (darkest pixels about RGB 80/42/16 against 119/87/52). His head hair is grey throughout. Read without opening Unreal.

## Questions

1. Which levels does the moustache have, with which material, and when does it switch?
2. Do the cards take colour from parameters or a texture; does recolour_hair reach them?
3. The levers, ranked; can Sheila's and Darren's grooms swap the same way?

## 1. Levels and switch

- Ron's built groom (MH_RoccoP2/Grooms/Mustache_L_Full) has 8 levels: 0-1 strands, 2-4 cards, 5-7 meshes. Only cards 1 and 3 and meshes 5 and 7 are kept. Epic's High build drops the rest (MetaHumanGroomEditorPipeline.cpp 114-141).
- Material slots: strands MI_Hair, cards MI_Facial_Hair, meshes MI_Hair_Helmet. The blueprint sets them to the three built MI_WI_Mustache_L_Full_None_1_* instances, in the right order.
- The groom's own screen sizes are not used. Ron's LODSync maps the Mustache, Hair and Eyebrows to groom levels 1, 3, 5 and 7, and Face drives it (LODSyncComponent.cpp 208-247). So face LOD0 shows strands, face LOD1 cards, face LOD2 meshes.
- The face changes level at screen sizes 0.2, 0.1 and 0.05, so the swap is the face crossing 0.2. That is about 2.6 m with the 78° room lens, using the face's own 24 cm bounds (estimate).

## 2. Colour on the cards

- There is no colour texture. The cards carry only attribute and tangent maps. M_Facial_Hair, M_hair_v4, MF_Hair_Color and MF_Hair_SaltAndPeper all compute colour from hairMelanin, hairRedness and WhiteAmount.
- hair_materials catches all three moustache instances (the "/Grooms/" path, the "MI_" start, the Mustache_L_Full stem). All three hold the brief's 0.35, 0.05 and 0.7. **The hypothesis is wrong as stated:** the recolour does reach the far version.
- What differs is the cards' material. The moustache's MI_Facial_Hair is translucent, with bIsHairCards off and a base melanin of 0.8, a dark brown. His head hair at the same level, with the same three values, uses MI_Hair_Cards (masked, bIsHairCards on) and stays grey. So the facial-hair cards material does not render the grey that WhiteAmount gives the strands. Whether only the whitening is lost is unverified.
- A second, later swap (unverified): from face LOD2 the build paints facial hair into the face texture, using the character's own groom parameters. The after-build recolour never touches those (MetaHumanDefaultGroomPipeline.cpp 107-183, GroomTextureMinLOD 5).

## 3. Levers, ranked

1. **First: keep strands at face LOD1.** Change the Mustache entry in Ron's LODSync CustomLODMapping from 1,3,5,7 to 1,1,5,7 (LODSyncComponent.cpp 278). One blueprint field, no rebuild. Cost: about 1,400 strands, against Epic's 10,000 for facial-hair LOD0 (H3-performance.md); frame time not measured. The swap moves out to about 5 m, where the grey mesh level takes over.
2. Point the card slot at an instance of MI_Hair_Cards holding the three values. It uses the same card texture layout (Layout2) and is proven grey on his head hair. No strand cost; the look of masked moustache cards is unknown.
3. Also set Ron's groom parameters at build (groom_params, as Tom's build does). This fixes the painted layer from face LOD2 on. Needs a rebuild.
4. bIsHairCards on in the built instance: effect unknown, new shader version.
5. Tinting a texture: none exists. Removing the cards level equals lever 1.

**Sheila and Darren.** Their head-hair cards use MI_Hair_Cards, so no colour swap is expected there. Their brows use the facial-hair cards (Sheila 0.5 melanin with 0.2 white; Darren 0.65 with 0.1), so they may lose their grey at the same distance. Darren's stubble has no card or mesh level and should vanish beyond face LOD0 (unverified). Both use the 1,3,5,7 mapping, so lever 1 covers them too.

## Not checked

- The material graphs; no shader was run.
- The face component's real bounds and the distance in each frame.
- The painted face texture's moustache colour (its thumbnail is too small).
- Strand cost in milliseconds.
- Epic's LOD page (controlling-metahuman-levels-of-detail-lods-in-unreal-engine, read 2 November) names no facial-hair levels. It says grooms have up to 8 levels, card hair is best at Min LOD 3, and r.HairStrands.UseCardsInsteadOfStrands forces cards.
