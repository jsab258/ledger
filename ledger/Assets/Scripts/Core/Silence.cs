using System.Text.RegularExpressions;

namespace Ledger.Core
{
    /// OWNING UP, AND "KEEP IT TO YOURSELF" (town list 6al; A15.18 and A20.15,
    /// the third checklist sweep). A friend seen at the window is asked about it
    /// and types "yeah, it was me" or "keep it to yourself". Neither counted:
    /// they asked again in every reply, and a character who said "not a word"
    /// had the town's gossip pass the story on anyway, a promise the world did
    /// not keep.
    ///
    /// The line is read in narrow shapes, as Claims.WhereHeSays reads a place:
    /// missing an admission costs a question asked again, while reading one he
    /// never made would tell the town something false (the independent check:
    /// "you're looking at me like it was me" and "it was me mum on the phone"
    /// were read as owning up). So an admission is a whole clause of the plain
    /// shape, with nothing else in its sentence but the words people put round
    /// one ("yeah", "so what", "not Darren"). The Core decides whether they keep
    /// quiet (canon: LLMs classify, never adjudicate), from who they are (the
    /// cast file's "keepsQuiet"), how well they know him, and how grave the deed
    /// is; the character is told the outcome, and the game whom its gossip keeps
    /// quiet. Money and threats are other verbs (Gossip's Bribe and Intimidate),
    /// so a line carrying either is not read as asking.
    public enum KeepsQuietFor
    {
        /// Keeps it quiet only for somebody on first-name terms with them.
        Friend,
        /// Mickey's own people: keeps it quiet for the new owner, whom they work for.
        Owner,
        /// Says yes to anybody, and the silence breaks as easily as it was given.
        Anyone,
        /// Keeps nothing quiet for the asking.
        Nobody,
    }

    public static class Silence
    {
        static string Words(string s) =>
            " " + Regex.Replace((s ?? "").ToLowerInvariant().Replace('’', '\'').Replace("'", ""), @"[^a-z]+", " ").Trim() + " ";

        static System.Collections.Generic.List<string> Sentences(string said)
        {
            var list = new System.Collections.Generic.List<string>();
            foreach (var raw in Regex.Split((said ?? "").Replace('’', '\''), @"(?<=[.!?])\s+"))
            {
                var t = raw.Trim();
                if (t.Length > 0) list.Add(t);
            }
            return list;
        }

        // The whole clause that owns up, and nothing else in it.
        static readonly Regex AdmitClause = new Regex(
            @"^ (yeah |yes |aye |all right |alright |ok |okay |fine |right |look |listen |so |well |oh )*" +
            @"((it|that) (was|were) me( (that|what|who|as) (broke|did|done|smashed|put) (it|that|the window|that window|your window)( in)?)?" +
            @"|twas me|i (did|done) (it|that)( and im not sorry| and i aint sorry)?|guilty as charged" +
            @"|i (put|broke|smashed) (it|the window|that window|your window)( in)?)" +
            @"( (then|mate|boss|love|pal|honest|so what|alright|all right|ok|okay))* $");
        // What people put round an admission, as clauses of their own.
        static readonly Regex AroundClause = new Regex(
            @"^ ((yeah|yes|aye|all right|alright|ok|okay|fine|right|look|listen|so|well|oh|then|mate|boss|love|pal|honest|so what|happy now|satisfied|eh|there|there you go|there you are)( |$))+$" +
            @"|^ not [a-z]+( [a-z]+)? $|^ and im not sorry $|^ and i aint sorry $|^ i admit it $|^ (ill pay for it|ill make it good|ill make it right|im sorry|sorry|sorry about that) $");
        // A tag after an admission that may end in a question mark.
        static readonly Regex TagQuestion = new Regex(@"^ (so what|alright|all right|ok|okay|happy now|satisfied|what of it|what about it) $");
        // Said as a joke, it was never owned up to.
        static readonly Regex Taken = new Regex(@" (as if|only joking|just joking|joking|kidding|pulling your leg|having you on|yeah right|prove it|not likely|not really|not a chance|not half|not at all|thats what you reckon|is that what you think) |^ not $");

        /// Whether a line of his owns up to the deed: a sentence that is a plain
        /// admission and the words round it ("Yeah, it was me.", "It was me, not
        /// Darren.", "Yeah, I did it, so what?"), never a denial, a supposition,
        /// a comparison, somebody else's words or a joke.
        public static bool OwnsUp(string said)
        {
            var sentences = Sentences(said);
            foreach (var s in sentences) if (Taken.IsMatch(Words(s))) return false;
            foreach (var sentence in sentences)
            {
                bool question = sentence.EndsWith("?");
                var clauses = sentence.TrimEnd('.', '!', '?').Split(new[] { ',', ';', ':' }, System.StringSplitOptions.RemoveEmptyEntries);
                bool admits = false, other = false;
                for (int i = 0; i < clauses.Length; i++)
                {
                    var w = Words(clauses[i]);
                    if (w.Trim().Length == 0) continue;
                    if (AdmitClause.IsMatch(w)) admits = true;
                    else if (AroundClause.IsMatch(w)) { }
                    else other = true;
                }
                // A question only when its last clause is a tag ("so what?").
                if (question && (clauses.Length < 2 || !TagQuestion.IsMatch(Words(clauses[clauses.Length - 1])))) continue;
                if (admits && !other) return true;
            }
            return false;
        }

        // THE ASK AS A WHOLE CLAUSE (the third review of 6cd: an ask with a
        // menace in its own sentence, "Keep your mouth shut or there'll be
        // trouble", "Keep it to yourself, or you're for it", bought silence):
        // the ask and only the words round one; every other clause of its
        // sentence filler or his owning up.
        const string Anyone = @"(anyone|anybody|a soul|nobody|the police|the coppers|the law|the old bill|the bizzies|rita|ron|darren|sheila|ada|her|him|them|[a-z]+)";
        static readonly Regex AskClause = new Regex(@"^ (please |just |so |look |listen |and |but |now |yeah |ok |okay |sheila |love |mate |ada |darren |ron |do me a favour and |do us a favour and )*(" +
            @"keep (it|this|that) (to yourself|quiet|under your hat|between us|between ourselves)( for (me|now))?" +
            @"|(dont|do not) (go )?(tell|telling|mention it to|mention this to|mention that to|say anything to) " + Anyone + "( else)?( (about (it|this|that|me)|it was me|you saw me|what you saw))?" +
            @"|(dont|do not) (tell|mention (this|that))" +
            @"|(promise|swear) (me )?(you wont|you will not|youll not) (tell|say anything to) " + Anyone +
            @"|(can|could|shall) we keep (it|this|that) (between (us|ourselves|you and me|us two)|quiet|to ourselves)" +
            @"|keep (it|this|that) between (you and me|us two|ourselves|us)" +
            @"|lets keep (it|this|that) (between (us|ourselves|you and me|us two)|quiet|to ourselves)" +
            @"|keep quiet( about (it|this|that))?" +
            @"|(dont|do not) (say|breathe) (a word|anything|owt|nothing)( (to|about it to) " + Anyone + ")?" +
            @"|not a word( to " + Anyone + ")?" +
            @"|keep (your|ya) (mouth|trap|gob) shut( about (it|this|that))?|keep (schtum|shtum|stum|mum)|mums the word" +
            @"|(this|it|that) stays between us|(can|could|will|would) you keep (it|this|that) (quiet|to yourself|between us)|can you keep a secret" +
            @"|you (wont|will not) (tell|say anything to) " + Anyone +
            @"|(id |i would )?(rather|prefer) you (kept|keep) (it|this|that) (to yourself|quiet)|say nothing( to " + Anyone + ")?" +
            @")( (please|sheila|love|mate|pal|eh|will you|would you|yeah|ok|okay|for me|for now|thanks|right|alright|all right|ada|darren|ron|rita))* $");
        // Not asking: money or a threat (other verbs), somebody else's words,
        // asking why they did not, or a turn of phrase.
        static readonly Regex NotAsking = new Regex(
            @" (or else|or youll|or ill|or youre next|youll regret|watch yourself|if you know whats good|if you want to keep|keep your teeth|see you right|worth your while|sort you out|quid|tenner|fiver|pounds|pay you|money|cash|heres" +
            @"|unless you want|nobody gets hurt|make it up to you|make it worth" +
            @"|did you|have you|why|couldnt you|didnt you|wouldnt you|shouldnt you|he said|she said|they said|told me to|told you to|a word of a lie|a word of truth" +
            @"|a word to say|just listen|hear me out|in here|said|used to say|(anyone|anybody) (where|what|who|how|when|why)) ");

        // A sentence that is an ask for silence as a whole: an ask clause, and
        // every other clause filler, a word of address or his owning up.
        static bool IsAskSentence(string sentence)
        {
            if (NotAsking.IsMatch(Words(sentence))) return false;
            bool asks = false;
            foreach (var clause in sentence.TrimEnd('.', '!', '?').Split(new[] { ',', ';', ':', '\u2014', '\u2013' }, System.StringSplitOptions.RemoveEmptyEntries))
            {
                var cw = Words(clause);
                if (cw.Trim().Length == 0) continue;
                if (AskClause.IsMatch(cw)) { asks = true; continue; }
                if (Filler.IsMatch(cw) || OwnsUp(clause) || AddressOnly.IsMatch(cw)) continue;
                return false;
            }
            return asks;
        }

        /// WHETHER A LINE OF HIS MENACES THEM AT ALL (the fifth review of 6cd):
        /// read wide, since it files no story and weighs nothing: it only keeps
        /// any later ask over the deed from buying silence, and has her own
        /// promise of silence caught.
        public static bool Menaces(string said) => !string.IsNullOrWhiteSpace(said) && (Threatens(said) || Menacing.IsMatch(Words(said)));

        // Menace words anywhere keep a line from being an ask for silence;
        // wide on purpose: missing an ask costs a question asked again.
        static readonly Regex Menacing = new Regex(
            @" (youll be sorry|you will be sorry|youll regret|you will regret|youll wish|you will wish|i know where you live|ill get you|break your|hurt you|kill you|youll get hurt|you will get hurt|youll pay|you will pay|whats good for you|or else|or youll|or you will|or ill|or i will|you saw nothing|you never saw|a slap|a hiding|stay healthy|shut it for you|or you know what|youre dead|youre for it|youre finished|therell be trouble|therell be consequences|no one gets hurt|nobody gets hurt|you wont get hurt|live longer|healthier|a kicking|a smack|your windows|your head|what happens to grasses|the worse for you|otherwise ill|or ya|ya ll be sorry|yall be sorry|or it ll|or itll" +
            // The sixth review's ordinary menaces.
            @"|do you in|smash your face|your face in|watch your back|watch yourself|im warning you|i am warning you|in one piece|a good hiding|youll be in trouble|youre in trouble|youre in for it|youll be in for it" +
            @"|come after you|have me to deal with|answer to me|shame if anything|anything happened to you|anything was to happen|didnt see anything|you didnt see nothing|forget you saw|you grass you die|grass and you die|last warning" +
            @"|dont cross me|one word and|breathe a word of|or youre dead|youre dead|ill find you|ill be watching|i know where you live) ");

        /// Whether a line of his asks them to keep the matter quiet: "Keep it to
        /// yourself.", "Can you keep this quiet?", "Don't tell anyone.", "Not a
        /// word to Rita, eh?"; never with money or a threat in the same sentence,
        /// nor asking why they did not.
        public static bool AsksQuiet(string said)
        {
            // Never with a threat anywhere in the line (the independent check:
            // "Keep it to yourself. I know where you live." was an ask).
            if (Threatens(said) || Menacing.IsMatch(Words(said))) return false;
            // Every sentence the ask, owning up, or the words round them:
            // anything else beside it ("Or I'll kill you.") makes it no plain
            // ask (the second review of 6cd: a threat still bought silence).
            bool any = false;
            foreach (var sentence in Sentences(said))
            {
                if (IsFiller(sentence) || OwnsUp(sentence)) continue;
                if (!IsAskSentence(sentence)) return false;
                any = true;
            }
            return any;
        }

        // A THREAT TO KEEP QUIET (town list 6cd; carried until Jafar rules on
        // his 30 September page: this week a threat never buys silence; it is
        // the street's story and makes them warier; the 1990 research,
        // production/research/threats-1990). Read as an admission is: a whole
        // sentence of a threat's plain shape and nothing else but the words
        // round one, since reading a threat he never made would tell the town
        // he threatened somebody (the independent check: menace words alone
        // took "I'll do you a favour", "You never saw me, I was at home" and
        // "Don't tell Rita or I'll never hear the end of it" for threats).
        // Missing an unusual threat costs less.
        const string Whom = @"( (to|about it to|about this to) (anyone|anybody|a soul|rita|the police|the coppers|the law|the old bill|them|her|him))?";
        const string Pays = @"(regret it|be sorry|wish you hadnt|wish you never had|get hurt|pay for it|pay for that)";
        // What follows "and" in a threat: his doing, or theirs to suffer.
        const string Then = @"((youll|you will) " + Pays + @"|youre (dead|for it|finished)|(ill|i will) (kill|hurt|do|sort) you( out)?)";
        const string Hush = @"(not a word( to (anyone|anybody|a soul|rita|the police|the coppers|the law|the old bill|them|her|him))?|keep (it|this|that) (quiet|to yourself|shut|under your hat)|(dont|do not) (say|breathe) (a word|anything|owt)|(dont|do not) (tell|mention it to|go telling) (anyone|anybody|a soul|rita|the police|the coppers|the law|the old bill)|keep quiet( about (it|this|that))?|keep (your|ya) (mouth|gob|trap) shut( about (it|this|that))?|say nothing)";
        static readonly Regex ThreatSentence = new Regex(@"^ (look |listen |right |now |so |just |and |you hear me )*(" +
            @"(say|breathe|utter|mention|whisper) (a word|one word|anything|a thing|owt|this|that|it)" + Whom + " and " + Then +
            @"|(tell|grass to|go to|go running to) (anyone|anybody|a soul|rita|the police|the coppers|the law|the old bill) and " + Then +
            @"|(grass|grass me up|shop me|dob me in) and " + Then +
            @"|(open|you open) (your|ya) (mouth|gob|trap) and " + Then +
            @"|" + Hush + " or (else( youll " + Pays + ")?|youll " + Pays + ")" +
            @"|" + Hush + " if you know whats good for you" +
            @"|(youll|you will) " + Pays + " if you do" +
            @"|(youll|you will) " + Pays + " if you (tell( (anyone|anybody|a soul|rita|the police|the coppers|them))?|say (a word|anything)|grass|open (your|ya) (mouth|gob|trap))" + Whom +
            @")( (mate|love|pal|then|understand|understood|right|got it|ok|okay|alright|all right|remember that|mind|yeah|eh|im not joking|i am not joking|im not kidding|i mean it|and i mean it))*( (rita|ron|darren|sheila|ada|june|hal|joey|love|mate|pal|son|pet|darling|sunshine|missus|sir))? $");
        // A sentence that says nothing of its own beside a threat or an ask
        // ("Please.", "I mean it.", "Understand?").
        static readonly Regex Filler = new Regex(
            @"^ ((please|thanks|thank you|cheers|ta|sheila|love|mate|pal|eh|yeah|yes|ok|okay|right|alright|all right|go on|for me|will you|would you|can you|could you|i mean it|i mean that|and i mean it|understand|understood|got it|remember that|between us|between ourselves|just this once|for mickeys sake|for old times sake|thats all|thats all im saying|im asking you|im asking nicely|im telling you|im not joking|i am not joking|look|listen|now|then|mind)( |$))+$");
        static bool IsFiller(string sentence) => Filler.IsMatch(Words(sentence));
        // A clause that is only a word of address ("..., Darren."), never a
        // word that begins a condition or a menace.
        static readonly Regex AddressOnly = new Regex(@"^ (?!(else|otherwise|or|and|if|unless|cos|because) )[a-z]+ $");

        // A question only when it ends in a tag ("..., understand?").
        static readonly Regex TagEnd = new Regex(@" (understand|understood|right|got it|ok|okay|alright|all right|yeah|eh) $");
        // Anywhere in the line: taken back, a joke, or somebody else's words.
        static readonly Regex NotThreat = new Regex(
            @" ((?<!not |im not |i am not )(joking|kidding)|ha|hah|haha|hehe|lol|jk|yeah right|apparently|allegedly|supposedly|so they say|so i hear|or so|as if|having you on|pulling your leg|winding you up|only messing|just messing|messing about|ha ha|haha|i dont mean (it|that)|dont mean it|not really" +
            @"|(?!i )[a-z]+ (said|says|used to say|would say|told me|tells me|reckons|always said)) ");

        /// Whether a line of his threatens them to keep quiet (town list 6cd):
        /// some sentence of it is a plain threat and the words round one
        /// ("Say a word and you'll regret it.", "Keep your mouth shut or else.",
        /// "Not a word to Rita, if you know what's good for you.", "I know where
        /// you live."), and nothing in the line takes it back or quotes it.
        public static bool Threatens(string said)
        {
            // "..., not!" at the end takes it back.
            if (string.IsNullOrWhiteSpace(said) || NotThreat.IsMatch(Words(said)) || Words(said).EndsWith(" not ")) return false;
            // A smiley, or the whole line in quotation marks: not his own threat.
            var trimmed = said.Trim();
            // A smiley, an emoji, a laugh, or quotation marks anywhere: not his
            // own plain threat (the fourth review: "…, ha!", "lol", "😉",
            // "\"Say a word…\" - Mickey").
            if (Regex.IsMatch(said, @"[:;=]'?-?[\)\(\]\[dDpP><3*]|\([:;]|\^_?\^|<3|(^|[\s.!?,])[xX][dD]\b|[\uD800-\uDBFF]|[\u2600-\u27BF]|[""\u201c\u201d]")
                || (trimmed.Length > 1 && "'\u2018".IndexOf(trimmed[0]) >= 0 && "'\u2019".IndexOf(trimmed[trimmed.Length - 1]) >= 0)) return false;
            // Every sentence the threat or the words round it: anything else
            // beside it (a joke, a quotation, an explanation, "sorry, I didn't
            // mean that") makes it no plain threat (the second review).
            bool any = false;
            foreach (var sentence in Sentences(said))
            {
                var w = Words(sentence);
                bool threat = (!sentence.Contains("?") || TagEnd.IsMatch(w)) && ThreatSentence.IsMatch(w);
                if (threat) any = true;
                else if (!IsFiller(sentence) && !OwnsUp(sentence) && !IsAskSentence(sentence)) return false;
            }
            return any;
        }

        /// The street's story of it, and how it is told.
        public const string ThreatPrefix = "player.threat_";
        public const string ThreatSaid = "The new owner has been threatening people to keep them quiet";
        /// What the one he threatened remembers of it.
        public const string ThreatMemory = "The new owner threatened me to my face, to keep me quiet.";
        public static bool IsThreat(Rumor r) =>
            r != null && r.Content != null && r.Content.Subject == "player" && r.TopicKey != null && r.TopicKey.StartsWith(ThreatPrefix, System.StringComparison.Ordinal);

        /// THE THREAT, FILED (town list 6cd): the one he threatened holds it
        /// first-hand, as a story about him that is not sensitive (nobody is
        /// ashamed to say they were threatened), under the deed it was about
        /// (player.threat_window_d1); once per deed and person. False when it
        /// could not be.
        public static bool FileThreat(GossipMill mill, string who, string deedTopic, GameTime at)
        {
            if (mill == null || string.IsNullOrEmpty(who) || string.IsNullOrEmpty(deedTopic) || !(mill.Get(who) is Gossiper g)) return false;
            string stem = deedTopic.StartsWith("player.", System.StringComparison.Ordinal) ? deedTopic.Substring("player.".Length) : deedTopic;
            var fact = new Fact("player", "threat_" + stem, "threatened");
            if (g.Rumors.Exists(r => r.TopicKey == ThreatPrefix + stem && r.Hops == 0)) return false;
            // Threatened to their face: remembered as that, never "I saw it myself" (B7).
            mill.WitnessRemembering(who, fact, ThreatSaid, false, at, ThreatMemory);
            return true;
        }

        /// Whether they keep it quiet when he asks. Never about a grave deed (a
        /// killing: canon's indelible, which no bribe or threat moves either).
        /// Mickey's own people, as he is the owner they work for; a friend only
        /// on first-name terms with him; anybody who says yes to anybody; nobody
        /// who keeps nothing quiet.
        public static bool Agrees(KeepsQuietFor who, bool firstNameTerms, bool grave)
        {
            if (grave) return false;
            switch (who)
            {
                case KeepsQuietFor.Owner: return true;
                case KeepsQuietFor.Friend: return firstNameTerms;
                case KeepsQuietFor.Anyone: return true;
                default: return false;
            }
        }

        /// A silence that breaks as easily as it was given: the game's gossip lets
        /// money or a threat from anybody else undo it.
        public static bool Fragile(KeepsQuietFor who) => who == KeepsQuietFor.Anyone;

        // Their own telling, from now on: not "did Mickey tell you?".
        static readonly Regex TellingWords = new Regex(
            @" (you (wont|will not|wouldnt|would not|dont|do not|arent going to|are not going to|going to)|youre (not )?going to|ya (wont|dont)) (tell|say|let on|breathe|mention|grass)" +
            @"| keep (it|this|that|quiet|mum|schtum|shtum|your mouth)| (dont|do not) (tell|say|let on|breathe|mention|go telling)" +
            @"| between us | secret | not a word | can i trust you | (who|will|would) you tell | grass ");

        /// Whether his line speaks of their keeping quiet from now on, so a bare
        /// "Not a word." in their answer is a promise of silence, not an answer to
        /// "did Mickey say anything?" or "did he tell you?" (the independent check).
        public static bool SpeaksOfTelling(string said) => !string.IsNullOrEmpty(said) && TellingWords.IsMatch(Words(said));

        /// The cast file's word for it: "owner", "anyone", "nobody", else a friend.
        public static KeepsQuietFor Parse(string word) =>
            word == "owner" ? KeepsQuietFor.Owner : word == "anyone" ? KeepsQuietFor.Anyone : word == "nobody" ? KeepsQuietFor.Nobody : KeepsQuietFor.Friend;
    }
}
