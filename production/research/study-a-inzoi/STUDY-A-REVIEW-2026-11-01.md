# Review of Study A (inZOI): 1 November 2026

A fresh reviewer, working only from public pages read in full on 1 November 2026 and the project's own records. Nothing was installed, clicked or signed into.

**Verdict: PASS WITH FIXES.** The facts about inZOI, NVIDIA's kit and PUBG Ally are right almost throughout: 59 claims checked, 1 wrong, 3 unsupported. But the section on what this means for LEDGER leaves out the project's own speech bar and its own measurements on this card. Fix 1 below must be made before the study steers a speech decision.

## 1. Claims checked against their sources

20 sources were re-read: [1] [2] [3] [4] [5] (the post and its table picture) [6] [7] [8] [9] [10] [11] [12] [13] [14] [17] [19] [23] (all three parts of the paper's text) [24] [25] [26] [27] [28].

| # | Claim in the study | Source | Mark |
|---|---|---|---|
| 1 | Smart Zoi is a ".5B billion parameter Mistral NeMo Minitron" | [1] | CONFIRMED (the source's own garbled words; 0.5B is a fair reading) |
| 2 | "GPU-accelerated exclusively on GeForce RTX GPUs" | [1] | CONFIRMED |
| 3 | Early access 28 March 2025; "experimental"; switched on by the player | [1][5] | CONFIRMED |
| 4 | End-of-day schedule change; inner thoughts shown live | [1][13] | CONFIRMED |
| 5 | NVIDIA's Minitron sizes are 2B, 4B, 8B | [2][3] | CONFIRMED |
| 6 | NVIGI takes the game's D3D12 device and queue ("compute in graphics") | [2] | CONFIRMED |
| 7 | Dead Meat runs Minitron-8B-128K on RTX 50-series; no speed given | [3] | CONFIRMED |
| 8 | ACE design adds retrieval memory and "reflection" | [3] | CONFIRMED |
| 9 | NVIDIA supplied the model to avoid frame drops; Krafton fine-tuned it on its own dataset and wrote the inference code; NVIDIA optimised for CUDA | [4] | CONFIRMED |
| 10 | Tier table: RTX 3060 8 GB / 12 GB RAM; RTX 4060 8 GB; RTX 5070 or 4070 Super 12 GB; RTX 5070 Ti or 4080 Super 16 GB / 32 GB RAM | [5] table picture | CONFIRMED |
| 11 | "Internet connection required" on every tier | [5] table picture | CONFIRMED |
| 12 | Only NVIDIA graphics cards named | [5] table picture | CONFIRMED (the processor row also lists AMD Ryzen) |
| 13 | Up to five sleepy Zois after 11 p.m. "may cause lag" | [5] | CONFIRMED |
| 14 | Zoi Pen English only at launch | [5] | CONFIRMED |
| 15 | RX 6650 XT stutter, August 2025 | [6] | CONFIRMED |
| 16 | RX 9070 crashes that came and went with drivers | [7] | CONFIRMED |
| 17 | RX 9060 XT crashes, 2026 | [8] | CONFIRMED |
| 18 | "Reportedly a limit of one Smart Zoi" | [8] | UNSUPPORTED. The player wrote "I had set it to only One Zoi": a setting the player chose, not a limit in the game. |
| 19 | v0.8.0, 29 April 2026: a notice at "7GB or less VRAM"; Unreal 5.6; Performance Safeguard | [9] | CONFIRMED |
| 20 | 12.1 GB peak at 4K, maximum settings, frame generation; "up to 10 GB" without Smart Zoi; "2-4 GB" stated, not measured | [10] | CONFIRMED |
| 21 | inZOI alone about 5,004 MiB on a 10 GB RTX 3080 (Linux); Smart Zoi switched itself off | [11] | CONFIRMED |
| 22 | Players: mostly thought bubbles, actions little changed, lower settings needed, "vendor locked" | [12] | CONFIRMED |
| 23 | "Every action sequence is made by language model inference"; "Planning is also done by language model inferences" (Kang-Wook Lee) | [13] | CONFIRMED |
| 24 | v0.10.0, 3 September 2026: location, group activity, social event, job or business used "to decide its interactions"; a symbol marks them | [14] | CONFIRMED |
| 25 | NVIGI hints: prioritise graphics, prioritise compute, balance (the default) | [17] | CONFIRMED |
| 26 | Driver 575.00 or 580.88; "Vulkan compute: not optimized" | [17] | CONFIRMED (575.00 is CUDA with D3D12; 580.88 is CUDA with Vulkan, or D3D compute) |
| 27 | Run across many frames; targets in "hundreds of milliseconds"; measure by switching the feature off and on | [17] | CONFIRMED |
| 28 | v0.5.2 "Rolled back SmartZoi feature to October version for stable service" | [19] | CONFIRMED |
| 29 | v0.5.2 dated 30 December 2025 | [19] | WRONG: posted 29 December 2025, 06:01 UTC (Steam news feed, read 1 Nov 2026: https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2456740&count=4&maxlength=0&enddate=1767225600&feeds=steam_community_announcements) |
| 30 | PUBG Ally models: Mistral-NeMo-Minitron-2B, kanana-1.5-2.1b, Qwen3-1.7B | [23] Table 3 | CONFIRMED |
| 31 | 4-bit | [23] Table 9 | CONFIRMED |
| 32 | GGUF, through NVIGI | [23] Appendix G | CONFIRMED |
| 33 | 1.6 to 2.1 GB including the key-value cache | [23] Section 7.3, Table 9 | CONFIRMED |
| 34 | Aimed at cards with at least 8 GB | [23] Section 2.2; [24] | CONFIRMED |
| 35 | Measured on RTX 4060-class cards | [23] Table 8 | CONFIRMED |
| 36 | Recognition 0.12 s, on the processor | [23] Table 8, Appendix H | CONFIRMED |
| 37 | Model 0.80 s median, 0.91 s at p90 | [23] Table 8, Section 7.3 | CONFIRMED |
| 38 | Speech 0.70 s | [23] Table 8 | CONFIRMED |
| 39 | Whole reply about 1.6 s against 3.4 s in the cloud; the cloud model's step 2.54 s | [23] Table 8 (1.62 s, 3.36 s) | CONFIRMED |
| 40 | One inference at a time | [23] Section 2.2 | CONFIRMED |
| 41 | About 5,000 tokens of context | [23] Section 3.2 | CONFIRMED |
| 42 | 90.7% prompt-prefix cache reuse | [23] Section 7.3 | CONFIRMED (±3.7 points) |
| 43 | 16 tools; an availability check before actions | [23] Table 1, Section 3.2 | CONFIRMED ("a bounded set of tools"; the word "fixed" is the study's) |
| 44 | Live tool results as "the only ground truth" | [23] | UNSUPPORTED. The phrase is not in any of the paper's three parts. The only "ground-truth" is Section 6, on scoring teammate quality. The nearest is Appendix J's grading rule: claims "must rest on tool results or observed events". Drop the quotation marks or quote Appendix J. |
| 45 | Distilled from a 31B teacher "given fixed rules" | [23] Sections 4.1, 4.2, 5.2 | UNSUPPORTED as worded. The teacher is Gemma 4 31B, passing through 8B intermediate teachers (Table 3). Its prompt was tuned with GEPA, and a safety list sat in its system prompt. The paper never calls these fixed rules. |
| 46 | A keyword filter before speech | [23] Section 5.3 | CONFIRMED |
| 47 | Grounding 0.932 against the teacher's 0.944 | [23] Section 7.1 | CONFIRMED (the "Fact" score from model judges) |
| 48 | NVIDIA blog: a 2B Minitron, quantised, runs on 8 GB cards | [24] | CONFIRMED (no timings or memory figures in the blog) |
| 49 | Total War: PHARAOH: "up to 6 GB"; over 1,200 tables; text only; cloud on Radeon if the developer chooses; experimental, January 2026 | [25] | CONFIRMED |
| 50 | NVIGI D3D12 and Vulkan plugins: "general GPU architectures/vendors"; "experimental and not intended for production use" | [26] | CONFIRMED, but this is the 1.2.0 entry. The 1.7.0 notes do not restate the status, so "shipped" should say "at 1.2.0". |
| 51 | Core tests "do not support AMD hardware" | [26] | CONFIRMED in substance (1.5.0 entry; the source says "does not") |
| 52 | Newer ACE models listed as multi-vendor GGUF | [27] | CONFIRMED, but the listed on-device models are 4B to 9B. The smallest is a 4 GB quantised build (Nemotron 3.5 Bolt E4B), which leaves no room in about 4 GB free. Say so. |
| 53 | ACE Unreal plugins cover 5.5 to 5.7, not 5.8 | [27] | CONFIRMED |
| 54 | 83.88 tokens a second, 7B 4-bit, RX 6700 XT | [28] | CONFIRMED: Llama 2 7B Q4_0, generation (tg128), flash attention off. Reading the prompt runs at 1,051 tokens a second, which matters more for a checker that reads a fact list. |
| 55 | The plain RX 6700 is not listed | [28] | CONFIRMED |
| 56 | inZOI warns at 7 GB (repeat of 19, in the AMD line) | [9] | CONFIRMED |
| 57 | Krafton's interview date, 5 June 2025 | [4] | CONFIRMED (the interview itself took place 27 May) |
| 58 | LEDGER's check: 1.1 s, or 2.3 to 2.8 s with a second look | production/research/voice-latency/CHECK-TIME-2026-10-27.md | CONFIRMED, but the study gives no link |
| 59 | About 4 GB free on the card | production/research/frame-headroom/FINDINGS-2026-10-23.md (the game alone peaks at 5.6 GB, with Pocket on the processor) | CONFIRMED only with the voice on the processor. No link in the study. |

Not re-checked: [15] [16] [18] [20] [21] [22] (the version notes for 0.4.0, 0.5.0, 0.6.0, 0.9.1 and 0.10.1, and the October letters).

## 2. Facts or inferences without support

- Claims 18, 44 and 45 above.
- Source [7] also says Smart Zoi worked on an RX 9070 under Linux and with an older Windows driver. So in practice it is not tied to CUDA, despite NVIDIA's "exclusively" in [1]. Whether it runs on the card or on the processor on AMD is unknown. This bears directly on question 8 and should be added, marked unverified.
- Elsewhere the study keeps "(inference)" and "Unverified" honest. The LEDGER section is labelled as inference as a whole, which is acceptable.

## 3. The LEDGER conclusions

**Fix 1 (blocking): measure against the project's own bar and its own records.** The study does not mention any of the following:

- **His bar for a local checker (his answer of 26 October).** It must run in 0.15 s or less beside the running game, with no frame stalls, and let through no more invented details than Haiku (1 in 42). Source: production/orders/2026-11-02.md, item o26-speech-checker. Against that bar, "a local check under a second is plausible" is the wrong test. PUBG Ally's 0.80 s on an NVIDIA card with CUDA is more than five times over it.
- **A fast local checker is already in the game.** It is a 17M model, on by default since 28 October, at 0.05 s beside the game with no frame stall (o27-checker-open). With Pocket, it brought 11 of 20 turns under 2.0 s (production/research/voice-latency/REMEASURE-2026-11-01.md). Any 2B model would replace or back up the Haiku second step, not "the cloud check" in general.
- **Small general models were already reviewed.** That review covered Qwen3-0.6B (0.8 to 2.1 s on the processor) and Granite Guardian 2B. Its finding: 0.15 s is reachable only on the card, and sharing the card with a game has no published measurement (production/research/invented-claims/LOCAL-CHECKERS-2026-10-26.md). On 26 October, five untrained checkers were also measured, and none passed.
- **The frame cost on this exact card was measured on 25 October.** With the cast voice running on the RX 6700, another process's AI work held the card for up to 487 ms of a 504 ms frame, and the card's memory peaked at 9.5 to 10.1 GB of 10. Two tries cut the worst frame only to 118 ms (production/research/frame-headroom/VOICE-ON-CARD-TRACE-2026-10-25.md). That is the strongest evidence on the main risk, and the study lists the risk as if untested.

Rewrite the "Best use" and "Needs" lines with these in view. The trial may still be worth running, but only as a replacement for Haiku's second look, judged against the 0.15 s bar or an explicitly different one, and only with the stall result above taken into account.

**Fix 2: name the AMD routes and their status.**

- ROCm/HIP on Windows: the RX 6700 (gfx1031) is marked unsupported for both the Runtime and the HIP SDK. Source: AMD HIP SDK 7.2.0 requirements, page dated 31 July 2026, read 1 November 2026, https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html. So llama.cpp's HIP build has no official support here. Vulkan stays the plain path, as the study says.
- DirectML and ONNX Runtime: Microsoft says DirectML "is in sustained engineering", and new work has moved to Windows ML (Microsoft Learn, updated 9 January 2026, read 1 November 2026, https://learn.microsoft.com/en-us/windows/ai/directml/dml). NVIGI itself lists an "ONNX DirectML GPT" plugin for "ONNX-supported GPU or CPU" [2]. This vendor-neutral route is missing from the study.
- Queue priority on AMD (D3D12 queue priority, Vulkan global priority) was not researched. List it as an open question, not as "no priority control".

## 4. Writing, links, dates

- Plain and short. Every outside number has a source tag, and the whole list carries one read date, which is acceptable.
- Add links for the LEDGER numbers (claims 58 and 59) and for "Pocket on the processor" (production/specs/voice-engines.json).
- Source [9]'s link now redirects to a Steam page that shows no notes. Give the Steam news-feed address as the readable copy, as [5] does.
- Correct the v0.5.2 date (claim 29).
