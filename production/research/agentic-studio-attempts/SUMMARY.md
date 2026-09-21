# Who else is running agents as a studio, and what happened to them

STATUS: SPEC (research delivery). Branch `research/agentic-studio-attempts`.
Written 2026-09-19. Audited against `BRIEF.md` in this folder, which was written
before the work started.

NOTHING HERE IS AN INSTRUCTION. No queue item, no decision record.

## 0. Sourcing, measured today and not recalled

**Every primary host the brief names is refused.** Probed this session, 12 of
12 answered with a gateway 403 to CONNECT: `news.ycombinator.com`,
`reddit.com` and `old.reddit.com`, `itch.io`, `store.steampowered.com`,
`youtube.com`, `gdcvault.com`, `medium.com`, `lobste.rs`, `substack.com`,
`x.com`, `gamedeveloper.com`.

So the brief's instruction to prefer people's own writing over reporting about
them could not be followed for devlogs, store pages, talks or threads. What I
could do: **five web searches**, returning titles, URLs and the search channel's
summaries, and **two primary documents read in full** through
`raw.githubusercontent.com`, which is open. Those two are the only pages in this
delivery I actually opened.

Every claim below is labelled. CITED means a search summary unless it names one
of the two READMEs. There is no number in this file I would defend to two
decimal places.

## 1. The answer, first

**Almost nobody is visibly doing what LEDGER is doing, and what IS visible in
volume is the scaffolding rather than the results.**

The dominant artifact of 2026 is not a finished ambitious game made by agents.
It is a GitHub repository that turns Claude Code into a notional game studio.
Searches returned at least six of these, several of them forks of each other:
`donchitos/Claude-Code-Game-Studios`, `IdoCohen560/claude-unity-game-studio`,
`CoralGame/Claude-Code-Game-Studios`, `pa4uslf/Codex-Game-Studios`,
`Millionluna/Codex-Game-Studios`, `chuanglibs/Claude-Code-Game-Studios-Codex`.

They are strikingly close to this project's own shape, arrived at
independently. CITED, read in full from `donchitos/Claude-Code-Game-Studios`
README: 49 agents, 73 skills, 12 hooks doing "automated validation on commits,
pushes, asset changes, session lifecycle, agent audit trail, and gap detection",
organised as "Tier 1 Directors (Opus): creative-director, technical-director,
producer / Tier 2 Department Leads (Sonnet) / Tier 3 specialists". LEDGER's
tier 1, 2 and 3 split with a director, a producer and model-per-tier is the same
idea, written by someone else.

**And the games that are visible are small and fast.** CITED: Void Balls, one
person and eight parallel agents in 10 days, 29,000 lines of C# across 173
scripts; Grumbulus, two people in two evenings, 15,000 lines of JavaScript;
CODEX MORTIS on Steam Early Access, self-described as the "world's first 100%
AI-developed game". DERIVED: these are code-shaped projects finished in days.
None of them is a multi-year, content-heavy, photoreal simulation, which is the
shape of the thing being attempted here.

## 2. The two questions the brief wanted answered rather than approached

### 2.1 Has anyone built a persistent studio structure? Partly, and not the hard half.

**Standing roles: yes, widely.** See section 1.

**Verification gates: yes, and one is worth copying.** CITED, read in full from
`IdoCohen560/claude-unity-game-studio` README, its "Director Gates" section:
a gate check runs four directors in parallel (creative, technical, producer,
art), each returning `READY`, `CONCERNS [list]` or `NOT READY [blockers]`, and
**"strictest verdict wins, one NOT READY blocks the whole phase"**. It also
ships three gate intensity modes, full, lean and solo, set in a file called
`production/review-mode.txt`, with "solo: no director gates" recommended for
game jams.

DERIVED, and it is the most useful single import in this delivery: a
parallel multi-director gate with an explicit strictest-verdict-wins rule is
sharper than a single reviewing director, and the intensity mode is an honest
admission that gates cost something.

**Budget discipline: essentially absent.** Grepped both READMEs for token, cost,
budget, overnight, unattended and API spend. **One line in two documents**: "The
toolkit uses multiple model tiers (Haiku for simple tasks, Sonnet for
implementation, Opus for reviews) to optimize cost." That is model selection,
not a budget.

**Overnight autonomy: absent, and one framework explicitly rules it out.** CITED,
same README: "From there, **you drive**. The AI asks questions, proposes options,
and waits for your decisions. It never writes code without approval."

**So the answer is: the roles and the gates exist elsewhere, the budget ledger
and the unattended overnight run do not.** On the evidence I could reach, those
two are where LEDGER is ahead of everything visible, which is uncomfortable as
well as flattering: nobody has published how they go wrong.

### 2.2 Has anyone solved content mass rather than code mass? No, and the failure has a name now.

CITED: "Prompt volume often widens the decision surface faster than reviewers can
evaluate it, shifting the bottleneck from image creation to judgment design."
And: generated meshes "still need a human pass for clean topology, UVs, and
rig/animation readiness", the tool providing "a production-grade blockout fast
while an artist makes it ship-ready". And a second-order problem nobody here has
considered: "AI-generated assets rarely arrive with meaningful metadata, creating
a searchability problem that grows worse when multiplied across hundreds of
sessions."

DERIVED, and it lands directly on gap 2 of `brief-coverage`: generation stopped
being the constraint and judgement became the constraint. A studio that can
produce a thousand assets and review ten has not solved content mass, it has
moved the queue. LEDGER's own asset audit says 26 of 84 kinds are absent and 47
part-done, and this is the evidence that filling them is a reviewing problem
rather than a generating one.

## 3. Costs, such as they are

All CITED from search summaries, and they are about coding agents generally
rather than game studios specifically.

| | figure |
|---|---|
| Solo developer, subscription | $20 to $100 a month, "$17 to $20 flat" on Pro |
| Anthropic's own average | $13 per developer per active day, $150 to $250 a month |
| Uber, ~5,000 engineers from Dec 2025 | $500 to $2,000 per engineer per month |
| One developer's overnight loop | woke up "about $6,000 poorer" |

That last row is the one that bears on this project, because unattended
overnight running is the thing LEDGER does and the frameworks do not. HOLE: it is
a single anecdote in a pricing article, with no detail on what ran.

## 4. Where the bottleneck turned out to be

CITED, Metaplay, "Agents in game development, 4 reasons they break and 3 ways to
fix it": game development "breaks AI agents in ways other software domains
don't: unclear goals, no standard architecture, visual editors they can't
operate, and too much tribal knowledge".

DERIVED: three of those four are live here. Visual editors agents cannot operate
is the reason this project drives Unreal through generators and probes rather
than the editor, so the constraint is already designed around. Tribal knowledge
is what CLAUDE.md and the casebooks are. Unclear goals is what the Meridian Test
and the quality ladder exist for. The answer to the brief's question, whether the
bottleneck is code, content, taste or coordination, is that nobody reports code:
it is judgement and coordination, twice, from two independent directions.

And the wider mood is worth recording because it is not flattering. CITED: a 2026
GDC report has 52 percent of developers saying AI has a negative impact on
various areas, up from 30 percent in 2025, with 7 percent positive.

## 5. The null result, stated plainly because the brief asked for it

**I found no postmortem of an abandoned agentic game project.** One of the five
searches targeted failures and abandonments directly, and two others would have
surfaced one. What came back was tool round-ups, pricing guides and advice
posts. The one honest failure signal is the GDC sentiment number above, which is
a mood rather than a case.

This is the same null the lane hit before: `systemic-game-postmortems` searched
four ways for a game whose NPC memory system was cut and found none. Two of this
project's central bets, the moat and the method, both sit in areas with no
cautionary literature. Nobody has proved either is a trap and nobody has proved
it is not.

DERIVED: the absence is partly structural. People publish a repository the week
they build it and publish nothing the month they stop.

## 6. What I would take from this

1. **Import the parallel gate with strictest-verdict-wins** (2.1). It is a
   sharper instrument than one director reviewing, and it is free to try.
2. **Treat content mass as a review-capacity problem, not a generation problem**
   (2.2). Our assembly line's next number should be the share of generated units
   that survive review, not the number generated.
3. **The overnight budget ledger is not a solved problem anywhere visible**, and
   the one published datapoint is a $6,000 accident. That is an argument for
   keeping this project's budget discipline rather than a reason to relax it.

## 7. What could not be established

1. **How many attempts exist.** Answered through a search index, not a count.
   Every store page, devlog, thread and talk was refused.
2. **What any of these projects actually shipped.** I could not open a Steam or
   itch page. Void Balls, Grumbulus and CODEX MORTIS are search summaries, and
   the third is a self-description.
3. **Whether any framework has ever produced a finished game.** The repositories
   describe structure. None of the material I reached connects one of them to a
   shipped title.
4. **Costs for anyone running a studio structure**, as opposed to per-developer
   coding costs.
5. **Any failure case in detail.** Section 5.
6. **Anything about groups of two or three**, which the brief asked about
   specifically. Everything visible is solo or a framework.

## 8. Sources

Read in full through `raw.githubusercontent.com`, 2026-09-19:
- `donchitos/Claude-Code-Game-Studios`, README.md (16,039 bytes)
- `IdoCohen560/claude-unity-game-studio`, README.md (28,165 bytes)

Search channel summaries only, retrieved 2026-09-19, none opened: pixelsham.com,
strayspark.studio, cinevva.com, metaplay.io, restofworld.org, morphllm.com,
finout.io, seeles.ai, nextmars.com, artstash.io, aitoolly.com,
martianlee.github.io, starlog.is, and the GitHub repository listings named in
section 1.

Refused, 12 of 12: `news.ycombinator.com`, `reddit.com`, `old.reddit.com`,
`itch.io`, `store.steampowered.com`, `youtube.com`, `gdcvault.com`,
`medium.com`, `lobste.rs`, `substack.com`, `x.com`, `gamedeveloper.com`.

## 9. Why there is no DELIVERY.md

Every other topic ships a long form beside its summary. This one does not,
because there was not enough primary material to justify one: two documents read
and five search summaries would be padded, not deepened, by a longer file. If the
hosts in section 0 open, this topic is worth redoing rather than extending.
