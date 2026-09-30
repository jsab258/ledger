using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// ONE SAVE FOR THE TOWN'S PIECES (town list 6bl; ROADMAP stage 4). The
    /// builder was asked to save six pieces of the new game's town one by one,
    /// each its own ToJson beside the game's save, and to restore each: one
    /// forgotten is a reload where the town forgets it. So they travel together:
    /// one object each way, with a version, every piece restored from what it
    /// can read and made fresh where it cannot.
    ///   hints   FirstMoments   the hints shown
    ///   asks    Arrangement    the outfit's asks answered
    ///   tea     AdasTea        Ada's tea, once made (null before)
    ///   police  PoliceFile     who told the police what, and her visits
    ///   heard   RemarkLedger   what he has heard, and who has remarked
    ///   news    TownNews       the town's own stories already filed (ids)
    ///   damage  Aftermath      each deed's damage, who has found it, until mended
    ///   arrests Custody        each time he was taken in, and what came of it
    ///   hours   TownHours      the hours the town has talked through
    ///   week    WeeksEnd       Sheila's question at the week's end, and his answer
    ///   shown   Waiting        the wait's lines he has been shown (the game's
    ///                          WaitBeats.Shown is this set; the time-and-state
    ///                          sweep, 30 September: kept nowhere, a reload
    ///                          stopped him again at lines already shown)
    public sealed class TownSave
    {
        /// The bundle's version. A file from a later version than this build
        /// knows is refused (SaveIncompatibleException), as the game's own save is.
        public const int Version = 1;

        public FirstMoments Hints = new FirstMoments();
        public Arrangement Asks = new Arrangement(0);
        public AdasTea Tea;
        public PoliceFile Police = new PoliceFile();
        public RemarkLedger Heard = new RemarkLedger();
        public readonly List<string> NewsFiled = new List<string>();
        public readonly List<Aftermath> Damage = new List<Aftermath>();
        public readonly List<Custody> Arrests = new List<Custody>();
        public TownHours Hours = new TownHours();
        public WeeksEnd Week = new WeeksEnd();
        public readonly HashSet<string> WaitShown = new HashSet<string>();

        public Dictionary<string, object> ToJson()
        {
            var news = new List<object>();
            foreach (var id in NewsFiled) news.Add(id);
            var d = new Dictionary<string, object>
            {
                { "version", (double)Version },
                { "hints", Hints.ToJson() },
                { "asks", Asks.ToJson() },
                { "police", Police.ToJson() },
                { "heard", Heard.ToJson() },
                { "news", news },
            };
            if (Tea != null) d["tea"] = Tea.ToJson();
            var damage = new List<object>();
            foreach (var a in Damage) damage.Add(a.ToJson());
            d["damage"] = damage;
            var arrests = new List<object>();
            foreach (var c in Arrests) arrests.Add(c.ToJson());
            d["arrests"] = arrests;
            d["hours"] = Hours.ToJson();
            d["week"] = Week.ToJson();
            var shown = new List<string>(WaitShown);
            shown.Sort(StringComparer.Ordinal);
            var shownList = new List<object>();
            foreach (var k in shown) shownList.Add(k);
            d["shown"] = shownList;
            return d;
        }

        // A wait's stop key as WaitStop makes it: a word ("sheila_answer" has an
        // underscore: the independent check), "@", and a day or a minute.
        static bool IsStopKey(string k)
        {
            int at = k.IndexOf('@');
            if (at <= 0 || at == k.Length - 1 || k.Length - at - 1 > 9) return false;
            for (int i = 0; i < k.Length; i++)
                if (i < at ? !((k[i] >= 'a' && k[i] <= 'z') || (k[i] == '_' && i > 0)) : i > at && !(k[i] >= '0' && k[i] <= '9')) return false;
            return true;
        }

        /// From ToJson's values: each piece from what it can read, fresh where
        /// it cannot (a damaged piece loses its own state, never the rest). A
        /// version later than this build's is refused, as SaveCodec refuses one;
        /// a missing or unreadable version is read as this one.
        public static TownSave FromJson(Dictionary<string, object> saved)
        {
            var t = new TownSave();
            if (saved == null) return t;
            if (saved.TryGetValue("version", out var v) && v is double dv && dv > Version)
                throw new SaveIncompatibleException(SaveFault.FromTheFuture, $"the town's save is version {dv}, this build reads {Version}");
            Dictionary<string, object> Obj(string key) => saved.TryGetValue(key, out var o) ? o as Dictionary<string, object> : null;
            t.Hints = FirstMoments.FromJson(Obj("hints"));
            t.Asks = Arrangement.FromJson(Obj("asks"));
            t.Tea = AdasTea.FromJson(Obj("tea"));
            t.Police = PoliceFile.FromJson(Obj("police"));
            t.Heard = RemarkLedger.FromJson(Obj("heard"));
            if (saved.TryGetValue("news", out var n) && n is List<object> list)
                foreach (var x in list)
                    if (x is string id && id.Length > 0 && !t.NewsFiled.Contains(id)) t.NewsFiled.Add(id);
            if (saved.TryGetValue("damage", out var dm) && dm is List<object> dmList)
                foreach (var x in dmList)
                    if (Aftermath.FromJson(x as Dictionary<string, object>) is Aftermath a && !t.Damage.Exists(o => o.Key == a.Key)) t.Damage.Add(a);
            // Each deed he was taken in for (the police file says which), once,
            // the earliest of any given twice, in the order taken.
            var arrests = new List<Custody>();
            if (saved.TryGetValue("arrests", out var ar) && ar is List<object> arList)
                foreach (var x in arList)
                    if (Custody.FromJson(x as Dictionary<string, object>) is Custody c && t.Police.Took(c)) arrests.Add(c);
            arrests.Sort((a, b) => a.TakenAt.TotalMinutes != b.TakenAt.TotalMinutes ? a.TakenAt.TotalMinutes.CompareTo(b.TakenAt.TotalMinutes) : string.CompareOrdinal(a.Topic, b.Topic));
            foreach (var c in arrests) if (!t.Arrests.Exists(o => o.Topic == c.Topic)) t.Arrests.Add(c);
            t.Hours = TownHours.FromJson(Obj("hours"));
            t.Week = WeeksEnd.FromJson(Obj("week"));
            if (saved.TryGetValue("shown", out var sh) && sh is List<object> shList)
                foreach (var x in shList) if (x is string k && IsStopKey(k)) t.WaitShown.Add(k);
            return t;
        }
    }
}
