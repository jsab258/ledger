<!-- Research note, 1 October 2026: written by a separate research helper given the problem (how game teams design an interface; in-world and minimal interfaces; subtitle and readability standards), saved by the design session as returned, apart from this line. -->

# How professional teams design a game interface, and the standards it must meet

Research, 1 October 2026, by a separate research helper.

Scope: the method from start to finish, then what the KCD2 and RDR2 teams did about in-world and minimal interfaces, then the legibility and subtitle numbers, then what this means for LEDGER's screens at 1920×1080 and 3440×1440. Font period look is a separate note and is not covered here, only legibility rules.

How reliable this is: the gateway refused most primary pages that day, including Microsoft's Xbox guidelines, the BBC guideline site, the Game Accessibility Guidelines site, Can I Play That, GDC Vault, W3C and most review sites. Epic's Unreal documentation, Wikipedia and GitHub opened. Each source in the list at the end is marked OPENED (read in full) or SNIPPET (known only from a search engine's summary). Before anything below hardens into a rule in DECISIONS.md, the numbers marked SNIPPET should be checked at source.

## (a) The professional pipeline, stage by stage

The order below is the common one in studio talks and books. What differs between studios is how much each stage costs, not the order. Each stage has its deliverable and the gate it must pass.

1. **Requirements and player needs.**
   - Deliverable: a screen inventory (every screen, overlay and prompt), the platforms, input devices, resolutions and aspect ratios, and the player's needs on each screen (what he must know, decide or do there).
   - Gate: sign-off by the design lead.
   - Hodent's framework is the usual yardstick. Usability has seven pillars: signs and feedback; clarity; form follows function; consistency; minimum workload; error prevention and recovery; flexibility (including accessibility). "Engage-ability" has three: motivation, emotion, game flow. [S8, S9]
   - Santa Monica's UI talk for God of War Ragnarök began from an internal critique of the previous game's UI and covered how to structure the UI team. [S5]
2. **Information architecture and flows.**
   - Deliverable: a flow chart or "wireflow" of how screens connect, including what Back and Esc do everywhere, and a ranking of the information on each screen.
   - Gate: walkthrough against the screen inventory. No dead ends, and every screen has a way back.
3. **Wireframes, or greybox UI.**
   - Deliverable: low-detail grey layouts with no styling, so the team argues about structure and not colour. These are often built straight into the engine as placeholder widgets, so the flow can be played early.
   - Gate: a usability walkthrough. Can a new player find Continue, change subtitle size and quit? [S50 snippets on generic UI pipelines]
4. **Art direction for the UI.**
   - Deliverable: a mood board, then a UI style guide. It covers a type scale (sizes for headings, body, labels and subtitles), a colour palette with its uses, iconography, materials and textures, spacing, and principles for motion and sound.
   - A useful rule from practice: interface colour usually comes from a narrow, desaturated slice of the world's palette, plus one accent the world does not use, so the accent always reads as "interface". [S51, snippet]
   - RDR2 separates decorative period lettering (titles, posters) from plain, legible type for menus, journal and HUD. [S41, snippet]
   - Gate: art director approval.
5. **Mock-ups or visual targets.**
   - Deliverable: paintovers on real in-game frames, at every target aspect ratio (for us, 16:9 and 21:9), showing the HUD at its busiest and at its emptiest.
   - Gate: director approval. For LEDGER this is "the overall look ... as whole frames", which goes on Jafar's page.
6. **Prototype.**
   - Deliverable: an interactive version, in the engine or a design tool, to test timing, navigation and reading speed before the art is final.
   - Gate: a usability test (stage 10).
7. **Component library, or UI kit.**
   - Deliverable: every reusable control with all of its states (normal, hovered, focused, pressed, disabled, selected): button, list row, slider, toggle, drop-down or carousel, tabs, scroll area, text input, key-glyph chip, tooltip, confirm dialog. Plus text styles and colour tokens.
   - Studios build these as "atomic" parts reused across screens and projects. [S6]
   - Focus states must be visible, because keyboard and gamepad users have no hover.
8. **Motion spec.**
   - Deliverable: how each element appears, changes and leaves, with durations and easing.
   - General interface practice: 100–200 ms for small feedback, and 200–400 ms for screen changes. Movement that starts fast and eases to a stop reads as responsive.
   - "Reduce motion" means fades instead of slides and scaling. [S52, snippet, general UI practice and not game-specific]
9. **Implementation in Unreal.**
   - **UMG** is the widget system. **CommonUI** is Epic's plugin, documented for UE 5.8 [S12]. It provides:
     - style assets kept separate from widgets;
     - an input routing system for layered UI;
     - button icons per platform and input device;
     - gamepad navigation in four directions.
   - Setup [S13]:
     - set the game viewport client class to `CommonGameViewportClient`;
     - make a `CommonInputActionDataBase` data table of UI actions;
     - make a `CommonUIInputData` asset for Click and Back;
     - make `CommonInputBaseControllerData` assets per input type, which supply the key glyphs.
   - Activatable widgets choose their focus target (`GetDesiredFocusTarget`, which Epic "strongly recommend[s]" you always implement) and set an input mode: Menu, Game or All. CommonUI restores the previous input config when a widget closes. [S14]
   - Lyra, Epic's sample game, layers its activatable widget stacks: Game, then GameMenu, then Menu, then Modal. [S22, snippet]
   - Lyra's **CommonLoadingScreen** plugin is a loading-screen manager that can be held open while anything is still loading. [S23, snippet]
   - **Scaling.**
     - The DPI scale rule options are Shortest Side, Longest Side, Horizontal, Vertical, Scale to Fit and Custom. Shortest Side is "the most common setting". [S15, S20]
     - The default curve keys are 480→0.444, 720→0.666, 1080→1.0, 8640→8.0, so the scale equals viewport height ÷ 1080. [S21, snippet from Epic's forum]
     - Epic advises authoring every widget at one reference resolution at scale 1.0. [S16, S19]
   - **Fonts.** Under Project Settings, User Interface, UMG Fonts, you can choose 72 DPI ("Default", the web and design-tool standard) or 96 DPI ("Unreal Engine", the old legacy setting). [S18]
     - This changes how a font "size" number turns into pixels, and Epic's pages and the search summaries disagreed on details.
     - Practical rule: **measure the rendered pixels in a screenshot, as the Xbox guideline does, rather than trusting the size field.**
   - **Safe Zone** widget: keeps children out of unsafe screen areas; debug display is on by default in the designer. [S17]
   - UMG good practice [S19]:
     - drive updates with events, not bindings or Tick;
     - use a Retainer to cache rarely changing widgets;
     - use a Scale Box, not render transforms, for permanent scaling;
     - make anything reused its own widget.
10. **Testing.**
    - Readability: measure text height in screenshots at each target resolution, using the Xbox method of drawing a box from the highest ascender to the lowest descender [S25]. Then look at it on the real monitor from the real seat.
    - Contrast: check against the worst background, such as sky, a lit wall or headlights.
    - Usability: think-aloud tests, where testers say what they are thinking while playing. [S10, S11]
    - Perception: Fortnite's team surveyed testers on whether icons read as intended. A trap icon was read as ammunition or trees. [S10, snippet]
    - Accessibility: review against the Xbox and Game Accessibility Guidelines checklists.

## (b) Immersive and minimal interfaces

### The taxonomy

Fagerholt and Lorentzon (Chalmers, 2009) sort interface elements on two axes: is it inside the story's world (fiction), and is it placed in the 3D scene (space)? [S1] That gives four kinds:
- **Diegetic**: in the world and the fiction. Dead Space's health bar on the suit's spine. [S4]
- **Non-diegetic**: neither. The classic HUD overlay.
- **Spatial**: in the 3D scene but not the fiction. A marker floating over an object, an outline.
- **Meta**: in the fiction but not in 3D space. Blood on the screen, a phone screen laid over the view.

Later findings:
- Removing the HUD raised expert players' involvement and sense of control. Novices lean on it more. [S2] This paper won CHI PLAY's 2025 Lasting Impact Award.
- In a 2018 controlled comparison, players monitored health better with a conventional HUD than with diegetic or spatial versions. The authors' conclusion: no type is best everywhere, so choose element by element. [S3]
- Ghost of Tsushima replaced waypoint arrows with the "Guiding Wind" blowing through the world, a common example of guidance without HUD. [S7]

### Kingdom Come: Deliverance II (Warhorse, February 2025)

- **Look.** Menus, inventory and codex are drawn as a medieval manuscript or codex. Maps are hand-illustrated in a period style; Paweł Kurowski is credited on the maps. Loading screens are original illustrations (19 reported) under art director Viktor Höschl. [S30, S31, S32, snippets]
- **HUD.** It shows a compass, health, stamina and a small crosshair (which can be turned off). The console variable `wh_ui_showHUD` hides the HUD entirely. [S33, snippet]
- **Hardcore mode** (patch 1.2.4, April 2025) removes the compass, map markers, fast travel and Henry's position on the map. You ask passers-by where you are. Warhorse's own words: "No map markers. No fast travel. No compass." [S34, snippets]
- **Interaction.**
  - Talk and use prompts appear when you look at something.
  - In dialogue the camera frames the speaker between letterbox bars. Options appear as a list, some with skill icons, and some are timed. [S35, snippets]
- **Subtitles.** Sizes "Classic", "Large" and "Extra Large"; speaker names; a "Contrast subtitles" background toggle. [S36, snippets]
- **On ultrawide, the game forces the subtitle background on.** A community fix says vanilla KCD2 "detects this and force-enables the subtitle background (ignoring your setting)". [S37, OPENED]
- **Criticism.**
  - Players report the UI does not scale on big screens, and font and HUD-size mods are popular. [S38, snippets]
  - A "Centered HUD" mod limits the HUD to a centred 16:9 area, because full-width placement "makes prompts easy to miss and requires far too much head movement". [S38, snippet]
  - There is no dedicated accessibility menu. [S36, snippet]
  - One reviewer called the UI "one of the worst UI/UX interfaces ever made", a minority view. Most praised its immersion. [S39, snippet]

### Red Dead Redemption 2 (Rockstar, October 2018; PC November 2019)

- **HUD.** Dynamic by default: elements appear only when relevant, for example the horse's stamina while galloping. [S40, OPENED]
  - Each element can be set to off, dynamic or always on, under Settings, Display. [S41, snippet]
  - Holding down on the D-pad cycles off, minimal and default. [S41, snippet]
  - The radar (mini-map) can be the normal mini-map, expanded, compass only, or off. With the radar off, a tap brings it back briefly. [S42, snippet]
- **Prompts.** You "focus" on a person by holding the aim button. Context prompts (Greet, Antagonize, Rob and so on) then appear bottom-right, with button glyphs and hold or tap instructions. [S43, snippets]
- **Menus and look.** Period print styling: menu and title type recalls wanted posters and newspapers, with plain type for reading. The shop catalogue is a browsable period catalogue. Arthur's journal holds his pencil sketches, and loading screens and title cards echo that sketch style. [S41, S44, snippets]
- **The map** is a paper-style map with filters. Holding the pause button opens the map directly, which reviewers praised. [S45, snippet]
- **Subtitles.**
  - On or off only, and small, with no size option. This was criticised by Can I Play That (accessibility review, 28 November 2018; deaf review, 19 February 2019) and by players.
  - They sit on a small dark backing that "only exceeds in a few millimeters that of the text", which helps readability.
  - "Subtitles Speaker Name" is a separate option, hidden in the Display menu.
  - Ambient townspeople's lines are subtitled only about half the time. [S46, S47, snippets]

### Others, briefly

- **Disco Elysium:** dialogue in a tall column at the right that scrolls up "like Twitter", always on a background, which its designers said helps legibility. A later update added larger font and UI options. [S48, snippets]
- **Mafia: Definitive Edition (2020):** a "Minimal HUD" mode and per-element toggles (markers, GPS, mini-map) were added after launch, plus Noir mode. It has speaker-tagged subtitles but no background, size or colour options, which Can I Play That criticised. [S49, snippets]
- **L.A. Noire:** the notebook holds clues, people and locations, and is used during interviews to pick questions. [S53, snippet]
- **Shadows of Doubt:** deliberately skeuomorphic. Evidence opens as case files; facts are joined with string on a cork board. [S54, snippet]
- **Hitman (World of Assassination):** most HUD elements can be switched off individually. [S55, snippet, low confidence on the details]
- **The Last of Us Part II (2020):** about 60 accessibility options, offered as presets:
  - Vision: high-contrast display, HUD scale Large, text-to-speech.
  - Hearing: subtitle names, subtitle direction, awareness indicators.
  - Motor: holds instead of repeated presses, auto pick-up.
  [S56, snippets]
- **Typed or spoken talk with AI characters:**
  - Vaudeville (released late 2025): reviewers note that "typing becomes challenging after a certain amount of words due to viewable chat window limitations". [S57, snippet, attribution to a specific review uncertain]
  - A KCD2 mod: hold V to speak, tap V to open a text box. Replies are spoken with 3D placement and shown in the HUD. [S58, OPENED]

## (c) Subtitles and readability: the numbers

**Pixel heights below are the ascender-to-descender height** (roughly the font size), as Xbox guideline 101 measures it, unless stated otherwise. The 1440 figures are the 1080 figures × 1.333, which is exactly what Unreal's default DPI curve does.

| Rule | 1080p | 1440p height | Source |
|---|---|---|---|
| Minimum text on PC (Xbox 101) | 18 px | 24 px (36 at 4K) | S24, S26 (snippet) |
| Minimum text on console / TV (Xbox 101) | 26 px | 35 px (52 at 4K) | S24, S26 (snippet) |
| Game Accessibility Guidelines (from Amazon's TV guidance): a floor, "not a target" | 28 px | 37 px | S27 (snippet) |
| Subtitle size, Hamilton (from Channel 4's HD broadcast requirement) | ≥ 46 px | ≥ 61 px | S29, S30 (snippet) |
| Subtitles larger than minimum text, scalable to ≥ 200% (Xbox 104) | — | — | S25 (snippet) |
| BBC online subtitles: font about 6.7% of picture height (validator accepts 2–8%); line height 120–125%; picture kept within 5–95% of the frame | about 72 px | about 96 px | S32 (OPENED) |

Note on the BBC row: 6.7% is a television and online-video figure, viewed from a sofa.

**Line length.**
- Xbox 104: at most 40 characters a line, 2 lines on screen. [S25, snippet]
- Hamilton: at most 38 characters; 2 lines, 3 only in exceptional cases. [S29, snippet]
- BBC: at most 68% of a 16:9 frame's width (Teletext's old limit was 37 characters). [S31, snippet]

**Speaker identification.**
- Xbox 104: name the speaker each time the speaker changes, or after a long pause; show direction when the speaker is not obvious. [S25, snippet]
- BBC: colour is the preferred method, in priority order white #FFFFFF, yellow #FFFF00, cyan #00FFFF, green #00FF00. If colour cannot be used, put each speaker on a new line starting with a dash. [S31, S32]
- Hamilton: offer a choice of no speaker marking, colours, or names. [S29, snippet]

**Background.**
- Xbox 104: players can put a solid background behind subtitles and adjust its opacity from 0 to 100%. [S25, snippet]
- Hamilton: a semi-opaque (50%) box as a sensible default. [S29, snippet]
- BBC: white text on a black box, one box per line (span), never across the whole region. [S32]

**Font.**
- Xbox 104: at least one sans-serif option; mixed case, not all capitals. [S25, snippet]
- BBC: Reith Sans; Tiresias Screenfont for broadcast. [S31, snippet]

**Contrast.**
- WCAG 2.2: text at least 4.5:1 (AA); large text 3:1, where large means ≥ 18 pt (about 24 px) or ≥ 14 pt bold (about 18.7 px). The enhanced level is 7:1 and 4.5:1. Non-text interface parts are 3:1. [S34, snippet; W3C refused]
- Xbox 101 also asks for 4.5:1 for important text. [S24, snippet]

**Timing.**
- BBC: 160–180 words a minute, about 0.3 s per word as a minimum time on screen. [S31, snippet]
- Ofcom's 2006 guidance had the same range. Ofcom's statement of 15 April 2024 **removed** the numeric words-a-minute targets in favour of quality and synchronisation. [S33, snippet]

**Subtitles on or off by default.**
- Ubisoft data shown by Ian Hamilton: about 95% of Assassin's Creed Odyssey players kept default-on subtitles on, and 97% in Far Cry New Dawn. With subtitles off by default (Origins), 60% turned them on. [S59, snippet]

**Size in terms of the eye (my working, not a published rule).**
- Reading speed falls off sharply below a lower-case letter height ("x-height") of about 0.2° of visual angle. Fluent reading spans about 0.2° to 2°. [S35, snippet]
- Assume x-height is about half the font size. Then Channel 4's 46 px on a 55-inch 1080p TV at about 2.75 m gives about 0.30°.
- A 24-inch 1080p monitor at 65 cm needs only about 25 px for the same angle.
- 36 px on that monitor is about 0.44°. On a 34-inch 3440×1440 monitor at 70 cm, 48 px is about 0.46°. I assumed 34 inches because that is the common size for this resolution; Jafar's actual size is unknown.
- So for a PC monitor, a default of **36 px at 1080 (48 px at 1440)** is about 1.5 times the angle of TV broadcast subtitles, with room to grow.

## (d) What this means for LEDGER

### Ground rules for every screen (recommendations, drawn from the above)

1. **Author at 1920×1080, Shortest Side rule, default curve.**
   - At 3440×1440 the engine scales ×1.333, so text grows with height and nothing needs sizing twice.
   - The canvas there is 2580×1080 units.
2. **Ultrawide.**
   - Everything the player must read or act on (prompts, subtitles, typing box, key hints, the loading bar) goes in a **centred 16:9 region**: 1920 units wide, which is 2560 px on 3440, leaving 440 px each side.
   - Full-width elements are only backgrounds, art and the notebook's spread.
   - Offer a setting, "Interface width: 16:9 (default) / Full width". Players asked for both: KCD2 players modded the HUD into the centre, and Horizon Forbidden West players asked for the corners. [S38, S60]
   - **Never force a subtitle background because of the aspect ratio** (the KCD2 bug, S37).
   - Cutscenes rendered in the engine at 21:9 need no side bars. Any pre-rendered 16:9 video gets black side bars, never stretching.
3. **Margins.** Text stays at least 5% of screen height from the top and bottom edges (54 units), following the BBC's 5–95% rule. Unreal's Safe Zone widget wraps the root of every screen.
4. **Sizes in Unreal units** (identical numbers at both resolutions; the second figure is pixels at 1440). Each should be checked by measuring a screenshot.

| Element | 1080 units (px at 1080) | px at 1440 |
|---|---|---|
| Absolute floor (Xbox 101, PC) | 18 | 24 |
| Smallest label (legal line, version number) | 20 | 27 |
| Body text in menus, settings, notebook | 24–26 | 32–35 |
| Settings option labels | 28 | 37 |
| Interaction prompt verb | 26–28 | 35–37 |
| Key hint | 26 | 35 |
| Typing box text | 30–32 | 40–43 |
| Subtitle size: Small | 28 | 37 |
| Subtitle size: **Default** | **36** | **48** |
| Subtitle size: Large | 46 (Hamilton's TV figure) | 61 |
| Subtitle size: Largest | 60 | 80 |
| Headings on menus | 40–56 | 53–75 |

   - The largest subtitle size, 60, is 333% of the 18 px floor and well over Xbox 104's 200%.
   - A global "Interface text size" setting (80–150%) multiplies everything except subtitles, which have their own setting.
5. **Contrast.**
   - Any text: 4.5:1 or better against its actual backing.
   - Subtitles, prompts and body text: aim for 7:1.
   - Text over the live 3D world always gets a backing plate, or a dark outline or shadow, and is tested over the worst frames: sky, a sodium-lit wall, headlights, fog.
   - Never rely on colour alone, for the colour-blind: a speaker's colour always goes with the name.
6. **Legibility rules for the font helper's choice.** OFL fonts only.
   - Mixed case.
   - Generous x-height.
   - Distinct I, l and 1, and distinct 0 and O.
   - Regular or medium weight over the world, never thin or light.
   - No condensed, handwritten or all-capitals type for running text. Period lettering is for headings and titles only, as RDR2 does.
   - At least one plain sans-serif for subtitles (Xbox 104).
7. **Motion.**
   - Prompts fade in over about 150 ms and out over about 200 ms.
   - Menus cross-fade over 200–250 ms.
   - Subtitles appear at once (or within 100 ms) so they keep pace with the voice.
   - No bouncing or sliding.
   - "Reduce motion" means fades only.
   - The paper notebook may open with a short page turn of about 300 ms, which can be switched off.
8. **Input.** Keyboard and mouse first.
   - Through CommonUI every screen also works with arrow keys, Tab and a gamepad, with a visible focus state and automatic key glyphs that follow remapping.
   - Esc is always "back", then "close".

### Screen by screen

**Title screen**
- Must show:
  - the title;
  - Continue (only if a save exists, showing the save's in-game day and time and the place);
  - New game (if a save exists, a confirm that the old save is kept or overwritten);
  - Settings;
  - Quit (no confirm needed at the title);
  - a small version number.
- Background: a still or near-still frame of the town at night, rendered by the game itself.
- Must not show: a "press any key" gate on PC (my recommendation), news feeds, online prompts or adverts, or anything that reveals the story.

**Pause menu (Esc)**
- Pauses the simulation.
- Must show: Resume; the Ledger (opens the notebook); Settings; Save and quit to title; Quit to desktop (both with a confirm that says when the last save was).
- Must not show: statistics, what other characters know, objectives or a map marker.
- Look: period print styling is fine for the frame (RDR2's approach), but all labels in plain legible type.

**Settings**
- Layout: tabs for Display and graphics, Audio, Controls, Interface and accessibility. A description and, where useful, a live preview beside each option (for example a sample subtitle at the chosen size and background).
- **Display and graphics** (established PC practice; not separately sourced today):
  - quality presets Low, Medium, High, Epic, plus Custom. These map to Unreal's scalability groups: view distance, anti-aliasing, shadows, global illumination, reflections, post-processing, textures, effects, foliage, shading;
  - auto-detect;
  - resolution, display mode, monitor, upscaler and render scale, frame cap, V-sync;
  - field of view;
  - motion blur, film grain and chromatic aberration as separate switches;
  - display changes revert after about 15 s unless confirmed.
- **Audio:** master, voices, effects, ambience, music.
- **Controls:**
  - full keyboard and mouse remapping (and gamepad);
  - hold or toggle for every held action;
  - mouse sensitivity, invert Y, camera shake.
- **Interface and accessibility:** as listed below.

**Interaction prompt (spatial)**
- Appears only when the player is close and facing a usable person or thing. One prompt at a time, the nearest one in view taking priority.
- Shows a small mark anchored at the person or thing, a short verb and the key glyph, for example "Talk  [E]" or "Read  [E]".
- Size: verb 26–28 units, kept inside the centred 16:9 region.
- Must not show: outlines or glow through walls, floating names, health or mood readouts, or any hint of what the person knows.
- Setting: Prompts On / Minimal (glyph only) / Off.

**First-time key hints**
- Shown once, at the moment the action first becomes possible (Hodent's "learning by doing", S9). One at a time, at most about six words plus the key glyph, low in the 16:9 region away from the subtitles.
- Dismissed by doing the action. Uses the player's current key bindings.
- Settings: hints on/off, and "reset hints".
- Must not: stack up, pause the game, or appear as a wall of text on the loading screen.

**Subtitles**
- Placement: bottom centre of the 16:9 region, last line about 8–10% above the bottom edge. Each line at most about 40 characters (about 720 units at the default size, so lines do not stretch on 21:9). At most 2 lines.
- **Speaker name:** shown when the speaker changes (Xbox 104), in the speaker's colour, with the line text in white.
  - Recommendation for Jafar (touches what the player knows): until the player has learned a name, show a short description, such as "Woman at the bus stop".
- Off-screen speakers get a small direction mark (‹ or ›).
- Backing box per line, default about 60% opacity, adjustable 0–100%.
- Timing follows the voice. Live speech is split into phrases of 2 lines or fewer, each held for its spoken length and never under about 1 s (from the BBC's 0.3 s a word).
- Separate switches for:
  - main conversation;
  - overheard and background conversation (the town's gossip; RDR2 was criticised for subtitling only half of these);
  - sound captions such as [door slams].

**Typing box** (the player types; characters answer aloud)
- Opens with one key when in talking range. Sits in the shared bottom-centre speech area, above where the reply subtitle will appear.
- Starts as one line and grows to 3, then scrolls. This avoids Vaudeville's cramped window (S57).
- Enter sends, Esc cancels, and the text is not lost if a reply times out.
- A character count appears only near the limit.
- **While waiting for a reply:**
  - no spinner;
  - the character's own listening and thinking animation carries the wait;
  - after about 2 s, a quiet "…" under the speaker's name in the subtitle area;
  - on time-out, an in-character recovery line (for the town session to write).
- If the protagonist's line is voiced, it is subtitled like any speaker; if not, it stays in the box until the reply begins.
- Must not show: suggested questions, relationship meters, or anything revealing what the character knows.
- Recommendation: the person waits for you while the world runs on, with an accessibility option "Pause the world while typing". This is a builder decision under current rulings, unless Jafar regards it as scope.

**Loading screen**
- Shows: one full-screen still (a frame of the town, or a page of the Ledger); a thin, honest progress bar fed by real loading work (Lyra's CommonLoadingScreen can be held while streaming finishes, S23); short phase text.
- If true progress is unknown: an indeterminate mark, not a fake bar.
- Fades from black into play. No "press to continue" unless the game would otherwise start mid-action.
- Must not: show tip walls, flash, or show text below 24 units.

**The Ledger notebook and paper map** (full-screen meta screens)
- Body text at 24–26 units in legible type. Handwriting only for short headings or annotations.
- The map follows the brief: no markers or waypoints.
- Recommendation for Jafar (scope): no "you are here" mark either, as in KCD2's Hardcore mode, consistent with finding the way by street signs.

### Accessibility settings to offer

Combined from Xbox 101/104, the Game Accessibility Guidelines, The Last of Us Part II and Ubisoft:
- **Subtitles:** on by default; size (four steps); background opacity 0–100%; speaker names on/off; name colours on/off; background-conversation subtitles on/off; sound captions on/off; direction marks on/off.
- **Interface:** interface text size (80–150%); prompts on / minimal / off; key hints on/off and reset; interface width 16:9 / full; high-contrast prompts.
- **Controls:** full remapping; hold or toggle per action; sensitivity; invert Y; "pause the world while typing".
- **Motion:** camera shake off; motion blur off; film grain and chromatic aberration off; field of view; reduce interface motion.
- **Colour:** nothing relies on colour alone. If any colour carries meaning, offer a colour-blind-safe alternative.
- **Advanced, optional:** menu text-to-speech (as in The Last of Us Part II).

### How each piece passes the gates

- **The interface's overall look** (title, pause, a street frame with prompt and subtitle at 16:9 and 21:9) is "the overall look ... as whole frames", so it goes on Jafar's page.
- **Individual components** pass the ordinary gate: your own check, then a reviewer who has not seen the work.
- **The AI tester** measures text heights and contrast from screenshots of the packaged build at both resolutions, using the Xbox method.

## (e) What could not be verified or reached

- **Xbox guidelines 101 and 104** (Microsoft Learn): refused. The numbers are from search summaries and the version-history summary (v2.0, 16 February 2021: 4K figures; v3.0, 9 May 2022: measuring method). Check at source.
- **BBC Subtitle Guidelines site:** refused. The colours, words a minute and 68% figure are from summaries. Only the BBC's validator discussion of technical limits was opened.
- **Game Accessibility Guidelines, Can I Play That, Ian Hamilton's article** (Game Developer, reported as 15 July 2015) **and 80.lv:** refused. All snippet.
- **W3C WCAG 2.2:** refused. The contrast figures are as widely published, from snippets.
- **GDC talks** (Bohn 2023, Rebrova 2019, Ignacio 2013, Rockenbeck 2021) and **Hodent's book and blog:** only descriptions read, not the talks or the book.
- **KCD2 and RDR2 details:** almost all from forums, mod pages and search summaries. The one exception is KCD2 forcing the subtitle background on ultrawide, which I opened (a mod's README). No developer interview on either game's UI was found.
- **Unreal's font DPI setting:** Epic's page and the search summaries disagreed on which preset new projects get and on the conversion example. Measure rendered text instead.
- **Unreal's default DPI curve keys:** from an Epic forum post seen in a snippet, not the docs page. Easy to confirm in Project Settings.
- **The size table (36 px default subtitle, and others) and all screen requirements in (d):** my recommendations, derived from the sources with visual-angle arithmetic. They are not published standards. I assumed Jafar's monitor is 34 inches; that is not known.
- **Licence:** reusing Lyra code or CommonLoadingScreen should be checked against the project's licence allowlist. CommonUI is an engine plugin.

## Sources

All read 1 October 2026.

- S1. Fagerholt, E. & Lorentzon, M., "Beyond the HUD: User Interfaces for Increased Player Immersion in FPS Games", MSc thesis, Chalmers University of Technology, 2009. https://odr.chalmers.se/server/api/core/bitstreams/fd267f70-c295-4eae-ae01-af5db676e61d/content. SNIPPET.
- S2. Iacovides, I., Cox, A., Kennedy, R., Cairns, P. & Jennett, C., "Removing the HUD: The impact of non-diegetic game elements and expertise on player involvement", CHI PLAY '15, 2015. https://pure.york.ac.uk/portal/en/publications/removing-the-hud-the-impact-of-non-diegetic-game-elements-and-exp/. SNIPPET.
- S3. Peacocke, M., Teather, R. J., Carette, J., MacKenzie, I. S. & McArthur, V., "An empirical comparison of first-person shooter information displays: HUDs, diegetic displays, and spatial representations", Entertainment Computing 26:41–58, 2018. https://www.yorku.ca/mack/ec2018.html. SNIPPET.
- S4. Ignacio, D. (EA Visceral), "Crafting Destruction: The Evolution of the Dead Space User Interface", GDC 2013. https://gdcvault.com/play/1017723. SNIPPET.
- S5. Bohn, Z. (Santa Monica Studio), "'God of War Ragnarök': Building the UI for a AAA Sequel", GDC 2023. https://www.gdcvault.com/play/1029143. SNIPPET.
- S6. Rebrova, N. (SYBO), "Building a Unified Cross-Project UI Framework", GDC 2019. https://gdcvault.com/browse/gdc-19/play/1026400. SNIPPET.
- S7. Game Developer, "See how Ghost of Tsushima's Guiding Wind came to life at GDC 2021" (talk by B. Rockenbeck, Sucker Punch), 2021. https://www.gamedeveloper.com/audio/see-how-i-ghost-of-tsushima-s-i-guiding-wind-came-to-life-at-gdc-2021. SNIPPET.
- S8. Hodent, C., The Gamer's Brain, CRC Press/Routledge, 2017. https://www.routledge.com/The-Gamers-Brain-How-Neuroscience-and-UX-Can-Impact-Video-Game-Design/Hodent/p/book/9780367638184. SNIPPET (pillar list via IxDF, "The Game UX Twist: Usability Principles for Games", undated, https://ixdf.org/literature/article/the-game-ux-twist-usability-principles-for-games, SNIPPET).
- S9. Hodent, C., "The Gamer's Brain, Part 2: UX of Onboarding and Player Engagement", GDC 2016 (blog post undated). https://celiahodent.com/the-gamers-brain-part-2-gdc16. SNIPPET.
- S10. Hodent, C., "Developing UX Practices at Epic Games", undated. https://celiahodent.com/ux-practices-epic-games/; and University of Utah, "The UX of Fortnite", undated, https://games.utah.edu/news/the-ux-of-fortnite/. SNIPPET.
- S11. Isbister, K. & Hodent, C. (eds.), Game Usability, 2nd ed., Routledge (date not verified). https://www.routledge.com/Game-Usability-Advice-from-the-Experts-for-Advancing-UX-Strategy-and-Practice-in-Videogames/Isbister-Hodent/p/book/9780367619923. SNIPPET.
- S12. Epic Games, "Common UI Plugin for Advanced User Interfaces in Unreal Engine" (UE 5.8 docs), undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/common-ui-plugin-for-advanced-user-interfaces-in-unreal-engine. OPENED.
- S13. Epic Games, "Common UI Quickstart Guide for Unreal Engine", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/common-ui-quickstart-guide-for-unreal-engine. OPENED.
- S14. Epic Games, "Input Fundamentals for CommonUI in Unreal Engine", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/input-fundamentals-for-commonui-in-unreal-engine. OPENED.
- S15. Epic Games, "DPI Scaling in Unreal Engine", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/dpi-scaling-in-unreal-engine. OPENED.
- S16. Epic Games, "Scaling UI for Different Devices in Unreal Engine", undated. https://dev.epicgames.com/documentation/unreal-engine/scaling-ui-for-different-devices-in-unreal-engine. OPENED.
- S17. Epic Games, "UMG Safe Zones in Unreal Engine", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-safe-zones-in-unreal-engine. OPENED.
- S18. Epic Games, "Font DPI Scaling in Unreal Engine", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/font-dpi-scaling-in-unreal-engine. OPENED.
- S19. Epic Games, "UMG Best Practices in Unreal Engine", undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/umg-best-practices-in-unreal-engine. OPENED.
- S20. Epic Games, "User Interface Settings in the Unreal Engine Project Settings" (UE 5.8), undated. https://dev.epicgames.com/documentation/unreal-engine/user-interface-settings-in-the-unreal-engine-project-settings. OPENED.
- S21. Epic Developer Community forum, "UE4 Reset Widget DPI Scaling Curve to Default", reply #2, undated. https://forums.unrealengine.com/t/ue4-reset-widget-dpi-scaling-curve-to-default/417224/2. SNIPPET.
- S22. x157, "How Common UI is Setup in LyraStarterGame", undated. https://x157.github.io/UE5/LyraStarterGame/CommonUI/. SNIPPET.
- S23. eelDev, "Common Loading Screen" documentation, undated. https://cls.eeldev.com/. SNIPPET.
- S24. Microsoft, "Xbox Accessibility Guideline 101: Text display", undated. https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/101. SNIPPET (refused).
- S25. Microsoft, "Xbox Accessibility Guideline 104: Subtitles and captions", undated. https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/104. SNIPPET (refused).
- S26. Microsoft, "Xbox Accessibility Guidelines – Version History" (v2.0 16 February 2021; v3.0 9 May 2022). https://learn.microsoft.com/en-us/gaming/accessibility/xag-version-history. SNIPPET.
- S27. Game Accessibility Guidelines, "Use an easily readable default font size", undated. https://gameaccessibilityguidelines.com/use-an-easily-readable-default-font-size/. SNIPPET.
- S28. Game Accessibility Guidelines, "If any subtitles / captions are used, present them in a clear, easy to read way", undated. https://gameaccessibilityguidelines.com/if-any-subtitles-captions-are-used-present-them-in-a-clear-easy-to-read-way/. SNIPPET.
- S29. Hamilton, I., "How to do subtitles well – basics and good practices", Gamasutra/Game Developer, reported as 15 July 2015. https://www.gamedeveloper.com/audio/how-to-do-subtitles-well-basics-and-good-practices. SNIPPET.
- S30. 80.lv, "10 Golden Rules on Subtitles for Games", undated (cites Hamilton, GDC 2019). https://80.lv/articles/10-golden-rules-on-subtitles-for-games. SNIPPET. (In (b), the KCD2 map credit is ArtStation, Kurowski, P., "Kingdom Come: Deliverance II – Maps", undated, https://www.artstation.com/artwork/rlYJm5, SNIPPET.)
- S31. BBC, "Subtitle Guidelines" (v1.2.x), undated. https://bbc.github.io/subtitle-guidelines/. SNIPPET (refused). Also the Kairos 23.1 article citing the 2017 BBC guidelines, https://kairos.technorhetoric.net/23.1/topoi/zdenek/typography.html, SNIPPET. (In (b), the KCD2 loading-screen art is ArtStation, Zavacky, J., "Kingdom Come Deliverance II – Loading screen", undated, https://www.artstation.com/artwork/y46l2O, SNIPPET.)
- S32. BBC, ttml-validator discussion #10, "BBC Subtitle Guidelines technical requirements for EBU-TT-D", started 20 February 2026. https://github.com/bbc/ttml-validator/discussions/10. OPENED. (In (b), KCD2 menus and codex are from the KCD2 codex wiki, https://kingdomcomedeliverance.wiki.gg/wiki/Kingdom_Come:_Deliverance_II_codex, SNIPPET.)
- S33. Ofcom, statement "Ensuring the quality of TV and on-demand access services", 15 April 2024. https://www.ofcom.org.uk/siteassets/resources/documents/consultations/category-1-10-weeks/264291-ensuring-the-quality-of-tv-and-on-demand-access-services/associated-documents/statement-on-ensuring-the-quality-of-tv-and-on-demand-services.pdf. SNIPPET. Also Ofcom, "Television Access Services Review", 2006, https://ofcom.org.uk/tv-radio-and-on-demand/broadcast-codes/tv-access-services/access-services-review, SNIPPET. (In (b), the KCD2 HUD console variables are from Nexus Mods, "Toggle HUD", https://www.nexusmods.com/kingdomcomedeliverance2/mods/43, and kcd2.org commands, https://kcd2.org/en/post/kcd2-commands, undated, SNIPPET.)
- S34. W3C, WCAG 2.2 (Recommendation 5 October 2023), "Understanding 1.4.3 Contrast (Minimum)". https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html. SNIPPET (refused). (In (b), KCD2 Hardcore mode: Warhorse on X, https://x.com/KingdomComeRPG/status/1952384026985079012, 2025; Steam News, "Hardcore Mode arrives April 15", 2025, https://store.steampowered.com/news/app/1771300/view/501695476544832462; PCGamesN, https://www.pcgamesn.com/kingdom-come-deliverance-2/hardcore-mode, 2025. All SNIPPET.)
- S35. Legge, G. E. & Bigelow, C. A., "Does print size matter for reading? A review of findings from vision science and typography", Journal of Vision 11(5):8, August 2011. https://jov.arvojournals.org/article.aspx?articleid=2191906. SNIPPET. (In (b), KCD2 dialogue: Fextralife, "Persuasion System", undated, https://kingdomcomedeliverance2.wiki.fextralife.com/Persuasion_System, SNIPPET; and Nexus Mods "No Letterbox", https://www.nexusmods.com/kingdomcomedeliverance2/mods/34, SNIPPET.)
- S36. KCD2 subtitle options: YouTube, "How to Change Subtitle Size in Kingdom Come: Deliverance II", undated, https://www.youtube.com/watch?v=uRDNdeQArFY; Steam discussion, https://steamcommunity.com/app/1771300/discussions/0/601895505111306639. SNIPPET.
- S37. Serafim96, "noletterbox-kcd2-21-9-fix" README, GitHub, undated. https://raw.githubusercontent.com/Serafim96/noletterbox-kcd2-21-9-fix/master/README.md. OPENED.
- S38. Nexus Mods, KCD2 "Centered HUD" (mod 2723), "BIGGER HUD" (1104), "BetterFontsJK" (1263), undated. https://www.nexusmods.com/kingdomcomedeliverance2/mods/2723; and Evetech, "KCD2 Ultrawide Support" guide, undated, https://evezone.evetech.co.za/deep-dives/kingdom-come-deliverance-2-ultrawide-support-219-and-329-setup-guide/. SNIPPET.
- S39. Infinite Lives (Substack), on KCD2, 2025, https://infinitelives.substack.com/p/kingdom-come-deliverance-ii-could; TechRadar review, 2025, https://www.techradar.com/gaming/kingdom-come-deliverance-2-review. SNIPPET.
- S40. Wikipedia, "HUD (video games)", revision as read. https://en.wikipedia.org/wiki/HUD_(video_games). OPENED.
- S41. RDR2 HUD settings: Steam discussion "HUD Question", https://steamcommunity.com/app/1174180/discussions/0/3191359376161388269/; GamesRadar, "Best Red Dead Redemption 2 settings", undated, https://www.gamesradar.com/best-red-dead-redemption-2-settings/; on period typography, madegooddesigns.com, "What Font Does Red Dead Redemption Use?", 2026, https://madegooddesigns.com/red-dead-redemption-font/. SNIPPET.
- S42. VGR, "Red Dead Redemption 2: How to Use Each Mini-Map Option", undated. https://www.vgr.com/red-dead-redemption-2-how-to-use-each-mini-map-option/. SNIPPET.
- S43. RDR2.org forum, "Menu at bottom right of screen", https://www.rdr2.org/forums/topic/5605-menu-at-bottom-right-of-screen/; ResetEra, "Talking is the most innovative feature in RDR2", 2018, https://www.resetera.com/threads/talking-is-the-most-innovative-feature-in-rdr2.86512/. SNIPPET.
- S44. Red Dead Wiki (Fandom), "Journal (RDR 2)", undated. https://reddead.fandom.com/wiki/Journal_(RDR_2). SNIPPET.
- S45. Skogberg, A., "The good, the bad and the ugly UX of Red Dead Redemption 2", December 2018. https://alexanderskogberg.com/2018/12/ux-red-dead-redemption-2/. SNIPPET.
- S46. Can I Play That?, "Red Dead Redemption II accessibility review", 28 November 2018, https://caniplaythat.com/2018/11/28/red-dead-redemption-ii-accessibility-review/; and "Deaf Game Review – Red Dead Redemption 2", 19 February 2019, https://caniplaythat.com/2019/02/19/deaf-game-review-red-dead-redemption-2/. SNIPPET.
- S47. TechWikies, "Red Dead Redemption 2: How are the subtitles", undated, https://www.techwikies.com/news/red-dead-redemption-2-how-are-the-subtitles-in-general/; Steam discussion on speaker names, https://steamcommunity.com/app/1174180/discussions/0/3493130356503434158/. SNIPPET.
- S48. GamerMatters, "Disco Elysium's Text Box Design Is Inspired By How We Use Computers And... Twitter", undated, https://gamermatters.com/disco-elysiums-text-box-design-is-inspired-by-how-we-use-computers-and-twitter/; PCGamesN, "Disco Elysium ... bigger font sizes", undated, https://www.pcgamesn.com/disco-elysium/update-bigger-fonts. SNIPPET.
- S49. Can I Play That?, "Mafia: Definitive Edition accessibility review", 15 October 2020, https://caniplaythat.com/2020/10/15/mafia-definitive-edition-accessibility-review/; 2K, "Mafia: Definitive Edition Update", undated, https://mafia.2k.com/news/mafia-definitive-edition-update-new-features/. SNIPPET.
- S50. Generic UI pipeline summaries: Pixune, "UI/UX Design Pipeline for Game Interfaces", undated, https://pixune.com/blog/ui-ux-design-pipeline/; Sketch, "What is game UI?", undated, https://www.sketch.com/blog/game-ui-design/. SNIPPET.
- S51. Idris, H., "Colour in game UI: a palette that sits on top of your game", undated. https://h-idris.com/blog/game-ui-colour. SNIPPET.
- S52. Material Design 3, "Transitions", undated, https://m3.material.io/styles/motion/transitions/applying-transitions; Gapsy Studio, "UI Animation Best Practices", undated, https://gapsystudio.com/blog/ui-animation-best-practices/. SNIPPET.
- S53. L.A. Noire Wiki (Fandom), "Notebook", undated. https://lanoire.fandom.com/wiki/Notebook. SNIPPET.
- S54. ColePowered Games, "Shadows of Doubt DevBlog 4: Case Folders & Cork Boards", undated. https://colepowered.com/shadows-of-doubt-devblog-4-case-folders-cork-boards/. SNIPPET.
- S55. Nexus Mods, Hitman 3 "Minimalist HUD" (mod 994), undated. https://www.nexusmods.com/hitman3/mods/994. SNIPPET.
- S56. Naughty Dog, "The Last of Us Part II: Accessibility Features Detailed", 2020, https://www.naughtydog.com/blog/the_last_of_us_part_ii_accessibility_features_detailed; PlayStation, "Accessibility options for The Last of Us Part II", undated, https://www.playstation.com/en-us/games/the-last-of-us-part-ii/accessibility/. SNIPPET.
- S57. Game8, "Vaudeville Review", undated (late 2025), https://game8.co/articles/reviews/vaudeville-review; Games Press, "Vaudeville supports speech recognition in 8 languages", undated. SNIPPET (the chat-window remark's exact source is uncertain).
- S58. KRYSYS1, "KCD2.AI.NPC" README, GitHub, undated. https://raw.githubusercontent.com/KRYSYS1/KCD2.AI.NPC/main/README.md. OPENED.
- S59. TrueAchievements, "New Insights from Ubisoft Show How Important Subtitles are to Modern Gamers", undated, https://www.trueachievements.com/n38283/assassins-creed-ubisoft-subtitles; Critical Hit, undated, https://www.criticalhit.net/gaming/subtitles-are-the-best-and-most-players-agree-on-that-according-to-ubisoft/. SNIPPET.
- S60. Steam discussions, Horizon Forbidden West Complete Edition, "HUD aspect ratio setting", 2024. https://steamcommunity.com/app/2420110/discussions/0/4292566217059869115/. SNIPPET.
