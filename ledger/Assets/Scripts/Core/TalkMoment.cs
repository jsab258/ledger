namespace Ledger.Core
{
    /// The kind of moment a line of talk is.
    public enum TalkKind
    {
        /// A greeting, a passing word, chat: the lighter model.
        SmallTalk,
        /// Real conversation: the better model.
        Conversation,
    }

    /// THE MODEL FOLLOWS THE KIND OF MOMENT, NEVER WHO IS TALKING (Jafar's ruling
    /// D48, again on 1 October: "everyone talks through the same model for the
    /// same kind of moment, small talk lighter and real conversation better,
    /// never by who the character is"; the rulings sweep of 1 October, item 11:
    /// each card's tier chose it, Ron and Darren lighter, Sheila better).
    public static class TalkMoment
    {
        /// Real conversation when the game says so; else when a deed or evidence
        /// comes with the line, or a deal is standing (Ron's ask, Sheila's week's
        /// question, either's plain question), or the line is one of a newcomer's
        /// real questions about the place (TalkRules); else small talk. What the
        /// game says ("moment": "smalltalk" | "conversation") wins.
        public static TalkKind Of(string said, bool deedOrEvidence = false, bool dealStanding = false, string gameSays = null)
        {
            if (gameSays == "conversation") return TalkKind.Conversation;
            if (gameSays == "smalltalk") return TalkKind.SmallTalk;
            if (deedOrEvidence || dealStanding) return TalkKind.Conversation;
            if (TalkRules.ConceptOf(said) != null) return TalkKind.Conversation;
            return TalkKind.SmallTalk;
        }

        /// The model for that kind of moment, the same for everybody.
        public static string ModelFor(TalkKind kind) => kind == TalkKind.Conversation ? Models.Core : Models.Ambient;
    }
}
