# 6. Risk register: the thirty-minute friends' build

**The aim at risk:** a thirty-minute build of Quay Street his friends play on this PC, which passes the Meridian Test. They do not bounce off the visuals, the town visibly knows them, talking feels live, and he would rather play it than not (CLAUDE.md, "The one list", 3 October).

Columns follow the standard register (ID, description, likelihood, impact, score as likelihood × impact, mitigation, contingency, trigger [W, Risk register]), plus an owner [SS, games practice].

**Baseline:** 3 October 2026, from the evidence in 2-FEASIBILITY.md.

## Scales

| | Likelihood | Consequence for the friends' build |
|---|---|---|
| 1 | Rare, under 10% | Negligible |
| 2 | Unlikely, 10–30% | Minor: a friend notices, play goes on |
| 3 | Possible, 30–50% | Moderate: one Meridian condition weakened, or a week's slip |
| 4 | Likely, 50–80% | Major: one Meridian condition fails, or several weeks' slip |
| 5 | Almost certain, or already happening | Severe: the build cannot be played, or the premise fails |

## The top ten

| ID | Risk | L | C | Score | Evidence today | Trigger (what shows it is happening) | Cheapest mitigation | Contingency | Owner | Trend |
|---|---|---|---|---|---|---|---|---|---|---|
| **R1** | **Talk feels empty, wrong or unchecked.** The town does not visibly know them, and talking does not feel live. | 5 | 5 | **25** | On a fresh set of 60 questions (48 answerable), "that's all I know" 23–25 times, on the bench (30 Sep). An invented detail in 7% of turns. The claim check off whenever a budget is set (Program.cs line 273, read here). Only three people can be talked to. | P4: more than 1 in 5 questions answered "that's all I know". P3: any invented detail a reviewer flags. Any live path without the checker. | **P3**: fix the budget bypass and measure the checked path. Keep friends' talk with the three grounded characters, steered by the suggested lines toward what they know. Author the newcomer's most-asked questions as grounded beats (the studio method the 30 Sep audit cites). | More written lines, fewer free ones. | town | new |
| **R2** | **Replies come too slowly.** Talking does not feel live. | 5 | 4 | **20** | First sound 5.41 s median, none of 30 within 2 s (30 Sep). The voice's share is 3.66 s beside the game. Even an instant voice leaves about 2 s, because the words take that long (3-PROOFS.md, P2). | The checked path's median first sound over 3 s in P3 or P2. | **P2** (list item 3): the voice off the card, timed beside the game. The thinking sounds and plain first sentences already in place. | A money ruling for Jafar: a paid streaming voice, researched at about $0.28 an hour of play. It would reopen "voices as chosen", need speaker consent the VCTK recordings lack, and need an allowlist entry. | builder | new |
| **R3** | **The street does not reach the bar** before the friends' build. They bounce off the visuals. | 4 | 5 | **20** | Every whole street frame since 1 Oct failed a reviewer or Jafar. Item 2.1 failed two reviews. The proof view alone is estimated at 30–50 builder-days. The friends' build waits on the proof view and the street-wide pass (DECISIONS 1 Oct). | Fewer than two proof-view items passing a week (P21). Any item failing twice. | **P10**: one house of the kit at the bar before six frontages. **P21**: a dated plan with a buffer, so the slip shows in week one. | Time-box each item. Keep the friends' walk to the dressed stretch and the hook camera's direction. | builder; Jafar for frames | new |
| **R4** | **People break the illusion.** | 4 | 4 | **16** | Tom, on screen for all thirty minutes, is a Mixamo stand-in in a grey tracksuit. No clothes meet the floor. All three cast share one stiff idle. Mouths "only open and close". Faces read underlit in passing. Three Mixamo stand-ins "jump out at night". | P8, P7, P6 or P20 failing. A reviewer flagging any person in P4's films. | **P8** (Tom first), **P7**, **P6**, **P20**. The 8 m crowd rule (3 Oct). | Fewer people on screen. Frame people from behind at distance, as the Hook sheet does. | builder, clothing; Jafar for people | new |
| **R5** | **Frame rate and memory give way** as the content arrives. | 4 | 4 | **16** | The sparse slice's slowest 1% sits at 16.7 ms. About 1.5–2.8 ms of GPU is left for the proof view's additions, and the memory envelope is already full. The voice crashed when squeezed to 1.4 GB (1 Oct). The asset plan assumes Nanite; the game has it off. The walk shows 23 of 847 frames over 33 ms. | Perf step: GPU median over 14 ms, slowest 1% over 25 ms. Game over 6.0 GB. The voice's speed halving. | **P1**. A fixed texture pool. The asset audit against 4-BUDGETS.md. Time the walk with the cast voice on every build. | Scalability High. Hold 50% scale. Fewer people in view. The voice off the card (P2). | builder | new |
| **R6** | **There are not thirty minutes worth playing.** | 4 | 4 | **16** | No thirty-minute session has ever been played or recorded. Ada and June, two of the first hour's "day-one five", cannot be met. The office is not enterable. The police are text captions. | P4: more than five minutes with nothing to do, or the deed's consequence not seen within thirty minutes. | **P4** now, on today's build. Its empty minutes become the content list. A written statement of what the thirty minutes contain (1-AUDIT.md, item 1). | Shorten the session to what holds. Script a stronger first beat. | builder, town; Jafar for scope | new |
| **R7** | **The build fails on the night.** | 3 | 5 | **15** | The key is read from the current user's folder (CrimeProbe.cpp line 3248), so a fresh account would run talk offline. The portable voice was never started outside his account. Every package is Development. Putting the key there would leave it in plain text in an account his friends use. F: free space is uncertain (27 or 40 GB on 3 Oct). | P5 fails. Any step that needs his account or a developer tool. | **P5** now, then once a month and the week before. One Shipping package. | Play from his own account. | builder; Jafar for the account | new |
| **R8** | **A licence, terms or disclosure problem** removes or blocks something already built. | 3 | 4 | **12** | The NoAI ruling removed 42 items in a day (3 Oct). The Unreal EULA, MetaHuman and Mixamo terms and Steam's survey are unread. The disclosure's "every line is checked" and "through LEDGER's own server" are untrue today. The repository is public, holding reference screenshots. The allowlist still admits the Game Animation Sample. | Any term read in P14 that forbids a use the pipeline makes. Any claim in the disclosure that a test contradicts. | **P14**. Record every source's licence before building on it (5-DONE.md, C6). | Replace the source by its CC0 or own-made alternative (asset plan). | builder; Jafar for rulings | new |
| **R9** | **The way of working stalls the list.** | 4 | 3 | **12** | The builder's order was replaced six times in four days. More than twelve items went past the two-tries rule. The builder holds 17 of the twenty basics and every port. Four licence reversals in a week. No target date exists, so no slip can be measured (1-AUDIT.md, item 10). | The list's order changing more than once a week. A two-tries breach. The weekly items-done rate falling. | **P21**: a dated plan and this weekly review. One item at a time (already ruled). | Ask Jafar to freeze the order for a week. | builder; Jafar | new |
| **R10** | **Friends' talk is not covered:** his rulings conflict, and money may run out mid-evening. | 4 | 4 | **16** | The key serves "his live play, and measurement runs", and "nothing else uses it" (DECISIONS line 257, 3 Oct). The friends' build runs on his PC with no relay (line 200, 1 Oct), so friends' talk can only use the key. Steady talk costs $1.07–3.22 an hour. The key's monthly cap is not in the repository; at the cap every call fails, and the characters fall back to brush-offs. | **Fired:** the two rulings conflict today. Later: P3's cost for thirty minutes, times the planned sessions, over the allowance; the month's spend past half the cap. | **One ruling from Jafar** on friends' sessions and their cap; the likelihood falls to 1 once he rules. A per-session cap that keeps the check on (after P3). | Shorter sessions; more written lines. | Jafar | new |

## Watch list (below the top ten)

| ID | Risk | L | C | Score | Trigger |
|---|---|---|---|---|---|
| W1 | **One PC is everything:** development machine, build machine, AI tester, voice and the friends' play machine. A failure or a bad Windows update stops all of it. The Dropbox backup covers approvals and listed folders. | 2 | 5 | 10 | Any unplanned downtime; a failed backup line in the summary |
| W2 | **F: is small** (about 111 GB in all; 27 or 40 GB free on 3 Oct). C: reached 0 bytes on 1 Oct. | 3 | 3 | 9 | The retention's morning line under 30 GB on F: |
| W3 | **The language model changes under us.** Every check runs on Haiku 4.5, whose retirement was promised not before 15 Oct 2026 (production/research/prompt-caching/NOTE-2026-09-29.md, read 29 Sep). | 2 | 4 | 8 | A deprecation notice; a change in reply behaviour on the fixed sixty questions |
| W4 | **Faces and bodies depend on Epic's cloud rigging service.** A forum thread of August 2026 reports auto-rig and texture downloads failing on a 300 s timeout, mostly outside the US (production/research/casting/notes/metahuman.md lines 77–78 and 214). | 2 | 3 | 6 | A failed rig on any new face or build |
| W5 | **VCTK speaker consent** is a stated risk (24 Sep): the recordings' consent terms are unpublished. | 2 | 3 | 6 | Any change in Edinburgh's terms, or a complaint |
| W6 | **His eye is the only final judge** of every whole frame, face, voice and garment. His time is finite, and a page a day caps the rate of visual decisions. | 3 | 3 | 9 | Pages waiting more than a day; items held on his yes |
| W7 | **A content-rule breach reaches a friend's screen.** The back-bar picture (`decal_05_interior_bar_back`) is still in the fallback street spec (production/specs/vignette-pieces.json); the brand bible still says Mickey's is a pub. | 2 | 4 | 8 | The content gate missing a file the game reads; anything with drink in a frame |

## The weekly review (15 minutes, Mondays)

The register was baselined on 3 October.

1. **For each risk, read its trigger's latest number** from the record that measures it:
   - the performance verdict;
   - P3 and P4's logs;
   - the retention's morning line;
   - the decisions of the week.
2. **Set likelihood and consequence again** and recompute the score. Mark the trend: up, down or level.
3. **Note the next action and its date.** A proof that has run moves its risk's likelihood from its result, not from the plan.
4. **Close a risk** only when its proof has passed and its trigger has stayed clear for two weeks.
5. **Add new risks** from FINDINGS.md, from audits and from any proof that failed. Keep ten in the top list and move the rest to the watch list.
6. **Put the top three, with their next actions,** into the Monday summary as recommendations.

Changing the summary, the overview or the list is outside this review. This page only proposes the cadence.

### Review log

| Date | Reviewer | What changed (IDs, scores, closed, added) | Top three |
|---|---|---|---|
| 2026-10-03 | this review (cloud) | Baseline; R10 raised to 16 after the independent check found the rulings conflict | R1 (25), R2 (20), R3 (20) |
| 2026-10-05 | builder, Monday review | R3 up to 25 (L5: the audit of 4 Oct finds the visual method unproved; five proof steps set aside, Mickey's room failed three reviews). R1 level 25 (bench not re-run; 0 of 8 empty in P4). R2 level 20 (first sound 4.6 s, text 2.5 s, P4). R10 down to 9 and R7 to 10 (friends on his own account, $5 cap tool, no second account; Shipping launch and restart limits unproved, item 0.6). R9 level 12 (weekly orders and one session adopted, not yet shown). | R3 (25), R1 (25), R2 (20) |

## What could not be verified

- **Every likelihood** is this review's judgement from the evidence named [I].
- **Effort and dates** depend on P21, which has not run.
- **The key's monthly cap,** and whether "Help improve Claude" is off.
- **The free space on F:** two records disagree.
