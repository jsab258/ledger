# LEDGER — early audit of the local replacement

**24 September 2026**

Audited main at [32f455b](https://github.com/jsab258/ledger/commit/32f455bae4f2dc6a3423b90d1838ea0e44d73b7d). **The replacement is producing game changes, but it is already rebuilding the mechanisms that delayed the game.**

1. **The biggest risk remains postponing the encounter that could invalidate the whole project.**

   The new player can walk and run, but has no crime or conversation input. The crime key belongs to the older probe character. Meanwhile, the conversation helper creates separate empty memories and knowledge stores, and supplies **Day 1** on every request. These components do not yet constitute one persistent encounter. Connecting their state is more important than another building. [SliceCharacter.cpp:91–102](https://github.com/jsab258/ledger/blob/32f455b/ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp#L91-L102), [LedgerCharacter.cpp:67–80](https://github.com/jsab258/ledger/blob/32f455b/ue-probe/Source/LedgerProbe/Private/LedgerCharacter.cpp#L67-L80), [TalkHelper:63–102](https://github.com/jsab258/ledger/blob/32f455b/ledger/TalkHelper/Program.cs#L63-L102).

   One safeguard I said to retain is weaker than advertised: the packaged “restart” test writes a save, then restores **strings retained in memory** into reconstructed objects. It never proves that closing the program and loading the saved file preserves the encounter. [CrimeProbe.cpp:838–893](https://github.com/jsab258/ledger/blob/32f455b/ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp#L838-L893).

   The cheapest risk reduction is one player-driven crime, witnessed and unwitnessed, followed by gossip, direct questioning and a genuine quit/reload. Use the existing street.

   Instead, the plan requires closing the current stage’s checklist before advancing. Stage 1 includes switchable lights and consistent cutscene brightness. Those are now prerequisites competing with the premise itself. My broad feature inventory was an inventory—not a dependency chain. Making almost everything a mandatory floor was a mistake. [CLAUDE.md:32–41](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L32-L41), [ROADMAP.md:333–345](https://github.com/jsab258/ledger/blob/32f455b/ROADMAP.md#L333-L345).

2. **The local replacement was only partially implemented.**

   My classification of the [post-switch history](https://github.com/jsab258/ledger/compare/c10749e...32f455b) finds **601 commits**: 37 merges, 122 automatic probe returns, and 442 remaining commits. Crediting mixed commits to game work whenever they touched runtime code, content or asset-generation sources:

   | Changed work | Commits | Share of 442 |
   |---|---:|---:|
   | Game/content sources, including engine probes | 177 | 40% |
   | Records and notes only | 156 | 35% |
   | Tools, infrastructure and tests | 48 | 11% |
   | Research and references | 31 | 7% |
   | Evidence captures and acceptance records | 30 | 7% |

   These are **commit shares, not hours or wasted budget**. Counting engine probes as game also makes this a generous production classification.

   Actual additions include the animated player, head turns, positional sound and persistence comparisons. “Nothing playable” would now be wrong; “the intended encounter is playable” would also be wrong. [Player commit](https://github.com/jsab258/ledger/commit/4c743e07001775ebf9708de0dbef22010a0d8b17), [head turns](https://github.com/jsab258/ledger/commit/b969697454aadec862424746336039ae95bdfc8f), [sound](https://github.com/jsab258/ledger/commit/59b88b53b08943fa50121d90c6e731d9b17e9da3).

   The stage counts show **24/47**, **5/255**, and **3/142** completed in the first three stages—not percentages of a finished game. The current roadmap actually contains **979 unique checklist rows**, beyond the quoted 963. [FOR-JAFAR.md:43–51](https://github.com/jsab258/ledger/blob/32f455b/FOR-JAFAR.md#L43-L51), [roadmap checklist](https://github.com/jsab258/ledger/blob/32f455b/ROADMAP.md#L270).

   The administrative relapse is concrete: the prescribed five-line NOW file has **1,290 lines**; the stop hook has **587**. It enforces continued work and reporting format, and required session-specific exceptions after trapping another session overnight. These were owner-authorised exceptions, not agent disobedience. [NOW.md](https://github.com/jsab258/ledger/blob/32f455b/NOW.md), [sitting-clock.py](https://github.com/jsab258/ledger/blob/32f455b/tools/sitting-clock.py), [CLAUDE.md:58–65](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L58-L65).

3. **The building measurement is useful, but it cannot price the remaining game.**

   The **61 minutes** measure a new exterior made using existing recipes, materials and checking tools. It still lacks its identifying sign. The preceding three-facade sitting measured checking existing buildings; its tools were built before measurement began. Neither establishes the cost of an enterable, furnished, functioning business. [FOR-JAFAR.md:60–67](https://github.com/jsab258/ledger/blob/32f455b/FOR-JAFAR.md#L60-L67), [measurement record](https://github.com/jsab258/ledger/blob/32f455b/production/sittings/2026-09-24-three-facades.md#L69-L86).

   Moreover, **39 minutes 54 seconds** elapsed between its three dispatch commits and their returns: **12:57, 12:57, 14:00**. That is roughly two-thirds of the sitting spent inside the runner round trips, although the history cannot separate queueing, building and rendering. Local implementation still does not mean local iteration before committing. [First return](https://github.com/jsab258/ledger/commit/635510b4c37c376a9e3d738671702294c781ab6d), [second](https://github.com/jsab258/ledger/commit/3576324aaf6efd61d94fbba07d247ce947027b21), [third](https://github.com/jsab258/ledger/commit/76f42503be844d46c485f52087ed198a8a3ad2f6).

   My **low-confidence planning ranges**, assuming 20 focused implementation hours weekly, existing assets and sharply limited scope:

   | Target | Remaining effort / calendar |
   |---|---|
   | Existing five-condition “presentable” milestone | Already recorded complete on 23 September; confirm by walking it |
   | Integrated 10–15-minute slice | 20–40 hours / 1–2 weeks |
   | Friends’ 30-minute test build | 60–120 hours cumulatively / 3–6 weeks |

   These estimate integration, a small playable situation, basic controls/save handling and testing—not completing every stage. They estimate **reaching the test, not passing it**. The dependencies are in [ROADMAP.md:43–105](https://github.com/jsab258/ledger/blob/32f455b/ROADMAP.md#L43-L105) and [stage 5](https://github.com/jsab258/ledger/blob/32f455b/ROADMAP.md#L231-L243). Unresolved integration could double them.

   Your approximately **1%** reading implies an **85%** allowance could fund roughly 85 identical repetitions, requiring **86 agent-hours**. That is arithmetic, not a demonstrated production rate. Coding, interiors and encounter design have no comparable meter measurement. The small slice is not disproved economically; its cost remains unestablished.

4. **The business direction caps liability but does not establish viable economics.**

   The research still models **14¢/hour** and **$5.60** for a 40-hour allowance. The repository’s actual call sample implies **16–63¢/hour**, depending on assumed conversation frequency. At its middle and upper assumptions, 40 hours costs **$12.40–$25.20**, against the spreadsheet’s **$17.49** net sale proceeds—before hosting and other costs. These use repository prices, not independently verified invoices. [Business summary:16–18](https://github.com/jsab258/ledger/blob/32f455b/production/research/runtime-ai-business/SUMMARY.md#L16-L18), [call-cost measurement](https://github.com/jsab258/ledger/blob/32f455b/production/research/talk-helper/cost-of-an-hour-2026-09-23.md).

   Prewriting unsolicited speech is appropriate **if selection still depends on actual knowledge**. But it supplies no additional saving against that measured bill: ambient speech was already excluded. And an allowance that ends direct conversation disables part of the product’s premise. Keep this a provisional business hypothesis, as the decision currently says. [Cost report:49–50](https://github.com/jsab258/ledger/blob/32f455b/production/research/talk-helper/cost-of-an-hour-2026-09-23.md#L49-L50), [DECISIONS.md:223–224](https://github.com/jsab258/ledger/blob/32f455b/DECISIONS.md#L223-L224).

5. **The model and character decisions are narrower than the conclusions being drawn.**

   Keeping the paid router follows the comparable results: **286/299 versus 271–274**, **0.7 versus 1.4 seconds**. However, the paid result still contains **12 confidently wrong answers**. This is evidence for a relative choice, not reliable interpretation. The research improvements also remain separate from the production router. [Local-model summary:6–18](https://github.com/jsab258/ledger/blob/32f455b/production/research/local-models/SUMMARY.md#L6-L18).

   “VCTK makes voices flat” is a plausible hypothesis, not an isolated diagnosis. Changing speakers confounds identity with delivery. Compare the same speaker and line using different reference delivery and emotion controls. More immediately, Nano takes roughly **four seconds to produce a three-second line** while the game runs, before playback begins. That is a conversation problem regardless of timbre. [Voice ruling](https://github.com/jsab258/ledger/blob/32f455b/DECISIONS.md#L226), [Nano measurement:35–45](https://github.com/jsab258/ledger/blob/32f455b/production/research/nano-listening-test/card-timing-2026-09-24.md#L35-L45).

   MetaHuman is a reasonable component choice, but one dressed idle figure proves neither period wardrobe production nor moving-crowd performance. Stop treating further dressing of the test figure as a prerequisite for integrating the slice. [DECISIONS.md:221–224](https://github.com/jsab258/ledger/blob/32f455b/DECISIONS.md#L221-L224).

6. **On Monday, change the stopping condition.**

   Make the week’s outcome **one integrated encounter**, including shared knowledge, audible consequence, direct questioning, actual disk reload and the unwitnessed control. Retain the Core suites and independent simulation review. Suspend visual-stage completion and the new mandatory AI playtester as prerequisites. [Current safeguards](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L53-L54), [new tester gate](https://github.com/jsab258/ledger/blob/32f455b/ROADMAP.md#L83-L105).

   Render locally during iteration; bank accepted batches. Keep NOW to current work. Measure this complete encounter’s elapsed time and your meter change. Another facade measurement will not answer the missing economic question.

**Confidence:** high in counts and cited code gaps; moderate in structural judgment; low in forecasts. I could not run Unreal, independently inspect the binary frames, verify the PC’s current processes, or read the subscription meter.

