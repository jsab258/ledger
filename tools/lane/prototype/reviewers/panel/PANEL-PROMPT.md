# The brief each panel judge gets (lane task 4t, piece 6)

How to run it, once per loop. For each AI player type's session (piece 2), build the packet with `panel.py strip` (using the player's answer only to choose clips). Give three fresh helpers (Opus, high effort) the text below, each with one packet folder (PACKET), ANCHORS.md copied into that folder, and nothing else: no design file, no player review, no hidden log. Three judges a session, judging different sessions where the budget is short (at least one judge for every session, three for the two sessions the players rated highest and lowest). For before and after a loop, `panel.py pair` makes two orders, order1/ and order2/, with A and B swapped and every label replaced by "version A" or "version B"; each judge answers order1 in one fresh session and order2 in another, never told that the letters were swapped; `panel.py score` counts a winner, overall and per axis, only when it holds in both orders. Answers go, one JSON file each, into one folder; `panel.py score` writes the verdict into production/lane/REVIEWS-loop<n>.md.

Note for piece 8: clips are chosen partly at the player's own best and worst minutes, so when the judges' best and worst moments are compared with the player's, leave those clips out of the comparison (panel.py writes why each clip was chosen beside the packet).

Why recordings and not a summary: his words (19 Nov), and the research (production/research/lane/PANEL-ON-RECORDINGS-2026-11-20.md): models find small glitches in frames poorly and report false ones often, so a judge's fault is only something to replay by machine; how well they judge pace and taste is unmeasured and is checked against his own words (piece 8).

---

You are a judge on a panel of experienced players and game critics. You are looking at a recording of someone's real session with a new PC game, set in a British port town in 1990: frame sheets (each frame captioned with the minute played, the key pressed and the words on screen) and the full log of keys and on-screen words. Open only the files in PACKET: PACKET.md first, every sheet it lists (look at each with your file reader), LOG.md and ANCHORS.md. Open nothing else and search nothing.

Judge the game, not the player: when the player does something odd, ask whether the game made it reasonable. Judge only what the frames and the log show; when an axis cannot be judged from them, say "not shown" and give no number. Compare honestly against the anchors (Kingdom Come: Deliverance II and GTA V at their best = 5).

For a pair (PAIR.md present), judge A and B on the same axes and say which is better overall and on each axis, or "same".

Answer with JSON only:

For one session:
{"judge": "<your judge number>", "session": "<the packet's label>", "would_recommend": true or false, "verdict": "<three sentences a player would understand>", "scores": {"hands_busy": {"score": 1-5, "why": "<what in the frames, with minutes>"}, "town_alive": {...}, "people_and_talk": {...}, "tension": {...}, "controls_and_camera": {...}, "period_and_place": {...}, "knowing_what_to_do": {...}, "looks_finished": {...}}, "dead_stretches": [{"from": minute, "to": minute, "what": "..."}], "best_moment": {"minute": 0, "what": "..."}, "worst_moment": {"minute": 0, "what": "..."}, "faults_seen": [{"minute": 0, "what": "...", "sheet": "..."}], "against_kcd2": "<one sentence>", "against_gta": "<one sentence>", "fix_first": "<the one change that would help most, from what you saw>"}

For a pair:
{"judge": "<your judge number>", "pair": "<the Pair line from PAIR.md, e.g. p1/order1>", "better": "A" or "B" or "same", "axes": {"hands_busy": "A" or "B" or "same", ...}, "why": "<three sentences, with minutes from each>"}
