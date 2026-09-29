# VoxCPM2's acted lines, through the gate (29 September)

Jafar's list, item 6: "livelier lines: VoxCPM2 with acting direction per line for the lines made in advance, on a blind page". The research's route 2 (production/research/character-pipeline/RESEARCH-2026-09-25.md): VoxCPM2 offline, a two-hour installation limit.

- **Installed in about ten minutes** on drive F (F:/LedgerTools/voxcpm2, CPU torch; the model, openbmb/VoxCPM2, Apache-2.0, 4.7 GB in F:/LedgerTools/hf). On the processor it makes a line in about 25 times its length (6 to 9 s of speech in 2 to 5 minutes): fine for lines made in advance, not for live talk. Compiling the model (its default) ended the process without a word; it runs with optimize=False.
- **Made** (tools/voice-live/voxcpm_takes.py): the acting test's four lines per character (threat, warmth, embarrassment, humour; tools/voice-live/acting-test.py), each cloned from the character's game clip two ways: plain (the clip and its transcript) and directed (the clip, with the acting direction in brackets before the line).
- **The gate's first half** (tools/voice-live/take_gate.py: the project's accent check over the whole take and every 2.5 s of it, the words heard back, the likeness to the clip):
  - Ron: all four directed takes pass (England throughout, the words right, likeness 0.64 to 0.76). The plain way began every take with the clip's own last word ("above"), so plain is not used.
  - Darren: directed, he comes out English (once Australian), not his Scottish; one plain take kept it. Fails.
  - Sheila: seven of eight takes lean American in a stretch, one is another woman (likeness 0.35). Her voice D itself leans that way (FINDINGS). Fails.
  - The game's own voice, the same lines for comparison: Ron passes 2 of 4, Darren 1, Sheila none (American stretches), so a blind pair exists only where both pass: Ron's threat and humour.
- **The gate's second half**, a blind reviewer measuring what it could not hear (whisper-medium, the accent check on 1.4 s and 0.55 s windows against 2,213 windows of English speech, formants, pitch, pace, level, clicks): the threat pair passes, both takes; in the humour pair the game voice's "Rain again." leans more American than Ron's own clip ever does, so that pair is not shown.
- **On Tuesday's page** (https://claude.ai/artifact/TmJnie1Qzo6jE6NdkyqRPo): Ron's threat line, A and B, loudness evened to -20 LUFS; ../acting-key-2026-09-29.json says which is which.

What it means: VoxCPM2 can act Ron's lines in his voice, English, from a direction, on this PC; it does not hold a Scottish voice, and it keeps whatever lean a voice already has. The game's current voice drifts more than it looked (whole-take checks passed it; 2.5 s windows do not), which is a finding for every voice the game speaks.
