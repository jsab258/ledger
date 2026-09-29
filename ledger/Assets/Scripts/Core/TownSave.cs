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
            return d;
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
            return t;
        }
    }
}
