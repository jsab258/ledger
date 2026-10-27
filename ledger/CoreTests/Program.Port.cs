using System;
using Ledger.Core;

namespace Ledger.CoreTests
{
    /// THE PORT'S RULES GIVEN THEIR HOME IN THE CORE (phase 3's port, his fallback work of 25 October).
    /// The 5 October sweep (production/audits/sweep-2026-10-05/port-vs-core.md, 1a) found five rules
    /// living only in the game's C++, with no C# source for the port to agree with. Each moved here
    /// gets its checks in this file, and its golden rows in ledger/PerceptionGolden.
    static partial class Program
    {
        /// G2, HOW WELL A WITNESS KNOWS HIS FACE FROM MEETINGS (the review's A4, 1 October): a stranger
        /// until met face to face; recognisable from the first meeting; a little more each further day
        /// met, to a cap below Close. It decides rung 4, so the report, the constable and the arrest.
        static void TestFamiliarityFromMeetings()
        {
            Console.WriteLine("Familiarity from meetings (the sweep's G2):");

            Check(Acquaintance.FromMeetings(0) == Acquaintance.Stranger && !Acquaintance.CanNameYou(Acquaintance.FromMeetings(0)),
                  "never met: a stranger, who cannot name him");
            Check(Acquaintance.FromMeetings(-3) == Acquaintance.Stranger,
                  "a negative count is never met, not a negative familiarity");
            Check(Acquaintance.CanNameYou(Acquaintance.FromMeetings(1)) && Math.Abs(Acquaintance.FromMeetings(1) - 0.4) < 1e-12,
                  "the first meeting puts him over recognition, at 0.4",
                  $"{Acquaintance.FromMeetings(1)}");
            Check(Math.Abs(Acquaintance.FromMeetings(2) - Acquaintance.FromMeetings(1) - 0.1) < 1e-12,
                  "each further day met adds 0.1");
            Check(Math.Abs(Acquaintance.FromMeetings(4) - 0.7) < 1e-12 && Acquaintance.FromMeetings(40) == Acquaintance.FromMeetings(4),
                  "it stops at 0.7 from the fourth day",
                  $"{Acquaintance.FromMeetings(4)} / {Acquaintance.FromMeetings(40)}");
            Check(Acquaintance.FromMeetings(int.MaxValue) < Acquaintance.Close,
                  "meeting him, however often, is not walking with him: always below Close");
            Check(Acquaintance.HeardOfYou < Acquaintance.FromMeetings(1),
                  "one meeting knows him better than having heard of him");
        }

        /// G1's rules, the first part: WHO SAW THE WINDOW GO AND WHAT THEY DO (the review's A1, A5 and B-b; the night
        /// of the game's own clock). The geography (who stands where at the hour) stays in the port for now.
        static void TestSighting()
        {
            Console.WriteLine("Sighting (the sweep's G1, its rules):");

            Check(Sighting.NightAt(19) && Sighting.NightAt(2) && Sighting.NightAt(6) && !Sighting.NightAt(7)
                  && !Sighting.NightAt(12) && !Sighting.NightAt(18),
                  "night is 19:00 to 07:00, the game's own clock");
            Check(Sighting.NightAt(-1) && Sighting.NightAt(43) && !Sighting.NightAt(31),
                  "an hour outside the day wraps round it");
            Check(Sighting.LightOnHim(false, 0.0) == 1.0 && Sighting.LightOnHim(true, 0.0) == 0.0,
                  "daylight lights him fully; the night alone not at all");
            Check(Math.Abs(Sighting.LightOnHim(true, 0.6) - 0.6) < 1e-12 && Sighting.LightOnHim(false, 0.6) == 1.0,
                  "at night a lamp's reach is his light; by day it adds nothing past full");
            Check(Sighting.LightOnHim(true, 3.0) == 1.0 && Sighting.LightOnHim(true, -1.0) == 0.0,
                  "a lamp's reach is held to 0 to 1");
            Check(Sighting.DeedSeconds == 1.0, "anybody with a clear line on him watched the deed one second");
            Check(Sighting.WhatWitnessFiles(0, false) == WitnessFiles.NoiseOnly && Sighting.WhatWitnessFiles(0, true) == WitnessFiles.NoiseOnly,
                  "a noise or no sighting files only the noise, never a story about him");
            Check(Sighting.WhatWitnessFiles(2, true) == WitnessFiles.StoryAboutHim && Sighting.WhatWitnessFiles(2, false) == WitnessFiles.Nothing,
                  "a sighting files a story only when the witness bank has words for it");
            Check(!Sighting.WitnessShouts(0) && Sighting.WitnessShouts(1) && Sighting.WitnessShouts(3),
                  "only somebody who saw it shouts at him");
        }

        /// W1, ONE TOWN SAVE: the bundle's version says whether it carries the game's hints and what he has heard
        /// (2), or whether a version-1 save left them to the files beside it.
        static void TestTownSaveVersion()
        {
            Console.WriteLine("The town's save, its version (the sweep's W1):");
            TownSave Read(string json) => TownSave.FromJson(MiniJson.AsObject(MiniJson.Deserialize(json)));
            Check(TownSave.Version == 2, "the bundle is version 2: the game's saves carry the hints and what he has heard");
            Check(Read("{\"version\": 1}").ReadVersion == 1, "a version-1 save says so, so its empty hints are not taken for the game's");
            Check(Read("{\"version\": 2}").ReadVersion == 2 && Read("{}").ReadVersion == TownSave.Version,
                  "a version-2 save, and one that gives no version, are read as this build's");
            Check(Read(MiniJson.Serialize(new TownSave().ToJson())).ReadVersion == 2,
                  "a save this build writes reads back as version 2, so its load trusts the bundle");
        }

        /// G1's geography, the second part: WHO STANDS WHERE ON QUAY STREET AT THE HOUR, and which way they look.
        static void TestSightingGeography()
        {
            Console.WriteLine("Sighting (the sweep's G1, its geography):");

            Check(Sighting.OnQuayStreet(-10.0, 10.0) && Sighting.OnQuayStreet(50.0, -10.0) && !Sighting.OnQuayStreet(50.1, 0.0) && !Sighting.OnQuayStreet(0.0, 10.1),
                  "Quay Street runs from 10 m below the quay's end to 50 m up, 10 m either side of its middle");
            Check(Sighting.IndoorPlace(7.0) && Sighting.IndoorPlace(-7.5) && !Sighting.IndoorPlace(6.99),
                  "a place 7 m or more from the street's middle is behind a window");
            Check(Sighting.BodySpot(12.0, 7.5) == (12.0, 4.6) && Sighting.BodySpot(12.0, -7.5) == (12.0, -4.6) && Sighting.BodySpot(12.0, 2.0) == (12.0, 2.0),
                  "an inside place's body stands on its own pavement, straight out from it; outside, where the place is");
            Check(Sighting.StreetFacingYaw(5.0, 0.2) == 0.0 && Sighting.StreetFacingYaw(5.0, 4.6) == -90.0 && Sighting.StreetFacingYaw(5.0, -4.6) == 90.0,
                  "in the street's middle one looks up it; at the side, across it");

            const string json = "{\"talk_range_m\":6,\"places\":{" +
                "\"office\":{\"x_m\":0,\"z_m\":7.5,\"body_x_m\":3.75},\"cafe\":{\"x_m\":25,\"z_m\":-7.5},\"pavement\":{\"x_m\":10,\"z_m\":2}}," +
                "\"people\":[" +
                "{\"id\":\"inside\",\"routine\":[[0,\"cafe\"]]}," +
                "{\"id\":\"outside\",\"routine\":[[0,\"pavement\"]]}," +
                "{\"id\":\"bodied\",\"routine\":[[0,\"office\"]]}," +
                "{\"id\":\"bodied_out\",\"routine\":[[0,\"pavement\"]]}," +
                "{\"id\":\"home\",\"routine\":[[0,\"off\"]]}],\"ties\":[]}";
            var cast = CastDay.Parse(json);
            Check(cast.BodyXOf("office") == 3.75 && cast.BodyXOf("cafe") == null, "the cast file's body_x_m is read, and only where given");
            Check(Sighting.BodySpot(cast, "office", 0.0, 7.5) == (3.75, 4.6), "a place's body waits where its body_x_m says along the pavement");
            var seen = Sighting.OnlookersAt(cast, 0, 12, new[] { "bodied", "bodied_out" });
            var ids = string.Join(",", seen.ConvertAll(o => o.Id));
            Check(ids == "inside,bodied,bodied_out", "the onlookers: somebody inside, and every body on the street; not somebody outside with no body, nor anyone at home", ids);
            var bodied = seen.Find(o => o.Id == "bodied");
            Check(bodied != null && bodied.Body && bodied.X == 3.75 && bodied.Z == 4.6 && bodied.YawDeg == -90.0 && bodied.Place == "office",
                  "a body for an inside place stands at its waiting spot on the pavement, looking across the street");
            var inside = seen.Find(o => o.Id == "inside");
            Check(inside != null && !inside.Body && inside.X == 25.0 && inside.Z == -7.5 && inside.YawDeg == 90.0,
                  "somebody inside is at their place, looking out at the street");
            bool refused = false;
            try { CastDay.Parse(json.Replace("\"body_x_m\":3.75", "\"body_x_m\":\"door\"")); } catch (FormatException) { refused = true; }
            Check(refused, "a body_x_m that is not a number is refused, as the game's own reading refuses it");
        }
    }
}
