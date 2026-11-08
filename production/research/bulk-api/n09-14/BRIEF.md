# n09-14: backstories and side-story outlines on the month's credit (prepared 8 November 2026, nothing sent)

**The requests (REQUESTS.jsonl, 35, built by build_requests.py from the sources):** three backstories, Ron Kirby, Sheila Dunn and Darren Milner, 600 to 900 words each, third person, every new fact marked [invented], closing with INVENTIONS and GAPS lists; and 32 side-story outlines, one for each story in game-design/side-stories-2026-11-08.md (as fixed after REVIEW-2026-11-08.md), 150 to 250 words under study 16's job-template headings, keeping each story's people, endings and what the town keeps.

**Sources (quoted, not retyped):** canon.md (Game, Era, Tone, Premise and cast, the content rule, What LEDGER is not); the story outline of 28 September; RULINGS.md's story section; the outfit's decision of 29 September; each person's card, casting sheet, the talk's fact list (the claim bench's 3 November requests) and their routine (production/specs/hook-cast.json); the side stories' rules, the regulars' roster and study 16's template. The system prompt states 1990, the content rule, no real names, and that canon's open questions stay open.

**Model: Sonnet 5.5.** The plan's runs: Haiku 5.5 fell one short of the bar on the claim labels (114 of 127, CLAIM-LABELS-SPEC-2026-11-03.md), so it is not trusted with canon-bound writing; Sonnet 5.5's harm-sort misses came mostly from not knowing the year (HARM-READER-2026-11-03.md), now stated. No writing trial exists, so this choice is unverified.

**Dry run (8 Nov):** worst case US$0.66 as a batch (US$1.32 unbatched); today's ceiling US$47.59, none spent; about US$190 of the US$200 left, four days to go. A review pass (about US$1.5 on Opus) fits easily. This text alone cannot use up the credit.

**To send:**

    python tools/api_batch.py --run production/research/bulk-api/n09-14/REQUESTS.jsonl production/research/bulk-api/n09-14/ANSWERS.jsonl --what "n09-14: three backstories and 32 side-story outlines (Sonnet 5.5)" --batch
