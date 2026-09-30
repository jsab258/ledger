# What an hour of conversation costs, from real calls (2026-09-30)

Made by tools/talk_cost_sample.py: the game's own talk program, started as the game starts it, with the real key; three conversations of eight turns (Sheila, Ron, Darren). Its own cost report at the game's rate card (US dollars):

- turns: 24 (answered offline: 0); calls: 97
- the session: US$0.3973; per turn: US$0.01655
- an hour of steady talk at 120 turns (one every 30 seconds): **US$1.99**; at 60 turns: US$0.99; at 180: US$2.98
- median time to the reply: 5.8 s
- with --early, as the game runs it: a first sentence heard in 21 of 24 turns, median 2.0 s, slowest 6.1 s
- how the turns went: brush 2, ended 1, fallback 1, own 20
- each step's end, median from the turn's start: draft 2.2 s (24 turns), check 4.9 s (21 turns), redraft 7.4 s (2 turns)

Tokens by model:

```
claude-sonnet-5: 8 calls, 34499 in / 347 out tokens
claude-haiku-4-5: 89 calls, 291652 in / 6632 out tokens
Estimated total: US$0.3973
```

The turns, what was said and what came back:

- lena: "Morning. You keep the books for Mickey's?" -> "Thirty-one years." (6.9 s, first sentence 3.9 s, own)
- lena: "How long have you worked here?" -> "Just told you. Thirty-one years." (8.4 s, first sentence 2.4 s, own)
- lena: "What was Mickey like to work for?" -> "Fair." (9.5 s, first sentence 1.4 s, own)
- lena: "Did you hear anything about the break-in on Quay Street?" -> "No break-in I've heard of. What are you asking me for, you think I keep a diary of every window that's been put through round here?" (5.8 s, first sentence 2.4 s, own)
- lena: "Who do you think did it?" -> "I told you, I've not heard of one. Can't tell you who did something I don't know happened. If there's a window gone somewhere, that's the first I'm hearing of it." (3.8 s, first sentence 2.3 s, own)
- lena: "Would you tell the police if you knew?" -> "Depends who's asking and what they're after." (12.9 s, first sentence 2.2 s, own)
- lena: "Is there anything you need doing round the office?" -> "Later. I'm in the middle of something." (8.0 s, brush)
- lena: "Right. I'll leave you to it. Thanks, Sheila." -> "That's new management. Mind the step going out, it's uneven." (7.3 s, first sentence 6.1 s, ended)
- rocco: "Alright, Ron. Quiet tonight?" -> "You've had the lot off me, friend." (7.4 s, fallback)
- rocco: "How long were you on the docks?" -> "Thirty years. Rain never once asked how I was doing." (4.7 s, first sentence 2.6 s, own)
- rocco: "What happened when the scheme ended?" -> "Mickey kept me on for the door and the rank. Better than the street, wasn't it. Since he went, I've stayed on out of habit, I suppose. Money's always a little short, but the rank's still here and I know the street." (8.2 s, first sentence 2.9 s, own)
- rocco: "Anybody been hanging about the rank who shouldn't be?" -> "Not that I've clocked, no. You get the usual faces round here, Darren's always on his rounds, the drivers come and go. Nothing's stuck out at me as off, if that's what you're asking." (4.1 s, first sentence 1.8 s, own)
- rocco: "I heard something happened on Quay Street. Did you see it?" -> "What sort of something? I'm out there most hours, but you've got to be specific. What are people saying happened?" (4.2 s, first sentence 1.5 s, own)
- rocco: "What would you do if you found out who it was?" -> "Depends what it was, doesn't it. And depends who's asking, and what they're paying. I keep the rank watched, that's all. Anything else, that's different money." (6.4 s, first sentence 1.6 s, own)
- rocco: "Do you trust Darren?" -> "Darren's alright." (6.3 s, first sentence 2.8 s, own)
- rocco: "Fair enough. See you later, Ron." -> "Right you are, boss. Keep your eyes open out there." (4.6 s, first sentence 1.7 s, own)
- sam: "Darren. What are you selling today?" -> "Nothing that's got a name yet, to be honest. But I'm listening, you after something particular, or you just making talk?" (3.6 s, first sentence 1.8 s, own)
- sam: "How much for a radio?" -> "I don't shift radios, mate." (4.9 s, first sentence 1.7 s, own)
- sam: "Where do you get your stuff from?" -> "Here and there. Depends what's moving, doesn't it. Someone's got something they need gone, someone else wants it, I'm the one in the middle knowing both of them. That's the trade." (3.8 s, first sentence 1.6 s, own)
- sam: "Have you heard about the break-in?" -> "Catch you on the way back." (8.1 s, brush)
- sam: "Somebody said they saw you near there." -> "Near where?" (5.0 s, first sentence 2.2 s, own)
- sam: "Can you find out who did it for me?" -> "Find out who did what, though? You're going to have to tell me what I'm listening for, aren't you. And near where, that matters too." (3.1 s, first sentence 1.6 s, own)
- sam: "What's it going to cost me?" -> "Depends what you want knowing, doesn't it." (4.7 s, first sentence 2.0 s, own)
- sam: "All right. Don't do anything stupid." -> "I'm not the one doing stupid things, mate. I look after myself first, everybody knows that much. You want something found out, you tell me what it is and I'll say if I can help or I can't. That's how it works." (3.1 s, first sentence 1.8 s, own)
