# Cheap tricks that read as expensive (18 November 2026)

Jafar's question: which cheap tricks make a small team's game look and feel AAA? This page lists documented, professional techniques, what each does to the player, its rough cost to the AI builder, whether LEDGER already has it, and a recommendation. A ranked top ten and a decision list close the page.

How it was made: web search, then fetches only of pages found in those searches, 18 November 2026, about 25 minutes. Other games are known here only from talks, articles and footage descriptions; no game files were opened for this page. Where LEDGER's own studies are cited, they are LEDGER's records, read as they stand.

Marks used:
- Hours are estimates (E) for the AI builder, not measured. They cover building and a first check by eye, not his review.
- "Reached" means the page was fetched and read (through a fetch tool's summary). "Snippet only" means the search result was seen but the page was not read; that is not evidence.
- Epic's documentation pages fetched today are labelled 5.8 or 5.9. LEDGER runs 5.8.2. Any setting named from a 5.9 page must be checked by name in 5.8 before use.
- "LEDGER has" cites a study line or a spec or code file. "Not found" means a search of production/specs, the probe's source and the studies found nothing; it may still exist elsewhere.

## The principle under all of it

- **Polish what players see most, and first.** Naughty Dog gave a whole GDC talk to its polish method: "The Last 10: Going From Good To Awesome", Benson Russell, GDC 2012 (reached: description only, https://gdcvault.com/play/1015601/The-Last-10-Going-From). Asobo made A Plague Tale: Requiem, widely compared with big-budget games, with 15 to 20 artists in about three years ("How To Make AAA-Looking Games Like A Plague Tale: Requiem with 20 Artists", GDC 2023; reached: description only, https://gdcvault.com/play/1029162/How-To-Make-AAA-Looking). The talks themselves were not watched; only their published descriptions were read.
- **Why the opening matters most.** Cheung, Zimmermann and Nagappan, "The First Hour Experience", CHI PLAY 2014 (reached, https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/First20Hour20-20CHIPlay20201420-20preprint2.pdf): the first hour is a probation in which players decide whether to stay. It is qualitative (212 reviews, 35 first-hour reviews, 6 interviews), not a measured quit rate. Josh Bycer, Game Developer, 13 October 2020 (reached, https://www.gamedeveloper.com/design/how-to-judge-game-design-with-achievement-analytics): from Steam achievements, about 26% of Hollow Knight players quit before the first charm and about 32% by the first boss, mostly within two hours.
- **Where the eye goes.** van der Heijden, "Better Games: Insights from Eye Tracking", User Experience Magazine 11(1), 2012 (reached, https://oldmagazine.uxpa.org/?p=98): racing players watched the screen's middle and missed buttons at the edges; small HUD arrows were not looked at; subtle light cues helped players find an exit in a dark level. So detail at the screen's centre and along the walking line pays; detail at the edges and up high pays less.

## By area

Each entry: source; what it does for the player; cost (E); LEDGER has; recommendation.

### Lighting and grading

**1. Colour grading as one authored look.**
- Source: Epic, "Using Lookup Tables for Color Grading" (reached, https://dev.epicgames.com/documentation/unreal-engine/using-lookup-tables-for-color-grading-in-unreal-engine). A 256 by 16 neutral table, graded in an image editor and set in a Post Process Volume. Epic's caveat: the table works after tone mapping, in low range, and does not adapt to HDR; Epic recommends its built-in Color Grading controls instead, with a table only for a quick look. Izzy Gramp, "LUTious Color: Grading for Games", GDC 2019 (reached: description only, https://gdcvault.com/play/1026004/LUTious-Color-Grading-for): consistency of the look across levels, and fixing bad tables.
- Player: the single biggest "this is a film, not a tech demo" signal. One palette ties mismatched assets together.
- Cost (E): 6 to 10 hours for day, dusk, night and interior grades on Quay Street, with before and after frames.
- LEDGER has: not found. unreal-look.json tunes exposure, fog and surfaces; no grade, table or saturation and contrast settings found.
- Recommend: adopt. Use the Color Grading controls (shadows, midtones, highlights), one set per hour of day; a table only to sketch. Judge against the Hook sheet and period photographs of British port towns, 1988 to 1992.

**2. Fog and atmosphere for depth.**
- Source: Epic, "Local Fog Volumes", 5.9 page (reached, https://dev.epicgames.com/documentation/unreal-engine/local-fog-volumes-in-unreal-engine): placeable spheres of fog, culled per screen tile, costed like dynamic lights, on all platforms; no volumetric shadowing unless Volumetric Fog is on. Valve's Source 2 lighting page (reached, https://developer.valvesoftware.com/wiki/Source_2/Docs/Level_Design/Lighting): volumetric fog makes "shafts of light coming through windows" a focal point; dim fill and bright key lights build contrast.
- Player: distance falls away softly, which hides the edge of a small set and reads as scale. Mist round a lamp or over the harbour reads as weather and place.
- Cost (E): 3 to 6 hours for harbour mist and lamp haloes, checked on the frame-time path.
- LEDGER has: height fog tuned in unreal-look.json (fog_height_falloff, fog_cap_gain_day; "the far end's depth", 23 September). Study 5 line 54: night fog is a gain of 0.2, not a density. Local fog volumes: not found.
- Recommend: adopt local fog volumes for the quay end and two or three lamp haloes. Check the 5.8 page first.

**3. Wet surfaces and night reflections.**
- Source: Arti Sergeev, "Building Streets in the Rain with UE4", 80 Level, 17 July 2018 (reached, https://80.lv/articles/tutorial-building-streets-in-the-rain-with-ue4): a wet version of the paving material, a 16-frame ripple flipbook, a box reflection capture, height fog. Cliff Chen, CGMA (undated; reached, https://cgmasteracademy.com/blog/how-to-use-impactful-decals-in-a-modular-environment-sanxia-street): puddles as decals with adjustable edge falloff.
- Player: wet stone under lamps is the cheapest "expensive night" frame there is.
- Cost (E): 4 to 8 hours for ripples in puddles and a rain-on-or-off switch on what exists.
- LEDGER has: largely. Study 5 lines 28 to 30 and 69; unreal-look.json wet floor notes (3 October) and ground coat (29 October). Puddles were set aside on 8 October (Study 5 table).
- Recommend: keep what exists. Add only rain ripples in low spots once puddles return. Not top ten.

**4. Lumen settings that matter.**
- Source: Epic, "Lumen Performance Guide", 5.9 page (reached, https://dev.epicgames.com/documentation/unreal-engine/lumen-performance-guide-for-unreal-engine?lang=en-US): High scalability targets 60 fps; software ray tracing is the fastest and the fallback for games that cannot afford hardware tracing; Max Roughness To Trace in the Post Process Volume limits which surfaces get traced reflections; reflections can run at half resolution. The page says nothing about night scenes or emissive lights.
- Player: none directly; the saving pays for the grade and fog above.
- Cost (E): 2 to 4 hours to try Max Roughness To Trace and half-resolution reflections against the frame-time path.
- LEDGER has: Study 5 line 55 and table: Lumen front layer plus per-window captures; frame-headroom/CARD-TIME-2026-10-23.md.
- Recommend: one short trial of the two settings named; keep only if the wet road still reads. Not top ten.

### Sound

**5. Layered beds, density layers and spot sounds.**
- Source: Scott Morgan (Radical Entertainment), "Dynamic Game Audio Ambience: Bringing Prototype's New York City to Life", Game Developer, 4 June 2009 (reached, https://www.gamedeveloper.com/audio/dynamic-game-audio-ambience-bringing-i-prototype-i-s-new-york-city-to-life): beds in the background; crowd and traffic layers that fade in with the number of people and cars near; single spot sounds in front, each with a voice limit; crossfades by position, not trigger; distant crowds filtered so they read as populated but far.
- Player: a street that sounds busy past the edge of what is built. Sound sells the town beyond the set.
- Cost (E): covered by Study 8's plan; the new part, crowd layers tied to the simulation's head count, 4 to 6 hours.
- LEDGER has: Study 8 line 5 and line 53 (three-part street adopted), plan table lines 65 to 80. Density-driven layers: not found.
- Recommend: build Study 8's plan as written, and tie the distant voices layer's level to how many people the town simulation has near. Top ten (with item 6).

**6. Reverb by space.**
- Source: Epic, "Audio Volumes", 5.8 page (reached, https://dev.epicgames.com/documentation/unreal-engine/audio-volumes-in-unreal-engine): reverb asset per volume, its level, a fade time on entering and leaving, priority where volumes overlap.
- Player: a step through a shop door that changes the sound is felt more than seen; rooms read as real rooms.
- Cost (E): 4 to 6 hours for street, doorway, shop and office.
- LEDGER has: Study 8 line 19 (echo: none) and line 57 (adopt echo zones, checked against 5.8 first). Not built.
- Recommend: adopt now; the 5.8 page is confirmed today.

**7. Footsteps by surface.**
- Source: Study 8 line 17 and line 56 hold the reference numbers already. No new source needed.
- Player: steps that change from paving to wood to wet stone.
- Cost (E): 3 to 5 hours to wire the five built surfaces and the wet layer.
- LEDGER has: in game, 16 steps on paving; 5 surfaces built (Study 8 line 17). Others' footsteps: lacks (line 80).
- Recommend: wire the built surfaces; not top ten on its own because it is already planned.

### Animation

**8. Look-at and head tracking.**
- Source: Epic, "Animation Blueprint Head Look At", 5.9 page (reached, https://dev.epicgames.com/documentation/unreal-engine/animation-blueprint-head-look-at-in-unreal-engine): clamp angles and an eased interpolation time. CD Projekt's dialogue generator, Piotr Tomsinski at GDC 2016, reported by PC Gamer, 19 March 2016 (reached, https://www.pcgamer.com/most-of-the-witcher-3s-dialogue-scenes-was-animated-by-an-algorithm): look-ats used attached poses, so a character might lean on one arm when looking; gestures were additive so they worked sitting or standing; the generator gave a base for all 1,463 dialogues.
- Player: people who notice Tom read as alive more than any other single cue.
- Cost (E): 2 to 4 hours to add eased interpolation and an occasional glance at passers-by, if missing.
- LEDGER has: yes. ue-probe PersonAnim.cpp lines 67 to 101: a Look At node on the head, clamp 60. Study 7 line 100: turn and look planned.
- Recommend: keep; check the turn eases in (not snaps) and add a body lean pose for long looks, Witcher style. Not top ten.

**9. Additive breathing and idle breaks.**
- Source: the Witcher 3 report above (additive gestures over any pose).
- Player: a still person who breathes and shifts weight never reads as a mannequin.
- Cost (E): 2 to 3 hours.
- LEDGER has: partly. PersonAnim.cpp line 39 and 119: an additive "break" layer over the idle. A breathing layer: not found.
- Recommend: add a slow chest and shoulder additive under every idle, varied per person. Small, cheap; folded into top ten item 4.

**10. Procedural foot placement.**
- Source: Study 7 lines 32 to 45 (Epic's Foot Placement node, For Honor's limits). Epic's Foot Placement API pages: snippet only.
- Player: no sliding or floating feet; failures are seen at once.
- Cost (E): open work already in the walk item.
- LEDGER has: yes, as active work (Study 7 lines 74 to 80).
- Recommend: no new action here.

**11. Short reaction animations.**
- Source: Epic, "Physics Driven Animation", 5.9 page (reached, https://dev.epicgames.com/documentation/unreal-engine/physics-driven-animation-in-unreal-engine): turn on simulation from the touched bone, ramp the physics blend up and back to zero; a hit reaction on top of the playing animation.
- Player: a shoulder that gives when Tom brushes past, a flinch at a shout. Small responses make the world feel solid and watched.
- Cost (E): 6 to 10 hours for a bump and a flinch on street people, with the startle and turn-and-look clips.
- LEDGER has: startle and turn-and-look listed (Study 7 lines 100 to 101). Physics bump: not found.
- Recommend: adopt the physics blend for bumps; it needs no new clips. Top ten.

### Camera

**12. Subtle handheld motion.**
- Source: Study 9 line 29 already records a rotation-only shake that grows with speed and is near nothing standing still. John Nesky (thatgamecompany), "50 Game Camera Mistakes", GDC 2014, reported by Game Developer 17 November 2015 (reached: the article names no single mistake; the list itself was not read). EXOR Studios, 15 May 2026 (reached, https://www.exorstudios.com/blog/rb-details): shake on a 0 to 100% slider because too much causes motion sickness.
- Player: a camera that breathes reads as filmed rather than computed.
- Cost (E): 2 to 3 hours.
- LEDGER has: not built (Study 9 table: lag none; line 68: shake goes under Reduce motion).
- Recommend: adopt with a strength slider and Reduce motion off-switch. Top ten.

**13. Field of view and depth of field.**
- Source: Study 9 line 11 (82 degrees proposed). Epic, "Depth of Field", 5.8 page (reached, https://dev.epicgames.com/documentation/unreal-engine/depth-of-field-in-unreal-engine): a cinematic method for desktop; no gameplay advice. Daedalic's camera post on Epic's blog (reached, undated, https://www.unrealengine.com/tech-blog/six-ingredients-for-a-dynamic-third-person-camera): depth of field changed in combat only, camera volumes with transition times.
- Player: a narrower lens and a soft background in talk shots read as film.
- Cost (E): 2 to 4 hours for depth of field in the talk camera only.
- LEDGER has: the lens is on his page route (Study 9 lines 11 and 62). Depth of field in talk: not found in specs (mentions exist in talk-protocol.md; not checked in detail).
- Recommend: talk shots only, with the 63 degree talk lens; never while walking.

### Set dressing

**14. Decals, grime and wear masks.**
- Source: Cliff Chen, CGMA (above): cracks, water stains, story posters and shop text decals make identical modular blocks read as different places; trim sheets avoid big cracks or stains because repetition shows.
- Player: wear is the difference between a level and a place. It hides repeated kit pieces.
- Cost (E): 10 to 16 hours to dress Quay Street to Study 5's mix and densest along the walking line.
- LEDGER has: partly. street-wear.json; Study 5 lines 32 to 35 and 70; vignette-scene.json line 709 holds imperfection masks "deliberately not scattered" yet.
- Recommend: adopt; place leak stains, base grime and posters (1990, no real brands, no drink or betting adverts) along the first walk. Top ten.

**15. Clutter rules.**
- Source: Study 4 line 18 (props per 10 m) already sets the count.
- Player: lived-in streets.
- Cost (E): inside item 14.
- LEDGER has: Study 4; vignette-pieces.json (dock clutter, litter).
- Recommend: no new rule; follow Study 4's count.

**16. The first 30 minutes polished hardest.**
- Source: the CHI PLAY 2014 paper and Bycer's data above; Naughty Dog's polish talk (description only).
- Player: the first impression sets the reviews and whether he keeps playing.
- Cost (E): 4 hours to map the first 30 minutes' route and its view lines, then each polish item above is done there first.
- LEDGER has: Study 2 measures the opening (lines 60 to 74). A rule to polish there first: not found.
- Recommend: adopt as an ordering rule for every item on this page. Top ten.

### Crowds and life

**17. Impostors and crowd levels of detail.**
- Source: Francois Cournoyer (Ubisoft), "Massive Crowd on Assassin's Creed Unity: AI Recycling", GDC 2015 (reached: description only, https://www.gdcvault.com/play/1022141/Massive-Crowd-on-Assassin-s): 40 full AIs, 120 high-detail models, about 10,000 crowd people, swapping low and high detail unseen. Epic, "Create MetaHuman Crowds", 5.8, Experimental (reached, https://dev.epicgames.com/documentation/metahuman/create-metahuman-crowds-in-unreal-engine): full MetaHumans near, baked GPU-animated instanced meshes at middle range, none far; timing variety to avoid lockstep.
- Player: a busy town beyond the near street.
- Cost (E): 25 to 40 hours; Experimental in 5.8.
- LEDGER has: Study 7 line 109: ignore for now, until phase 5's town.
- Recommend: keep deferred. Not top ten.

**18. Ambient vignettes.**
- Source: Espen Sogn (Guerrilla), GDC 2023, reported by Game Developer, 20 March 2023 (reached, https://gamedeveloper.com/gdc2023/adding-texture-to-the-people-and-places-of-horizon-forbidden-west): long looping work (painting a wall end to end, then turning back) so people look busy without finishing; props that move between two states with long pauses (a crate from table to floor and back later); behaviour that hints at a past without explaining it. PC Gamer on Red Dead Redemption 2, 17 November 2020 (reached, https://pcgamer.com/red-dead-redemption-2-npcs-lead-interesting-lives): small routines make the world "a real place" rather than "a beautiful painting".
- Player: the street has things going on that are not about Tom.
- Cost (E): 12 to 20 hours for six vignettes on Quay Street (sweeping, a shopkeeper restocking, a delivery, two people talking at a door, someone at the phone box, a smoker).
- LEDGER has: Study 7 lines 87 to 106 list the actions. The long-loop and two-state prop tricks: not found.
- Recommend: adopt the two tricks; they multiply what each clip gives. Top ten.

**19. Birds and litter.**
- Source: Drop Bear Bytes, "Breathing Life Into Our Environments", 12 February 2021 (reached, https://www.brokenroadsgame.com/dev-blog/breathing-life-into-our-environments): insects that scatter when disturbed, moths at lamps, wind in cloth and strings, dust and mist on wind. Bill Rockenbeck (Sucker Punch), "Blowing from the West: Simulating Wind in Ghost of Tsushima", GDC 2021 (reached through GDC's news page, https://gdconf.com/news/see-how-ghost-tsushima's-guiding-wind-came-life-gdc-2021): wind replaced the map arrow.
- Player: pigeons that lift as Tom walks through, gulls overhead, a sheet of newspaper on the wind. Motion at the edge of vision reads as life.
- Cost (E): 8 to 12 hours for a pigeon group that scatters, gulls, moths at lamps, and blown paper.
- LEDGER has: litter placed still (vignette-scene.json line 721, G8). Study 4 line 65: weather dressing, none in Quay Street. Gulls in sound only (Study 8).
- Recommend: adopt. Top ten.

### Interface and feedback

**20. Sound on every interaction, and eased transitions.**
- Source: Joseph Marchuk, "Approaching UI Audio from a UI Design Perspective", Audiokinetic blog, 2019 (reached, https://www.audiokinetic.com/en/blog/approaching-ui-audio-ui-design-perspective-1): similar functions get similar sounds; important cues stand out; nothing extra. Martin Jonasson and Petri Purho, "Juice It or Lose It" (GDC Vault page snippet only; a 2024 blog about it reached, https://roblog.co.uk/2024/03/juicy-games/, but it lists no techniques).
- Player: every press answered; menus that slide and fade rather than cut read as finished.
- Cost (E): 6 to 10 hours for a small set (open, close, select, confirm, refuse, page turn of the ledger) and eased fades.
- LEDGER has: Study 10 line 77: subtitle fade 0.2 s. Interface sounds: not found.
- Recommend: adopt, in period: paper, pencil and ledger sounds rather than digital beeps. Top ten.

## Ranked top ten for LEDGER

Ranked by impression gained per hour, for what LEDGER does not yet have. All hours are estimates.

| Rank | Technique | Hours (E) | Why first |
|---|---|---|---|
| 1 | Polish the first 30 minutes' route first (item 16) | 4, then an ordering rule | Makes every other hour count where players decide to stay |
| 2 | Colour grade per hour of day (item 1) | 6 to 10 | Biggest change to every frame; nothing exists yet |
| 3 | Wear decals and grime along the walking line (item 14) | 10 to 16 | Masks are held but not scattered; hides kit repetition |
| 4 | Reverb by space plus density-tied street beds (items 5, 6) | 8 to 12 | Sound is cheap and LEDGER has no echo |
| 5 | Interface sounds and eased transitions (item 20) | 6 to 10 | Touched constantly; nothing found |
| 6 | Ambient vignettes with long loops and two-state props (item 18) | 12 to 20 | Life without many clips |
| 7 | Birds and blown litter (item 19) | 8 to 12 | Motion at the edges of the frame |
| 8 | Reactions: physics bump, flinch, breathing additive (items 9, 11) | 8 to 13 | People who respond to Tom |
| 9 | Handheld camera sway with a slider (item 12) | 2 to 3 | Cheapest change of feel |
| 10 | Local fog volumes at the quay and lamps (item 2) | 3 to 6 | Depth and weather at night |

Total, rough: about 67 to 106 hours (E).

## Decisions for Jafar

Only canon, scope and money questions go to him. Recommendation marked.

1. **The look.** A: one colour grade per hour of day on Quay Street, shown to him as before and after frames (recommended). B: no grade until more art is in.
2. **The camera's sway.** A: a slight walking sway on by default, with a strength slider and off under Reduce motion (recommended). B: a still camera.
3. **Where polish goes first.** A: the first 30 minutes' route and what sits at the screen's centre, then outward (recommended). B: the whole street evenly.

Sessions decide the rest within canon and his rulings, recorded in DECISIONS.md: the reverb volumes, interface sounds, decals, vignettes, birds, reactions and fog volumes. Crowd impostors stay deferred as Study 7 says.

Content notes: posters and vignettes stay inside canon's rule: no drink or betting adverts, no children, smoking allowed; no real brands (licence allowlist, Never ship 5).

## Licences

No new tool is needed. Every technique uses Unreal 5.8's own features (post process, local fog volumes, audio volumes, physics blend, look-at, Niagara). Decal and sound sources must come from the allowlist: CC0 libraries (Poly Haven, ambientCG), Fab under its Standard Licence not marked NoAI (Epic's own Megascans excepted), and CC0 sound under D26. The MetaHuman crowd tool is Epic's and Unreal-only; it is Experimental, so not recommended now.

## Weak points

- GDC Vault pages gave descriptions only (Asobo, Naughty Dog, Ubisoft, LUTious); the talks were not watched. "Juice It or Lose It" and Nesky's 50 camera mistakes were not read in substance.
- Epic pages fetched are 5.9 for Lumen, look-at, local fog and physics animation; check each in 5.8.2.
- All hours are estimates, not from any LEDGER clock.
- Snippet only, not used as evidence: Epic's Foot Placement API pages, The Last of Us Part II sound articles, Ninja Theory's small-team article.
