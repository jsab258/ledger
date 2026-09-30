# Free garment bases, collars, hems and pockets (30 September 2026)

A research helper was given the problem, not a theory, and worked read-only for about thirty minutes. **D** means documented, with a source number. **I** means the helper's inference. "Search summary" means only a search engine's summary was seen.

## In short

- **Jackets and coats:** no CC0 donkey jacket, pea coat, car coat, overcoat, raincoat, trench coat, bomber or anorak exists in MakeHuman's index. All 558 CC0 clothes in it were filtered [11] (D). The nearest CC0 bases:
  - Toigo's suit jackets (suits01), for tailored coats.
  - "Vietnam Military Jacket", a crude field jacket, as a work-jacket start.
  - "Working_suit", bib overalls [2][11][13].
  - A trench coat, winter coat, duffle coat, denim jacket and motorcycle jacket exist only as **CC-BY**, which is not on the allowlist [11][12].
- **Knitwear:** CC0 Fisherman Sweater and Turtle Neck (both Toigo). Cardigans are CC-BY only, apart from a weak CC0 women's hooded cardigan.
- **Shirts:** weak in CC0: a polo, a women's blouse, and a white shirt with no preview. The good men's shirts are CC-BY.
- **Trousers:** CC0 Wool Pants (Toigo), Bootcut Jeans (vitalemarco), Cargo Pants (Cortu), and the suits01 trousers.
- **Skirts:** CC0 Long Full Skirt, Tiered Skirt and Shift Dress (all Toigo).
- **Footwear:** CC0 Ankle Boots and Loafers (Toigo), and Male boots (culturalibre). Poly Haven's CC0 green Rubber Boots are also usable (D [23]).
- **Caps:** CC0 Newsboy cap and Low poly Beanie. The flat cap is CC-BY only.

**Method, in three lines** (D [30][32][34][36]; the specifics are I):

1. **Collar:** make it a separate piece, drafted flat: a stand of about 2.5 cm and a fall of about 4.5 cm or more. Crease a loop at the roll line, put one thickness loop round the edge, and crease the points. Lay it over the neckline; do not grow it from the body.
2. **Hem:** make it a band with one thickness loop and creased square front corners, so subdivision cannot round them. Make it heavy (a double layer) or skinned.
3. **Pockets:** use thin geometry or baked floaters. Copy the weights of the panel beneath, and never simulate them.

## (a) Free ready-made bases

The MakeHuman items below are CC0 and fitted to **hm08** [11][14].

- Page: `http://www.makehumancommunity.org/node/<n>`.
- Pack zip: `https://files.makehumancommunity.org/asset_packs/<pack>/<pack>_cc0.zip` [2]–[9].
- Items outside a pack have per-file links on their page.

| Garment | Item (author), node | Pack | Looks like |
|---|---|---|---|
| Suit jacket, trousers | Men's Suit 3, 1733; Double-breasted, 1740; Suit Tie and Jacket, 1265 (Toigo) | suits01, 40 MB | Plain navy suit; lapels read mostly from the texture (I, render [13]) |
| Women's suit | Female Suit, 1324; Female Suit 2, 1739; DB Female Suit, 1742 (Toigo) | suits01 | Jacket and bottoms, with normal maps |
| Work jacket (start) | Vietnam Military Jacket, 2694 (MrGreaterThan, 2020) | none | Olive field jacket, small collar, pockets in the texture only [13] |
| Overalls | Working_suit, 593 (Marco_105, 2017) | none | Blue denim bib overalls |
| Men's work and casual | male_worksuit01, male_casualsuit01–06 (MakeHuman) | system assets, 267 MB | Not viewed |
| Jumper | Fisherman Sweater, 1187; Turtle Neck, 1104 (Toigo) | shirts01 (sweater) | Aran-style knit made by its normal map; plain turtleneck |
| Cardigan | hooded_cardigan, 674 (RadicalToast) | none | Purple women's hooded cardigan; weak |
| Shirt or blouse | Male Polo Shirt, 2909; Preppy blouse, 1158; BTH Shirt_White, 3165 | shirts01 (polo) | Basic polo; women's blouse; the white shirt has no preview |
| Trousers and jeans | Wool Pants, 1194; Bootcut Jeans, 807; Cargo Pants, 2798 | pants01 (wool, cargo) | Plain wool trousers; men's bootcut jeans; green cargos |
| Skirt or dress | Long Full Skirt, 1727; Tiered Skirt, 1641; Shift Dress, 1724 (Toigo) | skirts01, dress01 | Draped with Blender's cloth simulation |
| Shoes and boots | Ankle Boots M/F, 1743/1738; Loafers M/F, 1732/1741 (Toigo); Male boots, 2548 | shoes01, 79 MB (not the loafers) | Normal maps; the loafers come with socks |
| Wellies | Rubber Boots, Poly Haven, 9 Jun 2026 | polyhaven.com | Green, 35,000 polygons. Has an "embossed logo": **check it is not a real brand** |
| Caps | Newsboy cap, 78 (jujube); Low poly Beanie, 232 | hats01 (cap) | Crude; "clips through the hair models" |

**Elsewhere (D):**

- BlenderKit has 58 free CC0 clothing items; only cargo pants, sweat pants and scanned shoes are relevant [24]. Its "Royalty Free" licence is not allowlisted [25].
- Blender's Human Base Meshes have no clothes [26].
- Quaternius and OpenGameArt are stylised [27][28].
- A Sketchfab kit is titled CC0, but its licence field is unclear [29].

**CC-BY only, needing Jafar's ruling** [10][11]:

- Elvaerwyn: trench coat, flat cap, jeans, cardigan, coveralls.
- Mindfront: knitted sweaters, trousers, Oxford shoes.
- punkduck: winter coat, denim jacket, motorcycle jacket, jeans.

## (b) Collars, hems and pockets

**Collar**

- A two-piece collar is a stand and a fall, joined at the roll line. A tailored collar has a 2.5 cm stand and a 4.5 cm fall (D [34][35], search summary).
- Marvelous Designer folds a collar on an internal line set to a fold angle (D [37], search summary).
- Game artists model thickness only at visible rims, such as collars and cuffs (D [32], search summary). "Thickness is always a loop" (D [30]).
- I: the stand is 2 loops and the fall 3–4, with a crease loop at the roll line. The points are creased and carry the neck and chest weights. The "crew neck with a cape" came from growing the collar out of the body.

**Hem**

- Subdivision rounds uncreased corners (D [36], search summary).
- Remedy skinned the upper jacket and simulated the lower part (D [31]).
- I: model a 3–4 cm band with a creased bottom edge and 90° front corners. Make it heavier, or skinned.

**Pockets**

- Remedy kept the pocket silhouette in a render mesh separate from the simulated one (D [31]).
- Floaters baked into the normal map are common (D [32], search summary).
- Weights come by Data Transfer, "nearest face interpolated" (D [36], search summary).
- I: copy the panel's weights, never simulate, and crease the top edge.

## (c) Fitting a MakeHuman garment to another body

**hm08 itself**

- **It is CC0:** "explicitly released as CC0 in september 2020" (D [16][15]). Get `makehuman/data/3dobjs/base.obj` from GitHub `makehumancommunity/makehuman` [16].
- Body vertices 0–13,379, helpers to 19,157 (D [17]). Units are decimetres, 16.8 dm tall (D [18]).
- Pose: an A-pose, arms about 45° down (I, from thumbnails). MPFB can apply "a pose as rest pose, while keeping clothes and body part in sync" (D [21]).

**How clothes attach:** each .mhclo vertex is three hm08 vertices, barycentric weights, and an offset scaled by distances between named vertex pairs (D [19][14]).

**MPFB refits only to hm08** (D [20]). No MakeHuman-to-MetaHuman route is documented.

**I: a free scripted route.**

1. Shape and pose hm08 toward the MetaHuman in MPFB.
2. Register it non-rigidly onto the MetaHuman body with trimesh `nricp_amberg` [38]. Its licence is unchecked, and a new tool needs a decision record [39].
3. Re-evaluate the .mhclo lines on the moved hm08, or use Surface Deform plus a shape key [36].
4. Copy the weights from the MetaHuman.

Heavy bodies distort pockets (D [12]).

**Licence trap:** a 2017 mirror copy of male_worksuit01 says "AGPLv3" (D [14]). Use the CC0 pack copy and check its headers (I).

## Not found

- No breakdown of a lapelless work-jacket or pea-coat collar at game resolution.
- The Polycount threads are behind Cloudflare, so only their search summaries were seen.
- No documented hm08 pose.
- The system-asset suits were not seen.
- Kenney was not checked.
- Sketchfab was not searched item by item.

## Sources (all read 30 September 2026)

1. MakeHuman Community, "Asset Packs", undated, https://static.makehumancommunity.org/assets/assetpacks.html (read)
2. Same site, "suits01", undated, …/assets/assetpacks/suits01.html (read)
3. Same, "shirts01" (read)
4. Same, "pants01" (read)
5. Same, "shoes01" (read)
6. Same, "skirts01" (read)
7. Same, "hats01" (read)
8. Same, "dress01" (read)
9. Same, "makehuman_system_assets" (read)
10. Same, the CC-BY packs "shirts02", "pants02", "shoes03" and "hats03" (read)
11. MakeHuman asset index, assets.json, latest entry 29 Sep 2026, http://www.makehumancommunity.org/sites/default/files/assets.json (read in full and filtered: 1,362 clothes, 558 CC0, 804 CC-BY)
12. "Elvs Male Trench Coat1", 8 Apr 2019, http://www.makehumancommunity.org/clothes/elvs_male_trench_coat1.html (read)
13. Renders of Vietnam Military Jacket, Working_suit and Men's Suit 3, files.makehumancommunity.org (viewed)
14. male_worksuit01 folder and .mhclo header, files dated 5 Feb 2017, https://download.tuxfamily.org/makehuman/assets/1.1/base/clothes/male_worksuit01/ (read)
15. MakeHuman LICENSE.md, GitHub, 2020, https://github.com/makehumancommunity/makehuman/blob/master/LICENSE.md (read)
16. base.obj header, GitHub, 2020, https://raw.githubusercontent.com/makehumancommunity/makehuman/master/makehuman/data/3dobjs/base.obj (read)
17. "Basemesh", undated, https://static.makehumancommunity.org/about/concepts/basemesh.html (read)
18. "Exports and file formats", undated, https://static.makehumancommunity.org/makehuman/docs/exports_and_file_formats.html (read)
19. "File formats and extensions", undated, https://static.makehumancommunity.org/oldsite/documentation/file_formats_and_extensions.html (read)
20. MPFB docs, "Clothes, hair and body parts" and "Rigging mesh assets", undated, static.makehumancommunity.org/mpfb/docs/ (read)
21. "MPFB 2.0-alpha2", 4 Sep 2022, https://static.makehumancommunity.org/mpfb/releases/release_20a2.html (read)
22. "Are MakeHuman files free?", 17 Oct 2017, https://static.makehumancommunity.org/makehuman/faq/are_makehuman_files_free.html (read)
23. Poly Haven API, rubber_boots, fishermans_hat and garden_gloves_01, https://api.polyhaven.com/info/rubber_boots (read)
24. BlenderKit search API, free CC0 clothing, https://www.blenderkit.com/api/v1/search/?query=category_subtree:clothing+is_free:true+license:cc_zero (read)
25. Blendkit, "Licenses", undated, https://www.blendkit.com/docs/licenses/ (read)
26. CG Channel, "Download Blender Studio's free Human Base Meshes", June 2023, https://www.cgchannel.com/2023/06/download-blender-studios-free-human-base-meshes/ (search summary)
27. Quaternius, "Modular Character Outfits – Fantasy", undated, https://quaternius.com/packs/modularcharacteroutfitsfantasy.html (search summary)
28. OpenGameArt, "CC0 – 3D Humans / Players", undated, https://opengameart.org/content/cc0-3d-humans-players (search summary)
29. Sketchfab, "Clothing_And_Character_Kit 1.0 FBX (CC0)", 17 Oct 2021, https://sketchfab.com/3d-models/clothing-and-character-kit-10-fbx-cc0-77da31c1350343f9ae2f9ef4cb228b8a (read; licence field unclear)
30. Thunder Cloud Studio (Dzung Phung Dinh), "Topology for Low Poly Game Characters", 9 Sep 2024, https://thundercloud-studio.com/article/topology-for-low-poly-game-characters/ (read)
31. Henrik Enqvist, "The Secrets of Cloth Simulation in Alan Wake", Game Developer, 29 Apr 2010, https://www.gamedeveloper.com/programming/the-secrets-of-cloth-simulation-in-i-alan-wake-i- (read)
32. Polycount threads 225844 (coat collar), 184426 (retopologising clothes for rigging), 234075 (29 Sep 2023) and 110637 (floating geometry), https://polycount.com/discussion/… (search summaries; blocked by Cloudflare)
33. Blender Artists, "Jacket modeling", 6–7 Sep 2025, https://blenderartists.org/t/jacket-modeling/1609968 (read)
34. The London Pattern Cutter, "How To Draft A Tailored Collar And Lapel", 2026, https://thelondonpatterncutter.co.uk/tailored-collar-draft/ (search summary)
35. Müller & Sohn, "Pattern construction for collar with stand", undated, https://www.muellerundsohn.com/en/allgemein/pattern-construction-for-collar-with-stand/ (search summary)
36. Blender 5.2 Manual: Subdivision Surface (edge crease), Surface Deform and Data Transfer, https://docs.blender.org/manual/en/latest/ (search summaries)
37. Marvelous Designer, "Fold Pattern", undated, https://support.marvelousdesigner.com/hc/en-us/articles/47358354961049-Fold-Pattern (search summary)
38. trimesh, "nricp" docs, https://github.com/mikedh/trimesh/blob/main/docs/content/nricp.md (search summary)
39. LEDGER licence allowlist, ledger-v2/research/license-allowlist.md (read)
