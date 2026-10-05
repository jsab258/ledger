# Voice cloning and TTS licensing: what may ship, and on what terms

Research topic 20. Delivered to the studio. Nothing here is an instruction, and
nothing here is legal advice. Where it names law it names a secondary source
and a date, and says so.

Scope split with the neighbours, declared once: topic 1 asked how the live
speech stack should be SHAPED, topic 2 asked what it WEIGHS, topic 19 asked
what the language half COSTS. This one asks what may be SHIPPED and under whose
terms: the corpus licence, the speakers' consent, the model's conditions, and
the disclosure regimes that have changed underneath all three in 2026.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

Egress, stated because it fails silently: `datashare.ed.ac.uk`, the University
of Edinburgh page that holds the VCTK corpus and its licence text, is
EGRESS_BLOCKED from this container, measured 2026-09-14. The single document
this topic most needed to read is the one it could not open.

---

## Part 1. What this project ships, and what it says about it

Every claim in this part was produced by a command run on 2026-09-14.

### 1.1 The rules this project already holds, which are unusually good

CITED, `CLAUDE.md:163`, verbatim and in full:

    Voice sourcing consent rule: only corpora whose contributors donated their
    voices to build speech technology, and no identifiable public figures, ever.

CITED, `ledger-v2/research/license-allowlist.md`, SHIP-SAFE entry 1: "Voices:
the local voice pipeline as built; Kokoro (Apache 2.0), Chatterbox (MIT, keep
watermark), Piper (MIT original; the active fork is GPL-3.0, acceptable for
generated audio, check before embedding code). ElevenLabs on paid tiers if
adopted." NEVER SHIP entry 1: "XTTS-v2 or F5-TTS official weights output
(non-commercial)." NEVER SHIP entry 5 includes "cloned real voices, celebrity
styles".

CITED, PROCESS rule 1 of the same file: "Every asset and generated output
carries a license tag; untagged fails the license gate."

Interpretation, offered before the criticisms that follow: this is a stronger
starting position than most studios have. The consent standard is stricter than
the licence requires, the distinction between a licence and a consent is
already drawn, and the ban list names the two non-commercial TTS models by
name. The findings below are about REACH, not about intent.

### 1.2 Every voice in the game is VCTK, and the tool records how that was nearly missed

CITED, `tools/voice-fetch/ledger_voice_fetch.py`, the docstring at line 32
onward, verbatim in the parts that matter:

    THE CONSENT RULE, held unprompted
    Clips come only from corpora whose contributors donated their voices TO
    [build speech technology] ... copyright and does not settle consent, and a
    volunteer who read a novel ... public figures, ever.

    WHICH CORPUS, AND THIS PARAGRAPH WAS STALE UNTIL 13 AUGUST. It said
    "Common Voice (CC0) first, LibriTTS as fallback" and did not mention VCTK
    at all - while every voice in the shipped game is VCTK, which the picked
    [ids show, since] `pNNN` is VCTK's speaker id.

CITED, same file, line 468: "VCTK: 110 English speakers recorded in a treated
room at Edinburgh, each labelled with gender, age and accent", and line 474:
"Consent holds exactly as before: VCTK speakers were recruited and recorded for
speech-technology research."

CITED, `ledger/.verify-footer` from today's green run: "voice cast ok (0 uncast
of 7 tier-1 principal(s); 17 cast voice(s), 2 alias(es), 23 clip(s))", and
`game-design/shopping-list.md:22`: "Voices: DONE, and free. Nineteen cast from
VCTK, a corpus of donated" voices. 17 plus 2 aliases is 19 and the two agree.

DERIVED: the corpus in use is CSTR VCTK, from the University of Edinburgh. That
matters because everything in Part 2 hangs off which corpus it actually is, and
this project has already had one incident where a document said a different
one.

### 1.3 VCTK is CC BY 4.0, and nothing shippable attributes it

CITED: "The VCTK corpus is licensed under the Creative Commons License:
Attribution 4.0 International."
[University of Edinburgh DataShare, CSTR VCTK Corpus version 0.92](https://datashare.ed.ac.uk/handle/10283/3443)
(EGRESS BLOCKED; licence identified through search summary, not read on the
page)

CITED, checked today: this repository contains six `ATTRIBUTION.json` files.
Every one of them is 3D or image content:

    content/props/ATTRIBUTION.json
    ledger/Assets/Props/ATTRIBUTION.json
    ledger/Assets/StreamingAssets/CityPack/ATTRIBUTION.json
    ledger/Assets/StreamingAssets/Decals/generated/ATTRIBUTION.json
    production/assets/vignette/decals2d/ATTRIBUTION.json
    production/art/compare/hook-2026-09-09/ATTRIBUTION.json

CITED: a grep for `vctk`, `cstr` and `edinburgh` across `content/`,
`ledger/Assets/` and `game-design/` returns exactly one substantive hit, and it
is a shopping list, not an attribution: `game-design/shopping-list.md:22`.

DERIVED: CC BY 4.0's single obligation is attribution. Nineteen voices in the
game derive from a CC BY corpus and no shippable file names it. The allowlist's
own PROCESS rule 1 says an untagged asset fails the licence gate; the asset
class it is failing on is the one the gate does not look at.

This is the cheapest finding in the topic to fix and the easiest to leave
undone, because the six files that do exist make the whole area LOOK covered.

### 1.4 The ban on the non-commercial TTS models is enforced in the wrong pipeline

CITED, `tools/meshgen/meshgen.py:161`, a dictionary named `BANNED` whose
entries include:

    "xtts":   "allowlist NEVER SHIP 1: non-commercial weights",
    "f5-tts": "allowlist NEVER SHIP 1: non-commercial weights",

with a comment above it: "source naming any of these is refused mechanically
rather than argued about." It is a good guard, it is word-boundary matched, and
its selftest checks both outcomes including the accepting case (`TripoSR` must
NOT match the `tripo` ban).

CITED: a grep for `BANNED` and `banned_hits` across `tools/` and `ledger/`
returns hits in exactly one file, `tools/meshgen/meshgen.py`. Nothing in
`tools/voice-fetch/`, `tools/voice-gen/` or `tools/voice-live/` imports it.

DERIVED, and it is CLAUDE.md rule 6 applied to a legal guard: the mechanical
refusal of two TEXT-TO-SPEECH models is reachable only from the pipeline that
generates 3D PROPS. A voice tool handed a spec naming XTTS would be refused by
nothing. The guard is built; on the voice side it is not running.

I want to be fair about the severity. Nobody is about to fetch XTTS by
accident, and the human-readable rule is in the allowlist and in CLAUDE.md. The
value of the finding is the SHAPE: the project's one mechanical licence refusal
covers one of its two generative pipelines, and the uncovered one is the one
whose subject matter the ban was written about.

### 1.5 The watermark: declared, deferred, and now overtaken

CITED, `tools/voice-live/export_probe.py:1762`, a class `NoWatermark` whose
`apply_watermark` returns the audio unchanged, installed over
`perth.PerthImplicitWatermarker` when the real one cannot be constructed.

CITED, the same file at 2117 onward, and the reasoning is explicitly declared
rather than hidden:

    THE WATERMARKER MUST NOT BE ABLE TO STOP THIS ... it is IRRELEVANT to the
    question being asked: the watermarker is post-processing applied to
    finished audio, not one of the three pieces being exported ... DECLARED,
    not hidden - the shipped path has to make its own decision about Resemble's
    watermark, and this stub is for the export question only.

CITED, checked today: a grep for `watermark` across `ledger/Assets/Scripts/`
and `ue-probe/` returns nothing. The C# runtime and the Unreal probe contain no
watermarker.

DERIVED: the export probe's reasoning is correct on its own terms and the
decision it deferred has not been taken. The allowlist condition reads
"Chatterbox (MIT, keep watermark)". The three exported graphs are what the game
runs; the watermarker sat after them, in Python, in a path the game does not
use. So the shipped audio, today, carries no watermark, and no document records
that as a decision.

Part 2.3 is why that stopped being a housekeeping question in August.

### 1.6 The live path has no content screen, in text or in voice

CITED: `Core/ResponseValidator.cs` states its scope in its own header, "Two
jobs only", and they are reply length and the fourth wall. A grep of that file
for `ContentRule` returns zero.

CITED: `Core/ContentRule.cs` is D18's only code site and has three call sites
in the whole project: `Game/RealBody.cs:501`, `Core/Population.cs:177` and
`Core/Population.cs:186`. All three are crowd and body generation.

DERIVED: D18, the content rule, is enforced on the bodies the crowd generator
builds and on nothing that a character SAYS or that the voice pipeline SPEAKS.
Part 2.4 is why a storefront now cares about that.

---

## Part 2. What changed underneath this in 2026

### 2.1 The corpus licence settles copyright and does not settle consent

CITED: VCTK 0.92 is CC BY 4.0.
[Edinburgh DataShare](https://datashare.ed.ac.uk/handle/10283/3443) (blocked),
[VCTK on TensorFlow Datasets](https://www.tensorflow.org/datasets/catalog/vctk)

HOLE, stated rather than filled: the search could not establish what the VCTK
speakers' consent forms actually permit. The licence is a copyright licence
over the recordings. It does not, on its face, speak to the speakers'
personality or publicity rights, and it does not say whether a speaker
consented to having their voice used as the timbre reference for a synthetic
character in a commercial game.

The project's own tool already says this in one line, and it is the most
sophisticated sentence in the whole area: a licence "settles copyright and does
not settle consent". Nothing I found contradicts the project's judgement that
VCTK meets its consent rule, since the speakers were recruited and recorded
specifically to build speech technology. What I could not do is verify it
against the consent document, because the page is blocked.

### 2.2 Cloning law has hardened, and one date has already passed

CITED: the EU AI Act "becomes fully applicable on August 2, 2026", and "from
August 2026, providers must mark AI-generated audio in a machine-readable way,
and deployers must disclose deepfakes".
[Soundverse, EU AI Act and voice cloning regulations](https://www.soundverse.ai/blog/article/eu-ai-act-and-voice-cloning-regulations-explained-1055),
[Oreate AI, New federal laws and the EU AI Act](https://discover.oreateai.com/discover/new-federal-laws-and-the-eu-ai-act-are-redefining-voice-cloning-compliance)

CITED: Tennessee's ELVIS Act (2024) was the first state law to extend
right-of-publicity protection expressly to AI voice clones; 46 US states now
have at least one law touching AI-generated voice; California, New York and
Illinois apply existing publicity and biometric law to synthetic voices, and
California and New York extend those rights to deceased performers.
[Holon Law, Synthetic media and voice cloning: right of publicity risk map for 2026](https://holonlaw.com/entertainment-law/synthetic-media-voice-cloning-and-the-new-right-of-publicity-risk-map-for-2026/),
[Cognitive Future, Is AI voice cloning legal: state-by-state guide 2026](https://cognitivefuture.ai/ai-voice-cloning-legal-guide/)

DERIVED, and this is the sentence of the topic: today is 2026-09-14, so the
machine-readable marking obligation described above has been in force for about
six weeks, and this project removed its machine-readable marking in August for
a reason that was correct at the time and was never revisited.

I am not a lawyer and none of the above is a primary legal source. What I can
say precisely is that the allowlist's "keep watermark" is no longer only a
courtesy to Resemble, that the reason to keep it grew stronger while our
implementation of it went away, and that this is a question for a real check
rather than for more research from me.

Also worth carrying: the allowlist already bans Hunyuan3D outputs on a
territory argument, "given Switzerland plus likely EU reach, treat as banned".
The same reach argument applies here, and it applies to a thing we are doing
rather than to a thing we are not.

### 2.3 The watermark is a norm, not a licence condition, and that distinction matters

CITED: Chatterbox is MIT licensed and every output carries Resemble AI's PerTh
(Perceptual Threshold) watermark, described as imperceptible, surviving MP3
compression and common editing, with near-100 percent detection.
[Resemble AI, Chatterbox](https://www.resemble.ai/learn/models/chatterbox),
[ResembleAI/chatterbox on Hugging Face](https://huggingface.co/ResembleAI/chatterbox)

CITED, with the tension recorded rather than resolved: "the watermark exists so
generated content remains attributable, removing it is explicitly against the
intended use", while "a `disable_watermark` parameter appears in development
versions of the code" and the MIT licence itself permits modification.
[resemble-ai/chatterbox issue 142, how to disable or remove the watermark](https://github.com/resemble-ai/chatterbox/issues/142),
[GitHub, resemble-ai/chatterbox](https://github.com/resemble-ai/chatterbox)

DERIVED: MIT does not make keeping the watermark a licence obligation. Our own
allowlist does, by writing "keep watermark" into the ship-safe entry. So the
binding rule here is LEDGER's rule, not Resemble's, and LEDGER's rule currently
has no implementation in the shipped path. A project whose own law is stricter
than the licence, and whose code is looser than its law, has the gap in the
worst of the three places.

### 2.4 Steam's January 2026 clarification puts live voice in its own tier

CITED: Valve clarified the policy on 16 January 2026, "narrowing the disclosure
requirement to player-facing AI content and exempting internal development
tools", replacing the single checkbox with a two-tier classification.
Pre-generated covers anything shipped with the game including voice lines.
Live-generated covers "material a game creates while it is actually running,
such as dynamic NPC dialogue or procedurally voiced characters that respond to
a player in real time", and "because this content is unpredictable, Valve
requires developers to build safety guardrails preventing illegal or offensive
material from appearing".
[StraySpark, Steam's 2026 AI disclosure rules](https://www.strayspark.studio/blog/steam-ai-disclosure-rules-2026-indie-developer-guide),
[IndieForGames, Steam AI disclosure rules 2026](https://indieforgames.com/steam-ai-disclosure-rules/)

DERIVED, and it lands on 1.6: LEDGER is squarely in the live-generated tier,
twice over, once for the dialogue and once for the voice. The guardrail
requirement is a STOREFRONT CONDITION rather than a design preference, and the
project's content rule reaches the crowd generator and neither of the two live
surfaces. This is the same finding an earlier topic in this queue reached from
the text side; the voice side does not change it, it doubles it.

The allowlist anticipated the disclosure half exactly, at PROCESS rule 3:
"Steam generative-AI disclosure for player-facing content (coding tools
exempt)". The exemption clause it names is precisely the one Valve added in
January, which is a point in the allowlist's favour and worth saying.

---

## Part 3. What could not be established

1. **The VCTK licence and consent text as read.** `datashare.ed.ac.uk` is
   egress-blocked. The licence identification in 1.3 is a search summary.
2. **What the VCTK speakers actually consented to.** No source found states the
   consent form's terms. The project's inference from the corpus's purpose is
   reasonable and is not verified.
3. **Whether CC BY attribution for a synthesised voice is satisfied by naming
   the corpus, and where it must appear.** No source found addresses derived
   synthetic voices specifically.
4. **Any primary legal text.** Everything in 2.2 is secondary reporting of the
   EU AI Act and US state law. Dates and obligations should be confirmed
   against the instruments themselves before anything is built on them.
5. **Whether the exported ONNX path COULD carry a watermark.** The watermarker
   is Python post-processing on finished audio; whether it can be applied after
   the C# or C++ decode is an engineering question nobody has asked.
6. **What ElevenLabs' terms say**, which the allowlist admits as a paid-tier
   option. Not examined, because nothing in the project uses it.

---

## Part 4. Findings and interpretation

### Findings

F1. Every voice in the game is VCTK, 110 speakers recorded at Edinburgh CSTR,
and the project's own fetch tool records an incident in which its docstring
named the wrong corpus for months while VCTK was the one in use, corrected
13 August.

F2. VCTK 0.92 is CC BY 4.0, whose one obligation is attribution.

F3. Six `ATTRIBUTION.json` files exist in this repository and all six are 3D or
image content. No shippable file names VCTK, CSTR or Edinburgh.

F4. The mechanical ban on XTTS and F5-TTS lives only in
`tools/meshgen/meshgen.py`; no voice tool imports `banned_hits`. Two TTS models
are refused mechanically by the 3D pipeline and by nothing in the voice
pipeline.

F5. `export_probe.py` installs a `NoWatermark` stub, declares it in the output,
and states explicitly that the shipped path must make its own decision. That
decision has not been made: no watermarker exists in `ledger/Assets/Scripts/`
or `ue-probe/`.

F6. The EU AI Act became fully applicable on 2 August 2026, about six weeks
before this delivery, and secondary sources describe a requirement for
providers to mark AI-generated audio machine-readably.

F7. Keeping the PerTh watermark is Resemble's stated intended use and not an
MIT obligation. It IS an obligation under LEDGER's own allowlist, which writes
"keep watermark" into the ship-safe entry.

F8. Valve's 16 January 2026 clarification creates a live-generated tier
covering runtime NPC dialogue and procedurally voiced characters, and requires
safety guardrails against illegal or offensive output as a condition.

F9. `ResponseValidator` has "two jobs only", length and the fourth wall, and
never calls `ContentRule`. `ContentRule` has three call sites and all three are
crowd and body generation.

### Interpretation

I1. The cheapest fix in this topic is the attribution file. CC BY asks for one
thing, the project already has the file format and a gate that reads it for
props, and the voices are the one asset class with no such file. It costs an
afternoon and it closes a real obligation.

I2. The watermark is the finding with a clock on it. The allowlist told us to
keep it, the export path stubbed it out for a correct and declared reason, the
shipped path never picked the decision back up, and the external reason to keep
it strengthened in August. Whether it can be reapplied after the ONNX decode is
an engineering question that has never been asked, and it should be asked
before it becomes a ship blocker rather than a task.

I3. The guard-reach finding matters more as a pattern than as a risk. This
project's instinct is to make a rule mechanical, and it did: one dictionary,
word-boundary matched, with an accepting-case selftest. It then wired it into
one of two pipelines. That is worth knowing because the next legal rule made
mechanical will be wired the same way unless someone checks the other side.

I4. Where this project is stricter than the law, it should keep saying so out
loud. The consent rule in CLAUDE.md is stricter than CC BY requires and it is
the reason none of this is an emergency: a project that had scraped voices off
the internet would be reading Part 2 very differently. The findings above are
about paperwork and reach, not about the sourcing, and the sourcing is the part
that cannot be fixed afterwards.
