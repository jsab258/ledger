# Getting acting, not reading, from the game's voices

Research, 30 September 2026, by a separate research helper. (The helper returned its text; the session that asked for it saved it here after checking its claims about the project's own files.)

## What professionals do, in order

1. **Approve one voice per character** and check everything later against it.
2. **Give every line its context:** what has just happened, who is listening, what the character wants. Good directors avoid adjectives like "warm" or "menacing"; one London studio brings the game itself into the booth.
3. **Record several takes:** about two or three per line, more for short emotional lines.
4. **Choose by ear.** The director marks favourites; the editor picks on believability, cleanness and fit with the lines around it.
5. **Edit:** trim, keep natural breaths, remove clicks, keep gaps even.
6. **Mix:** even loudness from line to line, and a target for the whole game's sound (Sony publishes one). Distance and rooms are added in the game, not baked in.
7. **Listen in the game** and fix there.

Where synthetic voices reach shipped games, the acting still comes from people. Arc Raiders used actors' licensed voices for minor lines, then re-recorded some with people because of "a quality difference". For Cyberpunk's Polish expansion a living actor performed and the result was converted into a late actor's voice, with his family's permission.

## What the project does differently

- **The reference clips are read, not acted:** volunteers reading newspaper sentences. These models copy the style of their clip, so a read clip gives read lines. Probably the biggest single cause of the flatness.
- **Directions were adjectives, judged on one take each.** The acting model's makers say results vary and to try several times.
- **The live voice ignores its expression dial.** The game's live voice is Chatterbox's small, fast model, which accepts the expression setting and ignores it. Only the clip, the words and chance steer it.
- **The accent checker acted as a judge.** It fails about half of genuine Scotsmen.
- **Lines were judged alone, not in the street.**

## What to do instead, in order

1. **A library of clips per approved voice,** a few per mood (calm, warm, sharp, quiet, amused), from the same speaker's livelier recordings or from generated takes you approve by ear.
2. **A direction sheet per line made in advance:** situation, listener, intention, plus a few manner words for the model.
3. **Many takes per line** (my estimate: eight to twelve). A machine check removes wrong words, lost likeness and obvious accent slips; it screens, it does not judge.
4. **For one first scene, three or four finalists per line on your page.** Your picks show what works before anything is multiplied.
5. **Edit, even the loudness, and judge inside the game** through its own camera and sound.
6. **Live replies borrow the library:** each reply is tagged with a mood and spoken from that mood's clip, prepared in advance (the delay this adds is not yet measured). The most emotional moments should be made in advance.

**A question for you:** you could perform lines yourself and a converter would change them into the character's voice. Your acting would carry, but so would your own accent, which matters most for Darren. One converter is already allowed; others need a licence decision.

## What could not be verified

The network refused most studio sources (conference talks, Sony's loudness paper, Ubisoft's page) and the models' download pages; those points rest on search summaries. Nobody has published tests of these three models holding a Scottish or northern English accent while acting. "Two or three takes" comes from a developers' forum; other take counts are my estimates.
