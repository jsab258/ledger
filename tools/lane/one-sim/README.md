# one-sim: one simulation in the browser

Cloud lane, task 4s, first slice of 19 November 2026. The study and the reasons for the way picked: production/research/lane/ONE-SIM-METHOD-2026-11-19.md. Where the work stands and what is next: PROGRESS.md.

## What this is

The browser prototype is to run the game's real town rules, not its own JavaScript copy. This folder builds that: the game's own C++ town code (ue-probe/Source/LedgerProbe/Public, the Unreal port) compiled to WebAssembly, with a small front door for JavaScript, and tests that hold it to the C# Core, which is the reference.

No town rule lives in this folder. The rules are compiled from where they live. Nothing here writes under ledger/ or ue-probe/.

## What is here

- one-sim.sh: every command (setup, reference, wasm, test, selftest, browser, breaks, all).
- reference/: project files that build the REAL C# Core and its own check programs (PerceptionGolden, Soak, CoreTests) by path, with all output outside the repository. conda_unpack.py unpacks the .NET SDK from conda-forge.
- wasm/one_sim.cpp: the front door. It only calls the port.
- wasm/one-sim.mjs: the loader. A page, a Web Worker or Node imports it. No library needed.
- wasm/checks.mjs: the checks, one copy, run under Node (test_one_sim.mjs) and in a real page (browser/index.html through browser_test.py).
- wasm/selftest.mjs: spoils the table on purpose. The checks must fail.
- wasm/breaks.py: plants one-line breaks in a copy of the port. Do the checks see them?
- wasm/run_wasi.mjs: runs the port's own golden test, compiled to WebAssembly, under Node.

## Run

From the repository root, on Linux:

    tools/lane/one-sim/one-sim.sh setup    # once: .NET SDK 8.0.428 (conda-forge) and wasi-sdk 34 (GitHub), about 320 MB
    tools/lane/one-sim/one-sim.sh all      # about 3 minutes on two processors

Everything large goes to $ONE_SIM_WORK (default /home/claude/one-sim-work). The built one-sim.wasm is about 300 KB and is not committed: it is made from the sources by the script.

## Using it from a page

    import { loadOneSim } from './one-sim.mjs';
    const sim = await loadOneSim(await (await fetch('one-sim.wasm')).arrayBuffer());
    sim.newTown(castJsonText);                 // production/specs/hook-cast.json, as text
    const fields = sim.hour(0, 19, 'mickeys'); // one game hour, in the game's own order
    sim.placeOf('sam', 0, 12);                 // where someone is
    sim.knows();                               // the Ledger's facts: who knows what, and how (saw it or was told)

The full list of calls is in one-sim.mjs. The plain bridge for the prototype (what it calls each tick, what it reads back) is the next run's work.

## Licences

Nothing here is published yet. The parts that would ship inside one-sim.wasm, and the tools, are listed with their licences in the study, section 4. None is on the allowlist yet: the lines are his to add.
