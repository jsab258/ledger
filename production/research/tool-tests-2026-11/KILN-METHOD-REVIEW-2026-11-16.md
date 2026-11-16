Method researched: Macklin, Müller and Chentanez 2016 (XPBD), Müller 2008 (Hierarchical PBD), Kim, Chentanez and Müller 2012 (Long Range Attachments), all three read in full; SideFX Vellum "mass and thickness" page; Kiln's drapestudio engine source (sim.rs, mechanics.rs, serve.rs, body.rs, doc.rs), its MECHANICS.md, python/run_job_script.py, LOOP.md and the eleven round reports of 16 Nov 2026 (all read 16 Nov 2026)

# Kiln's cloth method as a whole: why each general fix moves something else (16 Nov 2026)

Review only. Nothing was changed, built or run. Reference games (Mafia, Kingdom Come II): none found for a drape solver used while making garments; their files were not searched in this review. The references used are the professional tools and papers the round reports already name.

## The answer

Kiln's drape engine has no material stiffness of its own: every stiffness in it is a count of solver passes, and every kind of rule (cloth links, seams, strain limits, body contact, cloth-to-cloth contact, layers) is applied in turn, once per small step, in a fixed order, with the last one applied winning. The drape that comes out is therefore the balance point of about forty hand-set counts and reaches, nearly all marked "estimated" and tuned on Tom's garments, not the resting state of a described fabric on a described body. Any general change to one count (nine times the passes), one start position (the collar floor) or one order moves that balance point for every garment, so a fix for one job shows up as a change in another. The paper behind the method names this exactly: with plain position-based dynamics "raising iteration counts to obtain stiffness on one object may inadvertently change the behavior of all other objects in the simulation. This often requires stiffness coefficients to be re-tuned globally" (XPBD, section 1). A method that does not trade faults keeps three things apart that Kiln mixes: what the fabric is (data, the same at any particle distance and any pass count), how accurately it is solved (a measured stop, per piece), and what goes in (bodies and patterns checked against written standards before the first step); and it has a gate that runs every job with bands, so a trade is seen the hour it is made.

## What the code does (the common cause)

Line numbers are of the working copy read on 16 Nov; Kiln's HEAD was 04f9c93. No shell was available in this review, so the committed text could not be compared with the working copy; another helper's arm-line edit (rig.rs) was in flight. The solver lines cited are not part of that edit as its method note describes it (unverified).

1. **A link's stiffness is its pass count.** A link is corrected by `(len - rest) * 0.8 / (wa + wb + compliance / h2)` (sim.rs 2435, with the weight sum at 2349). Nothing is stored between passes. XPBD's rule (its equation 18) subtracts the stored multiplier times the compliance and keeps one number per link; that term is what makes stiffness independent of pass count and time step. Without it, the paper says, "the effective constraint stiffness is now dependent on both the time step and the number of constraint projections performed" (section 3). In Kiln the "compliance" only sets how much of the error each pass removes.
   - Worked from the code's own constants (computed here, one link alone, grain mixing left out): rib knit's weft (stretch 50, doc.rs 99; compliance 10^-6, sim.rs 249-251) removes about 68% of its error per pass at Normal quality and about 15% at Fitting quality, only because the small step is five times shorter (mechanics.rs 10-12, 27; sim.rs 2340-2341). At Fitting, 8 passes leave about 28% of the error; 72 passes leave about 0.001%.
2. **The counts are fixed numbers, one set for the whole garment.** Passes are 6, 8 or 6 by quality (mechanics.rs 59-63), times a factor taken from the finest piece of the garment (sim.rs 1174, 2369-2371). The solver's tolerance constants add one pass and are otherwise unused (sim.rs 2334-2337). Nothing measures whether the cloth has reached its stiffness.
3. **Every point weighs the same, whatever its cloth.** `inv_mass = vec![1.0; n]` (sim.rs 1091). The fabrics carry a density (doc.rs 49, 77, 96-102) that sim.rs never reads (searched: no match). Compliance does not change with edge length (sim.rs 923-925, 989). So the same fabric is a different material at each particle distance. Derived here, not measured (unverified): with unit weights, a hanging strip of soft links at half the particle distance has twice the rows hanging under each link and half the edge length, so about four times the strain under its own weight. Vellum sets mass from area times density so that "as you change the resolution of your Vellum geometry, the behavior of the simulation shouldn't change very much" (https://www.sidefx.com/docs/houdini/vellum/mass_thickness.html, read 16 Nov 2026 through a summarising fetch; the same quote is in the slide method note from a saved copy).
4. **Rules are applied in turn; the last one wins.** One small step runs: links and seams (sim.rs 2412-2470), strain limits (2473-2496), body contact with friction (2509-2551), hold (2554-2564), cloth-to-cloth every 4th step (2567), body push every 2nd (2588), seam join (2595), then layers three times, face push and seams again (2603-2610). Each block can undo the one before. The comments record the trades one by one: "Layers last, so nothing after them in the substep pushes the inner garment back through" (2598-2600); body push lifting "stood a waistband off the hips (it slid 22 mm)" (mechanics.rs 297-299); a 1 mm layer gap "made the two garments jitter" (mechanics.rs 300-302).
5. **The numbers were set on one man's clothes.** engines/drapestudio/MECHANICS.md lines 92-116 and 278-310 list the solver's own rules as "estimated", with Tom's jumper, jacket and jeans as the evidence for each. The same note says the reference program's solver is "a different (implicit, conjugate-gradient) method" (line 94-95), so none of its numbers carry over.
6. **The end state depends on the start.** Static friction 0.8 holds a point where it first presses (sim.rs 2545-2546); the settle stops when 99% of points move under 30 mm/s for 10 frames (serve.rs 1093-1103; mechanics.rs 331-335), with a settled jumper still jittering at 18 to 21 mm/s (MECHANICS.md 306). A slow slide of under 1 mm a frame counts as still. So a different start gives a different "settled" drape.

## The four cases

### 1. The slide-down fix (KILN-SLIDE-FIX-2026-11-16)

- **What held the trousers before, and how thin it was.** Band rest 1,099.6 mm; strain limit 1.08; 1,099.6 x 1.08 = 1,187.6 mm against Ron's hips of 1,188 mm (the report's own figures). The band is 20 mm longer than his waist (1,080 mm). The trousers hang only if the links hold the band well under its limit; the limit itself gives no margin. This is an input fact as much as a solver fact.
- **Why the fix held them.** Runs d0 to e2 in the report: more link passes, not more limit passes, keep the band short enough. This is cause 1 above: stiffness is the pass count.
- **Why Tom's jumper changed.** His job has 6 mm rib pieces, so the whole garment's factor went from 3 to 9 (sim.rs 1174, 2369). Every soft link in the jumper (knit, rib, and the 0.3 share a knit link resists squeezing with, mechanics.rs 347, sim.rs 2436-2438) became stiffer in effect, by cause 1. The judge then read 191 inner edges over 1.2x against 61, with 39 on each rib cuff against 0, worst 1.574 against 1.518. The fabric values did not change; the fabric did.
  - The report says the rib cuffs "have no strain cap". The code is narrower: rib is exempt from the 1.12 cap only (sim.rs 921-922) and still gets the slider limit, about 1.27 along its weft at stretch 50 (sim.rs 996), measured from its shrunk rest length. Why the judge reads 1.42 there was not settled (the judge's code was not read): unverified.
  - The direction of the change (cuffs more stretched) is as the report guesses: a sleeve that now resists gathering holds the cuff's top wider. Not tested: unverified.
- **Why drapes got up to 2.7 times slower.** The factor follows the finest piece for every piece (sim.rs 1174). Skirt 374.6 s against 138.3 s (2.71x); Tom 116.5 s against 62.7 s (1.86x). The link solve was already the largest cost after round 10 (27 s of 46 s).
- **Sources.** Müller 2008: Gauss-Seidel "information propagates slowly through a mesh. The slow convergence lets cloth or soft bodies look stretchy, especially when high resolution meshes are used"; with a hierarchy, 2 passes matched the stiffness of about 20 (its figure 7). XPBD section 7: at zero compliance it "requires the same number of iterations to obtain a stiff result". That passes must grow with the square of the fineness is in none of the three papers: still unverified, as the slide report says.

### 2. Sheila's pleated skirt (falls in the first stage)

- **Facts.** On today's build every piece's top is at 42 to 115 mm by frame 51, before any particle-distance change (job_pleated_skirt.result.json, stage_ends). The first stage stopped as "settled" after 51 of 400 frames at 16.3 mm/s (pleated_skirt_start.txt line 20). It fell on the morning's build too (drops 668 and 748 mm, diagnosis section 4). The fall is older than every fix of the day.
- **The job reported success.** The result file says "ok": true and "state": "settled" with drop_ok false and a drop of 1,040 mm; run_job_script.py returns 0 whenever the script ran, failed checks or not (line 100).
- **What the start looked like.** The seams start 17,729 mm apart in total after one piece was turned end for end (26,027 mm as flagged); the start check took 11 rounds on cloth-through-cloth crossings; 701 points were lifted (result notes; start.txt lines 9-19).
- **Mechanism: not known.** Two candidates from the code, neither tested (both unverified):
  - (a) The sewing phase is not physical. While seams are open there is no friction (sim.rs 2505), no kept speed (2617, 2635-2637) and 2% gravity (2358-2364). Each stitch moves both sides by equal weight (2459-2468), up to 30 mm a pass (2465; mechanics.rs 45), six or more passes before the step's one body-contact pass (2412 against 2509). Body contact is a push to the nearest skin within 30 mm and sees nothing deeper (body.rs 51, 532, 698-706). So a long seam can drag well-placed pieces to badly placed ones, or cloth through a limb. The same was seen on Darren's jacket: "While the seams closed, the sleeves pulled the bodice down to them" (collar report). The morning's export lay round one shin only (diagnosis section 4), which a ring sliding over two hips cannot reach.
  - (b) The band (826 mm) is 96 mm longer than her waist (about 730 mm) and must catch on the hip slope (about 974 mm): it needs a limit under 974 / 826 = 1.18 that is really held. The band fabric's values were not read.

### 3. M4's thin margins (jacket over jumper)

- **Facts.** Through over 3 mm: 124 of 133. Worst edge: 2.88 of 3. Time: 144 s of 153 s (LOOP.md line 37). Round 10 confirms 191 over 1 mm, 124 over 3 mm, worst 2.875 on frontL.
- **The worst edge shows the trade.** The jacket's own strain limit is at most 1.12 (mechanics.rs 351), yet an edge ends at 2.875. finish_layers pushes layers apart, closes seams, applies limits four times, then runs two more rounds of pushes and seam closes with no limits after them (sim.rs 1799-1824). Separation wins over strain because it runs last. The job's bar for the worst edge is 3.0 for every fabric (mechanics.rs 200-202), so this passes.
- **Why the counts sit just under the bars.** Layer contact is a push from the nearest point or face inside fixed reaches (25, 16, 40, 70 mm; mechanics.rs 216-229), with no gap beyond the two half thicknesses (LAYER_GAP_MM 0). Three more passes were added in rounds 8 and 9 (face push, triangle push, untangle) after "764 such crossings ... which the nearest-feature pushes read as nearly clear" (Kiln README, round 9). Pass counts were raised until the count went under the bar: "one push per substep left 74 jacket points under the jumper, two left 20, three left 12" (MECHANICS.md 297). A count tuned to a bar lands beside the bar.

### 4. Collar placement moved Tom's neckband (KILN-COLLAR-FIX-2026-11-16)

- **Facts.** The collar floor (`partner.y.max(floor)`, sim.rs 414-415) applies to every body whose neck is found. Tom's neckband front starts up to 110 mm higher; his front and back 9 mm higher (serve.rs 117-119). His counts moved: worst 1.502 to 1.518, inner 64 to 61, away from seams 11 to 14. The start-placement fix before it had moved them from 1.561, 118 and 38.
- **Mechanism.** Cause 6: the drape is not a resting state reached from any reasonable start; it keeps a memory of where each piece began (sticking friction, an early stillness stop, a sewing phase that drags pieces). A start rule changed for Ron's stand therefore changes Tom's result.
- **No band exists to judge it by.** Runs repeat exactly, and the only regression rule in use was "byte for byte" or "no worse". Neither can pass a placement change, so each move was argued by hand in its report.

## A method that does not trade faults: ordered steps

Hours are estimates made here, not measurements. Each step is a general change; none names a garment. Every step is judged by step 1's gate. The order is cheapest and most revealing first. Whether any of it enters an order is the session's decision.

| # | Step | What it is | Est. cost | Closes |
|---|---|---|---|---|
| 1 | Regression gate per job, with bands | All eight jobs (Tom's jumper, jacket, jeans, layered; trousers, skirt, donkey jacket, nylon jacket) run before and after any engine change: about 15 minutes of machine time at today's times. Per job a recorded line: tops at each stage end, drop, through and inside counts, worst edge per piece, edges over 1.2x, seconds. Bands measured, not guessed: the same job run with its start nudged by 1 mm gives the method's own noise. run_job_script.py exits non-zero when checks fail. | 4-6 h | Trades made unseen (Tom moved in three rounds); a failed drop check read as a number; the skirt's "ok" |
| 2 | Input standards, checked before the first step | Body: one skin, a head or a joints file, A or T pose (CLO and Marvelous require it for their own fitting, per the arm-line note), person height. Pattern: every closed ring (waistband, cuff, neckband) compared with the girth it must hold on; refused or flagged when ring x strain limit reaches the widest girth below it (trousers: 1,187.6 against 1,188). Total and per-seam start travel capped. Particle distance stated per piece. | 6-8 h | Darren's class of fault at the door; the trousers' zero margin made visible; the skirt named at input if cause (b) |
| 3 | Passes per piece by its own particle distance | The loop is already per piece (sim.rs 2418). Legs at 10 mm get 4 times, only 6 mm bands 9 times. The slide report names this as the cheaper refinement not tried. | 3-4 h | Most of the 2.7x; nothing else. A stop-gap until step 4 |
| 4 | Stiffness as fabric data: true XPBD links, weight by area | Store one multiplier per link per small step and add XPBD's term (its Algorithm 1, lines 4, 7, 9: "trivial modifications to an existing PBD solver"). Weight each point by its share of the piece's area times the fabric's density. Scale compliance so one fabric gives one strain per load at any particle distance. Then passes set accuracy only, and a measured stop (worst stiff-link strain under a tolerance) can replace the counts. | 8-12 h code, then 12-20 h re-tuning the fabric presets against Tom's references | Tom's cuffs changing with passes; fabric changing with particle distance or quality; ends the need to re-tune everything after each pass change |
| 5 | Strain limits per material that hold at the end | Limits applied last in every finishing sequence, with the leftover reported. A piece fails when any edge passes its own fabric's limit by a small tolerance, in place of 3.0 for all. Rib's limit set in the fabric data. | 4-6 h | M4's worst edge (2.875 against a 1.12 fabric) shown honestly; the rib cuff question |
| 6 | Long-range limits for stiff cloth | Müller 2008: coarse one-sided upper limits with rest lengths summed along the fine edges; they "only grip if the entire material between the adjacent particles is fully stretched". Kiln already meshes every piece at 20 mm and maps between meshes by pattern coordinate (UvLocator, sim.rs 790), so the coarse level exists. Long Range Attachments does not fit: it needs attached points and "for unattached ... cloth ... does not provide benefits" (its section 6). | 16-24 h | The slide-down without nine times the passes; the rest of the time cost |
| 7 | Bounded moves between contact passes; sewing as a physical phase | No seam pull, push or step moves a point further than the contact reach before contact is applied again; body contact inside the pass loop. Sewing with friction and weight in proportion, closing by soft springs then welding (Vellum Drape's order, per the start-placement diagnosis). For layers, one contact rule with a real gap; the repo's own start check (the cloth crate's exact crossing test) is the measure. | seam bound 4-6 h; layer contact 20-40 h | The skirt if cause (a); the bodice dragged down on Darren; M4's through counts |
| 8 | Decision point after steps 1 to 5 | If the gate still shows trades, compare with the implicit solver already in the repo (ClothCraft's, in cloth/: 10.57 ms a step on the card against 122.8 ms on the processor for 2,454 points, round 10). It failed by eye in rounds 1 and 2 (LOOP.md lines 27-28), so this is a measured comparison, not a switch. | 6-8 h to measure | A wrong method kept past its limit |

Steps 1 to 3 change no drape of a passing job except in time. Steps 4 to 7 change every drape, so each needs every milestone re-judged; that is the price of ending the trades, and step 1 is what makes it affordable.

## Risks

- **Step 4 moves everything at once.** Every preset was tuned with pass-dependent stiffness; M2 to M4 will not hold byte for byte and may fail by eye before they pass again. It needs its own cap and its own failed-capability report if it does not land.
- **Honest limits fail first.** Step 5 will most likely fail the layered job on its worst edge the day it lands. That is a known shortfall being counted, not a new fault, and should be recorded as such before the step.
- **Input standards refuse real garments.** A ring rule set too strict refuses a loose skirt that should hang on the hips. The rule's margin needs measuring on the eight jobs first.
- **Bands hide slow drift.** A tolerance band per job lets small moves add up over rounds; the recorded line must be compared with a fixed baseline, not with yesterday's.
- **The hierarchy has its own faults.** Müller notes that poor coarse meshes give visible artefacts at low pass counts, and that rest lengths summed along edges can be "too loose".
- **The cuff explanation may be wrong.** If the cuffs' change is not the stiffer sleeve, step 4 may not close it; the gate would show that.
- **Two-tries rule.** The slide-down and start placement have each used both tries; the collar one of two. Steps touching those faults are new methods on faults at their limit.
- **Cost.** Steps 1 to 5 come to about 37 to 56 hours by these estimates; steps 6 and 7 to about 40 to 70 more.

## Unverified

- That passes must grow with the square of the fineness (measured in the slide report, in no source read).
- The four-times strain figure at half the particle distance (derived here from the code, not run).
- The per-pass shares for rib (computed from constants, one link alone; assumes the job uses the preset's values).
- Why Tom's cuffs read more stretched, and what the judge's 1.42 is measured against.
- Both candidate causes of the skirt's fall; that the morning's export round one shin means cloth passed through the body.
- That the solver lines cited are the same in the committed text (no comparison could be made).
- Every hour estimate.
- The Vellum page was read through a summarising fetch, not line by line.
- The links given for the Müller 2008 and Kim 2012 papers are their usual published addresses; the review read saved copies and did not fetch them again.

## Unreached, and not used as evidence

- Macklin et al. 2019, "Small Steps in Physics Simulation" (https://mmacklin.com/smallsteps.pdf): the file came down but no tool here could read a PDF; not read.
- Wang, O'Brien and Ramamoorthi 2010, "Multi-resolution isotropic strain limiting" (graphics.berkeley.edu): refused on a certificate error; no way round was tried.
- Goldenthal et al. 2007 and Provot 1995 (strain limiting): not fetched.
- Marvelous Designer's own account of its solver, of carrying a drape across a particle-distance change, or of holding a waistband: not found by any helper today.
- Kiln's committed text through git (no shell in this review).
- KILN-CLOTHCRAFT-BRIEFS.md and the cloth crate's source: not read. No file called a design note was found in the Kiln repository; engines/drapestudio/MECHANICS.md was read in full as the solver's design record.
- The judge's code and the held-back jobs: not opened, by the brief.

## Sources read in full (16 Nov 2026)

- Macklin, Müller and Chentanez, "XPBD: Position-Based Simulation of Compliant Constrained Dynamics", MiG 2016, http://dx.doi.org/10.1145/2994258.2994272 (saved text copy: F:/LedgerTools/tool-dev/runs/kiln-slide-2026-11-16/diag/sources/XPBD.txt).
- Müller, "Hierarchical Position Based Dynamics", VRIPHYS 2008, https://matthias-research.github.io/pages/publications/hpbd.pdf (saved copy: same folder, hpbd.txt).
- Kim, Chentanez and Müller-Fischer, "Long Range Attachments", SCA 2012, https://matthias-research.github.io/pages/publications/sca2012cloth.pdf (saved copy: same folder, sca2012cloth.txt).
- The eleven reports of 16 Nov in F:/LedgerTools/tool-dev/reports (KILN-ROUND10-REPORT, round10-bench not read, KILN-BREADTH-DRAPES, KILN-START-PLACEMENT-DIAGNOSIS and -FIX, KILN-COLLAR-METHOD and -FIX, KILN-SLIDE-METHOD and -FIX, KILN-ARMLINE-METHOD); F:/LedgerTools/tool-dev/LOOP.md lines 22-41.
