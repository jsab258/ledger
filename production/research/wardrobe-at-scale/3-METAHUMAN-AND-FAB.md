# Epic's 5.8 clothing, what Fab sells, and other ready sources (research note, 1 October 2026)

A separate helper was given the problem, not a theory, and spent about thirty minutes, reading only. **D** means documented, with the source number. **I** means its inference. Saved by the cloud session; its checks are in SUMMARY.md.

**Most of the sources were blocked.** The network proxy refused fab.com, forums.unrealengine.com, artstation.com, cgtrader.com, outfit-maker.com, reallusion.com, metahuman.com, unrealengine.com, 80.lv and cgchannel.com. Epic's documentation pages opened, some only in part. So almost every marketplace fact below comes from a **search-engine summary**: no images, ratings or "Created with AI" flags were seen, and most prices are missing.

## In short

1. **Nobody sells 1990 northern working clothes ready-made.** No MetaHuman donkey jacket, car coat, anorak or cagoule, shell suit, headscarf, flat cap, or "1980s", "1990s", "British" or "working class" pack was found (D, searches [S]).
2. **Suits, blazers, overcoats, trench coats, raincoats, a cardigan, an A-line midi skirt and bomber jackets do exist** as resizable MetaHuman outfits on Fab, most at US$20 to 35 and one at $60; none has had its look checked (D [S]; looks unseen).
3. **The leads worth putting through the gate** (I): CGTailor's *Parametric Workwear Outfit Pack* (worn and clean versions); suits from NDart, Husky Studio or CGTailor; outfit-maker's *Coat 53* (wool overcoat), *Trench 113*, *A-Line Midi Skirt 118* and *Beige Casual Cardigan 48*; a loose boxy bomber from polypixel.archive.
4. **Unreal 5.8 adds a crowd system** that mixes garments by slot and tints them per person. It is Experimental (D [5–7]), but it is the natural home for a crowd of 200 to 500 (I).
5. **Two 5.8 faults matter for bought clothing:** packages can arrive with their materials missing (D [9]), and a resizable wardrobe item can lose its cloth simulation (D [10], forum). Buy one item and test it on the six bodies before buying more (I).
6. **A ruling to check:** DECISIONS.md, 30 September, rules suits and coats from MakeHuman's free pieces, "not Fab's paid ones, and no Marvelous Designer". The brief of 1 October lets a month of a tool in; whether paid Fab garments are now allowed is Jafar's (I).

## 1. Epic's MetaHuman clothing in 5.7 and 5.8

**The format**
- Fab sells two kinds of MetaHuman clothing: **Outfit Clothing**, made with the Chaos Outfit asset, which "may be resized to automatically fit certain MetaHuman body shapes", and **Skeletal Clothing**, "created for a specific MetaHuman body shape(s) that is not able to be resized automatically" (D [1]).
- Both come as `.mhpkg`, which MetaHuman Manager verifies and packages (D [1]).

**How one garment fits many bodies**
- An outfit holds several source sizes; the system "automatically selects the size that fits the best" from the body's measurements, and a *Source Size Override* lets you choose (D [2]).
- Epic's warning: "In some cases, the source body and target body are too different, which can cause warping. This is especially the case with more realistic and detailed (not stylized or simplified) clothing." Epic encourages "multiple outfits for multiple source bodies" (D [3]).
- The Clothing Construction Presets, Set of 4, are the bodies Epic recommends for a four-size garment (D [4], search summary).
- From the project's earlier notes: the Outfit Asset is Beta in 5.8 while the Cloth Asset is production-ready; the import route is StaticMeshImport, then TransferSkinWeights, then the terminal node; resizing uses 1,000 to 2,500 interpolation points; Marvelous Designer or CLO send a render and a sim mesh by USD; Epic's free set has four LODs (D, clothing-pipeline/PIPELINE-2026-09-30.md and plain-1990-clothes/NOTE.md).
- **No published limit on quality was found**, beyond the warping warning (I).

**New in 5.8: crowds**
- The MetaHuman Crowd plugin and its *Collections* are **Experimental** ("use caution when shipping with it") (D [5][6]).
- The crowd pipeline has slots for **Top Garment, Bottom Garment and Shoes**, each taking "ChaosOutfitAsset or SkeletalMesh" (D [6]).
- Variety comes from "Instance Parameters such as hair color and clothing tint" (D [6][7]).
- Near the camera people are full actors; further away instanced meshes; beyond a set distance they stop rendering (D [7]).
- Epic's *MetaHuman Crowd Sample* on Fab is free (D [8], search summary); its clothing and licence were not verified. *City Sample Crowds* is "UE-Only Content", tops, bottoms and shoes on six body types (D [8], search summary): modern clothing.

**Known 5.8 faults**
- Epic's known issues, verbatim: a character "with clothing or grooms sourced outside the MetaHuman plugin's bundled content… packaged via MetaHuman Manager, the resulting `.mhpkg` file is missing parent materials. Clothing renders with the engine's default world-grid texture"; and verifying one wardrobe item "incorrectly flags unrelated WardrobeItems" (D [9]).
- Forum reports (search summaries only): a resizable item "converts back to static" when made a wardrobe item, losing its cloth (D [10]); open-blazer and sweater cuffs stretch "to the origin point" on the UEOptimized Medium skeleton (D [11]); custom items built through the crowd pipeline do not display (D [12]).
- The 5.8 release notes fix wardrobe items getting stuck or stale, and let you package only selected wardrobe items (D [13]).

**Epic's authoring kits**
- The *Fashion Starter Kit* is a showcase project with a runway and a turntable, for UE 5.7+; it does not make garments (D [14]).
- The *MetaHuman Fashion Kit* (April 2026) is one MetaHuman preset proportioned for fashion plus 60 seconds of motion capture (D [15], search summary).
- Epic covers only the Unreal side, with no guide to building garments in a modelling program (D [3]).

**Colour.** Every wardrobe item exposes colour slots, settable from Python (D, plain-1990-clothes/NOTE.md). Third-party items advertise per-part colour and roughness (Husky Studio) or "a custom shader… for creating any colorway" (polypixel) (D [S]).

## 2. Fab listings that could read as 1990

All resizable `.mhpkg` outfits unless marked fixed; all from search summaries; none seen.

| Listing | Seller | Price | How it might read for 1990 (I) |
|---|---|---|---|
| **Parametric Workwear Outfit Pack** | CGTailor | not found | Male and female; "Worn & weathered" and "Clean" materials; jacket, shirt, overall. **Best lead for dockers and workmen** |
| Parametric Formal Outfit for MetaHuman Vol 01–05, Pack Vol 01; Female Formal Pack Vol 01 | CGTailor | $19.99–34.99 | Modern formal suits; might pass recoloured |
| 1920s Gangsters & Police; 1920s British Police; Police Uniform; Prisoner; FBI Agents | CGTailor | not found | Wrong period |
| **Business Suit Outfit**; Business Blazer Jacket; Dress Trousers; Dress Shirt; Turtleneck Sweater; **Classic Pencil Skirt**; Mary Jane Flats | NDart | not found | Clean and realistic by its own account; plausible office and Sunday suits |
| **Suit Jacket – 51** (jacket, tie, shirt); Business Outfit 48; Business pants 45 | Husky Studio | not found | Per-part colour and roughness |
| Turtleneck & Blazer Outfit | polycornStudio | not found | Blazer, trousers, shoes |
| Formal Classic Suit – Resizable Outfit | Andi J | $59.99 | Fit unseen |
| Business Formal Outfit v2; Female Formal Outfit v3 | not found | not found | 90,758 vertices at LOD0; "Tech-Noir", likely too modern |
| **Coat for MetaHuman 53** (brown wool overcoat, notch lapels); **Belted Trench Coat 113**; Hooded Long Raincoat 115; **A-Line Midi Skirt 118**; Pleated Mini Skirt 116; Waistcoat 41; **Beige Casual Cardigan 48**; Leather Jackets 60 and 81; Jacket 46 (grey zip bomber); Military Winter Jacket 101 | Outfit-maker, also on Fab ("… for MetaHuman, Rigged 3D Model NN") | own site €13–19 personal, €111–179 professional; Fab price not found | `.mhpkg` and FBX, 4K textures. **The widest range of period-plausible garments.** A mass-numbered catalogue: check Fab's AI flag on each (I) |
| MetaHuman Male / Women's / Western Outfit Packs | Mesh Atelier | male pack $24.99 | **Fixed** to one body; modern |
| Metahuman Male Dresswear Clothing Pack (3 suits, 6 waistcoats, 4 shirts, 3 trousers) | not found | not found | Two source bodies only; heavy builds would warp (I) |
| Clothing Basics Pack; Metahuman Basic Clothing Pack | not found | $29.99; $19.99 | **Fixed** to one or two bodies |
| MetaWardrobe, Season 2 | Relentless Games | $27.99; $29.99 | Large modern library |
| **Bomber Jacket** (loose, boxy, 4 LODs, colourway shader, UE 5.6+); MetaHuman Bomber Outfit | polypixel.archive; Lespol | not found | Young men's blouson; possibly a Harrington base (I) |
| Realistic Worn Shirt & Pants; Lumberjack Logger Heavy-Duty Workwear | not found | not found | Worn workwear |
| Garment Tool for MetaHuman (v3.2.0, UE 5.8) | not found | not found | A tool: turns a static mesh into a **fixed** skeletal garment per body |

**Licence and AI.** All under the Fab Standard Licence, on the allowlist (D, clothing-pipeline/TAILORED-ROUTES-2026-09-30.md). Since January 2025 sellers who used AI must set the "Created with AI" flag (D [16]); check it on each listing before buying (I). Where a seller also sells elsewhere, buy the Fab copy so the Standard Licence applies (I).

## 3. Other sources

- **Reallusion (Character Creator):** its content licence changed on 1 August 2025; the Extended Licence was folded into the Standard, which now allows export to Unreal and use "in games or XR projects at scale" (D [17], search summary). No direct route to a resizable MetaHuman outfit: the community goes through MetaTailor or exports an FBX paired with a matching MetaHuman source body (D [18], search summary). Not on the allowlist.
- **Daz 3D:** game use needs an **Interactive License** per product, about $10 to 50 as an add-on (D [19], forum posts, loosely dated). Converting Daz clothes to MetaHumans is reported hard. Not on the allowlist.
- **MetaTailor:** fits clothing from Daz and other sources onto MetaHumans; its Unreal bridge left beta with 2.5 (February 2026); rental only, Pro $35 a month or $336 a year (D [20], search summary). A "month of a tool" candidate (I), but whether exports may be used after cancelling is **unverified**, and it supplies no 1990 garments.
- **Renderpeople and ActorCore:** scanned people whose clothing is baked into the body (I; [21] confirms only the scanned catalogue).
- **CGTrader and TurboSquid:** formal outfit packs rigged to MetaHuman and a "3D Suit with Metahuman Rig" (made in Marvelous Designer) are listed (D [S]); royalty-free game use (I, unverified); mostly fixed-size; not on the allowlist.
- **vr4d store:** a MetaHuman bomber jacket and jeans, its own licence (D [S]).

## The helper's recommendation (I)

1. Buy one cheap item first (outfit-maker *Coat 53* or CGTailor *Workwear*, through Fab); import it into 5.8 and check that its materials survive packaging, that it fits the heavy and slim builds without warping, that its cuffs do not stretch, and that it still works as a wardrobe item.
2. If it passes, put the shortlist through the gate against the Hook sheet and the KCD2 frames.
3. Keep making the donkey jacket, anorak, shell suit, flat cap, headscarf and car coat; a bought blazer or bomber may serve as a base, since the Standard Licence allows "Modify and adjust".
4. For the crowd: about 15 to 20 base garments in 5.8 Collections, with tint variety; test the Experimental path early.

## Sources

1. "MetaHumans on Fab", Epic, undated (5.8). https://dev.epicgames.com/documentation/metahuman/metahumans-on-fab (read)
2. "Tailoring Your Own Wardrobe Items", Epic, undated. https://dev.epicgames.com/documentation/metahuman/tailoring-your-own-wardrobe-items (read)
3. "Getting Started for creating Parametric Clothing in MetaHuman", Epic, undated. https://dev.epicgames.com/documentation/metahuman/getting-started-for-creating-parametric-clothing-in-metahuman (read, partial)
4. "MetaHuman Clothing Construction Presets, Set of 4", Epic on Fab. https://www.fab.com/listings/3c0c4df1-ce96-44cf-8a30-c47d744d2a0c (search summary)
5. "MetaHuman Collections in Unreal Engine", Epic, 5.8, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-collections-in-unreal-engine (read)
6. "Create MetaHuman Crowds in Unreal Engine", Epic, undated. https://dev.epicgames.com/documentation/metahuman/create-metahuman-crowds-in-unreal-engine (read)
7. "MetaHuman Crowd Sample Tutorial", Epic, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-crowd-sample-tutorial (read)
8. "MetaHuman Crowd Sample" https://www.fab.com/listings/5f481d73-afb1-4d94-ba6e-7cabf5d296fa and "City Sample Crowds" https://www.fab.com/listings/903037e9-e1ac-4f41-96e8-1683c6fa7ad4 (search summaries)
9. "MetaHuman Known Issues 5.8", Epic, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-known-issues-5-8-in-unreal-engine (read)
10. "Metahuman Parametric Wardrobe asset missing cloth simulation 5.8", Epic forums, 2026 (search summary)
11. "Certain MetaHuman clothing assets stretching", Epic forums, 2026 (search summary)
12. "Unable to get custom wardrobe items displaying properly in Metahuman Collection (5.8)", Epic forums, 2026 (search summary)
13. "MetaHuman 5.8 Release Notes", Epic, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine (read)
14. "MetaHuman Fashion Starter Kit", Epic, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-fashion-starter-kit (read)
15. "Epic Games – MetaHuman Fashion Kit", Epic forums, April 2026 (search summary)
16. "NoAI meta tags and Created with AI self-declaration", Fab support, January 2025. https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration (search summary)
17. "Reallusion Content EULA Updated (Effective August 1st, 2025)", Reallusion forum, July 2025 (search summary)
18. "Characters for Unreal: Character Creator 5 Meets MetaHuman", Reallusion Magazine, 6 February 2026, and "RL clothes to UE MetaHuman Parametric Clothing?", Reallusion forum (search summaries)
19. "Interactive License?", Daz 3D forums, various dates (search summary)
20. "MetaTailor 2.5 is out…", CG Channel, February 2026 (search summary)
21. Renderpeople home page, undated. https://renderpeople.com/ (search summary)

[S]: the Fab, outfit-maker and forum product listings named in section 2, found 1 October 2026 through search summaries only. Examples: CGTailor seller page https://www.fab.com/sellers/CGTailor; Workwear Pack https://www.fab.com/listings/709a5877-3cfe-4af8-819f-94983d26c53d; Coat 53 https://www.fab.com/listings/a95700e5-8a2d-48d6-843f-c6d673e56d65; Trench 113 https://www.fab.com/listings/f385f551-056f-4848-8e36-8f661c58839b.

## What could not be verified

- No Fab page opened (the proxy blocks it): for every listing the images, ratings, dates, the AI flag and most prices are missing, including outfit-maker's Fab prices.
- What is in CGTailor's Workwear Pack, and whether any of it resembles a donkey jacket.
- The full text of the forum fault threads, and whether Epic has fixed them.
- The full text of Epic's 5.8 "Building an Outfit Asset" page (behind Cloudflare).
- How many source bodies each third-party outfit carries.
- What clothing the MetaHuman Crowd Sample contains, and its licence.
- MetaTailor's terms for exports after cancelling, and Reallusion's licence text itself.
- Whether any listed garment would pass the KCD2 bar: nothing was seen.
