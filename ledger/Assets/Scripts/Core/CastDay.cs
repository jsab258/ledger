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
    /// that day; and "ties", each [a, b, strength] with anything after the
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
        readonly Dictionary<string, List<(int hour, string place)>> _daily = new Dictionary<string, List<(int, string)>>();
        readonly Dictionary<string, List<(int hour, string place)>[]> _byWeekday = new Dictionary<string, List<(int, string)>[]>();
        readonly List<string> _people = new List<string>();
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
            }
            foreach (var po in MiniJson.GetList(root, "people") ?? throw new FormatException("cast file: no people"))
            {
                var p = MiniJson.AsObject(po);
                var id = MiniJson.GetString(p, "id");
                if (string.IsNullOrEmpty(id)) throw new FormatException("cast file: a person with no id");
                if (c._daily.ContainsKey(id)) throw new FormatException($"cast file: {id} twice");
                c._people.Add(id);
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

        /// Where they stand, or null when off the street or unknown.
        public (double x, double z)? Where(string id, int day, int hour)
        {
            var place = PlaceOf(id, day, hour);
            if (place == null || place == Off) return null;
            return _places[place];
        }

        /// Both on the street and within talking range: the game's own rule.
        public bool Together(string a, string b, int day, int hour)
        {
            var wa = Where(a, day, hour);
            var wb = Where(b, day, hour);
            if (wa == null || wb == null) return false;
            double dx = wa.Value.x - wb.Value.x, dz = wa.Value.z - wb.Value.z;
            return Math.Sqrt(dx * dx + dz * dz) <= TalkRangeM;
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
