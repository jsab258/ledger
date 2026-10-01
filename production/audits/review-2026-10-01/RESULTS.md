# Results of running the proofs, 1 October 2026

Run in this cloud session on main at e42623c (after the builder's and the town's fixes, and the screens pull request), with .NET 8.0.131 and g++ 13.3. The programs are in `probes/` beside this file. FAULTS.md says what each result proves and what it still leaves to reading.

## The repository's own test table

`bash tools/ci-checks.sh`: **passed 38 of 38** (3 min 23 s). Among them:
- CoreTests: "All 5055 checks passed." Soak: all 9. SaveChaos: all 149.
- The port: "57901 check(s), 0 failure(s) over 57864 golden row(s), 0 mismatch(es), 0 unanswered, 7 skipped"; the table regenerated from the C# (57872 rows) matches the committed one ("goldenDrift=no").
- crime-probe-test: "300 check(s), 0 failure(s)". route-week: "16 rows and 11 stops; the game's week gives the Core's". The talk program's self-test: 112 of 112. The fake playtest: 89 passed.

## The 30 September C++ proofs, run unchanged against the new headers

`production/audits/review-2026-09-30/probes/high-faults.cpp`, built as before. It still prints "PROVED" for A1, A2, A3 and B1, because it repeats the game's call sites as they were on 30 September (the diagnostic summary, the fixed light, the fixed key "player.window_d1", the `Waits` gate). The game no longer calls them that way, so those four lines prove nothing now; `recheck.cpp` below repeats the new call sites. A4 and A5 changed inside the headers themselves and no longer reproduce:

```
[A4] Can any witness in free play report him?
  best rung at any distance, full light, facing him: familiarity 0.0 -> 3; familiarity 0.35 -> 4
  WouldReport(damage), loyalty 0.5 (the default, never set in play): yes
  WouldReport(damage), loyalty 0.4: yes
  => not reproduced
[A5] Does the rung matter to the police?
  a rung-0 (heard only) story: WhoSheAsks = []; Loudness counts it: 0
  => not reproduced
```

## probes/recheck.cpp (the game's C++ headers, with the steps of CrimeProbe.cpp it names repeated)

Every sightline is assumed open (Unreal's trace cannot run here); people stand where `OnlookersAt` and `BodySpotFor` put them, facing `StreetFacingYaw`; Tom stands at Rita's glass facing it.

```

[A1, A2, A4] Who sees Rita's window go, from where, in what light (OnlookersAt, LightOnHim, FamiliarityFromMeetings)

  D0 12:00, day, light on him 1.00 (slots: 4 the act, 8 who it was done to, 16 who did it)
    rocco      fish_front       body     6.9 m   87 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    lena       fish_front       body     6.9 m   87 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    sam        fish_front       body     6.9 m   87 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    marla      fish_counter     window   7.8 m   62 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    rita       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    victor     ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    hal        hals_shop        window  23.1 m   60 deg off  rung 0  certainty 0.80  slots 12  files the damage heard
    zora       laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    iva        laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    selma      laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    tanja      laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    katarina   laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    ines       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    marta      ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    hana       pension_counter  window  17.4 m   49 deg off  rung 1  certainty 0.86  slots 60  files a story about him

  D0 16:00, day, light on him 1.00 (slots: 4 the act, 8 who it was done to, 16 who did it)
    rocco      mickeys_rank     body    11.4 m   91 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    lena       mickeys_office   body    12.9 m   87 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    zlata      mickeys_office   window  13.4 m   74 deg off  rung 0  certainty 0.00  slots  0  files nothing
    sam        mickeys_rank     body    11.4 m   91 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    rita       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    hal        hals_shop        window  23.1 m   60 deg off  rung 0  certainty 0.80  slots 12  files the damage heard
    iva        laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    tanja      laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    katarina   laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  slots  4  files the damage heard
    ines       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    marta      ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  slots 60  files a story about him
    jelena     mickeys_office   window  13.4 m   74 deg off  rung 0  certainty 0.00  slots  0  files nothing

  D0 21:00, night, light on him 0.00 (no lamp reaches him) (slots: 4 the act, 8 who it was done to, 16 who did it)
    rocco      mickeys_office   body    12.9 m   87 deg off  rung 0  certainty 0.40  slots  4  files the damage heard

  D0 21:00, night, light on him 0.60 (a lamp reaches him) (slots: 4 the act, 8 who it was done to, 16 who did it)
    rocco      mickeys_office   body    12.9 m   87 deg off  rung 0  certainty 0.40  slots  4  files the damage heard

  D1 02:00, night, light on him 0.00 (no lamp reaches him) (slots: 4 the act, 8 who it was done to, 16 who did it)
    nobody on Quay Street can see him

  the rung-0 branch, as the game files it for Sheila:
    files a story about him: no; a diagnostic's words anywhere: no; shouts: no
    her memory:
      "I heard glass go over at Rita's. I never saw who did it."

[A3] Darren holds Rita's window (day 0) at rung 1; what the talk and keep-quiet see now (DeedKeyNow = player.window_d0)
  deed field sent to the talk: ,"deed":{"topic":"player.window_d0","day":0,"hour":11}
  kept quiet suppresses player.window_d0: yes
  owning up files: player.window_d0 = "the new owner told me himself that he put Rita's window in", sensitive=yes
  the evidence the game sends, asked as "player.broke_a_window": held=NO; asked as "player.window_d0": held=yes rung=1

[A4] Can a witness in free play report him now?
  best rung at any distance, full light, facing him: never met -> 3; met on one day -> 4
  WouldReport(damage) for lena   at the middle (0.5): yes
  WouldReport(damage) for sam    at the middle (0.5): yes
  WouldReport(damage) for rocco  at the middle (0.5): yes
  WouldReport(damage) for rita   at the middle (0.5), never to police: no
  Darren recognised him (rung 4):
    D1 09:00 sam goes to the police (Statement)
    D2 10:00 the constable takes him in: Charged
    taken in: day 3, Charged
  Ron recognised him (rung 4):
    D1 09:00 rocco goes to the police (Statement)
    D2 10:00 the constable takes him in: Charged
    taken in: day 3, Charged
  Rita's staff saw his face, never having met him (rung 3):
    D1 09:00 ines goes to the police (Description)
    D1 09:00 marta goes to the police (Description)
    taken in: no

[A5] Does the rung matter to the police now?
  a rung-0 story: names him no; WhoSheAsks = []
  a rung-1 story: names him no; WhoSheAsks = []
  a rung-3 story: names him no; WhoSheAsks = []
  a rung-4 story: names him yes; WhoSheAsks = [lena]

[B1] Sheila's week's-end question, as the game now asks it (AsksNow at the office, then Ask)
  talking with her at the office at D6 10:30: she asks yes
  talking with her at the office at D6 11:59: she asks yes
  talking with her at the office at D6 12:05: she asks no
  talking with her at the office at D6 17:00: she asks no
  talking with her at the office at D7 10:00: she asks yes
  talking with her at the office at D8 09:00: she asks yes

[NEW] Over days 0 to 6, every hour: who OnlookersAt ever lists, and who the game ever lets him meet
  ever an onlooker: ada(7h) danica(1h) drago(12h) ferko(6h) franjo(6h) goran(6h) hal(43h) hana(14h) ines(44h) iva(54h) jelena(27h) june(10h) katarina(34h) lena(49h) luka(6h) marla(41h) marta(38h) noor(3h) outfit_man(7h) rita(39h) rocco(100h) sam(60h) sanja(5h) selma(48h) tanja(66h) tomas(6h) vesna(6h) victor(33h) zlata(79h) zora(46h)
  Ada ever an onlooker: yes
  onlookers he can ever have met, so who can ever name him (rung 4): ada lena rocco sam

[NEW] A rung-4 witness's words (the bank's three rung-4 clauses), now that rung 4 is reachable
  cw-ws-r4-01: "it was Nowak that put the window in on Quay Street, the new owner up at Mickey's, and there's no mistaking him" (says Nowak: YES)
  cw-ws-r4-02: "the new owner that's got Mickey's now, Nowak, put the window in, and he'd be known anywhere" (says Nowak: YES)
  cw-ws-r4-03: "the fella from Mickey's put the shop window in, Nowak, and he was seen clear enough that there's no question who he is" (says Nowak: YES)
  Darren holds his name: no; Ron holds his name: no; Ron's memory after an hour of talk says Nowak: YES
      "I heard from sam that it was Nowak that put the window in on Quay Street, the new owner up at Mickey's, and there's no mistaking him"

[NEW] Darren saw it at rung 4; Tom threatens him over it (Silence::FileThreat, as the game files the reply's "threatened")
  would report before the threat: yes; threat filed: yes; would report after it: YES

[NEW] A smash on Monday at 17:30: who is measured as an onlooker, and who the damage's tick says was there
  onlookers in Rita's area: lena
  joey    at ritas_step     (outdoors, no body): "I was there when somebody put Rita's window in. I never saw who did it."
  rita    at ritas_step     (outdoors, no body): "Somebody put my window in while I was there. I never saw who did it."
  victor  at ritas_step     (outdoors, no body): "I was there when somebody put Rita's window in. I never saw who did it."
  tibor   at ritas_step     (outdoors, no body): "I was there when somebody put Rita's window in. I never saw who did it."
  ines    at ritas_step     (outdoors, no body): "I was there when somebody put Rita's window in. I never saw who did it."
```

## probes/EllisRecheck (the C# Core and the real cast file)

The 30 September proof with one change: the stories carry no rung (a thing told as known), so the town's A5 rule does not leave them out. Full list for Wednesday; Thursday and Friday summarised.

```
[A11] Wednesday, D2 09:00: she asks 21 people; 0 of them are not on Quay Street; 2 never go to the police; her file takes talk from 19, 0 of them people who never go to the police
    ada         at adas_step            16 m from the window
    ferko       at mickeys_rank         11 m from the window
    franjo      at mickeys_rank         11 m from the window
    hana        at adas_step            16 m from the window
    ines        at ritas_counter         3 m from the window
    iva         at laundry_counter      11 m from the window
    jelena      at ritas_counter         3 m from the window
    joey        at quay                 24 m from the window
    katarina    at laundry_counter      11 m from the window
    lena        at mickeys_office       13 m from the window
    marla       at fish_counter          7 m from the window
    marta       at ritas_counter         3 m from the window
    noor        at laundry_front        11 m from the window
    outfit_man  at cafe                 13 m from the window  (never goes to the police)
    rita        at ritas_counter         3 m from the window  (never goes to the police)
    rocco       at mickeys_rank         11 m from the window
    sam         at cafe                 13 m from the window
    selma       at laundry_counter      11 m from the window
    tanja       at laundry_counter      11 m from the window
    zlata       at mickeys_office       13 m from the window
    zora        at laundry_counter      11 m from the window
[A11] Thursday, D3 09:00: she asks 21 people; 0 of them are not on Quay Street; 2 never go to the police; her file takes talk from 19, 0 of them people who never go to the police
[A11] Friday, D4 09:00: she asks 19 people; 0 of them are not on Quay Street; 2 never go to the police; her file takes talk from 17, 0 of them people who never go to the police
  each of them remembers: "DS Ellis, the detective, stopped me on Quay Street and asked me about Mickey's nephew, the new owner."
  => not reproduced
```

## probes/talk-continue.sh (the game's talk program, stand-in replies, no model)

```
[case 1] game 1: Tom tells Darren where he was; the 14:57 save sends the talk under G1
{"talk":"saved","people":1}
  game.talk.json: stamp=G1 people=1; Darren still holds 'the pictures': yes
  Continue: the 15:00 autosave comes before the program is ready: no talk save, the clock file keeps G1
  the program ready: the load goes out under G1; then a word with Darren; the next save under G3
{"talk":"loaded","people":1,"skipped":0}
{"talk":"saved","people":1}
  after the next save: stamp=G3 people=1; Darren still holds 'the pictures': yes
[case 2] as case 1 to G1; then a save with the program ready sends G2, and the game is closed before the program writes it
{"talk":"saved","people":1}
  Continue: the clock file says G2; the load goes out under G2; then the next save under G3
{"talk":"loaded","people":0,"stale":true}
{"talk":"saved","people":1}
  after the next save: stamp=G3 people=1; Darren still holds 'the pictures': NO
[case 3] the 30 September name, talk.json
{"talk":"save","error":"path-must-end-.talk.json"}
```

## The readers' runs

Each was run again by this session against the repository's own files, with the same output, except the save reader's 140 reloads inside an hour, quoted as it ran them.

### probes/readers/time/gamesim.cpp (the game's free-play clock mirrored over its own headers)

```
== gamesim tea-cells

[S1] Monday's window seen and recognised (rung 4) by Darren; then a wait from Wednesday 09:30
  [D0 12:00] the deed (Darren, rung 4)
  [D0 20:00] Ron's at the door with an envelope for you
  [D1 09:00] sam goes to the police about player.window_d0
  [D2 10:00] WAIT STOPS: "There's a constable asking for you." (constable@2)
  [D2 10:00] A constable: I'm arresting you on suspicion of criminal damage. You do no...  (out at D2 16:00)
  [D2 10:00] Ada, from her step: "There'll be a pot on at nine tonight, if you want it. I don't ask twice, mind."
  [D2 16:00] release: You are charged with the offence(s) shown below. Y...
  [D2 16:00] wait from D2 09:30 ended (stopped)
  tea state now 1 (1=Asked); custody holds at 10:30? yes
== gamesim ellis-false

[S3] No envelopes (he never goes down); Thursday (day 3) 17:00 Sheila, on Rita's step by her day, sees the window at rung 4. Friday he presses Z at 09:05.
  [D0 20:00] Ron's at the door with an envelope for you
  [D2 10:00] Ada, from her step: "There'll be a pot on at nine tonight, if you want it. I don't ask twice, mind."
  [D2 20:00] Ron's at the door with an envelope for you
  [D3 17:00] the deed; Sheila's place by her routine now: ritas_step
  [D4 08:59] loudness at 08:59: 2
  [D4 09:00] lena goes to the police about player.window_d3
  [D4 09:00] loudness after the 09:00 hour's events and its 09:00 round: 3; visits 0
  [D4 09:05] WAIT STOPS: "DS Ellis is on Quay Street, asking after you." (ellis@4)
  [D4 09:05] wait from D4 09:05 ended (stopped)
  DS Ellis's visits so far: (none on day 4)
  [D4 17:05] wait from D4 09:05 ended (ran out)
  [D4 20:00] WAIT STOPS: "Ron's at the door with something for you." (ron@4)
  [D4 20:00] Ron's at the door with an envelope for you
  [D4 20:00] wait from D4 17:05 ended (stopped)
  DS Ellis's visits so far: 
== gamesim ellis-false-night

[S3b] As S3, but he presses Z on Friday at 02:00 (asleep through the morning).
  [D4 09:00] lena goes to the police about player.window_d3
  [D4 09:00] WAIT STOPS: "DS Ellis is on Quay Street, asking after you." (ellis@4)
  [D4 09:00] wait from D4 02:00 ended (stopped)
  DS Ellis's visits so far: 0
  [D4 17:00] wait from D4 09:00 ended (ran out)
  [D4 20:00] WAIT STOPS: "Ron's at the door with something for you." (ron@4)
  [D4 20:00] Ron's at the door with an envelope for you
  [D4 20:00] wait from D4 17:00 ended (stopped)
  [D4 22:00] WAIT STOPS: "They'll be expecting the envelope at the landing after ten." (landing@4)
  [D4 22:00] wait from D4 20:00 ended (stopped)
  DS Ellis's visits: 
[S5] Ada's tea, judged (FirstWeek.h): first minute..last minute -> state
  21:00..22:29 -> LeftEarly, loyalty 0.55: Mickey's nephew came for his tea and was off again before the pot was cold. Somewhere to be, had he.
  21:00..22:30 -> Stayed, loyalty 0.75: Mickey's nephew came for his tea and sat with me till gone half ten. There's more to him than they're saying.
  21:45..22:40 -> Stayed, loyalty 0.75: Mickey's nephew came late for his tea, but he sat with me till gone half ten. There's more to him than they're saying.
  22:00..22:30 -> Stayed, loyalty 0.75: Mickey's nephew came late for his tea, but he sat with me till gone half ten. There's more to him than they're saying.
  22:01..22:59 -> LeftEarly, loyalty 0.55: Mickey's nephew came for his tea with the pot near cold and gone ten. Better late, I suppose.
  21:31..22:35 -> Stayed, loyalty 0.75: Mickey's nephew came late for his tea, but he sat with me till gone half ten. There's more to him than they're saying.
  21:05..21:05 -> LeftEarly, loyalty 0.55: Mickey's nephew came for his tea and was off again before the pot was cold. Somewhere to be, had he.
[S9] A window at D2 00:30 (Tuesday night), seen at rung 4 by Darren
  mended at D2 16:00; first report morning D2 09:00
  [D2 09:00] sam goes to the police about player.window_d2
  [D2 10:00] Ada, from her step: "There'll be a pot on at nine tonight, if you want it. I don't ask twice, mind."
  [D2 20:00] Ron's at the door with an envelope for you
  [D3 09:00] DS Ellis is on Quay Street this morning, asking after you. (talk)
  [D3 10:00] A constable: I'm arresting you on suspicion of criminal damage. You do no...  (out at D3 16:00)
  [D3 16:00] release: You are charged with the offence(s) shown below. Y...
```

### probes/readers/save/talk-probe.sh (the talk program, stand-in replies)

```
== 1. C1 under the current rules ==
 session 1: Tom tells Darren he was at the pictures; the reply's save: fresh stamp G1
    {"id": 1, "to": "sam", "reply": "Morning. Quiet one today.", "refusedAsk": false}
    {"talk": "saved", "people": 1}
   file: stamp=G1 people=1; holds 'pictures': True
 session 2 (Continue): an hourly save before the talk program is ready keeps G1 and sends no talk save;
  ready -> load G1; next save G2
    {"talk": "loaded", "people": 1}
    {"talk": "saved", "people": 1}
   file: stamp=G2 people=1; holds 'pictures': True
== 2. Ron's own question pending across a Continue (C5) ==
 straight:
    {"id": 1, "to": "rocco", "reply": "You want me to tell them no to the envelope, boss? That's Mickey's arr", "refusedAsk": false}
    {"id": 2, "to": "rocco", "reply": "Right you are, boss. I'll take your no down the landing.", "refusedAsk": true}
 with the 23:00 autosave between and a Continue (the game marks the first line after Continue fresh: GLive.Talked is empty):
    {"id": 1, "to": "rocco", "reply": "You want me to tell them no to the envelope, boss? That's Mickey's arr", "refusedAsk": false}
    {"talk": "saved", "people": 1}
    {"talk": "loaded", "people": 1}
    {"id": 1, "to": "rocco", "reply": "Funny business round here. The player said to me: \"Tell them no, Ron.\"", "refusedAsk": false}
 (and even without fresh):
    {"talk": "loaded", "people": 1}
    {"id": 1, "to": "rocco", "reply": "Funny business round here. The player said to me: \"Tell them no, Ron.\"", "refusedAsk": false}
== 3. Sheila's plain question pending across a Continue (C5) ==
 straight:
    {"id": 1, "to": "lena", "reply": "I don't come in Sundays. That's Mickey's real book. Everything he ran,", "refusedAsk": false}
    {"id": 2, "to": "lena", "reply": "Take it over, then? Mickey's arrangements and everything that comes wi", "refusedAsk": false}
    {"id": 3, "to": "lena", "reply": "Right. Then it's your book.", "refusedAsk": false, "weekAnswer": "TakeOver"}
 with the 11:00 autosave between and a Continue:
    {"id": 1, "to": "lena", "reply": "I don't come in Sundays. That's Mickey's real book. Everything he ran,", "refusedAsk": false}
    {"id": 2, "to": "lena", "reply": "Take it over, then? Mickey's arrangements and everything that comes wi", "refusedAsk": false}
    {"talk": "saved", "people": 1}
    {"talk": "loaded", "people": 1}
    {"id": 1, "to": "lena", "reply": "Funny business round here. The player said to me: \"Morning, Sheila.\"", "refusedAsk": false}
== 4. A talk save that fails removes the good file; the game has already written the new stamp ==
    {"id": 1, "to": "sam", "reply": "Morning. Quiet one today.", "refusedAsk": false}
    {"talk": "saved", "people": 1}
   file: stamp=G5 people=1; holds 'pictures': True
    {"talk": "loaded", "people": 1}
    {"talk": "save", "error": "unwritable"}
   slot file exists after the failed save: NO
 Continue with clock.txt's G6:
    {"talk": "loaded", "people": 0, "missing": true}
```

### probes/readers/save/reload-week (the route's week saved and reloaded part way; the hour ends re-run here in 4 minutes)

```
hour ends: 171 of 171 runs with rows differing 0, end states differing 0
inside an hour: 311 of 311 runs with rows differing 0, end states differing 0
```

### probes/readers/route (p3: the evidence, a threat, keeping quiet)

```
[F] familiarity from days met: 0:0.00 1:0.40 2:0.50 3:0.60 4:0.70 6:0.70
    IdRung at 1.5 m, daylight, met once: 4; never met: 3

[E] Darren holds player.window_d0 at rung 4, hop 0
    AccountOf("player.broke_a_window"): held=0 -> Derive Trusting 0.00
    AccountOf("player.window_d0"):     held=1 rung=4 -> Derive Confronting 0.89 (I saw it myself: a clause, and it was him, I would swear to it)
    DeedJson(window_d0) = ,"deed":{"topic":"player.window_d0","day":0,"hour":10,"sawHimAt":"ritas_step"}

[R1] Mon 10:30: Darren rung 4, Ines rung 3, Rita rung 3; nothing said to anybody
    D1 09:00: sam goes to the police
    D1 09:00: ines goes to the police
    D2 10:00: a constable takes him (player.window_d0)
    file: sam player.window_d0 how=2 day=1
    file: ines player.window_d0 how=1 day=1

[R2] the same; he threatens Darren over it at Mon 11:00 (Silence::FileThreat, as TakeClaimsFromReply does)
    threat filed=1; WouldReport after it=1
    D1 09:00: sam goes to the police
    D2 10:00: a constable takes him (player.window_d0)

[R3] the same; Darren keeps it quiet at Mon 11:00 (KeepQuiet with the deed field's topic)
    (nothing above = no report, no constable)

[B] rung-4 clauses filed as the story's summary:
    cw-ws-r4-01: it was Nowak that put the window in on Quay Street, the new owner up at Mickey's, and there's no mistaking him
    cw-ws-r4-02: the new owner that's got Mickey's now, Nowak, put the window in, and he'd be known anywhere
    cw-ws-r4-03: the fella from Mickey's put the shop window in, Nowak, and he was seen clear enough that there's no question who he is
familiarity 0.20: knowsItIsHim=0 knowing=Enough stance=Indifferent -> KnowingJson sends {"level":"nothing"}
familiarity 0.40: knowsItIsHim=1 knowing=Enough stance=Comments -> KnowingJson sends the story
his memory: I saw it myself: it was Nowak that put the window in on Quay Street
```
