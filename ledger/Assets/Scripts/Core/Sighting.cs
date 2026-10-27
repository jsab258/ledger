namespace Ledger.Core
{
    /// What a witness files about the deed (the review's A1; Jafar's A5 ruling, 30 September).
    public enum WitnessFiles { Nothing, NoiseOnly, StoryAboutHim }

    /// WHO SAW THE WINDOW GO, AND WHAT THEY DO: THE RULES (27 October 2026, phase 3's port; the 5 October sweep's G1,
    /// production/audits/sweep-2026-10-05/port-vs-core.md). These lived only in the game's C++ (CrimeProbe.h), where
    /// nothing in the Core could disagree with them, though they decide who saw the window and so whether anyone
    /// reports him. Their home is here now; the port reads them through its golden rows. The geography (who stands
    /// where on Quay Street at the hour, from where they look) stays in the port for now.
    public static class Sighting
    {
        /// The swing and the glass going: anybody with a clear line on him watched that long.
        public const double DeedSeconds = 1.0;

        /// Night is the game's own, from 19:00 to 07:00 (ClockLight); an hour outside the day wraps round it.
        public static bool NightAt(int hour)
        {
            int h = ((hour % 24) + 24) % 24;
            return h >= 19 || h < 7;
        }

        /// The light on him (Perceivers.LevelAt's rule): daylight and the lamps that reach him, saturating; a
        /// lamp's reach held to 0 to 1.
        public static double LightOnHim(bool night, double lampReach)
        {
            double day = night ? 0.0 : 1.0;
            double l = System.Math.Max(0.0, System.Math.Min(1.0, lampReach));
            return System.Math.Max(0.0, System.Math.Min(1.0, day + l - day * l));
        }

        /// A story about him only from a sighting the witness bank has words for; a noise alone is the damage
        /// heard; otherwise nothing, never a diagnostic's words (A5: a noise or a shape is suspicion, never "he did
        /// it").
        public static WitnessFiles WhatWitnessFiles(int rung, bool bankHasWords)
        {
            if (rung <= 0) return WitnessFiles.NoiseOnly;
            return bankHasWords ? WitnessFiles.StoryAboutHim : WitnessFiles.Nothing;
        }

        /// Only somebody who saw it shouts at him.
        public static bool WitnessShouts(int rung) => rung >= 1;
    }
}
