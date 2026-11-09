# The AI-video motion experiment: shot rules, start frames, prompts and run order (9 Nov 2026)

Inputs: STOCK-FOOTAGE-2026-11-09.md (the three motions, stock control clips, Epic's guidelines page read 9 Nov), TOOLS-2026-11-09.md (pieces and licences), BRIEF-1 and BRIEF-2 (the advisor's web research, unread by this session; cited as "advisor brief 1/2"), and today's test run log C:\LedgerTools\ai-video\out\test33.log (read 9 Nov 2026). Nothing in this note has been run except the 33-frame test; every time below past 33 frames is an estimate.

Reference games: Mafia and Kingdom Come II are not known to make body motion from generated video; no method of theirs applies to this step (none found). The method followed is the advisor's (brief 1: image to video from a render of our own scene, static camera prompted, one subject, the motion step by step) checked against Epic's capture rules.

## 1. Shot rules (all three motions)

From Epic's capture guidelines (https://dev.epicgames.com/documentation/metahuman/metahuman-animator-video-capture-guidelines-in-unreal-engine, read 9 Nov 2026 in STOCK-FOOTAGE section 3; also as the advisor's brief 2 states them):
1. Whole body head to feet in every frame, with a clear margin on all sides. Working figure for this note: the performer's height at most 75% of the frame height, at least 8% of the frame free under the soles and above the head (a choice, not Epic's number).
2. Camera straight on, at neutral height (about chest to waist height of the performer), still for the whole clip. The start frame's camera is locked; the prompt says so; the negative prompt bans every camera move.
3. Even, diffused light, no harsh shadows, no backlight, no motion blur. Render the start frame with motion blur off and a flat, overcast-style light.
4. Performer distinct from the background; a clear floor line; matte floor and wall, no glass, no wet or shiny ground (the game's wet street coat is out for these frames).
5. Fitted clothes, shoes visible and contrasting with the floor; no long loose coat or wide trousers.
6. One performer; nobody else in frame, no reflection of anyone.
7. Nothing blocks any part of the body: a side-on stool or an open chair (no arms, open back, legs thin), a wall or rail instead of a solid counter; small props only.
8. Video models drop small objects (Bugliarello, CVPR 2026, per advisor brief 2; not read here: unverified). Keep props few, large enough to read at 480 px, and in the start frame already.

Model limits (TOOLS note, sd.cpp docs/wan.md read 9 Nov by the session): 480x832 (portrait) or 832x480 (landscape), cfg 6, euler, flow shift 3, 20 steps (today's log), --offload-to-cpu, diffusion flash attention (the log warns --diffusion-fa is deprecated: use "--flash-attn off,diffusion=on"). Frame counts must be 4n+1. Wan 2.2 TI2V 5B plays at 24 fps (advisor brief 1; unverified here: record the frame rate the output file carries). First-and-last-frame pinning is named by brief 1 for sd.cpp, but whether it works with TI2V 5B is unverified; not planned.

## 2. Run time, from today's figure

Measured (test33.log, 9 Nov): 33 frames at 480x832, 20 steps at about 55 s each, sampling 1,103.8 s; VAE decode 191.9 s only after two out-of-memory retries and a fall to 112x208 tiles; total 1,304.4 s. Text encoding 6.8 s, image encoding 1.6 s.

Estimate method: latent frames L = (frames - 1) / 4 + 1 (33 frames = 9). The decode scales with L. Sampling scales between linearly with L (the layers) and with L squared (attention); the central figure assumes 15% of today's sampling time was attention (an estimate from the model's shape, not measured). Low = linear, high = all quadratic would be far above the central figure and is given as the ceiling.

| Frames | Seconds at 24 fps | L | Low | Central | Ceiling |
|---|---|---|---|---|---|
| 33 | 1.4 | 9 | 1,304 s measured | 22 min | |
| 49 | 2.0 | 13 | 31 min | 33 min | 43 min |
| 81 | 3.4 | 21 | 50 min | 59 min | 108 min |
| 97 | 4.0 | 25 | 60 min | 74 min | 151 min |
| 121 | 5.0 | 31 | 74 min | 98 min | 229 min |

Risks: a longer clip may also run out of memory in sampling (unmeasured); if it does, the clip drops to the next shorter length once, and that is recorded. Turn VAE tiling on from the start so the two failed decode tries are skipped (option name as in sd.cpp's docs/wan.md; not re-read here). The video model uses the graphics card: never at the same time as an Unreal render, the runner's performance step or the night jobs (local 01:30, 03:30, 04:15).

## 3. Seed plan

Three seeds per motion, the same three for every motion so results compare: 1101, 2202, 3303. Prompt, start frame, settings and frame count are fixed across the three seeds; only the seed changes. File names carry motion, frame count and seed (for example m2-81f-s1101). Each run's log is kept beside its clip.

## 4. The three motions

### Motion 2: lean, shift weight, glance aside (run first)
- Start frame: portrait 480x832. One loyalist from the game's scene (Ron Kirby, or whoever has passed dressed views; the session's choice), whole body, feet with margin, about 70% of frame height. He stands side-on to a plain matte wall, shoulder and hip touching it, arms folded or hands in jacket pockets, weight on the leg nearer the wall, head facing camera-forward. Flat grey-brown wall, darker matte floor, clear floor line. No counter, no rail in front of him. Camera straight on, chest height, wide lens avoided (about 35 to 50 mm equivalent).
- Frames: 81 (3.4 s). Central 59 min a clip, three seeds about 3 h.
- Prompt: "Static camera, fixed tripod shot, full body visible from head to feet. A man in his fifties in a fitted dark jacket and trousers leans with his shoulder against a plain wall. He slowly shifts his weight from one leg to the other, settles, then turns his head to glance to his left for a moment and looks back ahead. Natural, unhurried movement, realistic body weight. Even soft daylight, plain background, matte floor."
- Negative prompt: "camera movement, pan, tilt, zoom, dolly, handheld shake, cut, cropped feet, cropped head, out of frame, motion blur, extra person, crowd, reflection, extra limbs, deformed hands, morphing, flicker, text, watermark, logo, children, alcohol, bottle, glass, counter, table"
- Check: whole body head to feet with margin in every frame; camera drift (a fixed background point moves under 2 px across the clip, measured on the wall line and floor line); no extra limbs or body melt; the glance and weight shift both happen; timing near the stock control's pace (STOCK-FOOTAGE, motion 2 candidates).

### Motion 3: a woman lights a cigarette and smokes (run second)
- Start frame: portrait 480x832. A woman from the game's scene (Sheila Dunn, 53, if a dressed model exists; the session's choice), whole body, feet with margin. She stands front-on to slightly three-quarter, in fitted clothes (a short fitted coat or a cardigan, no long loose coat), in front of a plain matte wall. Already in her hands in the start frame: an unlit cigarette in one hand near the chest and a lighter in the other, both large enough to read at 480 px. Whether the game has cigarette and lighter meshes is unchecked; if not, a simple pair is needed for this frame (reuse first). No bus shelter glass.
- Frames: 121 (5.0 s; lighting, a draw and an exhale need it). Central 98 min a clip, three seeds about 4.9 h. If time is short, 97 frames (4.0 s, central 74 min) with the exhale cut.
- Prompt: "Static camera, fixed tripod shot, full body visible from head to feet. A woman in her fifties in a fitted cardigan and skirt to the knee stands by a plain wall holding a cigarette and a small lighter. She raises the cigarette to her lips, cups the lighter in front of it and lights it with a small flame, lowers the lighter, takes a slow draw, lowers her hand and breathes out a thin stream of smoke. Natural, unhurried movement. Even soft daylight, plain background, matte floor."
- Negative prompt: as motion 2, plus "dropped cigarette, missing lighter, prop vanishing, second cigarette, large fire, sparks"
- Check: as motion 2, plus props kept: the cigarette visible in every frame, the lighter present until it is lowered, the flame appears once near the face; hands do not merge with the props. Tobacco is allowed; no alcohol in frame.

### Motion 1: rise from a chair and walk (run last)
- Start frame: landscape 832x480 (the walk needs width; same token count and time as portrait). One man from the game's scene, whole body, feet with margin, about 70% of frame height while standing (seated he is lower: frame for the standing height). An open chair or stool, side-on to the camera, legs thin, no arms, at the left third; he sits on it facing right in profile, hands on knees, feet flat. Plain matte wall, darker matte floor, clear floor line.
- "Walk out" is changed to "walk to the right third and stop": walking out of frame breaks rule 1. If the solve needs the exit, the session decides it separately.
- Frames: 97 (4.0 s: about 1.5 s to rise, two or three steps, a stop). Central 74 min a clip, three seeds about 3.7 h.
- Prompt: "Static camera, fixed tripod shot, full body visible from head to feet, side view. A man in his fifties in a fitted dark jacket and trousers sits on a plain wooden chair. He leans forward, pushes up with his hands on his knees, stands, then walks three steps to the right across the room and stops, still fully in view. Feet stay planted on the floor with each step, realistic weight and walking pace. Even soft daylight, plain background, matte floor."
- Negative prompt: as motion 2, plus "sliding feet, floating, moonwalk, walking out of frame, chair moving by itself"
- Check: as motion 2, plus: the chair stays where it was; the whole body stays in frame at the walk's end; step count and pace near the stock control (Pexels 6615631 played backwards, or 10567419; STOCK-FOOTAGE, motion 1). Foot contact: expect sliding (ViMoGen, https://arxiv.org/html/2510.26794v1, per advisor brief 2: about four times the foot sliding of text-to-motion; GenMimic, https://arxiv.org/html/2512.05094v2, per advisor brief 1: steps and turns about 40% usable; neither read here). Plan cleanup after the solve: mark each foot's planted frames (foot speed near zero and lowest height), lock the foot there and solve the leg back with two-bone IK, then measure the sliding left (centimetres per planted frame) before and after.

## 5. The 60 fps HD copy (solve test)

Each kept clip is solved twice: native (24 fps, 480 px), and as a copy interpolated to 60 fps then scaled to HD. Epic asks for HD or 4K at 60 fps and H.264 at CRF 18 or better (guidelines page above). The capture data and the image source carry the same frame rate (advisor brief 2). The solver's result on each is recorded; which one it handles better is part of the finding.

- Scale: portrait 480x832 by 2.25 to 1080x1872 (landscape 1872x1080), Lanczos, in FFmpeg. Upscaling adds no detail (brief 1: "no upscaling"); it only meets the size rule.
- 24 to 60 fps is 2.5 times, not a whole multiple: interpolate to 120 fps (5 times) and keep every second frame, or use an interpolator that takes a time step.

Interpolator candidates (licence pages read 9 Nov 2026, through a summarising fetch tool):

| Candidate | Licence (page read) | Weights | Fit |
|---|---|---|---|
| Practical-RIFE, https://github.com/hzwer/Practical-RIFE | MIT, https://raw.githubusercontent.com/hzwer/Practical-RIFE/main/LICENSE (full text read) | README: "The content of these links is under the same MIT license as this project" (Google Drive, Baidu) | --multi, --fps options; whether --fps 60 from 24 works with non-whole steps is unverified. Python and PyTorch: no PyTorch for this card (TOOLS note), so CPU only. |
| rife-ncnn-vulkan, https://github.com/nihui/rife-ncnn-vulkan | MIT, https://raw.githubusercontent.com/nihui/rife-ncnn-vulkan/master/LICENSE (full text read) | Models bundled (rife-v4, v4.6 and older); their licence not stated on the page: unverified (they come from RIFE, MIT) | Windows build for AMD on Vulkan; -n target frame count, -s time step 0 to 1. Best fit for this PC. Recommended first. |
| FILM, https://github.com/google-research/frame-interpolation | Apache 2.0, https://raw.githubusercontent.com/google-research/frame-interpolation/main/LICENSE (grant and commercial terms read; extracts, not the whole text) | Pretrained models' licence not stated in the README: unverified | Recursive midpoints only (2^n), so 24 to 96 then drop to 60 is uneven; TensorFlow. Second choice. |
| IFRNet, https://github.com/ltkong218/IFRNet | MIT, https://raw.githubusercontent.com/ltkong218/IFRNet/main/LICENSE (full text read) | Weights' licence not checked: unverified | PyTorch, CPU only here. Third choice. |
| AMT, https://github.com/MCG-NKU/AMT | CC BY-NC 4.0, https://raw.githubusercontent.com/MCG-NKU/AMT/main/LICENSE (read): "for NonCommercial purposes only" | | Excluded on licence. |
| FFmpeg minterpolate and scaling, https://ffmpeg.org/legal.html | LGPL 2.1 or later; GPL if built with GPL parts, "notably libx264" (read) | none | Motion-compensated interpolation is a fallback only (warps bodies); FFmpeg is the scaler and encoder. libx264 makes the build GPL, which binds the program's distribution, not the clips; FFmpeg's page also warns of H.264 patent fees for products that make money from them (a processing tool here, not shipped). |

None of these is on the licence allowlist; PROCESS 2 there needs a decision record citing the weights licence before adoption (license-allowlist.md, per STOCK-FOOTAGE section 2). Not reached or not read: the licences of RIFE's bundled ncnn models, FILM's and IFRNet's pretrained weights; EMA-VFI and GMFSS (not looked at); the raw full text of the FILM licence (extracts only).

## 6. Order to run before the plugin solve

1. Start frames: render all three from the game's scene (Unreal; never while the video model or the runner uses the card). Check each against section 1 rules 1 to 7 by eye before any clip.
2. Motion 2, seed 1101 (in place, expected best: brief 1). Run its check. If it fails on camera drift or framing, fix the start frame or prompt once before more seeds.
3. Motion 3, seed 1101. Check, props kept included.
4. Motion 1, seed 1101. Check, foot contact noted.
5. Seeds 2202 and 3303 for each motion in the same order, only for motions whose first seed passed or failed on a fault a seed could change (props, drift), not on the start frame. Central time for all nine: about 11.5 h; first three alone about 3.9 h.
6. For each passing clip: the 60 fps HD copy (section 5), then the plugin solve on both copies, body only, preview character off (brief 2), and the stock control clip of the same motion solved beside them.
7. Motion 1's foot-contact cleanup after its solve, sliding measured before and after.
