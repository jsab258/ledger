using System;

namespace Ledger.Core
{
    /// What happens with the man at the landing, as the game calls for his line.
    public enum LandingMoment
    {
        /// Tom comes up to him at the landing.
        Comes,
        /// Tom has just handed the envelope over (after Arrangement.Answer, Did).
        HandsOver,
        /// Tom leaves, or stands there, with nothing handed over.
        NothingToHand,
        /// Tom tries to talk with him.
        TalksToHim,
    }

    /// THE MAN AT THE LANDING (town list 6cj; the twelfth sweep; A33.05,
    /// "completion acknowledged rather than silently recorded"). The outfit's
    /// man takes the envelope at the ferry landing from ten till one, and
    /// said nothing: a friend who carried it on night one was never told the
    /// job was done or when the next comes, and the same silence met him
    /// empty-handed, on a night with no ask, or after he told Ron no. A few
    /// fixed lines, chosen by the arrangement's state: he asks for Mickey's,
    /// says when the next is, says when they are finished with him, and
    /// brushes off talk. None names what is in the envelope. Plain text: no
    /// voice is cast for him without Jafar's yes, and he has no talk card.
    /// The game shows each once a night; the brush-offs may come round again.
    public static class TheLanding
    {
        /// He is at the landing from ten till one (hook-cast.json, outfit_man).
        public const int From = 22;

        public const string Asks = "Mickey's?";
        /// {0}: when the next is, "Thursday" or "Tomorrow".
        public const string SameAgain = "Right. {0}, same again.";
        /// After the last ask night he stayed away from.
        public const string KeptWaiting = "You kept us waiting last time. Don't make a habit of it. {0}, same again.";
        public const string NothingForMe = "Nothing for me? Then you've no business down here.";
        /// {0}: when the next is.
        public const string NotTonight = "Nothing tonight. {0}, after ten.";
        public const string DoneRefused = "Ron's been down. We're done, you and us.";
        public const string DoneStopped = "You had your chances. We're done, you and us.";
        public const string DoneWound = "Winding it all up, Ron says. We're done, you and us.";
        public const string DoneYourBit = "You've done your bit. Go home.";
        public const string DoneGoOn = "We're done. Go on.";
        public static readonly string[] BrushOff = { "I've nothing to say to you.", "Not here. Go on.", "I don't do talking." };

        /// Whether he is at the landing at `now`.
        public static bool There(GameTime now) => now.Hour >= From || now.Hour < Arrangement.GaveUpHour;

        /// His line for this moment, or null when he has nothing to say (or is
        /// not there).
        public static string Line(Arrangement a, GameTime now, LandingMoment m, int seed = 0)
        {
            if (a == null || !There(now)) return null;
            int night = Arrangement.NightOf(now);
            bool didTonight = a.Nights.TryGetValue(night, out var tonight) && tonight == NightAnswer.Did;
            // Wound down, and Ron not yet down with the word (the second review:
            // a Monday's winding down answers the Tuesday's ask, yet Ron goes
            // down on the Monday at eleven): till then he waits on Mickey's as ever.
            bool notHeardYet = a.Ended && a.EndedWhy == "wound down" && a.WoundWordAt is GameTime word && now.CompareTo(word) < 0;
            if (m == LandingMoment.TalksToHim)
            {
                if (a.Ended && !notHeardYet) return DoneGoOn;
                if (didTonight) return DoneYourBit;
                return BrushOff[((seed % BrushOff.Length) + BrushOff.Length) % BrushOff.Length];
            }
            if (notHeardYet)
            {
                if (night == a.WoundNight) return m == LandingMoment.Comes ? Asks : m == LandingMoment.NothingToHand ? NothingForMe : null;
                return m == LandingMoment.Comes ? string.Format(NotTonight, When(a.WoundNight, night)) : null;
            }
            if (a.Ended)
                return m == LandingMoment.Comes ? (a.EndedWhy == "refused" ? DoneRefused : a.EndedWhy == "wound down" ? DoneWound : DoneStopped) : null;
            if (didTonight)
                return m == LandingMoment.HandsOver ? string.Format(StayedAwayLast(a, night) ? KeptWaiting : SameAgain, When(a.NextNight, night)) : null;
            // Tonight's ask, unanswered, whether or not Ron reached him with it.
            if (a.AsksOn(night))
                return m == LandingMoment.Comes ? Asks : m == LandingMoment.NothingToHand ? NothingForMe : null;
            // A night with no ask.
            return m == LandingMoment.Comes ? string.Format(NotTonight, When(a.NextNight, night)) : null;
        }

        // The last ask night answered before this one was a night he stayed away.
        static bool StayedAwayLast(Arrangement a, int night)
        {
            var last = NightAnswer.Undelivered;
            foreach (var kv in a.Nights)
                if (kv.Key < night && kv.Value != NightAnswer.Undelivered) last = kv.Value;
            return last == NightAnswer.NoShow;
        }

        static string When(int next, int night) =>
            next == night + 1 ? "Tomorrow" : new GameTime(next, From, 0).WeekdayName;
    }
}
