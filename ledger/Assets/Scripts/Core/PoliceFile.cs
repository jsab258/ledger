using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// What was done, as the law of 1990 grades it.
    public enum Offence
    {
        /// Something seen that is no crime on its face: a man with an envelope at the landing.
        Suspicious,
        /// Criminal damage: a shop window put in (a magistrates' matter under two thousand pounds).
        Damage,
        /// A common assault.
        Assault,
        /// A wounding.
        Wounding,
        /// A robbery.
        Robbery,
        /// A killing.
        Killing,
    }

    /// How the police came to hold something.
    public enum Known
    {
        /// The street's talk, reaching her on her enquiries: grounds to ask, never to charge.
        Talk,
        /// A statement from somebody who saw it, but could not say who.
        Description,
        /// A statement from somebody who saw it and names him, and will sign it.
        Statement,
    }

    /// WHO TELLS THE POLICE, WHAT THE POLICE DO, WHEN DS ELLIS COMES AND WHAT SHE
    /// CAN PUT TO HIM (town list 6ar; the checklist's K7, A15.09 and A15.11; the
    /// first hour Jafar approved, whose days 4 and 5 have her turn up on Quay
    /// Street if the street has got loud about him). From the research
    /// (production/research/police-response-1990), made deterministic from who
    /// each person is:
    ///   - most offences are never reported; a victim reports far more than a
    ///     witness, a shopkeeper reports damage for the insurance, and violence
    ///     between people who know each other is mostly settled privately;
    ///   - the response is proportionate: damage brings a uniformed constable and
    ///     a crime report, not a detective; a detective walks the street only
    ///     after a wounding, a robbery or, above all, a killing;
    ///   - the law let an officer arrest on reasonable suspicion, talk included,
    ///     but a charge needs somebody who saw it, names him and will sign; she
    ///     waits for that before she arrests (a choice of the game's, so that
    ///     talk alone never takes him).
    /// Ellis is already on the warehouse fire (the outline's Act I), so her
    /// enquiries bring her through the Hook: she comes to Quay Street for a body,
    /// for a crime a detective takes once reported, and, from the first hour's
    /// day 4, for the street's talk once it is loud. The street always knows
    /// more than she does. Who reports is decided by each person's nerve and
    /// loyalty; the cast file gives nobody their own yet (town list 6bj: moving
    /// the town off the middle values moves bribes, debts, company and more,
    /// so the scope is Jafar's), so at the defaults no witness reports unless
    /// the story cools them on him (Ada stood up for her tea).
    public sealed class PoliceFile
    {
        /// How many people of his day world must be passing talk of his nights
        /// round for her to come for it (Loudness). Measured against the first
        /// hour (TownReach --loud, 29 September): whether the talk gets this
        /// loud by days 4 and 5 depends on who saw him, since only somebody who
        /// meets many people spreads it far; the figures by witness are in
        /// game-design/ellis-2026-09-29.md, and the number is his to confirm.
        public const int LoudAt = 3;

        /// The first day (index) she can come for talk alone: the first hour's
        /// day 4, when her enquiries on the fire have had time to pick it up.
        public const int TalkNoSoonerThan = 3;

        public sealed class Entry
        {
            public string Who;        // the person the police heard it from (a cast id)
            public string Topic;      // the deed's topic key
            public Offence Offence;
            public Known How;
            public int Day;
        }

        readonly List<Entry> _entries = new List<Entry>();
        public IReadOnlyList<Entry> Entries => _entries;

        /// Every visit of hers to Quay Street: the day and why ("talk", "body",
        /// or a reported crime's offence and topic).
        readonly List<(int day, string why)> _visits = new List<(int, string)>();
        public IReadOnlyList<(int day, string why)> Visits => _visits;
        public int EllisCameOn => _visits.Count > 0 ? _visits[0].day : -1;

        readonly List<(int day, string topic)> _calls = new List<(int, string)>();
        /// The days a constable called to take him in, and for which deed.
        public IReadOnlyList<(int day, string topic)> ConstableCalls => _calls;

        /// WHETHER A CONSTABLE CALLS TODAY TO TAKE HIM IN (town list 6bp): a
        /// window is the constable's, not the detective's, so on a statement
        /// naming him he calls the day after it was given; each deed once, one a
        /// call (the game calls it until it returns null). The deed's topic, or
        /// null. The game takes him where he is found (Custody.Take); for a
        /// detective's crime she takes him on her visit (CanArrest).
        public string ConstableComes(int day)
        {
            // One call a day (the independent check: two windows took him twice
            // in one morning); the next deed waits for the next morning.
            if (_calls.Exists(c => c.day == day)) return null;
            foreach (var e in _entries)
                if (e.Offence == Offence.Damage && e.How == Known.Statement && e.Day < day && !_calls.Exists(c => c.topic == e.Topic) && !WasTaken(e.Topic))
                {
                    _calls.Add((day, e.Topic));
                    return e.Topic;
                }
            return null;
        }

        readonly List<(string topic, long outMinute)> _taken = new List<(string, long)>();

        /// Whether he has been taken in for this deed.
        public bool WasTaken(string topic) => _taken.Exists(t => t.topic == topic);

        /// HE IS TAKEN IN for a deed the police can arrest him for (CanArrest),
        /// by the constable who calls for it or by DS Ellis on her visit: the
        /// spell in custody (Custody.Take), recorded so that nobody takes him for
        /// the same deed again (the independent check: on her next visit she took
        /// him again for a window he had answered for); null, and nothing done,
        /// when there is no arrest to make or he is already in the cells.
        public Custody TakeIn(string topic, GameTime now, bool ownsUp, bool inTheCoat)
        {
            if (topic == null || !CanArrest(topic)) return null;
            foreach (var t in _taken) if (t.outMinute > now.TotalMinutes) return null;
            Offence o = Offence.Suspicious;
            foreach (var e in _entries) if (e.Topic == topic && e.How == Known.Statement && Arrestable(e.Offence)) { o = e.Offence; break; }
            var c = Custody.Take(topic, o, now, ownsUp, inTheCoat);
            if (c != null) _taken.Add((topic, c.OutAt.TotalMinutes));
            return c;
        }
        public string EllisCameFor => _visits.Count > 0 ? _visits[0].why : null;

        // Whether a detective takes this offence (the rest are a constable's).
        static bool Detective(Offence o) => o >= Offence.Wounding;

        /// WHETHER THE LAW OF 1990 MADE IT AN ARRESTABLE OFFENCE (PACE 1984 s.24
        /// as enacted; production/research/police-response-1990/ARREST-2026-09-29.md):
        /// criminal damage, even a window under two thousand pounds (its ten
        /// years' maximum counts, not the magistrates' cap), a wounding, a robbery
        /// and a killing are; a common assault is not, and is a summons.
        public static bool Arrestable(Offence o) => o == Offence.Damage || o >= Offence.Wounding;

        /// WOULD THIS PERSON GO TO THE POLICE with what they saw or suffered?
        /// `victim`: it was done to them or theirs.
        ///   - A victim of damage to their own property reports it, for the
        ///     insurance. A victim of violence or robbery reports it unless they
        ///     know him well enough to settle it themselves (loyalty) or are too
        ///     frightened (nerve), a wounding or robbery more readily than a push
        ///     (about half against a quarter, the research's rates). The victim
        ///     of a killing reports nothing: whoever finds the body does.
        ///   - A witness goes for a crime a detective takes, or a window (town
        ///     list 6bp, carried until Jafar rules on his page: so that an arrest
        ///     can follow the first build's only crime): a wounding, a robbery or
        ///     criminal damage unafraid and not on his side (nerve at least 0.4,
        ///     loyalty under 0.5), which at the middle values nobody is until a
        ///     story cools them on him; a killing whenever not on his side, the brave because
        ///     they can and the nervous because they crack (Watched.WouldTalkToPolice
        ///     is its low-nerve half; the independent check found a band between
        ///     the two where nobody reported a body, and watching it pushed people
        ///     into that band).
        ///   - Nobody reports a sighting that is no crime; nobody on a hook
        ///     reports anything; somebody bought or frightened quiet about this
        ///     deed (`topic` in their Suppressed) reports nothing but a body;
        ///     somebody whose trade keeps them from the police (`neverToPolice`,
        ///     CastDay.NeverToPolice) reports nothing at all.
        public static bool WouldReport(Gossiper g, Offence o, bool victim, string topic, bool neverToPolice = false)
        {
            if (g == null || neverToPolice || o == Offence.Suspicious || g.Leashed) return false;
            if (topic != null && g.Suppressed.Contains(topic) && o != Offence.Killing) return false;
            if (victim)
            {
                if (o == Offence.Killing) return false;
                if (o == Offence.Damage) return true;
                double settle = o == Offence.Assault ? 0.4 : 0.6;
                double fear = o == Offence.Assault ? 0.5 : 0.3;
                return g.Loyalty < settle && g.Nerve >= fear;
            }
            if (!Detective(o) && o != Offence.Damage) return false;
            if (o == Offence.Killing) return g.Loyalty < 0.5;
            return g.Nerve >= 0.4 && g.Loyalty < 0.5;
        }

        /// A report, as the police hold it: a statement naming him when the
        /// teller saw him well enough to (rung 4, recognition), else a
        /// description; a face they could pick out (rung 3) is a description
        /// too, since no identification parade is modelled (the design says so).
        /// Returns the entry, or null when this person has already given as
        /// good a statement about this deed; a description is raised to a
        /// statement when the same person later names him.
        public Entry Report(string who, string topic, Offence o, int rung, int day)
        {
            if (string.IsNullOrEmpty(who) || string.IsNullOrEmpty(topic)) return null;
            foreach (var e in _entries)
                if (e.Who == who && e.Topic == topic && e.How != Known.Talk)
                {
                    if (e.How == Known.Description && rung >= 4) { e.How = Known.Statement; e.Day = day; return e; }
                    return null;
                }
            var entry = new Entry { Who = who, Topic = topic, Offence = o, How = rung >= 4 ? Known.Statement : Known.Description, Day = day };
            _entries.Add(entry);
            return entry;
        }

        /// Talk reaching her on her enquiries, once a person a deed.
        public void Heard(string who, string topic, Offence o, int day)
        {
            if (string.IsNullOrEmpty(who) || string.IsNullOrEmpty(topic)) return;
            foreach (var e in _entries) if (e.Who == who && e.Topic == topic && e.How == Known.Talk) return;
            _entries.Add(new Entry { Who = who, Topic = topic, Offence = o, How = Known.Talk, Day = day });
        }

        // Talk a person of his day world would pass on: his hidden life, heard
        // from somebody, at the share floor, not bought or hooked quiet; a body
        // always (no leash or money keeps a killing to anybody, GossipMill.Tick).
        static IEnumerable<Rumor> TalkOf(GossipMill mill, Gossiper a)
        {
            if (a.Circle != "day") yield break;
            foreach (var r in a.Rumors)
                if (r.Content != null && r.Content.Subject == "player" && r.Sensitive && r.Hops >= 1
                    && (r.Indelible || (r.Confidence >= mill.MinConfidenceToShare && !a.Leashed && !a.Suppressed.Contains(r.TopicKey))))
                    yield return r;
        }

        /// HOW LOUD THE STREET IS about his nights: how many people of his day
        /// world (GossipMill's day circle, as DayCircleHeat counts it) are
        /// passing round talk about his hidden life that they heard from
        /// somebody (a retelling, not their own sighting). Not DayCircleHeat,
        /// which one first-hand witness fills: a witness is one person who saw
        /// something, talk is the street passing it round.
        public static int Loudness(GossipMill mill)
        {
            if (mill == null) return 0;
            int n = 0;
            foreach (var a in mill.Agents)
                foreach (var _ in TalkOf(mill, a)) { n++; break; }
            return n;
        }

        /// WHAT THE STREET TELLS HER when she comes for its talk: each person
        /// passing talk of his nights round, as talk, a deed each (`offenceOf`
        /// grades a topic; the game knows its deeds). Their own sightings are
        /// not talk: a witness is WouldReport's.
        public void HearTheStreet(GossipMill mill, int day, Func<string, Offence> offenceOf)
        {
            if (mill == null) return;
            foreach (var a in mill.Agents)
                foreach (var r in TalkOf(mill, a))
                    Heard(a.Id, r.TopicKey, offenceOf != null ? offenceOf(r.TopicKey) : Offence.Suspicious, day);
        }

        /// WHETHER SHE COMES TO QUAY STREET TODAY, and for what, each reason
        /// once: for a body (`inquiry` at Procedure or beyond, Police.SummonsEllis);
        /// for each crime a detective takes, once somebody has given a statement
        /// or description of it; and, from TalkNoSoonerThan, for the street's
        /// talk once it is loud. One reason a call: the game calls it until it
        /// returns null. Null when nothing brings her today.
        public string EllisComes(GossipMill mill, int day, Inquiry inquiry = Inquiry.None)
        {
            string Visit(string why)
            {
                foreach (var v in _visits) if (v.why == why) return null;
                _visits.Add((day, why));
                return why;
            }
            if (Police.SummonsEllis(inquiry) && Visit("body") is string body) return body;
            foreach (var e in _entries)
                if (Detective(e.Offence) && e.How != Known.Talk && Visit(e.Offence + " " + e.Topic) is string crime) return crime;
            if (day >= TalkNoSoonerThan && Loudness(mill) >= LoudAt && Visit("talk") is string talk) return talk;
            return null;
        }

        /// Every visit of hers about him is told under this topic and the day.
        public const string AskingPrefix = "player.police_d";
        /// How the people she asked tell it: news the street passes on, no
        /// secret of his (not sensitive), so it never counts towards her coming
        /// back (Loudness counts only his nights).
        public const string AskedSaid = "that detective, Ellis, was on Quay Street asking after Mickey's nephew";
        /// What each person she asked remembers, for their talk.
        public const string AskedMemory = "DS Ellis, the detective, stopped me on Quay Street and asked me about Mickey's nephew, the new owner.";

        /// Whether a story is the street's word that she was asking after him.
        public static bool IsAsking(Rumor r) =>
            r != null && r.TopicKey != null && r.TopicKey.StartsWith(AskingPrefix, StringComparison.Ordinal);

        /// WHO SHE ASKS on a visit about him (town list 6bq): everybody of his
        /// day world who holds a story of his nights, heard or seen, the ones
        /// her enquiries lead her to; in order, for the save and the port.
        public static List<string> WhoSheAsks(GossipMill mill)
        {
            var who = new List<string>();
            if (mill == null) return who;
            foreach (var a in mill.Agents)
            {
                if (a.Circle != "day") continue;
                foreach (var r in a.Rumors)
                    if (r.Content != null && r.Content.Subject == "player" && r.Sensitive && r.Confidence > 0) { who.Add(a.Id); break; }
            }
            who.Sort(StringComparer.Ordinal);
            return who;
        }

        /// SHE ASKED THEM (town list 6bq; the checklist's A15.06, a warning
        /// before any arrest, and the audible half of A15.09): on a visit that
        /// EllisComes gave for him (the street's talk or a crime of his, never
        /// a body, which is not about him), each person she asks remembers it
        /// and has it to pass on as the street's news, "that detective was
        /// asking after you" at his face, told like any story. Before it the
        /// people she asked forgot her at once, and the claim check refused
        /// anybody who said she had been. Returns how many she asked.
        public static int Asked(GossipMill mill, IEnumerable<string> who, string why, GameTime now)
        {
            if (mill == null || who == null || string.IsNullOrEmpty(why) || why == "body") return 0;
            var fact = new Fact("player", "police_d" + now.Day, "asking");
            string topic = AskingPrefix + now.Day;
            var seen = new HashSet<string>();
            int n = 0;
            foreach (var id in who)
            {
                var g = id == null ? null : mill.Get(id);
                // Once a day: a crime and the street's talk on one visit ask once.
                if (g == null || !seen.Add(id) || g.Rumors.Exists(r => r.TopicKey == topic && r.Hops == 0)) continue;
                int memories = g.Memory.Events.Count;
                mill.Witness(id, fact, AskedSaid, false, now, 1.0);
                // Their memory of it is being asked, not a sighting of their own.
                if (g.Memory.Events.Count > memories) g.Memory.Events.RemoveRange(memories, g.Memory.Events.Count - memories);
                g.Memory.Append(new MemoryEvent(now, "observation", 0.7, AskedMemory));
                n++;
            }
            return n;
        }

        /// WHAT SHE CAN PUT TO HIM about one deed: the strongest thing she holds
        /// (a statement naming him over a description over talk), or null.
        public Known? Strongest(string topic)
        {
            Known? best = null;
            foreach (var e in _entries)
                if (e.Topic == topic && (!best.HasValue || e.How > best.Value)) best = e.How;
            return best;
        }

        /// WHETHER THEY ARREST HIM for it: a statement that names him, about an
        /// arrestable offence (Arrestable); for a common assault, a summons.
        /// Talk never does, nor descriptions that cannot say who, however many:
        /// the law would allow it on reasonable suspicion, but the game waits,
        /// as a careful officer would, for what a charge needs. Each statement
        /// is judged by its own offence.
        public bool CanArrest(string topic)
        {
            if (topic == null || WasTaken(topic)) return false;
            foreach (var e in _entries)
                if (e.Topic == topic && e.How == Known.Statement && Arrestable(e.Offence)) return true;
            return false;
        }

        static bool KnownWhy(string why)
        {
            if (why == "talk" || why == "body") return true;
            int sp = why.IndexOf(' ');
            if (sp <= 0 || Array.IndexOf(Enum.GetNames(typeof(Offence)), why.Substring(0, sp)) < 0) return false;
            var topic = why.Substring(sp + 1);
            return Detective((Offence)Enum.Parse(typeof(Offence), why.Substring(0, sp))) && topic.Length > 0 && topic.Trim() == topic && topic.IndexOf(' ') < 0;
        }

        /// For any save's JSON.
        public Dictionary<string, object> ToJson()
        {
            var list = new List<object>();
            foreach (var e in _entries)
                list.Add(new Dictionary<string, object> { { "who", e.Who }, { "topic", e.Topic }, { "offence", e.Offence.ToString() }, { "how", e.How.ToString() }, { "day", (double)e.Day } });
            var visits = new List<object>();
            foreach (var (day, why) in _visits) visits.Add(new List<object> { (double)day, why });
            var calls = new List<object>();
            foreach (var (day, topic) in _calls) calls.Add(new List<object> { (double)day, topic });
            var taken = new List<object>();
            foreach (var (topic, outMinute) in _taken) taken.Add(new List<object> { topic, (double)outMinute });
            return new Dictionary<string, object> { { "entries", list }, { "visits", visits }, { "calls", calls }, { "taken", taken } };
        }

        /// From ToJson's values; what it cannot read it skips.
        public static PoliceFile FromJson(Dictionary<string, object> saved)
        {
            var f = new PoliceFile();
            if (saved == null) return f;
            bool Day(object v, out int day)
            {
                day = 0;
                if (!(v is double d) || d < 0 || d >= 100000 || d != Math.Floor(d)) return false;
                day = (int)d;
                return true;
            }
            if (saved.TryGetValue("entries", out var es) && es is List<object> list)
                foreach (var x in list)
                {
                    if (!(x is Dictionary<string, object> o)) continue;
                    var who = MiniJson.GetString(o, "who");
                    var topic = MiniJson.GetString(o, "topic");
                    var off = MiniJson.GetString(o, "offence");
                    var how = MiniJson.GetString(o, "how");
                    if (string.IsNullOrEmpty(who) || string.IsNullOrEmpty(topic)) continue;
                    if (Array.IndexOf(Enum.GetNames(typeof(Offence)), off) < 0 || Array.IndexOf(Enum.GetNames(typeof(Known)), how) < 0) continue;
                    if (!o.TryGetValue("day", out var dv) || !Day(dv, out int day)) continue;
                    var entry = new Entry { Who = who, Topic = topic, Offence = (Offence)Enum.Parse(typeof(Offence), off), How = (Known)Enum.Parse(typeof(Known), how), Day = day };
                    bool dup = false;
                    foreach (var e in f._entries) if (e.Who == entry.Who && e.Topic == entry.Topic && (e.How == Known.Talk) == (entry.How == Known.Talk)) dup = true;
                    if (!dup) f._entries.Add(entry);
                }
            if (saved.TryGetValue("visits", out var vs) && vs is List<object> visits)
                foreach (var x in visits)
                    if (x is List<object> pair && pair.Count == 2 && Day(pair[0], out int day) && pair[1] is string why && KnownWhy(why))
                    {
                        bool dup = false;
                        foreach (var v in f._visits) if (v.why == why) dup = true;
                        if (!dup) f._visits.Add((day, why));
                    }
            f._visits.Sort((a, b) => a.day.CompareTo(b.day));
            // A constable's call only for a statement about a window, given before it.
            if (saved.TryGetValue("calls", out var cs) && cs is List<object> calls)
                foreach (var x in calls)
                    if (x is List<object> pair && pair.Count == 2 && Day(pair[0], out int day) && pair[1] is string topic
                        && f._entries.Exists(e => e.Topic == topic && e.Offence == Offence.Damage && e.How == Known.Statement && e.Day < day)
                        && !f._calls.Exists(c => c.topic == topic))
                        f._calls.Add((day, topic));
            f._calls.Sort((a, b) => a.day.CompareTo(b.day));
            // Taken in only for a deed with a statement he could be arrested for.
            if (saved.TryGetValue("taken", out var tk) && tk is List<object> takenList)
                foreach (var x in takenList)
                    if (x is List<object> pair && pair.Count == 2 && pair[0] is string topic && pair[1] is double om && om >= 0 && om < 1e8 && om == Math.Floor(om)
                        && f.CanArrest(topic))
                        f._taken.Add((topic, (long)om));
            return f;
        }
    }
}
