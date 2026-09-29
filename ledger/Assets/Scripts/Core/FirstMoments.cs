using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// HINTS THAT FIRE THE FIRST TIME THEY MATTER (town list 6y; the checklist's
    /// A04.07, "instructions shown when their actions become relevant"; the
    /// first hour Jafar approved on 28 September). The old game's four hints ran
    /// on the clock: at two game minutes a real second they came at 1, 5, 30 and
    /// 90 seconds, two overlapping, and a player who had not found the walking
    /// keys was told about the Ledger and a night job inside a minute and a half
    /// (production/research/teaching-in-thirty-minutes). Here the game reports
    /// each moment every time it happens, and each hint shows once, the first
    /// time it can mean something: in the world's own words where somebody can
    /// say it (Sheila at the end of her walk-round, Ron with the coat) and plain
    /// text where nobody can. Walking comes first; never two within the gap; a
    /// hint about what just happened that has waited past its moment is dropped
    /// unshown, so the next time the moment comes round it can still teach. A
    /// spoken beat (Ron with the coat) and a screen's own line (the Ledger's) show
    /// at once, when the thing happens. The words are for Jafar's approval
    /// (game-design/first-moments-2026-09-29.md); the game fills in the keys as
    /// the player has them bound.
    public enum Moment
    {
        /// He has not moved a few seconds after a new game begins.
        StandingStill,
        /// He is free to talk to somebody: in the first hour, when Sheila's
        /// walk-round ends at the office door.
        CanTalk,
        /// Ron hands him the coat and the outfit's envelope (its first ask).
        FirstAsk,
        /// Somebody saw him do something the town will talk about.
        SeenAtDeed,
        /// He overheard a remark about himself.
        OverheardAboutHim,
        /// He opened the Ledger.
        LedgerOpened,
    }

    /// One hint. `Speaker` (a cast id) says `Line` in their own voice when they
    /// are with him, and a game that has nobody there leaves the line out;
    /// `Key` is plain text and always shows. Keys in braces ({Move}, {Run},
    /// {Talk}, {Coat}, {Ledger}) are the game's to fill (FirstMoments.Fill).
    public sealed class Hint
    {
        public Moment Moment { get; }
        public string Speaker { get; }
        public string Line { get; }
        public string Key { get; }
        /// Shown at once when the moment happens (a spoken beat, a screen's own
        /// line), never queued behind another.
        public bool AtOnce { get; }
        /// Real seconds it stays worth showing after its moment; beyond that
        /// it is dropped unshown.
        public double StaleAfter { get; }

        public Hint(Moment moment, string speaker, string line, string key, bool atOnce, double staleAfter)
        {
            Moment = moment; Speaker = speaker; Line = line; Key = key; AtOnce = atOnce; StaleAfter = staleAfter;
        }
    }

    public sealed class FirstMoments
    {
        /// Real seconds between two hints, so none overlaps another.
        public const double Gap = 12.0;
        /// Real seconds standing still in a new game before he is told how to walk.
        public const double StillFor = 4.0;

        /// The words, one hint a moment.
        public static readonly IReadOnlyDictionary<Moment, Hint> Words = new Dictionary<Moment, Hint>
        {
            { Moment.StandingStill, new Hint(Moment.StandingStill, null, null,
                "{Move} walks, {Run} runs. People on this street notice who's about.", false, double.PositiveInfinity) },
            { Moment.CanTalk, new Hint(Moment.CanTalk, "lena",
                "That's Ron on the rank. Go and say hello. Everyone out there wants a look at you.",
                "Walk up to anyone and press {Talk}. What you tell them, they remember.", false, 45) },
            { Moment.FirstAsk, new Hint(Moment.FirstAsk, "rocco",
                "If you go tonight, boss, wear that. In the dark nobody looks twice at a coat.",
                "{Coat} puts the coat on or takes it off: in the dark it makes you harder to recognise.", true, 0) },
            { Moment.SeenAtDeed, new Hint(Moment.SeenAtDeed, null, null,
                "Somebody saw that. What they make of it can go round.", false, 15) },
            { Moment.OverheardAboutHim, new Hint(Moment.OverheardAboutHim, null, null,
                "That was about you. {Ledger} shows what you believe the street knows.", false, 15) },
            { Moment.LedgerOpened, new Hint(Moment.LedgerOpened, null, null,
                "What you believe the street now knows about you.", true, 0) },
        };

        static readonly string[] Names = Enum.GetNames(typeof(Moment));

        readonly HashSet<Moment> _done = new HashSet<Moment>();
        readonly List<(Moment m, double since)> _waiting = new List<(Moment, double)>();
        double _began = double.NaN;
        bool _fresh, _moved;
        double _lastShown = double.NegativeInfinity;
        double _latest = double.NegativeInfinity;

        /// The moments whose hints have shown (or no longer can), for the save.
        public IReadOnlyCollection<Moment> Done => _done;

        // A clock that never runs backwards, whatever the game sends; NaN or an
        // infinity is no time.
        bool Clock(ref double at)
        {
            if (double.IsNaN(at) || double.IsInfinity(at)) return false;
            if (at < _latest) at = _latest;
            _latest = at;
            return true;
        }

        /// A session begins at this real second: a new game (`newGame`), which
        /// starts the hints over, or a loaded save (`saved`, ToJson's values),
        /// whose moments are done. The gap holds across a load; a clock the game
        /// restarted (a level opening) is taken up from where it is now. Only a
        /// new game tells him how to walk: after a load he has walked already.
        public void Begin(double at, bool newGame, Dictionary<string, object> saved = null)
        {
            _waiting.Clear();
            _moved = false;
            if (newGame) _done.Clear();
            else
            {
                if (saved != null) { _done.Clear(); Read(saved, _done); }
                _done.Add(Moment.StandingStill);
            }
            if (double.IsNaN(at) || double.IsInfinity(at)) { _began = double.NaN; _fresh = false; return; }
            if (at < _latest)
            {
                // The game's clock started again: the last hint was that long before now.
                double shift = _latest - at;
                _lastShown -= shift;
                _latest = at;
            }
            Clock(ref at);
            _began = at;
            _fresh = newGame;
        }

        /// He moved. Once he has, nobody tells him how, in this game or after
        /// a load: the moment is done without its hint.
        public void Moved(double at)
        {
            _moved = true;
            _done.Add(Moment.StandingStill);
            _waiting.RemoveAll(w => w.m == Moment.StandingStill);
        }

        /// The moment happened at this real second (the game reports it every
        /// time). A hint shown at once is returned now; any other waits for
        /// Due. Null when there is nothing to show now.
        public Hint Happened(Moment m, double at)
        {
            if (!Clock(ref at) || m == Moment.StandingStill || _done.Contains(m)) return null;
            var h = Words[m];
            if (h.AtOnce)
            {
                _done.Add(m);
                _waiting.RemoveAll(w => w.m == m);
                _lastShown = at;
                return h;
            }
            for (int i = 0; i < _waiting.Count; i++)
                if (_waiting[i].m == m) { _waiting[i] = (m, at); return null; }   // happened again: fresh again
            _waiting.Add((m, at));
            return null;
        }

        /// The hint to show at this real second, or null: at most one, never
        /// inside the gap after the last, walking before anything else in a new
        /// game, and nothing that has gone stale.
        public Hint Due(double at)
        {
            if (!Clock(ref at)) return null;
            bool walkFirst = _fresh && !_moved && !_done.Contains(Moment.StandingStill) && !double.IsNaN(_began);
            if (walkFirst && at - _began >= StillFor && !_waiting.Exists(w => w.m == Moment.StandingStill))
                _waiting.Insert(0, (Moment.StandingStill, at));
            _waiting.RemoveAll(w => at - w.since > Words[w.m].StaleAfter);
            if (_waiting.Count == 0 || at - _lastShown < Gap) return null;
            // Until he has walked or been told how, only the walking hint shows.
            int pick = walkFirst ? _waiting.FindIndex(w => w.m == Moment.StandingStill) : 0;
            if (pick < 0) return null;
            var m = _waiting[pick].m;
            _waiting.RemoveAt(pick);
            _done.Add(m);
            _lastShown = at;
            return Words[m];
        }

        /// A hint's text with the keys as the player has them bound; a key the
        /// game does not name, or names as nothing, is left in its braces.
        public static string Fill(string text, Func<string, string> keyFor)
        {
            if (string.IsNullOrEmpty(text) || keyFor == null) return text;
            return System.Text.RegularExpressions.Regex.Replace(text, @"\{(\w+)\}", m =>
            {
                var k = keyFor(m.Groups[1].Value);
                return string.IsNullOrWhiteSpace(k) ? m.Value : k;
            });
        }

        /// The moments done, for any save's JSON: "done", their names.
        public Dictionary<string, object> ToJson()
        {
            var done = new List<string>();
            foreach (var m in _done) done.Add(m.ToString());
            done.Sort(StringComparer.Ordinal);
            var list = new List<object>();
            foreach (var d in done) list.Add(d);
            return new Dictionary<string, object> { { "done", list } };
        }

        /// From ToJson's values: only a moment's exact name counts, and what it
        /// cannot read it skips, so a damaged save shows a hint again rather than
        /// losing the game.
        public static FirstMoments FromJson(Dictionary<string, object> saved)
        {
            var f = new FirstMoments();
            Read(saved, f._done);
            return f;
        }

        static void Read(Dictionary<string, object> saved, HashSet<Moment> into)
        {
            if (saved != null && saved.TryGetValue("done", out var done) && done is List<object> names)
                foreach (var n in names)
                    if (n is string s && Array.IndexOf(Names, s) >= 0) into.Add((Moment)Enum.Parse(typeof(Moment), s));
        }
    }
}
