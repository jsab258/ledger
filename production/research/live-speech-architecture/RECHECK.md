# RECHECK: does Chatterbox Turbo keep the exaggeration control, and does it run on AMD

STATUS: SPEC (research recheck). Branch `research/live-speech-architecture`,
added on top of `bf74ec2`. Written 2026-09-19 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item, no decision record, no
code touched.

## 0. Why this file exists, and what opened

Topic 1 ended on two holes it could not close, both because `huggingface.co`
was refused, and it named them as the pair that decides the recommendation:
does Turbo keep `exaggeration`, and does its ONNX export run on DirectML.

Measured this session, not recalled. `huggingface.co` is STILL refused: the
gateway answers 403 to CONNECT, for the site, for `/api/models/...` and for
`cdn-lfs.huggingface.co`, and WebFetch returns `EGRESS_BLOCKED`. So the model
cards named in topic 1 section 8 were not read this time either.

What opened instead is the vendor's own repository through
`raw.githubusercontent.com` (200). Read in full at `resemble-ai/chatterbox`,
branch `master`, on 2026-09-19: `README.md` (15,301 bytes),
`src/chatterbox/tts_turbo.py` (11,379 bytes), `src/chatterbox/tts.py`
(8,924 bytes), `pyproject.toml`, `LICENSE`. This is the vendor's source of
record for the same models. It is not the HuggingFace card, and where the card
might say something different, this file cannot see it.

## 1. Question one: does Turbo keep `exaggeration`? NO. It is accepted and ignored.

From `src/chatterbox/tts_turbo.py`, lines 272 to 291, quoted exactly:

    def generate(
        self,
        text,
        repetition_penalty=1.2,
        min_p=0.00,
        top_p=0.95,
        audio_prompt_path=None,
        exaggeration=0.0,
        cfg_weight=0.0,
        temperature=0.8,
        top_k=1000,
        norm_loudness=True,
    ):
        if audio_prompt_path:
            self.prepare_conditionals(audio_prompt_path, exaggeration=exaggeration, norm_loudness=norm_loudness)
        else:
            assert self.conds is not None, "Please `prepare_conditionals` first or specify `audio_prompt_path`"

        if cfg_weight > 0.0 or exaggeration > 0.0 or min_p > 0.0:
            logger.warning(f"CFG, min_p and exaggeration are not supported by the {self.model_label} version and will be ignored.")

And in `from_local`, line 159, for both Turbo and Nano: `hp.emotion_adv = False`.
`emotion_adv` is the conditioning channel `exaggeration` is written into.

THE ACCEPTING CASE, checked so that this is a difference and not a parameter
that is dead everywhere. `src/chatterbox/tts.py`, the model we actually run,
lines 208 to 230: `generate` defaults to `exaggeration=0.5`, and when the value
changes it rebuilds the T3 conditional rather than warning:

    # Update exaggeration if needed
    if exaggeration != self.conds.t3.emotion_adv[0, 0, 0]:
        _cond: T3Cond = self.conds.t3
        ...
        emotion_adv=exaggeration * torch.ones(1, 1, 1),

The README's model table says the same thing in the vendor's own words.
Chatterbox, 500M: "CFG & Exaggeration tuning". Chatterbox-Turbo, 350M:
"Paralinguistic Tags (`[laugh]`), Lower Compute and VRAM". The control is
listed for the model we run and is absent from Turbo's row.

**This OVERTURNS topic 1's recommendation.** Topic 1 wrote: "A faster model that
cannot do moods is not an upgrade, it is a different decision." It is a
different decision. `game-design/production-plan-audio-art.md:134` records that
chatterbox was adopted "specifically because it exposes an `exaggeration`
control", and the engine decision of 2026-07-28 was taken on the direction test
that control enables.

## 2. Question two: AMD on Windows. Not established, and now less urgent.

The reference implementation's device paths are `cuda`, `cpu` and `mps`, in the
README and in `from_pretrained`. DirectML appears nowhere in the repository
files read. `pyproject.toml` depends on `torch` and `torchaudio` and does not
depend on `onnxruntime` in any form.

The ONNX export topic 1 found, `ResembleAI/chatterbox-turbo-ONNX`, lives on
HuggingFace, which is refused, so operator coverage on the DML execution
provider is exactly as unmeasured as topic 1 left it. The difference is that
section 1 makes the CI run to find out not worth dispatching for Turbo's sake:
topic 1 said to answer the two questions "in this order because the second is
pointless if the first fails", and the first has now failed from a desk.

## 3. What topic 1 did not know exists: Chatterbox-Nano

Not named anywhere in topic 1. From the README, the vendor's words:

> For the most resource-constrained deployments, **Chatterbox-Nano** shares
> Turbo's architecture in an even smaller 110M parameter package. It targets
> on-device and CPU inference, running **3x faster than realtime on 8 CPU
> cores**, while keeping the same single-step decoder and native paralinguistic
> tag support.

It loads through the same class, `ChatterboxTurboTTS.from_pretrained(device=...,
nano=True)`, sets the same `hp.emotion_adv = False` and carries the same
warning, so it is not a route back to the mood control either.

Two cautions on the 3x figure, both mine. It is 8 cores; the development
machine is a Ryzen 5 5600X with 6 (`production/mesh-reports/mesh-machine-report.txt`),
and a per-core rate does not transfer across a core count without measurement.
And it is the vendor's own number with no method attached.

Why it matters anyway: topic 2 found the speech stack is the largest consumer on
a card that is already 3 GB short, and a 110M model running on the CPU takes the
whole speech stack off the card rather than shrinking it.

## 4. One hole topic 1 flagged is now closed

Topic 1, section 5.2: "HOLE: I did not verify that Turbo accepts the same
reference format." It does. Turbo and Nano both clone zero-shot from a
reference clip through the same call shape as the original, the README example
being `model.generate(text, audio_prompt_path="your_10s_ref_clip.wav")`, and
`prepare_conditionals(wav_fpath, ...)` is the same mechanism. The nineteen cast
voices remain reference clips under either model.

## 5. Licence

`LICENSE` at master reads "MIT License / Copyright (c) 2025 Resemble AI", read
in full. The allowlist line for chatterbox is unaffected by anything here.

## 6. What changes

1. **Topic 1's headline recommendation does not survive.** It read "the
   architecture does not need to change, the model probably does". Moving to
   Turbo buys roughly 4x on the chunk decode and costs the property the engine
   was chosen for. That trade is Jafar's to make or refuse, not a free upgrade.
2. **The Turbo DirectML CI run drops down the list.** It was topic 1's second
   of two questions and its own sequencing says the second is pointless now.
3. **Nano is a new and unexamined candidate**, and it is a different shape of
   answer to topic 2's problem than Turbo was: a model that leaves the card
   entirely. It cannot do moods, so at most it is a candidate for barks and
   short reflexive lines, never for the lines `exaggeration` was chosen for.
4. **Nothing here touches the architecture finding.** One thread, strictly
   interleaved, N steps then a chunk decode, settled by a crash, still stands.
   So does topic 1's advice to measure the chunk decode and the LLM leg.

## 7. What still could not be established

1. Anything written on a HuggingFace model card. Refused again, same policy.
2. Whether any Turbo or Nano ONNX export loads and runs on the DirectML
   execution provider on the RX 6700.
3. Any Turbo or Nano speed figure on an RX 6700. The only vendor figure found
   anywhere this session is Nano's CPU-core claim.
4. What the model SOUNDS like without emotion conditioning. I established that
   the parameter is ignored, which is a fact about the code, not about the
   audio. Rule 4 applies and nothing here is a listen.
5. Whether a separate Turbo checkpoint exists with `emotion_adv` enabled. The
   repository read here has one Turbo checkpoint, `t3_turbo_v1.safetensors`,
   and one Nano checkpoint, `t3_nano_v1.safetensors`.

## 8. Sources

Primary, read in full 2026-09-19 through `raw.githubusercontent.com`, at
`resemble-ai/chatterbox` `master`:

- `README.md`
- `src/chatterbox/tts_turbo.py`
- `src/chatterbox/tts.py`
- `pyproject.toml`
- `LICENSE`

Refused this session, named so the next reader does not retry blind:
`huggingface.co` (403 to CONNECT), `www.resemble.ai`, `docs.nvidia.com`,
`onnxruntime.ai`, `github.com` (403; `raw.githubusercontent.com` is the way in).

Repository sources named above were read by topic 1 at `074f85b` and are quoted
from it, not re-read here.
