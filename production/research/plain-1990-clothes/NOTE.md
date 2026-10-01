# Plain 1990 clothes on three MetaHumans, fastest sound path (research note, 1 October 2026)

A separate helper was given the problem, not a theory. It spent about thirty minutes, read only, and ran nothing on the graphics card. **D** means documented, with a source number. **L** means read on this PC. **I** means the helper's inference.

The problem: Jafar's ruling of 1 October. The cast's clothes read 2020s: slim jeans with contrast stitching, and slip-on trainers. Before the friends' build he wants plain 1990 clothes, with no contrast stitching and no trainers, for Ron (MH_RoccoP2), Sheila (MH_LenaS4) and Darren (MH_SamC5). The bar is Kingdom Come: Deliverance II.

## In short

1. **What makes them read 2020s is three Epic pieces, and the colours we left on them.** Today Ron wears Epic's Sweater, Jeans and Boots, Sheila wears Sweater, Jeans and Flats, and Darren wears a long-sleeved T, the *Slim* Jeans and the Casual Sneakers (L3, on the T2 takes; check this is still what the P2, S4 and C5 builds wear).
2. **Most of it can be fixed today by script, at no cost.** The fix is to swap pieces and set their colours. Every Epic wardrobe item exposes named colour slots, and Epic's own 5.8 example script sets them from Python (L1, L2).
   - The slim jeans have a **StitchColor** slot, so their stitching can be set to the denim colour.
   - The boots have a slot for stitches and lacing.
   - The regular (straight) Jeans have Primary, Secondary, Leather and Metal slots; which of them is the stitching needs one test grid (I).
3. **Pieces the clothing session has already handed over replace most of the rest.** They are ready, waiting only on fitting: Sheila's blouse, skirt and tights, and Darren's T-shirt, belt and pager (L4).
4. **New garments are still needed, and they are the slow part.** Ron needs work trousers and the donkey jacket, Sheila a cardigan, and Darren a shell-suit jacket. For a base, use MakeHuman's CC0 pieces (his ruling of 30 September), or cut down Epic's own fitted garments. Epic's garments are under the Fab Standard Licence, which allows changes (I, from the licence: "Modify and adjust").
5. **No money is needed, and no new licence.** Two things need Jafar:
   - **His Fab sign-in** to fetch Epic's free Oxfords, Chelsea Boots and Loafers.
   - **One canon tap:** Darren's casting sheet says "scuffed white trainers", and his ruling says no trainers.

## 1. What they actually wore: a northern port town, 1990

The images were **not viewed in this session**. Fab and the photo sites refuse automatic reading, and the shared browser pane was in use by another session. What the photographs show comes from the project's earlier notes, where the clothing session looked at them.

**Men in their fifties and sixties, working class.**
- **Outerwear:**
  - The donkey jacket: navy or black melton wool, a leather or PVC shoulder yoke, boxy, hem at the top of the thigh (production/reference/donkey-jacket-1990.md, from museum pieces and dated photographs, 1979 to 1992).
  - By 1989, dockers at Tilbury and those lobbying the TGWU wore **nylon anoraks and zip jackets**, with no donkey jacket in either frame (Report Digital, 14 April and 11 July 1989, in the same note).
  - The donkey jacket is one coat among several (I).
- **Trousers:** dark, heavy cloth, wide and straight in the leg, not tapered, the hem breaking on black boots. Seen in Peter Fryer's Smith's Dock, North Shields, 1990 to 1991 [W18], in production/reference/work-trousers-and-flat-cap-1990.md. Creased polyester "slacks" were a much-worn type (V&A, Farah trousers of 1986, blue crimplene [W16]).
- **Knitwear:** a plain machine-knitted wool cardigan or jumper. The V&A holds a grey Marks and Spencer cardigan of 1989 [W15]. On older men: a crew or V-neck jumper over a collared shirt (I).
- **Head and feet:** a checked tweed flat cap worn low (Fryer [W18]). Black leather boots or lace-ups (I).

**Women in their fifties.**
- A blouse with a small collar, a cardigan, a knee-length skirt (pleated or A-line), flesh tights, and flat lace-ups or court shoes. Outdoors, a raincoat or wool coat, and a headscarf or plastic rain hood. This is Sheila's sheet, and production/research/casting/dress-and-bearing-2026-09-28.md, from Hilda Ogden's costume, Gransnet memories, and a 1977 Hull photograph of fish-factory women in coats, headscarves and wellingtons.
- Trousers on women could still draw disapproval: a teacher's recollection in a 1998 TES article (same note).

**Young men, about 25.**
- 1990 was "era of shell suits" in Kays' own catalogue (Worcestershire Archive, 19 December 2019 [W14]).
- Also Harrington jackets, pale denim, and tapered high-waisted jeans (Wikipedia, "1990s in fashion" [W17]).
- Darren's sheet already says: a purple and teal nylon shell-suit jacket, a white T-shirt and stonewashed jeans.

**Colours (I, from the above):**
- Men: navy, black, charcoal, mid-grey, brown, bottle green, oatmeal.
- Women: beige, camel, cream, brown, navy, muted wine.
- Bright colour comes only from young people's nylon (the shell suit) and from purple, which Kays' 1990 catalogue shows as a fashion colour [W14].
- No black-on-black "techwear", and no saturated sportswear on anyone over 30.

**What reads 2020s, and what to avoid (I):**
- Slim legs tapering to a bare ankle.
- Crisp gold topstitching on dark raw indigo.
- Slip-on or knit-upper trainers.
- Athleisure fabrics, and cropped hems.
- Logos.

Real 1990 jeans often did have gold stitching (I), but on stonewash it reads faint. His ruling stands: stitching matches the cloth.

**Archives worth opening by eye before the gate:**
- Fryer, Smith's Dock, 1990 to 1991 [W18].
- Steve Thornton, *Fish Town*, Grimsby fish dock in 1990, 3,600 frames [W19].
- Alec Gill's Hessle Road archive, Hull, 1971 to 1987 [W20].
- Ken Grant, Liverpool and Birkenhead, 1986 onwards [W21].
- Report Digital's 1989 dock pictures.
- All are copyright: for looking only, never for textures or tracing (production/reference/photographs.md).

## 2. Epic's MetaHuman wardrobe, UE 5.6 to 5.8

- **Built in:** the 5.8 engine on this PC ships one outfit, `WI_DefaultGarment` (a shirt and shorts). Everything else is a download (L1). A 22 June 2026 guide to 5.8 says the same: "few clothes by default" [W3].
- **Epic's free set on Fab** (the "MHC Web App to Parametric Clothing Set"): Epic's seller page, read 1 October 2026, lists 24 items [W1]. Each is resizable, has four LODs and its own wardrobe item, and is under the Standard Licence. The Sweater was published 7 April 2026 for UE 5.7, as `oa_sweater.mhpkg` [W2].

| Item | Plain enough for 1990? | On this PC? |
|---|---|---|
| Sweater | **Yes**: a plain crew-neck knit; Ron's jumper, Sheila's stand-in | yes |
| Jeans (regular, straight) | **Yes for Darren**, stitching matched to the denim | yes |
| Slim Jeans Variants | **No**: the 2020s fit he named | yes |
| T Shirt / Tucked T Shirt Variants | Yes, plain white or grey under a jacket | T variants: yes |
| Boots (lace-up) | **Yes**: Darren now, townsmen | yes |
| Flats | Yes: Sheila now, recoloured brown | yes |
| Oxfords, Loafers, Chelsea Boots | Yes, likely (I; images not seen) | **no: need his Fab sign-in** |
| Hoodie, Cargo Pants, Shorts, Crop Top, Techwear | No | Cargo: no |
| Hightops, Running Shoes, Casual Sneakers, FlipFlops | No (trainers) | Sneakers: yes |

**Colour by script.** Each wardrobe item carries named colour slots (L2):
- Slim jeans: `PrimaryColorJeans_slm`, `StitchColorJeans_slm`, `LeatherTintJeans_slm`, `MetalTintJeans_slm`.
- Regular Jeans: `PrimaryColorJeans`, `SecondaryColorJeans`, `LeatherTintJeans`, `MetalTintJeans`.
- Boots: `PrimaryColorBoots`, `SoleColor`, `EyeletColor`, `StichesAndLacingColor`.
- Sweater: `PrimaryColorSweater`, `SecondaryColorSweater`.
- Flats: Primary, Secondary and Tertiary.

Epic's own script in the 5.8 install (`example_add_clothing.py`) uses three calls to set a garment's colour: `assemble_for_preview`, then `get_instance_parameters`, then `set_color`, on `PrimaryColorShirt` (L1). Epic's Python page says the same [W4, search summary only].

**More detail than the colour slots.** The materials underneath hold more settings than the colour slots expose (L3, the builder's dump of 24 September):
- `WearMaskStrength`, `pilling_normal_strength`, `A_FuzzAmount` and `B_FuzzAmount`, which give the worn wool, fuzz and pilling of the KCD2 look.
- `normal_CustomStitch_strength` and `Diffuse_mult_stitch`, which control the stitch relief and brightness.

A child material instance on the assembled mesh could set them (I; the same way garments.json already overrides the donkey jacket's materials).

**Limits:**
- The resizer works from Epic's four source bodies (medium build, standard and heavier, men and women: m/f, med, nrw/ovw) and may warp on unusual bodies. The fix is the "Source Size Override" (L, oa_jeans folder; [W2]).
- In 5.8, wardrobe items reset hand-made weights (production/research/game-clothing-pipeline/NOTE-2026-09-30.md).

## 3. Other sources, and their licences

| Source | What | Licence; on the allowlist? | Money |
|---|---|---|---|
| Epic's free set (above) | Plain basics and shoes | Fab Standard: **yes** | free; **his sign-in** |
| MakeHuman CC0 packs | Wool Pants, Fisherman Sweater, Turtle Neck, Long Full Skirt, Ankle Boots, Loafers, suits01; **no CC0 cardigan, anorak or coat worth having** (FREE-BASES-AND-COLLARS-2026-09-30.md) | CC0: **yes**. Check each item's own header, because a 2017 mirror of a worksuit says AGPL | free |
| City Sample Crowds (Epic) | Tops, bottoms and shoes on six older body types; modern American | **UE-Only Content** [W5][W6]: the allowlist's Unreal-only clause covers animation, not clothing, so **his licence ruling** would be needed | free |
| Third-party Fab outfits | e.g. Women's Outfit Pack, $24.99 (a wool skirt and a sweater; modern) [W8]; Workwear pack [W10]; Turtleneck & Blazer [W9] | Fab Standard: yes | **money**; on 30 September he ruled out paid Fab clothes for suits and coats |
| outfit-maker.com | e.g. a knee-length A-line skirt with front pleats, MetaHuman resizable, €19 personal or €119 professional [W7] | Its own EULA: **not on the allowlist** | money |
| Marvelous Designer / CLO | The industry tool for pattern and drape | Tools; $39 a month (MD) or $50 a month (CLO) (TAILORED-ROUTES-2026-09-30.md) | **money**; he ruled "no Marvelous Designer" on 30 September |
| Mutable (Epic plugin) | Mixes meshes, materials and textures at runtime, for crowds [W13] | Engine plugin; beta | free; not needed for three people |

## 4. How studios dress many period characters

- **Few bases, many variants:**
  - Warhorse's clothing system for KCD1 layers garments in up to 16 slots with no simulation. For variants they "REUSE BASE MESH" and "REUSE SKINNING, UVS, TRIANGLES, NORMALS", changing only material and textures [W11].
  - Epic's City Sample crowd mixes tops, bottoms, shoes and textures through one Blueprint [W5].
- **Simulate little:** shirts, trousers and fitted jackets are skinned; only hems and coat tails are simulated (PIPELINE-2026-09-30.md; Remedy and Naughty Dog, cited there). This matches his 30 September ruling.
- **The KCD2 bar is mostly surface:** worn, fuzzy wool and dirt in the textures, and true colours under the game's light (I). KCD2's realism started from scanning its cast in 2023 [W12]; how its garments were made is not published.
- **For us (I):**
  - One fitted base per garment type: the jumper, trousers, jeans, shirt or blouse, cardigan, jacket, skirt, boots and shoes.
  - Colour and wear set per person by script.
  - Townspeople later get the same bases, recoloured.

## 5. Recommended plan

**Step 1. The builder, today, about half a day (I).** Use script only: no new meshes, no Blender.
- **Ron:**
  - Sweater mid-grey, with pilling and fuzz up and sheen down.
  - Regular Jeans in charcoal, Secondary, Leather and Metal all set to the same charcoal. These are a stand-in for his work trousers, and still read as jeans close up.
  - His own boots, `ron_boots_skinned.fbx` (MH_RoccoP2, already in the game).
- **Sheila:**
  - Sweater in oatmeal, a stand-in for her cardigan.
  - Flats in brown.
  - Jeans off once her skirt is on (step 2).
- **Darren:**
  - Slim Jeans out; regular Jeans in pale stonewash blue, with stitching, leather and metal matched.
  - Casual Sneakers out; Boots in black, with lacing and sole dark.
- Render a test grid first to learn which slot on the regular Jeans is the stitching (MEMORY: test a grid first).

**Step 2. The builder, about one day (I).** Fit what the clothing session has handed over (L4), checking the version first:
- Sheila's cream blouse, pleated skirt (with its SkirtSim cone) and flesh tights. These were made on the **MH_LenaC1** body. Check that it is still the body under her S4 head before fitting: the bodies README marks the C1 export superseded, while the 30 September handover says her S4 head sits on C1's body.
- Darren's white T-shirt, belt and pager (MH_SamC5).
- When Jafar signs in to Fab, fetch the Oxfords for Sheila's flat brown lace-ups, and Chelsea Boots and Loafers for townsmen.

**Step 3. The clothing session, in this order, each 1 to 3 days (I; the jacket took days).** Each is bound panel by panel and handed back with the body version it fits.
1. **Ron's dark grey work trousers**, from MakeHuman CC0 Wool Pants (pants01) refitted on MH_RoccoP2: straight leg, about 54 cm round the hem, a half break on the boot.
2. **Sheila's beige cardigan**, from `model_cardigan.py`, the script that made her blouse and Darren's T-shirt, or by opening the front of Epic's Sweater (I).
3. **Darren's purple and teal shell-suit jacket** (SHELLSUIT-EDGES-2026-09-30.md).
4. **Ron's donkey jacket remake.** For the friends' build, Ron in a grey jumper, dark trousers and boots still reads 1990 (I).

**Judging each piece against the bar:**
- Use the game's own camera and exposure, day and night, at full size.
- Show front, side and back, walking, sitting and arms raised.
- At play distance (3 to 5 m):
  - **Silhouette:** straight or wide legs with a full seat and a break at the hem; nothing slim to the ankle.
  - **Palette:** the colours above; no stitching that shows against the cloth at 2 m; no trainers and no logos.
- At 1 m:
  - The knit shows stitches and pilling; wool shows fuzz and no sheen.
  - Denim shows wash variation; boots are scuffed.
- Compare side by side with production/reference/kcd2-town-*.jpg for wear and richness, and with Fryer and Report Digital for the period.
- Technical check: no body through the cloth, no stretched texture, and the LOD switch clean.
- Then the gate's blind reviewer, then his page as whole people.

## For Jafar (money, licence, canon, his hands)

- **His hands:** sign in to fab.com once, for Epic's free Oxfords, Chelsea Boots and Loafers. The allowlist and his standing permission cover the download, but Claude may not sign in.
- **Canon, one tap:** Darren's sheet says "scuffed white trainers"; his ruling says none. Options:
  - **A, black leather boots** (recommended for the friends' build).
  - B, plain white leather lace-up trainers of 1990 cut, never slip-ons.
  - C, black lace-up shoes.
- **No money is recommended.** The paid routes are listed only so he knows what exists. City Sample Crowds would need a licence ruling and is not recommended.

## Not found or not done

- No picture was judged in this session. Fab returned 403 to automatic reading. Epic's documentation pages did not render. The shared browser pane was being driven by another session, so it was left alone after one listing page.
- The look of Epic's Oxfords, Loafers and Chelsea Boots.
- Which of the regular Jeans' slots is the stitching.
- Whether the stitching is also baked into the jeans' base texture.
- A dated, text-described source for what fifty-year-old women in Hull wore in 1990. The Grattan and Littlewoods autumn/winter 1990 catalogues exist only as paid scans (cataloguecollections.co.uk).
- KCD2's own clothing pipeline.

## Sources (read 1 October 2026 unless stated)

Local:
- L1. UE 5.8 install: `Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Optional/Clothing` (only `OA_`/`WI_DefaultGarment`), and `Content/Python/examples/example_add_clothing.py`.
- L2. `F:/LedgerTools/mh-dress/Content/Fab/*/WI_*.uasset`: parameter names read as text.
- L3. `F:/LedgerTools/mh-dress/mh-cloth-materials.txt`, the builder's dump of 24 September 2026.
- L4. `F:/LedgerTools/garments/*/README.md`, 30 September 2026.
- Also the casting sheets, production/reference notes, the earlier clothing notes named above, DECISIONS.md (30 September), and ledger-v2/research/license-allowlist.md.

Web:
- W1. Fab, Epic Games seller page, search "MetaHuman" (browser, 24 items). https://www.fab.com/sellers/Epic%20Games?q=MetaHuman
- W2. Fab, "MetaHuman Sweater", published 7 April 2026. https://www.fab.com/listings/d401d47a-204f-4fde-aaec-c230042e7f60
- W3. nanana, "[UE5.8] Introduction to MetaHuman Creator", note.com, 22 June 2026. https://note.com/nanana_monokaki/n/n857937a2594e
- W4. Epic, "Python Scripting for MetaHuman Creator", undated (search summary only). https://dev.epicgames.com/documentation/metahuman/python-scripting-for-metahuman-creator
- W5. Fab, "City Sample Crowds", undated (search summary: UE-Only Content). https://www.fab.com/listings/903037e9-e1ac-4f41-96e8-1683c6fa7ad4
- W6. Epic Content EULA, undated. https://www.unrealengine.com/eula/content ; and forum thread "FAB UE-only content licensing", 2024. https://forums.unrealengine.com/t/fab-ue-only-content-licensing/2082870 (both search summaries)
- W7. outfit-maker.com, "A-Line Midi Skirt for MetaHuman 118", undated (read). https://www.outfit-maker.com/a-line-midi-skirt-for-metahuman-118-mhpkg/
- W8. Fab, "MetaHuman Women's Outfit Pack" (search summary). https://www.fab.com/listings/2f376410-f954-4e48-bcd3-d0fe8290e8ee
- W9. Epic forums, polycornStudio "Turtleneck & Blazer Outfit", 21 May 2026 (read). https://forums.unrealengine.com/t/polycornstudio-turtleneck-blazer-outfit-for-metahuman-resizable-blazer-pants-shoes/2723603
- W10. Fab, "Parametric Workwear Outfit Pack" (search summary). https://www.fab.com/listings/709a5877-3cfe-4af8-819f-94983d26c53d
- W11. Tomas Barak (Warhorse), "Adaptive Clothing System in Kingdom Come: Deliverance", GDC Europe 2015, transcript (read). https://archive.org/stream/GDCEU2015Barak/GDCEU2015-Barak_djvu.txt
- W12. 3d.sk blog, "Kingdom Come: Deliverance II", 28 January 2025 (search summary). https://blog.3d.sk/2025/01/28/kingdom-come-deliverance-ii-a-masterpiece-in-medieval-action-gaming/
- W13. Epic, "The Mutable Sample Project is now available", undated (search summary). https://www.unrealengine.com/news/the-mutable-sample-project-is-now-available
- W14. Worcestershire Archive & Archaeology Service, "Kays at Christmas, 1990", 19 December 2019 (read). https://www.explorethepast.co.uk/2019/12/kays-at-christmas-1990/
- W15. V&A O69860, cardigan, Marks and Spencer, 1989 (read through the V&A API). https://collections.vam.ac.uk/item/O69860/
- W16. V&A O138300, trousers, Farah, 1986 (read through the V&A API). https://collections.vam.ac.uk/item/O138300/
- W17. Wikipedia, "1990s in fashion", live page (read). https://en.wikipedia.org/wiki/1990s_in_fashion
- W18. Side Gallery, "Smith's Dock, North Shields" (Peter Fryer, 1990 to 1991), undated (search summary; the photographs were viewed by the clothing session on 29 September). https://sidegallery.co.uk/collection/smiths-dock-north-shields
- W19. Photography Chronicle, "Fish Town 1990-2020. The EU Years.", 2022 (read). https://photographychronicle.com/fish-town-1990-2020-the-eu-years/
- W20. It's Nice That, on Alec Gill's Hessle Road archive, May 2024 (search summary). https://www.itsnicethat.com/articles/alec-gill-the-alec-gill-hessle-road-photo-archive-photography-publication-project-140524
- W21. Wikipedia, "Ken Grant", live page (search summary). https://en.wikipedia.org/wiki/Ken_Grant
- W22. Fred Perry Subculture, "Shell Suits", undated (the page refused access; search summary only). https://www.fredperry.com/subculture/articles/shell-suits
