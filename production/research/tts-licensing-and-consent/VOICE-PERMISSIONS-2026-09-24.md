# The cast's voices: where each came from, and whether we may clone it

Checked 23 September 2026, against the TTS licensing research on main (`production/research/tts-licensing-and-consent/SUMMARY.md`, and its full version `DELIVERY.md` on the research branch). Nothing in the repository was changed.

**Summary.** There are **23 cast voices, not 19**. Nineteen were cast on 31 July: 13 named characters and 6 crowd voices. Four more were cast on 14 August: Aldous, Danny, June and Zlata. **All 23 come from the same place, the VCTK corpus**: about 110 volunteers recorded by the University of Edinburgh's speech research group (CSTR). For all 19 July voices that is proven: each clip is byte-for-byte the file a logged download from VCTK produced, and the speaker number matches. The four August clips have weaker records (see D below). **None is CLEAN today, all 23 are CONDITIONAL, and none is NOT CLEAN or UNKNOWN on where it came from.** The same three conditions apply to every voice (A, B and C below), and the four August voices have a fourth (D). The weak point is consent. VCTK's licence covers copyright and says in so many words that it does not cover the speakers' personal rights. No published document says the speakers agreed to have their voices cloned for a commercial game. The corpus's own title says it was built "for CSTR Voice Cloning Toolkit", so the project's belief that they agreed is reasonable. It is still not verified, and if it turns out to be wrong, all 23 fail together.

## What is true of every voice (the table refers to these)

- **Licence.** VCTK version 0.92 is Creative Commons Attribution 4.0 (CC BY 4.0). I read Edinburgh's licence file and README today; the research could not open that page, and it opens now. CC BY 4.0 allows commercial use and allows making new works from the recordings, and a cloned voice counts as one. It asks for one thing in return: credit.
- **Cloning allowed?** *Under copyright*, yes, as long as the credit is given. *Under personal rights*, the licence gives nothing. Its section 2(b)(1) says: "nor are publicity, privacy, and/or other similar personality rights" licensed. The research found the same gap: the licence "does not settle consent" (DELIVERY 2.1, HOLE; SUMMARY, "What I could not check").
- **Consent.** Nobody has published what the speakers signed. The README and the Edinburgh page say nothing about how speakers were recruited or what they agreed to. What we do have points the right way. The corpus is titled "English Multi-speaker Corpus for CSTR Voice Cloning Toolkit" and was designed for speech synthesis. The copy we downloaded (on Hugging Face) adds one condition: "You agree to not attempt to determine the identity of speakers". **Project-level ruling:** on 31 July Jafar answered "YES - proceed. The nineteen cast VCTK speakers may be cloned" (`legacy/studio-v2/game-design/decisions-pending.md:236`, commit 24b73cb7). That ruling is our own permission. It is not the speakers' consent, and it names the nineteen only.
- **Download runs (the evidence).** R1 is the CI run of 31 Jul 14:04Z (commit 3f1deb8a). Its log reads "vctk mirror CSTR-Edinburgh/vctk@parquet opened / source: vctk", and each clip below is byte-identical to that run's candidate file (`voice-candidates/<voice>/candidate-0N.mp3`), which the run's listening page labels with the same speaker number. Those clips were committed in 650c3aee. R2 is the CI run of 31 Jul 16:06Z (62f8f27b): same copy, same check, clips committed in 604618d3. R3 is the fetch run on Jafar's PC on 13 Aug ("The VCTK fetch landed", e5304ba1); its log is not in the repository.

## Voice by voice

| # | Voice | Used by | Source (speaker) | Licence | Cloning allowed? | Consent | Verdict | Evidence |
|---|---|---|---|---|---|---|---|---|
| 1 | lena | Lena, the bar's bookkeeper (principal) | VCTK p228 | CC BY 4.0 | Copyright yes with credit; personal rights not covered | Not documented; inferred; Jafar's 31 Jul ruling | CONDITIONAL (A, B, C) | `game-design/picked-clips/lena.p228.mp3`; R1 candidate 2 |
| 2 | rocco | Rocco, on the door (principal) | VCTK p227 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `rocco.p227.mp3`; R1 candidate 1 |
| 3 | ellis | Detective Mara Ellis (principal) | VCTK p231 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `ellis.p231.mp3`; R1 candidate 4 |
| 4 | reese | Tobias Reese, Board of Excise (principal) | VCTK p256 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `reese.p256.mp3`; R1 candidate 4 |
| 5 | kest | Sera Kest, the rival head (principal; the game's id `sera` points here) | VCTK p244 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `kest.p244.mp3`; R1 candidate 1 |
| 6 | sam | Sam (street) | VCTK p241 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `sam.p241.mp3`; R1 candidate 1 |
| 7 | ada | Ada (street) | VCTK p276 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `ada.p276.mp3`; R1 candidate 2 |
| 8 | vesna | Vesna (street) | VCTK p238 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `vesna.p238.mp3`; R1 candidate 1 |
| 9 | marla | Marla (street) | VCTK p282 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `marla.p282.mp3`; R1 candidate 1 |
| 10 | joey | Joey (street) | VCTK p263 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `joey.p263.mp3`; R1 candidate 2 |
| 11 | rita | Rita (street) | VCTK p249 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `rita.p249.mp3`; R1 candidate 3 |
| 12 | hal | Hal (street; the tier-1 card's id `halvard` points here) | VCTK p273 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `hal.p273.mp3`; R1 candidate 4 |
| 13 | emil | Father Emil (street) | VCTK p245 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `emil.p245.mp3`; R1 candidate 1 |
| 14 | crowd_m1 | Male crowd pool: every uncast man; 335 pre-rendered barks in the build | VCTK p287 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `crowd_m1.p287.mp3`; R1 candidate 2 |
| 15 | crowd_m2 | Male crowd pool; 335 barks | VCTK p272 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `crowd_m2.p272.mp3`; R1 candidate 1 |
| 16 | crowd_m3 | Male crowd pool; 335 barks | VCTK p292 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `crowd_m3.p292.mp3`; R2 candidate 4 |
| 17 | crowd_f1 | Female crowd pool: every uncast woman; 335 barks | VCTK p266 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `crowd_f1.p266.mp3`; R2 candidate 1 |
| 18 | crowd_f2 | Female crowd pool; 335 barks | VCTK p265 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `crowd_f2.p265.mp3`; R1 candidate 1 |
| 19 | crowd_f3 | Female crowd pool; 335 barks | VCTK p288 | CC BY 4.0 | as row 1 | as row 1 | CONDITIONAL (A, B, C) | `crowd_f3.p288.mp3`; R2 candidate 3 |
| 20 | aldous | Aldous Vane (principal) | VCTK p226, weaker record | CC BY 4.0 | as row 1 | Not documented; **outside the wording** of the 31 Jul ruling | CONDITIONAL (A, B, C, D) | `aldous.p226.wav`; R3; commit 681149c2 |
| 21 | danny | Danny Ro (principal) | VCTK p254, weaker record | CC BY 4.0 | as row 1 | as row 20 | CONDITIONAL (A, B, C, D) | `danny.p254.wav`; R3; commit 681149c2 |
| 22 | june | June (principal) | VCTK p225, weaker record | CC BY 4.0 | as row 1 | as row 20 | CONDITIONAL (A, B, C, D) | `june.p225.wav`; R3; commit ed051fde (she was first offered Lena's p228; that was caught and replaced) |
| 23 | zlata | Zlata (street) | VCTK p233, weaker record | CC BY 4.0 | as row 1 | as row 20 | CONDITIONAL (A, B, C, D) | `zlata.p233.wav`; R3; commit 681149c2 |

Clips 2 to 23 are in the same folder as row 1. Each one also has a conditioning file derived from it (`game-design/voice-conds/<voice>.bin`/`.npz`). The build ships those files, and they carry the same obligations as the clip.

## What would make them clean

- **A. Ship a correct credit (every voice).** A credit already exists in `THIRD-PARTY.md` and has been there since 31 July (commit 9c3f3551). It never reaches a player: neither the Unity game nor the Unreal probe has a credits screen. It also has faults. It spells the group "CVSTR". It lists only the 19 July speakers, and says "all 19 cast voices". It leaves out what CC BY 4.0 section 3(a) asks for: the creators' names (Yamagishi, Veaux, MacDonald), a link to the licence, the source's link or DOI (10.7488/ds/2645), and a note that the recordings were modified. Fix: correct that text and put it in the shipped credits.
- **B. Settle consent (every voice).** Nobody can read the speakers' consent from here, because it is not published. The cheapest way to settle it is to write to CSTR at Edinburgh and ask whether the VCTK consent covers use of a speaker's voice as a cloned character voice in a commercial game. That message is Jafar's to send. The alternative is for Jafar to accept the inference explicitly, and on the record, as a risk. Until one of those happens, "we have consent" is a belief the evidence supports, not a fact.
- **C. Make the allowlist agree with itself (every voice).** `ledger-v2/research/license-allowlist.md` puts "cloned real voices" on its NEVER SHIP list (entry 5). Read literally, that bans all 23 voices, because every one is a real volunteer's voice. Its SHIP-SAFE entry 1 allows "the local voice pipeline as built". The allowlist is law, and its two entries contradict each other. That makes it canon for Jafar to rule on. Recommended: entry 5 means *identifiable* real people and celebrities, and the ruling should say so in writing.
- **D. Close the paperwork on Aldous, Danny, June and Zlata.** Their source rests on three things: the speaker numbers in their filenames, the pick record (`game-design/voice-picks.json`, where age and accent are empty), and one commit message. The download log stayed on Jafar's PC. There is some support: the same four numbers appear as VCTK speakers on the logged July CI pages (p225 was Lena's candidate 4, p226 Rocco's 3, p233 Ellis's 3, p254 Reese's 1). They are missing from the credit's speaker list, from `voice-casting.md`, and from the conditioning manifest, which names 19 sources. Jafar's cloning ruling says "the nineteen". Fix: add the four to those three records, and ask Jafar for one line extending the 31 July ruling to them.

## Also found (these change what comes next)

- **The research on main is wrong in two places.** It says no attribution file mentions VCTK. That is true of the six asset attribution files, but `THIRD-PARTY.md` names VCTK and has done since 31 July. The real gap is that the credit is incomplete and never ships. It also gets 19 by adding "17 cast voices plus 2 aliases". That total is a coincidence: the two aliases are extra names for Hal and Sera Kest, and the real count is 17 named voices plus 6 crowd voices, 23 in all. The ruling in DECISIONS.md inherited the "nineteen".
- **Voices have already been recorded with.** The six crowd voices each have 335 generated barks in the build, 2,010 lines in total. None of them carries the watermark D50 says to keep, because every voice path still has it stubbed out. That is not a question about any one voice, but it applies to everything recorded from now on.
- **Never try to identify the speakers.** The Hugging Face copy's terms forbid it. Credits may list speaker numbers, but not names or guesses.

## Jafar's rulings, 24 September morning

- Consent: VCTK's consent is taken to cover cloned game characters, accepted on the record as a stated risk. No email to Edinburgh.
- The allowlist: "cloned real voices" means identifiable real people and public figures, not anonymous research volunteers. Written into ledger-v2/research/license-allowlist.md.
- Aldous, Danny, June and Zlata: allowed (VCTK), never approved. Not re-cast from the nineteen, because shared voices would repeat. A listening page of each beside two or three alternative VCTK speakers of a suitable age and accent goes to him to pick, once the card is free.
- From now on no voice is cast without his yes (CLAUDE.md).
