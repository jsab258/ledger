# Method: the brief each helper worked to (rulings sweep, 1 October 2026)

Eleven helpers, each given one batch of the 440 rulings (numbered DEC-, ARC-, CAN- and OTH- in the order of their files) and this brief, word for word. Each wrote its verdicts as one JSON line per ruling outside the repository; they are merged in rulings.json. The reviewer then checked every NOWHERE verdict and the high-impact PARTLY ones in the code (rows marked R in TABLE.md) and a random sample of BUILT ones.

---


You are one of several helpers in an independent review. You check a batch of rulings against the repository and report what you find. You are READ-ONLY on the repository: never edit, create, move or delete anything under /home/user/ledger, and never commit or push. Write your results only to the output file named in your task (outside the repository). No fixes, no praise.

## The problem being reviewed

Twice this week, a ruling by the owner (Jafar) turned out never to have been built:
- "Grime is the strategy" (D53, 21 September): the street generator's own docstring says the wear layer is not its job, so nothing built it.
- Character casting: flagged as missing a week before the characters were built without it.

Rulings that never become work are now a known failure of this project. For each ruling in your batch, decide what has actually become of it. Read the code, the content and the lists. Do NOT rely on the sessions' own claims. A DECISIONS line saying "built in X.cs" is a claim: open X.cs and find the behaviour. The same goes for a NOW.md line marked [x] or "done", and for a commit message.

## The repository (/home/user/ledger, branch claude/rulings-sweep, the latest main)

**What the player runs** is the Unreal 5.8 project `ue-probe/`:
- `Source/LedgerProbe/Public/*.h` holds the C++ port of the simulation and most game logic (Arrangement.h, CastDay.h, Gossip.h, Perception.h, PoliceFile.h, Silence.h, StreetVoice.h, TownSave.h, Waiting.h, WeeksEnd.h, PlayerIdentity.h and others).
- `Source/LedgerProbe/Private/*.cpp` holds CrimeProbe.cpp (free play and talk wiring), LedgerPause.cpp, TitleScreen.cpp, VignetteShot.cpp (the street, its look and frames), StreetSounds.cpp and others.

**The C# Core**, `ledger/Assets/Scripts/Core/*.cs`, is the source of truth for the simulation.
- The talk program `ledger/TalkHelper` (launched by the game) and `ledger/Relay` use it. So Core code that TalkHelper calls IS live in the game's conversations.
- Core simulation code that the game's C++ port does not have is NOT in the game, unless TalkHelper runs it.

**`ledger/Assets/Scripts/Game`** is the legacy Unity reference build. Something that exists only there is not in the game players run.

**Other places:**
- `content/` holds dialogue, brands, rules and voice lines.
- `production/specs/*.json` holds specs the game or tools read. Check that the game actually reads a spec, for example with grep in ue-probe.
- `production/cast/cards` holds the talk cards.
- `production/casting` holds the casting sheets, voices and approvals.
- `tools/` holds Python tools, gates, art recipes (`tools/art-recipes`), Unreal scripts (`tools/ue`), the AI tester (`tools/ai-tester`) and `tools/ci-checks.sh`.
- `game-design/` holds design documents. **A design document is not built work.**
- `legacy/studio-v2/respec/decision-register/D*.md` holds the old decision records named by the archive's lines.
- `ledger-v2/research/license-allowlist.md` is the licence allowlist.

**The lists of work still to do:**
- NOW.md: the builder's list, "Handovers to clothing" and "Handovers".
- TOWN.md: the town session's list.
- CLOTHES.md: the clothing session's list.
- ROADMAP.md.
- FINDINGS.md: open faults.
- FOR-JAFAR.md: the "Needs you" section.

**The sessions and their lanes:**
- **builder:** the Unreal project, art, faces, voices, anything using the graphics card, and wiring and porting into the game.
- **town:** the Core simulation, the conversation helper, casting sheets, story and documents.
- **clothing:** garments in Blender and Marvelous Designer.
- **Jafar:** decisions of money, licences, canon or scope.

## Classify each ruling as exactly one of these

1. **BUILT.** The ruling's behaviour exists where it takes effect. For game behaviour, that means in what the Unreal game runs: the C++ port and game code, the TalkHelper it launches, or content and specs the game reads. For a tooling or process ruling, it means in the tool, hook or setting it names.
2. **PARTLY.** Some of it exists but not all. Also use PARTLY when it exists only in the C# Core or the legacy Unity build and the game does not reach it, or when it is built but switched off by default.
3. **LISTED.** Not built (or not finished), but on a current list as work still to do. Quote the list line.
4. **SUPERSEDED.** A later ruling replaced it. Name the later ruling (its file:line).
5. **NOWHERE.** Not built, not on any list, and not superseded.
6. **CONDUCT.** Only if the ruling binds how sessions behave and names no artefact that could exist. Examples: "speak plainly", "ask him only about money". If it names a mechanism (a tool, a hook, a setting, a file, a page tool), check that mechanism and use 1 to 5 instead. Use CONDUCT sparingly.

**When a ruling has several parts,** judge each main part, and give the ruling the status of its weakest part that is not superseded. List which parts are missing.

**Pure records** ("the faces approved are X", "voice p267 cast") are BUILT only if the game actually uses what was ruled: the approved head, the cast voice, the name. Check the specs the game reads (for example production/specs/in-game.json, hook-cast.json, the voice keys), not only the approval files.

**Old decision records** (archive lines with a D-number link): open the record in legacy/studio-v2/respec/decision-register/. Find its operative requirement or requirements (what must exist in the game), and judge those.

## Evidence

- For every item, cite what you looked at as file:line, or as a grep that found nothing.
- Separate CHECKED from INFERRED:
  - **CHECKED** is what you saw yourself in code, content, specs or lists.
  - **INFERRED** is any conclusion you reached without direct sight. Examples: "probably called because…", "no grep hit, so likely absent".
- A grep that finds nothing is evidence of absence only for the names you tried. Try two or three likely names before you call something absent.

## For every NOWHERE and PARTLY item, also give these

- **player_impact**, from 1 to 5:
  - 5: a player would meet it in the first session, or it breaks the premise or a content or legal rule;
  - 4: visible in ordinary play;
  - 3: on a specific path, or over a long session;
  - 2: rare, or polish;
  - 1: invisible to players (process, tooling, records).
- **why:** one line explaining the score.
- **where_it_belongs:** the file or module in code, or the list it should be on.
- **lane:** builder, town, clothing or Jafar.

## Output

Write one JSON object per line (JSONL) to your output file, one line for each ruling id in your batch, in batch order. Use these fields:

```
{"id": "...", "status": "BUILT|PARTLY|LISTED|SUPERSEDED|NOWHERE|CONDUCT",
 "summary": "the ruling in under 20 words",
 "checked": ["file:line - what is there", "grep 'X' in ue-probe: no hit", ...],
 "inferred": ["..."],
 "missing": "what is not built (for PARTLY or NOWHERE), else empty",
 "superseded_by": "file:line or empty",
 "list_line": "file:line of the list entry, or empty",
 "player_impact": 1-5 or null, "why": "...", "where_it_belongs": "...", "lane": "builder|town|clothing|Jafar|none"}
```

**Time.** Work efficiently: grep first, then open only what you need. Aim to finish in about 40 to 50 minutes. If you run out of time, write every item you have done, mark the rest as `{"id": ..., "status": "UNCHECKED"}`, and say so.

**Final message.** Give:
- the counts by status;
- every NOWHERE and PARTLY id, with one line each (impact, what is missing, lane);
- anything surprising you found on the way.

Keep the final message under 900 words. The JSONL file is the full record.
