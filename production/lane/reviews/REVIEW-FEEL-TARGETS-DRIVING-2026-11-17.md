# Review: driving feel targets, Fable round two prompt, scripted drives tool (17 Nov 2026)

Fresh, hostile reviewer, about 10 minutes. Pieces: production/research/lane/FEEL-TARGETS-DRIVING-2026-11-17.md (the sheet), production/lane/FABLE-DRIVING-NEXT-ROUND.md (the prompt), tools/lane/driving_drives.py with its README and tests.

## Verdict: PASS WITH FIXES

What holds:
- The game bands agree everywhere they appear. The sheet's table in (f), the tool's TARGET_SETS (ordinary and fast) and the prompt's FIRST_TARGETS block match number for number, M1 to M10, both sets, including the fast set with no 0 to 30 or 100 m target.
- Tests: 26 passed (python3 -m pytest -q tools/lane/test_driving_drives.py, run today).
- Two real-car figures checked at the source today, both correct: Vauxhall Nova 1.2 S, 739 to 750 kg, 55 hp, 0 to 62 in 16 s, 94 mph, 9.4 m turning circle (auto-data.net, [READ] 17 Nov 2026); Rover 820 Si (1986), 1,290 kg, 138 bhp, 0 to 60 in 10.5 s, 126 mph (uniquecarsandparts.com.au, [READ] 17 Nov 2026).
- Metric code reasoned through on one case, D5 step steer: with a first-order yaw response (time constant 0.25 s, settled 0.1 rad/s), the code takes the settled value as the mean of the last 0.5 s of the step, finds the first crossing of 63.2% and returns 0.25 s; on release with a 0.3 s decay it returns ln(20) x 0.3 = 0.90 s, the time after which yaw stays under 5%. Correct. The unit tolerance lookup was also run on the real keys and returns the right unit for each (deg, pct, s, g, m; ratios get relative tolerance only).
- Outside-only rule: no breach. The frame plan says watch in the browser, step frames, screenshot only, never download; no game files are read.
- Canon: the prompt bans real brands and models in names, badges and shapes; real cars appear only as ground truth; no alcohol, gambling or children anywhere. No em-dashes, no italics found.
- The prompt is self-contained and buildable: frame, controllers, drives, stage names, telemetry columns, results keys, tuning panel, gamepad, later features list, and "keep round one's code".

## Fixes

1. FEEL-TARGETS-DRIVING-2026-11-17.md, section (c) against the bands: the stated widening does not produce three of the bands. 30 mph braking: 15% shorter than 11 m is 9.35 m, the band says 9.5 m. Roll: 1.5 times 4.5 deg is 6.75, the band says 6. Braking pitch: 1.5 times 3.5 is 5.25, the band says 5. Either change the bands (and the tool and prompt with them) or add one line under the note before (c): "bands rounded inward on 30 mph braking, roll and braking pitch, by choice".
2. FEEL-TARGETS-DRIVING-2026-11-17.md, (c) M8 and M9: the fast set's grip band 0.82 to 0.95 g and the ordinary handbrake band of 90 to 180 deg are not explained by the "Where games depart" column (it names 0.85 g for the ordinary car only, and the ordinary real handbrake range is 90 to 150 deg). Add the reason in those two cells, or cut the bands to 0.82 to 0.90 g and 90 to 150 deg in all three pieces.
3. FEEL-TARGETS-DRIVING-2026-11-17.md, (g) last table row: "any gap over 10% is a finding" contradicts the 5% rule in "In short" and in (f) Pass rules, and the tool's default. Change to "outside the 5% (or unit allowance) rule in (f) is a finding".
4. FABLE-DRIVING-NEXT-ROUND.md, section 1, M6 lines: telemetry pitch is "positive nose up", so braking pitch comes out negative while the target reads "2 to 5 deg". Add after the M6 block: "Pitch targets are sizes (nose down under braking, nose up under throttle); compare the size, ignore the sign." The tool already takes the size.
5. FABLE-DRIVING-NEXT-ROUND.md, D2 and "Not this round" item 6: the drives need a wet road now, but item 6 says wet roads are for later. Add to D2: "Wet road for this drive only: multiply tyre grip by the tuning panel's wet grip factor; no puddles, spray or visuals." Reword item 6 to "Wet and damp road visuals, puddles and spray, and grip that varies across the road."
6. FABLE-DRIVING-NEXT-ROUND.md, section 6: name the standard mapping indices so the build does not guess: "triggers are buttons[7] (throttle) and buttons[6] (brake), read as .value; left stick sideways is axes[0]; A or cross is buttons[0]; most browsers show a controller only after a button is pressed, so say so on screen."
7. FEEL-TARGETS-DRIVING-2026-11-17.md, (d) item 12: the page read is the UE 5.9 vehicle setup page while the project is on Unreal 5.8. Add "(read on the 5.9 page; check the same settings exist in 5.8 before Unreal tuning)".

Not a fix to these pieces, for the session: the project's CLAUDE.md "Reference first" line still says to look at Mafia's or Kingdom Come II's "files on demand" and has a "Game extracts" rule, which conflicts with his 17 Nov outside-only rule that this sheet follows. That line needs his ruling or an update.
