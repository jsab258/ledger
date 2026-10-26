# Darren's voice recast in Pocket: the candidates and the gate, 26 October 2026

His answer of 26 October, 3: "Darren: recast his voice. Make three young local English candidates in Pocket that fit his casting sheet, and put them on my page; his face and the rest of his sheet stay. This reopens my voice rulings for Darren only." Pocket made from Darren's old voice (VCTK p241, Scottish) drifted American on every line (the listening test that morning), so new references were needed.

## Where the voices come from

- VCTK (CSTR Edinburgh, CC BY 4.0; already on the licence allowlist: Ron's voice and Darren's old one came from it). His yes of 26 October to a download of five speakers only: the speaker list and sixteen recordings each were read out of VCTK-Corpus-0.92.zip by byte ranges, 20 MB fetched of the 10.9 GB file (F:/LedgerTools/vctk-young-men, the script beside them as HOW-FETCHED.py).
- The five: every young English man in VCTK from the north or the Midlands not already another character's voice: p270 (Yorkshire, 21), p259 (Nottingham, 23), p278 (Cheshire, 22), p279 (Leicester, 23), p286 (Newcastle, 23). (p287, York, is a crowd voice; p256, Birmingham, is Reese's.)
- Each speaker's reference: about 20 s of his own recordings joined (the first prompt skipped), evened to -20 dB (F:/LedgerTools/vctk-young-men/refs).

## The gate (tools/voice-live/take_gate.py: accent over the take and in 2.5 s windows, Whisper's words, likeness to the reference)

| Speaker | His three sheet lines, first takes | Retakes of a failed line | Twelve in-game lines | Likeness |
|---|---|---|---|---|
| p259 Nottingham | 3 of 3 | none needed | 12 of 12 | 0.76 to 0.83 |
| p270 Yorkshire | 2 of 3 (line 1 read Australian) | line 1: 3 of 9 | 12 of 12 | 0.52 to 0.66 |
| p286 Newcastle | 2 of 3 (line 1 American) | line 1: 2 of 4; line 3: 4 of 5 with every word | 12 of 12 | 0.65 to 0.80 |
| p279 Leicester | 2 of 3 (line 3 American) | line 3: 5 of 6; line 1: 2 of 2 | 12 of 12 | 0.45 to 0.70 |
| p278 Cheshire | 2 of 3 | line 1: 0 of 4 | not run | 0.45 to 0.68 |

Cheshire was dropped (his first line never passed). The in-game lines are the dialogue bank's lines for the lad in the yard plus five of his own (F:/LedgerTools/approvals/darren-recast-2026-10-26/drift).

## The fresh reviewer (measuring what it cannot hear)

- **First round:** A (Yorkshire) FAIL: on the joined take an American-reading stretch of 3.5 s ran across "You will, give it a week" into the join (each line alone had passed); B (Nottingham) PASS; C (Newcastle) FAIL: the "I" of "I saw a bit" missing (the word check's 0.11 passed it, the sheet's line was not whole). Also found: the word check scored "Mates' rates" wrong on every take (a trailing apostrophe; fixed in take_gate.py's norm), and that this classifier reads 4.5 s of Yorkshire's own genuine recording as American, so for p270 it cannot tell drift from his vowels.
- **Fixed:** A rebuilt with another clean first line (its joined take: American run 3.0 s, at the rule's limit, not over); C rebuilt with a third line whose "I" is heard; all three re-levelled to one loudness with lower peaks.
- **Second round:** B and C PASS (C's "I" heard, a 90 ms voiced vowel before the /s/; loudness spread 1.6 dB). A FAIL again: other-accent stretches of 4.0 s in its new first line and 3.5 s in its third, and its American run at 3.0 s fails on three of five shifted window grids. **The Yorkshire voice is set aside after two rounds**; the classifier reads his own recording the same way, so only a ruling to hear it by ear despite the measure could bring it back.
- **A replaced by the reserve, p279 (Leicester):** its original second line had lost "Mates" ("rates, rates"); a retake with every word was used. Its joined take passes the gate (American run 2.5 s, every word, likeness 0.67). All three re-levelled to -21 LUFS.
- **Third round (the Leicester voice's first try):** FAIL on the rule set for all three, no other-accent stretch over 3 s (4.0 s in line 3 and 3.5 s at the end of line 1, over 3 s on every grid); the genuine p279 recording reads cleanly, so this was the generated voice. Its own second line had lost "Mates" ("rates, rates") and was retaken. B and C unchanged and passing.
- **Fourth round (its second try):** new first and third lines chosen with the reviewer's own measure (the longest other-accent run over five shifted window grids, matching its numbers on all three takes): every other check passed, but the "I" of "I saw a bit" was not spoken (25 ms unvoiced, against B's and C's 90 ms vowel). **The Leicester voice is set aside after two tries.**
- **On his page:** the two that passed every round, heard blind as A and B (now the Newcastle and Nottingham voices; key.json). The third he asked for was not reached; the page says so first. Next, if he picks "neither": another source of young English men's voices, researched first.

## On his page

Blind, as A and B, the letters drawn at random; the key is kept off the page (F:/LedgerTools/approvals/darren-recast-2026-10-26/key.json). Page: https://claude.ai/artifact/8LsucbjBtuCj1QyaRamqpB (afternoon, 26 October).
