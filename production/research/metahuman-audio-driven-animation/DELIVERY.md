# Epic's audio-driven facial animation for MetaHumans: the detail

Research, 30 September 2026, by a separate research helper (about thirty minutes of reading). Companion to SUMMARY.md. It builds on production/research/lip-sync/NOTE-2026-09-30.md ("the lip-sync note"), which read the installed UE 5.8.2 engine source. This helper could not read the engine source and has not re-verified what that note found in it.

(The helper returned its text; the session that asked for it saved it here. That session checked the project facts in L2, L4 and L6 against the files: the 9.98 GB card, the head look-at's 60° and 0.2 s, the mouth node's 11 curves, and the gaze note's 4°. It replaced a "roughly 3.5 s" start-of-speech figure, which does not come from the real path, and reworded the graphics-memory line; nothing else was changed.)

Labels: **OPENED** means the helper read the page. **SNIPPET** means only a search-engine summary was seen, because the page was blocked or not opened. Bracketed IDs refer to the source list at the end.

Reach: only Epic's documentation site and GitHub opened. Epic's forums, metahuman.com, unrealengine.com, Fab, arXiv, the ACM library, NVIDIA's docs, Speech Graphics, Georgy Dev, GDC Vault, gameanim.com and all news sites were blocked by the network proxy. Most of section (a) and every third-party claim is therefore SNIPPET-level.

## (a) The professional facial-dialogue pipeline and its layers

### Established practice

1. **Tiering: decide what each line gets.**
   - Hogwarts Legacy (WB Avalanche): "gold" cutscenes used performance-captured upper faces with Speech Graphics' audio-driven lip-sync. "Silver" and "bronze" scenes, the large majority, were audio-driven alone. Over 50,000 lines per language, in 8 languages, ran through an automated pipeline on the build server [P4].
   - The Witcher 3: a 14-person dialogue team. A generator took three inputs (actor information, cinematic instructions, and data extracted from the voice-over as markers or accents) and produced fully animated scenes, which were then polished. The building blocks were about 2,400 dialogue animations, sorted by character type and pose [P1].
   - Cyberpunk 2077: "largely automatic but under animator control", from audio plus tagged transcripts, in ten languages. Language models drive the mouth and the "paralingual" motion of neck, brows and eyes; "directorial tags" in the transcript bring in performance-captured facial emotion [P2].
2. **Lip-sync layer.**
   - Classic method: phonemes become visemes, blended into each other. Half-Life 2 (2004) extracted phonemes into the WAV file and drove FACS-style controllers, combined with expressions and gestures in Face Poser [P7].
   - JALI (2016) separates the jaw's contribution from the lips' and varies the balance with speaking style: over-enunciation is mostly lips, mumbling mostly jaw, normal speech a mix [P3].
   - Current method: learned audio-to-rig models (Speech Graphics SGX, NVIDIA Audio2Face, Epic xADA). SGX and JALI can also use the transcript.
3. **Expression and emotion layer.** Kept separate from the mouth. It is driven by direction tags [P2], or detected from the audio (SGX's "full-face emotional expressions" [P5]; xADA's auto-detect or override [E1, E15]).
4. **Blinks.** Mean 17 a minute at rest, 26 while talking, 4.5 while reading (150 adults) [P12]. SGX and Epic's 5.8 real-time model generate blinks procedurally [P5, E10].
5. **Eye gaze and saccades.** "Eyes Alive" (2002) modelled saccades from eye-tracking statistics; gaze differs between speaking and listening [P9]. Ruhland et al. (2015) review eyes, eyelids and head together [P10]. SGX generates "eye darts" [P5].
6. **Head motion.** It correlates with the voice's pitch and loudness, and natural head motion measurably improves understanding of speech in noise [P11]. xADA's research model and SGX generate it [E15, P5]. Epic's offline solve can too, but Epic's real-time algorithm "does not produce head motion" [E1].
7. **Body gesture.** A library of conversation animations, triggered at markers [P1].
8. **Sync tolerance.** ITU-R BT.1359-1 (1998): viewers notice sound more than about 45 ms ahead of the picture, or more than about 125 ms behind it. Acceptability runs to about +90 / −185 ms (sources give −185 to −190) [P13]. A face slightly ahead of its sound is far safer than one behind it.
9. **Runtime speech at scale.**
   - Speech Graphics SG Com claims 50 ms latency on the device's CPU [P5].
   - Epic's Fortnite characters speak generated voices: Darth Vader in May 2025, and UEFN "Conversations" in April 2026 (Gemini and ElevenLabs) [P16].
   - How those faces are animated is not documented in anything reached. The personas page says only that creators can "add facial animations".
10. **Warning case.** Mass Effect: Andromeda (2017): press and animators blamed its mocked faces on procedural, largely FaceFX-driven automation at scale (about 41 hours of dialogue reported) without enough polish [P8]. Secondary sources only.

### What this means for LEDGER (the helper's reading, not established practice)

- The principal characters' lines are generated in play, so there is no hand-polished tier for them. All quality has to come from automatic layers, composed explicitly.
- The pre-made lines can get a higher tier: the offline bake.
- The emotion should come from the dialogue system's intended mood, as studios use tags, not from voice tone alone. The project's own casting notes already call one voice "flat, artificial".

## (b) Epic's audio-driven animation

### The model

"xADA: Controllable and Expressive Audio-Driven Animation", an Epic paper at SIGGRAPH 2025 [E15], also presented at Unreal Fest Orlando 2025 [E14]. From the abstract (SNIPPET):

- a Whisper audio encoder feeds GRU decoders, which output MetaHuman-compatible rig controls;
- it animates the face, tongue, head and blinks;
- it can express 21 emotions or blends of them, detected automatically or overridden, with blink timing also overridable;
- it generalises across languages, singing, coughs and laughter;
- it "supports both offline and streaming character speech animation in Unreal Engine".

### Form 1: offline Audio Driven Animation (MetaHuman Animator)

- **Versions.**
  - UE 5.5: Experimental [E13].
  - 5.6 added head movement, frame range, the "Realtime Audio" option, a blinks toggle, a process mask and mood overrides [E1].
  - 5.8 brought "a new real-time model" and "cleaner activation on key poses" [E6].
- **Setup** [E1, OPENED; page dated 3 Nov 2025]:
  1. Enable the MetaHuman Animator plugin.
  2. Create a MetaHuman Performance asset.
  3. Set Input Type to Audio, then choose the SoundWave and the MetaHuman face mesh.
  4. Click Process.
  5. Export as an Animation Sequence or a Level Sequence.
- **Options:**
  - Downmix Channels.
  - Generate Blinks.
  - Head Movement.
  - Realtime Audio: uses the real-time algorithm, gives no head motion, and hides the other options.
  - Process Mask: full face, or only the mouth curves "which you can use to swap/layer alternative lip animations".
  - Mood: Auto Detect, Neutral, Happy, Confident, Excited, Playful, Sad, Bored, Fear, Confused, Disgust, Anger or Surprise, with an intensity.
- **Output.** Face-rig animation tracks at a fixed 30 fps. This is a known 5.8 issue with no workaround [E8]; the 5.8 notes keep audio-only at 30 fps "to match the processing rate" [E7].
- **Packaged game.** The baked result is an ordinary animation, so it plays in a packaged game. The solving itself is editor-only: the lip-sync note names the module MetaHumanSpeech2Face, and the 5.8 notes call MetaHuman Animator an "editor-only solution; not a runtime or player-facing feature" in their Linux/macOS item [E6].
- **Hardware.** Epic's pages state no requirement. Not verified on AMD.
- **Fit.** The pre-made wav lines only.

### Form 2: real-time "MetaHuman (Audio)" Live Link source

- **Versions.**
  - 5.6 (3 June 2025) [E12, E3].
  - 5.7: mood override for real-time audio, and a Blueprint interface for real-time sources [E11].
  - 5.8: a new real-time audio model with procedural blinks ("drawn from a library of motion-captured blinks" at a natural frequency) and automatic emotion detection [E10]; also the Live Link preset can be set or cleared at runtime [E7].
- **Setup** [E2, OPENED; 25 Jun 2026]:
  1. Live Link, then Add Source, then MetaHuman (Audio).
  2. Choose the audio device, name the subject, and Connect.
  3. Optionally set a mood override (Neutral, Happy, Confident, Excited, Playful, Bored, Fear, Confused, Disgust, Anger, Surprise) with an intensity.
  4. On the character, set Live Link Subject and tick Use Live Link [E4].
- **Input.** "Any connected USB (UVC compliant) audio capture device" [E2]. There is no documented way to push PCM into it. A forum thread says the source's C++ API is not open and the preset stores the device's ID [E16]. A second thread asks exactly our question (ElevenLabs PCM chunks into xADA, UE 5.7); its replies could not be read [E17].
- **Cost.** "Can be computationally expensive and utilize the GPU" [E3]; no figures given.
- **Head motion.** None; the real-time algorithm produces none [E1].
- **Fit.** None for LEDGER. Routing speech through a virtual audio cable would mean installing an audio driver on players' PCs, which is not acceptable in a shipped game (the helper's judgement).

### Form 3: "Streaming Audio Driven Animation" (StreamingADA, module SpeechAnimationSolver)

- **Status.** A hidden beta plugin in the installed 5.8.2 engine (lip-sync note). No Epic page or release note reached mentions it; the 5.8 notes say only "a new real-time model" [E6, E7].
- **Runtime evidence.** GitHub's code-search index shows the plugin file declaring the module SpeechAnimationSolver as "Type": "Runtime" in two third-party copies [T3]:
  - a copy of the engine source;
  - a public dump of Fortnite's files, which suggests Epic ships it in Fortnite.

  Neither repository could be opened, and their provenance is unverified.
- **Interface** (from the lip-sync note, not re-verified here):
  - takes float audio of any chunk size and sample rate, resampled internally to 16 kHz mono;
  - returns one frame every 20 ms: 81 face controls (jaw, lips, tongue, brows, blinks, 12 moods);
  - accepts a Mood input and a reset flag at each line's start;
  - runs 80 ms ahead of its output (lookahead);
  - loads the model `/StreamingADA/xsada_face_base_fp32_v2_0_0` (34 MB);
  - Epic's own utility converts the controls to 251 raw face curves;
  - backends: ONNX Runtime on the CPU, or DirectML on the graphics card.
- **Corroboration** (SNIPPET):
  - The Fab plugin "MetaHuman Audio to Face Runtime" lists StreamingADA as a 5.8 dependency, offers begin/feed/end audio-stream calls for text-to-speech, and claims no pre-baking [T1].
  - Georgy Dev's "mood-enabled realistic model" has 81 controls, 12 moods and 20 ms frames at 16 kHz, and "runs on CPU, not GPU" [T2].
  - The matching numbers suggest the same model family. That is an inference, not a fact.
- **Blinks and emotion.** 5.8's real-time model has them [E10]. Whether that model is the one in StreamingADA's file is unverified.
- **Head motion.** Expected none (see Form 2). Verify.
- **Packaged game.** Unverified whether the model is cooked into the package. It loads by path, so its content folder must be added to the always-cook list (lip-sync note).
- **Hardware.**
  - ONNX Runtime on the CPU runs on any x64 processor.
  - DirectML runs on any DirectX 12 GPU from AMD GCN 1 onward [M1]; the RX 6700 (RDNA 2) qualifies.
  - UE 5.8 moved NNERuntimeORT to ONNX Runtime 1.24.3 and DirectML 1.15.4, and dropped NPU support from the DirectML runtime [E7].
  - DirectML is in maintenance mode; Microsoft points Windows 11 24H2 and later to Windows ML [M1]. That is a long-term risk for the graphics-card route, not the processor route.
- **Risks.** Hidden, beta and undocumented; it may change or vanish in 5.9. Pin the engine at 5.8.x until it is proven.

### Licence

- **Epic.** Epic's plugins and content are covered by the Unreal Engine EULA. Since 5.6 (June 2025), MetaHuman sits under the standard EULA: free under $1M a year in revenue; usable in "workflows that incorporate artificial intelligence technology", but never to train or enhance AI models [E18, SNIPPET]. Running Epic's model at runtime trains nothing. The EULA text itself could not be reached.
- **Project process.** The licence allowlist requires a decision record citing the weights' licence for any new tool. Here the weights are Epic content under the Unreal EULA.
- **Separate finding for Jafar.** The allowlist line "Faces: Audio2Face-3D (MIT)" is inaccurate:
  - MIT covers only the SDK, the Maya plugin and the UE plugin;
  - the Audio2Face-3D weights are under the NVIDIA Open Model License;
  - the Audio2Emotion weights are "Custom (use allowed with Audio2Face only)" [N2, OPENED];
  - it needs an NVIDIA GPU [N1].

## (c) Performance

### Every published figure found

| Figure | Source | Conditions | Label |
|---|---|---|---|
| No cost figure for any Epic audio solve | [E1, E3, E6, E7, E8] | Epic says only that the Live Link video and audio sources "can be computationally expensive and utilize the GPU", and advises capping the frame rate (t.maxfps) so animation keeps up | OPENED |
| Offline audio output fixed at 30 fps | [E8, E7] | 5.8 | OPENED |
| Streaming solver: 50 frames a second, 80 ms lookahead, 34 MB model (fp32) | lip-sync note | Read from the installed source; not a cost measurement | project |
| Similar paid model runs on the CPU; processes every 10 ms by default; 20 ms frames at 16 kHz; larger chunks lower CPU load | [T2] | Georgy Dev plugin; no millisecond figures reached | SNIPPET |
| 50 ms latency, on the device's CPU | [P5] | Speech Graphics SG Com; vendor claim | SNIPPET |
| Audio2Face-3D: regression model needs a 0.52 s audio chunk per frame; diffusion v3.0 takes 1 s chunks and returns 30 frames; about 180 million parameters | [N4] | NVIDIA paper | SNIPPET |
| Audio2Face-3D SDK "faster than 60 FPS frame generation" | [N1] | NVIDIA GPU, CUDA 12.8 or later, TensorRT 10.13 or later | OPENED |
| Audio2Face local inference needs an NVIDIA Ampere, Ada or Blackwell GPU and about 2.9 to 4.4 GiB of VRAM; several simultaneous sessions may be unstable | [N3] | ACE UE plugin 2.5 (UE 5.5/5.6) | SNIPPET |
| RigLogic 5.8 changes, no figures: FP16 on Windows desktop; cooked DNA restores its initialised state; optional single-threaded ML for small models; joints-only ML rigs faster on CPU | [E6, E7] | The face rig costs this whichever driver moves the mouth | OPENED |

### Helper's estimate (not a measurement)

- 34 MB at 32-bit is about 8.5 million weights.
- If each 20 ms step runs the whole network once, that is about 17 million multiply-adds per step, roughly 1 GFLOP/s per speaking character: well under a millisecond per step on one core of this six-core processor.
- If the encoder re-reads a sliding window of past audio every step (Whisper-style encoders work on windows), the cost could be 10 to 100 times higher: up to a few milliseconds per step, off the game thread if written that way.
- Only measurement settles it.

### Unmeasured: the list to measure

1. CPU time per step, and its spread, for each backend.
2. Real-time factor.
3. Model load time.
4. Latency to the first output.
5. RAM and VRAM.
6. Frame-time impact in the street, through the conversation camera.
7. Contention with the voice engine on the graphics card.
8. Whether DirectML starts on this RX 6700.
9. Whether the model is in the packaged build.

### Frame-budget context

- No frame rate (30 or 60) or budget has been set for the project [L2].
- Epic's published Lumen and Nanite cost on PS5 at 1080p: about 8.5 of 16.7 ms at 60 fps, about 12.5 of 33.3 ms at 30 fps [L2].
- This PC matches the common UE5 minimum: Ryzen 5 5600 class with an RX 6700 [L2]. Its graphics card has 9.98 GB of memory as measured by the hardware-floor note [L2]; budgets should use that figure.
- The game already has a MetaHuman cost probe that measures GPU frame time per condition (median and 95th percentile) [L4]. The benchmark below can add conditions to it.

## (d) Comparison

| Option | On this PC (AMD) | Packaged game, speech made at runtime | Drives | Licence / cost | Quality (expected) | Cost | Main failure modes |
|---|---|---|---|---|---|---|---|
| Loudness jaw (in the game now) | Yes | Yes, working | 11 mouth controls, from loudness | Engine only; free | Reads as talking at a distance; a "placeholder" close up (audit) | Negligible (not measured) | Opens on loud hisses; no closure for p, b, m; one shape for every vowel; lags by its smoothing; no brows or eyes |
| Epic streaming solver (StreamingADA) | CPU: yes. GPU via DirectML: should work, unproven | Runtime module; cooking unverified; hidden beta | 81 face controls: jaw, lips, tongue, brows, blinks, mood; no head (expected) | UE EULA; free | Epic's current real-time model; likely far better than loudness | Unmeasured; estimated from under 1 to a few ms per step on a worker thread | Beta, may change; mood misread on flat voices; no head motion; about 80 ms lookahead at line start |
| Epic offline bake | Unverified on AMD (no requirement stated) | Editor only; plays back as baked animation | Full face, head, blinks, mood; 30 fps | UE EULA; free | Epic's best | About zero at runtime | Pre-made lines only; fixed 30 fps; its head motion may clash with the game's look-at |
| Epic Live Link "MetaHuman (Audio)" | Probably; GPU-heavy (Epic) | No: listens only to an input device; C++ API closed | Face without head; mood | UE EULA; free | Same family as the streaming solver | "Expensive", on the GPU | Cannot hear generated speech |
| NVIDIA Audio2Face-3D | No: NVIDIA GPU, CUDA and TensorRT; plugin for UE 5.5/5.6 only | Yes, on NVIDIA | Face, tongue, emotion | SDK MIT; weights NVIDIA Open Model License; Audio2Emotion restricted | Strong | 2.9 to 4.4 GiB VRAM | Wrong card vendor; not on 5.8 |
| Paid Fab plugins (Georgy Dev; "MetaHuman Audio to Face Runtime") | Yes (CPU) | Yes (claimed) | 81 controls and 12 moods ("realistic"), or 14 visemes ("standard") | Paid, under the Fab Standard License (allowed for purchases); money is Jafar's call | Similar model family (inferred) | CPU; figures not reached | Money; third-party dependency; wraps what the engine already has |
| Speech Graphics SG Com | Yes (CPU) | Yes | Lips, expression, head, blinks, eye darts | Commercial; price not public | Proven in shipped games | 50 ms latency (claimed) | Money and a contract |
| Rhubarb Lip Sync | Yes | Whole files only | 6 to 9 cartoon mouth shapes | MIT; free | Cartoon | Offline | Not streaming; stylised |
| Oculus LipSync | n/a | n/a | Visemes | Oculus SDK licence; end of life | n/a | n/a | Excluded (lip-sync note) |

## (e) Steps for this project (the helper's recommendations; the thresholds are estimates)

Follow the project's rules throughout:

- Every number comes from the real path: the game's own voice engine, the three real voices, a packaged build.
- The playable route comes first.
- The two-tries rule applies. If the solver will not load in a packaged build after two attempts, research it. After a third failure, set it aside and keep the loudness jaw plus the layers in step 3.

### 1. Benchmark plan

**B0. Precondition.**
- Pass: the plugin builds in a packaged Development build and a Shipping build; the model file appears in the cook output; and the log shows the model loaded, with the backend it chose.

**B1. Solver throughput.**
- Method: a command-line mode in the packaged build, like the MetaHuman cost probe. Feed real voice-engine output (three lines per character plus the thinking sounds), at their native sample rate, in the chunk sizes the real queue delivers. Run on the CPU backend first, then DirectML.
- Record:
  - time per step: mean, 95th and 99th percentile, maximum;
  - real-time factor;
  - load time;
  - time to the first frame;
  - RAM increase, and VRAM increase for DirectML.
- Pass (estimate):
  - mean step at most 2 ms (real-time factor at most 0.1);
  - 99th percentile at most 10 ms;
  - no step over 20 ms (slower than real time) more than once a minute;
  - load at most 2 s, done at level load;
  - RAM at most 150 MB more; VRAM at most 200 MB more.

**B2. Frame cost in the street.**
- Method: the conversation camera, with one character speaking a 30-second line on a loop, under four conditions: silent, loudness jaw, solver on CPU, solver on DirectML. Run with the voice engine generating at the same time, because contention is the real risk.
- Pass (estimate):
  - 95th-percentile frame time at most 0.5 ms above the loudness jaw (1.5% of a 30 fps frame, 3% of a 60 fps frame);
  - GPU time at most 0.3 ms higher on DirectML;
  - no new hitch over 5 ms.

**B3. Sync.**
- Method: log each applied face frame's audio sample index against the samples the audio device has consumed, minus the measured output delay. Also check by eye on one screen-and-sound recording of a line full of p, b and m.
- Target (estimate): the face between 0 and 40 ms ahead of its sound.
- Fail: the face more than 45 ms behind, or more than 125 ms ahead (ITU detectability [P13]).

**B4. Soak.**
- Method: 30 minutes of continuous lines, including interrupted lines and two characters taking turns.
- Pass (estimate): offset drift at most 20 ms; memory growth at most 10 MB; no NaN values and no crash.

**B5. Start of a line.**
- Pass (estimate): no more than 100 ms added before a line is heard, or none at all if the loudness jaw bridges the start. For scale: today's wait from Enter to the first sound is several seconds, and it has not yet been measured on the real path (the builder's list, item 2).

**B6. Another PC.**
- Run the same build on a second PC, tying in with the audit's unproven "self-contained release on another PC".

### 2. Feeding runtime voice chunks

1. Copy the PCM where it enters the game's audio queue and pass it to the solver on a worker thread, never the game thread.
2. For the first chunk of each line, set the reset flag and the Mood.
3. Stamp each output frame with the audio sample time it belongs to. Confirm the lookahead against the installed source.
4. Keep the frames in a ring buffer for each speaker.
5. Every game frame:
   1. Work out the line's playback time from the audio clock (samples consumed, minus output delay), not from game time.
   2. Interpolate between the two neighbouring 20 ms frames.
   3. Convert the controls with Epic's utility.
   4. Write them into the face's curve node. The existing mouth node can carry them once its list of 11 curves is widened.
6. At the start of a line, take one of two routes:
   - hold playback until the solver is about 100 ms ahead, which adds about 0.1 s to a start that already takes several seconds; or
   - use the loudness jaw for the first 100 ms and crossfade over about 60 ms.

   Measure both.
7. At the end of a line, feed silence equal to the lookahead so the last syllables resolve and the mouth closes, then blend the speech weight to zero over about 150 ms (estimate).

### 3. Layering, in evaluation order

1. **Body pose and head look-at.** The game already turns the head toward a target (60° limit, 0.2 s easing).
2. **Head motion while speaking (new).** Small nods and tilts, a few degrees (estimate; judge by eye), added after the look-at and driven by the voice's loudness and pitch envelope [P11]. The existing loudness analysis gets a second job here.
3. **Face base.** The idle or listening expression, plus a mood expression while listening, from the conversation state.
4. **Speech layer.**
   - Option A, to start with: the full-face solver output, with the Mood and a low intensity (0.3 to 0.5, estimate) passed from the dialogue system.
   - Option B, if its brows fight the intended mood: take only the mouth, jaw, tongue and cheek curves from the solver and drive the brows from dialogue tags. Epic's own offline tool offers a mouth-only mask for exactly this [E1].
5. **Blinks: one owner at a time.**
   - While the solver speaks with its own blinks, switch the game's blinks off.
   - While listening, the game blinks at 17 to 26 a minute, at random intervals [P12].
   - Blinking at large gaze shifts is common practice, but no source for it was opened.
6. **Eyes.**
   - Look at the player's face.
   - While speaking, glance away briefly and come back at the ends of phrases.
   - While listening, hold the look longer.
   - Add small saccades [P9].
   - From the third-person camera the eyes read only when the viewer looks almost straight at them (within about 4°), so the head carries most of the gaze (the project's gaze note, 28 September).
7. **RigLogic** runs last, in the MetaHuman face post-process.

A quick read of the game's person-animation code found no blink or eye control yet.

### 4. Keeping the loudness jaw as the fallback

- Keep it built in and selectable for each speaker.
- Switch to it automatically when:
  - the model fails to load, or the backend fails;
  - the solver's lead over playback drops below 40 ms;
  - the solver returns NaN or out-of-range values;
  - the graphics settings are low;
  - the speaker is not the conversation partner, is off screen, or is beyond about 10 m (estimate).
- Always crossfade over about 100 ms; never snap.
- Log each switch with its reason, so the AI tester and the daily summary can count them.

### 5. Pre-made lines

- Bake the pre-made lines offline: set the mood, and turn head movement on or off to match how the streamed lines look.
- Alternatively, run them through the streaming solver from uncompressed copies, for consistency. Cooked SoundWaves are compressed, so keep raw copies.
- Decide between the two with the side-by-side in step 6.

### 6. Judging

1. **What to film.** Two lines per character: one calm, one emotional. Include words with p, b and m, pauses, and a thinking sound.
2. **How to film it.** Through the game's own camera and exposure, at the real over-the-shoulder conversation distance.
3. **Three versions of each line:**
   - A: the loudness jaw;
   - B: the solver with the layers;
   - C: the offline bake, as a reference for the best Epic can do on these faces.

   Show them in blind order for each line.
4. **Own check before the page.** Lips close on p, b and m. The mouth closes in pauses and at the end of lines. The mouth stays still on breaths and noise. Vowels take different shapes. The tongue does not poke through the teeth. The mood fits the line. No double blinks. The head does not fight the look-at.
5. **Fresh reviewer.** Someone who has not seen the work checks the same list, then Jafar's page: short clips with sound, pictures opening at full size. This is his call because faces are people.
6. **AI tester.** Finally, the AI tester walks the packaged build with the solver on.

### 7. Effort (estimates)

- Benchmark: about 1 day.
- Wiring the solver: 1 to 2 days (lip-sync note).
- Head motion, eyes and blinks: 1 to 2 days.
- If it proves much bigger, tell Jafar rather than push on.

### 8. For Jafar (licences)

- Adopting StreamingADA needs a decision entry citing the Unreal EULA. The recommended answer is yes: it adds no new terms.
- Correct or remove the "Audio2Face-3D (MIT)" allowlist line (see section b, Licence).

## (f) Not verified or not reached

- The engine source (lip-sync note facts not re-checked): the interface, the lookahead, the model path, cooking, and whether DirectML is the default.
- Replies on the forum thread about custom audio streams [E17]. The builder should read it in a normal browser.
- The Fab listings, Georgy Dev's performance tables, the xADA paper's body, and the results of the Utrecht perceptual study comparing Epic's animator with Audio2Face [P14].
- Whether Fortnite ships StreamingADA: seen only through search-index fragments of a third-party dump [T3].
- Whether 5.8's "new real-time model" is the same file as StreamingADA's v2 model.
- Any measured cost, anywhere.
- The 5.8 announcement date: Epic's release-notes page is dated 17 Jun 2026, but a search summary said July.
- The EULA text itself.
- Graphics memory: the brief this helper was given said 12 GB, but the project's hardware-floor note measured 9.98 GB, and the plain RX 6700 is a 10 GB card (the 6700 XT has 12 GB). This does not change the recommendation, but budgets should use the measured figure.
- The secondary sources on Mass Effect: Andromeda, Half-Life 2 and Hogwarts Legacy were seen as summaries only.

## Sources (all read or searched 30 Sep 2026)

- E1. "Audio Driven Animation", MetaHuman Documentation. Epic Games. Updated 3 Nov 2025. https://dev.epicgames.com/documentation/metahuman/audio-driven-animation?lang=en-US. OPENED
- E2. "Using a MetaHuman Audio Source". Epic Games. Updated 25 Jun 2026. https://dev.epicgames.com/documentation/metahuman/using-a-metahuman-audio-source-in-unreal-engine?lang=en-US. OPENED
- E3. "Real-Time Animation" (MetaHuman). Epic Games. Updated 25 Jun 2026. https://dev.epicgames.com/documentation/metahuman/realtime-animation-for-metahumans-in-unreal-engine?lang=en-US. OPENED
- E4. "Realtime Animation Using Live Link". Epic Games. Updated 16 Jul 2025. https://dev.epicgames.com/documentation/metahuman/realtime-animation-using-live-link?lang=en-US. OPENED
- E5. "MetaHuman Animator". Epic Games. Updated 19 Jun 2026. https://dev.epicgames.com/documentation/metahuman/metahuman-animator-in-unreal-engine?lang=en-US. OPENED
- E6. "MetaHuman 5.8 Release Notes". Epic Games. Updated 17 Jun 2026. https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine?lang=en-US. OPENED
- E7. "Unreal Engine 5.8 Release Notes". Epic Games. Updated 23 Jun 2026. https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes?lang=en-US. OPENED
- E8. "MetaHuman Known Issues 5.8". Epic Games. Updated 28 Jul 2026. https://dev.epicgames.com/documentation/metahuman/metahuman-known-issues-5-8-in-unreal-engine?lang=en-US. OPENED
- E9. "Neural Network Engine Overview in Unreal Engine" (5.8). Epic Games. Undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/neural-network-engine-overview-in-unreal-engine. OPENED (general only)
- E10. "MetaHuman 5.8 is now available". Epic Games. June 2026 (a search summary said July). https://www.metahuman.com/news/metahuman-5-8-is-now-available. SNIPPET
- E11. "MetaHuman 5.7 Release Notes" and "MetaHuman 5.7 is now available". Epic Games. November 2025. https://dev.epicgames.com/documentation/metahuman/metahuman-5-7-release-notes ; https://www.metahuman.com/releases/metahuman-5-7-is-now-available. SNIPPET
- E12. "MetaHuman 5.6 is here". Epic Games. 3 Jun 2025. https://www.metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release. SNIPPET
- E13. "Audio Driven Animation for MetaHuman Animator [Experimental]", Unreal Engine public roadmap. Epic Games. Undated. https://portal.productboard.com/epicgames/1-unreal-engine-public-roadmap/c/1629-audio-driven-animation-for-metahuman-animator-experimental- ; forum "UE 5.5 - MetaHuman Animator Audio-driven animation", undated, https://forums.unrealengine.com/t/ue-5-5-metahuman-animator-audio-driven-animation/2118725. SNIPPET (titles only)
- E14. "xADA: Expressive Audio Driven Animation for MetaHumans", Unreal Fest Orlando 2025. Epic Games. Talk June 2025; recording public by October 2025. https://dev.epicgames.com/community/learning/talks-and-demos/MoK4/xada-expressive-audio-driven-animation-for-metahumans-unreal-fest-orlando-2025. OPENED (title only; body did not render) and SNIPPET
- E15. "xADA: Controllable and Expressive Audio-Driven Animation", SIGGRAPH 2025 Conference Papers, ACM. Epic Games researchers (author list not read). August 2025. https://dl.acm.org/doi/10.1145/3721238.3730711. SNIPPET
- E16. "Change MetaHuman (audio) Live Link Source runtime", Epic forum. 25 Sep 2025 (date per lip-sync note). https://forums.unrealengine.com/t/change-metahuman-audio-live-link-source-runtime/2659888. SNIPPET
- E17. "MetaHuman xADA for Custom Audio Streams [Guidance Needed]", Epic forum. Undated (UE 5.7 era). https://forums.unrealengine.com/t/metahuman-xada-for-custom-audio-streams-guidance-needed/2675424. SNIPPET (question only)
- E18. "You can now sell MetaHumans, or use them in Unity or Godot". CG Channel. June 2025. https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/ ; "Licensing MetaHuman", Epic, undated, https://www.metahuman.com/license ; "Unreal Engine EULA", Epic, https://www.unrealengine.com/eula/unreal. SNIPPET (EULA text not reached)
- T1. "MetaHuman Audio to Face Runtime", Fab listing. odysseyzjh. Undated. https://www.fab.com/listings/7ba4ef64-5026-4c83-b3b1-bd4e1e0e5ff5. SNIPPET
- T2. "Runtime MetaHuman Lip Sync" documentation (Overview, Plugin Configuration, Audio Processing). Georgy Dev. Undated. https://docs.georgy.dev/runtime-metahuman-lip-sync/. SNIPPET
- T3. GitHub code search for "SpeechAnimationSolver": hits in Arkfall-Development/UnrealEngine (a third-party engine copy) and FirexzFNBR/FNConfig-Files (a third-party dump of Fortnite files), at the path of the plugin file StreamingADA.uplugin. Searched 30 Sep 2026. SNIPPET (index fragments; repositories not opened; provenance unverified. Read the installed copy instead.)
- N1. Audio2Face-3D-SDK README. NVIDIA. Repository created 8 Aug 2025. https://github.com/NVIDIA/Audio2Face-3D-SDK. OPENED
- N2. Audio2Face-3D (component and licence table). NVIDIA. Undated (open-sourced 24 Sep 2025). https://github.com/NVIDIA/Audio2Face-3D. OPENED
- N3. "Audio2Face-3D, ACE Unreal Plugin" 2.5. NVIDIA. Undated. https://docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-audio2face.html. SNIPPET
- N4. "Audio2Face-3D: Audio-driven Realistic Facial Animation For Digital Avatars", arXiv 2508.16401. NVIDIA. 25 Aug 2025. https://arxiv.org/abs/2508.16401. SNIPPET
- N5. Reports of the open-sourcing: TechPowerUp and Open Source For You. 24 to 26 Sep 2025. https://www.techpowerup.com/341304/nvidia-wants-everyone-to-own-a-digital-avatar-with-open-source-audio2face-animation-model ; https://www.opensourceforu.com/2025/09/nvidia-moves-audio2face-technology-to-open-source/. SNIPPET
- M1. DirectML README. Microsoft. Undated. https://github.com/microsoft/DirectML. OPENED
- P1. Tomsinski, "Behind the Scenes of Cinematic Dialogues in The Witcher 3: Wild Hunt", GDC 2016. CD Projekt Red. March 2016. https://www.gdcvault.com/play/1022988/Behind-the-Scenes-of-Cinematic ; PC Gamer coverage, March 2016, https://www.pcgamer.com/most-of-the-witcher-3s-dialogue-scenes-was-animated-by-an-algorithm/. SNIPPET
- P2. Edwards, Landreth, Popławski, Malinowski, Watling, Fiume and Singh, "JALI-Driven Expressive Facial Animation and Multilingual Speech in Cyberpunk 2077", SIGGRAPH 2020 Talks. JALI and CD Projekt Red. August 2020. https://dl.acm.org/doi/10.1145/3388767.3407339. SNIPPET
- P3. Edwards, Landreth, Fiume and Singh, "JALI: an animator-centric viseme model for expressive lip synchronization", ACM TOG 35(4). University of Toronto. July 2016. https://dl.acm.org/doi/10.1145/2897824.2925984. SNIPPET
- P4. "Audio Driven Facial Animation for Hogwarts Legacy". Speech Graphics case study. Undated (about 2023). https://www.speech-graphics.com/client-projects/hogwarts-legacy. SNIPPET
- P5. SG Com product page. Speech Graphics. Undated. https://www.speech-graphics.com/sg-com-runtime-audio-to-face-animation-software ; "A Deep Dive Into Speech Graphics' Facial Animation Solutions", 80 Level, undated, https://80.lv/articles/a-deep-dive-into-speech-graphics-facial-animation-solutions. SNIPPET
- P6. "Speech Graphics Acquires OC3 Entertainment" (FaceFX). Built In Edinburgh. 2 Sep 2025. https://builtinedinburgh.uk/articles/speech-graphics-acquires-oc3-entertainment-20250902. SNIPPET
- P7. "Half-Life 2 Choreo System Research". erysdren. 6 Mar 2026. https://erysdren.me/blog/2026-03-06/ ; "FacePoser Basics", ModDB, undated, https://www.moddb.com/games/half-life-2/tutorials/faceposer-basics. SNIPPET (secondary)
- P8. "Animators: Awkward 'Andromeda' Animations Are Automation Amok". Vice. Undated in the summary (the game came out in March 2017). https://www.vice.com/en/article/animators-awkward-andromeda-animations-are-automation-amok/ ; TweakTown, undated, https://www.tweaktown.com/news/63071/bioware-longer-andromedas-facial-animation-tech/index.html. SNIPPET
- P9. Lee, Badler and Badler, "Eyes Alive", ACM TOG 21(3) (SIGGRAPH 2002). July 2002. https://dl.acm.org/doi/10.1145/566654.566629. SNIPPET
- P10. Ruhland et al., "A Review of Eye Gaze in Virtual Agents, Social Robotics and HCI", Computer Graphics Forum 34(6). 2015. https://onlinelibrary.wiley.com/doi/10.1111/cgf.12603. SNIPPET
- P11. Munhall et al., "Visual prosody and speech intelligibility: head movement improves auditory speech perception", Psychological Science 15:133–137. 2004. https://pubmed.ncbi.nlm.nih.gov/14738521/. SNIPPET
- P12. Bentivoglio et al., "Analysis of blink rate patterns in normal subjects", Movement Disorders 12(6):1028–1034. 1997. https://movementdisorders.onlinelibrary.wiley.com/doi/abs/10.1002/mds.870120629. SNIPPET
- P13. ITU-R BT.1359-1, "Relative timing of sound and vision for broadcasting". ITU. 1998. https://www.semanticscholar.org/paper/0ee98071da172de6e1d6d1fcd560bad9e0a87d5e ; https://en.wikipedia.org/wiki/Lip_sync_error. SNIPPET
- P14. Busacchi, Haque and Yumak, "Deploying Speech-Driven 3D Facial Animation in Unreal Engine for Production-Ready Digital Humans", arXiv 2606.10753. Utrecht University. 9 Jun 2026. https://arxiv.org/abs/2606.10753. SNIPPET (results not read)
- P15. "Lip Sync in Gaming: How NPCs Learned to Talk". lipsync.com. 20 Jan 2026. https://lipsync.com/blog/lip-sync-gaming. SNIPPET
- P16. "Bring NPCs to Life with AI-Powered Conversations". Epic. April 2026. https://www.fortnite.com/news/bring-npcs-to-life-with-ai-powered-conversations. SNIPPET. "Developing Personas Overview in Unreal Editor for Fortnite". Epic. Undated. https://dev.epicgames.com/documentation/fortnite/developing-personas-overview-in-unreal-editor-for-fortnite?lang=en-US. OPENED. Darth Vader AI in Fortnite, WDW News Today, May 2025. https://wdwnt.com/2025/05/epic-games-adds-darth-vader-coversational-ai-feature-to-fortnite/. SNIPPET
- L1. production/research/lip-sync/NOTE-2026-09-30.md. Project. 30 Sep 2026.
- L2. production/research/unreal-frame-budget/SUMMARY.md; production/research/hardware-floor/SUMMARY.md. Project.
- L3. production/audits/2026-09-30-adversarial-audit.md (the Animation row). Project.
- L4. The game's person-animation code (ue-probe/Source/LedgerProbe/Private/PersonAnim.cpp: mouth curve node, head look-at) and its MetaHuman cost probe. Project, read 30 Sep 2026.
- L5. ledger-v2/research/license-allowlist.md. Project.
- L6. production/research/gaze-and-knowing/SUMMARY-2026-09-28.md. Project.
