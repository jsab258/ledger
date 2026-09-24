# Cast voices: older northern English reference voices - research notes

Researched 2026-09-24. Nothing downloaded (the two PDFs below were cached by the fetch tool itself and only text-searched).
Labels: OPENED = page/paper read; SNIPPET = search-result summary only, not read. LICENCE / TERMS / MEASURED / CLAIM as asked.
"Date" = the source's own date where shown; otherwise "n.d., accessed 2026-09-24".

---

## 1. Open corpora

### 1a. OpenSLR SLR83 - Google "Crowdsourced high-quality UK and Ireland English Dialect speech"
- LICENCE: CC BY-SA 4.0. https://www.openslr.org/83/ - n.d., accessed 2026-09-24 - OPENED.
- CAUTION on that page: its per-dialect numbers (e.g. "Northern English male 2,097") are LINE counts, not speakers. The paper's table (below) gives Northern English = 5 female + 14 male speakers (750 + 2,097 lines, ~150 lines each). Totals check: 120 speakers, 17,877 lines.
- Paper: Demirsahin, Kjartansson, Gutkin, Rivera, "Open-source Multi-speaker Corpora of the English Accents in the British Isles", LREC 2020, pp. 6532-6541. https://aclanthology.org/2020.lrec-1.804.pdf - 2020 - OPENED (text extracted).
  - TERMS/CONSENT (strongest found anywhere): "All volunteers signed a data release consent form allowing their recorded utterances to be placed in public domain with no restriction on academic, commercial or private use." Paper also says the corpora are "intended for speech technologies" and released "with no limitations on academic or commercial use". Recording guidelines are Google's crowdsourced TTS-corpus guidelines.
  - Ages: only "volunteers above 21 years of age". NO per-speaker age metadata. CLAIM (inference): Google London employees -> mostly working-age, probably few over 50.
  - Accent: self-identified; survey asked where they grew up "in or near London, Essex, Manchester, Leeds, Cardiff, Edinburgh, Glasgow" or other; grouped into Kortmann's three English regions. So "Northern" = Manchester/Leeds-type, not Hull/Grimsby specifically; no per-speaker locality published. Paper admits no sociolinguistic profile was taken.
  - Quality: Rode M5 mic, Blue Icicle, 48 kHz/16-bit, sound-insulated room in London (quiet rooms in Cardiff), 30 cm mic distance enforced. Studio-grade for cloning. ~150 read sentences (~15 min) per speaker.
  - Risk to note: ShareAlike. Whether synthetic speech generated from a CC BY-SA reference clip is an "adapted work" that must itself be CC BY-SA is unsettled; VCTK (CC BY 4.0) has no SA term. Needs an allowlist check before use.

### 1b. Mozilla Common Voice (now distributed only via Mozilla Data Collective)
- Distribution moved: "Effective October 2025, Mozilla Common Voice datasets are now exclusively available through Mozilla Data Collective". https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0 - accessed 2026-09-24 - OPENED.
- LICENCE: CC0-1.0. TERMS on download: "you will not re-host or re-share this dataset"; "not to attempt to determine the identity of speakers". Stated intended use: training/evaluating ASR, CALL, language revitalisation. No statement on TTS/cloning either way. https://mozilladatacollective.com/datasets/cmfzu8u8wa555eq8onrk334h4 - accessed 2026-09-24 - OPENED.
- TERMS (contributor side), Common Voice legal terms dated 31 October 2025: contributors agree Mozilla may offer contributions "under the CC0 public domain dedication" and make recordings "publicly available"; framing is a database "anyone can use to make innovative voice recognition apps"; no explicit mention of speech synthesis. https://commonvoice.mozilla.org/terms/%7B%7B*%7B%7Blanguage_code%7D%7D*%7D%7D.html - OPENED (via tool summary).
  - Assessment (CLAIM, mine): CC0 waives copyright/neighbouring rights; it does not by itself waive personality or data-protection rights. Consent basis = anonymous volunteer + public-domain dedication, framed for recognition. Same class of risk as VCTK, arguably slightly weaker (volunteers were told "recognition"). Fits the developer's "anonymous corpus volunteers, stated risk" ruling but needs his yes.
- Metadata / MEASURED (dataset card): "Common Voice Scripted Speech 26.0 - British English", MDC-derived subset, released 2026-07-20, CC0. Accent tags are self-declared, multi-select free text. Counts: England English 171,945 clips; Lancashire 2,628; Liverpool 2,628; Yorkshire 204 clips (0.09%). Age bands present: fifties 7.1%, sixties 6.2%, seventies 1.6%, eighties 0.1%. https://mozilladatacollective.com/datasets/cmrt6zrob000zmm07yqwjlpwi - OPENED.
  - So older + Yorkshire speakers exist but are few; Hull/Grimsby/Lincolnshire tags not seen in the summary (the full English release may have more free-text tags; not checked row-level, nothing downloaded).
  - Quality: CLAIM (general knowledge, not measured here): browser recordings on consumer mics, short clips (~3-6 s) -> several clips from one client_id would have to be joined to reach ~10 s; noise and room vary widely.

### 1c. LibriVox / LibriTTS
- LibriVox recordings are dedicated to the public domain; "Anyone can use all LibriVox recordings however they wish (even to sell them)". https://librivox.org/pages/public-domain/ and https://creativecommons.org/2008/06/02/librivox-1500-public-domain-audio-books/ - SNIPPET. LICENCE: PD dedication.
- Problems: readers are NAMED on every recording (identifiable -> conflicts with the no-identifiable-people rule more than anonymous corpora); no age/accent metadata; mostly US. Older British readers exist but finding a Yorkshire one means listening by hand. Consent to synthesis: none stated. LibriTTS licence not verified in this pass.

### 1d. Emilia / GigaSpeech (scraped web audio)
- Emilia: CC BY-NC 4.0 (non-commercial); Emilia-YODAS: CC BY 4.0. Audio is "in-the-wild" video/podcast speech; "Emilia does not own the copyright to the audio files". No age/accent metadata. https://huggingface.co/datasets/amphion/Emilia-Dataset - OPENED. LICENCE.
- GigaSpeech: users agree to "non-commercial research and educational purposes" only. https://huggingface.co/datasets/speechcolab/gigaspeech - SNIPPET. TERMS.
- Verdict: both are recordings of identifiable podcasters/YouTubers with no consent to cloning -> fail the allowlist. Do not use.

### 1e. ELRA British English corpora
- UK English Speecon (ELRA-S0215): 606 adults, "103 speakers are over 46"; 4 mics x office/car/public/entertainment; 16 kHz; no dialect regions listed; commercial licence EUR 75,000 (non-member). https://catalogue.elra.info/en-us/repository/browse/ELRA-S0215/ - OPENED. LICENCE.
- British English SpeechDat(II) FDB-4000 (ELRA-S0097): 4,000 speakers, 1,298 aged 46-60; recorded "over the British fixed telephone network"; commercial EUR 55,000 (non-member). https://catalogue.elra.info/en-us/repository/browse/ELRA-S0097/ - OPENED. LICENCE.
- Verdict: expensive, 16 kHz/telephone, consent was for recognition products, no region filter published. Not worth it.

### 1f. Survey of English Dialects (Leeds, 1950s)
- "Copyright in all Survey of English Dialects material resides with the University of Leeds." Reproduction/publication needs written consent from the Head of Special Collections. Audio: 311 discs, 96 reel tapes; minidisc copies consultable in the searchroom. https://explore.library.leeds.ac.uk/special-collections-explore/409355 - OPENED. TERMS.
- Verdict: right accents and right ages (elderly rural informants), but named informants, no synthesis consent, 1950s field-tape quality, case-by-case permission. Useful as an accent REFERENCE for ears, not as clone sources.

### 1g. BBC Voices (2004-2005)
- 303 locations, 1,293 people, group conversations recorded by BBC Local Radio May 2004 - July 2005; held at British Library Sounds; "can be played by anyone"; download for academic use in licensed UK HE/FE. https://sounds.bl.uk/Accents-and-dialects/BBC-Voices - SNIPPET. TERMS.
- Verdict: BBC copyright, named participants, group-conversation audio. Listening reference only.

### 1h. IViE (Oxford)
- 108 speakers, all aged 16, recorded in schools incl. Leeds, Bradford, Newcastle, Liverpool. https://www.phon.ox.ac.uk/files/apps/IViE/ - SNIPPET. Wrong age group. Licence not checked.

### 1i. ABI-1 (Accents of the British Isles)
- Includes Hull (East Yorkshire) and Burnley: 20 speakers per locality (10F/10M), "born in the region and had lived there for all of their lives"; each read a 92-word passage (30-45 s) plus 20 prompt texts. Hanani, Russell, Carey, Interspeech 2011. https://www.isca-archive.org/interspeech_2011/hanani11_interspeech.pdf - OPENED (text extracted). MEASURED (for accent ID, not cloning): text-dependent accent ID 95.18%; human listeners 58.25%.
- Licence and speaker ages: NOT found (ABI-1 was a Birmingham/SRL research corpus; distributor page shachi.org returned 503). CLAIM: not openly licensed; would need a licence negotiation and consent was for research. The one corpus with genuine lifelong Hull speakers - worth one email if the other routes fail.

---

## 2. Commercial routes

### 2a. Hiring local actors
- Equity-recommended game voice minimums (UK): GBP 300/hour session (big-budget games), GBP 200/hour walla, GBP 800 half-day group; "vocally stressful" sessions max 2 h. Source is a voice actor's blog quoting Equity's rate card (post 2023-09-13, updated 2024-07-28): https://www.martinwhiskin.co.uk/post/how-much-can-i-earn-as-a-voice-actor - OPENED. CLAIM (secondary; equity.org.uk blocked to the fetch tool, rate card not read directly). Other UK VO blogs say sessions GBP 250-350/hour plus a separate buyout (SNIPPET).
- Equity AI toolkit (2023, with Dr Mathilde Pavis): template AI contract for performance-cloning work, model AI clauses, take-down notice; principles: consent for past/current/future performances, fair remuneration, collective agreement. https://www.televisual.com/news/equity-launches-toolkit-on-ai-performance-cloning/ and https://deadline.com/2023/06/equity-ai-toolkit-performance-cloning-consent-sag-aftra-1235409450/ - SNIPPET. TERMS.
- UK context: Deadline 2025-10 reports AI terms are "not standard practice in the UK right now"; Equity members voted for industrial action over AI (Variety 2025). https://deadline.com/2025/10/uk-actors-contracts-ai-deadlock-1236596326/ - SNIPPET. No standard UK fee for a cloning buyout was found.
- SAG-AFTRA 2025 Interactive Media Agreement (ratified July 2025, 95% yes): consent must be "separately signed or initiated" and "reasonably specific" (game, role, whether real-time generation); minimums for digital-replica use; real-time generation at higher minimums (reported 7.5x scale); protections trigger only when output is "objectively identifiable" as the performer. https://www.dglaw.com/sag-aftras-new-video-game-agreement/ (2025-11-06) - OPENED. TERMS. (sagaftra.org returned 403.) Not binding on a Swiss studio hiring UK non-SAG talent, but it is the best template for what a consent form should say.
- Availability (SNIPPET): Hull/East Yorkshire VO artists are listed on thevoicerealm.com, voices.com (England > Yorkshire & Humber), voiceovers.co.uk/accent/yorkshire, qvoice.co.uk.
- CLAIM (my estimate, unsourced): 1-2 h per voice at GBP 250-350/h + studio + a negotiated synthesis buyout -> roughly GBP 500-1,500 per voice; a non-actor older local recorded at a home-studio with a paid consent could be less.
- RULE CONFLICT: the allowlist forbids cloning "identifiable real people". A hired, consenting private person is identifiable. This route needs an explicit ruling from Jafar (licence allowlist = his).

### 2b. Voice marketplaces
- ElevenLabs Voice Library: voices shared by their owners (Professional Voice Clone + voice captcha verification); paid users get commercial use; owner payouts per 1,000 characters. https://elevenlabs.io/docs/eleven-creative/voices/payouts - SNIPPET.
- ElevenLabs Prohibited Use Policy, last updated 17 Aug 2026 - OPENED - TERMS: s.5 forbids "using ElevenLabs audio output to intentionally replicate the voice of another person without consent"; s.9(l) forbids using Output "as part of a dataset ... for training, fine-tuning, developing, testing" any ML. https://elevenlabs.io/use-policy
  - => Using an ElevenLabs Library voice's output as a Chatterbox reference clip is prohibited. The only legal use is generating the lines inside ElevenLabs (paid plan), which leaves our local Chatterbox + Perth-watermark pipeline.
- ElevenLabs ToS (non-EEA) effective 31 Mar 2026: paid users may use Services commercially; "you retain all rights in and to your Output". https://elevenlabs.io/terms-of-use - OPENED. Voice Library Addendum last updated 6 Mar 2026: https://elevenlabs.io/vla - OPENED.
- Resemble AI marketplace: "40+ AI voices", commercial licence on paid plans, used inside Resemble's platform. https://www.resemble.ai/resemble-voice-marketplace/ - SNIPPET. Not a source of reference clips for local Chatterbox.
- Voices.com "Branded AI Voice": three-stage consent (platform opt-in, sample-clone approval, job-specific usage agreement); enterprise, custom quote. https://www.voices.com/solutions/ai-voice - SNIPPET. CLAIM: priced for brands, likely far above an indie budget.
- Replica Studios (SAG-AFTRA-licensed game voices) shut down 30 June 2025. https://multilingual.com/replica-studios-shutdown-2025/ - SNIPPET.

### 2c. Data protection (applies to any route with living people)
- ICO: voice recordings are personal data; they become special-category biometric data when processed to identify/verify a person; explicit consent is then usually the only basis. https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/biometric-data-guidance-biometric-recognition/key-data-protection-concepts/ - SNIPPET. TERMS. Cloning for a game character is arguably not "identification", but the recording is still personal data; a hiring contract should be a licence plus a data-protection notice. (Not legal advice; not checked against Swiss FADP.)

---

## 3. Technical

- MEASURED, and directly on our engine: "Singlish, Can or Not? Fine-Tuning and Evaluating Zero-Shot TTS for Singapore English", arXiv 2607.23027, 2026-07-25 - OPENED. Off-the-shelf zero-shot systems prompted with a Singlish reference "preserve speaker timbre but flatten the accent". Chatterbox accent similarity (ACC-SIM match) 0.5114 zero-shot -> 0.6376 after fine-tuning; CosyVoice 3 0.5771 -> 0.6036. Gains held on unseen speakers. https://arxiv.org/html/2607.23027
  - Implication: a perfect Hull reference clip will still come out partly flattened toward generic English. Fine-tuning on a few hours of the target accent measurably helps.
- Chatterbox controls (README, OPENED, https://github.com/resemble-ai/chatterbox, MIT): exaggeration and cfg_weight only; no age or accent control; README warns output "may inherit the accent of the reference clip's language" and suggests cfg_weight 0 to reduce cross-language accent bleed. Includes a voice-conversion example (example_vc.py) - functionality not documented in README. Perth watermark on every output. CLAIM.
  - Idea (CLAIM, untested): Chatterbox VC keeps the source recording's delivery and swaps timbre, so accent can come from one person's performance and timbre from another reference.
- VoiceShop (arXiv 2404.06674, 2024-04-10, OPENED): zero-shot speech-to-speech editing of "age, gender, accent, and speech style" while keeping identity. No numbers in abstract; no code/licence found. CLAIM.
- Scalable Controllable Accented TTS (arXiv 2508.07426, 2025-08-10, OPENED): accent labels from a speech-geolocation model on Common Voice, kNN-VC timbre augmentation; beats XTTS-v2 fine-tuned on self-reported labels. Which accents: not stated in abstract. CLAIM.
- Age: Voice Aging with Audio-Visual Style Transfer (arXiv 2110.02411) - SNIPPET, CLAIM; Perceptual evaluation of age disguise (arXiv 1804.08910, 2018, OPENED) - MEASURED, human speakers only: listeners heard intended "elderly" voices as older for both sexes. No open, measured tool was found that ages a cloned voice convincingly. DSP (lower pitch, slower rate, added jitter) is the cheap fallback; unmeasured.
- Evaluation frameworks exist (Pairwise accent similarity, arXiv 2505.14410, 2025-05-20, Edinburgh authors; TTS voice reconstruction over 17 zero-shot systems, arXiv 2606.21343, 2026-06-19) - OPENED abstracts, no age/accent numbers in abstracts.

---

## Bottom line (my reading)
1. No open corpus has studio-quality, Hull/Grimsby, 45-75 speakers with synthesis consent. The nearest pieces: SLR83 Northern (best consent, studio quality, 19 speakers, but no ages and Manchester/Leeds rather than Hull; ShareAlike question) and Common Voice (CC0, has fifties-seventies and a few Yorkshire tags, phone-grade, consent framed for recognition).
2. Marketplace voices cannot be used as Chatterbox references (ElevenLabs forbids it in writing).
3. Chatterbox measurably flattens regional accent from a reference clip; fine-tuning fixes part of it.
4. Cheapest sound route: audition older Common Voice speakers tagged Yorkshire/Northern (free, fits the existing anonymous-volunteer ruling) for the older roles; if the accent flattens, as measured, fine-tune on SLR83 Northern after clearing ShareAlike. Only if still short: record 3-4 older Hull/Grimsby locals with a written synthesis consent modelled on the SAG-AFTRA/Equity clauses, which needs an allowlist ruling.
