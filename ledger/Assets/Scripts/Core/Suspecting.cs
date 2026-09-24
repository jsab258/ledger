using System;

namespace Ledger.Core
{
    /// What one person holds about a deed: the account that reached them.
    public struct DeedAccount
    {
        /// They hold an account of the deed at all.
        public bool Held;
        /// They saw it themselves (hop 0) rather than heard it.
        public bool SawItMyself;
        /// How well the account identifies the man, on the five-rung ladder
        /// (0 someone, 1 silhouette, 2 a mark, 3 a face, 4 recognition), or -1
        /// when the account does not carry it. For a first-hand account it is
        /// the rung the witness reached; recognition (4) is what names him.
        /// NOT READ OFF THE CERTAINTY: a sighting is capped at 0.94 by
        /// Observe.CertaintyFor, so the 0.95 line can never name anybody
        /// (independent check, 24 September).
        public int Rung;
        /// A heard account whose first teller named him (they recognised
        /// him). A rumour does not carry its teller's rung yet, so a caller
        /// that cannot know says false.
        public bool NamesHim;
        /// The account's confidence as it reached them, 0..1.
        public double Confidence;
        /// What they were told or saw, as a clause ("the man that did the
        /// window looked straight in at the shop before he ran").
        public string Summary;
    }

    /// What one person holds about who was near the deed at the time.
    public struct Nearness
    {
        /// They saw the player near it themselves, well enough to know him
        /// again (see Suspecting.CanTieSighting).
        public bool SawHimMyself;
        /// Somebody told them the player, BY NAME, was near it. A sighting
        /// passed on by somebody who could not name him ("a man came through
        /// the yard") ties nobody when it is retold: talk alone must not let
        /// the town identify him (Acquaintance.HeardOfYou's own rule).
        public bool HeardHeWasNear;
        /// How many OTHER people they know were near it at the time.
        public int OthersNear;
        /// What they saw or heard of him, as a clause, or null.
        public string Summary;
    }

    /// WHY SOMEBODY HAS REASON TO SUSPECT TOM OF A DEED, from three things
    /// they hold: what they know about the deed, who they know was near it,
    /// and how they know Tom. Jafar, 24 September, after the encounter on the
    /// real model: the lad talked about the broken window and asked Tom
    /// nothing, because nothing gave him a reason to. Knowing that a window
    /// went is not a reason to suspect the man in front of you; knowing it
    /// went and having seen him come away from it, with nobody else about, is.
    ///
    /// DETERMINISTIC AND IN CORE, by canon: the Core decides every outcome the
    /// player feels, and the model only performs it. The model is handed the
    /// level and the reason in words, the reason in the character's own voice
    /// like every other entry in the tracker's trail; it never decides whether
    /// to suspect.
    ///
    /// NO NEW THRESHOLD. Each case is placed on one of the four existing
    /// SuspicionTracker bands (Trusting under 0.25, Uneasy, Suspicious from
    /// 0.50, Confronting from 0.80), which is an authoring decision about
    /// fiction, the same kind Acquaintance makes; within the band the account's
    /// own confidence sets where the number sits, never across a band edge.
    /// The ordering of the cases is what the tests assert.
    public static class Suspecting
    {
        /// A sighting ties the man seen to the man in front of you only if it
        /// was good enough to know him again: a mark (rung 2) or a face (rung
        /// 3), or recognition (rung 4). A silhouette (rung 1) is "a man, big,
        /// long coat", and that is half the street.
        public static bool CanTieSighting(int rung) => rung >= 2;

        public static (double value, SuspicionLevel level, string why) Derive(
            DeedAccount account, Nearness near, double familiarity)
        {
            if (!account.Held)
                return (0.0, SuspicionLevel.Trusting, null);
            string told = string.IsNullOrWhiteSpace(account.Summary)
                ? (account.SawItMyself ? "I saw what happened" : "I heard about what happened")
                : (account.SawItMyself ? $"I saw it myself: {account.Summary.Trim()}" : $"I heard that {account.Summary.Trim()}");
            int others = Math.Max(0, near.OthersNear);

            SuspicionLevel band;
            string why;
            if (account.SawItMyself && account.Rung >= 4)
            {
                band = SuspicionLevel.Confronting;
                why = $"{told}, and it was him, I would swear to it";
            }
            else if (account.SawItMyself && CanTieSighting(account.Rung))
            {
                // THE WITNESS WHO SAW HIS FACE AT IT: she would know him again,
                // and now he is standing in front of her.
                band = SuspicionLevel.Suspicious;
                why = $"{told}; and I'd know him again, and here he is";
            }
            else if (!account.SawItMyself && account.NamesHim)
            {
                band = SuspicionLevel.Suspicious;
                why = $"{told}, and whoever saw it named him";
            }
            else if (near.SawHimMyself && others == 0)
            {
                band = SuspicionLevel.Suspicious;
                why = $"{told}; and I saw him near it at the time{Seen(near)}, and nobody else about";
            }
            else if (near.SawHimMyself)
            {
                band = SuspicionLevel.Uneasy;
                why = $"{told}; and I saw him near it at the time{Seen(near)}, though others were about too";
            }
            else if (near.HeardHeWasNear && familiarity >= Acquaintance.HeardOfYou)
            {
                // Hearsay that "Novak was about" means something only to
                // somebody who knows who Novak is.
                band = SuspicionLevel.Uneasy;
                why = $"{told}; and I heard he was near it at the time";
            }
            else
            {
                return (0.0, SuspicionLevel.Trusting, $"{told}, but nothing I know ties him to it");
            }

            // HOW THEY KNOW HIM. His own people, crew and household, give him
            // the benefit of the doubt: one band lower. Knowing is the gate
            // for naming, not for liking, and this is the liking half.
            if (familiarity >= Acquaintance.Close && band > SuspicionLevel.Trusting)
            {
                band = band - 1;
                why += "; but he is one of my own, and I would rather it was not him";
            }
            return (Place(band, account.Confidence), band, why);
        }

        static string Seen(Nearness near) =>
            string.IsNullOrWhiteSpace(near.Summary) ? "" : $" ({near.Summary.Trim()})";

        /// The band's floor plus up to half its width, by the account's
        /// confidence: the level is the case's, the number carries the doubt.
        static double Place(SuspicionLevel band, double confidence)
        {
            double lo, hi;
            switch (band)
            {
                case SuspicionLevel.Uneasy: lo = 0.25; hi = 0.50; break;
                case SuspicionLevel.Suspicious: lo = 0.50; hi = 0.80; break;
                case SuspicionLevel.Confronting: lo = 0.80; hi = 1.00; break;
                default: return 0.0;
            }
            return lo + (hi - lo) * 0.5 * Math.Clamp(confidence, 0.0, 1.0);
        }
    }
}
