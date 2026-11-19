Addendum: DESIGN-ADDENDUM-2026-11-20.md (same folder) designs the gameplay parts the parts tree found missing or thin (hiding, tailing, searching, finding the way, the water's edge, traffic stops, the firm's growth, fronts, street happenings and more); read it with this file.

# LEDGER: the whole game

18 November 2026. One design by one author, built from canon.md, RULINGS.md and the synthesis pack. Canon outranks it and his rulings stand. Anything here that would change either is a question in QUESTIONS.md or a "conflict" line in TRACE.md, never settled here.

How to read it:
- "New" marks a choice this design makes that no source makes.
- Numbers are first values, to be tuned by play. A number that began as a read of another game's files is marked "lead": a starting point, not evidence (his rule of 17 Nov).
- KCD2 (Kingdom Come: Deliverance II) and GTA are the references. Mafia is one data point among others.
- Each system ends with its experience rules: an id, a plain rule and a check. B is the clumsy-player bot in a headless browser. S is a scripted test through the game's test hook. H is an AI hands-on session with screenshots and set questions (section 19).

## 1. The core loop

LEDGER is a game about doing crime with the hands in a town that is watching, and rising by what the town then believes. Three ledgers run through it: the one the town keeps on Tom (its memory), the one Tom keeps on the town (his notebook), and the one the inspector opens at the end (the fare book).

**Which game this is.** The design follows canon's pillar of 18 November and his words that day: "we don't want a gossip simulator. We want an exciting, immersive, novel game." The player mostly acts; the town's memory and gossip are the engine under the hood, not the show. Canon's older section, What LEDGER is not (14 Sep), pulls the other way on how play time is spent: it calls what people know about you "the mechanic" and gives anything that does not feed perception, memory, gossip or consequence "the smallest budget". It already exempts fighting (AAA, 12 Oct) and driving (AAA as the end state, 17 Nov), so the pull is on jobs, fares and how play time is shared. The design spends play time by the pillar (the hour budget below) and argues that every verb feeds consequence, but the two lines sit in canon side by side, so the conflict is his to settle (QUESTIONS 5).

The machine at the centre is Mickey's, a minicab office: "a book of every fare, a radio nobody can help overhearing, a yard with two escapes, a rank outside" (canon). New, and the design's main choice: the cab firm is the loop, not the backdrop. How much of the day is spent behind the wheel is a separate matter, a prototype question not yet adopted (section 5).
- Cover. Nobody looks twice at a minicab at two in the morning.
- Eyes. Drivers cross the town all day, passengers talk in the back, and the radio hears everything.
- Alibi and wash. Every fare is written down. Night money can hide only behind fares that were really driven.
- Risk. The firm's name is on the roof. What a cab does, the firm did.

**A minute: read, act, answer, get clear.** Tom reads the street: light, noise, who is out, which windows are lit, where the constable is. He acts with his hands: carries, drives, breaks in, fronts a man up, fights, runs. The street answers at once: a head turns, a lamp comes on, somebody walks off towards the phone box. Then the choice: finish, drop it, reach the witness first, or go. Being seen is not failure. It is the fork.

**An evening: one game day, 16 to 20 real minutes.** By day the radio gives fares, the debt book gives collections and the street gives side stories; all of it sets up the night. At dusk somebody brings a job and Tom gets ready at the office: the coat, two things in the pockets, which car, who comes. At night he does the job, three to six minutes under watch, and gets home. Then the count with Sheila: the tin (night money) against the fare book (clean money). Next morning it comes back: said to his face, shown in a look, or standing at the door in uniform.

**A playthrough: 15 to 20 hours, three acts** (canon's baseline; section 16). The Inheritance is week one. The Rise runs about seven game weeks. The Ledger Comes Due is the inspection week.

How the systems feed each other:

| System | Takes from | Gives to |
|---|---|---|
| The town's eyes (2) | every act, the light, the hour, people's routines | talk, the police, the rivals, crew loyalty, the Ledger |
| Jobs (4) | people who offer them, what the day turned up | night money, standing, and exposure to the town's eyes |
| The cab and fares (5) | routines (who goes where), the firm's cars | clean money, room in the book, knowledge, cover and an alibi; its name pays for every sighting |
| The night (6) | the day's set-up, the weather | the stage for jobs: fewer eyes, sharper ears |
| Combat and the dial (7) | nerve, the odds, crew, what is carried | debts paid, men down, statements, feuds; the dial changes the police and the rivals |
| Police (8) | statements from the town's eyes, the dial | hours lost, searches, Ellis's case, the ending |
| Money and the book (9) | fares (clean), jobs (the tin) | cars, crew, fronts, silence; the book's state goes to the inspection |
| The Ledger (10) | what Tom saw, heard and was told | direction, where he stands, his reading of the end |
| Talk (11) | what people know | what comes back, deals struck, witnesses turned, sit-downs decided |
| Crew (12) | money, a need or a hook, how Tom is seen | odds in a fight, eyes, alibis, work sent; and more men who know |
| Rivals (13) | what their own people see | pressure on his people, his clean money and his cover |
| The rise (14) | money, standing, crew, property | doors, bigger jobs, harder rivals |
| The endings (16) | the book, one friendship, the street's talk, Ellis's case, the police | the close |

A system that gives nothing to another is cut (section 18).

An hour budget by activity (Study 17, his lesson 2), set for 18 hours. New. The driving share is a prototype value, not adopted: whether the cab is the day's main verb is still a question (section 5; QUESTIONS 6).

| Activity | Hours | Share |
|---|---|---|
| On foot: walking, looking, carrying, following, running | 4.5 | 25% |
| Driving: fares, tails, getaways | 4 | 22% |
| Talk: what comes back, deals, witnesses, sit-downs | 3.5 | 19% |
| Jobs with the hands: break-ins, collections, searches, the count | 3 | 17% |
| Fights and chases | 1.5 | 8% |
| The Ledger, the map, getting ready | 1 | 6% |
| Watching and waiting together | 0.5 | 3% |

Experience rules, the whole game:
- ER-CORE-01 Never stuck. From any state the player can move on within 5 seconds: walk away, get out, back out, or a short in-world reset to clear ground. Check B: fails if, for 5 s of pressing toward any of four free directions in turn, neither Tom nor the car moves 1 m, or no input has any effect for 5 s.
- ER-CORE-02 No silent failure. Every change Tom could perceive (a job failed in front of him, a door shut in his face, money lost from his pocket or tin, a witness he could see or hear, an officer coming into view) is shown by the world within 3 s and written in the Ledger within a game minute. A change he could not perceive surfaces later only through the world (it comes back, ER-EYES-08). Check S: trigger each; assert the line and entry for the perceivable cases, and assert no screen text or Ledger line for the unperceived ones.
- ER-CORE-03 No failure without warning. Nothing permanent lands without a sign first, and a choice that cannot be undone asks twice. Check S on every such choice; H is asked "did you see it coming?".
- ER-CORE-04 A mistake becomes a story or a choice, never a reload. No game-over screen; every failure ends in a state the town can talk about, and control returns within 2 real minutes. Check S: every failure route, timed.
- ER-CORE-05 Something new at least every 3 minutes in the first hour, and never more than 5 minutes anywhere with nothing new. Check H: the log of new places, people, verbs and scenes.
- ER-CORE-06 About ten distinct activities per 30 minutes; talk under 30% of play; waiting under 10%. Check H: play time booked by activity.
- ER-CORE-07 Always something to do. By day, with no job live, a fare, a debt or a person with a word for him is within 30 real seconds. Check S: an idle probe at 20 random daytime moments.
- ER-CORE-08 Not a driving game (canon). Driving stays under 25% of play, and no fare runs longer than 2 real minutes without a decision, a person or a sighting. Check H.

## 2. The town's eyes (the engine)

The moat is canon and does not change. Every act exposes seven slots a witness may or may not catch (precursor, draw, act, victim, actor, flight, aftermath). Identification climbs five rungs (someone, a shape, a mark such as the coat, a face, recognition), and the top rung needs somebody who knows him. Memory is permanent. Gossip travels only where routines meet. The deterministic Core decides every outcome. None of this is shown as a system. The player meets it in the moment, and afterwards.

**In the moment** (first values, LEDGER's own). A watcher sees a shape at 35 m, a mark at 18 m and a face at 8 m, and recognises him at 25 m only if they know him. Light scales it: daylight 1, a lamp 0.7, an unlit street 0.25, a doorway 0.12. A glance takes 0.35 s and knowing who it was 1.2 s; running doubles how fast he is noticed. Sound has a reach set by the act, the hour and the rain: a footstep at three in the morning carries about 3.6 m and at noon nothing.

It shows with no meters. Light: the picture's corners follow the light value the rule uses. Sound: his own noise is mixed by the same number as its reach, and a street that has noticed him goes quiet. Bodies: a head turns, a longer look, a pause in a walk, two heads together, a step back at night, a figure at the glass of a lit window (D29: posture first). After a deed, near people look, some gather and drift back; witnesses talk quieter for a game hour (ruling 23 Sep). An assist, off by default, can outline the people Tom can see who are facing him (never a figure he could not see, never what they know).

**Afterwards:**
- A witness is only as sure as what they caught. A noise or a shape is suspicion, never "he did it" (ruling 30 Sep).
- The walk. A witness who means to tell sets off, to a friend, a phone box or the station, and is seen going (Study 1). No mobiles in 1990: the walk is the timer, and until it ends nothing is on record. Tom can reach them first: talk them round, pay, threaten, help, or let them go. A threat can stop a report to the police, never the street's talk (ruling 3 Oct).
- Talk passes only between people who know each other and meet, within 6 m, weaker with each telling (the Core's rule). The rumour study of 23 Sep found that what was missing was never how many knew, but how faintly they showed it. So those who know show it, on the Core's own ladder: notice, watch, comment, avoid, refuse, confront.
- It comes back. In week one every answer to the outfit and every plainly seen deed is said to Tom's face by somebody he has met, within one game day (on paper at the old clock: the outfit's answer at minute 13, by Darren; a seen night 16 times in 16; to be measured again at the prototype's clock).
- Talk cools, memory does not. How long a deed stays hot in talk depends on its kind, about 1 to 7 game days (lead); a body never cools; the person who saw keeps it for good. This would replace the Core's single 96-hour half-life: a town task with new golden rows, not a change to the moat.

**What gives him away** (Study 1, the coverage audits): running; the same coat as last night; blood, until washed with water and privacy (the launderette will wash a coat too, and remember it); dirt; a weapon in the hand; clothes wrong for the door he knocks at; the car; and, rarely, a camera: CCTV is rare in 1990, the bank's among the few, its tape recycled weekly (canon). The coat buys doubt about the face and none about the car.

**The town lives without him.** Everyone keeps a routine, each place in it with a cap and an owner so no doorway jams (Studies 1 and 17). The crowd keeps a few clock windows, their hours from 1990 research (owed). Unseen people go on perceiving, remembering and talking.

Each named person needs their own nerve and loyalty, so the same deed goes differently with different people there. That is his decision, open since 29 Sep (QUESTIONS 3).

Experience rules:
- ER-EYES-01 The three questions (is he seen, how far did that carry, who noticed) can be answered from picture and sound alone, scored only on watchers Tom could see or hear. Check H: asked at ten random moments, right 8 times in 10 against the simulation's truth; again with sound off, and again with the light cue off.
- ER-EYES-02 Symmetry. If he can tell a person is facing him and he is in light, that person can see him. Check S: figures at 8, 18 and 35 m.
- ER-EYES-03 Warning before knowing. A watcher's head turns at the start of the 1.2 s it takes to know him, not at the end. Check S: cue to identification at least 0.8 s.
- ER-EYES-04 A witness who will tell is seen to go, and the walk lasts at least 30 real seconds when it starts in Tom's sight. Check S.
- ER-EYES-05 No all-knowing town (punish 15). Every reaction by a neighbour, the police or a rival traces to a chain of sightings and tellings the test hook can print. Check S: a chain for every reaction in a seeded week.
- ER-EYES-06 A witness is only as sure as what they caught. Check S: golden rows.
- ER-EYES-07 Nothing is ever wiped. Every memory survives save, load and skipped time. Check S: reload at random moments and compare.
- ER-EYES-08 It comes back. In week one a plainly seen deed is said to his face within one game day. Check S: 16 seeded weeks.
- ER-EYES-09 After any seen deed, people within [first value] m look, at least one gathers and drifts back, and witnesses' talk is quieter for a game hour (ruling 23 Sep). Check S.
- ER-EYES-10 Each give-away in the list above makes a witness catch more than the same act without it, and a deed done from the car always names the car. Check S: golden rows, one per give-away.

## 3. Where tension comes from, minute to minute

Nine sources. Each is something the player can read and answer.
1. Eyes: who can see him now.
2. Ears: how far that carried.
3. The load: what is on him. The envelope, a holdall, blood, a weapon. Found is worse than used.
4. The window: the landing is open from ten till one, the customs lamp goes out at eleven, Ada's pot goes on at nine.
5. The walk: a witness on the way to a phone.
6. The law near: a beat, a car, Ellis on the street.
7. The other man's nerve: will he give way or stand?
8. The odds: two against one is deadly.
9. The two lives: the tea and the landing fall on the same night.

For the playtester's count, a tense moment is a stretch in which at least one source is live and the player has a choice. A retellable moment is a tense moment in which the player chose, it could have gone the other way, a named person was part of it, and it came back later.

An evening has a shape: an easy day, a tightening dusk, the job, the relief of getting home, the count, and the sting or the reward next morning. Tension that never lets go is as flat as none. The day shift is the rest between.

Experience rules:
- ER-TENS-01 At least 12 tense moments per 30 minutes, from at least four sources, none over half (round 5 had 19.5, nearly three quarters of them one kind). Check H.
- ER-TENS-02 One retellable moment in the first 30 minutes and two an hour after. Check H, and the panel: at least 5 of 8 reviewers name such a moment as the most exciting.

## 4. Jobs

A job is a small graph of saved states (Studies 11 and 16): four job states and five step states, every change saved. Each step has a place named by a landmark, who is there, a window on the town's clock, the act the town can perceive, two or more outcomes where it decides, a Ledger line of about 22 words, two or more sources of direction, and a skip the tester can call.

Six laws:
1. Offered by a person, on a state, never by a marker or the clock alone.
2. Three keys to every lock (the agency model's project law). No job needs talk, a fight or a car to finish.
3. Windows, not minutes. Patience on people, and a "wait until" for every known appointment.
4. Failure continues. Late, caught, wrong man hurt, refused: each ends in a state the town can talk about. Nothing restarts.
5. Authored, never rolled at random (ruling 13 Nov). Each job has a spec and a check.
6. No set piece twice in thirty minutes (the player study).

The families, which are the game's verbs:
- **Fares** (section 5).
- **Carries.** Move a thing through watched ground. The outfit's envelope to the ferry landing is the first.
- **Collections.** Mickey's debt book: five debts, five lessons. Darren Milner £22 (pays in what he hears). Wayne Harrison £30 (pays in goods from the pawn's back room). Lee Drewery £15 (stands, with the docks behind him). Julie Kettlewell £9 (cannot pay: mercy or shame). Dennis Iveson £80 (has the money, a yard and a yard hand, a man in his twenties). A debtor pays what his purse holds and the rest stays on the book. Squeezing is told on the street; so is letting a debt go.
- **Break-ins.** Rooms are labelled by privacy with a night rule. A challenge warns, warns again, then calls someone or acts, within half a minute at worst (lead); the warnings reset, the sighting is kept for good. A lock has several keys: a key lent or copied (Ian Megginson knows every lock on the street), a back way a routine leaves open, or force, which is loud, shows on the door for a day and is a crime. No lockpicking game.
- **Lifts.** Goods carry a hot mark that fades with value and distance while the owner never forgets. A shop buys, haggles or refuses, and remembers. Rita's back room fences at about 0.4 of an honest price (lead; the 1990 rate is owed).
- **Tails.** Follow a person or a car without being made, to learn a routine. The town's eyes in reverse.
- **Minding.** Stand at someone's door, sit in the car, be seen at someone's shoulder. The town's eyes record who stood with whom; what it pays is set in each job's spec.
- **Sending** (Act II). The eight owed verbs of D56, each through a named person (section 12).
- **Sit-downs.** The steps that decide an act, in talk (section 11).

Side stories: 25 to 40, found on foot, no markers, mostly light or grey against the main story (Study 17; the 32 drafts of 8 Nov are the list). Each is 3 to 5 steps and ends in something the town knows.

Guidance without markers (Study 16): the giver names the place by a landmark; the Ledger keeps the line; anyone who knows the place says so when asked; street signs and the paper map; Pauline on the radio in the car.

Experience rules:
- ER-JOB-01 Every go-to step names its place by a landmark, and a newcomer reaches it unaided within 3 real minutes (punish 14). Check H.
- ER-JOB-02 Every step has two or more sources of direction. Check S: the job data.
- ER-JOB-03 Three keys. Every job is finished by at least two scripted approaches; none needs talk, a fight or a car. Check S.
- ER-JOB-04 No lateness fail inside a window of at least 2 game hours; every appointment has a "wait until"; a wait or a sleep always stops for what the town has for him. Check S: the week of waits.
- ER-JOB-05 Every outcome of every job, failures included, is reached by a script and leaves a Ledger line. Check S.
- ER-JOB-06 No set piece twice in 30 minutes; no fare wrinkle twice running (punish 9). Check H: the log.
- ER-JOB-07 Steps sleep while he is away and settle by the clock; each has a tester's skip. Check S.

## 5. The cab and the car

His rulings: fun first, as open-world games that are not sims do it; 1990 by sound, sway, look and relative speed; automatic gearbox; real figures a floor. Canon: not a driving game; a car hurts, never kills.

New, and a prototype question, not adopted: whether the cab is the day's main verb. It pulls against canon ("NOT a driving game", and the smallest budget for anything that does not feed perception, memory, gossip or consequence), so it does change how a canon line is read and is his to settle (QUESTIONS 6). The case for it is that every fare here feeds perception and consequence; no research yet shows that fares stay fresh. The browser rounds test it inside the spend rule until the playtester shows fares stay fresh over a week, and ER-CORE-08 keeps driving under a quarter of play meanwhile.

**Fares.** Pauline calls them. Each fare is a named person going where their routine takes them at that hour: Brenda Laverack to the fish dock at dawn, the packing shift from the Old Basin cold stores at half past five (the atlas's proposal), a lodger for the last ferry. Fares are the town's daily life made playable, and driving them teaches the map and the hours with no tutorial. A fare lasts one to two real minutes and pays 80p plus distance.

About half of Act I's fares carry one wrinkle, a small decision: the talker, who says something true about somebody; the parcel ("take this too, no questions"); the tail (a car in the mirror, or "follow him"); the runner, out of the door without paying; the wait ("keep the engine running"); the hurry (the last ferry in four minutes); the face (somebody who matters gets in).

**The radio is the guide and the leak.** Pauline gives the way by landmark ("past the chapel, second left, the house with the slippers on the step") and says it again on a key. Nothing said on it is private: the office and every cab hear it (canon).

**The firm drives without him.** Kevin Needham drives days and Terry Hodgson nights whether Tom drives or not, so the book fills slowly without him. That is the lazy path.

**The car in the town:**
- It is ordinary. A cab waiting with its sign lit draws no look, by day or by night. That is its cover (new).
- It is known. Every sighting of a deed done from it names the car, even when the face is not known. The roof sign and the plate make it the firm's.
- It is loud: heard within about 44 m by day (the lane's proposal), much further at night.
- It can be hurt, in stages by closing speed (the driving study, round 3): a light touch does nothing; then dented; then crumpled; and from about 35 mph in one hit it will not drive on. Then Tom walks, the firm fetches the car, and it is off the road for a day.
- Reckless driving in a police car's sight starts a stop. Refusing it is a chase that ends caught or lost.

**Cars and people** (canon, his pick of 18 Nov). Only the player's car can strike anybody; other drivers always brake. A hit knocks a person down and can hurt them badly. It never kills. Hits are rare: people look before they step out, so at town speeds a hit is the player's doing. How bad it is scales with speed and intent: a clip at walking pace is a bruise and a mouthful, a hit at speed is a broken leg, and a car aimed at a man is an attack with a weapon (rung 7, section 7). A car strike is never a blow under the fall rule: whatever the person lands on, a car never kills, and rung 8 is never reached with a car. Then the choice, put at once:
- Stop and help. It costs minutes and puts Tom's face beside the cab. The victim and the street remember that he stopped.
- Drive off. It is a hit-and-run: the car is described, the police look for it, and a police car or a witness who sees it gives chase; "a Mickey's cab knocked her down and never stopped" goes round.

Either way the cost lands on the firm's name and its fares (people ring another firm for a while) and never ends the game. The talk fades unless another hit feeds it. The person who was hit never forgets.

**The edge is soft** (Study 2). A fare that leaves the Hook is driven to the west road or the north road and comes back as time passed and money paid. Nothing fails for leaving.

Experience rules (his quality rule of 18 Nov, after the pole and the jerky keys):
- ER-DRIVE-01 Never stuck. After any crash the car moves or can be left within 5 s. A car wedged on a pole or a wall always backs out. A car that will not drive on says so at once, Tom can get out, and the firm fetches it. Check B: 30 minutes of crashing. Check S: pole and wall hits at 10, 20, 35 and 50 mph.
- ER-DRIVE-02 Smooth on every device. On keys the steering eases to lock in 0.2 to 0.35 s and centres itself in 0.4 to 0.9 s; a lane change at 60 mph on keys swings the tail under 15 degrees and settles within 1 s; the pad is analogue; a set course takes the same time within 10% on either. Check S: the scripted drives D1 to D8, by keys and by pad.
- ER-DRIVE-03 A car hurts, never kills, and only the player's car can strike anybody. Check S: 1,000 seeded crossings in traffic with no contact; player hits at 5, 15, 30 and 50 mph, including hits that throw the person against a kerb, wall or step, aimed and unaimed; the hurt scales and nobody dies.
- ER-DRIVE-04 No hit from nowhere. Nobody steps out inside the stopping distance of a car doing 30 mph or less. Check S: a scripted lawful driver, 40 minutes, no hits.
- ER-DRIVE-05 After a hit the choice is put within 2 s, both answers play on, and neither ends the game. Check S.
- ER-DRIVE-06 The car's camera never enters a wall, a car or a post. Check B: a 40-minute soak with no such frame.
- ER-DRIVE-07 In or out in under 2 s; a blocked door never traps him. Check S.
- ER-DRIVE-08 A touch under 10 mph is forgiven, and the handling never changes without a cause the player can see or hear. Check S.
- ER-DRIVE-09 The way Pauline gives is always right and is repeated on a key. Check S: a scripted driver follows each fare's words alone and arrives.
- ER-DRIVE-10 A hit-and-run starts a chase whenever an officer or a police car sees the car, and a drive-off always costs the firm's name and fares for [first value] game days. Check S: both choices, seeded, fares counted for a week after.

## 6. The night

Night is the stage. Fewer eyes and sharper ears: pools of lamp light with dark between (his ruling), lit windows, and sound that carries twice as far in the small hours. The coat goes on at the office with one key and makes his face harder to know at night. Rain is cover: it cuts sight and sound, empties the street and halves the voices. Weather comes as weighted profiles (dry overcast, drizzle, rain), and one wetness value drives the look, what is seen and heard, and who is out.

A window is a watcher only when somebody is at it, and then a head and shoulders show at the glass. Ada in her dark front room is the exception the player learns once.

Each night offers at most one ask from the outfit (every other night in Act I), any jobs the day turned up, and the late fares. Nothing forces him out. Sleeping is a skip, never a need. Waiting is a key that offers "wait until" each known appointment, and a wait or a sleep always stops for what the town has for him (the waiting design of 29 Sep; Study 17: never force waiting).

Rooms are enterable where jobs and stories go: Mickey's and the flat above, the caff, Rita's back room, Hal's shop, Ada's front room, Iveson's hut, the chapel hall. Density goes up and back, not out: back rooms, yards, alleys, upstairs flats (Study 17).

Experience rules:
- ER-NIGHT-01 Dark is readable, not blind. Tom and the ground 5 m round him are always visible to the player, above a brightness floor in the game's exposure that lives in the one tuning table (section 19). Check H: screenshots at the darkest spots.
- ER-NIGHT-02 A window is a watcher only when a figure shows at it. Check S.
- ER-NIGHT-03 Rain changes who is out, what is heard and what is seen, the same way every time. Check S: the same seed dry, in drizzle and in rain.

## 7. Combat and the escalation dial

His design of 12 Oct stands: a ladder the whole street watches, good to do and costly to have done. Eight rungs: stare, square up, threaten, shove or grab, strike, weapon out, weapon used, kill. Most confrontations end on rungs 1 to 4. Each rung is an act with the seven slots, so the town treats it like any deed.

**Feel**, to the melee sheet (first values). A blow starts within 0.1 s of the button; a jab lands in 0.25 to 0.40 s and the committed blow in 0.63 to 0.85 s. Contact is sold by a short freeze, a brief camera close-in inside the wider fight view, a small shake and four layers of sound. A struck man reels by the side he was hit. An incoming blow can be read before it lands. No lock-on: Tom slides to about 1 m in the wind-up (lead) and hits the man the stick points at. No health bar, no combat music, no arena: condition shows in posture, breath, a dropped guard, blood and a limp. Mashing tires him and loses.

**Odds and endings.** A fair one-on-one is roughly even and skill tips it. Two against one is deadly; three is a beating. Other men have nerve: a man watched stands longer, and so does a man cornered (prototype rounds 4 and 5). A fight ends one of five ways: someone backs off, someone runs (a chase through alleys and yards), someone goes down, the police arrive, or people step in. Watchers keep about 3 m (lead) and scatter once a weapon is out.

**Death.** Tom cannot die. Beaten, he comes round on the pavement, in Grace Rinaldi's kitchen or in hospital, robbed by chance, with a street that knows he lost. Hospital costs days, not money, and plants a witness. Fists knock a man out and never kill on their own. A fall against a kerb, a wall or a step after a blow can kill, rarely, and the town treats it as a killing (ruling 30 Oct). A car strike is never such a blow (section 5). Finishing a man who is down is a separate decision, in the quiet afterwards. A body is never wiped, and a man who stops keeping his routine becomes the town's question before anyone finds him.

**The street is a weapon.** Walls, doorways, railings, car bonnets, steps, kerbs and the quay edge, as paired moves fitted by height, seven places first. Things to hand break: a chair after about 2 blows, a brick 3, a dustbin lid 4, a wheel brace never.

**Weapons** in four tiers: fists; things to hand, left behind; carried (cosh, knuckleduster, knife, bat), which can be seen on him, found in a search and have to be got rid of; firearms, rare and last. Two things under the coat; the rest stays at the office. A weapon drawn cannot be undrawn unseen. What the town makes of a blow rises by tier; no number is shown.

The prototype has Tom refuse to lay hands on a woman, anyone of sixty or over, or the priest. That rule is invented and waits for his ruling (QUESTIONS 2).

**The escalation dial** (ruling 18 Nov). The game starts with no gun in the Hook. Guns come only through people: bought, stolen, taken, or found once at Mickey's. The dial is a fact in the town's memory, not a meter. Four states (the wording is new):
- 0, Fists. Nobody carries a gun.
- 1, Shown. A gun has been seen. It is news across town, and the rivals' top men start carrying.
- 2, Fired. A shot is heard to about 177 m by day (LEDGER's own figure). Whoever hears it keeps it for good. Armed officers come from the station for gun calls, slowly. Ellis's interest rises a step. Guns stay rare: only named men carry.
- 3, War. A few named men on each side now carry, and everyone knows who. The police bring in armed cars (his words), stop and search on the street, and everyone is jumpier: watchers run sooner and report more, night fares fall. A shot can now kill, and each death is a named, permanent event; guns stay rare.

It rises with what the town learns and with who pushed: arming his crew or buying from the docks moves it, and the town remembers who brought the guns in. It falls one step only after about two quiet game weeks, and never back to 0. Staying a firm of fists and bats is a real way to play the whole game.

Experience rules:
- ER-FIGHT-01 Timings sit inside the melee sheet's bands, C1 to C15. Check S: the drills at 1/60 s.
- ER-FIGHT-02 Every incoming blow can be read 0.45 to 0.80 s before it lands, and at most two men swing at once, 0.4 s apart (punish 3). Check S.
- ER-FIGHT-03 A way out at every moment. Backing off and running are always inputs. Check B.
- ER-FIGHT-04 Tom never dies. Beaten, he is in control again within 60 real seconds, with the cost said. Check S.
- ER-FIGHT-05 No death breaks his ruling. Fists alone never kill; only a fall against a kerb, wall or step within 3 s of a blow can. A car strike never counts as a blow. Check S: 10,000 simulated fights.
- ER-FIGHT-06 The man the stick points at is the man hit, and nobody is hit through a wall. Check S.
- ER-FIGHT-07 Skill beats mashing. A patient scripted fighter wins most fair one-on-ones; a mashing one wins under 3 in 10. Check S.
- ER-FIGHT-08 A weapon comes out only on a held input, and the dial never moves on a deed nobody saw or heard. Check S.
- ER-FIGHT-09 Guns stay rare and killing stays rare at every dial state: at War, at most a few named carriers per side and no more than [first value] deaths an act. Check S: three seeded game weeks at War, carriers and deaths counted.

## 8. Police

A pressure Tom can read and answer, never the end of the game. Corruptible as individuals, never as a thesis (canon).

- **The beat.** A constable walks Quay Street and the quay at night (prototype round 2; Study 11's proposal; a new system that needs its place in PLAN.md). He challenges on suspicion: a man carrying at night, running, bloodied, or where he should not be. He calls out first. Stand, and he searches; what he finds he keeps. Run, and it is a chase, lost once Tom is unseen for 7 s or 70 m.
- **Statements.** Talk alone brings questions, never an arrest. An arrest needs a signed statement from someone who knew it was him, or an officer who saw it. A neighbour who sees him put a window in reports him unless on his side or talked round (ruling 1 Oct). Mickey's people never go to the police about one of their own. Some never go at all because of their trade: Rita, Wayne, Hal, the scrap dealer, the customs officer, the outfit's man.
- **Arrest.** It costs hours, never the game: about six for a window (two and a caution if he owns up), eight for a wounding, twelve for a robbery, twenty-two for a killing and then bail (bail after a killing was rare in 1990: to be checked against the period research). The duty solicitor is free. The coat is kept if he wore it. He is never taken twice for one deed. The street sees him go and says so.
- **Ellis.** DS Carol Ellis is already on the warehouse fire. She comes to Quay Street for a body, for a detective's crime once reported, and from day 4 for talk, once three people of Tom's day world pass talk of his nights. People she asks remember being asked and tell him.
- **Four stages, each with its sign:** nothing; asking round (her name in the street's talk); investigating (an officer at his door); a manhunt (a car on the street and his description). No stage is skipped unseen: this follows the ending signs' proposal of 30 Sep and is provisional until his answer on C5 (TRACE), which may let a witnessed killing go straight to a manhunt. Under either answer, a manhunt's sign shows at least one game hour before an arrest can land.

Experience rules:
- ER-POL-01 No arrest without a named statement or an officer who saw it. Check S: golden rows.
- ER-POL-02 The police announce themselves. A constable is heard or seen 3 s before he can challenge, and he calls out before he acts. Check S and H.
- ER-POL-03 An arrest costs game hours and under 2 real minutes, and never happens twice for one deed. Check S.
- ER-POL-04 A chase always ends, caught or lost, within 90 real seconds, and can always be lost by breaking sight. Check S: 50 seeded chases.
- ER-POL-05 Provisional until his answer on C5. No stage of police interest is skipped unseen; and even when a witnessed killing goes straight to a manhunt, its sign (a car on the street, his description said aloud) shows at least one game hour before an arrest can land. Check S: every route to a manhunt passes its signs, under both answers.

## 9. Money and the book

Two pots. Clean money is in the fare book and can be spent anywhere. Night money is in the tin and cannot be explained. Tom starts with £23.50 (the prototype's figure; a hard opening by his ruling). The rent is due on Friday: £18 in the prototype, with the 1990 figure for an office and a flat owed to research.

**The wash.** At the count, with Sheila: the fare book can hide £10 plus 80% of the fares really driven since the last wash (the prototype's rule). Over that the books are off. Sheila says so before she does it, thinks less of him for it, and the inspection in Act III reads every such week. This one rule ties the day to the night: more real fares, more night money made clean. It is a decision of twenty seconds, once a day, never a spreadsheet. New: a fare written for an hour he was somewhere else is an alibi the police can check, and a lie in the book that somebody may one day have to hold up.

**Everybody's money is somebody's circumstance** (canon: not an economy game). A debtor, a shopkeeper or a fence pays only what is in the purse or the drawer. Shops keep hours from their people and doors and restock weekly. There is buying, selling and fencing, no crafting (ruling 23 Sep).

**What money buys is position** (section 14): a car, a driver's wage, a share of a front, a better coat, a solicitor, somebody's silence. A player who only drives fares can pay the rent and keep the firm alive. The night is where it grows.

So that nobody confuses them: the fare book is the firm's clean record; the tin has no book; Mickey's debt book has five names; Mickey's real book is everything he ran, in his own hand, shown when Sheila trusts Tom; and the Ledger is Tom's own notebook (section 10).

Experience rules:
- ER-MONEY-01 No money from nowhere. Every pound traces through a sum of flows. Check S.
- ER-MONEY-02 He always knows what he has and what is owed by Friday, in words. Check H.
- ER-MONEY-03 The opening is hard but never a dead end. Doing nothing misses Friday's rent; a week of fares alone pays it. Check S: both weeks, scripted.
- ER-MONEY-04 Sheila warns before a wash puts the books off. Check S.

## 10. The Ledger

Tom's notebook of people and events (D12, D20, D37), and the one place the player sees where he stands. It has People (what he knows of each, and what he believes they know of him), the Day book (events in order), Open (jobs, debts, promises and appointments, each naming a person and a landmark), Money (in words), and a paper map of the Hook that marks only places he has been or been told of.

- It holds only what Tom saw, heard or was told, with how sure he is from how he learned it: said to his face is sure; saw them looking is "thinks so"; two heads together is "guesses".
- Nothing is erased. A wrong belief is struck through with the day and the reason.
- A line low on the screen says when he comes to believe something new.
- Every job step, done or failed, gets a line of about 22 words.
- On request, and at each act's end, it gives Tom's reading: how things stand as he sees them, built only from signs he was given (section 16).

It closes the one gap the coverage audits found in all five games studied: each of them tells the player where he stands, and LEDGER had no such surface. It does so without showing another mind (D33).

Experience rules:
- ER-LEDG-01 Every entry traces to something he saw, heard or was told, and nothing is ever erased. Check S: no entry without a source event; struck through, never removed.
- ER-LEDG-02 It opens in 120 ms, by keys or pad, with nothing smaller than the style guide's 24 units, and any person is found in three inputs (punish 17). Check S.
- ER-LEDG-03 A newcomer can answer "what next, and where" from the Ledger alone (punish 14 and 20). Check H.

## 11. Talk

Talk is the moat and never the main thing the player does (canon). It is where consequences surface and are dealt with. Five uses and no others:
1. It comes back: said to his face, once, by somebody who can tell it is him.
2. The deal: a job offered, taken or refused.
3. The witness: talked round, paid or threatened.
4. The question: the way, a name, what somebody saw. A character says only what the simulation knows.
5. The sit-down: the steps that decide an act.

**How it works** (his rulings). Anyone named can be spoken to: live talk for every named character if possible, the main characters at least (ruling 28 Oct). Live talk only when the player speaks to someone; everything the town says unprompted is written ahead and checked once. No prepared openings, no skill checks, no mission nags. Every line that decides is the game's own: a yes, a no and a line that keeps talking. Only a plain yes is taken, and anything that cannot be undone asks twice. The clock stops in talk and Leave is always there. Suggested lines on Tab, shown at once on a controller. A short thinking sound and a glance before a live answer, never a loading sign. Offline or slow, the written street carries on, with an in-character brush-off and a small sign. The AI notice shows once, before the first talk. Any live line can be reported from the pause menu or by a key, before outsiders play (ruling 24 Sep).

**Staging and volume** (Studies 3 and 9). Tom stands 1.5 m from a speaker and both face each other. Talk can run while walking or driving where a scene is staged that way: Alison asks her question from the back seat. Street lines are about 7 words, replies about 12, Tom's suggested lines about 4; a remark is said within 7 m. About 30 own street lines for each regular, except Sheila, Alison and Ada, who keep the shared lines (the ruling on street lines); Ron, Darren, Father Walsh and June have their own. For the crowd, at least 6 lines per situation per kind of speaker. Situations to write: greetings by regard (afraid, angry, knows and likes him, his appearance, neutral), bumping, neighbours greeting each other, talking to oneself at work, rain. Greetings by regard are how the rise is heard. Lines are remembered: a person's own line once a day, a shared line once a week per street (prototype round 5). Everyday street talk comes at most every 45 s.

The press works only through a person (D56): Alison Sedman, who remembers and can talk.

Father Brendan Walsh, the Irish-born parish priest (Father Walsh to the street), is one of the day-life ring: a person with his own street lines and his own memory, met by the chapel and in the street. Religion is part of life, never mocked and never a mechanic (canon), so the chapel is a place in his life, never a system.

Experience rules:
- ER-TALK-01 A reply is heard within 2 s or the written line plays; a line slower than 8 s is dropped with an in-character brush-off (basic 10). Check S: a slow stand-in.
- ER-TALK-02 Nobody says the same line twice in a day; no shared line twice in a week on one street; at least three closing lines each. Check H: the transcripts.
- ER-TALK-03 Talk never decides alone. Every decision is the game's own yes and no; what cannot be undone asks twice; Leave is always offered. Check S: 170 lines that are not a plain yes.
- ER-TALK-04 A character says only what the simulation knows. Check S: the claim check with planted bad replies.
- ER-TALK-05 Typing never moves Tom (basic 9), and the clock stops in talk. Check S.
- ER-TALK-06 No talk scene runs 60 s without a choice or control (punish 4). Check H.
- ER-TALK-07 Any live line can be reported. Check S: a report is filed from talk and from pause.

## 12. Crew

Tom's power is people (ruling 12 Oct). Crew are named residents with a routine, a need, a nerve and a loyalty with a ceiling. They act on orders (ruling 23 Sep).

**Inherited:** Ron Kirby (the door and the rank; he will stand at Tom's shoulder), Sheila Dunn (the book), Pauline Kitching (the radio), Kevin Needham and Terry Hodgson (the two cars), and Darren Milner, who runs messages and sells what he hears.

**Recruits** come from the thirty regulars, by one of two roads (open-city spec): meet a need, which is slow and holds (Julie Kettlewell, laid off, wants work and can drive); or spend a hook, which is quick and brittle. Each brings a use the firm lacks: Ian Megginson's locks, Lee Drewery's fists, Norman Dent's nights on the warehouse row, Karen Grummitt's view of the ferry, Shaun Hewson's paint for a cab that should not look like a cab.

**Orders,** two inputs at most: with me; wait here; watch that; fetch him; take this there; drive; lean on him. A crewman told to drive is an AI driver and always brakes for people (canon), so "the player's car" stays the car the player drives. From Act II, the eight owed verbs in his order (D56): have a named man hurt through a named man; point a plan at a person; frame someone through what the town believes; lean on a witness to change what they say; move or hide a body; dock, expel or beat one of his own; send men at a rival's property; have someone vouch for him. An order is given and a line is written. A beating is never shown at length.

**The accomplice is the risk, not the alibi.** Each man sent is a second person who knows. Past his nerve he talks, to a rival or to the police, and the sign comes first: he looks away, he asks for his cut early, he is not at his post. Crew can be poached, frightened, arrested, and killed for good.

**The board** (new). A chalkboard in the office with a line for each car and driver, placed by the last radio call, and the week's fares. It is where a car is put on a rank or a shift. A car on a rank is the firm's eyes there: its driver's sightings reach the radio, and a cab placed where Tom will be gives him an alibi or a witness. A minute a day at most; if he never touches it, Pauline runs it.

Experience rules:
- ER-CREW-01 An order takes two inputs at most and is answered in voice or body within 1 s; a man who cannot do it says why. Check S.
- ER-CREW-02 Crew never block a door or a lane; a follower keeps up or waits, and never fails the job. Check B.
- ER-CREW-03 A man near breaking shows it before he talks. Check S: the sign comes before the event in every seeded case.
- ER-CREW-04 Crew never do what cannot be undone unless told. Check S.

## 13. Rivals

Three, each going after a different ledger, each knowing only what its own people have seen or heard (the story outline; the Core's rule):
- **Maureen Jensen, the Widow:** the docks, muscle and smuggling. She goes after his people: a tax on his drivers at the dock gate, his least loyal man poached.
- **Geoffrey Agar:** old money, lawyers and stamps. He goes after his clean money with paper: the private-hire licence, a solicitor's letter, an inspection of the cars.
- **Danny Cammack:** the new crew, loud and reckless. He goes after his cover: trouble on Quay Street that brings heat Tom did not earn.

Each has eyes among the regulars. The empire roster, part of canon's baseline, names, through the cards, Lee Drewery and Kevin Needham for the docks, Susan Coverdale for Agar and Rita Welburn for Cammack; the cards settle it. So the first thing the Widow learns of Tom may come from his own day driver, over a radio nobody can help overhearing.

Each climbs the same ladder, never skipping a rung, and each rung is said to his face or shown on his street: noticed; a visit; pressure; a threat; a sit-down. Every pressure has three answers: pay, defy, or counter with what he knows. Keith Garbutt, the Fixer, sells true reads, a meeting and one truce.

Why they come to him: the Hook is the port's gate, with the ferry, the Old Basin, customs and the Harbour Board. All three want it, and Mickey's death left it open. So the whole contest plays inside the release map, the Hook plus the docks (ruling 28 Oct). If the docks are cut, the Widow's ground is the Old Basin and the fish dock inside the Hook. The Exchange and the Parade are where fares go and letters come from. New: a sit-down can happen in the back of his own cab, driving while they talk.

No faction is a number. The town has no opinion, only people (D34).

Experience rules:
- ER-RIV-01 Every rival move traces to something one of its people saw or heard. Check S.
- ER-RIV-02 No rung is skipped, and each rung is said to his face or shown on his street. Check S.
- ER-RIV-03 Every pressure has three answers and none ends the game. Check S.

## 14. The rise

Tom rises in position, never in numbers (ruling 30 Oct): money, respect, crew, property, clothes, access. He never gets better at fighting or driving. The player does.

| Rung | What the town calls him | What he holds | What opens |
|---|---|---|---|
| 1. The nephew | the new owner | two cars, two drivers, Ron, Sheila, £23.50, the debt book, the run | the street, the rank, the landing |
| 2. The firm is his | Nowak | his answer to Sheila, a third car, a first recruit | Mickey's locked office and the real book (on trust), Rita's back room |
| 3. The Hook's firm | Tom | five cars, a night desk, a first front, a first round, the cold-store shift contract | the dock gate, the Harbour Board's counter, a solicitor |
| 4. The port's man | Tom to most, Tommy to two or three | fronts and rounds across the Hook, men at the dock gate, the cold store and the landing, a brief on call | the sit-down; people step aside |

How it is felt, with no number on screen:
- The name. Each person uses the name they have reached. The gate is knowing, not liking; a step never goes back; Sheila withholds his name until she trusts him.
- Greetings and bodies: a nod, a door held, a path cleared, or a street that goes quiet.
- Property that reacts: the office fills, and the flat above stops being Mickey's.
- Clothes: three outfits across the game (as he arrived, a decent jacket, a good overcoat), each changing how strangers speak to him and which doors open, and a dark coat for nights; each his to approve in the game's camera (rulings 29 Sep and 3 Oct).
- Access as soft keys: standing, dress, an introduction, an appointment the Fixer brokers.
- The fleet: his cars pass him in the street.

What rises with him is risk: more men who know, more eyes on the firm, and rivals one rung higher. The hard opening stays hard: in week one he can be refused, ignored and knocked down.

Legitimate cover (Study 17, his lesson 6): the cold-store shift contract, cabs for the packing shift morning and evening, is the daily loop that earns and explains money. Empire as management on the street (his lesson 8): run through people and the board, never a screen of sliders.

Experience rules:
- ER-RISE-01 No number of standing, loyalty or heat is ever on screen. Check S: a screen inventory. Check H: screenshots.
- ER-RISE-02 Each step up the name ladder is heard within a game day of being reached and never goes back. Check S.
- ER-RISE-03 Each rung changes at least three things a newcomer can point to. Check H: the same street walked at rung 1 and rung 3, differences listed.

## 15. The first hour, minute by minute

The story beats are those of the first hour he approved on 29 Sep and the nine first-week designs, kept as written. The work between them (fares, the debt book, the first fight) comes from the prototype's rounds and this design. What is new is the staging, to meet canon's pillar of 18 Nov: hands first, and the speeches spread across the things they are about. His approved designs stand as written (ruling 29 Sep), so this restaging (arrival by ferry, a first fare at 2:30, the debt book at 4:30) is his to approve (QUESTIONS 4); until then it is built to the recommended answer. Clock: 45 real seconds a game hour, as the prototype plays (his feel decision, still open). The ferry lands at about twenty to four on Monday 15 October 1990.

| Min | What happens | New |
|---|---|---|
| 0:00 | The ferry comes in under a grey sky. One shot, 20 s, skippable. | |
| 0:20 | Control. Down the gangway with the suitcase and up the quay; people look. A hint only if he stands still for 4 s. | walking, places, faces |
| 1:30 | Quay Street. Darren on the pavement, friendly and owing; Ron on the rank ("boss"); Ada at her window; June Suddaby, Mickey's daughter, still in town and wanting nothing from the office (the approved hour): a line each, in passing. He can speak to anyone from here; the AI notice shows once. | people, talk |
| 1:45 | Sheila's walk-round, her six lines, walking with her. At the radio Pauline has a fare and no car. | the office, the radio |
| 2:30 | First verb: car two, a fare to the priest's house by the chapel, Pauline giving the way by landmarks. Dusk falls and the lamps come on as he drives. The fare goes in the book. | driving, the map, first money |
| 4:30 | Back at the office Sheila finishes at the things themselves: the fare book, the locked door, the flat and, as the prototype has it, the debt book: five names, £156. Rent is due on Friday. | the debt book, a purpose |
| 5:30 | First choice and deed. Darren owes £22 and is standing there. Front him up, take what he offers, or strike it out. Somebody sees. | fronting up |
| 7:00 | After dark Ron brings the outfit's first ask: a coat and an envelope for the ferry landing after ten. Go, say no (asked twice), or stay away. | the ask, the coat |
| 9:00 | The carry. The lit quay is quick and seen; the yard and the lane behind the warehouses are dark and slower; the cab is quickest and known. The constable is on his beat. If he calls out: stand and be searched, or run. | carrying under watch, a chase |
| 11:30 | The landing. "Mickey's?" The hand-over, and his cut comes back. Home by the yard. The tin. Sleep. The game saves. | night money |
| 13:00 | Tuesday. It comes back: Darren says it to his face, whichever it was. A look held too long. The Ledger opens for the first time. | the Ledger |
| 14:00 | The count with Sheila: how much of the tin the book can hide. | the wash |
| 15:00 | Day shift: three fares, two with a wrinkle (a talker about the fish dock, a parcel for Rita's side door), then the packing shift. | fare kinds, the docks |
| 19:00 | Wayne Harrison's £30 at the pawn's back room: goods or money. | haggling, the fence |
| 20:30 | Lee Drewery's £15 on the quay. He stands. It comes to blows, and people stop to watch. | the first fight |
| 23:00 | A side story found on foot, light in tone. | side stories |
| 25:00 | A night with no ask: Darren's tip (a first break-in) or the late fares (a runner). | a break-in or a chase |
| 29:00 | Wednesday. If a witness named him for the fight, a constable at ten: go, or run. Hours lost, never the game. | arrest |
| 31:00 | Ada asks him to tea at nine. Alison Sedman takes his cab to the warehouse row and asks about the fire on the way. Julie Kettlewell's £9: mercy or shame. | Ada, Alison, the fire |
| 39:00 | Ron with the second envelope at eight; Ada's pot at nine. The tea, the landing, or both, with Ada's window on the street. | the two lives |
| 45:00 | Thursday. Both nights come back. Somebody uses "Nowak". | the name |
| 47:00 | Dennis Iveson's £80 at the yard: front up his yard hand, come back for the hut at night, or lean on what he bought out of the burned warehouse. | three keys |
| 53:00 | If the street is loud, DS Ellis on Quay Street, asking. | Ellis |
| 56:00 | After dark two men from the docks wait by car two, for Lee. Back off, run through the yard, or have Ron there. Tomorrow is rent day. | outnumbered, a crew order |

Against the numbers. Study 2's figures rest on file reads and estimates, so they are leads; canon adopted three of them on 18 Nov.

| Measure | Target | This hour |
|---|---|---|
| First control (Study 2) | within 1.5 min | 0:20 |
| First verb with the hands (new) | within 3 min | 2:30 |
| Talk possible (Study 2) | within 3 min | 1:30 |
| A choice and a deed (Study 2) | within 20 min | 5:30 |
| Longest stretch without control (Study 2) | 3.5 min | 20 s |
| Something new (Study 2; canon) | every 3 min; never past about 5 | every row holds new things; to be measured from the log |
| Distinct activities per 30 min (canon) | about 10 | 13 by minute 30 |
| Talk share (canon) | well under half; aim under 30% | to be measured; round 5 had 25% |
| Waiting (round 5 had 41%) | under 10% | to be measured |
| Watching (Study 2; Study 16) | well under 29%; aim under 5% | under 1% |
| What a failure costs (Study 2) | at most 2 min | a search, a lost fight, an arrest: each under 2 min |
| A moment a friend would retell, first 30 min (his rule) | at least 1 | the carry; the fight with Lee |
| The town visibly knows him (Meridian Test) | by minute 30 | minute 13 |

The friends' thirty minutes on Quay Street take the on-foot cut of this hour: the arrival, the walk-round, Darren's debt, the carry and the morning after. The cab joins when the map grows.

Teaching: every hint fires the first time it can mean something or when the player hesitates, never on the clock; the interface appears piece by piece as each part is first used; Ron or Pauline nudge after a minute of standing about.

Experience rules:
- ER-FIRST-01 Control within 1.5 minutes (aim 20 s); a verb with the hands within 3; a choice and a deed within 20 (aim 6). Check S for control, H for the rest.
- ER-FIRST-02 No stretch over 3.5 minutes without control; under 5% of the hour watched; every scene skippable and at most 60 s. Check S.
- ER-FIRST-03 A hint only on first need or hesitation, each once, never two within 12 s (basic 7). Check S: an idle test.
- ER-FIRST-04 By minute 30 the town has visibly known him once. Check S on seeded runs, and H.

## 16. Three acts and the endings

**The cast** (canon's baseline and his rulings; nobody here is new):
- Tom Nowak, 32, the player.
- Mickey (Michael Suddaby), dead before the game opens. He died of his heart at the office early one morning; Ron found him; nobody thinks otherwise (ruling 30 Sep). Only regulars who knew him describe him, in the two approved lines.
- Mickey's people: Ron Kirby and Sheila Dunn (sections 9, 12, 15, 16).
- The rivals: Geoffrey Agar, Maureen Jensen (the Widow) and Danny Cammack (section 13). The Fixer, Keith Garbutt, brokers between all three (section 13).
- The law: DS Carol Ellis (sections 8, 16).
- The day-life ring: Darren Milner (sections 4, 12, 15); Ada (sections 6, 15, the tea); June Suddaby, Mickey's estranged daughter (section 15, minute 1:30; her own street lines, section 11); Father Brendan Walsh (section 11); Alison Sedman (sections 11, 15, 16); Philip Danby (Act I below, still to write in the approved outline). Danby is a teacher by trade; the school stands closed for the game's window (canon), so he is never seen at work.
- The thirty regulars stand as written (ruling 30 Sep); the design uses them by name in sections 4, 5, 12 and 13, the dispatcher among them (Pauline Kitching, section 5).

**Act I, The Inheritance** (week one, about two hours, the most scripted). Five threads (the outline): the outfit's claim; the warehouse fire; Mickey's real book; the street deciding who he is; someone worth being honest for, who can be Alison Sedman or Philip Danby. Winding the business down ends Mickey's arrangement. The fire has a street version, which is a street fact; the truth is never the street's (ruling 30 Sep). The asks fall on nights one, three, five and seven. Rent falls on Friday. On Sunday Sheila comes in on her day off: "So which is it going to be?" Wind it down, take it over, or refuse to say. The street learns the answer.

**Act II, The Rise and the Squeeze** (about seven game weeks, 11 to 14 hours). It opens when the business has grown. Beats fire on states, never on days. The firm climbs rungs 2 to 4 while each rival climbs its ladder against it. Ellis joins the street's crimes to the fire: one case. One collision is guaranteed: an evening of his day life interrupted by his night life at the door. It ends at a sit-down with one head: accept, defy, or counter with what he knows.

New, a proposal for the writing of Act II, to be judged when built: the men behind the landing are the last of an old firm. If Tom kept the run, they hand him its end of the Hook and fade, and he becomes what Mickey was. If he ended it, the ground is open and the three rivals come sooner. The design needs only this much: keeping the arrangement means night money, cover and asks that grow; ending it means freedom without cover.

**Act III, The Ledger Comes Due** (one week, 2 to 3 hours). A courteous letter: a VAT inspection by Customs and Excise. The inspector brings one item each morning; Tom produces it or asks for it in writing. Each morning is one deciding step, graded by what the books hold. Sheila, if she trusts him, says where the lie holds. Ellis offers a trade: give her a rival, and the street learns who talks. Someone in the crew may ask to take it over. On the last day he can reach only a few people. Then the books open.

**The endings** are states, never picked from a list, and no single beat can fail the run. How many there are is open: his ruling of 28 Oct asks for two or three, while the outline he approved on 28 Sep and the built story have five. It is his to settle (QUESTIONS 1). Until he answers, the five built states are kept underneath, so either answer is a change of names, not of build. The design's proposal shows three, each with a better and a plainer way to turn out:
- The Kingdom. The business survives and the books hold. At its best one friend still counts him and the street does not hold his rackets as fact (the built "Both", rare). At its plainest, people are civil and no more.
- The Straight Life. No business at the close, and one friendship holds. At its best he handed it to someone who can keep it and walked away clean (the built "Quiet", never while hunted for a killing).
- Burn Both. Neither. What doing nothing produces, and where a hunted man can end.

No redemption path is added (D58). Reloading is never stopped, and the game says what is permanent before it happens.

Every cost that decides the ending shows its sign before it decides (D58; the ending signs of 30 Sep): the inspector's manner when the books stop standing; Sheila's words when the true books cross the line; a friend's unasked act; a telling overheard as fact; Ellis asking, then telling; the police's four stages; the successor's offer, and its withdrawal.

Experience rules:
- ER-END-01 Every ending is reached by a scripted route, including from a hunted state (punish 10). Check S.
- ER-END-02 No ending lands while Tom's own reading says things are quiet; every sign he was shown agrees with the ending he gets. Check S: the balance sweep.
- ER-END-03 Asked "how does this end, and why", the hands-on tester predicts the ending the state gives. Check H.

## 17. Camera, sound, screen and saving

**Camera.** Third person, never first. One arm, read from rows by Tom's state: street (his ruling: the Between height, an 86-degree lens, 3.1 m back, feet in frame), run, room (closer), talk (closer), fight (wider: both men's feet and the watchers), and car (from the driving study: about 5.8 m back, the view widening with speed). Blends of a second or less. Shake obeys Reduce motion.

**Sound** carries the town's eyes. Footsteps by surface and gait, his own and other people's. Doors that creak, hit and latch: a forced door is the loudest thing in a quiet street. A street in three parts (beds, capped one-shots, placed sources) and four states of the hour. One rain value that fades layers and halves voices. Rooms that change the echo at the doorway. The quietest lead voice sets the mix and talk lowers the beds. Silence is the commonest music, and there is never combat music.

**Screen.** Nothing Tom could not know. No minimap, no waypoints, no marks over heads, no meters of standing or heat. A prompt on what he can use, naming the person ahead and in view. Subtitles and prompts stay large; a subtitle shows only with its audio; switches for prompts, first hints and street-chatter subtitles; a photosensitivity line once guns flash. Keyboard with mouse, and a pad, each drive everything.

**Saving.** An autosave after every deed, every consequence and every change of a job step, held during a fight, never refused. Reloading is never stopped. No destructive choice sits one press from Resume. Esc pauses everywhere.

Experience rules:
- ER-CAM-01 The camera never ends inside a wall, a body or a car: on foot, in rooms, in fights or driving (basic 15). Check B: a soak with a clip detector. Check H: screenshots in the tightest rooms.
- ER-CAM-02 Feet in frame on the street; both men's feet in at least 90% of a fight's frames. Check S: frames counted in a scripted walk and a scripted fight.
- ER-INPUT-01 Every action answers within 100 ms; a press 100 ms early still counts; movement on keys is eased and mouse look never jumps. Check S: an input probe on keys, mouse and pad.
- ER-INPUT-02 The prompt names the person ahead and in view, held 0.2 s, and everything usable has a prompt (basic 8). Check H: a walk-up sweep with no prompt faults.
- ER-INPUT-03 Keyboard with mouse, and a pad, each reach every verb. Check S: the same scripted evening played through each.
- ER-SND-01 Every noise the rule hears, the player hears, at the same strength. With the picture off a tester can still tell a walk from a run, and a quiet street from one that has noticed (basic 18). Check H.
- ER-SCREEN-01 Nothing is on screen that Tom could not know, except the optional assist of section 2, which outlines only people in Tom's view. Check S: a screen inventory. Check H.
- ER-SCREEN-02 Words never overlap or leave the screen at four window sizes, and nothing is under 24 units. Check S: the layout test.
- ER-SAVE-01 A save after every deed, consequence and job step; a reload at any moment gives the same next hour (basic 20; punish 19). Check S.
- ER-SAVE-02 Esc pauses everywhere; no destructive choice is one press from Resume; Continue returns him where he left (basic 19). Check S and B.
- ER-START-01 It starts from its shortcut, shows progress while it prepares, opens at a sensible size, offers quality presets, and offers New game, Continue and Quit (basics 1 to 5). Check S on the packaged build; H: first-launch screenshots.
- ER-PERF-01 It runs smooth: 60 frames a second at 3440×1440 on the RX 6700 with the voice running, never under 30, in rain and at night (ruling 23 Sep; punish 7). Check S: the packaged frame-time run; in the browser, the frame meter at the busiest corner.

## 18. What is cut, and why

| Cut | Why |
|---|---|
| Gossip as a thing the player manages: rumour screens, who-knows-what meters, reputation numbers | His words: not a gossip simulator. The engine stays under the hood. |
| Waypoints, a minimap, objective markers, timers on screen | Ruling 23 Sep. The radio, landmarks, people asked, signs and the Ledger carry direction. |
| Stats, levels, skills, perks, competence by domain | Ruling 30 Oct: position, never numbers. |
| Gunfights with cover; a wanted level that clears | Not a shooter. Nothing is forgotten. |
| Lock-on, finishers, duels, combat music | His combat design; no cruelty as spectacle. |
| Random street fights and random encounters | Not Yakuza's fights; authored breadth; players punish the same loop. |
| Lockpicking and crafting games, hunger, tiredness, fuel, wear | The grind test: a decision now and then, never upkeep on a timer. |
| Racing, car tuning, a garage of cars | Not a driving game. |
| Jumping; boats and buses as more than scenery; multiplayer | Ruling 23 Sep. |
| Price tables, stock, supply chains | Not an economy game. Purses and a weekly restock stay. |
| Prison terms, fines as a system | 1990: an arrest is hours, a caution, or a charge and bail. |
| Long cutscenes, a watched opening, fixed chapters | Ruling 23 Sep; players punish a slow opening. |
| Typed commands as a way to act | Verbs are on keys; typing is for talk only. New. |
| The Parade and four other districts at release | Ruling 28 Oct: the Hook plus the docks. They are where fares go. |
| Five endings shown as five: open, not yet cut | Ruling 28 Oct says two or three; the approved outline has five (QUESTIONS 1). |
| The silenced .22 | Ruling 18 Nov. |
| Drugs as a verb, drink, gambling, children | Canon. |
| Scene traces (prints, heel marks) and the camcorder beyond one side story | Held until the week holds; the smallest budgets. |

## 19. How the rules are tested

Three testers, cheapest first:
- **B, the clumsy-player bot.** A headless browser driven by random, impatient and wrong input: walking into walls, dropping jobs halfway, crashing the car, pressing everything in a talk. It runs 30 minutes a build and fails the build on any rule it can see.
- **S, scripted tests** through the game's test hook: the melee drills (C1 to C15), the scripted drives (D1 to D8), seeded weeks, every job's every outcome, reloads at random moments.
- **H, an AI hands-on session.** The playtester plays an evening or a week as a newcomer and answers set questions with screenshots: who can see you now; what next, and where; how does this end, and why.

Where a rule says only "Check S", the script sets up the case the rule names and asserts the rule's own words and numbers. Then the panel of eight reviewer cards reads only the playtester's record.

Every rule's number lives in one table, so the browser, the Core and the Unreal game are tuned from one home (Study 13). A play build reaches him only with a publish-gate pass and a known-issues note (ruling 18 Nov).
