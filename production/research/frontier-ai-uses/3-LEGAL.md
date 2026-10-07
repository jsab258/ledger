# 3. The legal position, plainly

**This is not legal advice.** It was compiled by a research helper, not a lawyer, and checked here only where a primary text could be read.

**Unreached:** every legislation and court site (fedlex, legislation.gov.uk, EUR-Lex, Cornell, BAILII, curia), Steamworks, and the Unreal EULA page. So the statute wording below comes from search summaries [SS] or from Wikipedia [W]. The Unreal, Fab, Adobe and Anthropic clauses come from LEDGER's own terms note, read from his PC on 3 October (production/research/terms-2026-10-03). Anything that matters should be checked against the official text by a lawyer.

The full note is notes/HF-legal.md.

## The rule of thumb

1. **Playing, watching, measuring, screenshotting for your own notes, and reading what developers have published (talks, papers, documentation, Unreal's own licensed source) is lawful everywhere.** This is how studios learn from each other.
2. **Do not decompile, disassemble, unpack or rip another game or engine to learn how it is made, or to take anything from it.** The legal exceptions in Europe are narrow [SS]:
   - decompiling to make one program work with another (interoperability);
   - correcting errors in software you are entitled to use;
   - observing, studying and testing a program while running it normally, to find the ideas and principles behind it.

   The third is why playing a game to see how it lights a street is lawful. Unpacking its files or decompiling it to see how is not covered by any of the three.
3. **Ideas, mechanics, rules and genres are free. Code, art, models, textures, animations, sounds, text, characters, names and a distinctive look are not.**
4. **Patents are the exception to "ideas are free".** A patented mechanic cannot be used even if invented independently. A clean room does not help against a patent.
5. **Never put another game's code or art into an AI to "rewrite" it.** A model that has read the code is not a clean room. In March 2026 the chardet library was rewritten by an AI and relicensed; its author and the Free Software Foundation objected that it was not clean [SS].

## By country

| | Decompiling another game | Contract bans in its EULA | Breaking copy protection or anti-cheat |
|---|---|---|---|
| **Switzerland** (where Jafar lives and works) | Allowed only to get interface information for interoperability (URG Art. 21) [SS]. Unfair-competition law separately forbids taking another's market-ready product by technical copying (UWG Art. 5 lit. c) [SS]. | Whether a EULA can override Art. 21 is **open** [SS] | Forbidden, except to make a use that is itself lawful (URG Art. 39a para. 4) [SS]. Decompiling to learn techniques is not such a use [I]. |
| **UK** | Allowed only for interoperability (CDPA s.50B); observing, studying and testing is allowed (s.50BA) [SS] | Void only against those narrow acts (s.296A) [SS]; it stands for everything else | Forbidden (from memory; text UNREACHED) |
| **EU** | Allowed only for interoperability (Directive 2009/24/EC art. 6); observe, study and test (art. 5(3)) [SS]. *SAS v World Programming* (CJEU, 2 May 2012): a program's functionality is not protected [SHOWN, Wikipedia]. | Void only against those acts (art. 8) [SS] | Forbidden |
| **US** | Intermediate copying for compatibility was fair use (*Sega v. Accolade*, 1992; *Sony v. Connectix*, 2000) [SHOWN, Wikipedia]. Neither case allows the copied material into the product. | **Enforceable even against fair use** (*Bowers v. Baystate*, 2003; *Davidson v. Jung*, 2005) [W] | Forbidden by DMCA §1201 (*MDY v. Blizzard*, 2010) [W]; about US$14.47 million against a cheat maker (*Activision v. EngineOwning*, 2024) [SS] |

For LEDGER, this settles the brief's question in practice.
- **In Switzerland, the UK and the EU,** no exception covers decompiling another game to learn its methods [SS].
- **In the US,** fair use has allowed disassembly to reach unprotected ideas where there was no other way (*Sega v. Accolade*) [SHOWN, Wikipedia]. But a game's licence can forbid it, and US courts have enforced such terms (*Bowers v. Baystate*) [W]. Game licences usually do forbid it [I].
- **Anywhere,** any protection broken is a further offence.
- **The same holds when an AI does the decompiling.** Uploading another company's program to a cloud model is itself a copy, and usually a licence breach [I].

LEDGER is made in Switzerland and sold in Europe, so that route is closed, and it is safe nowhere.

The mods and mashups of September 2026 (1-WHAT-IS-NEW.md, 1.2) move other publishers' code, behaviour and assets into another game. **They are not a route for LEDGER in any form.**

## Using what is learned

- **Allowed:** what anyone can see by playing, what developers published, and Unreal's own source under its licence. Build the result with LEDGER's own code and assets. No clean room is needed, because nothing protected was taken.
- **Not allowed:** any of their code, data tables, written lines, models, textures, animations or sounds. Nor a look so close that a screen could be mistaken for theirs.
  - *Tetris v. Xio* (2012) found the copied look of Tetris infringing [W].
  - Trade dress, UK passing off and Swiss UWG Art. 3(1)(d) all protect against confusion [SS].
- **LEDGER's references:** the KCD2 frames and the Hook sheet may be used for comparison, by people or models. They must never be fed to a generator, traced or shipped [I].
- **Patents.** Warner Bros' Nemesis patent, US 10,926,179, granted 23 February 2021, is reportedly in force until about 2035 [SS]. It covers characters who remember the player inside a combat hierarchy (nemeses, forts, vendettas, followers).
  - LEDGER's townspeople, who remember and gossip, are in the same broad territory, though the reported claims look far from a gossiping street [I].
  - Nintendo's mechanic patents against Palworld show such patents are enforced in Japan. In the US one was rejected on re-examination, not yet finally [SS].
  - **Only a patent attorney's reading of the claims settles freedom to operate. That costs money, so it is his decision.**

## AI points that matter to a sold game

| Point | What is known | Mark |
|---|---|---|
| Copyright in AI-made material | US: none without a human author. *Thaler* cert. denied 2 March 2026; the Copyright Office says prompts alone are not enough (29 Jan 2025). UK: s.9(3) still protects computer-generated works, but the government proposed its repeal on 18 March 2026. Switzerland: only human creations are protected. | [SS] |
| What stays protectable in LEDGER | His selection, arrangement and editing; human-written canon and story; the assembled game. LEDGER's records (DECISIONS.md, approval pages) document those human choices. | [I] |
| Training-data court decisions, July to October 2026 | *Thomson Reuters v. Ross*: training was not fair use, affirmed by the Third Circuit on 29 Sep. *Doe v. GitHub* (9th Cir., 16 Sep): AI code output is not a stripped copy under the DMCA. *GEMA v. Suno* (Munich, 31 Jul): infringement. *Bartz v. Anthropic* settlement approved. *Getty v. Stability* (UK): appeal permitted, no hearing found. | [SS]; court sites UNREACHED |
| **The live talk's own risk** | Whoever publishes AI output carries its risk, and in live talk that is the game. Munich found memorised song lyrics reproduced on request infringing (GEMA v. OpenAI, Nov 2025). **A 1990 British setting invites characters to quote lyrics.** | [SS]; the risk [I] |
| Model licences | Anthropic: the customer owns outputs, with an IP indemnity (Commercial Terms) [SHOWN]. Chatterbox: MIT, with a watermark in every output [SHOWN]. **FLUX.1 [dev]: model use non-commercial only, so out** [SHOWN]. **Hunyuan3D, HY-World, HY-Motion: their licences exclude the EU and UK, including use of their output, so out** [SHOWN]. | |
| **Telling players they talk to an AI** | Anthropic's usage policy: interactive AI agents "must disclose to users that they are interacting with AI ... at a minimum at the beginning of each chat session" [SHOWN]. EU AI Act Art. 50(1) reportedly applies from 2 August 2026. Commission guidelines of 20 July 2026 reportedly exempt game characters only where their AI nature is obvious to every player [SS]. LEDGER's photoreal voiced characters make that arguable. His ruling of 24 September already puts the AI notice before the first talk. | [SHOWN] Anthropic; [SS] the AI Act |
| Steam | Since 16 January 2026, AI used only as a development tool needs no disclosure. Content players see, and live-generated content with a description of its guardrails, still does [SS]. LEDGER's claim check and content rules answer the guardrail question. | [SS] |
| The Unreal and Mixamo licences | Unreal, 6(e): the engine may not be training input to a generative AI, nor prompt input to one that trains on its input; MetaHumans may not be used to build a database for an AI, or to train or test one. Adobe (Mixamo), 17(C): nothing from its services may be used to create, train, test or improve an AI. Anthropic's consumer terms let Max users opt in to training [SHOWN]. **The "Help improve Claude" setting must be off**, as he ruled on 3 October. | LEDGER's terms note, read from his PC on 3 October; the EULA page unreached from the cloud |
| The title | **"LEDGER" is also the name of a well-known hardware-wallet company that sells software** [I]. Search the Swiss, EU, UK and US trade-mark registers before any store page. | [I] |

## What follows for LEDGER (none of it changes a rule here)

1. Learn from other games only by playing, watching and reading what they published. Never decompile or rip them, or feed their material to a model. Attaching a frame-capture tool to another game is left out too: the cautious line, since whether it counts as "observing" was not checked [I].
2. **The AI notice already appears before the first conversation of each launch.** The game holds the flag only for the run (CrimeProbe.cpp, `bNoticeShown`, read here). That likely meets Anthropic's "beginning of each chat session" and the AI Act. Whether each separate conversation counts as a "session" is one of the questions for the lawyer in point 5.
3. **Canon already forbids real lyrics.** No line about them was found in the talk program, so proof 4 (4-FIVE-PROOFS.md) tests whether live talk keeps to it.
4. **Keep out every model whose licence is non-commercial, territory-limited, or trained on NoAI-tagged data:** FLUX.1 [dev], the Hunyuan family, HY-Motion, Lyra and the SMPL-based motion models. Objaverse-trained 3D generators raise the NoAI question; the allowlist lists TRELLIS 2 as MIT, so that entry is his to re-read before image-to-3D returns.
5. **Money, his decision:** before release, one review by a Swiss IP lawyer covering the title search, a reading of the Nemesis patent's claims, and the store, AI Act and privacy notices.
