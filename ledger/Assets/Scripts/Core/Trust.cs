using System.Collections.Generic;

namespace Ledger.Core
{
    /// WHEN SHEILA TRUSTS HIM (town list 6bz; the first hour's day 7 and the
    /// outline's Act I; carried until Jafar rules on his 30 September page).
    /// Her card has her size up whoever inherited the office, as she promised
    /// Mickey, calling him "new management" until he earns a name, and keeping
    /// the real book back "until I fully trust the new owner"; Jafar ruled she
    /// names him only on trust. Nothing decided when that was, so she never
    /// named him and never showed the book. As recommended meanwhile, from her
    /// own talk with him (the talk helper's engine for her): once he has talked
    /// with her on three different days (so the third day at the soonest),
    /// while she has never seen him, or heard of him, about the place when a
    /// deed was done (ConversationEngine.DeedEvidence), never caught him out
    /// (Doubted: a lie, a sighting his answer did not name, what he told
    /// others), and is not wary of him (suspicion Trusting). Whatever he says
    /// about it afterwards does not win it back this week: the independent
    /// check found, four times over, that weighing his answers inherited every
    /// limit of how answers are read (a lie naming nowhere known never taken
    /// down, a true answer hedged never counting, nothing read with talk off),
    /// so a lie could win her over and the truth could not. Once earned it
    /// holds: the book, once shown, cannot be unshown.
    public static class Trust
    {
        /// How many different days he must have talked with her.
        public const int DaysTalked = 3;

        /// Whether she has come to trust him by `today`, from her talk with him.
        public static bool Earned(ConversationEngine engine, int today)
        {
            if (engine == null) return false;
            if (engine.Suspicion.Level != SuspicionLevel.Trusting) return false;
            if (engine.Doubted || engine.ToldOthers.Count > 0) return false;
            foreach (var a in engine.Answers)
                if (a.Result == ClaimResult.Contradiction || a.SawElsewhere) return false;
            if (engine.DeedEvidence.Count > 0) return false;
            int days = 0;
            foreach (var d in engine.TalkDays) if (d <= today) days++;
            return days >= DaysTalked;
        }

        /// Marks it earned when it is: true only the turn it is first earned.
        public static bool Earn(ConversationEngine engine, int today)
        {
            if (engine == null || engine.TrustEarned || !Earned(engine, today)) return false;
            engine.TrustEarned = true;
            return true;
        }
    }
}
