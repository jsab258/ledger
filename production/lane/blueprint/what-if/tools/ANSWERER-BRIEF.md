# Brief for a blueprint answerer (what-if sweep, 24 Nov 2026)

You check whether a game's design blueprint answers specific player questions. The game: LEDGER, a 1990 British port-town crime game; the player is Frank Nowak, who inherited a minicab office (Mickey's) in the Hook, Meridian.

Blueprint: /home/claude/ledger/production/lane/blueprint/ : the chapters BLUEPRINT-01-hands.md to BLUEPRINT-10-shipping.md, BLUEPRINT.md, BLUEPRINT-11-conflicts-and-gaps.md (known conflicts and gaps: check it, a question listed there as a gap is "unanswered" or "weak"), data/ (JSON: police.json, tune.json, people/, cast.json, happenings.json, jobs/ and others), economy/, temper/. Do NOT read ai-brain/, reality-check/, prior-research/, checklist-check/, data-sweep/ or what-if/ (except your batch file). Authority over the blueprint: /tmp/claude-0/-home-claude/04b65caa-e826-5b3f-aded-6e3222356bc6/scratchpad/canon.md and RULINGS.md (read both first, quickly).

Method: for each question, search the blueprint with grep (several keywords, synonyms: e.g. "constable", "officer", "police"; "knife", "stab"; "body", "dock"), read the parts that match, and judge.

Verdicts (exactly one):
- WELL: the blueprint gives a specific, consistent answer a builder could implement and a tester could check, and it is plausible for 1990 Britain, inside canon and fun.
- WEAK: an answer exists but is vague, contradictory between parts, implausible for 1990 Britain, against canon or a ruling, leads to an absurd outcome or a dead end, or is listed as a gap in part. Say exactly what is weak.
- UNANSWERED: nothing in the blueprint covers it (say what you searched for).

Output: write a JSON Lines file (one JSON object per line) at the path given in your task, with keys:
"id", "answer" (the blueprint's answer in at most 45 words, plain words; empty if unanswered), "parts" (the part ids cited, e.g. "2.6.4; RT2-02; C-043"), "verdict" (WELL, WEAK or UNANSWERED), "why" (at most 35 words: for WEAK or UNANSWERED what is wrong or missing; for WELL why it holds), "harm" (if a player hits the gap: one of crash, dead end, absurd, immersion, minor, none), "likely" (how likely a player tries it in the first 3 hours: 1 rare to 5 almost everyone).

Be strict: an answer that only implies the outcome, or that a careful designer would call incomplete (missing what happens next, missing who notices, missing the case where nobody saw), is WEAK. Do not invent answers. British spelling, plain words, no em-dashes. Your final reply: one line with counts by verdict and the file path.
