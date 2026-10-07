> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand F: the legal position for LEDGER (reverse engineering, using what is learned, AI, mashups)

Written 7 October 2026 by a research helper. **I am not a lawyer and this is not legal advice.** It is a map of the law as far as I could check it in about thirty minutes, so that Jafar knows which questions are settled, which are open, and which ones are worth paying a Swiss IP lawyer to answer before release.

## How to read this

Marks follow the common brief:
- [SHOWN]: I read the primary text myself (a licence file, Anthropic's own terms page, or a Wikipedia article's text).
- [W]: a Wikipedia article read through a summarising fetch. I did not see the whole text.
- [SS]: a search summary only. It is a lead, not evidence.
- [I]: my own inference.
- "from memory": background I did not check in this session.
- UNREACHED: the source could not be opened.

**Unreached (all blocked by the network proxy):** every legislation site (fedlex.admin.ch, legislation.gov.uk, EUR-Lex, Cornell LII, copyright.gov), court and judgment sites (judiciary.uk, BAILII, curia, CourtListener), Steamworks documentation (partner.steamgames.com), unrealengine.com (the Unreal EULA), lawbrary.ch, droit-bilingue.ch, and all law-firm and press pages. The statutory wording below therefore comes from search summaries or memory. It was not read from the official text, and anything that matters should be checked against that text by a lawyer. Wikipedia's API rate-limited me after a few articles, so several Wikipedia pages were read only through the summarising fetch.

---

## The short answer (rule of thumb)

1. **Watching, playing, measuring, screenshotting for your own notes, reading developers' talks, papers and documentation is always fine.** This is how professionals learn from other games, and no law in Switzerland, the UK, the EU or the US stops it.
2. **Do not decompile, disassemble, unpack or rip another commercial game or engine to learn how it is made.** The narrow legal exceptions cover interoperability (making your program work with theirs), error correction in software you own, and "observing, studying and testing" while running it normally. "Learning their lighting or animation tricks for my own game" is none of these. EULAs, anti-tamper and anti-cheat add contract and anti-circumvention liability on top.
3. **Ideas, mechanics, rules, genres and methods are free to use. Code, art, models, textures, animations, sounds, text, characters, names, logos and a game's distinctive look are not.** Patents are the exception to "ideas are free". A patented mechanic cannot be used even if you invented it yourself.
4. **Never copy another game's code or assets, and never feed them to an AI to "rewrite" them.** An AI that has seen the code is not a clean room (the chardet dispute, March 2026).
5. **AI specifics for a game that will be sold:**
   - Read every model licence for commercial use, an output clause and a territory clause.
   - Assume purely AI-made material has thin or no copyright, so record the human choices.
   - Disclose AI use on Steam, including the live talk.
   - Tell players the characters' talk is AI-generated. Anthropic's usage policy already requires this, and the EU AI Act has applied since 2 August 2026.

---

## 1. Decompiling or reverse-engineering other games and engines

### 1.1 Switzerland (where Jafar lives and where his acts take place)

**Art. 21 URG (Copyright Act of 9 October 1992), "decoding" (decompiling) computer programs** [SS; official text UNREACHED]:
- Para. 1: anyone entitled to use a program may decode the code, or have a third party decode it, to obtain the *necessary information about interfaces* to independently developed programs.
- Para. 2: the information may be used *only* to develop, maintain and use *interoperable* programs, and only so far as this does not unreasonably harm the program's normal exploitation or the rights holder's legitimate interests.
- The Copyright Ordinance (URV) defines "necessary interface information" as information that is indispensable for interoperability and not readily available to the user [SS].
- Sources (leads): https://www.droit-bilingue.ch/en-de/2/23/231.1-21-25.html, https://lawbrary.ch/law/art/URG-v2022.01-en-art-21 (both UNREACHED).

**Art. 39a URG, technical protection measures** [SS]:
- Effective technical measures may not be circumvented.
- **Para. 4 says the ban cannot be enforced against someone who circumvents solely to make a legally permitted use.** This is a Swiss peculiarity, wider than UK, EU or US law.
- It does not turn a non-permitted use (for example, decompiling to learn techniques) into a permitted one [I].
- Leads: https://lawbrary.ch/law/art/URG-v2023.07-en-art-39a, https://www.netzwoche.ch/news/2014-01-31/urg-drm-darf-fuer-eigengebrauch-umgangen-werden (UNREACHED).

**Unfair Competition Act (UWG)** [SS]:
- Art. 5 lit. c forbids taking over and exploiting another's *market-ready work product* "by technical reproduction processes without reasonable effort of one's own". Search summaries name a computer program as an example. This catches asset ripping and code lifting even where copyright might be argued.
- Art. 3 para. 1 lit. d forbids creating a risk of confusion with another's goods or works. It is the Swiss counterpart of trade dress and passing off (see part 4).

**Open questions:**
- Whether a EULA can validly forbid what Art. 21 allows. One search summary claims Art. 21 is mandatory, but the source was weak [SS, weak].
- I could not verify a Swiss provision equivalent to the EU's express "observe, study and test" right (UNREACHED).

**LEDGER angle** [I]:
- Decompiling another game to see how it does lighting, hair, crowds or dialogue serves no interoperability purpose, so Art. 21 does not cover it. Copying and translating the code would be unauthorised reproduction.
- Copyright is territorial. Acts on Jafar's PC fall under Swiss law; copies of the game sold in the UK, EU and US are judged under each of those countries' laws.

### 1.2 United Kingdom

**CDPA 1988 computer-program exceptions**, inserted by the Copyright (Computer Programs) Regulations 1992, SI 1992/3233 [SS; legislation.gov.uk UNREACHED]:
- s.50A: back-up copy.
- s.50B: decompilation by a lawful user. Allowed only where it is necessary to obtain the information needed to create an independent program that operates with the decompiled program, and the information is used for no other purpose.
- s.50BA: observing, studying and testing the program's functioning while doing acts the user is entitled to do.
- s.50C: other acts necessary for lawful use, including error correction.
- **s.296A makes void any contract term that tries to forbid back-ups, s.50B decompilation or s.50BA observation** [SS].
- s.296 covers circumvention of technical devices applied to programs (from memory).

**Case law:**
- *SAS Institute v World Programming*. The CJEU (C-406/10, 2 May 2012) held that a program's functionality, programming language and data-file formats are not protected expression. A licensed user may observe, study and test a program to find its underlying ideas, and the licence could not forbid that. The English High Court (Arnold J, 2010) still found that WPL's *manual* infringed SAS's manual by copying its wording [SHOWN, Wikipedia]. https://en.wikipedia.org/wiki/SAS_Institute_Inc_v_World_Programming_Ltd
- *Nova Productions v Mazooma Games* [2007] EWCA Civ 219: no copyright in a game's general ideas or rules as played (from memory, not checked).
- *Navitaire v easyJet* (2004): no protection for functionality copied without code (mentioned in the SAS article) [SHOWN].

### 1.3 European Union (Directive 2009/24/EC of 23 April 2009, which replaced 91/250/EEC)

[Wikipedia SHOWN for the history; article text SS; EUR-Lex UNREACHED]
- **Art. 5(1):** acts necessary for the lawful acquirer's intended use, including error correction, unless the contract says otherwise. The CJEU in *Top System* (C-13/20, 6 October 2021) held that decompiling to correct errors is allowed under Art. 5(1) "within the limits of the acquirer's contractual obligations" [SS].
- **Art. 5(3):** a person entitled to use the program may observe, study or test it to find its ideas and principles, while loading, running and so on.
- **Art. 6:** decompilation only where indispensable for interoperability of an independently created program. The information must not be otherwise readily available, decompilation is confined to the necessary parts, and the information may not be used for other goals or to make a substantially similar program (conditions partly SS, partly from memory).
- **Art. 8:** contract terms contrary to Art. 6 or to Art. 5(2) and 5(3) are null and void [SS].
- **Trade Secrets Directive (EU) 2016/943, Art. 3(1)(b):** observation, study, disassembly or testing of a product that is public or lawfully held is a lawful way to acquire a trade secret, *if the acquirer is free of a legally valid duty to limit acquisition*. A valid licence clause can therefore change the answer [SS].

### 1.4 United States

**Fair use for intermediate copying:**
- *Sega v. Accolade*, 977 F.2d 1510 (9th Cir. 1992): disassembling Genesis code to learn the console's compatibility requirements was fair use [SHOWN, Wikipedia]. https://en.wikipedia.org/wiki/Sega_v._Accolade
- *Sony v. Connectix*, 203 F.3d 596 (9th Cir. 2000): copying the PlayStation BIOS during development of an emulator was fair use [SHOWN, Wikipedia].
- Both protect intermediate copying to reach *unprotected functional elements*, mostly for compatibility. Neither allows putting copied code or assets in the product.
- *Atari v. Nintendo* (Fed. Cir. 1992) adds that reverse engineering can be fair, but not when the code was obtained by deceit (from memory).

**Contracts can override fair use in the US:**
- *Bowers v. Baystate* (Fed. Cir., 29 January 2003): a shrink-wrap ban on reverse engineering was enforceable and not pre-empted [W].
- *Davidson & Associates v. Jung* (Blizzard v. bnetd) (8th Cir., September 2005): the EULA ban on reverse engineering was upheld; the DMCA was violated; the §1201(f) interoperability exception did not apply [W].

**DMCA §1201 anti-circumvention:**
- §1201(f) is a narrow interoperability exemption (from memory).
- *MDY v. Blizzard* (9th Cir., 14 December 2010): circumventing the Warden anti-cheat broke §1201(a)(2) even without copyright infringement. Merely breaching the EULA's anti-bot terms was not copyright infringement, because there was no nexus to an exclusive right [W].
- Triennial exemptions: the latest final rule was effective 28 October 2024. The next cycle (2027, docket 2026-4) had renewal petitions in 2026 [SS]. They cover preservation and security research, not "learning from a rival game".

**Recent anti-cheat and cheat-maker cases:**
- *Activision v. EngineOwning* (C.D. Cal., May 2024): about US$14.47 million statutory damages under §1201 trafficking [SS].
- *Bungie v. AimJunkies*: a jury verdict on 24 May 2024 for copyright infringement, and a separate arbitration award of about US$4.3 million [SS].

**Trade secrets:** the Defend Trade Secrets Act, 18 U.S.C. §1839(6)(B), says reverse engineering is not "improper means" on its own. It becomes improper when combined with theft, deceit or breach of a duty [SS].

### 1.5 What EULAs, anti-tamper and anti-cheat add (all jurisdictions)

- **Contract.**
  - Almost every game EULA forbids reverse engineering, decompiling, modifying, data-mining and using the game "for commercial purposes".
  - In the UK and EU such a ban is void only to the extent that it blocks the narrow statutory acts (interoperability decompilation; observe, study and test; back-up). It stands for everything else, such as asset extraction or decompiling to learn methods.
  - In the US the ban can be enforced even against fair-use reverse engineering (*Bowers*, *Davidson*).
  - The usual remedy is account termination plus damages. The governing law is usually the publisher's choice.
- **Anti-tamper (Denuvo and similar) and anti-cheat (kernel drivers such as Easy Anti-Cheat and BattlEye):**
  - Circumventing them is an anti-circumvention offence in the US (§1201), the UK (s.296 and s.296ZA, from memory) and most EU states. The Swiss Art. 39a para. 4 exemption needs a *legally permitted* purpose.
  - Tampering with anti-cheat also gets accounts banned and can be treated as hacking. [I]
- **Unreal Engine (the engine LEDGER uses)** [SS; EULA text UNREACHED]:
  - Epic's EULA forbids using the "Licensed Technology", including MetaHuman, as training input, or as **prompt-based input into a generative AI program that trains on input data**. (Search summaries of conductatlas.com; the EULA change log is at https://www.unrealengine.com/en-US/eula-change-log/unreal, UNREACHED.)
  - Studying Unreal's own source code is licensed to Unreal licensees and is the legitimate way to learn engine techniques. That source may be shared only within the licence's terms (from memory; check the EULA).
- **Using AI tools to decompile or analyse others' code:**
  - The legal tests do not change.
  - Uploading another company's binaries or decompiled code to a cloud model is itself a reproduction and usually a EULA breach [I].
  - If the model reproduces that code in your project, that is copying [I].

**LEDGER-specific check:**
- Anthropic's consumer terms (post of 28 August 2025) let Free, Pro and **Max** users, *including Claude Code on those accounts*, choose whether their chats and coding sessions are used to train models. If opted in, data is kept for five years [SHOWN]. https://www.anthropic.com/news/updates-to-our-consumer-terms
- If the setting is on, Unreal and MetaHuman material read into Claude Code sessions could arguably be "prompt-based input into a generative AI program that trains on input data", which Epic's EULA forbids [I, depends on EULA wording I could not read].
- **Cheap fix: confirm the "help improve Claude" setting is off on Jafar's account.**

### 1.6 Publishers' modding and fan-content policies

- Typical terms, using Microsoft's *Game Content Usage Rules* as an example [SS] (https://www.xbox.com/en-US/developers/Rules, UNREACHED):
  - a personal, revocable, non-transferable licence;
  - no reverse engineering to reach assets;
  - non-commercial only (some allow ad revenue on videos);
  - a "not endorsed" notice is required.
- Modding policies and official mod kits allow mods *for that game*, distributed free. They never permit lifting assets or code into a separately sold game [I, consistent across the policies I know of; not checked individually].

---

## 2. Using what is learned in a commercial game

### 2.1 Ideas and methods versus expression (settled in all four jurisdictions)

- Copyright protects expression: code (literal and closely paraphrased), art, models, textures, animations, audio, text, specific characters and specific audiovisual displays.
- It does not protect ideas, procedures, methods, functionality, game rules or genre conventions. Sources: SAS v WPL (EU/UK) [SHOWN]; for the US, 17 U.S.C. §102(b) (from memory) and the game cases in part 4 [W].
- So: "characters remember what the player did and gossip" is an idea. Another game's dialogue-system code, data tables, written barks and animation files are expression.

### 2.2 Clean-room practice

[SHOWN, Wikipedia "Clean-room design"] https://en.wikipedia.org/wiki/Clean-room_design
- One team studies the original and writes a specification free of protected expression, a lawyer checks it, and a separate team that never saw the original implements it. Examples are Phoenix's IBM-compatible BIOS (1984) and ReactOS.
- It is "best practice, but not strictly required by law". It is *evidence* of independent creation.
- **It does not help against patents**, because independent invention is no defence there.

**AI and the clean room (2026)** [SS]:
- In March 2026 the maintainers of the Python library chardet released v7.0 as an LLM-driven "ground-up" rewrite and relicensed it from LGPL to MIT.
- The original author and the Free Software Foundation objected that this was not a clean room: "There is nothing 'clean' about a Large Language Model which has ingested the code it is being asked to reimplement".
- No court has ruled that I found. Leads: https://phoronix.com/news/Chardet-LLM-Rewrite-Relicense, https://heathermeeker.com/tag/ai/ (UNREACHED).

**LEDGER angle** [I]:
- Do not create tainted material in the first place. An agent that has read decompiled code cannot later act as the "clean" implementer.
- Learning only from public talks, papers, documentation, Unreal's source (licensed) and one's own observation of play needs no clean room at all.

### 2.3 Trade secrets

- Reverse engineering a lawfully obtained product is generally lawful in the EU (Directive 2016/943, Art. 3), the UK (from memory) and the US (DTSA) [SS], unless a valid contract forbids it. Theft, deceit or breach of confidence is never lawful.
- Switzerland protects manufacturing and business secrets under UWG Art. 6 and the Criminal Code Art. 162 (from memory, not checked).
- Game engines' source and internal tools are trade secrets. Leaked source code (which circulates for many games) must never be opened [I].

### 2.4 Patents on game mechanics

**Europe:**
- The European Patent Convention excludes schemes, rules and methods for playing games, and programs for computers, "as such" (Art. 52(2)(c) EPC, from memory; text UNREACHED).
- A technical implementation can still be patented.
- Switzerland follows the EPC (from memory).

**US and Japan:** game mechanics patents are granted, though after *Alice* (2014, from memory) abstract ideas are harder to patent in the US. Examples:
- **Warner Bros' "Nemesis system": US 10,926,179**, "Nemesis characters, nemesis forts, social vendettas and followers in computer games". Granted 23 February 2021, filed March 2015, reportedly in force until about 2035 [SS]. https://www.patentarcade.com/2021/02/warner-brothers-granted-patent-for-nemesis-system-from-middle-earth-video-games.html (UNREACHED)
- **Nintendo and The Pokémon Company v. Pocketpair (Palworld):**
  - Filed in the Tokyo District Court on 18 September 2024 on Japanese patents. Pocketpair changed mechanics by patch [W].
  - In the US, the USPTO Director ordered re-examination of US 12,403,397 (summoning a character to battle), and all claims were rejected on prior art. The rejection is non-final [SS].
  - Wikipedia says an evidence hearing was set for 1 October 2026, with an opinion expected 9 November 2026 [W, unverified].
- Independent invention is no defence to a patent, and a clean room does not help.

**LEDGER angle** [I]:
- LEDGER's core feature (characters who remember what the player did and talk about it) is in the same broad territory as the Nemesis patent. The Nemesis claims as reported concern specific combat-hierarchy mechanics (nemeses, forts, vendettas, followers), which look far from a gossiping town. **Only a patent attorney's freedom-to-operate reading of the claims can settle this.**
- A cheap first step: read the published claims of US 10,926,179 and note how LEDGER differs. **Whether to pay for a professional opinion is a money decision for Jafar.**
- Patents are territorial. The US and Japan matter if the game sells there, which on Steam it does.

### 2.5 Why copying code or assets is not allowed

- **Copyright:** copying is reproduction, and a modified version is an adaptation. Both are exclusive rights in every jurisdiction here.
- **Contract:** the EULA.
- **Switzerland:** UWG Art. 5 lit. c bans taking a market-ready product by technical reproduction without your own effort [SS].
- **Anti-circumvention:** if protections had to be broken to get the files.
- **Store contracts:** stores make you warrant that you hold the rights to everything you ship [I]. Steam's distribution agreement was not read (UNREACHED).
- A ripped texture or animation clip is also traceable. Studios find their assets in other games and file takedowns, which can pull a game from Steam [I].

### 2.6 Plain rule of thumb

> **Learn by playing, watching, measuring and reading what they published. Build it yourself from that understanding, with your own code and your own assets. Never open their files, never break their protection, never paste their code or art into anything, including an AI. Check patents for any mechanic that is the heart of your game.**

---

## 3. AI points that matter to a game that will be sold

### 3.1 Copyright in AI-generated output

**United States:**
- *Thaler v. Perlmutter*: the D.C. Circuit affirmed in March 2025 that a work needs a human author (date from memory). **The Supreme Court denied certiorari on 2 March 2026** [SS]. Lead: https://www.mayerbrown.com/en/insights/publications/2026/03/supreme-court-denies-review-in-ai-authorship-case (UNREACHED)
- US Copyright Office report Part 2 (*Copyrightability*, 29 January 2025):
  - Protection needs "sufficient human control over the expressive elements".
  - **Prompts alone are not enough.**
  - Human selection, arrangement, modification and human-made parts remain protected [SS].
- Part 3 (*Generative AI Training*, pre-publication, May 2025) concerns training and fair use [SS].

**United Kingdom:**
- CDPA s.9(3): for a computer-generated work with no human author, the author is "the person by whom the arrangements necessary for the creation of the work are undertaken" [W].
- The government's *Report on Copyright and Artificial Intelligence* (18 March 2026, under the Data (Use and Access) Act 2025) [SS]:
  - **proposes repealing s.9(3)**; works made with AI *assistance* keep protection where a human is the author;
  - **declined to introduce a broad text-and-data-mining exception for AI training**.
- Leads: https://www.hsfkramer.com/notes/ip/2026-03/uk-government-report-on-copyright-and-ai-concludes-more-evidence-is-needed-although-s9-3-cdpa-could-go, https://ipkitten.blogspot.com/2026/03/uk-report-on-copyright-and-artificial.html (UNREACHED).
- Until the law is changed, s.9(3) still stands [I].

**Switzerland:**
- The URG protects "intellectual creations" with individual character by humans. Purely AI-generated output is not protected unless a human made a significant creative contribution [SS, from Baker McKenzie and Swisscopyright summaries]. No AI-specific copyright change is in force [SS].
- The Federal Council plans a consultation draft by the end of 2026 to implement the Council of Europe AI Convention, which Switzerland signed in 2025. It covers transparency, data protection, non-discrimination and supervision, and applies mainly to state actors [SS].
- Leads: https://connectontech.bakermckenzie.com/switzerlands-ai-copyright-debate-legal-developments-and-outlook/, https://www.bk.admin.ch/bk/en/home/digitale-transformation-ikt-lenkung/kuenstliche_intelligenz.html (UNREACHED).

**EU and Germany:**
- Originality means the author's own intellectual creation, which implies a human (from memory).
- OLG Düsseldorf (2 April 2026) found that an AI-modified version of a photograph did not take the photographer's protected creative elements [SS].

**LEDGER angle** [I]:
- Much of LEDGER (code, textures, dialogue lines, voices) is generated by AI agents, so parts may carry thin or no copyright, especially in the US. Others could copy them with little comeback.
- What stays protectable: Jafar's human selection, arrangement and editing; human-written canon and story; the assembled game; and any hand-made or hand-edited assets.
- **Keep the records LEDGER already keeps (DECISIONS.md, approvals pages, canon).** They document the human creative choices.
- When registering with the US Copyright Office, AI-generated material must be disclosed and disclaimed (from memory of the Office's March 2023 guidance; not checked).

### 3.2 Court decisions on training data and outputs

Earlier ones are background; those from July to October 2026 are marked ★.

- **Bartz v. Anthropic (N.D. Cal.):**
  - 23 June 2025: training on lawfully acquired books was fair use, but pirated library copies were not [SS].
  - The class settlement was about US$1.5 billion. ★ **Final approval was reported for July 2026** [SS].
- **Kadrey v. Meta (N.D. Cal., 25 June 2025):** fair use on that record. The authors showed no market harm or regurgitating outputs [SS].
- **Thomson Reuters v. Ross Intelligence:**
  - D. Del., February 2025: not fair use (a competing non-generative legal-search tool trained on Westlaw headnotes).
  - ★ **The Third Circuit affirmed on 29 September 2026**, the first US appellate ruling on AI-training fair use. Its reasoning was published a day later [SS]. Leads: https://www.insurancejournal.com/news/national/2026/09/30/887260.htm, https://www.plagiarismtoday.com/2026/10/01/understanding-the-reuters-ross-ai-ruling/ (UNREACHED).
- ★ **Doe v. GitHub (9th Cir., 16 September 2026):** a generative coding tool's outputs are new works, not "copies" stripped of copyright-management information, so DMCA §1202(b) did not apply. Contract claims remain [SS]. Leads: https://www.gibsondunn.com/ninth-circuit-clarifies-limits-of-dmca-liability-for-ai-generated-code/, https://www.eff.org/tl/deeplinks/2026/09/victory-appeals-court-rejects-expansive-new-copyright-claim (UNREACHED).
- **Getty Images v. Stability AI (UK High Court, [2025] EWHC 2863 (Ch), Joanna Smith J, 4 November 2025):**
  - Getty dropped its training claim because training took place outside the UK.
  - The secondary-infringement claim failed: the model may be an "article", but its weights do not store copies, so it is not an "infringing copy".
  - Getty won only narrow trade-mark points about watermarks reproduced by older model versions.
  - **Permission to appeal on the "infringing copy" point was granted in December 2025.** I found no Court of Appeal hearing date or judgment [SS].
  - Leads: https://www.burges-salmon.com/articles/102lydc/getty-images-v-stability-ai-getty-granted-permission-to-appeal, https://www.aippi.org/news/getty-images-v-stability-ai-uk-high-court-finds-no-secondary-copyright-infringement-in-landmark-genai-ruling/ (UNREACHED).
- **GEMA v. OpenAI (LG München I, 42 O 14139/24, 11 November 2025):** memorising song lyrics in a model, and reproducing them on prompt, is reproduction. The TDM exception covered preparing the training data but not this [SS].
- ★ **GEMA v. Suno (LG München I, 42 O 763/25, 31 July 2026):** the same reasoning applied to an AI music generator. Suno was found to infringe and ordered to disclose revenue [SS].
- ★ **ANI v. OpenAI (Delhi High Court, 24 July 2026):** an interim injunction was refused. This is an interim ruling only [SS].
- **Disney and Universal (and Warner Bros. Discovery) v. Midjourney:** filed June and September 2025; in discovery in 2026, with no merits ruling found [SS].

**LEDGER angle** [I]:
- Training liability lies mainly with the model makers.
- **Output liability lands on whoever publishes the output**, and in the live talk that is the game. The obvious risk in a 1990 British setting is **song lyrics** (GEMA v OpenAI and GEMA v Suno), plus quoted poems, film lines and real people.
- Cheap mitigation:
  - tell the talking model never to quote lyrics or other copyrighted text beyond a few words;
  - have the Haiku claim-check flag them;
  - never let characters "sing" real songs.

### 3.3 Model licences' output clauses (checked texts)

**Anthropic Commercial Terms (effective 17 June 2025)**, which cover LEDGER's own API key [SHOWN via fetch]. https://www.anthropic.com/legal/commercial-terms
- The customer owns its outputs.
- Anthropic defends customers against third-party IP claims over authorised use. The exclusions include modified outputs, outputs combined with non-Anthropic technology, the customer's own data, knowing infringement, and trade marks used commercially.
- No using the services to train competing models.

**Anthropic Usage Policy (effective 15 September 2025)** [SHOWN]. https://www.anthropic.com/legal/aup
- "All consumer-facing chatbots, including any external-facing or interactive AI agent, must disclose to users that they are interacting with AI rather than a human. This disclosure must be provided at a minimum at the beginning of each chat session."
- It also bans presenting outputs as human-generated so as to convince someone they are talking to a person.
- **LEDGER angle:** an AI-voiced character the player talks to is very likely an "interactive AI agent" here [I]. **A one-line notice at the start of each play session ("Characters' replies are written live by an AI") meets this cheaply.**

**Chatterbox (Resemble AI), LEDGER's voice:**
- MIT licence, so commercial use is fine [SHOWN]. https://raw.githubusercontent.com/resemble-ai/chatterbox/master/LICENSE
- The README says every generated file carries Resemble's **Perth** imperceptible watermark [SHOWN].
- [I] Check whether LEDGER's DirectML port keeps the watermarker. It may help with EU AI Act Art. 50(2) marking (3.5).

**FLUX.1 [dev] Non-Commercial License v1.1.1 (Black Forest Labs)** [SHOWN]. https://raw.githubusercontent.com/black-forest-labs/flux/main/model_licenses/LICENSE-FLUX1-dev
- §2(d) says "You may use Output for any purpose (including for commercial purposes)".
- But the licence to *use the model* is "solely for your Non-Commercial Purposes", and use "for revenue-generating activity" or "in direct interactions with or that has impact on end users" is *not* non-commercial. It also requires content filters and AI disclosure.
- [I] Generating assets for a game that will be sold is very likely outside this licence without a paid commercial licence. **Treat FLUX.1 [dev] (and similar "open weights, non-commercial" models) as not usable for LEDGER.**

**Tencent Hunyuan 3D 2.1 Community License (13 June 2025)** [SHOWN]. https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE
- "THIS LICENSE AGREEMENT DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA".
- §5(c): "You must not use, reproduce, modify, distribute, or display the Tencent Hunyuan 3D 2.1 Works, Output or results … outside the Territory."
- [I] A game containing its output and sold in the UK or EU would display output outside the Territory. Switzerland is inside the Territory, but the market is not. **Not usable for a game sold worldwide.**

**General checklist for any model** [I]:
1. Commercial use of the *model*, not just the outputs.
2. Output clause.
3. Territory.
4. Training-data taint (non-commercial datasets such as SMPL or AMASS carry into derived models' terms).
5. NoAI flags on any input.
6. Disclosure or filter duties.
7. Revenue caps (some community licences end above a revenue threshold).

### 3.4 Steam's AI disclosure rules

- **January 2024 framework** [SS; Steamworks UNREACHED]:
  - "Pre-generated" AI content (made during development) must meet the same rules as other content.
  - **"Live-generated" content (made while the game runs) needs a description of the guardrails that stop illegal content.**
  - Players can report illegal live-generated content through the Steam overlay.
  - The disclosures appear on the store page.
- **16 January 2026 rewrite** [SS]: AI tools used inside the development process (coding assistants and the like) no longer need disclosure. AI-generated content that players see (in the game, on the store page, in marketing) and live-generated content still do.
- Leads: https://www.videogameschronicle.com/news/valve-has-significantly-rewritten-steams-rules-for-how-developers-much-disclose-ai-use, https://partner.steamgames.com/doc/gettingstarted/contentsurvey (UNREACHED).
- **LEDGER angle** [I]: LEDGER will need both:
  - pre-generated disclosure for AI-made art, voices and text;
  - live-generated disclosure for the talk and live voice, with a plain account of its guardrails: the Haiku claim-check, the content rules (no alcohol, gambling or children; no real people), and refusal handling.

  The claim-check and canon rules are a ready answer to Valve's guardrail question.

### 3.5 EU AI Act: transparency for systems that talk to people

**Timing** [SS]:
- Art. 50 transparency duties **have applied since 2 August 2026**.
- The "Digital Omnibus on AI" was politically agreed on 7 May 2026, approved by Parliament on 16 June and by the Council on 29 June, and entered into force on 27 July 2026. It **did not delay Art. 50(1)**.
- It gave **systems already on the market before 2 August 2026 until 2 December 2026** to meet Art. 50(2) machine-readable marking.
- Leads: https://www.hoganlovells.com/en/publications/eu-legislators-agree-to-delay-for-highrisk-ai-rules, https://taylorwessing.com/en/insights-and-events/insights/2026/05/the-eu-digital-omnibus-on-ai-what-the-political-deal-means (UNREACHED).

**Guidance** [SS]:
- The Commission's final **Code of Practice on marking and labelling AI-generated content** was published on 10 June 2026 (voluntary).
- Its final **guidelines on Art. 50** followed on 20 July 2026.
- **The guidelines say AI-enabled NPCs can meet the "obvious" exception to Art. 50(1), but only in single-player games and only where the AI nature is obvious to all users, including vulnerable ones.** Realism, immersion and audience matter.
- Leads: https://www.paulweiss.com/insights/client-memos/eu-finalises-transparency-rules-for-ai-generated-content, https://chambers.com/articles/same-npc-different-rules-how-a-player-s-age-changes-their-responsibilities-under-the-ai-act (UNREACHED).

**What Art. 50 requires** (from memory and SS):
- 50(1): providers of systems meant to interact directly with people must make sure people are told they are dealing with AI, unless it is obvious.
- 50(2): providers of systems that generate synthetic audio, image, video or text must mark outputs in a machine-readable, detectable way, as far as technically feasible.
- 50(4): deployers must disclose deep fakes, with lighter duties for evidently artistic or fictional works.

**Reach and fines:**
- The Act reaches providers outside the EU who place systems on the EU market [W].
- Breaches of Art. 50 can be fined up to €15 million or 3% of worldwide turnover, whichever is *lower* for SMEs [SS].

**LEDGER angle** [I]:
- Selling on Steam into the EU very likely makes Jafar the "provider" of an AI system: the game with live talk built on Claude and Chatterbox.
  - **50(1):** LEDGER is single-player, but its characters are photoreal and voiced, so the "obvious" exception is arguable rather than safe. The session-start notice that Anthropic's policy needs anyway also settles this.
  - **50(2):** marking synthetic voice and text where feasible. Chatterbox's Perth watermark, if kept, covers the audio. How to mark text shown only inside the game is an **open question** to check in the Code of Practice (UNREACHED).
  - **50(4):** fictional characters who resemble no real person are probably not "deep fakes". Keep it that way: no real people's faces or voices.
- **Switzerland** has no equivalent law in force (draft expected by the end of 2026) [SS].
- **UK:** I found no AI-specific transparency statute that would apply. Consumer-protection and advertising rules still apply [I, unverified].

### 3.6 Related point outside this strand: personal data in live talk [I]

- The player's typed or spoken lines go to Anthropic in the US.
- Under the GDPR, UK GDPR and the Swiss data protection act (FADP), the game will need:
  - a short privacy notice;
  - a lawful basis for processing;
  - Anthropic's data-processing terms for international transfers.
- Microphone input raises the stakes. Not researched here.

---

## 4. Mashups: combining or imitating two existing games

**What courts have protected and not protected** [W, "Video game clone"; some details unverified]. https://en.wikipedia.org/wiki/Video_game_clone

- **Not protected (free to use):**
  - *Data East v. Epyx* (9th Cir. 1988): karate moves and the general fighting-game format are *scènes à faire*.
  - *Capcom v. Data East* (1990s; court and year from memory): common kicks and punches are unprotectable.
  - Rules, mechanics, genre, camera, user-interface conventions.
- **Protected:**
  - *Atari v. Philips* (7th Cir. 1982; court and year from memory): K.C. Munchkin copied Pac-Man's "unique expression" (character design, look).
  - *Tetris Holding v. Xio Interactive* (D.N.J. 2012): copying Tetris's board, piece shapes and colours, ghost piece, next-piece display and overall look was infringement of copyright and trade dress.
  - *Spry Fox v. LOLApps* (2012): the claim over *Triple Town*'s look and feel went ahead, and the case settled with Spry Fox taking ownership of *Yeti Town*. The Wikipedia summary mentions a preliminary injunction, which I could not verify.
- **Still filed in 2025:** Homa Games v. Century Games (C.D. Cal., complaint of 27 January 2025, alleging "level by level and element by element" copying) [SS].

**Other rights on the "look and feel":**
- **Trade dress** (US Lanham Act): non-functional, distinctive presentation.
- **Passing off** (UK).
- **UWG Art. 3(1)(d)** (Switzerland): risk of confusion [SS].
- **Registered and unregistered designs** (EU, UK, CH): user-interface and character designs.
- **Trade marks** on titles, logos and character names.

**Names** [I]:
- Clear the game's title and any invented brand names against trade-mark registers in Switzerland (Swissreg), the EU (EUIPO), the UK (UKIPO) and the US (USPTO). Classes 9 (software) and 41 (entertainment) matter.
- **The working title "LEDGER" coincides with a well-known hardware-wallet company that also sells software.** I did not check its registrations. A title search before the Steam page goes up is cheap; renaming after launch is not.

**Marketing** [I]:
- "Inspired by X" in press or interviews is generally lawful referential use if nothing implies endorsement.
- Do not use other games' logos, screenshots or key art.
- Since September 2024 Steam forbids images, links or widgets pointing to other Steam games in store-page descriptions [SS].

**LEDGER's own references** [I]:
- The KCD2 frames and the Hook sheet used as a visual bar are fine for human or AI *judgement* (comparison only).
- They must never be used as image input to a generator (img2img, style transfer, "make it look like this frame"), never traced, and never shipped.
- Style itself is not protected, but derivative frames would be.
- Period realism should keep using invented names for makers, papers, parties and shops, as canon already requires. Real car body designs and brand liveries are licensed in commercial games for a reason.

**Safe recipe for a mashup** [I]:
- Take the *systems* you admire from both games.
- Rebuild them with your own code, art, names and user interface.
- Give the result its own visual identity.
- Make sure no single screen could be mistaken for either source.
- Check any core mechanic for patents.

---

## Settled versus open

| Question | Status |
|---|---|
| Playing and observing other games to learn | Settled: lawful everywhere |
| Decompiling for interoperability, under conditions | Settled exception (CH Art. 21, UK s.50B, EU Art. 6, US fair use and §1201(f)) |
| Decompiling or ripping to learn techniques or take assets | Settled: not covered by any exception; infringement plus breach of EULA |
| EULA bans on reverse engineering | US: enforceable. UK and EU: void only against the narrow statutory acts. CH: **open** |
| Circumventing DRM or anti-cheat | Unlawful in the US, UK and EU; CH allows it only for a legally permitted use (Art. 39a para. 4) |
| Ideas and mechanics free; expression not | Settled |
| Game-mechanic patents | Real in the US and Japan (Nemesis, Nintendo); narrower in Europe; **freedom to operate is open for LEDGER** |
| Copyright in purely AI output | US: none (Thaler, cert. denied 2 March 2026). CH and EU: human creation required. UK: s.9(3) still in force, repeal proposed March 2026 |
| Training on copyrighted works | **Open**: US split by facts (Bartz and Kadrey fair use; Ross not fair use, affirmed 29 September 2026); UK appeal pending in Getty; Germany finds memorisation infringing (GEMA v OpenAI and v Suno) |
| Who carries output risk | The publisher of the output, which for live talk is the game |
| EU AI Act Art. 50 | In force for new systems since 2 August 2026; NPC "obvious" exception exists but is narrow |
| Steam disclosure | Required for content players see and for live generation; development tools exempt since 16 January 2026 |

## What Jafar could act on (money, licences, scope)

1. **(Free)** Confirm the "help improve Claude" model-training setting is off on his Max account, so Unreal and MetaHuman material in Claude Code sessions is not used for training (Epic's EULA, 1.5).
2. **(Free)** Add a one-line AI notice at the start of each play session, plus Steam's pre-generated and live-generated disclosures. This covers Anthropic's usage policy, Steam and EU AI Act Art. 50(1) together.
3. **(Free)** Forbid quoted lyrics, poems and long quotations in the talking model's instructions and the claim-check.
4. **(Free)** Keep FLUX.1 [dev], Hunyuan3D and any territory-limited or non-commercial model out of the pipeline; add them to the licence allowlist as excluded.
5. **(Money, his decision)** Before release, a one-off review by a Swiss IP lawyer covering three things:
   - the title search;
   - a quick freedom-to-operate reading of the Nemesis patent claims against LEDGER's memory-and-gossip system;
   - the Steam, AI Act and privacy notices.

   Recommendation: yes, once a release date exists. It is far cheaper than a rename or a takedown.
