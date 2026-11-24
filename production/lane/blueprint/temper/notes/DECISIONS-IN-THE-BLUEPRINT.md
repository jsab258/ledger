# Every decision a townsperson makes, and what drives it

Read: BLUEPRINT-01, 02, 03 (grepped, key parts read), SYSTEMS-THE-STORY-NEEDS, the economy design, and the Core C# in ledger/Assets/Scripts/Core (only Core is in this tree; no loader that maps data to Gossiper, and no callers outside Core).

Key. Frank is the player (code says "the new owner"). N = Nerve, L = Loyalty (goodwill to Frank, moves in play), G = Greed. "Fixed" means a trait; "state" means it changes. Code defaults: N, L, G all 0.5 (Gossip.cs:115-117). Design part numbers are BLUEPRINT-02 unless prefixed 1. or 3.

## The table

| # | Decision | Design | Code | Inputs | Formula or threshold | Per person in design? |
|---|---|---|---|---|---|---|
| 1 | Witness reports to police | 2.5.2, 2.6.3 | PoliceFile.cs:226 (OnHisSide :224; TownWeek.cs:109) | N (fixed, but drops 0.1 after a killing); L (state); Suppressed topic, Leashed, cast "police":"never" or keepsQuiet "owner" (state/flags) | Damage, wounding or robbery: N >= 0.4 and L <= 0.575. Killing: L <= 0.575 only. Common assault by a witness: never. Suppressed blocks all but a killing | Yes: "neighbour reports unless on his side or talked round" |
| 2 | Victim reports | 2.5.2 | PoliceFile.cs:233-238 | N, L | Damage: always. Assault: L < 0.4 and N >= 0.5. Wounding or robbery: L < 0.6 and N >= 0.3. Killing: never | Yes (settle it themselves, or too frightened) |
| 3 | Cracks and talks to police about a body | 2.5.2 | Homicide.cs:561 | N, L, Leashed | N < 0.35 and L <= 0.575 and not leashed | Yes |
| 4 | Testifies, corroborates a charge | 2.6.3, 2.6.5 | Informing.cs:94-177; Homicide.cs:255 | Caller supplies WouldTalk and credibility; story confidence | Counts if rumour confidence >= 0.5 (Homicide.cs:123); each extra witness +0.25 | No temper rule written; row 3 is the only per-person test |
| 5 | Sets off to tell: how fast, where | 2.5.1, 1.4.5 | Observation.cs:489 (Delivery.Begin) | N, willingness | N < 0.35: runs, walk x 0.45. Willingness < 0.5: waits 20 + 70(1 - w) minutes | Yes (destination "is characterisation") |
| 6 | Willingness to say it (formula) | 2.5.2 | Observation.cs:364 | N, L, own secret, fear of outfit, sympathy for victim | 0.45 + 0.35N + 0.35 sympathy - 0.55L - 0.85 secret - 0.45 fear. Never used: Observation.cs:289 and :325 hard-set it to 1.0 | Intended |
| 7 | First reaction (ignore, notice, investigate, alarm, flee, fetch police, deliver) | 2.5.3 | Reaction.cs:50 | Severity, N, "dutiful", willingness, body seen, already alarmed | Body or severity >= 0.75: N < 0.3 flee; dutiful > 0.55 fetch police; willingness > 0.4 deliver; else alarm. Below: N < 0.25 and severity > 0.5 flee; severity >= 0.45 and N > 0.4 investigate; else alarm | Yes |
| 8 | Steps in (hold-up, beating) | 2.5.3, 1.3.9 | Reaction.cs:66 | N, severity, already alarmed | Intervene only if N > 0.85, severity >= 0.9, someone already alarmed. Design says unarmed and "with the nerve" | Yes, no number in design |
| 9 | Flees | 2.5.3 | Reaction.cs:65, :75; Arsenal.cs:307 | N, weapon, public place | See 7, 10. Checklist A13.18 gap: run toward doors | Yes |
| 10 | Faces a drawn weapon | 1.3.7, 1.6.15 | Arsenal.cs:287-309 | Target N; weapon menace x (0.55 + 0.65 Frank's violence reputation); target armed or outfit | N > menace + 0.20: calls bluff. menace > N + 0.35: flees screaming in public, else complies. Between: freezes. Armed or outfit: escalates | Yes |
| 11 | Comes to look | 1.4.8, 2.5.3 | Reaction.cs:76; Notice.cs:104 | N; what is noticeable | Remarks if interest x (0.35 + 0.9N) >= 0.45: weapon needs N >= 0.11; blood 0.2; wrong place 0.33; running at night about 0.24; loitering 0.86 | Yes |
| 12 | Stands or folds in a fight | 1.3.8 | None in Core | Design: watched or cornered stands longer, alone gives way sooner, blood on Frank lowers his nerve | None. Data has fight_kind for 25 people, read by nothing | Yes |
| 13 | Shopkeeper answers a hold-up | 1.6.15 | None | "By his temper" | None written | Yes |
| 14 | Tells gossip or not; passes it on | 2.4.1, 2.14 | Gossip.cs:540-562 | Tie strength (state of graph; cast "ties"); same place; story confidence; Suppressed; Leashed; owner flag (KeepsHisDeedsFor) | Told if tie > 0, confidence x tie x 0.8 >= 0.2, once a round, not suppressed or leashed or Mickey's own. A body always passes. Reads no N, L, G, talk or discretion | Design says yes ("tells only her sister"); code says no |
| 15 | To whom | 2.4.1 | Gossip.cs:540; CastDay.cs ties; Confab.cs:98 | Ties, who is in the same place, 6.5 m | Listener walks to the teller | Ties differ per pair; temper plays no part |
| 16 | Answers news in character (lines only) | 2.14 | StreetVoice.cs:813, :830, :847 | N, L, G | N > 0.65 and sensitive: nervous bank; else L > 0.65: loyal bank; else G > 0.65: greedy bank; else plain. Flavour only | Yes |
| 17 | Goes quiet when Frank walks up | 2.4.3 | Confab.cs:147 | Tie (stands in for nerve) | Breaks off inside 4.5 x (1 - 0.62 tie) metres | Not temper: tie is borrowed |
| 18 | Keeps quiet when asked | 2.5.2 | Silence.cs:288; CastDay.cs:154, :589; DeedTalk.cs:133 | Cast keepsQuiet word (fixed); first-name terms (state); how grave | Grave (killing): never. owner: yes. friend: only on first-name terms. anyone: yes, but breakable. nobody: no | Yes. Data holds a true/false (38 true of 119); CastDay.cs:158 throws on a boolean |
| 19 | Takes a bribe to stay quiet | 2.5.2, 1.4.5 | Gossip.cs:1046-1075 | G; price; confidence | Price 50 + 150 x confidence. Takes it if G >= 0.3 (L +0.05). Else backfires: L -0.15 and a 0.9-confidence rumour. A body: refused | Yes ("her temper decides how hard she is to pay") |
| 20 | Yields to a threat | 2.5.2 | Gossip.cs:1078-1105; Silence.cs:265 | N, L | N <= 0.6: goes quiet, L -0.2. Else backfires, L -0.15, rumour "threatened". A body: refused | Yes. Design: threat stops the report, "never the street's talk"; Contain (Gossip.cs:1272) also stops telling, so check |
| 21 | Is blackmailed by a hook | RT-07, EC-09 | Gossip.cs:1187; Hooks.cs:10-62 | The secret (strong or weak), not traits | Strong: leashed for good, L -0.3. Weak: one story dropped once, L -0.2. Blackmail for money takes the purse, £50-300 | No: "knowledge beats traits" |
| 22 | Pays a debt, begs, or refuses | 2.8.1, 2.8.2 | Debts.cs:42, :111, :117 | L, N, purse (weekly £35-165 by hash) | L >= 0.5: pays what the purse holds (L -0.05, or -0.09 if emptied). Else N <= 0.5: begs a day. Else refuses, L -0.1, tells the street. At defaults everyone pays | Five debtors authored differently; 2.14 wants "debtor with nerve stands" |
| 23 | Borrows after being emptied | 2.8.2 | Debts.cs:163; Purses.cs:204 | Patron's spare cash | Once a night, patron keeps back a day's wage | No |
| 24 | Folds on a business squeeze | 2.17 | Empire.cs:461 | N, L | Hands over the shop if N <= 0.6 or L >= 0.6 (L -0.25). Else refuses and tells. At defaults everyone folds | Yes |
| 25 | Pays protection or refuses | EC-06, 2.17 | Not in Core (rackets are income lines only; Empire.cs:57) | Design: what the shop can bear; temper | £5-15 a shop; past that, tells by temper; after 3 squeezed weeks refuses and tells. "Afraid, not loyal" | Yes, no code |
| 26 | Agrees to a favour (any ask) | 2.11.1, 3.6.5 | Negotiation.cs:129, :155-215 | Ask size, L, suspicion, G, N, lever, novelty | Resistance = ask - 0.35L + 0.3 suspicion. Per push: money w(0.25+0.55G)(1-0.5s); need 0.85w; secret 0.8w; threat w(0.2+0.7(1-N)); respect w(0.15+0.45L); each repeat x 1/(1+n). Walks at resentment 0.9. After: L -= 0.5 x resentment (+0.2 for a secret) | Yes |
| 27 | Joins Frank's crew | 2.11.1 | Empire.cs:518, :558; RecruitAsk 0.7 (:352) | L, N, lever | Need route: L +0.25, joins at L >= 0.55. Competence = 0.3 + 0.4N + 0.2L, 0.2-0.9 (:538) | Yes; "loyalty ceiling" numbers a gap |
| 28 | Walks with him on a night | 1.7.4 | Companionship.cs:134 | L, N | L >= 0.55 and N >= 0.3 | Yes. Story wants Ron to refuse the gun (system 49, missing) |
| 29 | Is poached by a rival | 2.10.3, 2.11.3 | Empire.cs:1023-1050 | L only | Rival picks lowest-L crewman. L < 0.4: leaves. Else L +0.1 and tells Frank | "Least loyal man", yes |
| 30 | Rots, skims, quits | 2.11.2, 2.11.4 | Empire.cs:769-815 | L, route, cut | Skim: L -0.05 a day; generous +0.03. Need-route quits at L < 0.2. Hook-route skims a quarter at L < 0.3 | Yes |
| 31 | Betrays: talks to police or rival | 2.11.2 | Operation.cs:317; Companionship.cs:138; Household.cs:138 | L; Bond | Talker chance = (0.15 success, 0.4 partial, 0.65 failed) x (1 - L). Walks away at L < 0.4. Household talks at bond < 0.4. Nerve not read; "past his nerve he talks" has no code | Yes; break numbers a gap |
| 32 | Carries out a send | RT-08, 1.7.2 | Operation.cs (competence, not nerve) | Design: man's N against target's N, watchers, light, noise | None for nerve | Yes |
| 33 | Holds a post | RT2-09, 2.17 | None | Design: stands while loyal and has the nerve (story ask) | None | Yes |
| 34 | Driver leaves | 2.15.1 | None (economy F7: not modelled) | Pay under £60 two weeks, or frightened | Rule only | Frightened: yes |
| 35 | Remembers a slight or favour | 2.3.1, MEM-09 | L deltas throughout; Gossip.cs:1279; Harm.cs:292; Homicide.cs:520 | Event; N | Fixed constants (-0.05 to -0.3). Killing witness: L capped at 0.35 + 0.5N, N -0.1. Feud heat >= 0.5: will not work together | Memory is per person; the size of the grudge is not |
| 36 | Stance and warmth toward Frank | 2.4.3, 2.12.4 | StreetVoice.cs:285-345 | Suspicion, L, strongest story about him, leash, coat, knows him | Pressure = 0.55 suspicion + 0.45 story - 0.7 x (L - 0.5)+ (x0.4 if pressure >= 0.85) - 0.12 coat. Rungs at 0.12, 0.26, 0.42, 0.58, 0.72, 0.86 | Greetings by regard; not temper |
| 37 | What they say in live talk | 3.6.1 | ConversationEngine.cs:~572 | Suspicion level, memories, deed facts | The talk model is not given N, L, G, talk or discretion | No |
| 38 | Names him, trusts him (Sheila) | 2.12.1, Q7 | CastDay.cs:595; Trust.cs:30; ActThree.cs:513 | Knowing (four triggers), 3 talk days, no lies; Sheila L >= 0.7 to move ledgers | Gate is knowing, not liking | Sheila only |
| 39 | Tells Frank a secret | RT-07 | Hooks.cs:68 | L against floors the caller passes | L >= confess or share floor | Floors not set |
| 40 | Takes the firm (successor) | 3.1.3 | ActThree.cs:388 | L, competence, nerve | L >= 0.6, competence >= 0.55; design: most loyal man, 3 weeks, "not past his nerve" | Yes |
| 41 | Officers: look away, lose a statement, be bought | 2.6.8 | None | Fixed price per named officer; Ellis £800 then £100 a week | Authored | Authored |
| 42 | Haggles, buys, refuses goods | 2.7.5, 2.7.6 | Purses.cs | Purse, how hot the goods are, regard for Frank | No numbers | Partly |

## Temper fields read by nothing (in Core)

- venal: no Core code reads it. The nearest is Gossiper.Greed (bribe, money lever, one flavour line). Data derives venal from greed, from the prototype, or as 1 - 0.8 x dutiful (data build_people.py:320-330).
- talk (readiness to talk): read by nothing. Gossip.Tick ignores it; row 14 is the whole gap in the design. For 114 of 119 people it is just willingness copied; only 5 prototype people have a real value.
- discretion: read by nothing. For 114 of 119 it is 1 - 0.8 x willingness (build_people.py:336). The one "discretion" in code is a comment about Sheila (WeeksEnd.cs:37).
- temperament.nerve and top-level nerve are the same number. Gossiper.Nerve is read in about twelve places.
- temperament.dutiful: only a parameter of Reaction.Decide (:50). Gossiper has no such field, though Reaction.cs:48 says it does. In the data it is loyalty to Frank for 41 people, 1 - 0.8 venal for 5, a chosen figure for 73.
- temperament.willingness: Reaction.Decide, Delivery.Begin, Observation.Willingness. Nothing in Core calls Decide or Begin, and observations set willingness to 1.0.
- keepsQuiet: read, but as a four-word string (owner, anyone, nobody, friend); the data holds a boolean.
- No per-person "police: never" in data, though 2.5.2 names Rita, Wayne, Hal, the scrap dealer, the customs officer and the outfit's man. Only Core's cast file has it.

## Decisions that read a value with no per-person data

- Every L-based and N-based rule (rows 1, 19, 20, 22, 24, 26, 27, 29) runs on the 0.5 default for the named cast. PoliceFile.cs:54-58 says so; at defaults everyone pays a debt, takes a bribe, folds to a threat and a squeeze, and joins on a need. Only Population residents (crowd) get random values: G and N 0.2-0.8, L 0.3-0.7 (Population.cs:267).
- Starting loyalty to Frank has no source. Data "dutiful" is meant for it, but nothing loads it.
- Gossip passing (14) has a trait in the design and none in code. Tie strength stands in.
- Row 6 needs own secret, fear of the outfit and sympathy for the victim; nobody has any of the three.
- Rows 12, 13, 25, 32, 33, 34 have design text and no code.
- Rival men (data kind rival_man, 12 records) have no loyalty to their head; the code tracks only arm members as ids (Empire.cs:91). Story systems 7, 8 and 10 (pacts, betrayal, turning rivals' men) are missing.
- Crew nerve never enters a break decision: break uses loyalty alone (rows 29-31).
- Fixed numbers worth lifting to per person: 0.4 (report nerve), 0.575, 0.3 (greed floor), 0.6 (threat and squeeze), 0.5 (debt), 0.65 (flavour), 0.55 and 0.4 (crew floors), 0.35 (fright).
