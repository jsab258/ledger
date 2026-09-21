# RECHECK: the licence pages, read this time, and whether a commercial route exists

STATUS: SPEC (research recheck). Branch `research/markerless-mocap`, added on
top of `db6bfbd`. Written 2026-09-19 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No tool adopted, no queue item, no
decision record. I am not a lawyer and section 5 says where that bites.

## 0. Which pages opened and which did not

Measured this session. `datashare.ed.ac.uk` 200 and
`raw.githubusercontent.com` 200, so licence texts were read in full from both.
Still refused with a gateway 403 to CONNECT: `amass.is.tue.mpg.de`,
`mocap.cs.cmu.edu`, and `github.com` itself (its raw host is the way in).

So the two licences topic 8 leaned on hardest, AMASS's and CMU's, are STILL
search summaries and are not upgraded by this file. What is upgraded is
different and in one case sharper.

## 1. The Edinburgh licence, read in full, and it is the best sentence in this topic

First, what is actually there. Edinburgh DataShare was searched through its
DSpace REST API, not guessed at: "motion capture" returns 18 items, "mocap"
returns 1, and searches for `Komura`, `Holden`, `MOCAP Database`, `100STYLE`,
`gait capture` and `style locomotion` return nothing relevant. **There is no
human locomotion mocap database on Edinburgh DataShare.** The only human motion
capture item is orchestral conducting, and the only other motion-adjacent item
is a set of videos of a person holding still.

The rights statement on that item, `10283/2913`, read in full from its
metadata, quoted exactly:

> All six participants consented to share the recordings with research
> professionals. The recordings may be of interest to researchers examining
> movement associated with expressive and communicative performance, therefore
> they are shared here with the intention of further academic research. **The
> recordings are not permitted to be used for commercial, artistic, or
> entertainment purposes.** Otherwise, the provisions of the Creative Commons
> License: Attribution 4.0 International apply.

THIS IS THE FINDING AND IT GENERALISES. An academic dataset can carry a
CC BY 4.0 label and still bar entertainment use in the same sentence. A game is
entertainment. Reading the licence LABEL is not reading the licence, and the
whole of topic 8 section 2 was built on labels reported by a summariser.

For contrast, on the same repository: the Human MotionLess Dataset,
`10283/8851`, carries plain "Creative Commons Attribution 4.0 International
Public License" with no carve-out. Same host, same label, different terms. So
the rule is per item, never per repository.

## 2. LAFAN1, read from the dataset's own repository

Not examined in topic 8 at all, and it is the obvious candidate a reader would
reach for next: 77 sequences, 496,672 frames at 30fps, about 4.6 hours, themed
walk, run, sprint, obstacles, fall and get up.

Its README states its own terms: "This dataset can be used under the Creative
Commons Attribution-NonCommercial-NoDerivatives 4.0 International Public
License."

Non-commercial AND no-derivatives. No-derivatives forecloses retargeting and
cleanup even where non-commercial would not. Closed, and closed twice.

## 3. HumanML3D, confirmed from primary, plus a dependency topic 8 missed

Topic 8's chain from AMASS to HumanML3D was a search summary. It is now the
project's own words, from its README: "Due to the distribution policy of AMASS
dataset, we are not allowed to distribute the data directly. We provide a series
of script that could reproduce our HumanML3D dataset from AMASS dataset."

And a second encumbrance topic 8 did not record: reproducing it requires the
SMPL+H body model from `mano.is.tue.mpg.de` and DMPL from `smpl.is.tue.mpg.de`.
Those are separate Max Planck licences on separate download pages, both refused
here. So the chain has two MPI links in it, not one, and neither was read.

## 4. The half topic 8 did not licence-check, which is where the answer lives

Topic 8 licence-checked datasets and motion-generation models. It did not check
the pose estimators, which are the actual markerless pipeline. Read in full from
each project's own repository this session:

| Software | Licence file says | Usable commercially |
|---|---|---|
| MediaPipe (Google) | Apache License 2.0 | **Yes** |
| MMPose (OpenMMLab) | Apache License 2.0 | **Yes** |
| OpenPose (CMU) | "ACADEMIC OR NON-PROFIT ORGANIZATION NONCOMMERCIAL RESEARCH USE ONLY" | **No** |
| MDM (motion-diffusion-model) | MIT, for the code | see below |

MDM is the case topic 8 section 2.2 described and it is confirmed: an MIT
LICENSE on the repository, and a README whose data instructions route through
HumanML3D and `download_smpl_files.sh`. The code licence says nothing about
what the weights were trained on. Topic 8's judgement to treat open
text-to-motion models as "do not build on this until somebody has checked"
stands, now anchored on the repository's own setup instructions rather than a
summary.

## 5. So: does a commercially usable route exist? Yes, and it is not a library.

**Yes.** Shoot your own footage and run an Apache-2.0 estimator over it. Nothing
in that chain is encumbered: the software is Apache 2.0, the footage is yours,
the resulting motion is yours, and no dataset licence is involved anywhere
because no dataset is used.

What that route does NOT give you is what topic 8's brief asked about. It is not
a free mocap library. It is a capture pipeline, and topic 8's own labour
arithmetic is untouched: roughly 20 to 80 hours of skilled cleanup for twenty
movements, in a project with no animator.

**So topic 8's verdict is CONFIRMED and its reason is CORRECTED.** The verdict
was "bespoke motion capture is not worth doing for this project at this stage",
and that survives. The reason it gave, that "the licence position is much worse
than the phrase free mocap libraries suggests, and it eliminates most of the
option space", is right about libraries and wrong as a description of the whole
route. The licence wall is around DATASETS and around SMPL-based model weights.
It is not around the estimation software. The route is closed by labour, not by
licence, and those are different closures: labour is a budget question that a
different year answers, and a licence is not.

## 6. What changes

1. **Topic 8 section 2.3's table gains a row and a caveat.** The row: Apache-2.0
   estimators over your own footage, shippable. The caveat, from section 1: for
   any academic dataset, read the item's own rights text, because the label on
   the page and the terms in the sentence disagree at least sometimes.
2. **If anyone revisits this**, the question is no longer "which free library
   can we ship". It is "what does an Apache-2.0 estimator over our own footage
   cost per usable clip", and topic 8 section 3's eight-fault metric list
   (root trajectory, foot sliding, joint jitter, missed contacts, body
   orientation, hand behaviour, processing time, cleanup required) is already
   the gate for answering it.
3. **The footskate recommendation is untouched** and is still the only thing in
   topic 8 worth doing now. Nothing in this recheck bears on it.
4. **Nothing here reopens the verdict.** Confirming a no with a better reason is
   not an argument for yes.

## 7. What could not be established

1. **AMASS's actual licence text.** `amass.is.tue.mpg.de` refused, and the
   `nghorbani/amass` repository has no LICENSE or LICENSE.md at master (404 on
   both). Topic 8's AMASS quote remains a search summary.
2. **CMU's actual terms.** `mocap.cs.cmu.edu` refused. The claim that CMU "has
   been widely used commercially without issue" is still a statement about
   practice by a summariser, and topic 8's advice to read the terms before
   shipping a CMU-derived clip stands unchanged.
3. **SMPL, SMPL+H and DMPL licences.** All on refused Max Planck hosts, and all
   now known to be on the path for any SMPL-based estimator or dataset.
4. **Whether a model's output inherits its training data's licence.** Still a
   contested legal question, still outside my competence, still flagged rather
   than answered.
5. **Hosted video-to-motion services** (Rokoko, DeepMotion, Move.ai, Plask).
   Not surveyed, hosts not probed.
6. **What the estimators actually produce in quality terms.** This file read
   licences. It measured no take, opened no clip and ran nothing. Topic 8
   section 3's account of jitter, occlusion and foot sliding is unchanged and
   unverified.

## 8. Sources

Primary, read in full 2026-09-19.

Edinburgh DataShare, through its DSpace REST API:
- item `10283/2913`, "Orchestral conducting motion capture data", `dc.rights`
- item `10283/8851`, "Human MotionLess Dataset (HuMoLs)", `dc.rights`
- searches: motion capture (18 hits), mocap (1), human motion (17),
  locomotion (6), Komura (3, none relevant), Holden (4, none relevant),
  MOCAP Database (0), 100STYLE (26, none relevant), gait capture (1, not
  relevant), style locomotion (1, not relevant)

Through `raw.githubusercontent.com`, each project's own files:
- `ubisoft/ubisoft-laforge-animation-dataset` README.md
- `EricGuo5513/HumanML3D` README.md
- `google-ai-edge/mediapipe` LICENSE
- `open-mmlab/mmpose` LICENSE
- `CMU-Perceptual-Computing-Lab/openpose` LICENSE
- `GuyTevet/motion-diffusion-model` LICENSE and README.md
- `nghorbani/amass` LICENSE and LICENSE.md, both 404

Refused: `amass.is.tue.mpg.de`, `mocap.cs.cmu.edu`, `github.com`,
`huggingface.co`, `arxiv.org`.
