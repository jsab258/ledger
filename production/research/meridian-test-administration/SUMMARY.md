# Running the Meridian Test on friends without fooling yourself

STATUS: SPEC (research delivery). Branch `research/meridian-test-administration`.
Written 2026-09-19. Audited against `BRIEF.md` in this folder, written first.

NOTHING HERE IS AN INSTRUCTION.

## 0. Sourcing

`en.wikipedia.org` is open (200) and **four articles were read in full**:
Demand characteristics, Acquiescence bias, Social-desirability bias, Think-aloud
protocol. Two web searches for practitioner advice; those hosts
(`gamedeveloper.com`, `nngroup.com`, `userinterviews.com`, `itch.io`,
`antidote.gg`, `howtomarketagame.com`) are refused here, so that half is search
summary and labelled CITED-SUMMARY.

## 1. The bias has a name, a mechanism, and no cure

CITED, Wikipedia, Demand characteristics: participants "form an interpretation
of the experiment's purpose and subconsciously change their behavior to fit that
interpretation". The specific role Jafar described is named in the literature:

> The **good-participant role** (also known as the **please-you effect**) in
> which the participant attempts to discern the experimenter's hypotheses and to
> confirm them.

And the honest bound, quoted because it sets the whole shape of this delivery:

> Demand characteristics cannot be eliminated from experiments, but demand
> characteristics can be studied to see their effect on such experiments.

CITED, Acquiescence bias: "yea-saying", "the tendency of a respondent to agree
with a statement when in doubt", and it is specifically triggered by a format:
"a stimulus in the form of a statement is presented, followed by
'agree/disagree', 'yes/no' or 'true/false' response options". Its cause is
social: "pressure to conform to such norms and conventions prompts people to
agree".

DERIVED, and it is the single most actionable line in this file: **"Did the town
feel alive?" is the worst possible question.** It is a yes/no stimulus, which
invites yea-saying; it names the hoped-for property, which supplies the
hypothesis; and it is asked by the maker, which activates the good-participant
role. All three failure modes fire at once.

## 2. The standard defence is unavailable, and the substitute is separation

CITED, Wikipedia: the named mitigation is **double blind**, "do not inform the
person who has contact with the participants about the research hypotheses".

DERIVED: a one-person studio cannot run double blind in its textbook form,
because the person with participant contact is the person with the hypothesis
and also the person whose game it is. What survives of the principle is
**separation of roles across time and medium** rather than across people:

- The maker is not in the room, or is silent and out of the player's eyeline.
- The open question is asked by an instrument rather than a person, which is
  what CITED-SUMMARY practitioner advice independently recommends: "people will
  not want to give negative feedback to your face, but are much more likely to
  leave more honest feedback on an anonymous form".
- Nothing about the moat is said before the session. A friend who has heard
  about social memory will look for it and will find it.

## 3. The test is already well designed, if it is administered in the right order

This is the finding that surprised me. Condition 3 of the Meridian Test reads
"they describe the town as alive **without being prompted**". That is not an
opinion question. It is an **observable event**: either the description occurred
unprompted or it did not.

DERIVED: the condition is already written as behaviour rather than as a rating,
and it is only destroyed by administration. The order that preserves it:

1. Play, with the maker not asking anything.
2. One open question, in writing, that names nothing: "tell me about the half
   hour you just had." Record whether aliveness, being recognised, or a specific
   person appears unprompted. That is the measurement, and it is binary.
3. Only then, specific questions, whose answers are worth much less and should
   be recorded separately so they cannot be confused with step 2.

Step 2 must come before step 3 forever, because once you have named the thing
you cannot unname it, and every later session with that friend is contaminated.

## 4. What to observe instead of asking

CITED-SUMMARY: "studios don't ask 'Did you like it?' but observe what players
actually do." CITED, Wikipedia, Think-aloud protocol: it is the standard
usability instrument, participants verbalising while working.

DERIVED, and offered as candidates rather than a specification, because these
are the behaviours that would distinguish this game from a pretty street: did
the player go back to a person they had already met; did they follow up a rumour
without being told to; how long until they voluntarily started a conversation;
did they later refer to anyone by name; did they change behaviour after being
recognised. Every one of those is loggable by the game itself rather than
scored by a watching friend.

HOLE: a think-aloud protocol is itself intrusive and changes what it measures.
For a game whose whole claim is immersion, narrating aloud may damage the thing
being tested. I found no source addressing that specific conflict.

## 5. When a friend's session is worth nothing

DERIVED throughout from sections 1 and 2, stated as a checklist because the
brief asked when rather than whether:

- The maker asked a yes/no question that named the property. Worthless for
  condition 3, and it also spends the friend, who cannot be asked again.
- The friend knew what the project is trying to prove. Worthless for condition 3
  specifically, still useful for condition 1, the visual bounce test, which is a
  reaction rather than a judgement.
- The friend was told the maker's hope during play.
- The session was their second. First impressions are consumed once.

And when it is worth something: a first session, cold, with no framing, where
the only question comes afterwards and in writing.

## 6. Sample size, and the number everyone quotes is a median

CITED-SUMMARY: Nielsen's finding that five participants identify approximately
80 percent of usability problems, with the practitioner range at five to ten.

**And the caveat matters more than the number**, CITED-SUMMARY: "some random
sets of 5 participants identified up to 99% of the issues, while others
uncovered just 55%. With 10 participants, the minimum percentage of issues found
by any set rose to 80%."

DERIVED, and this is rule 2's case: 80 percent at five is an average over
samples, not a property of any five people you actually have. The spread from 55
to 99 is the real finding, and the way to buy down that variance is the tenth
participant, not the fifth.

DERIVED, and it is a different point: the Meridian Test is not a usability
study. Conditions 1 and 3 are proportions of people, so five is a very thin
denominator for a yes-or-no about human reaction. Five friends who all say the
town feels alive is 5 of 5, and 5 of 5 is consistent with a true rate anywhere
from about half to certain. The test does not currently say how many people must
pass it, and that is a gap in the test rather than in this research.

## 7. The condition nobody can administer, which is condition 4

Condition 4 is Jafar, on a free evening, choosing LEDGER over replaying KCD2.
Every bias in section 1 applies to the maker judging his own game, at full
strength, with no possibility of blinding.

DERIVED, and offered because it is cheap: that condition is also behaviour, and
behaviour is loggable. What was launched, on which evenings, for how long,
recorded automatically and read later, is a harder fact than a memory of
preferring it. Nothing here needs to be asked.

## 8. What could not be established

1. **Any practitioner source read in full.** All six are refused hosts, so
   section 2's form advice, section 4's observation advice and section 6's
   numbers are search summaries.
2. **Whether think-aloud damages an immersion test** (section 4).
3. **Any game-specific protocol.** Everything found is general usability
   research or indie marketing advice; nothing addresses testing a simulation's
   aliveness.
4. **What pass rate the Meridian Test requires** (section 6). That is Jafar's to
   set and the test does not say.
5. **Nielsen's original figures at first hand.** The 80 percent and the 55-to-99
   spread are summaries of summaries.

## 9. Sources

Read in full, `en.wikipedia.org`, 2026-09-19: Demand characteristics;
Acquiescence bias; Social-desirability bias; Think-aloud protocol.

Search channel summaries, none opened: gamedeveloper.com (two articles),
nngroup.com, userinterviews.com (two articles), antidote.gg,
howtomarketagame.com, firstlook.gg, closedbeta.substack.com.
