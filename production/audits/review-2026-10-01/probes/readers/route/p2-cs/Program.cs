using System;
using System.IO;
using System.Linq;
using System.Collections.Generic;
using Ledger.Core;

static class P
{
    static void Main(string[] args)
    {
        var cast = CastDay.Parse(File.ReadAllText(args[0]));
        var outp = new List<string>();
        var people = cast.People.ToList();
        for (int d = 0; d < 7; d++)
            for (int h = 0; h < 24; h++)
            {
                foreach (var p in people) if (cast.OnQuayStreet(p, d, h)) outp.Add($"Q|{d}|{h}|{p}");
                for (int i = 0; i < people.Count; i++)
                    for (int j = i + 1; j < people.Count; j++)
                        if (cast.Together(people[i], people[j], d, h)) outp.Add($"T|{d}|{h}|{people[i]}|{people[j]}");
            }
        foreach (var l in new[] { 0.5, 0.55, 0.575, 0.6, 0.75 })
            foreach (var n in new[] { 0.35, 0.4, 0.5 })
            {
                var g = new Gossiper("x", "x", null, null, null, "day", 0.5, n, l);
                outp.Add($"W|{l}|{n}|{PoliceFile.WouldReport(g, Offence.Damage, false, "player.window_d0")}");
            }
        // the keeper's memory, there and not there
        var a = new Aftermath("ritas", "rita_window", "somebody put Rita's window in", new GameTime(0, 10, 30));
        outp.Add("K|" + a.KeeperMemoryOf(cast, true));
        outp.Add("K|" + a.KeeperMemoryOf(cast, false));
        File.WriteAllLines(args[1], outp);
        Console.WriteLine($"lines {outp.Count}");
    }
}
