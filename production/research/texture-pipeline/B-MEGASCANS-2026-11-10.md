# B. Megascans on Fab: the 5 Nov change, candidates, library (read 10 November 2026)

First-pass reading, no decision. Questions 9 to 11 of QUESTIONS-2026-11-10.md. Every link read on 10 Nov 2026 unless stated. "Unverified" marks anything not confirmed on a page.

## 9. The change and Fab's terms

**The change.** Quixel's notice (https://quixel.com/news/update-megascans-are-going-free-again, dated 5 Nov 2026, read 10 Nov through a page-answering fetch tool, not raw text):
- The full Megascans library is made free on Fab.
- Quixel's terms for all Quixel assets are updated so that AI models may be trained on Megascans and Megaplants.
- Purchases of Megascans or a Quixel Bundle on or after 1 Jan 2025 are refunded to the buyer's Epic account balance, with the licence kept. The refund is paid by the end of 2026, and the balance buys only Epic products.
- Studio licences stay under their contracts.
- Fab support handles issues.

The notice links no separate terms text. Quixel's full updated terms were not reached (unreached).

**Secondary reports, same date range.**
- 80.lv (https://80.lv/articles/entire-quixel-megascans-library-now-available-for-free/, 6 Nov 2026, read 10 Nov) and CG Channel (https://www.cgchannel.com/?p=179945, 6 Nov 2026, read 10 Nov) say Fab listings update through 12 Nov, and CG Channel says most were already free when written.
- CG Channel says the Fab standard licence "doesn't appear to have changed", and that listings now read "Allows usage with AI: Yes".
- Both give over 23,000 assets (CG Channel).
- Quixel does not say how long the offer lasts. The 2024 free period ended (CG Channel).
- The 12 Nov date is from the press, not Quixel (unverified at the source).

**What the listings show today.** Every Quixel Megascans and Megaplants listing opened below read Price "Free" (0.0 CHF in the page data) and "Allows usage with AI: Yes". The "Generated with AI" line is "No" where shown. Where the licence field appears it reads "-".
- This reverses the 3 Oct finding that Megascans carry `isAiForbidden: true` (asset-plan/0-SOURCES-AND-LICENCES.md, source 10), at least for these listings.
- The allowlist (ledger-v2/research/license-allowlist.md, line 5, read 10 Nov) already admits Quixel Megascans, even tagged NoAI, by his ruling of 13 Oct. The tag no longer matters for these listings.

**Fab's licence terms, as read.**
- Fab licence summary, https://www.fab.com/eula, read 10 Nov (page partly rendered; the full EULA, the binding text, was not reached):
  - Allowed: "Use the assets commercially or privately" and "Commercially distribute your Projects with the Fab assets incorporated into it".
  - Credit: "You are not required to give credit to the publisher".
  - Barred: "Resell or redistribute the asset for free on a standalone basis or allow others to do the same".
  - The NoAI wording and the last-updated date were absent from what rendered.
- Fab licences and pricing, https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab, read 10 Nov:
  - Standard licence has Personal tier (buyer under US$100,000 gross commercial revenue in the last 12 months) and Professional tier.
  - The page does not mention Quixel.
  - The NoAI tag means "must not be used for generative AI data collection".
- Fab licence of Quixel listings: each page shows only "-". Standard licence is assumed from Quixel's Fab FAQ (https://forums.unrealengine.com/t/quixel-to-fab-transition-faqs/2033839, read 10 Nov: claimed free assets are "covered by the Fab Standard License"). That FAQ is from 2024; whether it holds for the 2026 items is unverified.
- Seller pages: https://www.fab.com/sellers/Quixel%20Megascans returned an empty listing (the filters read 0, a scripted page that did not render); its About page says the profile joined Fab on 12 Sep 2024.

**Megaplants flag.** Each Megaplants listing says Megaplants and the Procedural Vegetation Editor are Experimental, the plugin and "Nanite Foliage (Experimental)" must be switched on, and "We do not recommend shipping projects with Experimental features." (English Oak and Silver Birch pages, read 10 Nov.) This is a shipping risk, not a licence limit.

## Method and arithmetic

**Resolution.** Fab pages give texel density and scan area, not pixel size. Source map width is density times width of scan:
- 4096 px/m x 2 m = 8192 px;
- Brick Facade, 8192 px/m x 1 m = 8192 px.

Quixel's resolution tiers (low, medium, high) are not named on these pages (unverified), so 2K and 4K are what our game would downsample to.

**Card memory per map, with a full mip chain (x 1.333).**
- 2K = 2048 x 2048 = 4,194,304 px; 4K = 16,777,216 px.
- BC1 is 0.5 byte per pixel: 2K = 2 MiB, 2.67 MiB with mips; 4K = 8 MiB, 10.67 MiB with mips.
- BC5 and BC7 are 1 byte per pixel: 2K = 4 MiB, 5.33 MiB with mips; 4K = 16 MiB, 21.33 MiB with mips.

**A material set.** Base colour in BC1 (opaque), normal in BC5, one packed roughness/AO/height map in BC1 (our packing, not Megascans's):
- 2K = 2.67 + 5.33 + 2.67 = 10.7 MiB;
- 4K = 10.67 + 21.33 + 10.67 = 42.7 MiB;
- with base colour in BC7 instead, 2K = 13.3 MiB and 4K = 53.3 MiB.

A virtual texture, streaming or a shared tile that serves many walls costs the set once. A unique set per wall costs it per wall. Measured MB on the project's card is not given here (question 13 covers it).

## 10. Candidates and fit

Hours saved are compared with phase 2's rows in production/research/phase2-plan/PIECES-DRAFT-2026-11-08.md (§1, read 10 Nov). Phase 2's rows are guesses, so these savings are inferred by this note and are guesses too. "Fit" means what the listing's own tags and text say. No page claims Britain or 1990. All are unverified for fit until looked at by eye.

### Hill's tree crowns (phase 2: 8 to 16 h, "tries spent")
All four are Quixel Megaplants, free, "Allows usage with AI: Yes", format Unreal Engine (English Oak also USD), texture resolution and polycount not stated on the page.
1. Megaplants: English Oak (Quercus robur), https://www.fab.com/listings/83642c38-7661-4df1-8629-0422e1898d26
2. European Beech (17 trees: 8 forest, 1 field, 4 saplings, 4 seedlings; season and wind controls; Pivot Painter and simple wind options), https://www.fab.com/listings/d11cc01d-9422-41b7-950f-416c9ce79caf
3. Megaplants: Silver Birch (Betula pendula / papyrifera), https://www.fab.com/listings/94262633-61ed-4f4b-993e-dbc24af3e6ba
- Also seen: Megaplants: European Hornbeam, https://www.fab.com/listings/43679e75-6ed0-4b03-9288-9e2bc49376d2. No sycamore listing was found.
- Fit: oak, beech, birch and hornbeam are native or common in Britain (general knowledge, unverified for a northern port hillside). The hill sits 110 to 206 m from the camera (asset-plan SUMMARY, family 10), so crowns are seen as masses, where the experimental Nanite foliage may be the least costly route. Card memory: unverified, because the pages give no texture size. A tree's leaf atlas is the cost, not the set above.
- Hours saved: 4 to 8 h. Risks: the experimental status above; our two spent tries on the hill (his yes for a third); the engine version needed is not stated (unverified).

### Flemish bond brick (phase 2: 4 to 8 h)
No Megascans listing found named or tagged Flemish or header bond (searched 10 Nov).
1. Brick Wall Worn, 8192 px/m, 2 x 1 m (8192 x 4096 px source), maps include basecolor, normal, roughness, no AO or displacement listed, https://www.fab.com/listings/499d9ba7-f361-491c-b66e-c16c89bac34a
2. Brick Facade, 8192 px/m, 1 x 1 m, tags "decorative, modern, clean, ornate", https://www.fab.com/listings/0300d8e5-4ec6-4342-9afe-d2f54cc709e4
3. Old Damaged Wall, 3413 px/m, 2.4 x 2.4 m, https://fab.com/listings/cd91c1f2-5065-4662-8f9a-57d5d84af368
- Fit: all three unverified for Britain; Brick Facade's tags read modern. None can supply the bond. The pattern must be ours (the plan's own bond material), with a scan only as a wear and colour source.
- Card memory: one set, as above (10.7 MiB at 2K, 42.7 MiB at 4K), shared along the street.
- Hours saved: 0 to 2 h.

### Worn paint at shop fronts' edges (no own row; inside wear on shells and fronts)
1. Flaked Paint Wall, 4096 px/m, 2 x 2 m, tags plaster, peeling, flake, https://www.fab.com/listings/b718e7f1-4f5e-4dc9-a950-4aa2cf937b64
2. Painted Wall Plaster, 4096 px/m, 4 x 1 m, tags street, dirty, painted, https://www.fab.com/listings/437394c0-7993-4378-8b65-2d4ba3135a9f
- Fit: unverified (the first reads interior and rural). A scan of flaking paint is a mask or detail source for edges, not the edge wear itself, which our wear-in-the-material method places by rule.
- Card memory: one 2K mask in BC1 = 2.67 MiB; set as above.
- Hours saved: 1 to 2 h.

### Crates and bins (inside furniture 20 to 30 h and props rows)
Few fits. Bottle crates are out by rule; no wheelie bin, dustbin, milk crate or fish box listing was found by Quixel (searched 10 Nov).
1. Wooden Storage Box, 0.3 x 0.5 x 0.06 m, 6576 px/m, https://www.fab.com/listings/53a6cf14-0cf5-46d0-b90b-71134b7c490e
2. Industrial Junkyard Crate Metal, 0.89 x 1.23 x 0.76 m, 6382 px/m, https://www.fab.com/listings/3e83258c-676f-48b0-860c-10f16e917684
- Fit: both read industrial or warehouse (unverified for a 1990 British quay).
- Card memory: unique per prop, one set each (10.7 MiB at 2K).
- Hours saved: 1 to 3 h.

### Furniture and props (phase 2: about 10 kinds, 20 to 30 h; the task estimate 49 to 84 h is the brief's figure, not found in these files)
Megascans is strong on scanned junk, weak on street furniture. Found: the two items above. Nothing for bollards, benches, kiosk or pillar box. Hours saved: 0 to 2 h, beyond the crates row.

### Grime decals (inside wear and the street-weathering rows)
1. Leakage, 2048 px/m, 2 x 4 m, format Image (brush), tags seepage, wall, stained, https://www.fab.com/listings/ab46f137-ab5c-4f68-a2f5-508d7a04680e
- Third parties (not Quixel): Stains decals Vol. 1 (Unimodels) shows "Allows usage with AI: No", 8.18 CHF, so out (https://www.fab.com/listings/8b833dc7-5777-4a9a-b621-70c0128f2215).
- Other free Quixel decals (Mud Stain, Oil Stain) were seen only in a category snippet; not opened (unverified).
- Fit: unverified. Card memory: 2048 px/m x 4 m = 8192 px tall; at 2K width a BC4 (single mask) is 2 MiB with mips 2.67 MiB for 2K x 2K.
- Hours saved: 2 to 4 h.

### Street surfaces: flags, kerbs, setts, tarmac (phase 2: wet seam and icy lane 6 to 10 h; surfaces exist from ambientCG and Poly Haven)
1. Sidewalk Tiles, 8192 px/m, 1 x 1 m, tags worn, granite, https://www.fab.com/listings/bfbff6d3-7fb4-44bd-a618-29560f8fb075
2. Stone Pavement, 4096 px/m, 2 x 2 m, tags worn, chipped, https://fab.com/listings/75c9d8f7-52c5-4b3f-bd2d-82cfd7c9aa6f
3. Asphalt Road, 9752 px/m, 0.42 x 0.42 m, tags coarse, worn, dirt, https://www.fab.com/listings/ab56bd64-6bd4-4882-8a02-86826355a8dd
- Also: Road Asphalt, 10503 px/m, 0.39 m, tags fresh, smooth, https://www.fab.com/listings/37df99dd-442a-43ff-9e61-b85470d70341. Both asphalt scans are small areas (about 0.4 m), so tiling repeats show; unverified.
- Kerbs and setts: no Quixel listing found. "Megascans: Cobblestone" and "Megascans: Asphalt" were seen as legacy Marketplace items "not migrated to Fab" (search snippet, unverified). The one paving pack seen, Game ready Granitic Paving Stones (Rodrigo's kiosk), reads "Allows usage with AI: No" and 16.38 CHF, so out (https://www.fab.com/listings/31c64ed1-620d-4ce6-a955-6e022820e779).
- Card memory: a set per surface, 10.7 MiB at 2K, 42.7 MiB at 4K; four surfaces, 43 MiB at 2K.
- Hours saved: 1 to 3 h (the street's materials already exist).

### Total estimate
Hill 4 to 8, bond 0 to 2, paint 1 to 2, crates and bins 1 to 3, furniture 0 to 2, decals 2 to 4, surfaces 1 to 3 gives about 9 to 24 h of hand work avoided against phase 2's guesses (inferred; not measured). The hill's 4 to 8 h is the only large part, and it carries the experimental risk.

## 11. Least effort into his Fab library

- He signs in on fab.com (permitted: he signs in, not us) and opens each link above, then clicks Add to My Library on the free listing. One list of about 15 links in one message is the least effort found: it is one click per asset after the link opens.
- No bulk add or "collection" feature was confirmed. The 2024 forum threads say "Add All to Library" was promised and may never have shipped (search snippets, 10 Nov; unverified). support.fab.com returned only a loading page (unreached).
- The 2024 FAQ says claimed free assets may need a separate "Add to library" step (forum quoting, unverified for 2026).
- For use in the editor: Fab plugin in Unreal, window Fab, then Add to Project. Epic's launcher page: https://dev.epicgames.com/documentation/en-us/fab/exporting-assets-from-fab-in-launcher (search listing only, not read in full; unverified). A forum anecdote says Quixel materials sometimes work only by searching the exact name in the editor's Fab panel.
- The seller pages are scripted and showed no listings, so a link list from the individual pages above is the verified route.

## Unreached or not confirmed
- Quixel's full updated terms text; the full Fab EULA (section on NoAI, date); support.fab.com; seller listing grids.
- Megascans's resolution tiers; whether all links stay free after 12 Nov.
- Any British or 1990 fit (no page states origin beyond Roman Brick Wall's Spain and Urban Prison Wall's prison theme).
- The brief's 49 to 84 h figure: not found in the phase 2 files read.
- Pages not opened (search lists only): the Quixel Megascans and Megaplants pages for other trees, "Mud Stain", "Oil Stain".
- No download was made, and nothing was added to a library.
