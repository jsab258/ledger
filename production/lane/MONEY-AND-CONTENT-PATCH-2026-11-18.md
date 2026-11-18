# Money and content patch (18 November 2026)

1. The patch changes design notes in game-design/ only: in-game money from dollars to pounds, as the dollar list gives it, and the alcohol and gambling lines in current design notes.
2. 63 lines in 14 files: 52 money lines (every row the list marks for change; two of them, Victor's gambling marker and the slow beer, also fix the content rule), 10 more content-rule lines, and the "medical bills" town card.
3. Real-world US$ spending lines (asset shops, voices, the key) are untouched, as are the four lines describing the old switch to pounds.
4. Left for a decision: the six roadmap-history rows are in the patch but are history (the list calls them the builder's choice; drop those hunks to keep history as written); pub, bar and drink lines in logs, history and quoted samples are listed below, not changed.
5. Nothing was committed; the patch was checked with git apply --check on a clean tree.

## How to apply

From the repository root: `git apply production/lane/patches/money-and-content-2026-11-18.patch`

## What the content fixes say

- empire-roster.md 41: "a slice of his gambling marker cleared" becomes "a slice of his debt cleared".
- empire-roster.md 51, how-to-play.md 99, cast-tier1-batch2.md 46: the rival's first rung "slow beer" becomes "slow cup of tea" (same meaning: a Dockside man sitting a long time in your place).
- m15-the-world-speaks.md 28: "A drunk sings." becomes "Someone sings in the street."
- weapons-spec.md 652: "A bad drink and a long walk home." becomes "A dark night and a long walk home."
- open-city-spec.md 103: "protection/smuggling/gambling rackets" becomes "protection/smuggling rackets".
- imagegen-batch-2.md 89 to 103: betting shop, off-licence and amusement arcade dropped from the fascia list (~24 to ~21), bingo dropped from the posters (~16 to ~15). The game's own word rules (Core/ContentWords.cs 88 and 101) already count all four as gambling or drink.
- tier2-batch-1.json 2720 (design copy): "my sister's medical bills" becomes "my sister's rent arrears", the list's own replacement.

## Left as they are, for a decision or a later pass

- how-to-play.md 6 and counterparty-purses-spec.md 13 call Mickey's "your pub"; canon makes Mickey's a minicab office (D19). A pub as a place is allowed, so this is a canon tidy, not a content break. weapons-spec.md 654 says Tom Novak "runs a bar": same question.
- weapons-spec.md 249: describes Kingdom Come 2 reacting to "being drunk in daylight". A reference to another game, kept.
- Logs and history marked NOT CURRENT, left as records: writing-samples.md (87, 129, 213, 215, 245), writing-samples-before-fixes.md (54, 100, 104, 200), writing-check-free.md 115, research-openworld-audit.md (151, 191 "Gambling den as operating racket", 222), roadmap-history.md (395, 697, 1304, 1624, 1635), setting-britain-2026-07-31.md (82 to 224, the July pub plan, voided by D18).
- bark-names.json 618 to 623: "How's the pub treating you?" is generated from Core/StreetVoice.cs; fix it there (pub as place is allowed, but Mickey's is not a pub).
- Idioms (a bet, a gamble, betting the feedback) in weapons-spec.md 35 and 806, playtest-notes-2026-07-29.md 53, voice-pipeline-plan-2026-07-31.md 120, roadmap-history.md 532: not gambling, kept.
- Money in the forbidden folders was not touched, and the slow beer still lives in the Core: until the main session fixes the code below, the design notes say "slow cup of tea" and "debt" while the game text says otherwise.

## Hits in the forbidden folders, for the main session

Content rule (shown or spoken in the game):
- ledger/Assets/Scripts/Core/ActTwo.cs 50: "A Dockside man drinks one slow beer at your pub". Suggested: "A Dockside man sits over one slow cup of tea at your place".
- ledger/Assets/Scripts/Core/Empire.cs 1016: the same line.
- ledger/Assets/Scripts/Game/EmpireSetup.cs 93: "You quietly clear a slice of Victor's gambling marker." Suggested: "You quietly clear a slice of Victor's debt."
- ledger/CoreTests/Program.cs 4137: check name "the first slow beer".
- ledger/CoreTests/Program.cs 4642 and ledger/CoreTests/Program.Part3.cs 1403: beat "A drink for Mickey".
- ledger/Assets/StreamingAssets/Decals/generated/manifest.json 1247: "poster_bingo", bound to the amusement arcade window, Quay Street (1249).
- ledger/Assets/StreamingAssets/tier2-batch-1.json 2720: "my sister's medical bills" (game copy; the design copy changes in this patch).

In-game money in dollars (code, tests, harness):
- ledger/Assets/Scripts/Core/IntentRouter.cs 122 and 123: comments "Amount dollars".
- ledger/Assets/Scripts/Core/Access.cs 195 and 196: comment "forty dollars".
- ledger/Assets/Scripts/Core/Empire.cs 829: comment "a negative dollar figure".
- ledger/CoreTests/Program.cs 4240: message "no round ever reports a negative dollar".
- ledger/CoreTests/Program.Part2.cs 5038: comment "sixty dollars".
- ledger/SimHarness/Program.cs 526, 530, 666, 740: prompt text "about $120; you have $300", "$80 outstanding", "the bar took $180 yesterday", "the bar took $200 yesterday" (dollars and "the bar").
- ledger/BalanceLab/Program.cs 673: comment "Returns dollars spent".

Talk helper: no in-game dollars found; its US$ budget lines (TalkHelper/Program.cs, line 1363 and the budget flags) are real spending and stay.
