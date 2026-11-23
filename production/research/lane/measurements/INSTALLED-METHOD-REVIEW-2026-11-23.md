# Review of INSTALLED-METHOD.md (fresh reviewer, 23 Nov 2026)

Built on: INSTALLED-METHOD-NOTES-2026-11-23.md and FRAMETIME-METHOD-2026-11-17.md (the sources the method was checked against).

Checked against INSTALLED-METHOD-NOTES-2026-11-23.md, the questions, FRAMETIME-METHOD-2026-11-17.md and advisor 328's brief. Cited items were looked up in STATUS.md, DECISIONS (23 Nov), RULINGS (29 and 30 Oct) and the allowlist. Nothing was run.

## 1. Claims the notes do not support, or that are not marked

- "so input and video share one clock" (step 3). The notes say alignment is "UNVERIFIED" and "How a recorder's pts map to QPC time: not read". Fitting the offset to "the first frame that moves after the input" in each run is also circular. It counts the game's response delay as zero, so a punch's wind-up and the start of throttle or braking cannot be measured. Each session needs one shared clock (the recorder's start logged on the same counter, or one calibration event).
- "ffmpeg's desktop-duplication source keeps microsecond frame times". The notes say "Partly UNVERIFIED" (code read through a fetch summary), and the times count from "the first request". It is not in Gaps.
- "edges at 1 s or finer". STATUS.md's rule is "a step finer than the thing measured". A 1 s step cannot time a punch.
- "known lengths in view (lane marks, car lengths, kerb stones)". The notes say "UNVERIFIED as professional practice", and the method gives no way to learn those lengths in each game.
- "Openings with skilled real-time play (shooting, races) are where a script fails". The notes say "no source read. UNVERIFIED." It is not marked.
- "Sleeping Dogs (GOG installer signed) may be run", against the method's own rule that "program files carry the publisher's valid signature". A signed installer does not show a signed program. DECISIONS 15:26 records only the installer.

## 2. What the brief asks for that the method misses

- "A set speed": the method never says how one is reached without a speedometer (for example, a fixed throttle time from standstill).
- Runs: no save reload before each run, no warm-up pass to discard, and no rule to add passes when the spread is high (FRAMETIME section 6).
- Frame times: FRAMETIME's procedure is not carried over (VSync and frame generation off, MsBetweenAppStart, administrator rights or Performance Log Users). Recording the screen adds load, so frame-time runs should be kept apart from recorded drills.
- Two stars, then the same escape: police and traffic vary from run to run, so a blind script cannot repeat it. That is skilled play, for footage, unless a fixed route is shown to work. The star reader was built on GTA's HUD; Sleeping Dogs, the only game that may be run, has its own.
- "Openings got through once": the method never says who plays them. A script plays blind, and reading frames to choose keys amounts to computer use.

## 3. Unsafe or unworkable

- Timing: the notes leave Sleep and timer resolution "UNVERIFIED" and give a clock tick of 15.625 ms. The performance counter stamps times; it does not schedule inputs. Log the counter just before and after each SendInput, treat that log as the truth, and busy-wait for short holds. Add this to Gaps.
- Recording rate is never set. The default is 30 fps (33 ms steps), and dup_frames=1 adds copied frames. Set 60 fps or more and turn duplicates off.
- Focus and stuck keys: SendInput goes to whichever window is in front and "does not reset the keyboard's current state". The method has no check that the game is in front, no release of every key at the end or on a crash, and no stop when he comes back. A Windows Security box would receive the keys.
- Permission: scripted keys into a game are simulated keyboard input. RULINGS 29 and 30 Oct allow computer use only in Marvelous ("other apps need his page yes"). No page yes is cited.
- ffmpeg is not on the allowlist (only PresentMon, item 12). DECISIONS 23 Nov 13:51 records "no download ... without his word in chat". By the reviewer's own knowledge (not in the notes), ffmpeg.org publishes no Windows builds, so "official releases" needs naming.
