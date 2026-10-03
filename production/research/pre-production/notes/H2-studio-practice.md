> **Helper evidence note** for the pre-production review of 3 October 2026, kept as written by a read-only helper. Corrections found on checking are listed in ../SOURCES.md, "Corrections to the helper notes"; where they differ, the numbered sections govern.

# H2: What professional studios settle in pre-production

Research date: 3 October 2026. About 30 minutes of searching.

## Read this first: what could and could not be reached

The network proxy in this environment allowed only three sources: **en.wikipedia.org**, **dev.epicgames.com** (Epic's Unreal and UEFN documentation) and **github.com / raw.githubusercontent.com**. Every games-industry site I tried was blocked: gamedeveloper.com (Gamasutra), gdcvault.com, kotaku.com, partner.steamgames.com, store.steampowered.com, unrealengine.com, fab.com (I did not try it after unrealengine.com was blocked), pegi.info, globalratings.com, sagaftra.org, ico.org.uk, medium.com, substack-hosted sites, wiki.polycount.com, dota2.com, joelburgess.com, level-design.org, leveldesignbook.com, grumpygamer.com, dl.acm.org, gbv.de, flylib.com, jahej.com, patricklipo.com, pcgamer.com and others. (List of UNREACHED pages at the end.)

So:
- **READ** means I fetched the page. The fetch tool returns an extraction made by a small model, not the raw page. I quote only text that the extraction marked as verbatim. Wikipedia is a secondary source; where it cites Kotaku and similar, the underlying article was UNREACHED.
- **SNIPPET** means I saw only the search engine's result text. That text is itself a summary written by the search tool, so a snippet's wording may not be the page's wording. Treat every SNIPPET as a lead to verify from the PC, not as evidence. Steam's AI rules, the Unreal EULA, the Fab licence, PEGI's own site and every GDC talk fall into this class.
- Primary sources I could actually read are Epic's documentation (for the engine side) and nothing else from the industry. Producers' writing, GDC talks and postmortems are all SNIPPET-only.

---

## 1. Pre-production as a phase: gates, exit criteria, what goes wrong when it is skipped

**What studios settle.** Pre-production ends at a go/no-go gate. At that gate the studio has (a) a playable proof that the game is worth making and (b) enough knowledge of cost to plan production as a pipeline.

- **Cerny's "Method" (D.I.C.E. Summit 2002).** READ via Wikipedia (Mark Cerny article, which cites a 2010 GDC Europe lecture). Pre-production is free-form and ends in a "publishable first playable". In the extraction's words, that version "does not need to be content-complete but provide enough to be used in playtesting", and "If the game at this state does not excite players, then the game idea should be set aside before too much effort is put into it." Production then uses "scheduled milestones and deliverables". A SNIPPET (VGC feature, via search) quotes Cerny: "Pre-production must be allowed to be a chaotic process."
- **Standard milestone names.** READ, Wikipedia "Video game development": First Playable; Alpha ("feature-complete but with bugs"); Code Freeze; Beta; Code Release; Gold Master. Pre-production outputs listed there: high concept, pitch, concept document (genre, features, setting, story, audience, platforms, schedule, marketing analysis, team requirements and **risk analysis**), the game design document, and a "production plan".
- **Vertical slice.** READ, Wikipedia: "a type of milestone, benchmark, or deadline, with emphasis on demonstrating progress across all components of a project". Its only cited source is Heather Maxwell Chandler, *The Game Production Toolbox* (2019), p. 68. The term is ambiguous. SNIPPET, Game Developer, "Why We Should Stop Saying 'Vertical Slices'" (undated): the phrase "has widely different meanings", and Ron Gilbert's critique (grumpygamer.com, UNREACHED) treats slices as defined up front by a plan.
- **What the slice contains.** SNIPPET, Game Developer blog "What you should take out of Pre-Production" (undated). The deliverables are the prototype or vertical slice "together with the pipeline definition and documentation". A slice "could be a single level containing art that is close to final, or at least representative of it, and where you have the core systems in place."
- **A gated sequence.** SNIPPET, Kellee Santiago's 10-step production plan (Game Developer, GDC China talk, date not seen): assess assets and constraints, prototype key features, then a vertical slice, then Alpha I (playable start to finish, many playtesters), then Alpha II (all features implemented and final).
- **Pre-production must establish cost.** SNIPPET, Clinton Keith, "Production Debt" (agilegamedevelopment blog, August 2008 per its URL; the blog's DNS failed, so the page is UNREACHED). Teams "never transition from pre-production to production as if a switch were thrown", and asset types transition at different rates. You measure production debt by making a small set of production-quality assets, measuring the effort and scaling it up. Example: if a demo level was 10% of a level, level cost = 10 × demo effort × number of levels. Production "relies on knowledge acquired during pre-production to build at the lowest cost".
- **Rule of thumb on length.** SNIPPET only: "at least 10–25% of the total development time". The search tool attributed this to Chandler's *Game Production Handbook*. I could not see the book, so the attribution is unverified.

**What goes wrong when it is skipped or fails (READ via Wikipedia; the underlying Kotaku articles are UNREACHED):**
- *Mass Effect: Andromeda* (BioWare, 2017). The planned procedural generation of many planets was abandoned. The team "found themselves behind schedule, and ended up building most of the game during the ensuing 18 months". The move to Frostbite meant building "all systems, tools, and assets from scratch". (Wikipedia citing Jason Schreier, Kotaku, 2017.)
- *Anthem* (BioWare, 2019). "no one at BioWare, including Hudson, had a firm idea of what that meant"; "Frostbite was not originally designed for the purposes that the team had in mind"; the E3 2017 demo "served as the basis for the game's reveal"; and "most of Anthem was effectively developed in the year prior to release". (Wikipedia citing Schreier, Kotaku, 2 April 2019.)
- The pattern in both: the gate was passed without a proven core or proven tools, so the real pre-production happened inside production, under crunch.

## 2. Vision, pillars and the game design document

- **GDD.** READ, Wikipedia "Game design document": a "living software design document" that is "continuously improved upon throughout the implementation of the project, sometimes as often as daily". Typical coverage: story and characters, gameplay, level design, art, sound and music, UI and controls, monetisation, audience, accessibility, development timeline. Cited books: Bates, *Game Design* (2nd ed., 2004); Bethke, *Game Development and Production* (2003); Oxland, *Gameplay and Design* (2004).
- **The classic structure.** SNIPPET: Tim Ryan, "The Anatomy of a Design Document", Gamasutra. Part 1 (concept and proposal) is dated 19 October 1999. Part 2 (functional and technical specifications) is dated 17 December 1999. Snippet quote: "the purpose of design documentation is to express the vision for the game, describe the contents, and present a plan for implementation."
- **Pillars.** SNIPPET, Game Developer, "Agile Game Development part 2: Design Pillars" (Janusz Tarczykowski, undated). Pillars "should emphasize emotions, what players will experience, and they usually shouldn't be concrete features". It cites Charlie Cleveland's GDC talk "The Design of Subnautica" and gives 3 to 5 pillars as the norm. Its example is The Last of Us, with Crafting (scarce ammo, items in the world) and Story. Other SNIPPETs list God of War (2018) pillars as "Combat, Father & son, Exploration". The GDC 2019 combat talk PDF on media.gdcvault.com is UNREACHED. Patrick Lipo, "Making the Rules: Pillars and Razors" (9 June 2008 per its URL) is UNREACHED and was seen as a title only.
- **When.** The pillars and the GDD's stable core exist before the production gate. A SNIPPET from a producer's guide (nastyrodent.com, undated) calls pillars "the scope razor": every later feature request is measured against them.

## 3. The art bible

**Typical sections** (SNIPPETs only, mostly student examples and one producer's blog; no studio primary was reachable):
- overall style;
- characters (proportions, expressions, poses, scale comparison, clothes, palette);
- environment;
- colour palette;
- camera;
- level of detail and polygon counts;
- "technical guidelines: rules and formats each artistic asset should have".

One snippet describes the bible as defining "proportions, color logic, silhouette rules, material treatment, and lighting intent".

**Real studio examples (all SNIPPET; the primary pages are UNREACHED):**
- **Riot Games, "Defining the Rift's Visual Style"** (League of Legends dev blog; 2014 per a fan-site snippet, with a PDF mirrored on polycount). Its principles: a timeless style "anchored in reality"; gameplay clarity ("minimizes visual clutter"); and a visual hierarchy in which the map frames the champions so that characters stand out.
- **Valve, Dota 2 Workshop guides.** Valve published a Character Art Guide, a Texture Guide and per-hero technical requirements, which work as an outsourcing kit for community artists. Per the snippet: budgets "always refer to triangles"; per-slot limits per LOD (e.g. Visage head LOD0 3,000 and LOD1 1,200 triangles); hero plus items textures at most 1024×512.
- **Valve, Team Fortress 2.** A published paper on illustrative rendering and silhouette readability (NPAR 2007, per the snippet).
- **Wildfire Games, 0 A.D. Art Design Document.** Texture sizes by asset tier and rigs capped at 25 bones.
- **Revolutionary Games, Thrive visual style guide.** Organelles at 300 triangles, 512×512 textures.

**The engine vendor's equivalent of a bible's technical section** (READ, Epic, "Fortnite-Ready Assets Best Practices", current docs, undated):
- units: "Centimeters (1 unit is equal to 1 cm)";
- grid: "512 cm";
- player: "192 cm tall";
- Z up, DirectX normals;
- polygon budgets by complexity and size (shown below in section 5).

**Pattern.** A studio art bible pairs look rules (shape language, palette, silhouette, hierarchy, lighting intent) with hard technical numbers (triangles per class, texture sizes, scale and grid). It exists before production art starts, and outsourcing depends on it.

## 4. The asset list, production methods per family, outsourcing kits and modular kits

- **Master asset list.** No studio primary was reachable. SNIPPET, rpgmaker.net, "Game Development Project Management using Spreadsheets" (undated): a resource task list groups every asset by category. Its columns are ID, Name, Description, Who, When requested, Received, Cost (estimated), Cost (actual), Paid?, Notes. Clinton Keith's production-debt method (section 1) is how the list is costed: a measured cost per asset family times the count.
- **Production method per family.** No primary text was found that names this as a document. The evidence points to it being the output of "pipeline definition" in pre-production (the Game Developer blog in section 1) and to Keith's point that each asset type transitions to production separately, once its pipeline is proven.
- **Outsourcing kit.** SNIPPETs only, all from outsourcing vendors' blogs (rocketbrush.com, n-ix, vsquad.art, gameartservices.com; dates not seen). A brief contains:
  - the asset list with priority and short descriptions;
  - technical requirements per asset (polycount, texture resolution, maps required, file format, engine);
  - the style guide with do's and don'ts;
  - "approved concepts, in-engine screenshots, lighting conditions, camera framing, scale references, material examples, and one or more benchmark assets";
  - review owner and feedback process;
  - source-file expectations, IP ownership terms and NDA.

  For modular kits, one example spec reads "All floor tiles are 4×4 units. All walls are 4 units wide and 3 units tall. Doorways are 2 units wide and 2.5 units tall."
- **Modular kits.** SNIPPET: Joel Burgess, "Skyrim's Modular Level Design", GDC 2013 Level Design in a Day (blog transcript April 2013 per its URL; UNREACHED). Kits are "contextual systems snapped to grids" that are "more than a sum of their parts" and are "the primary building blocks of level design at Bethesda Game Studios". Epic's Fortnite-ready rules (READ) fix the grid at 512 cm, which is the vendor's version of the same idea.

## 5. Technical design document and performance budget

- **TDD contents.** SNIPPETs: target platforms and hardware; target frame rates; memory budgets per platform; loading-time limits; draw-call ceilings; system architecture. Tim Ryan's Part 2 (17 December 1999) covers "functional and technical specifications"; I saw the title only. A SNIPPET of AltDevBlogADay, "Planning Memory Budgets (Part 1)" (1 September 2011 per its URL; UNREACHED) describes the method: a table of platforms with available memory, the game broken into modules, and budgets calculated per module.
- **Frame-time targets.** READ, Epic, "Introduction to Performance Profiling and Configuration" (UE 5.8): "applications will target 30, 60, and 120 frames per second when considering their performance budget and target hardware", and "there is no substitute for profiling directly on your target hardware. The longer you go without testing on your hardware, the more likely that bugs will emerge that you are not aware of." The page gives no per-system millisecond split. SNIPPET from Epic's Niagara docs: there are budget variables in milliseconds per thread for effects (fx.Budget.GameThread, fx.Budget.RenderThread). As the budget is approached, effects "scale down more and more aggressively to remain in budget".
- **Per-asset budgets** (READ, Epic Fortnite-ready):
  - simple objects: small 400, medium 900, large 2,500 polygons;
  - medium objects: 700 / 2,000 / 6,000;
  - complex objects: 1,200 / 4,000 / 9,000;
  - "three LODs (LOD0, LOD1 and LOD2)", "Each LOD level should be half the polygons of the previous level";
  - "Limit your mesh to 10 UCX collision meshes or less";
  - textures "2k or less", powers of two.
- **Engine guidelines** (READ, Epic, "Performance Guidelines for Artists and Designers", UE 4.27):
  - combine meshes to "300+ per element" triangles;
  - LODs should reduce "vertex count by at least 2x";
  - texture cost "DXT1 is 4 bits per pixel, DXT5 is 8 bpp, ARGB uncompressed is 32 bpp";
  - "Never disable mip maps if the texture can be seen in a smaller scale";
  - light cost from static (cheapest) through stationary to dynamic.
- **Draw calls.** READ, Epic, "Guidelines for Optimizing Rendering for Real-Time" (UE 5.8, mobile and HMI context): "A good target for draw calls in an optimized scene is roughly 700 on a Galaxy Tab S6, and less than 500 on lower-end hardware."
- **How budgets are policed.**
  - READ, Epic UEFN "Memory Management". There is a hard content budget, enforced at publish: "if any area in your level exceeds 100,000, you will not be able to publish your island". Memory is computed at cook time per cell. The advice is "In a forest made of 100 trees, use 5 variations and duplicate them around instead of using 100 unique trees".
  - READ, Epic "Data Validation" (UE 5.8). Validators can check "name conventions", "space/performance budgets" and dependencies. Validation runs "on asset save (enabled by default)" and in CI via `UnrealEditor-Cmd.exe <PROJECT>.uproject -run=DataValidation`.
  - READ, Epic "Low-Level Memory Tracker": "Every memory allocation made by the Engine (including game code) is assigned a tag value identifying the category to which it belongs". This is the tool for checking a memory budget per category; the page does not set budgets.
  - SNIPPET, Epic: Asset Audit (exports per-asset data to CSV) and Size Map (disk or memory size of an asset and its dependencies).
- **When.** Budgets come from the target hardware and frame rate, which are set before production. They are checked on that hardware from the start (Epic's warning above) and enforced by tools at save, in CI and at cook or publish.

## 6. Pipeline and tools

- **Source control first.** READ, Epic, "Resources for Scaling Your Unreal Engine Team" (UE 5.8): "Setting up one of these for your project should be the first thing you do before anyone starts working on assets or code." The options named are Perforce, Git with Git LFS, Subversion and Diversion. Build automation is UAT BuildCookRun, BuildGraph or Horde ("a robust continuous integration suite"). A shared Derived Data Cache spares other users from recompiling or re-cooking.
- **Naming.** READ, Epic, "Recommended Asset Naming Conventions" (UE 5.8): format `[AssetTypePrefix]_[AssetName]_[Descriptor]_[OptionalVariantLetterOrNumber]`. "For large projects, we recommend you establish a common naming convention for individual Assets early in development." Prefixes include SM_, SK_, M_, MI_, T_, BP_, WBP_, ABP_ and FXS_.
- **Style guide.** READ, GitHub, Allar "ue5-style-guide" (community, widely used; repo undated). The format is `Prefix_BaseAssetName_Variant_Suffix`. Goal: the project should "look like a single person created it, no matter how many people contributed". On folders: "the directory structure style of a project should be considered law".
- **DCC to engine conventions.** READ, Epic, "FBX Static Mesh Pipeline" (UE 5.8): collision is identified by name, as `UBX_`, `UCP_`, `USP_` or `UCX_[RenderMeshName]_##`. "A Convex object can be any completely closed convex 3D shape". LODs can be imported from the DCC file.
- **Automated checks.** Data Validation on save and in CI (section 5). BuildGraph and Horde for the build pipeline (SNIPPET of Epic pages: BuildGraph "describes a parameterized dependency graph between nodes that produce artifacts").

## 7. Legal and licensing

**Engine and middleware licences.**
- Unreal: READ via Wikipedia, "5% of revenues over US$1 million", waived for games sold exclusively on the Epic Games Store. SNIPPET (gamefromscratch, cgchannel, October 2024): from 1 January 2025, "Launch Everywhere with Epic" cuts the rate to 3.5% for games released on the Epic Games Store no later than on other stores. The EULA page itself is UNREACHED.
- A licence changed underneath studios. READ via Wikipedia: Unity announced a per-install Runtime Fee on 12 September 2023, revised it on 22 September 2023, and Innersloth and Mega Crit announced moves to other engines. It was cancelled in September 2024. This is the standard games example of why middleware terms go on the risk register.

**Asset licences.** SNIPPET only (fab.com/eula UNREACHED): the Fab Standard License allows commercial use inside projects. It forbids standalone redistribution and requires end users to be restricted "from extracting or otherwise using content outside of the project". It also says you "shall not collect, aggregate, mine, scrape, or otherwise use content in datasets utilized by generative AI programs, in the development of generative AI programs, or as inputs to generative AI programs". The last clause matters for any pipeline that feeds purchased assets into AI tools, and needs checking on the real page. I found no reachable studio source describing a licence-tracking register; the asset-list columns above (Who, Cost, Paid?) are the nearest.

**Voice actors, consent and AI voices.**
- READ via Wikipedia: the SAG-AFTRA video game strike ran from 26 July 2024 to 9 July 2025. The agreement, ratified 9 July 2025 with 95.04% approval, requires consent for digital replicas, disclosure, comparable compensation, and the right to suspend consent during strikes.
- SNIPPET (NBC News and Axios, January 2024): SAG-AFTRA's deal with Replica Studios to license digital voice replicas.
- UK, SNIPPET:
  - Equity (FIA post, 17 February 2025): performer contracts "should not constitute a lawful basis" to train AI or generate replicas.
  - Equity members voted to refuse on-set digital scans (Deadline, December 2025).
  - Equity's 2026 TUC motion seeks UK personality rights (BroadwayWorld, 15 September 2026).
  - None of these pages was read.

**AI-generated content: Steam's rules** (primary Steamworks pages UNREACHED; everything below is READ via Wikipedia or SNIPPET):
- READ, Wikipedia "Steam (service)". In January 2024 Valve began "requiring games that did use content from generational AI to disclose this on the game's store page, including methods that the developers used to assure the AI engines did not generate illegal content."
- SNIPPET (Game World Observer and GeekWire, 10 January 2024). There are two categories:
  - **Pre-Generated** (made with AI during development): the developer promises no "illegal or infringing content".
  - **Live-Generated** (made while the game runs): the developer describes its guardrails against illegal content.

  Players can report illegal live-generated content through the overlay. "Adult Only Sexual Content that is created with Live-Generated AI" cannot be released.
- SNIPPET (PC Gamer and others, 16–17 January 2026): the disclosure form now focuses on content that "ships with your game, and is consumed by players" plus marketing material. "Efficiency gains through the use of these tools is not the focus of this section."
- Relevance: characters who talk live through a model are Live-Generated content under this scheme. The exact current wording must be read on the Steamworks Content Survey page from a PC that can reach it.

**EU AI Act.** READ via Wikipedia: transparency obligations for "limited-risk" systems, "ensuring users are informed that they are interacting with an AI system". This includes systems that "generate or manipulate images, sound, or videos (like deepfakes)". Most obligations apply 24 months after entry into force on 1 August 2024. I did not read the Act's own text.

**Real people, names and trademarks.** SNIPPET (Justia, CBC, UPI; ruling 29 March 2018): *Lohan v. Take-Two* (New York Court of Appeals). The claim failed because the character was "not reasonably identifiable as plaintiff", but the court held that a computer-generated image may be a "portrait" under New York civil rights law. That is US law. No UK case was researched; the UK has no general personality right, which is why Equity is campaigning for one (SNIPPET). Trademark cases such as *AM General v. Activision* (Humvee) were not reached.

**Age ratings.**
- PEGI. READ via Wikipedia:
  - ratings 3, 7, 12, 16 and 18;
  - descriptors: bad language, discrimination, drugs, fear, gambling, sex, violence, in-game purchases;
  - "the legally enforceable system for game classification in the UK since 30 July 2012", administered by the Video Standards Council.

  The extraction also reported PEGI criteria changes "as of July 2026" (loot boxes PEGI 16, and so on) and the 2025 reclassification of *Balatro* to PEGI 12. These are unverified; pegi.info is UNREACHED.
- ESRB. READ via Wikipedia: since April 2011 digital games use the multiple-choice "Short Form". Descriptors include Alcohol Reference, Use of Alcohol, Tobacco Reference, Use of Tobacco, Simulated Gambling and Real Gambling.
- IARC. READ via Wikipedia: one questionnaire produces ratings for several boards (ESRB, PEGI, USK, ClassInd, Australia and others) at no cost to the developer. The storefronts named include Google Play, Nintendo eShop, PlayStation Store and the Epic Games Store; "Steam is not listed as a participant". What Steam itself requires for ratings was not established.

**Privacy.** READ via Wikipedia: the UK ICO's Age Appropriate Design Code ("Children's Code") applies to "any internet-connected product or service that is likely to be accessed by a person under the age of 18", including online games. It took effect on 2 September 2020, with enforcement from September 2021. Privacy duties for sending players' speech or text to an AI service under UK GDPR were not researched further.

## 8. Budget (money) and schedule

All of this is SNIPPET; no producer primary was reachable.

- **Money.** Vendor and consultancy blogs (generalistprogrammer.com, gamedevproducer.com, juegostudio.com; dates not seen) say team costs are "60–80%" of a budget. Their rule of thumb for burn is "$10–15k per developer per month" including overhead. Chandler's *Game Production Handbook* (3rd edition listing on O'Reilly) has a chapter on budgets and schedules; it was not read.
- **Buffers.** Rob Sandberg, Production Alchemist, "How to Build a Game Milestone Schedule"; gamedevproducer.com; PMI, "The 20-percent solution" (all undated):
  - "If your estimate doesn't include a buffer of at least 20 to 25 percent, your estimate is incomplete";
  - "15 percent for well-understood work, 30 to 40 percent for anything involving new technology or first-time tasks";
  - "40 to 50 percent" for teams that have never shipped;
  - buffer at the milestone or gate level, not padded into each task;
  - declare it openly, e.g. "We have three weeks of contingency before certification. We're not spending it unless something in the critical path goes wrong."
- **Content cost.** Clinton Keith's production-debt method (section 1): cost per asset family measured during pre-production, multiplied by the asset list.
- READ, Wikipedia "Risk register": a "Contingency (budget allocated)" field is part of the standard register. This is where money buffers are tied to named risks.

## 9. The risk register

- **Columns.** READ, Wikipedia "Risk register", definition from ISO Guide 73:2009, a "record of information about identified risks":
  - category;
  - ID;
  - description;
  - impact (integer scale);
  - probability (integer scale);
  - score ("product of probability × impact");
  - mitigation steps;
  - contingent response;
  - contingency (budget);
  - trigger.

  The page does not state how often a register is reviewed.
- **Games practice.** SNIPPET, Game Studio Unlocked (Substack), "Risk registers for indie game studios" (undated):
  - categories: product risk, scope and execution risk, financial risk;
  - columns: description, likelihood, impact, mitigation, owner;
  - "trigger conditions" (what would show the risk is happening);
  - a total score of impact × probability "out of 25" (two 1–5 scales);
  - review "at least once a month for most risks", more often for risks being actively worked.

  Other SNIPPET-only titles: Rob Sandberg, "Agile Risk Management in the Game Studio"; Joseph Kim, "'Key Risks' Based Game Pre-production" (gamemakers.com), which organises pre-production around retiring the key risks; jennsand.com, "A game producer's guide to setting up a risk register to track your fears"; Marc Schmalz et al., "Risk Management in Video Game Development Projects" (IEEE Xplore 6759136; PDF UNREACHED).
- **Games-industry examples of risks that materialised** (READ via Wikipedia):
  - new engine and tools (Andromeda, Anthem);
  - an unproven core feature (Andromeda's procedural planets);
  - leadership and vision (Anthem);
  - a vendor licence change (Unity Runtime Fee, 2023);
  - performer availability and AI terms (the SAG-AFTRA strike, 2024–25).

## 10. Definition of done for an asset

- READ, Wikipedia "Scrum": "A team's 'definition of done' is a checklist of what needs to be completed for work to be considered 'done'". Per the extraction, it should evolve toward real release requirements as the team matures.
- SNIPPET, Clinton Keith, "Defining Done" (October 2013 per its URL; UNREACHED). Non-functional requirements include a smooth playable frame rate, running on all target platforms, streaming off disc cleanly, meeting coding standards, and "the assets are appropriately named and fit within budgets".
- SNIPPET (a student team's GitHub wiki, so not a studio): polycount within limit, pivot in the right place, UVs ready, named per the naming convention.
- **What an engine-side asset "done" checklist looks like when assembled from Epic's READ pages:**
  - named with the type prefix;
  - scale and grid per the project's metrics;
  - triangle count within its class budget;
  - LOD0–LOD2 present, each roughly half the previous;
  - collision present (UCX_ etc., at most 10 hulls);
  - textures powers of two, within the size cap, with mips;
  - passes Data Validation on save and in CI;
  - fits the memory or cook budget.
- **Gap.** I found no reachable studio source that lists "licence recorded" or "approved by art director" as DoD lines. They appear in outsourcing briefs (IP ownership terms, review owner) only as SNIPPET.

---

## Rules of thumb found (with their status)

| Rule | Source status |
|---|---|
| End pre-production with a playable proof that excites players, or set the idea aside (Cerny, 2002) | READ via Wikipedia |
| Measure the cost of each asset family from a few production-quality samples, then scale (Keith, 2008) | SNIPPET |
| Set up source control before anyone starts on assets or code | READ (Epic) |
| Fix the naming convention early | READ (Epic) |
| Profile on the target hardware from the start | READ (Epic) |
| Budgets per asset class, with LODs halving each level | READ (Epic Fortnite-ready) |
| Enforce budgets by tool at save, in CI and at publish or cook | READ (Epic Data Validation, UEFN memory) |
| Schedule buffer of at least 20–25%, more for new technology; held at milestone level and declared openly | SNIPPET |
| Pre-production at 10–25% of total time | SNIPPET, attribution unverified |
| Risk score = likelihood × impact (1–5 each); owner and trigger per risk; review at least monthly | SNIPPET (games) plus READ (Wikipedia columns) |

## Evidence gaps

- No GDC talk, Gamasutra article, Kotaku report or studio postmortem could be read; all are SNIPPET or UNREACHED.
- Steam's current AI disclosure text, the Unreal EULA, the Fab licence and PEGI's own criteria must be read from the PC before anything relies on them.
- No studio primary on a master asset list's columns, a licence-tracking register, or an asset DoD that includes licence and approval lines.

---

## Sources

### READ
| URL | Date | Notes |
|---|---|---|
| https://en.wikipedia.org/wiki/Video_game_development | live article, read 2026-10-03 | milestones, pre-production outputs |
| https://en.wikipedia.org/wiki/Vertical_slice | live, read 2026-10-03 | cites Chandler 2019 p.68 |
| https://en.wikipedia.org/wiki/Game_design_document | live, read 2026-10-03 | |
| https://en.wikipedia.org/wiki/Mark_Cerny | live, read 2026-10-03 | Method, 2002 |
| https://en.wikipedia.org/wiki/Mass_Effect:_Andromeda | live, read 2026-10-03 | cites Kotaku 2017 |
| https://en.wikipedia.org/wiki/Anthem_(video_game) | live, read 2026-10-03 | cites Kotaku 2019-04-02 |
| https://en.wikipedia.org/wiki/Steam_(service) | live, read 2026-10-03 | AI policy 2023/2024 |
| https://en.wikipedia.org/wiki/International_Age_Rating_Coalition | live, read 2026-10-03 | |
| https://en.wikipedia.org/wiki/Pan_European_Game_Information | live, read 2026-10-03 | 2026 changes unverified |
| https://en.wikipedia.org/wiki/Entertainment_Software_Rating_Board | live, read 2026-10-03 | |
| https://en.wikipedia.org/wiki/2024–2025_SAG-AFTRA_video_game_strike | live, read 2026-10-03 | |
| https://en.wikipedia.org/wiki/Risk_register | live, read 2026-10-03 | ISO Guide 73:2009 |
| https://en.wikipedia.org/wiki/Scrum_(software_development) | live, read 2026-10-03 | DoD |
| https://en.wikipedia.org/wiki/Unity_(game_engine) | live, read 2026-10-03 | Runtime Fee |
| https://en.wikipedia.org/wiki/Unreal_Engine | live, read 2026-10-03 | 5% over $1M |
| https://en.wikipedia.org/wiki/Artificial_Intelligence_Act | live, read 2026-10-03 | transparency |
| https://en.wikipedia.org/wiki/Age_appropriate_design_code | live, read 2026-10-03 | |
| https://en.wikipedia.org/wiki/Art_pipeline | live, read 2026-10-03 | little of use |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine | undated, UE 5.8 docs | |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/recommended-asset-naming-conventions-in-unreal-engine-projects | undated, UE 5.8 | |
| https://dev.epicgames.com/documentation/unreal-engine/setting-up-your-production-pipeline-in-unreal-engine | undated, UE 5.8 | index page only |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine | undated, UE 5.8 | |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/guidelines-for-optimizing-rendering-for-real-time-in-unreal-engine | undated, UE 5.8 | mobile/HMI numbers |
| https://dev.epicgames.com/documentation/en-us/uefn/memory-management-in-unreal-editor-for-fortnite | undated | |
| https://dev.epicgames.com/documentation/fortnite/fortniteready-assets-best-practices-in-fortnite?lang=en-US | undated | |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/performance-guidelines-for-artists-and-designers?application_version=4.27 | undated, UE 4.27 | |
| https://dev.epicgames.com/documentation/unreal-engine/resources-for-scaling-your-unreal-engine-team | undated, UE 5.8 | |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/using-the-low-level-memory-tracker-in-unreal-engine | undated, UE 5.8 | |
| https://dev.epicgames.com/documentation/unreal-engine/fbx-static-mesh-pipeline-in-unreal-engine?lang=en-US | undated, UE 5.8 | |
| https://dev.epicgames.com/documentation/unreal-engine/setting-up-collisions-with-static-meshes-in-unreal-engine | undated, UE 5.8 | did not contain the prefixes |
| https://github.com/Allar/ue5-style-guide and https://raw.githubusercontent.com/Allar/ue5-style-guide/main/README.md | undated repo | |

### SNIPPET only (search-result text; page not seen)
| URL | Date |
|---|---|
| https://www.gamedeveloper.com/blogs/what-you-should-take-out-of-pre-production | undated |
| https://www.gamedeveloper.com/production/kellee-santiago-s-10-step-video-game-production-plan | undated |
| https://www.gamedeveloper.com/design/why-we-should-stop-saying-vertical-slices- | undated |
| https://www.videogameschronicle.com/features/who-is-mark-cerny/ (Cerny quote) | undated |
| https://blog.agilegamedevelopment.com/2008/08/production-debt.html | Aug 2008 per URL (DNS failed: also UNREACHED) |
| https://blog.agilegamedevelopment.com/2013/10/defining-done.html | Oct 2013 per URL (DNS failed: also UNREACHED) |
| https://www.gamedeveloper.com/design/the-anatomy-of-a-design-document-part-1-documentation-guidelines-for-the-game-concept-and-proposal | 19 Oct 1999 (per snippet) |
| https://www.gamedeveloper.com/business/agile-game-development-part-2-design-pillars | undated |
| https://nastyrodent.com/pre-production-in-game-development/ and https://nastyrodent.com/game-art-bible/ | undated |
| http://wiki.polycount.com/wiki/Defining_the_Rift%E2%80%99s_Visual_Style ; https://www.surrenderat20.net/2014/11/red-post-collection-defining-rifts.html | 2014 (per fan-site URL) |
| https://www.dota2.com/workshop/requirements/visage ; https://support.steampowered.com/kb/9814-QSHK-8085/dota-2-workshop-item-model-requirements | undated |
| https://rpgmaker.net/articles/1413/ | undated |
| https://rocketbrush.com/blog/game-art-outsourcing-complete-guide ; https://vsquad.art/blog/how-to-outsource-game-art-a-guide-to-workflow-and-estimates ; https://gameartservices.com/blog/game-environment-art-outsourcing | undated |
| https://www.gamedeveloper.com/design/skyrim-s-modular-approach-to-level-design ; http://blog.joelburgess.com/2013/04/skyrims-modular-level-design-gdc-2013.html | GDC 2013 |
| https://jahej.com/alt/2011_09_01_planning-memory-budgets-part-one.html | 1 Sep 2011 per URL |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/niagara-debugger-for-unreal-engine (fx.Budget) | undated |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/buildgraph-for-unreal-engine ; https://dev.epicgames.com/documentation/en-us/unreal-engine/horde-build-automation-for-unreal-engine | undated |
| https://gamefromscratch.com/unreal-engine-launch-everywhere-with-epic/ ; https://www.cgchannel.com/2024/10/epic-games-to-cut-royalty-rate-on-unreal-engine-games/ | Oct 2024 |
| https://www.fab.com/eula (Fab Standard License text via snippet) | undated |
| https://gameworldobserver.com/2024/01/10/steam-ai-games-new-rules-pre-generated-live-generated ; https://www.geekwire.com/2024/valve-software-reveals-new-rules-for-ai-powered-game-development-on-steam/ | 10 Jan 2024 |
| https://www.pcgamer.com/software/ai/steam-updates-ai-disclosure-form-to-specify-that-its-focused-on-ai-generated-content-that-is-consumed-by-players-not-efficiency-tools-used-behind-the-scenes/ | Jan 2026 (16–17 Jan per snippets) |
| https://www.nbcnews.com/tech/video-games/sag-aftra-replica-studios-voice-actors-video-games-rcna133162 | Jan 2024 |
| https://fia-actors.com/2025/02/17/enforce-performers-data-rights-in-ai-equity-tells-entertainment-bosses/ | 17 Feb 2025 |
| https://deadline.com/2025/12/equity-british-actors-vote-digital-scand-ai-dispute-1236652329/ | Dec 2025 |
| https://www.broadwayworld.com/westend/article/Equity-Calls-for-Personality-Rights-for-Performers-Following-Louise-Haigh-AI-Comments-20260915 | 15 Sep 2026 |
| https://law.justia.com/cases/new-york/court-of-appeals/2018/24.html | 29 Mar 2018 (ruling) |
| https://gamestudiounlocked.substack.com/p/risk-registers-for-small-indie-studios | undated |
| https://www.productionalchemist.com/p/production-101-13-how-to-build-a | undated |
| https://gamedevproducer.com/posts/how-to-estimate-game-development-costs/ | undated |
| https://www.pmi.org/learning/library/accurate-estimates-20-percent-solution-9805 | undated |
| https://www.oreilly.com/library/view/the-game-production/9781449688097/part005.xhtml (Chandler, 3rd ed.) | book listing |

### UNREACHED (blocked by proxy, DNS failure or 404; used as evidence for nothing)
- https://partner.steamgames.com/doc/gettingstarted/contentsurvey (blocked)
- https://store.steampowered.com/news/... (blocked)
- https://web.archive.org/... (fetch refused)
- https://www.gamedeveloper.com/... (all pages; blocked)
- https://kotaku.com/the-story-behind-mass-effect-andromedas-troubled-five-1795886428 (blocked)
- https://www.gdcvault.com/... and https://media.gdcvault.com/gdc2019/presentations/Sheth_Mihir_EvolvingCombat.pdf (blocked)
- https://www.unrealengine.com/en-US/eula/unreal (blocked)
- https://pegi.info/page/pegi-age-ratings (blocked)
- https://www.globalratings.com/how-iarc-works.aspx (blocked)
- https://www.sagaftra.org/... (blocked)
- https://ico.org.uk/... (blocked)
- https://docs.unity3d.com/... (blocked)
- https://medium.com/@mateuszjanczewski/producers-diary-the-seven-deadly-sins-of-pre-production-81d58d0529c4 (blocked)
- https://blog.agilegamedevelopment.com/... (DNS failure)
- http://wiki.polycount.com/wiki/Art_Bible (blocked)
- https://www.gamemakers.com/p/key-risks-pre-production (blocked)
- https://bpb-us-e1.wpmucdn.com/.../Risk-management-in-video-game-development-projects.pdf (blocked)
- https://www.patricklipo.com/2008/06/09/pillars-and-razors/ (blocked)
- https://jennsand.com/advice/risk-register/ (blocked)
- https://www.dota2.com/workshop/requirements/visage (blocked)
- https://grumpygamer.com/vertical_slice/ (blocked)
- https://book.leveldesignbook.com/process/blockout/metrics/modular (blocked)
- https://level-design.org/?p=1643 (blocked)
- https://blog.joelburgess.com/2013/04/skyrims-modular-level-design-gdc-2013.html (blocked)
- https://dl.acm.org/doi/10.1145/3321388.3321389 (blocked)
- https://www.gbv.de/dms/ilmenau/toc/571145469.PDF (blocked)
- https://jahej.com/... (blocked)
- https://flylib.com/... (blocked)
- https://www.gamesindustry.biz/, https://www.eurogamer.net/, https://www.pcgamer.com/ (blocked or refused)
- https://en.wikipedia.org/wiki/Lohan_v._Take-Two_Interactive_Software,_Inc. and https://en.wikipedia.org/wiki/AM_General_v._Activision_Blizzard (404: wrong titles guessed)
