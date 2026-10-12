# Quay Street sound: the brief (12 October 2026)

Unit 10 of cloud week 42 (proof P13): the target the sounds are built to and judged against. Its numbers live in section 5's block; `make_sound.py` and `check_sound.py` both read them from here.

## 1. What Quay Street sounds like

A short, steep shop street running down to a harbour in a small British town, 1990, under grey sky. The Hook is the old port: the street ends at the quay, so water, boats and gulls sit at the bottom of the hearing, with the town's main road and the terraces behind. Hard surfaces: stone paving, setts in the gutter, shop glass, iron and timber doors. Nothing is loud: near things (steps, doors, the bell) over a low bed.

Weather is a range (5 October ruling): dry overcast, drizzle, rain; never sun. Rain changes what is heard: the road hisses, the gulls go quiet, windows are shut so voices and the radio sink, and the rain itself comes in three places (pavement, awning, gutter).

Never in any sound (the content rule, canon's era): children's voices or a playground; alcohol or gambling (no pub crowd, glasses, racing commentary); real music, lyrics, a real broadcast, station or brand; anything after 1992 (mobile phones, modern car alarms, electric cars, reversing bleepers); any word that can be understood.

## 2. The layers: day, night, rain

Ambience loops are 75 s, 48 kHz 16-bit WAV, seamless. Beds are stereo; point sources (gulls, voices, radio) and the pavement rain are mono.

| Layer | Day | Night | Rain |
|---|---|---|---|
| Distant traffic | a steady low roar from the main road, single cars and a bus rising and falling; no horn, no siren | long gaps, single cars passing far off, the quiet floor between | the same road with tyre hiss on wet tarmac: a higher, wider, steadier band |
| Gulls | herring gulls over the quay: long calls and runs of "kyow", near and far, about nine in 75 s | one or two calls, a bird passing | two far, dull calls |
| Harbour | water slapping hulls and quay walls, rigging rattling on masts, a small boat's engine far off once | calmer water, few slaps, rigging faint, no engine | duller steady water, rigging whistling in the wind |
| Wind | a gentle wind with gusts down the street | lower, darker, steadier | stronger, gustier, more mid-range |
| Voices through a window | a murmur of adult voices, no words | two adults, very quiet, in gaps | windows shut: barely there |
| A radio through a window | speech in a small speaker's band, no words | quieter | muffled |
| Rain on pavement / awning / gutter | not heard | not heard | steady drops on stone; a patter on canvas; running water and drips from a gutter |

Voices and the radio are recorded adult speech cut into grains of 80 to 160 ms, laid in random order and filtered to what passes glass (nothing above about 1.2 kHz): no word can survive.

## 3. Footsteps (mono one-shots, 8 variants per surface, 80 to 260 ms)

- **Paving**: boots on concrete flags: short, hard, a heel then a toe.
- **Setts**: hard stone: a knock with a little ring, harder than paving. No clean CC0 recording of setts or cobbles exists in the search (NOTES.md); these are steps on stone patio flags and rough old slabs, the nearest found.
- **Asphalt**: duller and finer than paving, a trace of grit.
- **Wet**: damp pavement and puddles: a soft slap, a splash, shorter ring.
- **Wood**: interior boards: a hollow knock and a little room.

## 4. Doors, bell, phone box (mono one-shots)

- **Shop door** (glazed, timber and iron): opening, closing (glass rattling), the latch.
- **House front door** (heavy timber): opening, closing with a thud, key and latch.
- **Shop bell**: a sprung bell on a coil above the door, rung by the door opening: a bright jangle that rings out for one to three seconds.
- **Phone box**: the door's creak and spring, the door shutting (glass and metal), a telephone ringing. No CC0 recording of a British kiosk payphone ringing exists; the ring is a GPO 746 house telephone's bell, a double ring (about 0.4 s, a gap of 0.2 s, 0.4 s), a stand-in to be replaced.

## 5. Targets (the home of every number)

Loudness is ITU-R BS.1770-4: integrated (LUFS) for loops; for one-shots the highest 400 ms momentary loudness (LUFS-M), since a 200 ms step has no integrated loudness. Beds sit 12 to 16 LU under the console programme target of -23 LUFS so that steps, doors and speech lead; one-shots sit 8 to 13 LU over the day bed. That offset is judgement (section 6). A one-shot whose peak would pass -1.5 dBTP is held back: under its target, never over.

```targets-json
{
 "loop_seconds_min": 60,
 "loop_seconds_max": 75,
 "loop_lufs_tolerance": 0.5,
 "true_peak_max_dbtp": -1.0,
 "loops_lufs": {
  "amb_traffic_day": -40, "amb_traffic_night": -45, "amb_traffic_rain": -42,
  "amb_harbour_day": -41, "amb_harbour_night": -43, "amb_harbour_rain": -43,
  "amb_wind_day": -46, "amb_wind_night": -47, "amb_wind_rain": -43,
  "amb_gulls_day": -48, "amb_gulls_night": -56, "amb_gulls_rain": -54,
  "amb_voices_day": -50, "amb_voices_night": -53, "amb_voices_rain": -55,
  "amb_radio_day": -52, "amb_radio_night": -54, "amb_radio_rain": -54,
  "amb_rain_pavement": -37, "amb_rain_awning": -42, "amb_rain_gutter": -47
 },
 "bed_mix_lufs": {"day": -36.5, "night": -39.5, "rain": -33.5},
 "bed_mix_tolerance": 1.5,
 "one_shot_lufs_m": {"step": -27, "door_open": -26, "door_close": -23, "door_latch": -29, "bell": -25,
                     "phonebox_creak": -31, "phonebox_shut": -23, "phonebox_ring": -27},
 "one_shot_tolerance": 1.5,
 "min_variants": {"step_paving": 6, "step_setts": 6, "step_asphalt": 6, "step_wet": 6, "step_wood": 6,
                  "door_shop_open": 2, "door_shop_close": 2, "door_shop_latch": 2,
                  "door_house_open": 2, "door_house_close": 2, "door_house_latch": 2,
                  "bell_shop": 3, "phonebox_door_creak": 3, "phonebox_door_shut": 2, "phonebox_ring": 1},
 "seam_jump_max": 4.0,
 "seam_step_percentile_max": 0.95,
 "seam_step_ok_db": 1.0,
 "step_variant_max_correlation": 0.9,
 "voice_hf_fraction_max": 0.001,
 "grain_ms_max": 160,
 "grain_reuse_min_s": {"amb_voices_day": 12, "amb_voices_night": 20, "amb_voices_rain": 7,
                       "amb_radio_day": 20, "amb_radio_night": 20, "amb_radio_rain": 20}
}
```

## 6. What was read (all 12 October 2026 unless dated otherwise)

- EBU R128 (https://tech.ebu.ch/docs/r/r128.pdf): programme loudness -23.0 LUFS, true peak not above -1 dBTP, to ITU-R BS.1770 (https://www.itu.int/rec/R-REC-BS.1770, BS.1770-5 in force since November 2023).
- Sony's audio standards group, by its audio director (https://designingsound.org/2012/07/30/video-games-and-loudness-standards-interview-with-sonys-garry-taylor/): -23 LUFS console, -18 handheld, tolerance 2 LU. Meta Quest (https://developers.meta.com/horizon/documentation/unreal/audio-loudness-meter-overview/): -16 LUFS standalone, -18 PC.
- Not reached: the Sony document itself (gameaudiopodcast.com does not resolve from the cloud); AES TD1004 (trade-press summaries only; not used). No source read gives levels for beds under a programme target.
- Loops (https://splice.com/blog/audio-soundscape-for-video-games): take protruding sounds out of a bed, rotate the halves and crossfade, never let a recognisable call repeat every 15 s. Variants (trade blogs, weak): 4 to 8 per surface; six is the floor here.
- Freesound's API page (https://freesound.org/docs/api/resources_apiv2.html): the high-quality preview is about 128 kbps MP3 or 192 kbps OGG, the original needs a login. The previews used measure 160 to 190 kbps: the sources are lossy (NOTES.md).
- CC0 1.0 (https://creativecommons.org/publicdomain/zero/1.0/): each source page states it.
- The ring's cadence (secondary only, Wikipedia and a forum copy of ITU-T E.180): 0.4 s, 0.2 s, 0.4 s, 2 s; measured from the recording instead. Kiosks in 1990: BT's KX from 1985, red K6 still common (https://en.wikipedia.org/wiki/KX_telephone_boxes).
- No recording of 1990 Britain was read: sections 1 to 4 are judgement from the era and the source descriptions, to be heard.

## 7. Acceptance cases

Automatic (`check_sound.py`, checks/check_v1.json; each row names its case):

1. All 21 loops exist (the names in `loops_lufs`), and every footstep surface and one-shot group has at least `min_variants` files.
2. Every file is WAV, 16-bit, 48 kHz; loops are 75 s; one-shots mono.
3. Every loop is at least `loop_seconds_min` long.
4. Every loop measures within `loop_lufs_tolerance` of its target (ffmpeg's ebur128, a second implementation).
5. Every output's true peak is at most `true_peak_max_dbtp`; no sample is at full scale.
6. Every loop closes cleanly: seam jump at most `seam_jump_max` typical sample steps, and the level step across the seam is under 1 dB or no larger than at 95 percent of other places on the loop.
7. Every one-shot measures within `one_shot_tolerance` of its target, or lower and peak-limited; never higher.
8. Every one-shot starts and ends without a click (first sample and last 2 ms under -50 dBFS).
9. Within each footstep surface no two variants correlate above `step_variant_max_correlation` and no two files are identical.
10. The day, night and rain beds (the layers summed, mono layers centred) measure within `bed_mix_tolerance` of `bed_mix_lufs`; night is at least 2 LU under day, rain at least 2 LU over it.
11. The rain traffic's spectral centroid is above the day traffic's; night gulls have fewer calls than day and at most three.
12. Voices and radio: grains no longer than `grain_ms_max`, and no more than `voice_hf_fraction_max` of the power above 2.5 kHz.
13. Every output's every source has a row in `sources.json` with its page, author, licence, date read, download and md5, and the file on disk matches the md5.
14. Every source's licence reads CC0 on its page, and no source's title or page text holds a content-rule word.
15. Every WAV's sha256 matches `manifest.json`.
16. The previews exist: sixteen spectrogram JPEGs (the six layers with day, night and rain stacked, the three rains, the five footstep surfaces, the four door, bell and phone-box sets; 1600 px wide, under 500 KB) and nine listening clips (OGG Vorbis, at most 20 s, under 300 KB: the three bed mixes, a walk on each surface, the doors; audio stays out of git).

By ear (the fresh listener, against sections 1 to 4; NOTES.md lists them for Jafar):

17. Day mix: can the listener name traffic, gulls, harbour water and wind? Any child, word, music, alcohol or modern sound is a fault.
18. Night mix: clearly quieter and emptier; rain mix: clearly louder, rain in three places, fewer gulls.
19. Voices and radio read as people and a radio behind glass, never as words.
20. Each footstep surface sounds like its name; the eight variants do not sound like one step repeated.
21. Doors, bell and phone box read as named; which movement is "open", which "close", which click the latch, is the listener's call.
