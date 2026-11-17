# Review: SIM-IN-BROWSER-2026-11-17 (fresh reviewer, 17 November 2026)

Reviewed: production/research/lane/SIM-IN-BROWSER-2026-11-17.md. About 15 minutes. Nothing in the project was changed except this file.

## Verdict: PASS WITH FIXES

The main measured result holds: the real Core builds with an ordinary .NET 10 build, and PerceptionGolden's output matches the committed table exactly. But the plan's central build step (leave out FastChecker.cs and LlmClient.cs from the project file) will not compile as written. The five-line summary repeats that error, and several smaller claims are wrong or overstated. None of this changes the recommendation. It does change step 2 of the plan, and probably its hours.

## What was checked, and how

| Claim | Check | Result |
|---|---|---|
| 140 .cs files, 50,512 lines | find and wc on the Core | Confirmed |
| No reflection, unsafe or native calls | grep for System.Reflection, unsafe, DllImport, extern, Marshal, Activator, typeof | Confirmed. The only hits are two `e.GetType()` calls used in error messages (FastChecker.cs:88, MiniJson.cs:78), which are harmless |
| Only FastChecker.cs uses Task.Run | grep | **Wrong.** ConversationEngine.cs:1841 also uses `Task.Run`. Its `.Result` reads (1812, 1949) are guarded by a RanToCompletion check, so they do not block, and the conclusion (one thread in a Web Worker) still holds |
| Only MemoryStore.cs touches files | grep File./Directory. | Confirmed for the Core apart from FastChecker.cs |
| 13 files use InvariantCulture | grep -l | **17 files**, not 13 |
| Helper's Core copy is the real Core | diff -r of the scratch copy against ledger/Assets/Scripts/Core; diff of the csproj | Identical. The only change is the target framework, net8.0 to net10.0. Program.cs is identical |
| Output identical to the committed table | Re-ran the built PerceptionGolden myself; compared it, with CRs stripped, against the five joined parts in ue-probe/perception-golden | **IDENTICAL**, 102,960 rows, 3.55 s. A run from outside the project fails on production/specs/hook-cast.json, as the study says |
| 267 rule names, 102,960 rows | cut and uniq | Confirmed. 269 first fields, less the 2 header lines. "102,962" in line 6 and the table counts lines, not answers |
| JS fallback, 30 of 30 rows | Re-ran jsharness/harness.mjs on golden.json | Confirmed: 30 of 30 pass. The 30 rows are MotionFactor 12, ConeWeight 10 and LightFactor 8 |
| Andrew Lock sizes | Fetched the cited page | Confirmed: 6.8/2.5/2.0 MB default and 4.3/1.7/1.4 MB invariant; .NET 10 preview 6; 12 August 2025 |
| Issue 129900 quote | Fetched the cited page | The quote is confirmed. The page names the speaker only as user "oroztocil", not as a Microsoft engineer, and shows no dates |
| Allowlist path | ls | ledger-v2/research/license-allowlist.md exists, as the study cites. production/research/license-allowlist.md does not exist |

Not re-checked: the Microsoft Learn AOT page, the Start Debugging page, the Uno page, the Emscripten README, the .NET 11 date (which the study itself says rests on search titles only).

## Fixes (numbered, precise)

1. **Plan step 2 cannot be built as written.** LlmClient.cs is not just a network client. It holds `ILlmClient`, `IStreamingLlmClient`, `IStartingLlmClient`, `LlmRequest`, `LlmResponse`, `LlmMessage`, `Models` and the `LlmStream*` exceptions, and 6 to 8 other Core files use them (BudgetedClient, ClaimCheck, ConversationEngine, Director, IntentRouter, Suggest, TalkLadder, CostTracker). `FastChecker` is a field type in ConversationEngine.cs:207. Removing either file from compilation breaks the build. Rewrite step 2 with one of these two options:
   - (a) Keep both files compiled. The platform analyser only warns, so no Core edit is needed. `Process.Start` and `SocketsHttpHandler` would throw only if called, and the browser front door never constructs `AnthropicClient` or `FastChecker`. Recommended, because it keeps "the Core files directly, never a copy".
   - (b) A Core edit that moves the interfaces and message types out of LlmClient.cs into their own file. This touches the game's code, so it would need the full simulation check suite.
   Re-cost step 2 either way.
2. **Correct the five-line summary, line 1.** "Only two small files would be left out" is wrong (see fix 1), and LlmClient.cs is 25 KB, not small. Suggested wording: "two files hold parts a browser cannot use (starting a helper program, the AI server's network handler); they stay in the build but are never called in the browser."
3. **Threads bullet:** add ConversationEngine.cs:1841 (Task.Run), and note that its result reads are guarded, so nothing blocks.
4. **Change "13 files use CultureInfo.InvariantCulture" to 17.**
5. **Counts:** say 102,960 answers (rows), not 102,962. The 102,962 lines include 2 header lines. Then the table row and the fallback's "102,960 rows" agree.
6. **Issue 129900:** change "a Microsoft engineer says so" to "a commenter (oroztocil) says so; the page as fetched shows no date". Better still, cite Microsoft's own documentation on .NET 10 WebAssembly multithreading, read in full, or mark the threading status unverified.
7. **Speed paragraph:** "one tick of the town is a tiny fraction of that" has no evidence behind it. The golden table runs single rule calls; it never steps a town. Either time one town step natively (SimHarness or CoreTests already step towns; this takes minutes), or mark the claim unmeasured.
8. **Size estimate:** the 1.4 to 2.0 MB baseline is Lock's trimmed hello-world. The Core will also pull in Regex (used in 23 files), Linq, Tasks and HttpClient, and the 0.41 MB figure is the untrimmed library. Either give the range as "about 2 to 4 MB compressed, unmeasured until step 4", or say plainly that Regex and the other framework parts are not in the baseline.
9. **Licences:**
   - (a) The allowlist now names three MIT tools by his pick (FoldCraft, ast-grep, PresentMon, item 12, added 17 November), not two.
   - (b) Note that the project already builds and runs its console checks (CoreTests, PerceptionGolden) on the .NET SDK, so the new decision is narrower: shipping the .NET browser runtime and Emscripten's runtime pieces inside a prototype page.
   - (c) Check Node's licence (MIT, at its source) or drop the row. "Not checked" should not sit in a table he may be asked to approve.
   - (d) With invariant globalisation, ICU is not shipped. Say so, because it shrinks the notice list.
   - (e) PROCESS 2 needs a DECISIONS.md record. List it as a plan step.
10. **Hours:** the steps add up to 13.5 to 25.5 hours, plus 2 for the optional AOT step. Add time for the decision record, the RECIPE.md lines, the fresh review and the re-cost from fix 1, and state the total as a range including them. Under the current CLAUDE.md (a weekly budget, items only through the Monday order), add one line saying the work goes on the order's waiting list rather than into the running week.
11. **The page ask:** the recommendation bundles a licence decision with a network setting. Under the current rules these are two different asks: a licence outside the list, and his sign-in or hands. Give each its own line with an exact action and link. The GitHub-runner route needs neither network change, so offer it as the recommended way to avoid the network setting.
12. **Fallback detail needed before anyone builds it:**
    - (a) State how a row's expected value is classed as a number or as text. The table uses formatted doubles from `D()` and bits from `Bit()`, and a bit column must not be compared as a number by accident.
    - (b) Rules whose rows depend on casting data (for example CastPlaceOf, 8,568 rows) need production/specs/*.json in the JavaScript too. Say how it is loaded and that it must be the same version the table was made from.
    - (c) The harness hard-codes Walk, Run, Fov and Acuity by hand. Export the constants with the rows, or check them from rows, so they cannot drift.
    - (d) Golden rows check single rules, not the order in which a town steps. Say that a JavaScript town loop has no check beyond per-rule rows. That is a second reason the fallback is the weaker route.
    - (e) Move the export script and harness.mjs out of the scratch folder into a lasting place (research folder or tools) and name it. The scratch folder can be wiped, and right now the "demonstrated today" proof lives only there.

## What is sound

The method is right (measure first, a golden-table proof, stop after two network refusals, unreached sources listed). The equivalence result is real and reproducible. The scan's main safety claim (no reflection, so trimming is low risk) holds. The size sources are quoted accurately. The recommendation (one simulation, proved against the same table, with the fallback started meanwhile) follows from the evidence.
