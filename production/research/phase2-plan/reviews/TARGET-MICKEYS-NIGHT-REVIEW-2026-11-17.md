# Review: TARGET-MICKEYS-NIGHT-2026-11-17.md (17 Nov 2026)

Verdict: PASS WITH FIXES.

Checked against the repository files the target cites (RULINGS.md "The look and the street", unreal-look.json, shop-interiors.json, mickeys-office.json, paint_wood_tile.py, gate-ritas-front/GATE.md). Web sources (Novak 2025, Wikipedia pages), the F: review files and the pictures were not opened: unchecked, not assumed. The studies/05-visuals.md and 1c/NIGHT files were not re-opened in this round either: unchecked.

## Must fix

1. **Conflicts with today's decision (lines 22, 46-48, 68, 75, 83-84).** Today's decision from canon: the front room is a working minicab office, lit at night; only Mickey's inner office stays dark. The target treats the front window as a locked dark room until the key (Aim B "night_dark", candidate 3, step 5, the Fail "a lit room before the key", Open question 1 recommending dark). Fix: rewrite Aim B so the lit front room is the normal night state (Aim B "lit" values become the main aim: window mean 80 to 110, clip at most 1%, 2 stops over lit pavement); drop or demote "night_dark" to the inner office only; delete the fail "a lit room before the key"; close Open question 1 as decided; reword candidate 3 (the room being dark is no longer a cause to keep, it is a spec to change: shop-interiors.json lit_at_start false and lit_note of 7 Oct, mickeys-office.json dark_until_inside, need a new record). Section 7 hours need a line for lighting the front room.
2. **Method steps follow the old premise (lines 64-68).** The split test "room lit (try value only)" becomes the baseline; step 4 (Rita's spill on Mickey's head) moves into try 1, since a lit office is the window's main light. Section 6 "before and after the key" cameras: change to front room (lit) and inner office (dark).
3. **Aim C spill has no number (line 50).** "No brighter than the lamp pool" is not pass/fail. Fix: give a ratio or luma bound on the flags, as Rita's gate did, and name its view. Also line 50 takes Rita's "216 to 105" from the "From the right" view (GATE.md line 69), not the hook view; say so.

## Should fix

4. **Aim B before-key and Aim A "separable, ratio 1.3" and "gilt 2:1"** are measurable, but the reverse night view has a camera named in section 6 and no aim or box tied to it. Add one box check or drop the camera.
5. **Aim B "room readable at least as on 8 Oct" (line 47)** rests on an unmeasured floor and a reviewer's naming: mark as judgement, or measure the 8 Oct box mean first as a step-1 output.
6. **Unreal-look.json line 187 verify text** ("letters at least 2:1") is quoted correctly; the "since 29 Oct 167" pool value is confirmed (lantern_pool_lumens 167; the 500 note is dated 8 Oct). The ground_coat_note's wording (3x) was not seen in the grep output (line omitted); recheck the quote.
7. **GATE.md lines 63-66:** the 98.5 and 108 means and "88" are confirmed (line 66). The "frame mean 16.2" was not seen in the lines returned; recheck.

## Checked and correct

- Reference-game line names methods (KCD2 plane light, Mafia wall-lamp spot) and says "none found" for a lit office front. Sound. Its study numbers were not re-opened.
- Paint (0.0625, 0.0875, 0.119) matches paint_wood_tile.py line 64. Arithmetic checks: 10x and 100x are 3.3 and 6.6 stops; 2 to 15 lux at 0.15 albedo gives about 0.1 to 0.7 cd/m2 (target says "0.1 to 1", acceptable).
- Reuse-first lists existing lights, materials, tools; missing pieces named.
- Unverified list counts 11 and matches the marked points. Hours sum to 6.5 h.
- RULINGS look section: nothing in the target contradicts "pools of lamp light with darkness between, lit windows, not one orange wash" (Aim C keeps pool-to-gap; "one orange wash" is a fail) or the day's exposure (listed under "Not changed"). A lit front room fits "lit windows".
- Source claims for lit_at_start false and dark_until_inside true are accurate to the files; they are now superseded for the front room only.
