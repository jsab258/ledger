# What an hour of conversation costs, from real calls (2026-09-30)

Made by tools/talk_cost_sample.py: the game's own talk program, started as the game starts it, with the real key; three conversations of eight turns (Sheila, Ron, Darren). Its own cost report at the game's rate card (US dollars):

- turns: 24 (answered offline: 0); calls: 103
- the session: US$0.4288; per turn: US$0.01787
- an hour of steady talk at 120 turns (one every 30 seconds): **US$2.14**; at 60 turns: US$1.07; at 180: US$3.22
- median time to the reply: 4.3 s
- with --early, as the game runs it: a first sentence heard in 22 of 24 turns, median 2.1 s, slowest 5.5 s
- with --pending: of those, 22 written ahead of their check, median 0.9 s, so the voice can start that much sooner (median 1.0 s)
- how the turns went: fallback 2, own 22
- each step's end, median from the turn's start: first-written 0.9 s (24 turns), first-passed 2.0 s (17 turns), draft 2.3 s (24 turns), check 4.2 s (21 turns), first-plain 2.2 s (4 turns), first-flagged 3.0 s (3 turns), re-first-written 4.2 s (3 turns), re-first-flagged 6.1 s (2 turns), redraft 5.5 s (3 turns), re-first-passed 5.5 s (1 turns), recheck 8.5 s (1 turns)

Tokens by model:

```
claude-sonnet-5: 9 calls, 41670 in / 369 out tokens
claude-haiku-4-5: 94 calls, 307972 in / 6761 out tokens
Estimated total: US$0.4288
```

The turns, what was said and what came back:

- lena: "Morning. You keep the books for Mickey's?" -> "Thirty-one years." (6.3 s, first sentence 3.4 s, own); steps: first-written 2.3, first-passed 3.3, draft 3.3, check 6.2
- lena: "How long have you worked here?" -> "Just told you. Thirty-one years." (4.2 s, first sentence 2.5 s, own); steps: first-written 1.8, first-passed 2.4, draft 2.4, check 4.2
- lena: "What was Mickey like to work for?" -> "Fair." (5.4 s, first sentence 2.1 s, own); steps: first-written 2.2, first-plain 2.2, draft 2.9, check 5.3
- lena: "Did you hear anything about the break-in on Quay Street?" -> "No. First I'm hearing of it. If something happened on this street, it didn't cross my desk." (6.5 s, first sentence 4.7 s, own); steps: first-written 4.7, first-plain 4.7, draft 5.1, check 6.4
- lena: "Who do you think did it?" -> "I don't guess." (4.7 s, first sentence 2.4 s, own); steps: first-written 1.3, first-passed 2.4, draft 2.4, check 4.7
- lena: "Would you tell the police if you knew?" -> "Depends who's asking and why. I've got no name to give you, so it doesn't come up." (3.9 s, first sentence 2.7 s, own); steps: first-written 2.0, first-passed 2.7, draft 2.7, check 3.9
- lena: "Is there anything you need doing round the office?" -> "That's the whole of it. The rest would be gossip." (6.2 s, fallback); steps: first-written 1.0, first-flagged 3.0, draft 3.0, re-first-written 4.3, re-first-flagged 6.1, redraft 6.1
- lena: "Right. I'll leave you to it. Thanks, Sheila." -> "Mm. Books don't keep themselves." (2.7 s, first sentence 2.1 s, own); steps: first-written 2.1, first-plain 2.1, draft 2.1, check 2.7
- rocco: "Alright, Ron. Quiet tonight?" -> "Ah, it's only just come on to midday, friend. The fish market's still busy across the way. Rain's been holding off so far, which helps, people get moving when the weather's decent. Nothing out of the usual yet." (3.8 s, first sentence 1.9 s, own); steps: first-written 0.8, first-passed 1.9, draft 1.9, check 3.7
- rocco: "How long were you on the docks?" -> "Thirty years, boss. Started when I was a young man and kept going till the scheme ended in eighty-nine. Mickey kept me on after that, needed someone for the door and the rank, and I knew the street by then, knew who was who. That was a long time ago now." (6.4 s, first sentence 3.1 s, own); steps: first-written 0.9, first-passed 3.1, draft 3.1, check 6.4
- rocco: "What happened when the scheme ended?" -> "Work dried up, friend." (6.2 s, first sentence 2.6 s, own); steps: first-written 0.8, first-passed 2.6, draft 2.6, check 6.2
- rocco: "Anybody been hanging about the rank who shouldn't be?" -> "Not that I've seen, no." (4.6 s, first sentence 1.8 s, own); steps: first-written 0.8, first-passed 1.8, draft 1.8, check 4.6
- rocco: "I heard something happened on Quay Street. Did you see it?" -> "You're going to have to be a bit more specific, friend." (4.4 s, first sentence 2.3 s, own); steps: first-written 1.0, first-passed 2.3, draft 2.3, check 4.3
- rocco: "What would you do if you found out who it was?" -> "Depends what it was, doesn't it." (4.3 s, first sentence 1.6 s, own); steps: first-written 0.7, first-passed 1.6, draft 1.6, check 4.3
- rocco: "Do you trust Darren?" -> "Darren's alright." (3.8 s, first sentence 1.8 s, own); steps: first-written 0.8, first-passed 1.8, draft 1.8, check 3.8
- rocco: "Fair enough. See you later, Ron." -> "Right you are, boss. Keep an eye on the weather, looks like it might turn." (1.8 s, first sentence 0.8 s, own); steps: first-written 0.8, first-plain 0.8, draft 0.9, check 1.8
- sam: "Darren. What are you selling today?" -> "So listen, nothing that's got a name yet, but I've got my ear to the ground. You need something moving, or you need to know what's moving?" (3.5 s, first sentence 2.1 s, own); steps: first-written 0.9, first-passed 2.1, draft 2.1, check 3.5
- sam: "How much for a radio?" -> "That's the lot, honest. I'd tell you if there was more." (5.1 s, fallback); steps: first-written 0.8, first-flagged 2.4, draft 2.4, re-first-written 3.2, re-first-flagged 5.0, redraft 5.0
- sam: "Where do you get your stuff from?" -> "Here and there." (4.2 s, first sentence 1.6 s, own); steps: first-written 0.9, first-passed 1.6, draft 1.6, check 4.2
- sam: "Have you heard about the break-in?" -> "Break-in where?" (3.5 s, first sentence 1.4 s, own); steps: first-written 0.7, first-passed 1.4, draft 1.4, check 3.5
- sam: "Somebody said they saw you near there." -> "Near where? You're going to have to tell me what you're on about, mate. I'm all over the street, that's the job. You hear something specific, I hear it too, usually before you do." (4.2 s, first sentence 1.7 s, own); steps: first-written 0.8, first-passed 1.7, draft 1.7, check 4.1
- sam: "Can you find out who did it for me?" -> "Depends what it is, doesn't it." (4.0 s, first sentence 1.5 s, own); steps: first-written 0.8, first-passed 1.5, draft 1.5, check 4.0
- sam: "What's it going to cost me?" -> "So listen, nothing that's got a name yet, but I've got my ear to the ground. You need something moving, or you need to know what's moving?" (8.5 s, first sentence 5.5 s, own); steps: first-written 1.0, first-flagged 3.3, draft 3.3, re-first-written 4.2, re-first-passed 5.5, redraft 5.5, recheck 8.5
- sam: "All right. Don't do anything stupid." -> "I don't do stupid, mate." (4.3 s, first sentence 2.0 s, own); steps: first-written 1.0, first-passed 2.0, draft 2.0, check 4.3
