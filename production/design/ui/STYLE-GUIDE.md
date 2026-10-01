# The evening paper: the interface's style guide

The look Jafar picked on 1 October 2026: the interface is a 1990 British local evening paper. Black ink on newsprint with one spot red, and no full colour (regional papers printed none in their editorial pages until the mid 1990s). Every screen is drawn in step2/evening-paper.html, and every part in every state in step2/kit.html. The research behind it is in production/research/ui-design/.

## Principles

1. **One paper, one red.** Ink, newsprint and a single spot red. Red means *the one in hand*, a band (STOP PRESS, SETTINGS, a question) or a speaker's name, and nothing else: the ears and the hint's tag are ink, the progress rule is newsprint.
2. **Period lettering for headings, plain type for reading.** The blackletter word is the game's name and nothing more. League Gothic is for bands, ears and small section heads only. Everything the player acts on or hears is in Libre Franklin; Old Standard TT italic carries only notes, captions and datelines, never below 24.
3. **Nothing he could not know.** No markers, no meters, no minds shown. A name appears only once Tom has learned it; until then the street's description of the person is used (D12).
4. **Read first, then belong.** Any style that costs legibility loses: speech is light on dark, never dark on newsprint.
5. **Out of the way of the street.** Everything the player reads or acts on sits in the centred 16:9 region of a wide screen. Only the street, and the shading over it, uses the full width.

## Layout

- **Units.** Everything is laid out at 1080 tall: 1920 wide at 16:9, 2580 wide at Jafar's 21:9. Unreal scales by the shortest side (the default DPI curve, 1080 = 1.0), so on his 3440 by 1440 screen every size here is drawn a third larger. Sizes below are in these units.
- **The safe region.** The centred 1920 by 1080; on 21:9 that leaves 330 units each side (440 pixels on his screen). A setting "Interface width: 16:9 / full width" comes later.
- **Margins.** 120 units left and right of the safe region, 52 to 74 at the top and bottom. Nothing sits closer than 54 to an edge (5%).
- **Spacing.** An 8-unit step. Rows of choices are 76 to 86 units (the larger with a note under the choice), settings lines 56, and gaps between keys 10.
- **Where things sit:**
  - **Title:** the front page at the left of the safe region.
  - **Pause and confirmations:** centred.
  - **Settings:** a listings page across the safe region, with key hints under it.
  - **Subtitles:** centred, their last line 104 units up (10%).
  - **The typing box:** above the subtitles, 252 up, on the side of the picture away from the person he is talking to, so their face and listening stay in view; its keys ride on its top edge and move as it grows.
  - **First-time hints:** a small slip low at the left, clear of the street ahead and of the subtitles.
  - **The prompt:** beside the person or thing it belongs to, anchored to its place in the picture, so it stays beside them at any shape of screen.

## Type

| Role | Face | Size (units) | Notes |
|---|---|---|---|
| Masthead | UnifrakturMaguntia | 112 to 128 | The game's name only: the title and loading pages. Never on the pause screen, and never the name of a newspaper in the town |
| Band | League Gothic, capitals | 40 to 58 | STOP PRESS, SETTINGS, confirmations; white on red |
| Ear, section head | League Gothic, capitals | 26 to 30 | LATE FINAL, RAIN LATER, THE SCREEN; ink, never red |
| Choice | Libre Franklin 800 | 48 to 50 | Mixed case; one per row |
| Setting, tab | Libre Franklin 600 / 800 | 30 / 32 | Values in 500, numbers tabular |
| Subtitle | Libre Franklin 450 | 39 | About 48 px from the top of an h to the foot of a y on a 1440 screen; at most two lines under 40 letters |
| Speaker's name | Libre Franklin 800, capitals | 30 | White on red, before the line |
| Typing box | Libre Franklin 450 | 36 | Grows to three lines, then scrolls |
| Suggested line | Libre Franklin 600 | 34 | At most about 40 letters, so it is one line |
| Key hint | Libre Franklin 500 | 30 | The key itself 700, in a ruled box |
| Note, caption | Old Standard TT italic | 26 to 30 | Where and when, why a choice is unavailable, a caption |
| Explanation in settings | Libre Franklin 400 | 27 | |
| Dateline | Old Standard TT, capitals, tracked | 24 | |
| Smallest label | Libre Franklin 400 | 22 | The build number only; nothing the player must read is smaller than 24 |

Fonts are all SIL OFL 1.1 (FONTS.md). Unreal needs static cuts of the variable families (Libre Franklin 450, 500, 600, 700 and 800; League Gothic regular), made with fontTools; none has a Reserved Font Name, so no renaming is needed.

## Colour

| Token | Value | Use | Contrast |
|---|---|---|---|
| Newsprint | #E8E3D6 | Every sheet | |
| Ink | #1E1E1D | Text on newsprint, rules, key boxes | 13.0 : 1 on newsprint |
| Spot red | #B4191F | The one in hand, bands, speakers' names; nothing else | 5.3 : 1 on newsprint (large bold type only); white on it 6.8 : 1 |
| Grey | #4F4C46 | Notes, unchosen tabs, arrows | 6.7 : 1 |
| Unavailable | #77726A | A choice that cannot be taken, always with a line saying why | 3.7 : 1 |
| On dark | #F1EDE3 | Text over the street | |
| Backing | #10100F at 80% | Behind subtitles, prompts and the typed name | On-dark text 8.9 : 1 over a white sky, 16.6 : 1 over black |

The backing's strength is the player's to set, from 0 to 100% (default 80%). No meaning rests on colour alone: whatever is in hand also carries a red bar, an underline or a ring.

## Materials

- **Newsprint:** a coarse fibre and yellowing towards the edges, a fold across larger sheets, and a soft shadow under them. In the game these become scanned paper, under the finish route Jafar chose, (a).
- **Halftone:** photographs of the town are the game's own frames, screened into dots that grow where the picture is dark, in ink on newsprint.
- **Coupon:** his own line goes on a cut-out reader's coupon with a dashed border.
- **Keys:** a square box ruled in ink, never rounded.

## Parts and their states

Every part is drawn in step2/kit.html.

- **Choice:**
  - normal: ink;
  - in hand: red, with a red bar at the left;
  - pressed: the bar widens and the row tints red for 120 ms;
  - unavailable: grey, with a line saying why ("No story saved yet.").
- **Settings line:**
  - normal;
  - in hand: red, with a bar;
  - unavailable: grey, with the reason in place of its value ("Same as your desktop", for the resolution of a borderless window).
  - Values change with ← and → between ‹ and ›, drawn in ink at 36 so they read as the way to change it.
- **Quality:** the preset sits over the five lines it sets (shadows, reflections in the wet, how far you see, textures, effects); changing one of them makes it Custom. The screen's own lines (display, resolution, frame rate, brightness) sit apart under their own head. The Picture section is changed over the live street, dimmed but not blurred, so each change shows as it is made.
- **Preset box:**
  - normal: ruled;
  - picked: filled with ink;
  - in hand: a red ring;
  - picked and in hand: filled, with the red ring outside.
- **Slider:** a thin rule and a block; red when in hand.
- **Tab:** grey; the current one red and underlined.
- **Speaker's name:**
  - a name, once learned, or else a description;
  - an arrowhead on the side of a speaker who is out of sight.
- **Subtitle:** one backing per line, light on dark; at most two lines.
- **Prompt:**
  - one at a time, the nearest in view;
  - a short line points to its person or thing;
  - the key in its box, then the verb on the backing ("Talk to Sheila", "The window"); the name in it follows the same rule as subtitles, and it is the only label ever shown on a person.
- **First-time hint:**
  - a small slip headed FIRST STEPS in ink: the keys, then the game's own line in italic;
  - one at a time;
  - gone the moment the action is done; never pauses the game.
- **Typing box:**
  - the coupon, headed TO SHEILA (to whoever he is talking to);
  - Enter says it; Esc stops typing and keeps the words;
  - grows with the text;
  - suggested lines sit above it on a keyboard when he asks for them (below).
- **Suggested lines** (Jafar, 1 October: for a controller, or for anyone who would rather not type; production/research/ui-design/SUGGESTED-LINES.md):
  - his exact words, never a summary of them (Mass Effect's wheel is the warning: a summary that says something he did not mean);
  - three at most, each with its own job: one asks or presses, one is his own business, one leaves; then "My own words…";
  - written only from what Tom himself knows (his Ledger and the talk so far), never from what the other person knows, and never ranked by whether they would work;
  - where his answer decides something (a deal he can end with a plain yes), the yes and the no are both offered, written from the game's state, never by the model, with a third line that keeps talking without deciding;
  - never the same line twice in one conversation; the same voice and period as everyone else, and the same content rule;
  - chosen, a line goes the same way as a typed one: it is what he says;
  - on a keyboard they open with Tab above the coupon, numbered 1 to 3; with a controller they are there from the start, moved with the pad and said with A, and "My own words…" (Y) opens Steam's floating keyboard over the game;
  - no timers;
  - the one in hand is red with its bar, like every other choice.
- **A controller's buttons:** round, ruled in ink, never square like keys; the letters are the pad's own, read from Steam Input, and they follow any rebinding.
- **Confirmation:** a red band asking the question, a line saying what is kept, and the safe choice in hand first ("Stay on the street").
- **Progress:**
  - a thin newsprint rule that fills when the work can be counted, with the game's own words for the phase ("Building the street", "Starting as soon as the street is ready", "312 to go"; the first-launch phase, "Getting the street ready for this PC's graphics card", only on the first run);
  - a short moving piece when it cannot be counted;
  - never a bar that guesses.

## How things appear and disappear

| What | In | Out | How |
|---|---|---|---|
| Subtitle | at once (under 100 ms), with its sound | when its sound ends, held at least 1 s | No fade on entry, so it keeps pace with the voice; a 150 ms fade out |
| Prompt | 150 ms fade | 200 ms fade | Only while he is close and facing it |
| First-time hint | 200 ms fade | 250 ms fade, the moment it is done | One at a time |
| Typing box | 150 ms fade | 150 ms fade | The keys come with it |
| Menus (title, pause, settings) | 220 ms cross-fade | 180 ms | No sliding or bouncing |
| The one in hand | 120 ms | 120 ms | The bar grows from the left |
| Loading | fade from black, 400 ms | into play, 400 ms | The rule moves only as the work does |

With "Reduce motion" on, everything is a fade only and the bar does not grow.

## Sound (to make)

Short, quiet and switchable off, all recorded or made by us:
- a soft paper rustle when a menu opens;
- a pencil tick when a choice is taken;
- the distant run of a press under the loading screen;
- a soft key sound as he types, the first thing to go if it tires.

## In Unreal

- CommonUI widgets, with one style asset per part above.
- A Safe Zone at the root of every screen, and the default DPI curve (Shortest Side).
- Every key shown is drawn from the player's own bindings.
- Text is measured in screenshots of the packaged game, at 1920 by 1080 and 3440 by 1440, by the AI tester.
