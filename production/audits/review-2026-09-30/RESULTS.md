# Results of running the proofs, 30 September 2026

Run in this cloud session on the review branch (main at 565e94ea plus the review), after the local history was replaced with a shallow copy and .NET 8.0.131 was installed from Ubuntu's archive (Jafar's approval, 30 September). The programs are in `probes/` beside this file; FAULTS.md says what each result proves and what it still leaves to reading.

## The Core's own test table, run here

`bash tools/ci-checks.sh`: **passed 37 of 37**. Among them:
- CoreTests: "All 5034 checks passed."
- Soak: all 9 checks passed. SaveChaos: all 149 checks passed.
- The port comparison: "57716 check(s), 0 failure(s) over 57679 golden row(s), 0 mismatch(es)"; the table regenerated from the C# matches the committed one.
- StrangerTest, the talk program's self-test, the route-week test and the fake playtest (89 passed).

GitHub's run 317 on the same commit gave the same 37 of 37.

## probes/high-faults.cpp (the game's C++ headers, g++ 13 with the repository's Unreal shim)

```

[A1] Sheila's stand-in and Rita's window (line to the glass open)
  her heading -159.4 deg; to Tom 9.90 m at 154.8 deg off axis; to the glass 9.87 m at 161.1 deg
  observation: filed=yes rung=0 certainty=0.40
  bank line for rung 0: NONE (no-line-at-witness_summary-rung-0)
  filed summary: "bank-unreadable/none"
  her memory now: "I think I saw it, couldn't swear to it: bank-unreadable/none"
  => PROVED: the town is handed the diagnostic string as her account

[A1] Sheila's stand-in and Rita's window (line to the glass BLOCKED)
  her heading -159.4 deg; to Tom 9.90 m at 154.8 deg off axis; to the glass 9.87 m at 161.1 deg
  observation: filed=no rung=0 certainty=0.00
  => nothing filed in this variant

[A2] The light a witness reading is judged in
  VantageOf gives light 1.00 to the actor and 1.00 to the window, whatever the hour (kLightLevel)
  at 12 m, on axis, light 1.0: sees him yes, best rung 1
  at 12 m, on axis, light 0.3: sees him yes, best rung 1
  at 12 m, on axis, light 0.1: sees him no, best rung 0
  => PROVED: the reading is fixed at full light; darker light would change what a witness sees

[A3] Darren holds Rita's window at rung 1; what the talk and keep-quiet see
  the story he holds: player.window_d0   the key the talk asks with: player.window_d1
  deed field sent to the talk: (EMPTY: no deed, so no keep-quiet, owning up or threat)
  kept quiet: [player.broke_a_window, player.was_near_the_deed, player.at_window_d1]; suppresses player.window_d0: NO
  owning up files: player.broke_a_window = "the new owner told me himself that he broke Mickey's window", sensitive=no
  => PROVED: the talk is never told the real deed, and keeping quiet leaves it spreading

[A4] Can any witness in free play report him?
  best rung at any distance, full light, facing him: familiarity 0.0 -> 3; familiarity 0.35 -> 4
  WouldReport(damage), loyalty 0.5 (the default, never set in play): NO
  WouldReport(damage), loyalty 0.4: yes
  => PROVED: with the game's familiarity (0.0) no reading reaches rung 4 (a Statement), and at the default loyalty nobody reports

[A5] Does the rung matter to the police?
  a rung-0 (heard only) story: WhoSheAsks = [lena]; Loudness counts it: 0
  => PROVED: a story from someone who only heard glass break marks her for DS Ellis's questions about him

[B1] Sheila's week's-end question (TownWeek's WeeksEnd, day 6)
  Waits(D6 10:30) = yes
  Waits(D6 11:59) = yes
  Waits(D6 12:05) = no
  Waits(D7 10:00) = no
  but Ask(D7 10:00) itself accepts: yes
  => PROVED: the gate the game calls first (Waits) is shut after Sunday noon, though the week's own Ask would still put the question
```

## probes/talk-stamp.sh (the game's talk program, stand-in replies, no model)

```
[game 1] Tom tells Darren where he was; the save goes out as G1
{"id":1,"to":"sam","day":1,"reply":"Morning. Quiet one today.","rest":null,"ms":160,"offline":false,"timedOut":false,"paused":null,"ends":false,"heard":[],"susp
{"talk":"saved","people":1}
  talk.json: stamp=G1 people=1
[Continue] the load goes out as G2 (an autosave replaced G1 before the talk program was ready); then the next save, G3
{"talk":"loaded","people":0,"stale":true}
{"talk":"saved","people":1}
  talk.json: stamp=G3 people=1; Darren still holds 'the pictures': NO
  => PROVED: the load was refused as stale and the next save wrote the loss over the good file
```

## probes/EllisProbe (the C# Core and the real cast file)

Set up as the committed golden row `SweepAsked` is: every cast member holding a sensitive story of his window. The full list for Wednesday; the two other days summarised.

```
[A11] Wednesday, D2 09:00: she asks 36 people; 15 of them are not on Quay Street; 4 never go to the police; her file takes talk from 36, 4 of them people who never go to the police
    ada         at adas_step            16 m from the window
    bruno       at harbour_office      119 m from the window  NOT ON QUAY STREET
    danica      at flats               126 m from the window  NOT ON QUAY STREET
    dario       at ferry_stop          127 m from the window  NOT ON QUAY STREET
    drago       at warehouse_row       159 m from the window  NOT ON QUAY STREET  (never goes to the police)
    emil        at chapel               81 m from the window  NOT ON QUAY STREET
    fabjan      at docks                79 m from the window  NOT ON QUAY STREET
    ferko       at mickeys_rank         11 m from the window
    franjo      at mickeys_rank         11 m from the window
    goran       at docks                79 m from the window  NOT ON QUAY STREET
    hana        at adas_step            16 m from the window
    ines        at ritas_counter         3 m from the window
    iva         at laundry_counter      11 m from the window
    jelena      at ritas_counter         3 m from the window
    joey        at quay                 24 m from the window
    katarina    at laundry_counter      11 m from the window
    lena        at mickeys_office       13 m from the window
    luka        at repair_yard          91 m from the window  NOT ON QUAY STREET
    magda       at chapel               81 m from the window  NOT ON QUAY STREET
    marla       at fish_counter          7 m from the window
    marta       at ritas_counter         3 m from the window
    noor        at laundry_front        11 m from the window
    outfit_man  at cafe                 13 m from the window  (never goes to the police)
    petra       at ferry_stop          127 m from the window  NOT ON QUAY STREET
    rita        at ritas_counter         3 m from the window  (never goes to the police)
    rocco       at mickeys_rank         11 m from the window
    sam         at cafe                 13 m from the window
    sanja       at boarding_house      121 m from the window  NOT ON QUAY STREET
    selma       at laundry_counter      11 m from the window
    stipe       at docks                79 m from the window  NOT ON QUAY STREET
    tanja       at laundry_counter      11 m from the window
    tibor       at customs_shed        124 m from the window  NOT ON QUAY STREET  (never goes to the police)
    tomas       at repair_yard          91 m from the window  NOT ON QUAY STREET
    vesna       at chapel               81 m from the window  NOT ON QUAY STREET
    zlata       at mickeys_office       13 m from the window
    zora        at laundry_counter      11 m from the window
[A11] Thursday, D3 09:00: she asks 36 people; 15 of them are not on Quay Street; 4 never go to the police; her file takes talk from 36, 4 of them people who never go to the police
[A11] Friday, D4 09:00: she asks 36 people; 17 of them are not on Quay Street; 4 never go to the police; her file takes talk from 36, 4 of them people who never go to the police
  each of them remembers: "DS Ellis, the detective, stopped me on Quay Street and asked me about Mickey's nephew, the new owner."
  => PROVED: people whose routine has them off Quay Street are asked, and remember being stopped on Quay Street
```
