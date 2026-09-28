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

        public const string Text =
            "The people of this town answer you in words written as you play by an AI model. " +
            "It is told only what each of them has seen, heard and believes, and each line is checked against that " +
            "before you hear it, but it can still get things wrong. " +
            "If a line is wrong, hurtful or breaks the game, report it: that line, what you said just before it " +
            "and your note go to the developers, and nothing else does.";

        public const string ReportLabel = "Report this line";

        /// What the player is told once a report has gone (the helper says where).
        public static string ReportThanks(string saved) =>
            saved == "relay" ? "Thank you. It has gone to the developers."
            : saved == "local" ? "Thank you. It is kept on this computer for the developers."
            : "Sorry, it could not be kept. Please try again.";
    }
}
