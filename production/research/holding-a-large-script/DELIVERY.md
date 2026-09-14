# Holding a large branching script without losing editorial control

Research topic 26. Delivered to the studio. Nothing here is an instruction.

**Standing egress note, from here on in every delivery rather than only where it
bites.** One route out of this container reads a page in full: `curl` reaches
package registries (`pypi.org`) and `raw.githubusercontent.com`, verified today
with real content. `github.com` and `api.github.com` return 403. Everything else
tried, including arxiv, Wikipedia, Hansard, journals, news and vendor
documentation, returns 000. So SOURCE REPOSITORIES AND LICENCE FILES ARE
READABLE PRIMARY SOURCES AND RESEARCH LITERATURE IS NOT. Where this delivery
cites a licence it was read in full; where it cites press or criticism it is a
search engine's summary and says so.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

---

## Part 1. What happened to Disco Elysium, from the person it happened to

CITED, via search summaries of January 2026 coverage of an interview with Helen
Hindpere, writer on the original game and lead writer on the Final Cut:

- The script is over a million words.
- On the tool: "There was a lot of dialogue so it got quite janky, at some point
  froze completely, because it definitely wasn't built for it."
- On the cause: "we were writing too much. Like, there wasn't enough time to
  edit it, to go over it, we would have to cut some parts." The team decided
  they would "just have to find the time", because of how good the writing was.
- On the consequence, in the reporting's words: there was so much text that
  control over the material began to be lost, and editing turned into a constant
  struggle with deadlines.

[PC Gamer, Disco Elysium had so much text it broke the branching narrative software](https://www.pcgamer.com/games/rpg/disco-elysium-had-so-much-text-it-broke-the-branching-narrative-software-we-were-writing-too-much/),
[ixbt Games, Disco Elysium hit a technical limit due to the volume of the script](https://ixbt.games/en/news/2026/01/16/disco-elysium-uperlas-v-texniceskii-predel-iz-za-obieema-scenariia.html),
[Articy's own showcase page for Disco Elysium](https://www.articy.com/en/showcase/disco-elysium/)

DERIVED, and the two halves are worth separating because only one of them is
about software: the tool froze, AND the editorial process failed. Those are
different failures with different causes. A faster tool would have fixed the
first. Nothing about a tool fixes "there wasn't enough time to edit it".

The sentence that matters most is the one about the decision: they chose not to
cut, on the grounds that the writing was good. That is a judgement about
quality made at the moment when the volume had already outgrown the process,
and it is exactly the judgement a project with this one's standard is most
likely to make.

---

## Part 2. What the tool landscape actually is

CITED: the tools split into two camps, visual node editors (articy:draft,
Arcweave, StoryFlow) and text-based scripting languages (Twine, Ink, Yarn
Spinner). Articy is described as "an integrated visual environment (similar to
a 'narrative CMS') combining story flow editing, object databases, and team
collaboration, unlike pure scripting tools like Ink or Yarn Spinner", with "a
built-in database to manage game assets, characters, locations, and inventory
items".
[Dunia, 10 best branching narrative tools for 2026](https://dunia.gg/blog/branching-narrative-tool),
[NarrativeFlow, Twine vs Yarn Spinner vs Ink](https://narrativeflow.dev/blog/twine-vs-yarn-spinner-vs-ink-vs-narrativeflow-which-branching-dialogue-tool-is-right-for-your-game/)

CITED, and this is the line that decides the question for this studio: "Choose
text-based scripting (Ink, Yarn Spinner, Twine) when the narrative is mostly
linear, writers are comfortable with markup, and you want CLEAN GIT DIFFS."
[NarrativeFlow, as above]

CITED, on scale: "If you're making a serious game and expect lots of state, ink
is the strongest long-term craft tool in this list. It asks more from you, but
it pays that back in control and scalability."
[Loreweaver, Best narrative design tools for game developers](https://loreweaver.ink/insights/best-narrative-design-tools/)

CITED, read in full from the primary source rather than summarised, because
`raw.githubusercontent.com` is reachable and the licence allowlist is law:

- **Ink** is MIT. `LICENSE.txt` on `inkle/ink` master reads "MIT License /
  Copyright (c) 2025 inkle Ltd."
- **Yarn Spinner** is MIT. `LICENSE.md` on `YarnSpinnerTool/YarnSpinner` main
  reads "The MIT License (MIT) / Copyright (c) Yarn Spinner Pty. Ltd., Secret
  Lab Pty. Ltd., and Yarn Spinner contributors."

Both would clear the allowlist's process rule on a decision record. Articy is
commercial licensed software and no purchase is authorised in this lane.

DERIVED: a binary node-graph database is not merely inconvenient for this
studio, it is architecturally opposed to how it works. Everything here is
committed, every claim carries a verify footer, and every gate reads files. A
format git cannot diff removes the review surface that this project's entire
method rests on. That is a stronger argument against Articy here than the
freezing is.

---

## Part 3. What LEDGER actually has, measured today

### 3.1 The corpus, counted

Measured on 2026-09-14 by walking every prose string in the authored content:

| file | words |
|---|---|
| `content/dialogue/crime-witness-v1.json` | 726 |
| `content/dialogue/pub-regular-v1.json` | 819 |
| `game-design/barks.json` | 50,660 |
| `game-design/tier2-batch-1.json` (60 cards) | 13,564 |
| **total authored speech and cards** | **65,769** |

DERIVED: 6.58% of Disco Elysium's million. The corpus that broke Articy is
fifteen times this one.

### 3.2 And it is not a branching script at all

CITED, the actual shape of `content/dialogue/pub-regular-v1.json`:

    rungs:    ["stranger", "novak", "tom"]
    contexts: ["greeting", "deed_reaction", "gossip_pass"]
    lines:    a flat list of 48 objects
    lines[0]: {"id": "pr-001", "rung": "stranger", "context": "greeting",
               "text": "Evening. You'll be the one that got the pub, then.
                        Mickey kept the mild on the left."}

DERIVED, and this is the finding of the topic: LEDGER's dialogue is a TAGGED
CORPUS SELECTED BY STATE, not a branching graph. There is no node, no edge, no
condition beyond two tags, and no path through the material. Three rungs times
three contexts is nine cells holding forty-eight lines.

That is a categorically different data structure from what Articy holds, and it
has categorically different failure modes. **You cannot freeze a flat list.**
Disco Elysium's specific disaster is structurally unavailable to this project,
and any proposal to adopt a graph tool to avoid it would be buying insurance
against a fire in a building we do not own.

### 3.3 What holds the words today, and it is more than nothing

Read off the green verify footer and the tools themselves on 2026-09-14:

- **`tools/content-gate.py`**, the D18 word lists: 7 of 18 clauses enforced
  mechanically, 10,058 strings scanned, `hitsNew=0`, 197 baselined and stamped,
  "THIS LIST IS TO BE EMPTIED, NEVER GROWN".
- **`tools/slopcheck.py`**, nineteen signs-of-AI-writing patterns over 4,975
  strings, reporting `slop 86/88`. Its docstring in `ledger/verify.py:2437`
  makes it "A RATCHET ON THE BACKLOG, not a wall. The bark bank and the Tier-2
  cards are at zero and must stay there", with the 86 being spaced em dashes in
  the Game layer's authored narration, and the ceiling permitted to move only
  downwards.
- **Bark enumeration**: "barks current (2604 lines enumerated, 0 drifted)".
- **Card discipline**: "13 card-writing rules", "60 cards shipped as edited",
  where the last check compares `StreamingAssets` against `game-design` and
  names which cards differ rather than saying they differ.
- **Repetition**: `production/throughput.md` records the pilot bank's
  "repetition worst 0.18".
- **Tone**: the D7 judges, pending on the pilot bank.

DERIVED: this is a real editorial apparatus and it is lexical and statistical
rather than structural. It cannot tell you that the script is incoherent. It can
tell you that a new line broke a rule, drifted from its manifest, repeated
itself, or sounded like a machine wrote it.

And it demonstrably works on exactly the case that would slip past a human. The
gate's report today reads:

    speech content/dialogue/pub-regular-v1.json:pr-001 rule=mild_noun
           kind=alcohol matched=the_mild
        Evening. You'll be the one that got the pub, then. Mickey kept the
        mild on the left.

That line is period-perfect, in register, and breaks D18's absolute alcohol
clause. No reader would catch it twice in a row across five thousand lines. The
word list caught it, named the rule, and it is already counted in the 197.

---

## Part 4. The failure mode this project actually has

If the graph-freeze is unavailable, what replaces it.

DERIVED, and offered as the substance of the topic rather than a hedge: a
tagged corpus does not lose editorial control by seizing up. It loses it by
DUPLICATION AND CONTRADICTION at a volume no one person can hold. At five
thousand lines, line 3,012 says the pub opens at eleven and line 418 says half
ten, and nothing in the apparatus above can see it, because both are clean, both
are in register, neither repeats the other and neither breaks a word list.

Three things make that risk sharper here than in an ordinary game:

1. **The corpus is the LLM's conditioning, not just its output.** The cards are
   already 13,564 words of the 65,769, and `ConversationEngine.BuildSystemPrompt`
   feeds a card block of 4,581 to 5,430 characters into every single turn (topic
   19). A contradiction in a card does not sit inertly in a file; it propagates
   into every generated line that character ever speaks.
2. **The moat is consistency.** Topic 25 found that players reliably notice NPCs
   FORGETTING and no research measures them noticing memory that works. A
   self-contradicting corpus is the authored form of forgetting.
3. **Volume is planned to grow and the tooling is not.** Two banks and a bark
   file today, against a phase 2 target of thirty to fifty residents on one
   street.

### 4.1 The third gate, which exists, works, and nothing runs

I first wrote this section saying `tools/canon-gate.py` was unread and might
close the gap. Rule 3 says open the file, so I did, and it changed the finding
twice over.

CITED, its own docstring: it checks "era artifacts and banned modernity" and
real brands, word-boundary matched, "reusing the imagegen forbidden-token list
so there is one list, not two". It states plainly what it refuses to claim:
"TONE IS NOT MECHANICAL and is not checked here ... A tool that pretended to
check tone would be a claim with no instrument, which is the exact thing the
constitution forbids." Every refusal names file, line and word; every clean
result ships its denominator.

CITED, run today over both banks and the bark file:

    canon-gate: clean - 0 finding(s) in 3 file(s), 97 line(s) examined,
                13 era term(s) and 45 brand token(s) screened

So it works, and it is another WORD LIST. It refuses a line that mentions a
mobile phone. It cannot tell that line 3,012 and line 418 disagree about when
the pub opens. The assertional gap in this section is therefore CONFIRMED rather
than closed: nothing in this checkout checks a line against the world facts it
asserts.

And the second thing, which is the sharper one. CITED: grepping every `.py`,
`.yml`, `.sh`, `.bat` and `.md` in the repository for `canon-gate` returns nine
hits and EVERY ONE IS A DOCUMENT. Three learning-log rows, four decision
records. No automated caller anywhere. `ledger/verify.py` does not run it: a
grep of that file for `canon-gate` returns nothing, while `content-gate` returns
six hits.

One of those documents says it out loud.
`game-design/decision-2026-09-08-the-lookup-that-lied-and-the-art-line-in-house.md:30`:
"`tools/canon-gate.py` was NOT run here. I did what the gate does by hand."

DERIVED, and it is CLAUDE.md rule 6 landing on the editorial apparatus itself:
the canon gate is built, tested, honest about its own limits, and hand-run. The
content gate and the slop check are wired into `verify.py` and therefore run
before every commit; the canon gate is a thing somebody has to remember. The
project's own record already contains the instance of somebody not remembering
and doing it by hand instead.

For a topic about what holds the words, that is the answer: two of the three
gates are held by the build and the third is held by attention.

---

## Part 5. What could not be established

1. **Nothing.** The one hole this delivery opened with, whether
   `tools/canon-gate.py` closes the assertional gap, was closed by reading it:
   it does not, and separately it has no automated caller. Recorded here so the
   list is honest about having shrunk.
2. **Any primary account from ZA/UM.** The Hindpere quotes are press summaries
   of an interview; the interview itself was not reachable.
3. **What Articy actually does at scale**, beyond the marketing description and
   the failure report. Its own docs were not fetched.
4. **Whether Ink or Yarn Spinner would suit a tagged corpus at all.** Both are
   built for branching flow, which is the structure this project does not have.
   The honest answer may be that neither is the right tool and the right tool is
   the JSON that exists plus more checks.
5. **The word count of the live generated speech.** Unbounded and unmeasured, by
   construction.

---

## Part 6. Findings and interpretation

### Findings

F1. Disco Elysium's million-word script froze Articy, in its lead writer's
words "it definitely wasn't built for it".

F2. The editorial failure was separate from the tool failure: "there wasn't
enough time to edit it", and the team chose not to cut because the writing was
good.

F3. The tool landscape splits into visual node editors and text scripting
languages, and the stated reason to choose the second is clean git diffs.

F4. Ink and Yarn Spinner are both MIT, read from their LICENSE files in full.

F5. LEDGER's authored speech and cards total 65,769 words, 6.58% of Disco
Elysium's million.

F6. LEDGER's dialogue is not a branching graph. A bank is a flat list of
`{id, rung, context, text}` objects over three rungs and three contexts.

F7. Editorial control today is lexical and statistical: a D18 word gate over
10,058 strings, a nineteen-pattern slop ratchet at 86/88 with banks and cards at
zero, bark enumeration at 2,604 lines with zero drift, 13 card-writing rules and
a shipped-cards comparison.

F8. The gate catches what a reader would not: `rule=mild_noun kind=alcohol
matched=the_mild` in a line that is otherwise period-perfect.

F9. Cards are 13,564 of the 65,769 words and are fed into every live
conversation turn.

F10. `tools/canon-gate.py` screens era terms and brand tokens, explicitly
refuses to claim tone, and runs clean today over both banks and the bark file:
"0 finding(s) in 3 file(s), 97 line(s) examined, 13 era term(s) and 45 brand
token(s) screened".

F11. It has no automated caller. Nine references across the repository are all
documents; `ledger/verify.py` never invokes it, and a decision record of
2026-09-08 states "tools/canon-gate.py was NOT run here. I did what the gate
does by hand."

F12. No gate in this checkout checks a line against the world facts it asserts.

### Interpretation

I1. The specific disaster in the brief cannot happen here, and the reason is
structural rather than lucky: a flat tagged corpus has no graph to freeze. A
tool adoption justified by Disco Elysium's story would be solving a problem this
project does not have.

I2. The failure that CAN happen is contradiction at volume, and it is worse here
than in an ordinary game because the corpus conditions a language model rather
than merely being read by a player. A wrong fact in a card is not one wrong
line, it is a wrong premise in every line that character will ever generate.

I3. The apparatus that exists is unusually good at the lexical layer and has
nothing at the assertional layer. That is now established rather than suspected.
All three gates are word lists: one for content rules, one for AI-writing tells,
one for period and brands. None of them can see a contradiction, which is the
failure mode a growing tagged corpus actually has.

I3b. The canon gate having no caller is the cheaper of the two things in this
delivery to fix and the easier to miss, because it is green when run and
therefore looks fine in every record that mentions it. A gate held by attention
is a gate that works until the day somebody is busy, and this repository already
records that day.

I4. The quote worth keeping is not about software. It is "we would have to cut
some parts" followed by the decision not to. This project already has the
instrument that makes that decision visible: the throughput ledger counts
verified pieces and records a finished brand bible as ZERO. The equivalent for
writing would be counting lines that something actually selects, which is rule 6
applied to prose.
