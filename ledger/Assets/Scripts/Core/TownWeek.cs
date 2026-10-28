using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// THE TOWN'S WEEK, HOUR BY HOUR (28 October 2026, the 5 October sweep's G4). The game's hourly step lived only
    /// in the port (ue-probe TownWeek.h, since 30 September) and, written apart, in the reference week's own loop
    /// (TownReach's WeekRows), so nothing compared the port's step with a C# one and three of its calls could vanish
    /// unseen (the sweep's planted breaks P1, P3 and P11). Its home is here now: TownReach's week runs on it, the
    /// port's TownWeek.h follows it line for line, and the TownWeekHour golden rows drive it hour by hour.
    ///
    /// The game's clock hands each game hour to the scheduled steps in this order (RunHour, below, which the port's
    /// CrimeProbe.cpp ConsequenceHour calls since 28 October 2026):
    /// six o'clock the asks' nights passed; the damage found; nine the witnesses to the police and DS Ellis; ten
    /// the constable and Ada's invitation (never while he is held); eight in the evening Ron at the door on an ask
    /// night (not while he is held); eleven the tea's close; every hour the week's end closed and the town's talk.
    /// What the player does (the deed, the envelope or a no, the tea, Sunday's answer) comes between those steps,
    /// called when he does it. Keyed by the cast's own ids (ROUTE.md step 0); one owner of the pieces, so the
    /// game's save is one TownSave of them.
    public sealed class TownWeek
    {
        public readonly Arrangement Asks = new Arrangement(0);
        public readonly AdasTea Tea = AdasTea.For(0, true);
        public readonly PoliceFile Police = new PoliceFile();
        public readonly WeeksEnd Week = new WeeksEnd();
        public readonly List<Aftermath> Damage = new List<Aftermath>();
        public readonly List<Custody> Arrests = new List<Custody>();
        public readonly TownHours Hours = new TownHours();

        /// The deed's story (ROUTE.md step 2), who saw it and at what rung; empty until he does one.
        public string DeedTopic = "";
        public int DeedDay = -1;
        /// When it was done: its night, and so its first report (the review's B5).
        public GameTime DeedAt;
        public List<(string who, int rung)> Witnesses = new List<(string, int)>();
        /// What the week has come to, as the reference week's rows put it.
        public string EllisFirst = "never", TakenFirst = "no";

        /// The custody holding him now, or null.
        public Custody Holding(GameTime now)
        {
            foreach (var c in Arrests) if (c != null && c.Holds(now)) return c;
            return null;
        }

        public Custody Latest() => Arrests.Count == 0 ? null : Arrests[Arrests.Count - 1];

        // ---- the scheduled steps, in the game's order within an hour ----

        /// AS EACH HOUR TURNS, before anything else in it: his no or the winding down reaches the landing when Ron
        /// goes down, and a night he stayed away passes from four (Arrangement.TellDue; the reviews' B3). Then at
        /// 06:00 the asks' nights passed, the dawn's call the step has made since 30 September. Since 1 October
        /// TellDue is itself PassedTo for the hour's own day, so the dawn's call repeats it and changes nothing
        /// (found 28 October: the sweep's P11, removing it, can fail no test); kept as the port has it.
        public void Six(GossipMill mill, GameTime now)
        {
            Asks.TellDue(mill, now);
            if (now.Hour == 6) Asks.PassedTo(now.Day, mill, now);
        }

        /// THE TOWN'S TALK UP TO A MOMENT (the review's A12): every round not yet run up to `at`, once; the game
        /// calls it as its minutes pass and before a talk turn, the reference week before each event's minute.
        public void RoundsTo(GossipMill mill, CastDay cast, GameTime at) => Hours.RunTo(mill, cast, at);

        /// THE DEED (ROUTE.md step 2), when he does it: the damage kept, and each witness holding it first-hand as a
        /// sensitive story at the rung they saw him at (a rung below 0: as the reference week, none).
        /// `witnessesLeftOut`: those who saw it done never "find" it (the town's card for the game); the reference
        /// week leaves nobody out. `alsoLeftOut`: those who only heard it go (the review's A1) know the window went
        /// and never "find" it either; they are not witnesses of him.
        public void Deed(GossipMill mill, GameTime now, string area, string thing, string said, IList<(string who, int rung)> saw,
                         string storyFact, string storySaid, double certainty, bool witnessesLeftOut = true, IEnumerable<string> alsoLeftOut = null)
        {
            var leaveOut = new List<string>();
            if (witnessesLeftOut) foreach (var s in saw) leaveOut.Add(s.who);
            if (alsoLeftOut != null) foreach (var h in alsoLeftOut) leaveOut.Add(h);
            // The port's Aftermath::Make refuses an unnamed deed where the C# throws: the step keeps no damage then.
            if (!string.IsNullOrEmpty(area) && !string.IsNullOrEmpty(thing) && !string.IsNullOrEmpty(said))
                Damage.Add(new Aftermath(area, thing, said, now, Aftermath.DefaultMend(now), witnessesLeftOut ? leaveOut : null));
            DeedTopic = "player." + storyFact;
            DeedDay = now.Day;
            DeedAt = now;
            Witnesses = new List<(string, int)>(saw);
            if (mill == null) return;
            foreach (var s in saw)
                mill.Witness(s.who, new Fact("player", storyFact, area), storySaid, true, now, certainty, false, s.rung);
        }

        /// Every hour after the deed: whoever comes into the area finds it.
        public List<(string who, GameTime when)> DamageTick(GossipMill mill, CastDay cast, GameTime now)
        {
            var found = new List<(string, GameTime)>();
            foreach (var a in Damage) found.AddRange(a.Tick(mill, cast, now));
            return found;
        }

        /// 09:00 from the morning after its night (a deed before six is the night before's, the review's B5): each
        /// witness goes to the police once they would (ROUTE.md step 4). Returns who did.
        public List<string> NineReports(GossipMill mill, CastDay cast, GameTime now, int rungOverride = -1)
        {
            var went = new List<string>();
            if (now.Hour != 9 || DeedDay < 0 || now.TotalMinutes < Aftermath.FirstReportMorning(DeedAt).TotalMinutes
                || string.IsNullOrEmpty(DeedTopic) || mill == null) return went;
            foreach (var w in Witnesses)
            {
                bool gave = false;
                foreach (var e in Police.Entries) if (e.Who == w.who && e.Topic == DeedTopic && e.How != Known.Talk) { gave = true; break; }
                if (gave) continue;
                bool never = cast != null && cast.NeverToPolice(w.who);
                if (!PoliceFile.WouldReport(mill.Get(w.who), Offence.Damage, false, DeedTopic, never)) continue;
                if (Police.Report(w.who, DeedTopic, Offence.Damage, rungOverride >= 0 ? rungOverride : w.rung, now.Day) != null) went.Add(w.who);
            }
            return went;
        }

        /// How the game grades its deeds for what DS Ellis hears of the street: a window is damage, the rest
        /// suspicious, as the reference week grades them.
        static Offence GradeOf(string topic) => topic.StartsWith("player.window", StringComparison.Ordinal) ? Offence.Damage : Offence.Suspicious;

        /// 09:00: DS Ellis, while there is a reason (ROUTE.md step 5). The reason, or null. Come for the street's
        /// talk, she hears it (PoliceFile.HearTheStreet); she hears and asks only the people on the street at nine.
        public string NineEllis(GossipMill mill, GameTime now, CastDay cast)
        {
            if (now.Hour != 9 || now.Day < 1 || mill == null) return null;
            string why = Police.EllisComes(mill, now.Day, Inquiry.None);
            if (why == null) return null;
            if (why == "talk") Police.HearTheStreet(mill, now.Day, GradeOf, cast, now);
            if (EllisFirst == "never") EllisFirst = $"day {now.Day + 1}, for {why}";
            PoliceFile.Asked(mill, PoliceFile.WhoSheAsks(mill, cast, now), why, now);
            return why;
        }

        /// 10:00, if he is not held: a constable (ROUTE.md step 6). The custody taken, or null. `area` is where he
        /// stands, which the street that sees him taken passes on.
        public Custody TenConstable(GossipMill mill, CastDay cast, GameTime now, string area, bool ownsUp = false, bool inTheCoat = false)
        {
            if (now.Hour != 10 || Holding(now) != null) return null;
            string topic = Police.ConstableComes(now.Day, now);
            if (topic == null) return null;
            var c = Police.TakeIn(topic, now, ownsUp, inTheCoat);
            if (c == null) return null;
            Custody.SeenTaken(mill, cast, area, now);
            Arrests.Add(c);
            if (TakenFirst == "no") TakenFirst = $"day {now.Day + 1}, {c.End}";
            return c;
        }

        /// 10:00 on the tea's day: Ada's invitation line, once, or null; never while he is in the cells (AdasTea's
        /// held, the review of 1 October, M3).
        public string TenTea(GameTime now)
        {
            if (Tea == null || now.Day != Tea.Day || now.Hour != 10) return null;
            return Tea.SheSeesHim(now, Holding(now) != null);
        }

        /// 20:00 on an ask night: Ron at the door with the envelope; not while he is in the cells (the review of
        /// 1 October, M3: Ron's envelope while he is held is the game's rule; the sweep's P3).
        public bool TwentyRon(GossipMill mill, GameTime now)
        {
            if (now.Hour != 20 || !Asks.AsksOn(now.Day) || mill == null || Holding(now) != null) return false;
            return Asks.Delivered(now.Day, mill.Get(Arrangement.Doorman), now);
        }

        /// 23:00 on the tea's day: her tea closed, however it went.
        public void TwentyThreeTea(GossipMill mill, GameTime now)
        {
            if (Tea == null || now.Day != Tea.Day || now.Hour != 23 || mill == null) return;
            Tea.Close(mill.Get(AdasTea.Ada), now);
        }

        /// Every hour, last: the week's end closed, then the town's talk. The rounds run up to `roundsUpTo` when
        /// given (the reference week: the hour's end), or to `now` (the game, whose rounds follow its minutes).
        public void HourEnd(GossipMill mill, CastDay cast, GameTime now, GameTime? roundsUpTo = null)
        {
            Week.Close(now, mill, cast);
            Hours.RunTo(mill, cast, roundsUpTo ?? now);
        }

        // ---- the hour: the steps in their order, one rule (28 October 2026) ----

        /// WHAT ONE HOUR'S STEPS DID (RunHour's answer): who found the damage, who went to the police, why DS Ellis came
        /// (null: she did not), the custody a constable took (null: none), Ada's invitation line (null: none), and
        /// whether Ron brought the envelope.
        public sealed class HourDone
        {
            public List<(string who, GameTime when)> Found = new List<(string, GameTime)>();
            public List<string> Went = new List<string>();
            public string Why;
            public Custody Taken;
            public string Invite;
            public bool Ron;
        }

        /// WHAT THE GAME DOES BETWEEN THE STEPS (its words on screen, its log, its session file, whom he has met): each
        /// called right after its own step, every hour, with what the hour has done so far, where ConsequenceHour did
        /// it between its calls; any may be null. Step, when given, is told each step's name as it ends, before that
        /// step's own call (the TownWeekSteps golden rows keep the order with it).
        public sealed class HourCalls
        {
            public Action<HourDone> Found, Went, Ellis, Taken, Invited, Ron;
            public Action<string> Step;
        }

        /// ONE GAME HOUR, ITS SCHEDULED STEPS IN THE GAME'S ORDER (28 October 2026, what remained of the 5 October
        /// sweep's G4). The order lived only in the port (CrimeProbe.cpp's ConsequenceHour called the steps one by
        /// one), so a reordered hour failed no row, though the order decides what the town knows (Ron's envelope
        /// before the hour's talk, the damage found after the dawn's passing). It is one rule now: the port's
        /// TownWeek.h RunHour follows this line for line and ConsequenceHour calls it, the TownWeekHour golden rows drive
        /// it, and the TownWeekSteps rows keep its order. `area`: where he stands, for ten's constable.
        public HourDone RunHour(GossipMill mill, CastDay cast, GameTime now, string area, HourCalls game = null)
        {
            var done = new HourDone();
            Six(mill, now);
            game?.Step?.Invoke(nameof(Six));
            done.Found = DamageTick(mill, cast, now);
            game?.Step?.Invoke(nameof(DamageTick));
            game?.Found?.Invoke(done);
            done.Went = NineReports(mill, cast, now);
            game?.Step?.Invoke(nameof(NineReports));
            game?.Went?.Invoke(done);
            done.Why = NineEllis(mill, now, cast);
            game?.Step?.Invoke(nameof(NineEllis));
            game?.Ellis?.Invoke(done);
            done.Taken = TenConstable(mill, cast, now, area);
            game?.Step?.Invoke(nameof(TenConstable));
            game?.Taken?.Invoke(done);
            done.Invite = TenTea(now);
            game?.Step?.Invoke(nameof(TenTea));
            game?.Invited?.Invoke(done);
            done.Ron = TwentyRon(mill, now);
            game?.Step?.Invoke(nameof(TwentyRon));
            game?.Ron?.Invoke(done);
            TwentyThreeTea(mill, now);
            game?.Step?.Invoke(nameof(TwentyThreeTea));
            HourEnd(mill, cast, now);
            game?.Step?.Invoke(nameof(HourEnd));
            return done;
        }

        // ---- what he does, between them ----

        /// His answer to the night's ask: the envelope at the landing, or a no. `now` is the answer's "as of" (for a
        /// no, Ron's question); `toldAt`, when given, is when he said it, which stamps what is told and remembered
        /// (Arrangement.Answer, the independent check of 1 October).
        public bool AnswerAsk(int day, NightAnswer what, GossipMill mill, GameTime now, GameTime? toldAt = null) =>
            Asks.Answer(day, what, mill, now, toldAt);
    }
}
