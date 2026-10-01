# Dressing a town: how studios build a wardrobe at scale (research note, 1 October 2026)

A separate helper was given the problem, not a theory, and spent about thirty minutes, reading only. **D** means documented (source number in brackets). **I** means its inference. Most studio pages were blocked to the fetch tool, so many sources are search summaries only (marked SUMMARY). It builds on production/research/casting/notes/crowd.md (24 September) and does not repeat it. Saved by the cloud session.

## In short

1. **Nobody dresses a crowd one garment at a time.** Every system examined works the same way: a few base garments in fixed slots, each fitted to every body type, multiplied mainly by material and colour, combined by a recipe for each kind of person (D [3][6][9][10][12][14]).
2. **Variety comes mainly from materials, not new meshes:** texture variants, masked fabric layers and tint settings (D [3][9][15][17]; table below).
3. **Period games dress people by recipe, not at random.** RDR2 gives each type of townsperson a few authored outfit presets [10]; KCD gives each NPC its own clothing preset [14]; Watch Dogs: Legion picks outfits from the person's background [29] (D).
4. **Period accuracy comes from a costume process, not from memory.** L.A. Noire hired a film costume designer, gathered real fabrics, scanned costumes and "shader swapped" them to dress the population [21] (D); KCD and Assassin's Creed Unity used historians [12][28] (D).
5. **Tailored pieces are made once, from patterns, then reused.** Mafia: The Old Country, a period game built on MetaHuman, lists Marvelous Designer, ZBrush, MetaHuman and Unreal in its character pipeline, and one character's outfits "share elements" [25] (D). For LEDGER the jacket is a base-garment problem: solve it once per silhouette, then vary it (I).

## 1. How a kit is laid out

- **Slots.** GTA V has 12 component slots (torso, legs, shoes, undershirt, tops and so on) and 5 prop slots (hats, glasses, ear pieces, watches, bangles); each slot holds several meshes, each mesh several textures (D [9]). KCD has 16 slots that layer, with up to four items on the chest (D [12]). RDR2 builds people from body components plus outfit presets per character model, with overlays and colour palettes as separate data (D [10][11]).
- **Bodies.** City Sample has 2 sexes × 3 weights = 6 bodies, and every garment is fitted to each one; each character is stored as a set of numbers: body, head, outfit, outfit material, hair, hair colour, accessory (D [2][3]).
- **Unreal 5.8 now does the same, but Experimental.** MetaHuman Collections have Top, Bottom and Shoes slots, which take a Chaos Outfit or a skeletal mesh; a slot can allow "multiple simultaneous selections … to wear multiple clothing items at once"; each character can override "hair color or material tints"; a Crowd Sample is on Fab (D [5][6][7]).
- **Layering needs a rule.** Cyberpunk's engine pushes the lower garment inwards so layers do not poke through ("Garment Support") (D [16]). Without that, recipes must allow only layer combinations that have been tested (I).

## 2. How variation is driven

| Method | Example | Source |
|---|---|---|
| Swap the mesh | GTA's swappable meshes; City Sample's tops, bottoms and shoes | D [9][3] |
| Texture or colour per mesh | Hitman's texture swaps; City Sample's pattern and colour; Unreal 5.8's "clothing tint" [5][6] | D [17][3] |
| Masked layers over a shared fabric library | Cyberpunk: up to 20 masks blend library surfaces, each with its own colour and tiling | D [15] |
| The same in Unreal | Material Layers; "All your layers are rendered simultaneously", so they cost more to draw | D [8] |
| Scanned cloth | The Order: 1886 built its own textile scanner and a library of base materials | D [27] |
| Wear and dirt | KCD's clothes grow "worn, dirty, or bloody"; Cyberpunk paints wear into greyscale masks | D [12][15] |
| Accessories | Accessories make "each instance unique" [20]; head accessories and the top's texture hide repeats as well as face texture does [19] | D |

## 3. How many pieces

- **City Sample:** women 27 tops, 15 bottoms, 9 pairs of shoes; men 36 tops, 18 bottoms, 6 pairs of shoes: 111 pieces, each fitted to six bodies, for a city of 35,000 simulated people (D [3]; the 35,000 via crowd.md). Heads: 12 in one breakdown, 18 per sex in another, unresolved.
- **RDR2 townspeople:** a modders' dump of the game data lists 2 to 13 outfit presets per type of townsperson (Valentine townsfolk 13, Blackwater 2, one worker type 4), more than 900 character models and more than 3,000 presets in all (D [10]; approximate). Rockstar also cast 1,200 actors (D [23]).
- **What people notice:** a repeated outfit before a repeated face; two different men in suits, or two in checked shirts, were taken for copies (D [18]). Varying the colours doubled the time it took to find a copy (D [18]). Eyes go to the head and upper body, rarely to the legs (D [19]).
- **No published figure** says how many tops a crowd needs before players notice repeats.

## 4. How period games got it right

- **L.A. Noire (1947):** a film costume designer, Wendy Cork, and real fabrics of the period; actors photographed in costume, principal costumes scanned; Team Bondi "scanned and photographed a massive variety of clothes so they could have 3D models to shader swap and merge together to dress the entire population" (D [21]). Behind it: 180,000 photographs, more than 1,000 newspapers and 140 production bibles (D [22]).
- **KCD and KCD2:** historians, universities and museums, and a historical consultant who said "It's a game, it's not an open-air museum" (D [12][13]).
- **Assassin's Creed Unity:** historian Laurent Turcot used paintings and engravings to show how the crowd looked (D [28]).
- **Mafia: The Old Country:** rare photographs, written accounts and trips to Sicily (D [24]). **Mafia: Definitive Edition:** films and old newspapers (D [26]).
- **RDR2:** no primary source found on its costume research.
- **What carries over (I):** a costume plan for each principal from dated photographs and catalogues (the dress-and-bearing notes already start this); a small library of fabrics (melton wool, polyester slacks cloth, denim, nylon shell, knit, tweed, gaberdine); scanning real cloth samples on a flatbed scanner, the cheap version of The Order's scanner (buying samples costs money: Jafar's decision).

## 5. City Sample and the Matrix crowd: reusable?

- **Contents:** heads and bodies made from MetaHumans, "a wardrobe of tops, bottoms, and shoes fitted to six body types", and a Blueprint that mixes and matches them (D [2]); garment materials built for "complex variation in fabric and pattern" (D [4]).
- **Licence:** "licensed for use only with Unreal Engine-based products" (D [2], summary only). The allowlist's Unreal-only entry covers Epic's animation only (D [30]); any use of the crowd assets needs Jafar's ruling.
- **Period:** the clothes are 2020s (D, crowd.md). Only the method carries over: characters as recipes, garments fitted to each body, material variants; Unreal 5.8's Collections now do the same (I).

## 6. Short answer: how many base garments (I)

From City Sample's 111 pieces, the finding that outfits are noticed first, and RDR2's presets:

- **One street (14 principals, about 30 regulars): about 40 base garments, each fitted to the 6 builds.**
  - Men's outerwear, 6: donkey jacket, anorak, suit jacket, cord or sports jacket, overcoat or car coat, shell-suit jacket or blouson.
  - Women's outerwear, 4: wool coat, belted mac, quilted anorak, skirt-suit jacket.
  - Shirts and knitwear: 8.
  - Trousers and skirts, 7: work trousers, slacks, jeans, suit trousers, cords, skirt, shell-suit bottoms.
  - Footwear, 6: work boots, lace-ups, trainers, court shoes, flats, wellingtons.
  - Head and small items, about 8: flat cap, woolly hat, headscarf, rain hood, glasses, clerical collar, scarf, handbag.
- **On top:** 4 to 8 fabric-and-colour variants of each from a muted 1990 palette, plus wear and dirt; 8 to 10 one-off pieces for principals (the solicitor's Chesterfield, the widow's fur-collared coat); 1 to 3 written outfits per principal; one fixed outfit per regular, so the street can recognise them.
- **The town (200 to 500 people on screen): about 60 to 70 base garments**, adding work clothes (fish-market whites, overalls, shop tabards, the cab driver's car coat, young men's sportswear); most variety in the upper body and outer layer, where eyes go; 20 to 40 outfit recipes per body; a cap on how often loud items (a red anorak, a shell suit) appear in one scene.
- **Order of work:** the ten outerwear silhouettes up to the bar, the jacket first, once, on one body; then resize to the other builds; only then the variants.

## What could not be verified

- The primary pages for KCD2, RDR2, Mafia, Hitman, L.A. Noire and Legion were blocked: those claims rest on search summaries, Wikipedia and crowd.md.
- The City Sample Crowds licence text was not read, and the two sources disagree on the head count.
- The RDR2 counts come from a modders' dump, read through the fetch tool's summary.
- No published threshold for when players notice repeated clothes; no garment counts for KCD2, Mafia, Hogwarts Legacy, Mad Max or GTA crowds.
- The search allowance ran out before RDR2's costume research or Hogwarts Legacy.

## Sources (accessed 1 October 2026)

1. Epic, "City Sample Project", Unreal 5.8 docs, undated. dev.epicgames.com/documentation/en-us/unreal-engine/city-sample-project-unreal-engine-demonstration. OPENED.
2. Epic, "City Sample Crowds", Fab, undated. fab.com/listings/903037e9-e1ac-4f41-96e8-1683c6fa7ad4. SUMMARY.
3. Vrealmatic, "Crowds in CitySample", 24 Oct 2023. vrealmatic.com/unreal-engine/city-sample/crowd. SUMMARY (opened by an earlier helper on 24 September, per crowd.md).
4. ArtStation, "Matrix Awakens Crowd Characters", undated. artstation.com/artwork/o2yk1w. SUMMARY.
5. Epic, "Create MetaHuman Crowds", undated. dev.epicgames.com/documentation/metahuman/create-metahuman-crowds-in-unreal-engine. OPENED.
6. Epic, "MetaHuman Collections", 5.8, undated. dev.epicgames.com/documentation/metahuman/metahuman-collections-in-unreal-engine. OPENED.
7. Epic, "Getting Started with MetaHuman Crowds", undated. dev.epicgames.com/documentation/metahuman/getting-started-with-metahuman-crowds-in-unreal-engine. OPENED.
8. Epic, "Layered Materials", 5.8, undated. dev.epicgames.com/documentation/en-us/unreal-engine/layered-materials-in-unreal-engine. OPENED.
9. lucienlmy, "Basic Ped YMT Editing", GitHub, undated. github.com/lucienlmy/5mod-tutorials. OPENED.
10. femga, rdr3_discoveries (clothes/metaped_outfits.lua), GitHub, undated. github.com/femga/rdr3_discoveries. OPENED through the fetch tool's summary.
11. Cfx forum, "Ped Modification and MetaData Overview", undated. forum.cfx.re/t/5124046. SUMMARY.
12. Wikipedia, "Kingdom Come: Deliverance", live page. OPENED.
13. Wikipedia, "Kingdom Come: Deliverance II", live page. OPENED.
14. Nexus Mods, "How to modify character_preset" (KCD2), undated. nexusmods.com/kingdomcomedeliverance2/articles/166. SUMMARY.
15. CDPR Modding Docs, "Multilayered: Cyberpunk's supershader", 15 Oct 2024. github.com/CDPR-Modding-Documentation/Cyberpunk-Modding-Docs. OPENED.
16. redmodding wiki, "Garment Support: How does it work?", undated. wiki.redmodding.org. SUMMARY.
17. Fauerby (IO Interactive), "Crowds in Hitman: Absolution", GDC 2012, slides PDF on media.gdcvault.com. SUMMARY (opened by an earlier helper on 24 September, per crowd.md).
18. McDonnell et al., "Clone Attack! Perception of Crowd Variety", SIGGRAPH 2008. SUMMARY (opened by an earlier helper on 24 September, per crowd.md).
19. McDonnell et al., "Eye-catching Crowds", ACM TOG 28(3), 2009. SUMMARY.
20. Maïm, Yersin and Thalmann, "Unique Character Instances for Crowds", IEEE CG&A 29(6), 2009. SUMMARY.
21. God is a Geek, "Behind the Scenes of L.A. Noire: Costume & Wardrobe", Feb 2011. SUMMARY.
22. Wikipedia, "L.A. Noire", live page. OPENED.
23. Wikipedia, "Development of Red Dead Redemption 2", live page. OPENED.
24. 2K, "Mafia: The Old Country Dev Diary 1", 2025. mafia.2k.com/the-old-country/news/dev-diary-1-authenticity-sicily/. SUMMARY.
25. 2K Valencia, "Mafia: The Old Country Character Art", undated. valencia.2k.com/mafia-the-old-country-character-art/. SUMMARY.
26. PlayStation Blog, "How Hangar 13 remade Mafia", 24 Sep 2020. SUMMARY.
27. Neubelt and Pettineo, "Crafting a Next-Gen Material Pipeline for The Order: 1886", SIGGRAPH 2013. SUMMARY.
28. Fast Company and CBC on Laurent Turcot, 2014. fastcompany.com/3037212. SUMMARY.
29. Dragert (Ubisoft), "Census", GDC 2021, gdcvault.com/play/1027018; GameRevolution's interview with Joel Burgess, 2020. SUMMARY.
30. Project files: production/research/casting/notes/crowd.md; ledger-v2/research/license-allowlist.md (entry 8); production/research/shop-window-interiors/NOTE.md.
