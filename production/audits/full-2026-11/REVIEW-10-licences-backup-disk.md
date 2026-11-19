# Review 10: licences, the outside-only rule, backup and disk

Fresh reviewer, 19 Nov 2026, branch lane-2026-11 (newest wip merged), full history fetched (6,243 commits). Read only; this file is the one thing written.

## Summary

The licence records are careful about small things and miss the large ones. Every CC0 texture and font has its row, but the public GitHub repository hands out 747 MB of raw Mixamo files, which Adobe's own FAQ forbids, and the same public repository carries the studio's own written record that it decrypted Mafia's files with a key found on a forum, from copies the studio itself noted carry a repack group's files. His outside-only rule of 17 Nov stopped new extraction, but its leftovers stand: the key and the file viewer are still on F:, CLAUDE.md and the order check still tell sessions to use the games' files, and 119 lines in 42 of the game's specs, code and tools still carry numbers "read from its files". The shipped cast voices run on Pocket TTS, which is not on the allowlist and whose terms forbid cloning without explicit consent. The credits file has not been updated since 30 Oct. Backup is the weakest area: about 36.6 GB of the 70 GB the storage map calls "backed up nightly to Dropbox" is not on the backup's list, the game's own Unreal content (15.9 GB) among it. No restore has ever been run, and the restore check reports OK without comparing anything when C: is under its floor. On 19 Nov at 00:56 C: had 37.4 GB free, under its 40 GB floor, so the nightly backup puts every new copy off. The allowlist exists in one copy only: production/research/license-allowlist.md has never existed in any commit. Twelve findings: five high, four medium, three low.

## Findings, ranked

### 1. The public repository holds raw Mixamo files that Adobe says must not be distributed (high)

Impact: this is a licence breach on a game he means to sell, and it is public today. Deleting the files does not end it, because git history keeps them.

Evidence:
- GitHub API, read today: jsab258/ledger is "private": false, "visibility": "public".
- 88 files under ledger/Assets/Characters, 746.8 MB in HEAD, are Mixamo bodies and clips (Adam.fbx 87 MB down to Remy.fbx 28 MB, plus four clip folders). Another seven Mixamo bodies sit in production/assets/people/*.glb (about 28 MB; commit cd4213d91: "a Mixamo man in a grey tracksuit").
- THIRD-PARTY.md lines 107-112 give Mixamo's terms as "no redistribution of the assets as assets" and then say "the FBX files are tracked because they are project inputs". The Mixamo licensing FAQ on Adobe's community site (posted 29 Sep 2022, read today) lists under NO: "Any type of free distribution of character or animation raw files".
- The history clean of 5 Oct (DECISIONS archive line 302; production/research/git-history-clean-2026-10-04.md) removed screenshots only and never looked at Mixamo.
- The pre-production review of 3 Oct recommended making the repository private (production/research/pre-production/SUMMARY.md line 64). The answer then was to take the screenshots out and leave the repository public.

End, ruling for him (licences): Should the raw Mixamo files stop being public? A) make the repository private and move the Mixamo inputs to F: and the backup (recommended; first check what private Actions minutes would cost for the Linux core tests, which nobody has checked); B) stay public and run a second history clean that removes them; C) leave it as it is.

### 2. Leftovers from the game-file extraction, and the public record of it (high)

Impact: legal exposure for a game he may sell. The decryption is written up in a public branch, and the tools to repeat it are still installed.

Evidence:
- DECISIONS archive (production/archive/DECISIONS-to-2026-11-09.md, public on origin/wip) line 673, 25 Oct: both installed copies "carry a repack group's file (_Redist/fitgirl.md5) and piracy sites' links ... not a store's"; the session held the work. Line 674: he answered "I own the games, this is nothing for you to decide. Go". Line 676: Mafia's AES key was taken from a public forum thread and "proved by decrypting the name index of all eight encrypted containers". Line 678: a mappings file was downloaded so FModel could open the packages. KCD2's archives were unpacked (31,150 files, 851 MB, line 674).
- The studio's own legal note had said the opposite on 12 Oct: "Do not decompile, disassemble, unpack or rip another game" (production/research/frontier-ai-uses/3-LEGAL.md line 24).
- RULINGS.md line 53 (17 Nov): "Never decompiled, their files never opened, copy protection never bypassed".
- What is still there on 19 Nov (pc-inventory.json): F:\LedgerTools\keys, 4 files (the Mafia key and the mappings file, per DECISIONS archive 676 and 678); F:\LedgerTools\aaa-study, 0.24 GB in 212 files; F:\LedgerTools\dotnet10, the runtime fetched only to run FModel. tools/outside_only_check.py lines 188-189 list the FModel zip, the FModel folder, the inZOI extract and the Silent Hill 2 reader as "WAITING HIS YES", and retention.json "protected" still names the keys and five aaa-study folders. The Mafia and KCD2 extracts themselves were deleted on his yes of 17 Nov (DECISIONS.md line 299, 14.6 GB together with other folders).
- No page verdict for "study-tools-delete-2026-11-17" exists in production/approvals/answers.

End, ruling for him (licences): What happens to the extraction leftovers? A) delete the key, the mappings file, FModel, dotnet10 and every aaa-study raw folder now, keep only our own written notes, and ask the studio for a short plain note on what the public record says (recommended); B) delete the leftovers, leave the record; C) keep everything as it is.

### 3. Numbers read from Mafia's files still drive the game, and the rules still ask for them (high)

Impact: his ruling says "only our own words and numbers"; the game does not follow it yet, and every new item is pushed back toward the games' files.

Evidence:
- 119 lines in 42 files under production/specs, ue-probe/Source, ue-probe/Config, tools/ue and tools/art-recipes name Mafia or KCD2. Examples: production/specs/camera.json line 3, "Mafia: The Old Country, read from its files ... on foot 1.65 back, 0.45 aside", and line 22, the talk camera "63 degrees, the pivot 1.50 m up, 1.20 m back"; production/specs/asset-budgets.json line 33, the jacket budget from "Mafia's median top 21,994"; Mickey's office grade from "Mafia's live values" (DECISIONS archive line 838); unreal-look.json line 176, the lamps.
- CLAUDE.md line 51: "look up how Mafia or Kingdom Come II does it (the studies, then their files on demand)"; line 52: "Mafia's missing numbers fetched only when an item needs one". DECISIONS.md line 341 notes this contradiction and leaves it to him.
- tools/order_ledger.py lines 23 and 108 still refuse a new item that names no "Reference:" from "Mafia's or Kingdom Come II's" study.
- production/RESTORE.md line 24: "Study extracts of other games: re-extracted from his installed games"; line 18: "the published Mafia key [is] set again by hand".
- Four hours before his ruling the session had decided to carry on reading the games' files (DECISIONS.md line 319, 17 Nov 18:55: "the study reads the games' files as it already does (FModel, published keys, F: only)").

End, list item: re-source each game value from outside footage, developer talks or our own tests, starting with camera.json and asset-budgets.json, and drop "read from its files" from specs and code. Rule: order_ledger.py and RESTORE.md say "outside reference (footage, talk, published analysis) or none found"; the CLAUDE.md wording goes to him, since the file is his.

### 4. The shipped cast voices run on a model outside the allowlist whose terms demand explicit consent (high)

Impact: Sheila's, Ron's and Darren's voices could have to be redone after release.

Evidence:
- THIRD-PARTY.md lines 158-164: Pocket TTS (Kyutai), CC BY 4.0, "Its access terms add a prohibited use: 'voice impersonation or cloning without explicit and lawful consent'". The voices are cloned from VCTK volunteers, who recorded for speech research.
- The allowlist's voice line (ledger-v2/research/license-allowlist.md line 4) names Kokoro, Chatterbox and Piper, and not Pocket. Process line 30 says a new tool needs "a decision record citing the weights license". Pocket was adopted on 26 Oct (DECISIONS archive lines 688 and 691), and its licence row was written on 27 Oct, after it was in use.
- The consent risk is covered by pointing to his ruling of 24 Sep (allowlist line 25), which was made a month before Pocket and its stricter clause.
- RULINGS.md line 76 lists p267, p227 and p286 "on Pocket".

End, ruling for him (licences): Pocket's terms ask for explicit consent, and VCTK's speakers consented only to research use. A) keep Pocket, add it to the allowlist, and record the consent risk as accepted by him in writing (recommended if the voices pass his ear); B) move the shipped voices back to Chatterbox (MIT, no consent clause); C) look for voices whose speakers consented explicitly.

### 5. Backup: half the lasting shelf is not backed up, nothing has ever been restored, and the check passes blind (high)

Impact: if the PC dies, the game's assembled Unreal content and other "lasting" work may be gone, while every record says it is safe.

Evidence:
- production/storage-map.json marks 39 folders "lasting", 70.2 GB in all, each "expiry: never; backed up nightly to Dropbox". The backup copies only what production/specs/in-game.json lists (9 approved items plus 14 backupAlso rows). Compared folder by folder, 36.6 GB is not on the list, including C:/Users/Jafar/ledger-local/ue-probe/Content (15.9 GB, map line 27, "the game itself", source "imported again from F: game inputs (unverified)"), C:/LedgerTools/mh-assemble (5.6 GB), F:/LedgerTools/fab, polyhaven and approved-cast-2026-09-25. production/RESTORE.md has no step that rebuilds ue-probe/Content.
- No restore has been recorded. No "restoreCheck=" result appears anywhere in the repository, and no restore drill appears in DECISIONS. RESTORE.md line 27 names a weekly restore check, but DECISIONS 17 Nov (backup review, line 50) says "nothing schedules it yet". Kiln's bundle is made with git bundle create (tools/backup-to-dropbox.py line 318) and never verified.
- tools/backup-to-dropbox.py lines 337-348: when C: is under 40 GB, the restore check skips every file and still returns "restoreCheck=OK sampled=20 differ=0".
- The nightly Task Scheduler entry was refused to the session (tools/register_backup_task.ps1 lines 3-4). The ACTION item was withdrawn (DECISIONS.md line 308). The backup runs from the first commit of the day and from fresh_gate.py.
- Losses that have already happened: on 12 Nov a wrong delete removed solve inputs with "No other copy (searched C:, F:, the backup)" (DECISIONS.md line 122); on 17 Nov there was "No copy of his face mesh on C:, F: or the backup" for Darren (line 262).
- There is one offsite copy, inside his Dropbox, whose plan and version-history length are "unknown" (production/research/disk/DROPBOX-ONLINE-ONLY-2026-11-17.md section 5).

End, list item: put ue-probe/Content's own made assets (or proof they rebuild from F:) and the other lasting folders on the backup list, or relabel them honestly; fix restore_check so a skipped file counts as not checked; run one real restore (a MetaHuman into a fresh project, Kiln from the bundle) and record it. Rule: storage-map's "backed up" must match in-game.json's list, checked by retention.py.

### 6. Disk: C: is under its floor and the build caches on C: are almost three times what he allowed (medium)

Impact: builds stop, the backup defers, and sessions spend time deleting instead of building.

Evidence:
- pc-inventory.json, 19 Nov 00:56: C: 37.41 GB free against its floor of 40 (RULINGS.md line 123). On 18 Nov C: was 39.0 before 7.9 GB of deletions (DECISIONS.md line 386). F: went under its 20 GB floor on 11, 14, 14 and 16 Nov (DECISIONS lines 56, 149, 152, 191).
- RULINGS.md line 123: the build cache "may use about 17 GB on C:". Measured: cargo-target 19.78 GB (13.9 on 17 Nov, map line 37), zen 12.61 GB (retention cap 10.7), actions runner 13.6 GB; about 46 GB in all.
- retention.json gives cargo-target no size cap, only "3 days untouched", and it is touched every day.
- CLAUDE.md: "nothing large on C:". C:\LedgerTools alone holds about 52 GB.
- Cost: 64 lines of DECISIONS.md since 9 Nov deal with space or deletion; C: free fell from 107 GB (9 Nov) to 44 (12 Nov) (line 119).

End, rule: a size cap on cargo-target (with kiln-lanes) in retention.json, enforced before each Kiln build; the Rust build cache moved to F: or to H: (51 GB free) or I: (35 GB free), if he agrees to use those drives.

### 7. The credits page is three weeks stale and misses a required attribution (medium)

Impact: shipping without Kyutai's CC BY credit breaches its licence, and the VCTK line lacks what THIRD-PARTY.md says CC BY needs.

Evidence:
- production/specs/credits.json was last changed on 30 Oct (b7f3b3ec6). It has no Kyutai or Pocket TTS, no Chatterbox or Resemble MIT notice, no CMU, and no Patrick Hand, Oswald or the other cloud-week fonts. Its VCTK line has no CC BY link and no note that the recordings were modified, both of which THIRD-PARTY.md lines 27-32 require.
- credits.json's own "what" says "a source added there is added here". tools/attribution-check.py checks folders against THIRD-PARTY.md, never credits.json against THIRD-PARTY.md.

End, list item: bring credits.json level with THIRD-PARTY.md. Rule: attribution-check fails when a THIRD-PARTY row marked attribution-required has no line in credits.json.

### 8. Kiln, the clothing tool, came from decompiling Marvelous Designer (medium)

Impact: garments made with it go into a sold game, and CLO's terms, which he accepts every month, forbid reverse engineering.

Evidence:
- DECISIONS.md line 34 (10 Nov): Drape Studio was built by "decompiling it and taking 59 of 82 values from Marvelous's preset files; CLO's General Terms forbid reverse engineering". His answer the same day (verdicts/drapestudio-licence-2026-11-10.json): "don't ask about licenses or terms ... this is not an issue".
- Line 359 (18 Nov): "Kiln's engine carries values from decompiling Marvelous (engines/drapestudio/MECHANICS.md, 78 address references)". Line 402: all 58 values replaced, "not yet, briefly" for the data-file start values and the leg and torso fits made against Marvelous's drapes. The replacement cost about 28 helper hours and 5 machine hours (line 368).
- Kiln's history, with the old values in it, goes nightly to Dropbox as kiln.bundle (in-game.json backupAlso).
- A working practice since 10 Nov, "his statements about his own tools ... taken as given: no licence, terms or contents checks" (DECISIONS-TRACE D-E-035), is not in RULINGS and cuts across the allowlist's "law".

End, ruling for him (licences): A) finish the replacement (start values and fits from our own measurements) before any Kiln garment ships, and keep Kiln's history private (recommended); B) ship Kiln garments as they are; C) do not use Kiln garments in the game.

### 9. Records that say things that are no longer true (medium)

Impact: future sessions act on wrong facts about licences and keys.

Evidence:
- THIRD-PARTY.md line 513: the KCD2 frames "remain in the repository's history until he decides on cleaning it". They were cleaned out on 5 Oct, and a search of all 42,865 blob names finds no screenshot of either game.
- storage-map.json line 1051 marks F:/LedgerTools/keys "backed up nightly to Dropbox", while the backup refuses that folder (backup-to-dropbox.py lines 66-68) and RESTORE.md line 18 says keys are never backed up.
- DECISIONS.md line 298: a test folder was deleted inside the Dropbox backup, against RULINGS.md line 125, "the Dropbox backup never deletes or overwrites".
- The allowlist admits "ElevenLabs on paid tiers if adopted" (line 4) against RULINGS.md line 47, "29 Sep: no paid voice service", and line 99, "no cloud voice".
- The allowlist's PROCESS line 29, "Every asset ... carries a license tag; untagged fails the license gate": the gate works by folder, not by tag.

End, list item: correct each line; the ElevenLabs words come out of the allowlist as already settled by his rulings.

### 10. One allowlist, kept in an old-version folder (low)

Impact: small; the law sits where the inventory calls things "reference (old version)".

Evidence: only ledger-v2/research/license-allowlist.md exists, in every commit; production/research/license-allowlist.md never existed (git log --all). CATALOGUE.md line 21 names it as the home, beside THIRD-PARTY.md. INVENTORY.md line 107 classes ledger-v2/research as "reference (old version)".

End, rule: leave one copy; the inventory script treats the allowlist's folder as live.

### 11. The attribution check fails on the lane branch (low)

Impact: the next merge of the lane into wip turns the build check red.

Evidence: python3 tools/attribution-check.py on lane-2026-11 gives "1 problem(s)": 47 prototype files under tools/lane/prototype/project/src that THIRD-PARTY.md does not know. They are on this branch and not on origin/wip. The check runs in tools/ci-checks.sh line 151.

End, list item: one "ours" row for the prototype's own code before the merge.

### 12. Git size is under control; the inventory overstates unnamed PC folders (low)

Impact: none harmful; two numbers to correct.

Evidence:
- History: 42,865 blobs, 7.04 GB raw, 3.47 GB packed; 49 blobs over 10 MB, 11 over 50 MB (all Mixamo). The 5 Oct clean took it from 30.8 to 3.2 GB, and the guards (tools/git-size-guard.py: 1 MB, game inputs 25 MB; push_guard.py) have held growth to about 0.27 GB since. quay-street.glb has 44 versions, 427 MB raw but 32 MB packed. Note: origin/main has not moved since 5 Oct; all work is on wip.
- INVENTORY.md line 287 says 61 PC folders are "named by nothing". The script never read storage-map.json, and 60 of the 61 are on the map; only ledger-local\.githooks is not.

End, rule: the inventory script reads storage-map.json.

## The seven questions in short

1. Same game: the licence rules point at a sold game; the extraction work and the public raw files do not.
2. Still true: findings 3, 5, 7 and 9 show records that no longer match.
3. Used: under his rule, the protected study folders, the key and dotnet10 are dead weight; ledger/Assets/Characters only feeds person-export.py and does not need to be in git.
4. Cost: history clean 30.8 to 3.2 GB (time not recorded); AAA study planned at 45 to 50 hours (STUDY-PLAN.md line 4), actual not recorded; Kiln decompile replacement about 28 helper hours plus 5 machine hours; disk upkeep 64 DECISIONS lines since 9 Nov, hours not recorded.
5. Missing: a proven restore; the backup covering what the map promises; Pocket on the allowlist; current credits.
6. Contradictions: CLAUDE.md lines 51-52 and order_ledger.py against RULINGS line 53; RESTORE.md lines 18 and 24 against the same; storage map against the backup list; allowlist against RULINGS on paid voices.
7. Raised by him first: the outside-only rule (17 Nov, 22:33), four hours after the session had chosen to keep reading the games' files (DECISIONS.md line 319); the studio's own legal note of 12 Oct should have stopped it. The three.js licence (18 Nov, 21:10: "why didn't this come to my needs you page", allowlist line 16): the code was bundled before it was on the list, and THIRD-PARTY.md line 609 shows it was known. The backup and storage concept (advisors 196 and 197, 17 Nov) came after the 12 Nov wrong delete had already found no backup copy; a restore drill would have caught the gap first.
