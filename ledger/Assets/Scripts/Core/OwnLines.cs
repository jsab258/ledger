using System.Collections.Generic;

namespace Ledger.Core
{
    /// THE STREET'S NAMED PEOPLE IN THEIR OWN WORDS (U2, Jafar's list of 30
    /// September: "the street's lines written ahead ... for every named
    /// character, in their own voice as their casting sheet describes it").
    /// StreetVoice's banks are anonymous: any speaker says any line, so the
    /// whole street talks with one voice, and a shared line can be absurd in a
    /// named mouth (Ron saying "Heard Ron went down the landing for you").
    /// Here a named person has lines of their own for a bank; StreetVoice
    /// takes theirs first, kept by the ledger under the bank and their id, so
    /// the no-repeat rule runs over their own lines, and falls back to the
    /// shared bank for any bank they have none for.
    ///
    /// How many a bank: from how often each fires for them in two hours of
    /// play on the busiest walk (TownReach --two-hours, by named speaker, 30
    /// September: Ron 28 everyday openers and 10 at night), with a margin, and
    /// at least two for any bank at all, so nothing comes back inside two
    /// hours (production/research/ambient-lines/METHOD-2026-09-30.md).
    ///
    /// Every opener must stand before any reply, and every reply after any
    /// opener: the two are chosen apart. Any line must stand at any hour of
    /// its band, in any weather, to anybody: no "morning" in the everyday
    /// band, which runs from five till nine at night, no sun, and nothing about
    /// who the other one is. Nothing here names a person, place or
    /// happening the speaker could not know, and nothing touches drink,
    /// betting or children (canon's content rule).
    ///
    /// One character complete first, Ron, as the sample for Jafar's page:
    /// nothing is multiplied before he approves one (CLAUDE.md).
    public static class OwnLines
    {
        public static readonly Dictionary<string, Dictionary<string, string[]>> ByCast = new Dictionary<string, Dictionary<string, string[]>>
        {
            // RON KIRBY (production/casting/ron-kirby/SHEET.md; the card, rocco.md):
            // 58, thirty years a docker until the scheme ended in 1989, the door
            // and the rank since; low, worn, decent without softness; rambling,
            // familiar, "boss" to Tom and "friend" now and then, never every
            // breath; answers from the pavement: the rank, the gate, the weather.
            ["rocco"] = new Dictionary<string, string[]>
            {
                ["ambient/open/ordinary"] = new[]
                {
                    "How's the world treating you, friend?",
                    "Keeping all right, friend?",
                    "Weather can't make its mind up.",
                    "Wind's round to the east. Feel that.",
                    "Fish van was late again.",
                    "Still going, then?",
                    "How's the back?",
                    "Not seen you on the street for a bit.",
                    "Kept you busy, have they?",
                    "Quiet on the rank today.",
                    "Taking it steady, friend?",
                    "Did you get that sorted, in the end?",
                    "Anything going cheap your end?",
                    "Grey old day, this.",
                    "Smell of fish never leaves this street, does it?",
                    "Not much in the paper. Never is.",
                    "Bearing up, friend?",
                    "Cold enough for you, friend?",
                    "Your feet holding up?",
                    "These boots have done some miles on that rank.",
                    "Looking better than last week, friend.",
                    "Anything doing your end?",
                    "They've still not fixed that lamp by the gate.",
                    "Getting by, are you?",
                    "Days are drawing in now, friend.",
                    "Water's brown as tea today.",
                    "You get your letter about the poll tax?",
                    "Gulls are loud today. Weather coming.",
                    "Keeping out of trouble?",
                    "You all right? You look done in.",
                    "Stop a minute, friend. How's things?",
                    "You'll want your big coat soon.",
                },
                ["ambient/reply/ordinary"] = new[]
                {
                    "Same as ever, friend.",
                    "Can't grumble. Wouldn't do any good.",
                    "Getting by, friend. Getting by.",
                    "Not so bad. Feet are killing me.",
                    "Could be worse. Thirty years on the quay taught me that.",
                    "Aye, well. You know how it is.",
                    "I'll live, friend.",
                    "Don't start me off, friend.",
                    "Ask me when I've sat down.",
                    "One day at a time, friend.",
                },
                ["ambient/open/night"] = new[]
                {
                    "You're out late, friend.",
                    "Rank's dead. Not had a fare in an hour.",
                    "Cold's come down now, hasn't it.",
                    "Quiet as the grave tonight.",
                    "Last hour, then I'm off.",
                    "Only us daft enough to be out, friend.",
                    "Mind the kerb. It's black as pitch down there.",
                    "You want to get yourself home. It's bitter.",
                    "Street's a different place once it's dark.",
                    "I'll give it another hour, then I'm off.",
                    "Hear that? Just the water.",
                    "Not a soul about. I like it like this.",
                    "You'll catch your death out here.",
                    "Long shift, friend?",
                },
                ["ambient/reply/night"] = new[]
                {
                    "Someone's got to watch the gate.",
                    "Nearly done, friend. Nearly.",
                    "Nights are the easy bit. Nobody wants owt.",
                    "I don't sleep much these days anyway.",
                    "Go on, get yourself in.",
                    "Aye. Mind how you go.",
                },
                ["ambient/open/slump"] = new[]
                {
                    "Three fares. That's the lot. Three.",
                    "Street's dead since the docks went.",
                    "Nobody's got the money for a cab these days.",
                    "Cab's sat on that rank like it's parked for good.",
                    "I've seen quiet, friend, but not like this.",
                    "Bus shelter's busier than the rank.",
                },
                ["ambient/reply/slump"] = new[]
                {
                    "Docks went and took the street with them.",
                    "Somebody's making money. It's not round here.",
                    "Same on the rank. Nobody's paying.",
                    "I've seen it come and go. It comes back.",
                },
                ["ambient/open/prices"] = new[]
                {
                    "Tea's gone up again at the caff.",
                    "You seen what they want for a loaf now?",
                    "Rent's up again. Letter came, bold as you like.",
                    "Everything's dearer and nobody's wages are.",
                    "Gas bill came. I had to sit down.",
                },
                ["ambient/reply/prices"] = new[]
                {
                    "Don't. I've stopped looking.",
                    "Same everywhere, friend.",
                    "I go without, mostly. Easier.",
                },
                ["ambient/open/injured"] = new[]
                {
                    "Don't ask. I walked into something.",
                    "Took a knock. It's nothing.",
                    "I'm all right. Don't fuss.",
                },
                ["ambient/reply/injured"] = new[]
                {
                    "Seen that go bad on the quay. Mind it.",
                    "Casualty'll see you. It's only a wait.",
                    "Sit down a minute. The rank'll keep.",
                },
                ["ambient/open/feud"] = new[]
                {
                    "I've nothing to say to you. Go on.",
                    "You know where I stand. Keep walking.",
                    "Say your piece or shift.",
                },
                ["ambient/reply/feud"] = new[]
                {
                    "Suit yourself, friend.",
                    "I'll remember that.",
                    "I'm not the one stood there scowling.",
                },
                ["ambient/open/justnow/glass"] = new[]
                {
                    "That's glass. That's a window, that.",
                    "Hear that? Somebody's window.",
                },
                ["ambient/open/justnow/shout"] = new[]
                {
                    "Who's that bawling?",
                    "Somebody's shouting down there.",
                },
                ["ambient/open/justnow/crash"] = new[]
                {
                    "What's come down?",
                    "That was a crash, that.",
                },
                ["ambient/open/justnow/noise"] = new[]
                {
                    "What was that?",
                    "Hang on. Something's up.",
                },
                ["ambient/reply/justnow"] = new[]
                {
                    "I'll not go looking. Not for nowt.",
                    "Leave it be. It's not ours.",
                    "Leave it. Somebody'll ring.",
                },
                ["ambient/open/settling"] = new[]
                {
                    "Gone quiet again.",
                    "Whatever it was, it's done.",
                    "Whole street'll know by tomorrow.",
                },
                ["ambient/reply/settling"] = new[]
                {
                    "Let it settle, friend.",
                    "Somebody saw. Somebody always does.",
                    "Best not to wonder, friend.",
                },
                // To Tom's face, as he goes by (StreetVoice.Recognition).
                ["recognition/ordinary"] = new[]
                {
                    "Boss.",
                    "All right. Rank's quiet.",
                    "Boss. Kettle's on in the office.",
                    "Cold one, boss. Mind how you go.",
                    "Anything you want watching, boss?",
                    "Quiet day. Mostly.",
                },
                ["recognition/sensitive"] = new[]
                {
                    "Your name's going round, boss. Just so you know.",
                    "People are talking. I don't join in.",
                    "Keep your head down a day or two, boss.",
                    "Heard a thing or two. It'll keep.",
                },
                ["recognition/confronts"] = new[]
                {
                    "A word, boss. Not out here.",
                    "We need to talk, you and me.",
                },
                ["recognition/refuses"] = new[]
                {
                    "Not today, boss. Ask somebody else.",
                    "I've nothing for you.",
                },
                ["recognition/avoids"] = new[]
                {
                    "Boss.",
                    "Busy, boss. After.",
                    "Another time, boss.",
                },
                ["recognition/taken-saw"] = new[]
                {
                    "Saw them put you in the car, boss. I kept the rank going.",
                    "You're out, then. Saw them take you off.",
                },
                ["recognition/taken-heard"] = new[]
                {
                    "Heard the police had you in, boss.",
                    "They say you were down the station.",
                },
                ["recognition/police-asked"] = new[]
                {
                    "Ellis was at me about you, boss. Wanted you to hear it from me.",
                    "Detective stopped me about you, boss. You'll want to hear what she asked.",
                },
                ["recognition/police-heard"] = new[]
                {
                    "Heard a detective's been asking round about you, boss.",
                    "Police are asking about you, so they say.",
                },
                ["recognition/arrival-saw"] = new[]
                {
                    "You'll be Mickey's nephew. Ron. I keep the rank.",
                    "Saw you come in with your case. Mickey's nephew, is it?",
                },
                ["recognition/arrival-heard"] = new[]
                {
                    "You'll be the new owner, then. Ron. The rank's mine, the door too.",
                    "Heard Mickey's nephew had come. That'll be you, boss.",
                },
                ["recognition/threat-told"] = new[]
                {
                    "I heard you, boss. I'm still stood here.",
                    "Thirty years on the quay, boss. I've been told worse by better.",
                },
                ["recognition/threat-heard"] = new[]
                {
                    "Word is you've been leaning on folk, boss. The street keeps count.",
                    "Heard you've been threatening people. It gets round.",
                },
                ["recognition/outfit-did"] = new[]
                {
                    "Heard you did Mickey's run. Watch yourself down there.",
                    "Went all right, I hear, boss. Say nowt.",
                },
                ["recognition/outfit-refused"] = new[]
                {
                    "I took your no down myself, boss. Mickey never sent one.",
                    "They had it from me. They'll not forget it.",
                },
                ["recognition/outfit-wounddown"] = new[]
                {
                    "That's Mickey's arrangement done with, boss. I took word down myself.",
                    "They'll not be calling. That's finished.",
                },
                ["recognition/outfit-noshow"] = new[]
                {
                    "Heard they waited on you at the landing, boss.",
                    "You never went down. They'll have noticed.",
                },
                ["recognition/week-winddown"] = new[]
                {
                    "Heard you're winding Mickey's down, boss. Just the cabs, then.",
                    "Can't say I'm sorry, boss. Mickey's other business never did him any good.",
                },
                ["recognition/week-takeover"] = new[]
                {
                    "Heard you're taking it all on. All of Mickey's.",
                    "So you're the new Mickey, boss. We'll see.",
                },
                ["recognition/week-wontsay"] = new[]
                {
                    "Sheila says you'll not tell her, boss. You'll not tell me either, I expect.",
                    "Keeping it to yourself. Fair enough.",
                },
                // Half a word to whoever is beside him, once Tom is past (StreetVoice.FaintRemark).
                ["faint"] = new[]
                {
                    "That's the boss. Mickey's nephew.",
                    "There's been talk about him. I'll not repeat it.",
                    "He's all right. So far.",
                },
            },
        };

        /// This person's own lines for the bank, and the name the ledger keeps
        /// them under ("bank@id"); null when they have none for it.
        public static (string bank, string[] lines)? For(string speakerId, string bank)
        {
            if (speakerId == null || bank == null) return null;
            if (!ByCast.TryGetValue(speakerId, out var banks) || !banks.TryGetValue(bank, out var lines) || lines == null || lines.Length == 0) return null;
            return (bank + "@" + speakerId, lines);
        }
    }
}
