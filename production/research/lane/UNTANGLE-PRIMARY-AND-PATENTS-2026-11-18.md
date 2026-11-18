# Untangling a sleeve end from the forearm: primary-source pass

Date of all reads: 18 Nov 2026. Helper research, about 25 minutes, no machine work.
Problem as given: in a position-based draping tool, a sleeve end starts tangled with the forearm (the cloth ring does not go round the arm).

Marks: PRIMARY = read in the authors' own text (paper, thesis, or the inventors' patent). SECONDARY = another author's description, a summary page, or a tool's summary of a page.

## Headline

- None of the four target papers' full text was reachable from here. The Pixar PDF link redirects to a Pixar landing page that timed out on approval; the Eurographics library records for Ye and Zhao 2012 and Ye et al. 2017 show no open file; no open copy of Volino and Magnenat-Thalmann 2006 turned up.
- The closest primary text for Baraff, Witkin, Kass is their own Pixar patent US 6,970,171 (same inventors, same method, full description on Google Patents and Justia). It was read.
- Two later primary texts describe and test the classic methods in detail: Sun, Nyberg, Xiong, Ye (Eurographics 2016 short paper, cloth vs obstacle) and Cha (SNU PhD thesis 2022, untangling with comparisons to GIA, ICM and UIR). Both read; they are PRIMARY for their own methods and SECONDARY for the classic papers.
- Both Pixar patents are expired (term ran out; all maintenance fees were paid).
- One open-source framework (OpenXRLab XRTailor, position-based cloth on GPU) states it uses global intersection analysis with ICM-style untangling. Its licence was not reached. ContourCraft (2024) code exists; its licence was not reached.

## 1. The four papers

### 1a. Baraff, Witkin, Kass 2003, "Untangling Cloth" (SIGGRAPH 2003)

Full text: Unreached (Pixar PDF redirect, see Unreached). Read instead: the abstract on the SIGGRAPH history archive and the inventors' patent US 6,970,171 description.

- Scope (SECONDARY, SIGGRAPH archive abstract): history-free cloth-cloth response that analyses intersections over the whole mesh each step and untangles as soon as geometry allows, including tangled starting states; a separate cloth-solid method, "collision flypapering", for pinches.
- Cloth vs solid body (PRIMARY, patent): the body is animated (kinematic), the cloth simulated. Oriented surfaces (bodies) define an inside, and "objects should always be ejected from this interior region if they manage to get inside." Cloth is "an unoriented surface". The attraction and repulsion rules apply "whenever surfaces are unoriented and at least one of the surfaces is simulated." So cloth into body is resolved by pushing out of the body's inside, not by the colouring rules. Pinching (cloth caught between two body parts whose insides disagree, for example the elbow crook) is detected and the pinched vertices have their motion constrained rather than being pushed; the patent says such cloth may be "completely immobilized". Flypapering itself is a separate Pixar patent application (US 2002/0118197) not read.
- Open boundaries (PRIMARY, patent): the description only treats closed intersection paths, traced "until one arrives back at the initial edge/face intersection". Cloth boundary edges are not discussed. A path is discarded when both sides escape the local "playpen" region. SECONDARY (ContourCraft 2024 and Cha 2022): GIA "does not address open-contour intersections such as penetrating pairs of mesh boundaries"; in Cha's tests GIA and UIR "do not take any actions for the LL cases".
- Moves (PRIMARY, patent): forces, not position corrections. Each intersection path colours the two sides (two meshes: black and white; one mesh self-intersecting: red) by breadth-first "playpen" then flood fill on each side; the side that stays inside the playpen is the interior. Rules on close vertex pairs: opposite colours from different regions switch from repulsion to attraction "to pull the cloth back through itself"; red with red gets neither; all others get normal repulsion.
- Cost and timings: not in the patent text read; Unreached for the paper.
- Failure cases (PRIMARY, patent): point or whole-plane contacts are not handled (random noise is added to avoid them); open paths fall outside the method as written.

### 1b. Volino and Magnenat-Thalmann 2006, "Resolving surface collisions through intersection contour minimization" (ACM TOG / SIGGRAPH 2006)

Full text: Unreached. Read: SIGGRAPH archive abstract, and descriptions in ContourCraft 2024, Sun et al. 2016 and Cha 2022.

- Idea (SECONDARY, archive abstract): separate two intersecting surface regions by relative displacements that minimise the length of the intersection contour; does not depend on finding intersection regions, so it applies more widely than region-based methods and is simpler to implement.
- Moves (SECONDARY, ContourCraft): for each intersecting triangle pair, the gradient of intersection length with respect to the involved vertices; vertices moved against it, iteratively and locally. ContourCraft splits the gradient into a translational part along the face normal and a distortional part in the plane, and keeps only the translational part because the other "induces compression". Cha: ICM "applied force/displacement to vertices in a way that would shorten the intersection in each triangle." So it works as either a displacement or a force; a position-based tool would use it as a displacement.
- Open boundaries (SECONDARY, ContourCraft): ICM was the method meant to fill GIA's open-contour gap; since it works per segment of contour, an open contour (one that ends on a boundary edge, such as a sleeve hem) still has length to shrink.
- Cloth vs solid (SECONDARY, Sun et al. 2016): ICM "is actually less effective for configurations involving oriented surfaces", and its global step does "a brutal averaging of all displacements for vertices along an intersection contour". A body is an oriented surface, so plain ICM is the weaker choice for cloth vs body.
- Cost and failures (SECONDARY, Ye and Zhao 2012 abstract): ICM "often fails or converges slowly when surface orientation matters"; Sun et al. repeat that ICM "often exhibits unpredictable convergence behavior".

### 1c. Ye and Zhao 2012, "The Intersection Contour Minimization Method for Untangling Oriented Deformable Surfaces" (SCA 2012)

Full text: Unreached (Eurographics record shows no open file). Read: the authors' abstract on the Eurographics digital library (PRIMARY for the abstract only) and Cha 2022's restatement.

- Cloth vs solid (PRIMARY, abstract): adds a "repulsive normal" to ICM so it works when one surface is oriented; this "resolves many previously failing configurations" and speeds up others. It also extends ICM from mesh vs mesh to mesh vs capsule (an analytic surface). A capsule is a common forearm proxy, so this is the closest match to the sleeve case.
- Moves (SECONDARY, Cha 2022): per intersecting edge E against a penetrated face with normal N, direction G = R + T, where R is the sum of two outward unit vectors lying in the penetrated surface and T = -(E.R)/(E.N) N.
- Open boundaries: not stated in what was read.
- Cost and timings: not reached.
- Failure cases (SECONDARY, Cha 2022): for a cone-shaped BLI tangle (path from a mesh boundary, through a loop vertex, ending inside the mesh) the method "loses its ability" to produce a useful direction and gets stuck.

### 1d. Ye, Ma, Jiang and others 2017, "A Unified Cloth Untangling Framework Through Discrete Collision Detection" (Computer Graphics Forum, DOI 10.1111/cgf.13287)

Full text: Unreached (Eurographics record shows no open file; Bohrium copy behind a firewall check). Read: the abstract on the Eurographics digital library (PRIMARY for the abstract only), Cha 2022 (SECONDARY).

- Method (PRIMARY, abstract): the Unified Intersection Resolver (UIR) handles impending collisions and existing penetrations in one pass. Edge-face intersections are detected with discrete collision detection and grouped into four-vertex stencils (vertex-face or edge-edge); vertices are relocated iteratively along a collision normal taken from predefined surface orientation, from history, or from global intersection analysis. Stencils forming one penetration region are resolved together, and it frees cloth trapped in pinched objects.
- Cloth vs solid (PRIMARY, abstract): the body's predefined orientation supplies the normal; pinch handling is claimed.
- Moves: position corrections. SECONDARY (Cha): UIR "calculated the minimal displacements for resolving the penetrations" with a stencil formulation.
- Open boundaries (SECONDARY, Cha): Ye et al. use properties of BIBI and BBII tangles (paths ending on boundaries) to find the region to resolve, but "BLI still remains unsolved"; UIR takes no action on LL cases.
- Cost and timings: not reached.

### 1e. Related primary texts read (useful for the sleeve case)

Sun, Nyberg, Xiong, Ye 2016, "Minimum Displacements For Cloth-obstacle Penetration Resolving" (Eurographics short paper). PRIMARY.
- Body must be watertight and oriented with outward normals. Discrete detection finds cloth edge vs body face crossings; the edge vertex on the negative side is marked illegal and moved along face normals until its signed distance reaches d (cloth thickness). Minimum-norm displacement per impact zone by Lagrange multipliers; repeat until no edge-face crossings remain. Position corrections, history free.
- Timings: integrated in ARCSim; over two 500-frame runs, total 3344.2 s against ARCSim's 3931.8 s, single thread (table partly garbled in extraction).
- Failure cases named by the authors: an arm pushed into a sleeve where the cylinder's orientation gives no moving direction cannot be resolved; a closed surface's normal can trap cloth in a local minimum. This is close to the case in hand and is the key warning.
- Self-collision of one mesh not supported.

Cha 2022, "Convergence Guaranteed Untangling for Clothing Simulation" (Seoul National University PhD thesis, CC BY-NC-ND 2.0 Korea). PRIMARY for its own method.
- Tangle classes after Wicke et al.: CLOSED, CROSS, EIGHT, LL, BIBI, BBII, BLI, where B means the path meets the mesh boundary, I ends inside, L passes a loop vertex. A sleeve hem ring stuck through the forearm is a boundary-touching (B) class case on the cloth side.
- Method: changes the rest shape (pull, triangle shrink, revoke, scaled by 0.8 at a 0.02 s step) and lets internal forces untangle the world mesh. Guarantees finite-time resolution for flat-pattern cloth except BLI; separate BLI resolvers (mesh tearing, regional flip, crease flip).
- Cloth vs body: no dedicated method; notes that sharp body parts (fingers) block edge shortening and suggests capping them; lapels and collars prone to fail against the bodice.
- Timings: 388-triangle handkerchief resolved in 75 steps; typical clothing 161 steps on average; interactive run about 1.56 fps; slower than one-shot methods.

## 2. Pixar patents

Sources: Google Patents pages for US6970171 and US7355600 (legal-event tables and bibliographic data), Justia page for 6970171. Read 18 Nov 2026. PRIMARY for the recorded dates (taken from the USPTO data those pages reproduce); the expiry status is Google's assumption, not a legal finding.

| | US 6,970,171 B2 | US 7,355,600 B2 |
|---|---|---|
| Application | 09/851,940 | 11/090,767, continuation of 09/851,940 |
| Filed | 10 May 2001 (no provisional listed) | 24 Mar 2005 |
| Earliest non-provisional filing | 10 May 2001 | 10 May 2001 |
| Granted | 29 Nov 2005 | 8 Apr 2008 |
| Maintenance fees | years 4, 8, 12 paid (2009-04-23, 2013-05-08, 2017-05-18) | years 4, 8, 12 paid (2011-09-22, 2015-09-23, 2019-10-03, large entity) |
| Google status | Expired - Lifetime | Expired - Lifetime |
| Google expiry | 12 Aug 2022 (adjusted) | 10 May 2021 |
| Computed expiry | 20 years from 10 May 2001 = 10 May 2021, plus term adjustment; Google's adjusted date 12 Aug 2022 implies about 459 days of adjustment (the adjustment figure itself was not seen) | 10 May 2021 (a continuation takes the parent's earliest filing date; no adjustment shown) |
| Status on 18 Nov 2026 | Expired at end of term, not lapsed for fees | Expired at end of term, not lapsed for fees |

Inventors Baraff, Witkin, Kass; assignee Pixar. The 7,355,600 independent claims cover polarity of vertices inside an intersection path, pinch detection with motion constraints, boundary finding by radial search, and attraction or repulsion by path membership. The separate flypapering application (US 2002/0118197) and pose-based flypapering patent (US 8,436,861) were seen only as citation titles; their status was not checked.

## 3. Open-source code

- OpenXRLab XRTailor (position-based and XPBD cloth on GPU). SECONDARY (its own documentation, read through a summary): the "Detangle" section says it employs global intersection analysis and follows reference [24], which is Volino and Magnenat-Thalmann 2006. The documentation says detangling targets cloth self-interpenetration; cloth vs obstacle contact is handled separately; it does not say detangling covers cloth vs body. Repository named in the docs: github.com/openxrlab/xrtailor. Licence: Unreached (the docs footer shows only a copyright line; the repository page was not fetched). A sister project, XRFeitoria, is Apache-2.0, which says nothing about XRTailor.
- ContourCraft (Grigorev and others, SIGGRAPH 2024). SECONDARY: a learned garment simulator using an intersection-contour loss derived from ICM, for cloth vs cloth (body contact by a separate term). Repository named on a mirror listing: github.com/Dolorousrtur/ContourCraft. Licence: Unreached (repository fetch refused).
- No open code was found implementing GIA or ICM specifically for cloth vs body.

## What this suggests for the sleeve (decision for the builder, not a finding of the papers)

- The forearm is a closed, oriented body, so the professional route is the oriented one: decide inside/outside against the body and push cloth vertices out along body normals to a thickness offset (Pixar patent rule; Sun et al. 2016; UIR uses the body's orientation as its normal source). Colouring (GIA) and plain ICM are cloth-cloth tools; GIA as written ignores open paths such as a hem.
- The known failure is exactly this shape: Sun et al. name "arm pushed into a sleeve" as unresolvable by normals alone. Ye and Zhao's capsule extension with repulsive normals targets the arm-proxy case. A practical reading: use a capsule proxy for the forearm and push the sleeve ring radially out from the capsule axis (a direction that always exists), rather than along nearest-face normals, then hand over to the normal mesh collision.
- Simplest robust alternative used by every method's assumptions: start the drape from a state with no intersection (for example a scaled-up or offset sleeve) so untangling is never needed. This is outside the papers and needs its own check.

## Sources read (18 Nov 2026)

- Google Patents, US6970171 (two reads, legal events): https://patents.google.com/patent/US6970171 PRIMARY (dates, description)
- Google Patents, US7355600 (two reads): https://patents.google.com/patent/US7355600 PRIMARY (dates, claims)
- Justia, 6970171: https://patents.justia.com/patent/6970171 PRIMARY (description quotes, dates)
- SIGGRAPH history archive, Untangling Cloth: https://history.siggraph.org/?p=115940 SECONDARY (abstract)
- SIGGRAPH history archive, Volino 2006: https://history.siggraph.org/?p=113608 SECONDARY (abstract)
- Eurographics library, Ye and Zhao 2012 record: https://diglib.eg.org/handle/10.2312/SCA.SCA12.311-316 PRIMARY (abstract only)
- Eurographics library, Ye et al. 2017 record: https://diglib.eg.org/items/8f4e4417-9f92-4b61-b013-f748a3a25602/full PRIMARY (abstract only)
- Sun, Nyberg, Xiong, Ye 2016: https://diglib7.eg.org/bitstream/handle/10.2312/egsh20161013/053-056.pdf PRIMARY
- Cha 2022 thesis: https://core.ac.uk/download/522190958.pdf PRIMARY (own method), SECONDARY (others)
- ContourCraft, arXiv HTML v2: https://arxiv.org/html/2405.09522v2 PRIMARY (own method), SECONDARY (ICM, GIA)
- XRTailor technical brief: https://xrtailor.readthedocs.io/en/latest/getting_started/technical_brief.html SECONDARY
- UW-Madison CS777 student summary: https://research.cs.wisc.edu/graphics/Courses/777-s2006/TextWeb/Summaries/Week11/krill-untangle.txt SECONDARY (adds nothing new)
- relatedrepos listing for ContourCraft: https://relatedrepos.com/gh/Dolorousrtur/ContourCraft SECONDARY (repo URL only)

## Unreached (not evidence)

- Pixar paper PDF and page (graphics.pixar.com/library/UntanglingCloth, paper.pdf): redirect to pixar.com/technology-libraries, whose fetch timed out on approval.
- Volino and Magnenat-Thalmann 2006 full text: no open copy found.
- Ye and Zhao 2012 full text: no open file on the Eurographics record.
- Ye et al. 2017 full text: no open file; Bohrium page behind a firewall check.
- github.com/Dolorousrtur/ContourCraft: fetch refused (approval not answered); repository also outside this session's GitHub access.
- XRTailor raw documentation source (readthedocs _sources): fetch refused.
- github.com/openxrlab/xrtailor: not fetched, so its licence is unknown.
- is.mpg.de ContourCraft page: bot-check page only.
- USPTO image-ppubs patent PDFs: found, not needed (Google Patents carried the same data); not read.
