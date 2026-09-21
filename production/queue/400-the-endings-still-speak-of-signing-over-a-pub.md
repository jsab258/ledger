line: sim (ledger/Assets/Scripts/Core/ActThree.cs; wording only, under D43)
spec: Jafar, 2026-09-21 (second message): "The endings still speak of
  signing over a pub. D19 made Mickey's a minicab office. The logic
  survives, a private-hire licence settling who owns a cab firm the way a
  pub licence did. The wording is wrong and gets updated in the same
  pass." D19
  (ledger-v2/respec/decision-register/D19-mickeys-is-a-minicab-office.md):
  "Mickey's is a minicab office... Pubs remain as buildings on the street,
  boarded or serving food, never entered for drink." D43 governs this as a
  correction the studio applies and reports rather than a card.

  EVERY "pub" REFERENCE FOUND IN ActThree.cs AT FILING TIME, grepped
  case-insensitive; verify the count fresh at pickup since the file may
  move: comments describing the premise, "the pub's books," "the pub
  earned more than a pub on this street," lines 10 and 15; the excuse
  mechanics, "empire is too big for the pub to explain its own money," "a
  pub can plausibly account for washing about a third," lines 167 and 184;
  a strain-reading string, "the books look like a pub's books," line 197;
  the Quiet gate's own comment, "owns a pub; it does not settle a body,"
  line 283; the audit letter's flavour text, "Hook Street pub is required
  to produce its books of account, and its records of duty paid on stock,"
  lines 389 and 394; the epilogue text, "the pub opened on time," line
  573; and the ending flavour text itself, StraightLifeText, "The pub is a
  pub... You have a pub, and the hours are bad," lines 534 and 539, and
  EndingText's Both branch, "they are a pub's books," line 544.

  WORDING ONLY: the logic, thresholds, booleans, the shape of the audit,
  does not change. "Duty paid on stock" is alcohol excise and is
  pub-specific; its minicab-office equivalent is the firm's own accounts,
  fares, driver settlements, the vehicles' logbooks, per D19's own words
  about the information room, "a book of every fare... a radio nobody can
  help overhearing." Replace the pub-specific mechanics of the audit
  (excise duty on stock) with the cab-office equivalent named by D19, and
  the licence being signed over from a pub licence to a private-hire
  licence, everywhere the word "pub" currently carries that meaning.

  legacy/v1-era/act-drafts/act3-draft.md, cited in ActThree.cs's own
  header comment, is the pre-D19 design source this file was built from.
  It is legacy (queue 395's sweep may rule it only-history) and is not a
  live spec this item is required to edit, but if it is still cited as
  ActThree.cs's source-of-truth doc after queue 395 rules on it, note that
  as a follow-on rather than silently leaving it inconsistent.
acceptance: `dotnet run -c Release --project CoreTests` is green before and
  after, full count reported both times, matching, proving the logic is
  unchanged; grepping ActThree.cs for pub (case-insensitive, word
  boundary) after this item lands returns zero hits that describe
  Mickey's own business, a hit inside an unrelated word or a different,
  non-Mickey's pub building D19 explicitly keeps "as buildings on the
  street" is not a violation and is named as such if found; the ending
  flavour text (KingdomText, StraightLifeText, EndingText, the
  audit-letter text, the epilogue text) reads consistently as a minicab
  office throughout, with no sentence mixing a pub detail (duty on stock,
  "the pub is a pub") into a cab-office paragraph; and the change is
  reported as a D43 correction, what was wrong and what is now right,
  stated in one sentence, rather than carded to Jafar
max_sessions: 1
status: READY 2026-09-21, CHECKPOINT WORK NOW per his explicit marking and
  under D43. MAY START THIS WEEK, one of the two exceptions his second
  message names. Independent of queue 399; either may run first.

  RULED BY: D58 (the endings) and D19 (Mickey's is a minicab office), applied under D43. Jafar 2026-09-21: "the endings still speak of signing over a pub. D19 made Mickey's a minicab office. The logic survives, since a private-hire licence settles who owns a cab firm the way a pub licence did, but the wording is wrong and gets updated in the same pass." CHECKPOINT WORK NOW, the second of the two. The strings are in Core, so it is a builder's change WITH review.
