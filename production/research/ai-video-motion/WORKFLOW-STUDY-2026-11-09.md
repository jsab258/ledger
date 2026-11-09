# Wan 2.2 image-to-video workflow study (read 9 Nov 2026)

Item n09-8. All pages read 9 Nov 2026 through a summarising fetch tool (not raw text), so every figure is "as summarised": unverified against the raw page. Reading only; nothing installed or run.

## Not reached (listed, not used)
- Civitai (https://civitai.com/models/1819263 and every Civitai page): HTTP 403. No Civitai download or like counts exist in this note. A third-party Civitai mirror turned up in search and was not used.
- Reddit (r/StableDiffusion search): fetch refused. A Reddit mirror (reddit.zackpollard.pro) failed on TLS. Upvote counts: none.
- Not read: sd-cli's own `-h` output (running a tool for its help is barred); flags below not in the docs are unverified.
- The aim of 6 to 10 popular community workflows was not met: five workflow settings sets plus two community recipes are below. The popularity ranking the brief asked for could not be made.

## 1. Workflows and recipes read

| # | Source (link) | Author | Popularity | Model and quant | Sampler / sched / steps / CFG / shift | Size, frames, fps |
|---|---|---|---|---|---|---|
| A | Wan2.2 official config, https://raw.githubusercontent.com/Wan-Video/Wan2.2/main/wan/configs/wan_i2v_A14B.py and wan_ti2v_5B.py; repo https://github.com/Wan-Video/Wan2.2 | Wan-AI | 18.5k stars | I2V A14B high/low, TI2V 5B, full precision | A14B: 40 steps, CFG 3.5 (both), shift 5.0, boundary 0.900. 5B: 50 steps, CFG 5.0, shift 5.0. Sampler not in excerpt | 5B: 121 frames, 24 fps. A14B 480P/720P; frames, fps not in excerpt. 80 GB card for the single-GPU command |
| B | ComfyUI I2V A14B template as mirrored, https://huggingface.co/datasets/stablediffusiontutorials/wan-workflows/blob/main/Wan2.2_14B_I2V.json; template guide https://docs.comfy.org/tutorials/video/wan/wan2_2 | Comfy / mirror by stablediffusiontutorials (mirror may differ from the live template: unverified) | no figure | fp16 high and low; text encoder fp8 | KSamplerAdvanced x2: euler, simple, 20 steps (high 0 to 10, low 10 to end), CFG 3.5, shift 8 | 1280x720, 121 frames, 24 fps; no LoRA |
| C | Wan2.2-Lightning I2V 4-step, https://huggingface.co/lightx2v/Wan2.2-Lightning and https://github.com/ModelTC/Wan2.2-Lightning | lightx2v / ModelTC | 640 likes, 100 downloads last month (HF); 319 stars (GitHub) | A14B with I2V 4-step LoRA rank 64 (V1, 7 Aug 2025) | 4 steps, no CFG trick; the T2V model card advice (maintainer, Aug 5 2025): Euler, shift 5, CFG 1 | not stated |
| D | Smooth Workflow Wan 2.2 v5.0 (19 Apr 2026), https://huggingface.co/Sentinel7/wan/commit/1794d5148ce16b4664eacc2dca9e948be48376de (a Hugging Face copy of the Civitai README) | DigitalPastel | 11 likes on the copy; downloads not shown | I2V A14B; text encoder umt5 fp8 scaled; Wan 2.1 VAE; Q6_K named for GGUF in search only | 6 steps (3+3) low-end, 10 steps (5+5) high-end; CFG, shift, sampler not stated; NAG on, said to make the negative prompt work at CFG 1.0 | 480x720 then 2x Lanczos to 960x1440; 81 frames; 30 fps (README inconsistent, says 25 elsewhere); loops 5 s at most; first-to-last-frame workflow included |
| E | Wan 2.2 14B i2v t2v Lightx2v Enhanced Motions v2, https://comfy.icu/models/1905937/Wan-2-2-14B-i2v-t2v-Lightx2v-Enhanced-Motions | author not listed | not shown | I2V A14B high and low, GGUF Q5_0; umt5 Q4_K_M GGUF | 4 steps high + 2 low = 6; "CFG++" named, no value; sampler, shift not stated | image scaled to about 0.25 megapixels; 16 GB VRAM advised; author says 5 to 7 min per render; RealESRGAN and FILM doubling the frame rate after |
| F | "3-sampler" recipe, https://huggingface.co/lightx2v/Wan2.2-Lightning/discussions/20 (8 Aug 2025) | bicio78ita | 6 likes on the comment | A14B high/low with lightx2v | Sampler 1: high noise, CFG 3.5, no LoRA, 1 to 4 steps. Sampler 2: high, CFG 1, LoRA 2.0. Sampler 3: low, CFG 1, LoRA 0.7 | thread: 1280x720 looked normal, 960x544 slightly slow, 832x480 slow motion (Sikaworld1990) |
| G | Strength recipe, https://huggingface.co/lightx2v/Wan2.2-Lightning/discussions/5 (5 Aug 2025) | Aorora12 | not shown | A14B with lightx2v | LoRA 0.6 to 0.8 high, 1.0 low; CFG 2 to 3.5 high, 1 low; 8 steps (4+4). Reported "noticeably better motion". Failed try: shift 5, strength 1.0 both, Euler, CFG 1, "very blurry" | not stated |

Not all of these are "most used": only A, C and the LoRA repos below carry a count read directly. Community ratings from Civitai and Reddit are missing (see above).

## 2. LoRAs and licences
| LoRA | Link | Licence (page) | Popularity | Note |
|---|---|---|---|---|
| Wan2.2-Lightning (I2V NFE4 V1, T2V V1.1) | https://huggingface.co/lightx2v/Wan2.2-Lightning | Apache 2.0 | 640 likes | maintainers: limits with very large motion |
| Wan2.2-Distill-Loras (I2V high and low rank 64, 4-step) | https://huggingface.co/lightx2v/Wan2.2-Distill-Loras | Apache 2.0 | 110,152 downloads last month, 290 likes | high-noise one "more creative, diverse", low-noise "more faithful to the input"; step list [1000, 750, 500, 250] |
| Slow-Mo Fix (I2V high and low) | https://huggingface.co/rzgar/Wan2.2_I2V_LightX2V_Slow-Mo_Fix | Apache 2.0 | 4 likes, about 6,047 downloads last month | strength 1.0 both, 4 steps; the author made it because the default ComfyUI I2V LightX2V LoRAs "tend to make scenes look like slow motion"; the 260412 variant is rank 128 extracted from lightx2v's Distill-Models. Base-model claim: its own, no benchmark |
| Kijai Lightx2v folder (rank 4 to 256) | https://huggingface.co/Kijai/WanVideo_comfy/tree/main/Lightx2v | not shown on the page: unverified | none shown | I2V 480p rank files exist (54 MB to 2.9 GB) |

The Apache 2.0 repos are not on the project allowlist; any adoption needs a decision record (TOOLS note, license-allowlist rule).

## 3. What the authors say about feet, weight, limbs, drift
No source read says anything about feet, weight transfer, limbs or drift. The only motion statements read: the slow-motion complaint (discussions #5 and #20: "kills the motion", "live wallpaper"; I2V LoRA better than T2V but "still worse than the 40-step base"; resolution matters; 832x480 slow in one report), and Lightning's own note on artifacts with extreme motion. DigitalPastel says to keep clips at 5 s or under. Official config negative prompt (read via mirror B, Chinese) lists deformed limbs, extra or fused fingers, three legs, crowded backgrounds, walking backwards.

## 4. What stable-diffusion.cpp can reproduce
From docs/wan.md (https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/wan.md, read 9 Nov 2026):
- TI2V 5B, I2V A14B and FLF2V A14B all supported, safetensors or GGUF; the A14B models run as a low-noise and high-noise pair: `--diffusion-model` takes the low, `--high-noise-diffusion-model` the high. Separate `--high-noise-steps`, `--high-noise-cfg-scale`, `--high-noise-sampling-method`.
- Flags found: `--flow-shift`, `--cfg-scale`, `--sampling-method`, `--steps`, `--offload-to-cpu`, `--vae-tiling`, `--vae-tile-size`, `--temporal-tiling`, `--extra-tiling-args`, `--lora-model-dir` with `<lora:name:weight>` tags, `--init-img` and `--end-img`, `-i`, `--video-frames`.
- A14B example: cfg 3.5, euler, 10 steps of which 8 high-noise, flow shift 3.0, Q8_0 GGUF, `--offload-to-cpu`. Two-model LoRA example: lightx2v 4-step with the `|high_noise|` tag form, 4 + 4 steps, CFG 3.5. The page says the lightx2v lightning LoRA at CFG 1.0 works for S2V (low-noise file only there; the high file "produces artifacts" on S2V only).
- Not on the page or in examples/cli/README.md (https://github.com/leejet/stable-diffusion.cpp/blob/master/examples/cli/README.md, read 9 Nov): a boundary or `--moe-boundary` setting (could not confirm: the high/low switch is probably set by the step counts), `--scheduler` choices, NAG, negative-prompt guidance beyond `-n`, `--fps`. All unverified.
- Reproduction by workflow: A (shift 5, 40 steps, CFG 3.5): shift, cfg, steps settable; euler assumed. B: two-pass with step split settable via the high-noise options; scheduler "simple" unverified. C, F, G: LoRA tags and per-model weights are possible; the 3-sampler recipe (three passes, LoRA on the second only) is not reproducible: sd.cpp has two stages, not three. D: NAG not found: cannot reproduce; the lightx2v CFG 1 path with `-n` having no effect would be the substitute. E: "CFG++" not found. First-and-last frame: A14B FLF2V only (documented); not documented for TI2V 5B.

## 5. Would I2V A14B Q4 GGUF fit 10 GB VRAM and 32 GB RAM?
- Size, https://huggingface.co/QuantStack/Wan2.2-I2V-A14B-GGUF (read 9 Nov 2026; 1,120,771 downloads last month, 460 likes, Apache 2.0): Q4_0 8.56 GB, Q4_K_S 8.75 GB, Q4_1 9.26 GB, Q4_K_M 9.65 GB (Q8_0 15.4 GB). The page lists one table; it is not stated whether this is per expert. Two experts are needed, so about 17 to 19 GB of weights, plus umt5 Q8 6.04 GB and the VAE, about 25 GB in all if all are resident.
- One 8.6 GB expert does not fit beside activations in 10 GB; `--offload-to-cpu` moves weights out of the card between use. Whether sd.cpp holds both experts in RAM, and the peak, is not documented: unverified. 32 GB looks tight but plausible (about 25 GB of weights, Windows and the process on top). The VAE decode on this card already ran out of memory at 33 frames and needed tiling (TOOLS note); A14B uses the Wan 2.1 VAE, which the docs call very memory-hungry (TAE option).
- Time: unmeasured. Estimate only: about 2.8 times the per-step compute of the 5B (14B against 5B active), but a lightx2v 4-step run is 4 steps instead of 20. Order of the TI2V figure (about 59 min for 81 frames) is not a guide; A14B time must be measured.
- Verdict: possible on paper, unproven; the only way to know is the A/B run.

## 6. Comparison with this PC
Current: TI2V 5B Q8, cfg 6, euler, shift 3, 20 steps, 480x832, no LoRA, no NAG, `-n` negative prompt, 24 fps assumed (TOOLS and SHOTS notes).
- Differences from the official numbers: the 5B official config is shift 5, 50 steps, CFG 5 at 121 frames (A). The PC's shift 3, cfg 6 follow sd.cpp's example, not Wan's config. Shift and steps are the cheapest things to align (shift raised toward 5; steps 20 against 50 is a cost trade).
- Resolution: the slow-motion thread links low resolution with slower motion in A14B (832x480 slow, 1280x720 normal; Sikaworld1990). 480x832 is at the low end. Unverified for the 5B.
- None of the workflows addresses foot planting; the PC's own test (feet planted at 33 frames) is the only evidence.

## What changes in SHOTS-AND-PROMPTS (motion 2, 81 frames)
1. Run settings, 5B: raise flow shift from 3 to 5 as one variable (official shift 5), keep cfg 6 only if shift is the sole change; log it. Keep 20 steps (time).
2. Turn VAE tiling and temporal tiling on from the start (`--vae-tiling --vae-tile-size` and the temporal option the 5B example uses); replace the deprecated `--diffusion-fa` with `--flash-attn off,diffusion=on`.
3. Prompt: the first clip turned the whole body. Describe the head alone ("his body stays leaning against the wall; only his head turns"), with the weight shift as a separate earlier sentence. Add "walking backwards", "three legs", "static" is not wanted; official negatives such as "extra or fused fingers, deformed limbs, three legs" can be added; keep "camera movement" bans.
4. Frame count: 81 stays; the sources say 5 s at most (D) and the official 5B default is 121.
5. A/B, same start frame, same seed 1101, same 81 frames, same 480x832, same prompt and negative:
   - Arm A: TI2V 5B Q8 as above (shift 5).
   - Arm B: I2V A14B Q4 GGUF (Q4_K_M if memory allows, Q4_0 otherwise) high and low pair, `--high-noise-diffusion-model`, cfg 3.5, euler, flow shift 3 (the docs' own A14B value), 20 steps with the high-noise share about half (official boundary 0.9 is by timestep; sd.cpp's split by steps, a choice), `--offload-to-cpu`, tiling on, umt5 Q8, Wan 2.1 VAE, CLIP vision file for I2V per docs.
   - Optional arm C only if B is too slow: B with the Apache-2.0 Distill-Loras (I2V, both strengths 1.0) or Slow-Mo Fix, 4 + 4 steps, cfg 1 to 1.5; record the licence in a decision record first.
   - Record per arm: seconds, peak RAM and VRAM, whether it finished, and the motion-2 checks (drift under 2 px, glance happens, weight shift, feet). Stop at the first out-of-memory failure of B and record it; no third try without a yes.
