# Quay Street sound: notes (12 October 2026, unit 10, proof P13)

## What was made

97 files, all 48 kHz 16-bit WAV, rebuilt exactly from 46 CC0 recordings by `make_sound.py` (BRIEF.md says what each must sound like and holds every number):

- **21 ambience loops, 60 to 75 s, seamless**: traffic, gulls, harbour, wind, voices through a window and a radio through a window, each in day, night and rain (18), and the rain on pavement, on an awning and in a gutter (3, rain only). Beds are stereo; gulls, voices, radio and the pavement rain are mono. Eighteen are 75 s; the rain traffic, the day wind and the rain harbour are 60 s (their recordings, the road 67 s, the wind 66.5 s and the rigging whistle 72 s, are too short for 75 s without playing part of them twice). Mixed at their own levels (the 60 s loops repeated, the mix measured over the 300 s in which all come round together) the day bed measures @@DAY@@ LUFS, night @@NIGHT@@, rain @@RAIN@@ (targets -36.5, -39.5, -33.5).
- **40 footsteps**: paving, setts, asphalt, wet, wood, 8 variants each (mono, @@STEPMIN@@ to 260 ms).
- **36 other one-shots**: shop door (open 2, close 3, latch 4), house door (open 3, close 5, latch 3), shop bell 5, phone box (door creak 5, door shut 3, a telephone ringing 3).
- Previews: 16 spectrogram JPEGs in `production/previews/cloud-week/sound/` (in git) and 9 listening clips (Ogg Vorbis, at most 20 s: the three bed mixes, a walk on each surface, the doors). **The clips are not in git** (the size guard refuses audio): they sit beside the JPEGs locally and in `/home/user/ledger-scratch/sound-out/clips/`. The WAVs and the clips live in `/home/user/ledger-scratch/sound-out/` and are rebuilt by one command, `make_sound.py`; on the PC they go to `F:\LedgerTools\sound-out`. The three mix clips carry +10 dB over their real levels, with a peak limiter, so they are audible (the rain clip is encoded at a lower Vorbis quality to stay under 300 KB); they are for judging what is in each bed.

## Rebuild

```
python production/cloud-week/sound/fetch_sources.py   # the sources, 102 MB, into SOUND_SOURCES
python production/cloud-week/sound/make_sound.py      # 97 WAVs (226 MB) and the 9 clips into SOUND_OUT, manifest.json; about 12 minutes
python production/cloud-week/sound/check_sound.py     # checks/check_v1.json: "N of M rows pass" (1049 of 1049 on the 12 October build)
python production/cloud-week/sound/make_previews.py   # the 16 spectrogram JPEGs, several minutes
python production/cloud-week/sound/check_sound.py --negative-controls   # breaks six outputs on purpose; each must fail by name (6 of 6 caught)
```

Needs ffmpeg, ffprobe, curl, numpy and scipy; no other package. The defaults are the cloud's folders; on the PC set SOUND_SOURCES and SOUND_OUT (for instance `F:/LedgerTools/sound-sources` and `F:/LedgerTools/sound-out`). Every step is deterministic (fixed cut points, seeded random numbers, seeded dither): a second run gives byte-identical WAVs, and `manifest.json` holds each file's sha256. `fetch_sources.py` refuses any source whose page does not say CC0, and downloads one file at a time, because Freesound's server answers 403 to parallel downloads.

## What is known to be short

- **The Freesound sources are lossy.** Each is the page's public high-quality preview (MP3, 160 to 190 kbps); the lossless original needs a free Freesound login, which is his to use or not. The 8 BigSoundBank sources are lossless. To swap in an original: put the file in the sources folder under the same name, run `fetch_sources.py --verify` after updating its md5, and rebuild.
- **Setts have no recording.** Two searches (Freesound: cobblestone, cobbled street, cobbles, setts, granite setts, paving stones, pavers, uneven stone, old town stones, pavés, adoquin; BigSoundBank: cobblestone, paving, stone) found one cobblestone footsteps take, at about 6 dB signal-to-noise: one step in 45 passed the clean-step tests. `step_setts_*` are steps on a stone patio and on old rough slabs: the nearest hard-stone steps found, not setts.
- **The phone box's ring is a house telephone.** A GPO 746 (1970s bell, double ring), not a kiosk payphone: searched phone box, phone booth, telephone box, kiosk, payphone, public telephone, British and UK telephone ring; no British kiosk ring is CC0.
- **Day traffic is a busy road made distant** by a low-pass and a leveller; night traffic is a quiet street in Hilversum; the rain traffic is a wet road in France with 8 dB more tyre hiss above 1.5 kHz (my processing, not a recording). The wind and some rain sources are French or Canadian. Nothing was heard.
- **Rain has one intensity.** The 5 October ruling has dry overcast, drizzle and rain; drizzle is not built separately (turn the three rain layers down for it, or the game fades them).
- **Gulls are few**: the day loop has nine calls from four takes, four of them re-pitched by 4 to 7 percent, in 75 s; night has one bird passing (a fifth take) and one far call; rain has two far calls.
- **The radio's identity is its band** (320 Hz to 3.2 kHz, a little distortion, hiss, then the window). It is made from an old-radio-style recording of someone talking far away, scrambled; no music.
- **Cut points for doors were read from envelopes and spectrograms, not by ear.** "Open", "close" and "latch" are the best reading; the shop door's open and close come partly from a heavy glass-and-metal theatre door and an old glass door. Eight one-shots are peak-limited and sit under their target (up to 4.5 LU under), never over.
- **Every loop is 75 s.** Layers started together repeat in lockstep: start each at a random point in its loop.
- **The footsteps are levelled to one loudness.** Natural differences between steps are gone; the game varies level and pitch. Paving is boots and trekking boots; Tom's trainers (`tools/ue/make_steps.py`, production/assets/steps) are separate and untouched. The paving takes carry a band near 1.2 kHz in every step, most likely the slabs ringing.

## Only an ear can judge (for Jafar, and the fresh listener)

1. Does the day bed read as a small British harbour town, or as somewhere else? (Distance of the traffic; the Hilversum and French sources.)
2. Gulls: right birds, right number, right nearness?
3. Voices and radio: behind glass, no word, no child (the sources are adult speech, but nobody has heard the loops); does the radio read as a radio?
4. Harbour: are there voices or people in the water recordings, or in the far boat engine (its page mentions a man and his dog aboard and wading birds; only the engine band below 700 Hz is used)? (The Dorset pages mention none; the Dorset takes open with what a comment on the page calls an "audio intro", so their first 12 s are not used.)
5. Rain mix: loud enough, the three rains in their places, the gutter not nagging.
6. Footsteps: does each surface sound like its name; do eight variants sound like one step repeated? Is the setts stand-in good enough or does it want a recording on the PC?
7. Doors, bell, phone box: which movement is open and which close, which click is the latch; does the bell read as a sprung coil bell above a door; is the ring right for 1990?
8. Anything modern, anything musical, anything alcoholic, anything a child said, anywhere.

## Set aside, and what was searched

- **Setts, kiosk payphone ring**: above.
- **A recorded radio**: searches (radio playing, radio voice, radio speech, AM radio, transistor radio, radio in the background, talk show radio) found real broadcasts, ham radio and effects; a real broadcast is out. Built from the scrambled voice instead.
- **Rejected sources** are in `sources.json` ("rejected") with why: a harbour page that mentions a beer delivery, a quay with summer crowds, a Leeds street with children, unfa's radio chatter (his page withholds consent for training generative models), the cobblestone take, wind-buried gulls.
- Nothing was substituted from a licence that is not CC0.

## Hosts

The cloud's proxy refused no host. Reached: freesound.org, cdn.freesound.org (403 to parallel downloads only, a Freesound rate limit; one at a time works), bigsoundbank.com, creativecommons.org, tech.ebu.ch, itu.int, designingsound.org, developers.meta.com, splice.com, en.wikipedia.org. Not reached: gameaudiopodcast.com (does not resolve; the Sony document), blog.criware.com (connection reset), zapsplat.com (403; not wanted). The web-fetch tool could not resolve any host; curl through the proxy worked.

## For the PC

The cloud has no Unreal, so the import format and the game's hooks are unknown here and nothing was guessed. Plain facts for whoever imports: PCM WAV, 48 kHz, 16-bit; no loop markers (set the loop flag in Unreal); mono for the sounds that should sit in space (gulls, voices, radio), stereo for beds; loop targets are integrated LUFS at nominal fader, one-shot targets are highest 400 ms momentary LUFS. How weather chooses day, night or rain and how the layers fade is the game's code, not decided here.
