# For Jafar

One dated summary per sitting, written at its end, under 200 words: what
changed, the evidence, what failed or is unproven, what is next, and any
decision you need to make. Unresolved decisions carry forward. Earlier
summaries are in git; everything before 24 September afternoon is in
production/archive/FOR-JAFAR-to-2026-09-24.md.


## 24 September, afternoon: one integrated encounter

**Changed.** Records cut to the audits' minimum; the checklist archived; the stop hook has one job. The encounter is built and is now the build's regression. The new player character breaks a window by his own key. The shopkeeper sees it and shouts. The gossip carries it to two more people. The lad, questioned, answers from his own memory on the right day. The town is saved to disk, the game quits, a new process reloads it, and they still know. Unseen, nobody knows.

**Evidence.** All three runs pass in the packaged build, and the shout's recording is in the probe folder. The Core suites pass; the independent check's findings are fixed.

**Unproven.** The questioning is proven only with a stand-in model. The real model, given the lad's memory, talked about the window but asked nothing: the game can't yet give him a reason to suspect you. The encounter runs as a test, not yet in the playable slice.

**Next.** Give characters suspicion, so they question you live, then put the encounter into the slice.

**Budget.** The chandler: 61 minutes, about one point (71 to 72).

Decisions: none.

### AI tester, 2026-09-24 17:00

45 steps, 2 minutes, $0.48. Not a gate. Worst first:
- (5) [the tester's own fault, fixed: it photographed the screen before the game had drawn, and caught another app. It now copies only the game window's pixels.]
- (4) E at Mickey's window seemed to do nothing. [It did break the window (the shout was recorded), but a clear pane vanishing cannot be seen and Lena's line lasted six seconds. Fixed: a line says the window goes in, and it stays up.]
- (4) [The same report again.]
- (3) Player camera is clipped extremely close inside another NPC's body model; the screen is mostly filled with the NPC's torso/clothing texture, blocking view entirely. [Fixed: the cast MetaHumans now block the player.]
- (3) Player camera remains stuck inside/against an NPC's body model even after walking backward twice; view is still mostly blocked by the NPC's torso, indicating a collision issue that persists.
- (2) Player character is stuck extremely close against a wall/window with an NPC clipping into frame; camera view is blocked, suggesting a collision/positioning issue near this shop front.
Full report: production/playtest/ai-tester/2026-09-24-1700/report.md

### AI tester, 2026-09-24 17:11

68 steps, 4 minutes, $0.75. Not a gate. Worst first:
- (4) Say/talk proximity detection consistently fails ("Nobody near enough to talk to") even when standing right next to an NPC like Lena, making dialogue impossible to trigger reliably.
- (4) Confirmed: player character (grey tracksuit man) is a separate NPC visible on screen, distinct from the camera-controlled avatar. The say/talk proximity check fails repeatedly even standing adjacent to Lena, making this 
- (3) Say command repeatedly reports "Nobody near enough to talk to" even when standing right next to an NPC (Lena/Sam visible adjacent to player); proximity detection for talking seems broken.
- (3) "Nobody near enough to talk to" appears even though the player character (grey tracksuit, seen from behind at center) is visible standing right in the middle of the scene, suggesting the actual controlled avatar may be a
- (3) Player camera is clipping extremely close into an NPC's striped shirt, filling most of the right side of the screen at very close range; the NPC model appears far too large/close, indicating a collision or camera clippin
- (2) A woman NPC is standing in an odd static pose directly in the player's path, facing the camera awkwardly close; she appears to be blocking movement near the shop window.
Full report: production/playtest/ai-tester/2026-09-24-1711/report.md
