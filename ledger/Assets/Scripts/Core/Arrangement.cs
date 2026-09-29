using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// What he did with one night's ask.
    public enum NightAnswer
    {
        /// He handed the envelope over at the landing.
        Did,
        /// He told Ron no: the arrangement ends at once.
        Refused,
        /// He said nothing and did not go.
        NoShow,
    }

    /// MICKEY'S ARRANGEMENT WITH THE OUTFIT, IN THE NEW GAME (town list 6z; the
    /// checklist's A33.01; the first hour Jafar approved on 28 September, whose
    /// second ask falls on day 3, the evening of Ada's tea). The outfit asks
    /// every other night from the first, through Ron: an envelope to the ferry
    /// landing (game-design/first-ask-2026-09-29.md). He can do it, refuse, or
    /// not turn up. Refusing ends the arrangement at once; a night he does not
    /// turn up costs the outfit's patience, and three such nights end it; a
    /// night done wins a little back. NEVER A GAME OVER: the old week's rule
    /// (Campaign.JobMissed, "the outfit stopped calling. Then they sent
    /// someone.") ended the game on the third missed night; the new game's
    /// story uses an ended arrangement, it does not stop on one.
    ///
    /// Whatever he does is a story, the outfit's talk as the first hour has it,
    /// told first by the outfit's man at the landing, who knows it first-hand:
    /// he took the envelope, or waited for nobody, or heard the no from Ron,
    /// who carries Tom's answer down (each summary says what he himself saw).
    /// Ron, who keeps things quiet for the owner, tells nobody. Only the
    /// envelope handed over is a night-life secret (sensitive); a refusal or a
    /// night he stayed away is not. Nights are answered in order, one at a
    /// time; a night that passed unanswered counts as one he stayed away
    /// (PassedTo), so the asks never stop unnoticed; and a save is replayed
    /// through the same rules, so it can hold nothing play could not reach
    /// (the independent check).
    public sealed class Arrangement
    {
        /// The game day whose night brings the first ask: day 0, the first day,
        /// as GameTime and the cast's routines count (day 0 a Monday).
        public int FirstDay { get; private set; }
        /// Nights between asks: 2, so the second falls on the third day.
        public const int Every = 2;
        /// A night he does not turn up; three and it ends, as the old rule counted.
        public const double PatienceLossPerNoShow = 0.34;
        /// A night done wins a little back, up to whole.
        public const double PatienceGainPerNight = 0.10;
        /// Who tells every answer first (a cast id): the outfit's man.
        public const string OutfitMan = "outfit_man";
        /// Every night's story is told under this topic and the night's day.
        public const string TopicPrefix = "player.outfit_d";

        public bool Ended { get; private set; }
        /// "refused" or "stopped", once ended.
        public string EndedWhy { get; private set; }
        public double Patience { get; private set; } = 1.0;
        readonly SortedDictionary<int, NightAnswer> _nights = new SortedDictionary<int, NightAnswer>();

        public Arrangement(int firstDay = 0) { FirstDay = Math.Max(0, firstDay); }

        /// The nights answered, in order, for the session record and the save.
        public IReadOnlyDictionary<int, NightAnswer> Nights => _nights;

        /// The night of the next ask, or -1 once the arrangement has ended.
        public int NextNight => Ended ? -1 : FirstDay + Every * _nights.Count;

        /// Whether the outfit asks on this day's night.
        public bool AsksOn(int day) => !Ended && day == NextNight;

        /// The topic the night's story is told under, as the session record keys deeds.
        public static string TopicFor(int day) => TopicPrefix + day;

        /// Whether a story is one of the arrangement's nights.
        public static bool IsNight(Rumor r) => r != null && r.TopicKey != null && r.TopicKey.StartsWith(TopicPrefix, StringComparison.Ordinal);

        /// How each answer is told, as the outfit's man saw it himself.
        public static string Said(NightAnswer a) =>
            a == NightAnswer.Did ? "Mickey's nephew brought the envelope down the landing"
            : a == NightAnswer.Refused ? "Ron came down the landing to say Mickey's nephew told them no"
            : "Mickey's nephew never turned up at the landing";

        /// The word each answer's story carries.
        public static string Value(NightAnswer a) => a == NightAnswer.Did ? "did" : a == NightAnswer.Refused ? "refused" : "noshow";

        /// He answered this night's ask. Returns false, changing nothing, unless
        /// it is the night the outfit asks (NextNight). With `mill`, the night's
        /// story goes into the gossip, told first by whoever knows it at `now`,
        /// which must then be given.
        public bool Answer(int day, NightAnswer what, GossipMill mill = null, GameTime? now = null)
        {
            if (mill != null && !now.HasValue) throw new ArgumentException("the story needs the time it is told", nameof(now));
            if (!AsksOn(day)) return false;
            _nights[day] = what;
            if (what == NightAnswer.Refused) { Ended = true; EndedWhy = "refused"; }
            else if (what == NightAnswer.Did) Patience = Math.Min(1.0, Patience + PatienceGainPerNight);
            else
            {
                Patience = Math.Max(0.0, Patience - PatienceLossPerNoShow);
                if (Patience <= 1e-9) { Ended = true; EndedWhy = "stopped"; }
            }
            if (mill != null)
                mill.Witness(OutfitMan, new Fact("player", "outfit_d" + day, Value(what)), Said(what), what == NightAnswer.Did, now.Value, 1.0);
            return true;
        }

        /// The day is now `day`: every ask night before it that nobody answered
        /// (a dawn the game missed, a load that skipped a night) counts as one
        /// he stayed away, told by the outfit's man when a mill is given: as of
        /// one in the morning after that night, when he gave up waiting, or
        /// `now` if that is earlier. The game calls it at each dawn and after
        /// every load.
        public void PassedTo(int day, GossipMill mill = null, GameTime? now = null)
        {
            if (mill != null && !now.HasValue) throw new ArgumentException("the story needs the time it is told", nameof(now));
            while (!Ended && NextNight < day)
            {
                GameTime? told = null;
                if (now.HasValue)
                {
                    var gaveUp = new GameTime(NextNight + 1, 1, 0);
                    told = gaveUp.TotalMinutes < now.Value.TotalMinutes ? gaveUp : now.Value;
                }
                Answer(NextNight, NightAnswer.NoShow, mill, told);
            }
        }

        /// For any save's JSON: "first", the first night's day; "nights", [day,
        /// answer] pairs in order. Patience and the end follow from them.
        public Dictionary<string, object> ToJson()
        {
            var nights = new List<object>();
            foreach (var kv in _nights) nights.Add(new List<object> { (double)kv.Key, Value(kv.Value) });
            return new Dictionary<string, object> { { "first", (double)FirstDay }, { "nights", nights } };
        }

        /// From ToJson's values, replayed in order through Answer: the first
        /// night that play could not have reached, and everything after it, is
        /// dropped, so a hand-edited save holds only what play could.
        public static Arrangement FromJson(Dictionary<string, object> saved)
        {
            int first = 0;
            if (saved != null && saved.TryGetValue("first", out var f) && f is double fd && fd >= 0 && fd < 100000 && fd == Math.Floor(fd)) first = (int)fd;
            var a = new Arrangement(first);
            if (saved == null || !saved.TryGetValue("nights", out var n) || !(n is List<object> nights)) return a;
            foreach (var x in nights)
            {
                if (!(x is List<object> pair) || pair.Count != 2 || !(pair[0] is double d) || !(pair[1] is string v)) break;
                NightAnswer? ans = v == "did" ? NightAnswer.Did : v == "refused" ? NightAnswer.Refused : v == "noshow" ? NightAnswer.NoShow : (NightAnswer?)null;
                if (!ans.HasValue || d != Math.Floor(d) || !a.Answer((int)d, ans.Value)) break;
            }
            return a;
        }
    }
}
