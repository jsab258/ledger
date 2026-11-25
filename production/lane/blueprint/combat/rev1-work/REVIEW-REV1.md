# Review of revision 1 (combat and stealth), 25 Nov 2026

Fresh reviewer; did not write the revision. Checked the changed parts of COMBAT-SYSTEM.md against his decisions of 25 Nov, the simulator (SIM/combat_sim.py, revision 1), its results and the research files. The simulator was rerun (seed 1990, n 2000, to a scratch file): its output matches results.json exactly, so every mismatch below is text against code, not a stale run. Canon: no break found (no drink, gambling or children; tobacco only as allowed; every make fictional; fists capped at serious with the fall as the only fist-fight death, as his ruling says).

Most serious first.

## 1. CS-31's knife-arm claim is false in the simulator
- Where: COMBAT-SYSTEM.md CS-31 Test ("an unarmed careful Frank breaks or cuts the knife arm in about 1 fight in 4 (arm out 0.27 a fight); face marks come in about half of knife fights"); combat_sim.py land() and aim_line().
- Fault: Frank's fists can never reach the knife man's arm. A guarded fist blow returns with no harm (only a weapon heavy breaks through onto the arm) and an unguarded blow is aimed only at head or torso. In "1v1 vs knife man patient" dropped_weapon_per_fight is 0.0. The 0.283 arms out and 0.533 face marks are the log's totals for both men: they are Frank's own forearm cut by slashes on his guard, and Frank's face slashed. The same table claims "a bat's heavy blow on a forearm" breaks it; in code a guarded bat heavy does about 3.6 against the 6 needed, so it takes two.
- Fix: log arm_out, face_mark and dropped_weapon per side (frank_ and foe_); rewrite the CS-31 Test from the split counts; add a "1v1 Frank bat vs knife man" scenario if CS-34's first can-you is to be shown; correct the bat line to "two heavy blows on a guarding forearm" or raise the guarded break-through factor.

## 2. A hidden roll still decides whether a committed blow is blocked
- Where: combat_sim.py react() (`if self.rng.random() < p`, p = defence); chance rule, CS-02, CS-05.
- Fault: when Frank commits a heavy (which "cannot be cancelled") at a man facing him and not mid-swing, a fresh per-blow coin with his defence value decides if the guard comes up. The text calls this the man's choice "shown before the blow lands", but the player cannot act on it once committed, and the same man in the same state blocks or not by the flip. That is the kind of roll his decision 1 forbids ("unaimed blows land by the attack's line and the men's positions, not a dice table").
- Fix: make the guard deterministic from readable state: he raises it if he faces the attacker, is not mid-swing or emptied, and his reaction time by kind (seeded per man, e.g. boxer 0.35 s, brawler 0.65 s) is shorter than the wind-up. A jab then beats a slow man's guard and a heavy does not, every time, and the player learns it. Rerun and update every fight number.

## 3. CS-13: a cosh's second blow on a man out is already critical
- Where: CS-13 ("A second blow on the man out is serious; a third reaches critical"); combat_sim.py land() with finishing=True.
- Fault: probed directly: the cosh from behind leaves head harm 9.26; a second heavy at full wind adds 6.18, giving 15.44, critical and dying. Only below about 0.95 wind is the second blow serious. The heed-the-cue scenario stops at serious, so this jump from hurt to critical carries no cue, which is why CS-14 still shows 2.5 deaths per 1,000 for a player who heeds it. His decision 2 wants danger readable as it gets worse.
- Fix: either cap a single finishing weapon blow to one level up (hurt to serious, serious to critical), so the cue always comes before a killing blow, or correct the CS-13 text to "a second blow can already be critical" and state the 2.5 per 1,000 there.

## 4. Knock-down threshold counts the blow's own harm
- Where: combat_sim.py land(): `tgt.dmg[z] += ...` runs before `steady = 1.0 + tgt.dmg["head"] / kd_head_soak`; CS-05 ("a head blow from force 3.4").
- Fault: the blow makes the man less steady before it is tested, so on a fresh man the real head threshold is about force 2.3, not 3.4. Every landed fist heavy to the head floors a fresh man; the fist from behind floors him even at Frank's wind 0.7 (force 3.3), where CS-13's "every time" should depend on Frank's breathing. The variable is also named backwards (higher steady means easier to drop).
- Fix: compute steadiness from head harm before this blow; rename it unsteady; rerun.

## 5. The reload check cannot fail for most draws, and some violent-end draws are not fixed to the save
- Where: combat_sim.py reload_check(); finish() (`helped = self.public and self.rng.random() < 0.55`); knockdown() (`self.rng.random() < self.place["near_edge"]`); gun_table() `helped`; chance rule bullet 4.
- Fault: the check reseeds the same stream and replays, so any draw from that stream passes; it fails only for unseeded randomness (tested: swapping fixed() for an unseeded draw makes it fail, but drawing from the run's stream would pass). Whether a dying man is helped, and whether a spent man falls at the edge, come from the run stream, so in a game where unrelated choices before the reload shift that stream, the death can reroll.
- Fix: draw helped and near-edge through fixed() keyed to the act (or make them deterministic from bystander count and position); add a check that calls edge_wound, the fall and the dying draw with the same save and act key under two different rng seeds and asserts identical results.

## 6. Numbers in the text that do not match results.json
- CS-11 Test: says 2 v 1 careful wins 29% (43% lost, 28% stopped), 3 v 1 1% (84% lost), with Ron 78%. Results: 25.7% (43.0, 31.4), 0.7% (79.5), 72.4%.
- CS-09 Test: "about 2 in 5 men yield and 1 in 7 run". Results: yielded 0.24 and fled 0.12 a fight (1 in 4, 1 in 8).
- CS-14 Test: "about 15% ended by a bystander and 2% by the police". Results: 19.1% and 2.9%. RULINGS-TO-REVISIT R14 repeats 15%.
- CS-18 Test: "about 87,000 man-days over 44,000 fights". Results: 103,647 over 24 scenarios of 2,000 (48,000 fights).
- CS-10 Test: cosh shown at menace 0.8 "51%"; results 53.6%.
- Fix: regenerate every Test line from results.json (better, have the simulator print the exact sentences), and update R14.

## 7. Legs are never hit in any fight
- Where: combat_sim.py decide() never returns "kick"; aim_line() sends thrusts to torso or neck and slashes to head, arms or torso; CS-05 ("a low kick on the legs") against aim_line ("kick": legs or torso, half each); CS-31 Test ("counts ... legs out").
- Fault: leg_out_per_fight is 0.0 in every scenario, so the leg row of CS-31 (limp, chase ends, crawl, femoral bleed) is untested in fights, and the kick's line is a coin, not "low is the legs".
- Fix: add kick to the bots' choices (a share by kind), send a low kick to the legs always, let a low knife thrust be the attacker's choice; rerun and report leg_out by side.

## 8. Law stated as fact where the research marks it unverified (and one the other way)
- CS-33: the 14-inch wooden truncheon in a trouser pocket and "side-handled baton came in 1994" rest on Wikipedia only (RESEARCH-LAW s.7, UNVERIFIED; the source says "batons", not side-handled); the pocketbook's date is also UNVERIFIED, but the text marks only whistle, cuffs and radio. CS-34 then rates the radio and pocketbook can-you "fit: yes (1990 personal radios and pocketbooks)".
- CS-32: "A cosh, knuckleduster or flick knife carried in public is an offensive weapon": the PCA 1953 s.4 definition and the case law were not fetched (UNVERIFIED). s.139 "in force 29 Sep 1988" is from Hansard only; the commencement order was not found.
- CS-23: "a revolver is a section 1 firearm" is confirmed only from a Wikipedia summary, s.5 unread.
- The other way: CS-32 calls the PACE s.1 and CJA s.140 search power "from memory; unverified", but RESEARCH-LAW s.1 marks s.140 extending PACE s.1 CONFIRMED.
- Fix: mark each as unverified in the text with the research line, add them to the PC research list, and drop "unverified" from the s.140 sentence.

## 9. CS-05's own knife standard is now missed without saying so
- Where: CS-05 Standard ("a knife fight kills in roughly 1 in 10") against its Test (57.5 per 1,000, about 1 in 17; was 94).
- Fault: revision 1 moved the result out of its standard silently. The sources span 0.9% (in hospital) to 17% (before hospital), so either can be argued, but the text must choose.
- Fix: restate the standard as a band from the sources (for example 3 to 12 in 100 fights where a knife is used) or retune; say which in DECISIONS.md.

## 10. CS-12: the still man under a lamp
- Where: CS-12 "How he turns" ("under a lamp a still man is seen at about 6 m"); combat_sim.py sight_reach() and approach().
- Fault: code sees a still figure under a lamp at 8.7 m with shadow nearby and 12.2 m without. The doorway (1.4 m) and unlit street (2.25 m) figures match. Also the text's crouch effect is "beyond 4 m in the dark"; code applies the 0.6 at every distance.
- Fix: state 9 to 12 m in the text, or tune sight_reach to give 6 m; make the crouch distance rule match one way or the other.

## 11. CS-02 still says limbs are hit "by chance"
- Where: COMBAT-SYSTEM.md CS-02, Aim: "arms and legs are hit by chance or by a low kick".
- Fault: contradicts the chance rule and CS-05 (blows land on the line; a guarded blow on the arms; a low kick on the legs).
- Fix: "arms are hit when he guards; legs by a low kick".

## 12. Gun aim "shown on screen" against the no-HUD rulings
- Where: CS-23 ("the aim, which sways with range, Frank moving and his wind, shown on screen, never a hidden roll"); CS-30 ("no reticle"); Out on purpose (no meters).
- Fault: it does not say how sway is shown without a reticle; the simulator models it as a gaussian error the player cannot see, which is a hidden roll in effect.
- Fix: say the shot goes exactly where the barrel points at the press, and the barrel's sway is seen in Frank's arms and the gun in the camera, no reticle; the simulator's error then stands for the player's skill, as already said in gun_hit's docstring.

## 13. A shove into a wall is multiplied by the weapon in hand
- Where: combat_sim.py land(): force uses `w["mult"]` for shove_surface; CS-07 ("hits at force 2.0"), CS-05 fists line.
- Fault: Frank holding a cosh shoves at 3.8 and uncapped (probed: head harm 4.75), though nothing struck him but the wall. Also when a brick or chair breaks on its last blow, weapon is reset to fists before the cap and manner checks, so the breaking blow is scored as a fist.
- Fix: use multiplier 1.0 for shove_surface (and apply the fists cap to it whatever is held); read the weapon before the breakage reset.

## 14. The held-choke curve starts earlier than its one source
- Where: CS-13 ("no risk for the first 20 s more ... 10% at 30 s"); combat_sim.py choke_death(); RESEARCH.md line 89.
- Fault: 10% death at 30 s past the knock-out is about 37 s of hold in all, earlier than the earliest stop of breathing in the cited series (62 s). The source is a teaching sheet; the series it cites (Sauvageau 2011) is, from this reviewer's recall and unverified, filmed hangings, not carotid holds. The text does call the curve judgement, but places it below the source's floor without saying so. The curve is also only printed, never drawn through fixed().
- Fix: start the rise at about 50 s past the knock-out, or say plainly it is set below the source on purpose; draw the outcome through fixed() in the simulator.

## 15. Smaller text and code mismatches
- CS-05 gives the boot on a downed man force 1.6; TUNE stamp is 1.3.
- CS-05 says a weapon on a man who did not see it puts him out at once; knockdown() excludes the knuckleduster though CS-05 calls it "a carried weapon, not fists".
- CS-08 says a gun is taken by the same disarm rule; try_grab() skips guns.
- finish() decides a gun death rate from any "critical_gun" key in the whole fight's log, not the man's own wound.
- Line 3 cites REVISION-1.md "lists every change"; no such file exists under blueprint/.
- Fix: align each (one value or one line each), and write REVISION-1.md or drop the reference.
