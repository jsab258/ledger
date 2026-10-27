using System;
using System.Collections.Generic;

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

        // WHO STANDS WHERE ON QUAY STREET AT THE HOUR (27 October 2026, the sweep's G1, its second part): the geography
        // the port kept when the rules above came home. Street metres: x along Quay Street, z across it from its middle.

        /// Within Quay Street's own stretch.
        public static bool OnQuayStreet(double x, double z) => x >= -10.0 && x <= 50.0 && Math.Abs(z) <= 10.0;

        /// The counters, the office and the cafe stand 7.5 m either side of the street's middle, behind their windows
        /// (hook-cast.json's places).
        public static bool IndoorPlace(double z) => Math.Abs(z) >= 7.0;

        /// Where a body stands for a place: an inside place's on its own pavement, straight out from it.
        public static (double x, double z) BodySpot(double x, double z) => IndoorPlace(z) ? (x, z > 0.0 ? 4.6 : -4.6) : (x, z);

        /// THE SAME, AT THE PLACE'S OWN WAITING SPOT (7 October, item 1.1's second fresh review: Sheila, in the locked
        /// office by her day, stood on the pavement straight out from its middle, square in front of Mickey's window and
        /// its camera): along the pavement where the file's "body_x_m" says, else straight out.
        public static (double x, double z) BodySpot(CastDay cast, string place, double x, double z) => BodySpot(cast.BodyXOf(place) ?? x, z);

        /// The yaw, in degrees, that faces from one point to another (0 up the street, 90 across it towards +z).
        public static double YawToFace(double fromX, double fromZ, double toX, double toZ) =>
            Math.Atan2(toZ - fromZ, toX - fromX) * 180.0 / Math.PI;

        /// Which way somebody at a place looks: out at the street (up it from the quay, in its middle).
        public static double StreetFacingYaw(double x, double z) =>
            Math.Abs(z) < 0.5 ? YawToFace(x, z, x + 10.0, z) : YawToFace(x, z, x, 0.0);

        /// One person on Quay Street at the hour who could see the window go: where they stand and which way they look.
        public sealed class Onlooker
        {
            public string Id, Place;
            /// A body stands for them in the street; otherwise they are inside their place, behind its window.
            public bool Body;
            public double X, Z, YawDeg;
        }

        /// THE ONLOOKERS AT AN HOUR: everybody on Quay Street then by the town's own rule (CastDay.OnQuayStreet, the
        /// street's own areas, as DS Ellis asks there; the review's A11), each where they stand: a body at its place's
        /// waiting spot, or somebody inside, at their place; a person with no body who is not inside is not counted.
        public static List<Onlooker> OnlookersAt(CastDay cast, int day, int hour, ICollection<string> withBodies)
        {
            var found = new List<Onlooker>();
            foreach (var id in cast.People)
            {
                var where = cast.Where(id, day, hour);
                var place = cast.PlaceOf(id, day, hour);
                if (where == null || place == null) continue;
                if (!cast.OnQuayStreet(id, day, hour)) continue;
                bool body = withBodies != null && withBodies.Contains(id);
                if (!body && !IndoorPlace(where.Value.z)) continue;
                var at = body ? BodySpot(cast, place, where.Value.x, where.Value.z) : where.Value;
                found.Add(new Onlooker { Id = id, Place = place, Body = body, X = at.x, Z = at.z, YawDeg = StreetFacingYaw(at.x, at.z) });
            }
            return found;
        }
    }
}
