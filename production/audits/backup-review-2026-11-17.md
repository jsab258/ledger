# Backup review, 17 Nov 2026 (tools/backup-to-dropbox.py, 4ceebeec0 plus the uncommitted manifest)

Real backup and sources only read: `--selftest` 26/26; `--dry-run` DRY-RUN copied=1 unchanged=10144; `--verify` NOT-WHOLE notWhole=391. Attacks: importlib on fake temp folders, deleted after. Python 3.12.8.

## Breaks

1. **Junction inside a listed folder copies its target, keys included (d, high in principle).** os.walk follows junctions; refused() reads path text only. Fake `game-inputs\k` junction to fake `LedgerTools\keys`: `backupToDropbox=OK copied=2`, key in backup: True. A junction to an ancestor loops. None in listed folders today.
   Fix: skip entries where islink or isjunction; run refused() on realpath.
2. **refused() is case-sensitive, its list narrow (d, high).** Passed: `LedgerTools\Keys\`, `LEDGERTOOLS/KEYS/`, `Secrets.json`, `AESKEYS.json`, `api_key.txt`, `API-KEY.txt`, `token.txt`, `github_token`, `id_rsa`, `credentials.json`, `anthropic.key`, FModel's `AppSettings.json`.
   Fix: lower-cased realpath; add token, credential, id_rsa, .pem, .key, api_key, FModel settings.
3. **Backup folder as a junction writes outside Dropbox, reported OK (c, medium).** islink() is False for junctions; inside() measures against realpath(dest). Fake case: OK copied=2, files in `elsewhere`.
   Fix: refuse if isjunction(dest) or realpath(dest) is not under realpath(DROPBOX).
4. **Same-minute runs overwrite a version (b, medium-low).** Stamp has minute resolution; copy2 lands on an existing versions file. Fake test: v2 replaced by v3, v2 lost.
   Fix: never copy onto an existing path; add seconds or a counter.
5. **stale() fooled (g, medium-high).** Ten nights DEFERRED gave (False, 7.0); `bundle=FAILED backupToDropbox=OK` counts good; a future stamp gives -1025 h. C: is 49.5 GB, under 10 GB above the floor, so lasting deferral is the likely silent failure.
   Fix: good = OK without bundle=FAILED; deferral older than 26 h is stale; ignore future stamps.
6. **--verify is NOT-WHOLE on the real backup with 391 false alarms (g, high).** It compares only the main copy. Lena's source matches `versions/2026-10-03-1159` (1513f37a...), not the main copy (ab8f06ce...): a held change, not damage. Real rot hides in this noise; verify is the manifest's stated truth check.
   Fix: verify accepts a newest-version match as whole and names files where no copy matches.
7. **Rot in a main copy passes the plain run and restore_check (g, low-medium).** Without the manifest the run writes a good version and says OK; restore_check accepts any version. Fix: report a main copy matching no recorded hash.
8. **restore_check stages up to 1.97 GB on C: temp with no floor check (f, narrow).** Fix: check free_gb per copy, or stage on F:.
9. **Push guard has no MetaHuman rule (e, medium, outside the script).** It refuses only size and pictures. `ue-probe/Content/MetaHumans/Common/Common/Rigs/` (3 Epic retarget uassets, under 1 MB) is not ignored; `git add -A` would push them.
   Fix: ignore `ue-probe/Content/MetaHumans/`; push_guard refuses MetaHumans, MH_, .dna paths.
10. **exclude drops matching names at every depth (low).** `src/out/keep_me.rs` was left out. Fix: match relative to the source root.

## Manifest (added during review)

11. **A lost or damaged backup copy is never noticed (g, high).** known_same() trusts the entry without checking that dst exists. Fake test after the backup file was removed: `OK copied=0 unchanged=1`, file still missing; replaced by ZZZZ bytes of the same size: OK.
    Fix: require os.path.exists(dst) and equal size before trusting an entry; restore_check samples manifest entries.
12. **A changed source with the same size and mtime is skipped (narrow).** Fake test: OK unchanged=1. A tampered sha also skips (needs F: write). Fix: hash the source when mtime is older than the entry's write time, weekly at least.
13. A wrong-type manifest (a list) crashes with AttributeError. Fix: treat non-dict as {}.
- Held: a corrupt manifest falls back to reading the backup; a fresh copy is still read back by same(); the manifest and its `.new` go only to fixed `F:/LedgerTools/backup-staging` (no junction), never into Dropbox. That path is not checked by inside(); a junction there could place it in Dropbox. Fix: refuse a realpath under DROPBOX.

## Held

- (a) No delete or move in copying code.
- (c) `as` = `C:/Windows/x` or `../../x` refused; `C:x` stays inside.
- No shared destinations; no junction in listed folders (10,145 files).
- make_bundle writes only F: staging (copyfile over its own staging file, not the backup).
- `--log` appends only to the git folder's log; installed hook matches the tracked one.
- (f) The copy checks C:'s floor before each file.

## Outcome (session, 17 Nov afternoon)
Fixed, with a self-test each (32 of 32): the manifest trusts an entry only while the backup's copy exists at its size; --verify counts a source held under versions/ as whole (the real backup now VERIFIED, 10,145 files, against 391 false alarms); links and junctions inside listed folders are never walked; the backup folder as a link or junction is refused; keys refused case-blind on the real path with a longer name list; only a plain OK in the past counts against the 26 h staleness line (DEFERRED, a failed bundle or a future date do not); a manifest that is not a dictionary is ignored; ue-probe/Content/MetaHumans/ is in .gitignore.
Listed, not fixed yet (the next session's backup item): two runs in one minute share a versions folder; the restore check does not check C:'s floor before copying to temp; exclude names match at any depth; a source changed with the same size and timestamp is skipped by the manifest until --verify; without the manifest a damaged main copy still passes the plain run.
