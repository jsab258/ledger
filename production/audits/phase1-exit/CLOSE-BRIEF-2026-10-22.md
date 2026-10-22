# Closing phase 1: what each fresh reviewer is given (22 October 2026)

His order of 21 October, item 9: "Close phase 1: a fresh reviewer per exit, then NOW.md set to phase 2 from PLAN.md, and one line on his page asking whether phase 2 starts."

PLAN.md: "A fresh model gets the requirements and outputs, never the maker's verdict, and verifies the exit." Each reviewer reads the requirement and the outputs named for one exit and reaches its own verdict from the raw numbers, pictures and logs. The research files hold the maker's reading of their own numbers: check the numbers and do not take the reading on trust. BUNDLE.md's "State" column is the maker's and is not evidence.

## The phase's exit (PLAN.md, phase 1)

> **Exit:** the samples meet the bar; the render and voice pairing has measured headroom; median first meaningful speech two seconds or less (no prepared openings, his 7 October ruling; else the stop rule).
> **Binding stop:** a sample that cannot pass within this ceiling halts expansion; the failed capability is reported plainly, never dressed as another plan.

The bar for anything seen: CLAUDE.md, "The gate". This means:
- checked against references (photographs, the approved face, the casting sheet, accent by ear);
- then the Hook sheet (production/previews/hook-sheet-2026-10-05.jpg);
- clothes judged on their own floor (RULINGS.md, 3 October: plain, period-plausible, no modern giveaways, no clipping or holes, nobody frozen stiff);
- "Done means in the packaged release build, walked by the AI tester".

## Exit A: Mickey's front office, a frontage, three street views (PLAN.md phase 1, first proof)

**Requirement.** "the room Tom walks into, from the room kit, researched first; real glass reflecting the street; a 1990 cab office's wear and clutter, radio set, ashtrays, kettle, telephone, scuffed counter; no glitches. With it one frontage of correct geometry, material and wear, its window of verified CC0 goods, and three fixed street views."

**Outputs.**
- The office's gates:
  - production/audits/phase1-exit/GATE-1.1-REVIEW-1.md, -2.md and -3.md, with their briefs;
  - production/audits/office-2026-10-08/GATE-OFFICE.md;
  - production/audits/glass-2026-10-08/, night-2026-10-08/, road-2026-10-08/, sky-2026-10-08/.
- The office's recipe and props:
  - tools/art-recipes/shop-room.py (mickeys);
  - production/specs/mickeys-office.json;
  - production/art/mickeys-props/README.md;
  - research in production/research/shop-window-interiors/ and production/research/cab-office-interior-1990/.
- The frontage:
  - Rita's front: production/audits/gate-ritas-front/GATE.md;
  - its page: production/approvals/2026-10-22-ritas/page.json and CHECK.md;
  - his answer on it: production/approvals/answers/2yznAYjEwDVv3RvzzKUpBR/verdicts/look-ritas-front-2026-10-22.json;
  - the goods' sources: production/art/shop-rooms/pawnbroker-goods-sources.md;
  - its wear: production/specs/street-wear.json.
- The three fixed views: production/previews/morning-hook-day-2026-10-22.jpg, morning-reverse-day-2026-10-22.jpg and morning-night-2026-10-22.jpg, beside the Hook sheet (made each morning by tools/morning_pictures.py; corrected after Exit A's review: from the editor in its game mode, not the packaged build).
- The AI tester's walk of the packaged game: production/playtest/nightly/2026-10-22.md and .json.
- Open faults: FINDINGS.md.

## Exit B: one complete Tom and one speaker, walking, sitting and turning

**Requirement.** "One complete Tom and one speaker walking, sitting and turning." His checkpoint: "one whole-frame and moving-character review; frozen identities preserved" (RULINGS.md, 30 September and 8 October: the frozen faces, Tom L1).

**Outputs.**
- Casting: production/casting/CASTING.md.
- The frozen faces: RULINGS.md, line beginning "30 Sep: Faces are frozen".
- Tom's face route: DECISIONS.md, 6 and 7 October, "TOM'S FACE".
- The playable Tom: ue-probe/Source/LedgerProbe/Public/SliceCharacter.h, opening comment, and MeshPath and ClipPath in SliceCharacter.cpp. The MetaHuman builds are in ue-probe/Content/Ledger/MetaHumans (MH_TomL1 and others).
- Walking:
  - production/research/sit-and-turn/METHOD-2026-10-06.md;
  - WALK-JOINS-2026-10-08.md;
  - TOM-MOTION-MATCHING-2026-10-22.md, with tom-walk-2026-10-22/ (the measured route for his walk and for the motion-matched one).
- Sitting and turning:
  - production/research/sit-and-turn/LOCOMOTION-2026-10-06.md and RETARGET-FAULT-2026-10-07.md;
  - DECISIONS.md, 7 October, "SITTING WORKS".
- Clothes:
  - RULINGS.md, 3, 8 and 13 October;
  - FINDINGS.md (clothes);
  - DECISIONS.md, 22 October 10:35 (Epic's garments).
- The AI tester's walk: production/playtest/nightly/2026-10-22.md and .json.
- Open faults: FINDINGS.md.

## Exit C: P2, the voice, and the speech line

**Requirement.**
- "P2, the voice: two measured approaches at most (shared graphics card; CPU or quantised), timed beside checked talk."
- The exit: "median first meaningful speech two seconds or less (no prepared openings, his 7 October ruling; else the stop rule)."
- RULINGS.md on speech: the 7 October lines.

**Outputs.**
- production/research/voice-off-card/NOTE.md, RESULTS-2026-10-06.md and CLOUD-VOICE-2026-10-07.md.
- production/research/voice-latency/: EVIDENCE-2026-10-01.md, FAST-FIRST-AUDIO-2026-10-01.md, STREAMING-IN-GAME-2026-10-01.md, POCKET-CPU-2026-10-21.md and GEMINI-CHECK-2026-10-22.md, with gemini-2026-10-22/.
- production/playtest/talk-runs.jsonl.
- production/research/pre-production/p1-packaged/runs.jsonl (the frame cost of each voice).
- FINDINGS.md: the line beginning "A spoken answer starts a median".

## Exit D: P1 packaged and the render and voice pairing's headroom

**Requirement.**
- "P1 completed packaged: day, night, walking, Windows memory, sustained speech."
- The exit: "the render and voice pairing has measured headroom."
- PLAN.md's performance exit: "Median frame at most 16.7 ms, p99 25 ms, dedicated memory 6 GB with the voice on the card".
- His order of 21 October, item 6: "the packaged build's worst frame at or under 33.3 ms on the walk, measured".

**Outputs.**
- production/research/pre-production/P1-PACKAGED-2026-10-07.md and P1-PACKAGED-2026-10-21.md (its last section is 21 October's fresh review).
- production/research/pre-production/p1-packaged/runs.jsonl: every capture, including the 22 October runs labelled pocket-below, pocket-below-4t and card-today.
- The raw frames: F:/LedgerTools/latency/p1-2026-10-21/ and F:/LedgerTools/tmp/p1-packaged/ (CSV; tools/perf-hook.py reads them).
- production/research/voice-latency/POCKET-CPU-2026-10-21.md, its 22 October section.
- FINDINGS.md: the line beginning "Frame spikes on the render-submission".
