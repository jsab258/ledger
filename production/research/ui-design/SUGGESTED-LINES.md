<!-- Research note, 1 October 2026: written by a separate research helper given the problem (players who use a controller, or will not type, choosing from suggested lines while typing stays; Jafar, 1 October), saved by the design session as returned, apart from this line. -->

# Suggested lines: talking without typing

Research note, 1 October 2026. I worked from the web only, for about 25 minutes, and changed nothing in the repository. The proxy blocked most sites, including Steam's store, community and Steamworks pages, PC Gamer, arXiv's main site, ACM and the review sites. I could open Wikipedia, raw GitHub files, Anthropic's docs and arXiv's export mirror. Anything marked SNIPPET is a search summary I could not open myself. OPENED means I read the page or file directly on 1 October 2026 unless another date is given. My own estimates and advice are marked JUDGEMENT.

## Headlines

- **No shipped AI-conversation game I could find offers a menu of suggested lines alongside free typing.** The shipped games pick one of three routes:
  - voice only (Suck Up!, Covert Protocol, Origins, Whispers from the Star on Steam);
  - typing with a microphone as the second option (Vaudeville, Where Winds Meet, Dead Meat, Mantella);
  - typing only (Uncover the Smoking Gun, the Bannerlord mods).
- **The one close match is a mod.** ImmersiveAI for Bannerlord has a "Think" key (Shift+Enter). The player's own hero drafts one next line from the conversation so far, and the draft goes into the typing box "to keep, change or bin". That is model-written, on request, one line, and editable.
- **The classic lesson is to show the full line, not a paraphrase.** Mass Effect's short wheel labels are criticised because the hero then says something the player did not expect. L.A. Noire renamed its three choices for the same reason in 2017, and critics still found them vague.
- **Typing with a controller is very slow,** about 6 words a minute on an on-screen keyboard against about 38 on a real keyboard. Steam has floating keyboard calls a game can open, and Steam Deck Verified requires the game to open one automatically whenever it needs text.
- **The real risk in LEDGER is a leak.** Suggestions written by the call that plays the character, which can see the character's secrets, would point at those secrets. Suggestions must be written only from what the player himself knows.
- **Suggestions probably reduce typing.** Predictive-text research found that suggested words make people write shorter, more predictable text, and Gmail's Smart Reply was used for 10% of mobile replies. I found nothing published on this for AI-character games.

## 1. Games with free talk to AI characters, and players who can't or won't type

- **Vaudeville** (Bumblebee Studios, released 28 Nov 2025): you type or talk into the microphone. Reviews were mixed to poor: replies wander off the subject, and the microphone sometimes stops being picked up (SNIPPET: game8; The Drastik Measure, 25 Feb 2026). I found no mention of suggested questions.
- **Whispers from the Star** (Anuttacon, 2025): on Steam, players saw only "Click to reply" with a microphone icon and could not type. Several forum threads ask for text input, for accessibility and for quiet rooms. Some sections allow typing and others need speech. I found no suggested replies and no patch adding typing (SNIPPET: Steam discussions, 2025, exact dates not shown).
- **Where Winds Meet** (NetEase; PC, PS5 and mobile, 14 Nov 2025): its "Jianghu Friends" NPCs open a chat box. You type or use the microphone, which turns speech into text. The search summary says you type "instead of choosing from scripted lines", and I found no mention of suggested replies. Players quickly found ways to talk the NPCs into skipping quests. The Steam page has disclosed the AI only since 12 Dec 2025 (SNIPPET: arcanumrpgs, 2026; Notebookcheck). This is the nearest case of free typing on a console controller. I could not see how its PS5 keyboard works.
- **Suck Up!** (Proxima, 2024): microphone, with speech turned into text and sent to GPT. Reviewers say speaking "changes the dynamic completely" (SNIPPET).
- **Dead Meat** (Meaning Machine): voice or keyboard (SNIPPET).
- **Uncover the Smoking Gun** (ReLU/Krafton, 2024): typed questions only, "free input rather than pre-determined options" (SNIPPET).
- **Inworld Origins** and **Covert Protocol** (Inworld with NVIDIA ACE, GDC/GTC March 2024): microphone only. You speak "instead of choosing from a list of preset options". Inworld's documentation recommends push-to-talk (SNIPPET).
- **Mantella** (Skyrim and Fallout 4 mod): built around speech recognition with Whisper or Moonshine (OPENED: GitHub README). Text input is the fallback: turn the microphone off in the mod's menu and press H for a text box (SNIPPET: Mantella docs).
- **Bannerlord mods:**
  - Sinkpoint's AI Dialogue, ChatAi and Inworld Calradia use a typed text box (SNIPPET).
  - ImmersiveAI has the "Think" draft described above. It can be steered by presets: "starter", "romantic", "ender", or the player's own (OPENED: GitHub README; latest commit 30 Sep 2026).
- **AI People** and **NVIDIA ACE game integrations**: not checked, for lack of time.

**Pattern (JUDGEMENT):** the industry's answer for players who don't type has been speech, not suggestions. Every product that is voice-only drew complaints from players who wanted text. Nobody has shipped the mixture of suggestions and free text that LEDGER wants, so there is no proven pattern to copy, and nothing on how many suggestions to show or how long they should be.

## 2. Classic dialogue choices built for controllers

- **Mass Effect** (2007):
  - The wheel's position carries meaning: left continues the conversation, right moves it towards an end, top is polite, bottom is hostile (OPENED: Wikipedia, citing IGN, Jan 2007).
  - The wheel shows "paraphrases of the responses subsequently spoken by the voiced protagonist". It is "criticised for obscuring exactly what the player character will say" (OPENED: Wikipedia, "Dialogue tree").
  - Harvey Randall (PC Gamer, 7 Aug 2025) gives the example "Time to shut you up!", after which Shepard punches a reporter. He compares choosing on the wheel to "pointing a weather vane" (SNIPPET).
  - From memory, not verified: up to six options, and you can choose before the other person finishes speaking.
- **L.A. Noire** (Truth/Doubt/Lie, renamed Good Cop/Bad Cop/Accuse in the 2017 re-release): Push Square called the rename "more fitting", but Nintendo Life and GameSpot found the labels "remained too vague" (OPENED: Wikipedia). The lesson: a label that names the intent, not the words, still surprises players.
- **Disco Elysium**: dialogue is a written list, "conversations in white and choices in orange", with skills cutting in. The Final Cut reached PS4 and PS5 on 30 Mar 2021 and the other consoles on 12 Oct 2021 (OPENED: Wikipedia). The article does not say how the controller moves through the list.
- **Kingdom Come: Deliverance II**: a list of full lines. Cutscene choices carry an hourglass timer, and players made mods to remove the timers in both games, which suggests they annoy at least some players (SNIPPET: Fextralife, Nexus Mods). I could not verify how long the timer runs.
- **Red Dead Redemption 2** (2018): hold the left trigger on a person, then two face-button prompts at a time (Greet or Defuse, and Antagonize), changing with the situation: Threaten, Dismiss, Rob and so on. There are no lines to read (SNIPPET: GameSpot, RDR2.org).
- **A study comparing typing with menus** (Sali, Wardrip-Fruin, Mateas and others, FDG 2010). They built three versions of Façade: typed natural language, a menu of full sentences, and short abstract labels like Mass Effect's (SNIPPET).
  - Full sentences "maximize[d] story involvement".
  - The abstract labels maximised reasoning about the game's workings.
  - 54.3% found typing the most engaging, despite reporting many problems with it.
  - "Changing the dialogue interface produces significant changes in gameplay experience."

**What follows for LEDGER (JUDGEMENT):** show the exact line that will be sent, never a paraphrase or a tone label. Two to four options at once, as the classic games use. No timers, because the player is waiting on a live reply anyway. Move with the stick or d-pad and confirm with one button, plus a fixed button for "say something else" and one for leaving.

## 3. Typing with a controller on PC

- Steamworks offers two calls (OPENED: Steamworks.NET wrapper, built against SDK 1.65):
  - `ShowFloatingGamepadTextInput` "Opens a floating keyboard over the game content and sends OS keyboard keys directly to the game". It is placed so it does not cover the text box, and has single-line, multi-line, email and number layouts.
  - `ShowGamepadTextInput` "Activates the full-screen text input dialog", and the game collects the text afterwards.
  - `IsSteamInBigPictureMode` tells the game when the player is "most likely using a gamepad". The game must be launched through Steam for the overlay to work.
- Steam "strongly recommends (and requires for Verified on Deck badging)" that a game automatically shows the on-screen keyboard whenever it needs text (SNIPPET: Steamworks Steam Deck page). On a Deck, Steam+X opens the keyboard by hand.
- Speed: about 5.8 to 6.3 words a minute with a d-pad or single-stick on-screen keyboard, and 6.4 with a two-stick layout, against about 38 on a real keyboard (SNIPPET: Wilson and Agrawala, Microsoft Research). The year 2006 is from memory.
  - JUDGEMENT: a ten-word line takes about 100 seconds on a pad, against about 15 on a keyboard. That is why controller players need suggestions.
- Not verified: whether Unreal opens Steam's floating keyboard by itself. I assume the game must call it, or draw its own on-screen keyboard when not running under Steam.
- Speech input is the third route the market uses (Where Winds Meet, Mantella's Whisper). It would be new scope for LEDGER.

## 4. Risks of suggestions in an AI-conversation game, and how to avoid them

- **They reveal hidden information.** If the call that plays the character also writes the suggestions, it sees that character's secrets, and the suggestions will drift towards them. The interface rule (show only what the player's own memory holds; the project's ui-design note) applies here.
  - JUDGEMENT: write suggestions in a separate call that is given only the conversation so far and the player's notebook (what Tom knows), never the character's card or private state.
  - Never filter or rank suggestions by whether they would work, since that is a leak too.
  - Suggestions may not name a fact Tom has not learned. The existing invented-facts check could screen them cheaply.
- **They steer towards a "correct" line.** Every list implies an answer. Both the Façade study and the dialogue-wheel complaints show the interface shapes play.
  - JUDGEMENT: at decision points such as an open deal, where a plain "yes" ends it, the game should offer the yes and the no side by side as written lines drawn from the game's state, never from the model. A third line should always keep the talk going without deciding.
- **They repeat.** Generated suggestions tend to converge; Google built diversity into Smart Reply on purpose (OPENED: arXiv abstract, 15 Jun 2016, which names "response diversity" as a challenge).
  - JUDGEMENT: never re-offer a suggestion already shown in this conversation or a line already said, and give each slot a different job: ask or press, something personal or off the subject, and ending the talk.
- **They break immersion.** Wording that sounds modern or American in a 1990 British street breaks the spell. The same voice and period rules as the characters' lines apply, plus the content rules: no alcohol, no gambling, no children.
- **Players stop typing.**
  - Predictive text made captions "shorter" and "more predictable", with "fewer words that the system did not predict" (SNIPPET: Arnold, Chauncey and Gajos, IUI 2020).
  - Smart Reply handled 10% of all mobile Gmail Inbox replies (OPENED: arXiv abstract, 2016).
  - Between people, suspected use of suggested replies made the partner seem less cooperative (SNIPPET: Hohenstein et al., Scientific Reports, Apr 2023). This is only loosely relevant.
  - I found nothing published on players of AI-character games dropping typing when offered suggestions.
  - JUDGEMENT: keyboard players should not see suggestions unless they ask.

## 5. Cost and speed

Prices (OPENED: Anthropic pricing page, read 1 Oct 2026), US$ per million tokens in / out: Haiku 4.5 $1 / $5; Sonnet 5 $2 / $10 (the launch price, now standard).

Starting figures are from the project's own notes, not re-measured: Haiku prompts about 3,200 to 3,600 tokens; a reply about 70 output tokens; Haiku about 0.62 s to first token and 83 tokens a second (Artificial Analysis, read 30 Sep 2026). Prompt caching does nothing on Haiku below 4,096 tokens. Three suggestions of about 12 words, with formatting, come to about 90 output tokens.

All figures below are JUDGEMENT, at 60 lines an hour, on Haiku:

| How | Extra per turn | Extra per hour | Added wait |
|---|---|---|---|
| A. Separate call with the full character context | about $0.004 | about $0.24, roughly doubling the reply's cost | none if run alongside the reply; leaks secrets |
| B. Same call as the reply, suggestions written after the line | about $0.0005 | about $0.03 | none to first words; about 1.1 s more writing after the reply; leaks secrets |
| C. Separate call that sees only what the player knows (about 1,200 tokens in) | about $0.0017 | about $0.10 | none if started when the reply text is final, since it is ready in about 1.7 s while the character is still speaking; about 1.7 s if asked for afterwards, unless fetched ahead |
| D. Written by authors, or picked from the conversation's state (topics Tom knows, open threads, a pending deal) | $0 | $0 | instant |

On Sonnet 5, double the figures for A, B and C. For comparison, the 23 September measurement put live talk at about $0.31 an hour at 60 lines.

Option D costs writing time instead of money and repeats sooner. A mixture is cheapest for what it gives: D for greetings, goodbyes and decisions, C for open questions. Any of these calls also counts against each copy's talk allowance.

## What I could not verify

- Steam's own pages, Steam reviews and forum threads, PC Gamer, the Façade paper's full text, and Whispers from the Star's current version.
- Whether any console AI-chat game (Where Winds Meet on PS5) offers quick replies.
- Mass Effect's option count; KCD2's timer length; how the controller moves through Disco Elysium's list.
- Unreal's handling of Steam's floating keyboard.

## For the owner to decide

1. **Who sees suggestions, and when?** (a) Controller players automatically, keyboard players only when they press a key. **Recommended.** (b) Everyone, always. (c) Only on request.
2. **How are suggestions written?** (a) A mixture: written from the game's state for greetings, goodbyes and decisions; written by Haiku from only what Tom knows for open talk; about $0.10 more an hour. **Recommended.** (b) Haiku with the full character context: about $0.24 an hour, and it risks revealing secrets. (c) Authors only: $0 a turn, a large writing job, repeats sooner.
3. **Do suggestion calls count against each copy's live-talk allowance?** (a) Yes; when the allowance runs out, suggestions fall back to the authored ones. **Recommended.** (b) No, a separate budget.
4. **Speech input (the microphone, as on Steam Deck) as a third route?** (a) Not now, look again after the playable route works. **Recommended.** (b) Now, which is new scope: local speech recognition and its accent testing.

Sources:
- Opened: [Anthropic pricing](https://platform.claude.com/docs/en/about-claude/pricing), [Steamworks.NET isteamutils.cs](https://raw.githubusercontent.com/rlabrecque/Steamworks.NET/master/com.rlabrecque.steamworks.net/Runtime/autogen/isteamutils.cs), [ImmersiveAI README](https://github.com/TraxData313/ImmersiveAI), [Mantella README](https://github.com/art-from-the-machine/Mantella), [Smart Reply (arXiv 1606.04870)](https://arxiv.org/abs/1606.04870), [Wikipedia: Dialogue tree](https://en.wikipedia.org/wiki/Dialogue_tree), [L.A. Noire](https://en.wikipedia.org/wiki/L.A._Noire), [Mass Effect](https://en.wikipedia.org/wiki/Mass_Effect_(video_game)), [Disco Elysium](https://en.wikipedia.org/wiki/Disco_Elysium).
- Search summaries only: [PC Gamer, Randall](https://www.pcgamer.com/games/rpg/the-dialogue-wheel-was-the-worst-thing-to-happen-to-rpgs-its-robbed-us-all-for-years-and-im-glad-its-dying-out/), [Whispers from the Star threads](https://steamcommunity.com/app/3730100/discussions/0/608668111724477736/), [Where Winds Meet AI](https://arcanumrpgs.com/blog/where-winds-meet-ai/), [Vaudeville review](https://www.thedrastikmeasure.com/2026/02/25/vaudeville-pc-review/), [Playing with words (FDG 2010)](https://dl.acm.org/doi/10.1145/1822348.1822372), [Predictive text encourages predictable writing](https://hci.seas.harvard.edu/publications/predictive-text-encourages-predictable-writing), [Hohenstein et al. 2023](https://www.nature.com/articles/s41598-023-30938-9), [Steam Deck recommendations](https://partner.steamgames.com/doc/steamdeck/recommendations), [dual-joystick text entry](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/10/Text-Entry-Using-a-Dual-Joystick-Game-Controller.pdf), [RDR2 interactions](https://www.gamespot.com/articles/in-red-dead-redemption-2-you-can-talk-your-way-out/1100-6461058/), [Covert Protocol](https://www.digitaltrends.com/computing/nvidia-ai-demo-gtc-2024/), [Mantella text input](https://art-from-the-machine.github.io/Mantella/pages/issues_qna.html), [Bannerlord AI mods](https://www.nexusmods.com/mountandblade2bannerlord/mods/10653), [KCD2 no-timer mod](https://www.nexusmods.com/kingdomcomedeliverance2/mods/3268).
