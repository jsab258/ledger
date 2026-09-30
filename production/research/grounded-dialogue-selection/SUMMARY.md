# How games choose what a character can say, and where LEDGER differs

Research, 30 September 2026, by a separate research helper. (The helper returned its text; the session that asked for it saved it here after checking its figures from the project's own files: the labellers' agreement, the checker's current catch and refusal rates, and how facts are chosen today.)

## How games do it, in order

1. **Each character holds facts.** Each fact is a small named entry, such as "saw the van" or "has told Tom about the will", sometimes with an expiry. The street holds facts of its own.
2. **When the player speaks, the game builds a question for itself.** It asks what kind of moment this is: a greeting, "where do I sleep?", "who runs things?". It adds who is speaking and everything they hold.
3. **Every written rule lists the conditions it needs.** The rule that matches the most conditions wins, so a special case beats a general one. A plain default always sits at the bottom, so a character never has nothing to say. Valve's released code does exactly this; Bethesda, BioWare and Hades work the same way in outline.
4. **The winning rule plays its line and records that it was said,** so the next question knows.
5. **"I don't know" is itself a written rule:** the default for that kind of question, often pointing to someone who does know. It is chosen; it is not what is left when something fails.

## How teams put a language model on top

- The code still chooses what may be said; the model only words it. Knowledge filters, per-character memories and game state are kept out of the model's reach.
- Where a model was allowed to decide the game's state, players talked it into handing out quest rewards (a large online game, 2025).
- Outside games, a big company's production dialogue system checked each generated line against the chosen content. If the line failed, it used a plain set phrasing of the same content: correct, "even if it is less natural".

## How they measure it

- They label questions, including some that cannot be answered.
- They count wrong refusals and wrong answers separately.
- They tune the checker on half of the labelled examples and confirm it on the other half.
- They compare methods question by question, and report how uncertain the result is.

## What LEDGER does differently

- It chooses facts by shared words, not by the kind of question.
- **Its "that's all I know" is what is left when the check refuses twice.** It throws away an answer the character could give, instead of falling back to a plain, true one.
- **Its checker has one setting, never chosen against labelled details.** Its worked examples come from the same questions it is tested on.
- **All sixty test questions can be answered,** so inventing on questions that cannot be answered, the other side of the trade, is never measured.
- **Sixty questions can show a fall from about 22 fallbacks to 15, not to 18.** The planning test could not have shown a difference either way.

## What to do, in order

1. **Find the causes (half a day).** For each of the 22 fallbacks, sort the cause: the wrong facts were chosen, a real embellishment, or a true paraphrase refused.
2. **Say the facts plainly (about a day).** When the check refuses twice, the character says the chosen facts plainly in their own manner, built by code from each fact. Put one sample on Jafar's page. "That's all I know" stays only for when no fact was chosen at all.
3. **Calibrate the checker (one to two days)** on about 250 labelled details:
   - code clears names, numbers and times that match the chosen facts;
   - the checker keeps the setting that refuses the fewest true paraphrases while letting through no more inventions than today;
   - the result is confirmed on questions it was never tuned on.
4. **A small rule table for the first week (two to three days),** like Valve's: the kind of question, who is asked, and what they hold decide among
   - an answer;
   - a partial answer;
   - "don't know, ask X";
   - or, for the few moments that matter, a written line.
5. **Measure every change** on the sixty, on a new sixty that nobody tuned on, and on thirty questions nobody in the town can answer.

## What could not be verified

- Valve's slides and wiki were blocked, so its method comes from its released code.
- The internals of Firewatch, The Last of Us and Hades.
- How often any studio's characters say "don't know".
- The details inside today's AI character products.
- The sample-size figures are my own simulation.
