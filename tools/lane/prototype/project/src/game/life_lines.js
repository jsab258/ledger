// LEDGER, the whole game: lines the street says unprompted, written ahead (DESIGN section 11). Greetings by regard
// and by the rung Tom has reached (2.12.4: how the rise is heard), the crowd's lines by situation and kind of
// speaker (3.6.4: at least six a situation a kind), and the calendar's days. About seven words a line.
// No drink, no gambling, no children, no real people or brands; nothing later than 1990.
// {name} is what this person calls him (the new owner, Nowak, Tom, Tommy).

// greetings by regard, then by rung: nephew (the new owner), owner (Nowak), firm (Tom), port (Tom, Tommy to a few)
export const GREET_BY = {
  afraid: {
    nephew: ['Not looking for trouble, me.', "I've seen nothing. Honest.", 'Morning. I was just going.'],
    owner: ['Mr Nowak. I was just off.', 'No bother from me, Mr Nowak.', "I've said nowt to nobody."],
    firm: ['Tom. All quiet. All quiet.', "Whatever you heard, it wasn't me.", 'I keep out of it, Tom.'],
    port: ["Tom. Anything you need, say.", 'I never saw you. As usual.', "We're all right, aren't we, Tom?"],
  },
  angry: {
    nephew: ["You've a nerve, coming down here.", 'Mickey would be ashamed.', "Don't speak to me."],
    owner: ["I know what you did, Nowak.", 'Keep walking, Nowak.', "Nowak. Still here, are you."],
    firm: ["Don't you 'morning' me, Tom.", "You'll get yours, Tom. Folk talk.", 'Big man now, are you.'],
    port: ['The whole Hook, and still not enough.', 'I remember you with one suitcase.', "Nobody's forgotten, Tom."],
  },
  likes: {
    nephew: ["Now then. You'll be Mickey's lad.", 'Settling in? Good.', 'Mind how you go, love.'],
    owner: ['Morning, Mr Nowak.', "Nowak. You're doing all right.", 'Looking after that office, I see.'],
    firm: ['Morning, Tom.', "Tom. Good to see you about.", 'Now then, Tom. Busy?'],
    port: ['Morning, Tom. After you.', 'Tom. Anything doing, you say.', "Tommy. They're asking for you up top."],
  },
  appearance: {
    nephew: ["That's a shiner you've got.", 'You want that lip looked at.', 'Walked into a door, did you?'],
    owner: ['Rough night, Mr Nowak?', "Somebody's marked you, Nowak.", 'That wants a stitch, that.'],
    firm: ['Who did that to you, Tom?', "I'd not like to see the other feller.", 'Tom. Your face.'],
    port: ["Nobody'd dare, I thought.", 'Tom. Who was daft enough?', "Say the word and it's seen to."],
  },
  neutral: {
    nephew: ['Morning.', 'Now then.', "You'll be the new owner.", 'Aye.'],
    owner: ['Morning, Nowak.', 'Mr Nowak.', 'Now then.'],
    firm: ['Morning, Tom.', 'Now then, Tom.', 'Tom.'],
    port: ['Tom.', 'Morning, Tom. After you.', 'Mr Nowak. Go on through.'],
  },
};
// The crowd, by situation and kind of speaker: om older man, ow older woman, ym younger man, yw younger woman.
export const CROWD_LINES = {
  bump: {
    om: ['Steady on, lad.', 'Mind where you put yourself.', "Pavement's wide enough for two.", 'Easy. Easy.', 'In a hurry, are we?', "You'll have me over."],
    ow: ['Mind my bag, love.', 'Excuse me, I am sure.', 'Watch where you are going.', 'Well. Manners.', 'Do you mind?', 'I am walking here, thank you.'],
    ym: ['Watch it, pal.', 'Oi. Look up.', 'You blind?', 'Steady, mate.', 'Easy, chief.', 'Mind the jacket.'],
    yw: ['Do you mind?', 'Watch it.', 'Oh. Sorry. No, you, actually.', 'Look where you are going.', 'Careful.', 'Charming.'],
  },
  neighbours: {
    om: ['Now then, Arthur.', 'Aye, not so bad. Yourself?', 'Still here, then.', "Seen owt of your lad?", 'Cold enough for you?', 'Same again tomorrow, I expect.'],
    ow: ['Morning, love. How is your mother?', 'Did you get your washing in?', 'I will knock later.', 'Have you seen the price of fish?', 'Is he no better?', 'Tell her I was asking.'],
    ym: ['Alright.', 'Any work going?', 'See you down there.', 'You hear about the dock?', "Foreman pick you? No. Nor me.", 'Later, pal.'],
    yw: ['Hiya. You off up the Row?', 'Is your Julie in?', 'I will ring you. Well. I will knock.', 'Have you seen what she is wearing?', 'Save us a seat.', 'Ta-ra, then.'],
  },
  working: {
    om: ['Forty year I have swept this step.', 'Where has that pencil gone.', 'Two and two is never five.', 'Should have retired when I said.', 'This lock wants oil.', 'Right. What was I doing.'],
    ow: ['Now where did I put it.', 'Half five cannot come soon enough.', 'Dust, dust, and more dust.', 'I only mopped this an hour ago.', 'One of these days.', 'There. That is straight.'],
    ym: ['Come on, come on.', "Boss'll have my hide.", 'Nearly. Nearly. There.', 'Who moved my flask?', 'Roll on Friday.', 'Not my job, this.'],
    yw: ['Hang on. Hang on.', 'That is not right. Count again.', 'Roll on dinner time.', 'Where is the other one?', 'Honestly.', 'Done. Next.'],
  },
  rain: {
    om: ['Rain again. There is a surprise.', 'Good for the ducks, this.', 'It will not stop for us.', 'I have known it worse. Not often.', 'Sideways, now. Lovely.', 'My knee said rain.'],
    ow: ['I have washing out in this.', 'Wet through, and only to the shop.', 'Never an umbrella when you want one.', 'It gets in your bones.', 'I will catch my death.', 'Look at it coming down.'],
    ym: ['Soaked. Absolutely soaked.', 'Typical.', 'No bus, no hood. Champion.', 'It is in my boots.', 'Run for it.', 'Who would live here?'],
    yw: ['My hair. Look at it.', 'I am not dressed for this.', 'It was dry when I set off.', 'Run. Run.', 'Is that bus never coming?', 'Drowned. I am drowned.'],
  },
  greet: {
    om: ['Morning.', 'Now then.', 'Aye.', 'How do.', 'Grand day. Well. A day.', 'Keeping busy?'],
    ow: ['Morning, love.', 'Hello, dear.', 'Turned out cold.', 'Morning.', 'Mind how you go.', 'Lovely to see a new face.'],
    ym: ['Alright.', 'Now then.', 'Y\'alright, pal.', 'Morning.', 'Aye aye.', 'Easy.'],
    yw: ['Hiya.', 'Morning.', 'Hello.', 'Alright?', 'Hi.', 'Cold, isn\'t it.'],
  },
};
// The calendar's days, said on the street (A20). The club and the paper are invented.
export const CALENDAR_LINES = {
  market: ['Thursday. Everybody is up the Row.', 'Market day. You could shout down here.', 'I am off up the market before the best has gone.', 'Quiet. It is always quiet of a Thursday.', 'Get your veg off the stalls, not the shop.', 'She will be up the market till three.'],
  match: ['Up the Town!', 'Three o\'clock kick-off. Come on.', 'We were robbed. Robbed.', 'Two nil. Do not ask.', 'Town at home today. Street will be full.', 'Never a penalty, that.'],
  sunday: ['Everything shut. Sunday.', 'Chapel was full this morning.', 'Day of rest. For some.', 'You will get nothing today but the caff.', 'Father Walsh went on a bit.', 'Sunday. Listen to it. Nothing.'],
  bonfire: ['Are you coming down the quay for the fire?', 'They light it at seven.', 'Harbour Board put on a good show.', 'Mind the sparks on that coat.', 'Best view is by the bollards.', 'Oooh. Look at that one.'],
  remembrance: ['Eleven o\'clock at the chapel.', 'I have my poppy.', 'Wreath goes on the stone at eleven.', 'My father is on that stone.', 'Two minutes. It is not much to ask.', 'They will read the names.'],
};
// Own street lines for the regulars who had none of their own (3.2.3, 3.6.3): a first set, to grow to thirty each.
export const OWN_STREET = {
  june: ['I am only here for the photographs.', 'Friday. Then I am gone.', 'He never wrote, you know.', 'This street has not changed. I have.', 'Do not ask me about the office.', 'I had forgotten the smell of the quay.', 'My train will not wait.', 'He kept my school reports. Imagine.'],
  pauline: ['Car one, where are you, love?', 'Two minutes means ten. Tell them ten.', 'I can hear the whole town from this chair.', 'Kevin never answers first time.', 'Station run, any car.', 'Hold the line, love.', 'I know every address by its voice.', 'Quiet. Too quiet for a Friday.'],
  kevin: ['Clutch is going on car one.', 'I do days. Nights is Terry.', 'Fish dock at dawn. Every dawn.', 'She never tips, that one.', 'Roads are greasy. Mind the setts.', 'I could drive this town blind.', 'Ask Pauline. I only drive.', 'Dock gate wanted money off me again.'],
  terry: ['Nights are when you see it all.', 'I say nowt and I drive.', 'Last ferry, then the stragglers.', 'Lamp is out on the landing again.', 'Had a runner Tuesday. Fast lad.', 'Dark by five now.', 'Quiet tonight.', 'I sleep when it is light.'],
  rita: ['Everything in here was somebody\'s.', 'I do not ask where. I ask how much.', 'Bring it round the side.', 'Looking costs nothing. Touching does.', 'Wayne. Wayne! Where is that lad.', 'Gold is gold. The rest is talk.', 'I close at six sharp.', 'You would be surprised what folk part with.'],
  wayne: ['Rita pays me Fridays.', 'I am just minding the back.', 'Not in the window, that. Under it.', 'You following?', 'Cash, pal.', 'I never saw who brought it.', 'Back in five minutes.', 'Ask Rita. I only carry.'],
  brenda: ['Crab is fresh. Landed at five.', 'Up at four, me. Every day.', 'Kippers, love? Go on.', 'The dock is not what it was.', 'Kevin runs me down at dawn.', 'I see who is about early.', 'Mind the ice on the step.', 'Half price after three.'],
  lee: ['Foreman never picked me.', 'I am on the casual. When there is any.', 'Ask at the gate. Not me.', 'I can look after myself.', 'Cammack\'s lot pay regular. Just saying.', 'Dock is finished. Everybody knows.', 'What are you looking at?', 'I owe who I owe.'],
  lily: ['Ten minutes for anything hot.', 'Salt and vinegar?', 'Peter is in the back.', 'We came in seventy-four.', 'Busy at eleven. Always eleven.', 'Open till late. Later than anyone.', 'Next, please.', 'Mind, it is hot.'],
  hal: ['We are between stock.', 'Coins tell you who has been through a port.', 'I buy, mostly. I seldom sell.', 'Come back Tuesday.', 'That is a Victorian penny. Worth a penny.', 'I keep the back locked.', 'Nobody collects any more.', 'Mind the cabinet.'],
  nora: ['Ah, it is yourself.', 'I do the flowers at the chapel.', 'God is good, and the bus is late.', 'I knew your uncle to nod to.', 'Father Walsh has a cold. I told him.', 'I see everything from the bus stop.', 'Say one for me.', 'Thursday I go up the market.'],
  sylvia: ['Feet. Mat. Thank you.', 'Rent is Friday. Friday means Friday.', 'I lock up at eleven.', 'I hear who comes in after.', 'No visitors in rooms.', 'Mr Rennison would not have stood for it.', 'Breakfast is at seven. Not after.', 'I run a clean house.'],
  julie: ['Hiya.', 'I have been on nothing since June.', 'I can drive. I passed first time.', 'Is there any work at yours?', 'Mam is at the window again.', 'Everything is shut or shutting.', 'I am not hiding. I am just broke.', 'Ta-ra, then.'],
  danby: ['I taught half this street. It shows.', 'The school is shut. I am not.', 'A book and a bench. That is my day.', 'Father Walsh wants the hall painted.', 'I was told you were the nephew.', 'One pot of tea, and I make it last.', 'You notice things, sitting still.', 'Good afternoon. It is, nearly.'],
};
const SPEAKER = (P) => ((P.def && P.def.age >= 55) || (P.look && P.look.old) ? 'o' : 'y') + ((P.def && P.def.sex) === 'f' ? 'w' : 'm');
export const speakerKind = SPEAKER;
export const allNewLines = () =>
  [GREET_BY, CROWD_LINES].flatMap((t) => Object.values(t).flatMap((k) => Object.values(k).flat())).concat(Object.values(CALENDAR_LINES).flat(), Object.values(OWN_STREET).flat());
