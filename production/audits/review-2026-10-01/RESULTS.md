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

  D0 12:00, day, light on him 1.00
    rocco      fish_front       body     6.9 m   87 deg off  rung 0  certainty 0.40  files the damage heard
    lena       fish_front       body     6.9 m   87 deg off  rung 0  certainty 0.40  files the damage heard
    sam        fish_front       body     6.9 m   87 deg off  rung 0  certainty 0.40  files the damage heard
    marla      fish_counter     window   7.8 m   62 deg off  rung 0  certainty 0.40  files the damage heard
    rita       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    victor     ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    hal        hals_shop        window  23.1 m   60 deg off  rung 0  certainty 0.80  files the damage heard
    zora       laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    iva        laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    selma      laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    tanja      laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    katarina   laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    ines       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    marta      ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    hana       pension_counter  window  17.4 m   49 deg off  rung 1  certainty 0.86  files a story about him

  D0 16:00, day, light on him 1.00
    rocco      mickeys_rank     body    11.4 m   91 deg off  rung 0  certainty 0.40  files the damage heard
    lena       mickeys_office   body    12.9 m   87 deg off  rung 0  certainty 0.40  files the damage heard
    zlata      mickeys_office   window  13.4 m   74 deg off  rung 0  certainty 0.00  files nothing
    sam        mickeys_rank     body    11.4 m   91 deg off  rung 0  certainty 0.40  files the damage heard
    rita       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    hal        hals_shop        window  23.1 m   60 deg off  rung 0  certainty 0.80  files the damage heard
    iva        laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    tanja      laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    katarina   laundry_counter  window  11.7 m   72 deg off  rung 0  certainty 0.40  files the damage heard
    ines       ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    marta      ritas_counter    window   3.7 m   14 deg off  rung 3  certainty 0.94  files a story about him
    jelena     mickeys_office   window  13.4 m   74 deg off  rung 0  certainty 0.00  files nothing

  D0 21:00, night, light on him 0.00 (no lamp reaches him)
    rocco      mickeys_office   body    12.9 m   87 deg off  rung 0  certainty 0.40  files the damage heard

  D0 21:00, night, light on him 0.60 (a lamp reaches him)
    rocco      mickeys_office   body    12.9 m   87 deg off  rung 0  certainty 0.40  files the damage heard

  D1 02:00, night, light on him 0.00 (no lamp reaches him)
    nobody on Quay Street can see him

  the rung-0 branch, as the game files it for Sheila:
    files a story about him: no; a diagnostic's words anywhere: no; shouts: no
    her memory:
      "I heard glass go over at Rita's. I never saw who did it."

[A3] Darren holds Rita's window (day 0) at rung 1; what the talk and keep-quiet see now (DeedKeyNow = player.window_d0)
  deed field sent to the talk: ,"deed":{"topic":"player.window_d0","day":0,"hour":11}
  kept quiet suppresses player.window_d0: yes
  owning up files: player.window_d0 = "the new owner told me himself that he put Rita's window in", sensitive=yes

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
