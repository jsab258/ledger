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
///     ... -- --cast production/specs/hook-cast.json --two-hours [--clear-every 45]
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
        if (metArg != null) return Meridian(cast, metArg.Split(','));
        if (Array.IndexOf(args, "--two-hours") >= 0) return TwoHours(cast, File.ReadAllText(castPath), double.Parse(Arg(args, "--clear-every", StreetVoice.ClearWordsEverySeconds.ToString(Inv)), Inv));

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

    /// MERIDIAN CONDITION 2, THE SIMULATION'S SIDE (town list 6l): "within those
    /// 30 minutes the world visibly knows them at least once". Play starts at
    /// nine on day one; he has met only `met` (the first hour's day one); he is
    /// seen on night one (22:00 to 04:00) by whoever of the cast is out on the
    /// street then. Counted by minute thirty (hour 60 of play): whether anyone he
    /// met shows it as he passes (the longer look, or a word), and whether one of
    /// them says it to his face. Only those he met can tell it is him; everyone
    /// else is a stranger to him, as canon has it. He passes everybody out on the
    /// street once an hour, as in the rest of this tool: generous.
    static int Meridian(CastDay cast, string[] met)
    {
        var people = cast.People;
        var metSet = new HashSet<string>(met.Select(m => m.Trim()).Where(m => m.Length > 0));
        Console.WriteLine($"meridian met={string.Join(",", metSet)} of {people.Count}; night one, play from 09:00, counted to minute 30 (hour 60)");
        foreach (double firstSight in new[] { 0.6, 1.0 })
        {
            int runs = 0, shown = 0, faced = 0;
            var firstShown = new List<int>();
            var firstHeld = new List<int>();
            for (int sightHour = 13; sightHour <= 19; sightHour++)
            {
                int sHour = (9 + sightHour) % 24;
                int sAbsDay = (9 + sightHour) / 24;
                foreach (var witness in people)
                {
                    if (cast.Where(witness, sAbsDay, sHour) == null) continue;   // not out on the street to see it
                    runs++;
                    var graph = new SocialGraph();
                    foreach (var (a, b, w) in cast.Ties) graph.Link(a, b, w);
                    var mill = new GossipMill(graph);
                    foreach (var p in people)
                        mill.Add(new Gossiper(p, p, new MemoryStore(p), new KnowledgeBase(), new SuspicionTracker()));
                    var start = new GameTime(sAbsDay, sHour, 0);
                    mill.Age(start);
                    mill.Witness(witness, new Fact("player", "night_walk_d1", "seen"),
                        "the new owner was about the yard after midnight", sensitive: true, start, confidence: firstSight);
                    var remarks = new RemarkLedger();
                    bool wasShown = false, wasFaced = false, wasHeld = false;
                    for (int playHour = sightHour; playHour < 60; playHour++)
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
            Console.WriteLine($"  someone he met first holds it (before it can show), minutes: {string.Join(" ", firstHeld.Select(h => (h * 0.5).ToString("0", Inv)))}");
            string when = firstShown.Count > 0 ? $"; when it shows, median minute {firstShown[firstShown.Count / 2] * 0.5:0} (all: {string.Join(" ", firstShown.Select(h => (h * 0.5).ToString("0", Inv)))})" : "";
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
    static int TwoHours(CastDay cast, string castJson, double clearEvery)
    {
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
                void Note(Dictionary<string, List<(double, string)>> into, string bank, double t, string text)
                {
                    if (bank == null || string.IsNullOrEmpty(text)) return;
                    if (!into.TryGetValue(bank, out var l)) into[bank] = l = new List<(double, string)>();
                    l.Add((t, text));
                }
                double nextTalk = 0;
                int ambientCount = 0;
                for (int playHour = 0; playHour < Hours; playHour++)
                {
                    int abs = 9 + playHour, day = abs / 24, hourOfDay = abs % 24;
                    if (abs == sightAbs) mill.Witness(witness, new Fact("player", "night_walk_d1", "seen"),
                        "the new owner was about the yard late at night", sensitive: true, seen, confidence: 1.0);
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
                            if (ev.Rumor == null || ev.Rumor.Content.Subject != "player") continue;
                            if (!earshot.Contains(ev.FromId) || !earshot.Contains(ev.ToId)) continue;
                            double t = hourStart + minute / 60.0 * SecondsPerHour;
                            var from = mill.Get(ev.FromId); var to = mill.Get(ev.ToId);
                            foreach (var l in StreetVoice.Exchange(ev.Rumor, from, to, day * 31 + hourOfDay)) Note(runSeed, l.Bank, t, l.Text);
                            foreach (var l in StreetVoice.Exchange(ev.Rumor, from, to, day * 31 + hourOfDay, ledger)) { Note(runFresh, l.Bank, t, l.Text); ledger.Heard(l); }
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
                    while (nextTalk < hourEnd)
                    {
                        double t = Math.Max(nextTalk, hourStart);
                        nextTalk = t + every;
                        if (pairs.Count == 0) continue;   // spent, with nobody to pair
                        var (a, b) = pairs[ambientCount++ % pairs.Count];
                        var now = new GameTime(day, hourOfDay, 0);
                        int seed = day * 17 + hourOfDay * 3 + near.Count;
                        foreach (var l in StreetVoice.Ambient(mill.Get(a), mill.Get(b), now, 0.5, 1.0, false, false, seed)) Note(runSeed, l.Bank, t, l.Text);
                        foreach (var l in StreetVoice.Ambient(mill.Get(a), mill.Get(b), now, 0.5, 1.0, false, false, seed, ledger)) { Note(runFresh, l.Bank, t, l.Text); ledger.Heard(l); }
                    }
                }
                foreach (var kv in runSeed) { if (!seedHeard.TryGetValue(kv.Key, out var l)) seedHeard[kv.Key] = l = new List<List<(double, string)>>(); l.Add(kv.Value); }
                foreach (var kv in runFresh) { if (!freshHeard.TryGetValue(kv.Key, out var l)) freshHeard[kv.Key] = l = new List<List<(double, string)>>(); l.Add(kv.Value); }
            }

            Console.WriteLine($"MODE {mode}: runs={runs} (each of the cast out at each hour of night one as the witness)");
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
