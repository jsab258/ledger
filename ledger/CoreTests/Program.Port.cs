using System;
using System.Collections.Generic;
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

        /// U3, THE REACTION LADDER AT A BROKEN WINDOW (ported 27 October 2026; production/audits/sweep-2026-10-05/
        /// U3-DESIGN-2026-10-27.md): what a witness got decides how bad it was, and their nerve what they do. At a
        /// window nobody flees, fetches the law or steps in; that needs a body or worse.
        static void TestReactionAtTheWindow()
        {
            Console.WriteLine("The reaction ladder at the window (the sweep's U3):");
            var noise = new Observation { Slots = Slot.None };
            var act = new Observation { Slots = Slot.Act };
            var actAndFlight = new Observation { Slots = Slot.Act | Slot.Flight };
            Check(Reaction.Severity(noise) == 0 && Reaction.Severity(null) == 0, "nothing got is nothing to react to");
            Check(Math.Abs(Reaction.Severity(act) - 0.40) < 1e-12 && Math.Abs(Reaction.Severity(actAndFlight) - 0.45) < 1e-12,
                  "the act alone is 0.40; the act and the flight 0.45", $"{Reaction.Severity(act)} / {Reaction.Severity(actAndFlight)}");
            Check(Reaction.Decide(0.10, 0.5, 0.5, 0.5, false, false) == Reacted.Notice, "a noise alone turns a head");
            Check(Reaction.Decide(Reaction.Severity(act), 0.9, 0.9, 0.9, false, false) == Reacted.Notice,
                  "the act alone, however bold the witness, turns a head");
            Check(Reaction.Decide(Reaction.Severity(actAndFlight), 0.6, 0.5, 0.5, false, false) == Reacted.Investigate,
                  "the act and the flight: a bold witness walks toward it");
            Check(Reaction.Decide(Reaction.Severity(actAndFlight), 0.3, 0.5, 0.5, false, false) == Reacted.Alarm
                  && Reaction.LoudnessOf(Reacted.Alarm) == Perception.LoudShout,
                  "a timid one shouts, and the shout is a loud sound others hear");
            bool anyGraver = false;
            foreach (var nerve in new[] { 0.0, 0.2, 0.5, 0.9, 1.0 })
                foreach (var dutiful in new[] { 0.0, 1.0 })
                {
                    var r = Reaction.Decide(Reaction.Severity(actAndFlight), nerve, dutiful, 1.0, false, true);
                    anyGraver |= r == Reacted.Flee || r == Reacted.FetchTheLaw || r == Reacted.Intervene || r == Reacted.Deliver;
                }
            Check(!anyGraver, "at a window nobody flees, fetches the law, steps in or goes to tell");
            Check(Reaction.Decide(1.0, 0.5, 0.9, 0.5, true, false) == Reacted.FetchTheLaw,
                  "a body with a dutiful witness fetches the law (his ruling keeps Mickey's people below it)");
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

        /// G4, THE GAME'S HOURLY STEP (28 October 2026): TownWeek, which lived only in the port's TownWeek.h and the
        /// reference week's own loop. The three calls the sweep could remove unseen (P1, P3, P11), each where it shows.
        static void TestTownWeek()
        {
            Console.WriteLine("The town's week, hour by hour (the sweep's G4):");

            GossipMill Landing()
            {
                var m = new GossipMill(null);
                foreach (var id in new[] { Arrangement.Doorman, Arrangement.OutfitMan })
                    m.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker()));
                return m;
            }
            string Told(GossipMill m, int night) =>
                m.Get(Arrangement.OutfitMan).Rumors.Find(r => r.TopicKey == "player.outfit_d" + night)?.Content.Value ?? "none";

            // His no at half past nine: the landing has it when Ron goes down at eleven, as that hour turns (P1).
            var no = new TownWeek();
            var noMill = Landing();
            var told = new List<string>();
            for (int h = 20; h <= 23; h++)
            {
                var now = new GameTime(0, h, 0);
                no.Six(noMill, now);
                no.TwentyRon(noMill, now);
                if (h == 21) no.AnswerAsk(0, NightAnswer.Refused, noMill, new GameTime(0, 21, 30));
                told.Add(h + ":" + Told(noMill, 0));
            }
            Check(string.Join(",", told) == "20:none,21:none,22:none,23:refused",
                  "his no reaches the landing as eleven turns, through the hour's step", string.Join(",", told));

            // A night he stayed away passes at four, as the hour turns, not at the dawn's six (P1).
            var away = new TownWeek();
            var awayMill = Landing();
            away.TwentyRon(awayMill, new GameTime(0, 20, 0));
            var passed = new List<string>();
            for (int h = 1; h <= 6; h++)
            {
                away.Six(awayMill, new GameTime(1, h, 0));
                passed.Add(h + ":" + Told(awayMill, 0));
            }
            Check(string.Join(",", passed) == "1:none,2:none,3:none,4:noshow,5:noshow,6:noshow" && away.Asks.Nights[0] == NightAnswer.NoShow,
                  "a night away passes at four, told to the landing then", string.Join(",", passed));

            // The dawn's own call repeats what TellDue did as the hour turned (the sweep's P11 changes nothing).
            var dawn = new TownWeek();
            var dawnMill = Landing();
            dawn.TwentyRon(dawnMill, new GameTime(0, 20, 0));
            dawn.Asks.TellDue(dawnMill, new GameTime(1, 6, 0));
            int heldBefore = dawnMill.Get(Arrangement.OutfitMan).Rumors.Count;
            dawn.Asks.PassedTo(1, dawnMill, new GameTime(1, 6, 0));
            Check(dawnMill.Get(Arrangement.OutfitMan).Rumors.Count == heldBefore && dawn.Asks.Nights.Count == 1,
                  "at six, PassedTo after TellDue in the same hour adds nothing");

            // Ron's envelope is not brought while he is in the cells, and is once he is out (P3).
            var held = new TownWeek();
            var heldMill = Landing();
            held.Police.Report("sam", "player.cut_d0", Offence.Wounding, 4, 0);
            held.Arrests.Add(held.Police.TakeIn("player.cut_d0", new GameTime(0, 14, 0), false, false));
            Check(held.Holding(new GameTime(0, 20, 0)) != null && !held.TwentyRon(heldMill, new GameTime(0, 20, 0)) && !held.Asks.WasDelivered(0),
                  "in the cells at eight, Ron does not bring the envelope");
            var free = new TownWeek();
            Check(free.TwentyRon(Landing(), new GameTime(0, 20, 0)) && free.Asks.WasDelivered(0),
                  "free at eight on an ask night, he does");
            Check(!new TownWeek().TwentyRon(Landing(), new GameTime(0, 21, 0)), "and only at eight");
        }

        /// THE HARD RULE ON NAMES (his order of 27 October 2026, evening; NameRules, its reference
        /// tools/checkers/name_rule.py): a sentence naming a person, place or event missing from the speaker's facts
        /// never passes, and the check refuses it before any call.
        static void TestNameRule()
        {
            Console.WriteLine("The hard rule on names:");
            Check(NameRuleShipped && NameRuleWiderShipped, "the game ships with the rule on, its wider form too (his answer of 28 October)");
            Check(TwoCopiesShipped, "the game ships with two copies of each check call (his answer of 28 October)");
            ClaimCheck.NameRule = true;
            var facts = new[] { "C1: Ron Kirby keeps Mickey's door and the rank.", "P17: Hal keeps the coin shop on Quay Street." };
            Check(NameRules.Missing("Hal runs it from the coin shop.", facts).Count == 0, "a name in the facts passes");
            Check(string.Join("|", NameRules.Missing("Frank Doyle runs it now.", facts)) == "Frank Doyle", "an invented person is refused");
            Check(string.Join("|", NameRules.Missing("I heard it from Father Walsh.", facts)) == "Father Walsh", "a title does not make a name known");
            Check(NameRules.Missing("Mickey's door shuts on a Sunday in November.", facts).Count == 0, "days and months are times, not names");
            Check(string.Join("|", NameRules.Missing("He came up from Leeds.", facts)) == "Leeds", "a place missing from the facts is refused");
            Check(NameRules.Missing("Mr Kirby keeps it.", facts).Count == 0, "a surname in the facts makes the name known");
            Check(string.Join("|", NameRules.Missing("The Crown shuts at ten on Mondays.", facts)) == "The Crown", "a common word never makes a name known");
            Check(NameRules.Missing("Head down Quay Street, mate.", facts).Count == 0, "a sentence's opening capital alone is no name");
            Check(NameRules.Missing("Frank was in earlier.", facts).Count == 0, "the known gap: a lone name opening a sentence is not caught");
            Check(string.Join("|", NameRules.Missing("I've kept this gate since nineteen eighty-two.", facts, true)) == "19|82",
                  "wider: a year the facts do not state is refused");
            Check(string.Join("|", NameRules.Missing("Ask the harbourmaster.", facts, true)) == "harbourmaster",
                  "wider: a role the facts do not have is refused");
            Check(NameRules.Missing("Ask the harbourmaster.", facts).Count == 0, "the wider form is off unless asked for");
            var items = new List<(string id, string text)> { ("C1", facts[0]), ("P17", facts[1]) };
            var (invented, calls) = ClaimCheck.CheckAsync(new FailingClient(), "claude-haiku-5-5", items, "Frank Doyle runs it now.",
                                                          System.Threading.CancellationToken.None).GetAwaiter().GetResult();
            Check(invented != null && invented.Count == 1 && calls.Count == 0, "the check refuses it before any call to a model");
            ClaimCheck.NameRule = false;
        }

        sealed class FailingClient : ILlmClient
        {
            public System.Threading.Tasks.Task<LlmResponse> CompleteAsync(LlmRequest request, System.Threading.CancellationToken ct = default) =>
                throw new InvalidOperationException("no call was expected");
        }

        /// THE FACTS CITED (his page note of 27 October 2026 night; ConversationEngine.CiteFacts): the reply is shown the
        /// check's numbered list and cites it after each sentence in braces, which nothing ever says, checks or keeps.
        static void TestCitedFacts()
        {
            Console.WriteLine("The facts cited:");
            Check(ConversationEngine.CiteFacts && !ConversationEngine.PlanFirst, "the game ships with the cited facts on");
            Check(ConversationEngine.WithoutCites("That's Mickey's door. {C1} Ask Sheila. {C2, P5}") == "That's Mickey's door. Ask Sheila.",
                  "the braces and their numbers are taken off", ConversationEngine.WithoutCites("That's Mickey's door. {C1} Ask Sheila. {C2, P5}"));
            Check(ConversationEngine.WithoutCites("That's Mickey's door. {C") == "That's Mickey's door.",
                  "a brace still being streamed is taken off too");
            Check(ConversationEngine.FirstSentence(ConversationEngine.WithoutCites("That's Mickey's door. {C1} Ask")) == "That's Mickey's door.",
                  "the first sentence streams out without its numbers");
            Check(ConversationEngine.WithoutCites("Aye. {}") == "Aye.", "an empty citation is taken off");
            Check(string.Join(",", ConversationEngine.CitesIn("Aye. {C1} Ask her. {C2, P5} Go on. {C1}")) == "C1,C2,P5", "what was cited, once each");
            Check(ConversationEngine.WithoutCites("No braces here.") == "No braces here.", "a reply with none is untouched");
            var card = MakeLenaCard();
            var engine = new ConversationEngine(new ScriptedLlm("unused"), card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
            string on = engine.BuildSystemPrompt("Who runs this place?", new GameTime(0, 10, 0), "In the office.");
            Check(on.Contains("Everything you know, numbered:") && on.Contains(ConversationEngine.FactsOnlyRule) && on.Contains("{C1}"),
                  "the prompt lists the facts numbered, says to keep to them, and asks for the numbers");
            ConversationEngine.CiteFacts = false;
            string off = engine.BuildSystemPrompt("Who runs this place?", new GameTime(0, 10, 0), "In the office.");
            ConversationEngine.CiteFacts = true;
            Check(!off.Contains("Everything you know, numbered:") && on.StartsWith(off.TrimEnd()), "switched off, the prompt is today's, which the cited block only follows");
        }
    }
}
