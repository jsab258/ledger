"""Rule checks: catch a Fable round that changes one of the prototype's rule numbers.

The rules come from production/lane/PROTOTYPE-RULES-READ-2026-11-18.md (read by hand from the
minified bundle, 18 Nov 2026, bundle version 1794862482-9f9b). Rule ids below are that file's
section and row, counted from the top of each table (1.01 is the first row of "Seeing and
witnessing"). Since Fable's round of 18 Nov the checks read his readable source
(tools/lane/prototype/project/, page version in PUBLISHED.json), not the bundle.

Two layers:

1. Static (no browser, no pictures; needs node for the rules table): each clearly read rule is
   checked in one of two ways.
   - kind "rules": the number is in Fable's rules table, project/src/rules.js (the game reads its
     numbers from there; the page shows the same table as window.LEDGER.rules). The module is
     evaluated with node and the named entry must hold the read value.
   - kind "outside_rules": the number (or the plain behaviour) is not in the rules table, so the
     row searches the named readable source file for a string, as often as it was found when
     re-pointed (18 Nov). A row with one number in the table and another outside counts as
     outside_rules. These rows survive a renaming of the table but not a reformat of the file.
   " inferred" is added where the reading file marks the number's meaning as inferred.

2. Live (headless Chromium, through the game's test hook window.LEDGER): a handful of rules
   checked by what the game does, not by its text, plus LEDGER.rules in the page against
   rules.js. Needs the pictures in the folder named by LEDGER_PROTO_ASSETS, as the smoke test;
   skipped otherwise, never passed. Also skipped when Playwright's Chromium cannot start.

Changed by Fable's 18 Nov round (the earlier readings were right for the bundle they were read
from; the rows now hold the new numbers and say so):
  4.13b rent late: was Saturday 00:00 (day 5), now Friday 18:00 ("Friday, by six").
  8.05  what is saved: the measures were added to the save.
  8.06  restore through the hook: it now rebuilds the people around their memories, as Continue.
  act table: 52 kinds, was 51 (a new private kind, "word", for a thing Tom is told).

Run with pytest (python -m pytest tests/rules_test.py). Rule reads found wrong are kept as strict
expected failures, so a later fix to the reading file or the game shows up (none at present).
"""
import functools, http.server, json, math, os, re, shutil, subprocess, sys, tempfile, threading, time

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import build  # noqa: E402

PROJECT = os.path.join(os.path.dirname(HERE), "project")
SRC = os.path.join(PROJECT, "src")
ASSETS = os.environ.get("LEDGER_PROTO_ASSETS")
GL = ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader"]
HOUR = 45  # LEDGER.step real seconds per game hour (rule 6.01)

RT = "rules"           # the number is in project/src/rules.js
OUT = "outside_rules"  # the number is searched for in a readable source file


def R(path, value):
    """The rules table entry at path (section.name) holds value."""
    return ("rule", path, value)


def F(file, search, count=1):
    """The readable source file (under project/src) holds search, count times."""
    return ("src", file, search, count)


def U(file, search, count=1):
    """The source file reads the rules-table entry as read (no number of its own): keeps a row "rules"."""
    return ("use", file, search, count)


def sched(rows):
    """A cast.js schedule as Prettier writes it (six spaces before each row)."""
    def item(v):
        return "'%s'" % v if isinstance(v, str) else repr(v)
    body = "".join("      [%s],\n" % ", ".join(item(v) for v in row) for row in rows)
    return "    sched: [\n" + body + "    ],"


def traits(nerve, venal, talk, discretion):
    return "    nerve: %r,\n    venal: %r,\n    talk: %r,\n    discretion: %r," % (nerve, venal, talk, discretion)


def kind_row(name, sev, val, crime):
    return "  %s: K(\n    %r,\n    %r,\n    %r," % (name, sev, val, crime)


RON_SCHED = [[0, "home", "sleep"], [6.6, "caff:s1", "sit"], [8.1, "rank", "idle"], [12.3, "fish:q1", "queue"],
             [12.8, "rank", "idle"], [17.4, "tangs:q1", "queue"], [17.9, "rank", "smoke"], [23.6, "home", "sleep"]]
SHEILA_SCHED = [[0, "off"], [7.5, "mickeys:sheila", "work"], [12.5, "caff:s7", "sit"],
                [13.1, "mickeys:sheila", "work"], [18.2, "off"]]
GRACE_SCHED = [[0, "home", "sleep"], [6, "caff:grace", "work"], [17.2, "home", "idle"], [22.5, "home", "sleep"]]

# (rule id, plain name with its number, checks, kind)
RULES = [
    # 1. Seeing and witnessing
    ("1.01", "sight range 4 + 44 x light^1.2, x(1 - 0.3 rain), x(1 - 0.22 mist at night)",
     [R("seeing.rangeInBlackMetres", 4), R("seeing.rangeAddedByFullLightMetres", 44),
      R("seeing.lightCurvePower", 1.2), R("seeing.rainCutsRangeByShare", 0.3),
      R("seeing.mistAtNightCutsRangeByShare", 0.22)], RT),
    ("1.02", "cab headlights: seen from at least 34 m", [R("seeing.headlampsSeenFromMetres", 34)], RT),
    ("1.03", "indoors: seen from at least 14 m", [R("seeing.indoorsSeenFromMetres", 14)], RT),
    ("1.04", "field of view on the street 1.08 rad each side", [R("seeing.viewHalfAngleRadians", 1.08)], RT),
    ("1.05", "field of view from a home window 1.35 rad each side",
     [R("seeing.windowViewHalfAngleRadians", 1.35)], RT),
    ("1.06", "under 3 m seen unless well behind (1.9 rad)",
     [R("seeing.closeByMetres", 3), R("seeing.closeByViewHalfAngleRadians", 1.9)], RT),
    ("1.07", "line of sight checked against walls",
     [F("seeing.js", "G.env.los(e.x, e.z, T.x, T.z)")], OUT),
    ("1.08", "clarity = 1 - distance / range, 0.05 to 1",
     [R("seeing.leastClarity", 0.05), U("seeing.js", "c = clamp(1 - d / range, SEE.leastClarity, 1);")], RT),
    ("1.09", "noise radius: cab 8 to 30, still 0.5, running 12, walking 5",
     [R("noise.cabIdlingMetres", 8), R("noise.cabAddedAtSpeedMetres", 22),
      R("noise.cabFullNoiseAtMetresPerSecond", 12), R("noise.stillBelowMetresPerSecond", 0.2),
      R("noise.standingMetres", 0.5), R("noise.runningMetres", 12), R("noise.walkingMetres", 5)], RT),
    ("1.10", "noise by hour: x0.5 10-16, x2 before 5, x1.5 5-7, x1.3 after 22, else x0.8",
     [R("noise.noonTimes", 0.5), R("noise.noonFromHour", 10), R("noise.noonUntilHour", 16),
      R("noise.deadOfNightTimes", 2), R("noise.deadOfNightUntilHour", 5), R("noise.earlyTimes", 1.5),
      R("noise.earlyUntilHour", 7), R("noise.lateEveningTimes", 1.3), R("noise.lateEveningFromHour", 22),
      R("noise.otherwiseTimes", 0.8)], RT),
    ("1.11", "rain muffles noise x(1 - 0.6 rain)", [R("noise.rainCutsByShare", 0.6)], RT),
    ("1.12", "a sleeper hears at 70 percent of the radius",
     [R("noise.throughAWindowTimes", 0.7),
      U("seeing.js", "hear: d <= T.noiseR * NOISE.throughAWindowTimes, c: 0, d, asleep: true")], RT),
    ("1.13", "attention rises 0.45 + 1.4 x clarity a second, x1.5 during an act",
     [R("seeing.attentionPerRealSecond", 0.45), R("seeing.attentionPerRealSecondPerClarity", 1.4),
      R("seeing.attentionFasterWhenRemarkableTimes", 1.5)], RT),
    ("1.14", "night out counts from 23:30 to 05:00",
     [R("time.smallHoursFromHour", 23.5), R("time.smallHoursUntilHour", 5)], RT),
    ("1.14b", "the cab at night is its own kind of being seen",
     [F("seeing.js", "return smallHours(h) || t.carry === 'bag' ? 'cab_night' : 'cab_drive';")], OUT),
    ("1.15", "one sighting event per kind per two-hour block", [R("seeing.sameSightingLastsGameHours", 2)], RT),
    ("1.16", "a heard memory at most every 90 game minutes",
     [R("noise.sameNoiseRemarkedEveryGameMinutes", 90)], RT),
    # The bundle string held the loud-act road (events.js, memory.heardSure 0.3). The small-hours noise
    # road in seeing.js has its own entry, noise.heardSure 0.25, not part of this rule.
    ("1.17", "loud acts reach hearers as a man at 0.3 sure",
     [R("memory.heardSure", 0.3),
      U("events.js", "remember(P, E, { src: 'heard', who: 'man', sure: MEM.heardSure, heat: MEM.heardHeat });")], RT),
    ("1.18", "sureness 0.35 + 0.65 x clarity, x0.85 unless named",
     [R("seeing.sureBase", 0.35), R("seeing.surePerClarity", 0.65), R("seeing.sureIfNotNamedTimes", 0.85)], RT),
    ("1.19", "a memory's starting heat is severity + 0.3",
     [R("seeing.heatAddedToSeverity", 0.3), R("memory.heatAddedToSeverity", 0.3)], RT),
    ("1.20", "named as Tom above face score 0.36", [R("seeing.namesHimAboveFace", 0.36)], RT),
    ("1.20b", "the coat at night cuts the face score x0.4",
     [R("seeing.coatAtNightFaceTimes", 0.4), R("seeing.coatHidesWhenNightAbove", 0.5)], RT),
    ("1.21", "act table: inherit severity 0.5", [F("kinds.js", kind_row("inherit", 0.5, 0, 0))], OUT),
    ("1.21b", "act table: arrive severity 0.3", [F("kinds.js", kind_row("arrive", 0.3, 0, 0))], OUT),
    ("1.21c", "act table: kill severity 1, crime 3", [F("kinds.js", kind_row("kill", 1, -1, 3))], OUT),
    ("1.22", "a non-act glance raises familiarity once every 20 game minutes",
     [R("seeing.plainSightingEveryGameMinutes", 20)], RT),
    # The default nerve 0.5 (a person with none set) is still written in seeing.js.
    ("1.23", "timid people (nerve under 0.62) step back",
     [R("watching.stepBackIfNerveBelow", 0.62),
      F("seeing.js", "(P.def.nerve == null ? 0.5 : P.def.nerve) < WATCH.stepBackIfNerveBelow")], OUT),
    ("1.24", "night: day 07:45 to 17:15, full night 18:45 to 06:15",
     [R("time.dayFullHour", 7.75), R("time.duskStartsHour", 17.25), R("time.nightFullHour", 18.75),
      R("time.dawnStartsHour", 6.25)], RT),
    # 2. Gossip and rumour
    ("2.01", "a gossip round every 4 game minutes", [R("ticking.gossipEveryGameMinutes", 4)], RT),
    ("2.02", "talking distance 4.8 m street, 8 m indoors",
     [R("gossip.withinMetresOnStreet", 4.8), R("gossip.withinMetresIndoors", 8)], RT),
    ("2.03", "closeness weight 0.42, +0.38 close friends, x(0.4 + talk) x(0.6 + 0.4 talk)",
     [R("gossip.affinityBase", 0.42), R("gossip.closeFriendsAdded", 0.38), R("gossip.tellerTalkBase", 0.4),
      R("gossip.talkativeIfNotSet", 0.6), R("gossip.listenerTalkBase", 0.6),
      R("gossip.listenerTalkShare", 0.4)], RT),
    ("2.04", "heat under 0.12 is not passed on", [R("gossip.notWorthTellingBelowHeat", 0.12)], RT),
    ("2.05", "a discreet person holds back by their discretion",
     [F("gossip.js", "chance(A.def.discretion ?? GOS.discretionIfNotSet)")], OUT),
    ("2.06", "each telling: sure x0.8, heat x0.92, hop +1; teller heat +0.12",
     [R("gossip.toldSureTimes", 0.8), R("gossip.toldHeatTimes", 0.92), R("gossip.tellerHeatAdded", 0.12),
      F("gossip.js", "hop: m.hop + 1,")], OUT),
    ("2.08", "passers-by pass on stories over heat 0.2 at 35 percent",
     [R("gossip.passerByTellsAboveHeat", 0.2), R("gossip.passerByChance", 0.35)], RT),
    ("2.09", "heat fades x e^(-minutes/1700)", [R("gossip.heatFadeGameMinutes", 1700)], RT),
    ("2.09b", "heat fades every 10 game minutes", [R("ticking.memoriesFadeEveryGameMinutes", 10)], RT),
    ("2.09c", "a forever act (a killing) keeps heat 0.6", [R("gossip.neverForgottenHeat", 0.6)], RT),
    ("2.10", "certainty does not fade, only heat",
     [F("gossip.js", "m.heat = Math.max(fl, m.heat * f);")], OUT),
    ("2.11", "Tuesday push at 08:45 on day 1",
     [F("scenes.js", "if (d === 1 && h >= 8.75 && !f.nudge) {")], OUT),
    ("2.12", "seeing two tell a story within 18 m makes a note", [R("gossip.tomCatchesThemWithinMetres", 18)], RT),
    ("2.13", "knowing score 0.25 + 0.09 per kind (up to 6) + 0.4 familiarity",
     [R("naming.knowsOfInheritance", 0.25), R("naming.perKindOfActKnown", 0.09),
      R("naming.kindsCountedAtMost", 6), R("naming.perFamiliarity", 0.4)], RT),
    ("2.13b", "names at 0.2, 0.5, 0.8, 1.05",
     [R("naming.levelOneFromScore", 0.2), R("naming.levelTwoFromScore", 0.5),
      R("naming.levelThreeFromScore", 0.8), R("naming.levelFourFromScore", 1.05)], RT),
    ("2.14", "the street's name: reached by 40 percent of locals", [R("naming.townLevelNeedsShareOfLocals", 0.4)], RT),
    ("2.15", "a story said to his face at most every 40 game minutes",
     [R("gossip.nextRemarkAfterGameMinutes", 40)], RT),
    # 3. The Ledger
    ("3.01", "every act goes on his own list",
     [F("ledger.js", "if (!G.ledger.acts.find((a) => a.e === E.id)) G.ledger.acts.push(")], OUT),
    ("3.02", "belief ranks: talking 0, window 1, saw 2",
     [F("events.js", "export const BR = { talking: 0, window: 1, saw: 2,")], OUT),
    ("3.03", "saw only when noticed: 34 m, 0.9 rad beyond 2.5 m, window 9 m, lit 0.2 beyond 7 m",
     [R("noticing.furthestMetres", 34), R("noticing.facingHalfAngleRadians", 0.9),
      R("noticing.mustFaceBeyondMetres", 2.5), R("noticing.darkWindowHidesBeyondMetres", 9),
      R("noticing.darkBelowLight", 0.2), R("noticing.darkFigureHidesBeyondMetres", 7)], RT),
    ("3.04", "there: done in front of them", [F("events.js", "ledgerSeen(E, P, 'there')")], OUT),
    ("3.05", "asked: he asked and was told", [F("talk.js", "ledgerSeen(E, P, 'asked'")], OUT),
    ("3.06", "two heads together in the caff make a note",
     [F("scenes.js", "had their heads together at Rinaldi's")], OUT),
    ("3.07", "first note shows the Ledger hint", [F("main.js", "L opens the Ledger")], OUT),
    # 4. Money and debts
    ("4.01", "Tom starts with 23.50 clean", [R("money.startsWithPocketPence", 2350)], RT),
    ("4.02", "Mickey's book: Dennis 80, Lee 15, Darren 22, Julie 9, Wayne 30",
     [R("prices.owedByIvesonPence", 8000), R("prices.owedByLeePence", 1500), R("prices.owedByDarrenPence", 2200),
      R("prices.owedByJuliePence", 900), R("prices.owedByWaynePence", 3000),
      U("state.js", "dennis: { owed: RULES.prices.owedByIvesonPence, st: 'open' },")], RT),
    ("4.03", "a debtor pays if fear over 0.45, or liking over 0.3 and owing 15 or less",
     [F("scenes.js", "if (P.mind.fear > 0.45 || (P.mind.regard > 0.3 && d.owed <= 1500)) {")], OUT),
    ("4.04", "a collected debt goes in the tin", [F("scenes.js", "earn(amt, true);")], OUT),
    ("4.05", "striking a debt out: liking +0.5",
     [F("scenes.js", "P.mind.regard = clamp(P.mind.regard + 0.5, -1, 1);")], OUT),
    ("4.06", "Julie's slate: nine pounds", [F("fares.js", "Nine pounds, since the summer", 2)], OUT),
    ("4.07", "fare 80p plus 0.9p a metre, rounded to 10p",
     [R("fares.flagFallPence", 80), R("fares.penceAddedPerMetre", 0.9), R("fares.roundedToPence", 10)], RT),
    ("4.08", "radio fares 07:00 to 23:12",
     [R("fares.radioFromHour", 7), R("fares.radioUntilHour", 23.2)], RT + " inferred"),
    ("4.08b", "a new fare offer every 16 to 34 seconds",
     [R("fares.nextOfferAfterRealSecondsAtLeast", 16), R("fares.nextOfferAfterRealSecondsAtMost", 34)],
     RT + " inferred"),
    ("4.08c", "an offer lasts 26 seconds", [R("fares.offerStandsRealSeconds", 26)], RT + " inferred"),
    ("4.08d", "after a missed offer, 20 to 40 seconds",
     [R("fares.afterAMissedOfferRealSecondsAtLeast", 20), R("fares.afterAMissedOfferRealSecondsAtMost", 40)],
     RT + " inferred"),
    ("4.08e", "after a paid fare, 14 to 30 seconds",
     [R("fares.afterAFareRealSecondsAtLeast", 14), R("fares.afterAFareRealSecondsAtMost", 30)], RT + " inferred"),
    ("4.10", "the book hides 10.00 + 80 percent of fares since the wash",
     [R("money.washedSafelyPence", 1000), R("money.washedSafelyShareOfFares", 0.8)], RT),
    ("4.11", "job 1 pays sixty", [F("jobs.js", "Sixty. Count it somewhere else.")], OUT),
    ("4.11b", "job 1 (the Monday bag) pay 60.00",
     [R("jobs.mondayBagPayPence", 6000), U("jobs.js", "pay: JOB.mondayBagPayPence,")], RT),
    ("4.12", "a job not done by 03:30 to 12:00 next day is a no-show",
     [R("jobs.missedFromHourNextDay", 3.5), R("jobs.missedUntilHourNextDay", 12)], RT),
    ("4.13", "rent 18.00", [R("money.rentPence", 1800)], RT),
    # Changed in Fable's 18 Nov round (CHANGELOG 2e): the bundle read was right (late from Saturday
    # 00:00, day 5); the rent is now late from Friday 18:00, as Mrs Rennison's line says.
    ("4.13b", "rent late from Friday 18:00 (was Saturday 00:00 until 18 Nov)",
     [R("money.rentDueDayIndex", 4), R("money.rentLateFromHour", 18)], RT),
    ("4.14", "Ron's door and Darren's good word: 5.00",
     [R("prices.ronWatchesTheDoorPence", 500), R("prices.darrenPutsAGoodWordAboutPence", 500)], RT),
    ("4.14b", "Darren's hearsay: 3.00", [R("prices.darrenSaysWhatHeHeardPence", 300)], RT),
    ("4.15", "tea and paper: 20p", [R("rest.teaAtTheCaffPence", 20), R("prices.eveningPaperPence", 20)], RT),
    ("4.15b", "tea passes 25 game minutes", [R("rest.teaAtTheCaffGameMinutes", 25)], RT),
    ("4.15c", "tea: caff people familiarity +0.06", [R("rest.caffFamiliarityGain", 0.06)], RT),
    ("4.16", "the paper",
     [F("scenes.js", "G.story.flags.dead ? 'MAN FOUND DEAD ON THE HOOK' : G.story.lastNews")], OUT),
    ("4.17", "spending takes dirty money first", [F("money.js", "const d = Math.min(m.dirty, pence);")], OUT),
    # The readable source names this 8.00 the plasters after the beating (beaten.plastersPence).
    ("4.18", "beaten down: pays up to 8.00 from clean",
     [R("beaten.plastersPence", 800), U("work.js", "Math.min(m.clean, BEAT.plastersPence)")], RT),
    # 5. Suspicion and police
    ("5.01", "statements taken at 04:00 from Tuesday",
     [F("scenes.js", "if (h >= 4 && d >= 1) nightly(d - 1);")], OUT),
    ("5.02", "a statement needs sure at least 0.55", [R("police.statementNeedsSureAtLeast", 0.55)], RT),
    ("5.03", "ten people never make a statement", [F("cast.js", "    nostmt: 1,\n", 10)], OUT),
    ("5.04", "violence (crime 2+) sends Ellis", [R("police.violentFromCrimeLevel", 2)], RT),
    ("5.05", "the police come at 09:00", [R("police.comesNextDayAtHour", 9)], RT),
    ("5.06", "held 4 hours (5 violent), +2 if he ran; bill 25.00 (40.00 if he ran)",
     [R("police.heldGameHours", 4), R("police.heldGameHoursIfViolent", 5),
      R("police.heldGameHoursAddedIfHeRan", 2), R("police.briefBillPence", 2500),
      R("police.briefBillPenceIfHeRan", 4000)], RT),
    ("5.07", "they give up after 7 s out of sight, 70 m or 60 s",
     [R("police.losesHimAfterRealSecondsUnseen", 7), R("police.losesHimBeyondMetres", 70),
      R("police.chaseLastsAtMostRealSeconds", 60)], RT + " inferred"),
    ("5.08", "loudness: heat x severity x badness, x0.6 if not by name",
     [R("naming.notNamedLoudnessTimes", 0.6)], RT),
    ("5.09", "Ellis walks Thursday or Friday, 10:00 to 13:00",
     [R("police.ellisFirstDayIndex", 3), R("police.ellisLastDayIndex", 4), R("police.ellisFromHour", 10),
      R("police.ellisUntilHour", 13)], RT),
    ("5.09b", "Ellis walks at loudness 2.2", [R("police.ellisComesAtLoudness", 2.2)], RT),
    ("5.09c", "Ellis asks up to 5 locals", [R("police.ellisAsksPeopleAtMost", 5)], RT),
    ("5.10", "Cammack's lads at loudness over 1.2", [F("scenes.js", "loudness() > 1.2")], OUT),
    ("5.11", "fear +0.07 told, +0.18 seen",
     [R("memory.fearFromSeriousCrimeTold", 0.07), R("memory.fearFromSeriousCrimeSeen", 0.18)], RT),
    ("5.12", "liking moves x0.15 told, x0.26 seen",
     [R("memory.regardPerToldAct", 0.15), R("memory.regardPerSeenAct", 0.26)], RT),
    # 6. Time of day and routines
    ("6.01", "one game hour is 45 real seconds", [R("time.realSecondsPerGameHour", 45)], RT),
    ("6.02", "a new week starts Monday 15:36 (save version 4)",
     [R("time.weekStartsGameMinute", 936), F("state.js", "export const VERSION = 4;")], OUT),
    ("6.05", "the weather list", [F("clock.js", "['mist', 'drizzle', 'drizzle', 'rain', 'dry', 'heavy']")], OUT),
    ("6.06", "Ron: home 00:00, caff 06:36, rank 08:06, fish 12:18, rank 12:48, Tang's 17:24, rank 17:54, home 23:36",
     [F("cast.js", sched(RON_SCHED))], OUT),
    ("6.07", "Sheila: office 07:30 to 18:12, caff 12:30", [F("cast.js", sched(SHEILA_SCHED))], OUT),
    ("6.07b", "Grace: caff 06:00 to 17:12", [F("cast.js", sched(GRACE_SCHED))], OUT),
    ("6.08", "Sheila: nerve 0.95, talk 0.15, discretion 0.92", [F("cast.js", traits(0.95, 0, 0.15, 0.92))], OUT),
    ("6.08b", "Darren: nerve 0.3, talk 0.95, discretion 0.05", [F("cast.js", traits(0.3, 0.95, 0.95, 0.05))], OUT),
    ("6.08c", "Ron: nerve 0.85, talk 0.7, discretion 0.35", [F("cast.js", traits(0.85, 0.8, 0.7, 0.35))], OUT),
    # 7. Talk
    ("7.01", "Tab opens the suggested lines", [F("talk.js", "if (code === 'Tab') {\n    T.open = !T.open;")], OUT),
    ("7.02", "at most three suggested lines", [F("talk.js", "L.length < 3 && D.keep")], OUT),
    ("7.05", "a live reply is cut to three sentences and 380 characters",
     [F("talk.js", "if (parts && parts.length > 3) s = parts.slice(0, 3).join('').trim();\n  return s.slice(0, 380);")],
     OUT),
    ("7.07", "talking costs 1.5 game minutes an exchange", [F("talk.js", "G.t += 1.5;")], OUT + " inferred"),
    # 8. Saving
    ("8.01", "save version 4; any other refused",
     [F("state.js", "export const VERSION = 4;"), F("saving.js", "if (o.v !== VERSION) return false;")], OUT),
    ("8.01b", "browser save key ledger.save.v4", [F("saving.js", "const LS = 'ledger.save.v' + VERSION,")], OUT),
    ("8.02", "account saves in chunks of 150,000 characters", [F("saving.js", "CH = 150000;")], OUT),
    ("8.03", "the newer save wins", [F("saving.js", "(at(b) > at(a) ? b : a)")], OUT),
    ("8.04", "autosave every 75 real seconds", [F("main.js", "autoT > 75 && !F.on")], OUT),
    # Changed in Fable's 18 Nov round: the save now also holds the Ledger screen test's measures.
    ("8.05", "what is saved (v, t, played, ... and since 18 Nov the measures)",
     [F("saving.js", "const KEYS = [\n  'v',\n  't',\n  'played',"),
      F("saving.js", "  'measures', // the Ledger screen test's measures")], OUT),
    # Changed in Fable's 18 Nov round (CHANGELOG 2a): the reading was right for the bundle (the hook's
    # restore did not rebuild the people's memories); restore and Continue now share one function.
    ("8.06", "restore through the hook rebuilds memory as Continue does (fixed 18 Nov)",
     [F("hook.js", "restore: x.loadWeek,")], OUT),
]
# Left out of the static table, and why: 2.07 and 4.19 are absences (no hop limit, no wages);
# 4.09 has no number and no unique string; 6.03, 6.04, 7.03 and 7.04 are read from the game's own
# design notes only, whose headings carry no number; 7.06 (a name learned when said) has no number.

# Rule reads found wrong against the readable source: rule id -> reason. Kept as strict expected
# failures. None found when re-pointed on 18 Nov.
WRONG = {}


@functools.lru_cache(maxsize=1)
def rules_table():
    """project/src/rules.js evaluated by node: its RULES export (the game's one rules table)."""
    node = shutil.which("node")
    if not node:
        pytest.skip("node not found: the rules table cannot be read")
    code = "import('./src/rules.js').then(m => console.log(JSON.stringify(m)))"
    out = subprocess.run([node, "--input-type=module", "-e", code], cwd=PROJECT, check=True,
                         capture_output=True, text=True).stdout
    mod = json.loads(out)
    assert list(mod) == ["RULES"], "rules.js exports %s, expected only RULES" % list(mod)
    return mod["RULES"]


@functools.lru_cache(maxsize=None)
def source(name):
    with open(os.path.join(SRC, name), encoding="utf-8") as f:
        return f.read()


def rule_value(path):
    node = rules_table()
    for part in path.split("."):
        assert isinstance(node, dict) and part in node, "rules.js has no entry %s" % path
        node = node[part]
    return node


def _param(row):
    rid, name, checks, kind = row
    if any(c[0] == "src" for c in checks):  # "use" checks do not count
        assert kind.startswith(OUT), "rule %s searches a source file but is not marked outside_rules" % rid
    else:
        assert kind.startswith(RT), "rule %s is all in the rules table but marked %s" % (rid, kind)
    marks = [pytest.mark.xfail(strict=True, reason=WRONG[rid])] if rid in WRONG else []
    return pytest.param(rid, name, checks, id="%s %s" % (rid, name[:50]), marks=marks)


@pytest.mark.parametrize("rid,name,checks", [_param(r) for r in RULES])
def test_static_rule(rid, name, checks):
    for c in checks:
        if c[0] == "rule":
            got = rule_value(c[1])
            assert got == c[2], "rule %s (%s): rules.js %s is %r, read as %r; the rule may have moved" % (
                rid, name, c[1], got, c[2])
        else:  # "src" or "use"
            _, file, search, count = c
            found = source(file).count(search)
            assert found == count, "rule %s (%s): %r found %d times in %s, expected %d; the rule may have moved" % (
                rid, name, search, found, file, count)


def test_static_rule_ids_unique():
    ids = [r[0] for r in RULES]
    assert len(ids) == len(set(ids))


def test_static_rules_table_is_what_the_game_reads():
    # Every source file that reads a rule imports the one table; none keeps a copy of it.
    t = rules_table()
    assert len(t) == 20, "rules.js has %d sections, 20 when re-pointed" % len(t)
    readers = [f for f in os.listdir(SRC) if f.endswith(".js") and "from './rules.js'" in source(f)]
    assert {"seeing.js", "gossip.js", "police.js", "money.js", "fares.js", "jobs.js", "hook.js"} <= set(readers)


def _act_kinds():
    # The act table in kinds.js: each top-level key is written "  name: K(".
    return re.findall(r"^  (\w+): K\($", source("kinds.js"), re.M)


def test_static_act_table_has_52_kinds():
    # 51 when read from the bundle; Fable's 18 Nov round added "word" (a private thing Tom is told).
    kinds = _act_kinds()
    assert len(kinds) == 52, kinds
    assert "word" in kinds and "choice_silent" in kinds


# 30 schedule blocks: 28 named people (cast.js) plus the fare passenger and the yard lad (routines.js).
def test_static_30_schedule_blocks():
    assert source("cast.js").count("sched: [") == 28
    assert source("routines.js").count("sched: [") == 2


# ---------------------------------------------------------------------------------------------
# Live layer: one headless Chromium, one new week; tests run in file order and share the street.

@pytest.fixture(scope="module")
def game():
    if not (ASSETS and os.path.isdir(ASSETS)):
        pytest.skip("LEDGER_PROTO_ASSETS not set: pictures missing, live rule checks skipped")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        pytest.skip("playwright not installed")
    tmp = tempfile.TemporaryDirectory()
    build.build(assets_dir=ASSETS, dist=tmp.name)

    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=tmp.name))
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    pw = sync_playwright().start()
    try:
        b = pw.chromium.launch(args=GL)
    except Exception as e:  # Chromium missing or unable to start here
        pw.stop(); srv.shutdown(); tmp.cleanup()
        pytest.skip("Chromium could not start: %s" % str(e).splitlines()[0])
    pg = b.new_page(viewport={"width": 1280, "height": 720})
    pg.errors = []
    pg.on("pageerror", lambda e: pg.errors.append(str(e)))
    pg.goto("http://127.0.0.1:%d/index.html" % srv.server_address[1])
    pg.wait_for_function("window.LEDGER && window.LEDGER.G", timeout=90000)
    pg.evaluate("LEDGER.startNew()")
    pg.wait_for_function("LEDGER.G.story.phase === 'play'", timeout=30000)
    pg.evaluate("window.LEDGER_MANUAL = true; window.LEDGER_NORENDER = true")
    yield pg
    try:
        b.close(); pw.stop()
    finally:
        srv.shutdown(); srv.server_close(); tmp.cleanup()


@pytest.fixture
def js(game):
    yield game.evaluate
    assert game.errors == [], "page errors: %s" % game.errors[:3]


def test_live_6_02_week_starts_monday_1536(js):
    # The page runs a frame or so before the clock is stopped, so allow a few game minutes.
    t = js("LEDGER.G.t")
    assert 936 <= t < 940, "a new week should start at Monday 15:36 (936), not %.1f" % t
    assert js("LEDGER.G.v") == 4


def test_live_6_01_one_game_hour_is_45_real_seconds(js):
    t0 = js("LEDGER.G.t"); js("LEDGER.step(45)"); t1 = js("LEDGER.G.t")
    assert abs((t1 - t0) - 60) < 0.01, "45 real seconds moved the clock %.2f game minutes" % (t1 - t0)
    js("LEDGER.step(4.5)")
    assert abs(js("LEDGER.G.t") - t1 - 6) < 0.01


def test_live_4_01_starting_money(js):
    m = js("LEDGER.G.money")
    assert (m["clean"], m["dirty"]) == (2350, 0)


def test_live_4_02_mickeys_book(js):
    d = js("LEDGER.G.debts")
    assert {k: v["owed"] for k, v in d.items()} == {
        "dennis": 8000, "lee": 1500, "darren": 2200, "julie": 900, "wayne": 3000}
    assert all(v["st"] == "open" for v in d.values())


def test_live_6_06_rons_schedule(js):
    assert js("LEDGER.G.people.ron.def.sched") == [
        [0, "home", "sleep"], [6.6, "caff:s1", "sit"], [8.1, "rank", "idle"], [12.3, "fish:q1", "queue"],
        [12.8, "rank", "idle"], [17.4, "tangs:q1", "queue"], [17.9, "rank", "smoke"], [23.6, "home", "sleep"]]


def test_live_6_08_traits(js):
    got = js("Object.fromEntries(['sheila','darren','ron'].map(k => { const d = LEDGER.G.people[k].def;"
             " return [k, [d.nerve, d.talk, d.discretion]]; }))")
    assert got == {"sheila": [0.95, 0.15, 0.92], "darren": [0.3, 0.95, 0.05], "ron": [0.85, 0.7, 0.35]}


def test_live_named_people_as_found(js):
    assert js("LEDGER.G.named.length") == 28
    assert js("LEDGER.G.named.every(p => Array.isArray(p.def.sched))")


def test_live_5_03_who_never_makes_a_statement(js):
    assert set(js("LEDGER.G.named.filter(p => p.def.nostmt).map(p => p.id)")) == {
        "sheila", "ron", "darren", "ellis", "rita", "wayne", "lee", "hal", "dennis", "pc"}
    assert not js("LEDGER.G.people.terry.def.nostmt"), "Terry can make a statement"


def test_live_8_01_save_version_4_in_the_browser(js):
    # Outside claude.ai saving falls back to the browser only (as systems_test.py).
    js("LEDGER.saveNow()")
    v = js("(() => { try { const s = localStorage.getItem('ledger.save.v4'); return s ? JSON.parse(s).v : null; }"
           " catch (e) { return 'err ' + e; } })()")
    assert v == 4


def test_live_2_09_heat_halves_in_about_20_game_hours(js):
    # A memory planted for Ada, who stays at home (gossip never runs at home, so nothing else moves
    # her heat). Five game hours later its heat must be x e^(-300/1700); heat fades in 10-minute
    # ticks, so allow one tick either way.
    assert js("LEDGER.G.people.ada.space") == "home"
    eid = js("""(() => { const G = LEDGER.G, id = G.nextE++;
        const e = {id, kind: 'stare', t: G.t, zone: G.tom.zone, x: 0, z: 0, coat: false, car: false, wit: []};
        G.events.push(e); G.ev[id] = e;
        const m = G.people.ada.mind, s = {e: id, src: 'told', from: null, who: 'tom', sure: 0.9, heat: 0.8,
          t: G.t, said: false, hop: 0, face: 1};
        m.mem.push(s); m.by[id] = s; return id; })()""")
    js("LEDGER.step(%d)" % (5 * HOUR))
    assert js("LEDGER.G.people.ada.space") == "home"
    heat = js("LEDGER.G.people.ada.mind.by[%d].heat" % eid)
    lo, hi = 0.8 * math.exp(-310 / 1700), 0.8 * math.exp(-290 / 1700)
    assert lo <= heat <= hi, "heat %.4f after five game hours, expected %.4f to %.4f" % (heat, lo, hi)


def test_live_5_06_arrest_hold_and_bill_when_he_ran(js, game):
    # The hook's arrestNow is the arrest for assaulting an officer: violent and counted as running,
    # so the top of the range: 5 + 2 = 7 hours and a 40.00 bill, paid from clean, the rest owed.
    # Kept last: it moves the clock seven hours. The lower rows (4 hours, 25.00) need the
    # constable's talk choice, a key press; they are held by the static row 5.06 only.
    t0, clean = js("LEDGER.G.t"), js("LEDGER.G.money.clean")
    js("LEDGER.G.hooks.arrestNow(LEDGER.G.people.pc)")
    time.sleep(0.2)
    game.wait_for_function("!LEDGER.G.paused", timeout=60000)
    assert abs(js("LEDGER.G.t") - t0 - 7 * 60) < 0.5, "held %.1f game minutes" % (js("LEDGER.G.t") - t0)
    paid = min(clean, 4000)
    assert js("LEDGER.G.money.clean") == clean - paid
    assert (js("LEDGER.G.story.flags.oweAgar") or 0) == 4000 - paid
    assert js("LEDGER.G.story.arrest") is None


def test_live_rules_table_in_the_page_is_rules_js(js):
    # LEDGER.rules is the table the game reads; it must be the same as rules.js in the source.
    assert js("JSON.parse(JSON.stringify(LEDGER.rules))") == rules_table()
