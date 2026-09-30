# The six named characters' street lines, third version: every bank written
# for all six side by side, each from what that character wants (Darren trades,
# Sheila withholds, Alison wants the story, Ada judges and remembers, Walsh cares
# and asks nothing, June keeps her distance). Emits C# for OwnLines.ByCast.
import json

HEAD = {
    'sam': '''            // DARREN MILNER (production/casting/darren-milner/SHEET.md; the card, sam.md):
            // 25, the street's hustler, out of work since a youth training scheme,
            // at his mother's, a pager and the phone boxes; quick, ingratiating,
            // never still; always halfway into a favour or out of one; "so listen"
            // once, when he has something to sell; "mate" to anybody; trades in
            // what he has heard, and cheerfully spineless about it.''',
    'lena': '''            // SHEILA DUNN (production/casting/sheila-dunn/SHEET.md; the card, lena.md):
            // 53, Mickey's bookkeeper thirty-one years, a widow in a council flat;
            // low, dry, unhurried, withholding judgement; short sentences, deadpan;
            // "love" to a neighbour; to Tom's face no name and no "new management"
            // (the talk gives her that until she trusts him, then his name);
            // nothing of the firm's takings or the real book. She meets him on his
            // walk-round, so she has no arrival lines.''',
    'noor': '''            // ALISON SEDMAN (production/casting/alison-sedman/SHEET.md): 30, a
            // reporter on the town's evening paper, local; bright and quick, a
            // reporter's neutral politeness over it; wants the story, and knows
            // people tell her more when she does not push.''',
    'ada': '''            // ADA (production/casting/ada/SHEET.md): 78, a widow who keeps a
            // window on Quay Street, her step across from Mickey's; thin, old and
            // sharp, broad local; judges, and remembers rather than gossips; "love"
            // now and then; promises nobody her silence; nothing of Mickey she was
            // not given (his character is Jafar's).''',
    'emil': '''            // FATHER BRENDAN WALSH, Father Walsh to the street (production/casting/
            // father-emil/SHEET.md; the id stays emil): about 61, the Irish-born
            // parish priest; soft and slow, Irish in his turn of phrase; never asks
            // where people have been, asks whether they are all right; religion part
            // of life, never pressed, and sparing; never afraid for Tom, never a hint
            // of what he holds in confidence.''',
    'june': '''            // JUNE SUDDABY (production/casting/june/SHEET.md): 38, Mickey's
            // estranged daughter, born in the Hook and gone young, back for the
            // funeral; quick and clipped, the accent worn down; not stopping long;
            // no feelings shown about her father or what becomes of his business
            // (unwritten backstory); family, so no arrival lines.''',
}

B = {}
def bank(name, **by):
    B[name] = by

# EVERYDAY, to a neighbour.
bank('ambient/open/ordinary',
     sam=["Alright? What's the word your end?", "Busy, are you?", "Anything going, mate? Anything at all?",
          "Heard anything worth hearing?", "Pager's not gone off once.", "Want anything? I'm not selling. Just asking.",
          "Every phone box on this street's broke but one.", "Seen anybody about? Anybody interesting?",
          "Know anybody after a radio?", "Doing all right, are you?", "I've been up and down this street that many times I've lost count.",
          "Can you change a fiver? No? Never mind.", "Fish market's always heaving first thing.", "I've walked my legs off.",
          "Go on then, what's new? Everybody's got something.", "So listen. Anything you need, mates' rates."],
     lena=["Keeping well, love?", "Another week gone.", "The phone's not stopped.", "I've a pile of post to get through.",
           "Another letter from the council.", "Another bill in the post.", "The rank's not busy.", "Council's sent another form.",
           "Same as yesterday.", "You look tired, love.", "Still at it, love?", "It's cold in the office. Always is."],
     noor=["Nothing on this street makes the paper. Not often.", "Same faces every day. I like that.",
           "The paper's short of stories this week.", "I like to hear a thing twice before I believe it.",
           "I've walked this street end to end and learned nothing.", "You'd be surprised what people tell me.",
           "Deadline's always an hour ago.", "I've three stories on the go and none of them stands up.",
           "Everybody's got a story. Most won't tell it.", "Busy on the paper this week."],
     ada=["Now then. Where are you off to, love?", "That wind'll find you.", "Another day.", "My hip's giving me what for.",
          "Same faces up and down.", "My chest's bad again.", "You look worn out, love."],
     emil=["God bless. How are you keeping?", "You're looking well.", "Are you all right, yourself?", "It's a raw one today.",
           "I'm up and down this street all hours.", "Stop a minute and tell me how you are."],
     june=["I'd forgotten the wind off the water.", "Same street. Nothing changes.", "It's colder than I remembered.", "I'm only passing."])
bank('ambient/reply/ordinary',
     sam=["Ducking and diving, mate.", "Busy busy. You know me.", "Hanging on, mate.", "Could be worse. Could be working.",
          "Keeping my head down.", "Ticking over, mate.", "Can't complain. Well, I can. I won't.", "Up and down, mate. Mostly up.",
          "Flat out, me. Doing what, don't ask.", "All the better for seeing you.", "Skint, but smiling.", "Busier than I look.",
          "Knackered, mate. Honest work, that's why.", "Rushed off my feet.", "Surviving, mate.", "Same old story, mate.",
          "Never better. Never worse, either.", "Earning, mate. A bit."],
     lena=["Much the same, love.", "I've known worse.", "Can't say I'm bad.", "Well enough.", "Tired, love. Same as everyone.",
           "Keeping busy.", "Middling, love.", "No worse than usual."],
     noor=["Busy. Chasing a man who won't ring back.", "Tired, but I'll live.", "Better for the walk.", "Up to my ears, as usual.",
           "Mustn't complain. I'm paid to listen.", "Fine, thanks. Nothing to report.", "Getting there.", "Plodding on, thanks."],
     ada=["Could be worse.", "Keeping going.", "Oh, you know, love.", "Much as ever.", "I'm still here.", "No worse than yesterday."],
     emil=["Ah, sure. We keep going.", "Ah, sure, it's hard going.", "It could be worse, I suppose.", "We'll see how it goes.",
           "Grand, thanks. Grand.", "We manage, thank God."],
     june=["No different.", "Can't complain.", "Not bad.", "Right."])
bank('ambient/open/night',
     sam=["Late one, this.", "You out as well? Thought it was just me.", "Street's dead. Good time for a chat.", "Freezing, this.",
          "Nobody about but us and the gulls.", "Night crowd's thin.", "Last phone box on the corner's still working. Just.",
          "You hear things at night you don't hear in the day."],
     lena=["Late, love.", "I should have been home an hour since.", "Everyone's in by now."],
     noor=["Still got copy to finish.", "It's another town at night.", "Only the gulls up now."],
     ada=["Late to be about, love.", "Everybody's in but us."],
     emil=["You're out late. Is everything all right?", "The street's gone quiet."],
     june=["Street's quiet now.", "Cold now, isn't it."])
bank('ambient/reply/night',
     sam=["Night's the best time, mate. Nobody asks.", "Can't sleep. Never could.", "I'm off in a bit.", "Keeps you honest, the cold.",
          "Right. Watch yourself.", "Out and about, same as you.", "Anything happens, I'll hear of it."],
     lena=["Just finishing up.", "Watch the kerb, love.", "Home, love. It's late."],
     noor=["Just heading back.", "I'll have it written before the desk's in.", "Mind yourself going home."],
     ada=["Home you go, love.", "Watch your feet. It's black out."],
     emil=["I'm on my way home myself.", "God keep you."],
     june=["I'm going in.", "Night."])
bank('ambient/open/slump',
     sam=["Nobody's buying nothing. Nothing.", "Trade's that dead I'm giving stuff away.", "Can't shift anything, mate.",
          "I've had one sale all week and that was me mother."],
     lena=["The cabs are sat idle.", "Nobody's ringing for cabs."],
     noor=["Half these shops won't see the new year.", "Another shutter down this week."],
     ada=["Street's not what it was.", "Half the shops shut up."],
     emil=["Times are hard on this street.", "The collection's light these weeks."],
     june=["It's worse than when I left.", "Half of it's boarded up."])
bank('ambient/reply/slump',
     sam=["Tell me about it. Tell me anything.", "It'll pick up. It always does. Doesn't it?", "I'll find a way. I always find a way.",
          "Money's about. It's just not mine."],
     lena=["It'll turn. Or it won't.", "I've kept books through worse.", "Money's gone out of this street."],
     noor=["Somebody should write that. Maybe me.", "It's the same all over the town."],
     ada=["It'll come back. I won't see it.", "I remember when this street was full."],
     emil=["We'll get through it.", "People are kind when it's hard."],
     june=["I'm not surprised.", "It'll get worse yet."])
bank('ambient/open/prices',
     sam=["Everything's gone up again, mate. Everything.", "Twenty pence more at the kiosk. For nothing.",
          "Can't afford to be poor these days.", "They want a fortune for a pair of jeans now."],
     lena=["The electric's gone up again.", "Stamps have gone up.", "The phone bill's gone up."],
     noor=["My rent's up and my pay's not.", "The bus fare's up again."],
     ada=["Pension doesn't go far.", "Bread's dear, love."],
     emil=["It's hard on the old people, the prices.", "The coal's gone up again, they tell me."],
     june=["Everything's dear.", "Everything's gone up since I was here."])
bank('ambient/reply/prices',
     sam=["I know a bloke. Cheaper. Ask me later.", "Daylight robbery, that.", "Cash, mate. Cheaper that way.",
          "Nobody pays full price. Not if they know me."],
     lena=["I've stopped adding it up.", "Everything but the wages."],
     noor=["I've stopped looking at the till.", "My purse agrees with you."],
     ada=["I make do.", "Everything but my pension."],
     emil=["Isn't it desperate.", "It's hard on people."],
     june=["It's no better anywhere.", "Don't start me."])
bank('ambient/open/injured',
     sam=["Don't look at me like that. Door jumped out at me.", "Bit of bother. Sorted now.", "Had a disagreement. I lost."],
     lena=["I caught it on the filing cabinet.", "It's only a bruise."],
     noor=["It's nothing. I tripped on the kerb.", "Don't ask. I'm fine."],
     ada=["My knees, love. Don't ask.", "I had a fall. I'm fine."],
     emil=["I'm grand. An old man's knees.", "I bumped myself. It's nothing to speak of."],
     june=["It's nothing.", "I'm fine. Leave it."])
bank('ambient/reply/injured',
     sam=["You want to get that looked at, mate.", "Who did that? Just asking.", "You're a funny colour, mate."],
     lena=["You want that seeing to, love.", "Doctor. Don't argue."],
     noor=["That wants a doctor.", "Let me get somebody."],
     ada=["Rest yourself a minute.", "You want that looking at, love."],
     emil=["You'll want that seen to.", "Sit a minute. Nobody minds."],
     june=["Get it seen to.", "You're white as a sheet."])
bank('ambient/open/feud',
     sam=["Oh. It's you.", "I'm not talking to you.", "Don't start."],
     lena=["Go on. I've said my piece.", "We've said all there is to say."],
     noor=["Not you again.", "I've nothing more for you."],
     ada=["I've said all I'll say to you.", "Go on. Off with you."],
     emil=["I've nothing unkind to say, so I'll say nothing.", "I won't quarrel with you in the street."],
     june=["Leave me be.", "Don't."])
bank('ambient/reply/feud',
     sam=["Please yourself, mate.", "Whatever you say.", "Fine by me."],
     lena=["If you like.", "So be it."],
     noor=["If that's how it is.", "Noted."],
     ada=["Have it your way.", "We'll see who's sorry."],
     emil=["If that's how you want it.", "Some other time, so."],
     june=["Fine.", "Your choice."])
bank('ambient/open/justnow/glass',
     sam=["That's a window going in.", "Hear that? Glass."],
     lena=["That's a window gone.", "Glass. That'll cost somebody."],
     noor=["That was glass.", "Somebody's lost a window."],
     ada=["Glass. I heard it go.", "There goes a window."],
     emil=["There's glass broken somewhere.", "A window's gone. God help them."],
     june=["Somebody's put a window in.", "Hear the glass?"])
bank('ambient/open/justnow/shout',
     sam=["Somebody's lost their rag.", "There's bother down there."],
     lena=["Somebody's making a show of themselves.", "Listen to that racket."],
     noor=["That's somebody's temper.", "Somebody's having a row."],
     ada=["Somebody's carrying on.", "Hark at that shouting."],
     emil=["Someone's in trouble.", "Someone's raising their voice."],
     june=["Who's shouting?", "There's a row on somewhere."])
bank('ambient/open/justnow/crash',
     sam=["Big one, that.", "Something's toppled over."],
     lena=["What on earth was that?", "Something heavy's gone."],
     noor=["That sounded bad.", "Did something fall?"],
     ada=["That's come down with a bang.", "That was a bang."],
     emil=["That was a fall, surely.", "Something's fallen."],
     june=["Something's gone over.", "What's fallen?"])
bank('ambient/open/justnow/noise',
     sam=["Hang about. What was that?", "Something's going on."],
     lena=["Hush a minute. Listen.", "What's all that?"],
     noor=["Listen. Hear it?", "What's that noise?"],
     ada=["What in the world was that?", "Did you hear that go?"],
     emil=["Listen. What's that?", "Did something happen?"],
     june=["Hear that?", "What's that?"])
bank('ambient/reply/justnow',
     sam=["Not my business, that.", "Not my patch, mate.", "I'll know who by tomorrow."],
     lena=["Let somebody else go.", "I'm not going down there."],
     noor=["I'd better go and see.", "Somebody will have rung it in."],
     ada=["I'm too old to go running.", "It's none of mine."],
     emil=["I'll go and see is anyone hurt.", "Let's hope nobody's hurt."],
     june=["Not my business.", "Leave it."])
bank('ambient/open/settling',
     sam=["That's that, then.", "All over now.", "Quiet as you like now."],
     lena=["Hush. It's stopped.", "That's the end of that, then."],
     noor=["Quiet again. For now.", "All quiet. Funny how quick."],
     ada=["All quiet now, love.", "That's done, then."],
     emil=["It's passed now.", "All's still again."],
     june=["Quiet again.", "It's over."])
bank('ambient/reply/settling',
     sam=["I'll have the whole story soon enough.", "Somebody'll tell me. They always do.", "Give it an hour, it'll be all round."],
     lena=["Least said, love.", "We'll hear soon enough."],
     noor=["Somebody will want to tell me about that.", "I'll hear the rest."],
     ada=["I'll remember it.", "It'll not be forgotten."],
     emil=["The street will talk.", "I'll look in on people later."],
     june=["That'll be talked about.", "There'll be a story."])

# TO TOM'S FACE, written side by side.
bank('recognition/ordinary',
     sam=["Alright, mate? Just passing. Always am.", "Mate. Anything you need, give us a shout.", "There he is. The man himself."],
     lena=["Office is open. It usually is.", "Post's on the desk.", "You know where the desk is."],
     noor=["Hello. How's the new job?", "I'm around, if you want to talk.", "Anything you'd like to tell me? No? Fine."],
     ada=["Hello, love.", "You're keeping busy.", "Go careful now."],
     emil=["Good to see you, young man.", "You're finding your feet, I hope.", "Go easy now."],
     june=["You.", "It's you."])
bank('recognition/arrival-saw',
     sam=["Clocked you the minute you turned up, mate. Darren. You'll have heard of me.", "Big case for a short stay, is it? Darren. I get things."],
     noor=["I noticed you arriving. Alison Sedman. The evening paper.", "New face on the street. Alison Sedman. I write for the paper."],
     ada=["Came up with your case, didn't you? I watched from the window. I'm Ada.", "Ada. From across the road. I saw you arrive."],
     emil=["I saw you arrive. Father Walsh. I'm sorry for your trouble.", "Welcome to the Hook. Father Walsh."])
bank('recognition/arrival-heard',
     sam=["So you're the new owner. Word gets round, mate. Darren.", "Mickey's nephew, is it? Darren. Anything you want, I'm your man."],
     noor=["Mickey's nephew, isn't it? Alison Sedman. I'm not writing about you.", "Word travels fast here. Alison Sedman. I'm on the paper."],
     ada=["You're the nephew they're all on about. I'm Ada.", "I'm Ada. That's my step, across from Mickey's."],
     emil=["They told me you'd come. Father Walsh. I'm sorry for your trouble.", "Father Walsh. If you need anything at all, ask."])
bank('recognition/sensitive',
     sam=["Your ears burning, mate? They should be.", "People are saying things about you. I'm only the messenger."],
     lena=["I'm hearing things about you in the office.", "Whatever they're saying, I'd keep to the office a day or two."],
     noor=["Your name's come up more than once.", "Somebody's been talking about you. I haven't written it down."],
     ada=["They're on about you. I remember what I hear.", "Mind yourself. The street's got your name."],
     emil=["People are talking. Are you all right?", "I've heard your name more than I'd like."],
     june=["They're talking about you now.", "Same street. New name to talk about."])
bank('recognition/confronts',
     sam=["Need a word, mate. Quiet, like.", "Hang on. You and me need a chat."],
     lena=["Come into the office. I want a word.", "Sit down when you get in. We're talking."],
     noor=["Have you got ten minutes? I'd rather not do this in the street.", "I'd like a word. Off the record."],
     ada=["Don't walk past my step. I want a word.", "Come here. I've something to say to you."],
     emil=["Stop a minute. I don't like what I'm hearing of you.", "Walk with me a minute, young man."],
     june=["Stop. I want to say something.", "We should talk."])
bank('recognition/refuses',
     sam=["Can't help you, mate. Not with that.", "Nothing doing. Sorry."],
     lena=["That's not mine to give.", "No. Ask me something else."],
     noor=["That's not something I can do.", "I can't. Sorry."],
     ada=["No, love. Whatever it is.", "I'm too old for favours."],
     emil=["I'd rather not, if it's all the same to you.", "I can't do that for you."],
     june=["No.", "Don't ask me."])
bank('recognition/avoids',
     sam=["Can't stop, mate. Places to be.", "Later, yeah? Later.", "In a rush. Catch you."],
     lena=["Later.", "I've the books to do.", "Not today."],
     noor=["Can't stop. Somebody's waiting on me.", "Later, maybe."],
     ada=["Not just now, love.", "Some other day."],
     emil=["Forgive me, I'm expected.", "Another time, young man."],
     june=["Not now.", "I'm going."])
bank('recognition/taken-saw',
     sam=["Watched them put you in the car, mate. Told a couple, mind.", "They let you go, then. I saw the whole thing."],
     lena=["I watched them take you. The office carried on.", "I saw the car. You're back."],
     noor=["I was there when they took you. I didn't write it.", "I saw it. Are you going to tell me why?"],
     ada=["I saw the police car. Whole street did.", "I watched them put you in. From my window."],
     emil=["They came for you in front of everybody. Are you all right?", "You're back. Good."],
     june=["Saw the police take you.", "Back already."])
bank('recognition/taken-heard',
     sam=["Word is the police took you in, mate.", "Heard you were down the station, mate."],
     lena=["You were at the station, I hear. The phones still rang.", "They took you to the station, I'm told."],
     noor=["It's not in the paper that the police had you. Not from me.", "Somebody says you were at the station."],
     ada=["They say you were took in.", "You've been at the station."],
     emil=["I heard they had you in. You're keeping well?", "They let you go, I'm told."],
     june=["Police had you, I heard.", "They had you down the station, I hear."])
bank('recognition/police-asked',
     sam=["Ellis collared me about you, mate. I played daft. I'm good at daft.", "That detective wanted you. Got nothing off me."],
     lena=["I was asked about you. The office hours are all she got.", "Ellis came by the office about you. I told her very little."],
     noor=["Ellis asked me about you. I asked her more than she asked me.", "DS Ellis wanted to know about you. I'd like to know why."],
     ada=["That detective was at my door about you.", "Ellis stopped at my step. She wanted you."],
     emil=["The detective called at the presbytery for you. I said you'd only just come.", "Sergeant Ellis was asking how you're getting on. I said you were new."],
     june=["She wanted you. I've been away too long to know anything.", "Ellis stopped me. I had nothing for her."])
bank('recognition/police-heard',
     sam=["Police are asking about you, mate. Thought you'd want to know.", "Detective's doing the rounds. Your name's on her list."],
     lena=["The police are asking after you, I hear.", "I'm told there's a detective about. Asking for you."],
     noor=["The police are interested in you. That usually means something.", "Somebody at the station's interested in you."],
     ada=["The police have been asking after you.", "They've a detective on the street, after you."],
     emil=["They're asking after you, I hear.", "I hear the police want a word."],
     june=["Police are curious about you.", "They're asking round about you."])
bank('recognition/threat-told',
     sam=["Steady on, mate. Scaring me's easy. Shutting me up's not.", "Whoa. No need for that."],
     lena=["Talk to me like that again and you can do your own books.", "I'll not forget that."],
     noor=["Say that again and my editor hears it.", "That's one I'll remember."],
     ada=["I'm seventy-eight. You'll not frighten me.", "Say that again and see where it gets you."],
     emil=["The door's still open, all the same.", "That's not the man I hoped you were."],
     june=["Don't threaten me. I'm not stopping long enough to care.", "Is that meant to frighten me?"])
bank('recognition/threat-heard',
     sam=["People say you've been heavy with folk, mate.", "Heard you've been putting the frighteners on people. Word travels."],
     lena=["I've heard you've been frightening people.", "It gets back to me when you frighten people."],
     noor=["Threatening people gets written down, you know.", "People tell me you've been threatening them."],
     ada=["Frightening folk's no way to start.", "Throwing your weight about, I hear."],
     emil=["I hear you've been hard on people. That's not the way.", "Frightening people, they tell me."],
     june=["So you're one of those now.", "People say you've been threatening them."])
bank('recognition/outfit-did',
     sam=["Mum's the word, mate. The landing.", "Heard you did Mickey's errand."],
     lena=["So you did the run. I'll say nothing.", "The landing, was it."],
     noor=["Down to the landing after ten, I'm told. Same as Mickey.", "Mickey's run, they say. I'd be careful."],
     ada=["You went down, then. Like Mickey.", "You did the landing. Mind how you go."],
     emil=["They're saying you did what Mickey did. I won't ask.", "I won't ask where you were."],
     june=["So you did the run. That's your lookout.", "Don't tell me about the landing."])
bank('recognition/outfit-refused',
     sam=["Brave, mate. Daft, but brave.", "Word is you sent them packing."],
     lena=["You told them no. Mind yourself.", "They'll remember your no."],
     noor=["Saying no to them takes nerve.", "You sent them a no, I'm told. I'd like to know who to."],
     ada=["Sent them off, did you? Good lad.", "They'll not like being told."],
     emil=["I hear you said no to them.", "You've made your choice, then."],
     june=["So it's no, then.", "Your business, not mine."])
bank('recognition/outfit-wounddown',
     sam=["Mickey's arrangement's gone, then. People will talk.", "All finished, I hear."],
     lena=["So it's done with. We'll see if it stays done.", "I'll believe it's over when they do."],
     noor=["Whatever Mickey had going, it's over, they say. I'd love to know what it was.", "So that's over. Whatever it was."],
     ada=["That's all finished, then. Well, well.", "So it's done."],
     emil=["That's done with, they say.", "So it's ended."],
     june=["Finished, is it. Nothing to do with me.", "Is it."])
bank('recognition/outfit-noshow',
     sam=["Heard you left them stood at the landing, mate.", "You never showed. That'll be remembered."],
     lena=["They were kept waiting, I hear.", "People like that keep count."],
     noor=["You didn't turn up at the landing, I'm told.", "Somebody waited for you. Who?"],
     ada=["You kept them waiting. That's not forgotten.", "They were stood at the landing for you."],
     emil=["You didn't go, I'm told.", "They waited, I hear. I won't ask."],
     june=["You never went.", "They were waiting on you, I hear."])
bank('recognition/week-winddown',
     sam=["Shutting down Mickey's other side, I hear. Shame. For some.", "Cabs only, is it?"],
     lena=["Cabs and nothing else, then. I've closed the book on it.", "Just the cabs. Simpler books."],
     noor=["Winding Mickey's down, I hear. The end of something.", "Only the cabs from now on? That's a story."],
     ada=["Letting it go, are you? Just the taxis.", "Mickey's other business, gone. Well."],
     emil=["It's to be the cabs only, I hear.", "You've let it go, then. That's your decision."],
     june=["So you're letting it go.", "Makes no odds to me."])
bank('recognition/week-takeover',
     sam=["Keeping the lot, mate? Big boots, them.", "The whole of Mickey's, I hear. You'll need friends. I'm a friend."],
     lena=["All of Mickey's, then. I hope you know what you've taken on.", "So you're keeping everything."],
     noor=["Taking it all on, they say. Brave.", "The whole business. That'll be a story one day."],
     ada=["Taking the lot on, I hear. I hope you know what you're about.", "That's a lot for one pair of hands, love."],
     emil=["You've a lot on your plate now, I'd say.", "You've taken a lot on."],
     june=["Rather you than me.", "I want none of it."])
bank('recognition/week-wontsay',
     sam=["Not telling Sheila, mate? Keeping it under your hat.", "Can't blame you. I'd not tell her either."],
     lena=["Still not saying. Then the street decides.", "You'll not tell me which. That's an answer too."],
     noor=["You're keeping everybody guessing.", "Not saying. I know the feeling."],
     ada=["Sheila won't thank you for that.", "Not saying, eh? She'll not ask twice."],
     emil=["That's between you and her.", "Keeping your own counsel. That's your right."],
     june=["You'll not tell her, then.", "Fair enough."])
bank('faint',
     sam=["That's Mickey's nephew, that.", "Word is he's alright. Word changes.", "Keep an eye on that one."],
     lena=["Too soon to say about him.", "That's him. The nephew.", "He's learning."],
     noor=["He's not what I expected.", "I'll find out about him.", "Mickey's nephew. Interesting."],
     ada=["That's Mickey's nephew.", "Something about him. I'll remember.", "We'll see what he's made of."],
     emil=["There goes Mickey's nephew.", "I'll call on him.", "He's new here yet."],
     june=["That's the nephew.", "He can have it."])

ORDER = ['sam', 'lena', 'noor', 'ada', 'emil', 'june']
out = []
for who in ORDER:
    out.append(HEAD[who])
    out.append('            ["%s"] = new Dictionary<string, string[]>' % who)
    out.append('            {')
    for name, by in B.items():
        if who not in by:
            continue
        lines = by[who]
        assert len(lines) >= 2 and len(set(lines)) == len(lines), (who, name)
        out.append('                ["%s"] = new[]' % name)
        out.append('                {')
        for l in lines:
            assert '"' not in l, l
            out.append('                    "%s",' % l)
        out.append('                },')
    out.append('            },')
open(r'C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-town\fcc1f54f-7060-4787-a3d7-468ba58b722f\scratchpad\own-v3.cs.txt', 'w', encoding='utf-8').write('\n'.join(out) + '\n')
json.dump(B, open(r'C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-town\fcc1f54f-7060-4787-a3d7-468ba58b722f\scratchpad\own-v3.json', 'w', encoding='utf-8'), indent=1)
print('ok', sum(len(v) for by in B.values() for v in by.values()), 'lines')
