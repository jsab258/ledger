using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using Ledger.Core;

/// THE STREET'S CAST, ONE SIGHTING, HOUR BY HOUR: who hears the story, and
/// whether it shows. 28 September, for the town list's first two items: the
/// town shows what it has heard, and friends who never meet.
///
///     dotnet run --project ledger/TownReach -c Release -- [--cast production/specs/quay-cast.json] [--days 14] [--every 1] [--ties]
///     ... -- --cast production/specs/hook-cast.json --meridian sheila,ron,darren,ada,june
///     ... -- --cast production/specs/hook-cast.json --two-hours [--clear-every 45] [--deed-at 30] [--town-news]
///     ... -- --cast production/specs/hook-cast.json --meridian ... --teller outfit_man --told-at 22 --answer did
///     ... -- --cast production/specs/hook-cast.json --loud [--second-night]
///     ... -- --cast production/specs/hook-cast.json --first-hour
///
/// A MEASUREMENT AND NOTHING ELSE. It changes no constant and decides nothing:
/// the mill is the shipped GossipMill with its own numbers, the routines are
/// read by Core's CastDay, the bearing is StreetVoice.RegardFor, and the
/// meeting rule is the game's (two tied people within the file's talking
/// range, a round every six game minutes, the hourly fade). It replaces the
/// throwaway programs of 23 September (game-design/rumour-reach-2026-09-23.md
/// section F and rumour-reach-quay-2026-09-23.md), which were never kept, so
/// the next measurement can be run again rather than rewritten.
///
/// WHAT IT PRINTS. The routines' own reading (each friendship's hours and
/// days together a week), then, for each certainty a witness might have at
/// first sight, the mean over every person in the cast as the witness and
/// every hour of a week as the moment they saw it:
///   - how many others hear it, by 30 minutes of play (60 game hours) and by
///     the end;
///   - how long a hearer's knowing SHOWS while they are out on the street,
///     under the rule before 28 September (only a story they would still pass
///     on) and after (a half-remembered one too), in game hours;
///   - how many show it in the same hour: the most in any hour of any run,
///     and the mean of each run's busiest hour, so a handful is seen not to
///     have become a crowd;
///   - how many hearers say something about the story at least once, and
///     how many of those say it half-remembered, to a companion.
/// The friendships are held to CastDay.FriendsMeetDays, the small town's rule.
/// THE ASSUMPTIONS, printed with the numbers: he has met every one of the
/// cast, so they can tell it is him (Acquaintance.Known); on arrival he is a
/// stranger to all of them (canon) and nothing they hold shows, so the hours
/// are what the town shows once he is known, a ceiling; the player passes everybody out on the street once
/// an hour and is always heard, which is generous and the same for both
/// rules; a companion is anybody else of the cast within talking range.
static class Program
{
    static readonly CultureInfo Inv = CultureInfo.InvariantCulture;

    static int Main(string[] args)
    {
        string castPath = Arg(args, "--cast", Path.Combine(RepoRoot(), "production", "specs", "quay-cast.json"));
        int days = int.Parse(Arg(args, "--days", "14"), Inv);
        // Sighting hours taken every N hours of the week (1: every one).
        int every = Math.Max(1, int.Parse(Arg(args, "--every", "1"), Inv));
        var cast = CastDay.Parse(File.ReadAllText(castPath));
        var people = cast.People;
        string metArg = Arg(args, "--meridian", null);
        if (metArg != null) return Meridian(cast, metArg.Split(','), double.Parse(Arg(args, "--rate", "2"), Inv),
                                            Arg(args, "--teller", null), int.Parse(Arg(args, "--told-at", "22"), Inv), Arg(args, "--answer", "did"));
        if (Array.IndexOf(args, "--loud") >= 0) return Loud(cast, Array.IndexOf(args, "--second-night") >= 0);
        if (Array.IndexOf(args, "--first-hour") >= 0) return FirstHourOnPaper(cast, double.Parse(Arg(args, "--rate", "2"), Inv));
        if (Array.IndexOf(args, "--found") >= 0) return FoundInTheMorning(cast);
        if (Array.IndexOf(args, "--arrest") >= 0) return TakenIn(cast);
        if (Array.IndexOf(args, "--week-end") >= 0) return WeekEnd(cast);
        if (Array.IndexOf(args, "--threat") >= 0) return Threat(cast);
        if (Array.IndexOf(args, "--week-waits") >= 0) return WeekWaits(cast);
        if (Array.IndexOf(args, "--week") >= 0) return WeekOnPaper(cast);
        if (Array.IndexOf(args, "--arrival") >= 0) return ArrivalOnPaper(cast);
        if (Array.IndexOf(args, "--two-hours") >= 0) return TwoHours(cast, File.ReadAllText(castPath), double.Parse(Arg(args, "--clear-every", StreetVoice.ClearWordsEverySeconds.ToString(Inv)), Inv),
                                                                   double.Parse(Arg(args, "--deed-at", "-1"), Inv),
                                                                   Array.IndexOf(args, "--town-news") >= 0 ? TownNews.Parse(File.ReadAllText(Path.Combine(Path.GetDirectoryName(Path.GetFullPath(castPath)), "town-news.json"))) : null);

        Console.WriteLine($"townReach cast={Path.GetFileName(castPath)} people={people.Count} ties={cast.Ties.Count} " +
                          $"talkRangeM={cast.TalkRangeM.ToString(Inv)} days={days}");

        // ---- the routines' own reading --------------------------------------
        int never = 0, belowTarget = 0;
        var hoursEach = new List<int>();
        var lines = new List<string>();
        foreach (var (a, b, w) in cast.Ties)
        {
            int hours = cast.HoursTogetherPerWeek(a, b);
            int dayCount = cast.DaysTogetherPerWeek(a, b);
            int want = CastDay.FriendsMeetDays(w);
            if (hours == 0) never++;
            if (dayCount < want) belowTarget++;
            hoursEach.Add(hours);
            lines.Add($"    {(dayCount >= want ? "  " : "! ")}{a}-{b} {w.ToString("0.00", Inv)}: {hours} h a week on {dayCount} days (a small town's rule: {want}+)");
        }
        Console.WriteLine($"coPresence never={never}/{cast.Ties.Count} belowTheTownsRule={belowTarget}/{cast.Ties.Count} " +
                          $"meanHoursPerWeek={hoursEach.DefaultIfEmpty(0).Average():0.0} meanHoursPerDay={hoursEach.DefaultIfEmpty(0).Average() / 7.0:0.0}");
        if (Array.IndexOf(args, "--ties") >= 0) foreach (var l in lines) Console.WriteLine(l);

        Console.WriteLine("assumptions: he has met all of the cast, so they know him by sight (Acquaintance.Known; anybody who has only heard of him shows nothing, by canon, so these hours are a ceiling); he passes everybody out on the street once an hour and is heard; " +
                          "a companion is anybody of the cast within talking range; the sighting hour runs over every hour of one week");

        foreach (double firstSight in new[] { 0.5, 0.6, 1.0 })
        {
            double reach60 = 0, reachEnd = 0, showBefore = 0, showAfter = 0, hearers = 0, storyRemarkers = 0, faintRemarkers = 0;
            int peakBefore = 0, peakAfter = 0, runs = 0, reachedNobody = 0, weekSecond = 0, weekThird = 0;
            var firstHops = new List<int>();
            double heardHour = 0, repeatsSeed = 0, repeatsFresh = 0;
            double busiestBefore = 0, busiestAfter = 0;
            foreach (var witness in people)
                for (int sightHour = 0; sightHour < 24 * 7; sightHour += every)
                {
                    runs++;
                    var graph = new SocialGraph();
                    foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                    var mill = new GossipMill(graph);
                    foreach (var p in people)
                        mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker()));
                    var start = new GameTime(sightHour / 24, sightHour % 24, 0);
                    mill.Age(start);
                    mill.Witness(witness, new Fact("player", "night_walk_d1", "seen"),
                        "the new owner was about the yard after midnight", sensitive: true, start, confidence: firstSight);

                    var remarks = new RemarkLedger();
                    // What he hears in his first hour of play (120 game hours), picked two ways.
                    var bySeed = new List<string>();
                    var byFresh = new List<string>();
                    var fresh = new RemarkLedger();
                    var heardBy = new HashSet<string>();
                    var saidAboutStory = new HashSet<string>();
                    var saidFaintly = new HashSet<string>();
                    int heardBy60 = 0, heardByWeek = -1, firstHop = -1, runPeakBefore = 0, runPeakAfter = 0;
                    for (int hour = 0; hour < days * 24; hour++)
                    {
                        int abs = sightHour + hour;
                        int day = abs / 24, hourOfDay = abs % 24;
                        for (int minute = 0; minute < 60; minute += 6)
                            mill.Tick(new GameTime(day, hourOfDay, minute), (a, b) => cast.Together(a, b, day, hourOfDay));
                        mill.Age(new GameTime((abs + 1) / 24, (abs + 1) % 24, 0));

                        int showingBefore = 0, showingAfter = 0;
                        foreach (var p in people)
                        {
                            var g = mill.Get(p);
                            if (p != witness && g.Rumors.Any(r => r.Content.Subject == "player")) heardBy.Add(p);
                            if (cast.Where(p, day, hourOfDay) == null) continue;   // off the street: nothing shows
                            bool companion = people.Any(o => o != p && cast.Together(p, o, day, hourOfDay));
                            var rg = StreetVoice.RegardFor(g, mill.MinConfidenceToShare, false, remarks, Acquaintance.Known, companion);
                            if (rg.Speaks && rg.Story != null)
                            {
                                if (hour < 120)
                                {
                                    int seed = (int)(Fnv(p + "@" + abs) & 0x7fffffff);
                                    var seedLine = rg.Faint ? StreetVoice.FaintRemark(g, rg.Story, seed) : StreetVoice.Recognition(g, rg.Story, rg.Stance, seed);
                                    var freshLine = rg.Faint ? StreetVoice.FaintRemark(g, rg.Story, seed, fresh) : StreetVoice.Recognition(g, rg.Story, rg.Stance, seed, fresh);
                                    if (seedLine != null && freshLine != null)
                                    {
                                        bySeed.Add(seedLine.Text);
                                        byFresh.Add(freshLine.Text);
                                        fresh.Heard(freshLine);
                                    }
                                }
                                bool aboutStory = rg.Faint || rg.Stance == StanceKind.Comments;
                                if (rg.Faint) remarks.RecordFaint(p, rg.Story, heard: true);
                                else remarks.Record(p, rg.Story, rg.Stance, heard: true);
                                if (p != witness && aboutStory) saidAboutStory.Add(p);
                                if (p != witness && rg.Faint) saidFaintly.Add(p);
                            }
                            if (p == witness) continue;
                            if (rg.Knowing == Knowing.Enough) { showingBefore++; showBefore++; }
                            if (rg.Knowing != Knowing.Nothing) { showingAfter++; showAfter++; }
                        }
                        runPeakBefore = Math.Max(runPeakBefore, showingBefore);
                        runPeakAfter = Math.Max(runPeakAfter, showingAfter);
                        if (firstHop < 0 && heardBy.Count > 0) firstHop = hour + 1;
                        if (hour == 59) heardBy60 = heardBy.Count;
                        if (hour == 24 * 7 - 1) heardByWeek = heardBy.Count;
                    }
                    peakBefore = Math.Max(peakBefore, runPeakBefore);
                    peakAfter = Math.Max(peakAfter, runPeakAfter);
                    busiestBefore += runPeakBefore;
                    busiestAfter += runPeakAfter;
                    reach60 += heardBy60;
                    reachEnd += heardBy.Count;
                    hearers += heardBy.Count;
                    storyRemarkers += saidAboutStory.Count;
                    faintRemarkers += saidFaintly.Count;
                    if (heardBy.Count == 0) reachedNobody++;
                    if (heardByWeek < 0) heardByWeek = heardBy.Count;
                    if (firstHop > 0) firstHops.Add(firstHop);
                    heardHour += bySeed.Count;
                    repeatsSeed += bySeed.Count - bySeed.Distinct().Count();
                    repeatsFresh += byFresh.Count - byFresh.Distinct().Count();
                    if (heardByWeek >= 1) weekSecond++;
                    if (heardByWeek >= 2) weekThird++;
                }
            double perHearer(double v) => hearers > 0 ? v / hearers : 0;
            Console.WriteLine($"FIRST SIGHT {firstSight.ToString("0.00", Inv)}: runs={runs} (every witness x every {every} h of a week)");
            Console.WriteLine($"  reach: others who hear it  at 60h mean={reach60 / runs:0.00}  by day {days} mean={reachEnd / runs:0.00}  witnesses reaching nobody={reachedNobody}/{runs}");
            // ROADMAP stage 3's test: the witness is the first resident to hold it;
            // a second and a third are the first two others to hear it.
            Console.WriteLine($"  stage 3 (one game week): reached a second resident {weekSecond}/{runs} ({weekSecond * 100.0 / runs:0}%), a second and a third {weekThird}/{runs} ({weekThird * 100.0 / runs:0}%)");
            // THE FIRST HOP, the teaching research's "one number to measure next": how
            // long, from the sighting, until one other person holds the story. A game
            // day is twelve real minutes (MinutesPerRealSecond 2), so an hour is thirty
            // real seconds.
            firstHops.Sort();
            if (firstHops.Count > 0)
                Console.WriteLine($"  first hop (runs where it happened, {firstHops.Count}/{runs}): median {firstHops[firstHops.Count / 2]} game h ({firstHops[firstHops.Count / 2] * 0.5:0} real min), " +
                                  $"slowest tenth {firstHops[(int)(firstHops.Count * 0.9)]} game h ({firstHops[(int)(firstHops.Count * 0.9)] * 0.5:0} real min)");
            // ROADMAP stage 6, "hours without repetition": lines about him that he
            // hears in his first hour of play, and how many repeat one already heard.
            Console.WriteLine($"  first hour, lines about him heard: mean {heardHour / runs:0.0}; repeats, chosen by the seed alone {repeatsSeed / runs:0.00}, " +
                              $"with the ledger of what he has heard {repeatsFresh / runs:0.00}");
            Console.WriteLine($"  shows, per hearer, game hours out on the street:  before={perHearer(showBefore):0.0}  after={perHearer(showAfter):0.0}");
            Console.WriteLine($"  showing in the same hour:  most in any run before={peakBefore} after={peakAfter};  a run's busiest hour, mean before={busiestBefore / runs:0.0} after={busiestAfter / runs:0.0}");
            Console.WriteLine($"  hearers who say something about the story at least once: {perHearer(storyRemarkers) * 100:0}%  " +
                              $"(half-remembered, to a companion: {(storyRemarkers > 0 ? faintRemarkers / storyRemarkers * 100 : 0):0}% of those who say something)");
        }
        return 0;
    }

    /// HIS ARRIVAL (town list 6cg): he comes to Mickey's at nine on the Monday;
    /// whoever is about Mickey's then, and Ada on her step, hold it first-hand.
    /// How many hold it by that evening and by noon on the Tuesday, on the
    /// game's own hourly call; and whether it ever shows over a deed's story.
    static int ArrivalOnPaper(CastDay cast)
    {
        var graph = new SocialGraph();
        foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
        var mill = new GossipMill(graph);
        foreach (var p in cast.People) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
        int Holders() => mill.Agents.Count(a => a.Rumors.Any(DayOne.IsArrival));
        // Who would say it to his face on sight, a stranger to them all: only
        // those who saw him come (the rest cannot tell it is him).
        int Showing() => mill.Agents.Count(a => StreetVoice.ArrivalLine(a, mill.MinConfidenceToShare, null, 0, 0.0, false, false) != null);
        var at = new Dictionary<string, string>();
        List<string> saw = null;
        mill.Age(new GameTime(0, 9, 0));
        for (int abs = 9; abs < 24 + 13; abs++)
        {
            int day = abs / 24, hod = abs % 24;
            var now = new GameTime(day, hod, 0);
            if (abs == 9) saw = DayOne.Arrived(mill, cast, now);
            TownRounds.Hour(mill, cast, now);
            if (day == 0 && hod == 12) at["Monday noon"] = $"{Holders()} hold it, {Showing()} would say it";
            if (day == 0 && hod == 20) at["Monday evening"] = $"{Holders()} hold it, {Showing()} would say it";
            if (day == 1 && hod == 12) at["Tuesday noon"] = $"{Holders()} hold it, {Showing()} would say it";
        }
        Console.WriteLine("his arrival: at Mickey's at nine on the Monday");
        Console.WriteLine($"  saw him come: {string.Join(", ", saw)}");
        foreach (var kv in at) Console.WriteLine($"  by {kv.Key}: {kv.Value} of {cast.People.Count}");
        return 0;
    }

    /// THE WHOLE WEEK ON PAPER (town list 6ce): day 1 to day 7 with every piece
    /// running together, on the game's own hourly call (TownRounds.Hour), for
    /// his choices: the envelope taken every night or Ron told no on night
    /// one; Ada's tea sat through or stood up; and the slice's window, at noon
    /// on the Tuesday, seen by Sheila from Mickey's rank (as the slice has it),
    /// by Ada, by nobody, or not done. Each piece as its own mode runs it: the
    /// asks (Delivered at eight, answered at half past ten, the tea's night
    /// after the walk), the tea, the damage found and mended the next morning
    /// (Aftermath), whoever saw it going to the police if they would
    /// (PoliceFile.WouldReport, the morning after), the constable at ten and
    /// custody, DS Ellis at nine on the street's talk and whom she asks, and on
    /// the Sunday Sheila's question at half past ten, answered "take it over".
    /// He talks with Sheila every morning at the office. Her trust is read as
    /// the talk reads it with two stand-ins the talk would have: her own
    /// sighting of a deed, or any story of his nights in her hands at the share
    /// floor, is a deed she has seen or heard of him at; and she is wary once
    /// such a story shows in her manner. The table is for Jafar's page.
    static int WeekOnPaper(CastDay cast)
    {
        Console.WriteLine("the whole week on paper: from 09:00 on day 1 (a Monday) to noon on day 8; he talks with Sheila each morning at ten");
        Console.WriteLine(WeekHeader);
        foreach (var row in WeekRows(cast, null, null, out _)) Console.WriteLine(row);
        return 0;
    }

    const string WeekHeader = "| the envelope | Ada's tea | the window seen by | DS Ellis | taken in | Sheila trusts him | day 7, over | the arrangement | his answer held by Monday noon |\n|---|---|---|---|---|---|---|---|---|";

    /// A WAIT EVERY EVENING (town list 6ci): the same week, with him waiting
    /// every evening from six till ten the next morning. A plain skip (the
    /// hours run with him away, as TownHours.RunTo has them) against the wait
    /// that stops (Waiting.Next before each hour): each thing the week has him
    /// do in those hours must come after a stop that says so, and the week
    /// must come out as it does with no waiting at all.
    static int WeekWaits(CastDay cast)
    {
        var none = WeekRows(cast, null, null, out _);
        var plain = WeekRows(cast, "plain", null, out _);
        Console.WriteLine("the week on paper with a wait every evening from six till ten the next morning (the Saturday night's till Sunday noon)");
        Console.WriteLine("(in a wait he does a thing only once its line has stopped the wait; each wait is read an hour at a time, as the game will)");
        Console.WriteLine();
        Console.WriteLine("a plain skip (the hours run with him away):");
        Console.WriteLine(WeekHeader);
        foreach (var row in plain) Console.WriteLine(row);
        Console.WriteLine($"rows as with no waiting: {none.Where((r, i) => r == plain[i]).Count()} of {none.Count}");
        Console.WriteLine();
        Console.WriteLine("the wait that stops (Waiting.Next), for three sets of walks (to Ada's, the landing, the office, in game minutes):");
        List<string> shownRows = null, firstStops = null;
        foreach (var (tea, landing, office) in new[] { (0, 0, 0), (30, 120, 30), (60, 180, 60) })
        {
            var stops = new List<string>();
            var rows = WeekRows(cast, "stopping", stops, out int missed, tea, landing, office);
            if (shownRows == null || tea == 30) { shownRows = rows; firstStops = stops; }
            Console.WriteLine($"  walks {tea}, {landing}, {office}: things he would have missed for want of a stop {missed}; rows as with no waiting {none.Where((r, i) => r == rows[i]).Count()} of {none.Count}");
        }
        Console.WriteLine();
        Console.WriteLine("with walks 30, 120, 30:");
        Console.WriteLine(WeekHeader);
        foreach (var row in shownRows) Console.WriteLine(row);
        Console.WriteLine("the stops, first row (takes the envelope, sits with Ada, Sheila sees the window):");
        foreach (var st in firstStops) Console.WriteLine("  " + st);
        return 0;
    }

    static List<string> WeekRows(CastDay cast, string waits, List<string> stopsOut, out int missed, int teaLead = 0, int landingLead = 0, int officeLead = 0)
    {
        var rows = new List<string>();
        missed = 0;
        int miss = 0;
        var people = cast.People;
        const string window = "player.window_d1";
        foreach (bool takes in new[] { true, false })
            foreach (bool sits in new[] { true, false })
                // Who sees the window: Sheila, one of Mickey's own, who never goes to the
                // police about him (Jafar's ruling of 1 October); Darren, at the fish
                // front with a body at Tuesday noon, who does (the review of 1 October,
                // M4: behind her window Ada could never see Rita's glass in play);
                // nobody; or no window at all.
                foreach (var seenBy in new[] { "lena", "sam", "nobody", "none" })
                {
                    var graph = new SocialGraph();
                    foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                    var mill = new GossipMill(graph);
                    foreach (var p in people) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
                    var arrangement = new Arrangement(0);
                    var tea = AdasTea.For(0, true);
                    var police = new PoliceFile();
                    var week = new WeeksEnd();
                    Custody custody = null;
                    Aftermath damage = null;
                    string ellis = "never", taken = "no", trust = "never";
                    var talkDays = new HashSet<int>();
                    bool sheSaw = seenBy == "lena", reported = false;
                    int handOverAt = -1;
                    // The wait every evening (WeekWaits): from six till ten the next morning.
                    bool first = takes && sits && seenBy == "lena";
                    var stopWhy = new HashSet<string>();
                    var shownLines = new HashSet<string>();
                    mill.Age(new GameTime(0, 9, 0));
                    // THE TOWN'S TALK IN TIME WITH WHAT HAPPENS (the independent review
                    // of 30 September, A12: the answer at 10:40 was filed before the
                    // hour's rounds ran from 10:00, so hearers held a 10:00 memory of
                    // it): what happens on the hour happens first, the rounds run up to
                    // each later event's minute before it, and the rest at the hour's
                    // end (TownHours.RunTo); his no or the winding down reaches the
                    // landing as each hour turns (Arrangement.TellDue).
                    var talk = new TownHours();
                    for (int abs = 9; abs < 24 * 7 + 12; abs++)
                    {
                        int day = abs / 24, hod = abs % 24;
                        var now = new GameTime(day, hod, 0);
                        // The rounds before minute m of this hour.
                        void Before(int m) => talk.RunTo(mill, cast, now.AddMinutes(m - 1));
                        arrangement.TellDue(mill, now);
                        // Every evening from six till ten the next morning; the
                        // Saturday night's till Sunday noon, over Sheila's ten o'clock.
                        bool InWait(int h) => waits != null && h >= 18 && (h % 24 >= 18 || h % 24 < (h / 24 == week.Day ? 12 : 10));
                        // Waiting through this hour since the last (the wait began in an earlier hour).
                        bool waitingOn = InWait(abs) && InWait(abs - 1);
                        if (InWait(abs) && !InWait(abs - 1)) stopWhy.Clear();
                        if (waits == "stopping" && waitingOn)
                        {
                            int wakeDay = hod >= 18 ? day + 1 : day;
                            var wake = new GameTime(wakeDay, wakeDay == week.Day ? 12 : 10, 0);
                            var beats = new WaitBeats { Asks = arrangement, Tea = tea, Police = police, Mill = mill, Week = week, Custody = custody, Shown = shownLines,
                                                        TeaLead = teaLead, LandingLead = landingLead, OfficeLead = officeLead,
                                                        AtAdas = sits && day == tea.Day && (hod - 1 == 21 || hod - 1 == 22) };
                            // Every stop that falls in the hour just waited through.
                            WaitStop st;
                            while ((st = Waiting.Next(now.AddMinutes(-60), wake, beats)) != null && st.At.CompareTo(now) <= 0)
                            {
                                Waiting.Showed(beats, st);
                                stopWhy.Add(st.Why);
                                if (first && stopsOut != null) stopsOut.Add($"day {st.At.Day + 1} {st.At.Hour:D2}:{st.At.Minute:D2} {st.Why}: \"{st.Line}\"");
                            }
                        }
                        // In a wait's hours he does a thing only once its line has
                        // stopped the wait (a plain skip, never); `count` counts
                        // what was skipped for want of a stop.
                        bool Skip(string why, bool count = true)
                        {
                            if (!waitingOn || waits == null) return false;
                            if (waits == "plain" || !stopWhy.Contains(why)) { if (count && waits == "stopping") miss++; return true; }
                            return false;
                        }
                        if (hod == 6) arrangement.PassedTo(day, mill, now);
                        // The slice's window, at noon on the Tuesday.
                        if (seenBy != "none" && day == 1 && hod == 12)
                        {
                            damage = new Aftermath("ritas", "rita_window", "somebody put Rita's window in", now, Aftermath.DefaultMend(now));
                            if (seenBy != "nobody")
                                mill.Witness(seenBy, new Fact("player", "window_d1", "ritas"), "the new owner put Rita's window in", true, now, 1.0);
                        }
                        damage?.Tick(mill, cast, now);
                        // Each morning after it, whoever saw it goes to the police once they
                        // would: by Jafar's rulings of 1 October the first morning, unless on
                        // his side or one of Mickey's own (Ada's tea on day 3 comes after it).
                        if (!reported && day >= 2 && hod == 9 && seenBy != "nobody" && seenBy != "none"
                            && PoliceFile.WouldReport(mill.Get(seenBy), Offence.Damage, false, window, cast.NeverToPolice(seenBy)))
                        {
                            police.Report(seenBy, window, Offence.Damage, 4, day);
                            reported = true;
                        }
                        if (hod == 9 && day >= 1)
                        {
                            string why = police.EllisComes(mill, day);
                            if (why != null)
                            {
                                if (ellis == "never") ellis = $"day {day + 1}, for {why}";
                                if (why == "talk") police.HearTheStreet(mill, day, t => t.StartsWith("player.window", StringComparison.Ordinal) ? Offence.Damage : Offence.Suspicious, cast, now);
                                PoliceFile.Asked(mill, PoliceFile.WhoSheAsks(mill, cast, now), why, now);
                            }
                        }
                        if (hod == 10 && custody == null && police.ConstableComes(day, now) is string t)
                        {
                            custody = police.TakeIn(t, now, false, false);
                            if (custody != null)
                            {
                                Custody.SeenTaken(mill, cast, "mickeys", now);
                                taken = $"day {day + 1}, {custody.End}";
                            }
                        }
                        bool held = custody != null && custody.Holds(now);
                        // He talks with Sheila at the office each morning he is free
                        // (not on her Sunday: that is her question).
                        if (hod == 10 && !held && day < week.Day && cast.AreaOf(cast.PlaceOf("lena", day, hod)) == "mickeys")
                            talkDays.Add(day);
                        if (trust == "never" && hod == 11 && TrustsNow(mill, talkDays, sheSaw, day)) trust = $"day {day + 1}";
                        if (day == tea.Day && hod == 10) tea.SheSeesHim(now, custody != null && custody.Holds(now));
                        if (hod == 20 && arrangement.AsksOn(day) && !Skip("ron")) arrangement.Delivered(day, mill.Get("rocco"), now);
                        if (sits && day == tea.Day && hod == 21 && !Skip("tea"))
                            for (int m = 0; m < 60; m++) tea.WithHer(new GameTime(day, 21, m));
                        if (sits && day == tea.Day && hod == 22 && !Skip("tea", false))
                            for (int m = 0; m <= 30; m++) tea.WithHer(new GameTime(day, 22, m));
                        if (day == tea.Day && hod == 23) tea.Close(mill.Get(AdasTea.Ada), now);
                        // Not sitting with her, he sets off at 21:45 and is seen going, in
                        // its own hour, after the rounds before it (the second independent
                        // check: it was filed in hour 22's pass, after rounds that ran without it).
                        if (hod == 21 && !sits && takes && day == tea.Day && arrangement.AsksOn(day) && !held && arrangement.WasDelivered(day) && !Skip("landing"))
                        {
                            Before(45);
                            tea.WentToTheLanding(mill, new GameTime(day, 21, 45), forTheAsk: true);
                            handOverAt = abs + 2;
                        }
                        if (hod == 22 && arrangement.AsksOn(day) && !held && arrangement.WasDelivered(day) && !(!sits && takes && day == tea.Day) && !Skip(takes ? "landing" : "ron"))
                        {
                            var answer = takes ? NightAnswer.Did : NightAnswer.Refused;
                            if (answer == NightAnswer.Did && day == tea.Day)
                            {
                                Before(31);
                                tea.WentToTheLanding(mill, new GameTime(day, 22, 31), forTheAsk: true);
                                handOverAt = abs + 2;
                            }
                            else { Before(30); arrangement.Answer(day, answer, mill, new GameTime(day, 22, 30)); }
                        }
                        if (abs == handOverAt && arrangement.AsksOn(tea.Day) && !Skip("landing", false))
                        {
                            Before(45);
                            arrangement.Answer(tea.Day, NightAnswer.Did, mill, new GameTime(day, hod, 45));
                        }
                        // The week's end: her question at half past ten on the Sunday.
                        if (day == week.Day && hod == 10 && week.AsksNow(new GameTime(day, 10, 30), atOffice: true) && !Skip("sheila"))
                        {
                            week.Ask(new GameTime(day, 10, 30), trust != "never");
                            Before(40);
                            week.Give(WeekAnswer.TakeOver, new GameTime(day, 10, 40), mill, cast, arrangement);
                        }
                        week.Close(now, mill, cast);
                        // The rest of the hour's rounds.
                        talk.RunTo(mill, cast, now.AddMinutes(59));
                    }
                    int holdAnswer = mill.Agents.Count(a => a.Rumors.Any(WeeksEnd.IsWeekAnswer));
                    string arr = arrangement.Ended ? $"ended ({arrangement.EndedWhy})" : $"stands ({arrangement.Nights.Count} nights)";
                    string book = week.AskedAt == null ? "not asked" : week.RealBook ? "the real book" : "the day-book";
                    rows.Add($"| {(takes ? "takes it every night" : "tells Ron no")} | {(sits ? "sits with her" : "stands her up")} | {(seenBy == "none" ? "no window" : seenBy == "nobody" ? "nobody" : seenBy)} | {ellis} | {taken} | {trust} | {book} | {arr} | {holdAnswer} of {people.Count} |");
                }
        missed = miss;
        return rows;
    }

    // Her trust as the talk reads it (Trust.Earned), with the week run's two
    // stand-ins for what the game would send: three different days of talk,
    // no deed of his she saw or holds a story of, and not wary.
    static bool TrustsNow(GossipMill mill, HashSet<int> talkDays, bool sheSaw, int today)
    {
        int days = talkDays.Count(d => d <= today);
        if (days < Trust.DaysTalked || sheSaw) return false;
        var she = mill.Get("lena");
        return she == null || StreetVoice.StoryThatShows(she, mill.MinConfidenceToShare) is not Rumor r || !r.Sensitive;
    }

    /// A THREAT TO KEEP QUIET (town list 6cd): Ada saw him at Rita's window on
    /// the Tuesday night; asked about it on the Wednesday at ten, he tells her
    /// to say a word and she'll regret it. She holds that first-hand; who holds
    /// it that evening, the Thursday noon and the Friday noon, and how much
    /// warier the town is of him.
    static int Threat(CastDay cast)
    {
        var graph = new SocialGraph();
        foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
        var mill = new GossipMill(graph);
        foreach (var p in cast.People) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
        int Holders() => mill.Agents.Count(a => a.Rumors.Any(Silence.IsThreat));
        var at = new Dictionary<string, int>();
        mill.Age(new GameTime(2, 0, 0));
        bool filed = false;
        for (int abs = 24 * 2; abs < 24 * 5; abs++)
        {
            int day = abs / 24, hod = abs % 24;
            var now = new GameTime(day, hod, 0);
            if (day == 2 && hod == 10) filed = Silence.FileThreat(mill, "ada", "player.window_d1", now);
            TownRounds.Hour(mill, cast, now);
            if (day == 2 && hod == 21) at["Wednesday evening"] = Holders();
            if (day == 3 && hod == 11) at["Thursday noon"] = Holders();
            if (day == 4 && hod == 11) at["Friday noon"] = Holders();
        }
        Console.WriteLine("a threat: Ada, asked on the Wednesday at ten, is told to say a word and she'll regret it");
        Console.WriteLine($"  filed first-hand for Ada: {(filed ? "yes" : "no")}");
        foreach (var kv in at) Console.WriteLine($"  hold it by {kv.Key}: {kv.Value} of {cast.People.Count}");
        return 0;
    }

    /// THE WEEK'S END (town list 6ca): Sheila waits at the office on the
    /// Sunday, the week's seventh day, from ten; he comes at half past ten and,
    /// asked, tells her plainly he is taking Mickey's business on. Who holds
    /// it that evening, the Monday noon and the Tuesday noon; and the same for
    /// a question he never answered, his refusal from midnight.
    static int WeekEnd(CastDay cast)
    {
        foreach (var answer in new[] { WeekAnswer.TakeOver, WeekAnswer.WontSay, WeekAnswer.WindDown })
        {
            // Mickey's arrangement, kept every night so far (town list 6cc).
            var asks = new Arrangement(0);
            asks.Answer(0, NightAnswer.Did); asks.Answer(2, NightAnswer.Did); asks.Answer(4, NightAnswer.Did);
            var graph = new SocialGraph();
            foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
            var mill = new GossipMill(graph);
            foreach (var p in cast.People) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
            var week = new WeeksEnd();
            int Holders() => mill.Agents.Count(a => a.Rumors.Any(WeeksEnd.IsWeekAnswer));
            var at = new Dictionary<string, int>();
            var heardFirst = new List<string>();
            mill.Age(new GameTime(6, 0, 0));
            for (int abs = 24 * 6; abs < 24 * 9; abs++)
            {
                int day = abs / 24, hod = abs % 24;
                var now = new GameTime(day, hod, 0);
                if (day == week.Day && hod == 10 && week.AsksNow(new GameTime(day, 10, 30), atOffice: true))
                {
                    week.Ask(new GameTime(day, 10, 30), false);
                    if (answer != WeekAnswer.WontSay) week.Give(answer, new GameTime(day, 10, 40), mill, cast, asks);
                    foreach (var g in mill.Agents) if (g.Rumors.Any(WeeksEnd.IsWeekAnswer)) heardFirst.Add(g.Id);
                }
                if (week.Close(now, mill, cast)) foreach (var g in mill.Agents) if (g.Rumors.Any(WeeksEnd.IsWeekAnswer)) heardFirst.Add(g.Id);
                if (hod == 6) asks.PassedTo(day, mill, now);
                TownRounds.Hour(mill, cast, now);
                if (day == 6 && hod == 21) at["Sunday evening"] = Holders();
                if (day == 7 && hod == 11) at["Monday noon"] = Holders();
                if (day == 8 && hod == 11) at["Tuesday noon"] = Holders();
            }
            Console.WriteLine(answer == WeekAnswer.TakeOver
                ? "the week's end: Sheila asks him at the office on the Sunday at 10:30; he tells her plainly he is taking it on"
                : answer == WeekAnswer.WindDown
                ? "the week's end: Sheila asks him at the office on the Sunday at 10:30; he tells her plainly he is winding it down"
                : "the week's end: Sheila asks him at the office on the Sunday at 10:30; he never answers, his refusal from midnight");
            Console.WriteLine($"  Mickey's arrangement: {(asks.Ended ? "ended, " + asks.EndedWhy + ", that night; no envelope on the Sunday" : "stands; Ron brings the envelope on the Sunday night")}");
            Console.WriteLine($"  told first-hand: {string.Join(", ", heardFirst)}");
            foreach (var kv in at) Console.WriteLine($"  hold it by {kv.Key}: {kv.Value} of {cast.People.Count}");
        }
        return 0;
    }

    /// WHAT AN ARREST DOES (town list 6bp): Rita's window put in at half past
    /// eleven on a Tuesday night, seen plainly by Ada from her window when she
    /// has cooled on him (loyalty 0.35, as after he stood her up); she goes to
    /// the police in the morning if WouldReport says so; a constable calls the
    /// next morning (ConstableComes) and takes him from the office at ten
    /// (Custody.Take, not owning up); whoever is at Mickey's then sees it
    /// (SeenTaken), and the gossip ticks on the cast's routines. When he is out,
    /// what comes of it, and how many hold it by that evening and the next noon.
    static int TakenIn(CastDay cast)
    {
        var graph = new SocialGraph();
        foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
        var mill = new GossipMill(graph);
        foreach (var p in cast.People) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
        var ada = mill.Get("ada");
        ada.Loyalty = 0.35;
        const string topic = "player.window_d1";
        var police = new PoliceFile();
        bool reports = PoliceFile.WouldReport(ada, Offence.Damage, false, topic, cast.NeverToPolice("ada"));
        if (reports) police.Report("ada", topic, Offence.Damage, 4, 2);
        Custody custody = null;
        var saw = new List<string>();
        int Holders() => mill.Agents.Count(a => a.Rumors.Any(Custody.IsTaken));
        var at = new Dictionary<string, int>();
        mill.Age(new GameTime(2, 0, 0));
        for (int abs = 48; abs < 24 * 5; abs++)
        {
            int day = abs / 24, hod = abs % 24;
            var now = new GameTime(day, hod, 0);
            if (hod == 10 && custody == null && police.ConstableComes(day, now) is string t)
            {
                custody = police.TakeIn(t, now, false, false);
                saw = Custody.SeenTaken(mill, cast, "mickeys", now);
            }
            TownRounds.Hour(mill, cast, now);
            if (custody != null && day == custody.TakenAt.Day && hod == 21) at["that evening"] = Holders();
            if (custody != null && day == custody.TakenAt.Day + 1 && hod == 11) at["the next noon"] = Holders();
        }
        Console.WriteLine("taken in: Rita's window, Tuesday 23:30, seen plainly by Ada, cooled on him");
        Console.WriteLine($"  Ada goes to the police: {(reports ? "yes, a statement naming him, Wednesday" : "no")}");
        if (custody == null) { Console.WriteLine("  nobody comes for him"); return 0; }
        Console.WriteLine($"  a constable takes him from the office day {custody.TakenAt.Day + 1} at {custody.TakenAt.Hour:00}:00; out at {custody.OutAt.Hour:00}:{custody.OutAt.Minute:00}, {custody.End}, to answer on day {custody.AnswerDay + 1}");
        Console.WriteLine($"  seen taken by {saw.Count}: {string.Join(", ", saw)}");
        foreach (var kv in at) Console.WriteLine($"  hold it by {kv.Key}: {kv.Value} of {cast.People.Count}");
        return 0;
    }

    /// THE DAMAGE FOUND IN THE MORNING (town list 6br): Rita's window put in at
    /// half past eleven on a Tuesday night, seen by nobody, mended by the
    /// glazier at four on the Wednesday; each hour whoever comes into Rita's
    /// finds it (Aftermath.Tick), and the gossip ticks on the cast's routines.
    /// Who finds it and when, and how many hold it at noon and at six on the
    /// Wednesday and at noon on the Thursday; and that it raised nobody's
    /// suspicion.
    static int FoundInTheMorning(CastDay cast)
    {
        var graph = new SocialGraph();
        foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
        var mill = new GossipMill(graph);
        foreach (var p in cast.People) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
        var broke = new GameTime(1, 23, 30);
        var mended = new GameTime(2, 16, 0);
        const string said = "somebody put Rita's window in";
        var damage = new Aftermath("ritas", "rita_window", said, broke, mended);
        double suspicionBefore = mill.Agents.Sum(a => a.Suspicion.Value);
        var finders = new List<string>();
        int Holders() => mill.Agents.Count(a => a.Rumors.Any(r => r.Content != null && r.Content.Subject == TownNews.Subject && r.Content.Predicate == "rita_window"));
        var at = new Dictionary<string, int>();
        mill.Age(new GameTime(2, 0, 0));
        for (int abs = 24; abs < 24 * 4; abs++)
        {
            int day = abs / 24, hod = abs % 24;
            var now = new GameTime(day, hod, 0);
            var nowFound = damage.Tick(mill, cast, now);
            foreach (var (who, when) in nowFound) finders.Add($"{who} {when.Hour:00}:00");
            TownRounds.Hour(mill, cast, now);
            if (day == 2 && hod == 11) at["Wednesday noon"] = Holders();
            if (day == 2 && hod == 17) at["Wednesday six"] = Holders();
            if (day == 3 && hod == 11) at["Thursday noon"] = Holders();
        }
        double suspicionAfter = mill.Agents.Sum(a => a.Suspicion.Value);
        Console.WriteLine($"found in the morning: Rita's window, put in Tuesday 23:30 unseen, mended Wednesday 16:00");
        Console.WriteLine($"  found by {finders.Count}: {string.Join(", ", finders)}");
        foreach (var kv in at) Console.WriteLine($"  hold it by {kv.Key}: {kv.Value} of {cast.People.Count}");
        Console.WriteLine($"  suspicion of him, summed over the cast: {suspicionBefore:0.###} before, {suspicionAfter:0.###} after");
        return 0;
    }

    /// THE FIRST HOUR ON PAPER (town list 6bk): the week the first hour spans,
    /// played through the Core's own pieces together, for each of Tom's choices:
    /// the outfit's asks every other night from night one while the arrangement
    /// stands (Arrangement: the envelope handed over, or Ron told no, at half
    /// past ten on an ordinary night; a night he stays away counted by
    /// PassedTo at dawn, six, as the handover has the game do it); Ada's tea on
    /// day 3 (AdasTea: she asks him at ten that morning; sitting with her he is
    /// there from nine to half past ten, then, taking the envelope, is seen
    /// leaving and reaches the landing near one after the two hours' walk);
    /// the gossip ticking hour by hour on the cast's routines; each morning at
    /// nine whether DS Ellis comes (PoliceFile, on the street's talk), and if
    /// she does, whom she asks (PoliceFile.Asked, town list 6bq); and what
    /// the five he met on day 1 show or say to his face as he passes each of
    /// them once an hour (StreetVoice.RegardFor, as --meridian: a best case).
    /// No other sighting is filed (the envelope's walk and the tea's are seen
    /// only as the pieces have it), so this is the pieces' own reach, not the
    /// perception's. Alison's question is not in it: the fire is not written.
    static int FirstHourOnPaper(CastDay cast, double rate)
    {
        var people = cast.People;
        var met = new[] { "lena", "rocco", "sam", "ada", "june" };
        int lastHour = (int)Math.Round(60 * rate);   // minute sixty, in game hours from 09:00 on day 0
        int halfHour = (int)Math.Round(30 * rate);
        double MinuteOf(int gameHour) => gameHour / rate;
        Console.WriteLine($"first hour on paper: met {string.Join(",", met)}; play from 09:00 on day 0 to minute 60 (hour {lastHour}) at {rate.ToString(Inv)} game minutes a real second");
        Console.WriteLine("| the envelope | Ada's tea | first shown to him | first said to his face | by minute 30 | the arrangement by minute 60 | Ada | Ellis | word of her by minute 60 |");
        Console.WriteLine("|---|---|---|---|---|---|---|---|---|");
        var policies = new (string name, NightAnswer first, NightAnswer later)[]
        {
            ("takes it every night", NightAnswer.Did, NightAnswer.Did),
            ("takes it once, then stays away", NightAnswer.Did, NightAnswer.NoShow),
            ("tells Ron no", NightAnswer.Refused, NightAnswer.Refused),
            ("stays away", NightAnswer.NoShow, NightAnswer.NoShow),
        };
        foreach (var (name, first, later) in policies)
            foreach (bool sits in new[] { true, false })
            {
                var graph = new SocialGraph();
                foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                var mill = new GossipMill(graph);
                foreach (var p in people) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
                var arrangement = new Arrangement(0);
                var tea = AdasTea.For(0, true);
                var police = new PoliceFile();
                var remarks = new RemarkLedger();
                string firstShown = null, firstFaced = null, ellis = "does not come", byThirty = null, policeFaced = null;
                int askedBy = 0;
                int handOverAt = -1;   // play hour at which a delayed envelope is handed over
                mill.Age(new GameTime(0, 9, 0));
                for (int playHour = 0; playHour < lastHour; playHour++)
                {
                    int abs = 9 + playHour, day = abs / 24, hod = abs % 24;
                    var now = new GameTime(day, hod, 0);
                    if (hod == 6) arrangement.PassedTo(day, mill, now);
                    if (hod == 9 && day >= 1)
                    {
                        string why = police.EllisComes(mill, day);
                        if (why != null && ellis == "does not come") ellis = $"day {day + 1} (minute {MinuteOf(playHour):0}), for {why}";
                        if (why != null) askedBy += PoliceFile.Asked(mill, PoliceFile.WhoSheAsks(mill, cast, now), why, now);
                    }
                    if (day == tea.Day && hod == 10) tea.SheSeesHim(now);
                    // Ron brings the ask after dark, at the office, before the tea.
                    if (hod == 20 && arrangement.AsksOn(day)) arrangement.Delivered(day, mill.Get("rocco"), now);
                    if (sits && day == tea.Day && hod == 21)
                        for (int m = 0; m < 60; m++) tea.WithHer(new GameTime(day, 21, m));
                    if (sits && day == tea.Day && hod == 22)
                        for (int m = 0; m <= 30; m++) tea.WithHer(new GameTime(day, 22, m));
                    if (day == tea.Day && hod == 23) tea.Close(mill.Get(AdasTea.Ada), now);
                    for (int minute = 0; minute < 60; minute += 6)
                        mill.Tick(new GameTime(day, hod, minute), (a, b) => cast.Together(a, b, day, hod));
                    // The ask, after the hour's talk: on an ordinary night at half
                    // past ten; on the tea's night, taking it after his tea, he is seen
                    // leaving at 22:31 and hands it over at 00:45, after the walk.
                    if (hod == 22 && arrangement.AsksOn(day))
                    {
                        var answer = arrangement.Nights.Count == 0 ? first : later;
                        if (answer == NightAnswer.Did && day == tea.Day)
                        {
                            tea.WentToTheLanding(mill, new GameTime(day, sits ? 22 : 21, sits ? 31 : 45), forTheAsk: true);
                            handOverAt = playHour + (sits ? 2 : 1);
                        }
                        else if (answer != NightAnswer.NoShow) arrangement.Answer(day, answer, mill, new GameTime(day, 22, 30));
                    }
                    if (playHour == handOverAt && arrangement.AsksOn(tea.Day))
                        arrangement.Answer(tea.Day, NightAnswer.Did, mill, new GameTime(day, hod, 45));
                    mill.Age(new GameTime((abs + 1) / 24, (abs + 1) % 24, 0));
                    foreach (var p in met)
                    {
                        var g = mill.Get(p);
                        if (g == null || cast.Where(p, day, hod) == null) continue;
                        bool companion = people.Any(o => o != p && cast.Together(p, o, day, hod));
                        var rg = StreetVoice.RegardFor(g, mill.MinConfidenceToShare, false, remarks, Acquaintance.Known, companion);
                        if (rg.Knowing == Knowing.Nothing || !rg.KnowsItIsHim) continue;
                        firstShown ??= $"minute {MinuteOf(playHour + 1):0}, {p}";
                        if (rg.Speaks && !rg.Faint && (firstFaced == null || (policeFaced == null && PoliceFile.IsAsking(rg.Story))) && rg.Story != null)
                        {
                            var line = StreetVoice.Recognition(g, rg.Story, rg.Stance, playHour, remarks);
                            string said = $"minute {MinuteOf(playHour + 1):0}, {p}: \"{line?.Text}\"";
                            firstFaced ??= said;
                            if (PoliceFile.IsAsking(rg.Story)) policeFaced ??= said;
                        }
                        if (rg.Speaks && rg.Story != null)
                        {
                            if (rg.Faint) remarks.RecordFaint(p, rg.Story, heard: true);
                            else remarks.Record(p, rg.Story, rg.Stance, heard: true);
                        }
                    }
                    if (playHour + 1 == halfHour)
                        byThirty = (firstFaced != null ? "said to his face" : firstShown != null ? "shown, not said" : "nothing shown")
                                   + $"; loudness {PoliceFile.Loudness(mill)}";
                }
                var adaG = mill.Get(AdasTea.Ada);
                string adaAfter = $"{tea.State}, regard {adaG.Loyalty:0.00}" + (tea.SeenGoing ? ", saw him go" : "");
                string arr = arrangement.Ended ? $"ended ({arrangement.EndedWhy}, {arrangement.Nights.Count} nights)" : $"stands ({arrangement.Nights.Count} nights)";
                int holdWord = mill.Agents.Count(a => a.Rumors.Any(PoliceFile.IsAsking));
                string word = askedBy == 0 ? "-" : $"she asked {askedBy}, {holdWord} hold it; " + (policeFaced ?? "not said to his face");
                Console.WriteLine($"| {name} | {(sits ? "sits with her" : "stands her up")} | {firstShown ?? "never"} | {firstFaced ?? "never"} | {byThirty} | {arr} | {adaAfter} | {ellis} | {word} |");
            }
        return 0;
    }

    /// HOW LOUD THE STREET GETS (town list 6ar): every night-one sighting by
    /// each of the cast out between 22:00 and 04:00, at a first sight of 0.6
    /// and of 1.0, and PoliceFile.Loudness (people of his day world passing the
    /// talk round, a retelling each) each morning at nine of days 1 to 5, the
    /// days the first hour spans; for choosing PoliceFile.LoudAt so that DS
    /// Ellis comes on days 4 and 5 "if the street has got loud about him".
    static int Loud(CastDay cast, bool secondNight = false)
    {
        var people = cast.People;
        Console.WriteLine($"loud: night-one sightings, loudness at 09:00 each morning, {people.Count} people");
        foreach (double firstSight in new[] { 0.6, 1.0 })
        {
            var byDay = new List<int>[6];
            for (int d = 1; d <= 5; d++) byDay[d] = new List<int>();
            var byWitness = new Dictionary<string, int[]>();
            var witnesses = new List<string>();
            var pairs = new Dictionary<string, SortedSet<string>>();
            int runs = 0;
            for (int hour = 22; hour <= 28; hour++)
            {
                int day = hour / 24, hod = hour % 24;
                foreach (var witness in people)
                {
                    if (cast.Where(witness, day, hod) == null) continue;
                    runs++;
                    var graph = new SocialGraph();
                    foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                    var mill = new GossipMill(graph);
                    foreach (var p in people) mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(p)));
                    var start = new GameTime(day, hod, 0);
                    mill.Age(start);
                    mill.Witness(witness, new Fact("player", "night_walk_d0", "seen"), "the new owner was about the yard after midnight", true, start, firstSight);
                    witnesses.Add(witness);
                    // With --second-night, the night of day index 2 (the second
                    // ask) is seen too, by the next of the cast out at that hour.
                    string second = null;
                    if (secondNight)
                    {
                        int i0 = people.ToList().IndexOf(witness);
                        for (int k = 1; k < people.Count && second == null; k++)
                        {
                            var c = people[(i0 + k) % people.Count];
                            if (c != witness && cast.Where(c, day + 2, hod) != null) second = c;
                        }
                    }
                    int secondAt = hour + 48;
                    if (second != null)
                    {
                        if (!pairs.ContainsKey(witness)) pairs[witness] = new SortedSet<string>();
                        pairs[witness].Add(second + "@" + (hour % 24));
                    }
                    int at = hour + 1;
                    for (int morning = 1; morning <= 5; morning++)
                    {
                        int until = morning * 24 + 9;
                        for (; at <= until; at++)
                        {
                            int dd = at / 24, hh = at % 24;
                            if (second != null && at == secondAt)
                                mill.Witness(second, new Fact("player", "night_walk_d2", "seen"), "the new owner was about the quay late", true, new GameTime(dd, hh, 0), firstSight);
                            for (int minute = 0; minute < 60; minute += 6)
                                mill.Tick(new GameTime(dd, hh, minute), (x, y) => cast.Together(x, y, dd, hh));
                            mill.Age(new GameTime(dd, hh, 59));
                        }
                        int loudNow = PoliceFile.Loudness(mill);
                        byDay[morning].Add(loudNow);
                        if (!byWitness.ContainsKey(witness)) byWitness[witness] = new int[6];
                        byWitness[witness][morning] = Math.Max(byWitness[witness][morning], loudNow);
                    }
                }
            }
            Console.WriteLine($"FIRST SIGHT {firstSight.ToString("0.0", Inv)}: runs={runs}, by {byWitness.Count} different first witnesses");
            foreach (var kv in byWitness.OrderBy(k => k.Key))
                Console.WriteLine($"  first witness {kv.Key}: loudness at nine on days 2 to 6, at its loudest hour: {string.Join(" ", kv.Value.Skip(1))}"
                                  + (secondNight && pairs.TryGetValue(kv.Key, out var two) ? $" (second night seen by {string.Join(", ", two)})" : ""));
            for (int d = 1; d <= 5; d++)
            {
                var v = byDay[d];
                v.Sort();
                string at = string.Join(" ", new[] { 2, 3, 4, 6, 8 }.Select(k => $">={k}:{v.Count(x => x >= k) * 100 / Math.Max(1, v.Count)}%"));
                Console.WriteLine($"  morning of day {d + 1} (day index {d}): median {v[v.Count / 2]}, max {v[v.Count - 1]}; {at}");
            }
        }
        return 0;
    }

    /// MERIDIAN CONDITION 2, THE SIMULATION'S SIDE (town list 6l): "within those
    /// 30 minutes the world visibly knows them at least once". Play starts at
    /// nine on day one; he has met only `met` (the first hour's day one); he is
    /// seen on night one (22:00 to 04:00) by whoever of the cast is out on the
    /// street then. Counted by minute thirty (hour 60 of play): whether anyone he
    /// met shows it as he passes (the longer look, or a word), and whether one of
    /// them says it to his face. Only those he met can tell it is him; everyone
    /// else is a stranger to him, as canon has it. He passes everybody out on the
    /// street once an hour, as in the rest of this tool: generous.
    /// `teller` (town list 6z): instead of every sighting of night one, the one
    /// telling of his night by this cast member at `toldAt` o'clock on night
    /// one, for certain: the outfit's man after the landing.
    static int Meridian(CastDay cast, string[] met, double rate, string teller = null, int toldAt = 22, string answer = "did")
    {
        var people = cast.People;
        NightAnswer what = answer == "refused" ? NightAnswer.Refused : answer == "noshow" ? NightAnswer.NoShow : NightAnswer.Did;
        if (teller != null && (!people.Contains(teller) || (toldAt < 22 && toldAt > 4) || toldAt < 0 || toldAt > 23 || Arrangement.Value(what) != answer))
        {
            Console.Error.WriteLine($"meridian: --teller must be a cast id ({teller}), --told-at an hour of night one, 22 to 4 ({toldAt}), --answer did, refused or noshow ({answer})");
            return 2;
        }
        var metSet = new HashSet<string>(met.Select(m => m.Trim()).Where(m => m.Length > 0));
        // THE CLOCK (town list 6x): game minutes a real second. At 2 a game hour
        // is half a real minute and minute thirty is game hour 60; at 1, hour 30.
        int lastHour = (int)Math.Round(30 * rate);
        double MinuteOf(int gameHour) => gameHour / rate;
        Console.WriteLine($"meridian met={string.Join(",", metSet)} of {people.Count}; night one, play from 09:00, counted to minute 30 (hour {lastHour}) at {rate.ToString(Inv)} game minutes a real second");
        foreach (double firstSight in teller != null ? new[] { 1.0 } : new[] { 0.6, 1.0 })
        {
            int runs = 0, shown = 0, faced = 0;
            var firstShown = new List<int>();
            var firstHeld = new List<int>();
            for (int sightHour = 13; sightHour <= 19; sightHour++)
            {
                int sHour = (9 + sightHour) % 24;
                int sAbsDay = (9 + sightHour) / 24;
                if (teller != null && sHour != toldAt) continue;
                foreach (var witness in people)
                {
                    if (teller != null && witness != teller) continue;
                    // A teller knows it wherever they are.
                    if (teller == null && cast.Where(witness, sAbsDay, sHour) == null) continue;   // not out on the street to see it
                    runs++;
                    var graph = new SocialGraph();
                    foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                    var mill = new GossipMill(graph);
                    foreach (var p in people)
                        mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker()));
                    var start = new GameTime(sAbsDay, sHour, 0);
                    mill.Age(start);
                    // With a teller, the arrangement's own story of night one, as
                    // Arrangement.Answer files it (town list 6z).
                    if (teller != null)
                        mill.Witness(witness, new Fact("player", "outfit_d0", Arrangement.Value(what)), Arrangement.Said(what), what == NightAnswer.Did, start, 1.0);
                    else
                        mill.Witness(witness, new Fact("player", "night_walk_d1", "seen"),
                            "the new owner was about the yard after midnight", sensitive: true, start, confidence: firstSight);
                    var remarks = new RemarkLedger();
                    bool wasShown = false, wasFaced = false, wasHeld = false;
                    for (int playHour = sightHour; playHour < lastHour; playHour++)
                    {
                        int abs = 9 + playHour, day = abs / 24, hourOfDay = abs % 24;
                        for (int minute = 0; minute < 60; minute += 6)
                            mill.Tick(new GameTime(day, hourOfDay, minute), (a, b) => cast.Together(a, b, day, hourOfDay));
                        mill.Age(new GameTime((abs + 1) / 24, (abs + 1) % 24, 0));
                        foreach (var p in metSet)
                        {
                            var g = mill.Get(p);
                            if (g == null) continue;
                            if (!wasHeld && g.Rumors.Any(r => r.Content.Subject == "player")) { wasHeld = true; firstHeld.Add(playHour + 1); }
                            if (cast.Where(p, day, hourOfDay) == null) continue;
                            bool companion = people.Any(o => o != p && cast.Together(p, o, day, hourOfDay));
                            var rg = StreetVoice.RegardFor(g, mill.MinConfidenceToShare, false, remarks, Acquaintance.Known, companion);
                            if (rg.Knowing != Knowing.Nothing && rg.KnowsItIsHim)
                            {
                                if (!wasShown) firstShown.Add(playHour + 1);
                                wasShown = true;
                                if (rg.Speaks && !rg.Faint) wasFaced = true;
                                if (rg.Speaks && rg.Story != null)
                                {
                                    if (rg.Faint) remarks.RecordFaint(p, rg.Story, heard: true);
                                    else remarks.Record(p, rg.Story, rg.Stance, heard: true);
                                }
                            }
                        }
                    }
                    if (wasShown) shown++;
                    if (wasFaced) faced++;
                }
            }
            firstShown.Sort();
            firstHeld.Sort();
            Console.WriteLine($"  someone he met first holds it (before it can show), minutes: {string.Join(" ", firstHeld.Select(h => MinuteOf(h).ToString("0", Inv)))}");
            string when = firstShown.Count > 0 ? $"; when it shows, median minute {MinuteOf(firstShown[firstShown.Count / 2]):0} (all: {string.Join(" ", firstShown.Select(h => MinuteOf(h).ToString("0", Inv)))})" : "";
            Console.WriteLine($"FIRST SIGHT {firstSight.ToString("0.00", Inv)}: runs={runs} (each of the cast out on the street at each hour of night one)");
            Console.WriteLine($"  by minute 30, someone he met shows it: {shown}/{runs} ({shown * 100.0 / Math.Max(1, runs):0}%); says it to his face: {faced}/{runs} ({faced * 100.0 / Math.Max(1, runs):0}%){when}");
        }
        return 0;
    }

    /// TWO HOURS WITHOUT REPETITION, THE CORE'S SIDE (town list 6o; ROADMAP stage
    /// 6, "no detectable line repetition in a two-hour session"). Everything the
    /// street says in his hearing over two hours of play, 240 game hours from
    /// nine on day one (a game hour is thirty real seconds), bank by bank: the
    /// words picked by the seed alone, and with the ledger of what he has heard.
    ///
    /// Each game hour he stands at one of the street's places: WALKING, the
    /// places in turn; BUSIEST, wherever most of the cast are out. Neither is a
    /// ceiling: the game counts crowd walkers too, and a street crowded enough
    /// talks at the floor, where a fourteen-line bank comes back after fourteen
    /// floors (printed as the worst case). What he hears is the C# game layer's
    /// rules (GossipDirector), with the cast's places for positions:
    ///   - the neighbours' own talk: the game's timer, one exchange every
    ///     StreetVoice.AmbientEverySeconds(heat, near) seconds, near meaning
    ///     within 14 m of him; the timer waits while fewer than two are near and
    ///     fires as soon as two are, and when it fires with no two of them within
    ///     7 m of each other it is spent all the same; the economy even, nobody
    ///     hurt or feuding;
    ///   - gossip passing: every telling between two people both within 6 m of
    ///     him (the game's earshot);
    ///   - the story shown: anybody within 7 m who knows him and speaks
    ///     (RegardFor; he has met them all, a ceiling, as the first-hour
    ///     measure), once a game hour each (the game's cooldown is 45 s, so
    ///     this is a little generous).
    /// One story, a plain sighting on night one (22:00 to 04:00), by each of the cast out then.
    /// The seeds alone are the C# game layer's (day and hour); the ledger is one
    /// RemarkLedger for the whole two hours, told only of what he heard. With
    /// --clear-every N, the neighbours' words he can make out come no oftener
    /// than every N seconds instead of the Core's floor, to compare (the street's murmur is not counted).
    static int TwoHours(CastDay cast, string castJson, double clearEvery, double deedAtMinute = -1, TownNews newsFile = null)
    {
        // The named characters: those the cast file gives a name.
        var named = new HashSet<string>();
        using (var doc = System.Text.Json.JsonDocument.Parse(castJson))
            foreach (var person in doc.RootElement.GetProperty("people").EnumerateArray())
                if (person.TryGetProperty("name", out _) && person.TryGetProperty("id", out var pid)) named.Add(pid.GetString());
        var people = cast.People;
        var placesObj = MiniJson.AsObject(MiniJson.AsObject(MiniJson.Deserialize(castJson))["places"]);
        var spots = new List<(string name, double x, double z)>();
        foreach (var kv in placesObj)
        {
            var o = MiniJson.AsObject(kv.Value);
            spots.Add((kv.Key, Convert.ToDouble(o["x_m"], Inv), Convert.ToDouble(o["z_m"], Inv)));
        }
        const double NearM = 14.0, EarshotM = 6.0, RemarkM = 7.0, PairM = 7.0, SecondsPerHour = 30.0;
        const int Hours = 240;
        Console.WriteLine($"twoHours cast people={people.Count} places={spots.Count}; play from 09:00 day 0 for {Hours} game hours ({Hours * SecondsPerHour / 3600:0.0} real hours); near={NearM} m; neighbours' words no oftener than every {clearEvery.ToString(Inv)} s; worst case, a crowd always near him: a fourteen-line bank back after {14 * clearEvery / 60:0.0} min");

        foreach (string mode in new[] { "walking", "busiest" })
        {
            // bank -> per run: (seconds, text) heard, two ways
            var seedHeard = new Dictionary<string, List<List<(double t, string text)>>>();
            var freshHeard = new Dictionary<string, List<List<(double t, string text)>>>();
            // BY NAMED SPEAKER (U2, 30 September): how many lines each named
            // character says in his hearing, bank by bank, with the ledger; what
            // sizes each one's own lines.
            var spokenBy = new Dictionary<(string who, string bank), int>();
            var mostBy = new Dictionary<string, int>();
            int runs = 0;
            foreach (int sightAbs in new[] { 22, 23, 24, 25, 26, 27, 28 })
            foreach (var witness in people)
            {
                if (cast.Where(witness, sightAbs / 24, sightAbs % 24) == null) continue;
                runs++;
                var graph = new SocialGraph();
                foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                var mill = new GossipMill(graph);
                foreach (var p in people)
                    mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker()));
                var seen = new GameTime(sightAbs / 24, sightAbs % 24, 0);
                mill.Age(new GameTime(0, 9, 0));
                var ledger = new RemarkLedger();
                var remarks = new RemarkLedger();
                var runSeed = new Dictionary<string, List<(double, string)>>();
                var runFresh = new Dictionary<string, List<(double, string)>>();
                var runBy = new Dictionary<string, int>();
                void Said(SpokenLine l)
                {
                    if (l == null || l.SpeakerId == null || !named.Contains(l.SpeakerId)) return;
                    var k = (l.SpeakerId, l.Bank ?? "?");
                    spokenBy[k] = (spokenBy.TryGetValue(k, out var c) ? c : 0) + 1;
                    runBy[l.SpeakerId] = (runBy.TryGetValue(l.SpeakerId, out var r) ? r : 0) + 1;
                }
                void Note(Dictionary<string, List<(double, string)>> into, string bank, double t, string text)
                {
                    if (bank == null || string.IsNullOrEmpty(text)) return;
                    if (!into.TryGetValue(bank, out var l)) into[bank] = l = new List<(double, string)>();
                    l.Add((t, text));
                }
                double nextTalk = 0;
                int ambientCount = 0;
                // A WINDOW GOES IN where he stands, at --deed-at real minutes (town
                // list 6an): what the neighbours in earshot say after it.
                double deedT = deedAtMinute < 0 ? -1 : deedAtMinute * 60.0;
                bool deedHeard = false;
                // THE TOWN'S OWN NEWS (town list 6aq): filed as its hour comes.
                TownNews news = null;
                if (newsFile != null) { news = new TownNews(); news.Stories.AddRange(newsFile.Stories); }
                for (int playHour = 0; playHour < Hours; playHour++)
                {
                    int abs = 9 + playHour, day = abs / 24, hourOfDay = abs % 24;
                    if (abs == sightAbs) mill.Witness(witness, new Fact("player", "night_walk_d1", "seen"),
                        "the new owner was about the yard late at night", sensitive: true, seen, confidence: 1.0);
                    news?.Seed(mill, cast, new GameTime(day, hourOfDay, 0));
                    var outNow = people.Where(p => cast.Where(p, day, hourOfDay) != null).ToList();
                    (string name, double x, double z) at;
                    if (mode == "walking") at = spots[playHour % spots.Count];
                    else at = spots.OrderByDescending(s => outNow.Count(p => Dist(cast.Where(p, day, hourOfDay).Value, s) <= NearM)).First();
                    var near = outNow.Where(p => Dist(cast.Where(p, day, hourOfDay).Value, at) <= NearM).ToList();
                    double DistTo(string p) => Dist(cast.Where(p, day, hourOfDay).Value, at);
                    var earshot = new HashSet<string>(near.Where(p => DistTo(p) <= EarshotM));
                    double hourStart = playHour * SecondsPerHour;

                    // Gossip passing in his hearing.
                    for (int minute = 0; minute < 60; minute += 6)
                    {
                        var events = mill.Tick(new GameTime(day, hourOfDay, minute), (a, b) => cast.Together(a, b, day, hourOfDay));
                        foreach (var ev in events)
                        {
                            if (ev.Rumor == null || (ev.Rumor.Content.Subject != "player" && (news == null || ev.Rumor.Content.Subject != TownNews.Subject))) continue;
                            if (!earshot.Contains(ev.FromId) || !earshot.Contains(ev.ToId)) continue;
                            double t = hourStart + minute / 60.0 * SecondsPerHour;
                            var from = mill.Get(ev.FromId); var to = mill.Get(ev.ToId);
                            foreach (var l in StreetVoice.Exchange(ev.Rumor, from, to, day * 31 + hourOfDay)) Note(runSeed, l.Bank, t, l.Text);
                            foreach (var l in StreetVoice.Exchange(ev.Rumor, from, to, day * 31 + hourOfDay, ledger)) { Note(runFresh, l.Bank, t, l.Text); ledger.Heard(l); Said(l); }
                        }
                    }
                    mill.Age(new GameTime((abs + 1) / 24, (abs + 1) % 24, 0));

                    // The story shown, by those near him.
                    foreach (var p in near)
                    {
                        if (DistTo(p) > RemarkM) continue;
                        var g = mill.Get(p);
                        bool companion = people.Any(o => o != p && cast.Together(p, o, day, hourOfDay));
                        var rg = StreetVoice.RegardFor(g, mill.MinConfidenceToShare, false, remarks, Acquaintance.Known, companion);
                        if (!rg.Speaks || rg.Story == null) continue;
                        int seed = (int)(Fnv(p + "@" + abs) & 0x7fffffff);
                        var bySeed = rg.Faint ? StreetVoice.FaintRemark(g, rg.Story, seed) : StreetVoice.Recognition(g, rg.Story, rg.Stance, seed);
                        var byFresh = rg.Faint ? StreetVoice.FaintRemark(g, rg.Story, seed, ledger) : StreetVoice.Recognition(g, rg.Story, rg.Stance, seed, ledger);
                        if (bySeed == null || byFresh == null) continue;
                        Note(runSeed, bySeed.Bank, hourStart, bySeed.Text);
                        Note(runFresh, byFresh.Bank, hourStart, byFresh.Text);
                        ledger.Heard(byFresh);
                        Said(byFresh);
                        if (rg.Faint) remarks.RecordFaint(p, rg.Story, heard: true);
                        else remarks.Record(p, rg.Story, rg.Stance, heard: true);
                    }

                    // The neighbours' own talk, at the game's own pace.
                    var pairs = new List<(string a, string b)>();
                    for (int i = 0; i < near.Count; i++)
                        for (int j = i + 1; j < near.Count; j++)
                        {
                            var pj = cast.Where(near[j], day, hourOfDay).Value;
                            if (Dist(cast.Where(near[i], day, hourOfDay).Value, (near[j], pj.x, pj.z)) < PairM) pairs.Add((near[i], near[j]));
                        }
                    double every = StreetVoice.AmbientEverySeconds(mill.DayCircleHeat(), near.Count, clearEvery);
                    if (every > 1e8) continue;   // fewer than two near: the game's timer waits
                    double hourEnd = hourStart + SecondsPerHour;
                    // The first words after the deed come as the hush lifts.
                    if (deedT >= 0 && !deedHeard && deedT < hourEnd && nextTalk > deedT + StreetVoice.JustNowSpeakAfterSeconds)
                        nextTalk = Math.Max(hourStart, deedT + StreetVoice.JustNowSpeakAfterSeconds);
                    while (nextTalk < hourEnd)
                    {
                        double t = Math.Max(nextTalk, hourStart);
                        if (deedT >= 0 && t >= deedT) deedHeard = true;
                        nextTalk = t + every;
                        if (pairs.Count == 0) continue;   // spent, with nobody to pair
                        var (a, b) = pairs[ambientCount++ % pairs.Count];
                        var now = new GameTime(day, hourOfDay, 0);
                        int seed = day * 17 + hourOfDay * 3 + near.Count;
                        string justNow = deedT >= 0 && t >= deedT ? "glass" : null;
                        double since = deedT >= 0 && t >= deedT ? t - deedT : -1;
                        foreach (var l in StreetVoice.Ambient(mill.Get(a), mill.Get(b), now, 0.5, 1.0, false, false, seed, null, justNow, since)) Note(runSeed, l.Bank, t, l.Text);
                        foreach (var l in StreetVoice.Ambient(mill.Get(a), mill.Get(b), now, 0.5, 1.0, false, false, seed, ledger, justNow, since)) { Note(runFresh, l.Bank, t, l.Text); ledger.Heard(l); Said(l); }
                    }
                }
                foreach (var kv in runSeed) { if (!seedHeard.TryGetValue(kv.Key, out var l)) seedHeard[kv.Key] = l = new List<List<(double, string)>>(); l.Add(kv.Value); }
                foreach (var kv in runFresh) { if (!freshHeard.TryGetValue(kv.Key, out var l)) freshHeard[kv.Key] = l = new List<List<(double, string)>>(); l.Add(kv.Value); }
                foreach (var kv in runBy) mostBy[kv.Key] = Math.Max(mostBy.TryGetValue(kv.Key, out var m) ? m : 0, kv.Value);
            }

            Console.WriteLine($"MODE {mode}: runs={runs} (each of the cast out at each hour of night one as the witness)");
            if (newsFile != null)
            {
                // The town's own news: how often he overheard it, and when first.
                int runsHeard = 0, inFirstHour = 0, inTwo = 0; var firsts = new List<double>();
                for (int r = 0; r < runs; r++)
                {
                    double first = double.MaxValue;
                    foreach (var kv in freshHeard)
                    {
                        if (kv.Key != "exchange/tell/news" || r >= kv.Value.Count) continue;
                        foreach (var (t, _) in kv.Value[r])
                        {
                            if (t < 3600) inFirstHour++;
                            if (t < 7200) inTwo++;
                            first = Math.Min(first, t);
                        }
                    }
                    if (first < double.MaxValue) { runsHeard++; firsts.Add(first / 60.0); }
                }
                firsts.Sort();
                string med = firsts.Count == 0 ? "never" : firsts[firsts.Count / 2].ToString("0.0", Inv) + " min";
                Console.WriteLine($"  the town's own news: overheard in {runsHeard}/{runs} runs, first a median {med} in; tellings he overheard in the first hour {inFirstHour / (double)runs:0.0} a run, in two hours {inTwo / (double)runs:0.0}");
            }
            if (deedAtMinute >= 0)
            {
                // After the deed: what the neighbours said, and how soon.
                double d0 = deedAtMinute * 60.0;
                int everydaySoon = 0, reactions = 0, settlingLines = 0, everydaySettling = 0, runsHeard = 0;
                var firstAfter = new List<double>();
                for (int r = 0; r < runs; r++)
                {
                    double first = double.MaxValue;
                    foreach (var kv in freshHeard)
                    {
                        if (r >= kv.Value.Count || !kv.Key.StartsWith("ambient/open/")) continue;
                        foreach (var (t, _) in kv.Value[r])
                        {
                            if (t < d0 || t >= d0 + StreetVoice.SettlingSeconds + 120) continue;
                            bool soon = t < d0 + StreetVoice.JustNowSeconds;
                            if (kv.Key.StartsWith("ambient/open/justnow/")) { reactions++; first = Math.Min(first, t - d0); }
                            else if (kv.Key == "ambient/open/settling") settlingLines++;
                            else if (soon) everydaySoon++;
                            else everydaySettling++;
                        }
                    }
                    if (first < double.MaxValue) { runsHeard++; firstAfter.Add(first); }
                }
                firstAfter.Sort();
                string firstMedian = firstAfter.Count == 0 ? "none" : firstAfter[firstAfter.Count / 2].ToString("0", Inv) + " s";
                Console.WriteLine($"  after the deed at minute {deedAtMinute.ToString(Inv)}: runs where he heard a reaction {runsHeard}/{runs}, the first a median {firstMedian} after; within {StreetVoice.JustNowSeconds.ToString(Inv)} s: reactions {reactions}, everyday lines {everydaySoon}; from then to {(StreetVoice.SettlingSeconds + 120).ToString(Inv)} s: settling {settlingLines}, everyday {everydaySettling}");
            }
            Console.WriteLine("  bank: lines seen | heard in two hours, mean (most) | most in any ten minutes (lines needed for none to come back inside BarkGen's ten-minute floor, with the ledger) | repeats (exact words: right for its one story), seed alone / ledger | shortest gap between hearing one line twice, minutes, the median over the runs where a line came back (k/runs), seed alone / ledger");
            foreach (var bank in freshHeard.Keys.Union(seedHeard.Keys).OrderBy(k => k, StringComparer.Ordinal))
            {
                var fr = freshHeard.TryGetValue(bank, out var f) ? f : new List<List<(double t, string text)>>();
                var sd = seedHeard.TryGetValue(bank, out var s) ? s : new List<List<(double t, string text)>>();
                int bankSize = fr.Concat(sd).SelectMany(r => r).Select(x => x.text).Distinct().Count();
                double meanUses = fr.Count == 0 ? 0 : fr.Sum(r => r.Count) / (double)runs;
                int mostUses = fr.Count == 0 ? 0 : fr.Max(r => r.Count);
                double Rep(List<List<(double t, string text)>> rs) => rs.Sum(r => r.Count - r.Select(x => x.text).Distinct().Count()) / (double)runs;
                string Gap(List<List<(double t, string text)>> rs)
                {
                    var gaps = new List<double>();
                    foreach (var r in rs)
                    {
                        double g = double.MaxValue;
                        foreach (var grp in r.GroupBy(x => x.text))
                        {
                            var ts = grp.Select(x => x.t).OrderBy(x => x).ToList();
                            for (int i = 1; i < ts.Count; i++) g = Math.Min(g, ts[i] - ts[i - 1]);
                        }
                        if (g < double.MaxValue) gaps.Add(g / 60.0);
                    }
                    if (gaps.Count == 0) return "none";
                    gaps.Sort();
                    return gaps[gaps.Count / 2].ToString("0.0", Inv) + $" ({gaps.Count}/{runs} runs)";
                }
                int mostInTen = 0;
                foreach (var r in fr)
                {
                    var ts = r.Select(x => x.t).OrderBy(x => x).ToList();
                    for (int i = 0, j = 0; i < ts.Count; i++)
                    {
                        while (ts[i] - ts[j] >= 600) j++;
                        mostInTen = Math.Max(mostInTen, i - j + 1);
                    }
                }
                Console.WriteLine($"  {bank}: seen {bankSize} | {meanUses:0.0} ({mostUses}) | {mostInTen} | {Rep(sd):0.0} / {Rep(fr):0.0} | {Gap(sd)} / {Gap(fr)}");
            }
            Console.WriteLine("  by named speaker: lines said in his hearing in two hours, mean over the runs (the most in one run), then bank by bank, mean");
            foreach (var who in named.OrderBy(x => x, StringComparer.Ordinal))
            {
                var mine = spokenBy.Where(kv => kv.Key.who == who).OrderBy(kv => kv.Key.bank, StringComparer.Ordinal).ToList();
                if (mine.Count == 0) { Console.WriteLine($"    {who}: none"); continue; }
                double total = mine.Sum(kv => kv.Value) / (double)runs;
                Console.WriteLine($"    {who}: {total:0.0} ({(mostBy.TryGetValue(who, out var most) ? most : 0)}) | " +
                                  string.Join(", ", mine.Select(kv => $"{kv.Key.bank} {kv.Value / (double)runs:0.0}")));
            }
        }
        return 0;
    }

    static double Dist((double x, double z) a, (string name, double x, double z) b)
    {
        double dx = a.x - b.x, dz = a.z - b.z;
        return Math.Sqrt(dx * dx + dz * dz);
    }

    static uint Fnv(string s)
    {
        uint h = 2166136261;
        foreach (char c in s) { h ^= c; h *= 16777619; }
        return h;
    }

    static string Arg(string[] args, string name, string fallback)
    {
        for (int i = 0; i + 1 < args.Length; i++) if (args[i] == name) return args[i + 1];
        return fallback;
    }

    static string RepoRoot()
    {
        var d = new DirectoryInfo(AppContext.BaseDirectory);
        while (d != null && !File.Exists(Path.Combine(d.FullName, "canon.md"))) d = d.Parent;
        return d?.FullName ?? ".";
    }
}
