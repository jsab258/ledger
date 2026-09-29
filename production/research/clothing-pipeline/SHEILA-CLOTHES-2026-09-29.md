# Sheila's clothes, 1990: cardigan, blouse, pleated skirt (research note, 29 September 2026)

The clothing session asked for this before making Sheila Dunn's clothes. A separate helper was given the problem, not a theory, and worked for about thirty minutes, read only. Every source was read on 29 September 2026. **D** means documented, with its source. **I** means the helper's inference. "Search summary" means only a search engine's summary was seen, not the page. Pictures could not be viewed: for photograph sets, only the captions and dates were read.

## In short

- **Route (I).** *Cardigan:* do not sew it. Build it as a close offset of her body in the reference pose, with the proportions taken from FreeSewing's Sven. Open the front and add a button band. Model the ribbing; the knit stitch comes from a tiling normal map. Skin it from the body, with no Chaos. *Blouse:* model only what shows, a flat round collar drafted by the shoulder-overlap rule, over the cardigan's neckband. *Skirt:* take the hip part from FreeSewing's Sarah and lay the pleats in by the three-times rule, knee length, stitched down to the hip. Build it by projection, not sewing. Skin the top; the bottom is Chaos.
- **The closest dated reference is a museum costume.** The V&A holds the brown, knee-length, side-pleated skirt worn by Dot Cotton in *EastEnders*, about 1985, with its measurements. Her wardrobe is recorded as "neat cardigans, patterned blouses" (D [R1]).
- **FreeSewing has no pleated skirt, no cardigan and no Peter Pan collar.** It has Sarah, a skirt block after Aldrich (v4.2, 2025); Sven, a set-in sweatshirt with ribbing; Hugo, a raglan; Bella, a women's bodice block; and Hortensia, a handbag (D [F1]–[F7]).
- **Chaos keeps pre-folded pleats.** Its bending constraints default to rest angles taken from the 3D rest mesh. They can also use a flatness ratio or explicit angles (D [E1], 5.8 source). Blender's cloth also takes its rest shape from the first frame (D [E3]).
- **Knitwear is a close, stretchy layer, so the set-in sleeve problem mostly goes away** if the cardigan is an offset surface rather than sewn panels (I). The seam line becomes a drawn detail.
- **Skirt weights:** keep the skirt on the pelvis, not the thighs, with InpaintMask below the hip (I, from our 29 September note [L1]). Sitting is the test.
- **No dated photograph was verified to show the whole outfit.** Four sets to look through are named in A (D for the dates; the contents are I).

## A. References

- **Dot Cotton's costumes, V&A, all about 1985 (D [R1]).**
  - Skirt S.109-2023: brown, knee length, side pleats, lined, side zip, a false-pocket button at the back. Length 66 cm, waist 35 cm flat, hem 66 cm flat.
  - Skirt S.110-2023: red, Jaeger label, 67 cm long.
  - Blouses S.113-2023 (checked viscose, collared) and S.112-2023 (a pussy-bow).
  - The wardrobe came from charity shops and was approved by June Brown.
  - I: this is the nearest real analogue to Sheila: a working-class woman of her generation, dressed by a costume department from real second-hand clothes. The flat hem is about twice the flat waist, so the pleats are grouped at the sides, not all round.
- **Ordinary high-street knit (D [R2]):** a grey machine-knitted wool cardigan by Marks & Spencer, 1989, V&A T.98-1994. The record gives no sleeve or band details.
- **Photograph sets to look through (D for the dates; whether each shows this outfit is not verified):**
  - Tom Wood, *Women's Market*, Great Homer Street, Liverpool, 1978 to 1999. Captions dated 1989 to 1992 [R3].
  - Martin Parr, *The Cost of Living*, Bristol, 1986 to 1989 (search summary [R4]).
  - The Kays catalogue for 1990, fashion pages 48–49 and 388–389 [R5].
  - Henry Grant's London archive at the London Museum, CC BY-NC 4.0. His shopper in a cardigan over a blouse is dated February 1971, before canon's window [R6].
- **Pattern leaflets:** Patons printed "set in sleeve" crew- or V-neck cardigans (search result title only [K1]). A retro classic by Pat Menchini (2023) has set-in sleeves, a deep ribbed welt and ribs running up from it [K2]. Crimplene had become "day wear for the suburban middle-aged" from the early 1970s (search summary [R7]).
- **I, to confirm against the pictures:** a hand-knitted cardigan for a woman in her fifties in 1990 was hip length, close but not tight, and done up to the top. It had 7 to 9 buttons, 3 to 5 cm ribbing at the welt and cuffs, a knitted-on or separate front band, and a round neck. Set-in sleeves were the "classic"; raglan was also common. A round collar would lie over the cardigan's neckband. Tights were flesh-coloured; the shoes were flat lace-ups.

## B. Patterns

- **Blouse.** Simone has chest, waist and hip ease, a bust adjustment, and a stand collar with nine options, but no flat or round collar (D [F4]). Bella is a women's bodice block with darts and sleeves, based on an Italian industry block (D [F7]). The rule for a Peter Pan collar: lay the front and back bodices together at the neck point, with the shoulder tips overlapping 2 cm. Trace the neckline and draw the collar about 4 to 5 cm wide. Make the top collar 3 mm bigger than the under collar all round, so the edge seam rolls under (D [P1], 2017). I: take the neckline from Simone or Bella and draft only the collar.
- **Cardigan.** No FreeSewing design opens at the front. Sven is Brian plus ribbing: set-in sleeves, ribbing height 3 to 15% (default 8%), ribbing stretch, length bonus 0 to 30%, hip ease (D [F5]). Hugo is a raglan with ribbing height 4 to 20% and seam-shift options (D [F6]). I: take Sven's proportions, open the centre front, and add a 2.5 to 3 cm band.
- **Skirt.**
  - Sarah is the natural-waist block from Aldrich's *Metric Pattern Cutting for Women's Wear* (6th edition) (D [F2][F3]). It needs waist, seat, hips, waist-to-seat, waist-to-hips and waist-to-floor. Length runs from 25 to 100% of waist-to-floor, and there are three pairs of darts, a waist drop and ease options. Penelope is a pencil skirt, Sandy a circle skirt.
  - The traditional rules (D [P2], 2019): for all-round knife pleats, share the darts' width out among the pleats; the pleats are then made by slash-and-spread, and the top is stitched down to hold them. Touching pleats take three times the finished width (search summary [P3]).
  - I: for Sheila (waist 824 mm, hips 931 mm), all-round pleats need about 2.8 m of cloth at the hem. Dot's skirt suggests grouped side pleats, which are lighter to simulate. Knee length on a 1.50 m woman is about 55 to 60 cm from the waist.

## C. Making them

1. **Pleated skirt as game cloth.**
   - Marvelous Designer makes a knife pleat from three internal lines with opposing 180-degree folds (D [G4], 2020). Its fold angles are 0 and 360 degrees for the two fold directions, and 180 for none (search summary [G5]).
   - Chaos bending elements take rest angles from the 3D mesh by default. They also offer buckling ratio and buckling stiffness (D [E1]).
   - I: model the pleats into the rest mesh, stitched flat to the hip. Skin the yoke. Simulate below the hip with high bending stiffness, max distance rising from 0 at the hip to a few centimetres at the hem, and leg capsules. Keep self-collision off. If the pleats cost too much, use a coarse sim cone that drives the pleated render mesh.
   - Test sitting before anything else. A skirt skinned to the pelvis is pierced by the thighs when they lift; the front hem needs some thigh weight or simulation.
2. **Knitwear.**
   - Loops, ribs and cables have real height and self-shadow, so smooth-cloth normal maps undersell them. Normal maps carry the yarn-level detail (search summary [G3]).
   - I: model the ribbing as geometry at the welt, cuffs and bands; they carry the silhouette. Put the stocking stitch in a tiling normal and roughness map with a slight fuzz. Add a few irregular stitches for the hand-knit look. Beige wool must be checked against the references under the street's light.
3. **Blouse under a cardigan.** Production games often delete or hide what the clothes cover, which also stops layers poking through (D [G1], forum, 2022). There is a MetaHuman 5.6 body-mask tutorial (search summary [G2]). I: model only the collar and the small visible front. If the cardigan ever comes off in the game, the whole blouse is needed; that is a scope question.
4. **Sleeves.** Our earlier notes cover this [L1]: drape in an A-pose, weld the seams at low gravity, then lower the arms. Epic advises masking the armpit and crotch for inpainted weights. I: a close knit made as a body offset has no cap to ease in; the armpit is solved by skin weights, not sewing. Raglan or set-in is then a line on the texture. Choose it from the photographs.

## D. MetaHuman clothing tools, 5.6 to 5.8

- The Outfit Asset (5.6) resizes garments for the parametric MetaHuman. Resizing works only in the editor, not while the game runs. A morph-target import bug was fixed in 5.7.1 (D [E2], Epic staff, 12 September and 28 October 2025).
- TransferSkinWeights has no bone exclusion. InpaintMask forces smooth, inpainted weights where it is set, such as the skirt below the hip. The skeletal-mesh template keeps the garment's own weights (D [L1]).
- Max distance limits how far a vertex leaves its skinned place; backstop stops it going inward (D [L1]).
- No Epic example of a skirt was found. Epic's documentation pages load by script and could not be read.

## Sources (all read 29 September 2026)

- [F1] FreeSewing, designs list, freesewing.eu/designs and /docs/designs/ (undated).
- [F2] FreeSewing, Sarah, freesewing.eu/designs/sarah and /docs/designs/sarah/options/ (undated).
- [F3] FreeSewing newsletter, 2025 Q4, freesewing.eu/newsletter/2025q4 (1 October 2025).
- [F4] Simone options, /docs/designs/simone/options/ (undated).
- [F5] Sven options, /docs/designs/sven/options/ (undated).
- [F6] Hugo options, /docs/designs/hugo/options/ (undated).
- [F7] Bella, freesewing.eu/designs/bella (undated).
- [P1] R. Khusainova, "How to draft and sew a Peter Pan collar", blog.fabrics-store.com (10 October 2017).
- [P2] Minna, "Discover how to draft flared and pleated skirts", theshapesoffabric.com (9 March 2019).
- [P3] Search summary: minervapatterns.com "Drafting pleats" (undated; the page refused) and blog.treasurie.com "Knife pleats" (undated).
- [R1] V&A S.109-2023 (collections.vam.ac.uk/item/O1757988), S.110-2023 (O1757989), S.113-2023 (O1757991), S.112-2023 (O1757990), given by the *EastEnders* Costume Department; records read through api.vam.ac.uk (undated records).
- [R2] V&A T.98-1994, Marks & Spencer cardigan, 1989 (O69860), © V&A.
- [R3] AnOther, "At the Women's Market", anothermag.com (11 September 2018).
- [R4] Search summary: thephotographersgallery.org.uk and huxleyparlour.com on *The Cost of Living* (undated).
- [R5] Worcestershire Archive, "Kays at Christmas, 1990", explorethepast.co.uk (19 December 2019).
- [R6] London Museum, Henry Grant, "Woman shopper with a shop assistant", object 767941, February 1971, CC BY-NC 4.0.
- [R7] Search summary: "Crimplene", en.wikipedia.org (undated).
- [K1] Search result title: Ravelry, Patons "Set in Sleeve Cardigans - crew neck or v neck" (undated).
- [K2] Ravelry, Pat Menchini, "Retro Classic Cardigan", *Knitting* magazine 239 (January 2023).
- [G1] blenderartists.org, "Question about clothes and hiding/deleting geometry underneath" (17–20 December 2022).
- [G2] Search summary: Epic community tutorial, "Body Mask for Metahumans in Unreal Engine 5.6" (undated).
- [G3] Search summary: style3d.ai blog on knitwear displacement (undated).
- [G4] J. Versluis, "How to use the Pleats tools in Marvelous Designer", versluis.com (26 December 2020).
- [G5] Search summary: Marvelous Designer support, "Fold/Sew Pleats" (undated; the page refused).
- [E1] Unreal Engine 5.8 source on this PC: Chaos `PBDBendingConstraintsBase.h` (ERestAngleConstructionType: Use3DRestAngles, FlatnessRatio, ExplicitRestAngles) and `PBDBendingConstraints.h` (default Use3DRestAngles; BucklingRatio, BucklingStiffness).
- [E2] Epic forum, "Tutorial: Chaos Cloth Outfit Asset Resizing Addendum" (19 August 2025; replies 12 September and 28 October 2025).
- [E3] Blender manual bundled with the Blender MCP: physics/cloth/settings/shape.rst ("Dynamic Mesh") and physical_properties.rst (bending model) (undated).
- [L1] Our notes: production/research/character-pipeline/cloth-weight-maps-2026-09-29.md; clothing-pipeline/SLEEVES-RECIPE-2026-09-29.md, SKINNING-TROUSERS-2026-09-29.md, FIT-AND-STIFFNESS-2026-09-29.md.
