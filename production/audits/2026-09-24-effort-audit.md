Audited [main at 32f455b](https://github.com/jsab258/ledger/commit/32f455b), unchanged since the attached audit. **The recoverable cost is repeated reporting, document rereading and iteration delays; 35% of commits does not establish 35% wasted effort.**

The earlier 156 “records” include two character-card changes, [d0bfba8c](https://github.com/jsab258/ledger/commit/d0bfba8c) and [347f6133](https://github.com/jsab258/ledger/commit/347f6133). Correcting that leaves **154 records-only commits**. Their file touches overlap:

| File | Commits touching it | Requirement producing the updates |
|---|---:|---|
| FOR-JAFAR.md | 81; 49 alone | [CLAUDE:13–19](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L13-L19): record every owner-facing item before messaging; retain resolutions; repeat the file at closing. |
| NOW.md | 78; 45 alone | [CLAUDE:26–29](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L26-L29): continually update/refill work; [62–65](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L62-L65): clock stamp and closing checkpoint. |
| FINDINGS.md / DECISIONS.md | 23 / 11 | [CLAUDE:61–63](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L61-L63): dated findings, decisions and cheaper-choice notes. |
| ROADMAP.md | 13 | [CLAUDE:36–39](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L36-L39): disposition, evidence and stage completion. |
| Other | 8 file touches | CLAUDE 2; facade sitting log 4; canon 1; old roadmap 1. Owner rulings, measurement instructions or relocation, without a blanket hook requirement. |

**139/154 touch NOW or FOR-JAFAR:** those two rules dominate. **37** change only one or two added/deleted lines; **44** if a replacement counts once; median **seven** diff lines. These are counts from the [audited history](https://github.com/jsab258/ledger/compare/c10749e...32f455b). Neither the rules nor the [stop hook](https://github.com/jsab258/ledger/blob/32f455b/tools/sitting-clock.py#L166-L187) require a separate commit per update. The microscopic commits are an implementation choice. The [commit-message hook](https://github.com/jsab258/ledger/blob/32f455b/.githooks/commit-msg) checks repeated subjects, not record completeness.

For effort, I used author timestamps, capped each preceding gap at `min(10, 1+√changed-lines)` minutes, and split mixed changes using square-root line weights. Binary artifacts receive a fixed weight of ten lines. Boundaries follow [NOW’s sitting stamps](https://github.com/jsab258/ledger/commits/32f455b/NOW.md); early unstamped sittings remain grouped. Percentages describe **attributed active effort**, with research/evidence filling the remainder. Game includes probe code. Build-pending minutes overlap work. Reading estimates use the four files at each window’s first commit, not observed reads.

| Sitting start, Swiss time | Game / records / tools | Build pending, minutes | Full startup read, k tokens |
|---|---:|---:|---:|
| 22 Sep, before 14:30 | 48% / 17% / 18% | 81 | ~2 initially |
| [22 Sep, 14:30](https://github.com/jsab258/ledger/commit/25ad37d5) | 34% / 24% / 15% | 129 | 5 |
| [22 Sep, 20:54](https://github.com/jsab258/ledger/commit/54897884) | 38% / 26% / 9% | 32 | 16 |
| [23 Sep, 07:57](https://github.com/jsab258/ledger/commit/e5c1c0e1) | 54% / 31% / 5% | 276 | 24 |
| [23 Sep, 14:41](https://github.com/jsab258/ledger/commit/0a85e462) | 43% / 30% / 11% | 329 | 29 |
| [23 Sep, 22:31](https://github.com/jsab258/ledger/commit/16eee120) | 33% / 31% / 17% | 302 | 70 |
| [24 Sep, 07:31](https://github.com/jsab258/ledger/commit/3c3defaf) | 2% / 34% / 12% | 14 | 80 |
| [24 Sep, 09:41](https://github.com/jsab258/ledger/commit/3ecbcbd8) | 0% / 23% / 21% | 0 | 86 |
| [24 Sep, 10:02](https://github.com/jsab258/ledger/commit/9bac76d2) | 53% / 11% / 2% | 40 | 86 |

Across the [same history](https://github.com/jsab258/ledger/compare/c10749e...32f455b), model variants suggest **roughly 35–55% game, 17–33% records and 10–15% tools**. Confidence is low: parallel research contaminates sitting boundaries, and a notes-only commit can bank substantial investigation. The model leaves **5–9 hours potentially waiting during pending builds**; it cannot prove inactivity. Another **3–8 hours remain unassigned**, not charged to any activity. The chandler has **40 of 62 elapsed minutes** inside its three round trips ([returns](https://github.com/jsab258/ledger/compare/9bac76d2...32f455b)).

Reading is a separate cost. [NOW](https://github.com/jsab258/ledger/blob/32f455b/NOW.md), [FOR-JAFAR](https://github.com/jsab258/ledger/blob/32f455b/FOR-JAFAR.md), [CLAUDE](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md) and [ROADMAP](https://github.com/jsab258/ledger/blob/32f455b/ROADMAP.md) total **60,910 words, approximately 86,000 input tokens** at four characters/token. One complete read would consume 43% of an illustrative 200,000-token input budget, or 17% of 500,000. **The actual subscription-budget percentage is unknowable from Git:** reading, caching and compaction logs are absent.

My purpose review of 48 tool-related commits distinguishes:

| Kind | Count | Examples and judgment |
|---|---:|---|
| Necessary build/test/evidence repairs | 19 | [Archived bootstrap](https://github.com/jsab258/ledger/commit/59b4007a), [unread crime verdict](https://github.com/jsab258/ledger/commit/f145fe5e), [unrun spec tests](https://github.com/jsab258/ledger/commit/5f93abd7). Preserve the resulting safeguards. |
| New delivery/measurement capabilities, plus their repairs | 8 + 6 | [Facade tools](https://github.com/jsab258/ledger/commit/15cec6b6), [performance check](https://github.com/jsab258/ledger/commit/33bc9b1f), [Gauntlet launcher](https://github.com/jsab258/ledger/commit/cc4186a8), backup and router experiments. New machinery, sometimes justified; not all recoverable. |
| Session/checklist control | 9 | [Stop hook](https://github.com/jsab258/ledger/commit/25ad37d5), [stage checker](https://github.com/jsab258/ledger/commit/246dd390), subsequent repairs/extensions. Administrative machinery. |
| Reference/prompt work | 6 | [Prompt replacement](https://github.com/jsab258/ledger/commit/c46ed517), iterations and [reference routing](https://github.com/jsab258/ledger/commit/91db5c08); neither game tests nor session bureaucracy. |

The hook also changed inside two game-classified commits, [fea0138e](https://github.com/jsab258/ledger/commit/fea0138e) and [30073795](https://github.com/jsab258/ledger/commit/30073795). Category totals conceal that overhead. Worse, [CLAUDE:58](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L58) says stop when outcomes finish, while [62](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L62) blocks stopping until time expires. Both measured sittings rewrote their limits to escape ([f1b233e6](https://github.com/jsab258/ledger/commit/f1b233e6), [32f455ba](https://github.com/jsab258/ledger/commit/32f455ba)).

Replace the cited recording rules with this minimum:

- **NOW:** five current-state lines, ≤150 words; no completed-work history.
- **FOR-JAFAR:** one dated end-of-sitting summary, ≤200 words: changed, evidence, failed/unproven, next, owner decisions. Carry unresolved questions forward. Delete per-message mirroring, verbatim closing dumps, stage counts and resolution reshuffling; Git preserves earlier summaries.
- **DECISIONS:** one entry per material choice: date, decision, reason, authority and implementation link. Routine implementation choices belong in commit messages. **FINDINGS:** only unresolved defects, ≤20 entries; retire the duplicate historical notebook.
- **CLAUDE:** ≤600 words. Remove the stop hook and clock-stamp rules. **ROADMAP:** ≤100 lines of milestone outcomes; archive the exhaustive checklist and retire its completion gate. Read detailed history only when relevant.
- Retain the [Core suites, independent simulation check and Unreal build](https://github.com/jsab258/ledger/blob/32f455b/CLAUDE.md#L53-L57). Batch records with accepted work or the closing checkpoint; iterate locally where possible.

**Planning estimate:** recover 15–20 percentage points of active effort; target **60–70% game production and ≤5% recording**. Confidence: high in counts and file sizes, moderate in rule/tool judgments, low in effort and recovery forecasts. This is a target to measure, not a demonstrated saving.
