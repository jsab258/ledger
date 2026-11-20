#!/usr/bin/env python3
"""Status sweep of the 91 parts added late to the parts tree (work/added-ids.txt), prototype track,
from the prototype source on the lane branch (tools/lane/prototype/project/src, round 6 source, round 5 published).
Lane run of 20 Nov 01:17. Unreal statuses are left as the tree session set them (repository records only)."""
import json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
F = os.path.join(ROOT, "production", "lane", "parts-tree", "PARTS-TREE.json")
S = "src/"
P = {
 "1.1.7": ("built shallow", "holding Z leans Tom on a wall and lets time pass (src/player.js waiting, G.fast; design_notes.js); no sit, bench, smoke or bus stop"),
 "1.1.8": ("missing", "no vault anywhere in src (grep 'vault' empty); walls and fences are plain solids in map.js; question A26 pending"),
 "1.2.8": ("designed", "Tom always drives; passengers are fares only (src/fares.js); no ride as passenger"),
 "1.2.9": ("designed", "no repair, plates or paint; round 6 removed stranding instead (src/drive.js wayOut, workClear)"),
 "1.2.10": ("designed", "parked cars are solid obstacles only (src/drive.js trafficAt parkedOnly); no taking a car"),
 "1.3.11": ("designed", "no lasting marks on Tom; rules.js only grades a run-down (runDownIsAClipBelowMetresPerSecond)"),
 "1.3.12": ("designed", "src/fight.js has one opponent model (guard, swing, stagger); no boxer, brawler or big-man types"),
 "1.4.7": ("built shallow", "stare, square up, threaten and shove are rungs of the fronting-up ladder (src/fight.js, design_notes_text.js), not free acts on one key; greeting only by typed or suggested talk (talk.js GREETS, hook.js); no nod"),
 "1.4.8": ("designed", "noise exists as Tom's own noise reach (ui.js mnoise, seeing.js) but nothing thrown or made to draw a watcher"),
 "1.6.9": ("built shallow", "pocket money and the holdall carried on night jobs (src/money.js, jobs.js, hook.js pocketPence); no coat pockets or office storage"),
 "1.6.10": ("designed", "no wardrobe or changing clothes; seeing.js reads 'coat' as a recognition step only"),
 "1.6.11": ("designed", "no casing act; only design_notes_text.js mentions it"),
 "1.7.4": ("designed", "no followers; Cammack's lads are a threat (src/scenes.js lads()), not Tom's men"),
 "2.1.5": ("built shallow", "crowd walks routines (src/routines.js goToPoint) with foot solids (drive.js footSolid, footClear); no queueing or stepping aside for each other found"),
 "2.1.6": ("built shallow", "weekdays named (src/util.js DAYS), rent Friday, jobs by weekday (jobs.js); no market day, match day or dated days"),
 "2.2.6": ("designed", "no trespass or ground rules in src (grep empty); shop hours only (rules.shops)"),
 "2.4.5": ("built shallow", "src/scenes.js paper(): an evening paper for 20p with headlines (talk_lines.js HEADLINES) and story news (lastNews); Alison Sedman's questions (scenes.js); her stories are not built from what she knows"),
 "2.6.7": ("designed", "no patrol car or traffic stop (grep empty); police are on foot (src/police.js)"),
 "2.6.8": ("designed", "a bought witness gives no statement (src/police.js mind.bought) and talk has a bribe intent (talk.js); no named officer to pay"),
 "2.6.9": ("built shallow", "src/police.js arrestScene, arrestNow, custody: Ellis asks Tom to the station; no charge joining the case, bail or office search"),
 "2.7.8": ("built shallow", "src/rules.js prices: tea at the caff, the paper, chips, cosh and knife (scenes.js); no clothes, tools or property to buy"),
 "2.12.5": ("designed", "the office and flat do not change with play"),
 "2.15.1": ("designed", "no fleet or drivers (grep empty)"),
 "2.15.2": ("built shallow", "a rank and its sign exist (src/map.js rank, ranksign; rules.js routine at the rank) and fares come from it; no winning ranks or accounts"),
 "2.15.3": ("designed", "no other minicab firm"),
 "2.17": ("designed", "no fronts or rackets held"),
 "2.18": ("designed", "no ambulance or hospital (grep empty)"),
 "2.19": ("designed", "no lasting marks on the town (grep empty)"),
 "3.5.6": ("built shallow", "src/jobs.js JOBS table (from, to, pay, after hour) with saved state; not a general step graph with windows and outcomes"),
 "3.5.7": ("built shallow", "jobs reach Tom through set scenes and the to-do line (src/scenes.js, ui.js obj); no phone, messages or callers"),
 "3.6.8": ("built", "typing on the keyboard and numbered suggested lines (src/talk.js, hook.js say a suggested line, ui.js talk box); pad cannot type words (6.6); Tom not heard aloud"),
 "3.7": ("built shallow", "overheard lines on a timer (src/scenes.js overhear, talk_lines.js OVERHEARD) and the lads at night (lads()); no authored incidents placed on the clock"),
 "4.1.3": ("built shallow", "shop fascia signs (src/map.js sign: MICKEY'S CARS, LAVERACK) and named spots (map.js names); no street-name plates"),
 "4.1.4": ("designed", "no out-of-town fares; the map is the Hook only"),
 "4.2.3": ("designed", "no dock gate, customs or Harbour Board in src"),
 "4.2.4": ("built shallow", "water areas and a ladder (src/map.js WATER, ladder); water is blocked to walking; no knocked-in man climbing out"),
 "4.5.1": ("built shallow", "AI traffic on routes with a bus (src/drive.js stepTraffic, spawn, spawnBusLeaving); giving way and reacting to people not checked"),
 "4.9": ("built shallow", "1990 money, the paper's headlines and shop signs (talk_lines.js, map.js); no poll-tax posters or brand set"),
 "4.10": ("designed", "no pub or school places in src"),
 "4.11.1": ("designed", "no yard dogs (only 'watchdog' in checks.js, a code timer)"),
 "5.2.6": ("designed", "people are plain figures; no posture of knowing"),
 "5.4.2": ("built", "src/light.js one light field: sodium lamp pools with falloff, lit and late shop windows (channels 0 to 3), the same numbers for seeing"),
 "5.6.3": ("designed", "no thinking sound or glance before an answer"),
 "5.8.3": ("built shallow", "src/ui.js scene(), say(), choose() run written beats from scenes.js (Ellis's arrest, Alison, Sheila) but pause play; no blocking or performance inside play"),
 "6.1.5": ("built shallow", "the time shows on screen always (src/ui.js dtime hhmm); no watch key, street clocks or chapel bell"),
 "6.9": ("built shallow", "the to-do line names places (src/ui.js obj, scenes.js objective 'Quay Street, the quay end, under the blue sign') and the Ledger map (6.3); no house numbers or asking the way"),
 "6.10": ("built shallow", "Mrs Dunn's letter at the start (src/design_notes.js introLetter) and the evening paper (scenes.js paper); no solicitor's or VAT letters"),
 "7.15": ("built shallow", "src/end_screen.js the end of the week: truth beside the Ledger and the run report (a playtest view); no story close or credits"),
 "7.16": ("designed", "no pastimes"),
 "8.4.1": ("built shallow", "subtitles always shown (6.1.2) and a noise meter (src/ui.js mnoise); no stand-ins for other sound cues"),
 "8.8": ("built", "src/talk.js RULES (absolute content rules sent with every live line) and BANNED word check on what comes back"),
 "8.9": ("built shallow", "English only; lines kept in src/talk_lines.js and numbers in rules.js, but much text still inside code (scenes.js, ui.js)"),
 "8.10": ("built shallow", "src/map.js solids and sight lines, drive.js solidAt (lamp posts and parked cars solid since round 6, unpublished); no ragdoll, doors or props pushed"),
 "9.4": ("missing", "no port yet; tools/lane/one-sim (way A) is the first step, not swapped in"),
 "9.7.1": ("built", "the prototype's licence lines are on the allowlist (lane log 19 Nov 19:17, item 18); tools/lane/one-sim licence lines approved"),
 "9.7.2": ("built shallow", "tools/lane/prototype/project/CHANGELOG.md, RESULTS.md and the lane handover; no RECIPE lines for the prototype (the lane may not write RECIPE.md)"),
 "9.9": ("built shallow", "the driving and feel sheets and method exist (production/research/lane/FEEL-MEASUREMENT-METHOD-2026-11-20.md, the driving sheet); no reference game measured yet"),
 "9.10": ("built shallow", "production/lane/ROUND-HOURS.md records each round's cloud hours and models"),
 "9.11": ("built", "the 18 studies and the lane's reference research (production/research/lane/)"),
 "9.12": ("built", "canon.md, VISION.md, DESIGN.md and its addendum, BUILD-ORDER.md, this tree (production/lane/synthesis/, parts-tree/)"),
}
doc = json.load(open(F, encoding="utf-8"))
by = {p["id"]: p for p in doc["parts"]}
ids = [l.strip() for l in open(os.path.join(os.path.dirname(F), "work", "added-ids.txt")) if l.strip()]
n = 0
for i in ids:
    p = by[i]
    if "prototype" not in p["status"]:
        continue
    if i not in P:
        raise SystemExit("no sweep line for prototype part " + i)
    st, ev = P[i]
    p["status"]["prototype"] = {"status": st, "evidence": ev + " (sweep 20 Nov 01:17)"}
    n += 1
json.dump(doc, open(F, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("prototype statuses swept:", n)
