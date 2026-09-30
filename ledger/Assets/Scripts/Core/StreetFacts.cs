using System.Collections.Generic;

namespace Ledger.Core
{
    /// WHAT THE STREET KNOWS THAT NOBODY HAD WRITTEN (town list ck; decided 29
    /// September, DECISIONS). Asked a newcomer's twenty first questions,
    /// Sheila, Ron and Darren answered 38 of 60 with "that's all I know", for
    /// want of plain facts: the door Sheila does not open, the funeral, what
    /// Mickey left, where Tom sleeps, the drivers, the trade, where to eat.
    /// Written from canon and the story outline (Mickey dead three weeks; the
    /// letter; the funeral he missed; June back for it, wanting nothing; the
    /// dispatcher and the two drivers of the cast; the parade and the shops
    /// across from its north half; the office's hours), and given to every
    /// talking character as things they know. Never his name: the street
    /// learns that by the ladder (PlayerIdentity). How Mickey died and the
    /// warehouse fire as the street has it, as Jafar ruled on 30 September; never
    /// the fire's truth, and never why the docks went (the outline keeps that
    /// "underneath, never explained"). The person a fact is about knows it in
    /// their own words.
    public static class StreetFacts
    {
        /// (whom it is about, or "", the street's words, their own words).
        public static readonly (string about, string fact, string own)[] All =
        {
            ("", "Mickey died three weeks before the new owner, his nephew, came to Quay Street.", null),
            // How Mickey died (Jafar, 30 September): his heart; nobody thinks otherwise.
            ("rocco", "Mickey died of his heart, at the office early one morning; Ron found him when he came on at the rank, and the doctor said it was his heart.",
                      "I found Mickey at the office early one morning, when I came on at the rank; the doctor said it was his heart."),
            // The warehouse fire as the street has it (Jafar, 30 September); the truth is never the street's.
            ("", "Last November, on a Saturday night, the importer's warehouse at the far end of the old warehouse row burned down; the evening paper called it arson, since it started in two places, but nobody was charged, and the street says the owner had it done for the insurance.", null),
            ("", "Mickey left the office, Mickey's, the cab office on Quay Street, to his nephew, the new owner, by his will; the new owner came with one suitcase and a letter saying so.", null),
            ("", "Mickey's funeral was at Father Walsh's chapel, before the new owner came; he missed it.", null),
            ("june", "June, Mickey's daughter, came back to the Hook for the funeral and is still in town; she wants nothing from the office.",
                     "I came back to the Hook for my father's funeral and I am still in town; I want nothing from the office."),
            ("", "The new owner is living in Mickey's flat over the office.", null),
            ("lena", "The door at the back of Mickey's that Sheila does not open is Mickey's own room; it has been locked since he died, and Sheila keeps the key.",
                     "The door at the back of the office that I do not open is Mickey's own room; it has been locked since he died, and I keep the key."),
            ("", "Mickey's has two cab drivers on the rank, one by day and one by night, and a dispatcher on the radio and the phone.", null),
            ("", "The cab office opens at seven in the morning, nine on Sundays, and runs until the night driver goes home at three.", null),
            ("", "Mickey's has not made much money since the docks went; trade has been thin.", null),
            ("", "The cafe is across the street, in the shops opposite the north end of the parade; it opens at half past six and shuts at ten at night, and on Sundays it is open only from eight till twelve.", null),
        };

        /// Gives a card the street's facts for this person, once each.
        public static CharacterCard AddTo(CharacterCard card, string who)
        {
            if (card == null) return null;
            foreach (var fact in For(who))
                if (!card.HardFacts.Contains(fact)) card.HardFacts.Add(fact);
            return card;
        }

        /// What this person knows of them (a cast id; the facts about
        /// somebody else in the street's words, their own in theirs).
        public static List<string> For(string who)
        {
            var list = new List<string>();
            foreach (var (about, fact, own) in All)
            {
                if (about.Length > 0 && about == who) { if (own != null) list.Add(own); }
                else list.Add(fact);
            }
            return list;
        }
    }
}
