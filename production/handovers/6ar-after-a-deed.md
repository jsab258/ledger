# After a deed: the damage, the police, DS Ellis, an arrest

Town list 6br, 6ar, 6bj, 6bq, 6bp, 6bu, 6bm and 6bt. Settled or decided by the
town, 29 September. Design: game-design/ellis-2026-09-29.md,
police-asking-2026-09-29.md, arrest-2026-09-29.md and
arrest-words-2026-09-29.md. Code: ledger/Assets/Scripts/Core/TownNews.cs
(Aftermath), PoliceFile.cs and Custody.cs.

**What the player gets, for the slice's one crime (Rita's window):**
- The damage is found in the morning and becomes the street's news, naming
  nobody.
- A witness who saw him plainly, is not afraid and has cooled on him goes to
  the police.
- A constable takes him from wherever he is at ten the next morning. He is held
  some hours, cautioned or charged, and let go with plain words. The street
  that saw it talks.
- If the street's talk of him gets loud, DS Ellis comes asking about him, and
  that becomes talk too.

## Wire it, in the order play meets it

1. **At the deed:**
   - Make an `Aftermath(area, key, "somebody put Rita's window in", doneAt, mendedAt or null, whoSawTheDeed)`
     and keep it in `TownSave.Damage`. A null `mendedAt` means the next working
     day at four; those who saw the deed itself never "find" it.
   - Grade the deed (`Offence`).
   - For its victim and each witness, ask
     `PoliceFile.WouldReport(g, offence, victim, topic, cast.NeverToPolice(id))`,
     and for each who would, `police.Report(who, topic, offence, theirRung, day)`.
2. **Every game hour, and after a load:** `aftermath.Tick(mill, cast, now)`.
   Whoever comes into the area finds it, once.
3. **Each morning at nine:** `police.EllisComes(mill, day, inquiry)` until it
   returns null.
   - On "talk": `police.HearTheStreet(mill, day, grading, cast, now)` (only the
     people on the street then, the ones she asks).
   - For any reason but "body":
     `PoliceFile.Asked(mill, PoliceFile.WhoSheAsks(mill, cast, now), reason, now)`
     (only the people on the street then).
   - Put Ellis on Quay Street for the visit. What she puts to him is
     `police.Strongest(topic)`. Her words wait on her talk card.
4. **Each morning at ten:** if `police.ConstableComes(today, now)` gives a deed (or
   Ellis's visit is for a crime where `CanArrest` holds), take him where he is:
   - `custody = police.TakeIn(deed, now, ownedUpInTalk, woreTheCoat)`; null
     means no arrest;
   - `Custody.SeenTaken(mill, cast, area, now)`;
   - the arrester says `custody.ArrestWords()`, and the station shows
     `Custody.Rights`;
   - black the screen to `custody.OutAt`, and take the coat off him if
     `CoatKept`;
   - keep it in `TownSave.Arrests`;
   - while `custody.Holds(now)`, Ron cannot reach him with an ask;
   - when he is out, show `custody.ReleaseWords()` plainly on screen.
5. **Session record:**
   - a `police` line (`who`, `story`, `how`) for each report;
   - an `ellis` line (`why`, `day`) for each visit;
   - a `taken` line (`story`, `day`, `end`) for each arrest

   (production/specs/session-record.md).

## Port

`Aftermath`, `PoliceFile` (with `NeverToPolice` from the cast file), `Custody`,
and StreetVoice's banks recognition/police-asked, police-heard, taken-saw and
taken-heard. `StoryThatShows` takes `PoliceFile.IsAsking` and `Custody.IsTaken`,
and `RegardFor` leaves the asking out of the pressure. Match the rows behind
`--awaiting-port`: `CustodyTake`, `CustodyNextSitting`, `CustodyIsTaken`,
`RecognitionTaken`, `TakenShows`, `PoliceIsAsking`, `RecognitionPolice`,
`PoliceShows`, `PoliceRegard` and `AskedAboutBody`.

Once the port matches, move `EmitPoliceAsked` above the awaiting line.

## Voices

- Crowd-voice clips for the twelve police-asking and police-heard lines, and
  for the taken-saw and taken-heard banks.
- The arrest words and release words, if voiced at all, only from the approved
  cast. The 1990 caution is safe to voice.
- Ellis's own words wait on her talk card.

## Save

`TownSave.Police`, `TownSave.Damage` and `TownSave.Arrests`: the town's pieces
travel as one `TownSave`, its `ToJson` beside the game's save and
`TownSave.FromJson` on a load. A later version is refused, as the game's save
is.

## Walk it

1. Put Rita's window in at night, seen by nobody. In the morning, whoever comes
   into the pawn finds it, and by noon others are talking of it, naming nobody.
2. In a second run, let Ada see it after he stood her up. The next morning at
   ten a constable takes him from the office, and the people there see it. He
   is out by four, charged, with the day he answers on screen.
