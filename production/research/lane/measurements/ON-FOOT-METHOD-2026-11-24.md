Built on: ON-FOOT-RULERS-2026-11-24.md (no on-screen ruler in any of the three games; heights only as community estimates), ON-FOOT-PUBLISHED-2026-11-24.md (published speeds almost absent), FILM-RULER-2026-11-23.md (frame stepping fit for speeds), SLEEPING-DOGS-DRILL-2026-11-23.md (the solid Sleeping Dogs speeds, by distance readout, used here as the check).

# On-foot speeds from footage: the method (24 Nov 2026, 10:52 Swiss)

Method researched: ON-FOOT-RULERS-2026-11-24.md and the gait literature's split of speed into cadence times step length (speed = steps a second x metres a step), the standard decomposition in walking and running biomechanics. No game shows a speed or coordinate on screen, so speed is built from two things footage does show well.

## What is read
1. **Cadence** (steps a second): footfalls counted over a straight, steady stretch of at least 4 s, read frame by frame (frame_grab.js, fixed seeks at 1/30 s steps near each footfall). Footage gives this exactly; no ruler needed.
2. **Step length as a share of the character's height**: on side-on frames (camera square to the path, the body within the middle third of the frame so lens stretch is small), the gap between the two heels at the moment both feet touch, divided by the standing height in the same frame (crown to sole). A pixel ratio, so the camera's distance cancels out.
3. **Height** (metres): the community estimate (Arthur about 1.85 m; Franklin about 1.83 m; Henry none found, so KCD2 uses the median adult male height of the game's period setting only as a stated assumption, about 1.70 m, marked). This is the one weak number; it moves every speed by the same share.

Speed = cadence x (step ratio x height). Each run gives one sample; five runs a gait a game, from uncut, dated footage, make it solid by count, with the height's uncertainty stated beside it (about plus or minus 3% for the GTA and RDR heights, unknown for Henry).

## The check before trusting it
Sleeping Dogs' sprint (5.5 m/s) and jog (4.5 m/s) are solid by its own distance readout. The method is run once on Sleeping Dogs footage of the same gaits; if it lands within 10% of those, the method stands; if not, it is questioned before any other game is read.

## The known weak point
The play camera sits behind the character, so side-on frames are rare: they come when a player swings the camera round mid-run, from cinematic camera modes, or from clips showing other characters crossing the view. Cadence can be read from behind (the shoulders and heels show each step); the step ratio needs at least two side-on footfalls in the same run. Where none exists, the run gives cadence only and stays a lead.

## First look (24 Nov about 11:00 Swiss, not yet a try)
Sleeping Dogs free roam CGho8_UOzSk (647 s, uploaded 9 May 2025, served 1280x720): coarse sheet every 53 s shows the camera behind or three-quarter on every on-foot stretch (30, 137, 243, 350, 564, 617 s). A 0.1 s sheet at 30.0 to 31.1 s: the legs readable from three-quarter, wide stances at about 30.1, 30.4 and 30.6 s, so roughly 3.5 steps a second (in line with the drill's jog at about 3.4), then he slows to a stop by 31.0 s. A 0.1 s grid is too coarse for the rule (read finer than the thing measured): the try needs 1/30 s seeks over 4 s of steady running. Step ratio: three-quarter frames foreshorten the stride, so side-on stretches are still to find (the Sleeping Dogs walkthroughs nDThIiEgyDA and q-XdObZ24eA, no commentary, are the next places to look).

## Walk
Sleeping Dogs has no walk. The walk comes from KCD2 or GTA V (advisor 341's second game for the one-game lead).

## Not used, and why
Map distances (no scale shown on screen); world features of known size (none published for these games); vehicle lengths (no published in-game sizes).

## Try 1 of the check (24 Nov 2026, 11:42 to 11:46 Swiss; Method researched: ON-FOOT-METHOD-2026-11-24.md)
Clip CGho8_UOzSk (uploaded 9 May 2025, served 1280x720), read 24 Nov in the browser pane by seek-and-draw crops (the session's own reading, no helper).
- **Cadence, works from behind.** The white soles show at each rear swing; the frame where a sole is highest marks one step, and the sole's side alternates (left, right) as it should. Read at 1/15 s steps (about five times finer than a step) over 557.0 to 560.2 s, steady straight running, camera behind: mid-swings at about 557.27, 557.60, 557.93, 558.33, 558.73, 559.05, 559.40, 559.80, 560.15 s: 8 steps in 2.88 s, **about 2.8 steps a second** (one sample, timing about 0.03 s at each end, so about 2%). A lead. The drill's earlier 3.4 (read at a 90 ms grab step, ±0.4) is not confirmed; which gait this is (jog or sprint) is not known from this view.
- **Step length, fails as written.** A run has no moment with both feet down (a flight phase between steps), so "the gap between the heels when both feet touch" does not exist for runs; it holds for walks only. Read instead as the landing positions against the pavement tiles in the side-on stretch at 554.8 to 555.6 s: the camera swings round during it and the front foot leaves the bottom of the picture at each landing, so no landing was seen. Nothing measured.
- **What it implies if the gait is the jog (4.5 m/s):** a step of about 1.6 m; if the sprint (5.5 m/s), about 2.0 m. Neither checked.
- An automatic count of white sole pixels (fixed crop) was tried and read the pavement instead: by-eye crops only.

## Next (try 2, a different reading of step length; the check's last try before the method is questioned)
Runs: step length = the distance between successive landings against a fixed ground mark, read side-on with the camera still and both landings in the picture; marks with a ratio to the body taken in the same frame (tile pitch, kerb stones). Walks keep the heel-gap reading. If no such stretch is found in two uncut Sleeping Dogs clips, the speeds are read as cadence only (leads) and the method is questioned in a dated note before KCD2, GTA V or RDR2 are read.

## Try 2 and the method questioned (24 Nov 2026, 11:46 to 11:48 Swiss)
Searched for a side-on, still-camera run with both landings in the picture: CGho8_UOzSk whole (coarse sheets every 53 s and at 3 s around 555 to 588 s) and nDThIiEgyDA (16 h walkthrough, uploaded date not read) at 300 to 2,000 s every 50 to 100 s: cutscenes and a following camera behind or three-quarter throughout; none found. By the rule above, step length is set aside: **from footage, on-foot speeds are cadence only, as leads.**
The question for the method: a following third-person camera never shows the ground a step covers, so speed cannot be built from footage alone in these games. What could: (a) our own scripted runs of the installed games (allowed: played offline by scripts outside the game, 17 and 23 Nov) where the game shows a distance (Sleeping Dogs' marker readout gave the solid 5.5 and 4.5 m/s); (b) footage passing objects whose size the same frame gives against the character (doorways, kerbs) where the camera holds side-on, rare. Recommendation: (a), KCD2 and GTA V first, priced before it starts; footage keeps the cadence and the gait shapes. Not yet decided; the next session prices (a).

## Priced (24 Nov 2026, 11:53 Swiss; estimates, marked)
The Sleeping Dogs drill cost about 0.85 h logged and about 2.75 h of wall time (22:05 to 00:50, three runs lost) once its launch script existed. Scripted runs give speed only where the game shows a distance or a ruler sits in view: Sleeping Dogs' marker readout did; KCD2 and GTA V show none found so far (GTA V's first-person view and its road dashes are a candidate ruler, size unverified; KCD2 none). So (a) costs per game about 0.5 h to find and check a ruler, then about 3 h for the harness and five runs a gait; without a ruler it fails as footage did. Being seen in KCD2 needs no ruler (times only): about 3 h harness plus 1.5 h for five staged incidents a kind. Order: KCD2 being seen first (no ruler risk), then GTA V's ruler check, then on-foot runs.

## Withdrawn (2026-11-24 12:41 Swiss)
The order above is withdrawn: the GTA V and KCD2 copies on this PC are not run (DECISIONS 23 Nov 15:26 and 20:30, replaced unsigned program files). On-foot speeds for KCD2 and GTA V stay cadence leads from footage; KCD2 being seen goes back to long uncut footage. Sleeping Dogs and our own build stay the only drill games.
