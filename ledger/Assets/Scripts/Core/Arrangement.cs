using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// What he did with one night's ask.
    public enum NightAnswer
    {
        /// He handed the envelope over at the landing.
        Did,
        /// He told Ron no: the arrangement ends at once.
        Refused,
        /// He had the ask, said nothing and did not go.
        NoShow,
        /// Ron never reached him that night: the ask passed without his knowing,
        /// and nothing follows (town list 6bn).
        Undelivered,
    }

    /// MICKEY'S ARRANGEMENT WITH THE OUTFIT, IN THE NEW GAME (town list 6z; the
    /// checklist's A33.01; the first hour Jafar approved on 28 September, whose
    /// second ask falls on day 3, the evening of Ada's tea). The outfit asks
    /// every other night from the first, through Ron: an envelope to the ferry
    /// landing (game-design/first-ask-2026-09-29.md). He can do it, refuse, or
    /// not turn up. Refusing ends the arrangement at once; a night he does not
    /// turn up costs the outfit's patience, and three such nights end it; a
    /// night done wins a little back. NEVER A GAME OVER: the old week's rule
    /// (Campaign.JobMissed, "the outfit stopped calling. Then they sent
    /// someone.") ended the game on the third missed night; the new game's
    /// story uses an ended arrangement, it does not stop on one.
    ///
    /// Whatever he does is a story, the outfit's talk as the first hour has it,
    /// told first by the outfit's man at the landing, who knows it first-hand:
    /// he took the envelope, or waited for nobody, or heard the no from Ron,
    /// who carries Tom's answer down (each summary says what he himself saw).
    /// Ron, who keeps things quiet for the owner, tells nobody. Only the
    /// envelope handed over is a night-life secret (sensitive); a refusal or a
    /// night he stayed away is not. Nights are answered in order, one at a
    /// time; a night that passed unanswered after Ron brought him the ask
    /// counts as one he stayed away (PassedTo), so the asks never stop
    /// unnoticed; and a save is replayed
    /// through the same rules, so it can hold nothing play could not reach
    /// (the independent check).
    ///
    /// THE ASK IN TALK (town list 6bn): the Core knows whether Ron reached him
    /// with it (Delivered): a night Ron never did passes silently, never "they
    /// waited on you at the landing" about an ask he never had; Ron remembers
    /// its terms (Terms), so he can say where and when and that a no ends it,
    /// and the claim check lets him; and a no is two steps, since it ends the
    /// arrangement for good: a line to Ron on an ask night that sounds like
    /// one (SoundsLikeNo, the whole clause, as Silence reads an admission) gets
    /// his own plain question back (AskPlainly), and only a plain yes to that
    /// question (ConfirmsNo) is the no; a line read from free talk alone
    /// failed the independent check twice ("The drivers want Sunday off. Tell
    /// them no.", "Tell them no. Only messing."). Ron learns it is finished
    /// only when it is (HeardNo, HeardStopped), so nothing he remembers says a
    /// no the game never had, or "tonight" once it has ended.
    public sealed class Arrangement
    {
        /// The game day whose night brings the first ask: day 0, the first day,
        /// as GameTime and the cast's routines count (day 0 a Monday).
        public int FirstDay { get; private set; }
        /// Nights between asks: 2, so the second falls on the third day.
        public const int Every = 2;
        /// A night he does not turn up; three and it ends, as the old rule counted.
        public const double PatienceLossPerNoShow = 0.34;
        /// A night done wins a little back, up to whole.
        public const double PatienceGainPerNight = 0.10;
        /// Who tells every answer first (a cast id): the outfit's man.
        public const string OutfitMan = "outfit_man";
        /// Who brings the ask and carries a no down (a cast id): Ron, Mickey's doorman.
        public const string Doorman = "rocco";
        /// The hour of the morning after an ask night when the man at the
        /// landing gives up waiting.
        public const int GaveUpHour = 1;
        /// Every night's story is told under this topic and the night's day.
        public const string TopicPrefix = "player.outfit_d";

        public bool Ended { get; private set; }
        /// "refused" or "stopped", once ended.
        public string EndedWhy { get; private set; }
        public double Patience { get; private set; } = 1.0;
        readonly SortedDictionary<int, NightAnswer> _nights = new SortedDictionary<int, NightAnswer>();
        readonly HashSet<int> _delivered = new HashSet<int>();

        /// What Ron tells him, handing over the coat and the envelope, as Ron
        /// remembers it: where, when, to whom, and that a no ends it.
        public const string Terms = "I gave Mickey's nephew the envelope for the ferry landing: after ten tonight, to the man who asks for Mickey's. I told him that if he says no, Mickey's arrangement is finished.";
        /// TONIGHT'S LINE FOR RON'S TALK (ConversationEngine.Tonight), while the
        /// ask stands: what is his to answer, and that only the plain yes to
        /// Ron's own question counts.
        public const string TonightAsked = "Tonight you brought him Mickey's envelope for the ferry landing, and he has not given you his answer yet: he can take it down after ten, or tell you no, which finishes Mickey's arrangement for good. He has not refused until he says yes to the plain question that is asked for him, so never ask him yourself whether to tell them no, and never say you will tell them no or take a no down. If he seems to be turning it down, tell him plainly that a no finishes Mickey's arrangement for good, and that if he means it he need only say \"tell them no\".";
        /// Tonight's line when Ron asked him plainly and his next line was no
        /// plain yes (the independent check: the talk model took "Yes please",
        /// which the reader then missed, for the no).
        public const string TonightNotYes = "You asked him plainly whether to tell them no to the envelope, and he did not say yes: he has not refused, and the envelope is still his to take down after ten. Never say you will tell them no or take a no down; if he still means no, tell him he need only say \"tell them no\".";
        /// RON'S OWN QUESTION, said in place of a reply when a line of his
        /// sounds like a no (the talk helper): plain about what, and what a yes does.
        public const string AskPlainly = "You want me to tell them no to the envelope, boss? That's Mickey's arrangement finished, for good. Say yes and I'll take your no down the landing.";
        /// Ron's answer to his yes when live talk is off, in place of a brush-off.
        public const string TookNo = "Right you are, boss. I'll take your no down the landing.";
        /// Tonight's line once his line to Ron is read as a no.
        public const string TonightToldNo = "He has just told you no to tonight's envelope. You will take his answer down to the ferry landing tonight, and that is Mickey's arrangement finished: say so plainly.";
        /// What Ron remembers when the game has his no (Answer, Refused).
        public const string HeardNo = "He told me no to the envelope, so I'm taking his answer down to the landing tonight: that's Mickey's arrangement finished.";
        /// What Ron remembers when Tom has told Sheila he is winding Mickey's
        /// business down (town list 6cc, WoundDown).
        public const string HeardWoundDown = "He told Sheila he's winding Mickey's business down, so I'm taking word down to the landing: that's Mickey's arrangement finished.";
        /// How the outfit's man tells it.
        public const string SaidWoundDown = "Ron came down the landing to say Mickey's nephew is winding Mickey's business down: no more envelopes";
        /// What Ron remembers when the outfit stops the asks (the last night away).
        public const string HeardStopped = "Word came up from the landing: Mickey's nephew stayed away once too often, and Mickey's arrangement is finished. Nobody down there expects anything from him now.";

        public Arrangement(int firstDay = 0) { FirstDay = Math.Max(0, firstDay); }

        // The nights whose no came by his telling Sheila he is winding it down.
        readonly HashSet<int> _woundDown = new HashSet<int>();
        // The outfit's man hears it when Ron goes down that night: the story
        // waits till then (the independent check: told at twenty to ten in the
        // morning, the street had it before Ron had been anywhere).
        int _woundTellNight = -1;
        GameTime _woundTellAt;
        /// Wound down and Ron not yet down the landing with the word: when he
        /// goes, and the night it answers (town list 6cj: the man at the landing
        /// knows only then). Null and -1 otherwise.
        public GameTime? WoundWordAt => _woundTellNight >= 0 ? _woundTellAt : (GameTime?)null;
        public int WoundNight => _woundTellNight;
        /// The furthest day the arrangement walks to, as its save keeps it.
        public const int LastDay = 100000;
        /// When Ron takes word down: eleven at night, or at once if later.
        public const int RonGoesDownHour = 23;

        /// HE TOLD SHEILA HE IS WINDING IT DOWN (town list 6cc; the week's end,
        /// WeeksEnd.Give): her words close the book on Mickey's arrangements,
        /// so the arrangement ends that night, as his no to Ron does: any ask
        /// night before tonight that nobody answered passes first (PassedTo),
        /// then tonight's ask, or the next one, is answered no, Ron carries the
        /// word down and remembers it, and it is the outfit's talk. The eleventh
        /// sweep found Ron bringing the envelope the evening she closed the
        /// book. False, changing nothing, once it has ended.
        public bool WoundDown(GameTime now, GossipMill mill = null)
        {
            if (Ended) return false;
            PassedTo(NightOf(now), mill, mill != null ? now : (GameTime?)null);
            if (Ended) return false;
            int day = NextNight;
            _woundDown.Add(day);
            Record(day, NightAnswer.Refused, null, null);
            // Ron knows at once; the man at the landing when Ron goes down.
            if (mill != null && mill.Get(Doorman) is Gossiper ron)
                ron.Memory.Append(new MemoryEvent(now, "observation", 0.8, HeardWoundDown));
            var goesDown = new GameTime(now.Day, RonGoesDownHour, 0);
            _woundTellNight = day;
            _woundTellAt = now.Hour < GaveUpHour || now.TotalMinutes >= goesDown.TotalMinutes ? now : goesDown;
            TellWoundDown(mill, now);
            return true;
        }

        /// HIS NO, OR THE WINDING DOWN, REACHES THE LANDING WHEN RON GOES DOWN
        /// (the independent review of 30 September, B3: told only when the game
        /// called PassedTo at dawn, stamped eleven after the night's rounds had
        /// run without it): the game calls this as each hour turns, before the
        /// town's rounds, and the outfit's man has it from the moment it is due.
        /// And a night he stayed away, at one, when the man at the landing gives
        /// up waiting (the review's B3, its third part; the second independent
        /// check), as PassedTo files it.
        public void TellDue(GossipMill mill, GameTime now) => PassedTo(now.Day, mill, now);

        // The outfit's man has the no and the wound-down story once Ron has been
        // down (TellDue each hour; PassedTo at dawn; or later).
        void TellWoundDown(GossipMill mill, GameTime? now)
        {
            if (mill == null || !now.HasValue) return;
            if (_noTellNight >= 0 && now.Value.TotalMinutes >= _noTellAt.TotalMinutes)
            {
                mill.Witness(OutfitMan, new Fact("player", "outfit_d" + _noTellNight, Value(NightAnswer.Refused)), Said(NightAnswer.Refused), false, _noTellAt, 1.0);
                _noTellNight = -1;
            }
            if (_woundTellNight < 0 || now.Value.TotalMinutes < _woundTellAt.TotalMinutes) return;
            mill.Witness(OutfitMan, new Fact("player", "outfit_d" + _woundTellNight, "wounddown"), SaidWoundDown, false, _woundTellAt, 1.0);
            _woundTellNight = -1;
        }

        /// The nights answered, in order, for the session record and the save.
        public IReadOnlyDictionary<int, NightAnswer> Nights => _nights;

        /// The night of the next ask, or -1 once the arrangement has ended.
        public int NextNight => Ended ? -1 : FirstDay + Every * _nights.Count;

        /// Whether the outfit asks on this day's night.
        public bool AsksOn(int day) => !Ended && day == NextNight;

        /// When the man at the landing gives up waiting on this night's answer.
        public static GameTime GaveUpAt(int day) => new GameTime(day + 1, GaveUpHour, 0);

        /// WHETHER TONIGHT'S ASK STANDS at `now`: Ron has brought it, it is not
        /// answered, and the man at the landing has not given up waiting. The
        /// game sends the talk helper "ask": {"tonight": true} with lines to Ron
        /// only while this holds.
        public bool AskStands(GameTime now)
        {
            int night = NightOf(now);
            return AsksOn(night) && _delivered.Contains(night);
        }

        /// The day whose night it is at `now`: until one in the morning, the
        /// day before's.
        public static int NightOf(GameTime now) => now.Hour < GaveUpHour ? now.Day - 1 : now.Day;

        /// The topic the night's story is told under, as the session record keys deeds.
        public static string TopicFor(int day) => TopicPrefix + day;

        /// Whether a story is one of the arrangement's nights.
        public static bool IsNight(Rumor r) => r != null && r.TopicKey != null && r.TopicKey.StartsWith(TopicPrefix, StringComparison.Ordinal);

        /// How each answer is told, as the outfit's man saw it himself.
        public static string Said(NightAnswer a) =>
            a == NightAnswer.Did ? "Mickey's nephew brought the envelope down the landing"
            : a == NightAnswer.Refused ? "Ron came down the landing to say Mickey's nephew told them no"
            : "Mickey's nephew never turned up at the landing";

        /// The word each answer's story carries.
        public static string Value(NightAnswer a) =>
            a == NightAnswer.Did ? "did" : a == NightAnswer.Refused ? "refused" : a == NightAnswer.NoShow ? "noshow" : "undelivered";

        /// RON REACHED HIM WITH TONIGHT'S ASK: the coat and the envelope handed
        /// over, the terms said. With `ron` (his gossiper) and `now`, Ron
        /// remembers the terms, which the game sends his talk like any memory.
        /// False, changing nothing, unless the outfit asks tonight, he has not
        /// had it yet and, with `now`, it is that night (from its morning until
        /// one the next morning, NightOf).
        public bool Delivered(int day, Gossiper ron = null, GameTime? now = null)
        {
            if (!AsksOn(day) || (now.HasValue && NightOf(now.Value) != day) || !_delivered.Add(day)) return false;
            if (ron != null && now.HasValue) ron.Memory.Append(new MemoryEvent(now.Value, "observation", 0.8, Terms));
            return true;
        }

        /// Whether Ron reached him with this night's ask.
        public bool WasDelivered(int day) => _delivered.Contains(day);

        /// He answered this night's ask. Returns false, changing nothing, unless
        /// it is the night the outfit asks (NextNight); a night away (NoShow)
        /// only once Ron has reached him with it, and Undelivered never (only
        /// PassedTo marks a night the ask never reached him). Taking the
        /// envelope or telling Ron no means he had it; with `now`, only before
        /// the man at the landing gives up waiting (GaveUpAt), so the game
        /// answers a no as of when he said it. With `mill`, the night's story
        /// goes into the gossip, told first by whoever knows it at `now`, which
        /// must then be given, and Ron, if the mill has him, learns when it ends.
        public bool Answer(int day, NightAnswer what, GossipMill mill = null, GameTime? now = null)
        {
            if (mill != null && !now.HasValue) throw new ArgumentException("the story needs the time it is told", nameof(now));
            if (what == NightAnswer.Undelivered || !AsksOn(day)) return false;
            if (what == NightAnswer.NoShow && !_delivered.Contains(day)) return false;
            // NO NO BEFORE THE ASK (the independent review of 30 September): a no
            // told as of a time needs Ron to have brought that night's ask first.
            if (what == NightAnswer.Refused && now.HasValue && !_delivered.Contains(day)) return false;
            if (what != NightAnswer.NoShow && now.HasValue && now.Value.TotalMinutes >= GaveUpAt(day).TotalMinutes) return false;
            // ONLY ON ITS OWN NIGHT (the port's independent check, 30 September:
            // an envelope two nights ahead could be done on the Monday, and a
            // night away filed before the landing opened): the envelope or the no
            // on that night, the night away once the man has given up waiting.
            if (now.HasValue && what != NightAnswer.NoShow && NightOf(now.Value) != day) return false;
            // The envelope is handed over at the landing, while its man is there
            // (the independent check: done at nine that morning, he was filed as
            // seeing it at nine).
            if (now.HasValue && what == NightAnswer.Did && !TheLanding.There(now.Value)) return false;
            if (now.HasValue && what == NightAnswer.NoShow && now.Value.TotalMinutes < GaveUpAt(day).TotalMinutes) return false;
            _delivered.Add(day);
            // A PLAIN NO GOES DOWN WITH RON, as the wound-down word does (the
            // port's independent check): the man at the landing knows it only
            // when Ron has been down, at eleven or at once if later; Ron knows now.
            if (what == NightAnswer.Refused && now.HasValue)
            {
                Record(day, what, null, now);
                if (mill?.Get(Doorman) is Gossiper ron) ron.Memory.Append(new MemoryEvent(now.Value, "observation", 0.8, HeardNo));
                var goesDown = new GameTime(now.Value.Day, RonGoesDownHour, 0);
                _noTellNight = day;
                _noTellAt = now.Value.Hour < GaveUpHour || now.Value.TotalMinutes >= goesDown.TotalMinutes ? now.Value : goesDown;
                TellWoundDown(mill, now);
                return true;
            }
            return Record(day, what, mill, now);
        }

        // A plain no waiting for Ron to take it down: the night and when he goes.
        int _noTellNight = -1;
        GameTime _noTellAt;
        /// His no, not yet at the landing: when Ron takes it down; null otherwise.
        public GameTime? NoWordAt => _noTellNight >= 0 ? _noTellAt : (GameTime?)null;
        /// The night the no waiting for Ron answers; -1 when none waits.
        public int NoNight => _noTellNight;

        bool Record(int day, NightAnswer what, GossipMill mill, GameTime? now)
        {
            _nights[day] = what;
            if (what == NightAnswer.Undelivered) return true;
            if (what == NightAnswer.Refused) { Ended = true; EndedWhy = _woundDown.Contains(day) ? "wound down" : "refused"; }
            else if (what == NightAnswer.Did) Patience = Math.Min(1.0, Patience + PatienceGainPerNight);
            else
            {
                Patience = Math.Max(0.0, Patience - PatienceLossPerNoShow);
                if (Patience <= 1e-9) { Ended = true; EndedWhy = "stopped"; }
            }
            if (mill != null)
            {
                bool wound = _woundDown.Contains(day);
                mill.Witness(OutfitMan, new Fact("player", "outfit_d" + day, Value(what)), wound ? SaidWoundDown : Said(what), what == NightAnswer.Did, now.Value, 1.0);
                if (Ended && mill.Get(Doorman) is Gossiper ron)
                    ron.Memory.Append(new MemoryEvent(now.Value, "observation", 0.8, wound ? HeardWoundDown : what == NightAnswer.Refused ? HeardNo : HeardStopped));
            }
            return true;
        }

        /// The day is now `day`: every ask night before it that nobody answered
        /// (a dawn the game missed, a load that skipped a night) counts as one
        /// he stayed away if Ron had reached him with it, told by the outfit's
        /// man when a mill is given: as of one in the morning after that night,
        /// when he gave up waiting; with `now`, a night whose man is still
        /// waiting does not pass yet. A night Ron never reached him passes
        /// silently (Undelivered). The game calls it at each dawn and after
        /// every load.
        public void PassedTo(int day, GossipMill mill = null, GameTime? now = null)
        {
            if (mill != null && !now.HasValue) throw new ArgumentException("the story needs the time it is told", nameof(now));
            // With `now`, a night passes only once the man has given up waiting
            // (the independent check: a load between midnight and one passed a
            // night whose ask still stood).
            TellWoundDown(mill, now);
            // NO FURTHER THAN A SAVE CAN HOLD (the port's independent check, 30
            // September: a far-future day was walked night by night, ten million
            // nights and a 244 MB save): the save keeps days under LastDay.
            day = Math.Min(day, LastDay);
            while (!Ended && NextNight < day && (!now.HasValue || GaveUpAt(NextNight).TotalMinutes <= now.Value.TotalMinutes))
            {
                GameTime? told = null;
                if (now.HasValue) told = GaveUpAt(NextNight);
                if (_delivered.Contains(NextNight)) Record(NextNight, NightAnswer.NoShow, mill, told);
                else Record(NextNight, NightAnswer.Undelivered, null, null);
            }
        }

        // HOW A NO IS READ (the independent check of town list 6bn): as Silence
        // reads an admission, the whole clause must be the no, and every other
        // clause of the sentence only the words people put round one. That
        // only decides whether Ron asks him plainly; the no is the plain yes.
        static string Words(string s) =>
            " " + Regex.Replace(Apostrophes(s).ToLowerInvariant().Replace("'", ""), @"[^a-z]+", " ").Trim() + " ";

        static string Apostrophes(string s) => (s ?? "").Replace('\u2019', '\'').Replace('\u2018', '\'').Replace('`', '\'').Replace('\u00b4', '\'');

        static List<string> Sentences(string said)
        {
            var list = new List<string>();
            foreach (var raw in Regex.Split(Apostrophes(said), @"(?<=[.!?])\s+"))
            {
                var t = raw.Trim();
                if (t.Length > 0) list.Add(t);
            }
            return list;
        }

        const string Lead = @"(no |nah |nope |look |listen |sorry |right |ron |well |so |honestly |just |ok |okay |alright |all right |you |go and |go )*";
        const string What = @"(it|that|this|the envelope|their envelope|mickeys envelope|any of it|their errands|mickeys errands|their dirty work|mickeys dirty work)";
        const string After = @"( for them| anymore| any more| again| down there| down| there| to the landing| down the landing| down to the landing)*";
        const string Tail = @"( (then|ron|mate|boss|pal|love|sorry|honestly|mind|from me|for me|for good|and thats final|and thats that|thanks|thank you))* $";
        // The whole clause that says no to the ask.
        static readonly Regex RefuseClause = new Regex(@"^ " + Lead + "(" +
            @"tell (them|em|him|the outfit|them lot|that lot|the man|mickeys people) (no|its a no|the answers no|my answers no|the answer is no|i said no|im not doing it|i wont do it|im not interested|to find (somebody|someone) else|to get (somebody|someone) else|where to stick it|to sling their hook|to get lost)" +
            @"|(im|i am) not (doing|taking|carrying|running|touching|delivering) " + What + After +
            @"|(im|i am) not going to (do|take|carry|run|touch|deliver) " + What + After +
            @"|i (wont|will not|shant|refuse to|aint going to|aint gonna) (do|take|carry|run|touch|deliver) " + What + After +
            @"|i (wont|will not|shant) be (doing|taking|carrying|running) " + What + After +
            @"|count me out|no deal|(the|my) answers no|(the|my) answer is no|(its|thats) a no|no thanks|no thank you|(im|i am) not interested|find (somebody|someone) else|forget it" +
            @"|ill have nothing to do with (it|this|that|any of it)|i will have nothing to do with (it|this|that|any of it)" +
            @"|i said no|(im|i am) out|(im|i am) not going( down)? (to the landing|down the landing|to the ferry|down there|there)" +
            @"|i (cant|cannot) do (it|that|this)|i dont want to do (it|that|this)|i dont want (any part|no part) of (it|this|that)|(im|i am) not coming|tell (them|em) (im|i am) not coming" +
            @"|(im|i am) having no part (of|in) (it|this|that|any of it)|i want no part (of|in) (it|this|that|any of it)" +
            @"|i want nothing to do with (it|this|that|any of it)|mickeys arrangement is (finished|over|done)" +
            ")" + Tail);
        // A clause of the words round a no, which says nothing of its own.
        static readonly Regex AroundClause = new Regex(
            @"^ ((no|nah|nope|look|listen|sorry|right|ron|mate|boss|pal|love|well|so|honestly|then|ok|okay|alright|all right|thanks|ta|cheers|mind|never|not a chance|no chance|no way|not on your life|absolutely not|definitely not|certainly not|im sorry|thats final|and thats final|thats that|and thats that|end of|end of story|my minds made up)( |$))+$");
        // Anywhere in the line, it is no plain no: taken back, put off,
        // supposed, or somebody else's words ("Darren said tell them no"; "tell
        // them I said no" is his own).
        static readonly Regex TakenBack = new Regex(
            @" (only joking|just joking|joking|kidding|only messing|messing|having you on|winding you up|pulling your leg|yeah right|as if|not really|on second thoughts?|second thoughts|changed my mind|actually|wait|hang on|hold on|think about it|ill (do|take|carry|go|think)|ill have (it|that|the envelope)|im (doing|taking|going)|i will (do|take|go)|course (im|i am|i will|ill)|give it here|hand it over|go on then|maybe|perhaps|probably|not likely|or not|or should i|should i|shall i|unless|if|what if|suppose|supposing|not yet|yet|tonight|tomorrow|later|for now|this time|next time) " +
            @"| (?!i )[a-z]+ (said|says|reckons|told me|tells me) ");
        // His plain yes to Ron's own question, read over the whole sentence,
        // commas or none (the independent check: "Yes please" was missed): only
        // these words and phrases, and one of them a yes.
        static readonly Regex YesSentence = new Regex(
            @"^ ((yes|yeah|yep|yup|aye|sure|definitely|certainly|absolutely|of course|course|correct|exactly|right|thats right|that is right|thats it|thats what i said|thats my answer|you heard me|you heard|i do|i am|im sure|i am sure|im certain|i mean it|do it|go ahead|please do|tell them no|tell em no|its a no|thats a no|im not doing it|i am not doing it|im not taking it|i wont do it|find someone else|find somebody else|i said no|count me out|yea|sir|please|ron|mate|boss|pal|love|then|thanks|ta|cheers|honestly|ok|okay|sorry|for good|thats final|and thats final)( |$))+$");
        static readonly Regex YesWord = new Regex(
            @" (yes|yeah|yea|yep|yup|aye|sure|definitely|certainly|absolutely|of course|correct|exactly|thats right|that is right|thats it|thats what i said|thats my answer|you heard me|i do|im sure|i am sure|im certain|i mean it|tell them no|tell em no|its a no|thats a no) ");
        // What only sounds like a yes: brushing him off ("Yeah yeah."), or
        // telling them something else ("Tell them thanks.").
        static readonly Regex NotAYes = new Regex(@" (yeah yeah|sure sure|aye aye|yep yep) | tell (them|em) (?!no )");
        // The words round that yes: nothing that could be a no to the question.
        static readonly Regex PoliteClause = new Regex(
            @"^ ((ron|mate|boss|pal|love|then|please|thanks|ta|cheers|honestly|ok|okay|sorry|im sorry|thats final|and thats final|for good|look|listen)( |$))+$");

        // Every clause of the sentence the shape or the words round it, and one the shape.
        static bool AllClauses(string sentence, Regex shape, Regex around)
        {
            bool found = false;
            foreach (var clause in sentence.TrimEnd('.', '!', '?').Split(new[] { ',', ';', ':', '\u2014', '\u2013' }, StringSplitOptions.RemoveEmptyEntries))
            {
                var w = Words(clause);
                if (w.Trim().Length == 0) continue;
                if (shape.IsMatch(w)) found = true;
                else if (!around.IsMatch(w)) return false;
            }
            return found;
        }

        // A sentence that answers Ron's question yes: a plain yes and the words
        // round it, never a line that is only a refusal, which said back to his
        // question can mean "no, don't" (the independent check: "No thanks.",
        // "Forget it." ended it).
        static bool AnswersYes(string sentence)
        {
            var w = Words(sentence);
            return YesSentence.IsMatch(w) && YesWord.IsMatch(w) && !NotAYes.IsMatch(w);
        }

        static bool AnyTakenBack(List<string> sentences)
        {
            foreach (var s in sentences) if (TakenBack.IsMatch(Words(s))) return true;
            return false;
        }

        /// WHETHER A LINE OF HIS TO RON SOUNDS LIKE A NO to the ask: a clause
        /// that is a plain no to it ("Tell them no, Ron.", "I'm not doing it.",
        /// "Count me out.", "No thanks."), in no question, and nothing in the
        /// line supposed, put off till later, taken back or somebody else's
        /// words; never a bare "no". It is never the no itself, only whether
        /// Ron asks him plainly (AskPlainly, which names the envelope), so it
        /// reads wider than the no: only his plain yes (ConfirmsNo) ends it.
        /// The game asks only while tonight's ask stands (AskStands).
        public static bool SoundsLikeNo(string said)
        {
            var sentences = Sentences(said);
            if (AnyTakenBack(sentences)) return false;
            foreach (var s in sentences)
            {
                if (s.EndsWith("?")) continue;
                foreach (var clause in s.TrimEnd('.', '!').Split(new[] { ',', ';', ':', '\u2014', '\u2013' }, StringSplitOptions.RemoveEmptyEntries))
                    if (RefuseClause.IsMatch(Words(clause))) return true;
            }
            return false;
        }

        /// HIS ANSWER TO RON'S OWN QUESTION (AskPlainly), his next line to
        /// anybody: the whole line a plain yes and the words round it ("Yes.",
        /// "Yes please", "Yes, I'm sure", "Sure.", "That's right, Ron.", "Tell
        /// them no.", "Yes, I'm not doing it."), every sentence of it; never a
        /// question, never a refusal alone ("No thanks.", "Forget it."), never
        /// a brush-off ("Yeah yeah."), nothing else beside it, nothing taken back.
        public static bool ConfirmsNo(string said)
        {
            var sentences = Sentences(said);
            // "Forget it" said back to his question can mean "never mind"
            // (the independent check: "Yeah, forget it.").
            if (sentences.Count == 0 || AnyTakenBack(sentences) || Words(said).Contains(" forget it ")) return false;
            bool yes = false;
            foreach (var s in sentences)
            {
                if (s.EndsWith("?")) return false;
                if (AnswersYes(s)) yes = true;
                // Beside a yes, a sentence that is only a no to the ask ("Yes,
                // I'm sure. I'm not doing it."); alone it is no yes.
                else if (!AllClauses(s, PoliteClause, PoliteClause) && !AllClauses(s, RefuseClause, AroundClause)) return false;
            }
            return yes;
        }

        /// For any save's JSON: "first", the first night's day; "nights", [day,
        /// answer] pairs in order; "delivered", the ask nights Ron reached him.
        /// Patience and the end follow from them.
        public Dictionary<string, object> ToJson()
        {
            var nights = new List<object>();
            foreach (var kv in _nights) nights.Add(new List<object> { (double)kv.Key, Value(kv.Value) });
            var delivered = new List<object>();
            var days = new List<int>(_delivered);
            days.Sort();
            foreach (var d in days) delivered.Add((double)d);
            var d0 = new Dictionary<string, object> { { "first", (double)FirstDay }, { "nights", nights }, { "delivered", delivered } };
            if (_woundDown.Count > 0) { var w = new List<object>(); foreach (var x in _woundDown) w.Add((double)x); d0["woundDown"] = w; }
            if (_woundTellNight >= 0) d0["woundTell"] = new List<object> { (double)_woundTellNight, (double)_woundTellAt.TotalMinutes };
            if (_noTellNight >= 0) d0["noTell"] = new List<object> { (double)_noTellNight, (double)_noTellAt.TotalMinutes };
            return d0;
        }

        /// From ToJson's values, replayed in order through Answer: the first
        /// night that play could not have reached, and everything after it, is
        /// dropped, so a hand-edited save holds only what play could.
        public static Arrangement FromJson(Dictionary<string, object> saved)
        {
            int first = 0;
            if (saved != null && saved.TryGetValue("first", out var f) && f is double fd && fd >= 0 && fd < 100000 && fd == Math.Floor(fd)) first = (int)fd;
            var a = new Arrangement(first);
            if (saved == null) return a;
            var delivered = new HashSet<int>();
            // A save from before the ask in talk (no "delivered") knew no night
            // he never had: its nights away stand (the independent check).
            bool before6bn = !saved.ContainsKey("delivered");
            if (saved.TryGetValue("delivered", out var dl) && dl is List<object> dlist)
                foreach (var x in dlist) if (x is double dd && dd >= 0 && dd < 100000 && dd == Math.Floor(dd)) delivered.Add((int)dd);
            var wound = new HashSet<int>();
            if (saved.TryGetValue("woundDown", out var wl) && wl is List<object> wlist)
                foreach (var x in wlist) if (x is double wd && wd >= 0 && wd < 100000 && wd == Math.Floor(wd)) wound.Add((int)wd);
            if (saved.TryGetValue("nights", out var n) && n is List<object> nights)
                foreach (var x in nights)
                {
                    if (!(x is List<object> pair) || pair.Count != 2 || !(pair[0] is double d) || !(pair[1] is string v) || d != Math.Floor(d)) break;
                    NightAnswer? ans = v == "did" ? NightAnswer.Did : v == "refused" ? NightAnswer.Refused : v == "noshow" ? NightAnswer.NoShow
                                     : v == "undelivered" ? NightAnswer.Undelivered : (NightAnswer?)null;
                    if (!ans.HasValue || !a.AsksOn((int)d)) break;
                    int day = (int)d;
                    // A night away needs the ask delivered, a night it never reached him needs it not.
                    if (ans.Value == NightAnswer.Undelivered)
                    {
                        if (delivered.Contains(day)) break;
                        a.Record(day, NightAnswer.Undelivered, null, null);
                        continue;
                    }
                    if (ans.Value == NightAnswer.NoShow && !delivered.Contains(day) && !before6bn) break;
                    // Wound down only from the week's end (the independent check:
                    // a save could wind down night 0); otherwise a plain no.
                    if (ans.Value == NightAnswer.Refused && wound.Contains(day) && day >= first + WeeksEnd.After)
                    {
                        // Replayed as it was made: delivered only if Ron had
                        // brought it before she closed the book (the independent
                        // check: a load marked it delivered; the time-and-state
                        // sweep: brought at eight, wound down at half past, a
                        // load forgot it had been).
                        if (delivered.Contains(day)) a._delivered.Add(day);
                        a._woundDown.Add(day);
                        a.Record(day, NightAnswer.Refused, null, null);
                        continue;
                    }
                    if (!a.Answer(day, ans.Value) && !(ans.Value == NightAnswer.NoShow && a.Delivered(day) && a.Answer(day, ans.Value))) break;
                }
            // Tonight's ask, had and not yet answered.
            if (!a.Ended && delivered.Contains(a.NextNight)) a.Delivered(a.NextNight);
            // A wound-down story the outfit's man has not had yet.
            if (saved.TryGetValue("woundTell", out var wt) && wt is List<object> wtl && wtl.Count == 2 && wtl[0] is double tn && wtl[1] is double tm
                // A whole night, and no later than play can make it: before one
                // (the time-and-state sweep: 6.5 was read as night 6, and one
                // o'clock itself was kept, as noTell's bound does not).
                && tn == Math.Floor(tn) && tn >= 0 && tn < 100000
                && a._woundDown.Contains((int)tn) && tm == Math.Floor(tm)
                && tm >= ((int)tn - Every) * 24.0 * 60 && tm < ((int)tn + 1) * 24.0 * 60 + GaveUpHour * 60)
            {
                a._woundTellNight = (int)tn;
                a._woundTellAt = GameTime.FromTotalMinutes((long)tm);
            }
            // A plain no the outfit's man has not had yet: only for a night
            // answered no, not wound down, and taken down that night.
            if (saved.TryGetValue("noTell", out var nt) && nt is List<object> ntl && ntl.Count == 2 && ntl[0] is double nn && ntl[1] is double nm
                && nn == Math.Floor(nn) && nn >= 0 && nn < 100000 && a._nights.TryGetValue((int)nn, out var said) && said == NightAnswer.Refused
                && !a._woundDown.Contains((int)nn) && nm == Math.Floor(nm)
                // Only when play could make it (the independent check): from Ron's
                // hour that night until the man gives up waiting.
                && nm >= (int)nn * 24.0 * 60 + RonGoesDownHour * 60 && nm < ((int)nn + 1) * 24.0 * 60 + GaveUpHour * 60)
            {
                a._noTellNight = (int)nn;
                a._noTellAt = GameTime.FromTotalMinutes((long)nm);
            }
            return a;
        }
    }
}
