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
| LEDGER's own files | production/research/voice-off-card/CLOUD-VOICE-2026-10-07.md (the real-path timings); production/research/invented-claims/CHECK-FLOOR-PROPOSAL-2026-10-07.md (his words of 7 October); production/audits/review-2026-10-01/FAULTS.md, D1 (the twelve mutations); ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp (the notice flag; the "ready pose" comment); tools/catalogue.py |

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

1. **HE, section 0 and section 1.** "About 1.0 to 1.4 s with a streaming cloud voice" assumed Sonnet reaches the first full sentence in 0.8–1.0 s. LEDGER measured 1.35 s median for one model on 7 October, and the faster first sentence stays off by his ruling. With a 0.1 s local check and a 0.2 s cloud voice, first sound is about 1.65 s (2-FIT-TO-LEDGER.md).
2. **HG, section 3.** "$0.50 to $1.00 an hour" is an estimate from an assumed conversation shape. LEDGER's measured figures ($0.026 a reply; about $0.57 an hour at the pace played, $2.30 heavy) are used instead.
3. **HD, section B1.** The idle the builder rejected was described by the builder in a code comment, not by Jafar (4-FIVE-PROOFS.md, idea 2).
4. **All notes.** Product names from OpenAI and Google ("GPT-6 Astra", "GPT-6.1 Sol", "Gemini 3.8") stay unverified except where Anthropic's own page prints them, which was checked here for GPT-6 Astra and GPT-5.6 Sol.
