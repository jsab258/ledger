using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// WHERE THE TOWN'S NAMED PEOPLE ARE, HOUR BY HOUR, AND WHO IS WITH WHOM.
    ///
    /// Canon's moat: "gossip spreads through schedule intersections". Two
    /// friends pass a story on only while they stand within talking range of
    /// each other (GossipDirector's six metres), so the routines decide who
    /// can ever hear what. The rumour-reach study of 23 September found 55 of
    /// the prototype city's 80 friendships never within range at all, because
    /// every routine had been placed by hand, one person at a time, with
    /// nobody checking the pairs (game-design/rumour-reach-2026-09-23.md).
    ///
    /// So the routines are DATA, read by one reader, and the pairs are checked:
    /// production/specs/quay-cast.json (the ten on the built street) and
    /// production/specs/hook-cast.json (every named person with a friendship,
    /// 28 September), in the same shape. The Unreal walkers are to read the
    /// same files through a port of this reader (handed to the builder), and
    /// CoreTests asserts every friendship in the file meets.
    ///
    /// THE FILE: "talk_range_m"; "places", each {x_m, z_m} in metres; "people",
    /// each with "id" and a "routine" of [hour, place] pairs, where a pair's
    /// place runs from its hour to the next pair's and the last runs round
    /// to the first, "off" meaning off the street; optionally "days", keyed by
    /// weekday ("mon" to "sun"), each a routine that replaces the daily one on
    /// that day; optionally "name", what the street calls them when canon or
    /// the street gives them one, "called", how another local speaks of them
    /// ("the dispatcher at the cab office"), "role", a note of what they do,
    /// and "keepsQuiet", for whom they keep a thing quiet when asked ("owner",
    /// "anyone", "nobody", else a friend: Silence); "namesHim": "on-trust"
    /// for somebody who keeps Tom at "the new owner" until they trust him,
    /// whatever name the game's ladder gives (Jafar, 28 September, on the 29
    /// September page: Sheila, by her own choice); and "ties", each [a, b, strength] with anything after the
    /// strength (a note of where they meet) ignored. A place a routine names
    /// that "places" does not define is refused, so a typo cannot quietly
    /// send somebody off the street.
    ///
    /// THE WEEK is Population's: day modulo 7, 0 Monday to 6 Sunday, so
    /// Saturday and Sunday are IsRestDay's days 5 and 6.
    public sealed class CastDay
    {
        public const string Off = "off";
        public static readonly string[] WeekdayKeys = { "mon", "tue", "wed", "thu", "fri", "sat", "sun" };

        public double TalkRangeM { get; private set; }
        readonly Dictionary<string, (double x, double z)> _places = new Dictionary<string, (double, double)>();
        readonly Dictionary<string, string> _said = new Dictionary<string, string>();
        readonly Dictionary<string, string> _areaOf = new Dictionary<string, string>();
        readonly Dictionary<string, List<string>> _areaNames = new Dictionary<string, List<string>>();
        readonly Dictionary<string, string> _within = new Dictionary<string, string>();
        readonly HashSet<string> _street = new HashSet<string>();
        readonly HashSet<string> _inside = new HashSet<string>();
        readonly Dictionary<string, string> _keeper = new Dictionary<string, string>();
        readonly Dictionary<string, (double open, double close)?[]> _hours = new Dictionary<string, (double, double)?[]>();
        readonly Dictionary<string, string> _hoursNote = new Dictionary<string, string>();
        readonly Dictionary<string, List<(double from, double to)>[]> _breaks = new Dictionary<string, List<(double, double)>[]>();
        readonly Dictionary<string, List<(int hour, string place)>> _daily = new Dictionary<string, List<(int, string)>>();
        readonly Dictionary<string, List<(int hour, string place)>[]> _byWeekday = new Dictionary<string, List<(int, string)>[]>();
        readonly List<string> _people = new List<string>();
        readonly Dictionary<string, string> _name = new Dictionary<string, string>();
        readonly Dictionary<string, string> _role = new Dictionary<string, string>();
        readonly Dictionary<string, string> _called = new Dictionary<string, string>();
        readonly Dictionary<string, KeepsQuietFor> _quiet = new Dictionary<string, KeepsQuietFor>();
        readonly HashSet<string> _nameOnTrust = new HashSet<string>();
        readonly Dictionary<string, string> _circle = new Dictionary<string, string>();
        readonly HashSet<string> _neverToPolice = new HashSet<string>();
        readonly List<(string a, string b, double w)> _ties = new List<(string, string, double)>();

        public IReadOnlyList<string> People => _people;
        public IReadOnlyList<(string a, string b, double w)> Ties => _ties;
        public IEnumerable<string> Places => _places.Keys;

        public static int Weekday(int day) => ((day % 7) + 7) % 7;

        /// Reads a cast file. Throws FormatException naming what is wrong.
        public static CastDay Parse(string json)
        {
            var root = MiniJson.AsObject(MiniJson.Deserialize(json));
            if (root == null) throw new FormatException("cast file: not an object");
            var c = new CastDay();
            if (!root.TryGetValue("talk_range_m", out var tr) || !(tr is double range) || !(range > 0))
                throw new FormatException("cast file: talk_range_m missing or not a positive number");
            c.TalkRangeM = range;
            var places = MiniJson.GetObject(root, "places") ?? throw new FormatException("cast file: no places");
            foreach (var kv in places)
            {
                var p = MiniJson.AsObject(kv.Value);
                if (p == null || !(p.TryGetValue("x_m", out var xo) && xo is double x) || !(p.TryGetValue("z_m", out var zo) && zo is double z))
                    throw new FormatException($"cast file: place {kv.Key} needs x_m and z_m");
                if (kv.Key == Off) throw new FormatException("cast file: 'off' is not a place");
                c._places[kv.Key] = (x, z);
                if (p.TryGetValue("said", out var so) && so is string saidWords && saidWords.Trim().Length > 0) c._said[kv.Key] = saidWords.Trim();
                if (p.TryGetValue("inside", out var io))
                {
                    if (!(io is bool inside)) throw new FormatException($"cast file: place {kv.Key}'s inside must be true or false");
                    if (inside) c._inside.Add(kv.Key);
                }
            }
            // The areas, optional: each a list of its places and the names people use.
            foreach (var kv in MiniJson.GetObject(root, "areas") ?? new Dictionary<string, object>())
            {
                var a = MiniJson.AsObject(kv.Value);
                if (MiniJson.GetString(a, "within") is string within && within.Length > 0) c._within[kv.Key] = within;
                if (a != null && a.ContainsKey("keeper"))
                {
                    if (!(a["keeper"] is string kp) || kp.Trim().Length == 0) throw new FormatException($"cast file: area {kv.Key}'s keeper must be a person's id");
                    c._keeper[kv.Key] = kp.Trim();
                }
                if (a != null && a.ContainsKey("street"))
                {
                    if (!(a["street"] is bool st)) throw new FormatException($"cast file: area {kv.Key}'s street must be true or false");
                    if (st) c._street.Add(kv.Key);
                }
                var names = new List<string>();
                foreach (var n in MiniJson.GetList(a, "names") ?? new List<object>()) if (n is string ns && ns.Trim().Length > 0) names.Add(ns.Trim());
                c._areaNames[kv.Key] = names;
                if (a != null && a.ContainsKey("hours")) c._hours[kv.Key] = ReadHours(kv.Key, a["hours"]);
                if (MiniJson.GetString(a, "hours_note") is string hn && hn.Trim().Length > 0) c._hoursNote[kv.Key] = hn.Trim();
                if (a != null && a.ContainsKey("hours_breaks"))
                {
                    if (!c._hours.TryGetValue(kv.Key, out var wk)) throw new FormatException($"cast file: area {kv.Key} has breaks but no hours");
                    c._breaks[kv.Key] = ReadBreaks(kv.Key, a["hours_breaks"], wk);
                }
                foreach (var pl in MiniJson.GetList(a, "places") ?? new List<object>())
                    if (pl is string pls)
                    {
                        if (!c._places.ContainsKey(pls)) throw new FormatException($"cast file: area {kv.Key} names a place {pls} that \"places\" does not define");
                        c._areaOf[pls] = kv.Key;
                    }
            }
            foreach (var po in MiniJson.GetList(root, "people") ?? throw new FormatException("cast file: no people"))
            {
                var p = MiniJson.AsObject(po);
                var id = MiniJson.GetString(p, "id");
                if (string.IsNullOrEmpty(id)) throw new FormatException("cast file: a person with no id");
                if (c._daily.ContainsKey(id)) throw new FormatException($"cast file: {id} twice");
                c._people.Add(id);
                if (MiniJson.GetString(p, "name") is string nm && nm.Trim().Length > 0) c._name[id] = nm.Trim();
                if (MiniJson.GetString(p, "role") is string rl && rl.Trim().Length > 0) c._role[id] = rl.Trim();
                if (MiniJson.GetString(p, "called") is string cl && cl.Trim().Length > 0) c._called[id] = cl.Trim();
                if (p.ContainsKey("keepsQuiet"))
                {
                    // Only the words it knows: a typo was read as a friend's silence, so
                    // Mickey's own reported again (the independent check of 1 October).
                    if (!(p["keepsQuiet"] is string kq) || !(kq.Trim() == "owner" || kq.Trim() == "anyone" || kq.Trim() == "nobody" || kq.Trim() == "friend"))
                        throw new FormatException("person " + id + ": keepsQuiet must be \"owner\", \"anyone\", \"nobody\" or \"friend\"");
                    c._quiet[id] = Silence.Parse(kq.Trim());
                }
                if (p.ContainsKey("police"))
                {
                    if (!(p["police"] is string pol) || pol != "never")
                        throw new FormatException($"cast file: {id}'s police must be \"never\" or absent");
                    c._neverToPolice.Add(id);
                }
                if (p.ContainsKey("circle"))
                {
                    if (!(p["circle"] is string cr) || (cr != "day" && cr != "night" && cr != "both"))
                        throw new FormatException($"cast file: {id}'s circle must be \"day\", \"night\" or \"both\"");
                    c._circle[id] = cr;
                }
                if (p.ContainsKey("namesHim"))
                {
                    if (!(p["namesHim"] is string nh) || nh.Trim() != "on-trust")
                        throw new FormatException($"cast file: {id}'s namesHim must be \"on-trust\" or absent");
                    c._nameOnTrust.Add(id);
                }
                c._daily[id] = c.ReadRoutine(id, MiniJson.GetList(p, "routine"));
                if (p.ContainsKey("days") && !(p["days"] is Dictionary<string, object>))
                    throw new FormatException($"cast file: {id}'s days must be an object keyed mon to sun");
                var days = MiniJson.GetObject(p, "days");
                if (days != null)
                {
                    var week = new List<(int, string)>[7];
                    foreach (var kv in days)
                    {
                        int wd = Array.IndexOf(WeekdayKeys, kv.Key);
                        if (wd < 0) throw new FormatException($"cast file: {id} has a day '{kv.Key}' (mon to sun)");
                        week[wd] = c.ReadRoutine(id + "." + kv.Key, MiniJson.AsList(kv.Value));
                    }
                    c._byWeekday[id] = week;
                }
            }
            if (root.ContainsKey("ties") && !(root["ties"] is List<object>))
                throw new FormatException("cast file: ties must be a list");
            var seen = new HashSet<string>();
            foreach (var to in MiniJson.GetList(root, "ties") ?? new List<object>())
            {
                var t = MiniJson.AsList(to);
                if (t == null || t.Count < 3 || !(t[0] is string a) || !(t[1] is string b) || !(t[2] is double w))
                    throw new FormatException("cast file: a tie that is not [a, b, strength]");
                if (!c._daily.ContainsKey(a) || !c._daily.ContainsKey(b))
                    throw new FormatException($"cast file: tie {a}-{b} names somebody who is not in the cast");
                if (a == b) throw new FormatException($"cast file: {a} is tied to themselves");
                if (!(w > 0.0 && w <= 1.0)) throw new FormatException($"cast file: tie {a}-{b} has strength {w}, not in (0, 1]");
                string key = string.CompareOrdinal(a, b) < 0 ? a + "|" + b : b + "|" + a;
                if (!seen.Add(key)) throw new FormatException($"cast file: tie {a}-{b} twice");
                c._ties.Add((a, b, w));
            }
            foreach (var kv in c._keeper)
                if (!c._daily.ContainsKey(kv.Value)) throw new FormatException($"cast file: area {kv.Key}'s keeper {kv.Value} is not in the cast");
            return c;
        }

        /// A SMALL TOWN'S RULE for how often friends meet: an authoring rule,
        /// not a finding, since no measured figures were found
        /// (production/research/small-town-meetings): a friendship of 0.6 or
        /// stronger on at least five days a week, 0.45 to 0.55 on three,
        /// weaker ones on one. CoreTests holds hook-cast.json to it and
        /// ledger/TownReach prints it.
        internal static int FriendsMeetDays(double tie) => tie >= 0.6 ? 5 : tie >= 0.45 ? 3 : 1;

        List<(int hour, string place)> ReadRoutine(string who, List<object> steps)
        {
            if (steps == null || steps.Count == 0) throw new FormatException($"cast file: {who} has no routine");
            var r = new List<(int, string)>();
            foreach (var so in steps)
            {
                var s = MiniJson.AsList(so);
                if (s == null || s.Count < 2 || !(s[0] is double h) || !(s[1] is string place))
                    throw new FormatException($"cast file: {who} has a step that is not [hour, place]");
                if (h < 0 || h > 23 || h != Math.Floor(h)) throw new FormatException($"cast file: {who} has hour {h}");
                if (place != Off && !_places.ContainsKey(place))
                    throw new FormatException($"cast file: {who} goes to '{place}', which is not a place in the file");
                r.Add(((int)h, place));
            }
            r.Sort((x, y) => x.Item1.CompareTo(y.Item1));
            for (int i = 1; i < r.Count; i++)
                if (r[i].Item1 == r[i - 1].Item1) throw new FormatException($"cast file: {who} is in two places at {r[i].Item1}:00");
            return r;
        }

        /// The place somebody is at on this game day and hour, "off" when off
        /// the street, or null for somebody not in the cast.
        public string PlaceOf(string id, int day, int hour)
        {
            if (id == null || !_daily.TryGetValue(id, out var routine)) return null;
            if (_byWeekday.TryGetValue(id, out var week) && week[Weekday(day)] != null) routine = week[Weekday(day)];
            int h = ((hour % 24) + 24) % 24;
            string place = routine[routine.Count - 1].place;
            foreach (var (from, pl) in routine) if (from <= h) place = pl;
            return place;
        }

        /// THE AREA A PLACE BELONGS TO, as people say it (town list 6ac): the fish
        /// market's counter and its pavement are both "the fish market", so a
        /// true answer about where somebody was is never read as a lie. Null
        /// when the file gives the place no area.
        public string AreaOf(string place) => place != null && _areaOf.TryGetValue(place, out var a) ? a : null;

        /// Who keeps a place (the file's "keeper": Rita keeps Rita's), or null.
        public string KeeperOf(string area) => area != null && _keeper.TryGetValue(area, out var k) ? k : null;

        /// WHETHER SOMEBODY IS ON QUAY STREET at an hour: their place then is in
        /// one of the areas the file marks "street" (Mickey's, the fish market,
        /// Rita's, the kiosk, the laundry, the quay at its foot, Ada's step, the
        /// cafe, the newsagent's, Hal's, the bus stop), not the docks, the chapel,
        /// the landing or anywhere else in the Hook, and not at home (the
        /// independent review of 30 September, A11: DS Ellis "on Quay Street"
        /// stopped people at the chapel and the landing). A file that marks no
        /// area (a test's small street) counts anybody not at home.
        public bool OnQuayStreet(string id, int day, int hour)
        {
            var place = PlaceOf(id, day, hour) ?? Off;
            if (place == Off) return false;
            return _street.Count == 0 || (AreaOf(place) is string a && _street.Contains(a));
        }

        // An area's hours: each weekday it opens, [open, close] in whole or half
        // hours from that day's midnight, a close past 24 into the next morning
        // but never round to the next day's opening; a weekday left out is shut.
        static (double open, double close)?[] ReadHours(string area, object value)
        {
            var o = MiniJson.AsObject(value) ?? throw new FormatException($"cast file: area {area}'s hours must be an object of weekdays");
            if (o.Count == 0) throw new FormatException($"cast file: area {area}'s hours name no weekday; leave hours out for a place with none");
            var week = new (double open, double close)?[7];
            foreach (var kv in o)
            {
                int wd = Array.IndexOf(WeekdayKeys, kv.Key);
                if (wd < 0) throw new FormatException($"cast file: area {area}'s hours name no weekday: {kv.Key}");
                if (!(kv.Value is List<object> pair) || pair.Count != 2 || !(pair[0] is double open) || !(pair[1] is double close)
                    || open < 0 || open >= 24 || close <= open || close > 30 || close - open > 24 || open * 2 != Math.Floor(open * 2) || close * 2 != Math.Floor(close * 2))
                    throw new FormatException($"cast file: area {area}'s hours on {kv.Key} must be [open, close], whole or half hours, open before 24 and close after it, by six the next morning at the latest");
                week[wd] = (open, close);
            }
            // A close past midnight must not run into the next day's opening.
            for (int wd = 0; wd < 7; wd++)
                if (week[wd].HasValue && week[(wd + 1) % 7].HasValue && week[wd].Value.close - 24 > week[(wd + 1) % 7].Value.open)
                    throw new FormatException($"cast file: area {area}'s hours on {WeekdayKeys[wd]} run past the next day's opening");
            return week;
        }

        // An area's breaks (town list 6by): on a weekday, [from, to], or a list
        // of them, in whole or half hours strictly inside that day's hours, when
        // it is shut because whoever keeps it is elsewhere (Hal on Mondays at
        // Rita's); never overlapping.
        static List<(double from, double to)>[] ReadBreaks(string area, object value, (double open, double close)?[] week)
        {
            var o = MiniJson.AsObject(value) ?? throw new FormatException($"cast file: area {area}'s hours_breaks must be an object of weekdays");
            var breaks = new List<(double from, double to)>[7];
            foreach (var kv in o)
            {
                int wd = Array.IndexOf(WeekdayKeys, kv.Key);
                if (wd < 0) throw new FormatException($"cast file: area {area}'s hours_breaks name no weekday: {kv.Key}");
                var list = kv.Value as List<object>;
                var pairs = list != null && list.Count > 0 && list[0] is List<object> ? list : new List<object> { kv.Value };
                var day = new List<(double from, double to)>();
                foreach (var x in pairs)
                {
                    if (!(x is List<object> pair) || pair.Count != 2 || !(pair[0] is double from) || !(pair[1] is double to)
                        || to <= from || from * 2 != Math.Floor(from * 2) || to * 2 != Math.Floor(to * 2)
                        || !week[wd].HasValue || from <= week[wd].Value.open || to >= week[wd].Value.close
                        || day.Exists(b => from < b.to && b.from < to))
                        throw new FormatException($"cast file: area {area}'s breaks on {kv.Key} must be [from, to], whole or half hours, strictly inside that day's hours, never overlapping");
                    day.Add((from, to));
                }
                day.Sort((a, b) => a.from.CompareTo(b.from));
                breaks[wd] = day;
            }
            return breaks;
        }

        /// OPEN AND CLOSED (town list 6bo): whether a place or area is open at
        /// this hour and minute of this day, its hours from the cast file (a
        /// close past midnight counts on the next morning); null when it has no
        /// hours, being no shop (the quay, the flats, the chapel).
        public bool? OpenAt(string placeOrArea, int day, int hour, int minute = 0)
        {
            var area = AreaFor(placeOrArea);
            if (area == null || !_hours.TryGetValue(area, out var week)) return null;
            // The hour and minute wrapped into the day, as PlaceOf wraps them.
            long all = ((long)day * 24 + hour) * 60 + minute;
            long d0 = all >= 0 ? all / 1440 : -((-all + 1439) / 1440);
            day = (int)d0;
            double t = (all - d0 * 1440) / 60.0;
            _breaks.TryGetValue(area, out var breaks);
            bool InBreak(int wd, double at) => breaks != null && breaks[wd] != null && breaks[wd].Exists(b => b.from <= at && at < b.to);
            var today = week[Weekday(day)];
            if (today.HasValue && today.Value.open <= t && t < today.Value.close) return !InBreak(Weekday(day), t);
            var before = week[Weekday(day - 1)];
            if (before.HasValue && t + 24 < before.Value.close) return !InBreak(Weekday(day - 1), t + 24);
            return false;
        }

        static readonly string[] Numbers = { "twelve", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven" };
        static readonly string[] DayNames = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };

        // A time as a local says it: "half five", "three in the morning".
        static string TimeWords(double t, bool closing)
        {
            int h = (int)Math.Floor(t);
            bool half = t - h >= 0.5;
            string said = (half ? "half " : "") + Numbers[h % 12];
            if (!half && h % 24 == 0) return "midnight";
            if (closing ? (t > 24 || t <= 7) : t < 7) return said + " in the morning";
            if (!closing && t >= 18) return said + " in the evening";
            if (closing && t >= 20) return said + " at night";
            return said;
        }

        // Weekdays as a local says them: "Monday to Friday", "Tuesdays and Fridays".
        static string DaysWords(List<int> days)
        {
            days.Sort();
            bool run = days.Count >= 3 && days[days.Count - 1] - days[0] == days.Count - 1;
            if (run) return DayNames[days[0]] + " to " + DayNames[days[days.Count - 1]];
            var names = days.ConvertAll(d => DayNames[d] + "s");
            return names.Count == 1 ? names[0] : string.Join(", ", names.GetRange(0, names.Count - 1)) + " and " + names[names.Count - 1];
        }

        /// AN AREA'S HOURS AS PEOPLE SAY THEM (town list 6bo): its usual hours,
        /// the days that differ, and the days it is shut, each said in full
        /// ("nine till half five, on Wednesdays it shuts at one, shut on
        /// Sundays"), since the claim check's second look did not read "Wednesdays
        /// till one" as shutting at one; a place open three days or fewer by its
        /// days ("Tuesdays, Fridays and Saturdays, eight till four"). Null when
        /// it has no hours.
        public string HoursWords(string area)
        {
            if (area == null || !_hours.TryGetValue(area, out var week)) return null;
            var groups = new List<((double open, double close) h, List<int> days)>();
            var shut = new List<int>();
            for (int d = 0; d < 7; d++)
            {
                if (!week[d].HasValue) { shut.Add(d); continue; }
                var h = week[d].Value;
                int g = groups.FindIndex(x => x.h == h);
                if (g < 0) groups.Add((h, new List<int> { d }));
                else groups[g].days.Add(d);
            }
            string Span((double open, double close) h) => h.open == 0 && h.close == 24 ? "day and night" : TimeWords(h.open, false) + " till " + TimeWords(h.close, true);
            var bits = new List<string>();
            if (7 - shut.Count <= 3)
                foreach (var (h, days) in groups) bits.Add(DaysWords(days) + ", " + Span(h));
            else if (groups.Count > 0)
            {
                // The usual hours: the most days, the earliest first.
                int u = 0;
                for (int i = 1; i < groups.Count; i++) if (groups[i].days.Count > groups[u].days.Count) u = i;
                var usual = groups[u].h;
                bits.Add(Span(usual) + (groups.Count == 1 && shut.Count == 0 ? " every day" : ""));
                for (int i = 0; i < groups.Count; i++)
                {
                    if (i == u) continue;
                    var (h, days) = groups[i];
                    bits.Add("on " + DaysWords(days) + (h.close == usual.close ? " it opens at " + TimeWords(h.open, false)
                                                     : h.open == usual.open ? " it shuts at " + TimeWords(h.close, true)
                                                     : " " + Span(h)));
                }
                if (_breaks.TryGetValue(area, out var breaks))
                {
                    var byBreak = new List<(string said, List<int> days)>();
                    for (int d = 0; d < 7; d++)
                    {
                        if (breaks[d] == null || breaks[d].Count == 0) continue;
                        string said = string.Join(" and ", breaks[d].ConvertAll(b => "from " + TimeWords(b.from, true) + " till " + TimeWords(b.to, false)));
                        int g = byBreak.FindIndex(x => x.said == said);
                        if (g < 0) byBreak.Add((said, new List<int> { d })); else byBreak[g].days.Add(d);
                    }
                    foreach (var (said, days) in byBreak)
                        bits.Add("on " + DaysWords(days) + " shut " + said);
                }
                if (shut.Count > 0) bits.Add("shut on " + DaysWords(shut));
            }
            if (_hoursNote.TryGetValue(area, out var note)) bits.Add(note);
            return string.Join(", ", bits);
        }

        /// What people call an area, the first way first ("the fish market").
        public IReadOnlyList<string> AreaNames(string area) =>
            area != null && _areaNames.TryGetValue(area, out var n) ? n : (IReadOnlyList<string>)new List<string>();

        /// Every spoken name to the areas it can mean, as Claims.WhereHeSays reads
        /// a line: lower case, without apostrophes or a leading "the". A name can
        /// mean more than one ("the fish market": the shop and the fish dock), and
        /// an area's names cover the areas within it ("the docks": the fish dock,
        /// customs, the repair yard), so a true answer is never read as a lie.
        public Dictionary<string, HashSet<string>> SpokenAreas()
        {
            var d = new Dictionary<string, HashSet<string>>();
            foreach (var kv in _areaNames)
                foreach (var name in kv.Value)
                {
                    var k = SpokenKey(name);
                    if (k.Length == 0) continue;
                    if (!d.TryGetValue(k, out var set)) d[k] = set = new HashSet<string>();
                    set.Add(kv.Key);
                    foreach (var w in _within) if (w.Value == kv.Key) set.Add(w.Key);
                }
            return d;
        }

        /// Whether an area he named fits the area he was seen in: the same, or
        /// one within the other either way (the fish dock is on the docks).
        public bool Fits(string named, string seen) =>
            named != null && seen != null && (named == seen
                || (_within.TryGetValue(seen, out var w1) && w1 == named)
                || (_within.TryGetValue(named, out var w2) && w2 == seen));

        /// A known place or area id, as the area it is in; null for anything else.
        public string AreaFor(string placeOrArea) =>
            placeOrArea == null ? null : AreaOf(placeOrArea) ?? (_areaNames.ContainsKey(placeOrArea) ? placeOrArea : null);

        /// A name as Claims reads it: lower case, no apostrophes, no leading "the".
        public static string SpokenKey(string name)
        {
            var k = (name ?? "").ToLowerInvariant().Replace("'", "").Replace("\u2019", "").Trim();
            return k.StartsWith("the ") ? k.Substring(4) : k;
        }

        /// THE PLACE IN PLAIN WORDS, as a person there would say where they are
        /// ("the pavement outside the fish market"), from the file's "said"; null
        /// when it has none (town list 6u: each person's own place in their talk).
        public string SaidOf(string place) => place != null && _said.TryGetValue(place, out var w) ? w : null;

        /// Where somebody is this hour, in plain words, or null when off the street or unknown.
        public string WhereWords(string id, int day, int hour) => SaidOf(PlaceOf(id, day, hour));

        /// Where they stand, or null when off the street or unknown.
        public (double x, double z)? Where(string id, int day, int hour)
        {
            var place = PlaceOf(id, day, hour);
            if (place == null || place == Off) return null;
            return _places[place];
        }

        /// Whether a place is inside a building (the file's "inside": the office,
        /// the counters, the cafe), where a wall stands between it and the next.
        public bool IsInside(string place) => place != null && _inside.Contains(place);

        /// Both on the street and within talking range, and in the same area or
        /// both out on the pavement: never through a wall (the independent review
        /// of 30 September, D: Mickey's office and the fish counter, 6.0 m apart,
        /// gossiped as if together).
        public bool Together(string a, string b, int day, int hour)
        {
            var wa = Where(a, day, hour);
            var wb = Where(b, day, hour);
            if (wa == null || wb == null) return false;
            double dx = wa.Value.x - wb.Value.x, dz = wa.Value.z - wb.Value.z;
            if (Math.Sqrt(dx * dx + dz * dz) > TalkRangeM) return false;
            string pa = PlaceOf(a, day, hour), pb = PlaceOf(b, day, hour);
            return AreaOf(pa) == AreaOf(pb) && AreaOf(pa) != null || (!IsInside(pa) && !IsInside(pb));
        }

        /// WHAT THE STREET CALLS SOMEBODY (town list 6ad): the name canon or the
        /// street gives them ("Ron Kirby", "Rita"), or null for somebody known
        /// only by what they do.
        public string NameOf(string id) => id != null && _name.TryGetValue(id, out var n) ? n : null;

        /// What they do, as a neighbour would put it: the file's role without the
        /// name before its colon or its "(canon)" mark ("Mickey's door and rank").
        public string RoleOf(string id)
        {
            if (id == null || !_role.TryGetValue(id, out var r)) return null;
            r = r.Replace("(canon)", " ");
            int colon = r.IndexOf(':');
            if (colon >= 0 && NameOf(id) != null) r = r.Substring(colon + 1);
            return System.Text.RegularExpressions.Regex.Replace(r, @"\s+", " ").Trim(' ', ',', ';');
        }

        /// For whom somebody keeps a thing quiet when asked (town list 6al): the
        /// file's "keepsQuiet", else a friend.
        public KeepsQuietFor QuietStance(string id) => id != null && _quiet.TryGetValue(id, out var q) ? q : KeepsQuietFor.Friend;

        /// Whether somebody calls Tom by name only once they trust him (the
        /// file's "namesHim"): until then "the new owner", whatever the game's
        /// ladder sends (Jafar, on the 29 September page: Sheila is the exception by
        /// her own choice, as she promised Mickey to size him up).
        public bool NamesHimOnlyOnTrust(string id) => id != null && _nameOnTrust.Contains(id);

        /// Whether somebody never goes to the police, whatever they saw or
        /// suffered: their trade keeps them from it (the file's "police": "never",
        /// town list 6bj), or they are Mickey's own people (the file's keepsQuiet
        /// "owner": Ron and Sheila), who never go to the police about one of their
        /// own, ever, and handle what they saw privately (Jafar's ruling of 1
        /// October, on the independent review's N4). Read by PoliceFile.WouldReport
        /// and HearTheStreet.
        public bool NeverToPolice(string id) => id != null && (_neverToPolice.Contains(id) || MickeysOwn(id));

        /// MICKEY'S OWN PEOPLE (the file's keepsQuiet "owner": Ron and Sheila), his
        /// inherited loyalists: they never go to the police about him and handle
        /// what they saw privately (Jafar's ruling of 1 October; GossipMill.
        /// KeepsHisDeedsFor).
        public bool MickeysOwn(string id) => id != null && _quiet.TryGetValue(id, out var q) && q == KeepsQuietFor.Owner;

        /// Which of his worlds somebody belongs to, for the gossip (Gossiper.Circle):
        /// the file's "circle", else "day", the town he lives among by day
        /// (town list 6ar: the outfit's man is his night world's).
        public string CircleOf(string id) => id != null && _circle.TryGetValue(id, out var c) ? c : "day";

        // The street's words for the named people, beside their names (town list 6bd).
        static readonly Dictionary<string, string[]> RoleWords = new Dictionary<string, string[]>
        {
            { "lena", new[] { "the bookkeeper" } },
            { "noor", new[] { "the reporter", "the journalist" } },
            { "emil", new[] { "the priest", "the Father" } },
            { "ada", new[] { "the widow" } },
            { "sam", new[] { "the hustler" } },
            { "rita", new[] { "the pawnbroker" } },
            { "june", new[] { "Mickey's daughter" } },
            { "zlata", new[] { "the dispatcher" } },
        };

        /// WHOM A TYPED LINE NAMES (town list 6bd, the fourth sweep): the cast ids
        /// of the people it names by name, first name or surname ("Sheila", "Dunn",
        /// "Father Walsh"), or by the street's word for a named person ("the
        /// bookkeeper"), for the session record's `named` line, never the words.
        /// A name that is a place's ("at Rita's", "Hal's") is the place, not them.
        public List<string> WhoNamed(string line)
        {
            var ids = new List<string>();
            if (string.IsNullOrWhiteSpace(line)) return ids;
            string text = line.Replace('\u2019', '\'');
            var places = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
            foreach (var kv in _areaNames) foreach (var n in kv.Value) places.Add(n.Replace('\u2019', '\''));
            foreach (var id in _people)
            {
                var forms = new List<string>();
                if (_name.TryGetValue(id, out var full))
                {
                    forms.Add(full);
                    var parts = full.Split(' ');
                    foreach (var part in parts) if (part.Length > 2 && part != "Father") forms.Add(part);
                }
                if (RoleWords.TryGetValue(id, out var roles)) forms.AddRange(roles);
                foreach (var form in forms)
                {
                    bool role = form.StartsWith("the ", StringComparison.Ordinal) || form.Contains(" ");
                    var rx = new System.Text.RegularExpressions.Regex(@"(?<![\w'])" + System.Text.RegularExpressions.Regex.Escape(form) + @"(?![\w-])" + (role ? "" : @"(?!'s\b)"),
                        role ? System.Text.RegularExpressions.RegexOptions.IgnoreCase : System.Text.RegularExpressions.RegexOptions.None);
                    bool hit = false;
                    foreach (System.Text.RegularExpressions.Match m in rx.Matches(text)) { hit = true; break; }
                    // "Kirby's" is him; "Rita's" is the pawn when the street names a place so.
                    if (!hit && !role)
                    {
                        var poss = new System.Text.RegularExpressions.Regex(@"(?<![\w'])" + System.Text.RegularExpressions.Regex.Escape(form) + @"'s\b");
                        if (poss.IsMatch(text) && !places.Contains(form + "'s")) hit = true;
                    }
                    if (hit) { if (!ids.Contains(id)) ids.Add(id); break; }
                }
            }
            return ids;
        }

        /// Somebody as another person speaks of them in passing: by name, or as
        /// the street describes them.
        public string Called(string id) => NameOf(id) ?? Described(id);

        /// Somebody as another local would describe them: the file's "called"
        /// ("Ron Kirby, who keeps Mickey's door and the rank"), else their name
        /// and role.
        public string Described(string id)
        {
            if (id != null && _called.TryGetValue(id, out var c)) return c;
            var n = NameOf(id); var r = RoleOf(id);
            return n != null ? (r != null ? n + ", " + r : n) : (r ?? id);
        }

        /// The most friends a person is told of besides the named people and
        /// their close friends, strongest first (the prompt's length is paid
        /// each turn).
        public const int MostKnown = 12;

        static readonly (string part, int from, int to)[] PartsOfDay = { ("mornings", 7, 12), ("afternoons", 12, 17), ("evenings", 17, 23), ("nights", 23, 30) };

        /// WHERE SOMEBODY USUALLY IS, as a friend would know it: for each part of
        /// the day, the area they are in for at least half of its hours across the
        /// week, parts in the same area run together ("Rita's in the mornings and
        /// afternoons", "the chapel most of the day"). Null when they have no
        /// usual place on the street (Darren on his rounds).
        public string UsualWords(string id)
        {
            if (id == null || !_daily.ContainsKey(id)) return null;
            var usual = new List<(string part, string area)>();
            foreach (var (part, from, to) in PartsOfDay)
            {
                var count = new Dictionary<string, int>();
                int all = 0;
                for (int d = 0; d < 7; d++)
                    for (int h = from; h < to; h++)
                    {
                        all++;
                        var pl = PlaceOf(id, h >= 24 ? d + 1 : d, h % 24);
                        var ar = pl == Off ? null : AreaOf(pl) ?? pl;
                        if (ar != null) count[ar] = count.TryGetValue(ar, out var c) ? c + 1 : 1;
                    }
                string best = null; int bestN = 0;
                foreach (var kv in count)
                    if (kv.Value > bestN || (kv.Value == bestN && string.CompareOrdinal(kv.Key, best) < 0)) { best = kv.Key; bestN = kv.Value; }
                if (best != null && bestN * 2 >= all) usual.Add((part, best));
            }
            if (usual.Count == 0) return null;
            var bits = new List<string>();
            for (int i = 0; i < usual.Count;)
            {
                int j = i;
                var parts = new List<string>();
                while (j < usual.Count && usual[j].area == usual[i].area) { parts.Add(usual[j].part); j++; }
                var names = AreaNames(usual[i].area);
                string where = names.Count > 0 ? names[0] : usual[i].area;
                bool nights = parts.Remove("nights");
                bits.Add(parts.Count == 0 ? where + " at night"
                    : parts.Count == 3 ? where + (nights ? " day and night" : " most of the day")
                    : where + " in the " + string.Join(" and ", parts) + (nights ? " and at night" : ""));
                i = j;
            }
            return string.Join(", ", bits);
        }

        /// WHO SOMEBODY KNOWS, AND WHERE (town list 6ad): with no map, asking a
        /// local is the way round, and nobody could say where a friend usually
        /// is. Everybody in the named cast has heard of the named people (thirty
        /// to fifty authored residents sit inside one person's circle:
        /// production/research/small-town-networks); their friends they know by
        /// where they usually are; whoever is with them now they can see; and the
        /// street's places they can name. Lines for their talk, each a thing the
        /// claim check lets them say (its P items). Empty for somebody not in the
        /// cast. `present`, when the game sends it, is who is really with them
        /// (cast ids), in place of the routines' guess.
        public List<string> PeopleFor(string id, int day, int hour, IEnumerable<string> present = null)
        {
            var lines = new List<string>();
            if (id == null || !_daily.ContainsKey(id)) return lines;
            var listed = new HashSet<string> { id };
            var friends = new List<(string who, double w)>();
            foreach (var (a, b, w) in _ties)
            {
                if (a == id) friends.Add((b, w));
                else if (b == id) friends.Add((a, w));
            }
            friends.Sort((x, y) => x.w != y.w ? y.w.CompareTo(x.w) : string.CompareOrdinal(x.who, y.who));
            // The named people and close friends always; other friends, strongest
            // first, up to twelve in all besides the named.
            int weakRoom = MostKnown;
            foreach (var (who, w) in friends) if (w >= 0.6 && NameOf(who) == null) weakRoom--;
            foreach (var (who, w) in friends)
            {
                bool close = w >= 0.6;
                if (!close && NameOf(who) == null && weakRoom-- <= 0) continue;
                listed.Add(who);
                var usual = UsualWords(who);
                lines.Add(Described(who) + (close ? "; you know each other well" : "; you know each other a little") + (usual != null ? "; usually at " + usual : "") + ".");
            }
            foreach (var who in _people)
                if (!listed.Contains(who) && NameOf(who) != null)
                {
                    listed.Add(who);
                    lines.Add(Described(who) + "; everybody on the street knows who that is.");
                }
            var here = new List<string>();
            if (present != null)
            {
                var seenIds = new HashSet<string>();
                foreach (var who in present)
                    if (who != id && who != null && _daily.ContainsKey(who) && seenIds.Add(who)) here.Add(Called(who));
            }
            else
            {
                // The routines' guess: within talking range and in the same area,
                // so the counters either side of a wall are not together (the
                // independent check: Mickey's and the fish market's, 6.0 m apart).
                string myArea = AreaOf(PlaceOf(id, day, hour));
                foreach (var who in _people)
                    if (who != id && myArea != null && AreaOf(PlaceOf(who, day, hour)) == myArea && Together(id, who, day, hour)) here.Add(Called(who));
            }
            if (here.Count > 0) lines.Add("Here with you now: " + string.Join("; ", here) + ".");
            var places = new List<string>();
            foreach (var kv in _areaNames) if (kv.Value.Count > 0 && !_within.ContainsKey(kv.Key)) places.Add(kv.Value[0]);
            if (places.Count > 0) lines.Add("The street's places, as people call them: " + string.Join(", ", places) + ".");
            return lines;
        }

        /// THE STREET'S OPENING HOURS AS EVERYBODY KNOWS THEM (town list 6bo):
        /// every shop's hours and whether it is open at this hour and minute,
        /// one line for anybody's talk (ConversationEngine.StreetHours) and the
        /// claim check's O item; null when no area has hours.
        public string HoursFor(int day, int hour, int minute = 0)
        {
            var hours = new List<string>();
            foreach (var kv in _areaNames)
                if (_hours.ContainsKey(kv.Key))
                {
                    string name = kv.Value.Count > 0 ? kv.Value[0] : kv.Key;
                    hours.Add(char.ToUpperInvariant(name[0]) + name.Substring(1) + ": " + HoursWords(kv.Key) + "; " + (OpenAt(kv.Key, day, hour, minute) == true ? "open now." : "shut now."));
                }
            return hours.Count > 0 ? "Opening hours, as everybody on the street knows them. " + string.Join(" ", hours) : null;
        }

        /// Hours a week the two are together, over one whole week.
        public int HoursTogetherPerWeek(string a, string b)
        {
            int n = 0;
            for (int d = 0; d < 7; d++)
                for (int h = 0; h < 24; h++)
                    if (Together(a, b, d, h)) n++;
            return n;
        }

        /// Days of the week on which the two are together at least an hour.
        public int DaysTogetherPerWeek(string a, string b)
        {
            int n = 0;
            for (int d = 0; d < 7; d++)
                for (int h = 0; h < 24; h++)
                    if (Together(a, b, d, h)) { n++; break; }
            return n;
        }
    }
}
