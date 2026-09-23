# Nano on the card with the game running, 24 September

Jafar's order of 23 September, overnight: "Time Nano on the card with the game
running." Measured on his PC (AMD Radeon RX 6700, about 9.4 GB of video memory
usable), 23:35 to 23:55, with the build machine idle and nothing else on the
card. Nano spoke the listening test's ten lines in its BUILT-IN voice: no cast
voice was recorded, since the consent questions are open.

## What ran where

Nano's token model runs on the card through DirectML. The last step, which
turns sound tokens into a waveform, stays on the processor: DirectML has no
complex numbers and aborts on that step. The timing script works round three
DirectML gaps without touching Nano: the built-in voice was saved on an NVIDIA
card; inference mode is not supported; and empty tensors cannot be joined.

## The numbers

| run | what | frame median | slowest 1% | frames a second | video memory |
| --- | --- | --- | --- | --- | --- |
| A | the slice at 1280x720 | 8.4 ms | 9.4 ms | 120 | game 3.0 GB |
| B | the slice at 3440x1440, drawn at half and upscaled | 11.8 ms | 12.9 ms | 85 | game 3.5 GB |
| C | B with Nano speaking on the same card (two runs) | 12.5 ms | 16.0 ms | 80 | game 3.5 GB + Nano 2.1 GB |

Nano, seconds of work per second of speech (under 1 keeps up with talk):

| run | overall | median | worst line |
| --- | --- | --- | --- |
| Nano alone on the card (30 lines over two runs) | 0.90 to 1.04 | 0.89 to 0.95 | 1.8 |
| Nano with the game running (12 lines in each of two runs) | 1.28 to 1.32 | 1.33 to 1.38 | 1.55 |
| Nano on the processor alone (23 Sep, contended) | about 1.9 | | |

## What it means

- The game meets the performance target today, at Jafar's screen size with
  the voice running: 80 frames a second, and the slowest 1% at 62, never near
  30. That is the ordinary slice, with the player standing still, at the
  default settings. The corner's highest settings are a different load (25 ms a
  frame at 1280x720 on the probe).
- With the game running, Nano is slower than talk: a three-second line takes
  about four seconds before any of it can play, because Nano gives the whole
  line at once rather than a piece at a time.
- On memory, game and voice together take about 5.7 GB, which leaves about
  3.7 GB of the card for anything else that runs locally, such as a
  line-writing model.

Raw summary: card-timing-2026-09-24.json. Scripts: card_matrix.ps1 (the
runs) and nano_card_timing.py (Nano's timing). The game's frame times come
from its own CSV profiler, and the first 300 frames are dropped while the
street loads.
