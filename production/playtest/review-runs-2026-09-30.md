# The review's three runs of the finished game, 30 September

The independent review (production/audits/review-2026-09-30/FAULTS.md, "What still needs the game itself") asked for three short runs of the packaged game to settle what it could only read. They were played by the AI tester on the build machine's package of c6a47f331 (the played copy, F:\LedgerTools\played-game, 20:05), stand-in talk, before any of the fixes. The pictures are in production/playtest/ai-tester/2026-09-30-2022 and 2026-09-30-2034.

## 1. One smash, the witnesses' memories read afterwards (A1, A2, A3, A4): all confirmed

- The deed at D0 16:37, session key `player.window_d0`. The log: "2 saw it", both at rung 0 (`witness_lena=0`, `witness_sam=0` in the save).
- **A1, worse than read.** Both filed the game's internal words as a memory: Sheila "I think I saw it, couldn't swear to it: bank-unreadable/none"; Darren the same with "bank-unreadable/no-line-at-witness_summary-rung-0". By 17:00 gossip had carried Darren's to Ron, Danica and Fabjan ("I heard from Darren that bank-unreadable/..."), and Ron's talk was handed it as the story he knows about the new owner. Sheila still shouted "Stop. I mean it. Stop." though she saw nothing.
- **A2.** Only the two stand-ins were read. Rita's day had her behind her own counter at 16:37, a metre from the glass; she was no witness and "found the damage" at 17:00 with Ines, Victor, Tibor and Joey. At 20:00 and 02:00 Sheila and Darren still stood in the street, though both their days end at 18:00.
- **A3.** Ron's talk carried no deed at all: the save filed `player.window_d0`, the talk looked for `player.window_d1`.
- **A4.** No reading above rung 0, so no statement and no report was possible.

## 2. One Continue (C1): confirmed, with a second cause the review did not see

- After Continue the game logged "the save's talk loaded", and Ron's talk said he had never met the player.
- **The talk was never saved at all.** The talk program writes and reads only a file whose name ends ".talk.json" (its guard against writing over anything else); the game asked for "talk.json", which it refuses with `path-must-end-.talk.json`. Shown directly with the game's own talk program: "talk.json" refused, "game.talk.json" saved. No save of this build ever kept a conversation, and the refusal was never shown or logged.

## 3. Sunday played past noon, then Sheila at the office (B1): confirmed

- The waits stopped at D6 10:00 for her; the next wait ran to 18:07 without seeing her, and on to D7. At D7 05:00, 5.1 m from Mickey's office, he talked to her: no question was put (no "Sheila puts her question" in the log).
- DS Ellis had been on the street asking after the player during the week (Sheila's talk knew "that detective, Ellis, was on Quay Street asking after Mickey's nephew").

## Also seen

- The visual slice's stand-in silhouette (Mixamo's "Michelle", a stylised modern figure with headphones, 16 September) stands by the fish market every night in free play: the night light spawns it. Barred from play in the same change as the fixes; the frames for Jafar's page keep it.
- The pavement at Rita's traps the player between the telephone box, the crates and the parked cars; the tester got out only backwards. The two parked cars at Rita's leave no way through to her window from the road.

## The same three runs after the fixes (30 September, 23:08, to 1 October, 00:25)

Played by the AI tester in the build machine's packages of ccf9b7740 (the review's High faults and the town's half), 90ca1e36a (the wait, saves, walls, witness lines) and e7a80159d (the town's second check), stand-in talk. Pictures: production/playtest/ai-tester/2026-09-30-2308, 2026-09-30-2354 and 2026-10-01-0018.

1. **The smash.** At D0 11:39 the onlookers were the people really there: Darren on Rita's step (his day), Rita and her staff behind her counter, the fish counter, the pension counter, Sheila and Ron at Mickey's. Darren, who had met him, recognised him at 1.5 m (rung 4) and alone filed "the new owner was at Rita's on Monday"; everyone else filed what they had: the damage heard, or a shape. No memory anywhere holds "bank-unreadable"; the talk saved beside the save ("people":1); the save holds the meetings (met_lena, met_sam).
2. **Continue.** He came back where he stood, and the talk program loaded the saved conversation ("loaded, people 1"). The Z wait now goes hour by hour: it stopped at 20:00 for Ron's envelope and at 22:00 for the landing, then ran on to morning.
3. **Sunday past noon.** The waits stopped at D6 10:00 for Sheila's appointment; he waited on past noon without seeing her, and on Monday at 10:45 at the office she put her question (the log: "Sheila puts her question at D7 10:45").

Known, not faults of the route: the build machine's packages all stamp their commit as SHA-UNKNOWN, so a save from an older package is not refused as "another build's" (harmless for play); the review's C5 small save items remain (see its list).
