namespace Ledger.Core
{
    /// THE NOTICE THAT THE TOWN TALKS THROUGH AN AI (town list 6c, 28
    /// September). The EU's AI Act, Article 50, applying since 2 August 2026:
    /// people must be told they are interacting with an AI system at the latest
    /// at their first interaction. Steam, Microsoft and PEGI want a way to
    /// report what it says (production/research/runtime-ai-business/notes/stores.md).
    /// Shown once before the first conversation and again from the menu; the
    /// words live here, and reach the game in the talk helper's ready message,
    /// so the game and the store page say the same thing.
    public static class AiNotice
    {
        public const string Title = "Before you talk to anyone";

        /// THE NOTICE, true to how this copy talks (town list 6w, 28 September;
        /// production/research/player-data-notice/NOTE-2026-09-28.md): through
        /// our relay, or straight to the provider as in Jafar's own copy. It
        /// names where the words go and what is kept, as the GDPR and the Swiss
        /// FADP want at the point of collection. Anthropic's commercial terms as
        /// read on 28 September 2026: deleted within 30 days, longer only if its
        /// safety checks flag them or the law requires it, and not used for
        /// training. The fuller privacy notice it should link to does not exist
        /// yet (a decision for Jafar); until it does, no link is promised.
        public static string TextFor(bool throughRelay) =>
            "The people of this town answer you in words written as you play by an AI model. " +
            "It is told only what each of them has seen, heard and believes, and each line is checked against that " +
            "before you hear it, but it can still get things wrong. " +
            (throughRelay
                ? "What you type is sent through our server to Anthropic, the American company whose Claude model writes the replies. " +
                  "Our server keeps none of your words unless you report a line. "
                : "What you type is sent to Anthropic, the American company whose Claude model writes the replies. ") +
            "Anthropic deletes it within 30 days, or longer only if its safety checks flag it or the law requires it, " +
            "and does not train its models on it. " +
            "If a line is wrong, hurtful or breaks the game, report it: that line, what you said just before it " +
            "and your note " +
            (throughRelay ? "are kept for the developers, with a code for your copy of the game." : "are kept on this computer for the developers.");

        /// The notice for the copies friends and players get, which talk through the relay.
        public static readonly string Text = TextFor(true);

        public const string ReportLabel = "Report this line";

        /// WHEN THE TOWN'S LIVE TALK STOPS (town list 6t), what the player is
        /// told, plainly and not in any character's voice: why, and when it comes
        /// back. Null for any other failure, which stays a brush-off.
        public static string TalkPaused(string errorType, string until) =>
            errorType == "allowance_spent"
                ? "This copy has used its live talk " + (until == "next month" ? "for the month. It comes back at the start of next month." : "for today. It comes back tomorrow.")
                  + " Until then people answer in a few words of their own."
            : errorType == "relay_stopped"
                ? "Live talk is paused for everyone for the rest of the month. Until it is back, people answer in a few words of their own."
            : errorType == "too_busy"
                ? "Too many lines at once. Give it a moment and try again."
            : errorType == "unknown_copy"
                ? "This copy cannot reach the town's talk. Check that the game is up to date, or tell the developers."
            : null;

        /// TALK THAT CANNOT BE REACHED (town list 6ax, the fourth sweep): every
        /// failure but the relay's four refusals used to become the character's
        /// brush-off with no word to the player (the relay unreachable, a bad
        /// key, a dropped connection), so a friend could not tell broken talk
        /// from a town that would not speak to him.
        public const string TalkUnreachable =
            "Live talk cannot be reached just now. Until it comes back, people answer in a few words of their own.";

        /// A copy with no way to talk at all (no key and no relay).
        public const string TalkOff =
            "Live talk is off in this copy. People answer in a few words of their own.";

        /// What the player is told once a report has gone (the helper says where).
        public static string ReportThanks(string saved) =>
            saved == "relay" ? "Thank you. It has gone to the developers."
            : saved == "local" ? "Thank you. It is kept on this computer for the developers."
            : "Sorry, it could not be kept. Please try again.";
    }
}
