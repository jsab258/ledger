line: engine and instruments (the 3D generation line, never yet run)
spec: Jafar, 2026-09-21: "The MESH station, which has never run. It is
  wired to the original TRELLIS; the allowlist permits TRELLIS 2 as well,
  and nobody has chosen between them... a ROCm fork of TRELLIS has run end
  to end on a 16 GB AMD card, Hunyuan3D 2.1 runs on AMD via ROCm on
  Windows, and a DirectML port routes the CUDA calls through Microsoft's
  own path. The real limit is memory, around ten gigabytes for shape
  alone, which is exactly my card. Pick whichever route has the best
  chance, TRELLIS 2 included, install it through a dispatched job, and put
  one image through it. Texture generation is expected to fail and does
  not matter... Report the route, what it needed, and the memory it used
  or where it ran out."

  VERIFIED AT FILING TIME: tools/meshgen/README.md's own words, "MESH -
  TRELLIS (microsoft/TRELLIS, MIT) turns that image into geometry. NVIDIA
  only. Never yet run by anyone on this project," and its trellis-backend
  requirement list (16 GB VRAM, CUDA toolkit, MSVC) is written against
  Jafar's actual card, an AMD Radeon RX 6700 with 9.98 GB and no Visual
  Studio, which the README itself names as CANNOT RUN. The allowlist
  (ledger-v2/research/license-allowlist.md, ship-safe row 2) already
  permits "TRELLIS/TRELLIS 2 (MIT)," so no new licence decision is needed
  to choose between them, only the choice itself, which this item makes
  by running one.

  HUNYUAN3D IS ON THE NEVER-SHIP LIST (license-allowlist.md, never-ship
  row 3: territory-excluded licence, Switzerland plus likely EU reach
  treated as banned). Jafar names it in the same breath as a route that
  has run on AMD; that is evidence about which routes are technically
  possible on his card, not an instruction to ship its output. Nothing
  produced by a Hunyuan3D route may pass the licence gate; if that route
  is the one tried, say so plainly and do not tag its output as ship-safe.

  The README's own authorising mechanism: a decision record citing the
  weights licence, carrying "TOOL-DECISION: <tool>" alone on its own line
  at column 0, is required before a TRELLIS-family output may ship
  (ship_ok=false otherwise). This item is a FIRST RUN to measure the route
  and the memory ceiling, not a ship decision; note in the report whether
  a TOOL-DECISION marker for the chosen route already exists, and if not,
  that ship_ok stays false regardless of how the run goes.
acceptance: one route is chosen from among TRELLIS, TRELLIS 2, the ROCm
  TRELLIS fork, Hunyuan3D 2.1 via ROCm, or a DirectML port, named with the
  reason it was picked; the install is run through a dispatched job, not
  by hand on Jafar's own machine outside the job system, and the job's own
  log is the evidence; one image is put through the MESH stage; and the
  report states, each as a printed reading rather than a guess, whether it
  ran to completion or where it stopped, the memory used or the point it
  ran out of memory, and whether texture generation, expected to fail,
  failed as expected or did something else worth naming
max_sessions: 2
status: READY 2026-09-21, filed with the visual slice's order. Runs in
  parallel with the slice, behind it on the runner. Needs a dispatched job
  on Jafar's PC per .claude/rules/ci.md's expensive-job rule; if no PC
  runner slot is free behind the slice and the other measurements, this
  item waits for one rather than running in the container, where the
  probe already reads CANNOT RUN. This is this week's work.
