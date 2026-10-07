# A streaming cloud voice: the numbers (7 October 2026)

For his 7 October speech ruling; nothing signed up for, bought or keyed. **O** opened and read 7 October (also repository records, today's network timing); **S** search summary; **I** inference. Replaces the 28 September pick.

## One screen

| | |
|---|---|
| Provider, plan | ElevenLabs Flash v2.5, Starter |
| Billing | Subscription: $6 a month, credit inside, then per character [2] |
| Account he would create | ElevenLabs, his name, a card; its key never shipped |
| First word, part 1 in place | measured 7 October (below): about 2.4 s, set by the first sentence's check; 3.0 s without the faster first sentence |
| Writing and voice, per hour | measured: $0.57 at the pace played so far; $2.30 heavy talk; plus the $6 |

1. **Time (I from O).** Faster model's first sentence 0.81 s (Haiku 4.5, 1 October bench) + round trip 0.015 s (measured today) + Flash's first audio 0.18–0.20 s (Coval, its network included) [9][10] ≈ 1.0 s. But it is spoken only once checked, a median 1.27–1.34 s later in the played game (3–5 October). The voice works meanwhile, so the check sets the floor, ≈ 2.1 s; under two seconds needs it 0.1–0.2 s quicker. The voice's own share falls from 3.66 s to about 0.2 s.
2. **Cost (I from O).** Typical: 15 replies × ($0.0252 writing + $0.0036 faster-model call) = $0.43, plus 975 characters × $40/M = $0.04. Heavy: 60 × ($0.031 + $0.0036) = $2.07, plus 11,460 × $40/M = $0.46. Writing is 82–92%. Starter's $6 buys about 150,000 characters (I).
3. **Quality.** Most replies are one sentence (7 of 8 on 4 October, 12 of 24 on 30 September): the faster model would often write all of it. Blind check here (1 October), Sheila's twenty answers: her model preferred 13 times, the faster 6; mean 3.45 against 3.25. Speculative decoding is lossless only because the big model checks every word [L1]; small-then-big writing lost "minimal" quality [L2]; a fast 3–7-word opening, the strong model continuing, kept 99% of quality behind a learned gate, without it 8.6–11.5% rated poor [L3]. Expect a modest loss of character in one-line replies (I).
4. **To measure:** blind pairs per character, split against Sonnet alone; how often the faster sentence fails the check (4 of 23 of Sonnet's did, 5–7 s each); contradictions; first sound on the real path; accents by his ear.
5. **Licence and identity.** Already on the allowlist (paid tiers); a decision record is owed. Stock voices replace the cast's, reopening "voices as chosen" (3 October): his page. Cloning the VCTK voices needs speaker consent they lack. The OEM terms bar Starter to Pro from "Making Available" the service [5]; a sold game may need Scale, $299 a month (I).

**Runner-up:** Inworld TTS-2 Flash, pay per use: fastest, cheapest ($0.45 and $2.25 an hour), commercial without a fee; off the allowlist, six generic British voices [11]. Its speed hides behind the check; allowlist and voices decide.

## The comparison

| Service | First audio, Coval median [9][10] | Billing, $/M characters | Stock voices commercially; British ones |
|---|---|---|---|
| ElevenLabs Flash v2.5 | 182–202 ms | Starter $6 a month, 40 [2] | paid plans [3]; library, accent filter [4] |
| Inworld TTS-2 Flash | 72–75 ms | per use, 15 [7] | yes, disclaimer [8]; six [11] |
| Cartesia Sonic 3.6 | 437–440 ms | Pro $5 a month, 50 [13][14] | Pro up [15], clone consent [16]; several [17] |
| Deepgram Aura-2 | 290 ms | per use, 30 [19] | yes, never as human [20]; two [21] |
| OpenAI gpt-4o-mini-tts | unpublished | per use, ~15 (S) [22][23] | yes, disclosed [22]; by instruction |
| Azure neural | unread | per use, 15; HD 22 [24][25] | yes, disclosed [26]; 14 plus HD, one a child's [27] |
| Google Chirp 3 HD | 438 ms | per use, 30 [29] | terms unread; 28 [28] |

All but ElevenLabs need a licence entry. Round trip from here: 12–17 ms.

## Play numbers (O, repository)

- **Replies an hour:** the AI tester's thirty minutes (3 October), 15 in two runs; part b, 8 in 41 minutes. Heavy: one a minute (I).
- **Characters a reply:** mean 61 (4 October), 67 (30 September), 191 (23 paid played-game replies).
- **Writing a reply:** $0.0252 (4 October); $0.031 (24 paid ones). Anthropic's API on his key: Sonnet 5 ($2/$10 a million tokens [30]) for conversation, Haiku 4.5 ($1/$5) for small talk and checks. Extra call: 3,526 input tokens × $1/M ≈ $0.0036.

## Sources (7 October 2026 unless dated; O but [23])

ElevenLabs: [2] API pricing; [3] terms (31 Mar 2026); [4] voice library; [5] OEM terms (28 Feb 2025). Inworld: [7] pricing; [8] terms (14 May 2026). [9] Coval TTFA blog. [10] gradium.ai, Coval of 8 Sep. [11] famulor.io. Cartesia: [13][14] pricing; [15] terms (14 Jun 2024); [16] acceptable use (23 Jul 2025); [17] models. Deepgram: [19] pricing; [20] terms (6 Aug 2026); [21] models. OpenAI: [22] guide, pricing; [23] community forum. Azure: [24] pricing; [25] price API; [26] code of conduct (1 May 2026); [27] voices (10 Sep 2026). Google: [28] Chirp 3 HD (30 Sep 2026); [29] pricing. [30] claude.com. arXiv: [L1] 2211.17192; [L2] 2302.07863; [L3] 2603.23346.

Unreached: Coval's live board, Google's terms.

## Part 1 measured on the real path (7 October, 10:27 and 10:32)

The played copy (a32eeeb) with the repository's talk program, the AI tester typing to Sheila, LEDGER's capped key, today's free voice on the card. Five checked replies each way (one line of six was not taken in each). From the game's own timing lines and the talk program's steps; production/playtest/talk-runs.jsonl.

| | one model | the faster first sentence |
|---|---|---|
| first sentence written (median) | 1.35 s | 0.75 s |
| its check passed (median) | 2.96 s | 2.41 s |
| first sound: each reply | 3.59, 4.55, 4.63, 4.75, 5.72 | 2.63, 2.90, 3.99, 4.75, 7.78 (a second draft) |
| first sound (median) | 4.63 s | 3.99 s |
| the voice making the first piece | 2.20 to 4.37 s | 1.57 to 3.38 s |
| cost per reply, writing and checks | $0.026 | $0.032 |

Beside the game (off_card_bench.py, 24 lines): the voice's own time to a first sound was 1.97 s for a first piece of 20 characters, 2.47 s for 35, 3.66 s for whole first sentences.

**Under two seconds: not reached.** The free voice alone takes longer than two seconds for all but the shortest pieces. A streaming cloud voice (about 0.2 s) leaves the first sentence's check, 1.0 to 1.9 s after the sentence is written, as the floor: about 2.4 s.

**Quality, blind (a fresh reader, the five pairs, not told which was which):** openings about even (one model's better twice, the faster once, two equal); whole replies worse with the faster first sentence in 4 of 5, padded with facts nobody asked for and running on, as Sonnet carried on from Haiku's sentence.

**Cost per hour, measured:** 15 replies an hour at $0.032 with 143 characters each: $0.48 writing and $0.09 voice, $0.57; heavy, 60 an hour: $1.94 and $0.34, $2.28. Plus Starter's $6 a month.
