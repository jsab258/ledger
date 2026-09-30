using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// THE TOWN TALKS BY ITS ROUTINES (town list 6bs; ROADMAP stage 3's measure
    /// in the game, and the checklist's A25.06 and A25.12). Every figure the
    /// first hour rests on (the night back at his face by minute 13, DS Ellis on
    /// day 5, twenty of forty-one knowing he was taken) comes from rounds run by
    /// the cast's routines: whoever is together by their routines this hour
    /// (CastDay.Together) talks, six minutes a round, and the mill ages each
    /// hour. The game ran rounds only between people standing near each other on
    /// the street in front of him, so nobody off Quay Street talked, and nobody
    /// at all while he slept or sat in the cells. So: the game keeps one
    /// TownHours and calls its RunTo as game time passes (as often as it likes,
    /// and after a load), which runs every round not yet run up to now, once,
    /// each at its own minute and none before it (the independent review of
    /// 30 September, A12), this hour's with the street as it stands
    /// (`onStreet`, the people the game has walking there, whose rounds are
    /// its own by distance) and any before it with nobody on it. A round passes
    /// stories only between the pairs it is given, so the game's rounds and
    /// these never tell the same pair twice; the ageing is here, once an hour,
    /// and nowhere else.
    public static class TownRounds
    {
        /// Game minutes between two rounds, as TownReach has always run them.
        public const int MinutesBetweenRounds = 6;

        /// The most hours one catch-up runs: two weeks. A longer gap (a save
        /// edited by hand, a clock set wrong) runs its last two weeks.
        public const int LongestCatchUpHours = 14 * 24;

        /// ONE GAME HOUR OF THE TOWN'S TALK from `hourStart` (its minutes are
        /// ignored): the rounds by the routines for every pair the street does
        /// not hold, then the hour's ageing. Returns how many stories passed.
        public static int Hour(GossipMill mill, CastDay cast, GameTime hourStart, Func<string, bool> onStreet = null)
        {
            if (mill == null || cast == null) return 0;
            int day = hourStart.Day, hour = hourStart.Hour;
            int passed = 0;
            for (int m = 0; m < 60; m += MinutesBetweenRounds)
                passed += mill.Tick(new GameTime(day, hour, m),
                    (a, b) => !(onStreet != null && onStreet(a) && onStreet(b)) && cast.Together(a, b, day, hour)).Count;
            mill.Age(new GameTime(day, hour, 0).AddMinutes(60));
            return passed;
        }

        /// EVERY HOUR SKIPPED, from the hour `from` falls in up to (not
        /// including) the hour `to` falls in, as Hour does each, with nobody on
        /// the street: a night asleep, a spell in the cells, the time a load
        /// jumps. Returns how many hours ran.
        public static int CatchUp(GossipMill mill, CastDay cast, GameTime from, GameTime to)
        {
            if (mill == null || cast == null) return 0;
            long first = FloorDiv(from.TotalMinutes, 60), last = FloorDiv(to.TotalMinutes, 60);
            if (last - first > LongestCatchUpHours) first = last - LongestCatchUpHours;
            int ran = 0;
            for (long h = first; h < last; h++, ran++)
                Hour(mill, cast, HourStart(h));
            return ran;
        }

        /// The start of an hour counted from day 0's midnight, days rounded
        /// down (so hour -1 is the day before's eleven o'clock).
        internal static GameTime HourStart(long h)
        {
            long day = FloorDiv(h, 24);
            return new GameTime((int)day, (int)(h - day * 24), 0);
        }

        internal static long FloorDiv(long a, long b) => a >= 0 ? a / b : -((-a + b - 1) / b);
    }

    /// THE HOURS THE TOWN HAS TALKED (town list 6bs, the independent check: an
    /// hour run twice, after a reload or a missed check, told the same pairs
    /// twice and aged twice). One per game, saved with the town (TownSave).
    public sealed class TownHours
    {
        /// The first round not yet run, in minutes from day 0's midnight (a
        /// multiple of TownRounds.MinutesBetweenRounds); -1 before any.
        public long NextRound { get; private set; } = -1;
        /// The first hour not yet wholly run; -1 before any.
        public long NextHour => NextRound < 0 ? -1 : TownRounds.FloorDiv(NextRound, 60);

        /// EVERY ROUND ONCE, AND NONE BEFORE ITS TIME (the independent review
        /// of 30 September, A12: the hour's ten rounds ran as the hour started,
        /// so a talk at 13:01 could hold a memory stamped 13:54, and a deed at
        /// 12:05 was first passed on at 13:00): every round from the first not
        /// yet run up to `now`, each at its own minute; the rounds of the hour
        /// `now` is in with `onStreet` (the people the game has walking there,
        /// whose rounds are its own by distance), any before it with nobody on
        /// the street (skipped: asleep, in the cells, a load's jump), two weeks
        /// at most; the mill aged as each hour turns. While the game runs its own
        /// street it calls this at least once a round (every six game minutes) or
        /// oftener, and asked each round or each minute the town ends the same;
        /// a longer gap within the hour is taken with the street as the call
        /// gives it, and whole hours gone by as time the street did not run (the
        /// second independent check: asked only each hour, the rounds of the
        /// hour gone ran with nobody on the street, telling the street's pairs
        /// again). The first call starts at the hour now's start. Returns how
        /// many rounds ran.
        public int RunTo(GossipMill mill, CastDay cast, GameTime now, Func<string, bool> onStreet = null)
        {
            if (mill == null || cast == null) return 0;
            const int step = TownRounds.MinutesBetweenRounds;
            long nowM = now.TotalMinutes;
            long hourNowStart = TownRounds.FloorDiv(nowM, 60) * 60;
            long lastRound = TownRounds.FloorDiv(nowM, step) * step;
            bool firstCall = NextRound < 0;
            if (firstCall) NextRound = hourNowStart;
            if (lastRound < NextRound) return 0;
            // The mill's ageing clock is not in the save: started again at the
            // hour the last round ran in, where the mill last aged, a load loses
            // no hour of fading (the independent check: one hour's fade missing
            // after each load; the second: saved at the end of an hour, with the
            // next round on the hour, one hour was still lost). A mill that has
            // aged to that hour already is not aged again.
            if (!firstCall) mill.Age(At(TownRounds.FloorDiv(NextRound - step, 60) * 60));
            long earliest = hourNowStart - TownRounds.LongestCatchUpHours * 60L;
            if (NextRound < earliest) NextRound = earliest;
            int ran = 0;
            for (long r = NextRound; r <= lastRound; r += step, ran++)
            {
                var at = At(r);
                if (r % 60 == 0) mill.Age(at);
                var street = r >= hourNowStart ? onStreet : null;
                int day = at.Day, hour = at.Hour;
                mill.Tick(at, (x, y) => !(street != null && street(x) && street(y)) && cast.Together(x, y, day, hour));
            }
            NextRound = lastRound + step;
            return ran;
        }

        // A minute counted from day 0's midnight as a time of day, days rounded
        // down, so minute -30 is the day before's 23:30 (the second independent
        // check: GameTime.FromTotalMinutes truncates towards zero).
        static GameTime At(long minutes)
        {
            long day = TownRounds.FloorDiv(minutes, 24 * 60), m = minutes - day * 24 * 60;
            return new GameTime((int)day, (int)(m / 60), (int)(m % 60));
        }

        public Dictionary<string, object> ToJson() => new Dictionary<string, object> { { "next", (double)NextHour }, { "round", (double)NextRound } };

        /// From ToJson's values: the next round; a save from before rounds were
        /// kept (the next hour only) reads as that hour's start.
        public static TownHours FromJson(Dictionary<string, object> saved)
        {
            var t = new TownHours();
            // -1 is "none yet"; any other round a multiple of the step, days before
            // day 0 included (the second independent check).
            if (saved != null && saved.TryGetValue("round", out var r) && r is double rd && rd > -6e8 && rd < 6e8 && rd == Math.Floor(rd)
                && (rd == -1 || rd % TownRounds.MinutesBetweenRounds == 0))
                t.NextRound = (long)rd;
            else if (saved != null && saved.TryGetValue("next", out var n) && n is double d && d >= -1 && d < 1e7 && d == Math.Floor(d))
                t.NextRound = d < 0 ? -1 : (long)d * 60;
            return t;
        }
    }
}
