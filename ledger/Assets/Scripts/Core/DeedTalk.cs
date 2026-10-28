using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace Ledger.Core
{
    /// THE DEED'S STORIES AND THE TALK'S EVIDENCE (28 October 2026, the 5 October sweep's G3). The stories the game
    /// files about a deed (he was seen near it, he says where he was, he owned up, somebody keeps it quiet) and the
    /// two pieces of every line to a character that tell the talk program what they hold of it ("deed" and
    /// "evidence.account", production/specs/talk-protocol.md) lived only in the port (ue-probe CrimeProbe.h, since
    /// 29 September and 1 October). The talk program (ledger/TalkHelper, C#) reads what they write and every talk
    /// reply comes back into the town's memory through them, yet nothing compared them with C# code: crime-probe-test
    /// and tools/talk-protocol-check.py pin them against the written protocol only. Their home is here now: the
    /// port's CrimeProbe.h follows this file line for line, and the DeedTalk golden rows drive each shape through its
    /// cases, so a field renamed, an escape dropped or a word changed on either side fails rows.
    ///
    /// BYTE FOR BYTE THE PORT'S TEXT, which sets three things here that are not this Core's usual habits. A number in
    /// the account is written as C's "%f" writes it (std::to_string: six decimals, ties to even); "F6" agreed with
    /// MSVC's on all 540,022 values measured on 28 October 2026, exact ties among them. A deed's ids are escaped for a
    /// quote and a backslash only, an account's words for those and a newline, a carriage return and a tab, as the
    /// port escapes them (an id with a newline would be bad JSON on both sides; the cast's ids have none). And the
    /// fields come in the port's order. A NaN or an infinity has no shared text (the port's differs by compiler), and
    /// none reaches here: the mill refuses a rumour at NaN (town list 6bw).
    ///
    /// The talk program only reads these (TalkHelper's Answer, with System.Text.Json); its self-test writes its own
    /// requests by hand, some on purpose in shapes the game never sends (an account without "topic", "heardHeSaid" as
    /// one string), so nothing there is built from these functions.
    public static class DeedTalk
    {
        static readonly CultureInfo Inv = CultureInfo.InvariantCulture;

        /// The window's deed as the session record keys it (the scripted encounter's, and free play's on day 1).
        public const string WindowDeedKey = "player.window_d1";
        /// The scripted encounter's own story of the window, the mill's (the review of 1 October, N1).
        public const string ScriptedStoryKey = "player.broke_a_window";
        /// The predicate a sighting near the window is filed under (CrimeProbe.h NearPredicate).
        public const string NearPredicate = "was_near_the_deed";

        /// "player.window_d1" is "window_d1"; a key without the prefix is itself.
        public static string DeedStem(string deedKey)
        {
            deedKey = deedKey ?? "";
            return deedKey.StartsWith("player.", StringComparison.Ordinal) ? deedKey.Substring(7) : deedKey;
        }

        /// A story of the deed itself: always its own key (the review's A3: free play files "player.window_dN"); for
        /// the window's day-1 key also the mill's "broke_a_window" and the sighting near it.
        public static bool IsDeedStory(Rumor r, string deedKey)
        {
            if (r == null || r.Content == null || r.Content.Subject != "player") return false;
            if (r.TopicKey == deedKey) return true;
            if (deedKey == WindowDeedKey) return r.Content.Predicate == "broke_a_window" || r.Content.Predicate == NearPredicate;
            return false;
        }

        /// "at_window_d1": he was seen at a place near the deed's time.
        public static string SightingPredicate(string deedKey) => "at_" + DeedStem(deedKey);
        /// "claim_window_d1": what he says about where he was.
        public static string ClaimPredicate(string deedKey) => "claim_" + DeedStem(deedKey);

        /// THE STORY THAT HE WAS SEEN AT A PLACE NEAR A DEED'S TIME (town list 6au): "the new owner was at the fish
        /// market on Tuesday night", its value the area id, not sensitive, carrying the witness's rung (Jafar's A5
        /// ruling: no sighting reads as "he did it" unless the witness knew him). Never learned into anybody's
        /// knowledge; the talk program judges it. Night is from six in the evening to six in the morning here, the
        /// words' own night, not Sighting.NightAt's.
        public static Rumor SightingStory(string deedKey, string area, string areaWords, int day, int hour,
                                          string witnessId, double confidence, int rung)
        {
            return new Rumor
            {
                Content = new Fact("player", SightingPredicate(deedKey), area),
                OriginId = witnessId,
                OriginRung = rung,
                Hops = 0,
                Confidence = confidence,
                Sensitive = false,
                Summary = "the new owner was at " + areaWords + " on " + new GameTime(day, hour, 0).WeekdayName
                          + ((hour >= 18 || hour < 6) ? " night" : ""),
            };
        }

        /// WHAT HE SAYS ABOUT WHERE HE WAS (town list 6am), once the talk program says his answer was definite: "the
        /// new owner says he was at the chapel", its value the reply's area ids comma-joined, heard from him by the
        /// one he told. Filed under the claim's own predicate, never the place's, so the town never learns where he
        /// was from what he says (the sweep's U1).
        public static Rumor ClaimStory(string deedKey, IReadOnlyList<string> areas, string areaWords, string toldTo)
        {
            return new Rumor
            {
                Content = new Fact("player", ClaimPredicate(deedKey), string.Join(",", areas ?? Array.Empty<string>())),
                OriginId = toldTo,
                Hops = 0,
                Confidence = 0.9,
                Sensitive = false,
                Summary = "the new owner says he was at " + areaWords,
            };
        }

        /// HE OWNED UP (town list 6al): the deed's story as told by him, certain. With a place (free play, the
        /// review's A3) the deed's own story, Fact("player", deed, place), sensitive, in the words said; without, the
        /// window's day-1 key files the mill's "broke_a_window" story, any other deed "owned_up".
        public static Rumor OwnedUpStory(string deedKey, string toldTo, string place = null, string said = null)
        {
            if (!string.IsNullOrEmpty(place))
            {
                return new Rumor
                {
                    Content = new Fact("player", DeedStem(deedKey), place),
                    OriginId = toldTo,
                    Hops = 0,
                    Confidence = 1.0,
                    Sensitive = true,
                    Summary = string.IsNullOrEmpty(said) ? "the new owner owned up to it himself" : said,
                };
            }
            bool window = deedKey == WindowDeedKey;
            return new Rumor
            {
                Content = window ? new Fact("player", "broke_a_window", "mickeys_window") : new Fact("player", DeedStem(deedKey), "owned_up"),
                OriginId = toldTo,
                Hops = 0,
                Confidence = 1.0,
                Sensitive = false,
                Summary = window ? "the new owner told me himself that he broke Mickey's window" : "the new owner owned up to it himself",
            };
        }

        /// A PERSON AGREES TO KEEP A DEED QUIET (town list 6al), the reply's keepsQuiet with agreed true: its stories,
        /// and the sighting of him near it, go into their Suppressed, which the mill honours; they still remember
        /// everything, so the talk program is still told the deed. Not GossipMill.Contain, which also cuts the story's
        /// confidence (the sweep's U5). A refusal files nothing.
        public static void KeepQuiet(Gossiper g, string deedKey)
        {
            if (g == null) return;
            var topics = new List<string> { deedKey };   // the deed's own story, always (the review's A3)
            if (deedKey == WindowDeedKey) { topics.Add(ScriptedStoryKey); topics.Add("player." + NearPredicate); }
            topics.Add("player." + SightingPredicate(deedKey));
            foreach (var t in topics) g.Suppressed.Add(t);
        }

        /// THE DEED AS THE TALK PROGRAM IS TOLD IT (town list 6ac, 6am, 6au), the line's ',"deed":{...}', for
        /// somebody who holds any of its stories or saw him near it: "topic", "day", "hour"; "sawHimAt", the place
        /// they saw him; "heardHimAt", the area the surest sighting of him they heard of puts him at (their own
        /// sighting goes as sawHimAt); "heardHeSaid", the areas of what he has told people, once that has reached
        /// them, which alone does not tell them the deed. Empty for somebody the deed has not reached.
        public static string DeedJson(Gossiper g, string deedKey, int day, int hour, string sawHimAt)
        {
            if (g == null) return "";
            bool holds = !string.IsNullOrEmpty(sawHimAt);
            string heardHimAt = "";
            double heardConf = -1.0;
            var heardHeSaid = new List<string>();
            string sighting = SightingPredicate(deedKey), claim = ClaimPredicate(deedKey);
            foreach (var r in g.Rumors)
            {
                if (r == null || r.Content == null || r.Content.Subject != "player") continue;
                if (IsDeedStory(r, deedKey)) { holds = true; continue; }
                if (r.Content.Predicate == sighting && r.Hops > 0 && r.Confidence > heardConf)
                {
                    holds = true;
                    heardConf = r.Confidence;
                    heardHimAt = r.Content.Value;
                }
                else if (r.Content.Predicate == claim)
                {
                    foreach (var a in r.Content.Value.Split(','))
                        if (a.Length > 0 && !heardHeSaid.Contains(a)) heardHeSaid.Add(a);
                }
            }
            if (!holds) return "";
            var sb = new StringBuilder(",\"deed\":{\"topic\":").Append(JsonId(deedKey))
                .Append(",\"day\":").Append(day.ToString(Inv)).Append(",\"hour\":").Append(hour.ToString(Inv));
            if (!string.IsNullOrEmpty(sawHimAt)) sb.Append(",\"sawHimAt\":").Append(JsonId(sawHimAt));
            if (heardHimAt.Length > 0) sb.Append(",\"heardHimAt\":").Append(JsonId(heardHimAt));
            if (heardHeSaid.Count > 0)
            {
                sb.Append(",\"heardHeSaid\":[");
                for (int i = 0; i < heardHeSaid.Count; i++) sb.Append(i > 0 ? "," : "").Append(JsonId(heardHeSaid[i]));
                sb.Append(']');
            }
            return sb.Append('}').ToString();
        }

        /// WHAT A RESIDENT HOLDS OF THE DEED, AS THE EVIDENCE SENT WITH EACH LINE (the independent review of
        /// 1 October, N1): their account of the deed's story as it was filed, Suspecting.AccountOf. In free play that
        /// is the deed's own key ("player.window_dN"); the scripted encounter files the mill's "player.broke_a_window".
        public static DeedAccount EvidenceAccount(Gossiper g, bool freePlay, string filedKey) =>
            Suspecting.AccountOf(g, freePlay ? filedKey : ScriptedStoryKey);

        /// THAT ACCOUNT AS THE TALK PROGRAM IS SENT IT, the inside of "evidence":{"account":{...}}, opening on
        /// "topic", the deed's key as the line's deed.topic gives it: the talk program uses an account only for the
        /// deed the line is about (the town's half of N1). Who told them (ToldBy) is not sent: the game's mill keeps
        /// no teller.
        public static string EvidenceAccountFields(DeedAccount a, string deedKey)
        {
            string j = "\"topic\":\"" + EvidenceEsc(deedKey) + "\",";
            if (!a.Held) return j + "\"held\":false";
            return j + "\"held\":true,\"seen\":" + (a.SawItMyself ? "true" : "false")
                + ",\"rung\":" + a.Rung.ToString(Inv)
                + ",\"names\":" + (a.NamesHim ? "true" : "false")
                + ",\"confidence\":" + Fixed6(a.Confidence)
                + (a.NamesHim ? ",\"namingConfidence\":" + Fixed6(a.NamingConfidence) : "")
                + ",\"summary\":\"" + EvidenceEsc(a.Summary) + "\"";
        }

        // std::to_string's "%f": six decimals (see the class's note).
        static string Fixed6(double v) => v.ToString("F6", Inv);

        // An id in the deed's JSON: a quote and a backslash escaped, nothing else (CrimeProbe.h JsonId).
        static string JsonId(string s)
        {
            var sb = new StringBuilder("\"");
            foreach (var c in s ?? "")
            {
                if (c == '"' || c == '\\') sb.Append('\\');
                sb.Append(c);
            }
            return sb.Append('"').ToString();
        }

        // An account's words: a quote, a backslash, a newline, a carriage return and a tab (CrimeProbe.h EvidenceEsc).
        static string EvidenceEsc(string s)
        {
            var sb = new StringBuilder();
            foreach (var c in s ?? "")
            {
                if (c == '\\' || c == '"') sb.Append('\\').Append(c);
                else if (c == '\n') sb.Append("\\n");
                else if (c == '\r') sb.Append("\\r");
                else if (c == '\t') sb.Append("\\t");
                else sb.Append(c);
            }
            return sb.ToString();
        }
    }
}
