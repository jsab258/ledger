using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// His answer to Sheila's question at the week's end.
    public enum WeekAnswer
    {
        /// Not answered yet (or never asked).
        None,
        /// Wind Mickey's business down: a cab firm and nothing more.
        WindDown,
        /// Take it over, Mickey's arrangements and all.
        TakeOver,
        /// He would not say: said so plainly, or the day she asked ended unanswered.
        WontSay,
    }

    /// THE WEEK'S END (town list 6ca; the first hour Jafar approved: "The week
    /// ends on day 7 ... Sheila, over the real book, 'So which is it going to
    /// be?'"; the outline: "Wind it down, take it over, or refuse to say; the
    /// street learns the answer"). From the week's seventh day (the game's
    /// first day plus six, as the outfit's asks count from it), the first time
    /// he talks with her she puts the question, over Mickey's real book if she
    /// trusts him (Trust.Earned, town list 6bz) and over the day-book if not.
    /// From a Monday start that day is a Sunday, her day off: she comes in to
    /// the office for it, at ten, and waits till twelve (Waits); if he does not
    /// come, she asks the next time he talks with her.
    ///
    /// His answer is two steps, as his no to Ron is (town list 6bn), since it
    /// is for good: a line that sounds like one answer, and only one (Sounds),
    /// gets her own plain question back (AskPlainly), and only his plain yes to
    /// that (Confirms), as his very next line to her, is the answer. A day she
    /// asked that ends unanswered is his refusal to say (Close). Whatever he
    /// answers is the street's story: she holds it first-hand, and so does
    /// anybody the cast has in the office then; her discretion decides how far
    /// it goes. What each answer does beyond that is Act II's.
    public sealed class WeeksEnd
    {
        /// Who asks (a cast id): Sheila.
        public const string Sheila = "lena";
        /// The week's seventh day comes six after the first.
        public const int After = 6;
        /// On a Sunday she waits at the office from ten till twelve.
        public const int WaitFrom = 10, WaitUntil = 12;
        /// Once she has asked on her Sunday, she stays till six for his answer.
        public const int StayUntil = 18;
        /// The game's first day (day 0, a Monday, as GameTime and the cast count).
        public int FirstDay { get; private set; }
        /// The day she first asks.
        public int Day => FirstDay + After;
        public WeeksEnd(int firstDay = 0) { FirstDay = Math.Max(0, firstDay); }
        /// Where she waits (a cast place).
        public const string Office = "mickeys_office";

        /// The question, as the first hour has it.
        public const string Question = "So which is it going to be?";

        /// What she says as she puts it, the game's own words, over the real
        /// book or the day-book; on her day off, she says so first.
        public static string Opening(bool realBook, bool dayOff = false) => (dayOff ? "I don't come in Sundays. " : "") + (realBook
            ? "That's Mickey's real book. Everything he ran, in his own hand. You've had your week. " + Question
            : "That's the day-book. The other one stays where it is. You've had your week. " + Question);

        /// When his line sounds like an answer, her plain question back.
        public static string AskPlainly(WeekAnswer a)
        {
            switch (a)
            {
                case WeekAnswer.WindDown: return "Wind it down, then? Mickey's arrangements finished, and this a cab firm and nothing more. Say yes and I'll close the book on it.";
                case WeekAnswer.TakeOver: return "Take it over, then? Mickey's arrangements and everything that comes with them, yours. Say yes and it's your book.";
                case WeekAnswer.WontSay: return "You won't say, then? Say yes and I'll take that as your answer.";
                default: return null;
            }
        }

        /// What she says to his plain yes.
        public static string Took(WeekAnswer a)
        {
            switch (a)
            {
                case WeekAnswer.WindDown: return "Right. I'll close the book on it.";
                case WeekAnswer.TakeOver: return "Right. Then it's your book.";
                case WeekAnswer.WontSay: return "Suit yourself. The street will decide for you, then.";
                default: return null;
            }
        }

        /// With live talk off, to any other line while the question stands: the
        /// question again, never a brush-off (the independent check: "Give me
        /// ten minutes" on her day off, and midnight took it as his refusal).
        public const string StillAsks = "You heard me. Wind it down, take it over, or won't you say?";

        /// What the street says of it: the story's summary.
        public static string Said(WeekAnswer a)
        {
            switch (a)
            {
                case WeekAnswer.WindDown: return "The new owner told Sheila he's winding Mickey's business down.";
                case WeekAnswer.TakeOver: return "The new owner told Sheila he's taking Mickey's business on, all of it.";
                case WeekAnswer.WontSay: return "Sheila asked the new owner what he means to do with Mickey's business, and he wouldn't say.";
                default: return null;
            }
        }

        /// What she remembers of it.
        public static string Remembered(WeekAnswer a)
        {
            switch (a)
            {
                case WeekAnswer.WindDown: return "I asked Mickey's nephew, the new owner, which it was going to be, and he told me plainly: he's winding Mickey's business down.";
                case WeekAnswer.TakeOver: return "I asked Mickey's nephew, the new owner, which it was going to be, and he told me plainly: he's taking Mickey's business on, all of it.";
                case WeekAnswer.WontSay: return "I asked Mickey's nephew, the new owner, which it was going to be, and he wouldn't say.";
                default: return null;
            }
        }

        /// The story's topic prefix: "player.week_d" + the day she asked.
        public const string TopicPrefix = "player.week_d";
        public static bool IsWeekAnswer(Rumor r) =>
            r != null && r.Content != null && r.Content.Subject == "player" && r.TopicKey != null && r.TopicKey.StartsWith(TopicPrefix, StringComparison.Ordinal);

        static string Value(WeekAnswer a) => a == WeekAnswer.WindDown ? "winddown" : a == WeekAnswer.TakeOver ? "takeover" : "wontsay";

        /// When she put the question, or null.
        public GameTime? AskedAt { get; private set; }
        /// Over the real book.
        public bool RealBook { get; private set; }
        public WeekAnswer Answer { get; private set; } = WeekAnswer.None;
        public GameTime? AnsweredAt { get; private set; }
        public bool Answered => Answer != WeekAnswer.None;

        /// Whether she is at the office for him on the seventh day when it is a
        /// Sunday, her day off: ten till twelve, and once she has asked, while
        /// her question stands, till six, "before the day's out" as she tells
        /// him (the independent checks: she went home the moment she asked, or
        /// half an hour after, and midnight took it as his refusal).
        public bool Waits(GameTime now)
        {
            if (now.Day != Day || CastDay.Weekday(Day) != 6 || now.Hour < WaitFrom) return false;
            // Answered, or asked another day: she has no reason to be there.
            if (Answered || AskedAt is GameTime asked && asked.Day != Day) return false;
            if (now.Hour < WaitUntil) return true;
            return AskedAt is GameTime && Stands(now) && now.Hour < StayUntil;
        }

        /// Whether she puts the question now, the first time he talks with her
        /// at the office from day 7 on: true once, the turn she asks. Only at
        /// the office, where the book is and whom the story names as there
        /// (the independent check: asked at the fish shop "over the book", the
        /// people at Mickey's heard it and those beside her did not).
        public bool Ask(GameTime now, bool realBook, bool atOffice = true)
        {
            if (AskedAt != null || now.Day < Day || !atOffice) return false;
            AskedAt = now;
            RealBook = realBook;
            return true;
        }

        /// Whether the question stands at `now`: asked, unanswered, the same day.
        public bool Stands(GameTime now) => AskedAt is GameTime at && !Answered && now.Day == at.Day && now.CompareTo(at) >= 0;

        /// His plain answer, given while the question stands; filed as the
        /// street's story and her memory. False when it cannot be.
        public bool Give(WeekAnswer a, GameTime now, GossipMill mill, CastDay cast)
        {
            if (a == WeekAnswer.None || !Stands(now)) return false;
            bool atOffice = Waits(now);
            Answer = a;
            AnsweredAt = now;
            File(mill, cast, now, atOffice);
            return true;
        }

        /// The day she asked ended unanswered: his refusal to say, from midnight.
        /// True when it closes now.
        public bool Close(GameTime now, GossipMill mill, CastDay cast)
        {
            if (!(AskedAt is GameTime at) || Answered || now.Day <= at.Day) return false;
            Answer = WeekAnswer.WontSay;
            AnsweredAt = new GameTime(at.Day + 1, 0, 0);
            File(mill, cast, AnsweredAt.Value, false);
            return true;
        }

        // Filed once: her memory and the story, first-hand for her and for
        // anybody the cast has in the office's area then (never at midnight,
        // when she is not there to be overheard: only she knows).
        void File(GossipMill mill, CastDay cast, GameTime at, bool atOffice)
        {
            if (mill == null) return;
            var fact = new Fact("player", "week_d" + AskedAt.Value.Day, Value(Answer));
            if (mill.Get(Sheila) is Gossiper she)
                she.Memory?.Append(new MemoryEvent(at, "conversation", 0.9, Remembered(Answer)));
            mill.Witness(Sheila, fact, Said(Answer), false, at, 1.0);
            if (cast == null || at.Hour == 0 && at.Minute == 0) return;
            // Where she is when he answers: her routine's place, or the office
            // on her Sunday off (the independent check: an answer on Rita's step
            // was heard by the people at Mickey's).
            // Off, anywhere else (after her hours), nobody else overhears it.
            string area = atOffice ? cast.AreaOf(Office) : cast.AreaOf(cast.PlaceOf(Sheila, at.Day, at.Hour));
            if (area == null) return;
            foreach (var p in cast.People)
                if (p != Sheila && cast.AreaOf(cast.PlaceOf(p, at.Day, at.Hour)) == area)
                    mill.Witness(p, fact, Said(Answer), false, at, 1.0);
        }

        /// Her line for the talk while the question stands (a per-turn line,
        /// as Ron's Tonight is): she never answers it for him.
        public static string StandingLine(bool realBook) =>
            "Today you put it to him, over " + (realBook ? "Mickey's real book" : "the day-book, the real one kept back") +
            ", as you promised Mickey you would: which is it going to be? Wind Mickey's business down, take it over, or will he not say? " +
            "Never answer it for him and never take a half answer for one; never say you will close the book or that it is his. " +
            "If he dodges it, tell him you'll have his answer before the day's out.";

        // HOW HIS ANSWER IS READ, as his no to Ron is (Arrangement): the whole
        // clause must be the answer, every other clause only the words round
        // one; a question, a supposition, a joke or somebody else's words is none.
        static string Words(string s) =>
            " " + Regex.Replace(Apostrophes(s).ToLowerInvariant().Replace("'", ""), @"[^a-z]+", " ").Trim() + " ";

        static string Apostrophes(string s) => (s ?? "").Replace('’', '\'').Replace('‘', '\'').Replace('`', '\'').Replace('´', '\'');

        static List<string> Sentences(string said)
        {
            var list = new List<string>();
            foreach (var raw in Regex.Split(Apostrophes(said), @"(?<=[.!?])\s+"))
            {
                var t = Regex.Replace(raw.Trim(), @",\s*(alright|all right|ok|okay|right|yeah|eh|see|got it|understand|understood)\s*\?+$", ".", RegexOptions.IgnoreCase);
                if (t.Length > 0) list.Add(t);
            }
            return list;
        }

        static IEnumerable<string> Clauses(string sentence) =>
            sentence.TrimEnd('.', '!', '?').Split(new[] { ',', ';', ':', '—', '–' }, StringSplitOptions.RemoveEmptyEntries);

        const string Lead = @"(look |listen |right |well |so |honestly |sheila |ok |okay |alright |all right |i think |i reckon |i suppose |then |yes |yeah |no |nah |im |i am |im going to |i am going to |ill |i will |im gonna |were going to |we are going to |were |lets |let us |i said |like i said |i told you )*";
        const string It = @"(it|the business|mickeys business|the lot|all of it|everything|this|that|the office|the firm|mickeys|mickeys arrangements|the arrangements|his arrangements)";
        const string Tail = @"( (then|sheila|love|now|for good|and thats final|and thats that|honestly|mind|i think|i reckon))* $";

        static readonly Regex WindDownClause = new Regex(@"^ " + Lead + "(" +
            @"wind(ing)? " + It + " (down|up)|wind(ing)? down " + It + "|wind(ing)? down|(shut|shutting|close|closing) " + It + " (down|up)|(shut|shutting|close|closing) down " + It +
            @"|(get|getting) out( of (it|mickeys business|the business|the lot|all of it))?|(im|i am) out|(go|going) straight|(sell|selling) up|(packing|pack) (it|the lot|mickeys business|the business) in for good|(finish|finishing|end|ending) (it|mickeys business|the business|mickeys arrangements|the arrangements)" +
            @"|just cabs|(its|it is|itll be|it will be|it stays|keep it|keeping it) (a cab firm|a cab office|a minicab firm|a minicab office|just a cab firm|just the cabs|just cabs|cabs and nothing else|cabs and nothing more|a cab firm and nothing (else|more))|just the cabs|no more (arrangements|of mickeys arrangements|of that|of it|envelopes)" +
            ")" + Tail);
        static readonly Regex TakeOverClause = new Regex(@"^ " + Lead + "(" +
            @"(take|taking) " + It + " over|(take|taking) over " + It + "|(take|taking) over|(take|taking) " + It + " on|(keep|keeping) " + It + " (going|running)|(carry|carrying) on (where mickey left off|as mickey did|like mickey|with it|with mickeys business|with the business)|(carry|carrying) " + It + " on" +
            @"|(run|running) " + It + "( myself| now| like mickey did| as mickey did)?|(im|i am) (in|taking it|taking the lot|having it|having the lot)|(its|it is) mine( now)?|i want (it|the lot|all of it|everything)|(pick|picking) up where mickey left off|same as mickey|(keep|keeping) mickeys arrangements" +
            @"|(ill|i will) keep (it|the business|mickeys business|the lot|all of it)( going)?|(im|i am) keeping (it|the business|mickeys business|the lot|all of it)|count me in|(take|taking) it all over|(ill|i will) carry on( with it)?" +
            ")" + Tail);
        static readonly Regex WontSayClause = new Regex(@"^ " + Lead + "(" +
            @"(im|i am) not (saying|telling|telling you)|i (wont|will not|shant) (say|tell you|be telling you)|not telling( you)?|not saying|none of your (business|concern)|mind your own( business)?|(thats|that is) my (business|affair|lookout)" +
            @"|no comment|thats for me to know( and you to find out)?|(im|i am) keeping (that|it) to myself|i (wont|will not|shant) be saying|(im|i am) saying nothing|i (wont|will not|shant) answer (that|you)" +
            @"|(its|thats|that is|it is) none of your (business|concern)|never you mind|(im|i am) not going to (tell you|say)|wont say|not going to say|(id|i would|i had|id much) rather not say|(ill|i will) not say|(thats|that is|its|it is) not for you to know" +
            ")" + Tail);
        // The words round an answer, which say nothing of their own.
        static readonly Regex AroundClause = new Regex(
            @"^ ((look|listen|right|well|so|honestly|sheila|love|then|ok|okay|alright|all right|yes|yeah|aye|sorry|thats final|and thats final|thats that|and thats that|end of|my minds made up|thats my answer|there you are|there it is|thats it|youve had my answer|youve got my answer|for good|now|mind)( |$))+$");
        // Anywhere in the line, it is no plain answer: taken back, put off,
        // supposed, joking, or somebody else's words.
        static readonly Regex TakenBack = new Regex(
            @" (only joking|just joking|joking|kidding|only messing|messing|having you on|winding you up|pulling your leg|yeah right|as if|not really|ha|haha|not likely|no chance|no way|not a chance|over my dead body|in your dreams|dream on|you must be joking|youre joking|pull the other one|ill let you know|i will let you know|ask me later|ask me another time|well see|wait and see|youll see|havent decided|not decided|dont know yet|i dont think|am i heck|joke|let me think|give me time|take that back|scratch that|fat chance|not a hope|taking the mickey|time will tell|depends|not on your nelly|do me a favour|leave it out|aye right|if you like|suppose so|i suppose|might as well|on second thoughts?|second thoughts|changed my mind|actually|wait(?! and see)|hang on|hold on|think about it|maybe|perhaps|probably|possibly|might|could|would|not sure|or not|or should i|should i|shall i|unless|if|what if|suppose|supposing|not yet|for now|for a bit|for a while|either|neither|or) " +
            @"| (?!i )[a-z]+ (said|says|reckons|told me|tells me|wants|wanted) ");

        // A sentence that is only a no: after an answer it takes it back ("Take
        // it over. No.", "Take it over. Not.").
        static readonly Regex NoSentence = new Regex(@"^ ((not|no|nah|nope|never|hardly|no way|no chance|not likely|not a chance|not really)( |$))+$");
        // A clause that starts with a yes and says the answer ("Yes take it over").
        // A no anywhere in his yes ("Yes, well no.") makes it none.
        static readonly Regex AnyNo = new Regex(@" (no(?! more )|nah|nope|not really|no way|no chance) ");
        static readonly Regex LeadingYes = new Regex(@"^ (yes|yeah|yep|yup|aye|sure|right|definitely|absolutely|certainly|of course) ");

        static readonly Regex[] Shapes = { WindDownClause, TakeOverClause, WontSayClause };
        static readonly WeekAnswer[] Kinds = { WeekAnswer.WindDown, WeekAnswer.TakeOver, WeekAnswer.WontSay };

        /// WHETHER A LINE OF HIS SOUNDS LIKE AN ANSWER, and which: a clause that
        /// is one of the three, in no question, with nothing else in its
        /// sentence but the words round an answer, nothing in the line taken
        /// back, supposed, joked or refused ("No chance.", "Ha!"), and no
        /// clause of another answer. A put-off ("I'll let you know") is none.
        /// Never the answer itself, only whether she asks him plainly.
        public static WeekAnswer Sounds(string said)
        {
            var sentences = Sentences(said);
            foreach (var s in sentences)
                if (TakenBack.IsMatch(Words(s))) return WeekAnswer.None;
            var found = WeekAnswer.None;
            foreach (var s in sentences)
            {
                // A no before an answer is how people answer ("No. Take it
                // over."); after one it takes it back ("Take it over. No.").
                if (NoSentence.IsMatch(Words(s))) { if (found != WeekAnswer.None) return WeekAnswer.None; continue; }
                if (s.Contains("?")) continue;
                var kinds = new List<WeekAnswer>();
                bool other = false;
                foreach (var clause in Clauses(s))
                {
                    var w = Words(clause);
                    if (w.Trim().Length == 0) continue;
                    if (NoSentence.IsMatch(w))
                    {
                        // "No, I'm taking it over." but never "Take it over, no."
                        if (kinds.Count > 0) return WeekAnswer.None;
                        continue;
                    }
                    int hit = -1;
                    for (int i = 0; i < Shapes.Length; i++)
                    {
                        if (!Shapes[i].IsMatch(w)) continue;
                        if (hit >= 0 && Kinds[hit] != Kinds[i]) return WeekAnswer.None;
                        hit = i;
                    }
                    if (hit >= 0) kinds.Add(Kinds[hit]);
                    else if (!AroundClause.IsMatch(w)) other = true;
                }
                if (kinds.Count == 0) continue;
                // An answer beside words that are not only round it ("Carry on,
                // Sheila, I'm listening.", "Wind it down, over my dead body.").
                if (other) return WeekAnswer.None;
                foreach (var k in kinds)
                {
                    if (found != WeekAnswer.None && found != k) return WeekAnswer.None;
                    found = k;
                }
            }
            return found;
        }

        static readonly Regex YesSentence = new Regex(
            @"^ ((yes|yeah|yep|yup|aye|sure|definitely|certainly|absolutely|of course|course|correct|exactly|thats right|that is right|thats it|thats what i said|thats my answer|you heard me|you heard|i do|i am|im sure|i am sure|im certain|i mean it|i did|it is|go ahead|go on then|sheila|love|then|please|honestly|ok|okay|for good|thats final|and thats final|fine|indeed|mate|mrs dunn)( |$))+$");
        static readonly Regex YesWord = new Regex(
            @" (yes|yeah|yep|yup|aye|sure|definitely|certainly|absolutely|of course|correct|exactly|thats right|that is right|thats it|thats what i said|thats my answer|you heard me|im sure|i am sure|im certain|i mean it|i do|ok|okay|go on then) ");
        // A brush-off: a yes said twice ("OK, OK.", "Sure, Sheila, sure."), or
        // one that means no ("Aye, right.") (the independent checks).
        static readonly Regex NotAYes = new Regex(@" (yeah|yes|yep|yup|aye|sure|ok|okay|of course|right|alright|fine)( (sheila|love|then|now))? \1 | aye right | yeah right | whatever | fine fine ");

        /// HIS PLAIN YES TO HER OWN QUESTION (AskPlainly for `asked`), as his very
        /// next line to her: a yes, alone or with the same answer said again in
        /// the same sentence or the next ("Yes, take it over.", "Yeah, I'm
        /// taking it over.", "Yes. That's final."), and nothing else but the
        /// words round it; never a question, another answer, a no, or anything
        /// taken back.
        public static bool Confirms(string said, WeekAnswer asked)
        {
            if (asked == WeekAnswer.None) return false;
            var sentences = Sentences(said);
            // A brush-off ("Yeah, yeah.") however it is punctuated (the
            // independent check).
            if (sentences.Count == 0 || NotAYes.IsMatch(Words(said)) || AnyNo.IsMatch(Words(said))) return false;
            foreach (var s in sentences)
            {
                var w = Words(s);
                if (TakenBack.IsMatch(w) || NoSentence.IsMatch(w)) return false;
            }
            var shape = Shapes[Array.IndexOf(Kinds, asked)];
            bool yes = false;
            foreach (var s in sentences)
            {
                if (s.Contains("?")) return false;
                if (IsYes(Words(s))) { yes = true; continue; }
                foreach (var clause in Clauses(s))
                {
                    var cw = Words(clause);
                    if (cw.Trim().Length == 0) continue;
                    if (NoSentence.IsMatch(cw)) return false;
                    if (IsYes(cw)) { yes = true; continue; }
                    if (shape.IsMatch(cw)) { if (LeadingYes.IsMatch(cw)) yes = true; continue; }
                    if (!AroundClause.IsMatch(cw)) return false;
                }
            }
            return yes;
        }

        static bool IsYes(string w) => YesSentence.IsMatch(w) && YesWord.IsMatch(w) && !NotAYes.IsMatch(w);

        /// For the save: when she asked (minutes), over which book, the answer
        /// and when; replayed through the rules on load.
        public Dictionary<string, object> ToJson()
        {
            var d = new Dictionary<string, object> { { "first", (double)FirstDay } };
            if (AskedAt is GameTime at) { d["asked"] = (double)at.TotalMinutes; d["realBook"] = RealBook; }
            if (Answered && AnsweredAt is GameTime t) { d["answer"] = Answer.ToString(); d["answered"] = (double)t.TotalMinutes; }
            return d;
        }

        /// From ToJson's values, through Ask and Give (no mill: the story is in
        /// the town's own save); a fresh one for anything it cannot read.
        public static WeeksEnd FromJson(Dictionary<string, object> saved)
        {
            if (saved == null) return new WeeksEnd();
            int first = saved.TryGetValue("first", out var f) && f is double fd && fd >= 0 && fd <= 100000 && fd == Math.Floor(fd) ? (int)fd : 0;
            var w = new WeeksEnd(first);
            if (!(saved.TryGetValue("asked", out var a) && a is double am && am >= 0 && am <= 1e8 && am == Math.Floor(am))) return w;
            bool real = saved.TryGetValue("realBook", out var rb) && rb is bool b && b;
            if (!w.Ask(GameTime.FromTotalMinutes((long)am), real)) return new WeeksEnd(first);
            if (!(MiniJson.GetString(saved, "answer") is string an) || Array.IndexOf(Enum.GetNames(typeof(WeekAnswer)), an) < 0) return w;
            var ans = (WeekAnswer)Enum.Parse(typeof(WeekAnswer), an);
            if (!(saved.TryGetValue("answered", out var t) && t is double tm && tm >= 0 && tm <= 1e8 && tm == Math.Floor(tm))) return w;
            var when = GameTime.FromTotalMinutes((long)tm);
            if (ans == WeekAnswer.WontSay && when.Day > w.AskedAt.Value.Day && when.Hour == 0 && when.Minute == 0) w.Close(when, null, null);
            else w.Give(ans, when, null, null);
            return w;
        }
    }
}
