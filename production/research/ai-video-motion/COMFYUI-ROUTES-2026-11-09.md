# ComfyUI routes for the RX 6700 (gfx1031) (9 Nov 2026)

All pages read 9 Nov 2026 (read through a fetch tool that summarises the page; GitHub file listings were not read line by line, so scripts' contents beyond install-n.bat are unverified). No install or download made.

## Correction to TOOLS-2026-11-09.md
That note read AMD's `https://rocm.nightlies.amd.com/v2/` and found no torch for gfx103X. Re-read 9 Nov: `/v2/gfx103X-all/` lists only ROCm SDK packages (no torch), but `https://rocm.nightlies.amd.com/v2-staging/gfx103X-all/` lists torch, torchvision, torchaudio and triton (package names only; wheel versions not shown by the fetch). So the earlier finding was true of `/v2/` only. Both sides below.

## Q1. patientx/ComfyUI-Zluda (https://github.com/patientx/ComfyUI-Zluda)
- Windows-only fork of Comfy-Org/ComfyUI using ZLUDA. Its README says it is superseded by a newer project, comfyui-rocm (below).
- Licence: GPL-3.0 (LICENSE read at raw.githubusercontent.com/patientx/ComfyUI-Zluda/master/LICENSE). ZLUDA (https://github.com/lshqqytiger/ZLUDA, the fork used): Apache-2.0 or MIT, dual.
- gfx1031: README lists the RX 6700/6700 XT in the "VEGA through 6700" group: HIP SDK 6.2.4 (not 6.4.2, which it calls untested for that group). Supported by the README.
- README steps (RDNA2 group): install Git, Python 3.11.9+ (3.12 for Triton; not the Store version), VC++ runtime, VS Build Tools, AMD driver above 25.5.1; install HIP SDK 6.2.4; set system variables HIP_PATH and HIP_PATH_62 to `C:\Program Files\AMD\ROCm\6.2\`, add its `bin` to PATH; extract the "HIP SDK extension" (ZLUDA 3.9.5) into the ROCm 6.2 folder; replace the rocBLAS `library` folder with the gfx1031 pack (backup first; source named: likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU v0.6.2.4); restart; `git clone https://github.com/patientx/ComfyUI-Zluda`, `cd ComfyUI-Zluda`, `install-n.bat`. Antivirus may flag a dummy `nccl.dll`.
- What `install-n.bat` runs (read in full, raw file, master branch): makes a venv; upgrades pip; `pip install -r requirements.txt`; replaces torch with torch 2.7.0, torchvision 0.22.0, torchaudio 2.7.0 from `download.pytorch.org/whl/cu118`; unpinned onnxruntime; numpy 1.26.4; a Triton 3.4.0 wheel from github.com/lshqqytiger/triton releases (Python 3.11 or 3.12 only); unpinned pypatch-url, then two patches from raw.githubusercontent.com/sfinktah/amd-torch (applied to triton and torch); sageattention 1.0.6 plus three patched files from the repo; git clones of patientx/CFZ-SwitchMenu, ltdrdata/ComfyUI-Manager and sfinktah/ovum-cudnn-wrapper; copies Python's `libs`; downloads ZLUDA nightly `ZLUDA-nightly-windows-rocm6-amd64.zip` (lshqqytiger release rel.5e717459...) with curl and unpacks it; renames the ZLUDA DLLs over torch's cublas/cusparse/nvrtc/cufft DLLs; sets MIOPEN and FLASH_ATTENTION env vars; launches `zluda.exe -- python main.py --use-quad-cross-attention`.
- Wan: README ships a Wan 2.2 i2v workflow (Kijai wrapper) in `cfz/workflows`; says Wan runs faster with fp16 VAE (cfz-vae-loader node); tiled VAE for Triton/MIOpen errors at decode; cuDNN toggle node for VAE errors. No speeds given.

## Q2. RYZENNAVI repos
- comfyui-zluda-gfx1031 (https://github.com/RYZENNAVI/comfyui-zluda-gfx1031): archived, moved to rdna2; 0 stars, 6 commits; MIT.
- comfyui-zluda-rdna2 (https://github.com/RYZENNAVI/comfyui-zluda-rdna2): 2 stars, 0 forks, 21 commits, one anonymous account. Scripts MIT; the kernel packs it fetches are GPL-3.0 and not redistributed. States tested only on RX 6950 XT and RX 6700 XT (HIP 6.2 on gfx1031; torch 2.7.0+cu118, Python 3.11.9). It needs a working ComfyUI-Zluda first. Fixes it lists: ZLUDA/HIP major version mismatch (0xC0000135), ZLUDA DLL names in torch\lib, mem-efficient attention resetting the driver, comfyui.bat overwriting comfy\zluda.py, missing gfx1031 rocBLAS kernels; says cuDNN need not be disabled. Downloads (Install-Kernels.ps1, via 7-Zip) the first matching pack from likelovewant/ROCmLibs-for-gfx1103-AMD780M-APU and brknsoul/ROCmLibs; no version pin, no hash.
- Are they unnecessary? The main README already covers the rocBLAS library replacement by hand (same likelovewant source). So the kernel fix is documented upstream; the rest of these repos is unverified extra with very low trust (2 stars, anonymous). Not recommended as a dependency; the manual rocBLAS step does the same.

## Q3. Issue #430 (https://github.com/patientx/ComfyUI-Zluda/issues/430)
Opened 2 Feb 2026 by Kaichi34, still open: "GET was unable to find an engine to execute this computation" in FaceDetailer / VAE decode on RX 6700 XT, persisting with TRITON_OVERRIDE_ARCH=gfx1031. The log shows a cuDNN conv2d failure (not Triton). Owner's reply 3 Feb: disable cuDNN around that node, as is done for VAE encode and decode. No confirmation that it fixed it. Related: the README's cuDNN-toggle node and tiled VAE; a closed issue #232 (same message, closed 24 Mar 2026). A forum summary also cites the maintainer suggesting `--cpu-vae` for end-of-run VAE memory failure (search result, unverified).

## Q4. comfyui-rinsei (https://github.com/eviscerations/comfyui-rinsei; README at /blob/master/README.md)
- MIT. 4 stars, 4 commits, one user. Native ROCm (no ZLUDA) on Windows, tested on RX 6700 XT 12 GB only; other gfx103x unverified.
- Steps: take the official ComfyUI AMD portable build (Comfy-Org releases); pip-install `torch==2.10.0+rocm7.14.0a20260603`, torchaudio 2.11.0, torchvision 0.25.0, and `rocm`, `rocm-sdk-core`, `rocm-sdk-devel`, `rocm-sdk-libraries-gfx103X-all` (same date tag), all `--no-deps` from `https://rocm.nightlies.amd.com/v2-staging/gfx103X-all/`; uninstall comfy_kitchen, install comfy-aimdo; launch with HSA_OVERRIDE_GFX_VERSION=10.3.0, `--use-quad-cross-attention --disable-async-offload`. Custom nodes (GGUF, KJNodes, VideoHelperSuite, Wan22FMLF) by Manager or git. Nightly wheels may be removed from the index over time (unverified; the pinned build is 5 months old).
- Known failures it lists: async offload crash (0xC0000005), fp8/safetensors models need comfy_kitchen and crash (use GGUF), fp8 CLIP fails, SageAttention unsupported, old `gfx103X-dgpu` index has broken gfx1031 kernels, cold MIOpen cache about 4x slower first run.
- Related: https://github.com/patientx/ComfyUI-Zluda/issues/435 (open; read 9 Nov): experimental ROCm/PyTorch builds for all gfx103X; reports working on RX 6750 XT, 6650 XT, 6700 XT, 6600 XT; SD1.5 about 1.70 it/s on a 6700 XT; some users had corrupt wheels, VAE OOM stutter, wrong GPU picked (set HIP_VISIBLE_DEVICES), Sage OOM. Maintainer there points to comfyui-rocm.

## Newer main route: patientx-cfz/comfyui-rocm (https://github.com/patientx-cfz/comfyui-rocm)
GPL-3.0, 405 stars, 26 forks, 6,924 commits (landing page, 9 Nov). Windows, AMD's ROCm/PyTorch wheels, lists RDNA2; the author tested only an RX 6800; no gfx1031 note. Steps: Git, VC++ runtime, VS Build Tools (C++), unzip the latest release to a drive root, `install.bat`, launch `comfyui-user.bat`. Release comfyui-rocm-101026 (10 Oct). Release notes: a 17 Jun build switched gfx103x from a shared package to per-GPU builds; dynamic VRAM "runs better on RDNA2". Includes tested Wan 2.2 i2v workflows. The installer script and the release asset names/sizes were not read (README raw URL 404; assets not shown): what it downloads is unverified. The lowest-risk path to read first.

## Q5. Reported Wan runs on a 6700-class card
- Only direct report: rinsei README (above), RX 6700 XT 12 GB, native ROCm, GGUF Q3_K_M (6.7 GB): Wan 2.2 I2V, split attention, 480x832, 17 frames, about 28 s/step (warm); 352x608, 33 frames, about 25 s/step; quad attention 240-480 s/step; cold cache up to about 1,075 s/step. The author's own claim; no independent reproduction found. Q4_K_S and Q5_K_M ran out of memory at 480x832 on 12 GB. These are 14B-class GGUF figures (5B not stated). This card has 10 GB, so even these are not transferable (unverified).
- No report found for Wan on ZLUDA with any 6700-class card. Nearest: RX 6800 via ZLUDA, a 1 s clip took 19 min, model unnamed (https://huggingface.co/Zarxrax/removetext/discussions/1).
- Linux, not these routes: RX 6650 XT 8 GB, ROCm 5.6, Wan 2.2 i2v 120 steps 480x480 about 30 min (https://reddit.sentinel-team.org/posts/1s6vojw/snapshots/2026-04-03T21%3A13%3A18.877582Z).
- Comparison: our current route took 1,300 s for 33 frames at 480x832 (TOOLS note).

## Opposite search (evidence against)
- Same Reddit thread: a 6700 XT user on Linux ROCm 7.2: SVD OOM, AnimateDiff noise; commenters called Wan 5B "not happening" on 12 GB (opinion, not a test).
- ZLUDA issues #430 and #232 (decode error, cuDNN) for gfx1031; ZLUDA on RDNA2 needs HIP 6.2.4 plus a hand rocBLAS swap.
- rinsei: crashes unless async offload is off; fp8/safetensors unusable.
- Searches for "gfx1031 Wan 2.2 ZLUDA" found no success report and no refusal; absence is not proof.
- Search found no failure report for the v2-staging gfx103X-all route beyond those listed.

## Q6. Disk on C: (none documented; estimates unverified)
- ZLUDA route: HIP SDK 6.2.4 on C (AMD page not read; several GB, unverified) plus venv with torch cu118 (about 3-5 GB, unverified), ComfyUI, Triton. Models reuse current GGUFs by pointing at them.
- rinsei / comfyui-rocm: ROCm SDK wheels plus torch wheels (several GB, unverified; no sizes seen). ComfyUI can be placed on F: (install location is a free choice in all READMEs; READMEs say a drive root, not Program Files). Only the ZLUDA route forces files into `C:\Program Files\AMD\ROCm`.
- Caches (MIOpen, Triton, ZLUDA) grow under the user profile (unverified).

## Q7. Option facts (no choice made here)
1. comfyui-rocm release: GPL-3.0, active, large community; gfx1031 untested by the author; read its install.bat before running (not read).
2. rinsei steps: fully listed above, one-person repo, pinned nightly wheels; the only documented Wan speed on this card class; runs only downloads from Comfy-Org, AMD, PyPI, Hugging Face.
3. Main ComfyUI-Zluda steps: fully documented, supports gfx1031, bigger install footprint on C, many unpinned and patched pieces (list under Q1).
Reporting only: none of the one-click RYZENNAVI scripts is needed for route 3.

## Not reached
- raw README of comfyui-rocm (404); its install.bat and release assets (not shown).
- Wheel filenames and sizes on the AMD indexes (names only).
- AMD HIP SDK download page and sizes; Reddit and other threads beyond those linked.
- The README of ComfyUI-Zluda was read as a summary; install-n.bat as raw file.
