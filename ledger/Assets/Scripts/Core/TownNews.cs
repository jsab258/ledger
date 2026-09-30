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
                // A whole day within what a save keeps, a whole hour (the port's
                // independent check, 30 September: 1e10, or a fraction, was taken).
                if (dd != Math.Floor(dd) || dd < 0 || dd >= Arrangement.LastDay || hh != Math.Floor(hh))
                    throw new FormatException($"town news: {st.Id} needs a whole day from 0 to {Arrangement.LastDay - 1} and a whole hour");
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

    /// THE DAMAGE FOUND AFTERWARDS (town list 6br; the town's half of A12.16,
    /// what is broken stays broken, and A25.07, what a deed leaves handled
    /// consistently). A window put in where nobody saw it was talked of by
    /// nobody next day, though the pane was gone. Now whoever comes into the
    /// deed's area, hour by hour from the hour after it until it is mended,
    /// finds it: the town's own news, naming nobody ("somebody put Rita's window
    /// in"), filed as a sighting is and told by the news bank, so it raises
    /// nobody's suspicion. The routines put each keeper at their counter when
    /// they open, so Rita finds her own window when she comes in. Whoever saw
    /// the deed itself (LeaveOut) finds nothing new; whoever had heard it before
    /// they came by sees it, and gets no second copy; nobody finds it twice,
    /// however long it stays unmended or their story fades (the independent
    /// check: a faded finder found it again at the old hour). Their memory is
    /// of the damage they saw, never of the deed. Saved with the town
    /// (TownSave); the game calls Tick every hour and after a load.
    public sealed class Aftermath
    {
        public string Area { get; private set; }
        public string Key { get; private set; }
        public string Said { get; private set; }
        public GameTime DoneAt { get; private set; }
        public GameTime MendedAt { get; private set; }
        readonly HashSet<string> _leaveOut = new HashSet<string>();
        readonly HashSet<string> _found = new HashSet<string>();
        long _nextHour;

        /// Who has found it so far (for the tests; the save carries it).
        internal IEnumerable<string> FoundBy => _found;

        /// When a pane put in overnight is mended if the game does not say:
        /// boarded that morning, the glazier by four the working day after the
        /// night, never a Sunday, when nobody would come by to find it (the
        /// independent check) (inferred).
        public static GameTime DefaultMend(GameTime done)
        {
            int d = done.Hour < 6 ? done.Day : done.Day + 1;
            while (CastDay.Weekday(d) == 6) d++;
            return new GameTime(d, 16, 0);
        }

        /// The longest a damage stays unmended, however it is given: ninety days.
        public const int LongestUnmendedDays = 90;

        /// What a finder remembers: the damage they saw, not the deed.
        public string MemoryOf() => "I came by and saw it for myself: " + Said + ". I never saw who did it.";

        static long FloorDiv(long a, long b) => a >= 0 ? a / b : -((-a + b - 1) / b);

        /// A deed's damage in `area` (a CastDay area id), under `key` (unique
        /// to the deed), told as `said`, done at `doneAt`, mended at `mendedAt`
        /// (DefaultMend when null); `leaveOut`, whoever saw the deed itself.
        public Aftermath(string area, string key, string said, GameTime doneAt, GameTime? mendedAt = null, IEnumerable<string> leaveOut = null)
        {
            if (string.IsNullOrEmpty(area) || string.IsNullOrEmpty(key) || string.IsNullOrEmpty(said))
                throw new ArgumentException("the damage needs an area, a key and its words");
            Area = area; Key = key; Said = said; DoneAt = doneAt;
            var mend = mendedAt ?? DefaultMend(doneAt);
            long longest = doneAt.TotalMinutes + LongestUnmendedDays * 24L * 60;
            MendedAt = mend.TotalMinutes > longest ? GameTime.FromTotalMinutes(longest) : mend;
            foreach (var p in leaveOut ?? Array.Empty<string>()) if (p != null) _leaveOut.Add(p);
            _nextHour = FloorDiv(doneAt.TotalMinutes, 60) + 1;
        }

        /// THE HOURS SINCE THE LAST CALL, up to `now` or its mending: whoever came
        /// into the area in them finds it, filed at the hour they came. Returns
        /// who found it in this call, and when.
        public List<(string who, GameTime when)> Tick(GossipMill mill, CastDay cast, GameTime now)
        {
            var found = new List<(string, GameTime)>();
            if (mill == null || cast == null) return found;
            // Each hour as it starts, up to now's own hour; only hours wholly
            // before it is mended.
            long nowM = now.TotalMinutes, mendM = MendedAt.TotalMinutes;
            var fact = new Fact(TownNews.Subject, Key, "found");
            long h = _nextHour;
            for (; h * 60 <= nowM && (h + 1) * 60 <= mendM; h++)
            {
                int day = (int)FloorDiv(h, 24), hour = (int)(h - (long)day * 24);
                foreach (var p in cast.People)
                {
                    if (_found.Contains(p) || _leaveOut.Contains(p)) continue;
                    if (cast.AreaOf(cast.PlaceOf(p, day, hour)) != Area) continue;
                    var g = mill.Get(p);
                    if (g == null) continue;
                    _found.Add(p);
                    // Heard it before coming by: they see it, and keep the one copy.
                    if (g.Rumors.Exists(r => r.Content != null && r.Content.Subject == TownNews.Subject && r.Content.Predicate == Key)) continue;
                    var at = new GameTime(day, hour, 0);
                    int memories = g.Memory.Events.Count;
                    mill.Witness(p, fact, Said, false, at, 0.9);
                    if (g.Memory.Events.Count > memories) g.Memory.Events.RemoveRange(memories, g.Memory.Events.Count - memories);
                    g.Memory.Append(new MemoryEvent(at, "observation", 0.6, MemoryOf()));
                    found.Add((p, at));
                }
            }
            if (h > _nextHour) _nextHour = h;
            return found;
        }

        /// For the save.
        public Dictionary<string, object> ToJson()
        {
            var leave = new List<object>(); foreach (var p in _leaveOut) leave.Add(p);
            var found = new List<object>(); foreach (var p in _found) found.Add(p);
            return new Dictionary<string, object>
            {
                { "area", Area }, { "key", Key }, { "said", Said }, { "done", (double)DoneAt.TotalMinutes }, { "mended", (double)MendedAt.TotalMinutes },
                { "leaveOut", leave }, { "found", found }, { "next", (double)_nextHour },
            };
        }

        /// From ToJson's values; null for anything it cannot read.
        public static Aftermath FromJson(Dictionary<string, object> saved)
        {
            if (saved == null) return null;
            string area = MiniJson.GetString(saved, "area"), key = MiniJson.GetString(saved, "key"), said = MiniJson.GetString(saved, "said");
            if (string.IsNullOrEmpty(area) || string.IsNullOrEmpty(key) || string.IsNullOrEmpty(said)) return null;
            bool ReadMinutes(string k, out long v)
            {
                v = 0;
                if (!saved.TryGetValue(k, out var o) || !(o is double d) || Math.Abs(d) > 1e8 || d != Math.Floor(d)) return false;
                v = (long)d; return true;
            }
            if (!ReadMinutes("done", out var done) || !ReadMinutes("mended", out var mended) || mended < done) return null;
            var leave = new List<string>();
            foreach (var x in MiniJson.GetList(saved, "leaveOut") ?? new List<object>()) if (x is string ls && ls.Length > 0) leave.Add(ls);
            var a = new Aftermath(area, key, said, GameTime.FromTotalMinutes(done), GameTime.FromTotalMinutes(mended), leave);
            foreach (var x in MiniJson.GetList(saved, "found") ?? new List<object>()) if (x is string fs && fs.Length > 0) a._found.Add(fs);
            // Never before the hour after the deed, never past its mending.
            if (ReadMinutes("next", out var next))
                a._nextHour = Math.Max(a._nextHour, Math.Min(next, FloorDiv(mended, 60) + 1));
            return a;
        }
    }
}
