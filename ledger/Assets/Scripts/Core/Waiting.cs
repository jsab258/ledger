using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// Where a wait must end, and why, in plain words for the player.
    public sealed class WaitStop
    {
        public GameTime At { get; }
        /// "ron", "landing", "tea", "constable", "ellis", "sheila",
        /// "sheila_answer" or "released".
        public string Why { get; }
        public string Line { get; }
        /// The day it is for: for Ron and the landing, the ask's night (so a
        /// stop after midnight still names the night before).
        public int ForDay { get; }
        /// What the game adds to WaitBeats.Shown once it has shown the line.
        public string Key { get; }
        public WaitStop(GameTime at, string why, string line, int forDay, string key = null)
        { At = at; Why = why; Line = line; ForDay = forDay; Key = key ?? why + "@" + forDay; }
    }

    /// What the game has running, for a wait to read (any may be null).
    public sealed class WaitBeats
    {
        public Arrangement Asks;
        public AdasTea Tea;
        public PoliceFile Police;
        public GossipMill Mill;
        public Inquiry Inquiry = Inquiry.None;
        public WeeksEnd Week;
        public Custody Custody;
        /// Sheila's walk-round is over (DayOne.WalkRoundEnds has happened).
        public bool WalkRoundDone = true;
        /// He is waiting in Ada's house, where the minutes count as his tea.
        public bool AtAdas;
        /// The lines the game has shown him (each stop's Key): each stops a
        /// wait once. The game keeps it in its save.
        public HashSet<string> Shown = new HashSet<string>();
        /// His walk, in game minutes, to Ada's, to the landing and to the
        /// office; unset, the call's leadMinutes.
        public int? TeaLead, LandingLead, OfficeLead;
    }

    /// A WAIT THAT STOPS FOR WHAT THE TOWN HAS FOR HIM (town list 6ci; the
    /// twelfth sweep; A25.11, A25.12, A15.19). To the Core a wait is skipped
    /// hours, and through the week's beats each would pass silently or turn
    /// against him: the night's ask never brought, Ada's tea a stand-up, the
    /// constable, DS Ellis and Sheila's Sunday question all while he was away.
    /// Next reads each piece's own state and says when a wait from `now`
    /// towards `until` must end, and why, or null when it may run to `until`.
    /// Nothing is changed.
    ///
    /// Each beat's line stops a wait once (the independent check: a line
    /// whose walk-time had begun before the wait began was never shown, so a
    /// sleep ran through the tea): early enough for his walk there, or at once
    /// if that time has come, as long as the beat is still to come or under
    /// way and he has not been shown its line (WaitBeats.Shown, which the game
    /// fills and saves). Once shown, a wait runs on past it: he may skip it
    /// knowingly. Each beat's line holds until the last minute it is still of
    /// use, that minute included (the second review: a line due on the hour
    /// was missed by the call made at it). Ron comes to him after dark on an
    /// ask night, and at once if he is looking for him, until one; a sleep is
    /// a wait, and Ron knocks. In the cells the wait runs to his release and
    /// nothing else stops it. During Sheila's walk-round there is no wait at
    /// all (Refused). The game runs a wait an hour at a time and calls Next
    /// before each hour, since the town's talk moves while he waits; it looks
    /// at most two weeks ahead.
    public static class Waiting
    {
        /// Ron brings the ask after dark: fully dark by about eight in autumn
        /// (production/research/evening-light-1990), as the week on paper has it.
        public const int RonComesHour = 20;
        /// "After ten, to the man who asks for Mickey's" (Arrangement.Terms).
        public const int LandingFrom = 22;
        /// The hours the week on paper keeps: DS Ellis at nine, the constable at ten.
        public const int EllisHour = 9, ConstableHour = 10;
        /// Sheila wants his answer before six, when she goes home: he is told
        /// in time to be with her by half past five, less his walk.
        public const int AnswerBy = WeeksEnd.StayUntil;
        public const int AnswerTime = 30;
        /// The longest a lead may be; how far ahead a wait is read.
        public const int MaxLead = 180, DaysAhead = 14;

        public const string WalkRoundLine = "Sheila's still showing you round.";
        public const string RonLine = "Ron's at the door with something for you.";
        public const string LandingLine = "They'll be expecting the envelope at the landing after ten.";
        public const string TeaLine = "Ada's pot goes on at nine.";
        public const string ConstableLine = "There's a constable asking for you.";
        public const string EllisLine = "DS Ellis is on Quay Street, asking after you.";
        /// For a body: she comes for the dead, not about him (PoliceFile).
        public const string EllisBodyLine = "DS Ellis is on Quay Street.";
        public const string SheilaLine = "Sheila's waiting for you in the office this morning, on her day off.";
        public const string SheilaAnswerLine = "Sheila wants your answer before the day's out.";
        public const string ReleasedLine = "They're letting you go.";

        static GameTime At(int day, int hour) => new GameTime(day, hour, 0);

        public static WaitStop Next(GameTime now, GameTime until, WaitBeats b, int leadMinutes = 0)
        {
            var all = Stops(now, until, b, leadMinutes);
            return all.Count > 0 ? all[0] : null;
        }

        /// EVERY KNOWN STOP from `now` to `until`, earliest first, for a "wait
        /// until" choice (production/research/waiting: waiting as the way to
        /// reach an appointment, not to miss it). Only what is known now: the
        /// next ask night, not the ones after it.
        public static List<WaitStop> Ahead(GameTime now, GameTime until, WaitBeats b, int leadMinutes = 0) =>
            Stops(now, until, b, leadMinutes);

        /// WHETHER NO WAIT MAY START AT ALL, and why: during Sheila's walk-round.
        /// Null when a wait may start.
        public static string Refused(WaitBeats b) => b != null && !b.WalkRoundDone ? WalkRoundLine : null;

        /// The game has shown him this stop's line.
        public static void Showed(WaitBeats b, WaitStop s) { if (b != null && s != null) (b.Shown ??= new HashSet<string>()).Add(s.Key); }

        static List<WaitStop> Stops(GameTime now, GameTime until, WaitBeats b, int leadMinutes)
        {
            var found = new List<WaitStop>();
            if (b == null || until.CompareTo(now) <= 0) return found;
            if (Refused(b) != null) return found;
            var shown = b.Shown ?? new HashSet<string>();
            // In the cells: to his release, that minute included, and nothing else.
            var held = b.Custody;
            // Keyed by the minute, so two spells ending the same day are two (the third review).
            string releasedKey = held == null ? null : "released@" + held.OutAt.TotalMinutes;
            if (held != null && now.CompareTo(held.TakenAt) >= 0 && now.CompareTo(held.OutAt) <= 0 && !shown.Contains(releasedKey))
            {
                if (held.OutAt.CompareTo(until) <= 0) found.Add(new WaitStop(held.OutAt, "released", ReleasedLine, held.OutAt.Day, releasedKey));
                return found;
            }
            int Lead(int? l) => Math.Max(0, Math.Min(MaxLead, l ?? leadMinutes));

            // A beat at `at`, its line of use until `last`, that minute
            // included: once, `lead` before it or at once; in time order, the
            // first offered first on a tie.
            void Beat(string why, int forDay, GameTime at, GameTime last, int lead, string line)
            {
                if (shown.Contains(why + "@" + forDay) || now.CompareTo(last) > 0) return;
                var t = at.AddMinutes(-lead);
                if (t.CompareTo(now) < 0) t = now;
                if (t.CompareTo(until) > 0) return;
                int i = found.Count;
                while (i > 0 && t.CompareTo(found[i - 1].At) < 0) i--;
                found.Insert(i, new WaitStop(t, why, line, forDay));
            }

            var asks = b.Asks;
            if (asks != null && !asks.Ended && asks.NextNight >= 0)
            {
                int n = asks.NextNight;
                // A night past one in the morning, unanswered, counts at dawn
                // (Arrangement.PassedTo): the next is two nights on, unless that
                // night away ends it.
                if (now.CompareTo(Arrangement.GaveUpAt(n)) >= 0)
                    n = asks.WasDelivered(n) && asks.Patience - Arrangement.PatienceLossPerNoShow <= 1e-9 ? -1 : n + Arrangement.Every;
                if (n >= 0)
                {
                    var lastMinute = Arrangement.GaveUpAt(n).AddMinutes(-1);
                    if (!asks.WasDelivered(n)) Beat("ron", n, At(n, RonComesHour), lastMinute, 0, RonLine);
                    else Beat("landing", n, At(n, LandingFrom), lastMinute, Lead(b.LandingLead), LandingLine);
                }
            }

            var tea = b.Tea;
            // Not once he has been with her (the third review: a man who sat with
            // her till half ten and slept at a quarter to eleven was told of it).
            if (tea != null && tea.State == TeaState.Asked && !b.AtAdas && tea.LatestMinute < 0)
                Beat("tea", tea.Day, At(tea.Day, AdasTea.From), At(tea.Day, AdasTea.Until).AddMinutes(-1), Lead(b.TeaLead), TeaLine);

            var police = b.Police;
            // Counted wide (the port's independent check, 30 September: within
            // fourteen days of the largest day, now.Day + DaysAhead wrapped and
            // the wait never stopped; at the very top the loop never ended).
            long lastDay = Math.Min((long)until.Day, (long)now.Day + DaysAhead);
            if (police != null)
            {
                for (long dd = Math.Max(0, now.Day); dd <= lastDay; dd++)
                {
                    int d = (int)dd;
                    var t = At(d, ConstableHour);
                    if (t.AddMinutes(60).CompareTo(now) > 0 && police.ConstableWouldCome(d) != null) { Beat("constable", d, t, t.AddMinutes(59), 0, ConstableLine); break; }
                }
                for (long dd = Math.Max(0, now.Day); dd <= lastDay; dd++)
                {
                    int d = (int)dd;
                    var t = At(d, EllisHour);
                    if (t.AddMinutes(60).CompareTo(now) <= 0) continue;
                    // FROM NINE ON HER DAY, WHETHER SHE CAME, not whether she would now
                    // (the independent review of 1 October, M2): nine's decision is taken
                    // on the talk heard by then, and the hour's talk can grow louder after
                    // it; before nine, what would bring her.
                    List<string> whys;
                    if (now.CompareTo(t) < 0) whys = police.EllisWouldComeAll(b.Mill, d, b.Inquiry);
                    else
                    {
                        whys = new List<string>();
                        foreach (var v in police.Visits) if (v.day == d) whys.Add(v.why);
                    }
                    if (whys.Count > 0)
                    {
                        // About him if any of the day's reasons is, or the inquiry asks about him.
                        bool aboutHim = whys.Exists(w => w != "body") || Police.AsksAboutYou(b.Inquiry);
                        Beat("ellis", d, t, t.AddMinutes(59), 0, aboutHim ? EllisLine : EllisBodyLine);
                        break;
                    }
                }
            }

            var week = b.Week;
            if (week != null && !week.Answered)
            {
                if (week.AskedAt == null && CastDay.Weekday(week.Day) == 6)
                    Beat("sheila", week.Day, At(week.Day, WeeksEnd.WaitFrom), At(week.Day, WeeksEnd.WaitUntil).AddMinutes(-1), Lead(b.OfficeLead), SheilaLine);
                else if (week.AskedAt is GameTime asked && week.Stands(now))
                {
                    // With her by half past five, less his walk, since she goes
                    // home at six (the second review: told at her deadline, he
                    // came to an empty office); any day she asked.
                    var by = At(asked.Day, AnswerBy).AddMinutes(-AnswerTime);
                    Beat("sheila_answer", asked.Day, by, At(asked.Day, AnswerBy).AddMinutes(-1), Lead(b.OfficeLead), SheilaAnswerLine);
                }
            }
            return found;
        }
    }
}
