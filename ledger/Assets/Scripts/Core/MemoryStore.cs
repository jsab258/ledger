using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace Ledger.Core
{
    public class MemoryEvent
    {
        public GameTime Time;
        public string Kind;       // conversation | observation | heard | reflection
        public double Importance; // 0..1
        public string Text;

        public MemoryEvent(GameTime time, string kind, double importance, string text)
        {
            Time = time;
            Kind = kind;
            Importance = Math.Clamp(importance, 0.0, 1.0);
            Text = text.Replace("\n", " ").Trim();
        }

        public string ToLine() =>
            $"- [{Time}] ({Importance.ToString("0.00", System.Globalization.CultureInfo.InvariantCulture)}|{Kind}) {Text}";

        public static MemoryEvent FromLine(string line)
        {
            // - [D3 14:05] (0.80|conversation) text...
            var t = line.Trim();
            if (!t.StartsWith("- [")) return null;
            int closeBracket = t.IndexOf(']');
            if (closeBracket < 0) return null;
            if (!GameTime.TryParse(t.Substring(3, closeBracket - 3), out var time)) return null;

            int openParen = t.IndexOf('(', closeBracket);
            if (openParen < 0) return null;
            // Search for the closing paren AFTER the opening one. A ')' that appears
            // earlier (e.g. a hand-edited ":)" before the metadata) must not be picked
            // up, or the Substring length goes negative and throws — aborting the whole
            // memory load over one malformed line. Return null instead: skip the line.
            int closeParen = t.IndexOf(')', openParen);
            if (closeParen < 0) return null;
            var meta = t.Substring(openParen + 1, closeParen - openParen - 1).Split('|');
            if (meta.Length != 2) return null;
            if (!double.TryParse(meta[0], System.Globalization.NumberStyles.Float,
                    System.Globalization.CultureInfo.InvariantCulture, out var importance)) return null;

            return new MemoryEvent(time, meta[1], importance, t.Substring(closeParen + 1).Trim());
        }
    }

    /// One character's persistent memory: an append-only event stream plus a small
    /// set of distilled beliefs (produced by reflection). Stored as human-readable
    /// markdown so memories can be inspected, debugged, and hand-edited.
    ///
    /// NOTHING IS EVER WIPED. `canon.md` line 99 and pillar 1: permanent per-NPC
    /// memory, remediation is behavioral. A 600-event cap stood here from the
    /// 2026-07-27 audit until Jafar ruled queue 115 on 2026-09-14, "canon
    /// stands, the code changes ... nothing is ever wiped", and it was not
    /// theoretical: at 2800 game-days, the horizon `BalanceLab` already drives,
    /// six of the soak's seven agents sat pinned between 500 and 600 events with
    /// everything else dropped, and the soak's own memory series read as a world
    /// that had gone quiet rather than as a store that was deleting.
    ///
    /// REMOVING THE CAP ALSO REMOVED THE ONLY O(n) WRITE ON THIS PATH. A prune
    /// changed the list's structure and so rewrote the whole markdown file; now
    /// every remembered hour is the O(1) file append below, for every hour of a
    /// campaign, which is what the 2026-07-27 audit actually wanted.
    ///
    /// WHAT PERMANENCE COSTS is `BytesPerEvent` and `ProjectedBytes`, measured
    /// rather than argued, and `ledger/Soak` prints both every commit.
    public class MemoryStore
    {
        public string CharacterId { get; }
        public List<string> Beliefs { get; } = new List<string>();
        public List<MemoryEvent> Events { get; } = new List<MemoryEvent>();

        readonly string _filePath; // null => in-memory only (tests)

        public MemoryStore(string characterId, string filePath = null)
        {
            CharacterId = characterId;
            _filePath = filePath;
            if (_filePath != null && File.Exists(_filePath)) LoadFrom(File.ReadAllText(_filePath));
        }

        public void Append(MemoryEvent e)
        {
            Events.Add(e);
            if (!AppendToFile(e)) Save();
        }

        /// What one remembered hour costs in RAM, AT WORST, and at worst because
        /// it assumes no two events share a string, and the game does share
        /// summaries between gossipers, so a real store costs less than this.
        ///
        /// MEASURED, .NET 8 x64, GC.GetTotalMemory(true) delta between 50,000
        /// and 100,000 retained events so the list's own fixed cost cancels
        /// and what is left is the cost of ONE MORE event. The series, with a
        /// 12-character Kind beside each text length:
        ///
        ///     textChars   0    20    40    60    80   120
        ///     bytes     112   176   216   256   296   376
        ///
        /// which is exactly EventObjectBytes + a string each for Kind and
        /// Text. The 0 row allocates no text string at all because
        /// `new string(c, 0)` is String.Empty, shared; that is why
        /// StringBytes returns 0 there rather than a header.
        ///
        /// UNITY IS NOT .NET 8. IL2CPP's object header and allocator differ,
        /// so treat this as the desktop figure it was taken on; the soak
        /// prints it beside the projection every run so a port that changes
        /// it changes the printed number rather than an assumption.
        public static int BytesPerEvent(int textChars, int kindChars) =>
            EventObjectBytes + StringBytes(kindChars) + StringBytes(textChars);

        /// 56 for the object (16 header + 16 GameTime padded + 8 Kind ref +
        /// 8 Importance + 8 Text ref) and 8 for the slot in Events.
        const int EventObjectBytes = 64;

        /// A .NET string is a 16-byte header, a 4-byte length, the chars and a
        /// two-byte terminator, rounded up to the 8-byte allocation quantum.
        static int StringBytes(int chars) =>
            chars <= 0 ? 0 : (22 + 2 * chars + 7) / 8 * 8;

        /// Bytes the whole town's permanent memory holds after `days` of play.
        /// Every argument is a denominator the caller has to name out loud,
        /// which is the point: the rate is the soft one (queue 116: the soak
        /// measures it on SEVEN agents, not on a town).
        public static double ProjectedBytes(int residents, int days,
                                            double eventsPerNpcPerDay, int bytesPerEvent) =>
            (double)residents * days * eventsPerNpcPerDay * bytesPerEvent;

        /// The INVERSE, and it is the honest direction. A projection inherits
        /// the uncertainty of a rate nobody has measured at town scale; the
        /// rate a given budget affords does not, so the finding can be stated
        /// as a headroom multiple over the rate that WAS measured.
        public static double AffordableEventsPerNpcPerDay(long bytes, int residents,
                                                          int days, int bytesPerEvent) =>
            bytes / ((double)residents * days * bytesPerEvent);

        /// D25: "a town of three to five hundred residents who all remember".
        /// Both, because Jafar asked for both.
        public const int TargetResidentsLow = 300;
        public const int TargetResidentsHigh = 500;

        /// 400 weeks, which is `BalanceLab.WeeksPerPolicy` and the longest
        /// horizon anything in this project actually drives. Not a guess at
        /// how long a campaign is: a horizon already being run.
        public const int LongCampaignDays = 400 * 7;

        /// A REFERENCE SCALE, NOT A BUDGET, and the distinction matters
        /// because nothing is gated on it. No memory budget is recorded for
        /// this project (`game-design/research/performance-budget.md` sets
        /// frame and VRAM figures and no system-RAM ceiling), so the headroom
        /// is expressed as "the rate one gibibyte would buy", a ratio against
        /// a measured rate, rather than as a pass or a fail.
        public const long ReferenceScaleBytes = 1024L * 1024L * 1024L;

        /// The town's memory bill as one verdict line, from a live run's own
        /// tally: `events` remembered across `agents` residents over `days`,
        /// and the `bytes` those events cost by BytesPerEvent.
        ///
        /// THE ARITHMETIC AND THE STRING ARE HERE AND NOT IN THE CALLER, and
        /// that is the standing rule of 25 Aug rather than a preference. The
        /// live caller is `SimDirector`, in a layer that does not compile in
        /// this container, so a formatter written there would ship UNRUN and
        /// an unrun formatter printing a plausible string is the quietest
        /// instrument fault there is. The caller supplies membership and live
        /// state; every division below is executed by CoreTests.
        ///
        /// A ZERO SHIPS ITS DENOMINATOR. No events, or no residents, or no
        /// days, and the line says `nothing-measured` in the places a number
        /// would have gone rather than printing a confident 0 that cannot be
        /// told apart from a town that remembers nothing.
        public static string BudgetLine(int events, long bytes, int agents, int days)
        {
            var inv = System.Globalization.CultureInfo.InvariantCulture;
            string head = "memEvents=" + events.ToString(inv)
                        + " memAgents=" + agents.ToString(inv)
                        + " memDays=" + days.ToString(inv);
            if (events <= 0 || agents <= 0 || days <= 0)
                return head + " memBytesPerEvent=nothing-measured memKb=nothing-measured"
                           + " memPerNpcPerDay=nothing-measured memTownMb=nothing-measured"
                           + " memHeadroomX=nothing-measured";

            int bytesPerEvent = (int)(bytes / events);
            double rate = events / (double)agents / days;
            double lowMb = ProjectedBytes(TargetResidentsLow, LongCampaignDays, rate, bytesPerEvent)
                           / (1024.0 * 1024.0);
            double highMb = ProjectedBytes(TargetResidentsHigh, LongCampaignDays, rate, bytesPerEvent)
                            / (1024.0 * 1024.0);
            double affords = AffordableEventsPerNpcPerDay(
                                 ReferenceScaleBytes, TargetResidentsLow, LongCampaignDays, bytesPerEvent);
            // NO SPACES IN A VALUE: every reader of these lines splits on
            // whitespace, so the structure goes in with '/' and '..'.
            return head
                 + " memBytesPerEvent=" + bytesPerEvent.ToString(inv)
                 + " memKb=" + (bytes / 1024).ToString(inv)
                 + " memPerNpcPerDay=" + rate.ToString("0.000", inv)
                 + " memTownMb=" + TargetResidentsLow.ToString(inv) + "res/"
                 + LongCampaignDays.ToString(inv) + "d/" + lowMb.ToString("0", inv) + "MB.."
                 + TargetResidentsHigh.ToString(inv) + "res/"
                 + LongCampaignDays.ToString(inv) + "d/" + highMb.ToString("0", inv) + "MB"
                 + " memHeadroomX=" + (affords / rate).ToString("0.0", inv);
        }

        /// Events are the file's last section, so a new one can ride an O(1)
        /// file append instead of rewriting the whole markdown — the rewrite
        /// made every remembered hour cost all the hours before it (audit
        /// 2026-07-27). Returns false when a full save is needed instead.
        bool AppendToFile(MemoryEvent e)
        {
            if (_filePath == null) return true;      // in-memory store: nothing to write
            if (!File.Exists(_filePath)) return false;
            try { File.AppendAllText(_filePath, e.ToLine() + "\n"); return true; }
            catch { return false; }
        }

        public void ReplaceBeliefs(IEnumerable<string> beliefs)
        {
            Beliefs.Clear();
            foreach (var b in beliefs)
            {
                var t = b.Trim().TrimStart('-', ' ');
                if (t.Length > 0) Beliefs.Add(t);
            }
            Save();
        }

        public List<MemoryEvent> EventsOnDay(int day) =>
            Events.FindAll(e => e.Time.Day == day);

        public void LoadFrom(string markdown)
        {
            Beliefs.Clear();
            Events.Clear();
            string section = null;
            foreach (var raw in markdown.Replace("\r\n", "\n").Split('\n'))
            {
                if (raw.StartsWith("## ")) { section = raw.Substring(3).Trim(); continue; }
                if (section == "Beliefs")
                {
                    var t = raw.Trim();
                    if (t.StartsWith("- ")) Beliefs.Add(t.Substring(2).Trim());
                }
                else if (section == "Events")
                {
                    var e = MemoryEvent.FromLine(raw);
                    if (e != null) Events.Add(e);
                }
            }
        }

        public string ToMarkdown()
        {
            var sb = new StringBuilder();
            sb.AppendLine($"# Memory: {CharacterId}");
            sb.AppendLine();
            sb.AppendLine("## Beliefs");
            foreach (var b in Beliefs) sb.AppendLine($"- {b}");
            sb.AppendLine();
            sb.AppendLine("## Events");
            foreach (var e in Events) sb.AppendLine(e.ToLine());
            return sb.ToString();
        }

        /// The last conversation event starting with `prefix` given new text,
        /// and the file rewritten (26 September: what a character keeps of its
        /// own reply is put right to what the player actually heard).
        public void CorrectLast(string prefix, string text)
        {
            for (int i = Events.Count - 1; i >= 0; i--)
            {
                var e = Events[i];
                if (e.Kind != "conversation" || !e.Text.StartsWith(prefix, StringComparison.Ordinal)) continue;
                Events[i] = new MemoryEvent(e.Time, e.Kind, e.Importance, text);
                Save();
                return;
            }
        }

        void Save()
        {
            if (_filePath == null) return;
            var dir = Path.GetDirectoryName(_filePath);
            if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);
            File.WriteAllText(_filePath, ToMarkdown());
        }
    }
}
