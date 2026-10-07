# Sources

## What could be reached (7 October 2026)

**Reachable:**
- the arXiv API (export.arxiv.org, abstracts and PDFs);
- GitHub's public pages, READMEs and licence files;
- Wikipedia (rate-limited part of the time);
- Epic's documentation (dev.epicgames.com);
- Anthropic's pages (anthropic.com, platform.claude.com, code.claude.com, support.claude.com).

**Refused** (so UNREACHED, and used as evidence for nothing):
- openai.com and its developer and community sites;
- Google's AI, DeepMind and Vertex sites;
- huggingface.co, so no model card or licence page;
- nvidia.com and NVIDIA's project and NGC pages;
- unrealengine.com, so no EULA, and fab.com, so no "Allows usage with AI" flag could be read;
- Reddit, YouTube, X, Hacker News;
- the games and hardware press;
- artificialanalysis.ai;
- every legislation and court site;
- Steamworks;
- law firms' pages.

Search summaries [SS] are leads only.

## Checked by this session itself

| Source | What was confirmed |
|---|---|
| https://www.anthropic.com/legal/consumer-terms | "To develop any products or services that compete with our Services, including to develop or train any artificial intelligence or machine learning algorithms or models or resell the Services." Effective 8 October 2025. |
| https://www.anthropic.com/claude-opus-5-5 | Published 22 September 2026. The benchmark tables name "GPT-6 Astra" and "GPT-5.6 Sol". The one game sentence is quoted in 1.1. |
| https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-mcp-in-unreal-editor | An MCP server inside the editor, Experimental; 127.0.0.1:8000/mcp; "no authentication layer"; clients Claude Code, Cursor, VS Code, Gemini, Codex; "Cooked and shipping game builds can host an MCP server by calling `IModelContextProtocolModule::StartServer()`". |
| https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine | "capture body, or both body and face performance from a single camera"; Experimental, from UE 5.8; processed "locally on your machine"; installed from Fab; Windows only. |
| https://raw.githubusercontent.com/KRLabsOrg/LettuceDetect/main/LICENSE | MIT |
| https://github.com/nv-tlabs/kimodo (README) | Apache-2.0 code. SOMA-RP weights trained on Bones Rigplay 1, "a large-scale (700 hours) commercially-friendly optical motion capture dataset". The model list includes an SMPL-X version. |
| arXiv API, by identifier | 2609.31588 RePlay (25 Sep); 2609.00581 Enoki (1 Sep); 2609.23142 CraftBench-UE (19 Sep); 2609.40325 WorldAuditBench (30 Sep); 2609.36777 Code4Scene (29 Sep); 2610.07641 speculative execution for voice agents (6 Oct); 2609.05370 "When LLM Decompilers Recompile More and Preserve Less" (4 Sep) |
| RePlay, full paper (after the check) | Disney Research; plays only pre-recorded lines; 383 ms median; Cascade A (2.6 s) "excluded" from the user study; against Cascade C, n = 8, 63% against 12% (p = 0.008), rated on wait time, pace, back-and-forth and responsiveness; against Cascade B, n = 6, 46% against 21% (p = 0.50) |
| Enoki, full paper (after the check) | Encoder 69.1% F1 at 0.13 s; the slow LLM version 76.4%; Claimify 11.95 s a sentence; Table 10 is "relative comparison across methods, rather than ... exact hardware-level accounting" |
| WorldAuditBench abstract (after the check) | Agents explore UE5 and Three.js worlds "under a fixed exploration budget"; 213 anomaly tasks; 6.6–42.3% against people's 83.4% |
| Kimodo README (after the check) | About 17 GB of video memory on the card, less with the text encoder on the processor; "most extensively tested on GeForce RTX 3090, GeForce RTX 4090, and NVIDIA A100 GPUs" |
| LEDGER's own files, first version | production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md (the real-path timings); production/research/invented-claims/CHECK-FLOOR-PROPOSAL-2026-10-07.md (his words of 7 October); production/audits/review-2026-10-01/FAULTS.md, D1 (one-line breaks at twelve lines); ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp (the notice flag; the "ready pose" comment); tools/catalogue.py |
| LEDGER's own files, read after the independent check | RULINGS.md in full; DECISIONS.md, 30 September (lines 156, 163, 165, 168–170: planning first measured; the voice inside the game), 3 October (250–257: licences, NoAI, the nightly report, the key) and 7 October (330–340: the voice and the check study); production/research/terms-2026-10-03/NOTE.md (Unreal 6(e), Adobe 17(C), Anthropic's commercial terms B and D.4); ledger-v2/research/license-allowlist.md (entries 2 and 3); production/research/markerless-mocap/DELIVERY.md; production/research/sit-and-turn/METHOD-2026-10-06.md; production/research/natural-idles/NOTE.md; production/research/asset-plan/1-BUILDINGS-AND-INTERIORS.md (PCG); production/research/blender-mcp; tools/nightly_walk.py and production/playtest/nightly/2026-10-04 to 07 (the record; no pictures); ledger/PerceptionGolden/GossipFuzz.cs (12,000 worlds, 37 planted faults); ledger/Assets/Scripts/Core/ClaimCheck.cs (the player's words not sent, 25 September); canon.md ("No real people, voices, logos, lyrics, car models"); a search for "lyric" in the talk program, the content rules and the casting folder (none) |
| LEDGER's own files, read after the second check | production/audits/sweep-2026-10-05/port-vs-core.md (651,000 scripts; 30 planted breaks; D1 re-tested); tools/ai-tester/play.py (step-NNN.jpg; the window's own pixels); ledger/Assets/Scripts/Core/RealWorld.cs ("a band or singer") and ConversationEngine.cs (the writer is claude-sonnet-5); ledger/ClaimBench/Program.cs (the small-talk set); production/playtest/talk-runs.jsonl (7 October: $0.1324 for five replies, Sonnet 23,339 tokens in, 264 out); production/research/ui-design/BRANDING.md (the name); production/research/prompt-caching/NOTE-2026-09-29.md (Sonnet 5.5's 512-token minimum; Haiku 5.5 promised); production/research/aaa-street/1-PIPELINE.md (Epic's MCP left open); production/research/pre-production/6-RISKS.md (W3); tools/frame-drift.py |

## The helper notes (notes/)

Seven read-only helpers each took one strand for about thirty minutes, given the problem and not a theory (notes/METHOD-BRIEF.md). Their full source lists are in their notes:

| Note | Strand |
|---|---|
| HA-decompile-mod-mashup.md | Decompiling, modding, mashups, one-person agent game-building |
| HB-engine-agents-playtest.md | Agents in Unreal and Blender; agents that judge frames; agents that play and test |
| HC-worlds-3d-garments.md | World models, generated 3D, materials, garments |
| HD-motion.md | Motion from video and text; retargeting; faces from audio |
| HE-speech-small-models.md | Speech-to-speech, streaming voices, small checkers, grounding, shipped LLM games |
| HF-legal.md | Reverse engineering, using what is learned, AI law, mashups |
| HG-models-workflow.md | The frontier models; directing agents; judging images; small local models |

### Corrections to the helper notes

1. **HE, section 0 and section 1.** "About 1.0 to 1.4 s with a streaming cloud voice" assumed Sonnet reaches the first full sentence in 0.8–1.0 s. LEDGER measured 1.35 s median for one model on 7 October, and the faster first sentence stays off by his ruling. A cloud voice is itself ruled out (7 October), so the figure does not apply.
2. **HG, section 3.** "$0.50 to $1.00 an hour" is an estimate from an assumed conversation shape. LEDGER's measured $0.026 a reply with one model gives about $0.39 an hour at the pace played and $1.56 heavy; those are used instead.
3. **HD, section B1.** The idle the builder rejected was described by the builder in a code comment, not by Jafar (4-FIVE-PROOFS.md, idea 2).
4. **All notes.** Product names from OpenAI and Google ("GPT-6 Astra", "GPT-6.1 Sol", "Gemini 3.8") stay unverified except where Anthropic's own page prints them, which was checked here for GPT-6 Astra and GPT-5.6 Sol.
5. **HE, RePlay and Enoki.** RePlay picks only pre-recorded lines (no generated glue), and its 63% preference was against a small-model cascade, not the 2.6 s one. Enoki's 0.13 s version is less exact (69.1% against 76.4%), and "against 11.95 s" was the slowest of several comparisons. Both corrected in 1-WHAT-IS-NEW.md and 2-FIT-TO-LEDGER.md.
6. **HE and HG, the first sentence.** "Name the facts, then check" is LEDGER's plan-first mode, built and measured on 30 September with no gain. With today's voice, the voice and not the check sets the first sound.
7. **HD, motion.** His rulings of 3 and 7 October name MetaHuman's clips and Mixamo; the 6 October method exists. Kimodo is from March–April and was tested mainly on NVIDIA cards.
8. **HB, the tester reading memory through MCP.** The game's own session record already gives it.
9. **HC, TRELLIS.2.** LEDGER's allowlist lists TRELLIS 2 as MIT; the note's finding on nvdiffrast and Objaverse is a question for that entry, not a settled exclusion.
10. **All notes, the Unreal licence.** Called unreached; LEDGER's own terms note holds its clause 6(e), read from his PC on 3 October.

## The independent check (7 October)

A fresh reviewer, who had not seen the work being made, was given the folder, CLAUDE.md and the brief, and told to break it. It reached every source in its spot-check list and found them matching on the consumer terms, the usage policy, Epic's MCP and markerless pages, Kimodo's README, the arXiv abstracts, Epic's Claude Code plugin licence (MIT), the latency sums, the notice flag and the "ready pose" comment. It found nothing recommending copying another game.

What it found, and what changed:

| Finding | Change |
|---|---|
| The first version contradicted his 7 October ruling: it treated a cloud voice as open, though he ruled "no cloud voice", and called a faster local voice "his call" | Problem 1 rewritten under his rulings; the check moved to "only if a ruling changes" |
| "Name the facts first" was presented as new; it was built and measured on 30 September (no gain, about 0.25 s slower) | Said so; out of the five |
| The Unreal licence was called unreached, though LEDGER holds it (6(e)); the planted-fault test as written would test an AI with MetaHuman frames; Mixamo's terms bar the same | Proof 1 now uses frames with no people; the licence quoted from the terms note |
| The motion proof ignored his rulings on MetaHuman and Mixamo clips and the 6 October method; Kimodo is not new and was tested mainly on NVIDIA cards | Out of the five, into "only if a ruling changes" |
| RePlay and Enoki were misreported | Corrected from the papers |
| The tester proof ignored the game's own session record and his "played as a player would" | Out; replaced by pictures for the walk's eyes (proof 2) |
| The planted-fault cost was understated (0.3 million tokens; about 0.7 million) | Corrected |
| WorldAuditBench measures agents exploring, not judges of still frames | Restated, and used for the walk |
| Legal points stated too firmly: observe-study-test ignored; *Sega* ignored; marks missing on the AI Act and on the filter clause | 3-LEGAL.md corrected |
| Conclusions from unreached sources ("no shipped game", "stricter than what has shipped") | Removed or marked |
| "12 one-line faults" (eleven items, twelve lines); "$0.026 a reply, so $0.57 an hour" (the $0.57 includes the faster first sentence and a cloud voice) | Corrected: eleven at twelve lines; $0.39 an hour with one model |
| The summary used jargon, raised questions his rulings settle and gave items without a recommendation; "attacks the floor itself" | Summary rewritten |
| TRELLIS 2, Meshy and Tripo ruled out against the allowlist without saying so | Said so; the entry is his to re-read |

Not changed: the reviewer's point that writing a training script with Claude Code would itself be "using the Services" is noted beside the check (4-FIVE-PROOFS.md, "Only if a ruling changes"); it is not settled here.

## The second independent check (7 October)

A second fresh reviewer checked the revised proofs against RULINGS.md, DECISIONS.md, the allowlist, the terms note and the code. It found no proof in outright breach of a ruling, nothing recommending copying another game, and no conclusion from an unreached source. It confirmed the 7 October timings, the $0.026 a reply (talk-runs.jsonl, $0.1324 for five), the GossipFuzz figures, and that nobody in the repository has tried Unreal's editor MCP server.

What it found, and what changed:

| Finding | Change |
|---|---|
| Proof 2's premise was false. The walk does save pictures, as step-NNN.jpg (tools/ai-tester/play.py); the nightly report's eyes look only for .png (tools/nightly_walk.py). The tester already takes the window's own pixels, with a fallback for black frames. | Proof 2 dropped; the mismatch reported as a fault found on the way (4-FIVE-PROOFS.md) |
| Proof 3 ignored the port audit of 5 October (production/audits/sweep-2026-10-05/port-vs-core.md): 651,000 random scripts through both languages, 30 planted breaks, 11 uncaught, and eight of D1's twelve lines still passing. Its own re-run on 7 October: nine of twelve pass. Also, one reviewer wrote both versions of GossipFuzz, and "eleven" did not match D1's twelve lines. | Proof 3 dropped; the open lines reported as a fault found on the way, citing the audit |
| "Choosing the facts first gave no gain" mislabelled 30 September. Choosing them by code is today's method (36 to a mean of 21.7); it was the model planning first that gained nothing. | Corrected in all three files |
| Proof 4 searched only for "lyric". The talk's real-names rule already forbids naming "a band or singer" (RealWorld.cs), and ClaimBench's small-talk set asks about music. Only quotations are new. | Proof 4 narrowed to quotations |
| The catalogue check fails on this folder | Not fixable from this branch (CATALOGUE.md is outside the folder); named in the pull request |
| "What needs him" asked for choices on faults in work he has already ruled on, recommended "nothing now" on a matter his ruling parks, and put nothing as multiple choice | Rewritten as three multiple-choice questions, each with a recommendation |
| Proof 1's frame counts disagreed (ten frames, but 75 pictures per model). It measures no faults in people, though people are what he judges most. tools/frame-drift.py was not cited. | 20 planted and 5 clean frames; the people limit stated; frame-drift cited |
| Proof 5 did one task twice, so the second run learns from the first. The allowlist's decision record for a new tool was missing. | Two comparable tasks, order swapped; the decision record first |
| The licence reading was settled quietly. The allowlist says "test"; his 3 October ruling and the terms note say training clauses. "As the licences require" overstated "[I, the cautious reading]". "Help improve Claude stays off, as he ruled": he said he would switch it off; the setting was never read. | Put to him as question 1; the wording corrected |
| "The voice sets the first sound" contradicts his own words of 7 October without telling him | Said plainly, with why: his words hold for a cloud voice |
| 2-FIT dropped "reportedly" on the Munich case | Restored |

In their place: proof 2, Sonnet 5.5 writing on the real path (the live talk still writes with Sonnet 5, read here), and proof 3, the claim check on its successor before Haiku 4.5 retires (the risk register's W3, which has no proof). A trade-mark search was considered and dropped: production/research/ui-design/BRANDING.md (1 October) already covers it.

