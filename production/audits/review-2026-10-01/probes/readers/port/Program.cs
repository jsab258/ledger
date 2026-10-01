using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using Ledger.Core;

static class P
{
    static string D(double d) => d.ToString("F6", CultureInfo.InvariantCulture);
    static void Out(string s) => Console.WriteLine(s);
    static GossipMill Mill(CastDay c)
    {
        var m = new GossipMill(new SocialGraph());
        foreach (var id in c.People) m.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker()));
        return m;
    }
    static void DumpMem(GossipMill m, CastDay c, string tag)
    {
        foreach (var id in c.People.OrderBy(x => x, StringComparer.Ordinal))
        {
            var g = m.Get(id);
            foreach (var e in g.Memory.Events) Out(tag + " M " + id + " " + e.Time.Day + ":" + e.Time.Hour + ":" + e.Time.Minute + "|" + e.Kind + "|" + D(e.Importance) + "|" + e.Text);
            foreach (var r in g.Rumors) Out(tag + " R " + id + " " + r.TopicKey + "|" + r.Content.Value + "|" + D(r.Confidence) + "|" + r.Hops + "|" + r.OriginRung + "|" + r.Summary);
        }
    }
    static void Main()
    {
        // S1/S2: Aftermath there-paths
        var kept = CastDay.Parse("{\"talk_range_m\":6,\"places\":{\"counter\":{\"x_m\":0,\"z_m\":0,\"inside\":true},\"step\":{\"x_m\":0,\"z_m\":3}}," +
            "\"areas\":{\"shop\":{\"places\":[\"counter\",\"step\"],\"names\":[\"Rita's\",\"the pawn shop\"],\"keeper\":\"rita\"}}," +
            "\"people\":[{\"id\":\"rita\",\"routine\":[[0,\"off\"],[9,\"counter\"],[17,\"off\"]]},{\"id\":\"passer\",\"routine\":[[0,\"off\"],[12,\"step\"],[15,\"off\"]]},{\"id\":\"hal\",\"routine\":[[0,\"off\"],[11,\"counter\"],[12,\"off\"]]}],\"ties\":[]}");
        foreach (var (done, mend, leave) in new[] {
            (new GameTime(0, 12, 5), (GameTime?)null, (string[])null),
            (new GameTime(0, 11, 30), (GameTime?)new GameTime(0, 11, 50), null),
            (new GameTime(0, 11, 30), (GameTime?)new GameTime(0, 11, 30), null),
            (new GameTime(0, 11, 59), (GameTime?)new GameTime(0, 12, 0), null),
            (new GameTime(0, 2, 0), (GameTime?)null, new[]{"passer"}),
            (new GameTime(1, 0, 30), (GameTime?)null, null),
        })
        {
            var m = Mill(kept);
            var a = new Aftermath("shop", "k", "somebody put Rita's window in", done, mend, leave);
            var f1 = a.Tick(m, kept, new GameTime(0, 11, 45));
            var f2 = a.Tick(m, kept, new GameTime(2, 20, 0));
            Out("AFT " + done + " " + string.Join(",", f1.ConvertAll(x => x.who + "@" + x.when.TotalMinutes)) + " | " + string.Join(",", f2.ConvertAll(x => x.who + "@" + x.when.TotalMinutes)) + " | " + MiniJson.Serialize(a.ToJson()));
            DumpMem(m, kept, "AFT");
        }
        // S3: KeeperMemoryOf wordings
        var names = CastDay.Parse("{\"talk_range_m\":6,\"places\":{\"counter\":{\"x_m\":0,\"z_m\":0}}," +
            "\"areas\":{\"shop\":{\"places\":[\"counter\"],\"names\":[\"Rita's\",\"the pawn shop\",\"Rita's place\",\"pawn\"],\"keeper\":\"rita\"},\"bare\":{\"places\":[],\"names\":[],\"keeper\":\"rita\"}}," +
            "\"people\":[{\"id\":\"rita\",\"routine\":[[0,\"counter\"]]}],\"ties\":[]}");
        foreach (var said in new[] { "somebody put Rita's window in", "the pawn shop's window was put in", "somebody put rita's window in.", "glass all over Rita's place step", "the pawn's door kicked", "  somebody put Rita's window in . . ", "ésomething at Rita's", "somebody smashed RITA'S window", "pawn shop glass" })
            foreach (var area in new[] { "shop", "bare" })
                foreach (var there in new[] { false, true })
                    Out("KMO " + area + " " + there + " [" + said + "] => " + new Aftermath(area, "k", said, new GameTime(0, 2, 0)).KeeperMemoryOf(names, there) + " || " + new Aftermath(area, "k", said, new GameTime(0, 2, 0)).PresentMemoryOf() + " || " + new Aftermath(area, "k", said, new GameTime(0, 2, 0)).MemoryOf());
        // S4: Ada's tea
        foreach (var (how, spans) in new (string, (int, int)[])[] {
            ("slipped", new[]{(21*60+5, 21*60+40), (21*60+55, 22*60+40)}),
            ("neareleven", new[]{(22*60+10, 22*60+50)}),
            ("lateleft", new[]{(21*60+45, 22*60+20)}),
            ("ten", new[]{(22*60, 22*60+40)}),
            ("tenone", new[]{(22*60+1, 22*60+40)}),
            ("ontime-tolast", new[]{(21*60+30, 22*60+30)}),
            ("late-gap", new[]{(21*60+45, 22*60+5), (22*60+16, 22*60+40)}),
            ("one", new[]{(22*60+59, 22*60+59)}),
        })
        {
            var mill = new GossipMill(null);
            mill.Add(new Gossiper("ada", "ada", new MemoryStore("ada"), new KnowledgeBase(), new SuspicionTracker()));
            var ada = mill.Get("ada");
            var tea = AdasTea.For(0, true);
            tea.SheSeesHim(new GameTime(2, 10, 0));
            foreach (var (from, to) in spans) for (int mm = from; mm <= to; mm++) tea.WithHer(new GameTime(2, mm / 60, mm % 60));
            var st = tea.Close(ada, new GameTime(2, 23, 0));
            var back = AdasTea.FromJson(tea.ToJson());
            Out("TEA " + how + " " + st + " " + D(ada.Loyalty) + " " + D(ada.Suspicion.Value) + " " + (ada.Memory.Events.Count > 0 ? ada.Memory.Events[ada.Memory.Events.Count - 1].Text : "none") + " back=" + back.State);
        }
        // S5: CastDay.Parse refusals
        string Base(string placeExtra, string areaExtra) => "{\"talk_range_m\":6,\"places\":{\"a\":{\"x_m\":0,\"z_m\":0" + placeExtra + "}},\"areas\":{\"A\":{\"places\":[\"a\"]" + areaExtra + "}},\"people\":[{\"id\":\"p\",\"routine\":[[0,\"a\"]]}],\"ties\":[]}";
        foreach (var (label, json) in new[] {
            ("inside-yes", Base(",\"inside\":\"yes\"", "")),
            ("inside-1", Base(",\"inside\":1", "")),
            ("inside-null", Base(",\"inside\":null", "")),
            ("inside-false", Base(",\"inside\":false", "")),
            ("keeper-nobody", Base("", ",\"keeper\":\"nobody\"")),
            ("keeper-empty", Base("", ",\"keeper\":\" \"")),
            ("keeper-num", Base("", ",\"keeper\":3")),
            ("keeper-null", Base("", ",\"keeper\":null")),
            ("keeper-spaced", Base("", ",\"keeper\":\" p \"")),
            ("street-1", Base("", ",\"street\":1")),
            ("street-null", Base("", ",\"street\":null")),
            ("street-true", Base("", ",\"street\":true")),
            ("hours-text", Base("", ",\"hours\":\"x\"")),
            ("hours-bad-day", Base("", ",\"hours\":{\"funday\":[9,17]}")),
            ("hours-25", Base("", ",\"hours\":{\"mon\":[9,49]}")),
            ("hours-backwards", Base("", ",\"hours\":{\"mon\":[17,9]}")),
            ("hours-quarter", Base("", ",\"hours\":{\"mon\":[9.25,17]}")),
            ("breaks-no-hours", Base("", ",\"breaks\":{\"mon\":[[12,13]]}")),
            ("hours-ok", Base("", ",\"hours\":{\"mon\":[9,17.5]}")),
            ("keeper-twice-last-bad", Base("", ",\"keeper\":\"p\",\"keeper\":\"zz\"")),
        })
        {
            string outcome;
            try { var c = CastDay.Parse(json); outcome = "accepted keeper=" + (c.KeeperOf("A") ?? "null") + " inside=" + c.IsInside("a") + " street=" + c.OnQuayStreet("p", 0, 9); } catch (FormatException e) { outcome = "refused"; }
            Out("PARSE " + label + " " + outcome);
        }
        // S6: Together walls
        var walls = CastDay.Parse("{\"talk_range_m\":6,\"places\":{\"ia\":{\"x_m\":0,\"z_m\":0,\"inside\":true},\"ia2\":{\"x_m\":1,\"z_m\":0,\"inside\":true},\"ib\":{\"x_m\":2,\"z_m\":0,\"inside\":true},\"oc\":{\"x_m\":3,\"z_m\":0},\"od\":{\"x_m\":4,\"z_m\":0},\"ie\":{\"x_m\":5,\"z_m\":0,\"inside\":true},\"oa\":{\"x_m\":0,\"z_m\":1}}," +
            "\"areas\":{\"A\":{\"places\":[\"ia\",\"ia2\",\"oa\"]},\"B\":{\"places\":[\"ib\"]},\"C\":{\"places\":[\"oc\"]}}," +
            "\"people\":[{\"id\":\"ia\",\"routine\":[[0,\"ia\"]]},{\"id\":\"ia2\",\"routine\":[[0,\"ia2\"]]},{\"id\":\"ib\",\"routine\":[[0,\"ib\"]]},{\"id\":\"oc\",\"routine\":[[0,\"oc\"]]},{\"id\":\"od\",\"routine\":[[0,\"od\"]]},{\"id\":\"ie\",\"routine\":[[0,\"ie\"]]},{\"id\":\"oa\",\"routine\":[[0,\"oa\"]]},{\"id\":\"off\",\"routine\":[[0,\"off\"]]}],\"ties\":[]}");
        foreach (var x in walls.People) Out("TOG " + x + " " + string.Concat(walls.People.Select(y => walls.Together(x, y, 0, 9) ? "1" : "0")));
        // S7: MergeRung
        var rs = new[] { -1, 0, 1, 3, 4, 5 };
        foreach (var x in rs) Out("MERGE " + x + " " + string.Join(",", rs.Select(y => Rumor.MergeRung(x, y))));
        // S7b: second look via Witness
        foreach (var (r1, r2) in new[] { (-1, 1), (1, -1), (4, 2), (2, 4), (-1, 4), (0, 3) })
        {
            var m = new GossipMill(null);
            m.Add(new Gossiper("w", "w", new MemoryStore("w"), new KnowledgeBase(), new SuspicionTracker()));
            m.Witness("w", new Fact("player", "x_d1", "v"), "s", true, new GameTime(1, 10, 0), 0.5, rung: r1);
            m.Witness("w", new Fact("player", "x_d1", "v"), "s2", true, new GameTime(1, 11, 0), 0.7, rung: r2);
            var g = m.Get("w");
            Out("LOOK " + r1 + " " + r2 + " " + string.Join(";", g.Rumors.Select(r => r.OriginRung + "/" + D(r.Confidence) + "/" + r.Summary)) + " mem=" + string.Join(";", g.Memory.Events.Select(e => e.Text)));
        }
        // S8: TownHours sequences
        var small = CastDay.Parse("{\"talk_range_m\":6,\"places\":{\"a\":{\"x_m\":0,\"z_m\":0}},\"people\":[{\"id\":\"p\",\"routine\":[[0,\"a\"]]},{\"id\":\"q\",\"routine\":[[0,\"a\"]]},{\"id\":\"r\",\"routine\":[[0,\"off\"],[13,\"a\"]]}],\"ties\":[[\"p\",\"q\",0.9],[\"q\",\"r\",0.9]]}");
        foreach (var seq in new[] { new[] { 723, 779, 850 }, new[] { 720, 721, 722, 726, 900 }, new[] { 779, 780, 3000 }, new[] { -30, 5, 70 } })
        {
            var g = new SocialGraph(); foreach (var (a, b, w) in small.Ties) g.Link(a, b, w);
            var m = new GossipMill(g);
            foreach (var id in small.People) m.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker()));
            m.Witness("p", new Fact("player", "seen_d0", "here"), "the new owner was here", true, new GameTime(0, 12, 0), 0.9, rung: 4);
            var th = new TownHours();
            var log = new List<string>();
            foreach (var t in seq)
            {
                int ran = th.RunTo(m, small, GameTime.FromTotalMinutes(t) );
                log.Add(t + ":" + ran + ":" + MiniJson.Serialize(th.ToJson()));
            }
            Out("HOURS " + string.Join(",", seq) + " " + string.Join(" ", log));
            foreach (var id in small.People) foreach (var r in m.Get(id).Rumors) Out("HOURS  R " + id + " " + r.TopicKey + " " + D(r.Confidence) + " " + r.Hops);
            foreach (var id in small.People) foreach (var e in m.Get(id).Memory.Events) Out("HOURS  M " + id + " " + e.Time + " " + e.Text);
        }
        foreach (var js in new[] { "{\"round\":726}", "{\"round\":727}", "{\"next\":12}", "{\"round\":-6,\"next\":3}", "{\"round\":-1}", "{\"round\":-7,\"next\":3}", "{\"round\":6e8,\"next\":2}", "{\"round\":\"6\",\"next\":2}", "{\"next\":-1}", "{\"round\":-0.0}", "{\"round\":12.0}", "{\"round\":599999994}" })
            Out("HJSON " + js + " => " + MiniJson.Serialize(TownHours.FromJson(MiniJson.AsObject(MiniJson.Deserialize(js))).ToJson()));
        // S9: WitnessRemembering on an existing rumor
        {
            var m = new GossipMill(null);
            m.Add(new Gossiper("w", "w", new MemoryStore("w"), new KnowledgeBase(), new SuspicionTracker()));
            m.Witness("w", new Fact("player", "week_d6", "takeover"), "heard", false, new GameTime(6, 9, 0), 0.4);
            m.WitnessRemembering("w", new Fact("player", "week_d6", "takeover"), "told", true, new GameTime(6, 10, 0), "remembered");
            m.WitnessRemembering("w", new Fact("player", "week_d6", "takeover"), "told2", false, new GameTime(6, 11, 0), "");
            var g = m.Get("w");
            Out("WREM " + string.Join(";", g.Rumors.Select(r => r.Summary + "/" + D(r.Confidence) + "/" + r.Sensitive + "/" + r.Hops)) + " mem=" + string.Join(";", g.Memory.Events.Select(e => e.Kind + "/" + D(e.Importance) + "/" + e.Text)));
        }
        // S10: OnQuayStreet small cast vs real: not here.
    }
}
