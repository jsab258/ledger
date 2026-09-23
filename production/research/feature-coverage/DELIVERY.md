# The master checklist: 957 features, and the 462 neither list had

STATUS: SPEC (research delivery). Branch `research/feature-coverage`. THIS
REPLACES the earlier DELIVERY.md of this topic, whose 179-item checklist is
carried inside the master list below rather than deleted. The commission is
[BRIEF.md](./BRIEF.md); the one-page reading is [SUMMARY.md](./SUMMARY.md); the
independent list this was compared against is
[astra-list.md](./astra-list.md), 923 items, written by a different model
without sight of mine.

## 0. The numbers

| | count | of |
|---|---|---|
| Expectations in the independent list | **923** | |
| In my checklist AND in the plan | 172 | 923 |
| In my checklist, absent from the plan | 116 | 923 |
| IN THE PLAN, absent from my checklist | **99** | 923 |
| Ruled out for this game by its own decisions | 74 | 923 |
| **In neither: the blind spots** | **462** | 923 |

My checklist covered **288 of 923**. Half the list was
invisible to it.

The master checklist below merges both lists at the level of specific features:
923 from the independent list plus **34** of my own that it does
not contain, so **957 rows**, each with its stage in `ROADMAP.md`
or the decision that rules it out.

## 1. What the comparison actually says

**One list of 179 against one list of 923 is not a difference of opinion about
scope. It is a difference of ALTITUDE.** Almost every row of mine turns out to
be a heading with between two and twenty behaviours inside it. `Interaction
prompts` is twenty-four items in the other list. `Title screen with Continue,
New Game, Load, Settings, Quit` is twenty. `Positional sound from its source`
is fifteen.

That is the same failure this whole exercise exists to find. The head turn and
positional sound went missing because they were inside `bodies and faces` and
`sound in the Unreal build`. My own delivery said so, and then produced 179
rows at exactly the altitude it had just diagnosed.

**The second finding is the one I did not expect: 99 items the plan
holds are absent from MY list.** They are concentrated in stealth and the law
(13), world layout (10), enemy awareness (6), lighting (6) and environment art
(5). Four lenses built from credits, engine modules, a generic first session
and compliance checklists produce a generic game. They under-read the parts
that are this game's actual subject, which the plan has been writing down for
weeks.

**The third: the independent list had the sources mine could not reach.** Its
own header cites the Steam controller documentation and the Xbox accessibility
guidelines, both refused by this environment's proxy. Its accessibility and
platform sections are the ones where my blind-spot count is highest, and that
is not a coincidence.

## 2. The blind spots, grouped by area

462 expectations that are in neither my checklist nor the plan nor ruled
out. Each group names the lens of mine that should have caught it and why it
did not. The five failure modes, in the order of how much damage they did:

- **F1** granularity: my row was the heading, and the behaviours lived inside it (31 of 51 areas)
- **F3** imagined happy path: I walked a session that worked, so what goes wrong was never in the walk (4 of 51 areas)
- **F4** wrong altitude: a module list names a capability, never the ways it fails (5 of 51 areas)
- **F2** source refused: the lens ran on a reconstruction, which yields categories rather than checkpoints (7 of 51 areas)
- **F5** outside my frame: no construction I used would ever have produced the subject (4 of 51 areas)

### Launching and reaching the game  (11 of 18)

Should have been caught by **lens 3, moment by moment**. Mode **F3**. My walk began at the title screen. Everything before it, and everything that can go wrong on the way, was never in the walk.

- `A01.01` A working launch from the installed shortcut or platform library (stage 4)
- `A01.02` A visible response while the application starts (stage 4)
- `A01.03` Startup that does not require unrelated windows or manual commands (stage 4)
- `A01.06` Startup on the intended monitor (stage 4)
- `A01.07` Initial sound at a reasonable volume (stage 4)
- `A01.11` A readable explanation of required account or permission requests (stage 4)
- `A01.12` Offline access to offline content where supported (stage 4)
- `A01.13` A usable response to unavailable online services (stage 4)
- `A01.15` An explanation when required content is still installing (stage 4)
- `A01.16` An actionable error when the game cannot start (stage 4)
- `A01.18` Skippable repeated introductory logos where permitted (stage 4)

### Title screen and menu navigation  (15 of 20)

Should have been caught by **lens 3, moment by moment**. Mode **F1**. I wrote the title screen as ONE row naming five buttons. Twenty behaviours live inside those five words.

- `A02.03` Protection against replacing an existing playthrough with "New Game" (stage 4)
- `A02.04` A visible selected menu item (stage 4)
- `A02.05` Menu navigation in a predictable order (stage 4)
- `A02.06` Consistent confirm and back controls (stage 4)
- `A02.07` A reliable way back from every screen (stage 4)
- `A02.09` Clickable areas that match their visible buttons (stage 4)
- `A02.10` Scroll-wheel support for scrolling lists (stage 4)
- `A02.12` Selection that remains visible while a list scrolls (stage 4)
- `A02.13` Useful explanations for disabled options (stage 4)
- `A02.14` Confirmation before destructive actions (stage 4)
- `A02.15` Dialogues that capture input without activating buttons behind them (stage 4)
- `A02.16` Menus that remember position when returning from a detail screen (stage 4)
- `A02.17` Text entry that works with the current device (stage 4)
- `A02.18` An on-screen keyboard when physical typing is unavailable (stage 4)
- `A02.20` Protection against repeated clicks starting the same operation twice (stage 4)

### Input fundamentals  (15 of 24)

Should have been caught by **lens 2, what runs every frame**. Mode **F4**. The module list gave me InputCore, EnhancedInput and CommonInput, so I wrote down input, prompts and remapping. A module list names a capability; it never names the ways that capability goes wrong.

- `A03.03` Consistent controls across equivalent situations (stage 4)
- `A03.05` Prompts that update after rebinding (stage 4)
- `A03.08` No duplicate action from one physical button press (stage 4)
- `A03.10` Clear feedback when an action requires holding (stage 4)
- `A03.11` Reasonable tolerance for slightly early action presses (stage 4)
- `A03.12` Predictable handling of conflicting simultaneous inputs (stage 4)
- `A03.13` Movement that stops when the movement input stops (stage 4)
- `A03.14` No stuck movement after opening a menu or changing focus (stage 4)
- `A03.15` No attack caused by the same click that dismisses a menu (stage 4)
- `A03.16` No unexpected action from an input held through a loading screen (stage 4)
- `A03.17` Analogue movement speed on supported sticks (stage 4)
- `A03.18` Equal intended movement speed in straight and diagonal directions (stage 4)
- `A03.22` Safe reconnection without restarting the game (stage 4)
- `A03.23` Input handling independent of frame rate (stage 4)
- `A03.24` Clear control ownership when several controllers are connected (stage 4)

### Onboarding and the first minute  (13 of 16)

Should have been caught by **lens 3, moment by moment**. Mode **F3**. My walk had the player learning. It did not have the player forgetting, mistiming, experimenting early, or replaying.

- `A04.01` An unmistakable transition from watching to controlling (stage 4)
- `A04.02` A starting camera aimed at something useful (stage 4)
- `A04.03` A safe opportunity to test movement (stage 4)
- `A04.04` A safe opportunity to test the camera (stage 4)
- `A04.08` Instructions using the player's actual bindings (stage 4)
- `A04.09` Time to read an instruction before it disappears (stage 4)
- `A04.10` Confirmation that a tutorial action succeeded (stage 4)
- `A04.11` A way to recover instructions dismissed accidentally (stage 4)
- `A04.12` Tutorials that cope with an action performed early (stage 4)
- `A04.13` Tutorials that stop repeating after understanding is demonstrated (stage 4)
- `A04.14` A way to revisit controls and basic rules (stage 4)
- `A04.15` A way to skip familiar instruction without breaking progression (stage 4)
- `A04.16` An opening that permits ordinary experimentation without trapping the player (stage 4)

### Camera behaviour  (12 of 24)

Should have been caught by **lens 2, what runs every frame**. Mode **F1**. Six camera rows for a subsystem whose failure modes are what a player actually meets: stairs, corners, foliage, recentering, cuts.

- `A05.07` Camera recovery after an obstruction clears (stage 2)
- `A05.08` Smooth handling of poles, foliage and other small obstructions (stage 2)
- `A05.09` Character fading or another solution when the camera gets too close (stage 2)
- `A05.11` A usable view while ascending and descending stairs (stage 5)
- `A05.12` A usable view while climbing or hanging (stage 3)
- `A05.13` Camera behaviour that does not repeatedly fight manual input (stage 2)
- `A05.14` Predictable recentering, if provided (stage 2)
- `A05.16` Appropriate framing when crouching or going prone (stage 2)
- `A05.17` Aiming that follows the intended sightline (stage 6)
- `A05.21` Camera recovery after a cutscene without disorienting rotation (stage 2)
- `A05.23` Stable horizon and manageable camera motion (stage 2)
- `A05.24` A sensible relationship between camera direction and movement after a camera cut (stage 2)

### Walking, running and turning  (9 of 21)

Should have been caught by **lens 2, what runs every frame**. Mode **F1**. Locomotion was four rows. Astra has twenty-one, and the extra seventeen are all collision and gait, which is where a third-person game feels wrong.

- `A06.07` Backward movement with an appropriate gait (stage 2)
- `A06.08` Sideways movement with an appropriate gait (stage 2)
- `A06.10` Consistent movement relative to the camera or facing convention (stage 2)
- `A06.12` Reliable movement up and down ordinary stairs (stage 2)
- `A06.13` Sensible behaviour on slopes (stage 2)
- `A06.14` Clear limits on slopes too steep to climb (stage 2)
- `A06.17` A crouched collision shape that actually fits under lower obstacles (stage 2)
- `A06.18` Prevention of standing through a ceiling (stage 2)
- `A06.19` Movement that follows moving platforms (stage 2)

### Jumping, climbing and water traversal, where supported  (10 of 20)

Should have been caught by **lens 2, what runs every frame**. Mode **F1**. I wrote jump, vault and climb as one row and marked it absent. One row cannot say what climbing has to do.

- `A07.04` A landing animation appropriate to the fall (stage 3)
- `A07.05` Fall damage that follows understandable rules (stage 3)
- `A07.06` A clear distinction between a safe drop and a dangerous fall (stage 3)
- `A07.10` Prevention of climbing into blocked space (stage 3)
- `A07.11` A way to cancel or drop from a climb (stage 3)
- `A07.12` Ladder entry from plausible positions (stage 3)
- `A07.13` Ladder exit without falling or becoming stuck (stage 3)
- `A07.14` Consistent behaviour at climbable and non-climbable lookalikes (stage 3)
- `A07.18` Readable breath or drowning rules if diving is possible (stage 3)
- `A07.19` Water camera and sound changes when submerged (stage 3)

### Character appearance  (5 of 17)

Should have been caught by **lens 1, who builds it**. Mode **F1**. The character art department gave me bodies, faces, clothing, skin and hair. It did not give me hands, mouths, holsters, gaps or cross-context consistency.

- `A08.04` Believable hands and fingers (stage 2)
- `A08.06` A mouth interior that survives ordinary close-ups (stage 2)
- `A08.10` Held items attached to the correct hand and orientation (stage 2)
- `A08.12` No major body or clothing gaps during ordinary poses (stage 2)
- `A08.14` Consistent appearance across gameplay, menus and cutscenes (stage 2)

### Body animation and physical contact  (11 of 24)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Animation gave me idle, foot planting, look-at, bumping and ragdoll. Everything between those, which is most of what animation IS, fell through.

- `A09.06` Stride length that matches travel speed (stage 2)
- `A09.07` Body lean during acceleration and turning (stage 2)
- `A09.09` Upper-body actions that coexist with leg movement (stage 2)
- `A09.11` Hands that meet handles, rails and other contact points (stage 2)
- `A09.12` Finger poses that fit held objects (stage 2)
- `A09.13` Two-handed objects held by both hands (stage 2)
- `A09.16` Animation appropriate to the character's current weapon or burden (stage 2)
- `A09.18` Interruptions that leave the body in a valid pose (stage 2)
- `A09.19` Recovery from knockdown that connects to the final fallen position (stage 6)
- `A09.21` Bodies that rest on the ground rather than hover (stage 2)
- `A09.23` No sudden default pose while an animation loads (stage 2)

### Looking, expressions and social presentation  (8 of 14)

Should have been caught by **lens 1, who builds it**. Mode **F1**. THIS IS THE SECTION THE ACCIDENT CAME FROM. I had head turn and lip sync as two rows. Astra has fourteen, and eight of them are still nowhere.

- `A10.03` The torso turning when the player moves beyond a comfortable head angle (stage 2)
- `A10.04` Limits that prevent impossible head and neck rotation (stage 2)
- `A10.06` Eye contact that occasionally breaks (stage 2)
- `A10.07` Blinking rather than a permanent stare (stage 2)
- `A10.09` Listener reactions while another person speaks (stage 2)
- `A10.10` Gestures that fit the conversation rather than random arm waving (stage 2)
- `A10.11` People orienting toward a shared point of interest (stage 2)
- `A10.14` A return to ordinary activity after the player leaves (stage 2)

### Object interaction  (14 of 24)

Should have been caught by **lens 3, moment by moment**. Mode **F1**. Interaction was one row, `interaction prompts`. Every rule about what a prompt points at, when it fails, and how it cancels was inside that row.

- `A11.02` A stable current interaction target (stage 3)
- `A11.04` Interaction range that matches apparent reach (stage 3)
- `A11.05` No interaction through an intervening solid wall (stage 3)
- `A11.06` Appropriate priority when talk, loot and open share a button (stage 3)
- `A11.07` A clear description of the action before committing (stage 3)
- `A11.09` Feedback explaining why an interaction is unavailable (stage 3)
- `A11.10` Progress indication for prolonged interactions (stage 3)
- `A11.11` Predictable cancellation of prolonged interactions (stage 3)
- `A11.13` Door handling that does not trap the player inside the door (stage 3)
- `A11.14` Sensible behaviour when a door's path is obstructed (stage 3)
- `A11.20` Return from inspection to the previous position and context (stage 3)
- `A11.21` Controls for switches, terminals and similar devices that produce a visible result (stage 3)
- `A11.22` Occupied objects that cannot be used by two characters simultaneously (stage 3)
- `A11.24` An interaction ending cleanly if its object is destroyed or removed (stage 3)

### Collision and object physics  (11 of 18)

Should have been caught by **lens 2, what runs every frame**. Mode **F4**. Chaos and PhysicsCore told me physics produces pushable objects. They did not tell me what a physics system owes a player: stable settling, sane mass, no launched bottles.

- `A12.01` Solid ground everywhere that appears walkable (stage 2)
- `A12.02` Solid walls where walls are visibly present (stage 2)
- `A12.04` Doorways that admit a character who visibly fits (stage 2)
- `A12.08` Objects settling instead of vibrating indefinitely (stage 2)
- `A12.09` No explosive physics response from mild contact (stage 2)
- `A12.10` Fast objects that do not pass through obvious barriers (stage 2)
- `A12.12` A workable solution to being blocked by a friendly character (stage 2)
- `A12.13` Moving machinery carrying or blocking objects consistently (stage 2)
- `A12.14` Appropriate friction on visibly different surfaces where it matters (stage 2)
- `A12.15` Physical reactions accompanied by matching sound (stage 2)
- `A12.18` Stable interaction between bodies, props and uneven ground (stage 2)

### Ordinary civilian behaviour  (13 of 26)

Should have been caught by **lens 1, who builds it**. Mode **F1**. I had eight rows for the whole of civilian behaviour in a game whose entire subject is civilians.

- `A13.06` A response to repeatedly blocking someone's route (stage 2)
- `A13.07` Navigation through doorways without permanent jams (stage 2)
- `A13.08` Use of stairs rather than walking through their geometry (stage 2)
- `A13.12` People taking turns rather than all speaking simultaneously (stage 2)
- `A13.17` Fleeing or taking cover from danger (stage 3)
- `A13.18` Escape routes that lead away from danger (stage 3)
- `A13.20` A way for panic to resolve once danger passes (stage 3)
- `A13.21` People who do not immediately resume cheerful chatter beside an ongoing emergency (stage 3)
- `A13.22` Consistency between a person's current behaviour and dialogue (stage 2)
- `A13.23` Appropriate response when spoken to during another activity (stage 2)
- `A13.24` Some continuity when briefly looking away and back (stage 2)
- `A13.25` No obvious appearance or disappearance directly in view (stage 2)
- `A13.26` A reasonable solution when an NPC's intended route becomes blocked (stage 2)

### Enemy awareness and decision-making, where combat or stealth exists  (15 of 23)

Should have been caught by **lens 2, what runs every frame**. Mode **F1**. AIModule, StateTree and the perception model gave me reaction to noise and police response. Search, alert propagation, repositioning and disengagement were inside those two rows.

- `A14.06` Search focused on the last plausible known position (stage 3)
- `A14.09` Enemy movement that uses the actual available routes (stage 3)
- `A14.10` Replanning when doors, vehicles or other obstacles move (stage 3)
- `A14.11` Enemies able to negotiate ordinary stairs and doorways (stage 3)
- `A14.12` Combat positioning that avoids all enemies occupying one point (stage 3)
- `A14.13` Enemies using appropriate engagement distance (stage 3)
- `A14.14` Enemies not firing continuously into an obvious obstruction (stage 3)
- `A14.15` Appropriate retreat, advance or repositioning (stage 3)
- `A14.16` A response to being flanked (stage 3)
- `A14.17` A response to allies being injured or killed (stage 3)
- `A14.18` Believable limits on accuracy and reaction speed (stage 3)
- `A14.19` Clear reasons when an enemy cannot be damaged or interrupted (stage 3)
- `A14.20` A sensible end to searching or combat (stage 3)
- `A14.22` No pursuit through impossible or inaccessible routes (stage 3)
- `A14.23` No permanent lock into combat after every threat is gone (stage 3)

### Stealth, trespass and law, where included  (3 of 19)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Three rows, where the plan itself already has sixteen of these. My lenses were generic-game lenses and under-read this game's own subject.

- `A15.06` A warning or understandable transition before punishment where appropriate (stage 3)
- `A15.14` Searches that do not continuously know the hidden player's exact location (stage 3)
- `A15.19` No punishment for an action the controls misleadingly presented as harmless (stage 3)

### Companions and friendly allies, where included  (12 of 14)

Should have been caught by **lens 1, who builds it**. Mode **F5**. No lens of mine asked who walks beside the player. Departments, engine modules, a first session and a compliance checklist can all be built without ever mentioning a companion.

- `A16.01` Following at a useful distance (stage 6)
- `A16.02` Keeping up without repeatedly falling far behind (stage 6)
- `A16.03` Slowing down or waiting appropriately during guided travel (stage 6)
- `A16.04` Yielding when blocking a doorway or corridor (stage 6)
- `A16.05` Navigating the same ordinary obstacles as the player (stage 6)
- `A16.06` Sensible recovery when separated (stage 6)
- `A16.07` Entering and leaving vehicles appropriately (stage 6)
- `A16.09` A clear response to friendly fire (stage 6)
- `A16.11` Dialogue that survives walking, stopping and temporary interruption (stage 6)
- `A16.12` No repeated dialogue announcing an event that has already happened (stage 6)
- `A16.13` Clear downed, dead or unavailable states (stage 6)
- `A16.14` A companion's presence and equipment surviving save and load (stage 6)

### Combat fundamentals  (7 of 15)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Combat was seven rows for the whole layer, and they named the verbs rather than the feedback.

- `A17.01` A clear distinction between exploration and combat readiness (stage 6)
- `A17.06` Reactions showing where damage came from (stage 6)
- `A17.09` A comprehensible relationship between commitment and cancellation (stage 6)
- `A17.10` Reliable switching between available combat actions (stage 6)
- `A17.12` Consistent interaction between attacks and scenery (stage 6)
- `A17.13` A clear end to the encounter (stage 6)
- `A17.15` Camera and effects that leave the important action visible (stage 6)

### Melee combat, where included  (5 of 14)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Melee is the layer this game actually gets, and I gave it three rows.

- `A18.04` Directional movement that does not slide the attacker implausibly into position (stage 6)
- `A18.05` Readable attack recovery (stage 6)
- `A18.07` Clear distinction between blockable and unblockable attacks (stage 6)
- `A18.09` Parry timing with readable success and failure, if present (stage 6)
- `A18.11` Knockback or stagger appropriate to the attack (stage 6)

### Ranged weapons and thrown objects, where included  (13 of 24)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Firearms are rare events here, which made me write three rows and stop. Rare is not absent, and an event needs its feedback.

- `A19.04` Recoil that is visible and reflected in subsequent aim (stage 6)
- `A19.05` Muzzle flash or another appropriate firing cue (stage 6)
- `A19.07` Impacts at the actual hit location (stage 6)
- `A19.08` Different impact responses for flesh, wood, metal and stone (stage 6)
- `A19.10` Ammunition counts that agree with shots fired (stage 6)
- `A19.11` Distinct empty-weapon feedback (stage 6)
- `A19.12` Reloading with correct ammunition transfer (stage 6)
- `A19.13` Reload animation that matches the weapon (stage 6)
- `A19.15` Weapon switching without duplicated or missing weapons (stage 6)
- `A19.18` Controller aiming assistance appropriate to the design (stage 6)
- `A19.20` A visible aiming or trajectory cue for throws where precision is expected (stage 6)
- `A19.21` Thrown objects leaving from a plausible position (stage 6)
- `A19.24` Weapon behaviour near walls that does not visibly put the barrel through everything (stage 6)

### Health, injury, death and retry  (6 of 16)

Should have been caught by **lens 3, moment by moment**. Mode **F1**. Death and retry were two rows. What a player meets after dying is a whole flow.

- `A20.03` Low-health warning without making the game unreadable (stage 3)
- `A20.05` Healing resource consumption that matches the action (stage 3)
- `A20.06` Clear status effects and their duration or removal conditions (stage 3)
- `A20.09` Some indication of the cause of defeat (stage 3)
- `A20.12` Consistent reset of enemies, resources and objectives on retry (stage 3)
- `A20.13` No respawn inside an active unavoidable hazard (stage 3)

### World layout and navigation through space  (7 of 18)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Level design was not one of my department rows at all; world layout arrived only as `interiors` and `the town`.

- `A21.04` Clear distinction between reachable scenery and background scenery (stage 5)
- `A21.08` Consistent visual language for climbable, breakable and inaccessible objects (stage 5)
- `A21.09` Boundaries communicated by believable obstacles or explicit rules (stage 5)
- `A21.10` A usable response to leaving the intended play area (stage 5)
- `A21.14` Travel distances appropriate to available movement options (stage 5)
- `A21.15` A way back from ordinary exploratory detours (stage 5)
- `A21.16` Consistency between visible danger and actual traversal rules (stage 5)

### Environment art and object appearance  (8 of 17)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Environment art gave me materials, grime and LOD. It did not give me the faults a player sees: stretching, flicker, floating, repetition.

- `A22.01` Complete visible surfaces without holes or missing faces (stage 1)
- `A22.03` Textures that do not stretch conspicuously (stage 1)
- `A22.04` Texture scale consistent with real object size (stage 1)
- `A22.06` Object edges that do not all look infinitely sharp (stage 1)
- `A22.08` Believable joins between walls, floors, roofs and terrain (stage 1)
- `A22.09` No conspicuous flickering between overlapping surfaces (stage 1)
- `A22.15` Objects that remain recognisable across lighting conditions (stage 1)
- `A22.17` Interior dressing that survives viewing from both directions (stage 1)

### Lighting and rendering  (4 of 17)

Should have been caught by **lens 2, what runs every frame**. Mode **F4**. The renderer's module list gave me lighting, GI, post-processing and anti-aliasing. It did not give me light leaks, exposure transitions or glass.

- `A23.04` No major light leaking through solid walls (stage 1)
- `A23.14` Motion rendering without severe ghost trails (stage 1)
- `A23.15` Consistent colour and brightness across gameplay and cutscenes (stage 1)
- `A23.17` Important targets remaining distinguishable amid visual effects (stage 1)

### Weather, water and environmental effects, where applicable  (10 of 18)

Should have been caught by **lens 2, what runs every frame**. Mode **F4**. Niagara and Water told me effects and water exist. The rules that make them read as real, rain under a roof, effects that stop with their source, were not in the module names.

- `A24.02` Hanging fabric and similar objects responding to the environment (stage 2)
- `A24.03` Rain that does not visibly fall through ordinary roofs (stage 2)
- `A24.09` Ripples or splashes when entering water (stage 2)
- `A24.10` Wakes from moving boats or swimmers (stage 2)
- `A24.11` Fire giving appropriate light, movement and sound (stage 2)
- `A24.13` Surface-specific debris from impacts (stage 2)
- `A24.15` Footprints or tracks where a visibly impressionable surface invites them (stage 2)
- `A24.16` Effects ending when their source ends (stage 2)
- `A24.17` Effects staying attached to moving sources (stage 2)
- `A24.18` Weather and time changes that do not visibly reset at ordinary area boundaries (stage 2)

### Ambient life and world continuity  (6 of 16)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Ambient life was one row. Continuity, the harder half, was not a row at all.

- `A25.06` Continuity when leaving a small area and immediately returning (stage 2)
- `A25.08` Clear rules for replenishing loot or respawning enemies (stage 2)
- `A25.09` Events that do not visibly restart every time the player crosses a nearby boundary (stage 2)
- `A25.12` Safe handling of time skips with active missions or followers (stage 2)
- `A25.13` Ambient events that allow interruption and recovery (stage 2)
- `A25.16` No immediate repopulation directly in front of the player after a disturbance (stage 2)

### Road vehicles and traffic, where included  (19 of 24)

Should have been caught by **lens 1, who builds it**. Mode **F1**. I wrote traffic and parked vehicles as street dressing and let D24 cap the rest. Mickey's is a MINICAB OFFICE, so driving is closer to this game than the spend rule suggests.

- `A26.02` Entry animation that fits the door and seat (ship-prep)
- `A26.03` Sensible entry when one side is obstructed (ship-prep)
- `A26.05` Acceleration and braking appropriate to the vehicle (ship-prep)
- `A26.06` Steering that remains manageable across speeds (ship-prep)
- `A26.07` Reverse controls that are clear and usable (ship-prep)
- `A26.08` Wheels rotating at a plausible rate (ship-prep)
- `A26.09` Front wheels turning with steering where appropriate (ship-prep)
- `A26.10` Suspension responding to road irregularities (ship-prep)
- `A26.11` Tyre contact that broadly matches the ground (ship-prep)
- `A26.12` Engine sound responding to speed and load (ship-prep)
- `A26.13` Skid and collision sounds responding to the actual event (ship-prep)
- `A26.14` Brake lights, headlights and reversing lights where the vehicle has them (ship-prep)
- `A26.15` A usable driving camera and rearward view (ship-prep)
- `A26.16` A way to leave the vehicle safely (ship-prep)
- `A26.17` Exiting that avoids placing the player inside walls or traffic (ship-prep)
- `A26.21` Traffic responding to obstructions and collisions (stage 2)
- `A26.22` Pedestrians responding to approaching vehicles (stage 2)
- `A26.23` Passengers remaining correctly seated during movement (ship-prep)
- `A26.24` A vehicle remaining where it was left under the game's persistence rules (stage 2)

### Other transport and mounts, where included  (4 of 12)

Should have been caught by **lens 1, who builds it**. Mode **F5**. A port town has boats and a ferry in canon, and no lens of mine produced water transport.

- `A27.08` Boat steering, acceleration and stopping appropriate to water travel (ship-prep)
- `A27.09` Boarding and leaving without falling through the vessel (ship-prep)
- `A27.10` Movement that remains stable on a moving deck (ship-prep)
- `A27.12` Carried equipment and companions surviving transport transitions (ship-prep)

### Spatial sound  (10 of 15)

Should have been caught by **lens 2, what runs every frame**. Mode **F1**. THIS IS THE SECOND SECTION THE ACCIDENT CAME FROM. I had five rows. Astra has fifteen, and ten of them are nowhere.

- `A28.03` Moving sources carrying their sounds with them (stage 2)
- `A28.05` Distant sources losing appropriate detail (stage 2)
- `A28.07` Openings providing a plausible route for sound (stage 2)
- `A28.09` Larger and smaller rooms sounding different where conspicuous (stage 2)
- `A28.10` Smooth acoustic transitions at room boundaries (stage 2)
- `A28.11` Large sources sounding spatially broad rather than like tiny points (stage 2)
- `A28.12` Above and below having useful audible distinction where supported (stage 2)
- `A28.13` A sensible listening position when the camera moves away from the character (stage 2)
- `A28.14` No distant conversation playing at intimate, full-volume closeness (stage 2)
- `A28.15` No obvious snapping between left and right as a source passes nearby (stage 2)

### Foley and event sound  (14 of 18)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Foley was one row, footsteps. Audio departments do the other seventeen.

- `A29.03` Footstep cadence changing with movement speed (stage 2)
- `A29.04` Appropriate landing sound (stage 2)
- `A29.07` Doors sounding when they move and latch (stage 2)
- `A29.08` Pickups and item handling providing subtle confirmation (stage 2)
- `A29.09` Collision sounds appropriate to the materials involved (stage 2)
- `A29.10` Breakage sounds matching the object (stage 2)
- `A29.11` Weapon handling, firing and reloading sounds aligned with actions (stage 2)
- `A29.12` Damage and pain sounds fitting the affected character (stage 2)
- `A29.13` Machines sounding active only while operating (stage 2)
- `A29.14` Splash sounds matching water contact (stage 2)
- `A29.15` Variation that prevents repeated actions sounding mechanically identical (stage 2)
- `A29.16` No double-triggered sound for a single event (stage 2)
- `A29.17` No continued footsteps after the character stops (stage 2)
- `A29.18` Sound events occurring when the action happens rather than noticeably late (stage 2)

### Voice, music and the final audio mix  (7 of 16)

Should have been caught by **lens 1, who builds it**. Mode **F1**. The mix was three rows. Everything about loudness, clipping, loops and state was inside them.

- `A30.05` No clipping or harsh overload during loud events (stage 2)
- `A30.06` No audible clicks at the start or end of loops (stage 2)
- `A30.08` Combat music starting and ending with the encounter (stage 6)
- `A30.11` Avoidance of conspicuously short musical loops (stage 3)
- `A30.13` No dialogue continuing from a dead or departed speaker without explanation (stage 2)
- `A30.14` Audio pausing, resuming and loading consistently with the game state (stage 2)
- `A30.15` Consistent presentation across headphones and supported speaker layouts (stage 2)

### Dialogue and conversations  (8 of 18)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Conversation is this game's pillar and I gave it seven rows, all about the surface rather than the flow.

- `A31.02` Acknowledgement when the player initiates speech (stage 2)
- `A31.03` Conversational distance and facing that look plausible (stage 2)
- `A31.08` Choice selection that does not accidentally confirm during menu navigation (stage 2)
- `A31.09` A predictable response to walking away (stage 2)
- `A31.10` A predictable response to combat interrupting speech (stage 2)
- `A31.16` Subtitles matching the actual spoken line (stage 2)
- `A31.17` Appropriate pauses and turn-taking (stage 2)
- `A31.18` No conspicuous silence while a character appears to be waiting for a missing line (stage 2)

### Cutscenes and cinematic transitions  (8 of 13)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Cinematics gave me a camera and a skip. The state handling around a scene, which is where they break, did not arrive.

- `A32.03` Characters and props arriving in the correct positions (stage 4)
- `A32.04` Player equipment and appearance carried into scenes where appropriate (stage 4)
- `A32.08` Protection against accidentally skipping an entire scene (stage 4)
- `A32.09` Subtitles that survive cinematic framing and letterboxing (stage 4)
- `A32.10` Gameplay resuming in a sensible position and facing (stage 4)
- `A32.11` No damage or enemy activity during a scene that denies player control unless deliberately communicated (stage 4)
- `A32.12` Correct state changes even when a scene is skipped (stage 4)
- `A32.13` No prolonged loading hidden behind a frozen character or black screen without feedback (stage 4)

### Missions, objectives and activities  (15 of 21)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Mission design was not a department row, so objectives arrived only through the thirty-minute walk, which sees a task start and finish and nothing in between.

- `A33.03` Clear distinction between mandatory and optional tasks (stage 4)
- `A33.04` Objective progress updating after relevant actions (stage 4)
- `A33.05` Completion acknowledged rather than silently recorded (stage 4)
- `A33.07` Failure conditions communicated before they matter where possible (stage 4)
- `A33.08` A clear response to leaving an active mission area (stage 4)
- `A33.09` Tasks that survive doing valid steps in an unexpected order (stage 4)
- `A33.10` Recognition of an item already owned when it is requested (stage 4)
- `A33.12` Protection against permanently losing an indispensable quest item (stage 4)
- `A33.13` Required interactions remaining usable despite ordinary world changes (stage 4)
- `A33.14` A way to restart or recover a broken activity (stage 4)
- `A33.15` Clear communication of time limits (stage 4)
- `A33.16` Dialogue and markers agreeing on the destination (stage 4)
- `A33.17` Markers resolving to reachable interaction points (stage 4)
- `A33.19` Completed objectives not continuing to issue obsolete instructions (stage 4)
- `A33.20` A reason to explore beyond the main route (stage 4)

### HUD and moment-to-moment feedback  (11 of 16)

Should have been caught by **lens 2, what runs every frame**. Mode **F1**. UMG and CommonUI gave me the HUD and prompts as two rows. Every rule about what a HUD owes in a busy moment was inside them.

- `A34.02` Ammunition or resource information readable before an action fails (stage 4)
- `A34.04` Feedback when an action is on cooldown or otherwise unavailable (stage 4)
- `A34.06` Aiming indicators visible against varied backgrounds (stage 4)
- `A34.07` Damage direction or an equivalent way to locate unseen danger (stage 6)
- `A34.09` Status-effect indicators that explain their meaning (stage 4)
- `A34.10` Notifications that remain long enough to read (stage 4)
- `A34.11` Notification handling that does not bury urgent information (stage 4)
- `A34.12` No overlapping subtitles, prompts and objective text (stage 4)
- `A34.13` Appropriate removal or reduction of HUD during noninteractive scenes (stage 4)
- `A34.14` A clear indication when the world continues running behind a menu (stage 4)
- `A34.15` UI values that match actual gameplay state (stage 4)

### Maps, journals and navigation aids, where provided  (11 of 20)

Should have been caught by **lens 3, moment by moment**. Mode **F1**. The map was one row, and D20 rules out a minimap, which let me stop thinking about navigation altogether.

- `A35.03` A clear indication of facing or travel direction (stage 4)
- `A35.04` Useful map scale and zoom (stage 4)
- `A35.05` Panning with the current input device (stage 4)
- `A35.06` Legible labels and distinguishable icons (stage 4)
- `A35.07` A legend or explanation for unfamiliar symbols (stage 4)
- `A35.08` Selection of overlapping icons (stage 4)
- `A35.09` A way to place and remove a personal waypoint (stage 4)
- `A35.11` Recalculation after leaving a suggested route (stage 4)
- `A35.12` Height or floor distinction where a flat marker would mislead (stage 4)
- `A35.13` Clear distinction between discovered and undiscovered places (stage 4)
- `A35.14` Clear distinction between completed and incomplete activities (stage 4)

### Inventory, equipment and loot, where included  (13 of 21)

Should have been caught by **lens 3, moment by moment**. Mode **F1**. Inventory was one row. It is a screen with twenty rules.

- `A36.02` Pickup feedback identifying what was acquired (stage 4)
- `A36.05` Sorting or filtering sufficient for the expected inventory size (stage 4)
- `A36.06` Consistent stacking of identical items (stage 4)
- `A36.07` Quantity selection for moving or discarding stacks (stage 4)
- `A36.10` Equipment restrictions explained before selection (stage 4)
- `A36.12` Quick access to frequently used items (stage 4)
- `A36.13` Consistent consumption of single-use items (stage 4)
- `A36.14` A clear capacity or weight rule if capacity is limited (stage 4)
- `A36.15` Feedback when a pickup fails because the inventory is full (stage 4)
- `A36.17` Protection against accidental destruction of valuable items (stage 4)
- `A36.19` Containers retaining sensible contents after being opened (stage 4)
- `A36.20` Inventory state surviving death and reload according to the stated rules (stage 4)
- `A36.21` Menus remaining usable while quantities change (stage 4)

### Shops, economy and crafting, where included  (6 of 16)

Should have been caught by **lens 3, moment by moment**. Mode **F1**. Buy and sell was one row in a game with rackets, debts and a book of fares.

- `A37.04` Preview of the actual transaction quantity and total (stage 6)
- `A37.05` Insufficient-funds feedback that explains the shortfall (stage 6)
- `A37.06` Transactions occurring once per confirmed purchase (stage 6)
- `A37.08` Recovery from accidental sale where a buyback system is provided (stage 6)
- `A37.09` Shop stock and availability behaving consistently (stage 6)
- `A37.16` No unexplained loss of money or materials when an operation is cancelled (stage 6)

### Progression, customisation and difficulty, where included  (5 of 15)

Should have been caught by **lens 1, who builds it**. Mode **F1**. Progression was one row and standing is the game's real progression, so the row was too generic to carry it.

- `A38.03` Explanation of what an upgrade actually changes (stage 4)
- `A38.04` Clear prerequisites and costs (stage 4)
- `A38.05` Immediate application of purchased abilities (stage 4)
- `A38.06` Instruction for newly unlocked actions (stage 4)
- `A38.12` Appropriate acknowledgement when difficulty is changed (stage 4)

### Saving, loading and persistence  (13 of 28)

Should have been caught by **lens 3, moment by moment**. Mode **F3**. My walk saved once and reloaded once. It never had a save fail, a save collide, or a save be interrupted.

- `A39.01` A clear explanation of when progress is saved (stage 4)
- `A39.05` Clear reasons when saving is temporarily unavailable (stage 4)
- `A39.06` A clear distinction between checkpoint, autosave and manual save (stage 4)
- `A39.08` Confirmation before overwriting or deleting a save (stage 4)
- `A39.09` Separate playthroughs or profiles not silently overwriting each other (stage 4)
- `A39.15` Timers and temporary effects restored according to clear rules (stage 4)
- `A39.16` No duplicated rewards or consumed items after reloading (stage 4)
- `A39.17` No loading into an unavoidable death loop (stage 4)
- `A39.21` Clear compatibility handling after updates or missing downloadable content (stage 4)
- `A39.22` Offline saves retained when reconnecting (stage 4)
- `A39.25` Machine-specific graphics settings not making another machine unusable (stage 4)
- `A39.27` Control withheld until the loaded world is ready (stage 4)
- `A39.28` A sensible return to title or another save after load failure (stage 4)

### Pausing, interruption and quitting  (8 of 14)

Should have been caught by **lens 3, moment by moment**. Mode **F3**. Quitting was in my walk. Losing focus, sleeping the machine and closing the process were not.

- `A40.02` A clear distinction between menus that pause and menus that do not (stage 4)
- `A40.04` Resuming without a queued accidental attack or movement (stage 4)
- `A40.05` Sensible behaviour when the application loses focus (stage 4)
- `A40.06` Safe recovery after system sleep or suspend (stage 4)
- `A40.09` A warning when quitting would lose unsaved progress (stage 4)
- `A40.10` Quitting that waits for an active save or clearly explains why it cannot yet finish (stage 4)
- `A40.11` No indefinitely hanging process after closing the game (stage 4)
- `A40.12` No continued game audio after exit (stage 4)

### Graphics and display settings  (7 of 22)

Should have been caught by **lens 4, what the industry checks**. Mode **F1**. Display settings were four rows. The screen has twenty-two, and the plan names three.

- `A41.03` Monitor selection on supported PC setups (stage 4)
- `A41.04` Refresh-rate handling that uses the chosen display correctly (stage 4)
- `A41.09` Texture quality appropriate to available graphics memory (stage 4)
- `A41.16` Clear distinction between rendered frame rate and generated-frame options where offered (stage 4)
- `A41.18` Correct aspect-ratio handling without stretched people or clipped HUD (stage 4)
- `A41.19` Preview or explanation of what a graphics setting changes (stage 4)
- `A41.21` Clear indication when a setting requires restarting (stage 4)

### Audio and control settings  (10 of 20)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. The two guideline sites that enumerate these are refused by this environment, so this lens ran on a reconstruction and produced categories, not checkpoints.

- `A42.02` Volume changes audible while adjusting them (stage 4)
- `A42.04` Speaker and headphone presentation choices where relevant (stage 4)
- `A42.05` A reduced dynamic-range option for quiet listening (stage 4)
- `A42.08` Rebinding of menu actions where necessary for accessibility (stage 4)
- `A42.10` A way to restore default bindings (stage 4)
- `A42.11` Independent horizontal and vertical sensitivity where useful (stage 4)
- `A42.12` Separate aiming and general camera sensitivity (stage 4)
- `A42.15` Stick and trigger response options where supported (stage 4)
- `A42.17` Adjustable vibration and haptic intensity (stage 4)
- `A42.19` Controls explained without requiring memorisation of a diagram (stage 4)

### Accessibility: text and visual information  (7 of 16)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. Same refusal. I built accessibility from three barrier classes and six strategies, which produces headings; the guidelines produce testable lines.

- `A43.03` Text reflow without clipping after enlargement (stage 4)
- `A43.09` Optional emphasis for interactable objects where needed (stage 4)
- `A43.10` A way to distinguish important objects from visual clutter (stage 4)
- `A43.13` Narrated or otherwise accessible error and confirmation messages (stage 4)
- `A43.14` Accessible reading of essential documents and clues (stage 4)
- `A43.15` UI focus that remains visible and inside the active dialogue (stage 4)
- `A43.16` Gameplay information that remains legible after changing display size or resolution (stage 4)

### Accessibility: hearing and speech  (3 of 11)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. Same refusal, and this is the section where a missing line is a player who cannot play.

- `A44.02` Subtitles available before the opening scene (stage 4)
- `A44.06` Sufficient subtitle display time (stage 4)
- `A44.10` Alternatives to required speech input where voice commands exist (stage 4)

### Accessibility: motor control and interaction  (6 of 12)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. Same refusal. Motor accessibility is the area where my reconstruction was thinnest.

- `A45.04` Alternatives to difficult simultaneous button combinations (stage 4)
- `A45.07` Menu operation without precise pointer placement (stage 4)
- `A45.08` Adjustable cursor or menu-navigation speed (stage 4)
- `A45.09` Assistance for sustained steering, aiming or camera control where offered (stage 4)
- `A45.10` A way to pause without demanding the same dexterity as combat (stage 4)
- `A45.11` Support for compatible alternative controllers (stage 4)

### Accessibility: cognition, difficulty and comfort  (5 of 14)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. Same refusal. Comfort and cognition arrived as four rows and needed fourteen.

- `A46.03` Adjustable or pausable reading time (stage 4)
- `A46.04` Clear indication of what changed after a menu action (stage 4)
- `A46.07` Optional navigation assistance where the world is difficult to parse (stage 4)
- `A46.09` Control over camera recentering where it causes discomfort (stage 4)
- `A46.12` Control over repetitive UI pulsing and notifications (stage 4)

### Localisation and text handling  (5 of 12)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. Localisation came from the engine's Localization module and a cert instinct, neither of which enumerates text handling.

- `A47.05` Appropriate line breaks and reading direction (ship-prep)
- `A47.07` Localised button and keyboard instructions that match the actual controls (ship-prep)
- `A47.08` User-entered names preserving supported accents and characters (ship-prep)
- `A47.11` No exposed placeholder keys or internal labels (ship-prep)
- `A47.12` Language changes that apply predictably and explain any restart requirement (ship-prep)

### Performance and technical stability  (10 of 20)

Should have been caught by **lens 2, what runs every frame**. Mode **F4**. The module list gave me frame budget, streaming and significance. Stability under change, which is what these twenty items are, has no module.

- `A48.03` No major hitch at the first use of an ordinary effect or weapon (stage 2)
- `A48.06` Textures resolving before their absence becomes conspicuous (stage 2)
- `A48.09` Menus that remain responsive when the world is busy (stage 2)
- `A48.12` Stable behaviour when changing graphics settings (stage 2)
- `A48.13` Stable behaviour when changing audio or input devices (stage 2)
- `A48.14` Correct recovery after task switching (stage 2)
- `A48.15` No simulation speed changes caused by frame-rate changes (stage 2)
- `A48.18` Error messages that explain the problem in player language (stage 2)
- `A48.19` No routine need to restart the game to restore basic controls or interactions (stage 2)
- `A48.20` Updates that preserve existing progress and settings where promised (stage 2)

### Platform integration and account handling  (7 of 14)

Should have been caught by **lens 4, what the industry checks**. Mode **F2**. Platform certification was the half of lens 4 whose sources are entirely blocked here; I wrote achievements and cloud save and stopped.

- `A49.01` Correct association between the signed-in player and their saves (ship-prep)
- `A49.02` A clear response when an account signs out (ship-prep)
- `A49.03` Controller ownership changing safely with the active user (ship-prep)
- `A49.04` Platform overlays opening and closing without breaking control (ship-prep)
- `A49.05` Screenshots and capture shortcuts working normally (ship-prep)
- `A49.09` Missing content explained without silently damaging saves (ship-prep)
- `A49.12` System sleep and resume behaving predictably (ship-prep)

### Optional presentation and long-term conveniences  (7 of 13)

Should have been caught by **lens 1, who builds it**. Mode **F5**. Marketing capture and community were department rows, so I got photo mode and credits and nothing about what a player does after the ending.

- `A51.02` Photo controls that do not accidentally trigger gameplay actions (ship-prep)
- `A51.04` Captures saved somewhere discoverable (ship-prep)
- `A51.05` A streamer-friendly music option where licensed music would obstruct sharing (ship-prep)
- `A51.06` Rewatchable tutorials, cinematics or records where the game provides an archive (ship-prep)
- `A51.08` Credits that can be paused, scrolled or exited (ship-prep)
- `A51.11` Clear rules for replay, chapter selection or New Game Plus where offered (ship-prep)
- `A51.12` A way to distinguish completed content from remaining content (ship-prep)

## 3. What the plan holds and my checklist missed

99 items. They matter because they are the reverse error: not a gap in
the plan, a gap in the instrument I used to audit it. The largest groups:

**Stealth, trespass and law, where included** (13)
- `A15.03` Consistent effects of lighting if darkness is a stealth mechanic. Held at: INV the lit window as an information carrier
- `A15.04` Sound generation that matches movement and actions. Held at: INV perception, the hearing model
- `A15.05` Readable boundaries for restricted areas. Held at: INV doors and who gets in
- `A15.07` Distinction between suspicious behaviour and an openly hostile act. Held at: INV suspicion and heat
- `A15.08` Witness reactions that depend on whether they could observe the event. Held at: INV witnesses and what they caught
- `A15.09` A visible or audible reporting process if reporting matters. Held at: INV the law and the police
- `A15.10` A chance to respond before an alert spreads, where promised by the design. Held at: INV the gap between the act and the discovery
- `A15.11` Law response proportionate to the apparent offence. Held at: INV the law and the police
- `A15.12` An understandable wanted or pursuit state. Held at: INV the what-they-know HUD for wanted states
- `A15.15` Consistent treatment of disguises or changed appearance if supported. Held at: INV disguise
- `A15.16` Distinction between surrender, escape and renewed aggression. Held at: RES failure-after-arrest
- `A15.17` Clear consequences of fines, arrest or confiscation. Held at: RES failure-after-arrest
- `A15.18` A usable return to ordinary play after punishment or escape. Held at: RES failure-after-arrest

**World layout and navigation through space** (10)
- `A21.01` Human-scale doors, stairs, furniture and streets. Held at: RES atlas-01, dimensioned layouts; INV the town layout
- `A21.02` Plausible connections between adjacent spaces. Held at: RES atlas-01 MICKEYS
- `A21.03` Exteriors and interiors that broadly agree in position and size. Held at: RES atlas-01
- `A21.05` Readable routes through ordinary environments. Held at: INV the town layout, street network
- `A21.06` Landmarks that help orientation. Held at: RES atlas-01; CANON seven districts
- `A21.07` Visually distinct areas rather than indistinguishable repeated streets. Held at: CANON seven districts
- `A21.12` Alternative routes where exploration is presented as open-ended. Held at: RES atlas-01, the yard with two escapes
- `A21.13` Useful destinations rather than scenery alone. Held at: CANON venues and districts
- `A21.17` Clear access rules for closed buildings or locked regions. Held at: INV doors and who gets in
- `A21.18` Indoor layouts that permit both navigation and intended encounters. Held at: RES atlas-01 MICKEYS

**Enemy awareness and decision-making, where combat or stealth exists** (6)
- `A14.02` Solid cover preventing direct sight where expected. Held at: INV perception
- `A14.03` A readable transition from unaware to suspicious to engaged. Held at: INV suspicion and heat; RES detection-legibility
- `A14.05` Investigation of a sound's location rather than magical knowledge of the player. Held at: INV the law and the police, patrol focus
- `A14.07` A distinction between seeing the player and being told about them. Held at: CANON gossip; INV witnesses and what they caught
- `A14.08` Communication of an alert through visible or audible behaviour. Held at: INV the law and the police, denouncing and informers
- `A14.21` No immediate forgetting of a fight merely because the player steps around a corner. Held at: CANON permanent per-NPC memory

**Lighting and rendering** (6)
- `A23.05` Indoor light levels that differ plausibly from outdoors. Held at: DEC 2026-09-23 the day's exposure and fog
- `A23.06` Exposure changes that do not blind the player during ordinary transitions. Held at: DEC 2026-09-23 the night row held at 0.1
- `A23.07` Dark areas that remain playable under the intended rules. Held at: INV light and the time of day, a measured night floor
- `A23.09` Switchable lights whose appearance and illumination change together. Held at: INV light and the time of day, lamps that toggle
- `A23.12` Glass that behaves consistently as transparent, reflective or obscured. Held at: DEC 2026-09-23 lit rooms behind see-through glass
- `A23.16` Distant scenery integrated with sky and atmosphere. Held at: RES photoreal-on-a-budget, the sky

**Environment art and object appearance** (5)
- `A22.07` Buildings and props visibly grounded rather than floating. Held at: RES placement metric, foot-gap to the datum
- `A22.10` Variation that disguises obvious repeated components. Held at: INV props and dressing, 791 items placed by rule
- `A22.12` Furnishing and clutter consistent with a place's function. Held at: ROADMAP stage 5, a designed layout with chosen contents
- `A22.13` Signs and labels that are readable when they matter. Held at: INV brands and signage, 153 pieces of world text
- `A22.14` Period and setting consistency in conspicuous objects. Held at: CANON era, enforced by tools/canon-gate.py

**Ordinary civilian behaviour** (4)
- `A13.10` Hands and props matching the activity being performed. Held at: INV ambient street life, a man fixing a van
- `A13.15` Reactions to a visibly drawn weapon where the setting warrants it. Held at: INV the four-rung concealment model
- `A13.16` Different reactions to harmless proximity and actual violence. Held at: CANON the moat, seven perceivable slots
- `A13.19` A response to an injured or dead person. Held at: INV the gap between the act and the discovery

**Voice, music and the final audio mix** (4)
- `A30.02` Consistent dialogue loudness across speakers. Held at: INV audio mix, a per-bus voice budget
- `A30.04` Speech fitting the speaker's emotional situation. Held at: RES live-speech-architecture
- `A30.10` Appropriate silence and contrast rather than constant maximum intensity. Held at: INV SFX, spare and diegetic by choice
- `A30.16` Radio or other in-world music sounding attached to its source. Held at: CANON Mickey's radio; INV radio and TV

**Dialogue and conversations** (4)
- `A31.07` A distinction between asking for information and making a consequential commitment. Held at: RES holding-information
- `A31.12` Conversation state that does not repeat completed introductions endlessly. Held at: CANON permanent memory; what the town calls you
- `A31.13` Dialogue that acknowledges relevant completed actions. Held at: CANON the moat
- `A31.14` Dialogue that does not refer to absent or dead characters as visibly present. Held at: CANON permanent memory

**Missions, objectives and activities** (4)
- `A33.06` Rewards actually delivered and explained. Held at: INV crime jobs and takings, payout
- `A33.11` A solution when a required character is absent, dead or obstructed. Held at: CANON killing is permanent; RES authored-stories-in-simulation
- `A33.18` Sensible handling of multiple simultaneous missions. Held at: INV crime jobs and takings
- `A33.21` Activity variety appropriate to the game's promised scope. Held at: ROADMAP stage 6, the hours-of-content reading

**Character appearance** (3)
- `A08.02` Consistent scale between characters and their surroundings. Held at: INV bodies and faces, heights 1.58 to 1.91
- `A08.11` Holstered gear occupying a plausible place on the body. Held at: INV the four-rung concealment model
- `A08.16` Visible wetness, dirt or injury where the presentation promises it. Held at: INV blood on the player

**Inventory, equipment and loot, where included** (3)
- `A36.04` Clear distinction between usable, equippable, valuable and quest items. Held at: INV object provenance across five origins
- `A36.08` A clear equipped state. Held at: INV the four-rung concealment model
- `A36.11` Immediate gameplay and visual effects from equipping. Held at: INV disguise

## 4. The master checklist

**It is the file beside this one: [MASTER-CHECKLIST.md](./MASTER-CHECKLIST.md).**
957 rows, every one a specific feature and never a heading, grouped by area,
each with where it stands (`both`, `plan`, `mine`, `blind`, `out`) and its stage
in `ROADMAP.md`. It is a separate file for one reason, stated plainly: the only
way this session can write to the repository is one tool call per file, and the
merged checklist plus this analysis in a single document is larger than one call
can carry. Nothing was cut to make them fit.

## 5. The per-stage index

Item ids only, for folding into `ROADMAP.md`. Counts exclude the rows ruled
out.

| stage | items |
|---|---|
| stage 1 | 47 |
| stage 2 | 230 |
| stage 3 | 139 |
| stage 4 | 291 |
| stage 5 | 24 |
| stage 6 | 82 |
| ship-prep | 70 |
| ruled out | 74 |

**stage 1** (47): A08.07, A08.08, A08.15, A09.01, A09.02, A09.24, A21.01, A21.05, A21.06, A21.07, A22.01, A22.02, A22.03, A22.04, A22.05, A22.06, A22.07, A22.08, A22.09, A22.10, A22.11, A22.12, A22.13, A22.14, A22.15, A22.16, A22.17, A23.01, A23.02, A23.03, A23.04, A23.05, A23.06, A23.07, A23.09, A23.10, A23.12, A23.13, A23.14, A23.15, A23.16, A23.17, A24.05, A41.14, A48.07, P3, V6

**stage 2** (230): A05.01, A05.02, A05.04, A05.05, A05.06, A05.07, A05.08, A05.09, A05.13, A05.14, A05.15, A05.16, A05.21, A05.23, A05.24, A06.01, A06.02, A06.03, A06.04, A06.05, A06.06, A06.07, A06.08, A06.09, A06.10, A06.11, A06.12, A06.13, A06.14, A06.15, A06.16, A06.17, A06.18, A06.19, A06.20, A06.21, A08.01, A08.02, A08.03, A08.04, A08.05, A08.06, A08.09, A08.10, A08.11, A08.12, A08.13, A08.14, A08.16, A09.03, A09.04, A09.05, A09.06, A09.07, A09.08, A09.09, A09.10, A09.11, A09.12, A09.13, A09.14, A09.15, A09.16, A09.18, A09.21, A09.22, A09.23, A10.01, A10.02, A10.03, A10.04, A10.05, A10.06, A10.07, A10.08, A10.09, A10.10, A10.11, A10.12, A10.13, A10.14, A11.08, A11.12, A12.01, A12.02, A12.03, A12.04, A12.05, A12.06, A12.07, A12.08, A12.09, A12.10, A12.11, A12.12, A12.13, A12.14, A12.15, A12.16, A12.17, A12.18, A13.01, A13.02, A13.03, A13.04, A13.05, A13.06, A13.07, A13.08, A13.09, A13.10, A13.12, A13.13, A13.22, A13.23, A13.24, A13.25, A13.26, A20.07, A23.08, A24.01, A24.02, A24.03, A24.04, A24.06, A24.07, A24.09, A24.10, A24.11, A24.12, A24.13, A24.15, A24.16, A24.17, A24.18, A25.01, A25.02, A25.03, A25.04, A25.05, A25.06, A25.07, A25.08, A25.09, A25.10, A25.12, A25.13, A25.14, A25.15, A25.16, A26.20, A26.21, A26.22, A26.24, A28.01, A28.02, A28.03, A28.04, A28.05, A28.06, A28.07, A28.08, A28.09, A28.10, A28.11, A28.12, A28.13, A28.14, A28.15, A29.01, A29.02, A29.03, A29.04, A29.05, A29.06, A29.07, A29.08, A29.09, A29.10, A29.11, A29.12, A29.13, A29.14, A29.15, A29.16, A29.17, A29.18, A30.01, A30.02, A30.04, A30.05, A30.06, A30.10, A30.12, A30.13, A30.14, A30.15, A31.02, A31.03, A31.04, A31.06, A31.07, A31.08, A31.09, A31.10, A31.15, A31.16, A31.17, A31.18, A32.02, A32.05, A44.05, A48.01, A48.02, A48.03, A48.06, A48.08, A48.09, A48.11, A48.12, A48.13, A48.14, A48.15, A48.18, A48.19, A48.20, H9, N7, V1, V2

**stage 3** (139): A05.12, A07.01, A07.02, A07.03, A07.04, A07.05, A07.06, A07.07, A07.08, A07.09, A07.10, A07.11, A07.12, A07.13, A07.14, A07.15, A07.16, A07.17, A07.18, A07.19, A11.02, A11.04, A11.05, A11.06, A11.07, A11.09, A11.10, A11.11, A11.13, A11.14, A11.15, A11.16, A11.17, A11.18, A11.19, A11.20, A11.21, A11.22, A11.23, A11.24, A13.11, A13.14, A13.15, A13.16, A13.17, A13.18, A13.19, A13.20, A13.21, A14.01, A14.02, A14.03, A14.04, A14.05, A14.06, A14.07, A14.08, A14.09, A14.10, A14.11, A14.12, A14.13, A14.14, A14.15, A14.16, A14.17, A14.18, A14.19, A14.20, A14.21, A14.22, A14.23, A15.01, A15.02, A15.03, A15.04, A15.05, A15.06, A15.07, A15.08, A15.09, A15.10, A15.11, A15.12, A15.13, A15.14, A15.15, A15.16, A15.17, A15.18, A15.19, A17.14, A20.03, A20.05, A20.06, A20.08, A20.09, A20.10, A20.12, A20.13, A20.14, A20.15, A24.08, A24.14, A25.11, A30.03, A30.07, A30.09, A30.11, A31.01, A31.05, A31.12, A31.13, A31.14, A33.06, A33.11, A34.03, A36.04, A36.16, A36.18, A38.02, A38.07, A38.14, A38.15, A39.04, A39.10, A39.11, A39.12, A39.13, A39.14, A39.18, A39.20, A48.16, A51.09, A51.10, K7, V3, V8, V9

**stage 4** (291): A01.01, A01.02, A01.03, A01.04, A01.05, A01.06, A01.07, A01.09, A01.10, A01.11, A01.12, A01.13, A01.15, A01.16, A01.17, A01.18, A02.01, A02.02, A02.03, A02.04, A02.05, A02.06, A02.07, A02.08, A02.09, A02.10, A02.11, A02.12, A02.13, A02.14, A02.15, A02.16, A02.17, A02.18, A02.20, A03.01, A03.02, A03.03, A03.04, A03.05, A03.06, A03.08, A03.09, A03.10, A03.11, A03.12, A03.13, A03.14, A03.15, A03.16, A03.17, A03.18, A03.19, A03.20, A03.22, A03.23, A03.24, A04.01, A04.02, A04.03, A04.04, A04.05, A04.06, A04.07, A04.08, A04.09, A04.10, A04.11, A04.12, A04.13, A04.14, A04.15, A04.16, A05.03, A05.22, A11.01, A11.03, A20.11, A20.16, A31.11, A32.01, A32.03, A32.04, A32.06, A32.07, A32.08, A32.09, A32.10, A32.11, A32.12, A32.13, A33.01, A33.02, A33.03, A33.04, A33.05, A33.07, A33.08, A33.09, A33.10, A33.12, A33.13, A33.14, A33.15, A33.16, A33.17, A33.18, A33.19, A33.20, A34.02, A34.04, A34.05, A34.06, A34.09, A34.10, A34.11, A34.12, A34.13, A34.14, A34.15, A34.16, A35.01, A35.02, A35.03, A35.04, A35.05, A35.06, A35.07, A35.08, A35.09, A35.11, A35.12, A35.13, A35.14, A35.15, A35.16, A35.17, A36.01, A36.02, A36.03, A36.05, A36.06, A36.07, A36.08, A36.10, A36.11, A36.12, A36.13, A36.14, A36.15, A36.17, A36.19, A36.20, A36.21, A38.01, A38.03, A38.04, A38.05, A38.06, A38.11, A38.12, A39.01, A39.02, A39.03, A39.05, A39.06, A39.07, A39.08, A39.09, A39.15, A39.16, A39.17, A39.19, A39.21, A39.22, A39.25, A39.27, A39.28, A40.01, A40.02, A40.03, A40.04, A40.05, A40.06, A40.07, A40.08, A40.09, A40.10, A40.11, A40.12, A40.13, A40.14, A41.01, A41.02, A41.03, A41.04, A41.05, A41.06, A41.07, A41.08, A41.09, A41.10, A41.11, A41.13, A41.15, A41.16, A41.17, A41.18, A41.19, A41.20, A41.21, A41.22, A42.01, A42.02, A42.03, A42.04, A42.05, A42.07, A42.08, A42.09, A42.10, A42.11, A42.12, A42.13, A42.14, A42.15, A42.16, A42.17, A42.19, A43.01, A43.02, A43.03, A43.04, A43.05, A43.06, A43.07, A43.09, A43.10, A43.11, A43.12, A43.13, A43.14, A43.15, A43.16, A44.01, A44.02, A44.03, A44.04, A44.06, A44.07, A44.08, A44.09, A44.10, A45.01, A45.02, A45.03, A45.04, A45.05, A45.07, A45.08, A45.09, A45.10, A45.11, A46.01, A46.02, A46.03, A46.04, A46.05, A46.06, A46.07, A46.08, A46.09, A46.10, A46.11, A46.12, A46.13, A46.14, A49.10, A49.11, A49.14, A51.03, A51.07, A51.13, A1, A2, D1, E4, F2, F7, O6, V10

**stage 5** (24): A01.14, A02.19, A05.10, A05.11, A21.02, A21.03, A21.04, A21.08, A21.09, A21.10, A21.11, A21.12, A21.13, A21.14, A21.15, A21.16, A21.17, A21.18, A39.26, A48.04, A48.05, A48.10, J9, U5

**stage 6** (82): A05.17, A09.17, A09.19, A09.20, A16.01, A16.02, A16.03, A16.04, A16.05, A16.06, A16.07, A16.08, A16.09, A16.10, A16.11, A16.12, A16.13, A16.14, A17.01, A17.02, A17.03, A17.04, A17.06, A17.07, A17.08, A17.09, A17.10, A17.11, A17.12, A17.13, A17.15, A18.01, A18.02, A18.03, A18.04, A18.05, A18.06, A18.07, A18.08, A18.09, A18.11, A18.13, A18.14, A19.01, A19.03, A19.04, A19.05, A19.06, A19.07, A19.08, A19.10, A19.11, A19.12, A19.13, A19.15, A19.16, A19.18, A19.20, A19.21, A19.23, A19.24, A20.01, A20.02, A20.04, A27.11, A30.08, A30.16, A33.21, A34.01, A34.07, A37.01, A37.02, A37.03, A37.04, A37.05, A37.06, A37.07, A37.08, A37.09, A37.16, V4, V7

**ship-prep** (70): A01.08, A03.21, A26.01, A26.02, A26.03, A26.04, A26.05, A26.06, A26.07, A26.08, A26.09, A26.10, A26.11, A26.12, A26.13, A26.14, A26.15, A26.16, A26.17, A26.23, A27.07, A27.08, A27.09, A27.10, A27.12, A39.23, A39.24, A42.06, A47.01, A47.02, A47.03, A47.04, A47.05, A47.06, A47.07, A47.08, A47.09, A47.10, A47.11, A47.12, A48.17, A49.01, A49.02, A49.03, A49.04, A49.05, A49.06, A49.07, A49.09, A49.12, A51.01, A51.02, A51.04, A51.05, A51.06, A51.08, A51.11, A51.12, A4, Q5, R11, S5, T1, T4, T5, T6, T7, U3, U4, V5

## 6. Method, and what it cannot tell you

**How each of the 923 was judged.** For each item I decided two things by
reading: does one of my 179 rows name the same behaviour such that a builder
working from my row would produce it, and does the plan name it. The first test
is deliberately strict. A row of mine that names the AREA does not count as
covering a behaviour inside it, because treating a heading as coverage is the
exact error being measured.

**The plan side is the same corpus as before**: `ROADMAP.md`, `canon.md`,
`DECISIONS.md`, the 111-row systems inventory and 69 research files, 73 files in
all. Where an item is marked as held by the plan, the table names the entry.

**What it cannot tell you.** The 923 judgements are mine alone and were not
re-checked by a second pass, so a wrong one shows up as a feature quietly
marked covered. I would expect the error to run in the direction of too much
coverage rather than too little: it is easier to read one of my headings as
covering an item than to notice it does not. Treat the blind-spot count as a
floor.

**The stage assignments are mine**, from a default per area with 81 overrides.
They are a proposal for the local session to fold in, not a ruling.

**Ruled out means a record rules it out**, not that it seemed unlikely. The 74
rows carry the decision: D24 for the spend rule, D18 for content, D20 for the
minimap, D33 for what the player may see, canon for single player and for the
era. Multiplayer is 25 of the 74.
