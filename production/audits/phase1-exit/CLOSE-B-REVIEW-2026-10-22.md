# Phase 1's close, Exit B (one complete Tom and one speaker, walking, sitting and turning): the fresh review, 22 October 2026

A fresh reviewer (Opus) was given CLOSE-BRIEF-2026-10-22.md and the outputs, not the maker's verdict, and worked read-only. Its report, verbatim in substance:

## Clause verdicts

- **Tom complete (his L1 face and body as the player sees him): NOT MET.**
  - SliceCharacter.cpp line 42 loads SK_tom-player, the Mixamo stand-in of 23 September, which SliceCharacter.h lines 5 to 7 call "a stand-in until Tom's look is settled".
  - No source file references MH_TomL1.
  - L1's own reviewer said no to 2026-grade (production/casting/tom-nowak/CLOSEST-2026-10-08.md, section 3).
- **Tom walking: NOT MET.** tom-walk-clips.txt reads `ledgerTomWalk=FAIL`: worst join 43.4 cm against 3 cm, starts' median 26.9 cm.
- **Tom sitting: NOT MET.** Nothing is built; DECISIONS.md line 367 says "Not yet: … Tom sitting".
- **Tom turning: NOT MET.** 8 of 18 turn contacts slide 18 to 43 cm. There is no turn clip; the capsule rotates at 540° a second.
- **One speaker complete: NOT MET.** Sheila is MH_LenaS4, but:
  - FINDINGS.md says her face fails its sheet;
  - her glasses and chain are held back (packaged log);
  - she wears the white base layer.
- **The speaker walking: NOT MET.** Sheila's -WalkProof (editor) failed: first step 13 to 20 cm, stop 18 to 27 cm (DECISIONS.md line 377). It was set aside after six tries (WALK-JOINS-2026-10-08.md).
- **The speaker sitting: NOT MET in the game.**
  - Ron's editor SitProof passed at 0.5 cm.
  - But the seat exists only under -MickeysInside, which a plain packaged launch does not set (LedgerProbe.cpp:832; CrimeProbe.cpp:4226 and 7027).
  - In the packaged walk of 22 October, Ron is at Mickey's office from 20:00 to 22:00 with no LedgerSeat line, so he never sat.
- **The speaker turning: NOT SHOWN at the bar.** The editor TurnProof passed at 99.6 and 99.4 of 100°, and the packaged log shows the turn running. But there is no packaged picture, foot measure or tester judgement of it.
- **Clothes on their floor: NOT MET.**
  - The white base layer stays, reported failed (FINDINGS.md; RULINGS.md, 8 October).
  - Epic's Techwear is a yellow technical jacket with yellow trainers (fab-garments.jpg, confirmed).
  - The previews show Sheila barefoot in a white slip and Ron in a white T-shirt and briefs.
- **Frozen identities preserved: MET for Ron P2, Sheila S4 and Darren S6** (packaged log of 22 October). **NOT MET for Tom L1**, who is absent from the game.

## Faults the maker's files do not name

- **Nobody sits in the game as played.** Mickey's office interior and Ron's seat appear only with -MickeysInside. Neither the plain launch, tools/play/PLAY THE ENCOUNTER.bat nor the friends' shortcut passes it. This touches Exit A too.
- **TOM-MOTION-MATCHING-2026-10-22.md's table understated Tom's own clips.**
  - The worst stop is 30.8 cm by the run's own header, not 23.2.
  - The loop's 3.4 cm median hid his right foot sliding 27 to 36 cm on every steady stride (15 of 40 loop contacts over 7 cm).
  - (Checked and corrected by the maker the same day.)
- **No single speaker walks, sits and turns.** Walking and turning are Sheila's; sitting is Ron's.
- **Every walk, sit and turn proof ran in the editor, none in the packaged build.**
- **The AI tester has been blind since 8 October.**
  - On 21 and 22 October its picture check failed with "OAuth session expired".
  - Its 8 October finding ("Tom stands splay-legged with stiff arms … a broken default idle") is in no FINDINGS line and has no recorded fix.
  - Its route never exercises sitting, turning or a speaker walking. On 22 October it failed the Ron and Darren stages.
- **Ron's sit and stand still look folded over.** In sit-stand-office-2026-10-08.jpg, frames 2 and 6, he is folded nearly double with his head at counter height.
- **The morning pictures are filmed in the editor's game mode, not the packaged build** (tools/morning_pictures.py, lines 43 and 96).
- **Tom L1's freeze has no approval file beside it;** only RULINGS.md line 60 records it.
- **Other garments are held back in the packaged game:** Darren's belt and pager, and Ron's jacket.

## Not reached

- The tester's 22 October pictures (none on F:/LedgerTools/nightly/2026-10-22) and the 8 October step pictures.
- The scratch measure files on F: (walk_phase, walk_join, sit_join, turnprofile2, sitprofile2, walk_idle).
- The MH_TomL1 asset itself.
- Where the 22 October Tom walk measure ran (the file does not say). It was the editor's game mode, -game, on the local build.

## Verdict

Exit B does not pass phase 1's bar.
