# G1 addendum: one native listener for the voices (18 Nov 2026)

Blind-spots recommendation 10, part 1. Adds to G1-FRIENDS-PLAYTEST-PLAN-2026-11-17.md, unchanged until the lines at the end are pasted.

## Why

RULINGS.md (30 Sep): voices are judged by ear; the accent checker is a screen, never a gate. So far the only ears are Jafar's (Swiss) and the AI's measures. Studies find that listeners place an accent best near where they grew up (Leach, Watson and Gnevsheva 2016, northern England, abstract only; Pinget and Voeten 2023, 1,578 Dutch listeners: for a speaker living nearest the listener, about 24% better recognition than average, the advantage fading with distance up to about 150 km). A 2026 synthetic-speech test found listeners who share an accent rate accent likeness higher than those who do not, on a 1 to 5 scale (CodecMOS-Accent, March 2026), so one listener's score is read beside the real recording's, never alone.

## The cast's voices by region

From RULINGS.md (line "The voices in the game", 3, 26, 27 Oct) and the VCTK inventory (production/research/voice-alternatives-2026-09-24/vctk-inventory.json):

| Person | Source voice | Region of the source | Note |
|---|---|---|---|
| Darren Milner | VCTK p286 | Newcastle | his pick, 26 Oct (production/casting/darren-milner/voice-2026-10-26/REVIEW.md) |
| June | VCTK p277 | North-East England | sheet: "near a local one but not it"; on the listening page of fitting voices (RULINGS.md, 27 Oct), so may change |
| Sheila Dunn | VCTK p267 | Yorkshire | |
| Ron Kirby | VCTK p227 | Cumbria | |
| Geoffrey Agar | VCTK p226 | Surrey | educated, by design |
| Danny Cammack | VCTK p243 | London | sheet flags it: Grimsby man |
| the dispatcher | VCTK p280 | France (accent "Unknown") | |
| Father Walsh | July voice (p245, Dublin, per father-emil/SHEET.md) | Dublin | sheet says Irish and needs an older voice; on the listening page (RULINGS.md, 27 Oct). REGULARS.md's Cork accent is his housekeeper Nora Cronin's, not his |

The town's own accent is the Humber's (production/casting/regulars/REGULARS.md; CASTING.md draws the town from Hull and Grimsby).

## Who to recruit first

1. A North-East listener (Tyneside first): covers two voices, Darren and June, and Darren's is the newest pick. Recommended first.
2. If a second turns up: someone from Hull, Grimsby or East Yorkshire, who hears Sheila (Yorkshire) and judges whether any voice could pass as the town's own.

## Who counts as a native listener

Grew up in the region, roughly from age 4 to 16 (the window Pinget and Voeten required of their speakers), or lived there at least ten years as an adult (estimate). Still hears the accent often (family, visits). Not Jafar, and not anyone who has heard the voices before.

## Finding one for free

Jafar asks friends, then friends of friends: "Anyone from Newcastle or the North East who could spare fifteen minutes listening to some voices?" Done remotely: the clips on a phone are enough; no game, key or PC needed. Paid panels (Prolific and the like) cost money: his call, not recommended.

## The listening protocol

- Clip set, fixed and versioned (named by voice version, like a handover): for each regional voice, three game lines spoken by the game voice, plus one real recording of the source speaker (VCTK, already on the allowlist, CC BY 4.0) as a control. About 8 seconds each; 8 clips for Darren and June, shuffled, labelled only by number.
- Blind: the listener is told some clips are made by AI and some are real people, not which. The key stays with the session.
- For each clip, written answers:
  1. Where is this person from? (free answer)
  2. Does this sound like someone from there? 1 (not at all) to 5 (exactly).
  3. Anything wrong: a word, a sound, a drift to another accent? Note the moment.
  4. Real or made? (guess)
- Afterwards: told which were which.

## The pass line (estimate, to be confirmed by his ruling)

A voice passes when, over its three game clips: the listener places it in the right region at least twice; the mean score is 4 or more; no clip scores 2 or lower; and the game clips average within one point of the real recording. One listener is a screen; two agreeing are a verdict.

## How results feed back

- A failed voice: one row in FINDINGS.md as a fault for the voices (person, voice version, score, the listener's words, the moment). Recasting touches identity, so it reaches his page with a recommendation; no recast without his yes (RULINGS.md, 24 Sep).
- A pass: noted beside the voice's approval (tools/approvals.py); it lapses when the voice changes.

## Consent and privacy

The listener's voice is never recorded; answers are written (paper, message or form). Stored under initials only, with the region and years lived there; deleted with G1's raw notes on the agreed date (within 30 days, as G1's consent line). Told beforehand what the clips are and that they can stop any time.

## Time

Listener: about 15 minutes (estimate: 8 clips of 8 seconds, four questions each). Session: about 2 hours to cut, level and key the clips; 30 minutes to sort results. Jafar: one message and passing on the answers, about 20 minutes. No money.

## Lines to paste into G1

Under "## The method, end to end", after step 4:

> 5. Native listener (addendum G1-NATIVE-LISTENER-ADDENDUM-2026-11-18.md): one friend or friend of a friend from the North East hears a fixed, blind clip set of Darren's and June's voices (and real recordings as controls), about 15 minutes, by phone; a Hull or East Yorkshire listener next if found. Free; no recording of the listener.

Under "## How findings are sorted", at the end:

> A voice the native listener fails (right region named on fewer than two of its three game clips, mean under 4, any clip 2 or lower, or the game clips more than one point below the real recording) is a FINDINGS.md fault for the voices; a recast goes to his page.

Under "## Rough hours":

> Native listener: clips 2 h, sorting 0.5 h, his time about 20 min (est.); no money.

## Sources (read 18 Nov 2026)

- Leach, Watson, Gnevsheva, "Perceptual dialectology in northern England", Journal of Sociolinguistics 20(2), 2016 (abstract page only): https://eprints.whiterose.ac.uk/id/eprint/124508/
- Pinget and Voeten, "Social factors in accent recognition", Cambridge University Press, 11 Jul 2023: https://core-prod.cambridgecore.org/core/product/3E0055501F7EC39C805CF7E1B5640B7A/core-reader
- CodecMOS-Accent, arXiv 2603.14328 (March 2026; same-accent bias, 1 to 5 accent-likeness scale): https://arxiv.org/html/2603.14328v1
- Alconost, "Why native-speaker testing matters in game localization", 10 Aug 2026: https://alconost.com/en/blog/game-localization-lqa
- Such A Voice, dialect coach on authentic game dialects, 30 Oct 2025 (believable and consistent over perfect): https://www.suchavoice.com/?p=34041
- Unreached: a dialect coach's or studio's written accent sign-off procedure for games; ICO guidance on informal surveys.
