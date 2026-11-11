# Paid-tools sweep, 2026-11-11

Search terms (case-insensitive, production/research all subfolders and production/audits): his decision, Jafar's decision, Jafar's call, his call, money, paid, purchase, buy, subscription, per month, a year, US$, $, £, €, CHF, outside the allowlist, outside the list, not on the list, licence outside, commercial licence, Indie. The raw hits ran to about 500 lines (most are 1990 prices and game-review quotes); only tool/service hits are kept. Not read in full: aaa-reference (player reviews, credits map), bulk-api texts, cab-office price notes (period prices, no tools). Dates are file dates (name or first lines); "line" is the file line of the cost.

"On his page" = grep of production/approvals/needs-you/items.json and archive.json by tool name.

## Tools

| # | Tool: what it does | Cost as written | Source (file:line) | Proposed for (file's words) | Date | On his page |
|---|---|---|---|---|---|---|
| 1 | **Houdini** (SideFX): procedural 3D, cloth drape, grooming. DECIDED already (free tests said yes 16:14, 11 Nov) | Indie US$299 a year; Apprentice non-commercial | research/clothing-pipeline/SLEEVES-RECIPE-2026-09-29.md:53 "Paid: Jafar's decision"; casting/TOM-FACE-METHOD-2026-10-07.md:35; aaa-street/1-PIPELINE.md:54 "price unchecked" | cloth "Vellum Drape" for sleeves; "Flatter needs a new groom" (Darren's hair); buildings | 29 Sep, 7 Oct | yes (houdini-cascadeur-accounts-2026-11-11, open; paid-tools-ruling-2026-11-11, open) |
| 2 | **Cascadeur**: keyframe physics and AI in-betweening. DECIDED already (free tests) | Indie about $19 a month or $96 a year (search summary, unverified) | research/frontier-ai-uses/notes/HD-motion.md:25, :174-175 "it costs money, so it is Jafar's decision"; :237 "only on Jafar's yes" | "hand-keyed sit and stand transitions" (motion) | 7 Oct | yes (same open item) |
| 3 | **Marvelous Designer** (CLO): pattern and cloth drape | US$39 a month or US$280 a year (Personal); Enterprise US$199 a month or US$2,000 a year for batch use | clothing-pipeline/MARVELOUS-PRICE-2026-10-23.md:14,21; MARVELOUS-UNATTENDED-2026-11-08.md:39 "Needs money: his decision"; TAILORED-ROUTES-2026-09-30.md:12 | tailored jackets; unattended batch drape | 30 Sep to 8 Nov | yes (Marvelous items in archive; the program is in use; Enterprise batch licence: not found as its own item) |
| 4 | **CLO** (full): same engine as Marvelous | $50 a month or $450 a year | wardrobe-at-scale/4-MARVELOUS-MONTH.md:54; clothing-pipeline/TAILORED-ROUTES-2026-09-30.md:37 "Jafar's decision" | "Dearer, with no gain" over Marvelous | 30 Sep | no |
| 5 | **MetaTailor**: fits any garment mesh onto a MetaHuman | Pro $35 a month or $336 a year (five free exports a month per audit) | wardrobe-at-scale/3-METAHUMAN-AND-FAB.md:77; 5-SCANS-AND-AI.md:27; audits/2026-10-02-clothing-plan.md:23 "Defer both" | "month of a tool" for garment fitting | 2 Oct | no |
| 6 | **Clothy3D Studio**: same job | free public beta (licence not read) | wardrobe-at-scale/5-SCANS-AND-AI.md:27 | garment fitting | undated (about Oct) | no (free, unreviewed) |
| 7 | **Garment Tool, Simply Cloth** (Blender add-ons) | US$36 to 170 | clothing-pipeline/TAILORED-ROUTES-2026-09-30.md:36 "Jafar's decision" | tailored cloth | 30 Sep | no |
| 8 | **Character Creator 5** (Reallusion; Headshot 3) | CC5 $299 | audits/2026-10-02-clothing-plan.md:23; casting/notes/metahuman.md:123 | garment fitting; faces from a photo | 2 Oct | no |
| 9 | **KeenTools FaceBuilder** (Blender): head from photos, MetaHuman texture | Freelancer $19.99 a month or $191.88 a year (excl. tax) | character-pipeline/RESEARCH-2026-09-25.md:9; casting/notes/metahuman.md:121, :207-208 "One subscription month (money → Jafar)" | faces (Darren, Sheila "fail their sheets") | 25 Sep to 7 Oct | no (a ruling names "the paid Blender add-on's free trial" as fallback, audits/rulings-sweep/rulings.json:504; not put as an item) |
| 10 | **Hyper3D Rodin**: image to textured mesh | Creator $30 a month, Business $120 a month, about $0.4 to 1.5 a model | casting/notes/metahuman.md:129 | faces | about 7 Oct | no |
| 11 | **Avaturn**: selfie avatar (not MetaHuman) | Pro $800 a month | casting/notes/metahuman.md:130 | faces | about 7 Oct | no |
| 12 | **3D Scan Store**: scanned garments, MetaHuman Identity heads | Garment jacket £25.99 personal, +£209.99 per item commercial, male pack +£1,379.99; Identity £29.99 personal, £329.98 one commercial project | wardrobe-at-scale/5-SCANS-AND-AI.md:16; casting/TOM-FACE-METHOD-2026-10-07.md:40 "his call (licence, money)" | scanned clothes; Tom's face | Oct | no |
| 13 | **Renderpeople / AXYZ Metropoly** | posed $39, rigged $79, 120 people $999; AXYZ €19-59 each, anima €649 a year | wardrobe-at-scale/5-SCANS-AND-AI.md:17, :19 | "reference or distant crowd only" | Oct | no |
| 14 | **Fab "Curly Short 01/02"** (hair) | CHF 8.95 personal, 17.02 professional; listings "Allows usage with AI: No" | character-pipeline/faces-and-hair-2026-09-28.md:15 "Money and a li[cence]"; ruling: curls made in Blender (rulings.json:2478) | Darren's curls/hair | 28 Sep | no (settled by his ruling, not an item) |
| 15 | **Fab MetaHuman suits/coats** (cheap purchase) | about US$5 to 20 each | clothing-pipeline/TAILORED-ROUTES-2026-09-30.md:11 "Jafar's decision, money" | tailored coats, jackets | 30 Sep | no (retired by ruling, audits/2026-10-04-adversarial-audit.md:46 "no-purchase/plain-clothes") |
| 16 | **Commission** (Husky Studio, Fiverr) for garment corrections | envelope about $225 to 690 for first street | audits/2026-10-02-clothing-plan.md:25, :42 | garment corrections | 2 Oct | no (retired same way) |
| 17 | **Car Primitives** (Blender add-on) | $19.95 commercial | field-scans/CARS-2026-11-08.md:16 | parked cars (model for parameters only) | 8 Nov | no (not wanted: "no purchase") |
| 18 | **Rokoko cloud, Move AI, DeepMotion** (video mocap services) | prices not read | frontier-ai-uses/notes/HD-motion.md:225 "commercial services" | motion clips | 7 Oct | no |
| 19 | **Paid voice services** (Resemble marketplace, Voices.com, Cartesia, Hume, ElevenLabs) | plans not priced; Speecon corpus EUR 75,000 | casting/notes/voices.md:40, :77-78; character-pipeline/RESEARCH-2026-09-25.md:37-41 | voices (Sheila, accents) | Sep | no (ruled: no paid voice, DECISIONS.md:105; his p267 yes settled Sheila's voice, rulings.json:3220) |
| 20 | **Swiss IP lawyer review** (title search, Nemesis patent, store/AI Act notices) | cost not stated | frontier-ai-uses/3-LEGAL.md:63, :85 "Money, his decision" | release | 7 Oct | no (release, not a standing problem) |
| 21 | **Stock footage (Pexels/Pixabay) licences** | free; licences OUTSIDE the allowlist | ai-video-motion/STOCK-FOOTAGE-2026-11-09.md:35 | motion source or test control | 9 Nov | no |
| 22 | **Fab Megascans stains decals (third party)** | 8.18 CHF; "Allows usage with AI: No", so out | texture-pipeline/B-MEGASCANS-2026-11-10.md:104 | textures/materials | 10 Nov | n/a (excluded); his five Megascans picks are free (fab-megascans-five, done) |
| 23 | **Meshy, Hyper3D etc. (AI 3D)** | paid tiers are subscriptions; free output CC BY 4.0 | aaa-street/4-VEHICLES-AND-FURNITURE.md:103 | vehicles, props | Sep | no |

Also seen and not paid: Style3D free tier is non-commercial (TAILORED-ROUTES:12); InstaMAT free under US$100k revenue (clothing-pipeline/PIPELINE-2026-09-30.md:30); Quixel Megascans free on Fab (B-MEGASCANS).

Count: 23 rows (21 distinct paid or money-bearing tools or services, plus 2 free-but-outside-list entries).

## Open problems (to match against tools)

From HANDOVER.md "Tried and failed" (11 Nov):
1. Sheila's colours: garment with no maps drawn white (fixed, now a selftest).
2. Drape Studio layering: cloth over frozen cloth lets the inner garment through (jacket over jumper, 4,082 s against 587 s).
3. Sheila's blouse hem through the cardigan: 3 tries, worst point stayed 11.8 mm.
4. Ron's boots cut low for Sheila: ragged edge, orphaned eyelets; a different shoe must be modelled new.

From HANDOVER.md "Tries used" (still open or set aside):
5. Tom's surfaces: 3 tries, set aside, listed.
6. Sheila's skirt band clear: 2 of 2, set aside.
7. The cast's bind pose: 1 of 2 (fallback idle).
8. The office exit: 2 of 2 (stand-up).
9. The crown (hair): 4 tries, listed.
10. The solve (markerless mocap): commandlet 2, full editor 2 (crashed, no card support).
11. Drape Studio's jumper: 2 of 2, spent.
12. Sheila's cardigan left band: 0 of 2; her blouse at the shoulders: 0 of 2.
13. Motion 3's clip 2 of 2; motion 1's clip 2 of 2, set aside.
14. Texturing: jeans masks 2 then fair film (set aside as garment method); brick 2 offline plus one packaged film; timber edge wear 2 of 2 set aside; the cornice 2 of 2 set aside.

From FINDINGS.md (20 open lines, short):
15. Hill haze does not thicken toward the crest.
16. Street details: broken window has no crack; fish crates not walked; Mickey's window reflected roofline draws as steps.
17. Suspicion: Core number not read by the game's talk.
18. Live talk still invents (7% of turns).
19. Speech misses its bar (median 2.02 s against 2.0 s).
20. Frame headroom: stutter set aside, 2 tries spent.
21. Faces in daylight underlit; Sheila's and Darren's faces fail their sheets (eyes green).
22. Voices: crowd's recorded lines drift American.
23. Newcomer's first questions end in "that's all I know" about a third of the time.
24. Three placeholder Mixamo figures (Martha, Kate, Leonard) out of period.
25. Tom and a speaker as played: motion-matching sample; stand-in motion.
26. Police file time-and-state faults (set aside).
27. Free-play faults: south quay near black at night; Rita's pavement trap.
28. Mickey's past disagrees with itself (canon).
29. Nothing ships yet (launchers; three libraries without licence read).
30. Sash windows 1.50 m high against 1.68 m.
31. Clothes and hair: near hair short of brief; cast wear white base layer; Tom's jacket chin/jaw show through collar.
32. Collision switched off does not stay off.
33. Office camera can cut off seated Ron (try 1 of 2).
34. Quay end: hidden wall held people short (try 1 of 2).

Not read: DECISIONS.md and NOTEBOOK.md (not read whole by brief). Sources behind the tools' prices are search summaries in several rows (marked unverified in their files).

## Ranked by expected gain against cost (the builder, 11 Nov 17:40; prices as the source files give them, unverified where marked there)
1. MetaTailor: its free version first (Pro about US$35 a month; site 11 Nov shows a free version, price fields blank): garment refits onto each MetaHuman body; Sheila's refit took most of 11 Nov in Blender with five faults; every later wearer needs the same. On his page.
2. KeenTools FaceBuilder: its 15-day free trial first (US$19.99 a month; keentools.io read 11 Nov): faces from photographs for the faces that fail their casting sheets (Darren, Sheila). On his page.
3. Marvelous Designer Enterprise, one month (US$199): unattended batch drape, the route Drape Studio's layering failed on 11 Nov. On his page.
4. Character Creator 5 (US$299): overlaps 1 and 2 but outside the MetaHuman pipeline.
5. 3D Scan Store garments: personal licence cannot ship; commercial £209.99 an item.
6. Hyper3D Rodin: faces, overlaps 2, a monthly fee.
7. CLO: same engine as Marvelous, dearer.
Motion-capture services (Rokoko, Move AI, DeepMotion) are out under his 5 Nov ruling (no money for motion capture); Houdini and Cascadeur already decided as free tests.
