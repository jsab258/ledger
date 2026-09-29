# What an hour of conversation costs, from real calls (2026-09-29)

Made by tools/talk_cost_sample.py: the game's own talk program, started as the game starts it, with the real key; three conversations of eight turns (Sheila, Ron, Darren). Its own cost report at the game's rate card (US dollars):

- turns: 24 (answered offline: 0); calls: 104
- the session: US$0.3568; per turn: US$0.01487
- an hour of steady talk at 120 turns (one every 30 seconds): **US$1.78**; at 60 turns: US$0.89; at 180: US$2.68
- median time to the reply: 4.1 s
- with --early, as the game runs it: a first sentence heard in 22 of 24 turns, median 1.7 s, slowest 4.1 s
- how the turns went: brush 1, ended 1, own 22
- each step's end, median from the turn's start: draft 1.9 s (24 turns), check 4.0 s (23 turns)

Tokens by model:

```
claude-sonnet-5: 8 calls, 31016 in / 303 out tokens
claude-haiku-4-5: 96 calls, 261252 in / 6094 out tokens
Estimated total: US$0.3568
```

The turns, what was said and what came back:

- lena: "Morning. You keep the books for Mickey's?" -> "Thirty-one years." (7.0 s, first sentence 4.1 s, own)
- lena: "How long have you worked here?" -> "Just told you. Thirty-one years." (4.8 s, first sentence 2.9 s, own)
- lena: "What was Mickey like to work for?" -> "Fair." (4.1 s, first sentence 1.9 s, own)
- lena: "Did you hear anything about the break-in on Quay Street?" -> "No break-in I've heard of." (4.1 s, first sentence 2.0 s, own)
- lena: "Who do you think did it?" -> "Told you, I've not heard of one. Can't have a view on something that didn't happen." (3.4 s, first sentence 2.3 s, ended)
- lena: "Would you tell the police if you knew?" -> "That depends what I knew, and who's asking." (4.5 s, first sentence 2.3 s, own)
- lena: "Is there anything you need doing round the office?" -> "Later. I'm in the middle of something." (8.0 s, brush)
- lena: "Right. I'll leave you to it. Thanks, Sheila." -> "Mm." (3.0 s, own)
- rocco: "Alright, Ron. Quiet tonight?" -> "It's the morning, friend." (4.1 s, first sentence 1.6 s, own)
- rocco: "How long were you on the docks?" -> "Thirty years. Rain never once asked how I was doing." (4.5 s, first sentence 2.3 s, own)
- rocco: "What happened when the scheme ended?" -> "Mickey kept me on for the door and the rank. Better than out on my arse, wasn't it. Since he went, I've stayed on out of habit more than anything else." (5.0 s, first sentence 2.7 s, own)
- rocco: "Anybody been hanging about the rank who shouldn't be?" -> "Not that I've seen." (4.4 s, first sentence 1.7 s, own)
- rocco: "I heard something happened on Quay Street. Did you see it?" -> "What kind of something? I'm out here most days, but you've got to tell me what I'm meant to have seen before I know whether I saw it or not." (2.6 s, first sentence 1.4 s, own)
- rocco: "What would you do if you found out who it was?" -> "Depend on who it was, wouldn't it. And what they did. I'm not interested in trouble that isn't paid for." (2.6 s, first sentence 1.6 s, own)
- rocco: "Do you trust Darren?" -> "Darren's alright." (3.7 s, first sentence 1.7 s, own)
- rocco: "Fair enough. See you later, Ron." -> "Right you are, boss." (3.4 s, first sentence 1.4 s, own)
- sam: "Darren. What are you selling today?" -> "Got nothing moving this morning, to be honest with you. Weather's kept people indoors. But I'm listening if there's something you need." (2.9 s, first sentence 1.7 s, own)
- sam: "How much for a radio?" -> "I haven't got a radio on me. You after one, or you've got one you're trying to move?" (3.1 s, first sentence 1.6 s, own)
- sam: "Where do you get your stuff from?" -> "Here and there." (8.7 s, first sentence 2.4 s, own)
- sam: "Have you heard about the break-in?" -> "What break-in? Where?" (2.6 s, first sentence 1.7 s, own)
- sam: "Somebody said they saw you near there." -> "Near where? You've got to tell me what you're on about first." (3.2 s, first sentence 1.7 s, own)
- sam: "Can you find out who did it for me?" -> "Listen, I'm not a detective." (3.4 s, first sentence 1.4 s, own)
- sam: "What's it going to cost me?" -> "Cost you for what?" (4.9 s, first sentence 1.2 s, own)
- sam: "All right. Don't do anything stupid." -> "I'm not going to do anything at all until you tell me straight what you want." (4.7 s, first sentence 1.5 s, own)
