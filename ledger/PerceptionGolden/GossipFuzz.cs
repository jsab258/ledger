using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;
using Ledger.Core;

namespace Ledger.PerceptionGolden
{
    /// THE SEEDED GOSSIP GENERATOR, AS A FAMILY OF GOLDEN ROWS.
    ///
    /// WHAT IT IS. A seeded random world of two to five people, their ties,
    /// sightings (Witness), rumours put straight into their heads, facts,
    /// bribes, leashes, rounds of talk (Tick) and questions asked outright
    /// (CompareNotes), with every agent's rumours, knowledge, suspicion and
    /// new memory lines written out after every step, and then what each of
    /// them would say (Best, BestOfValue, Suspecting.AccountOf and Derive).
    /// And a seeded hand-mangled save read back by SaveCodec.RestoreMillAgents.
    /// Each world's whole trace is hashed (FNV-1a 64 over its UTF-8 bytes)
    /// and the row carries the hash and the line count:
    ///
    ///   GossipFuzz|scenario|seed|nan 0/1|hash|lines
    ///   GossipFuzz|save|seed|hash|lines
    ///
    /// WHY (the independent reviewer's finding, 29 September). He wrote this
    /// generator twice, in C# and in C++, and the two agreed byte for byte on
    /// 12,000 worlds and 3,000 saves once Gossiper.Best and BestOfValue ranked
    /// a NaN as the C#'s OrderByDescending does. It caught every one of 37
    /// faults planted in the port that the hand-written rows missed. So it is
    /// part of the table now, rather than something one reviewer once ran.
    ///
    /// THE TWO MUST BE CHANGED TOGETHER. The C++ twin is
    /// ue-probe/Source/LedgerProbe/Public/GossipFuzz.h, and it draws the same
    /// random numbers in the same order and writes the same lines. Any change
    /// here (a step, a draw, a word in a line) is made there in the same
    /// commit, or every row goes red, which is the point.
    ///
    /// NaN is a parameter, not shared state: the reviewer's "nonan" run
    /// swapped the NaN entries of the weight and confidence tables for 0.5 by
    /// writing into them; here each world is told which it is, so no row
    /// changes what another row draws.
    public static class GossipFuzz
    {
        static readonly CultureInfo Inv = CultureInfo.InvariantCulture;

        public const int ScenarioSeeds = 1500;
        public const ulong SaveSeedFrom = 1000001;
        public const int SaveSeeds = 500;

        public static void Emit(StringBuilder sb)
        {
            foreach (var nan in new[] { true, false })
                for (int seed = 1; seed <= ScenarioSeeds; seed++)
                {
                    var g = new Gen((ulong)seed, nan);
                    g.RunScenario((ulong)seed);
                    sb.Append("GossipFuzz|scenario|").Append(seed.ToString(Inv)).Append('|').Append(nan ? "1" : "0")
                      .Append('|').Append(g.Hash()).Append('|').Append(g.Lines.ToString(Inv)).Append('\n');
                }
            for (int i = 0; i < SaveSeeds; i++)
            {
                ulong seed = SaveSeedFrom + (ulong)i;
                var g = new Gen(seed, true);
                g.RunSave(seed);
                sb.Append("GossipFuzz|save|").Append(seed.ToString(Inv))
                  .Append('|').Append(g.Hash()).Append('|').Append(g.Lines.ToString(Inv)).Append('\n');
            }
        }

        static readonly double[] W = { 0.0, 0.1, 0.25, 0.3, 0.5, 0.7, 0.9, 1.0, 1.5, -0.2, double.NaN };
        static readonly double[] C = { 0.05, 0.1, 0.19, 0.2, 0.25, 0.3, 0.5, 0.6, 0.8, 0.9, 0.94, 0.95, 1.0, 1.3, -0.1, double.NaN };
        static readonly int[] Rungs = { -5, -1, -1, 0, 1, 2, 3, 4, 4, 7 };
        static readonly int[] DRungs = { -1, 0, 1, 2, 3, 4, 4 };
        static readonly int[] HopsP = { 0, 1, 1, 2, 3 };
        static readonly string[][] Facts = {
            new[]{"player","window_d1","seen"}, new[]{"player","window_d1","other"}, new[]{"player","killed_d1","docker"},
            new[]{"bob","location_d1","docks"}, new[]{"player","where_d1","docks"} };
        static readonly string[] Circles = { "day", "night", "both" };
        static readonly string[] Tok = { "4","2.7","-0.5","1e300","-1e300","1e400","-1e400","\"3\"","null","true","false","4.",".5","+3","-1","-2","0","1E1","3e-1","-0","1e-400","2147483648","-2147483649","4.9999999999999999","00","007","[4]","{}","4abc","0x4","NaN","Infinity","1e","-","4.5.6","+.5","1.e0","-00","2147483647","-2147483648","3 ", "1", "2", "3", "4" };

        static string B(double d) => double.IsNaN(d) ? "NaN" : BitConverter.DoubleToInt64Bits(d).ToString("x16", Inv);
        static string I(long v) => v.ToString(Inv);

        /// One world's state: its random stream, its NaN switch, and the
        /// running hash of its trace. A new one per row.
        sealed class Gen
        {
            ulong s;
            readonly bool nan;
            ulong h = 0xcbf29ce484222325UL;
            public long Lines;

            public Gen(ulong seed, bool withNaN) { s = seed; nan = withNaN; }

            public string Hash() => h.ToString("x16", Inv);

            ulong Next()
            {
                unchecked
                {
                    s += 0x9E3779B97F4A7C15UL;
                    ulong z = s;
                    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9UL;
                    z = (z ^ (z >> 27)) * 0x94D049BB133111EBUL;
                    return z ^ (z >> 31);
                }
            }
            int R(int n) => (int)(Next() % (ulong)n);

            double PickW() { int i = R(21); if (i >= 11) i -= 11; return !nan && i == 10 ? 0.5 : W[i]; }
            double PickC() { int i = R(31); if (i >= 16) i -= 16; return !nan && i == 15 ? 0.5 : C[i]; }

            /// One line of the trace, hashed as its UTF-8 bytes and a newline.
            void L(string x)
            {
                unchecked
                {
                    foreach (var b in Encoding.UTF8.GetBytes(x)) { h ^= b; h *= 0x100000001b3UL; }
                    h ^= (byte)'\n'; h *= 0x100000001b3UL;
                }
                Lines++;
            }

            void DumpAgents(GossipMill mill, string[] ids, Dictionary<string, int> memSeen)
            {
                L("OFF " + I(mill.WitnessesOffered) + " " + I(mill.WitnessesDropped));
                foreach (var id in ids)
                {
                    var g = mill.Get(id);
                    L("A " + id + " susp=" + B(g.Suspicion.Value) + " leash=" + (g.Leashed ? 1 : 0) + " n=" + I(g.Rumors.Count));
                    foreach (var r in g.Rumors)
                        L("R " + r.TopicKey + "=" + r.Content.Value + "|" + r.OriginId + "|" + r.Summary + "|" + B(r.Confidence) + "|" + I(r.Hops) + "|" + (r.Sensitive ? 1 : 0) + (r.Indelible ? 1 : 0) + "|" + I(r.OriginRung));
                    foreach (var f in g.Knowledge.Facts) L("K " + f.Subject + "." + f.Predicate + "=" + f.Value);
                    int seen = memSeen.TryGetValue(id, out var sv) ? sv : 0;
                    for (int i = seen; i < g.Memory.Events.Count; i++)
                    {
                        var e = g.Memory.Events[i];
                        L("M " + e.Time.ToString() + "|" + e.Kind + "|" + B(e.Importance) + "|" + e.Text);
                    }
                    memSeen[id] = g.Memory.Events.Count;
                }
            }

            void DumpEvents(List<GossipEvent> ev)
            {
                L("EV " + I(ev.Count));
                foreach (var e in ev)
                    L("E " + e.FromId + ">" + e.ToId + " c" + (e.Contradiction ? 1 : 0) + " x" + (e.Exposure ? 1 : 0) + " " + e.Rumor.TopicKey + "=" + e.Rumor.Content.Value + " " + B(e.Rumor.Confidence) + " h" + I(e.Rumor.Hops) + " r" + I(e.Rumor.OriginRung) + " i" + (e.Rumor.Indelible ? 1 : 0));
            }

            public void RunScenario(ulong seed)
            {
                L("SEED " + seed.ToString(Inv));
                int n = 2 + R(4);
                var ids = new string[n];
                var graph = new SocialGraph();
                var mill = new GossipMill(graph);
                for (int i = 0; i < n; i++)
                {
                    ids[i] = "a" + I(i);
                    string circle = Circles[R(3)];
                    mill.Add(new Gossiper(ids[i], "N" + I(i), new MemoryStore(ids[i]), new KnowledgeBase(), new SuspicionTracker(), circle));
                }
                for (int i = 0; i < n; i++)
                    for (int j = i + 1; j < n; j++)
                    {
                        int k = R(4);
                        if (k == 0) continue;
                        double w = PickW();
                        if (k == 1) graph.Link(ids[j], ids[i], w); else graph.Link(ids[i], ids[j], w);
                    }
                var memSeen = new Dictionary<string, int>();
                int steps = 6 + R(20);
                for (int st = 0; st < steps; st++)
                {
                    var now = new GameTime(1 + st / 20, st % 20, st % 60);
                    int kind = R(16);
                    L("STEP " + I(st) + " kind " + I(kind));
                    if (kind <= 4)
                    {
                        int ai = R(n + 1);
                        int fi = R(5);
                        int sm = R(6);
                        bool sens = R(2) == 1;
                        double conf = PickC();
                        bool indel = R(5) == 0;
                        int rung = Rungs[R(Rungs.Length)];
                        string summary = sm == 0 ? " s" + I(st) + " " : (sm == 1 ? "   " : "s" + I(st));
                        string wid = ai == n ? "zz" : ids[ai];
                        mill.Witness(wid, new Fact(Facts[fi][0], Facts[fi][1], Facts[fi][2]), summary, sens, now, conf, indel, rung);
                    }
                    else if (kind <= 6)
                    {
                        int ai = R(n);
                        int fi = R(5);
                        int oi = R(n);
                        double conf = PickC();
                        int hops = HopsP[R(HopsP.Length)];
                        bool sens = R(2) == 1;
                        bool indel = R(6) == 0;
                        int rung = DRungs[R(DRungs.Length)];
                        mill.Get(ids[ai]).Rumors.Add(new Rumor { Content = new Fact(Facts[fi][0], Facts[fi][1], Facts[fi][2]), OriginId = ids[oi], Summary = "d" + I(st), Confidence = conf, Hops = hops, Sensitive = sens, Indelible = indel, OriginRung = rung });
                    }
                    else if (kind == 7)
                    {
                        int ai = R(n);
                        int fi = R(5);
                        mill.Get(ids[ai]).Knowledge.Learn(new Fact(Facts[fi][0], Facts[fi][1], Facts[fi][2]));
                    }
                    else if (kind == 8)
                    {
                        int ai = R(n);
                        int fi = R(5);
                        mill.Get(ids[ai]).Suppressed.Add(Facts[fi][0] + "." + Facts[fi][1]);
                    }
                    else if (kind == 9)
                    {
                        int ai = R(n);
                        if (R(3) == 0) mill.Get(ids[ai]).Leashed = true;
                    }
                    else if (kind <= 12)
                    {
                        int mode = R(3);
                        var m = new bool[n, n];
                        for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) m[i, j] = R(3) != 0;
                        Func<string, string, bool> tog = null;
                        if (mode == 1) tog = (x, y) => m[int.Parse(x.Substring(1), Inv), int.Parse(y.Substring(1), Inv)];
                        else if (mode == 2) tog = (x, y) => true;
                        var ev = mill.Tick(now, tog);
                        DumpEvents(ev);
                    }
                    else if (kind <= 14)
                    {
                        int ci = R(n + 1);
                        int pi = R(n);
                        string cid = ci == n ? "zz" : ids[ci];
                        var ev = mill.CompareNotes(cid, ids[pi], now);
                        DumpEvents(ev);
                    }
                    else
                    {
                        int ai = R(n), bi = R(n);
                        double w = PickW();
                        graph.Link(ids[ai], ids[bi], w);
                    }
                    DumpAgents(mill, ids, memSeen);
                }
                // Final reads.
                var topics = new[] { "player.window_d1", "player.killed_d1", "bob.location_d1", "player.where_d1", "player.nothing", "" };
                var fams = new[] { 0.0, 0.2, 0.5, 0.8, 1.0, double.NaN };
                foreach (var id in ids)
                {
                    var g = mill.Get(id);
                    foreach (var f in Facts)
                    {
                        var bv = g.BestOfValue(f[0] + "." + f[1], f[2]);
                        var bt = g.Best(f[0] + "." + f[1]);
                        L("BV " + id + " " + f[0] + "." + f[1] + "=" + f[2] + " " + (bv == null ? "none" : B(bv.Confidence) + "/" + bv.Summary) + " best " + (bt == null ? "none" : B(bt.Confidence) + "/" + bt.Summary));
                    }
                    foreach (var t in topics)
                    {
                        var acc = Suspecting.AccountOf(g, t);
                        L("AC " + id + " [" + t + "] h" + (acc.Held ? 1 : 0) + " s" + (acc.SawItMyself ? 1 : 0) + " r" + I(acc.Rung) + " n" + (acc.NamesHim ? 1 : 0) + " " + B(acc.Confidence) + " " + B(acc.NamingConfidence) + " [" + (acc.Summary ?? "<null>") + "]");
                        for (int nv = 0; nv < 5; nv++)
                        {
                            var near = new Nearness();
                            if (nv == 1) { near.SawHimMyself = true; near.Summary = " by the glass "; }
                            if (nv == 2) { near.SawHimMyself = true; near.OthersNear = 2; }
                            if (nv == 3) { near.HeardHeWasNear = true; near.OthersNear = -3; }
                            if (nv == 4) { near.SawHimMyself = true; near.OthersNear = -1; near.Summary = "  "; }
                            foreach (var fam in fams)
                            {
                                var (value, level, why) = Suspecting.Derive(acc, near, fam);
                                L("DV " + I(nv) + " " + B(fam) + " " + B(value) + " " + level + " [" + (why ?? "<null>") + "]");
                            }
                        }
                    }
                }
            }

            public void RunSave(ulong seed)
            {
                L("SAVE " + seed.ToString(Inv));
                int k = 1 + R(6);
                var sb = new StringBuilder();
                sb.Append("{\"agents\":[{\"id\":\"w\",\"rumors\":[");
                for (int i = 0; i < k; i++)
                {
                    if (i > 0) sb.Append(',');
                    string ht = Tok[R(Tok.Length)];
                    string rt = Tok[R(Tok.Length)];
                    int form = R(6);
                    sb.Append("{\"subj\":\"player\",\"pred\":\"p" + I(i) + "\",\"val\":\"v\",\"conf\":0.5,\"hops\":" + ht);
                    if (form == 0) { }
                    else if (form == 1) sb.Append(",\"rung\":" + rt + ",\"rung\":" + Tok[R(Tok.Length)]);
                    else if (form == 2) sb.Append(",\"ru\\u006eg\" : " + rt);
                    else if (form == 3) sb.Append(",\"inner\":{\"rung\":" + rt + "},\"rung\":1");
                    else sb.Append(",\"rung\":" + rt);
                    sb.Append('}');
                }
                sb.Append("]}]}");
                string json = sb.ToString();
                L("JSON " + json);
                var mill = new GossipMill(new SocialGraph());
                mill.Add(new Gossiper("w", "w", new MemoryStore("w"), new KnowledgeBase(), new SuspicionTracker()));
                mill.Get("w").Rumors.Add(new Rumor { Content = new Fact("player", "sentinel", "v"), OriginId = "w", Summary = "x", Confidence = 0.5, Hops = 7, OriginRung = 3 });
                SaveCodec.RestoreMillAgents(json, mill);
                foreach (var r in mill.Get("w").Rumors)
                    L("SR " + r.Content.Predicate + " h" + I(r.Hops) + " r" + I(r.OriginRung) + " " + B(r.Confidence));
            }
        }
    }
}
