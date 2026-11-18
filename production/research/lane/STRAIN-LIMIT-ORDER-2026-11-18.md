# Strain limit order versus body contact (Kiln)

Date: 2026-11-18. Helper research, about 30 minutes. Problem given: where strain limiting should sit relative to body contact in Kiln's substep, and whether the two can be made compatible.

## Short answer

Nobody in the literature or the production docs read here runs strain repair as the very last thing with nothing after it. The established patterns are either (a) strain repair, then collisions last, accepting some leftover stretch in contact areas (Bridson 2002, Narain 2012, PBD long range attachments, Vellum's post collision passes), or (b) strain limits and contact solved in the same loop, so neither undoes the other (Wang 2010, Vellum's interleaving, Wētā's Loki 2025, C-IPC 2021). For Kiln the recommended default is (b) in its cheap form: alternate strain repair and an outward-only body projection inside one loop, with contact points weighted as heavy in the strain repair, and end the loop on the body projection. Layer finishing should move inside that loop. Details and costs below.

Plain summary: today the stretch fix and the push-out-of-the-body fix take turns once and undo each other; the published way is to let them take turns several times in one short loop, always finishing with the push out of the body, and to report any stretch that remains as a garment that does not fit. Checked by a fresh reviewer 2026-11-18.

## 1. What each paper says about order

Narain, Samii, O'Brien, "Adaptive Anisotropic Remeshing for Cloth Simulation", 2012 (ARCSim). https://escholarship.org/content/qt5s1775xd/qt5s1775xd.pdf?t=rbpzun , read 2026-11-18.
- Order: implicit integration, then strain limiting, then collision resolution (non-rigid impact zones). Quote: "We perform strain limiting once at every time step before performing collision resolution."
- Why: no explicit rationale beyond the strain limiter "is not aware of self-collision constraints, which are left to the subsequent collision resolution procedure."
- Known cost of that order, in their words: "Collision resolution may thus cause the cloth to violate the strain limits in colliding regions." They name a tight knot as a bad case and suggest adding collision constraints into the strain limiting optimisation as future work.

Wang, O'Brien, Ramamoorthi, "Multi-Resolution Isotropic Strain Limiting", 2010 (ACM TOG 29(6)). https://escholarship.org/content/qt2qf676hh/qt2qf676hh.pdf?t=rbq03s , read 2026-11-18.
- Order: strain limiting as a velocity filter, with body contact handled inside the same iterations, not as a separate pass. Quote: "We process boundary conditions simultaneously with strain limiting." A vertex that moves into a solid is "projected back to the solid surface" whenever it moves; friction applied to velocity after. Self collision only "once every 64 iterations".
- Why: so that "enforcing one set of constraints does not cause the other to be violated."
- Limit: when contact over-constrains the cloth there is no solution; their dragon reached about -60 percent strain against a -5 percent target. Contact won, strain was reported.
- Cost: 2x2 or 3x3 SVD per violating element; per-frame 0.38 s to 16.67 s excluding collision detection (0.5 to 6 s).

Goldenthal, Harmon, Fattal, Bercovier, Grinspun, "Efficient Simulation of Inextensible Cloth", 2007. Project page https://www.cs.columbia.edu/cg/ESIC/esic.html read 2026-11-18. The PDF (linked from that page) was not reached; see unreached list.
- From the page: fast projection "acts as a velocity filter that easily integrates into existing simulation code". Order relative to collisions not confirmed from the paper itself (unverified).
- Secondary source: Bender and Bayer, "Parallel Simulation of Inextensible Cloth", VRIPHYS 2008, https://animation.rwth-aachen.de/media/papers/2008-VRIPHYS-Parallel_Inextensible_Cloth.pdf , read 2026-11-18. It describes Goldenthal's method as a velocity filter combined with "other velocity filters (like collision response)", and states the general problem with sequential passes: "The next pass may violate the already enforced constraints of the prior one", concluding that "ideal constraint enforcement can only be achieved if the passes are combined". Their own method does contact and friction "in the same process" as the inextensibility iteration.

Thomaszewski, Pabst, Strasser, "Continuum-based Strain Limiting", 2009 (Computer Graphics Forum 28(2)). Abstract page https://diglib.eg.org/items/686588fd-3030-4a3a-9db3-69919355f32f/full , read 2026-11-18. Full text not reached.
- Abstract only: per-element limits on each strain component (stretch and shear separately), a 6x6 linear system per element, a velocity filter that "integrates seamlessly into standard collision handling". Exact order relative to collisions unverified.
- Relevance: edge-based limits (Provot, Kiln today) are mesh-dependent; per-triangle limits control shear separately. Not the cause of Kiln's problem.

Müller, Chentanez, Kim, Macklin, "Long Range Attachments: A Method to Simulate Inextensible Clothing in Computer Games", SCA 2012. https://matthias-research.github.io/pages/publications/sca2012cloth.pdf , read 2026-11-18.
- Order inside each projection iteration (3 to 5 per frame): local stretch, shear, bending constraints first; then long range attachment (LRA) constraints; then "apply collision and other constraints". Collisions are last in every iteration.
- LRA constraints are one-sided ("get activated only when cloth is stretched"), keep each free particle within its rest geodesic distance of an attachment point, averaged Jacobi-style over up to 4 attachments. Cost: "less than 2% of overall simulation cost".

Müller, "Ten Minute Physics 15: self collision" notes, https://matthias-research.github.io/pages/tenMinutePhysics/15-selfCollision.pdf , read 2026-11-18. Per substep: integrate, solve all constraints, update velocity; collision placement inside the solve not shown in the notes (unverified).

Zhai, Schweickart, Haryono, Ilinov, Merlo (Wētā FX), "Stabilizing Impossible Collisions with Loki", supplemental, 2025. https://www-ext.wetafx.co.nz/assets/Uploads/PDFs/Stabilizing_Supplement.pdf , read 2026-11-18.
- Directly on Kiln's question. A strain limit run as a post-collision step "can invalidate collision resolution and lead to penetrations", because "the collision pass is unaware of the edge shrinking process". Two fixes named: "iterate between these passes until convergence" or "unify the constraints into a single solvable system". Loki does the second.

Bridson, Fedkiw, Anderson 2002, https://www.cs.ubc.ca/~rbridson/docs/cloth2002.pdf (reviewer read 2026-11-18): strain limiting (Provot-style, on velocities, Section 4) is part of the internal dynamics that produce candidate velocities; repulsions, then collision resolution and impact zones, follow in Section 5's step. So collisions last, after strain repair. Consistent with Narain and Müller.

## 2. Methods that make the two compatible, and their cost

- Interleave (Gauss-Seidel alternation). Alternate strain repair and contact projection in one loop and finish on contact. Wang 2010, Bender and Bayer 2008, Vellum (below), Loki's first option. Cost: roughly the cost of one contact projection per strain sweep; cheap when contact is a point-versus-body-field test, as Kiln's body push is. Does not converge if the garment is genuinely too small; leftover stretch must then be reported, not hidden.
- Contact-aware weighting. When repairing an edge, give an endpoint that is in contact zero or reduced weight along the contact normal (it behaves like a pinned point), so the free endpoint takes the correction. This is the standard PBD inverse-mass mechanism and how Wang treats "boundary conditions". Cost: negligible.
- One-sided (outward-only) contact projection. Body contact only pushes points out along the body normal and never pulls them in, so a final contact pass cannot shorten or lengthen anything except by the push itself. Vellum's "post collision passes" are this, and its tips page warns: "Because these passes don't interact with the constraints, you will get protrusions where the cloth is pushed out in the shape of the collider" (vellumtips page; the solver node page does not contain this sentence).
- Unified solve. Strain limits and contact as one optimisation: C-IPC (Li et al. 2021, https://arxiv.org/abs/2012.04457v3 , abstract read 2026-11-18) claims "strict satisfaction of strain-limit inequalities" together with interpenetration-free contact, via barrier energies in a Newton solve; Loki 2025 builds on it; Wang, Wang, Tang, Tong 2016 (https://link.springer.com/article/10.1007/s41095-016-0042-8 , abstract read 2026-11-18) uses semidefinite programming. Cost: a different solver class (Newton with line search and continuous collision detection, or SDP), many times slower per step and weeks of work. Not proportionate for Kiln.
- Long range attachments / tethers. One-sided distance limits from holds (or from a pinned seam) to every point, with geodesic rest lengths, inside the same loop and before the contact projection. Cost under 2 percent (Müller 2012). They stop global stretch; they do not fix local spikes at a layer or seam.

## 3. Production solvers (official docs)

Houdini Vellum solver, https://www.sidefx.com/docs/houdini/nodes/dop/vellumsolver.html and https://www.sidefx.com/docs/houdini/vellum/vellumtips.html , read 2026-11-18.
- Collision passes "are interleaved between the constraint iterations" (example: 50 iterations, 5 collision passes, 10 iterations between each).
- "After all constraints are performed, a final round of collision detection is done" (Post Collision Passes, suggested "number of stacked layers + 2"). These final passes do not respect constraints, so protrusions can appear.
- On stretch near bodies: "Since collisions always pre-empt constraints, the result is cloth or hair stretching." Collision wins; stretch is the visible cost. Fix advised: more substeps and constraint iterations.
- No hard max-stretch setting was found on that page; stiffness and iterations control stretch.

Unreal Chaos Cloth, https://docs.unrealengine.com/4.27/API/Plugins/ChaosCloth/ChaosCloth/UChaosClothConfig/index.html and https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/ChaosCloth/EChaosClothTetherMode , read 2026-11-18.
- Long range attachment constraints ("aka tether limit") with TetherStiffness and LimitScale; geodesic option "more accurate at establishing the correct position and length of the tethers, and therefore is less prone to artifacts". Tether modes: fast euclidean ("very prone to artifacts") to accurate geodesic ("the most accurate setting showing the less artifacts").
- StrainLimitingStiffness exists only as a deprecated property. Solve order is not documented on these pages (unverified).

NVIDIA NvCloth user guide, https://docs.nvidia.com/gameworks/content/gameworkslibrary/physx/nvCloth/UserGuide/Index.html , read 2026-11-18.
- Tethers "improve behavior and reduce stretchiness by adding long range constraints between particles and fixed points"; the tether stage is skipped at stiffness 0. Phase configurations set constraint order. Collision position in the iteration not documented there (unverified).

Pattern across all three: stretch control by stiff local constraints plus one-sided long range tethers; collision interleaved and/or last; leftover stretch tolerated near contact.

## 4. Recommendation for Kiln

Diagnosis from the facts given: the 2.875 edge comes from passes that run after the strain limits with nothing correcting them (cloth-cloth contact, seam join, and above all the layer finishing passes). No source above runs unconstrained position edits after the last constraint pass except collision, and even Vellum warns that this makes protrusions.

Option A: stretch-last as the default (today's switch, on).
- Changes: worst edge drops to near its limit; leftover reported.
- Risk: the Wētā and Bridson point. Edge shortening can pull points back into the body or into another layer. One clean trousers run (body-through 0, 1.242) is one sample, and 1.242 is still over the 1.12 class of limits, so it did not converge. Tight garments (jacket, layered over shirt) are where it will fail.
- Size (estimate): 0.5 h (flip the default). Not recommended alone.

Option B (recommended): one closing loop that does both, collisions last.
- Changes: replace the tail of the frame and of the layer finish with a loop of K rounds (start K = 8): (1) Provot edge repair, with points currently in body contact weighted heavy (inverse mass scaled toward 0 along the contact normal) and held points fixed; (2) seam closure and layer separation as constraints inside the same round, not after it; (3) outward-only body projection (push along body normal to the surface plus thickness, never pull). Stop when worst ratio is within limit plus tolerance and body-through is 0, or after K rounds. Always end on step (3). Report leftover per fabric and where it is (which panel, near which contact).
- Risk: does not converge where the garment is too small for the body or two layers fight; then stretch stays and must be reported as a fit fault (Wang's dragon is the published example of this). Possible bulges from the final push where cloth takes the body's shape (Vellum's protrusions); a small smoothing pass before the final push may limit them (untested suggestion). Extra cost per frame about K times one strain sweep plus one body query, offline so acceptable.
- Size (estimate): 6 to 10 h for an AI coder including tests (loop and stop rule 2 h, contact weighting 1 to 2 h, moving layer finish and seam join into the loop 2 to 3 h, reporting and gate wiring 1 to 2 h, runs on the gate jobs 1 h).

Option C (add after B if global stretch remains): long range attachments from holds.
- Changes: one-sided geodesic tethers from waistband or shoulder holds, inside the loop before step (3).
- Risk: geodesic precompute on garments with seams across panels; euclidean is "very prone to artifacts" (Chaos docs).
- Size (estimate): 4 to 6 h.

Option D (not recommended now): unified barrier solve (C-IPC style). Strict guarantees, but a new solver, many times slower, weeks of work.

Measurable check that proves Option B, on every gate job (trousers, jacket, each layered pair):
- body-through count 0 at the final frame and at every saved frame;
- worst edge ratio per fabric at or under its limit plus a stated tolerance (suggest 0.02, so 1.14 for a 1.12 fabric), and the 99th percentile edge ratio reported too;
- cloth-cloth through count 0 between layers;
- leftover reported per job (worst edge, its panel, whether it touches contact, rounds used), and a job that cannot meet both fails as a fit fault, not silently;
- regression rows: the 2.875 jacket edge, the 1.242 trousers edge, and a deliberately undersized garment that must fail with a clear report;
- a fresh reviewer compares before and after frames for new protrusions at contact.

## Unreached sources (not evidence)

- Goldenthal et al. 2007 full PDF, http://www.cs.columbia.edu/cg/pdfs/131-ESIC.pdf : permission request timed out.
- NVIDIA PhysX 3.4 cloth manual, https://docs.nvidia.com/gameworks/content/gameworkslibrary/physx/guide/Manual/Cloth.html : blocked by the site (robots).
- PhysX 3.4.1 cloth manual mirror, https://documentation.help/NVIDIA-PhysX-SDK-3.4.1/Cloth.html : site error.
- Unreal current UChaosClothConfig page, https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/ChaosCloth/UChaosClothConfig : page returned no content.
- Thomaszewski et al. 2009 full text: only the abstract page was found.
- C-IPC (Li et al. 2021) and Wang et al. 2016: abstracts only; cost figures not read.
- Provot 1995: not re-read this run (team has read it). Bridson 2002 was re-read by the reviewer, see section 1.
