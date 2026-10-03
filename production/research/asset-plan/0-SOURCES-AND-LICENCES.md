# 0. Sources and licences: the landscape every family depends on

Research helper's note for the asset plan, 3 October 2026. About thirty minutes; 25 web searches.
Marks: **[READ]** read at the source; **[SS]** search summary only; **[I]** my inference; **UNREACHED** the page refused me. **[PC]** means read on Jafar's PC by another session and recorded in the repository (named in Sources); it is not my own read.

## The headline: read this before planning anything

1. **The free Megascans are NoAI.** Every Megascans record the shop-goods research checked on the PC on 3 October carries `isAiForbidden: true` [PC, source 10]. Search summaries say the same of two Megascans listings, "Asphalt Road" and "Leakage" [SS, 9]. Under the owner's rule (NoAI is never used, not even as a reference), **every Megascan in his Fab library is out**: the 18 surfaces and decals for the proof frame and the shop goods (production/specs/fab-free-megascans.md). His rulings of 1 and 3 October rest on them, so this needs his ruling now. Until then, no plan should count on a Megascan.
2. **Epic's own samples appear to be NoAI too.** Search summaries say the Game Animation Sample and City Sample listings "do not allow usage with AI" [SS, 8]. If that holds, GASP is out under the owner's rule. GASP is the source for the people's poses (proof-frame item 11, and his yes of 3 October). Confirm on the PC from the listing's own data before anyone builds on it.
3. **Fab makes every MetaHuman-compatible listing NoAI, automatically.** That covers characters, grooms and clothing: "The NoAI tag is required for all listings of MetaHuman compatible content. It is applied automatically to these listings." [READ, 2]. So the 247 NoAI suits found on 2 October were Fab's rule at work, not bad luck. **No MetaHuman-ready garment on Fab can ever pass.** Searching Fab for one again is wasted time.
4. **What NoAI forbids is wider than "training".** Fab's documentation calls it a tag meaning an asset "must not be used for generative AI data collection" [READ, 1]. The contract goes further [SS, 4]: NoAI content may not be used "(iii) as inputs to Generative AI Programs". Claude is such a program [I]. In this pipeline an agent opens the files, judges renders and walks the game, so a NoAI asset cannot be used without an AI taking it as input [I]. The owner's rule is the safe reading of the contract, not an over-reading. The natural-idles note ("our AI tester ... trains nothing, so the NoAI flag does not touch it") misses clause (iii) [I].
5. **The clean free sources are few: CC0 (Poly Haven, ambientCG, Sketchfab's CC0 items with no NoAI tag, Blender's CC0 demo files, Quaternius, Kenney), MIT (Rocketbox), Mixamo and OFL fonts.** Of these, only Poly Haven, ambientCG and Sketchfab CC0 scans reach the photoreal bar. Little else does [I].
6. **Nothing printed in Britain in 1990 is public domain.** Crown copyright on a published work lasts "50 years from the date of publication" [READ, 29], so a 1990 government poster is protected until the end of 2040 [I]. Private posters, packaging and signs are protected for longer [I]. Period pictures are references only, and the designs are always ours.

## 1. Fab's NoAI tag and the Fab Standard Licence

**The exact wording I could reach:**
- Fab documentation [READ, 1]: "The NoAI meta tag indicates that an asset must not be used for generative AI data collection." It also says: "NoAI meta tags might not be compatible with Creative Commons licenses. This means that you cannot offer an asset with the NoAI meta tag under the Creative Commons Attribution license."
- Licence types on Fab [READ, 1]:
  - Creative Commons Attribution (CC-BY), free;
  - the Standard licence, free or for sale, in Personal (buyer under US$100,000 gross revenue in the last 12 months) and Professional tiers;
  - the legacy "UE Marketplace License", "being phased out".
  - **Fab has no CC0 option.**
- Epic Content License Agreement, the clause as quoted by search summaries [SS, 4; the page was UNREACHED]:
  - The clause: "You shall not collect, aggregate, mine, scrape, or otherwise use NoAI Content (i) in datasets utilized by Generative AI Programs; (ii) in the development of Generative AI Programs; or (iii) as inputs to Generative AI Programs."
  - "NoAI Content" means "Licensed Content that has been tagged, labeled, or otherwise marked 'NoAI' via the functionality provided by the platform."
  - "Generative AI Programs" means "artificial intelligence, machine learning, deep learning, neural networks, or similar technologies designed to automate the generation of or aid in the creation of new content, including but not limited to audio, visual, or text-based content."
  - Epic promises not to use or license content for generative AI "unless that Licensed Content is owned by Epic" [SS, 4]. So Epic keeps that right over its own content.
- **The Fab EULA itself was UNREACHED here.**
  - The PC read it on 3 October as "last updated 1 October 2024" [PC, 10].
  - An Epic forum post, also UNREACHED, says a 2025 update changed "Section 18.k ... wording around NoAI and CreatedWithAI tags". It also says "the NoAI tag will now be applied by default to MetaHumans published on Fab" [SS, 7].
  - These two dates disagree. The PC should read section 18.k word for word before the owner rules.

**What it forbids, in plain words:**
- Using NoAI content in an AI's datasets.
- Using it in building an AI.
- Using it as **input** to an AI.

It does not say "with AI tools" in those words. But input covers an agent reading the mesh or textures, and very probably an agent judging a render that shows the asset [I]. Clause (iii) has no exception for "we only render it".

**Who sets the tag:**
- The publisher, by ticking "Disallow use by generative AI" in the Fab Publisher Portal [SS, 6].
- Fab itself, on all MetaHuman-compatible content [READ, 2].
- Sellers who used AI must also set "Created with AI" [SS, 6]. That is a different flag.

**Epic's own content:**
- Megascans: `isAiForbidden: true` on every record checked [PC, 10], and "does not allow usage with AI" on two listings [SS, 9].
- Game Animation Sample and City Sample: "does not allow usage with AI" [SS, 8].
- Electric Dreams, Lyra, Cropout and the PCG samples: unknown. They are probably NoAI, given the pattern [I].
- The MetaHuman Clothing Construction Presets in his library are Epic's own MetaHuman-compatible content. They are very probably NoAI under Fab's own rule [I].

**How to tell from a listing:**
- Visible on the page: the details panel reads "Allows usage with AI: No" (or "does not allow usage with AI") [PC, 11].
- In the listing's data: the field `isAiForbidden` is true or false [PC, 10 and 11]. The page also carries an HTML "NoAI" meta tag [SS, 6].
- Shortcuts:
  - a CC-BY listing on Fab cannot carry NoAI [READ, 1];
  - a MetaHuman-compatible listing always does [READ, 2].
- Two traps:
  - mature listings hide the field from a signed-out browser [PC, 11];
  - "free" may mean only the "UEFN – Reference only" tier [PC, 10].
- From this container fab.com is UNREACHED. **Only the PC can read the field.**

## 2. Sketchfab's equivalent

- Sketchfab added "NoAI" and "CreatedWithAI" tags in February 2023 [SS, 13]. Its blog post "Restricting Generative AI Use of Free Models" was UNREACHED; summarised [SS, 12]:
  - The tag "indicates to generative AI programs that a particular model is not to be used for generative AI data collection".
  - A creator who puts NoAI on a Creative Commons model gets a tag that "may not be enforceable outside of the Sketchfab platform because the CC license may allow use of the work by generative AI programs regardless of the tag".
  - So Sketchfab let free models use its own Standard Licence instead, "to contractually prohibit use of their model for generative AI data collection".
- **Can a CC0 model carry NoAI? Yes, as a tag** [SS, 12]. The tag is set apart from the licence, and the blog warns it may not bind a CC model. **Under the owner's rule a CC0 model tagged NoAI is still out.** So the "CC0 filter" is not enough: each page must also show no NoAI tag. Such pages have been read on the PC [PC, 11].
- Two more traps, both found on the PC [PC, 10]:
  - "CC0" in a title can hide a CC-BY licence field ("CC0 – Jar" by plaggy is CC BY);
  - Sketchfab free models under Sketchfab's Standard Licence are a marketplace licence, so they need a ruling.
- sketchfab.com was UNREACHED from here.

## 3. The AI terms of the other sources

| Source | Licence (exact where read) | AI clause | Note |
|---|---|---|---|
| Poly Haven | Licence page: "Our assets are all licensed as CC0, which is effectively Public Domain"; "You can use our assets for any purpose, including commercial work" [READ, 14] | None. The page names "AI researchers using our assets in their work" with approval [READ, 14] | Read from the site's published source, not the live page (UNREACHED) |
| ambientCG | "Creative Commons CC0 1.0 Universal License" [SS, 15] | None found [SS] | Live page UNREACHED |
| Quaternius | All CC0 [SS, 17] | None found | Stylised low-poly. Has a "Universal Animation Library" [SS, title only] |
| Kenney | All CC0: "Commercial use: Yes!", "Attribution: No requirement" [SS, 16] | None found | Stylised, below the bar |
| BlenderKit | Two licences, "Royalty Free" and "CC0"; Royalty Free "doesn't allow to re-sell 3D models even if modified" [SS, 18] | Unknown; licence page UNREACHED | Royalty Free is a marketplace's own licence, so it needs a ruling. CC0 items are allowed item by item. The site may now be called "Blendkit" [SS] |
| Smithsonian Open Access 3D | CC0 on "over 90%" of about 3,000 3D objects [SS, 21] | None found | American collection; little fits |
| Other museum CC0 3D | Sketchfab's CC0 dedication for cultural institutions (2020, 27 institutions; 2,925 models) [SS, 22] | Per item: check the NoAI tag | Many British museums use NC licences [I, unverified]: check each |
| Objaverse / Objaverse-XL | "The use of the dataset as a whole is licensed under the ODC-By v1.0 license. Individual objects in Objaverse-XL are licensed under different licenses." [READ, 23] | It is itself an AI dataset. Objects keep their source licences and may carry NoAI at the source [I] | Take any object from its source page instead (allowlist: "only with per-object license filtering") |
| OpenGameArt CC0 | Per item (CC0, CC-BY, CC-BY-SA, GPL and others) [I] | Unknown; UNREACHED, 24 | Mostly stylised game art; poor fit |
| Blender demo files | Per file: CC0, CC-BY, CC-BY-SA. "Human Base Meshes v1.4.1 ... 49 MB – CC0"; "Classroom ... (CC0, 72 MB)"; most splash scenes CC-BY or CC-BY-SA [READ, 19] | None stated | CC-BY-SA is not on the allowlist (ShareAlike) |
| Blender Studio | "Unless notified otherwise, all digital content (webpages, video, artwork, 3D data) is available under the Creative Commons Attribution 4.0." [READ, 20] | None stated | Production assets need a €11.50 a month subscription [READ, 20]: money. CC-BY 3D needs a ruling |
| MetaHuman (Epic's own) | Unreal EULA since June 2025; free under US$1M revenue [project record]. No use "to build or enhance any database or training or testing any artificial intelligence, machine learning, deep learning, neural networks, or similar technologies" [SS, 27] | Training, testing and enhancing only. Use "in workflows that incorporate artificial intelligence technology" is allowed [SS, 27] | Not a Fab listing, so the NoAI rule for MetaHuman-compatible listings does not touch Epic's own Creator [I] |
| Mixamo | Royalty-free for personal, commercial and non-profit projects [SS, 26]. The user may not "create, train, test, or otherwise improve any machine learning algorithms or artificial intelligence systems" [SS, 26] | Training clause only; no NoAI tag | On the allowlist (D46). Our use trains nothing [I] |
| Microsoft Rocketbox | "MIT License, Copyright (c) 2020 Microsoft"; "The library of avatars is now released under MIT License." 115 rigged avatars and 417 animations [READ, 25] | None | Older game-quality avatars [I]. Check for and exclude any child avatars (canon) [I, unverified] |
| Unreal samples: City Sample, Electric Dreams, Lyra, Cropout, PCG samples | "UE-Only Content – Licensed for Use Only with Unreal Engine-based Products" [SS, 28]. A commercial Unreal game may ship it [project record, 28] | City Sample: NoAI [SS, 8]. Others unknown | Allowlist: UE-only content other than animation needs a ruling. City Sample is modern American; Electric Dreams is jungle; Lyra is sci-fi [project record, 28] |
| Game Animation Sample | Fab Standard Licence; Epic's Unreal-only animation [project record] | NoAI [SS, 8]; the project's own note also calls its flag "NoAI" | Allowed by SHIP-SAFE 8, but out under the NoAI rule if confirmed |
| Megascans, legacy (Bridge and the old Quixel plan) | Old Unreal-plan and Bridge items were UE-Only; items claimed on Fab in 2024 stay usable under the Standard licence [project record, 28] | Today's Fab copies: NoAI [PC, 10] | His account claimed nothing in 2024 (DECISIONS, 1 October), so the legacy terms give him nothing. Bridge is deprecated in 5.8 [project record] |

## 4. Period pictures, print and lettering

- **Copyright term.** A 1990 government poster or leaflet is Crown copyright until the end of 2040. Published Crown works last "50 years from the date of publication" [READ, 29]. Works by private firms last longer [I]. **No 1990 poster, sign or packet is public domain.** Use them for proportion, colour and period feel only; draw our own fictional designs.
- **The Open Government Licence (OGL).** Some Crown works are released under it. Version 3.0 "permits anyone to copy, publish, distribute, transmit and adapt the licensed work, and to exploit it both commercially and non-commercially" [READ, 30].
  - The one condition: "acknowledge the source of the work and (if possible) provide a link to the OGL" [READ, 30].
  - It is "interoperable with Creative Commons' Attribution 4.0 licence" [READ, 30].
  - It does not cover "Logos, crests, and Royal Arms", "Third-party rights" or "Patents, trademarks, and design rights" [READ, 30].
  - The OGL is not on the allowlist, so it needs a ruling.
- **Wikimedia Commons:** UNREACHED (40).
  - What is public domain there is mostly old (for example UK government works published 50 or more years ago, so 1975 or earlier) [I].
  - Photographs of 1990 Britain on Commons are mostly CC-BY-SA, many copied from Geograph [I].
  - Use them as references only, by link.
- **Geograph:** "Creative Commons Attribution-ShareAlike 2.0 Generic" [READ, 31]. It accepts historic photographs and rewards them ("TPoint") [READ, 31], so some 1985 to 1995 street photographs exist [I].
  - As references: fine [I].
  - As textures: CC-BY-SA, which needs a ruling, and ShareAlike is awkward inside a game [I].
  - No AI clause [READ, 31: none mentioned].
- **Historic England Archive:** any reproduction, publication or commercial use needs written permission. The England's Places collection is "for personal reference use only" [SS, 34; UNREACHED].
  - **Never as an asset.**
  - Whether agents may look at it as a reference needs a ruling [I]: showing it to an AI goes beyond "personal reference use" on a strict reading.
- **Not checked:** Flickr Commons ("no known copyright restrictions"), the Imperial War Museum and the Science Museum Group. My memory says IWM and the Science Museum Group use NC licences; that is unverified.

**Fonts.** OFL 1.1 is on the allowlist (SHIP-SAFE 7). Each licence file below was read in Google Fonts' own repository [READ, 35], or in the font's repository where named. Period fits are my judgement [I].

| Font | Licence, as read | Near which 1990 British lettering [I] |
|---|---|---|
| Railway Sans (Greg Fleming; "An open source version of Edward Johnston's ... Typeface for London Underground of 1916") | "licensed under the SIL Open Font License, Version 1.1", Reserved Font Name Railway [READ, 36] | Johnston. London-specific: use only for transport-style notices, never anything that reads as TfL |
| Jost | OFL 1.1 [READ] | Futura: estate agents, chemists, 1980s fascias |
| Libre Franklin | OFL 1.1 [READ] | Franklin Gothic: newspaper bills, posters |
| Oswald | OFL 1.1 [READ] | Condensed gothic: newsagents' boards, posters |
| Alfa Slab One | OFL 1.1, RFN "Alfa Slab" [READ] | Heavy slab: market and sale posters |
| Fraunces | OFL 1.1 [READ] | Its soft, heavy cut comes near Cooper Black: cafés, take-aways |
| Libre Baskerville | OFL 1.1, RFN [READ] | Banks, solicitors, building societies |
| Old Standard TT | OFL 1.1 [READ] | Victorian modern: ghost signs, old fascias |
| Abril Fatface | OFL 1.1 [READ] | Didone display: magazines, beauty salons |
| Josefin Sans | OFL 1.1, RFN [READ] | Art-deco geometric: older cinemas and shops |
| Archivo | OFL 1.1 [READ] | Grotesque: signage, forms |
| Courier Prime | OFL 1.1 [READ] | Typewriter: police forms, notices |
| UnifrakturMaguntia | In Google Fonts' `ofl` folder; authors "j. 'mach' wust", "Peter Wiegel" [READ] | Blackletter: newspaper mastheads |
| Liberation Sans and Serif | "licensed under the SIL Open Font License" [READ, 37] | Arial and Times metrics: print, notices |
| Marcellus SC | OFL 1.1 [READ] | Already ruled for the name plates |
| Overpass | OFL 1.1 [READ] | **Do not use:** it is the American Highway Gothic |

**Transport, the British road-sign typeface:**
- Free versions exist at roads.org.uk ("Transport Medium", "Transport Heavy", by Nathaniel Porter). Search summaries say they are "subject to Crown Copyright" and contain "public sector information licensed under the Open Government Licence v1.0". The same summaries also say the free versions "were only intended for private non-commercial use" [SS, 33; UNREACHED].
  - The two statements conflict. The class is RULING at best, and NO if the non-commercial line holds.
- The commercial "New Transport" (Kubel and Calvert, 2012) and K-Type's "Transport New" (2008) exist [READ, 32]. Both cost money.
- No OFL version was found.
- [I] A route for a ruling: draw our own sign lettering from the Department for Transport's published drawings, if those are under the OGL (not verified).

## 5. Terrain and geodata

| Source | Licence | Attribution | Class |
|---|---|---|---|
| OpenStreetMap | ODbL [I; UNREACHED] | "© OpenStreetMap contributors" [I] | ALLOWED as skeleton only (allowlist 6) |
| Overture Maps | Varies by theme: ODbL or permissive [I, unverified] | Per theme | ALLOWED as skeleton only, if the theme is ODbL or permissive [I] |
| Environment Agency LIDAR Composite DTM, 1 m (England; 2019 to 2022 composites) | "Open Government Licence" [SS, 38] | "© Environment Agency copyright and/or database right [year]" [SS, 38] | RULING: the OGL is not on the allowlist |
| Ordnance Survey OS Terrain 50 (Great Britain, 50 m grid) | OS OpenData, "under an attribution-only licence compatible with CC-BY" since 2010 [READ, 39]; now the OGL [SS, 39] | "Contains OS data © Crown copyright and database right (year)" [SS, 39] | RULING |

- **Does the OGL fit the allowlist?** Not as written. It is an attribution licence for data, interoperable with CC-BY 4.0 [READ, 30], and has no AI clause [READ, 30: none]. It sits closest to CC-BY, which the owner allows today only for voices and garments. **It needs one ruling, and one would cover every UK government source:** LIDAR, OS OpenData, DfT drawings and OGL photographs.
- Terrain from a real port is a height skeleton only; the town stays fictional, as with OSM [I]. LIDAR is from the 2010s and 2020s, and its DTM strips the buildings, which suits a 1990 rebuild [I].

## THE TABLE

Classes:
- ALLOWED: on the allowlist and not NoAI.
- RULING: needs the owner's ruling.
- NO: never, or out under a rule already made.

| # | Source | What it holds that fits 1990 Britain | Licence (exact where read) | AI clause or NoAI | Class | Access | Link |
|---|---|---|---|---|---|---|---|
| 1 | Fab, third-party Standard-licence items with `isAiForbidden` false | Some props, materials and unrigged meshes; must be screened one by one | Fab Standard licence (Personal/Professional) [READ, 1] | None on these items; check every listing | ALLOWED | fab.com UNREACHED; [PC] | https://www.fab.com |
| 2 | Fab, any listing tagged NoAI | Most marketplace clothing and many packs | Standard licence + NoAI | NoAI: no datasets, no AI development, not "as inputs to Generative AI Programs" [SS, 4] | NO | [PC], [SS] | https://www.fab.com |
| 3 | Fab, MetaHuman-compatible content (characters, grooms, clothing) | Suits, coats, hair | Standard only; CC-BY disabled [READ, 2] | NoAI always, set automatically [READ, 2] | NO | [READ] (docs) | https://dev.epicgames.com/documentation/metahuman/selling-metahumans-on-fab |
| 4 | Fab, Quixel Megascans (free starter set and paid) | Asphalt, flags, brick, leakage decals, food | Standard licence [PC, 10] | NoAI: `isAiForbidden: true` on every record checked [PC, 10]; [SS, 9] | NO under his rule; ruling needed now | [PC], [SS] | https://www.fab.com/sellers/Quixel%20Megascans |
| 5 | Fab, Epic's Game Animation Sample | About 1,800 idles, walks and breaks | Standard licence; Unreal-only use (SHIP-SAFE 8) | NoAI [SS, 8] | NO if confirmed; check on PC | [SS] | https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016 |
| 6 | Fab, City Sample (Buildings, Vehicles, Crowds) | Methods only; modern American art | "UE-Only Content – Licensed for Use Only with Unreal Engine-based Products" [SS, 28] | NoAI [SS, 8] | NO | [SS] | https://www.fab.com/listings/4898e707-7855-404b-af0e-a505ee690e68 |
| 7 | Fab, Electric Dreams, Lyra, Cropout, PCG samples | Methods (spline PCG for kerbs and walls), not art | UE-Only Content [SS, 28] | Unknown; probably NoAI [I] | RULING (UE-only), and NO if NoAI; check before an agent opens one | [SS] | https://dev.epicgames.com/documentation/unreal-engine/electric-dreams-environment-in-unreal-engine |
| 8 | Fab, CC-BY listings | Assorted scans and props | CC-BY 4.0 [READ, 1] | Cannot carry NoAI [READ, 1] | RULING (CC-BY for 3D) | [READ] (docs) | https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab |
| 9 | Fab, legacy "UE Marketplace License" items | Older packs | UE Marketplace Licence, "being phased out" [READ, 1] | Unknown | RULING | [READ] (docs) | https://www.unrealengine.com/eula/content |
| 10 | Megascans, legacy Bridge and Quixel plan | Nothing for him: his account claimed none in 2024 | UE-Only (old) [project record] | n/a | NO (nothing held) | project record | production/research/aaa-street/2-EPIC-FREE-CONTENT.md |
| 11 | MetaHuman (Epic's Creator and its bodies) | The cast | Unreal EULA; free under US$1M | No use to "build or enhance any database or training or testing any artificial intelligence..." [SS, 27]; AI workflows allowed | ALLOWED | [SS]; EULA UNREACHED | https://www.unrealengine.com/eula/unreal |
| 12 | Mixamo | Idles, walks, gestures; bodies | Royalty-free, Adobe's terms [SS, 26] | No use to "create, train, test, or otherwise improve" AI [SS, 26]; no NoAI | ALLOWED (D46) | [SS]; FAQ UNREACHED | https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html |
| 13 | Sketchfab, CC0 items | Food scans (ffishAsia), period objects, museum scans | CC0 1.0, read from the licence field, not the title | NoAI tag possible even on CC models [SS, 12]; check each page | ALLOWED item by item | sketchfab.com UNREACHED; [PC] | https://sketchfab.com/search?features=downloadable&licenses=7c23a1ba438d4306920229c12afcb5f9&type=models |
| 14 | Sketchfab, CC-BY and Sketchfab Standard (free) | Suits, props | CC BY 4.0, or Sketchfab Standard | CC-BY may carry the tag; Standard + NoAI is binding [SS, 12] | RULING (CC-BY 3D; marketplace licence); NO if tagged | [SS], [PC] | https://sketchfab.com/blogs/community/restricting-generative-ai-use-of-free-models/ |
| 15 | Poly Haven | Brick, plaster, asphalt, cobbles, overcast HDRIs, a few props | "all licensed as CC0, which is effectively Public Domain" [READ, 14] | None; welcomes AI researchers [READ, 14] | ALLOWED | [READ] (site source on GitHub); site UNREACHED | https://polyhaven.com/license |
| 16 | ambientCG | Materials, decals, wear masks | "Creative Commons CC0 1.0 Universal License" [SS, 15] | None found | ALLOWED | [SS]; UNREACHED | https://docs.ambientcg.com/license/ |
| 17 | Quaternius | Stylised props; a CC0 animation library | CC0 [SS, 17] | None found | ALLOWED (below the bar except animations) | [SS]; UNREACHED | https://quaternius.com/ |
| 18 | Kenney | Stylised kits; blockout at most | CC0 [SS, 16] | None found | ALLOWED (below the bar) | [SS]; UNREACHED | https://kenney.nl/support |
| 19 | BlenderKit, CC0 items | Materials, some props; scriptable add-on | CC0 [SS, 18] | Unknown | ALLOWED item by item | [SS]; UNREACHED | https://www.blenderkit.com/docs/licenses/ |
| 20 | BlenderKit, Royalty Free items | Most models | "Royalty Free"; no resale [SS, 18] | Unknown | RULING | [SS]; UNREACHED | https://www.blenderkit.com/docs/licenses/ |
| 21 | Blender demo files, CC0 ones | Human Base Meshes v1.4.1 (garment and figure bases), Classroom scene | "CC0" per file [READ, 19] | None | ALLOWED | [READ] | https://www.blender.org/download/demo-files/ |
| 22 | Blender demo files CC-BY and CC-BY-SA; Blender Studio | Production rigs and assets, little period fit | "Creative Commons Attribution 4.0" (Studio, unless notified) [READ, 20]; CC-BY-SA per file [READ, 19] | None | RULING (CC-BY 3D; CC-BY-SA); Studio assets cost €11.50 a month | [READ] | https://studio.blender.org/terms-and-conditions/ |
| 23 | Smithsonian Open Access 3D | Few: American objects | CC0 on over 90% [SS, 21] | None found | ALLOWED item by item | [SS]; 3d.si.edu UNREACHED | https://3d.si.edu/ |
| 24 | Other museums' CC0 3D (Sketchfab dedication) | Occasional British objects | CC0 per item [SS, 22] | Check each page's tag | ALLOWED item by item; many British museums use NC (NO) [I] | [SS] | https://sketchfab.com/blogs/community/sketchfab-launches-public-domain-dedication-for-3d-cultural-heritage/ |
| 25 | Objaverse / Objaverse-XL | Copies of Sketchfab, GitHub and Thingiverse objects | Dataset ODC-By v1.0; objects their own [READ, 23] | Made for AI training; source NoAI tags may be lost [I] | RULING per object; prefer the source page | [READ] README; HF card UNREACHED | https://github.com/allenai/objaverse-xl |
| 26 | OpenGameArt | Little photoreal | Per item [I] | Unknown | ALLOWED only for CC0 items; poor fit | UNREACHED | https://opengameart.org/content/faq |
| 27 | Microsoft Rocketbox | 115 rigged avatars, 417 animations: distant crowd at most | "MIT License, Copyright (c) 2020 Microsoft" [READ, 25] | None | ALLOWED (exclude any child avatars) | [READ] | https://github.com/microsoft/Microsoft-Rocketbox |
| 28 | Wikimedia Commons, PD and CC0 categories | Mostly pre-1975 public-domain material; 1990 photos are CC-BY-SA | Per file | None | ALLOWED only for PD or CC0 files; others reference only | UNREACHED | https://commons.wikimedia.org/wiki/Commons:Licensing |
| 29 | Geograph | Street photographs, some historic | "Creative Commons Attribution-ShareAlike 2.0 Generic" [READ, 31] | None | Reference: fine. Texture: RULING | [READ] (Wikipedia); site UNREACHED | https://www.geograph.org.uk |
| 30 | 1990 government posters and leaflets (Crown copyright) | Road safety and public information designs | Crown copyright, 50 years from publication [READ, 29]: until 2040 | n/a | NO as assets; reference only | [READ] | https://en.wikipedia.org/wiki/Crown_copyright |
| 31 | OGL-released Crown material (e.g. DfT drawings) | Sign layouts, lettering drawings [I] | OGL v3.0 [READ, 30] | None | RULING (one ruling covers 30 to 33's OGL sources) | [READ] (Wikipedia); TNA UNREACHED | https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/ |
| 32 | Historic England Archive and England's Places | Period photographs of English streets | Permission needed; "personal reference use only" [SS, 34] | n/a | NO as assets; RULING for agents to view | [SS]; UNREACHED | https://historicengland.org.uk/images-books/archive/policies/using-images/ |
| 33 | OFL fonts (Railway Sans, Jost, Libre Franklin, Oswald, Alfa Slab One, Fraunces, Libre Baskerville, Old Standard TT, Courier Prime, Liberation and others) | Fascias, posters, notices, mastheads | "SIL Open Font License, Version 1.1" [READ, 35 to 37] | None | ALLOWED | [READ] | https://github.com/google/fonts/tree/main/ofl |
| 34 | Transport, free versions (roads.org.uk) | 1990 road signs | Crown copyright; OGL v1.0; also reported as "private non-commercial use" [SS, 33] | None known | RULING at best; NO if non-commercial | [SS]; UNREACHED | https://www.roads.org.uk/fonts |
| 35 | New Transport (A2-Type) and Transport New (K-Type) | 1990 road signs | Commercial [READ, 32] | Unknown | NO (money, under today's rule) | [READ] (Wikipedia) | https://en.wikipedia.org/wiki/Transport_(typeface) |
| 36 | OpenStreetMap / Overture | Street skeletons of real ports | ODbL; Overture per theme [I] | None | ALLOWED as skeleton only | UNREACHED | https://www.openstreetmap.org/copyright |
| 37 | Environment Agency LIDAR, 1 m DTM | The hill's shape from a real English port | Open Government Licence [SS, 38] | None | RULING | [SS]; UNREACHED | https://www.data.gov.uk/dataset/3fc40781-7980-42fc-83d9-0498785c600c/lidar-composite-dtm-2019-1m |
| 38 | OS Terrain 50 (OS OpenData) | Coarse terrain of Great Britain | OGL; attribution-only since 2010 [READ, 39; SS, 39] | None | RULING | [SS]; UNREACHED | https://www.data.gov.uk/dataset/835cf20a-8feb-4394-8b30-dcfe840ac13d/os-terrain-50-dtm2 |

## What the owner should be asked (for the planner to pass on)

1. **Megascans and GASP are NoAI.** Megascans are confirmed on the PC; GASP is from search summaries only. Options:
   - (a) keep the rule: drop them, and use Poly Haven and ambientCG for surfaces, and Mixamo, Rocketbox or Quaternius for idles; **my recommendation**;
   - (b) allow NoAI Epic content in the build only, with agents never opening or judging it. This is unworkable here, because every frame is judged by an AI [I].
2. **One ruling for the Open Government Licence** (LIDAR, OS Terrain 50, OGL drawings and photographs). It is an attribution licence like CC-BY.
3. **Whether agents may look at Historic England and other "personal reference only" archives.**

## What I could not reach or verify

- **Pages refused:**
  - fab.com: the EULA, listings and Fab's own data;
  - support.fab.com, forums.unrealengine.com, unrealengine.com (the Epic Content and Unreal EULAs), quixel.com;
  - sketchfab.com, polyhaven.com, ambientcg.com, blenderkit.com and blendkit.com, kenney.nl, quaternius.com, opengameart.org;
  - helpx.adobe.com, 3d.si.edu, huggingface.co, commons.wikimedia.org, wiki.openstreetmap.org, nationalarchives.gov.uk, data.gov.uk, historicengland.org.uk, roads.org.uk, whatdotheyknow.com;
  - gamefromscratch.com, the-decoder.com.
- **Not verified:**
  - the Fab EULA's own NoAI wording (section 18.k) and its current date;
  - whether GASP, the Clothing Construction Presets, Electric Dreams, Lyra, Cropout and the PCG samples carry `isAiForbidden: true`;
  - BlenderKit's AI terms;
  - the Overture licences;
  - whether Rocketbox has child avatars;
  - which British museums publish CC0 3D;
  - the licence of the free Transport fonts.
- The NoAI clause text comes from search summaries of the Epic Content License Agreement. **It is not read.** The PC should read fab.com/eula before the ruling.

## Sources (all read or searched on 3 October 2026)

1. "Licenses and Pricing in Fab", Epic developer documentation, undated. https://dev.epicgames.com/documentation/en-us/fab/licenses-and-pricing-in-fab [READ]
2. "Selling MetaHumans on Fab", Epic developer documentation, undated. https://dev.epicgames.com/documentation/metahuman/selling-metahumans-on-fab?lang=en-US [READ]
3. "Publishing Assets for Sale or Free Download in Fab", Epic developer documentation, undated (no AI text found). https://dev.epicgames.com/documentation/fab/publishing-assets-for-sale-or-free-download-in-fab [READ]
4. Epic Content License Agreement, undated. https://www.unrealengine.com/eula/content [SS; UNREACHED]
5. Fab End User License Agreement. https://www.fab.com/eula [UNREACHED here; read on the PC as "last updated 1 October 2024", see 10]
6. "(Fab) NoAI meta tags and Created with AI self-declaration", Fab support, January 2025. https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration [SS; UNREACHED]
7. "Fab Document Updates (EULA, Fab Distribution Agreement, etc.)", Epic forums, 2025. https://forums.unrealengine.com/t/fab-document-updates-eula-fab-distribution-agreement-etc/2540618 [SS; UNREACHED]
8. Fab listings, undated: Game Animation Sample https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016 ; City Sample https://www.fab.com/listings/4898e707-7855-404b-af0e-a505ee690e68 [SS; UNREACHED]
9. Fab listings, undated: Asphalt Road https://www.fab.com/listings/ab56bd64-6bd4-4882-8a02-86826355a8dd ; Leakage https://www.fab.com/listings/ab46f137-ab5c-4f68-a2f5-508d7a04680e [SS; UNREACHED]
10. production/research/shop-window-interiors/GOODS-2026-10-03.md, 3 October 2026, section 2 (Megascans `isAiForbidden: true`; the Fab EULA date; Sketchfab traps). [project record, PC]
11. production/art/clothing/SCREENING-2026-10-02.md, 2 October 2026 ("Allows usage with AI: No"; `isAiForbidden`; 247 of 387 NoAI). [project record, PC]
12. "Restricting Generative AI Use of Free Models", Sketchfab blog, undated. https://sketchfab.com/blogs/community/restricting-generative-ai-use-of-free-models/ [SS; UNREACHED]
13. "Sketchfab introduces NoAI and CreatedWithAI tags", CG Channel, February 2023. https://www.cgchannel.com/2023/02/sketchfab-introduces-noai-and-createdwithai-tags/ [SS]
14. Poly Haven licence page text, from the site's source repository (master branch), undated. https://raw.githubusercontent.com/Poly-Haven/polyhaven.com/master/public/locales/en/license.json [READ]; live page https://polyhaven.com/license [UNREACHED]
15. "License – ambientCG Docs", undated. https://docs.ambientcg.com/license/ [SS; UNREACHED]
16. "Support – Kenney", undated, and Kenney on X, 2025. https://kenney.nl/support [SS; UNREACHED]
17. Quaternius, undated. https://quaternius.com/ ; https://quaternius.com/packs/universalanimationlibrary.html [SS; UNREACHED]
18. BlenderKit licences, undated. https://www.blenderkit.com/docs/licenses/ and https://www.blendkit.com/docs/licenses/ [SS; UNREACHED]
19. "Demo Files", blender.org, updated to 2 October 2026. https://www.blender.org/download/demo-files/ [READ]
20. Blender Studio "Terms and conditions", undated, and "Welcome", undated. https://studio.blender.org/terms-and-conditions/ ; https://studio.blender.org/welcome/ [READ]
21. Smithsonian OpenAccess repository README, updated 21 December 2021. https://raw.githubusercontent.com/Smithsonian/OpenAccess/master/README.md [READ] (metadata only); CC0 3D figures from si.edu and CG Channel, March 2020 [SS]
22. "Sketchfab Launches Public Domain Dedication for 3D Cultural Heritage", Sketchfab blog, February 2020. https://sketchfab.com/blogs/community/sketchfab-launches-public-domain-dedication-for-3d-cultural-heritage/ [SS; UNREACHED]
23. Objaverse-XL README, undated. https://raw.githubusercontent.com/allenai/objaverse-xl/main/README.md [READ]
24. OpenGameArt FAQ. https://opengameart.org/content/faq [UNREACHED]
25. Microsoft Rocketbox LICENSE.md and README.md, 2020 to 2022. https://raw.githubusercontent.com/microsoft/Microsoft-Rocketbox/master/LICENSE.md [READ]
26. Mixamo FAQ, Adobe, undated. https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html [SS; UNREACHED]; Adobe community thread "Mixamo Copyright on Machine Learning" [SS]
27. "You can now sell MetaHumans, or use them in Unity or Godot", CG Channel, June 2025 [SS]; Unreal Engine EULA https://www.unrealengine.com/eula/unreal [SS; UNREACHED]
28. Fab listings "Electric Dreams Env", "City Sample Buildings", "City Sample Vehicles", "Lyra Starter Game", undated [SS]; production/research/aaa-street/2-EPIC-FREE-CONTENT.md, 1 October 2026 [project record]
29. "Crown copyright", Wikipedia, live article. https://en.wikipedia.org/wiki/Crown_copyright [READ]
30. "Open Government Licence", Wikipedia, live article. https://en.wikipedia.org/wiki/Open_Government_Licence [READ]
31. "Geograph Britain and Ireland", Wikipedia, live article. https://en.wikipedia.org/wiki/Geograph_Britain_and_Ireland [READ]
32. "Transport (typeface)", Wikipedia, live article. https://en.wikipedia.org/wiki/Transport_(typeface) [READ]
33. "Fonts", roads.org.uk, undated. https://www.roads.org.uk/fonts [SS; UNREACHED]; WhatDoTheyKnow FOI "What licence are the fonts used on the UK's signage released under?" [UNREACHED]
34. "Using Images from the Historic England Archive" and "Using the Collection Online" (England's Places), undated. https://historicengland.org.uk/images-books/archive/policies/using-images/ [SS; UNREACHED]
35. Google Fonts repository, `ofl/<font>/OFL.txt` for Jost, Fraunces, Oswald, Libre Baskerville, Courier Prime, UnifrakturMaguntia, Marcellus SC, Alfa Slab One, Bebas Neue, Abril Fatface, Josefin Sans, Overpass, Archivo, Libre Franklin, Old Standard TT. https://github.com/google/fonts/tree/main/ofl [READ]
36. Railway Sans README and LICENSE.txt (Greg Fleming, 2012). https://raw.githubusercontent.com/davelab6/Railway-Sans/master/LICENSE.txt [READ]
37. Liberation Fonts LICENSE. https://raw.githubusercontent.com/liberationfonts/liberation-fonts/main/LICENSE [READ]
38. "LIDAR Composite DTM 2019 – 1m", data.gov.uk [SS; UNREACHED]; Environment Agency LIDAR Open Data FAQ v5 (PDF, owenboswarva.com) [SS]
39. "Ordnance Survey", Wikipedia, live article (OS OpenData, 1 April 2010) [READ]; "OS Terrain 50 DTM", data.gov.uk [SS; UNREACHED]
40. "Commons:Licensing", Wikimedia Commons. https://commons.wikimedia.org/wiki/Commons:Licensing [UNREACHED]
41. "Quixel to Fab Transition FAQs", Fab support, undated [SS]; "Epic has made Megascans free to all", CG Channel, October 2024 [SS]
