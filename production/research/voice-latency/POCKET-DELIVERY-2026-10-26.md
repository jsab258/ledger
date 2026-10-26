# Livelier delivery from Pocket TTS: Darren (26 October 2026)

The owner on Darren's Pocket voice (VCTK p286): "A is ok, but very robotic and unemotional". This builds on production/research/voice-direction/SUMMARY.md (30 September): read clips give read lines.

## Questions

1. In Pocket TTS, what controls expressiveness and prosody: the reference clip (style, emotion, length), temperature, decode steps, noise clamp, punctuation, anything else?
2. How do practitioners of zero-shot cloning choose or prepare reference clips for emotion, and do they keep several per character for moods?
3. Which open, licence-clear sources of expressive or conversational British (ideally north-east) male speech could serve as reference clips?
4. What in the installed source shows how the clip is used?
5. What to try, cheapest first, and how to judge each?

Method: every link was read on 26 October 2026 (through a page-text tool, or the browser pane for script-built pages). The installed package (pocket-tts 4.0.1, installed 21 October) was read directly. Kyutai's code and docs are MIT-licensed and quoted briefly; other sources are paraphrased.

## 1. What steers delivery in Pocket TTS

- **The reference clip, above all.** Kyutai's docstring says the voice state captures "speaker voice, style, prosody" (models/tts_model.py line 934). Training cuts each utterance between two words: the part before is the prompt, the rest the target (manukyutai, Kyutai collaborator, [issue #198](https://github.com/kyutai-labs/pocket-tts/issues/198)). So the model learns to carry on the clip's own utterance. Inference, untested: read newspaper sentences ask for more reading.
- **Recording conditions carry over:** "the audio quality of the sample is also reproduced" ([README](https://github.com/kyutai-labs/pocket-tts)). A Kyutai contributor says audiobook voices may not suit conversation ([#115](https://github.com/kyutai-labs/pocket-tts/issues/115)).
- **Temperature** sets the sampling noise. The default, 0.3, is what listeners preferred (config/english.yaml line 5), and Darren runs at it today. Kyutai's docs list 1.0 as "More expressive" ([generate docs](https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/)). Higher temperature also spreads speaker identity ([CALM paper](https://arxiv.org/html/2509.06926v3), Appendix C), moving the voice away from the clip. September's American drift was on an older build, at an unknown temperature.
- **Decode steps** (default 1) buy quality, not expression, at a time cost. **Noise clamp** (off) cuts extreme noise; its effect on liveliness is unverified.
- **Text:** the model was trained on single sentences ending in . ? or ! (text_chunking.py line 64). Pauses in text are unsupported ([model card](https://huggingface.co/kyutai/pocket-tts)). There are no emotion tags; the request is open ([#52](https://github.com/kyutai-labs/pocket-tts/issues/52), [#15](https://github.com/kyutai-labs/pocket-tts/issues/15)), and Kyutai's answer is to fine-tune on emotional data.
- **Accent:** a user reports cloned UK voices losing much of their accent, with no Kyutai reply ([#152](https://github.com/kyutai-labs/pocket-tts/issues/152)).

## 2. The professional method

- **ElevenLabs:** a clone copies pace, inflection, accent and emotion; a monotone sample gives monotone speech; one consistent performance per voice, 1 to 2 minutes ([Instant Voice Cloning](https://elevenlabs.io/docs/product-guides/voices/voice-cloning/instant-voice-cloning)). Deliveries already in the source audio come most easily ([prompting guide](https://elevenlabs.io/docs/best-practices/prompting/eleven-v3)).
- **F5-TTS** takes one reference clip per speech type (Regular, Surprised, Sad, Angry, Whisper, Shouting). Each clip runs under 12 s and ends on about 1 s of silence ([infer README](https://github.com/SWivid/F5-TTS/blob/main/src/f5_tts/infer/README.md), [app source](https://raw.githubusercontent.com/SWivid/F5-TTS/main/src/f5_tts/infer/infer_gradio.py)).
- **Kyutai** ships one EARS speaker's separate emotional recordings so users can try one voice with several emotions ([tts-voices](https://huggingface.co/kyutai/tts-voices)).
- **XTTS-v2** claims emotion and style transfer by cloning ([card](https://huggingface.co/coqui/XTTS-v2)). **StyleTTS 2**'s beta trades the clip's prosody for the text's: more emotion, less likeness ([notebook](https://raw.githubusercontent.com/yl4579/StyleTTS2/main/Demo/Inference_LibriTTS.ipynb)). F5-TTS and XTTS are on the never-ship list; they are cited for method only.
- **In short:** the clip is the performance. Use a clean clip already in the wanted register, one mood per clip, and several clips per character, chosen per line.

## 3. Sources of British male speech for reference clips

| Source | Speech | North-east | Licence | Game use |
|---|---|---|---|---|
| [VCTK](https://datashare.ed.ac.uk/handle/10283/3443) | read, studio | p286 | CC BY 4.0 (Kyutai's page, allowlist; licence file unopened) | yes |
| [OpenSLR 83](https://www.openslr.org/83/) | read | "Northern English male", town not given | CC BY-SA 4.0 | yes, share-alike |
| [Common Voice](https://mozilladatacollective.com) | read ("British English", 6.97 GB); spontaneous answers (English, 519 MB) | self-reported; unverified | CC0-1.0 (listing); terms of use unverified | likely; download needs his yes |
| [EdAcc](https://huggingface.co/datasets/edinburghcstr/edacc) | Zoom conversations, 40 h | none seen | CC BY-SA 4.0 | yes, but copies Zoom sound |
| [LibriVox](https://librivox.org/pages/public-domain/) | dramatic readings | Lancashire, Yorkshire readers only ([table](https://wiki.librivox.org/index.php/Accents_Table)) | public domain in the USA, "not necessarily" elsewhere | his call: named readers may count as real people (allowlist) |
| Kyutai voice-donations | volunteers | unverified | CC0 | yes |
| [DECTE](https://research.ncl.ac.uk/decte/) | Tyneside interviews | yes | none stated; "designed for research use" | no, without permission |
| Expresso, EARS | acted emotion | no | CC BY-NC 4.0 | no |
| [Emilia](https://huggingface.co/datasets/amphion/Emilia-Dataset) | internet speech | unlabelled | NC; YODAS part CC BY 4.0 | no: identifiable real speakers |

None found is expressive, north-east, male and commercially clear. The professional route, a hired actor recording clips per mood with written consent to cloning, is money and identity: the owner's decision.

## 4. How the installed source uses the clip

- `get_state_for_audio_prompt` (tts_model.py lines 928 to 1054) keeps the first 30 s, given `truncate=True` (lines 1028 to 1032; pocket-server.py line 102). `end_on_pause` (data/audio_utils.py lines 31 to 58) ends it on 80 ms of silence, since a clip ending on speech gets continued.
- `_encode_audio` (lines 455 to 464) turns the clip into frames, 12.5 a second, and every frame enters the transformer's memory (lines 1045 to 1048). Nothing is reduced to one fingerprint, so rhythm and pitch movement stay available to copy (inference).
- Each sentence restarts from the same state (lines 764 to 765); a TODO (lines 717 to 720) says one chunk's audio does not yet condition the next, and the server reseeds per sentence (pocket-server.py lines 136 to 139). Every sentence leans on the clip alone.
- `_ensure_terminal_punctuation` (text_chunking.py lines 61 to 79) turns a trailing comma into a full stop, and `sentences()` (voice-server.py lines 55 to 81) cuts a long first sentence at a comma: "Dark coat, moving quick" begins as a finished "Dark coat." Possibly part of the stiffness; unverified by ear.
- Temperature and clamp: `FlowLMModel.forward` (flow_lm.py lines 168 to 174); decode steps: `lsd_decode` (lines 20 to 41).

## 5. What to try, cheapest first

Each trial: the 12 in-game lines and his three sheet lines, screened by take_gate.py (England in every window, every word, likeness to p286 within today's 0.65 to 0.80); survivors heard blind beside today's take; first sound timed packaged, near 0.2 s.

1. **Temperature 0.45, 0.6, 0.8** (about 1 h; adds no time). The gate sets the ceiling against drift; a noise clamp may help at the top (unverified).
2. **Recut the p286 clip** from his 16 recordings on F:: liveliest sentences, shortest gaps, the liveliest last, at 10 s and 20 s (1 to 2 h). Still read speech: a small gain at best.
3. **No comma-made full stop** in the first piece (about 1 h with timing).
4. **A bootstrapped lively clip:** 40 spirited lines at 0.6 to 0.8; passing takes he likes by ear become a 10 to 15 s clip (half a day). Sheila's and Ron's clips also came from another TTS. Gate against p286 so drift cannot compound.
5. **One clip per mood** (calm, wary, heated), each stored once as a state (`export_model_state`) and picked by the reply's mood tag; no added time per line, about 12 MB per 20 s clip (worked out from the config, unmeasured). About a day.
6. **Common Voice north-east speakers,** if any exist; the download needs his yes.
7. **A hired north-east actor:** the professional answer, for his page.
8. **Fine-tuning:** at least 100 h of data and a GPU ([training README](https://github.com/kyutai-labs/pocket-tts/blob/main/training/README.md)); out of scope.

## Not reached

- Kyutai's [tech report](https://kyutai.org/blog/2026-01-13-pocket-tts): its body did not load.
- The Common Voice dataset pages did not load, so their terms are unread.
- The licence files of VCTK and OpenSLR 83.
- The licence terms of IViE (Newcastle included) and of EdAcc's own site.
- The Voice-Zero repository and the CosyVoice docs.
- No published measure of Pocket's emotional range, or of how well it holds a north-east accent.

## Fresh review (26 October, evening)

Every source reopened 26 October 2026; the installed package read directly.

**What steers Pocket**
- Clip carries "speaker voice, style, prosody": supported (tts_model.py line 935, not 934); training cuts between two words: supported ([#198](https://github.com/kyutai-labs/pocket-tts/issues/198)).
- Default 0.3 from human evals: supported (english.yaml line 5). 1.0 "More expressive (higher temperature)": supported ([docs](https://kyutai-labs.github.io/pocket-tts/CLI%20Commands/generate/)). In code it only scales per-frame noise (flow_lm.py line 169).
- Temperature moves the voice off the clip: partly. [CALM](https://arxiv.org/html/2509.06926v3) Appendix C measured unprompted voices; the rest is inference.
- No emotion tags: supported ([#52](https://github.com/kyutai-labs/pocket-tts/issues/52) open, Kyutai asks for emotional data; [#15](https://github.com/kyutai-labs/pocket-tts/issues/15) open).
- 30 s truncation, 80 ms pause, every sentence from the clip alone: supported (tts_model.py 1028-1032, 764-765; pocket-server.py 102, 139).
- Comma made full stop: supported, but the first piece would be "Dark coat, moving quick.", not "Dark coat." (voice-server.py 69-71).
- Fine-tuning "at least 100 h": partly; that is the [training README](https://github.com/kyutai-labs/pocket-tts/blob/main/training/README.md)'s general data minimum; it gives no fine-tune figure.

**Licences**
- VCTK CC BY 4.0: supported, licence file now read ([datashare](https://datashare.ed.ac.uk/handle/10283/3443)).
- OpenSLR 83 CC BY-SA 4.0: supported, LICENSE read ([page](https://www.openslr.org/83/)); whether share-alike reaches generated lines is unverified.
- Common Voice CC0: partly. Listings say CC0-1.0, but the [consumer terms](https://mozilladatacollective.com/terms/consumers) need an account, forbid re-identifying contributors, and require model outputs to "not contain personal data" and be labelled machine-made.
- EdAcc CC BY-SA 4.0: supported ([card](https://huggingface.co/datasets/edinburghcstr/edacc)). DECTE research-only: supported ([site](https://research.ncl.ac.uk/decte/)).
- Expresso, EARS non-commercial; Emilia NC with YODAS CC BY 4.0; LibriVox: supported ([Expresso](https://speechbot.github.io/expresso/), [EARS](https://github.com/facebookresearch/ears_dataset), [Emilia](https://huggingface.co/datasets/amphion/Emilia-Dataset), [LibriVox](https://librivox.org/pages/public-domain/)).

**The ranking**
Since measured, temperatures 0.3 to 0.8 change neither pitch range nor length, and all 16 p286 recordings sit at 4.2 to 5.5 semitones, as today's output does. This bears out the note: Pocket copies the clip, a read one. Items 1 and 2 are spent, and item 4 rested on hotter takes being livelier, which they are not.

**Must change before his page**
1. Drop items 1 and 2; rework item 4 around another ship-safe engine with an expression control (unverified) or drop it.
2. Keep item 3 (cheap, phrasing only).
3. Common Voice: an account only he can open and the personal-data clause go to him as a licence question; name the spontaneous set, since the British set is read.
4. The gate's p286 likeness band rejects any new speaker, so items 4, 6 and 7 are identity decisions.
5. Update "Not reached".

**Overall: SOUND WITH FIXES.**

## Measured, and what goes to him (26 October, evening)

Six of Darren's lines (his three sheet lines and three in-game lines) made as the game makes them (tools/voice-live/pocket_delivery_trial.py; F:/LedgerTools/approvals/darren-delivery-2026-10-26), gated by tools/voice-live/take_gate.py, pitch movement measured with pYIN (semitones about each take's median):

| Try | Pitch movement (sd) | Gate |
|---|---|---|
| Today: temperature 0.3, each sentence its own piece | 4.56 | 5 of 6 (line 1 American, as at casting) |
| Temperature 0.45 / 0.6 / 0.8 | 4.73 / 4.37 / 4.55 | 6 / 5 / 5 of 6 |
| p286's own 16 recordings | 4.2 to 5.5 | |
| **Each line spoken whole, 0.3** | **5.18** | **6 of 6** (line 1 passes) |

- **Temperature and the recut are spent** (the reviewer's fix 1): Pocket copies the clip, and every p286 recording is read alike.
- **A finding beyond the note's item 3:** the voice program speaks every sentence as its own piece, each started afresh from the clip, with a pause between ("Alright?" / "Darren." / "You'll have heard of me." / "No?"). None of these six lines was cut at a comma; the cut is at every sentence end. Spoken whole, the same lines move more (5.18 against 4.56), keep their likeness (0.59 to 0.79), and start as fast (first sound 0.17 to 0.20 s, Pocket streams either way). Whether it sounds livelier is for his ear: A (today) against B (whole), blind.
- **Beyond that, only a new reference voice changes the delivery,** and the gate's likeness to p286 rejects any new speaker, so each is his decision: a north-east actor recording a lively reference (money and identity); a Common Voice speaker from its spontaneous set (an account only he can open, and its terms on personal data in outputs: a licence question); or keeping p286's read voice.
