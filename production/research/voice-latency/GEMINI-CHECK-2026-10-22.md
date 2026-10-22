# The talk check on Gemini Flash, 22 October 2026

His order of 21 October, item 8: "The Gemini Flash test once he has put the key in the file you open for it". His key arrived in `F:\LedgerTools\keys\google.txt` on 22 October. It was read only into memory and sent only in the `x-goog-api-key` header; it was never printed, copied or committed.

**What the test is.** The lab's prepared run (lab test 6, `production/lab/talk-check/gemini_check.py`, written 8 October and skipped then for want of the key) checks the talk check's second look (is each DETAIL of a reply stated or implied by what the speaker knows?) on Gemini. It uses the same 127 held-out labelled details, 85 true and 42 invented (`F:/LedgerTools/town-scratch/detail-bench/detail-gold.jsonl`), and the same prompt as Haiku 5.5's run of 7 October, one call per detail, timed from this PC. The check sits on the path to first sound: the first sentence is not spoken until it is checked.

## Results

| model, setting | true details refused | invented details passed | median / slowest tenth / slowest per detail (s) |
|---|---|---|---|
| **Gemini 3.5 Flash-Lite** (no thinking setting sent: it refuses `thinkingBudget 0`) | 15/85 (18%) | 3/42 (7%) | **0.60 / 0.70 / 0.97** |
| Gemini 3.8 Flash, thinking off | 19/82 (23%; 3 unread) | **0/42 (0%)** | 1.82 / 2.92 / 5.24 |
| Haiku 5.5, the split (7 Oct, the game's check now) | 23/85 (27%) | 1/42 (2%) | 0.97 / 1.99 |
| Haiku 5.5, thinking off (7 Oct) | 22/85 (26%) | 6/42 (14%) | 0.70 / 1.01 |

The Haiku rows are from `production/lab/talk-check/REPORT.md` (7 October's run, the same held half and prompt).

**Tokens.**

| model | in | out |
|---|---|---|
| Gemini 3.8 Flash | 271,199 | 2,739 |
| Gemini 3.5 Flash-Lite | 277,774 | 3,286 |

Both are about 2,200 per detail. Gemini's prices are **not verified**: Google's pricing page was not read, and the research's figures for 3.8 Flash conflict (frontier-ai-uses HG). So the cost is not stated.

## What it says

- **Flash-Lite is the faster check and the steadier one.** It is 0.37 s quicker than the game's Haiku check on the median and 1.3 s quicker on the slowest tenth. It refuses fewer true details (18% against 27%), but lets three invented details through where Haiku lets one.
  - Against Haiku with thinking off (the fast setting), Flash-Lite is better on all four numbers.
  - The first-sound saving at the median would be about 0.4 s (an estimate from these per-detail times; not measured end to end).
- **3.8 Flash is the most accurate** (no invented detail passed) but too slow for the path to first sound: 1.8 s median, and its slowest 5.2 s.
- **Not measured.**
  - First sound and the whole answer with Gemini in the game. The talk helper speaks only Anthropic's interface; adding a Gemini client to the game is a change of provider and his to decide. The live talk model is not called in development (his ruling of 29 September).
  - The first-sentence and whole-reply parts of the check (the lab ported the detail check only).
- **The 2-second bar stays until he rules.** Whether to switch the check to Flash-Lite trades three invented details in 42 for 0.4 s at the median. Under the lab's rule (switch only if no less accurate and faster), it does not qualify. That makes it a question for him, not a switch made here.

## Evidence

- `gemini-2026-10-22/`: each detail's verdict and time per model (`gemini_<model>.jsonl`) and the summaries.
- Runner: the lab's script, unchanged, for 3.8 Flash. For Flash-Lite, `tools/voice-live/gemini_check_run.py --no-thinking-config`, which imports the lab's script and drops only the refused setting.
- The models the key reaches were listed by name from Google's model list on 22 October. The newest Flash is 3.8 and the newest stable Flash-Lite is 3.5.
