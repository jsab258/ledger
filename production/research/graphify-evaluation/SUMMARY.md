# graphify: built for the half of our repository that is not our problem

STATUS: SPEC (research delivery). Branch `research/graphify-evaluation`.
Written 2026-09-19. Audited against `BRIEF.md` in this folder, written first.

NOTHING HERE IS AN INSTRUCTION. Nothing was installed, per the brief.

## 0. Sourcing

`github.com` and its API are refused for this repository; `raw.githubusercontent.com`
is open, so **the project's own README (63,754 bytes, `master`) and BENCHMARKS.md
(7,846 bytes) were read in full**. An older, shorter README on `main` (7,106
bytes) was also read and is superseded. One web search for third-party reports;
those hosts are refused, so that half is search summary and labelled
CITED-SUMMARY.

MY OWN INSTRUMENT FAILED ONCE, recorded because this project's rules require it:
my first fetch of BENCHMARKS.md wrote two different URLs to the same local
filename, so a 404 body overwrote the real file and my first read of it returned
nothing. Re-fetched cleanly. The numbers below come from the second read.

## 1. The answer, first

**Not worth trying, on our repository, as it stands.** Not because the tool is
bad. Because three measurements of our own repository say we would be buying the
half it does worst, and one of them is decisive on its own.

## 2. What it actually produces

CITED, README. `graphify-out/` containing `graph.html` (interactive), an
Obsidian vault, optional `wiki/` articles, `GRAPH_REPORT.md` (god nodes,
surprising connections, suggested questions), `graph.json`, and a SHA256
`cache/`. Commands are `query`, `path`, `explain`; there is an MCP server
(`python -m graphify.serve`), stdio or HTTP. `graphify-out/` is meant to be
committed, with a merge driver so `graph.json` avoids conflict markers.

It handles our file types on paper: docs are `.md .mdx .qmd .html .txt .rst
.yaml .yml`, and critically, CITED: "markdown `[text](./other.md)` links and
`[[wikilinks]]` become `references` edges between docs".

## 3. The three measurements of our repository

### 3.1 Our documents do not link to each other, they quote paths

Graphify builds doc-to-doc edges from markdown links and wikilinks. Measured
across **all 861 markdown files on `origin/main`, no cap**:

| form | count |
|---|---|
| markdown links to a `.md` file | **16** |
| `[[wikilinks]]` | **0** |
| backticked bare `.md` paths | **2,135** |

DERIVED, and this is the decisive one: we cite each other 2,135 times and link
each other 16 times, a ratio of 133 to 1 against the only form the tool reads.
The relationships Jafar wants found, a delivery overturned by a later delivery,
are written as `` `production/research/clothing-pipeline/RECHECK.md` ``, which is
not a link. The doc graph over our corpus would be built from 16 edges while the
2,135 real references stayed invisible.

### 3.2 The deliveries are not on the branch the tool would index

Measured: files under `production/research/` on `origin/main`: **0**. All
forty-seven deliveries live on forty-seven branches. Graphify indexes a working
tree. Its git integration rebuilds on commit and on branch switch, which means
it models one branch at a time, and nothing in the README describes querying
across branches.

DERIVED: a graph built on `main` contains none of the research corpus. A graph
built on a delivery branch contains that delivery and whichever earlier ones
that branch happened to inherit. The finding problem Jafar described is
precisely a cross-branch problem, and this tool has no cross-branch concept.

### 3.3 The free rebuild is the one we would never trigger

CITED, README's recommended workflow: `git commit` "rebuilds automatically, AST
only, no API cost". And separately: "When docs or papers change, run
`/graphify --update` to refresh those nodes too (code and docs update
independently)."

CITED, README: "Code is extracted locally with no API calls (AST via
tree-sitter). Everything else goes through your AI assistant's model API."

DERIVED: the automatic zero-cost path is code. Our changes are documents, so the
path that matters is the manual, model-priced one. Our corpus is **861 markdown
files, 7.9 MB** on main alone, before the forty-seven branches.

## 4. What the benchmarks measure, which is not this

CITED, BENCHMARKS.md. The headline suites are **LOCOMO** and **LongMemEval-S**,
which are conversational-memory benchmarks: recall@10 0.497 and QA accuracy
45.3% on LOCOMO, 76% on LongMemEval-S, against mem0, supermemory, BM25 and dense
RAG. The judging is careful (one shared model, blind-validated judge, 90.6%
agreement, Cohen's kappa 0.81), and the harness is reproducible.

The code result is separate and small: on ERPNext, "one graphify tool lifts
key-fact coverage across the graded question set **(n=6)** from 70.8% (a grep
and read baseline) to 82.0%, at about **140K tokens per query**".

DERIVED, three things:
1. **Neither headline benchmark is document retrieval across a repository.** They
   are long-conversation memory. Our problem is neither.
2. **n=6 is the denominator of the only code-intelligence result.** A 70.8 to
   82.0 move on six questions is a direction, not a number.
3. **140K tokens per query is not cheap**, and it sits oddly beside the marketing
   line about "71.5x fewer tokens per query", which is a ratio against
   context-stuffing rather than against grep.

**And the flagship cost claim is scoped in a way the headline hides.**
BENCHMARKS.md: "Graph construction costs zero LLM credits ... building the index
uses no API tokens." That is true of the tree-sitter path. The README says
everything that is not code goes through the model. For a repository that is
half documents, the "$0 build" claim does not describe our build.

## 5. Marketing against experience, as the brief asked

**Marketing** (the project's own and its ecosystem): 71.5x fewer tokens per
query, zero-credit graph build, "honest about what it found vs guessed", YC
backing, thirty-odd README translations, Trendshift badge. CITED-SUMMARY shows
the same claim quoted as 71x, 70x and 49x in different write-ups, which is
itself a signal about how it is being repeated.

**Experience**, all CITED-SUMMARY and all from people who used it:
- "the current workflow still felt rough enough that one developer did not keep
  reaching for it during day-to-day development"
- "The tool ended up uninstalled from every project."
- "For a 40-file side project, the graph took longer to build than the bug it
  was supposed to help you find."
- Rebuilds are CPU-intensive: "3 concurrent graphify processes at 65 to 73% CPU
  each, load average 12+, RAM saturated".
- A reviewer's reframing, which is the best sentence anyone has written about
  it: the question "isn't how much does this save, it's does my team even have
  the problem this solves".

## 6. What could go wrong that the README does not mention

The README is unusually honest and its troubleshooting section already names
twenty-odd failure modes, including "Extraction returns empty nodes/edges for
docs or PDFs", "Graph has duplicate nodes for the same entity (ghost
duplicates)", "`LLM returned invalid JSON`", "Graph HTML is too large to open in
a browser (>5000 nodes)", "`graph.json` has conflict markers after two devs
commit at once", and "Claude Code prompt cache invalidated after every `graphify
extract`". That last one is a real cost for a studio that runs long sessions.

What it does NOT say, and all of it bears on us:

1. **What happens when a document corpus has no links.** It says links become
   edges. It never says the doc graph is only as connected as your linking
   habit, which for us means a near-empty edge set (3.1).
2. **That there is no cross-branch view** (3.2).
3. **Any per-document cost figure.** There is a `graphify-out/cost.json` ledger,
   so the tool measures its own spend, but no published number for what a
   markdown corpus of our size costs to pass semantically. HOLE, and it is the
   number I most wanted.
4. **That committing `graphify-out/` to forty-seven branches** means a generated
   artifact and a merge driver in every one of them.

## 7. What it would cost us per rebuild

HOLE, honestly: **I could not establish a per-document price**, and I will not
invent one. What can be said with measured inputs:

- The corpus is 861 markdown files and 7.9 MB on `main`, plus 47 branches.
- The full first pass sends all of it through a model. The incremental pass
  sends changed docs only, via the SHA256 cache.
- Our actual daily churn is smaller than the brief assumed. Measured on this
  clone: **2 markdown files changed in the last day, 6 in two days, 28 in three
  days.** CAVEAT, and it bites: this clone is shallow, 58 commits reaching back
  only to 2026-09-16, and the 7-day figure reads 861 only because two bulk
  restructure commits touched 839 and 837 files. So "documents change daily" is
  true, but it is a handful a day, not the corpus.

DERIVED: incremental cost is therefore probably modest. The first build is the
expensive one, and it would have to be paid once per branch we care about.

## 8. The standing rule, and it fails that too

The rule is that no new instrument is adopted this month unless one is retired
in the same batch. **graphify has nothing to retire.** The thing it would
replace is grep, which is not an instrument this project owns, cannot be
retired, and costs nothing to keep. Nothing in `tools/` overlaps with it. So it
would be a net addition, which the rule exists to prevent, and it does not
qualify as an exception because the problem it solves is not one of the gaps a
gate currently fails to catch.

## 9. Recommendation

**Not worth trying**, in the brief's first form, for these reasons in order:
the deliveries are not on the indexed branch (3.2), our documents do not carry
the links the doc graph is made of (3.1), the free rebuild path is the one our
work never triggers (3.3), the benchmarks measure conversational memory rather
than document retrieval (4), the people who tried it uninstalled it (5), and it
retires nothing (8).

**And the honest footnote, because the problem is real.** Two of those six are
facts about us rather than about the tool. If the research corpus were merged to
one branch, and if deliveries cited each other with markdown links instead of
backticked paths, the two decisive objections would both disappear. Both changes
are cheap, both are independently useful for a human reader, and neither needs
this tool to justify it. If they ever happen, this evaluation should be reopened
rather than cited: the answer would genuinely be different.

What I would not do is adopt a code-intelligence tool to fix a
documents-across-branches problem and then discover we had bought the graph for
the 16 links rather than the 2,135 references.

## 10. What could not be established

1. **Any per-document or per-megabyte cost** for the semantic pass (7).
2. **Whether the doc pass extracts useful nodes without links.** It may still
   produce concept nodes from content even where no link edges exist; the README
   does not say, and I could not test it. This is the one hole that could change
   section 3.1, and it is the first thing to check if this is ever reopened.
3. **The third-party reports at first hand.** Every one is a search summary from
   a refused host, including all of section 5.
4. **The repository's code itself.** Only the two documents named in section 0
   were read; the API is refused for this repo, so I could not list its tree,
   read its tests, or check how doc extraction actually works.
5. **Churn beyond three days** (7), because the clone is shallow.

## 11. Sources

Read in full through `raw.githubusercontent.com`, 2026-09-19:
- `Graphify-Labs/graphify`, `master`, README.md (63,754 bytes)
- `Graphify-Labs/graphify`, `master`, BENCHMARKS.md (7,846 bytes)
- `Graphify-Labs/graphify`, `main`, README.md (7,106 bytes, older)

Measured from this repository at `origin/main`: markdown file count and size,
link and citation forms across all 861 files, `production/research/` presence,
and commit churn over the available 58 commits.

Search channel summaries, none opened: dev.to, mindstudio.ai, towardsai.net,
blog.alexrusin.com, kevinkinnett.com, clskillshub.com, graphify.net.
