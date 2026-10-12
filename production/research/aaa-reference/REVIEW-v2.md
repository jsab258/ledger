FAIL

# Second and last review of KIT.md (queue unit 6.1)

12 October 2026, by a fresh reviewer. Pages were read through raw.githubusercontent.com and git. GitHub's web pages and API were blocked.

## The seven faults of REVIEW-v1.md

1. Key: **fixed as written.** cs.rin.ru is gone and option B is word for word. One older sentence was left behind (new fault 2).
2. Mapping file: **fixed**, apart from a capital letter (new fault 3).
3. "Since 1.2": **fixed** in all three rows.
4. Crime article: **fixed.** Everything now matches KM-A-27, which was read again. One gloss goes beyond the page (new fault 4).
5. Folder: **fixed.** All three paths now point to the folder that retention.json protects.
6. Lua docs: **fixed.** KM-A-55 does list Tools/modding/docs/.
7. Interview: **fixed.** Both "absent" guesses were deleted.

## Spot-checks

**Confirmed:**
- K1 is a snapshot "exported 2026-06-23".
- KM-A-87 is Warhorse's Workshop guidelines.
- F11 (repak) works "with Unreal Engine .pak files".
- F6 is injected as a DLL.
- K7 is from KCD1's time.

**Wrong:** none found.

Every part of 6.1 is present.

## New faults, worst first

1. **WHAT:** The reading list sends readers to what the kit rules out:
   - F9's page on keys shows how to find a game's key.
   - F7 holds a published key and links the cracking forum.
   - F6 is a DLL to inject, with a warning about anti-cheat bans.
   - F5 holds mapping files dumped from games.

   **WHERE:** section 5a, the last line.
   **FIX:** Replace "F1: FModel wiki, Settings Explanation. F9: AES key and mapping basics. F5, F6, F7, F8: mappings, dumper, keys, compatibility list. F10, F11: repak and retoc." with "F1: FModel wiki, Settings Explanation. F8: FModel's compatibility list. F10, F11: repak and retoc. F5, F6, F7 and F9 are cited in section 3 only and are not reading. They hold mapping files dumped from games, a DLL to inject into a game, a published key with a link to a cracking forum, and guides to finding keys."

2. **WHAT:** Step 5 still says where to type a key, just before it says stop.
   **WHERE:** section 3, step 5.
   **FIX:** Delete "If FModel asks: Directory > AES takes a key as `0x` plus 64 characters [R F3]."

3. **WHAT:** A capital letter follows a semicolon.
   **WHERE:** section 3, step 4.
   **FIX:** Change "attach to the running game; Every mapping file" to "attach to the running game. Every mapping file".

4. **WHAT:** KM-A-27 never says what "expiration" and "isSpreadable" mean, but 5a states a meaning without marking it as a guess.
   **WHERE:** 5a, the KM-A-27 line.
   **FIX:** Replace "how long a crime is remembered and whether word of it spreads (rpg/crime.xml, ai/script_params.xml)" with "the fields expiration and isSpreadable, which the page does not explain, and crime memory values such as crime_longTermMemoryTrespassExpiration (rpg/crime.xml, ai/script_params.xml)".

New fault 1 alone is why this fails. Once the four fixes are made as written, the kit passes.
