using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// How Ada's tea went.
    public enum TeaState
    {
        /// Not yet asked.
        NotAsked,
        /// She has asked him; the evening has not closed.
        Asked,
        /// He came and sat with her till half past ten or later.
        Stayed,
        /// He came and was gone again before half past ten.
        LeftEarly,
        /// He never came.
        StoodUp,
    }

    /// ADA'S TEA, THE FIRST HOUR'S DAY-3 SCENE (town list 6bg; the first hour
    /// Jafar approved: "Ada asks him in for tea on the evening the outfit's
    /// second ask falls: the week's first test of which life he keeps"). The old
    /// game's Beat counted a moment's visit as coming (the independent check:
    /// he could drop in at nine and still make the landing, losing nothing), so
    /// the tea is its own scene here. She asks him when she first sees him that
    /// day; the pot is on at nine; to count as having come he is there by half
    /// past nine and sits with her an hour or more, through half past ten (the
    /// independent check: one minute at 22:31 counted as staying). The landing
    /// is open till one, but at the first hour's clock the walk from her step
    /// is about two game hours, so a man who stays arrives near one. Going to
    /// the landing on an ask night while she sits at her window that evening,
    /// before or after his tea or instead of it, he is seen going
    /// (WentToTheLanding): the test is which life he is seen to keep.
    /// What it leaves is her regard for him (Gossiper.Loyalty), which with her
    /// nerve decides whether she would go to the police about him
    /// (PoliceFile.WouldReport): stayed, it rises above where she would; stood
    /// up, it falls. Never the game. Alison's question the same day waits on the
    /// warehouse fire's facts (his page).
    public sealed class AdasTea
    {
        public const string Ada = "ada";
        /// The evening: the pot on at nine; the evening closes at eleven.
        public const int From = 21, Until = 23;
        /// To count as having come: there by half past nine, still there at half
        /// past ten, and never away more than ten minutes between (the
        /// independent check: an hour's gap counted as staying).
        public const int ArriveByMinute = 21 * 60 + 30, StayUntilMinute = 22 * 60 + 30, LongestAway = 10;
        public const double StayedGain = 0.25, LeftEarlyGain = 0.05, StoodUpCost = 0.15;

        /// What she says when she asks him.
        public const string Invite = "There'll be a pot on at nine tonight, if you want it. I don't ask twice, mind.";

        /// The day of the tea: the night of the outfit's second ask.
        public int Day { get; private set; }
        public TeaState State { get; private set; } = TeaState.NotAsked;
        readonly SortedSet<int> _minutes = new SortedSet<int>();
        /// The minutes of the evening (from midnight) he was with her.
        public IReadOnlyCollection<int> Minutes => _minutes;
        /// The latest of them, or -1.
        public int LatestMinute => _minutes.Count > 0 ? _minutes.Max : -1;
        public bool SeenGoing { get; private set; }

        /// THE TEA FOR THIS RUN, made on the morning of its day: on the night of
        /// the outfit's second ask (the first ask's day plus Arrangement.Every),
        /// for a man who has met her by then; null for one who has not, since she
        /// does not ask a stranger in. Without the ask (he told them no) it is
        /// that evening all the same, and is only tea.
        public static AdasTea For(int firstAskDay, bool metAdaByThen) =>
            !metAdaByThen || firstAskDay < 0 ? null : new AdasTea { Day = firstAskDay + Arrangement.Every };

        /// She sees him on the tea's day before nine and asks him, once.
        /// Returns her line, or null when it is not the moment.
        public string SheSeesHim(GameTime now)
        {
            if (State != TeaState.NotAsked || now.Day != Day || now.Hour >= From) return null;
            State = TeaState.Asked;
            return Invite;
        }

        /// He is in her house at this minute (the game calls it for every game
        /// minute he is there, skipped time included): counted between nine and
        /// eleven on the tea's day, once she has asked.
        public void WithHer(GameTime now)
        {
            if (State != TeaState.Asked || now.Day != Day || now.Hour < From || now.Hour >= Until) return;
            _minutes.Add(now.Hour * 60 + now.Minute);
        }

        // How the evening went, from the minutes alone.
        TeaState Judge()
        {
            if (_minutes.Count == 0) return TeaState.StoodUp;
            if (_minutes.Min > ArriveByMinute || _minutes.Max < StayUntilMinute) return TeaState.LeftEarly;
            int last = -1;
            foreach (var m in _minutes)
            {
                // The minutes away are those between two he was there: stamps
                // eleven apart are ten away, which is allowed (the port's
                // independent check, 30 September).
                if (last >= 0 && m - last - 1 > LongestAway) return TeaState.LeftEarly;
                last = m;
            }
            return TeaState.Stayed;
        }

        /// The evening closes (eleven, or any later call): how it went, and what
        /// it leaves with her.
        public TeaState Close(Gossiper ada, GameTime now)
        {
            if (State != TeaState.Asked) return State;
            if (now.Day == Day && now.Hour < Until) return State;
            State = Judge();
            if (ada != null)
            {
                if (State == TeaState.Stayed)
                {
                    ada.Loyalty = Math.Min(1.0, ada.Loyalty + StayedGain);
                    ada.Suspicion.Lower(0.1, "Mickey's nephew sat with me over a pot of tea");
                    ada.Memory.Append(new MemoryEvent(now, "conversation", 0.7,
                        "Mickey's nephew came for his tea and sat with me till gone half ten. There's more to him than they're saying."));
                }
                else if (State == TeaState.LeftEarly)
                {
                    ada.Loyalty = Math.Min(1.0, ada.Loyalty + LeftEarlyGain);
                    ada.Memory.Append(new MemoryEvent(now, "conversation", 0.6,
                        "Mickey's nephew came for his tea and was off again before the pot was cold. Somewhere to be, had he."));
                }
                else
                {
                    ada.Loyalty = Math.Max(0.0, ada.Loyalty - StoodUpCost);
                    ada.Memory.Append(new MemoryEvent(now, "observation", 0.65,
                        "I asked Mickey's nephew in for his tea. He never came. I'll not ask again."));
                }
            }
            return State;
        }

        /// He went down to the landing for the outfit's ask on the tea's night
        /// (`forTheAsk`: the game says so only on an ask night), called when he
        /// sets off from Quay Street or when he reaches the landing, between nine
        /// that evening and one in the morning, when the landing closes, having
        /// been asked in: she saw him go from her window, before his tea, after
        /// it or instead of it, knowing him, and it is hers to tell, a secret of
        /// his nights like any sighting. Once. Without the ask, a walk is only a
        /// walk.
        public void WentToTheLanding(GossipMill mill, GameTime now, bool forTheAsk)
        {
            if (SeenGoing || mill == null || !forTheAsk || State == TeaState.NotAsked) return;
            bool thatNight = (now.Day == Day && now.Hour >= From) || (now.Day == Day + 1 && now.Hour < 1);
            // Nobody sees him go when Ada is not in the mill (the port's
            // independent check, 30 September: he was marked seen, and nobody
            // held it).
            if (!thatNight || mill.Get(Ada) == null) return;
            SeenGoing = true;
            mill.Witness(Ada, new Fact("player", "left_tea_for_landing_d" + Day, "seen"),
                         "Mickey's nephew went off down towards the ferry, late, the night I'd asked him in for his tea", true, now, 1.0, rung: 4);
        }

        /// For any save's JSON.
        public Dictionary<string, object> ToJson()
        {
            var minutes = new List<object>();
            foreach (var m in _minutes) minutes.Add((double)m);
            return new Dictionary<string, object> { { "day", (double)Day }, { "state", State.ToString() }, { "minutes", minutes }, { "seenGoing", SeenGoing } };
        }

        /// From ToJson's values; what it cannot read it skips (a damaged tea is
        /// one not yet asked, on its day).
        public static AdasTea FromJson(Dictionary<string, object> saved)
        {
            if (saved == null || !(saved.TryGetValue("day", out var d) && d is double dd && dd >= 0 && dd < 100000 && dd == Math.Floor(dd))) return null;
            var t = new AdasTea { Day = (int)dd };
            var state = MiniJson.GetString(saved, "state");
            if (state != null && Array.IndexOf(Enum.GetNames(typeof(TeaState)), state) >= 0) t.State = (TeaState)Enum.Parse(typeof(TeaState), state);
            // Minutes only once asked, and only the evening's.
            if (t.State != TeaState.NotAsked && saved.TryGetValue("minutes", out var ms) && ms is List<object> list)
                foreach (var x in list)
                    if (x is double m && m >= From * 60 && m < Until * 60 && m == Math.Floor(m)) t._minutes.Add((int)m);
            // A closed evening is what its minutes say, whatever the file says.
            if (t.State == TeaState.Stayed || t.State == TeaState.LeftEarly || t.State == TeaState.StoodUp) t.State = t.Judge();
            if (saved.TryGetValue("seenGoing", out var s) && s is bool sb) t.SeenGoing = sb && t.State != TeaState.NotAsked;
            return t;
        }
    }
}
