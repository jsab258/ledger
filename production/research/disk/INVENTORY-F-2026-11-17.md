# F: storage inventory, 17 Nov 2026 (read-only; nothing changed)

Measured 17 Nov 2026 about 13:00 local with a .NET walk (sum of file bytes, 1 GB = 10^9, links not followed). Newest write = newest file mtime in the tree. Readers = grep of tools/, ledger/, ue-probe/Config and Source, .github/, retention.json, HANDOVER.md, CLOTHES.md, TOWN.md, needs-you/items.json and the Kiln/judge sources on F: for the folder path (1571 files read); "Dropbox" = path named in production/specs/in-game.json "backup" or "backupAlso".

## Totals

- F: total 119.5 GB, used 84.4 GB, free 35.0 GB (volume figures, `shutil.disk_usage`). The rows below add to 86.0 GB of file bytes.
- Shelf totals (top-level LedgerTools folders): lasting 43.2 GB, tools 22.7 GB, working 20.1 GB, not-LEDGER 0.0 GB (vuze, $RECYCLE.BIN, System Volume Information: unread, see Unread). F:/town-* (0.08 GB, Sep) are old town work, working, outside the sum.
- Remove/shrink candidates: 17.4 GB in all, 13.3 GB of it protected in retention.json (needs his yes); none needs his sign-in to get back (list at the bottom).
- Since 16 Nov: free 22.4 to 35.0 GB; gate/new 13.2 to 5.4 GB; GameAnimationSample (5.6 GB) gone.

## Questions answered

- mh-dress (21.2 GB, last write 7 Nov): still read. About 17 tools/ue scripts launch `UnrealEditor.exe F:/LedgerTools/mh-dress/MHAssemble.uproject` (cloth_graph_probe, export_dcc, import_anim, make_builds, make_cloth_garment, speech_faces and others); tools/ue/link_candidates.py reads Content/Ledger/MetaHumans; tools/garments_shipped_check.py reads Content/Ledger/MetaHumans/Garments; make_cast_metahumans.py cites preset-coeffs.json. Garments are imported into C:/LedgerTools/mh-assemble now, but the approved cast MetaHumans live here (Cast 9.9 GB, Ledger 9.5 GB of which MetaHumans 8.6 GB, Fab 0.45 GB). Shelf lasting, keep. Rebuildable parts only: Saved 0.15 GB, Intermediate 0.14 GB, DerivedDataCache 0.014 GB (Unreal makes them again).
- gate/new (5.4 GB now): the 32 folders the 17 Nov clear-out list marked "may go" are no longer there; what remains is the list's "stays" set (office 1.07 GB, look 0.61, brick-flemish 0.50, tom-outfit 0.43, chandler-joinery 0.39, chandler-wear 0.36, street-level 0.26, tom films 0.45, 17 Nov n16-5 frames about 0.4). Superseded now: nothing certain; office could be thinned by hand (note's own words).
- The game's voice: ue-probe CrimeProbe.cpp starts "the voice server beside the game" (tools/voice-live/voice-server.py). That script runs Chatterbox Nano from C:/LedgerTools/chatterbox-nano (Darren) and Pocket TTS from F:/LedgerTools/pocket-tts/env with weights in F:/LedgerTools/hf/hub (Sheila, Ron; its default Python path is F:/LedgerTools/pocket-tts/env/Scripts/python.exe). F: voice-portable is the same voice packed for the friends' build (make_portable.py). parler-tts, voice-graphs, voice-env-export are casting or research leftovers, not the game's path.
- Python setups and model caches: see the rows for pocket-tts, voice-portable, parler-tts, voice-env-export, bpyenv, pylib, uv, garmentcode-lab, hf, voice-graphs, models and accent-id.

## Top-level LedgerTools folders (largest first)

| Folder | GB | Newest write | Readers (top 1-3) | Protected | Refetch | Shelf | Proposal | Dropbox |
|---|--:|---|---|---|---|---|---|---|
| mh-dress | 21.2 | 2026-11-07 | link_candidates.py, speech_faces.py | yes | Content: approved cast, not refetchable; Intermediate/Saved/DerivedDataCache rebuilt by Unreal | lasting | keep (rebuildable parts shrink, see below) | yes (Cast uassets, Ledger/MetaHumans/MH_LenaS4, RoccoP2, SamS6, uproject, init_unreal.py) |
| garments | 7.1 | 2026-11-16 | jeans.py, regression_jobs.json | yes | unique made work (garments tom 5.8 GB largest) | lasting | keep | yes |
| gate | 6.5 | 2026-11-17 | street_wear.py, a_board_face.py | yes | made by LEDGER runs; approved pictures also copied under production/approvals | working | keep; gate/new now 5.4 GB, all of it from the 17 Nov keep list (the 7.7 GB clear-out has been done) | no |
| played-game | 6.5 | 2026-11-17 | nightly_walk.py, retention.json | yes | rebuilt by the packaged build workflow | working | keep (the played build; limit: latest two) | no |
| parler-tts | 5.5 | 2026-09-24 | retention.json, longer_takes.py | yes | Parler model is public (Hugging Face parler-tts-mini-v1; a second copy sits in C: HF cache); env rebuildable by pip | tools | shrink: hf-cache 3.5 GB duplicates the C: copy; env 2.0 GB used only by casting tool longer_takes.py. Protected: needs his yes | no |
| voice-portable | 4.4 | 2026-11-07 | make_portable.py, portable_test.py | yes | rebuilt by tools/voice-live/make_portable.py (python 1.35 GB, nano 3.0 GB weights from Resemble Chatterbox Nano, public) | tools | keep (friends build voice, nothing installed) | no |
| slr83 | 3.8 | 2026-09-29 | cleanup.py, retention.json | yes | public OpenSLR dataset 83 (re-download; exact URL unverified) | lasting | shrink candidate: 3.8 GB, newest write 29 Sep (file dates 2019), only tools/cleanup.py names it; protected: needs his yes | no |
| game-inputs | 3.8 | 2026-11-17 | cmu_ue_retarget.py, cmu_measure.py | yes | inputs made or fetched for the game; mixed (cmu-* 0.3 GB are 17 Nov run outputs; gasp 1.5 GB Epic sample, Fab = his sign-in) | lasting | keep | no |
| uv | 3.1 | 2026-11-13 | retention.json | yes | rebuilt by uv from PyPI | tools | shrink: cache 2.95 GB is over its 2.5 GB cap (retention.json); `uv cache prune` is safe | no |
| voice-env-export | 2.3 | 2026-10-26 | retention.json | yes | unknown (an exported Python env; no requirements file seen) | tools | remove candidate: 2.25 GB, no reader, no write since 26 Oct; protected: needs his yes | no |
| aaa-study | 2.0 | 2026-11-06 | retention.json | yes | game extracts re-made from C:/Games with FModel and the key in F: keys (kcd2, mafia 1.75 GB); study notes small | lasting | shrink candidate: kcd2 + mafia extracts 1.75 GB, no write since 28 Oct, CLAUDE.md says extracts go once numbers are recorded; protected: needs his yes | no |
| tool-dev | 2.0 | 2026-11-17 | retention.json, run_prune.py | yes | Kiln tool sources and runs; runs rebuilt by rerunning jobs; judge protected | working | keep (runs 1.0 GB governed by retention limit) | no |
| fab | 1.8 | 2026-11-02 | import_fab_clothes.py, retention.json | yes | Epic/Fab content: needs his sign-in | lasting | keep | no |
| bodies | 1.4 | 2026-11-17 | job-result.json, job-result.json | yes | unique approved bodies | lasting | keep | yes |
| voice-graphs | 1.4 | 2026-10-06 | nano_step_graph.py, off_card.py | yes | rebuilt by tools/voice-live/nano_step_graph.py (needs C: chatterbox-nano) | tools | keep (research item; 6 Oct last write, has a reader) | no |
| hf | 1.2 | 2026-11-17 | retention.json, voxcpm_takes.py | yes | public Hugging Face models (whisper-small.en, ecapa, accent-id, pocket-tts, flan-t5) | tools | keep (pocket-tts here is the game voice weights) | no |
| texture-tools | 1.1 | 2026-11-12 | import_crate_test.py | no | made by LEDGER runs | working | keep | no |
| pylib | 1.1 | 2026-10-08 | none found | no | pip --target dir for lettucedetect (public, PyPI); named by no path | tools | remove candidate: 1.05 GB, no path reader (tools/checkers/measure_checkers.py imports lettucedetect), no write since 8 Oct | no |
| lab | 1.0 | 2026-10-22 | none found | no | made by the lab side session (clothes, jacket, sash, door); unique work: unknown | working | remove/shrink candidate: 0.99 GB, no reader, last write 22 Oct; check with him before any delete | no |
| blender52 | 1.0 | 2026-11-17 | regression_jobs.json, heldback_jobs.json | yes | public Blender 5.2.2 portable | tools | keep | no |
| approved-cast-2026-09-25 | 1.0 | 2026-09-25 | retention.json | yes | approved, not refetchable | lasting | keep | no |
| tool-tests-2026-11 | 0.9 | 2026-11-17 | job-result.json, job-result.json | no | rerun the test jobs; limit: tool test and Kiln run outputs | working | keep (limit covers it) | no |
| bpyenv | 0.9 | 2026-10-21 | front_for_game.py, kit_stain.py | no | Python env for Blender recipes; requirements file not found: unknown | tools | keep (3 art recipe readers) | no |
| pocket-tts | 0.8 | 2026-10-30 | voice_load.py, voice-server.py | no | pip env (pocket-tts public, Kyutai); rebuildable from its package | tools | keep: the game voice engine for Sheila and Ron | no |
| polyhaven | 0.7 | 2026-11-08 | wood_trim.py, verify_display_sources.py | yes | public CC0 Poly Haven downloads | lasting | keep | no |
| garmentcode-lab | 0.6 | 2026-11-11 | pleated_skirt.py, TROUSERS-METHOD-2026-11-16.md | no | GarmentCode src public; venvs rebuildable by pip | tools | shrink: venv (0.26 GB) older duplicate of venv-1109 | no |
| sw-scratch | 0.5 | 2026-10-24 | none found | no | made by LEDGER runs (shop windows, scratch); rerun unknown | working | shrink candidate: 0.54 GB, no reader, last write 24 Oct | no |
| checkers | 0.5 | 2026-11-03 | name_rule.py, Source.cs | no | made by LEDGER runs; rebuildable by tools/checkers scripts | working | keep (readers: tools/checkers) | no |
| tmp | 0.3 | 2026-11-17 | play.py, voice_load.py | no | scratch, 7-day limit | working | keep (limit covers it) | no |
| dotnet10 | 0.2 | 2026-10-25 | retention.json | yes | public Microsoft .NET 10 | tools | keep | no |
| town-scratch | 0.2 | 2026-11-16 | Program.cs, measure_checkers.py | no | made by LEDGER runs (bench/arm folders from 30 Sep) | working | shrink candidate: 0.17 GB, 76 old bench folders, last write 16 Nov in one small folder | no |
| drapestudio-test-2026-11-11 | 0.1 | 2026-11-11 | none found | no | rerun | working | remove candidate: superseded by -final (protected) | no |
| saved-branches-2026-10-05 | 0.1 | 2026-10-05 | retention.json | yes | saved git branch results | lasting | keep | no |
| ast-grep | 0.1 | 2026-11-16 | CREDITS.md | no | public ast-grep release | tools | keep | no |
| approvals | 0.1 | 2026-10-26 | retention.json | yes | approved pictures and films, not refetchable | lasting | keep | yes |
| models | 0.1 | 2026-09-25 | retention.json, take_gate.py | yes | public speaker model (speechbrain) | tools | keep | no |
| accent-id | 0.1 | 2026-09-25 | accent_check.py, retention.json | yes | public ecapa source | tools | keep | no |
| drapestudio-test-2026-11-13-final | 0.1 | 2026-11-13 | regression_jobs.json, retention.json | yes | rerun | working | keep (named in regression jobs, protected) | no |
| blender_mcp | 0.1 | 2026-09-29 | retention.json | yes | public Blender MCP source | tools | keep | no |
| dotnet10-download | 0.1 | 2026-10-25 | none found | no | public Microsoft download | tools | remove candidate: 0.08 GB leftover installer beside the installed dotnet10 | no |
| atlas-01-2026-09-22 | 0.1 | 2026-09-22 | retention.json | yes | approved concept sheets | lasting | keep | no |
| retention | 0.1 | 2026-11-17 | retention.json, retention.py | yes | LEDGER retention logs | tools | keep | no |
| vctk-north | 0.1 | 2026-09-29 | retention.json | yes | public VCTK voice samples | lasting | keep | no |
| reference-other-games | 0.0 | 2026-09-23 | portrait_sheet.py, attribution-check.py | yes | reference frames, not refetchable | lasting | keep | yes |
| old small work (under 0.06 GB each) (36 folders) | 0.4 | 2026-11-17 | mostly none (md-jobs, nightly, renders have one script each) | partly | mixed made-by-runs or reference; none read | working | keep, later look; total tiny | no |

## Second level: largest and decision-relevant rows only (word cap); every other L2 folder is under 0.1 GB, or equals its parent's row above (fab, garments, game-inputs, texture-tools, pocket-tts, hf, bodies, voice-portable, voice-graphs, sw-scratch, lab, played-game)

| Path | GB | Newest | Note |
|---|--:|---|---|
| mh-dress/Content | 20.9 | 7 Nov | lasting keep; Cast 9.9, Ledger 9.5, Fab 0.45, Builds 0.06; Dropbox yes for the 3 Cast uassets and 3 built MetaHumans folders (Ledger/MetaHumans/MH_LenaS4, MH_RoccoP2, MH_SamS6) |
| mh-dress/Saved, Intermediate, DerivedDataCache | 0.15, 0.14, 0.014 | 7 Nov (DDC 24 Sep) | shrink: rebuilt by Unreal; Dropbox no |
| gate/new | 5.4 | 17 Nov | working, see above |
| parler-tts/hf-cache | 3.5 | 24 Sep | shrink candidate (public model, C: copy exists) |
| voice-portable/nano | 3.0 | 6 Nov | keep, rebuilt by make_portable.py |
| uv/cache | 2.95 | 13 Nov | shrink to 2.5 GB cap |
| voice-env-export/Lib | 2.25 | 26 Oct | remove candidate |
| parler-tts/env | 2.0 | 24 Sep | shrink candidate |
| slr83/male, scottish_male, female | 1.25, 0.95, 0.47 | 29 Sep | shrink candidate (public OpenSLR) |
| pylib/lettuce | 1.05 | 8 Oct | remove candidate |
| tool-dev/runs, kiln | 1.0 | 17 Nov | working, retention limit |
| aaa-study/kcd2, mafia | 0.97, 0.78 | 28 Oct | shrink candidate (re-extract from C:/Games with the key) |

Small folders (under 0.1 GB each) are summed in their parent row; polyhaven (170 folders, 0.48 GB) and town-scratch (76 folders) are the many-folder cases.

## Unread and unmeasured

- F:/vuze (not LEDGER's, du says 0 MB), F:/$RECYCLE.BIN and F:/System Volume Information: not opened; sizes unreadable or zero. F:/LedgerTools/keys: skipped on purpose (size and date only: one subfolder mafia-usmap, newest 25 Oct; not listed in the sums).
- Unknown: whether lab holds unique work; requirements of bpyenv and voice-env-export; slr83's exact source; why file bytes (86.0) exceed volume used (84.4).
- Reader search is by path text only.

## Remove and shrink candidates (none is mh-dress itself)

| Candidate | GB | Protected (his yes) | Back from |
|---|--:|---|---|
| parler-tts (hf-cache 3.5 + env 2.0) | 5.48 | yes | public Hugging Face + pip; C: copy of the model exists |
| slr83 | 3.82 | yes | public OpenSLR 83 (exact link unverified) |
| voice-env-export | 2.25 | yes | unknown (no requirements file seen) |
| aaa-study kcd2 + mafia extracts | 1.75 | yes | re-extract from C:/Games (needs FModel and the key in F: keys; no sign-in) |
| pylib/lettuce | 1.05 | no | pip install lettucedetect (public) |
| lab (clothes, jacket, sash, door, talk, tmp) | 0.99 | no | unknown: may be unique; ask him first |
| sw-scratch | 0.54 | no | unknown |
| uv/cache over its cap | 0.45 | yes (uv is protected) | PyPI by uv |
| mh-dress Saved + Intermediate + DerivedDataCache | 0.30 | partly (Content only is protected) | Unreal rebuilds |
| garmentcode-lab/venv | 0.26 | no | pip |
| town-scratch (LedgerTools 0.17 + F: town-* 0.08) | 0.25 | no (ci-tree inside is protected) | made by LEDGER runs, unknown if rerunnable |
| drapestudio-test, -2026-11-11, -2026-11-13 | 0.16 | no | rerun; -final is protected and stays |
| dotnet10-download | 0.08 | no | public Microsoft |

Totals: 17.4 GB; protected rows 13.3 GB, unprotected 4.1 GB. Needing his Fab/Epic sign-in to get back: none (GameAnimationSample, which did, is already gone). Approved, bought and unrefetchable folders (mh-dress Content, garments, bodies, approvals, approved-cast, fab, reference-other-games, game-inputs, gate) all stay.
