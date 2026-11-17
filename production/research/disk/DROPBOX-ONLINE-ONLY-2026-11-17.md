Method researched: Make files online-only (Dropbox Help) with Microsoft Learn "Build a Cloud Sync Engine that Supports Placeholder Files"

Read 2026-11-17. First pass, no decision. Nothing on the PC's Dropbox was touched.

## 1. Which implementation
- Dropbox's Windows help page says the Windows app was rebuilt on "Microsoft's new sync API called cloud files". It covers Windows 11 23H2+ and Windows 10 22H2+. Eligible users are migrated automatically. Accounts with 500k+ files, and legacy Dropbox Backup users, are not migrated yet. Users can opt out under Advanced settings. https://help.dropbox.com/installs/dropbox-for-windows (read 2026-11-17).
- Since which app version: not stated on the page. UNVERIFIED. A help-center change page is dated 31 May 2024 (per a search summary, not read in full).
- How to tell: the "Expected changes" article says sync icons were changed to match Windows' cloud-files icons, and Explorer's Details view gets a Status column. https://help.dropbox.com/installs/windows-support-for-expected-changes (read 2026-11-17). Microsoft says cloud-files placeholders are reparse points, hidden from ordinary apps. https://learn.microsoft.com/en-us/windows/win32/cfapi/build-a-cloud-file-sync-engine (read 2026-11-17). Folder-location and junction behaviour: not confirmed (UNVERIFIED). Which attribute bits Dropbox's placeholders show: UNVERIFIED.

## 2. Making a folder online-only
- Supported route: in File Explorer, right-click the file or folder, then "Make online-only". Reverse: "Make available offline". https://help.dropbox.com/sync/make-files-online-only (read 2026-11-17).
- attrib supports `+u` (Unpinned) and `+p` (Pinned), with `/s /d`. https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/attrib (read 2026-11-17). Microsoft defines UNPINNED as "should not be kept fully present locally except when being actively accessed", for hierarchical storage software. https://learn.microsoft.com/en-us/windows/win32/fileio/file-attribute-constants (read 2026-11-17).
- Whether Dropbox honours those attributes, and any Dropbox-supported command line: NOT FOUND in Dropbox's pages. Forum threads show users asking for a script and no official answer; the one thread read had an empty body. https://community.dropbox.com/t5/Discuss-Dropbox-Developer-API/How-to-programmatically-make-files-available-offline/m-p/636934. The attrib route for Dropbox is UNVERIFIED.

## 3. Reading, hashing, stat
- Microsoft: placeholders "automatically hydrate into full files under normal use", through any file API, the command prompt or a desktop app. Opening a placeholder over a few seconds shows progress. When not opened at the user's request, a toast appears so the user can block the app. Blocked apps are managed under Settings > "Automatic file downloads". Hydration policy is fixed at open time. https://learn.microsoft.com/en-us/windows/win32/cfapi/build-a-cloud-file-sync-engine
- A read or hash opens the file, so it hydrates (supported by the above). Stat and attribute reads: Microsoft's pages read do not say they hydrate. The attribute doc says RECALL_ON_DATA_ACCESS means "reading the file / enumerating the directory will be more expensive", i.e. a data read recalls. That stat or GetFileAttributes does not hydrate is UNVERIFIED for Dropbox; to be measured, not assumed.
- Hydrated files can be dehydrated again by the system for space (Microsoft, "Full file" state).

## 4. New files written into an online-only folder
- Dropbox's page: the "online-only by default" preference (Preferences > Sync) applies only to new items added directly to the root of the Dropbox folder, not to existing files; files moved in from elsewhere stay available offline unless changed manually. https://help.dropbox.com/sync/make-files-online-only
- So a new file inside an online-only subfolder most likely stays local. Whether it turns online-only after syncing: NOT STATED, UNVERIFIED. Forum reports of files reverting to online-only after Windows updates exist (https://www.dropboxforum.com/discussions/101001014/dropbox-keeps-resetting-with-every-windows-update-to-online-only-despite-my-sett/848718/replies/848729, unreached; known only from a search listing).

## 5. Completeness and restore
- Dropbox's page: an online-only file lives in the cloud; the placeholder remains; deleting an online-only file deletes it everywhere. Making online-only itself is not described as deleting anything.
- Version history: Plus 30 days; Professional (also Essentials, Business, Standard) 180 days; extended version history is a paid add-on. Windows start on upgrade date, not retroactive. Permanently deleted files' previous versions cannot be viewed or restored. Version history does not count against storage. https://help.dropbox.com/delete-restore/version-history-overview (read 2026-11-17). Which plan the user holds: unknown. Deleted-file recovery window: the page gives none.
- Selective sync versus online-only: not covered in the pages read. UNVERIFIED.

## 6. Local space
- Microsoft: placeholder uses about 1 KB for the file-system header. Dropbox: "very little space". The macOS space-reporting quirk on 10.13 to 12.2 is a Mac note only. A forum thread titled "Online-only files taking up space on Windows" exists (unread).

## Unreached or incompletely read
- https://community.dropbox.com/... threads: returned empty bodies or redirects (cloud-files overview thread, reset-to-online-only thread).
- Dropbox "Sync icons in the desktop app for Windows and Linux" page: not fetched.
- Dropbox page on the Dropbox folder as junction point, and any app-version statement: not found.
- Microsoft pages on Cloud Files stat/attribute-read hydration behaviour: not found.
- Search engine result lists were used only to find pages, not as evidence.

## Measured on this PC (2026-11-17 14:28)
Three 2 MB files in a test folder inside LEDGER backup, synced (PowerShell shows Archive and ReparsePoint, 0x420: cloud-files placeholders, fully present). `attrib +U -P` set UNPINNED (0x100420); Dropbox cleared it within 10 seconds, twice, and the files stayed fully on disk (GetCompressedFileSizeW 2,097,152 bytes each; no OFFLINE or RECALL bit ever appeared). So Dropbox does not honour attrib's unpinned mark here: online-only cannot be set by script. The documented way is Explorer's right-click "Make online-only" (his hands). The backup folder holds 23.3 GB in 15,253 files on C: (45.9 GB free, floor 40). Still unmeasured: whether metadata reads (exists, size) hydrate a placeholder; the manifest already keeps the backup from reading copies' bytes. Test folder deleted.
