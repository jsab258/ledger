# FoldCraft solver read, 16 Nov 2026 (item n16-1)

Method researched: DISCUSSIONS-2026-11-14.md (the community scan that named it, 14 Nov) and KILN-ROUND1-2026-11-13.md round 9 (the first read, 14 Nov); read 16 Nov 2026.

Questions
1. Licence file and copyright line at HEAD; other-licence code inside.
2. GPU solvers, what each solves, CPU path.
3. Source of the claimed speed, with the repo's own timings.
4. How layers are kept apart; whether a crossing is repaired.
5. AMD / Windows / backend choice; vendor-specific code.
6. How garment and body enter; closeness to the vendored ClothCraft.
7. Reusable pieces ranked for speed and layer separation.
8. Not reached.

Base: https://github.com/NicTanghe/FoldCraft, HEAD fcd319ad0814045b8454405ccd9299c1bb8b9462, 15 Nov 2026 ("Merge pull request #52", source: https://api.github.com/repos/NicTanghe/FoldCraft/commits/HEAD, read 16 Nov). Raw files read through a page-reading tool that summarises, so line numbers below are approximate (marked ~) and quotes are as returned by it; none read by hand line by line. All dates read: 16 Nov 2026.

## 1. Licence
- File `LICENSE`: "MIT License", "Copyright (c) 2026 erythrofr and ClothCraft contributors" (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/LICENSE).
- THIRD_PARTY_NOTICES.md (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/THIRD_PARTY_NOTICES.md) lists:
  - `src/cosserat.rs`: MIT, "Copyright 2025 Jerry Hsu" (its own notice must travel with that file; not a solver Kiln needs).
  - `assets/makehuman/base.obj` (and derived mannequin.obj, measurements.json): CC0 (MakeHuman). No MakeHuman program code.
  - `experiments/box3d`: Box3D keeps its own MIT; not vendored.
  - Rust dependencies keep their own licences (resolved by Cargo.lock; not individually checked: unverified).
  - A GPL repo (YarnBall GPU) is named as "not incorporated".
- No GPL code found in the listed notices. The notices file is the only source checked; a source-by-source licence scan was not done (unverified).

## 2. Solvers
Tree: https://api.github.com/repos/NicTanghe/FoldCraft/git/trees/HEAD?recursive=1. README: https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/README.md.
- Default desktop GPU solver: WGSL "finite AVBD / Jacobi pipeline with a squared-distance IPC-style barrier". Files: `src/gpu_avbd.rs`, `src/gpu_avbd/{main,solve,contact,coupled,jet,al}.wgsl`, `packing.rs`, `profile.rs`. Integrator: simultaneous Jacobi solve of an implicit Euler target (gravity and mass-proportional damping), a device-side global Armijo test, plus a coupled Gauss-Newton/PCG correction (8 linear iterations per sweep). Membrane, bending and sewing are finite-stiffness energies; hard joints not implemented; pins remove degrees of freedom. Contact: IPC-style barrier B(d) = -(k r²/8)(s-1)² log(s), s = d²/r², plus a step bound so the whole linear update keeps positive clearance; no friction, no full CCD, no canonical deduplication. (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/docs/wgsl-avbd-ipc.md)
- Experimental variant: `ContactMethod::BarrierAl` (same backend, augmented-Lagrangian barrier).
- Hybrid: CPU OGC contact + GPU VBD (`src/gpu_vbd.rs`, `gpu_vbd/*.wgsl`, `src/vbd.wgsl`, `cloth.wgsl`). Colour-by-colour VBD dispatches: 1 + iterations x colours per step; subgroup reduction only if subgroup size is exactly 32, else a portable reduction (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/src/gpu_vbd.rs, ~l.96-115).
- CPU path: VBD with OGC contact (`src/vbd.rs`, `src/ogc/*`, flag `--cpu`); double-precision Newton reference (`--reference`, `src/solver.rs`); research adapters in `src/solver_lab/` (headless only).
- The vendored ClothCraft already has `src/gpu_vbd.rs` and `gpu_bench.rs` (local glob). It has no `gpu_avbd*`, no `vbd.wgsl` check made (unverified). So the hybrid GPU VBD is already in Kiln's base; the resident AVBD/IPC solver is the new piece.

## 3. Where the speed comes from
Source: https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/docs/wgsl-performance.md and gpu_avbd.rs.
- Data kept on the card: yes. `resident: RefCell<Option<Resident>>`; eight storage buffers and a uniform, reallocated only if method, garment pointer, pins, faces, edges or grab changes; positions re-uploaded only if input differs from last accepted state (gpu_avbd.rs ~l.300-340). One readback per accepted step ("One accepted-state readback serves CPU consumers; no iteration readback"), one encoder, one submit, one compute pass.
- The document itself says "Residency alone does not establish a speedup". The measured gains came from: contact data (normal, weights, curvature) frozen once per sweep and reused in each PCG product; material records cut from 208 to 144 bytes; scalar energy evaluation; candidate list cut from about 40,500 to 9,850 by a support-axis filter.
- Published timings (one machine: Apple M1 Pro, Metal 4, two CPU threads, 2454-vertex T-shirt; background and clocks not controlled): IPC 547.59 -> 166.36 ms for 20 draped steps (3.29x); assembly 245.30 -> 115.04 ms. Hybrid CPU-OGC/GPU-VBD control 16.13 ms for the same 20 draped steps: "about 10x faster" than the resident GPU solver. The repo claims no dense-garment speedup. Quality gate: RMS position difference from CPU 4-5 mm; a 200-step test took 115 s including the CPU control.
- Reading: the repo's own numbers show its resident solver slower than its hybrid on that machine. Not reproduced here; nothing run.

## 4. Layers
- No layer ids, no per-layer offsets. `OgcWorld::new(x, triangles, moving, excluded)` takes one triangle list; vertices below `moving` are cloth, the rest fixed (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/src/ogc/world.rs, ~l.202-229). Seams use an exclusion-pair set. OgcSettings radius: "Offset radius in metres. This is a contact shell, not material thickness", default 0.003 (~l.62-74); relaxation must stay below 0.5 (~l.66, l.89). In the AVBD document, thickness appears only in the Project sphere ("radius includes half the material thickness").
- Repair: none. `validate_start` rejects an initial crossing: "OGC initial intersection between faces ... reset/rearrange before simulating" (~l.449) and touching/coplanar features (~l.460). README: protections "do not repair initial intersections".
- Kiln's own `ogc/world.rs` has a three-layer test with 3 mm spacing (local, l.1013-1028), so the same keep-apart mechanism is already there.

## 5. AMD, Windows, backend
- gpu_avbd.rs: `wgpu::Instance::new(InstanceDescriptor::new_without_display_handle())`, `PowerPreference::HighPerformance`, CPU adapters refused, only TIMESTAMP_QUERY requested (~l.137-150). No `Backends::` choice, no DX12/Vulkan named anywhere read. Cargo.toml: wgpu 30.0.1, no explicit features (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/Cargo.toml). Which API wgpu picks on Windows is wgpu's default (unverified here).
- No vendor branches (Apple, NVIDIA, AMD) in gpu_avbd.rs or gpu_vbd.rs. Only hardware-dependent code: subgroup path needing min and max size 32 (AMD may report 64 or 32 depending on mode; unverified). README says Windows is the main development platform. No AMD run is reported in anything read; measured data is Apple only.
- Package name is "marvelous-cloth" in Cargo.toml (same as Kiln's cloth crate name, noted only).

## 6. Interfaces
- Garment: `VbdSolver::new(garment: Arc<CompiledGarment>, avatar: Option<&SurfaceMesh>, state: &State) -> Result<Self, String>` and `step(&mut self, state, &VbdSettings, Option<&Grab>) -> Result<VbdMetrics, String>` (https://raw.githubusercontent.com/NicTanghe/FoldCraft/HEAD/src/vbd.rs, ~l.186, l.350). GPU: `GpuAvbd::step(&self, solver: &mut VbdSolver, state, settings, grab)` and `ProjectAvbd::step(project, mesh, state)`; `request_device()` makes the device.
- Body: static OBJ or glTF/GLB avatar (README "Files"); animated avatars unsupported.
- Closeness: the vendored copy (commit 16761c55600342334a2fd585c80f9fe811c2b20c, packed-refs) has the same `VbdSolver::new/step` and `VbdSettings` (vbd.rs l.24, l.181, l.345 vs FoldCraft l.24, l.186, l.350; Kiln's copy l.27, l.191, l.374, so Kiln has edited it). A full diff was not done; sizes of signatures only (unverified beyond that). `GpuAvbd` takes the same `VbdSolver` and `State`, so the entry is near-compatible in shape.

## 7. Reuse candidates (all MIT; keep LICENSE copyright line and notice)
Ranked by likely gain; effort figures are guesses.
1. Contact and candidate filtering ideas from the residency work (frozen per-sweep contact cache, support-axis candidate filter, 40,500 -> 9,850): applies to CPU too if Kiln's drape loop re-evaluates contact each iteration. Gain unknown. Effort guess: 1-3 days.
2. Hybrid path already vendored (`gpu_vbd.rs`): the repo's own data shows it as the fastest of its backends (16 ms per 20 draped steps vs 166 ms). Check whether Kiln's 144-156 s job uses it. Effort guess: hours to confirm.
3. Whole `gpu_avbd` backend: self-contained but the repo's numbers show it slower than hybrid; has no layer support beyond the shared OGC world. Gain for Kiln doubtful. Effort guess: 3-6 days incl. AMD testing.
4. Layer separation: nothing new to take; FoldCraft has no layer model and no crossing repair. Kiln already holds the same OGC world. A repair step would have to be written fresh.

## 8. Not reached
- No reproduction, no timings on AMD or Windows, nothing run or cloned (by rule).
- Raw WGSL shaders, docs/ogc.md, docs/reports/wgsl-residency/report.pdf, and the file-by-file diff against the vendored copy: not read this pass.
- wgpu 30's default backend list on Windows: not looked up.
- Dependency licences (Cargo.lock): not scanned.
- Tool used summarised files rather than returning raw text; quoted lines come from its extracts, line numbers approximate.

## The session's check (16 Nov, 06:5x)

Kiln's own cloth crate runs the solve on the processor only: its Cargo.toml says the GPU and editor parts were not ported (F:/LedgerTools/tool-dev/kiln/cloth/Cargo.toml line 19), though the vendored ClothCraft carries the hybrid GPU VBD path (gpu_vbd.rs). So the largest speed lever for Kiln's drape runs (about 144 to 156 s on the layered job) is porting the vendored hybrid path, with FoldCraft's contact cache and candidate trimming as the second; both are MIT, reuse with notice. Neither is measured on our AMD card yet: the first speed round measures the hybrid on the layered job before anything is kept.
