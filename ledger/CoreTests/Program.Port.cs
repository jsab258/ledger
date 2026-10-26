using System;
using Ledger.Core;

namespace Ledger.CoreTests
{
    /// THE PORT'S RULES GIVEN THEIR HOME IN THE CORE (phase 3's port, his fallback work of 25 October).
    /// The 5 October sweep (production/audits/sweep-2026-10-05/port-vs-core.md, 1a) found five rules
    /// living only in the game's C++, with no C# source for the port to agree with. Each moved here
    /// gets its checks in this file, and its golden rows in ledger/PerceptionGolden.
    static partial class Program
    {
        /// G2, HOW WELL A WITNESS KNOWS HIS FACE FROM MEETINGS (the review's A4, 1 October): a stranger
        /// until met face to face; recognisable from the first meeting; a little more each further day
        /// met, to a cap below Close. It decides rung 4, so the report, the constable and the arrest.
        static void TestFamiliarityFromMeetings()
        {
            Console.WriteLine("Familiarity from meetings (the sweep's G2):");

            Check(Acquaintance.FromMeetings(0) == Acquaintance.Stranger && !Acquaintance.CanNameYou(Acquaintance.FromMeetings(0)),
                  "never met: a stranger, who cannot name him");
            Check(Acquaintance.FromMeetings(-3) == Acquaintance.Stranger,
                  "a negative count is never met, not a negative familiarity");
            Check(Acquaintance.CanNameYou(Acquaintance.FromMeetings(1)) && Math.Abs(Acquaintance.FromMeetings(1) - 0.4) < 1e-12,
                  "the first meeting puts him over recognition, at 0.4",
                  $"{Acquaintance.FromMeetings(1)}");
            Check(Math.Abs(Acquaintance.FromMeetings(2) - Acquaintance.FromMeetings(1) - 0.1) < 1e-12,
                  "each further day met adds 0.1");
            Check(Math.Abs(Acquaintance.FromMeetings(4) - 0.7) < 1e-12 && Acquaintance.FromMeetings(40) == Acquaintance.FromMeetings(4),
                  "it stops at 0.7 from the fourth day",
                  $"{Acquaintance.FromMeetings(4)} / {Acquaintance.FromMeetings(40)}");
            Check(Acquaintance.FromMeetings(int.MaxValue) < Acquaintance.Close,
                  "meeting him, however often, is not walking with him: always below Close");
            Check(Acquaintance.HeardOfYou < Acquaintance.FromMeetings(1),
                  "one meeting knows him better than having heard of him");
        }
    }
}
