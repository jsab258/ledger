using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// How a spell in custody ends.
    public enum CustodyEnd
    {
        /// He owned up to a window: cautioned and let go, nothing to answer.
        Cautioned,
        /// Charged and bailed to the magistrates' next sitting.
        Charged,
        /// Let go without charge, on bail to come back to the station.
        BailedToReturn,
    }

    /// WHAT AN ARREST DOES (town list 6bp; the checklist's A15.16 to A15.18 and
    /// A25.12; ROADMAP stage 3's arrest reachable from live play). From the
    /// research (production/research/police-response-1990/CUSTODY-2026-09-29.md):
    /// in 1990 an arrest cost hours, not the game. Held at the station on a
    /// named statement, the custody officer keeps whatever may be evidence (the
    /// coat he wore to the deed, while there is a case), and he is out again
    /// after about as long as the Home Office's study of the late 1980s found
    /// for his offence: a window six hours charged, two cautioned if he owns up;
    /// a wounding eight and a robbery twelve, charged either way on the named
    /// statement (silence blocks a caution, not a charge). Then a caution, or a
    /// charge and bail to the magistrates' next weekday sitting (inferred: the
    /// research gives the first sitting for a man kept in, not the date a bailed
    /// man is given). A killing is the game's choice, not the record's: held the
    /// twenty-two hours the most serious averaged, then bailed to come back in
    /// four weeks while they make their enquiries, where in 1990 he would more
    /// likely have been kept; never a game end, and put to Jafar. The street that
    /// sees him put in the car passes it on (SeenTaken); what the ask night makes
    /// of time in the cells is Arrangement's own rules (Ron cannot reach him, or
    /// he stays away).
    public sealed class Custody
    {
        public string Topic { get; private set; }
        public Offence Offence { get; private set; }
        public GameTime TakenAt { get; private set; }
        public GameTime OutAt { get; private set; }
        public CustodyEnd End { get; private set; }
        /// The coat he wore to the deed, kept as evidence.
        public bool CoatKept { get; private set; }
        /// The day he answers bail: the magistrates' sitting when charged, the
        /// station twenty-eight days on when bailed to return (inferred); -1
        /// when cautioned.
        public int AnswerDay { get; private set; }

        /// Every story of the street seeing him taken is under this topic and the day.
        public const string TakenPrefix = "player.taken_d";
        /// How those who saw it tell it: no secret, a thing done in the street.
        public const string TakenSaid = "the police took Mickey's nephew away in a car";

        Custody() { }

        /// HE IS TAKEN IN on a deed the police can arrest for (PoliceFile.CanArrest),
        /// at `at`; `ownsUp` if he admits it at the station, `inTheCoat` if he wore
        /// the coat to it. Null, and nothing done, for an offence no arrest is for.
        public static Custody Take(string topic, Offence o, GameTime at, bool ownsUp, bool inTheCoat)
        {
            if (string.IsNullOrEmpty(topic) || !PoliceFile.Arrestable(o)) return null;
            double hours;
            CustodyEnd end;
            switch (o)
            {
                // Criminal damage: cautioned 2.0 hours, charged 5.9 (HORS 104).
                case Offence.Damage: end = ownsUp ? CustodyEnd.Cautioned : CustodyEnd.Charged; hours = ownsUp ? 2 : 6; break;
                // Violence charged: 8.2 hours.
                case Offence.Wounding: end = CustodyEnd.Charged; hours = 8; break;
                // Robbery charged: 12.3 hours.
                case Offence.Robbery: end = CustodyEnd.Charged; hours = 12; break;
                // A killing: about 22 hours, the most serious offences' mean
                // (HORS 185), then bail to come back (the game's choice, not the
                // record's: never a game end).
                default: end = CustodyEnd.BailedToReturn; hours = 22; break;
            }
            var outAt = at.AddMinutes((int)Math.Round(hours * 60));
            return new Custody
            {
                Topic = topic, Offence = o, TakenAt = at, OutAt = outAt, End = end, CoatKept = inTheCoat && end != CustodyEnd.Cautioned,
                AnswerDay = end == CustodyEnd.Cautioned ? -1 : end == CustodyEnd.Charged ? NextSitting(outAt.Day) : outAt.Day + 28,
            };
        }

        /// The magistrates' first sitting after the day he is let go: the next
        /// weekday (day 0 a Monday), so a Friday's charge waits for Monday.
        public static int NextSitting(int day)
        {
            int d = day + 1;
            while (CastDay.Weekday(d) >= 5) d++;
            return d;
        }

        /// THE CAUTION IN FORCE IN 1990 (town list 6bu; PACE Code C, 1986, para
        /// 10.4, unchanged in the 1991 edition): given on arrest and on charge,
        /// from the Code's own text (production/research/police-response-1990/
        /// WORDS-2026-09-29.md).
        public const string Caution = "You do not have to say anything unless you wish to do so, but what you say may be given in evidence.";

        /// What the custody sergeant tells him on arrival: the gist of the
        /// written notice of his three rights and that he need not use them now
        /// (Code C, 1986); a London force's notice of the time was found, not
        /// Humberside's, so these are plain words, not a form's.
        public const string Rights = "You can have someone told you're here. You can see a solicitor, and the duty solicitor is free. You can read the codes of practice. You don't have to do any of that now.";

        static readonly string[] Weekdays = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" };

        /// The offence as the police name it to him.
        static string OffenceWords(Offence o) =>
            o == Offence.Damage ? "criminal damage" : o == Offence.Wounding ? "wounding" : o == Offence.Robbery ? "robbery"
            : o == Offence.Killing ? "murder" : o == Offence.Assault ? "assault" : "being suspicious";

        /// WHAT HE IS TOLD TAKING HIM IN: the arrest and the caution.
        public string ArrestWords() => "I'm arresting you on suspicion of " + OffenceWords(Offence) + ". " + Caution;

        /// WHAT HE IS TOLD LETTING HIM GO, plainly (town list 6bu; the checklist's
        /// A15.17, the consequences made clear, and A46.01, plain words): how it
        /// ended, the day he answers and what not turning up means (the Bail Act
        /// 1976), and the coat if they kept it. Ten o'clock is the game's hour
        /// (inferred); a charge's notice begins with the Code's own words.
        public string ReleaseWords()
        {
            string coat = CoatKept ? " We're keeping the coat you had on, as evidence." : "";
            string day = AnswerDay >= 0 ? Weekdays[CastDay.Weekday(AnswerDay)] : null;
            switch (End)
            {
                case CustodyEnd.Cautioned:
                    return "You've been cautioned for the " + OffenceWords(Offence) + ": you admitted it, so there's no charge, but the caution stays on your record and can be mentioned in court if you're ever back. You're free to go.";
                case CustodyEnd.Charged:
                    return "You are charged with the offence(s) shown below. " + Caution + " The offence: " + OffenceWords(Offence) + ". You're bailed to appear at the magistrates' court on " + day +
                           " at ten o'clock. Not turning up is an offence in itself." + coat;
                default:
                    return "You're released on bail without charge, while enquiries continue. You're to come back to this station in four weeks, on a " + day +
                           ", at ten o'clock. Not turning up is an offence in itself." + coat;
            }
        }

        /// Whether he is in the cells at `now`.
        public bool Holds(GameTime now) => now.TotalMinutes >= TakenAt.TotalMinutes && now.TotalMinutes < OutAt.TotalMinutes;

        /// Whether a story is the street's word that the police took him.
        public static bool IsTaken(Rumor r) =>
            r != null && r.TopicKey != null && r.TopicKey.StartsWith(TakenPrefix, StringComparison.Ordinal);

        /// THE STREET SEES HIM TAKEN: everybody of the cast in the area where he
        /// was taken, at that hour, saw the police put him in the car, and has it
        /// to pass on. Once a person a day. Returns who saw it.
        public static List<string> SeenTaken(GossipMill mill, CastDay cast, string area, GameTime at)
        {
            var saw = new List<string>();
            if (mill == null || cast == null || string.IsNullOrEmpty(area)) return saw;
            var fact = new Fact("player", "taken_d" + at.Day, "police");
            string topic = TakenPrefix + at.Day;
            foreach (var p in cast.People)
            {
                if (cast.AreaOf(cast.PlaceOf(p, at.Day, at.Hour)) != area) continue;
                var g = mill.Get(p);
                if (g == null || g.Rumors.Exists(r => r.TopicKey == topic && r.Hops == 0)) continue;
                mill.Witness(p, fact, TakenSaid, false, at, 1.0);
                saw.Add(p);
            }
            return saw;
        }

        /// For the save: the deed's topic, the offence, when taken and let go
        /// (minutes), how it ended, the coat and the day he answers.
        public Dictionary<string, object> ToJson() => new Dictionary<string, object>
        {
            { "topic", Topic }, { "offence", Offence.ToString() }, { "taken", (double)TakenAt.TotalMinutes },
            { "ownsUp", End == CustodyEnd.Cautioned },
            { "coat", CoatKept },
        };

        /// From ToJson's values, taken again through Take; null for anything it
        /// cannot read. Whether he could have been taken for it at all is the
        /// police file's (TownSave keeps an arrest only for a deed it took him for).
        public static Custody FromJson(Dictionary<string, object> saved)
        {
            if (saved == null) return null;
            if (!(MiniJson.GetString(saved, "topic") is string topic) || topic.Length == 0) return null;
            if (!(MiniJson.GetString(saved, "offence") is string os) || Array.IndexOf(Enum.GetNames(typeof(Offence)), os) < 0) return null;
            var o = (Offence)Enum.Parse(typeof(Offence), os);
            if (!saved.TryGetValue("taken", out var t) || !(t is double tm) || tm < 0 || tm > 1e8 || tm != Math.Floor(tm)) return null;
            bool ownsUp = saved.TryGetValue("ownsUp", out var ou) && ou is bool b && b;
            bool coat = saved.TryGetValue("coat", out var co) && co is bool c && c;
            return Take(topic, o, GameTime.FromTotalMinutes((long)tm), ownsUp, coat);
        }
    }
}
