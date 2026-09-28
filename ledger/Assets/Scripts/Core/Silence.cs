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

        static readonly Regex AskShape = new Regex(
            @" (keep (it|this|that) (to yourself|quiet|under your hat|between us|between ourselves)" +
            @"|(dont|do not) (go )?(tell|telling|mention it to) (anyone|anybody|a soul|nobody|the police|the coppers|the law|the old bill|the bizzies)" +
            @"|keep quiet about (it|this|that)" +
            @"|(dont|do not) (say|breathe) (a word|anything|owt|nothing)" +
            @"|not a word to (anyone|anybody|a soul|nobody|[a-z]+)" +
            @"|keep (your|ya) (mouth|trap|gob) shut|keep (schtum|shtum|stum|mum)|mums the word" +
            @"|(this|it|that) stays between us|(can|could|will|would) you keep (it|this|that) (quiet|to yourself)|can you keep a secret" +
            @"|you (wont|will not) (tell|say anything to) (anyone|anybody|a soul|nobody)|(rather|prefer) you (kept|keep) (it|this|that) (to yourself|quiet)) ");
        // "Say nothing" is an ask only at the start of what he says.
        static readonly Regex AskAtStart = new Regex(@"^ (just |so )?say nothing ");
        // Not asking: money or a threat (other verbs), somebody else's words,
        // asking why they did not, or a turn of phrase.
        static readonly Regex NotAsking = new Regex(
            @" (or else|or youll|or ill|or youre next|youll regret|watch yourself|if you know whats good|if you want to keep|keep your teeth|see you right|worth your while|sort you out|quid|tenner|fiver|pounds|pay you|money|cash|heres" +
            @"|unless you want|nobody gets hurt|make it up to you|make it worth" +
            @"|did you|have you|why|couldnt you|didnt you|wouldnt you|shouldnt you|he said|she said|they said|told me to|told you to|a word of a lie|a word of truth" +
            @"|a word to say|just listen|hear me out|in here|said|used to say|(anyone|anybody) (where|what|who|how|when|why)) ");

        /// Whether a line of his asks them to keep the matter quiet: "Keep it to
        /// yourself.", "Can you keep this quiet?", "Don't tell anyone.", "Not a
        /// word to Rita, eh?"; never with money or a threat in the same sentence,
        /// nor asking why they did not.
        public static bool AsksQuiet(string said)
        {
            foreach (var sentence in Sentences(said))
            {
                var w = Words(sentence);
                if ((AskShape.IsMatch(w) || AskAtStart.IsMatch(w)) && !NotAsking.IsMatch(w)) return true;
            }
            return false;
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
