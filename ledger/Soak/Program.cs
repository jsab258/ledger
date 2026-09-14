using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Ledger.Core;

namespace Ledger.Soak
{
    /// LAYER 4, TIME: the other half. What the world does after a very long
    /// time, and whether it does the same thing twice.
    ///
    ///     dotnet run -c Release --project ledger/Soak
    ///     dotnet run -c Release --project ledger/Soak -- --days 2000 --seed 3
    ///
    /// WHAT THIS IS NOT. `BalanceLab` already drives the real Core day loop for
    /// four hundred weeks per policy, and it is not this: it measures BALANCE —
    /// fate tables, cash curves, whether a strategy dominates. It asks whether
    /// the numbers are GOOD. This asks whether they are NUMBERS.
    ///
    /// THREE QUESTIONS, and the roadmap names the reason for all three as "a
    /// bug that is currently unreproducible":
    ///
    ///   1. DETERMINISM. Same seed, same world, twice — do the two runs agree
    ///      day by day? A save file is a promise that the world can be put back
    ///      the way it was, and hidden nondeterminism (an unseeded RNG, an
    ///      iteration order that depends on hash layout, a clock read) breaks
    ///      that promise silently and only for some players. This names the
    ///      first day the two runs diverge, which is the difference between a
    ///      bug report and a bug.
    ///
    ///   2. INVARIANTS, every day rather than at the end. NaN, infinity, a
    ///      negative purse, a suspicion outside 0..1. `SaveChaos` found five of
    ///      these reachable through a corrupt file; this asks whether ordinary
    ///      play reaches them on its own after long enough. A NaN that appears
    ///      on day 300 and is checked for on day 500 has had two hundred days
    ///      to spread.
    ///
    ///   3. GROWTH, REPORTED AND NOT GATED. Rumours, memories, reasons trails,
    ///      debts. Something that grows without bound is a leak, and on a long
    ///      enough save it is the leak that ends the playthrough — but NOBODY
    ///      HAS MEASURED what these do over five hundred days, so this prints
    ///      the series and the per-day slope and gates on none of it. Rule 2:
    ///      make the run print the number, look, and set the threshold from
    ///      evidence. Inventing a rumour ceiling here would be `nightNotDarker`
    ///      failing at 0.136 against 0.135, again.
    ///
    ///   4. MEMORY IS PERMANENT, AND WHAT THAT COSTS. Added by Jafar's ruling on
    ///      queue 115, 2026-09-14: canon says nothing is ever wiped, so the only
    ///      open question is the bill. Two things run here that did not before.
    ///      A GATE: no resident's remembered event count may ever fall, which is
    ///      the canon property stated as something a run can fail, and which the
    ///      600-event prune removed on 2026-09-14 would have failed on this very
    ///      street. A PROJECTION: the per-event cost is measured and the town's
    ///      bill is printed at D25's three and five hundred residents, so the
    ///      next session reads the number instead of the argument.
    ///
    ///      THE RATE IS THE SOFT HALF AND IT SAYS SO. Seven agents is not a
    ///      town (queue 116), so the projection names its denominators and the
    ///      HEADROOM is printed as a multiple of the measured rate, which is
    ///      the direction that does not inherit the rate's uncertainty.
    static class Program
    {
        static int _checks, _failed;
        static readonly List<string> _findings = new List<string>();

        static int Main(string[] args)
        {
            System.Globalization.CultureInfo.CurrentCulture =
                System.Globalization.CultureInfo.InvariantCulture;
            int days = ArgInt(args, "--days", 500);
            int seed = ArgInt(args, "--seed", 1);

            Console.WriteLine($"Soak — {days} in-game days, seed {seed}");

            var a = Run(days, seed);
            var b = Run(days, seed);

            // ---- 1. determinism -------------------------------------------
            int diverged = -1;
            for (int i = 0; i < Math.Min(a.digests.Count, b.digests.Count); i++)
                if (a.digests[i] != b.digests[i]) { diverged = i; break; }
            if (diverged < 0 && a.digests.Count != b.digests.Count) diverged = Math.Min(a.digests.Count, b.digests.Count);

            Require(a.digests.Count == b.digests.Count,
                    $"two runs of seed {seed} last the same number of days "
                    + $"({a.digests.Count} vs {b.digests.Count})");
            Require(diverged < 0,
                    diverged < 0
                        ? "same seed, same world"
                        : $"same seed, same world — DIVERGED on day {diverged + 1} "
                          + $"({Snip(a.states.ElementAtOrDefault(diverged))} vs "
                          + $"{Snip(b.states.ElementAtOrDefault(diverged))})");

            // ---- 2. invariants --------------------------------------------
            Require(a.brokenOn < 0,
                    a.brokenOn < 0
                        ? "no invariant broke in any day"
                        : $"no invariant broke — day {a.brokenOn}: {a.brokenWhy}");

            // ---- 3. growth, reported --------------------------------------
            Console.WriteLine($"  ran {a.digests.Count} day(s), verdict {a.verdict}");
            // NO CEILING IS GATED ON ANY ROW HERE, memories included: section 4
            // gates the DIRECTION of that one series and never its size.
            Console.WriteLine("  growth (REPORTED, NOT GATED: no ceiling has been measured):");
            foreach (var (label, series) in a.growth)
            {
                var shown = Sample(series, 8);
                double slope = series.Count > 1
                    ? (series[series.Count - 1] - series[0]) / (double)(series.Count - 1)
                    : 0.0;
                Console.WriteLine($"    {label,-16} [{string.Join(" ", shown)}]  "
                                  + $"first={series[0]} last={series[series.Count - 1]} "
                                  + $"per-day={slope:+0.000;-0.000;0.000}");
            }

            // ---- 4. memory is permanent, and what the town's costs ---------
            MemoryReport(a);

            Console.WriteLine();
            if (_failed == 0)
            {
                Console.WriteLine($"soak ok — all {_checks} checks passed");
                return 0;
            }
            Console.WriteLine($"soak FAILED — {_failed} of {_checks} checks");
            foreach (var f in _findings) Console.WriteLine("  FAILED " + f);
            return 1;
        }

        /// THE POPULATIONS, THE HORIZON AND THE REFERENCE SCALE ARE CORE'S,
        /// not restated here: `MemoryStore.TargetResidentsLow` and `High` are
        /// D25's three and five hundred, `LongCampaignDays` is BalanceLab's
        /// 400 weeks, and `ReferenceScaleBytes` is a gibibyte that nothing
        /// gates on. The same constants feed SimDirector's verdict line, and
        /// two copies of a number are two numbers as soon as one moves.
        static readonly int[] TownSizes =
            { MemoryStore.TargetResidentsLow, MemoryStore.TargetResidentsHigh };

        /// Queue 115, ruled by Jafar 2026-09-14. The gate is canon stated as
        /// something a run can fail; the numbers under it are the bill.
        static void MemoryReport(Outcome a)
        {
            // THE ACCEPTING CASE FIRST, and it ships its denominator: a clean
            // "never fell" is worthless without the count of what was looked
            // at, and a run that remembered nothing must not read the same as
            // a run that remembered everything.
            Require(a.memFellOnDay < 0,
                    a.memFellOnDay < 0
                        ? $"nothing is ever wiped ({a.events} events over {a.agents} residents"
                          + $" x {a.closedDays} closed days examined)"
                        : $"nothing is ever wiped: day {a.memFellOnDay}, {a.memFellWhy}");

            // AND THE CASE IT MUST CATCH. A gate that has never seen the fault
            // is a ratchet (rule 5b), so here is the 600-event prune's own
            // shape, a block of the oldest weak events going at once, fed to
            // the same FirstFall the gate above used.
            var planted = new List<int> { 1, 2, 3, 598, 599, 600, 500, 501 };
            Require(FirstFall(planted) == 6,
                    FirstFall(planted) == 6
                        ? "and a store that pruned 600 back to 500 would have failed that"
                        : $"and a store that pruned 600 back to 500 would have failed that"
                          + $" (detector said {FirstFall(planted)}, wanted 6)");

            if (a.events <= 0)
            {
                Console.WriteLine("  memory: NOTHING MEASURED"
                                  + $" (0 events over {a.agents} residents x {a.closedDays} closed days)");
                return;
            }

            // MEANS, over every event the run produced. A mean and not a
            // median because the projection multiplies by a COUNT, and the
            // only average that survives multiplication by a count is the one
            // that was summed. The bytes figure is the SUM of the per-event
            // model divided by the count, not the model of the mean.
            int textChars = (int)(a.textChars / a.events);
            int kindChars = (int)(a.kindChars / a.events);
            int bytes = (int)(a.eventBytes / a.events);
            double rate = a.events / (double)a.agents / a.closedDays;
            double busiest = a.busiestAgentEvents / (double)a.closedDays;

            Console.WriteLine("  memory: permanent (canon.md:99, queue 115 ruled 2026-09-14). The bill:");
            Console.WriteLine($"    bytesPerEventAtWorst={bytes}"
                              + $" textChars/event(mean-over-{a.events}-events)={textChars}"
                              + $" kindChars/event(mean)={kindChars}");
            Console.WriteLine($"    eventsPerNpcPerDay(mean-over-{a.agents}-residents-x-{a.closedDays}-days)={rate:0.000}"
                              + $" busiestResident={busiest:0.000}"
                              + $"   [queue-116:{a.agents}-residents-is-not-a-town]");
            foreach (int town in TownSizes)
                Console.WriteLine($"    {town}residents/{a.closedDays}days={Mb(town, a.closedDays, rate, bytes)}"
                                  + $"  {town}residents/{MemoryStore.LongCampaignDays}days={Mb(town, MemoryStore.LongCampaignDays, rate, bytes)}"
                                  + $"  atBusiestRate/{MemoryStore.LongCampaignDays}days={Mb(town, MemoryStore.LongCampaignDays, busiest, bytes)}");
            double affords = MemoryStore.AffordableEventsPerNpcPerDay(
                                 MemoryStore.ReferenceScaleBytes, TownSizes[0],
                                 MemoryStore.LongCampaignDays, bytes);
            // KEY=VALUE AND NO SPACES IN A VALUE, because the headroom is the
            // number a later reader greps for rather than reads.
            Console.WriteLine($"    headroomAt={TownSizes[0]}residents/{MemoryStore.LongCampaignDays}days/1GiB(reference-scale,not-a-budget)"
                              + $" affordsEventsPerNpcPerDay={affords:0.00}"
                              + $" xMeasuredMean={affords / rate:0.0} xBusiestResident={affords / busiest:0.0}");
        }

        static string Mb(int residents, int days, double rate, int bytes) =>
            (MemoryStore.ProjectedBytes(residents, days, rate, bytes) / (1024.0 * 1024.0))
                .ToString("0.0") + "MB";

        /// The index of the first reading in one resident's memory series that
        /// is SMALLER than the one before it, or -1 for a series that only
        /// ever grew. Canon says nothing is ever wiped, so a fall is a
        /// deletion and there is no second explanation available for one.
        ///
        /// A FUNCTION RATHER THAN A CONDITION INSIDE THE DAY LOOP, so the gate
        /// and the planted counter-case are the same code rather than two
        /// implementations of one idea.
        static int FirstFall(List<int> counts)
        {
            for (int i = 1; i < counts.Count; i++)
                if (counts[i] < counts[i - 1]) return i;
            return -1;
        }

        static void Require(bool ok, string what)
        {
            _checks++;
            if (ok) return;
            _failed++;
            _findings.Add(what);
        }

        class Outcome
        {
            public readonly List<uint> digests = new List<uint>();
            public readonly List<string> states = new List<string>();
            public readonly List<(string label, List<int> series)> growth =
                new List<(string, List<int>)>();
            public int brokenOn = -1;
            public string brokenWhy = "";
            public string verdict = "?";

            /// Queue 115. The first day any resident's remembered event count
            /// FELL, and whose, or -1 for never. Per resident and not on the
            /// total, because a total hides one person forgetting while
            /// another is talked about.
            public int memFellOnDay = -1;
            public string memFellWhy = "";

            /// The denominators the memory projection is divided by, carried
            /// out of the run so the print cannot invent one: events summed
            /// over every resident at the end, the residents that held them,
            /// the closed days they took, and the characters of Text and Kind
            /// those events actually used.
            public int events, agents, closedDays;
            public long textChars, kindChars, eventBytes;
            public int busiestAgentEvents;
        }

        /// One full run of the real Core systems, hour by hour.
        ///
        /// The shape is `BalanceLab`'s open-city loop, because that is the loop
        /// the game actually runs and a soak of a loop nobody plays is a soak of
        /// nothing. What differs is what happens at the end of each day: the lab
        /// records money, this records a digest and checks the world is still
        /// made of numbers.
        ///
        /// THE ROSTER IS A COPY AND THE ECONOMY IS NOT. Seven gossipers and
        /// three purses are restated here rather than shared with the lab, and
        /// that is a deliberate line: the properties under test are properties
        /// of the SYSTEMS, so any representative street exercises them. The
        /// economy is different — it is a shipped table of suppliers and prices
        /// that the game reads, so `EconomySetup` is compiled in rather than
        /// approximated, exactly as the lab does it.
        static Outcome Run(int days, int seed)
        {
            var o = new Outcome();
            var rng = new Random(seed);
            var camp = new Campaign();
            var mill = BuildStreet();
            var wallet = new Wallet(250);
            var economy = Ledger.Game.EconomySetup.Build();
            var purses = new PurseBook();
            purses.Add(new Purse { OwnerId = "Sam", Name = "Sam", Weekly = 60, Ceiling = 95, Cash = 45 });
            purses.Add(new Purse { OwnerId = "Rocco", Name = "Rocco", Weekly = 140, Ceiling = 260, Cash = 180 });
            purses.Add(new Purse { OwnerId = "Donna", Name = "Donna", Weekly = 220, Ceiling = 520, Cash = 380 });

            mill.Witness("Rocco", new Fact("player", "location_d2_evening", "warehouse"),
                         "the new owner was at the old warehouse the night of the fire",
                         true, new GameTime(1, 9, 0));

            var rumours = new List<int>();
            var reasons = new List<int>();
            var leads = new List<int>();
            var purseCash = new List<int>();
            var memories = new List<int>();
            var perAgentMemory = new Dictionary<string, List<int>>();

            var now = new GameTime(1, 9, 0);
            int lastClosedDay = 1;
            while (now.Day <= days)
            {
                now = now.AddMinutes(60);
                mill.Age(now);
                mill.Tick(now, (x, y) => rng.NextDouble() < 0.10);

                if (now.Hour < 8 || now.Day <= lastClosedDay) continue;
                lastClosedDay = now.Day;

                double heat = mill.DayCircleHeat();
                int takings = camp.CloseDay(heat);
                wallet.EarnClean((int)Math.Round(takings * economy.FactorFor("bar")));
                wallet.Launder();
                if (camp.Verdict == Verdict.WonWeek) camp.EnterOpenMode();
                economy.DailyTick(now, wallet, 0, 0, heat);
                purses.DailyTick(now.Day, economy.Prosperity);

                // A NEW RUMOUR NOW AND THEN, because a street where nothing
                // ever happens again is a street whose growth curves are flat
                // by construction — and a flat curve from a dead world is the
                // most convincing wrong answer this tool could give.
                if (rng.NextDouble() < 0.25)
                    mill.Witness("Rocco", new Fact("player", "seen_d" + now.Day, "the yard"),
                                 "somebody was in the yard again", true, now);

                string state = State(now, wallet, camp, economy, mill, purses);
                o.states.Add(state);
                o.digests.Add(VoiceBank.Hash(state));

                if (o.brokenOn < 0)
                {
                    var why = Broken(now, wallet, camp, economy, mill, purses);
                    if (why != null) { o.brokenOn = now.Day; o.brokenWhy = why; }
                }

                rumours.Add(mill.Agents.Sum(g => g.Rumors.Count));
                reasons.Add(mill.Agents.Sum(g => g.Suspicion.Reasons.Count));
                leads.Add(mill.Leads("player").Count());
                purseCash.Add(purses.All.Sum(p => p.Cash));
                memories.Add(mill.Agents.Sum(g => g.Memory.Events.Count));

                // Canon, day by day, PER RESIDENT and not on the total: a
                // total hides one person forgetting while another is being
                // talked about. Kept as a series rather than judged here so
                // the gate and its planted counter-case run the same
                // FirstFall, one idea and one implementation.
                foreach (var g in mill.Agents)
                {
                    if (!perAgentMemory.TryGetValue(g.Id, out var series))
                        perAgentMemory[g.Id] = series = new List<int>();
                    series.Add(g.Memory.Events.Count);
                }
            }

            o.verdict = camp.Verdict.ToString();
            o.growth.Add(("rumours", rumours));
            o.growth.Add(("suspicion notes", reasons));
            o.growth.Add(("leads on player", leads));
            o.growth.Add(("purse cash", purseCash));
            o.growth.Add(("memories", memories));

            foreach (var kv in perAgentMemory.OrderBy(k => k.Key, StringComparer.Ordinal))
            {
                int fell = FirstFall(kv.Value);
                if (fell < 0 || o.memFellOnDay >= 0) continue;
                o.memFellOnDay = fell + 1;                       // index 0 is the first closed day
                o.memFellWhy = $"{kv.Key} remembered {kv.Value[fell - 1]} events and then {kv.Value[fell]}";
            }

            o.agents = mill.Agents.Count();
            o.closedDays = o.digests.Count;
            foreach (var g in mill.Agents)
            {
                o.events += g.Memory.Events.Count;
                if (g.Memory.Events.Count > o.busiestAgentEvents)
                    o.busiestAgentEvents = g.Memory.Events.Count;
                foreach (var e in g.Memory.Events)
                {
                    o.textChars += e.Text.Length;
                    o.kindChars += e.Kind.Length;
                    // SUMMED PER EVENT, never BytesPerEvent(mean, mean): the
                    // per-string cost steps in eights, so a mean fed through
                    // the model reads 2% under the same events costed one at
                    // a time (224 against 229 on the first run of this).
                    o.eventBytes += MemoryStore.BytesPerEvent(e.Text.Length, e.Kind.Length);
                }
            }
            return o;
        }

        /// Everything that must be identical between two runs of one seed,
        /// as text. Text rather than a struct because when it differs the
        /// DIFFERENCE is the finding, and a hash alone cannot be read.
        static string State(GameTime now, Wallet w, Campaign c, Economy e,
                            GossipMill m, PurseBook p)
        {
            var sb = new StringBuilder();
            sb.Append(now.Day).Append('|').Append(w.Clean).Append(',').Append(w.Dirty)
              .Append('|').Append(c.OutfitPatience.ToString("0.000000")).Append(',')
              .Append(c.JobsDone).Append(',').Append(c.JobsMissed).Append(',').Append(c.Verdict)
              .Append('|').Append(e.Prosperity.ToString("0.000000")).Append(',')
              .Append(e.PriceLevel.ToString("0.000000")).Append('|');
            // ORDERED BY ID, and that is not tidiness either — enumerating a
            // Dictionary in insertion order happens to be stable in .NET today
            // and is not promised anywhere. A digest that depends on it would
            // report a divergence that is really the runtime's, which is the
            // instrument lying in the most convincing possible way.
            foreach (var g in m.Agents.OrderBy(x => x.Id, StringComparer.Ordinal))
                sb.Append(g.Id).Append(':').Append(g.Rumors.Count).Append(',')
                  .Append(g.Loyalty.ToString("0.0000")).Append(',')
                  .Append(g.Suspicion.Value.ToString("0.0000")).Append(';');
            sb.Append('|');
            foreach (var q in p.All.OrderBy(x => x.OwnerId, StringComparer.Ordinal))
                sb.Append(q.OwnerId).Append(':').Append(q.Cash).Append(';');
            return sb.ToString();
        }

        /// The first invariant this world breaks, or null.
        ///
        /// Every clause is a thing the rest of the game reads without checking.
        /// None of them is a threshold — they are the ranges the types
        /// themselves already promise, which is why they can be asserted
        /// without measuring anything first.
        static string Broken(GameTime now, Wallet w, Campaign c, Economy e,
                             GossipMill m, PurseBook p)
        {
            if (w.Clean < 0) return $"wallet.Clean={w.Clean}";
            if (w.Dirty < 0) return $"wallet.Dirty={w.Dirty}";
            if (Bad(c.OutfitPatience)) return $"patience={c.OutfitPatience}";
            if (c.OutfitPatience < 0.0 || c.OutfitPatience > 1.0)
                return $"patience={c.OutfitPatience} outside 0..1";
            if (c.JobsDone < 0 || c.JobsMissed < 0)
                return $"jobs={c.JobsDone}/{c.JobsMissed}";
            if (Bad(e.Prosperity)) return $"prosperity={e.Prosperity}";
            if (Bad(e.PriceLevel)) return $"priceLevel={e.PriceLevel}";
            if (e.PriceLevel <= 0.0) return $"priceLevel={e.PriceLevel} (a price cannot be free)";
            foreach (var g in m.Agents)
            {
                if (Bad(g.Loyalty)) return $"{g.Id}.Loyalty={g.Loyalty}";
                if (Bad(g.Suspicion.Value)) return $"{g.Id}.Suspicion={g.Suspicion.Value}";
                if (g.Suspicion.Value < 0.0 || g.Suspicion.Value > 1.0)
                    return $"{g.Id}.Suspicion={g.Suspicion.Value} outside 0..1";
                foreach (var r in g.Rumors)
                    if (Bad(r.Confidence)) return $"{g.Id} holds a rumour with confidence {r.Confidence}";
            }
            foreach (var q in p.All)
                if (q.Cash < 0) return $"{q.OwnerId}'s purse holds {q.Cash}";
            return null;
        }

        static bool Bad(double d) => double.IsNaN(d) || double.IsInfinity(d);

        /// Same seven-person street the lab and the game wire up.
        static GossipMill BuildStreet()
        {
            var graph = new SocialGraph();
            graph.Link("Rocco", "Lena", 0.7);
            graph.Link("Rocco", "Sam", 0.8);
            graph.Link("Sam", "Lena", 0.6);
            graph.Link("Ada", "Lena", 0.6);
            graph.Link("Ada", "Sam", 0.5);
            graph.Link("Joey", "Rocco", 0.6);
            graph.Link("Joey", "Sam", 0.3);
            graph.Link("Marla", "Ada", 0.5);
            graph.Link("Marla", "Sam", 0.4);
            graph.Link("Victor", "Lena", 0.4);
            graph.Link("Victor", "Sam", 0.5);
            var mill = new GossipMill(graph);
            mill.Add(Brain("Lena", "day", 0.25, 0.75, 0.5));
            mill.Add(Brain("Rocco", "night", 0.6, 0.5, 0.6));
            mill.Add(Brain("Ada", "day", 0.15, 0.8, 0.4));
            mill.Add(Brain("Sam", "both", 0.85, 0.25, 0.3));
            mill.Add(Brain("Joey", "night", 0.7, 0.45, 0.35));
            mill.Add(Brain("Marla", "day", 0.55, 0.35, 0.4));
            mill.Add(Brain("Victor", "day", 0.7, 0.4, 0.4));
            return mill;
        }

        static Gossiper Brain(string name, string circle, double greed, double nerve, double loyalty) =>
            new Gossiper(name, name, new MemoryStore(name.ToLowerInvariant()), new KnowledgeBase(),
                         new SuspicionTracker(), circle, greed, nerve, loyalty);

        /// Evenly spaced readings including both ends — the shape of the curve
        /// rather than its first eight days, which on a growth question is the
        /// only part that answers anything.
        static List<int> Sample(List<int> series, int n)
        {
            var outp = new List<int>();
            if (series.Count == 0) return outp;
            if (series.Count <= n) return new List<int>(series);
            for (int i = 0; i < n; i++)
                outp.Add(series[(int)((long)i * (series.Count - 1) / (n - 1))]);
            return outp;
        }

        static string Snip(string s) =>
            s == null ? "(none)" : s.Length <= 110 ? s : s.Substring(0, 110) + "…";

        static int ArgInt(string[] args, string name, int fallback)
        {
            for (int i = 0; i + 1 < args.Length; i++)
                if (args[i] == name && int.TryParse(args[i + 1], out var v)) return v;
            return fallback;
        }
    }
}
