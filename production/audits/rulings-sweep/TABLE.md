# Every ruling, and what became of it

One row per ruling, in the order of its file. Status: BUILT, PARTLY, LISTED (on a list as work still to do), SUPERSEDED, NOWHERE, CONDUCT (binds behaviour only; nothing to build). "Checked" is what was seen in the code, content or lists, file:line; "Inferred" is what was concluded without direct sight. Rows marked **R** were also checked by this reviewer in the code (the reviewer's lines are under "Reviewer"). The full record, with every citation, is `rulings.json` beside this file.

## DECISIONS.md

### DEC-001 · BUILT · DECISIONS.md:7

- **Ruling:** Build one integrated encounter first; visual work pauses until it exists. (Jafar, 2026-09-24)
- **Checked:** ROADMAP.md:26-27 - PASSED 24 September, all seven conditions, the build's regression ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:282 and :8964 - -Encounter=play/reload/unseen modes ; .github/workflows/ledger-probe-unreal.yml:3014-3040 - 'Judge the encounter, the build's regression' runs tools/encounter-verdict-check.py on the three runs and both live runs for the commit ; tools/ci-checks.sh:174 - encounter-verdict-check selftest in the Core job
- **Inferred:** The visual pause was lifted once it passed; later route-first pauses (DECISIONS.md:154) are separate rulings.

### DEC-002 · SUPERSEDED · DECISIONS.md:8

- **Ruling:** Shrink the way of working: five-line NOW, one closing summary, stop hook, no notes-only commits, checklist archived. (Jafar, 2026-09-24)
- **Superseded by:** DECISIONS.md:49
- **Checked:** DECISIONS.md:49 - stop hook removed, a dated summary a day replaces the per-sitting summary, NOW's word cap dropped ; .claude/settings.json - no hooks section (stop hook gone); tools/sitting-clock.py absent ; production/archive/ROADMAP-checklist-to-2026-09-24.md - checklist archived as a reference (part still in force, built) ; FINDINGS.md - 20 entries ('- ' lines), within its cap
- **Inferred:** 'No notes-only commits', 'local iteration' and 'short CLAUDE.md/ROADMAP' are conduct with no mechanism to check.

### DEC-003 · BUILT · DECISIONS.md:9

- **Ruling:** Keep Core suites, the C++ comparison, the independent check and the Unreal build on push. (Jafar, 2026-09-24)
- **Checked:** tools/ci-checks.sh:179-185 - core-tests, soak, save-chaos, perception-golden (tools/port-golden-check.sh), stranger-test in the table ; .github/workflows/ledger-core-tests.yml:4-24,66 - runs tools/ci-checks.sh on push ; .github/workflows/ledger-probe-unreal.yml:43-75 - Unreal build on push; :285-289 regenerates the golden table from the C# Core; :411 builds and runs the golden test
- **Inferred:** The independent check on simulation changes is conduct; DECISIONS lines cite passes of it, not verified here.

### DEC-004 · PARTLY · DECISIONS.md:10

- **Ruling:** Provisional business model: sold once, server-counted live-talk allowance, then brush-off; own-key mode; capable cards later. (Jafar, 2026-09-24)
- **Missing:** An own-key mode for players does not exist anywhere and is on no list; the relay is built but not wired into the game (deferred by DECISIONS.md:200).
- **Impact to a player:** 1 (Matters only when copies are sold; nobody but Jafar and friends on his PC plays now.) · **belongs:** ue-probe CrimeProbe.cpp (key/relay choice) and ledger/TalkHelper; or ROADMAP.md 'Then' milestone · **lane:** builder
- **Checked:** ledger/Relay/Relay.cs:25,241-258 - allowance per copy per day/month, 'allowance_spent' and 'relay_stopped' refusals ; ledger/TalkHelper/Program.cs:1140, :2174-2179 - a spent allowance gives a brush-off and tells the player when talk comes back ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3218 - the game starts the helper with '--early --pending' only, never --relay ; DECISIONS.md:200 - friends' test on his PC, no relay and no sent copies for now (defers the relay wiring) ; …
- **Inferred:** 'Capable cards later' is explicitly future; not judged.

### DEC-005 · BUILT · DECISIONS.md:11

- **Ruling:** Unprompted town speech is written ahead; live model talk only when the player talks to someone. (Jafar, 2026-09-24)
- **Checked:** ue-probe/Source/LedgerProbe/Public/StreetVoice.h:260-403 - fixed written banks of 14 lines each; OwnLines.h written per-character lines ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5802-5824 - remarks come from StreetVoice::Recognition/FaintRemark banks, then voiced ; CrimeProbe.cpp:213-214, :1695 - witness lines from content/dialogue/crime-witness-v1.json ; CrimeProbe.cpp:4625 - the talk helper is called only for a conversation line

### DEC-006 · PARTLY **R** · DECISIONS.md:12

- **Ruling:** Keep the paid model as the action router; a local model only later, as offline fallback. (Jafar, 2026-09-24)
- **Missing:** The router the ruling keeps exists only in the C# Core and the legacy Unity build; the game players run never routes a typed line through it.
- **Impact to a player:** 2 (The current game takes decisions through conversation; a player typing an action gets talk, not an action.) · **belongs:** ledger/TalkHelper/Program.cs (if typed actions are wanted) or a DECISIONS line retiring the router · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/IntentRouter.cs:363 - the router (paid model, with RouterExamples) ; grep 'IntentRouter' outside Core: only ledger/Assets/Scripts/Game/IntentBridge.cs (legacy Unity), SimHarness, RouterFloor, Adversary ; grep 'IntentRouter/verb/intent' in ledger/TalkHelper/Program.cs: no hit; grep -i 'router' in ue-probe/Source: no hit ; production/research/local-models/SUMMARY.md:1-20 - the router picks actions from typed lines
- **Inferred:** The Unreal game has no typed-action routing at all; decisions are taken through talk (Arrangement's two-step yes, suggested lines), so the router may simply be obsolete, but no ruling retires it.
- **Reviewer:** grep 'IntentRouter/.Route(' in ledger/TalkHelper and ledger/Relay source: no hit; the game's talk never calls the router

### DEC-007 · PARTLY · DECISIONS.md:13

- **Ruling:** Voices: Aldous keeps p226; Danny p243, June p277, Zlata p280; none cast without his yes; VCTK consent risk. (Jafar, 2026-09-24)
- **Missing:** The three new picks were never made into game clips; picked-clips still holds older uncast voices for Danny, June and Zlata. Not on any list.
- **Impact to a player:** 2 (Not heard yet; the first time June or Danny speaks (June's own street lines are already ported) it is in a voice he did not pick.) · **belongs:** game-design/picked-clips (voice clips) and NOW.md builder list · **lane:** builder
- **Checked:** game-design/picked-clips/ - aldous.p226.wav (matches); danny.p254.wav, june.p225.wav, zlata.p233.wav (NOT his picks p243, p277, p280) ; grep 'p243/p277/p280' outside research/archive: only casting sheets (danny-cammack/SHEET.md:17, june/SHEET.md:19) and DECISIONS ; tools/voice-live/voice-server.py:43-53 - clip_for() takes the first <who>.*.wav/.mp3 from picked-clips, so June would speak in p225 ; production/archive/NOW-to-2026-09-24.md:46 - 'CAST THE THREE NEW VOICES he picked' was a list item; not on any current list ; …
- **Inferred:** None of Danny, June or Zlata is heard aloud in the game yet, since only the three principals talk or remark.

### DEC-008 · BUILT · DECISIONS.md:14

- **Ruling:** MetaHuman files stay out of the public repository, backed up to Dropbox, never a release. (Jafar, 2026-09-24)
- **Checked:** .gitignore:154-162 - ue-probe/Content/Ledger/MetaHumans/, Cloth/, Export/, MH_Test.uasset ignored ; git ls-files: no MetaHuman .uasset/.fbx/.dna tracked (only Mixamo fbx and props) ; tools/backup-to-dropbox.py:9-13 - the MetaHuman sources copied to Dropbox from production/specs/in-game.json's backup lists (in-game.json:8-20 MH_LenaS4 etc.) ; grep 'gh release/action-gh-release/releases' in .github/workflows: no hit

### DEC-009 · BUILT · DECISIONS.md:15

- **Ruling:** MH_Test gets only free clothing or waits; it is not a prerequisite for the slice. (Jafar, 2026-09-24)
- **Checked:** tools/ue/dress_metahuman.py:1-20 - MH_Test dressed by script in the plugin's free WI_DefaultGarment ; grep 'MH_Test' in ue-probe/Source and production/specs: no hit - the test figure is not in the game; the slice proceeds without it

### DEC-010 · BUILT · DECISIONS.md:16

- **Ruling:** The encounter regression talks to a stand-in model answering from sent memories; live model checked by hand. (Claude (his to overrule), 2026-09-24)
- **Checked:** ledger/TalkHelper/Program.cs:76-80 - FAKE MODE --fake: a stand-in answers from the memories in its prompt ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:7060,7075 - the encounter starts the helper with --fake unless somebody plays ; CrimeProbe.cpp:3208-3218 - live play uses the stand-in for unattended runs, LEDGER's key only in a played run
- **Inferred:** 'The live model is checked by hand' is conduct.

### DEC-011 · BUILT · DECISIONS.md:17

- **Ruling:** Suspicion from account, sighting and familiarity on four levels; at Suspicious the model asks straight out. (Claude (his to overrule), 2026-09-24)
- **Checked:** ledger/Assets/Scripts/Core/Suspecting.cs:74,133 - Suspecting.Derive ; ledger/TalkHelper/Program.cs:564-592 - reads the game's evidence (account, near, familiarity) and calls Suspecting.Derive ; ledger/Assets/Scripts/Core/ConversationEngine.cs:638-641 - 'ask them straight out, your own way' (bounded later by DECISIONS.md:76) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4625 - the game sends evidence=EvidenceFor(...) with each line
- **Inferred:** FINDINGS.md:10 notes the C++ port's own suspicion number is read by nothing in the game; the ruling itself puts the decision in the helper, so that is not counted against it.

### DEC-012 · SUPERSEDED · DECISIONS.md:18

- **Ruling:** Cast MetaHumans start from shipped Jorge, Grace and Orlando, replacing three stand-ins. (Claude (his to overrule), 2026-09-24)
- **Superseded by:** DECISIONS.md:20
- **Checked:** DECISIONS.md:18 - the entry itself says replaced the same night by the cast brief ; DECISIONS.md:20 (brief), :39 (faces approved), then S4/P2/C5 in CrimeProbe.cpp:917 ; CrimeProbe.cpp:918-919 - take list ends with T2 and the bare stand-in, so the stand-ins remain the fallback

### DEC-013 · CONDUCT · DECISIONS.md:19

- **Ruling:** Download free allowlisted Unreal content without asking; note it in the summary. (Jafar, 2026-09-24)
- **Checked:** CLAUDE.md 'Talking to Jafar' - the standing permission, restated
- **Inferred:** Names no artefact; a standing permission for how sessions act.

### DEC-014 · SUPERSEDED · DECISIONS.md:20

- **Ruling:** Cast made to a written brief (Lena ~60 small, Rocco heavy, Sam Scottish) as blended faces, take T2. (Claude (his to overrule), 2026-09-24)
- **Superseded by:** DECISIONS.md:25; DECISIONS.md:34; DECISIONS.md:39
- **Checked:** DECISIONS.md:20 - says itself superseded the same night by the names and faces rulings ; DECISIONS.md:25 (names), :34 (faces cast in MetaHuman first), :39 (faces approved) ; CrimeProbe.cpp:917-919 - T2 kept only as a fallback take

### DEC-015 · SUPERSEDED · DECISIONS.md:21

- **Ruling:** Playable encounter roles: Lena witness at Mickey's, Sam lad in the yard, Rocco his mate; no constable. (Claude (his to overrule), 2026-09-24)
- **Superseded by:** DECISIONS.md:155; DECISIONS.md:178
- **Checked:** DECISIONS.md:155 - free play's crime is Rita's window; the three talk by their routines; only the scripted regression keeps Mickey's ; DECISIONS.md:178 - witnesses are whoever's day puts them on Quay Street ; DECISIONS.md:95/:98 - constable and DS Ellis now exist (PoliceFile)

### DEC-016 · PARTLY **R** · DECISIONS.md:22

- **Ruling:** Router gets six nearest worked examples; its block also catches orders said in plain words. (Claude (his to overrule), 2026-09-24)
- **Missing:** Built in the C# Core only; the Unreal game and its talk helper never use the router or its order-catching block.
- **On a list:** ROADMAP.md:40-42
- **Impact to a player:** 2 (No typed actions in the current game; the injection-catching block does not stand in front of live talk, only a prompt line does.) · **belongs:** ledger/TalkHelper/Program.cs (block on the player's line) or a ruling retiring the router · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/RouterExamples.cs:33 and IntentRouter.cs:363 - examples built into the router prompt ; grep 'IntentRouter/PosesAsInstruction' in ledger/TalkHelper and Core outside IntentRouter: no use (Director.cs:258 uses ExtractJson only) ; ledger/Assets/Scripts/Game/IntentBridge.cs - the only game-layer user is the legacy Unity build ; ledger/Assets/Scripts/Core/ConversationEngine.cs:506 - the live talk prompt tells the model to treat instructions as strange talk (a prompt line, not the router's block) ; …
- **Inferred:** The Unreal game has no action router; the block's protection exists in live talk only as a prompt line.
- **Reviewer:** grep 'IntentRouter/.Route(' in ledger/TalkHelper and ledger/Relay source: no hit; the game's talk never calls the router

### DEC-017 · BUILT · DECISIONS.md:23

- **Ruling:** AI tester: one screenshot and action per step, only after two idle minutes, keys only to its own window. (Claude (his to overrule), 2026-09-24)
- **Superseded by:** DECISIONS.md:99 (the 'through the conversation model (Sonnet 5)' part: the tester is now played by the Claude Code session, play.py:16-26)
- **Checked:** tools/ai-tester/play.py:418-420 - refuses start when the PC was used in the last 120 s unless --force ; tools/ai-tester/play.py:221-228 - game_in_front(): no key sent unless the game's process owns the front window ; tools/ai-tester/play.py:1-26 - one action per command, then a picture

### DEC-018 · BUILT · DECISIONS.md:24

- **Ruling:** Project facts: third-person, Windows PC, Britain 1990, no alcohol/gambling, tobacco allowed, no children. (Jafar, 2026-09-24)
- **Checked:** ue-probe/Source/LedgerProbe/Private/LedgerCharacter.cpp:36-48 - spring-arm third-person camera, arm 350 ; canon.md:102-110 - content rule (alcohol and gambling out entirely) ; ledger/Assets/Scripts/Core/ResponseValidator.cs:69-73 - live replies speaking of drink, betting or children are not said (ContentRule.SpeechBreaks) ; tools/ci-checks.sh:155-156 - content-gate in CI ; …

### DEC-019 · BUILT · DECISIONS.md:25

- **Ruling:** Renames: Sheila Dunn, Ron Kirby, Darren Milner, DS Carol Ellis, Geoffrey Agar and the rest; Tom Nowak. (Jafar, 2026-09-24)
- **Checked:** canon.md:92-100 - NAMES block ; production/cast/cards/lena.md:1 'Sheila Dunn', rocco.md:1 'Ron Kirby', sam.md:1 'Darren Milner' ; production/specs/hook-cast.json - display names Ron Kirby, Sheila Dunn, Darren Milner, Alison Sedman, Father Walsh ; ue-probe/Source/LedgerProbe/Public/PlayerIdentity.h:30 - Surname 'Nowak'; Waiting.h:105 'DS Ellis' ; …

### DEC-020 · BUILT · DECISIONS.md:26

- **Ruling:** Old names survive only as internal ids; only what the player sees and hears is renamed. (Claude (his to overrule), 2026-09-24)
- **Superseded by:** DECISIONS.md:90 (the 'Father Emil and the Fixer stay' part: now Father Brendan Walsh and Keith Garbutt)
- **Checked:** hook-cast.json ids lena, rocco, sam, noor, emil etc. with renamed display names ; tools/names-gate.py:17-23 - lower-case ids allowed, capitalised retired names refused ; CrimeProbe.cpp:915-917 - asset names MH_Lena/Rocco/Sam kept, marked names-gate: allow

### DEC-021 · SUPERSEDED · DECISIONS.md:27

- **Ruling:** Faces built by script from the nearest preset against an approved portrait; paid Blender add-on fallback. (Jafar, 2026-09-24)
- **Superseded by:** DECISIONS.md:34
- **Checked:** DECISIONS.md:34 - faces cast in MetaHuman first; a generated portrait is a mood reference only ; DECISIONS.md:81 - faces then finished from measurements (S1-S4)

### DEC-022 · PARTLY · DECISIONS.md:28

- **Ruling:** No hiring; keep approved voices that fit age; older characters get clean references; nothing noisy. (Jafar, 2026-09-24)
- **Missing:** Clean older voices for Ada, Carol Ellis, Geoffrey Agar, June and Maureen Jensen: not made and on no list (only Walsh's is listed).
- **On a list:** NOW.md:52 (Walsh only)
- **Impact to a player:** 2 (None of them speaks aloud in the game yet; the moment they do, a 78-year-old widow speaks with a 24-year-old Oxford voice.) · **belongs:** NOW.md builder list (voices), game-design/picked-clips · **lane:** builder
- **Checked:** production/casting/{ada,carol-ellis,geoffrey-agar,june,maureen-jensen,father-emil}/SHEET.md - each says 'Needs an older voice' (Ada 24 vs 78 'the most urgent') ; NOW.md:52 - only Father Walsh's older Irish voice is on a list ; game-design/picked-clips/ - ada.p276, ellis.p231, aldous.p226, june.p225, kest.p244, emil.p245: the young VCTK voices still in place ; game-design/picked-clips/lena.parler-d.mp3 - Sheila's clean designed voice (built for her); Ron keeps p227, approved by Jafar (DECISIONS.md:128) ; …
- **Inferred:** No one has been hired (nothing found suggesting it).

### DEC-023 · PARTLY · DECISIONS.md:29

- **Ruling:** Six mechanisms: one sample first; approvals lapse and are flagged by the build; tester on release build; one page; facts; audits. (Jafar, 2026-09-24)
- **Missing:** Nothing placed in the game has a current approval in the place the build checks (8 of 8 flagged); in-game.json is stale against his latest picks; the tester walks a Development package, the release-build walk is still to come.
- **On a list:** NOW.md:21 (release walk only)
- **Impact to a player:** 1 (Process and records; the build flags but never fails, so the lapse mechanism currently protects nothing.) · **belongs:** production/specs/in-game.json and *.approval.json beside each placed thing (tools/approvals.py --record) · **lane:** builder
- **Checked:** tools/approvals.py and tools/ci-checks.sh:157-158 - the lapse-and-flag mechanism runs in CI ; python3 tools/approvals.py (run read-only): 'placedInGame=8 placedWithoutCurrentApproval=8' - every thing production/specs/in-game.json places in the game is flagged NO APPROVAL ; production/specs/in-game.json:5,25,45 - names the three SHEET.md files; ls production/casting/{sheila-dunn,ron-kirby,darren-milner}: no SHEET.md.approval.json ; in-game.json:6,46 - still says Darren take C5 and Sheila voice lena.parler-d, behind DECISIONS.md:136 (S6, p267) ; …
- **Inferred:** The approval mechanism exists but its data was not kept: approvals were written beside candidate pictures (e.g. candidates-2026-09-28/S4/sheila-dunn/S4-front.jpg.approval.json) while in-game.json points at the sheets.

### DEC-024 · BUILT · DECISIONS.md:30

- **Ruling:** Adopt Parler-TTS mini v1 for designed voices; SLR83 lowest-pitched speakers as blind candidates only. (Claude (his to overrule), 2026-09-24)
- **Checked:** THIRD-PARTY.md:84,98-99 - SLR83 four speakers with CC BY-SA risk stated; Parler-TTS mini v1, Apache-2.0 ; game-design/picked-clips/lena.parler-d.mp3 - a Parler-designed voice in use ; production/casting/voice-key.json - candidates and removals recorded ; game-design/picked-clips/: no SLR83 (nof_/nom_) clip in the game

### DEC-025 · PARTLY · DECISIONS.md:31

- **Ruling:** Approval page stores his verdicts; the next sitting turns them into approval files beside the sheets. (Claude (his to overrule), 2026-09-24)
- **Missing:** His approvals of the three principals (faces, voices) never became approval files where the build looks; Darren's approved face has none at all.
- **Impact to a player:** 1 (Records only; it leaves the build unable to tell an approved principal from an unapproved one.) · **belongs:** production/casting/<principal>/SHEET.md.approval.json via tools/approvals.py --record · **lane:** builder
- **Checked:** tools/approval_page.py:1-17 - verdicts stored in the page's db (verdicts/<slug>), approval files via tools/approvals.py --record ; production/approvals/2026-09-30/verdicts.json etc. - verdicts kept ; find *.approval.json: 26 files (11 casting sheets, S4 front picture, P2 front picture, two voice clips, thinking sounds...) ; no approval file for Sheila's, Ron's or Darren's SHEET.md, and none for Darren's approved face (C5 or S6); production/approvals/2026-09-25-casting has no verdicts.json

### DEC-026 · BUILT **R** · DECISIONS.md:32

- **Ruling:** Claim check: second model reads each reply against what the character knows; redraft then fallback; logged unchecked. (Claude (his to overrule), 2026-09-25)
- **Superseded by:** DECISIONS.md:53, :71, :172 (the single 'That's all I know' fallback: six wordings, the card's own lines, the plain line)
- **Checked:** ledger/Assets/Scripts/Core/ClaimCheck.cs:27 - the player's words are not sent ; ledger/TalkHelper/Program.cs:268-273 - checker on the real model only, not the stand-in ; ledger/Assets/Scripts/Core/ConversationEngine.cs:1449,1787 - a redraft repeating a flagged phrase is refused (ClaimCheck.Repeats) ; TalkHelper/Program.cs:1161,1181,1208 - a failed check marked and logged 'unchecked'
- **Reviewer:** TalkHelper/Program.cs:273 sets the claim checker only when the client is an AnthropicClient; :1424-1432 wraps it in BudgetedClient whenever a budget is set; tools/ai-tester/play.py:426-428 sets the budget for real talk: so the capped measuring run had no claim check (read, not run)

### DEC-027 · BUILT · DECISIONS.md:33

- **Ruling:** The local line-writing blind test (L01) was run before the voice export fix; his blind picks on the page. (Claude (his to overrule), 2026-09-25)
- **Checked:** production/research/local-writers/README.md:48-66 - picks unblinded 29 September: paid 8, Qwen3.5-4B 3, Ministral 1 of 12 ; production/research/local-writers/key.json, letters.json, lines.json - the test's materials
- **Inferred:** The README says which writer live talk uses is his decision; no DECISIONS line records one, but the paid model is in use and he preferred it (and DECISIONS.md:189 keeps Sheila on it).

### DEC-028 · BUILT · DECISIONS.md:34

- **Ruling:** Faces cast in MetaHuman first: several candidates per sheet, front, profile, speaking in game light. (Jafar, 2026-09-25)
- **Checked:** production/approvals/2026-09-26-weekend/files.json:2-4 - P2-front, P2-profile, P2-speak candidate pictures ; production/casting/candidates-2026-09-28/{S1..S4,gate.json,MEASURES.md} - candidates per character with a gate ; CrimeProbe.cpp:905-917 - the approved candidates are what the game spawns
- **Inferred:** Only the three principals have been cast this way so far, as the 'one sample first' rule asks.

### DEC-029 · SUPERSEDED · DECISIONS.md:35

- **Ruling:** Voices free first: calm vs acted test; VoxCPM2 for prepared lines; fast model for live; paid only if free fails. (Jafar, 2026-09-25)
- **Superseded by:** DECISIONS.md:128; DECISIONS.md:105
- **Checked:** production/casting/acting-key.json - the calm-against-acted test was run (built) ; DECISIONS.md:87 - VoxCPM2 kept for Ron only; :128 - Ron's prepared lines keep the game's own engine (his blind B over VoxCPM2) ; DECISIONS.md:105 - no paid voice service ; tools/voice-live/voice-server.py:206-235 - live talk on Nano (or Sopro by spec); voice-engines.json engines {}

### DEC-030 · SUPERSEDED · DECISIONS.md:36

- **Ruling:** Clothes from FreeSewing patterns in Blender, fitted by Unreal's outfit tools; Marvelous at $39 if it stalls. (Jafar, 2026-09-25)
- **Superseded by:** DECISIONS.md:161; DECISIONS.md:211; DECISIONS.md:216
- **Checked:** DECISIONS.md:161 - MakeHuman CC0 suits bound as skinned meshes, no Marvelous ; DECISIONS.md:211 - clothing a blocked capability; Epic's plainest garments meanwhile ; DECISIONS.md:216 - Marvelous trial for one proof jacket; CLOTHES.md:13 item 0

### DEC-031 · BUILT · DECISIONS.md:37

- **Ruling:** Overnight points: Blender garment route; SLR83 voices listening candidates only; Ada keeps surname Vane. (Jafar, 2026-09-25)
- **Superseded by:** DECISIONS.md:161; DECISIONS.md:216 (the Blender garment route part)
- **Checked:** production/casting/ada/SHEET.md:1 '# Ada Vane'; tools/names-gate.py:37-39 - bare 'Vane' deliberately not retired ; game-design/picked-clips/: no SLR83 clip; tools/voice-live/voice-server.py:43-53 reads only that folder ; THIRD-PARTY.md:98 - 'one reason these are candidates only'

### DEC-032 · BUILT · DECISIONS.md:38

- **Ruling:** Quality gate: own comparison against references plus a blind reviewer before his page; rough proofs are findings. (Jafar, 2026-09-25)
- **Superseded by:** DECISIONS.md:154 (the accent checker rejecting voices: now a screen only, voices judged by ear)
- **Checked:** production/casting/candidates-2026-09-28/gate.json, production/approvals/2026-09-26-weekend/gate.json:9-19 - gate verdicts per candidate ; tools/town_day_page.py:471-474 - the blind reviewer's remaining notes shown beside items ; tools/voice-live/take_gate.py:1-25 - the voice gate's checks ; tools/candidate_page.py, tools/page_pictures.py - the 25 September page format kept
- **Inferred:** Mostly a practice: no page tool refuses an item without a gate file; evidence is that gate files exist for the page items checked. ; DECISIONS.md:196 shows the gate passed four looks he rejected; DECISIONS.md:197 raised the bar.

### DEC-033 · BUILT · DECISIONS.md:39

- **Ruling:** Faces approved as concept: Sheila C1, Ron C1, Darren C5; the flat cap rejected. (Jafar, 2026-09-25)
- **Superseded by:** DECISIONS.md:128 (Sheila S4); Ron P2 per production/specs/in-game.json:28 (no DECISIONS entry); DECISIONS.md:136 (Darren S6, not yet in the game)
- **Checked:** CrimeProbe.cpp:917 - Darren is MH_SamC5 in the game ; DECISIONS.md:128 - Sheila S4 replaced C1 (CrimeProbe.cpp:917 'S4') ; production/specs/in-game.json:28 and CrimeProbe.cpp:909-910 - Ron's P2, 'Jafar picked P2 on the 26 September weekend page', replaced C1 ; grep -i 'flat.cap' in ue-probe/Source: only MetaHumanPortrait.cpp:18-21 (a portrait-tool option), never worn in play
- **Inferred:** Ron's change from C1 to P2 has no DECISIONS.md entry; it is recorded only in in-game.json and a code comment.

### DEC-034 · PARTLY · DECISIONS.md:40

- **Ruling:** Prepared lines for Ron and Darren use an acted reference; Sheila's use her calm one. (Jafar, 2026-09-25)
- **Missing:** No prepared line for Ron or Darren uses an acted reference; the tool that makes them has no such path.
- **Impact to a player:** 2 (Only two thinking sounds per man are prepared today; flatness he already noticed in the voices.) · **belongs:** tools/voice-live/speak_lines.py and content/voice; or a DECISIONS line retiring it · **lane:** builder
- **Checked:** production/casting/acting-key.json - the decoded test (acted_reference per line) ; THIRD-PARTY.md:93 - content/voice/acks (the only prepared lines in play) 'spoken by the game's voice engine from the same game clips (Ron's p227, Darren's p241)', i.e. the calm references ; tools/voice-live/speak_lines.py:2-10 - prepared lines are made from the game clip in game-design/picked-clips; no acted-reference option ; production/casting/acting-key-2026-09-29.json - Ron's threat take B (his pick, DECISIONS.md:128) made from the calm clip rocco.p227
- **Inferred:** His later yes to the calm-clip thinking sounds and threat take (DECISIONS.md:128) may have overtaken this, but no ruling says so; the voice-direction method (DECISIONS.md:162, a clip library per mood) is the nearest successor and is on no list.

### DEC-035 · BUILT · DECISIONS.md:41

- **Ruling:** In the game: approved candidates, no donkey jacket by default, Sheila in pick D, Ron keeps p227. (Claude, under his rulings, 2026-09-25)
- **Superseded by:** DECISIONS.md:128 (Sheila S4); DECISIONS.md:136 (Darren S6, Sheila p267)
- **Checked:** CrimeProbe.cpp:915-919 - Darren C5, Ron P2, Sheila S4 spawned ; ue-probe/Source/LedgerProbe/Public/LedgerJacket.h:40-48 - jacket only with -Jacket= ; game-design/picked-clips/rocco.p227.mp3 and lena.parler-d.mp3 (the only lena clip) - voice-server.py:46-53 picks them
- **Inferred:** DECISIONS.md:136 (Sheila's voice p267) is not in the game: no p267 clip in game-design/picked-clips, grep 'p267' in tools, ue-probe/Source, production/specs, game-design: no hit.

### DEC-036 · BUILT · DECISIONS.md:42

- **Ruling:** American-accented voices out: 39 casting clips marked removed, five crowd lines replaced in English voice. (Claude, under his rulings, 2026-09-25)
- **Checked:** production/specs/street-sounds.json 'accentCheck' - Leonard's lines now crowd_m1 takes, Martha's and Kate's American line taken out ; production/casting/voice-key.json - 44 'removed' marks ; FINDINGS.md:17 - the crowd drift recorded

### DEC-037 · BUILT · DECISIONS.md:43

- **Ruling:** Backup from his approvals list; never deletes or overwrites, stays in its folder, keeps C: free, verifies, runs on summary commit. (Jafar, 2026-09-25)
- **Checked:** tools/backup-to-dropbox.py:14-40 - list from in-game.json backup lists and backupAlso; versions/<date-time>/; destination check; FLOOR_GB=1.8; SHA-256 read-back ; tools/hooks/post-commit - runs the backup when a commit changes FOR-JAFAR.md
- **Inferred:** The hook must be copied into .git/hooks on the PC; not verifiable here. ; The list follows in-game.json, which lags his latest picks (Darren S6, Sheila p267), but it backs up what the game actually uses.

### DEC-038 · BUILT · DECISIONS.md:44

- **Ruling:** Deletion only within a fixed list after an approved cleanup page; large-file record; free C: in summaries. (Jafar, 2026-09-25)
- **Checked:** tools/cleanup.py:41-65 - ALLOWED fixed list and PROTECTED paths; :203-210 deletes only groups approved on the page ; tools/large_files.py and production/large-files.json (entries) - the large-file record ; FOR-JAFAR.md Needs you item 1 - cleanup page first with C: under 60 GB; summaries give C: free

### DEC-039 · BUILT · DECISIONS.md:45

- **Ruling:** Approved cleanup: old copies deleted after proofs; voice, played game moved to F:; F: deletable only for own rejects. (Jafar, 2026-09-26)
- **Checked:** production/approvals/2026-09-25-cleanup/proofs.json - every safeguard true (renamed, moved and verified, voice made a line, build, shortcut) ; tools/play/PLAY THE ENCOUNTER.bat:23,31 and tools/ai-tester/play.py:67 - pointed at F:\LedgerTools\played-game ; tools/cleanup.py:136-151 - F:\LedgerTools deletable only for the large-file record's rejected/superseded entries
- **Inferred:** FINDINGS.md:14 - the old studio's launchers still name the deleted copy; not used by the game.

### DEC-040 · BUILT · DECISIONS.md:46

- **Ruling:** Delay fixes: helper streams a checked first sentence early; voice server prewarms; streamed sound joined with no gap. (Jafar (the list), Claude (the method), 2026-09-26)
- **Superseded by:** DECISIONS.md:132 (a plain first sentence is now spoken before its own check, narrowing 'nothing unchecked is said early')
- **Checked:** ledger/TalkHelper/Program.cs:1030-1073,1448 - --early sends the first sentence once checked and validated; CorrectLastSaid keeps what was heard (:1196) ; CrimeProbe.cpp:3218 - the game passes --early --pending ; CrimeProbe.cpp:3332-3334 - voice server started with --prewarm ; CrimeProbe.cpp:3238-3243,3748 - 'joined' pieces played with no gap

### DEC-041 · BUILT · DECISIONS.md:47

- **Ruling:** Pocket TTS set aside: it drifted American or away from the approved voices. (Claude, under Jafar's gate, 2026-09-26)
- **Checked:** production/specs/voice-engines.json - engines {} (everyone on Nano) ; tools/voice-live/voice-server.py:216-229 - only 'sopro' or 'nano' accepted; Pocket not an engine in the game ; DECISIONS.md:85 - set aside for good after a third attempt

### DEC-042 · LISTED · DECISIONS.md:48

- **Ruling:** Faces read East Asian because of street daylight; brightening the daylight toward the concept sheet is his call. (Claude; the street's light is his decision, 2026-09-26)
- **Missing:** The street's daylight was never brightened or ruled on; only the fault entry keeps it.
- **On a list:** FINDINGS.md:16
- **Checked:** production/approvals/2026-09-26-weekend/gate.json:72 - the weekend page showed faces in plain light (built) ; FOR-JAFAR.md:111 - 26 September 'Decide: Street daylight: (A) brighten it toward the concept sheet (recommended), (B) leave it' ; grep -i 'daylight' DECISIONS.md: only line 48; no answer recorded; not in the current Needs you ; DECISIONS.md:83 - the conversation light fixes faces in talk only ; …
- **Inferred:** The question to Jafar dropped out of Needs you unanswered, against CLAUDE.md's 'unresolved decisions carry forward'; the visual bar (NOW.md:10-19) covers night (V5) but no day-light item.

### DEC-043 · BUILT · DECISIONS.md:49

- **Ruling:** Week's way of working: /goal, stop hook and sitting clock removed, daily summary, research helpers, town worktree, NOW.md uncapped. (Jafar, 2026-09-28)
- **Checked:** .claude/settings.json:1-16 - permissions only, no hooks block (no Stop hook) ; ls tools/sitting-clock.py - no such file ; tools/hooks/post-commit:9-15 - backup runs when a commit changes FOR-JAFAR.md ; FOR-JAFAR.md:34,55,69 - dated per-session summaries; FOR-JAFAR.md:51 gives C: free ; …
- **Inferred:** /goal itself and the 'wait out usage limits' setting live on Jafar's PC, not in the repo; not checkable here

### DEC-044 · BUILT · DECISIONS.md:50

- **Ruling:** Blender live via official Blender Lab MCP on portable 5.2.2; Unreal Zen cache capped user-wide, old file cache delete-only. (Claude, on Jafar's instruction, 2026-09-28)
- **Checked:** tools/blender-live/start-blender-live.ps1:1-25 - starts F:\LedgerTools\blender52\blender-5.2.2 with --online-mode for the MCP add-on on port 9876 ; tools/ue/UserEngine.ini:4-12 - [Zen.AutoLaunch] ExtraArgs with --gc-cache-duration-seconds 604800 (7 days) and --gc-disksize-softlimit 10737418240; InstalledLocal DeleteOnly=true, UnusedFileAge=7 ; production/research/unreal-cache-cap/SUMMARY-2026-09-28.md:15 - zenserver.log '20G soft limit' and 'DeleteOnly' checked on the PC ; ls -a /home/user/ledger - no .mcp.json (project-scope MCP registration not in the repo)
- **Inferred:** The MCP server registration is presumably in the PC's local Claude config (start script says 'registered for this project'); not visible in the repo ; The cap is now 10 GiB (UserEngine.ini:7 says 'on his yes, 29 September'), stricter than the ruling's 20 GiB; no DECISIONS line found for the change (grep '10 GiB' DECISIONS.md: no hit)

### DEC-045 · BUILT · DECISIONS.md:51

- **Ruling:** Knowing a little shows: gaze, a half-remembered remark once per story, cooler manner in talk, only if they can tell it is him. (Claude (his to overrule), 2026-09-28)
- **Checked:** ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1091-1229 - port of RegardFor: KnowingLookSeconds 1.5, FirstLook/SecondLook metres, LooksBack, bKnowsItIsHim, MayRemarkFaintly ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5725-5815 - RegardTick each second calls StreetVoice::RegardFor for Sheila, Darren, Ron; sets head look via SetRegard; says FaintRemark to a companion once he has passed ; ue-probe/Source/LedgerProbe/Private/PersonAnim.cpp:225-234,412-418 - SetRegard drives the head look and the look back ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4566-4577 - KnowingJson sends knowing level only when bKnowsItIsHim ; …
- **Inferred:** Applies to the three cast bodies only (lena, sam, rocco); the other 37 named people have no bodies in the street

### DEC-046 · BUILT · DECISIONS.md:52

- **Ruling:** Friends meet: every friendship in hook-cast.json has pair-by-pair weekday routines; meeting frequency by tie strength. (Claude (his to overrule), 2026-09-28)
- **Checked:** production/specs/hook-cast.json - keys week, places, areas, people (41 entries), ties; each person has routine and days ; ue-probe/Source/LedgerProbe/Public/CastDay.h:269-341 - FriendsMeetDays (0.6->5, 0.45->3, else 1), Together, DaysTogetherPerWeek ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4676-4718 - LiveTiesFromCast reads hook-cast.json; in free play the whole cast joins the mill with every tie ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2389-2407 - TownHoursTick runs the town's rounds by CastDay.Together each game hour
- **Inferred:** The 'all 80 meet' assertion is in the golden/Core tests (CastDay.h:8-9 says it asserts every friendship meets); not re-run here

### DEC-047 · BUILT · DECISIONS.md:53

- **Ruling:** Live talk checked detail by detail: every specific needs a sourced item, second look on flags, six fallback wordings. (Claude (town list item 3), 2026-09-28)
- **Checked:** ledger/Assets/Scripts/Core/ClaimCheck.cs:107-155 - numbered known items (C,H,P,B,M,W,S,T); 231-247 second look for each flagged detail; 53-89 fallback wordings ; ledger/TalkHelper/Program.cs:268-274 - NewEngine sets engine.Checker = _llm when the client is AnthropicClient ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3218 - the game starts LedgerTalk with --early --pending and no budget, so in his play the client is AnthropicClient and the check runs ; ledger/TalkHelper/Program.cs:1418-1430 + 273 - WITH a budget (--budget-usd / LEDGER_TALK_BUDGET_USD) the client becomes BudgetedClient, '_llm is AnthropicClient' is false, so Checker stays null: no claim check, no promise or real-name redraft, no early first sentence (ConversationEngine.cs:1678,1730) ; …
- **Inferred:** The 30 September 'real path' measurement (production/playtest/real-talk-2026-09-30.md: words 1.9 s median, min 1.12 s, none fell back) therefore ran with the claim check OFF; its timings do not include the check the town believes they include (TOWN.md:57-58)

### DEC-048 · PARTLY · DECISIONS.md:54

- **Ruling:** Act III reads as a cab office: VAT inspection letter, Customs and Excise officer, back room, laundering ceiling on TakingsToDate. (Claude, under D58, 2026-09-28)
- **Missing:** Act III (the VAT inspection and its endings) is not in the Unreal game: ActThree.cs has no C++ port and TalkHelper does not run it; not on any list.
- **Impact to a player:** 2 (Not reachable in today's first-week build; matters only once Act III is playable.) · **belongs:** a C++ port of ActThree.cs in ue-probe/Source/LedgerProbe/Public, on ROADMAP after the friends' build · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/ActThree.cs:77,185-204,400-408,445,492 - TakingsToDate, cab-office plausibility, Schedule 7 VAT letter, Customs and Excise, back room ; grep 'ActThree/Schedule 7/Customs and Excise/TakingsToDate' in ue-probe/Source - no hit in the port (only 'minicab office' errand text, CrimeProbe.cpp:7909) ; grep 'ActThree' ledger/TalkHelper/Program.cs - no hit ; grep -i 'act iii/endings/inspection' NOW.md TOWN.md ROADMAP.md FINDINGS.md - no list line
- **Inferred:** Act III is unreachable in the current game (the game covers the first week), so the wording exists only in the C# Core

### DEC-049 · BUILT · DECISIONS.md:55

- **Ruling:** A first sentence failing its check stops the draft; the second draft is streamed at once and speaks its first passing sentence. (Claude (town list 6a), 2026-09-28)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:1357-1364,1715-1785 - stopped stream recorded, second draft (d2) streamed with Prefix 're-', 'repeats nothing in flagged' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3218 - game launches the talk program with --early --pending ; ledger/TalkHelper/Program.cs:1073 - early 'first' emitted when it passes
- **Inferred:** As with DEC-047, under a budget (BudgetedClient) Checker is null and none of this runs (ConversationEngine.cs:1678)

### DEC-050 · PARTLY **R** · DECISIONS.md:56

- **Ruling:** Every live model call can go through our relay: no key in game, per-role model, reply cap, four request kinds, allowances, 80% stop. (Claude (town list 6b); hosting and budget his, 2026-09-28)
- **Missing:** The relay was not updated for the later live calls (suggested lines, threat reading), so not every live call can go through it any more.
- **Impact to a player:** 2 (The relay is unused until friends play off his PC; then suggestions and threat reads would silently fail.) · **belongs:** ledger/Relay/Relay.cs SystemShapes (and its self-test) · **lane:** town
- **Checked:** ledger/Relay/Relay.cs:20-79 - copy codes hashed, Roles core/ambient, MaxTokens caps, CopyDayUsd 0.50, CopyMonthUsd 5.00, StopAt 0.8, logs sizes and costs only ; ledger/Relay/Relay.cs:62-71,371-398 - accepts only system prompts opening 'You are ' + 'Rules that override...', 'You read one line a character' + specifics, 'You check details against' + verdicts, or a reflection message ; ledger/TalkHelper/Program.cs:1407-1412,1436-1446 - --relay/--copy builds a keyless AnthropicClient pointed at the relay; reports go to /v1/report ; ledger/Assets/Scripts/Core/Suggest.cs:66 - suggestion prompt opens 'You suggest what Tom Nowak could say next' (matches no relay shape) ; …
- **Inferred:** Through the relay, Tom's suggested lines and the model's threat reading would be refused as 'Not one of the game's requests' and fall back silently
- **Reviewer:** Relay.cs:62-71 accepts system prompts opening 'You are ', 'You read one line a character', 'You check details against'; Suggest.cs:66 opens 'You suggest', ThreatRead.cs:23 'You read one line a man says': refused through the relay (read, not run)

### DEC-051 · LISTED · DECISIONS.md:57

- **Ruling:** Players told the town talks through an AI before first talk, can report any line; every reply marked generated. (Claude (town list 6c), 2026-09-28)
- **Missing:** The 'generated'/'model' mark reaches no subtitle log or anything machine-readable on the player's side.
- **On a list:** NOW.md:52 - "generated" and "model" into a subtitle log (6c)
- **Checked:** ledger/Assets/Scripts/Core/AiNotice.cs:13-45 - title, text, report label ; ledger/TalkHelper/Program.cs:1452 - ready line carries notice title/text/report label ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2992-3125 - notice card before the first talk, F1 shows it again ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3127-3134,5090-5098 - R reports the last reply as {"report":id} ; …

### DEC-052 · BUILT · DECISIONS.md:58

- **Ruling:** Content rule on every live line plus a narrow SafetyRule against urging self-harm; refused lines remembered as a change of subject. (Claude (town list 6e), 2026-09-28)
- **Checked:** ledger/Assets/Scripts/Core/ResponseValidator.cs:76 - SafetyRule.SpeechBreaks(reply) deflects ; ledger/Assets/Scripts/Core/ResponseValidator.cs:188-219,316 - stage-direction replies refused ; ledger/Assets/Scripts/Core/Director.cs:281 and ConversationEngine.cs:1907 - director's line and nightly beliefs pass ContentRule and SafetyRule ; ledger/TalkHelper/Program.cs:1-27 - helper runs ConversationEngine then ResponseValidator (live in the game)
- **Inferred:** The director and nightly reflection are not run by the game, so those two parts have no effect in play yet

### DEC-053 · PARTLY · DECISIONS.md:59

- **Ruling:** D58's first condition: Kingdom and Straight Life endings reachable from a hunted state; Hunted set in one place. (Claude (town list 6g), 2026-09-28)
- **Missing:** The endings and their reachability exist only in the C# Core; the game has no Act III or endings; not listed.
- **Impact to a player:** 2 (No ending is reachable in the current build; matters once Act III is playable.) · **belongs:** a C++ port of ActThree.cs in ue-probe, on ROADMAP after the friends' build · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/ActThree.cs - the endings and Hunted logic (Core only) ; ledger/Assets/Scripts/Core/ActThree.cs:71,294 - Hunted and the endings list ; grep -i 'ActThree/Hunted/Kingdom/Straight Life' in ue-probe/Source - no hit ; grep -i 'endings/kingdom/straight life' NOW.md TOWN.md ROADMAP.md FINDINGS.md - no list line
- **Inferred:** Endings are unreachable in today's first-week game

### DEC-054 · BUILT · DECISIONS.md:60

- **Ruling:** His cleanup carried out; each Unreal build clears its working copy's old history and waits for the builder's running Unreal work. (Jafar (the picks), Claude (the two steps), 2026-09-28)
- **Checked:** .github/workflows/ledger-probe-unreal.yml:392-409 - 'Wait for this PC's own Unreal work to finish' before compiling ; .github/workflows/ledger-probe-unreal.yml:3111-3121 - 'Clear the old history': git reflog expire, git gc --prune=now ; production/approvals/2026-09-28-cleanup/ exists (his picks)
- **Inferred:** The deletions themselves (14.95 GB cache, 15.67 GB working copy) happened on the PC; not checkable here

### DEC-055 · BUILT · DECISIONS.md:61

- **Ruling:** The street does not repeat itself: each bank gives an unheard line, else the one heard longest ago. (Claude (town list 6k), 2026-09-28)
- **Checked:** ue-probe/Source/LedgerProbe/Public/StreetVoice.h:656-694 - RemarkLedger with Fresh; 1283 FaintRemark uses Heard->Fresh ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5803-5820 - Recognition/FaintRemark called with &GLive.Remarks; GLive.Remarks.Heard(*Line) ; grep 'pub treating' in ue-probe/Source, Core, content, specs - no hit (the voiced pub line is gone)

### DEC-056 · BUILT · DECISIONS.md:62

- **Ruling:** Talk naming Tom can raise suspicion: the first teller's rung travels through retellings and the save; surest copy counts. (Claude (town list 6n), 2026-09-28)
- **Checked:** ue-probe/Source/LedgerProbe/Public/Gossip.h:214-242,583-617,768-781,910-917 - Rumor.OriginRung, MergeRung, carried on every retelling ; ue-probe/Source/LedgerProbe/Public/Suspecting.h:53-105 - DeedAccount.Rung read from OriginRung ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4622 - each line sends EvidenceFor(...) to the talk program, whose Suspecting.Derive sets suspicion (TalkHelper Program.cs:52-63)
- **Inferred:** FINDINGS.md:10 says the port's own suspicion number is not yet read by talk (talk reads the helper's), which this ruling does not require

### DEC-057 · PARTLY · DECISIONS.md:63

- **Ruling:** Overheard gossip and neighbours' talk do not repeat; neighbours' words no oftener than 45 s; heard-ledger saved; 27 lines replaced. (Claude (town list 6o), 2026-09-28)
- **Missing:** Free-play overheard gossip (StreetVoice::Exchange with the ledger) is never voiced and is on no list; the neighbours' own talk (Ambient) is not called (listed in V4).
- **On a list:** NOW.md:14 - V4 '... the neighbours' small talk to each other heard in play (StreetVoice.Ambient, never called ...) at the street's 45-second spacing' (covers Ambient only, not Exchange)
- **Impact to a player:** 3 (The street never passes a story aloud where he can overhear it in free play; the town's talk stays silent.) · **belongs:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp free-play tick (call StreetVoice::Exchange with &GLive.Remarks when a story passes in earshot); add to NOW.md V4 · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/StreetVoice.h:925-943,1766-1803 - Exchange and Ambient take the ledger (Fresh); 45 s pacing in the port ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:7321,7487-7492 - remarks.json saved and loaded ; grep 'Exchange(/Ambient(' in ue-probe/Source/LedgerProbe/Private - no call; Exchange reached only via ComposeOverheard (CrimeProbe.h:1221) at CrimeProbe.cpp:8547,8841, the scripted encounter, with no ledger argument ; NOW.md:14 - V4 says StreetVoice.Ambient is 'never called' ; …
- **Inferred:** In free play no overheard gossip exchange is ever voiced, so the no-repeat rule for it has nothing to act on

### DEC-058 · BUILT · DECISIONS.md:64

- **Ruling:** A per-session record on the PC (places, still spells, names, deeds, when the town knew), never typed words; a reader beside the runbook. (Claude (town list 6p), 2026-09-28)
- **Checked:** ue-probe/Source/LedgerProbe/Public/LedgerSession.h:4-6,119-164 - places within 6 m, still spells of 20 s+, start/end ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp - LedgerSession::Write events: deed, known, named, talk (who only), reply (who/how/s only), witness, police, etc. ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6956,8061 - Look ticks and Start ; tools/session_read.py:3-10 - prints what the runbook watches for, beside his four notes

### DEC-059 · BUILT · DECISIONS.md:65

- **Ruling:** The relay is not hosted until his friends test; then on his existing Hetzner server. (Jafar, 2026-09-28)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3218 - talk program launched without --relay ; NOW.md:21 - friends' build on his PC, 'no relay and no sent copies for now'
- **Inferred:** Hosting on Hetzner is a future step; nothing to check until the relay is needed

### DEC-060 · NOWHERE · DECISIONS.md:66

- **Ruling:** Tom's reading of what the ending will cost is built from what he saw and heard, never the true state. (Jafar, 2026-09-28)
- **Missing:** No reading of the ending's cost exists in Core or game; deferred by Jafar until the route works, but on no list to resume.
- **Impact to a player:** 2 (The game has no endings yet, so nothing is misread today; it becomes a trap once Act III exists.) · **belongs:** TOWN.md list (after the route), from game-design/ending-signs-2026-09-30.md · **lane:** town
- **Checked:** grep -i 'EndingReading/TomsReading/ending reading' in Core, ue-probe/Source, TalkHelper - no implementation (attempts only as .txt in production/research/ending-reading) ; game-design/ending-signs-2026-09-30.md:1-8 - third design; 'Code waits on Jafar's scope call' ; DECISIONS.md:158 - Jafar: 'The ending's signs wait until the playable route works; the design stays on file' ; TOWN.md:29-74 and NOW.md - no item for the ending reading or signs
- **Inferred:** Deferred by DECISIONS.md:158 rather than replaced; nothing carries it forward for when the route works

### DEC-061 · BUILT · DECISIONS.md:67

- **Ruling:** The town session's 863 MB F:\town-verify removed to F:'s Recycle Bin on his yes. (Jafar, 2026-09-28)
- **Checked:** production/large-files.json:1506-1512 - F:/town-verify status superseded, 'Removed on Jafar's yes, 28 September: sent to F:'s Recycle Bin (863 MB)'
- **Inferred:** The removal itself happened on the PC; only its record is checkable

### DEC-062 · BUILT · DECISIONS.md:68

- **Ruling:** Where Tom was at the deed's hour travels as a story; judged only by the talk helper (heardHimAt by time and area). (Claude (town list 6au), 2026-09-29)
- **Checked:** ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:2015-2093 - DeedJson sends sawHimAt, heardHimAt, heardHeSaid ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4600-4602 - DeedField sent with each line ; ledger/TalkHelper/Program.cs:441-475,754,817 - reads heardHimAt, judges by Cast.AreaFor

### DEC-063 · BUILT · DECISIONS.md:69

- **Ruling:** The claim check exempts a speaker's own everyday life, tastes, belongings and the street's ordinary fixtures. (Claude (town list 6at), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/ClaimCheck.cs:200-208 - the exemption in the checker's instructions ; ledger/TalkHelper/Program.cs:273 - checker live in normal play
- **Inferred:** Off under a budget wrapper, as DEC-047

### DEC-064 · PARTLY · DECISIONS.md:70

- **Ruling:** The town has its own news among the named cast, spread by gossip and told as news; one sample (Hal and Rita's row). (Claude (town list 6aq), the sample for Jafar, 2026-09-29)
- **Missing:** The sample news is not in the game: no read of town-news.json, no story filed in the mill, never overheard; so Jafar cannot meet it in the assembled game as DECISIONS.md:124 requires. Not listed.
- **Impact to a player:** 3 (Every story in play is still his; the street has nothing of its own to pass on in ordinary play.) · **belongs:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp (file TownNews stories into GMill at their hour), on NOW.md's list · **lane:** builder
- **Checked:** production/specs/town-news.json - one story, hal_rita_row, day 0 hour 11 ; ue-probe/Source/LedgerProbe/Public/TownNews.h exists; used only by CoreGolden.h:2086-2148 ; grep 'TownNews/town-news' ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp - only the #include (69) and a TownNews::Subject constant (2536); the game never reads town-news.json or files its stories ; tools/ue/stage_game_data.py:40 - town-news.json staged 'for the TownNewsWitnesses rows of the golden run' ; …
- **Inferred:** Even if filed, free play never voices an overheard exchange (see DEC-057), so the news could reach him only through talk

### DEC-065 · BUILT · DECISIONS.md:71

- **Ruling:** Each talking character has own fixed lines in the card, hidden from the model; tics bounded in the card's words. (Claude (town list 6ap), 2026-09-29)
- **Checked:** production/cast/cards/rocco.md:37-51, lena.md:36, sam.md:36 - 'Their Own Words' (known-only, deflect, brush-off, opener) ; production/cast/cards/rocco.md:12 and sam.md:12 - 'boss' now and then; 'so listen' when selling, never twice running ; ledger/Assets/Scripts/Core/CharacterCard.cs:96-107,175-180 - OwnWords parsed ; ledger/TalkHelper/Program.cs:659 - own brush-off used before the shared ones ; …

### DEC-066 · BUILT · DECISIONS.md:72

- **Ruling:** Live talk names no real brand, shop, programme, public figure or post-1992 thing; reply naming one is redrafted; Zlata dropped. (Claude (town list 6ao), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:554 - RealWorld.PromptRule in the prompt ; ledger/Assets/Scripts/Core/ConversationEngine.cs:1752-1767 - RealWorld.Find(reply) then a second draft ; grep -i 'zlata' production/cast/cards content - no hit
- **Inferred:** The redraft sits inside 'if (Checker != null)' (ConversationEngine.cs:1730), so under a budget wrapper only the prompt rule applies

### DEC-067 · LISTED · DECISIONS.md:73

- **Ruling:** Just after a deed, 90 real seconds of neighbours reacting, 90 settling, then everyday talk; first words 3 s after the hush. (Claude (town list 6an), 2026-09-29)
- **Missing:** The neighbours' reaction after a deed is never heard: StreetVoice::Ambient is not called in the game.
- **On a list:** NOW.md:14 - V4 '... the neighbours' small talk to each other heard in play (StreetVoice.Ambient, never called ...)'
- **Checked:** ledger/Assets/Scripts/Core/StreetVoice.cs:1188-1294 - JustNowSeconds 90, SettlingSeconds 180, settling banks ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1766-1803 - ported inside Ambient ; grep 'Ambient(' ue-probe/Source/LedgerProbe/Private - no call ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5795-5797 - only a 60 s hush on passing remarks after the shout
- **Inferred:** V4 names Ambient but not the deed's time; wiring it without the deed would miss this reaction

### DEC-068 · BUILT · DECISIONS.md:74

- **Ruling:** A lie can be found out later when the person learns where they saw him; hearsay counts half, once. (Claude (town list 6am), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:835-880 - a lie found out later; half a caught lie for hearsay and for what he told others ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:2016,2093 - heardHeSaid sent ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4744-4762 - his definite claim filed as a story in the mill

### DEC-069 · LISTED · DECISIONS.md:75

- **Ruling:** Asked to keep a deed quiet: nobody for a killing; Ron/Sheila for their owner; Darren yes but fragile; others first-name only. (Claude (town list 6al), for Jafar to confirm, 2026-09-29)
- **Missing:** Darren's silence breaking when someone else pays or threatens him is not in the game.
- **On a list:** NOW.md:52 - "fragile" and "grave" (6al) once paying, threatening and killing exist
- **Checked:** ledger/TalkHelper/Program.cs:932-949 - Silence.AsksQuiet, stance from Cast.QuietStance, keepsQuiet {topic, agreed, fragile} ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4766-4771 - agreed silence filed (LedgerCrime::KeepQuiet suppresses the stories) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4726 - 'NOT HERE: a fragile agreement taken back when somebody pays' ; grep 'fragile' CrimeProbe.cpp - only that comment; the game ignores 'fragile'

### DEC-070 · BUILT · DECISIONS.md:76

- **Ruling:** A suspicious character asks straight out at most twice per conversation, never again once answered; a caught lie is put instead. (Claude (town list 6ak), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:60,624-641 - MaxAsks; 'do not ask again; say what you make of that' ; ledger/Assets/Scripts/Core/ConversationEngine.cs:936-959 - AskedWhereAbout
- **Inferred:** Live through the talk program the game launches

### DEC-071 · BUILT · DECISIONS.md:77

- **Ruling:** In talk, everyone knows the nine named people; others only by description; friends' whereabouts by part of day; at most twelve. (Claude (town list 6ad), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/CastDay.cs:607-678 - MostKnown = 12, PartsOfDay ; production/specs/hook-cast.json - named people (Ron Kirby, Sheila Dunn, Darren Milner, June, Ada, Alison Sedman, Father Walsh, Rita, Hal); others only 'called' descriptions ; tools/publish-talk-helper.ps1:21 - hook-cast.json shipped beside LedgerTalk.exe; ledger/TalkHelper/Program.cs:1364-1366 LoadCast ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4606-4618 - 'present' sent from real distances

### DEC-072 · BUILT · DECISIONS.md:78

- **Ruling:** Only a plain one-place answer to their where-were-you question is laid against sightings; lie +0.15, truth -0.03; 23 areas. (Claude (town list 6ac), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/Claims.cs:86,95 - Raise(0.15*weight), Lower(0.03*weight) ; production/specs/hook-cast.json - 'areas' has 23 entries ; ledger/TalkHelper/Program.cs:783 - Claims.WhereHeSays on every line

### DEC-073 · BUILT · DECISIONS.md:79

- **Ruling:** Talk is kept with the save: .talk.json beside it, restored on load, forgotten on a new game. (Claude (town list 6r), 2026-09-28)
- **Checked:** ledger/TalkHelper/Program.cs:276-358 - talk save/load/reset with stamp ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:7314 - save sends {"talk":"save"}; 5120-5122 load or reset once the program is ready

### DEC-074 · BUILT · DECISIONS.md:80

- **Ruling:** The notice says where typed words go and what is kept: Anthropic, 30-day deletion, no training; relay keeps only reports. (Claude (town list 6w), 2026-09-28)
- **Checked:** ledger/Assets/Scripts/Core/AiNotice.cs:24-36 - TextFor(throughRelay) with both wordings ; ledger/TalkHelper/Program.cs:1452 - TextFor(relay != null) in the ready line ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3040-3125 - shown before the first talk
- **Inferred:** The notice says each line 'is checked ... before you hear it', which is false in any budget-capped run (see DEC-047)

### DEC-075 · BUILT · DECISIONS.md:81

- **Ruling:** Sheila's and Darren's faces finished from measurements (S1-S4); S4 of each to his page with the reviewer's notes. (Claude, then Jafar, 2026-09-28)
- **Checked:** production/specs/in-game.json:5-21 - Sheila in the game as MH_LenaS4 ; DECISIONS.md:136,184 - Darren approved as S6 (his S4 face with Epic's short cut) ; production/specs/in-game.json:45-60 - Darren still MH_SamC5 in the game
- **Inferred:** Darren's S4-based S6 is not yet in the game; that belongs to DECISIONS.md:136, outside this batch

### DEC-076 · BUILT · DECISIONS.md:82

- **Ruling:** The gate stops obvious failures, not imperfection: narrow-point fails go to his page with the notes. (Jafar, 2026-09-28)
- **Checked:** CLAUDE.md, 'THE GATE (Jafar, 25 September ...)' paragraph - 'The gate stops obvious failures, not imperfection ... his eye decides the rest (Jafar, 28 September)'

### DEC-077 · BUILT · DECISIONS.md:83

- **Ruling:** Conversation light: 0.6 cd key from 45 degrees, none on a sunlit face, 1 cd eye light, no shadows, skin only. (Claude, under his gate, 2026-09-28)
- **Checked:** ue-probe/Source/LedgerProbe/Public/LedgerTalkLight.h:65,68,71 - KeyCandela 0.6, SunShare 0, EyeCandela 1.0 ; ue-probe/Source/LedgerProbe/Public/LedgerTalkLight.h:73-91 - hair excluded from the light's channel ; ue-probe/Source/LedgerProbe/Public/LedgerTalkLight.h:166,182 - shadows off unless -TalkShadow ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5670-5708 - applied to whoever he talks to

### DEC-078 · PARTLY **R** · DECISIONS.md:84

- **Ruling:** A short thinking sound of their own with a glance covers the pause, cut when the answer starts; Ron and Darren two each, Sheila none. (Jafar (the list), Claude (the method), 2026-09-28)
- **Missing:** Sheila has no thinking sounds, so every line put to her waits in silence; not on any list.
- **Impact to a player:** 4 (Sheila is one of three people he talks to; her answers start about 5 s after Enter with nothing covering the wait.) · **belongs:** content/voice/acks/lena (with face animations), under NOW.md item 2 (the delay) · **lane:** builder
- **Checked:** content/voice/acks/rocco: let-me-think.wav, well-now.wav; content/voice/acks/sam: hmm-well-now.wav, let-me-think.wav ; ls content/voice/acks - no lena folder; grep 'acks/lena/ack_lena' repo-wide - no hit ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3778-3840 - AckFiles/AckStart/AckEnd: played at once, own face animation, cut by the answer ; grep -i 'thinking sound' NOW.md TOWN.md FINDINGS.md - no item for Sheila's
- **Inferred:** Sheila's voice is now decided (DECISIONS.md:136, p267), so the blocker the ruling named may be gone
- **Reviewer:** content/voice/acks holds rocco and sam only: Sheila has no thinking sounds

### DEC-079 · BUILT · DECISIONS.md:85

- **Ruling:** Pocket TTS set aside for good after its third attempt; next step a paid voice (his). (Claude, under his gate, 2026-09-28)
- **Superseded by:** DECISIONS.md:105 (the paid-voice part only)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3319 - the game starts tools/voice-live/voice-server.py, not pocket-server.py ; DECISIONS.md:105 - 'no paid voice service ... the free routes continue' (the paid-voice step is overtaken)

### DEC-080 · BUILT · DECISIONS.md:86

- **Ruling:** The skin-shell donkey jacket set aside after three blind reviews; useful parts kept; next jacket's route to Jafar as scope. (builder, 2026-09-29)
- **Checked:** FINDINGS.md:13 - no donkey jacket; the route chosen by Jafar on 30 September ; DECISIONS.md:104 (Blender stays the route), :161 (MakeHuman suits), :216 (Marvelous trial) - the scope question was answered ; CLOTHES.md:17 - the donkey jacket and suit jacket set aside

### DEC-081 · SUPERSEDED · DECISIONS.md:87

- **Ruling:** The voice gate reads every 2.5 s window: American over 0.30 anywhere rejects; VoxCPM2 kept for Ron only. (builder, 2026-09-29)
- **Superseded by:** DECISIONS.md:88; DECISIONS.md:154
- **Checked:** DECISIONS.md:88 - window rule recalibrated the same day (more than 3 s running, or 0.5 whole) ; DECISIONS.md:154 - 'the accent checker is a screen, never a gate (voices by ear)' ; tools/voice-live/take_gate.py:9-25,36-37,124 - still prints REJECT and says takes are 'rejected before he hears it'
- **Inferred:** take_gate.py's wording was not updated to 'screen'; sopro_takes.py:19 and voxcpm_takes.py:19 still call it judging takes 'before anyone hears'

### DEC-082 · SUPERSEDED · DECISIONS.md:88

- **Ruling:** Calibrated voice window rule: reject at 0.30+ American for over 3 s running, or 0.5 over the whole take. (Claude, 2026-09-29)
- **Superseded by:** DECISIONS.md:154
- **Checked:** tools/voice-live/take_gate.py:36-37,124 - AMERICAN_RUN_MAX_S 3.0, AMERICAN_WHOLE_MAX 0.5 implemented ; DECISIONS.md:154 and CLAUDE.md 'VOICES ARE JUDGED BY EAR' - the checker is a screen only, never a gate
- **Inferred:** The rule survives as the screen's threshold; only its power to reject is superseded

### DEC-083 · BUILT · DECISIONS.md:89

- **Ruling:** The story's spine is canon's baseline: Tom Nowak, three acts, three rivals, the empire roster; outline approved. (Jafar, 2026-09-28)
- **Checked:** canon.md:69-91 - 'Premise and cast (the baseline: Jafar, 2026-09-28, OPEN 2)' ; game-design/story-outline-2026-09-28.md and .approval.json beside it ; ue-probe/Source/LedgerProbe/Public/PlayerIdentity.h:30 - Surname "Nowak" for the player
- **Inferred:** Acts II and III exist only in the C# Core (see DEC-048, DEC-053)

### DEC-084 · LISTED · DECISIONS.md:90

- **Ruling:** Names: Father Brendan Walsh, Keith Garbutt, June and Michael Suddaby; Tom's past unsaid; Ada never a teacher; older Irish voice for Walsh. (Jafar, 2026-09-28)
- **Missing:** No older Irish voice for Father Walsh found or approved.
- **On a list:** NOW.md:52 - Father Walsh (emil) needs an older Irish voice for Jafar's yes
- **Checked:** canon.md:71,74-76,84-87,96-98 - Suddaby, life before the Hook unsaid, Father Brendan Walsh, Keith Garbutt, 'Ada was never a teacher' ; production/specs/hook-cast.json - id emil named 'Father Walsh' ; grep 'Walsh' Core - HookMap.cs, CastDay.cs, StreetFacts.cs, ClaimCheck.cs, OwnLines.cs ; content/dialogue/pub-regular-v1.json:41 - still 'Father Emil' (grep 'pub-regular' in ue-probe/Source and stage_game_data.py: no hit, so not read by the game)

### DEC-085 · BUILT · DECISIONS.md:91

- **Ruling:** Eleven casting sheets approved as text, approvals beside each; renamed three carry his names. (Jafar, 2026-09-28)
- **Checked:** production/casting/{ada,alison-sedman,carol-ellis,danny-cammack,father-emil,geoffrey-agar,june,maureen-jensen,philip-danby,the-fixer,tom-nowak}/SHEET.md.approval.json - all eleven exist, by Jafar, 2026-09-28 ; tools/approvals.py status() run on each: all eleven 'current' (sheet unchanged since approval) ; production/casting/father-emil/SHEET.md:1 '# Father Brendan Walsh'; june/SHEET.md:1 '# June Suddaby'; the-fixer/SHEET.md:1 '# Keith Garbutt, the Fixer' ; production/specs/hook-cast.json:1442-1445 emil named 'Father Walsh' (canon: Father Brendan Walsh); :563-565 June; :990-992 Alison Sedman; :880-882 Ada ; …
- **Inferred:** Agar, Jensen, Cammack, Danby and Garbutt are not in the street's cast yet; that is the story's scope, not a gap in this ruling.

### DEC-086 · LISTED · DECISIONS.md:92

- **Ruling:** First hour is the plan; neighbours' own talk no oftener than 45 s; Sheila names him only on trust. (Jafar, 2026-09-28)
- **Missing:** The neighbours' own talk to each other is never played in the game, so its 45-second spacing is not in effect (no C++ AmbientEverySeconds).
- **On a list:** NOW.md:14 'V4 ... And the neighbours' small talk to each other heard in play (StreetVoice.Ambient, never called ...), at the street's 45-second spacing, never during his talk.'
- **Checked:** game-design/first-hour-2026-09-29.md exists (the plan) ; production/specs/hook-cast.json:362 lena 'namesHim': 'on-trust'; production/cast/cards/lena.md:12 'Calls the player new management until they earn a name' ; ledger/TalkHelper/Program.cs:725-726 callsHim nulled unless TrustsHim for a NamesHimOnlyOnTrust card; Program.cs:2210 test 'Sheila calls him the new owner ... until it says she trusts him' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4839-4844 game reads trustEarned/trusts and sets bSheilaTrusts (saved, :7296/:7465) ; …

### DEC-087 · BUILT · DECISIONS.md:93

- **Ruling:** Claim check knows a character's own name from the card heading, not for a lent card. (Claude (town list 6be), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/ClaimCheck.cs:132-146 'Their own name is ...' item from card.Name unless ownName given (lent card: empty) ; ledger/Assets/Scripts/Core/ConversationEngine.cs:445,487 KnownItems used in the live check; Program.cs:273 engine.Checker set for the real client ; production/cast/cards/lena.md:1 '# Sheila Dunn', rocco.md:1 '# Ron Kirby', sam.md:1 '# Darren Milner' ; ledger/TalkHelper/Program.cs:2476 test 'a card lent to somebody else does not lend them its name'

### DEC-088 · BUILT · DECISIONS.md:94

- **Ruling:** Outfit's asks via Ron every other night from night one; no ends it; envelope a secret; never a game end. (Claude (town list 6z), within canon; Jafar may overturn, 2026-09-29)
- **Superseded by:** DECISIONS.md:96 (DEC-090) replaces 'three nights away in a row' and 'a night nobody answered counts as one away'; DECISIONS.md:120 (DEC-114) settles the outfit's reading
- **Checked:** ue-probe/Source/LedgerProbe/Public/Arrangement.h:57 Every = 2; :1-24 port of Arrangement.cs/TheLanding.cs; 'Never a game over' ; Arrangement.h:412-425 Record: Refused ends at once; NoShow costs patience; Witness(OutfitMan, ..., bSensitive = What == Did) so only the envelope handed over is a secret ; Gossip.h:797-812 a sensitive (night) story reaching a day-world listener raises suspicion (leak) ; production/specs/hook-cast.json:2967 outfit_man, never named, ferry_stop 22-01, cafe at 9; tie outfit_man-sam 'cafe 09:00 Mon..Fri'; sam routine [9,'cafe'] ; …

### DEC-089 · PARTLY · DECISIONS.md:95

- **Ruling:** Police: who reports, proportionate response, when DS Ellis comes, arrest or summons on a named statement. (Claude (town list 6ar), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** No summons for a common assault exists in Core or port (a named assault statement does nothing).
- **Superseded by:** DECISIONS.md:98 (DEC-092) and DECISIONS.md:186 replace 'a witness only for a crime a detective takes'; DECISIONS.md:210 adds Mickey's people never report
- **Impact to a player:** 1 (No assault deed exists in the game, so no player can reach the missing summons yet.) · **belongs:** ledger/Assets/Scripts/Core/PoliceFile.cs / Custody.cs, then PoliceFile.h · **lane:** town
- **Checked:** ue-probe/Source/LedgerProbe/Public/PoliceFile.h:403-424 WouldReport: victim of damage reports; victims settle/afraid by loyalty/nerve; killing victim never; Leashed (hooked) never; suppressed (bought) only for a killing ; PoliceFile.h:287-288 LoudAt = 3, TalkNoSoonerThan = 3 (day index 3 = day 4); :494-500 Ellis for body, detective crime, talk ; PoliceFile.h:150 Arrestable = Damage or Wounding and above; :370-382 arrest only on a Statement ; TownWeek.h:143-169 NineEllis, TenConstable; CrimeProbe.cpp:6128-6160 called hourly in the game ; …
- **Inferred:** Assault, wounding, robbery and killing are not deeds the game offers yet, so their branches are latent.

### DEC-090 · PARTLY · DECISIONS.md:96

- **Ruling:** Night away only if Ron reached him and after 1 am; three away with none done between end it; two-step no. (Claude (town list 6bn), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** 'None done between' is approximated by patience: one done night only adds 0.10, so after away, away, done, two more aways end it (should take three).
- **Impact to a player:** 2 (Only reachable on a fifth ask night, past the week's end, if he keeps the arrangement.) · **belongs:** ledger/Assets/Scripts/Core/Arrangement.cs Record/Patience, then Arrangement.h · **lane:** town
- **Checked:** ue-probe/Source/LedgerProbe/Public/Arrangement.h:63 GaveUpHour = 1; :100 AskStands needs Delivered; :413 Undelivered changes nothing ; Arrangement.h:58-59,415-419 patience: -0.34 per night away, +0.10 per night done, ended at 0 ; Arithmetic on that rule: away, away, done, away, away = 0.66, 0.32, 0.42, 0.08, 0 -> ended, though no three nights away have none done between them ; ledger/Assets/Scripts/Core/Arrangement.cs:100 AskPlainly is Ron's fixed question word for word; TalkHelper Program.cs:865-876 SoundsLikeNo -> question, ConfirmsNo -> the no ; …
- **Inferred:** Within the first week (asks on days 0, 2, 4, 6) the patience rule gives the ruling's result; the deviation needs a fifth ask night (day 8).

### DEC-091 · BUILT · DECISIONS.md:97

- **Ruling:** Shops have researched 1990 hours; everybody's talk knows them; the claim check reads them separately. (Claude (town list 6bo), 2026-09-29)
- **Checked:** production/specs/hook-cast.json:6 hours_what with the research's sources; :187-203 per-area 'hours' ; ledger/TalkHelper/Program.cs:674 engine.StreetHours = Cast.HoursFor(day, hour, minute) ; ledger/Assets/Scripts/Core/ClaimCheck.cs:105-115 O items for the street's opening hours in KnownItems

### DEC-092 · PARTLY · DECISIONS.md:98

- **Ruling:** What an arrest does: constable or Ellis, hours held by offence, caution if owned up, coat kept, bail, no game end. (Claude (town list 6bp), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** The caution path (owning up -> 2 h and no charge) is unreachable: nothing ever passes bOwnsUp. The coat does not exist in the game, so it is never kept as evidence.
- **Superseded by:** DECISIONS.md:186 replaces its witness clause ('unafraid and cooled on him') with 'reports unless on his side or talked round'
- **Impact to a player:** 3 (On the arrest path every window ends charged after 6 h; owning up to it never earns the caution the ruling promises.) · **belongs:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp ConstableHour (pass ownedUp to the deed); Core decides what owning up to police is; the coat in the ask (Arrangement) · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/PoliceFile.h:153-174 Custody::Take: window 6 h (2 h cautioned if bOwnsUp), wounding 8, robbery 12, killing 22 bailed; coat kept if bInTheCoat ; PoliceFile.h:177-182 next weekday sitting; :191-210 ReleaseWords; :222-240 SeenTaken (street sees it) ; TownWeek.h:157-169 TenConstable(..., bOwnsUp = false, bInTheCoat = false) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6069 GWeek.TenConstable(GMill.get(), &GCast, H, Area) - neither flag ever passed ; …

### DEC-093 · BUILT · DECISIONS.md:99

- **Ruling:** No API calls in development; LEDGER's key only for live talk in attended runs; no tool or workflow uses it. (Jafar, 2026-09-29)
- **Superseded by:** DECISIONS.md:126 (DEC-120) allows the key for talk measurements (about $1 a day, logged), which talk_cost_sample.py --live and first_token_sample --live use
- **Checked:** CLAUDE.md:92 NO API CALLS IN DEVELOPMENT rule ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3136-3172 LiveTalkPlayed() excludes unattended/scripted/TalkFake runs; key read only from %LOCALAPPDATA%\LEDGER\live-talk-key.txt; inherited ANTHROPIC_API_KEY cleared ; tools/blender-live/live_piece.py:50, tools/voice-live/latency.py:135, tools/ai-tester/play.py:425, tools/first_token_sample.py:66 pop ANTHROPIC_API_KEY ; .github/workflows/ledger-ai-playtest.yml:1-8 live mode removed; grep 'ANTHROPIC_API_KEY' in .github/workflows: no hit ; …
- **Inferred:** The other project's key leaving the game's secrets file is on Jafar's PC and cannot be seen from the repository.

### DEC-094 · BUILT · DECISIONS.md:100

- **Ruling:** Sheila trusts him after talk on three days, never caught out, never seen at a deed, not wary; holds once earned. (Claude (town list 6bz), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/Trust.cs:27-48 DaysTalked = 3; Suspicion Trusting; not Doubted/ToldOthers/Threatened; no contradiction; no DeedEvidence ; ledger/TalkHelper/Program.cs:186-208 TrustsHim = game said true OR engine.TrustEarned (game can grant, never take back); :1218 TrustAfter earned only on own/ended/fallback turns ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4839-4844 reads trustEarned/trusts -> bSheilaTrusts; :4548-4554 her week's question offers the real book when she trusts him; :7296,:7465 saved

### DEC-095 · BUILT · DECISIONS.md:101

- **Ruling:** Winding it down at the week's end ends Mickey's arrangement that night; Ron carries the word. (Claude (town list 6cc), for Jafar's approval, 2026-09-29)
- **Checked:** ue-probe/Source/LedgerProbe/Public/WeeksEnd.h:186 WindDown -> Asks->WoundDown(Now, Mill) ; ue-probe/Source/LedgerProbe/Public/Arrangement.h:117-136 WoundDown ends it that night; :75-76 HeardWoundDown/SaidWoundDown lines; :405-407 outfit man told once Ron has been ; WeeksEnd.h:89 TakeOver reads bArrangementEnded (no undoing a no) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4830-4836 GWeek.Week.Give(...) with &GWeek.Asks in the game

### DEC-096 · BUILT · DECISIONS.md:102

- **Ruling:** Only people, whole street frames, story, canon, money and licences reach his page; small assets pass by gate. (Jafar, 2026-09-29)
- **Checked:** CLAUDE.md:80 WHAT REACHES HIS PAGE rule ; production/art/clutter-2026-09-29/README.md:'Approval' section - nine pieces approved by the gate alone under this ruling ; README 'In the street' + tools/art-recipes/terrace-front.py:453-486 _street_furniture places them; production/assets/street/clutter/ holds seven .glb

### DEC-097 · BUILT · DECISIONS.md:103

- **Ruling:** A threat never buys silence; remembered, makes them warier, blocks Sheila's trust, is the street's story. (Claude (town list 6cd), for Jafar's approval, 2026-09-29)
- **Superseded by:** DECISIONS.md:186 (1 October: a witness 'talked round (keeps it quiet, a threat)' does not report) replaces 'never buys silence' for reporting; DECISIONS.md:140 and :150 settle his two questions
- **Checked:** ue-probe/Source/LedgerProbe/Public/Silence.h:29-56 FileThreat: first-hand story 'The new owner has been threatening people', memory 'threatened me to my face' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4788-4794 game files the reply's 'threatened' ; ledger/Assets/Scripts/Core/Trust.cs:34 Threatened blocks trust ; ledger/TalkHelper/Program.cs: Silence.Threatens/Menaces/AsksQuiet, ThreatRead.Parse/Ask called (how a threat is read, settled by DECISIONS.md:150)
- **Inferred:** N3 (a threat stops a witness reporting) is listed for the port at NOW.md:8; that belongs to the superseding ruling, not this one.

### DEC-098 · SUPERSEDED · DECISIONS.md:104

- **Ruling:** The jacket: Blender stays the route; drape arms out, one more day; then check MD scripting. (Jafar, 2026-09-29)
- **Superseded by:** DECISIONS.md:161 (30 Sep, MakeHuman suits and coats) and DECISIONS.md:216 (1 Oct, Marvelous Designer joins the clothing lane)
- **Checked:** FINDINGS.md:13 the sewn jacket's sleeves failed by two methods; 'Jafar chose the route on 30 September: MakeHuman's free suits and coats' ; CLOTHES.md item 0: Marvelous Designer proof (1 October)

### DEC-099 · BUILT · DECISIONS.md:105

- **Ruling:** No paid voice service for the delay; free routes continue. (Jafar, 2026-09-29)
- **Checked:** grep -i 'inworld/elevenlabs/cartesia' in ue-probe/Source, tools/voice-live, TalkHelper, Core: no hit ; tools/voice-live/ holds the free local route (export-for-game.py, latency.py, make_portable.py) ; NOW.md:20 item 2, the delay, worked on the free route; FINDINGS.md:15 voice speed on the card

### DEC-100 · SUPERSEDED · DECISIONS.md:106

- **Ruling:** Hair curls made in Blender, not Fab's paid haircuts. (Jafar, 2026-09-29)
- **Superseded by:** DECISIONS.md:184 (2026-10-01, the hair call settled by his own picks); set aside at DECISIONS.md:129
- **Checked:** DECISIONS.md:129 curls set aside after three attempts ; DECISIONS.md:184 hair settled by his picks: Darren S6 with Epic's library cut, Sheila S4's own hair, no curls made

### DEC-101 · LISTED · DECISIONS.md:107

- **Ruling:** Clothing to a third Blender session; builder fits by script and puts dressed people on his page; working rules. (Jafar, 2026-09-29)
- **Missing:** Dressed characters on his page: not yet (clothing blocked; plain garments due under V9).
- **On a list:** NOW.md:19 'V9. Everyone in plain 1990 clothes, no contrast stitching and no trainers, with the clothing session's garments as they pass'
- **Superseded by:** DECISIONS.md:151 (garments bound as skinned meshes, panel by panel) replaces the resizing-graph fit; DECISIONS.md:212 replaces the builder's order
- **Checked:** CLAUDE.md:63-69 three sessions, clothing session's folders; CLAUDE.md:58,87,88 two-tries, before-push, done rules ; CLOTHES.md exists with the clothing session's list ; production/specs/in-game.json:99-108 F:/LedgerTools/bodies and garments in the backup list ; tools/ue/import_garments.py:1-25 builder fits garments by script; NOW.md:37 boots and handbag in the game ; …

### DEC-102 · BUILT · DECISIONS.md:108

- **Ruling:** Names by knowing: the new owner, Nowak once known, Tom after two days or asked, never Tommy week one. (Claude (town list 6ch), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/PlayerIdentity.cs:142-155 RungByKnowing; Tommy for nobody in the first week; never back down ; ledger/TalkHelper/Program.cs:703-723 GivesName, MickeysOwn, RungByKnowing, callsHim from the rung when the game sends none ; ue-probe/Source/LedgerProbe/Public/PlayerIdentity.h:36-68 NameTold files his name as a street fact; CrimeProbe.cpp:4783-4784 on the reply's gaveName ; TalkHelper Program.cs:725-726 Sheila still only on trust

### DEC-103 · BUILT · DECISIONS.md:109

- **Ruling:** A wait or sleep stops early for the town's beats, one line each, never twice; Ron knocks on a sleep. (Claude (town list 6ci), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ue-probe/Source/LedgerProbe/Public/Waiting.h:100-109 lines: Ron, landing, tea, constable, Ellis, Sheila's Sunday and last hour, release ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6619-6700 WaitKeyTick (Z): Waiting::Next hour by hour, Showed, GWaitShown kept in the save; 8 h if nothing due

### DEC-104 · BUILT · DECISIONS.md:110

- **Ruling:** Friends' talk through the relay gets no key yet. (Jafar, 2026-09-29)
- **Checked:** ledger/Relay/Relay.cs:40-41,101 key only from the server's environment, never in a file ; grep -i 'relay' in .github/workflows and the game's CrimeProbe.cpp: no hit (no deployment, game does not use it) ; DECISIONS.md:200 friends play on his PC, no relay for now
- **Inferred:** No server holds a key: inferred from no deployment config in the repository.

### DEC-105 · BUILT · DECISIONS.md:111

- **Ruling:** Sessions decide within canon, one DECISIONS line each; only identity or hard-to-undo calls, at most three a day. (Jafar, 2026-09-29)
- **Checked:** CLAUDE.md:79 EVERY PAGE FITS ONE PHONE SCREEN: at most three decisions; decided items go to DECISIONS.md ; tools/town_day_page.py:131-151 the 30 Sep page's three calls (how Mickey died, winding down, threats), 'at most three new a day' ; DECISIONS.md:112-125 the town-decided entries recorded one line each

### DEC-106 · BUILT · DECISIONS.md:112

- **Ruling:** The day runs at two game minutes a real second (twelve real minutes a day). (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ue-probe/Source/LedgerProbe/Public/LiveClock.h:5-8,37 MinutesPerRealSecond = 2.0 ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:376-382 GClock, :6254 ticked a frame at a time

### DEC-107 · NOWHERE · DECISIONS.md:113

- **Ruling:** Each thing that decides the ending gets a sign Tom sees that changes exactly at its line. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** No sign, no reading and no ending in the Unreal game; the design waits with no list entry.
- **Impact to a player:** 2 (The game has no endings yet, so no player meets the gap until endings are ported.) · **belongs:** TOWN.md list (deferred item after the route); Core ActThree factors, then the port · **lane:** town
- **Checked:** game-design/ending-signs-2026-09-30.md:9 'Code waits on Jafar's scope call'; :21-22 'The Unreal game has no endings yet. Nothing that decides them is ported.' ; grep -i 'EndingReading/TomsReading/ending sign' in Core, ue-probe, TalkHelper: no hit (attempts only in production/research/ending-reading/*.txt) ; DECISIONS.md:158 (Jafar, 30 Sep) 'The ending's signs wait until the playable route works' ; grep -i 'ending' in TOWN.md, NOW.md, FOR-JAFAR.md, ROADMAP.md: no list item
- **Inferred:** Deferred by DECISIONS.md:158 rather than replaced; but no current list carries it, so it can be forgotten.

### DEC-108 · BUILT · DECISIONS.md:114

- **Ruling:** Mickey's own people (Sheila, Ron, Darren) know Tom's name before he comes; the rest do not. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/PlayerIdentity.cs:153 MickeysOwn = lena, rocco, sam ; ledger/TalkHelper/Program.cs:709-712 MickeysOwn learn the name from day 0; others only when told or the game says so

### DEC-109 · NOWHERE · DECISIONS.md:115

- **Ruling:** The privacy notice is drafted before any friend plays through our server, not now. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** A privacy notice draft, gated on server play; not on any list.
- **Impact to a player:** 1 (No one plays through the server; it matters only before relay play begins.) · **belongs:** ROADMAP.md 'Then' pre-server list (beside the AI notice) · **lane:** town
- **Checked:** grep -i 'privacy notice' in TOWN.md, NOW.md, ROADMAP.md, FOR-JAFAR.md, the sweep's BUILDER.md: no hit ; ROADMAP.md:48-53 pre-server list names an AI notice, a report button, Steam's description, but no privacy notice ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3041 ShowAiNotice (the notice already shown) ; DECISIONS.md:200 friends play on his PC, no relay, so the trigger is not live
- **Inferred:** Nothing is due now; the risk is that server play starts without the draft, since no list carries the condition.

### DEC-110 · BUILT · DECISIONS.md:116

- **Ruling:** The claim check's retune goes ahead on the subscription, in small runs (town list q). (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** production/research/grounded-replies/PLAIN-AND-CHECK-2026-09-30.md:42-65 retune run on a 255-detail labelled bench, four versions; 'Today's check stays; tuning it is set aside after three tries' ; TOWN.md:69 'the check's tuning (kept as it is)' ; DECISIONS.md:142 reopened by Jafar on 30 Sep, method first
- **Inferred:** The run happened and ended in a set-aside, so the ruling's action is done; the fault stays in FINDINGS.md:11 and :19.

### DEC-111 · LISTED · DECISIONS.md:117

- **Ruling:** Who keeps a deed quiet for Tom stays as read from the cards (DECISIONS.md:75). (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** Darren's fragile silence (breaks when anyone else pays or threatens him) and the killing case are not wired in the game.
- **On a list:** NOW.md:52 'From the town, still to do when the game has them: ... "fragile" and "grave" (6al) once paying, threatening and killing exist'
- **Checked:** production/specs/hook-cast.json:296,361 keepsQuiet 'owner' (Ron, Sheila); :614 'anyone' (Darren) ; ledger/TalkHelper/Program.cs: Silence.AsksQuiet/Agrees/Fragile called; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4766-4771 game files keepsQuiet.agreed (KeepQuiet) ; NOW.md:52 '"fragile" and "grave" (6al) once paying, threatening and killing exist' - Darren's silence breaking when another pays or threatens him is not in the game

### DEC-112 · BUILT · DECISIONS.md:118

- **Ruling:** Each friend's copy keeps an allowance of $0.50 a day and $5 a month. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ledger/Relay/Relay.cs:48-49 CopyDayUsd = 0.50, CopyMonthUsd = 5.00; :241-258 allowance enforced before the call

### DEC-113 · BUILT · DECISIONS.md:119

- **Ruling:** Street's plain facts written for everybody: locked door, funeral, will, flat, drivers, takings, cafe. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/StreetFacts.cs:33-61 facts: died, fire, will, funeral, june, flat, door (Sheila keeps the key), drivers, hours ; ledger/TalkHelper/Program.cs:1390-1391 StreetFacts.AddTo(card, key) for every talking card; :2373-2377 test lists door, funeral, will, flat, drivers, hours, trade, cafe

### DEC-114 · BUILT · DECISIONS.md:120

- **Ruling:** The outfit is somebody else's; Tom inherits Mickey's place; not one of the three rivals. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** production/specs/hook-cast.json:2967 outfit_man role 'one of the outfit Mickey had his arrangement with, never named' ; ue-probe/Source/LedgerProbe/Public/Arrangement.h:73-77 lines speak of Mickey's arrangement with an unnamed outfit; tools/town_day_page.py:81 recommended reading

### DEC-115 · BUILT · DECISIONS.md:121

- **Ruling:** The street's talk brings DS Ellis once three of his day world pass it round, from day 4. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** ue-probe/Source/LedgerProbe/Public/PoliceFile.h:287-288 LoudAt = 3, TalkNoSoonerThan = 3 (index; Core PoliceFile.cs:69-71 'the first hour's day 4') ; PoliceFile.h:500 talk visit; TownWeek.h:143-152 NineEllis; CrimeProbe.cpp:6138 called at nine each day

### DEC-116 · BUILT · DECISIONS.md:122

- **Ruling:** The warehouse fire drafted from the outline; the street's version said, the truth kept apart. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Checked:** game-design/warehouse-fire-2026-09-29.md and its .approval.json ; ledger/Assets/Scripts/Core/StreetFacts.cs:41-44 'fire' street fact (last November, arson by the paper, nobody charged, insurance rumour); the truth absent ; DECISIONS.md:141 Jafar picked the draft on 30 Sep

### DEC-117 · NOWHERE **R** · DECISIONS.md:123

- **Ruling:** Everybody gets own nerve, loyalty and greed; the rule answering the bravest as frightened is fixed. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** No per-person nerve, loyalty or greed in the cast file, Core or port; the inverted nerve rule still in Core and port.
- **Impact to a player:** 3 (Forty people with one temper react alike (every witness reports or none), which shows over a longer session.) · **belongs:** production/specs/hook-cast.json + CastDay.cs/CastDay.h; StreetVoice.cs:813/StreetVoice.h:457; TOWN.md list · **lane:** town
- **Checked:** game-design/town-traits-draft-2026-09-29.md:3-6 'A DRAFT, NOT IN THE GAME ... Taken back out of the cast file ... kept here for Jafar's answer on its scope' ; grep '"nerve"/"greed"/"loyalty"' in production/specs/hook-cast.json: 0 hits; Gossip.cs:109-111 and Gossip.h:301 everybody 0.5 ; ledger/Assets/Scripts/Core/StreetVoice.cs:813 and ue-probe/.../StreetVoice.h:457 still 'Nerve > 0.65 && Sensitive -> nervous' (the bravest answered as frightened), unfixed ; grep 'traits/bj/nerve' in TOWN.md, NOW.md, FOR-JAFAR.md Needs you: only TOWN.md:27 'C5's nerve' (saving Nerve, review C5), not this
- **Inferred:** DECISIONS.md:126 (no new systems) may be why it stopped, but it does not replace the ruling, and the scope question is not in Needs you.
- **Reviewer:** production/specs/hook-cast.json has no 'nerve' field; StreetVoice.cs:813 and StreetVoice.h:457 still answer Nerve > 0.65 as nervous

### DEC-118 · PARTLY · DECISIONS.md:124

- **Ruling:** The town's one news sample stands; ten more wait until Jafar meets it in the assembled game. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** The sample is never loaded or filed in the game, so Jafar cannot meet it in the assembled game.
- **Impact to a player:** 2 (One ambient happening on day one; it would be heard mostly in neighbours' talk, which is not played either.) · **belongs:** ue-probe/Source/LedgerProbe/Public/TownWeek.h hourly step + CrimeProbe.cpp load of production/specs/town-news.json · **lane:** builder
- **Checked:** production/specs/town-news.json: 1 story (hal_rita_row, day 0 11:00) ; ue-probe/Source/LedgerProbe/Public/TownNews.h: port of TownNews.cs (Parse, stories, filed) ; grep 'TownNews ' instances in ue-probe: only CoreGolden.h:2104,2147,2185 (tests); grep 'town-news.json' in ue-probe Private: no hit ; TownSave.h:49,62 saves NewsFiled, but nothing in the game files a story ; …

### DEC-119 · PARTLY **R** · DECISIONS.md:125

- **Ruling:** Settled as written: hints, first ask, Ellis, Ada's tea, first hour, police asking, arrest words, week's end, day one, wait, landing man. (Claude (town), within canon; Jafar may overturn, 2026-09-29)
- **Missing:** The man at the landing's lines (when next, kept waiting, nothing for me, we're done, brush-offs) are never shown; coat and Ledger hints wait on features not in the game.
- **Impact to a player:** 4 (Most players carry the first envelope about ten minutes in; the design's lines telling when to come back are missing there.) · **belongs:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp quay handling (~:6242) calling TheLanding::Line · **lane:** builder
- **Checked:** Hints: CrimeProbe.cpp:2723,7805-7887 FirstMoments shown; coat and Ledger hints held, 'its key is not in the game yet' (:7801) ; Ask, Ellis, tea, arrest words, week's end, wait: CrimeProbe.cpp:4542,6138,6147,6072,4833,6619-6700 ; Police asking: PoliceFile.h:547-552 Asked files the story; TownWeek.h:151 ; Day one: bSheilaMet walk-round, Waiting.h:100 WalkRoundLine ; …
- **Reviewer:** grep 'TheLanding::' in ue-probe/Source/LedgerProbe/Private: no hit; CrimeProbe.cpp:6247 shows the game's own caption instead

### DEC-120 · BUILT · DECISIONS.md:126

- **Ruling:** No new systems until the slice is worth playing; town's order; done means wired and walked; key for measurements only. (Jafar, 2026-09-29)
- **Checked:** TOWN.md:29-66 the list in that order; TOWN.md:73 'Stop: new systems, checklist sweeps ...' ; CLAUDE.md:58,87,88 two-tries, before-push, done rules ; tools/talk_cost_sample.py:55 LIVE_DAILY_USD = 1.00, :82 refused under CI; production/playtest/talk-runs.jsonl 4 runs logged with tokens and dollars

### DEC-121 · BUILT · DECISIONS.md:127

- **Ruling:** The magistrates' day (town list bv) is set aside unpushed; its research stays. (Claude (town), under Jafar's ruling, 2026-09-29)
- **Checked:** production/research/police-response-1990/COURT-2026-09-29.md exists ; grep -i 'magistrates' in Core: only Custody.cs bail words and PoliceFile.cs comments; no court-day system
- **Inferred:** The charge's words still name a court day on which nothing happens; that is the set-aside's consequence.

### DEC-122 · BUILT · DECISIONS.md:128

- **Ruling:** His Wednesday picks: Sheila S4 in game, Darren S4 no, Ron's threat keeps the game's voice engine, other yeses. (Jafar, 2026-09-29)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:912-917 Sheila's take S4 loaded first; Darren stays C5 ; production/specs/in-game.json placed: Sheila 'take S4' ; CrimeProbe.cpp:3600-3653 thinking sounds; :141,5670-5686 LedgerTalkLight conversation light; PersonAnim.cpp:37-66 head look-at ; DECISIONS.md:183 Ron stays on the game's voice engine

### DEC-123 · BUILT · DECISIONS.md:129

- **Ruling:** Set aside Blender curls and the three spare builds; Epic library haircuts put to him as a call. (Claude, 2026-09-29)
- **Checked:** NOW.md:39 'the three builds (MH_BuildSlim/Average/Heavy) are still the preset's one body and set aside' ; DECISIONS.md:184 the hair call settled by his picks (Darren S6 with Epic's cut, Sheila S4's hair)
- **Inferred:** Darren's S6 is not yet loaded in the game (CrimeProbe.cpp:917 uses C5); that belongs to DECISIONS.md:184.

### DEC-124 · BUILT · DECISIONS.md:130

- **Ruling:** FOR-JAFAR.md opens with one builder-kept overview: Needs you (max five) and Road to worth playing. (Jafar, 2026-09-29)
- **Checked:** FOR-JAFAR.md:8-60 'Overview (Thursday 1 October, 20:20)', 'Needs you' three items with pages and recommendations, 'Road to worth playing' with owner, state and change per line ; CLAUDE.md:31 THE OVERVIEW rule

### DEC-125 · PARTLY **R** · DECISIONS.md:131

- **Ruling:** Pillar box and kiosk get made-up 1990-style marks; they stand plain until the marks pass the gate. (Claude, within canon; Jafar may overturn, 2026-09-29)
- **Missing:** The made-up postal cipher and telephone company mark do not exist and no list asks for them; the pieces stand plain.
- **Impact to a player:** 2 (A blank pillar box and kiosk in the street read as placeholders to a British eye, against the bar.) · **belongs:** content/brands/brand-bible-v1.json + tools/meshgen/blender/clutter/pillar_box.py, kx100_kiosk.py; NOW.md V2/V4 · **lane:** builder
- **Checked:** tools/meshgen/blender/clutter/pillar_box.py:13-15 'NO CIPHER, CROWN OR LETTERING YET'; kx100_kiosk.py:12-13 'NO OPERATOR MARK' ; production/assets/street/clutter/pillar-box.glb, kx100-kiosk.glb placed plain (terrace-front.py) ; content/brands/brand-bible-v1.json: no postal cipher or telephone company mark ; grep -i 'cipher/cypher/operator mark/telephone company' in NOW.md, TOWN.md, FINDINGS.md, FOR-JAFAR.md, ROADMAP.md: no hit
- **Reviewer:** content/brands/brand-bible-v1.json:11 'MICKEY'S IS A PUB AND STAYS A PUB', :88-89 kind 'pub', founded 1962; no kiosk mark or postal cypher in the brand bible

### DEC-126 · BUILT · DECISIONS.md:132

- **Ruling:** A plain first sentence is spoken without its own check; the whole reply is still checked. (Claude (town), 2026-09-29)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:1441-1450 PlainWords.IsPlain(said) skips the first sentence's check; the whole reply goes through CheckLine later ; ledger/Assets/Scripts/Core/PlainWords.cs:54 IsPlain ; production/research/grounded-replies/NOTE-2026-09-29.md and FINDINGS.md:19 the fallback rate recorded as set aside

### DEC-127 · BUILT · DECISIONS.md:133

- **Ruling:** Tom's footsteps cut from two CC0 trainer recordings, credited (Claude, 2026-09-30)
- **Checked:** THIRD-PARTY.md:364-369 - sturmankin (Freesound 273077) and Joseph Sardin (BigSoundBank s0514), CC0 ; production/assets/steps - step-walk-0..7.wav, step-run-0..7.wav ; tools/ue/import_sounds.py:17,68 - imports to /Game/Ledger/Sounds/Steps ; ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:139,142-200,253-257 - StepTick loads the clips and plays one per landing ; …

### DEC-128 · BUILT · DECISIONS.md:134

- **Ruling:** Mouths follow voice loudness via face rig; garments worn by script from garments.json, unfit ones held (Claude, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Private/PersonAnim.cpp:500 - jawOpen from loudness; :268-300 mouth controls only ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3464 - per-sentence level (MouthLevelFrom) opens the jaw; :3885 loudness mouth kept by his picks ; ue-probe/Source/LedgerProbe/Public/LedgerGarments.h:32-35,87-100 - reads production/specs/garments.json, skips entries with 'hold' unless -WearHeld ; production/specs/garments.json - SheilaSpectacles/GlassesChain held with picture path (spectacles-on-S4-in-game.jpg) ; …
- **Inferred:** The 'streaming solver next' part was overtaken by later rulings (item 4 settled 1 Oct; V8 audio-driven mouths for prepared lines, NOW.md:18); not judged as missing.

### DEC-129 · PARTLY **R** · DECISIONS.md:135

- **Ruling:** Day one: Sheila's walk-round first, then hints and errand; arrival waits for day 0 (builder, 2026-09-30)
- **Missing:** His arrival on day 0 (DayOne::Arrived filing who saw him come, and StreetVoice::ArrivalLine said to his face once) is ported but never called by the game, and no list carries it.
- **Impact to a player:** 3 (The street's first talk of the newcomer ('You'll be Mickey's nephew, then') is designed for the first minutes and never happens.) · **belongs:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp (free-play day 0 and the passing-remark path); NOW.md builder's list · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:8050-8056 - new free-play game enters LiveWalkRound; :7948-7967 WalkRoundTick shows DayOne::WalkRound stops; :7925-7943 WalkRoundEnd starts hints ; ue-probe/Source/LedgerProbe/Public/DayOne.h - WalkRound, WalkRoundEnds, Arrived ported; CoreGolden.h:1916-1974 rows ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:8030 - a new free-play game now starts at GameTime(0, 9, 0): day 0 exists ; grep 'DayOne::Arrived/ArrivalLine/player.arrived' in ue-probe/Source/LedgerProbe/Private: no hit (only CoreGolden.h test rows) ; …
- **Inferred:** The ruling's condition for the arrival (a running first week with a day 0) appears met, yet nobody picked it back up.
- **Reviewer:** CrimeProbe.cpp:8030 a free-play new game starts on day 0 at 09:00; DayOne::Arrived and StreetVoice::ArrivalLine are called only in CoreGolden.h:1916-1976 (the tests)

### DEC-130 · PARTLY **R** · DECISIONS.md:136

- **Ruling:** Darren S6 into the game; Ron on Nano; Sheila p267; OFL allowed, Marcellus SC plates; cleanup (Jafar, 2026-09-30)
- **Missing:** Darren's approved S6 face is not in the game (C5 loads). Sheila's approved p267 voice is not in the game (she still speaks from lena.parler-d, which leans American); the check of p267 through the game's own engine is not recorded. Neither is on the builder's list.
- **Impact to a player:** 4 (Sheila and Darren are two of the three talking characters; the player sees the unapproved face and hears the American-leaning voice in ordinary play.) · **belongs:** CrimeProbe.cpp:917 (Darren's take), game-design/picked-clips + production/specs/in-game.json (Sheila's clip); NOW.md builder's list · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:917 - Approved take for Sam is still 'C5' (MH_SamC5); no S6 anywhere in ue-probe/Source, tools/ue or production/specs ; production/specs/in-game.json:43-62 - Darren 'take C5'; Sheila 'voice lena.parler-d ... it leans American' ; tools/voice-live/voice-server.py:43-52 - voice learned from game-design/picked-clips/<who>.*; game-design/picked-clips has lena.parler-d.mp3, no p267 clip ; grep -rl p267 (whole tree): only FOR-JAFAR.md, DECISIONS.md, approval page files, voice-candidates/listen.html, casting REVIEW.md - no spec, clip or tool ; …
- **Inferred:** FINDINGS.md:18 still says Sheila's voice 'waits on the paid-voice decision', which his p267 yes settled; stale.
- **Reviewer:** CrimeProbe.cpp:917 hard-codes Darren's approved take as 'C5'
- **Reviewer:** game-design/picked-clips holds one Sheila clip, lena.parler-d.mp3; voice-server.py:46-52 clip_for takes the first lena.* clip; grep 'p267' in tools, production/specs, ue-probe/Source, game-design: no hit (a clip kept only on Jafar's PC cannot be seen from here)

### DEC-131 · BUILT · DECISIONS.md:137

- **Ruling:** Local build and tester close allowed; full-size pictures on every page; capped key only for live talk (Jafar, 2026-09-30)
- **Checked:** .claude/settings.json - allows 'powershell.exe -NoProfile -File tools/ue/build-local.ps1' and 'python tools/ai-tester/play.py close' ; tools/page_pictures.py exists; imported by approval_page, candidate_page, day_page, ingame_page, town_day_page, town_page, weekend_page ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3135-3172 - key read only from live-talk-key.txt in played runs, cleared otherwise ; CLAUDE.md 'RESEARCH THE METHOD BEFORE THE SYMPTOM' - the rule is written

### DEC-132 · BUILT · DECISIONS.md:138

- **Ruling:** Mickey died of his heart at the office; Ron found him; a street fact for every talker (Jafar, 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/StreetFacts.cs:35-39 - died_heart fact, Ron's own words ; ledger/Assets/Scripts/Core/StreetFacts.cs:130-136 - AddTo puts the facts in each card's HardFacts ; ledger/TalkHelper/Program.cs:1391 - every loaded card gets StreetFacts.AddTo

### DEC-133 · BUILT · DECISIONS.md:139

- **Ruling:** Winding the business down ends Mickey's arrangement (Jafar, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/WeeksEnd.h:186 - WindDown answer calls Asks->WoundDown ; ue-probe/Source/LedgerProbe/Public/Arrangement.h:75-76,119-138 - WoundDown ends it and Ron takes the word to the landing ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4829-4836 - Sheila's weekAnswer from the talk applied via GWeek.Week.Give
- **Inferred:** Arrangement.h:70 comment still says 'WeeksEnd is not ported yet' (stale comment, not a fault).

### DEC-134 · BUILT · DECISIONS.md:140

- **Ruling:** Threat never buys silence; checking model reads deed lines for threats, live key only (Jafar, 2026-09-30)
- **Superseded by:** DECISIONS.md:186 (the 'never buys silence' half only)
- **Checked:** ledger/TalkHelper/Program.cs:952-975 - ThreatRead by the checking model beside the reply, only with a client and a deed topic ; ledger/TalkHelper/Program.cs:164-168 - ThreatByModel true, ThreatWait 2 s ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3135-3172 - the key reaches the talk program only in played runs ; ledger/Assets/Scripts/Core/Silence.cs:180-189 - code still says a threat never buys silence
- **Inferred:** The 'never buys silence' half was reversed on 1 October (a witness can be talked round by a threat); that reversal is N3 on NOW.md:8, not yet on main.

### DEC-135 · BUILT · DECISIONS.md:141

- **Ruling:** The warehouse fire as the street tells it is a street fact; never the truth (Jafar, 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/StreetFacts.cs:40-44 - fire fact: last November, Saturday night, arson by the paper, nobody charged, owner for the insurance ; ledger/TalkHelper/Program.cs:1391 - given to every card

### DEC-136 · BUILT · DECISIONS.md:142

- **Ruling:** The check's retune reopened, starting with research into the method (Jafar, 2026-09-30)
- **Checked:** production/research/talk-helper/METHOD-2026-09-30.md, production/research/grounded-dialogue-selection/SUMMARY.md - method research ; production/research/grounded-replies/PLAIN-AND-CHECK-2026-09-30.md - tuning on 255 labelled details
- **Inferred:** The retune was then tried three times and set aside (DECISIONS.md:169); the ruling's own ask (reopen, method first) was carried out.

### DEC-137 · LISTED · DECISIONS.md:143

- **Ruling:** Steam's AI disclosure approved as drafted (Jafar, 2026-09-30)
- **Missing:** The store page / Valve survey that uses the text.
- **On a list:** ROADMAP.md:52
- **Checked:** production/store/steam-ai-disclosure.md - the draft; .approval.json beside it (Jafar, 30 Sep, against its hash) ; ROADMAP.md:52 - 'Steam's safeguards description' before anyone outside his friends plays
- **Inferred:** Nothing in the game uses it; it belongs to the store page, which does not exist yet. ; The approved text says replies go 'through LEDGER's own server'; the friends' build ruling of 1 Oct has no relay, so the text will need re-checking before the store page (and re-approval if edited).

### DEC-138 · BUILT · DECISIONS.md:144

- **Ruling:** Method research first; answered items never reappear; pages dated today; pictures full size (Jafar, 2026-09-30)
- **Checked:** tools/town_day_page.py:22-33,124-126,449-450 - answered keys from production/approvals/town-answered.json left out ; tools/town_day_page.py:527-530 - refuses a page not dated today ; tools/town_day_page.py:439-440 - page_pictures.apply ; CLAUDE.md 'RESEARCH THE METHOD BEFORE THE SYMPTOM'
- **Inferred:** Only the town's page tool was checked for the answered-item filter; the builder's page tools were not.

### DEC-139 · BUILT · DECISIONS.md:145

- **Ruling:** Talk grounds the reply before writing: the facts bearing on his line put first (Claude (town), 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/ClaimCheck.cs:1076 - Bearing ; ledger/Assets/Scripts/Core/ConversationEngine.cs:77 - ChooseFirst = true; :482-500 bearing items and 'What none of it gives, you do not know' ; ledger/TalkHelper/Program.cs - the game's talk program runs ConversationEngine

### DEC-140 · BUILT · DECISIONS.md:146

- **Ruling:** Check clears word-for-word stated details and present-tense people lines by code (Claude (town), 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/ClaimCheck.cs:299 - stated details cleared via StatedIn/Timeless ; ledger/Assets/Scripts/Core/ClaimCheck.cs:828 Timeless, :1032 StatedIn

### DEC-141 · BUILT · DECISIONS.md:147

- **Ruling:** --pending sends the first sentence before its check; game plays it only when cleared (Claude (town), 2026-09-30)
- **Checked:** ledger/TalkHelper/Program.cs:156-158,1449,1780-1781 - --pending ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3215-3218 - the game launches the talk program with '--early --pending' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3244-3247,4442-4470,4968 - pending pieces held until the matching first arrives

### DEC-142 · LISTED · DECISIONS.md:148

- **Ruling:** Named characters' own street lines first; Ron's 159 as the sample; thirty years on the docks (Claude (town), within canon, 2026-09-30)
- **Missing:** Ron's 109 ambient lines (about two thirds of his 159) are never heard because the game never calls StreetVoice::Ambient.
- **On a list:** NOW.md:14
- **Checked:** ue-probe/Source/LedgerProbe/Public/OwnLines.h - generated port; Ron: 109 ambient, 47 recognition, 3 faint lines ; ue-probe/Source/LedgerProbe/Private/LedgerProbe.cpp:836-840 - OwnLines on by default ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1257-1278,2106 - own lines taken first ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5813 - StreetVoice::Recognition called; grep 'StreetVoice::Ambient' in Private: no hit ; …

### DEC-143 · PARTLY · DECISIONS.md:149

- **Ruling:** The thirty regulars chosen within canon and census; one contact sheet on his page (Claude (town), within canon, 2026-09-30)
- **Missing:** Nothing of the regulars is in the game: names, ages, trades and voice slots are not in the cast file or talk cards, and the old tier-2 cards still give some of them other ages and trades.
- **Impact to a player:** 2 (The regulars are passers-by and remark-givers, not talkers; their names and trades reach the player only indirectly.) · **belongs:** production/specs/hook-cast.json and the tier-2 cards; TOWN.md list · **lane:** town
- **Checked:** production/casting/regulars/REGULARS.md:84-117 - thirty sheets; REGULARS.md.approval.json beside it ; grep 'Kitching/Rinaldi/Cronin' in production/specs, content, ledger/TalkHelper, ue-probe/Source: no hit (an earlier case-insensitive 'tang' matched only inside other words) ; production/specs/hook-cast.json - the ids (zlata etc.) carry the old roles; no takeaway in any spec ; production/cast/cards - only lena, rocco, sam
- **Inferred:** DECISIONS.md:160 defers putting them in until the route works; see DEC-154.

### DEC-144 · BUILT · DECISIONS.md:150

- **Ruling:** Threats the words miss are read by the model beside the reply, at most 2 s (Jafar; built by Claude (town), 2026-09-30)
- **Checked:** ledger/TalkHelper/Program.cs:164-168 - ThreatByModel = true, ThreatWait = 2 s ; ledger/TalkHelper/Program.cs:952-975 - asked beside the reply, awaited at most ThreatWait, a found threat counts as one the words found ; ledger/Assets/Scripts/Core/ThreatRead.cs exists

### DEC-145 · BUILT · DECISIONS.md:151

- **Ruling:** Garments bound to the MetaHuman skeleton panel by panel; judged moving in Unreal (production/art/clothing/jacket-bound-test-2026-09-30, 2026-09-30)
- **Checked:** tools/meshgen/blender/bind_garment.py:23-36,64-65,97-151 - panels from the 'pattern' UV, sleeves to the arm, trunk keeps shoulder correctives ; production/specs/garments.json - RonJacketB 'made' by bind_garment.py, held as a method test

### DEC-146 · SUPERSEDED · DECISIONS.md:152

- **Ruling:** Ending signs: named states read by both the ending and its sign; code waits on scope (Claude (town), 2026-09-30)
- **Superseded by:** DECISIONS.md:158
- **Checked:** game-design/ending-signs-2026-09-30.md - the design (not built work) ; grep -i 'ending/signs' NOW.md TOWN.md ROADMAP.md: no list entry
- **Inferred:** The scope call it waited on came as DECISIONS.md:158 (wait until the route works). See DEC-152 for the gap that leaves.

### DEC-147 · BUILT · DECISIONS.md:153

- **Ruling:** Town's list after the audit; stops; key cap enforced in code at the day's dollar (Jafar, 2026-09-30)
- **Checked:** tools/talk_cost_sample.py:55 - LIVE_DAILY_USD = 1.00 ; tools/first_token_sample.py:30-33,162-174 - refuses when today's logged runs plus this run's worst case pass the day's dollar; logs to talk-runs.jsonl ; ledger/Assets/Scripts/Core/BudgetedClient.cs; ledger/TalkHelper/Program.cs:1420-1434 - per-run --budget-usd cap ; TOWN.md - current state and list only
- **Inferred:** The list's order was itself replaced by DECISIONS.md:168; its items were done first (DECISIONS.md:156-157).

### DEC-148 · PARTLY · DECISIONS.md:154

- **Ruling:** Builder's list replaced after the audit; rules: accent checker a screen, handover versions, NOW short (Jafar, 2026-09-30)
- **Missing:** The accent checker is still written as a gate in the voice tools (take_gate.py verdicts, page_voices.py leaving lines out); the rule says screen only, flagged beside the take, his ear decides.
- **Superseded by:** DECISIONS.md:174 (the list order only)
- **Impact to a player:** 1 (Tooling: decides which voice takes reach Jafar's ear, not what a player sees directly.) · **belongs:** tools/voice-live/take_gate.py, page_voices.py, speak_lines.py · **lane:** builder
- **Checked:** DECISIONS.md:174 and :212 - the list was replaced twice since; its remaining items are on NOW.md:21 (Shipping build in a fresh account), :26 (packaged tests), :27 (Mickey's office) ; CLAUDE.md - the rules (faces frozen, lighting through the game's camera, handover versions, NOW short, overview numbers from the real path, voices by ear) are written ; tools/voice-live/take_gate.py:5-13,124-139 - still marks REJECT/FAIL on the accent classifier 'before he hears it' ; tools/voice-live/page_voices.py:9-11 - lines failing the accent check are left out of the page; tools/voice-live/speak_lines.py:11-12 - 'checked ... before it can reach the page'
- **Inferred:** Whether a session still drops takes on the checker's verdict is behaviour, not visible in code; the tools as written still gate.

### DEC-149 · BUILT · DECISIONS.md:155

- **Ruling:** Free play's crime is Rita's pawn window; whole cast in gossip by own ids (builder, within canon, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:199 - RITA'S WINDOW; :2559 Fact player window_dN at ritas; :6108 GWeek.Deed at ritas ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:384 - the three by the cast's own ids in free play; :7271 the whole cast's memories ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:7910 - the errand to Rita's window

### DEC-150 · BUILT · DECISIONS.md:156

- **Ruling:** Facts chosen by code before writing kept; planned method stays off behind its switch (Claude (town), 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:77 ChooseFirst = true; :113 PlanFirst = false ; ledger/TalkHelper/Program.cs:1401-1402 - no PlanFirst set (stays off) ; production/research/grounded-replies/MEASURED-2026-09-30.md exists

### DEC-151 · BUILT · DECISIONS.md:157

- **Ruling:** Time-and-state sweep: ten Core faults fixed with rows for the port; three set aside (Claude (town), 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/TownSave.h:54-57,70 - the wait's lines shown travel in the town's one save ; ue-probe/Source/LedgerProbe/Public/PoliceFile.h:695 - Ellis asks only who is on the street at her visit's hour ; ue-probe/Source/LedgerProbe/Public/CoreGolden.h:4247 - the talk's ageing never runs back (row) ; FINDINGS.md - the three detective-crime faults set aside
- **Inferred:** Sampled three of the ten in the port; the rest not opened one by one.

### DEC-152 · NOWHERE · DECISIONS.md:158

- **Ruling:** Ending signs wait for the route; design on file; police investigating day with the week's end (Jafar, 2026-09-30)
- **Missing:** No list carries the ending's signs for after the route, and the police's investigating day did not go in with the week's end.
- **Impact to a player:** 3 (Over a week's play the ending shuts or opens with no readable sign; the investigating day matters only once a killing exists.) · **belongs:** TOWN.md list (states, signs, reading) and NOW.md (ActThree and police stages in the game) · **lane:** town
- **Checked:** game-design/ending-signs-2026-09-30.md:78-86 - police states (asking round, investigating, manhunt); a design, not built work ; ue-probe/Source/LedgerProbe/Public/WeeksEnd.h and ledger/Assets/Scripts/Core/WeeksEnd.cs: grep -i 'police/ellis/quiet' no hit - the week's end is in the game (CrimeProbe.cpp:4829-4836) without an investigating day ; grep -i 'manhunt/Investigating' in ue-probe/Source: no hit (only Core Homicide.cs) ; grep -i 'ending/signs/investigat' NOW.md TOWN.md ROADMAP.md: no list entry
- **Inferred:** The route is now in its cloud review (NOW.md:8); nothing records that the ending's signs come back after it.

### DEC-153 · LISTED · DECISIONS.md:159

- **Ruling:** Ron's 159 street lines stand; on in the game via OwnLines; five to Jafar for tone (Claude (town), under Jafar's delegation, 2026-09-30)
- **Missing:** The 109 ambient lines are never heard (StreetVoice::Ambient never called).
- **On a list:** NOW.md:14
- **Checked:** production/casting/ron-kirby/STREET-LINES.md and its approval beside it ; ue-probe/Source/LedgerProbe/Private/LedgerProbe.cpp:836-840 - OwnLines on ; ue-probe/Source/LedgerProbe/Public/OwnLines.h - Ron 109 ambient / 47 recognition / 3 faint ; grep 'StreetVoice::Ambient' in ue-probe/Source/LedgerProbe/Private: no hit ; …

### DEC-154 · NOWHERE · DECISIONS.md:160

- **Ruling:** Regulars stand as written; after the route: cast file names, talk cards, Grace's and Tangs' routines (Claude (town), under Jafar's delegation, 2026-09-30)
- **Missing:** Their names into the cast file, their talk cards replacing the old tier-2 ones, Grace's and the Tangs' routines, and the takeaway's bay and sign: none built and none on a list.
- **Impact to a player:** 2 (The street's passers-by keep old ages and trades; the caff and takeaway regulars are absent; seen only indirectly.) · **belongs:** TOWN.md (names, cards, routines) and NOW.md (bay, sign, faces) · **lane:** town
- **Checked:** production/casting/regulars/REGULARS.md and .approval.json - stand as written (the record part done) ; grep 'Kitching/Rinaldi/Cronin' in production/specs, content, ue-probe/Source, ledger/TalkHelper: no hit ; grep -i 'takeaway' production/specs/*.json: no hit; hook-cast.json:220 only names 'the cafe' as a place ; grep -i 'regular/Grace/Tang/tier-2' NOW.md TOWN.md ROADMAP.md FINDINGS.md FOR-JAFAR.md: no hit
- **Inferred:** The ruling defers the work to after the route works; the route is now in review (NOW.md:8), and no list keeps it.

### DEC-155 · SUPERSEDED · DECISIONS.md:161

- **Ruling:** Suits and coats from free MakeHuman CC0, refitted and bound panel by panel; no Fab, no MD (Jafar, 2026-09-30)
- **Superseded by:** DECISIONS.md:211; DECISIONS.md:216
- **Checked:** THIRD-PARTY.md:373-377 - MakeHuman Men's Suit 3, CC0 ; NOW.md:23 - suit jacket filmed in the game; CLOTHES.md item 1 - set aside after three reviews ; DECISIONS.md:211 - clothing a blocked capability, Epic's plainest garments meanwhile; DECISIONS.md:216 - Marvelous Designer joins for one proof, reopening 'no Marvelous Designer'

### DEC-156 · BUILT · DECISIONS.md:162

- **Ruling:** Four cloud method notes merged; they govern voices, mouths, packaged tests, Mickey's office (Jafar, 2026-09-30)
- **Checked:** production/research/voice-direction, metahuman-audio-driven-animation, packaged-game-testing, interior-blockout - present ; NOW.md:18,20,26,27 - the list items name those notes as their method
- **Inferred:** The voice-direction method (clip library per mood, direction per line) is not yet applied to any voice; it is named as item 2's method (NOW.md:20).

### DEC-157 · BUILT · DECISIONS.md:163

- **Ruling:** Narrowed second try stays off; prompting the writer set aside (Claude (town), 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:80 - NarrowRedraft = false ; ledger/TalkHelper/Program.cs:1401-1402 - not switched on

### DEC-158 · BUILT · DECISIONS.md:164

- **Ruling:** Epic's free Unreal-only animation content allowed in the game only; on the allowlist (Jafar, 2026-09-30)
- **Checked:** ledger-v2/research/license-allowlist.md:11 - entry 8, Animation (Epic, Unreal-only)

### DEC-159 · BUILT · DECISIONS.md:165

- **Ruling:** Voice in the game: ONNX conversion for release; Python stopgap in the game's folder for friends (Jafar, 2026-09-30)
- **Checked:** tools/voice-live/make_portable.py:1-26 - the portable voice folder ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3305-3326 - the game starts Voice/python/python.exe beside itself, needing nothing installed ; NOW.md:21 - item 3 uses the stopgap; DECISIONS.md:191 - his pick on the voice (1 Oct) after he heard the options
- **Inferred:** The release conversion is deferred by his 1 October pick and tracked in NOW.md's STATE line, not as a numbered item.

### DEC-160 · NOWHERE **R** · DECISIONS.md:166

- **Ruling:** Townspeople after the route: measure 0/5/10/20, fix walkers' feet, one approved sample first (Jafar, 2026-09-30)
- **Missing:** The crowd measurement at 0, 5, 10 and 20 people in the packaged game, the walkers' speed matched to the clip, and the one-sample-before-twenty step: none built; only natural walking is listed (V6).
- **Impact to a player:** 3 (Walkers sliding is visible when people walk; frame cost of a crowd is unmeasured before the friends' build.) · **belongs:** ue-probe/Source/LedgerProbe/Private/PersonAnim.cpp (speed match); NOW.md builder's list (measurement) · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/PersonAnim.cpp:344,507-513 - walkers still move at WalkSpeedCms (1.2 m/s default per research DELIVERY.md:5) times the blend weight, not the clip's own speed ; grep -i 'townspeople/walkers/1.2 m/0, 5, 10/twenty people' NOW.md TOWN.md ROADMAP.md FINDINGS.md FOR-JAFAR.md: no hit ; NOW.md:16 - V6 'People idle and walk naturally from Epic's free animation sample (production/research/natural-idles)'
- **Inferred:** V6 may absorb the walk/feet fix but names a different research note and does not include the 0/5/10/20 measurement or the one-sample approval.
- **Reviewer:** PersonAnim.cpp:344 walkers advance at a fixed WalkSpeedCms whatever the clip's feet do

### DEC-161 · BUILT · DECISIONS.md:167

- **Ruling:** Second three cloud notes merged and assigned to town and builder (Jafar, 2026-09-30)
- **Checked:** production/research/grounded-dialogue-selection, townspeople-animation, voice-in-the-game - present ; DECISIONS.md:168 - the town's list ordered by grounded-dialogue-selection

### DEC-162 · BUILT · DECISIONS.md:168

- **Ruling:** Town's list from the research: empty answers by cause, plain line, tuned check, rule table, measured (Jafar, 2026-09-30)
- **Checked:** production/research/grounded-replies/CAUSES-2026-09-30.md, PLAIN-AND-CHECK-2026-09-30.md, RULES-2026-09-30.md ; ledger/Assets/Scripts/Core/TalkRules.cs - the first-week rule table ; ledger/TalkHelper/Program.cs:1401-1402 - UseRules and PlainFallback on ; DECISIONS.md:171 - the plain wording's sample answered on his page

### DEC-163 · SUPERSEDED · DECISIONS.md:169

- **Ruling:** Plain line stays off; the check stays as it is after three tuning tries (Claude (town), 2026-09-30)
- **Superseded by:** DECISIONS.md:172
- **Checked:** ledger/TalkHelper/Program.cs:1402 - PlainFallback = true (now on) ; DECISIONS.md:172 - the rule table and the plain line switched on
- **Inferred:** The 'check stays as it is' half still holds (no tuned checker in the code).

### DEC-164 · BUILT · DECISIONS.md:170

- **Ruling:** Ron's tone right; others may follow his pattern; the street's missing knowledge into the rule table (Jafar, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/OwnLines.h - own lines for sam, emil, june beside rocco ; DECISIONS.md:190,199 - Sheila, Alison and Ada keep the shared lines; Darren, Father Walsh and June own lines in (his yes) ; ledger/Assets/Scripts/Core/StreetFacts.cs and TalkRules.cs - written facts and rules for the newcomer's questions

### DEC-165 · BUILT · DECISIONS.md:171

- **Ruling:** 'What was Mickey like?': only his two lines, for those who knew him, then 'that's as much...' (Jafar, 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/StreetFacts.cs:76-80 - mickey_counsel and mickey_kept_ron ; ledger/Assets/Scripts/Core/StreetFacts.cs:140-144 - never june or noor (Alison, production/specs/hook-cast.json:990-992) ; ledger/Assets/Scripts/Core/TalkRules.cs:60,87 - mickey_like rule, Partial, those two facts ; ledger/Assets/Scripts/Core/ConversationEngine.cs:705 - 'That's as much as I can tell you.'

### DEC-166 · BUILT · DECISIONS.md:172

- **Ruling:** First-week rule table and plain line on in the talk program (Claude (town), by Jafar's rule, 2026-09-30)
- **Checked:** ledger/TalkHelper/Program.cs:1395-1402 - UseRules = true, PlainFallback = true

### DEC-167 · BUILT **R** · DECISIONS.md:173

- **Ruling:** One measuring run: 30 real lines in the finished game, capped at $0.50 in code (Jafar, 2026-09-30)
- **Checked:** tools/ai-tester/play.py:29-34,82,426-428,682 - REAL_TALK_BUDGET_USD 0.50 set for the game's talk program ; ledger/TalkHelper/Program.cs:1420-1434 - BudgetedClient enforces it ; production/playtest/real-talk-2026-09-30.md - run done, $0.2324 spent
- **Reviewer:** TalkHelper/Program.cs:273 sets the claim checker only when the client is an AnthropicClient; :1424-1432 wraps it in BudgetedClient whenever a budget is set; tools/ai-tester/play.py:426-428 sets the budget for real talk: so the capped measuring run had no claim check (read, not run)

### DEC-168 · LISTED · DECISIONS.md:174

- **Ruling:** Builder's list replaced: measuring run, delay, friends' build, mouths, nightly tests, office, jacket film (Jafar, 2026-09-30)
- **Missing:** The delay, the friends' build, audio-driven mouths for prepared lines, nightly packaged tests and Mickey's office are not done.
- **On a list:** NOW.md:20; NOW.md:21; NOW.md:18; NOW.md:26; NOW.md:27
- **Checked:** NOW.md:7 - measuring run done; NOW.md:23 - jacket filmed, done ; NOW.md:20 - item 2, the delay, open; NOW.md:21 - item 3, the friends' build, open; NOW.md:18 - V8 prepared-line mouths, open ; NOW.md:26 - item 5 nightly tests and NOW.md:27 - item 6 Mickey's office, 'kept for later' ; DECISIONS.md:212 - the order since replaced (review faults, interface, visual bar)

### DEC-169 · BUILT · DECISIONS.md:175

- **Ruling:** A witness's story only as sure as the witness: a noise or shape is suspicion, never 'he did it'. (Jafar, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/Gossip.h:234-239 - Rumor::NamesHim(): only rung 4 (recognised) or no rung names him ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:1872-1877 - WhatWitnessFiles: rung 0 files the noise only, never a story about him ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2525-2546 - a hearing-only witness files 'I heard glass go over at Rita's. I never saw who did it.' ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:613 - remarks about him skip rumours that do not name him ; …

### DEC-170 · LISTED · DECISIONS.md:176

- **Ruling:** The route is not done: the 30 Sept review's faults first, split builder/town; review merged only with running proofs. (Jafar, 2026-09-30)
- **Missing:** Leftovers of the 30 September faults (B3's night away, C3, C5(b)-(h), A13a, the C++ cast reader's hours check) are not fixed
- **On a list:** NOW.md:8 (1b: '...the Low items, the walk'); NOW.md:51 (town: 'B3 and L4')
- **Checked:** NOW.md:45 - the split is recorded under Handovers as ruled ; git log: 473082c 'Review of 30 September: the High faults run and proved, with the proofs and their output'; production/audits/review-2026-09-30/probes exists ; production/audits/review-2026-10-01/SUMMARY.md:13-35 - most of the 30 September faults fixed and proved; not fully fixed: N1 evidence key, M2 Ellis line, B3 the landing's hours (Low), small save items (Low) ; production/audits/review-2026-10-01/FAULTS.md:44 A13a not fixed; :53 B3 partly; :71 C5 mostly not fixed; :87 the C++ cast reader never checks hours ; …
- **Inferred:** The 30 September leftovers (A13a, B3, C3, C5, the cast reader's hours) are covered by 1b's 'the Low items', since the 1 October review lists them; not named one by one on the list

### DEC-171 · BUILT · DECISIONS.md:177

- **Ruling:** Ada's tea judged as she'd tell it: up to 30 min late and staying counts as staying (+0.25), remembered as late. (Claude (the town), under Jafar's list of 30 September, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/FirstWeek.h:53-57 - ArriveBy 21:30, StayUntil 22:30, LongestAway 10, LateArriveBy 22:00, StayedGain 0.25, LeftEarlyGain 0.05 ; ue-probe/Source/LedgerProbe/Public/FirstWeek.h:207-231 - How {OnTime, Late, CameNearEleven, SlippedOut, LeftEarly}; Late maps to Stayed ; ue-probe/Source/LedgerProbe/Public/FirstWeek.h:111-122 - 'came late for his tea, but he sat with me till gone half ten' memory ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6230, 6693 - the game feeds his minutes with Ada into the tea ; …
- **Inferred:** The 1 October review's L6 (a short late visit counts more than a long early one) is a consequence of this ruling, flagged 'needs his eye' in FAULTS.md:153, not on Needs you

### DEC-172 · BUILT · DECISIONS.md:178

- **Ruling:** Free-play witnesses are whoever's day puts them on Quay Street then, from where they stand, in that hour's light; strangers until met. (builder, within canon, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:1771-1789 - NightAt 19:00-07:00, LightOnHim from daylight and lamp reach ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:1843-1866 - OnlookersAt: on Quay Street by CastDay, bodies placed at their place's pavement (BodySpotFor), the bodyless only from an indoor place (line 1859) ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:1674-1678 - FamiliarityFromMeetings: 0 unmet, 0.4 once met, +0.1 a day, cap 0.7 ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:218-222 - CanNameHim only at rung 4 ; …
- **Inferred:** L2 (Sheila can ask at the fish market) and L7 are Low leftovers covered by NOW.md:8's 'the Low items'

### DEC-173 · BUILT · DECISIONS.md:179

- **Ruling:** Michelle, the night silhouette, never appears in play; page frames keep it. (builder, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:790 - GFigureBarredInPlay ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:6611-6617 - DriveFigure hides the figure when barred in play ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:8640-8644 - ApplyPlayCondition sets the bar for every play condition
- **Inferred:** The page-frame path does not go through ApplyPlayCondition, so frames keep the figure

### DEC-174 · BUILT · DECISIONS.md:180

- **Ruling:** Witness lines lose details wrong in play: no fixed time, no lamp by day, no 'before he ran', no 'served him'. (builder, within canon, 2026-09-30)
- **Checked:** content/dialogue/crime-witness-v1.json - grep 'half nine/streetlight/lamp/before he ran/served him': no hit ; grep 'about half nine/served him in the shop' in content, ue-probe/Source, Core, TalkHelper, specs: only test fixtures and comments (CrimeProbe.h:1027-2488) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:213-214 - the game reads crime-witness-v1.json ; content/dialogue/crime-witness-v1.json:24-25 - overheard r1 lines still say 'a wet night' / 'on a night like this'; used only in the scripted encounter's Round2 (CrimeProbe.cpp:8518-8536)
- **Inferred:** The night wording in the overheard bank is not reached in free play, so not a live fault

### DEC-175 · BUILT · DECISIONS.md:181

- **Ruling:** No talk through a wall: talk only in range and same area or both on the pavement; Marta out on Rita's step 11-12. (town, landed by the builder, 2026-09-30)
- **Checked:** ue-probe/Source/LedgerProbe/Public/CastDay.h:308-324 - Together(): range, then same area or both outside; IsInside from the cast file ; production/specs/hook-cast.json:8,20,32,62,74 - mickeys_office, fish_counter, ritas_counter, laundry_counter, cafe marked 'inside': true ; production/specs/hook-cast.json:2027, 2042 - Marta [11, 'ritas_step'], [12, 'ritas_counter'] ; ue-probe/Source/LedgerProbe/Public/TownRounds.h:77,149 and Gossip.h:715 - the rounds use Together

### DEC-176 · BUILT · DECISIONS.md:182

- **Ruling:** The reaction opener stays off; the plain rule's reaction words stay. (Claude (the town), within his rulings, 2026-09-30)
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:97-102 - ReactFirst = false ; grep 'ReactFirst' in ledger/TalkHelper and ledger/Relay: no hit (never switched on) ; ledger/Assets/Scripts/Core/PlainWords.cs:30-37 - reaction words and 'hang on'/'of course' phrases in the plain list

### DEC-177 · BUILT · DECISIONS.md:183

- **Ruling:** Ron stays on Chatterbox Nano; Sopro off for Ron and not offered for Sheila. (Jafar, 2026-09-30)
- **Checked:** production/specs/voice-engines.json:3 - 'engines': {} (everyone on Nano; Sopro only by entry here) ; grep 'sopro' in ue-probe/Source: no hit; only tools/voice-live bench and worker scripts
- **Inferred:** The 'faster way that keeps the game's voice' is item 2 on NOW.md:20

### DEC-178 · PARTLY **R** · DECISIONS.md:184

- **Ruling:** Hair settled by his picks: Darren's S6 (Epic short cut), Sheila's S4 with its hair; no Blender curls. (Claude, under his picks, 2026-10-01)
- **Missing:** Darren's S6 head is not in the game (C5 still worn), its approval is not recorded, and no list item puts it in
- **Impact to a player:** 4 (Darren is one of the three principals; his face and hair in ordinary play are not the ruled ones) · **belongs:** production/specs/in-game.json and CrimeProbe.cpp:917 (Approved take); an item on NOW.md · **lane:** builder
- **Checked:** production/specs/in-game.json:6-20 - Sheila in the game as MH_LenaS4 (BUILT) ; production/specs/in-game.json:46-60 - Darren in the game is still MH_SamC5, not S6 ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:917 - Darren's approved take hard-coded 'C5' ; tools/ue/make_cast_metahumans.py:542-551 - S6 (S4 face + WI_Hair_S_Casual) exists as a buildable take ; …
- **Inferred:** The S6 pick may sit in the page's store but is not recorded in the repo, so the approval file the build checks cannot exist
- **Reviewer:** CrimeProbe.cpp:917 hard-codes Darren's approved take as 'C5'

### DEC-179 · BUILT · DECISIONS.md:185

- **Ruling:** Voice speed work set aside past two tries; in-sentence streaming off by default; compiled step kept on F:. (Claude; the next step his, 2026-10-01)
- **Checked:** tools/voice-live/voice-server.py:296-302 - streaming only when LEDGER_VOICE_STREAM=1 ; production/large-files.json:1481-1483 - F:/LedgerTools/voice-graphs/nano/nano-step.onnx kept 'as the first piece of the voice's conversion into the game' ; FINDINGS.md:49 - set aside, his scope question (answered by DEC-185)

### DEC-180 · LISTED **R** · DECISIONS.md:186

- **Ruling:** A neighbour who sees him break a window reports, unless won over (tea, friend) or talked round (quiet, threat). (Jafar (his page of 1 October, police-witness), 2026-10-01)
- **Missing:** A threat does not talk a witness out of reporting (N3), in Core or port
- **On a list:** NOW.md:8 (1b: 'N3 a threat stops a witness reporting him (his ruling; town Core, my port)'); NOW.md:51
- **Checked:** ue-probe/Source/LedgerProbe/Public/PoliceFile.h:401-424 - WouldReport: reports unless Loyalty > OnHisSide (0.575) or the deed is Suppressed ; ue-probe/Source/LedgerProbe/Public/TownWeek.h:131 - the game's week calls WouldReport ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:1990-2000 - KeepQuiet puts the deed in Suppressed (keeps it quiet: built) ; ledger/Assets/Scripts/Core/ConversationEngine.cs:184-186 - 'a threat never buys silence this week (carried until Jafar rules)': the threat half is not built on main ; …
- **Inferred:** FOR-JAFAR.md's Town summary (2 October) says 'a threat silences a witness' is done; no such change is on main, so it is at best on the unpushed town branch
- **Reviewer:** FOR-JAFAR.md 'Town, 2 October' calls these done 'each test first'; not on main (the last Core commit is a0a0891, 20:01) nor on GitHub's town branch (last pushed 28 September)

### DEC-181 · BUILT · DECISIONS.md:187

- **Ruling:** Sheila tried on the faster model: twenty blind paired replies; she moves only if she still sounds like herself. (Jafar (his page of 1 October, sheila-model), 2026-10-01)
- **Checked:** production/playtest/first-token-2026-10-01.md:44-63 - the blind check of twenty pairs, preferred 13 to 6, with its key and scores files

### DEC-182 · BUILT · DECISIONS.md:188

- **Ruling:** Street lines get one more try, a new way: lines where each person's day puts them, one review; fail keeps shared lines. (Jafar (his page of 1 October, street-lines), 2026-10-01)
- **Checked:** production/research/ambient-lines/own-lines-2026-10-01.md exists on main ; TOWN.md:42-53 - the fourth try run and reviewed once; three passed, three failed ; ue-probe/Source/LedgerProbe/Public/OwnLines.h - banks for sam, emil, june (and rocco); none for lena, alison, ada

### DEC-183 · BUILT · DECISIONS.md:189

- **Ruling:** Sheila stays on her model (Sonnet 5) after the blind check. (Claude (the town), under his tap (sheila-model: try), 2026-10-01)
- **Checked:** production/cast/cards/lena.md:3 - tier: core; rocco.md:3 and sam.md:3 - tier: ambient ; ledger/Assets/Scripts/Core/ConversationEngine.cs:281 - core tier takes Models.Core ; ledger/Assets/Scripts/Core/LlmClient.cs:55-56 - Core = claude-sonnet-5, Ambient = claude-haiku-4-5 ; ledger/TalkHelper/Program.cs:267-268 - the talk program builds each engine with no model override

### DEC-184 · BUILT · DECISIONS.md:190

- **Ruling:** Sheila, Alison and Ada keep the shared street lines for good; the three that passed wait on his yes. (Claude (the town), under his tap (street-lines: try), 2026-10-01)
- **Superseded by:** DECISIONS.md:199 (DEC-193, his yes) replaces the 'wait on his yes' part
- **Checked:** ue-probe/Source/LedgerProbe/Public/OwnLines.h - grep of bank headers: rocco 40, sam 16, emil 8, june 4; no lena, alison or ada banks ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1259-1266 - Own() falls back to the shared bank for anyone without own lines

### DEC-185 · LISTED · DECISIONS.md:191

- **Ruling:** Voice: this week's other items first, then move the voice into the game, only with evidence it shortens the delay. (Jafar, 2026-10-01)
- **Missing:** The voice is not moved into the game; no evidence step has run yet
- **On a list:** NOW.md:20
- **Checked:** NOW.md:20 - item 2, the delay, alongside, open ; NOW.md:29 and FOR-JAFAR.md:23 - the condition (evidence it shortens the delay before the two weeks start) recorded ; production/large-files.json:1481-1483 - the compiled Nano step kept for the move

### DEC-186 · SUPERSEDED · DECISIONS.md:192

- **Ruling:** Every line plays the loudness mouth; MetaHuman Animator faces only with -MadeFace. (Jafar, 2026-10-01)
- **On a list:** NOW.md:18
- **Superseded by:** DECISIONS.md:201
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3888-3889 - made faces play only with -MadeFace or -FaceAB ; DECISIONS.md:201 (DEC-195) - prepared lines get Epic's audio-driven mouths, reversing the loudness pick ; NOW.md:18 - V8 open; NOW.md:22 item 4 marked REOPENED as V8
- **Inferred:** Live (generated) lines can only have the loudness mouth, so that part stands

### DEC-187 · BUILT · DECISIONS.md:193

- **Ruling:** Approval pages show every picture full-screen on the page (zoom, swipe, films with sound), one viewer in every page tool. (Jafar, 2026-10-01)
- **Checked:** tools/page_pictures.py:1-22 - the viewer: full resolution, pinch, swipe, Esc, films with sound ; tools/approval_page.py:388, candidate_page.py:298, day_page.py:259, ingame_page.py:277, town_day_page.py:440,483, town_page.py:224, weekend_page.py:248 - each applies page_pictures.apply ; production/approvals/2026-10-01/index.html and 2026-10-01-town-4/index.html - carry the viewer's marker ; tools/cleanup.py - no page_pictures (its page has no pictures)

### DEC-188 · BUILT · DECISIONS.md:194

- **Ruling:** A witness is on his side only above 0.575 regard; one nudge does not win them; Watched reads the same line. (Claude (the town), under his ruling of 1 October, 2026-10-01)
- **Checked:** ue-probe/Source/LedgerProbe/Public/PoliceFile.h:401, 421-423 - OnHisSide = 0.575 in the port's WouldReport ; ledger/Assets/Scripts/Core/PoliceFile.cs:224, 244-246 - the same in the Core ; ledger/Assets/Scripts/Core/Homicide.cs:561-562 - Watched.WouldTalkToPolice reads PoliceFile.OnHisSide (Core only; killings are not in the game) ; ue-probe/Source/LedgerProbe/Public/TownWeek.h:131 - the game calls WouldReport

### DEC-189 · BUILT · DECISIONS.md:195

- **Ruling:** Mickey's back room merged with the rear lobby, 3.45 m deep, WC closet and kettle shelf. (Claude (builder), within the brief, 2026-10-01)
- **Checked:** production/specs/mickeys-office.json:26-27 - staff-side wall at z 9.4-9.55; :35-37 back wall at z 13.0 (3.45 m) ; production/specs/mickeys-office.json:32-34 - WC a closet in the back room's corner; the kettle on its shelf ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4039-4041 - the game reads mickeys-office.json
- **Inferred:** The blockout itself runs only under -MickeysInside; item 6 is kept for later (NOW.md:27)

### DEC-190 · LISTED · DECISIONS.md:196

- **Ruling:** No to all four of Wednesday's looks (street day/night, mouths, boots/handbag); the page's yes was wrong. (Jafar, by message, 2026-10-01)
- **Missing:** The named faults are not yet fixed in the game
- **On a list:** NOW.md:10-19 (V, V1-V9)
- **Checked:** NOW.md:11-19 - V1 shop windows, V2 cars/phone box/skip/pallets, V3 hillside, V4 dressing, V5 night pools, V6 idles, V7 Sheila's mouth, V8 mouths, V9 clothes: each of his named faults has an open item ; NOW.md:11 - V1 in progress (pawnbroker only); V2-V6, V8, V9 not started

### DEC-191 · BUILT · DECISIONS.md:197

- **Ruling:** The gate judges every visual against the Hook sheet and KCD2 frames; yes only for 2026-game quality. (Jafar, 2026-10-01)
- **Checked:** CLAUDE.md:81 - the rule, as ruled ; production/reference/hook-sheet.png, kcd2-town-arcades.jpg, kcd2-town-fountain.jpg - exist ; NOW.md:11 - V1's review names its shortfalls against the 2026 bar; production/art/clothing/.../ready-pieces-against-the-bar-2026-10-01.md cited at NOW.md:56
- **Inferred:** No page tool forces 'shortfalls first, no yes'; tools/day_page.py etc. carry no bar check, so it rests on the sessions' conduct

### DEC-192 · LISTED · DECISIONS.md:198

- **Ruling:** Before the friends' build: shop interiors, Epic idles, Sheila's mouth fix, plain 1990 clothes; after it cars, hill, night, dressing. (Jafar, 2026-10-01)
- **Missing:** Idles, plain clothes and the rest of V1/V7 not in the game
- **On a list:** NOW.md:11, 16, 17, 19
- **Checked:** NOW.md:11 V1 in progress; NOW.md:16 V6 open; NOW.md:17 V7 in progress (fix A filmed); NOW.md:19 V9 open ; production/research/shop-window-interiors, natural-idles, talking-face-faults, plain-1990-clothes - each has a NOTE.md (method researched)
- **Inferred:** The 'after it' order is replaced by DEC-195 (everything before the friends' build) and DEC-206's order

### DEC-193 · PARTLY · DECISIONS.md:199

- **Ruling:** Darren's, Father Walsh's and June's own street lines (58) go into the game. (Jafar (the town's page of 1 October, own-lines-three: yes, 12:41), 2026-10-01)
- **Missing:** Father Walsh's and June's lines are unreachable: neither exists as a speaker in play
- **Impact to a player:** 2 (Only Darren's share is heard; the rest waits on townspeople who walk, so a player never notices the gap) · **belongs:** CrimeProbe.cpp remark loop (5730) once townspeople have bodies; NOW.md V4 · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/OwnLines.h - banks for sam (16), emil (8), june (4) ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1259-1266, 1278, 1784, 2106 - Own() puts a named person's lines first ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5730-5737 - street remarks are made only by lena, sam and rocco ; grep '"emil"/"june"' in ue-probe/Source/LedgerProbe Private and CrimeProbe.h: no hit; production/specs/street-people.json: no emil/june
- **Inferred:** Darren's lines are heard; Father Walsh and June have no body or voice in play, so their lines are in the build but never spoken

### DEC-194 · LISTED · DECISIONS.md:200

- **Ruling:** The friends' test runs on Jafar's PC from a shortcut in a fresh Windows account; no relay, no sent copies. (Jafar, 2026-10-01)
- **Missing:** The friends' build is not made
- **On a list:** NOW.md:21
- **Checked:** NOW.md:21 - item 3, open, with this scope ; NOW.md:29 - 'waits on his fresh Windows account and room on F:'

### DEC-195 · LISTED · DECISIONS.md:201

- **Ruling:** Higher bar for the friends' build: no placeholder anywhere (V1-V9) and the interface built as designed, never debug text. (Jafar, 2026-10-01)
- **Missing:** Most of V1-V9 and the rest of the interface are not built
- **On a list:** NOW.md:9-19
- **Checked:** NOW.md:9 - UI in progress; NOW.md:10-19 - V1-V9 open ; ue-probe/Source/LedgerProbe/Private/LedgerProbe.cpp:502 - the only AddOnScreenDebugMessage, in the probe shot path (not play)

### DEC-196 · SUPERSEDED · DECISIONS.md:202

- **Ruling:** Builder's order: cloud review, visual bar, voice alongside, interface once approved, friends' build. (Jafar, 2026-10-01)
- **Superseded by:** DECISIONS.md:212
- **Checked:** DECISIONS.md:205 (DEC-199) - interface moved before the visual bar ; DECISIONS.md:212 (DEC-206) - the review's two High faults, interface, visual bar, friends' build ; NOW.md:5 - the list's order follows the later ruling

### DEC-197 · BUILT · DECISIONS.md:203

- **Ruling:** Shop rooms and displays from Poly Haven CC0 by script; room picture with depth; real display; reflective glass; night spill light. (Builder, 2026-10-01)
- **Checked:** tools/art-recipes/fetch_polyhaven.py:1-50 - CC0 fetch lists; 'No weapons, no drink, no toys' ; production/specs/shop-interiors.json - pawnbroker room, display glb, lit_at_night, spill_lumens 350 (a tube-white rect light in the window head) ; ue-probe/Config/DefaultEngine.ini:74 - r.Lumen.TranslucencyReflections.FrontLayer.EnableForProject=True ; tools/ue/make_glass_material.py:107-117 - Thin Translucent glass keeps the reflection whole (replaces the Fresnel-opacity try) ; …
- **Inferred:** The Fresnel method gave way to Thin Translucent after two tries; the ruling's outcome (glass that mirrors the street) is what is built ; Only the pawnbroker exists, by the multiply-after-one-sample rule

### DEC-198 · BUILT · DECISIONS.md:204

- **Ruling:** The pawnbroker's window is lit at night, its room seen lit. (Builder, 2026-10-01)
- **Checked:** production/specs/shop-interiors.json - pawnbroker lit_at_night: true, brightness_night 0.7, spill 350 lm ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:7116, 7138 - read by the game

### DEC-199 · LISTED · DECISIONS.md:205

- **Ruling:** The interface is the evening paper, built as drawn, before the visual bar. (Jafar, 2026-10-01)
- **Missing:** The interface's sounds, round buttons and review are not done
- **On a list:** NOW.md:9
- **Superseded by:** DECISIONS.md:212 replaces its order (High faults first)
- **Checked:** production/design/ui/README.md:11, 27 - the evening paper chosen and drawn ; NOW.md:9 - UI in progress: title, loading, settings, pause, subtitles, coupon, prompt built; 'Left: suggested lines ..., the controller's round buttons, the sounds' ; FOR-JAFAR.md:30 - 'Left: the sounds, and an independent review'

### DEC-200 · LISTED · DECISIONS.md:206

- **Ruling:** Suggested lines are 'Mixed': written lines for hellos, goodbyes, decisions; the small model for the rest, given only what Tom knows. (Jafar, 2026-10-01)
- **Missing:** Not shown to players until his yes and the spec's status flipped
- **On a list:** FOR-JAFAR.md:16 (Needs you 3); TOWN.md:85
- **Checked:** ledger/Assets/Scripts/Core/Suggest.cs:10-25 - three jobs, the small model given only Tom's knowledge, written lines as fallback ; ledger/TalkHelper/Program.cs:215-260, 490-492 - the talk program answers {kind: suggest} ; production/specs/suggested-lines.json:2 - status 'in review ... not for play until his yes' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5184-5202 - the panel stays dark while the file says 'in review' ; …

### DEC-201 · BUILT · DECISIONS.md:207

- **Ruling:** Suggested lines appear at once with a controller, on a keyboard only on Tab. (Jafar, 2026-10-01)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5402 - bOpen = passed && (Always // talk by pad) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5336-5341 - Tab (SuggestTakeKeys) opens them on a keyboard
- **Inferred:** Dark in play until DEC-209's condition is met (his yes on the written lines)

### DEC-202 · NOWHERE · DECISIONS.md:208

- **Ruling:** A microphone for talking is looked at again once the playable route works. (Jafar, 2026-10-01)
- **Missing:** The deferral is on no list, so nothing will bring it back when the route works
- **Impact to a player:** 1 (A deferred review; invisible to players, but it can be forgotten) · **belongs:** NOW.md 'kept for later' or ROADMAP.md · **lane:** builder
- **Checked:** grep -i 'microphone/speech input/voice input' in NOW.md, TOWN.md, ROADMAP.md, CLOTHES.md, FOR-JAFAR.md, FINDINGS.md: no hit ; production/design/ui/README.md:50 - recorded only in the design's README

### DEC-203 · BUILT · DECISIONS.md:209

- **Ruling:** Pause page keeps 'The Ledger' greyed with its reason; 'Quit to the title' restarts the game from its command line. (Builder, 2026-10-01)
- **Checked:** ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:72 - 'The Ledger' unavailable, 'Tom's notebook is not in this build yet.' ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:82, 149 - Quit to the title with its confirmation ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:8153-8161 - CreateProc with the original command line, then exit

### DEC-204 · LISTED **R** · DECISIONS.md:210

- **Ruling:** Mickey's people never go to the police about him; Ron and Sheila handle it privately; Sheila's trust counts. (Jafar, 2026-10-01)
- **Missing:** Nothing built: Ron and Sheila still report him like anyone else; no private handling
- **On a list:** NOW.md:8 (N4); NOW.md:51
- **Checked:** production/specs/hook-cast.json:295-296, 360-361 - rocco and lena have keepsQuiet 'owner' but no 'police': 'never' ; ledger/Assets/Scripts/Core/PlayerIdentity.cs:153 - MickeysOwn {lena, rocco, sam} used only for knowing his name (TalkHelper Program.cs:711) ; grep -i 'favour owed/one of their own/handle it privately' in Core, port, TalkHelper: no hit ; NOW.md:8 - N4 listed as left (town Core and story, builder's port and wiring)
- **Inferred:** FOR-JAFAR.md's Town summary (2 October) says 'Ron and Sheila never go to the police and keep it to themselves' is done; nothing of it is on main
- **Reviewer:** FOR-JAFAR.md 'Town, 2 October' calls these done 'each test first'; not on main (the last Core commit is a0a0891, 20:01) nor on GitHub's town branch (last pushed 28 September)

### DEC-205 · LISTED · DECISIONS.md:211

- **Ruling:** Clothing is a blocked capability: wardrobe research; meanwhile Epic's plainest garments re-coloured plus pieces that passed. (Jafar, 2026-10-01)
- **Missing:** Epic's plainest re-coloured garments and the passed pieces are not on the cast in the game
- **On a list:** NOW.md:19 (V9); NOW.md:54, 56
- **Checked:** FOR-JAFAR.md:15 - Needs you 2, clothing BLOCKED, as ruled ; CLAUDE.md:59 - 'A SET-ASIDE NEVER SIMPLY STOPS' rule ; production/research/wardrobe-at-scale/SUMMARY.md and notes 1-5 - merged ; production/specs/garments.json - worn: RonBoots, SheilaHandbag; held: spectacles, chain, Darren's belt and pager; skirt and tights absent ; …

### DEC-206 · BUILT · DECISIONS.md:212

- **Ruling:** Builder's order: the 1 Oct review's two High faults, then the interface, then the visual bar with voice alongside, then the friends' build. (Jafar, 2026-10-01)
- **Checked:** NOW.md:5 - ORDER line records it ; git log: a0a0891 (20:01, High fault fixed), then 3e693da (20:39) and 318d9dc (21:21) interface work - the order followed
- **Inferred:** NOW.md:5 adds 'then its Medium and Low' before the interface, which the ruling does not say; the builder followed the ruling, not that line

### DEC-207 · BUILT · DECISIONS.md:213

- **Ruling:** The AI notice is a card before the first conversation; Enter/A on, typing goes on, Esc leaves; F1 shows it 16 s at the top. (builder, within his interface ruling, 2026-10-01)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3024-3036 - SNoticeCard: Enter/A go on, Esc/B leave, a typed character goes on with that letter ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3041-3123 - card centred (VAlign_Center), slip at the top for 16 s ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:7035 - the card before the first talk ; ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:300 - F1 bound to RequestNotice

### DEC-208 · BUILT · DECISIONS.md:214

- **Ruling:** On a controller 'My own words...' (Y) returns to the coupon; Steam's keyboard only once under Steam. (builder, within the design, 2026-10-01)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5306-5311 - 'My own words...' row back to the coupon ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp: SSuggestKeys OnKeyDown - Gamepad_FaceButton_Top gives the keys back ; grep 'ShowFloatingGamepadTextInput/SteamUtils' in CrimeProbe.cpp: no hit (as ruled)

### DEC-209 · BUILT · DECISIONS.md:215

- **Ruling:** Keyboard asks for suggestions only on Tab (or 'Always'); controller when the coupon opens; nothing while the spec says 'in review'. (builder, within his rulings, 2026-10-01)
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5184-5202 - bSuggestPassed from the spec's status ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5238-5240 - AskSuggest refuses unless passed ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5336-5341, 5402-5407 - asked on Tab, on opening with a pad, or with SuggestAlways

### DEC-210 · LISTED · DECISIONS.md:216

- **Ruling:** Marvelous Designer joins the clothing lane for one tailored-jacket proof; the paid month bought only if it passes. (Jafar, 2026-10-01)
- **Missing:** No jacket made in Marvelous yet; the construction body is not exported
- **On a list:** CLOTHES.md:13; NOW.md:53
- **Checked:** CLOTHES.md:13 - item 0, the Marvelous proof, open; Jaeger drafted, construction body asked ; NOW.md:53 - the clothing session's request for Epic's construction body, not yet done by the builder ; CLOTHES.md:3 - header still says 'made in Blender only ... nothing bought (Jafar, 30 September: not Marvelous Designer)'

### DEC-211 · PARTLY · DECISIONS.md:217

- **Ruling:** Marvelous garments are ours; the trial is evaluation only, so what ships is made or re-exported under the paid month. (Jafar, 2026-10-01)
- **Missing:** The two constraints (re-export under the paid month; cancel or pay by 15 October) are tracked nowhere but DECISIONS
- **Impact to a player:** 2 (A licence and money exposure only if a trial-made jacket ships or the trial renews unnoticed; players never see it) · **belongs:** CLOTHES.md item 0 (re-export step) and FOR-JAFAR.md Needs you (the 15 October renewal) · **lane:** clothing
- **Checked:** DECISIONS.md:217 - the ruling and the terms read ; CLOTHES.md:13 - 'free trial (ends 15 October)'; 'Pass: he buys the month and I make the ten ... in it' ; grep -i 'marvelous' in ledger-v2/research/license-allowlist.md, THIRD-PARTY.md, FOR-JAFAR.md, ROADMAP.md: no hit ; No list line for re-exporting the proof jacket under the paid month, or for cancelling the trial before it turns paid on 15 October
- **Inferred:** The proof jacket, if it passes, could reach the game as made under the trial

## The archive (production/archive/DECISIONS-to-2026-09-24.md), which CLAUDE.md says still binds

### ARC-001 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:31

- **Ruling:** Unreal is the engine; Unity archived not deleted; C# Core stays source of truth; five Core suites keep running.
- **Checked:** ue-probe/LedgerProbe.uproject and ue-probe/Source/LedgerProbe/* - the Unreal game exists and is what the player runs ; tools/ci-checks.sh:179-184 - core-tests, soak, save-chaos, perception-golden (port-golden-check.sh), stranger-test in the real table ; .github/workflows/ledger-core-tests.yml:4,66 - on push, runs bash tools/ci-checks.sh ; tools/ci-checks.sh:98-104 - port-golden-check regenerates the C# table and runs the C++ port against it (Core as source of truth) ; …
- **Inferred:** The D1 dashboard selftest note in the record is moot: the dashboard tool is not in tools/ (not checked further).

### ARC-002 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:32

- **Ruling:** D1 engine probe: two-engine measured probe deciding Unity vs Unreal; world stays data-driven.
- **Superseded by:** legacy/studio-v2/respec/decision-register/D16-engine-unreal.md:9
- **Checked:** legacy/studio-v2/respec/decision-register/D1-engine-probe.md:3 - 'CLOSED 2026-09-10 BY D16: the engine is Unreal' ; legacy/studio-v2/respec/decision-register/D16-engine-unreal.md:9 - 'Unreal. D1's probe is closed on the evidence.' ; production/assets/street/quay-street.json and production/specs/vignette-pieces.json - the street is JSON emitted by recipes and read by VignetteShot.cpp:1253-1259,1891-1904 (D1's 'world stays data-driven' clause holds)
- **Inferred:** Committed .uasset files under ue-probe/Content/Ledger are assumed to be script-made build products (tools/ue); not traced one by one.

### ARC-003 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:33

- **Ruling:** Chatterbox-Nano evaluated ahead of turbo, because turbo drops the exaggeration (direction) control.
- **Checked:** production/specs/voice-engines.json:2 - 'Everyone is on Nano, the game's own engine'; engines {} (nobody moved) ; DECISIONS.md:165 - the voice in the game: Nano to ONNX is the release route ; DECISIONS.md:183 - Ron stays on the game's voice (Chatterbox Nano) by Jafar's blind pick
- **Inferred:** The 28 July record's note (legacy game-design file) was not re-read; the operative part (Nano evaluated and adopted, turbo not) is in the game.

### ARC-004 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:34

- **Ruling:** No hardware floor is written from the sub-gigabyte paper; only its memory measurement transfers.
- **Checked:** production/research/hardware-floor/SUMMARY.md:1-5 - 'PARTLY OVERTURNED' header: the paper's sub-GB model is refuted; the 12 GB floor is not derived from it ; production/research/hardware-floor/RECHECK.md:135-160 - recommendation 2 struck; what transfers stated ; grep 'hardware floor/min-spec/minimum spec' over current *.md (excluding legacy/archive): no min-spec stated anywhere; production/research/checklist-sweep-2026-09-29/BUILDER.md:918 defers 'Minimum specification' to ship-prep

### ARC-005 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:35

- **Ruling:** Graphify is declined; it retires nothing and replaces grep.
- **Checked:** grep -ril graphify over the tree: only production/research/graphify-evaluation/*, production/archive/DECISIONS-to-2026-09-24.md and legacy/ records ; .claude/settings.json - no graphify tool or permission; tools/ has no graphify ; .github/workflows/* - no graphify step

### ARC-006 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:39

- **Ruling:** No alcohol or gambling shown, served, drunk or spoken of; pubs may exist as places; four enforcement sites.
- **Checked:** canon.md:109-111 - the rule in canon ; tools/content-gate.py:795-825 - word-list gate over banks, barks, prompt specs, brand bible; image-spec clause audit (exit 3); tools/ci-checks.sh:155-156 runs it on push ; content/brands/brand-bible-v1.json:6-7 - brand bible carries the content rule and is checked ; ledger/Assets/Scripts/Core/ResponseValidator.cs:73 - ContentRule.SpeechBreaks deflects a live reply; ledger/TalkHelper/Program.cs:1070,1130,1135 - every reply (and the early first sentence) validated before it is said ; …
- **Inferred:** The bar-back picture shows only if the Blender street fails to load (VignetteShot.cpp:2022-2025 fallback); in normal play it is hidden. It was never replaced as the D17 pass recommended (05-D17-town-pass.md:326-330). ; The static gate's corpus is mostly Unity-era files; the game's own talk cards and specs are covered instead by the Core's ContentWords tests and the live screen.

### ARC-007 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:40

- **Ruling:** Permanent content rule incl. NO CHILDREN ANYWHERE, enforced at six sites incl. crowd generation and the animation library.
- **Missing:** Sites 4 and 6 do not reach the Unreal game: no gate walks the game's animation clip and slot names, and the crowd-age guard exists only in Core; the image-clause audit does not read the game's current art specs.
- **Impact to a player:** 2 (No break found today; a future clip or image could reach players unchecked.) · **belongs:** tools/content-gate.py (LIBRARY_DIR and CORPUS extended to the Unreal animation imports and production/specs art specs); tools/ci-checks.sh · **lane:** builder
- **Checked:** canon.md:103-135 - the full rule, six sites named ; tools/content-gate.py, tools/ci-checks.sh:155-156 - word-list gate and image clause run on push; content/brands/brand-bible-v1.json:6 ; ledger/Assets/Scripts/Core/ResponseValidator.cs:73-76 and TalkHelper/Program.cs:1070,1130 - live replies screened ; tools/content-gate.py:1003 - site 6 (animation library) walks LIBRARY_DIR = ledger/Assets/Characters, the Unity library only ; …
- **Inferred:** No current break found: the clips the game uses are benign and its people are adults. The gap is coverage: NOW.md:16 (V6) brings Epic's animation sample into the game, and nothing would walk its clip names. ; The image-spec clause audit reads Unity-era prompt specs; the game's new image recipes (production/specs/shop-interiors.json 'never' clause, tools/art-recipes) are not gated by it.

### ARC-008 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:41

- **Ruling:** Live content screening on the reply path, before the voice, failing closed to an in-character deflection.
- **Checked:** ledger/Assets/Scripts/Core/ResponseValidator.cs:69-76 - ContentRule.SpeechBreaks and SafetyRule.SpeechBreaks deflect a reply ; ledger/TalkHelper/Program.cs:1070-1071 - the early first sentence is validated before it is sent to be spoken; :1130,:1135 - the whole reply ; ledger/TalkHelper/Program.cs:1178 - each turn logs went='refused' for a deflection ; ledger/CoreTests/Program.cs:3272,3281 - accepting and rejecting cases for the content rule ; …
- **Inferred:** The 'denominator' (replies screened, replies refused) is a per-turn log field, and 'refused' covers every deflection, not only content; no aggregate count was found.

### ARC-009 · NOWHERE **R** · production/archive/DECISIONS-to-2026-09-24.md:42

- **Ruling:** No resident speaks through a worse model because of who they are; tier by interaction or everyone better.
- **Missing:** The game tiers the language model by person (card tier): Sheila on Sonnet, Ron and Darren on Haiku. Neither 'tier by interaction' nor 'everyone on the better model' was chosen.
- **Impact to a player:** 4 (Players talk to all three in the first session; reply quality differs by who they are, the exact tell D48 forbids.) · **belongs:** ledger/Assets/Scripts/Core/ConversationEngine.cs:281 and the cards' tier field; a decision for FOR-JAFAR.md Needs you · **lane:** Jafar
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:281 - Model = card.Tier == 'core' ? Models.Core : Models.Ambient (model chosen by PERSON) ; ledger/Assets/Scripts/Core/LlmClient.cs:55-56 - Core = claude-sonnet-5, Ambient = claude-haiku-4-5 ; production/cast/cards/lena.md:3 'tier: core' (Sheila); rocco.md:3 and sam.md:3 'tier: ambient' (Ron, Darren) ; ledger/Relay/Relay.cs:43 - relay maps core->Models.Core, ambient->Models.Ambient ; …
- **Inferred:** DECISIONS.md:186/189 (Jafar's 'sheila-model: try' tap) tolerate per-person models in practice but never name D48, so I do not count them as superseding it; it needs his explicit ruling. ; D48's condition for choosing (the small-model test and cost per hour) now exists (DECISIONS.md:12, first-token-2026-10-01.md), so the choice it asked for is due.
- **Reviewer:** ConversationEngine.cs:281 picks the model by card.Tier; production/cast/cards: lena 'tier: core', rocco and sam 'tier: ambient'

### ARC-010 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:43

- **Ruling:** Comedy register: dry British wit, sparing seaside-postcard smut, Viz/tabloid flavour, never American satire; gate-enforced.
- **Missing:** None of D3's three enforcement sites exists: the canon gate excludes tone, the brand bible does not carry the register, and no narrative/tone verifier (D7 judge) is built; the live prompt does not state the register.
- **Impact to a player:** 2 (Tone drift in live replies would be noticed only gradually; cards carry the voice today.) · **belongs:** ledger/Assets/Scripts/Core/CharacterCard.cs prompt block (register line) and a tone check in the reviewer gate; TOWN.md · **lane:** town
- **Checked:** canon.md:63-64 - the register recorded in canon ; production/cast/cards/lena.md:12 'Dry humour, delivered deadpan'; production/cast/cards/rocco.md:15-17 example lines in register ; tools/canon-gate.py:17-20 - 'TONE IS NOT MECHANICAL and is not checked here: the D3 register needs the D7 judge' ; tools/dialogue-verify.py:8 - 'Tone is deliberately absent' ; …
- **Inferred:** Authored street lines get a blind reviewer for tone against the casting sheet (DECISIONS.md:190), which partly stands in for the narrative verifier; live replies get no tone check.

### ARC-011 · NOWHERE · production/archive/DECISIONS-to-2026-09-24.md:44

- **Ruling:** Crime layer owes eight verbs in order, press via a person, grassing; combat's three gaps; all stage 3.
- **Missing:** All eight verbs (order a man hurt, plan at a person, frame, lean on a witness, move a body, sanction crew, hit property, vouch), the press through a person, grassing, and the three combat gaps.
- **Impact to a player:** 3 (The boss half's missing act; met on the crime path once play goes past the first slice.) · **belongs:** ROADMAP.md stage 3 (as a named list), then Core (town) and the C++ port (builder) · **lane:** town
- **Checked:** grep 'vouch/alibi/grass/reporter/outnumber/flee/crew/sanction/order hurt' in ue-probe/Source: no verb implementation ; grep 'TargetPerson/OrderHurt/Outnumber/RunAway/Retract/Reporter' in ledger/Assets/Scripts/Core/*.cs: no verb (only Arsenal.cs:272 FleeScreaming, a witness reaction) ; grep the same over NOW.md, TOWN.md, ROADMAP.md, FINDINGS.md, CLOTHES.md, FOR-JAFAR.md: no list item ; ROADMAP.md:61 - stage 3 'One street that knows me: the crime loop visible' does not name the verbs ; …
- **Inferred:** Ordered not to be built 'this week' (21 Sept) and never re-filed on a current list when the studio's queue was archived.

### ARC-012 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:48

- **Ruling:** LEDGER is not a sandbox, shooter, driving game, economy sim or story-first game; non-core gets minimal budget.
- **Checked:** canon.md:151-156 - 'What LEDGER is not (D24)' with the budget rule, recorded in canon as the record asks
- **Inferred:** The budget half is a spend rule for sessions; no driving or combat is in the game (ue-probe has no combat port), consistent with it.

### ARC-013 · CONDUCT · production/archive/DECISIONS-to-2026-09-24.md:49

- **Ruling:** The end state is the ambition; reduced phase plans say they are scheduling documents in their first line.
- **Checked:** ROADMAP.md:1-3 - first line '# LEDGER: the milestones', 'Outcomes, in order' - a route ending at 'Then the town' (ROADMAP.md:64), not presented as final scope ; canon.md:12-20 - 'Game' section has no statement of the pillars or the 300-500-resident end state ; find vision-pillars*: only legacy/studio-v2/respec/vision-pillars-v2.md
- **Inferred:** The end-state ambition now lives only in legacy files and the binding archive (production/archive/DECISIONS-to-2026-09-24.md:49); no current governing file states it, which is the drift D27 guards against.

### ARC-014 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:50

- **Ruling:** Conversation pillar stands: live LLM talk with memory; the model classifies, never adjudicates; size from measurement.
- **Checked:** ledger/TalkHelper/Program.cs:265-274 - live talk per character with MemoryStore, KnowledgeBase, claim check ; DECISIONS.md:32 - 'Classifying a draft is the model's job; the Core decides what is said' (ClaimCheck.cs) ; DECISIONS.md:12 and production/research/local-models/SUMMARY.md - the small-model measurement ordered here was run ; no hardware floor or model size written from argument (see ARC-004)
- **Inferred:** D47's aside 'nothing tiers residents by model (D48)' is broken in the build; judged under ARC-009.

### ARC-015 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:51

- **Ruling:** NPC knowledge never shown as truth; Tom's own reading shown live and in the Ledger; NeitherKnows: nothing.
- **Missing:** The after-the-fact Ledger with itemised reasons (listed for stage 4, ROADMAP.md:62); the in-the-moment cue is not tied to Tom's own noticing (Awareness unused), so the NeitherKnows rule is not enforced.
- **On a list:** ROADMAP.md:62 (the Ledger only)
- **Impact to a player:** 4 (Every crime in ordinary play triggers the hint; the Ledger is a greyed menu entry players see.) · **belongs:** CrimeProbe.cpp HintHappened call sites gated on Awareness (builder); the Ledger under ROADMAP stage 4 / NOW.md UI item · **lane:** builder
- **Checked:** grep 'murmuring/uneasy/hostile/StreetWord/Reputation' in ue-probe/Source: no group or NPC-knowledge display ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:72 - 'The Ledger' greyed: 'Tom's notebook is not in this build yet.' ; ROADMAP.md:62 - stage 4 lists 'the Ledger' ; ledger/Assets/Scripts/Core/FirstMoments.cs:81-82 - in-the-moment hint 'Somebody saw that. What they make of it can go round.' ; …
- **Inferred:** The flee-sighting hint can warn the player in the NeitherKnows case (a witness behind him), the 'ghost' D33 and Observation.cs forbid.

### ARC-016 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:52

- **Ruling:** No global or group reputation number is ever stored; the town is only people.
- **Checked:** grep -i 'reputation/heat/notoriety' in ue-probe/Source TownSave.h, PoliceFile.h, TownWeek.h, WeeksEnd.h: no stored global or group number ; ue-probe/Source/LedgerProbe/Public/Gossip.h:31-32 - DayCircleHeat not ported; the port keeps per-agent rumours only ; ledger/Assets/Scripts/Core/Gossip.cs:830 - DayCircleHeat computed live, stores nothing

### ARC-017 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:53

- **Ruling:** Residents tiered by authoring, never memory: everyone perceives, remembers and gossips; 300-500 residents remain the target.
- **Missing:** Visible street people with no perception or memory; non-street cast without a MemoryStore in the game's mill. Not on any list.
- **Impact to a player:** 4 (A player can break a window in front of a walking passer-by who turns to look and never knows anything.) · **belongs:** production/specs/street-people.json and VignetteShot.cpp SpawnPeople (give them perception and a gossiper, or remove them); CrimeProbe.cpp:4699 · **lane:** builder
- **Checked:** production/specs/street-people.json:2 - the street's visible people 'are seen and not simulated: no collision, no perception, nothing a system reads' ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:2044,2184-2187 - SpawnPeople places them in the game (walking in free play) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4693-4701 - in free play the rest of the cast joins the mill with std::shared_ptr<MemoryStore>() and no KnowledgeBase ; ue-probe/Source/LedgerProbe/Public/TownRounds.h:1-15 - the whole cast talks by routine (gossip) in the port ; …
- **Inferred:** The cast beyond Sheila, Darren and Ron keep rumours (a memory of sorts) but no MemoryStore in the game, so they hold no episodic memory; whether that matters in play depends on whether they are ever talked to.
- **Reviewer:** production/specs/street-people.json:2 'seen and not simulated: no collision, no perception, nothing a system reads'

### ARC-018 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:54

- **Ruling:** Body language is moat: half-recognition, lying and having heard about Tom must show in posture before speech.
- **Missing:** A lying tell; the identification ladder's own tells beyond the three cast's looks; the owed list of every movement marked covered/free/town-specific.
- **Impact to a player:** 3 (Lying shows nothing in conversation; noticed by an attentive player in ordinary talk.) · **belongs:** PersonAnim.cpp / RegardTick (builder) fed by a Core 'is lying' signal from the talk program (town); NOW.md V6 · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5726-5764 - RegardTick: looks driven by what each holds about him and familiarity (first look, second look, look away) ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1131,1168-1199 - Knowing levels; bKnowsItIsHim from familiarity (half-recognition) ; grep -i 'lie/lying/liar' in StreetVoice.h, PersonAnim.h/.cpp, CrimeProbe.cpp: no lying tell in body or face ; RegardTick (CrimeProbe.cpp:5734-5737) covers only Sheila, Darren and Ron ; …

### ARC-019 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:55

- **Ruling:** The narrative is owed; a standing writing lane opens after the visual slice.
- **Checked:** CLAUDE.md:66 - the town session's lane includes 'the story' (a standing lane) ; game-design/story-outline-2026-09-28.md and .approval.json - story outline approved by Jafar 28 September ; game-design/first-hour-2026-09-29.md, week-end-2026-09-29.md - authored first hour and week's end; ue-probe FirstWeek.h, DayOne.h, WeeksEnd.h port them
- **Inferred:** Hours beyond the first week have an outline but no production plan; D30 asked only that the lane exist and the debt be recorded.

### ARC-020 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:56

- **Ruling:** Nothing stops reloading; instead the game plainly states which things are permanent.
- **Missing:** The plain in-game statement of what is permanent, so a reloading player knows he opts out.
- **Impact to a player:** 2 (A missing message; players would not notice its absence, but it is the ruling's whole point.) · **belongs:** FirstMoments.cs/FirstMoments.h hint words (town) and the title/loading or pause page (builder, NOW.md UI item) · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6254-6257 - each hour crossed is autosaved; TitleScreen.cpp:410 'Continue' loads it: no save cost ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:91-93,143-145 - pause text says only when it was last saved ; ledger/Assets/Scripts/Core/FirstMoments.cs:73-86 - hints: 'What you tell them, they remember.' Nothing on permanence or reloading ; grep -i 'permanent/reload/for good/can't be undone' in LedgerPause.cpp, TitleScreen.cpp, FirstMoments.h/.cs, production/design/ui/*.md: no statement ; …

### ARC-021 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:57

- **Ruling:** Five endings hold, no redemption path; hunted-state endings reachable; cost visible as it approaches.
- **Missing:** The five endings exist only in the C# Core, not in the Unreal game; the cost-visibility surface (the Ledger) is not built (listed for stage 4). Wiring the endings is on no list.
- **Impact to a player:** 3 (Only met at the end of a long campaign; no current build reaches an ending.) · **belongs:** C++ port of ActThree (builder) and ROADMAP.md stage 5/6; the Ledger under ROADMAP stage 4 · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/ActThree.cs - five endings in Core; grep 'Kingdom/StraightLife/BurnBoth/ActThree' in ue-probe/Source: none (PersonAnim's bSaidEnding is unrelated) ; ledger/TalkHelper/Program.cs: no call to ActThree (only compiled in) ; ledger/CoreTests/Program.cs:17650-17671 - condition 1: hunted-state reachability traced and tested (Kingdom reached) ; grep -wi pub ActThree.cs: only a comment at :193; :560 'You sign it over' (pub wording fixed) ; …
- **Inferred:** The game's week's end (WeeksEnd.h) is not the five endings.

### ARC-022 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:61

- **Ruling:** Visual bar: photoreal wet overcast grimy Britain, Meridian Test as bar, GTA V PS3 retired.
- **Missing:** The look at the bar: grime and wear, night light, dressing, convincing props (open items V1-V9).
- **On a list:** NOW.md:10 '- [ ] V. THE VISUAL BAR (Jafar, 1 October; each part researched for its method first, judged in the game's camera against the Hook sheet and the KCD2 frames ...)'
- **Checked:** canon.md:65-67 - the bar in canon, GTA V PS3 retired; grep 'GTA V/PS3' in current docs: no new document cites it as a target ; production/specs/unreal-look.json:13-14 - wet film day 0.6, night 0.9 (wet is built) ; DECISIONS.md:196 - Jafar's no to all four looks on 1 October: 'the street is too clean', night flat, windows black voids ; NOW.md:10-19 - 'V. THE VISUAL BAR' V1-V9 open, incl. NOW.md:14 'stains and wear' (grime) ; …
- **Inferred:** Grime (D53) was found unbuilt this week; V4 is its home now.

### ARC-023 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:62

- **Ruling:** The Meridian Test is the quality bar; the AA or premium-indie ceiling is dropped and never cited again.
- **Checked:** legacy/studio-v2/respec/decision-register/D9-quality-ceiling.md:7-15 - the Meridian Test governs, the AA/premium-indie label is dropped, the instrument is the test sampled at the roadmap's phase gates ; canon.md:65-67 - 'The bar is the Meridian Test (D8, D9); GTA V PS3 is retired as a reference bar' ; ROADMAP.md:63-64 - stage 5 judged by 'the four Meridian Test conditions read off one session', stage 6 samples conditions 2 and 3 ; ue-probe/Source/LedgerProbe/Public/LedgerSession.h:1-10 - the game writes a per-session record for Jafar's runbook; DECISIONS.md:64 ties it to the stage-5 Meridian reading ; …
- **Inferred:** The test itself has not been run, because stage 5 is not reached: the instrument is due later, not missing.

### ARC-024 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:63

- **Ruling:** Phase A's bar is the in-house Hook sheet, a floor not a ceiling, judged by Jafar beside a built frame.
- **Checked:** legacy/studio-v2/respec/decision-register/D23-the-phase-a-bar-is-the-hook-sheet.md:5-22 - the sheet as a floor; the test is Jafar unable to say which way the gap runs ; production/reference/hook-sheet.png exists, beside kcd2-town-arcades.jpg and kcd2-town-fountain.jpg ; ROADMAP.md:59 - stage 1 'One street that looks right', judged by 'His eye, beside the Hook sheet' ; CLAUDE.md:81 and DECISIONS.md:197 - every visual is compared with the Hook sheet and the KCD2 frames, its shortfalls named ; …
- **Inferred:** Adding the KCD2 frames on 1 October raises the bar without replacing the sheet, which fits 'a floor and not a ceiling'.

### ARC-025 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:64

- **Ruling:** The visual path in order: light, surfaces, wetness, clutter, geometry last, with D28's ten steps placed inside it.
- **Superseded by:** DECISIONS.md:201 (with DECISIONS.md:212 and NOW.md:5-19); geometry-last was first lifted by legacy/studio-v2/respec/decision-register/D28-presentation-is-built-early.md:48-66
- **Checked:** legacy/studio-v2/respec/decision-register/D31-the-visual-path.md:12-57 - the five-step order, and the table placing D28's steps inside it ; legacy/studio-v2/respec/decision-register/D28-presentation-is-built-early.md:48-66 - A1, 17 September: Jafar lifts the exclusion on geometry and buildings ('geometry and facades are the blocker') ; production/archive/DECISIONS-to-2026-09-24.md:159 - 22 September: a new order for the visual lane (lens, palette and colour, composition, shopfronts) ; production/archive/DECISIONS-to-2026-09-24.md:165 and :167 - 23 September: the look moves into Unreal, and Blender is for shapes and layout only ; …
- **Inferred:** The step contents D31 shares with D28 (post-processing, camera) are judged under ARC-028, not here.

### ARC-026 · NOWHERE **R** · production/archive/DECISIONS-to-2026-09-24.md:65

- **Ruling:** Grime is the strategy: surfaces carry wear as a separable layer, with a printed wear-coverage floor.
- **Missing:** In the game, no wear on facades, brick or ground beyond ten stains and the lamp's streaks. No wearCoverage is printed by the material station or for any street surface, and no floor (amendment A1) was ever set. The direction is on NOW.md V4; the measured floor is on no list.
- **On a list:** NOW.md:14 (the direction only)
- **Impact to a player:** 4 (Every street frame reads too clean (Jafar's 1 October no); with no floor, the look is argued again at every render.) · **belongs:** tools/ue/make_base_material.py (a wear mask per surface and a wearCoverage key) and the street painting in VignetteShot.cpp; a floor line under NOW.md V4 · **lane:** builder
- **Checked:** legacy/studio-v2/respec/decision-register/D53-grime-is-the-strategy-and-a-surface-carries-wear-above-a-floor.md:23-62 - the operative parts: wear over clean; wearCoverage printed per surface by tools/ue/make_base_material.py; the floor set as amendment A1 from the printed series; the facade authored with separable wear that prints wearCoverage ; grep 'wearCoverage/wear_coverage/wearMask/wear_mask' outside legacy/: only tools/art-recipes/lighting-column.py:1382-1476, its verdict production/art/atlas-01/lighting-column/lighting-column-verdict.txt:29-32, the spec production/specs/terrace-fronts.md:346-376 and a clothing note; no hit in tools/ue/ or ue-probe/ ; tools/ue/make_base_material.py: grep 'wear/grime/D53' finds no wear key, only the call to the stain-decal material at :4062-4079 ; The D53 record has no amendment A1; production/specs/terrace-fronts.md:356 'THE FLOOR HAS NO NUMBER AND THIS SPEC DOES NOT SET ONE' ; …
- **Inferred:** The Blender wear on the terrace fronts never reaches the game, since the GLB carries geometry and the sidecar no wear term; not confirmed with a render. ; V4 may add wear decals, but nothing listed would print a coverage number or set a floor, so the ruling's own point (a number, so the look is not argued again at every render) stays unbuilt after V4.
- **Reviewer:** terrace-front.py:63 says the wear layer 'is not this station'; grep wearCoverage in tools/ue and ue-probe/Source: no hit; NOW.md:14 (V4, since 1 October) lists 'stains and wear', not the floor or the measure

### ARC-027 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:66

- **Ruling:** The sky is the overcast photograph, not a SkyAtmosphere; how it is wired is free.
- **Checked:** legacy/studio-v2/respec/decision-register/D40-the-sky-is-a-photograph-not-an-atmosphere.md:9-13 and :88-101 - the photograph is the sky; A1: the ruling is the photograph, not the binding ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:294-312 - the rung was taken on 16 September: the photograph as a long-lat PNG on an unlit dome that the sky light captures ; production/d1-probe/ue-slicewalk-verdict.txt:66 (UE probe of 1 October, the walk in play) - skyModel=photograph-longlat-png-on-an-unlit-dome, skyHdriBoundAs=...belfast_open_field_2k, skyDomeMatIsSky=yes, ambientModel=skylight-captured-sky=THE-PHOTOGRAPH-ON-THE-DOME
- **Inferred:** D40's own open note, the photograph's horizon of trees and a field at the street's vanishing point, is not a requirement of the ruling; it falls under NOW.md:13 V3 (the hillside convincing or hidden). Research on 1 October calls the day sky 'flat white, with no haze' (production/research/aaa-street/SUMMARY.md, 'The rest of the frame').

### ARC-028 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:67

- **Ruling:** Presentation is built early: ten steps from the exposure fix through post-processing, camera, wetness, surfaces, wear, title card, cab office.
- **Missing:** Step 3: film grain, slight chromatic aberration, lens dirt and a grade toward the period's film stock (the vignette and bloom exist only as engine defaults). Step 4: depth of field for close conversation. Step 1: the probe's repeat of one scene still differs (1 October). None is on any list.
- **Impact to a player:** 3 (Seen in every frame, but as finish rather than function; it is part of what makes a frame read as a real game, which Jafar judges.) · **belongs:** a post-process block in production/specs/unreal-look.json applied by the playable street's volume (VignetteShot.cpp:8506-8674) and the talk camera; a line under NOW.md V · **lane:** builder
- **Checked:** legacy/studio-v2/respec/decision-register/D28-presentation-is-built-early.md:10-36 - the ten steps; :48-66 A1 lifts the exclusion on geometry ; Step 1: ue-probe/Source/LedgerProbe/Public/FrameStats.h:2026-2027, the settle rule exists; but production/d1-probe/ue-vignette-verdict.txt (1 October) prints rigDeterminism=DIFFERS, rigDiffPct=84.96, rigMeanLumaDelta=-0.0066 against the 0.005 bound, rigRepeatsWithinBound=1/of=2 ; Step 2: production/d1-probe/ue-slicewalk-verdict.txt:66 lanternsPlaced=4/4; production/specs/unreal-look.json lantern_lumens, lantern_linear_rgb, night_exposure_pin ; Step 3: grep 'FilmGrain/VignetteIntensity/SceneFringe/ChromaticAberration/BloomDirt/LensDirt/ColorGrad/LUT' in ue-probe/Source and ue-probe/Config: no hit; the source's post-process overrides are exposure only (VignetteShot.cpp:3987-4092, :8506-8674; MetaHumanPortrait.cpp:527-544); unreal-look.json's keys are gains, fog, glass, wetness and lanterns, with no grain, aberration, lens dirt or grade ; …
- **Inferred:** The vignette and the bloom come from Unreal's post-process defaults (vignette intensity 0.4, bloom on), not from a choice made for the look; film grain and chromatic aberration default to zero, so they are absent. ; Head bob was written for a first-person camera; the game is third-person (CLAUDE.md), so that sub-item is probably moot. ; Step 8 (twelve packages priced on the throughput ledger) was the retired studio's; production/throughput.md no longer exists. ; …

### ARC-029 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:68

- **Ruling:** Characters you talk to get blendshape faces driven by their audio (Audio2Face then; MetaHuman rigs under Unreal).
- **Missing:** Audio-driven faces for lines made in advance are made but switched off by default; listed as V8.
- **On a list:** NOW.md:18
- **Superseded by:** the driving layer only (Audio2Face): DECISIONS.md:134
- **Checked:** legacy/studio-v2/respec/decision-register/D2-faces.md:4-6 - blendshape-capable heads for every conversational character; audio-driven, batch over the clip corpus, live later ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:915-933 - Ron, Sheila and Darren spawn as the MetaHumans MH_RoccoP2, MH_LenaS4, MH_SamC5 ; production/cast/cards holds only lena.md, rocco.md, sam.md: the three who can be talked to are all MetaHumans ; DECISIONS.md:134 - mouths follow the voice's loudness through the MetaHuman face rig; Epic's speech-to-face comes next (this replaces Audio2Face) ; …
- **Inferred:** Street speakers who cannot be talked to ride stand-ins (FINDINGS.md:9), which D2 allows ('crowd-only NPCs may keep static faces').

### ARC-030 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:69

- **Ruling:** Every authored asset's brief names the concept sheet and research that govern it, which outrank any reply, even his.
- **Checked:** legacy/studio-v2/game-design/decision-2026-09-21-ruling-the-sheet-and-the-research-govern-every-authored-asset.md:11-22 and :24-46 - the standing rule, and the research consolidation pulled forward ; production/research/README.md:1-20 - routes 'which research governs it, and which concept sheet', quoting the rule and that the sheet and research win 'INCLUDING A DIRECT REPLY' ; game-design/research/GOVERNS.md:1-35 - the per-asset index for 17 street families, its pointer corrected to production/reference/hook-sheet.png ; CLAUDE.md:12-14 (production/research/README.md governs each thing's look) and CLAUDE.md:91 (sheet for mood, palette, composition; photographs win where they disagree) ; …
- **Inferred:** Putting the sheet and research above his own reply is a rule of conduct; the mechanism it names (the index and the consolidation) exists.

### ARC-031 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:70

- **Ruling:** Kit first, author second: assemble the street from free scanned libraries; author only British identity and real gaps.
- **Missing:** Kit-sourced cars, props and clutter (V2, V4); the dirty-down under the grime rule (ARC-026); no per-item shopping list.
- **On a list:** NOW.md:12; NOW.md:14
- **Superseded by:** the terrace fronts only: legacy/studio-v2/game-design/decision-2026-09-21-ruling-the-terrace-fronts-are-authored-and-everything-else-comes-from-what-we-hold.md:10-18
- **Checked:** legacy/studio-v2/game-design/decision-2026-09-21-ruling-kit-first-author-second.md:40-51 - shopping list (found, close enough, missing; licence checked), assemble, make it Meridian (grime, 1990 signs, Mickey's as cab office, D17/D18 check), fill only the gaps ; CLAUDE.md:22 and DECISIONS.md:19 - free Unreal content on the allowlist is downloaded without asking ; production/research/aaa-street/2-EPIC-FREE-CONTENT.md - 1 October survey of free Epic and other content against a 1990 port street (Fab itself was unreadable); the nearest thing to the shopping list ; production/assets/street/quay-street.json - the street in play is the authored Blender GLB, with 1990 signs (street_sign_fascia_*), Mickey's (street_mickeys_*) and Poly Haven scans (production/specs/ps5-corner.json 'scanned': brick_4, brick_wall_001, painted_concrete_02, always on) ; …
- **Inferred:** No per-item found / close enough / missing list against the Hook sheet exists; the 1 October research notes stand in for it item by item.

### ARC-032 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:71

- **Ruling:** Terrace fronts authored in Blender from the atlas plans under the grime rule, dressed in free scans; the rest from kits held.
- **Missing:** The fronts' wear under the grime rule does not reach the game: listed as NOW.md V4; its measured floor is on no list (ARC-026).
- **On a list:** NOW.md:14
- **Superseded by:** the British lamps from held kits: legacy/studio-v2/game-design/decision-2026-09-21-ruling-the-lamp-column-is-authored-and-it-is-the-authoring-lines-first-test.md:10-20
- **Checked:** legacy/studio-v2/game-design/decision-2026-09-21-ruling-the-terrace-fronts-are-authored-and-everything-else-comes-from-what-we-hold.md:10-18 and :43-64 ; tools/art-recipes/terrace-front.py builds the fronts; --export-glb writes production/assets/street/quay-street.glb and .json, read by ue-probe/Source/LedgerProbe/Public/StreetMeshes.h:1-16 ; production/specs/ps5-corner.json 'scanned': brick_red as brick_4, brick_grey as brick_wall_001, paint as painted_concrete_02, always true; applied in VignetteShot.cpp:7262-7300 ; Grime: terrace-front.py:63 'the wear layer ... is not this station'; _wear() at :5572 is Blender shader nodes only; no wear in Unreal (ARC-026) ; …
- **Inferred:** The scans' 'always' flag applies in live play as in the probe's shots (VignetteShot.cpp:7298); not confirmed from a play frame.

### ARC-033 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:72

- **Ruling:** The lamp column is authored in Blender, a plain steel swan-neck with a sodium lantern: the authoring line's first test.
- **Checked:** legacy/studio-v2/game-design/decision-2026-09-21-ruling-the-lamp-column-is-authored-and-it-is-the-authoring-lines-first-test.md:10-20 and :46-53 ; tools/art-recipes/lighting-column.py:1-40 - the authored recipe, citing the ruling and its governing sheet and research ; production/art/atlas-01/lighting-column/lighting-column-verdict.txt:1-12 - status=RAN, commission lamp-attempt-6-spigot, every dimension agreeing with the spec (shaft 0.114 m by 4.7 m) ; tools/art-recipes/terrace-front.py:1706-1766 - the street imports the accepted column and stands four of them, so it ships in quay-street.glb ; …
- **Inferred:** Its batch row on production/throughput.md (cost before and after) was studio bookkeeping; the file no longer exists, and the shrink of 24 September (DECISIONS.md:8) retired such records.

### ARC-034 · NOWHERE **R** · production/archive/DECISIONS-to-2026-09-24.md:76

- **Ruling:** Meridian's map is hand-drawn from canon as data, after a form bible, with testable gameplay layout rules and a reads-as-real gate.
- **Missing:** Rider 2, the layout spec with testable gameplay requirements, and rider 3, the mechanical reads-as-real gate; the form bible is unapproved. None is on a list.
- **Impact to a player:** 2 (The game is one street; these riders govern the Hook and the town at stages 5 and 6.) · **belongs:** a layout spec beside production/specs/hook-cast.json, named in ROADMAP.md's stage 5 and 6 rows · **lane:** town
- **Checked:** legacy/studio-v2/respec/decision-register/D13-street-layout-method.md:8-49 - drawn by hand from canon, nothing imported; riders: form bible first, a layout spec with testable requirements, a mechanical reads-as-real gate ; production/research/atlas-01/TOWN-FORM-BIBLE.md:1-30 - the bible exists, marked 'ART PROPOSAL ... Appearance and layouts remain unapproved'; rule 8 (a venue at each district's route crossing) is a design intention ; production/specs/vignette-scene.json:5 and production/specs/hook-cast.json (29 places, each with x_m and z_m) - the one built street is authored data; nothing imported ; grep 'interceptable/escape route/witness run/layout spec' in production/specs and tools: no hit (production/research/checklist-sweep-2026-09-29/BUILDER.md:381 is a combat row) ; …
- **Inferred:** With one street built, rider 2's requirements (venues at crossings, an interceptable witness run, countable escapes) have little to apply to before stage 5.
- **Reviewer:** D13's record, lines 24-35 and 85-86: the layout spec with testable requirements and the reads-as-real gate are owed

### ARC-035 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:77

- **Ruling:** Interiors in three tiers, with procedurally generated rooms on first entry (promotion by attention) as a gated experiment.
- **Superseded by:** legacy/studio-v2/respec/decision-register/D14-authored-interiors.md:11-16
- **Checked:** legacy/studio-v2/respec/decision-register/D5-interiors.md:3-9 - header: SUPERSEDED 2026-09-14 BY D14; the three tiers and the experiment are not the plan ; legacy/studio-v2/respec/decision-register/D14-authored-interiors.md:11-16 - the room grammar is retired; promotion by attention may generate nothing undesigned

### ARC-036 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:78

- **Ruling:** Every interior in scope is designed and script-assembled from designed kits; no room grammar; photoreal, not stylised.
- **Checked:** legacy/studio-v2/respec/decision-register/D14-authored-interiors.md:11-23 ; production/specs/mickeys-office.json 'what' - Mickey's office as a designed layout, assembled by script; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4016-4067 builds it from that file (only with -MickeysInside) ; grep 'room grammar/RoomGrammar/GenerateRoom/procedural interior' in ue-probe/Source, tools/ue and ledger/Assets/Scripts/Core: no hit ; Shop windows use interior mapping and cards (production/specs/shop-interiors.json; NOW.md:11 V1): a texture on glass, which D14 leaves alone ; …
- **Inferred:** D14 is a constraint more than a feature; nothing in the game breaks it, and the one interior is designed.

### ARC-037 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:79

- **Ruling:** Mickey's stands on the one built street, Quay Street in the Hook (siting kept; the pub half is void).
- **Superseded by:** the pub half only: legacy/studio-v2/respec/decision-register/D19-mickeys-is-a-minicab-office.md:8-10 and :25-31 (the pub decisions are VOID), with D15's own header at :3-9
- **Checked:** legacy/studio-v2/respec/decision-register/D15-mickeys-on-the-built-street.md:18-20 (the siting) and :47-53 (the amendment, option C: the built street is Quay Street in the Hook) ; canon.md:25 - 'THE BUILT STREET IS QUAY STREET, IN THE HOOK, and Mickey's stands on it'; canon.md:41-42 - 'D15's siting on Quay Street stands' ; production/specs/vignette-scene.json:5 street_identity: Quay Street, in the Hook ; production/assets/street/quay-street.json - meshes street_mickeys_frame_painted, street_mickeys_glass, street_mickeys_interior, street_sign_fascia_mickeys_plain ; …
- **Inferred:** production/specs/vignette-scene.json:5 still calls Mickey's 'the player's pub': stale wording in a file the game reads, though in a description field.

### ARC-038 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:80

- **Ruling:** Mickey's is a minicab office whose information room (fare book, radio, yard with two escapes, rank) makes knowledge.
- **Missing:** The information room as play: entered in normal play, the fare book read, the radio overheard, the yard's two escapes.
- **On a list:** NOW.md:27
- **Checked:** legacy/studio-v2/respec/decision-register/D19-mickeys-is-a-minicab-office.md:8-37 - the rule, why the cab office wins (its information room), the pub void, what pubs remain ; canon.md:18, :41-46, :72 - Mickey's a minicab office; other pubs boarded or serving food, never entered for drink ; production/cast/cards lena.md, rocco.md, sam.md mention the cab office or the rank (grep counts 2, 4, 2) ; production/specs/hook-cast.json:450, :493, :532 - the dispatcher (zlata) and the day and night cab drivers (ferko, dusan); places mickeys_office and mickeys_rank ; …
- **Inferred:** The radio 'nobody can help overhearing' and the fare book as a source of knowledge exist in no game code; the information room as play is the unbuilt half.

### ARC-039 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:81

- **Ruling:** No markers or fast travel now; places keep real coordinates and ids, the Ledger records where, maps come from data.
- **Missing:** The Ledger, and its record of where each thing happened.
- **On a list:** ROADMAP.md:62
- **Checked:** legacy/studio-v2/respec/decision-register/D36-a-maps-design-follows-the-worlds-size.md:6-21 ; grep 'fast.?travel/waypoint/minimap/map marker/objective marker' in ue-probe/Source: no hit ; production/specs/hook-cast.json - 29 places with stable ids and x_m/z_m ; ue-probe/Source/LedgerProbe/Public/LedgerSession.h:1-10 - the session record writes where the player went ; …
- **Inferred:** No map exists yet, so 'generated from data' is untested. The Core's ledger entry (ledger/Assets/Scripts/Core/PlayerKnowledge.cs:9-15, KnownLead) keeps holder, topic, source and time but no place, so when the Ledger is built the 'where' still has to be added.

### ARC-040 · NOWHERE **R** · production/archive/DECISIONS-to-2026-09-24.md:82

- **Ruling:** Director's landing ruling: the animation-library content gate, the settled night frame, the soak's scope, and filed follow-ups (smoking clip, watermark).
- **Missing:** The smoking clip that Jafar said was wrongly dropped (queue 406): no smoking animation anywhere in the Unreal game, and on no list. From the same filings: no trace of D50's watermark in the game's voice path or spec (queue 407). The sixth site and the night settle rule are built.
- **Impact to a player:** 2 (Smoking is canon-allowed period colour that a player notices only by its absence; it breaks no rule.) · **belongs:** NOW.md V6 (natural idles from Epic's sample, plus a smoking idle within D18); the watermark in tools/voice-live and production/specs/voice-engines.json · **lane:** builder
- **Checked:** legacy/studio-v2/game-design/decision-2026-09-21-ruling-five-landings-the-sixth-site-the-settled-night-frame-and-the-neighbourhood-that-is-not-the-town.md:69-136 (site 6 and the smoking clip), :137-213 (night settle), :214-288 (soak), :289-310 (queue 370), :377-389 (queues 406, 407, 408) ; tools/content-gate.py:981-1118 - site 6 walks ledger/Assets/Characters by slot name and Mixamo title; tools/ci-checks.sh:155-156 runs it and its selftest; canon.md:129 'Enforced at six sites' ; ue-probe/Source/LedgerProbe/Public/FrameStats.h:2026-2027 - kSettleMeanLumaBound 0.005, kSettleTakesMax 4; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:917 - kRepeatTargets = 2 (the first shot and the first night shot) ; production/d1-probe/ue-vignette-verdict.txt (UE probe of 1 October): rigRepeatOf=vign_camA_day and vign_camA_night, rigRepeatsWithinBound=1/of=2; the day repeat SETTLED in 2 takes yet reads rigMeanLumaDelta=-0.0066 against the 0.005 bound, the case this ruling says means the bound is wrong and its series must be read again ; …
- **Inferred:** Site 6 walks the old Unity layer's library, not the Unreal game's animations (MetaHuman, Epic's sample, the Mixamo street figures), so the content rule over the shipped game's clips is probably unwalked. ; Queue 370's column (spawn-cost.py, agent-turns.tsv) was studio bookkeeping, retired by the shrink of 24 September (DECISIONS.md:8).
- **Reviewer:** ledger/Assets/Characters/C/smoke__Smoking_*.fbx.rejected is the only smoking clip; grep 'smok' in ue-probe/Source: no animation

### ARC-041 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:86

- **Ruling:** The player has no stats or skills; each person believes him from their own record of him, never a global number.
- **Checked:** legacy/studio-v2/respec/decision-register/D11-player-progression.md:8-40 ; grep 'credibility/reputation/skill/level ?up/xp' in ue-probe/Source: no hit beyond number parsing in MemoryStore.h ; ue-probe/Source/LedgerProbe/Public/Gossip.h:383, :409-416, :770-774 - suspicion per hearer, raised when a rumour contradicts what the player told that person, with its reason ('a rumor about ... contradicts what the new owner told me') ; ledger/TalkHelper/Program.cs:50-63, :429-433 - each speaker's 'suspicion' and 'suspicionWhy' come from the Core into the talk ; …
- **Inferred:** FINDINGS.md:10: the port's suspicion number drives how a person treats him (RegardFor) while their talk reads the helper's; both are per person, so no global number exists, but the two can disagree.

### ARC-042 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:87

- **Ruling:** The player's own memory is surfaced in the Ledger journal; NPC minds are only ever the player's evidence-based model.
- **Missing:** The Ledger journal and its page in conversation; the evidence-based model of what each person knows.
- **On a list:** ROADMAP.md:62
- **Checked:** legacy/studio-v2/respec/decision-register/D12-information-surfaces.md:7-39 - the Ledger journal (entries tagged witnessed, heard, deduced), the Ledger page in conversation, NPC minds never shown, a model with confidence, diegetic verbs, the HUD scoped down ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:72 and LedgerPause.h:3-4 - 'Tom's notebook is not in this build yet' ; ledger/Assets/Scripts/Core/PlayerKnowledge.cs:6-23 - the player's belief about the rumour network exists in the C# Core only; grep 'PlayerKnowledge' in ue-probe/Source and ledger/TalkHelper/Program.cs: no hit ; ROADMAP.md:62 - stage 4 includes the Ledger ; …
- **Inferred:** PlayerKnowledge in the Core is the Ledger's model, but the game reaches it through neither the port nor the talk program.

### ARC-043 · NOWHERE **R** · production/archive/DECISIONS-to-2026-09-24.md:88

- **Ruling:** No minimap in Phase A; navigation is the what-they-know HUD, a paper map in the Ledger, and street signs.
- **Missing:** The what-they-know HUD (the police's knowledge during wanted states): not built, on no list. The paper map waits with the Ledger (ROADMAP.md:62).
- **On a list:** ROADMAP.md:62 (paper map, via the Ledger)
- **Impact to a player:** 2 (One street needs no navigation; the HUD's police role matters only on the arrest path.) · **belongs:** ROADMAP.md stage 4 beside the Ledger, then the builder's interface (LedgerPaper, production/design/ui) · **lane:** builder
- **Checked:** legacy/studio-v2/respec/decision-register/D20-no-minimap-for-phase-a.md:5-10 ; grep 'minimap/waypoint/map marker' in ue-probe/Source: no hit (no minimap) ; production/assets/street/quay-street.json - street_sign_plate_quay_street (signage) ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:72 - the Ledger is not in the build; ROADMAP.md:62 lists the Ledger (and so its paper map) ; …
- **Inferred:** The game has a police file and arrests (ue-probe/Source/LedgerProbe/Public/PoliceFile.h:1-12) but no 'wanted' state as such, so the HUD has little to show yet.
- **Reviewer:** D20's record, lines 7-8: the navigation surface is 'the what-they-know HUD'; grep in ue-probe and production/design/ui: only a hint that points at the unbuilt Ledger (FirstMoments.h:108)

### ARC-044 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:89

- **Ruling:** The Ledger is a notebook of per-person and per-event entries, not a corkboard; D12 stands.
- **Missing:** The Ledger notebook itself.
- **On a list:** ROADMAP.md:62
- **Checked:** legacy/studio-v2/respec/decision-register/D37-the-ledger-is-the-notebook-not-a-corkboard.md:5-10 ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:72 - 'Tom's notebook is not in this build yet' ; production/design/ui/README.md:3 - the interface designed 'in the same world as the Ledger notebook (D37)' ; ROADMAP.md:62 - stage 4 includes the Ledger

### ARC-045 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:90

- **Ruling:** Combat (melee first, firearms rare, as town-wide events) comes before driving, which waits for the region.
- **Missing:** Combat callable from live play (fists, improvised weapons) and gunshot perception: only a dormant C# design, on no list.
- **Impact to a player:** 3 (A player of a crime game who tries to hit someone finds nothing; it lies off the slice's main route (a window), so it is a specific path.) · **belongs:** a ROADMAP.md stage row naming combat (per G3), then a C++ port of Core/Combat.cs into ue-probe · **lane:** builder
- **Checked:** legacy/studio-v2/respec/decision-register/D4-combat-before-driving.md:4-5 - instrument: combat callable from live play; gunshot perception measured ; ledger/Assets/Scripts/Core/Combat.cs:1-25 - combat phases 1 and 2 exist in the C# Core, marked 'DORMANT ON PURPOSE. Do not "fix" this by wiring it in' ; grep 'combat/melee/punch/gunshot' in ue-probe/Source: only Gossip.h:216 (a fact a killing sets); grep 'Combat\.' in ledger/TalkHelper/Program.cs: no hit ; production/archive/DECISIONS-to-2026-09-24.md:110-111 - G3 (fists and improvised weapons in full; firearms as events) and G4 (Tom's driving waits for the region) ; …
- **Inferred:** The order holds by default, since neither combat nor driving exists. 'Stage 6' is the sweep's own placement; ROADMAP.md's six stages never mention combat.

### ARC-046 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:108

- **Ruling:** G1: Tom steps onto kerbs and climbs low walls and fences; no parkour; swims to a ladder if he falls in the basin.
- **Missing:** Climbing low walls and fences (no climb, vault or mantle anywhere in the game); swimming to a ladder (no basin water, no swim state).
- **Impact to a player:** 3 (Escapes over walls matter on the chase path after a deed; ordinary walking is unaffected.) · **belongs:** ue-probe SliceCharacter (a mantle/vault for low obstacles); a list item in NOW.md or ROADMAP stage 3 · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:58-61 - movement set (orient, rotation, walk speed); MaxStepHeight not set, so the engine default applies ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:527 - footway is one kerb upstand (0.125 m) above the carriageway ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:1800 - 'the road below the kerb is lower by its step, which is no obstacle' ; ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:289-300 - keys bound: run, act (E), talk, pause, quit, report, wait, notice; no climb, vault or mantle ; …
- **Inferred:** Kerb stepping works because Unreal's default step height (45 cm) exceeds the 12.5 cm kerb; not set explicitly in code ; The street as built has no basin water to fall into (FINDINGS.md:266 says the street ends in open paved ground), so the swimming half cannot arise yet

### ARC-047 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:109

- **Ruling:** G2: Rocco (Ron) and Lena (Sheila) are crew who act on Tom's orders, not followers.
- **Missing:** Ordering Ron or Sheila to do a job (the crime layer's crew assignments) exists only in the C# Core (Empire.cs) and the legacy Unity build; in the game Ron only carries Tom's no to the landing.
- **Impact to a player:** 3 (Felt once a player tries to run the firm through its people; the first week's route does not need it.) · **belongs:** port of Core Empire.cs crew assignments into ue-probe, or a ROADMAP stage entry · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/Arrangement.h:7 - Ron brings Mickey's envelope and can take Tom's no to the man at the landing (the one place Ron acts on Tom's word) ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1920 - street line 'Heard Ron went down the landing for you' ; ledger/Assets/Scripts/Core/Empire.cs:30-37 - CrewMember with Assignment (crew assigned to rackets); used by ledger/Assets/Scripts/Game/GameController.cs (legacy Unity) ; ledger/Assets/Scripts/Core/Companionship.cs:1-20 - companion-as-witness design, Core only ; …

### ARC-048 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:110

- **Ruling:** G3 (D4): fists and improvised weapons in full; firearms rare, as events; not a shooter.
- **Missing:** Any fight: no fists, no improvised weapons in the game; the combat code is dormant in the C# Core and unported.
- **Impact to a player:** 3 (A crime-game player who tries to hit someone finds nothing; the window is the only deed in the first week.) · **belongs:** ue-probe port of Core Combat.cs/Arsenal.cs; a ROADMAP stage line naming fights · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/Combat.cs:18-41 - 'DORMANT ON PURPOSE... Nothing outside this file references Fighter, Blow...' ; ledger/Assets/Scripts/Core/Arsenal.cs:1-20 - weapon table in Core ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:388 - 'needs Arsenal and Weapon, neither of which is ported'; Observation.h:16 same ; grep 'fist/punch/melee/Combat' in ue-probe/Source: no game hit (only the ported witness fields WeaponDrawn) ; …

### ARC-049 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:111

- **Ruling:** G4: moving traffic and the firm's cars driven by others are in the street now; Tom driving waits.
- **Missing:** Moving traffic and the firm's cars driven by others: none in the game (parked cars only); the traffic model exists only in Core and the legacy Unity build.
- **Impact to a player:** 4 (Seen in every minute of street play; Jafar's own reason was that a street with no traffic feels dead.) · **belongs:** ue-probe (port of Core Traffic.cs, cars on the carriageway); an item on NOW.md's list · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:2093-2101 - SpawnVehicles places the parked cars from production/specs/street-vehicles.json ; grep 'traffic/moving car' in ue-probe/Source: only the parked-vehicle spawner and a distant-traffic sound bed (production/specs/street-sounds.json ambience 'traffic-distant') ; ledger/Assets/Scripts/Core/Traffic.cs:4-20 - traffic model in Core; used by ledger/Assets/Scripts/Game/TrafficHost.cs (legacy Unity) ; production/research/checklist-sweep-2026-09-29/BUILDER.md:42 - 'moving traffic (his G4...: a street with no traffic feels dead; nothing moves today)' just below the twenty; rows A26.* marked later ; …

### ARC-050 · NOWHERE · production/archive/DECISIONS-to-2026-09-24.md:112

- **Ruling:** G5: boats and buses are moving scenery on a timetable, not ridden, for now.
- **Missing:** No moving boats or buses and no timetable anywhere; only a bus vehicle kind in the C# Core traffic model.
- **Impact to a player:** 2 (Moving scenery at a port; its absence is polish, though a quay with no boat moving reads still.) · **belongs:** ue-probe street (scenery movers on a schedule); a ROADMAP stage 2 line · **lane:** builder
- **Checked:** grep 'bus/boat/ferry/timetable' in ue-probe/Source: only lines of dialogue (OwnLines.h:102, StreetVoice.h:1668) and a town-news test row (CoreGolden.h:2148) ; ledger/Assets/Scripts/Core/Traffic.cs:67-94 - a 'bus' vehicle kind that stops at stops; no timetable (grep 'timetable' in Core: no hit); no boat kind ; NOW.md, TOWN.md, ROADMAP.md, FINDINGS.md: grep 'bus/boat' no list hit

### ARC-051 · NOWHERE **R** · production/archive/DECISIONS-to-2026-09-24.md:113

- **Ruling:** G6: a handful of short, skippable cutscenes for big beats such as the arrival with the suitcase.
- **Missing:** No cutscene system and no arrival scene; nothing on a list.
- **Impact to a player:** 3 (The opening beat a new player would meet first is missing, but play works without it.) · **belongs:** ue-probe (Level Sequences or scripted camera beats); a ROADMAP stage 4 line with the first hour · **lane:** builder
- **Checked:** grep 'cutscene/LevelSequence/MovieScene/suitcase/cinematic/skippable' in ue-probe/Source: no hit (only 'arrival' as a gossip story in StreetVoice.h) ; ue-probe/Source/LedgerProbe/LedgerProbe.Build.cs:18-69 - no LevelSequence or MovieScene module ; production/research/checklist-sweep-2026-09-29/BUILDER.md:87,107,309-310 - cutscene rows marked later (not a work list) ; NOW.md, TOWN.md, ROADMAP.md: grep 'cutscene/suitcase/arrival' no hit
- **Reviewer:** no Sequencer, LevelSequence or MovieScene module in ue-probe's Build.cs or .uproject

### ARC-052 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:114

- **Ruling:** G7: jobs and consequences, with a light note in the Ledger of what Tom is doing; no waypoints.
- **Missing:** The Ledger note of what Tom is doing (the notebook is not in the game).
- **On a list:** ROADMAP.md:62 - '/ 4 / The player's shell: menus, save, settings, controls, the Ledger and the first hour. /'
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6155 - Ron brings the envelope job ('for the ferry landing, after ten tonight') ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6247 - the envelope handed over at the landing; consequences through Arrangement.h and the town's talk ; ue-probe/Source/LedgerProbe/Private/LedgerPause.cpp:72 - 'The Ledger' greyed out: 'Tom's notebook is not in this build yet.' ; grep 'waypoint/objective/marker' in ue-probe/Source/LedgerProbe/Private: no hit (no waypoints, as ruled) ; …
- **Inferred:** The light Ledger note of what Tom is doing would live in the notebook, so it is covered by the stage 4 line

### ARC-053 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:115

- **Ruling:** G8 (D20, D37): no minimap; a paper map; the Ledger notebook.
- **Missing:** The paper map and the Ledger notebook are not in the game.
- **On a list:** ROADMAP.md:62 - '/ 4 / The player's shell: menus, save, settings, controls, the Ledger and the first hour. /'
- **Checked:** legacy/studio-v2/respec/decision-register/D20-no-minimap-for-phase-a.md - no minimap; 'a paper map in the Ledger' ; legacy/studio-v2/respec/decision-register/D37-the-ledger-is-the-notebook-not-a-corkboard.md - the Ledger is a notebook ; grep 'minimap' in ue-probe/Source: no hit (no minimap, as ruled) ; grep 'paper ?map/PaperMap/OpenMap' in ue-probe/Source: no hit ; …
- **Inferred:** D20 puts the paper map inside the Ledger, so the stage 4 line covers both; the sweep's 'when the town is bigger than the Hook' is a reinterpretation not ruled by Jafar

### ARC-054 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:116

- **Ruling:** G9: coat and pockets, plus storage at the cab office; bodies leave evidence, not loot.
- **Missing:** Coat and pockets and the cab-office storage exist only in the C# Core and the legacy Unity build; the game has no inventory.
- **Impact to a player:** 2 (Nothing in the first week needs carrying beyond the scripted envelope; matters once items and weapons exist.) · **belongs:** ue-probe port of Core Coat.cs; ROADMAP stage 4 or 5 · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/Coat.cs:6-20 - 'what is on you tonight', OnMe and AtHome, Core only ; ledger/Assets/Scripts/Game/CoatHost.cs - legacy Unity host ; grep 'pocket/inventory/OnMe/AtHome/storage' in ue-probe/Source: no inventory (only 'coat' as worn clothing and PoliceFile.h:197 'keeping the coat you had on, as evidence') ; production/research/checklist-sweep-2026-09-29/BUILDER.md:453-454 - 'G9: coat and pockets beyond the one envelope, and the office's storage' marked later ; …
- **Inferred:** The envelope is carried by script, not as an item in a pocket

### ARC-055 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:117

- **Ruling:** G10: buying, selling and fencing are in; crafting is out.
- **Missing:** Buying, selling and fencing: none in the game (no money); only the C# Core and legacy Unity economy.
- **Impact to a player:** 3 (The street's shops and Rita's pawn are visible but nothing can be bought, sold or fenced.) · **belongs:** ue-probe port of Core Wallet/Economy and the pawn's fencing; a ROADMAP stage line · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/Wallet.cs:12, Economy.cs:1-20, Purses.cs:1-20 - money and economy in Core ; ledger/Assets/Scripts/Core/Empire.cs:64 - 'fencing needs the pawnshop' (racket front), Core only ; grep 'buy/sell/fence/price/wallet/money' in ue-probe CrimeProbe.cpp/CrimeProbe.h/Arrangement.h/WeeksEnd.h: only a greeting line ('What are you selling today, then?', CrimeProbe.cpp:5622) ; grep 'Wallet/Economy/Empire' in ledger/TalkHelper/Program.cs: no hit ; …
- **Inferred:** No crafting found anywhere, consistent with the ruling

### ARC-056 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:118

- **Ruling:** G11 (D11): no stats; difficulty only as accessibility assists, never a hard mode.
- **Checked:** legacy/studio-v2/respec/decision-register/D11-player-progression.md - no improvable stats; progression external ; grep 'stat(s)/skill/level up/XP/hard mode/difficulty' in ue-probe/Source: no player stat or difficulty mode ; ue-probe/Source/LedgerProbe/Private/LedgerSettings.cpp:30-31,289-309 - subtitles, subtitle size, backing, speaker names, reduce motion, suggested lines, invert, sensitivity, brightness ; ue-probe/Source/LedgerProbe/Private/LedgerSettings.cpp:280 - 'The keys are fixed in this build; changing them comes later.'
- **Inferred:** Key remapping (a basic accessibility item) is absent; the sweep marks 'assists' later (BUILDER.md:456-459). The ruling's restriction (no stats, no hard mode) holds

### ARC-057 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:119

- **Ruling:** G12: English only for now, with all text kept out of the code so localisation is possible later.
- **Missing:** Text kept out of the code: interface strings are TEXT() literals and the street's own and shared lines live in C# and C++ source.
- **Impact to a player:** 1 (Invisible to English players; it only raises the cost of a later translation.) · **belongs:** ue-probe UI strings as FText/string tables; Core OwnLines.cs and StreetVoice.cs banks moved into content/ · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/OwnLines.h:1-2 - street lines generated from ledger/Assets/Scripts/Core/OwnLines.cs into C++ string arrays ; ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1390,1628,1920 - street lines compiled into code (ported from StreetVoice.cs) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:6155 - game captions as TEXT() literals; LedgerPause.cpp:71-80 and LedgerSettings.cpp labels likewise ; grep 'LOCTEXT/NSLOCTEXT/StringTable' in ue-probe/Source: no hit; no Content/Localization folder ; …

### ARC-058 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:120

- **Ruling:** G0: multiplayer stays out.
- **Checked:** grep 'OnlineSubsystem/multiplayer/bReplicates/ServerTravel/NetDriver' in ue-probe/Source and Config: no hit ; ue-probe/Source/LedgerProbe/LedgerProbe.Build.cs:18-69 - no networking modules

### ARC-059 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:121

- **Ruling:** The three areas the genre sort did not name (object interaction, optional presentation, making the game) are floor, marked in the checklist.
- **Checked:** production/archive/ROADMAP-checklist-to-2026-09-24.md:277 - explains 'floor (my call)' for the three areas ; grep -c 'floor (my call)' in that file: 72 rows (24 under A11 object interaction, 13 under A51, the rest single rows) ; production/archive/FOR-JAFAR-to-2026-09-24.md:249 - put to Jafar ('they're on the checklist marked floor (my call)')
- **Inferred:** What the game itself has of these areas is judged under ARC-118 (Jafar's confirmation of the same ruling)

### ARC-060 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:122

- **Ruling:** Close calls in the genre sort marked 'unsure': twelve kept in, and the jump ruled out under G1.
- **Checked:** production/archive/ROADMAP-checklist-to-2026-09-24.md:616 - A07.01 jump 'out', 'G1: unsure, my call: no jump' ; grep -c 'in by G[0-9]*: unsure' in that file: 11 rows kept in (the ruling says twelve) ; ue-probe/Source/LedgerProbe/Public/LedgerCharacter.h:7 and SliceCharacter.cpp:289-300 - no jump bound
- **Inferred:** The count differs by one (11 found, 12 claimed); a row may carry 'unsure' in other words. Not material

### ARC-061 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:126

- **Ruling:** D46: Mixamo bodies are in, the same way Mixamo animations are.
- **Checked:** ledger-v2/research/license-allowlist.md SHIP-SAFE 3 - 'Mixamo characters AND animations, with Jafar's account and a token he supplies (D46)' ; production/specs/street-people.json - the street's people are Mixamo bodies (production/assets/people/*.glb) ; ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:36-45 - the player's stand-in is tom-player (Mixamo) ; THIRD-PARTY.md:101 - 'Character models and animation — Adobe Mixamo'
- **Inferred:** The later bar (NOW.md:5, 'no placeholder anywhere a friend can look') and FINDINGS.md:266 treat the remaining Mixamo figures as placeholders to replace; that changes their use, not this permission

### ARC-062 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:127

- **Ruling:** D54: no MetaHuman wardrobe; the clothing route is a checker, then one jacket moved between bodies.
- **Superseded by:** DECISIONS.md:36 (route) and DECISIONS.md:211 (Epic's MetaHuman garments in use, contradicting 'no wardrobe')
- **Checked:** legacy/studio-v2/respec/decision-register/D54-*.md - route: garment meshes on the shared skeleton, a checker, then a jacket via Blender weight transfer ; DECISIONS.md:36 - 25 Sept: FreeSewing patterns in Blender, then Unreal's outfit tools; Marvelous approved if the free route stalls ; DECISIONS.md:211 - 1 Oct: meanwhile people wear Epic's plainest garments, re-coloured ; NOW.md:54 - 'Epic's plainest black leather lace-up boots from the MetaHuman wardrobe' ; …

### ARC-063 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:128

- **Ruling:** D55: the animation route is open; a generated-animation assembly line is the question, commissioned at stage 2.
- **Superseded by:** DECISIONS.md:164 and DECISIONS.md:198
- **Checked:** legacy/studio-v2/respec/decision-register/D55-*.md - commission: one clip through a spec-to-import line, or the named break ; DECISIONS.md:164 - Epic's free Unreal-only animation content (Game Animation Sample, Lyra) allowed ; DECISIONS.md:198 - natural idles and movement from Epic's free animation sample before the friends' build ; NOW.md:16 - V6 'People idle and walk naturally from Epic's free animation sample'
- **Inferred:** No assembly-line evaluation was found; the later rulings chose Epic's library instead

### ARC-064 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:129

- **Ruling:** D26: sound becomes a lane with a daily deliverable: footsteps by surface, doors, cloth, breath, rain, room tone, harbour bed; CC0 only.
- **Missing:** Footsteps by surface, doors, cloth, breath, rain, room tone, the harbour bed; no sound lane or daily deliverable.
- **On a list:** ROADMAP.md:60 - '/ 2 / One street that lives: residents on schedules, varied bodies, a face that moves and a voice, foley and an ambient bed. /'
- **Checked:** legacy/studio-v2/respec/decision-register/D26-sound-is-a-lane.md - the contents and the CC0 constraint ; production/assets/steps - one set of walk and run steps (no per-surface sets) ; production/specs/street-sounds.json - ambience is one 'traffic-distant' bed plus crowd voice lines ; ue-probe/Source/LedgerProbe/Private/StreetSounds.cpp:1-40 - positional ambience; grep 'rain/room tone/harbour/door/cloth/breath' no hit ; …
- **Inferred:** The lane structure itself appears replaced by the three-session structure (CLAUDE.md), with no ruling saying so

### ARC-065 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:133

- **Ruling:** The licence allowlist is law: nothing ships off it; new tools enter only by a record naming the weights licence.
- **Missing:** No mechanical check that what ships is on the allowlist; the named tool walks THIRD-PARTY.md entries for repo folders only.
- **Impact to a player:** 2 (Invisible in play; a licence slip would surface only at release.) · **belongs:** tools/attribution-check.py (or a license gate) covering the staged package and F:/LedgerTools sources · **lane:** builder
- **Checked:** ledger-v2/research/license-allowlist.md - the allowlist exists (SHIP-SAFE 1-8, NEVER SHIP 1-6, PROCESS 1-3) ; license-allowlist.md PROCESS 1 - 'untagged fails the license gate'; grep 'license gate/licence gate/license_tag' in tools: no such gate ; tools/attribution-check.py WATCHED - checks repo directories against tokens in THIRD-PARTY.md; 'allowlist' appears only in comments (lines 109, 314, 334, 508) ; tools/ci-checks.sh:151-152 - attribution check runs in CI ; …
- **Inferred:** Content the packaged game uses from outside the repo (MetaHumans in F:/LedgerTools/mh-dress, Epic animation, voice engines) is walked by nothing

### ARC-066 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:134

- **Ruling:** The attributions themselves, for everything shipped, in THIRD-PARTY.md.
- **Missing:** THIRD-PARTY.md lacks the Unreal engine, MetaHuman and Epic entries and still names Unity; no attribution (VCTK CC BY among them) ships with the packaged game and there is no credits screen.
- **Impact to a player:** 4 (Invisible in play, but the first copy that leaves his PC would breach CC BY attribution.) · **belongs:** THIRD-PARTY.md, tools/ue/stage_game_data.py (stage it), a credits page in the title menu · **lane:** builder
- **Checked:** THIRD-PARTY.md:1-14 - the file and its rule; tools/attribution-check.py runs in CI (tools/ci-checks.sh:151) ; THIRD-PARTY.md:126-132 - 'Engine — Unity' (stale: the game ships on Unreal) ; grep -i 'metahuman/unreal/epic' THIRD-PARTY.md: only body names at line 380; no MetaHuman, Unreal Engine or Epic entry ; tools/ue/stage_game_data.py:40-60 - stages fonts with their OFL texts, voices and acks, but not THIRD-PARTY.md or any attribution text ; …
- **Reviewer:** THIRD-PARTY.md:126-132 'Engine — Unity'; no Unreal, MetaHuman or Epic section

### ARC-067 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:135

- **Ruling:** D50: the voice watermark is kept on generated speech.
- **Missing:** Prepared lines (the street's voice bank, the thinking sounds, VoxCPM2 and Sopro takes) carry no watermark found; the live path's failure is silent.
- **Impact to a player:** 3 (Inaudible to players; unmarked generated speech is a compliance risk once the game is public.) · **belongs:** tools/voice-live (every take generator and the Sopro worker); a log line when marking fails · **lane:** builder
- **Checked:** legacy/studio-v2/respec/decision-register/D50-the-voice-watermark-is-kept.md - every voice path ran with the watermarker stubbed (21 Sept) ; tools/voice-live/voice-server.py:376-379 - live speech: apply_watermark per piece, an exception passes silently ('a piece too short to mark still plays') ; tools/voice-live/precompute-voices.py:177-179 - 'watermarker: ... (stubbed — it is not used here at all)' ; tools/voice-live/export_probe.py:1762-1771 - NoWatermark stub replaces Perth when it cannot load ; …
- **Inferred:** Whether Perth actually loads on his PC for the live path is not verifiable here; a failure is silent

### ARC-068 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:136

- **Ruling:** Characters and animations from Mixamo on Jafar's account with his token; nothing purchased; purchases and accounts are his.
- **Checked:** ledger-v2/research/license-allowlist.md SHIP-SAFE 3 - the same words ; production/assets/people/*.glb and THIRD-PARTY.md:101 - Mixamo assets in use and attributed

### ARC-069 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:146

- **Ruling:** A stop hook blocks a turn ending while NOW.md's sitting list is unfinished and time remains.
- **Superseded by:** DECISIONS.md:49 (and CLAUDE.md:49)
- **Checked:** .claude/settings.json - permissions only, no hooks key ; ls tools/sitting-clock.py: no such file ; ls .claude/hooks: no such directory ; DECISIONS.md:49 - 'our stop hook is removed (settings, its script and tools/sitting-clock.py)' ; …

### ARC-070 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:148

- **Ruling:** References live only in production/reference/; hook-sheet.png there; hook-pair.py refuses when it is missing.
- **Checked:** production/reference/hook-sheet.png exists (4.8 MB), retired sheet beside it ; tools/hook-pair.py:47 REFERENCE = production/reference/hook-sheet.png ; tools/hook-pair.py:162-167 _read_sheet returns 'no-sheet-at-...' error, no fallback ; tools/hook-pair.py:292 selftest checks the sheet is at the one path ; …
- **Inferred:** Recipes outside tools/ were not searched for other sheet paths.

### ARC-071 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:150

- **Ruling:** Quay Street: east six-bay parade; the west block opposite the north half has shops; the quay-end west block plain terraces.
- **Checked:** canon.md:33-40 - the three sides recorded, reworded 23 Sept by his decision 8(a) to say where the shop block is ; production/specs/vignette-scene.json:107,116 west_south ground_floor 'plain' ; production/specs/vignette-scene.json:129,138 west_north ground_floor 'shopfront', note at :147 'SHOPS, ruled by Jafar 2026-09-22' ; production/specs/vignette-pieces.json:460-463 west_north_bay0, pilasters and stallriser pieces (34 west_north shop pieces) ; …
- **Inferred:** Did not render a frame; that the GLB in production/assets/street/ was re-exported after the west_north change is inferred from the recipe and sidecar.

### ARC-072 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:152

- **Ruling:** Every message to Jafar opens 'For you:' then items or 'nothing'; the stop hook enforces it.
- **Superseded by:** DECISIONS.md:49 (enforcement removed); CLAUDE.md:19 and :31 (new message and channel format)
- **Checked:** DECISIONS.md:49 - the stop hook that enforced it is removed ; ls .claude/hooks and tools/sitting-clock.py: absent; .claude/settings.json has no hooks ; CLAUDE.md:19 - message format now 'Finished work: three lines: what changed; the picture; what next' ; CLAUDE.md:31 - the overview's 'Needs you' is the channel for what waits on him ; …

### ARC-073 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:153

- **Ruling:** Only two Unreal builds must not overlap; tools/art-recipes/** removed from the Unreal probe's triggers.
- **Checked:** .github/workflows/ledger-probe-unreal.yml:50-97 - paths list has no tools/art-recipes/**, comment records his 22 Sept ruling ; .github/workflows/ledger-probe-unreal.yml:108-110 concurrency group ledger-probe-unreal, cancel-in-progress false ; tools/ue/build-local.ps1:5,11-26 Wait-Runner waits while the runner builds, -WaitMutex on compile ; CLAUDE.md:85 - 'Two Unreal builds must not overlap'

### ARC-074 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:154

- **Ruling:** The west side is a half turn of the frontage on the object, not a reflection, so signs read right.
- **Checked:** tools/art-recipes/terrace-front.py:1920-1937 half turn about the block's own centre preserves handedness ; tools/art-recipes/terrace-front.py:5079-5119 the west block's half turn put on the OBJECT (obj.rotation_euler = (0,0,pi)) ; tools/art-recipes/terrace-front.py:6435-6438 lettered faces take UVs worked out after the export's reflection
- **Inferred:** Not checked in a rendered frame; west_north carries no lettering today, so the visible effect is on Blender-side signs only.

### ARC-075 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:156

- **Ruling:** Image-to-3D generation test deferred to stage 2, unscheduled; returns when one-at-a-time props become the bottleneck.
- **Checked:** grep 'image-to-3d/trellis/hunyuan/MESH3D' in NOW.md, TOWN.md, CLOTHES.md, ROADMAP.md, FINDINGS.md, FOR-JAFAR.md, DECISIONS.md: no hit (nothing scheduled, as ruled) ; production/research/aaa-street/SUMMARY.md:209 (1 Oct) - AI 3D generators re-examined when prop volume came up: 'a rough shell at best', TRELLIS needs an NVIDIA card, Hunyuan3D banned by the allowlist ; production/research/aaa-street/4-VEHICLES-AND-FURNITURE.md:101-102 - TRELLIS.2 cannot run on the AMD RX 6700
- **Inferred:** A deferral ruling: honoured (no test scheduled). Its return trigger (prop volume) has effectively arrived with NOW.md V2/V4, and the 1 Oct research looked again and found it unusable; no ruling records that re-look.

### ARC-076 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:157

- **Ruling:** Hook sheet pass 4 is the reference; 9 Sept sheet kept as retired; second MICKEY'S sign and third car not citable; dish citable.
- **Checked:** production/reference/hook-sheet.png and hook-sheet-2026-09-09-retired.png both present ; production/reference/README.md:27-33 - the second MICKEY'S sign and the third car not citable; the satellite dish citable ; production/specs/street-vehicles.json:3-17 - exactly two cars ; production/assets/street/quay-street.json - one street_sign_fascia_mickeys_plain mesh, street_dish_grey present ; …

### ARC-077 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:158

- **Ruling:** A beat constable knows Tom by sight (at the recognition line); strangers cannot place him.
- **Missing:** No beat constable exists in free play: no body, no routine, no cast entry; the 'knows Tom by sight' reading only runs in the scripted regression.
- **Impact to a player:** 3 (Only matters on the path where a constable could witness a deed; free play's arrests come through statements instead.) · **belongs:** ue-probe CrimeProbe.cpp free-play witnesses (a constable body and routine), production/specs/hook-cast.json · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:255-269 kConstableFamiliarity = Perception::RecognitionFamiliarity, 'the RECOMMENDED answer, built while he decides' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:8339-8340,8473-8474 the scripted regression's constable c1 reads with that familiarity ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2309-2313 'NO CONSTABLE IN PLAY: the cast has no policeman yet' - GC1Body is null when GEnc == Live (free play) ; grep 'constable/bobby/policeman' in production/specs/hook-cast.json, quay-cast.json, street-people.json: no hit ; …
- **Inferred:** The police-file constable who calls after a statement (CrimeProbe.cpp:6056-6072) is not a sighting witness, so his familiarity never matters.
- **Reviewer:** CrimeProbe.cpp:2310 'NO CONSTABLE IN PLAY: the cast has no policeman yet'

### ARC-078 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:159

- **Ruling:** Visual order once the sheet is approved: lens from the sheet, palette at that lens, composition, shopfronts to the 1989 photos, pair each step.
- **Checked:** production/reference/hook-sheet-lens.md and hook-sheet-lens-vp.py - the lens derived and written down ; production/specs/vignette-scene.json:892-903 cam_hook from that lens ; tools/art-recipes/terrace-front.py:7291 'THE PARADE, REWORKED TO THE 1989 PHOTOGRAPHS' with acceptance checks; :2383,4453 composition changes of 22 Sept ; tools/hook-pair.py - the pair tool ; …
- **Inferred:** The palette and composition steps were done in Blender and their results became targets once the look moved to Unreal (ARC-086); this is inferred from comments, not from frames.

### ARC-079 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:160

- **Ruling:** Night of 22-23 Sept: decisions take their recommendation, written in FOR-JAFAR.md, with a five-line Overnight section.
- **Checked:** production/archive/FOR-JAFAR-to-2026-09-24.md:759-761 the rule recorded that night ; production/archive/FOR-JAFAR-to-2026-09-24.md:549 'The Overnight section of 22-23 September, read. Its five lines...' ; CLAUDE.md:20 and :49 - the standing form: carry on with the recommendation; nothing waits on his hands
- **Inferred:** A one-night ruling, carried out; it binds nothing now beyond its standing successors in CLAUDE.md.

### ARC-080 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:161

- **Ruling:** Unreal's orientation is true; the Blender street's mirror is fixed once at export; the sheet is compared flipped.
- **Checked:** tools/art-recipes/terrace-front.py:6425-6438 one reflection of the whole street, y to -y, at export, windings reversed ; ue-probe/Source/LedgerProbe/Public/StreetMeshes.h:1-12 the export arrives the right way round ; tools/hook-pair.py:170-174 flip_for_true_street mirrors the sheet unless --sheet-as-drawn ; tools/hook-pair.py:12 'an Unreal frame beside the flipped sheet'

### ARC-081 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:162

- **Ruling:** No single-material tint in Unreal: the whole look crosses, tuned in one pass, and his 0.85 grade strength re-read then.
- **Checked:** production/specs/unreal-look.json:23-45 per-surface gains by base material (brick_red, brick_grey, paving, interior_lit), tuned 23 Sept against the sheet ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:6897-6908 each street mesh takes the palette over its photograph times its surface gain ; ue-probe/Source/LedgerProbe/Public/SurfaceBind.h:410,415 JafarGradeStrength still 0.85, dated 2026-09-15; :926 'This change does not re-read it'
- **Inferred:** The 0.85 was never re-read, but it now acts only through WetGradeFor on the scene file's own ground pieces, which the Blender street hides (street_in_play true), so it no longer reaches the visible street.

### ARC-082 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:163

- **Ruling:** The router stays on the paid model; run the 42 test lines on it; an offline router needs a trained small model.
- **Missing:** The router is not in the game at all: neither TalkHelper nor the Unreal code calls it, and the relay has no role for it. No NOW.md item wires it.
- **On a list:** ROADMAP.md:40-42 (milestone text only; no NOW.md item)
- **Impact to a player:** 3 (A player who types an action or order in talk gets talk back, never a game verb; contradicts ROADMAP's slice.) · **belongs:** ledger/TalkHelper (call IntentRouter before ConversationEngine) and ue-probe CrimeProbe.cpp talk wiring; NOW.md if still wanted · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/IntentRouter.cs:1-50 the router (classifies typed text into verbs) in the C# Core; RouterExamples.cs beside it ; production/research/local-models/SUMMARY.md:30 - the paid model's 41 of 42 on the old 42 lines (the test was run) ; DECISIONS.md:12 - 'The paid router stays; the local model is a later option' ; grep 'IntentRouter/PosesAsInstruction/RouteLexical' in ledger/TalkHelper, ledger/Relay, ue-probe/Source: no hit; callers are only SimHarness, RouterFloor, Adversary and the legacy Unity layer ; …
- **Inferred:** The Unreal game sends every typed line to talk; nothing in it routes text to a verb, so the router's model choice has no effect on play.
- **Reviewer:** grep 'IntentRouter/.Route(' in ledger/TalkHelper and ledger/Relay source: no hit; the game's talk never calls the router

### ARC-083 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:164

- **Ruling:** Rumour reach: find why a realistic witness under-fills the circle and if it is too few in 30 min; no constant moves.
- **Checked:** production/archive/FOR-JAFAR-to-2026-09-24.md:292-298 the finding brought: 'the town does not visibly know within thirty minutes, and more people knowing would not fix it', with why ; production/archive/FOR-JAFAR-to-2026-09-24.md:292 his decision 7 ruled (a): routines fixed so friends meet ; DECISIONS.md:52 - friends meet by routine (CastDay), 80 of 80 friendships ; production/research/rumour-propagation/SUMMARY.md exists
- **Inferred:** That no gossip constant moved between 23 Sept and the finding is taken from the summary's account, not diffed.

### ARC-084 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:165

- **Ruling:** The look moves into Unreal: geometry via meshes, materials rebuilt, then light and grade tuned until the Unreal frame matches the sheet.
- **Missing:** The Unreal frame does not yet match the sheet to his eye (stage 1 exit not passed).
- **On a list:** NOW.md:10 (V. THE VISUAL BAR, items V1-V9 at NOW.md:11-19)
- **Checked:** tools/art-recipes/terrace-front.py:6402,6425-6438 --export-glb; production/assets/street/quay-street.glb and .json ; tools/ue/import_street.py:127-192 imports the street as static meshes ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:1003-1043,1940-2048 the street placed and its look read from production/specs/unreal-look.json ; production/specs/vignette-scene.json:1463 exposure_pin_provenance: tuned 23 Sept at cam_hook, brick 0.96, road 0.94, far 0.91, shop 0.89, sky 1.03 of the sheet ; …

### ARC-085 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:166

- **Ruling:** The stop hook also blocks an empty list with time left until it is refilled from ROADMAP.md.
- **Superseded by:** DECISIONS.md:49 (and CLAUDE.md:49)
- **Checked:** DECISIONS.md:49 - the stop hook, its script and tools/sitting-clock.py removed ; ls tools/sitting-clock.py and .claude/hooks: absent; .claude/settings.json has no hooks ; CLAUDE.md:49 - 'no stop hook of our own'; the list is worked in order under /goal

### ARC-086 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:167

- **Ruling:** Blender for shapes and layout only; all look-dev in Unreal against the sheet, far-end depth with Unreal fog.
- **Missing:** The look in Unreal is not finished against the sheet; the far hill's depth was set aside.
- **On a list:** NOW.md:10 and NOW.md:13 (V3, the hillside)
- **Checked:** production/specs/unreal-look.json:2 'the look is developed in Unreal against the sheet'; lighting, wet, glass, grade and fog live there ; ue-probe/Source/LedgerProbe/Public/StreetMeshes.h:1-16 Blender colours carried only as targets ; production/specs/unreal-look.json:57-58 fog_note: far end 120/109/101 against the sheet's 120/108/104; the far hill 'SET ASIDE AFTER TWO TRIES' ; DECISIONS.md:196 his 1 Oct no: 'the hillside is identical boxes by day and black blocks by night' ; …
- **Inferred:** The lane change itself is in force (no look work found in Blender recipes after 23 Sept beyond shapes); not exhaustively checked.

### ARC-087 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:168

- **Ruling:** The street crosses as one GLB reflected at export, one mesh per material, Nanite off, replacing the scene file's pieces.
- **Checked:** tools/art-recipes/terrace-front.py:6402-6403 --export-glb; :6425-6438 whole-street reflection, rewinding, lettering UVs after reflection ; tools/art-recipes/terrace-front.py:6470-6476 THE GLASS CROSSES ONE MESH PER BAY AND FLOOR - glass later split by bay so a broken pane can hide ; tools/ue/import_street.py:127-135,174-182 Nanite off, read back; :111-124 complex-as-simple collision ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:2028-2043 replaced scene-file pieces hidden, not removed ; …
- **Inferred:** 'The walk and the crime keep the scene file's street' was overtaken the same day by street_in_play/street_collision (builder's choice in the look file), not by a ruling line.

### ARC-088 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:169

- **Ruling:** cam_hook is the approved sheet's lens: x -3.2, z -2.2, eye 2.0 on the quay apron, pitched up 3.4 degrees.
- **Checked:** production/specs/vignette-scene.json:892-903 cam_hook x -3.2, z -2.2, eye 2.0, declared_ground quay apron, yaw 20.4, pitch -3.4 (up), fov 46 ; ue-probe/Source/LedgerProbe/Public/VignetteSpec.h reads the cameras (via vignette-pieces.json)

### ARC-089 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:170

- **Ruling:** Blender's drawn brick, flag and stallriser patterns cross to Unreal as seamless 1024 px maps.
- **Checked:** tools/props/make_street_surfaces.py:41 PX = 1024; :346 SURFACES brick_red, brick_grey, paving, tile_patterned, kerbstone ; production/assets/street/surfaces/ - albedo, normal and roughness maps for all five; paving.png is 1024x1024 ; production/assets/street/quay-street.json - drawn_map for each of the five surfaces ; ue-probe/Source/LedgerProbe/Public/StreetMeshes.h:62-66 DrawnMap read and preferred over the photograph

### ARC-090 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:171

- **Ruling:** Unreal-only look settings live in production/specs/unreal-look.json, read at run time and printed on the verdict line.
- **Checked:** production/specs/unreal-look.json exists with 20+ settings ; ue-probe/Source/LedgerProbe/Public/StreetMeshes.h:271-373 Look struct and ParseLook (:779 street_in_play etc.) ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:1940-1945 read at run time; :2415-2425 printed on the verdict line ; production/specs/vignette-scene.json conditions keep sun_intensity 3.0 and sky_intensity 0.7; unreal-look.json:19 sun_gain is a multiplier

### ARC-091 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:172

- **Ruling:** The day's exposure pin is 2.000 and its fog density 0.0040, tied through the tests, with provenance named.
- **Checked:** production/specs/vignette-scene.json:916,918 overcast_day fog_density 0.0040, exposure_pin 2.000 ; production/specs/vignette-scene.json:1463 exposure_pin_provenance names the 23 Sept tuning ; grid_null_repeat, wet ladder and fog010 rows also at pin 2.0 / fog 0.004 (python read of conditions) ; production/specs/vignette-pieces.json carries exposure_pin 2 and fog_density 0.004 (what the game reads) ; …
- **Inferred:** The fog_maxop rows still carry fog 0.012; whether 'the fog series' in the ruling meant those or the fog010 rows was not resolved.

### ARC-092 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:173

- **Ruling:** From wet_film_from 0.5 the ground's relief map is swapped for a flat one, so a wet road is a film of water.
- **Checked:** production/specs/unreal-look.json:13-14 wet_film_from 0.5 with its note ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:7249-7255 bFilm = Wetness >= WetFilmFrom swaps in GStreetFlatNormal

### ARC-093 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:174

- **Ruling:** Shop glass is its own see-through material, M_LedgerGlass; without it the glass is left out, not opaque.
- **Checked:** tools/ue/make_glass_material.py exists with selftest; called from tools/ue/make_base_material.py:4045-4051 ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:2008-2019 loads /Game/Ledger/M_LedgerGlass, hides the glass if absent ; production/specs/unreal-look.json:17 glass_see_through true; glass_opacity note: Thin Translucent since 1 Oct

### ARC-094 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:175

- **Ruling:** Day fog cap is a x3 multiplier in the look file, leaving the scene file's 0.100 unchanged.
- **Checked:** production/specs/unreal-look.json:57-58 fog_cap_gain_day 3.0 with fog_note ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:3564 FogMaxOpacity * (SunOn ? FogCapGainDay : 1.0) ; production/specs/vignette-scene.json overcast_day fog_max_opacity still 0.1

### ARC-095 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:176

- **Ruling:** The kerb stands 125 mm above its channel, the footway falls to it, and the kerb is drawn as 915 mm precast blocks.
- **Checked:** tools/art-recipes/terrace-front.py:3550 KERB_UPSTAND_M = 0.125; :3554-3570 road_z, kerb_top_z, footway_z ; tools/art-recipes/terrace-front.py:2089-2116 kerb pieces stood on road_z/footway_z ; tools/props/make_street_surfaces.py:303-313 the kerb drawn as precast 915 mm blocks, KERB_BLOCKS = 4

### ARC-096 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:177

- **Ruling:** A night row asking no exposure pin is held at a fixed pin in Unreal (0.1 then) so lit glass does not blacken the meter.
- **Checked:** production/specs/unreal-look.json:59-60 night_exposure_pin 0.4; note: 0.1 on 23 Sept, moved to 0.4 on 29 Sept once the lamps lit the street ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:3472-3474 a night condition with no pin takes GLook.NightExposurePin ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:8640-8673 ApplyPlayCondition moves the player's volume to the same pin, with the night bias
- **Inferred:** The mechanism is as ruled; the value is now 0.4, a later builder choice recorded only in the look file's note, not in DECISIONS.md.

### ARC-097 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:178

- **Ruling:** The parked cars face the camera (nose toward the south end), with headlamps, in the sheet's navy and pale blue-grey.
- **Checked:** production/specs/street-vehicles.json:3-17 two cars, hatch-navy and hatch-bluegrey, face_deg 180 ('down the street toward the camera') ; tools/art-recipes/terrace-front.py:3738-3750 facing -1, turned round 23 Sept ; tools/art-recipes/car-model.py:189 headlamps ; production/assets/vehicles/hatch-navy.glb, hatch-bluegrey.glb
- **Inferred:** The cars themselves failed his 1 Oct look ('crude boxes', NOW.md:12 V2); that is their quality, not this ruling.

### ARC-098 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:179

- **Ruling:** The playable street holds the day's exposure through an unbound post-process volume with the day's pin.
- **Checked:** ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:8457,8491-8516 BuildInteractiveStreet spawns an APostProcessVolume, bUnbound = true, min=max=GExposurePinNow ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:8640-8673 the pin follows the light in play

### ARC-099 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:180

- **Ruling:** Each flag is its own stone in Unreal: tones spread 1.8x, a hue per flag, darker joints, symmetric about the mean.
- **Checked:** tools/props/make_street_surfaces.py:221-252 FLAG_SPREAD 1.8, FLAG_HUE per flag, FLAG_JOINT_WET 0.65, symmetric about the recipe's mean ; production/assets/street/surfaces/paving.png (1024x1024) and its drawn_map in quay-street.json

### ARC-100 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:181

- **Ruling:** The port takes the Core's crowd schedule (OutdoorsAt, OutdoorPosition, IsRestDay, TripHours) with golden rows; crowd generation not ported.
- **Missing:** The ported crowd schedule is never called by the game; only the golden comparison runs it.
- **Impact to a player:** 2 (Invisible today: no anonymous crowd walks; named people follow CastDay instead.) · **belongs:** ue-probe CrimeProbe.cpp / VignetteShot.cpp SpawnPeople, or a ruling retiring the crowd schedule · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/Schedule.h:2-18,66,82-123 IsRestDay, OutdoorsAt, OutdoorPosition, TripHours transliterated ; ue-probe/Source/LedgerProbe/Public/CoreGolden.h:49,5039-5062 golden rows compare them ; grep 'Schedule.h/Schedule::' in ue-probe/Source/LedgerProbe/Private: no hit - no game code calls the crowd schedule ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:66,4676-4706 the game uses CastDay (the named cast's routines, ported later, DECISIONS.md:52) ; …
- **Inferred:** The anonymous crowd this schedule drives does not exist in the game; the later named-routine approach (CastDay, 30 regulars) may have made it obsolete, but no ruling says so.

### ARC-101 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:182

- **Ruling:** Lumen on for the whole street: software GI and reflections over distance fields; both bricks' gains raised a quarter.
- **Checked:** ue-probe/Config/DefaultEngine.ini:46-48 r.DynamicGlobalIlluminationMethod=1, r.ReflectionMethod=1, r.GenerateMeshDistanceFields=True ; ue-probe/Config/DefaultEngine.ini:58 r.Lumen.HardwareRayTracing=0 (software) ; production/specs/unreal-look.json:23-45 brick gains and the note 'RAISED A QUARTER FOR BOTH BRICKS 23 September, when Lumen went on'

### ARC-102 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:183

- **Ruling:** The game targets SM6 on DX12; ray tracing compiled in and off for the street, on only for the PS5 corner's max shot.
- **Checked:** ue-probe/Config/DefaultEngine.ini:79-85 DefaultGraphicsRHI_DX12, -PCD3D_SM5, +PCD3D_SM6 ; ue-probe/Config/DefaultEngine.ini:49-62 r.RayTracing=True, r.RayTracing.Enable=0 ; production/specs/ps5-corner.json shot corner_max cvars include r.RayTracing.Enable 1

### ARC-103 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:184

- **Ruling:** The wet is standing water: thin dark near-mirror sheets at kerb edges, gutters and road pools, off pavement objects.
- **Checked:** tools/art-recipes/terrace-front.py:3137-3175 standing_water / standing_water_flags placed by road_z/footway_z falls ; production/assets/street/quay-street.json - meshes street_standing_water and street_standing_water_flags exported
- **Inferred:** 'Kept off anything standing on the pavement' was not traced line by line.

### ARC-104 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:185

- **Ruling:** The PS5 corner lives in production/specs/ps5-corner.json, appended after the scene's shots, settings set and put back per shot.
- **Checked:** production/specs/ps5-corner.json - cameras, shots corner_street, corner_max, hook_max, corner_scanned, hook_scanned with cvars ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:1286,1503 AppendShotsFile('ps5-corner.json') ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:8265 previous shot's cvars put back, this shot's set (DriveCornerCvars)

### ARC-105 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:186

- **Ruling:** The router's guard is the game's: instruction-shaped lines become speech before either path; the rest reach the model fenced.
- **Missing:** The guard runs only in the C# Core's router and its test harness; the game's typed lines never pass through it.
- **On a list:** ROADMAP.md:40-42 ('the game's own block widened', milestone text only)
- **Impact to a player:** 2 (Without a router in the game, nothing a forged line could trigger exists; matters only once verbs are routed.) · **belongs:** ledger/TalkHelper alongside the router (see ARC-082) · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/IntentRouter.cs:480-500 PosesAsInstruction: role, machinery, override, plain-order and identifier shapes ; ledger/Assets/Scripts/Core/IntentRouter.cs:386 PlayerLineMessage fences the line ; ledger/RouterFloor/Program.cs:443,692 the guard measured there ; grep 'PosesAsInstruction/PlayerLineMessage/IntentRouter' in ledger/TalkHelper, ledger/Relay, ue-probe/Source: no hit ; …
- **Inferred:** Because the game never routes typed text to verbs, the guard has nothing to protect in play today; a hostile line reaches the talk model as speech.
- **Reviewer:** grep 'IntentRouter/.Route(' in ledger/TalkHelper and ledger/Relay source: no hit; the game's talk never calls the router

### ARC-106 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:187

- **Ruling:** The slice's cast: ten of the prototype cast placed hour by hour on Quay Street (quay-cast.json).
- **Superseded by:** DECISIONS.md:52 (hook-cast.json, forty people read by CastDay)
- **Checked:** production/specs/quay-cast.json - the ten (rocco, lena, zlata, sam, rita, victor, marla, joey, ada, noor) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4652-4655 - live play reads production/specs/hook-cast.json ; tools/ue/stage_game_data.py:38 - quay-cast.json staged only 'for the CastDay rows of the golden run' ; DECISIONS.md:72 - 'Zlata' was a placeholder no ruling made a name

### ARC-107 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:188

- **Ruling:** The slice's talkers speak from new cards in production/cast/cards, brought to D18 and D19.
- **Checked:** production/cast/cards/lena.md, rocco.md, sam.md - the three cards ; ledger/TalkHelper/Program.cs:1344-1355 - CardsDir finds production/cast/cards (or 'cards' beside the program) ; production/cast/cards/lena.md:6,27 and rocco.md:34 - Mickey's is a minicab office (D19); grep 'pub/pint/drink' no hit (D18)

### ARC-108 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:189

- **Ruling:** The content rule is carried twice in talk: in the model's instructions and in the reply check generated as ContentWords.cs.
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:542-548 - the rule in the model's instructions ; ledger/Assets/Scripts/Core/ContentWords.cs:1-2 - 'GENERATED by tools/content-gate.py --emit-core' ; ledger/Assets/Scripts/Core/ContentRule.cs:159-167 and ResponseValidator.cs:73 - replies checked against ContentWords ; tools/content-gate.py:1855-1856 - --emit-core with --check ; …
- **Inferred:** Nothing automated runs 'content-gate.py --emit-core --check' (grep in tools/ci-checks.sh and .github/workflows: no hit), so a stale copy would not fail CI

### ARC-109 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:190

- **Ruling:** The slice's player is its own Character (ALedgerSliceCharacter) with movement and a spring-arm camera, under -LedgerSlice.
- **Checked:** ue-probe/Source/LedgerProbe/Public/SliceCharacter.h:25 - class ALedgerSliceCharacter : public ACharacter ; ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:58-70 - movement and spring-arm camera ; ue-probe/Source/LedgerProbe/Private/LedgerGameMode.cpp:56-58 - -LedgerSlice sets it as the pawn

### ARC-110 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:191

- **Ruling:** The slice's player wears a stand-in body (Mixamo Adam, grey tracksuit) until Tom's look and period clothes are settled.
- **Checked:** ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:36-45 - SK_tom-player with idle, walk and run ; production/assets/people/tom-player.glb - present
- **Inferred:** Tom is still the stand-in; NOW.md:56 asks for Tom's body after Ron, Darren and Sheila, and V9 (NOW.md:19) covers 'everyone' in 1990 clothes

### ARC-111 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:192

- **Ruling:** The navigation mesh is built at run time and only around invokers; the slice's player carries one.
- **Checked:** ue-probe/Config/DefaultEngine.ini:109 - bGenerateNavigationOnlyAroundNavigationInvokers=True ; ue-probe/Config/DefaultEngine.ini:120 - RuntimeGeneration=Dynamic ; ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:73-74 - NavInvoker on the slice player

### ARC-112 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:193

- **Ruling:** The simulation steps on a fixed clock (LedgerSim::FixedClock, 0.1 s, at most eight a frame, dropped steps counted).
- **Missing:** FixedClock is built and tested but wired into nothing; the live clock reads the frame's length and drops time over 1 s silently.
- **Impact to a player:** 2 (Only a long hitch or a very low frame rate would show it, as lost game time.) · **belongs:** ue-probe CrimeProbe.cpp ClockTick (step through FixedClock) · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/FixedClock.h:31-52 - the fixed clock as ruled ; ue-probe/tests/core-port-test.cpp:289-301 - tested ; grep 'FixedClock/LedgerSim::' in ue-probe/Source/LedgerProbe (outside FixedClock.h): no hit - the game never uses it ; ue-probe/Source/LedgerProbe/Public/LiveClock.h:52-63 - the game's clock adds each frame's real seconds (capped at 1 s, nothing counted) into game minutes ; …
- **Inferred:** The town's hourly work runs on whole hours crossed, so most simulation is frame-rate independent in effect; per-frame perception was not traced
- **Reviewer:** grep 'FixedClock' in ue-probe/Source outside FixedClock.h: no hit

### ARC-113 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:194

- **Ruling:** The street's people are solid in the slice (a capsule blocking bodies, never sight), not in the probe's walk and crime.
- **Checked:** ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:1622-1640 - MakeSolid: capsule blocks bodies, ignores Visibility and Camera ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:2309 - only when interactive and -LedgerSlice

### ARC-114 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:198

- **Ruling:** Decision 7(a): a hearer who knows remarks once per story, then watches Tom longer; the paper counts.
- **Missing:** 'The paper counts': the newspaper (Core Press.cs) is not in the game, so nobody learns of Tom from a front page.
- **Impact to a player:** 2 (Only matters once a deed is big enough for the paper; the window deed spreads by talk.) · **belongs:** ue-probe port of Core Press.cs · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/StreetVoice.h:512-560 - Stance with bRemarkedAlready: once per story, then the look (ported, golden-checked) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2953, 5754 - RemarkLedger and RegardFor used in play ; production/archive/FOR-JAFAR-to-2026-09-24.md:225 - 'The paper counts, so after a front page the whole street looks' ; ledger/Assets/Scripts/Core/Press.cs:1-15 - the newspaper channel, Core only ; …

### ARC-115 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:199

- **Ruling:** Dropped or slow connection: the authored street carries on; an in-character brush-off and a small sign; slow lines abandoned after about 8 s.
- **Checked:** ledger/TalkHelper/Program.cs:31-32 - 'a model that has not answered in eight seconds is abandoned for the same brush-off' ; ledger/TalkHelper/Program.cs:658-659 - the card's own brush-off line ; ledger/TalkHelper/Program.cs:1138-1151 - unreachable or paused talk sets 'paused' (AiNotice.TalkUnreachable / TalkPaused) ; ledger/Assets/Scripts/Core/AiNotice.cs:46,63,67 - the sign's wording ; …

### ARC-116 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:200

- **Ruling:** The pause before an answer: a breath, glance or filler in their own voice picked by mood; the subtitle appears only with its audio.
- **Missing:** Fillers picked by mood; Sheila's fillers; subtitles held until their audio plays (they show about 3.5 s early).
- **Impact to a player:** 4 (Every conversation shows the words seconds before the voice; Sheila, the main talker, has no filler.) · **belongs:** ue-probe CrimeProbe.cpp (Say on the first piece's playback; AckStart by mood); content/voice/acks/lena · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3840-3870 - AckStart plays a thinking sound with its glance animation ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3850 - picked in rotation (Files[GAckTurn++ % n]), not by mood ; content/voice/acks - rocco and sam only; Sheila (lena) has none (also DECISIONS.md:84 'Sheila none yet') ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5001 - the first sentence's subtitle is shown the moment its words arrive, before its sound ; …
- **Reviewer:** CrimeProbe.cpp:5001 shows the first sentence as a subtitle when its text arrives; the voice is released after it (:5003)
- **Reviewer:** content/voice/acks holds rocco and sam only: Sheila has no thinking sounds

### ARC-117 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:201

- **Ruling:** The minute after a deed: near people look and some gather, drift back within minutes, witnesses talk quieter for an hour, heat fades it.
- **Missing:** In the game nobody looks at or gathers after the smash, nobody drifts back, the quieter talk is never called, and heat does not fade it; only the looking and the talk are on a list.
- **On a list:** NOW.md:14 (V4, the neighbours' talk) and NOW.md:21 (item 3's twenty basics, BUILDER.md:36 'people turn toward the smash'); gathering and drifting back are on no list
- **Impact to a player:** 4 (The window is the first deed; a street that ignores breaking glass is seen in the first session.) · **belongs:** ue-probe CrimeProbe.cpp (call StreetVoice::Ambient; reactions in PersonAnim and the walkers) · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Public/StreetVoice.h:1768-1816 - the 90 s just-now and settling talk banks, inside Ambient() ; NOW.md:14 - V4: 'StreetVoice.Ambient, never called' ; grep 'StreetVoice::Ambient/Ambient(' in ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp: no hit ; grep 'gather/turn toward/toward the smash' in CrimeProbe.cpp/PersonAnim.cpp: no hit; gathering exists only in legacy ledger/Assets/Scripts/Game/NpcWalker.cs ; …

### ARC-118 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:202

- **Ruling:** Jafar: the three unnamed areas are floor: object interaction, optional presentation (photo mode, credits, post-ending), making the game.
- **Missing:** Credits, photo mode and the post-ending state: none in the game and none on a list.
- **Impact to a player:** 2 (Polish for most players, though a credits screen is also where shipped attributions usually live.) · **belongs:** ue-probe TitleScreen.cpp (credits); a ROADMAP stage 4 line · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:291-292 - act (E) and talk (T); prompts on people (NOW.md:9) ; grep 'credits/photo ?mode' in TitleScreen.cpp, LedgerPause.cpp, LedgerSettings.cpp: no hit ; ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:410-413 - title offers Continue, New game (and Settings, Quit); no credits ; production/casting and tools/ai-tester - casting and QA (making the game) exist ; …
- **Inferred:** The post-ending state cannot exist until an ending is in the game

### ARC-119 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:203

- **Ruling:** The slice's talking runs beside the game: the tested C# engine as a helper program (TalkHelper), not rewritten in C++.
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3176-3200 - LiveHelperStart launches TalkHelper (or LedgerTalk.exe beside the package) ; ledger/TalkHelper/TalkHelper.csproj - compiles ../Assets/Scripts/Core/**/*.cs

### ARC-120 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:204

- **Ruling:** The six realistic Mixamo extras become the slice's cast, Rocco, Lena and Sam first.
- **Superseded by:** DECISIONS.md:18 (cast MetaHumans) and DECISIONS.md:34
- **Checked:** production/archive/FOR-JAFAR-to-2026-09-24.md:256-257 - the question: the six realistic Mixamo extras as the walking cast ; DECISIONS.md:18 - cast MetaHumans take the places of three stand-ins; DECISIONS.md:34 - faces cast in MetaHuman ; FINDINGS.md:266 - the remaining three Mixamo figures (Martha, Kate, Leonard) stand as placeholders, not in the town

### ARC-121 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:205

- **Ruling:** The AI tester's hands: Claude's computer control through the paid API, run while Jafar is away.
- **Superseded by:** DECISIONS.md:99
- **Checked:** DECISIONS.md:99 - no API calls in development; the AI tester is played by the session itself ; DECISIONS.md:23 - earlier method through the conversation model

### ARC-122 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:206

- **Ruling:** Downloads go ahead: Chatterbox Nano (MIT), CC0 scanned materials for the PS5 corner, MetaHuman with Jafar's Epic sign-in.
- **Checked:** tools/voice-live/voice-server.py:128-129 - NANO_PKG and NANO_WEIGHTS under C:\LedgerTools\chatterbox-nano ; production/assets/scanned/polyhaven - brick_4, brick_wall_001, concrete_pavement_02, asphalt_01, painted_concrete_02 ; production/specs/in-game.json - MetaHumans (MH_LenaS4, MH_RoccoP2) in use

### ARC-123 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:207

- **Ruling:** The PS5 corner stands beside Kingdom Come Deliverance 2, an overcast town street; Jafar supplies the frame.
- **Checked:** production/reference/kcd2-town-arcades.jpg and kcd2-town-fountain.jpg - present ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:1282-1300, 1503 - the corner's shots from production/specs/ps5-corner.json ; CLAUDE.md 'THE GATE JUDGES AGAINST THE BAR' - KCD2 frames are the bar

### ARC-124 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:208

- **Ruling:** Canon: Tom has never been to the Hook; a stranger, known only as Mickey's nephew by name.
- **Checked:** canon.md:73-74 - the rule ; production/cast/cards/lena.md:30, rocco.md:32, sam.md:31 - 'Before he came to the Hook I had never met Mickey's nephew'
- **Inferred:** FINDINGS.md:265: the claim check does not read what a character says about Tom ('we've known each other a good while' passes), so enforcement in live talk rests on the prompt and cards

### ARC-125 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:209

- **Ruling:** The PS5 corner's scanned materials from Poly Haven CC0: brick_4, brick_wall_001, concrete_pavement_02, asphalt_01, painted_concrete_02.
- **Checked:** production/assets/scanned/polyhaven - the five, with materials.json ; production/specs/ps5-corner.json:351-401 - the corner uses them ; THIRD-PARTY.md:355 - 'Scanned materials — Poly Haven, CC0'
- **Inferred:** The playable street does not wear them (production/specs/vignette-pieces.json 'scanned' is empty); the ruling was for the corner only

### ARC-126 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:211

- **Ruling:** Local models: router candidates downloaded, fresh held-out lines run, no training on paid answers; line-writing online by default, local writers tested blind.
- **Checked:** production/research/local-models/ - BRIEF, RESULTS, SUMMARY, heldout, runs ; DECISIONS.md:12 - the paid router stays; local model a later option ; DECISIONS.md:33 - the local line-writing blind test run ; production/research/local-writers/README.md:50-62 - Jafar's picks recorded

### ARC-127 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:215

- **Ruling:** Platform: PC only, Windows.
- **Checked:** .github/workflows/ledger-probe-unreal.yml:456 - builds LedgerProbe Win64 ; CLAUDE.md 'Project facts' - PC only, Windows
- **Inferred:** No other platform target found

### ARC-128 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:216

- **Ruling:** Performance target: 60 fps at his monitor's resolution on the RX 6700, never below 30, with the voice running; the slice measures against it.
- **Missing:** No measurement since 24 September of the game at 3440x1440 with the voice running, after MetaHumans, shop interiors and cloth were added; no standing check against 60/30.
- **Impact to a player:** 3 (Unknown frame rate under the current visual bar; a drop would show as stutter in ordinary play.) · **belongs:** tools/route_walk.py or the AI tester's walk (log frame times with the voice on); a NOW.md line · **lane:** builder
- **Checked:** ROADMAP.md:33 - 73 fps at his screen size, 24 September (the last recorded measurement) ; ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:73-74, 557-569 - first launch tunes quality and render scale to a 16 ms frame ; grep 'fps/frame budget/16.6' in tools/route_walk.py, tools/ai-tester/*.py, tools/ci-checks.sh: no hit ; NOW.md, FINDINGS.md, FOR-JAFAR.md: no current frame-rate figure ; …
- **Inferred:** The first-launch tune measures at the title, without the street's load or the voice running

### ARC-129 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:217

- **Ruling:** The cast's voices checked for source and consent before more is recorded; the answer voice by voice in FOR-JAFAR.
- **Checked:** production/research/tts-licensing-and-consent/VOICE-PERMISSIONS-2026-09-24.md - present ; production/archive/FOR-JAFAR-to-2026-09-24.md:186 - 'there are 23, not 19... all 23 are CONDITIONAL' ; DECISIONS.md:13 - VCTK consent accepted as a stated risk

### ARC-130 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:218

- **Ruling:** The cost of an hour of conversation is measured from real calls, beside what it means for a released game, in FOR-JAFAR.
- **Checked:** production/archive/FOR-JAFAR-to-2026-09-24.md:194 - 'What an hour of talk costs, measured from 24 real calls' with a 30-hour playthrough ; production/playtest/talk-cost-2026-09-30-after.md:1-8 - US$2.14 an hour of steady talk, from the game's own talk program

### ARC-131 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:219

- **Ruling:** Yes to the downloads for Nano on the card (DirectML add-on and the older library) so it can be timed with the game running.
- **Checked:** tools/voice-live/voice-server.py:166-168 - imports torch_directml and loads Nano on the card ; FINDINGS.md:251 - Nano on the card measured (cloning aborts on DirectML; speech runs)

### ARC-132 · SUPERSEDED · production/archive/DECISIONS-to-2026-09-24.md:220

- **Ruling:** Downloads for Unreal from Epic's services go ahead without asking, each named in FOR-JAFAR with source and size.
- **Superseded by:** DECISIONS.md:19
- **Checked:** DECISIONS.md:19 - free content for Unreal (Fab, Epic or elsewhere) on the allowlist downloaded without asking, noted in the summary ; CLAUDE.md 'Talking to Jafar' - the same, wider rule

### ARC-133 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:221

- **Ruling:** Answers to the overnight decisions: MH_Test, MetaHuman files outside git, one timing job, 60 fps by upscaling, VCTK risk, allowlist wording, four voice picks.
- **Checked:** (1) DECISIONS.md:15 - MH_Test's dressing replaced by 'free Fab clothing only, or waits' (superseded part) ; (2) .github/workflows/ledger-probe-unreal.yml:341 - the build copies the MetaHuman in; DECISIONS.md:14 ; (4) ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:73-74, 557 - render scale 100/70/55% toward a 16 ms frame ; (6) DECISIONS.md:13 - VCTK consent as a stated risk ; …
- **Inferred:** (3) and (5) were one-off steps with nothing to find now

### ARC-134 · PARTLY **R** · production/archive/DECISIONS-to-2026-09-24.md:222

- **Ruling:** Three router changes: worked examples for the paid router, typed orders answered as refusals, the game's block widened to plain-word orders.
- **Missing:** The router is not on the game's talk path (TalkHelper never calls it), so the changes exist only in Core and the legacy Unity build; ROADMAP.md:40-42 is stale.
- **Impact to a player:** 2 (A typed order or an attempt to steer the model meets only the claim check and content rule; rarely tried.) · **belongs:** ledger/TalkHelper/Program.cs (route typed lines through IntentRouter), or a ruling that the router is retired · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/RouterExamples.cs and IntentRouter.cs:432-495 - examples and the PlainOrder block, in Core ; DECISIONS.md:22 - recorded as done in RouterExamples.cs ; grep 'IntentRouter/RouterExamples' in ledger/TalkHelper/Program.cs and ue-probe/Source: no hit; the only callers are Core/Director.cs and legacy Game/IntentBridge.cs ; ROADMAP.md:40-42 - still lists 'The router changes on the list' as work
- **Inferred:** The live talk sends the player's typed line straight to the conversation engine, so none of the three changes acts in the game
- **Reviewer:** grep 'IntentRouter/.Route(' in ledger/TalkHelper and ledger/Relay source: no hit; the game's talk never calls the router

### ARC-135 · LISTED · production/archive/DECISIONS-to-2026-09-24.md:223

- **Ruling:** Working business direction: sold once, a talk allowance counted on our server, own-key mode later; AI01-AI04, L01, AI05-AI08 recorded.
- **Missing:** The relay in use (friends' build runs without it by his 1 October ruling), Steam's safeguards description, a players' own-key mode.
- **On a list:** ROADMAP.md:48-51 - 'Before anyone outside his friends plays ... every live AI call through a server of ours ..., a notice ..., a way to report bad output, Steam's safeguards description, and the content rule enforced on everything said live.'
- **Checked:** ledger/Relay - the relay built (DECISIONS.md:56), not hosted (DECISIONS.md:65) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2927, 2992-3045, 4941 - the AI notice card and report label shown in the game ; ledger/Assets/Scripts/Core/SafetyRule.cs and ContentRule.cs - content rule on live lines (DECISIONS.md:58) ; DECISIONS.md:33 - L01 blind test run ; …
- **Inferred:** The players' own-key mode is a stated direction, not one of the ruled requirements, and is on no list

### ARC-136 · BUILT · production/archive/DECISIONS-to-2026-09-24.md:224

- **Ruling:** Answers to the morning's decisions: MH_Test from free Fab clothes, the town's unprompted lines written ahead, one runner cleanup, backup to Dropbox, housekeeping.
- **Checked:** (1) DECISIONS.md:15 - recorded; later superseded by DECISIONS.md:211 (Epic's plainest garments) ; (2) ue-probe/Source/LedgerProbe/Public/OwnLines.h and StreetVoice.h - the street's unprompted lines are written banks; DECISIONS.md:11 ; (3) DECISIONS.md:60 - the runner's copy cleaned; deletion now governed by CLAUDE.md 'Disk' ; (4) tools/backup-to-dropbox.py and tools/hooks/post-commit:4-7 - backup to his Dropbox ; …

### ARC-137 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:225

- **Ruling:** Jafar's voice picks: Aldous p226, Danny p243, June p277, Zlata p280; the new three to be cast in the game later.
- **Missing:** Danny p243 and June p277 never cast (clips, keys, attribution); both sheets now flag the picks as wrong for age or accent, with no list item to recast them.
- **Impact to a player:** 2 (Neither speaks in the game yet; it matters when they do.) · **belongs:** game-design/picked-clips and the voice keys; a NOW.md voices line or a page for Jafar · **lane:** builder
- **Checked:** production/casting/geoffrey-agar/SHEET.md:18, danny-cammack/SHEET.md:17, june/SHEET.md:19 - picks recorded on the sheets ; game-design/picked-clips - aldous.p226.wav (matches), but danny.p254.wav, june.p225.wav, zlata.p233.wav (the old voices, not the picks) ; grep 'p243/p277/p280' in production/specs, content, ue-probe/Source, tools/voice-live: no hit ; production/casting/june/SHEET.md:19 - 'Needs an older voice'; danny-cammack/SHEET.md:17 - 'the accent is not' right ; …
- **Inferred:** Danny and June are not talking characters yet, so no player hears the wrong voice today

### ARC-138 · PARTLY · production/archive/DECISIONS-to-2026-09-24.md:226

- **Ruling:** Voices sound flat: an experiment, cheapest first (per-line emotion, paralinguistic tags, livelier references, a more expressive source), with blind pages.
- **Missing:** Per-line emotion control from what the character feels and paralinguistic tags; the live voice speaks every line the same way, and no list item carries it.
- **Impact to a player:** 4 (Flat delivery is heard in every conversation; Jafar called Sheila's voice flat on 1 October.) · **belongs:** tools/voice-live/voice-server.py (direction per line from TalkHelper's mood); a NOW.md item · **lane:** builder
- **Checked:** DECISIONS.md:40 and production/casting/acting-key.json - acted references tested blind and adopted for Ron and Darren ; DECISIONS.md:35, 87 - VoxCPM2 tried for lines made in advance (kept for Ron only) ; grep 'exaggerat/emotion/mood' in tools/voice-live/voice-server.py and ledger/TalkHelper/Program.cs: no hit (no per-line emotion in live speech) ; ROADMAP.md - no VX01 line any more ; …

## canon.md

### CAN-001 · LISTED · canon.md:14

- **Ruling:** LEDGER is an open-town crime sim and social RPG, single player, PC first.
- **Missing:** The open town: the game is one street; the Hook and the wider town are roadmap stages.
- **On a list:** ROADMAP.md:64
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2560 - the one player deed is breaking a window (Fact player.broke_a_window); witness, gossip, police file and live talk built around it ; ue-probe/Source/LedgerProbe.Target.cs - a single Game target; no multiplayer or session code found ; production/assets/street/quay-street.json - the game builds one street (Quay Street), not a town ; ROADMAP.md:63-64 - stage 5 'The block becomes the Hook', stage 6 'Then the town.'
- **Inferred:** The crime-sim and social-RPG core and single-player PC are built; only the open-town scale is missing, and it is the roadmap's stages 5 and 6.

### CAN-002 · BUILT · canon.md:15

- **Ruling:** Third-person, never first-person; PC only, on Windows.
- **Checked:** ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp:63-71 - spring-arm boom 320 cm behind the player, camera on the boom ; ue-probe/Source/LedgerProbe/Private/LedgerCharacter.cpp:36-49 - default pawn also a 350 cm third-person boom ; tools/play/PLAY THE ENCOUNTER.bat:36 - the played build launches -LedgerSlice (the slice character) ; ue-probe/Config/DefaultEngine.ini:76 - Windows target settings; grep 'first.person/FirstPerson' in ue-probe/Source: only comments about first-person sentences

### CAN-003 · LISTED · canon.md:17

- **Ruling:** Town is Meridian, a fictional British port; one map, seven named districts.
- **Missing:** Six of the seven districts are not in the game (one street only); they wait on roadmap stage 6.
- **On a list:** ROADMAP.md:64
- **Checked:** ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:246 - dateline 'The Hook, Meridian', '1990' ; production/cast/cards/lena.md:27 - Quay Street in the Hook, the bridges across to Copper Row ; ledger/Assets/Scripts/Core/HookMap.cs:63,81,120 - Copper Row, Ironside, Gullwing places exist in the Core map only ; grep 'Ironside/Gullwing/the Exchange/Copper Row' in ue-probe/Source: no hit (Fairview once, in a test line) ; …
- **Inferred:** No contradiction found: only the Hook is in the game, and nothing names a district wrongly.

### CAN-004 · LISTED · canon.md:21

- **Ruling:** Streets minted: Quay Street, Weighhouse Lane, Tannery Row.
- **Missing:** Weighhouse Lane and Tannery Row are not in the game; they belong to the wider town (roadmap stage 6).
- **On a list:** ROADMAP.md:64
- **Checked:** production/assets/street/quay-street.json:2553 - the street's name plate 'plate_quay_street' in the live street ; ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp - 'Quay Street today.', 'Back on Quay Street' and others ; grep 'Weighhouse/Tannery Row' in ue-probe/Source: no hit ; ROADMAP.md:64 - 'Then the town.'
- **Inferred:** Quay Street is used as minted; the other two streets lie outside the one built street.

### CAN-005 · LISTED · canon.md:22

- **Ruling:** Quay Street is in the Hook, Weighhouse Lane in Copper Row, Tannery Row in Ironside.
- **Missing:** Weighhouse Lane (Copper Row) and Tannery Row (Ironside) are not in the game.
- **On a list:** ROADMAP.md:64
- **Checked:** ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:246 - 'The Hook, Meridian' over the Quay Street pages ; production/cast/cards/lena.md:27 - 'on Quay Street in the Hook' ; grep 'Weighhouse/Tannery' in ue-probe/Source and production/cast/cards: no hit
- **Inferred:** Quay Street's district is used and consistent; the other two are not reached by the one-street game.

### CAN-006 · BUILT · canon.md:25

- **Ruling:** The built street is Quay Street in the Hook, with Mickey's minicab office on it.
- **Checked:** production/assets/street/quay-street.json:2530-2554 - fascia 'fascia_mickeys_plain' and 'plate_quay_street' in the live street ; ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:246 - 'The Hook, Meridian' ; production/specs/vignette-scene.json:5 - street_identity 'Quay Street, in the Hook' ; grep 'East Parade' (capitalised) in ue-probe/Source, content, specs: no hit (east_parade_* stay asset ids)

### CAN-007 · BUILT · canon.md:33

- **Ruling:** Quay Street: east six-bay parade; west shops opposite its north half; west terraces opposite Mickey's.
- **Checked:** tools/art-recipes/terrace-front.py:806 - STREET_BLOCKS east_parade, west_south, west_north, east_chandler ; production/specs/vignette-scene.json:129,147 - west_north 'SHOPS, ruled by Jafar 2026-09-22' ; tools/art-recipes/terrace-front.py:1266-1268,4449 - west_south built as a domestic terrace elevation; west_north (x 24 to 42) carries the shopfronts ; tools/art-recipes/terrace-front.py:795-797 - Mickey's is east_parade bay 0 (the quay end)
- **Inferred:** west_south (to x 21) faces Mickey's at the quay end; west_north faces the parade's north half. Read from block extents, not walked.

### CAN-008 · LISTED · canon.md:41

- **Ruling:** Mickey's is a minicab office whose information room (fare book, radio, yard with two escapes, rank) is the business.
- **Missing:** The playable office interior (off by default, set aside); the overheard radio as a working source of information; the yard's two escapes lead nowhere; the brand bible and the Core's Acts II and III still describe Mickey's as a pub.
- **On a list:** NOW.md:27
- **Checked:** production/assets/street/quay-street.json:2541 - plain MICKEY'S fascia on the cab office ; ledger/Assets/Scripts/Core/StreetFacts.cs:45,61 - the will; drivers on the rank; a dispatcher on the radio and the phone (talk facts) ; production/cast/cards/lena.md:6,27 - the book of every fare; Ron keeps the rank and the yard gate ; production/specs/mickeys-office.json - blockout boxes 'the book of every fare', 'the radio', a yard with gate A and gate B, the lanes beyond 'not built' ; …
- **Inferred:** The overheard radio as a source of information exists nowhere in Core or game (grep 'radio' in Gossip and CastDay: nothing); it is only a 'use' box in the blockout. ; ActTwo and ActThree are Core-only (not ported, not run by TalkHelper), so their pub text does not reach the player today.

### CAN-009 · NOWHERE · canon.md:47

- **Ruling:** Graffiti tags minted: TANNER, SNIDE, GULL, QUAY FIRM (the Hook), PARADE RATS.
- **Missing:** No graffiti at all in the street; QUAY FIRM, the Hook's tag, is not on Quay Street; graffiti is named on no current list.
- **Impact to a player:** 2 (Polish: its absence reads as a clean wall, not a contradiction, but the Hook sheet bar wants wear and marks.) · **belongs:** NOW.md V4 (street dressing); tools/art-recipes street decals · **lane:** builder
- **Checked:** grep 'QUAY FIRM/graffiti/PARADE RATS/SNIDE/TANNER' in ue-probe/Source, production/assets/street/quay-street.json, the Core: no hit ; production/specs/vignette-scene.json:818 - G7_graffiti_tags 'twenty asked for and none generated yet' ; production/specs/vignette-bill-of-materials.json:987 - G7_graffiti_tags, in the bill of materials only ; NOW.md:14 - V4's street dressing names posters, signs, litter, stains and wear, not graffiti
- **Inferred:** The bill of materials is a spec, not a current work list.

### CAN-010 · LISTED · canon.md:54

- **Ruling:** Era: late 1980s to early 1990s, working window 1988 to 1992.
- **Missing:** What the player sees still breaks the window: 2020s clothes on the cast, out-of-period placeholder figures, props not yet 1990.
- **On a list:** NOW.md:19
- **Checked:** ue-probe/Source/LedgerProbe/Private/TitleScreen.cpp:246 - the paper's dateline '1990' ; ledger/Assets/Scripts/Core/RealWorld.cs:93 - talk prompt rule 'It is 1990: nobody has a mobile phone, the internet or email' ; NOW.md:34 - Jafar, 1 October: the cast's clothes 'read 2020s, slim jeans with contrast stitching and slip-on trainers' ; NOW.md:19 - V9 'Everyone in plain 1990 clothes, no contrast stitching and no trainers' ; …

### CAN-011 · NOWHERE · canon.md:55

- **Ruling:** Late-analog 1990: landlines, phone boxes, answering machines, pagers; CCTV only at the bank; one camcorder witness; no mobiles.
- **Missing:** CCTV at the bank (tape recycled weekly) and the one camcorder as a rare witness type exist nowhere, in Core or game; answering machines are absent; Jafar's second CCTV site is not on Needs you; Darren's pager is not yet worn.
- **Impact to a player:** 2 (Rare witness types on paths the one street does not yet have; the visible era props (kiosk, landline talk) are there.) · **belongs:** Core perception and witness types (ledger/Assets/Scripts/Core Perception/Observation), then the port; Jafar's second CCTV site on FOR-JAFAR.md Needs you · **lane:** town
- **Checked:** production/assets/street/clutter/kx100-kiosk.glb - a phone kiosk stands in the live street ; ledger/Assets/Scripts/Core/RealWorld.cs:93 - talk rule: no mobile phone, internet or email; 'there is the phone box' ; production/specs/garments.json:42-47 - Darren's pager fitted but held ('worn once his own T-shirt is fitted'); NOW.md:56 lists it ready to fit ; grep -i 'cctv/camcorder/videotape/security camera/answering machine/answerphone' in ledger/Assets/Scripts, ledger/TalkHelper, ue-probe/Source: no hit ; …
- **Inferred:** No bank stands on Quay Street, so CCTV's absence in play is not yet a contradiction; the camcorder is a ruled witness type that nothing implements.

### CAN-012 · BUILT · canon.md:60

- **Ruling:** Any 1950s or 1970s framing is wrong and corrected on sight.
- **Checked:** tools/canon-gate.py:102 - CORPUS_ROOTS content, ledger/Assets/Scripts, production/specs; run here: 'clean - 0 finding(s) in 255 file(s) ... 13 era term(s)' ; tools/ci-checks.sh:153 - canon-gate --corpus runs in CI ; ledger/Assets/Scripts/Core/RealWorld.cs:93 - the talk prompt fixes the year at 1990
- **Inferred:** The era gate does not read production/cast/cards (the talk cards) or ue-probe/Source strings; the cards were read by hand here and carry no 1950s or 1970s framing.

### CAN-013 · PARTLY · canon.md:63

- **Ruling:** Tone: grounded noir, dry British wit and sparing seaside smut; never GTA-style American satire.
- **Missing:** The D7 calibrated tone judge; any register rule or check on live replies (never American, the comic register).
- **Impact to a player:** 2 (No tone failure was found; the gap is that nothing measures tone in the live talk the player hears.) · **belongs:** ledger/Assets/Scripts/Core/ConversationEngine.cs prompt rules; a D7 judge tool · **lane:** town
- **Checked:** production/cast/cards/lena.md:12-17, rocco.md, sam.md - speech style and sample lines carry the register ; TOWN.md:42-53 - the street's own lines passed a fresh reviewer and Jafar's yes ; legacy/studio-v2/respec/decision-register/D7-verification-model.md:4 - a calibrated tone judge (80 percent agreement) was ruled ; ls tools / grep judge: none; tools/dialogue-verify.py:7 'Tone is deliberately absent: it belongs to the D7 judge' ; …
- **Inferred:** Canon says tone is 'the judge's under D7, not a gate'; that judge was never built, and the live replies (most of what the player hears) carry no register rule beyond the cards.

### CAN-014 · LISTED · canon.md:65

- **Ruling:** Visual target photoreal, wet, overcast, grimy Britain; weather and grime are the strategy.
- **Missing:** The wear layer above a floor (D53); falling rain and changing weather (the settings label promises rain and steam that do not exist).
- **On a list:** NOW.md:14
- **Checked:** ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:48-49,1053-1058 - ground Wetness driven per condition ; ue-probe/Source/LedgerProbe/Private/VignetteShot.cpp:7354-7409 - stains stood as deferred decals with M_LedgerGrime ; grep -i 'rain/weather/Niagara' in ue-probe/Source: rain only as a wetness scalar (SurfaceBind.h:729-743), in spoken lines, and in the settings label 'Effects: Rain, steam and the glow round the lamps' (LedgerSettings.cpp:135); grep 'ParticleSystem/NiagaraComponent/SpawnEmitter' in ue-probe/Source: no hit, so no falling rain, steam or weather change ; legacy/studio-v2/respec/decision-register/D53-grime-is-the-strategy-and-a-surface-carries-wear-above-a-floor.md - wear above a measured floor on every surface ; …
- **Inferred:** D53's per-surface wear layer is still not built (as the brief notes); V4 is its only list line. ; The settings page offers an 'Effects' quality for rain and steam that the game does not have.

### CAN-015 · PARTLY · canon.md:70

- **Ruling:** Tom Nowak, 32, Mickey's nephew, inherits the cab office and debts; a stranger; his past is never asked or told.
- **Missing:** Nothing stops a character asking about his life before the Hook; the book of uncollectable debts is absent; the arrival with the suitcase and the letter is not shown (listed for later).
- **Impact to a player:** 3 (A character asking where he came from breaks a ruled premise in ordinary talk; the debts are missing from the inheritance.) · **belongs:** ledger/Assets/Scripts/Core/ConversationEngine.cs prompt rules; StreetFacts.cs · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/Suggest.cs:65-68 - Tom 32, the new owner, 'a stranger here and never says where he grew up or what he did before' ; ledger/Assets/Scripts/Core/StreetFacts.cs:45 - 'the new owner came with one suitcase and a letter saying so' (a talk fact) ; production/cast/cards/lena.md:30 - 'Before he came to the Hook I had never met Mickey's nephew' ; ue-probe/Source/LedgerProbe/Public/WeeksEnd.h:5-12 - the inherited outfit's arrangement and Sheila's wind-down or take-over question ; …
- **Inferred:** The suggested-lines panel stays dark until Jafar's yes (NOW.md:50) and the player types freely, so 'he never tells' rests on the player.

### CAN-016 · BUILT · canon.md:77

- **Ruling:** Inherited loyalists: Ron Kirby, 58, docker until 1989; Sheila Dunn, 53, at Mickey's since 22.
- **Checked:** production/cast/cards/rocco.md:1,6 - Ron Kirby, a docker 'until the dock labour scheme ended in 1989', kept on for the door and the rank ; production/cast/cards/lena.md:1,6 - Sheila Dunn, the bookkeeper for thirty-one years (53 less 22) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5627-5629 - on-screen names Sheila, Ron, Darren ; FINDINGS.md:24 - Mickey's past disagrees with itself (Sheila there from 1959, before minicab offices existed)
- **Inferred:** The 1959 start is a canon-against-history tension already on FINDINGS for Jafar; content/brands/brand-bible-v1.json:89 also has Mickey's 'founded 1962', after Sheila's start.

### CAN-017 · PARTLY · canon.md:80

- **Ruling:** Three rival organisations: Agar's old-money machine, Jensen's dockside syndicate, Cammack's new crew.
- **Missing:** The rivals exist only in the C# Core's Act II; nothing of them reaches the game or the talk program, and no list carries them.
- **Impact to a player:** 3 (A longer session never meets the premise's antagonists; the first week does not need them.) · **belongs:** ledger/Assets/Scripts/Core/ActTwo.cs reworded, then ported to ue-probe; TOWN.md · **lane:** town
- **Checked:** ledger/Assets/Scripts/Core/ActTwo.cs:51-107 - the three arms by canon's names (Core only) ; grep 'Agar/Jensen/Cammack/Widow' in ue-probe/Source, production/specs/hook-cast.json, StreetFacts.cs, production/cast/cards: no hit ; grep 'ActTwo/Empire/Campaign' in ledger/TalkHelper/Program.cs: no hit ; production/casting/CASTING.md:66-68 - casting sheets exist ; …
- **Inferred:** ActTwo.cs still frames Mickey's as a bar ('the bar's takings'), so porting it as it stands would break D19.

### CAN-018 · PARTLY · canon.md:83

- **Ruling:** DS Carol Ellis and the day-life ring: Darren, Ada, June Suddaby, Father Walsh, Alison Sedman, Philip Danby, Keith Garbutt.
- **Missing:** Philip Danby and Keith Garbutt are not in the game or the talk; Ada has no card.
- **Impact to a player:** 2 (Two ring members are absent in the first week; nothing contradicts the names that do appear.) · **belongs:** production/specs/hook-cast.json and production/cast/cards · **lane:** town
- **Checked:** production/specs/hook-cast.json - sam 'Darren Milner', ada 'Ada: the widow', june 'June', emil 'Father Walsh', noor 'Alison Sedman' ; ue-probe/Source/LedgerProbe - 'DS Ellis' in 16 places (the police file's visits) ; grep 'Danby/Garbutt/Fixer' in ue-probe/Source, hook-cast.json, StreetFacts.cs: no hit ; grep -i 'teacher/classroom' in ue-probe/Source and hook-cast.json: Ada is never a teacher ; …

### CAN-019 · BUILT · canon.md:88

- **Ruling:** The town calls him the new owner, Nowak, Tom, Tommy by knowing; Sheila withholds his name until trust.
- **Checked:** ledger/Assets/Scripts/Core/PlayerIdentity.cs:141-160 - Rung NewOwner, Surname, First, Diminutive; RungByKnowing gates on knowing ; ledger/TalkHelper/Program.cs:690-726 - the talk applies the ladder; Sheila kept at 'the new owner' until trust (Cast.NamesHimOnlyOnTrust) ; ledger/Assets/Scripts/Core/Trust.cs:29-49 - Sheila's trust is decided by the Core ; content/dialogue/crime-witness-v1.json - the rung-4 lines say 'the new owner', never 'Nowak' (N2 fixed) ; …
- **Inferred:** The game never sends 'trusts' to the talk; it relies on the talk program's own TrustEarned, restored from its save (ConversationEngine.cs:1289).

### CAN-020 · BUILT · canon.md:92

- **Ruling:** Renames: the old names (Lena, Rocco, Sam, Novak, Emil and the rest) are ids only, never seen or heard.
- **Checked:** tools/names-gate.py run here: 'files=216 retired-names=0'; in CI (tools/ci-checks.sh:165) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:5627-5629,7968 - subtitles name Sheila, Darren, Ron ; production/specs/hook-cast.json - emil shown as 'Father Walsh' ; tools/names-gate.py:39-42 - the RETIRED list lacks 'Emil' (renamed 28 September) ; …
- **Inferred:** The gate would pass a 'Father Emil' line anywhere it reads; none is in what the game reads today.

### CAN-021 · PARTLY · canon.md:109

- **Ruling:** No alcohol or gambling, shown or spoken; pubs may exist as places. Enforced at six sites.
- **Missing:** Two of the six sites do not reach the game: the word gate skips the talk cards and the game's own strings, and the animation check skips Unreal's clips (V6 will add Epic's). The brand bible is stale, and a back-bar picture is still placed in the fallback street spec.
- **Impact to a player:** 2 (No violation was found in what the player meets; the gaps are in what the checks read.) · **belongs:** tools/content-gate.py corpus and clip roots (Unreal content); production/specs/vignette-pieces.json; content/brands/brand-bible-v1.json · **lane:** builder
- **Checked:** tools/content-gate.py run here: hitsNew=0 over 9374 strings, clipsExamined=68 ; ledger/Assets/Scripts/Core/ConversationEngine.cs:548 and ResponseValidator.cs:73 - live replies are told the rule and checked against it (ContentRule.SpeechBreaks) ; grep for alcohol and gambling words over OwnLines.h, StreetVoice.h, TownNews.h, the cards and the Core's spoken text: clean ; tools/content-gate.py:795-823 - the speech corpus is content/dialogue, game-design barks and tier2; not production/cast/cards, ue-probe strings or the Core's spoken text ; …
- **Inferred:** The fallback street is drawn only when quay-street.json is not found, and tools/ue/stage_game_data.py stages only the live street's pictures, so the bar picture is unlikely to reach a player.

### CAN-022 · BUILT · canon.md:112

- **Ruling:** Tobacco stays.
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:548 - offered a drink, turn it to 'a tea, a smoke' ; content/brands/brand-bible-v1.json:12 - 'TOBACCO IS ALLOWED' ; ledger/Assets/Scripts/Core/ContentWords.cs - rule groups alcohol, gambling, children, cruelty, drugs, sex, slur; none for tobacco

### CAN-023 · PARTLY · canon.md:113

- **Ruling:** Violence stays, with blood and light gore; no torture or cruelty as spectacle.
- **Missing:** No violence in the game: Combat and Arsenal are Core-only, not ported, and on no list.
- **Impact to a player:** 3 (A crime sim whose canon keeps violence offers none; a player who tries it finds nothing.) · **belongs:** a ue-probe port of Core Combat/Arsenal (D56's owed verbs) · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/Combat.cs, Arsenal.cs - violence exists in the Core ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:388,420 - 'needs Arsenal and Weapon, neither of which is ported' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2560 - the only player deed is the broken window; the key bindings hold no attack ; FINDINGS.md:22 - 'a wounding, a robbery, a killing, which the game does not have yet' ; …
- **Inferred:** No list item builds violence; TOWN.md says 'still no new systems'.

### CAN-024 · PARTLY · canon.md:115

- **Ruling:** Killing is possible, rare, permanent, and the town remembers it forever.
- **Missing:** Killing is not possible in the game; Homicide is Core-only and unported, and no list builds it.
- **Impact to a player:** 3 (Canon says killing is possible; the game cannot do it on any path.) · **belongs:** a ue-probe port of Core Homicide.cs · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/Homicide.cs - killing in the Core ; ue-probe/Source/LedgerProbe/Public/PoliceFile.h:46 - Offence::Killing exists in the port's police file, but grep 'Offence::Killing' in CrimeProbe.cpp: no player path ; FINDINGS.md:22 - the game has no killing yet ; NOW.md:52 - town items wait 'once paying, threatening and killing exist' (conditional, not a work item) ; …

### CAN-025 · BUILT · canon.md:116

- **Ruling:** Full period swearing allowed; no slurs of any kind.
- **Checked:** content/rules/slurs-v1.json - closed slur list read by tools/content-gate.py (slurs=40) ; ledger/Assets/Scripts/Core/ContentWords.cs:113 - the slur rule applied to live replies through ResponseValidator.cs:73 ; ledger/Assets/Scripts/Core/ContentWords.cs - no swearing rule (swearing allowed)

### CAN-026 · BUILT · canon.md:117

- **Ruling:** Drugs only as an off-screen economy others run: never shown, used, or a player verb.
- **Checked:** ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp, CrimeProbe.cpp - the player's keys: move, run, talk, Enter, Escape, Tab; no drug verb ; tools/content-gate.py:447-450 - drug use refused, the trade vocabulary kept ; ledger/Assets/Scripts/Core/ContentWords.cs - two drug rules on live replies ; grep -i 'drug/heroin/cannabis' in OwnLines.h, StreetVoice.h, the cards, StreetFacts.cs: no hit

### CAN-027 · BUILT · canon.md:119

- **Ruling:** No prostitution or sexual content; seaside-postcard innuendo stays.
- **Checked:** ledger/Assets/Scripts/Core/ContentWords.cs - two 'sex' rules on live replies ; tools/content-gate.py - the speech rules include sexual content (rulesSpeech=88)

### CAN-028 · BUILT · canon.md:121

- **Ruling:** No children anywhere; the school stands closed and empty.
- **Checked:** ledger/Assets/Scripts/Core/ConversationEngine.cs:548 - 'there are no children ... Never mention ... children' ; ledger/Assets/Scripts/Core/ContentWords.cs - nine children rules on live replies ; tools/ue/import_figure.py:28,888 - figures checked adult ; production/specs/street-people.json and hook-cast.json - fixed adult people; no crowd generator in ue-probe ; …

### CAN-029 · BUILT · canon.md:124

- **Ruling:** Racism and sectarianism only as facts about characters; never slurs, never rewarded.
- **Checked:** ledger/Assets/Scripts/Core/ContentWords.cs:113 - slurs refused in live replies ; content/rules/slurs-v1.json - the gate's list ; grep -i 'racis/sectarian' in ue-probe/Source: no mechanic that rewards it

### CAN-030 · BUILT · canon.md:126

- **Ruling:** Religion present as part of life, never mocked, never a mechanic.
- **Checked:** production/specs/hook-cast.json - Father Walsh (mass, the presbytery), his housekeeper, the chapel cleaner ; ledger/Assets/Scripts/Core/StreetFacts.cs:48 - Mickey's funeral at Father Walsh's chapel ; TOWN.md:47-50 - Father Walsh's street lines passed a fresh review ; grep 'Walsh/chapel/mass' in ue-probe/Source game logic: no religious mechanic

### CAN-031 · PARTLY · canon.md:127

- **Ruling:** Police are corruptible as individuals, never as a thesis.
- **Missing:** No individual officer can be corrupted in the game; the Core's bribe and hook are unported.
- **Impact to a player:** 2 (A specific path: a player trying to buy off DS Ellis finds no way to.) · **belongs:** ue-probe/Source/LedgerProbe/Public/Gossip.h (port Bribe and UseHook) and the police file · **lane:** builder
- **Checked:** ledger/Assets/Scripts/Core/Gossip.cs:1019,1160 - Bribe and UseHook exist in the Core ; ue-probe/Source/LedgerProbe/Public/Gossip.h:31-34 - 'OUT OF SCOPE AND NOT HERE: ... Bribe, Intimidate, Discredit, UseHook' ; grep -i 'bribe/corrupt' in ue-probe/Source game logic: comments only; no way to corrupt DS Ellis or a constable
- **Inferred:** Whether the Core's Bribe and UseHook can target a police officer was not traced.

### CAN-032 · BUILT · canon.md:142

- **Ruling:** Every act exposes seven perceivable slots.
- **Checked:** ue-probe/Source/LedgerProbe/Public/Observation.h:45-63 - Precursor, Draw, Act, Victim, Actor, Flight, Aftermath ; ue-probe/Source/LedgerProbe/Public/Observation.h:285-327 - each slot filled by its own test ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:518 - live witnessing calls Observe::Resolve

### CAN-033 · BUILT · canon.md:143

- **Ruling:** Five-rung identification ladder; recognition gated by relationship, not by distance or light alone.
- **Checked:** ue-probe/Source/LedgerProbe/Private/Perception.cpp:45-57 - IdRung 0 to 4; rung 4 needs Familiarity >= RecognitionFamiliarity ; production/audits/review-2026-10-01/FAULTS.md:35 - familiarity from meetings (FamiliarityFromMeetings), kept in the save ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2775 - the live flight sighting uses IdRung with the witness's familiarity
- **Inferred:** Some live paths (CrimeProbe.cpp:2774-2794, the flight sighting) still use the constant overcast-day light kLightLevel=1.0 at any hour; the main witness path measures light (CrimeProbe.cpp:6558).

### CAN-034 · BUILT · canon.md:145

- **Ruling:** Permanent per-NPC memory; nothing is ever wiped.
- **Checked:** ue-probe/Source/LedgerProbe/Public/MemoryStore.h:465-472 - MaxEvents and PruneTo removed; 'NOTHING IS EVER WIPED' ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:7255-7281 - every person's memory saved to memory-<id>.md ; ue-probe/Source/LedgerProbe/Public/Gossip.h:548-552 - KeepFirst only replaces a memory appended in the same call

### CAN-035 · BUILT · canon.md:146

- **Ruling:** Gossip spreads through schedule intersections.
- **Checked:** ue-probe/Source/LedgerProbe/Public/TownRounds.h:30-40 - whoever is together by their routines this hour talks ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:2402 - GTownHours.RunTo at each game hour

### CAN-036 · BUILT · canon.md:147

- **Ruling:** Live LLM conversations with per-character memory and local voice.
- **Checked:** ledger/TalkHelper/Program.cs - one ConversationEngine per character, saved with the game (CrimeProbe.cpp:7286-7289, the talk stamp) ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4500-4512 - each person's memories sent to the talk ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3224-3320 - the voice from a local server beside the game (tools/voice-live/voice-server.py)

### CAN-037 · BUILT · canon.md:148

- **Ruling:** The deterministic Core decides every outcome the player feels; LLMs classify, never adjudicate.
- **Checked:** ledger/Assets/Scripts/Core/Trust.cs:29-49 - Sheila's trust is a Core rule ; ledger/TalkHelper/Program.cs:930-949 - keeping quiet is decided by Silence.Agrees from the person's stance, not by the model ; ledger/TalkHelper/Program.cs:888-912 - Sheila's week answer read by WeeksEnd.Confirms, with fixed lines ; FINDINGS.md:10 - suspicion is decided by the C# Core in the talk program and by the port in the game, both deterministic
- **Inferred:** The model alone decides to end a conversation (ConversationEngine.cs, the DoneMark rule), and an ended turn counts toward trust: a small outcome the model adjudicates. ; FINDINGS.md:11 - live talk still invents details in about 7 percent of turns; these are words, not changes of state.

### CAN-038 · BUILT · canon.md:152

- **Ruling:** Not a sandbox, shooter, driving, economy or story-first game; what people know about you is the mechanic.
- **Checked:** ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp, CrimeProbe.cpp - the player's keys: walk, run, talk, Enter, pause; no shooting or driving ; production/specs/street-vehicles.json - two parked cars only ; ue-probe/Source/LedgerProbe/Public/Perception.h, Gossip.h, MemoryStore.h - perception, gossip and memory drive play

### CAN-039 · CONDUCT · canon.md:155

- **Ruling:** Smallest budget for what does not feed perception, memory, gossip or consequence; nothing may look broken.
- **Checked:** canon.md:155-158 - a spend rule on how effort is allotted; it names no artefact
- **Inferred:** Its 'must not look broken' half is checked in practice by NOW.md:12 (V2, the cars and props).

### CAN-040 · BUILT · canon.md:161

- **Ruling:** All brands, bands, clubs, products, weapons and vehicles fictional; no real people, voices, logos; the allowlist is law.
- **Checked:** ledger/Assets/Scripts/Core/RealWorld.cs:93 - the talk prompt's rule against any real make, brand, club, paper, programme or person; ConversationEngine.cs:1752 redrafts a reply naming one ; production/specs/street-vehicles.json - cars built by tools/art-recipes/car-model.py, 'no recognisable real car model' ; tools/canon-gate.py run here: 45 brand tokens screened, clean ; DECISIONS.md:13 - the VCTK voices ruled not 'real voices' (identifiable people only) ; …
- **Inferred:** The brand gate (canon-gate) does not read the talk cards or ue-probe strings; read by hand, they name no real brand.

### CAN-041 · NOWHERE **R** · canon.md:163

- **Ruling:** Minted: Mickey's, the Tivoli, Harbour Board, Ferry. Owed: club, paper, pirate radio, regional TV, kiosk mark, postal cypher.
- **Missing:** The telephone operator's mark and the postal cypher are unwritten; the four drafted brands were never minted; the brand bible still calls Mickey's a pub; none of this is on a list.
- **Impact to a player:** 3 (The unlettered kiosk and pillar box stand in the one street every player walks.) · **belongs:** content/brands/brand-bible-v1.json, then the kiosk and pillar box recipes; a mint for Jafar · **lane:** town
- **Checked:** content/brands/brand-bible-v1.json - drafts Meridian Town AFC, the Meridian Argus, Radio Tideline, Coastway Television; canon still lists them as owed, and nothing mints them (grep 'Argus/Tideline/Coastway' in DECISIONS.md and canon.md: no hit) ; content/brands/brand-bible-v1.json:86-89 - Mickey's entry: kind 'pub', founded 1962 ; ledger/Assets/Scripts/Core/StreetVignette.cs:1314-1317 - the kiosk 'ships unlettered' because the operator 'has not been written' ; tools/art-recipes/terrace-front.py:483-494 - the live kx100 kiosk and pillar box in plain materials, no mark or cypher ; …
- **Inferred:** NOW.md:12 (V2: the phone box looks like a real 1990 one) may need the operator's mark but does not name it.
- **Reviewer:** content/brands/brand-bible-v1.json:11 'MICKEY'S IS A PUB AND STAYS A PUB', :88-89 kind 'pub', founded 1962; no kiosk mark or postal cypher in the brand bible

### CAN-042 · BUILT · canon.md:170

- **Ruling:** Engine is Unreal; Unity is the legacy reference; the C# Core is the truth the port is checked against.
- **Checked:** ue-probe/LedgerProbe.uproject - EngineAssociation 5.8 ; tools/port-golden-check.sh:1-17 - regenerates the golden table from the C# Core and compares the port ; tools/ci-checks.sh:184 - perception-golden runs in CI

### CAN-043 · PARTLY · canon.md:174

- **Ruling:** The story outline of 28 September is the baseline: Tom, three acts, three rivals, the empire roster.
- **Missing:** Acts II and III, the rivals and the empire roster are Core-only and unported (Acts II and III still read Mickey's as a pub); Ada's card is unwritten.
- **Impact to a player:** 3 (Past the first week there is no story; a long session meets nothing of Acts II and III.) · **belongs:** Core ActTwo/ActThree/Empire reworded, then ported; TOWN.md · **lane:** town
- **Checked:** game-design/story-outline-2026-09-28.md:35-47 - Act I's threads; ue-probe has Arrangement.h (the outfit's ask), WeeksEnd.h (Sheila's question), FirstWeek.h (Ada's tea), PoliceFile.h (Ellis) ; ledger/Assets/Scripts/Core/ActTwo.cs, ActThree.cs, Empire.cs - Acts II and III and the empire in the Core only; grep in ue-probe/Source and TalkHelper: no hit ; game-design/story-outline-2026-09-28.md:102-107 - 'Act III's text in the Core still reads as a pub' (owed, in a design document only) ; production/cast/cards - no Ada card: the Sam and Ada mismatch canon leaves to the cards is unsettled
- **Inferred:** The story outline is a design document, not a work list; no current list carries Act II, Act III or the empire.

## Rulings in CLAUDE.md, ROADMAP.md, NOW.md, TOWN.md and CLOTHES.md

### OTH-001 · BUILT · CLAUDE.md:22

- **Ruling:** Free allowlisted Unreal content: download it, note it in the summary, never ask.
- **Checked:** ledger-v2/research/license-allowlist.md:5 - Fab Standard License and CC0 libraries on the allowlist ; ledger-v2/research/license-allowlist.md:11 - Epic's free Unreal-only animation content allowed; 'each pack's own licence ... named in THIRD-PARTY.md' ; tools/ue/import_fab_clothes.py:1-12 - imports Epic's free MetaHuman clothing from Fab by script ; grep -i 'fab/epic/metahuman/poly haven/makehuman/unreal' THIRD-PARTY.md: no hit (only fonts, VCTK, Mixamo, Kenney, Unity)
- **Inferred:** The rule itself is a permission; whether each download was noted in a summary cannot be checked from the repo. ; THIRD-PARTY.md has no entry for Epic's MetaHumans, Epic's outfit pieces the cast wears, or Fab content, which allowlist line 11 requires; a records gap rather than a gap in this ruling.

### OTH-002 · PARTLY · CLAUDE.md:27

- **Ruling:** NOW.md holds only GOAL, the builder's list, one state line and Handovers; short; done handovers leave.
- **Missing:** Done and superseded handovers have not left; the state line is stale and long; list items carry history.
- **Impact to a player:** 1 (Records only; a stale state line and dead handovers can mislead the sessions, not players.) · **belongs:** NOW.md (builder keeps it) · **lane:** builder
- **Checked:** NOW.md:1 - GOAL line present ; NOW.md:3-29 - builder's list with [ ]/[x] ; NOW.md:29 - STATE is one ~400-word paragraph stamped 'Thursday 1 October, 11:50' and says '1b ready for Jafar's cloud review', contradicting NOW.md:8 (1b reopened that evening) ; wc -w NOW.md: 3379 words ; …
- **Inferred:** No tool or check enforces NOW.md's shape or length (grep NOW.md in tools/ci-checks.sh and tools/*.py: no hit).

### OTH-003 · PARTLY · CLAUDE.md:28

- **Ruling:** Every handover names the exact asset version it fits; the receiver checks it is current before fitting.
- **Missing:** No mechanised receiver check (garments.json has no made-on field; import_garments.py does not compare versions); NOW.md:39 contradicts NOW.md:37 on Sheila's body version.
- **Impact to a player:** 2 (A garment fitted to a replaced body shows on a principal (spectacles sat 2-3 cm high); caught by eye so far.) · **belongs:** production/specs/garments.json (a made-on field) and tools/ue/import_garments.py (refuse a mismatch); NOW.md:39 · **lane:** builder
- **Checked:** NOW.md:34,35,37,38,54,55,56 - handovers name body versions (MH_RoccoP2, MH_LenaS4, MH_SamC5; 'as exported 29 September 17:33') ; NOW.md:39 - SUITS AND COATS handover says fit Sheila to 'MH_LenaC1's body under her MH_LenaS4 head', while NOW.md:37 in the same section says 'Sheila MH_LenaS4 (... the C1 export is superseded)' ; production/specs/garments.json - entries carry who/name/fbx/handed only; no field naming the body version a garment was made on ; tools/ue/import_garments.py:36 - BODY = {Rocco: MH_RoccoP2, Lena: MH_LenaS4, Sam: MH_SamC5}, fixed; no check of the version a garment was made against ; …
- **Inferred:** The bodies README and garment.json files on F: may record versions; they are not in the repository.

### OTH-004 · PARTLY · CLAUDE.md:29

- **Ruling:** Every number in the overview comes from the real path or says plainly it does not.
- **Missing:** The 4.5 s first-sound figure and the 23-of-60 count are not marked as off the real path.
- **Impact to a player:** 1 (Records only: it misleads Jafar's judgement of the delay, not the players.) · **belongs:** FOR-JAFAR.md overview, Road to worth playing · **lane:** builder
- **Checked:** FOR-JAFAR.md:22 - 'the first sound is about 4.5 s after Enter' is derived (words 1.9 s plus voice work 2.98 s), not measured on the real path, and is not marked as an estimate ; NOW.md:7 - the real-path measurement was first sound 5.4 s median (production/playtest/real-talk-2026-09-30.md) ; production/research/voice-latency/STREAMING-IN-GAME-2026-10-01.md:27 - 2.98 s is voice work alone beside the game ; FOR-JAFAR.md:23 - '23 of 60' from the town's bench run, not labelled as off the real path ; …
- **Inferred:** Whether the town's 23-of-60 run used the game's real talk path is not stated anywhere I found; read as a bench run from TOWN.md:33-43.

### OTH-005 · PARTLY · CLAUDE.md:30

- **Ruling:** One dated summary a day per session by 07:00, under 200 words, page first, C: before/after, research lines; nothing settled asked.
- **Missing:** Clothing's summary still asks a settled scope question; an old 26 September summary stays in the file; the town's summary has no backup line.
- **Impact to a player:** 1 (Records only: Jafar may be asked something he already ruled on.) · **belongs:** FOR-JAFAR.md (Clothes section; the leftover 26 September block) · **lane:** clothing
- **Checked:** FOR-JAFAR.md:34-54 Town 2 October - 198 words, page linked first, C: 63 then 47 GB; no backup line ; FOR-JAFAR.md:69-92 Builder 1 October - 193 words, page first, C: 64.9 then 67.8 GB, research lines, backup line ; FOR-JAFAR.md:55-68 Clothes 1 October - 183 words, 'Written 30 September, 16:00'; still asks 'Needs you (scope) ... (A) ... (B) ... (C) a paid Fab jacket' ; DECISIONS.md:211,216 - Jafar settled clothing on 1 October (blocked capability; the Marvelous proof), so the Clothes summary asks a settled question ; …
- **Inferred:** The town's 2 October summary was written at 21:15 on 1 October, ten hours early, so it cannot cover the night.

### OTH-006 · BUILT · CLAUDE.md:31

- **Ruling:** Overview first in FOR-JAFAR, builder only: Needs you (at most five, linked, recommended) and Road to worth playing.
- **Checked:** FOR-JAFAR.md:8-33 - overview first, two parts only: '### Needs you' (3 items) and '### Road to worth playing' ; FOR-JAFAR.md:18-33 - Road lines for faces, people dressed, the delay, replies that time out, the route, and the AI tester, each with owner and 'Since ...' ; git show 99559a6 - the town's commit changes only its own section
- **Inferred:** Needs-you item 2 (clothing blocked) has no page or recommendation, as OTH-014 allows; it went stale at 21:28 when DECISIONS.md:216 settled the Marvelous proof (overview stamped 20:20). ; No separate line for 'the first week wired into the game'; read as covered by the route line (FOR-JAFAR.md:20). ; FOR-JAFAR.md:19 Road intro still quotes the 30 September order, not NOW.md:5's order of 1 October.

### OTH-007 · BUILT · CLAUDE.md:32

- **Ruling:** Read each page's stored picks (verdicts/<key>) before every summary and Needs-you entry.
- **Checked:** tools/cleanup.py page JS - save() writes db.doc('verdicts/'+key) and reads it back on load ; grep 'verdicts/' in tools: town_page.py, cleanup.py, approval_page.py, ingame_page.py, town_day_page.py, day_page.py, candidate_page.py, weekend_page.py ; production/approvals/town-answered.json - the town's record of answered keys ; FOR-JAFAR.md:12 - 'Every page's stored answers checked at 20:15'
- **Inferred:** The reads happen through the artifact store (ArtifactData), so whether they took place cannot be seen in the repo; the dated line is the session's own claim.

### OTH-008 · PARTLY · CLAUDE.md:39

- **Ruling:** Disk section: delete only inside the fixed list after his page; large files recorded and swept daily; C: reported.
- **Missing:** The end-of-day sweep of my own rejected and superseded entries is not happening (101 entries, about 32 GB, outstanding).
- **Impact to a player:** 1 (Disk housekeeping, invisible to players; C: is below 60 GB.) · **belongs:** tools/large_files.py sweep plus tools/cleanup.py sweep-record, run at each day's end · **lane:** builder
- **Checked:** tools/cleanup.py:44-77 - ALLOWED and PROTECTED lists; allowed() refuses outside; delete_group() refuses unless verdicts.json says yes ; tools/cleanup.py selftest - Documents, Desktop, Downloads, Dropbox refused ; tools/large_files.py - record tool; production/large-files.json holds 180 entries ; production/large-files.json - 101 entries still 'rejected' or 'superseded' (about 32 GB), recorded 26 Sep (17), 28 Sep (45), 29 Sep (6), 30 Sep (16), 1 Oct (17); none marked deleted since ; …
- **Inferred:** Whether those 101 entries are still on disk cannot be checked here; the record does not mark them deleted, so the daily sweep looks not done since 26 September.

### OTH-009 · PARTLY · CLAUDE.md:41

- **Ruling:** Deletion only inside the fixed list, after an approved cleanup page; nothing of his touched.
- **Missing:** cleanup.py allows all of production/playtest, including tracked records, where the ruling allows only gitignored render and scratch output.
- **Impact to a player:** 1 (Tooling: tracked records could be deleted locally (git still holds them); players never see it.) · **belongs:** tools/cleanup.py ALLOWED (narrow to production/playtest/ai-tester) · **lane:** builder
- **Checked:** tools/cleanup.py:44-56 - ALLOWED includes the old copies, ue-probe Intermediate/Saved/Packaged/DerivedDataCache, C:\LedgerTools, the runner's _work, UnrealEngine\Common, .claude/worktrees ; tools/cleanup.py:49 - ALLOWED also includes the whole of production/playtest; .gitignore:143 ignores only production/playtest/ai-tester/, and git ls-files shows 15 tracked files there (e.g. real-talk-2026-09-30.md, the measuring run's evidence) ; tools/cleanup.py:136-145 - F:\LedgerTools limited to the large-file record's own rejects; the folder itself refused ; tools/cleanup.py:208-225 - delete_group refuses a group not approved on the page ; …
- **Inferred:** The .NET bin/obj folders named in the ruling are absent from ALLOWED; narrower, so harmless.

### OTH-010 · PARTLY · CLAUDE.md:47

- **Ruling:** The week: one goal; list in order; daily summary with an action, then backup via hook, its line, record swept.
- **Missing:** The large-file record is not swept daily; the town's summary omits the backup line.
- **Impact to a player:** 1 (Process and housekeeping only.) · **belongs:** each session's day-end routine; tools/large_files.py sweep · **lane:** builder
- **Checked:** NOW.md:1 - GOAL line to Sunday 4 October ; tools/hooks/post-commit:9-15 - a commit touching FOR-JAFAR.md runs tools/backup-to-dropbox.py and logs its line ; tools/backup-to-dropbox.py:1-40 - adds only, never deletes or overwrites ; FOR-JAFAR.md:89 Builder 'Backup with this commit'; FOR-JAFAR.md:68 Clothes 'Backup ran: OK'; Town summary (FOR-JAFAR.md:34-54) has no backup line ; …
- **Inferred:** Whether the hook is installed in .git/hooks on Jafar's PC cannot be checked from this clone.

### OTH-011 · BUILT · CLAUDE.md:53

- **Ruling:** Research first: check production/research; research by a helper, dated, saved by topic, one line in the summary.
- **Checked:** production/research/ - about 110 topic folders plus README.md ; production/research/plain-1990-clothes/NOTE.md:1-3 - dated 1 October, 'a separate helper was given the problem, not a theory ... about thirty minutes', 22 links ; FOR-JAFAR.md:87 Builder 'Research:' line; FOR-JAFAR.md:64 Clothes 'Research:' line ; DECISIONS.md:216 - the Marvelous month (money) taken to Jafar as a decision, as required
- **Inferred:** The town's 2 October summary has no research line; it may have done no research that day.

### OTH-012 · BUILT · CLAUDE.md:57

- **Ruling:** Before new work, research the whole professional pipeline first; on failure, question the method before the symptom.
- **Checked:** production/research/aaa-street/1-PIPELINE.md - street pipeline method (merged f0a1724) ; production/research/wardrobe-at-scale/SUMMARY.md - method-level research after clothing failed; DECISIONS.md:216 acts on it ; production/research/clothing-pipeline/PIPELINE-2026-09-30.md - the clothing pipeline ; production/research/ui-design/PIPELINE-AND-STANDARDS.md - interface method ; …
- **Inferred:** V3 (hillside) and V5 (night) are covered only within aaa-street (SUMMARY, 3-LIGHT-AND-GRADE); no separate note.

### OTH-013 · BUILT · CLAUDE.md:58

- **Ruling:** Two tries then research; one more failure, set aside; every daily summary names what went past that.
- **Checked:** FOR-JAFAR.md:91 Builder 'Failed, past two tries: the voice in pieces, and a compiled loop' ; FOR-JAFAR.md:49 Town 'Past the two-tries rule: the written lines ... and the street lines' ; FOR-JAFAR.md:62 Clothes 'Set aside: the donkey jacket ... the suit jacket' ; NOW.md:29 - the indoor camera 'SET ASIDE under the two-tries rule' with what was tried
- **Inferred:** The office camera set-aside (1 October) is due in the builder's 2 October summary, not yet written.

### OTH-014 · BUILT · CLAUDE.md:59

- **Ruling:** A set-aside the game cannot do without goes into Needs you at once as blocked, with research in another direction.
- **Checked:** FOR-JAFAR.md:15 - Needs you item 2 'Clothing is BLOCKED', with the four routes tried, why they failed, and research in another direction (wardrobe-at-scale) ; production/research/wardrobe-at-scale/SUMMARY.md - that research exists ; DECISIONS.md:211 - recorded ; CLOTHES.md:13 - the Marvelous proof's fail path is written as 'a blocked capability in Needs you'
- **Inferred:** The voice-delay methods were 'set aside past the two-tries rule' (FOR-JAFAR.md:22) and are not in Needs you; read as acceptable, since the voice works at about 4.5-5.4 s and the delay item is scheduled by his pick.

### OTH-015 · BUILT · CLAUDE.md:63

- **Ruling:** Three sessions in separate lanes and checkouts; handovers in NOW.md; fetch and rebase before push; push to main.
- **Checked:** git ls-remote: refs/heads/town exists (the town's branch) ; NOW.md:31 '## Handovers to clothing' and NOW.md:41 '## Handovers' headings with lines from each session ; git log - clothing commits on main (bde70db, 3981e28), town commits on main (7f7ed78, 99559a6)
- **Inferred:** No remote 'clothes' branch; the clothing session pushes straight to main, which the ruling allows. ; Fetch-and-rebase discipline cannot be seen in a shallow clone.

### OTH-016 · LISTED · CLAUDE.md:67

- **Ruling:** Clothing in Blender on exported bodies; builder fits by script (resizing graph, Strip Sim Mesh false, Chaos cloth); dressed people to his page.
- **Missing:** Fitting by MetaHuman's resizing graph with Strip Sim Mesh false is not built; garments are fitted as skinned FBX.
- **On a list:** CLOTHES.md:13 (handed to the builder 'for the Outfit Asset on Ron (MH_RoccoP2) and Darren (MH_SamC5)'); NOW.md:53 (construction body handover)
- **Superseded by:** DECISIONS.md:216 (the 'only in Blender' part)
- **Checked:** NOW.md:37 - bodies Ron MH_RoccoP2, Sheila MH_LenaS4, Darren MH_SamC5 in F:/LedgerTools/bodies; the slim/average/heavy builds set aside ; production/specs/garments.json - garments handed back from F:/LedgerTools/garments ; tools/ue/import_garments.py + ue-probe/.../LedgerGarments.h:1-12 - fitting today imports a skinned FBX onto the body skeleton and follows the leader pose ; grep 'StripSimMesh/bStripSimMesh/Strip Sim Mesh/strip_sim_mesh' in tools and ue-probe/Source: no hit ; …
- **Inferred:** The Outfit Asset step named in CLOTHES.md:13 is the resizing-graph route; Epic's construction preset bodies (NOW.md:53) replace the three builds for that route.

### OTH-017 · BUILT · CLAUDE.md:72

- **Ruling:** The playable route comes first; all other visual iteration stops while the route (list's first item) is broken.
- **Checked:** NOW.md:5 - ORDER of 1 October evening keeps the review's High faults first, then Medium and Low, then the interface, then the visual bar ; NOW.md:8 - 1b (the route's faults) is the first open item; V1-V9 come after it (NOW.md:10-20) ; git log - High faults fixed in a0a0891 (20:01); interface commits 3e693da (20:39) and 318d9dc (21:21) followed while N3, N4, M3 and M4 were still open
- **Inferred:** The interface work after the High faults matches his evening order; the open Medium items were waiting on the town's Core. ; FOR-JAFAR.md:19 still quotes the 30 September wording ('other visual work stopped while it is broken'), which no longer describes the order.

### OTH-018 · PARTLY **R** · CLAUDE.md:73

- **Ruling:** Faces frozen: Ron's and Sheila's approved heads final, Darren's once approved; no more portrait adjustments.
- **Missing:** Darren's approved face S6 (approved 30 September) is not in the game; the game still loads MH_SamC5, and no list item says to change it.
- **Impact to a player:** 3 (Darren is met in ordinary play wearing a face Jafar did not approve; players cannot tell, but his approved look is missing.) · **belongs:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:917 and production/specs/in-game.json; an item on NOW.md's builder list · **lane:** builder
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:915-918 - game loads Rocco P2 and Lena S4 (approved), and Sam 'C5' for Darren ; production/specs/in-game.json:49-60 - Darren's backed-up and placed head is MH_SamC5 ; DECISIONS.md:136 - 30 September: 'Darren is S6 ... and goes into the game'; DECISIONS.md:184 confirms S6 ; grep 'S6' NOW.md: only NOW.md:37,39 (handover remarks); no builder list item to put S6 in the game ; …
- **Inferred:** No portrait re-work after 30 September found; the freeze itself is being kept.
- **Reviewer:** CrimeProbe.cpp:917 hard-codes Darren's approved take as 'C5'

### OTH-019 · BUILT · CLAUDE.md:74

- **Ruling:** Lighting judged through the game's own camera and exposure, never portrait frames alone.
- **Checked:** ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:4180-4187 - -PageShots=day/night takes frames in the running game 'through the game's own light and exposure' at window size (2560x1440) ; production/approvals/2026-10-01/page.json - street looks 'Taken today in the game at 2560 by 1440, through its own light and exposure' ; production/approvals/2026-10-01/street-hook-day.webp - 2560x1440
- **Inferred:** The page shots use the scene file's three fixed composition cameras (cam_hook, cam_A, cam_B; CrimeProbe.cpp:4181-4183), not the player's third-person camera; exposure and light are the game's.

### OTH-020 · BUILT · CLAUDE.md:78

- **Ruling:** Pictures judged on the page: tap for full-screen at full resolution, pinch, swipe, close; films with sound; every page tool.
- **Checked:** tools/page_pictures.py:1-22 - viewer: full-screen at own resolution, pinch/wheel zoom, swipe/arrows, Close/Esc, data-film-sprite films with sound, no links ; grep 'page_pictures' tools/*.py: approval_page, candidate_page, day_page, ingame_page, town_day_page, town_page, weekend_page ; tools/town_day_page.py:499 - selftest asserts the viewer mark in every built page ; production/approvals/2026-10-01/index.html, 2026-10-01-town-4/index.html, design/ui/step1/2/page/index.html - viewer mark present ; …
- **Inferred:** tools/cleanup.py's page has no viewer, but it shows no pictures.

### OTH-021 · PARTLY · CLAUDE.md:79

- **Ruling:** Every page fits one phone screen: at most three decisions, one line each with a tap; detail folded shut.
- **Missing:** The builder's page tool (day_page.py) does not enforce three decisions; Thursday's page carried four.
- **Impact to a player:** 1 (Approval-page usability only.) · **belongs:** tools/day_page.py (a limit like town_day_page.one_screen) · **lane:** builder
- **Checked:** tools/town_day_page.py:318-409 - MAX_DECISIONS=3 and one_screen() raises on more decisions, long questions or long options ; grep 'MAX/three/one screen' tools/day_page.py: no limit (day_page.py makes the builder's daily page) ; production/approvals/2026-10-01/page.json and index.html - four decision keys (look-street-dressed, look-street-night, look-mouths-speaking, look-dressed-boots-handbag), after the 30 September ruling ; tools/day_page.py:199-220 - detail folded in <details> (closed)
- **Inferred:** candidate_page.py, ingame_page.py, approval_page.py and weekend_page.py also have no decision limit; they may no longer be in use.

### OTH-022 · CONDUCT · CLAUDE.md:80

- **Ruling:** Only expensive or taste items reach his page; props, clutter, materials and sounds pass by the gate alone.
- **Checked:** production/approvals/2026-10-01/page.json - four items: two whole street frames, the cast's mouths, the cast's first garments (all kinds the ruling allows) ; NOW.md:11 V1 - the pawnbroker's display went into the game through the gate (two fresh reviewers), not onto his page as a prop
- **Inferred:** A sorting rule for what goes on pages; no tool enforces it, and the pages checked comply.

### OTH-023 · BUILT · CLAUDE.md:81

- **Ruling:** Every visual judged against the Hook sheet and KCD2 frames; page names shortfalls first; yes only for 2026-grade.
- **Checked:** production/reference/hook-sheet.png, kcd2-town-arcades.jpg, kcd2-town-fountain.jpg - present ; production/art/clothing/footwear/darren-boots-review-1.md:4 - judged 'against the bar (production/reference/hook-sheet.png and the KCD2 frames)' ; production/art/clothing/sheila/ready-pieces-against-the-bar-2026-10-01.md - pieces judged against the bar ; NOW.md:11 V1 - the reviewer's shortfalls against the 2026 bar recorded, going to his page with those notes ; …
- **Inferred:** The first page under this rule (2 October) is not made yet, so 'shortfalls named first, no yes' cannot be checked on a page.

### OTH-024 · PARTLY · CLAUDE.md:82

- **Ruling:** The gate: own check against references, then a blind reviewer; voices judged by ear, the accent checker a screen only.
- **Missing:** The accent checker is still coded and described as a gate that rejects takes; no page tool shows its flag beside the take for his ear.
- **Impact to a player:** 1 (Process: genuine regional voices could be withheld from Jafar; not visible to players directly.) · **belongs:** tools/voice-live/take_gate.py (flag, not FAIL), speak_lines.py, and the page tools (show the flag beside a take) · **lane:** builder
- **Checked:** tools/voice-live/take_gate.py:1-25 - 'The gate's first half for a voice take'; 'a voice drifting American ... is rejected before he hears it' ; tools/voice-live/take_gate.py:124-127 - verdict FAIL on 'american' or 'accent:<top>' ; grep '30 September/1 October/screen' in take_gate.py, accent_check.py: no update after the by-ear ruling ; tools/voice-live/speak_lines.py:12 - lines 'checked by accent_check.py before it can reach the page' ; …
- **Inferred:** Whether sessions still drop takes on take_gate's FAIL cannot be seen; the tools still call it the gate.

### OTH-025 · CONDUCT · CLAUDE.md:87

- **Ruling:** Before every push know which workflows it sets off and their cost; never push on a failing check.
- **Checked:** tools/hooks/ - only post-commit; no pre-push hook ; .github/workflows/*.yml - each workflow's header comments state its triggers and runner (e.g. ledger-probe-unreal.yml:18-43, self-hosted ledger-pc) ; CLOTHES.md:last Status bullet - the clothing session records what its pushes set off
- **Inferred:** No tool enforces it; it binds behaviour.

### OTH-026 · BUILT · CLAUDE.md:88

- **Ruling:** Done means in the build and walked by the AI tester; big items done only after his independent cloud review.
- **Checked:** tools/ai-tester/play.py:1-55 - the AI tester drives the packaged game with real key presses ; tools/route_walk.py; production/playtest/route-walk/2026-10-01-0551/verdict.json - route walks ; FOR-JAFAR.md:20,30 - route and interface lines say 'not yet walked' and 'Left: ... an independent review', not done ; NOW.md:8 - 'never "done" before it passes' ; …
- **Inferred:** TOWN.md:21-43 marks items DONE (rule table, street lines, the text half of the delay) without a cited AI-tester walk; the lines are in the build (OwnLines.h; TalkHelper/Program.cs:1401), so 'walked' is unproven, not disproven. ; No mechanism ties a [x] or DONE to a tester run.

### OTH-027 · BUILT · CLAUDE.md:89

- **Ruling:** Golden rows written from the design; a faulty row gets a failing design test first, then code and row fixed together.
- **Checked:** production/audits/review-2026-09-30/FAULTS.md:10,319 - four faults were written into golden rows (A9, A11, B6, WeekFiled) ; production/audits/review-2026-10-01/SUMMARY.md - 'The four faults written into the test tables are gone from them'; FAULTS.md:41,84 A10 rows fixed ; ue-probe/perception-golden.txt:55658 - TeaClosed/late now 'Stayed'; :57060 Aftermath now Rita's own first-person line ; ue-probe/Source/LedgerProbe/Public/CrimeProbe.h:2932-2935 - N1 test rows named for the design ('n1-the-account-is-sent-under-the-lines-deed')
- **Inferred:** Test-first order cannot be checked in this shallow clone (35 commits). ; perception-golden.txt:57852 SweepAsked/2 still lists rita; the 1 October review reports A11 fixed, so read as acceptable.

### OTH-028 · PARTLY · CLAUDE.md:92

- **Ruling:** No API calls in development; only live play uses LEDGER's key, with a hard monthly cap; no tool or workflow uses it.
- **Missing:** No monthly cap in code on the game's live talk (no budget is passed when he or his friends play); the cap, if any, sits only with the provider.
- **Superseded by:** DECISIONS.md:126 (the 'no tool may ever use it' part, for capped talk measurements)
- **Impact to a player:** 1 (Invisible to players; a money risk to Jafar once friends play on his key.) · **belongs:** ue-probe CrimeProbe.cpp LiveHelperStart (pass a budget) or TalkHelper (a persisted monthly ledger) · **lane:** builder
- **Checked:** .github/workflows/tier2-generate.yml:26-30 - the API workflow is 'if: false' ; tools/ai-tester/play.py:425,680 - removes ANTHROPIC_API_KEY; selftest asserts no api.anthropic.com in the source ; ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3137-3172 - the key is read from %LOCALAPPDATA%\LEDGER\live-talk-key.txt only in a played run (never -unattended, -TalkFake or scripted runs) ; ledger/Assets/Scripts/Core/BudgetedClient.cs:72-75 + TalkHelper/Program.cs:1420-1432 - a per-run budget only when --budget-usd or LEDGER_TALK_BUDGET_USD is given ; …
- **Inferred:** A spending cap may be set on the key in the provider's console; that cannot be seen from the repo.

### OTH-029 · BUILT · ROADMAP.md:7

- **Ruling:** One integrated encounter (crime, witness, gossip, consequence, questioning, quit-reload, unwitnessed control) as the build's regression.
- **Checked:** ROADMAP.md:22-24 - 'PASSED 24 September ... it is the build's regression' ; .github/workflows/ledger-probe-unreal.yml:2438-2450 - runs -Encounter=play/reload/unseen with a disk save between launches ; .github/workflows/ledger-probe-unreal.yml:3029-3030 - tools/encounter-verdict-check.py judges all three per commit ; tools/encounter-verdict-check.py:1-15 - the seven conditions
- **Inferred:** The regression runs the talk stand-in (-TalkFake) and the scripted deed; the 1 October review's N1 fault lived in free play, which this regression does not cover.

### OTH-030 · LISTED · NOW.md:5

- **Ruling:** Order of 1 October: review faults, then interface, then visual bar with the voice delay, then the friends' build; no placeholders.
- **Missing:** The items it orders are still open.
- **On a list:** NOW.md:5
- **Checked:** NOW.md:5 - the ORDER line ; NOW.md:8 (1b), :9 (UI), :10-20 (V1-V9), :21-22 (2, the delay), :23 (3, friends' build) - all open ; production/research/checklist-sweep-2026-09-29/BUILDER.md - the twenty basics exist
- **Inferred:** The bar ('no placeholder anywhere a friend can look') is not yet met; it is the substance of V1-V9 and item 3.

### OTH-031 · LISTED · NOW.md:8

- **Ruling:** 1b: fix the 1 October review's faults (N1, N2 High; N3, N4, M1-M4 Medium; Low), test first, then walk.
- **Missing:** N3, N4, M3 ports; M4; the Low items; the walk; his cloud review.
- **On a list:** NOW.md:8
- **Checked:** ue-probe/.../CrimeProbe.cpp:2850-2853 - N1 game half: EvidenceAccount under DeedKeyNow(); CrimeProbe.h:1658-1660 sends 'topic' ; ledger/TalkHelper/Program.cs:577 - N1 town half reads evidence 'topic' ; grep -c Nowak content/dialogue/crime-witness-v1.json: 0 (N2 town half) ; git log - a0a0891 'The review's first High fault fixed in the game, two Medium ones'; 7f7ed78 the town's High halves ; …
- **Inferred:** N3, N4 and M3 are claimed done in the town's Core (FOR-JAFAR.md:43-45); no main commit after 7f7ed78 shows them, so they may still be on the town branch.

### OTH-032 · LISTED · NOW.md:9

- **Ruling:** Interface built as drawn at 1080 high, inside the middle 16:9, readable at 3440x1440 and 1920x1080; no debug text.
- **Missing:** Suggested lines (pending his yes), the controller's round buttons, the sounds, the independent review.
- **On a list:** NOW.md:9
- **Checked:** ue-probe/Source/LedgerProbe/Public/LedgerPaper.h, LedgerPause.h, TitleScreen.h, LedgerSettings.h - the kit and screens exist ; ue-probe/.../CrimeProbe.cpp:5321,5430 - suggested-lines and typing-box Slate widgets ; grep AddOnScreenDebugMessage in ue-probe/Source: one hit, LedgerProbe.cpp:502, in the probe-shot mode only
- **Inferred:** Whether any debug text shows in ordinary play needs a run; none found in play code.

### OTH-033 · LISTED · NOW.md:10

- **Ruling:** The visual bar V1-V9, each researched first, judged in game camera against Hook sheet and KCD2, as whole frames.
- **Missing:** V1-V9 not finished.
- **On a list:** NOW.md:10
- **Checked:** NOW.md:10-20 - V1 to V9 all '[ ]' ; NOW.md:11 - V1 the pawnbroker in the game; the other eleven windows wait on his yes ; production/research/ - method notes for V1, V2, V4, V6, V7, V8, V9 (see OTH-012)

### OTH-034 · LISTED · NOW.md:18

- **Ruling:** Prepared lines get Epic's audio-driven mouths (reverses the loudness mouth for them).
- **Missing:** Audio-driven mouths are not on by default for prepared lines.
- **On a list:** NOW.md:18
- **Checked:** ue-probe/.../CrimeProbe.cpp:3888-3889 - made faces play only with -MadeFace or -FaceAB (off by default) ; NOW.md:24 - 'every line plays it [the loudness mouth]; the made faces stay on file (-MadeFace)'
- **Inferred:** Audio-driven mouths exist for some prepared lines but are switched off by default; making them the default is the open work.

### OTH-035 · LISTED · NOW.md:21

- **Ruling:** Friends' build: runs from a shortcut in a fresh Windows account on his PC, twenty basics, voice stopgap, walked 30 minutes.
- **Missing:** The build, the basics and the thirty-minute walk.
- **On a list:** NOW.md:21
- **Checked:** tools/voice-live/make_portable.py - the voice stopgap tool exists ; production/research/checklist-sweep-2026-09-29/BUILDER.md - the twenty basics listed ; NOW.md:29 - '3 waits on his fresh Windows account and room on F:'

### OTH-036 · SUPERSEDED · NOW.md:22

- **Ruling:** Item 4: mouths for prepared lines, settled for the loudness mouth by blind picks, then reopened.
- **Superseded by:** NOW.md:18 (V8); DECISIONS.md:201
- **Checked:** NOW.md:24 - '[x] 4 ... SETTLED 1 October ... REOPENED the same afternoon by his ruling as V8' ; NOW.md:18 - V8 open: prepared lines get Epic's audio-driven mouths ; DECISIONS.md:201 - the reversal recorded

### OTH-037 · LISTED · NOW.md:34

- **Ruling:** Plain 1990 clothes for Ron, Sheila, Darren before the friends' build: no contrast stitching, no trainers.
- **Missing:** The swaps and fittings; the cast still wears the 2020s pieces.
- **On a list:** NOW.md:20; CLOTHES.md:19
- **Checked:** NOW.md:20 - V9 open ; CLOTHES.md:19 - item 3 open, with the agreed split (clothing's ready pieces; Epic's plainest swapped in by the builder) ; NOW.md:54,56 - clothing answered which pieces are its own and which to swap ; production/specs/garments.json - only RonBoots and SheilaHandbag worn; spectacles, chain, belt, pager held; no skirt, tights or Epic swaps listed ; …

### OTH-038 · SUPERSEDED · NOW.md:39

- **Ruling:** Suits and coats from MakeHuman CC0, refitted in Blender and bound panel by panel to named body versions.
- **Superseded by:** DECISIONS.md:216; CLOTHES.md:13
- **Checked:** DECISIONS.md:161 - the 30 September ruling (free MakeHuman, 'no Marvelous Designer') ; DECISIONS.md:211 - clothing blocked after four free routes, including MakeHuman's suit jacket ; DECISIONS.md:216 - Marvelous Designer proof for tailored outerwear, 'Reopens 30 September's "no Marvelous Designer"' ; CLOTHES.md:17 - MakeHuman suits 'not worked until 3' ; …
- **Inferred:** The handover should have left NOW.md under OTH-002.

### OTH-039 · LISTED · NOW.md:45

- **Ruling:** 30 September split of the review's faults: Core side to the town, game side and ports to the builder.
- **Missing:** B8's Core items, C5's nerve, D's port (talk through a wall), and what moved into 1b.
- **On a list:** TOWN.md:26; NOW.md:8
- **Checked:** TOWN.md:21-26 - town side done and on main except D (on branch town-wall, waiting for the port), B8's Core items and C5's nerve ; production/audits/review-2026-10-01/SUMMARY.md - most 30 September faults fixed and proved; the rest carried into the 1 October faults ; git ls-remote: no 'town-wall' branch on GitHub
- **Inferred:** D's port is not named on the builder's list; it sits only in this handover and TOWN.md:24. ; This handover is largely done but still in NOW.md (see OTH-002).

### OTH-040 · LISTED · NOW.md:51

- **Ruling:** 1 October split: town does N2, N1's half, Mickey's people, N3, M3, B3/L4; builder does N1's key, M1, M2, M4 and ports.
- **Missing:** N3, N4, M3 (Core, then ports), B3/L4, M4, the Low items.
- **On a list:** NOW.md:8; NOW.md:51
- **Checked:** grep -c Nowak content/dialogue/crime-witness-v1.json: 0 (N2 done) ; ledger/TalkHelper/Program.cs:577 - evidence 'topic' read (N1 town half) ; ue-probe/.../CrimeProbe.h:1658-1660, 2932-2935 - N1 key sent and tested (builder half) ; NOW.md:8 - M1 and M2 marked done; N3, N4, M3 ports, M4, the Low items and the walk left
- **Inferred:** The town's N3, N4 and M3 Core work was not found on main under the names tried (Mickey's people, NeverReport, tea while held).

### OTH-041 · LISTED · TOWN.md:15

- **Ruling:** The town's first task: the independent review's Core side, each a failing test first, then code and golden row.
- **Missing:** B8's Core items, C5's nerve, D merged and ported.
- **On a list:** TOWN.md:26
- **Checked:** TOWN.md:21-26 - State: done and on main (B1, A11, A10, A5, A9, B6, B7, A13, A12, B3, B4a, B5, ...); left B8's Core items and C5's nerve; D waits on branch town-wall ; production/audits/review-2026-10-01/FAULTS.md:41,84 - A10 and the golden rows proved fixed

### OTH-042 · BUILT · TOWN.md:18

- **Ruling:** Fix 'couldn't swear to it', every golden row encoding a fault, and A5 (a noise or a shape is suspicion).
- **Checked:** production/audits/review-2026-10-01/FAULTS.md:41 - A10 'Fixed', proved (CertaintyFor rows now 1) ; production/audits/review-2026-10-01/SUMMARY.md - 'A shape or a noise no longer counts as "it was him"'; 'The four faults written into the test tables are gone' ; ue-probe/.../Gossip.h:670-679 and Core/Gossip.cs:419 - the phrase now used only below full certainty ; ue-probe/perception-golden.txt:55658, 57060 - Ada's tea and Rita's window rows changed

### OTH-043 · BUILT · TOWN.md:29

- **Ruling:** The town's list of 30 September: rule table measured and switched on, other characters' street lines, text half of the delay.
- **Checked:** TOWN.md:31-77 - items 1-3 marked done with measurements ; ledger/TalkHelper/Program.cs:1397-1402 - UseRules=true, PlainFallback=true ; ue-probe/Source/LedgerProbe/Public/OwnLines.h (545 lines); LedgerProbe.cpp:837-839 - own street lines on unless -NoOwnLines ; ledger/Assets/Scripts/Core/LlmClient.cs:99 - HTTP/2 warm connection
- **Inferred:** 'Still no new systems' binds behaviour; the town's 1 October work (suggestions for the interface) was Jafar's own order.

### OTH-044 · BUILT · CLOTHES.md:3

- **Ruling:** Clothing session: Blender only, own worktree, bodies via handovers, garments to F:\garments, in order, nothing bought.
- **Superseded by:** DECISIONS.md:216 (the 'Blender only, not Marvelous Designer' part)
- **Checked:** NOW.md:31-39 - bodies handed over under 'Handovers to clothing' ; NOW.md:53-56 - garments handed back with lines under 'Handovers' ; production/specs/garments.json - F:/LedgerTools/garments paths ; DECISIONS.md:216 - Marvelous Designer added to the lane (free trial; the month bought only if the proof passes) ; …
- **Inferred:** No 'clothes' branch on GitHub; commits go straight to main (bde70db, 3981e28).

### OTH-045 · BUILT · CLOTHES.md:5

- **Ruling:** Clothing method: research the whole pipeline first; game clothes are skinned meshes, cloth only for loose parts; builder tests in Unreal.
- **Checked:** production/research/clothing-pipeline/PIPELINE-2026-09-30.md, RETOPOLOGY-AND-SKINNING-2026-09-30.md - method research ; tools/meshgen/blender/bind_garment.py, skin_garment.py, retopo_garment.py - skinned-mesh chain ; tools/ue/make_cloth_garment.py - cloth only for the skirt (NOW.md:26) ; production/art/clothing/suit-jacket-ingame-2026-10-01 - builder's in-engine test (NOW.md:35)

### OTH-046 · LISTED · CLOTHES.md:11

- **Ruling:** The clothing list of 30 September (in order), replacing the previous one.
- **Missing:** Items 0-3 open; item 1's waiting note is stale.
- **On a list:** CLOTHES.md:13-19
- **Checked:** CLOTHES.md:13 item 0, :15 item 1, :16 item 2, :19 item 3 - all open ; CLOTHES.md:15 - still 'WAITING ON JAFAR (scope ...): (A) ... (B) ... (C)', settled by DECISIONS.md:211,216

### OTH-047 · LISTED · CLOTHES.md:13

- **Ruling:** Marvelous proof: one 1990 charcoal suit jacket in the free trial, fitted as Outfit Asset on Ron and Darren, judged against the bar.
- **Missing:** The jacket, its fitting and the review; the construction body export.
- **On a list:** CLOTHES.md:13
- **Checked:** CLOTHES.md:13 - open ; git ls-files / grep MD-TAILORED: no hit; the cited production/research/clothing-pipeline/MD-TAILORED-JACKET-2026-10-01.md is not in the repo (the research is in production/research/wardrobe-at-scale/4-MARVELOUS-MONTH.md) ; tools/meshgen/blender/body_measurements.py:184 - shoulder to elbow measured for Jaeger ; NOW.md:53 - construction body asked of the builder (a handover, not on the builder's ordered list) ; …
- **Inferred:** Jaeger drafts are said to be on F:; cannot be checked.

### OTH-048 · LISTED · CLOTHES.md:19

- **Ruling:** Principals' plain 1990 outfits: clothing's ready pieces fitted, Epic's plainest swapped in for the rest, judged against the bar.
- **Missing:** Fitting the ready pieces and Epic's swaps on all three.
- **On a list:** CLOTHES.md:19; NOW.md:20
- **Checked:** CLOTHES.md:19 - open ; NOW.md:20 - V9 open ; production/specs/garments.json - Sheila's skirt and tights not listed; spectacles, chain, belt and pager on hold ; production/art/clothing/footwear/darren-boots-review-1.md - the boots failed against the bar, so they go to the builder as a swap
