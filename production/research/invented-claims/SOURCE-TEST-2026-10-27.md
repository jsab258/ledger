# Invented first sentences: harm, the source, and a hard rule (27 October 2026, evening)

His order that evening (production/orders/2026-10-25.md, "His order (27 October 2026, about 20:05)"): sort the
invented sentences Haiku lets through by harm; test at the source, on the same 617, the reply's instructions to state
only the speaker's facts and deflect otherwise, then a version where each fact carries an ID and each sentence names
the facts it uses; add a hard rule that no sentence naming a person, place or event missing from the facts may pass;
report invented per 300, harmful and harmless apart, and false refusals, against today, on his page. His budget: up to
$20 (20:10).

## Questions, written first

1. Of the invented first sentences Haiku's check lets through on the 617 (and the two the small checker's open cut-off
   adds), which are harmful (a person, place, time or event the facts lack) and which harmless (opinion, overstatement,
   manner)?
2. Written by the game's own reply model for the same 617 questions, how many first sentences are invented, how many
   get through the check, and how many true ones does it refuse: with today's instructions, with "only your facts,
   else deflect", and with numbered facts cited after each sentence?
3. What does a hard rule on names catch, and what does it refuse wrongly? What would a wider one catch?
4. What is the professional method for keeping a model to its sources?

## The method, from its source

Anthropic's guide "Reduce hallucinations" (https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-hallucinations,
read in full 27 October 2026, 20:58): its basic strategies are to allow the model to say it does not know, to ground
it in direct quotes, and to verify with citations, a claim with no supporting quote retracted; among its advanced ones,
"external knowledge restriction", an explicit instruction to use only the documents given. It says these reduce
hallucinations but do not remove them. His two versions are its restriction with permission to deflect, and its
citations; the game's prompt already carries a form of both ("Answer from what you have been told here ... What none
of it gives, you do not know"), without the facts listed beside the rule or cited.

## 1. The harm sort (a fresh reader, blind to where each came from)

The 37: the 35 invented sentences (Gemini's labels) Haiku's check passes among the 617, and the 2 the small checker's
open cut-off adds. Packet and key: F:/LedgerTools/checkers/try4/harm37-key.json, harm37-verdicts.json.

| | Harmful | Harmless | Not invented on reading |
|---|---|---|---|
| Haiku alone's 35 | 23 | 10 | 2 |
| Added by the open cut-off | 1 (Hal "runs everything") | 1 ("nothing much open on this side") | 0 |

Per 300 of the 308 invented sentences offered: Haiku alone lets through about 22 harmful and 10 harmless. The harmful
are mostly times and years (half past seven, eight in the morning, since nineteen sixty-three, since nineteen
eighty-two, back in eighty-two, eighty-seven), jobs given to the wrong person (Ron driving by day, Sheila on the
radio), places the facts lack (the pier head, over the chemist's shop) and contradictions (Mickey dying in his flat
upstairs). The reader's four low-confidence calls: three small invented objects (in her pocket, the awning, the sign),
counted harmful, and "his daughter June ...", counted harmless. The two "not invented" read "last year" as 1989, right
only because the game is set in 1990.

## 3. The hard rule on names (NameRules in the game's code; tools/checkers/name_rule.py, its reference)

Designed on the tuning half only (2,151 sentences), then run once on the 617. The facts are read without their IDs
("C1: ", "P22: "), as the game hands them to the rule (the fresh review's fix: read with them, the numbers 1 to 22 always
counted as stated, so the wider form's first figures were too low).

| | True refused, tuning (909) | Inventions caught, tuning (1,242) | The 617: of Haiku's 35 stopped | The 617: true newly refused | The source test: through stopped / true newly refused |
|---|---|---|---|---|---|
| His rule: names (people, places, events) | 0 | 8 (Leeds, London, Newcastle, Manchester) | 0 | 0 | 0 / 0 |
| Wider (beyond his rule): also numbers, years, and a short list of place and role nouns | 0 | 150 | 8, all harmful | 0 | 1 / 0 |

His rule as written catches nothing Haiku lets through, because the leaks describe rather than name. The wider one stops
"since nineteen sixty-three", "since five", "back in eighty-two", "since nineteen eighty-two", "eighty-seven", "the
harbourmaster", "the pier head", "over the chemist's shop" and "the awning". What neither catches: times whose numbers
the facts state for something else (the facts' opening hours hold most small numbers, so "half past seven" passes),
wrong jobs and contradictions. The name rule's known gap: a lone invented name opening a sentence ("Frank was in").

In the game's code from 27 October night, packaged with that night's build: the name rule on, before any call
(ClaimCheck.NameRule; refused there and then, no model asked); the wider form off until his word
(ClaimCheck.NameRuleWider). 14 core checks.

## 2. The source test (ledger/ClaimBench source; tools/checkers/source_test.py; raw F:/LedgerTools/checkers/source)

Each of 412 of the 617 rows (two in every three, the same rows in every version: his $20 did not cover all 617 three
ways once the facts list lengthened the prompt) asked its question again, as a newcomer's first question, of the game's
own reply model (Sonnet 5, by moment) with the game's own prompt, Monday 10:00; its raw first sentence kept, before any
check or rewrite; then the game's whole check on it (Haiku 5.5, unchanged in every version; the bench binary that ran
predates the name rule); then Gemini 3.8 Flash's label against the same facts the check read (the prompt that labelled
the 617). The versions: today's prompt; plus the check's own facts listed and "say only what this list says ...
deflect in character"; plus the facts numbered and each sentence followed by the numbers it uses in braces, taken off
before the check. **The 412 rows are 31 questions (three speakers), each asked about 13 times**, so the tests below are
paired by question (a sign test over the questions where the versions differ).

Per 300 first sentences written (Gemini's labels; harm by a fresh reader, blind to the version):

| | Invented written | Invented through the check | of which harmful | of which harmless | True refused by the check |
|---|---|---|---|---|---|
| Today | 28.5 (39 of 411) | 10.2 (14) | 5.8 (8) | 4.4 (6) | 35.0 (48; 12.9% of true) |
| Only the facts, else deflect | 6.6 (9 of 412) | 5.1 (7) | 0.7 (1) | 3.6 (5) | 35.0 (48; 11.9%) |
| Facts numbered and cited | 10.2 (14 of 410) | 4.4 (6) | 1.5 (2) | 1.5 (2) | 24.9 (34; 8.6%) |

- **Invented written falls by about three quarters** with the facts listed beside the rule, and that holds paired by
  question (today higher on 11 of 12 questions that differ, p = 0.006; cited, 10 of 12, p = 0.04).
- **Invented through, harmful through and true refused: not proven.** 14 to 7 and 6 through is p = 0.45 and 0.13 paired
  by question. Harmful 8 to 1 and 2: 5 of today's 8 come from one question ("What happens now?", the will misread), 4
  of the 8 are the reader's low-confidence calls, and near-identical cafe sentences were read harmful, harmless and not
  invented. True refused, today against cited, p = 0.19. Between the two new versions every difference is noise.
- The reader found 1 of the 7 and 2 of the 6 not invented after all (counted harmless or not invented, never harmful).
- **Today's harmful leaks** include the model reading Mickey's will as a man four times ("Will left you the office"
  twice), "his uncle's will" and "she's got a daughter"; with the facts listed, the cafe moved ("opposite end of the
  parade").
- **Gemini's labels, checked** (a second fresh reader, blind, 45 sentences: 30 refused as true, 15 passed as true): 27
  of the 30 refusals were supported on reading, 3 not (two today, one cited); 14 of the 15 passed were supported, one
  (cited) invented. So the false refusals may run about a tenth high, and the invented through may be undercounted
  (one in fifteen of the passed true, a wide range on so few).
- **Haiku is much weaker on the game's own inventions than on the 617's:** it lets through 14 of the 39 the game wrote
  today (36%) against 35 of the 308 Gemini wrote on purpose (11%; p = 0.0002). The game's own first sentences are
  invented about one in ten today (39 of 411); the 617 were half invented by design.
- **Cost and time:** the facts list adds about 2,500 tokens to the prompt: 1.00, 1.52 and 1.58 cents a reply at the
  game's price (+52% and +58%), and the draft's median time 1.62, 1.77 and 1.83 s (whole drafts of up to 150 tokens; the
  first sentence's own time not measured). The cited version left out its braces on 42 of 412 (10%).
- **The hard rule on names, on these sentences:** it stops none of the invented sentences through and refuses no true
  one, in any version; the wider form stops 1 (with the facts listed) and refuses none. "Will left you the office"
  opens a sentence with a lone name (the rule's known gap), and "will" is a word of the facts anyway.

Spent: $17.54 on the replies and checks (with the pilot), $0.32 on Gemini's labels: $17.86 of his $20.

**Fresh review (27 October, night): SOUND WITH FIXES**, all taken above: the tests paired by question (the through,
harmful and refusal differences no longer called falls); the recommendation of the cited version withdrawn (no
difference between the new versions is more than noise); Haiku's weakness on the game's own inventions added; the label
check read both ways; the wider rule re-measured without the fact IDs; the spend, the will and cafe sentences and the
low-confidence count corrected.

**For his page:** which version goes into the game. Recommended: "only the facts, else deflect", the plainer of the two
(no braces to drop), with the fewest invented written; the cited version is no better on this test. Either costs about
half again a reply and some 0.15 to 0.2 s a draft. Then it is measured live with the voice, and the fast checker's
cut-off measured again on what it writes.

## In the game (27 October, night; his page note "Facts cited")

- **The cited version is the game's prompt** (ConversationEngine.CiteFacts, on; the block word for word as measured,
  CitedFactsBlock, appended at the prompt's end; off with the plan first). Its braces are taken off before anything is
  checked, said, shown or remembered (WithoutCites: the whole reply, the second draft, and the streamed text from which
  the first sentence is cut early, a brace still being written included); what was cited is kept (LastCited). The bench's
  source mode now reads "today" as the prompt without it. 9 core checks.
- **Thirty real first turns through the game's whole path** (ClaimBench firsts at the game's switches, ten questions to
  each of the three; F:/LedgerTools/town-scratch/cited-firsts; $0.59): no brace or fact number in any reply; the first
  sentence written in a median 1.21 s against 1.08 s for the same questions on 26 October, and passed by its check in
  3.03 s against 2.85 s, inside the service's own swing between identical runs (3.3 to 7.0 s). 25 of the 30 first
  sentences passed the check, against 24 of 30 before.
- Not yet measured: a long run's refusals and wait, and the fast checker's cut-off on what this version writes.

## The wider rule on (28 October, his answer)

His answer of 28 October: "the wider hard rule, yes". ClaimCheck.NameRuleWider is on in the game: numbers, years and the
short list of places and roles the speaker's facts lack are refused before any call, as measured above (on the 617 it
stops 8 of Haiku's 35 leaks, all harmful, and refused no true sentence on any test).
