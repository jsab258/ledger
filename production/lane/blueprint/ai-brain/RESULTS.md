# Results: five brain levels side by side

24 Nov 2026, the brain job. Method in VARIANTS.md; numbers from outputs/metrics.json and the blind judges' files in responses/; corrected once after the fresh review (REVIEW.md, 12 must-fix and 12 should-fix points; section "After the review" says what changed). Proxies only: AI players, AI judges; fun shows only in real play.

## Shortfalls first

- V5 (AI-authored, rule-run) failed: 23 faults in 12 playthrough-evenings (after the review's correction), 22 flat moments, 1.17 retellable an evening. People repeated their written rows whatever Frank said. Built here with Sonnet as the author; an Opus author is untested.
- V1 (rules decide, AI talks; the design now) came fourth on interest (1.83 retellable an evening against 2.75 to 2.92 for V2 to V4) and had 5 faults after correction, against 2 to 3. Its remaining faults come from two rule outcomes this job wrote (Grace's squeeze, Kevin's plant), repeated across styles: the V1 result judges this job's quick rules as much as the level.
- V2 (AI proposes, rules check) is not proven better than V1 on everything. As tested it needs the classifier's tags before it can build the allowed set, so it takes two model calls before the first word, like V1 (about 2.8 s, over the 2 s bar). Its words can outrun its action: in M03 Rita told the talker where the radios went while the game carried out nothing (a bargain). Its talker payoff is unstable: on replay Rita, Jason and Shane moved from help to bargain, and the talker's lead over the honest player falls from +0.12 to about +0.04. Asking again until yes was not measured. The mode BRAIN-SWITCH proposes (V2 with the rules deciding the seven guarded moments) was not itself run or judged.
- V4 (AI decides) let the model decide a turning point (June dropped her claim to the honest player), punished the talker (-0.19 against honest), and about 8 of its 60 outcomes were new deeds the game has no code for ("goes to tell Danny"); its town-wide social life would cost about US$1.43 an evening on top of talk.
- No variant granted an impossible ask: 0 of 15 for V1 and V5, 0 of 30 for V2, V3 and V4 over two breaker rounds. For V1, V2 and V5 that holds by construction once the classifier tags the ask impossible, which it did for all fifteen breaker talks; the breaker never attacked the classifier itself, which is those variants' real gate. A floor, not proof.
- AI-run gossip did not agree with itself: on the same input, the V3 pass found 10 tellings and the V4 pass 36, and they read the input differently (V4 counted victims as knowing their own deed). V4 spread every deed wider than the temper model (the debt threat to 11 of 20 against 2); V3 spread the blow on the rank wider (12 against 5) and the other three narrower. The two sides were counted over different people and hours, so the comparison is rough.
- Interest among V2, V3 and V4 is a tie: 35, 34 and 33 moments from one judge in one pass.

## The table

| | V1 rules decide | V2 AI proposes, rules check | V3 AI social life | V4 AI decides | V5 AI-authored |
|---|---|---|---|---|---|
| Faults (blind; 12 playthrough-evenings), as judged | 9 | 5 | 3 | 2 | 24 |
| Faults after removing two harness defects (M11's grant named facts missing from the card; M15's honest grant planted a story the lines never told) | 5 | 3 | 3 | 2 | 23 |
| Retellable moments an evening (blind, one judge) | 1.83 | 2.92 | 2.83 | 2.75 | 1.17 |
| Funny / flat | 4 / 7 | 12 / 7 | 10 / 5 | 7 / 3 | 6 / 22 |
| Impossible asks granted | 0 of 15 | 0 of 30 | 0 of 30 | 0 of 30 | 0 of 15 |
| Value to Frank by action label: honest / talker / racketeer | 0.37 / 0.58 / 0.41 | 0.47 / 0.59 / 0.19 | 0.38 / 0.39 / 0.31 | 0.53 / 0.33 / 0.11 | 0.24 / 0.39 / 0.31 |
| Talker minus honest (agency) | +0.21 | +0.12 (about +0.04 on replay) | +0.01 | -0.19 | +0.15 |
| Model calls before the first word, as tested | 2 (classify, voice) | 2 (classify, propose) | 1 in open moments, 2 in guarded | 1 | 2 |
| First sentence, estimated from the bench | about 2.8 s | about 2.8 s | 1.5 s open, 2.8 s guarded | 1.5 s | about 2.8 s |
| Social life off the talk path, an evening, whole town (estimate) | none | none | about US$0.06 | about US$1.43 | none |
| Replay: same action on the same 30 prompts | code, given the tags | 24 of 30 | 28 of 30 (14 of 16 in open moments) | 25 of 30 | code, given the tags |
| New deeds the game has no code for | 0 | 0 | free text in open moments, not counted | about 8 of 60 | 0 |

Value is scored on the action label (help 1, bargain 0.6, stall 0.3, lie 0.1, refuse 0, goes to someone against him -0.5), not on what is actually given, so a bargain that hands over the fact scores below a help.

Speed: from the builder's bench on his PC (Sonnet 5.5 median 1.41 s to the first sentence, Haiku 1.71 s on one run), not measured here. A two-call design meets the 2 s bar only if the classifier is much faster (a small local model) or merged into the reply call, which would let the model tag its own player's line, a gate the breaker could then attack; neither was tested. Today's free talk in the Unreal build (median 2.02 s, 4 Nov) has no classifier in front because decisions go through written decision lines (part 3.6.5).

Cost: the bench puts Sonnet 5.5 live talk at about US$0.09 a real hour at 15 replies (a floor), about US$0.27 a three-hour evening for one call a reply; two calls a reply come to about US$0.46 (the harness's token ratio of 1.7). V1, V2 and V5 cost about the same; V3 adds about US$0.06 and V4 about US$1.43 for town-wide social life (harness token estimates, scaled from twenty people to 118). All fit his US$5 an evening cap (ruling of 4 Oct). Prices from third-party pages (US$2 in, US$10 out a million tokens), not Anthropic's own.

## What the judges said about agency (blind letters resolved)

- V2: clear payoff (Rita free, Jason paying, Shane crossing over, June at the table, the story planted), and menace costs the racketeer; but three of those five wins changed to bargains on replay.
- V3: modest payoff; menace has believable costs.
- V4: menace has the strongest costs; the talker barely beats the honest player.
- V1: the talker gains visibly, but menace has few costs.
- V5: little payoff; the same set lines whatever Frank says.

## Brain by importance

Not supported by this test. Of the fifteen moment people seven are principals and eight supporting; no resident was in a moment. Counting the interest judge's retellable moments by tier over all twenty transcripts gives 7.6 a moment for the core cast against 10.6 for supporting people, so the core cast was not where the moments came from here, and faults did not separate the tiers. Tiering remains a cost and scope choice (the fourteen principals are few, the 49 minor people and the crowd stay on rules and written lines as his ruling of 24 Nov on residents' lines has it), to be tested in the loops, not a measured gain.

## Testability

V1 and V5 replay exactly from the log once the classifier's tags are stored. V2 changed its chosen action on 6 of 30 fresh calls, all inside the allowed set: the checkers can test the set and the carried-out grant exactly, and a recorded answer (a cassette) makes replays deterministic. V3's gossip pass is one model run with no rules underneath. V4's new deeds cannot be checked by code.

## After the review

Taken in: V2's two calls and 2.8 s; the guarded hybrid untested; corrected fault counts; V1's rules named as this job's; V2's unstable talker payoff and its words outrunning its action; impossible asks held by construction for V1, V2 and V5; V4's new deeds recounted (about 8, not 27); the gossip claim narrowed; the tier claim withdrawn; SUMMARY's slips. Not done (budget): re-judging with the defects fixed, the guarded hybrid run, a neutral outcome form for blinding, second judges, a breaker against the classifier. These are listed for the loops in BRAIN-SWITCH 8.13.4.
