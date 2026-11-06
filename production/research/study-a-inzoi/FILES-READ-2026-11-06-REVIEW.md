# Review of FILES-READ-2026-11-06.md, 6 November 2026

Method: model folders and the program file read as bytes (not run); the ini, the situation enum and GameOption.json pulled with the project reader. Extracts (about 351 KB) were deleted afterwards.

| Claim | Verdict | Why |
|---|---|---|
| A1 three model sizes, config values, version notes | holds | sizes, "vram" 1024/2048/2048, contexts 4096/8192/8192 match |
| A1 gguf headers (936A llama, 24 blocks, 1152, type 15, ctx 8192, template 1,367 chars with tools; 936B/C qwen35, 752M, 24, 1024, 8/2 heads, type 7, template 162 chars, no tools) | holds | parsed from headers. Vocabulary 248,320 not checked |
| A1 936A older leftover | holds (inferred, marked) | its notes read arco_v1.1.0, no SmartZoi |
| A2 whole ini, 13 settings | holds | every value matches (340 bytes, in the pack, not loose) |
| A2 per-model setting names at 0xecee550 | holds | |
| A3 13 situations | holds | enum has 13 plus Invalid and Max |
| A3 "Call exactly one tool" at 0xf195d11; "Available Tools"; versions; think_tool, compressed_prompt, prompt_mode | holds | |
| A4 tool names; intent_window 240; reason and bubble flags | holds | |
| A4 prefetch settings | holds | all ten values match |
| A4 fallback names | holds | present in program text |
| A5 rules at 0xf1e8980 (labels, one tool, persona kept out of keys, persona after safety) | holds | "one tool" holds only when think_tool is off, which the note's own setting says |
| A5 version-mismatch and failure names | holds | |
| A6 error texts, MCP calls | holds | |
| A7 GameOption values (on/off 0; city 0-2 def 2; viewport 0,2,4 def 2; waiting 4-12 def 8; model None) | holds | |
| A7 row "SmartZoiAutonomy" | fails | no such row; the rows are SmartZoi, RangeInCity, RangeInViewport, WaitingCount, Model and four Caption rows. The note lists "SmartZoiAutonomy" as measured. |
| "Measured" vs inference | mostly holds | no measured item found that is really inference; A1 template remark is marked inferred |
| Unreached list | holds | nothing in it was answered above |
| Quotes | holds, borderline | quotes are short labels. A5 paraphrases the rule list closely and A3 lists the user prompt's section headings in order, near a map of the prompt, though not its text |

Minor: the English file's header tags say Korean (languages ko); the note does not mention it.

Not checked: vocabulary count, the locres claims, the Lua type files other than two, the byte offsets of A3 sizes and the other 258,000 files.
