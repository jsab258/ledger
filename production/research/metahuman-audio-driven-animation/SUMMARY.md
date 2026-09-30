# Talking faces: how studios do it, and Epic's tool

Research, 30 September 2026, by a separate research helper. (The helper returned its text; the session that asked for it saved it here after checking its claims about the project's own files.)

## What professionals do, in order

1. **Sort lines by importance.** Big scenes are filmed with actors; the rest is animated automatically from the voice. Hogwarts Legacy did this for over 50,000 lines in each language; The Witcher 3 built most of its conversations by machine from about 2,400 stock movements.
2. **Move the mouth from the sound**, and from the words where available. Jaw and lips are separate actions: in ordinary speech the lips do much of the work.
3. **Add emotion as its own layer**, set by the script's direction.
4. **Blinks and eyes.** About 26 blinks a minute in conversation. The eyes flick about, and look away more when speaking than when listening.
5. **Head movement that follows the voice's rhythm and pitch.** It measurably helps people understand speech.
6. **Gestures** from a library, on the stressed words.
7. **Judge in context**, and polish what matters most by hand. Mass Effect: Andromeda (2017) shows what automation without that care looks like.

## Epic's tool, and which form fits us

Epic's model (xADA, published at SIGGRAPH 2025) turns speech into MetaHuman face controls: jaw, lips, tongue, brows, blinks and a mood. It needs no script. It comes in three forms:

- **Offline, in the editor** (since 5.5). It bakes a recorded line into animation, with head movement. Best quality and free while playing, but only for lines made in advance.
- **Live from a microphone** (since 5.6; 5.8 added natural blinks and detected emotion). It only listens to a sound input, and Epic says it works the graphics card hard. It cannot hear our generated speech. Not for us.
- **A streaming version hidden in the engine** (5.8, test status, undocumented). It takes the voice in pieces as we make it and returns the face fifty times a second, about a twelfth of a second behind the sound. **This is the one that fits.** Paid add-ons on Fab appear to be built on it and claim it works in finished games; a public copy of Fortnite's files appears to contain it.

It is part of Unreal, under the Unreal licence, so it is free. It runs on the processor, or on any modern graphics card including AMD. NVIDIA's rival, Audio2Face, needs an NVIDIA card.

## What it costs

Known: the model is about 34 MB, and a similar model sold on Fab runs on the processor. Unknown: the time it takes each frame, its memory, whether it is packed into the finished game, and whether the AMD route works. Nobody we could reach has published a figure.

## Against the loudness jaw

The loudness jaw is free, never breaks, and reads as talking at a distance. Close up it flaps: it opens on loud hisses where a real mouth nearly closes, never presses the lips for p, b and m, and makes one shape for every vowel. The solver shapes the words and adds brows and blinks. It may read a flat synthetic voice as bored or sad, and its cost is unmeasured.

## What to do, in order

1. Measure it in a finished build on this PC with the real voices, on the processor first (the graphics card is busy with the picture and the voice).
2. If it passes, feed it the voice pieces as they queue, and show each face frame when its sound plays.
3. Give it the mood from the conversation instead of letting it guess.
4. Add what it lacks: eyes that look and glance away, head movement, blinking while listening.
5. Keep the loudness jaw as the safety net, and for each line's first tenth of a second.
6. Bake the pre-made lines offline.
7. Show Jafar the same lines through the game's own camera, side by side, unlabelled.

## What could not be verified

Most outside pages were blocked, including Epic's forums. The thread asking exactly our question, the Fab listings and the SIGGRAPH paper were seen only as search summaries. The engine source could not be read from here. No cost figure exists anywhere we could reach.

One licence point for Jafar came up on the way: the licence list calls NVIDIA's Audio2Face "MIT", but only its code is; its trained models are under NVIDIA's own licence, and it needs an NVIDIA card.
