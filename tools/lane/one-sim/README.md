# one-sim: one simulation in the browser

Cloud lane, task 4s, 19 November 2026. The study and the reasons for the way picked: production/research/lane/ONE-SIM-METHOD-2026-11-19.md. Where the work stands and what is next: PROGRESS.md. What the prototype calls and reads back: BRIDGE.md. Where the prototype's own town differs from the real rules, and what the swap changes for the player: DIFFERENCES.md.

## What this is

The browser prototype is to run the game's real town rules, not its own JavaScript copy. This folder builds that: the game's own C++ town code (ue-probe/Source/LedgerProbe/Public, the Unreal port) compiled to WebAssembly, with a small front door for JavaScript, and tests that hold it to the C# Core, which is the reference.

No town rule lives in this folder. The rules are compiled from where they live. Nothing here writes under ledger/ or ue-probe/.

## What is here

- one-sim.sh: every command (setup, reference, wasm, test, selftest, browser, breaks, differences, all).
- reference/: project files that build the REAL C# Core and its own check programs (PerceptionGolden, Soak, CoreTests) by path, with all output outside the repository. The three check programs are built from these lane-written project files, which list the same sources as the originals (ledger/PerceptionGolden, ledger/Soak, ledger/CoreTests). `reference` asks the build tool for both lists on every run and stops if they differ (compare_sources.py). Run 1 also switched on invariant globalisation, which the originals do not have; it was not needed and is removed. The programs therefore need an ICU library on the machine, as .NET on Linux does by default (Ubuntu 24.04 has libicu74). conda_unpack.py unpacks the .NET SDK from conda-forge; zstd-requirements.txt pins the one Python module it needs.
- wasm/one_sim.cpp: the front door. It only calls the port.
- wasm/one-sim.mjs: the loader. A page, a Web Worker or Node imports it. No library needed.
- wasm/one-sim-bridge.mjs: the plain bridge for the prototype, over the loader: its clock in, each hour's doings out, the town in its save (BRIDGE.md). No rule of its own.
- differences/measure.mjs: loads the prototype's own rule files, unchanged, beside the real town and measures three differences (DIFFERENCES.md).
- wasm/checks.mjs: the checks, one copy, run under Node (test_one_sim.mjs) and in a real page (browser/index.html through browser_test.py).
- wasm/selftest.mjs: spoils the table on purpose. The checks must fail.
- wasm/breaks.py: plants one-line breaks in a copy of the port and runs every check on each, the whole table included. Does anything see them?
- wasm/engines_agree.py: compares the town's digest from Node with the one from the real browser (the last step of `all`).
- wasm/run_wasi.mjs: runs the port's own golden test, compiled to WebAssembly, under Node.

## Run

From the repository root, on Linux:

    tools/lane/one-sim/one-sim.sh setup    # once: .NET SDK 8.0.428 (conda-forge) and wasi-sdk 34 (GitHub), about 320 MB
    tools/lane/one-sim/one-sim.sh all      # about 3.5 minutes on two processors

Everything large goes to $ONE_SIM_WORK (default /home/claude/one-sim-work). The built one-sim.wasm is about 420 KB (109 KB to download, compressed) and is not committed: it is made from the sources by the script.

## Using it from a page

    import { loadOneSim } from './one-sim.mjs';
    const sim = await loadOneSim(await (await fetch('one-sim.wasm')).arrayBuffer());
    sim.newTown(castJsonText);                 // production/specs/hook-cast.json, as text
    const fields = sim.hour(0, 19, 'mickeys'); // one game hour, in the game's own order
    sim.placeOf('sam', 0, 12);                 // where someone is
    sim.knows();                               // the Ledger's facts as the town holds them: who knows what, and how (saw it or was told).
                                               // Their details are not yet compared with the C# Core: no golden rows exist for them.

The full list of calls is in one-sim.mjs. The prototype does not call these one by one: it goes through the bridge.

    import { openTown } from './one-sim-bridge.mjs';
    const town = await openTown({ wasm, castJson, startMinute: G.t });   // or { wasm, castJson, saved: G.town }
    for (const hour of town.tick(G.t, area)) { /* who found it, who went to the police, DS Ellis, an arrest, Ada, Ron */ }
    G.town = town.save();                      // the town, as one plain object, for the prototype's save

The prototype's own source is not changed yet. That swap is step 4, a later round through the publish gate.

## Licences

Nothing here is published yet. The parts that would ship inside one-sim.wasm, and the tools, are listed with their licences in the study, section 4. The tools are on the allowlist (item 17, his yes of 19 November). The pieces that ship inside the simulation file are not: that line is held, so nothing with one-sim.wasm inside may be published until the allowlist carries it. The full licence texts are in production/licences/one-sim/.
