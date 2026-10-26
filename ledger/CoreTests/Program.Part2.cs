using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

namespace Ledger.CoreTests
{
    /// THE SUITE CONTINUED (26 October 2026): Program.cs was 2 MB and the push guard refuses any changed file
    /// over 1 MB, so no test could be added; the class is cut into parts at member boundaries, unchanged.
    static partial class Program
    {
        /// A CLAIM THAT IS CAUGHT OUT DOES NOT BECOME WHAT THEY KNOW.
        ///
        /// `KnowledgeBase` says in its own summary that "an NPC cannot be
        /// talked out of what it knows", and until this test existed the code
        /// broke that invariant on the one path through which the player
        /// talks. `LawHost.Claim` caught a lie with `Claims.Process` and then
        /// handed the same lie to `GossipMill.PlayerClaims`, which learned it,
        /// and `Learn` replaces on topic: the lie was written over the
        /// witnessed fact that had just caught it.
        ///
        /// THE COST WAS ARITHMETIC, NOT RHETORIC. `Claims.Process` raises
        /// suspicion 0.15 on a contradiction and lowers it 0.03 when the story
        /// checks out, and every repeat of a stored lie read Consistent, so the
        /// fifth repetition of a caught lie cancelled the penalty for being
        /// caught and the sixth was a net gain in trust. The series below is
        /// printed rather than only asserted so that the next reader setting a
        /// bound here sets it from evidence.
        ///
        /// ACCEPTING CASE FIRST, and it is the half that matters most: a claim
        /// nobody can contradict must STILL become what they know. A guard that
        /// cannot tell a caught lie from an honest correction would quietly
        /// stop the town ever updating, which is a worse bug than the one it
        /// was written to fix.
        /// THE CORE'S FAULTS THE PORTS' REVIEWS FOUND (FINDINGS, 30 September):
        /// the builder's independent checks of the C++ ports found them in the C#
        /// the ports copy; one regression each, and rows for the port to follow
        /// (PerceptionGolden --awaiting-port, EmitPortReviewFixes).
        static void TestSweepFaults()
        {
            Console.WriteLine("-- the time-and-state sweep of the Core (30 September)");
            // 1. The talk's ageing never runs back: a late call for an earlier hour ages nothing.
            {
                double After(params int[] hours)
                {
                    var mill = new GossipMill(new SocialGraph());
                    mill.Add(new Gossiper("a", "a", new MemoryStore("a"), new KnowledgeBase(), new SuspicionTracker()));
                    mill.Get("a").Rumors.Add(new Rumor { Content = new Fact("player", "window_d1", "ritas"), Summary = "x", Confidence = 1.0, Hops = 1 });
                    foreach (var h in hours) mill.Age(new GameTime(1, h, 0));
                    return mill.Get("a").Rumors[0].Confidence;
                }
                double straight = After(10, 12), late = After(10, 12, 11, 12);
                Check(Math.Abs(straight - late) < 1e-12, "a late call to age the talk for an earlier hour ages nothing, and the next hour is not aged twice", $"{straight} {late}");
            }
            // 2. A constable's call only for today's date.
            {
                var police = new PoliceFile();
                police.Report("rita", "w1", Offence.Damage, 4, 1);
                var early = police.ConstableComes(3, new GameTime(2, 10, 0));
                var today = police.ConstableComes(3, new GameTime(3, 10, 0));
                Check(early == null && today == "w1" && police.ConstableCalls.Count == 1 && police.ConstableCalls[0].day == 3,
                      "a constable's call for a later day made today is refused and recorded nowhere; made that day, it comes", $"{early} {today} {police.ConstableCalls.Count}");
            }
            // 3. DS Ellis asks only the people on the street when she is there, the
            // town as the game builds it, each in their own world.
            {
                var cast = CastDay.Parse(File.ReadAllText(Root("production/specs/hook-cast.json")));
                var mill = new GossipMill(new SocialGraph());
                foreach (var id in cast.People)
                {
                    mill.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker(), cast.CircleOf(id)));
                    mill.Get(id).Rumors.Add(new Rumor { Content = new Fact("player", "window_d1", "ritas"), Summary = "x", Confidence = 0.9, Sensitive = true, Hops = 1 });
                }
                // Quay Street itself (canon; the cast file's places within the street):
                // not the docks, the customs shed, the ferry, the warehouses, the
                // chapel, the market, the boarding house, the flats or the allotments
                // (the independent review of 30 September, A11: she "stopped" people at
                // the chapel and the landing, and each remembered it as Quay Street).
                var quayStreet = new HashSet<string> { "mickeys", "fish_market", "ritas", "kiosk", "laundry", "quay", "adas", "cafe", "newsagent", "hals", "bus_stop" };
                foreach (var visit in new[] { new GameTime(6, 9, 0), new GameTime(2, 9, 0), new GameTime(3, 14, 0) })
                {
                    var all = PoliceFile.WhoSheAsks(mill);
                    var there = PoliceFile.WhoSheAsks(mill, cast, visit);
                    var onStreet = all.Where(id => quayStreet.Contains(cast.AreaOf(cast.PlaceOf(id, visit.Day, visit.Hour)) ?? "")).ToList();
                    if (visit.Hour == 9 && visit.Day == 2 && there.Contains("outfit_man"))
                        Check(false, "the outfit's man, at his breakfast in the cafe, is his night world's: she never asks him", "");
                    Check(there.SequenceEqual(onStreet) && there.Count > 0 && (visit.Day != 6 || !there.Contains("lena")),
                          $"DS Ellis on Quay Street at {visit} asks only the people on Quay Street then: not those at home, nor at the docks, the chapel, the landing or anywhere else in the Hook",
                          string.Join(",", there.Except(onStreet)) + " / missing " + string.Join(",", onStreet.Except(there)));
                    // And hears the street's talk only from those she asked who ever talk to the police.
                    var file = new PoliceFile();
                    file.HearTheStreet(mill, visit.Day, t => Offence.Damage, cast, visit);
                    var heard = file.Entries.Select(e => e.Who).Distinct().OrderBy(x => x, StringComparer.Ordinal).ToList();
                    var talks = onStreet.Where(id => !cast.NeverToPolice(id)).OrderBy(x => x, StringComparer.Ordinal).ToList();
                    Check(heard.SequenceEqual(talks), $"and at {visit} files the street's talk only from those she asked who ever talk to the police",
                          "heard " + string.Join(",", heard) + " / should " + string.Join(",", talks));
                }
            }
            // 4. A night Ron brought, then wound down that evening, is delivered after a load.
            {
                var a = new Arrangement(0);
                for (int n = 0; n < 6; n += Arrangement.Every) a.PassedTo(n + 1);
                bool brought = a.Delivered(6, null, new GameTime(6, 20, 0));
                bool wound = a.WoundDown(new GameTime(6, 20, 30));
                var back = Arrangement.FromJson(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(a.ToJson()))));
                Check(brought && wound && back.WasDelivered(6) && back.WoundNight == 6,
                      "a night Ron brought at eight and wound down at half past is still one he brought after a load", $"{brought} {wound} {back.WasDelivered(6)} {back.WoundNight}");
                // 5. The wound-down word waiting for the landing: a whole night, and before one.
                var json = a.ToJson();
                double atOneMinute = 7 * 1440.0 + 60;
                json["woundTell"] = new List<object> { 6.5, 6 * 1440.0 + 23 * 60 };
                var half = Arrangement.FromJson(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(json))));
                json["woundTell"] = new List<object> { 6.0, atOneMinute };
                var atOne = Arrangement.FromJson(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(json))));
                json["woundTell"] = new List<object> { 6.0, atOneMinute - 1 };
                var before = Arrangement.FromJson(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(json))));
                Check(half.WoundNight == -1 && atOne.WoundNight == -1 && before.WoundNight == 6,
                      "a saved wound-down word for night 6.5, or at one o'clock itself, is not restored; at 00:59 it is", $"{half.WoundNight} {atOne.WoundNight} {before.WoundNight}");
            }
            // 6. Ada's tea is not judged before its evening.
            {
                var tea = AdasTea.For(0, true);
                tea.SheSeesHim(new GameTime(tea.Day, 8, 0));
                var ada = new Gossiper("ada", "ada", new MemoryStore("ada"), new KnowledgeBase(), new SuspicionTracker());
                double loyal = ada.Loyalty;
                var early = tea.Close(ada, new GameTime(tea.Day - 1, 12, 0));
                Check(early == TeaState.Asked && tea.State == TeaState.Asked && ada.Loyalty == loyal && ada.Memory.Events.Count == 0,
                      "Ada's tea closed on a day before its own is still to come, not a stand-up", $"{early} {ada.Loyalty}");
            }
            // 7. A saved arrest is kept only as the police file took him.
            {
                var police = new PoliceFile();
                police.Report("rita", "w1", Offence.Damage, 4, 1);
                police.ConstableComes(2, new GameTime(2, 10, 0));
                var c = police.TakeIn("w1", new GameTime(2, 10, 0), false, false);
                var town = new TownSave { Police = police };
                town.Arrests.Add(c);
                var json = MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(town.ToJson())));
                var kept = TownSave.FromJson(json);
                var arrest = (Dictionary<string, object>)((List<object>)json["arrests"])[0];
                arrest["offence"] = "Killing";
                arrest["taken"] = 40.0 * 1440 + 600;
                var edited = TownSave.FromJson(json);
                arrest["offence"] = "Damage";
                var moved = TownSave.FromJson(json);
                Check(c != null && kept.Arrests.Count == 1 && edited.Arrests.Count == 0 && moved.Arrests.Count == 0,
                      "a saved arrest edited to another offence, or another day, than the police file took him for is not kept", $"{kept.Arrests.Count} {edited.Arrests.Count} {moved.Arrests.Count}");
                // The independent check: a description raised to a statement of another
                // offence after he was taken comes first in the file; the arrest stands.
                var file = new PoliceFile();
                file.Report("p1", "player.cut_d1", Offence.Robbery, 3, 1);
                file.Report("p2", "player.cut_d1", Offence.Wounding, 4, 1);
                file.EllisComes(new GossipMill(new SocialGraph()), 2);
                var cut = file.TakeIn("player.cut_d1", new GameTime(2, 9, 0), false, false);
                file.Report("p1", "player.cut_d1", Offence.Robbery, 4, 3);
                var townCut = new TownSave { Police = file };
                townCut.Arrests.Add(cut);
                var cutBack = TownSave.FromJson(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(townCut.ToJson()))));
                // Two arrests of one deed at the same minute, saved in an order: the
                // first saved is kept, whatever the sort (the builder's independent
                // check of the port: List.Sort is not stable).
                bool firstKept = true;
                for (int round = 0; round < 20; round++)
                {
                    var twice = MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(town.ToJson())));
                    var one = (Dictionary<string, object>)((List<object>)twice["arrests"])[0];
                    var coat = new Dictionary<string, object>(one) { ["coat"] = true };
                    // Three of one deed at one minute, differing only in the coat he wore.
                    twice["arrests"] = round % 2 == 0 ? new List<object> { one, coat, coat } : new List<object> { coat, one, one };
                    var kept2 = TownSave.FromJson(twice);
                    if (kept2.Arrests.Count != 1 || kept2.Arrests[0].CoatKept != (round % 2 == 1)) firstKept = false;
                }
                Check(firstKept, "of two arrests of one deed at the same minute, the first saved is the one kept, every time");
                Check(cut != null && cut.Offence == Offence.Wounding && cutBack.Arrests.Count == 1,
                      "an arrest for a wounding stands after a load when a robbery statement about the same deed came later and sits first in the file", $"{cut?.Offence} {cutBack.Arrests.Count}");
            }
            // 8. A deed's damage from before the first day is not read.
            {
                var dmg = new Aftermath("ritas", "player.window_d1", "Rita's window is boarded up.", new GameTime(1, 21, 0));
                var json = MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(dmg.ToJson())));
                bool fine = Aftermath.FromJson(json) != null;
                json["done"] = -50000.0;
                Check(fine && Aftermath.FromJson(json) == null, "a deed's damage saved at minus fifty thousand minutes is refused");
            }
            // 9. A memory's time only as the game writes one.
            {
                Check(GameTime.TryParse("D3 14:05", out var ok) && ok.Day == 3 && ok.Hour == 14 && ok.Minute == 5
                      && !GameTime.TryParse("D1 25:99", out _) && !GameTime.TryParse("D-3 -4:-5", out _) && !GameTime.TryParse("D2147483647 00:00", out _)
                      && !GameTime.TryParse("D100000 00:00", out _) && GameTime.TryParse("D99999 23:59", out _)
                      && MemoryEvent.FromLine("- [D1 25:99] (0.50|observation) he was about") == null
                      && MemoryEvent.FromLine("- [D1 23:59] (0.50|observation) he was about") != null,
                      "a memory's time is read only as the game writes one: hours to 23, minutes to 59, days from 0 below 100000");
            }
            // 10. The wait's lines already shown travel in the town's save.
            {
                var town = new TownSave();
                town.WaitShown.Add("ron@1");
                town.WaitShown.Add("released@4380");
                town.WaitShown.Add("sheila_answer@6");
                var json = MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(town.ToJson())));
                var back = TownSave.FromJson(json);
                var shown = (List<object>)json["shown"];
                json["shown"] = new List<object> { "ron@1", "Ron@1", "x@", "@3", "_x@3", "tea@1234567890", "tea@-1", "tea 1", 3.0, "landing@3" };
                var damaged = TownSave.FromJson(json);
                Check(back.WaitShown.SetEquals(new[] { "ron@1", "released@4380", "sheila_answer@6" }) && (string)shown[0] == "released@4380"
                      && damaged.WaitShown.SetEquals(new[] { "ron@1", "landing@3" }),
                      "the wait's lines already shown are saved in order and restored, and a key WaitStop could not make is dropped",
                      string.Join(",", damaged.WaitShown));
            }
        }

        static void TestPortReviewFaults()
        {
            Console.WriteLine("-- the Core's faults the ports' reviews found (30 September)");
            // 1. His arrival, like his name, is the street's plain fact: never a lead,
            // never his exposure.
            {
                var mill = new GossipMill(new SocialGraph());
                foreach (var id in new[] { "a", "b" }) mill.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker()));
                mill.Get("a").Rumors.Add(new Rumor { Content = new Fact("player", "arrived", "mickeys"), Summary = DayOne.ArrivalSaid, Confidence = 0.9, Hops = 0 });
                mill.Get("b").Rumors.Add(new Rumor { Content = new Fact("player", "window_d1", "ritas"), Summary = "He put Rita's window in.", Confidence = 0.9, Hops = 0 });
                var leads = mill.Leads();
                var exposure = mill.ExposureOf("player", _ => false);
                Check(leads.Count == 1 && leads[0].TopicKey == "player.window_d1" && exposure.Yours == 1,
                      "his arrival is the street's plain fact, never a lead nor his exposure, as his name is",
                      string.Join(",", leads.Select(l => l.TopicKey)) + " yours=" + exposure.Yours);
            }
            // 2. Nor what shows in anybody's manner, even marked sensitive (a damaged save).
            {
                var g = new Gossiper("s", "s", new MemoryStore("s"), new KnowledgeBase(), new SuspicionTracker());
                g.Rumors.Add(new Rumor { Content = new Fact("player", "arrived", "mickeys"), Summary = DayOne.ArrivalSaid, Confidence = 0.9, Sensitive = true, Hops = 0 });
                var shows = StreetVoice.StoryThatShows(g, 0.35);
                g.Rumors[0].Confidence = 0.1;
                var half = StreetVoice.StoryHalfRemembered(g, 0.35);
                Check(shows == null && half == null, "his arrival marked sensitive never shows in anybody's manner, nor as a half-remembered story");
            }
            // 3. His name told to somebody who had it second-hand at full certainty
            // becomes theirs first-hand, from him, once, remembered as told.
            {
                var mill = new GossipMill(new SocialGraph());
                mill.Add(new Gossiper("h", "h", new MemoryStore("h"), new KnowledgeBase(), new SuspicionTracker()));
                var id = new PlayerIdentity();
                mill.Get("h").Rumors.Add(new Rumor { Content = new Fact("player", "name", id.Surname), OriginId = "ada", Summary = "Mickey's nephew is called " + id.Surname, Confidence = 1.0, Hops = 2 });
                bool first = id.NameTold(mill, "h", new GameTime(1, 10, 0));
                bool again = id.NameTold(mill, "h", new GameTime(1, 11, 0));
                var names = mill.Get("h").Rumors.FindAll(r => r.TopicKey == PlayerIdentity.NameTopic);
                var told = mill.Get("h").Memory.Events.FindAll(e => e.Text.Contains("called " + id.Surname));
                Check(first && !again && names.Count == 1 && names[0].Hops == 0 && names[0].OriginId == "h"
                      && told.Count == 1 && told[0].Text.StartsWith("He told me himself") && !told.Exists(e => e.Text.StartsWith("I saw it myself")),
                      "his name told to somebody who had heard it at full certainty is made theirs first-hand, once, and remembered as told, never as seen",
                      $"{first} {again} {names.Count} hops={names[0].Hops} from={names[0].OriginId} " + string.Join(" / ", told.Select(e => e.Text)));
            }
            // 4. Ada's tea: ten minutes away is allowed, eleven is not.
            {
                TeaState Evening(int gapAway)
                {
                    var tea = AdasTea.For(1, true);
                    tea.SheSeesHim(new GameTime(tea.Day, 10, 0));
                    int day = tea.Day;
                    for (int m = 21 * 60 + 25; m <= 22 * 60 + 40; m++)
                    {
                        if (m > 21 * 60 + 40 && m <= 21 * 60 + 40 + gapAway) continue;
                        tea.WithHer(new GameTime(day, m / 60, m % 60));
                    }
                    var ada = new Gossiper("ada", "Ada", new MemoryStore("ada"), new KnowledgeBase(), new SuspicionTracker());
                    return tea.Close(ada, new GameTime(day, 23, 0));
                }
                var ten = Evening(10);
                var eleven = Evening(11);
                Check(ten == TeaState.Stayed && eleven == TeaState.LeftEarly,
                      "at Ada's tea ten minutes away is allowed and eleven is leaving early, as \"never away more than ten\" says", ten + " / " + eleven);
            }
            // 5. With no Ada in the mill nobody sees him go to the landing, and he is not marked seen.
            {
                var tea = AdasTea.For(1, true);
                tea.SheSeesHim(new GameTime(tea.Day, 10, 0));
                var empty = new GossipMill(new SocialGraph());
                tea.WentToTheLanding(empty, new GameTime(tea.Day, 22, 0), true);
                bool unseen = !tea.SeenGoing;
                var withAda = new GossipMill(new SocialGraph());
                withAda.Add(new Gossiper("ada", "Ada", new MemoryStore("ada"), new KnowledgeBase(), new SuspicionTracker()));
                tea.WentToTheLanding(withAda, new GameTime(tea.Day, 22, 5), true);
                Check(unseen && tea.SeenGoing && withAda.Get("ada").Rumors.Count == 1,
                      "with no Ada in the mill he is not marked seen going to the landing; with her, she sees him and holds it");
            }
            // 6. The envelope or the no only on its own night (the no then goes down
            // with Ron, tested with the outfit's talk).
            {
                var arr = new Arrangement(2);
                bool early = arr.Answer(2, NightAnswer.Did, null, new GameTime(0, 20, 0));
                bool onTheNight = arr.Answer(2, NightAnswer.Did, null, new GameTime(2, 22, 0));
                var morning = new Arrangement(0);
                bool atNine = morning.Answer(0, NightAnswer.Did, null, new GameTime(0, 9, 0));
                var late = new Arrangement(0);
                var lateMill = new GossipMill(null);
                lateMill.Add(new Gossiper(Arrangement.OutfitMan, Arrangement.OutfitMan, new MemoryStore("m"), new KnowledgeBase(), new SuspicionTracker()));
                late.Delivered(0);
                late.Answer(0, NightAnswer.Refused, lateMill, new GameTime(0, 23, 30));
                bool toldAtOnce = lateMill.Get(Arrangement.OutfitMan).Rumors.Count == 1 && !late.NoWordAt.HasValue;
                Arrangement Loaded(double minute) => Arrangement.FromJson(new Dictionary<string, object>
                {
                    { "first", 0.0 }, { "nights", new List<object> { new List<object> { 0.0, "refused" } } }, { "delivered", new List<object> { 0.0 } },
                    { "noTell", new List<object> { 0.0, minute } },
                });
                bool morningNoTell = Loaded(600).NoWordAt.HasValue, oneOClock = Loaded(1500).NoWordAt.HasValue, elevenOk = Loaded(1380).NoWordAt.HasValue;
                Check(!early && onTheNight && !atNine && toldAtOnce && !morningNoTell && !oneOClock && elevenOk,
                      "the envelope only on its own night and while the landing is open; a no after eleven reaches the landing at once; a save's waiting no only between eleven and one",
                      $"{early} {onTheNight} {atNine} {toldAtOnce} {morningNoTell} {oneOClock} {elevenOk}");
            }
            // 7. A far-future day is walked no further than a save can hold.
            {
                var far = new Arrangement(0);
                var clock = System.Diagnostics.Stopwatch.StartNew();
                far.PassedTo(10000000);
                Check(far.Nights.Count <= Arrangement.LastDay / Arrangement.Every + 1 && clock.ElapsedMilliseconds < 2000,
                      "a far-future day is walked no further than the save's last day", far.Nights.Count + " nights, " + clock.ElapsedMilliseconds + " ms");
            }
            // 8. His plain answer at 00:00 is overheard like any other; only the day
            // closing unanswered at midnight is Sheila's alone.
            {
                var cast = CastDay.Parse("{\"talk_range_m\":6,\"places\":{\"" + WeeksEnd.Office + "\":{\"x_m\":0,\"z_m\":0}},"
                    + "\"areas\":{\"mickeys\":{\"places\":[\"" + WeeksEnd.Office + "\"]}},"
                    + "\"people\":[{\"id\":\"lena\",\"routine\":[[0,\"" + WeeksEnd.Office + "\"]]},{\"id\":\"rocco\",\"routine\":[[0,\"" + WeeksEnd.Office + "\"]]}],\"ties\":[]}");
                GossipMill Mill() { var m = new GossipMill(null); foreach (var id in new[] { "lena", "rocco" }) m.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker())); return m; }
                var said = Mill();
                var wk = new WeeksEnd();
                wk.Ask(new GameTime(7, 0, 0), true);
                bool given = wk.Give(WeekAnswer.TakeOver, new GameTime(7, 0, 0), said, cast);
                var closed = Mill();
                var unanswered = new WeeksEnd();
                unanswered.Ask(new GameTime(7, 0, 0), true);
                unanswered.Close(new GameTime(8, 0, 0), closed, cast);
                Check(given && said.Get("rocco").Rumors.Count == 1 && closed.Get("rocco").Rumors.Count == 0 && closed.Get("lena").Rumors.Count == 1,
                      "a plain answer given at midnight is overheard like any other; only the day closing unanswered is Sheila's alone",
                      said.Get("rocco").Rumors.Count + " / " + closed.Get("rocco").Rumors.Count);
            }
            // 9. The police file's visits load by day, those of one day in the order saved.
            {
                var visits = new List<object>();
                for (int k = 0; k < 20; k++) visits.Add(new List<object> { (double)(k % 2 == 0 ? 6 : 5), "Wounding mark" + k });
                var reports = new List<object>();
                for (int k = 0; k < 20; k++) reports.Add(new Dictionary<string, object> { { "who", "w" + k }, { "topic", "mark" + k }, { "offence", "Wounding" }, { "how", "Statement" }, { "day", 1.0 } });
                var loaded = PoliceFile.FromJson(new Dictionary<string, object> { { "entries", reports }, { "visits", visits } });
                var sixes = loaded.Visits.Where(v => v.day == 6).Select(v => v.why).ToList();
                var wantSixes = Enumerable.Range(0, 20).Where(k => k % 2 == 0).Select(k => "Wounding mark" + k).ToList();
                Check(loaded.Visits.Count == 20 && loaded.Visits[0].day == 5 && sixes.SequenceEqual(wantSixes),
                      "the police file's visits load by day, and those of one day in the order they were saved", string.Join(",", sixes));
            }
            // 10. No constable calls while he is in the cells: the other window waits for its call.
            {
                var file = new PoliceFile();
                file.Report("rita", "player.window_d1", Offence.Damage, 4, 1);
                file.Report("hal", "player.window_d2", Offence.Damage, 4, 2);
                var held = file.TakeIn("player.window_d1", new GameTime(3, 8, 0), false, false);
                string whileHeld = held == null ? "not held" : file.ConstableComes(3, new GameTime(3, 10, 0)) ?? "none";
                int callsWhileHeld = file.ConstableCalls.Count;
                string after = file.ConstableComes(4, new GameTime(4, 10, 0));
                Check(held != null && whileHeld == "none" && callsWhileHeld == 0 && after == "player.window_d2",
                      "no constable calls while he is in the cells, so the other window waits for its call instead of being used up",
                      $"{whileHeld} {callsWhileHeld} {after}");
            }
            // 12. The wait near the largest day: a constable due still stops it, and it ends.
            {
                var file = new PoliceFile();
                file.Report("rita", "player.window_d1", Offence.Damage, 4, 1);
                int top = int.MaxValue - 5;
                var stop = Waiting.Next(new GameTime(top, 8, 0), new GameTime(int.MaxValue, 23, 0), new WaitBeats { Police = file });
                var last = Waiting.Next(new GameTime(int.MaxValue, 11, 0), new GameTime(int.MaxValue, 23, 0), new WaitBeats { Police = file });
                Check(stop != null && stop.Why == "constable" && stop.At.Day == top && last == null,
                      "near the largest day the wait still stops for a constable due, and a wait on the last day ends", stop?.Why ?? "none");
            }
            // 13. A telling's wording is one, whatever the story's first letter.
            {
                string capital = StreetVoice.Unfill("Here, Hal and Rita had words.", "Hal and Rita had words");
                string lower = StreetVoice.Unfill("Here, the new owner was out late.", "the new owner was out late");
                var led = new RemarkLedger();
                led.HeardLine("exchange/tell/news", "Here, {What}.");
                string next = led.Fresh("exchange/tell/news", new[] { "Here, {what}.", "Did you hear? {what}." }, 0);
                Check(capital == "Here, {what}." && capital == lower && next == "Did you hear? {what}.",
                      "a telling's wording is one whatever the story's first letter, and a wording saved the old way counts as heard", capital + " | " + lower + " | " + next);
            }
            // 14. The town's news refuses a day no save could hold, or a fraction.
            {
                string News(string day, string hour) =>
                    "{\"stories\":[{\"id\":\"x\",\"summary\":\"Hal and Rita had words\",\"area\":\"ritas\",\"day\":" + day + ",\"hour\":" + hour +
                    ",\"fact\":[\"town\",\"x_d0\",\"seen\"],\"confidence\":0.9,\"parties\":[\"hal\",\"rita\"]}]}";
                bool Refused(string day, string hour) { try { TownNews.Parse(News(day, hour)); return false; } catch (FormatException) { return true; } }
                Check(!Refused("2", "10") && Refused("1e10", "10") && Refused("2.5", "10") && Refused("-1", "10") && Refused("2", "10.5"),
                      "the town's news refuses a day no save could hold, a fraction of a day or an hour, or a day before the first");
            }
            // 11. A police save keeps only what play could make.
            {
                var e = new List<object>
                {
                    new Dictionary<string, object> { { "who", "rita" }, { "topic", "player.window_d1" }, { "offence", "Damage" }, { "how", "Statement" }, { "day", 1.0 } },
                    new Dictionary<string, object> { { "who", "hal" }, { "topic", "player.window_d2" }, { "offence", "Damage" }, { "how", "Statement" }, { "day", 1.0 } },
                };
                var saved = new Dictionary<string, object>
                {
                    { "entries", e },
                    { "visits", new List<object> { new List<object> { 2.0, "talk" }, new List<object> { 4.0, "Wounding player.cut_d1" }, new List<object> { 3.0, "talk" } } },
                    { "calls", new List<object> { new List<object> { 2.0, "player.window_d1" }, new List<object> { 2.0, "player.window_d2" } } },
                    { "taken", new List<object> { new List<object> { "player.window_d1", (double)(20 * 1440) } } },
                };
                var f = PoliceFile.FromJson(saved);
                var fair = PoliceFile.FromJson(new Dictionary<string, object>
                {
                    { "entries", e }, { "calls", new List<object> { new List<object> { 2.0, "player.window_d1" } } },
                    { "taken", new List<object> { new List<object> { "player.window_d1", (double)(2 * 1440 + 16 * 60) } } },
                });
                Check(f.Visits.Count == 1 && f.Visits[0].why == "talk" && f.Visits[0].day == 3 && f.ConstableCalls.Count == 1 && !f.WasTaken("player.window_d1")
                      && fair.WasTaken("player.window_d1"),
                      "a police save keeps only what play could make: her visit for the talk from day 3, for a crime only once reported, one call a day, a spell no longer than the longest after its call",
                      string.Join(",", f.Visits.Select(v => v.day + ":" + v.why)) + " calls=" + f.ConstableCalls.Count + " taken=" + f.WasTaken("player.window_d1") + "/" + fair.WasTaken("player.window_d1"));
            }
        }

        /// THE KEY'S CAP, ENFORCED IN CODE (Jafar, 30 September): a call that could
        /// take the run past its budget is refused before it is sent; spending
        /// settles to the tokens used; a stream goes through, a plain client too.
        static void TestBudgetedClient()
        {
            Console.WriteLine("-- the key's cap, in code");
            var req = new LlmRequest { Model = Models.Ambient, MaxTokens = 300, System = new string('x', 4000) };
            req.Messages.Add(new LlmMessage("user", "hello"));
            double worst = BudgetedClient.WorstCaseUsd(req);
            double settled = 10 / 1_000_000.0 * Models.Cost[Models.Ambient].inPerM + 10 / 1_000_000.0 * Models.Cost[Models.Ambient].outPerM;
            var inner = new CountingClient();
            // A limit under one call's worst case: refused before sending.
            var tight = new BudgetedClient(inner, worst * 0.9);
            bool tightRefused;
            try { tight.CompleteAsync(req).GetAwaiter().GetResult(); tightRefused = false; } catch (BudgetSpentException) { tightRefused = true; }
            int sentUnderTight = inner.Calls;
            // A limit of a call's worst case and a half: calls go while what they
            // really cost leaves room for the next one's worst case, then stop.
            var b = new BudgetedClient(inner, worst * 1.5);
            int sent = 0;
            bool stopped = false;
            for (int k = 0; k < 1000 && !stopped; k++)
            {
                try { b.CompleteAsync(req).GetAwaiter().GetResult(); sent++; } catch (BudgetSpentException) { stopped = true; }
            }
            int expected = (int)Math.Floor((worst * 0.5) / settled) + 1;
            var unknown = new LlmRequest { Model = "some-dearer-model", MaxTokens = 100, System = "x" };
            Check(worst > 0.0012 && worst < 0.003 && tightRefused && sentUnderTight == 0 && tight.Refused == 1
                  && stopped && Math.Abs(sent - expected) <= 1 && b.SpentUsd <= b.LimitUsd
                  && BudgetedClient.WorstCaseUsd(unknown) >= BudgetedClient.WorstCaseUsd(new LlmRequest { Model = Models.Core, MaxTokens = 100, System = "x" }),
                  "a paid run's client refuses, before sending, any call whose worst case would pass its budget; what it spends settles to the tokens used, so it stops where they reach it; an unknown model is costed at the dearest rate",
                  $"worst={worst:0.0000} sent={sent} expected={expected} spent={b.SpentUsd:0.0000}");

            // A FRIENDS' EVENING (P5; Jafar, 3 October: his friends talk on his key, five dollars an
            // evening): the cap starts from what the evening has already spent, so a restarted game
            // never gets a fresh five dollars, and it reports every change so the evening can be kept.
            var late = new BudgetedClient(new CountingClient(), worst * 1.5, worst * 0.9);
            bool lateRefused;
            try { late.CompleteAsync(req).GetAwaiter().GetResult(); lateRefused = false; } catch (BudgetSpentException) { lateRefused = true; }
            var kept = new System.Collections.Generic.List<double>();
            var early = new BudgetedClient(new CountingClient(), worst * 1.5, 0.0) { OnSpent = s => kept.Add(s) };
            early.CompleteAsync(req).GetAwaiter().GetResult();
            Check(lateRefused && Math.Abs(late.SpentUsd - worst * 0.9) < 1e-12
                  && kept.Count == 2 && Math.Abs(kept[0] - worst) < 1e-12 && Math.Abs(kept[1] - settled) < 1e-12
                  && Math.Abs(new BudgetedClient(new CountingClient(), 1.0, -3.0).SpentUsd) < 1e-12,
                  "an evening's cap starts from what the evening already spent, refusing what that leaves no room for, and reports each reserve and settlement so it outlives a restart",
                  $"lateSpent={late.SpentUsd:0.0000} kept={string.Join(",", kept)}");
        }

        sealed class CountingClient : ILlmClient
        {
            public int Calls;
            public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
            {
                Calls++;
                return Task.FromResult(new LlmResponse { Text = "ok", Model = request.Model, InputTokens = 10, OutputTokens = 10 });
            }
        }

        static void TestCaughtClaimIsNotLearned()
        {
            Console.WriteLine("A caught claim is not what they know:");
            var now = new GameTime(3, 12, 0);
            Fact At(string where) => new Fact("player", "location_d2_evening", where);

            // ---- ACCEPTING: an uncaught claim is still learned ----
            {
                var (mill, _, lena) = FreshMill();
                var verdict = mill.PlayerClaims("lena", At("home"), now);
                Check(verdict == ClaimResult.Unknown,
                      "a claim about a topic the listener knows nothing about is Unknown, not refused",
                      verdict.ToString());
                Check(lena.Knowledge.CheckClaim(At("home")) == ClaimResult.Consistent,
                      "an uncaught claim STILL becomes what they know");
                Check(lena.Knowledge.Facts.Count == 1,
                      "and it is the one fact they hold on the subject",
                      lena.Knowledge.Facts.Count.ToString());

                // And it is still a lie that can catch up with them later,
                // which is the entire reason the claim is stored at all: Rocco
                // saw the warehouse, and one gossip round brings it over.
                var evs = mill.Tick(now.AddMinutes(30), (a, b) => true);
                Check(evs.Exists(e => e.ToId == "lena" && e.Contradiction),
                      "a stored claim is still exposed when the rumour reaches the person it was told to",
                      $"{evs.Count} event(s)");
            }

            // ---- ACCEPTING, THE HONEST CORRECTION ----
            // Told a place, then told the same place again. Nothing here is a
            // contradiction, so nothing is refused and the fact stands.
            {
                var (mill, _, lena) = FreshMill();
                mill.PlayerClaims("lena", At("home"), now);
                var again = mill.PlayerClaims("lena", At("home"), now.AddMinutes(5));
                Check(again == ClaimResult.Consistent, "repeating a claim they already hold is Consistent",
                      again.ToString());
                Check(lena.Knowledge.Facts.Count == 1, "and does not file a second copy",
                      lena.Knowledge.Facts.Count.ToString());
            }

            // ---- REJECTING: the planted case, the bug itself ----
            {
                var (mill, _, lena) = FreshMill();
                // THE TRUTH, PLANTED. Lena knows where the player was.
                lena.Knowledge.Learn(At("warehouse"));

                // The pair exactly as `LawHost.Claim` hand-sequences it:
                // `Claims.Process` first, then `PlayerClaims`. `GossipDirector`
                // builds every mill agent with the host's own knowledge, so
                // these two read and write ONE KnowledgeBase, which is what
                // made the overwrite possible.
                var was = Claims.Process(lena.Knowledge, lena.Suspicion, lena.Memory, At("cinema"), now);
                Check(was == ClaimResult.Contradiction, "the lie is caught", was.ToString());
                double s1 = lena.Suspicion.Value;
                Check(s1 > 0, "and catching it costs the liar something", s1.ToString("0.000"));

                var filed = mill.PlayerClaims("lena", At("cinema"), now);
                Check(filed == ClaimResult.Contradiction,
                      "and the mill REFUSES it, and says so, so a caller can count refusals",
                      filed.ToString());
                Check(lena.Knowledge.CheckClaim(At("warehouse")) == ClaimResult.Consistent,
                      "the witnessed truth is still what she knows: she cannot be talked out of it");
                Check(lena.Knowledge.CheckClaim(At("cinema")) == ClaimResult.Contradiction,
                      "and the lie is still a lie to her");
                Check(lena.Knowledge.Facts.Count == 1,
                      "one fact on the topic, not two and not the wrong one",
                      lena.Knowledge.Facts.Count.ToString());

                // IT IS STILL REMEMBERED, at two saliences: what was said
                // (0.4, from the mill) and what it was worth (0.8, from
                // Process). Refusing to BELIEVE a lie is not forgetting it.
                Check(lena.Memory.Events.Any(e => e.Text.Contains("told me")),
                      "the telling is remembered even though it was not believed");
                Check(lena.Memory.Events.Any(e => e.Text.Contains("lied")),
                      "and so is the fact that it was a lie");

                // ---- THE SERIES, PRINTED. Five repetitions of a caught lie.
                // Under the old behaviour repetitions 2..5 read Consistent and
                // each LOWERED suspicion 0.03, so the fifth value returned to
                // the first and the sixth went under it. These are the running
                // values of one variable after each repetition, not five
                // independent measurements.
                var series = new List<double> { s1 };
                for (int i = 0; i < 4; i++)
                {
                    var repeat = Claims.Process(lena.Knowledge, lena.Suspicion, lena.Memory,
                                                At("cinema"), now.AddMinutes(10 * (i + 1)));
                    Check(repeat == ClaimResult.Contradiction,
                          $"repetition {i + 2} of a caught lie is still caught", repeat.ToString());
                    var refiled = mill.PlayerClaims("lena", At("cinema"), now.AddMinutes(10 * (i + 1)));
                    Check(refiled == ClaimResult.Contradiction,
                          $"and repetition {i + 2} is still refused", refiled.ToString());
                    series.Add(lena.Suspicion.Value);
                }
                Console.WriteLine("    suspicion after each repetition of one caught lie (running value, "
                                  + $"{series.Count} repetitions): "
                                  + string.Join(" ", series.Select(v => v.ToString("0.000"))));
                Check(series[4] >= series[0],
                      "repeating a lie they have already caught never buys trust back",
                      $"first={series[0]:0.000} fifth={series[4]:0.000}");
                Check(lena.Knowledge.Facts.Count == 1 && lena.Knowledge.CheckClaim(At("warehouse")) == ClaimResult.Consistent,
                      "and after five tellings she still knows the warehouse");

                // ---- THE RATCHET GUARD ----
                // A guard that cannot tell a regression from an improvement is
                // a ratchet. Telling the TRUTH after all that must still read
                // Consistent and must still buy the 0.03 back: the fix refuses
                // lies, not claims.
                double before = lena.Suspicion.Value;
                var honest = Claims.Process(lena.Knowledge, lena.Suspicion, lena.Memory,
                                            At("warehouse"), now.AddMinutes(60));
                double after = lena.Suspicion.Value;
                Check(honest == ClaimResult.Consistent,
                      "the truth still checks out after the lies", honest.ToString());
                Check(Math.Abs((before - after) - 0.03) < 1e-9,
                      "and still lowers suspicion by the 0.03 it always did",
                      $"before={before:0.000} after={after:0.000} delta={before - after:0.000}");
                var truthful = mill.PlayerClaims("lena", At("warehouse"), now.AddMinutes(60));
                Check(truthful == ClaimResult.Consistent && lena.Knowledge.Facts.Count == 1,
                      "and the mill files the true claim rather than refusing it", truthful.ToString());
            }

            // ---- THE SECOND SOURCE: truth that arrived by being SEEN ----
            // The planted case above used `Learn` directly. This one never
            // calls `Learn` from the test at all: `Witness` at certainty is
            // what promotes a sighting into hard knowledge (Gossip.cs, "only
            // certainty becomes hard knowledge"), so the refusal is a property
            // of what she knows and not of how the test put it there.
            {
                var (mill, _, lena) = FreshMill();
                mill.Witness("lena", At("warehouse"), "I watched him walk in", false, now, 0.95);
                Check(lena.Knowledge.CheckClaim(At("warehouse")) == ClaimResult.Consistent,
                      "a certain sighting is hard knowledge");
                var seen = mill.PlayerClaims("lena", At("cinema"), now.AddMinutes(5));
                Check(seen == ClaimResult.Contradiction,
                      "a lie told to an eyewitness is refused too", seen.ToString());
                Check(lena.Knowledge.CheckClaim(At("warehouse")) == ClaimResult.Consistent
                      && lena.Knowledge.Facts.Count == 1,
                      "and what she saw with her own eyes survives being lied to");

                // THE OTHER HALF OF THE BOUND: a sighting BELOW certainty is
                // not knowledge, so the same lie is learned. This is what keeps
                // the guard from being a ratchet at the confidence threshold,
                // and it is why the 2026-09-06 sweep could never see this bug:
                // that grid filed sightings at 0.9.
                var (mill2, _, lena2) = FreshMill();
                mill2.Witness("lena", At("warehouse"), "I think I saw him", false, now, 0.9);
                var doubtful = mill2.PlayerClaims("lena", At("cinema"), now.AddMinutes(5));
                Check(doubtful == ClaimResult.Unknown,
                      "a doubtful sighting is not knowledge, so the claim is not refused",
                      doubtful.ToString());
                Check(lena2.Knowledge.CheckClaim(At("cinema")) == ClaimResult.Consistent,
                      "and somebody who only half-saw you does take your word for it");
            }
        }

        static async Task TestReflection()
        {
            Console.WriteLine("Reflection:");
            var llm = new FakeLlm { NextReply = "- The new owner lies when cornered.\n- I should watch the books more closely.\n" };
            var card = MakeLenaCard();
            var memory = new MemoryStore("lena");
            memory.Append(new MemoryEvent(new GameTime(3, 12, 0), "observation", 0.8, "The player lied about the cinema."));
            var engine = new ConversationEngine(llm, card, memory, new KnowledgeBase(), new SuspicionTracker(), new CostTracker());

            await engine.ReflectAsync(3, new GameTime(3, 23, 0));
            Check(memory.Beliefs.Count == 2, "reflection replaced beliefs");
            Check(memory.Beliefs[0].Contains("lies when cornered"), "belief content from model");
            Check(llm.LastRequest.Messages[0].Content.Contains("cinema"), "reflection prompt carries the day's events");
        }

        static async Task TestTranscriptRollback()
        {
            Console.WriteLine("Transcript rollback:");
            var llm = new FakeLlm();
            var engine = new ConversationEngine(llm, MakeLenaCard(), new MemoryStore("lena"),
                new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
            var now = new GameTime(1, 12, 0);

            // A failed call must roll back the user turn it optimistically appended,
            // or the transcript (and the API request) carries a phantom orphaned turn.
            llm.ThrowNext = new LlmApiException(503, "overloaded");
            bool threw = false;
            try { await engine.SayToAsync("first turn, this one fails", now); }
            catch (LlmApiException) { threw = true; }
            Check(threw, "SayToAsync propagates the API failure");

            var reply = await engine.SayToAsync("second turn, this one works", now.AddMinutes(1));
            Check(reply == "Hm. Is that so.", "engine recovers on the next turn after a failure");
            Check(llm.LastRequest.Messages.Count == 1, "the failed user turn was rolled back (no orphan)");
            Check(llm.LastRequest.Messages[0].Content.Contains("second turn"),
                "transcript contains only the successful turn");

            bool leaked = false;
            foreach (var e in engine.Memory.Events)
                if (e.Text.Contains("first turn")) leaked = true;
            Check(!leaked, "the failed turn wrote nothing to memory");
        }

        static async Task TestRetryAndErrors()
        {
            Console.WriteLine("AnthropicClient retry/errors:");

            AnthropicClient Client(ScriptedHandler h)
            {
                var c = new AnthropicClient("test-key", handler: h);
                c.RetryDelay = _ => TimeSpan.Zero; // don't actually sleep in tests
                return c;
            }

            // 200 straight through.
            var hOk = new ScriptedHandler(() => Http(HttpStatusCode.OK, OkBody));
            var rOk = await Client(hOk).CompleteAsync(OneTurn());
            Check(rOk.Text == "ok" && hOk.Calls == 1, "200 parsed on the first attempt");

            // 429 then 200 → transparently retried.
            var hRate = new ScriptedHandler(
                () => Http((HttpStatusCode)429, "{}"),
                () => Http(HttpStatusCode.OK, OkBody));
            var rRate = await Client(hRate).CompleteAsync(OneTurn());
            Check(rRate.Text == "ok" && hRate.Calls == 2, "429 retried once, then succeeded");

            // Mid-flight network drop then 200 → retried.
            var hDrop = new ScriptedHandler(
                () => null, // throws HttpRequestException
                () => Http(HttpStatusCode.OK, OkBody));
            var rDrop = await Client(hDrop).CompleteAsync(OneTurn());
            Check(rDrop.Text == "ok" && hDrop.Calls == 2, "network drop retried, then succeeded");

            // Persistent 500 → retries are exhausted, then throws with the status.
            var h500 = new ScriptedHandler(() => Http(HttpStatusCode.InternalServerError,
                "{\"error\":{\"message\":\"boom\"}}"));
            var c500 = Client(h500);
            c500.MaxRetries = 2;
            bool threw500 = false;
            try { await c500.CompleteAsync(OneTurn()); }
            catch (LlmApiException ex)
            {
                threw500 = true;
                Check(ex.StatusCode == 500, "exhausted 500 surfaces as LlmApiException(500)");
                Check(ex.Message.Contains("boom"), "server error message is extracted from the body");
            }
            Check(threw500, "persistent 500 throws after retries");
            Check(h500.Calls == 3, "500 tried MaxRetries+1 times (initial + 2 retries)");

            // 400 → fails fast, no retry (client error is not the caller's to retry).
            var h400 = new ScriptedHandler(() => Http(HttpStatusCode.BadRequest,
                "{\"error\":{\"message\":\"bad request\"}}"));
            var h400Client = Client(h400);
            bool threw400 = false;
            try { await h400Client.CompleteAsync(OneTurn()); }
            catch (LlmApiException ex)
            {
                threw400 = true;
                Check(ex.StatusCode == 400 && ex.Message.Contains("bad request"), "400 surfaces its message");
            }
            Check(threw400, "400 throws");
            Check(h400.Calls == 1, "400 is not retried");

            // THE REPLY AS IT IS WRITTEN (StreamAsync, 26 September): server-sent
            // events assembled in order; an error before any text, or a stream that
            // stops short before any, falls back to the plain call; one that stops
            // short after text was handed over fails rather than pass as whole.
            static string Sse(params string[] events)
            {
                var sb = new System.Text.StringBuilder();
                foreach (var e in events) sb.Append("event: x\r\ndata: ").Append(e).Append("\r\n\r\n");
                return sb.ToString();
            }
            const string Start = "{\"type\":\"message_start\",\"message\":{\"model\":\"m\",\"usage\":{\"input_tokens\":7}}}";
            static string Delta(string t) => "{\"type\":\"content_block_delta\",\"index\":0,\"delta\":{\"type\":\"text_delta\",\"text\":\"" + t + "\"}}";
            const string Stop = "{\"type\":\"message_stop\"}";
            const string Done = "{\"type\":\"message_delta\",\"delta\":{\"stop_reason\":\"end_turn\"},\"usage\":{\"output_tokens\":4}}";
            var seen = new List<string>();
            var hs = new ScriptedHandler(() => Http(HttpStatusCode.OK, Sse(Start, Delta("Aye. "), "{\"type\":\"ping\"}", Delta("I saw him."), Done, Stop)));
            var rs = await Client(hs).StreamAsync(OneTurn(), t => seen.Add(t));
            Check(rs.Text == "Aye. I saw him." && seen.Count == 2 && seen[0] == "Aye. " && rs.StopReason == "end_turn"
                  && rs.InputTokens == 7 && rs.OutputTokens == 4, "a stream is read whole, in order, with its counts");
            var he = new ScriptedHandler(() => Http(HttpStatusCode.OK, Sse(Start, "{\"type\":\"error\",\"error\":{\"type\":\"overloaded_error\",\"message\":\"Overloaded\"}}")),
                                         () => Http(HttpStatusCode.OK, OkBody));
            bool brokeE = false;
            try { await Client(he).StreamAsync(OneTurn(), null); } catch (LlmStreamBrokenException) { brokeE = true; }
            Check(brokeE && he.Calls == 1, "an error mid-stream is reported as a broken stream, not retried here");
            var hshort = new ScriptedHandler(() => Http(HttpStatusCode.OK, Sse(Start, Delta("Aye. I saw him go by the chi"))));
            bool threwShort = false;
            try { await Client(hshort).StreamAsync(OneTurn(), null); }
            catch (LlmStreamBrokenException) { threwShort = true; }
            Check(threwShort, "a stream that stops short after text fails, never passes as the whole reply");
            var hnothing = new ScriptedHandler(() => Http(HttpStatusCode.OK, Sse(Start)), () => Http(HttpStatusCode.OK, OkBody));
            var hdrop = new ScriptedHandler(() => new HttpResponseMessage(HttpStatusCode.OK) { Content = new StreamContent(new DroppingStream(Sse(Start, Delta("Aye, I")))) });
            bool brokeD = false;
            try { await Client(hdrop).StreamAsync(OneTurn(), null); } catch (LlmStreamBrokenException) { brokeD = true; }
            Check(brokeD, "a connection dropped mid-reply is a broken stream too, for the caller to ask again");
            bool brokeN = false;
            try { await Client(hnothing).StreamAsync(OneTurn(), null); } catch (LlmStreamBrokenException) { brokeN = true; }
            Check(brokeN && hnothing.Calls == 1, "so is one that stops before any text");
        }

        static void TestResponseParsing()
        {
            Console.WriteLine("AnthropicClient.ParseResponse:");
            var json = "{\"id\":\"msg_x\",\"type\":\"message\",\"role\":\"assistant\"," +
                       "\"model\":\"claude-haiku-4-5\"," +
                       "\"content\":[{\"type\":\"text\",\"text\":\"Hello \"},{\"type\":\"text\",\"text\":\"there.\"}]," +
                       "\"stop_reason\":\"end_turn\",\"usage\":{\"input_tokens\":12,\"output_tokens\":5}}";
            var r = AnthropicClient.ParseResponse(json);
            Check(r.Text == "Hello there.", "text blocks concatenated");
            Check(r.StopReason == "end_turn", "stop_reason parsed");
            Check(r.InputTokens == 12 && r.OutputTokens == 5, "usage parsed");
            Check(r.Model == "claude-haiku-4-5", "model parsed");
        }

        // ---------------------------------------------------------------
        // The intent router (roadmap M6.5)
        // ---------------------------------------------------------------

        /// A representative moment: talking to a debtor who is also carrying a
        /// rumor about you, while you hold something on them.
        static IntentContext SampleContext()
        {
            var ctx = new IntentContext { SpeakingTo = "Rocco", Scene = "the bar, after close" };
            ctx.KnownPeople.AddRange(new[] { "Rocco", "Lena", "Sera Kest" });
            ctx.Verbs.Add(new VerbSpec("pay_off", "pay them to keep quiet", "costs £120 dirty")
                .WithLexical("pay them off", "pay him off", "buy their silence"));
            ctx.Verbs.Add(new VerbSpec("lean_on", "threaten them into silence")
                .WithLexical("lean on", "threaten"));
            ctx.Verbs.Add(new VerbSpec("collect_debt", "collect what they owe", "£80 outstanding")
                .WithLexical("collect", "collect the debt"));
            ctx.Verbs.Add(new VerbSpec("set_cut", "change what a crew member keeps")
                .WithArg("policy", "fair", "generous", "skim")
                .WithLexical("set their cut", "change their cut"));
            return ctx;
        }

        static void TestIntentLexical()
        {
            Console.WriteLine("IntentRouter — the free path:");
            var ctx = SampleContext();

            var a = IntentRouter.RouteLexical("Fine. I'll pay them off and be done with it.", ctx);
            Check(a.Kind == IntentKind.Mechanical && a.VerbId == "pay_off", "an unambiguous phrasing routes for free");
            Check(a.Source == "lexical", "the free path is labelled as such");

            var b = IntentRouter.RouteLexical("How's your sister doing?", ctx);
            Check(b.Kind == IntentKind.Narrative, "ordinary talk stays talk");

            // Two different verbs, equally specific: refuse rather than guess.
            var c = IntentRouter.RouteLexical("Should I lean on him or collect?", ctx);
            Check(c.Kind == IntentKind.Narrative, "an ambiguous line is not guessed at");

            // Word boundaries: "collect" must not fire inside "collectors".
            var d = IntentRouter.RouteLexical("The collectors came by yesterday.", ctx);
            Check(d.Kind == IntentKind.Narrative, "a verb keyword inside a longer word does not fire");

            var e = IntentRouter.RouteLexical("Set their cut to generous from now on.", ctx);
            Check(e.Kind == IntentKind.Mechanical && e.Arg("policy") == "generous",
                "the free path binds an argument it can see exactly once");

            var f = IntentRouter.RouteLexical("Set their cut — fair, or skim?", ctx);
            Check(f.Kind == IntentKind.Narrative, "two candidate argument values means no free routing");

            var g = IntentRouter.RouteLexical("Change their cut, would you.", ctx);
            Check(g.Kind == IntentKind.Narrative, "a verb whose argument cannot be filled is not routed for free");

            var empty = IntentRouter.RouteLexical("pay them off", new IntentContext());
            Check(empty.Kind == IntentKind.Narrative, "with no verbs offered, nothing routes");
        }

        static void TestIntentValidation()
        {
            Console.WriteLine("IntentRouter — the closed-set boundary:");
            var ctx = SampleContext();

            var ok = IntentRouter.Validate("{\"kind\":\"verb\",\"verb\":\"pay_off\",\"why\":\"paying for quiet\"}", ctx);
            Check(ok.Kind == IntentKind.Mechanical && ok.VerbId == "pay_off", "a listed verb validates");
            Check(ok.Because == "paying for quiet", "the router's reason survives");

            // The security boundary. A verb the game did not offer cannot exist,
            // no matter how confidently it is named.
            var invented = IntentRouter.Validate("{\"kind\":\"verb\",\"verb\":\"kill_them\"}", ctx);
            Check(invented.Kind == IntentKind.Narrative, "an invented verb is rejected outright");

            var cased = IntentRouter.Validate("{\"kind\":\"verb\",\"verb\":\"PAY_OFF\"}", ctx);
            Check(cased.Kind == IntentKind.Mechanical && cased.VerbId == "pay_off",
                "verb casing is tolerated but canonicalised to the spec's");

            var badArg = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"set_cut\",\"args\":{\"policy\":\"everything\"}}", ctx);
            Check(badArg.Kind == IntentKind.Narrative, "an argument outside its closed set kills the routing");

            var missingArg = IntentRouter.Validate("{\"kind\":\"verb\",\"verb\":\"set_cut\"}", ctx);
            Check(missingArg.Kind == IntentKind.Narrative, "a verb missing a required argument is not half-executed");

            // A NUMBER IS A VALUE, 23 September: the paid router sent the right
            // amount as a JSON number and was refused as if it had sent none.
            // It is matched against the same closed set, so 999 is still out.
            var money = new IntentContext { SpeakingTo = "Lena", Scene = "the pub, after close" };
            money.Verbs.Add(new VerbSpec("pay_off", "pay them to keep quiet").WithArg("amount", "120", "240"));
            var numeric = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"pay_off\",\"args\":{\"amount\":240}}", money);
            Check(numeric.Kind == IntentKind.Mechanical && numeric.Arg("amount") == "240",
                "an amount sent as a number is read, and canonicalised to the set's own text");
            var numericOut = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"pay_off\",\"args\":{\"amount\":999}}", money);
            var numericHalf = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"pay_off\",\"args\":{\"amount\":240.5}}", money);
            var numericList = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"pay_off\",\"args\":{\"amount\":[240]}}", money);
            Check(numericOut.Kind == IntentKind.Narrative && numericHalf.Kind == IntentKind.Narrative
                  && numericList.Kind == IntentKind.Narrative,
                "and a number outside the set, a fraction, or a list is still refused");

            var extraArg = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"set_cut\",\"args\":{\"policy\":\"fair\",\"amount\":\"9999\"}}", ctx);
            Check(extraArg.Kind == IntentKind.Narrative, "an undeclared argument is treated as confusion, not extra credit");

            var goodArg = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"set_cut\",\"args\":{\"Policy\":\"SKIM\"}}", ctx);
            Check(goodArg.Kind == IntentKind.Mechanical && goodArg.Arg("policy") == "skim",
                "argument key casing is tolerated and the value is canonicalised");

            // Novel path vocabulary.
            var novel = IntentRouter.Validate(
                "{\"kind\":\"novel\",\"check\":\"dirty_cash\",\"amount\":60,\"effect\":\"standing_up\"," +
                "\"magnitude\":0.05,\"target\":\"Lena\",\"why\":\"buying a round\"}", ctx);
            Check(novel.Kind == IntentKind.Novel && novel.Check == Checks.DirtyCash, "a novel action names a known check");
            Check(novel.Target == "Lena", "a novel target the game knows is kept");

            var badCheck = IntentRouter.Validate(
                "{\"kind\":\"novel\",\"check\":\"summon_demon\",\"effect\":\"standing_up\"}", ctx);
            Check(badCheck.Kind == IntentKind.Narrative, "a check outside the vocabulary is rejected");

            var badEffect = IntentRouter.Validate(
                "{\"kind\":\"novel\",\"check\":\"none\",\"effect\":\"give_player_money\"}", ctx);
            Check(badEffect.Kind == IntentKind.Narrative, "an effect outside the vocabulary is rejected");

            var huge = IntentRouter.Validate(
                "{\"kind\":\"novel\",\"check\":\"none\",\"effect\":\"standing_up\",\"magnitude\":99}", ctx);
            Check(huge.Kind == IntentKind.Novel && huge.Magnitude <= Effects.MaxMagnitude,
                "magnitude is clamped, not trusted");

            var negative = IntentRouter.Validate(
                "{\"kind\":\"novel\",\"check\":\"cash\",\"amount\":-500,\"effect\":\"nothing\"}", ctx);
            Check(negative.CheckAmount == 0, "a negative amount cannot become a refund");

            var strangerTarget = IntentRouter.Validate(
                "{\"kind\":\"novel\",\"check\":\"none\",\"effect\":\"rumor\",\"target\":\"The Mayor\"}", ctx);
            Check(strangerTarget.Kind == IntentKind.Novel && strangerTarget.Target == "",
                "a target the game has never heard of becomes no target");

            // Real model output habits.
            var fenced = IntentRouter.Validate(
                "Sure! ```json\n{\"kind\":\"verb\",\"verb\":\"lean_on\"}\n```", ctx);
            Check(fenced.Kind == IntentKind.Mechanical && fenced.VerbId == "lean_on", "fenced JSON with prose around it is recovered");

            var braceInString = IntentRouter.Validate(
                "{\"kind\":\"verb\",\"verb\":\"lean_on\",\"why\":\"he said \\\"} now\\\"\"}", ctx);
            Check(braceInString.Kind == IntentKind.Mechanical, "a brace inside a string does not truncate the object");

            Check(IntentRouter.Validate("not json at all", ctx).Kind == IntentKind.Narrative, "unparseable output is speech");
            Check(IntentRouter.Validate("", ctx).Kind == IntentKind.Narrative, "empty output is speech");
            Check(IntentRouter.Validate("{\"kind\":\"speech\"}", ctx).Kind == IntentKind.Narrative, "speech is speech");
        }

        /// The same idea as "every input to the ending is read", applied to the
        /// two closed vocabularies the novel-action path runs on.
        ///
        /// A Check with no case in the switch falls to `default` and fails
        /// forever; an Effect with no case in the bridge validates, adjudicates,
        /// and then does nothing at all. Both are silent, both look like working
        /// code, and both are the shape of the bug found in `Eligible()` today.
        /// "Does anything actually read this", applied to the two places money
        /// is modified on its way to the player. Each of these is a multiplier
        /// sitting in a chain, and a multiplier that never fires is the same
        /// bug as a strain nobody consults — the design says the street pushes
        /// back, and the only proof is that the number moves.
        /// The same question again, asked of authored TEXT rather than of logic.
        ///
        /// Every kind of key a door can want has a line for being let past on
        /// it, and a line for nearly making it. A kind with no case falls to a
        /// flat default — nothing crashes, nothing is logged, and the player
        /// simply gets a worse game at that door than at every other one.
        ///
        /// This found two: the hour keys, which are precisely the doors where
        /// the clock is the whole content of being let in, were being told
        /// "the man on the door lets you past".
        /// The last closed list: the three ways to run an operation.
        ///
        /// An Approach that changes neither the risk, nor who sees you, nor the
        /// words is a choice in a menu and nothing else — and this is the system
        /// the agency model called the biggest hole in the game before it was
        /// built, so a decorative approach would be the worst possible outcome.
        static void TestEveryApproachIsADifferentPlan()
        {
            Console.WriteLine("Operations — the three approaches are genuinely three plans:");
            var target = new OperationTarget
            {
                Id = "store", Name = "the bonded store", PlaceId = "bonded_store",
                Difficulty = 0.5, Payout = 200, Exposure = 0.5,
            };
            OperationState Steady() => new OperationState { Heat = 0.2, Nerve = 0.5, Coated = true };

            var risk = new Dictionary<Approach, double>();
            var seen = new Dictionary<Approach, double>();
            var worry = new Dictionary<Approach, string>();
            foreach (Approach a in Enum.GetValues(typeof(Approach)))
            {
                var plan = new OperationPlan(target.Id) { Approach = a, Hour = 2, Tools = true };
                var read = Operations.Read(plan, target, Steady());
                risk[a] = read.Risk;
                seen[a] = read.Visibility;
                worry[a] = read.Worry;
                Check(read.Line.Length > 0, $"{a} has a plan somebody would say out loud", a.ToString());
                Check(!read.Line.Any(char.IsDigit) && !read.Worry.Any(char.IsDigit),
                    $"{a} says it without a single number", read.Line);
            }

            Check(new HashSet<double>(risk.Values).Count == risk.Count,
                "each approach carries its own risk", string.Join(" ", risk.Values.Select(v => v.ToString("0.00"))));
            Check(new HashSet<double>(seen.Values).Count == seen.Count,
                "and its own chance of being seen", string.Join(" ", seen.Values.Select(v => v.ToString("0.00"))));
            Check(risk[Approach.Forced] < risk[Approach.Quiet],
                "forcing it is the reliable one", $"{risk[Approach.Forced]:0.00} vs {risk[Approach.Quiet]:0.00}");
            Check(seen[Approach.Forced] > seen[Approach.Quiet],
                "and the loud one — which is the whole trade");

            // The approaches must also disagree about DIFFERENT worlds, or the
            // ordering above is a constant rather than a choice.
            var hot = new OperationState { Heat = 0.9, Nerve = 0.5, Coated = true };
            var jumpy = new OperationState { Heat = 0.2, Nerve = 0.1, Coated = true };
            double socialWhenKnown = Operations.Read(
                new OperationPlan(target.Id) { Approach = Approach.Social, Hour = 2 }, target, hot).Risk;
            double socialWhenNot = Operations.Read(
                new OperationPlan(target.Id) { Approach = Approach.Social, Hour = 2 }, target, Steady()).Risk;
            Check(socialWhenKnown > socialWhenNot,
                "talking your way in gets harder once the street knows your name");

            double quietWhenJumpy = Operations.Read(
                new OperationPlan(target.Id) { Approach = Approach.Quiet, Hour = 2 }, target, jumpy).Risk;
            Check(quietWhenJumpy > risk[Approach.Quiet],
                "and the quiet one leans on a steady hand you may not have");
        }

        static void TestEveryKeyKindHasItsOwnWords()
        {
            Console.WriteLine("Doors — every kind of key has its own words:");
            var generic = new HashSet<string>();
            var lines = new Dictionary<KeyKind, string>();

            // One gate per kind, with a state built to satisfy exactly that key
            // — After and Before disagree about the hour, so they cannot share.
            AccessState StateFor(KeyKind kind)
            {
                var st = new AccessState { Dress = "plain", Hour = 12, Money = 0, Crew = 0 };
                switch (kind)
                {
                    case KeyKind.Standing: st.Standing["dockside"] = 0.5; break;
                    case KeyKind.Quiet: st.Notoriety = 0.02; break;
                    case KeyKind.Notorious: st.Notoriety = 0.9; break;
                    case KeyKind.Introduction: st.Introductions.Add("dockside"); break;
                    case KeyKind.Payment: st.Money = 500; break;
                    case KeyKind.After: st.Hour = 22; break;
                    case KeyKind.Before: st.Hour = 6; break;
                    case KeyKind.Hook: st.HoldsHookOnDoor = true; break;
                    case KeyKind.Crew: st.Crew = 20; break;
                }
                return st;
            }

            foreach (KeyKind kind in Enum.GetValues(typeof(KeyKind)))
            {
                var gate = new Gate("room", "the room", "Hal");
                gate.WithKey(new AccessKey(kind, 10, who: "dockside", dress: "plain"));
                var r = Doors.Try(gate, StateFor(kind));
                Check(r.Allowed, $"{kind} can actually open a door", kind.ToString());
                if (!r.Allowed) continue;
                lines[kind] = r.Line;
                Check(!string.IsNullOrEmpty(r.Line), $"{kind} has something to say", kind.ToString());
                if (r.Line.EndsWith("lets you past.")) generic.Add(kind.ToString());
            }

            Check(generic.Count == 0,
                "and none of them falls back on the flat default",
                generic.Count == 0 ? "all specific" : string.Join(", ", generic));

            // Distinct, too — two keys sharing a line is the same failure
            // wearing a copy-paste.
            var distinct = new HashSet<string>(lines.Values);
            Check(distinct.Count == lines.Count,
                "and no two keys share a line", $"{distinct.Count} of {lines.Count} distinct");
        }

        static void TestEveryModifierBites()
        {
            Console.WriteLine("Money — every modifier on the way in actually moves it:");

            // ---- the street's factor ----
            var econ = Ledger.Game.EconomySetup.Build();
            double neutral = econ.TakingsFactor;
            Check(Math.Abs(neutral - 1.0) < 0.12,
                "an unsqueezed street is neutral, so a campaign that takes nothing is unchanged",
                neutral.ToString("0.00"));

            var poor = Ledger.Game.EconomySetup.Build();
            poor.Restore(MiniJson.AsObject(MiniJson.Deserialize(
                "{\"prosperity\":0.05,\"priceLevel\":1.0}")));
            Check(poor.TakingsFactor < neutral, "a starved street pays the bar less",
                poor.TakingsFactor.ToString("0.00"));

            var dear = Ledger.Game.EconomySetup.Build();
            dear.Restore(MiniJson.AsObject(MiniJson.Deserialize(
                "{\"prosperity\":0.55,\"priceLevel\":1.6}")));
            Check(dear.TakingsFactor < neutral, "and dear prices take a bite of their own",
                dear.TakingsFactor.ToString("0.00"));

            var wild = Ledger.Game.EconomySetup.Build();
            wild.Restore(MiniJson.AsObject(MiniJson.Deserialize(
                "{\"prosperity\":9.0,\"priceLevel\":0.0}")));
            Check(wild.TakingsFactor <= econ.MaxTakingsFactor + 1e-9
                  && wild.TakingsFactor >= econ.MinTakingsFactor - 1e-9,
                "and neither runs away with it", wild.TakingsFactor.ToString("0.00"));

            // A supplier who has stopped delivering costs THAT front and not
            // the others — the whole reason the factor is per-business.
            var withSupplier = Ledger.Game.EconomySetup.Build();
            var sup = withSupplier.Suppliers.FirstOrDefault();
            if (sup != null)
            {
                string biz = sup.ServesBusinessId;
                double before = withSupplier.FactorFor(biz);
                sup.Refusing = true;
                double after = withSupplier.FactorFor(biz);
                Check(after < before, "a front nobody will deliver to earns less",
                    $"{before:0.00} -> {after:0.00}");
                Check(Math.Abs(withSupplier.FactorFor("nothing_of_theirs") - before) < 1e-9,
                    "and only that one — which is why the factor is per-business");
            }

            // ---- the empire's take ----
            //
            // Each of these is a term in one expression, and the risk is not
            // that the arithmetic is wrong but that the condition in front of
            // it never becomes true in play. Set each condition by hand and
            // require the day's take to move.
            int TakeFor(Action<EmpireBook> arrange)
            {
                var mill = new GossipMill(new SocialGraph());
                foreach (var id in new[] { "Sam" })
                    mill.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(),
                        new SuspicionTracker()) { Loyalty = 0.7, Nerve = 0.7 });
                var e = new EmpireBook();
                e.Rackets.Add(new Racket
                {
                    Id = "collection", Name = "collection round",
                    IncomePerDay = 100, BaseRisk = 0.0, Established = true, RunnerId = "Sam",
                });
                e.Crew.Add(new CrewMember
                {
                    Id = "Sam", Name = "Sam", Route = "need", Competence = 0.7,
                    Assignment = "collection", Cut = "fair",
                });
                arrange?.Invoke(e);
                var wallet = new Wallet(0);
                int take = 0;
                foreach (var ev in e.DailyTick(new GameTime(9, 9, 0), wallet, mill))
                    if (ev.Kind == "income") take += ev.Amount;
                return take;
            }

            int plain = TakeFor(null);
            Check(plain > 0, "a round pays something to begin with", plain.ToString());

            Check(TakeFor(e => e.ArmOf("newcrew").Stage = 3) < plain,
                "the New crew taxing your rounds actually costs you",
                TakeFor(e => e.ArmOf("newcrew").Stage = 3).ToString());
            Check(TakeFor(e => e.TributeShare = 0.12) < plain,
                "a tribute treaty actually costs you", TakeFor(e => e.TributeShare = 0.12).ToString());
            Check(TakeFor(e => e.SharedRacketId = "collection") < plain,
                "and a shared round is genuinely shared",
                TakeFor(e => e.SharedRacketId = "collection").ToString());

            // The cut, which is the §6.5 rule: generosity costs money and buys
            // loyalty; skimming does the reverse. Both must show in the till.
            Check(TakeFor(e => e.Crew[0].Cut = "generous") < plain,
                "paying a generous cut costs the till");
            Check(TakeFor(e => e.Crew[0].Cut = "skim") > plain,
                "and skimming shows up in it too, which is what makes it tempting");

            // AND THE ONE THAT USED NOT TO BITE. Decision 9, answered
            // 2026-07-27: couple it.
            //
            // Empire.DailyTick read `r.IncomePerDay` flat, so a district you had
            // starved paid the same round as a rich one — the last infinite
            // pocket in the game, sitting on the player's main income. The purse
            // spec had skipped it citing "already coupled through prosperity",
            // which was true in the direction that DRAINS the street and absent
            // in the direction that limits the take.
            //
            // Now the round is scaled by the same factor the bar's till uses, so
            // the squeeze is genuinely two turns of the same screw.
            int TakeAtStreet(double factor)
            {
                var mill = new GossipMill(new SocialGraph());
                mill.Add(new Gossiper("Sam", "Sam", new MemoryStore("sam"), new KnowledgeBase(),
                    new SuspicionTracker()) { Loyalty = 0.7, Nerve = 0.7 });
                var e = new EmpireBook();
                e.Rackets.Add(new Racket
                {
                    Id = "collection", Name = "collection round",
                    IncomePerDay = 100, BaseRisk = 0.0, Established = true, RunnerId = "Sam",
                });
                e.Crew.Add(new CrewMember
                {
                    Id = "Sam", Name = "Sam", Route = "need", Competence = 0.7,
                    Assignment = "collection", Cut = "fair",
                });
                var w = new Wallet(0);
                int take = 0;
                foreach (var ev in e.DailyTick(new GameTime(9, 9, 0), w, mill, factor))
                    if (ev.Kind == "income") take += ev.Amount;
                return take;
            }
            Check(TakeAtStreet(1.0) == plain, "an ordinary street pays an ordinary round");
            Check(TakeAtStreet(0.4) < plain,
                "and a street you have starved cannot pay a full one — decision 9",
                $"{plain} -> {TakeAtStreet(0.4)}");
            Check(TakeAtStreet(1.3) > plain, "while a prosperous one pays more");

            // A poor street says so, in somebody's words rather than in a figure.
            var poorMill = new GossipMill(new SocialGraph());
            poorMill.Add(new Gossiper("Sam", "Sam", new MemoryStore("sam"), new KnowledgeBase(),
                new SuspicionTracker()) { Loyalty = 0.7, Nerve = 0.7 });
            var poorEmpire = new EmpireBook();
            poorEmpire.Rackets.Add(new Racket
            {
                Id = "collection", Name = "collection round",
                IncomePerDay = 100, BaseRisk = 0.0, Established = true, RunnerId = "Sam",
            });
            poorEmpire.Crew.Add(new CrewMember
            {
                Id = "Sam", Name = "Sam", Route = "need", Competence = 0.7,
                Assignment = "collection", Cut = "fair",
            });
            bool saidSo = false;
            foreach (var ev in poorEmpire.DailyTick(new GameTime(9, 9, 0), new Wallet(0), poorMill, 0.4))
                if (ev.Kind == "street") saidSo = true;
            Check(saidSo, "and somebody tells you why, rather than the number just being smaller");
        }

        static void TestClosedVocabulariesAreHandled()
        {
            Console.WriteLine("Novel actions — every check and effect is actually handled:");

            // A state generous enough that any check CAN pass, so a check that
            // fails here fails because nothing handles it.
            var rich = new AdjudicationInput
            {
                Clean = 10000, Dirty = 10000, Crew = 9, Hour = 23,
                Standing = 1.0, Heat = 0.0, HoldsHook = true,
            };
            // Every check has a case that can pass. "none" is the one that
            // carries no requirement, so it can only pass an effect that touches
            // nothing; everything else passes a real change on a generous state.
            // 8 checks examined, 0 skipped.
            foreach (var check in Checks.All)
            {
                var intent = new Intent
                {
                    Kind = IntentKind.Novel, Check = check, CheckAmount = 1,
                    Effect = check == Checks.None ? Effects.Nothing : Effects.StandingUp,
                    Magnitude = 0.05,
                };
                Check(Adjudicator.Resolve(intent, rich).Passed,
                    $"check '{check}' has a case that can pass", check);
            }

            // And every check must be able to FAIL a state-altering effect, or
            // it is a requirement in name only.
            //
            // THE SKIP THAT CERTIFIED THE HOLE. This loop used to read
            // `if (check == Checks.None) continue;   // costs nothing but nerve,
            // by design`, so the suite's own proof that requirements can refuse
            // was taken over a set trimmed to the members that pass, and the one
            // member that could refuse NOTHING was the one it did not examine.
            // An outside audit found check:none reaching live state on the
            // model's own say-so six weeks later, 26 July to 6 September, both
            // dates read from git log (queue 113). The denominator is
            // now the whole vocabulary: 8 checks examined, 0 skipped.
            var broke = new AdjudicationInput
            {
                Clean = 0, Dirty = 0, Crew = 0, Hour = 0,
                Standing = -1.0, Heat = 1.0, HoldsHook = false,
            };
            int refused = 0;
            foreach (var check in Checks.All)
            {
                var intent = new Intent
                {
                    Kind = IntentKind.Novel, Check = check, CheckAmount = 50,
                    Effect = Effects.StandingUp, Magnitude = 0.05,
                };
                var r = Adjudicator.Resolve(intent, broke);
                if (!r.Passed && r.Reason.Length > 0) refused++;
                Check(!r.Passed && r.Reason.Length > 0,
                    $"check '{check}' can refuse, and says why", check + ": " + r.Reason);
            }
            Check(refused == Checks.All.Length,
                "and that is the WHOLE vocabulary, not the part that passes",
                $"{refused}/{Checks.All.Length} refused a state change they could not carry");

            // THE CANARY. Effects are applied in the game layer, which CoreTests
            // cannot reach — so this pins the vocabulary instead. If somebody
            // adds an effect, this fails and points at the two switches in
            // IntentBridge (the one that APPLIES it and the one that NARRATES
            // it) that must gain a case, plus this list. That is a deliberately
            // annoying test: the alternative is an effect that quietly does
            // nothing, which is how a feature ships broken and stays that way.
            var expected = new[]
            {
                Effects.Nothing, Effects.StandingUp, Effects.StandingDown,
                Effects.SuspicionUp, Effects.SuspicionDown,
                Effects.AttentionUp, Effects.AttentionDown, Effects.Rumor,
            };
            Check(Effects.All.Length == expected.Length,
                "the effect vocabulary is the size IntentBridge handles",
                $"{Effects.All.Length} effects — if you added one, IntentBridge.Apply and " +
                "IntentBridge's narration switch both need a case");
            foreach (var e in expected)
                Check(Effects.Known(e), $"effect '{e}' is still in the vocabulary", e);

            // THE SECOND CANARY, same shape, one system over. The Director's
            // pressure kinds are the other closed vocabulary the model writes
            // into, and DirectorHost.Fire switches on them. A kind with no case
            // there is scheduled, validated, comes due, and silently does
            // nothing — a night the world was supposed to move and did not.
            //
            // The sim already asserts the reverse direction (nothing UNKNOWN is
            // ever scheduled). This is the direction that was missing.
            var firedKinds = new[]
            {
                Pressures.Rumor, Pressures.Meeting, Pressures.Demand,
                Pressures.Schedule, Pressures.Grievance,
            };
            Check(Pressures.All.Length == firedKinds.Length + 1,
                "the pressure vocabulary is the size DirectorHost handles",
                $"{Pressures.All.Length} kinds — if you added one, DirectorHost.Fire needs a case " +
                "and this list needs the name; 'nothing' is the +1 and correctly has no case");
            foreach (var k in firedKinds)
                Check(Pressures.Known(k), $"pressure '{k}' is still in the vocabulary", k);
            Check(Pressures.Known(Pressures.Nothing),
                "and 'nothing' stays in it, because the correct answer most nights is no pressure");

            // Magnitude is clamped whatever the model says, including when it
            // says something that is not a number.
            //
            // On a check that PASSES, deliberately. This loop used to run on
            // `Checks.None`, which now refuses a state-altering effect, and a
            // refusal reports Magnitude 0 and would have satisfied the bound
            // without the clamp ever running. A clamp test has to reach the
            // clamp: cash for £50 is a requirement `rich` meets.
            foreach (var mag in new[] { 99.0, -99.0, double.NaN, double.PositiveInfinity })
            {
                var intent = new Intent
                {
                    Kind = IntentKind.Novel, Check = Checks.Cash, CheckAmount = 50,
                    Effect = Effects.StandingUp, Magnitude = mag,
                };
                var r = Adjudicator.Resolve(intent, rich);
                Check(r.Passed && r.Magnitude >= 0 && r.Magnitude <= Effects.MaxMagnitude,
                    $"a magnitude of {mag} is clamped to something real", r.Magnitude.ToString("0.00"));
            }
        }

        static void TestAdjudicator()
        {
            Console.WriteLine("Adjudicator — novel actions cost something real:");
            var state = new AdjudicationInput
            {
                Clean = 200, Dirty = 90, Crew = 1, Hour = 21, Standing = 0.4, Heat = 0.3, HoldsHook = false,
            };

            var afford = Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.DirtyCash, CheckAmount = 60,
                Effect = Effects.StandingUp, Magnitude = 0.05,
            }, state);
            Check(afford.Passed && afford.CashSpent == 60 && afford.SpentDirty, "an affordable dirty cost is charged");

            var cantAfford = Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Cash, CheckAmount = 400, Effect = Effects.StandingUp,
            }, state);
            Check(!cantAfford.Passed && cantAfford.Reason.Contains("£200"), "an unaffordable cost fails and says why");

            var capped = Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Cash, CheckAmount = 100000, Effect = Effects.Nothing,
            }, new AdjudicationInput { Clean = 100000 });
            Check(capped.Passed && capped.CashSpent == Adjudicator.MaxNovelCost,
                "a novel action can never cost more than the cap, however it is phrased");

            var noHook = Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Hook, Effect = Effects.SuspicionDown,
            }, state);
            Check(!noHook.Passed, "leverage you do not hold fails the check");
            state.HoldsHook = true;
            Check(Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Hook, Effect = Effects.SuspicionDown,
            }, state).Passed, "leverage you do hold passes it");

            Check(!Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Crew, CheckAmount = 4, Effect = Effects.Nothing,
            }, state).Passed, "a crew you do not have fails");

            Check(!Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Standing, CheckAmount = 70, Effect = Effects.Nothing,
            }, state).Passed, "standing you have not earned fails");

            Check(Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Heat, CheckAmount = 50, Effect = Effects.Nothing,
            }, state).Passed, "a heat check passes while you are under it");
            state.Heat = 0.8;
            Check(!Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Heat, CheckAmount = 50, Effect = Effects.Nothing,
            }, state).Passed, "the same check fails once the street is watching");

            state.Hour = 9;
            Check(!Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Hour, CheckAmount = 22, Effect = Effects.Nothing,
            }, state).Passed, "an hour that has not arrived fails");

            // The router clamps magnitude on the way in; this clamps it again on
            // the way out, from a hand-built intent the router never saw. On a
            // check that passes: `Checks.None` used to stand here, and it now
            // refuses a state-altering effect, which would have reported
            // Magnitude 0 and proved nothing. `state.HoldsHook` is true by this
            // point in the battery.
            var wild = Adjudicator.Resolve(new Intent
            {
                Kind = IntentKind.Novel, Check = Checks.Hook, Effect = Effects.StandingUp, Magnitude = 50,
            }, state);
            Check(wild.Passed && wild.Magnitude <= Effects.MaxMagnitude, "the adjudicator clamps magnitude independently of the router");

            var notNovel = Adjudicator.Resolve(new Intent { Kind = IntentKind.Mechanical, VerbId = "pay_off" }, state);
            Check(!notNovel.Passed, "a mechanical intent is not adjudicated as a novel one");

            // No effect in the vocabulary pays the player. This is a project law,
            // not an accident, so it is asserted rather than assumed.
            Check(!Effects.All.Any(e => e.Contains("cash") || e.Contains("money") || e.Contains("pay")),
                "no novel effect can mint money");
        }

        /// THE MODEL DOES NOT ADJUDICATE (queue 113; outside audit 2026-09-06,
        /// verified by Jafar and re-verified in the code before this was written).
        ///
        /// IntentRouter.Validate takes `check`, `amount` and `effect` straight
        /// from the model's JSON, so the model proposes the action AND names the
        /// requirement that governs it. If it may name one that cannot refuse, it
        /// is the referee. `check:none` was exactly that: Checks.Known("none") is
        /// true, so it cleared the vocabulary gate, and the adjudicator's case for
        /// it broke out of the switch into Pass, after which the game layer wrote
        /// the effect into live state.
        ///
        /// The property pinned here is NOT "none is refused". It is "an effect
        /// that alters state travels only on a requirement that could have
        /// refused it", which is why the vacuous-amount forms are in this battery
        /// as well: they are the same authority wearing a word that looks like a
        /// constraint, and fixing only the one the audit named would have left
        /// `cash` for £0 doing the identical job.
        ///
        /// Watched red before it was watched green: with the old Adjudicator in
        /// place, the rejecting case below reports PASSED and this battery is the
        /// first thing in the suite to fail.
        static void TestModelCannotChooseAnUnrefusableCheck()
        {
            Console.WriteLine("Novel actions. The model may narrow a requirement, never remove it:");

            var ctx = new IntentContext();
            // Generous enough that every requirement in the vocabulary is met, so
            // anything refused below is refused for being unrefusable, not for
            // being unaffordable.
            var rich = new AdjudicationInput
            {
                Clean = 10000, Dirty = 10000, Crew = 9, Hour = 23,
                Standing = 1.0, Heat = 0.0, HoldsHook = true,
            };

            // Exactly the shape the router parses, so this is the model's own
            // path end to end rather than a hand-built Intent standing in for it.
            string Novel(string check, int amount, string effect) =>
                "{\"kind\":\"novel\",\"check\":\"" + check + "\",\"amount\":" + amount
                + ",\"effect\":\"" + effect + "\",\"magnitude\":0.15,"
                + "\"why\":\"buying the room a round\"}";

            // ACCEPTING CASE FIRST. A legitimate novel action, on a requirement
            // that could have refused it, still lands and still costs.
            var legit = IntentRouter.Validate(Novel(Checks.DirtyCash, 40, Effects.StandingUp), ctx);
            var landed = Adjudicator.Resolve(legit, rich);
            Check(landed.Passed && landed.CashSpent == 40 && landed.SpentDirty
                  && landed.Effect == Effects.StandingUp && landed.Magnitude > 0,
                "a novel action on a requirement that could refuse it still lands, and still costs",
                $"{landed.Effect}/{landed.Magnitude:0.00}/£{landed.CashSpent}");

            // And the one thing "none" is for survives: an attempt that changes
            // nothing needs nothing behind it.
            var narration = IntentRouter.Validate(Novel(Checks.None, 0, Effects.Nothing), ctx);
            var told = Adjudicator.Resolve(narration, rich);
            Check(told.Passed && told.Effect == Effects.Nothing && told.CashSpent == 0,
                "and 'none' still passes the attempt that moves nothing, which is what it is for",
                told.Effect);

            // THE REJECTING CASE.
            var crafted = IntentRouter.Validate(Novel(Checks.None, 0, Effects.StandingUp), ctx);
            Check(crafted.Kind == IntentKind.Novel && crafted.Check == Checks.None
                  && crafted.Effect == Effects.StandingUp,
                "a crafted check:none with a state-altering effect still PARSES, so what refuses it "
                + "is the adjudicator and not the parser", crafted.ToString());

            var verdict = Adjudicator.Resolve(crafted, rich);
            Check(!verdict.Passed && verdict.Reason.Length > 0,
                "check:none cannot carry a change to state, however rich the player is",
                verdict.Passed ? "PASSED, and the model is adjudicating again" : verdict.Reason);
            Check(verdict.Effect == Effects.Nothing && verdict.Magnitude == 0 && verdict.CashSpent == 0,
                "and the refusal hands the game layer no effect, no magnitude and no spend",
                $"{verdict.Effect}/{verdict.Magnitude:0.00}/£{verdict.CashSpent}");

            // THE TWINS. Every branch that reads an amount has a setting at which
            // nobody can fail it. Read out of the switch in Adjudicator.Evaluate
            // rather than guessed at: cash and dirty cash at £0, crew of nobody,
            // an hour that has already happened, and a heat ceiling at the top of
            // a 0..1 scale.
            var vacuous = new (string check, int amount, string why)[]
            {
                (Checks.None, 0, "no requirement at all"),
                (Checks.Cash, 0, "£0 clean, which everybody has"),
                (Checks.DirtyCash, 0, "£0 dirty, which everybody has"),
                (Checks.Crew, 0, "nobody, which is what having no crew is"),
                (Checks.Hour, 0, "after midnight, which it always is"),
                (Checks.Heat, 100, "under 100 per cent watched, which is the top of the scale"),
            };
            int stopped = 0;
            foreach (var v in vacuous)
            {
                var r = Adjudicator.Resolve(
                    IntentRouter.Validate(Novel(v.check, v.amount, Effects.SuspicionDown), ctx), rich);
                if (!r.Passed) stopped++;
                Check(!r.Passed,
                    $"'{v.check}' at {v.amount} is a formality ({v.why}) and carries no state change",
                    r.Passed ? "PASSED" : r.Reason);
            }
            Check(stopped == vacuous.Length,
                "every unrefusable form of a requirement is stopped",
                $"{stopped}/{vacuous.Length} stopped. The two checks not in this list are "
                + "'standing', which at 0 still refuses anybody standing below neutral, and "
                + "'hook', which takes no amount and refuses anybody holding nothing");

            // And no other branch moved: the same requirements, named with an
            // amount that bites, pass a state change on a state that meets them.
            int carried = 0;
            var binding = new (string check, int amount)[]
            {
                (Checks.Cash, 50), (Checks.DirtyCash, 50), (Checks.Crew, 1),
                (Checks.Hour, 1), (Checks.Heat, 50), (Checks.Standing, 50), (Checks.Hook, 0),
            };
            foreach (var b in binding)
            {
                var r = Adjudicator.Resolve(
                    IntentRouter.Validate(Novel(b.check, b.amount, Effects.SuspicionDown), ctx), rich);
                if (r.Passed && r.Effect == Effects.SuspicionDown) carried++;
            }
            Check(carried == binding.Length,
                "and a requirement that bites still carries the effect it always did",
                $"{carried}/{binding.Length} landed on a state that meets them");
        }

        // ---------------------------------------------------------------
        // The living economy (roadmap M7)
        // ---------------------------------------------------------------

        static Economy FreshEconomy()
        {
            var e = new Economy();
            e.Suppliers.Add(new Supplier
            {
                Id = "drayman", Name = "Mitch", Goods = "the drink",
                ServesBusinessId = null, PricePerWeek = 90,
            });
            e.Suppliers.Add(new Supplier
            {
                Id = "grocer", Name = "Vesna", Goods = "the stock",
                ServesBusinessId = "pawnshop", PricePerWeek = 60,
            });
            return e;
        }

        static void TestEconomy()
        {
            Console.WriteLine("Economy — the street has a finite amount of money in it:");

            // THE STREET IS NOT THE BAR'S CELLAR (decision 9, audit 2026-07-27).
            // FactorFor(null) means "the district as a whole", and it must never
            // accidentally match a supplier whose ServesBusinessId happens to be
            // null. It did: the bar's drayman was authored with a null id, so his
            // refusal starved every racket in every district. The rackets read the
            // street; only the business he actually serves reads him.
            var cellar = FreshEconomy();
            var dray = cellar.SupplierNamed("drayman");
            dray.Refusing = true;
            Check(Math.Abs(cellar.FactorFor(null) - cellar.TakingsFactor) < 1e-9,
                "the district factor ignores any one supplier's tantrum (decision 9)",
                $"{cellar.FactorFor(null):0.000} vs street {cellar.TakingsFactor:0.000}");
            // And the business he DOES serve still pays for the tantrum — the
            // starving is real, it just lands on the right door.
            var served = FreshEconomy();
            served.Suppliers.Add(new Supplier
            {
                Id = "barman", Name = "Mirek2", Goods = "the drink",
                ServesBusinessId = "bar", PricePerWeek = 90, Refusing = true,
            });
            Check(served.FactorFor("bar") < served.TakingsFactor * 0.6,
                "while the door he serves goes hungry", served.FactorFor("bar").ToString("0.000"));

            // A campaign that takes nothing must behave exactly as it did before
            // this system existed. The economy bites only once you start taking.
            var quiet = FreshEconomy();
            var rich = new Wallet(100000);
            for (int d = 1; d <= 21; d++)
                quiet.DailyTick(new GameTime(d, 9, 0), rich, racketIncomeToday: 0, wagesPaidToday: 0, heat: 0.1);
            Check(quiet.TakingsFactor > 0.95 && quiet.TakingsFactor < 1.15,
                "an unsqueezed street pays out about what it always did", quiet.TakingsFactor.ToString("0.000"));

            // THE LOOP: squeezing the street makes the street poorer, and a poorer
            // street spends less in your bar. The dirty money costs you clean money.
            var squeezed = FreshEconomy();
            var wallet2 = new Wallet(100000);
            for (int d = 1; d <= 21; d++)
                squeezed.DailyTick(new GameTime(d, 9, 0), wallet2, racketIncomeToday: 170, wagesPaidToday: 0, heat: 0.1);
            Check(squeezed.Prosperity < quiet.Prosperity - 0.1,
                "a squeezed street gets poorer", $"{squeezed.Prosperity:0.00} vs {quiet.Prosperity:0.00}");
            Check(squeezed.PriceLevel > quiet.PriceLevel + 0.05,
                "and dearer", $"{squeezed.PriceLevel:0.00} vs {quiet.PriceLevel:0.00}");
            Check(squeezed.TakingsFactor < quiet.TakingsFactor * 0.85,
                "so the bar takes noticeably less", squeezed.TakingsFactor.ToString("0.000"));

            // Heat is an economic input, not a flavor: the same squeeze on a
            // hotter street leaves the district poorer. Deleting the heat
            // coupling used to leave every check in this suite green (audit
            // 2026-07-27).
            var cool = FreshEconomy(); var hot = FreshEconomy();
            var wH1 = new Wallet(100000); var wH2 = new Wallet(100000);
            for (int d = 1; d <= 21; d++)
            {
                cool.DailyTick(new GameTime(d, 9, 0), wH1, 120, 0, heat: 0.1);
                hot.DailyTick(new GameTime(d, 9, 0), wH2, 120, 0, heat: 0.9);
            }
            Check(hot.Prosperity < cool.Prosperity - 0.05,
                "a hot street is a poorer street, same squeeze",
                $"{hot.Prosperity:0.00} vs {cool.Prosperity:0.00}");
            // And a supplier who has stopped liking you charges for it.
            var soured = FreshEconomy();
            var dray2 = soured.SupplierNamed("drayman");
            int likedPrice = soured.DeliveryPrice(dray2);
            dray2.Standing = -0.9;
            Check(soured.DeliveryPrice(dray2) > likedPrice,
                "a soured supplier charges for the relationship",
                $"{soured.DeliveryPrice(dray2)} vs {likedPrice}");

            // Paying people well is economic policy, not charity.
            var generous = FreshEconomy();
            var wallet3 = new Wallet(100000);
            for (int d = 1; d <= 21; d++)
                generous.DailyTick(new GameTime(d, 9, 0), wallet3, racketIncomeToday: 170, wagesPaidToday: 110, heat: 0.1);
            Check(generous.Prosperity > squeezed.Prosperity,
                "wages put back into the street soften what the rackets take out",
                $"{generous.Prosperity:0.00} vs {squeezed.Prosperity:0.00}");

            // It must move over a week, not overnight: a player has to be able to
            // feel a decision before its consequence lands on them.
            var slow = FreshEconomy();
            double startP = slow.Prosperity;
            slow.DailyTick(new GameTime(1, 9, 0), new Wallet(100000), 180, 0, 0.5);
            Check(Math.Abs(slow.Prosperity - startP) < 0.06,
                "one bad day does not collapse a district", (slow.Prosperity - startP).ToString("0.000"));

            // No death spiral: even at maximum squeeze and maximum heat the floor
            // holds, because a floor of zero is not a decision, it is an ending.
            var worst = FreshEconomy();
            var wallet4 = new Wallet(100000);
            for (int d = 1; d <= 60; d++)
                worst.DailyTick(new GameTime(d, 9, 0), wallet4, 400, 0, 1.0);
            // Two real assertions where a tautology used to stand (audit
            // 2026-07-27: the old ">= floor" check could not fail — the daily
            // targets are clamped upstream, so 400 brutal days bottom out at
            // ~0.45 and the floor never binds on any simulated path). Pin the
            // actual worst-case equilibrium instead, tight enough that balance
            // drift in either direction is a red bar:
            Check(worst.TakingsFactor >= 0.40 && worst.TakingsFactor <= 0.50,
                "maximum squeeze and heat settle at the designed worst case, not below it",
                worst.TakingsFactor.ToString("0.000"));
            // ...and prove the floor clamp is load-bearing where it CAN bind:
            // Restore accepts PriceLevel up to 3.0 and Prosperity down to 0.0
            // from a save file, and there the formula would go to zero without it.
            var outOfBand = FreshEconomy();
            outOfBand.Prosperity = 0.0; outOfBand.PriceLevel = 3.0;
            Check(outOfBand.TakingsFactor == outOfBand.MinTakingsFactor,
                "a hostile save meets the floor, not a dead street",
                outOfBand.TakingsFactor.ToString("0.000"));
            Check(worst.Prosperity > 0.0, "the street never reaches zero", worst.Prosperity.ToString("0.000"));

            // Suppliers are people. They arrive, they are paid or they are not,
            // and they form an opinion about it.
            var supply = FreshEconomy();
            var broke = new Wallet(0);
            var evs = supply.DailyTick(new GameTime(1, 9, 0), broke, 0, 0, 0.1);
            Check(evs.Any(e => e.Kind == "supplier"), "an unpaid delivery is reported, not silently absorbed");
            Check(supply.SupplierNamed("drayman").Unpaid == 1, "and it is remembered");
            Check(supply.SupplierNamed("drayman").Standing < 0, "and it costs you with him");

            // Weekly, not daily: a delivery is an event.
            var paid = FreshEconomy();
            var w = new Wallet(100000);
            var day1 = paid.DailyTick(new GameTime(1, 9, 0), w, 0, 0, 0.1);
            Check(day1.Count(e => e.Kind == "supply") == 2, "both suppliers deliver on the first day");
            var day2 = paid.DailyTick(new GameTime(2, 9, 0), w, 0, 0, 0.1);
            Check(!day2.Any(e => e.Kind == "supply"), "and not again the next morning");
            var day8 = paid.DailyTick(new GameTime(8, 9, 0), w, 0, 0, 0.1);
            Check(day8.Any(e => e.Kind == "supply"), "but again a week later");

            // Push a supplier far enough and he stops coming. That is a business
            // starved of stock, not a business at zero.
            var lost = FreshEconomy();
            var empty = new Wallet(0);
            for (int d = 1; d <= 40; d++) lost.DailyTick(new GameTime(d, 9, 0), empty, 180, 0, 0.8);
            var mirek = lost.SupplierNamed("drayman");
            mirek.ServesBusinessId = "bar"; // as authored in the game since decision 9's audit fix
            Check(mirek.Refusing, "a supplier you never pay and a street you squeeze eventually stops delivering");
            Check(lost.FactorFor("bar") < lost.TakingsFactor,
                "the bar he supplied earns less than the street alone would explain");
            Check(lost.FactorFor(null) > 0, "but it is not shut — a floor of zero is an ending, not a decision");

            // The design decision behind that: what loses you a supplier is
            // NEGLECT, not a poor neighbourhood. A man who is paid every Thursday
            // does not walk out because the street got harder — he raises his
            // price, and you hear him do it.
            var kept = FreshEconomy();
            var flush2 = new Wallet(100000);
            int firstPrice = kept.DeliveryPrice(kept.SupplierNamed("drayman"));
            for (int d = 1; d <= 40; d++) kept.DailyTick(new GameTime(d, 9, 0), flush2, 180, 0, 0.8);
            Check(!kept.Suppliers.Any(s => s.Refusing),
                "a supplier you always pay keeps coming, however hard you squeeze the street");
            Check(kept.DeliveryPrice(kept.SupplierNamed("drayman")) > firstPrice,
                "but he charges more for it than he used to",
                $"{firstPrice} then {kept.DeliveryPrice(kept.SupplierNamed("drayman"))}");

            // Making amends is expensive on purpose: the cheap moment to keep him
            // was every week before this one.
            var poor = new Wallet(50);
            Check(!lost.MakeAmends(mirek, poor, new GameTime(41, 9, 0), out var refusedLine)
                  && refusedLine.Contains("£"),
                "you cannot fix it without the money, and he names the figure");
            var flush = new Wallet(100000);
            Check(lost.MakeAmends(mirek, flush, new GameTime(41, 9, 0), out var fixedLine) && !mirek.Refusing,
                "paying what he asks brings him back");
            Check(fixedLine.Contains("Mitch"), "and it is said as a person, not a status change");
            Check(!lost.MakeAmends(mirek, flush, new GameTime(42, 9, 0), out _),
                "and there is nothing to fix twice");

            // Legibility law: every reported line reads as somebody's
            // circumstance. No percentages, no bare numbers-as-nouns.
            var legible = FreshEconomy();
            var wl = new Wallet(100000);
            var lines = new List<string>();
            for (int d = 1; d <= 30; d++)
                foreach (var ev in legible.DailyTick(new GameTime(d, 9, 0), wl, 170, 0, 0.4))
                    lines.Add(ev.Text);
            Check(lines.Count > 0, "the economy actually says things");
            Check(!lines.Any(t => t.Contains("%")), "and never says any of them as a percentage");
            Check(legible.ProsperityWord() != null && legible.PriceWord() != null,
                "the street's state has words, not just values");

            // Persistence: the city's state is the save file (pillar P5).
            var before = FreshEconomy();
            var wb = new Wallet(100000);
            for (int d = 1; d <= 14; d++) before.DailyTick(new GameTime(d, 9, 0), wb, 150, 20, 0.3);
            before.SupplierNamed("grocer").Refusing = true;
            var after = FreshEconomy();
            after.Restore(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(before.Capture()))));
            Check(Math.Abs(after.Prosperity - before.Prosperity) < 1e-6, "prosperity survives a save");
            Check(Math.Abs(after.PriceLevel - before.PriceLevel) < 1e-6, "prices survive a save");
            Check(after.SupplierNamed("grocer").Refusing, "a supplier's refusal survives a save");
            Check(after.SupplierNamed("drayman").LastPaidDay == before.SupplierNamed("drayman").LastPaidDay,
                "and so does when he was last paid");
            after.Restore(null);
            Check(Math.Abs(after.Prosperity - before.Prosperity) < 1e-6, "restoring nothing changes nothing");
        }

        // ---------------------------------------------------------------
        // The street network (roadmap M12)
        // ---------------------------------------------------------------

        static void TestStreets()
        {
            Console.WriteLine("Streets — the city gets roads:");
            StreetMap.Rebuild();

            // Two districts now: the Hook's 5x5 and Copper Row's 5x3 across the
            // cut. Counted from the district table rather than hardcoded, so
            // adding a third district does not silently break an assertion that
            // was really about the Hook.
            int expectedJunctions = 0, expectedBlocks = 0;
            foreach (var d in StreetMap.Districts)
            {
                expectedJunctions += d.AvenuesX.Length * d.AvenuesZ.Length;
                expectedBlocks += (d.AvenuesX.Length - 1) * (d.AvenuesZ.Length - 1);
            }
            Check(StreetMap.Nodes.Count(n => n.IsJunction) == expectedJunctions,
                "every district's junctions are on the map",
                $"{StreetMap.Nodes.Count(n => n.IsJunction)} of {expectedJunctions}");
            Check(StreetMap.Blocks.Count == expectedBlocks, "and every district's buildable blocks",
                StreetMap.Blocks.Count.ToString());
            Check(StreetMap.Districts.Length == 7,
                "all seven of the design doc's districts are on the ground (M14, 2026-07-28)");

            // ---- ADDRESSES OFF THE CARRIAGEWAY -----------------------------
            //
            // Shipped without a test, which rule 5b is explicitly about, and
            // the accepting case is the half that goes unwritten: the ones that
            // must NOT move matter more here than the ones that must, because a
            // normalisation that over-reaches walks a crossing off its own
            // crossing and looks like progress while doing it.
            // NOT `AddressesSetBack > 0`, which is what I wrote first and the
            // test rejected on its first run. That counter is only non-zero on
            // the pass that actually MOVES somebody, and by the time this test
            // runs an earlier one has already touched `StreetMap` and snapped
            // them — so it reads zero, correctly, because the idempotence two
            // assertions below is working. An order-dependent assertion in a
            // suite that grows by appending is a failure waiting for somebody
            // else to be blamed for.
            //
            // The INVARIANT is the thing worth asserting and it holds on every
            // pass: whatever the order, no building stands in a carriageway
            // afterwards. `AddressesLeftInRoad` is recomputed from scratch on
            // each rebuild and is order-independent for the same reason.
            Check(HookMap.Places.Count > 0,
                "there are addresses to normalise at all",
                HookMap.Places.Count.ToString());

            // THE ACCEPTING CASE. A corner is a crossing, a cab rank, a bridge,
            // a gate — it belongs in a right of way and must be left alone.
            int cornersInRoad = 0, cornersTotal = 0;
            foreach (var pl in HookMap.Places)
            {
                if (pl.Kind != "corner") continue;
                cornersTotal++;
                if (StreetMap.OnRoad(pl.X, pl.Z)) cornersInRoad++;
            }
            Check(cornersTotal > 0, "there are corners to leave alone at all",
                cornersTotal.ToString());
            Check(StreetMap.AddressesLeftInRoad == cornersTotal,
                "and every one of them is left where it was, counted as exempt "
                + "rather than as a failure",
                $"{StreetMap.AddressesLeftInRoad} of {cornersTotal}");
            Check(cornersInRoad > 0,
                "some of them really are in a carriageway, so the exemption is "
                + "doing something rather than describing an empty set",
                cornersInRoad.ToString());

            // THE REJECTING CASE, stated as the thing that must not be true: no
            // address with a BUILDING on it may stand on tarmac a car uses.
            var stillIn = new List<string>();
            foreach (var pl in HookMap.Places)
            {
                if (!pl.Planned || pl.Kind == "corner") continue;
                if (StreetMap.OnRoad(pl.X, pl.Z)) stillIn.Add(pl.Id);
            }
            Check(stillIn.Count == 0,
                "and no address with a building on it is left in a carriageway",
                stillIn.Count == 0 ? "none" : string.Join(",", stillIn));

            // IDEMPOTENT. A normalisation that drifted a little further every
            // time `Ensure` was reached would be the worst kind of bug to find,
            // and `Rebuild` is the only way to ask it twice.
            var was = new Dictionary<string, (double, double)>();
            foreach (var pl in HookMap.Places) was[pl.Id] = (pl.X, pl.Z);
            StreetMap.Rebuild();
            int drifted = 0;
            foreach (var pl in HookMap.Places)
            {
                var (wx, wz) = was[pl.Id];
                if (Math.Abs(pl.X - wx) > 1e-9 || Math.Abs(pl.Z - wz) > 1e-9) drifted++;
            }
            Check(drifted == 0,
                "and asking twice moves nobody — the set-back is idempotent",
                drifted.ToString());

            // ---- ONE POINT OFF THE CARRIAGEWAY -----------------------------
            //
            // The accepting case FIRST, because it is the one that matters and
            // the one that goes unwritten: a point already on the pavement must
            // not move at all. A rule that shuffles everything it is handed is
            // useless for authored positions, which is what this is for.
            {
                var door = new { X = -6.0, Z = 6.0 };   // WorldBuilder.BarDoor
                Check(!StreetMap.OnRoad(door.X, door.Z),
                      "the bar door is not itself in a carriageway");
                StreetMap.OffTheCarriageway(door.X, door.Z, out var dx, out var dz);
                Check(Math.Abs(dx - door.X) < 1e-9 && Math.Abs(dz - door.Z) < 1e-9,
                      "and a point already clear of the road is left exactly alone",
                      $"({dx:0.00},{dz:0.00})");

                // AND THE REJECTING CASE, planted rather than hoped for: a
                // point ON a known centreline, which must come out clear.
                var e = StreetMap.Edges.Find(x => x.Driveable);
                Check(e != null, "there is a driveable road to stand in");
                var a = StreetMap.Node(e.A);
                var b = StreetMap.Node(e.B);
                double mx = (a.X + b.X) / 2, mz = (a.Z + b.Z) / 2;
                Check(StreetMap.OnRoad(mx, mz),
                      "the midpoint of a driveable edge is in a carriageway");
                StreetMap.OffTheCarriageway(mx, mz, out var ox, out var oz);
                Check(!StreetMap.OnRoad(ox, oz),
                      "and OffTheCarriageway takes it out of one",
                      $"({mx:0.0},{mz:0.0}) -> ({ox:0.0},{oz:0.0})");

                // IDEMPOTENT, same argument as the address set-back: a caller
                // may pass everything through this without deciding first, so
                // it has to be safe to apply twice.
                StreetMap.OffTheCarriageway(ox, oz, out var ox2, out var oz2);
                Check(Math.Abs(ox2 - ox) < 1e-9 && Math.Abs(oz2 - oz) < 1e-9,
                      "and applying it again moves nothing");
            }

            // `NearestOnRoad` MUST IGNORE LANES, which is the whole reason it
            // exists beside `NearestOnStreet`: snapping off the nearest STREET
            // cleared 14 of 31 because a place beside a service lane snapped
            // relative to the lane and landed back in the avenue.
            foreach (var e in StreetMap.Edges)
            {
                if (e.Driveable) continue;
                var a = StreetMap.Node(e.A);
                var b = StreetMap.Node(e.B);
                double mx = (a.X + b.X) / 2, mz = (a.Z + b.Z) / 2;
                StreetMap.NearestOnRoad(mx, mz, out var px, out var pz, out var w);
                Check(w >= 6.0,
                    "the nearest ROAD to a lane's midpoint is never that lane",
                    $"width {w:0.0} at ({mx:0},{mz:0})");
                break;   // one is enough; the property is structural
            }
            // A KILLING'S TOPIC KEY MUST BE THE KEY THE MILL ACTUALLY FILED,
            // AND FOR EVERY VICTIM IN THIS GAME IT WAS NOT.
            //
            // `TopicKey` built `"player.killed_" + VictimId` by hand while
            // `Fact` lowercases its parts in the constructor, so a killing of
            // "Hal" was stored as `player.killed_hal` and looked up as
            // `player.killed_Hal`. `LiveWitnesses` therefore returned nobody in
            // every run this project has kept, the inquiry could not pass
            // Procedure, and `CoatHost.Arrested` has never had a caller.
            //
            // Found by printing the two strings side by side after four builds
            // of counters that were all healthy. This is the guard so it cannot
            // come back: the accepting case is a capitalised name, because
            // capitalised is what every name in the cast is.
            {
                var mill = new GossipMill(new SocialGraph());
                var ids = new List<string> { "w0", "w1", "w2" };
                foreach (var id in ids) mill.Add(new Gossiper(id, id, null, null, null));

                var book = new HomicideBook();
                var when = new GameTime { Day = 5, Hour = 22 };
                var k = book.Record("Hal", "Hal", when.Day, when.Hour, "hook");
                foreach (var id in ids) k.SawYouDoIt.Add(id);
                book.FileWith(mill, k, when, _ => true);

                var held = mill.Get("w0").Rumors[0].Content;
                Check(k.TopicKey == held.Subject + "." + held.Predicate,
                      "a killing's topic key is the key the mill filed it under",
                      $"want {k.TopicKey} filed {held.Subject}.{held.Predicate}");

                int holds = 0;
                foreach (var id in k.SawYouDoIt)
                    if (mill.Get(id)?.BestOfValue(k.TopicKey, "true") != null) holds++;
                Check(holds == ids.Count,
                      "and every witness to a capitalised name can be found again",
                      $"{holds} of {ids.Count}");

                Check(book.LiveWitnesses(mill, _ => true).Count == ids.Count,
                      "so LiveWitnesses returns them, which is what drives the inquiry",
                      book.LiveWitnesses(mill, _ => true).Count.ToString());
            }

            // NEGOTIATION — the design claim, asserted rather than described.
            //
            // The comment in `Negotiation.cs` says the fast levers cost you the
            // person. That is the whole thesis of the game in one object, and a
            // thesis living only in a comment is the thing this project has
            // been caught by more than any other. So it is a test.
            {
                Func<double, double, double, Gossiper> who = (greed, nerve, loyal) =>
                {
                    var g = new Gossiper("x", "X", null, null, null);
                    g.Greed = greed; g.Nerve = nerve; g.Loyalty = loyal;
                    return g;
                };

                // THE ACCEPTING CASE FIRST. An honest, well-aimed offer to a
                // greedy man gets there, and costs nothing afterwards.
                var greedy = who(0.9, 0.5, 0.5);
                var p = Negotiation.Open(greedy, 0.6);
                Check(p.Resistance > 0 && !p.Agreed, "a real ask opens as a no",
                      p.Resistance.ToString("0.00"));
                for (int i = 0; i < 4 && !p.Agreed && !p.Walked; i++)
                    Negotiation.Push(p, greedy, Lever.Money, 1.0);
                Check(p.Agreed, "money moves a greedy man to yes", p.Why);
                Check(Negotiation.LoyaltyCost(p) == 0,
                      "and paying somebody costs you nothing afterwards");

                // THE CLAIM ITSELF: the same yes, bought with a threat, costs.
                var timid = who(0.5, 0.1, 0.5);
                var q = Negotiation.Open(timid, 0.6);
                Negotiation.Push(q, timid, Lever.Threat, 1.0);
                Check(q.Resentment > 0, "a threat always costs, even when it works",
                      q.Resentment.ToString("0.00"));
                Check(Negotiation.LoyaltyCost(q) > 0,
                      "and the cost outlives the scene");

                // AND IT CAN END THE RELATIONSHIP. Two hard threats and they
                // stop dealing with you at all — a negotiation you can LOSE by
                // winning too hard.
                var brave = who(0.5, 0.9, 0.5);
                var r = Negotiation.Open(brave, 1.0);
                Negotiation.Push(r, brave, Lever.Threat, 1.0);
                Negotiation.Push(r, brave, Lever.Threat, 1.0);
                Check(r.Walked, "leaning on a brave man twice ends the relationship", r.Why);
                Check(!r.Agreed, "and walking is not agreeing");
                Check(r.Resistance > 0.3,
                      "he was never close to yes either — threats do not move nerve",
                      r.Resistance.ToString("0.00"));

                // REPEATING YOURSELF IS WORTH LESS. The third push of one lever
                // must move strictly less than the first, or a player grinds
                // one idea into a yes and there is no negotiation to have.
                var a1 = who(0.5, 0.5, 0.5); var s1 = Negotiation.Open(a1, 1.0);
                double before1 = s1.Resistance;
                Negotiation.Push(s1, a1, Lever.Money, 0.5);
                double first = before1 - s1.Resistance;
                Negotiation.Push(s1, a1, Lever.Money, 0.5);
                double beforeThird = s1.Resistance;
                Negotiation.Push(s1, a1, Lever.Money, 0.5);
                Check(beforeThird - s1.Resistance < first,
                      "the third push of one lever moves less than the first");

                // A LIE THEY CAN CHECK MOVES NOTHING AND COSTS LIKE A THREAT,
                // or claiming a favour would be strictly better than doing one.
                var honestMan = who(0.5, 0.5, 0.5);
                var t = Negotiation.Open(honestMan, 0.5);
                double held = t.Resistance;
                Negotiation.Push(t, honestMan, Lever.Need, 1.0, honest: false);
                Check(t.Resistance == held, "a lie moves nobody", t.Resistance.ToString("0.00"));
                Check(t.Resentment > 0, "and being taken for a fool costs");

                // RESPECT COMPOUNDS WHERE THE OTHERS DECAY: it is the only
                // lever that works better on somebody who already trusts you,
                // which is what makes having been decent earlier pay.
                var warm = who(0.5, 0.5, 0.9); var cold = who(0.5, 0.5, 0.1);
                var pw = Negotiation.Open(warm, 1.0); var pc = Negotiation.Open(cold, 1.0);
                double bw = pw.Resistance, bc = pc.Resistance;
                Negotiation.Push(pw, warm, Lever.Respect, 1.0);
                Negotiation.Push(pc, cold, Lever.Respect, 1.0);
                Check((bw - pw.Resistance) > (bc - pc.Resistance),
                      "respect moves somebody who trusts you further than somebody who does not");

                // AND THE MODEL IS HANDED A STANCE, NEVER A LINE. If this ever
                // starts containing dialogue, the file has stopped obeying
                // "game state decides, the model performs".
                var stance = Negotiation.Stance(q, timid);
                Check(stance.Length > 0 && !stance.Contains("\""),
                      "the stance handed to the model is a position, not a script");
            }

            // No two districts may overlap: every junction must sit in exactly
            // the district that claims it, or DistrictAt would lie somewhere.
            // FROM THE BLOCKS, NOT FROM THE AVENUE ARRAYS.
            //
            // This used to average `AvenuesX[0]` and `AvenuesX[last]` and ask
            // `DistrictAt` about the result. Those arrays are UNSCALED source
            // data and `WideBlocks` scales the whole city about the origin, so
            // the test was asking about a coordinate that is not anywhere on
            // the map — it passed only because `DistrictAt` had the identical
            // fault and the two errors cancelled. Fixing `DistrictAt` is what
            // made this go red, which is the honest way round for a test that
            // never had a chance of catching the bug it sat next to.
            //
            // A block's centre is a real, scaled place with buildings on it,
            // so this now asserts something about the world rather than about
            // one arithmetic mistake agreeing with another.
            foreach (var d in StreetMap.Districts)
            {
                StreetMap.Block mid = null;
                foreach (var b in StreetMap.Blocks)
                    if (StreetMap.DistrictAt(b.CentreX, b.CentreZ) == d.Name) { mid = b; break; }
                Check(mid != null, $"{d.Name} has a block to test with",
                    mid == null ? "none" : "ok");
                if (mid == null) continue;
                Check(StreetMap.DistrictAt(mid.CentreX, mid.CentreZ) == d.Name,
                    $"a block in {d.Name} resolves to {d.Name}",
                    StreetMap.DistrictAt(mid.CentreX, mid.CentreZ) ?? "nowhere");
            }

            // A DISTRICT CONTAINS THE THINGS BUILT IN IT, which is not what a
            // box around the avenues gives you.
            //
            // `parcelsByDistrict` came back `none:268` of 376 — 71% of every
            // terrace in the world belonging to no district, and Fairview
            // absent entirely. The cause was a flat 12m margin against block
            // spacing of 20 to 34m: a parcel outside the outermost avenue sits
            // up to HALF A BLOCK beyond it, so the box was too small in six of
            // seven districts and worst where blocks are widest.
            //
            // The ordering it produced looked like a finding — the Hook keeps
            // the most because its blocks are the tightest — and agreed with
            // the district photographs, which is the hardest kind of wrong
            // number to catch.
            //
            // EVERY BLOCK IS IN A DISTRICT, AND THIS IS THE ASSERTION THAT
            // WOULD HAVE CAUGHT THE WHOLE THING.
            //
            // `DistrictAt` read the avenue arrays RAW while `WideBlocks`
            // scales the city about the origin, so it tested scaled positions
            // against unscaled boxes: 38 of 52 block centres were in no
            // district at all and the Exchange, the Parade, Fairview and
            // Gullwing contained NONE. Their buildings stand 136-184m from the
            // streets named for them, which is what every district photograph
            // has been showing.
            //
            // A block is a rectangle of buildable ground bounded by four
            // avenues OF A DISTRICT — it cannot be in none of them. That is a
            // property of the map, not a threshold, so it needs no measured
            // bound and there is nothing here to tune.
            //
            // The previous version of this paragraph explained why the
            // assertion could not be written yet, and blamed the flat 12m
            // margin. Wrong premise: with the box in the right PLACE, margins
            // of 12, 20 and 26 assign all 52 blocks identically.
            {
                int homeless = 0;
                var perDistrict = new Dictionary<string, int>();
                foreach (var b in StreetMap.Blocks)
                {
                    var dn = StreetMap.DistrictAt(b.CentreX, b.CentreZ);
                    if (dn == null) { homeless++; continue; }
                    perDistrict.TryGetValue(dn, out var n);
                    perDistrict[dn] = n + 1;
                }
                Check(homeless == 0,
                    "every block on the map is inside some district",
                    $"{homeless} of {StreetMap.Blocks.Count} in none");
                // AND THE DENOMINATOR ON THE OTHER SIDE (rule 3b): zero
                // homeless blocks would also be true of a map with no blocks,
                // and "every district has some" is the half that says the
                // districts are all real places rather than one district
                // having swallowed the lot.
                var empty = new List<string>();
                foreach (var d in StreetMap.Districts)
                    if (!perDistrict.ContainsKey(d.Name)) empty.Add(d.Name);
                Check(empty.Count == 0,
                    "and every district has blocks in it",
                    empty.Count == 0
                        ? $"{StreetMap.Blocks.Count} blocks over {StreetMap.Districts.Length} districts"
                        : string.Join("/", empty.ToArray()));
            }

            // AND THE WIDER BOXES MUST STILL NOT TOUCH, which is the half that
            // a margin change can break silently: `DistrictAt` returns the
            // FIRST match, so an overlap would not error, it would quietly
            // hand every point in the seam to whichever district is declared
            // earlier. The separations run to 40m at the tightest, so this
            // passes today — and it is asserted rather than assumed, because
            // the next district added is what breaks it.
            for (int a = 0; a < StreetMap.Districts.Length; a++)
                for (int b = a + 1; b < StreetMap.Districts.Length; b++)
                {
                    var da = StreetMap.Districts[a];
                    var db = StreetMap.Districts[b];
                    double ma = 0, mb = 0;
                    for (int i = 1; i < da.AvenuesX.Length; i++) ma = Math.Max(ma, (da.AvenuesX[i] - da.AvenuesX[i - 1]) / 2);
                    for (int i = 1; i < da.AvenuesZ.Length; i++) ma = Math.Max(ma, (da.AvenuesZ[i] - da.AvenuesZ[i - 1]) / 2);
                    for (int i = 1; i < db.AvenuesX.Length; i++) mb = Math.Max(mb, (db.AvenuesX[i] - db.AvenuesX[i - 1]) / 2);
                    for (int i = 1; i < db.AvenuesZ.Length; i++) mb = Math.Max(mb, (db.AvenuesZ[i] - db.AvenuesZ[i - 1]) / 2);
                    ma = Math.Max(12, ma); mb = Math.Max(12, mb);
                    bool xOverlap = da.AvenuesX[0] - ma <= db.AvenuesX[db.AvenuesX.Length - 1] + mb
                                 && db.AvenuesX[0] - mb <= da.AvenuesX[da.AvenuesX.Length - 1] + ma;
                    bool zOverlap = da.AvenuesZ[0] - ma <= db.AvenuesZ[db.AvenuesZ.Length - 1] + mb
                                 && db.AvenuesZ[0] - mb <= da.AvenuesZ[da.AvenuesZ.Length - 1] + ma;
                    Check(!(xOverlap && zOverlap),
                        $"{da.Name} and {db.Name} do not overlap once the margins are half a block");
                }

            // Ironside's whole brief is "places without witnesses", and the only
            // part of that a map can carry is the block size: fewer corners per
            // acre means longer walls and nowhere to be standing by accident.
            double BlockSpan(string id)
            {
                var d = StreetMap.Districts.First(x => x.Id == id);
                return d.AvenuesX[1] - d.AvenuesX[0];
            }
            Check(BlockSpan("ironside") > BlockSpan("hook") && BlockSpan("hook") > BlockSpan("copper"),
                "Ironside's blocks are the widest and the market quarter's the tightest",
                $"{BlockSpan("ironside")} / {BlockSpan("hook")} / {BlockSpan("copper")}");

            // Scale, against the urban-design benchmarks. Portland's walkable
            // block is 79m and Barcelona's Eixample is 113m; a game compresses,
            // but the OLD district was a 90m slab entire — one city block for a
            // whole city, which is why it read as a diorama.
            double span = StreetMap.AvenuesX.Max() - StreetMap.AvenuesX.Min();
            Check(span >= 100, "the city spans more than a single real city block", span + "m");
            Check(StreetMap.Spacing >= 20 && StreetMap.Spacing <= 40,
                "blocks are compressed for a game but not alleys", StreetMap.Spacing.ToString());
            foreach (var b in StreetMap.Blocks)
                Check(b.Width >= 12 && b.Depth >= 12, "every block has room to build on",
                    $"{b.Width}x{b.Depth}");

            // THE ONE THAT CAUGHT A REAL BUG. An earlier grid put avenues
            // straight through all four founding corner buildings; nobody
            // should discover that by driving into one. The founding boxes are
            // re-placed into blocks by the world builder now, so what this
            // asserts is that the ones that have NOT moved are still clear.
            foreach (var x in StreetMap.AvenuesX)
                Check(x == 0 || StreetMap.AvenueClear(x, northSouth: true),
                    $"the avenue at x={x} does not cut through a standing building");
            foreach (var z in StreetMap.AvenuesZ)
                Check(z == 0 || StreetMap.AvenueClear(z, northSouth: false),
                    $"the avenue at z={z} does not cut through a standing building");

            // Every named place must sit on buildable ground or on its own
            // lane — a doorway in the middle of an avenue is not a doorway.
            foreach (var place in HookMap.Places)
            {
                bool onBlock = StreetMap.BlockAt(place.X, place.Z) != null;
                bool nearRoad = StreetMap.OnStreet(place.X, place.Z, margin: 3);
                Check(onBlock || nearRoad, $"{place.Id} is either on a block or beside a road",
                    $"({place.X},{place.Z})");
            }
            Check(StreetMap.Edges.Any(e => e.Kind == "avenue"), "there are avenues");
            Check(StreetMap.Edges.Any(e => e.Kind == "lane"), "and lanes to the doors");

            // The founding cross must survive untouched — geometry is already
            // built on it and moving a road under a building is not a refactor.
            Check(StreetMap.AvenuesX.Contains(0.0) && StreetMap.AvenuesZ.Contains(0.0),
                "the founding cross at x=0 and z=0 is part of the grid, so nothing built moves");
            Check(StreetMap.Edges.Any(e => e.Kind == "street"), "and keeps its own narrower class");

            // Irregular spacing: a chessboard reads as a chessboard.
            // A regular grid is fine — Barcelona's Eixample is one, and the
            // research is clear that what makes a grid read as designed is the
            // CHAMFERED CORNER, not irregular spacing. Cutting the corner off
            // each block turns every crossroads into a small plaza and opens
            // the diagonal sightline, for almost nothing.
            Check(StreetMap.Chamfer > 0 && StreetMap.Chamfer < StreetMap.Spacing / 4,
                "junction corners are chamfered, and modestly", StreetMap.Chamfer.ToString());

            // THE PROPERTY THAT MATTERS. An unreachable address is worse than no
            // streets at all, because the player will walk at it.
            Check(StreetMap.FullyConnected(), "every junction is reachable from every other by road");
            foreach (var place in HookMap.Places)
            {
                var stop = StreetMap.Node("stop_" + place.Id);
                Check(stop != null, $"{place.Id} is on the map as an address");
                Check(StreetMap.EdgesAt(stop.Id).Any(), $"{place.Id} has a lane to a street");
            }

            // Every place routes to every other. Sampled across the extremes
            // rather than all 576 pairs, which would be slow and no more true.
            var ends = new[] { "bar_door", "customs_shed", "warehouse_row", "tenement_north", "repair_yard" };
            foreach (var a in ends)
                foreach (var b in ends)
                {
                    var route = StreetMap.Route("stop_" + a, "stop_" + b);
                    Check(route.Count > 0, $"you can get from {a} to {b}");
                    Check(route[0].Id == "stop_" + a && route[route.Count - 1].Id == "stop_" + b,
                        $"and the route from {a} to {b} actually starts and ends there");
                }

            // A driving route may pull out of a lane and park in one, but must
            // not thread lanes in the middle — that is driving through gardens.
            var drive = StreetMap.Route("stop_bar_door", "stop_customs_shed", driveableOnly: true);
            Check(drive.Count > 2, "a car can drive across the city");
            for (int i = 1; i + 1 < drive.Count; i++)
                Check(drive[i].IsJunction, "and does it on junctions, not through people's lanes", drive[i].Id);

            // Steering: the nearest point on a street, and what counts as road.
            Check(StreetMap.NearestOnStreet(2, 2, out var nx, out var nz, out var ne),
                "any position has a nearest street");
            Check(Math.Abs(nx) < 3 || Math.Abs(nz) < 3, "which near the crossing is the crossing", $"{nx:0.0},{nz:0.0}");
            Check(StreetMap.OnRoad(0, 0), "the middle of the founding crossing is road");
            // ASKED OF THE MAP, NOT REMEMBERED. This was `OnRoad(26, 10)`,
            // and 26 was an avenue line when the grid pitch was 26m. The
            // topology re-plan (street-spec.md) stretches the city, that line
            // moved to 55.9, and the test failed while asserting something
            // still perfectly true — a gate reading a coordinate it was
            // handed once rather than the geometry it means to check. Take a
            // junction and step along its own avenue instead: correct at any
            // pitch, and it fails only if an avenue genuinely stops being
            // road.
            var anyJ = StreetMap.Nodes.First(n => n.IsJunction
                && StreetMap.EdgesAt(n.Id).Any(e => e.Driveable));
            var anyE = StreetMap.EdgesAt(anyJ.Id).First(e => e.Driveable);
            var farEnd = StreetMap.Node(StreetMap.Other(anyE, anyJ.Id));
            Check(StreetMap.OnRoad((anyJ.X + farEnd.X) / 2, (anyJ.Z + farEnd.Z) / 2),
                "an avenue is road along its length", $"{anyJ.Id}->{farEnd.Id}");
            // No AVENUE may cross a block interior — that is the whole promise
            // of a grid. Lanes may and should: a lane crossing a courtyard to
            // reach a door is a driveway, which is correct.
            foreach (var b in StreetMap.Blocks)
                Check(!StreetMap.OnRoad(b.CentreX, b.CentreZ),
                    "no avenue runs through the middle of a block", $"({b.CentreX},{b.CentreZ})");
            Check(StreetMap.Blocks.Any(b => StreetMap.OnStreet(b.CentreX, b.CentreZ)),
                "but lanes do reach into blocks, because doors are inside them");

            // Determinism: the city must be the same city every run.
            var before = StreetMap.Edges.Count;
            StreetMap.Rebuild();
            Check(StreetMap.Edges.Count == before, "rebuilding produces the same city");

            // Streets have names, and the plates and the gossip read the same
            // table — the city must never tell the player one name and a
            // character another.
            Check(StreetMap.NameOf(0, northSouth: true) == "Hook Street",
                "the founding street is Hook Street, where the bar is");
            Check(StreetMap.NameOf(7, northSouth: true, near: 0) == null, "and nothing runs where no avenue runs");
            var namesSeen = new HashSet<string>();
            foreach (var d in StreetMap.Districts)
            {
                foreach (var x in d.AvenuesX) namesSeen.Add(StreetMap.NameOf(x, true, d.AvenuesZ[0]));
                foreach (var z in d.AvenuesZ) namesSeen.Add(StreetMap.NameOf(z, false, d.AvenuesX[0]));
            }
            Check(!namesSeen.Contains(null), "every street in the city has a name");
            Check(namesSeen.Count >= 16, "and there are a lot of them now", namesSeen.Count.ToString());
            Check(StreetMap.NamesAt(StreetMap.Node("j2_2"), out var nsName, out var ewName)
                && nsName == "Hook Street" && ewName == "Quay Street",
                "a junction is the corner of two named streets", $"{nsName} / {ewName}");
            Check(!StreetMap.NamesAt(StreetMap.Node("stop_bar_door"), out _, out _),
                "and a doorway is not a corner");
            Check(StreetMap.AddressOf(0, 0) == "Hook Street at Quay Street",
                "standing on the crossing, you are on a corner", StreetMap.AddressOf(0, 0));
            Check(StreetMap.AddressOf(-6, 6) != null, "and anywhere else has a nearest street",
                StreetMap.AddressOf(-6, 6));

            // COPPER ROW. It was in the population and the fiction and nowhere on
            // the ground, which meant the game could talk about somewhere the
            // player could never walk to.
            Check(StreetMap.DistrictAt(-6, 6) == "the Hook", "the bar is in the Hook");
            Check(StreetMap.DistrictAt(-6, 102) == "Copper Row", "and the covered market is across the cut");
            Check(StreetMap.DistrictAt(0, 72) == null, "with the cut between them");

            // x=0 is Hook Street in one district and Copper Row in the other,
            // which is how streets actually work.
            Check(StreetMap.NameOf(0, northSouth: true, near: 0) == "Hook Street",
                "x=0 is Hook Street where the bar is");
            Check(StreetMap.NameOf(0, northSouth: true, near: 112) == "Copper Row",
                "and Copper Row across the cut", StreetMap.NameOf(0, true, 112));
            Check(StreetMap.AddressOf(0, 112) == "Copper Row at Market Road",
                "so a corner up there is named from its own district", StreetMap.AddressOf(0, 112));

            // The property that matters, extended: a second district is only
            // real if you can GET there. Two bridges, and every Copper Row
            // address routes from the bar.
            foreach (var id in new[] { "covered_market", "weighhouse", "north_market", "stair_tenements", "money_changer" })
            {
                var over = StreetMap.Route("stop_bar_door", "stop_" + id);
                Check(over.Count > 0, $"you can walk from the bar to {id}");
                var driven = StreetMap.Route("stop_bar_door", "stop_" + id, driveableOnly: true);
                Check(driven.Count > 0, $"and drive there");
            }
            var backAgain = StreetMap.Route("stop_north_market", "stop_customs_shed", driveableOnly: true);
            Check(backAgain.Count > 0, "and come back the other way");

            // Only two ways across, because a chokepoint is a place things can
            // happen and an open grid is not.
            int bridges = 0;
            foreach (var e in StreetMap.Edges)
            {
                var a = StreetMap.Node(e.A);
                var b = StreetMap.Node(e.B);
                if (a == null || b == null) continue;
                // The CUT is water only where the Hook faces Copper Row; the
                // Fairview drive crosses the same latitude far to the west,
                // over dry hillside (M14).
                bool inCutX = a.X > -60 && a.X < 60 && b.X > -60 && b.X < 60;
                if (inCutX && ((a.Z < 60 && b.Z > 60) || (b.Z < 60 && a.Z > 60))) bridges++;
            }
            Check(bridges == 2, "two bridges across the cut, and only two", bridges.ToString());

            // Copper Row is tighter than the Hook — older and denser, and it
            // costs nothing, because the grid generator does not care.
            var copper = StreetMap.Districts[1];
            double copperGap = copper.AvenuesX[1] - copper.AvenuesX[0];
            Check(copperGap < StreetMap.Spacing, "Copper Row's blocks are tighter than the Hook's",
                $"{copperGap} vs {StreetMap.Spacing}");

            Check(StreetMap.Route("nowhere", "stop_bar_door").Count == 0, "a route from nowhere is empty, not null");
            Check(StreetMap.Route("stop_bar_door", "stop_bar_door").Count == 1, "and a route to where you stand is one stop");
        }

        // ---------------------------------------------------------------
        // D18, the content rule, at the one enforcement site that is code
        // ---------------------------------------------------------------

        static void TestContentRule()
        {
            Console.WriteLine("ContentRule — D18 at the generator:");

            // ACCEPTING FIRST, AND ON THE LIVE TABLES. A validator nothing
            // survives is the expensive failure, so before any refusal is
            // checked, the crowd this project actually ships has to pass.
            var refused = Population.TradesRefused;
            Check(refused.Count == 0,
                  "ACCEPTING: the live trade table is clean",
                  $"refused {refused.Count} of {Population.TradesScreened}: "
                  + string.Join(", ", refused));
            Check(Population.TradesScreened >= 30,
                  "and the screen looked at the whole table",
                  $"screened {Population.TradesScreened}");

            // The live cast: 60 tier-2 cards, none under the floor. Read off
            // the ages the generator would have to honour rather than a
            // number typed here.
            Check(ContentRule.IsShowableAge(24) && ContentRule.IsShowableAge(58),
                  "ACCEPTING: the live cast's youngest and oldest ages pass");
            foreach (var stem in new[] { "Adam", "Kate", "SportyGranny",
                                         "BigVegas", "TheBoss", "Michelle" })
                Check(!ContentRule.IsUnderageModel(stem),
                      $"ACCEPTING: the live model '{stem}' is not refused");

            // AND THE WORDS THAT MUST NOT BE REFUSED. British usage: a boy
            // is a grown man, the lads are dockers, a son can be forty.
            foreach (var stem in new[] { "Boyer", "Childers", "Sonya",
                                         "Kidman", "Ladd" })
                Check(!ContentRule.IsUnderageModel(stem),
                      $"ACCEPTING: '{stem}' is a name, not a child");
            foreach (var trade in new[] { "barber", "bartender", "waitress",
                                          "nurse", "dock hand" })
                Check(ContentRule.IsShowableTrade(trade),
                      $"ACCEPTING: trade '{trade}' is allowed");

            // REJECTING, on synthetic values that exist nowhere in the repo,
            // so doing the work this rule asks for can never break its test.
            Check(!ContentRule.IsShowableAge(17), "17 is refused");
            Check(!ContentRule.IsShowableAge(0), "0 is refused");
            Check(!ContentRule.IsShowableAge(-4),
                  "a negative age is refused, not accepted by arithmetic");
            Check(ContentRule.AdultFloorYears == 18, "the floor is eighteen");
            foreach (var stem in new[] { "ChildModel", "school_boy",
                                         "Teenager", "toddler_walk", "Kid" })
                Check(ContentRule.IsUnderageModel(stem),
                      $"REJECTING: model '{stem}' is refused");
            foreach (var trade in new[] { "brewer", "bookmaker",
                                          "turf accountant", "croupier",
                                          "bingo caller" })
                Check(!ContentRule.IsShowableTrade(trade),
                      $"REJECTING: trade '{trade}' is refused");

            // AND THE RUN WHERE THE THING IT ASSERTS CAN HAPPEN. Plant a
            // refused trade in a table and prove the screen sees it, so this
            // is a guard rather than a ratchet that only ever says zero.
            var planted = ContentRule.Screen(new[]
                { "dock hand", "bookmaker", "clerk", "brewer" });
            Check(planted.Count == 2,
                  "PLANTED: a table with two refused trades screens to two",
                  $"screened out {planted.Count}: {string.Join(", ", planted)}");

            // THE GENERATOR CANNOT PRODUCE ONE, which is the point of the
            // site: not that the table is clean today, but that a resident
            // drawn three thousand times is drawn from the screened wheel.
            var city = Population.Generate(3000, 20260726,
                new[] { "the Hook", "Copper Row", "Ironside" });
            int bad = 0;
            foreach (var r in city.Residents)
                if (!ContentRule.IsShowableTrade(r.Trade)) bad++;
            Check(bad == 0,
                  $"3000 generated residents, 0 refused trades among them",
                  $"{bad} of {city.Residents.Count}");
        }

        // ---------------------------------------------------------------
        // People live in their own district (M9 + Copper Row)
        // ---------------------------------------------------------------

        static void TestPopulationDistricts()
        {
            Console.WriteLine("Population — people live where they say they live:");
            StreetMap.Rebuild();
            var pop = Population.Generate(600, 4242, new[] { "the Hook", "Copper Row" });

            int hookHomes = 0, copperHomes = 0, commuters = 0, misplaced = 0;
            foreach (var r in pop.Residents)
            {
                var where = StreetMap.DistrictAt(r.HomeX, r.HomeZ);
                if (where != r.District) misplaced++;
                if (r.District == "the Hook") hookHomes++; else copperHomes++;
                if (StreetMap.DistrictAt(r.WorkX, r.WorkZ) != r.District) commuters++;
            }

            // THE BUG THIS EXISTS TO CATCH: anchors were -40..40 for everybody,
            // which was fine with one district and quietly wrong with two —
            // every resident "of Copper Row" was living in the Hook, and the
            // crowd would never have gone north of the cut.
            Check(misplaced == 0, "everybody's home is in the district they belong to", misplaced.ToString());
            Check(copperHomes > 200, "and Copper Row has a real share of the city", copperHomes.ToString());
            Check(hookHomes > 200, "without emptying the Hook", hookHomes.ToString());

            // A third cross the water to work, which is what makes two bridges
            // carry somebody rather than being scenery.
            double commuteShare = (double)commuters / pop.Residents.Count;
            Check(commuteShare > 0.2 && commuteShare < 0.45,
                "about a third of the city crosses the cut to work", commuteShare.ToString("0.00"));

            // Still deterministic, which the whole save format depends on.
            var twin = Population.Generate(600, 4242, new[] { "the Hook", "Copper Row" });
            bool same = true;
            for (int i = 0; i < pop.Residents.Count && same; i++)
                same = twin.Residents[i].HomeX == pop.Residents[i].HomeX
                    && twin.Residents[i].WorkZ == pop.Residents[i].WorkZ;
            Check(same, "and the same seed still builds the same city");

            // A district that exists in the fiction and not on the ground must
            // not throw. Ironside used to be the example and now has streets;
            // Downtown is still only a name in §7 of the design doc.
            var withGhost = Population.Generate(60, 7, new[] { "the Hook", "Downtown" });
            Check(withGhost.Residents.Count == 60, "somewhere not yet built still houses its people");

            // IRONSIDE. Its whole brief is "places without witnesses", and the
            // only thing that actually makes a place unwitnessed is that nobody
            // is in it. So the district has to be genuinely thin at night — and
            // genuinely busy by day, or it is a hole in the map rather than a
            // working part of the city somebody has a reason to walk into.
            var city = Population.Generate(3000, 20260726,
                new[] { "the Hook", "Copper Row", "Ironside" },
                new[] { 45, 40, 7 }, new[] { 35, 30, 33 });
            int sleepsIn = 0, worksIn = 0;
            foreach (var r in city.Residents)
            {
                if (r.District == "Ironside") sleepsIn++;
                if (StreetMap.DistrictAt(r.WorkX, r.WorkZ) == "Ironside") worksIn++;
            }
            double sleepShare = (double)sleepsIn / city.Residents.Count;
            double workShare = (double)worksIn / city.Residents.Count;
            Check(sleepShare < 0.12, "almost nobody sleeps in Ironside", sleepShare.ToString("0.00"));
            Check(workShare > sleepShare * 1.5,
                "and far more people spend the day there than the night — which IS the district",
                $"{workShare:0.00} by day against {sleepShare:0.00} by night");

            // And the homes it does have are in Ironside, not quietly in the
            // Hook: the exact bug the two-district version of this test caught.
            int ironMisplaced = 0;
            foreach (var r in city.Residents)
                if (r.District == "Ironside" && StreetMap.DistrictAt(r.HomeX, r.HomeZ) != "Ironside")
                    ironMisplaced++;
            Check(ironMisplaced == 0, "and the few who do live there live there", ironMisplaced.ToString());
        }

        // ---------------------------------------------------------------
        // Phones and the distance layer (roadmap M10)
        // ---------------------------------------------------------------

        static void TestPhones()
        {
            Console.WriteLine("Phones — a phone is a place, not a pocket:");
            var book = new PhoneBook();
            var bar = new Phone { PlaceId = "bar", PlaceName = "the bar", OpenFrom = 10, OpenTo = 24 };
            bar.Regulars.Add("Lena"); bar.Regulars.Add("Rocco");
            book.Add(bar);
            var house = new Phone { PlaceId = "boarding", PlaceName = "the boarding house", Public = true, OpenFrom = 7, OpenTo = 22 };
            house.Regulars.Add("Ada"); house.Regulars.Add("Sam");
            book.Add(house);

            var noon = new GameTime(3, 12, 0);
            Func<string, string, bool> everyone = (who, where) => true;
            Func<string, string, bool> nobody = (who, where) => false;

            // No line at all.
            var nowhere = book.Ring("customs_shed", "Hal", noon, everyone);
            Check(nowhere.Result == CallResult.NoLine, "some places still expect you to walk");

            // Out of hours the bell rings in an empty room.
            var dawn = book.Ring("bar", "Lena", new GameTime(3, 4, 0), everyone);
            Check(dawn.Result == CallResult.NoAnswer, "nobody keeps the bar line at four in the morning");

            // THE GOOD CASE.
            var got = book.Ring("bar", "Lena", noon, everyone);
            Check(got.Result == CallResult.Answered && got.AnsweredById == "Lena",
                "ring the bar at noon and Lena picks up");

            // THE INTERESTING CASE — not a failure state. Lena is out, Rocco is
            // by the phone, and now Rocco knows you rang.
            Func<string, string, bool> lenaOut = (who, where) => who != "Lena";
            var wrongPerson = book.Ring("bar", "Lena", noon, lenaOut);
            Check(wrongPerson.Result == CallResult.SomebodyElse && wrongPerson.AnsweredById == "Rocco",
                "somebody else picking up is the interesting outcome, not a failure");
            Check(wrongPerson.Line.Contains("now they know you rang"),
                "and the game says so plainly", wrongPerson.Line);

            // Nobody near it at all.
            var empty = book.Ring("bar", "Lena", noon, nobody);
            Check(empty.Result == CallResult.NoAnswer, "and an empty room is an empty room");

            // Order matters: whoever is nearest reaches for it first.
            Check(book.Ring("bar", "Rocco", noon, everyone).AnsweredById == "Lena",
                "whoever is by the phone answers it, not whoever you wanted");

            // MESSAGES. The cost is that the person holding it now knows.
            var mill = new GossipMill(new SocialGraph());
            var rocco = new Gossiper("Rocco", "Rocco", null, null, null, "night", 0.5, 0.5, 0.6);
            mill.Add(rocco);
            int memories = rocco.Memory.Events.Count, rumors = rocco.Rumors.Count;
            Check(book.LeaveMessage(wrongPerson, mill, "player", "Tell her Novak called about the delivery.", noon),
                "you can leave word with whoever answered");
            Check(rocco.Memory.Events.Count > memories, "and they remember taking it");
            Check(rocco.Rumors.Count > rumors, "and it enters the mill as talk, because that is what a message is");
            Check(rocco.Rumors[rocco.Rumors.Count - 1].Hops == 1,
                "one hop out, because somebody is carrying it for you");
            Check(rocco.Rumors[rocco.Rumors.Count - 1].Confidence < 0.7,
                "at second-hand confidence, like anything passed along");
            Check(!book.LeaveMessage(empty, mill, "player", "anything", noon),
                "you cannot leave a message with nobody");
            Check(!book.LeaveMessage(null, mill, "player", "anything", noon), "or with nothing");

            // REACH is the thing a phone buys, and it is real.
            Check(book.ReachableNow("Lena", noon, everyone), "Lena can be reached at noon");
            Check(!book.ReachableNow("Lena", new GameTime(3, 4, 0), everyone),
                "and cannot at four in the morning");
            Check(!book.ReachableNow("Lena", noon, lenaOut), "or when she simply is not there");
            // SOMEBODY WITH NO LINE OF THEIR OWN IS NOT ON A PRIVATE ONE — and
            // this used to read "is never on one", which stopped being the rule
            // the moment `Phone.Public` was read at all.
            //
            // At eleven at night the bar is open and the boarding house is
            // shut, so the only line live is a private one Hal is not on. That
            // is the assertion that still means something, and it is sharper
            // than the old one: it pins what PUBLIC buys rather than what
            // having no number costs.
            var lateNight = new GameTime(3, 23, 0);
            Check(!book.ReachableNow("Hal", lateNight, everyone),
                "somebody with no line of their own is not on a private one");
            Check(book.ReachableNow("Lena", lateNight, everyone),
                "and its regular still is, at the same hour — so it is the LINE that "
                + "changed and not the clock");
            Check(book.LinesFor("Sam").Count == 1,
                "you can ask what numbers somebody might be on");

            // A PUBLIC LINE IS ONE ANYBODY CAN USE, AND NOTHING READ THE FLAG.
            //
            // `Phone.Public` was set by `PhoneSetup` on three lines, saved and
            // restored, and consulted nowhere — so `LinesFor` matched regulars
            // only, the player is nobody's regular, and `ReachableNow("player")`
            // was false at every hour. `summonsTaken=0` in a hundred and
            // thirty-one runs is that field never being read.
            //
            // BOTH DIRECTIONS, and the second is the one that matters: a
            // stranger reaches the callbox and does NOT reach the private line
            // beside it, or "public" would mean nothing at all.
            var box = new PhoneBook();
            box.Add(new Phone { PlaceId = "hall", PlaceName = "the hall phone",
                                OpenFrom = 7, OpenTo = 22, Public = true });
            box.Add(new Phone { PlaceId = "office", PlaceName = "the office",
                                OpenFrom = 9, OpenTo = 17 });
            Check(box.LinesFor("a stranger").Count == 1
                  && box.LinesFor("a stranger")[0].PlaceId == "hall",
                "a stranger can use the hall phone and not the office line");
            Check(box.ReachableNow("a stranger", noon, everyone),
                "so somebody with no number of their own is still reachable at a callbox");
            Check(!box.ReachableNow("a stranger", new GameTime(3, 4, 0), everyone),
                "and not when the hall is shut, which is the hours still deciding");

            // FIDELITY is the price of reach, and it cuts both ways: a call
            // cannot read a face, so your lies land better AND so do theirs.
            Check(PhoneBook.Damped(0.4) < 0.4, "suspicion moves less on the line");
            Check(PhoneBook.Damped(0.4) > 0, "but it does move");
            // (audit 2026-07-27: the old check here compared Damped(1.0) to the
            // constant it multiplies by — true by construction. The real
            // property is that the SAME factor applies to a rise and a fall.)
            Check(Math.Abs(PhoneBook.Damped(0.4) + PhoneBook.Damped(-0.4)) < 1e-9,
                "a raise and a soothe are damped by the same factor on the line — neither direction is an upgrade");

            var snap = MiniJson.Serialize(book.Capture());
            var twin = new PhoneBook();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(snap)));
            Check(MiniJson.Serialize(twin.Capture()) == snap, "the exchange survives its own codec");
            Check(twin.AtPlace("bar") != null && twin.AtPlace("bar").Regulars.Count == 2,
                "including who is expected to be near which phone");
            twin.Restore(null);
            Check(twin.All.Count == 2, "restoring nothing changes nothing");
        }

        // ---------------------------------------------------------------
        // Act III — The Ledger Comes Due
        // ---------------------------------------------------------------

        static LedgerState Kingdom() => new LedgerState
        {
            BusinessesOwned = 2, RacketsEstablished = 2, CrewCount = 3,
            BestDayLifeLoyalty = 0.2, DayCircleRacketHeat = 0.8,
            TotalWashed = 900, TotalRacketIncome = 1000, TakingsToDate = 3000,
        };

        static void TestActThree()
        {
            Console.WriteLine("Act III — the ledger comes due:");

            // The act opens on state, never on a date.
            Check(!ActThreeState.ShouldOpen(false, true, 3, 3), "Act III waits for the Table to be answered");
            Check(ActThreeState.ShouldOpen(true, true, 0, 0),
                "then opens when Ellis can name the rackets");
            Check(ActThreeState.ShouldOpen(true, false, 2, 1),
                "or when the empire is too big for the bar to explain its own money");
            Check(!ActThreeState.ShouldOpen(true, false, 1, 1), "a small operation is still deniable");

            // THE LEDGER STRAIN, wrong in BOTH directions. This is the idea the
            // whole act rests on: laundering too little and laundering too much
            // are the same crime to a careful reader.
            var honest = new LedgerState { TotalRacketIncome = 0, TotalWashed = 0, TakingsToDate = 2000 };
            Check(ActThreeState.LedgerStrain(honest) < 0.05, "a bar that only ever sold drink has nothing to explain");

            var unwashed = new LedgerState { TotalRacketIncome = 1000, TotalWashed = 0, TakingsToDate = 2000 };
            Check(ActThreeState.LedgerStrain(unwashed) > 0.9,
                "night money with no laundering behind it has nowhere to have come from");

            var overwashed = new LedgerState { TotalRacketIncome = 1000, TotalWashed = 3000, TakingsToDate = 1000 };
            Check(ActThreeState.LedgerStrain(overwashed) > 0.9,
                "and a bar that washed more than it could ever have taken is telling a story nobody believes",
                ActThreeState.LedgerStrain(overwashed).ToString("0.00"));

            var careful = new LedgerState { TotalRacketIncome = 500, TotalWashed = 500, TakingsToDate = 4000 };
            Check(ActThreeState.LedgerStrain(careful) < 0.3, "careful laundering inside a real trade holds",
                ActThreeState.LedgerStrain(careful).ToString("0.00"));

            // Never a number to the player.
            for (double x = 0; x <= 1.0; x += 0.1)
            {
                var word = ActThreeState.StrainWord(x);
                Check(!string.IsNullOrEmpty(word) && !word.Contains("0."), "the books are described, never scored", word);
            }

            // THE ENDINGS ARE STATES, NOT A MENU.
            var kingdom = Kingdom();
            Check(ActThreeState.Resolve(kingdom) == Ending.Kingdom,
                "keep everything and lose everybody, and that is the Kingdom");

            var straight = Kingdom();
            straight.EmpireDissolved = true; straight.BestDayLifeLoyalty = 0.8;
            Check(ActThreeState.Resolve(straight) == Ending.StraightLife,
                "give up the business to keep the people, and that is the Straight Life");

            var burn = Kingdom();
            burn.EmpireDissolved = true; burn.BestDayLifeLoyalty = 0.1;
            Check(ActThreeState.Resolve(burn) == Ending.BurnBoth, "lose both and the ledger took it all");

            // Doing NOTHING must produce Burn Both — the ledger comes due whether
            // or not you answer it, and that has to be the default rather than a
            // special case somebody remembered to write.
            // The old fixture had TotalRacketIncome = 0 — the books had nothing
            // to explain, strain was zero, and Resolve returned Kingdom
            // deterministically; the BurnBoth arm was dead code and the comment
            // above was unpinned (audit 2026-07-27). Doing nothing for an act
            // means the rackets RAN and nobody managed anything.
            var did_nothing = new LedgerState
            {
                BusinessesOwned = 1, RacketsEstablished = 1,
                BestDayLifeLoyalty = 0.1, DayCircleRacketHeat = 0.9,
                TotalRacketIncome = 2500, TotalWashed = 0, TakingsToDate = 400,
            };
            Check(ActThreeState.Resolve(did_nothing) == Ending.BurnBoth,
                "doing nothing produces Burn Both, as the default and not a special case",
                ActThreeState.Resolve(did_nothing).ToString());

            // "Both" is the hard one and must require the information landscape
            // to have been actively managed — not merely a big empire and a friend.
            var both = Kingdom();
            both.BestDayLifeLoyalty = 0.8;
            both.DayCircleRacketHeat = 0.2;
            both.EllisCaseAnswerable = true;
            Check(ActThreeState.Resolve(both) == Ending.Both, "manage every mouth on the street and you keep both");

            var loud = Kingdom();
            loud.BestDayLifeLoyalty = 0.8; loud.DayCircleRacketHeat = 0.9; loud.EllisCaseAnswerable = true;
            Check(ActThreeState.Resolve(loud) != Ending.Both,
                "but not if the day circle holds the rackets as fact", ActThreeState.Resolve(loud).ToString());

            var unanswered = Kingdom();
            unanswered.BestDayLifeLoyalty = 0.8; unanswered.DayCircleRacketHeat = 0.2;
            unanswered.EllisCaseAnswerable = false;
            Check(ActThreeState.Resolve(unanswered) != Ending.Both,
                "and not with Ellis's case still standing", ActThreeState.Resolve(unanswered).ToString());

            // The Quiet Ending outranks everything, because it is the only one
            // you cannot arrive at by accident.
            var quiet = Kingdom();
            quiet.BestDayLifeLoyalty = 0.8; quiet.DayCircleRacketHeat = 0.2;
            quiet.EllisCaseAnswerable = true;
            quiet.HasReadySuccessor = true; quiet.HandedOver = true; quiet.SuccessorName = "Sam";
            Check(ActThreeState.Eligible(quiet).Contains(Ending.Both), "several endings can be live at once");
            Check(ActThreeState.Resolve(quiet) == Ending.Quiet, "and handing it over outranks keeping it");

            var wishful = Kingdom();
            wishful.HandedOver = true; wishful.HasReadySuccessor = false;
            Check(ActThreeState.Resolve(wishful) != Ending.Quiet,
                "you cannot hand it to somebody who could not hold it");

            Check(ActThreeState.Resolve(null) == Ending.BurnBoth, "and no world at all resolves safely");

            // Succession is a judgement of a PERSON.
            // The scope terms pinned exactly, both directions (audit 2026-07-27:
            // the stonewall term was pinned only from below; inflating it hid
            // behind the 1.6 clamp).
            Check(System.Math.Abs(ActThreeState.ScopeFactor(0, 1) - 1.15) < 1e-9,
                "one stonewall costs exactly its 0.15 — no more, no clamp to hide in",
                ActThreeState.ScopeFactor(0, 1).ToString("0.000"));
            Check(System.Math.Abs(ActThreeState.ScopeFactor(1, 0) - 0.955) < 1e-9,
                "and one cooperation buys exactly its 0.045",
                ActThreeState.ScopeFactor(1, 0).ToString("0.000"));

            Check(ActThreeState.CouldHold(0.8, 0.8, independent: true, feuding: false), "a good one can hold it");
            Check(!ActThreeState.CouldHold(0.8, 0.8, true, feuding: true), "not while feuding with the crew");
            Check(!ActThreeState.CouldHold(0.8, 0.8, independent: false, feuding: false),
                "not before they can stand on their own");
            Check(!ActThreeState.CouldHold(0.3, 0.9, true, false), "loyalty is not competence");
            // The thresholds bracketed tightly from both sides (audit
            // 2026-07-27: a large drift was invisible to the wide checks).
            Check(ActThreeState.CouldHold(0.55, 0.6, true, false) && !ActThreeState.CouldHold(0.54, 0.6, true, false),
                "the competence bar sits exactly at its documented line");
            Check(ActThreeState.CouldHold(0.55, 0.6, true, false) && !ActThreeState.CouldHold(0.55, 0.59, true, false),
                "and so does the loyalty bar");
            Check(!ActThreeState.CouldHold(0.9, 0.3, true, false), "and competence is not loyalty");

            // The authored text exists for every ending — an ending with no
            // words is an ending the player never sees.
            foreach (Ending e in Enum.GetValues(typeof(Ending)))
            {
                if (e == Ending.None) continue;
                var text = ActThreeState.EndingText(e, "Sam");
                Check(!string.IsNullOrEmpty(text) && text.Length > 80, $"{e} has something to say", e.ToString());
            }
            Check(ActThreeState.EndingText(Ending.Quiet, "Sam").Contains("Sam"),
                "and the quiet one names who you handed it to");

            // Lena's scene is gated entirely on the relationship, which is the
            // project's whole thesis stated as a mechanic.
            var cold = ActThreeState.Pp2LenaText(0.2, 0.8);
            var warm = ActThreeState.Pp2LenaText(0.9, 0.8);
            Check(cold != warm && warm.Length > cold.Length,
                "the most valuable information in the game is gated on a relationship");
            Check(!cold.Contains("kettle") && warm.Contains("kettle"), "and she only puts the kettle on for a friend");

            // Save-load.
            var act = new ActThreeState { Opened = true, OpenedDay = 20, AuditClosesDay = 26, Pp2Fired = true };
            act.Result = Ending.Quiet; act.SuccessorId = "Sam";
            act.InspectorAskedDay = 25;   // the daily ask must survive a save (audit 2026-07-27)
            var snap = MiniJson.Serialize(act.Capture());
            var twin = new ActThreeState();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(snap)));
            Check(MiniJson.Serialize(twin.Capture()) == snap, "Act III survives its own codec");
            Check(twin.Result == Ending.Quiet && twin.SuccessorId == "Sam", "including how it ended and who got it");
            Check(twin.InspectorAskedDay == 25,
                "the inspector's open question survives a save — his item is not destroyed by quitting");

            // A Fall inside the audit gives the grace days back: the letter
            // promised days, not calendar dates (audit 2026-07-27).
            Check(ActThreeState.ClosesDayAfterJump(closesDay: 15, lastSeenDay: 9, nowDay: 12) == 17,
                "a three-day fall inside the audit returns its two skipped days",
                ActThreeState.ClosesDayAfterJump(15, 9, 12).ToString());
            Check(ActThreeState.ClosesDayAfterJump(15, 11, 12) == 15,
                "and an ordinary morning extends nothing");
            twin.Restore(null);
            Check(twin.Opened, "restoring nothing changes nothing");

            // The three verbs are one-way, so their flags MUST survive a save —
            // a reload that quietly un-sells a business would hand the player a
            // different ending than the one they earned.
            var acted = new ActThreeState
            {
                Opened = true, AuditClosesDay = 30,
                SoldUp = true, Deflected = true,
                DeflectedOnto = "dockside", BurnedWitnessId = "Ada",
            };
            var twin2 = new ActThreeState();
            twin2.Restore(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(acted.Capture()))));
            Check(twin2.SoldUp && twin2.Deflected, "selling up and pointing it elsewhere survive a reload");
            Check(twin2.DeflectedOnto == "dockside" && twin2.BurnedWitnessId == "Ada",
                "and so does who you gave up, and who paid for it");

            // The epilogue is the only "after" this game has, and it reports the
            // world you handed over rather than how the handover felt.
            var handedHot = new LedgerState { DayCircleRacketHeat = 0.9, BestDayLifeLoyalty = 0.1 };
            var handedQuiet = new LedgerState { DayCircleRacketHeat = 0.1, BestDayLifeLoyalty = 0.9 };
            for (int i = 0; i < ActThreeState.EpilogueDays; i++)
            {
                var text = ActThreeState.EpilogueText(i, "Sam", handedQuiet);
                Check(!string.IsNullOrEmpty(text) && text.Length > 60, $"epilogue day {i} has words", i.ToString());
            }
            Check(ActThreeState.EpilogueText(1, "Sam", handedHot) != ActThreeState.EpilogueText(1, "Sam", handedQuiet),
                "a street you left loud is not a street you left quiet");
            Check(ActThreeState.EpilogueText(2, "Sam", handedHot) != ActThreeState.EpilogueText(2, "Sam", handedQuiet),
                "and a life you kept still writes to you");

            TestEveryInputIsRead();
            TestBooksMustHold();
            TestTheInspector();
            TestLastDay();
            TestDissolve();
        }

        /// THE GENERALISED VERSION OF TODAY'S BUG.
        ///
        /// `LedgerStrain` was computed, worded, displayed — and never read by
        /// the function that picks the ending. Every laundering decision across
        /// three acts was decorative, and no test caught it because each test
        /// varied the thing it was about and left the rest of the world alone.
        ///
        /// So: for every field of LedgerState, perturb THAT FIELD ALONE and
        /// require that it can change the answer. An input nobody reads is
        /// either a bug or a decision, and this forces it to be a decision —
        /// the exemptions below are listed with reasons rather than discovered
        /// six months later by somebody wondering why their number does nothing.
        static void TestEveryInputIsRead()
        {
            Console.WriteLine("Act III — every input to the ending is actually read:");

            // A world sitting near enough to several lines that a single nudge
            // in any direction can move it.
            LedgerState Base() => new LedgerState
            {
                BusinessesOwned = 1, RacketsEstablished = 1, CrewCount = 2,
                BestDayLifeLoyalty = 0.6, DayCircleRacketHeat = 0.3,
                EllisCaseAnswerable = false,
                TotalWashed = 900, TotalRacketIncome = 1000, TakingsToDate = 3000,
                HasReadySuccessor = true,
            };

            // `setup` puts the world where the field under test is the only
            // thing holding its condition up — otherwise a field can look dead
            // when it is merely redundant with another. Owning a shop and
            // running a round both keep the empire alive, so zeroing either one
            // alone proves nothing about whether it is read.
            void Reads(string field, Action<LedgerState> setup, params Action<LedgerState>[] nudges)
            {
                LedgerState Start() { var w = Base(); setup?.Invoke(w); return w; }
                var baseline = ActThreeState.Resolve(Start());
                bool moved = false;
                foreach (var nudge in nudges)
                {
                    var w = Start();
                    nudge(w);
                    if (ActThreeState.Resolve(w) != baseline) { moved = true; break; }
                }
                Check(moved, $"{field} can change the ending on its own", baseline.ToString());
            }

            Reads("BusinessesOwned", w => w.RacketsEstablished = 0, w => w.BusinessesOwned = 0);
            Reads("RacketsEstablished", w => w.BusinessesOwned = 0, w => w.RacketsEstablished = 0);
            Reads("EmpireDissolved", null, w => w.EmpireDissolved = true);
            // The life decides the ENDING where there is no empire to keep
            // (straight life against losing both), and decides what the ending
            // SAYS where there is — Kingdom covers "kept it, kept somebody" and
            // "kept it, kept nobody", which are not the same evening.
            Reads("BestDayLifeLoyalty", w => { w.BusinessesOwned = 0; w.RacketsEstablished = 0; },
                w => w.BestDayLifeLoyalty = 0.1);
            Check(ActThreeState.KingdomText(true) != ActThreeState.KingdomText(false),
                "and where it does not change the ending it changes what the ending says");
            Check(!ActThreeState.KingdomText(true).Contains("That is the whole of it"),
                "so nobody with a friend left is told they have nobody");
            // Heat only decides anything where Both is otherwise live — it is
            // one of the two halves of "the information landscape was managed",
            // and the other half is the deflection.
            Reads("DayCircleRacketHeat", w => w.EllisCaseAnswerable = true,
                w => w.DayCircleRacketHeat = 0.95);
            Reads("EllisCaseAnswerable", null, w => w.EllisCaseAnswerable = true);
            Reads("TotalWashed", null, w => w.TotalWashed = 0, w => w.TotalWashed = 9000);
            Reads("TotalRacketIncome", null, w => w.TotalRacketIncome = 9000);
            Reads("TakingsToDate", null, w => w.TakingsToDate = 1);
            Reads("HandedOver", null, w => w.HandedOver = true);
            // Only meaningful once you have actually signed: it is the check
            // that stops you handing it to somebody who could not hold it.
            Reads("HasReadySuccessor", w => w.HandedOver = true, w => w.HasReadySuccessor = false);
            // The three that only bite on books near the line — which is the
            // design: none of them is allowed to rescue a business that never
            // made sense, and none of them is meant to matter when it did. The
            // world-setup goes in `setup` so the nudge really is one field.
            Reads("Cooperations", w => w.TotalWashed = 200, w => w.Cooperations = 6);
            Reads("Stonewalls", w => w.TotalWashed = 450, w => w.Stonewalls = 4);
            Reads("LedgersMoved", w => w.TotalWashed = 300, w => w.LedgersMoved = true);
            // Prison does not launder the state's ledger (decided 2026-07-28,
            // by recommendation): the same books read HARDER with a conviction
            // on file — and the term is modest, not fatal.
            {
                var noRecord = new LedgerState { TotalRacketIncome = 2000, TotalWashed = 200, TakingsToDate = 400 };
                var record = new LedgerState { TotalRacketIncome = 2000, TotalWashed = 200, TakingsToDate = 400, PublicRecord = true };
                Check(ActThreeState.SeenStrain(record) > ActThreeState.SeenStrain(noRecord) + 1e-9,
                    "a conviction on file makes the same books read harder",
                    $"{ActThreeState.SeenStrain(record):0.000} vs {ActThreeState.SeenStrain(noRecord):0.000}");
                Check(ActThreeState.SeenStrain(record) < ActThreeState.SeenStrain(noRecord) * 1.2,
                    "but it reads as a record, not a verdict — modest, by design");
            }
            // "The single largest movement any one action makes" is a design
            // claim, and it is now an assertion: moving the books must beat the
            // deflection's easing, and by a real margin (audit 2026-07-27: the
            // 0.55 was pinned only from above).
            {
                var baseline = new LedgerState { TotalRacketIncome = 2000, TotalWashed = 200, TakingsToDate = 400 };
                var moved = new LedgerState { TotalRacketIncome = 2000, TotalWashed = 200, TakingsToDate = 400, LedgersMoved = true };
                var pointed = new LedgerState { TotalRacketIncome = 2000, TotalWashed = 200, TakingsToDate = 400, EllisCaseAnswerable = true };
                double easeMoved = ActThreeState.SeenStrain(baseline) - ActThreeState.SeenStrain(moved);
                double easePointed = ActThreeState.SeenStrain(baseline) - ActThreeState.SeenStrain(pointed);
                Check(easeMoved > easePointed + 1e-9,
                    "moving the books eases more than pointing the case away — the largest single movement, as designed",
                    $"{easeMoved:0.000} vs {easePointed:0.000}");
            }

            // The two that deliberately do NOT decide, named so that being
            // unread is a choice rather than an oversight:
            //
            //   CrewCount      — how MANY people you have never decided which
            //                    life you keep. Whether one of them could hold
            //                    it does, and that is HasReadySuccessor.
            //   DayLifeDeparted— the ending asks whether anybody still counts
            //                    you, not how many walked. Best-not-average is
            //                    the whole point: one friend IS a life kept.
            //
            // Both are carried for the ledger screen and the epilogue's wording.
            // If either ever needs to decide something, delete it from here and
            // this test will start demanding it.
            foreach (var (name, nudge) in new (string, Action<LedgerState>)[]
                { ("CrewCount", w => w.CrewCount = 40), ("DayLifeDeparted", w => w.DayLifeDeparted = 40) })
            {
                var w2 = Base();
                nudge(w2);
                Check(ActThreeState.Resolve(w2) == ActThreeState.Resolve(Base()),
                    $"{name} is deliberately not a deciding input", name);
            }
        }

        /// THE HOLE THIS CLOSES. Strain was computed, worded, and shown — and
        /// never read by the thing that decides the ending. Three acts of
        /// laundering decisions were decorative, and an audit resolved without
        /// consulting the document it came to read.
        static void TestBooksMustHold()
        {
            // A player who did everything else right: big empire, a friend who
            // still counts them, the street quiet, Ellis answered — and books
            // that describe a business which does not exist.
            LedgerState Ruinous()
            {
                var s = Kingdom();
                s.BestDayLifeLoyalty = 0.8;
                s.DayCircleRacketHeat = 0.2;
                s.EllisCaseAnswerable = true;
                s.TotalWashed = 0;            // every coin of racket income unexplained
                s.TotalRacketIncome = 4000;
                return s;
            }
            var ruined = Ruinous();
            Check(ActThreeState.LedgerStrain(ruined) > 0.9, "unwashed racket income is ruinous on its face",
                ActThreeState.LedgerStrain(ruined).ToString("0.00"));
            Check(ActThreeState.Resolve(ruined) != Ending.Both,
                "managing every mouth on the street does not save books that cannot be read",
                ActThreeState.Resolve(ruined).ToString());

            // MITIGATION SAVES YOU; IT DOES NOT BUY YOU THE BEST ENDING.
            // With both reliefs stacked — the case pointed elsewhere, the scope
            // narrowed — ruinous books drop under the threshold and used to
            // qualify for Both. The lab measured it at fifty-one runs in a
            // hundred on an aggressive campaign, against a design that calls
            // Both "rare, and earned rather than lucky" and a player decision
            // that it should not be reachable on a first playthrough.
            var mitigated = Ruinous();
            mitigated.Cooperations = 5;
            mitigated.EllisCaseAnswerable = true;
            Check(ActThreeState.SeenStrain(mitigated) < LedgerState.BooksHoldThreshold,
                "handling it well does save ruinous books from being read",
                ActThreeState.SeenStrain(mitigated).ToString("0.00"));
            Check(ActThreeState.Resolve(mitigated) != Ending.BurnBoth,
                "so you do not lose everything");
            Check(ActThreeState.Resolve(mitigated) != Ending.Both,
                "but you do not get to keep both lives on books that never made sense",
                ActThreeState.Resolve(mitigated).ToString());

            // The same world with the washing actually done keeps everything.
            var washed = Ruinous();
            washed.TotalWashed = 3800; washed.TakingsToDate = 14000;
            Check(ActThreeState.SeenStrain(washed) < LedgerState.BooksHoldThreshold,
                "and the same world with the washing done reads as a bar",
                ActThreeState.SeenStrain(washed).ToString("0.00"));
            Check(ActThreeState.Resolve(washed) == Ending.Both, "which is what keeps both");

            // Keeping the empire alone is gated the same way: the audit takes
            // the business whether or not anybody still likes you.
            var coldAndRuined = Ruinous();
            coldAndRuined.BestDayLifeLoyalty = 0.1;
            Check(ActThreeState.Resolve(coldAndRuined) == Ending.BurnBoth,
                "and a kingdom with unreadable books is not a kingdom",
                ActThreeState.Resolve(coldAndRuined).ToString());

            // Two deliberate exemptions, both of which are the price of a door.
            var soldUp = Ruinous();
            soldUp.EmpireDissolved = true;
            Check(ActThreeState.Resolve(soldUp) == Ending.StraightLife,
                "selling up outruns the books, because there is nothing left to be in them");

            // THE HOLE THE BALANCE LAB FOUND. StraightLife used to require
            // EmpireDissolved, which meant a player who never built an empire
            // could not reach it — you cannot sell what you never bought — and
            // had exactly one ending available: "you lose the business and you
            // lose the people", having neither. The lab's do-nothing plan ended
            // that way a hundred times out of a hundred.
            var neverBuilt = new LedgerState
            {
                BusinessesOwned = 0, RacketsEstablished = 0, CrewCount = 0,
                EmpireDissolved = false,          // never dissolved, because never built
                BestDayLifeLoyalty = 0.7,
                TotalWashed = 1800, TotalRacketIncome = 0, TakingsToDate = 3099,
            };
            Check(ActThreeState.LedgerStrain(neverBuilt) > LedgerState.BooksHoldThreshold,
                "an honest player's books can still read badly (see decisions-pending #10)",
                ActThreeState.LedgerStrain(neverBuilt).ToString("0.00"));
            Check(ActThreeState.Resolve(neverBuilt) == Ending.StraightLife,
                "but never building it is a way of keeping your life, and it gets the same door");

            // And it is still gated on the life: nothing built and nobody left
            // is not the straight life, it is just nothing.
            var neitherOne = new LedgerState { BestDayLifeLoyalty = 0.1 };
            Check(ActThreeState.Resolve(neitherOne) == Ending.BurnBoth,
                "nothing built and nobody left is not a quiet ending, it is an empty one");

            // The two roads into the straight life do not read the same.
            Check(ActThreeState.StraightLifeText(true) != ActThreeState.StraightLifeText(false),
                "and a man who gave it up is not a man who never started");
            Check(ActThreeState.StraightLifeText(false).Contains("never put"),
                "with the harder game getting its own paragraph");

            var handed = Ruinous();
            handed.HandedOver = true; handed.HasReadySuccessor = true; handed.SuccessorName = "Sam";
            Check(ActThreeState.Resolve(handed) == Ending.Quiet,
                "and handing it over outruns them too — it lands on whoever signed");
        }

        /// The inspector: not buyable, and therefore the only thing about him
        /// that can move is how much he reads.
        static void TestTheInspector()
        {
            Check(ActThreeState.ScopeFactor(0, 0) == 1.0, "an inspection nobody has handled is an ordinary one");
            Check(ActThreeState.ScopeFactor(4, 0) < 1.0 && ActThreeState.ScopeFactor(4, 0) > 0.75,
                "producing what is asked for narrows it, and only somewhat (decision 10)",
                ActThreeState.ScopeFactor(4, 0).ToString("0.00"));
            // The asymmetry is deliberate: being difficult with a revenue man
            // was never meant to be a strategy, and it is far easier to make
            // somebody look harder than to make them look away.
            Check(1.0 - ActThreeState.ScopeFactor(3, 0) < ActThreeState.ScopeFactor(0, 3) - 1.0,
                "and being difficult moves him further than cooperating does",
                $"{ActThreeState.ScopeFactor(3, 0):0.00} vs {ActThreeState.ScopeFactor(0, 3):0.00}");
            Check(ActThreeState.ScopeFactor(0, 3) > 1.35, "and being difficult widens it",
                ActThreeState.ScopeFactor(0, 3).ToString("0.00"));
            Check(ActThreeState.ScopeFactor(99, 0) >= 0.55 && ActThreeState.ScopeFactor(0, 99) <= 1.6,
                "and neither runs away with it — cooperation is not a cheat code");

            // THE PROPERTY THAT MAKES THE VERB WORTH HAVING: on books that sit
            // near the line, how the man was handled decides the ENDING. Not by
            // money, not by leverage — by having answered him for six mornings.
            //
            // Built as a Kingdom candidate (empire intact, nobody left who knew
            // you before it) so that the books are genuinely the only thing left
            // deciding it, and the flip is visible rather than implied.
            LedgerState Marginal(int coop, int stone)
            {
                var s = Kingdom();
                s.BestDayLifeLoyalty = 0.2;      // the life is already gone
                s.DayCircleRacketHeat = 0.8;
                s.EllisCaseAnswerable = false;   // no deflection easing it
                s.TotalWashed = 1000; s.TotalRacketIncome = 3000; s.TakingsToDate = 9000;
                s.Cooperations = coop; s.Stonewalls = stone;
                return s;
            }
            Check(ActThreeState.Resolve(Marginal(0, 0)) == Ending.BurnBoth,
                "the same world, unhandled, loses everything");
            Check(ActThreeState.Resolve(Marginal(5, 0)) == Ending.Kingdom,
                "and handled, keeps the kingdom — six mornings of paperwork is the whole difference");
            Check(ActThreeState.Resolve(Marginal(0, 2)) == Ending.BurnBoth,
                "being difficult with him never helps");
            double bare = ActThreeState.SeenStrain(Marginal(0, 0));
            Check(bare > LedgerState.BooksHoldThreshold,
                "books a third washed do not survive an ordinary reading", bare.ToString("0.00"));
            Check(ActThreeState.SeenStrain(Marginal(5, 0)) < LedgerState.BooksHoldThreshold,
                "the same books survive a narrow one",
                ActThreeState.SeenStrain(Marginal(5, 0)).ToString("0.00"));
            Check(ActThreeState.SeenStrain(Marginal(0, 2)) > bare, "and are worse under a wide one");

            // Pointing the case elsewhere also eases what gets read — they do
            // not look as hard at a business they have stopped suspecting.
            var deflected = Marginal(0, 0);
            deflected.EllisCaseAnswerable = true;
            Check(ActThreeState.SeenStrain(deflected) < bare,
                "and a case pointed elsewhere is a case read less carefully");

            // The words never become numbers, at either end.
            foreach (var f in new[] { 0.55, 0.7, 1.0, 1.2, 1.6 })
            {
                var word = ActThreeState.ScopeWord(f);
                Check(!string.IsNullOrEmpty(word) && !word.Any(char.IsDigit),
                    $"scope at {f} is said as a circumstance", word);
            }

            // He survives a reload with his count intact — a saved game that
            // forgot six mornings of cooperation would hand back a different
            // ending than the one that was earned.
            var act = new ActThreeState
            {
                Opened = true, InspectorArrived = true,
                Cooperations = 4, Stonewalls = 1, LastDealtDay = 22,
            };
            var twin = new ActThreeState();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(act.Capture()))));
            Check(twin.InspectorArrived && twin.Cooperations == 4 && twin.Stonewalls == 1
                  && twin.LastDealtDay == 22, "and every morning you answered him survives a reload");
        }

        /// PP5. The line "you can reach a few people, and reaching one is not
        /// reaching another" was written before there was anything to reach
        /// them ABOUT. These are the rules that make it true.
        static void TestLastDay()
        {
            var act = new ActThreeState { Opened = true, AuditClosesDay = 30 };
            Check(!act.IsLastDay(28), "the last day is not the whole week");
            Check(act.IsLastDay(29) && act.IsLastDay(30), "it is the eve and the day itself");
            act.AuditClosed = true;
            Check(!act.IsLastDay(30), "and it is over once the books are open");

            var live = new ActThreeState { Opened = true, AuditClosesDay = 30 };
            Check(live.LastDayLeft == ActThreeState.LastDayBudget, "two calls, to start with");
            live.LastDayActions = 1;
            Check(live.LastDayLeft == 1, "one spent is one left");
            live.LastDayActions = 9;
            Check(live.LastDayLeft == 0, "and it never goes negative, however hard anybody tries");

            // Moving the books is the largest single movement in the act, and
            // it is gated on a relationship rather than on money — which is the
            // same rule Lena's PP2 scene runs on, applied to the last day.
            Check(!ActThreeState.WillMoveTheLedgers(0.5), "she will not commit a felony for an employer");
            Check(ActThreeState.WillMoveTheLedgers(0.8), "she will for somebody she decided about long ago");
            Check(ActThreeState.LastDayLenaText(true) != ActThreeState.LastDayLenaText(false),
                "and the refusal is its own scene rather than a failure message");
            Check(ActThreeState.LastDayLenaText(false).Contains("daughter"),
                "with a reason that belongs to her rather than to you");

            LedgerState Books(bool moved)
            {
                var s = Kingdom();
                s.TotalWashed = 1000; s.TotalRacketIncome = 3000; s.TakingsToDate = 9000;
                s.LedgersMoved = moved;
                return s;
            }
            double kept = ActThreeState.SeenStrain(Books(false));
            double gone = ActThreeState.SeenStrain(Books(true));
            Check(gone < kept, "what is not in the cellar cannot be read out of it",
                $"{kept:0.00} -> {gone:0.00}");
            Check(kept > LedgerState.BooksHoldThreshold && gone < LedgerState.BooksHoldThreshold,
                "and on books at the line it is the difference between keeping it and not");

            // It survives a reload, like every other one-way thing in the act.
            var spent = new ActThreeState
            {
                Opened = true, AuditClosesDay = 30, LastDayActions = 2, LedgersMoved = true,
            };
            var twin = new ActThreeState();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(MiniJson.Serialize(spent.Capture()))));
            Check(twin.LastDayActions == 2 && twin.LedgersMoved,
                "and the last day cannot be replayed by reloading");

            // The authored text names the person rather than a role, because a
            // last call is to somebody.
            Check(ActThreeState.LastDayCrewText("Sam").Contains("Sam")
                  && ActThreeState.LastDayTruthText("Ada").Contains("Ada"),
                "and every last-day line is addressed to a name");
        }

        /// Selling up: the straight life's price, paid in the thing you built.
        static void TestDissolve()
        {
            var mill = new GossipMill(new SocialGraph());
            var wallet = new Wallet(0);
            var now = new GameTime(20, 10, 0);
            var e = new EmpireBook();
            e.Businesses.Add(new Business
            {
                Id = "shop", Name = "shop", OwnerId = "Rita", AskPrice = 400,
                CleanIncomePerDay = 20, LaunderPerDay = 60, Owned = true, AcquiredVia = "clean",
            });
            e.Rackets.Add(new Racket { Id = "collection", Name = "rounds", Established = true, RunnerId = "Sam" });
            e.Crew.Add(new CrewMember { Id = "Sam", Name = "Sam", Assignment = "collection", Cut = "skim" });
            e.Crew.Add(new CrewMember { Id = "Rocco", Name = "Rocco", Cut = "generous" });
            foreach (var id in new[] { "Rita", "Sam", "Rocco" })
                mill.Add(new Gossiper(id, id, new MemoryStore(id), new KnowledgeBase(), new SuspicionTracker())
                    { Loyalty = 0.6 });

            int raised = e.Dissolve(wallet, mill, now);
            Check(raised == 200, "everything goes at about half what it cost", raised.ToString());
            Check(wallet.Clean == 200, "and it lands as clean money, which is the whole point of taking the loss");
            Check(!e.Businesses[0].Owned && e.Businesses[0].AcquiredVia == null, "the shop is theirs again");
            Check(!e.Rackets[0].Established && e.Rackets[0].RunnerId == null, "the rounds stop");
            Check(e.Crew.TrueForAll(c => c.Departed && c.Assignment == null), "and everybody is paid off");
            Check(e.OwnedLaunderCapacity == 0, "the washing capacity goes with the fronts");

            // How they take it depends on what they were getting, which is the
            // §6.5 rule holding right up to the last day.
            Check(mill.Get("Rocco").Loyalty > mill.Get("Sam").Loyalty,
                "a fair cut is remembered kindly even when the job ends");
            Check(mill.Get("Rita").Memory.Events.Count > 0, "and the seller remembers who sold back at a loss");
        }

        // ---------------------------------------------------------------
        // Who the player is, and what the street calls them
        // ---------------------------------------------------------------

        static void TestIdentity()
        {
            Console.WriteLine("Identity — the street learns your name:");
            var me = new PlayerIdentity();
            Check(me.Full == "Tom Nowak", "the protagonist has a name at last (Nowak since the names ruling of 24 September)", me.Full);
            Check(me.BenefactorFirst == "Mickey", "and the uncle who left him the bar is still Mickey");

            // THE DESIGN DECISION. "The new owner" was never a placeholder — it
            // is what people call you before they know you, and this is a game
            // about being known. So it survives, as the bottom of a gradient.
            Check(me.AddressBy(knowsName: false, closeness: 1.0) == "the new owner",
                "somebody who has not placed you calls you the new owner, however much they like you");
            Check(me.AddressBy(true, 0.1) == "Nowak", "once they know you, you are a fact on this street");
            Check(me.AddressBy(true, 0.5) == "Tom", "people who decided about you use your name");
            Check(me.AddressBy(true, 0.9) == "Tommy", "and two or three people, ever, use the short one");

            // The gate is knowing, not liking — someone can think well of you
            // and still not know what to call you.
            Check(me.AddressBy(false, 0.9) != me.AddressBy(true, 0.9),
                "closeness cannot promote a stranger");

            // Talk travels further than acquaintance: a rumor can carry your
            // surname into mouths that never met you.
            Check(me.InTalk(true) == "Nowak" && me.InTalk(false) == "the new owner",
                "a name gets around a district ahead of the person");

            // From a real person.
            var mill = new GossipMill(new SocialGraph());
            var stranger = new Gossiper("s", "Stranger", null, null, null, "day", 0.5, 0.5, 0.9);
            Check(!PlayerIdentity.KnowsName(stranger), "somebody who has never noticed you does not know your name");
            Check(me.AddressBy(stranger) == "the new owner", "and calls you what the street calls you");
            stranger.Memory.Append(new MemoryEvent(new GameTime(1, 9, 0), "conversation", 0.5,
                "Talked to the one who took over Mickey's place."));
            Check(PlayerIdentity.KnowsName(stranger), "one memory of you is enough to learn it");
            Check(me.AddressBy(stranger) == "Tommy", "and a friend uses the short one", me.AddressBy(stranger));
            Check(me.AddressBy((Gossiper)null) == "the new owner", "asking about nobody is safe");
            // WHERE THEY ARE, in plain words (town list 6u): every place of the named
            // cast has words a person there would use, and the routine gives them.
            {
                var hook = CastDay.Parse(File.ReadAllText(Root("production/specs/hook-cast.json")));
                var wordless = new List<string>();
                foreach (var pl in hook.Places) if (hook.SaidOf(pl) == null || System.Text.RegularExpressions.Regex.IsMatch(hook.SaidOf(pl), @"decal|_|\d")) wordless.Add(pl);
                string anyWhere = null;
                foreach (var person in hook.People)
                    for (int hh = 0; hh < 24 && anyWhere == null; hh++)
                        if (hook.Where(person, 1, hh) != null) anyWhere = hook.WhereWords(person, 1, hh);
                Check(wordless.Count == 0 && anyWhere != null && hook.SaidOf("off") == null && hook.SaidOf(null) == null,
                      "every place a person can be has plain words for it, none of them an asset name", string.Join(",", wordless));
            }
            // WHERE HE SAYS HE WAS (town list 6ac): places grouped by area as people
            // say them, and read only from plain statements, never so a true answer
            // is a lie (the independent check's cases, each a regression here).
            {
                var hookA = CastDay.Parse(File.ReadAllText(Root("production/specs/hook-cast.json")));
                var noArea = new List<string>();
                foreach (var pl in hookA.Places) if (hookA.AreaOf(pl) == null) noArea.Add(pl);
                var spoken = hookA.SpokenAreas();
                string Says(string line) { var set = new List<string>(Claims.WhereHeSays(line, spoken)); set.Sort(StringComparer.Ordinal); return string.Join(",", set); }
                var cases = new (string line, string areas)[]
                {
                    ("I was at the chapel all night.", "chapel"),
                    ("I was at the fish market this morning, prices are mad.", ""),
                    ("Who says I was at Rita's? I was at the chapel.", "chapel"),
                    ("If I was at Rita's you'd have seen me.", ""),
                    ("I was at the chapel, then Rita's.", "chapel,ritas"),
                    ("I was at the market, the fish market I mean.", "fish_dock,fish_market,market"),
                    ("I wasn't at Rita's.", ""),
                    ("I was at Rita\u2019s.", "ritas"),
                    ("I was at the cafeteria.", ""),
                    ("Were you at the chapel?", ""),
                    ("He was at the chapel.", ""),
                    ("I was at the harbour office.", "harbour_office"),
                };
                string wrong = null;
                foreach (var (line, want) in cases) if (Says(line) != want) wrong = line + " -> " + Says(line) + " (want " + want + ")";
                Check(noArea.Count == 0 && hookA.AreaOf("fish_front") == "fish_market" && spoken["fish market"].SetEquals(new[] { "fish_market", "fish_dock" })
                      && spoken["docks"].IsSupersetOf(new[] { "docks", "fish_dock", "customs", "repair_yard", "harbour_office" }),
                      "every place has an area; a name can mean more than one, and the docks cover what is on them", string.Join(",", noArea));
                Check(wrong == null, "where he says he was: plain statements only, every place named, never another time, a question, a supposition or somebody else", wrong ?? "");
                // THE SECOND PASS: punctuation never hides a place; a place the list does
                // not know beside one it does, a clock time, another day: never definite.
                string SaysD(string line) { var set = new List<string>(Claims.WhereHeSays(line, spoken, new Claims.DeedWhen(1, 23, 2), false, out bool def)); set.Sort(StringComparer.Ordinal); return string.Join(",", set) + (def ? " definite" : ""); }
                var cases2 = new (string line, string want)[]
                {
                    ("I was at the chapel all night.", "chapel definite"),
                    ("I was at \"the chapel\".", "chapel definite"),
                    ("I was at the chapel; then Rita's.", "chapel,ritas"),
                    ("I was at the chapel\u2014then Rita's.", "chapel,ritas"),
                    ("I was at the chapel: Rita's was shut.", "chapel,ritas"),
                    ("I was at the pawn, then walked past the chapel.", "chapel,ritas"),
                    ("I was at home, not at Rita's.", "ritas"),
                    ("I was in the yard all night, then the cafe.", "cafe"),
                    ("I was at the cafe at six.", ""),
                    ("I was at the cafe till ten, then home.", "cafe"),
                    ("I was at the cafe till four, then home.", ""),
                    ("I was at the cafe on Monday.", ""),
                    ("I was at the cafe on Tuesday night.", "cafe definite"),
                    ("I was at the chapel. Then Rita's.", "chapel"),
                    ("I was at the chapel! Went on to Rita's after.", "chapel"),
                    ("I was at the market all night.", "fish_market,market definite"),
                    ("After the chapel I was at Rita's.", "chapel,ritas"),
                    ("Left the cafe and I was at Rita's all night.", "cafe,ritas"),
                    ("Past the kiosk, I was at the chapel.", "chapel,kiosk"),
                    ("Me? I was at the chapel all night.", "chapel definite"),
                    ("No. I was at the chapel.", "chapel definite"),
                    ("I was at the chapel around eleven.", "chapel"),
                    ("I was at the chapel last night.", "chapel definite"),
                    ("I was at the chapel on Tuesday night.", "chapel definite"),
                    ("I was at the chapel yesterday.", "chapel"),
                };
                string wrong2 = null;
                foreach (var (line, want) in cases2) if (SaysD(line) != want) wrong2 = line + " -> " + SaysD(line) + " (want " + want + ")";
                var tueNight = new Claims.DeedWhen(1, 23, 2);
                var bare = Claims.WhereHeSays("At the chapel, all night.", spoken, tueNight, true, out bool bareDef);
                var bareNot = Claims.WhereHeSays("At the chapel, all night.", spoken, tueNight, false, out _);
                var bareRank = Claims.WhereHeSays("The rank was empty when I left.", spoken, tueNight, true, out _);
                Check(bare.SetEquals(new[] { "chapel" }) && bareDef && bareNot.Count == 0 && bareRank.Count == 0,
                      "a bare \"At the chapel, all night.\" is his answer when he is answering their question, and only then; \"The rank was empty when I left\" is no answer");
                var times = new (string line, Claims.DeedWhen deed, bool other)[]
                {
                    ("Where were you around eleven, when the window went?", tueNight, false),
                    ("Where were you at half ten?", tueNight, false),
                    ("Where were you at 11pm?", tueNight, false),
                    ("Where were you at 22:30?", tueNight, false),
                    ("Where were you at midnight?", tueNight, false),
                    ("No one saw you. Where were you?", tueNight, false),
                    ("Where were you last night?", tueNight, false),
                    ("Where were you at three?", tueNight, true),
                    ("Where were you at 3?", tueNight, true),
                    ("Where were you last night?", new Claims.DeedWhen(0, 23, 2), true),
                    ("Where were you this afternoon?", new Claims.DeedWhen(2, 14, 2), false),
                    ("Where were you this afternoon?", tueNight, true),
                    ("Where were you at lunchtime?", new Claims.DeedWhen(2, 13, 2), false),
                    ("Where were you at lunchtime?", tueNight, true),
                    ("Where were you on Tuesday night?", tueNight, false),
                    ("Where were you on Monday?", tueNight, true),
                    ("Where were you at eleven?", default, true),
                    ("Where were you at 11am?", tueNight, true),
                    ("Where were you at eleven in the morning?", tueNight, true),
                    ("Where were you at eleven at night?", tueNight, false),
                    ("Where were you at 11?", tueNight, false),
                    ("Where were you on Tuesday afternoon?", tueNight, true),
                    ("Where were you on Tuesday morning?", tueNight, true),
                    ("Where were you on Tuesday night?", new Claims.DeedWhen(1, 14, 2), true),
                    ("Where were you on Tuesday afternoon?", new Claims.DeedWhen(1, 14, 2), false),
                    ("Where were you on Wednesday morning?", new Claims.DeedWhen(2, 2, 2), false),
                    ("Where were you on Tuesday night?", new Claims.DeedWhen(2, 2, 2), false),
                    ("Where were you on Wednesday night?", new Claims.DeedWhen(2, 2, 2), true),
                    ("Where were you Tuesday night, or was it Tuesday morning?", tueNight, true),
                };
                string wrongTime = null;
                foreach (var (line, deed, other) in times) if (Claims.NamesAnotherTime(line, deed) != other) wrongTime = line;
                if (Claims.WhereHeSays("I was at the chapel on Tuesday night.", spoken, new Claims.DeedWhen(1, 14, 2), false, out _).Count != 0)
                    wrongTime = "his Tuesday night answer, for a deed on Tuesday afternoon";
                Check(wrongTime == null, "a time is the deed's when it is within an hour of it, on its day or its part of the day; with no deed, every time is another", wrongTime ?? "");
                var looseCases = new (string line, bool loose)[]
                {
                    ("Where were you yesterday?", true),
                    ("What were you doing after work?", true),
                    ("Where were you on Tuesday?", true),
                    ("Where were you on Tuesday night?", false),
                    ("Where were you last night?", false),
                    ("Where were you around eleven?", false),
                    ("Where were you yesterday, around eleven?", false),
                    ("Where were you, then?", false),
                };
                string wrongLoose = null;
                foreach (var (line, loose) in looseCases) if (Claims.LooseTime(line, tueNight) != loose) wrongLoose = line;
                Check(wrongLoose == null, "a question about a whole day, or part of one with no day, is too loose to judge a plain answer by", wrongLoose ?? "");
                Check(wrong2 == null && hookA.Fits("fish_dock", "docks") && hookA.Fits("docks", "fish_dock") && !hookA.Fits("chapel", "ritas")
                      && hookA.AreaFor("ritas_counter") == "ritas" && hookA.AreaFor("ritas") == "ritas" && hookA.AreaFor("quay_street") == null && hookA.AreaFor("off") == null,
                      "only a plain answer naming one place is definite; a place on the docks fits the docks; a sighting must be a known place", wrong2 ?? "");
            }
            {
                var asks = new ConversationEngine(new FakeLlm { NextReply = "Where were you this morning, then?" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                asks.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                var asksYa = new ConversationEngine(new FakeLlm { NextReply = "Where were ya, then?" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                asksYa.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                var knows = new ConversationEngine(new FakeLlm { NextReply = "I know where you were." }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                knows.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                var asksSix = new ConversationEngine(new FakeLlm { NextReply = "Where were you at six, then?" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                asksSix.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                var asksTue = new ConversationEngine(new FakeLlm { NextReply = "Where were you on Tuesday night?" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                asksTue.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                var asksAfter = new ConversationEngine(new FakeLlm { NextReply = "I saw you this morning. Where were you that night?" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                asksAfter.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                var asksDay = new ConversationEngine(new FakeLlm { NextReply = "Where were you yesterday?" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                asksDay.SayToAsync("Morning.", new GameTime(2, 10, 0), "").GetAwaiter().GetResult();
                Check(asksAfter.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2), out bool looseAfter) && looseAfter
                      && asksDay.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2), out bool looseDay) && looseDay
                      && asksTue.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2), out bool looseTue) && !looseTue,
                      "their question is read from the sentence that asks it; another time elsewhere in their reply, or a whole day, makes it loose");
                Check(!asksSix.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2)) && asksTue.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2)) && !asksTue.AskedWhereAbout(new Claims.DeedWhen(0, 23, 2)),
                      "their question at another hour or on another day is not about the deed; on the deed's own day it is");
                Check(!asks.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2)) && asksYa.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2)) && !knows.AskedWhereAbout(new Claims.DeedWhen(1, 23, 2)),
                      "asking where he was this morning is not asking about the deed; \"where were ya\" is asking; \"I know where you were\" is not");
            }
            // THE STREET JUST AFTER A DEED (town list 6an): a reaction first, then
            // the street settling, then everyday talk; nothing changes without a
            // deed; every line within canon's content rule; the shared replies fit
            // every kind of noise.
            {
                var ja = new Gossiper("ja", "ja", new MemoryStore("ja"), new KnowledgeBase(), new SuspicionTracker());
                var jb = new Gossiper("jb", "jb", new MemoryStore("jb"), new KnowledgeBase(), new SuspicionTracker());
                var jnow = new GameTime(1, 10, 0);
                string wrongJ = null;
                for (int seed = 0; seed < 40; seed++)
                {
                    var plain = StreetVoice.Ambient(ja, jb, jnow, 0.5, 1.0, false, false, seed);
                    var none = StreetVoice.Ambient(ja, jb, jnow, 0.5, 1.0, false, false, seed, null, null, -1);
                    var gone = StreetVoice.Ambient(ja, jb, jnow, 0.5, 1.0, false, false, seed, null, "glass", StreetVoice.SettlingSeconds);
                    if (plain[0].Text != none[0].Text || plain[1].Text != none[1].Text || plain[0].Text != gone[0].Text) wrongJ = "without a deed, or after it, the talk changed: seed " + seed;
                    foreach (var kind in new[] { "glass", "shout", "crash", "bang" })
                    {
                        var fresh = StreetVoice.Ambient(ja, jb, jnow, 0.5, 1.0, false, false, seed, null, kind, 0.0);
                        var late = StreetVoice.Ambient(ja, jb, jnow, 0.5, 1.0, false, false, seed, null, kind, StreetVoice.JustNowSeconds - 0.1);
                        var settle = StreetVoice.Ambient(ja, jb, jnow, 0.5, 1.0, false, false, seed, null, kind, StreetVoice.JustNowSeconds);
                        string want = kind == "bang" ? "noise" : kind;
                        if (fresh[0].Bank != "ambient/open/justnow/" + want || late[0].Bank != fresh[0].Bank || fresh[1].Bank != "ambient/reply/justnow"
                            || settle[0].Bank != "ambient/open/settling" || settle[1].Bank != "ambient/reply/settling") wrongJ = "banks wrong for " + kind + " seed " + seed;
                        foreach (var l in new[] { fresh[0], fresh[1], settle[0], settle[1] })
                        {
                            if (ContentRule.SpeechBreaks(l.Text) != null) wrongJ = "content rule: " + l.Text;
                            if (l.AboutPlayer) wrongJ = "about the player: " + l.Text;
                        }
                        foreach (var l in new[] { fresh[1], settle[0], settle[1] })
                            if (System.Text.RegularExpressions.Regex.IsMatch(l.Text, @"\b(glass|window|shout|bang|crash)", System.Text.RegularExpressions.RegexOptions.IgnoreCase)) wrongJ = "a shared line names one kind: " + l.Text;
                    }
                }
                Check(wrongJ == null && StreetVoice.JustNowSpeakAfterSeconds < StreetVoice.ClearWordsEverySeconds,
                      "after a deed: a reaction for ninety seconds, the street settling for ninety more, then everyday talk; unchanged without one; within the content rule; shared lines fit every noise", wrongJ ?? "");
            }

            // A STAGE DIRECTION SAID IN THE FIRST PERSON (town list 6aj): taken out,
            // the speech kept; talk that only sounds like one kept whole.
            {
                var gestureCases = new (string reply, string want)[]
                {
                    ("I look at you steady. What do you want?", "What do you want?"),
                    ("I look up from the rank, squinting at you through the drizzle. Rain's coming on.", "Rain's coming on."),
                    ("I turn from the phone box. Evening.", "Evening."),
                    ("Aye. I shrug. Nothing I can do.", "Aye. Nothing I can do."),
                    ("I look after Mickey's books.", "I look after Mickey's books."),
                    ("I look at you and I see Mickey.", "I look at you and I see Mickey."),
                    ("I nod to the lads every morning, that's all.", "I nod to the lads every morning, that's all."),
                    ("I smile when I think of him.", "I smile when I think of him."),
                    ("I watch the rank for Mickey, mate.", "I watch the rank for Mickey, mate."),
                    ("I looked at him and he ran.", "I looked at him and he ran."),
                    ("I take the fares.", "I take the fares."),
                    ("I look at you steady", "I look at you steady"),
                    ("I look at you like you've lost the plot. Go on then.", "Go on then."),
                    ("I shift my weight, eyes still on the street. Quiet tonight.", "Quiet tonight."),
                    ("I stop and look at you proper. Who told you that?", "Who told you that?"),
                    ("I nod, because that fits what I saw. Go on.", "Go on."),
                    ("I look up to Ron, always have.", "I look up to Ron, always have."),
                    ("I look out for the lads.", "I look out for the lads."),
                    ("I stare at them books all day.", "I stare at them books all day."),
                    ("I turn to Rita when I'm short.", "I turn to Rita when I'm short."),
                };
                string wrongG = null;
                foreach (var (reply, want) in gestureCases) if (ResponseValidator.WithoutGestures(reply) != want) wrongG = reply + " -> " + ResponseValidator.WithoutGestures(reply);
                Check(wrongG == null && ResponseValidator.IsDeflection(ResponseValidator.Validate("I turn from the phone box.", "Ron Kirby"), "Ron Kirby")
                      && ResponseValidator.Validate("I look at you steady. What do you want?", "Ron Kirby") == "What do you want?"
                      && ConversationEngine.FirstSentence(ResponseValidator.WithoutGestures("I look at you steady. Rain's coming on. And")) == "Rain's coming on.",
                      "a stage direction said in the first person is taken out and never spoken early; talk that only sounds like one is kept whole", wrongG ?? "");
            }

            // OPEN AND CLOSED (town list 6bo): every shop's hours from the cast file,
            // researched for 1990 and fitted to who keeps it when; as people say
            // them, and whether it is open now; bad hours refused.
            {
                var hookH = CastDay.Parse(File.ReadAllText(Root("production/specs/hook-cast.json")));
                // Day 0 is a Monday, so day 2 a Wednesday and day 6 a Sunday.
                bool ritas = hookH.OpenAt("ritas", 2, 12, 59) == true && hookH.OpenAt("ritas_counter", 2, 13) == false && hookH.OpenAt("ritas", 1, 17, 29) == true
                             && hookH.OpenAt("ritas", 1, 17, 30) == false && hookH.OpenAt("ritas", 6, 11) == false && hookH.OpenAt("ritas", 0, 8, 59) == false;
                bool late = hookH.OpenAt("mickeys", 1, 2, 30) == true && hookH.OpenAt("mickeys", 1, 3) == false && hookH.OpenAt("mickeys_rank", 7, 1) == true
                            && hookH.OpenAt("mickeys", 6, 8) == false && hookH.OpenAt("mickeys", 6, 9) == true && hookH.OpenAt("mickeys", -1, 22) == true
                            && hookH.OpenAt("mickeys", 6, 23, 30) == false && hookH.OpenAt("mickeys", 7, 0, 30) == true
                            && hookH.OpenAt("hals", 0, 11, 30) == false && hookH.OpenAt("hals", 0, 10, 59) == true && hookH.OpenAt("hals", 0, 12) == true && hookH.OpenAt("hals", 1, 11, 30) == true;
                bool others = hookH.OpenAt("market", 1, 10) == true && hookH.OpenAt("market", 2, 10) == false && hookH.OpenAt("quay", 1, 10) == null
                              && hookH.OpenAt("nowhere", 1, 10) == null && hookH.OpenAt(null, 1, 10) == null && hookH.OpenAt("cafe_front", 6, 12) == false
                              && hookH.OpenAt("fish_market", 6, 10) == false && hookH.OpenAt("kiosk", 6, 10) == true && hookH.HoursWords("cafe") != null;
                // Open with somebody in (town list 6by): at every open half hour of
                // Hal's, the fish shop and Mickey's, somebody of the cast is there.
                string openEmpty = null;
                foreach (var area in new[] { "hals", "fish_market", "mickeys" })
                    for (int d = 0; d < 7; d++)
                        for (int h = 0; h < 24; h++)
                            foreach (var m in new[] { 0, 30 })
                                if (hookH.OpenAt(area, d, h, m) == true && !hookH.People.Any(pp => hookH.AreaOf(hookH.PlaceOf(pp, d, h)) == area))
                                    openEmpty = area + " day " + d + " " + h + ":" + m;
                // Whoever keeps a shop is only at its counter in an hour it is open.
                string keeperAtShut = null;
                foreach (var (who, place) in new[] { ("rita", "ritas_counter"), ("marla", "fish_counter"), ("hal", "hals_shop"), ("zlata", "mickeys_office"), ("dusan", "mickeys_rank") })
                    for (int d = 0; d < 7; d++)
                        for (int h = 0; h < 24; h++)
                            if (hookH.PlaceOf(who, d, h) == place && hookH.OpenAt(place, d, h) != true && hookH.OpenAt(place, d, h, 59) != true) keeperAtShut = who + " day " + d + " hour " + h;
                var said = new Dictionary<string, string>
                {
                    { "ritas", "nine till half five, on Wednesdays it shuts at one, shut on Sundays" },
                    { "mickeys", "seven till three in the morning, on Sundays it opens at nine, on Sundays shut from six till seven in the evening and from eleven at night till midnight" },
                    { "hals", "ten till six, on Wednesdays it shuts at one, on Mondays shut from eleven till twelve, shut on Sundays" },
                    { "market", "Tuesdays, Fridays and Saturdays, eight till four" },
                    { "cafe", "half six in the morning till ten at night, on Sundays eight till twelve" },
                    { "fish_market", "half seven till two, on Wednesdays it shuts at one, shut on Sundays" },
                    { "newsagent", "six in the morning till half five, on Sundays seven till twelve, the pensions counter nine till half five on weekdays" },
                    { "laundry", "eight till half five, shut on Sundays" },
                };
                string wrongWords = null;
                foreach (var kv in said) if (hookH.HoursWords(kv.Key) != kv.Value) wrongWords = kv.Key + ": " + hookH.HoursWords(kv.Key);
                var ronHours = hookH.HoursFor(1, 10);
                var ronLate = hookH.HoursFor(1, 17, 45);
                Check(ritas && late && others && keeperAtShut == null && openEmpty == null && wrongWords == null && hookH.HoursWords("quay") == null
                      && ronHours != null && ronHours.StartsWith("Opening hours, as everybody on the street knows them. Mickey's: seven till three in the morning, on Sundays it opens at nine, on Sundays shut from six till seven in the evening and from eleven at night till midnight; open now. ")
                      && ronHours.Contains("Rita's: nine till half five, on Wednesdays it shuts at one, shut on Sundays; open now.") && !ronHours.Contains("the quay")
                      && ronLate.Contains("Rita's: nine till half five, on Wednesdays it shuts at one, shut on Sundays; shut now.") && ronLate.Contains("The cafe: half six in the morning till ten at night, on Sundays eight till twelve; open now."),
                      "every shop has its hours, as the street says them and whether it is open now, a late close running into the next morning; whoever keeps a shop is at its counter only while it is open",
                      $"{ritas} {late} {others} {keeperAtShut} {openEmpty} {wrongWords} | {ronHours}");

                string Cast(string hours) =>
                    "{\"talk_range_m\":6,\"places\":{\"a\":{\"x_m\":0,\"z_m\":0}},\"areas\":{\"shop\":{\"places\":[\"a\"],\"names\":[\"the shop\"],\"hours\":" + hours + "}},\"people\":[{\"id\":\"p\",\"routine\":[[0,\"a\"]]}],\"ties\":[]}";
                string acceptedBad = null;
                foreach (var badBreak in new[] { "{\"mon\":[[11,13],[12,14]]}", "{\"mon\":[9,10]}", "{\"mon\":[16,17]}", "{\"tue\":[11,12]}", "{\"mon\":[12,11]}", "{\"mon\":[11.25,12]}", "[]", "{\"monday\":[11,12]}" })
                {
                    try { CastDay.Parse(Cast("{\"mon\":[9,17]},\"hours_breaks\":" + badBreak)); acceptedBad = "break " + badBreak; }
                    catch (FormatException) { }
                }
                try { CastDay.Parse("{\"talk_range_m\":6,\"places\":{\"a\":{\"x_m\":0,\"z_m\":0}},\"areas\":{\"shop\":{\"places\":[\"a\"],\"hours_breaks\":{\"mon\":[11,12]}}},\"people\":[{\"id\":\"p\",\"routine\":[[0,\"a\"]]}],\"ties\":[]}"); acceptedBad = "breaks without hours"; }
                catch (FormatException) { }
                foreach (var bad in new[] { "[]", "{}", "{\"mon\":[12,36]}", "{\"mon\":[20,31]}", "{\"mon\":[0,30]}", "{\"sunday\":[9,17]}", "{\"mon\":[9]}", "{\"mon\":[9,9]}", "{\"mon\":[25,26]}", "{\"mon\":[9.25,17]}", "{\"mon\":[20,45]}",
                                            "{\"mon\":[-1,5]}", "{\"mon\":[\"9\",17]}", "{\"mon\":[7,32],\"tue\":[7,20]}", "{\"sun\":[7,32],\"mon\":[7,20]}", "{\"mon\":[9,17,1]}" })
                {
                    try { CastDay.Parse(Cast(bad)); acceptedBad = bad; }
                    catch (FormatException) { }
                }
                var overnight = CastDay.Parse(Cast("{\"mon\":[7,30],\"tue\":[6,20]}"));
                var allWeek = CastDay.Parse(Cast("{\"mon\":[9,17],\"tue\":[9,17],\"wed\":[9,17],\"thu\":[9,17],\"fri\":[9,17],\"sat\":[9,17],\"sun\":[9,17]}"));
                var weekdays = CastDay.Parse(Cast("{\"mon\":[0,24],\"tue\":[9,12],\"wed\":[9,12],\"thu\":[9,12],\"fri\":[9,12]}"));
                // In talk: the line is shown and is the check's O item; a shop's
                // hours cited to it go to the second look, which is shown it.
                var he = new ConversationEngine(new FakeLlm { NextReply = "x" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                he.StreetHours = hookH.HoursFor(2, 14, 30);
                string hp = he.BuildSystemPrompt("Is Rita's open?", new GameTime(2, 14, 30), "");
                var hItems = ClaimCheck.KnownItems(MakeLenaCard(), new List<MemoryEvent>(), null, null, null, null, null, null, null, he.StreetHours);
                var hIds = hItems.ConvertAll(i => i.id);
                var asHabit = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Rita's shuts at one on Wednesdays\", \"kind\": \"habit\", \"source\": \"O1\"}]}", hIds, new List<string>());
                var asTime = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"the cafe shuts at ten\", \"kind\": \"time\", \"source\": \"O1\"}]}", hIds, new List<string>());
                var unsourced = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Rita's opens at eight\", \"kind\": \"time\", \"source\": \"none\"}]}", hIds, new List<string>());
                // Never on the card's word, never passed as small talk, while the hours are an item.
                var hCardIds = new List<string>(hIds); hCardIds.Add("H1");
                var onCard = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Mickey's is open all night\", \"kind\": \"habit\", \"source\": \"H1\"}]}", hCardIds, new List<string>());
                var asNow = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Rita's is open now\", \"kind\": \"now\", \"source\": \"none\"}]}", hIds, new List<string>());
                var cardWithout = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Mickey's is open all night\", \"kind\": \"habit\", \"source\": \"H1\"}]}", new List<string> { "C1", "H1" }, new List<string>());
                var pHabit = new List<string>();
                var viaPeople = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Rita's shuts at one on Wednesdays\", \"kind\": \"habit\", \"source\": \"P1\"}]}", new List<string>(hIds) { "P1" }, pHabit);
                bool words = ClaimCheck.TellsOfHours("Rita's shuts at one on Wednesdays") && ClaimCheck.TellsOfHours("it's shut now") && ClaimCheck.TellsOfHours("open all night")
                             && ClaimCheck.TellsOfHours("the cafe shuts at 10") && ClaimCheck.TellsOfHours("they close at eleven") && ClaimCheck.TellsOfHours("the cafe doesn't close till eleven")
                             && ClaimCheck.TellsOfHours("we open at eight") && ClaimCheck.TellsOfHours("Rita's is shut") && ClaimCheck.TellsOfHours("shuts at teatime")
                             && !ClaimCheck.TellsOfHours("the door's open") && !ClaimCheck.TellsOfHours("the door's open now") && !ClaimCheck.TellsOfHours("the road's closed today")
                             && !ClaimCheck.TellsOfHours("kept one eye open all night") && !ClaimCheck.TellsOfHours("keeps his mouth shut") && !ClaimCheck.TellsOfHours("it's close to ten")
                             && !ClaimCheck.TellsOfHours("quiet till dinner") && !ClaimCheck.TellsOfHours("takings in the till are down")
                             && ClaimCheck.TellsOfHours("I'm shutting at five today") && ClaimCheck.TellsOfHours("Rita's is nine till six") && ClaimCheck.TellsOfHours("Rita's shut about an hour ago")
                             && ClaimCheck.TellsOfHours("Rita's shuts at six, just in case");
                // Every kind but the speaker's own, the weather and the talk goes to
                // the second look, which may clear it from anything but the people.
                var hMemItems = ClaimCheck.KnownItems(MakeLenaCard(), new List<MemoryEvent> { new MemoryEvent(new GameTime(2, 9, 0), "observation", 0.5, "The cafe was busy.") },
                                                      null, null, null, null, null, null, null, he.StreetHours);
                var hMemIds = hMemItems.ConvertAll(i => i.id);
                int kindsFlagged = 0;
                foreach (var (d, k, src) in new[] { ("Rita's is nine till six", "habit", "C1"), ("the cafe doesn't open till nine on Sundays", "denial", "none"), ("we open at eight", "time", "M1"),
                                                     ("they close at eleven", "habit", "C1"), ("it's shut now", "now", "none") })
                    kindsFlagged += ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"" + d + "\", \"kind\": \"" + k + "\", \"source\": \"" + src + "\"}]}", hMemIds, new List<string>()).Count;
                string cafeList = "{\"specifics\": [{\"detail\": \"the cafe shuts at ten\", \"kind\": \"time\", \"source\": \"M1\"}]}";
                var byMemory = ClaimCheck.CheckAsync(new ScriptedLlm(cafeList, "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"M1\"}]}"), "m", hMemItems, "x", CancellationToken.None).GetAwaiter().GetResult();
                var byHours = ClaimCheck.CheckAsync(new ScriptedLlm(cafeList, "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"O1\"}]}"), "m", hMemItems, "x", CancellationToken.None).GetAwaiter().GetResult();
                var hPeopleItems = new List<(string id, string text)>(hMemItems) { ("P1", "Somebody or somewhere on the street they know: Rita, who keeps Rita's pawn; usually at Rita's.") };
                string ritaList = "{\"specifics\": [{\"detail\": \"Rita's shuts at six on Wednesdays\", \"kind\": \"habit\", \"source\": \"P1\"}]}";
                var byPeople = ClaimCheck.CheckAsync(new ScriptedLlm(ritaList, "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"P1\"}]}"), "m", hPeopleItems, "x", CancellationToken.None).GetAwaiter().GetResult();
                bool selfLeft = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"it's closing in\", \"kind\": \"weather\", \"source\": \"none\"}]}", hMemIds, new List<string>()).Count == 0;
                bool hoursAlone = kindsFlagged == 5 && byMemory.invented.Count == 0 && byMemory.calls.Count == 2 && byHours.invented.Count == 0 && byPeople.invented.Count == 1 && selfLeft;
                var selfShut = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"I'll shut the door\", \"kind\": \"self\", \"source\": \"none\"}]}", hIds, new List<string>());
                Check(hp.Contains("Rita's: nine till half five, on Wednesdays it shuts at one, shut on Sundays; shut now.") && hItems.Exists(i => i.id == "O1" && i.text.StartsWith("Opening hours"))
                      && asHabit.Count == 1 && asTime.Count == 1 && unsourced.Count == 1 && onCard.Count == 1 && asNow.Count == 1 && cardWithout.Count == 0 && selfShut.Count == 0 && viaPeople.Count == 1 && pHabit.Count == 0 && words && hoursAlone
                      && ClaimCheck.KnownItems(MakeLenaCard(), new List<MemoryEvent>(), null, null, null, null).TrueForAll(i => i.id != "O1"),
                      "the street's hours are in the talk and are the check's O item: a shop's hours given as a habit, the street, now, a denial or an event go to the second look, which may clear them from anything but the street's people, while the hours are an item; a door, a road, a mouth, the weather and the speaker's own doings untouched",
                      string.Join(" | ", asHabit) + " / " + string.Join(" | ", asTime) + $" / {unsourced.Count} {onCard.Count} {asNow.Count} {cardWithout.Count} {selfShut.Count} {viaPeople.Count} {pHabit.Count} {words} {kindsFlagged} {byMemory.invented?.Count} {byHours.invented?.Count}");
                Check(acceptedBad == null && overnight.OpenAt("shop", 1, 5, 59) == true && overnight.OpenAt("a", 1, 7) == true && overnight.OpenAt("a", 2, 6) == false
                      && allWeek.HoursWords("shop") == "nine till five every day" && weekdays.HoursWords("shop") == "nine till twelve, on Mondays day and night, shut on Saturdays and Sundays"
                      && weekdays.OpenAt("a", 0, 0) == true && weekdays.OpenAt("a", 0, 23, 59) == true && weekdays.OpenAt("a", 1, 0) == false
                      && weekdays.OpenAt("a", 1, -20) == true && weekdays.OpenAt("a", -1, 25) == true && weekdays.OpenAt("a", 0, 9, -1) == true
                      && CastDay.Parse(Cast("{\"fri\":[19,27]}")).HoursWords("shop") == "Fridays, seven in the evening till three in the morning"
                      && CastDay.Parse(Cast("{\"fri\":[0,6]}")).HoursWords("shop") == "Fridays, midnight till six in the morning",
                      "an area's hours are refused unless every weekday named opens as [open, close] in whole or half hours, a late close never running past the next day's opening",
                      (acceptedBad ?? "") + " | " + allWeek.HoursWords("shop") + " | " + weekdays.HoursWords("shop"));
            }

            // WHO THEY KNOW, AND WHERE (town list 6ad): with no map, asking a local is
            // the way round. The named people by name, everybody else by what they
            // do; friends by where they usually are; whoever is here now; and the
            // claim check lets them say it (P items), habits and all.
            {
                var hookP = CastDay.Parse(File.ReadAllText(Root("production/specs/hook-cast.json")));
                var named = new[] { "rocco", "lena", "sam", "june", "ada", "noor", "emil", "rita", "hal" };
                string missing = null;
                foreach (var who in hookP.People)
                {
                    string all = string.Join("\n", hookP.PeopleFor(who, 1, 10));
                    foreach (var n in named)
                        if (n != who && !all.Contains(hookP.NameOf(n) + ", ")) missing = who + " knows nothing of " + n;
                    int told = 0;
                    foreach (var l in hookP.PeopleFor(who, 1, 10)) if (!l.StartsWith("Here with you now") && !l.StartsWith("The street's places")) told++;
                    int always = 0;
                    foreach (var o2 in hookP.People) if (o2 != who && hookP.NameOf(o2) != null) always++;
                    foreach (var (ta, tb, tw) in hookP.Ties) if ((ta == who || tb == who) && tw >= 0.6 && hookP.NameOf(ta == who ? tb : ta) == null) always++;
                    int named9 = 0;
                    foreach (var o2 in hookP.People) if (o2 != who && hookP.NameOf(o2) != null) named9++;
                    if (told > named9 + Math.Max(CastDay.MostKnown, always - named9)) missing = who + " is told of " + told;
                    if (hookP.Described(who) == who || all.Contains(" " + who + " ") || all.Contains(" " + who + ";")) missing = who + " has no description of their own";
                    if (all.Contains(" " + who + ",") || all.Contains("(canon)")) missing = who + "'s lines show an id or a note";
                }
                var ron = hookP.PeopleFor("rocco", 1, 10);
                Check(hookP.NameOf("rocco") == "Ron Kirby" && hookP.RoleOf("rocco") == "Mickey's door and rank" && hookP.NameOf("zlata") == null
                      && hookP.Called("zlata") == "the dispatcher at the cab office" && hookP.Described("rocco") == "Ron Kirby, who keeps Mickey's door and the rank" && hookP.RoleOf("emil") == "mass, the presbytery, calls on the old"
                      && hookP.UsualWords("rocco") == "Mickey's most of the day" && hookP.UsualWords("sam") == null
                      && hookP.UsualWords("joey") == "the quay in the mornings, Mickey's in the afternoons"
                      && hookP.UsualWords("filip") == "the warehouses in the evenings and at night",
                      "the street's names for people, what they do, and where they usually are", hookP.UsualWords("joey") ?? "");
                Check(missing == null && ron.Exists(l => l.StartsWith("Sheila Dunn, Mickey's bookkeeper; you know each other well; usually at Mickey's"))
                      && ron.Exists(l => l.StartsWith("Here with you now: ") && l.Contains("Sheila Dunn"))
                      && ron.Exists(l => l.StartsWith("The street's places, as people call them: ") && l.Contains("the chapel") && !l.Contains("the fish dock"))
                      && hookP.PeopleFor("nobody", 1, 10).Count == 0
                      && hookP.PeopleFor("rocco", 1, 10, new[] { "sam", "zlata", "ghost" }).Contains("Here with you now: Darren Milner; the dispatcher at the cab office.")
                      && hookP.PeopleFor("zora", 1, 10, new[] { "selma", "tanja", "selma" }).Contains("Here with you now: a laundress at the steam laundry; a laundress at the steam laundry.")
                      && !hookP.PeopleFor("zlata", 1, 10).Exists(l => l.StartsWith("Here with you now") && l.Contains("the woman from the fish shop"))
                      && hookP.PeopleFor("sam", 1, 10).FindAll(l => l.Contains("; you know each other")).Count >= 12
                      && !hookP.PeopleFor("rocco", 1, 10, new string[0]).Exists(l => l.StartsWith("Here with you now")),
                      "everybody in the named cast has heard of every named person; a friend comes with where they usually are, and whoever is here now", missing ?? string.Join(" | ", ron));
                var pe = new ConversationEngine(new FakeLlm { NextReply = "x" }, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
                pe.People = hookP.PeopleFor("lena", 1, 10);
                string pp = pe.BuildSystemPrompt("Where's Ron?", new GameTime(1, 10, 0), "");
                var pItems = ClaimCheck.KnownItems(MakeLenaCard(), new List<MemoryEvent>(), null, null, null, null, null, pe.People);
                var pIds = new List<string>();
                foreach (var (id, _) in pItems) pIds.Add(id);
                var pHabits = new List<string>();
                var habitP = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Ron is at Mickey's most of the day\", \"kind\": \"habit\", \"source\": \"P1\"}]}", pIds, pHabits);
                // The second look clears a habit from a P item, never an event.
                string habitList = "{\"specifics\": [{\"detail\": \"Rita does the books\", \"kind\": \"habit\", \"source\": \"P1\"}]}";
                string eventList = "{\"specifics\": [{\"detail\": \"Ron was at the quay\", \"kind\": \"place\", \"source\": \"P1\"}]}";
                string lookP = "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"P1\"}]}";
                var habitCleared = ClaimCheck.CheckAsync(new ScriptedLlm(habitList, lookP), "m", pItems, "x", CancellationToken.None).GetAwaiter().GetResult();
                var eventKept = ClaimCheck.CheckAsync(new ScriptedLlm(eventList, lookP), "m", pItems, "x", CancellationToken.None).GetAwaiter().GetResult();
                Check(pHabits.Count == 1 && habitCleared.invented.Count == 0 && habitCleared.calls.Count == 2 && eventKept.invented.Count == 1,
                      "a habit cited to what they know of the street's people gets a second look, which may clear it from those; an event it never may");
                var habitNone = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Ron is at Mickey's most of the day\", \"kind\": \"habit\", \"source\": \"none\"}]}", pIds);
                var eventP = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Ron was at the quay last night\", \"kind\": \"place\", \"source\": \"P1\"}]}", pIds);
                Check(pp.Contains("- Ron Kirby, who keeps Mickey's door and the rank; you know each other well") && pp.Contains("you do not know where anyone is right now unless they are here with you")
                      && pIds.Contains("P1") && ClaimCheck.NumberedKnown(pItems).Contains("P1: Somebody or somewhere on the street they know: ")
                      && habitP.Count == 1 && habitNone.Count == 1 && eventP.Count == 1
                      && ClaimCheck.RequestItems("m", "x", "y").System.Contains("a C, H or P item describes, but never a shop's opening hours")
                      && ClaimCheck.RequestItems("m", "x", "y").System.Contains("the speaker's own everyday life, tastes and belongings")
                      && ClaimCheck.RequestItems("m", "x", "y").System.Contains("\"I never learned to drive\""),
                      "they are told who they know, and the claim check reads it: a habit or event from a P item alone goes to the second look");

                // A NEWCOMER'S FIRST QUESTIONS (town list 6be): "Who are you?"
                // answered with their own name fell back to "that's all I know".
                // Their own name is a card item, and none for a card lent to
                // somebody else. Who the street's people are stays in the P items,
                // which clear only a habit: split out to clear more, it failed the
                // independent check twice, and its attacks stay refused here.
                string ownName = pItems.Find(i => i.text.StartsWith("Their own name")).id;
                // One detail through the whole check, the second look citing `look`:
                // what is left invented (empty when it may be said).
                IReadOnlyList<string> OneDetail(List<(string id, string text)> items, string detail, string kind, string source, string look) =>
                    ClaimCheck.CheckAsync(new ScriptedLlm("{\"specifics\": [{\"detail\": \"" + detail + "\", \"kind\": \"" + kind + "\", \"source\": \"" + source + "\"}]}",
                                                          "{\"verdicts\": [{\"n\": 1, \"supported\": true, \"source\": \"" + look + "\"}]}"),
                                          "m", items, "x", CancellationToken.None).GetAwaiter().GetResult().invented;
                string ronP = pItems.Find(i => i.text.Contains("Ron Kirby")).id, darrenP = pItems.Find(i => i.text.Contains("Darren Milner")).id;
                Check(pItems.Exists(i => i.id[0] == 'C' && i.text == "Their own name is Lena Moreau.")
                      && OneDetail(pItems, "Lena Moreau", "person", ownName, ownName).Count == 0
                      && ClaimCheck.KnownItems(MakeLenaCard(), new List<MemoryEvent>(), null, null, null, null, null, pe.People, "").TrueForAll(i => !i.text.StartsWith("Their own name"))
                      && OneDetail(pItems, "Ron minding Mickey's door", "person", ronP, ronP).Count == 1
                      && OneDetail(pItems, "Darren doing his rounds", "action", darrenP, darrenP).Count == 1
                      && OneDetail(pItems, "Ron was on Mickey's door", "place", ronP, ronP).Count == 1
                      && OneDetail(pItems, "Darren was with me", "person", darrenP, darrenP).Count == 1,
                      "their own name may be said, and no name for a card lent to somebody else; what the street's people habitually do never places them at a time");
                // TWO OLDER GAPS (town list 6bf, the independent check of 6be): an
                // alibi given as "now" and naming nobody was dropped unread; the
                // same words given twice took the habit's leave both times.
                var nowIds = new List<string> { "S1", "T1", "M1", "P1" };
                var alibi = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"he was here with me when the window went\", \"kind\": \"now\", \"source\": \"S1\"}]}", nowIds);
                var smallTalk = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"quiet this morning\", \"kind\": \"now\", \"source\": \"none\"}, {\"detail\": \"it's gone five\", \"kind\": \"now\", \"source\": \"T1\"}]}", nowIds);
                var twiceHabits = new List<string>();
                var twiceGiven = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Ron on the door\", \"kind\": \"place\", \"source\": \"none\"}, {\"detail\": \"Ron on the door\", \"kind\": \"habit\", \"source\": \"P1\"}]}", nowIds, twiceHabits);
                var onceHabits = new List<string>();
                ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"Ron on the door most days\", \"kind\": \"habit\", \"source\": \"P1\"}]}", nowIds, onceHabits);
                var asSelf = ClaimCheck.ParseItems("{\"specifics\": [{\"detail\": \"he was here with me when the window went\", \"kind\": \"self\", \"source\": \"none\"}]}", nowIds);
                var bareHabits = new List<string>();
                var bareTwice = ClaimCheck.ParseItems("{\"specifics\": [\"Ron on the door\", {\"detail\": \"Ron on the door\", \"kind\": \"habit\", \"source\": \"P1\"}]}", nowIds, bareHabits);
                string leak = null;
                foreach (var a in new[] { "we were in here together when the window went", "my brother was with me all night", "a chap was in here earlier",
                                          "he walked in at nine", "him and me, in here till midnight", "the lads were in here" })
                    if (!ClaimCheck.TellsOfThen(a)) leak = a;
                string small = null;
                foreach (var a in new[] { "he's sat in his cab", "she's got the kettle on", "they close before six", "I've been stood here all afternoon", "she's tired" })
                    if (ClaimCheck.TellsOfThen(a)) small = a;
                Check(alibi.Count == 1 && asSelf.Count == 1 && smallTalk.Count == 0 && twiceGiven.Count == 2 && twiceHabits.Count == 0 && onceHabits.Count == 1
                      && bareTwice.Count == 2 && bareHabits.Count == 0 && leak == null && small == null
                      && ClaimCheck.TellsOfThen("he was here with me when the window went") && !ClaimCheck.TellsOfThen("quiet since eight")
                      && !ClaimCheck.TellsOfThen("it's gone five") && !ClaimCheck.TellsOfThen(null),
                      "an alibi given as any loose kind is read as the claim it is, small talk about now is not; words given both as a habit and as a claim, bare or not, are read as the claim", (leak ?? "") + (small ?? ""));
            }

            // HOW THEY KNOW HIM, for their talk (town list 6s): met is the game's
            // word or their own earlier talk, and what they call him is the game's.
            string never = me.HowTheyKnowHim(false, false, "Tom"), heardOf = me.HowTheyKnowHim(false, true, "Tom");
            Check(never.Contains("for the first time") && never.Contains("the new owner") && !never.Contains("Nowak") && !never.Contains("call him Tom")
                  && heardOf.Contains("have not met") && heardOf.Contains("Nowak") && heardOf.Contains("would not know him by sight") && !heardOf.Contains("call him Tom"),
                  "never met: the new owner, for the first time; heard of: the name, not the face, and never Tom, whatever the game sends", heardOf);
            Check(me.HowTheyKnowHim(true, false, null).Contains("you call him the new owner.") && me.HowTheyKnowHim(true, false, "Nowak").Contains("you call him Nowak.")
                  && me.HowTheyKnowHim(true, false, "Tom").Contains("you call him Tom.") && me.HowTheyKnowHim(true, false, "Tommy").Contains("you call him Tommy.")
                  && me.HowTheyKnowHim(true, false, "Boss").Contains("you call him the new owner.") && me.HowTheyKnowHim(true, false, null).Contains("Say nothing about when, where or how often")
                  && me.HowTheyKnowHim(true, false, null, onlyTheirOwnTalk: true).StartsWith("You have spoken with"),
                  "met: the name the game sends, only if he goes by it, else the new owner; met only by their own talk, spoken with before; always held to their memories");

            // Renaming is free, which is the whole reason this is data.
            var snap = MiniJson.Serialize(me.Capture());
            var twin = new PlayerIdentity();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(snap)));
            Check(twin.Full == me.Full, "the name survives a save");
            twin.Restore(null);
            Check(twin.Full == me.Full, "restoring nothing changes nothing");
            var renamed = new PlayerIdentity();
            renamed.Restore(MiniJson.AsObject(MiniJson.Deserialize("{\"first\":\"Ilya\",\"surname\":\"Brandt\"}")));
            Check(renamed.Full == "Ilya Brandt" && renamed.Diminutive == "Tommy",
                "and a later rename costs nothing, field by field", renamed.Full);
            var old = new PlayerIdentity();
            old.Restore(MiniJson.AsObject(MiniJson.Deserialize("{\"first\":\"Tom\",\"diminutive\":\"Toma\",\"surname\":\"Novak\"}")));
            Check(old.Full == "Tom Nowak" && old.Diminutive == "Tommy",
                "a save made before the names ruling comes back as Nowak and Tommy", old.Full + " / " + old.Diminutive);
        }

        // ---------------------------------------------------------------
        // The consequence layer of violence (roadmap M11)
        // ---------------------------------------------------------------

        static void TestHarm()
        {
            Console.WriteLine("Harm — violence that lasts:");
            var book = new HarmBook();

            // An injury persists. That is the whole point: a punch with no
            // aftermath teaches the player violence is free.
            var cut = book.Inflict("Sam", "Sam", InjuryKind.Cut, day: 3,
                "somebody opened his arm on the ferry rail");
            Check(cut != null && book.IsHurt("Sam", 3), "getting hurt leaves something behind");
            Check(book.IsHurt("Sam", 5), "and it is still there days later");
            Check(!book.IsHurt("Sam", 30), "but it does not last forever");
            Check(!book.IsHurt("Rocco", 3), "and it belongs to the person it happened to");
            Check(book.Inflict(null, null, InjuryKind.Cut, 3, "nobody") == null,
                "hurting nobody is safe");

            // Capability. Injuries compound rather than add — three bruises are
            // not a broken arm — and a person is never quite nothing.
            Check(book.Capability("Rocco", 3) == 1.0, "an unhurt person is all of themselves");
            double hurt = book.Capability("Sam", 3);
            Check(hurt < 1.0 && hurt > 0, "a hurt one is less", hurt.ToString("0.00"));
            book.Inflict("Sam", "Sam", InjuryKind.Bruised, 3, "and took a few more");
            Check(book.Capability("Sam", 3) < hurt, "and two injuries are worse than one");
            for (int i = 0; i < 6; i++) book.Inflict("Sam", "Sam", InjuryKind.Broken, 3, "again");
            Check(book.Capability("Sam", 3) > 0, "but nobody is ever reduced to literally nothing",
                book.Capability("Sam", 3).ToString("0.000"));

            // It SHOWS. An injury is information before it is a stat.
            Check(book.LooksLike("Sam", 3) != null, "you can see it on them");
            Check(book.LooksLike("Rocco", 3) == null, "and see that somebody else is fine");
            var quiet = new HarmBook();
            quiet.Inflict("Ada", "Ada", InjuryKind.Broken, 2, "a rib, under the coat", visible: false);
            Check(quiet.IsHurt("Ada", 2) && quiet.LooksLike("Ada", 2) == null,
                "but a cracked rib is nobody's business");

            // The infirmary. Money AND being seen paying it — the caller plants
            // the fact, but the cost has to be real or it is not a decision.
            var clinic = new HarmBook();
            var arm = clinic.Inflict("Sam", "Sam", InjuryKind.Cut, 3, "the ferry rail");
            var poor = new Wallet(10);
            Check(clinic.Treat(arm, poor, 3) == 0 && !arm.Treated,
                "you cannot be treated on money you do not have");
            var rich = new Wallet(500);
            int paid = clinic.Treat(arm, rich, 3);
            Check(paid == HarmBook.PriceOf(InjuryKind.Cut) && arm.Treated, "treatment costs", paid.ToString());
            Check(rich.Clean == 500 - paid, "and the money is really gone");
            Check(clinic.Treat(arm, rich, 3) == 0, "and you only pay once");

            var dirty = new Wallet(0);
            dirty.EarnDirty(900);
            var arm2 = clinic.Inflict("Rocco", "Rocco", InjuryKind.Cut, 3, "a bottle");
            Check(clinic.Treat(arm2, dirty, 3) == 0,
                "and you cannot hand a doctor a roll of night money");

            // Treated heals faster, and healing restarts from the day you went —
            // a week of ignoring it does not count as a week of getting better.
            var slowBook = new HarmBook();
            var untreated = slowBook.Inflict("A", "A", InjuryKind.Broken, 1, "a door");
            var treatedOne = slowBook.Inflict("B", "B", InjuryKind.Broken, 1, "a door");
            slowBook.Treat(treatedOne, null, 1);
            Check(treatedOne.HealsOnDay < untreated.HealsOnDay, "seeing somebody helps",
                $"{treatedOne.HealsOnDay} vs {untreated.HealsOnDay}");

            // THE DECISION THE INFIRMARY EXISTS FOR: leave it and it turns.
            var rot = new HarmBook();
            var ignored = rot.Inflict("Sam", "Sam", InjuryKind.Cut, 1, "a knife nobody admits to");
            var seen = rot.Inflict("Rocco", "Rocco", InjuryKind.Cut, 1, "the same knife");
            rot.Treat(seen, null, 1);
            var news = rot.DailyTick(2);
            Check(news.Count == 0, "one day is not neglect");
            news = rot.DailyTick(4);
            Check(news.Count == 1, "but leaving it is", news.Count.ToString());
            Check(ignored.WentBad && ignored.Kind == InjuryKind.Broken, "and it gets worse, not just longer");
            Check(!seen.WentBad, "while the one that was looked at is fine");
            Check(rot.DailyTick(6).Count == 0, "and a wound cannot rot twice");
            var bruise = new HarmBook();
            bruise.Inflict("C", "C", InjuryKind.Bruised, 1, "a shove");
            Check(bruise.DailyTick(5).Count == 0, "a bruise is just a bruise and never turns");

            // Trauma is cumulative and does NOT heal with the wound. That is the
            // entire difference between an injury and a scar.
            Check(book.ScarsOf("Sam") == 8, "every hurt leaves a mark on the count", book.ScarsOf("Sam").ToString());
            Check(book.ScarsOf("Rocco") == 0, "and somebody untouched carries none");
            Check(!book.IsHurt("Sam", 200) && book.ScarsOf("Sam") == 8,
                "the wounds heal and the scars do not");

            // Feuds. Not a belief — it does not decay when you leave the room,
            // and evidence cannot settle it. Only somebody choosing to stop can.
            var f = new HarmBook();
            Check(f.FeudBetween("Sam", "Rocco") == null, "two people start out fine");
            var feud = f.Flare("Sam", "Sam", "Rocco", "Rocco", day: 4);
            Check(feud != null && feud.Exchanges == 1, "hurting somebody starts one");
            Check(f.FeudBetween("Rocco", "Sam") == feud, "and it reads the same from either side");
            var again = f.Flare("Rocco", "Rocco", "Sam", "Sam", day: 6);
            Check(ReferenceEquals(again, feud), "a second exchange flares the same feud, not a rival one");
            Check(feud.Exchanges == 2 && feud.Heat > 0.35, "and it gets hotter and longer-running");
            Check(f.Flare("Sam", "Sam", "Sam", "Sam", 6) == null, "nobody feuds with themselves");
            Check(f.Flare(null, null, "Rocco", "Rocco", 6) == null, "and a feud needs two people");

            // A hot feud is a scheduling problem the player solves with people.
            Check(!f.WillWorkTogether("Sam", "Rocco"), "people in a hot feud will not work together");
            Check(f.WillWorkTogether("Sam", "Ada"), "but strangers are fine");
            Check(f.Hottest() == feud, "the Director can ask what the worst of it is");

            // Time cools it but never finishes it.
            for (int d = 7; d < 60; d++) f.DailyTick(d);
            Check(feud.Heat <= 0.21 && feud.Heat > 0, "a feud cools with time");
            Check(!feud.Settled, "but time never ends one");
            Check(f.WillWorkTogether("Sam", "Rocco"), "though it cools enough to stand near each other");
            Check(f.Settle(feud) && feud.Settled && feud.Heat == 0, "somebody has to choose to stop");
            Check(!f.Settle(feud), "and stopping twice is not a thing");
            Check(f.FeudBetween("Sam", "Rocco") == null, "a settled feud is over");
            Check(f.FeudsOf("Sam").Count == 0, "and stops following them around");
            Check(f.Hottest() == null, "with nothing left for the Director to read");

            // Save and load.
            var snap = MiniJson.Serialize(f.Capture());
            var twin = new HarmBook();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(snap)));
            Check(MiniJson.Serialize(twin.Capture()) == snap, "harm survives its own codec");
            var snap2 = MiniJson.Serialize(rot.Capture());
            var twin2 = new HarmBook();
            twin2.Restore(MiniJson.AsObject(MiniJson.Deserialize(snap2)));
            Check(twin2.IsHurt("Sam", 5) == rot.IsHurt("Sam", 5), "including who is still hurt");
            Check(twin2.All.Count == rot.All.Count, "and everything that happened to them");
            var wentBad = false;
            foreach (var i in twin2.All) if (i.WentBad) wentBad = true;
            Check(wentBad, "and which wounds were left too long");
            twin2.Restore(null);
            Check(twin2.All.Count == rot.All.Count, "restoring nothing changes nothing");
        }

        // ---------------------------------------------------------------
        // Finite counterparty purses (roadmap M13)
        // ---------------------------------------------------------------

        static void TestPurses()
        {
            Console.WriteLine("Purses — willing is not the same as able:");
            var book = new PurseBook();
            book.Add(new Purse { OwnerId = "sam", Name = "Sam", Weekly = 60, Ceiling = 95, Cash = 45, PatronId = "danica" });
            book.Add(new Purse { OwnerId = "danica", Name = "Donna", Weekly = 220, Ceiling = 520, Cash = 380 });

            // THE POINT OF THE WHOLE SYSTEM: you get what is there, never more.
            var part = book.Take("sam", 120, day: 1);
            Check(part.Paid == 45, "you get what is in the drawer", part.Paid.ToString());
            Check(part.Short == 75, "and the rest stays owed", part.Short.ToString());
            Check(book.Of("sam").Cash == 0, "the drawer is empty afterwards");
            Check(part.Emptied && !part.InFull, "and the system knows it emptied them");
            Check(part.Line != null && !part.Line.Contains("95") && !part.Line.Contains("/"),
                "the line is a circumstance, not a balance", part.Line);

            var nothing = book.Take("sam", 50, day: 1);
            Check(nothing.Nothing && nothing.Paid == 0, "asking an empty man twice gets you nothing");
            Check(nothing.Line != null, "and he shows you why");
            Check(book.Of("sam").Cash == 0, "you cannot take a negative amount out of somebody");

            // Nobody is ever left owing money to the void.
            var free = book.Take("danica", 0, day: 1);
            Check(free.Paid == 0 && free.Short == 0, "asking for nothing takes nothing");

            // Refill, and the coupling that makes this worth building: a poorer
            // street cannot pay you, and finds out a few days later.
            Check(Math.Abs(PurseBook.FlowAt(0.5) - 1.0) < 1e-9,
                "at ordinary prosperity purses fill at exactly the old rate");
            Check(PurseBook.FlowAt(0.2) < PurseBook.FlowAt(0.8),
                "a squeezed street fills its pockets slower");
            Check(PurseBook.FlowAt(0.0) > 0, "but never stops entirely — a famine is not an economy");

            var rich = new PurseBook();
            rich.Add(new Purse { OwnerId = "a", Weekly = 70, Ceiling = 200, Cash = 0 });
            var poor = new PurseBook();
            poor.Add(new Purse { OwnerId = "a", Weekly = 70, Ceiling = 200, Cash = 0 });
            for (int d = 1; d <= 7; d++) { rich.DailyTick(d, 0.8); poor.DailyTick(d, 0.2); }
            Check(rich.Of("a").Cash > poor.Of("a").Cash,
                "after a week the prosperous street has more in its pockets",
                $"{rich.Of("a").Cash} vs {poor.Of("a").Cash}");
            for (int d = 1; d <= 60; d++) rich.DailyTick(d, 1.0);
            Check(rich.Of("a").Cash == 200, "and nobody hoards past what they would keep to hand",
                rich.Of("a").Cash.ToString());

            // Borrowing: the money MOVES. Cash is conserved on this street, and
            // the favour is real state rather than flavour text.
            int before = book.Of("danica").Cash;
            var patron = book.Borrow("sam", 75, day: 2);
            Check(patron == "danica", "somebody with nowhere to go stays broke; Sam has an uncle", patron);
            Check(book.Of("sam").Cash == 75, "and comes back with what he was asked for");
            Check(book.Of("danica").Cash == before - 75, "which came out of somebody else's pocket");
            Check(book.Favours.Count == 1 && book.Favours[0].PatronId == "danica" && !book.Favours[0].Settled,
                "and is recorded as a favour the Director can read");
            Check(book.Owed("danica").Count == 1, "you can ask who is owed what");
            Check(book.Borrow("sam", 40, day: 2) == null, "nobody goes begging twice in one night");

            // A patron never lends the last of it, and nobody without a patron
            // can borrow at all.
            var tight = new PurseBook();
            tight.Add(new Purse { OwnerId = "x", Weekly = 70, Ceiling = 100, Cash = 0, PatronId = "y" });
            tight.Add(new Purse { OwnerId = "y", Weekly = 70, Ceiling = 100, Cash = 8 });
            Check(tight.Borrow("x", 50, day: 3) == null, "a patron with nothing spare lends nothing");
            tight.Add(new Purse { OwnerId = "z", Weekly = 70, Ceiling = 100, Cash = 0 });
            Check(tight.Borrow("z", 50, day: 3) == null, "and having nobody to go to is its own kind of poor");
            Check(tight.Borrow("nobody", 50, day: 3) == null, "asking about a stranger is safe");

            // Generated purses: three thousand residents, no authored numbers,
            // and the same person always has the same means.
            var gen = new PurseBook();
            var p1 = gen.For("resident_412", "Mira");
            var p2 = gen.For("resident_412");
            Check(ReferenceEquals(p1, p2), "asking twice finds the same person, not a second one");
            var gen2 = new PurseBook();
            Check(gen2.For("resident_412").Weekly == p1.Weekly && gen2.For("resident_412").Cash == p1.Cash,
                "and a fresh city gives that person the same means again");
            Check(p1.Cash > 0 && p1.Cash <= p1.Ceiling, "generated purses start part-full, not empty",
                $"{p1.Cash}/{p1.Ceiling}");
            var spread = new HashSet<int>();
            for (int i = 0; i < 40; i++) spread.Add(gen.For("resident_" + i).Weekly);
            Check(spread.Count > 10, "and people are not all the same means", spread.Count.ToString());

            Check(gen.Liquidity() > 0 && gen.Liquidity() <= 1, "the street's liquidity is a fraction",
                gen.Liquidity().ToString("0.00"));

            // Collection, end to end: a willing debtor who cannot pay it all.
            var mill = new GossipMill(new SocialGraph());
            var sam = new Gossiper("sam", "Sam", null, null, null, "night", 0.5, 0.5, 0.9);
            mill.Add(sam);
            var purses = new PurseBook();
            purses.Add(new Purse { OwnerId = "sam", Name = "Sam", Weekly = 60, Ceiling = 95, Cash = 45 });
            var debts = new DebtBook();
            var marker = new Debtor { Id = "sam", Name = "Sam", Amount = 120, Note = "stock money" };
            debts.Add(marker);
            var wallet = new Wallet(0);
            var day1 = new GameTime(1, 12, 0);

            var loyaltyBefore = sam.Loyalty;
            var outcome = marker.Collect(sam, wallet, mill, day1, purses);
            Check(outcome == CollectOutcome.PaidPart, "a willing man who is short pays what he has", outcome.ToString());
            Check(wallet.Clean == 45, "the money is real", wallet.Clean.ToString());
            Check(marker.Amount == 75, "and the balance stays on the page", marker.Amount.ToString());
            Check(marker.Outstanding, "the debt is not closed");
            Check(sam.Loyalty < loyaltyBefore - 0.05,
                "emptying somebody costs more than being paid by them earns", sam.Loyalty.ToString("0.00"));
            Check(marker.Collect(sam, wallet, mill, day1, purses) == CollectOutcome.Nothing,
                "and you still only ask once a day");

            // Willing and completely empty is a beg, and a truthful one.
            var day2 = new GameTime(2, 12, 0);
            var begged = marker.Collect(sam, wallet, mill, day2, purses);
            Check(begged == CollectOutcome.Begged, "a man with nothing begs rather than refusing", begged.ToString());
            Check(wallet.Clean == 45, "and nothing moves");

            // With no purse book at all, the old behaviour is exactly preserved —
            // every existing caller and save keeps working.
            var oldWay = new DebtBook();
            var rocco = new Gossiper("rocco", "Rocco", null, null, null, "night", 0.5, 0.5, 0.9);
            var full = new Debtor { Id = "rocco", Name = "Rocco", Amount = 60 };
            oldWay.Add(full);
            var w2 = new Wallet(0);
            Check(full.Collect(rocco, w2, mill, day1) == CollectOutcome.Paid,
                "without purses a willing debtor simply pays, as before");
            Check(w2.Clean == 60 && !full.Outstanding, "in full, and the page closes");

            // Overnight, the emptied debtor goes to whoever they have.
            purses.Of("sam").PatronId = "danica";
            purses.Add(new Purse { OwnerId = "danica", Name = "Donna", Weekly = 220, Ceiling = 520, Cash = 380 });
            mill.Add(new Gossiper("danica", "Donna", null, null, null, "day", 0.5, 0.5, 0.5));
            int memoriesBefore = sam.Memory.Events.Count;
            var went = debts.NightBorrowing(purses, mill, new GameTime(3, 2, 0));
            Check(went.Count == 1 && went[0] == "sam", "the man you emptied goes and asks somebody");
            Check(purses.Of("sam").Cash >= 75, "and has it when you next come", purses.Of("sam").Cash.ToString());
            Check(sam.Memory.Events.Count > memoriesBefore, "and remembers having to ask");
            Check(purses.Favours.Count == 1, "somebody on this street is now owed a favour");

            // MONEY THE PLAYER SPENDS ON PEOPLE LANDS IN THEIR DRAWER. Money
            // that vanished when spent would make the district's economy a
            // fiction the moment the player participated in it.
            var paid_out = new PurseBook();
            paid_out.Add(new Purse { OwnerId = "Rocco", Name = "Rocco", Weekly = 140, Ceiling = 260, Cash = 100 });
            paid_out.Credit("Rocco", 200, day: 5);
            Check(paid_out.Of("Rocco").Cash == 300, "a bribe goes into their pocket, not out of the world",
                paid_out.Of("Rocco").Cash.ToString());
            Check(paid_out.Of("Rocco").Cash > paid_out.Of("Rocco").Ceiling,
                "and a windfall is allowed past what they would normally keep to hand");
            Check(paid_out.CarryingUnexplained("Rocco"),
                "which leaves them carrying money their life does not explain");
            Check(paid_out.Of("Rocco").LastWindfallDay == 5, "and the game knows which day it arrived");

            // And they can pay a debt with it next week, which is the loop.
            var payBack = paid_out.Take("Rocco", 250, day: 6);
            Check(payBack.Paid == 250, "so they can settle with the money you gave them", payBack.Paid.ToString());

            // Ordinary income is not a windfall and does respect the ceiling.
            paid_out.Credit("Rocco", 500, day: 7, windfall: false);
            Check(paid_out.Of("Rocco").Cash <= paid_out.Of("Rocco").Ceiling,
                "ordinary money still stops at what somebody keeps to hand");
            Check(paid_out.CarryingUnexplained("nobody") == false, "and a stranger is carrying nothing");
            paid_out.Credit("Rocco", 0, day: 7);
            paid_out.Credit(null, 50, day: 7);
            Check(paid_out.Of("Rocco") != null, "paying nothing, or paying nobody, is safe");

            // Save and load: a part-paid debt must not quietly reset to its
            // original figure, which would steal back everything collected.
            var codecMill = new GossipMill(new SocialGraph());
            codecMill.Add(new Gossiper("sam", "Sam", null, null, null, "night", 0.5, 0.5, 0.9));
            var saved = SaveCodec.Capture(day2, wallet, new Campaign(), new PlayerKnowledge(),
                new SecretsBook(), new BeatBook(), codecMill, debts, null);
            var reloadDebts = new DebtBook();
            var reloadMarker = new Debtor { Id = "sam", Name = "Sam", Amount = 120 };
            reloadDebts.Add(reloadMarker);
            SaveCodec.Restore(saved, new Wallet(0), new Campaign(), new PlayerKnowledge(), new SecretsBook(),
                new BeatBook(), new GossipMill(new SocialGraph()), reloadDebts, out _);
            Check(reloadMarker.Amount == 75, "a part-paid debt reloads at what is still owed, not at what it was",
                reloadMarker.Amount.ToString());

            var purseSnap = MiniJson.Serialize(purses.Capture());
            var twin = new PurseBook();
            twin.Restore(MiniJson.AsObject(MiniJson.Deserialize(purseSnap)));
            Check(MiniJson.Serialize(twin.Capture()) == purseSnap, "and the purses survive their own codec");
            Check(twin.Of("sam").PatronId == "danica", "including who somebody can go to");
            Check(twin.Favours.Count == 1, "and what the street is owed");
            twin.Restore(null);
            Check(twin.Of("sam") != null, "restoring nothing changes nothing");
        }

        // ---------------------------------------------------------------
        // Traffic (roadmap M12)
        // ---------------------------------------------------------------

        static void TestTraffic()
        {
            Console.WriteLine("Traffic — the streets get used:");
            StreetMap.Rebuild();

            // The catalogue. Six kinds, and the differences between them have to
            // be real differences, or "vehicle variety" is six colours of car.
            Check(VehicleKinds.All.Length == 7, "seven kinds of vehicle",
                VehicleKinds.All.Length.ToString());
            foreach (var k in VehicleKinds.All)
            {
                Check(k.Length > 0 && k.Width > 0 && k.TopSpeed > 0, $"{k.Id} has a size and a speed");
                Check(!string.IsNullOrEmpty(k.Witness), $"{k.Id} is something a witness can name");
                Check(k.Brake > k.Accel, $"{k.Id} stops faster than it starts, like every real vehicle");
            }
            Check(VehicleKinds.Truck.Length > VehicleKinds.Car.Length
                && VehicleKinds.Bus.Length > VehicleKinds.Truck.Length
                && VehicleKinds.Bike.Length < VehicleKinds.Car.Length,
                "a bus is longer than a lorry is longer than a car is longer than a bicycle");
            Check(VehicleKinds.Bike.TopSpeed < VehicleKinds.Car.TopSpeed, "and a bicycle is slower than a car");
            Check(VehicleKinds.Bus.StopsAtStops && VehicleKinds.Taxi.WaitsAtRanks && VehicleKinds.Bike.UsesLanes,
                "buses stop, cabs wait, bicycles use the lanes");
            Check(VehicleKinds.ById("truck") == VehicleKinds.Truck && VehicleKinds.ById("nope") == null,
                "kinds look up by id, and an unknown id is null rather than a guess");

            // THE PATROL CAR. A big saloon, quicker than the traffic, and the
            // only vehicle in the catalogue a witness names as information
            // rather than as a noun.
            Check(VehicleKinds.Police.Length > VehicleKinds.Car.Length
                && VehicleKinds.Police.TopSpeed > VehicleKinds.Car.TopSpeed,
                "a police car is longer and faster than an ordinary one");
            Check(VehicleKinds.Police.Rarity <= VehicleKinds.Truck.Rarity,
                "and rarer than a lorry, so it is a thing you notice");
            Check(!VehicleKinds.Police.StopsAtStops && !VehicleKinds.Police.WaitsAtRanks
                && !VehicleKinds.Police.UsesLanes,
                "it does not queue at stops, wait at ranks or thread the bike lanes");

            // EVERY VEHICLE FITS ITS HALF OF THE NARROWEST ROAD IT DRIVES ON,
            // and this check is load-bearing in a way it was not before.
            //
            // `TrafficHost` used to scale a kit mesh UNIFORMLY by its length,
            // so what the sim collided and what the player saw were different
            // objects: measured with `tools/prop-dimensions.py`, the rendered
            // lorry was 3.97m against a declared 2.4, and on a six-metre
            // street that put it 0.48m over the centreline and 0.48m over the
            // kerb. `vehiclesOffRoad=0` could never see it — that gate reads
            // `Kind.Width`, and the box was never what was too big.
            //
            // The mesh is now scaled to this box on every axis, so these
            // numbers are the render as well as the collision, and a kind that
            // outgrows its lane here is a kind that will visibly do it.
            //
            // A street is 6.0m wide (`StreetEdge.Width`), traffic rides at
            // width/4 from the centreline, so the lane centre is 1.5m out and
            // the kerb is at 3.0m. Bicycles are excluded because they alone
            // ride the 4.0m lanes, on their own offset rule.
            const double streetHalf = 3.0, laneCentre = 1.5;
            foreach (var k in VehicleKinds.All)
            {
                if (k.UsesLanes) continue;
                Check(k.Width / 2.0 <= laneCentre,
                    $"{k.Id} keeps its own side of a street", $"{k.Width:0.00}m wide");
                Check(laneCentre + k.Width / 2.0 <= streetHalf,
                    $"{k.Id} stays inside the kerb on a street",
                    $"{laneCentre + k.Width / 2.0:0.00}m of {streetHalf:0.00}m");
            }

            // PATROL DENSITY — the street saying how hard she is looking.
            //
            // A white saloon going past is set dressing. Three of them in an
            // hour where there was one yesterday is the player being told the
            // inquiry has moved, without a UI and without a number, which is
            // what "information 90" is supposed to mean.
            //
            // THE ACCEPTING CASE IS THE QUIET TOWN AND IT GOES FIRST, because
            // the expensive failure here is not "a manhunt looks the same" —
            // it is a default that fills an ordinary street with police and
            // makes the loud state unreachable. A sim nobody has told about
            // the inquiry must produce exactly the traffic that existed before
            // any of this was written.
            var quietSim = new TrafficSim(seed: 4242);
            Check(quietSim.PatrolWeight == VehicleKinds.Police.Rarity,
                "a sim nobody has told about the law runs the base rarity",
                $"{quietSim.PatrolWeight}");
            Check(TrafficSim.PatrolWeightFor(Inquiry.None) == VehicleKinds.Police.Rarity,
                "and so does an inquiry that has not started");

            // MONOTONIC, WHICH IS THE WHOLE CLAIM. Each stage is louder than
            // the one below it; anything else and the street would say the
            // heat had dropped while it rose.
            var stages = new[] { Inquiry.None, Inquiry.Procedure,
                                 Inquiry.Investigation, Inquiry.Manhunt };
            for (int s = 1; s < stages.Length; s++)
                Check(TrafficSim.PatrolWeightFor(stages[s])
                      > TrafficSim.PatrolWeightFor(stages[s - 1]),
                    $"{stages[s]} puts more cars out than {stages[s - 1]}",
                    $"{TrafficSim.PatrolWeightFor(stages[s])}");

            // AND THE TWO ENDS MUST BE FAR ENOUGH APART TO READ WITHOUT
            // COUNTING, since counting is exactly what a player will not do.
            quietSim.Populate(28);
            int quietWant = quietSim.PatrolTarget();
            quietSim.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.Manhunt);
            int huntWant = quietSim.PatrolTarget();
            Console.WriteLine($"  .. patrols of 28: none={quietWant} manhunt={huntWant}");
            Check(huntWant >= quietWant * 3,
                "a manhunt puts at least three times as many patrols out as a quiet week",
                $"{quietWant} -> {huntWant}");

            // REBALANCE, BOTH DIRECTIONS, AND ONLY WHILE PARKED.
            var patrolSim = new TrafficSim(seed: 99);
            patrolSim.Populate(28);
            patrolSim.SetHour(3);                 // the small hours: most parked up
            patrolSim.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.Manhunt);
            var moved = new List<int>();
            int n1 = patrolSim.Rebalance(moved);
            Check(n1 > 0 && moved.Count == n1,
                "a manhunt converts parked cars into patrols and names them",
                $"{n1} changed, {moved.Count} named");
            Check(patrolSim.PatrolCount() == patrolSim.PatrolTarget(),
                "and it reaches the target",
                $"{patrolSim.PatrolCount()} of {patrolSim.PatrolTarget()}");
            Check(patrolSim.Rebalance() == 0,
                "asking twice changes nothing — it is a level, not a step");

            patrolSim.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.None);
            Check(patrolSim.Rebalance() > 0 && patrolSim.PatrolCount() == patrolSim.PatrolTarget(),
                "and when she loses interest the street empties of them again",
                $"{patrolSim.PatrolCount()} of {patrolSim.PatrolTarget()}");

            // A MOVING CAR IS NEVER TOUCHED. The seam this avoids is a mesh
            // changing in front of the player, and it is the reason the whole
            // thing hangs off dormancy rather than off a timer.
            var busySim = new TrafficSim(seed: 7);
            busySim.Populate(28);
            busySim.SetHour(8);                   // rush: everything awake
            int awake = busySim.AwakeCount();
            int wasPatrol = busySim.PatrolCount();
            busySim.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.Manhunt);
            busySim.Rebalance();
            int stillMoving = 0;
            foreach (var v in busySim.Vehicles)
                if (!v.Dormant && v.Kind.Id == VehicleKinds.PoliceId) stillMoving++;
            Check(stillMoving == wasPatrol,
                "at rush hour no vehicle on the road is converted under the player",
                $"{awake} awake, patrols among them {wasPatrol} -> {stillMoving}");

            // AND THE BUS AND THE BICYCLES SURVIVE IT. Converting the route
            // bus would strand the transit line, and a bicycle is a different
            // shape of thing entirely.
            var keepSim = new TrafficSim(seed: 11);
            keepSim.Populate(28);
            keepSim.SetHour(3);
            int busesBefore = 0, bikesBefore = 0;
            foreach (var v in keepSim.Vehicles)
            {
                if (v.Kind.Id == VehicleKinds.BusId) busesBefore++;
                if (v.Kind.Id == VehicleKinds.BikeId) bikesBefore++;
            }
            keepSim.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.Manhunt);
            keepSim.Rebalance();
            int busesAfter = 0, bikesAfter = 0;
            foreach (var v in keepSim.Vehicles)
            {
                if (v.Kind.Id == VehicleKinds.BusId) busesAfter++;
                if (v.Kind.Id == VehicleKinds.BikeId) bikesAfter++;
            }
            Check(busesAfter == busesBefore && bikesAfter == bikesBefore,
                "the bus and the bicycles are never converted",
                $"bus {busesBefore}->{busesAfter}, bikes {bikesBefore}->{bikesAfter}");

            // A PATROL GOES WHERE THE TROUBLE IS, and the numbers that forced
            // this are worth keeping beside it. `01f4eeb` ran a full manhunt
            // with every car the loudest state asks for out on the street —
            // `patrolWant=6 patrolNow=6` — and the shot counter read
            // `patrolInShotPeak=1 patrolInShotMean=0.10` over twenty frames.
            // One frame in ten, never more than one. The quiet state is two
            // cars, about 0.03, and a player cannot tell those apart.
            //
            // Six cars spread evenly over seven districts is nothing anywhere,
            // and the fix is not a bigger weight — that fills the far
            // districts with police nobody sees. It is that patrols work a
            // BEAT.
            //
            // THE ACCEPTING CASE FIRST: no focus set must mean the traffic
            // that existed before any of this, or a quiet street becomes a
            // police state by default.
            var beatSim = new TrafficSim(seed: 31);
            beatSim.Populate(28);
            Check(beatSim.PatrolFocusDistrict == "",
                "with no focus set the patrols wander like anybody else");

            // Drive both ways and compare where the patrols END UP, which is
            // the only thing a player can see. Districts rather than metres,
            // because the district is the unit the routing actually uses and
            // measuring in metres here would invent a second definition of
            // "near" beside the one being tested.
            string Beat(TrafficSim s)
            {
                var counts = new Dictionary<string, int>();
                foreach (var v in s.Vehicles)
                {
                    if (v.Kind == null || v.Kind.Id != VehicleKinds.PoliceId) continue;
                    var n = StreetMap.Node(v.ToId);
                    if (n == null) continue;
                    var d = StreetMap.DistrictAt(n.X, n.Z) ?? "";
                    counts[d] = counts.TryGetValue(d, out var c) ? c + 1 : 1;
                }
                var best = ""; int most = 0;
                foreach (var kv in counts) if (kv.Value > most) { most = kv.Value; best = kv.Key; }
                return $"{best}:{most}/{counts.Count}";
            }

            beatSim.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.Manhunt);
            beatSim.SetHour(3);
            beatSim.Rebalance();
            beatSim.SetHour(8);
            int patrols = beatSim.PatrolCount();
            Check(patrols >= 4, "the manhunt has patrol cars to place", $"{patrols}");

            // Loose, because a route is a path and a car in the wrong corner
            // takes time to arrive: what is asserted is that they CONVERGE,
            // not that they teleport.
            var focus = StreetMap.DistrictAt(
                StreetMap.Node(beatSim.Vehicles[0].ToId).X,
                StreetMap.Node(beatSim.Vehicles[0].ToId).Z) ?? "";
            beatSim.PatrolFocusDistrict = focus;
            for (int t = 0; t < 400; t++) beatSim.Step(0.5);
            string after = Beat(beatSim);
            Console.WriteLine($"  .. patrol beat: focus={focus} spread after={after}");
            int inFocus = 0;
            foreach (var v in beatSim.Vehicles)
            {
                if (v.Kind == null || v.Kind.Id != VehicleKinds.PoliceId) continue;
                var n = StreetMap.Node(v.ToId);
                if (n != null && (StreetMap.DistrictAt(n.X, n.Z) ?? "") == focus) inFocus++;
            }
            Check(inFocus > patrols / 2,
                "most of the patrols are heading into the district with the trouble in it",
                $"{inFocus} of {patrols} bound for {focus}");

            // AND CLEARING THE FOCUS MUST STOP THEM BEING STEERED THERE —
            // which is NOT the same as "they leave", and the difference cost
            // this test a failure worth keeping.
            //
            // The first version asserted that after standing the beat down
            // the patrols disperse out of the focus district. It passed until
            // `DistrictAt`'s margin was corrected from a flat 12m to half a
            // block, at which point the districts got bigger and all five
            // stayed put. That is not a regression: ordinary traffic PREFERS
            // its own district by design, because uniform destinations put
            // every journey through one of four bridges. Cars in the Hook
            // stay in the Hook whether or not anybody is hunting you, and the
            // old assertion only passed because the boxes were too small to
            // contain them.
            //
            // So the property is comparative, and it is measured that way: a
            // beat aimed at a district the patrols are NOT in must draw them,
            // and no beat must not. Same sim, same seed, same step count —
            // only the focus differs, so nothing has to be assumed about how
            // fast a car crosses town.
            int InFocusAfter(int seed, string focusDistrict, string countIn)
            {
                var s2 = new TrafficSim(seed: seed);
                s2.Populate(28);
                s2.PatrolWeight = TrafficSim.PatrolWeightFor(Inquiry.Manhunt);
                s2.SetHour(3);
                s2.Rebalance();
                s2.SetHour(8);
                s2.PatrolFocusDistrict = focusDistrict;
                for (int t = 0; t < 600; t++) s2.Step(0.5);
                int n = 0;
                foreach (var v in s2.Vehicles)
                {
                    if (v.Kind == null || v.Kind.Id != VehicleKinds.PoliceId) continue;
                    var nd = StreetMap.Node(v.ToId);
                    if (nd != null && (StreetMap.DistrictAt(nd.X, nd.Z) ?? "") == countIn) n++;
                }
                return n;
            }
            var target = "Ironside";
            int drawn = InFocusAfter(31, target, target);
            int undrawn = InFocusAfter(31, "", target);
            Console.WriteLine($"  .. patrol beat: {target} with a beat={drawn}, without={undrawn}");
            Check(drawn > undrawn,
                "a beat draws patrols into a district they were not working",
                $"{drawn} with, {undrawn} without");

            // Lights. A pure function of the clock, so a light cannot drift out
            // of step with its own render or need saving.
            var centre = StreetMap.Node("j2_2");        // the founding cross
            var lit = StreetMap.Node("j1_1");           // avenue meets avenue
            var edge = StreetMap.Node("j0_0");          // the outer ring
            Check(Signals.HasLights(lit), "the big crossings have lights");
            Check(!Signals.HasLights(centre), "the founding cross keeps its old give-way");
            Check(!Signals.HasLights(edge), "and the edge of town gets a stop sign, not a light");
            Check(!Signals.HasLights(StreetMap.Node("stop_bar_door")), "a doorway is not a junction");
            Check(!Signals.HasLights(null), "and asking about nothing is safe");

            // Over one cycle, both axes get a green and the two greens never
            // overlap. This is the property that means the lights are safe.
            bool sawNs = false, sawEw = false, everBoth = false;
            for (double t = 0; t < Signals.Cycle; t += 0.25)
            {
                bool ns = Signals.MayEnter(lit, t, northSouth: true);
                bool ew = Signals.MayEnter(lit, t, northSouth: false);
                sawNs |= ns; sawEw |= ew; everBoth |= ns && ew;
            }
            Check(sawNs && sawEw, "both directions get a turn");
            Check(!everBoth, "and never at the same moment");
            Check(Signals.Phase(lit, 0) == Signals.Phase(lit, Signals.Cycle),
                "the cycle actually cycles");
            bool offsets = Signals.Offset(StreetMap.Node("j1_1")) != Signals.Offset(StreetMap.Node("j3_3"));
            Check(offsets, "junctions do not all change together, which is what makes a grid feel mechanical");

            // A populated city.
            var sim = new TrafficSim(seed: 11);
            sim.Populate(14);
            Check(sim.Vehicles.Count >= 10, "the streets have traffic on them", sim.Vehicles.Count.ToString());
            Check(sim.Vehicles.Exists(v => v.Kind.StopsAtStops), "including a bus");
            Check(sim.BusLoop.Count >= 8 && sim.IsBusStop(sim.BusLoop[0]),
                "which has a circuit with stops on it", sim.BusLoop.Count.ToString());

            // THINGS THAT WAIT, which nothing has ever asserted.
            //
            // `DwellUntil` is honoured by the mover and set on arrival for a
            // bus at a stop and a cab at a rank. Both were written, both are
            // live, and the whole mechanism had one mention in this file — the
            // shape rule 6 is about, one step short of it: not unreached, just
            // unproven.
            //
            // It matters more than a bus timetable. A vehicle that waits is
            // most of what separates traffic from a conveyor belt, and a cab
            // standing on a rank is a thing the street has that nobody drives.
            //
            // Asserted by RUNNING it rather than by reading the flags, because
            // the flags are what I would have got wrong: `WaitsAtRanks` being
            // true on the kind proves nothing about whether any cab ever
            // reaches a rank.
            var waits = new TrafficSim(seed: 5);
            waits.Populate(24);
            bool taxiWaited = false, busWaited = false;
            for (int i = 0; i < 3000 && !(taxiWaited && busWaited); i++)
            {
                waits.Step(0.5);
                foreach (var v in waits.Vehicles)
                {
                    if (v.DwellUntil <= waits.Clock) continue;
                    if (v.Kind.WaitsAtRanks) taxiWaited = true;
                    else if (v.Kind.StopsAtStops) busWaited = true;
                }
            }
            Check(waits.Ranks.Count > 0, "the city has cab ranks to wait on",
                  waits.Ranks.Count.ToString());
            Check(busWaited, "a bus dwells at its stops rather than sailing past");
            Check(taxiWaited, "and a cab actually waits on a rank");
            foreach (var v in sim.Vehicles)
                Check(v.Edge != null && v.Edge.Driveable || v.Kind.UsesLanes,
                    $"vehicle {v.Id} starts on a road it is allowed to use", v.Edge?.Kind);

            // Three minutes of traffic, checked every step for the things that
            // must NEVER be true. A screenshot cannot tell you any of this.
            double worstGap = 999;
            double earlyDistance = 0, midDistance = 0;
            int redRunners = 0, offRoad = 0, litCrossings = 0;
            var heading = new Dictionary<int, (string from, string to)>();
            for (int i = 0; i < 360; i++)
            {
                heading.Clear();
                foreach (var v in sim.Vehicles) heading[v.Id] = (v.FromId, v.ToId);
                double before = sim.Clock;
                sim.Step(0.5);
                if (i == 119) earlyDistance = sim.TotalDistance;
                if (i == 239) midDistance = sim.TotalDistance;
                double gap = sim.TightestGap();
                if (gap < worstGap) worstGap = gap;
                foreach (var v in sim.Vehicles)
                {
                    // TARMAC, NOT CARRIAGEWAY, AND THE DIFFERENCE ONLY STARTED
                    // MATTERING WHEN THE ADDRESSES MOVED.
                    //
                    // The router's own comment says a driving route "may leave a
                    // lane at the start and enter one at the end — that is a car
                    // pulling out and parking". So a vehicle on a lane at either
                    // end of its journey is doing exactly what it is allowed to
                    // do. This asked `OnRoad`, which excludes lanes, and passed
                    // anyway for a reason that was about to stop being true:
                    // thirty-one of the fifty-two addresses were standing IN a
                    // carriageway, so parking happened on the road.
                    //
                    // `StreetMap.SetPlacesBackFromRoads` puts them on pavements,
                    // and every one of the resulting failures was measured
                    // rather than assumed — all of them a vehicle on a `lane`
                    // edge with `from` or `to` a `stop_` node, and `OnStreet`
                    // true for every single one. The subject changed and the
                    // instrument kept its old question, which is this project's
                    // most repeated fault wearing a test's clothes.
                    //
                    // THE TEETH ARE UNCHANGED. A car in a courtyard or a field
                    // is on neither a road nor a lane and still fails here, and
                    // threading lanes MID-route is forbidden by the router and
                    // asserted separately. Widening a margin would have been the
                    // thing rule 2 forbids; asking the right question is not.
                    if (!v.Kind.UsesLanes
                        && !StreetMap.OnRoad(v.X, v.Z, margin: 1.0)
                        && !StreetMap.OnStreet(v.X, v.Z, margin: 1.0)) offRoad++;

                    // A vehicle whose road changed has just passed through the
                    // junction between them. That is the exact instant "entering
                    // on red" means — being NEAR a red light is not an offence,
                    // and asking the question any earlier tests the approach
                    // rather than the crossing.
                    var prior = heading[v.Id];
                    if (prior.to == v.FromId && prior.from != v.FromId)
                    {
                        var crossed = StreetMap.Node(prior.to);
                        if (!Signals.HasLights(crossed)) continue;
                        litCrossings++;
                        var a = StreetMap.Node(prior.from);
                        bool ns = Math.Abs(crossed.Z - a.Z) >= Math.Abs(crossed.X - a.X);
                        bool greenSomewhereInStep = false;
                        for (double t = before; t <= sim.Clock + 1e-9; t += TrafficSim.SubStep)
                            greenSomewhereInStep |= Signals.MayEnter(crossed, t, ns);
                        if (!greenSomewhereInStep) redRunners++;
                    }
                }
            }
            Check(litCrossings > 0, "traffic does pass through the lit junctions", litCrossings.ToString());
            Check(worstGap >= 0, "no two vehicles ever occupy the same piece of road", worstGap.ToString("0.00"));
            Check(offRoad == 0, "and nobody ever leaves the tarmac", offRoad.ToString());
            Check(redRunners == 0, "nobody crosses a stop line on red", redRunners.ToString());

            // Liveness. The failure that would actually ruin an evening is not a
            // crash — it is a grid wedged solid, with the player stuck behind a
            // queue that will never move again.
            Check(sim.TotalDistance > 1000, "the traffic actually goes somewhere", sim.TotalDistance.ToString("0"));
            int moving = sim.Vehicles.FindAll(v => v.Speed > 0.5).Count;
            Check(moving >= sim.Vehicles.Count / 3, "and most of it is moving at any moment", moving.ToString());

            // THE GATE THAT CAUGHT IRONSIDE. A single-instant sample cannot tell
            // a queue from a city slowly congealing, and congealing is exactly
            // what a third district produced: uniform random destinations made
            // every second journey cross one of four chokepoints, and throughput
            // fell by two thirds over three minutes without ever hard-locking.
            // So measure the LAST minute against the first and require the city
            // to still be moving at the end of the evening.
            double firstThird = earlyDistance;
            double lastThird = sim.TotalDistance - midDistance;
            Check(lastThird > firstThird * 0.6,
                "and it is still moving as freely at the end as at the start",
                $"{firstThird:0} then {lastThird:0}");
            // NOBODY IS PERMANENTLY WEDGED — AND THE FIRST VERSION OF THIS
            // GATE COULD NOT TELL A STUCK CAR FROM ONE THAT DROVE IN A CIRCLE.
            //
            // It sampled (edge, s) once, stepped sixty seconds, sampled again,
            // and called a vehicle wedged if both matched within two metres.
            // Two instants cannot see the sixty seconds between them: a car
            // that leaves, drives a loop of eight edges and comes back reads
            // EXACTLY like one that never moved.
            //
            // MEASURED, which is how it was caught: the flagged car reported
            // `edgesSeenInWindow=8`. It crossed the Exchange twice.
            //
            // THE COST OF THIS ONE WAS A WRONG CONCLUSION, NOT A WRONG NUMBER.
            // The false positive appeared the moment `DistrictAt` started
            // routing traffic into the outer districts, so it read as "that
            // change wedges traffic" — and a real fix was queued for a day on
            // the strength of it. A ten-seed sweep then "confirmed" wedging at
            // double density on unmodified code, which was the same false
            // positive at a density that loops more, quoted as exoneration.
            // Both readings came from an instrument that answers a different
            // question from the one in its name.
            //
            // So the window is read WHOLE. A vehicle is wedged when it
            // occupied exactly ONE edge for the entire minute and advanced no
            // more than two metres along it. Every distinct edge it touches is
            // recorded on every step, so a loop is visible as the eight edges
            // it actually is.
            // THE PREDICATE, NAMED, SO BOTH OF ITS ANSWERS CAN BE WATCHED.
            //
            // Rule 5b: a guard has two outcomes and shipping it means having
            // seen BOTH. The live run below is the accepting case — it is
            // green, over a real sim. The rejecting case cannot be produced on
            // demand from a real sim (that is the whole difficulty: a genuine
            // wedge is rare and seed-dependent), so it is asserted here
            // directly against the numbers that describe one.
            //
            // The third row is the REAL reading that defeated the old gate,
            // kept as a fixture: eight edges and a 0.3m difference between the
            // window's two ends. The old test called that wedged. If this
            // starts calling it wedged again, the regression is caught by the
            // test rather than by a day of chasing a fix that was never wrong.
            static bool MovedOn(bool dormant, int edgesSeen, double deltaS) =>
                dormant || edgesSeen > 1 || deltaS > 2.0;

            Check(!MovedOn(false, 1, 0.5),
                "the wedge gate calls one edge and half a metre in a minute WEDGED");
            Check(MovedOn(false, 1, 40.0),
                "and a car that stayed on one long edge but covered forty metres is not");
            Check(MovedOn(false, 8, 0.3),
                "and the eight-edge loop that defeated the two-instant version is not",
                "edgesSeen=8 deltaS=0.3");
            Check(MovedOn(true, 1, 0.0),
                "and a parked car is not traffic");

            int stuck = 0;
            var mark = new Dictionary<int, double>();
            foreach (var v in sim.Vehicles) mark[v.Id] = sim.TotalDistance;
            var was = new Dictionary<int, (string from, string to, double s)>();
            foreach (var v in sim.Vehicles) was[v.Id] = (v.FromId, v.ToId, v.S);
            var seenEdges = new Dictionary<int, HashSet<string>>();
            foreach (var v in sim.Vehicles) seenEdges[v.Id] = new HashSet<string>();
            for (int i = 0; i < 120; i++)
            {
                sim.Step(0.5);
                foreach (var v in sim.Vehicles) seenEdges[v.Id].Add(v.FromId + "->" + v.ToId);
            }
            foreach (var v in sim.Vehicles)
            {
                var w = was[v.Id];
                bool movedOn = MovedOn(v.Dormant, seenEdges[v.Id].Count, Math.Abs(v.S - w.s));
                if (!movedOn)
                {
                    stuck++;
                    // BOTH ENDS OF THE WINDOW, because one end cannot show a
                    // wedge. The first version of this line printed `w.from`
                    // and `w.to` — the BEFORE edge — beside `v.S`, the AFTER
                    // position, and reported a car that had crossed four
                    // junctions as stuck at 63.8m. A diagnostic that mixes two
                    // instants is the exact fault the rest of this project
                    // spends its time finding, and it was in the tool written
                    // to find it.
                    Console.WriteLine($"  WEDGED v{v.Id} kind={v.Kind.Id} "
                        + $"before={w.from}->{w.to}@{w.s:0.0} "
                        + $"after={v.FromId}->{v.ToId}@{v.S:0.0} "
                        + $"speed={v.Speed:0.00} dormant={v.Dormant} "
                        + $"route={v.Route.Count} stoppedAt={v.StoppedAt} inJunction={v.InJunction}");
                }
            }
            Check(stuck == 0, "in a minute of traffic, nobody is permanently wedged", stuck.ToString());

            // WHAT THE SIM'S `gap` NUMBER HAS ACTUALLY BEEN SAYING, and it took
            // sixty-eight kept runs to ask. Reading `gap=` off every one of them:
            // twenty said `not-measured`, four were negative (-0.28, -2.58,
            // -2.69, -3.20) and SIXTEEN read exactly 0.00. Sixteen identical
            // readings to two decimals is not sixteen coincidences.
            //
            // 0.00 is `Enforce` firing. The clamp sets `v.S = lead.S -
            // lead.Kind.Length`, so a resolved overlap leaves the pair at a gap
            // of exactly zero — and zero passes `>= 0`, which is every bound this
            // has ever had. "The planner kept the room" and "the clamp had to
            // shove them apart this frame" were the same reading.
            //
            // So the distance was never the question. `OverlapsResolved` is, and
            // these two assertions are the pair rule 5b asks for: one that a
            // healthy run must PASS, and one that says what would have to break
            // for it to fail.
            var clean = new TrafficSim(seed: 11);
            clean.Populate(14);
            for (int i = 0; i < 240; i++) clean.Step(0.5);
            Check(clean.OverlapsResolved >= 0 && clean.TotalDistance > 500,
                "the overlap counter exists on a run that actually drove",
                $"{clean.OverlapsResolved} resolved over {clean.TotalDistance:0}m");
            // THE PLANNER, NOT THE CLAMP, MUST BE DOING THE DRIVING. A clamp that
            // fires once per several hundred metres is the discrete-step rounding
            // it was written for; one that fires every few metres means `Decide`
            // is not keeping the room and the traffic is being held apart by
            // force. Bounded per METRE DRIVEN rather than per step, because the
            // step count is a property of the test and the metres are a property
            // of the city.
            double perKm = clean.TotalDistance > 0
                ? 1000.0 * clean.OverlapsResolved / clean.TotalDistance : 0;
            // PRINTED, BECAUSE `Check` SWALLOWS ITS DETAIL WHEN IT PASSES — and
            // a bound set against a number nobody has seen is rule 2's whole
            // complaint. The first draft of this line read `< 50.0`, chosen out
            // of the air, and it went green, which is the failure mode exactly:
            // an invented threshold that passes tells you nothing and reads like
            // evidence.
            //
            // THE SWEEP THAT SET IT. Fifteen configurations — 14, 20, 28, 40 and
            // 60 vehicles across three seeds, ten minutes of traffic each,
            // roughly 460km driven in total:
            //
            //     n=14  0 clamps    n=20  0 clamps    n=28  0 clamps
            //     n=40  0 clamps    n=60  0, 0 and 1 clamp over 32.8km
            //
            // The planner does not need the clamp at any density this city
            // reaches. One clamp in 460km is 0.03/km at the single worst
            // configuration, so 2.0/km is roughly sixty times the worst thing
            // ever observed and still small enough to catch a planner that has
            // started leaning on the clamp instead of steering.
            //
            // AND IT DOES NOT EXPLAIN THE SIM. Sixteen sim runs read `gap=0.00`,
            // which is the clamp's exact signature, and nothing here reproduces
            // it — so the difference is something the sim has and this does not:
            // pedestrians stepping into the road, and the player at a wheel. A
            // leader that stops DEAD for somebody is not a leader braking
            // comfortably, which is all `Decide` plans against. That is the next
            // question, and `OverlapsResolved` now travels into the sim verdict
            // so the run can answer it rather than another guess.
            Console.WriteLine($"  .. clamps: {clean.OverlapsResolved} over "
                              + $"{clean.TotalDistance:0}m = {perKm:0.00}/km, "
                              + $"tails behind an edge start: {clean.TailsBehindStart}");

            Check(perKm < 2.0,
                "and the planner keeps the room, rather than the clamp forcing it",
                $"{perKm:0.0} clamps per km over {clean.TotalDistance:0}m");

            // AND THE SENTENCE HAS TO SAY SOMETHING. `TightestGapWhy` is the
            // repair for four runs whose entire failure report was the word
            // `traffic`. Both branches are exercised: a populated road, and one
            // where no two vehicles share an edge.
            clean.TightestGap();
            Check(!string.IsNullOrEmpty(clean.TightestGapWhy) &&
                  clean.TightestGapWhy != "not measured",
                "the tightest pair describes itself after a measurement",
                clean.TightestGapWhy);
            var lonely = new TrafficSim(seed: 5);
            lonely.Populate(1);
            lonely.Step(0.5);
            Check(lonely.TightestGap() > 900 &&
                  lonely.TightestGapWhy.Contains("no two vehicles"),
                "and one vehicle alone reports no measurement rather than clearance",
                lonely.TightestGapWhy);

            // Determinism: the same seed drives the same city. The CI sim and the
            // player's machine must not merely look similar.
            var a1 = new TrafficSim(seed: 3); a1.Populate(12);
            var a2 = new TrafficSim(seed: 3); a2.Populate(12);
            for (int i = 0; i < 200; i++) { a1.Step(0.25); a2.Step(0.25); }
            bool identical = a1.Vehicles.Count == a2.Vehicles.Count;
            for (int i = 0; identical && i < a1.Vehicles.Count; i++)
                identical = Math.Abs(a1.Vehicles[i].X - a2.Vehicles[i].X) < 1e-9
                         && Math.Abs(a1.Vehicles[i].Z - a2.Vehicles[i].Z) < 1e-9;
            Check(identical, "the same seed produces the same traffic, step for step");

            // Frame rate independence: a machine running at 60fps and one
            // stuttering at 10fps must produce the same city, or the CI sim
            // proves nothing about the player's build.
            var fast = new TrafficSim(seed: 5); fast.Populate(12);
            var slow = new TrafficSim(seed: 5); slow.Populate(12);
            for (int i = 0; i < 600; i++) fast.Step(1.0 / 60.0);
            for (int i = 0; i < 100; i++) slow.Step(0.1);
            double drift = 0;
            for (int i = 0; i < fast.Vehicles.Count; i++)
                drift = Math.Max(drift, Math.Abs(fast.Vehicles[i].S - slow.Vehicles[i].S));
            Check(drift < 2.5, "a stuttering machine gets the same traffic as a smooth one", drift.ToString("0.00"));

            // THE DESIGN DECISION, held as a test. A car brakes for a person and
            // never, ever drives through one. Running people over is not in this
            // game — see streets-and-cars-spec.md §5.
            var yield = new TrafficSim(seed: 21);
            yield.Populate(6);
            var driver = yield.Vehicles[0];
            for (int i = 0; i < 40; i++) yield.Step(0.25);   // get them rolling
            driver = yield.Vehicles[0];
            var fa = StreetMap.Node(driver.FromId);
            var fb = StreetMap.Node(driver.ToId);
            double ux = fb.X - fa.X, uz = fb.Z - fa.Z;
            double ulen = Math.Sqrt(ux * ux + uz * uz); ux /= ulen; uz /= ulen;
            // Stand a person eight metres in front of them and do not move.
            double px = driver.X + ux * 8.0, pz = driver.Z + uz * 8.0;
            yield.Hazards.Add(new TrafficSim.Hazard { X = px, Z = pz, R = 0.6 });
            // THE PROPERTY IS "DOES NOT DRIVE THROUGH THEM", NOT "KEEPS 0.9m".
            //
            // This asserted a clearance of 0.9m from a person standing EIGHT
            // metres ahead, and passed for a year because the 26m grid meant
            // a car was always braking for the next junction and never
            // reached its 11 m/s top speed. The topology stretch gave cars
            // room to get there, and a car at 11 m/s needs 11m to stop at
            // 5.5 m/s^2 — so the old assertion now demands physics the sim
            // is right to refuse. A real driver in that situation brakes hard
            // and stops close.
            //
            // What must still hold, and what the game actually promises: the
            // car ENDS STOPPED and never passes the person. Both are checked
            // along the road rather than as a radius, so "stopped just short"
            // and "went through and carried on" cannot read alike.
            double closest = 999, passedBy = 0;
            double startS = yield.Vehicles[0].S;
            double hazardS = startS + 8.0;
            for (int i = 0; i < 100; i++)
            {
                yield.Step(0.1);
                var d = yield.Vehicles[0];
                double gap = Math.Sqrt((d.X - px) * (d.X - px) + (d.Z - pz) * (d.Z - pz));
                if (gap < closest) closest = gap;
                if (d.FromId == driver.FromId && d.ToId == driver.ToId)
                    passedBy = Math.Max(passedBy, d.S - hazardS);
            }
            Check(passedBy <= 0.05, "and never drives past them", passedBy.ToString("0.00"));
            Check(yield.Vehicles[0].Speed < 0.35, "and is stopped when it gets there",
                yield.Vehicles[0].Speed.ToString("0.00"));
            Check(closest > 0.25, "a car stops for somebody in the road rather than driving through them",
                closest.ToString("0.00"));
            Check(yield.Vehicles[0].Speed < 0.5, "and waits there while they stand in it",
                yield.Vehicles[0].Speed.ToString("0.00"));
            Check(yield.YieldsToPeople > 0, "and the sim reports that it yielded");
            yield.Hazards.Clear();
            for (int i = 0; i < 60; i++) yield.Step(0.1);
            Check(yield.Vehicles[0].Speed > 0.5, "and drives on once the road is clear",
                yield.Vehicles[0].Speed.ToString("0.00"));

            // Speed limits by road class: nobody does forty down a lane.
            foreach (var v in sim.Vehicles)
                Check(v.Speed <= Math.Min(v.Kind.TopSpeed, TrafficSim.LimitOf(v.Edge)) + 0.5,
                    $"vehicle {v.Id} keeps to the limit for the road it is on",
                    $"{v.Speed:0.0} on a {v.Edge.Kind}");

            // Witnesses (spec §4): what somebody saw arrive.
            var near = sim.NearestTo(sim.Vehicles[0].X, sim.Vehicles[0].Z, within: 3.0);
            Check(near == sim.Vehicles[0], "you can ask what vehicle was nearest a place");
            Check(sim.NearestTo(9999, 9999) == null, "and nothing was near the far side of nowhere");

            // A stall must not teleport traffic across the city.
            var stall = new TrafficSim(seed: 9); stall.Populate(8);
            for (int i = 0; i < 40; i++) stall.Step(0.25);
            var beforeStall = stall.Vehicles[0].S;
            var edgeBefore = stall.Vehicles[0].Edge;
            stall.Step(30.0);
            bool sane = stall.Vehicles[0].Edge != edgeBefore
                || Math.Abs(stall.Vehicles[0].S - beforeStall) < TrafficSim.SpeedLimitAvenue * 1.5;
            Check(sane, "a thirty-second freeze advances traffic by a second, not by a minute");
            Check(stall.TightestGap() >= 0, "and does not pile anybody into anybody");

            // The street empties overnight. A city with literally no traffic at
            // 4am reads as broken rather than as late, so it thins rather than
            // stops — and the same cars are out at the same hours, because it is
            // by index and not by a roll.
            var hours = new TrafficSim(seed: 13);
            hours.Populate(14);
            Check(TrafficSim.BusynessAt(8) > TrafficSim.BusynessAt(14),
                "the morning is busier than the middle of the day");
            Check(TrafficSim.BusynessAt(18) > TrafficSim.BusynessAt(1),
                "and the evening is busier than the small hours");
            Check(TrafficSim.BusynessAt(4) > 0, "but the small hours are never empty");
            hours.SetHour(8);
            int rush = hours.AwakeCount();
            hours.SetHour(4);
            int night = hours.AwakeCount();
            Check(night < rush && night >= 2, "fewer cars are out at four in the morning",
                $"{night} vs {rush}");
            hours.SetHour(8);
            Check(hours.AwakeCount() == rush, "and the street refills at the same hour every day");
            hours.SetHour(3);
            var parkedIds = new List<int>();
            foreach (var v in hours.Vehicles) if (v.Dormant) parkedIds.Add(v.Id);
            hours.SetHour(8); hours.SetHour(3);
            var again = new List<int>();
            foreach (var v in hours.Vehicles) if (v.Dormant) again.Add(v.Id);
            Check(string.Join(",", parkedIds) == string.Join(",", again),
                "the same cars are parked up at the same hour, so the street has a character");

            // A parked car must not block anybody, and the thinned street must
            // obey every rule the full one does.
            hours.SetHour(3);
            for (int i = 0; i < 200; i++) hours.Step(0.5);
            Check(hours.TightestGap() >= 0, "a thinned street still has nobody inside anybody");
            Check(hours.TotalDistance > 100, "and the few cars still out are still driving",
                hours.TotalDistance.ToString("0"));
            foreach (var v in hours.Vehicles)
                if (v.Dormant) Check(v.Speed == 0, $"parked vehicle {v.Id} is not creeping");

            // Collisions that hurt without killing (player decision 2026-07-27).
            // AI drivers still brake for everybody — an NPC car maiming a
            // pedestrian while the player watches is a consequence with no
            // decision attached. Only the player's car can strike anybody.
            var road = new TrafficSim(seed: 33);
            road.Populate(6);
            road.Hazards.Add(new TrafficSim.Hazard { X = 4, Z = 4, R = 0.5, Id = "Lena", Name = "Lena" });
            Check(road.Contact(4, 4, speed: 0.5, 1.1, 2.3) == null,
                "a car at walking pace does not put anybody in the infirmary");
            var struck = road.Contact(4, 4, speed: 9.0, 1.1, 2.3);
            Check(struck != null && struck.Value.VictimId == "Lena",
                "but at speed it knocks somebody down, and the somebody has a name");
            Check(struck.Value.ByPlayer, "and it was the player at the wheel, which is the only case that matters");
            Check(struck.Value.Force > 0 && struck.Value.Force <= 1,
                "how hard it was is a fraction, not a fatality", struck.Value.Force.ToString("0.00"));
            Check(road.Strikes.Count == 1, "and it is reported for the host to act on");
            Check(road.Contact(40, 40, 9.0, 1.1, 2.3) == null, "missing everybody hits nobody");
            road.Hazards.Add(new TrafficSim.Hazard { X = 9, Z = 9, R = 1.2, Id = road.PlayerHazardId });
            Check(road.Contact(9, 9, 9.0, 1.1, 2.3) == null, "and your own car is not somebody you can run into");
            var anonymous = new TrafficSim(seed: 34);
            anonymous.Hazards.Add(new TrafficSim.Hazard { X = 0, Z = 0, R = 0.5 });
            Check(anonymous.Contact(0, 0, 9.0, 1.1, 2.3) == null,
                "an unnamed obstacle is a bollard, not a person");

            // Force scales with speed and saturates — the top of an arcade speed
            // range is as bad as it ever gets, and it is still not fatal.
            var soft = new TrafficSim(seed: 35);
            soft.Hazards.Add(new TrafficSim.Hazard { X = 0, Z = 0, R = 0.5, Id = "A", Name = "A" });
            var gentle = soft.Contact(0, 0, 3.0, 1.1, 2.3);
            soft.Hazards.Clear();
            soft.Hazards.Add(new TrafficSim.Hazard { X = 0, Z = 0, R = 0.5, Id = "B", Name = "B" });
            var hard = soft.Contact(0, 0, 13.0, 1.1, 2.3);
            Check(gentle.Value.Force < hard.Value.Force, "faster hurts more");
            Check(hard.Value.Force <= 1.0, "and nothing goes past the worst it can be");

            // Zero deltas and empty streets are not crashes.
            var empty = new TrafficSim(seed: 1);
            empty.Step(0.5); empty.Step(0);
            Check(empty.Vehicles.Count == 0 && empty.TotalDistance == 0, "an empty city ticks quietly");
        }

        // ---------------------------------------------------------------
        // Access as soft keys (roadmap M7.5)
        // ---------------------------------------------------------------

        /// The back room at the ferry: four ways in, each costing something else.
        static Gate BackRoom()
        {
            var g = new Gate("backroom", "the back room at the ferry", "Hal's man")
            {
                Refusal = "\"Private tonight,\" he says, and does not move.",
            };
            g.WithKey(new AccessKey(KeyKind.Introduction, who: "Hal"));
            g.WithKey(new AccessKey(KeyKind.Standing, 40, who: "dockside"));
            g.WithKey(new AccessKey(KeyKind.Payment, 60));
            g.WithKey(new AccessKey(KeyKind.Dress, dress: "plain"));
            return g;
        }

        static void TestAccess()
        {
            Console.WriteLine("Access — doors are decisions, not walls:");

            var gate = BackRoom();
            var nobody = new AccessState { Dress = "coat", Money = 10, Hour = 21 };
            var refused = Doors.Try(gate, nobody);
            Check(!refused.Allowed, "somebody with nothing is turned away");
            Check(refused.Line.Contains("Private tonight"), "and it is a person saying so, not a padlock");
            Check(refused.Nearest != null && refused.Hint.Length > 0,
                "and they are told what would have worked");

            // Four ways in, each independently sufficient. This is the law of
            // multiple solutions, enforced structurally rather than remembered.
            var introduced = new AccessState { Dress = "coat", Money = 0, Hour = 21 };
            introduced.Introductions.Add("Hal");
            Check(Doors.Try(gate, introduced).Allowed, "a word from Hal is enough");

            var standing = new AccessState { Dress = "coat", Money = 0, Hour = 21 };
            standing.Standing["dockside"] = 0.5;
            Check(Doors.Try(gate, standing).Allowed, "so is standing with the docks");

            var paying = new AccessState { Dress = "coat", Money = 100, Hour = 21 };
            Check(Doors.Try(gate, paying).Allowed, "so is money");

            var dressed = new AccessState { Dress = "plain", Money = 0, Hour = 21 };
            Check(Doors.Try(gate, dressed).Allowed, "so is simply not looking like a man on a job");

            // The cheapest key held wins. A player holding both an introduction
            // and sixty dollars must not silently spend the sixty dollars.
            var both = new AccessState { Dress = "coat", Money = 100, Hour = 21 };
            both.Introductions.Add("Hal");
            var chose = Doors.Try(gate, both);
            Check(chose.Allowed && chose.Used.Kind == KeyKind.Introduction,
                "a free way in is taken over a costly one", chose.Used.Kind.ToString());
            Check(chose.Paid == 0, "and nothing is spent that did not need spending");

            var mustPay = new AccessState { Dress = "coat", Money = 100, Hour = 21 };
            var paid = Doors.Try(gate, mustPay);
            Check(paid.Allowed && paid.Paid == 60, "when money is the only way in, it is charged");

            // The near miss must be the USEFUL one, not the first one listed.
            var almostPaid = new AccessState { Dress = "coat", Money = 58, Hour = 21 };
            var close = Doors.Try(gate, almostPaid);
            Check(!close.Allowed && close.Nearest.Kind == KeyKind.Payment,
                "the hint names the way in you came closest to", close.Nearest.Kind.ToString());
            Check(close.Hint.Contains("£60") && close.Hint.Contains("£58"),
                "and says the figure and what you actually have", close.Hint);

            var almostStanding = new AccessState { Dress = "coat", Money = 0, Hour = 21 };
            almostStanding.Standing["dockside"] = 0.38;
            var closeStanding = Doors.Try(gate, almostStanding);
            Check(closeStanding.Nearest.Kind == KeyKind.Standing,
                "standing you nearly have beats money you do not have at all",
                closeStanding.Nearest.Kind.ToString());

            // Hours, notoriety and leverage.
            var night = new Gate("cellar", "the cellar", "Rocco");
            night.WithKey(new AccessKey(KeyKind.After, 22));
            Check(!Doors.Try(night, new AccessState { Hour = 20 }).Allowed, "too early is refused");
            Check(Doors.Try(night, new AccessState { Hour = 23 }).Allowed, "late enough is not");

            var quiet = new Gate("parlour", "the parlour");
            quiet.WithKey(new AccessKey(KeyKind.Quiet, 30));
            Check(Doors.Try(quiet, new AccessState { Notoriety = 0.1 }).Allowed,
                "a room that only opens to people nobody is talking about");
            Check(!Doors.Try(quiet, new AccessState { Notoriety = 0.8 }).Allowed,
                "closes once the street is saying your name");

            var known = new Gate("table", "the upstairs table");
            known.WithKey(new AccessKey(KeyKind.Notorious, 50));
            Check(!Doors.Try(known, new AccessState { Notoriety = 0.2 }).Allowed,
                "and some rooms only open to somebody who is already somebody");
            Check(Doors.Try(known, new AccessState { Notoriety = 0.9 }).Allowed,
                "which the same street noise eventually makes you");

            var leaned = new Gate("office", "the office", "the clerk");
            leaned.WithKey(new AccessKey(KeyKind.Hook));
            Check(Doors.Try(leaned, new AccessState { HoldsHookOnDoor = true }).Allowed,
                "something on the man at the door is a key like any other");
            Check(!Doors.Try(leaned, new AccessState()).Allowed, "and having nothing on him is not");

            var mob = new Gate("yard", "the yard");
            mob.WithKey(new AccessKey(KeyKind.Crew, 3));
            Check(Doors.Try(mob, new AccessState { Crew = 4 }).Allowed, "enough people behind you opens a yard");
            var alone = Doors.Try(mob, new AccessState { Crew = 1 });
            Check(!alone.Allowed && alone.Hint.Contains("3"), "and being short is said as a number of people");

            // Design laws, asserted rather than assumed.
            var wall = new Gate("nowhere", "a door with no way through it");
            Check(Doors.Try(wall, new AccessState()).Allowed,
                "a gate with no keys is a design failure, so it simply opens");
            Check(!Doors.Try(null, new AccessState()).Allowed, "and nothing at all is not a door");
            Check(!Doors.Try(gate, null).Allowed, "nor is a player who does not exist");

            // THE SHIPPED GATES, not a fixture. A door in the actual game that
            // nobody can open is a wall, and walls are the one thing this whole
            // system exists in order not to build.
            foreach (var g in Ledger.Game.AccessSetup.Build())
            {
                Check(g.Keys.Count > 0, $"the shipped gate '{g.Id}' has a way in");
                Check(!string.IsNullOrEmpty(g.Doorman), $"'{g.Id}' has somebody standing there");
                Check(!string.IsNullOrEmpty(g.Refusal), $"'{g.Id}' has a refusal in a person's voice");
                foreach (var k in g.Keys)
                    Check(!string.IsNullOrEmpty(k.Opens) && !string.IsNullOrEmpty(k.Nearly),
                        $"every way into '{g.Id}' reads both when it works and when it nearly does");

                // Somebody with nothing at three in the morning: either they get
                // in, or they are told what would have worked. Never neither.
                var pauper = Doors.Try(g, new AccessState { Hour = 3, Dress = "coat", Money = 0 });
                Check(pauper.Allowed || (pauper.Nearest != null && pauper.Hint.Length > 0),
                    $"'{g.Id}' either opens or teaches — it is never simply shut");
            }

            // The pair that makes the system a system: one room closes as you
            // become somebody, the other opens. No build holds both.
            var shipped = Ledger.Game.AccessSetup.Build();
            var loft = shipped.Find(g => g.Id == "laundry");
            var yard = shipped.Find(g => g.Id == "repair_yard");
            var unknown = new AccessState { Notoriety = 0.05, Hour = 22, Money = 0 };
            var famous = new AccessState { Notoriety = 0.9, Hour = 22, Money = 0 };
            Check(Doors.Try(loft, unknown).Allowed, "the quiet loft opens to somebody nobody has heard of");
            Check(!Doors.Try(loft, new AccessState { Notoriety = 0.9, Hour = 12, Money = 0 }).Allowed,
                "and closes once the street is saying your name");
            Check(Doors.Try(yard, famous).Allowed, "the yard opens to somebody the street talks about");
            // ...and it is the NOTORIETY that opens it: at noon the after-hours
            // key is dead, so this passes only through the Notorious key — the
            // old check passed via Hour 22 whatever the notoriety was (audit
            // 2026-07-27).
            Check(Doors.Try(yard, new AccessState { Notoriety = 0.9, Hour = 12, Money = 0 }).Allowed,
                "and it is the name that opens it, not the hour");
            Check(!Doors.Try(yard, new AccessState { Notoriety = 0.05, Hour = 12, Money = 0 }).Allowed,
                "a nobody at noon stays outside");

            // Every refusal must be legible: somebody talking, and never a code.
            foreach (var state in new[] { nobody, almostPaid, almostStanding })
            {
                var r = Doors.Try(gate, state);
                Check(!r.Line.Contains("DENIED") && !r.Line.Contains("_") && r.Line.Length > 8,
                    "a refusal is always somebody talking", r.Line);
                Check(r.Hint.Length > 0, "and always teaches you something", r.Hint);
            }
        }

        // ---------------------------------------------------------------
        // Operation planning (roadmap M7.5)
        // ---------------------------------------------------------------

        static OperationTarget Warehouse() => new OperationTarget
        {
            Id = "ironside_shed", Name = "the Ironside shed", PlaceId = "ironside",
            Difficulty = 0.5, Payout = 300, Exposure = 0.5,
        };

        static OperationState Steady()
        {
            var s = new OperationState { Heat = 0.2, Nerve = 0.5, Coated = true };
            s.Competence["Sam"] = 0.6;  s.Loyalty["Sam"] = 0.8;
            s.Competence["Joey"] = 0.7; s.Loyalty["Joey"] = 0.7;
            s.Competence["Ada"] = 0.15;  s.Loyalty["Ada"] = 0.9;
            return s;
        }

        /// A fixed sequence, so a test asserts the RULES rather than a lucky roll.
        static Func<double> Rolls(params double[] values)
        {
            int i = 0;
            return () => values[Math.Min(i++, values.Length - 1)];
        }

        static void TestOperations()
        {
            Console.WriteLine("Operations — deciding beforehand, and living with it:");

            var state = Steady();

            // Every one of the four decisions must move the read, or it is not a
            // decision. Checked against the internal number the player never sees.
            double baseline = Operations.Read(new OperationPlan("x") { Approach = Approach.Quiet, Hour = 23 },
                Warehouse(), state).Risk;

            double forced = Operations.Read(new OperationPlan("x") { Approach = Approach.Forced, Hour = 23 },
                Warehouse(), state).Risk;
            Check(forced < baseline, "forcing it is more likely to work than doing it quietly");

            double withHands = Operations.Read(
                new OperationPlan("x") { Approach = Approach.Quiet, Hour = 23 }.Bringing("Joey"),
                Warehouse(), state).Risk;
            Check(withHands < baseline, "bringing a competent man helps");

            double withAda = Operations.Read(
                new OperationPlan("x") { Approach = Approach.Quiet, Hour = 23 }.Bringing("Ada"),
                Warehouse(), state).Risk;
            Check(withAda > baseline, "bringing somebody who has never done this is worse than going alone");

            double withTools = Operations.Read(new OperationPlan("x") { Tools = true, Hour = 23 },
                Warehouse(), state).Risk;
            Check(withTools < baseline, "tools help");

            // The trade that makes it a decision rather than an optimum: forcing
            // it is likelier to work AND likelier to be seen.
            var quietRead = Operations.Read(new OperationPlan("x") { Approach = Approach.Quiet, Hour = 23 }, Warehouse(), state);
            var forcedRead = Operations.Read(new OperationPlan("x") { Approach = Approach.Forced, Hour = 23 }, Warehouse(), state);
            Check(forcedRead.Visibility > quietRead.Visibility,
                "and forcing it is much more likely to be seen — the whole trade");

            // The hour is a real choice in both directions.
            Check(Operations.HourDensity(3) < Operations.HourDensity(20),
                "three in the morning is emptier than eight at night");
            Check(Operations.HourDensity(12) > Operations.HourDensity(23),
                "and the middle of the day is the worst time to be anywhere");
            var noon = Operations.Read(new OperationPlan("x") { Hour = 12 }, Warehouse(), state);
            var night = Operations.Read(new OperationPlan("x") { Hour = 23 }, Warehouse(), state);
            Check(noon.Visibility > night.Visibility, "so going at noon is seen more than going at eleven");

            // Talking your way in is free until the street knows your name.
            var quietStreet = new OperationState { Heat = 0.05, Nerve = 0.5 };
            var loudStreet = new OperationState { Heat = 0.9, Nerve = 0.5 };
            Check(Operations.Read(new OperationPlan("x") { Approach = Approach.Social }, Warehouse(), quietStreet).Risk
                < Operations.Read(new OperationPlan("x") { Approach = Approach.Social }, Warehouse(), loudStreet).Risk,
                "talking your way in stops working once people have heard of you");

            // The coat is worth something here too.
            var bare = Steady(); bare.Coated = false;
            Check(Operations.Read(new OperationPlan("x") { Hour = 23 }, Warehouse(), bare).Visibility
                > Operations.Read(new OperationPlan("x") { Hour = 23 }, Warehouse(), Steady()).Visibility,
                "the coat is worth something on a job, not only afterwards");

            // THE APPROVED DECISION: qualitative odds, never a percentage.
            for (double r = 0; r <= 1.0001; r += 0.05)
            {
                var word = Operations.RiskWord(r);
                Check(!word.Contains("%") && !word.Any(char.IsDigit),
                    "a plan is read in words and never in numbers", word);
            }
            Check(Operations.RiskWord(0.1) != Operations.RiskWord(0.9),
                "and the words actually distinguish a good plan from a bad one");

            // The read must teach: name the decision most worth changing.
            var talky = Operations.Read(new OperationPlan("x") { Approach = Approach.Social }, Warehouse(),
                new OperationState { Heat = 0.8, Nerve = 0.5 });
            Check(talky.Worry.Contains("heard of you"), "a bad approach is named as the problem", talky.Worry);
            var daylight = Operations.Read(new OperationPlan("x") { Approach = Approach.Forced, Hour = 12 }, Warehouse(), bare);
            Check(daylight.Worry.Contains("daylight"), "so is a bad hour", daylight.Worry);
            var crowded = Operations.Read(
                new OperationPlan("x") { Hour = 3 }.Bringing("Sam", "Joey", "Ada", "Sam"), Warehouse(), Steady());
            Check(crowded.Worry.Contains("Four people"),
                "and a plan with too many people in it names the crowd as the problem", crowded.Worry);

            // Running it. Three bands, and the partial is the interesting one.
            var win = Operations.Run(new OperationPlan("x") { Approach = Approach.Forced, Hour = 3 },
                Warehouse(), Steady(), Rolls(0.99, 0.0, 0.0, 0.0));
            Check(win.Success && win.Take == 300, "a good roll on a good plan pays out in full");

            var target = Warehouse();
            var messy = Operations.Run(new OperationPlan("x") { Hour = 3 }, target, Steady(), Rolls(0.5, 0.0, 0.0));
            Check(messy.Partial && messy.Take > 0 && messy.Take < 300,
                "and the middle band gets you most of the way, which is the interesting outcome",
                messy.Take.ToString());
            Check(target.Done, "a job you half-did is still done — there is no second attempt at the same shed");

            var flop = Warehouse();
            double before = flop.Difficulty;
            var lost = Operations.Run(new OperationPlan("x") { Hour = 3 }, flop, Steady(), Rolls(0.0, 0.0, 0.0));
            Check(!lost.Success && !lost.Partial && lost.Take == 0, "a bad roll gets you nothing");
            Check(!flop.Done, "a failure leaves the job there");
            Check(flop.Difficulty > before, "harder than it was, which is a consequence and not a punishment");

            // Failing is loud: more people see a botched job than a clean one.
            var seenWin = Operations.Run(new OperationPlan("x") { Approach = Approach.Forced, Hour = 12 },
                Warehouse(), bare, Rolls(0.99, 0.99, 0.0, 0.0));
            var seenLoss = Operations.Run(new OperationPlan("x") { Approach = Approach.Forced, Hour = 12 },
                Warehouse(), bare, Rolls(0.0, 0.99, 0.0, 0.0));
            Check(seenLoss.Witnesses > seenWin.Witnesses, "a botched job is seen by more people than a clean one",
                $"{seenLoss.Witnesses} vs {seenWin.Witnesses}");

            // Your own people talk, and loyalty is what decides whether they do.
            var disloyal = Steady();
            disloyal.Loyalty["Sam"] = 0.0;
            var talked = Operations.Run(new OperationPlan("x").Bringing("Sam"), Warehouse(), disloyal,
                Rolls(0.0, 0.0, 0.1));
            Check(talked.Talkers.Contains("Sam"), "a frightened man with no reason to protect you talks afterwards");
            var loyal = Steady();
            loyal.Loyalty["Sam"] = 1.0;
            var quiet = Operations.Run(new OperationPlan("x").Bringing("Sam"), Warehouse(), loyal,
                Rolls(0.99, 0.0, 0.9));
            Check(quiet.Talkers.Count == 0, "and a loyal one on a clean job does not");

            // THE SHIPPED TARGETS. Three jobs are only worth having if each
            // one wants a DIFFERENT plan — otherwise it is one job listed three
            // times, and the panel is a menu rather than a decision.
            var board = Ledger.Game.OperationSetup.Build();
            Check(board.Count >= 3, "there are jobs on the board");
            Check(board.Select(t => t.Id).Distinct().Count() == board.Count, "and no two are the same job");
            foreach (var t in board)
            {
                Check(!string.IsNullOrEmpty(t.Name) && !string.IsNullOrEmpty(t.PlaceId),
                    $"'{t.Id}' is somewhere real with a name");
                Check(Ledger.Core.HookMap.Get(t.PlaceId) != null,
                    $"'{t.Id}' happens at a place that exists on the map");
                Check(t.Payout > 0 && t.Difficulty > 0 && t.Difficulty < 1, $"'{t.Id}' is worth doing and possible");
            }

            // The best plan must not be the same plan for all three. Sweep the
            // approaches and hours and check the boards disagree about what the
            // safest option is — that disagreement IS the content.
            string BestPlanFor(OperationTarget t)
            {
                var st = Steady();
                var options = new List<(string label, double risk)>();
                foreach (Approach ap in new[] { Approach.Quiet, Approach.Forced, Approach.Social })
                    foreach (int hr in new[] { 3, 12, 19, 23 })
                        options.Add(($"{ap}@{hr}",
                            Operations.Read(new OperationPlan(t.Id) { Approach = ap, Hour = hr }, t, st).Risk
                            + Operations.Read(new OperationPlan(t.Id) { Approach = ap, Hour = hr }, t, st).Visibility));
                return options.OrderBy(o => o.risk).First().label;
            }
            var bests = board.Select(BestPlanFor).ToList();
            Check(bests.Distinct().Count() > 1,
                "the three jobs do not all want the same plan — that difference is the content",
                string.Join(" / ", bests));

            // The warehouse row is the safest and the worst-paid on purpose:
            // going back to the place that burned should never be about money.
            var row = board.First(t => t.Id == "warehouse_row");
            Check(row.Exposure == board.Min(t => t.Exposure), "the warehouse row is the least overlooked place on the board");
            Check(row.Payout == board.Min(t => t.Payout), "and pays the worst, so going back there is never about money");

            // Degenerate inputs, since this runs off player choices.
            Check(Operations.Read(null, null, null).Risk >= 1, "an empty plan is not a plan");
            Check(!Operations.Run(null, null, null, null).Success, "and cannot be run");
            var done = Warehouse(); done.Done = true;
            Check(Operations.Read(new OperationPlan("x"), done, Steady()).Line.Contains("already"),
                "a finished job says so rather than offering itself again");
            Check(!Operations.Run(new OperationPlan("x"), done, Steady(), Rolls(0.99)).Success,
                "and cannot be done twice");
        }

        // ---------------------------------------------------------------
        // Population at district scale (roadmap M9)
        // ---------------------------------------------------------------

        static readonly string[] Districts = { "the Hook", "Copper Row", "Ironside" };

        static void TestPopulation()
        {
            Console.WriteLine("Population — the city stops being 36 people:");

            var sw = System.Diagnostics.Stopwatch.StartNew();
            var pop = Population.Generate(3000, 20260726, Districts);
            sw.Stop();
            Check(pop.Residents.Count == 3000, "three thousand people exist");
            Check(sw.ElapsedMilliseconds < 500, "and generating them is not something you would notice",
                sw.ElapsedMilliseconds + "ms");

            // Determinism is not a nicety here: it is what lets a save file store
            // a seed instead of ten thousand people.
            var twin = Population.Generate(3000, 20260726, Districts);
            Check(twin.Residents[1500].Name == pop.Residents[1500].Name
                  && twin.Residents[1500].Trade == pop.Residents[1500].Trade
                  && twin.Residents[1500].HomeX == pop.Residents[1500].HomeX,
                "the same seed always builds the same city");
            var other = Population.Generate(3000, 7, Districts);
            Check(other.Residents[1500].Name != pop.Residents[1500].Name
                  || other.Residents[1500].Trade != pop.Residents[1500].Trade,
                "and a different seed builds a different one");

            Check(pop.Residents.All(r => !string.IsNullOrEmpty(r.Name) && r.Name.Contains(" ")),
                "everybody has a name");
            Check(pop.Residents.Select(r => r.Name).Distinct().Count() > 1000,
                "and the street is not full of one family",
                pop.Residents.Select(r => r.Name).Distinct().Count().ToString());
            Check(Districts.All(d => pop.Residents.Any(r => r.District == d)), "every district is populated");
            Check(pop.Residents.Any(r => r.Circle == "night") && pop.Residents.Any(r => r.Circle == "day"),
                "and the city has a night shift as well as a day one");

            // Level of detail. Almost nobody is simulated, and the caps hold.
            var loadBearing = new HashSet<string>();
            double DistanceFromOrigin(Resident r) => Math.Sqrt(r.HomeX * r.HomeX + r.HomeZ * r.HomeZ);
            pop.SetBands(DistanceFromOrigin, loadBearing);
            Check(pop.CountIn(Lod.Near) == pop.NearCap, "only a capped few have a body and a brain");
            Check(pop.CountIn(Lod.Mid) == pop.MidCap, "a larger band carries talk without rendering");
            Check(pop.CountIn(Lod.Far) == 3000 - pop.NearCap - pop.MidCap, "and the rest are records");

            // Only what changed is reported, so the game spawns and despawns
            // exactly those and nothing else.
            var again = pop.SetBands(DistanceFromOrigin, loadBearing);
            Check(again.Count == 0, "standing still changes nobody's band");

            // A CEILING, NOT JUST A QUOTA (playtest 2026-07-28). Band assignment
            // was pure rank, so the nearest N always got bodies however far away
            // they were: walk into an empty quarter and the crowd materialised
            // around you. Out in the fields, nobody is near enough to render.
            var empty = pop.SetBands(r => 5000.0, loadBearing);
            Check(pop.CountIn(Lod.Near) == 0,
                "an empty horizon spawns nobody, whatever the cap allows", pop.CountIn(Lod.Near).ToString());
            Check(empty.Count > 0, "and the people who had bodies are told to put them away");

            // Most people are INDOORS. The street is a handful of walkers, not
            // the whole population standing on the pavement.
            int outAtNoon = 0, outAtThree = 0;
            foreach (var r in pop.Residents)
            {
                if (Population.OutdoorsAt(r, 0, 13)) outAtNoon++;
                if (Population.OutdoorsAt(r, 0, 3)) outAtThree++;
            }
            Check(outAtNoon < pop.Residents.Count / 3,
                "most of the city is indoors at any hour", $"{outAtNoon} of {pop.Residents.Count} out at one o'clock");
            Check(outAtThree < outAtNoon / 2,
                "and the small hours belong to far fewer", $"{outAtThree} out at three in the morning");
            var someone = pop.Residents[42];
            Check(Population.OutdoorsAt(someone, 0, 13) == Population.OutdoorsAt(someone, 0, 13),
                "whether somebody is out is stable, not a coin flipped every frame");

            // DAYS THAT DIFFER, which this model did not have until the routine
            // took a day at all. It reduced the hour mod 24 and nothing else, so
            // every Tuesday in this town was every Saturday — and the fault
            // surfaced as arithmetic rather than as a complaint: `Recurrence`
            // looped a week, every column came out identical, and 86% of
            // encounters read as "repeat", which is exactly 6/7.
            Check(!Population.IsRestDay(0) && !Population.IsRestDay(4)
                  && Population.IsRestDay(5) && Population.IsRestDay(6),
                "day 0 is a Monday, so 5 and 6 are the rest days");

            // WHO is out has to change, or the day parameter is decoration.
            // Counted as a disagreement rather than as two totals, because two
            // days with the same NUMBER of people out and the same PEOPLE out
            // is exactly the failure being guarded against.
            int differs = 0;
            foreach (var r in pop.Residents)
                if (Population.OutdoorsAt(r, 1, 13) != Population.OutdoorsAt(r, 2, 13)) differs++;
            Check(differs > pop.Residents.Count / 40,
                "a different set of people is outdoors on a different day",
                $"{differs} of {pop.Residents.Count} differ between two working days at one o'clock");

            // And WHEN, on a rest day: no commute, so eight in the morning is
            // quiet and the middle of the day is thicker. Compared against the
            // working day rather than against a threshold — the claim is a
            // RELATION between two days and stating it as one is what keeps it
            // honest when the rates are next retuned.
            int workRush = 0, restRush = 0, workNoon = 0, restNoon = 0;
            foreach (var r in pop.Residents)
            {
                if (Population.OutdoorsAt(r, 0, 8)) workRush++;
                if (Population.OutdoorsAt(r, 5, 8)) restRush++;
                if (Population.OutdoorsAt(r, 0, 14)) workNoon++;
                if (Population.OutdoorsAt(r, 5, 14)) restNoon++;
            }
            Check(restRush < workRush,
                "nobody commutes on a rest day, so eight in the morning is quieter",
                $"working {workRush} vs rest {restRush}");
            Check(restNoon > workNoon,
                "and the middle of a free day is busier than the middle of a working one",
                $"working {workNoon} vs rest {restNoon}");

            // A DAY IS STILL DETERMINISTIC. The whole point of the seeded model
            // is that the player can leave a street and come back to the same
            // world; adding a dimension to the hash must not cost that.
            Check(Population.OutdoorsAt(someone, 3, 13) == Population.OutdoorsAt(someone, 3, 13),
                "a given day is as stable as a given hour was");

            // THE CITY TABLE, WHICH USED TO BE TWO TABLES AND ONE FALSE PROMISE.
            // `Recurrence` carried a copy of the districts and shares under a
            // comment saying that if they drifted the tool would be measuring a
            // city the game does not build, "so they are asserted below" — and
            // there was no assertion anywhere in that file. Both are `CityPlan`
            // now, so drift cannot happen; this checks the remaining hand-edit
            // hazard, which is a district appended to one array and not the
            // others, silently shifting every share after it onto the wrong
            // place.
            // NARRATION, FROM THE TRANSCRIPT THAT FOUND IT. The real failure
            // was "Sam squints at that like you've asked him to fly" — a reply
            // that is prose about a character rather than a character talking.
            Check(ResponseValidator.ReadsAsNarration(
                      "Sam squints at that like you've asked him to fly.", "Sam"),
                "a character narrating themselves is caught");
            Check(!ResponseValidator.ReadsAsNarration(
                      "Sam's the one you want, not me.", "Rocco"),
                "talking ABOUT somebody else is not narration");
            Check(!ResponseValidator.ReadsAsNarration(
                      "Sam, you're not listening.", "Sam"),
                "a name followed by a comma is address, not narration");
            Check(!ResponseValidator.ReadsAsNarration(
                      "Sam? Never heard of him.", "Sam"),
                "a name followed by a question mark is not narration");

            // THE ONE THAT GOT THROUGH, VERBATIM FROM THE 5 AUGUST TRANSCRIPT.
            // The guard tested the first token of `Name` only, Ada's card is
            // headed "# Ada", and the model narrated her as "Mrs Vane" — a name
            // the card gives her ("You will call me Mrs Vane") and the guard had
            // never been handed.
            var vane = new List<string> { "Mrs Vane", "Vane" };
            Check(ResponseValidator.ReadsAsNarration(
                      "Mrs Vane looks you over the way she'd size up a new face at the back of a classroom.",
                      "Ada", vane),
                "a character narrating themselves by a name off their card is caught");
            Check(ResponseValidator.ReadsAsNarration(
                      "Vane considers that for a moment.", "Ada", vane),
                "the bare surname is the same fault with the honorific dropped");

            // AND THE CASE IT MUST PASS, which is the half rule 5b says goes
            // unrun. The self-name set is PER CHARACTER, so the identical
            // sentence out of somebody else's mouth is ordinary gossip and must
            // survive — widening the guard is only safe because of this.
            Check(!ResponseValidator.ReadsAsNarration(
                      "Mrs Vane looks you over the way she'd size up a new face at the back of a classroom.",
                      "Rocco"),
                "the same sentence from another speaker is talk about a third party");
            Check(!ResponseValidator.ReadsAsNarration(
                      "Sammy grins like he knows something.", "Sam"),
                "a longer name that merely starts with the speaker's is not narration");
            Check(ResponseValidator.IsDeflection(ResponseValidator.Validate(
                      "Mrs Vane looks you over.", "Ada", vane), "Ada"),
                "Validate deflects the narration it is handed the names for");

            // THE HARVEST ITSELF, on the real card text rather than a fixture.
            var adaNames = new List<string>();
            CharacterCard.HarvestCalledNames(
                "- \"You will call me Mrs Vane or you will call me nothing at all.\"", adaNames);
            Check(adaNames.Contains("Mrs Vane") && adaNames.Contains("Vane"),
                "the card line yields the name the character goes by");
            Check(!adaNames.Contains("Nothing") && adaNames.Count == 2,
                "\"call me nothing at all\" in the same sentence yields no name");

            // NEGOTIATION HAS A CALLER AT LAST — M19's verb, written complete
            // and tested and never once executed. These test the CALL SITE,
            // not the maths: `Negotiation` already has its own tests and they
            // all passed while nothing ran.
            {
                var eb = new EmpireBook();
                var gm = new GossipMill(new SocialGraph());
                var now = new GameTime(3, 12, 0);

                // A MET NEED RECRUITS SOMEBODY WHO HALF-TRUSTS YOU — the
                // accepting case, per rule 5b, and the one that goes unrun.
                var willing = new Gossiper("willing", "Willing", new MemoryStore("willing"), new KnowledgeBase(), new SuspicionTracker(), "day", 0.5, 0.5, 0.6);
                var got = eb.Negotiate(willing, EmpireBook.RecruitAsk,
                    new[] { (Lever.Need, 1.0, true) }, now, gm);
                Check(got.Agreed && eb.CrewOf("willing") != null,
                    "a met need recruits somebody who already half-trusts you");

                // AND THE COST IS PAID EITHER WAY. A threat can win the room
                // and still take the loyalty with it — the whole design claim,
                // and the thing two booleans could not express.
                var scared = new Gossiper("scared", "Scared", new MemoryStore("scared"), new KnowledgeBase(), new SuspicionTracker(), "day", 0.5, 0.1, 0.6);
                double before = scared.Loyalty;
                var bullied = eb.Negotiate(scared, EmpireBook.RecruitAsk,
                    new[] { (Lever.Threat, 1.0, true) }, now, gm);
                Check(scared.Loyalty < before,
                    "threatening somebody costs loyalty whether or not it worked");
                Check(!bullied.Agreed || eb.CrewOf("scared")?.Route == "threat",
                    "a recruit remembers which lever actually moved them");

                // WALKING OUT IS REAL, and it must not enlist anybody.
                var proud = new Gossiper("proud", "Proud", new MemoryStore("proud"), new KnowledgeBase(), new SuspicionTracker(), "day", 0.5, 0.9, 0.5);
                var walked = eb.Negotiate(proud, EmpireBook.RecruitAsk,
                    new[] { (Lever.Threat, 1.0, true), (Lever.Threat, 1.0, true) }, now, gm);
                Check(walked.Walked && eb.CrewOf("proud") == null,
                    "two hard threats end the conversation and recruit nobody");
                Check(walked.Why != "still talking",
                    "a settled negotiation says why, in words rather than a number");

                // NOBODY THERE IS NOT A CRASH.
                var nobodyThere = eb.Negotiate(null, EmpireBook.RecruitAsk, null, now, gm);
                Check(nobodyThere != null && !nobodyThere.Agreed,
                    "negotiating with nobody returns a refusal rather than throwing");

                Check(EmpireBook.RecruitAsk > 0 && EmpireBook.RecruitAsk < 1,
                    "the recruit ask is one number on Negotiation's own scale");
            }

            Check(CityPlan.Balanced,
                "the city's districts and its home/work shares are the same length and total 100",
                $"{CityPlan.Districts.Length} districts, "
                + $"home {CityPlan.HomeShares.Sum()}, work {CityPlan.WorkShares.Sum()}");
            Check(CityPlan.KeepThree.All(i => i >= 0 && i < CityPlan.Districts.Length)
                  && CityPlan.KeepTwo.All(i => i >= 0 && i < CityPlan.Districts.Length),
                "the district subsets index districts that exist");

            // AND THE WALK DIFFERS TOO, which is the subtler half. A different
            // set of people outdoors, every one of them walking the identical
            // route in the identical direction as yesterday, would change who is
            // out while leaving the street looking the same.
            int routeDiffers = 0;
            foreach (var r in pop.Residents)
            {
                bool a = Population.OutdoorPosition(r, 1, 13, out var ax, out _);
                bool b = Population.OutdoorPosition(r, 2, 13, out var bx, out _);
                if (a && b && Math.Abs(ax - bx) > 0.5) routeDiffers++;
            }
            Check(routeDiffers > 0,
                "and somebody out on both days is not always at the same point of the same walk",
                $"{routeDiffers} residents stand somewhere else");

            // With an unstable sort, people at equal distance can swap places
            // and be reported as having changed when nothing about them did —
            // the game would despawn and respawn them forever. Force a heap of
            // exact ties and check the ordering is total.
            var tied = Population.Generate(400, 5, Districts);
            var none = new HashSet<string>();
            tied.SetBands(r => 1.0, none);                       // everybody equidistant
            for (int pass = 0; pass < 4; pass++)
                Check(tied.SetBands(r => 1.0, none).Count == 0,
                    "a street where everyone is equally close does not churn");

            // The rule that outranks the caps.
            var farAway = pop.Residents.OrderByDescending(DistanceFromOrigin).First();
            Check(farAway.Band == Lod.Far, "somebody across the city is a record");
            farAway.Known = true;
            pop.SetBands(DistanceFromOrigin, loadBearing);
            Check(farAway.Band >= Lod.Mid,
                "but somebody the player has actually met is never dropped back to one");

            var crew = pop.Residents.OrderByDescending(DistanceFromOrigin).Skip(1).First();
            loadBearing.Add(crew.Id);
            pop.SetBands(DistanceFromOrigin, loadBearing);
            Check(crew.Band >= Lod.Mid, "and neither is anyone load-bearing, however far away they are");

            // Walking somewhere new re-bands around the new position.
            var corner = pop.Residents.OrderBy(r => r.HomeX).First();
            pop.SetBands(r => Math.Abs(r.HomeX - corner.HomeX) + Math.Abs(r.HomeZ - corner.HomeZ), loadBearing);
            Check(corner.Band == Lod.Near, "walking somewhere makes the people there real");
            Check(pop.CountIn(Lod.Near) == pop.NearCap, "and the cap still holds after moving");
            Check(farAway.Band >= Lod.Mid && crew.Band >= Lod.Mid, "and the people who matter are still not records");

            // The statistical band, which answers exactly one question.
            Check(Population.AmbientReach(0.0, 10) == 0, "a street with no talk has nothing to have heard");
            Check(Population.AmbientReach(0.8, 0) == 0, "and talk that started today has reached nobody yet");
            Check(Population.AmbientReach(0.8, 3) > Population.AmbientReach(0.8, 1),
                "talk reaches further the longer it circulates");
            Check(Population.AmbientReach(0.8, 3) > Population.AmbientReach(0.3, 3),
                "and further when the street is louder");
            Check(Population.AmbientReach(1.0, 500) <= Population.AmbientCeiling,
                "but never reaches everybody, because some people do not listen");

            // Promotion must be consistent between visits. Walking away and
            // coming back cannot re-roll what the neighbourhood remembers.
            double reach = Population.AmbientReach(0.7, 5);
            var sample = pop.Residents.Take(400).ToList();
            var firstVisit = sample.Select(r => Population.HeardIt(r, reach)).ToList();
            var secondVisit = sample.Select(r => Population.HeardIt(r, reach)).ToList();
            Check(firstVisit.SequenceEqual(secondVisit), "who had heard it does not change between visits");
            int heard = firstVisit.Count(h => h);
            Check(heard > 0 && heard < sample.Count, "some of them had heard it and some had not");
            Check(Math.Abs(heard / (double)sample.Count - reach) < 0.08,
                "and about as many as the district's reach says should have",
                $"{heard}/{sample.Count} vs {reach:0.00}");
            Check(!Population.HeardIt(pop.Residents[0], 0), "nobody has heard a story that isn't circulating");
            Check(Population.HeardIt(pop.Residents[0], 1.0), "and everybody has heard one that is everywhere");

            // Persistence: a seed and the exceptions, not ten thousand people.
            var saved = pop.Capture(3000, 20260726);
            var json = MiniJson.Serialize(saved);
            Check(json.Length < 4000, "the whole city saves in a few hundred bytes", json.Length + " bytes");
            var reloaded = Population.Generate(3000, 20260726, Districts);
            reloaded.RestoreKnown(MiniJson.AsObject(MiniJson.Deserialize(json)));
            Check(reloaded.ById(farAway.Id).Known, "somebody the player met is still met after a reload");
            Check(reloaded.ById(farAway.Id).Band >= Lod.Mid, "and comes back at a band that keeps their state");
            Check(reloaded.Residents.Count(r => r.Known) == pop.Residents.Count(r => r.Known),
                "and exactly the people who were met, no more");
            reloaded.RestoreKnown(MiniJson.AsObject(MiniJson.Deserialize("{\"known\":[]}")));
            Check(reloaded.Residents.Count(r => r.Known) == 0, "a save where nobody was met restores a city of strangers");
            reloaded.ById(farAway.Id).Known = true;
            reloaded.RestoreKnown(null);
            Check(reloaded.ById(farAway.Id).Known,
                "but a MISSING population block leaves the city alone rather than wiping it");

            // Degenerate inputs must not throw — this runs at startup.
            Check(Population.Generate(0, 1, Districts).Residents.Count == 0, "a city of nobody is empty, not broken");
            Check(Population.Generate(10, 1, null).Residents.Count == 0, "and a city with no districts is too");
            Check(new Population().SetBands(null, null).Count == 0, "banding with nothing to measure changes nothing");
        }

        // ---------------------------------------------------------------
        // The Director (roadmap M8)
        // ---------------------------------------------------------------

        static WorldSnapshot SampleWorld(int day = 12)
        {
            var w = new WorldSnapshot { Day = day, Heat = 0.5, Street = "tight, prices up" };
            w.People.Add(new WorldPerson("Lena", "bookkeeper", 0.6, 0.55, "counts money she can't explain"));
            w.People.Add(new WorldPerson("Sam", "crew", 0.35, 0.2, "has been skimmed three weeks running"));
            w.People.Add(new WorldPerson("Mitch", "supplier", 0.4, 0.1, "owed for two deliveries"));
            w.People.Add(new WorldPerson("Sera Kest", "rival head", 0.1, 0.6));
            w.Ignored.Add("Mitch has not been paid since day 4");
            w.Recent.Add("the collection round paid out every night this week");
            return w;
        }

        static void TestFeel()
        {
            Console.WriteLine("Feel — momentum, camera lag, and the limp:");

            // ---- momentum: you accelerate, you do not teleport ----
            var loc = new Locomotion();
            loc.Step(0, 1, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(loc.Speed > 0.01 && loc.Speed < Locomotion.WalkSpeed * 0.5,
                "one frame of full input does not reach walking speed",
                $"speed {loc.Speed:0.00} after 16ms");

            for (int i = 0; i < 60; i++) loc.Step(0, 1, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(Math.Abs(loc.Speed - Locomotion.WalkSpeed) < 0.01,
                "a second of input reaches walking speed", $"speed {loc.Speed:0.000}");

            double peak = 0;
            var accel = new Locomotion();
            for (int i = 0; i < 300; i++)
            {
                accel.Step(0, 1, Locomotion.WalkSpeed, 1.0 / 60.0);
                peak = Math.Max(peak, accel.Speed);
            }
            Check(peak <= Locomotion.WalkSpeed + 1e-9,
                "acceleration from rest never overshoots the top speed", $"peak {peak:0.0000}");

            // ---- and you settle out of a stop ----
            loc.Step(0, 0, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(loc.Speed > 0.1, "letting go does not stop you dead", $"speed {loc.Speed:0.00}");
            double before = loc.Speed;
            for (int i = 0; i < 60; i++) loc.Step(0, 0, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(loc.Speed == 0, "but you do come to a complete stop", $"from {before:0.00}");
            Check(loc.Decel > loc.Accel, "stopping is quicker than starting, as bodies are");

            // ---- reversal costs a moment ----
            var rev = new Locomotion();
            for (int i = 0; i < 60; i++) rev.Step(0, 1, Locomotion.RunSpeed, 1.0 / 60.0);
            double atSpeed = rev.Speed;
            bool passedThroughZero = false;
            for (int i = 0; i < 60; i++)
            {
                rev.Step(0, -1, Locomotion.RunSpeed, 1.0 / 60.0);
                if (rev.Speed < atSpeed * 0.15) passedThroughZero = true;
            }
            Check(passedThroughZero,
                "a full reversal passes through a stop rather than mirroring instantly");

            // ---- a body cannot pivot instantly ----
            var turn = new Locomotion { FacingDegrees = 0 };
            turn.Step(0, -1, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(Math.Abs(Feel.DeltaAngle(turn.FacingDegrees, 180)) > 150,
                "one frame turns only a fraction of a 180", $"facing {turn.FacingDegrees:0.0}");
            for (int i = 0; i < 60; i++) turn.Step(0, -1, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(Math.Abs(Feel.DeltaAngle(turn.FacingDegrees, 180)) < 0.001,
                "and arrives exactly, without spinning past", $"facing {turn.FacingDegrees:0.000}");

            Check(Math.Abs(Feel.DeltaAngle(350, 10) - 20) < 1e-9,
                "turning takes the short way round the wrap point",
                $"{Feel.DeltaAngle(350, 10)}");
            Check(Math.Abs(Feel.MoveTowardsAngle(350, 10, 5) - 355) < 1e-9,
                "a limited turn across the wrap point still goes the short way");

            // ---- frame-rate independence: the whole point of doing this in maths ----
            var slow = new Locomotion();
            var fast = new Locomotion();
            for (int i = 0; i < 30; i++) slow.Step(0.7, 0.7, Locomotion.RunSpeed, 1.0 / 30.0);
            for (int i = 0; i < 240; i++) fast.Step(0.7, 0.7, Locomotion.RunSpeed, 1.0 / 240.0);
            Check(Math.Abs(slow.Speed - fast.Speed) < 1e-9,
                "the same second of input gives the same speed at 30fps and 240fps",
                $"{slow.Speed:0.000000} vs {fast.Speed:0.000000}");

            double a30 = Feel.Approach(0, 1, 9, 1.0 / 30.0);
            double a240 = 0;
            for (int i = 0; i < 8; i++) a240 = Feel.Approach(a240, 1, 9, 1.0 / 240.0);
            Check(Math.Abs(a30 - a240) < 1e-12,
                "camera lag is exactly frame-rate independent, not approximately",
                $"{a30:0.000000000} vs {a240:0.000000000}");

            // ---- run to walk decelerates rather than snapping ----
            var slowdown = new Locomotion();
            for (int i = 0; i < 120; i++) slowdown.Step(0, 1, Locomotion.RunSpeed, 1.0 / 60.0);
            slowdown.Step(0, 1, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(slowdown.Speed > Locomotion.WalkSpeed,
                "releasing run does not snap you to walking speed",
                $"speed {slowdown.Speed:0.00}");
            for (int i = 0; i < 60; i++) slowdown.Step(0, 1, Locomotion.WalkSpeed, 1.0 / 60.0);
            Check(Math.Abs(slowdown.Speed - Locomotion.WalkSpeed) < 0.01,
                "but it does arrive at walking speed");

            // ---- the camera follows; it is not welded on ----
            var rig = new CameraRig();
            rig.Place(0, 2, 0);
            Check(rig.Fov == rig.BaseFov, "a placed camera starts at the resting FOV");
            rig.Follow(4, 2, 0, 0, 0, 0, 1.0 / 60.0);
            Check(rig.X > 0 && rig.X < 4,
                "the camera lags a jump in the target", $"x {rig.X:0.00}");
            for (int i = 0; i < 240; i++) rig.Follow(4, 2, 0, 0, 0, 0, 1.0 / 60.0);
            Check(Math.Abs(rig.X - 4) < 0.01 && rig.X <= 4.0000001,
                "and settles onto it without overshooting", $"x {rig.X:0.0000}");

            var fresh = new CameraRig();
            fresh.Follow(50, 2, 50, 0, 0, 0, 1.0 / 60.0);
            Check(fresh.X == 50 && fresh.Z == 50,
                "an unplaced camera snaps instead of sweeping across the city");

            var tp = new CameraRig();
            tp.Place(0, 2, 0);
            tp.Follow(0, 2, 400, 0, 0, 0, 1.0 / 60.0);
            Check(tp.Z == 400,
                "a teleport is cut to, not flown to — no spring across the city",
                $"z {tp.Z:0.00}");
            tp.Follow(0, 2, 403, 0, 0, 0, 1.0 / 60.0);
            Check(tp.Z > 400 && tp.Z < 403,
                "but a large real movement still springs", $"z {tp.Z:0.00}");

            var fov = new CameraRig();
            fov.Place(0, 2, 0);
            for (int i = 0; i < 600; i++) fov.Follow(0, 2, 0, 1.0, 0, 1, 1.0 / 60.0);
            Check(Math.Abs(fov.Fov - (fov.BaseFov + fov.FovGain)) < 0.01,
                "FOV opens up at full effort", $"fov {fov.Fov:0.00}");
            Check(Math.Abs(fov.AheadZ - fov.LookAheadMetres) < 0.01,
                "and the frame leads you into where you are going",
                $"ahead {fov.AheadZ:0.00}");
            for (int i = 0; i < 600; i++) fov.Follow(0, 2, 0, 0.0, 0, 1, 1.0 / 60.0);
            Check(Math.Abs(fov.Fov - fov.BaseFov) < 0.01, "and closes again when you stop");
            Check(Math.Abs(fov.AheadZ) < 0.01, "and stops leading");

            // ---- the limp: rhythm, not speed ----
            Check(Gait.StrideFor(0, 0) == Gait.StrideFor(1, 0),
                "a healthy walk is symmetrical");
            double good = Gait.StrideFor(0, 0.8), bad = Gait.StrideFor(1, 0.8);
            Check(good > bad, "an injured one is not: the good leg carries");
            Check(Math.Abs((good + bad) - 2 * Gait.StrideMetres) < 1e-9,
                "but a pair of steps covers exactly the ground two healthy ones would",
                $"{good:0.000} + {bad:0.000}");
            Check(Gait.StrideFor(0, 0.9) - Gait.StrideFor(1, 0.9) >
                  Gait.StrideFor(0, 0.3) - Gait.StrideFor(1, 0.3),
                "and the worse the injury, the more lopsided the walk");
            Check(Gait.StrideFor(1, 5.0) > 0,
                "a severity above 1 still produces a forward step, not a backward one");

            Check(Gait.SpeedFactor(0) == 1.0, "an unhurt player moves at full speed");
            Check(Gait.SpeedFactor(1.0) < Gait.SpeedFactor(0.3),
                "and a hurt one is slower the worse it is");
            Check(Gait.SpeedFactor(5.0) >= 0.55,
                "but is never reduced to something unplayable",
                $"{Gait.SpeedFactor(5.0):0.00}");
            Check(Math.Abs(Gait.SeverityFromCapability(0.6) - 0.4) < 1e-9,
                "severity reads straight off the harm system's capability");

            Check(Gait.StepWeight(0, 0.8) > Gait.StepWeight(1, 0.8),
                "a limping step lands harder on the good leg");
            Check(Gait.StepWeight(0, 0) == Gait.StepWeight(1, 0),
                "and evenly when unhurt");
            Check(Gait.BobAmplitude(1.0) > Gait.BobAmplitude(0.0) &&
                  Gait.BobAmplitude(1.0) < 0.06,
                "head bob scales with effort and stays well short of seasick");

            // ---- input buffering and forgiveness ----
            var buf = new InputBuffer();
            buf.Press(10.0);
            Check(buf.Consume(10.1), "a press just before the action was legal still counts");
            Check(!buf.Consume(10.11), "but only once");
            buf.Press(20.0);
            Check(!buf.Consume(20.5), "a press older than the window is forgotten");
            buf.Press(30.0);
            buf.Clear();
            Check(!buf.Consume(30.01), "and a cleared buffer fires nothing");

            var grace = new Forgiveness();
            grace.SeenInRange(5.0);
            Check(grace.StillOffered(5.2), "a prompt survives a step out of range");
            Check(!grace.StillOffered(5.9), "but not indefinitely");
            grace.SeenInRange(6.0);
            grace.Drop();
            Check(!grace.StillOffered(6.01), "and a dropped prompt is gone at once");
        }

        static void TestAcoustics()
        {
            Console.WriteLine("Acoustics — how well you heard it is how sure you get to be:");

            // ---- distance ----
            Check(Acoustics.Gain(0, Acoustics.SpeechCarry) == 1.0, "a sound at your ear is full volume");
            double last = 1.0, rose = -1;
            for (double m = 0.5; m <= 60; m += 0.5)
            {
                double g = Acoustics.Gain(m, Acoustics.SpeechCarry);
                if (g > last && rose < 0) rose = m;
                last = g;
            }
            Check(rose < 0, "volume falls off monotonically", $"rose again at {rose}m");
            Check(last > 0 && last < 0.05,
                "and is nearly gone across the district but never exactly zero", $"{last:0.0000}");
            Check(Acoustics.Gain(20, Acoustics.ShoutCarry) > Acoustics.Gain(20, Acoustics.SpeechCarry),
                "a shout carries further than a word");

            // ---- the cutoff IS the distance cue ----
            Check(Acoustics.LowPassHz(0, false) > 20000, "a sound at your ear is unfiltered");
            Check(Acoustics.LowPassHz(30, false) < Acoustics.LowPassHz(5, false),
                "distance eats the high end");
            Check(Acoustics.LowPassHz(1, true) < Acoustics.LowPassHz(20, false),
                "a wall a metre away muffles more than twenty metres of open air",
                $"{Acoustics.LowPassHz(1, true):0} vs {Acoustics.LowPassHz(20, false):0}");

            // ---- can you actually make out the words ----
            Check(Acoustics.CanMakeOutWords(1.5, false),
                "you can hear someone you are standing with");
            Check(Acoustics.CanMakeOutWords(4, false),
                "and someone at the other end of the bar");
            Check(!Acoustics.CanMakeOutWords(20, false),
                "but not a conversation across the street");
            Check(!Acoustics.CanMakeOutWords(2, true),
                "nor one through a wall you are leaning on");
            Check(Acoustics.CanMakeOutWords(5, false, 0.0) &&
                  !Acoustics.CanMakeOutWords(5, false, 1.0),
                "and a loud street genuinely hides talk, rather than only sounding as if it does");

            double near = Acoustics.Intelligibility(2, false);
            double far = Acoustics.Intelligibility(9, false);
            Check(near > far, "clarity falls with distance");
            Check(near - Acoustics.Intelligibility(4, false) >
                  Acoustics.Intelligibility(9, false) - Acoustics.Intelligibility(11, false),
                "and falls fastest close in, where the meaning is");
            Check(Acoustics.Intelligibility(100, false) == 0 &&
                  Acoustics.Intelligibility(-5, false) <= 1.0,
                "clarity stays inside 0..1 at absurd distances");

            // ---- and what that is worth as a rumour ----
            Check(Acoustics.OverheardConfidence(1, false) < 0.95,
                "OVERHEARING IS NEVER KNOWLEDGE — the mill must not promote it",
                $"{Acoustics.OverheardConfidence(1, false):0.00}");
            Check(Acoustics.OverheardConfidence(1, false) >
                  Acoustics.OverheardConfidence(8, false),
                "you are surer of what you heard up close");
            Check(Acoustics.OverheardConfidence(30, false) == 0,
                "and carry nothing at all from across the district");
            Check(Acoustics.OverheardConfidence(3, true) < Acoustics.OverheardConfidence(3, false),
                "a wall makes a witness less sure");
            double worst = -1;
            for (double m = 0; m <= 40; m += 0.25)
                foreach (bool wall in new[] { false, true })
                    foreach (double noise in new[] { 0.0, 0.5, 1.0 })
                    {
                        double c = Acoustics.OverheardConfidence(m, wall, noise);
                        if ((c < 0 || c > 0.9) && worst < 0) worst = m;
                    }
            Check(worst < 0,
                "confidence never leaves 0..0.9 at any distance, wall or noise level",
                $"left the range at {worst}m");

            // The mill's own promotion rule is what this is protecting.
            var earshot = Agent("witness", "Witness", "night");
            var mill = new GossipMill(new SocialGraph());
            mill.Add(earshot);
            var heard = new Fact("player", "warehouse_d3", "seen");
            mill.Witness("witness", heard, "heard him say he'd been at the warehouse",
                true, new GameTime(3, 22, 0), Acoustics.OverheardConfidence(1.0, false));
            Check(earshot.Best("player.warehouse_d3") != null,
                "the closest overhearing does become a rumour");
            Check(earshot.Knowledge.CheckClaim(heard) == ClaimResult.Unknown,
                "but never hard knowledge — overhearing is not knowing");

            // ---- the line as it was actually heard ----
            const string spoken = "I'm telling you, he was down at the warehouse the night it went up.";
            Check(Acoustics.AsHeard(spoken, 1.0, 1) == spoken, "up close you get the whole line");
            Check(Acoustics.AsHeard(spoken, 0.0, 1) == null,
                "and across the district you get no line at all, not a quiet one");
            Check(Acoustics.AsHeard(null, 1.0, 1) == null && Acoustics.AsHeard("  ", 1.0, 1) == null,
                "nothing spoken is nothing heard");

            string half = Acoustics.AsHeard(spoken, 0.55, 7);
            Check(half != null && half.Contains("…"),
                "a half-heard line has holes in it", half);
            Check(half.Length < spoken.Length, "and is shorter than what was said", half);
            Check(half.Split(' ').Any(w => spoken.Contains(w) && w != "…"),
                "while keeping real words, so it is a gap and not a garble", half);
            Check(Acoustics.AsHeard(spoken, 0.55, 7) == half, "the same line heard twice is the same");
            Check(Acoustics.AsHeard(spoken, 0.55, 8) != half,
                "but two listeners catch different parts");

            // Averaged over seeds, because any single seed can be lucky.
            double SurvivingWords(double clarity)
            {
                double total = 0;
                for (int seed = 0; seed < 200; seed++)
                {
                    var h = Acoustics.AsHeard(spoken, clarity, seed);
                    total += h == null ? 0 : h.Split(' ').Count(w => w != "…");
                }
                return total / 200.0;
            }
            Check(SurvivingWords(0.8) > SurvivingWords(0.6) &&
                  SurvivingWords(0.6) > SurvivingWords(0.35),
                "the further away you are, the less of it you get",
                $"{SurvivingWords(0.8):0.0} > {SurvivingWords(0.6):0.0} > {SurvivingWords(0.35):0.0}");

            bool everBlank = false;
            for (int seed = 0; seed < 500; seed++)
            {
                var h = Acoustics.AsHeard(spoken, 0.3, seed);
                if (h != null && (h.Trim().Length == 0 || h.Trim() == "…")) everBlank = true;
            }
            Check(!everBlank,
                "and a heard line is never just an ellipsis — that is noise on the screen, not speech");

            // ---- and what the place does to it ----
            Check(Acoustics.DecaySeconds(SpaceKind.Outdoors) > 0,
                "even a street has a tail — a zero here is why outdoor scenes sound like a booth");
            Check(Acoustics.DecaySeconds(SpaceKind.Hall) > Acoustics.DecaySeconds(SpaceKind.Room) &&
                  Acoustics.DecaySeconds(SpaceKind.Room) > Acoustics.DecaySeconds(SpaceKind.Alley) &&
                  Acoustics.DecaySeconds(SpaceKind.Alley) > Acoustics.DecaySeconds(SpaceKind.Outdoors),
                "and the four spaces are ordered by how long they ring");
            Check(Acoustics.Wetness(SpaceKind.Alley) > Acoustics.Wetness(SpaceKind.Room) &&
                  Acoustics.DecaySeconds(SpaceKind.Alley) < Acoustics.DecaySeconds(SpaceKind.Room),
                "an alley reflects MORE than a room but for LESS time — that is what narrow sounds like");
            Check(Acoustics.RoomMetres(SpaceKind.Hall) > Acoustics.RoomMetres(SpaceKind.Room),
                "pre-delay tracks how big the place is");
            Check(Acoustics.OutsideBleed(SpaceKind.Outdoors) == 1.0 &&
                  Acoustics.OutsideBleed(SpaceKind.Room) < 0.5,
                "and stepping through a door shuts the street out");

            // The alley comes free from the street network, which was
            // authored for pathfinding and turns out to describe acoustics.
            Check(Acoustics.SpaceFor("lane", 1.0) == SpaceKind.Alley,
                "a four-metre lane between two building faces IS an alley");
            Check(Acoustics.SpaceFor("avenue", 1.0) == SpaceKind.Outdoors &&
                  Acoustics.SpaceFor("street", 1.0) == SpaceKind.Outdoors,
                "a road wide enough to drive down is not");
            Check(Acoustics.SpaceFor("lane", 20.0) == SpaceKind.Outdoors,
                "and standing in a yard twenty metres off it is not either");
            Check(Acoustics.SpaceFor(null, 0.0) == SpaceKind.Outdoors,
                "nowhere near a street is the sky, not a room");

            // Every lane on the real map must classify as an alley from its
            // own centreline, or the whole thing is theory.
            int lanes = 0, alleys = 0;
            foreach (var e in StreetMap.Edges)
            {
                if (e.Kind != "lane") continue;
                lanes++;
                if (Acoustics.SpaceFor(e.Kind, 0.5) == SpaceKind.Alley) alleys++;
            }
            Check(lanes > 0 && lanes == alleys,
                "and every lane the city actually has reads as one",
                $"{alleys}/{lanes}");

            // -- WHO ELSE HEARD THAT ------------------------------------------
            //
            // An alibi told to one person was told to exactly one person,
            // however crowded the room, because nothing asked whether a
            // bystander made out the WORDS. `CanMakeOutWords` and
            // `OverheardConfidence` were built for that and never called.
            //
            // THE ACCEPTING CASE FIRST, and it is the one with teeth: somebody
            // standing close DOES catch it. A version of this that quietly
            // caught nobody would look identical to a quiet street, and would
            // have shipped as "the mechanic never fires on this map".
            var ears = new List<Acoustics.Ear>
            {
                new Acoustics.Ear("close", 1.5),
                new Acoustics.Ear("across the room", 5.0),
                new Acoustics.Ear("down the street", 30.0),
                new Acoustics.Ear("through a wall", 2.0, occluded: true),
            };
            var overheardBy = Acoustics.WhoOverheard(ears);
            var bystanderIds = overheardBy.ConvertAll(h => h.ListenerId);
            Check(bystanderIds.Contains("close"),
                "somebody at arm's length catches an alibi you told to someone else",
                string.Join(", ", bystanderIds));
            Check(!bystanderIds.Contains("down the street"),
                "and somebody thirty metres off does not");
            Check(!bystanderIds.Contains("through a wall"),
                "nor somebody two metres away through a wall — a wall is not a distance");

            // NEVER KNOWLEDGE. The mill promotes anything at 0.95 into hard
            // fact, and a thing caught across a room becoming a thing you KNOW
            // is the difference between this game's rumour mill and a
            // database. The cap is asserted here rather than trusted, because
            // it is enforced in a different method from the one being called.
            foreach (var h in overheardBy)
                Check(h.Confidence < 0.95 && h.Confidence > 0,
                      $"what {h.ListenerId} took away is usable and never certain",
                      h.Confidence.ToString("0.00"));

            // CLOSER IS SURER, which is the whole model in one assertion.
            double nearEar = Acoustics.OverheardConfidence(1.5, false);
            double farEar = Acoustics.OverheardConfidence(5.0, false);
            Check(nearEar > farEar, "and the nearer ear is the surer one",
                  $"{nearEar:0.00} vs {farEar:0.00}");

            // A LOUD STREET IS COVER. Same geometry, noisier room, fewer ears
            // — so WHERE you say it is a decision, which is the point.
            int noisyCount = Acoustics.WhoOverheard(ears, streetNoise: 1.0).Count;
            Check(noisyCount <= overheardBy.Count,
                  "a loud street is cover, and never the reverse",
                  $"{noisyCount} of {overheardBy.Count}");

            Check(Acoustics.WhoOverheard(null).Count == 0,
                  "nobody in the room is not a crash");

            TestTelephone();
        }

        /// The second channel had a social model and no acoustic one — a voice
        /// on the phone was sample-identical to the same voice in the room.
        static void TestTelephone()
        {
            Console.WriteLine("The telephone — the mechanic that had no sound of its own:");

            Check(Acoustics.TelephoneLowHz == 300 && Acoustics.TelephoneHighHz == 3400,
                "the passband is the ITU voice channel, not a number somebody liked");
            Check(Acoustics.TelephoneHighHz < Acoustics.LowPassHz(0, false),
                "and it is narrower than a voice in the room, which is the whole point",
                $"{Acoustics.TelephoneHighHz:0} vs {Acoustics.LowPassHz(0, false):0}");
            Check(Acoustics.HandsetResonanceHz > Acoustics.TelephoneLowHz &&
                  Acoustics.HandsetResonanceHz < Acoustics.TelephoneHighHz,
                "the handset's ring sits INSIDE the band, or it would be filtered away");

            var kinds = new[] { Acoustics.LineKind.Handset, Acoustics.LineKind.PayPhone,
                                Acoustics.LineKind.LongDistance, Acoustics.LineKind.BadLine };
            for (int i = 1; i < kinds.Length; i++)
            {
                Check(Acoustics.LineClarity(kinds[i]) < Acoustics.LineClarity(kinds[i - 1]),
                    $"{kinds[i]} is a worse line than {kinds[i - 1]}");
                Check(Acoustics.LineNoise(kinds[i]) > Acoustics.LineNoise(kinds[i - 1]),
                    $"and a noisier one");
            }
            foreach (var k in kinds)
                Check(Acoustics.LineNoise(k) > 0,
                    $"no line is silent behind the voice — {k} would be the tell that nobody treated it");

            // THE DESIGN DECISION, asserted rather than left in a comment: a
            // good handset must clear the elision threshold, or every line of
            // a core mechanic arrives with a hole in it.
            const string said = "He was at the yard on Tuesday and he paid cash for it.";
            // EVERY SEED, not one. A single seed passes by luck at a clarity
            // just under the threshold — a break run that dropped the handset
            // from 0.94 to 0.84 survived this check when it tested seed 3
            // alone, which is the check being decorative.
            int wholeLine = 0;
            for (int seed = 0; seed < 300; seed++)
                if (Acoustics.AsHeardOnTheLine(said, Acoustics.LineKind.Handset, 0.0, seed) == said)
                    wholeLine++;
            Check(wholeLine == 300,
                "A GOOD HANDSET GIVES YOU THE WHOLE LINE, every time — it sounds like a "
                + "phone, it is not a puzzle",
                $"{wholeLine}/300");
            Check(Acoustics.AsHeardOnTheLine(said, Acoustics.LineKind.BadLine, 0.0, 3) != said,
                "and a bad junction is where the degradation gets spent");
            Check(Acoustics.AsHeardOnTheLine(said, Acoustics.LineKind.BadLine, 0.0, 3)?.Contains("…")
                  != false,
                "with holes in it, not a quieter version of it");

            // Distance does not exist on a line, and that is not an oversight.
            Check(Acoustics.LineIntelligibility(Acoustics.LineKind.Handset) ==
                  Acoustics.LineIntelligibility(Acoustics.LineKind.Handset),
                "a caller two hundred miles away arrives at the same clarity as one next door");
            Check(Acoustics.LineIntelligibility(Acoustics.LineKind.Handset, 1.0) <
                  Acoustics.LineIntelligibility(Acoustics.LineKind.Handset, 0.0),
                "but a loud room at the LISTENER's end still costs, because that is in with their ear");
            Check(Acoustics.LineIntelligibility(Acoustics.LineKind.Handset, 1.0) >
                  Acoustics.Intelligibility(0, false, 1.0),
                "and costs LESS than in the room — a handset shields the ear, which is why "
                + "people put a finger in the other one",
                $"{Acoustics.LineIntelligibility(Acoustics.LineKind.Handset, 1.0):0.00} vs "
                + $"{Acoustics.Intelligibility(0, false, 1.0):0.00}");
            foreach (var k in kinds)
                foreach (var n in new[] { 0.0, 0.5, 1.0, 4.0, -1.0 })
                    Check(Acoustics.LineIntelligibility(k, n) >= 0 &&
                          Acoustics.LineIntelligibility(k, n) <= 1,
                        $"clarity stays inside 0..1 for {k} at noise {n}");

            // WHOSE VOICE WAS THAT — the mechanic the band limit buys.
            Check(!Acoustics.CanPlaceTheVoice(Acoustics.LineKind.PayPhone, 0.4),
                "a callbox hides an acquaintance, which is why anonymous calls work in every crime story");
            Check(Acoustics.CanPlaceTheVoice(Acoustics.LineKind.Handset, 0.4),
                "the same person on your own line does not get to be anonymous");
            Check(!Acoustics.CanPlaceTheVoice(Acoustics.LineKind.BadLine, 0.9),
                "and a bad junction hides even somebody you know well");
            Check(Acoustics.CanPlaceTheVoice(Acoustics.LineKind.BadLine, 1.0),
                "though a voice you know perfectly still comes through — never say never");
            for (int i = 1; i < kinds.Length; i++)
            {
                // Monotone in the line: a worse line never makes somebody
                // EASIER to place.
                bool better = Acoustics.CanPlaceTheVoice(kinds[i - 1], 0.72);
                bool worse = Acoustics.CanPlaceTheVoice(kinds[i], 0.72);
                Check(!(worse && !better), $"{kinds[i]} never places a voice {kinds[i - 1]} could not");
            }

            // THE ROOM BEHIND THE CALLER. A jukebox behind Ellis tells you
            // which bar he is in, and nobody wrote a line of dialogue for it.
            Check(Acoustics.Bleed(SpaceKind.Hall, Acoustics.LineKind.Handset) >
                  Acoustics.Bleed(SpaceKind.Room, Acoustics.LineKind.Handset),
                "a hall comes down the wire and an office does not — which is why an empty "
                + "office sounds like nowhere");
            Check(Acoustics.Bleed(SpaceKind.Hall, Acoustics.LineKind.BadLine) <
                  Acoustics.Bleed(SpaceKind.Hall, Acoustics.LineKind.Handset),
                "and a bad junction buries the room along with everything else");
            foreach (SpaceKind s in Enum.GetValues(typeof(SpaceKind)))
                foreach (var k in kinds)
                    Check(Acoustics.Bleed(s, k) > 0 && Acoustics.Bleed(s, k) < 1,
                        $"bleed from {s} on a {k} is a real fraction");
        }

        /// A backend that plays back a script instead of running a model, so
        /// the loop's decisions can be tested without a GPU, a graph, or a
        /// 28-minute build.
        ///
        /// IT RECORDS WHAT IT WAS ASKED, not just what it returned. Three of
        /// the checks below are about the loop's side of the conversation —
        /// that a filtered token is still fed back, that `Release` happens on
        /// the failure path — and a stub that only answers cannot see those.
        sealed class ScriptedVoice : ISpeechBackend
        {
            readonly int[] _script;         // token to make most likely, per step
            int _step;
            public int FailAt = -1;         // step at which Next() returns false
            public bool FailBegin;
            public readonly List<int> FedBack = new List<int>();
            public int Released;
            /// THE MODEL'S REAL WIDTH, not a convenient small one. The first
            /// version used 32 and every run died on an IndexOutOfRange,
            /// because the stop token is 6562 and does not fit in a stub
            /// somebody sized for readability.
            public int Vocab = SpeechVocab.Size;

            public ScriptedVoice(params int[] script) { _script = script; }

            public int VocabSize => Vocab;
            public int StopToken => SpeechVocab.Stop;
            public int Rows => 1;

            void Fill(float[] logits)
            {
                for (int i = 0; i < logits.Length; i++) logits[i] = 0f;
                // A single dominant logit, so min-p keeps exactly one token
                // and the draw is forced. The sampler's own behaviour is
                // tested separately; here the point is the loop around it.
                int want = _step < _script.Length ? _script[_step] : SpeechVocab.Stop;
                logits[want] = 40f;
            }

            public bool Begin(string voiceId, string text, float[] logits)
            {
                if (FailBegin) return false;
                _step = 0;
                Fill(logits);
                return true;
            }

            public bool Next(int token, float[] logits)
            {
                FedBack.Add(token);
                _step++;
                if (FailAt >= 0 && _step >= FailAt) return false;
                Fill(logits);
                return true;
            }

            public void Release() { Released++; }

            /// One sample per token, which is enough to tell "produced audio"
            /// from "produced none" — the only distinction the queue makes.
            public float[] Decode(int[] tokens)
            {
                if (tokens == null || tokens.Length == 0) return null;
                var wav = new float[tokens.Length];
                for (int i = 0; i < tokens.Length; i++) wav[i] = tokens[i] / 8194f;
                return wav;
            }
        }

        /// A sink that records the token count at every call, so the test
        /// can assert the stream grew one acoustic token at a time.
        sealed class CountingSink : ISpeechStreamSink
        {
            readonly List<int> _counts;
            public CountingSink(List<int> counts) { _counts = counts; }
            public void Tokens(IReadOnlyList<int> tokens)
            { _counts.Add(tokens.Count); }
        }

        /// A decoder that emits exactly what the seam arithmetic promises,
        /// records which token counts it was asked at, and can be told to
        /// refuse a specific call — both fates of the follower in one fake.
        sealed class SeamFake : ISpeechChunkDecoder
        {
            public readonly List<int> Calls = new List<int>();
            public int FailAt = -1;
            bool _first = true;

            public float[] DecodeChunk(int[] tokens, int melOffset, bool final)
            {
                Calls.Add(tokens.Length);
                if (tokens.Length == FailAt) return null;
                int avail = SpeechStream.MelsPerToken * tokens.Length
                    - (final ? 0 : SpeechStream.MelsPerToken
                                   * SpeechStream.LookaheadTokens);
                int emitted = SpeechStream.EmittedSamples(
                    avail - melOffset, _first, final);
                _first = false;
                return new float[emitted];
            }
        }

        /// The step loop — the one piece of live speech that cannot be
        /// converted, because its length depends on the words.
        static void TestSpeechLoop()
        {
            Console.WriteLine("The speech loop — what the graph cannot contain:");

            // THE CONSTANTS ARE THE MODEL'S. Pinned to literals because the
            // first draft of SpeechLoop invented four of them and every one
            // looked reasonable. If chatterbox ever changes these, this fails
            // loudly rather than the voice quietly changing.
            Check(SpeechVocab.Size == 8194, "the logit width is the model's 8194");
            Check(SpeechVocab.Stop == 6562, "end-of-speech is 6562");
            Check(SpeechVocab.IsAcoustic(6560) && !SpeechVocab.IsAcoustic(6561),
                "6561 and up are not sound — the model's own `< 6561` filter");

            // ---- the accepting case, first, per CLAUDE.md rule 5b ----
            //
            // TEN TOKENS, NOT FIVE, because the default plan now carries a
            // per-word floor: three words demand nine steps before a stop
            // counts as finished, and the old five-token script sat under it.
            var good = new ScriptedVoice(11, 12, 13, 14, 15, 16, 17, 18, 19, 20);
            var run = SpeechLoop.Run(good, "rocco", "the docks, midnight");
            Check(run.Stop == SpeechStop.Finished, "a scripted line reaches its stop token",
                run.Stop.ToString());
            Check(run.Usable, "and is usable");
            Check(run.Tokens.Length == 10, "with every acoustic token kept",
                run.Tokens.Length.ToString());
            Check(run.Steps == 11, "and one more step than tokens — the stop token cost a step",
                run.Steps.ToString());
            Check(good.Released == 1, "and the cache was released exactly once",
                good.Released.ToString());

            // ---- determinism, which is VoiceBank's promise reaching here ----
            var again = SpeechLoop.Run(new ScriptedVoice(11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
                                       "rocco", "the docks, midnight");
            Check(string.Join(",", run.Tokens) == string.Join(",", again.Tokens),
                "the same voice and the same words give the same take");

            // ---- a filtered token is STILL FED BACK ----
            //
            // The easiest thing to get wrong in this file. A start-of-speech
            // token sampled mid-line is dropped from the AUDIO and must stay
            // in the model's history; feeding back the filtered stream tells
            // the model it said something it did not, from that step on.
            var stray = new ScriptedVoice(11, SpeechVocab.Start, 13);
            var strayRun = SpeechLoop.Run(stray, "rocco", "a line with a stray token");
            Check(strayRun.Tokens.Length == 2,
                "a non-acoustic token mid-line is dropped from the audio",
                strayRun.Tokens.Length.ToString());
            Check(stray.FedBack.Contains(SpeechVocab.Start),
                "but IS fed back to the model, or its history is a lie");
            Check(strayRun.Steps == 4,
                "and it still cost a step — Steps is what the latency estimate reads",
                strayRun.Steps.ToString());

            // ---- every refusing case ----
            var instant = new ScriptedVoice();     // stops at once
            var instantRun = SpeechLoop.Run(instant, "rocco", "hm");
            Check(instantRun.Stop == SpeechStop.StoppedShort && !instantRun.Usable,
                "a model that stops immediately is not a very short line, it is a failure",
                instantRun.Stop.ToString());

            // ---- THE FLOOR SCALES WITH THE WORDS — the fp16 fault, replayed ----
            //
            // Measured 12 August: an fp16 text stage rendered the sweep's
            // nine-word line as 4 tokens, and 4 passed the old constant
            // `MinSteps = 4` exactly. It would have PLAYED — a fifth of a
            // second of noise sold as a sentence — and then taught
            // `SpeechDirector` that nine words cost five steps. The text
            // here is that exact line, and five acoustic tokens clear the
            // old floor, so only the new one refuses this run.
            var quit = new ScriptedVoice(21, 22, 23, 24, 25);
            var quitRun = SpeechLoop.Run(quit, "ada",
                "Seen the van again. Thursday, same as last Thursday.");
            Check(quitRun.Stop == SpeechStop.StoppedShort && !quitRun.Usable,
                "a nine-word line ending after five steps is refused, whatever "
                + "the constant floor says", quitRun.Stop.ToString());

            // And the SAME count of steps with one word to say is a sentence —
            // the floor scaled down, not the model up. "No." measured 19
            // tokens on the real model; five is still past its floor of four.
            var curt = new ScriptedVoice(21, 22, 23, 24, 25);
            var curtRun = SpeechLoop.Run(curt, "ada", "No.");
            Check(curtRun.Stop == SpeechStop.Finished && curtRun.Usable,
                "while a one-word line ending at the same step is finished — "
                + "the floor is per word, not per line", curtRun.Stop.ToString());

            // The arithmetic, pinned: larger of the absolute and per-word
            // floors, words counted from the spoken text, zero disables.
            var floors = new SpeechPlan();
            Check(SpeechLoop.Floor(floors, "No.") == 4,
                "one word floors at MinSteps — the absolute floor still owns "
                + "the shortest lines", SpeechLoop.Floor(floors, "No.").ToString());
            Check(SpeechLoop.Floor(floors, "one two three four") == 12,
                "four words floor at twelve — three steps a word",
                SpeechLoop.Floor(floors, "one two three four").ToString());
            Check(SpeechLoop.Floor(new SpeechPlan { MinStepsPerWord = 0 },
                    "one two three four") == 4,
                "and zero turns the scaling off, leaving only the constant");

            var ceiling = new ScriptedVoice(1, 2, 3, 4, 5, 6, 7, 8);
            var ceilRun = SpeechLoop.Run(ceiling, "rocco", "a long one",
                new SpeechPlan { StepCeiling = 4 });
            Check(ceilRun.Stop == SpeechStop.StepCeiling, "the ceiling stops a runaway",
                ceilRun.Stop.ToString());
            Check(!ceilRun.Usable, "and a line cut mid-word is never played");

            var dead = new ScriptedVoice(1, 2, 3, 4, 5, 6, 7, 8);
            double clock = 0;
            var deadRun = SpeechLoop.Run(dead, "rocco", "a slow one",
                new SpeechPlan { DeadlineSeconds = 2.5 },
                () => { clock += 1.0; return clock; });
            Check(deadRun.Stop == SpeechStop.Deadline, "the deadline stops a slow machine",
                deadRun.Stop.ToString());
            Check(!deadRun.Usable, "and that line is dropped rather than played half-said");
            Check(deadRun.Steps > 0 && deadRun.SecondsPerStep > 0,
                "and it still reports a rate — the machines that hit this are the ones "
                + "whose speed we need to know",
                deadRun.SecondsPerStep.ToString("0.000"));

            var noStart = new ScriptedVoice(1, 2) { FailBegin = true };
            var noStartRun = SpeechLoop.Run(noStart, "rocco", "anything");
            Check(noStartRun.Stop == SpeechStop.BackendFailed,
                "a backend that will not start is reported, not thrown");
            Check(noStart.Released == 1,
                "and the cache is released even then — the finally, not the happy path",
                noStart.Released.ToString());

            var died = new ScriptedVoice(1, 2, 3, 4, 5, 6) { FailAt = 3 };
            var diedRun = SpeechLoop.Run(died, "rocco", "a driver reset");
            Check(diedRun.Stop == SpeechStop.BackendFailed && !diedRun.Usable,
                "a driver that goes away mid-line degrades to silence, not an exception",
                diedRun.Stop.ToString());

            Check(SpeechLoop.Run(new ScriptedVoice(1), "", "words").Stop == SpeechStop.Nothing,
                "no voice is nothing to say");
            Check(SpeechLoop.Run(new ScriptedVoice(1), "rocco", "   ").Stop == SpeechStop.Nothing,
                "and so is a text that normalises to empty");

            // ---- the runaway guard the ENGLISH model does not have ----
            //
            // OFF BY DEFAULT, and that is the point of the first check. The
            // analyzer this copies is only constructed `if is_multilingual`,
            // which is `text_tokens_dict_size == 2454`; the English model is
            // 704 — the exact vocabulary size the probe read off Jafar's
            // install. So it never runs, and defaulting it ON would end a line
            // at the first repeated token, which at 25 Hz is an ordinary thing
            // in a held vowel.
            Check(!new SpeechPlan().StopOnRepeat,
                "the repetition guard is OFF by default — the English model has "
                + "no alignment analyzer, so adding one would cut lines short");
            var allowed = SpeechLoop.Run(new ScriptedVoice(7, 7, 7, 7), "rocco", "stuck");
            Check(allowed.Stop == SpeechStop.Finished,
                "so a repeated token runs on, as it does in the model",
                allowed.Stop.ToString());
            var stuck = new ScriptedVoice(7, 7, 7, 7, 7, 7);
            var stuckRun = SpeechLoop.Run(stuck, "rocco", "stuck",
                new SpeechPlan { StopOnRepeat = true });
            Check(stuckRun.Stop == SpeechStop.Repetition,
                "and turned on — for a multilingual voice, which does have one — "
                + "two identical tokens in a row stop the line",
                stuckRun.Stop.ToString());
            Check(stuckRun.Usable,
                "and that IS a finished utterance — the model deciding it is done");

            // ---- the streaming sink hears the line grow ----
            var heard = new List<int>();
            var sink = new CountingSink(heard);
            var streamed = SpeechLoop.Run(
                new ScriptedVoice(31, SpeechVocab.Start, 33, 34), "rocco",
                "hum", null, null, sink);
            Check(string.Join(",", heard) == "1,2,3",
                "the sink hears every ACOUSTIC token as it lands — the stray "
                + "start token cost a step but made no sound and no call",
                string.Join(",", heard));
            Check(streamed.Tokens.Length == 3,
                "and the finished run agrees with what the sink was shown",
                streamed.Tokens.Length.ToString());

            // ---- classifier-free guidance ----
            //
            // Two rows in, one row out: cond + w*(cond - uncond). Checked by
            // arithmetic rather than by eye, because it is the mechanism the
            // first draft of the loop did not know existed at all.
            var two = new float[] { 2f, 0f, 1f, 4f };     // vocab 2, rows 2
            var into = new double[2];
            var guided = (double[])SpeechLoop.Guided(two, into, 2, 2, 0.5);
            Check(Math.Abs(guided[0] - (2 + 0.5 * (2 - 1))) < 1e-9,
                "guidance steers away from the unconditional row", guided[0].ToString("0.000"));
            Check(Math.Abs(guided[1] - (0 + 0.5 * (0 - 4))) < 1e-9,
                "including when that means going down", guided[1].ToString("0.000"));
            Check(ReferenceEquals(SpeechLoop.Guided(two, into, 2, 1, 0.5), two),
                "and a single-row backend is passed through untouched, not copied");

            // ---- the sampler, on its own ----
            var plan = new SpeechPlan();
            var flat = new float[8];
            for (int i = 0; i < 8; i++) flat[i] = 1f;
            var rng = new Random(1);
            var drawn = new HashSet<int>();
            for (int i = 0; i < 200; i++) drawn.Add(SpeechLoop.Pick(flat, 8, null, plan, rng));
            Check(drawn.Count == 8,
                "on a flat distribution every token is reachable — min-p keeps them all",
                drawn.Count.ToString());

            var peaked = new float[8];
            peaked[3] = 20f;                        // everything else is e^-20 away
            var peakDrawn = new HashSet<int>();
            for (int i = 0; i < 200; i++) peakDrawn.Add(SpeechLoop.Pick(peaked, 8, null, plan, rng));
            Check(peakDrawn.Count == 1 && peakDrawn.Contains(3),
                "and on a confident one min-p cuts the tail away entirely",
                string.Join(",", peakDrawn));

            // The penalty has to be able to CHANGE THE ANSWER, or it is
            // decoration. Two close tokens, the leader already spoken.
            var close = new float[] { 0f, 0f, 2.0f, 1.9f, 0f, 0f, 0f, 0f };
            Check(SpeechLoop.Pick(close, 8, null, plan, new Random(3)) == 2,
                "the likeliest token wins when nothing has been said yet");
            Check(SpeechLoop.Pick(close, 8, new HashSet<int> { 2 }, plan, new Random(3)) == 3,
                "and loses once it has — the repetition penalty reorders, it does "
                + "not merely nudge");

            // A negative logit must get LESS likely, not more. Dividing
            // throughout is the obvious implementation and it is backwards for
            // the whole negative half of the range.
            var negative = new float[] { -2.0f, -2.1f, -40f, -40f, -40f, -40f, -40f, -40f };
            Check(SpeechLoop.Pick(negative, 8, new HashSet<int> { 0 }, plan, new Random(3)) == 1,
                "penalising a NEGATIVE logit pushes it down, not up");

            var broken = new float[8];
            for (int i = 0; i < 8; i++) broken[i] = float.NaN;
            Check(SpeechLoop.Pick(broken, 8, null, plan, new Random(1)) >= 0,
                "and degenerate logits return a token rather than throwing");

            // ---- CONFORMANCE WITH THE MODEL'S OWN SAMPLER ----
            //
            // Everything above checks that this sampler behaves sensibly.
            // Sensible is not the bar: the bar is IDENTICAL to chatterbox's,
            // because every way of being wrong here still produces speech —
            // a voice, saying the words, sounding slightly off, with no error
            // anywhere and nothing to grep for.
            //
            // These numbers are not mine. `tools/voice-live/sampler-reference.py`
            // runs the actual HuggingFace processors `t3.py` builds —
            // RepetitionPenalty, MinP, TopP, in that order — over these exact
            // logits and prints what survives. Re-run it to regenerate them.
            //
            // The DRAW is not compared and cannot be: Python and C# have
            // different random generators, so the same seed picks differently
            // and always will. The distribution is the part that can be
            // identical, and it is the whole of the sampler.
            void Conforms(string name, float[] logits, int[] said,
                          int[] wantKept, double[] wantWeights)
            {
                var seenSet = said == null ? null : new HashSet<int>(said);
                SpeechLoop.Distribution(logits, logits.Length, seenSet, new SpeechPlan(),
                                        out var kept, out var weights);
                Check(string.Join(",", kept) == string.Join(",", wantKept),
                    $"conforms — {name}: the same tokens survive, in the same order",
                    $"got [{string.Join(",", kept)}] want [{string.Join(",", wantKept)}]");
                double worst = 0;
                for (int i = 0; i < Math.Min(weights.Length, wantWeights.Length); i++)
                    worst = Math.Max(worst, Math.Abs(weights[i] - wantWeights[i]));
                Check(weights.Length == wantWeights.Length && worst < 1e-5,
                    $"conforms — {name}: and with the same weights, to 1e-5",
                    $"worst {worst:0.0000000}");
            }

            Conforms("flat", new float[] { 1, 1, 1, 1, 1, 1, 1, 1 }, null,
                new[] { 0, 1, 2, 3, 4, 5, 6, 7 },
                new[] { 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125, 0.125 });

            Conforms("confident", new float[] { 0, 0, 0, 20, 0, 0, 0, 0 }, null,
                new[] { 3 }, new[] { 1.0 });

            Conforms("two close, nothing said",
                new float[] { 0, 0, 2.0f, 1.9f, 0, 0, 0, 0 }, null,
                new[] { 2, 3, 0, 1, 4, 5, 6, 7 },
                new[] { 0.421052, 0.371577, 0.034562, 0.034562,
                        0.034562, 0.034562, 0.034562, 0.034562 });

            Conforms("two close, leader already said",
                new float[] { 0, 0, 2.0f, 1.9f, 0, 0, 0, 0 }, new[] { 2 },
                new[] { 3, 2, 0, 1, 4, 5, 6, 7 },
                new[] { 0.43382, 0.324071, 0.040352, 0.040352,
                        0.040352, 0.040352, 0.040352, 0.040352 });

            // THE ONE THAT CATCHES THE OBVIOUS BUG. A penalty written as a
            // plain divide turns -2.0 into -1.67, which is MORE likely — so
            // it rewards what it exists to discourage, across the whole
            // negative half of the range, which is most of it.
            Conforms("negative logits, leader already said",
                new float[] { -2.0f, -2.1f, -40, -40, -40, -40, -40, -40 }, new[] { 0 },
                new[] { 1, 0 }, new[] { 0.592667, 0.407333 });

            // Min-p cutting a real tail: four of eight survive, and which
            // four is not something you would guess.
            Conforms("a graded spread",
                new float[] { 3.0f, 2.5f, 2.0f, 1.0f, 0.0f, -1.0f, -5.0f, -20.0f }, null,
                new[] { 0, 1, 2, 3 },
                new[] { 0.525251, 0.281147, 0.150487, 0.043115 });

            Conforms("a graded spread with two said",
                new float[] { 3.0f, 2.5f, 2.0f, 1.0f, 0.0f, -1.0f, -5.0f, -20.0f },
                new[] { 0, 2 },
                new[] { 0, 1, 2, 3 },
                new[] { 0.399007, 0.399007, 0.140796, 0.06119 });
        }


        /// A character's voice, as the game will read it off disk.
        static void TestVoiceConditionals()
        {
            Console.WriteLine("Voice conditionals — the numbers behind a character's voice:");

            var dir = new DirectoryInfo(AppContext.BaseDirectory);
            string folder = null;
            while (dir != null)
            {
                var p = Path.Combine(dir.FullName, "game-design", "voice-conds");
                if (Directory.Exists(p)) { folder = p; break; }
                dir = dir.Parent;
            }
            var files = folder == null ? new string[0] : Directory.GetFiles(folder, "*.bin");
            Array.Sort(files);
            if (files.Length == 0)
            {
                // A DENOMINATOR ON THE SKIP, same as the tokeniser's. "the
                // voices are not computed" and "the reader works" must not
                // print the same way.
                Check(true, "voice conditionals SKIPPED — no game-design/voice-conds/*.bin, "
                            + "0 voices read");
                return;
            }

            // EVERY VOICE, NOT ONE. The prompt lengths differ between them —
            // five distinct lengths across the nineteen — so a reader that
            // works on the first file is a reader that has not been tested.
            int ok = 0, arrays = 0;
            string firstWhy = null, firstBad = null;
            var lengths = new HashSet<int>();
            foreach (var f in files)
            {
                string why;
                var v = VoiceConditionals.Load(File.ReadAllBytes(f), out why);
                if (v == null)
                {
                    if (firstBad == null) { firstBad = Path.GetFileName(f); firstWhy = why; }
                    continue;
                }
                ok++;
                arrays += v.Count;
                var pt = v.Get("gen.prompt_token");
                if (pt != null) lengths.Add(pt.Rows);
            }
            Check(ok == files.Length,
                $"all {files.Length} committed voices load — {arrays} arrays in total",
                firstBad + ": " + firstWhy);
            if (ok == 0) return;

            Check(lengths.Count > 1,
                $"and they carry {lengths.Count} different prompt lengths, so the reader "
                + "is taking the shape from the file rather than from a constant",
                string.Join(", ", lengths));

            var one = VoiceConditionals.Load(File.ReadAllBytes(files[0]), out _);
            Check(one.Has("t3.speaker_emb") && one.Has("t3.cond_prompt_speech_tokens")
                  && one.Has("t3.emotion_adv") && one.Has("gen.prompt_token")
                  && one.Has("gen.prompt_feat") && one.Has("gen.embedding"),
                "and each has the six arrays the three graphs ask for",
                string.Join(", ", one.Names));

            var emb = one.Get("gen.embedding");
            Check(emb != null && emb.Floats != null && emb.Count == 192,
                "the speaker embedding is 192 floats, which is what s3gen takes",
                emb == null ? "absent" : emb.Count + (emb.Floats == null ? " ints" : " floats"));
            var tok = one.Get("gen.prompt_token");
            Check(tok != null && tok.Longs != null && tok.Longs.Length > 0,
                "and the prompt tokens came back as integers rather than floats",
                tok == null ? "absent" : (tok.Longs == null ? "floats" : tok.Longs.Length + " ints"));

            var feat = one.Get("gen.prompt_feat");
            Check(feat != null && feat.Shape.Length == 3 && feat.Shape[2] == 80,
                "the prompt spectrogram is 80 bands deep, and its length travels with it",
                feat == null ? "absent" : string.Join("x", feat.Shape));

            // NOT ALL ZERO. A reader that returns the right shapes full of
            // nothing passes every check above, and a silent voice is what
            // that produces — audible only as a character who never speaks.
            var sp = one.Get("t3.speaker_emb");
            double peak = 0;
            for (int i = 0; i < sp.Floats.Length; i++) peak = Math.Max(peak, Math.Abs(sp.Floats[i]));
            Check(peak > 1e-6, $"and the numbers are numbers — the speaker vector peaks at {peak:0.###}",
                peak.ToString());

            // THE REJECTING CASES, run rather than reasoned about.
            string badWhy;
            Check(VoiceConditionals.Load(System.Text.Encoding.ASCII.GetBytes("NOTAVOICE!!!!!!!"), out badWhy) == null
                  && badWhy != null && badWhy.Contains("not a voice file"),
                "a file with the wrong header is refused and says so", badWhy);
            Check(VoiceConditionals.Load(null, out badWhy) == null && badWhy != null,
                "so is nothing at all", badWhy);

            var whole = File.ReadAllBytes(files[0]);
            var half = new byte[whole.Length / 2];
            Array.Copy(whole, half, half.Length);
            Check(VoiceConditionals.Load(half, out badWhy) == null
                  && badWhy != null && badWhy.Contains("truncated"),
                "and a half-copied file is caught rather than read as a quieter voice",
                badWhy);
        }

        /// Words into the numbers the model reads.
        static void TestSpeechTokenizer()
        {
            Console.WriteLine("The speech tokeniser — words into the model's numbers:");

            // THE REAL VOCABULARY, off Jafar's machine on 7 August. Found by
            // walking up from the test binary, because CoreTests runs from
            // `bin/Release/netX/` and the repository root is what everything
            // else here is relative to.
            var dir = new DirectoryInfo(AppContext.BaseDirectory);
            string path = null;
            while (dir != null)
            {
                var p = Path.Combine(dir.FullName, "tools", "voice-live", "tokenizer.json");
                if (File.Exists(p)) { path = p; break; }
                dir = dir.Parent;
            }
            if (path == null)
            {
                // A DENOMINATOR ON THE SKIP. "the vocabulary is not fetched
                // yet" and "the tokeniser is correct" must not read the same.
                Check(true, "tokeniser SKIPPED — no tools/voice-live/tokenizer.json, "
                            + "0 of 14 texts checked");
                return;
            }

            var tok = SpeechTokenizer.Load(File.ReadAllText(path), out var why);
            Check(tok != null, "the shipped vocabulary loads", why);
            if (tok == null) return;
            Check(tok.Count == 704 && tok.Merges == 265,
                "and it is the one the probe reported — 704 tokens, 265 merges",
                $"{tok.Count}/{tok.Merges}");

            // EVERY EXPECTED SEQUENCE CAME OUT OF HUGGINGFACE'S OWN TOKENISER.
            // `python3 tools/voice-live/tokenizer-reference.py --cs` prints
            // these lines ready to paste. Do not hand-edit one because it
            // looks wrong — twice now the thing that looked wrong was right.
            void Same(string text, params int[] want)
            {
                var got = tok.Encode(text);
                Check(string.Join(",", got) == string.Join(",", want),
                    $"tokenises [{text}]",
                    $"got [{string.Join(",", got)}] want [{string.Join(",", want)}]");
            }

            Same("I was on the docks when it happened.", 285, 2, 81, 2, 47, 2, 42, 2, 134, 197, 32, 2, 199, 2, 60, 2, 102, 246, 50, 49, 9);
            // A capital and its word: the merge table was learned on lower
            // case, so "Hello" is four pieces and not one.
            Same("Hello there.", 284, 18, 84, 28, 2, 172, 9);
            // punc_norm's double space survives as TWO [SPACE] tokens.
            Same("Wait,  what.", 299, 14, 60, 7, 2, 2, 193, 9);
            Same("the", 42);
            Same("a", 14);
            // No `aa` merge exists, so eight a's are eight tokens — the case
            // that would pass if merging were done once instead of to fixpoint.
            Same("aaaaaaaa", 14, 14, 14, 14, 14, 14, 14, 14);
            // The pre-tokeniser splits words from punctuation.
            Same("don't", 17, 47, 4, 33);
            Same("one-two", 110, 8, 232, 28);
            Same("ZQXJ", 302, 293, 300, 286);
            Same("...", 9, 9, 9);
            Same("he said, go now.", 62, 2, 252, 7, 2, 119, 2, 145, 9);
            Same("\u00e9clair na\u00efve", 402, 16, 25, 14, 98, 2, 27, 14, 408, 76);
            // Out of the vocabulary entirely: one UNK EACH, because
            // `fuse_unk` is false. Fusing them would lose a syllable.
            Same("\u4e2d\u6587", 1, 1);
            Same("Ends with a dash -", 281, 27, 17, 32, 2, 103, 2, 14, 2, 17, 55, 21, 2, 8);

            // ---- the refusing cases ----
            Check(tok.Encode("").Length == 0 && tok.Encode(null).Length == 0,
                "nothing in, nothing out");
            Check(SpeechTokenizer.Load("", out var w1) == null && w1 != null,
                "an empty file is refused WITH a reason", w1);
            Check(SpeechTokenizer.Load("{\"model\":{}}", out var w2) == null && w2 != null,
                "and so is json that is not a tokenizer.json", w2);
            Check(SpeechTokenizer.Load("{not json", out var w3) == null && w3 != null,
                "and so is a truncated one, rather than throwing into a frame", w3);

            // THE WHOLE FRONT DOOR, END TO END. `SpeechText.Normalise` is what
            // runs before this in the real path, and its output is what the
            // literals above were generated from — so this is the join, not a
            // third thing.
            Check(string.Join(",", tok.Encode(SpeechText.Normalise("hello there")))
                  == string.Join(",", tok.Encode("Hello there.")),
                "and punc_norm feeding the tokeniser gives the same ids as the "
                + "text it produces — the two halves join");
        }

        /// What the model is actually told to say.
        static void TestSpeechText()
        {
            Console.WriteLine("Speech text — the tidy-up the model runs before it tokenises:");

            // EVERY EXPECTED STRING CAME OUT OF THE REAL FUNCTION.
            // `python3 tools/voice-live/sampler-reference.py --text` prints
            // these lines ready to paste. Re-run it to regenerate them; do not
            // hand-edit one because it looks wrong, because twice now the
            // thing that looked wrong was the thing that was right.
            void Same(string given, string want)
            {
                var got = SpeechText.Normalise(given);
                Check(got == want, $"punc_norm — [{given}]",
                    $"got [{got}] want [{want}]");
            }

            Same("hello there", "Hello there.");
            // NOT capitalised: the first character is a space, and the capital
            // happens BEFORE the whitespace collapse. Swapping those two lines
            // changes this and nothing else would report it.
            Same("  leading space and lower", "leading space and lower.");
            Same("already. Fine.", "Already. Fine.");
            // A DOUBLE SPACE, and it is correct. "..." becomes ", " — comma
            // and space — next to the space that was already there, and the
            // collapse has already run. An implementation that tidied it up
            // would be feeding the model different text from the one it was
            // trained against.
            Same("wait... what", "Wait,  what.");
            Same("he said: go now", "He said, go now.");
            Same("one - two", "One, two.");
            Same("stop; go", "Stop,  go.");
            Same("an em—dash and an en–dash", "An em-dash and an en-dash.");
            Same("“quoted” and ‘single’", "\"quoted\" and 'single'.");
            Same("trailing spaces   ", "Trailing spaces.");
            // Already ends in an ender, so no full stop is added.
            Same("ends with a dash -", "Ends with a dash -");
            Same("lots     of      space", "Lots of space.");
            Same("a , b", "A, b.");
            Same("MiXeD case stays", "MiXeD case stays.");

            // THE ONE DELIBERATE DIVERGENCE. chatterbox answers empty text
            // with the sentence "You need to add some text for me to talk."
            // In a game that is a cast voice reading an error message aloud.
            Check(SpeechText.Normalise("") == null
                  && SpeechText.Normalise(null) == null
                  && SpeechText.Normalise("   ") == null,
                "empty text is nothing to say, NOT the model's spoken error message");
            Check(SpeechLoop.Run(new ScriptedVoice(1), "rocco", "  ").Stop == SpeechStop.Nothing,
                "and the loop refuses it too, so there are two ways this cannot happen");
        }

        /// A line takes nine seconds and a frame takes sixteen milliseconds.
        static void TestSpeechQueue()
        {
            Console.WriteLine("The speech queue — what gets said, and what stops being worth saying:");

            var q = new SpeechQueue();
            Check(q.Seen == 0 && q.Spoken == 0,
                "a fresh queue has seen nothing — a count, not a silence");

            // ---- the accepting case first, per CLAUDE.md rule 5b ----
            Check(q.Offer("rocco", "the docks, midnight", 0.0), "a line is accepted");
            Check(q.Waiting == 1 && !q.Busy, "and waits, with nothing in flight");
            var job = q.TakeNext(0.1);
            Check(job != null && job.VoiceId == "rocco", "the worker takes it");
            Check(q.Busy && q.Waiting == 0, "and it is in flight, not waiting");
            q.Deliver(job, new SpeechRun { Stop = SpeechStop.Finished, Steps = 40,
                                           Tokens = new int[39] }, new float[8000], 3.0);
            Check(!q.Busy, "delivering frees the session");
            var got = q.Collect();
            Check(got != null && got.Speakable, "and the main thread collects a speakable line");
            Check(q.Spoken == 1 && q.Collect() == null,
                "counted once, and there is nothing else waiting to be collected");

            // ---- ONE AT A TIME ----
            var one = new SpeechQueue();
            one.Offer("rocco", "first", 0.0);
            one.Offer("lena", "second", 0.0);
            var a = one.TakeNext(0.0);
            Check(a != null && one.TakeNext(0.0) == null,
                "a second line cannot start while the first is in flight — there is "
                + "one model and one set of cache tensors");

            // ---- THE QUEUE IS SHALLOW, AND REFUSAL IS COUNTED ----
            var full = new SpeechQueue { Depth = 2 };
            Check(full.Offer("a", "one", 0) && full.Offer("b", "two", 0),
                "two lines fit a depth of two");
            Check(!full.Offer("c", "three", 0) && full.Refused == 1,
                "the third is refused and said so — a deeper queue would only buy "
                + "more discarded speech");
            Check(full.Seen == 3, "and the denominator counts it: 3 seen, 2 taken",
                full.Seen.ToString());

            // ---- THE SAME LINE TWICE IS ONE LINE ----
            var dup = new SpeechQueue();
            dup.Offer("rocco", "look out", 0);
            Check(!dup.Offer("rocco", "look out", 0) && dup.Waiting == 1,
                "two walkers reacting to one event do not generate it twice");
            Check(dup.Offer("rocco", "look  out", 0) == false,
                "and whitespace does not make it a different line");
            Check(dup.Offer("lena", "look out", 0),
                "but a different voice saying it does");

            // ---- SHELF LIFE: WAITING TOO LONG ----
            var stale = new SpeechQueue { ShelfSeconds = 5.0 };
            stale.Offer("rocco", "too late", 0.0);
            Check(stale.TakeNext(4.9) != null, "a line inside its shelf life is taken");
            var stale2 = new SpeechQueue { ShelfSeconds = 5.0 };
            stale2.Offer("rocco", "too late", 0.0);
            Check(stale2.TakeNext(5.1) == null && stale2.Expired == 1,
                "and one past it is dropped where it sits rather than generated");
            Check(stale2.Waiting == 0, "leaving nothing behind");

            // ---- SHELF LIFE: GENERATED, BUT THE MOMENT HAS GONE ----
            //
            // THE CASE WORTH COUNTING MOST. It means the machine CAN speak and
            // cannot speak in TIME, which is a different problem from a machine
            // that cannot speak at all — and both would otherwise be silence.
            var late = new SpeechQueue { ShelfSeconds = 5.0 };
            late.Offer("rocco", "answer", 0.0);
            var lj = late.TakeNext(0.1);
            late.Deliver(lj, new SpeechRun { Stop = SpeechStop.Finished, Steps = 40,
                                             Tokens = new int[39] }, new float[8000], 9.0);
            var lc = late.Collect();
            Check(lc != null && !lc.Speakable && lc.Drop == SpeechDrop.TooLate,
                "a line finished after its moment is NOT played", lc?.Drop.ToString());
            Check(late.Expired == 1 && late.Spoken == 0,
                "and is counted as expired rather than spoken");

            // ---- A FAILED RUN IS NOT A SPOKEN ONE ----
            var bad = new SpeechQueue();
            bad.Offer("rocco", "broken", 0.0);
            var bj = bad.TakeNext(0.0);
            bad.Deliver(bj, new SpeechRun { Stop = SpeechStop.BackendFailed }, null, 0.5);
            var bc = bad.Collect();
            Check(bc != null && !bc.Speakable && bad.Failed == 1 && bad.Spoken == 0,
                "a driver that went away mid-line is counted as failed, not spoken");
            Check(!bad.Busy, "and it still freed the session, or nothing could ever run again");

            // A run that finished but produced no audio is also a failure, not
            // a silent success — the two look identical from outside.
            var empty = new SpeechQueue();
            empty.Offer("rocco", "silence", 0.0);
            var ej = empty.TakeNext(0.0);
            empty.Deliver(ej, new SpeechRun { Stop = SpeechStop.Finished, Tokens = new int[5] },
                          new float[0], 0.5);
            Check(empty.Collect()?.Speakable == false && empty.Failed == 1,
                "and a run that returned no samples at all is a failure too");

            Check(!new SpeechQueue().Offer("", "words", 0)
                  && !new SpeechQueue().Offer("rocco", "   ", 0),
                "nothing to say is not queued");

            var line = q.Verdict();
            Check(line.Split(' ').Length == 8 && !line.Contains("= "),
                "the verdict line is eight space-separated pairs", line);
        }

        /// Who speaks live, and whether this machine can afford it.
        /// The pop Jafar heard at the top of every line in the five-line
        /// test file, and the game's own playback path had it waiting.
        /// The streaming plan — the C# half of an arithmetic that exists
        /// twice on purpose. `hear-chunks.py plan_chunks` is the python
        /// twin; these cases are ITS cases, so a drift between them fails a
        /// test rather than clicking at a seam on Jafar's machine.
        static void TestSpeechStream()
        {
            Console.WriteLine("The streaming plan — chunks, seams, and when to start:");

            var p = SpeechStream.Plan(86);
            Check(p.Count == 4 && p[p.Count - 1].Final
                  && p[p.Count - 1].VisibleTokens == 86,
                "an 86-token line plans four chunks and the final one sees "
                + "every token", p.Count.ToString());
            bool onlyLast = true;
            for (int i = 0; i < p.Count - 1; i++) onlyLast &= !p[i].Final;
            Check(onlyLast, "and only the final chunk is final");
            int mels = 0;
            bool covered = true;
            foreach (var c in p)
            {
                if (c.MelOffset != mels) covered = false;
                mels = SpeechStream.MelsPerToken * c.VisibleTokens
                    - (c.Final ? 0 : SpeechStream.MelsPerToken
                                     * SpeechStream.LookaheadTokens);
            }
            Check(covered && mels == SpeechStream.MelsPerToken * 86,
                "every mel is rendered exactly once across the plan — a gap "
                + "is silence and an overlap is a stutter",
                mels.ToString());

            Check(SpeechStream.Plan(5).Count == 1 && SpeechStream.Plan(5)[0].Final
                  && SpeechStream.Plan(5)[0].MelOffset == 0,
                "a line shorter than one chunk is a single final call");
            Check(SpeechStream.Plan(24).Count == 1,
                "and a line of exactly one chunk is too");
            Check(SpeechStream.Plan(0).Count == 0, "an empty line plans nothing");
            var tail = SpeechStream.Plan(25);
            Check(tail.Count == 2 && !tail[0].Final && tail[0].VisibleTokens == 24
                  && tail[1].Final && tail[1].MelOffset == 42,
                "a one-token tail still gets a final call that releases the "
                + "held-back lookahead",
                tail.Count + " chunks, offset " + (tail.Count > 1
                    ? tail[1].MelOffset.ToString() : "-"));

            // The seam accounting: what the chunks EMIT must close to the
            // whole line, and the first chunk must out-render the holdback
            // it keeps back — its seam is EMPTY, the whole-line function
            // exactly — both facts the export selftest proved on the real
            // (small) model, kept here as arithmetic so a plan change
            // cannot silently break them.
            foreach (var n in new[] { 86, 24, 25, 5, 100 })
            {
                var q = SpeechStream.Plan(n);
                int emitted = 0, off = 0;
                for (int i = 0; i < q.Count; i++)
                {
                    int avail = SpeechStream.MelsPerToken * q[i].VisibleTokens
                        - (q[i].Final ? 0 : SpeechStream.MelsPerToken
                                            * SpeechStream.LookaheadTokens);
                    emitted += SpeechStream.EmittedSamples(
                        avail - off, i == 0, q[i].Final);
                    off = avail;
                }
                Check(emitted == SpeechStream.MelsPerToken * n
                                 * SpeechStream.SamplesPerMel,
                    "the emitted stream closes to the whole line for "
                    + n + " tokens", emitted.ToString());
            }
            {
                var q = SpeechStream.Plan(100);
                int firstFresh = SpeechStream.MelsPerToken * q[0].VisibleTokens
                    - (q[0].Final ? 0 : SpeechStream.MelsPerToken
                                        * SpeechStream.LookaheadTokens);
                Check(q[0].Final || firstFresh * SpeechStream.SamplesPerMel
                      > SpeechStream.SeamSamples,
                    "and a first chunk out-renders the holdback it keeps "
                    + "back, so it always emits",
                    (firstFresh * SpeechStream.SamplesPerMel).ToString());
            }

            // THE FOLLOWER: the live driver over a fake decoder that emits
            // exactly what the seam arithmetic promises — which doubles as
            // a parity check between EmittedSamples and any decoder that
            // disagrees with it.
            {
                var fake = new SeamFake();
                var follower = new SpeechChunkFollower(
                    fake, 60, 40.0, 1.0, 0.1, 0.005);
                var live = new List<int>();
                for (int t = 1; t <= 60; t++)
                {
                    live.Add(t);
                    follower.Tokens(live);
                }
                Check(fake.Calls.Count == 2 && fake.Calls[0] == 24
                      && fake.Calls[1] == 48,
                    "sixty tokens cross two boundaries mid-line, at 24 and "
                    + "48", string.Join(",", fake.Calls));
                Check(!follower.Complete,
                    "and the line is not complete until Finish");
                follower.Finish(live.ToArray());
                Check(follower.Complete && !follower.Failed,
                    "Finish decodes the final chunk and completes the line");
                var all = follower.TakeReady();
                Check(all != null && all.Length == 60
                      * SpeechStream.MelsPerToken * SpeechStream.SamplesPerMel,
                    "and the banked stream IS the whole line, sample for "
                    + "sample of length", (all == null ? 0 : all.Length).ToString());
                Check(follower.CanStartNow,
                    "a finished line may always start");
                Check(follower.SamplesReady == 0 && follower.TakeReady() == null,
                    "and the bank drains exactly once");
            }
            {
                // The failure fate: the decoder says no mid-line, the
                // follower flips Failed, stops asking, and the caller
                // falls back to the whole-line path.
                var fake = new SeamFake { FailAt = 48 };
                var follower = new SpeechChunkFollower(
                    fake, 90, 40.0, 1.0, 0.1, 0.005);
                var live = new List<int>();
                for (int t = 1; t <= 90; t++) { live.Add(t); follower.Tokens(live); }
                Check(follower.Failed && fake.Calls.Count == 2,
                    "a decoder refusal flips Failed and no further chunk is "
                    + "asked for", fake.Calls.Count.ToString());
                follower.Finish(live.ToArray());
                Check(!follower.Complete && !follower.CanStartNow,
                    "a failed line never completes and never starts");
            }
            {
                // A line under one chunk: no mid-line call, one final one.
                var fake = new SeamFake();
                var follower = new SpeechChunkFollower(
                    fake, 10, 40.0, 1.0, 0.1, 0.005);
                var live = new List<int>();
                for (int t = 1; t <= 10; t++) { live.Add(t); follower.Tokens(live); }
                follower.Finish(live.ToArray());
                Check(fake.Calls.Count == 1 && follower.Complete,
                    "a short line is one final chunk",
                    fake.Calls.Count.ToString());
                var all = follower.TakeReady();
                Check(all != null && all.Length == 10
                      * SpeechStream.MelsPerToken * SpeechStream.SamplesPerMel,
                    "and it banks the whole short line",
                    (all == null ? 0 : all.Length).ToString());
            }

            // The no-underrun rule is arithmetic, and both fates of it.
            Check(SpeechStream.CanStart(1.0, 2.0, 2.5),
                "playback starts when the work owed is under the audio in "
                + "hand plus the audio that work yields");
            Check(!SpeechStream.CanStart(1.0, 4.0, 2.5),
                "and waits when the work owed exceeds it — starting there "
                + "underruns mid-line by construction");
            Check(!SpeechStream.CanStart(0.0, 0.5, 3.0),
                "and never starts with nothing banked, whatever the rates say");

            // Sustainability: the resident path streams, the CPU path does
            // not, and an unmeasured machine does not guess.
            Check(SpeechStream.Sustainable(58.0, 0.98),
                "58 steps a second at the measured token ratio streams");
            Check(!SpeechStream.Sustainable(14.0, 0.98),
                "a CPU-rate machine does not — a stutter reads worse than a "
                + "pause before a whole line");
            Check(!SpeechStream.Sustainable(0.0, 0.0),
                "and an unmeasured machine does not stream on hope");
        }

        static void TestSpeechSamples()
        {
            Console.WriteLine("Feathered line edges — the pop is a step from zero:");
            // TWO HEADS, TWO FATES — the gate is the test. A fixed 25ms mute
            // ate the "S" of a render that started speaking at sample zero
            // and Jafar heard a "tch" where the onset was. The click this
            // repair exists for is only audible against SILENCE, so:
            // a sustained head is a voice and keeps its onset...
            var wav = new float[24000];
            for (int i = 0; i < wav.Length; i++) wav[i] = 0.8f;
            SpeechSamples.Feather(wav, 24000);
            Check(wav[300] == 0.8f,
                "a render that starts speaking at sample zero KEEPS its onset — "
                + "the unconditional mute here is what turned an S into a tch");
            Check(wav[0] == 0f && wav[100] < wav[200],
                "while the fade still rises from zero, which no click survives");
            Check(Math.Abs(wav[wav.Length - 1]) < 1e-6f,
                "and the last sample is zero, for the pop in reverse");
            Check(wav[12000] == 0.8f,
                "the middle of the line is untouched — this is edge shaping, "
                + "not a volume change");
            // ...and a loud instant against silence is a click and dies.
            var clicky = new float[24000];
            for (int i = 0; i < 200; i++) clicky[i] = 0.5f;
            for (int i = 200; i < 3000; i++) clicky[i] = 0.001f;
            for (int i = 3000; i < clicky.Length; i++) clicky[i] = 0.8f;
            SpeechSamples.Feather(clicky, 24000);
            Check(clicky[100] == 0f,
                "an isolated transient against silence is muted — the "
                + "cold-vocoder click, by its own signature",
                clicky[100].ToString("0.000"));
            Check(clicky[3500] == 0.8f,
                "and the speech further in is untouched by the verdict on "
                + "the head");
            // A MUTTER SURVIVES ITS OWN FADES. 24000 samples of ramp against
            // a 100-sample clip would silence the whole word.
            var blip = new float[100];
            for (int i = 0; i < blip.Length; i++) blip[i] = 0.5f;
            SpeechSamples.Feather(blip, 24000);
            Check(blip[50] != 0f,
                "a clip shorter than mute+ramps keeps its middle — each repair "
                + "clamps instead of eating the word");
            // AND THE DEGENERATE INPUTS ARE A NO-OP, NOT A THROW. This runs
            // on the audio worker, where an exception takes the process down.
            // ---- THE "AH" BEFORE THE "No.", and the "S" that must survive it.
            //
            // Built to the shape measured in the take Jafar judged: 70ms of
            // quiet sound, 50ms of silence, then the word eight times louder.
            var ah = new float[24000];
            for (int i = 0; i < 1680; i++)            // 70ms head at 0.08
                ah[i] = (float)(0.08 * Math.Sin(i * 0.30));
            for (int i = 2880; i < 24000; i++)        // word from 120ms at 0.62
                ah[i] = (float)(0.62 * Math.Sin(i * 0.21));
            int cutAh = SpeechSamples.TrimDetachedHead(ah, 24000);
            Check(cutAh > 0, "A DETACHED HEAD IS CUT — the 'ah' before the word",
                  "cut " + cutAh + " samples");
            Check(Math.Abs(ah[0]) > 0.3f,
                  "and the line now STARTS on the word rather than on the noise",
                  ah[0].ToString("0.000"));

            // The accepting case, and it is the one that matters: a soft
            // consonant running straight into a vowel has no gap, and the
            // mute that ignored that ate an S the day after it shipped.
            var ess = new float[24000];
            for (int i = 0; i < 2400; i++)            // quiet "S" 0-100ms
                ess[i] = (float)(0.05 * Math.Sin(i * 0.9));
            for (int i = 2400; i < 24000; i++)        // straight into the vowel
                ess[i] = (float)(0.6 * Math.Sin(i * 0.21));
            Check(SpeechSamples.TrimDetachedHead(ess, 24000) == 0,
                  "AND A SOFT ONSET WITH NO GAP IS LEFT ALONE — no silence "
                  + "inside it means it is a word, however quiet");

            // A line that simply begins in silence has no head at all.
            var late = new float[24000];
            for (int i = 4800; i < 24000; i++) late[i] = (float)(0.6 * Math.Sin(i * 0.21));
            Check(SpeechSamples.TrimDetachedHead(late, 24000) == 0,
                  "and a line that starts in silence is not a detached head");

            // A short loud clip must not be eaten for having a pause in it.
            var pause = new float[24000];
            for (int i = 0; i < 3000; i++) pause[i] = (float)(0.6 * Math.Sin(i * 0.21));
            for (int i = 6000; i < 24000; i++) pause[i] = (float)(0.6 * Math.Sin(i * 0.21));
            Check(SpeechSamples.TrimDetachedHead(pause, 24000) == 0,
                  "and a full-level first word followed by a pause is speech, "
                  + "not a head — loudness is what tells them apart");

            // ---- AND NOW THE REAL RECORDING, BECAUSE THE FIXTURES ABOVE
            // ---- WERE BUILT TO MY OWN DIAGNOSIS.
            //
            // Jafar asked how we can be sure the "ah" is gone, and the
            // honest answer was that we could not: every check above uses a
            // signal I synthesised to the shape I had decided the fault was.
            // That is a test of the code against my belief, and it is fooled
            // by exactly the case where the belief is wrong.
            //
            // `fixture-detached-head.wav` is the first 1.4s of the take he
            // judged — the actual "No." with the actual "ah" in front of it,
            // kept because a real rejecting case cannot be argued with. The
            // detector below is the one that FOUND the fault (10ms windows,
            // leading sound then a real gap), so the assertion is measured
            // the same way the complaint was.
            var real = ReadWavMono(Root("game-design/voice-live/fixture-detached-head.wav"));
            if (real != null && real.Length > 24000)
            {
                Check(SpeechSamples.DetachedHeadMs(real, 24000) > 0,
                      "THE KEPT RECORDING STILL HAS THE FAULT — a fixture that "
                      + "quietly stopped failing would prove nothing",
                      SpeechSamples.DetachedHeadMs(real, 24000) + "ms");
                int cutReal = SpeechSamples.TrimDetachedHead(real, 24000);
                Check(cutReal > 0, "and the trim fires on it", cutReal + " samples");
                Check(SpeechSamples.DetachedHeadMs(real, 24000) == 0,
                      "AND THE 'AH' JAFAR HEARD IS MEASURABLY GONE from the "
                      + "real audio, not from a signal I invented");
                double peak = 0;
                foreach (var x in real) if (Math.Abs(x) > peak) peak = Math.Abs(x);
                Check(peak > 0.3, "and the word itself survived the cut",
                      peak.ToString("0.00"));
            }
            else
            {
                Check(false, "the kept recording is readable",
                      "no fixture-detached-head.wav — the real-audio check "
                      + "cannot run and this must not read as a pass");
            }

            // ---- COUNTING WHAT WAS SAID, on the recording that has two.
            var two = ReadWavMono(Root("game-design/voice-live/fixture-detached-head.wav"));
            if (two != null && two.Length > 24000)
            {
                Check(SpeechSamples.Utterances(two, 24000) >= 2,
                      "THE 'ah ... No.' RENDER COUNTS AS MORE THAN ONE "
                      + "UTTERANCE, which is the fault stated as a number",
                      SpeechSamples.Utterances(two, 24000) + " parts");
            }
            var one = new float[24000];
            for (int i = 2400; i < 14400; i++) one[i] = (float)(0.6 * Math.Sin(i * 0.21));
            Check(SpeechSamples.Utterances(one, 24000) == 1,
                  "AND A SINGLE CLEAN LINE COUNTS AS ONE — the accepting case, "
                  + "without which every render looks broken");
            var gapless = new float[24000];
            for (int i = 0; i < 24000; i++) gapless[i] = (float)(0.6 * Math.Sin(i * 0.21));
            Check(SpeechSamples.Utterances(gapless, 24000) == 1,
                  "and continuous speech with no silence at all is still one");
            Check(SpeechSamples.Utterances(new float[24000], 24000) == 0,
                  "and pure silence is nothing said, not one thing said");

            SpeechSamples.TrimDetachedHead(null, 24000);
            SpeechSamples.TrimDetachedHead(new float[0], 24000);
            SpeechSamples.TrimDetachedHead(new float[10], 0);
            Check(true, "and the trim survives null, empty and a zero rate");

            SpeechSamples.Feather(null, 24000);
            SpeechSamples.Feather(new float[0], 24000);
            SpeechSamples.Feather(new float[10], 0);
            Check(true, "null, empty and zero-rate inputs pass through harmlessly");
        }

        static void TestSpeechDirector()
        {
            Console.WriteLine("The speech director — what a machine can afford to say:");

            var d = new SpeechDirector();

            // Every zero needs its denominator, and this one has to be right
            // before any of the rest means anything.
            Check(d.Asked == 0 && d.Live == 0,
                "a fresh director has asked nothing — and says so as a count, not a silence");

            Check(d.Route("rocco", "we should talk", banked: true, haveModel: true)
                  == SpeechRoute.Banked,
                "an authored line comes from the bank, free and instant");
            Check(d.Route("rocco", "an improvised remark", banked: false, haveModel: false)
                  == SpeechRoute.NoModel,
                "with no model on the machine, that is its own answer");
            Check(d.Route("", "words", true, true) == SpeechRoute.Nothing
                  && d.Route("rocco", "  ", true, true) == SpeechRoute.Nothing,
                "and nothing to say is neither");

            // THE FIRST LINE ALWAYS GOES THROUGH, or the measurement that
            // would open the gate can never be taken.
            Check(d.StepsPerSecond == 0, "nothing measured yet");
            Check(d.Route("rocco", "a first improvised line", false, true) == SpeechRoute.Live,
                "the first live line is always allowed — a gate that holds itself "
                + "shut can never learn it could have opened");
            Check(d.Projected("anything") == 0,
                "and it projects nothing rather than a guess");

            // ---- a fast machine ----
            var fast = new SpeechDirector();
            fast.Route("rocco", "priming", false, true);
            fast.Observed(new SpeechRun { Steps = 100, Seconds = 1.0,
                                          Stop = SpeechStop.Finished,
                                          Tokens = new int[99] }, "twenty-five characters!");
            Check(Math.Abs(fast.StepsPerSecond - 100) < 1e-9,
                "a hundred steps in a second is a hundred steps a second",
                fast.StepsPerSecond.ToString("0.0"));
            Check(fast.StepsPerUnitMeasured,
                "and a whole line measures the steps a character costs");
            Check(fast.Route("rocco", "a normal length remark", false, true) == SpeechRoute.Live,
                "so a normal line is affordable");

            // ---- a slow one, same code ----
            var slow = new SpeechDirector();
            slow.Route("rocco", "priming", false, true);
            slow.Observed(new SpeechRun { Steps = 100, Seconds = 5.0,
                                          Stop = SpeechStop.Finished,
                                          Tokens = new int[99] }, "twenty-five characters!");
            Check(Math.Abs(slow.StepsPerSecond - 20.0) < 1e-9,
                "and a slow card measures twenty steps a second",
                slow.StepsPerSecond.ToString("0.0"));
            Check(slow.Route("rocco", "a normal length remark", false, true) == SpeechRoute.TooSlow,
                "so a full sentence is refused, and the character simply stays quiet");
            Check(slow.TooSlow == 1 && slow.Asked == 2,   // the priming line, then this one
                "counted against a denominator, so 'no live speech' can be told apart "
                + "from 'nobody asked'", $"{slow.TooSlow}/{slow.Asked}");

            // THE REFUSAL IS PER LINE, NOT A SWITCH THAT LATCHES OFF. A card
            // that cannot afford a sentence can still afford a mutter, and a
            // director that gave up on the machine would throw that away.
            Check(slow.Route("rocco", "hm", false, true) == SpeechRoute.Live,
                "while a two-word mutter still gets through on the same card");

            // ---- and a machine where the honest answer is "none of it" ----
            //
            // Integrated graphics, a laptop on battery, a card already busy
            // with the game. At two steps a second even two characters project
            // past four seconds, and the director says so rather than
            // producing lines that arrive after the moment has gone.
            var crawling = new SpeechDirector();
            crawling.Route("rocco", "priming", false, true);
            crawling.Observed(new SpeechRun { Steps = 100, Seconds = 50.0,
                                              Stop = SpeechStop.Finished,
                                              Tokens = new int[99] }, "twenty-five characters!");
            Check(crawling.Route("rocco", "hm", false, true) == SpeechRoute.TooSlow,
                "on a card doing two steps a second, nothing at all is affordable — "
                + "and that is a measurement, not a policy");

            // ---- a cut-off line still teaches the rate, but not the length ----
            var cut = new SpeechDirector();
            cut.Observed(new SpeechRun { Steps = 40, Seconds = 4.0,
                                         Stop = SpeechStop.Deadline }, "some text here");
            Check(Math.Abs(cut.StepsPerSecond - 10.0) < 1e-9,
                "a line cut by the deadline still measured a rate — the slow machines "
                + "are exactly the ones whose lines get cut");
            Check(!cut.StepsPerUnitMeasured,
                "but NOT how long a line is: it stopped for a reason that has nothing "
                + "to do with the words, and counting it would measure the deadline");

            // And a refused EARLY stop is the same shape from the other side.
            // The fp16 fault this guards against rendered nine words as four
            // tokens; folded in as a whole line, it would teach the director
            // that nine words cost five steps — an estimator poisoned by the
            // exact failure the floor refuses to play.
            var shorted = new SpeechDirector();
            shorted.Observed(new SpeechRun { Steps = 5, Seconds = 0.2,
                                             Stop = SpeechStop.StoppedShort,
                                             Tokens = new int[4] },
                             "Seen the van again. Thursday, same as last Thursday.");
            Check(Math.Abs(shorted.StepsPerSecond - 25.0) < 1e-9,
                "a line the floor refused still measured a rate",
                shorted.StepsPerSecond.ToString("0.0"));
            Check(!shorted.StepsPerUnitMeasured && !shorted.TokensPerStepMeasured,
                "but teaches neither length nor ratio — a broken render is not "
                + "a measurement of the words");

            // ---- the deadline handed to SpeechPlan ----
            Check(fast.Deadline("a normal length remark") < fast.PatienceSeconds,
                "a fast machine gets a tight deadline, so a runaway line frees the "
                + "slot instead of spending the whole budget",
                fast.Deadline("a normal length remark").ToString("0.00"));
            Check(new SpeechDirector().Deadline("anything") == 4.0,
                "and an unmeasured machine gets the full patience, having nothing to "
                + "project from");

            // ---- THE OTHER HALF OF THE WAIT: the decoder ----
            //
            // The step loop chooses sound tokens; a second network turns them
            // into samples, and on the one machine that has run this it was
            // 3.5 seconds of a 7.3-second line. `Projected` measured the first
            // half and was compared against the player's patience, so it was
            // not slightly optimistic — it was answering a different question
            // from the one being asked of it, which is this project's oldest
            // fault wearing a new coat.
            var quiet = new SpeechDirector();
            quiet.Route("rocco", "priming", false, true);
            quiet.Observed(new SpeechRun { Steps = 100, Seconds = 1.0,
                                           Stop = SpeechStop.Finished,
                                           Tokens = new int[100] }, "twenty-five characters!");
            double before = quiet.Projected("a normal length remark");
            Check(!quiet.DecodeMeasured && quiet.DecodeSeconds(100) == 0.0,
                "a machine that has never decoded adds nothing for decoding — the "
                + "honesty arrives with the evidence, not ahead of it");
            quiet.ObservedDecode(100, 2.0);
            Check(quiet.DecodeMeasured
                  && Math.Abs(quiet.DecodeFixedSeconds - 2.0) < 1e-9
                  && quiet.DecodeSecondsPerToken == 0.0,
                "ONE line is a flat cost and no slope: two coefficients cannot be "
                + "separated from one point, and a slope drawn through one looks "
                + "exactly like a slope drawn through fifty",
                $"{quiet.DecodeFixedSeconds:0.00}/{quiet.DecodeSecondsPerToken:0.0000}");
            Check(Math.Abs(quiet.Projected("a normal length remark") - (before + 2.0)) < 1e-9,
                "and the projection grows by it — the number now reaches the sound "
                + "rather than stopping at the tokens",
                $"{before:0.00} -> {quiet.Projected("a normal length remark"):0.00}");

            // TWO LENGTHS SEPARATE THEM, and the fit must recover a straight
            // line exactly or it is publishing a cost nobody can check.
            var fitted = new SpeechDirector();
            fitted.ObservedDecode(50, 2.0);
            fitted.ObservedDecode(100, 3.0);
            Check(Math.Abs(fitted.DecodeFixedSeconds - 1.0) < 1e-9
                  && Math.Abs(fitted.DecodeSecondsPerToken - 0.02) < 1e-9,
                "two lengths recover the fixed cost and the per-token one exactly",
                $"{fitted.DecodeFixedSeconds:0.000}+{fitted.DecodeSecondsPerToken:0.0000}/tok");
            Check(Math.Abs(fitted.DecodeSeconds(75) - 2.5) < 1e-9,
                "so a length between them is interpolated rather than guessed",
                fitted.DecodeSeconds(75).ToString("0.000"));

            // A LONGER LINE THAT HAPPENED TO RUN FASTER IS NOISE, NOT A
            // DISCOUNT. Left alone the fit slopes downward, which says a long
            // sentence decodes quicker and, extended, that a very long one
            // costs nothing at all.
            var noisy = new SpeechDirector();
            noisy.ObservedDecode(50, 3.0);
            noisy.ObservedDecode(100, 2.0);
            Check(noisy.DecodeSecondsPerToken == 0.0 && noisy.DecodeFixedSeconds >= 0.0
                  && noisy.DecodeSeconds(1000) < 100.0,
                "a downward slope is clamped to flat rather than promising that a "
                + "long line is free",
                $"{noisy.DecodeFixedSeconds:0.00}/{noisy.DecodeSecondsPerToken:0.0000}");

            // A DECODE THAT PRODUCED NOTHING IS NOT A MEASUREMENT. Zero tokens
            // or zero seconds is the absence of a decode, and folding it in
            // would drag the fixed cost toward whatever failed.
            var empty = new SpeechDirector();
            empty.ObservedDecode(0, 3.0);
            empty.ObservedDecode(100, 0.0);
            Check(!empty.DecodeMeasured,
                "and a decode with no tokens or no time in it is not folded in at all");

            // THE DEADLINE HAS TO LEAVE ROOM FOR IT. This bounds the step loop
            // only, so handing it the whole of the player's patience spends the
            // budget before the second half of the work begins.
            // MEASURED SLOW ENOUGH THAT THE PATIENCE IS WHAT BINDS. On a fast
            // machine the loop's own estimate is the smaller of the two and
            // the leftover budget never comes into it, so a test built on one
            // would pass whatever this code did — which is what the first
            // version of this check did, reading 1.91 before and after.
            var roomy = new SpeechDirector();
            roomy.Route("rocco", "priming", false, true);
            roomy.Observed(new SpeechRun { Steps = 100, Seconds = 3.0,
                                           Stop = SpeechStop.Finished,
                                           Tokens = new int[100] }, "twenty-five characters!");
            double wideOpen = roomy.Deadline("a normal length remark");
            roomy.ObservedDecode(100, 2.0);
            double squeezed = roomy.Deadline("a normal length remark");
            Check(squeezed < wideOpen && squeezed <= roomy.PatienceSeconds - 2.0 + 1e-9,
                "once the decoder's cost is known the loop is given what is LEFT of "
                + "the patience, not all of it",
                $"{wideOpen:0.00} -> {squeezed:0.00}");
            Check(roomy.Deadline("a normal length remark") >= 0.5,
                "and never so little that the loop cannot take a step");
            // AND A DECODER THAT EATS THE WHOLE BUDGET STILL LEAVES A FLOOR
            // rather than a deadline of zero, which would cut every line
            // before its first step and report it as the machine being slow.
            var swamped = new SpeechDirector();
            swamped.Route("rocco", "priming", false, true);
            swamped.Observed(new SpeechRun { Steps = 100, Seconds = 3.0,
                                             Stop = SpeechStop.Finished,
                                             Tokens = new int[100] }, "twenty-five characters!");
            swamped.ObservedDecode(100, 30.0);
            Check(swamped.Deadline("a normal length remark") == 0.5,
                "a decoder costing more than the whole patience floors the loop's "
                + "deadline instead of taking it below zero",
                swamped.Deadline("a normal length remark").ToString("0.00"));

            // HOW MANY STEPS ARE SOUND, learned rather than assumed to be all
            // of them. The projection counts steps and the decoder charges for
            // tokens; a silent 1:1 between them is the kind of quiet
            // conversion this file exists to stop.
            var ratio = new SpeechDirector();
            ratio.Observed(new SpeechRun { Steps = 100, Seconds = 1.0,
                                           Stop = SpeechStop.Finished,
                                           Tokens = new int[80] }, "twenty-five characters!");
            Check(ratio.TokensPerStepMeasured && Math.Abs(ratio.TokensPerStep - 0.8) < 1e-9,
                "eighty sound tokens from a hundred steps measures the ratio",
                ratio.TokensPerStep.ToString("0.00"));
            var cutRatio = new SpeechDirector();
            cutRatio.Observed(new SpeechRun { Steps = 100, Seconds = 1.0,
                                              Stop = SpeechStop.Deadline,
                                              Tokens = new int[10] }, "twenty-five characters!");
            Check(!cutRatio.TokensPerStepMeasured,
                "while a line cut off mid-sentence measures where the deadline fell, "
                + "not what the model does");

            // ---- length is counted in TOKENS when a tokeniser is handed in ----
            //
            // The model charges one step per TOKEN, not per character, and the
            // two disagree in both directions: "the" is one token, "ZQXJ" is
            // four. A director measuring characters was answering a question
            // the model does not ask.
            var byChar = new SpeechDirector();
            var byToken = new SpeechDirector { Length = t => t.Length / 4 };
            foreach (var dir in new[] { byChar, byToken })
            {
                dir.Route("rocco", "priming", false, true);
                dir.Observed(new SpeechRun { Steps = 100, Seconds = 5.0,
                                             Stop = SpeechStop.Finished,
                                             Tokens = new int[99] }, "twenty-five characters!");
            }
            Check(byToken.StepsPerUnit > byChar.StepsPerUnit * 3,
                "a line of few tokens costs MORE steps each than a line of many "
                + "characters — the unit changes the answer, which is why it moved",
                $"{byToken.StepsPerUnit:0.0} vs {byChar.StepsPerUnit:0.0}");
            // AND THEY AGREE ON THE LINE THEY MEASURED ON, which is the only
            // line they must: there, units x steps-per-unit is the step count
            // exactly, whatever the unit. On any OTHER line they differ, and
            // differing is the point — that is the better estimate arriving.
            // The first version of this check claimed they agree everywhere,
            // which would have meant the change did nothing.
            Check(Math.Abs(byToken.Projected("twenty-five characters!")
                           - byChar.Projected("twenty-five characters!")) < 1e-6,
                "and both project the line they measured on identically — the "
                + "unit cancels there, so this is a recalibration and not a jump",
                $"{byToken.Projected("twenty-five characters!"):0.000} vs "
                + $"{byChar.Projected("twenty-five characters!"):0.000}");
            Check(Math.Abs(byToken.Projected("the") - byChar.Projected("the")) > 1e-6,
                "and they disagree on a SHORT one, which is the whole reason to "
                + "count tokens: three characters is one token, not three");

            // A TOKENISER THAT THROWS MUST NOT SILENCE THE STREET. The
            // vocabulary is shipped data; a damaged one degrades to counting
            // characters rather than taking the feature down.
            var broken = new SpeechDirector { Length = t => throw new Exception("bad vocab") };
            Check(broken.Route("rocco", "anything at all", false, true) == SpeechRoute.Live,
                "and a tokeniser that throws falls back to characters rather than "
                + "taking live speech down with it");

            // ---- the verdict line ----
            var line = slow.Verdict();
            Check(!line.Contains("= ") && line.Split(' ').Length == 8,
                "the verdict line is eight space-separated pairs", line);
            Check(!new SpeechDirector().Verdict().Contains("0.00 "),
                "and an unmeasured rate says so rather than reporting 0.00, which "
                + "reads as a measurement");
            // THE DECODE'S TWO COEFFICIENTS TRAVEL AS ONE VALUE WITH NO SPACE
            // IN IT. `verdict.txt` is space-separated `key=value`, and a value
            // containing a space is read as a truncated one by every tool that
            // has ever looked at that file — silently, which is the part that
            // cost a morning.
            Check(new SpeechDirector().Verdict().Contains("speechDecodeSec=unmeasured"),
                "a machine that has never decoded says so rather than printing a zero "
                + "cost, which would read as a free decoder");
            Check(fitted.Verdict().Contains("speechDecodeSec=1.00/0.0200")
                  && fitted.Verdict().Split(' ').Length == 8,
                "and once measured both coefficients travel in one value, joined "
                + "without a space so the verdict reader cannot truncate it",
                fitted.Verdict());
        }

        /// Audit item 5: the same character must sound the same next week.
        static void TestVoiceBank()
        {
            Console.WriteLine("The voice bank — a name a generator and a game can both compute:");

            // THE HASH IS THE PROMISE. If this ever changes, every file in
            // the bank is orphaned at once and the symptom is every voice in
            // the game vanishing for no traceable reason. Pinned to literals
            // so a "harmless" refactor of the hash cannot pass silently.
            Check(VoiceBank.Hash("") == 2166136261u, "FNV-1a's offset basis, unchanged");
            Check(VoiceBank.Hash("a") == 0xe40c292cu, "and its published value for \"a\"",
                $"{VoiceBank.Hash("a"):x8}");
            Check(VoiceBank.Hash("rocco") == VoiceBank.Hash("rocco"),
                "the same string hashes the same inside one process");
            Check(VoiceBank.Hash("rocco") != VoiceBank.Hash("rocca"),
                "and one letter apart is a different clip");

            Check(VoiceBank.Normalise("  two   words \n") == "two words",
                "whitespace is collapsed — a line that gained a double space in an "
                + "edit must not orphan its recording");
            Check(VoiceBank.Normalise("No") != VoiceBank.Normalise("NO"),
                "but CASE IS KEPT, because capitals change how an engine reads a line");

            const string said = "He was at the yard on Tuesday.";
            Check(VoiceBank.ClipName("rocco", said) == VoiceBank.ClipName("rocco", "  He was at the yard on Tuesday.  "),
                "a re-indented line is the same recording");
            Check(VoiceBank.ClipName("rocco", said) != VoiceBank.ClipName("lena", said),
                "two people saying the same words are two recordings");
            Check(VoiceBank.ClipName("rocco", said).StartsWith("rocco/"),
                "the voice is the folder, so a recast is a directory nobody has to reindex",
                VoiceBank.ClipName("rocco", said));
            Check(VoiceBank.ClipName("rocco", said).Length == "rocco/".Length + 8,
                "and the name is the voice plus eight hex digits, nothing else",
                VoiceBank.ClipName("rocco", said));
            Check(VoiceBank.ClipName(null, said) == null &&
                  VoiceBank.ClipName("rocco", "   ") == null &&
                  VoiceBank.ClipName("rocco", null) == null,
                "an unspeakable line gets NO plausible-looking path — the one way this "
                + "goes wrong is a caller trusting a name for a clip that cannot exist");

            // No collisions across the whole enumerated bark bank, which is
            // the only test of a hash that means anything.
            var names = new HashSet<string>();
            int lines = 0, collisions = 0;
            foreach (var voice in VoiceBank.Cast)
                for (int i = 0; i < 400; i++)
                {
                    var text = $"Line number {i} about the warehouse on Tuesday, more or less.";
                    lines++;
                    if (!names.Add(VoiceBank.ClipName(voice, text))) collisions++;
                }
            Check(collisions == 0, "no two lines in a bank of thousands share a filename",
                $"{collisions} collisions in {lines}");

            // Determinism: the seed is the name.
            Check(VoiceBank.Seed("rocco", said) == VoiceBank.Seed("rocco", said),
                "the same line seeds the same take — regenerate the bank and nobody drifts");
            Check(VoiceBank.Seed("rocco", said) != VoiceBank.Seed("lena", said),
                "and two voices are two takes");
            foreach (var voice in VoiceBank.Cast)
                Check(VoiceBank.Seed(voice, said) >= 0,
                    $"{voice}'s seed is non-negative — half the RNGs here reject a negative");

            // Casting.
            Check(VoiceBank.VoiceFor("rocco", VoiceBank.Cast) == "rocco",
                "a cast member IS their voice");
            var walker = VoiceBank.VoiceFor("resident_8817", VoiceBank.Cast);
            Check(walker != null && walker.StartsWith("crowd_"),
                "and everybody else draws a crowd voice", walker);
            Check(VoiceBank.VoiceFor("resident_8817", VoiceBank.Cast) == walker,
                "the same walker sounds like the same person every time you pass them");
            Check(VoiceBank.VoiceFor("resident_8817", VoiceBank.Cast, true).StartsWith("crowd_m") &&
                  VoiceBank.VoiceFor("resident_8817", VoiceBank.Cast, false).StartsWith("crowd_f"),
                "a caller who knows the speaker's gender gets a voice that matches it");
            // AND THE GENDERED PATHS MUST SPREAD TOO. Checking only the
            // PREFIX passes when every man on the street is crowd_m1, which
            // is the actual defect worth catching — a break run proved the
            // first version of this test slept through exactly that.
            var men = new HashSet<string>();
            var women = new HashSet<string>();
            for (int i = 0; i < 4000; i++)
            {
                men.Add(VoiceBank.VoiceFor("resident_" + i, VoiceBank.Cast, true));
                women.Add(VoiceBank.VoiceFor("resident_" + i, VoiceBank.Cast, false));
            }
            Check(men.Count == VoiceBank.PoolMasculine.Length &&
                  women.Count == VoiceBank.PoolFeminine.Length,
                "and four thousand of each reach every voice of their own gender, not one",
                $"{men.Count} masculine, {women.Count} feminine");
            Check(VoiceBank.VoiceFor(null, VoiceBank.Cast) == null,
                "and nobody speaking has no voice");

            // THE POOL IS THIN, and the test says the number rather than
            // asserting a comfortable one. Six crowd voices is what the
            // casting sheet funds; if that changes, this changes with it.
            Check(VoiceBank.PoolVoices == 6,
                "six crowd voices — thin for a street, and the fix is casting, not a constant",
                $"{VoiceBank.PoolVoices}");
            var used = new HashSet<string>();
            for (int i = 0; i < 4000; i++)
                used.Add(VoiceBank.VoiceFor("resident_" + i, VoiceBank.Cast));
            Check(used.Count == VoiceBank.PoolVoices,
                "and four thousand walkers reach every one of them, not three",
                string.Join(",", used.OrderBy(v => v)));

            // THE CROSS-LANGUAGE CONTRACT. The generator is Python and the
            // game is C#; there is no shared runtime, so the rule is stated
            // twice and pinned by these exact vectors — the same four are
            // asserted in `tools/voice-fetch/voice_bank.py`. A drift on
            // either side goes red on both with the same numbers instead of
            // the bank silently orphaning itself.
            var vectors = new (string voice, string text, string name, int seed)[]
            {
                ("rocco", "He was at the yard on Tuesday.", "rocco/df92fd5e", 1603468638),
                ("lena", "He was at the yard on Tuesday.", "lena/1d5782f8", 492274424),
                ("crowd_m1", "Evening.", "crowd_m1/953df5cc", 356382156),
                // Outside the basic plane: TWO UTF-16 units here and one
                // Python character there. A naive port of this file passes
                // every other vector and fails only on this one, which is
                // exactly why it is a vector.
                ("rocco", "Told you \U0001F600 nothing.", "rocco/f278f6c6", 1920530118),
            };
            foreach (var v in vectors)
            {
                Check(VoiceBank.ClipName(v.voice, v.text) == v.name,
                    $"vector {v.voice} names {v.name} — the Python generator computes this too",
                    VoiceBank.ClipName(v.voice, v.text));
                Check(VoiceBank.Seed(v.voice, v.text) == v.seed,
                    $"vector {v.voice} seeds {v.seed}",
                    VoiceBank.Seed(v.voice, v.text).ToString());
            }

            Check(VoiceBank.SeedFor("a line") == VoiceBank.SeedFor("a  line") &&
                  VoiceBank.SeedFor("a line") >= 0,
                "the elision seed is stable and non-negative — it used to be "
                + "string.GetHashCode(), which is randomised per process in modern .NET");
        }

        /// Audit item 4: three of §6.2's four channels are audio, so a spec
        /// that calls its redundancy the point was not redundant at all for a
        /// deaf player.
        static void TestCaptions()
        {
            Console.WriteLine("Captions — the channels that are sound with no words in them:");

            const CaptionLevel off = CaptionLevel.Off;
            const CaptionLevel speech = CaptionLevel.Speech;
            const CaptionLevel both = CaptionLevel.SpeechAndSound;

            // OFF IS OFF, and "Speech" must not quietly start captioning
            // sounds — a player who asked for subtitles did not ask for this.
            foreach (var lvl in new[] { off, speech })
            {
                Check(Captions.ForSound(lvl, "slam", 55, 0, 5, 40) == null,
                    $"at {lvl}, a sound gets no caption");
                Check(Captions.ForHush(lvl, 1.0, false) == null,
                    $"at {lvl}, the street going quiet gets no caption");
                Check(Captions.ForAttentionStem(lvl, true) == null,
                    $"at {lvl}, the music turning gets no caption");
            }

            // ---- direction, which is most of the point ----
            Check(Captions.Direction(0) == "ahead" && Captions.Direction(180) == "behind" &&
                  Captions.Direction(90) == "right" && Captions.Direction(270) == "left",
                "the four cardinals name themselves");
            Check(Captions.Direction(45) == "ahead right" && Captions.Direction(225) == "behind left",
                "and the diagonals exist — four arcs would make \"behind\" a hundred and "
                + "eighty degrees, which is the difference between turning round and "
                + "turning the RIGHT way");
            // Centred on the name, not starting at it.
            Check(Captions.Direction(20) == "ahead" && Captions.Direction(-20) == "ahead",
                "an arc is centred on its name rather than starting at it");
            Check(Captions.Direction(-90) == "left" && Captions.Direction(450) == "right" &&
                  Captions.Direction(-450) == "left",
                "and a bearing outside 0..360 still lands somewhere sensible");
            var arcs = new HashSet<string>();
            for (double b = -720; b <= 720; b += 0.5) arcs.Add(Captions.Direction(b));
            Check(arcs.Count == 8, "every bearing lands in one of exactly eight arcs",
                $"{arcs.Count}: {string.Join("|", arcs.OrderBy(a => a))}");

            // ---- and how loud, because loudness is a mechanic here ----
            Check(Captions.Loudness(Perception.LoudShout).Length > 0 &&
                  Captions.Loudness(Perception.LoudFootstepWalk).Length > 0,
                "a shout and a scuff are both marked");
            Check(Captions.Loudness(Perception.LoudShout) != Captions.Loudness(Perception.LoudFootstepWalk),
                "and marked DIFFERENTLY — flattening a slam and a scuff into one line "
                + "throws away the mechanic the noise ring exists for");
            Check(Captions.Loudness(Perception.LoudConversation) == "",
                "while the ordinary case goes unmarked, so the marking means something");

            // ---- the audibility gate: a caption is not an X-ray ----
            Check(Captions.ForSound(both, "slam", Perception.LoudDoorSlam, 180, 60, 40) == null,
                "A SOUND YOU COULD NOT HAVE HEARD IS NOT CAPTIONED — the caption layer is "
                + "the same information in another sense, not more of it");
            Check(Captions.ForSound(both, "slam", Perception.LoudDoorSlam, 180, 5, 40) != null,
                "and one you could have heard is");
            // AT ZERO METRES, which is the case the `radius <= 0` half of the
            // guard actually exists for. A break run proved the first version
            // of this check useless: it asked at five metres, where the OTHER
            // half (`metres > radius`) already returns null, so removing the
            // masking guard changed nothing and the break survived. The
            // reachable case is your own footstep at noon — a sound at your
            // feet that the street has masked out entirely.
            Check(Captions.ForSound(both, "footstep", Perception.LoudFootstepWalk, 0, 0, 0) == null,
                "a sound MASKED TO NOTHING is silent to the captions even at zero metres — "
                + "the whole masking model reused, not a distance check wearing its hat");
            Check(Captions.ForSound(both, "slam", Perception.LoudDoorSlam, 180, 5, 0) == null,
                "and one out past a zero radius is silent too");

            var cap = Captions.ForSound(both, "slam", Perception.LoudDoorSlam, 180, 5, 40);
            Check(cap.StartsWith("[") && cap.EndsWith("]"), "a caption is bracketed", cap);
            Check(cap.Contains("behind"), "and says WHERE, always", cap);
            Check(!cap.Contains("slam\"") && cap.Contains("door"), "in words, not identifiers", cap);
            Check(Captions.ForSound(both, "sfx_door_03", 55, 0, 5, 40) == null &&
                  Captions.ForSound(both, null, 55, 0, 5, 40) == null,
                "AN UNKNOWN KIND IS SILENT rather than printing its own id at the player — "
                + "which is how \"[sfx_door_03]\" ends up in a shipped screenshot");

            // Every kind the game actually emits must have words.
            foreach (var kind in new[] { "speech", "slam", "alarm" })
                Check(Captions.Describe(kind) != null,
                    $"\"{kind}\" is emitted by the game today and must have a caption");

            // ---- the hush: an ABSENCE of sound, and §6.2's best idea ----
            Check(Captions.ForHush(both, 0.9, false) != null,
                "the street going quiet is captioned");
            Check(Captions.ForHush(both, 0.0, false) == null,
                "and an ordinary street is not");
            Check(Captions.ForHush(both, 0.9, true) == null,
                "it is not repeated once shown — a caption that re-fires every frame is a strobe");
            Check(Captions.ForHush(both, 0.0, true) != null,
                "AND IT RUNS BACKWARDS: the street resuming is how the player learns the "
                + "event is over, which is the half stealth games are chronically bad at");
            Check(Captions.ForHush(both, 0.9, false) != Captions.ForHush(both, 0.0, true),
                "and the two directions do not read the same");
            // Hysteresis: no band where both fire, and none where it flickers.
            for (double h = 0; h <= 1.0; h += 0.01)
            {
                bool opens = Captions.ForHush(both, h, false) != null;
                bool closes = Captions.ForHush(both, h, true) != null;
                Check(!(opens && closes),
                    $"at hush {h:0.00} the caption cannot both open and close");
            }
            Check(Captions.HushClearBelow < Captions.HushCaptionAt,
                "the clear threshold sits below the fire threshold, so a street hovering at "
                + "the line does not flicker between the two lines forever");

            // ---- THE TEST THE SPEC ITSELF DEMANDS ----
            //
            // §6.2: "play a scene with the sound off... if either pass leaves
            // the player unable to tell they were noticed, the channels are
            // not redundant and one of them is decoration."
            //
            // With the sound off, channel 3 (behaviour) is visual and
            // survives. Of the three audio channels, how many reach a deaf
            // player? Before this file: one, via subtitles, and only when
            // somebody happened to speak.
            int reachable = 0;
            if (Captions.ForHush(both, 0.9, false) != null) reachable++;          // 1
            if (Captions.ForSound(both, "alarm", Perception.LoudShout, 90, 6, 40) != null) reachable++; // 2
            if (Captions.ForAttentionStem(both, true) != null) reachable++;       // 4
            Check(reachable == 3,
                "SOUND OFF: all three audio channels reach the player, so with the visual "
                + "channel that is four — the redundancy §6.2 claims is now true rather "
                + "than true for hearing players",
                $"{reachable}/3");
            int withoutCaptions = 0;
            if (Captions.ForHush(speech, 0.9, false) != null) withoutCaptions++;
            if (Captions.ForSound(speech, "alarm", Perception.LoudShout, 90, 6, 40) != null) withoutCaptions++;
            if (Captions.ForAttentionStem(speech, true) != null) withoutCaptions++;
            Check(withoutCaptions == 0,
                "and subtitles alone carried NONE of them — which is the hole, measured",
                $"{withoutCaptions}/3");
        }

        static void TestCrowdOnTheStreet()
        {
            Console.WriteLine("The crowd is on the street, not inside the walls:");

            var pop = Population.Generate(700, 1234, new[] { "the Hook", "Copper Row", "Downtown" });
            Check(pop.Residents.Count == 700, "seven hundred residents");

            // THE DEFECT, reproduced as a measurement. Home and work are both
            // inside buildings, so if position is always one of them, almost
            // nobody is ever near a street — which is exactly what the CI
            // density sampler found: 19 bodies within 20m, only 3 of them
            // crowd.
            int outdoors = 0, atADoor = 0;
            foreach (var r in pop.Residents)
            {
                if (!Population.OutdoorPosition(r, 0, 13, out var x, out var z)) continue;
                outdoors++;
                bool onHome = Math.Abs(x - r.HomeX) < 0.001 && Math.Abs(z - r.HomeZ) < 0.001;
                bool onWork = Math.Abs(x - r.WorkX) < 0.001 && Math.Abs(z - r.WorkZ) < 0.001;
                if (onHome || onWork) atADoor++;
            }
            Check(outdoors > 40,
                "a good fraction of the city is outdoors at one in the afternoon",
                $"{outdoors}/700");
            Check(atADoor == 0,
                "and NONE of them are standing in their own doorway — which is where "
                + "every one of them used to be",
                $"{atADoor} still at a door");

            // Indoors must still be indoors, or the whole day/night rhythm goes.
            int outAt3am = 0;
            foreach (var r in pop.Residents)
                if (Population.OutdoorPosition(r, 0, 3, out _, out _)) outAt3am++;
            Check(outAt3am < outdoors / 2,
                "and far fewer are out at three in the morning", $"{outAt3am} vs {outdoors}");

            // Stable within an hour: a person who teleports every frame is
            // worse than one standing in a wall.
            var sample = pop.Residents[42];
            Population.OutdoorPosition(sample, 0, 13, out var x1, out var z1);
            Population.OutdoorPosition(sample, 0, 13, out var x2, out var z2);
            Check(x1 == x2 && z1 == z2, "where somebody stands does not flicker within the hour");

            // But it MOVES across hours, or the street is a diorama of
            // statues.
            int moved = 0;
            foreach (var r in pop.Residents)
            {
                if (!Population.OutdoorPosition(r, 0, 13, out var ax, out var az)) continue;
                if (!Population.OutdoorPosition(r, 0, 14, out var bx, out var bz)) continue;
                if (Math.Abs(ax - bx) > 0.5 || Math.Abs(az - bz) > 0.5) moved++;
            }
            Check(moved > 50,
                "and everybody out at both hours has MOVED between them — a street of "
                + "statues is not a crowd", $"{moved} moved");

            // The thing the first version got wrong, now asserted: presence
            // must not flicker. Somebody outdoors at 13:00 and indoors at
            // 14:00 does not walk home, they vanish — which is the "characters
            // appearing suddenly" complaint reintroduced through another door.
            int flickered = 0, outAt13 = 0;
            foreach (var r in pop.Residents)
            {
                bool a = Population.OutdoorPosition(r, 0, 13, out _, out _);
                bool b = Population.OutdoorPosition(r, 0, 14, out _, out _);
                if (a) outAt13++;
                if (a != b) flickered++;
            }
            Check(outAt13 > 40 && flickered == 0,
                "and NOBODY blinks out of existence between one hour and the next",
                $"{flickered} of {outAt13} flickered");

            // Being out must not correlate with WHERE you stand, or the crowd
            // bunches at one end of every street.
            double lowHalf = 0, total = 0;
            foreach (var r in pop.Residents)
            {
                if (!Population.OutdoorPosition(r, 0, 13, out var px, out _)) continue;
                double span = r.WorkX - r.HomeX;
                if (Math.Abs(span) < 1) continue;
                double t = (px - r.HomeX) / span;
                total++;
                if (t < 0.5) lowHalf++;
            }
            Check(total > 20 && lowHalf / total > 0.25 && lowHalf / total < 0.75,
                "and the outdoor crowd spreads along the route rather than bunching",
                $"{lowHalf / Math.Max(1, total):0.00} in the near half");
        }

        static void TestCombat()
        {
            Console.WriteLine("Combat — violence that works and costs more than it saves:");

            Fighter Guy(string id, double cap = 1.0) =>
                new Fighter { Id = id, Name = id, Capability = cap };

            // ---- reach: a hit that lands from four metres loses the player ----
            var me = Guy("me"); var him = Guy("him");
            Check(!Combat.Available(Blow.Strike, me, him, 4.0),
                "a strike cannot reach across the street");
            Check(Combat.Available(Blow.Strike, me, him, 1.2),
                "but lands at arm's length");
            Check(Combat.Resolve(Blow.Strike, me, him, 4.0).Landed == false,
                "and resolving an unavailable blow does nothing at all");

            // ---- available() and resolve() must agree, or prompts lie ----
            var tired = Guy("tired"); tired.Stamina = 0.05;
            Check(!Combat.Available(Blow.Strike, tired, him, 1.0),
                "an exhausted fighter cannot swing");
            Check(!Combat.Resolve(Blow.Strike, tired, him, 1.0).Landed,
                "and the rules refuse it for the same reason the prompt would grey it out");

            // ---- a tired swing is a weak one ----
            var fresh = Guy("fresh"); var weary = Guy("weary"); weary.Stamina = 0.3;
            var a = Guy("a"); var b = Guy("b");
            double hard = Combat.Resolve(Blow.Strike, fresh, a, 1.0).Force;
            double soft = Combat.Resolve(Blow.Strike, weary, b, 1.0).Force;
            Check(hard > soft, "a tired swing is a weaker one", $"{hard:0.00} vs {soft:0.00}");

            // ---- a hurt fighter hits softer AND goes down sooner ----
            var hurt = Guy("hurt", 0.4);
            var whole = Guy("whole");
            double hurtHit = Combat.Resolve(Blow.Strike, hurt, Guy("x"), 1.0).Force;
            double wholeHit = Combat.Resolve(Blow.Strike, whole, Guy("y"), 1.0).Force;
            Check(hurtHit < wholeHit, "an injured fighter hits softer");

            // ---- guarding absorbs, never negates ----
            var att = Guy("att"); var def = Guy("def");
            def.Guarding = true;
            var guarded = Combat.Resolve(Blow.Strike, att, def, 1.0);
            Check(guarded.Landed && guarded.Guarded, "a guarded blow still lands");
            Check(def.Punished > 0, "and still hurts — a guard that negates is one you hold forever");
            Check(!def.Guarding, "and it breaks the guard");

            // ---- you can be put down, and only then finished ----
            var victim = Guy("victim");
            var puncher = Guy("puncher");
            int swings = 0;
            while (victim.Footing != Footing.Down && swings < 20)
            {
                puncher.Stamina = 1.0;                 // isolate the target's side
                Combat.Resolve(Blow.Strike, puncher, victim, 1.0);
                swings++;
            }
            Check(victim.Footing == Footing.Down, "enough clean blows put somebody down");
            Check(swings >= 2,
                "and it is never one punch — a one-shot knockdown is a different genre",
                $"{swings} swings");
            Check(!victim.CanAct, "somebody down cannot act");

            // THE SEPARATION THAT IS THE DESIGN.
            var standing = Guy("standing");
            Check(!Combat.Available(Blow.Finish, puncher, standing, 1.0),
                "FINISHING SOMEBODY STANDING IS IMPOSSIBLE — it is not a combat move, "
                + "it is a decision made in the quiet afterwards");
            Check(Combat.Available(Blow.Finish, puncher, victim, 1.0),
                "only somebody already down can be finished");
            Check(!Combat.Available(Blow.Finish, puncher, victim, 3.0),
                "and not from across the room");
            var kill = Combat.Resolve(Blow.Finish, puncher, victim, 1.0);
            Check(kill.Killed, "and then it is done");

            // Nothing else in the entire verb set can kill. Checked
            // exhaustively rather than by inspection, because "no accidental
            // deaths" is a promise and not a preference.
            bool anyAccident = false;
            foreach (Blow verb in Enum.GetValues(typeof(Blow)))
            {
                if (verb == Blow.Finish) continue;
                for (int i = 0; i < 40; i++)
                {
                    var p = Guy("p"); var q = Guy("q");
                    p.Stamina = 1.0;
                    if (Combat.Resolve(verb, p, q, 1.0).Killed) anyAccident = true;
                }
            }
            Check(!anyAccident,
                "NO verb except Finish can ever kill — not once in every blow at every state");

            // ---- back off is always available, because leaving must be ----
            var cornered = Guy("cornered"); cornered.Stamina = 0;
            Check(Combat.Available(Blow.BackOff, cornered, him, 0.5),
                "you can always leave, even exhausted and up against somebody");

            // ---- stamina comes back by NOT swinging ----
            var winded = Guy("winded"); winded.Stamina = 0.2;
            Combat.Breathe(winded, 3.0);
            Check(winded.Stamina > 0.2 && winded.Stamina <= 1.0,
                "standing off gets your wind back", $"{winded.Stamina:0.00}");

            // ---- WHO SAW IT: the half of combat that is actually the game ----
            Check(Violence.Confidence(2, false) > Violence.Confidence(20, false),
                "a fight at your elbow is surer than one down the street");
            Check(Violence.Confidence(2, true) < Violence.Confidence(2, false),
                "and through a wall you know something happened, not what");
            Check(Violence.Confidence(2, true) <= 0.5,
                "capped, because hearing is not seeing", $"{Violence.Confidence(2, true):0.00}");
            Check(Violence.Confidence(200, false) == 0, "and across the district, nothing");
            Check(Violence.Confidence(2, false) > Acoustics.OverheardConfidence(2, false),
                "you do not need to make out words to know what you are looking at");

            var nearby = new List<FightWitness>
            {
                new FightWitness { Id = "close", Metres = 3 },
                new FightWitness { Id = "far", Metres = 200 },
                new FightWitness { Id = "wall", Metres = 3, Occluded = true },
            };
            var saw = Violence.Saw(nearby);
            Check(saw.Count == 2 && saw.Exists(w => w.Id == "close") && saw.Exists(w => w.Id == "wall"),
                "only the people who could have carried it away are witnesses",
                string.Join(",", saw.ConvertAll(w => w.Id)));

            // The alley at three versus the bar at noon. This difference IS
            // the game.
            Check(Violence.Notoriety(0, false) < Violence.Notoriety(6, false),
                "a fight nobody saw is not the day's news");
            Check(Violence.Notoriety(0, true) >= 0.75,
                "but a KILLING nobody saw is still enormous — a body is not a rumour",
                $"{Violence.Notoriety(0, true):0.00}");

            // ---- NOTORIETY IS NOT HEAT, AND THIS IS THE CLAIM (M21) --------
            //
            // `Access` has gated doors on notoriety for weeks while `AccessHost`
            // fed it `CurrentHeat` — one variable under two names. The whole
            // point of separating them is that they answer different questions
            // on different timescales, so the tests assert the DIFFERENCE
            // rather than the numbers.
            var fame = new Campaign();
            Check(fame.Notoriety == 0, "a new man is nobody");

            fame.Noted(Violence.Notoriety(6, false));
            double afterBrawl = fame.Notoriety;
            Check(afterBrawl > 0, "a brawl six people watched is worth something",
                $"{afterBrawl:0.00}");

            // EACH ACT CLOSES SOME OF THE GAP, AND THE FIRST VERSION TOOK A
            // MAXIMUM. That assertion read "a smaller act afterwards does not
            // make you MORE known", and it was defensible for exactly as long
            // as violence was the only source: reputation is what you are known
            // FOR, and a brawl does not make a killing worse.
            //
            // With a second source it is wrong, and wrong in this project's
            // most expensive direction. A maximum means the loudest event
            // permanently silences every other, so informing — wired, tested
            // and running — could never move the number once anybody had been
            // killed. Built, and invisible.
            // ONE WITNESS, NOT ZERO. `Violence.Notoriety(0, false)` is exactly
            // zero — a fight nobody saw is worth nothing, which is the model
            // working — and `Noted` returns early on a weight of zero, so the
            // first version of this assertion compared 0.70 against 0.70 and
            // would have passed under EITHER rule. A test that cannot fail for
            // the reason it was written is the shape rule 5b is about.
            fame.Noted(Violence.Notoriety(1, false));
            Check(fame.Notoriety > afterBrawl,
                "a smaller act afterwards still makes you a little better known",
                $"{afterBrawl:0.00} -> {fame.Notoriety:0.00}");

            fame.Noted(Violence.Notoriety(0, true));
            Check(fame.Notoriety >= 0.75,
                "and a killing is enormous whatever came before it",
                $"{fame.Notoriety:0.00}");

            // IT SATURATES, AND THE TEST CORRECTED THE CLAIM I WROTE BESIDE IT.
            //
            // The comment said it "approaches one and cannot reach it", which is
            // true of the algebra and false of the arithmetic. A witnessed
            // killing is worth 0.75, so the gap shrinks by a factor of four each
            // time — 0.750, 0.938, 0.984 — and by the twenty-seventh the gap is
            // 0.25^27, smaller than a double can hold beside 1.0. It lands on
            // exactly 1.0 and stays there.
            //
            // That is the right BEHAVIOUR — somebody who has killed twenty-seven
            // people in front of witnesses is as known as it is possible to be —
            // and the wrong SENTENCE, which is the shape rule 2 keeps catching:
            // a property asserted in prose that the code does not have. What is
            // asserted now is what is true: it climbs, never exceeds one, and a
            // realistic career is very well known without being pinned there.
            var loud = new Campaign();
            double last = 0;
            bool climbs = true;
            for (int i = 0; i < 200; i++)
            {
                loud.Noted(Violence.Notoriety(9, true));
                if (loud.Notoriety < last || loud.Notoriety > 1.0) climbs = false;
                last = loud.Notoriety;
            }
            Check(climbs && loud.Notoriety == 1.0,
                "two hundred witnessed killings climb monotonically to total notoriety",
                $"{loud.Notoriety:0.0000}");

            var career = new Campaign();
            career.Noted(Violence.Notoriety(3, true));
            career.Noted(Violence.Notoriety(6, false));
            Check(career.Notoriety > 0.8 && career.Notoriety < 1.0,
                "one killing and one public brawl is very well known, and not yet maximal",
                $"{career.Notoriety:0.0000}");

            // ONE ACT LANDS EXACTLY AT ITS OWN WEIGHT, from nothing — identical
            // to what the maximum did, which is why no existing reading of this
            // number changes shape.
            var once = new Campaign();
            once.Noted(0.42);
            Check(System.Math.Abs(once.Notoriety - 0.42) < 1e-9,
                "the first act lands at exactly its own weight",
                $"{once.Notoriety:0.0000}");

            // ---- INFORMING IS THE SECOND SOURCE, AND THE ORDER IS THE DESIGN
            //
            // The magnitudes are authored constants like `Violence.Notoriety`'s
            // division by six. What is asserted is the ORDERING, because that is
            // the claim a reader would want to argue with.
            double charged = Informing.Notoriety(Accusation.Charged, 0.8, seen: false);
            double blew = Informing.Notoriety(Accusation.BlewBack, 0.8, seen: false);
            double noted = Informing.Notoriety(Accusation.Noted, 0.8, seen: false);
            double ignored = Informing.Notoriety(Accusation.Ignored, 0.8, seen: false);
            Check(charged > blew && blew > noted && noted > ignored,
                "a charge that sticks is the loudest, and being caught lying is next",
                $"{charged:0.00} {blew:0.00} {noted:0.00} {ignored:0.00}");
            Check(Informing.Notoriety(Accusation.Charged, 0.8, seen: true) >
                  Informing.Notoriety(Accusation.Charged, 0.8, seen: false),
                "being SEEN going in is worth more than going in");
            Check(Informing.Notoriety(Accusation.Charged, 0.9, seen: true) <
                  Violence.Notoriety(0, killed: true),
                "and none of it reaches what a killing is worth",
                $"{Informing.Notoriety(Accusation.Charged, 0.9, true):0.00} < "
                + $"{Violence.Notoriety(0, true):0.00}");
            Check(Informing.Notoriety(Accusation.Charged, 0.1, seen: false) <
                  Informing.Notoriety(Accusation.Charged, 0.9, seen: false),
                "a charge six people would back is louder than one nobody would");

            // AND IT FADES ON A DIFFERENT CLOCK FROM HEAT, which is the entire
            // reason it is a second number. Six weeks of complete quiet still
            // leaves a man who killed somebody halfway known.
            double known = fame.Notoriety;
            fame.FadeNotoriety(42);
            Check(fame.Notoriety > known / 2.0,
                "six weeks of quiet does not make a killer anonymous",
                $"{known:0.00} -> {fame.Notoriety:0.00}");
            Check(fame.Notoriety < known,
                "but it does fade — being known is not permanent either");

            // FOUR SITES OF ONE IDEA, AND TWO MORE WERE MISSING THE LINE.
            // Found by grepping for the flag after fixing the second, which is
            // the mechanical step rule 1's third corollary asks for. `Leads`
            // and the day-circle heat both skipped a leashed agent BEFORE
            // looking at their rumours, so a hooked witness to a killing gave
            // the player no lead and added nothing to the heat — while telling
            // everybody they met about it through the two paths that were
            // already correct.
            var bodyGraph = new SocialGraph();
            var bodyMill = new GossipMill(bodyGraph);
            var hooked = Agent("hooked", "Zora", "day");
            bodyMill.Add(hooked);
            bodyMill.Witness("hooked", new Fact("player", "killed", "yes"),
                             "I saw him do it.", sensitive: true,
                             now: new GameTime(1, 22, 0), confidence: 0.9,
                             indelible: true);
            bodyMill.Witness("hooked", new Fact("player", "met", "Rocco"),
                             "He was with Rocco.", sensitive: true,
                             now: new GameTime(1, 22, 0), confidence: 0.9);
            hooked.Leashed = true;

            var leads = bodyMill.Leads("player");
            Check(leads.Exists(l => l.TopicKey.Contains("killed")),
                "a hooked witness to a body is still a lead the player can work",
                $"{leads.Count} lead(s)");
            Check(!leads.Exists(l => l.TopicKey.Contains("met")),
                "and the leash still hides everything else they hold");
            Check(bodyMill.DayCircleHeat() > 0,
                "and the body still counts towards what the day circle believes",
                $"{bodyMill.DayCircleHeat():0.00}");

            // ---- THE PAPER: THE ONE CHANNEL WITH NO HOPS -----------------
            //
            // Every other way information moves here is person to person and
            // decays with distance, which is the moat and is right. It also
            // means a killing in an empty alley is known to nobody for ever,
            // and notoriety can only be bought with witnesses. A town has a
            // newspaper; each of its three rules is a refusal.

            // MOST THINGS ARE NOT NEWS, on the scale that already grades how
            // loud an act is rather than a second one invented here.
            Check(Press.Print(3, Violence.Notoriety(0, killed: false), Inquiry.Manhunt,
                              lethal: false, place: "Hook Street") == null,
                "a fight nobody watched is not in the paper");
            Check(Press.Print(3, Violence.Notoriety(6, killed: false), Inquiry.Manhunt,
                              lethal: false, place: "Hook Street") != null,
                "a brawl six people watched is");

            // A BODY ALWAYS IS, whatever anybody saw. `HomicideBook`'s own note
            // says a body does not stay a rumour, and this is the mechanism by
            // which that becomes true for people who were nowhere near it.
            var quietKill = Press.Print(3, Violence.Notoriety(0, killed: true), Inquiry.Procedure,
                                        lethal: true, place: "Hook Street");
            Check(quietKill != null, "a killing nobody saw is still in the paper");

            // AND IT DOES NOT KNOW SECRETS. With nothing the street would tell
            // a detective, the story runs WITHOUT the name — which is the more
            // interesting outcome: the town knows a man was killed and does not
            // know it was you.
            Check(!quietKill.NamesYou && quietKill.Content.Subject != "player",
                "with the law not asking about you it prints the act and not the name",
                quietKill.Headline);
            Check(Press.Notoriety(quietKill) == 0,
                "and an unnamed story makes you no better known — that is a "
                + "different thing, not a smaller one");

            var named = Press.Print(3, Violence.Notoriety(4, killed: true),
                                    Inquiry.Investigation,
                                    lethal: true, place: "Hook Street");
            Check(named.NamesYou && named.Content.Subject == "player",
                "once the law is asking about you by name, so does the paper",
                named.Headline);

            // THE PRINTED FACT MUST BE THE SAME FACT A WITNESS HOLDS, or a
            // story read and a story seen would stack as two separate beliefs
            // instead of corroborating — the distinction the day-circle heat
            // reading is built on.
            Check(named.Content.Predicate == "killed",
                "and on the same topic a witness would use, so the two corroborate");

            // A READER IS NOT A WITNESS. Reused from the phone layer rather
            // than picked again, so the game cannot come to hold two opinions
            // about what secondhand is worth.
            Check(named.Confidence < Violence.Notoriety(4, killed: true)
                  && named.Confidence > 0,
                "a reader believes less than somebody who was there",
                $"{named.Confidence:0.00}");

            // ---- A BODY CANNOT BE MANAGED OFF THE TABLE, ON EITHER PATH --
            //
            // `Tick` has always exempted an indelible rumour from the leash,
            // from suppression and from the confidence floor, on the design
            // that no amount of information landscaping makes Ellis's case
            // answerable once there is a corpse. `CompareNotes` — a detective
            // asking somebody straight out — exempted it from none of them, so
            // a hook bought silence about a body under direct questioning while
            // the same witness would have volunteered it in ordinary talk.
            var hushGraph = new SocialGraph();
            var hush = new GossipMill(hushGraph);
            var witnessToBody = Agent("saw", "Vera", "day");
            var detective = Agent("asks", "Ellis", "day");
            hush.Add(witnessToBody);
            hush.Add(detective);
            hushGraph.Link("asks", "saw", 0.9);
            var body = new Fact("player", "killed", "yes");
            hush.Witness("saw", body, "I watched him do it.", sensitive: true,
                         now: new GameTime(1, 22, 0), confidence: 0.9, indelible: true);
            witnessToBody.Leashed = true;
            var told = hush.CompareNotes("asks", "saw", new GameTime(1, 23, 0));
            Check(detective.Rumors.Exists(r => r.Content.Predicate == "killed"),
                "a leashed witness asked straight out about a body still answers",
                $"{detective.Rumors.Count} rumour(s) passed, {told.Count} event(s)");

            // AND THE LEASH STILL HOLDS FOR EVERYTHING ELSE, which is the half
            // that makes the exemption a design rather than a hole.
            var quietGraph = new SocialGraph();
            var quiet = new GossipMill(quietGraph);
            var seen2 = Agent("seen2", "Remy", "day");
            var asks2 = Agent("asks2", "Ellis", "day");
            quiet.Add(seen2);
            quiet.Add(asks2);
            quietGraph.Link("asks2", "seen2", 0.9);
            quiet.Witness("seen2", new Fact("player", "met", "Rocco"),
                          "He was talking to Rocco.", sensitive: true,
                          now: new GameTime(1, 22, 0), confidence: 0.9);
            seen2.Leashed = true;
            quiet.CompareNotes("asks2", "seen2", new GameTime(1, 23, 0));
            Check(!asks2.Rumors.Exists(r => r.Content.Predicate == "met"),
                "but a leashed witness still says nothing about anything else");

            // ---- M21: SHE RINGS YOU, AND NOT PICKING UP IS AN ANSWER ------
            //
            // The roadmap has said for weeks that the rival is a person rather
            // than a stage counter, and that what is missing is her RINGING
            // you: `ResolveTable` already takes accept, defy and counter, and
            // all three require the player to be in the room. A call has a
            // fourth answer those cannot express — not being there — and it is
            // the one the rest of this game is built to make interesting.
            var she = new EmpireBook();
            var kest = she.ArmOf("dockside");

            // A QUIET ARM DOES NOT RING. Stage 0 is "quiet"; a call from
            // somebody who has not noticed you is the game telling the player
            // they matter rather than the world deciding it.
            kest.Stage = 0; kest.Attention = 1.0; kest.LastActDay = -1;
            Check(Summoning.Due(kest, 5, 20) == null,
                "an arm that has not noticed you does not telephone you");

            // NOR ONE THAT IS NOT THINKING ABOUT YOU.
            kest.Stage = 2; kest.Attention = 0.2;
            Check(Summoning.Due(kest, 5, 20) == null,
                "nor one whose attention you do not have");

            kest.Attention = 0.8;
            var ring = Summoning.Due(kest, 5, 20);
            Check(ring != null && ring.ArmId == "dockside" && ring.Day == 5,
                "a rival at stage two with your attention rings you");

            // DETERMINISTIC, AND THAT IS THE POINT RATHER THAN A CONVENIENCE.
            // A roll here would mean two loads of one save differ in whether
            // the phone rang, and this whole design turns on the player being
            // able to believe what happened followed from what they did.
            var again = Summoning.Due(kest, 5, 20);
            Check(again != null && again.Terms == ring.Terms,
                "and asking twice gives the same call, not a second roll");

            // SHE RINGS IN THE EVENING, WHATEVER HOUR THE QUESTION IS ASKED.
            // The day turns at eight in the morning, so hanging the call on
            // that hour would have her telephoning a publican at eight a.m.
            // about a share of his rackets — and would ask a callbox whether it
            // was live at an hour it is not, making the miss the world's fault
            // rather than the player's.
            Check(ring.Hour == Summoning.RingsAtHour && ring.Hour >= 18,
                "she rings in the evening even when asked at the day's close",
                $"asked at 20, rings at {ring.Hour}");
            var atDawn = Summoning.Due(kest, 5, 8);
            Check(atDawn != null && atDawn.Hour == ring.Hour,
                "and asking at eight in the morning does not move it");

            // THE ORDERING IS THE DESIGN. Magnitudes are authored; what is
            // asserted is that taking the call is the only answer that can gain
            // standing, that refusing to her face costs most, and that missing
            // sits between them — a man who is never reachable is telling you
            // something, but he has not SAID it and she cannot repeat it.
            Check(Summoning.StandingChange(Answered.Took) > 0,
                "taking the call is the only answer that can gain you anything");
            Check(Summoning.StandingChange(Answered.Missed)
                  > Summoning.StandingChange(Answered.Refused),
                "missing costs less than refusing to her face",
                $"{Summoning.StandingChange(Answered.Missed):0.00} vs "
                + $"{Summoning.StandingChange(Answered.Refused):0.00}");
            Check(Summoning.StandingChange(Answered.Missed) < 0,
                "and it is not free — never being reachable is its own answer");

            // MISSING LEAVES THE MATTER LIVE. Taking the call buys attention
            // back the way a settlement does; refusing spikes it the way defying
            // her at a table does; missing moves it not at all, so she rings
            // again.
            Check(Summoning.AttentionChange(Answered.Took) < 0
                  && Summoning.AttentionChange(Answered.Missed) == 0
                  && Summoning.AttentionChange(Answered.Refused) > 0,
                "a missed call leaves her attention exactly where it was");

            // AND THE CLOCK MOVES ON A MISS, which is the one that would have
            // been forgotten. `Due` refuses to ring again for three days from
            // the last act; if a miss did not count as an act she would ring
            // every day until somebody answered — harassment reachable only
            // through the answer that does not involve the player at all.
            kest.LastActDay = -1;
            var missed = Summoning.Due(kest, 10, 21);
            Summoning.Apply(she, missed, Answered.Missed, 10);
            Check(Summoning.Due(kest, 11, 21) == null,
                "she does not ring again the next day just because nobody answered");
            Check(Summoning.Due(kest, 13, 21) != null,
                "but she does three days later");

            // ---- THE SYSTEM MUST NOT BE INERT (BalanceLab, 2026-07-28) ----
            //
            // The original constants made a clean strike do 0.86 against a
            // floor of 1.0, so a fight was over in TWO BLOWS and stamina fell
            // from 1.00 to 0.88 across the whole thing. Guard, footing and
            // stamina were all decorative — they never got a turn — and the
            // fight lab's verdict was that mashing Strike won 76% of
            // exchanges while taking the LEAST punishment, which is exactly
            // what combat-spec §2 says breaks the fiction.
            //
            // None of the tests above could see it. Every one of them was
            // true, and the system was still hollow. That is the difference
            // between checking rules and checking BALANCE, and it is why the
            // lab exists.
            {
                var swinger = Guy("swinger");
                var taker = Guy("taker");
                int clean = 0;
                while (taker.Footing != Footing.Down && clean < 20)
                {
                    if (!Combat.Available(Blow.Strike, swinger, taker, 1.0)) break;
                    Combat.Resolve(Blow.Strike, swinger, taker, 1.0);
                    clean++;
                    Combat.Breathe(swinger, 0.9);
                }
                Check(clean >= 3,
                    "a fight takes at least three committed swings — at two, stamina and "
                    + "guard and footing never get a turn and the whole file is decoration",
                    $"{clean} blows");
                Check(swinger.Stamina < 0.55,
                    "AND THE SWINGER IS SPENT BY THE END. A fighter who can mash and "
                    + "recover has no reason ever to stop, which is the mechanic "
                    + "StrikeStamina was written for and could not reach",
                    $"{swinger.Stamina:0.00} left");
            }
            {
                // The consequence that makes it a decision: a tired swing is
                // dramatically weaker, not marginally.
                var rested = Guy("f2"); var spent = Guy("s2");
                var a2 = Guy("a2"); var b2 = Guy("b2");
                double full = Combat.Resolve(Blow.Strike, rested, a2, 1.0).Force;
                spent.Stamina = 0.4;
                double weak = Combat.Resolve(Blow.Strike, spent, b2, 1.0).Force;
                Check(weak < full * 0.85,
                    "and an exhausted swing lands meaningfully softer, so spending "
                    + "everything early is a decision with a price",
                    $"{weak:0.00} vs {full:0.00}");
            }
            {
                // Guard has to be worth the turn it costs.
                var hitter = Guy("h3");
                var blocking = Guy("g3"); blocking.Guarding = true;
                var open = Guy("o3");
                double stopped = Combat.Resolve(Blow.Strike, hitter, blocking, 1.0).Force;
                hitter.Stamina = 1.0;
                double through = Combat.Resolve(Blow.Strike, hitter, open, 1.0).Force;
                Check(stopped < through * 0.35,
                    "a guard saves most of a blow — at a third saved it cost a whole turn "
                    + "to avoid a third of one hit, which is a losing trade in every "
                    + "situation, so the verb existed and nobody would ever have used it",
                    $"{stopped:0.00} vs {through:0.00}");
            }

            // ---- THE ASYMMETRY: a body cannot be discredited ----
            Check(Violence.KillingConfidence(3, false) >= 0.95,
                "seeing a killing is being CERTAIN of it");
            Check(Violence.KillingConfidence(3, false) > Acoustics.OverheardConfidence(3, false),
                "far past anything the gossip mill lets an overheard thing reach");
            var mill = new GossipMill(new SocialGraph());
            var eyes = Agent("eyes", "Eyes", "night");
            mill.Add(eyes);
            var killing = new Fact("player", "killed_d5", "true");
            mill.Witness("eyes", killing, "watched him do it", true, new GameTime(5, 23, 0),
                Violence.KillingConfidence(3, false));
            Check(eyes.Knowledge.CheckClaim(killing) == ClaimResult.Consistent,
                "so unlike EVERY other thing in this game, it becomes hard knowledge — "
                + "which is exactly what makes killing terrifying rather than efficient");

            // -- WIND, SPENT BY RUNNING ---------------------------------------
            //
            // `Rig.BreathRate` runs from fifteen breaths a minute to fifty-one
            // and `PlayerController` fed it the literal 1.0 since it was
            // written, waiting for a combat system that is deliberately last.
            //
            // THE ACCEPTING CASE FIRST, and here it is the ordinary one:
            // walking must GIVE wind back. A drain that fired at walking pace
            // would leave the player permanently winded from crossing a room,
            // and it would look exactly like the model working.
            double walked = Combat.StaminaAfterMoving(0.5, Locomotion.WalkSpeed, 1.0);
            Check(walked > 0.5, "walking pace gives wind back, it does not cost any",
                  $"0.50 -> {walked:0.000}");
            double stood = Combat.StaminaAfterMoving(0.5, 0.0, 1.0);
            Check(stood > 0.5 && System.Math.Abs(stood - walked) < 1e-9,
                  "and standing still is the same — below walking pace nothing is spent",
                  $"{stood:0.000}");

            // AND THE CASE IT EXISTS FOR.
            double sprinted = Combat.StaminaAfterMoving(1.0, Locomotion.RunSpeed, 1.0);
            Check(sprinted < 1.0, "a sprint costs wind", $"1.00 -> {sprinted:0.000}");

            // THE RELATIONSHIP, ASSERTED RATHER THAN THE NUMBER. The drain is
            // stated as "at full sprint you lose it as fast as you regain it
            // standing", which is a claim a test can hold and a picked constant
            // is not.
            double regained = Combat.StaminaAfterMoving(0.0, 0.0, 1.0);
            Check(System.Math.Abs((1.0 - sprinted) - regained) < 1e-9,
                  "and at full sprint it costs exactly what standing still returns, "
                  + "which is the stated relationship rather than a number I picked",
                  $"{1.0 - sprinted:0.000} vs {regained:0.000}");

            // BETWEEN THE TWO IT SCALES, so a jog is not a sprint.
            double jogged = Combat.StaminaAfterMoving(1.0,
                (Locomotion.WalkSpeed + Locomotion.RunSpeed) / 2.0, 1.0);
            Check(jogged > sprinted && jogged < 1.0,
                  "a jog costs something, and less than a sprint",
                  $"{jogged:0.000} between {sprinted:0.000} and 1.000");

            Check(Combat.StaminaAfterMoving(1.0, Locomotion.RunSpeed, 0.0) == 1.0
                  && Combat.StaminaAfterMoving(0.0, Locomotion.RunSpeed, 999.0) >= 0.0,
                  "no time is no change, and it never goes below empty");

            // THE TWO WAYS TO GET YOUR WIND BACK ARE ONE WAY.
            //
            // `Breathe` recovers a Fighter between exchanges and
            // `StaminaAfterMoving` recovers anybody below walking pace. Those
            // were the same arithmetic written twice, an hour apart, agreeing
            // by coincidence — the shape rule 1 calls the most repeated fault
            // here, where the copy nobody reads is the one missing a line.
            //
            // This does not assert the FORMULA, which would just be the
            // duplication moved into the test. It asserts that the two paths
            // land in the same place, which is the property that was never
            // held and the one that would break if either drifted.
            var resting = new Fighter { Stamina = 0.4 };
            Combat.Breathe(resting, 2.0);
            double stoodInstead = Combat.StaminaAfterMoving(0.4, 0.0, 2.0);
            Check(System.Math.Abs(resting.Stamina - stoodInstead) < 1e-12,
                  "breathing between exchanges and standing still give back the same wind, "
                  + "because they are now the same line of code",
                  $"{resting.Stamina:0.0000} vs {stoodInstead:0.0000}");

            // And the shared floor and ceiling hold from either door.
            var toppedUp = new Fighter { Stamina = 0.9 };
            Combat.Breathe(toppedUp, 999.0);
            Check(toppedUp.Stamina == 1.0 && Combat.Recovered(0.9, 999.0) == 1.0
                  && Combat.Recovered(0.5, 0.0) == 0.5 && Combat.Recovered(0.5, -1.0) == 0.5,
                  "wind stops at full, and no time is no change",
                  $"{toppedUp.Stamina:0.000}");
        }

        static void TestHomicide()
        {
            Console.WriteLine("The body — combat phase 3b, the price of the lethality answer:");
            var now = new GameTime(6, 23, 0);

            GossipMill Street(params string[] ids)
            {
                var g = new SocialGraph();
                for (int i = 0; i < ids.Length; i++)
                    for (int j = i + 1; j < ids.Length; j++)
                        g.Link(ids[i], ids[j], 0.9);
                var m = new GossipMill(g);
                foreach (var id in ids) m.Add(Agent(id, id, "night"));
                return m;
            }

            // ---- THE ASYMMETRY, one machine at a time ----
            // Every containment tool in the game, aimed at a body, one by one.
            // If any of these bite, killing is just another problem you can pay
            // your way out of, and the entire point of the feature is gone.
            {
                var mill = Street("saw");
                var book = new HomicideBook();
                var k = book.Record("victim", "The Victim", 6, 23, "the alley");
                k.SawYouDoIt.Add("saw");
                book.FileWith(mill, k, now);

                var held = mill.Get("saw").BestOfValue(k.TopicKey, "true");
                Check(held != null && held.Indelible && held.Confidence >= 0.95,
                    "a witness to a killing carries it as a fact, at certainty");

                // 1. Time.
                mill.Age(now);
                mill.Age(new GameTime(60, 23, 0));   // fifty-four days of lying low
                var after = mill.Get("saw").BestOfValue(k.TopicKey, "true");
                Check(after != null && after.Confidence >= 0.95,
                    "fifty-four days of lying low does nothing to it",
                    after == null ? "gone" : $"{after.Confidence:0.00}");

                // 2. Denial.
                var dc = mill.Discredit(k.TopicKey, "true", now);
                Check(dc.Outcome == DcOutcome.Indelible,
                    "denying it is refused outright — and NOT as 'no such rumour', "
                    + "because telling the player it died down would be a lie");
                Check(mill.Get("saw").BestOfValue(k.TopicKey, "true").Confidence >= 0.95,
                    "and the denial changed nothing");
                Check(!mill.IsDiscredited(k.TopicKey),
                    "nor did it burn the once-per-story denial on the way past");

                // 3. Money.
                mill.Get("saw").Greed = 1.0;
                var br = mill.Bribe("saw", k.TopicKey, 100000, now);
                Check(br.Outcome == DcOutcome.Indelible,
                    "the greediest man on the street will not take money for it");
                Check(mill.Get("saw").BestOfValue(k.TopicKey, "true").Confidence >= 0.95,
                    "and he is still carrying it at certainty");

                // 4. Fear.
                mill.Get("saw").Nerve = 0.0;
                var it = mill.Intimidate("saw", k.TopicKey, now);
                Check(it.Outcome == DcOutcome.Indelible,
                    "and the most frightened man on the street cannot be frightened off it");

                // 5. A hook.
                mill.Get("saw").Leashed = true;
                mill.Get("saw").Suppressed.Add(k.TopicKey);
                var mill2 = mill;
                var evs = mill2.Tick(now, (x, y) => true);
                Check(evs.Count == 0, "with nobody to tell, nothing moves");
            }

            // ---- it still SPREADS through a leash and a bribe ----
            {
                var mill = Street("saw", "b", "c");
                var book = new HomicideBook();
                var k = book.Record("victim", "The Victim", 6, 23, "the alley");
                k.SawYouDoIt.Add("saw");
                book.FileWith(mill, k, now);
                mill.Get("saw").Leashed = true;
                mill.Get("saw").Suppressed.Add(k.TopicKey);

                mill.Tick(now, (x, y) => true);
                var heard = mill.Get("b")?.BestOfValue(k.TopicKey, "true");
                Check(heard != null,
                    "a leashed, bribed, frightened witness tells it anyway — "
                    + "silence is something you buy about stories, not about bodies");
                Check(heard != null && heard.Confidence >= 0.95,
                    "and it arrives as true as it left, with no hop decay at all",
                    heard == null ? "gone" : $"{heard.Confidence:0.00} at {heard.Hops} hop(s)");
                Check(mill.Get("b").Knowledge.CheckClaim(k.Fact) == ClaimResult.Consistent,
                    "so a man who only HEARD about it can still catch you in a denial");
            }

            // ---- the contradiction still fires, which is the whole point ----
            {
                var mill = Street("saw", "b");
                var book = new HomicideBook();
                var k = book.Record("victim", "The Victim", 6, 23, "the alley");
                k.SawYouDoIt.Add("saw");
                book.FileWith(mill, k, now);
                // The player looked b in the eye and said it wasn't him.
                mill.PlayerClaims("b", new Fact("player", "killed_victim", "false"), now);
                double before = mill.Get("b").Suspicion.Value;
                var evs = mill.Tick(now, (x, y) => true);
                Check(evs.Exists(e => e.ToId == "b" && e.Contradiction),
                    "the lie is caught the moment the body reaches the man you told it to");
                Check(mill.Get("b").Suspicion.Value > before,
                    "and it costs, rather than being noted and dropped");
            }

            // ---- THE ARITHMETIC OF THE TRADE ----
            // This is the part the whole feature stands or falls on. Killing a
            // witness must genuinely work, and must never pay for itself.
            {
                var mill = Street("w1", "w2", "w3");
                var book = new HomicideBook();
                var dead = new HashSet<string>();
                Func<string, bool> alive = id => !dead.Contains(id);

                var first = book.Record("mark", "The Mark", 6, 23, "the alley");
                first.SawYouDoIt.Add("w1");
                book.FileWith(mill, first, now, alive);

                double p1 = book.Pressure(mill, alive);
                Check(book.Stage(mill, alive) == Inquiry.Manhunt,
                    "one killing with one living eyewitness IS a manhunt", $"{p1:0.00}");

                // So you kill the witness. It works. That has to be true or the
                // choice is fake.
                var second = book.Record("w1", "The Witness", 7, 2, "the yard");
                dead.Add("w1");
                book.FileWith(mill, second, now, alive);
                double p2 = book.Pressure(mill, alive);
                Check(book.Stage(mill, alive) == Inquiry.Investigation,
                    "killing the only witness GENUINELY takes the manhunt off you — "
                    + "if it did not, the player would stop believing the system", $"{p2:0.00}");
                Check(p2 < p1, "the pressure really does come down", $"{p2:0.00} < {p1:0.00}");
                Check(book.Stage(mill, alive) > Inquiry.Procedure,
                    "and it NEVER takes you back to where one body left you");

                // A third, to fix the second.
                var third = book.Record("w2", "Another", 8, 1, "the canal");
                dead.Add("w2");
                book.FileWith(mill, third, now, alive);
                Check(book.Stage(mill, alive) == Inquiry.Manhunt,
                    "and the body you added to fix the last one puts you past where you started",
                    $"{book.Pressure(mill, alive):0.00}");
                Check(book.Pressure(mill, alive) > p1,
                    "worse, measurably, than the manhunt you were solving",
                    $"{book.Pressure(mill, alive):0.00} > {p1:0.00}");
            }

            // ---- a body nobody saw is still a case ----
            {
                var mill = Street("nobody");
                var book = new HomicideBook();
                var k = book.Record("mark", "The Mark", 6, 3, "the canal");
                book.FileWith(mill, k, now);
                Check(book.Stage(mill) == Inquiry.Procedure,
                    "a killing in an empty street at three in the morning is still a homicide file");
                Check(Police.SummonsEllis(book.Stage(mill)),
                    "which puts Ellis on the street whatever the talk is doing");
                Check(!Police.AsksAboutYou(book.Stage(mill)),
                    "but she is not asking about you, because nobody can put you there");
            }

            // ---- witnesses who cannot name you still escalate ----
            {
                var mill = Street("heard1", "heard2");
                var book = new HomicideBook();
                var k = book.Record("mark", "The Mark", 6, 3, "the alley");
                k.KnowsOfIt.Add("heard1");
                k.KnowsOfIt.Add("heard2");
                book.FileWith(mill, k, now);
                Check(book.LiveWitnesses(mill).Count == 0,
                    "someone who knows there is a body cannot testify that you made it");
                Check(mill.Get("heard1").BestOfValue("mark.died", "violently") != null,
                    "but they carry the death itself, as a fact");
                Check(book.Stage(mill) == Inquiry.Procedure,
                    "so the case opens without your name on it");
            }

            // ---- corroboration is what turns a word into a case ----
            {
                var one = Street("a"); var many = Street("a", "b", "c");
                var b1 = new HomicideBook(); var b2 = new HomicideBook();
                var k1 = b1.Record("v", "V", 6, 23, "x"); k1.SawYouDoIt.Add("a");
                var k2 = b2.Record("v", "V", 6, 23, "x");
                k2.SawYouDoIt.Add("a"); k2.SawYouDoIt.Add("b"); k2.SawYouDoIt.Add("c");
                b1.FileWith(one, k1, now); b2.FileWith(many, k2, now);
                Check(b2.Pressure(many) > b1.Pressure(one),
                    "three people saying it is worse than one saying it",
                    $"{b2.Pressure(many):0.00} vs {b1.Pressure(one):0.00}");
            }

            // ---- the same body twice is one body ----
            {
                var book = new HomicideBook();
                book.Record("v", "V", 6, 1, "x");
                book.Record("v", "V", 6, 1, "x");
                Check(book.BodyCount == 1,
                    "recording the same killing twice does not double the pressure off one act");
            }

            // ---- police consequences ----
            Check(Police.RumorHalfLifeHours(Inquiry.Investigation, 96)
                  > Police.RumorHalfLifeHours(Inquiry.Procedure, 96),
                "nothing about you goes cold while she is asking your name");
            Check(Police.RumorHalfLifeHours(Inquiry.None, 96) == 96,
                "and with no body, the street forgets at its normal pace");
            Check(Police.SuspicionFloor(Inquiry.Manhunt) > Police.SuspicionFloor(Inquiry.Investigation)
                  && Police.SuspicionFloor(Inquiry.None) == 0,
                "the suspicion floor rises with the inquiry and is zero without one");
            Check(Police.ForcesActThree(Inquiry.Investigation) && !Police.ForcesActThree(Inquiry.Procedure),
                "a case with your name on it cannot be waited out; an open file can");
            Check(Police.BarsQuietExit(Inquiry.Manhunt) && !Police.BarsQuietExit(Inquiry.Investigation),
                "and you cannot hand the bar to a successor and walk away from a manhunt");

            // ---- the crew who watched ----
            {
                var steady = Agent("steady", "Steady", "night");
                var nervous = Agent("nervous", "Nervous", "night");
                steady.Nerve = 0.9; steady.Loyalty = 1.0;
                nervous.Nerve = 0.2; nervous.Loyalty = 1.0;
                Watched.Saw(steady, now);
                Watched.Saw(nervous, now);
                Check(steady.Loyalty < 1.0 && nervous.Loyalty < steady.Loyalty,
                    "nobody who watched is quite the same, and the nervous one least of all",
                    $"steady {steady.Loyalty:0.00} vs nervous {nervous.Loyalty:0.00}");

                double ceiling = nervous.Loyalty;
                nervous.Loyalty = 1.0;          // pay them, protect them, supply the need
                Watched.Saw(nervous, now);
                Check(nervous.Loyalty <= ceiling + 1e-9,
                    "and no amount of paying them well ever lifts the ceiling back off",
                    $"{nervous.Loyalty:0.00} vs {ceiling:0.00}");
                int marks = nervous.Memory.Events.Count(e => e.Text.StartsWith("I watched them do it"));
                Check(marks == 1,
                    "held down nightly without grinding them to nothing or repeating the memory",
                    $"{marks} memory/ies");

                Check(Watched.WouldTalkToPolice(nervous) && !Watched.WouldTalkToPolice(steady),
                    "the one who goes to the police is the frightened one, not the disloyal one");
            }

            // ---- what a body does to Act III ----
            {
                var mill = Street("saw");
                var book = new HomicideBook();
                var k = book.Record("v", "V", 6, 23, "the alley");
                k.SawYouDoIt.Add("saw");
                book.FileWith(mill, k, now);
                // Every tool the player has for managing the landscape, at once.
                mill.Get("saw").Leashed = true;
                mill.Get("saw").Suppressed.Add(k.TopicKey);
                mill.Discredit(k.TopicKey, "true", now);
                Check(mill.StrongestSurvivingPlayerLead() >= LedgerState.CaseStandsAt,
                    "a body is the one lead that cannot be managed off the table, "
                    + "so Ellis's case stands however well you handle the street",
                    $"{mill.StrongestSurvivingPlayerLead():0.00}");

                var s = new LedgerState { HandedOver = true, HasReadySuccessor = true };
                Check(ActThreeState.Eligible(s).Contains(Ending.Quiet),
                    "handing the bar over is normally the quietest door out");
                s.Hunted = true;
                Check(!ActThreeState.Eligible(s).Contains(Ending.Quiet),
                    "and a successor can inherit a licence but never a homicide — "
                    + "killing takes the quiet ending off the table outright");

                // D58, CONDITION 1 (queue 399, Jafar 21 September: "confirm that
                // the two endings left to a hunted player ... are actually
                // reachable from a hunted state"). Traced 28 September: neither
                // the Kingdom's nor the Straight Life's condition reads Hunted,
                // and Hunted is set in one place (ActThreeHost.Books, from
                // Police.BarsQuietExit). What a body does besides: Ellis's case
                // stands (the check above), which only Both needs and which costs
                // the Kingdom the 0.7 easing of what the inspection sees; and a
                // witness's loyalty is capped by their nerve (Watched). Nothing
                // in the Core lowers anyone's loyalty for a killing or a manhunt
                // otherwise, and no arrest ends the run before the audit closes.
                var huntedKeeps = new LedgerState
                {
                    Hunted = true, EllisCaseAnswerable = false,          // the body's lead stands
                    BusinessesOwned = 1, RacketsEstablished = 1,
                    TotalRacketIncome = 1000, TotalWashed = 600, TakingsToDate = 4000, Cooperations = 3,
                    BestDayLifeLoyalty = 0.2,                             // nobody who knew him before
                };
                Check(ActThreeState.Eligible(huntedKeeps).Contains(Ending.Kingdom) && ActThreeState.Resolve(huntedKeeps) == Ending.Kingdom,
                    "a hunted player who kept the business, with books that hold, reaches the Kingdom",
                    string.Join(",", ActThreeState.Eligible(huntedKeeps)) + $" seen {ActThreeState.SeenStrain(huntedKeeps):0.00}");
                var huntedGivesUp = new LedgerState
                {
                    Hunted = true, EllisCaseAnswerable = false,
                    BusinessesOwned = 1, EmpireDissolved = true,          // sold up
                    BestDayLifeLoyalty = 0.6,                             // one friend still counts him
                };
                var huntedNeverBuilt = new LedgerState { Hunted = true, EllisCaseAnswerable = false, BestDayLifeLoyalty = 0.6 };
                Check(ActThreeState.Resolve(huntedGivesUp) == Ending.StraightLife && ActThreeState.Resolve(huntedNeverBuilt) == Ending.StraightLife,
                    "and one who gave up the business, or never built it, and kept a friend reaches the Straight Life",
                    ActThreeState.Resolve(huntedGivesUp) + " / " + ActThreeState.Resolve(huntedNeverBuilt));
                Check(Watched.LoyaltyCeiling(0.2) < LedgerState.TrustThreshold && Watched.LoyaltyCeiling(0.5) >= LedgerState.TrustThreshold,
                    "the friend can be a witness with a steady hand (nerve 0.4 or more), or anyone who never watched: "
                    + "only a nervous witness is capped below a friend's loyalty",
                    $"{Watched.LoyaltyCeiling(0.2):0.00} / {Watched.LoyaltyCeiling(0.5):0.00}");
            }

            // ---- it survives a save ----
            {
                var book = new HomicideBook();
                var k = book.Record("v", "The Victim", 6, 23, "the alley");
                k.SawYouDoIt.Add("saw"); k.KnowsOfIt.Add("heard");
                // Through actual JSON TEXT, not the dictionary — an int stays an
                // int in a dictionary and becomes a double through a file, and
                // a codec test that skips the text tests the wrong thing.
                var back = new HomicideBook();
                back.FromJson(MiniJson.Deserialize(MiniJson.Serialize(book.ToJson()))
                    as System.Collections.Generic.Dictionary<string, object>);
                var r = back.Of("v");
                Check(back.BodyCount == 1 && r != null && r.VictimName == "The Victim"
                      && r.Day == 6 && r.Hour == 23 && r.Where == "the alley"
                      && r.SawYouDoIt.Contains("saw") && r.KnowsOfIt.Contains("heard"),
                    "a killing round-trips through a save with its witnesses intact");
            }
            {
                var mill = Street("saw");
                var k = new HomicideBook().Record("v", "V", 6, 23, "x");
                k.SawYouDoIt.Add("saw");
                new HomicideBook().FileWith(mill, k, now);
                var json = SaveCodec.Capture(now, new Wallet(0), new Campaign(), new PlayerKnowledge(),
                    new SecretsBook(), new BeatBook(), mill, new DebtBook(), null);
                var mill2 = Street("saw");
                SaveCodec.RestoreMillAgents(json, mill2);
                var r = mill2.Get("saw")?.BestOfValue(k.TopicKey, "true");
                Check(r != null && r.Indelible,
                    "and a body reloads as a body rather than as an ordinary rumour "
                    + "that a night's sleep would wash out");
            }
        }

        static void TestLightModel()
        {
            Console.WriteLine("Light model — the cheapest large win in the project (the-gap.md §3a):");

            // ---- TONE MAPPING: the difference between a photograph and a clamp ----
            Check(LightModel.Aces(0) == 0, "black stays black");
            bool monotone = true;
            double prev = -1;
            for (double x = 0; x <= 8.0; x += 0.01)
            {
                double y = LightModel.Aces(x);
                if (y < prev - 1e-12) monotone = false;
                prev = y;
            }
            Check(monotone, "and the curve never goes backwards, so no brighter input is darker out");
            bool inRange = true;
            for (double x = 0; x <= 200; x += 0.5)
                if (LightModel.Aces(x) > 1.0 || LightModel.Aces(x) < 0) inRange = false;
            Check(inRange, "nothing leaves the curve out of range, however hot the light");

            // The property the whole thing exists for. A linear clamp takes
            // everything over 1.0 to white and a red sign becomes a white
            // rectangle — the exact defect the neon pass had, one level down.
            double midIn = 0.4, hotIn = 3.0;
            double midGain = LightModel.Aces(midIn) / midIn;
            double hotGain = LightModel.Aces(hotIn) / hotIn;
            // A linear clamp also passes a naive compression ratio (1.0 vs
            // 0.33), so the discriminating check is where the ROLL-OFF
            // starts: a filmic curve is already bending well below white,
            // and a clamp is dead straight until it hits the wall.
            Check(LightModel.Aces(1.0) < 0.85,
                "the curve is already rolling off at 1.0 rather than running straight "
                + "into a wall, which is what a clamp does",
                $"{LightModel.Aces(1.0):0.000}");
            Check(hotGain < midGain * 0.5,
                "highlights are COMPRESSED far harder than midtones — that roll-off "
                + "is what keeps hue in a bright sign instead of clipping it to white",
                $"mid x{midGain:0.00} vs hot x{hotGain:0.00}");
            Check(LightModel.Aces(3.0) > LightModel.Aces(1.5),
                "and a hotter light is still brighter, rather than flattening to one value");

            // ---- EXPOSURE: night STOPS DOWN, and that is the third revision ----
            //
            // 0.55 was sized for an unlit street, 0.10 for one with light
            // shafts, and this one also has wet asphalt that really reflects
            // the lamps — measurably, into fourteen percent of a night frame,
            // as of this morning. Every version of this number was authored
            // against a street with less light in it than the street has now.
            Check(LightModel.Exposure(1.0) < LightModel.Exposure(0.0),
                "night stops the aperture DOWN, because the lamps and their reflections "
                + "are doing the lifting — opening up on top of them pays twice for light "
                + "the scene already has, and costs the one property a night must keep",
                $"{LightModel.Exposure(1.0):0.000} at night against "
                + $"{LightModel.Exposure(0.0):0.000} by day");
            Check(LightModel.Exposure(1.0) > 0.85,
                "but not so far that an unlit corner goes to nothing — this is a stop, "
                + "not a fade");

            // AND THE GAP IS THE CLAIM, not the ordering. Night came out
            // exactly equal to noon once the stop-down landed — 0.117 against
            // 0.117 — which an ordering check calls a near miss and a
            // photographer calls impossible. A midday street and a midnight
            // one exposed identically is the actual defect, and only a margin
            // can see it.
            double dayNightStops = LightModel.Exposure(0.0) / LightModel.Exposure(1.0);
            Check(dayNightStops > 1.15,
                "and noon is exposed a clear step above midnight — an ordering check "
                + "passes on a hair, and two frames a hair apart is a day and a night "
                + "that look the same",
                $"{dayNightStops:0.000}x");
            Check(LightModel.Exposure(0, 1) < LightModel.Exposure(0, 0),
                "an overcast day loses light");
            Check(LightModel.Exposure(1, 1) > LightModel.Exposure(1, 0),
                "but a wet night GAINS it, because everything reflects the lamps");

            // ---- THE SKY, in three bands ----
            var (sr, sg, sb) = LightModel.SkyColour(1.0);
            var (hr, hg, hb) = LightModel.HorizonColour(1.0);
            var (gr, gg, gb) = LightModel.GroundColour(1.0);
            Check(sb > sr && sb > sg, "a night sky is BLUE, not grey");
            Check(sr + sg + sb > 0.05,
                "and never black — a black sky reads as a missing skybox, not as night");
            Check(hr > hb, "the horizon carries the sodium glow of a city on low cloud");
            Check(hr + hg + hb > sr + sg + sb,
                "which is brighter than the sky above it, so the middle distance "
                + "does not fall into a flat void",
                $"horizon {hr+hg+hb:0.000} vs sky {sr+sg+sb:0.000}");
            Check(gr + gg + gb < hr + hg + hb, "and the ground is the darkest band");
            var (dsr, dsg, dsb) = LightModel.SkyColour(0.0);
            Check(dsr + dsg + dsb > sr + sg + sb, "day is brighter than night in every band");

            // Rain takes SATURATION out rather than adding grey.
            double Sat(double r, double g, double b)
            {
                double mx = Math.Max(r, Math.Max(g, b)), mn = Math.Min(r, Math.Min(g, b));
                return mx <= 0 ? 0 : (mx - mn) / mx;
            }
            var (wr, wg, wb) = LightModel.SkyColour(1.0, 1.0);
            Check(Sat(wr, wg, wb) < Sat(sr, sg, sb),
                "rain desaturates the sky rather than greying it down",
                $"{Sat(wr, wg, wb):0.000} vs {Sat(sr, sg, sb):0.000}");

            // ---- FOG: depth cueing, not weather ----
            Check(LightModel.FogDensity(0, 0) > 0,
                "there is always some fog — without it every building sits at the "
                + "same apparent distance");
            Check(LightModel.FogDensity(0, 1) > LightModel.FogDensity(0, 0), "rain thickens it");
            Check(LightModel.FogDensity(1, 0) > LightModel.FogDensity(0, 0), "and so does night");
            Check(LightModel.FogDensity(1, 1) < 0.05,
                "but never so far that you cannot see across the street",
                $"{LightModel.FogDensity(1, 1):0.0000}");

            var (fr, fg, fb) = LightModel.FogColour(1.0);
            // Measured against the horizon it is DERIVED FROM, not against
            // itself. The first version of this check compared r to b and
            // passed with the warm term deleted, because the horizon is
            // already warm — it was testing HorizonColour and reporting on
            // FogColour, which is the third time on this project a metric has
            // measured the wrong thing.
            Check(fr / Math.Max(1e-6, fb) > hr / Math.Max(1e-6, hb) * 1.05,
                "NIGHT FOG IS WARMER THAN THE SKY IT SITS UNDER, because it is lit by "
                + "sodium lamps from inside the scene. Grey fog at night is the single "
                + "most common way a street reads as untextured game rather than photograph",
                $"fog r/b {fr / fb:0.000} vs horizon r/b {hr / hb:0.000}");
            var (dfr, dfg, dfb) = LightModel.FogColour(0.0);
            Check(dfr + dfg + dfb > fr + fg + fb, "and day fog is brighter than night fog");
            Check(fr <= 1 && fg <= 1 && fb <= 1, "fog never leaves the colour range");

            // ---- DUSK (M17.10 V6): the crossover is its own colour ----
            Check(LightModel.Dusk(0) == 0 && LightModel.Dusk(1) == 0,
                "dusk is zero at full day and full night — it is the crossover, not a tint");
            Check(Math.Abs(LightModel.Dusk(0.5) - 1.0) < 1e-9, "and peaks at the half-lit moment");
            Check(Math.Abs(LightModel.Dusk(0.3) - LightModel.Dusk(0.7)) < 1e-9,
                "symmetrically — dawn and dusk are the same sky in this model");
            var (xr, xg, xb) = LightModel.FogColour(0.5);
            Check(xr > xb,
                "THE DUSK HAZE IS WARM — red over blue at the crossover, where a "
                + "plain mix of the cool day arm and the sodium night arm would sit "
                + "between them instead of looking like a low sun",
                $"dusk fog r={xr:0.000} b={xb:0.000}");
            Check(dfr < dfb, "while the day fog it came from stays cool");
            var (duskWetR, _, duskWetB) = LightModel.FogColour(0.5, 1.0);
            Check(duskWetR - duskWetB < (xr - xb) * 0.5,
                "and rain flattens the warmth — an overcast dusk is grey",
                $"wet gap {duskWetR - duskWetB:0.000} vs clear gap {xr - xb:0.000}");

            // ---- VOLUMETRICS ----
            Check(LightModel.Transmittance(0, 0.02) == 1.0, "nothing is absorbed at zero distance");
            Check(LightModel.Transmittance(50, 0.02) < LightModel.Transmittance(5, 0.02),
                "and more of the light is eaten the further it travels");
            Check(LightModel.Transmittance(1e6, 0.02) >= 0 && LightModel.Transmittance(1e6, 0.02) < 1e-6,
                "it approaches zero without ever going negative");
            Check(LightModel.Transmittance(50, 0.05) < LightModel.Transmittance(50, 0.01),
                "thicker fog eats more of it");

            // THE reason volumetric light looks like light.
            double toward = LightModel.Phase(1.0), across = LightModel.Phase(0.0),
                   away = LightModel.Phase(-1.0);
            Check(toward > across && across > away,
                "fog scatters FORWARD — a lamp glows far more looking toward it than "
                + "away, and that asymmetry is why a shaft reads as light rather than "
                + "as a translucent cone-shaped object",
                $"{toward:0.000} / {across:0.000} / {away:0.000}");
            Check(Math.Abs(LightModel.Phase(1.0, 0.0) - LightModel.Phase(-1.0, 0.0)) < 1e-9,
                "and with no anisotropy it is uniform haze — which is what fog on the "
                + "LENS looks like, and is the wrong effect");
            bool phaseFinite = true;
            for (double g = -0.99; g <= 0.99; g += 0.01)
                for (double c = -1; c <= 1; c += 0.05)
                {
                    double v = LightModel.Phase(c, g);
                    if (double.IsNaN(v) || double.IsInfinity(v) || v < 0) phaseFinite = false;
                }
            Check(phaseFinite,
                "and it never divides by zero at grazing angles, however extreme the "
                + "anisotropy — a NaN here is a black or white screen, not a soft bug");

            Check(LightModel.ConeBrightness(100, 13, 1, 0, 0.02) == 0,
                "a lamp throws nothing past its range");
            Check(LightModel.ConeBrightness(3, 13, 1, 0, 0.02)
                  > LightModel.ConeBrightness(9, 13, 1, 0, 0.02),
                "and less the further out you stand in it");
            Check(LightModel.ConeBrightness(3, 13, 1, 0, 0.02)
                  > LightModel.ConeBrightness(3, 13, 1, 0.9, 0.02),
                "the lip of the cone is soft, because a hard edge is a cone-shaped object");
            Check(LightModel.ConeBrightness(3, 13, 1, 0, 0.04)
                  > LightModel.ConeBrightness(3, 13, 1, 0, 0.01),
                "and there is more of it to see in thicker air");
            Check(LightModel.ConeBrightness(0, 13, 1, 0, 0.02) < 1e6,
                "standing in the bulb does not divide by zero");

            // ---- SURFACES: the mistake everybody makes ----
            Check(LightModel.Smoothness(0.15, 1.0) > LightModel.Smoothness(0.15, 0.0),
                "wet ground is shinier");
            Check(LightModel.AlbedoScale(1.0) < LightModel.AlbedoScale(0.0),
                "AND DARKER. A water film fills the micro-structure so less light "
                + "scatters back out. Raising smoothness alone gives polished plastic; "
                + "dropping albedo at the same time is what makes the lamps pop off a "
                + "dark road, which is the whole look of a rainy street at night",
                $"{LightModel.AlbedoScale(1.0):0.00} vs {LightModel.AlbedoScale(0.0):0.00}");
            Check(LightModel.AlbedoScale(1.0) > 0.4,
                "but not so dark the road becomes a hole in the world");
            Check(LightModel.Smoothness(0.15, 1.0) <= 1.0 && LightModel.Smoothness(0.9, 1.0) <= 1.0,
                "and smoothness never leaves its range, however smooth it started");

            // Wetness lags rain in both directions — free continuity.
            double wet = 0;
            for (int i = 0; i < 30; i++) wet = LightModel.Wetness(wet, 1.0, 1.0 / 60.0);
            Check(wet > 0.05 && wet < 1.0, "the street takes time to get wet", $"{wet:0.00}");
            double soaked = 1.0, drying = 1.0;
            for (int i = 0; i < 60; i++) drying = LightModel.Wetness(drying, 0.0, 1.0 / 60.0);
            double wetting = 0;
            for (int i = 0; i < 60; i++) wetting = LightModel.Wetness(wetting, 1.0, 1.0 / 60.0);
            // A REAL MARGIN, not `<`. The first version compared the two
            // rates directly, and with the asymmetry deleted they come out
            // equal to within floating-point noise on two differently-rounded
            // sequences — so the comparison went whichever way the last bits
            // fell, and a deliberate break passed. A test decided by rounding
            // is not a test.
            Check((soaked - drying) < wetting * 0.6,
                "and dries MUCH slower than it wets, so the street still looks like it "
                + "rained half an hour after it stopped",
                $"dried {soaked - drying:0.000} vs wetted {wetting:0.000}");

            // ---- EXPOSURE MUST NOT UNDO THE NIGHT ----
            //
            // Two curves that are each correct alone and wrong together, and
            // nothing tied them: the ambient bands make night about 0.77x as
            // bright as noon, and `Exposure` lifts night by 1.55x to keep the
            // street legible. Multiply them and NIGHT COMES OUT BRIGHTER THAN
            // DAY - the tonemap sees more light at midnight than at midday.
            //
            // It went unnoticed because the post stack was attached to a
            // child of the camera and never ran, so the exposure was never
            // applied to anything at all. The moment that was fixed, this
            // became a rendering bug. Tying the two curves together here
            // means neither can be tuned into contradicting the other again.
            foreach (double rain in new[] { 0.0, 0.5, 1.0 })
            {
                double dayScene = (BandLuma(LightModel.SkyColour(0, rain))
                                   + BandLuma(LightModel.HorizonColour(0, rain))
                                   + BandLuma(LightModel.GroundColour(0, rain))) / 3;
                double nightScene = (BandLuma(LightModel.SkyColour(1, rain))
                                     + BandLuma(LightModel.HorizonColour(1, rain))
                                     + BandLuma(LightModel.GroundColour(1, rain))) / 3;
                double dayLit = LightModel.Aces(dayScene * LightModel.Exposure(0, rain));
                double nightLit = LightModel.Aces(nightScene * LightModel.Exposure(1, rain));
                // 0.45, not the 0.88 this started at. The real margin is
                // 0.23 — night renders at under a quarter of day — so a bound
                // at 0.88 had four times more headroom than the property it
                // was guarding and would have sat green through an exposure
                // lift twice too strong. A test with that much slack states a
                // requirement without enforcing one.
                Check(nightLit < dayLit * 0.45,
                    $"after exposure and the tonemap, night is still clearly darker than "
                    + $"day (rain {rain:0.0}) - a lift that fully compensates the dark is "
                    + "a lift that has deleted the night",
                    $"night {nightLit:0.000} vs day {dayLit:0.000} "
                    + $"(scene {nightScene / dayScene:0.00}x, exposure "
                    + $"{LightModel.Exposure(1, rain) / LightModel.Exposure(0, rain):0.00}x)");
            }
            // The street stays legible at night WITHOUT the aperture, which
            // is the claim that replaces the old one. The tonemapped night
            // scene must still land somewhere a player can read — it is just
            // the lamps and their reflections doing it now rather than a
            // wider aperture applied to everything including the dark.
            Check(LightModel.Aces(0.35 * LightModel.Exposure(1, 0)) > 0.08,
                "a lit night surface is still legible with the aperture stopped down — "
                + "a player who cannot see the street is not experiencing atmosphere, "
                + "they are experiencing a bug report",
                $"{LightModel.Aces(0.35 * LightModel.Exposure(1, 0)):0.000}");

            // ---- BLOOM, WHICH BLEW THE NIGHT OUT ----
            //
            // Third number authored while the post stack was dead. On the
            // first frame it was ever applied to, night came out at 0.549
            // mean luminance against 0.159 at noon.

            Check(LightModel.BloomThreshold(1) > LightModel.BloomThreshold(0),
                "what counts as a highlight RISES at night, because the exposure does "
                + "— a fixed threshold under a moving aperture stops meaning 'the "
                + "lamps' and starts meaning 'half the frame'",
                $"{LightModel.BloomThreshold(0):0.00} by day, "
                + $"{LightModel.BloomThreshold(1):0.00} at night");
            Check(LightModel.BloomThreshold(0) > 0.5 && LightModel.BloomThreshold(1) < 0.95,
                "and it stays a threshold at both ends — never so low it selects the "
                + "whole image, never so high it selects nothing");

            Check(LightModel.BloomStrength(1) < LightModel.BloomStrength(0),
                "and there is LESS bloom at night, not more: this city has three "
                + "hundred and sixty light shafts, so the glow around a lamp is already "
                + "geometry and blooming it again counts it twice",
                $"{LightModel.BloomStrength(0):0.00} vs {LightModel.BloomStrength(1):0.00}");
            double maxBloom = 0;
            for (double n = 0; n <= 1.0001; n += 0.05)
                maxBloom = Math.Max(maxBloom, LightModel.BloomStrength(n));
            Check(maxBloom < 0.5 && LightModel.BloomStrength(0) > 0.1,
                "bloom is added BEFORE the tonemap, so it compounds with everything "
                + "else rather than replacing it — and it is still visible",
                $"peak {maxBloom:0.00}");

            // ---- THE VIGNETTE, WHICH WAS DELETING THE CORNERS ----
            //
            // Authored at 0.34 by day and 0.50 at night, never applied to a
            // frame because the post stack never ran. Those put the corners
            // at 10% of centre and at EXACTLY ZERO respectively — a black
            // frame border, not a vignette, halving the mean luminance of
            // every image in the game.

            Check(LightModel.VignetteAt(0, 0) == 1.0 && LightModel.VignetteAt(0, 1) == 1.0,
                "the middle of the frame is never touched, day or night");
            foreach (double n in new[] { 0.0, 0.5, 1.0 })
            {
                double corner = LightModel.VignetteAt(0.5, n);
                Check(corner > 0.5 && corner < 0.85,
                    $"and a corner is dimmed but plainly still there (night {n:0.0}) — "
                    + "a vignette pulls the eye inward, it does not crop the frame",
                    $"{corner:0.000} of centre");
                Check(Math.Abs(corner - LightModel.VignetteCorner(n)) < 1e-9,
                    $"the shader parameter is solved from the corner we asked for, so "
                    + $"the number in the source is the one you can have an opinion "
                    + $"about (night {n:0.0})",
                    $"asked {LightModel.VignetteCorner(n):0.000}, get {corner:0.000}");
            }
            Check(LightModel.VignetteAt(0.5, 1) < LightModel.VignetteAt(0.5, 0),
                "night closes in a little more than day, which was the original intent "
                + "and survives at a tenth of the original strength");

            bool vigMonotone = true;
            double vigPrev = 2;
            for (double dd = 0; dd <= 0.5001; dd += 0.005)
            {
                double v = LightModel.VignetteAt(dd, 0.5);
                if (v > vigPrev + 1e-9) vigMonotone = false;
                vigPrev = v;
            }
            Check(vigMonotone, "and it darkens outward without ever brightening again");

            // THE WHOLE FRAME, not just the corners. This is the number that
            // actually moved: mean luminance across the image.
            double meanFactor = 0; int samples = 0;
            for (double x = -0.5; x <= 0.5; x += 0.02)
                for (double y = -0.5; y <= 0.5; y += 0.02)
                {
                    meanFactor += LightModel.VignetteAt(x * x + y * y, 0);
                    samples++;
                }
            meanFactor /= samples;
            Check(meanFactor > 0.80,
                "the vignette costs the frame under a fifth of its light overall — the "
                + "authored version cost roughly half, which is why noon rendered at "
                + "0.088 mean luma when the ungraded scene was 0.168",
                $"mean factor {meanFactor:0.000}");

            // ---- AMBIENT OCCLUSION ----
            //
            // The last cheap win: untextured geometry reads flat because
            // nothing sits IN anything. The corner where a bin meets a wall
            // is lit exactly as brightly as open ground, so the bin floats.

            Check(LightModel.AoStrength(1.0, 0) > LightModel.AoStrength(0, 0),
                "occlusion counts for more at night, when nearly all the light is fill "
                + "and there is ambient to block",
                $"{LightModel.AoStrength(1.0, 0):0.00} vs {LightModel.AoStrength(0, 0):0.00}");
            Check(LightModel.AoStrength(0, 1.0) > LightModel.AoStrength(0, 0),
                "and in the rain even at noon, because overcast flattens daylight into "
                + "ambient — applying a constant amount is what makes cheap AO read as "
                + "smudge");
            Check(LightModel.AoStrength(0, 0) > 0.15 && LightModel.AoStrength(1, 1) < 0.85,
                "but it is never off and never total",
                $"{LightModel.AoStrength(0, 0):0.00}..{LightModel.AoStrength(1, 1):0.00}");

            // ---- THE AMBIENT IS NOT THE SKY (M17.10 V1) ----
            //
            // One set of colour functions used to feed both the skybox dome
            // and the diffuse fill; the dome's honest daytime brightness as
            // fill is why the noon stills never showed a shadow. The Ambient*
            // accessors are the fill's OWN values: same hues, day scaled,
            // night bit-identical.
            double L3((double r, double g, double b) c) => c.r + c.g + c.b;
            Check(L3(LightModel.AmbientSky(0)) < L3(LightModel.SkyColour(0)),
                "the day FILL is dimmer than the dome it derives from — a sky can be "
                + "bright without every shaded wall being bright",
                $"fill {L3(LightModel.AmbientSky(0)):0.000} vs dome {L3(LightModel.SkyColour(0)):0.000}");
            Check(Math.Abs(L3(LightModel.AmbientSky(1)) - L3(LightModel.SkyColour(1))) < 1e-9
                && Math.Abs(L3(LightModel.AmbientGround(1)) - L3(LightModel.GroundColour(1))) < 1e-9,
                "night ambient is bit-identical to the night colours — night was tuned "
                + "AS ambient and this change must not touch the half that already reads right");
            Check(L3(LightModel.AmbientSky(0, 1)) > L3(LightModel.AmbientSky(0, 0)) * 1.2,
                "rain lifts the day fill back toward the dome, because a true overcast "
                + "really is one big soft source — that is the reference set's third frame",
                $"wet {L3(LightModel.AmbientSky(0, 1)):0.000} vs dry {L3(LightModel.AmbientSky(0, 0)):0.000}");
            Check(L3(LightModel.AmbientGround(0)) < L3(LightModel.AmbientHorizon(0)),
                "and the three bands keep their order through the scaling");

            // THE RANGE CHECK is what separates AO from a dark halo traced
            // round every silhouette — the single most recognisable tell of
            // screen-space occlusion done cheaply.
            Check(LightModel.AoRangeCheck(0.1, 0.55) == 1.0,
                "a sample within the radius counts fully");
            Check(LightModel.AoRangeCheck(4.0, 0.55) == 0,
                "a sample metres in front of the surface is a different object, and "
                + "counting it draws a dark halo round every silhouette");
            double r1 = LightModel.AoRangeCheck(0.7, 0.55), r2 = LightModel.AoRangeCheck(0.9, 0.55);
            Check(r1 > r2 && r1 < 1.0 && r2 > 0,
                "and it falls off between, or the halo is merely a hard edge instead of "
                + "a soft one",
                $"{r1:0.00} then {r2:0.00}");

            // DIRECTLY-LIT PIXELS GET RELIEF. A post pass cannot separate
            // ambient from direct, so multiplying the whole frame darkens a
            // sunlit wall as much as a shaded corner — which is why so much
            // screen-space AO looks like grime.
            Check(LightModel.AoDirectRelief(1.0) < LightModel.AoDirectRelief(0.0),
                "a bright pixel is probably directly lit, so occlusion backs off there "
                + "— an approximation, and stated as one");

            // NEVER TO BLACK.
            double darkest = 9;
            for (double raw = 0; raw <= 1.0001; raw += 0.05)
                for (double lum = 0; lum <= 1.0001; lum += 0.1)
                    darkest = Math.Min(darkest,
                        LightModel.AoMultiplier(raw, LightModel.AoStrength(1, 1), lum));
            Check(darkest >= 0.35 - 1e-9,
                "and no corner is ever unlit — an occlusion term that reaches zero "
                + "turns every interior angle into a hole",
                $"darkest {darkest:0.00}");
            Check(LightModel.AoMultiplier(0, 0.7, 0.2) == 1.0,
                "open ground is untouched, so the effect costs nothing where there is "
                + "nothing to occlude");
            Check(LightModel.AoMultiplier(1, 0.7, 0.2) < LightModel.AoMultiplier(0.3, 0.7, 0.2),
                "more enclosure is more darkening");
            Check(LightModel.AoRadiusMetres > 0.2 && LightModel.AoRadiusMetres < 1.2,
                "the radius is contact-scale, not room-scale — a large one produces a "
                + "soft grey wash that reads as dirt rather than as contact",
                $"{LightModel.AoRadiusMetres}m");

            // ---- REFLECTIONS ----
            Check(LightModel.ReflectionStrength(0.0, 1.0) == 0,
                "a dry street reflects nothing, and is not charged for the privilege");
            Check(LightModel.ReflectionStrength(1.0, 1.0) > LightModel.ReflectionStrength(1.0, 0.0),
                "a wet street at NIGHT reflects more than the same road at noon — the "
                + "reflection is there either way and at noon the sky is brighter than "
                + "anything in it",
                $"{LightModel.ReflectionStrength(1.0, 1.0):0.00} vs {LightModel.ReflectionStrength(1.0, 0.0):0.00}");
            Check(LightModel.ReflectionStrength(1.0, 1.0) > LightModel.ReflectionStrength(0.4, 1.0),
                "and wetter reflects more than damp");
            Check(LightModel.ReflectionStrength(5, 5) <= 1.0 && LightModel.ReflectionStrength(-3, -3) >= 0,
                "bounded at both ends however it is called");

            // WHERE THE GATE SITS, pinned with literals rather than with the
            // constant it guards — a test written against the constant moves
            // with it and cannot see it move. Both misses in the first break
            // run were dead-code breaks (the outer Clamp01 already zeroes
            // below the gate and clamps above), so the guard and the input
            // clamp could each be deleted with the suite still green. What
            // was actually untested was the THRESHOLD: raise it to 0.5 and a
            // rain-slicked street goes matte with every check still passing.
            Check(LightModel.ReflectionStrength(0.30, 1.0) > 0.05,
                "a merely damp street still catches the lights — the gate is for a road "
                + "with nothing on it, not for one it has just finished raining on",
                $"{LightModel.ReflectionStrength(0.30, 1.0):0.000}");
            Check(LightModel.ReflectionStrength(0.10, 1.0) == 0,
                "and a road that is barely misted is still dry as far as the probe is "
                + "concerned, because the alternative is paying for a reflection nobody "
                + "can see");

            // THE INSIGHT: staleness is DISTANCE, not time.
            Check(!LightModel.ShouldRefreshReflection(0, 0.5, 1.0),
                "a player standing still is looking at a reflection that is already "
                + "correct, and refreshing it on a timer pays every second for nothing");
            Check(LightModel.ShouldRefreshReflection(9, 0.1, 1.0),
                "but one who has run down the street is looking at one that is wrong");
            Check(LightModel.ShouldRefreshReflection(0, 9, 1.0),
                "and a floor in seconds catches the player spinning on the spot, who "
                + "covers no distance and changes the entire view");
            Check(!LightModel.ShouldRefreshReflection(99, 99, 0),
                "with nothing to reflect, nothing is resampled at all — which is the "
                + "whole point of gating it");

            // Frame-rate independence, same standard as everything else here.
            double a30 = 0, a240 = 0;
            for (int i = 0; i < 30; i++) a30 = LightModel.Wetness(a30, 1.0, 1.0 / 30.0);
            for (int i = 0; i < 240; i++) a240 = LightModel.Wetness(a240, 1.0, 1.0 / 240.0);
            Check(Math.Abs(a30 - a240) < 1e-3,
                "the street wets at the same rate at 30fps and 240",
                $"{a30:0.0000} vs {a240:0.0000}");
        }
    }
}
