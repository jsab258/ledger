PASS

# Quay Street sound: fresh listener-reviewer's check, v1 (12 October 2026, unit 10, proof P13)

The reviewer did not write or build the unit and **cannot hear audio**. Nothing here was listened to. Every judgement below rests on measurement of the 97 WAVs and 9 clips, the 16 spectrogram pictures, the sources' own pages, a rebuild, and reading the code. The "ONLY AN EAR CAN JUDGE" section at the end lists what still needs Jafar's ears. The builder's own check was not re-run; every number here comes from the reviewer's own scripts. Loudness was measured with ffmpeg's ebur128, seams and spectra with numpy and scipy.

Verdict: no fault. All 16 automatic acceptance cases pass on independent measurement. No content-rule matter was found on any page read or by measurement. 16 rebuilt outputs are byte-identical. There are 12 narrow points, each with an exact fix. Under Jafar's ruling of 9 October that makes the unit a PASS, with the points below.

## Faults

None.

## Narrow points (worst first; each with its measurement and exact fix)

1. **Three beds play part of their own source twice inside the 75 s loop.** This was confirmed by waveform correlation of 1.000 at the predicted lag (0.70 for the harbour whistle, which sits under different water), against 0.03 at a lag 3 s off.
   - `amb_wind_rain`: source seconds 41 to 50 play at loop 41 to 50 and again at 50 to 59, **back to back, 9 s apart**. The brief's own research says never let a recognisable sound repeat every 15 s.
   - `amb_traffic_rain`: about 22 s (source 24 to 46) plays twice, 19 s apart.
   - `amb_wind_day`: about 28 s plays twice, 39 s apart.
   - `amb_harbour_rain`: the rigging whistle's 10 to 25 s plays twice, 59 s apart.

   NOTES and the manifest do not say so. The fixes:
   - Wind rain: the source is 90.75 s long, so take it in one piece, `cut_src("bsb_625", 0.0, 79.5)`.
   - Traffic rain and wind day: their sources are only 67.1 s and 66.5 s, too short for 75 + 4 s without a repeat. Build them as 60 s loops from source 0 to 64 s, giving `bed_loop` a length argument. Change the brief's case 2 from "loops are 75 s" to "loops are 60 to 75 s"; case 3 already allows 60 s. Unequal loop lengths also stop layers repeating in lockstep.
   - Harbour rain: leave it as it is (59 s apart), or take one longer whistle stretch.
2. **`amb_harbour_rain` carries a steady low engine-like drone the whole way through.** It is a harmonic series at about 73, 96, 111, 128, 144 and 193 Hz. In the right channel it stands mostly 10 to 20 dB over its neighbouring frequencies and sits 8 to 28 dB under that channel's total power. It comes from the Dorset take 182612 (the lines are there through the whole take) and not from the other two Dorset takes. The brief has an engine in the day harbour once, none at night, and none in the rain. Fix: in `build_harbour("rain")`, high-pass the 182612 water at 200 Hz (order 4) instead of 100 Hz. Then measure again: no line over 10 dB between 60 and 220 Hz.
3. **`amb_traffic_rain`, right channel: a steady whine at 1281 Hz** from about 5 s to the end. It stands 10 to 19 dB over its neighbours and sits 16 to 24 dB under that channel's power. It is in the BigSoundBank source's right channel (+10 to +18 dB there). It is steady, with no regular pulsing, so it is not a reversing beeper. It is still a stray tone. Fix: a notch at 1281 Hz (Q about 30, at least 20 dB deep) on channel 1 of the bsb_621 cut, before the hiss boost.
4. **Wet steps 01 to 04 stop while still sounding.** Their last 20 ms are only 7 to 10 dB under their peak, and a 15 ms fade cuts them off. They show as flat rectangular blocks in the wet-steps picture. The other 36 steps end 14 to 38 dB down. The cutter's "died away" test accepts any tail under 3 times the take's noise floor, and these puddle takes are noisy. Fix: in `stepcut.cut`, judge "died away" against the step's own peak (-20 dB) and not against the floor. Re-pick the wet set, or give wet steps a 40 ms fade.
5. **Some steps start inside a sound already going.** In the source, the 10 to 40 ms before the cut is already 4 to 15 dB under the step's peak:
   - `step_paving_06` ramps up to -5 dB re its peak before the cut.
   - `step_wood_06` and `step_wet_02` have -4 to -20 dB of sound before the cut.
   - `step_wet_07` measures -6 dB in its first 2 to 8 ms.

   The 2 ms fade-in then makes a second, artificial onset about 10 ms before the real hit. Fix: in `stepcut.cut`, reject a candidate whose 20 ms before the cut is within 20 dB of its peak, or give such steps an 8 ms raised-cosine fade-in.
6. **The night wind is not "lower, darker" than the day wind, as the brief asks.** Its spectral centroid is 633 Hz against 517 Hz. Its 1 to 4 kHz share is the same (18%), and its below-250 Hz share is half the day's. It is also 1 LU louder (targets -45 against -46). It is steadier, as asked: 3.9 dB against 10.9 dB between the 10th and 95th percentile of its 100 ms level. Fix: night wind low-pass 1800 Hz → 1000 Hz and target -47 LUFS. The night bed then measures -40.1 LUFS, within 1.5 of -39.5 and 3.6 under day. Or reword the brief to what was built.
7. **Voices and radio: three places where speech runs on longer than one grain.** A replay of the builder's own random draws confirms grains of 80 to 149 ms (voices) and 90 to 159 ms (radio). But at three places the next grain starts within 10 ms of where the previous grain left off in the source, so up to about 225 ms of continuous speech is heard: night voices at 42.3 s and 52.5 s, the radio at 43.5 s (all three radio versions). Fix: in `grain_babble`, draw again when a grain's source start is within 50 ms of the previous grain's continuation in the same source.
8. **The radio and the night voices are drawn from very short recordings.**
   - The radio's source is 18.8 s, and each 10 ms of it is reused about 8 times in 75 s (up to 17).
   - The night voices' source is 19.7 s, reused 7.9 times on average.
   - The radio's source is already muffled: 90% of its power lies between 445 and 727 Hz. So the builder's 320 Hz to 3.2 kHz "small speaker band" has nothing above about 820 Hz to work on.

   The radio measures nearly like the voices: 99.4% of its power is in 250 to 1000 Hz against 93% for the day voices, and its 95% roll-off is 756 Hz against 844 Hz. Its identity as a radio is at risk, and repeated fragments may be heard. Fix: if Jafar's ear says it does not read as a radio, use a longer CC0 adult-speech source with a full band, so the speaker band and its distortion have something to work on. Keep the window as it is.
9. **The previews show a false line, and NOTES misreads it.** Every spectrogram panel has a horizontal line one tenth of the way up: 960 Hz on the 10 kHz panels, 1.2 kHz on the one-shot panels, 1.4 kHz on the rain panel. It is a drawing artefact of the settings used in `make_previews.py`. Pink noise drawn the same way shows it, and no WAV has a tone or a notch there (Welch spectra). NOTES' sentence "The paving takes carry a band near 1.2 kHz in every step, most likely the slabs ringing" reads this artefact as sound. Measured, there is no such band: the strongest narrow peak in the paving steps between 0.7 and 1.8 kHz is +4.4 dB, the same as on the other surfaces. Fix: delete that sentence from NOTES, and add one line under the previews saying the line is the drawing's.
10. **The brief's prose disagrees with its own numbers.** The numbers block is the home, so the prose should follow it.
    - "Beds sit 12 to 16 LU under -23 LUFS": the night bed is 16.5 under and the rain bed 10.5 under.
    - "One-shots sit 8 to 13 LU over the day bed": latch is 7.5, phone-box creak 5.5, door close and phone-box shut 13.5.

    Fix: reword to "the day bed 13.5 LU under the programme, night 3 LU lower, rain 3 LU higher; one-shots 5.5 to 13.5 LU over the day bed".
11. **The listening clips are kept out of git only by this clone's own exclude file** (`.git/info/exclude`, which is not versioned). On the PC, `make_sound.py` will write nine OGGs as untracked audio into `production/previews/cloud-week/sound/`. Fix: in `make_previews.make_clips`, write the clips only to `SOUND_OUT/clips`, or add `production/previews/cloud-week/sound/*.ogg` to the tracked `.gitignore`.
12. **Small record and code gaps:**
    - `sources.json` has `"uploaded": null` for fs_744592; its page says 4 July 2024.
    - THIRD-PARTY's "Street sound" row says `check_sound.py` refuses a source whose page does not say CC0. `check_sound.py` reads `sources.json`; it is `fetch_sources.py` that reads the page. Reword.
    - Case 11's gull count is read from the manifest's plan, not measured in the audio. Measured from the audio, it agrees: rises above the floor at day 12 (9 calls, some runs split), night 2, rain 3 (2 calls).
    - `build_harbour` has dead code, `104.0 if False else 100.0`.

## What is right

**The acceptance cases, measured independently:**

| Case | Result | Measurement |
|---|---|---|
| 1 inventory | PASS | 21 loops. Steps 8 per surface. Shop door open 2, close 3, latch 4; house door 3, 5, 3; bell 5; phone box creak 5, shut 3, ring 3. Every group at or over its minimum. |
| 2 format | PASS | ffprobe: all 97 are 16-bit PCM, 48 kHz. Loops 75.000 s. All 76 one-shots mono. |
| 3 length | PASS | 75.0 s ≥ 60. |
| 4 loop loudness | PASS | ffmpeg ebur128: all 21 on target, to the meter's 0.1 LU. |
| 5 peaks | PASS | Highest true peak: loops -2.7 dBTP (pavement rain), one-shots -1.5 dBTP. Highest sample -1.51 dBFS. Bed mixes -15.1, -17.1, -5.7 dBTP. |
| 6 seams | PASS | Own test, each channel of every loop joined end to start. Sample jump at most 0.74 of the 99.9th-percentile step nearby. No click-energy burst: the join's 3 ms high-frequency energy ranks below 89% of all windows in every loop. Level step at 1 s within the ordinary. At 400 ms two joins stand out (harbour rain right 3.8 dB, 98th percentile; night voices 7.3 dB, 96th). By construction the join is the recording's own continuation (beds) or a point on a circle (voices), so this is content, not a seam. |
| 7 one-shot loudness | PASS | 68 within 0.6 LU of target. 8 peak-limited, 0.2 to 4.5 LU under. None over. |
| 8 one-shot ends | PASS | Loudest first sample -90.3 dBFS. Loudest last 2 ms -57.4 dBFS (step_wet_02). |
| 9 step variants | PASS | Closest pairs by cross-correlation: paving 0.74, setts 0.79, asphalt 0.71, wet 0.27, wood 0.60 (limit 0.9). No identical files. No two cuts overlap in a source. |
| 10 bed mixes | PASS | Own sum (mono layers centred), ffmpeg: day -36.5, night -39.6, rain -33.4 LUFS. Night 3.1 LU under day, rain 3.1 over. |
| 11 versions differ | PASS | Rain traffic centroid 920 Hz against day 476 Hz; also steadier (5.7 against 8.9 dB) and wider (roll-off 2.5 against 1.2 kHz). Gull calls: day 9, night 2, rain 2. |
| 12 voices, radio | PASS | Replayed grains at most 150 / 160 ms. Power above 2.5 kHz 0.002 to 0.006% (limit 0.1%). Above 1.2 kHz 0.01 to 0.4%. |
| 13 source records | PASS | All 47 source md5s match the files. Every output's sources have full rows. Every source is used. THIRD-PARTY lists all 47. |
| 14 licences, words | PASS | 23 source pages read (below). Each states CC0. Titles, authors and dates match `sources.json` except one missing date (point 12). |
| 15 hashes | PASS | All 97 sha256 match the manifest. |
| 16 previews | PASS | 16 JPEGs, all 1600 px wide, 93 to 353 KB. 9 clips Ogg Vorbis, 5.3 to 20.0 s, 20 to 254 KB. |
| 17 to 21 | NOT JUDGEABLE WITHOUT AN EAR | See the last section. Supporting measurements are above and in points 1 to 8. |

**Rebuild.** Sixteen outputs were rebuilt from the sources with `make_sound.py`'s own functions into a scratch folder, without writing `manifest.json`:

- the loops `amb_traffic_rain`, `amb_voices_night`, `amb_radio_day`, `amb_gulls_day`, `amb_harbour_day`;
- all 8 wet steps;
- `door_shop_close_02`, `phonebox_ring_01`, `bell_shop_03`.

All 16 are byte-identical to the outputs, with a maximum sample difference of 0. The manifest's hash was unchanged afterwards. The build is deterministic, as NOTES says.

**The layers against the brief (spectrograms and measurement):**

- **Traffic.** Day is a low roar under 1.8 kHz with soft swells. Night has long quiet stretches with single passes (levels vary 16.4 dB between the 10th and 95th percentile). Rain is a wider, steadier band.
- **Gulls.** Sparse, high harmonic calls with silence between: day 9 placed calls, night one bird passing at 31 to 43 s and one faint call, rain two dull calls.
- **Harbour.** Day has water slaps and rigging. Night is calmer, with no engine line. Rain has the whistle at 2.5 to 3 kHz (and the drone, point 2).
- **Rain.** Pavement is dense broadband drops. Awning is a softer patter. Gutter is a running-water band with drips.
- **Voices and radio.** Band-limited under about 1.2 kHz, a dense grain texture with slow swells. Night voices come and go in gaps, as the brief asks.
- **Footsteps** are single short events of 101 to 260 ms: paving mostly heel then toe, setts, asphalt and wood mostly one or two hits.
- **Bell** partials ring out for 1 to 3 s.
- **Phone ring** shows the bell's partials in a double burst.
- **Door creaks** show as gliding harmonics.

**Stray sounds, by measurement.** The reviewer searched every loop for tones lasting at least 120 ms and standing 15 dB over their surroundings. Outside the gulls, voices and radio, none was found:

- no steady pulsed tone at 1 to 3 kHz (a reversing beeper);
- no slowly sweeping tone (a siren);
- no harmonic stacks moving in steps (music).

The two steady tones found are points 2 and 3. A voice detector was checked against the Dorset take's spoken introduction: it found 7 voiced runs in that 10.5 s and none in 84 s of the water. Run over every bed, it found:

- no speech-like voicing in traffic rain, harbour day and rain, wind day and rain, awning or gutter;
- 10 very short, steady-pitched runs in day traffic, which are engine tones;
- four short runs (60 to 80 ms) in the first 10 s of the night harbour, two of them with moving pitch (5.5 s and 9.6 s); probably water, listed for the ear;
- one 70 ms run with moving pitch in the pavement rain at 31.8 s; listed for the ear.

**Sources.** Each page was opened by the reviewer, one request at a time through the proxy, and read on 12 October 2026.

- Every stand-in or substitute the notes name: setts fs_637555 and fs_868548; the ring fs_435577; the radio fs_528615; the shop door fs_402460 and bsb_1270; traffic fs_503456, fs_395686 and bsb_621.
- 12 more drawn at random (seeded): fs_575898, fs_538015, fs_372213, fs_57743, fs_73497, fs_744592, fs_454130, fs_554845, fs_538016, fs_182610, fs_182612, fs_757318.
- Two the notes single out: fs_559821 and fs_846446.

All 23 pages state "Creative Commons 0" (Freesound) or "CC0 (public domain)" (BigSoundBank) and link the CC0 1.0 deed. Titles and authors match. Nothing in any description, tag or comment puts children, alcohol or a pub, gambling, a real brand or broadcast, or music into the file. What was looked at:

- **fs_868548**: "recorded on a mobile phone". The phone is the recorder, not a sound. The page was uploaded 1 September 2026.
- **fs_846446**: recorded December 2025 in a village lane. The era matters only if a modern sound is heard. In the used cut (high-passed at 250 Hz) no tone of any kind was found.
- **fs_559821**: the page mentions a man, a dog and wading birds. The used 150 to 186 s, low-passed at 700 Hz, has no burst more than 10 dB over the running level between 300 and 700 Hz, and no voiced run: no bark or sneeze by measurement.
- **fs_528615**: tagged "old radio". A commenter asks how the "radio edit" was done, so the radio colour is the uploader's own processing. The page does not say who speaks, or that it is not taken from a broadcast. After scrambling, no word or voice identity should survive; listed for the ear.
- **The Dorset takes**: the spoken introduction is real. A picture of 182611's first 16 s shows speech harmonics up to about 10.5 s. The builder's cut at 12 s (14 s for 182610) is right.

**The rejected list is honest where checked.** unfa's page (245660) does withhold consent for training generative models. The Dorset 01 page (182601) has the "audio intro" comment. The Leeds page (412012) says "children screaming". The remaining rejections (the Swanage summer quay, the cobblestone take, the wind-buried gulls) rest on the builder's judgement or measurement, not on page text, and were not re-checked.

**What the work gets right.** The unit is well made:

- Every number has one home and the code reads it from there.
- The build is exactly repeatable.
- The loops are seamless by construction, and the measurement agrees.
- Levels are set by gain and never by a limiter.
- The stand-ins are named honestly in the brief and the notes.
- The rejected sources are recorded with reasons.
- The content rule was applied at source selection, with care: the Whitby beer delivery, the Leeds children, the Dorset spoken introduction cut off.

## Limits of this review

- **Not reached:** the Whitby page (freesound.org/s/748894, the beer-delivery rejection) answered 403 twice, so that reason is unverified (rejecting it is safe either way). Freesound answers 403 to a plain request on its short `/s/` addresses; the author's full page address with browser headers works. One page (fs_575898) refused once and was read on the second try.
- **What measurement cannot show:**
  - Whether a single short word survives inside one grain. A grain of up to 160 ms can hold a one-syllable word, and low-passing at 1.2 kHz removes most consonants but not all vowels.
  - Whether a voice in the murmur is a child's.
  - A car's era.
  - Whether a door sounds "modern".
  - Whether a layer sounds like what it is named.

  The syllable-rate test does not separate scrambled from intact speech here: both keep 45 to 58% of their envelope power at 2 to 8 Hz, because each grain is about one syllable long. So the "no word survives" claim rests on construction (one grain at most, two random grains always overlapping) and on Jafar's ear, not on that measure.

## ONLY AN EAR CAN JUDGE

For Jafar, in plain words. The clips are in `sound-out/clips` (on the PC, `F:\LedgerTools\sound-out\clips`); the full files are beside them. Headphones, at a normal listening level.

1. **Day street** (`clip_mix_day`): can you hear traffic, gulls, harbour water and wind? Does it sound like a small British harbour town around 1990, or like somewhere else? Any word, any child, any music, anything modern?
2. **Night and rain** (`clip_mix_night`, `clip_mix_rain`): is night clearly quieter and emptier? Is rain clearly louder, with rain in three places (on stone, on a canvas awning, from a gutter), fewer gulls, and the gutter not nagging?
3. **People and radio behind a window** (`amb_voices_day`, `amb_voices_night`, `amb_voices_rain`, `amb_radio_day`, `amb_radio_night`, `amb_radio_rain`; play each whole):
   - Do you ever catch a word? Listen hardest at about 42 and 52 seconds in the night voices, and at about 43 to 44 seconds in the radio.
   - Any child's voice? Any singing?
   - Does a bit of speech keep coming back?
   - Does the radio sound like a radio at all, or just like more people talking?
4. **Repeats in the loops:**
   - Rain wind (`amb_wind_rain`), 41 to 59 seconds: the same 9 seconds of wind play twice in a row. Do you notice?
   - Rain traffic (`amb_traffic_rain`): a stretch from 24 seconds comes again at 43 seconds.
   - Day wind (`amb_wind_day`): a stretch from 8 seconds comes again at 47 seconds.
5. **Rain harbour** (`amb_harbour_rain`): is there a low steady hum or engine under the water all the way through? Does it sound like a boat's engine, a machine, or nothing? Is it wanted?
6. **Rain traffic** (`amb_traffic_rain`), right ear: a faint steady high whistle. Can you hear it?
7. **Night harbour** (`amb_harbour_night`), first 10 seconds: any voice in the water? And the pavement rain (`amb_rain_pavement`) at about 32 seconds: a bird or a voice?
8. **Footsteps** (the five `clip_steps_` clips, then the 40 files):
   - Does each surface sound like its name: paving, setts, asphalt, wet, wood?
   - Do the eight sound like one step repeated?
   - Do wet steps 1 to 4 sound chopped off at the end?
   - Do paving 6, wood 6 and wet 2 start too abruptly?
   - Are the setts, which are a stand-in made from stone patio and old slabs, good enough, or do they want a real recording?
9. **Doors, bell, phone box** (`clip_doors` plays one of each; all 36 files are beside it):
   - Which is the door opening, which closing, which click is the latch?
   - Does the bell sound like a sprung bell over a shop door?
   - Is a 1970s house telephone's ring acceptable for a phone box in 1990?
   - Do house-door closes 4 and 5, from a "modern front door" recording, sound modern?
10. **Loop ends:** set any loop to repeat and listen across its end for a bump or a click, especially rain harbour and night voices.
11. **Anywhere:** a car alarm, a mobile phone, an electric car's whine, a reversing beep, a siren, music, glasses or pub noise, a child.
