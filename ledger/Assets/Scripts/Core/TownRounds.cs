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
    /// TownHours and calls its RunTo as each game hour starts (and after a
    /// load), which runs every hour not yet run, once, the hour now with the
    /// street as it stands (`onStreet`, the people the game has walking there,
    /// whose rounds are its own by distance) and any hours skipped with nobody
    /// on it. A round passes stories only between the pairs it is given, so the
    /// game's rounds and these never tell the same pair twice; the ageing is
    /// here, once an hour, and nowhere else. Who is on the street is read as the
    /// hour starts, for the whole hour.
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
        /// The first hour not yet run, counted from day 0's midnight; -1 before any.
        public long NextHour { get; private set; } = -1;

        /// AS EACH GAME HOUR STARTS, and after a load: every hour not yet run up
        /// to and including the hour `now` is in, once each; the hours before
        /// it with nobody on the street (skipped: asleep, in the cells, a load's
        /// jump), the hour now with `onStreet`. The first call runs only the
        /// hour now. Returns how many hours ran.
        public int RunTo(GossipMill mill, CastDay cast, GameTime now, Func<string, bool> onStreet = null)
        {
            if (mill == null || cast == null) return 0;
            long hourNow = TownRounds.FloorDiv(now.TotalMinutes, 60);
            if (hourNow < NextHour) return 0;
            int ran = 0;
            if (NextHour >= 0 && hourNow > NextHour)
                ran += TownRounds.CatchUp(mill, cast, TownRounds.HourStart(NextHour), TownRounds.HourStart(hourNow));
            TownRounds.Hour(mill, cast, TownRounds.HourStart(hourNow), onStreet);
            NextHour = hourNow + 1;
            return ran + 1;
        }

        public Dictionary<string, object> ToJson() => new Dictionary<string, object> { { "next", (double)NextHour } };

        public static TownHours FromJson(Dictionary<string, object> saved)
        {
            var t = new TownHours();
            if (saved != null && saved.TryGetValue("next", out var n) && n is double d && d >= -1 && d < 1e7 && d == Math.Floor(d)) t.NextHour = (long)d;
            return t;
        }
    }
}
