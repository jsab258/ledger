using System;
using System.Collections.Generic;

namespace Ledger.Core
{
    /// M15.1 — THE CITY BECOMES AUDIBLE.
    ///
    /// The gossip mill has always known who is telling whom what about you.
    /// Until now the player's only way to find out was a row in a panel:
    /// `ReportOverheard` detected two people trading a rumour six metres away
    /// and answered by updating a ledger. Two people were discussing the
    /// warehouse fire in front of him and the game said nothing out loud.
    ///
    /// This turns that state into SPEECH. Every line here is causally true —
    /// it exists because a specific person heard a specific thing from a
    /// specific source — which is the thing recorded barks cannot do and the
    /// whole reason this game has a gossip network under it.
    ///
    /// DELIBERATELY NOT LLM-GENERATED (yet). Lines are selected from real
    /// state, so they are free, deterministic, testable in CI, and they still
    /// work with no API key — the world stays audible even when it cannot
    /// think. The LLM's job is to make this ELOQUENT later, per-cast-member;
    /// its job is not to make it exist.
    public enum StanceKind
    {
        /// You are a person in the street like any other.
        Indifferent = 0,
        /// They clock you. A look, no more.
        Notices = 1,
        /// The look lasts. They keep you in view while you are in it.
        Watches = 2,
        /// They say something — to you, or pointedly near you.
        Comments = 3,
        /// They would rather be elsewhere, and go there.
        Avoids = 4,
        /// They will not deal with you. The door does not open.
        Refuses = 5,
        /// They come to you about it.
        Confronts = 6,
    }

    /// One thing somebody says out loud, with the state that justifies it.
    public class SpokenLine
    {
        public string SpeakerId;
        public string Text;
        /// The bank the line was taken from, for RemarkLedger.Heard (town list 6k).
        public string Bank;
        /// A composed telling's wording, the story taken out, fixed when the line
        /// is made, so the story being retold before he hears it cannot change
        /// what the ledger keeps (town list 6o); null for any other line.
        public string Wording;
        /// True when this is about the player — those carry a lead if heard.
        public bool AboutPlayer;
        /// The rumour behind it, when there is one. The player who overhears
        /// this learns exactly this, which is why hearing is knowing.
        public Rumor Source;
        /// TRUE WHEN THE WORDS WERE ASSEMBLED AT RUN TIME, so no recording of
        /// them can exist and none ever will.
        ///
        /// `VoiceBank.ClipName` keys a clip by (voice, EXACT text). A line
        /// built as template-plus-`{what}` is therefore a different clip for
        /// every rumour the street has ever carried, and the summaries are
        /// themselves composed — "someone in a runner's coat — maybe Sam —
        /// was handling a package past midnight, on Copper Row". That space
        /// is unbounded, so it is not a bank that is behind: it is a bank
        /// that cannot be written.
        ///
        /// It matters because `speechNoClip` was being read as a rendering
        /// backlog. Measured on the bank as shipped: the 42 `exchange.tell.*`
        /// lines of 336 atomic ones are all instantiated with ONE specimen
        /// rumour ("the new owner was at the warehouse on Tuesday"), which is
        /// one point in that space, so their 252 rendered clips can only ever
        /// play for a rumour that says exactly that sentence. Only `Exchange`
        /// composes; `Recognition` and `Ambient` are literal throughout —
        /// checked, zero interpolations between them — and are bankable.
        public bool Composed;
    }

    /// WHO HAS ALREADY REMARKED TO THE PLAYER ON WHICH STORY, decision 7 (a),
    /// 23 September: a story that shows is remarked on once, then only
    /// watched. In Core so the rule is tested here and the game and the study
    /// harness keep it the same way. A remark counts only when it was the
    /// story's own - said at Comments, the floor's rung, not a "Door's shut."
    /// from further up the ladder - and HEARD: the game says a line at the far
    /// edge of its 7 m range, where the player often cannot make out the
    /// words, and an unheard remark must not use up the only one. The key
    /// carries the story's value as well as its topic, so informing on one
    /// person and on another are two stories.
    public sealed class RemarkLedger
    {
        readonly HashSet<string> _said = new HashSet<string>();

        public static string KeyFor(string personId, Rumor r) =>
            r == null || r.Content == null ? null
            : (personId ?? "") + "|" + r.Content.Subject + "." + r.Content.Predicate + "=" + (r.Content.Value ?? "");

        public bool HasRemarked(string personId, Rumor r)
        {
            var k = KeyFor(personId, r);
            return k != null && _said.Contains(k);
        }

        /// True when this remark is now recorded.
        public bool Record(string personId, Rumor r, StanceKind saidAt, bool heard)
        {
            if (!heard || saidAt != StanceKind.Comments) return false;
            var k = KeyFor(personId, r);
            return k != null && _said.Add(k);
        }

        /// A HALF-REMEMBERED STORY'S ONE REMARK (StreetVoice.FaintRemark),
        /// 28 September. Heard, or it does not count. The key is the story's, so
        /// a story remarked on faintly is not remarked on again if it comes
        /// back strong, and one remarked on strongly is not remarked on again
        /// as it fades: one remark per person per story, whichever came first.
        public bool RecordFaint(string personId, Rumor r, bool heard)
        {
            if (!heard) return false;
            var k = KeyFor(personId, r);
            return k != null && _said.Add(k);
        }

        public int Count => _said.Count;

        // THE LINES HE HAS HEARD, bank by bank, and when (town list 6k).
        readonly Dictionary<string, Dictionary<string, int>> _linesHeard = new Dictionary<string, Dictionary<string, int>>();
        int _hearings;

        /// A LINE FROM A BANK THAT HE HAS NOT HEARD LATELY (town list 6k,
        /// ROADMAP stage 6, "hours of content without repetition"): one he has
        /// never heard, the seed choosing where to start, or, once he has heard
        /// them all, the one heard longest ago. Chance alone repeats itself: five
        /// remarks drawn at random from fourteen repeat one more often than not.
        public string Fresh(string bank, string[] lines, int seed)
        {
            if (lines == null || lines.Length == 0) return "";
            _linesHeard.TryGetValue(bank ?? "", out var heard);
            int n = lines.Length, start = ((seed % n) + n) % n;
            string oldest = null;
            int oldestAt = int.MaxValue;
            for (int k = 0; k < n; k++)
            {
                var line = lines[(start + k) % n];
                if (heard == null || !heard.TryGetValue(line, out var at)) return line;
                if (at < oldestAt) { oldestAt = at; oldest = line; }
            }
            return oldest;
        }

        /// He heard this line: remembered under its own bank, so the bank moves on.
        public void Heard(SpokenLine line)
        {
            if (line == null) return;
            HeardLine(line.Bank, StreetVoice.WordingOf(line));
            // A telling of the town's own news, counted by story (town list 6aq).
            if (line.Composed && line.Source?.Content != null && line.Source.Content.Subject == TownNews.Subject)
            {
                var key = line.Source.TopicKey;
                _storyTold[key] = TimesToldHim(key) + 1;
            }
        }

        /// How many tellings of a story of the town's own he has made out.
        public int TimesToldHim(string topicKey) => topicKey != null && _storyTold.TryGetValue(topicKey, out var n) ? n : 0;
        readonly Dictionary<string, int> _storyTold = new Dictionary<string, int>();

        /// He heard this line from this bank: remembered, so the bank moves on.
        /// Only what he heard counts, as for the remarks themselves.
        public void HeardLine(string bank, string line)
        {
            if (string.IsNullOrEmpty(line)) return;
            if (!_linesHeard.TryGetValue(bank ?? "", out var heard)) _linesHeard[bank ?? ""] = heard = new Dictionary<string, int>();
            heard[line] = ++_hearings;
        }

        /// THE LEDGER IN A SAVE (town list 6o): who has remarked on which story,
        /// and the lines he has heard, oldest first, so that after a reload
        /// nobody remarks again on a story they already remarked on (decision
        /// 7 (a)) and no bank starts over. Plain values, for any save's JSON:
        /// "said", the remark keys; "heard", [bank, line] pairs in the order heard.
        public Dictionary<string, object> ToJson()
        {
            var heard = new List<(int at, string bank, string line)>();
            foreach (var bank in _linesHeard)
                foreach (var kv in bank.Value) heard.Add((kv.Value, bank.Key, kv.Key));
            heard.Sort((x, y) => x.at.CompareTo(y.at));
            var said = new List<string>(_said);
            said.Sort(StringComparer.Ordinal);
            var saidOut = new List<object>();
            foreach (var s in said) saidOut.Add(s);
            var heardOut = new List<object>();
            foreach (var h in heard) heardOut.Add(new List<object> { h.bank, h.line });
            var told = new Dictionary<string, object>();
            foreach (var kv in _storyTold) told[kv.Key] = kv.Value;
            return new Dictionary<string, object> { { "said", saidOut }, { "heard", heardOut }, { "told", told } };
        }

        /// A ledger from ToJson's values. Whatever it cannot read, it skips: a
        /// damaged save loses remarks, never the game.
        public static RemarkLedger FromJson(Dictionary<string, object> saved)
        {
            var ledger = new RemarkLedger();
            if (saved == null) return ledger;
            if (saved.TryGetValue("said", out var said) && said is List<object> keys)
                foreach (var k in keys) if (k is string s && s.Length > 0) ledger._said.Add(s);
            if (saved.TryGetValue("heard", out var heard) && heard is List<object> pairs)
                foreach (var p in pairs)
                    if (p is List<object> pair && pair.Count == 2 && pair[0] is string bank && pair[1] is string line)
                        ledger.HeardLine(bank, line);
            if (saved.TryGetValue("told", out var told) && told is Dictionary<string, object> toldMap)
                foreach (var kv in toldMap)
                    if (kv.Value is double dv && dv >= 0) ledger._storyTold[kv.Key] = (int)dv;
                    else if (kv.Value is int iv && iv >= 0) ledger._storyTold[kv.Key] = iv;
            return ledger;
        }
    }

    /// HOW MUCH OF A STORY ABOUT THE PLAYER SOMEBODY HOLDS, for how it shows
    /// (Jafar's list, 28 September).
    public enum Knowing
    {
        /// Nothing about his night, or only what they were paid or scared off.
        Nothing = 0,
        /// A story of his night they would no longer pass on: fading, not gone.
        ALittle = 1,
        /// A story they would still pass on (StreetVoice.StoryThatShows).
        Enough = 2,
    }

    /// One person's bearing toward the player right now (StreetVoice.RegardFor).
    public sealed class Regard
    {
        public Knowing Knowing;
        /// The story behind it, or null.
        public Rumor Story;
        public StanceKind Stance;
        /// They can tell the man in front of them is the one their story is
        /// about (Acquaintance.CanNameYou). When false nothing they hold shows,
        /// and the game sends the conversation helper no "knowing".
        public bool KnowsItIsHim;
        /// Where the first look lands as he comes towards them, in metres.
        public double FirstLookMetres;
        /// How long it holds, in seconds; infinity while he is in range.
        public double FirstLookSeconds;
        /// Where a second, knowing look comes, in metres; 0 for none.
        public double SecondLookMetres;
        /// How long the second look holds, in seconds.
        public double SecondLookSeconds;
        /// Where their eyes drop as he comes close; 0 when they keep looking.
        public double LookAwayMetres;
        /// Whether they look back after he has passed.
        public bool LooksBack;
        /// They have already had their one say on this story.
        public bool RemarkedAlready;
        /// A line is due while he is in earshot.
        public bool Speaks;
        /// And it is a half-remembered one (FaintRemark), said to the companion
        /// beside them rather than to him, once he has gone past; not Recognition.
        public bool Faint;
    }

    public static class StreetVoice
    {
        // ---- the reaction ladder (M15.2) ----

        /// How somebody stands toward the player right now.
        ///
        /// Everything here already existed as numbers the player could only
        /// read in a panel. As a STANCE it becomes something they can watch
        /// happen: the room going quiet, a face turning away, a door not
        /// opening. That is the same information delivered by the world
        /// instead of by the interface.
        ///
        /// Loyalty pulls DOWN the ladder — a friend who has heard something
        /// bad about you asks you about it rather than crossing the street,
        /// which is what makes friendship mechanically worth having.
        public static StanceKind Stance(double suspicion, double loyalty,
            double strongestAboutPlayer, bool leashed, bool wearingCoat, bool knowsSomething = false,
            bool remarkedAlready = false, bool knowsALittle = false)
        {
            // A leash is a mouth held shut, not a mind changed: they still
            // watch, they simply do not speak.
            double pressure = Clamp01(0.55 * Clamp01(suspicion) + 0.45 * Clamp01(strongestAboutPlayer));
            // Somebody fond of you gives you the benefit of the doubt, right
            // up until it is unmistakable.
            pressure -= 0.35 * Clamp01(loyalty - 0.5) * 2.0 * (pressure < 0.85 ? 1.0 : 0.4);
            // The coat is deniability, and deniability buys distance from the
            // ladder — but only from people who are not already certain.
            if (wearingCoat && pressure < 0.7) pressure -= 0.12;
            pressure = Clamp01(pressure);

            var rung = Rung(pressure, leashed);
            // KNOWING SHOWS, Jafar's decision 7 (a), 23 September. A hearer
            // holds a retold story at 0.2 to 0.38, which the arithmetic above
            // turns into a pressure of 0.09 to 0.17 - a glance at most, the
            // same glance any passer-by gives - so the handful who had heard
            // were invisible. Ruled: "a hearer who knows even a little looks
            // at Tom longer, remarks on it, treats him differently", touching
            // no constant. So a person who holds a story that SHOWS (see
            // StoryThatShows: the player's night life, not bought or scared
            // quiet, still strong enough to pass on) stands on a floor under
            // the ladder rather than a number on it. ONCE PER STORY, THEN THE
            // LOOK (Jafar's option (a), recommended and carried while he
            // decides, 23 September): until they have remarked on it the
            // floor is Comments, the rung that says something; afterwards it
            // is Watches, the look that lasts and reaches furthest short of
            // avoiding him (GazeMetres 14 against Comments' 12) - so knowing
            // never shortens how far off they pick him out for long, and his
            // own staff do not remark every time he passes. Leashed, they
            // watch without a word; in the coat they only glance, unsure it
            // is him. A floor only - a stronger story or real suspicion climbs
            // past it as before - and only when the caller says so, so every
            // caller that does not ask gets the ladder exactly as it stood.
            if (knowsSomething)
            {
                var floor = wearingCoat ? StanceKind.Notices
                          : leashed || remarkedAlready ? StanceKind.Watches
                          : StanceKind.Comments;
                if (rung < floor) rung = floor;
            }
            // KNOWING A LITTLE SHOWS TOO (Jafar's list, 28 September: "someone
            // who has heard a little about Tom behaves exactly like someone who
            // has heard nothing"). A story below the share floor is one they
            // would no longer pass on, and the mill keeps it for about eleven
            // more days as it fades (Age drops it under 0.03). Through those
            // days its pressure is under 0.09 and the ladder above leaves them
            // Indifferent. So a half-remembered story is a floor of its own,
            // one rung under a story that shows: they notice him, and look
            // again, longer than a stranger would, as he passes (SecondLookMetres).
            // Leashed, a look is still allowed; in the coat, unsure it is him,
            // nothing.
            if (knowsALittle && !wearingCoat && rung < StanceKind.Notices) rung = StanceKind.Notices;
            return rung;
        }

        /// THE STORY A PERSON HOLDS THAT SHOWS IN HOW THEY TREAT THE PLAYER,
        /// or null: decision 7 (a)'s "knows even a little", made exact by what
        /// the mill already means. It is about the player and SENSITIVE (his
        /// night life - the crime - rather than the neighbourhood's vague talk,
        /// which reaches most of a district and would turn a handful into a
        /// crowd); it is not a topic they have been paid or scared into keeping
        /// quiet about (Gossiper.Suppressed, which the mill already honours when
        /// they talk); and it is still at or above the mill's own share floor,
        /// the certainty at which they would pass it on, so a story visibly
        /// cools out of their manner as it fades rather than lingering down to
        /// the tidy-up threshold. The floor is the caller's mill's
        /// MinConfidenceToShare, so no number is introduced here.
        public static Rumor StoryThatShows(Gossiper g, double shareFloor)
        {
            if (g == null) return null;
            Rumor best = null;
            foreach (var r in g.Rumors)
            {
                // His night, or what he did with the outfit's ask, which shows
                // though only the envelope handed over is a secret (town list 6z),
                // or the police asking after him (town list 6bq).
                if (r == null || r.Content == null || r.Content.Subject != "player" || !(r.Sensitive || Arrangement.IsNight(r) || PoliceFile.IsAsking(r))) continue;
                if (!r.Indelible && g.Suppressed.Contains(r.TopicKey)) continue;
                if (!(r.Confidence >= shareFloor)) continue;
                if (best == null || r.Confidence > best.Confidence) best = r;
            }
            return best;
        }

        /// THE STORY A PERSON STILL HOLDS BUT WOULD NO LONGER PASS ON, or null:
        /// the same kind of story as StoryThatShows (his night, not bought or
        /// scared quiet) held under the mill's share floor. The strongest of
        /// them. Whether a stronger story also shows is the caller's question
        /// (RegardFor asks StoryThatShows first).
        internal static Rumor StoryHalfRemembered(Gossiper g, double shareFloor)
        {
            if (g == null) return null;
            Rumor best = null;
            foreach (var r in g.Rumors)
            {
                // His night, or what he did with the outfit's ask, which shows
                // though only the envelope handed over is a secret (town list 6z);
                // not the police asking after him, which shows while it is news
                // and is then forgotten, with no faint remark (town list 6bq).
                if (r == null || r.Content == null || r.Content.Subject != "player" || !(r.Sensitive || Arrangement.IsNight(r))) continue;
                if (!r.Indelible && g.Suppressed.Contains(r.TopicKey)) continue;
                if (!(r.Confidence > 0.0) || r.Confidence >= shareFloor) continue;
                if (best == null || r.Confidence > best.Confidence) best = r;
            }
            return best;
        }

        /// WHETHER SOMEBODY WHO KNOWS A LITTLE SAYS SO, once: "may remark on
        /// it" (Jafar, 28 September). Some do and some do not, and the fainter
        /// the story the fewer: a person remarks when their own fixed draw,
        /// a stable hash of who they are and which story, falls under the
        /// story's confidence as a share of the floor. At the floor that is
        /// everybody; halfway down, half. No number is introduced: the floor
        /// is the mill's. The draw is fixed per person and story, so the same
        /// save gives the same street, and as the story fades the ones still
        /// minded to say something only ever get fewer.
        internal static bool MayRemarkFaintly(string personId, Rumor r, double shareFloor)
        {
            var k = RemarkLedger.KeyFor(personId, r);
            if (k == null || !(shareFloor > 0.0)) return false;
            return FaintDraw(k) < r.Confidence / shareFloor;
        }

        /// The fixed draw, 0 to 0.9999, from FNV-1a (ASCII keys, so the port's
        /// byte-wise Hash agrees).
        internal static double FaintDraw(string key) => (Hash(key) % 10000u) / 10000.0;

        // ---- the look itself (production/research/gaze-and-knowing, 28 September) ----
        //
        // What the street did before this: every head within 5 m turned to him
        // the same way, stranger or not. What people do (the research's
        // measured street studies): a stranger glances early, from about ten
        // metres, for about half a second, and has looked away by about 2.4 m.
        // Somebody who knows something glances the same way and then, as he
        // comes through the passing zone, looks again and holds it past the
        // one-second polite line, into close range. Somebody watching keeps
        // him in view from further off and looks back after he has passed.
        // The contrast is the point, so the stranger's glance is written down
        // here too. Every look turns the head: from a camera behind him, eyes
        // alone cannot be read. GazeMetres is the ladder's own number and is
        // left as it stood; the look reads it only for those who watch.

        /// WHERE THE FIRST LOOK LANDS as he comes towards them, in metres: the
        /// stranger's early glance for everybody, or further off for those the
        /// ladder has watching him.
        internal static double FirstLookMetres(StanceKind stance) =>
            Math.Max(CivilGlanceMetres, GazeMetres(stance));

        /// HOW LONG THE FIRST LOOK HOLDS, in seconds: a glance, except for
        /// those who watch him, who keep him in view for as long as he is in
        /// range (infinity: the game ends that look when he leaves it).
        internal static double LookHoldSeconds(StanceKind stance) =>
            stance == StanceKind.Watches || stance == StanceKind.Comments || stance == StanceKind.Confronts
                ? double.PositiveInfinity : CivilGlanceSeconds;

        /// WHERE THE SECOND LOOK COMES, in metres, or 0 for none: the knowing
        /// look of somebody who notices him, as he comes into the passing zone,
        /// held for KnowingLookSeconds.
        internal static double SecondLookMetres(StanceKind stance) =>
            stance == StanceKind.Notices ? PassingZoneMetres : 0.0;

        /// WHERE THE EYES GO ELSEWHERE as he comes close, in metres: a
        /// stranger's civil look away (and one who avoids or refuses him, who
        /// has no wish to be caught looking); 0 for everybody who knows
        /// something, who keeps looking as he passes.
        internal static double LookAwayMetres(StanceKind stance) =>
            stance <= StanceKind.Indifferent || stance == StanceKind.Avoids || stance == StanceKind.Refuses
                ? CivilLookAwayMetres : 0.0;

        /// WHETHER THEY LOOK BACK after he has passed: those who watch him.
        internal static bool LooksBack(StanceKind stance) =>
            stance == StanceKind.Watches || stance == StanceKind.Comments || stance == StanceKind.Confronts;

        /// Where a stranger's glance at a passer-by lands: the median measured
        /// look distance, 10.3 m (Fotios and others, Sheffield, 2015), rounded.
        public const double CivilGlanceMetres = 10.0;

        /// A stranger's glance: the median measured look, 0.48 s (Fotios and
        /// others, 2015), rounded.
        public const double CivilGlanceSeconds = 0.5;

        /// Where two passing people come closest to each other's notice: the
        /// passing zone, 3.0 to 3.7 m (Patterson and others, 2002), its near end.
        public const double PassingZoneMetres = 3.0;

        /// The knowing look: the top of the "intensified glance" still held at
        /// close range, 0.39 to 1.52 s (Arminen and Heino, 2023), past the
        /// one-second line where polite ends, short of the 3.3 s of comfortable
        /// eye contact (Binetti and others, 2016). From the passing zone at a
        /// walking pace it holds until he is about alongside them.
        public const double KnowingLookSeconds = 1.5;

        /// Where a stranger's eyes drop as somebody comes close: Goffman's
        /// eight feet (1963). What glance there is at close range starts at
        /// 2.5 to 3 m and is over in half a second (Arminen and Heino, 2023).
        public const double CivilLookAwayMetres = 2.4;

        /// HOW ONE PERSON TREATS THE PLAYER RIGHT NOW, in one call, so the game,
        /// the port and the tests cannot compose it three different ways.
        ///
        /// `familiarity` is how well they know him by sight (Acquaintance): a
        /// story shows only in somebody who can tell that the man in front of
        /// them is the one it is about. Somebody who has only heard of him
        /// cannot pick him out of a bus queue (Acquaintance.HeardOfYou), so
        /// whatever they hold, they treat him as the stranger he is to them
        /// (the independent check, 28 September: without this, gossip alone
        /// let the town recognise him). `companionNear` is whether somebody
        /// they could talk to is beside them: a half-remembered story is said
        /// about him to a companion, not to his face (the gaze research: faint
        /// knowledge is a word to a companion, and lines people say to each
        /// other read as natural where lines aimed at the player do not).
        /// `remarks` is the caller's record of who has had their say (may be
        /// null: nobody has).
        ///
        /// The caller says a line only when `Speaks` and the player is in
        /// earshot, and records it only if it was heard: Record for a story
        /// that shows, RecordFaint for a half-remembered one. A stance of
        /// Comments or above reached by suspicion alone speaks on the caller's
        /// own cooldown, as the ladder always has; the once-per-story rule is
        /// the floor's, so `Speaks` and `RemarkedAlready` can both be true.
        public static Regard RegardFor(Gossiper g, double shareFloor, bool wearingCoat, RemarkLedger remarks,
                                       double familiarity, bool companionNear)
        {
            var out1 = new Regard();
            if (g == null) return out1;
            Rumor strongest = null;
            foreach (var r in g.Rumors)
            {
                if (r == null || r.Content == null || r.Content.Subject != "player") continue;
                // The police asking after him is news of the police, not of
                // anything he did: it shows in their manner, but weighs nothing
                // on how they stand to him (town list 6bq, the independent check:
                // being asked moved a person from Comments to Avoids).
                if (PoliceFile.IsAsking(r)) continue;
                if (!(r.Confidence >= 0.0)) continue;   // a NaN must not hide a real story
                if (strongest == null || r.Confidence > strongest.Confidence) strongest = r;
            }
            var shows = StoryThatShows(g, shareFloor);
            var little = shows == null ? StoryHalfRemembered(g, shareFloor) : null;
            out1.Story = shows ?? little;
            out1.Knowing = shows != null ? Knowing.Enough : little != null ? Knowing.ALittle : Knowing.Nothing;
            out1.KnowsItIsHim = Acquaintance.CanNameYou(familiarity);
            bool shows1 = shows != null && out1.KnowsItIsHim;
            bool little1 = little != null && out1.KnowsItIsHim;
            bool had = remarks != null && remarks.HasRemarked(g.Id, out1.Story);
            out1.RemarkedAlready = had;
            // NOT THE LADDER'S PRESSURE EITHER (the second independent check): a
            // story about a man they cannot pick out is not a story about the
            // man in front of them, so it adds nothing to how they stand to him.
            double aboutHim = out1.KnowsItIsHim && strongest != null ? strongest.Confidence : 0.0;
            out1.Stance = Stance(g.Suspicion != null ? g.Suspicion.Value : 0.0, g.Loyalty,
                aboutHim, g.Leashed, wearingCoat,
                knowsSomething: shows1, remarkedAlready: had, knowsALittle: little1);
            out1.FirstLookMetres = FirstLookMetres(out1.Stance);
            out1.FirstLookSeconds = LookHoldSeconds(out1.Stance);
            out1.SecondLookMetres = SecondLookMetres(out1.Stance);
            out1.SecondLookSeconds = out1.SecondLookMetres > 0 ? KnowingLookSeconds : 0.0;
            out1.LookAwayMetres = LookAwayMetres(out1.Stance);
            out1.LooksBack = LooksBack(out1.Stance);
            // IN THE COAT, UNSURE IT IS HIM: whoever the coat leaves noticing him
            // only glances and looks away, as a stranger does (the check found
            // the knowing look given to a coat).
            if (wearingCoat && out1.Stance == StanceKind.Notices)
            {
                out1.SecondLookMetres = 0.0;
                out1.SecondLookSeconds = 0.0;
                out1.LookAwayMetres = CivilLookAwayMetres;
            }
            if (out1.Stance >= StanceKind.Comments)
                out1.Speaks = true;
            else if (little1 && companionNear && !had && !g.Leashed && !wearingCoat && MayRemarkFaintly(g.Id, little, shareFloor))
            {
                out1.Speaks = true;
                out1.Faint = true;
            }
            return out1;
        }

        /// WHAT SOMEBODY WHO KNOWS A LITTLE SAYS, once, to a companion, about
        /// him, as he goes past, where he can overhear (the gaze research: a
        /// word to a companion once he is past). None of it names the story:
        /// they would no longer pass it on. Their memory still holds it, so he
        /// can stop and ask what they meant.
        /// With `heard`, the line is one he has not heard lately (RemarkLedger.Fresh);
        /// without it, as before, the seed alone chooses.
        public static SpokenLine FaintRemark(Gossiper g, Rumor about, int seed, RemarkLedger heard = null)
        {
            if (g == null || about == null) return null;
            string text = heard != null ? heard.Fresh("faint", FaintLines, seed) : Pick(seed, FaintLines);
            return new SpokenLine { SpeakerId = g.Id, Text = text, AboutPlayer = true, Source = about, Bank = "faint" };
        }

        /// Fourteen, as every band is (BarkGen's repeat floor).
        internal static readonly string[] FaintLines =
        {
            "That's Mickey's nephew, that is.",
            "Is that him? The nephew?",
            "Somebody was saying something about him. I forget what.",
            "I've heard his name somewhere. Can't place it.",
            "There was talk about that one. Or was it somebody else.",
            "Him. Something went round about him. It'll come to me.",
            "I've heard a thing or two about him. Nothing I'd swear to.",
            "His name came up. I wasn't really listening.",
            "Didn't somebody say something about him? Never mind.",
            "He's the one people were on about. Only talk, mind.",
            "Something was said about him. It's gone now.",
            "People have been saying things about him. Half of it rubbish, I expect.",
            "I heard something about him. Can't remember who from.",
            "Keeps busy, that one, so I hear. Or so somebody said.",
        };

        /// The ladder's rungs by pressure, as they have stood since M15.2.
        static StanceKind Rung(double pressure, bool leashed)
        {
            if (pressure >= 0.86 && !leashed) return StanceKind.Confronts;
            if (pressure >= 0.72) return StanceKind.Refuses;
            if (pressure >= 0.58) return StanceKind.Avoids;
            if (pressure >= 0.42) return leashed ? StanceKind.Watches : StanceKind.Comments;
            if (pressure >= 0.26) return StanceKind.Watches;
            if (pressure >= 0.12) return StanceKind.Notices;
            return StanceKind.Indifferent;
        }

        /// How far away somebody starts tracking you with their eyes. An
        /// ordinary passer-by does not; somebody who has heard about the
        /// warehouse can pick you out down the length of a street.
        public static double GazeMetres(StanceKind stance) =>
            stance <= StanceKind.Indifferent ? 0
            : stance == StanceKind.Notices ? 6
            : stance == StanceKind.Watches ? 14
            : stance == StanceKind.Comments ? 12
            : stance == StanceKind.Avoids ? 18
            : 22;

        // ---- overheard exchanges: the mill, out loud ----

        /// The most tellings of one story of the town's own he makes out (town list 6aq).
        public const int MostNewsTellings = 4;

        /// What the two of them SAY when a rumour passes between them.
        ///
        /// The teller names the story; the hearer answers in the way their
        /// own disposition dictates. Both lines carry the rumour, so a player
        /// in earshot learns it by listening — the ledger row becomes a side
        /// effect of having heard, rather than the event itself.

        public static List<SpokenLine> Exchange(Rumor r, Gossiper from, Gossiper to, int seed, RemarkLedger heard = null)
        {
            var lines = new List<SpokenLine>();
            if (r == null || from == null || to == null) return lines;
            string what = Trim(r.Summary);
            if (string.IsNullOrEmpty(what)) return lines;
            // With `heard`, a line he has not heard lately from each bank
            // (RemarkLedger.Fresh, town list 6o); without it, the seed alone.
            string tellBank = null, answerBank = null;
            // A telling carries the story, so the ledger weighs its WORDING, the
            // story taken out (the independent check: three stories in a row all
            // opened "It's going round that", each fresh for its own story).
            string Tell(string bank, string[] bankLines)
            {
                tellBank = bank;
                if (heard == null) return Pick(seed, bankLines);
                var wordings = new string[bankLines.Length];
                for (int i = 0; i < bankLines.Length; i++) wordings[i] = Unfill(bankLines[i], what);
                int at = Array.IndexOf(wordings, heard.Fresh(bank, wordings, seed));
                return bankLines[at < 0 ? 0 : at];
            }
            string Reply(string bank, string[] bankLines)
            {
                answerBank = bank;
                int s = Answer(seed, to.Id);
                return heard != null ? heard.Fresh(bank, bankLines, s) : Pick(s, bankLines);
            }

            // THE TOWN'S OWN NEWS (town list 6aq): told as news, not as something
            // seen of a man ("I'd say it in front of him" is about him), and never
            // about the player.
            if (r.Content != null && r.Content.Subject == TownNews.Subject)
            {
                // Four tellings of one story he can make out; after that it is the
                // street's murmur, as real talk is (TownReach: thirteen an hour
                // before, the same words back inside three minutes).
                if (heard != null && heard.TimesToldHim(r.TopicKey) >= MostNewsTellings) return lines;
                string news = Tell("exchange/tell/news", new[]
                {
                    $"Did you hear? {Cap(what)}.",
                    $"Here, {what}.",
                    $"{Cap(what)}, apparently.",
                    $"You'll never guess. {Cap(what)}.",
                    $"They're saying {what}.",
                    $"Seems {what}.",
                    $"Have you heard? {Cap(what)}.",
                    $"I'll tell you something. {Cap(what)}.",
                    $"Talk of the street, this. {Cap(what)}.",
                    $"You'll want to hear this. {Cap(what)}.",
                });
                string heardIt = Reply("exchange/reply/news", new[]
                {
                    "Never.",
                    "Well, I never.",
                    "Go on.",
                    "You're joking.",
                    "Doesn't surprise me.",
                    "First I've heard of it.",
                    "There's always something.",
                    "Who told you that?",
                    "Well, it's none of my business.",
                    "I'd not have thought it."
                });
                lines.Add(new SpokenLine { SpeakerId = from.Id, Text = news, AboutPlayer = false, Source = r, Composed = true, Bank = tellBank, Wording = Unfill(news, what) });
                lines.Add(new SpokenLine { SpeakerId = to.Id, Text = heardIt, AboutPlayer = false, Source = r, Bank = answerBank });
                return lines;
            }

            // Fourteen a band rather than two or three. BarkGen measured the
            // old banks: EVERY slot in the game repeated inside ninety
            // seconds, and the ambient ones inside thirty. A street that says
            // the same eight sentences all evening is a street the player
            // stops hearing, and it takes the gossip system down with it —
            // the whole point is that what you overhear is causally true, and
            // nobody listens to a loop.
            string tell =
                r.Confidence >= 0.8 ? Tell("exchange/tell/certain", new[]
                {
                    $"I'm telling you, {what}.",
                    $"{Cap(what)}. I know what I saw.",
                    $"You want to know why I've been quiet? {Cap(what)}.",
                    $"{Cap(what)}. I'd say it in front of him.",
                    $"I was there. {Cap(what)}, and that's the end of it.",
                    $"Don't look at me like that. {Cap(what)}.",
                    // FOUR OF THESE USED TO OPEN ON THE SUMMARY, which made it
                    // six of fourteen — and a bank where nearly half the lines
                    // begin with the same six words is a bank the ear starts
                    // predicting. Found by the M17.4 curation pass, splitting
                    // the enumerated banks apart and counting openings, because
                    // the manifest's 126-line pair slots are 14 openers times 9
                    // replies and hide it completely.
                    //
                    // Two are DELIBERATELY left leading with the story. At this
                    // confidence, stating the thing flatly and letting it sit
                    // is what certainty sounds like, and rewriting every one of
                    // them would have cost the band its character to fix a
                    // counting problem.
                    $"My own eyes, not somebody's mouth. {Cap(what)}.",
                    $"You can believe what you like. {Cap(what)}.",
                    $"I've not slept right since. {Cap(what)}.",
                    $"I wish I hadn't seen it, but I did: {what}.",
                    $"Ask me again in a year and I'll tell you the same: {what}.",
                    $"There's no other way to read it: {what}.",
                    $"I'm not guessing. {Cap(what)}.",
                    $"Nobody's done a thing about it. {Cap(what)}.",
                })
                : r.Confidence >= 0.5 ? Tell("exchange/tell/secondhand", new[]
                {
                    $"They're saying {what}.",
                    $"Word is {what}.",
                    $"Somebody told me {what}. Make of it what you like.",
                    $"It's going round that {what}.",
                    $"Two people told me {what}. And those two don't speak.",
                    $"I had it off someone who'd know: {what}.",
                    $"You've heard, then. {Cap(what)}.",
                    $"The way I heard it, {what}. Others tell it worse.",
                    $"{Cap(what)}, if you believe the market.",
                    $"I'd not repeat it, but {what}.",
                    $"The talk is {what}. Take that how you like.",
                    $"Somebody at the docks reckons {what}.",
                    $"{Cap(what)}. That's the third time this week I've heard it.",
                    $"I'll say this much: {what}.",
                })
                : Tell("exchange/tell/doubtful", new[]
                {
                    $"There's a story going round that {what}. Probably nothing.",
                    $"You hear all sorts. {Cap(what)}, apparently.",
                    $"Somebody's saying {what}. Somebody's always saying something.",
                    $"{Cap(what)}, supposedly. People talk.",
                    $"I heard {what}, but not from anybody I'd trust.",
                    $"Bit of nonsense going about. {Cap(what)}.",
                    $"They'll tell you {what}. They'll tell you anything.",
                    $"Half the street reckons {what}. Half the street's wrong.",
                    $"{Cap(what)}? I'd want it from somebody with sense.",
                    $"You know how it is. {Cap(what)}, they say.",
                    $"There's a whisper that {what}. Not worth much.",
                    $"{Cap(what)}, or so I'm told, by people who weren't there.",
                    $"Don't quote me. {Cap(what)}, maybe.",
                    $"I'd give it a week before somebody says the opposite: {what}.",
                });

            // The hearer's answer is their character, not a canned reply.
            // The reply is CHARACTER, not acknowledgement. The same news has
            // to land differently on a frightened man and a greedy one, or
            // the disposition numbers under all of this are decoration.
            string answer =
                to.Nerve > 0.65 && r.Sensitive ? Reply("exchange/answer/nervous", new[]
                {
                    "Say that where it can be heard and see what it costs you.",
                    "I'd keep that behind my teeth if I were you.",
                    "Not here. Not with that door open.",
                    "You're a braver man than me, saying it out loud.",
                    "I didn't hear that. Understand me. I didn't hear it.",
                    "Whatever you think you know, forget it.",
                    "There's people who'd pay to hear you say that again.",
                    "Stop. I mean it. Stop.",
                    "You want to be careful whose name you put in a sentence.",
                    "I've got my mother to think of. Talk about the weather.",
                    "Some things you carry. You don't hand them round.",
                    "That's the kind of talk that ends with somebody moving away.",
                    "Say it quieter or don't say it.",
                    "I'm going to walk off now, and you're going to let me.",
                })
                : to.Loyalty > 0.65 ? Reply("exchange/answer/loyal", new[]
                {
                    "That's talk. People love talk.",
                    "I've known better people do worse for less.",
                    "And you believed it, did you?",
                    "There'll be a reason. There usually is.",
                    "That's not how he's struck me.",
                    "I'd want to hear it from him before I said it again.",
                    "People are quick to have an opinion about a stranger.",
                    "Mickey's family. That still means something to me.",
                    "You'd say the same about anyone with a bit of money coming in.",
                    "Half of that's true and the wrong half's the loud one.",
                    "I'll not be the one carrying that any further.",
                    "Give it a month. It'll be somebody else's turn.",
                    "That's a hard thing to say about a man who's done me no harm.",
                    "I've heard that story before, about somebody else.",
                })
                : to.Greed > 0.65 ? Reply("exchange/answer/greedy", new[]
                {
                    "Interesting, that. Worth something to somebody.",
                    "Who else knows?",
                    "How long have you been sitting on it?",
                    "There's people who'd want that. Paying people.",
                    "That's not gossip. That's leverage.",
                    "Keep it to yourself for a day or two. Do us both a favour.",
                    "Who'd you tell before me?",
                    "And what's he doing about it, that's the question.",
                    "You could do something with that, you know.",
                    "Does he know you know?",
                    "I'd not give that away for nothing.",
                    "Say that again, slowly.",
                    "Now that IS worth hearing.",
                    "Everything's worth something to the right ear.",
                })
                : Reply("exchange/answer/neutral", new[]
                {
                    "Who told you that?",
                    "Since when?",
                    "God. And here?",
                    "On this street?",
                    "Are you sure it was him?",
                    "That's the first I've heard of it.",
                    "Well. That's the week made interesting.",
                    "Since when has anybody round here been surprised by that?",
                    "Hm. Does Sheila know?",
                    "I'd rather not have heard that, if I'm honest.",
                    "What, and nobody's said anything?",
                    "That would explain a few things.",
                    "You're serious.",
                    "There's always something.",
                });

            // THE TELLING ONLY. It carries `what` inside it and is therefore
            // a new sentence every time; the answer is a literal pick from a
            // band and is in the bank as written, which the pair-halves check
            // confirms for all 2,268 pairs. Marking both would be tidier and
            // would put a real, renderable hole in the structural bucket the
            // first time a reply went missing — which is the misreading this
            // field exists to stop.
            lines.Add(new SpokenLine { SpeakerId = from.Id, Text = tell, AboutPlayer = true, Source = r, Composed = true, Bank = tellBank, Wording = Unfill(tell, what) });
            lines.Add(new SpokenLine { SpeakerId = to.Id, Text = answer, AboutPlayer = true, Source = r, Bank = answerBank });
            return lines;
        }

        /// Something said as the player goes past, by somebody who is holding
        /// a story about them. Short, pointed, and STOPPABLE — the player can
        /// turn round and ask what they meant, because the speaker's memory
        /// holds the same rumour this line came from.
        public static SpokenLine Recognition(Gossiper g, Rumor about, StanceKind stance, int seed, RemarkLedger heard = null)
        {
            if (g == null || stance < StanceKind.Comments) return null;
            // With `heard`, a line he has not heard lately from the same bank
            // (RemarkLedger.Fresh, town list 6k); without it, the seed alone.
            string usedBank = null;
            string From(string bank, string[] lines) { usedBank = bank; return heard != null ? heard.Fresh(bank, lines, seed) : Pick(seed, lines); }
            // Every one of these has to INVITE being stopped, because it can
            // be: the speaker's memory holds the same rumour the line came
            // from, so the player can turn round and ask what they meant. A
            // line that closes the subject wastes the only bark system in the
            // genre that can be interrogated.
            string text =
                stance >= StanceKind.Confronts ? From("recognition/confronts", new[]
                {
                    "You and I need a word. Not here.",
                    "I've been waiting to see you, as it happens.",
                    "Don't walk past me. Not today.",
                    "Stop there. You know why.",
                    "I've been rehearsing this. Give me a minute of it.",
                    "There you are. I've had four days to think about this.",
                    "You're going to stand there and hear it.",
                    "A word. It won't take long and it won't be pleasant.",
                    "I want to hear you say it to my face.",
                    "You've been avoiding this street. I noticed.",
                    "No. You'll not just nod and walk on.",
                    "Two minutes. You owe me that much.",
                    "I'd like an answer, and I'd like it today.",
                    "Look at me when I'm talking to you.",
                })
                : stance == StanceKind.Refuses ? From("recognition/refuses", new[]
                {
                    "I've nothing for you today.",
                    "Whatever it is, no.",
                    "Door's shut. Try somebody else.",
                    "Not for you. Not any more.",
                    "I'd rather not, and I'd rather not explain why.",
                    "We're closed. To you.",
                    "You'll want to ask somebody who doesn't know you.",
                    "No. And don't ask twice.",
                    "There's nothing here you want.",
                    "I've made up my mind about you.",
                    "Save your breath.",
                    "Not today. Not tomorrow either.",
                    "I've heard enough to know my answer.",
                    "Ask me in a year.",
                })
                : stance == StanceKind.Avoids ? From("recognition/avoids", new[]
                {
                    "...",
                    "Excuse me.",
                    "Sorry, in a hurry.",
                    "Can't stop.",
                    "Another time.",
                    "Mm.",
                    "I'm late as it is.",
                    "Not now. Sorry.",
                    "Right. Right.",
                    "Somebody's waiting on me.",
                    "Yes. No. Sorry.",
                    "I've got to be somewhere.",
                    "Mind yourself.",
                    "...Evening.",
                })
                // THE POLICE ASKING AFTER HIM (town list 6bq): whoever she asked
                // says so as the one she asked; whoever heard it, as talk.
                : PoliceFile.IsAsking(about) && about.Hops == 0 ? From("recognition/police-asked", new[]
                {
                    "That detective stopped me about you.",
                    "Had a detective on at me about you. Ellis, she said.",
                    "Ellis was asking me about you. Thought you'd want to know.",
                    "There's a woman detective asking about you.",
                    "The police asked me about you.",
                    "I've had the police at me over you.",
                })
                : PoliceFile.IsAsking(about) ? From("recognition/police-heard", new[]
                {
                    "That detective was asking after you, I hear.",
                    "Police were round asking about you, they say.",
                    "You've got the police asking questions, you know.",
                    "Word is Ellis was down the street after you.",
                    "Heard a detective's been asking about you.",
                    "They say the police have been asking round about you.",
                })
                // WHAT HE DID WITH THE OUTFIT'S ASK (town list 6z): the first hour
                // Jafar approved has the night come back to his face either way,
                // "Heard you told them no", and every answer sounded alike. Only
                // from somebody who heard it (the outfit's man was there). Six a
                // bank, not fourteen: a person remarks once on a story
                // (RemarkLedger), and a night's story reaches a handful in a day.
                : Arrangement.IsNight(about) && about.Hops > 0 && about.Content.Value == "did" ? From("recognition/outfit-did", new[]
                {
                    "Heard you did Mickey's run.",
                    "Down the landing after dark, I hear. Same as Mickey.",
                    "They say you've picked up where Mickey left off.",
                    "Word is you kept Mickey's arrangement. I'd keep that quiet.",
                    "Late one, was it? Down by the ferry.",
                    "So you're doing Mickey's rounds now.",
                })
                : Arrangement.IsNight(about) && about.Hops > 0 && about.Content.Value == "refused" ? From("recognition/outfit-refused", new[]
                {
                    "Heard you told them no.",
                    "Heard you sent Ron back with it.",
                    "They say you turned Mickey's lot down.",
                    "Word is you said no to them. Brave or daft, I've not decided.",
                    "You told them no, then. Not like Mickey, that.",
                    "Not doing Mickey's errands, I hear.",
                })
                : Arrangement.IsNight(about) && about.Hops > 0 && about.Content.Value == "noshow" ? From("recognition/outfit-noshow", new[]
                {
                    "Heard they waited on you at the landing.",
                    "Somebody stood by the ferry half the night, I'm told.",
                    "They say you never turned up.",
                    "Word is you left them waiting. They'll not like that.",
                    "Mickey'd never have kept them waiting, they say.",
                    "Busy, were you? Not at the landing, anyway.",
                })
                : about != null && about.Sensitive ? From("recognition/sensitive", new[]
                {
                    "There he is. The busy one.",
                    "Heard your name this week. More than once.",
                    "Funny hours you keep.",
                    "You get about, don't you.",
                    "Sleeping all right?",
                    "You want to be careful, a man as talked-about as you.",
                    "Someone was asking after you. I said I hadn't seen you.",
                    "Busy week, was it.",
                    "Odd, the places a name turns up.",
                    "I'd not say what I've heard. But I've heard it.",
                    "You'll know what people are saying.",
                    "Still standing. That surprises some.",
                    "Careful on that corner. People watch it.",
                    "You and I should have a proper talk one day.",
                })
                : From("recognition/ordinary", new[]
                {
                    "Mickey's nephew. Still standing, then.",
                    "All right.",
                    "How's Mickey's treating you?",
                    "Cold enough for you?",
                    "Your uncle'd have hated this weather.",
                    "Tell Sheila I said hello.",
                    "Still open, is it?",
                    "You've the look of him, you know. Around the eyes.",
                    "Long day?",
                    "Mind how you go.",
                    "That step of yours needs seeing to.",
                    "Good to see the lights on down there.",
                    "You'll be at the market Thursday, I expect.",
                    "Evening.",
                });
            return new SpokenLine { SpeakerId = g.Id, Text = text, AboutPlayer = about != null, Source = about, Bank = usedBank };
        }

        // ---- ambient life: the city that is busy without you ----

        /// Two people talking about THEIR OWN lives, not yours.
        ///
        /// This is the half that makes a place feel like it existed before
        /// the player arrived — and it is the half that was entirely absent.
        /// Everything here is drawn from state the game already simulates, so
        /// a street that has been squeezed sounds squeezed.
        /// THE STREET JUST AFTER A DEED (town list 6an; A13.21 and A13.20, the third
        /// checklist sweep): glass went, the street hushed for a second, and the
        /// next words he made out were two neighbours on the price of bread. For
        /// the first JustNowSeconds after a deed within earshot of them, a pair
        /// says what anybody would ("What was that? Glass?"), naming nobody they
        /// did not see; then, to SettlingSeconds, the street settling ("Gone quiet
        /// now, anyway."); and after that everyday talk again, which is the panic
        /// passing. In the player's real
        /// seconds, as what he hears is paced (ClearWordsEverySeconds): at two
        /// game minutes a second, ten game minutes would pass in five. `justNow`
        /// is what they heard: "glass", "shout", "crash", or anything else for a
        /// noise; `secondsSince` the real seconds since, below zero for none.
        public const double JustNowSeconds = 90.0, SettlingSeconds = 180.0;

        /// The first exchange after a deed comes as soon as the hush lifts, not
        /// ClearWordsEverySeconds later: people say "what was that" at once.
        public const double JustNowSpeakAfterSeconds = 3.0;

        public static List<SpokenLine> Ambient(Gossiper a, Gossiper b, GameTime now,
            double prosperity, double priceLevel, bool aInjured, bool feuding, int seed, RemarkLedger heard = null,
            string justNow = null, double secondsSince = -1)
        {
            var lines = new List<SpokenLine>();
            if (a == null || b == null) return lines;

            string opener;
            string reply;
            // With `heard`, lines he has not heard lately (town list 6o).
            string openBank = null, replyBank = null;
            string OpenLine(string bank, string[] bankLines) { openBank = bank; return heard != null ? heard.Fresh(bank, bankLines, seed) : Pick(seed, bankLines); }
            string ReplyLine(string bank, string[] bankLines)
            {
                replyBank = bank;
                int s = Answer(seed, b.Id);
                return heard != null ? heard.Fresh(bank, bankLines, s) : Pick(s, bankLines);
            }

            bool fresh = justNow != null && secondsSince >= 0 && secondsSince < JustNowSeconds;
            bool settling = justNow != null && secondsSince >= JustNowSeconds && secondsSince < SettlingSeconds;
            if (fresh)
            {
                string kind = justNow == "glass" || justNow == "shout" || justNow == "crash" ? justNow : "noise";
                opener = kind == "glass" ? OpenLine("ambient/open/justnow/glass", new[]
                    {
                        "What was that? Glass?",
                        "That was glass, that.",
                        "Somebody's window's gone in.",
                        "Did you hear that? Sounded like a window.",
                        "That's a window going, that is.",
                        "Glass. Down the road somewhere.",
                    })
                    : kind == "shout" ? OpenLine("ambient/open/justnow/shout", new[]
                    {
                        "Who's that shouting?",
                        "Somebody's shouting their head off.",
                        "Did you hear that shouting?",
                        "That's trouble, that is.",
                        "Hark at that.",
                    })
                    : kind == "crash" ? OpenLine("ambient/open/justnow/crash", new[]
                    {
                        "What was that bang?",
                        "Something's gone over, listen.",
                        "That was a crash, that.",
                        "What's gone on down there?",
                        "Something's come down, that.",
                        "Hell of a bang, that.",
                    })
                    : OpenLine("ambient/open/justnow/noise", new[]
                    {
                        "What was that?",
                        "Did you hear that?",
                        "What's going on down there?",
                        "Something's up.",
                        "What's all that about?",
                        "What the hell was that?",
                    });
                reply = ReplyLine("ambient/reply/justnow", new[]
                {
                    "Came from down that way.",
                    "I'm not going to look.",
                    "Best stay out of it.",
                    "Someone'll ring the police.",
                    "It's always something round here.",
                    "Keep your head down, that's what I say.",
                    "Not our business.",
                    "Don't go over. Leave it.",
                    "I heard it. I didn't see it.",
                    "Let's hope that's the end of it.",
                });
                lines.Add(new SpokenLine { SpeakerId = a.Id, Text = opener, Bank = openBank });
                lines.Add(new SpokenLine { SpeakerId = b.Id, Text = reply, Bank = replyBank });
                return lines;
            }
            if (settling)
            {
                opener = OpenLine("ambient/open/settling", new[]
                {
                    "Gone quiet now, anyway.",
                    "Whatever that was, it's done with.",
                    "Did anybody see what happened?",
                    "Curtains are twitching all down the street.",
                    "My heart's going ten to the dozen.",
                    "Whole street's on edge now.",
                });
                reply = ReplyLine("ambient/reply/settling", new[]
                {
                    "Somebody'll know what it was. Somebody always does.",
                    "I didn't see and I'm not asking.",
                    "Best not to wonder.",
                    "It'll be all round the street by tomorrow.",
                    "Least said, soonest mended.",
                    "Let it lie.",
                });
                lines.Add(new SpokenLine { SpeakerId = a.Id, Text = opener, Bank = openBank });
                lines.Add(new SpokenLine { SpeakerId = b.Id, Text = reply, Bank = replyBank });
                return lines;
            }

            // Fourteen a band. This is the family the player hears MOST — a
            // busy street starts one of these every thirteen seconds — and
            // BarkGen measured the original four-line bank looping inside
            // half a minute. The writing here is deliberately ordinary:
            // nothing in this function is about the player, and the moment a
            // line reaches for interest it stops being a city and starts
            // being a stage set with something to tell you.
            if (feuding)
            {
                opener = OpenLine("ambient/open/feud", new[]
                {
                    "I've nothing to say to you.",
                    "Don't. Just don't.",
                    "You've a nerve, standing there.",
                    "Walk on.",
                    "I saw you coming and I stayed anyway. Don't make me regret it.",
                    "I'm not having this.",
                    "Say what you came to say or move.",
                    "I've said all I'm saying.",
                    "You know what you did.",
                    "Not in front of people.",
                    "Whatever it is, it's too late for it.",
                    "I'd cross the road but I got here first.",
                    "Don't smile at me.",
                    "There's nothing left to talk about.",
                });
                reply = ReplyLine("ambient/reply/feud", new[]
                {
                    "Suits me.",
                    "That's how it is, then.",
                    "Right.",
                    "Have it your way. You always do.",
                    "I wasn't going to.",
                    "Fine.",
                    "One of us has to be sensible, and it won't be you.",
                    "As you like.",
                    "I'll be here when you've calmed down.",
                    "Understood.",
                    "You'll come round. You did last time.",
                    "Then I'll not keep you.",
                    "Suit yourself.",
                    "That's a shame. That's genuinely a shame.",
                });
            }
            else if (aInjured)
            {
                opener = OpenLine("ambient/open/injured", new[]
                {
                    "It's not healing. I've stopped pretending it is.",
                    "Can't lift with it. Can't do the work either.",
                    "It wakes me. That's the worst of it.",
                    "Doctor'd sign me off, and who pays the rent then?",
                    "I've been strapping it up and hoping.",
                    "You can smell it going bad. I'm not imagining that.",
                    "Every step. Every single step.",
                    "I've been doing it one-handed a fortnight now.",
                    "They'll not keep me on if I can't carry.",
                    "It was nothing. A week ago it was nothing.",
                    "I daren't stop. If I stop I don't start again.",
                    "It's worse in the cold. It's always worse in the cold.",
                    "I'd have it looked at if I could spare the day.",
                    "Don't. Don't touch it.",
                });
                reply = ReplyLine("ambient/reply/injured", new[]
                {
                    "Get it seen to before it goes bad.",
                    "You said that last week.",
                    "Go down casualty. You'll wait, but you'll be seen.",
                    "You'll lose the arm being proud.",
                    "Have you told them at work?",
                    "Sit down, at least. Sit down.",
                    "My father did the same and he never worked again.",
                    "That's not a wound any more, that's a decision.",
                    "Let me see it. No, properly.",
                    "You keep saying it's fine. It's not fine.",
                    "Take the day. The work'll still be there.",
                    "I'd not let a dog go on like that.",
                    "There's no shame in a week on the sick.",
                    "Promise me you'll go this week.",
                });
            }
            else if (priceLevel > 1.12)
            {
                opener = OpenLine("ambient/open/prices", new[]
                {
                    "Bread's gone up again. Again.",
                    "Everything's dearer and nobody will say why.",
                    "I paid what I paid last month and got less of it.",
                    "Have you seen what they want for mince?",
                    "Same basket, half the basket.",
                    "I stopped buying it. That's my answer to it.",
                    "It all adds up. Penny here, penny there.",
                    "It's not the price. It's that they say it like it's normal.",
                    "My rent's the same, my wages are the same, and yet.",
                    "There's no shortage. I've seen the store rooms.",
                    "Somebody's making that money. It's not us.",
                    "Twice this month. Twice.",
                    "I asked why and got a shrug for my trouble.",
                    "I've started keeping a list. It's not cheering reading.",
                });
                reply = ReplyLine("ambient/reply/prices", new[]
                {
                    "It's the deliveries. Ask anyone who takes one.",
                    "My money's the same money it was.",
                    "You'll get used to it. We always do.",
                    "There's men getting fat on it, you can be sure.",
                    "Wait till the winter.",
                    "It's the same everywhere. That's what they tell me, anyway.",
                    "I've gone back to the market. Costs me an hour, saves me a pound.",
                    "Nobody's putting wages up to match, funny that.",
                    "My mother said the same in her day. Doesn't help.",
                    "You should see what they charge across the water.",
                    "Complain to who? That's the trouble.",
                    "I buy less and eat less and there we are.",
                    "It'll settle. It usually settles.",
                    "Don't get me started.",
                });
            }
            else if (prosperity < 0.35)
            {
                opener = OpenLine("ambient/open/slump", new[]
                {
                    "Nobody's spending. You can feel it on the street.",
                    "Third quiet week. I've started counting them.",
                    "I've had four people in since I opened.",
                    "You can hear the clock in my shop. That's how quiet.",
                    "Even the market's thin.",
                    "I've laid my assistant off. I hated doing it.",
                    "Half these shutters weren't down last year.",
                    "There's no work at the docks. None.",
                    "People are walking past looking, not coming in.",
                    "I'll give it till the spring and then I don't know.",
                    "It's not a bad patch now. It's just how it is.",
                    "Nobody's got it to spend, that's the truth of it.",
                    "I've started taking payment in bits.",
                    "It's the waiting I can't stand.",
                });
                reply = ReplyLine("ambient/reply/slump", new[]
                {
                    "It'll turn. It always turns.",
                    "And the bank wants its money all the same.",
                    "Same for everybody. If that helps, which it doesn't.",
                    "Give it till the season changes.",
                    "I've been saying that for six months.",
                    "You've weathered worse than this.",
                    "There's still money on this street. It's just not moving.",
                    "My takings are down a third and I'm one of the lucky ones.",
                    "It's not you. Don't go blaming yourself.",
                    "Hold on. That's all any of us can do.",
                    "There'll be work when the boats come back.",
                    "I'd not shut. Once you shut you don't open.",
                    "Everybody's saying it. That's how I know it's real.",
                    "Come round Sunday. We'll not talk about money.",
                });
            }
            else if (now.Hour >= 21 || now.Hour < 5)
            {
                opener = OpenLine("ambient/open/night", new[]
                {
                    "You're out late.",
                    "Long shift?",
                    "You'll catch your death standing about.",
                    "Nothing good happens at this hour.",
                    "Couldn't sleep either?",
                    "It's a different street after eleven.",
                    "You're the third person I've passed. On a Tuesday.",
                    "Quiet, isn't it. Properly quiet.",
                    "I like it now. Nobody wants anything.",
                    "Watch the corner. It's dark since the lamp went.",
                    "Off home?",
                    "You're keeping strange hours lately.",
                    "That's the second time round the block for me.",
                    "Cold gets in at this hour.",
                });
                reply = ReplyLine("ambient/reply/night", new[]
                {
                    "It's the only quiet part of the day.",
                    "Someone has to be.",
                    "Nearly. Nearly.",
                    "I'll sleep when the bill's paid.",
                    "Couldn't settle. You know how it is.",
                    "Walking helps. Don't ask me why.",
                    "Work. What else.",
                    "I've stopped trying to sleep before two.",
                    "Nowhere to be, that's the trouble.",
                    "Same as you, by the look of it.",
                    "It's the only time I get to think.",
                    "Half an hour and I'm in.",
                    "You take care going back.",
                    "Aye. Goodnight to you.",
                });
            }
            else
            {
                opener = OpenLine("ambient/open/ordinary", new[]
                {
                    "Cold one.",
                    "How's your mother keeping?",
                    "Did you settle that business with the landlord?",
                    "You'll be at the market Thursday?",
                    "That's the rain coming, that is.",
                    "You've had your hair cut.",
                    "Have you a minute? No, it'll keep.",
                    "I've been meaning to catch you.",
                    "Did the roof hold?",
                    "You look better than you did.",
                    "Any word from your brother?",
                    "They've dug the road up again.",
                    "I've got that thing you asked about, when you want it.",
                    "You're the fourth person to say that to me today.",
                });
                // SIX OF THESE USED TO ANSWER ONE SPECIFIC OPENER, and that is
                // a defect the manifest cannot show you.
                //
                // `Answer()` hashes the REPLIER's id, deliberately decorrelated
                // from which opener was drawn — so the two are picked
                // independently and every reply has to work after every opener.
                // The other five ambient bands are single-topic, so any reply
                // follows any opener and the decorrelation is free. `ordinary`
                // is not a topic, it is a catch-all: its openers are about a
                // roof, a landlord, a mother, a market, a brother and the road.
                //
                // So "It held. Just about." — written for "Did the roof hold?"
                // — landed after "Cold one." thirteen times in fourteen. Every
                // line was well-formed, distinct and clean under `TextShape`;
                // the pair was simply nonsense, and a player who hears two
                // neighbours fail to have a conversation learns that the street
                // is generated. That is the exact thing the whole system exists
                // to avoid.
                //
                // Rewritten so each one follows anything a neighbour might open
                // with. The specificity moves to the OPENER side, which is
                // unconditioned and cannot mismatch.
                reply = ReplyLine("ambient/reply/ordinary", new[]
                {
                    "Same as ever.",
                    "Better this week, any road.",
                    "Don't ask. Not today.",
                    "All being well.",
                    "Can't complain. Well. I could.",
                    "Somebody was asking after you, as it happens.",
                    "Not so bad. You?",
                    "Ask me tomorrow and you'll get a different answer.",
                    "Just about holding. That's the size of it.",
                    "I'll catch you Friday, if that suits.",
                    "Getting on with it, you know.",
                    "Mustn't grumble.",
                    "There's always something, isn't there.",
                    "Aye, well. It passes.",
                });
            }

            lines.Add(new SpokenLine { SpeakerId = a.Id, Text = opener, Bank = openBank });
            lines.Add(new SpokenLine { SpeakerId = b.Id, Text = reply, Bank = replyBank });
            return lines;
        }

        // ---- the street's volume IS its temperature ----

        /// How loud the street is about you, 0..1 — the thing the status line
        /// used to say in words. A hot street is a talkative one, and the
        /// player should learn to read the NOISE rather than the readout.
        public static double ChatterLevel(double dayCircleHeat, int peopleInEarshot) =>
            Clamp01(0.25 + 0.75 * Clamp01(dayCircleHeat)) * Clamp01(peopleInEarshot / 6.0);

        /// How often, in seconds, an ambient exchange should start near the
        /// player. Busier when there are more people and when there is
        /// something to talk about; but never oftener than
        /// ClearWordsEverySeconds, the words he can make out (the street's
        /// murmur is ChatterLevel and keeps its pace).
        public static double AmbientEverySeconds(double dayCircleHeat, int peopleInEarshot) =>
            AmbientEverySeconds(dayCircleHeat, peopleInEarshot, ClearWordsEverySeconds);

        /// The same at another floor, for measuring what the floor does
        /// (TownReach --two-hours --clear-every). A heat that is not a number
        /// counts as none, so no heat can take the pace under the floor.
        public static double AmbientEverySeconds(double dayCircleHeat, int peopleInEarshot, double floorSeconds)
        {
            if (peopleInEarshot < 2) return double.MaxValue;
            if (double.IsNaN(dayCircleHeat)) dayCircleHeat = 0.0;
            double busy = 0.5 + 0.5 * Clamp01(dayCircleHeat);
            return Math.Max(floorSeconds, 26.0 / busy / Math.Max(1, peopleInEarshot) * 3.0);
        }

        /// THE NEIGHBOURS' WORDS NO OFTENER THAN THIS (town list 6o, 28
        /// September; the ruling is Jafar's, on the 29 September page, and this
        /// is the recommendation carried meanwhile). Measured over two hours of
        /// play on the named cast's street (TownReach --two-hours, the game's own
        /// timer and ranges): at the old floor of 6 s he heard 137 to 443
        /// exchanges, and a fourteen-line band came round every 1.4 to 1.7
        /// minutes even with the ledger of what he has heard. At 45 s (64 to 96
        /// exchanges), fourteen lines never come back inside BarkGen's ten-minute
        /// floor: 22 minutes on a walk, 15 where the cast is busiest, and 10.5
        /// with a crowd always near him.
        public const double ClearWordsEverySeconds = 45.0;

        // ---- helpers ----

        static string Pick(int seed, string[] options)
        {
            if (options == null || options.Length == 0) return "";
            int i = seed % options.Length;
            if (i < 0) i += options.Length;
            return options[i];
        }

        /// The seed for the SECOND half of an exchange.
        ///
        /// This used to be `seed + 1`, which sounds harmless and is not.
        /// Every bank is the same length, so opener[i] was always followed by
        /// reply[i+1] — fourteen banks of fourteen lines produced fourteen
        /// fixed conversations rather than a hundred and ninety-six, and no
        /// amount of writing more lines would have changed that. BarkGen
        /// found it by counting distinct PAIRS instead of distinct lines,
        /// which is the number a listener actually experiences.
        ///
        /// The seed for the reply — mixed with WHO IS REPLYING.
        ///
        /// This took three attempts and the first two were both wrong in ways
        /// that only counting distinct CONVERSATIONS could see:
        ///
        ///   `seed + 1`    — fourteen banks of fourteen gave fourteen fixed
        ///                   conversations. opener[i] always met reply[i+1].
        ///   `seed * 7 + 3` — WORSE. Seven divides fourteen, so the reply
        ///                   index took two values and every band collapsed
        ///                   from fourteen replies to two.
        ///   `seed * 97`   — still fourteen conversations, because both
        ///                   indices were functions of ONE number, and a
        ///                   bijection is a bijection however prime you make
        ///                   it.
        ///
        /// The actual fix is a second independent input, and there is an
        /// obvious one: the person answering. The same remark now gets a
        /// different answer from a different neighbour, which is what it
        /// should have been doing all along.
        ///
        /// FNV-1a rather than string.GetHashCode, which is randomised per
        /// process on .NET Core — the same save would have produced different
        /// conversations on each launch, and every deterministic test in this
        /// repo would have been quietly lying.
        static int Answer(int seed, string replierId) =>
            seed * 97 + 31 + (int)(Hash(replierId) % 9973);

        static uint Hash(string s)
        {
            uint h = 2166136261;
            if (s != null)
                foreach (char c in s) { h ^= c; h *= 16777619; }
            return h;
        }

        static string Trim(string s)
        {
            if (string.IsNullOrEmpty(s)) return s;
            s = s.Trim();
            if (s.EndsWith(".")) s = s.Substring(0, s.Length - 1);
            return s;
        }

        /// The rumour, capitalised, for the templates that put it at the start
        /// of a sentence.
        ///
        /// A `Rumor.Summary` is a lowercase clause — "the new owner was at the
        /// warehouse on Tuesday" — because it is written to be spliced into
        /// the middle of a sentence, and half the templates do exactly that.
        /// The other half do not: twenty-one of the forty-two open on it or
        /// follow a full stop, and every one of those was rendering "Don't
        /// quote me. the new owner was at the warehouse on Tuesday" in a
        /// subtitle. Found by reading the generated bank line by line, which
        /// is what the bark curation pass is for — no test asserts the shape
        /// of a sentence, and it is the most-heard mechanic in the game.
        ///
        /// Only the first character moves. A summary that already starts with
        /// a proper noun is left exactly as it is.
        /// A composed line with its story taken back out: "{what}" where the
        /// story stood, "{What}" where it opened the sentence.
        internal static string Unfill(string text, string what)
        {
            if (string.IsNullOrEmpty(text) || string.IsNullOrEmpty(what)) return text;
            return text.Replace(Cap(what), "{What}").Replace(what, "{what}");
        }

        /// What the ledger keeps of a line he heard: the words, or for a
        /// composed telling its wording without the story (town list 6o).
        internal static string WordingOf(SpokenLine line) =>
            line == null ? null
            : line.Wording ?? (line.Composed && line.Source != null ? Unfill(line.Text, Trim(line.Source.Summary)) : line.Text);

        static string Cap(string s) =>
            string.IsNullOrEmpty(s) || !char.IsLower(s[0])
                ? s
                : char.ToUpperInvariant(s[0]) + s.Substring(1);

        static double Clamp01(double v) => v < 0 ? 0 : v > 1 ? 1 : v;
    }
}
