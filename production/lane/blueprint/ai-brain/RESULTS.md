# Results: five brain levels side by side

24 Nov 2026, the brain job. Method in VARIANTS.md; numbers from outputs/metrics.json and the blind judges' files in responses/. Proxies only: AI players, AI judges; fun shows only in real play.

## Shortfalls first

- V5 (AI-authored, rule-run) failed: 24 faults in 12 playthrough-evenings, 22 flat moments, 1.17 retellable an evening. People repeated their written rows whatever Frank said. Built here with Sonnet as the author; an Opus author is untested.
- V1 (rules decide, AI talks; the design now) came fourth: 9 faults, 1.83 retellable an evening. Its faults came from the rules deciding outcomes the cards contradict (Kevin telling Frank to his face he passes things to the Widow; Grace "thinking on" protection money), which the model then had to voice. It also needs two model calls in a row when talk decides anything (about 2.8 s to the first sentence, over the 2 s bar).
- V4 (AI decides) is the most coherent on paper but the least buildable: 27 of its 60 outcomes were free-text deeds the game has no code for ("goes to tell Danny", "will tell the police"), so they cannot be carried out or tested; it punished the talker (-0.19 against the honest player); its town-wide social life would cost about US$1.43 an evening on top of talk.
- No variant granted an impossible ask: 0 of 15 for V1 and V5, 0 of 30 for V2, V3 and V4 over two breaker rounds (five turns, the second adapted to the replies). One soft spot: Kevin Needham, the Widow's informer, offered in V3 and V4 to tell Frank what he passes on, for a price; the breaker's goal was that for nothing.
- AI-run gossip spread far wider than the temper model's: by Friday the blow on the rank was known to 12 (V3) and 13 (V4) of the twenty against 5 under the rules; the debt threat to 11 under V4 against 2. The two passes read the same input differently (V4 counted victims as knowing their own deed, V3 did not) and found 10 against 36 tellings.

## The table

| | V1 rules decide | V2 AI proposes, rules check | V3 AI social life | V4 AI decides | V5 AI-authored |
|---|---|---|---|---|---|
| Faults (blind; 12 playthrough-evenings) | 9 (0.75 an evening) | 5 (0.42) | 3 (0.25) | 2 (0.17) | 24 (2.0) |
| Retellable moments an evening (blind) | 1.83 | 2.92 | 2.83 | 2.75 | 1.17 |
| Funny / flat | 4 / 7 | 12 / 7 | 10 / 5 | 7 / 3 | 6 / 22 |
| Impossible asks granted | 0 of 15 | 0 of 30 | 0 of 30 | 0 of 30 | 0 of 15 |
| Value to Frank: honest / talker / racketeer | 0.37 / 0.58 / 0.41 | 0.47 / 0.59 / 0.19 | 0.38 / 0.39 / 0.31 | 0.53 / 0.33 / 0.11 | 0.24 / 0.39 / 0.31 |
| Talker minus honest (agency) | +0.21 | +0.12 | +0.01 | -0.19 | +0.15 |
| Calls before the first word | 2 (classify, voice) | 1 | 1 | 1 | 2 |
| First sentence, estimated from the bench | 2.8 s (3.1 s with a Haiku classifier) | 1.5 s | 1.5 s | 1.5 s | 2.8 s |
| Talk cost an evening, relative | 1.7 | 1.0 | 1.0 | 1.0 | 1.7 |
| Social life off the talk path, an evening (whole town, estimate) | none | none | about US$0.06 | about US$1.43 | none |
| Replay: same action on the same 30 prompts | code (given the tags) | 24 of 30 | 28 of 30 | 25 of 30 | code (given the tags) |
| Outcomes the game has no code for | 0 | 0 | 0 in guarded moments; free text in social ones | 27 of 60 | 0 |
| Core overrides needed | none possible | 0 | 0 | none possible | none possible |

Cost: the builder's bench puts Sonnet 5.5 live talk at about US$0.09 a real hour at 15 replies (a floor), so about US$0.27 for a three-hour evening at relative cost 1.0 and about US$0.46 at 1.7; the harness's own token estimate is lower (US$0.07 and US$0.12), so the bench figure is used. All fit his US$5 an evening cap (ruling of 4 Oct); V4's social life would take about a third of it. Prices from third-party pages (US$2 and US$10 a million tokens), not Anthropic's own; speeds from his PC's bench, not measured here.

## What the judges said about agency (one line each, blind letters resolved)

- V2: clear payoff; the talker gets Rita free, Jason paying, Shane crossing over, June at the table and the false story planted, where the honest Frank gets refusals; the racketeer's menace costs him a police witness, Ada's free account, Grace's goodwill and a reported bribe.
- V3: modest payoff; menace has believable costs.
- V4: menace has the strongest costs; the talker barely beats the honest player.
- V1: the talker gains visibly, but menace has few costs.
- V5: little payoff; the same set lines whatever Frank says.

## Brain by importance

Of the fifteen moment people, seven are principals (the core cast) and eight supporting; no resident was in a moment, so the residents' tier is argued, not measured. Faults by tier did not separate the tiers (V2: core 3, supporting 2; V3: 0 and 3). The case for tiering is cost and scope, not measured quality: the core cast's 14 people are where retellable moments come from, so they can carry V3's social layer (retold gossip in their own words, a weekly goal) for about US$0.01 an evening; the 56 supporting people take V2; the 49 minor people and the crowd stay on rules and written lines, as his ruling of 24 Nov on residents' lines already has it.

## Testability

V1 and V5 replay exactly from the log once the classifier's tags are stored. V2 changed its chosen action on 6 of 30 replays, but every choice stayed inside the allowed set, so the checkers can test the set and the Core's grant exactly and record the model's pick for replays. V3 kept 28 of 30, but its gossip pass is a single model run with no rules underneath. V4's free-text deeds cannot be checked by code at all.
