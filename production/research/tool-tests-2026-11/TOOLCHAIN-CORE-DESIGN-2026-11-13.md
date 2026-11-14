Method researched: tool sources and notes of all four tools, read 13 Nov 2026 (Seamshift src and MECHANICS.md; Drape Studio AUTOMATION.md and src/serve.rs, 85 commands; ClothCraft at commit 16761c55, 8 Nov, src/vbd.rs, src/ogc, src/fabrics.rs; Loomwright MECHANICS.md and job.rs) and their test reports in this folder. ClothCraft's brief page (claude.ai artifact DMSWtYf5MnqSZcpZckqNuy) was unreachable (docs connector errors, three tries); its file list is to be checked against this note before the first fixer round.

# The shared core of LEDGER's tools: design note (13 November 2026)

Advisor 139 and his ruling of 13 Nov 14:19 (RULINGS): one combined toolchain that serves the game, never itself. This note fixes only the interfaces today's modules need. Nothing here is built without a game item that needs it.

## Why, and what it must save
- Game items it unblocks: Tom's outfit (jumper, zip jacket, jeans) and its layering (the tailor boss), the cast's outfits refitted (Ron, Darren, Sheila, the townspeople), later the cast's hair. Today these run through Marvelous (paid month ending about 20 Nov, clicks and a bridge) and a Blender chain.
- Hours it should save, against measured costs: the Blender refit chain took 3.2 h for the whole chain, Seamshift 0.8 s per garment per body (SEAMSHIFT-ROUND1, round 1); a drape runs 124 s in Marvelous for the jumper (DRAPESTUDIO-TEST-2026-11-11) but needs a live, clicked Marvelous. Target: a garment draped, refitted to five bodies and skinned with no clicks in under 15 minutes of machine time and under 0.5 h of builder time.
- Share cap: at most 15% of a week's usage (RULINGS 13 Nov), measured in each Monday audit; over it, one keep-or-extend question to him.
- Checkpoint (his park rule): the clothing tool reaches M3 (jumper, jacket with cuff grip, jeans at or better than Marvelous on our check) by the end of the double week, about 22 Nov; else parked as keep-or-drop.

## One program, five parts
Base: the copy of Seamshift (F:/LedgerTools/tool-dev/clothing, tag his-seamshift-2026-11-13), because it already passes the most of our tests and writes skinned FBX that Unreal imports exactly (round 2).

1. **Body and skeleton loader** (Seamshift scene.rs, fbx.rs; keep). Reads binary FBX of any axis and units, MetaHuman bodies point for point; bones and skin weights; fingerprints every body (SHA-256 of file and shape). Add only: glTF reading when a job needs it (Loomwright's body.rs has it). One body type for every part: Body {mesh, bones, weights, landmarks, fingerprint}.
2. **Job and result format** (Seamshift job.rs; keep and extend). A job names inputs, steps and pass bars; a result names every check, number, output file and SHA-256, with exit codes 0 pass, 1 a check failed, 2 bad input. New step kinds sit beside "fit": "drape" (pattern pieces, seams, fabric, arrangement, simulate) and later "groom". Same input, same bytes out, checked by the tool's own test.
3. **The check suite** (Seamshift checks.rs; keep, add). Today: body through cloth, cloth inside body, bands, openings, gap, stretch, folds, skin, mesh intact, camera coverage, identity, negative controls. Add, from today's failures: worst case per piece (stretch, through) not only shares (Drape Studio's cuffs, 11 Nov); every layer present and on the body (Loomwright's lost jacket, 13 Nov); a shape check beside every count (Seamshift's ballooning hem, round 4); settled or jammed label at the end of a drape. Checks run the same on a drape and on a refit.
4. **The viewer** (Seamshift render.rs, viewer.rs; keep). Headless pictures per job: torso views, neck, test poses, source beside result. The window viewer stays optional; nothing needs clicks.
5. **The cloth slot**: one trait, Drape { load(body with its bones and pose, pieces each with its mesh size, seams with easing, fabrics, arrangement, settings) -> Result ; pin / freeze / shrink(piece) ; step(n) -> Result ; positions() ; diagnostics() }, with one engine behind it, ported from ClothCraft (MIT; its licence notice kept at the top of every copied file and in CREDITS.md): pattern to mesh (garment/ template, meshing, seam with easing, embedding; model.rs, energy.rs, math.rs), the VBD solver (vbd.rs and vbd/), Offset Geometric Contact (ogc/), its start check, fabric presets (fabrics.rs), body inspection (avatar/diagnostics.rs). Seamshift has no pattern mesher, so that part is ported too. CPU first; ClothCraft's GPU path only if time measures say so. All layers of an outfit are one cloth system with self-contact, so a jacket over a jumper is solved together, not over a frozen copy.

## The front end
Drape Studio's Python job interface is copied, not its engine: python/run_job_script.py and the compat module, so Marvelous's job scripts for Tom's garments (job_j3.py, zip_jacket.py, jeans.py) run unchanged. The module talks to the tool's `serve` command over the same command names Drape Studio's serve.rs answers (79; the ones our three jobs use first, the rest only when a job calls them). Nothing of Drape Studio's engine, presets or files is copied: its own log says it decompiled Marvelous and copied 59 of its preset values (his page item of 10 Nov), so fabrics come from ClothCraft's presets and our own measured values. Copying its interface is a licence question that is his (the Clothes ruling: the licence judgement is his); it goes to him as one tap before any garment made through it is adopted, and nothing made through it enters the game before then.

## Hair and motion slots (named, not designed)
- Groom: Loomwright's hair module (its copy in tool-dev/loomwright) writes strands and cards; it will use the same body loader (a head mesh), job and result format and checks; its loop runs on its own copy until a game need joins them.
- Motion: none yet. Motionsmith and HumanMotionCraft are under test; a slot is designed only when one passes for a game item.

## The judge, outside the tool
Our measuring scripts (measure_fit.py, drape_check_any.py, bounds.py), the jobs, input bodies, Marvelous's own results and the bars live in F:/LedgerTools/tool-dev/judge (made 13 Nov, with run_round.py and bars.json), never inside the copy; their SHA-256 list is checked before every round and a changed file stops the round. The fixer may change the tool and its own checks, never the judge.

## Milestones (advisor 139), each with the game item it serves
M1 the combined tool builds and every Seamshift job matches round 4 (no regression; serves the cast refits; met by the unchanged copy, 13 Nov). M2 Tom's jumper from Marvelous's job at or better than Marvelous on our check, at most 1.5x its 124 s (Tom's outfit; saves the live, clicked Marvelous run and its bridge, about 0.3 h a garment). M3 the jacket with cuff grip and the jeans the same (the rest of his outfit; Marvelous's month can end). M4 jacket over jumper, nothing showing through from the cameras (the layering that failed in Drape Studio, 11 Nov). M5 outfits refitted and rigged to the cast, the heavy body sitting under its bar (Ron, Darren, Sheila, the townspeople; the 3.2 h chain per garment replaced). M6 one outfit in the packaged game for the gate (the tailor boss).

## Risks
- Speed: ClothCraft's measured timings are on a graphics card; on the processor the jumper may miss M2's 186 s. Measured in round 1 before more is built.
- Its start check refuses any overlap, which layering and refits produce: layers must start apart (as Loomwright's shells do).
- Zips and fastening: ClothCraft's trims are annotations only, so the jacket's zip and fasten calls have no engine yet (a risk to M3).
- No rib-knit preset among its fabrics; the jumper's bands need one, from measured values.
- Same bytes twice: a test with different thread counts.

## Not in this note
Pattern making (Marvelous's patterns and FreeSewing stay the source), textures, Unreal-side tools, anything for hair beyond its slot.

## Breadth by design (his decision, 14 November 08:32; advisor 157)
Standing for every Kiln module (clothing, hair, props, buildings, motion). No special cases: a fix changes the method; any change that adds a code path, setting or number used by only one garment or job, or names a job in code, is refused; per-fabric numbers come only from the fabric presets; each round's report says "special cases: none" or names what was refused. Every module's milestones include held-back jobs drawn from the game's own need lists: at least two never go to the fixer (kept outside its folder, hash-locked with the judge) and run unchanged at every milestone (clothing: from M4 on, six jobs from HOOK-GARMENT-LIST-2026-11-03.md). Held-back jobs passing about as well as the practised ones means the fixes are general; far worse means the tool is being taught to the test and the next round fixes the method. A held-back job shown to a fixer becomes a practice job and a fresh one is drawn.
