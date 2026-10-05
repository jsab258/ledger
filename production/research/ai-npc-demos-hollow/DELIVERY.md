# Topic 5: why the AI NPC demos of 2023 to 2026 felt hollow

STATUS: SPEC (research delivery). Branch `research/ai-npc-demos-hollow`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged: no
external page was read in full; every external citation is the search channel's
summary of a named page. Repository claims name their file and line and were
produced by commands run this session.

## 1. Why this topic is different from the others in my queue

Every other topic asks what somebody else did well. This one asks what everybody
did badly, in the exact thing LEDGER's second pillar promises. The brief's
framing is right and worth keeping in front of the reader: **we are building the
thing they promised.**

So the useful output is not a list of criticisms. It is a list of FAILURE MODES
with a check against our own code, and section 5 is where that stops being
comfortable.

## 2. The five failure modes, and what each one actually is

### 2.1 They talk without saying anything

CITED (search summary of PC Gamer, "MMO life sim Seed's AI-powered avatars prove
once again that nothing shatters immersion quicker than crappy chatbot
dialogue"): "AI-powered NPCs can talk and talk and talk, that's for damn sure.
But they're not saying anything worth listening to."

CITED (search summaries of Engadget, "NVIDIA's AI NPCs are a nightmare", and
Kotaku, "AI Video Game Characters Seem As Soulless As You'd Expect"): the
dialogue is "stiff, robotic, and hollow, reminding critics more of an automated
voice mailbox message than an actual human", and the generated lines "sound like
they're being read from a parody book of cyberpunk and detective genre cliches".

DERIVED: this is the volume failure. An LLM given an open brief produces
plausible, fluent, generic speech, and fluency is not information. The
criticism is not that the lines are badly written; it is that nothing in them is
NEWS.

### 2.2 They are reactive, deferential, and will not push back

CITED (search summary of Engadget and Gizmodo, "These Nvidia AI NPCs Are Just as
Obnoxious as Real Players"): "The NPCs are reactive to player questions, not
proactive, and are completely deferential to players' demands. NVIDIA's public
pitch is that they won't demonstrate more antagonistic behavior."

**This is the sharpest of the five and the easiest to miss, because it is a
choice rather than a limitation.** A vendor selling NPC technology to studios
cannot ship a character who refuses, lies, or takes against you, because a demo
that goes wrong is a demo that does not sell. So the category-defining product
has a category-defining hole in it, and the hole is exactly the part that would
make a character feel like a person.

### 2.3 A single wrong syllable destroys the illusion instantly

CITED (search summary of the same PC Gamer piece on Seed): "Seed's tutorial bot
will sometimes mispronounce a common word or stress the wrong syllable, which is
immediately immersion-breaking because it's an instant reminder that you're
seeing or hearing something fake, an uncanny valley thing."

DERIVED, and it matters to us more than to any of them: this is a
LATENCY-AND-VOICE failure, not a writing failure, and it is asymmetric. A
thousand correct lines buy nothing; one wrong stress costs the illusion. Topic 1
treated the voice pipeline as a latency problem. This says the quality floor is
at least as load-bearing as the speed floor, and that a fast pipeline that
mispronounces is worse than a slow one that does not.

### 2.4 Personality with no mechanical consequence reads as no personality

CITED (search summary of PC Gamer's report on an inZOI player survey): among the
game's biggest problems, "characters often freeze and feel lifeless, and
relationships grow through spammed identical dialogues with personality having no
impact".

DERIVED: this is the one that indicts the architecture rather than the writing.
If what a character says does not change what the game DOES, then the generative
layer is decoration over a relationship meter, and players find the shortest path
to the meter. Which is precisely the dominant-strategy failure that game 5 of the
coverage audit found in Shadows of Doubt from a different direction.

### 2.5 Players will immediately try to break it, and succeed

CITED (search summary of PC Gamer, "Wuxia MMO Where Winds Meet is full of AI
chatbot NPCs, and people are doing all the standard obscene stuff to them"): a
quoted player, "I made him think that my character was pregnant with his child".

DERIVED: an open conversational surface is a surface players will probe until it
does something absurd, and they will screenshot the absurd thing. This is not a
moral point, it is a design one: the failure is that the world ACCEPTED the
absurdity, which means the conversation had authority it should not have had.
Section 4 is why LEDGER is unusually well defended here and section 5 is where it
is not.

## 3. The reception numbers, because they bound how much benefit of the doubt exists

CITED (search summary of Quantic Foundry, "Gamers Are Overwhelmingly Negative
About Gen AI in Video Games", December 2025): negative sentiment at **77 to 83
percent**, and the study's own note that "this highly-skewed negative response is
rare in years of survey research among gamers".

CITED (search summaries of the GDC 2026 State of the Game Industry coverage and
Game Developer): **52 percent** of game industry professionals think generative
AI is having a negative impact, up from 30 percent the previous year and 18
percent the year before; the most unfavourable groups are visual and technical
art (64 percent), game design and narrative (63 percent) and programming (59
percent). Generative AI USE among developers fell to **29 percent in 2026**.
CITED (GamesIndustry.biz survey, relayed): **88.4 percent** of industry workers
think any use of generative AI should be declared on storefronts.

DERIVED, and it is the strategic fact of this topic: **the audience is not
neutral and is getting less neutral.** LEDGER's second pillar is the thing that
77 to 83 percent of players say they do not want, and the project's own standing
order is "we don't ship low quality / AI slop here". Those two sentences have to
be reconciled by the work, and the only reconciliation available is that the
thing is actually good, because there is no goodwill to borrow.

NOT ENUMERATED, and I want to be fair rather than only alarming: the same
searches surfaced claims that hybrid approaches (human-authored foundations with
generative layers) are what is now working, and one product, Status by Wishroll,
reported at 2.5 million registered users averaging 90 minutes a day. HOLE: those
claims come from AI-industry-adjacent sources rather than from critics or
surveys, and I have weighted them accordingly and not built anything on them.

## 4. What LEDGER already does right, and it is most of it

This is not reassurance. Each is a specific structural defence against a
specific failure mode above, and each is readable in the repository.

**Against 2.1 (talk without news):** the architecture forbids open generation.
Pillar 2: "Conversation always matters: outputs are classifications and
closed-set choices that deterministic Core executes." Pillar 3: "LLMs classify,
never adjudicate." A character who can only say things the simulation licenses
cannot produce plausible nothing, because there is nothing plausible for it to
say. `ledger/Assets/Scripts/Core/ConversationEngine.cs` builds the system prompt
from the card and the scene, and `Core/IntentRouter.cs` and
`Core/ResponseValidator.cs` sit either side of it.

**Against 2.2 (deferential):** `Core/Homicide.cs` states the opposite position
in as many words, about a killing: "whether they will still say so is nobody's,
a killing cannot be bought or scared quiet". The inventory's tile "recognition
and confrontation" names a stance ladder and a standoff.
`Core/Observation.cs`'s `Awareness` enum has a state documented as "They know you
saw them, and you do not. The worst one, and the game must allow it." A design
that writes that sentence down is not going to ship a deferential NPC.

**Against 2.4 (personality with no consequence):** this is the whole moat. D11
forbids a global credibility number precisely so that what a character believes
is per-person and mechanical, and D12 requires that a judgement surface the
memory behind it.

**Against 2.5 (players breaking it):** the closed-set architecture again. A
player cannot make an NPC believe an absurdity if the NPC's beliefs are rows in
a memory store written by a deterministic Core, and the conversation is a
classifier over them. This is the single strongest structural argument the
project has, and I do not think it has ever been written down as one.

**Against 2.3 (a wrong syllable):** nothing structural. It is a quality floor on
the voice pipeline, and topic 1 is where it lives.

## 5. Where we are not defended, measured this session

Two findings. The second is a shipping requirement.

### 5.1 The two symptoms we have already measured in ourselves

The inventory records, in its own typed notes:

- "in 90 of 90 caught lies not one spoken line differed", and "Truth and silence
  both end at suspicion 0.060, so honesty pays nothing" (tile: the player's
  claims and lies).
- "every recognition beat measured sat below the rung at which anybody comments,
  1944 of 1944, so nobody says a word to you" (tile: recognition and
  confrontation).

DERIVED, and it is uncomfortable: the first is failure mode 2.4, personality
without mechanical consequence, stated in our own numbers. The second is failure
mode 2.1's twin, a world that has the information and says nothing with it. The
architecture that defends against these failures is right; the current build
exhibits them anyway, and it exhibits them measured, which is better than
inZOI's position and not different in kind.

The coverage audit's Disco Elysium delivery already recommended the fix for the
first (failure producing content rather than a refusal). This topic is the second
independent reason for it.

### 5.2 The live output path has no D18 enforcement, and Steam will ask

MEASURED THIS SESSION, by grep and by reading:

- `Core/ResponseValidator.cs`'s own header says its scope: "Two jobs only, keep
  replies conversation-sized (truncate at a sentence boundary), and never let a
  character break the fourth wall". A grep for `ContentRule`, `D18`, `slur`,
  `forbidden` and `banned` in that file returns nothing.
- It has exactly one caller: `Game/ConversationHost.cs:149`.
- `Core/ContentRule.cs` is D18's "ONE ENFORCEMENT SITE THAT IS CODE", and its
  header says why it exists: "a crowd that samples ages cannot be allowed to
  sample a child [...] a generator has to be UNABLE to produce the thing". Its
  three call sites are `Game/RealBody.cs:501` (an underage model check on a mesh
  stem) and `Core/Population.cs:177` and `:186` (trade screening). All three are
  the crowd generator. None is dialogue.
- `tools/content-gate.py` walks repository files by glob. It is a build-time gate
  over authored corpora, not a runtime path, and `canon.md` describes it as "over
  dialogue and spoken lines", which is the authored ones.
- A grep of `Core/ConversationEngine.cs` and `Core/CharacterCard.cs`, the two
  files that build the system prompt, for content-clause words (never say, do
  not say, slur, swear, children, alcohol, drink) returns nothing.

**So a live generated line passes a length check and a fourth-wall check and
reaches the player.** D18's clauses (no slurs of any kind, no children anywhere,
no sexual content, alcohol and gambling out entirely, drugs never a player verb)
are enforced at five sites, and none of the five is on this path.

BOUNDED HONESTLY, because this is a serious claim: I grepped two files for
content words and read one validator and one rule file. I did not read the
system prompt's assembled output, and a prompt fragment could live somewhere I
did not look. What I establish is that no D18 PREDICATE is called on the output
path and no content clause appears in the two files that build the prompt. A
prompt instruction would in any case be a soft guard, and `Core/ContentRule.cs`'s
own header is the argument against relying on one: a generator "has to be UNABLE
to produce the thing".

**AND IT IS NOW A STORE REQUIREMENT.** CITED (search summaries of KitGuru, AI
Trace's Valve entry, IndieForGames and BigGo on the January 2026 update): Steam
requires disclosure of AI-generated content that "ships with your game, and is
consumed by players", splitting it into "Pre-Generated" and "Live-Generated";
the January 2026 rewrite exempted development tools and narrowed the focus to
player-facing content; live-generated adult content is banned entirely; and
**"developers using AI to generate content during gameplay must describe their
safeguards to prevent illegal/inappropriate output, with failure resulting in
removal from Steam."** AI disclosure now appears on around 20 percent of Steam
games.

DERIVED: LEDGER is a Live-Generated case by definition. The allowlist's process
section already anticipates the disclosure ("At ship-prep: Steam generative-AI
disclosure for player-facing content"). What it does not anticipate is that the
disclosure requires a DESCRIBED SAFEGUARD, and the safeguard has to exist to be
described. This moves a D18 completeness question from a design concern to a
storefront condition, and it is the most concrete deadline-shaped fact in my
queue so far.

## 6. Recommendation

1. **Write the structural defence down.** Section 4's argument (a closed-set
   architecture cannot produce plausible nothing and cannot be talked into an
   absurdity) is the project's best answer to the 77-to-83-percent problem, and
   it is currently implicit across three pillars and a decision record. If
   anybody ever has to explain in public why this is not the thing players hate,
   that paragraph is the explanation.
2. **Treat 5.2 as a gap with a deadline rather than a design note.** Not because
   it is urgent today, but because it is the one thing in my queue that a third
   party will eventually check.
3. **Add a quality floor to the voice work, alongside the latency floor.** 2.3
   says one wrong stress costs more than a hundred right lines buy. Topic 1 sized
   the speed; nothing sizes the correctness.
4. **Read the Steam review paper.** arXiv 2608.11539, "Player Perceptions of
   Generative AI in Games: A Steam Review Analysis", is the only primary study I
   found on what players actually say in reviews rather than in surveys, and it
   is egress-blocked from here.

## 7. What could not be established

1. **The arXiv Steam review study** (2608.11539). Blocked. It is the best
   available evidence on this topic and I could not read it.
2. **Whether any prompt fragment carries D18 clauses**, beyond the two files I
   grepped (5.2's stated bound).
3. **The positive cases.** The claims about hybrid approaches working, and the
   Status by Wishroll figures, come from AI-industry-adjacent sources rather than
   from critics or surveys. I have not relied on them and a proper pass would
   need better sources.
4. **Whether the reception numbers move with framing.** Every survey quoted asks
   about "generative AI in games" as a category. Nobody has asked players about a
   specific well-executed implementation, so the 77 to 83 percent is a measure of
   the category's reputation and not necessarily a prediction about one game.
   That distinction matters and I cannot close it.
5. **Ubisoft's Teammates**, the 2025 successor to NEO NPC, appeared in searches
   and was not examined.
6. **Where Winds Meet's** actual scale and reception beyond the one quoted
   article.

## 8. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Engadget, "NVIDIA's AI NPCs are a nightmare", https://www.engadget.com/gaming/pc/nvidias-ai-npcs-are-a-nightmare-140313701.html
- Kotaku, "AI Video Game Characters Seem As Soulless As You'd Expect", https://kotaku.com/nvidia-convai-ai-video-game-npc-characters-tech-demo-1851181329
- Gizmodo, "These Nvidia AI NPCs Are Just as Obnoxious as Real Players", https://gizmodo.com/these-nvidia-ai-npcs-are-just-as-obnoxious-as-real-players-2000550516
- Game Developer, "Is NVIDIA's AI-driven NPC tech just really expensive improv?", https://www.gamedeveloper.com/audio/is-nvidia-s-ai-driven-npc-tech-just-really-expensive-improv-
- Aftermath, "AI NPCs Have Potential, But Not The Kind Big Video Game Companies Want", https://aftermath.site/ai-npcs-nvidia-unity-ubisoft-convai-inworld/
- Laptop Mag, "Why Nvidia's big bet on AI NPC's has me unconvinced", https://www.laptopmag.com/laptops/gaming-laptops-pcs/nvidia-ai-npc-gaming-chatbot-
- PC Gamer, "MMO life sim Seed's AI-powered avatars prove once again that nothing shatters immersion quicker than crappy chatbot dialogue", https://www.pcgamer.com/games/sim/mmo-life-sim-seeds-ai-powered-avatars-prove-once-again-that-nothing-shatters-immersion-quicker-than-crappy-chatbot-dialogue/
- PC Gamer, "Wuxia MMO Where Winds Meet is full of AI chatbot NPCs", https://www.pcgamer.com/games/rpg/wuxia-mmo-where-winds-meet-is-full-of-ai-chatbot-npcs-and-people-are-doing-all-the-standard-obscene-stuff-to-them-i-made-him-think-that-my-character-was-pregnant-with-his-child/
- PC Gamer, "Inzoi's biggest problems right now are overwhelmingly the fact it's lacking simulation content and its painfully awkward social interactions, player survey reveals", https://www.pcgamer.com/games/life-sim/inzois-biggest-problems-right-now-are-overwhelmingly-the-fact-its-lacking-simulation-content-and-its-painfully-awkward-social-interactions-player-survey-reveals/
- PC Gamer, "The bigwigs who want AI-generated NPCs and writing think you're too dumb to appreciate a good story", https://www.pcgamer.com/gaming-industry/game-development/the-bigwigs-who-want-ai-generated-npcs-and-writing-think-youre-too-dumb-to-appreciate-a-good-story-dont-prove-them-right/
- Ubisoft, "NEO NPC" press release (GDC 2024), https://staticctf.ubisoft.com/8aefmxkxpxwl/Mw2s4KjssknqHHh1VIf8V/720296810ecc3deae51778a219732c7f/PRESS_RELEASE_GDC_UbisoftUnveilsNEONPC_190324.pdf
- Ubisoft News, "How Ubisoft's New Generative AI Prototype Changes the Narrative for NPCs", https://news.ubisoft.com/en-us/article/5qXdxhshJBXoanFZApdG3L/how-ubisofts-new-generative-ai-prototype-changes-the-narrative-for-npcs
- AI and Games, "Ubisoft's Teammates Demo and Their New Generative AI Push", https://www.aiandgames.com/p/ubisofts-teammates-demo-and-their
- Quantic Foundry, "Gamers Are Overwhelmingly Negative About Gen AI in Video Games", https://quanticfoundry.com/2025/12/18/gen-ai/
- GDC, "GDC 2026 State of the Game Industry Reveals Impact of Layoffs, Generative AI, and More", https://gdconf.com/article/gdc-2026-state-of-the-game-industry-reveals-impact-of-layoffs-generative-ai-and-more/
- Game Developer, "One third of game workers using genAI, but half think it's bad", https://www.gamedeveloper.com/business/one-third-of-game-workers-use-generative-ai-but-half-think-it-s-bad-for-the-industry
- 80.lv, "GDC Survey Says Over 50% Of Game Devs See Gen AI As Harmful", https://80.lv/articles/gdc-survey-over-50-of-game-devs-say-generative-ai-harms-industry
- Outlook Respawn, "Generative AI Use Among Game Developers Falls to 29% in 2026", https://respawn.outlookindia.com/gaming/gaming-news/survey-indicates-falling-generative-ai-use-among-game-developers
- arXiv 2608.11539, "Player Perceptions of Generative AI in Games: A Steam Review Analysis", https://arxiv.org/pdf/2608.11539 (EGRESS BLOCKED)
- KitGuru, "Steam updates its gen-AI disclosure policies", https://www.kitguru.net/desktop-pc/mustafa-mahmoud/steam-updates-its-gen-ai-disclosure-policies/
- AI Trace, Valve disclosure practice entry, https://www.aitrace.org/company/valve/practice/e62f0dfa-ea81-47ca-98d5-ffbab5fd6814
- IndieForGames, "Steam AI Disclosure Rules 2026: What You Must Declare", https://indieforgames.com/steam-ai-disclosure-rules/
- BigGo Finance, "Valve Clarifies Steam's AI Disclosure Rules: Focus Shifts to Player-Facing Content, Not Dev Tools", https://finance.biggo.com/news/202601171220_Steam_AI_Disclosure_Update_Focuses_on_Player_Content
- tech-insider, "Steam AI Disclosure Hits 20% of Games as Rivals Skip", https://tech-insider.org/steam-ai-disclosure-2026/

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Core/ResponseValidator.cs`, `Core/ContentRule.cs`,
`Core/ConversationEngine.cs`, `Core/CharacterCard.cs`, `Core/Homicide.cs`,
`Core/Observation.cs`, `Core/Population.cs`, `Game/ConversationHost.cs`,
`Game/RealBody.cs`, `tools/content-gate.py`, `canon.md`,
`ledger-v2/respec/vision-pillars-v2.md`,
`ledger-v2/research/license-allowlist.md`, `production/systems-inventory.json`,
`ledger-v2/respec/decision-register/D11-player-progression.md` and
`D12-information-surfaces.md`.
