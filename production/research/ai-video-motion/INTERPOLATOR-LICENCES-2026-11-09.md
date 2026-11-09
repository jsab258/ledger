# Interpolator licences, read 2026-11-09

## Questions
1. rife-ncnn-vulkan: code licence; licence of each bundled model folder (rife-v4.6 and later), traced to RIFE / Practical-RIFE and any model card.
2. FILM (google-research/frame-interpolation) and IFRNet (ltkong218/IFRNet): code and weights licences.
3. Does any forbid commercial use of outputs or weights, or impose an attribution duty?
4. Windows Vulkan build released by the author: version and date.
5. Is any listed in ledger-v2/research/license-allowlist.md?

## Answers
0. Allowlist: searched for rife, film, ifrnet, interpol (case-insensitive); no match. None listed (read 2026-11-09). Each needs a line added by whoever owns the list.
1. rife-ncnn-vulkan code: MIT, Copyright (c) 2020 nihui (LICENSE read). README states no licence for the models. Its table maps folders to upstream versions (rife 1.2 ... rife-v4 4.0, rife-v4.6 4.6); no folder newer than v4.6 is listed on the README page. Upstream: ECCV2022-RIFE LICENSE is MIT, Copyright (c) Megvii Inc. Practical-RIFE LICENSE is MIT, Copyright (c) 2021 hzwer; its README says the trained-model downloads "are under the same MIT license as this project". The v4.6 model weights therefore trace to MIT (Practical-RIFE statement); no separate model card was found. Whether the ncnn-converted copies carry their own notice: unverified (repository model folders not opened).
2. FILM: code Apache-2.0 (LICENSE read). The README gives no licence for the saved models (Google Drive download); unverified, treat as undetermined. Repo archived read-only 14 Oct 2025. README says "not an officially supported Google product". IFRNet: code MIT, Copyright (c) 2022 Lingtong Kong (LICENSE read). README gives no weights licence (Dropbox link); unverified.
3. No source read forbids commercial use of code, weights or outputs. Duties: MIT (all of RIFE, ncnn code, IFRNet) needs the copyright and permission notice kept with copies or substantial portions. Apache-2.0 (FILM) needs the licence copy, change notices, and NOTICE-file content if one exists. Citation requests (RIFE paper, FILM, IFRNet) are requests, not licence terms. Outputs (frames) are not addressed by any licence read. Practical-RIFE also names SAFA and credits SVFI, with no licence term attached.
4. Author's releases (github.com/nihui/rife-ncnn-vulkan/releases): latest tag 20221029 (29 Oct 2022; adds CPU temporal TTA for RIFE v4). Others 20220728, 20220330, 20220318, 20220313, 20220303 (v2.3 default), 20220228 (v2.3, v4 added), 20210520, 20210516, 20210227. README says Windows/Linux/MacOS executables exist; the asset file names and which models each zip holds (is v4.6 inside?) did not load: unverified. The README table lists v4.6, so the latest build probably includes it (unverified).

## Sources (all read 2026-11-09)
- https://github.com/nihui/rife-ncnn-vulkan and /releases, raw .../master/LICENSE
- https://github.com/hzwer/Practical-RIFE and raw .../main/LICENSE
- https://github.com/hzwer/ECCV2022-RIFE and raw .../main/LICENSE
- https://github.com/google-research/frame-interpolation and raw .../main/LICENSE
- https://github.com/ltkong218/IFRNet and raw .../main/LICENSE
- C:\Users\Jafar\ledger-local\ledger-v2\research\license-allowlist.md

## Not reached / not done
Release asset file names; model folders inside the repo and zips; the Google Drive and Dropbox model pages; any model card; the ncnn repo's NOTICE-type files. No download made. Pages were read through a summarising fetch tool, not raw reading by eye, so licence texts are as summarised (treat as moderately confirmed).

## Recommendation
RIFE via rife-ncnn-vulkan (MIT code, MIT-stated v4.x weights) is the cleanest candidate; ship the MIT notices. Hold FILM and IFRNet weights until their licence is confirmed from the Drive or Dropbox page or the author; add RIFE and ncnn to the allowlist only after the model-folder and release asset check.
