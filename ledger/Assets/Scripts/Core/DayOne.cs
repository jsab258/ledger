using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// DAY ONE'S WORDS (town list 6cg; the first hour's minutes 0 to 7, which
    /// Jafar approved: Sheila meets him, shows him round, stops at the one door
    /// she does not open, and sends him out; the outline's Arrival: "the first
    /// thing the town does is talk"). Nothing of it was written, so the builder
    /// had nothing to stage and the street said nothing about him until night
    /// one's story came back at minute 13.
    ///
    /// Her walk-round is fixed lines in her own voice, from canon and the
    /// street's plain facts as recommended on his 29 September page (the door
    /// is Mickey's own office, locked since he died, and she keeps the key; he
    /// sleeps in the flat over the office; one driver by day, one by night;
    /// takings thin since the docks went), carried until he rules. Played or
    /// skipped, it ends the same way (WalkRoundEnds): she has met him, and the
    /// hint to talk has its moment. She calls him "new management", as her
    /// card and his ruling on her naming him have it.
    ///
    /// His arrival is the street's first story of him: first-hand for whoever
    /// is about Mickey's when he comes, and for Ada, who watches from her
    /// window (the outline; her step in the cast), passed on by the town's
    /// rounds, said to his face once in a bank of its own
    /// (StreetVoice.ArrivalLine), never by Sheila or his family. It is
    /// nobody's secret, never enters anybody's manner or how they stand to
    /// him, is never voiced in an overheard exchange, and gives way to any
    /// other story of him.
    public static class DayOne
    {
        public const string Sheila = "lena";
        public const string Ada = "ada";
        /// His family on the street, who never greet him as a stranger: June,
        /// Mickey's daughter.
        public static readonly HashSet<string> Family = new HashSet<string> { "june" };

        /// Sheila's walk-round, stop by stop, in order; her last line is the
        /// talk hint's own (FirstMoments, Moment.CanTalk).
        public static readonly (string stop, string line)[] WalkRound =
        {
            ("door", "New management. Sheila Dunn, I keep the books. Come on, I'll show you round before you start looking lost."),
            ("office", "Phone, radio, and the fare book. Every fare goes in the book. That was Mickey's rule, and it's mine now."),
            ("drivers", "One driver by day, one by night, and the radio in between. The takings have been thin since the docks laid men off."),
            ("mickeys-door", "That's Mickey's office. It's been locked since he died, and I've the key. Not today."),
            ("flat", "Your flat's upstairs, over the office. His things are still in it. I didn't have the heart."),
        };

        /// The walk-round is over, played or skipped: the same state either way
        /// (A32.12): Sheila has met him (the game counts her met), and the
        /// moment to talk has come; its hint (her last line) shows when the
        /// hints are next asked (FirstMoments.Due), never over another.
        public static Hint WalkRoundEnds(FirstMoments hints, double at) => hints?.Happened(Moment.CanTalk, at);

        /// His arrival's story: its topic, and how it is told.
        public const string ArrivalTopic = "player.arrived";
        public const string ArrivalSaid = "Mickey's nephew has come to take on the office";
        public static bool IsArrival(Rumor r) =>
            r != null && r.Content != null && r.Content.Subject == "player" && r.TopicKey == ArrivalTopic;

        /// HE ARRIVES at `at`: whoever the cast has about Mickey's then, and Ada
        /// if she is on her step, hold it first-hand, once. Returns who.
        public static List<string> Arrived(GossipMill mill, CastDay cast, GameTime at, int firstDay = 0)
        {
            var saw = new List<string>();
            // Only on the game's first day, and once (the second review: a call
            // before anybody was about, or long after it had faded, filed it again).
            if (mill == null || cast == null || at.Day != firstDay) return saw;
            foreach (var a in mill.Agents) if (a.Rumors.Exists(IsArrival)) return saw;

            string mickeys = cast.AreaOf("mickeys_office");
            var fact = new Fact("player", "arrived", "mickeys");
            foreach (var p in cast.People)
            {
                string area = cast.AreaOf(cast.PlaceOf(p, at.Day, at.Hour));
                if (area == null || !(area == mickeys || (p == Ada && area == cast.AreaOf("adas_step")))) continue;
                var g = mill.Get(p);
                if (g == null || g.Rumors.Exists(r => IsArrival(r) && r.Hops == 0)) continue;
                mill.Witness(p, fact, ArrivalSaid, false, at, 1.0);
                saw.Add(p);
            }
            return saw;
        }
    }
}
