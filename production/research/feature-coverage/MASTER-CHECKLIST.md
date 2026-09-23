# The master checklist: 957 features

STATUS: SPEC (research delivery). Branch `research/feature-coverage`. This is
section 4 of [DELIVERY.md](./DELIVERY.md) and is a file of its own only because
a single tool call cannot carry both. Read the analysis, the 462 blind spots and
the method there; this is the list.

Every row is a specific feature, never a heading. **Where**: `both` in my
179-row checklist and in the plan, `plan` in the plan only, `mine` in my
checklist only, `blind` in neither, `out` ruled out for this game by its own
decisions. **Stage** is the row of `ROADMAP.md` it belongs to, `ship-prep` for
past the sixth stage, or the decision that rules it out.

### 1. Launching and reaching the game

| id | feature | where | stage |
|---|---|---|---|
| A01.01 | A working launch from the installed shortcut or platform library | blind | stage 4 |
| A01.02 | A visible response while the application starts | blind | stage 4 |
| A01.03 | Startup that does not require unrelated windows or manual commands | blind | stage 4 |
| A01.04 | Clear identification of the game being launched | plan | stage 4 |
| A01.05 | A sensible initial display resolution | both | stage 4 |
| A01.06 | Startup on the intended monitor | blind | stage 4 |
| A01.07 | Initial sound at a reasonable volume | blind | stage 4 |
| A01.08 | Access to language selection before language-dependent instructions | both | ship-prep |
| A01.09 | Access to subtitles before the opening dialogue | both | stage 4 |
| A01.10 | Access to essential accessibility settings before gameplay | plan | stage 4 |
| A01.11 | A readable explanation of required account or permission requests | blind | stage 4 |
| A01.12 | Offline access to offline content where supported | blind | stage 4 |
| A01.13 | A usable response to unavailable online services | blind | stage 4 |
| A01.14 | Progress information during lengthy initial preparation | both | stage 5 |
| A01.15 | An explanation when required content is still installing | blind | stage 4 |
| A01.16 | An actionable error when the game cannot start | blind | stage 4 |
| A01.17 | Remembered first-run choices | both | stage 4 |
| A01.18 | Skippable repeated introductory logos where permitted | blind | stage 4 |

### 2. Title screen and menu navigation

| id | feature | where | stage |
|---|---|---|---|
| A02.01 | A clear distinction between starting, continuing and loading | both | stage 4 |
| A02.02 | "Continue" that selects the appropriate latest progress | both | stage 4 |
| A02.03 | Protection against replacing an existing playthrough with "New Game" | blind | stage 4 |
| A02.04 | A visible selected menu item | blind | stage 4 |
| A02.05 | Menu navigation in a predictable order | blind | stage 4 |
| A02.06 | Consistent confirm and back controls | blind | stage 4 |
| A02.07 | A reliable way back from every screen | blind | stage 4 |
| A02.08 | Mouse support for visible buttons on PC | plan | stage 4 |
| A02.09 | Clickable areas that match their visible buttons | blind | stage 4 |
| A02.10 | Scroll-wheel support for scrolling lists | blind | stage 4 |
| A02.11 | Controller navigation that reaches every setting | mine | stage 4 |
| A02.12 | Selection that remains visible while a list scrolls | blind | stage 4 |
| A02.13 | Useful explanations for disabled options | blind | stage 4 |
| A02.14 | Confirmation before destructive actions | blind | stage 4 |
| A02.15 | Dialogues that capture input without activating buttons behind them | blind | stage 4 |
| A02.16 | Menus that remember position when returning from a detail screen | blind | stage 4 |
| A02.17 | Text entry that works with the current device | blind | stage 4 |
| A02.18 | An on-screen keyboard when physical typing is unavailable | blind | stage 4 |
| A02.19 | Loading or busy feedback after an accepted selection | plan | stage 5 |
| A02.20 | Protection against repeated clicks starting the same operation twice | blind | stage 4 |

### 3. Input fundamentals

| id | feature | where | stage |
|---|---|---|---|
| A03.01 | Movement and actions that respond promptly to input | mine | stage 4 |
| A03.02 | Camera movement that responds promptly | mine | stage 4 |
| A03.03 | Consistent controls across equivalent situations | blind | stage 4 |
| A03.04 | Correct button prompts for the connected device | mine | stage 4 |
| A03.05 | Prompts that update after rebinding | blind | stage 4 |
| A03.06 | Switching between supported mouse, keyboard and controller input | both | stage 4 |
| A03.07 | Simultaneous input where useful, such as controller movement with gyro aiming | out | no gyro: PC, keyboard and pad |
| A03.08 | No duplicate action from one physical button press | blind | stage 4 |
| A03.09 | Correct distinction between pressing, holding and releasing | mine | stage 4 |
| A03.10 | Clear feedback when an action requires holding | blind | stage 4 |
| A03.11 | Reasonable tolerance for slightly early action presses | blind | stage 4 |
| A03.12 | Predictable handling of conflicting simultaneous inputs | blind | stage 4 |
| A03.13 | Movement that stops when the movement input stops | blind | stage 4 |
| A03.14 | No stuck movement after opening a menu or changing focus | blind | stage 4 |
| A03.15 | No attack caused by the same click that dismisses a menu | blind | stage 4 |
| A03.16 | No unexpected action from an input held through a loading screen | blind | stage 4 |
| A03.17 | Analogue movement speed on supported sticks | blind | stage 4 |
| A03.18 | Equal intended movement speed in straight and diagonal directions | blind | stage 4 |
| A03.19 | Sensible controller dead zones | mine | stage 4 |
| A03.20 | Predictable mouse movement without unwanted acceleration | mine | stage 4 |
| A03.21 | A usable response to controller disconnection | mine | ship-prep |
| A03.22 | Safe reconnection without restarting the game | blind | stage 4 |
| A03.23 | Input handling independent of frame rate | blind | stage 4 |
| A03.24 | Clear control ownership when several controllers are connected | blind | stage 4 |

### 4. Onboarding and the first minute

| id | feature | where | stage |
|---|---|---|---|
| A04.01 | An unmistakable transition from watching to controlling | blind | stage 4 |
| A04.02 | A starting camera aimed at something useful | blind | stage 4 |
| A04.03 | A safe opportunity to test movement | blind | stage 4 |
| A04.04 | A safe opportunity to test the camera | blind | stage 4 |
| A04.05 | A clear initial purpose | both | stage 4 |
| A04.06 | A discoverable first destination or activity | both | stage 4 |
| A04.07 | Instructions shown when their actions become relevant | both | stage 4 |
| A04.08 | Instructions using the player's actual bindings | blind | stage 4 |
| A04.09 | Time to read an instruction before it disappears | blind | stage 4 |
| A04.10 | Confirmation that a tutorial action succeeded | blind | stage 4 |
| A04.11 | A way to recover instructions dismissed accidentally | blind | stage 4 |
| A04.12 | Tutorials that cope with an action performed early | blind | stage 4 |
| A04.13 | Tutorials that stop repeating after understanding is demonstrated | blind | stage 4 |
| A04.14 | A way to revisit controls and basic rules | blind | stage 4 |
| A04.15 | A way to skip familiar instruction without breaking progression | blind | stage 4 |
| A04.16 | An opening that permits ordinary experimentation without trapping the player | blind | stage 4 |

### 5. Camera behaviour

| id | feature | where | stage |
|---|---|---|---|
| A05.01 | Free horizontal and vertical looking within the intended camera model | plan | stage 2 |
| A05.02 | A useful default viewing distance in third person | plan | stage 2 |
| A05.03 | A useful default field of view | mine | stage 4 |
| A05.04 | Camera framing that keeps the controlled character readable | both | stage 2 |
| A05.05 | Camera movement that does not lag so much that control feels detached | both | stage 2 |
| A05.06 | Camera collision that prevents seeing through walls | both | stage 2 |
| A05.07 | Camera recovery after an obstruction clears | blind | stage 2 |
| A05.08 | Smooth handling of poles, foliage and other small obstructions | blind | stage 2 |
| A05.09 | Character fading or another solution when the camera gets too close | blind | stage 2 |
| A05.10 | A usable view in cramped interiors | mine | stage 5 |
| A05.11 | A usable view while ascending and descending stairs | blind | stage 5 |
| A05.12 | A usable view while climbing or hanging | blind | stage 3 |
| A05.13 | Camera behaviour that does not repeatedly fight manual input | blind | stage 2 |
| A05.14 | Predictable recentering, if provided | blind | stage 2 |
| A05.15 | Smooth transitions between exploration, aiming and conversation | both | stage 2 |
| A05.16 | Appropriate framing when crouching or going prone | blind | stage 2 |
| A05.17 | Aiming that follows the intended sightline | blind | stage 6 |
| A05.18 | Shoulder switching where the aiming design requires it | out | D24: not a shooter, no cover system |
| A05.19 | Lock-on that selects a plausible target, if present | out | D24: not a shooter, no lock-on |
| A05.20 | Lock-on that releases sensibly when a target dies or disappears | out | D24: not a shooter, no lock-on |
| A05.21 | Camera recovery after a cutscene without disorienting rotation | blind | stage 2 |
| A05.22 | Camera shake that does not hide essential information | both | stage 4 |
| A05.23 | Stable horizon and manageable camera motion | blind | stage 2 |
| A05.24 | A sensible relationship between camera direction and movement after a camera cut | blind | stage 2 |

### 6. Walking, running and turning

| id | feature | where | stage |
|---|---|---|---|
| A06.01 | Walking, jogging and running appropriate to the control scheme | both | stage 2 |
| A06.02 | A usable sprint where the game's travel distances imply one | both | stage 2 |
| A06.03 | Acceleration that fits the character's apparent weight | mine | stage 2 |
| A06.04 | Deceleration that fits the intended responsiveness | mine | stage 2 |
| A06.05 | Turning that looks and feels connected to the feet | mine | stage 2 |
| A06.06 | Stationary turning without impossible foot rotation | mine | stage 2 |
| A06.07 | Backward movement with an appropriate gait | blind | stage 2 |
| A06.08 | Sideways movement with an appropriate gait | blind | stage 2 |
| A06.09 | Smooth transitions between movement speeds | mine | stage 2 |
| A06.10 | Consistent movement relative to the camera or facing convention | blind | stage 2 |
| A06.11 | Reliable movement over small kerbs and floor seams | mine | stage 2 |
| A06.12 | Reliable movement up and down ordinary stairs | blind | stage 2 |
| A06.13 | Sensible behaviour on slopes | blind | stage 2 |
| A06.14 | Clear limits on slopes too steep to climb | blind | stage 2 |
| A06.15 | No snagging on tiny decorative geometry | mine | stage 2 |
| A06.16 | Predictable sliding along a wall instead of becoming stuck | mine | stage 2 |
| A06.17 | A crouched collision shape that actually fits under lower obstacles | blind | stage 2 |
| A06.18 | Prevention of standing through a ceiling | blind | stage 2 |
| A06.19 | Movement that follows moving platforms | blind | stage 2 |
| A06.20 | Appropriate restrictions while carrying, aiming or injured | plan | stage 2 |
| A06.21 | Recovery from being wedged between objects | mine | stage 2 |

### 7. Jumping, climbing and water traversal, where supported

| id | feature | where | stage |
|---|---|---|---|
| A07.01 | A responsive jump with readable height and distance | mine | stage 3 |
| A07.02 | Predictable control while airborne | mine | stage 3 |
| A07.03 | Forgiveness around ledge departure and landing inputs | mine | stage 3 |
| A07.04 | A landing animation appropriate to the fall | blind | stage 3 |
| A07.05 | Fall damage that follows understandable rules | blind | stage 3 |
| A07.06 | A clear distinction between a safe drop and a dangerous fall | blind | stage 3 |
| A07.07 | Consistent identification of vaultable obstacles | mine | stage 3 |
| A07.08 | Vaulting that fits the obstacle's height and thickness | mine | stage 3 |
| A07.09 | Mantling that puts hands and feet on the actual surface | mine | stage 3 |
| A07.10 | Prevention of climbing into blocked space | blind | stage 3 |
| A07.11 | A way to cancel or drop from a climb | blind | stage 3 |
| A07.12 | Ladder entry from plausible positions | blind | stage 3 |
| A07.13 | Ladder exit without falling or becoming stuck | blind | stage 3 |
| A07.14 | Consistent behaviour at climbable and non-climbable lookalikes | blind | stage 3 |
| A07.15 | Clear entry into swimming rather than walking underwater | both | stage 3 |
| A07.16 | A usable transition between swimming and the shore | both | stage 3 |
| A07.17 | Swim movement and animation that agree | both | stage 3 |
| A07.18 | Readable breath or drowning rules if diving is possible | blind | stage 3 |
| A07.19 | Water camera and sound changes when submerged | blind | stage 3 |
| A07.20 | Appropriate controls and release behaviour for ropes, ziplines or grapples, if included | out | D24: no ropes, ziplines or grapples in a 1990 port town |

### 8. Character appearance

| id | feature | where | stage |
|---|---|---|---|
| A08.01 | A complete character model from ordinary viewing angles | both | stage 2 |
| A08.02 | Consistent scale between characters and their surroundings | plan | stage 2 |
| A08.03 | Clothing that fits the body rather than visibly floating | both | stage 2 |
| A08.04 | Believable hands and fingers | blind | stage 2 |
| A08.05 | Believable eyes, eyelids and gaze direction | mine | stage 2 |
| A08.06 | A mouth interior that survives ordinary close-ups | blind | stage 2 |
| A08.07 | Hair that behaves plausibly under the game's lighting | mine | stage 1 |
| A08.08 | Skin, fabric, leather and metal that look different | both | stage 1 |
| A08.09 | Equipped clothing and gear reflected on the visible character | both | stage 2 |
| A08.10 | Held items attached to the correct hand and orientation | blind | stage 2 |
| A08.11 | Holstered gear occupying a plausible place on the body | plan | stage 2 |
| A08.12 | No major body or clothing gaps during ordinary poses | blind | stage 2 |
| A08.13 | A character shadow that matches the visible body and equipment | mine | stage 2 |
| A08.14 | Consistent appearance across gameplay, menus and cutscenes | blind | stage 2 |
| A08.15 | Detail changes with distance that do not transform identity | mine | stage 1 |
| A08.16 | Visible wetness, dirt or injury where the presentation promises it | plan | stage 2 |
| A08.17 | Consistent first-person hands, body and third-person appearance where both views exist | out | third person only; no first-person view is planned |

### 9. Body animation and physical contact

| id | feature | where | stage |
|---|---|---|---|
| A09.01 | Idle breathing and small posture changes | both | stage 1 |
| A09.02 | Idle variation rather than a conspicuous repeating loop | both | stage 1 |
| A09.03 | Feet that remain planted instead of sliding during stops | both | stage 2 |
| A09.04 | Foot placement that follows stairs and uneven ground | both | stage 2 |
| A09.05 | Knees and hips that accommodate different foot heights | both | stage 2 |
| A09.06 | Stride length that matches travel speed | blind | stage 2 |
| A09.07 | Body lean during acceleration and turning | blind | stage 2 |
| A09.08 | Smooth transitions between idle, walking and running | mine | stage 2 |
| A09.09 | Upper-body actions that coexist with leg movement | blind | stage 2 |
| A09.10 | Head movement that is partly independent of the torso | mine | stage 2 |
| A09.11 | Hands that meet handles, rails and other contact points | blind | stage 2 |
| A09.12 | Finger poses that fit held objects | blind | stage 2 |
| A09.13 | Two-handed objects held by both hands | blind | stage 2 |
| A09.14 | Seated bodies that actually meet the chair | both | stage 2 |
| A09.15 | Sit-down and stand-up transitions | both | stage 2 |
| A09.16 | Animation appropriate to the character's current weapon or burden | blind | stage 2 |
| A09.17 | Reactions to impacts that fit their direction | both | stage 6 |
| A09.18 | Interruptions that leave the body in a valid pose | blind | stage 2 |
| A09.19 | Recovery from knockdown that connects to the final fallen position | blind | stage 6 |
| A09.20 | Death motion or ragdoll behaviour consistent with the hit | mine | stage 6 |
| A09.21 | Bodies that rest on the ground rather than hover | blind | stage 2 |
| A09.22 | Hair, clothing and attachments that follow body movement | mine | stage 2 |
| A09.23 | No sudden default pose while an animation loads | blind | stage 2 |
| A09.24 | No identical synchronised idle motion across a crowd | mine | stage 1 |

### 10. Looking, expressions and social presentation

| id | feature | where | stage |
|---|---|---|---|
| A10.01 | NPCs turning their eyes toward someone addressing them | mine | stage 2 |
| A10.02 | NPCs turning their head toward an approaching player when appropriate | mine | stage 2 |
| A10.03 | The torso turning when the player moves beyond a comfortable head angle | blind | stage 2 |
| A10.04 | Limits that prevent impossible head and neck rotation | blind | stage 2 |
| A10.05 | Gaze directed at the player's face rather than their feet or empty space | mine | stage 2 |
| A10.06 | Eye contact that occasionally breaks | blind | stage 2 |
| A10.07 | Blinking rather than a permanent stare | blind | stage 2 |
| A10.08 | Facial expression that broadly fits the line being spoken | both | stage 2 |
| A10.09 | Listener reactions while another person speaks | blind | stage 2 |
| A10.10 | Gestures that fit the conversation rather than random arm waving | blind | stage 2 |
| A10.11 | People orienting toward a shared point of interest | blind | stage 2 |
| A10.12 | Expression and posture changes when a conversation becomes hostile | plan | stage 2 |
| A10.13 | Reactions to excessive proximity | plan | stage 2 |
| A10.14 | A return to ordinary activity after the player leaves | blind | stage 2 |

### 11. Object interaction

| id | feature | where | stage |
|---|---|---|---|
| A11.01 | A clear way to distinguish usable objects from decoration | mine | stage 4 |
| A11.02 | A stable current interaction target | blind | stage 3 |
| A11.03 | Prompts attached to the intended object | mine | stage 4 |
| A11.04 | Interaction range that matches apparent reach | blind | stage 3 |
| A11.05 | No interaction through an intervening solid wall | blind | stage 3 |
| A11.06 | Appropriate priority when talk, loot and open share a button | blind | stage 3 |
| A11.07 | A clear description of the action before committing | blind | stage 3 |
| A11.08 | Feedback when an interaction succeeds | both | stage 2 |
| A11.09 | Feedback explaining why an interaction is unavailable | blind | stage 3 |
| A11.10 | Progress indication for prolonged interactions | blind | stage 3 |
| A11.11 | Predictable cancellation of prolonged interactions | blind | stage 3 |
| A11.12 | Doors whose visible movement agrees with their blocking state | both | stage 2 |
| A11.13 | Door handling that does not trap the player inside the door | blind | stage 3 |
| A11.14 | Sensible behaviour when a door's path is obstructed | blind | stage 3 |
| A11.15 | Locked doors that communicate their status | both | stage 3 |
| A11.16 | Containers that visibly and mechanically change after opening | both | stage 3 |
| A11.17 | Pickups that disappear or change state when taken | both | stage 3 |
| A11.18 | A dropped object appearing in a sensible reachable place | plan | stage 3 |
| A11.19 | Readable inspection views for documents and small objects | plan | stage 3 |
| A11.20 | Return from inspection to the previous position and context | blind | stage 3 |
| A11.21 | Controls for switches, terminals and similar devices that produce a visible result | blind | stage 3 |
| A11.22 | Occupied objects that cannot be used by two characters simultaneously | blind | stage 3 |
| A11.23 | Clear distinction between harmless use and theft or aggression | both | stage 3 |
| A11.24 | An interaction ending cleanly if its object is destroyed or removed | blind | stage 3 |

### 12. Collision and object physics

| id | feature | where | stage |
|---|---|---|---|
| A12.01 | Solid ground everywhere that appears walkable | blind | stage 2 |
| A12.02 | Solid walls where walls are visibly present | blind | stage 2 |
| A12.03 | Collision shapes that broadly match visible objects | mine | stage 2 |
| A12.04 | Doorways that admit a character who visibly fits | blind | stage 2 |
| A12.05 | Small loose objects that do not act like immovable roadblocks | mine | stage 2 |
| A12.06 | Heavy objects that do not behave like weightless toys | mine | stage 2 |
| A12.07 | Dropped objects falling under consistent gravity | mine | stage 2 |
| A12.08 | Objects settling instead of vibrating indefinitely | blind | stage 2 |
| A12.09 | No explosive physics response from mild contact | blind | stage 2 |
| A12.10 | Fast objects that do not pass through obvious barriers | blind | stage 2 |
| A12.11 | Characters not pushing through one another without explanation | mine | stage 2 |
| A12.12 | A workable solution to being blocked by a friendly character | blind | stage 2 |
| A12.13 | Moving machinery carrying or blocking objects consistently | blind | stage 2 |
| A12.14 | Appropriate friction on visibly different surfaces where it matters | blind | stage 2 |
| A12.15 | Physical reactions accompanied by matching sound | blind | stage 2 |
| A12.16 | Broken objects leaving plausible remnants if destruction exists | mine | stage 2 |
| A12.17 | Destruction that changes collision as well as appearance | mine | stage 2 |
| A12.18 | Stable interaction between bodies, props and uneven ground | blind | stage 2 |

### 13. Ordinary civilian behaviour

| id | feature | where | stage |
|---|---|---|---|
| A13.01 | People walking somewhere or doing something | both | stage 2 |
| A13.02 | Variation in pace, posture and activity | both | stage 2 |
| A13.03 | People avoiding one another while moving | both | stage 2 |
| A13.04 | People avoiding the player when there is room | mine | stage 2 |
| A13.05 | A response to bumping into someone | mine | stage 2 |
| A13.06 | A response to repeatedly blocking someone's route | blind | stage 2 |
| A13.07 | Navigation through doorways without permanent jams | blind | stage 2 |
| A13.08 | Use of stairs rather than walking through their geometry | blind | stage 2 |
| A13.09 | Plausible transitions into sitting, working or leaning | both | stage 2 |
| A13.10 | Hands and props matching the activity being performed | plan | stage 2 |
| A13.11 | Conversations with actual listeners | both | stage 3 |
| A13.12 | People taking turns rather than all speaking simultaneously | blind | stage 2 |
| A13.13 | Ambient speech that is not repeated every few seconds | both | stage 2 |
| A13.14 | Reactions to a nearby loud or unusual event | both | stage 3 |
| A13.15 | Reactions to a visibly drawn weapon where the setting warrants it | plan | stage 3 |
| A13.16 | Different reactions to harmless proximity and actual violence | plan | stage 3 |
| A13.17 | Fleeing or taking cover from danger | blind | stage 3 |
| A13.18 | Escape routes that lead away from danger | blind | stage 3 |
| A13.19 | A response to an injured or dead person | plan | stage 3 |
| A13.20 | A way for panic to resolve once danger passes | blind | stage 3 |
| A13.21 | People who do not immediately resume cheerful chatter beside an ongoing emergency | blind | stage 3 |
| A13.22 | Consistency between a person's current behaviour and dialogue | blind | stage 2 |
| A13.23 | Appropriate response when spoken to during another activity | blind | stage 2 |
| A13.24 | Some continuity when briefly looking away and back | blind | stage 2 |
| A13.25 | No obvious appearance or disappearance directly in view | blind | stage 2 |
| A13.26 | A reasonable solution when an NPC's intended route becomes blocked | blind | stage 2 |

### 14. Enemy awareness and decision-making, where combat or stealth exists

| id | feature | where | stage |
|---|---|---|---|
| A14.01 | Enemies detecting the player through understandable senses | both | stage 3 |
| A14.02 | Solid cover preventing direct sight where expected | plan | stage 3 |
| A14.03 | A readable transition from unaware to suspicious to engaged | plan | stage 3 |
| A14.04 | Reactions to relevant sounds | both | stage 3 |
| A14.05 | Investigation of a sound's location rather than magical knowledge of the player | plan | stage 3 |
| A14.06 | Search focused on the last plausible known position | blind | stage 3 |
| A14.07 | A distinction between seeing the player and being told about them | plan | stage 3 |
| A14.08 | Communication of an alert through visible or audible behaviour | plan | stage 3 |
| A14.09 | Enemy movement that uses the actual available routes | blind | stage 3 |
| A14.10 | Replanning when doors, vehicles or other obstacles move | blind | stage 3 |
| A14.11 | Enemies able to negotiate ordinary stairs and doorways | blind | stage 3 |
| A14.12 | Combat positioning that avoids all enemies occupying one point | blind | stage 3 |
| A14.13 | Enemies using appropriate engagement distance | blind | stage 3 |
| A14.14 | Enemies not firing continuously into an obvious obstruction | blind | stage 3 |
| A14.15 | Appropriate retreat, advance or repositioning | blind | stage 3 |
| A14.16 | A response to being flanked | blind | stage 3 |
| A14.17 | A response to allies being injured or killed | blind | stage 3 |
| A14.18 | Believable limits on accuracy and reaction speed | blind | stage 3 |
| A14.19 | Clear reasons when an enemy cannot be damaged or interrupted | blind | stage 3 |
| A14.20 | A sensible end to searching or combat | blind | stage 3 |
| A14.21 | No immediate forgetting of a fight merely because the player steps around a corner | plan | stage 3 |
| A14.22 | No pursuit through impossible or inaccessible routes | blind | stage 3 |
| A14.23 | No permanent lock into combat after every threat is gone | blind | stage 3 |

### 15. Stealth, trespass and law, where included

| id | feature | where | stage |
|---|---|---|---|
| A15.01 | A clear indication of whether the player is concealed or exposed | both | stage 3 |
| A15.02 | Consistent effects of posture on visibility and noise | both | stage 3 |
| A15.03 | Consistent effects of lighting if darkness is a stealth mechanic | plan | stage 3 |
| A15.04 | Sound generation that matches movement and actions | plan | stage 3 |
| A15.05 | Readable boundaries for restricted areas | plan | stage 3 |
| A15.06 | A warning or understandable transition before punishment where appropriate | blind | stage 3 |
| A15.07 | Distinction between suspicious behaviour and an openly hostile act | plan | stage 3 |
| A15.08 | Witness reactions that depend on whether they could observe the event | plan | stage 3 |
| A15.09 | A visible or audible reporting process if reporting matters | plan | stage 3 |
| A15.10 | A chance to respond before an alert spreads, where promised by the design | plan | stage 3 |
| A15.11 | Law response proportionate to the apparent offence | plan | stage 3 |
| A15.12 | An understandable wanted or pursuit state | plan | stage 3 |
| A15.13 | Clear conditions for losing pursuit | both | stage 3 |
| A15.14 | Searches that do not continuously know the hidden player's exact location | blind | stage 3 |
| A15.15 | Consistent treatment of disguises or changed appearance if supported | plan | stage 3 |
| A15.16 | Distinction between surrender, escape and renewed aggression | plan | stage 3 |
| A15.17 | Clear consequences of fines, arrest or confiscation | plan | stage 3 |
| A15.18 | A usable return to ordinary play after punishment or escape | plan | stage 3 |
| A15.19 | No punishment for an action the controls misleadingly presented as harmless | blind | stage 3 |

### 16. Companions and friendly allies, where included

| id | feature | where | stage |
|---|---|---|---|
| A16.01 | Following at a useful distance | blind | stage 6 |
| A16.02 | Keeping up without repeatedly falling far behind | blind | stage 6 |
| A16.03 | Slowing down or waiting appropriately during guided travel | blind | stage 6 |
| A16.04 | Yielding when blocking a doorway or corridor | blind | stage 6 |
| A16.05 | Navigating the same ordinary obstacles as the player | blind | stage 6 |
| A16.06 | Sensible recovery when separated | blind | stage 6 |
| A16.07 | Entering and leaving vehicles appropriately | blind | stage 6 |
| A16.08 | Participation in combat consistent with the companion's role | plan | stage 6 |
| A16.09 | A clear response to friendly fire | blind | stage 6 |
| A16.10 | Commands with acknowledgement and visible results | plan | stage 6 |
| A16.11 | Dialogue that survives walking, stopping and temporary interruption | blind | stage 6 |
| A16.12 | No repeated dialogue announcing an event that has already happened | blind | stage 6 |
| A16.13 | Clear downed, dead or unavailable states | blind | stage 6 |
| A16.14 | A companion's presence and equipment surviving save and load | blind | stage 6 |

### 17. Combat fundamentals

| id | feature | where | stage |
|---|---|---|---|
| A17.01 | A clear distinction between exploration and combat readiness | blind | stage 6 |
| A17.02 | Attacks that occur in response to the intended input | both | stage 6 |
| A17.03 | Reach and hit detection that broadly match the visible action | mine | stage 6 |
| A17.04 | A visible or audible distinction between hitting and missing | mine | stage 6 |
| A17.05 | A distinction between damaging armour, a shield and an exposed target | out | D24 and the era: no armour or shields in 1990 Meridian |
| A17.06 | Reactions showing where damage came from | blind | stage 6 |
| A17.07 | Clear feedback for blocked, resisted or ineffective attacks | mine | stage 6 |
| A17.08 | Enemy attacks that can be read before they connect | mine | stage 6 |
| A17.09 | A comprehensible relationship between commitment and cancellation | blind | stage 6 |
| A17.10 | Reliable switching between available combat actions | blind | stage 6 |
| A17.11 | A readable resource cost where attacks consume stamina or energy | plan | stage 6 |
| A17.12 | Consistent interaction between attacks and scenery | blind | stage 6 |
| A17.13 | A clear end to the encounter | blind | stage 6 |
| A17.14 | Feedback for victory, escape or failure | both | stage 3 |
| A17.15 | Camera and effects that leave the important action visible | blind | stage 6 |

### 18. Melee combat, where included

| id | feature | where | stage |
|---|---|---|---|
| A18.01 | Attack animations that fit the equipped weapon | both | stage 6 |
| A18.02 | Contact timing that agrees with damage timing | mine | stage 6 |
| A18.03 | Plausible weapon reach | mine | stage 6 |
| A18.04 | Directional movement that does not slide the attacker implausibly into position | blind | stage 6 |
| A18.05 | Readable attack recovery | blind | stage 6 |
| A18.06 | Blocking that responds within the game's stated rules | both | stage 6 |
| A18.07 | Clear distinction between blockable and unblockable attacks | blind | stage 6 |
| A18.08 | Dodge movement with understandable distance and vulnerability | both | stage 6 |
| A18.09 | Parry timing with readable success and failure, if present | blind | stage 6 |
| A18.10 | Combos that accept inputs predictably, if present | out | D24: fighting gets the smallest budget; no combo system |
| A18.11 | Knockback or stagger appropriate to the attack | blind | stage 6 |
| A18.12 | Finishing moves that cope with nearby walls and furniture | out | D18: no cruelty as spectacle, so no finishers |
| A18.13 | Multiple attackers behaving in a way the camera and controls can handle | both | stage 6 |
| A18.14 | Consistent handling of unarmed attacks versus weapons | both | stage 6 |

### 19. Ranged weapons and thrown objects, where included

| id | feature | where | stage |
|---|---|---|---|
| A19.01 | Aiming aligned with where the shot can actually travel | both | stage 6 |
| A19.02 | A solution to the camera seeing around cover while the muzzle remains blocked | out | D24: not a shooter, no cover system |
| A19.03 | Projectile or hit behaviour consistent with the weapon | both | stage 6 |
| A19.04 | Recoil that is visible and reflected in subsequent aim | blind | stage 6 |
| A19.05 | Muzzle flash or another appropriate firing cue | blind | stage 6 |
| A19.06 | Firing sound appropriate to the weapon and distance | plan | stage 6 |
| A19.07 | Impacts at the actual hit location | blind | stage 6 |
| A19.08 | Different impact responses for flesh, wood, metal and stone | blind | stage 6 |
| A19.09 | Appropriate rate of fire | out | D24: firearms are events, not a rate of fire |
| A19.10 | Ammunition counts that agree with shots fired | blind | stage 6 |
| A19.11 | Distinct empty-weapon feedback | blind | stage 6 |
| A19.12 | Reloading with correct ammunition transfer | blind | stage 6 |
| A19.13 | Reload animation that matches the weapon | blind | stage 6 |
| A19.14 | Predictable handling of interrupted reloads | out | D24: not a shooter |
| A19.15 | Weapon switching without duplicated or missing weapons | blind | stage 6 |
| A19.16 | Equip and holster transitions that match the visible state | plan | stage 6 |
| A19.17 | Clear distinctions between ammunition types or firing modes, if supported | out | D24: no ammunition types or firing modes |
| A19.18 | Controller aiming assistance appropriate to the design | blind | stage 6 |
| A19.19 | Scope transitions that preserve orientation | out | D24: no scopes |
| A19.20 | A visible aiming or trajectory cue for throws where precision is expected | blind | stage 6 |
| A19.21 | Thrown objects leaving from a plausible position | blind | stage 6 |
| A19.22 | Explosion effects with understandable range and cover interaction | out | D24 and the era: no explosives as a player weapon |
| A19.23 | Damage feedback that distinguishes a hit from a kill | both | stage 6 |
| A19.24 | Weapon behaviour near walls that does not visibly put the barrel through everything | blind | stage 6 |

### 20. Health, injury, death and retry

| id | feature | where | stage |
|---|---|---|---|
| A20.01 | An understandable representation of remaining health | both | stage 6 |
| A20.02 | Clear distinction between damage, healing and temporary protection | both | stage 6 |
| A20.03 | Low-health warning without making the game unreadable | blind | stage 3 |
| A20.04 | Healing controls that give immediate acknowledgement | both | stage 6 |
| A20.05 | Healing resource consumption that matches the action | blind | stage 3 |
| A20.06 | Clear status effects and their duration or removal conditions | blind | stage 3 |
| A20.07 | Readable stamina or similar exhaustion feedback | both | stage 2 |
| A20.08 | A clear death or defeat state | both | stage 3 |
| A20.09 | Some indication of the cause of defeat | blind | stage 3 |
| A20.10 | A quick, understandable retry route | both | stage 3 |
| A20.11 | Checkpoints placed to avoid needless repetition | both | stage 4 |
| A20.12 | Consistent reset of enemies, resources and objectives on retry | blind | stage 3 |
| A20.13 | No respawn inside an active unavoidable hazard | blind | stage 3 |
| A20.14 | Clear penalties for death, if any | plan | stage 3 |
| A20.15 | A way to recover from an unwinnable checkpoint or stuck state | plan | stage 3 |
| A20.16 | Ability to adjust relevant difficulty or assistance without discarding the playthrough | mine | stage 4 |

### 21. World layout and navigation through space

| id | feature | where | stage |
|---|---|---|---|
| A21.01 | Human-scale doors, stairs, furniture and streets | plan | stage 1 |
| A21.02 | Plausible connections between adjacent spaces | plan | stage 5 |
| A21.03 | Exteriors and interiors that broadly agree in position and size | plan | stage 5 |
| A21.04 | Clear distinction between reachable scenery and background scenery | blind | stage 5 |
| A21.05 | Readable routes through ordinary environments | plan | stage 1 |
| A21.06 | Landmarks that help orientation | plan | stage 1 |
| A21.07 | Visually distinct areas rather than indistinguishable repeated streets | plan | stage 1 |
| A21.08 | Consistent visual language for climbable, breakable and inaccessible objects | blind | stage 5 |
| A21.09 | Boundaries communicated by believable obstacles or explicit rules | blind | stage 5 |
| A21.10 | A usable response to leaving the intended play area | blind | stage 5 |
| A21.11 | Space for the character and camera along intended routes | mine | stage 5 |
| A21.12 | Alternative routes where exploration is presented as open-ended | plan | stage 5 |
| A21.13 | Useful destinations rather than scenery alone | plan | stage 5 |
| A21.14 | Travel distances appropriate to available movement options | blind | stage 5 |
| A21.15 | A way back from ordinary exploratory detours | blind | stage 5 |
| A21.16 | Consistency between visible danger and actual traversal rules | blind | stage 5 |
| A21.17 | Clear access rules for closed buildings or locked regions | plan | stage 5 |
| A21.18 | Indoor layouts that permit both navigation and intended encounters | plan | stage 5 |

### 22. Environment art and object appearance

| id | feature | where | stage |
|---|---|---|---|
| A22.01 | Complete visible surfaces without holes or missing faces | blind | stage 1 |
| A22.02 | Appropriate detail at normal viewing distance | both | stage 1 |
| A22.03 | Textures that do not stretch conspicuously | blind | stage 1 |
| A22.04 | Texture scale consistent with real object size | blind | stage 1 |
| A22.05 | Materials distinguishable as wood, metal, glass, cloth and stone | both | stage 1 |
| A22.06 | Object edges that do not all look infinitely sharp | blind | stage 1 |
| A22.07 | Buildings and props visibly grounded rather than floating | plan | stage 1 |
| A22.08 | Believable joins between walls, floors, roofs and terrain | blind | stage 1 |
| A22.09 | No conspicuous flickering between overlapping surfaces | blind | stage 1 |
| A22.10 | Variation that disguises obvious repeated components | plan | stage 1 |
| A22.11 | Wear and dirt consistent with use and exposure | both | stage 1 |
| A22.12 | Furnishing and clutter consistent with a place's function | plan | stage 1 |
| A22.13 | Signs and labels that are readable when they matter | plan | stage 1 |
| A22.14 | Period and setting consistency in conspicuous objects | plan | stage 1 |
| A22.15 | Objects that remain recognisable across lighting conditions | blind | stage 1 |
| A22.16 | Detail changes with distance that do not cause conspicuous shape popping | mine | stage 1 |
| A22.17 | Interior dressing that survives viewing from both directions | blind | stage 1 |

### 23. Lighting and rendering

| id | feature | where | stage |
|---|---|---|---|
| A23.01 | Lighting that establishes readable shapes and space | both | stage 1 |
| A23.02 | Shadows connecting people and objects to their surroundings | both | stage 1 |
| A23.03 | Shadows that broadly follow moving characters and lights | both | stage 1 |
| A23.04 | No major light leaking through solid walls | blind | stage 1 |
| A23.05 | Indoor light levels that differ plausibly from outdoors | plan | stage 1 |
| A23.06 | Exposure changes that do not blind the player during ordinary transitions | plan | stage 1 |
| A23.07 | Dark areas that remain playable under the intended rules | plan | stage 1 |
| A23.08 | Visible lamps whose surroundings respond to their light | both | stage 2 |
| A23.09 | Switchable lights whose appearance and illumination change together | plan | stage 1 |
| A23.10 | Reflections that broadly agree with the environment | both | stage 1 |
| A23.11 | A sensible solution for player visibility in mirrors where mirrors are usable | out | no usable mirrors planned; D24 spend rule |
| A23.12 | Glass that behaves consistently as transparent, reflective or obscured | plan | stage 1 |
| A23.13 | Stable image edges without distracting shimmer | mine | stage 1 |
| A23.14 | Motion rendering without severe ghost trails | blind | stage 1 |
| A23.15 | Consistent colour and brightness across gameplay and cutscenes | blind | stage 1 |
| A23.16 | Distant scenery integrated with sky and atmosphere | plan | stage 1 |
| A23.17 | Important targets remaining distinguishable amid visual effects | blind | stage 1 |

### 24. Weather, water and environmental effects, where applicable

| id | feature | where | stage |
|---|---|---|---|
| A24.01 | Vegetation moving appropriately in wind | mine | stage 2 |
| A24.02 | Hanging fabric and similar objects responding to the environment | blind | stage 2 |
| A24.03 | Rain that does not visibly fall through ordinary roofs | blind | stage 2 |
| A24.04 | A change in rain sound when moving under cover | mine | stage 2 |
| A24.05 | Wet surfaces looking different from dry ones | both | stage 1 |
| A24.06 | Plausible transitions into and out of weather | both | stage 2 |
| A24.07 | Character or NPC responses to conspicuous weather where the presentation warrants them | mine | stage 2 |
| A24.08 | Water surfaces moving rather than appearing solid | both | stage 3 |
| A24.09 | Ripples or splashes when entering water | blind | stage 2 |
| A24.10 | Wakes from moving boats or swimmers | blind | stage 2 |
| A24.11 | Fire giving appropriate light, movement and sound | blind | stage 2 |
| A24.12 | Smoke and dust appearing to originate from their causes | mine | stage 2 |
| A24.13 | Surface-specific debris from impacts | blind | stage 2 |
| A24.14 | Temporary marks such as bullet holes or blood persisting long enough to connect cause and effect | plan | stage 3 |
| A24.15 | Footprints or tracks where a visibly impressionable surface invites them | blind | stage 2 |
| A24.16 | Effects ending when their source ends | blind | stage 2 |
| A24.17 | Effects staying attached to moving sources | blind | stage 2 |
| A24.18 | Weather and time changes that do not visibly reset at ordinary area boundaries | blind | stage 2 |

### 25. Ambient life and world continuity

| id | feature | where | stage |
|---|---|---|---|
| A25.01 | Background activity beyond the player's immediate objective | both | stage 2 |
| A25.02 | Ambient sound appropriate to the location | both | stage 2 |
| A25.03 | Population density that fits the place and time | both | stage 2 |
| A25.04 | People occupying different activities rather than all wandering | both | stage 2 |
| A25.05 | A plausible distinction between open and closed businesses, if operating hours exist | plan | stage 2 |
| A25.06 | Continuity when leaving a small area and immediately returning | blind | stage 2 |
| A25.07 | Consistent handling of dropped objects and casualties | plan | stage 2 |
| A25.08 | Clear rules for replenishing loot or respawning enemies | blind | stage 2 |
| A25.09 | Events that do not visibly restart every time the player crosses a nearby boundary | blind | stage 2 |
| A25.10 | Day and night changes reflected in lighting and relevant activity, if time advances | both | stage 2 |
| A25.11 | A wait or sleep mechanism where schedules make waiting necessary | both | stage 3 |
| A25.12 | Safe handling of time skips with active missions or followers | blind | stage 2 |
| A25.13 | Ambient events that allow interruption and recovery | blind | stage 2 |
| A25.14 | Animals behaving like animals rather than stationary ornaments, where present | mine | stage 2 |
| A25.15 | Birds or small wildlife reacting to close movement or noise | mine | stage 2 |
| A25.16 | No immediate repopulation directly in front of the player after a disturbance | blind | stage 2 |

### 26. Road vehicles and traffic, where included

| id | feature | where | stage |
|---|---|---|---|
| A26.01 | A clear way to enter the intended vehicle and seat | plan | ship-prep |
| A26.02 | Entry animation that fits the door and seat | blind | ship-prep |
| A26.03 | Sensible entry when one side is obstructed | blind | ship-prep |
| A26.04 | Driving controls that respond consistently | plan | ship-prep |
| A26.05 | Acceleration and braking appropriate to the vehicle | blind | ship-prep |
| A26.06 | Steering that remains manageable across speeds | blind | ship-prep |
| A26.07 | Reverse controls that are clear and usable | blind | ship-prep |
| A26.08 | Wheels rotating at a plausible rate | blind | ship-prep |
| A26.09 | Front wheels turning with steering where appropriate | blind | ship-prep |
| A26.10 | Suspension responding to road irregularities | blind | ship-prep |
| A26.11 | Tyre contact that broadly matches the ground | blind | ship-prep |
| A26.12 | Engine sound responding to speed and load | blind | ship-prep |
| A26.13 | Skid and collision sounds responding to the actual event | blind | ship-prep |
| A26.14 | Brake lights, headlights and reversing lights where the vehicle has them | blind | ship-prep |
| A26.15 | A usable driving camera and rearward view | blind | ship-prep |
| A26.16 | A way to leave the vehicle safely | blind | ship-prep |
| A26.17 | Exiting that avoids placing the player inside walls or traffic | blind | ship-prep |
| A26.18 | Vehicle damage communicated visually or mechanically | out | D24: not a driving game, smallest budget |
| A26.19 | Recovery from an overturned or irretrievably stuck vehicle | out | D24: not a driving game |
| A26.20 | Traffic following plausible lanes and junction rules | both | stage 2 |
| A26.21 | Traffic responding to obstructions and collisions | blind | stage 2 |
| A26.22 | Pedestrians responding to approaching vehicles | blind | stage 2 |
| A26.23 | Passengers remaining correctly seated during movement | blind | ship-prep |
| A26.24 | A vehicle remaining where it was left under the game's persistence rules | blind | stage 2 |

### 27. Other transport and mounts, where included

| id | feature | where | stage |
|---|---|---|---|
| A27.01 | Mounting and dismounting from plausible positions | out | no mounts in 1990 Britain |
| A27.02 | Mount movement whose gait matches its speed | out | no mounts |
| A27.03 | Mount turning and stopping that fit its body | out | no mounts |
| A27.04 | Mount avoidance of ordinary obstacles | out | no mounts |
| A27.05 | A usable way to call, locate or recover an owned mount | out | no mounts |
| A27.06 | Clear mount health, stamina or distress where those affect play | out | no mounts |
| A27.07 | Boats floating at a plausible height | plan | ship-prep |
| A27.08 | Boat steering, acceleration and stopping appropriate to water travel | blind | ship-prep |
| A27.09 | Boarding and leaving without falling through the vessel | blind | ship-prep |
| A27.10 | Movement that remains stable on a moving deck | blind | ship-prep |
| A27.11 | Public transport that clearly communicates boarding and destination | plan | stage 6 |
| A27.12 | Carried equipment and companions surviving transport transitions | blind | ship-prep |

### 28. Spatial sound

| id | feature | where | stage |
|---|---|---|---|
| A28.01 | Sounds coming from the direction of their source | mine | stage 2 |
| A28.02 | Sound direction changing correctly as the player turns | mine | stage 2 |
| A28.03 | Moving sources carrying their sounds with them | blind | stage 2 |
| A28.04 | Distant sources sounding quieter than nearby sources | both | stage 2 |
| A28.05 | Distant sources losing appropriate detail | blind | stage 2 |
| A28.06 | Walls and closed doors muffling relevant sounds | both | stage 2 |
| A28.07 | Openings providing a plausible route for sound | blind | stage 2 |
| A28.08 | Room acoustics differing from open air | both | stage 2 |
| A28.09 | Larger and smaller rooms sounding different where conspicuous | blind | stage 2 |
| A28.10 | Smooth acoustic transitions at room boundaries | blind | stage 2 |
| A28.11 | Large sources sounding spatially broad rather than like tiny points | blind | stage 2 |
| A28.12 | Above and below having useful audible distinction where supported | blind | stage 2 |
| A28.13 | A sensible listening position when the camera moves away from the character | blind | stage 2 |
| A28.14 | No distant conversation playing at intimate, full-volume closeness | blind | stage 2 |
| A28.15 | No obvious snapping between left and right as a source passes nearby | blind | stage 2 |

### 29. Foley and event sound

| id | feature | where | stage |
|---|---|---|---|
| A29.01 | Footsteps synchronised with foot contact | both | stage 2 |
| A29.02 | Different footstep sounds on different surfaces | both | stage 2 |
| A29.03 | Footstep cadence changing with movement speed | blind | stage 2 |
| A29.04 | Appropriate landing sound | blind | stage 2 |
| A29.05 | Clothing and equipment movement where audible | plan | stage 2 |
| A29.06 | Breathing or exertion appropriate to strenuous activity | both | stage 2 |
| A29.07 | Doors sounding when they move and latch | blind | stage 2 |
| A29.08 | Pickups and item handling providing subtle confirmation | blind | stage 2 |
| A29.09 | Collision sounds appropriate to the materials involved | blind | stage 2 |
| A29.10 | Breakage sounds matching the object | blind | stage 2 |
| A29.11 | Weapon handling, firing and reloading sounds aligned with actions | blind | stage 2 |
| A29.12 | Damage and pain sounds fitting the affected character | blind | stage 2 |
| A29.13 | Machines sounding active only while operating | blind | stage 2 |
| A29.14 | Splash sounds matching water contact | blind | stage 2 |
| A29.15 | Variation that prevents repeated actions sounding mechanically identical | blind | stage 2 |
| A29.16 | No double-triggered sound for a single event | blind | stage 2 |
| A29.17 | No continued footsteps after the character stops | blind | stage 2 |
| A29.18 | Sound events occurring when the action happens rather than noticeably late | blind | stage 2 |

### 30. Voice, music and the final audio mix

| id | feature | where | stage |
|---|---|---|---|
| A30.01 | Important speech intelligible over ambience and action | both | stage 2 |
| A30.02 | Consistent dialogue loudness across speakers | plan | stage 2 |
| A30.03 | Distinct voices that help identify recurring characters | both | stage 3 |
| A30.04 | Speech fitting the speaker's emotional situation | plan | stage 2 |
| A30.05 | No clipping or harsh overload during loud events | blind | stage 2 |
| A30.06 | No audible clicks at the start or end of loops | blind | stage 2 |
| A30.07 | Music transitions that do not cut abruptly without intention | both | stage 3 |
| A30.08 | Combat music starting and ending with the encounter | blind | stage 6 |
| A30.09 | Exploration music that does not overwhelm ordinary interaction | both | stage 3 |
| A30.10 | Appropriate silence and contrast rather than constant maximum intensity | plan | stage 2 |
| A30.11 | Avoidance of conspicuously short musical loops | blind | stage 3 |
| A30.12 | Important sounds remaining audible in a crowded mix | both | stage 2 |
| A30.13 | No dialogue continuing from a dead or departed speaker without explanation | blind | stage 2 |
| A30.14 | Audio pausing, resuming and loading consistently with the game state | blind | stage 2 |
| A30.15 | Consistent presentation across headphones and supported speaker layouts | blind | stage 2 |
| A30.16 | Radio or other in-world music sounding attached to its source | plan | stage 6 |

### 31. Dialogue and conversations

| id | feature | where | stage |
|---|---|---|---|
| A31.01 | A clear way to start and leave a conversation | both | stage 3 |
| A31.02 | Acknowledgement when the player initiates speech | blind | stage 2 |
| A31.03 | Conversational distance and facing that look plausible | blind | stage 2 |
| A31.04 | Mouth movement synchronised approximately with speech | both | stage 2 |
| A31.05 | Correct association between the speaking voice and visible character | both | stage 3 |
| A31.06 | Dialogue choices that communicate the intended meaning | both | stage 2 |
| A31.07 | A distinction between asking for information and making a consequential commitment | plan | stage 2 |
| A31.08 | Choice selection that does not accidentally confirm during menu navigation | blind | stage 2 |
| A31.09 | A predictable response to walking away | blind | stage 2 |
| A31.10 | A predictable response to combat interrupting speech | blind | stage 2 |
| A31.11 | Important information recoverable after interruption | both | stage 4 |
| A31.12 | Conversation state that does not repeat completed introductions endlessly | plan | stage 3 |
| A31.13 | Dialogue that acknowledges relevant completed actions | plan | stage 3 |
| A31.14 | Dialogue that does not refer to absent or dead characters as visibly present | plan | stage 3 |
| A31.15 | Ambient and important dialogue prevented from talking over one another excessively | both | stage 2 |
| A31.16 | Subtitles matching the actual spoken line | blind | stage 2 |
| A31.17 | Appropriate pauses and turn-taking | blind | stage 2 |
| A31.18 | No conspicuous silence while a character appears to be waiting for a missing line | blind | stage 2 |

### 32. Cutscenes and cinematic transitions

| id | feature | where | stage |
|---|---|---|---|
| A32.01 | A clear distinction between a cutscene and interactive control | mine | stage 4 |
| A32.02 | Camera placement that shows the intended action | both | stage 2 |
| A32.03 | Characters and props arriving in the correct positions | blind | stage 4 |
| A32.04 | Player equipment and appearance carried into scenes where appropriate | blind | stage 4 |
| A32.05 | Facial and body performance consistent with the dialogue | both | stage 2 |
| A32.06 | A way to pause where the presentation permits it | mine | stage 4 |
| A32.07 | A way to skip already-seen scenes | mine | stage 4 |
| A32.08 | Protection against accidentally skipping an entire scene | blind | stage 4 |
| A32.09 | Subtitles that survive cinematic framing and letterboxing | blind | stage 4 |
| A32.10 | Gameplay resuming in a sensible position and facing | blind | stage 4 |
| A32.11 | No damage or enemy activity during a scene that denies player control unless deliberately communicated | blind | stage 4 |
| A32.12 | Correct state changes even when a scene is skipped | blind | stage 4 |
| A32.13 | No prolonged loading hidden behind a frozen character or black screen without feedback | blind | stage 4 |

### 33. Missions, objectives and activities

| id | feature | where | stage |
|---|---|---|---|
| A33.01 | A clear current objective or understandable self-directed goal | both | stage 4 |
| A33.02 | A way to review the objective after forgetting it | both | stage 4 |
| A33.03 | Clear distinction between mandatory and optional tasks | blind | stage 4 |
| A33.04 | Objective progress updating after relevant actions | blind | stage 4 |
| A33.05 | Completion acknowledged rather than silently recorded | blind | stage 4 |
| A33.06 | Rewards actually delivered and explained | plan | stage 3 |
| A33.07 | Failure conditions communicated before they matter where possible | blind | stage 4 |
| A33.08 | A clear response to leaving an active mission area | blind | stage 4 |
| A33.09 | Tasks that survive doing valid steps in an unexpected order | blind | stage 4 |
| A33.10 | Recognition of an item already owned when it is requested | blind | stage 4 |
| A33.11 | A solution when a required character is absent, dead or obstructed | plan | stage 3 |
| A33.12 | Protection against permanently losing an indispensable quest item | blind | stage 4 |
| A33.13 | Required interactions remaining usable despite ordinary world changes | blind | stage 4 |
| A33.14 | A way to restart or recover a broken activity | blind | stage 4 |
| A33.15 | Clear communication of time limits | blind | stage 4 |
| A33.16 | Dialogue and markers agreeing on the destination | blind | stage 4 |
| A33.17 | Markers resolving to reachable interaction points | blind | stage 4 |
| A33.18 | Sensible handling of multiple simultaneous missions | plan | stage 4 |
| A33.19 | Completed objectives not continuing to issue obsolete instructions | blind | stage 4 |
| A33.20 | A reason to explore beyond the main route | blind | stage 4 |
| A33.21 | Activity variety appropriate to the game's promised scope | plan | stage 6 |

### 34. HUD and moment-to-moment feedback

| id | feature | where | stage |
|---|---|---|---|
| A34.01 | Health or equivalent survival information readable when needed | both | stage 6 |
| A34.02 | Ammunition or resource information readable before an action fails | blind | stage 4 |
| A34.03 | Clear current weapon, tool or ability state | plan | stage 3 |
| A34.04 | Feedback when an action is on cooldown or otherwise unavailable | blind | stage 4 |
| A34.05 | Interaction prompts that do not obscure the object | mine | stage 4 |
| A34.06 | Aiming indicators visible against varied backgrounds | blind | stage 4 |
| A34.07 | Damage direction or an equivalent way to locate unseen danger | blind | stage 6 |
| A34.08 | Distinguishable friendly, hostile and neutral indicators where used | out | D33: the player sees their own position, never other minds; no faction markers |
| A34.09 | Status-effect indicators that explain their meaning | blind | stage 4 |
| A34.10 | Notifications that remain long enough to read | blind | stage 4 |
| A34.11 | Notification handling that does not bury urgent information | blind | stage 4 |
| A34.12 | No overlapping subtitles, prompts and objective text | blind | stage 4 |
| A34.13 | Appropriate removal or reduction of HUD during noninteractive scenes | blind | stage 4 |
| A34.14 | A clear indication when the world continues running behind a menu | blind | stage 4 |
| A34.15 | UI values that match actual gameplay state | blind | stage 4 |
| A34.16 | A way to reduce unnecessary HUD elements where supported | mine | stage 4 |

### 35. Maps, journals and navigation aids, where provided

| id | feature | where | stage |
|---|---|---|---|
| A35.01 | A map that opens promptly and returns cleanly to gameplay | both | stage 4 |
| A35.02 | A visible player position | both | stage 4 |
| A35.03 | A clear indication of facing or travel direction | blind | stage 4 |
| A35.04 | Useful map scale and zoom | blind | stage 4 |
| A35.05 | Panning with the current input device | blind | stage 4 |
| A35.06 | Legible labels and distinguishable icons | blind | stage 4 |
| A35.07 | A legend or explanation for unfamiliar symbols | blind | stage 4 |
| A35.08 | Selection of overlapping icons | blind | stage 4 |
| A35.09 | A way to place and remove a personal waypoint | blind | stage 4 |
| A35.10 | A route or directional cue that follows reachable paths where supplied | out | D20: no minimap for phase A |
| A35.11 | Recalculation after leaving a suggested route | blind | stage 4 |
| A35.12 | Height or floor distinction where a flat marker would mislead | blind | stage 4 |
| A35.13 | Clear distinction between discovered and undiscovered places | blind | stage 4 |
| A35.14 | Clear distinction between completed and incomplete activities | blind | stage 4 |
| A35.15 | Navigation aids that remain consistent with world signs and names | plan | stage 4 |
| A35.16 | A journal that preserves useful task and story information | both | stage 4 |
| A35.17 | A way to review recently acquired notes or clues | both | stage 4 |
| A35.18 | Fast-travel eligibility, cost and restrictions explained where fast travel exists | out | a small dense town: no fast travel planned |
| A35.19 | Fast travel arriving at a safe, usable position | out | no fast travel planned |
| A35.20 | Travel preserving relevant equipment, followers and mission state | out | no fast travel planned |

### 36. Inventory, equipment and loot, where included

| id | feature | where | stage |
|---|---|---|---|
| A36.01 | A reliable record of what the player owns | both | stage 4 |
| A36.02 | Pickup feedback identifying what was acquired | blind | stage 4 |
| A36.03 | Item names, quantities and useful descriptions | both | stage 4 |
| A36.04 | Clear distinction between usable, equippable, valuable and quest items | plan | stage 3 |
| A36.05 | Sorting or filtering sufficient for the expected inventory size | blind | stage 4 |
| A36.06 | Consistent stacking of identical items | blind | stage 4 |
| A36.07 | Quantity selection for moving or discarding stacks | blind | stage 4 |
| A36.08 | A clear equipped state | plan | stage 4 |
| A36.09 | Comparison with currently equipped gear | out | no gear statistics to compare; objects carry history, not stats |
| A36.10 | Equipment restrictions explained before selection | blind | stage 4 |
| A36.11 | Immediate gameplay and visual effects from equipping | plan | stage 4 |
| A36.12 | Quick access to frequently used items | blind | stage 4 |
| A36.13 | Consistent consumption of single-use items | blind | stage 4 |
| A36.14 | A clear capacity or weight rule if capacity is limited | blind | stage 4 |
| A36.15 | Feedback when a pickup fails because the inventory is full | blind | stage 4 |
| A36.16 | A way to drop, store or otherwise manage unwanted items | both | stage 3 |
| A36.17 | Protection against accidental destruction of valuable items | blind | stage 4 |
| A36.18 | Clear ownership or theft status where relevant | both | stage 3 |
| A36.19 | Containers retaining sensible contents after being opened | blind | stage 4 |
| A36.20 | Inventory state surviving death and reload according to the stated rules | blind | stage 4 |
| A36.21 | Menus remaining usable while quantities change | blind | stage 4 |

### 37. Shops, economy and crafting, where included

| id | feature | where | stage |
|---|---|---|---|
| A37.01 | Clear prices before purchase | both | stage 6 |
| A37.02 | A visible current balance | plan | stage 6 |
| A37.03 | Distinct buying and selling states | both | stage 6 |
| A37.04 | Preview of the actual transaction quantity and total | blind | stage 6 |
| A37.05 | Insufficient-funds feedback that explains the shortfall | blind | stage 6 |
| A37.06 | Transactions occurring once per confirmed purchase | blind | stage 6 |
| A37.07 | Clear distinction between sale value and purchase price | plan | stage 6 |
| A37.08 | Recovery from accidental sale where a buyback system is provided | blind | stage 6 |
| A37.09 | Shop stock and availability behaving consistently | blind | stage 6 |
| A37.10 | Crafting recipes showing ingredients and output | out | D24: not an economy simulation, no crafting |
| A37.11 | Clear indication of which ingredients are missing | out | no crafting |
| A37.12 | Preview of upgrade effects before spending resources | out | no crafting |
| A37.13 | Crafting consuming the stated ingredients and producing the stated result | out | no crafting |
| A37.14 | Safe handling of crafting while inventory capacity is limited | out | no crafting |
| A37.15 | Clear distinction between repair, upgrade and replacement | out | no crafting or upgrade system |
| A37.16 | No unexplained loss of money or materials when an operation is cancelled | blind | stage 6 |

### 38. Progression, customisation and difficulty, where included

| id | feature | where | stage |
|---|---|---|---|
| A38.01 | Clear feedback when experience or progression is earned | both | stage 4 |
| A38.02 | A readable current level or equivalent advancement state | both | stage 3 |
| A38.03 | Explanation of what an upgrade actually changes | blind | stage 4 |
| A38.04 | Clear prerequisites and costs | blind | stage 4 |
| A38.05 | Immediate application of purchased abilities | blind | stage 4 |
| A38.06 | Instruction for newly unlocked actions | blind | stage 4 |
| A38.07 | Visible acknowledgement of meaningful milestones | plan | stage 3 |
| A38.08 | Customisation previews before commitment | out | a fixed protagonist, Tom Novak: no character creation |
| A38.09 | Character creation that can be inspected under useful lighting | out | no character creation |
| A38.10 | Appearance choices that remain recognisable in gameplay | out | no character creation |
| A38.11 | Difficulty descriptions that say what changes | mine | stage 4 |
| A38.12 | Appropriate acknowledgement when difficulty is changed | blind | stage 4 |
| A38.13 | A clear distinction between cosmetic and mechanical choices | out | no character creation |
| A38.14 | Explanation of irreversible choices or respec limits | plan | stage 3 |
| A38.15 | Progression and unlocks surviving reload | both | stage 3 |

### 39. Saving, loading and persistence

| id | feature | where | stage |
|---|---|---|---|
| A39.01 | A clear explanation of when progress is saved | blind | stage 4 |
| A39.02 | Autosaving at sensible milestones | both | stage 4 |
| A39.03 | A visible indication while a save is in progress | mine | stage 4 |
| A39.04 | Manual saving or an explicitly communicated alternative | both | stage 3 |
| A39.05 | Clear reasons when saving is temporarily unavailable | blind | stage 4 |
| A39.06 | A clear distinction between checkpoint, autosave and manual save | blind | stage 4 |
| A39.07 | Save entries identifiable by time, location or progress | mine | stage 4 |
| A39.08 | Confirmation before overwriting or deleting a save | blind | stage 4 |
| A39.09 | Separate playthroughs or profiles not silently overwriting each other | blind | stage 4 |
| A39.10 | Player location restored to a usable position | both | stage 3 |
| A39.11 | Inventory and equipment restored consistently | both | stage 3 |
| A39.12 | Mission progress and completed choices restored consistently | both | stage 3 |
| A39.13 | Relevant world changes restored consistently | both | stage 3 |
| A39.14 | Relevant NPC states restored consistently | both | stage 3 |
| A39.15 | Timers and temporary effects restored according to clear rules | blind | stage 4 |
| A39.16 | No duplicated rewards or consumed items after reloading | blind | stage 4 |
| A39.17 | No loading into an unavoidable death loop | blind | stage 4 |
| A39.18 | Previous valid progress surviving an interrupted save | both | stage 3 |
| A39.19 | A useful message when storage is full or unwritable | mine | stage 4 |
| A39.20 | Recovery options for a damaged save where possible | both | stage 3 |
| A39.21 | Clear compatibility handling after updates or missing downloadable content | blind | stage 4 |
| A39.22 | Offline saves retained when reconnecting | blind | stage 4 |
| A39.23 | Cloud conflicts presented without silently destroying newer progress | mine | ship-prep |
| A39.24 | Progress transferring correctly between supported machines | mine | ship-prep |
| A39.25 | Machine-specific graphics settings not making another machine unusable | blind | stage 4 |
| A39.26 | Loading screens that provide progress or signs of life | both | stage 5 |
| A39.27 | Control withheld until the loaded world is ready | blind | stage 4 |
| A39.28 | A sensible return to title or another save after load failure | blind | stage 4 |

### 40. Pausing, interruption and quitting

| id | feature | where | stage |
|---|---|---|---|
| A40.01 | A pause command available during ordinary single-player play | both | stage 4 |
| A40.02 | A clear distinction between menus that pause and menus that do not | blind | stage 4 |
| A40.03 | Simulation, animation and relevant sound pausing consistently | both | stage 4 |
| A40.04 | Resuming without a queued accidental attack or movement | blind | stage 4 |
| A40.05 | Sensible behaviour when the application loses focus | blind | stage 4 |
| A40.06 | Safe recovery after system sleep or suspend | blind | stage 4 |
| A40.07 | A clear route back to the title menu | both | stage 4 |
| A40.08 | A clear quit-to-desktop option on PC | both | stage 4 |
| A40.09 | A warning when quitting would lose unsaved progress | blind | stage 4 |
| A40.10 | Quitting that waits for an active save or clearly explains why it cannot yet finish | blind | stage 4 |
| A40.11 | No indefinitely hanging process after closing the game | blind | stage 4 |
| A40.12 | No continued game audio after exit | blind | stage 4 |
| A40.13 | Settings and intended progress retained on the next launch | both | stage 4 |
| A40.14 | A useful reminder of current objectives after a longer break | mine | stage 4 |

### 41. Graphics and display settings

| id | feature | where | stage |
|---|---|---|---|
| A41.01 | Resolution selection appropriate to the display | both | stage 4 |
| A41.02 | Windowed, borderless or fullscreen options appropriate to the platform | mine | stage 4 |
| A41.03 | Monitor selection on supported PC setups | blind | stage 4 |
| A41.04 | Refresh-rate handling that uses the chosen display correctly | blind | stage 4 |
| A41.05 | A frame-rate limit option on PC | mine | stage 4 |
| A41.06 | Vertical synchronisation or an equivalent tearing control | mine | stage 4 |
| A41.07 | Quality presets with meaningful performance differences | both | stage 4 |
| A41.08 | Individual control over major expensive visual features | both | stage 4 |
| A41.09 | Texture quality appropriate to available graphics memory | blind | stage 4 |
| A41.10 | Field-of-view adjustment where the camera model permits it | mine | stage 4 |
| A41.11 | Brightness or gamma calibration with a useful reference | mine | stage 4 |
| A41.12 | HDR configuration where HDR is supported | out | no HDR target named; PC first, smallest budget |
| A41.13 | Motion-blur control | mine | stage 4 |
| A41.14 | Film grain, chromatic aberration and similar presentation controls where used | plan | stage 1 |
| A41.15 | Upscaling and image-quality choices where supported | both | stage 4 |
| A41.16 | Clear distinction between rendered frame rate and generated-frame options where offered | blind | stage 4 |
| A41.17 | UI scaling that remains usable at the chosen resolution | both | stage 4 |
| A41.18 | Correct aspect-ratio handling without stretched people or clipped HUD | blind | stage 4 |
| A41.19 | Preview or explanation of what a graphics setting changes | blind | stage 4 |
| A41.20 | Confirmation with automatic reversal of an unusable display mode | mine | stage 4 |
| A41.21 | Clear indication when a setting requires restarting | blind | stage 4 |
| A41.22 | Settings that remain applied after restarting | both | stage 4 |

### 42. Audio and control settings

| id | feature | where | stage |
|---|---|---|---|
| A42.01 | Separate master, dialogue, effects and music volume controls | both | stage 4 |
| A42.02 | Volume changes audible while adjusting them | blind | stage 4 |
| A42.03 | Correct selection or following of the intended output device | mine | stage 4 |
| A42.04 | Speaker and headphone presentation choices where relevant | blind | stage 4 |
| A42.05 | A reduced dynamic-range option for quiet listening | blind | stage 4 |
| A42.06 | Independent subtitle and spoken-language settings where supported | both | ship-prep |
| A42.07 | Full rebinding of ordinary gameplay actions | both | stage 4 |
| A42.08 | Rebinding of menu actions where necessary for accessibility | blind | stage 4 |
| A42.09 | Warnings about conflicting bindings | plan | stage 4 |
| A42.10 | A way to restore default bindings | blind | stage 4 |
| A42.11 | Independent horizontal and vertical sensitivity where useful | blind | stage 4 |
| A42.12 | Separate aiming and general camera sensitivity | blind | stage 4 |
| A42.13 | Camera inversion options | mine | stage 4 |
| A42.14 | Adjustable controller dead zones | mine | stage 4 |
| A42.15 | Stick and trigger response options where supported | blind | stage 4 |
| A42.16 | Hold-versus-toggle choices for sustained actions | mine | stage 4 |
| A42.17 | Adjustable vibration and haptic intensity | blind | stage 4 |
| A42.18 | Aim-assistance configuration where assistance is provided | out | D24: not a shooter, no aim assistance to configure |
| A42.19 | Controls explained without requiring memorisation of a diagram | blind | stage 4 |
| A42.20 | Separate contextual bindings where driving or other modes require them | out | driving takes the smallest budget; no separate driving bindings planned |

### 43. Accessibility: text and visual information

| id | feature | where | stage |
|---|---|---|---|
| A43.01 | Readable default text at normal viewing distance | both | stage 4 |
| A43.02 | Adjustable text size | both | stage 4 |
| A43.03 | Text reflow without clipping after enlargement | blind | stage 4 |
| A43.04 | Adequate contrast between text and background | mine | stage 4 |
| A43.05 | Configurable text backgrounds or outlines where needed | mine | stage 4 |
| A43.06 | Important information conveyed through more than colour alone | both | stage 4 |
| A43.07 | Distinguishable friendly, hostile and neutral markers for different colour-vision needs | both | stage 4 |
| A43.08 | Scalable or configurable aiming reticles | out | D24: not a shooter, no reticle |
| A43.09 | Optional emphasis for interactable objects where needed | blind | stage 4 |
| A43.10 | A way to distinguish important objects from visual clutter | blind | stage 4 |
| A43.11 | Menu narration or screen-reader support where offered | mine | stage 4 |
| A43.12 | Narration that announces selection, value and changes | mine | stage 4 |
| A43.13 | Narrated or otherwise accessible error and confirmation messages | blind | stage 4 |
| A43.14 | Accessible reading of essential documents and clues | blind | stage 4 |
| A43.15 | UI focus that remains visible and inside the active dialogue | blind | stage 4 |
| A43.16 | Gameplay information that remains legible after changing display size or resolution | blind | stage 4 |

### 44. Accessibility: hearing and speech

| id | feature | where | stage |
|---|---|---|---|
| A44.01 | Subtitles available for essential dialogue | both | stage 4 |
| A44.02 | Subtitles available before the opening scene | blind | stage 4 |
| A44.03 | Speaker identification when the speaker is not obvious | mine | stage 4 |
| A44.04 | Directional indication for important off-screen speech or sound where needed | mine | stage 4 |
| A44.05 | Captions for essential non-speech sounds | both | stage 2 |
| A44.06 | Sufficient subtitle display time | blind | stage 4 |
| A44.07 | Subtitle styling and size options | both | stage 4 |
| A44.08 | Mono output without losing essential information | mine | stage 4 |
| A44.09 | Visual equivalents for gameplay-critical audio signals | mine | stage 4 |
| A44.10 | Alternatives to required speech input where voice commands exist | blind | stage 4 |
| A44.11 | Separate voice-chat and game-audio control in multiplayer | out | single player: no voice chat |

### 45. Accessibility: motor control and interaction

| id | feature | where | stage |
|---|---|---|---|
| A45.01 | Core actions remappable rather than only swapping entire preset layouts | both | stage 4 |
| A45.02 | Alternatives to repeated rapid button presses | mine | stage 4 |
| A45.03 | Alternatives to prolonged button holds | mine | stage 4 |
| A45.04 | Alternatives to difficult simultaneous button combinations | blind | stage 4 |
| A45.05 | Adjustable timing windows for demanding interactions where offered | mine | stage 4 |
| A45.06 | Quick-time events that can be simplified or bypassed where appropriate | out | no quick-time events planned |
| A45.07 | Menu operation without precise pointer placement | blind | stage 4 |
| A45.08 | Adjustable cursor or menu-navigation speed | blind | stage 4 |
| A45.09 | Assistance for sustained steering, aiming or camera control where offered | blind | stage 4 |
| A45.10 | A way to pause without demanding the same dexterity as combat | blind | stage 4 |
| A45.11 | Support for compatible alternative controllers | blind | stage 4 |
| A45.12 | No mandatory motion gesture without a button alternative where practical | out | PC first: no motion controls |

### 46. Accessibility: cognition, difficulty and comfort

| id | feature | where | stage |
|---|---|---|---|
| A46.01 | Plain explanations of goals and unfamiliar terms | both | stage 4 |
| A46.02 | A way to review tutorials and recent information | mine | stage 4 |
| A46.03 | Adjustable or pausable reading time | blind | stage 4 |
| A46.04 | Clear indication of what changed after a menu action | blind | stage 4 |
| A46.05 | Assistance settings separated by challenge where practical | mine | stage 4 |
| A46.06 | Difficulty changes that do not require restarting the game | mine | stage 4 |
| A46.07 | Optional navigation assistance where the world is difficult to parse | blind | stage 4 |
| A46.08 | Reduced camera shake and head movement options | both | stage 4 |
| A46.09 | Control over camera recentering where it causes discomfort | blind | stage 4 |
| A46.10 | Control over strong flashing and other avoidable visual triggers | mine | stage 4 |
| A46.11 | Reduced motion or animated-background options in menus | both | stage 4 |
| A46.12 | Control over repetitive UI pulsing and notifications | blind | stage 4 |
| A46.13 | Clear content information where potentially distressing content is central | both | stage 4 |
| A46.14 | Accessibility settings retained across sessions | both | stage 4 |

### 47. Localisation and text handling

| id | feature | where | stage |
|---|---|---|---|
| A47.01 | Interface text available in the selected supported language | both | ship-prep |
| A47.02 | Subtitles and audio using the selected supported languages | both | ship-prep |
| A47.03 | Correct characters rather than missing-glyph boxes | mine | ship-prep |
| A47.04 | Longer translated text fitting the interface | mine | ship-prep |
| A47.05 | Appropriate line breaks and reading direction | blind | ship-prep |
| A47.06 | Names and terminology used consistently across dialogue, maps and objectives | plan | ship-prep |
| A47.07 | Localised button and keyboard instructions that match the actual controls | blind | ship-prep |
| A47.08 | User-entered names preserving supported accents and characters | blind | ship-prep |
| A47.09 | Sensible number, date and measurement formatting | mine | ship-prep |
| A47.10 | Legible translated versions of essential in-world writing | plan | ship-prep |
| A47.11 | No exposed placeholder keys or internal labels | blind | ship-prep |
| A47.12 | Language changes that apply predictably and explain any restart requirement | blind | ship-prep |

### 48. Performance and technical stability

| id | feature | where | stage |
|---|---|---|---|
| A48.01 | A stable frame rate appropriate to the selected mode | both | stage 2 |
| A48.02 | Even frame timing rather than frequent small freezes | both | stage 2 |
| A48.03 | No major hitch at the first use of an ordinary effect or weapon | blind | stage 2 |
| A48.04 | World loading that keeps up with supported travel speeds | both | stage 5 |
| A48.05 | Terrain and collision loaded before the player reaches them | both | stage 5 |
| A48.06 | Textures resolving before their absence becomes conspicuous | blind | stage 2 |
| A48.07 | No large visible objects appearing suddenly at short range | mine | stage 1 |
| A48.08 | Stable performance in the expected crowd and combat density | both | stage 2 |
| A48.09 | Menus that remain responsive when the world is busy | blind | stage 2 |
| A48.10 | Loading that does not indefinitely freeze without explanation | mine | stage 5 |
| A48.11 | Long-session stability without steadily worsening performance | both | stage 2 |
| A48.12 | Stable behaviour when changing graphics settings | blind | stage 2 |
| A48.13 | Stable behaviour when changing audio or input devices | blind | stage 2 |
| A48.14 | Correct recovery after task switching | blind | stage 2 |
| A48.15 | No simulation speed changes caused by frame-rate changes | blind | stage 2 |
| A48.16 | No obvious corruption after repeated save and load | both | stage 3 |
| A48.17 | A usable recovery route from a crash | mine | ship-prep |
| A48.18 | Error messages that explain the problem in player language | blind | stage 2 |
| A48.19 | No routine need to restart the game to restore basic controls or interactions | blind | stage 2 |
| A48.20 | Updates that preserve existing progress and settings where promised | blind | stage 2 |

### 49. Platform integration and account handling

| id | feature | where | stage |
|---|---|---|---|
| A49.01 | Correct association between the signed-in player and their saves | blind | ship-prep |
| A49.02 | A clear response when an account signs out | blind | ship-prep |
| A49.03 | Controller ownership changing safely with the active user | blind | ship-prep |
| A49.04 | Platform overlays opening and closing without breaking control | blind | ship-prep |
| A49.05 | Screenshots and capture shortcuts working normally | blind | ship-prep |
| A49.06 | Supported achievements or trophies unlocking at the intended time | mine | ship-prep |
| A49.07 | Offline-earned progress synchronising appropriately when supported | mine | ship-prep |
| A49.08 | Owned downloadable content correctly recognised | out | no downloadable content planned |
| A49.09 | Missing content explained without silently damaging saves | blind | ship-prep |
| A49.10 | Required permissions requested at a relevant moment | mine | stage 4 |
| A49.11 | Optional data collection distinguishable from required operation | mine | stage 4 |
| A49.12 | System sleep and resume behaving predictably | blind | ship-prep |
| A49.13 | Handheld or small-display interfaces remaining usable where the platform is supported | out | PC first: no handheld or small-display target |
| A49.14 | Battery or power interruptions not corrupting the last completed save | both | stage 4 |

### 50. Multiplayer and cooperative play, only if included

All twenty-five rows are out under the same decision, so it is stated once here
rather than twenty-five times: CANON says single player, PC first. Multiplayer
is out of this game entirely.

| id | feature | where | stage |
|---|---|---|---|
| A50.01 | A clear way to host, join or find a session | out | single player |
| A50.02 | Clear distinction between private, friends-only and public sessions | out | single player |
| A50.03 | Invitations that reach the correct session | out | single player |
| A50.04 | Useful explanation when joining fails | out | single player |
| A50.05 | Connection progress with a way to cancel | out | single player |
| A50.06 | Region or connection-quality information where latency matters | out | single player |
| A50.07 | Other players' movement represented smoothly enough to interpret | out | single player |
| A50.08 | Hits and interactions resolving consistently enough to feel fair | out | single player |
| A50.09 | Clear ownership of mission progress and rewards | out | single player |
| A50.10 | Clear rules for shared versus individual loot | out | single player |
| A50.11 | Safe handling of players joining or leaving mid-activity | out | single player |
| A50.12 | Recovery or clear consequences when the host disconnects | out | single player |
| A50.13 | Rejoining without unnecessary loss of progress where supported | out | single player |
| A50.14 | Clear downed, dead and spectating states | out | single player |
| A50.15 | A usable revive or respawn flow where the mode includes one | out | single player |
| A50.16 | Communication through voice, text or pings as appropriate | out | single player |
| A50.17 | Voice input and output selection | out | single player |
| A50.18 | Visible microphone state and a reliable mute control | out | single player |
| A50.19 | Individual mute, block and report controls | out | single player |
| A50.20 | Clear communication of friendly-fire rules | out | single player |
| A50.21 | Understandable handling of version or content mismatches | out | single player |
| A50.22 | Clear warning that menus do not pause a live session | out | single player |
| A50.23 | Protection against common forms of cheating or session disruption appropriate to the mode | out | single player |
| A50.24 | Supported cross-play and cross-progression behaving as advertised | out | single player |
| A50.25 | A clear end-of-session flow that preserves earned progress | out | single player |

### 51. Optional presentation and long-term conveniences

| id | feature | where | stage |
|---|---|---|---|
| A51.01 | A photo mode that pauses or clearly explains its live behaviour | both | ship-prep |
| A51.02 | Photo controls that do not accidentally trigger gameplay actions | blind | ship-prep |
| A51.03 | A way to hide the HUD for clean captures | mine | stage 4 |
| A51.04 | Captures saved somewhere discoverable | blind | ship-prep |
| A51.05 | A streamer-friendly music option where licensed music would obstruct sharing | blind | ship-prep |
| A51.06 | Rewatchable tutorials, cinematics or records where the game provides an archive | blind | ship-prep |
| A51.07 | Credits accessible without having to finish the game | both | stage 4 |
| A51.08 | Credits that can be paused, scrolled or exited | blind | ship-prep |
| A51.09 | Clear communication of the ending's effect on continued free play | both | stage 3 |
| A51.10 | A usable post-completion state where continued exploration is offered | plan | stage 3 |
| A51.11 | Clear rules for replay, chapter selection or New Game Plus where offered | blind | ship-prep |
| A51.12 | A way to distinguish completed content from remaining content | blind | ship-prep |
| A51.13 | Returning after a long break without having to reconstruct the entire playthrough from memory | mine | stage 4 |

### 52. From my own checklist, and not in the independent list

The independent list is a list of PLAYER expectations, so it contains nothing
about making the game. That is where most of these come from, and it is the one
place my lens 1 earned its keep.

| id | feature | where | stage |
|---|---|---|---|
| A1 | Splash and logo screens, legal notices | blind | stage 4 |
| A2 | First-run hardware detection and default quality preset | blind | stage 4 |
| A4 | Build version visible to the player | blind | ship-prep |
| D1 | Keyboard and mouse | plan | stage 4 |
| E4 | Look sensitivity and acceleration | plan (partly) | stage 4 |
| F2 | Objective or quest log | plan (partly) | stage 4 |
| F7 | Screen reader or menu narration | blind | stage 4 |
| H9 | Animation budget at crowd scale | blind | stage 2 |
| J9 | Interiors that can be entered | plan | stage 5 |
| K7 | Police and authority response | plan | stage 3 |
| N7 | Live spoken conversation with memory | plan | stage 2 |
| O6 | Statistics and a session summary | blind | stage 4 |
| P3 | Post-processing chain | plan | stage 1 |
| Q5 | Minimum specification and the hardware floor | plan | ship-prep |
| R11 | Accessibility information before purchase | blind | ship-prep |
| S5 | Content variation by locale | blind | ship-prep |
| T1 | A store page, a build and patching | plan (partly) | ship-prep |
| T4 | Age rating submission | blind | ship-prep |
| T5 | EULA and third-party licence attributions | plan | ship-prep |
| T6 | Anti-cheat or DRM decision | blind | ship-prep |
| T7 | Platform terminology and button naming | blind | ship-prep |
| U3 | A way for the player to report a problem | plan | ship-prep |
| U4 | Patch notes and a post-launch plan | blind | ship-prep |
| U5 | Playtesting with people outside the team | plan | stage 5 |
| V1 | Voice casting and direction | plan | stage 2 |
| V10 | A credits screen naming everyone | plan | stage 4 |
| V2 | Motion capture and performance | plan | stage 2 |
| V3 | Music composition and licensing | plan | stage 3 |
| V4 | Brand and legal clearance | plan | stage 6 |
| V5 | Marketing capture: trailers and screenshots | plan (partly) | ship-prep |
| V6 | Art direction and a style bible | plan | stage 1 |
| V7 | Writing at volume, and editing it | plan | stage 6 |
| V8 | QA: functional, compliance and localisation testing | plan | stage 3 |
| V9 | Build and release engineering | plan | stage 3 |
