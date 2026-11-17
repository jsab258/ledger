# If the PC dies: how LEDGER comes back

One page (advisor 197, his pick of 17 November 2026). What comes from where, in order. "Sign-in" marks what needs Jafar's own account; nothing here needs money. The backup's rules: it never deletes, never overwrites, never copies keys, and MetaHuman files never go to GitHub.

## 1. The three sources
- **GitHub** (the repository, branches main and wip): every script, tool, spec, record, ruling, research note, the game's code and its text and small files, previews. Clone it to C:/Users/Jafar/ledger-local.
- **Dropbox**, folder "LEDGER backup" (sign-in: his Dropbox): the approved cast's MetaHumans (Tom, Ron, Sheila, Darren: source assets and built folders) and their voices; the project they are rebuilt in; the bodies, garments and approvals; Kiln's source and records plus kiln.bundle, Kiln's whole history (`git clone kiln.bundle kiln`); F:/LedgerTools/game-inputs (what the night build reads beside the repository); the judge folder. Changed files sit beside the old under versions/<date-time>/.
- **Downloads again**: the rest is fetched, never backed up.

## 2. Order
1. Windows account, then Git, Python (miniconda), the GitHub CLI; clone the repository.
2. Dropbox (sign-in), let "LEDGER backup" sync; check with `python tools/backup-to-dropbox.py --verify`.
3. Epic Games Launcher and Unreal Engine 5.8 (sign-in: Epic), with its MetaHuman parts.
4. Copy back from Dropbox: the cast project to F:/LedgerTools/mh-dress (and C:/LedgerTools/mh-assemble from it), bodies and garments, game-inputs, the judge folder; clone Kiln from kiln.bundle to F:/LedgerTools/tool-dev/kiln.
5. Fab library items (sign-in: Epic/Fab): Epic's MetaHuman garments, Megascans, anything his library lists. Megascans and Epic's samples are re-downloaded, never backed up.
6. Programs he installed (sign-in each): Marvelous Designer (CLO account), Houdini (SideFX), Cascadeur; Blender 5.2 portable (free download) to F:/LedgerTools/blender52.
7. Rebuildable without sign-in: Python environments (from the tools' requirements), the voice engines in use (Pocket TTS for Sheila and Ron, the Nano voice for Darren: public weights), Hugging Face models, Rust builds of Kiln and Loomwright (`cargo build --release`), Unreal's caches and the build machine (re-registered on GitHub: sign-in).
8. Keys are never in any backup: the router and API keys, his GitHub token and the published Mafia key are set again by hand (his accounts).
9. Run `bash tools/ci-checks.sh`, then a packaged build, before any work.

## 3. What is lost if the PC dies today
- Anything uncommitted and not yet on the night's backup (at most a day).
- Run outputs, renders, review pictures, caches: working files, remade by rerunning.
- Study extracts of other games: re-extracted from his installed games.

Checked by: the weekly restore check (`python tools/backup-to-dropbox.py --restore-check`, about 20 files restored and compared by SHA-256) and the 26-hour staleness line (`--stale`) in the hourly row.
