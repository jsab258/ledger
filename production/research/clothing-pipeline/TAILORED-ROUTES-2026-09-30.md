# Tailored clothes: the realistic routes (research note, 30 September 2026)

A separate helper, about thirty minutes, read-only; nothing downloaded or signed into. **D** documented (source number in brackets); **I** the helper's inference.

## In short

Cheapest first:

1. **Free, no decision needed: shoes only.** Epic's free resizable MetaHuman footwear on Fab (Oxfords, Loafers, Chelsea Boots, Flats, Boots) is Standard Licence, which is on the allowlist [2, 3] (D). Downloading needs Jafar signed in to Fab. Epic ships **no suits, blazers, coats, skirts or tailored trousers**, in Creator or on Fab [1, 2, 3] (D).
2. **Free, allowlisted: MakeHuman "suits01" (CC0)**, eight modelled suits, men's and women's, some double-breasted [9] (D): refit in Blender to our source bodies, then the builder's Outfit Asset step. Whether their detail passes the gate is unknown (I). Free patterns exist (FreeSewing, GarmentCode, MIT) [10, 11], but our failures were in draping, not drafting (I).
3. **Cheap purchase (Jafar's decision, money): resizable MetaHuman suits, coats, trench coats, leather jackets and women's suits on Fab**, about US$5 to 20 each, Standard Licence, allowlisted as "Fab purchases" [3] (D). Quality is uneven (one suit rated 1.7 of 5) [3] (D); period fit unverified, each through the gate (I).
4. **Paid tool (Jafar's decision, money): Marvelous Designer** at $39 a month or $280 a year. It is the source Epic documents for resizable outfits (USD with a simulation mesh) and the industry norm [5, 12, 14] (D). CLO costs $50 a month or $450 a year; Style3D's free tier is non-commercial [12] (D).
5. Whatever the route, studios drape in Marvelous and then finish folds and details by **sculpting by hand** [14] (D), so a ready-modelled mesh (routes 2 and 3) is the likeliest way to get lapels that read right (I). None of these fixes the seat when sitting by itself (I).

## (a) What MetaHuman ships, how it fits, and the licence

- Creator's wardrobe starts with grooms and "an outfit" [1] (D); on this PC's Unreal 5.8 install it is `DefaultGarment`, a shirt and shorts (D, local file names). Users found no clothing presets in 5.6 [7] (D).
- **Epic's free MetaHuman clothing on Fab** [2, 3] (D): the Techwear Outfit (jacket, trousers, shoes as one), Hoodie, Sweater, T-shirts, Crop Top, Jeans, Cargo Pants, Shorts, Yoga Pants; nine kinds of footwear (from the old web app, rebuilt as resizable outfits; Oxfords published 7 April 2026); and bodies for tailoring, the Clothing Construction Presets and Fashion Starter Kit [6] (D).
- **Fitting:** the Outfit Asset "associates your clothing with the body it was made for (source body)" and warps it to each target [5] (D); it holds several sizes and picks the closest, with a "Source Size Override" [3] (D). "The more source bodies you have, the higher the quality" [5] (D); realistic clothing warps most (RECHECK.md) (D). Since 5.7, Python drives the wardrobe [8] (D).
- **Licence:** MetaHuman is under the Unreal EULA since June 2025 [13] (D); seats free while revenue is "less than $1,000,000 USD" over 12 months, and never "to build or enhance any database or training" of AI [4] (D). Fab Standard Licence [3] (D): "Use the assets commercially or privately", "Modify and adjust", "Commercially distribute your Projects", never "Resell or redistribute the asset ... on a standalone basis"; players must be kept from extracting it; "Allows usage with AI: No" items may not train generative AI. Both are on the allowlist.

## (b) Importing our own garment

Yes: an FBX render mesh, a USD from Marvelous Designer or CLO with a simulation mesh, or a render mesh plus a hand-made simulation mesh [5] (D), modelled on source bodies exported from Creator [5] (D), no skinning needed (RECHECK.md) (D). So a free or bought suit that is not already a MetaHuman outfit is first refitted onto our source bodies in Blender (I); the builder already runs the rest. Resizing adapts to body shape, not to pose or tailoring quality (I).

## (c) Free or open sources, and alternatives to Marvelous Designer

| Source | Licence | On the allowlist? |
|---|---|---|
| MakeHuman suits01 [9] | CC0 (D) | Yes |
| GarmentCodeData patterns and meshes | CC BY 4.0 (D, earlier note) | No for 3D: Jafar's licence decision |
| GarmentCode [11] | MIT; its simulator is non-commercial (D, earlier note) | Tool: needs a decision record |
| FreeSewing Jaeger (sport coat), Carlton (long coat), Wahid (waistcoat) [10] | MIT (D, earlier note) | Already in use |
| Other sellers' free Fab suits and coats | Only low-poly or stylised items found (D; not exhaustive) | n/a |
| Blender, OpenSew-2 add-on | GPL; output is ours [12] (D) | Yes |
| Garment Tool, Simply Cloth add-ons | Paid, US$36 to 170 (D, earlier note) | Jafar's decision |
| CLO | $50 a month; Python only inside the open program [12, 15] (D) | Jafar's decision |
| Style3D | Free tier non-commercial [12] (D) | No |

## (d) How studios make suits and coats

Marvelous Designer for the base drape, ZBrush for folds, seams and the lapel's roll, retopology, then normal bakes [14] (D). Mafia: Definitive Edition's lead character artist credits "sculpting, lowmesh, and baking of clothing" [16] (D, search summary). Tailored jackets are mostly skinned, with cloth only on hems and coat tails (I).

## What could not be found

The shipped outfit's name in Epic's documentation; the look of any Fab suit (no images judged; the AI flag checked on three listings); suits01's polygon count and date; Style3D's own licence text; any published pipeline for 1990 suits. Epic's 5.7 release-notes address now redirects to 5.8.

## Sources

1. "Hair and Clothing Tools", Epic (MetaHuman docs), undated: https://dev.epicgames.com/documentation/metahuman/hair-and-clothing-tools (read in full)
2. MetaHuman Techwear Outfit and MetaHuman Vampire listings, Fab (published 3 June 2025, updated 12 November 2025; 17 June 2026): https://www.fab.com/listings/9e04c752-1979-4723-b78f-6d24afc532bc (read)
3. Fab: Epic Games seller search, "MetaHuman Oxfords" (7 April 2026), "Classic Close Suit - Metahuman" (23 October 2025), and searches for third-party suits and coats with prices, read 30 September 2026; Fab Standard License and EULA (last updated 1 October 2024): https://www.fab.com/eula (read)
4. Unreal Engine EULA, Epic, undated: https://www.unrealengine.com/eula/unreal (MetaHuman, seat and royalty clauses read)
5. "Creating Parametric Clothing", "Building an Outfit Asset", "Creating Your MetaHuman Characters", Epic, undated: https://dev.epicgames.com/documentation/metahuman/creating-your-metahuman-characters (read)
6. "MetaHuman Clothing Construction Presets, Set of 4" (3 June 2025) and "MetaHuman Fashion Kit" (21 April 2026), Epic forums: https://forums.unrealengine.com/t/epic-games-metahuman-clothing-construction-presets-set-of-4/2538920 (read)
7. "MetaHuman Clothing in 5.6", Epic forums, June 2025: https://forums.unrealengine.com/t/metahuman-clothing-in-in-5-6/2541589 (read)
8. "MetaHuman 5.7 is now available", metahuman.com, 15 December 2025: https://www.metahuman.com/releases/metahuman-5-7-is-now-available (read)
9. suits01 asset pack, MakeHuman Community, undated: https://static.makehumancommunity.org/assets/assetpacks/suits01.html (read)
10. FreeSewing designs (Jaeger, Carlton, Wahid), freesewing.eu, undated: https://freesewing.eu/docs/designs/ (search summary)
11. GarmentCode, GitHub (M. Korosteleva), MIT: https://github.com/maria-korosteleva/GarmentCode (search summary)
12. "3D Clothing Software Pricing and Licensing Models Compared", Marvelous Designer, modified 18 September 2026: https://www.marvelousdesigner.com/explore/guide/3d-clothing-software-pricing-licensing-models-compared (read; a competitor's page)
13. "You can now sell MetaHumans, or use them in Unity or Godot", CG Channel, 4 June 2025: https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/ (read)
14. "Workflows for Creating 3D Game Characters", 80.lv, 12 December 2018: https://80.lv/articles/001agt-004adk-workflows-for-creating-3d-game-characters (read); plus 80.lv and ArtStation breakdowns (search summaries)
15. CLO API Python docs, CLO Virtual Fashion, undated: https://developer.clo3d.com/python.html (search summary)
16. "Mafia Definitive Edition", Rohit Singh, ArtStation, undated: https://www.artstation.com/artwork/VgR0OP (search summary only; page refused)

Earlier notes relied on: RECHECK.md, MD-SCRIPTING-2026-09-29.md, SLEEVES-RECIPE-2026-09-29.md, character-pipeline/RESEARCH-2026-09-25.md.
