# Study A from inZOI's own files: small language model, read 6 November 2026

Source: C:\Games\inZOI.v0.10.1\inZOI.v0.10.1\game (v0.10.1), study-only reading as allowed by RULINGS (11 Oct, as amended). Nothing from the game is kept in LEDGER or git; prompts are described in words, one short quote at most. "Measured" = read from the named file; "inferred" = reasoning, unverified. Read order: the three earlier notes (FILES-2026-11-06.md, FILES-EXTRACT-2026-11-06.md, STUDY-A-2026-11-01.md) first.

## How it was read

- The packed containers (36 mounted, 258,469 files) were opened with the Silent Hill 2 reader and the key file on F:, by path only. Plain files pulled out (6,980 lua, ini and uplugin files, about 21 MB; a few json tables; two English string tables) and read; extraction total under 110 MB, all deleted afterwards.
- Reader result: file listing, byte reads and the plain files worked. Property values of data assets failed (see "Unreached"): the game has no mappings file here.
- Game logic is not in Lua here: the Lua folder holds only type definitions (luals-defs, 6,451,857 bytes in 6,531 files). The prompt text and its settings were found as printable text inside the program file Binaries\Win64\inZOI-Win64-Shipping.exe (285,372,856 bytes), read as text only, nothing run. Offsets below are byte offsets into that file.

## Answers

### A1. Which model loads, from where

- Measured, from disk (BlueClient\Plugins\NVIGIPlugin\Source\thirdparty\nvigi\models\nvigi.plugin.gpt.ggml\): three folders, each with model.gguf, nvigi.model.config.json and version.txt.
  - ...936A: model.gguf 480,622,400 B, llama architecture, 24 blocks, embedding 1152, file type 15 (Q4_K_M), header context 8192; config says context 4096 and "vram" 1024; its chat template has a tools block (about 1,367 characters) in the style of Mistral-NeMo.
  - ...936B (English): 811,835,872 B, architecture qwen35, label 752M, 24 blocks, embedding 1024, 8 attention heads with 2 key-value heads, file type 7 (Q8_0), vocabulary 248,320 tokens; config context 8192, "vram" 2048.
  - ...936C (Korean): 811,835,904 B, same architecture and numbers as 936B.
  - The English folder's model header tags its language as Korean (FILES-READ-2026-11-06-REVIEW.md). The vocabulary count and the string-table claims were not re-checked by the review.
  - Chat template of 936B and 936C (162 characters, read from the file header): plain role-and-content turns, with no tools block. So the tool-call format is carried in the prompt body, not the template (inferred).
- Which of the three the game loads: unread. The program file holds the plugin's own names for the three-way choice only as the model key property (ModelKey, offset 0xecee550); the value and the language-to-folder mapping are not in any file read. The two Qwen-style builds are the ones whose notes (version.txt) mention SmartZoi; the 936A file is also on disk (480 MB). Inferred and unverified: 936A is an older leftover.

### A2. Size and memory settings

- Measured, BlueClient\Plugins\NVIGIPlugin\Config\DefaultNVIGIPlugin.ini (340 bytes), section NVIGISettings: ArchitectureRequirement 368 (meaning not stated); MemoryRequirementCuda 7000; MemoryRequirementVulkan 10000 (units not stated; inferred MB); ContextSize 4096; MaxNumTokensToPredict 1024; MaxBatchSize 2048; PhysicalBatchSize 512; NumThreads 1; VramBudgetMB 2048; Seed -1; NumParallel 1; BatchSize 2048; Temperature 0.8.
- Measured, program file text (offset 0xecee550): the plugin's per-model setting names are ModelKey, ContextSize, MaxNumTokensToPredict, PhysicalBatchSize, CacheTypeK, CacheTypeV, FlashAttention, inside a class named NvigiModelConfig. Their per-model values: unread.
- Measured, string table BlueClient\Content\Localization\Blue_Data\en\Blue_Data.locres (18,017,454 B): the in-game help says 7 GB or more of video memory is recommended for Smart Zoi.
- Measured, same file and Blue_UI.locres (1,425,087 B): two bullet lines name NVIDIA RTX 3000 series with 8 GB or higher and AMD RX 6000 series with 12 GB or higher. Which feature they belong to is not shown in the lines read (unverified that it is Smart Zoi).
- Runtime beside it, from the earlier note: three back-end libraries (CUDA 63,060,592 B, Vulkan 50,534,512 B, processor 7,210,096 B).

### A3. What feeds it (prompt contract, output format, sizes)

All measured from program text (offsets 0xf193280 to 0xf1ee6e4 region) unless stated; wording below is the note's own.

- Situation triggers (13 types, measured in Content\Data\Lua\luals-defs\enums\EB2SmartZoiSituationType.lua, 556 B): relationship talk record, receiving a phone message, emotion level change, drama event popup, choice card answer, gift box, karma interaction, coop interaction, mission interaction, preference interaction, checking the phone, performing a need interaction, going to sleep. A situation carries a type, an id, a name, a free-text description, and a flag whether to notify those around (measured, FB2AutonomyComponent.lua, 16,216 B).
- Context sent per character (field names in the program text): identity and traits, likes, dislikes, a "hidden persona" text (zoi pen, limited per character and for the world by MaxSmartZoiPenLength and MaxWorldSmartZoiPenLength; values unread), current emotion and its value and level, job and rank, relationships and relationship records, family relationships, schedule of the day, site and its tags, weather and time, nearby characters and objects (with a broken flag), the last interaction, banned and filtered activities, lists of available and important interaction ids, recent completed actions, current intent, a reason an intent update is required, and a just-arrived notice.
- The user prompt is a templated document with these headed sections: hidden persona, identity, inner state, current scene, today's schedule, nearby objects, nearby people, recent completed actions, current intent, intent update required, just arrived, task.
- Message shape: system and user turns; a tool list is written into the prompt as "Available Tools" with each tool's input schema; the reply must be a JSON object with a list of tool calls, each a name and an input object. The prompt says "Call exactly one tool appropriate for the current situation" (offset 0xf195d11). An alternative layout allows a tool-result turn to be fed back (tool_result, tool round).
- Prompt versions in the built-in config (measured, text around 0xf196a37 to 0xf1982dd): a "teacher" and a "student" prompt mode, student selected (prompt_mode: student); named versions per step: action selection v11 (student v11), compact v9, set_intent v4 (student v1), get_actions v4 (student v2), get_proper_site v2 (student v1), choose_option v4 (student v1), a reduced one for the youngest growth stage, a status prompt for business staff and customers; "compressed_prompt: false"; "think_tool: false" (no thinking tool). Version notes on disk say "v26 student prompt contract" and "no-think".
- Sizes: model context 8192 tokens in the two Qwen-style configs, 4096 in the settings ini, 1024 tokens to predict (A2). Prompt and response length in characters and latency in milliseconds are logged per request (field names prompt_length, response_length, latency_ms, elapsed_ms at 0xf193dd8 to 0xf193df8). No size in tokens of the real prompt was found.

### A4. What it decides, and what stays scripted

- Tools the model can call (names measured in program text): set_intent (a rough direction for the next few hours; window setting intent_window_minutes 240), get_actions (reads available actions at the present site), get_proper_site (picks a place), choose_option (picks one listed option), think (switched off), other_tools, entity_show_speech_bubble, and a query for needs. The youngest growth stage is told it may only call choose_option.
- Outputs of note: inner_thought (the shown thought), reason_text (inner_thought_as_reason: true, so the thought doubles as the reason), optionally an intent (also_return_intent: false); speech bubble from an inner thought when social: false.
- Scripted or game-side (measured from names and Lua types): what triggers a request (the 13 situations); the queue of interactions it fills (EB1InteractionPlayReason has SmartZoi, SmartZoiCoop, SmartZoiTalk); coop role assignments (role id per character) for a group action; cooldown check on autonomy interactions; the interaction itself and its animation. Fallback events named in the program text: auto_choice, selection_fallback, intent_required_idle, retrieval_unselected_idle, fallback_idle, action_not_executed (inferred: idle or automatic choice when the model gives nothing usable).
- Prefetch (measured settings, program text 0xf1976ab to 0xf197b80): prefetch_enabled true; horizon 20 minutes; need_recovery 60; need_gain 10; max age 60 minutes; poll interval 5 seconds; queue size 4; poll stat "Toilet"; prefetch_exclusive_llm true; held_object_action true; failed_interaction_ms 6000. Inferred: it guesses a need ahead of time and asks while the character is busy; the "exclusive" flag keeps only one request on the model.
- With a user-supplied model, only inner-thought text is produced and action choice is switched off (measured, Blue_UI.locres sentence, and bSupportsActionSelection in FB1Packet_S_SmartZoiModelSwitchResult.lua, 476 B).

### A5. How invented facts are kept out

Measured from the prompt rules (program text 0xf1e8980): the model is told to use only labels that actually appeared in tool results; to call exactly one tool each time; to keep speech-style persona out of tool names, JSON keys, enum values, ids and selection labels (persona style goes only in intent and inner thought); to put persona after safety, physical needs and schedule. Actions are picked from a list the game builds (get_actions), by label, so a free-text action cannot enter (inferred). Tool descriptions are version-checked against the prompt config at load (error text "Tool spec version mismatch", 0xf1e7b48). An empty or failed reply is counted as a named failure (llm_empty_response, llm_error_response) and the packet FB1Packet_S_SmartZoiInferenceFailed carries a reason string (measured, 255 B). A student model distilled from a teacher is implied by the version notes ("student") (inferred). No checker of the generated sentences was found in the files read.

### A6. Card sharing, back end, fallback

- Measured: the plugin ties to NVIDIA's in-game inference SDK (NVIGIPlugin.uplugin, 600 B; error texts "nvigiInit failed", "nvigiGetInterface(GPT) failed", "...(HWI CUDA) failed" at 0xdaa80c8). The three back-end libraries exist (CUDA, Vulkan, processor). The settings file has separate memory minimums for CUDA (7000) and Vulkan (10000). DAISmartZoi.uplugin (platforms Win64 and Mac) describes itself as a wrapper of a "zoi_system_sdk" static library; DAILm.uplugin as wrapping NVIGI, Win64 only.
- Measured: the same plugin set has an API back end (names "APIBackend", "backend", "no_backend", and an MCP client with tools/list and tools/call at 0xf1e4a90) — inferred: a remote or developer route used for testing or as the teacher; whether the shipped game uses it is unread.
- Measured in-game messages (Blue_UI.locres): hardware-accelerated GPU scheduling must be on for the feature; running other programs that use the GPU at the same time may close the game; a minimum graphics driver is recommended (NVIDIA 545.23.06). Option rows SmartZoiCaptionHWS and SmartZoiCaptionHWSNUpdate exist for those captions (GameOption.json, 350,630 B). Their tie to Smart Zoi is inferred from the row names.
- The model states are Disabled, Loading, Ready, Transitioning, Failed (EB1SmartZoiModelState.lua, 251 B); a model failure packet carries a reason and a request generation number (FB1Packet_S_SmartZoiModelFailed.lua, 280 B). A restore attempt flag exists in the switch result. Which back end the game picks on a card without CUDA: unread.
- Fallback when the model is off or fails: not readable in plain files beyond the idle and auto-choice names in A4.

### A7. Settings for speed limits

- Measured, Content\Data\JsonResult\GameOption.json (350,630 B), rows for Smart Zoi: SmartZoi on/off default 0 (off); SmartZoiRangeInCity three choices 0, 1, 2, default 2; SmartZoiRangeInViewport three choices 0, 2, 4, default 2; SmartZoiWaitingCount five choices 4, 6, 8, 10, 12, default 8; SmartZoiModel (upload of a user model, default "None"); four caption rows. (Corrected by its review: no SmartZoiAutonomy row exists.) The labels of the choices are text ids, not read.
- Measured, applied-area enum: only the controlled Zoi, the controlled family, or all Zois in the city (EB1SmartZoiAppliedArea.lua, 259 B). Settings packet fields: path, range in city, range in viewport, waiting count, on/off, a request generation number.
- Measured, DLD manager type (FB2DLDSLMManager.lua, 7,061 B): maximum characters reasoning at once, and in the viewport; maximum waiting queue; a flag "can request" checked per character by group type, viewport and reasoning kind; two lists of characters (those waiting on a reply, those allowed to idle).
- Measured, names only, UB1DNDAutonomyConfigDataAsset.lua (1,295 B): ResponseTimeoutSec, RetryCount, RequestTimelineRetryCount, CollectAOILevel, MaxSmartZoiPenLength, MaxWorldSmartZoiPenLength. Values: unread (the data asset could not be parsed).
- Measured, preset tables GameOptionSimulationPreset.json (8,922 B), GameOptionGPUPreset.json (229,290 B), GameOptionCPUPreset.json (50,024 B): searched for Smart Zoi; no preset row sets any Smart Zoi option.

## Unreached, with why

- Values inside data assets (DA_DNDAutonomyConfig.uasset 326 B, DA_DLD.uasset 4,495 B): parse failed, "Read size is bigger than remaining archive length" and, with the newer engine setting, "mapping file is missing"; no mappings file on this PC and none fetched.
- Which model file the game loads; per-model settings values; the real prompt length in tokens; the tool schemas' full contents; the hidden-persona text format: not found in plain files.
- Frame cost, speed in tokens a second, card use measured in play: needs a running game; not done.
- Source code of the plugins (DAISmartZoi, DAILm, DAICore): compiled into the program file, not present as source.
- Whether the 936A file is used, whether the API back end is shipped active, which back end the game chooses on AMD: not readable.
