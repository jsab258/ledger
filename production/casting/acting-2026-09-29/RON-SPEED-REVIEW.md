# Ron, faster: the blind pair's gate, 29 September 2026

A and B: the same three lines ("I don't know anything about that, and I'd rather keep it that way." / "Right. I'll bring the car round at half nine, then." / "Who told you that? Was it Darren? It was, wasn't it."), one through Sopro V2 Turbo (the fast free engine, first sound about 2 s in play) and one through the game's engine (his approved voice, 3.5 s steady in play, 6.8 s while the game settles). Which is which: ../acting-key-2026-09-30-ron-speed.json, never on the page. Levelled to -21.4 LUFS each.

My check (take_gate.py per line): the fast engine held his accent on 15 of 16 test lines; the game's engine on 12 of 12, with word slips on 4.

A fresh reviewer, measuring what it could not hear (F:/LedgerTools/tmp/review-ron-speed):
- Both word-perfect; no artefacts; neither clips.
- A: closer to his reference (likeness 0.86, pitch 122 Hz as the reference's, range 105 to 139 Hz, 3.8 syllables a second, a creak on "Right" that suits him); a 4.0 s stretch across the join "that way. / Right. I'll bring the car" reads American in 2.5 s windows though every line on its own reads English, and the windows swing between 0.01 and 0.98 when moved by a quarter second: FAIL, borderline, "should get a human listen".
- B: England throughout (likeness 0.73); livelier than the reference, rising about 7 semitones on "Who told you that?" (range 108 to 189 Hz): PASS.
- Same man by the measures (A against B 0.71).

The borderline point is the classifier's to doubt and his ear's to settle, so the pair goes on his page with these notes (CLAUDE.md, the gate: narrow points go beside the item).
