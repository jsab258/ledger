# Workflows retired on 5 October 2026

His order with the new repository: "Retire the two Unity workflows, and check every other workflow for whether it still serves the current game; retire the ones that do not." Kept files here never run (GitHub runs only .github/workflows); history keeps them too.

| Workflow | What it did | Why retired |
|---|---|---|
| ledger-build-windows.yml | the Unity build for Windows (manual) | his order: the Unity builds are legacy since Unreal became the engine on 10 September; its two Unity secrets are not carried over |
| ledger-build-mac.yml | the Unity build for macOS (manual) | the same |
| citypack-fetch.yml | fetched textures and a typeface into the Unity project and committed them | Unity-era; commits pictures and binaries into git, which the push guard now refuses |
| citypack-inventory.yml | inventoried the city pack's sources | Unity-era, part of the same pack |
| citypack-shortlist.yml | shortlisted candidates and committed contact-sheet pictures | Unity-era; commits pictures outside production/previews |
| props-fetch.yml | fetched CC0 model kits into the Unity project and committed them | Unity-era; commits models into git; kits are now fetched to F: on this PC by the asset plan |
| voice-candidates.yml | fetched VCTK voice candidates (July) | voices are cast; the corpus is on F: (vctk-north) |
| tier2-generate.yml | generated character cards with the paid model in development | his ruling of 29 September: no API calls in development |
| ledger-ai-playtest.yml | ran the C# street simulation's fake playtest on Core changes | the cloud Core tests already run the same playtest (tools/ci-checks.sh, playtest-fake) |

Kept: ledger-core-tests.yml (the cloud Core tests: tools/ci-checks.sh), ledger-probe-unreal.yml (the build machine's Unreal build, now refusing anything but text in its commit), and the new ledger-push-guard.yml.
