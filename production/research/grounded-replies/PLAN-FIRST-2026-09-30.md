# Picking the facts and the intent before the words: contextual dialogue, end to end (research note, 30 September 2026)

Asked by Jafar's list of 30 September, after the adversarial audit: grounded
replies, method first, Valve's GDC talk included. A research helper was given
the problem and the audit's diagnosis, not a theory; about thirty minutes, web
only.

The work: a character in LEDGER answers a typed line aloud. Claude Haiku 4.5
writes the answer from what the character and the street hold, and a second call
rejects any reply with an unsupported specific. Three characters fall back to
"that's all I know" on 23 to 38 of a newcomer's 60 first questions.

## 1. Studios: facts first, then the line

1. **Valve (Ruskin, GDC 2012).**
   - Each event builds one query: the concept, plus facts from the speaker, its
     memory and the world.
   - A rule matches only if all its criteria hold. The rule with the most
     criteria wins, so special cases beat general ones.
   - The winning rule writes facts back, which feed the next query and can
     expire.
   - Left 4 Dead 2 had about 10,000 lines, each looked up in microseconds.
   - Sources: https://gdcvault.com/play/1015946/AI-driven-Dynamic-Dialog-through ;
     https://archive.org/stream/valve-publications/2012/GDC2012_Ruskin_Elan_DynamicDialog_djvu.txt
2. **Descendants.**
   - Hades plays a pre-written event whose conditions match, weighted by the
     team (13 Feb 2020,
     https://www.gamedeveloper.com/design/how-supergiant-weaves-narrative-rewards-into-i-hades-i-cycle-of-perpetual-death).
   - Yarn Spinner 3 drops lines whose conditions fail, scores the rest, and
     prefers the least seen
     (https://docs.yarnspinner.dev/write-yarn-scripts/advanced-scripting/saliency,
     read 30 Sep 2026).
3. **A line stays true because it plays only if its criteria hold in the fact
   store.**
   - Talk of the Town expands a grammar symbol only when its preconditions hold
     in the game state (8 Oct 2016,
     https://ojs.aaai.org/index.php/AIIDE/article/view/12877).
   - Hidden Door never takes the model's text as game state (20 Jun 2023,
     https://www.engadget.com/how-do-you-prevent-an-ai-generated-game-from-losing-the-plot-170002788.html).

## 2. Plan, then realise

4. **The classic pipeline.**
   - A content-planning step beat end-to-end models on unseen domains:
     adequacy 4.67 against 3.03 to 3.81 out of 7 (Aug 2019,
     https://arxiv.org/abs/1908.09022).
   - A symbolic plan worded by a neural model cut invented facts from 29 to 3
     out of 440, with fluency on par (Apr 2019, https://arxiv.org/abs/1904.03396).
5. **Knowledge before the reply.**
   - Wizard of Wikipedia (Nov 2018, https://arxiv.org/abs/1811.01241).
   - Grounding cut judged hallucination from 68.2% to 7.9% to 20.9%, while
     engagingness fell from 85.5% to 71% to 78% (Apr 2021,
     https://arxiv.org/abs/2104.07567).
   - K2R writes the knowledge, then the reply: hallucination fell from 16% to
     7%, and engagingness from 66% to 53% (Nov 2021,
     https://arxiv.org/abs/2111.05204).
6. **Intent plans.**
   - A policy chose each sentence's dialogue act and knowledge; its replies
     matched or beat a human's in 52% of cases (May 2020,
     https://arxiv.org/abs/2005.12529).
   - Human-rated gains were mixed (Feb 2024, https://arxiv.org/abs/2402.02077).
7. **Language models.**
   - Select, plan, then write: tighter attribution at equal quality (Mar 2024,
     https://arxiv.org/abs/2403.17104).
   - Answerability and sentence selection before writing: faithfulness up to
     16.8% higher (Feb 2024, https://arxiv.org/abs/2402.11770).
   - Reasoning first about what the character can know: 46.5% to 93.0% on
     questions it should not answer (May 2024, https://arxiv.org/abs/2405.18027).
   - Facts filtered by who may know them, before writing: fidelity up 34.6
     points (24 Jun 2026, https://arxiv.org/abs/2606.25632).
   - Strict JSON hurt reasoning but helped classification (Aug 2024,
     https://arxiv.org/abs/2408.02442).

## 3. Game characters with a plan step

8. **A detective game.** One model picks the single permitted fact or none, a
   second writes the line, and a third checks it. Invented turns fell from 17.8%
   to 6.3%, and players disliked the forced reveals (19 Sep 2026,
   https://arxiv.org/abs/2609.23043).
9. **CPDC 2025.** One model decides what game state to fetch, another words it:
   about 3 s a reply (3 Nov 2025, https://arxiv.org/abs/2511.01720).
10. **Latency.** No source prices the plan step alone. Haiku 4.5's first token
    comes at a median 0.62 s, then 83 tokens a second
    (https://artificialanalysis.ai/models/claude-4-5-haiku/providers, read 30 Sep 2026).

## 4. Measuring

11. **BEGIN** labels each reply attributable, not attributable or generic, with
    three annotators, a majority vote and alpha 0.7 (May 2021,
    https://arxiv.org/abs/2105.00071).

## What it says for LEDGER's test (inference)

- **Bounds and choice.** Code offers the character's own facts, with ids, and
  the allowed intents; the model chooses inside them. Code settles the plain
  "not known" itself.
- **The plan.**
  - An intent: answer, partial, deflect, don't know, ask back or refuse.
  - One to three fact ids.
  - What not to say.
  - Then the line. Unknown ids are rejected before anything is voiced.
- **A narrower check stays,** since planned systems still invent (7%, 6.3%):
  only the line against the chosen facts, while the first sentence is voiced.
- **Under half a second.** One call, the plan first in loose tags rather than
  strict JSON: 15 to 25 tokens, 0.2 to 0.3 s. A separate plan call would add
  about 0.6 s.
- **Measure.**
  - The same 60 questions, at least three runs an arm (at 60 a rate carries
    about ±12 points).
  - Two labellers blind to the arm, a third to adjudicate.
  - Compared question by question.
  - Also a blind preference for naturalness, since grounding cost engagingness
    in every study.

Not confirmed from the source: Firewatch's internals. Valve's figures come from
the archived slide text.
