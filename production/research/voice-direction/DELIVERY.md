# Voice direction: how studios get acting, and what it means for LEDGER's cloned voices

Research, 30 September 2026, by a separate research helper (about thirty minutes of searching and reading). The question: how game studios get acting, not reading, from voices, from start to finish; then how that sequence applies to cloned voices from Chatterbox, VoxCPM2 and Pocket TTS on this PC.

(The helper returned its text; the session that asked for it saved it here. That session checked the project facts against the files: the voice server loads Chatterbox Nano and prepares the cast's voices with its prewarm option, and the voice-engines spec says everyone is on Nano. It reworded the note on the brief in (b); nothing else was changed.)

How to read it:
- **OPENED** means I read the page itself. **SNIPPET** means I saw only a search engine's summary because the network refused the page.
- The network allowed GitHub, Wikipedia, arXiv's API and PyPI. It refused GDC Vault, Hugging Face, Ubisoft, Sony's PDF host, Game Developer, A Sound Effect, trade press, and the vendor and union sites.
- Codes in brackets (P1, M2 …) point to the source list at the end.
- "Practice" means a source says studios do it. "My recommendation" and "my estimate" mean it is mine.

## (a) The professional pipeline, stage by stage

### 1. Character and casting reference
- **Practice.**
  - A written character spec comes before casting and is sent to the actor before the session: bio, age, origin, references, pronunciations, emotional range, and what the character never does.
  - Muziument describes a "voice directing sheet for each character" with voice references, emotional range, vocal characteristics and prohibited expressions [P4].
  - A British voice actor's guide (30 Sep 2021) asks for bios, references, pronunciations and emotional context in advance [P3].
  - A GDC talk covers "how to fully flesh out character specs when casting" [P12b].
  - At Ubisoft Toronto a voice designer preps and runs voice, mocap and cinematic sessions, tracks session data, edits, supports integration, and works with narrative, casting and localisation [P1].
- **Evidence:** moderate; all from search summaries.
- **LEDGER:** the approved clip is the "actor". An actor brings range. A VCTK reference brings one register: read sentences [M19].

### 2. Script with context, and direction
- **Context on every line.** Each line carries the situation that triggers it, who is addressed and what the character wants [P2, P3, P5, P5b].
- **Directors are warned off "result direction".** The sources say "adverbs, adjectives and judgements are never an effective direction" and "intentions can be acted, objectives cannot". They advise situation and intention instead [P5b]. This is a search summary merging three pages; I can't tie each quote to one page.
- **Game-specific advice:** "write a single sentence describing what game situation triggers a line and what action the player is performing" [P5b].
- **One line may need different reads for different game states,** such as exerting versus idle [P5].
- **Session tools:**
  - line reads: the director says the line and the actor copies it;
  - "ABC": three reads of the actor's choice;
  - alts and intensity variations;
  - pick-ups [P3, P2, via search summary].
  - "Wild lines": I found no game-specific definition.
- **Context in the booth.** Mark Estdale (OMUK, London; about 500 games) built tools to "emulate the game engine in the recording studio immersing the actor in the game at the point of creation". His reason: "What the actor needs is something at the point of performance that they can react to" [P6, P7].
- **Cinematic AAA records voice with the body.** The Last of Us Part II used performance capture, "recording motion and voice simultaneously" [P8].
- **Unreal support.** Unreal's Dialogue Wave asset holds speaker and listener contexts and a "Voice Actor Direction" field [P21].

### 3. Recording sessions and takes
- **Pace:** about 100 lines an hour at 2–3 takes per line for ordinary dialogue. Short callouts run about 300 lines in 2 hours and over 1,000 takes [P9]. This is a search summary of a forum thread; the weakest number here.
- **Session length:** traditionally four hours. SAG-AFTRA's 2025 agreement caps vocally stressful sessions at two hours [P10].
- **Small-team example:** Hades, fewer than 20 staff and more than 22,000 lines. The audio director did all voice direction, recording, processing and implementation [P11].
- **My reading:** studio take counts are low because every take costs an actor's effort. With synthesis, takes are cheap and the variety comes from the reference clip and the random seed, so more takes and stricter selection make sense.

### 4. Take selection
- **Practice:**
  - In film, the script supervisor "circles" the takes the director liked [P24].
  - After a game session, selection happens with the engineer. The order of priority is "authenticity of the performance → technical flaws → tonal consistency with other lines in-game" [P4].
  - Selection is made by people: the director, voice designer or dialogue editor.
- **No source I reached describes an automated judge of acting.** Tools such as whisper checks screen the words only [M8].

### 5. Dialogue editing
- **Editors work to a written spec:** how much silence before and after, and whether to remove breaths and pops [P15].
- **Breaths and efforts ("emotes")** are planned and recorded as their own assets [P15].
- **Csurics (2K Marin, GDC 2012)** says dialogue is cut "tight, microscope clean, with natural breaths and peak normalized -.03" [P13]. The units are as the summary gives them, probably −0.3 dBFS; not verified.
- **Film dialogue editors** replace unusable portions with alternate takes [P19].

### 6. Mixing, processing and loudness
- **Sony ASWG-R001:**
  - Created November 2012.
  - Wikipedia cites the August 2013 version: −23 LUFS for console and desktop, −18 for portable [P17].
  - A summary of the PDF says a revision moved console to −24 LKFS to match ATSC. It measures the whole mix, not dialogue alone, over at least 30 minutes [P16].
- **EBU R128 (v4.0, August 2020):** −23 LUFS ±0.5 LU; maximum true peak −1 dBTP [P18].
- **Dialogue is the anchor** the rest of the mix is set around. Crytek worked at −23 [P20].
- **Voice processing in engine:** dialogue specialists build "process patches" for voices, check lip sync, and handle priority, queuing and ducking of music and effects under dialogue [P23].
- **Distance and rooms** come from the engine's attenuation and reverb, not from the recording (general practice; I reached no primary source for this).

### 7. Implementation
- Dialogue assets carry speaker/listener context and subtitles in Unreal [P21], with priority, ducking and queuing rules [P23].

### 8. Listening in context
- **Sourced weakly.** Estdale's argument that context matters at the moment of performance [P6], plus the audit.
- **No primary source I reached describes a studio's in-engine review routine in detail.** I treat it as consensus practice, not a documented standard.

### 9. Synthetic voice in professional use, 2020–2026
- **Placeholders and prototypes:**
  - Sonantic's emotional TTS was used by Obsidian, Splash Damage and 4A Games "from development through post-production" (March 2021) [S2].
  - Ubisoft La Forge presented speech synthesis for games at GDC 2021 [S1].
  - Vendors describe TTS as scratch voice to test timing before casting [S9, vendor].
- **Shipped minor lines:**
  - Embark (The Finals, Arc Raiders) used TTS from actors paid to license their voices, for "lines that aren't as essential" [S4].
  - Eurogamer's review (10 Nov 2025) criticised the generated lines.
  - By 13 Mar 2026 the CEO said some had been re-recorded by humans: "a quality difference" [S3].
- **Performance transfer (CD Projekt Red with Respeecher):**
  - Phantom Liberty (released 26 Sep 2023), Polish Viktor Vektor.
  - Janusz Zadura performed the lines, imitating the late Miłogost Reczek's style.
  - Respeecher converted them into Reczek's voice with his family's permission, announced October 2023 [S5, S6].
- **Live-generated voice:**
  - Fortnite's Darth Vader (16 May 2025): Gemini 2.0 Flash wrote the replies and ElevenLabs Flash v2.5 spoke them, in consultation with the Jones family.
  - Players got him to swear; it was hot-fixed within about 30 minutes [S7].
- **Union terms:** SAG-AFTRA's 2025 agreement, ratified July 2025, requires separate written consent and disclosure for digital replicas [P10].
- **My reading:** in every case I reached, either the acting came from a human performance or the synthetic lines were the least important. No source shows a studio shipping emotionally central lines from zero-shot TTS.

## (b) The open models: real direction levers, weights licence, what is known

**General evidence first:**
- **Zero-shot TTS copies the reference's style.** It "strongly inherit[s] the speaking style present in the reference", so a desired style "often requires carefully selecting reference audio" [M17, 7 Jan 2026].
- **Zero-shot TTS flattens accents.** It reproduces "a speaker's timbre while flattening the accent toward generic English". Fine-tuning Chatterbox raised accent similarity, including on speakers it hadn't seen [M18, 25 Jul 2026].
- **Clones only reproduce emotion that is in their audio.** A vendor, ElevenLabs, says a clone reproduces emotion only if it is present in the training audio, and advises recording several "mood passes" [S10].
- **VCTK is read speech.** Each speaker reads about 400 sentences: Glasgow Herald newspaper text, the rainbow passage and an elicitation paragraph [M19]. The project's references are read speech by construction.

### Original Chatterbox (500M, English)
- **Levers (read in source [M2]):**
  - the reference clip;
  - `exaggeration`, default 0.5, written into an emotion conditioning channel;
  - `cfg_weight`, default 0.5;
  - `temperature` 0.8, `min_p` 0.05, `top_p` 1.0, `repetition_penalty` 1.2;
  - the text and its punctuation.
  - There are no text instructions and no tags.
- **Vendor tips [M1]:**
  - the defaults suit most prompts;
  - for a fast-speaking reference, CFG about 0.3;
  - for drama, CFG about 0.3 and exaggeration about 0.7 or more;
  - higher exaggeration speeds speech up;
  - set CFG to 0 when the reference language differs from the target, to stop accent transfer.
- **Takes:**
  - seed and temperature;
  - a community tool makes several "candidates per chunk", checks them with whisper, and has seeded retries and fallbacks [M8];
  - a live demo maps 12 detected emotions per reply to exaggeration 0.05–0.95 and CFG 0.2–0.95 [M9].
- **Accent:** an American user reports "about one in every five" generations coming out British, with no replies (8 Sep 2025) [M7]. Accent drift follows the reference and chance, in both directions.
- **Claims about capitals and em-dashes** shifting delivery come from a third-party blog [M21] and are unverified.
- **Licence:**
  - code MIT, "Copyright (c) 2025 Resemble AI" [M3];
  - weights MIT per the Hugging Face card (SNIPPET; the card was refused) [M4];
  - every output carries the PerTh watermark [M1].

### Chatterbox Turbo (350M) and Nano (110M): the game's live engine is Nano
- **Levers:**
  - the reference clip, with `norm_loudness` applied to it;
  - `temperature` 0.8, `top_p` 0.95, `repetition_penalty` 1.2;
  - tags in the text: `[cough]`, `[laugh]`, `[chuckle]` "and more" (the full list not verified).
- **Ignored:** `exaggeration`, `cfg_weight` and `min_p` are accepted and ignored with the warning "not supported by the {Turbo/Nano} version and will be ignored". I confirmed this today in `tts_turbo.py` [M2], which matches the project's 19 September recheck.
- **Speed:** Nano is "3x faster than realtime on 8 CPU cores" (vendor) [M1].
- **Licence:**
  - code MIT [M3];
  - Turbo card MIT, page updated about 15 Dec 2025 (SNIPPET) [M4];
  - Nano's card not read; Nano was merged upstream on about 21 Jul 2026 (third-party SNIPPET) [M5].
- **Project note:** the brief this helper was given said the live engine is "the original Chatterbox"; that was the asking session's mistake. The project's own records say otherwise: the voice server loads `ChatterboxTurboTTS(nano=True)`, and the voice-engines spec says "Everyone is on Nano". The acting test used the original model for its acted references.

### VoxCPM2 (OpenBMB, 2B)
- **Levers (README [M10]):**
  - the instruction goes in parentheses at the start of the text, e.g. `(slightly faster, cheerful tone)Target text`, for both voice design and "controllable cloning";
  - `reference_wav_path`;
  - "Ultimate Cloning": `prompt_wav_path` plus its transcript continues from the reference, reproducing "timbre, rhythm, emotion, and style";
  - `cfg_value` (2.0 in examples), `inference_timesteps` (10), `seed`;
  - a temperature control is named in a page summary but not shown in the README code (not verified).
- **Stability:** "results can vary between runs — you may try to generate 1~3 times".
- **Fine-tuning:** LoRA and full, "with as little as 5–10 minutes of audio".
- **Accent:** 30 languages and 9 Chinese dialects are listed; no English regional accents. In the project's test it held Ron's voice, lost Darren's Scottish and kept Sheila's American lean. The test used one take per condition and manner-adjective directions.
- **Licence:** weights and code Apache-2.0, stated in the README and the technical report abstract [M10, M11], both OPENED; the Hugging Face metadata agrees (SNIPPET). Released April 2026; technical report 5 Jun 2026.
- **Speed:** RTF about 0.3 on an RTX 4090 (vendor). The project measured about 25 times real time on this PC's processor.

### Pocket TTS (Kyutai, 100M)
- **Levers (README [M12]):**
  - a reference wav, or a voice state exported to a file;
  - the model choice, including an English variant `english_drifting_26-09`;
  - no documented emotion, style or instruction control;
  - pauses via silence in the text are "not support[ed]";
  - other sampling controls are not documented in the README (not verified).
- **Speed:** about 200 ms to the first chunk; about 6 times real time on a MacBook Air M4; 2 CPU cores.
- **Accent:** the default voices are cloned from English audio, and their English accent carries into other languages [M16]. The reference's accent dominates. I found nothing published on its acting.
- **Licence:**
  - code MIT [M12];
  - weights CC-BY-4.0 per the Hugging Face card (SNIPPET) [M13], which is not on the allowlist;
  - cloning weights are gated behind a consent promise;
  - acceptable use forbids cloning without explicit lawful consent [M12].
- **Dates:** paper 8 Sep 2025 [M14]; blog 13 Jan 2026 [M15]; training code released August 2026 [M12].

**What published users say about acted delivery and accents:** little. For Chatterbox there are the vendor tips, the accent-drift issue, and emotion-to-setting projects. For VoxCPM2, only the vendor's note that results vary. For Pocket TTS, nothing on acting. I found no published test for British regional accents on any of them.

## (c) Speech-to-speech and performance transfer

A person, or another voice, performs the line and a converter swaps in the character's timbre. The professional precedent is CD Projekt Red with Respeecher [S5, S6]: a human actor supplied the performance and imitated the target's style; the converter supplied the timbre.

**Chatterbox VC**
- **How it works:** `ChatterboxVC.generate(audio, target_voice_path)`, using weights from the same repository as the TTS [M6].
- **Licence:** MIT, covered by the existing allowlist entry [M3].
- **Caveat:** timbre only; I found no claim that it converts accent.

**Seed-VC**
- **Licence:** GPL-3.0 code [V1]; weights GPL-3.0 (SNIPPET).
- **Versions:**
  - V1 converts timbre only.
  - V2 is described as "Voice & Accent Conversion". Its `--convert-style` option uses a model "for accent & emotion conversion".
  - V2's changelog is dated 2024-04-16 as written, but it sits above a 2025-03-03 entry, so it is probably 2025.
- **Speed:** a reference of 1–30 s; real-time delay of about 300 ms (algorithm) plus about 100 ms (device), with a GPU recommended.
- **Caveat:** converting "emotion" toward the reference could undo the performance; untested.

**RVC**
- **Licence:** MIT code (2023) [V2]. The pretrained base weights are on Hugging Face (lj1995); their licence was not verified.
- **Caveat:** it trains a per-voice model from "≤10 mins" of audio. The performer's accent stays (timbre model; my inference).

**kNN-VC**
- **Licence:** MIT code (Stellenbosch University, 2023) [V3]. The checkpoints come from the GitHub releases; their licence is not stated separately.
- **How it works:** each performed frame is replaced by the nearest frames from the target's own recordings. Quality improves with more target speech, with diminishing returns beyond 5 minutes [V3].
- **Caveat:** it is the only one that draws on the target speaker's own sounds; VCTK has about 20–25 minutes per speaker (project estimate). Whether that restores Scottish vowels is unproven.

**OpenVoice v2**
- **Licence:** MIT since April 2024 [V4].
- **Caveat:** a tone-colour converter; the project's earlier research found it keeps the source's accent.

**Canon and consent.** Canon forbids real people's voices; the allowlist bans clones of identifiable real people.
- If Jafar performs a line and it is converted into a VCTK character's timbre, the timbre heard is the VCTK speaker's. That is already a stated, accepted risk.
- The performance, and any trace of his own accent, would be his. This is not cloning a real person into the game, but it puts his delivery inside the characters.

**Question for him (for the builder to ask):**
- A) No: synthesis only.
- **B) Yes, as a trial (my recommendation if he is willing).** He performs three of Ron's lines on his phone. They are converted with Chatterbox's own converter, which is already allowed, and judged blind against the best synthetic takes. It is free, needs no new licence, and starts with Ron because his synthetic voice already holds its accent, so the trial isolates whether a human performance adds acting.
- C) Yes, and also try Seed-VC's accent conversion. This needs a licence decision (GPL-3.0 code and weights, used only as an offline tool). My reading is that audio a program outputs is not itself covered by the program's GPL; this is not legal advice.

## (d) Concrete steps for this project

### Lines made in advance (offline; slow on the processor is fine)
1. **Freeze the character reference.** Name the approved clip exactly (take id, engine, approval date) beside the casting sheet: age, place, register, pace [P3, P4; the project's exact-version rule].
2. **Build a reference library for each character.** My estimate: 5 moods (calm, warm, sharp or threatening, quiet or confiding, amused) with 2–3 clips each, about 10 s per clip. Sources for the clips, cheapest first:
   - the same VCTK speaker's livelier sentences (questions, exclamations, the elicitation paragraph): the same person, so likeness holds, but the range is narrow;
   - generated acted takes that a human ear approves as in accent and in character (the original Chatterbox pushed hard, or VoxCPM2 with direction for Ron), extending the acted references the acting test already made;
   - new speakers from conversational corpora, such as EdAcc (CC BY-SA, about 40 h of video-call conversation) [M20]. That would be a recast: it needs Jafar's yes and settles the ShareAlike question.

   Each library clip is a person's voice, so each goes on his page once.
3. **Write a direction sheet for each line:**
   - the situation and what has just happened;
   - the listener;
   - the intention, as a verb ("warn him off", "reassure", "deflect");
   - the subtext;
   - for the model: 3–6 manner words (VoxCPM2's own examples are manner words), the mood (which picks the library clip), and exaggeration/CFG starting points from the vendor tips.

   Keep the sheet with the line; Unreal's Dialogue Wave has a direction field [P21].
4. **Generate takes.** My estimate: 2–3 library clips times 3–4 seeds, so 6–12 takes per line. For comparison: studios take 2–3 per line [P9]; VoxCPM says try 1–3 times [M10].
5. **Screen, don't judge.** Check the words heard back, the likeness to the approved clip, and clipping or artefacts. Write the accent classifier's flag beside each take but never reject on it alone: it passes only 26 of 50 genuine Scottish clips (project measurement, 29 Sep). Keep the best 3–4.
6. **Select by ear, for one first scene only.** My suggestion is 10–15 lines across Ron, Sheila and Darren. Put 3–4 finalists per line on his page, each heard as a short clip from the game (step 9), with its direction sentence beside it. The practice criteria are believable, clean and consistent with the neighbouring lines [P4]. Record which clip and settings won each line; that becomes the recipe for multiplying.
7. **Edit to a written spec [P15].** My estimates:
   - trim heads to 50–100 ms and tails to 150–300 ms;
   - keep a natural in-breath where it carries intention;
   - cut artefacts and any continuation words (VoxCPM's continuation mode began takes with the reference's last word);
   - don't join two synthetic takes unless their timbre matches.
8. **Set loudness.**
   - Each line: one speech loudness, my estimate about −23 LUFS integrated, true peak no higher than −1 dBTP [P18].
   - The game mix: about −23 to −24 LUFS integrated over a walk of at least 30 minutes [P16, P17]. PC has no platform rule; Sony's figure is the nearest published target.
   - Lines stay dry; distance, room and occlusion come from Unreal's attenuation and reverb, the same as for live lines.
9. **Listen in context.** Capture each line playing in the game, through the game's camera and exposure (from the AI tester's walk or a scripted shot), and judge that clip, not the bare file. The approval names both the take and the build.
10. **Multiply only after he approves that scene.**

### Live replies
**What the live path can borrow:**
- **The reference library.**
  - The conversation model adds one mood tag to each reply, chosen from a closed set that matches the library.
  - The voice uses that clip's conditioning, prepared at start-up; the voice server already prepares the cast voices before it says it is ready.
  - Cost per clip and start-up time are not measured. My estimate is that switching between prepared clips costs almost nothing when speaking.
- **Text shaping.**
  - The writer produces speakable text: short sentences, and commas and dashes for pauses.
  - Nano's tags (`[laugh]`, `[chuckle]`, `[cough]`) sparingly, and only where the mood allows [M1].
- **Temperature per mood.** Lower for calm or threat, higher for amused. My suggestion; untested.
- **Loudness.** Automatic per reply, to the same target as the lines made in advance, with the same in-engine perspective.
- **Lines made in advance.** Barks, thinking sounds and greetings come from the offline pipeline. The most emotional beats are authored and made in advance, as the audit also advised.

**What it cannot borrow:**
- many takes and selection by ear: there is no time, and the live voice (Nano, its sound tokens made on the graphics card and the rest on the processor) has no headroom for a second take (project measurements);
- exaggeration and CFG, which Nano ignores;
- direction and editing for each line.

**Check:** in the game, by the AI tester's walk and by Jafar's play, with the delay measured while mood switching is on.

**Order (my recommendation):**
1. Ron's library and one scene made in advance, onto his page.
2. Meanwhile, wire the live mood switch and measure the delay.
3. Then Sheila's and Darren's libraries; the choice of reference matters most for their accents.
4. Fine-tuning for accent (the Singlish study [M18]) stays a later scope and graphics-card decision for Jafar.

## (e) What could not be verified or reached
- **Pages refused:**
  - GDC Vault: Hades 2021, Dialogue 101 2015, Speech Synthesis 2021, Anatomy of Great Voice-Over, and the Spot the Difference 2012 slides;
  - Game Developer, A Sound Effect, and Ubisoft Toronto (the audit's own source, so I could not read what it actually says);
  - Sony's ASWG-R001 PDF;
  - Hugging Face, so every weights licence rests on GitHub files or search summaries;
  - kyutai.org, resemble.ai, respeecher.com, sagaftra.org, Epic's documentation, and the trade press.
- **Loudness:** Wikipedia's citation says −23 (August 2013); a summary of the PDF says a later revision moved it to −24 LKFS. Which is current is not verified.
- **Csurics' "-.03" figure:** units unclear.
- **"Wild lines":** no game-specific definition found.
- **Take counts:** from a forum only. I found no source on how many takes studios generate with TTS.
- **Acting and accents in these models:** no published measurement of acted delivery or British regional accent retention for Chatterbox, Turbo/Nano, VoxCPM2 or Pocket TTS.
- **Model details not confirmed:**
  - VoxCPM2's temperature control;
  - Nano's tag list beyond three tags;
  - Nano's release date and card licence;
  - Pocket TTS's sampling controls;
  - RVC's pretrained weights licence;
  - kNN-VC's checkpoint licence;
  - Seed-VC V2's date.
- **Unmeasured claims:** the added delay of choosing a clip per reply on this PC; whether kNN-VC or Seed-VC V2 restores a Scottish accent.
- **Vendor interest:** ElevenLabs, Respeecher and Resemble have a commercial interest in their claims.
- **Records disagreed:** the brief this helper was given said the live engine is the original Chatterbox; the project records and code say Nano, and the code is right.

## Sources (all read 30 Sep 2026)

**Professional pipeline**
- P1. People of Ubisoft Toronto — Meet Johnny Lucas, Voice Designer. Ubisoft Toronto. Undated. https://toronto.ubisoft.com/people-of-ubisoft-toronto-meet-johnny-lucas-voice-designer/ . Read 30 Sep 2026. SNIPPET.
- P2. Directing the Voice-over Actor: Tips for Better Communication. Vicki Amorose, Game Developer (formerly Gamasutra). Undated. https://www.gamedeveloper.com/audio/directing-the-voice-over-actor-tips-for-better-communication . Read 30 Sep 2026. SNIPPET.
- P3. How to Direct Voice Actors in Video Games. Naturally RP (British voice-over artist). 30 Sep 2021 (from the URL). https://www.naturallyrp.co.uk/blog/2021/9/30/how-to-direct-voice-actors-in-video-games . Read 30 Sep 2026. SNIPPET.
- P4. Game Voice Directing Guide: Script to Final Audio Asset. Muziument. Undated. https://muziument.com/en/blog/game-sound-director-voice-directing-workflow . Read 30 Sep 2026. SNIPPET.
- P5. Dialogue for Video Games: 11 Things you Should Know. GameSoundCon. 9 Sep 2019. https://www.gamesoundcon.com/post/2019/09/09/dialogue-for-video-games-11-things-you-should-know . Read 30 Sep 2026. SNIPPET.
- P5b. Result direction versus intention; one merged search summary of three pages. Why Voice Acting with Intention is a Strong Choice, Kim Handysides, 2 Nov 2021, https://kimhandysidesvoiceover.com/2021/11/02/why-voice-acting-with-intention-is-a-strong-choice/ ; 20 examples of result directing, Ernest Goodman Studio, undated, https://www.ernestgoodmanstudio.com/20-examples-of-result-directing/ ; How to Direct Your Game's Voice Actors, How to Write a Game (Substack), undated, https://howtowriteagame.substack.com/p/how-to-direct-your-games-voice-actors . Read 30 Sep 2026. SNIPPET.
- P6. Mark Estdale. Wikipedia. Current revision, undated. https://en.wikipedia.org/wiki/Mark_Estdale . Read 30 Sep 2026. OPENED.
- P7. Services Spotlight: OMUK. MCV/Develop. Undated. https://mcvuk.com/development-news/services-spotlight-omuk/ . Read 30 Sep 2026. SNIPPET.
- P8. The Last of Us Part II. Wikipedia. Current revision. https://en.wikipedia.org/wiki/The_Last_of_Us_Part_II . Read 30 Sep 2026. OPENED.
- P9. 1 hr of Voice Acting translates into how much hrs of Voice Actor work? GameDev.net forums. Undated (thread about 2016). https://gamedev.net/forums/topic/676955-1-hr-of-voice-acting-translates-into-how-much-hrs-of-voice-actor-work/ . Read 30 Sep 2026. SNIPPET; the summary may also draw on Backstage, https://www.backstage.com/magazine/article/how-long-does-voice-acting-take-76067/ .
- P10. 2025 Interactive Media (Video Game) Agreement Summary. SAG-AFTRA. June 2025 (from the URL). https://www.sagaftra.org/sites/default/files/2025-06/2025%20Interactive%20Media%20(Video%20Game)%20Agreement%20Summary.pdf ; and Inside the New SAG-AFTRA Interactive Media Agreement, Frankfurt Kurnit (Smizer, Thomas), 2025, https://technologylaw.fkks.com/post/102mewu/inside-the-new-sag-aftra-interactive-media-agreement-new-standards-for-ai-and-di . Read 30 Sep 2026. SNIPPET.
- P11. Breathing Life into Greek Myth: The Dialogue of 'Hades'. Greg Kasavin and Darren Korb, Supergiant Games, GDC 2021. https://www.gdcvault.com/play/1026975/Breathing-Life-into-Greek-Myth ; preview https://www.gamedeveloper.com/audio/dive-into-the-dialogue-of-i-hades-i-at-gdc-2021 ; interview, Echoes and Dust, February 2021, https://echoesanddust.com/2021/02/a-conversation-with-hades-composer-and-audio-director-darren-korb/ . Read 30 Sep 2026. SNIPPET.
- P12. Audio Bootcamp: Dialogue 101. Michael Csurics, GDC 2015. https://www.gdcvault.com/play/1021815/Audio-Bootcamp-Dialogue . Read 30 Sep 2026. SNIPPET.
- P12b. Anatomy of Great Voice-Over: A Casting & Recording Primer. GDC Vault; speaker and year not seen. https://www.gdcvault.com/play/1023353/Anatomy-of-Great-Voice-Over . Read 30 Sep 2026. SNIPPET.
- P13. Spot the Difference: AAA vs Indie VO Techniques (slides). Michael Csurics (2K Marin) and David Gilbert (Wadjet Eye Games), GDC 2012. https://media.gdcvault.com/gdc2012/slides/Audio%20Track/michaelCsurics/csurics_Michael_SpotTheDifference_speech.pdf . Read 30 Sep 2026. SNIPPET.
- P14. A Beginner's Guide to Dialogue Editing for Video Games. Alyx Jones (Liquid Violet), Guildford Game Audio. Undated. https://www.guildfordgameaudio.com/post/a-beginners-guide-to-dialogue-editing-for-video-games . Read 30 Sep 2026. SNIPPET (content not shown).
- P15. How Dialogue Works In Video Games. Game Audio Learning Portal. Undated. https://www.gameaudiolearning.com/knowledgebase/how-dialogue-works-in-video-games . Read 30 Sep 2026. SNIPPET.
- P16. Recommendation ASWG-R001: Average Loudness and Peak Levels of Audio Content on Sony Computer Entertainment Platforms. Sony Audio Standards Working Group. November 2012, revised (August 2013 per Wikipedia). http://gameaudiopodcast.com/ASWG-R001.pdf . Read 30 Sep 2026. SNIPPET.
- P17. Audio normalization. Wikipedia. Current revision. https://en.wikipedia.org/wiki/Audio_normalization . Read 30 Sep 2026. OPENED.
- P18. EBU R 128. Wikipedia. Current revision (the recommendation is v4.0, August 2020). https://en.wikipedia.org/wiki/EBU_R_128 . Read 30 Sep 2026. OPENED.
- P19. Dialogue editor. Wikipedia. Current revision. https://en.wikipedia.org/wiki/Dialogue_editor . Read 30 Sep 2026. OPENED.
- P20. Audio loudness for gaming: The battle against 'ear fatigue'. MCV/Develop. Undated. https://mcvuk.com/development-news/audio-loudness-for-gaming-the-battle-against-ear-fatigue/ . Read 30 Sep 2026. SNIPPET.
- P21. Using Dialogue Voices and Waves. Epic Games, Unreal Engine 4.27 documentation (a 5.4 page also listed). Undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-dialogue-voices-and-waves?application_version=4.27 . Read 30 Sep 2026. SNIPPET.
- P23. What's Your Job? Audio Dialogue Specialist. Full Sail University. Undated. https://hub.fullsail.edu/articles/whats-your-job-audio-dialogue-specialist ; and Game Dialogue Tools and Recording, Mark Estdale, LinkedIn, undated, https://www.linkedin.com/pulse/game-dialogue-tools-recording-mark-estdale . Read 30 Sep 2026. SNIPPET.
- P24. Script supervisor. Wikipedia. https://en.wikipedia.org/wiki/Script_supervisor . Read 30 Sep 2026. SNIPPET.

**Synthetic voice in professional use**
- S1. Speech Synthesis in the Context of Video Gaming. Marc-André Carbonneau, Ubisoft La Forge, GDC 2021. https://gdcvault.com/play/1027229/Speech-Synthesis-in-the-Context . Read 30 Sep 2026. SNIPPET.
- S2. Sonantic uses AI to infuse emotion in automated speech for game prototypes. GamesBeat (VentureBeat). March 2021. https://venturebeat.com/games/sonantic-uses-ai-to-infuse-emotion-in-automated-speech-for-game-prototypes/ . Read 30 Sep 2026. SNIPPET.
- S3. ARC Raiders. Wikipedia (cites Eurogamer, 10 Nov 2025, and GamesIndustry.biz, 13 Mar 2026). https://en.wikipedia.org/wiki/ARC_Raiders . Read 30 Sep 2026. OPENED.
- S4. Arc Raiders has been cutting back its AI voices. PCGamesN. 2026, exact date not seen. https://www.pcgamesn.com/arc-raiders/ai-voices-replaced ; and Arc Raiders' AI Voice Acting Is A Bigger Deal Than You Think, TheGamer, undated, https://www.thegamer.com/arc-raiders-ai-voice-acting-explained-embark-studios-nexon/ . Read 30 Sep 2026. SNIPPET.
- S5. Respeecher. Wikipedia. Current revision. https://en.wikipedia.org/wiki/Respeecher . Read 30 Sep 2026. OPENED.
- S6. Respeecher and Cyberpunk 2077: How AI Revived a Beloved Voice. Respeecher (vendor case study). Undated. https://www.respeecher.com/case-studies/how-respeecher-and-cd-projekt-red-preserved-the-voice-of-cyberpunk-2077s-viktor-vektor . Read 30 Sep 2026. SNIPPET.
- S7. James Earl Jones' Darth Vader Returns to 'Fortnite' Using AI Technology. Variety. May 2025. https://variety.com/2025/artisans/news/james-earl-jones-darth-vader-fortnite-ai-1236400633/ ; and Gizmodo, May 2025, https://gizmodo.com/fortnite-darth-vader-ai-epic-games-star-wars-james-earl-jones-2000603304 . Read 30 Sep 2026. SNIPPET.
- S9. Text-to-Speech for Games: Tools & Best Practices for Developers. Respeecher blog (vendor). Undated. https://www.respeecher.com/blog/text-to-speech-gaming-best-practices . Read 30 Sep 2026. SNIPPET.
- S10. Professional Voice Cloning. ElevenLabs documentation (vendor). Undated. https://elevenlabs.io/docs/eleven-creative/voices/voice-cloning/professional-voice-cloning . Read 30 Sep 2026. SNIPPET.

**Models and speech research**
- M1. Chatterbox README and example_tts_turbo.py. Resemble AI, GitHub master. File undated. https://github.com/resemble-ai/chatterbox . Read 30 Sep 2026. OPENED.
- M2. Chatterbox source, src/chatterbox/tts.py and tts_turbo.py. Resemble AI, GitHub master. https://github.com/resemble-ai/chatterbox/tree/master/src/chatterbox . Read 30 Sep 2026. OPENED.
- M3. Chatterbox LICENSE (MIT, "Copyright (c) 2025 Resemble AI"). https://github.com/resemble-ai/chatterbox/blob/master/LICENSE . Read 30 Sep 2026. OPENED.
- M4. Hugging Face cards ResembleAI/chatterbox and ResembleAI/chatterbox-turbo. Resemble AI. Turbo page updated about 15 Dec 2025. https://huggingface.co/ResembleAI/chatterbox , https://huggingface.co/ResembleAI/chatterbox-turbo . Read 30 Sep 2026. SNIPPET.
- M5. Chatterbox gains Nano, pull request #4. MaroonedSoftware/rhapsode. Says Nano merged upstream 21 Jul 2026. https://github.com/MaroonedSoftware/rhapsode/pull/4 . Read 30 Sep 2026. SNIPPET. The Nano card (https://huggingface.co/ResembleAI/chatterbox-nano) was not read.
- M6. Chatterbox example_vc.py and src/chatterbox/vc.py. Resemble AI. https://github.com/resemble-ai/chatterbox/blob/master/example_vc.py . Read 30 Sep 2026. OPENED.
- M7. TTS keeps inserting british accent, issue #267. Zsnack. 8 Sep 2025. https://github.com/resemble-ai/chatterbox/issues/267 . Read 30 Sep 2026. OPENED.
- M8. Chatterbox-TTS-Extended README. petermg. Undated. https://github.com/petermg/Chatterbox-TTS-Extended . Read 30 Sep 2026. OPENED.
- M9. chatterbox-fastrtc-realtime-emotion README. dwain-barnes. Undated. https://github.com/dwain-barnes/chatterbox-fastrtc-realtime-emotion . Read 30 Sep 2026. OPENED.
- M10. VoxCPM README. OpenBMB, GitHub main (news entries to April 2026). https://github.com/OpenBMB/VoxCPM . Read 30 Sep 2026. OPENED.
- M11. VoxCPM2 Technical Report, arXiv 2606.06928. Zhou et al., OpenBMB. 5 Jun 2026. https://arxiv.org/abs/2606.06928 . Read 30 Sep 2026. OPENED (abstract, via arXiv's API).
- M12. Pocket TTS README. Kyutai, GitHub main. https://github.com/kyutai-labs/pocket-tts . Read 30 Sep 2026. OPENED.
- M13. kyutai/pocket-tts, Hugging Face card (weights CC-BY-4.0, cloning gated). Kyutai. Undated. https://huggingface.co/kyutai/pocket-tts . Read 30 Sep 2026. SNIPPET.
- M14. Continuous Audio Language Models, arXiv 2509.06926. Kyutai. 8 Sep 2025. https://arxiv.org/abs/2509.06926 . Read 30 Sep 2026. OPENED (abstract).
- M15. Pocket TTS: a high-quality TTS with voice cloning that runs on CPU. Kyutai blog. 13 Jan 2026. https://kyutai.org/blog/2026-01-13-pocket-tts/ . Read 30 Sep 2026. SNIPPET (title and date only).
- M16. Add new default voices for each new language to avoid english accents, issue #166. kyutai-labs/pocket-tts. Undated. https://github.com/kyutai-labs/pocket-tts/issues/166 . Read 30 Sep 2026. SNIPPET.
- M17. ReStyle-TTS: Relative and Continuous Style Control for Zero-Shot Speech Synthesis, arXiv 2601.03632. 7 Jan 2026. https://arxiv.org/abs/2601.03632 . Read 30 Sep 2026. OPENED (abstract).
- M18. Singlish, Can or Not? Fine-Tuning and Evaluating Zero-Shot TTS for Singapore English, arXiv 2607.23027. 25 Jul 2026. https://arxiv.org/abs/2607.23027 . Read 30 Sep 2026. OPENED (abstract).
- M19. CSTR VCTK Corpus (version 0.92). University of Edinburgh, CSTR. Undated page. https://datashare.ed.ac.uk/handle/10283/3443 . Read 30 Sep 2026. SNIPPET.
- M20. The Edinburgh International Accents of English Corpus. University of Edinburgh. 2023 (arXiv 2303.18110). https://datashare.ed.ac.uk/items/355c07b4-500d-4e80-8f12-225e646293c9 . Read 30 Sep 2026. SNIPPET.
- M21. Chatterbox TTS Guide: How to Control Emotion and 22 Languages with Text Alone. deAPI.ai blog (third party). Undated. https://deapi.ai/blog/chatterbox-tts-guide-how-to-control-emotion-and-22-languages-with-text-alone . Read 30 Sep 2026. SNIPPET.

**Voice conversion**
- V1. Seed-VC README and LICENSE (GPL-3.0). Plachtaa, GitHub main. https://github.com/Plachtaa/seed-vc . Read 30 Sep 2026. OPENED. Weights card https://huggingface.co/Plachta/Seed-VC . Read 30 Sep 2026. SNIPPET.
- V2. Retrieval-based-Voice-Conversion-WebUI LICENSE (MIT, 2023). RVC-Project. https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI . Read 30 Sep 2026. OPENED for the licence; "≤10 mins" and the pretrained weights' location SNIPPET.
- V3. kNN-VC README and LICENSE (MIT, 2023, MediaLab, Stellenbosch University). https://github.com/bshall/knn-vc . Read 30 Sep 2026. OPENED.
- V4. OpenVoice README and LICENSE (MIT since April 2024). MyShell.ai. https://github.com/myshell-ai/OpenVoice . Read 30 Sep 2026. OPENED.

**Project records read for context** (not re-researched): the character-pipeline research of 25 September; ACCENT-KEEPING and SCOTTISH-CHECK of 29 September; the acting README of 29 September; the live-speech SUMMARY and RECHECK; the TTS licensing SUMMARY; DECISIONS.md; FINDINGS.md; the voice-engines spec (production/specs/voice-engines.json); and the voice-server, acting-test and voxcpm_takes scripts (tools/voice-live/).
