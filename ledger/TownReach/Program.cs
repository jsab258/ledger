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
            int peakBefore = 0, peakAfter = 0, runs = 0, reachedNobody = 0;
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
                    var heardBy = new HashSet<string>();
                    var saidAboutStory = new HashSet<string>();
                    var saidFaintly = new HashSet<string>();
                    int heardBy60 = 0, runPeakBefore = 0, runPeakAfter = 0;
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
                        if (hour == 59) heardBy60 = heardBy.Count;
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
                }
            double perHearer(double v) => hearers > 0 ? v / hearers : 0;
            Console.WriteLine($"FIRST SIGHT {firstSight.ToString("0.00", Inv)}: runs={runs} (every witness x every {every} h of a week)");
            Console.WriteLine($"  reach: others who hear it  at 60h mean={reach60 / runs:0.00}  by day {days} mean={reachEnd / runs:0.00}  witnesses reaching nobody={reachedNobody}/{runs}");
            Console.WriteLine($"  shows, per hearer, game hours out on the street:  before={perHearer(showBefore):0.0}  after={perHearer(showAfter):0.0}");
            Console.WriteLine($"  showing in the same hour:  most in any run before={peakBefore} after={peakAfter};  a run's busiest hour, mean before={busiestBefore / runs:0.0} after={busiestAfter / runs:0.0}");
            Console.WriteLine($"  hearers who say something about the story at least once: {perHearer(storyRemarkers) * 100:0}%  " +
                              $"(half-remembered, to a companion: {(storyRemarkers > 0 ? faintRemarkers / storyRemarkers * 100 : 0):0}% of those who say something)");
        }
        return 0;
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
