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
    ///     dotnet run -c Release --project ledger/Soak -- --residents 7,50,200
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
    ///
    ///   5. POPULATION, AND WHAT A RESIDENT ABOVE SEVEN IS. Queue 351, ruled by
    ///      Jafar 2026-09-16, with queue 116 folded into it: "the soak is run at
    ///      50 residents and then at 200, and reports what holds and what falls
    ///      over". `--residents 7,50,200` is a LADDER: one contributor moves,
    ///      every rung printed from the same vantage in one process, because a
    ///      rung compared across runs is a different photograph.
    ///
    ///      THE SEVEN ARE AUTHORED AND EVERYBODY ABOVE THEM IS A COPY WITH A
    ///      VARIED SEED. `BuildTown` states exactly what varies (id, three
    ///      jittered traits, drawn ties) and what does not (behaviour, circle
    ///      mix, vocabulary, schedule, economy), and every line carrying a
    ///      population says `copies-with-varied-seeds` in those words. So a
    ///      number from here bounds the MACHINERY and says nothing about
    ///      content or social variety, and the run's own `soakSupports` line
    ///      says so rather than leaving it to a document that may not travel
    ///      with the tool.
    ///
    ///      WHAT THE FIRST REAL SERIES SAID, 2026-09-21, 500 days, seed 1,
    ///      rungs 7/50/200/300/500: everything gated HELD (determinism, the
    ///      invariants, nobody forgot), wall clock grew 3.0x for 28.6x the
    ///      population, and the thing that fell over was REACH. Residents who
    ///      ever remembered anything: 7 of 7, then 17 of 50, then 15 of 200,
    ///      20 of 300, 15 of 500. Talk never crossed more than two mouths in
    ///      2187 hops, so the audience is the witness's two-hop neighbourhood
    ///      and that is a constant of the mean degree, not of the town.
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
            // A LIST AND NOT A NUMBER, because the answer to "does it scale"
            // is a difference between rungs and a rung compared across runs is
            // a different photograph: `--residents 7,50,200` drives all three
            // from one process, one binary, one clock.
            int[] asked = ArgInts(args, "--residents", new[] { AuthoredResidents });

            // THE FOUR NUMBERS, BEFORE JAFAR RULES ON REACH. A measurement and
            // nothing else: no gate, no constant changed, and it says so.
            if (args.Contains("--reach-series"))
                return ReachSeries(asked.Length > 0 && asked[0] > AuthoredResidents ? asked[0] : 200,
                                   days, seed);

            SelfTest();

            // THE FIRST RUNG PAYS THE JIT BILL AND THE LADDER READS IT AS
            // SCALING. Measured before this line existed: the 7-resident
            // control spent 0.22s on its first half and 0.11s on its second,
            // identical work, and on a ladder that whole overhead lands on the
            // smallest rung and flatters every rung above it. A throwaway
            // three-day run pays it before anything is timed.
            Run(3, seed, AuthoredResidents);

            var ladder = new List<Rung>();
            foreach (int want in asked)
            {
                int residents = Math.Max(AuthoredResidents, want);
                if (residents != want)
                    Console.WriteLine($"  NOTE: --residents {want} is under the authored roster of "
                                      + $"{AuthoredResidents}; CLAMPED to {residents} (the seven are "
                                      + "authored and this tool does not delete people)");
                ladder.Add(RunRung(residents, days, seed));
            }
            if (ladder.Count > 1) PrintLadder(ladder);
            PrintSupports(ladder, days, seed);

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

        /// ONE RUNG: the same world at one population, run twice.
        ///
        /// Everything whole-run goes on this rung's done line and nothing
        /// per-day does, because a reader greping `events=` across a ladder
        /// otherwise gets three moments as one.
        static Rung RunRung(int residents, int days, int seed)
        {
            Console.WriteLine();
            Console.WriteLine($"Soak — {days} in-game days, seed {seed}, residents {residents}");

            var swA = System.Diagnostics.Stopwatch.StartNew();
            var a = Run(days, seed, residents);
            swA.Stop();
            var swB = System.Diagnostics.Stopwatch.StartNew();
            var b = Run(days, seed, residents);
            swB.Stop();

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
                if (series.Count == 0)
                {
                    // THE NEVER-RAN CASE IS A SENTENCE AND NOT A CRASH. This
                    // block indexed [0] of an empty list, so a run where no day
                    // ever closed (`--days 1`) ended in a stack trace after
                    // behaving correctly, which costs twenty minutes before
                    // anybody notices it worked.
                    Console.WriteLine($"    {label,-16} nothing measured (0 closed days)");
                    continue;
                }
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

            // ---- 5. what this population cost to run (queue 351) ----------
            var rung = new Rung
            {
                residents = residents,
                synthetic = residents - AuthoredResidents,
                days = days,
                closedDays = a.closedDays,
                wallSecA = swA.Elapsed.TotalSeconds,
                wallSecB = swB.Elapsed.TotalSeconds,
                o = a,
                rssHwmBytes = RssHighWaterBytes(),
            };
            ScaleReport(rung);
            return rung;
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
                        // THE DENOMINATOR NAMES WHAT IT COUNTED. At 200
                        // residents only fifteen ever heard anything, and a
                        // gate reporting "200 residents examined" would be
                        // counting 185 people who had nothing to forget as
                        // evidence that nothing was forgotten.
                        ? $"nothing is ever wiped ({a.events} events over {a.agents} residents"
                          + $" x {a.closedDays} closed days examined, of whom"
                          + $" {a.residentsWithAnyMemory} ever had anything to forget)"
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

            // EVERY DENOMINATOR, NOT JUST THE FIRST ONE. This guarded `events`
            // alone, so a run that closed no day (`--days 1`) divided by zero
            // days and printed `eventsPerNpcPerDay=Infinity` and `300residents
            // /0days=NaNMB`: a confident-looking value from a run that measured
            // nothing, which is rule 3b exactly. `MemoryStore.BudgetLine` in
            // the tested layer already guards all three, and this is the copy
            // of that idea that nobody had run.
            if (a.events <= 0 || a.agents <= 0 || a.closedDays <= 0)
            {
                Console.WriteLine("  memory: NOTHING MEASURED"
                                  + $" ({a.events} events over {a.agents} residents"
                                  + $" x {a.closedDays} closed days; a zero in any of the three"
                                  + " means there is no rate to print)");
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
            // THE COVERAGE RIDES ON THE SAME LINE AS THE RATE IT DIVIDES, and
            // not three lines away: this mean is over EVERY resident, most of
            // whom may have heard nothing, and a reader who takes it for one
            // resident's rate has the projection wrong by exactly that factor.
            Console.WriteLine($"    eventsPerNpcPerDay(mean-over-{a.agents}-residents-x-{a.closedDays}-days)={rate:0.000}"
                              + $" busiestResident={busiest:0.000}"
                              + $" remembered={a.residentsWithAnyMemory}/{a.agents}residents"
                              + $"   [queue-116:{AuthoredResidents}authored+{a.agents - AuthoredResidents}copies-with-varied-seeds]");
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

            /// QUEUE 351, THE SCALE HALF. Every field here is named for the
            /// statistic it is, because "gossip fan-out" is four different
            /// numbers and only one of them answers any given question.

            /// CUMULATIVE over the whole run: every rumour hop the mill made.
            /// Read where the run ends, never inside a sampler.
            public long gossipHops;

            /// PEAK over the hours of the run: the busiest single gossip
            /// round, the day it happened, and the two denominators captured
            /// AT THAT INSTANT rather than at the end (rule 2, four sites on
            /// 4 August divided two maxima).
            public int gossipPeakPerHour;
            public int gossipPeakDay = -1;
            public int rumoursHeldAtWorst, carriersAtWorst;

            /// LAST-WINS, at the end of the run: how many residents hold at
            /// least one remembered event, and how many hold at least one
            /// live rumour. The denominator is `agents`. Pillar 1 says they
            /// ALL remember, so this is the fraction that claim is about.
            public int residentsWithAnyMemory, residentsWithAnyRumour;

            /// MEDIAN over residents of the remembered-event count at the end
            /// of the run. A mean cannot see a minority and this world has
            /// one by construction: most of a big town is out of earshot.
            public int medianAgentEvents;

            /// The shape of the graph the run was actually driven on, measured
            /// off the built graph rather than assumed from the generator.
            public double meanDegree;
            public int minDegree, maxDegree, isolated, ties, tiesWanted, witnessDegree;
            public bool tieGuardBit;

            /// How many residents sit within one, two and three mouths of the
            /// witness, measured off the built graph. The reach number's
            /// denominator: "15 of 200 remembered" is a different finding
            /// depending on how many were ever within earshot.
            public int witnessBall1, witnessBall2, witnessBall3;

            /// CUMULATIVE over the run, by hop count: how far talk actually
            /// travelled. Index 0 is unused by construction (a hop event is at
            /// least the first hop) and the last bucket is a cap that says so.
            public readonly int[] hopHistogram = new int[6];
            public int maxHopEver;   // PEAK over the run

            /// RETAINED, forced-collect, world still alive: bytes the whole
            /// run holds at the end minus what the process held before it
            /// started. Includes this instrument's own per-day records, and
            /// `instrumentChars` is the part of that which is ours.
            public long heapRetainedBytes, instrumentBytes;

            /// PEAK of GC.GetTotalMemory(false) sampled at each day close, and
            /// the day it peaked. Sampled and uncollected: an upper envelope
            /// of the live heap, never a retained figure.
            public long heapPeakSampledBytes;
            public int heapPeakDay = -1;
        }

        /// One population's whole-run reading. Whole-run numbers only: the
        /// per-day series stay on `Outcome` and get printed on their own lines.
        /// THE FOUR NUMBERS JAFAR ASKED FOR, 22 September, before he rules on
        /// reach: "how strong the town's friendships actually are, how
        /// confident a witness is at first sight, what counts as one retelling,
        /// and then a series showing how reach moves as each one is changed
        /// alone. I am not turning a constant up until a rumour crosses the
        /// town."
        ///
        /// EVERY KNOB DEFAULTS TO WHAT THE GAME DOES, so a run with none turned
        /// is the run this tool has always made - proved by diffing its output
        /// before and after this was added, not asserted. NOTHING HERE CHANGES
        /// A SHIPPED CONSTANT: HopDecay and MinConfidenceToShare are fields on
        /// the mill INSTANCE this run builds, and the ties are scaled as this
        /// run links them.
        sealed class Knobs
        {
            /// Multiplies every tie, authored and drawn, as it is linked. The
            /// graph clamps at 1.0, so scaling past that saturates rather than
            /// inventing a friendship stronger than total.
            public double TieScale = 1.0;
            /// The confidence a witness files at. The soak has always called
            /// Witness with no confidence, so its default, 1.0 - CERTAIN - is
            /// what every reach number this tool has printed was measured at.
            public double FirstSight = 1.0;
            /// NaN means the mill's own value is left alone.
            public double HopDecay = double.NaN;
            public double ShareFloor = double.NaN;
            /// SEVERITY. The mill already treats a body as indelible - it
            /// "arrives at the far end of the street exactly as true as it
            /// left" - so this files the witnessed fact as indelible, which is
            /// the route severity already has. Not a new rule: the existing one,
            /// measured.
            public bool Indelible = false;
            public string Label = "as-shipped";
            public static readonly Knobs Shipped = new Knobs();
        }

        /// THE REACH SERIES, 22 September. Jafar, before ruling: "print the
        /// numbers the old studio asked for and never produced. How strong the
        /// town's friendships actually are, how confident a witness is at first
        /// sight, what counts as one retelling, and then a series showing how
        /// reach moves as each one is changed alone. I am not turning a
        /// constant up until a rumour crosses the town; my instinct is that one
        /// act reaching a circle is right, and that town-wide knowledge should
        /// come from severity, repetition and the newspaper. The series tells
        /// me whether that instinct survives."
        ///
        /// ONE RUN PER SETTING, same seed, same days, same town: the only thing
        /// that differs between two rows is the knob the row names. The
        /// determinism check is the ordinary soak's job and is not repeated.
        static int ReachSeries(int residents, int days, int seed)
        {
            Console.WriteLine($"REACH SERIES - {residents} residents, {days} days, seed {seed}. "
                              + "A MEASUREMENT: no gate, and no shipped constant is changed.");

            // ---- 1. THE FRIENDSHIPS -------------------------------------------
            var g0 = new SocialGraph();
            var street = BuildStreet(g0);
            var authored = new List<double>();
            foreach (var a in street.Agents)
                foreach (var c in g0.Contacts(a.Id))
                    if (string.CompareOrdinal(a.Id, c) < 0) authored.Add(g0.Tie(a.Id, c));
            authored.Sort();
            Console.WriteLine();
            Console.WriteLine("1. HOW STRONG THE TOWN'S FRIENDSHIPS ACTUALLY ARE");
            Console.WriteLine($"   the seven authored residents have {authored.Count} ties between them, "
                              + $"weights {string.Join(" ", authored.Select(w => w.ToString("0.0")))}");
            Console.WriteLine($"   mean {authored.Average():0.00}, weakest {authored.First():0.0}, "
                              + $"strongest {authored.Last():0.0}");
            Console.WriteLine("   everybody above the seven is a copy whose ties are DRAWN FROM THIS SAME BAG, "
                              + "so this is the whole town's distribution, not a sample of it");

            // ---- 2. FIRST SIGHT ------------------------------------------------
            Console.WriteLine();
            Console.WriteLine("2. HOW CONFIDENT A WITNESS IS AT FIRST SIGHT");
            Console.WriteLine("   the game's own callers, read off the code: a body seen in the open 1.0, "
                              + "a body seen occluded 0.6, street trouble 0.5, a racket sighting "
                              + "0.45 to 0.80 by the runner's competence");
            Console.WriteLine("   THIS SOAK HAS ALWAYS WITNESSED AT 1.0 - CERTAIN - the most favourable case "
                              + "there is, so every reach figure it has printed is a ceiling");

            // ---- 3. ONE RETELLING ----------------------------------------------
            var mill0 = new GossipMill(new SocialGraph());
            Console.WriteLine();
            Console.WriteLine("3. WHAT COUNTS AS ONE RETELLING");
            Console.WriteLine($"   a speaker passes a rumour to a friend they are WITH at the time; it arrives at "
                              + $"confidence x tie x {mill0.HopDecay:0.00} and is refused below "
                              + $"{mill0.MinConfidenceToShare:0.00}; one hop per round");
            Console.WriteLine("   A BODY IS EXEMPT: an indelible fact arrives exactly as true as it left, "
                              + "so severity already has a road across town and ordinary talk does not");
            Console.WriteLine("   how many retellings a CERTAIN rumour survives along a chain of equal ties:");
            foreach (var t in new[] { 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0 })
            {
                double c = 1.0; int n = 0;
                while (n < 50)
                {
                    double next = c * t * mill0.HopDecay;
                    if (next < mill0.MinConfidenceToShare) break;
                    c = next; n++;
                }
                Console.WriteLine($"     tie {t:0.0}: {n} retelling(s), last at {c:0.00}");
            }

            // ---- 4. THE SERIES -------------------------------------------------
            Console.WriteLine();
            Console.WriteLine("4. HOW REACH MOVES AS EACH IS CHANGED ALONE");
            Console.WriteLine("   remembered = residents who ever remembered anything; two-tie-circle = residents "
                              + "within two ties of the witness on the built graph, the most a two-retelling story could reach");
            var rows = new List<Knobs> { new Knobs { Label = "as-shipped" } };
            foreach (var v in new[] { 0.75, 1.25, 1.5, 2.0 })
                rows.Add(new Knobs { TieScale = v, Label = $"ties x{v:0.00}" });
            foreach (var v in new[] { 0.5, 0.6, 0.8 })
                rows.Add(new Knobs { FirstSight = v, Label = $"first-sight {v:0.00}" });
            foreach (var v in new[] { 0.7, 0.9, 1.0 })
                rows.Add(new Knobs { HopDecay = v, Label = $"hop-decay {v:0.00}" });
            foreach (var v in new[] { 0.3, 0.1, 0.05 })
                rows.Add(new Knobs { ShareFloor = v, Label = $"share-floor {v:0.00}" });
            // AND SEVERITY, the half of the instinct the four knobs do not
            // reach: the same witnessing, filed the way a body is filed.
            rows.Add(new Knobs { Indelible = true, Label = "severe (indelible)" });

            Console.WriteLine($"   {"setting",-20} {"remembered",14} {"two-tie-circle",14} {"max-hops",9}  hops-by-distance(1..5+)");
            foreach (var k in rows)
            {
                var o = Run(days, seed, residents, k);
                int earshot = o.witnessBall2;
                Console.WriteLine($"   {k.Label,-20} {o.residentsWithAnyMemory,6}/{o.agents,-7} "
                                  + $"{earshot,14} "
                                  + $"{o.maxHopEver,9}  "
                                  + string.Join(" ", o.hopHistogram.Skip(1)));
                Console.WriteLine($"reachSeriesRow setting={k.Label.Replace(' ', '_')} residents={o.agents} "
                                  + $"remembered={o.residentsWithAnyMemory} earshot2={earshot} "
                                  + $"maxHop={o.maxHopEver} hops={string.Join(",", o.hopHistogram.Skip(1))}");
            }
            Console.WriteLine();
            Console.WriteLine("reachSeries done: a measurement; nothing tuned, nothing gated.");
            return 0;
        }

        class Rung
        {
            public int residents, synthetic, days, closedDays;
            public double wallSecA, wallSecB;
            public long rssHwmBytes;
            public Outcome o;
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
        static Outcome Run(int days, int seed, int residents) =>
            Run(days, seed, residents, Knobs.Shipped);

        static Outcome Run(int days, int seed, int residents, Knobs k)
        {
            // THE BASELINE FOR THE RETAINED FIGURE, taken after a forced
            // collect and before anything of this run exists, so a previous
            // rung's leftovers sit in the baseline rather than in the answer.
            long heapAtStart = GC.GetTotalMemory(true);
            var o = new Outcome();
            var rng = new Random(seed);
            var camp = new Campaign();
            var mill = BuildTown(residents, seed, o, k);
            var wallet = new Wallet(250);
            var economy = Ledger.Game.EconomySetup.Build();
            var purses = new PurseBook();
            purses.Add(new Purse { OwnerId = "Sam", Name = "Sam", Weekly = 60, Ceiling = 95, Cash = 45 });
            purses.Add(new Purse { OwnerId = "Rocco", Name = "Rocco", Weekly = 140, Ceiling = 260, Cash = 180 });
            purses.Add(new Purse { OwnerId = "Donna", Name = "Donna", Weekly = 220, Ceiling = 520, Cash = 380 });

            mill.Witness(WitnessId, new Fact("player", "location_d2_evening", "warehouse"),
                         "the new owner was at the old warehouse the night of the fire",
                         true, new GameTime(1, 9, 0), k.FirstSight, k.Indelible);

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

                // FAN-OUT IS A RETURN VALUE THIS LOOP USED TO DROP. One hop is
                // one rumour crossing one tie, so this is the mill's work per
                // hour and the thing that grows with the graph.
                var hops = mill.Tick(now, (x, y) => rng.NextDouble() < 0.10);
                o.gossipHops += hops.Count;                       // CUMULATIVE
                foreach (var h in hops)
                {
                    // HOW FAR IT GOT, cumulative. This is the mechanism behind
                    // any reach number below: confidence decays per hop and
                    // stops being shared under MinConfidenceToShare, so the
                    // ceiling here is the Core's rule and not the town's size.
                    o.hopHistogram[Math.Min(h.Rumor.Hops, o.hopHistogram.Length - 1)]++;
                    if (h.Rumor.Hops > o.maxHopEver) o.maxHopEver = h.Rumor.Hops;
                }
                if (hops.Count > o.gossipPeakPerHour)             // PEAK, with its own instant's denominators
                {
                    o.gossipPeakPerHour = hops.Count;
                    o.gossipPeakDay = now.Day;
                    o.rumoursHeldAtWorst = mill.Agents.Sum(g => g.Rumors.Count);
                    o.carriersAtWorst = mill.Agents.Count(g => g.Rumors.Count > 0);
                }

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
                    mill.Witness(WitnessId, new Fact("player", "seen_d" + now.Day, "the yard"),
                                 "somebody was in the yard again", true, now, k.FirstSight, k.Indelible);

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

                // PEAK of a SAMPLED live-heap reading, over the baseline, with
                // the day it peaked. Uncollected garbage is in it, so it is an
                // upper envelope and never a retained figure; the retained one
                // is taken once, forced, at the end.
                long heapNow = GC.GetTotalMemory(false) - heapAtStart;
                if (heapNow > o.heapPeakSampledBytes)
                {
                    o.heapPeakSampledBytes = heapNow;
                    o.heapPeakDay = now.Day;
                }
            }

            o.verdict = camp.Verdict.ToString();
            o.growth.Add(("rumours", rumours));
            // THE CAP IS IN THE LABEL BECAUSE IT BITES IN EVERY RUN. This
            // series plateaus at 32 reasons a resident (SuspicionTracker
            // .MaxReasons) times however many residents are suspicious at all,
            // and a flat tail that is a ceiling reads exactly like a world
            // that has gone quiet. It is the ceiling.
            o.growth.Add(($"suspicion(cap{SuspicionTracker.MaxReasons}/res)", reasons));
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
            var perAgentFinal = new List<int>();
            var perAgentRumours = new List<int>();
            foreach (var g in mill.Agents)
            {
                perAgentFinal.Add(g.Memory.Events.Count);
                perAgentRumours.Add(g.Rumors.Count);
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
            // LAST-WINS, at the end of the run, through the SAME counter the
            // selftest plants a case against: the fraction pillar 1's "who all
            // remember" is actually about.
            o.residentsWithAnyMemory = CountPositive(perAgentFinal);
            o.residentsWithAnyRumour = CountPositive(perAgentRumours);
            o.medianAgentEvents = Median(perAgentFinal);

            // WHAT THIS INSTRUMENT ITSELF HOLDS, so the retained figure below
            // can be read as the world's cost minus a named overhead rather
            // than taken whole. A state string per closed day is the bulk of
            // it and it grows with the population, which is exactly the shape
            // that would otherwise be mistaken for the world growing.
            long stateChars = 0;
            foreach (var s in o.states) stateChars += s.Length;
            o.instrumentBytes = 2 * stateChars + 24 * o.states.Count       // the state strings
                              + 4L * o.digests.Count                        // the digests
                              + 4L * o.agents * o.closedDays;               // the per-resident memory series

            // RETAINED, forced, WITH THE WORLD STILL ALIVE. KeepAlive is not
            // decoration: the JIT is free to collect `mill` at its last use,
            // which would measure the cost of a town that had been deleted.
            o.heapRetainedBytes = GC.GetTotalMemory(true) - heapAtStart;
            GC.KeepAlive(mill);
            GC.KeepAlive(perAgentMemory);
            return o;
        }

        /// The middle reading of a set, lower of the two on an even count. A
        /// median and not a mean because a big town's memory is held by a
        /// minority and a mean cannot see one.
        static int Median(List<int> xs)
        {
            if (xs.Count == 0) return 0;
            var sorted = new List<int>(xs);
            sorted.Sort();
            return sorted[(sorted.Count - 1) / 2];
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

        /// HOW MANY RESIDENTS ARE AUTHORED, counted off the roster rather than
        /// written down beside it: two copies of a number are two numbers as
        /// soon as one of them moves.
        static readonly int AuthoredResidents = BuildStreet(new SocialGraph()).Agents.Count();

        /// The one witness the player's night life is offered to. Named once
        /// because the reach numbers are all measured from this person.
        const string WitnessId = "Rocco";

        /// THE TOWN, AND WHAT A SYNTHETIC RESIDENT IS. Read this before
        /// reading any number this tool prints at a population above seven.
        ///
        /// The seven are AUTHORED: names, circles, traits and eleven ties that
        /// somebody wrote. EVERY RESIDENT ABOVE SEVEN IS A COPY OF ONE OF THEM
        /// WITH A VARIED SEED, and the output says so in those words on every
        /// line that carries a population.
        ///
        /// WHAT VARIES between a copy and its archetype: the id, the three
        /// traits (jittered by up to 0.15 either way and clamped), and which
        /// residents they are tied to and how strongly (weights resampled from
        /// the eleven authored ones).
        ///
        /// WHAT DOES NOT VARY, and this is the half that bounds the claim: the
        /// behaviour (one Core drives everybody), the circle (inherited from
        /// the archetype, so the day/night/both mix stays the authored mix),
        /// the vocabulary (one player, one set of facts, the same summaries),
        /// the schedule (there is none here, `together` is a 10% coin per tied
        /// pair and the same coin for everybody), and the economy (one town's
        /// Campaign, Wallet and three purses whatever the population).
        ///
        /// SO WHAT IS A NUMBER FROM HERE A MEASUREMENT OF: the LOAD and the
        /// REACH of the Core's gossip and memory machinery at N residents in
        /// one graph. Not of a town of N people, because a town of N people
        /// has N sets of business and this has one set repeated. It bounds the
        /// machinery and says nothing about the content.
        ///
        /// THE GRAPH is the authored eleven ties plus uniformly drawn random
        /// pairs up to the AUTHORED MEAN DEGREE, which is measured off the
        /// authored street rather than chosen: a town does not give every
        /// resident N acquaintances, so per-capita connectivity is the thing
        /// to hold still while the population moves. The degree distribution
        /// that results is printed, isolates included, because an isolate can
        /// never hear anything and that is half of any reach number here.
        static GossipMill BuildTown(int residents, int seed, Outcome o) =>
            BuildTown(residents, seed, o, Knobs.Shipped);

        static GossipMill BuildTown(int residents, int seed, Outcome o, Knobs k)
        {
            var graph = new SocialGraph();
            var mill = BuildStreet(graph);
            // THE KNOBS THAT LIVE ON THE MILL, set on this run's instance only.
            if (!double.IsNaN(k.HopDecay)) mill.HopDecay = k.HopDecay;
            if (!double.IsNaN(k.ShareFloor)) mill.MinConfidenceToShare = k.ShareFloor;
            // THE AUTHORED TIES, SCALED BY RE-LINKING. Link overwrites and
            // clamps, so this is the authored street at k.TieScale strength.
            // Skipped outright at 1.0, so the shipped run does not even touch
            // the graph a second time.
            if (k.TieScale != 1.0)
            {
                var authored = new List<(string, string, double)>();
                foreach (var g in mill.Agents)
                    foreach (var c in graph.Contacts(g.Id))
                        if (string.CompareOrdinal(g.Id, c) < 0)
                            authored.Add((g.Id, c, graph.Tie(g.Id, c)));
                foreach (var (a, b, w) in authored) graph.Link(a, b, w * k.TieScale);
            }
            var ids = mill.Agents.Select(g => g.Id).ToList();

            // The authored street's own shape, MEASURED off the graph: every
            // tie is counted from both ends, so ends/2 is the tie count and
            // ends/residents is the mean degree.
            var weights = new List<double>();
            int authoredEnds = 0;
            foreach (var id in ids)
                foreach (var c in graph.Contacts(id)) { authoredEnds++; weights.Add(graph.Tie(id, c)); }
            int authoredTies = authoredEnds / 2;
            double authoredMeanDegree = authoredEnds / (double)ids.Count;

            // A SEPARATE DIE FROM THE WORLD'S. `pop` builds the population and
            // never advances the simulation's `rng`, so a population knob
            // cannot silently re-roll the weather.
            var pop = new Random(unchecked(seed * 31 + 17));
            var archetypes = mill.Agents.ToList();
            for (int i = AuthoredResidents; i < residents; i++)
            {
                // ROUND-ROBIN over the seven, so the circle mix and the trait
                // spread stay the authored ones rather than an invented draw.
                var src = archetypes[i % archetypes.Count];
                string id = "res" + i.ToString("000");
                mill.Add(new Gossiper(id, id, new MemoryStore(id.ToLowerInvariant()),
                                      new KnowledgeBase(), new SuspicionTracker(), src.Circle,
                                      Jitter(src.Greed, pop), Jitter(src.Nerve, pop), Jitter(src.Loyalty, pop)));
                ids.Add(id);
            }

            int tiesWanted = (int)Math.Round(authoredMeanDegree * residents / 2.0);
            int ties = authoredTies;
            int tries = 0, maxTries = Math.Max(1000, tiesWanted * 50);
            while (ties < tiesWanted && tries < maxTries)
            {
                tries++;
                string a = ids[pop.Next(ids.Count)], b = ids[pop.Next(ids.Count)];
                if (a == b || graph.Tie(a, b) > 0) continue;
                // The drawn ties come from the authored bag, which above is
                // ALREADY scaled when TieScale is turned, so they scale with it.
                graph.Link(a, b, weights[pop.Next(weights.Count)]);
                ties++;
            }

            var degrees = ids.Select(id => graph.Contacts(id).Count()).ToList();
            o.ties = ties;
            o.tiesWanted = tiesWanted;
            o.tieGuardBit = ties < tiesWanted;          // A CAP THAT ANNOUNCES WHEN IT BITES
            o.meanDegree = degrees.Sum() / (double)degrees.Count;
            o.minDegree = degrees.Min();
            o.maxDegree = degrees.Max();
            o.isolated = degrees.Count(d => d == 0);
            o.witnessDegree = graph.Contacts(WitnessId).Count();
            o.witnessBall1 = Ball(graph, WitnessId, 1);
            o.witnessBall2 = Ball(graph, WitnessId, 2);
            o.witnessBall3 = Ball(graph, WitnessId, 3);
            return mill;
        }

        /// How many residents are within `hops` mouths of `from`, COUNTING
        /// `from`, who is in earshot of himself: he is the one who saw it. The
        /// first version excluded him and printed `remembered=7/6within2hops`,
        /// a numerator above its own denominator, which is the impossibility
        /// that tells you a pair was taken from two different sets.
        ///
        /// A plain breadth-first walk of the graph the run is actually driven
        /// on, so the reach finding is attributable to a structure somebody
        /// can look at rather than emergent.
        static int Ball(SocialGraph graph, string from, int hops)
        {
            var seen = new HashSet<string> { from };
            var edge = new List<string> { from };
            for (int h = 0; h < hops; h++)
            {
                var next = new List<string>();
                foreach (var id in edge)
                    foreach (var c in graph.Contacts(id))
                        if (seen.Add(c)) next.Add(c);
                edge = next;
            }
            return seen.Count;
        }

        /// Up to 0.15 either way on a trait, clamped. The spread is the only
        /// thing telling one copy from another and it is small ON PURPOSE: a
        /// copy with freely random traits would be a different person, and
        /// this tool cannot claim to have written a hundred and ninety-three
        /// people.
        static double Jitter(double v, Random r) =>
            Math.Clamp(v + (r.NextDouble() - 0.5) * 0.30, 0.0, 1.0);

        /// Same seven-person street the lab and the game wire up. The graph is
        /// passed in rather than made here because the town builder above adds
        /// ties to it afterwards, and a mill keeps its graph to itself.
        static GossipMill BuildStreet(SocialGraph graph)
        {
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

        /// A comma list, for the ladder. An unparseable entry is DROPPED AND
        /// SAID SO rather than silently becoming a zero that then clamps to
        /// the authored roster and reads as a deliberate control rung.
        static int[] ArgInts(string[] args, string name, int[] fallback)
        {
            for (int i = 0; i + 1 < args.Length; i++)
            {
                if (args[i] != name) continue;
                var outp = new List<int>();
                foreach (var part in args[i + 1].Split(','))
                {
                    if (int.TryParse(part, out var v)) outp.Add(v);
                    else Console.WriteLine($"  NOTE: {name} value '{part}' is not a number; DROPPED");
                }
                if (outp.Count > 0) return outp.ToArray();
                Console.WriteLine($"  NOTE: {name} parsed to nothing; using the default");
            }
            return fallback;
        }

        /// PEAK RESIDENT SET of the whole PROCESS, from /proc/self/status
        /// VmHWM, or -1 where that file does not exist. Linux-only and it says
        /// so rather than printing a plausible zero.
        ///
        /// PROCESS-CUMULATIVE: a high-water mark over the process lifetime, so
        /// on a multi-rung run every row after the first carries the largest
        /// rung before it. The print says that on the line.
        static long RssHighWaterBytes()
        {
            try
            {
                foreach (var line in System.IO.File.ReadAllLines("/proc/self/status"))
                {
                    if (!line.StartsWith("VmHWM:")) continue;
                    var parts = line.Split(new[] { ' ', '\t' }, StringSplitOptions.RemoveEmptyEntries);
                    if (parts.Length >= 2 && long.TryParse(parts[1], out var kb)) return kb * 1024L;
                }
            }
            catch { }
            return -1;
        }

        /// How many of these counts are above zero. THE ONE IMPLEMENTATION of
        /// "how many residents have any", used by the run and by the planted
        /// case in the selftest, the same shape as `FirstFall`.
        static int CountPositive(List<int> counts)
        {
            int n = 0;
            foreach (int c in counts) if (c > 0) n++;
            return n;
        }

        static string MbOf(long bytes) =>
            bytes < 0 ? "nothing-measured" : (bytes / (1024.0 * 1024.0)).ToString("0.00") + "MB";

        /// QUEUE 351: WHAT ONE POPULATION COST AND HOW FAR IT REACHED.
        ///
        /// WHOLE-RUN NUMBERS ONLY. The per-day series are printed above on
        /// their own lines; mixing the two under one key is how a grep turns
        /// two moments into one.
        static void ScaleReport(Rung r)
        {
            var o = r.o;
            string pop = $"{r.residents}residents/{AuthoredResidents}authored"
                       + $"+{r.synthetic}copies-with-varied-seeds";
            if (o.closedDays <= 0)
            {
                Console.WriteLine($"  scale rung={pop} days={r.days} state=nothing-measured"
                                  + " closedDays=0");
                return;
            }
            double wall = r.wallSecA + r.wallSecB;
            double rate = o.events / (double)o.agents / o.closedDays;
            double amongRemembering = o.residentsWithAnyMemory > 0
                ? o.events / (double)o.residentsWithAnyMemory / o.closedDays : 0.0;

            Console.WriteLine($"  scale rung={pop} days={r.days} closedDays={o.closedDays}");
            Console.WriteLine($"    graph ties={o.ties}/{o.tiesWanted}wanted"
                              + (o.tieGuardBit ? "(GUARD-BIT:draw-gave-up-early)" : "")
                              + $" meanDegree={o.meanDegree:0.00}"
                              + $" degree=min{o.minDegree}/max{o.maxDegree}"
                              + $" isolated={o.isolated}/{o.agents} witnessDegree={o.witnessDegree}");
            // WALL CLOCK, both halves, and the per-day cost that makes rungs
            // comparable. Seconds of one machine, so a ratio between rungs is
            // the number to carry and the absolute is not.
            Console.WriteLine($"    wall runA={r.wallSecA:0.00}s runB={r.wallSecB:0.00}s"
                              + $" bothRuns={wall:0.00}s secPerDayPerRun={wall / 2.0 / o.closedDays:0.0000}");
            // REACH, last-wins at the end of the run. Pillar 1 says they all
            // remember; this is the fraction that sentence is about.
            Console.WriteLine($"    reach remembered={o.residentsWithAnyMemory}/{o.agents}residents"
                              + $" holdingRumour={o.residentsWithAnyRumour}/{o.agents}residents"
                              + $" medianResidentEvents={o.medianAgentEvents}"
                              + $" busiestResidentEvents={o.busiestAgentEvents}"
                              + $" events={o.events}"
                              + $" rememberedOfEarshot={o.residentsWithAnyMemory}/{o.witnessBall2}within2hops");
            // WHY THE REACH NUMBER IS WHAT IT IS, on the line under it: the
            // ball the one witness sits in, and how far talk actually got.
            Console.WriteLine($"    earshot witness={WitnessId} withinHops=1st:{o.witnessBall1}"
                              + $"/2nd:{o.witnessBall2}/3rd:{o.witnessBall3}of{o.agents}residents"
                              + $" hopsTakenCumulative=1st:{o.hopHistogram[1]}/2nd:{o.hopHistogram[2]}"
                              + $"/3rd:{o.hopHistogram[3]}/4th:{o.hopHistogram[4]}"
                              + $"/5thAndBeyond:{o.hopHistogram[5]}"
                              + $" deepestHopEver={o.maxHopEver}");
            // TWO RATES OF ONE VARIABLE, AND THEY ARE NOT INDEPENDENT: the
            // first is the second times remembered/agents. Both are printed
            // because the projection multiplies by a headcount and the reader
            // has to know which headcount.
            Console.WriteLine($"    rate perNpcPerDay(mean-over-{o.agents}-residents-x-{o.closedDays}-days)={rate:0.000}"
                              + $" perRememberingNpcPerDay(mean-over-{o.residentsWithAnyMemory}-x-{o.closedDays})={amongRemembering:0.000}");
            Console.WriteLine($"    gossip hopsCumulative={o.gossipHops}"
                              + $" hopsPerDay={o.gossipHops / (double)o.closedDays:0.00}"
                              + $" peakPerHour={o.gossipPeakPerHour}@d{o.gossipPeakDay}"
                              + $" rumoursHeldAtWorst={o.rumoursHeldAtWorst}"
                              + $" carriersAtWorst={o.carriersAtWorst}/{o.agents}");
            long modelBytes = o.eventBytes;
            // THE INSTRUMENT IS PART OF WHAT IT WEIGHS, and at this population
            // it is most of it: a state string per closed day grows with the
            // roster, so the raw retained figure would read as the world
            // growing. `minusInstrumentModel` is a MEASUREMENT WITH A MODEL
            // SUBTRACTED and is named so rather than passed off as measured.
            long world = o.heapRetainedBytes - o.instrumentBytes;
            Console.WriteLine($"    heap retainedAtEnd={MbOf(o.heapRetainedBytes)}"
                              + $" peakSampledAtDayClose={MbOf(o.heapPeakSampledBytes)}@d{o.heapPeakDay}"
                              + $" instrumentOwn={MbOf(o.instrumentBytes)}"
                              + $" minusInstrumentModel={MbOf(world)}"
                              + $" eventModel={MbOf(modelBytes)}"
                              + $" worldOverEventModelX={(modelBytes > 0 ? (world / (double)modelBytes).ToString("0.0") : "nothing-measured")}");
            Console.WriteLine($"    rss processHighWater={MbOf(r.rssHwmBytes)}"
                              + " scope=whole-process/cumulative-across-rungs");
        }

        /// THE LADDER. One contributor moves (the population) and every rung is
        /// printed from the same vantage in the same process, because a rung
        /// compared across runs is a different photograph.
        ///
        /// Every column is a MULTIPLE OF THE FIRST RUNG, beside the population
        /// multiple, so superlinear is `wallX > popX` read on one line rather
        /// than an arithmetic a reader has to do.
        static void PrintLadder(List<Rung> ladder)
        {
            Console.WriteLine();
            Console.WriteLine($"  ladder base={ladder[0].residents}residents"
                              + " columns=multiples-of-the-base-rung/same-process/same-clock");
            var b = ladder[0];
            double bWall = b.wallSecA + b.wallSecB;
            foreach (var r in ladder)
            {
                var o = r.o;
                if (o.closedDays <= 0)
                {
                    Console.WriteLine($"    ladderRow residents={r.residents} state=nothing-measured");
                    continue;
                }
                double wall = r.wallSecA + r.wallSecB;
                Console.WriteLine($"    ladderRow residents={r.residents}"
                                  + $" popX={r.residents / (double)b.residents:0.0}"
                                  + $" wallX={X(wall, bWall)}"
                                  + $" hopsX={X(o.gossipHops, b.o.gossipHops)}"
                                  + $" eventsX={X(o.events, b.o.events)}"
                                  + $" retainedX={X(o.heapRetainedBytes, b.o.heapRetainedBytes)}"
                                  + $" worldRetainedX={X(o.heapRetainedBytes - o.instrumentBytes, b.o.heapRetainedBytes - b.o.instrumentBytes)}"
                                  + $" remembered={o.residentsWithAnyMemory}/{o.agents}"
                                  + $" rememberedFrac={o.residentsWithAnyMemory / (double)o.agents:0.000}"
                                  + $" ratePerNpcPerDay={o.events / (double)o.agents / o.closedDays:0.000}");
            }
        }

        /// A multiple, or the words for the case where the base was zero: a
        /// ratio with a zero denominator is not a large number, it is an
        /// absent measurement.
        static string X(double v, double baseline) =>
            baseline > 0 ? (v / baseline).ToString("0.0") + "x" : "nothing-measured";

        /// QUEUE 116'S OTHER HALF: THE INSTRUMENT CARRIES ITS OWN LIMITS, so
        /// the next reader gets them from the run rather than from a document
        /// that may not travel with it. The numbers in it are this run's.
        static void PrintSupports(List<Rung> ladder, int days, int seed)
        {
            Console.WriteLine();
            var live = ladder.Where(r => r.o.closedDays > 0).ToList();
            if (live.Count == 0)
            {
                Console.WriteLine("soakSupports state=nothing-measured rungs=0closed-a-day");
                Console.WriteLine("supports: nothing measured. No rung closed a day, so this run is"
                                  + " evidence for nothing at all.");
                return;
            }
            var top = live.OrderByDescending(r => r.residents).First();
            Console.WriteLine($"soakSupports maxResidents={top.residents}"
                              + $" population={AuthoredResidents}authored+{top.synthetic}copies-with-varied-seeds"
                              + $" days={days}x2runs seed={seed} rungs={live.Count}"
                              + $" remembered={top.o.residentsWithAnyMemory}/{top.residents}residents"
                              + " measures=load-and-reach-of-one-Core/not-social-variety"
                              + $" notEvidenceFor={MemoryStore.TargetResidentsLow}..{MemoryStore.TargetResidentsHigh}-authored-residents");
            Console.WriteLine($"supports: the Core ran {top.residents} residents through {days} in-game days"
                              + $" twice at seed {seed}, and what that proves is exactly the checks above:"
                              + " the same seed made the same world, no invariant broke, and nobody forgot.");
            Console.WriteLine($"does not support: D25's {MemoryStore.TargetResidentsLow} to "
                              + $"{MemoryStore.TargetResidentsHigh} residents who all remember. Above "
                              + $"{AuthoredResidents} every resident here is a COPY of one of the seven with a"
                              + " varied seed and randomly drawn ties, so this bounds the MACHINERY and says"
                              + " nothing about content or social variety; and whether they all remember is"
                              + $" the reach line above, which read {top.o.residentsWithAnyMemory} of "
                              + $"{top.residents} at this population.");
            // TWO NUMBERS OUT OF ONE VARIABLE ARE ONE NUMBER TWICE, and here
            // they are: the tick is cheap at this population BECAUSE most of
            // the town carries nothing. Saying so on the run's own last lines
            // is cheaper than the session that quotes the wall clock as
            // headroom for a town where everybody talks.
            if (top.o.residentsWithAnyMemory < top.residents)
                Console.WriteLine($"read together: the wall clock and the reach are one finding twice."
                                  + $" {top.residents - top.o.residentsWithAnyMemory} of {top.residents}"
                                  + " residents carried nothing, so the per-hour cost is a walk over"
                                  + " everybody and real work over almost nobody. A town where every"
                                  + " resident holds talk is NOT measured by this run.");
        }

        /// THE SELFTEST, ACCEPTING CASE FIRST, and it runs on every invocation
        /// rather than behind a flag: a validator nothing survives is the
        /// expensive failure and one nobody runs is the cheap one.
        ///
        /// The live authored street is the accepting fixture, so doing the work
        /// this tool prompts cannot break the tool; the rejecting fixtures are
        /// synthetic counts and a population that exists nowhere.
        static void SelfTest()
        {
            var o7 = new Outcome();
            var t7 = BuildTown(AuthoredResidents, 1, o7);
            int n7 = t7.Agents.Count();
            bool authored = n7 == AuthoredResidents && o7.isolated == 0
                            && !t7.Agents.Any(g => g.Id.StartsWith("res"));
            Require(authored,
                    authored
                        ? $"the authored street builds unchanged at --residents {AuthoredResidents}"
                          + $" ({n7} residents, {o7.ties} ties, {o7.isolated} isolated, 0 copies)"
                        : $"the authored street builds unchanged at --residents {AuthoredResidents}"
                          + $" (got {n7} residents, {o7.ties} ties, {o7.isolated} isolated)");

            // A KNOB THAT DOES NOTHING is the failure this tool is most likely
            // to have, so it is asserted rather than assumed: fifty must be
            // fifty, and the ties must have grown with them.
            var o50 = new Outcome();
            var t50 = BuildTown(50, 1, o50);
            int n50 = t50.Agents.Count();
            Require(n50 == 50 && o50.ties > o7.ties,
                    n50 == 50 && o50.ties > o7.ties
                        ? $"the population knob moves the town (50 residents, {o50.ties} ties"
                          + $" against the authored {o7.ties})"
                        : $"the population knob moves the town (got {n50} residents, {o50.ties} ties)");

            // AND A SEED THAT DOES NOTHING is the same fault one layer down: a
            // builder that ignores its seed would make every rung the same
            // photograph twice.
            var o50b = new Outcome();
            var t50b = BuildTown(50, 1, o50b);
            var o50c = new Outcome();
            var t50c = BuildTown(50, 2, o50c);
            uint same = TownDigest(t50), repeat = TownDigest(t50b), other = TownDigest(t50c);
            Require(same == repeat && same != other,
                    same == repeat && same != other
                        ? "the town builder is deterministic in its seed and sensitive to it"
                          + $" (seed1 {same} twice, seed2 {other})"
                        : $"the town builder is deterministic in its seed and sensitive to it"
                          + $" (seed1 {same}/{repeat}, seed2 {other})");

            // THE REACH COUNTER'S OWN COUNTER-CASE. Three of these five
            // residents remember nothing, and a counter that cannot see that
            // would report a town that all remembers.
            var planted = new List<int> { 0, 4, 0, 0, 9 };
            Require(CountPositive(planted) == 2 && Median(planted) == 0,
                    CountPositive(planted) == 2 && Median(planted) == 0
                        ? "and a town where three of five remember nothing reads as 2 of 5, median 0"
                        : $"and a town where three of five remember nothing reads as 2 of 5, median 0"
                          + $" (counter said {CountPositive(planted)}, median said {Median(planted)})");
        }

        /// A town's shape as one number: every resident's id, degree and greed,
        /// hashed. For the selftest only, and it exists so "the seed did
        /// something" is a comparison rather than an impression.
        static uint TownDigest(GossipMill mill)
        {
            var sb = new StringBuilder();
            foreach (var g in mill.Agents.OrderBy(x => x.Id, StringComparer.Ordinal))
                sb.Append(g.Id).Append(':').Append(g.Greed.ToString("0.0000")).Append(';');
            foreach (var g in mill.Agents.OrderBy(x => x.Id, StringComparer.Ordinal))
                foreach (var other in mill.Agents.OrderBy(x => x.Id, StringComparer.Ordinal))
                    if (mill.Tie(g.Id, other.Id) > 0)
                        sb.Append(g.Id).Append('-').Append(other.Id).Append(':')
                          .Append(mill.Tie(g.Id, other.Id).ToString("0.00")).Append(';');
            return VoiceBank.Hash(sb.ToString());
        }
    }
}
