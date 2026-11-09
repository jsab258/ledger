# Wan 2.2 workflows readable without Civitai or Reddit (read 9 Nov 2026)

Reading only. All pages read 9 Nov 2026 through a summarising fetch tool (JSON values as extracted, not raw text): "as summarised", unverified against the raw file. No synthesis here. Earlier note: WORKFLOW-STUDY-2026-11-09.md (workflows A to G there are not repeated).

## Table

| # | Workflow (link) | Model | Steps / CFG / shift / sampler / scheduler | Frames, size, fps | LoRA | Negative prompt | Licence, date, VRAM stated |
|---|---|---|---|---|---|---|---|
| 1 | ComfyUI template video_wan2_2_5B_ti2v, https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan2_2_5B_ti2v.json (guide https://docs.comfy.org/tutorials/video/wan/wan2_2) | TI2V 5B fp16, umt5 fp8, wan2.2 VAE | 20 / 5 / 8 / uni_pc / simple | 121 frames, 1280x704, 24 fps; Load Image node ships bypassed (text-to-video until re-enabled) | none | Chinese official list (quality, static, extra fingers, malformed limbs, "walking backwards") | Repo MIT (https://github.com/Comfy-Org/workflow_templates); template date not shown; guide: "should fit on 8GB" with ComfyUI offloading |
| 2 | ComfyUI template video_wan2_2_14B_i2v (live, with turbo switch), https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/video_wan2_2_14B_i2v.json | I2V A14B high/low fp8_scaled, umt5 fp8, Wan 2.1 VAE | Turbo off: 20 (split 10) / 3.5 / 5 / euler / simple. Turbo on: 4 steps, CFG 1, split 2 | 81 frames (5 s x 16), 640x640, 16 fps | lightx2v I2V 4-step high and low, strength 1.0 each, active only in turbo | Chinese official list incl. three legs, walking backwards | MIT repo; date not shown; VRAM not stated |
| 3 | I2V 14B template as mirrored by stablediffusiontutorials (older copy), https://huggingface.co/datasets/stablediffusiontutorials/wan-workflows/blob/main/Wan2.2_14B_I2V.json | I2V A14B fp8_scaled pair | 20 (0-10, 10-end) / 3.5 / 8 / euler / simple | 121 frames, 1280x720, 24 fps | none | same Chinese list | licence of the dataset not read: unverified |
| 4 | Kijai WanVideoWrapper I2V A14B example (WIP), https://raw.githubusercontent.com/kijai/ComfyUI-WanVideoWrapper/main/example_workflows/wanvideo_2_2_I2V_A14B_example_WIP.json | I2V A14B fp8 KJ pair, umt5 bf16, Wan 2.1 VAE | 6 total, split 3 / CFG 2 high (schedule), 1 low / shift 8 / dpm++_sde | 81 frames, 704x704, 16 fps; 20 block swaps | lightx2v I2V 480p CFG-distill rank 64: strength 3 high, 1 low | Chinese official list | repo licence not shown on page: unverified; date not read |
| 5 | Kijai WanVideoWrapper 5B I2V example (WIP), https://raw.githubusercontent.com/kijai/ComfyUI-WanVideoWrapper/main/example_workflows/wanvideo_2_2_5B_I2V_example_WIP.json | TI2V 5B fp16 | 30 / 5 / 8 / flowmatch_pusa; EasyCache 0.015, SLG layers 7-9 scale 0.1 | 121 frames, input resized 1024x1024 (size widget 832x480 overridden), 24 fps | none | English translation of the same list | licence unverified; VRAM not stated |
| 6 | Official model cards: https://huggingface.co/Wan-AI/Wan2.2-TI2V-5B and https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B | 5B / A14B | steps, shift, CFG not on the cards | 5B: 720P (1280*704), 24 fps, 5 s clip; A14B: 480P and 720P | none | not on cards | Apache 2.0; 28 Jul 2025 (code and weights); 5B: at least 24 GB (4090) with offload flags, "under 9 minutes" for 5 s 720P; A14B: 80 GB for the single-GPU command |
| 7 | Repackaged files page, https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged | all variants | no settings given | no | lightx2v 4-step LoRAs listed by file name | n/a | Apache 2.0; links to the template JSONs above |

Other Kijai files listed (not read): wanvideo_2_2_5B_I2V_controlnet_example, wanvideo_2_2_Fun_control_camera_example_01, wanvideo_2_2_Fun_control_example_03, wanvideo_2_2_14B_Pusa_extension_example_01, wanvideo_2_2_I2V_A14B_TimeToMove_example (https://github.com/kijai/ComfyUI-WanVideoWrapper/tree/main/example_workflows).

## Camera stillness, full-body framing, foot sliding

- Foot sliding: none of the sources read mentions it (rows 1 to 7).
- Full-body framing: none states a framing recommendation. Row 2's template uses a square 640x640 frame; the official size options are 480P/720P (row 6).
- Camera stillness: no workflow states a still-camera setting. The shared negative prompt (rows 1 to 5) contains "static" and "motionless frame" as things to avoid (the words forbid frozen scenes, not camera motion). A Wan 2.2 Fun Camera tutorial lists a "Static" camera-motion option, 81 frames default (https://docs.comfy.org/tutorials/video/wan/wan2-2-fun-camera.md): seen only in a search result summary, page not read: unverified.
- Snippet-only, not read: Wan 2.2 Animate pose-driven workflows on runcomfy.com ("steady camera ... in the driver clip" advice): unverified.

## Unreached or unread

- https://comfy.icu: no Wan 2.2 workflow pages found by search in this run (the earlier note's page https://comfy.icu/models/1905937/ was read in the earlier note only).
- https://stable-diffusion-art.com/wan-2-2-image-to-video/: HTTP 403.
- https://github.com/Comfy-Org/workflow_templates/tree/main/templates: listing truncated (728 entries omitted); the template files above were read by direct raw URL instead. Template dates and commit history not read.
- Template video_wan2_2_14B_flf2v.json and t2v: not read.
- https://www.comfy.org/workflows/video_wan2_2_14B_i2v-e066a0912cad, https://comfy.org/workflows/03_video_wan2_2_14B_i2v_subgraphed-598da2637dc8/, runcomfy.com and comfyui-wiki.com Wan 2.2 pages: appeared in search, not read.
- https://github.com/kijai/ComfyUI-WanVideoWrapper licence and file dates: not shown.
- Civitai and Reddit (and mirrors): refused earlier, not retried.
