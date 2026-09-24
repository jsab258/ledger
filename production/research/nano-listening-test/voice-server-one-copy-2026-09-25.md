# The voice server with one copy of the model: measured 25 September

The voice server beside the game used to load the voice model twice: a whole
copy on the processor only to learn each character's voice (the voice encoder
aborts on the card), and a second copy to speak. Now the one copy keeps the
parts that learn a voice on the processor and only the part that makes the
sound tokens on the card, and each learned voice is kept on disk, named by a
hash of its clip, so it is learned once per clip, not once per run.

Measured on this PC (RX 6700, DirectML), nothing else running, the same three
lines each time (two for Darren, then one for Sheila; ids sam and lena), the old server from git
beside the new one, by a scratch driver polling the process's memory.

| | old: two copies | new, first run (learns) | new, voices kept |
|---|---|---|---|
| ready after | 21.6 s | 16.5 s | 16.5 s |
| first sound, Darren's first line | 5.34 s | 4.26 s | 3.38 s |
| first sound, Darren's second line | 2.78 s | 2.86 s | 2.75 s |
| first sound, Sheila's first line | 2.65 s | 2.60 s | 1.90 s |
| memory in use (working set, peak) | 6.69 GB | 4.83 GB | 4.92 GB |
| memory committed, settled | 9.78 GB | 7.39 GB | 6.52 GB |

The sound is bit-identical: every one of the six sentence files from the new
server matches the old server's sample for sample (correlation 1.000, largest
difference 0.0000), because the voice is learned by the same code on the same
processor and the same seed makes the same line.

What it does not change: the card's own memory (the speaking half was always
on the card), and the in-game delay from the words appearing to the voice
starting, which also includes the game's side and the first sentence's length.

Tool: tools/voice-live/voice-server.py (`learn`, `cache_path`); the learned
voices live in C:\LedgerTools\chatterbox-nano\voice-cache on this PC.
