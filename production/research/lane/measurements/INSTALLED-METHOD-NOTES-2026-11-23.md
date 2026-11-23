# Installed-game measuring: reading notes (read 23 Nov 2026)

Built on: FRAMETIME-METHOD-2026-11-17.md (PresentMon, benchmark practice) and GAME-TERMS-AND-STUDY-LAW-2026-11-17.md.

Answers INSTALLED-METHOD-QUESTIONS.md. Notes only; no synthesis. Builds on FRAMETIME-METHOD-2026-11-17.md (sections 5 anti-cheat and 6 benchmark practice read again, not repeated). All "read" dates are 23 Nov 2026. UNVERIFIED = not confirmed from a primary page read in full.

## Q1. How professionals measure a shipped game's movement and vehicle feel from outside

- No primary source on this was reached in this pass. Swink's Game Feel, GDC talks, Digital Foundry and automotive-sim reviewer methods: not read. All UNVERIFIED.
- Speedrun community timing from video (speedrun.com FAQ) refused: HTTP 403. Not used.
- Nothing here confirms a named professional method for top speed, time to top speed, braking distance or turning radius from outside a game. Q2, Q4 and Q5 below give only the measurement pieces (distance references, recording, timing, repeats).

## Q2. Distance without a speedometer

- No primary source reached that states the known-length, map-coordinate, pixel-motion or landmark-time methods as practice. UNVERIFIED as "professional practice".
- Only usable facts read: a QPC timestamp has a resolution of 1 microsecond or better and a +/-1 tick quantisation; for short intervals oscillator error is negligible (+/-10 ppm gives +/-10 microseconds per second) (https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps, read 23 Nov 2026). This bears on the time half of "time between landmarks", not on the distance half.
- The video side's frame quantum is set by recording rate (Q4): ddagrab pts are in microseconds but frames arrive paced at the set framerate (default 30).

## Q3. Repeating inputs exactly from outside

Microsoft docs (read in full):
- KEYBDINPUT: `KEYEVENTF_SCANCODE` (0x0008): "If specified, wScan identifies the key and wVk is ignored." Remarks: scan code input "is useful for simulating a physical keystroke regardless of which keyboard is currently being used"; "The virtual key value of a key can change depending on the current keyboard layout... but the scan code will always be the same." The `time` field is the event timestamp in ms; "If this parameter is zero, the system will provide its own time stamp." https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput (page dated 2023-05-02, read 23 Nov 2026).
- SendInput: events inserted serially, not interspersed with other input; it is "subject to UIPI. Applications are permitted to inject input only into applications that are at an equal or lesser integrity level"; when blocked by UIPI neither return value nor GetLastError reports that cause; it "does not reset the keyboard's current state" (held keys may interfere; check GetAsyncKeyState). https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-sendinput (read 23 Nov 2026).
- Keyboard input overview: WASD game bindings given as the example where scan codes are needed to be layout-independent; scan code table lists W 0x11, A 0x1E, S 0x1F, D 0x20, Space 0x39, Enter 0x1C, Esc 0x01, LeftShift 0x2A, LeftCtrl 0x1D. https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input (updated 2026-07-08, read 23 Nov 2026).
- That a given shipped game ignores virtual-key SendInput but honours scan codes: no primary source read. UNVERIFIED. (Games that read via DirectInput or Raw Input: the Raw Input page read lists WM_INPUT and RAWKEYBOARD but does not say whether injected input reaches it. UNVERIFIED.)

Timing precision:
- QPC is the Microsoft-recommended method for time-stamping and short intervals; resolution 1 microsecond or better; frequency fixed at boot; examples of 10 MHz under a hypervisor. https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps (read 23 Nov 2026).
- The same page's clock table lists the PC RTC at 15.625 ms resolution (64 Hz) and says GetTickCount-type calls suit "resolution of 10 to 16 milliseconds". These bound how accurately a script can sleep or time between sends if it uses coarse clocks. Sleep and timer-resolution behaviour: page not read. UNVERIFIED.

AutoHotkey v2 docs (read in full):
- SendMode: Event (slowest, 10 ms default key delay), Input (default, fastest, "usually most reliable", limited to about 5000 characters), Play (sends to the active window, "wider range of games", deprecated, can fail under UAC, "may have no effect on Windows 11 and later"). https://www.autohotkey.com/docs/v2/lib/SendMode.htm (read 23 Nov 2026).
- Send: `{vkXXscYYY}` sends a key with a given scan code; "Send may have no effect if the active window is running with administrative privileges and the script is not" (UIPI); SendPlay "can work in cases where the other modes fail, particularly in some games". https://www.autohotkey.com/docs/v2/lib/Send.htm (read 23 Nov 2026).

Virtual gamepad:
- ViGEmBus: a Windows kernel-mode driver emulating Xbox 360 and DualShock 4 controllers; games see real hardware. Needs driver installation (pre-built signed binaries from an all-in-one setup; self-built drivers need signing or test mode). README states "THIS PROJECT HAS BEEN RETIRED"; repository archived 2 Nov 2023; licence BSD-3-Clause; v1.17+ supports Windows 10 and 11. https://github.com/nefarius/ViGEmBus (read 23 Nov 2026). Note for the project: a driver install is needed (the question asked for this to be noted).

Anti-cheat or launcher in offline single-player:
- FRAMETIME file section 5 (read 23 Nov 2026): no primary source that capture tools are banned; blocking considered possible.
- For SendInput, scripting or virtual pads specifically in GTA V, GTA IV, Sleeping Dogs, RDR2 offline: no primary source reached. UNVERIFIED. (GTA V's BattlEye and RDR2's Rockstar launcher behaviour: not read.)

## Q4. Screen recording with timestamps, input alignment

- ffmpeg gdigrab (https://ffmpeg.org/ffmpeg-devices.html, read 23 Nov 2026, via fetch summary): `framerate` default `ntsc` (30000/1001); `draw_mouse` default 1; `show_region`; `offset_x/offset_y`; `video_size`. The page text read gave no timestamp description for gdigrab.
- ddagrab filter source (libavfilter/vsrc_ddagrab.c on master, read 23 Nov 2026 via raw.githubusercontent.com): options `output_idx` 0, `draw_mouse` 1, `framerate` "30", `video_size`, `offset_x/y`, `output_fmt` 8bit, `allow_fallback` 0, `force_fmt` 0, `dup_frames` 1 ("duplicate frames to maintain framerate"). Frame pts for a new capture = current time since the first request, in microseconds; output time base 1/1000000; the source comment notes AcquireNextFrame "sometimes has bursts of delay"; with dup_frames off, no duplicates and output rate can fall when the screen is static. The filter's doc section in ffmpeg-filters.html was not located in the fetched chunks, so the doc text was not read; the above is from code, as summarised by the fetch tool (not read line by line by this reader). Partly UNVERIFIED.
- Whether ddagrab or gdigrab can capture exclusive-fullscreen games: not confirmed. UNVERIFIED. (FFmpeg wiki page blocked: "Access Denied" bot-protection page.)
- OBS Studio and ShadowPlay: OBS video-recording-guide URL returned 404; ShadowPlay not searched. Not reached.
- Input-to-video alignment: no primary source read on on-screen marker, audio click or input log methods. UNVERIFIED. What the read docs give: SendInput's `time` field is system-supplied when zero; QPC supplies a monotonic microsecond clock independent of system time (https://learn.microsoft.com/en-us/windows/win32/sysinfo/acquiring-high-resolution-time-stamps, read 23 Nov 2026), and GetSystemTimePreciseAsFileTime is the UTC-synchronised alternative. How a recorder's pts map to QPC time: not read.

## Q5. How many repeats, how spread is reported

- Already in FRAMETIME file section 6 (not repeated): GamersNexus "a minimum of 4 times and averaged"; "When deviation runs high, we typically just run more test passes"; error bars; CapFrameX more than 1000 frames for P0.1/P0.2 (read 17 Nov 2026).
- "Five-sample rule": no primary source found or read. UNVERIFIED as an established rule.
- Nothing further read this pass.

## Q6. GTA V, GTA IV, Sleeping Dogs

Opening length before free roam (none confirmed in minutes):
- GTA V: Wikipedia says the world "may be fully explored after the opening prologue without restriction"; prologue length and content not stated. https://en.wikipedia.org/wiki/Grand_Theft_Auto_V (first 100,000 chars read, 23 Nov 2026). Fandom mission page: HTTP 402, not read. Minutes: UNVERIFIED.
- GTA IV: Wikipedia says free roam is restricted at the start: initially only Bohan, Broker and Dukes; bridges locked "due to a terrorist threat" with police pursuit; other islands unlock with story. Exact point free roam begins not stated. https://en.wikipedia.org/wiki/Grand_Theft_Auto_IV (first 100,000 chars of 225,160 read). Fandom page 402. Minutes: UNVERIFIED.
- Sleeping Dogs: Wikipedia "The initial missions of the game are a linear tutorial for controlling the character" and "After these missions, the player is allowed to explore the game's world"; some areas locked until milestones. https://en.wikipedia.org/wiki/Sleeping_Dogs_(video_game) (first 100,000 of 131,069 chars read). Minutes: UNVERIFIED.
- Which parts need skilled real-time play: no source read. UNVERIFIED.

Replay tools:
- GTA V Rockstar Editor: Wikipedia says it "lets players capture and edit gameplay videos" on PC; Director Mode is mentioned only in the April 2022 re-release context. A Rockstar support search summary (https://support.rockstargames.com/articles/4gZPiqdUZD8ZhaJ81IPDJr/how-to-record-clips-and-access-the-rockstar-editor-in-gtav-on-pc) said clips from Story Mode and Online can be recorded, the Editor is reached from the pause menu's rightmost tab and not from GTA Online; the page itself timed out when fetched, so this is from a search summary, UNVERIFIED. Director Mode detail: third-party only, UNVERIFIED.
- Rockstar Editor frame-by-frame or deterministic replay behaviour (does it re-render from recorded data, camera control): not read.
- GTA IV: Wikipedia says the PC port added a Video Editor; no dedicated replay mode or mission-replay menu mentioned in the part read. https://en.wikipedia.org/wiki/Grand_Theft_Auto_IV.
- Sleeping Dogs: no replay tool read.

Built-in benchmarks:
- GTA V: the benchmark "appears only in story mode, and not always"; run by pressing Tab or the bottom-right button after applying settings; five test sections, the last "most representative of gameplay"; results as text files with minimum and average frame rates per section. Source: Corsair guide for GTA V Enhanced (path Documents\Rockstar Games\GTAV Enhanced\Benchmarks), https://www.corsair.com/us/en/explorer/gamer/gaming-pcs/how-to-benchmark-gta-v-enhanced/ (read 23 Nov 2026). Secondary source; applicability to the original PC release UNVERIFIED (the guide says the same process).
- GTA IV: a community forum post (Beyond3D, from search results, not opened) lists a `-benchmark` launch parameter and a Benchmark.cli results file; Rockstar's GTA IV troubleshooting article is said to mention a benchmarking utility. Neither page was read. UNVERIFIED. Note the launch parameter question falls under the guard "no mods, script hooks"; a command-line flag is not a mod, but this was not assessed.
- Sleeping Dogs: one third-party guide (search result only) says a Benchmark Mode exists in display options. UNVERIFIED. Feral manual (Mac) not relevant.

## Q7. RDR2

- Built-in benchmark: Rockstar support page "RDR2 Benchmark Test" (https://support.rockstargames.com/articles/69mcPf8HikSaZ5mS20rK6k/rdr2-benchmark-test) exists; the page itself timed out on all three attempts. The search tool's summary of it: Settings, Graphics, "Run Benchmark Tests", confirm prompt, results saved in Documents\Rockstar Games\Red Dead Redemption 2\Benchmarks. From a search summary, UNVERIFIED.
- Opening length before free roam: Wikipedia RDR2 article (first 100,000 of 243,264 chars read, 23 Nov 2026) says "Outside of missions, they can freely roam the interactive world" but does not give prologue or chapter structure or when free roam begins. Minutes: UNVERIFIED.

## Unreached

- Swink "Game Feel", GDC Vault talks, Digital Foundry methods, automotive-sim reviewers: not searched or read.
- speedrun.com FAQ: HTTP 403.
- GTA and Sleeping Dogs Fandom wiki pages: HTTP 402.
- FFmpeg wiki Capture/Desktop: bot-protection "Access Denied".
- ffmpeg-filters.html ddagrab doc section: not found in the chunks read (large page; only the code was read).
- OBS video-recording-guide: 404. ShadowPlay: not searched.
- Rockstar support pages (Rockstar Editor, RDR2 benchmark): timed out; used search-result summaries only (marked UNVERIFIED).
- Microsoft Raw Input "About Raw Input" page (injected input behaviour), Sleep/timer resolution page: not read.
- GTA IV Rockstar troubleshooting page, Beyond3D thread, Sleeping Dogs benchmark source: search results only.
- Anti-cheat statements for the four games: none found.
- ViGEmBus's linked end-of-life statement: not followed.
