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
    /// nothing is multiplied before he approves one (CLAUDE.md). Then (his tap
    /// of 1 October, one more try, one review) only the moments the game plays
    /// to Tom, each person only for the stories their day lets them hold:
    /// Darren, Father Walsh and June passed the review and are here; Sheila,
    /// Alison and Ada failed it and keep the shared banks for good
    /// (production/research/ambient-lines/own-lines-2026-10-01.md).
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
            // DARREN MILNER (production/casting/darren-milner/SHEET.md; the card, sam.md):
            // 25, the street hustler on his rounds; quick, ingratiating, always half into
            // a favour; what he has heard is what he trades, and he says so; easily
            // scared and open about it. "So listen" when he has something to sell.
            ["sam"] = new Dictionary<string, string[]>
            {
                ["recognition/sensitive"] = new[]
                {
                    "So listen. Your name's doing the rounds. I'm not saying where. Yet.",
                    "Everybody's got a version of you going. Mine's the one worth having.",
                    "There he is. You want to know what's being said, you know where I'll be.",
                },
                ["faint"] = new[]
                {
                    "Him? I had something on him. Can't have been worth much, I've forgot it.",
                    "Don't look. That's him. Whisper going round a while back. Old news.",
                },
                ["recognition/police-asked"] = new[]
                {
                    "Ellis had me in a doorway over you. I said I'd seen nothing. I'm good at that.",
                    "Your detective friend's been on at me. Didn't tell her much. Didn't know much, did I.",
                },
                ["recognition/taken-saw"] = new[]
                {
                    "Saw them stick you in the back of the panda. You're out quick. Who'd you know?",
                    "Out already? Watched them drive you off. Thought that was the last of you.",
                },
                ["recognition/taken-heard"] = new[]
                {
                    "Hear you had a ride with the police. Free taxi, that. Nice for a cab man.",
                    "They're saying the law lifted you. You're walking about, so it can't have been much.",
                },
                ["recognition/outfit-did"] = new[]
                {
                    "So you did Mickey's errand by the ferry. I'll not ask. I'd only have to forget it.",
                    "Picked up the late run, they're saying. Nobody's heard it from me.",
                },
                ["recognition/outfit-refused"] = new[]
                {
                    "Turned them down, did you? Takes nerve, that. Or you don't know who they are.",
                    "Word is you turned the ferry lot down. I'd walk the long way home for a bit.",
                },
                ["recognition/outfit-wounddown"] = new[]
                {
                    "Mickey's old arrangement's off, they say. There's people by the ferry not happy about that.",
                    "Finished with the sideline, I hear. Clean hands. Doesn't pay, but there you go.",
                },
                ["recognition/outfit-noshow"] = new[]
                {
                    "You left them stood by the ferry half the night. They've been asking where you were.",
                    "Never turned up, they're saying. I'd have a story ready if I were you.",
                },
                ["recognition/threat-told"] = new[]
                {
                    "Message received, mate. I've gone deaf and blind, me.",
                    "No need to say it twice. I've forgot everything already.",
                },
                ["recognition/threat-heard"] = new[]
                {
                    "Leaning on folk now, are you? Not on me, I hope. I scare easy, me.",
                    "Somebody's been told to keep shut, I hear. I keep shut for nothing, me.",
                },
                ["recognition/week-takeover"] = new[]
                {
                    "Mickey's whole lot, then? Big shoes, mate. Anything wants fetching, I'm your man.",
                    "Taking the lot on, they're saying. You'll be needing friends. I'm cheap.",
                },
                ["recognition/week-winddown"] = new[]
                {
                    "Only the cabs from now on, I hear. Shame. I had ideas.",
                    "Winding the other business up, they reckon. Safer. Duller, mind.",
                },
                ["recognition/week-wontsay"] = new[]
                {
                    "Not even telling Sheila, they say. You can tell me. I'll only tell people who pay.",
                    "Keeping it under your hat. That's worth something, that, to the right buyer.",
                },
                ["recognition/refuses"] = new[]
                {
                    "I'm not dealing with you, mate. Bad for business.",
                    "Your money's no good with me now. Nothing personal.",
                },
                ["recognition/confronts"] = new[]
                {
                    "Here. Word with you. What you did's got people asking me, and I don't like being asked.",
                    "No, stop a minute. I've had nothing but grief over you.",
                },
            },
            // FATHER WALSH (production/casting/father-emil/SHEET.md): about 61, the
            // Irish-born parish priest; soft and slow; never asks where anyone has been,
            // only whether they are all right; the police are "the guards" from habit.
            ["emil"] = new Dictionary<string, string[]>
            {
                ["recognition/sensitive"] = new[]
                {
                    "I hear things, God help me. I don't hold any of them against a man.",
                    "You look like a man carrying something. My door's open, any hour.",
                    "There's a lot said about you. None of it's my business unless you make it so.",
                },
                ["faint"] = new[]
                {
                    "God keep him. There's been talk, I know. I'd not trouble with it.",
                    "That's the young fella with the cabs. Whatever it was, I let it go by.",
                },
                ["recognition/police-asked"] = new[]
                {
                    "The detective was round asking about you. I said I see you about the street, which is the truth of it.",
                    "That Ellis woman came to me about you. I've no stories to give her, and I said so.",
                },
                ["recognition/police-heard"] = new[]
                {
                    "The guards are asking after you, I'm told. The police, I mean. Old habit.",
                    "If the police come to you, and you want somebody to stand beside you, say.",
                },
                ["recognition/taken-heard"] = new[]
                {
                    "I heard they took you in. I said a prayer, for what it's worth. It's not nothing.",
                    "You're out, thank God. I hope they treated you decent.",
                },
                ["recognition/threat-told"] = new[]
                {
                    "Threats don't work on an old priest, son. I've nothing left anyone can take.",
                    "I'll forget you said that. I'd rather you did too.",
                },
                ["recognition/threat-heard"] = new[]
                {
                    "Frightening people, they're saying. That's not the man I took you for.",
                    "Fear buys you nothing in the end. I've watched men try.",
                },
                ["recognition/avoids"] = new[]
                {
                    "The chapel's waiting on me. Another time.",
                    "Forgive me, I'm late for a call.",
                },
            },
            // JUNE (production/casting/june/SHEET.md): 38, Mickey's estranged daughter,
            // back for the funeral and leaving soon; Tom's cousin; quick, clipped, on
            // guard; holds nothing the street says of Mickey or his business.
            ["june"] = new Dictionary<string, string[]>
            {
                ["recognition/sensitive"] = new[]
                {
                    "Whatever you've got yourself into, I don't want to hear it. Well. Go on, then.",
                    "You've got this street talking already. Took me years to get away from it.",
                },
                ["recognition/police-heard"] = new[]
                {
                    "Police, now. I came back for a funeral, not this.",
                    "Sort out whatever the police want before I go home, would you.",
                },
                ["recognition/taken-heard"] = new[]
                {
                    "I'm not asking what the police wanted you for. I'm just saying I know.",
                    "You get yourself arrested, and I'm the one getting looks in the street. Thanks.",
                },
                ["recognition/avoids"] = new[]
                {
                    "Not now. I've a train to see about.",
                    "I'm not stopping.",
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
