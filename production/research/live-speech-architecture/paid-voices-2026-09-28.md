# Paid streaming voices for live conversation (research, 28 September 2026)

Which paid streaming voice could speak Sheila, Ron and Darren in under 2 s, keep their accents, and be allowed in a sold game. Thirty minutes of web reading; nothing signed up for or downloaded. [n] = sources at the end.

**Arithmetic.** 150 words/min × 60 = 9,000 words/h × 5.5–6 characters/word ≈ 50,000–55,000 characters per hour of speech; I use 55,000. Cost/h of speech = $ per 1M chars × 0.055. **Assumption: 20 min of speech per hour of play** (18,300 chars), so cost/h of play = $ per 1M × 0.0183.

| Service (model) | $/1M chars, plan | Per hour of speech | Per hour of play | First audio | Cloning, and its terms | Accent evidence |
|---|---|---|---|---|---|---|
| **Inworld Realtime TTS-2 Flash** | $15 On-Demand (no fee); $10 Creator ($25/mo); $7 Growth [1] | $0.83 / $0.55 / $0.39 | **$0.28** / $0.18 / $0.13 | Coval P50 **75 ms** (independent, 8 Sep) [27]; vendor 25 ms [2] | 3–30 s clip [3]; pro clone (beta) ~10 min, English [34]. A voice "you are authorized to share" [4]; tick-box [3] | Docs: instant clones "may not perform well" for "unique accents" [3] |
| Inworld Realtime TTS-2 | $25 / $20 / $12.50 [1] | $1.38 / $1.10 / $0.69 | $0.46 / $0.37 / $0.23 | Coval P50 170 ms [27]; 30-day mean 182 ms [28] | as above | Speaker similarity 3.62/5 (Hume's blind test) [30] |
| Cartesia Sonic-3.6 | 1 credit/char [7]: Pro $5/100K = $50; Startup $49/1.25M = $39; Scale $299/8M = $37 [6] | $2.75 / $2.16 / $2.06 | $0.92 / $0.72 / $0.69 | Coval 30-day mean **394 ms** [28]; vendor "sub-90ms" [35] | 10 s, "up to 60 seconds to better retain the speaker's accent"; pro 30+ min [8]. "others with explicit consent" [9]; "express permission" [10] | Only vendor saying accent carries over [8]; similarity 3.70 (3.5), 3.63 (3.6-beta) [30] |
| ElevenLabs Flash v2.5 / v4 Turbo | $40 ($0.04/1K) on paid tiers; v4 Turbo $11 until 12 Oct (promotion) [11] | $2.20 (promo $0.61) | $0.73 (promo $0.20) | Flash: Coval P50 185 ms [27], vendor ~75 ms [13]. v4 Turbo (out today): vendor ~150 ms [12] | 10 s (v4) [12], 1–2 min advised [14]; "right and consent to clone the voice" [14]; not "without consent or legal right" [18]; pro clone needs the speaker's spoken check [15] | Instant clones "may struggle with uncommon accents" [14] |
| Hume Octave 2 | Pro $70 for 1M, then $120; Business $500/10M = $50 [19] | $3.85 (over quota $6.60) / $2.75 | $1.28 ($2.20) / $0.92 | Vendor only, 100–200 ms [37]; not on Coval board [27] | 15 s [30]; "necessary rights or consent" [20] | none found |
| Fish Audio s2.1-pro | $15 per 1M bytes, no monthly minimum [24] | $0.83 | $0.28 | no measurement found | ~10 s; "explicit permission" [30]; commercial terms unclear | Best speaker similarity, 4.03 [30] |
| Rime (Mist v3 / Arcana) | $30 / $40 [22] | $1.65 / $2.20 | $0.55 / $0.73 | vendor 37 ms P50 (Mist v3) [22] | Enterprise only, 30–60 min of recordings [23] | none found |
| Azure personal voice; Google Chirp 3 custom voice | not collected | – | – | – | **Excluded**: the speaker must record a consent statement; gated access [25][26] | – |
| PlayHT | shut down 31 Dec 2025 after Meta bought it [33] | – | – | – | – | – |

## The three voices, and commercial use

- **Sheila** (designed, no real person): any service except Azure and Google; the rights are ours.
- **Ron, Darren** (VCTK p227, p241): CC BY 4.0 does not license **"publicity, privacy, and/or other similar personality rights"** [32]. Every service wants the speaker's consent or authorisation (Cartesia's wording strictest); VCTK speakers gave recordings for a synthesis corpus [36], not for commercial cloning. **A licence question for Jafar.**
- **Commercial:** Inworld licenses it even on free On-Demand [1] and assigns outputs to us [5]; Cartesia from Pro ($5) [6]; Hume Pro ($70) per pricing, Creator per terms [19][21]; ElevenLabs any paid plan [16], but serving a product's end users falls under OEM terms needing **Scale ($299/month)+** [17]. No attribution anywhere. Downloaded output may be used outside the service [4][10][16], so pre-generated lines can ship.

## Recommendation (confidence: medium on cost and speed, low on accent)

**Inworld Realtime TTS-2 Flash: about $0.28 per hour of play pay-as-you-go ($0.18 on Creator, $25/month)**, no minimum fee: the fastest independently measured and the cheapest major service, commercial without a subscription. TTS-2 if Flash clones worse ($0.37–0.46). Clone all three on it, with Cartesia as the comparison, and put them through the accent gate: no evidence found that any service keeps a Scottish or regional English accent. Jafar decides VCTK cloning first.

## Documented vs inferred

**Documented:** prices, fees, clip lengths, consent wording, Coval and Hume figures, the CC BY exclusion, the ElevenLabs OEM tier, PlayHT's end.

**Inferred (mine):**
- First sound ≈ 1.4 s (text) + 0.1–0.4 s (voice) + network from Europe (unmeasured; Coval's location unstated [29]) ≈ **1.5–1.9 s**: under 2 s. Near 1 s needs the text model's first sentence sooner.
- Vendors count 45,000 [6] to 60,000 [11][19] characters per hour; slower game speech costs less than shown.
- Per sold copy, 10 hours of play ≈ $2.80 on Inworld Flash, paid by us indefinitely; the game needs internet and a small server of ours holding the key.
- Speaker and accent similarity correlate (0.75, open models [31]), so higher-similarity services may hold accents better; unproven for commercial ones.
- Whether a live-speaking game is ElevenLabs "OEM" use.
- VCTK's ~400 sentences per speaker [36] may suffice for Inworld's ~10 min pro clone.

## Sources (read 28 September 2026)

1. inworld.ai/pricing (undated). 2. Inworld TTS-2 launch, finance.yahoo.com/technology/ai/articles/inworld-launches-realtime-tts-2-160000791.html (2 Sep 2026). 3. docs.inworld.ai/tts/voice-cloning (undated). 4. inworld.ai/service-specific-terms (14 May 2026). 5. inworld.ai/terms (11 Jun 2025). 6. cartesia.ai/pricing (undated). 7. docs.cartesia.ai/pricing (undated). 8. docs.cartesia.ai/build-with-cartesia/capability-guides/clone-voices (undated). 9. cartesia.ai/legal/acceptable-use (23 Jul 2025). 10. cartesia.ai/legal/terms (14 Jun 2024). 11. elevenlabs.io/pricing/api (undated; promotion to 12 Oct). 12. elevenlabs.io/blog/eleven-v4 (28 Sep 2026). 13. elevenlabs.io/docs/models (undated). 14. elevenlabs.io/docs/product-guides/voices/voice-cloning/instant-voice-cloning (undated). 15. …/professional-voice-cloning (undated). 16. elevenlabs.io/terms-of-use (31 Mar 2026). 17. elevenlabs.io/oem-terms (28 Feb 2025). 18. elevenlabs.io/use-policy (17 Aug 2026). 19. hume.ai/pricing (undated). 20. dev.hume.ai/docs/voice/voice-cloning (undated). 21. hume.ai/terms-of-use (25 Feb 2025). 22. rime.ai/pricing (undated). 23. docs.rime.ai/platform/voice-cloning (undated; seen via search summary only). 24. docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits (undated). 25. learn.microsoft.com/en-us/azure/ai-services/speech-service/personal-voice-overview (16 Sep 2026). 26. docs.cloud.google.com/text-to-speech/docs/chirp3-instant-custom-voice (24 Sep 2026). 27. Coval board read 8 Sep, reported by a competitor: gradium.ai/content/tts-latency-benchmark-2026 (updated 10 Sep 2026). 28. Coval 30-day means to 22 Sep: dasha.ai/blog/tts-leaderboard (23 Sep 2026). 29. gradium.ai/blog/coval-perceived-ttfa-benchmark (9 Sep 2026). 30. Hume's Voice Replication Leaderboard (10 Sep 2026), via marktechpost.com/2026/09/21/best-voice-cloning-apis-in-2026-speaker-similarity-consent-checks-and-price-per-1m-characters/ (21 Sep 2026). 31. arxiv.org/html/2603.14328 (15 Mar 2026). 32. creativecommons.org/licenses/by/4.0/legalcode.en §2(b)(1) (undated). 33. rinzara.com/articles/playht-alternatives-2026 (undated, 2026). 34. orcarouter.ai/blog/inworld-realtime-tts-2-flash-launch (4 Sep 2026). 35. marktechpost.com/2026/08/18/cartesia-ships-sonic-3-6-a-streaming-tts-model-that-now-leads-both-artificial-analysis-speech-arenas/ (18 Aug 2026). 36. datashare.ed.ac.uk/handle/10283/3443 (13 Nov 2019). 37. hume.ai/blog/octave-2-launch (seen via search summary only; undated).
