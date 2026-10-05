# Topic 8: markerless motion capture and free animation sources

STATUS: SPEC (research delivery). Branch `research/markerless-mocap`, from commit
`074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written, no tool adopted.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged: no
external page was read in full. Repository claims name their file and line.

**D28 DOES NOT EXIST IN THIS CHECKOUT.** The brief says "D28 parks animation
polish until presentation is right". Measured this session: a grep for `D28` and
for `D25` through `D29` across every markdown file in the repository returns zero
hits, and the D-numbered spine in
`ledger-v2/respec/decision-register/rulings-log.md` runs D1 to D18. This is the
second such record the brief cites that is not here; the coverage audit found the
same for D24. Recorded as a hole and not filled. The brief's statement of the
policy is used as given, and it agrees with two things that ARE in the
repository: `ledger-v2/respec/vision-pillars-v2.md` names "Animation parity with
mocap studios" on the "Worse at, and at peace with it" list, and
`production/ladder.md` puts "one face that moves" at rung 5.

This topic asks for a plain verdict. Section 1 is it.

## 1. The verdict: no, not now, and one small exception

**Bespoke motion capture is not worth doing for this project at this stage.** The
argument is five facts, four of them from this repository:

1. **The licence position is much worse than the phrase "free mocap libraries"
   suggests**, and it eliminates most of the option space (section 2).
2. **The one genuinely free library is CMU**, and it is 2,500 sequences of
   early-2000s academic capture, which is a different thing from twenty bespoke
   movements (section 2.1).
3. **Cleanup is the cost, and it is measured in animator-hours we do not have**
   (section 4).
4. **The route we are on works.** The tile "bodies and faces" reads "92 rigs,
   heights 1.58 to 1.91, Mixamo clips advancing, feet solved, nobody in a
   T-pose". Mixamo is free, on the allowlist by name, and 2,500-plus clips deep.
5. **The animation we already have is not wired.** The same tile records that
   "`Core/MotionMatch.cs` has no caller in the Game layer walked here". Adding
   twenty bespoke clips to a motion system nothing calls is building the second
   floor of a house with no stairs.

**THE EXCEPTION, and it is the only recommendation in this file:** a footskate
cleanup TOOL, not a mocap pipeline. Section 5 is the argument, and the short
version is that the single biggest tell of amateur animation has a known
algorithmic fix, and writing algorithmic fixes with a printed number attached is
the thing this studio is actually good at.

## 2. The licence finding, which is the important half of this topic

### 2.1 CMU is free. AMASS is not. And AMASS is the good one.

CITED (search summaries of re3data's CMU Graphics Lab entry and MoCap Online's
free-mocap guide): the CMU Graphics Lab Motion Capture Database has been
maintained since the early 2000s, holds "over 2,500 motion sequences", is
available with no licence fee, "was originally released under a permissive
licence", and "while the original terms predate modern open-source conventions,
it has been widely used commercially without issue".

CITED (search summaries of the AMASS licence page and the AMASS GitHub
repository): the AMASS licence "grants use of the dataset for the sole purpose of
performing non-commercial scientific research, non-commercial education, or
non-commercial artistic projects, with any other use, particularly for commercial
purposes, prohibited. This includes incorporation in a commercial product, use in
a commercial service, or production of other artifacts for commercial purposes."
Commercial licensing is by enquiry to the Max Planck Institute.

DERIVED, and it is the shape of the problem: AMASS is the archive that made free
mocap usable, because it unifies roughly two dozen separate capture datasets into
one parameterisation. CMU is one of the datasets it unified. **So the thing that
made the free libraries convenient is the thing that cannot ship, and what
remains shippable is the raw, unnormalised, twenty-year-old source.**

### 2.2 And the restriction travels downstream, into the AI models

This is the finding I did not expect and it is the one with teeth.

CITED (search summaries of the HumanML3D GitHub repository and EmergentMind's
dataset page): "HumanML3D originates from the AMASS motion collection" and
"comprises 14,616 distinct motion sequences sourced from the AMASS collection".
And: "Due to the distribution policy of AMASS dataset, HumanML3D cannot be
distributed directly, but scripts are provided to reproduce the HumanML3D dataset
from AMASS dataset."

HumanML3D is the standard training and benchmark set for text-to-motion. CITED
(search summaries of the MoMask and MDM papers and the survey on multimodal
motion generation): MDM "introduces a diffusion-based generative model trained
separately on various motion tasks", MoMask "performs hierarchical masked 3D
human motion generation", and these are the models a project would reach for to
generate "the handful of movements nothing else has".

DERIVED, and flagged as the reason this needs a lawyer's eye rather than mine:
**a text-to-motion model trained on HumanML3D inherits a question about AMASS's
non-commercial terms, and the allowlist's own discipline is exactly this.** The
allowlist's process clause says "New tool adoption requires a decision record
citing the weights license", and its own top line is "verify weights license, not
code license". An MIT-licensed repository whose weights were trained on a
non-commercial dataset is the precise case that clause exists for, and it is the
same shape as the entries already on the NEVER SHIP list ("XTTS-v2 or F5-TTS
official weights output (non-commercial)").

**HOLE, and it is important that I am honest about its size.** Whether a model's
OUTPUT is encumbered by its training data's licence is a contested legal question
and I am not qualified to answer it, could not read the licence text, and am not
asserting that it is. What I establish is narrower and sufficient: the chain from
AMASS to HumanML3D to these models is documented by the projects themselves, and
AMASS's terms are explicitly and specifically anti-commercial. That is enough to
put every open text-to-motion model in the same category the allowlist already
uses for XTTS-v2, which is "do not build on this until somebody has checked".

### 2.3 What is left after the licence pass

| Source | Shippable? | What it is |
|---|---|---|
| Mixamo | **Yes**, on the allowlist by name, and already in use | 2,500-plus clips, biped only |
| CMU mocap | **Probably**, per 2.1, with the caveat about pre-modern terms | 2,500-plus sequences, early-2000s academic capture |
| AMASS and the academic collections it unifies | **No** | non-commercial by its own licence |
| HumanML3D | **No**, inherits AMASS | 14,616 sequences |
| Open text-to-motion models trained on HumanML3D | **Unresolved**, and treat as no until checked | MDM, MoMask, MLD and the rest |
| Free stock video plus pose estimation | **Yes on licence, expensive in labour** | section 3 |
| Hosted video-to-motion services | **Per their terms**, not surveyed here | Rokoko, DeepMotion, Move.ai, Plask |

## 3. What free video plus pose estimation actually produces

CITED (search summaries of Uthana's 2026 motion-capture tool round-up, the
PhysCap paper's abstract and the Motion2Motion paper): physics-based monocular
capture "can significantly reduce common artifacts like motion jitter,
penetration into the floor, foot sliding and unnatural body leaning", while
"lower-end video-based pose estimation methods exhibit occasional jitter and
limited handling of occlusion". The metrics named for evaluating a take are "root
trajectory, foot sliding, joint jitter, missed contacts, body orientation, hand
behavior, processing time, and cleanup required". And on the practical side:
"Cleanup involves filling gaps from occlusion, filtering jitter, and locking foot
contacts to stop sliding. On a good take this cleanup takes minutes per clip; on
a bad one it takes hours."

DERIVED, and it answers the brief's framing directly: the brief says pose
estimators "inherit sliding feet and jittering limbs", and that is right, but the
sources say something more useful. Those are not one problem, they are a NAMED
LIST of eight measurable faults, and the list is the interesting part. A project
whose whole method is "make the system print the series, read it, then set the
bound" has an obvious relationship to a list of eight metrics that decide whether
a take is usable.

## 4. The twenty bespoke movements, priced

CITED (search summaries of MoCap Online's cleanup workflow guide and the
footskate-cleanup literature, including the UnderPressure paper and Kovar et
al.'s "Footskate Cleanup for Motion Capture Editing"): "An experienced technical
animator typically spends 2 to 4 hours cleaning a single minute of
production-quality motion capture animation." Foot sliding "is the most visible
mocap artifact and audiences notice it instantly, even small amounts of foot
slide destroy the illusion of weight and contact". It happens because "foot bones
continue to move during contact phases due to root bone velocity" and because
capture is "typically collected on soft flexible mats". The professional fix is
"detecting foot plant frames, locking foot position by pinning the foot IK target
to a fixed world position during plant frames, blending in and out, and adjusting
pelvis height to compensate for leg length changes that locking introduces".

DERIVED, with the arithmetic printed and its assumption named. ASSUMED: twenty
movements at 3 to 5 seconds each, so 60 to 100 seconds, call it 1.3 minutes.

| Route | Cleanup estimate | Reasoning |
|---|---|---|
| If the source were studio mocap | 2.7 to 5.3 hours | 1.3 minutes at 2 to 4 hours per minute |
| From video plus pose estimation, good takes | about 3 hours | 20 clips at "minutes per clip" |
| From video plus pose estimation, bad takes | 20 to 60 hours | 20 clips at "hours" each |

Plus, and not in the table: capturing the footage, retargeting to the rigs,
importing to Unreal, and the iterations that any of the above will need.

**So the honest number is roughly 20 to 80 hours of skilled animation labour, and
the project has no animator.** Jafar directs on evenings and weekends and is
non-technical by his own description; every implementer here is an agent. Twenty
to eighty hours of a skill nobody in the project has is not a budget line, it is
a hiring decision.

## 5. The exception, and why it is the right shape for this studio

The 2-to-4-hours figure is for HAND cleanup. Footskate is not a taste problem, it
is a geometry problem with a published algorithm, and the fix is stated above as
four mechanical steps: detect plant frames, pin the IK target, blend, compensate
the pelvis. It has been in the literature since Kovar et al. and has a recent
deep-learning treatment (UnderPressure, 2022) aimed at exactly this.

DERIVED, and it is the only thing in this file I would actually recommend:

- The single biggest tell of amateur animation has a known algorithmic fix.
- The project's comparative advantage is writing tools that measure and correct
  things, with a printed number attached. That is what
  `.claude/rules/instruments.md` is a whole document about.
- The metrics list in section 3 is already the gate: root trajectory, foot
  sliding, joint jitter, missed contacts, body orientation, hand behaviour.
- And it improves the clips we ALREADY HAVE. The tile says "Mixamo clips
  advancing, feet solved", so something is already solving feet; a measured
  footskate number would say how well, on the 64 clips already shipped, for free.

That is a small instrument job with an immediate readout on existing content,
and it is the opposite shape from a mocap pipeline, which is a large labour job
with a payoff that arrives at rung 5.

## 6. Why the answer is no, restated against the project's own sequencing

Three things in this repository already say animation waits, and none of them is
D28:

- Pillar list: "Animation parity with mocap studios" is named on "Worse at, and
  at peace with it", which exists so "nobody quietly reopens them without a
  decision record".
- `production/ladder.md`: rung 1 is the street matched to the Hook sheet, rung 5
  is "one face that moves".
- The tile: `Core/MotionMatch.cs` has no Game-layer caller.

And two things from my own earlier deliveries say the budget is elsewhere: topic
1 and topic 2 both independently recommend the same voice-model evaluation as the
next cheap high-value step, and topic 2 found the video-memory floor does not
currently fit the machine the game is built on.

**Twenty bespoke movements would be the best possible answer to a question nobody
is asking yet.**

## 7. What could not be established

1. **D28.** Does not exist in this checkout (section 0). Second missing record
   the brief cites.
2. **The actual CMU licence text.** Every claim about it is a summariser's
   characterisation, including the phrase "widely used commercially without
   issue", which is a statement about practice and not about terms. Before
   anybody ships a CMU-derived clip, somebody should read the terms.
3. **Whether a model's output inherits its training data's licence** (2.2). A
   contested legal question, outside my competence, flagged rather than answered.
4. **The commercial terms of the hosted video-to-motion services** (Rokoko,
   DeepMotion, Move.ai, Plask, QuickMagic). Not surveyed. Some have free tiers
   whose output licence is the whole question, and this repository's own
   `ai-gamedev-feasibility-FULL.md` already notes Cascadeur's free tier "went
   non-commercial in mid-2026", which is the pattern to expect.
5. **AI-generated VIDEO** as a motion source, as distinct from text-to-motion.
   The brief asks about it specifically and my searches returned marketing pages
   for video tools rather than any evaluation of pose extraction from generated
   footage. The brief's own statement of the problem, that generated footage has
   soft physics which estimators then inherit, is the most substantive thing I
   have on it, and I could not improve on it.
6. **How many clips we actually have and what they cover.** The verify footer
   reads "clips ok (64 read, 2 known finding(s))" and I did not enumerate the 64
   or establish what movements they are, so "what twenty movements would add" is
   unanswered.
7. **Whether Mixamo is still being maintained.** This repository's own research
   file says it is "in maintenance mode and biped-only" and "briefly broke in
   mid-2025", which is a risk to a route the allowlist depends on, and I did not
   re-check its current state.

## 8. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- AMASS licence page, Max Planck Institute, https://amass.is.tue.mpg.de/license.html
- AMASS project page, https://amass.is.tue.mpg.de/
- GitHub, "nghorbani/amass", https://github.com/nghorbani/amass
- GitHub, "EricGuo5513/HumanML3D", https://github.com/EricGuo5513/HumanML3D
- EmergentMind, "HumanML3D: Text-to-Motion Dataset", https://www.emergentmind.com/topics/humanml3d-dataset
- re3data, "CMU Graphics Lab Motion Capture Database", https://www.re3data.org/repository/r3d100012183
- MoCap Online, "Free Motion Capture Animations Guide", https://mocaponline.com/blogs/mocap-news/free-motion-capture-animations-guide
- MoCap Online, "MoCap Data Cleanup Workflow: From Raw Capture to Production", https://mocaponline.com/blogs/mocap-news/mocap-data-cleanup-workflow
- MoCap Online, "Blender Mocap: Import, Retarget, and Animate Characters", https://mocaponline.com/blogs/mocap-news/blender-motion-capture-guide
- Uthana, "Best AI Motion Capture Tools in 2026", https://uthana.com/resources/best-ai-motion-capture-tools
- arXiv 2008.08880, "PhysCap: Physically Plausible Monocular 3D Motion Capture in Real Time", https://arxiv.org/pdf/2008.08880 (EGRESS BLOCKED)
- arXiv 2312.00063, "MoMask: Generative Masked Modeling of 3D Human Motions", https://arxiv.org/pdf/2312.00063 (EGRESS BLOCKED)
- arXiv 2506.03191, "Multimodal Generative AI with Autoregressive LLMs for Human Motion Understanding and Generation", https://arxiv.org/pdf/2506.03191 (EGRESS BLOCKED)
- ScienceDirect, "Motion2Motion: Learning human pose refining in videos without ground truth label", https://www.sciencedirect.com/science/article/abs/pii/S003132032600573X
- Wiley, "UnderPressure: Deep Learning for Foot Contact Detection, Ground Reaction Force Estimation and Footskate Cleanup", https://onlinelibrary.wiley.com/doi/abs/10.1111/cgf.14635
- University of Wisconsin, Kovar et al., "Footskate Cleanup for Motion Capture Editing", https://research.cs.wisc.edu/graphics/Gallery/kovar.vol/Cleanup/cleanup.pdf
- Sunstrike Studios, "How Motion Capture Works in Video Games: Full Mocap Guide 2026", https://sunstrikestudios.com/en/blog/motion_capture_for_games_and_film/
- Pixel Pastry Studios, "How to Set Up Performance Capture at Home on a Budget in 2026", https://www.pixelpastry.com/how-to-set-up-performance-capture-at-home-on-a-budget-in-2026/
- QuickMagic, "Free AI Text to Motion Generator", https://www.quickmagic.ai/tools/text-to-motion

Repository sources, read this session at commit `074f85b`:
`production/systems-inventory.json`, `production/ladder.md`,
`ledger-v2/respec/vision-pillars-v2.md`,
`ledger-v2/research/license-allowlist.md`,
`ledger-v2/research/full/ai-gamedev-feasibility-FULL.md`,
`ledger-v2/respec/decision-register/rulings-log.md`,
`ledger-v2/studio-v2/casebook-claims.md`, `.claude/rules/instruments.md`.
