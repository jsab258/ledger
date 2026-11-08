# n09-11: where the prompt-cache writes come from, and which loaded tools go unused (2 to 8 November)

Diagnosis only; nothing in the project, its settings or its tools was changed. Written 8 November 2026.

## Sources and method

- Read: every Claude Code session log of this project changed since 1 November (`~/.claude/projects/C--Users-Jafar-ledger-local/*.jsonl` and `<session>/subagents/agent-*.jsonl` with their `.meta.json`), streamed line by line in Python; only record types, counts, sizes, timestamps, model names, tool names and request metadata were read. No prompt or message text was printed or quoted.
- Window: 2 November 00:00 to 9 November 00:00 Swiss time (UTC+1); the logs end on 8 November, evening.
- One step = one assistant message, counted once by its message id (a message logged over several lines is merged), "<synthetic>" messages skipped. 15,653 steps: 8,111 by the main sessions, 7,542 by helpers.
- Dollars are list prices from tools/token_audit.py's table (Opus 5.5: 5-minute write $5/M, 1-hour write $8/M, read $0.20/M; Sonnet 5.5 half that). A measure for comparing work, not his bill. Each write is priced by its own lifetime (the log's `ephemeral_5m` and `ephemeral_1h` split).
- The week: all steps US$1,323.43; cache writes US$338.98 (26%), cache reads US$730.70. Main sessions write with a 1-hour lifetime (request metadata `ttl: 1h`); helpers with the 5-minute default.

### How each write was assigned a cause

A step re-reads, from the cache, the whole prompt of the step before it and writes only what is new. So each step's write was split in two:

- **Rebuild** = the previous step's full prompt minus this step's cache read (when 3,000 tokens or more). This is context that had already been written once and had to be written again. Its cause was taken from what the log shows between the two steps, in this order: a compaction marker; a different model; a gap longer than the cache's lifetime (5 minutes for 5-minute writes, 60 for 1-hour); a change of the request's tool/system shape with a tool-list or MCP delta; a startup-file attachment (CLAUDE.md, MEMORY.md, skills); otherwise "not determined".
- **Growth** = the rest: content written for the first time (the previous step's own output, including its thinking; tool results; pictures; attachments). Split at 20,000 tokens into ordinary and large single additions.
- **Start** = a log's first step (all of its write).

## Question 1: the cache writes by cause

### First, the measure itself is partly wrong

The overview's line 3 (tools/token_measures.py, `measure_day`) for 7 November read "writes US$42.06, of which starts US$10.19; 1 rewrite mid-run US$2.21", leaving about US$29.66 apparently unexplained. Reproduced exactly from the logs, that figure has two faults:

1. **It prices every write at the 1-hour rate** (`cost = cw * p[3]`). Helpers write with the 5-minute lifetime, so their writes are overstated by 60%: 7 November's true write cost is **US$35.28, not US$42.06** (helpers US$11.30, reported US$18.09). tools/token_audit.py's `step_cost` splits the two correctly; token_measures does not use it for this line.
2. **Its categories cover only the main session's first eight steps and its mid-run writes over 30,000 tokens.** Everything else is unnamed: every helper's writes and the main session's ordinary step-by-step growth. On 7 November the unnamed part was US$11.57 of main growth plus US$18.09 (true US$11.30) of helpers. "Starts" also counts steps 2 to 8 (US$4.65 of the US$10.19); the first steps themselves were US$5.55.

So most of the "unexplained" writes are not a fault: they are the normal one-time write of each step's new content, plus helpers, which the line does not name. The one real mid-run rewrite on 7 November (US$2.21) is the "not determined" case below.

### Share of cache-write dollars by cause, 2 to 8 November (US$338.98 = 100%)

| Cause | Count | Tokens written | US$ | Share |
|---|---|---|---|---|
| Ordinary growth (new content under 20k a step) | 15,162 steps | 36.6 M | 215.74 | 63.6% |
| Large single additions (20k tokens or more in one step) | 112 steps | 3.3 M | 20.56 | 6.1% |
| Helper starts | 271 | 8.1 M | 34.99 | 10.3% |
| Main session starts | 108 | 3.9 M | 30.87 | 9.1% |
| Gap past the cache's lifetime | 18 (8 main, 10 helpers) | 3.9 M | 26.07 | 7.7% |
| Compaction | 9 (main) | 0.7 M | 5.59 | 1.6% |
| Client restart with changed request headers | 1 (main, 4 Nov 21:05) | 0.18 M | 1.43 | 0.4% |
| Not determined | 4 (2 main, 2 helpers) | 0.56 M | 3.74 | 1.1% |
| Model switch | 0 | 0 | 0 | 0% |
| Tool list or MCP change mid-session | 0 | 0 | 0 | 0% |
| Startup file changed mid-session | 0 | 0 | 0 | 0% |

Notes on the rows:

- **Growth, what it is made of** (estimated; tokens from characters at 2.6 characters a token, a ratio calibrated on the logs' own first steps, so inferred): main growth 15.6 M tokens = its own previous output with thinking 5.6 M (36%), tool-result text about 6.8 M (43%; Bash 7.1 M characters, Read 5.8 M, Artifact 1.8 M, ArtifactData 1.1 M), pictures 0.57 M (456 pictures), his and queued messages about 1.2 M, about 1.5 M not attributed. Helper growth 24.1 M = own output 7.2 M (30%), tool-result text about 12.4 M (51%; Bash 13.6 M characters, Read 8.9 M, Grep 1.4 M, WebFetch 0.7 M), **pictures about 3.45 M (14%, 3,199 pictures read)**, and **MCP server instructions about 1.1 M (4%)**: every one of the 271 helpers, including the lean custom ones that cannot call any MCP tool, receives the MCP servers' instruction blocks (computer-use, Blender, Claude Docs, Chrome, Google Docs; about 12,000 characters) as a message after its first step.
- **Starts:** a main start reads about 47,000 tokens from the shared cache (system prompt and tool schemas) and writes a mean 35,700 more: the skills list (29,900 characters), CLAUDE.md with MEMORY.md (25,300), MCP instructions (11,800), the deferred-tool list (7,300), the opening prompt (5,300), the helper-type list (4,900), git status (4,200). 108 main starts in seven days (102 from the desktop app, 6 from the command line). Helper starts: **general-purpose helpers start at a median 64,000 tokens** (their full tool set, including the Artifact tool's 36,000-character schema and the built-in browser's 22,000, plus the skills list), against 17,000 to 19,000 for the custom types (final-reviewer, small-reviewer, research-reader, extractor, diagnoser, importer). The 106 general-purpose starts wrote 5.18 M of the 8.11 M helper-start tokens; 63 of them found nothing in the cache.
- **Gaps:** main, 8 events, US$17.23; **US$14.53 of it is one long session (b8fdf2ea)** resumed four times after 2 to 8.4 hours with a context of 0.16 to 0.92 M tokens (06:58 on 2 Nov alone: 876,000 tokens, US$7.01). That session wrote US$55.67 in the week, 16% of all writes, and holds 6 of the 9 compactions. Helpers, 10 events, US$8.84: helpers idle 6 to 14 minutes (waiting on a long command) past their 5-minute lifetime, rewriting 0.14 to 0.31 M tokens each.
- **Client restart (4 Nov 21:05, session 55a4a011):** after a 31-minute pause the request was rebuilt from scratch (`keep 0`), the beta-header list grew from 19 to 20, and a new deferred-tool list was attached; the cache read was 0, including the system prompt. Inferred: the app was restarted or updated, and the changed header set missed the cache. High confidence that the headers changed; medium that this caused the miss.
- **Not determined (4 events, US$3.74):** 7 Nov 22:33, session 61a0bd52 (the overview's "1 rewrite mid-run US$2.21"): 4 minutes after a step that read 320,000 tokens, the next one read only the 46,900-token system prefix. The same pair of requests with queued helper notices occurred at 22:28 without a miss; version, model, shape hash, headers and cache markers were unchanged. The only candidate left is the server dropping the cache entry (prompt caching is best-effort), which the log cannot show. The two helper cases (2 Nov 07:40 and 08:09) look the same. Low confidence on cause.
- **1-hour lifetime for the main session is the right choice.** At 5-minute rates the main sessions' writes would cost US$114.74 instead of US$183.59 (US$68.85 less), but 193 main steps came 5 to 60 minutes after the one before and hit the cache only because of the 1-hour lifetime; at 5 minutes they would have rewritten about 75 M tokens, about US$375.66. For helpers the reverse holds (1-hour writes would add about US$93 to save US$8.84). Estimate, inferred from the logs.

### The top three causes and what would cut each

1. **Growth, 70% (US$236).** Each new token is written once; the lever is fewer new tokens. Helpers' Bash and Read output (22.4 M characters), helpers reading pictures (3,199, about 3.45 M tokens), and long thinking/output. Cuts: narrower reads and filtered command output in helper briefs; pictures sized down or fewer per helper; dropping unused MCP servers removes their instruction blocks from every helper (about 1.1 M tokens a week, see question 2).
2. **Starts, 19% (US$65.86).** Cuts: give helpers a custom type instead of general-purpose where the work allows (about 45,000 fewer start tokens each; estimated US$15 to 20 a week in writes alone, more in reads); fewer main restarts (108 a week); a shorter start: the skills list carries 49 skills never used this week (about 18,900 characters), the MCP instructions and deferred lists carry servers never called.
3. **Gaps past the lifetime, 8% (US$26.07).** Cuts: do not resume a very large session after more than an hour; start a fresh one from the handover instead (one session cost US$14.53 this way); keep helpers off long waits (run long builds or walks from the main session, or in the background with the helper finishing first).

Confidence: high for the totals, the split by lifetime, the measure's two faults (reproduced to the cent) and the gap and compaction events; medium for the growth breakdown (character-based estimates). What would confirm: tools/token_measures.py's line 3 recomputed with `step_cost` and these categories should give 7 November US$35.28, split as above; the client-restart case would be confirmed by the app's update history for 4 November, about 20:05 UTC.

## Question 2: tools loaded but unused

Method: tool calls counted from the assistant messages of 2 to 8 November (main and helpers, one count per tool-use id); tools offered read from the logged request shapes (always-loaded tool schemas, newest per agent type), the deferred-tool lists (names only, loaded on demand with ToolSearch), the MCP-instruction attachments and the MCP failure notices. Sizes are characters in the logs; tokens are estimated (schemas about 3.4 characters a token, messages about 2.6, both calibrated on the logs' first steps; inferred).

Calls by server, the week: built-in tools 21,487 (Bash 9,927, Read 5,390, Grep 1,178, Edit 1,061, PowerShell 927, ArtifactData 782, Write 574, WebFetch 387, Agent 272, Artifact 207, WebSearch 106, Skill 46); ccd_turn 464; ccd_session_mgmt 99; scheduled-tasks 46; computer-use 39; Claude_Browser 17; Claude Docs (server 1a59c906) 13; ccd_session 2; ccd_sidebar 2. Every other server: 0.

What a thousand tokens in the start costs (estimate): about US$2.50 a week in the main sessions (108 starts at the 1-hour write rate plus 8,111 cache reads) and about US$1.50 more in general-purpose helpers; MCP instruction blocks reach every helper too.

### Ready to switch off (never or almost never called)

| Server or plugin | Calls 2-8 Nov | What it puts in the context | Note |
|---|---|---|---|
| claude-in-chrome | 0 | 22 deferred names (800 characters) + instructions (1,000) in every main start and every helper | His rules forbid browser interfaces to helpers |
| Google Drive (two copies: server 41d29ed5 and the claude.ai connector) | 0 | 32 deferred names (1,650 characters) | Duplicate connector |
| Google Docs (two copies: server 869c26a5 and the claude.ai connector) | 0 | 4 deferred names + two short instruction blocks (about 400 characters) | Duplicate connector |
| Claude Docs, claude.ai connector copy | 0 | 8 deferred names (270) + instructions (1,900) | The other copy (1a59c906) is the one called |
| Gmail, Google Calendar, n8n (claude.ai connectors) | 0 | listed as needing sign-in at each start | Not connected; switching off removes the notice |
| mcp-registry | 0 | 3 deferred names | |
| Skills never used this week (account skills unrelated to the project) | 0 | about 18,900 characters (est. 7,300 tokens) of the 29,900-character list, in every main start and general-purpose helper; est. US$29 a week | e.g. golf-journal-entry, erp-lastenheft-merger, ifs-* (3), initialschulung, process-profile-merger, n8n-workflow-json, deck-storyline, 2bcs-pptx, config-sheet-reader, google-workspace, docx, xlsx, pptx, pdf, humanizer, handoff-prompt, dataviz, code-review |

### Rarely used; his or the session's call (sizes shown, kept for now)

| Item | Calls | Size | Note |
|---|---|---|---|
| Claude_Browser (the app's built-in browser and preview) | 17 (main only) | 22,400 characters of always-loaded schemas (est. 6,600 tokens) in main and general-purpose helpers; est. US$17 a week in reads | Largest unused-ish item. Unverified whether the desktop app lets it be switched off |
| Claude Docs (server 1a59c906) | 13 (read 11, guide 2) | 1,800 characters of schemas + 5 deferred names + 1,900 of instructions | Which documents were read was not looked at (content rule) |
| visualize, terminal | 0 | 4,200 and 1,100 characters of always-loaded schemas | App built-ins; unverified whether switchable |
| App built-in tools never called: Workflow, SendUserFile, SuggestPluginInstall, ReportFindings, SearchPlugins, SuggestSkills | 0 | 17,000 characters of always-loaded schemas together (est. 5,000 tokens) | App built-ins; unverified whether a deny rule removes them from the request |
| ccd_host, ccd_pr, ccd_view, ccd_window, ccd_connectors, ccd_directory, ccd_settings | 0 | about 30 deferred names, about 900 characters | App built-ins, names only, small |

### Needed by the project's rules: stay

| Item | Calls | Size | Rule |
|---|---|---|---|
| Blender MCP | 0 this week | 26 deferred names (1,140 characters) + instructions (4,100) | Clothing work (CLAUDE.md, Blender live connection) |
| Unreal MCP (unreal-mcp) | 0 | failed to connect at 136 starts (connection refused: no editor running); costs only the failure notice | Unreal editor tools (CLAUDE.md) |
| computer-use | 39 | 27 deferred names (830) + instructions (5,100, the largest block) | Marvelous only (RULINGS 29 Oct) |
| scheduled-tasks | 46 | 6 deferred names | The hourly fresh-start task |
| Artifact, ArtifactData | 207 and 782 | Artifact's schema is the largest single tool: 37,800 characters (est. 11,000 tokens) | His page |
| ccd_turn, ccd_session_mgmt | 464 and 99 | 7,800 and 1,200 characters | Plan, wrap-up, usage reads |
| Project skills (street-weathering, packaged-walk, his-page, game-garment, speech-bench, asset-import, gate, shopfront, slate-roofs, artifact-capabilities, artifact-design, claude-api) and deep-research, the Unreal skills, computer-use, schedule | used, or named by the rules | | CLAUDE.md research method; Unreal, Marvelous, scheduled-task rules |

Estimated saving from the "switch off" list: about 22,000 characters of the start (skills list share 18,900, MCP instructions and deferred names about 3,300), roughly US$35 a week at list prices (inferred); more if Claude_Browser and the unused app built-ins can be dropped, and up to about US$55 a week if all general-purpose helpers became custom types (about 45,000 fewer start tokens over 106 starts and some 4,675 requests; inferred).

## Not checked

- The desktop app's own settings and the MCP configuration files were not opened (they may hold keys); so where each server is switched on, and whether the app's built-ins (Claude_Browser, visualize, terminal, Workflow and the others) can be switched off, is unverified.
- Exact token counts per part: the logs give only each step's totals; parts are estimated from characters.
- The server-side reason for the four undetermined misses.
- Why main starts share slightly different system-and-tools prefixes (cache reads of 45,950 to 51,005 tokens) was not examined.
- His plan's real meter: dollars here are list prices.
