# How much should the AI be the brain of LEDGER's people? The variants and the method

24 Nov 2026, the brain job (claude-opus-5-5, lane-2026-11). Results in RESULTS.md, the owner's page in SUMMARY.md, the switch in BRAIN-SWITCH.md, extracts in SAMPLES.md. Everything here is a proxy measured by AI players and AI judges; whether any level is fun shows only in real play.

## 1. The five variants as built in the harness

All five share the same people (data/people, temper/tempers.json), ties, routines, the same fifteen moments and the same player lines. They differ only in who decides.

| | Who decides what a person does | What the language model is given | What the game carries out |
|---|---|---|---|
| V1 Rules decide, AI talks (the design now) | The Core, from the classifier's tags on the player's line (menace, money offered, leverage named, a real tie appealed to, whether the ask is possible) and the person's dials | The decision, to voice | Only the moment's defined grant, if the rules say help |
| V2 AI proposes, rules check | The model picks one action from the set the rules allow this person here (help only when the rules' score is within 0.15 of the bar and the ask is possible; bargain, lie, go to someone only where the dials allow) | The allowed set and the exact grant | The defined grant if help; any action outside the set is overridden to V1's outcome |
| V3 AI runs social life | The model, for trust, talk, gossip and a weekly goal; the rules for money, freedom, life and death and the story's turning points (here M01, M07, M08, M14 money; M10 freedom; M12, M13 turning points) | The guarded ruling where one applies; otherwise free | Free-text grants in social moments; the defined grant in guarded ones |
| V4 AI decides | The model, everything; rules only for what is physically possible | Nothing but the person and the moment | Whatever the model grants |
| V5 AI-authored, rule-run | At build time a model wrote each person's behaviour rows (conditions on the same tags, an action, two lines); at run time code matches the rows | The matched action and the written lines, to voice close to them | The defined grant if the matched row says help |

The rules are the temper model's (temper/TEMPER-MODEL.md section 3; temper/temper_sim.py class New) with per-moment shapes and talk modifiers added for this test in brain_harness.py, rule_score(): leverage named adds 0.15, a real tie appealed to adds 0.10 where regard is at least 0.3, money in weeks of wages and menace enter as the temper formulas take them. These additions are this job's, not the blueprint's.

## 2. The test

- The people: the twenty nearest Frank's path. Fifteen are the moments' people; five more by the hours they spend in the path's places on Monday, Wednesday and Friday evenings, 17:00 to 23:00 (Albert Suggitt, Lily and Peter Tang, Shaun Hewson, Sylvia Rennison). They appear in the gossip and ambient passes.
- Three evenings (Monday, Wednesday, Friday), fifteen set moments: a bribe to a witness, a threat, asking about Danny, a lie that the Widow sent Frank, a witness questioned (Ada), a recruit offered, a debt called in, a squeeze, a poach, a constable asked to look away, the red book, the confession, June's claim, the Fixer, a planted story. Each has a possible ask, a defined grant, the facts the person holds, a leverage Frank may use and an impossible ask.
- Four player styles: honest, racketeer and talker (two lines each, written by the lead before any run, inputs/moments.json); and the breaker, a fresh Opus adversary told only to talk people into the impossible or break the town, who wrote three escalating turns per person blind (responses/breaker_lines.json), then, after reading the first replies of V2, V3 and V4 (as letters), two more adaptive turns each (responses/breaker_round2.json).
- What people know: deeds the playthrough commits (the blow on the rank for all; three threats for the racketeer) spread by the temper model's gossip hour by hour for V1, V2 and V5; for V3 and V4 by a model-run ambient pass over the 189 meetings among the twenty (responses/ambient_V3.json, ambient_V4.json), which also gave each person a weekly goal. The man a deed was done to knows it.
- The in-game model: the brief asks for Sonnet 5.5, the game's live model. This cloud job has no API key, so every in-game call was answered by a Sonnet helper through the session's helper tool, one batch file per variant and style pair, each prompt answered as a fresh call. 300 encounters, plus 45 second-round breaker talks and 90 replays. The helper is the tool's current Sonnet; its exact version was not confirmed.
- Judges: two fresh Opus readers, blind to the variants (letters by a fixed hash: A V2, B V3, C V5, D V1, E V4). One counted faults against the cards and facts (out of character, contradiction, invented, impossible yes); one counted retellable moments by EMERGENT-MEASURE's spirit (tests 2 and 4 cannot be proved on single scenes, so a looser "would a player tell a friend" count), funny and flat moments, and judged agency.
- Code measures: the outcome's value to Frank (help 1, bargain 0.6, stall 0.3, lie 0.1, refuse 0, goes to someone against him -0.5) by style; Core overrides; impossible asks granted; replay agreement (the same 30 talker and breaker prompts answered twice for V2, V3, V4); outcomes the game has no code for.
- Cost and speed are not measured here (helper calls are not API calls). They are derived: tokens from the prompts (4 characters a token), Sonnet 5.5 at US$2 in and US$10 out per million (pricepertoken.com, updated 22 Oct 2026, and eesel.ai, 29 Sep 2026, both read 24 Nov; not confirmed on Anthropic's own page), 45 replies an evening (15 an hour, the builder's bench assumption, over three hours); speed from the builder's bench on his PC (Sonnet 5.5 median 1.41 s to the first sentence over two days; Haiku 1.71 s on one run).

## 3. What would make these numbers lie

- AI players and AI judges measure proxies. A judge's "retellable" is one reader's taste; fun shows only in real play.
- Fifteen moments, one judge each: differences of one or two faults between V2, V3 and V4 are within judging noise (the coherence judge said so); the gaps to V1 and V5 are large enough to stand.
- Encounters are independent: an outcome in one moment does not change a later one beyond the fixed gossip state. Consequences across evenings are not tested.
- V1 and V5 are only as good as their rules. V1's rules here are a quick extension of the temper model; V5's rows were written by Sonnet (an Opus author might do better, untested). The V1 and V5 results judge these rules as much as the level.
- The breaker had five turns at most; a human with hours and a reload button will find more. Zero granted impossible asks is a floor on safety, not a proof.
- The constable's knowledge of the blow on the rank is written into his moment's facts, so his callback is the scene's, not play's (the interest judge noticed).
- The ambient passes ran once each, on the racketeer's week only.

## 4. Files

brain_harness.py (stages base, encounters, apply, round2, apply2, report, metrics); inputs/ (people, moments, cards, briefs); batches/ (every prompt sent); responses/ (every helper and judge output); outputs/ (applied.json, applied_round2.json, metrics.json, results.json, blind_key.json); transcripts/ (the twenty blind transcripts and the second round).
