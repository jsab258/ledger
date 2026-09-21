# Self-audit: what forty-three deliveries actually answered

STATUS: SPEC (stocktake, not a research topic). Written 2026-09-19 by the
research lane, on its own work, before more research is commissioned.

WHAT WAS EXAMINED: 39 delivered topics (every `production/research/<topic>/`
directory carrying a DELIVERY.md, unioned across all 40 research branches) plus
the 4 RECHECK files of 2026-09-19. 43 in total. Every SUMMARY.md was read in
full, 4,289 lines; the DELIVERY files, 14,315 lines, were searched rather than
read whole, and where that limits a claim below it says so.

## Finding 1, and it is the one that made Jafar's discovery an accident

**The commission is not in the record.** No brief for any research topic exists
anywhere in this repository. Searched: all 266 files under `production/queue/`,
zero mention a research topic; `production/inbox/` (3 files) and
`production/brief-input/` (6 files), zero carry a research commission. The only
trace of what was asked is whatever the delivery chose to quote of it.

**17 of 39 deliveries contain a sentence stating what was asked. 22 do not.**
And both topics Jafar caught, small-team-shipping and systemic-game-postmortems,
are in the 22.

That is the whole mechanism. A delivery that does not carry its commission can
only be audited against itself, and against itself every one of these is
coherent. Drift is undetectable by reading, which is why it took a conversation
to find. Everything below is therefore reconstructed from the deliveries' own
framing, and for the 22 it is reconstructed from nothing.

## The table

Answered = what the delivery demonstrably establishes. Commissioned = what it
says it was asked, or "not recorded". Flags: DRIFT answered an adjacent
question; REPO answered "what does our code already do" in place of an outward
question; OVERTURNED contradicted by a later delivery; SELF the lane set the
question itself.

| topic | answered | commissioned | flag |
|---|---|---|---|
| 1990-on-film-stock | our reference photographs are colour-graded, so they mislead | not recorded | DRIFT (self-declared) |
| ai-npc-demos-hollow | five ways shipped AI-NPC demos fail | not recorded | |
| asset-coverage | 84 asset kinds: 11 exist, 47 part-done, 26 absent | what a game of this shape is made of | |
| asset-packs | buying saves almost nothing, except clothing | not recorded | OVERTURNED by 31 |
| authored-stories-in-simulation | preparation for a writing lane not yet opened | feeds a later lane | |
| british-crime-fiction-tone | the town's economics, via one 1989 date | not recorded | DRIFT (self-declared) |
| british-policing-1988-1992 | what a person experiences of policing, 1988 to 1992 | procedure detail it could not source | partial |
| clothing-assembly-line | yes, clothes can be made the way kerbs are | which step stops the line | |
| clothing-pipeline | the pipeline decision was already taken by D2 plus D16 | make or buy period clothing | REPO, OVERTURNED by RECHECK |
| coverage-audit-disco-elysium | 26 systems checked, 5 structural | not recorded | |
| coverage-audit-hitman | 32 systems checked, 20 gaps | not recorded | OVERTURNED in part by rdr2 |
| coverage-audit-kcd2 | 71 systems checked, take 5 | not recorded | |
| coverage-audit-rdr2 | 36 systems checked, take 5 | what NPCs do unobserved | |
| coverage-audit-shadows-of-doubt | the one game that built our thing, and what it cost | not recorded | |
| crime-scene-1990 | 1990 forensics confirms a suspect, cannot find one | a period list of collectable evidence | |
| detection-legibility | how much of being watched the player should see | not recorded | SELF (asked Jafar twice, unresolved) |
| egress-allowlist | which hosts were refused and what it cost | not recorded | lane infrastructure, not research |
| emergent-story-legibility | how to make an emergent story followable | not recorded | SELF (lane's own recurring problem) |
| ethics-and-reception | two reception risks and one number | not recorded | |
| eyewitness-testimony | the ladder holds, plus one missing rung | validation of the ladder | |
| failure-after-arrest | nothing happens after arrest because arrest has no caller | not recorded | REPO |
| group-standing-without-a-score | it is already built; its statistic is the wrong kind | a district's feeling | REPO |
| hardware-floor | 12 GB, from three consumers added | not recorded | OVERTURNED in part by RECHECK |
| hitman-density | how a small place reads as full | not recorded | worst-sourced by its own account |
| holding-a-large-script | three gates hold the words, one does not run | what holds the words | |
| holding-information | how to hold information a player cannot write down | not recorded | |
| live-speech-architecture | the experiment already ran; the margin is 1.07x not 2.3x | is the August experiment still next | OVERTURNED by RECHECK |
| llm-inference-economics | the game phones Anthropic and the player pays | not recorded | |
| markerless-mocap | no, not now; footskate tool instead | is bespoke mocap worth doing | reason CORRECTED by RECHECK |
| photoreal-on-a-budget | trim sheets and wear carry a frame, and a generator can emit them | not recorded | |
| players-and-a-world-that-remembers | players tell somebody; our measure is awkward | not recorded | DRIFT (self-declared) |
| precomputed-day | we already do this; three deliveries said we did not | live or precomputed simulation | REPO |
| rumour-propagation | five differences, one of them our own two files disagreeing | not recorded | |
| small-team-shipping | how one person survives a seven-year project | not recorded | DRIFT (Jafar found this) |
| small-town-networks | the non-uniformity is in canon and nothing reads it | so intersections are not uniform | REPO |
| systemic-game-postmortems | how four human-made simulation games got hurt | not recorded | DRIFT (Jafar found this) |
| teaching-in-thirty-minutes | the tutorial is the first ninety seconds | how a game teaches a social system | |
| tts-licensing-and-consent | what we may ship, and the missing attribution | not recorded | |
| unreal-frame-budget | nobody can set the number yet | not recorded | |
| RECHECK live-speech | Turbo drops exaggeration; Nano exists | two named questions | commissioned precisely |
| RECHECK hardware-floor | the paper says close to the opposite | what the paper establishes | commissioned precisely |
| RECHECK markerless-mocap | closed by labour, not licence | does a commercial route exist | commissioned precisely |
| RECHECK clothing-pipeline | one unnamed outfit; no skinning required | three named questions | commissioned precisely |

## Finding 2: the afternoon pattern is real but narrower than suspected

Six deliveries name an afternoon or an hour: asset-coverage, asset-packs,
clothing-assembly-line, clothing-pipeline, llm-inference-economics and
tts-licensing-and-consent. Read against "would this tell us we were done", they
split four ways, and only one is the failure Jafar described.

- **No success criterion at all: llm-inference-economics.** "Putting a small
  local model behind it and seeing whether it can hold a character is an
  afternoon." Holding a character is not a measurable state, so the afternoon
  cannot end. This is the clean case.
- **Criterion present, afternoon assigned to Jafar: clothing-pipeline.** It did
  say what each outcome would mean. It asked the one person whose evenings are
  the project's scarcest resource to spend one, on a question the studio could
  have answered from a document. The afternoon did not happen for eight days,
  and the RECHECK then answered it from a desk in an hour, finding the premise
  false. **The fault was not the missing criterion, it was the assignee.**
- **Done correctly: clothing-assembly-line.** "Build the verifier first, then
  spend an afternoon." The verifier is the criterion. This is the template.
- **Criterion present, nobody assigned: asset-coverage and asset-packs.** Both
  park their afternoon under "what could not be established", and both name a
  number that would end it: what share of 157 meshes survives the 1988 to 1992
  rule, and what share of a modern British pack is period-safe. A named number
  with no owner is a different failure from a vague test, and it is the quieter
  one, because the file reads as complete.

tts-licensing's afternoon is a task, not a test, and is not an instance.

## Finding 3: nine overturns, and not one is marked

| overturned | by | still live in its own file |
|---|---|---|
| asset-packs: clothing is the one purchase worth making | clothing-pipeline (the BOM says no purchase) | yes, line 84 |
| clothing-pipeline: Mixamo bodies are fused, no re-dress | clothing-assembly-line (14 of 18 carry separate garments, one shared skeleton) | yes |
| clothing-pipeline: garments must be weighted to metahuman_base_skel | RECHECK (Epic: you do not have to skin your clothing) | yes |
| clothing-pipeline: Jafar should inspect the wardrobe | RECHECK (there is no wardrobe) | yes |
| live-speech: move to Turbo | RECHECK (Turbo drops exaggeration) | yes |
| live-speech: chunk decode unmeasured, its weakest link | hardware-floor (0.454s per second of audio, already measured) | yes |
| hardware-floor: a sub-GB fixed-persona model is a researched position | RECHECK (the paper's authors decline to recommend it) | yes |
| markerless-mocap: the route is closed by licence | RECHECK (closed by labour) | yes |
| three deliveries: Shadows-of-Doubt precompute is absent here | precomputed-day | yes |

**Zero of 39 deliveries carry a supersession marker.** Grepped for SUPERSEDED,
CORRECTED BY and OVERTURNED at line start across all 39 summaries and all 39
deliveries: one hit, and it is prose about a game-design document rather than a
marker on a delivery. So every overturned sentence above is still readable as
current by anyone who opens that file, and every correction was found by the
next topic that happened to walk over the same ground. Nothing scheduled found
any of them.

## The topics where the question was never asked

Distinguish two things that look alike.

**Never asked by Jafar, asked by the lane of itself: two.**
detection-legibility says it "answers a question I have now put to you twice and
could not resolve either time", and emergent-story-legibility says "this is the
third time my own work has arrived at this problem". Both are good work. Neither
was commissioned, and both consumed a delivery slot.

**Not research at all: one.** egress-allowlist is a report on the lane's own
blocked hosts. It belongs in operations.

**Unrecoverable: twenty-two.** For these the honest statement is not that no
question was asked but that no record of one survives, and I will not invent the
difference. This is the same 22 as Finding 1.

## What I would change, and it is three lines

1. **A delivery quotes its brief in its first ten lines, verbatim.** Without it
   no future audit can do better than this one did.
2. **An afternoon names the sentence that ends it**, and names who spends it.
   Default to the studio; Jafar's hour is for judgement a document cannot settle.
3. **An overturned delivery gets a line at the top saying so, on the day it is
   overturned, by whoever overturns it.** Nine wrong sentences are currently
   readable as current, and the next reader has no way to know.

## What this audit could not establish

- **The real commissioned questions.** Not in the repository, so drift is
  measured against each delivery's own account of its brief. Jafar can refute
  any row above from memory and I cannot.
- **Whether the 22 unrecorded topics drifted.** Unknowable from here. The two
  known cases are both in that group, which is a reason to suspect more, and
  suspicion is not a finding.
- **Whether the 9 overturns are all of them.** They were found by searching for
  correction language. An overturn nobody noticed says nothing, so this count is
  a floor.
- **Anything about delivery quality.** This audit asked what question each
  answered, not how well.
