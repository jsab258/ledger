# Kiln round 10, speed: the fixer's brief (drafted 16 Nov 2026, ready to send)

Method researched: FOLDCRAFT-SOLVER-READ-2026-11-16.md (Kiln is processor-only; the vendored ClothCraft carries the hybrid card path, gpu_vbd.rs; FoldCraft's gains came from caching contact data and trimming the candidate list) and KILN-ROUND1-2026-11-13.md rounds 7 to 9 (measure each cost on the real job; one-change tests first).

**Game item it unblocks:** n16-1's M5 and M7. Every garment on the Hook's list is draped several times (pose tests, refits to the cast, reruns after each fix); at 66 to 156 s a job, the drape time sets how many jobs a round can judge. Hours saved: measured by this round, not claimed in advance.

**Send only after:** his answer to the advisor's evaluation sets Kiln's share (Monday 07:40), and the meter allows (RULINGS 7, 10 Nov). Not before 13:00 unless it can finish by 12:55.

## The brief (to one fresh Opus fixer)

1. Goal: the layered job (jacket over jumper, the round 9 judge run) and the jumper job run at least 2x faster with every judge count unchanged or better, by porting the vendored ClothCraft hybrid path (GPU VBD with processor OGC contact, vendor/ClothCraft/src/gpu_vbd.rs, gpu_vbd/, vbd.wgsl, cloth.wgsl) into Kiln's cloth crate behind its existing interface. MIT; credit in Kiln's CREDITS.md.
2. First, a one-change test: build the vendored copy's own GPU bench (gpu_bench.rs) on this PC's AMD card and record whether wgpu picks DX12 or Vulkan and its step time beside the processor path on the same mesh. If the card path is not faster there, stop and report: that is the round's result.
3. Then port; then FoldCraft's contact-data cache and candidate trimming only if the measured contact share of a step is over a third.
4. Rules: no special cases (no code path, setting or number for one garment or job; per-fabric numbers only from presets); the judge (F:/LedgerTools/tool-dev/judge) is never edited or read for its bars beyond bars.json; M1's five old jobs stay byte for byte unless the card path's float order changes them, which is reported, not hidden.
5. Disk and paths: free space by `python tools/retention.py space --job "kiln r10" --drives CF` before any build (F: floor 20 GB); every output path through outpath.py; c_root_guard before and after; builds and outputs only under F:/LedgerTools/tool-dev.
6. Never: simulated mouse or keyboard, computer use, any other app, stopping a process, Unreal, a run between 01:15 and 04:30.
7. Report: the bench result, the two jobs' times before and after (three runs each, median), every judge count, what failed and why, "special cases: none" or what was refused.

Time log: "tool loop: kiln round 10 speed". Review: the judge's counts plus one fresh reviewer only if the drape changes by eye.
