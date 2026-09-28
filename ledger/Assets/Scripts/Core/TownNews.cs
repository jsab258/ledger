using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// THE TOWN'S OWN NEWS (town list 6aq; ROADMAP stage 6 and A25.01, the third
    /// checklist sweep). Every rumour the new game carried was about Tom: before
    /// he did anything the street had nothing to pass on, so he could not see
    /// talk travel until it was about him, and over two hours the only stories
    /// anyone told were his. A town whose talk is all about the player is the
    /// stage set this Core's comments warn against.
    ///
    /// So happenings among the named cast are DATA (production/specs/town-news.json),
    /// drawn from their routines: each at a place and hour, seen by everybody in
    /// that area then (CastDay), filed through GossipMill.Witness as any sighting
    /// is, and so spread by the same rounds and told by the same street banks
    /// (StreetVoice.Exchange's news bank). A story not about him raises nobody's
    /// suspicion. One sample first; more only after Jafar has heard it.
    public sealed class TownNews
    {
        public sealed class Story
        {
            public string Id, Summary, Area;
            public int Day, Hour;
            public Fact Fact;
            public double Confidence = 0.9;
            /// The people the story is about: they hold it, so nobody tells it
            /// back to them, but never pass it on, and keep no "I saw" memory of
            /// their own doings (the independent check: Rita told her own row).
            public readonly List<string> Parties = new List<string>();
        }

        /// The subject of every story of the town's own.
        public const string Subject = "town";

        public readonly List<Story> Stories = new List<Story>();
        readonly HashSet<string> _filed = new HashSet<string>();

        /// The stories already filed, for a save (and FromFiled for a load).
        public IEnumerable<string> Filed => _filed;
        public void FromFiled(IEnumerable<string> ids) { _filed.Clear(); foreach (var id in ids ?? Array.Empty<string>()) _filed.Add(id); }

        /// Reads the news file. Throws FormatException naming what is wrong.
        public static TownNews Parse(string json)
        {
            var root = MiniJson.AsObject(MiniJson.Deserialize(json)) ?? throw new FormatException("town news: not an object");
            var news = new TownNews();
            foreach (var so in MiniJson.GetList(root, "stories") ?? throw new FormatException("town news: no stories"))
            {
                var o = MiniJson.AsObject(so) ?? throw new FormatException("town news: a story that is not an object");
                var st = new Story
                {
                    Id = MiniJson.GetString(o, "id"),
                    Summary = MiniJson.GetString(o, "summary"),
                    Area = MiniJson.GetString(o, "area"),
                };
                if (string.IsNullOrEmpty(st.Id) || string.IsNullOrEmpty(st.Summary) || string.IsNullOrEmpty(st.Area))
                    throw new FormatException("town news: a story needs an id, a summary and an area");
                if (!(o.TryGetValue("day", out var d) && d is double dd) || !(o.TryGetValue("hour", out var h) && h is double hh) || hh < 0 || hh > 23)
                    throw new FormatException($"town news: {st.Id} needs a day and an hour");
                st.Day = (int)dd; st.Hour = (int)hh;
                var f = MiniJson.GetList(o, "fact");
                if (f == null || f.Count != 3 || !(f[0] is string fs) || !(f[1] is string fp) || !(f[2] is string fv))
                    throw new FormatException($"town news: {st.Id} needs a fact [subject, predicate, value]");
                // The town's own subject, and only it: StreetVoice tells "town" stories
                // as news, never a killing or anything about the player (the check).
                if (fs != Subject) throw new FormatException($"town news: {st.Id}'s fact must have the subject \"{Subject}\"");
                foreach (var other in news.Stories)
                    if (other.Id == st.Id || (other.Fact.Subject == fs && other.Fact.Predicate == fp))
                        throw new FormatException($"town news: {st.Id} repeats an id or a fact");
                st.Fact = new Fact(fs, fp, fv);
                if (o.TryGetValue("confidence", out var c) && c is double cv) st.Confidence = Math.Max(0.0, Math.Min(1.0, cv));
                foreach (var pp in MiniJson.GetList(o, "parties") ?? new List<object>()) if (pp is string ps && ps.Length > 0) st.Parties.Add(ps);
                news.Stories.Add(st);
            }
            return news;
        }

        /// Files every story whose hour has come and that is not yet filed, as
        /// seen by everybody in its area at that hour; returns the ids filed.
        public List<string> Seed(GossipMill mill, CastDay cast, GameTime now)
        {
            var filed = new List<string>();
            if (mill == null || cast == null) return filed;
            foreach (var st in Stories)
            {
                if (_filed.Contains(st.Id)) continue;
                var at = new GameTime(st.Day, st.Hour, 0);
                if (now.TotalMinutes < at.TotalMinutes) continue;
                _filed.Add(st.Id);
                foreach (var p in cast.People)
                    if (cast.AreaOf(cast.PlaceOf(p, st.Day, st.Hour)) == st.Area || st.Parties.Contains(p))
                    {
                        var g = mill.Get(p);
                        int memories = g?.Memory.Events.Count ?? 0;
                        mill.Witness(p, st.Fact, st.Summary, false, at, st.Confidence);
                        if (g != null && st.Parties.Contains(p))
                        {
                            // Theirs to know, not to tell, and not to remember as seen.
                            g.Suppressed.Add(st.Fact.Subject + "." + st.Fact.Predicate);
                            if (g.Memory.Events.Count > memories) g.Memory.Events.RemoveRange(memories, g.Memory.Events.Count - memories);
                        }
                    }
                filed.Add(st.Id);
            }
            return filed;
        }

        /// Who saw a story: everybody in its area at its hour.
        public List<string> WitnessesOf(Story st, CastDay cast)
        {
            var w = new List<string>();
            if (st == null || cast == null) return w;
            foreach (var p in cast.People)
                if (cast.AreaOf(cast.PlaceOf(p, st.Day, st.Hour)) == st.Area) w.Add(p);
            return w;
        }
    }
}
