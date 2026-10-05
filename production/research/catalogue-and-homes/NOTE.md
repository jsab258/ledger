# One home per fact, a catalogue, and checks that fail: the method (5 October 2026)

For phase 0, items 0.4 and 0.5 (PLAN.md; his edits 9 and 10). About twenty minutes. O = opened, S = search summary only, I = inference.

## The method, end to end

1. **One source of truth for each kind of fact.** Every other copy is derived from it and checked against it, never edited by hand. Data-driven game teams keep the canonical data in one file or database and generate the runtime copies (Perforce on SSOT, S; Wikipedia "Single source of truth", S). The project already works this way where it holds: vignette-scene.json is the street's home and vignette-pieces.json is generated from it by CoreTests, which fails when the two drift; the C# Core is the simulation's home and the C++ port is checked against its golden table (I, from the repository).
2. **Checks at the point of entry.** Mature asset pipelines put sanity checks into the export step, so nothing reaches the build without passing them (ixiegaming, "Why game art pipelines break", S). Here: a check in tools/ci-checks.sh, which the commit and the build machine run, failing loudly.
3. **Discoverability.** A catalogue is one of the five pillars of a healthy asset workflow, beside the single source of truth and meaningful versions (artstash, "Essential guide to game asset workflows", S). It must be complete to be trusted, so the check is that every folder of art and research has a line.
4. **Branches.** A branch list is only navigable when old branches leave it; the standard is a policy age (30 days or less), then an archive tag (archive/<name>) pushed before the branch is deleted, so the commits stay reachable and anything can be restored (pullpanda, gitscripts, an atlarge-research issue, S). His rule sets the age at one week.

## What this changes

- CATALOGUE.md holds the homes table, the disagreements found today and a line for every art and research folder; tools/catalogue.py checks it (item 0.5).
- A derived copy that disagrees with its home is a failing check where a script can compare them (the street against the atlas once adopted; the port against the golden table, already), and a listed disagreement where it cannot yet.

## Not reached or not established

No studio's internal catalogue practice was read in full; the sources above were seen as search summaries only. The claim that the existing generated-file checks catch drift is from reading this repository, not from a test written today.
