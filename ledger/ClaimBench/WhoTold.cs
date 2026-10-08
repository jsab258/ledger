using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Ledger.Core;

/// WHO TOLD ME, COUNTED (the talk task of 7 October 2026, item 2): a seeded town
/// of the street's people passes a few witnessed stories round for a day, and
/// the count is taken of every second-hand copy: does it know who told its
/// holder, is that right, does it survive a save, and does the holder's reason
/// name them. "Today" is what the code before the change could say: no copy
/// carried a teller, so every heard reason read "I heard that ...". No model is
/// called and nothing is spent.
///
///     whotold [--people 14] [--seed 7] [--hours 24]
static partial class Program
{
    static int WhoTold(string[] args)
    {
        int people = int.Parse(Arg(args, "--people", "14")), seed = int.Parse(Arg(args, "--seed", "7")), hours = int.Parse(Arg(args, "--hours", "24"));
        var rng = new Random(seed);
        var names = new[] { "Sheila", "Ron", "Darren", "Ada", "June", "Rita", "Hal", "Father Walsh", "the sign painter", "the washerwoman",
                            "the locksmith", "the appraiser", "the runner", "the dispatcher", "the day driver", "the night driver" };
        var ids = Enumerable.Range(0, Math.Min(people, names.Length)).Select(i => "p" + i).ToList();
        var graph = new SocialGraph();
        foreach (var a in ids)
            foreach (var b in ids)
                if (string.CompareOrdinal(a, b) < 0 && rng.NextDouble() < 0.3) graph.Link(a, b, 0.6 + 0.4 * rng.NextDouble());
        var mill = new GossipMill(graph);
        for (int i = 0; i < ids.Count; i++) mill.Add(new Gossiper(ids[i], names[i], new MemoryStore(ids[i]), new KnowledgeBase(), new SuspicionTracker()));
        // Three stories, each seen by somebody, one of them naming him.
        var stories = new[] { ("window_d1", "the man that did Rita's window ran towards the quay", 2), ("yard_visit", "Nowak was in the yard after midnight", 4),
                              ("seen_at", "the new owner was down the docks before dawn", -1) };
        int w = 0;
        foreach (var (pred, summary, rung) in stories)
            mill.Witness(ids[(w++ * 5) % ids.Count], new Fact("player", pred, "seen"), summary, true, new GameTime(1, 22, 0), 0.9, rung: rung);
        for (int h = 0; h < hours; h++)
            mill.Tick(new GameTime(1 + (22 + h) / 24, (22 + h) % 24, 0), (a, b) => rng.NextDouble() < 0.5);
        Func<string, string> nameOf = id => mill.Get(id)?.DisplayName;

        int heard = 0, known = 0, right = 0;
        var tellers = new Dictionary<Rumor, string>();
        foreach (var id in ids)
            foreach (var r in mill.Get(id).Rumors.Where(r => r.Hops > 0))
            {
                heard++;
                if (r.ToldById == null) continue;
                known++;
                // Right: the holder remembers hearing it from that very person.
                if (mill.Get(id).Memory.Events.Any(e => e.Text.StartsWith("I heard from " + nameOf(r.ToldById) + " that", StringComparison.Ordinal)
                                                       || e.Text.StartsWith(nameOf(r.ToldById) + " told me, when I asked", StringComparison.Ordinal))) right++;
                tellers[r] = id;
            }
        // Reasons: every holder of a heard account, as they would say it, today and now.
        int accounts = 0, namedToday = 0, namedNow = 0;
        foreach (var id in ids)
            foreach (var topic in mill.Get(id).Rumors.Select(r => r.TopicKey).Distinct())
            {
                var now = Suspecting.AccountOf(mill.Get(id), topic, nameOf);
                if (!now.Held || now.SawItMyself) continue;
                accounts++;
                var today = Suspecting.AccountOf(mill.Get(id), topic);
                if (Suspecting.Derive(today, new Nearness(), 0.2).why.Contains(" told me that ")) namedToday++;
                if (Suspecting.Derive(now, new Nearness(), 0.2).why.Contains(" told me that ")) namedNow++;
            }
        // A save and a load: every teller where it was.
        var json = SaveCodec.Capture(new GameTime(2, 22, 0), new Wallet(10), new Campaign(), new PlayerKnowledge(), new SecretsBook(), new BeatBook(), mill, new DebtBook(), null);
        var again = new GossipMill(graph);
        for (int i = 0; i < ids.Count; i++) again.Add(new Gossiper(ids[i], names[i], new MemoryStore(ids[i]), new KnowledgeBase(), new SuspicionTracker()));
        SaveCodec.RestoreMillAgents(json, again);
        int kept = 0;
        foreach (var id in ids)
        {
            var before = mill.Get(id).Rumors.Where(r => r.Hops > 0).Select(r => r.TopicKey + "|" + r.Content.Value + "|" + r.Hops + "|" + r.ToldById).OrderBy(x => x).ToList();
            var after = again.Get(id).Rumors.Where(r => r.Hops > 0).Select(r => r.TopicKey + "|" + r.Content.Value + "|" + r.Hops + "|" + r.ToldById).OrderBy(x => x).ToList();
            kept += before.Count(after.Contains);
        }
        Console.WriteLine($"whotold: {ids.Count} people, {stories.Length} stories, {hours} hours (seed {seed}): {heard} second-hand copies; " +
                          $"who told them known today 0, now {known}; confirmed by their own memory of the telling {right} of {known}; kept through a save {kept} of {heard}");
        Console.WriteLine($"whotold: {accounts} heard accounts; the reason names who told them today {namedToday}, now {namedNow}");
        return 0;
    }
}
