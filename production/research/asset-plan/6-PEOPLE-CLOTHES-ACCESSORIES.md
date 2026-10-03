# People, clothes and accessories: how they are made, what is free, and the one proof (asset-plan note 6, 3 October 2026)

A research helper, read only, about thirty minutes of searching after reading the project's own research. 24 web searches. Families: (A) people, (B) clothes, (C) accessories.

**Marks.** [READ] read at the source today. [SS] search summary only. [I] my inference. UNREACHED: the page refused me. "(project: file)" means a fact from the project's own research, with the mark it carried there; I did not re-read it at source. An unreached page is never evidence.

**Reachable today.** WebFetch opened dev.epicgames.com and en.wikipedia.org only. Refused: metahuman.com, unrealengine.com, helpx.adobe.com, commons.wikimedia.org, static.makehumancommunity.org. curl reached nothing (github.com now answers 403 to this session). Fab, Sketchfab, Poly Haven and archive.org were not tried by fetch, per the brief; they are search summaries only.

---

## In short

1. **The NoAI rule, applied as written, removes most of Epic's own free people content, and that collides with two live rulings.** Epic's Game Animation Sample (GASP) carries "Allows usage with AI: No" (project: natural-idles, read at its Fab page on 1 October). Search summaries say the same of Epic's MetaHuman Crowd Sample, City Sample Crowds and Epic's MetaHuman Techwear Outfit, and of a resizable "Sweater" wardrobe item [SS]. Every Megascans record carries `isAiForbidden: true` (project: GOODS-2026-10-03). Yet the 3 October list builds the proof frame's people from GASP (item 11), and the 1 and 3 October rulings dress people in "Epic's plainest garments, re-coloured". One ruling is needed (Decision 1). Until then, nothing new is taken from those sources.
2. **The engine itself is clean.** The MetaHuman plugin is part of Unreal from 5.6 and comes under the Unreal Engine EULA, not a Fab listing [SS]. Its bodies, faces, Python API, 31 locomotion clips and the 5.8 Crowd plugin and Collections are usable. MetaHuman's AI clause forbids training, testing or building a database with MetaHumans. It allows "workflows that incorporate artificial intelligence technology" [SS]. Our agent-driven pipeline fits within that, with one gap: if "Help improve Claude" is on in Jafar's account, the MetaHuman renders our sessions send to Claude may be used to train Anthropic's models [SS]. Switching it off closes that (Decision 3).
3. **How AAA games make crowds of period people is already well researched** (wardrobe-at-scale, casting/notes/crowd.md, natural-idles). Every one uses the same method: a few bodies and heads; garments in fixed slots, fitted to every body; variety from material, colour, accessories and scale; a written recipe for each kind of person; walks played out of step. I add only Mafia: The Old Country, Still Wakes the Deep and Watch Dogs: Legion, below.
4. **Looking at the Hook sheet itself changes what the crowd needs.** Its people are older men and women in dark wool coats and jackets, nearly all seen from behind or side-on at 8 to 40 m [READ, the image]. At those distances a lapel is 4 to 14 pixels (project: RUBRIC.md). So the crowd's coats are judged on back, shoulders, length, colour and drape, not on the lapel roll that blocks every tailored garment so far. A crowd-distance rubric would let the crowd be dressed before tailoring is solved for the principals at talk distance (Decision 2) [I].
5. **Accessories have almost no allowed free source.** Fab accessories and Megascans are NoAI. Sketchfab's lighters are CC-BY or real brands [SS]. Poly Haven has one vintage suitcase [SS], and MakeHuman lists CC0 glasses and hats that nobody here has seen [SS]. But accessories are the cheapest thing we make. Four already passed blind review (Sheila's handbag and spectacles, Darren's belt and pager), all from `tools/meshgen/blender/model_accessory.py`. Make them as parametric Blender kits on sockets.
6. **The variety needed for the first street is small.** It needs 14 principals, about 30 regulars and 30 to 40 passers-by, with 10 to 25 people on screen at once [I]. The Hook sheet shows about ten, and the KCD2 fountain frame about ten. The town later needs 200 to 500 on screen. Spend the variety on head, hair, headwear and the outer layer's colour, where eyes go (project: crowd.md, Clone Attack and Eye-catching Crowds).
7. **The one proof:** three passers-by from one recipe ("older man, out on foot"), each with a different face, build, hair, coat cloth, headwear and hand item, and a different walk out of step. They walk in the proof view, side by side with the Hook sheet's two foreground men and the KCD2 fountain frame. Effort is about 8 to 14 builder-days, with the coat as the risk [I]. Nothing is multiplied before he approves it in the game.

---

## 0. What the project already knows (read, summarised, not repeated)

- **wardrobe-at-scale (1 Oct):**
  - Studios dress crowds from a few base garments in slots, fitted to every body, multiplied by material and recipe. City Sample uses 111 pieces on 6 bodies for 35,000 people. RDR2 uses 2 to 13 presets per type of townsperson. GTA V has 12 component slots and 5 prop slots. KCD has 16 layered slots.
  - The first street needs about 40 base garments, ten of them tailored outerwear. The town needs 60 to 70.
  - The ranked routes put Marvelous Designer first. That route has since failed and was stopped on 2 October.
- **free-garments (2 Oct, cloud and PC):** CLO's CONNECT gives a professional pattern for every one of the ten silhouettes, under a free commercial licence ruled allowed, with a revocable clause. They are patterns, not rigged garments, and draping them was stopped by his ruling of 2 October. Every free CGTrader garment carries "Royalty Free License (no AI)" and is not allowed.
- **plain-1990-clothes (1 Oct):**
  - What a northern port town wore in 1990, by age and sex.
  - Epic's free wardrobe items expose named colour slots settable from Python.
  - Archives to look at: Fryer, Thornton, Gill, Grant and Report Digital.
  - **Its licence line predates the NoAI rule** and must now be re-checked (section 1).
- **casting (24 and 28 Sept):**
  - Census shares for 30 regulars.
  - 12 to 16 crowd faces by age decade, with period traits in census proportions: moustaches on about a third of men aged 35 to 60, perms or sets on about half of women over 45, glasses on about a third.
  - Dress and bearing for eleven principals.
  - The no-children floor: briefs at 25 and over, crowd faces at 21 and over that read unmistakably adult, and an apparent-age test.
- **natural-idles (1 Oct) and townspeople-animation (30 Sept):**
  - 15 to 25 clips per sex.
  - Random start, a play rate between 0.9 and 1.1, no two neighbours on the same base idle.
  - Retarget offline. Move each body at its walk clip's own speed.
  - The C++ nodes already exist in 5.8.
  - **GASP's NoAI flag was read there and judged harmless.** The brief's rule of 3 October now says otherwise.
- **character-pipeline (25 to 29 Sept):**
  - The MetaHuman Python API: conform, landmarks, face coefficients, and body constraints with `request_auto_rigging` before export.
  - Hair: no curl parameter exists, so period hair is new groom geometry, made from Blender hair curves by script.
  - MPFB2 output is CC0.
  - Fab's curly grooms are NoAI.
- **clothing-pipeline/ACCESSORIES (30 Sept):**
  - Spectacles, handbag and pager go on sockets on `head`, `hand_r` and `pelvis`.
  - MetaHuman Creator has no eyewear slot.
  - Triangle budgets for each piece.
- **CLOTHES.md and RUBRIC.md (2 and 3 Oct):**
  - The fixed rubric and the game's viewing distances.
  - None of the ready-made suits screened qualifies: 247 of 387 Fab suit listings are NoAI, including every MetaHuman-rigged suit read.
  - Tailoring waits.

---

## 1. NoAI: the rule that now cuts across all three families

**What the words say.**
- Fab's own documentation [READ]: "The NoAI meta tag indicates that an asset must not be used for generative AI data collection."
- Fab's and Sketchfab's wider wording [SS]: tagged content may not be used "in datasets for, in the development of, or as inputs to generative AI programs".
- Our agents see these assets in rendered frames, and their scripts open the files. "As inputs to" plausibly covers that [I]. So the owner's strict reading is the safe one: never used, not even as a reference.

**What carries the flag, in my families:**

| Item (Epic or Fab) | What it is to us | NoAI? | Mark |
|---|---|---|---|
| Game Animation Sample (GASP) | Idles, walks, look-at: the proof frame's item 11 | **Yes**: "Allows usage with AI: No" | project: natural-idles, read at the listing 1 Oct |
| MetaHuman Crowd Sample | Epic's crowd example content | **Yes** | [SS] |
| City Sample Crowds | Heads, bodies, modern wardrobe; also "UE-Only" | **Yes** | [SS] |
| MetaHuman Techwear Outfit (Epic) | One of Epic's free resizable outfits | **Yes** | [SS] |
| "Sweater Metahuman Wardrobe cloth" (listing e785d5d1) | A resizable sweater; whether this is Epic's own sweater is unconfirmed | **Yes** | [SS] |
| Epic's other free wardrobe items (Jeans, Boots, Flats, T-shirts) | What people wear today as the stopgap | **Unknown**; likely, given the two above [I] | not seen |
| MetaHuman Clothing Construction Presets | Epic's bodies for authoring garments | Unknown | [SS], flag unseen |
| Fab grooms (AnnaLev "Curly Short") | Period perms | **Yes** | project: faces-and-hair |
| Every Megascans record | Bags, books, paper and textures | **Yes** (`isAiForbidden: true`) | project: GOODS-2026-10-03 |
| Fab MetaHuman accessories (e.g. "Glasses Tactic") | Spectacles and the like | **Yes**, by summary | [SS] |
| Fab suits at $40 or under | Tailoring | 247 of 387 Yes; every MetaHuman-rigged suit read | project: SCREENING-2026-10-02 |

**What is not a Fab listing, and so not tagged:**
- the MetaHuman plugin and its bundled content, part of the engine from 5.6 [SS];
- the 5.8 Crowd plugin and Collections (engine features);
- Mixamo;
- CC0 libraries (CC0 cannot carry NoAI: Fab's docs say NoAI cannot be combined with Creative Commons [READ]).

**The conflict.**
- DECISIONS.md, 3 October: "the people's poses from Epic's Game Animation Sample", and "his Fab list is in his library (… Epic's Game Animation Sample among it)".
- DECISIONS.md, 1 and 3 October: people wear "Epic's plainest garments, re-coloured".
- The brief of 3 October: NoAI is never used; "two ready-made suits were rejected on 3 October for exactly this".
- These cannot all stand. Decision 1 asks him which governs.

**Without NoAI assets, people can still be built from** [I]:
- the engine's MetaHuman locomotion: 31 clips on `metahuman_base_skel`, including walk starts and stops, plus one standing idle and the template idles (project: natural-idles, read in the 5.8 install);
- Mixamo idles, gestures and smoking (allowed, D46);
- garments that have passed our gate;
- our own grooms and accessories.

What is lost is GASP's 45 idles and 446 walks (a third party's count), and Epic's plain basics as an instant stopgap.

---

## 2. MetaHuman's AI clause, and whether our agent-driven pipeline is within it

**The clause.** Since 5.6, MetaHuman comes under the Unreal Engine EULA, section 6 [SS, the pages UNREACHED]. You may not "use, or permit others to use, MetaHuman digital characters and animation curves (or any rendered output thereof if crafted to replicate the functionality of MetaHuman) to build or enhance any database or training or testing any artificial intelligence, machine learning, deep learning, neural networks, or similar technologies". Epic's licensing page says MetaHumans may be used "in workflows that incorporate artificial intelligence technology" [SS]. It is free under US$1M revenue (allowlist).

**Our pipeline, line by line [I]:**

| What we do | Within the clause? |
|---|---|
| Agents drive MetaHuman Creator and Unreal by Python, export bodies to Blender, fit garments | Yes: a workflow, nothing trained |
| Renders shown to Claude for the gate and the blind reviewer | Yes as inference. **But** on a consumer plan with "Help improve Claude" on, Anthropic may use those sessions for training, with five-year retention ([SS], consumer terms of 28 Aug 2025). That is arguably "permit others to use … for training". **Switch it off** (Decision 3). |
| MetaHuman Animator's mouths from sound; live talk driven by a language model | Yes: Epic's own tool; a workflow |
| The AI tester walking the build | Yes: it tests the game, not an AI. Never use its MetaHuman frames to train or score a model. |
| A render used once as a conditioning image | Workflow use, by the project's earlier reading (casting/notes/metahuman.md) |
| **Not allowed:** a LoRA or face model fine-tuned on MetaHuman renders; an embedding index (CLIP or DINO) of MetaHuman renders kept as a searchable database; MetaHuman renders as training or test data for any checker (accent, face, clothing) | Outside the clause |

---

## FAMILY A: PEOPLE

### A1. How professional games make crowds of distinct period people

Summarised from the project's notes. New items are marked as read today.

| Game | Method | Source |
|---|---|---|
| **City Sample / Matrix Awakens** (2021–22) | 12 heads, 6 bodies (2 sexes × 3 weights), ~10 grooms, 16 skin atlases with melanin and redness, 63 tops, 33 bottoms, 15 shoes, 10 hand props, per-person scale. Near: full MetaHumans; far: vertex-animated static meshes | project: crowd.md (Vrealmatic, opened 24 Sept) |
| **Hitman: Absolution** (GDC 2012) | ±5% scale per agent "does wonders"; diffuse texture swaps; loops started at random; "crowd acts" (smoking, bench) by upgrading a crowd agent near the player | project: crowd.md (slides opened) |
| **Assassin's Creed Unity** (GDC 2015) | Three distance tiers, at most 40 full NPCs; 29 low-res meshes; on the swap to full detail, the colour is re-applied and the hats matched; the regional mix set statistically | project: crowd.md |
| **RDR2** | 2 to 13 outfit presets per townsperson type; over 1,000 actors captured | project: wardrobe note 1 |
| **KCD and KCD2** | 16 layered slots; each NPC its own preset; clothes become worn and dirty; nearly 2,400 NPCs, half in one city, with AI level of detail | project: crowd.md, wardrobe note 1 [SS] |
| **Watch Dogs: Legion** (London) | "Census" builds each person's look from their role and life | project: crowd.md (opened) |
| **L.A. Noire** | Film costume designer; scanned real costumes "shader swapped" to dress the population | project: wardrobe note 1 [SS] |
| **Mafia: The Old Country** (2025, UE5, early-1900s Sicily) | Marvelous Designer, ZBrush, MetaHuman for facial rigs, Unreal for materials; "period-accurate outfits and historically-inspired hair grooms"; systemic NPC motion captured on a stage in Brno | [SS], Epic interview and 2K Valencia |
| **Still Wakes the Deep** (2024, 1975 Scottish rig) | MetaHuman face rigs for a cast of ordinary workers, with oil grease and sweat in the materials; Speech Graphics for lip sync | [SS] |

**What carries over [I]:**
- A recipe per kind of person, drawn from what the simulation says they are (as in Legion).
- Variety from material, colour, headwear and hand items before new meshes.
- Few full-detail people near the camera.
- Clothes worn and dirtied as standard.
- One costume process from dated photographs.

Nobody at this budget captures motion. Mafia and KCD2 did, so their motion is not ours to copy.

**Unreal 5.8's own crowd tools** [READ, Epic docs]:
- MetaHuman Crowds is **Experimental** ("use caution when shipping with it").
- Near people are full actors. Further people use the Instanced Skinned Mesh Component, which "does not run the post-process Anim Blueprint and therefore does not apply animation correctives".
- The pipeline turns strand grooms into card meshes and strips the high levels of detail.

**Collections** [READ]:
- Experimental.
- The example slots are Character, Hair, Eyebrows, Top Garment and Bottom Garment. The garment slots take a Chaos Outfit or a skeletal mesh.
- "These are examples only. When you create a custom pipeline, you choose exactly which slots to expose."
- Per-item instance overrides such as "hair color or material tints".

**Licence:** engine features, under the UE EULA. Only Epic's sample content carries NoAI. One open report describes a GPU-memory leak in Mass crowds (project: crowd.md).

### A2. Free sources without AI restrictions

| Source | Licence; NoAI or AI clause | Fits 1990 and the bar? | Mark |
|---|---|---|---|
| **MetaHuman Creator and plugin** (UE 5.8): bodies, faces, presets, Python API | UE EULA; AI clause: no training, testing or databases (section 2); no NoAI tag | Yes. Presets lean young and modern; faces are aged and individualised by script | [SS] licence; API from project notes |
| **Engine's MetaHuman animations**: 31 UEFNAnimPreset locomotion clips, template idles | Engine content, UE EULA | Starts, loops and stops on our skeleton; only one standing idle | project: natural-idles (read in the install) |
| **MetaHuman Crowd plugin, Collections, Instances** | Engine, UE EULA | The tiers and the tints we need; Experimental | [READ] docs |
| **Mixamo** characters and animations | Adobe: royalty-free for commercial games; forbids reselling raw files and bulk downloading for machine learning; no clause against AI workflows | Idles, gestures and smoking of uneven quality; women's idles; no period | [SS]; FAQ UNREACHED; allowlisted (D46) |
| **MPFB2 (MakeHuman for Blender)**: European adult heads at any age, as conform targets | Code GPLv3; output CC0 | A base for faces that do not lean modern | project: faces-and-hair [SS] |
| **Our own capture**: phone video through Apache-2.0 MediaPipe, or 5.8's experimental video-to-body | Apache 2.0, or engine | Labour; a human performer may count as a "human-made input" needing his ruling [I] | project: markerless-mocap, townspeople-animation |
| GASP; MetaHuman Crowd Sample; City Sample Crowds; Fab grooms | **NoAI** | Excluded by the rule | section 1 |
| CMU motion library | Commercial use allowed, resale not [SS]; old and noisy | Fallback only | project: townspeople-animation |

### A3. The kit method: people

**The parts:**
- **Bodies:** 6 builds (male and female × slim, average, heavy), plus ±5% scale per person. All read adult: a height floor, adult proportions, and the apparent-age test (casting rules).
- **Heads:**
  - 14 principals, frozen once approved.
  - About 30 regulars. I recommend a face each, not shared crowd faces. Talk happens at 4.4 m, where a reused face shows, and a face made by script costs minutes while a garment costs days [I].
  - 16 crowd faces by age decade (casting DELIVERY 7.2).
- **Hair:**
  - 10 to 12 period grooms. Men: short back and sides; receding, bald and comb-over; side parting; mullet; grown-out perm. Women: shampoo-and-set; perm; feathered bob; big mid-length perm; short and practical. A headscarf hides hair cheaply.
  - Facial hair: a full moustache on about a third of men aged 35 to 60; stubble.
  - Hair colour through the melanin and redness parameters, greying with age.
- **Skin and age:** the skin preset by complexion, then ageing, freckles and redness ([SS]: Creator exposes "skin aging"). Smoker's lines on about 4 in 10 working men. Denture-shaped mouths for older people. "People looked older for their age" (casting SUMMARY).
- **Motion:**
  - per sex: base idles (4+), breaks (8 to 12), breathing, 2 speaker and 2 listener loops, 6 to 10 gestures (natural-idles);
  - walks: 6 to 10 gaits by age and sex, play rate ±10%, random phase;
  - crowd acts: smoking, looking in a window, waiting.

**The variation:**
- A seed per person picks:
  - face, build, scale, groom and its colour, facial hair, skin age;
  - idle set, gait and rate;
  - the clothing recipe (family B) and the accessories (family C).
- The census sets spawn weights, not face counts (casting 7.1).
- Rules:
  - neighbours never share a base idle or a gait;
  - no two people in one frame share a face, unless one is beyond 20 m.

**The tools:**

| Tool | Use |
|---|---|
| MetaHuman Creator Python, run by agents | Duplicate a preset; push face coefficients toward the European set; sculpt landmarks; set body constraints, then `request_auto_rigging` (blocking) and export while open. From 5.7, almost every Creator step can be batched [SS] |
| Blender 4.5 | Hair curves with Curl, Frizz and Clump node groups, exported as Alembic. Unreal's groom import and `create_new_groom_binding_asset` are scriptable (project: faces-and-hair, hair-groom-script) |
| Unreal | Collections and Instances (Experimental), with the game's own recipe in JSON and C++ as the fallback that keeps everything ours. Crowd tier through the crowd plugin; AnimToTexture as the shipped fallback. The Animation Budget Allocator. Retargeting offline per body (tools/ue/retarget_metahuman_idle.py) |

**Where a human eye must judge:**
- every face: apparent age at or above the floor, no resemblance to a real person (reverse image search), period look;
- every new groom, in the game's light;
- the whole frame against the bar.

Agents do the generating and the counting: clone phases, foot slide, weight shift within 10 s (project: natural-idles section 5).

### A4. The reference that sets the bar (links only; looked at, never copied)

**The bar itself** [READ, looked at today]:
- **The Hook sheet.** About ten people, mostly older, in dark wool overcoats and jackets (navy, black, brown, a beige pair of trousers, one maroon coat), almost all seen from behind or side-on at 8 to 40 m, walking. Nobody has an umbrella in the drizzle.
- **The KCD2 fountain frame.** About ten people, each a distinct silhouette with one dominant matte colour (ochre, green, brown, red, a black habit). They stand loosely or walk, and carry things, at 5 to 40 m.

**Dated photographs of northern crowds:**
- **Tom Wood, *All Zones Off Peak*:** Merseyside bus passengers, 1978 to 1996, chosen from about 100,000 negatives: "lined, weary faces, changing fashions" [SS]. The best single source for how ordinary northern people of every age sat, stood and dressed.
- **Ken Grant, *The Close Season*:** Liverpool and Birkenhead, from 1989 [SS]. Dated prints, for example "Brothers outside the Kop, waiting, Liverpool, 1989", in the Hyman Collection [SS]. Adults only as reference: some frames show children, and none are used.
- **Documentary Photography Archive, Greater Manchester County Record Office** [READ, Wikipedia]:
  - Martin Parr, *Retailing in the Borough of Salford* (1985);
  - Tom Wood, *Care in the Community, Rainhill Hospital* (1988–90) and *Cammell Laird Shipyard, Birkenhead* (1993–96);
  - viewable through the Manchester Archive+ Flickr.
- **Steve Thornton, *Fish Town*:** Grimsby fish dock, 1990 (project).
- **Peter Fryer, Smith's Dock:** 1990–91 (project).
- **Report Digital's dockers:** 1989 (project).
- **Alec Gill, Hessle Road:** to 1987 (project).
- **Grimsby Telegraph, "Looking back at Freeman Street from the 1970s to the 1990s":** a gallery [SS].
- **Geograph, "Grimsby B & Q":** about 1990, pre-Easter shoppers, CC BY-SA 2.0 [SS].

### A5. The variety, and why

| Tier | How many | Distinct by | Why |
|---|---|---|---|
| Principals | 14 | own face, voice, 1 to 3 outfits | canon |
| Regulars | about 30 (14 men, 16 women, census-weighted) | own face [I], own groom, one fixed outfit | the street must recognise them; talk at 4.4 m |
| Passers-by, first street | 30 to 40 people in the day, 10 to 25 on screen [I] | 16 crowd faces × 6 builds × 12 grooms × colour × recipe | the Hook sheet and KCD2 frames show about ten each |
| Town, later | 200 to 500 on screen | as above, crowd tier beyond about 15 m | casting DELIVERY |

The limit is not faces. It is clothing silhouettes. "Two men in suits" were taken for clones; colour tinting doubled the time to spot one (5.7 s to 12.3 s); in a crowd of 20 seen for 10 s, four appearance clones went unnoticed (project: crowd.md, Clone Attack, measured).

---

## FAMILY B: CLOTHES

### B1. How professional games make them

Summarised from wardrobe-at-scale and plain-1990-clothes:
- base garments in slots, skinned meshes and not simulated cloth (only hems and coat tails simulated);
- one base fitted to every body;
- variants are the same mesh with new materials (Warhorse: "REUSE BASE MESH … UVS");
- masked fabric layers (Cyberpunk's 20 masks);
- wear and dirt maps;
- a recipe per kind of person;
- a costume process from dated sources.

Tailored pieces come from patterns made once (Mafia: Marvelous, ZBrush, MetaHuman). Our attempts at that failed on the cut and the lapel, and the route is stopped.

**One point from looking at the bar [I]:** the crowd is seen at 8 to 28 m, mostly from behind (A4). At 10 m a lapel is about 13 pixels wide and a whole coat about 100 pixels tall (RUBRIC section 1). So the crowd's coats need back, shoulders, length, colour, cloth and movement, which are what our chain already produces. The MakeHuman CC0 suit jacket walked and raised its arms cleanly in Unreal on Ron and Darren. It failed at talk distance on the lapel and the shape (project: CLOTHES.md). That is the reason for Decision 2.

### B2. Free sources without AI restrictions

| Source | What | Licence; NoAI | Status | Mark |
|---|---|---|---|---|
| CLO CONNECT "Official" MV2 and FV2 patterns (KOFOTI) | A professional pattern for each of the ten silhouettes | CONNECT Free License, free commercial use, revocable; **allowed by his ruling of 2 Oct** | Patterns, not rigged; draping stopped 2 Oct | project: free-garments/pc |
| FreeSewing (Carlton, Carlita, Jett, Jaeger, Devon, Bent, Florent cap, Charlie trousers) | Patterns | MIT, allowed | Our own finishing has failed on tailoring | project |
| MakeHuman CC0 packs (suits01, Wool Pants, Fisherman Sweater, Long Skirt, boots) | Meshes to fit | CC0 (check each header) | The suit jacket walks clean; failed at talk distance | project |
| Sketchfab CC-BY garments (TopNotch "Black Suit", Style3D CG suit) | Unrigged meshes, modern cuts | CC-BY: allowed with credit for garments (ruling) | Weak | project |
| Microsoft Rocketbox | Fused work-jacket people | MIT | Grade C, shape only | project |
| **Poly Haven fabrics**: Denim Fabric 03, 04, 05, 06; Poly Wool Herringbone (8K) | Fabric surfaces for the cloth library | CC0; no NoAI possible | **Use**: denim and wool herringbone now | [SS] |
| **ambientCG** | 2,000+ CC0 materials: fabrics and leathers to check | CC0 | **Use** for the library | [SS] |
| Epic's free MetaHuman wardrobe (Sweater, Jeans, Boots, Flats, T-shirts) | The current stopgap | Fab Standard; **NoAI on Techwear and a Sweater [SS]**; the rest unknown | Hold until each flag is read signed in (Decision 1) | [SS] |
| Fab paid suits ($40 or under) | Rigged tailoring | 247 of 387 NoAI; the one unreached (Nice Pictures) unseen | None qualifies | project |
| CGTrader free garments | Patterns and meshes | "Royalty Free License (no AI)": **never** | Out | project |

### B3. The kit method: clothes

**The parts:**
- **Slots, as the game's recipe:**
  - head (hat or scarf);
  - outer layer;
  - top (shirt, blouse, jumper, cardigan, T-shirt);
  - bottom (trousers or skirt);
  - legs (tights as a skin material);
  - feet;
  - small worn pieces (belt, pager, watch);
  - hand items (family C).
- **A layering rule:** only combinations already tested may be recipes. Unreal has no "garment support" (Cyberpunk's push-in), so recipes must not invent new layer stacks [I].
- **Base garments:** about 40 for the first street, as planned (wardrobe note 1). For the crowd, outer layers first: dark overcoat, car coat, anorak, quilted anorak, wool coat, belted mac, sports jacket.
- **The fabric library**, as Unreal material layers or instances:
  - melton and overcoat wool;
  - tweed and herringbone (Poly Haven's poly-wool herringbone);
  - worsted suiting;
  - corduroy;
  - gaberdine;
  - polyester slacks cloth;
  - denim, with stonewash variants (Poly Haven denim 03 to 06);
  - nylon shell (anorak, shell suit);
  - machine knit;
  - PVC (donkey-jacket yoke);
  - leather.
  - Each carries wear, pilling, fuzz and dirt (Epic's garment materials already expose `WearMaskStrength`, `pilling_normal_strength` and `A_FuzzAmount` [project]; our own materials repeat the idea).

**The variation:**
- The seed picks a base garment from the recipe, a fabric, a colour from the palette for that age and sex, a wear level (0.2 to 0.8), and dirt at the hem and cuffs.
- **Palette** (plain-1990-clothes): men navy, black, charcoal, mid-grey, brown, bottle green, oatmeal; women beige, camel, cream, brown, navy, muted wine.
- Bright nylon is only for the young: a shell suit, purple, teal.
- **Loud-item cap:** at most one loud item per frame.
- **Frame rule:** no two people in one frame share a top garment in the same colourway [I].

**Recipes per kind of person** (from casting, dress-and-bearing and plain-1990-clothes; weights from the census):

| Kind | Outer | Under | Head | Feet | Hand (C) |
|---|---|---|---|---|---|
| Older man (55–75) | dark overcoat, donkey jacket, car coat, nylon anorak, tweed sports jacket | V-neck or crew jumper over a collared shirt; dark wide trousers | flat cap or bareheaded | black boots or lace-ups | folded newspaper, cigarettes |
| Older woman, widow (60–85) | wool coat, belted mac | cardigan, blouse, skirt below the knee, tights | headscarf, plastic rain hood over a set | flat lace-ups, fur-lined ankle boots | handbag on the forearm, shopping bag, tartan shopping trolley, spectacles |
| Fish-market worker, man or woman | white overall coat or smock, or nylon anorak | jumper; work trousers | woolly hat; headscarf for women | white wellingtons | none |
| Docker or shipping man | nylon anorak or zip jacket | jumper, work trousers | woolly hat or bare | work boots | cigarettes |
| Cab driver | car coat or zip jacket | shirt, slacks | bare | slip-ons | driving gloves, cigarettes |
| Shop worker | nylon overall or tabard | blouse and skirt, or shirt and slacks | — | flats | — |
| Office man (25–55) | raincoat or overcoat | grey or navy suit, tie | bare | lace-ups | briefcase, rolled umbrella |
| Office woman (25–50) | belted mac | skirt suit with modest shoulder pads, blouse, tights | — | court shoes | shoulder bag |
| Woman (30–55) out shopping | quilted anorak or wool coat | jumper, slacks or skirt | perm, rain hood | flat boots | carrier bags |
| Young man (18–30) | shell-suit top, Harrington, bomber | T-shirt or polo, stonewash jeans | mullet or grown-out perm | boots (his ruling: no trainers on the cast; the crowd follows until he says otherwise) | gold chain, rare pager |
| Young woman (18–30) | denim jacket or long coat | jumper, short skirt with opaque tights, or jeans | big permed hair | ankle boots | shoulder bag, big earrings |
| Priest | dark raincoat | black suit, clerical collar | black beret | black shoes | — |

Uniforms (police, post) carry no real insignia unless canon names them.

**The tools:**
- Blender 4.5 by script: the project's chain, from `pattern_panels.py` and `sew_*.py` through `retopo_garment.py` and `skin_garment.py` to `carry_garment.py`.
- Unreal by script:
  - the Outfit Asset for resizing;
  - Collections tints, or our own dynamic material instances;
  - Epic's `example_add_clothing.py` pattern for colour slots;
  - Mutable (beta) or Skeletal Mesh Merge to cut draw calls in the crowd.

**Where a human eye must judge:**
- every base garment, against the rubric at the distance it will be seen;
- the colourways as a set (a palette sheet);
- whole frames, which go to his page.

Fabric variants of a base that has passed are judged by the gate alone, as small assets are [I].

### B4. The reference

- RUBRIC.md's four dated suit photographs: Major at Camp David, 22 Dec 1990; Kinnock, 5 Sept 1989; LSE, Dec 1988; Maastricht, 9 Dec 1991.
- The northern crowd photographs of A4.
- **Catalogues:**
  - Kays 1990, "era of shell suits" (Worcestershire Archive, project) [SS];
  - Argos Autumn/Winter 1990/91 on archive.org [SS; archive.org not tried, blocked before].
  - Look at adult goods only; copy no design and no brand.
- **Museum objects:** V&A, M&S cardigan of 1989 and Farah slacks of 1986 (project).

### B5. The variety

- **First street:** about 40 base garments × 4 to 8 fabric and colour variants × wear = 200 to 300 looks, enough for 30 to 40 recipe outfits plus the principals' and regulars' fixed ones [I].
- **Town:** 60 to 70 bases, adding the work clothes above.
- **Outerwear comes first,** because the eye goes to the upper body and the crowd is seen from behind.

---

## FAMILY C: ACCESSORIES

### C1. How professional games make them

- GTA V gives props their own 5 slots: hats, glasses, ear pieces, watches, bangles (project: wardrobe note 1).
- City Sample carries 10 hand props.
- AC Unity spawned "all hats … on real" people and matched props when a far figure became a near one.
- Hitman's smoking and bench "crowd acts" upgrade an agent near the player.
- Eye-tracking: head accessories and the top's texture hide clones **as well as** varying the face texture, and better than changing the face's shape (project: crowd.md).
- So accessories are among the cheapest variety per hour [I].
- Things with print on them (newspapers, packets) are simple shapes with the effort spent on the printed graphics (project: GOODS).

### C2. Free sources without AI restrictions

| Source | Items | Licence; NoAI | Fit | Mark |
|---|---|---|---|---|
| Our own (`model_accessory.py`) | **Passed:** Sheila's handbag, spectacles and chain; Darren's belt and pager | Ours | At the bar by blind review | project |
| Poly Haven "Vintage Suitcase" | Worn green leather case, rusted clasps, "weathered travel stickers" | CC0 | Holdall or suitcase base; check the stickers for real names | [SS] |
| MakeHuman **glasses01** | Spectacle set | CC0 | Unseen | [SS]; page UNREACHED |
| MakeHuman **hats01**; system fedoras | Hats and caps; fedora01 | CC0 | Unseen; a fedora is the trilby cliché to avoid | [SS]; UNREACHED |
| MakeHuman **hats03**, incl. "elvs_male_flat_cap1" | Flat cap | **CC-BY**: allowed for garments with credit, if a cap counts as a garment [I] | A base for the cap that failed twice in sewing | [SS]; UNREACHED |
| Poly Haven and ambientCG leathers and fabrics | Surfaces for bags, gloves, scarves | CC0 | Use | [SS] |
| Sketchfab lighters | "Zippo" models | CC-BY, or the licence unseen; a real product | **Out**: a real brand, and CC-BY for non-garment 3D needs a ruling | [SS] |
| Fab accessories, Megascans | Glasses, bags, paper | **NoAI** | Out | section 1 |
| Newspapers, cigarette packets | none scanned anywhere | — | Ours, with fictional print | project: GOODS |

**Plainly:** nothing free beyond a suitcase and some unseen MakeHuman pieces. Accessories are a make-it family.

### C3. The kit method: accessories

| Kit | 1990 form (references) | Parts and parameters | Variation | Attach | Triangles [I] |
|---|---|---|---|---|---|
| **Spectacles** (passed) | Large square on older women, smaller round tortoiseshell as fashion, gold metal; photochromic tints (Science Museum) | Rim outline curve, bridge, arms, lens size 50–58 mm | Material (gold, brown or black acetate, tortoiseshell), tint | `head` socket, 1–2 mm off the nose | 2–4k |
| **Handbag** (passed) | Structured leather, about 27 × 18 cm (V&A, about 1990) | Body box, flap or frame top, clasp, strap length | Leather colour, wear at the corners, size | `hand_r` or forearm, grip pose | 3–6k |
| **Shopping** | Plastic carriers, a string bag, a **tartan two-wheeled shopping trolley** for older women [I] | Bag panels baked from one cloth drape to 3 fill states; trolley frame and wheels | Print (the street's own fictional shop names), fullness | `hand_r` or `hand_l` | 1–4k |
| **Umbrella** | Men: long, black, rolled; women: telescopic | Shaft, 8 ribs, canopy radius 0.45–0.55 m, closed or open | Colour, open or closed | `hand_r` | 2–5k. Use sparingly: the Hook sheet shows none |
| **Headwear** | Flat cap, woolly or bobble hat, headscarf tied under the chin, clear plastic rain hood, black beret | Panels, or a skinned shell on `head` and `neck` | Cloth, colour, wear | Skinned to `head` and `neck`; hair swapped to a flattened "hat groom" or hidden | 1–4k |
| **Scarf** | Knitted wool; football colours fictional only | A tube on the neck, ends to the spine | Colour, stripes | Skinned to `neck` and `spine_05` | 1–2k |
| **Gloves** | Leather, wool | Crowd: a hand material only; principals: a shell | Colour | Hand material | 0–2k |
| **Watch** | Metal bracelet or leather strap | Case and strap | — | Wrist; principals only (3–5 px at 8 m) | 0.5–1k |
| **Cigarettes and lighters** | About 30% of adults smoked; packet, disposable lighter, matchbox, roll-up tin | Cigarette with an emissive ember and a Niagara thread of smoke; packet with fictional print | Brand art (fictional), roll-up or tailor-made | `hand_r` or the lips, with a smoking animation | <0.5k each |
| **Newspaper** | A folded tabloid or broadsheet; the game's own evening paper | A 3–4 mm slab, soft fold, slight curl (GOODS) | Masthead and pages (ours), fold | Under the arm or in the hand | <1k |
| **Pager** (passed) | Black matt, about 80 × 50 × 25 mm | as built | — | `pelvis` | 0.5–1.5k |
| **Walking stick** | For many over 75 [I] | Shaft, crook | Wood or metal | `hand_r`, a gait to match | <1k |

**What is never made:**
- pushchairs, prams or anything of a child's (the September crowd note's "pushchair" is struck);
- off-licence bags or bottle shapes;
- betting slips, pools coupons or scratchcards;
- mobile phones;
- real brands, clubs or mastheads.

**The tools:**
- One Blender recipe per kit (`model_accessory.py` extended with `--kind`), with parameters and a seed. The agent runs it headless on the exported bodies and renders a sheet.
- Unreal attaches to sockets at spawn from the recipe, the same in the game's code and in a Collection custom slot. Creator itself has no eyewear slot (project).

**Where a human eye must judge:** the gate, which already passed four pieces. Small accessories are approved by the gate alone and seen in context on his page.

### C4. The reference

- Science Museum objects: BT and Motorola pagers; photochromic spectacles of 1980 (project, opened).
- V&A: Dot Cotton's handbag, about 1990 (project, opened).
- Argos Autumn/Winter 1990/91 and 1989/90 on archive.org, and Retromash: watches, umbrellas, handbags [SS]. Look only.
- Kays 1990 [SS].
- The photographs of A4, for how things were carried: bags on the forearm, papers under the arm, cigarettes cupped.

### C5. The variety

- About 10 head items and 10 hand items (casting DELIVERY), each with 3 to 6 material variants.
- Spread by recipe and census weight.
- At most one open umbrella and one loud scarf per frame [I].

---

## THE ONE PROOF BEFORE ANYTHING IS MULTIPLIED

**What.** Three passers-by from **one recipe, "older man, out on foot"**, walking in the proof view (the hook camera by day) at 8 to 15 m, with one of them also seen at talk distance (4.4 m). They are made entirely by the kit:
- a different crowd face each, aged 58 to 72 by script;
- a different build each;
- a different period groom each, with a moustache on one;
- **one base coat in three fabrics**: navy melton, brown herringbone tweed, charcoal;
- headwear: a flat cap, bareheaded, a woolly hat;
- hand items: a folded paper, a cigarette, a carrier bag;
- their own idle sets and gaits, out of step;
- trousers and boots that have already passed.

The recipe mirrors the Hook sheet's two foreground men, so the comparison is direct.

**Judged** side by side with the Hook sheet and the KCD2 fountain frame, by my check and then a fresh reviewer:
1. Do the three read as three different northern men of 1990, not one man three times? A fresh reviewer is given the frame for 10 s and asked to find two people sharing something (the Clone Attack method).
2. Silhouette, shoulder line, length and colour against the sheet's men. Cloth matte and worn, never plastic.
3. Apparent age adult and old enough. No resemblance to a real person.
4. No 2020s cue: no slim fit, no contrast stitching, no trainers, no logos.
5. Motion: never an A-pose; a weight shift within 10 s; not in step; no foot slide (measured by the AI tester).
6. Cost on the RX 6700: GPU ms and video memory for 3, then 20, people, measured in the game.

It passes when a fresh reviewer fails it only on narrow points (the gate rule). Then it goes to his page as one whole frame. **Only after his yes in the game** is the recipe multiplied, first to the older-woman recipe, then the rest.

**What it depends on.** One coat that passes at crowd distance.
- If Decision 2 says yes, the candidates are the MakeHuman CC0 suit jacket lengthened into an overcoat (it already walks clean in Unreal), or our own chain's simplest coat [I].
- If he says no, the crowd waits on the blocked tailoring like the principals. The people half (faces, hair, age, idles, accessories) can still be proven in the stopgap clothes, but not judged complete.

**Rough effort** [I]:

| Part | Builder-days |
|---|---|
| Three faces and three grooms | 2–3 |
| The coat at crowd distance | 1–3, **the risk** |
| Three cloths with wear | 1 |
| New accessories: cap base, woolly hat, newspaper, carrier bag, cigarette | 2–3 |
| The recipe and seed system in the game | 1–2 |
| Idles and walks | shared with natural-idles' "one person first" |
| Two review rounds | 1–2 |
| **Total** | **8 to 14** |

---

## Per family, in one line

- **People:**
  - *Free:* MetaHuman Creator and the engine's bodies, faces, 31 locomotion clips and 5.8 crowd tools; Mixamo; CC0 MPFB2 heads.
  - *We make:* aged and varied faces by script, period hair from Blender curves, idle sets and the recipe system.
  - *Impossible without a ruling:* GASP, the MetaHuman Crowd Sample, City Sample Crowds and Fab grooms (all NoAI), and any captured human performance.
- **Clothes:**
  - *Free:* CLO's CONNECT patterns (ruled allowed, but draping is stopped), FreeSewing, CC0 and CC-BY meshes (weak), and CC0 fabric textures for the cloth library.
  - *We make:* the base garments as skinned meshes, with fabric, colour and wear variants and recipes per kind of person.
  - *Impossible without a ruling:* Epic's free MetaHuman wardrobe if its flags read NoAI as they appear to; any ready-rigged suit (every one read at $40 or under is NoAI); and tailoring at the bar, which is a blocked capability.
- **Accessories:**
  - *Free:* almost nothing; Poly Haven's suitcase, MakeHuman's unseen CC0 glasses and hats, and CC0 leathers.
  - *We make:* nearly everything, as parametric Blender kits on sockets (four already passed).
  - *Impossible without a ruling:* Megascans and Fab accessories (NoAI), CC-BY 3D outside garments, and anything branded.

## Decisions for Jafar (licence and scope; one line each, recommendation marked)

1. **NoAI and Epic's own free content** (GASP, Epic's free MetaHuman wardrobe, the Crowd Sample):
   - **(A, recommended)** the rule as written: they leave the plan. Idles come from the engine's MetaHuman clips and Mixamo, the stopgap clothes from what passes our gate, and each Epic wardrobe item's flag is read signed in first.
   - (B) an exception for Epic's first-party content used only inside the game.
   - (C) keep them as now.
2. **A crowd-distance rubric:**
   - **(A, recommended)** passers-by are judged only from 8 m out, front, side and back, so a coat that fails the lapel at talk distance can still dress the crowd.
   - (B) one rubric for everyone.
3. **Switch off "Help improve Claude"** in his Claude account's privacy settings, so MetaHuman renders sent to our sessions are never used for training:
   - **(A, recommended)** yes;
   - (B) no.

CC-BY for non-garment accessories is not needed now. We make them.

## What I could not reach or verify

- **MetaHuman's licence and the Unreal EULA at source:** metahuman.com and unrealengine.com were blocked. The clause is quoted from search summaries.
- **Fab's EULA wording on NoAI** ("as inputs to"): a summary only. Fab's own docs say only "must not be used for generative AI data collection" [READ].
- **Every Fab listing** (GASP's flag rests on the project's read of 1 October), the AI flag on each of Epic's free wardrobe items, the Clothing Construction Presets, and the MetaHuman Crowd Sample's contents.
- **Which grooms ship inside the 5.8 MetaHuman plugin** (engine content, so no NoAI) and which are Fab downloads: to be read in the install on his PC.
- **Mixamo's terms:** the FAQ was blocked; summary only.
- **Anthropic's consumer-terms page:** summaries only. The setting's current name should be checked in his account.
- **MakeHuman's hats01, hats03 and glasses01:** unseen; their per-item licences are unread.
- **Poly Haven's suitcase stickers:** unseen.
- **The Argos and Kays catalogues, the Grimsby Telegraph galleries and the Geograph image:** not opened.
- **Whether Collections' custom pipelines can add hat, spectacles or hand-prop slots in 5.8:** the docs say slots are chosen in a custom pipeline; the project's earlier note says Creator runs no custom pipelines in 5.8. Untested.
- **Every cost and effort figure:** none is measured on the RX 6700.
- **KCD2's and RDR2's own appearance pipelines:** no primary source.

## Sources (all read or searched 3 October 2026 unless said)

1. Epic, "Licenses and Pricing in Fab", undated. https://dev.epicgames.com/documentation/fab/licenses-and-pricing-in-fab [READ]
2. Epic, "MetaHuman Crowds in Unreal Engine", 5.8, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-crowds-in-unreal-engine [READ]
3. Epic, "MetaHuman Collections in Unreal Engine", 5.8, undated. https://dev.epicgames.com/documentation/metahuman/metahuman-collections-in-unreal-engine [READ]
4. Epic, "Licensing MetaHuman", undated. https://www.metahuman.com/license UNREACHED; [SS]
5. Epic, "Unreal Engine EULA", undated. https://www.unrealengine.com/eula/unreal UNREACHED; [SS]
6. CG Channel, "You can now sell MetaHumans, or use them in Unity or Godot", 4 June 2025. https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/ [SS]
7. Fab support, "NoAI meta tags and Created with AI self-declaration", January 2025. https://support.fab.com/s/article/Introducing-NoAI-meta-tags-and-Created-with-AI-self-declaration [SS]
8. Sketchfab, "Introducing the NoAI and CreatedWithAI tags", February 2023. https://sketchfab.com/blogs/community/introducing-the-noai-createdwithai-tags/ [SS]
9. Fab, "Game Animation Sample", published 11 June 2024, updated 17 Aug 2026. https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016 (project: natural-idles, read 1 Oct; not re-read)
10. Fab, "MetaHuman Crowd Sample", undated. https://www.fab.com/listings/5f481d73-afb1-4d94-ba6e-7cabf5d296fa [SS]
11. Fab, "City Sample Crowds", undated. https://www.fab.com/listings/903037e9-e1ac-4f41-96e8-1683c6fa7ad4 [SS]
12. Fab, "MetaHuman Techwear Outfit" (Epic), undated. https://www.fab.com/listings/9e04c752-1979-4723-b78f-6d24afc532bc [SS]
13. Fab, "Sweater Metahuman Wardrobe cloth", undated. https://www.fab.com/listings/e785d5d1-f8fd-41ab-a351-d8bf8dc5928c [SS]
14. Fab, "MetaHuman Clothing Construction Presets, Set of 4", undated. https://www.fab.com/listings/3c0c4df1-ce96-44cf-8a30-c47d744d2a0c [SS]; AI flag unseen
15. Fab, "Glasses Tactic - Metahuman", undated. https://www.fab.com/listings/4f7c0fa0-e129-474f-b0fc-38c10b11231a [SS]
16. Adobe, "Mixamo FAQ", undated. https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html UNREACHED; [SS]
17. Anthropic, "Updates to our consumer terms", 28 Aug 2025. https://www.anthropic.com/news/updates-to-our-consumer-terms [SS]; MacRumors, 28 Aug 2025. https://www.macrumors.com/2025/08/28/anthropic-claude-chat-training/ [SS]
18. Epic, "Mafia: The Old Country: Making the old feel new with Unreal Engine 5", undated. https://www.unrealengine.com/developer-interviews/mafia-the-old-country-making-the-old-feel-new-with-unreal-engine-5 [SS]; 2K Valencia, "Mafia: The Old Country Character Art", undated. https://valencia.2k.com/mafia-the-old-country-character-art/ [SS]; 2K, "Dev Diary 3: Capturing Performance", 2025. https://mafia.2k.com/en-GB/the-old-country/news/dev-diary-3-capturing-performance/ [SS]
19. Speech Graphics, "Still Wakes The Deep", undated. https://www.speech-graphics.com/client-projects/still-wakes-the-deep [SS]
20. Poly Haven, "Vintage Suitcase", undated. https://polyhaven.com/a/vintage_suitcase [SS]
21. Poly Haven, "Denim Fabric 03/04/05/06" and "Poly Wool Herringbone", undated. https://polyhaven.com/a/denim_fabric_05 ; https://polyhaven.com/a/poly_wool_herringbone [SS]
22. ambientCG, home, undated. https://ambientcg.com/ [SS]
23. MakeHuman Community, asset packs hats01, hats03, glasses01, makehuman_system_assets, undated. https://static.makehumancommunity.org/assets/assetpacks/hats01.html (and siblings) UNREACHED; [SS]
24. Sketchfab, "Zippo lighter" models (Rostislav Sokolovskiy and others), undated. https://sketchfab.com/3d-models/zippo-lighter-77a7ca30c36d49e3aafdf42db2ebf946 [SS]; rejected
25. Wikipedia, "Documentary Photography Archive", live page. https://en.wikipedia.org/wiki/Documentary_Photography_Archive [READ]
26. Dewi Lewis Publishing, Tom Wood, *All Zones Off Peak*, undated. https://www.dewilewis.com/products/all-zones-off-peak [SS]; Wikipedia, "Tom Wood (photographer)". https://en.wikipedia.org/wiki/Tom_Wood_(photographer) [SS]
27. Hyman Collection, Ken Grant, "Brothers outside the Kop, waiting, Liverpool, 1989", undated. https://hymancollection.org/artworks/categories/17/1072-ken-grant-brothers-outside-the-kop-waiting-liverpool-1989/ [SS]; Wikipedia, "Ken Grant". https://en.wikipedia.org/wiki/Ken_Grant [SS]
28. Internet Archive, "Argos Autumn/Winter 1990/91 catalogue", undated. https://archive.org/details/argos-autumn-winter-1990-1991 [SS]; Retromash, "Argos Catalogues". https://retromash.com/argos/ [SS]
29. Worcestershire Archive and Archaeology Service, "Kays at Christmas, 1990", 19 Dec 2019. https://www.explorethepast.co.uk/2019/12/kays-at-christmas-1990/ [SS]
30. Grimsby Live, "Looking back at Freeman Street from the 1970s to the 1990s", undated. https://www.grimsbytelegraph.co.uk/news/nostalgia/freeman-street-how-it-looked-1453870 [SS]
31. Geograph, "Grimsby B & Q", David Wright, CC BY-SA 2.0, about 1990. https://www.geograph.org.uk/photo/150880 [SS]
32. Manchester Archive+, "Manchester Local Image Collection" (Flickr), undated. https://www.flickr.com/photos/manchesterarchiveplus/albums/72157628581776571/ [SS]; Picture Sheffield. https://www.picturesheffield.com/ [SS]
33. Medium, James Roha, "A Beginner's Guide to MetaHumans in Unreal Engine 5.6 and 5.7", undated. https://medium.com/@Jamesroha/a-beginners-guide-to-metahumans-in-unreal-engine-5-6-and-5-7-e9b14fadbf3d [SS] (5.7 batching; skin ageing)
34. Epic, "Skin Material Controls", undated. https://dev.epicgames.com/documentation/metahuman/skin-material-controls : fetched, but no content came back (scripted page): effectively UNREACHED

**Project files read (3 October 2026):**
- production/research/wardrobe-at-scale/ (SUMMARY, notes 1 and 3)
- production/research/free-garments/ (SUMMARY, PC-SUMMARY, pc/ by search)
- production/research/plain-1990-clothes/NOTE.md
- production/research/casting/ (SUMMARY, dress-and-bearing-2026-09-28, DELIVERY sections 4, 5 and 7, notes/crowd.md, notes/census.md, notes/metahuman.md by search)
- production/research/natural-idles/NOTE.md
- production/research/townspeople-animation/SUMMARY.md
- production/research/character-pipeline/ (RESEARCH-2026-09-25, faces-and-hair, metahuman-builds)
- production/research/clothing-pipeline/ACCESSORIES-2026-09-30.md
- production/research/shop-window-interiors/GOODS-2026-10-03.md (by search)
- production/research/markerless-mocap/
- production/art/clothing/ (RUBRIC.md, SCREENING-2026-10-02.md, accessories/README.md)
- CLOTHES.md
- DECISIONS.md (the last forty lines)
- ledger-v2/research/license-allowlist.md
- production/reference/README.md, hook-sheet.png and kcd2-town-fountain.jpg (looked at)
- tools/meshgen/blender/model_accessory.py (header)
