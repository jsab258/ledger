# SOUND-PLAN: how the game sounds, as standards a checker can test

Blueprint preparation item (d), 23 Nov 2026, blueprint preparation session (Opus 5.5). For the browser game the one-shot builds, written so the same standards carry to the Unreal game. Each standard has an id (SND-nn), the rule, and how it is tested: A means an automatic check through the game's test door (`LEDGER.mix()`, TECH-PLAN section 8), E means by ear (a sound-only listening test with the picture off, then his ear on his PC as usual).

Inputs from the project: ONE-SHOT-PROMPT.md section 8 (reaches, three parts, four hour states, footsteps by surface and gait) and section 6 (the sound shown assist), BLUEPRINT-05 sections 5.5.1 to 5.5.7 (CC0 only for effects, rule D26; car note 28 to 210 Hz; fight layers and timings; the mix and sliders), canon.md (no real brands or bands, all fictional; no alcohol, gambling or children, in sound too), the licence allowlist (item 5 music; NEVER SHIP item 5: real brands, lyrics, cloned real voices), and the prototype's audio.js as counted on 23 Nov.

Built on (PRIOR-RESEARCH-INDEX.md, read 23 Nov; files on wip): production/cloud-week/sound (12 to 13 Oct: 97 sound files already built from 46 CC0 recordings, 21 loops, 40 footsteps and 36 one-shots, with a loudness plan: beds at -36.5 LUFS by day, -39.5 at night, -33.5 in rain, 13.5 LU under a -23 target; judgement figures, nobody has heard them in the game; known short: no clean setts recording, one rain intensity, sources mostly not British); research/footsteps (30 Sep: Tom's walk and run from two CC0 recordings); production/specs/street-sounds.json (the first street wiring: traffic falloff 70 m, voices 1.5 to 16 m, a line every 18 to 40 s); production/cloud-week/lines/rules.json (hearing radius for a spoken line 7 m dry, 6 drizzle, 5 rain, 4 hushed; witnesses quieter for an hour). None of these figures is measured against a reference; all are leads until the listening pass (MEASUREMENTS-NEEDED A7) and, for any footage figure, until STATUS.md marks it solid (advisor 302).

## 1. What the published work of the four teams tells us

Research done 23 Nov from web search and fetched articles and slides only (no videos). What was found, and what was not:

GTA V (Rockstar North), from the GDC 2014 talk "The Sound of Grand Theft Auto V" by Alastair MacGregor, lead audio programmer (slide text: https://gta.com.ua/img/news/sound-of-gta5-gdc2014.pdf ; abstract: https://www.gdcvault.com/play/1021165/The-Sound-of-Grand-Theft ; Japanese coverage: https://www.gamespark.jp/article/2014/04/08/47678.html , 8 Apr 2014) and an Audio Technology feature with Will Morton and Craig Conner (https://audiotechnology.com/?p=72897):
- The world is covered by authored ambience zones and rules, not one loop: 949 zones, 1,210 rules and 518 static emitters, against 86, 57 and 198 in GTA IV.
- Traffic is heard in close, mid and far layers plus distant one-shots and a city bed.
- Engines: granular playback, with intake, transmission and other parts made by synthesis; engine and exhaust are separate parts; parts are shared across vehicles; distance changes the sound, and details such as an engine cooling down are included.
- About 1,000 sounds are tracked at once and 96 are actually played, chosen by loudness, distance and priority (Conner).
- Mixing uses named scenes that change groups of sounds together; voices route to sub-mixes.
- Sounds for things a player cannot interact with are left out (GTA IV had no dogs, so no barks).
- About 150,000 lines of dialogue; a passer-by's script averages about 200 lines (Morton).
- Radio is processed differently from the score so the two never blur; the score is 8 stems mixed by mood.

Red Dead Redemption (Rockstar San Diego, the 2010 game; nothing comparable was found for RDR2's sound team) from Designing Sound's interview with audio director Jeffrey Whitcher (https://designingsound.org/2010/08/20/red-dead-redemption-exclusive-interview-with-audio-director-jeffrey-whitcher/ , 20 Aug 2010):
- Each region has its own ambience, split into sub-areas; birds, insects and animals are adjusted for weather and time of day, and the creatures heard set the mood.
- The mix adapts at run time so music never masks speech and important sounds are not lost; it was tuned on a television first, then on monitors.
- Thousands of foley sounds were recorded in a week-long session; thousands of animations were tagged with sounds.
For RDR2 itself, the only published audio detail reached was the score (Mix, with composer Woody Jackson and Rockstar's music director Ivan Pavlovich, https://www.mixonline.com/?p=2091 ): three kinds of score, narrative, environmental (people playing music in the world) and interactive (reacting to play), and "we've gone from eight stems to 15". A Guardian reprint (https://inkl.com/news/get-real-behind-the-scenes-of-red-dead-redemption-2-the-most-realistic-video-game-ever-made ) records that a lifelike tree took people "to record and mix its rustling", but gives no method.

Kingdom Come: Deliverance 2 (Warhorse), from GamesRadar with audio director Vojtech Nedved and composer Jan Valta (https://www.gamesradar.com/games/rpg/we-were-having-so-much-fun-trying-not-to-overdo-it-kingdom-come-deliverance-2-devs-talk-us-through-the-medieval-spice-that-brought-the-rpgs-sound-to-life ), PC Games on KCD1 (https://www.pcgames.de/Kingdom-Come-Deliverance-Spiel-16151/Specials/Kingdom-Come-Deliverance-Interview-Special-Teil-4-Soundeffekte-Musik-und-Klangbild-1156355/ , 17 Apr 2015) and Wccftech with Martin Klima (https://wccftech.com/kingdom-come-deliverance-2-qa-half-of-the-voiced-lines-arent-related-to-the-story-at-all/amp/ ):
- Recorded mostly by the team itself (foley preferred to libraries; Nedved oversaw 95% of recordings); pitch variation used to make crowds, rain and birdsong feel spread in space.
- Period music only where it is played in the world; on silence Valta says "The second best tool you can have is that it ends, and it doesn't play anymore"; "a hierarchy for music and a hierarchy for silence" (Adam Sporka, KCD1).
- KCD1, from PC Games' 2015 demo: when an ambush comes the ambience recedes within seconds, gradually (the same passage has the music turning dramatic; LEDGER keeps the ambience falling back and has no combat music).
- Almost half the voiced lines are not story lines but reactions (to theft, trespass, a body found); greetings to passers-by come separately, through a chat system.

GTA VI: Rockstar has published nothing on its sound technology that this research reached (a third-party summary says the same: https://gtaintel.com/news/gta-6-audio-and-3d-sound ). Nothing from GTA VI is used as a standard here. No story details are included.

Not found anywhere reached: footsteps split by gait or surface counts, occlusion and reverb values, ducking amounts, any of the four studios' loudness targets, memory budgets. Where a standard below needs such a number, it comes from a published general standard or from our own design, and says so.

General standards used: game loudness of -23 LUFS average over at least 30 minutes, plus or minus 2 LU (Sony's Garry Taylor, Designing Sound, 30 Jul 2012: https://designingsound.org/2012/07/30/video-games-and-loudness-standards-interview-with-sonys-garry-taylor/ ); -24 LUFS plus or minus 2 LU and true peak at most -1 dBTP for console (IESD Mix Reference Levels v03.02: https://www.audiogang.org/wp-content/uploads/2015/04/IESD-Mix-Ref-Levels-v03.02.pdf ). Neither covers PC, which has no platform rule; the plan takes -23 LUFS.

## 2. What the browser prototype does now (counted 23 Nov)

All sound is made in the page by Web Audio synthesis; there are no sound files. Nodes used: oscillators, a 3 s noise buffer, filters, gains and one convolver reverb (2.6 s made from noise). No panner: nothing is placed left or right or in 3D. Buses: master, street bed (filtered by inside, street, cab), effects, "world" (sounds that carry, louder or softer by the hour and rain), music, reverb return. Loops: rain, sea (louder near the quay), a town hum (louder at night), the cab's engine (a sawtooth whose pitch follows speed). Scheduled: gulls, a ship's horn every 55 to 140 s, radio chatter in the office or cab, a soft generated score. 17 named effects (tick, paper, stamp, coin, cloth, ferry horn, stair, door, car door, shout, thud, hit, block, crash, face, radio, step) and chimes. Speech is a short run of tones per line. Footsteps are one noise burst a step whose filter moves from 900 to 1,500 Hz when the ground is wet and whose rate follows run, walk and slow walk; there is no surface or shoe and no left and right. No voice limit. The `LOUD` table and `heard()` log the asked-for loudness of effects and voices only to a mix record; the loops, gulls, horn, timed radio and score are not logged. That record is the start of `LEDGER.mix()`.

What the browser can do without files: everything in this plan except recorded texture. With files: the 97 cloud-week files can be played in the browser as compressed loops and one-shots (as built they are 48 kHz WAVs; compressed to Ogg or Opus they shrink about tenfold, to be checked against the published page's size limit of 16 MB a file), which gives real recorded texture for the beds, footsteps and doors at once. The plan is both: recorded files for beds, footsteps and doors where they exist, synthesis for the engine (its pitch must follow the car) and for anything the files lack. Web Audio has 3D panners (HRTF for near sounds, a cheaper model for far ones), convolution reverb, filters and compressors, and runs offline for tests. The one budget to respect is how many sounds play at once (section 3, SND-03).

## 3. The standards

Street ambience by hour and weather

- SND-01 Three parts. The street is a bed (quiet loops), one-shots spawned around the listener and capped by place and hour, and placed sources each heard within its own distance (ONE-SHOT-PROMPT s8). Test A: `LEDGER.mix()` at 10 sample moments shows sounds from all three parts in the street by day, and no placed source playing beyond its distance.
- SND-02 Four states of the hour, three weathers (the four states and their hours are our design; the sources name none). Starting levels: the cloud-week loudness plan (beds -36.5 LUFS day, -39.5 night, -33.5 rain; judgement, to be heard), and spoken lines heard within 7 m dry, 6 in drizzle, 5 in rain, 4 when the street is hushed (lines/rules.json). States: early (05:30 to 08:00), day (08:00 to 18:00), evening (18:00 to 23:00), small hours (23:00 to 05:30); weathers dry overcast, drizzle, rain. Each of the 12 combinations is a named mix of the bed, the one-shot caps and the reach multiplier. One-shot caps on a quiet street: day at most 3 far voices and 3 activity sounds, the small hours none (BLUEPRINT-05 5.5.3); early and evening at most 2 and 2 (our design). In the small hours every reach is doubled. Rain cuts every reach (the rule's own value) and halves the far voices allowed. Test A: one sample per combination at the same place; one-shot counts within caps, reach values as set; E: a listener with the picture off names the hour state right 8 times in 10.
- SND-03 A limit on sounds at once, like Rockstar's 96 of 1,000. At most 40 sounds play at once in the browser (24 on the low setting; both our design, no source); more are tracked but silent, chosen by loudness at the listener, distance and a priority (voices and Tom's own noises first). Test A: in the busiest view (Quay Street's busy band, 20 people, dry; and the Saturday match crowd) `LEDGER.mix()` never lists more than 40 playing, and a voice line in earshot is never the one dropped.
- SND-04 Only what can matter makes noise. Every placed source belongs to something in the world the player could see or reach (the GTA rule: no barks without dogs). Test A: each placed source names its owner (person, door, car, animal, machine); none without one.

Footsteps by surface and gait

- SND-05 Surfaces (the count is our design). At least 7: setts and cobbles, flagstone pavement, tarmac, wet ground with puddles, wooden decking and stairs, iron plates and gratings on the docks, indoor boards and lino. The surface comes from the ground under the foot (map zones). Test A: walking Tom across each surface gives a different footstep name in the mix.
- SND-06 Gaits and shoes. Walk, run and slow walk for Tom (there is no crouch, ONE-SHOT-PROMPT s6); walk and run for others; at least three shoe kinds (Tom's shoes, women's heels, work boots). Left and right feet alternate and differ slightly; no two steps in a row identical (pitch and level vary a little). Test E: with the picture off a listener tells a walk from a run 9 times in 10 and Tom's steps from a passer-by's 8 times in 10 (ONE-SHOT-PROMPT s8).
- SND-07 Steps carry as the rule hears them. Tom's step is as loud as its reach: about 3.6 m at three in the morning, nothing heard at noon; the player hears what the town's rule hears at the same strength. The table from reach to level is one function kept with the noise rule (today audio.js uses loudness = reach in metres divided by 10). Test A: at 03:00 the step's level matches that function within 1 dB; at noon the step is not played or is below -60 dBFS.

Cars (1990, automatic)

- SND-08 Engine. Layered like GTA V's: an engine note from about 28 Hz at idle to about 210 Hz at the limit (a small four-cylinder, 800 to 900 rpm idle, 6,000 to 6,500 limit, BLUEPRINT-05 5.5.5), exhaust as a separate layer, tyres on dry and wet road, wind from speed. Test A: the note's frequency tracks the engine speed within 5% over a drive.
- SND-09 Automatic gearbox. Gear changes are short soft dips in the note, never a clutch or a manual crunch; a 1990 three- or four-speed automatic changes up two or three times between rest and 50 mph (our design, no source). Test A: the engine note falls at each change with no gap in the sound; E: no listener hears a manual change.
- SND-10 Reaches. The car is heard within about 44 m by day and further at night; the horn about 60 m by day; tyre squeal begins at about 80% of grip as the warning. Test A: reach values in the mix match the table.
- SND-11 The 1990 street. Traffic is close, mid and far layers plus passing cars placed in 3D. The patrol car's siren is a two-tone horn of the period, used only in a chase, and fictional in make. No modern sounds (no keyless-lock chirps, no reversing beepers on cars, no mobile phone ringtones). Test E: a listener lists nothing out of period; A: the siren plays only in a chase state.

Crowds

- SND-12 Walla by density. The crowd's murmur follows how many people are near (our bands, sized to the rescaled G9 counts of BLUEPRINT-02): none under 3, a thin murmur at 3 to 11, a full murmur at 12 or more. Murmur is wordless; words come only from people's own lines. Test A: murmur level rises with people within 20 m.
- SND-13 A street that noticed him goes quiet. When people near have seen a deed, the murmur drops and the one-shots stop for about a game hour (the length is our design), the strongest sound cue the design has (ONE-SHOT-PROMPT s6). Test A: after a seen deed the bed and one-shots fall by at least 6 dB in that street; E: a listener with the picture off tells a noticed street from a calm one 8 times in 10.
- SND-14 Reactions are the town's voice. As KCD2 found (half its lines are reactions), people's short lines react to what they see; the line tables of INVENTORY.md carry them. Test A: every reaction situation has lines for at least 6 speaker kinds.

The docks

- SND-15 Working waterfront. A docks bed (water at the quay, ropes and fenders creaking, distant ship engines), placed sources (gulls thick on the fish dock by day, 5 to 20 birds, P45; winches and a crane; fish boxes; the cold store's plant hum; the tea stall at the gate at night), and the ship's horn, heard across the Hook. Gulls stop at night and indoors. Test A: at the fish dock by day gulls are in the mix, at night not; E: a listener knows the docks from Quay Street by sound alone 9 times in 10.

Interiors

- SND-16 Rooms change the echo at the doorway. Each kind of room has its own short reverb (office, caff, launderette, chapel, shop, flat, hut, back room); at the doorway the street bed fades and the room's reverb crossfades in over about 1 m of walking, never a jump (BLUEPRINT-05 5.5.4 found the prototype has a reverb inside but no change at doorways). One reverb is shared and swapped, not one per room. Test A: crossing a door, the reverb's wet level changes over at least 0.5 s; E: no audible jump.
- SND-17 Room tones. Every enterable room has its own quiet tone (the office radio, the launderette machines, the chapel's stillness, the caff's urn and plates) at least 10 dB under speech. Test A: each room lists its tone in the mix, and during a spoken line in that room the tone is at least 10 dB under the voice.
- SND-18 Doors tell the street. Doors creak, hit and latch; a forced door or broken glass is the loudest thing in a quiet street, heard at its force reach (ONE-SHOT-PROMPT s8). Test A: forced door's reach equals the force reach; it is the loudest one-shot in the street's mix at that moment.

Fights and guns

- SND-19 Blows in four layers with set timings: the whoosh from 0.05 s before to 0.10 s after the blow starts, the impact within 0.034 s of contact, the pain cry 0.05 to 0.30 s after, an attacker's shout at least 0.40 s before his blow lands; never combat music (BLUEPRINT-05 5.5.6). Test A: the timings read from the mix record against the fight's own events.
- SND-20 Shots. A shot is heard about 177 m by day and further at night, with an echo off the warehouses and the quay walls (Game*Spark's coverage of the GTA V talk: gunshots echo off tall buildings); after a shot the street goes silent (SND-13) and birds lift. Guns are rare and late (his ruling), so this sound is rare. Test A: reach equals the table; the after-shot quiet applies.

Music

- SND-21 Music only where it plays in the world. No music in the cab and no score under play (DEFINITIONS P09): the caff's radio, a record through a window, the chapel organ, the boxing club's radio, a busker's tune (the busker is our addition). Our rule (BLUEPRINT-05 5.5.7): silence is the commonest music; compare Valta and Sporka above. Test A: no music in the mix unless a world source is within its distance.
- SND-22 Music is made for the game. Every tune and every band is fictional (canon); tunes are made with an allowlisted tool, as item 5 reads: "self-hosted MusicGen (MIT) or Stable Audio Open; ElevenLabs Music if adopted. Final pick re-verified when radio production starts" (the allowlist's header: verify the weights licence, not the code licence), or played by synthesis in the browser; never a real song, a real band's name or real lyrics (NEVER SHIP item 5). Radio speech is fictional presenters, made like any other voice. This is settled by the allowlist, so it is no question for Jafar. Test A: every music file or recipe carries its tool and licence line; the content check finds no real band names.
- SND-23 Radio sounds like a radio. Following GTA V (radio processed apart from the score), any world music passes through a small-speaker filter (no deep bass, no sparkle), its level falling with distance and walls. Test A: world music always has its speaker filter.

The mix

- SND-24 Speech first. Talk lowers the beds; the quietest lead voice sets the mix; a line a player needs is never masked (the RDR rule: the mix adapts so music never masks speech). Sliders: master, voices, effects, street, music; a "voices clear" switch lifts voices 6 dB over the street; a "loud noise softening" switch caps gunshots at a door slam's level (BLUEPRINT-05 5.5.7). Test A: during a spoken line the bed is at least 6 dB under the voice.
- SND-25 Loudness. Measured over 30 minutes of ordinary play: -23 LUFS integrated, plus or minus 2 LU; true peak at most -1 dBTP; the loudest single sound (a shot near), as momentary loudness over 400 ms, at most 20 LU above the long-term level. Test A: a 30-minute recording from the page's output (a tap on the master bus) measured to ITU-R BS.1770 by the checker; whether headless Chrome renders audio for this is not yet tried, so the first run is on his PC by the usual route.
- SND-26 Sound shown. With the assist on, a short word at the screen's edge for Tom's loud noises, a street gone quiet, a shout or a car heard; it shows what Tom hears, never what anyone knows (ONE-SHOT-PROMPT s6). Test A: each of the four (a loud noise of Tom's, a street gone quiet, a shout, a car heard) produces its word when the assist is on, none when off.

Effects sources

- SND-27 Effects come from synthesis in the browser or from CC0 sources (rule D26), each with its source line; recorded effects made by the project itself are also allowed. Test A: every sound recipe or file has a source line; none outside CC0, own recordings or allowlisted tools.

## 4. Count of sound kinds the game needs

Used by INVENTORY.md:

| Group | Kinds |
|---|---|
| Beds: 12 hour and weather mixes, docks bed, 8 room tones | 21 |
| Footsteps: 7 surfaces x 3 gaits, plus shoe variants as settings | 21 |
| Cars: engine, exhaust, gear dip, tyres dry and wet, squeal, wind, door, boot, horn, passing car, van, lorry, siren | 14 |
| Crowd: three murmur densities, shouts, calls across a street | 5 |
| Docks: water, ropes, ship engine, ship's horn, gulls, winch, crane, fish boxes, plant hum | 9 |
| Doors and things: creak, latch, slam, forced door, glass, shop bell, till, phone bell, answering machine, kettle, stair, letterbox, bin rattle, thrown stone | 14 |
| Fights and guns: whoosh, impacts (light, heavy, weapon), pain, shout, fall, chair, brick, bin lid, revolver, shotgun, echo | 13 |
| Weather: drizzle, rain light and heavy, rain on the car roof, gutters, wind | 6 |
| Animals: gulls (above), pigeons, cats, a yard dog's bark | 3 |
| World music sources: caff radio, record player, chapel organ, club radio, busker | 5 |
| The town's clocks and the Ledger: chapel bell, office clock, paper, page, stamp, coin, cloth | 7 |
| Total | 118 |

## 5. Order of work for the one-shot

0. Bring in the 97 cloud-week files (compressed), with their source lines, after a content check (no voices through a window saying anything the content rule forbids).
1. Add panners (SND-03 budget with priority) and the `LEDGER.mix()` read (TECH-PLAN 8), logging every loop and timed sound and its level at the listener, not only effects and voices.
2. Beds and states (SND-01, 02), footsteps (SND-05 to 07), doors and rooms (SND-16 to 18): these carry the noise rule, so stories need them.
3. Cars (SND-08 to 11), crowd and quiet (SND-12, 13), docks (SND-15).
4. Fights and guns (SND-19, 20), world music (SND-21 to 23), and remove the prototype's generated score, which SND-21 bans.
5. Mix and loudness (SND-24, 25), sound shown (SND-26).

The recipes for steps 2 to 4 (synthesis settings per sound) are a make-ahead item (INVENTORY section 4, item 7).

## Rulings to revisit

None. No finding here argues against a ruling: music stays fictional and made for the game (canon, allowlist), effects CC0 or our own (D26), and the voices are his PC's Pocket voices (TECH-PLAN section 10).
