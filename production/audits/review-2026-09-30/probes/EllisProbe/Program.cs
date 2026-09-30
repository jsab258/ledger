// PROOF FOR A11: whom DS Ellis "stops on Quay Street" at a visit, with the
// Core's own WhoSheAsks and HearTheStreet and the real cast file, set up as
// the committed golden row SweepAsked is (every cast member holding a
// sensitive story of his window). Prints each person asked, where their
// routine has them at 09:00, and how far that place is from Rita's window.
//
//   dotnet run --project production/audits/review-2026-09-30/probes/EllisProbe
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using Ledger.Core;

static class Program
{
    static int Main()
    {
        string root = Directory.GetCurrentDirectory();
        while (!File.Exists(Path.Combine(root, "canon.md"))) root = Path.GetDirectoryName(root);
        string castPath = Path.Combine(root, "production", "specs", "hook-cast.json");
        string json = File.ReadAllText(castPath);
        var cast = CastDay.Parse(json);
        var places = new Dictionary<string, (double x, double z)>();
        using (var doc = JsonDocument.Parse(json))
            foreach (var p in doc.RootElement.GetProperty("places").EnumerateObject())
                places[p.Name] = (p.Value.GetProperty("x_m").GetDouble(), p.Value.GetProperty("z_m").GetDouble());

        var mill = new GossipMill(new SocialGraph());
        foreach (var id in cast.People)
        {
            mill.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker()));
            mill.Get(id).Rumors.Add(new Rumor { Content = new Fact("player", "window_d1", "ritas"), Summary = "x", Confidence = 0.9, Sensitive = true, Hops = 1 });
        }
        // Quay Street as built: the parade and the blocks opposite, from the
        // quay at its south end (x -5) to the bus stop at its north end (x 46).
        bool OnQuayStreet(string place) => place != null && places.TryGetValue(place, out var at) && at.x >= -5 && at.x <= 46 && Math.Abs(at.z) <= 10;
        const double wx = 18.869, wz = 4.985;   // Rita's window
        int worst = 0;
        foreach (int day in new[] { 2, 3, 4 })
        {
            var at = new GameTime(day, 9, 0);
            var asked = PoliceFile.WhoSheAsks(mill, cast, at);
            int off = 0, never = 0;
            var lines = new List<string>();
            foreach (var id in asked)
            {
                string place = cast.PlaceOf(id, day, 9);
                double dist = places.TryGetValue(place ?? "", out var p) ? Math.Sqrt((p.x - wx) * (p.x - wx) + (p.z - wz) * (p.z - wz)) : double.NaN;
                bool onStreet = OnQuayStreet(place);
                if (!onStreet) off++;
                if (cast.NeverToPolice(id)) never++;
                lines.Add(string.Format("    {0,-11} at {1,-16} {2,6:0} m from the window{3}{4}", id, place, dist, onStreet ? "" : "  NOT ON QUAY STREET", cast.NeverToPolice(id) ? "  (never goes to the police)" : ""));
            }
            var file = new PoliceFile();
            file.HearTheStreet(mill, day, t => Offence.Damage, cast, at);
            int heardNever = 0;
            foreach (var e in file.Entries) if (cast.NeverToPolice(e.Who)) heardNever++;
            Console.WriteLine($"[A11] {at.ToldAs}: she asks {asked.Count} people; {off} of them are not on Quay Street; {never} never go to the police; her file takes talk from {file.Entries.Count}, {heardNever} of them people who never go to the police");
            foreach (var l in lines) Console.WriteLine(l);
            if (off > worst) worst = off;
        }
        Console.WriteLine("  each of them remembers: \"" + PoliceFile.AskedMemory + "\"");
        Console.WriteLine(worst > 0
            ? "  => PROVED: people whose routine has them off Quay Street are asked, and remember being stopped on Quay Street"
            : "  => not reproduced");
        return 0;
    }
}
