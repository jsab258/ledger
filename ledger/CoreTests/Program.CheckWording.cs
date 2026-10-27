using System;
using Ledger.Core;

namespace Ledger.CoreTests
{
    /// THE CHECK'S WORDING (his note of 26 October: keep working on why Haiku refuses true sentences). Each switch that
    /// changes what the check is told gets its checks here; what it lets through is measured on the held test, not here.
    static partial class Program
    {
        /// EACH DETAIL A WHOLE STATEMENT (ClaimCheck.WholeDetails): the list is told to write each detail with its
        /// subject and to keep to what the line says, only when the switch is on; off, its prompt is as before.
        static void TestWholeDetails()
        {
            Console.WriteLine("Each detail a whole statement (ClaimCheck.WholeDetails):");
            bool was = ClaimCheck.WholeDetails;
            try
            {
                const string known = "H1: Mickey died three weeks ago.\n";
                ClaimCheck.WholeDetails = false;
                var off = ClaimCheck.RequestItems("m", known, "Three weeks ago, love.", "seal0001").System;
                ClaimCheck.WholeDetails = true;
                var on = ClaimCheck.RequestItems("m", known, "Three weeks ago, love.", "seal0001").System;
                Check(!off.Contains("whole statement"), "off, the list's instructions are as before");
                Check(on.Contains("whole statement") && on.Contains("\"Mickey died three weeks ago\", not \"three weeks ago\""),
                      "on, the list is told to write each detail whole, with who or what it is about");
                Check(on.Contains("naming someone is not saying where they are"), "and to keep to what the line says");
                Check(on.Replace(on.Substring(on.IndexOf("Write each specific as a whole statement", StringComparison.Ordinal),
                                              on.IndexOf("Examples, with M1", StringComparison.Ordinal) - on.IndexOf("Write each specific as a whole statement", StringComparison.Ordinal)), "") == off,
                      "and nothing else in its instructions changes");
            }
            finally { ClaimCheck.WholeDetails = was; }
        }
    }
}
