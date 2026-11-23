# The hidden-check harness: short spec

Written 23 Nov 2026 by the checkers session. Code: tools/lane/checkers/hidden.py, tests test_hidden.py (6, no browser). It keeps the one-shot's hidden playthrough checks out of the builder's reach, runs them by separate checkers, and turns their results into the go or no-go after two days.

## What the builder sees and does not see

- Sees: the 41 play stories as prose in the giant prompt, and the test hook's contract (window.LEDGER: read, places, press, tick with LEDGER_MANUAL, saveText and restore, written, rules). It writes its own story tests as it does now.
- Never sees: the hidden checks' code, their off-path variants (another route, another order, another time of day, a save loaded mid-way), their exact numbers beyond the prose, or where they are kept.

## Where the checks live

1. Preferred: a separate private repository (for example jsab258/ledger-checks), attached only to the checkers' sessions with add_repo. A session's GitHub reach is the repositories attached to it, so a builder session that never attaches it cannot read it, and the giant prompt never names it. Creating it is one step for the advisor or main session (the checkers may not create repositories unasked).
2. Until it exists: the checks are written at check time (hour 48) by a fresh checker helper from the story prose alone, so there is nothing to hide in between, and committed to production/lane/checkers/ only after the verdict.
3. Either way, every check file carries a canary line (LEDGER-HIDDEN-CANARY- and 16 hex digits). At the start, `hidden.py manifest` fingerprints the checks and the fingerprint file is committed where the builder can see it: the checkers cannot change a check after seeing the build without it showing (`hidden.py verify`).

## The run, at hour 48 (and nightly if wanted)

1. Pin the builder's commit. Build it outside the repository into its own work folder (variant.py's way); story saves in a folder of their own.
2. `hidden.py leak CHECKS BUILDER_TREE`: a canary or a copied check file in the builder's tree stops the run and is reported as a leak.
3. Run every first-week check twice on the scripted path and twice off it, one browser at a time (two at once on a two-core machine crashed the page twice in this proof). A crashed page is run once more; a second crash counts as "not reached", never as a pass.
4. The machine checks, the clumsy run, the consequence checker and the AI players run beside the checks on the same pinned build.
5. Results go to the private place; `hidden.py redact` gives the builder only story, week, run, pass or fail and what the player met, never the code or the variant.
6. `hidden.py verdict`: go when at least half of the first-week checks really work. A check really works only when all its runs pass, on both runs and on the off-path variant; flaky and path-bound checks count as not working and are listed.

## Tests (test_hidden.py)

A changed, added or missing check is caught; a canary or a copied check file in the builder's tree is caught and a clean tree passes; the redacted record keeps what the player met and drops code, variant and canary; the verdict needs both runs and the off-path variant, names flaky and path-bound checks, ignores later weeks and refuses a go on no checks.
