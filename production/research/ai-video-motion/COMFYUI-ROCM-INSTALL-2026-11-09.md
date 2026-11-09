# ComfyUI native AMD (ROCm) portable install (9 Nov 2026)

Installed 9 Nov 2026, about 21:17-21:45, on Jafar's instruction of 21:17. Install only: ComfyUI not launched, no GPU work. Nothing outside `F:\LedgerTools\ai-video\comfyui-rocm`; no PATH, registry, driver, SDK or environment change; no install scripts run.

## Sources (read 9 Nov 2026)
- ComfyUI release v0.44.0 (4 Nov 2026), https://github.com/Comfy-Org/ComfyUI/releases/tag/v0.44.0, asset `ComfyUI_windows_portable_amd.7z`, 1,671,700,941 bytes, SHA-256 b9ff564c...fedd28, matching GitHub's published digest. Licence GPL-3.0 (https://raw.githubusercontent.com/Comfy-Org/ComfyUI/master/LICENSE).
- rinsei README, read in full: https://github.com/eviscerations/comfyui-rinsei/blob/master/README.md (last commit 3c7eb9839d, 29 Jun 2026; MIT). It links the "latest" AMD portable and was tested with ComfyUI 0.23.0 on an RX 6700 XT, Python 3.12.10. So v0.44.0 with these wheels is **untested by the README**.
- Index: https://rocm.nightlies.amd.com/v2-staging/gfx103X-all/ (all seven pinned files still present).

## Installed (embedded Python 3.12.10, `pip --force-reinstall --no-deps --index-url <index>`, the README's three commands; pip cache off, temp on F:)
| Package | File (index URL + name) | Download |
|---|---|---|
| torch 2.10.0+rocm7.14.0a20260603 | torch-2.10.0%2Brocm7.14.0a20260603-cp312-cp312-win_amd64.whl | 153 MB |
| torchaudio 2.11.0+rocm7.14.0a20260603 | torchaudio-2.11.0%2B...-cp312-cp312-win_amd64.whl | 0.3 MB |
| torchvision 0.25.0+rocm7.14.0a20260603 | torchvision-0.25.0%2B...-cp312-cp312-win_amd64.whl | 1.7 MB |
| rocm 7.14.0a20260603 | rocm-7.14.0a20260603.tar.gz (built locally) | 19 kB |
| rocm-sdk-core | rocm_sdk_core-7.14.0a20260603-py3-none-win_amd64.whl | 733 MB |
| rocm-sdk-devel | rocm_sdk_devel-7.14.0a20260603-py3-none-win_amd64.whl | 1,784 MB |
| rocm-sdk-libraries-gfx103X-all | rocm_sdk_libraries_gfx103x_all-7.14.0a20260603-py3-none-win_amd64.whl | 239 MB |

Replaced the build's bundled torch 2.9.1, torchaudio 2.9.1, torchvision 0.24.1, rocm and rocm-sdk-core 7.2.1. The bundled `rocm-sdk-libraries-custom` 7.2.1 (1.7 GB) stays; the README does not mention it.

Licences: torch BSD-3-Clause, torchvision BSD, torchaudio BSD (each wheel's METADATA). The four ROCm wheels state no licence in metadata; component files inside are MIT (e.g. `_rocm_sdk_core/share/doc/hipcc/LICENSE.txt`); AMD's build repo TheRock is MIT (https://raw.githubusercontent.com/ROCm/TheRock/main/LICENSE). Per-component licences of the whole SDK: unverified.

## Disk
Install 14 GB (rocm_sdk_devel 7.0 GB, rocm core 2.1 GB, old custom libs 1.7 GB, gfx103X libs 1.1 GB, torch 0.56 GB). Archive and scratch folders deleted after use. F: free now 6.2 GB.

## Check
`python_embeded\python.exe -I -c "import torch; print(torch.__version__)"` gave `2.10.0+rocm7.14.0a20260603` (import only; no device touched).

## Problems
- py7zr cannot open the archive (BCJ2 filter); extracted with Windows' own `tar.exe` (libarchive 3.8.9), nothing installed.
- Not done (outside the instruction): README step 4, `pip uninstall comfy_kitchen -y` (bundled 0.2.40; the README says it breaks every gfx1031 dispatch) and keeping comfy-aimdo (bundled 0.6.0, README tested 0.4.8). Needed before a first run.

## First-run command (not run)
In `F:\LedgerTools\ai-video\comfyui-rocm\ComfyUI_windows_portable`, a cmd window, settings for that window only (README's launch values):
```
set HSA_OVERRIDE_GFX_VERSION=10.3.0
set HIP_VISIBLE_DEVICES=0
set ROCR_VISIBLE_DEVICES=0
set TORCH_BACKENDS_CUDA_FLASH_SDP_ENABLED=0
set TORCH_BACKENDS_CUDA_MEM_EFF_SDP_ENABLED=0
set MIOPEN_FIND_MODE=2
set PYTORCH_HIP_ALLOC_CONF=expandable_segments:True
python_embeded\python.exe -s ComfyUI\main.py --use-quad-cross-attention --disable-async-offload
```
Install log: `F:\LedgerTools\ai-video\comfyui-rocm\pip-install.log`.
