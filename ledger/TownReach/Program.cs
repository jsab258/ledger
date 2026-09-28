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
