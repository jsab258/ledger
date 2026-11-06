# Study A from inZOI's packed files, 6 November 2026: stopped at the key

(20:58: replaced as to access: a published key opens the containers, KEY-AND-MAPPINGS-2026-11-06.md; this note stands as the record of the 19:45 state. Its line that the reader already takes a key was wrong: a small change was needed.)

Source: C:\Games\inZOI.v0.10.1\inZOI.v0.10.1\game\BlueClient\Content\Paks (v0.10.1). Read 6 November 2026. Nothing from the game is kept in LEDGER.

## Access result (measured, file headers)

- Every game container is encrypted. In each .utoc the container-flags byte is 15 (compressed, encrypted, signed, indexed) for all 18 containers read (BlueClient, BlueClient_Content and its BG, BG_BLDG, BG_HS, BG_Megascans, BG_VH, BG_Working, BG_citysample, BG_marketplace, Characters, Characters_Anims, FX, Map, MetaHumans, Sound, UI, UE). In the two .pak files checked (BlueClient_Content_Characters, BlueClient) the footer's index-encrypted flag is 1. Only global.utoc (flag 4: signed, not encrypted) is open, and it holds no game content.
- No key for inZOI is in F:\LedgerTools\keys (it holds google.txt, mafia-aes.txt and the Mafia mappings folder only). No published key was looked up or used. By the brief, nothing was done to get one: the file names, sizes and contents inside these containers were therefore not read.
- Method that works for the Silent Hill 2 containers (no encryption) was prepared (see the Silent Hill 2 note) and would apply here once a key exists; its use needs the key on F: only.

## Questions of section 3 (FILES-2026-11-06.md), none answered from inside the packs

- Q2 (speed, frame cost): needs a running game; not allowed. Unanswered.
- Q3 (what the small model decides, what lines it writes) and Q4 (how invented facts are avoided): prompt contract and tool-call harness are in packed game data or the executable. Unreached (encrypted).
- Q5 (card sharing, back-end choice, fallback): settings in the packed data or the executable. Unreached (encrypted).
- Q1 residue (which of the three models loads; "vram" units): unreached (encrypted).
- Clothes method (garment skeletal mesh counts, triangle counts, material and texture sizes, simulated cloth or not, hems and skirts): unreached. The only thing known is the earlier plain-file result in FILES-2026-11-06.md section 2 (names of cloth settings in Lua type definitions; the Characters pak is 5,889,588,016 bytes in size), which is not an extraction.
- Q6, Q7, Q8: not file questions.

## What would be needed

A decryption key for inZOI v0.10.1 on F:\LedgerTools\keys (never in git, never printed). Its source is not chosen here. No tool needs downloading: the program built for the Silent Hill 2 note already loads encrypted containers when given a key.
