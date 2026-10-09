# Unreal MCP in the UE 5.8 editor: setup note (research note 1e, 8 October 2026)

**Summary line:** Epic's Unreal MCP can be switched on in about ten minutes without touching the committed project (two plugins named on the editor's command line, one `claude mcp add` in local scope), but LEDGER has no street level to inspect until Play is pressed, because code builds the street at run time, and every action passes through one tool (`call_tool`), so prompts must stay on; the first test is therefore read-only on the Play-in-Editor street, then one lantern value changed and put back.

**Marks.** [SHOWN] read at its source on 8 October. [CLAIMED] from the 7 October notes (Epic's pages, unreachable from this cloud today). [SS] search summary only. [I] my inference. Anything resting only on [SS] or [I] is tagged **(confirm)** and listed in section 9.

## 1. What it is, and what it is for here

- **What.** The `ModelContextProtocol` plugin runs an MCP server inside the editor at `http://127.0.0.1:8000/mcp` [SHOWN, plugin README and setup.md]. Experimental, loopback only, no authentication layer [CLAIMED; the README's "localhost is not a trust boundary" is SHOWN]. The `AllToolsets` plugin supplies the tools; without it the server runs and exposes none [SHOWN].
- **How Claude sees it.** Three meta-tools: `list_toolsets`, `describe_toolset`, `call_tool`. Every real action goes through `call_tool` with `toolset_name`, `tool_name`, `arguments` [SHOWN, SKILL.md].
- **What for.** Looking at and tuning the live street: actors, properties, screenshots, camera, logs, materials.
- **LEDGER has no street level.** `GameDefaultMap=/Engine/Maps/Entry`, `EditorStartupMap` unset, no `.umap` in the repository [SHOWN]. On a plain launch `ALedgerGameMode::InitGame` calls `BuildInteractiveStreet`. It reads `ue-probe/vignette-pieces.json` (copied from `production/specs/`; 641 pieces, 4 lanterns), plus the look, street and people files found from the checkout, and spawns labelled actors [SHOWN, VignetteShot.cpp]. **It also spawns six street people, and cast MetaHumans where their assets exist** (`SkeletalMeshActor`s) [SHOWN].
- **Consequence.** The street exists only while Play runs; MCP edits to it vanish at Stop. To keep a good value, write it into `unreal-look.json`, the scene file, C++ or `tools/ue/make_*.py`. Saved edits to `/Game/Ledger` assets persist, but those scripts would overwrite them.
- **The hook camera is not an actor.** `cam_hook` is JSON: x -3.0 m, z -1.6 m, eye 2.2 m above declared ground 0, yaw 20.4, pitch -3.4 (negative is up), vertical field 46 [SHOWN, vignette-scene.json]. The game spawns a `CameraActor` for `-PageShots` and `-PerfHook` [SHOWN]. By the code's conversion (X = x*100, Y = z*100, Z = height*100) the Unreal pose is location (-300, -160, 220), Pitch +3.4, Yaw 20.4, Roll 0, horizontal field 74.08 degrees at 16:9 [I]. **(confirm)**

## 2. Before you start

1. Engine 5.8 [SHOWN]; editor at `C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` [SHOWN, play.py]. Check that `Engine\Plugins\Experimental\ModelContextProtocol` exists (setup.md names its `Extras\Proxy` folder, SHOWN). Where `AllToolsets` lives is unread. **(confirm)**
2. Add a DECISIONS.md entry first (the allowlist's process for a new tool [CLAIMED]).
3. **Licence gate.** Unreal licence 6(e): no engine use as training input to a generative AI or prompt input to one that trains on it; no MetaHuman content in AI databases, training or testing [CLAIMED, terms note of 3 October]. Claude Code on Free, Pro or Max trains on prompts only if "Help improve Claude" is on; commercial plans never [SHOWN, data-usage page]. Jafar said on 3 October he was switching it off; nobody has read the setting [SHOWN, SUMMARY.md]. Put one line in Needs you and start only once answered. His 3 October ruling already covers frames the AI tester sends, so MCP adds no new kind of data.
4. Keep MetaHuman people and NoAI items out of the test picture (the open question on people recommends it [SHOWN]). Test step 4 hides them.
5. Run `python tools/retention.py space --job "unreal editor with MCP" --drives CF` [SHOWN, CLAUDE.md]. Full disk: stop.
6. Nothing else running: no build, no play, no runner job (the `Wait-Runner` check in `tools/ue/build-local.ps1`) [SHOWN]. Close voice and Blender jobs [I].
7. Save and commit. Epic: "Save and commit (or shelve) before any long MCP-driven session" [SHOWN]. The 21 tracked `.uasset` files under `ue-probe/Content` make a local commit a real recovery point [SHOWN]. Do not push for this.
8. Permission mode **default**, never `bypassPermissions`. Epic: prefer not to use `--dangerously-skip-permissions` with this plugin [SHOWN]. Whether `auto` gates MCP calls is unread. **(confirm)**
9. Port 8000: nothing in the repository uses it [SHOWN, grep]. `netstat -ano | findstr :8000` should print nothing.

## 3. Enable in the editor

The committed `.uproject` lists only `MetaHumanCharacter` and `ChaosClothAsset` [SHOWN]. **Do not add the MCP plugins to it.** Epic's setup edits it [SHOWN], but a committed edit could reach the build machine, and `ModelContextProtocol` can be hosted in cooked builds [CLAIMED]. Instead:

1. Copy `production\specs\vignette-pieces.json` to `ue-probe\vignette-pieces.json` (git-ignored). The game looks there; the play .bat does the same [SHOWN].
2. Start the editor with the plugins on the command line:

```powershell
& "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" "C:\Users\Jafar\ledger-local\ue-probe\LedgerProbe.uproject" -EnablePlugins=ModelContextProtocol,AllToolsets -ModelContextProtocolStartServer
```

   `-ModelContextProtocolStartServer` and `-ModelContextProtocolPort=<port>` are Epic's flags [SHOWN, setup.md]. `-EnablePlugins=` is already used in this repository (`PythonScriptPlugin`) [SHOWN]. That it pulls in `AllToolsets`' dependencies is untested. **(confirm)**
3. If they do not load, use Epic's `.uproject` entries (`{"Name": "ModelContextProtocol", "Enabled": true}` and the same for `AllToolsets`) [SHOWN]. Never commit that; run `git diff --stat ue-probe/LedgerProbe.uproject` before every commit.
4. The Output Log shows MCP startup lines [SHOWN]; or type `ModelContextProtocol.StartServer [port]` in the console [SHOWN].
5. `netstat -ano | findstr :8000` must show `127.0.0.1` LISTENING, not `0.0.0.0`. [I]
6. Tools missing: `ModelContextProtocol.RefreshTools`, then check `AllToolsets` [SHOWN]. Leave `bEnableToolSearch` at its default; `False` registers every tool upfront [SHOWN].
7. Do **not** use `bAutoStartServer=True` in `Saved\Config\WindowsEditor\EditorPerProjectUserSettings.ini` (Epic's way, SHOWN): every commandlet run (the `tools/ue` import scripts) would open a Python-running port. The flag leaves nothing behind. [I]
8. An Editor Preferences panel (General, Model Context Protocol) shows port and path [SS]. **(confirm)**

## 4. Connect Claude Code

**Route A, first: the connection.** In `C:\Users\Jafar\ledger-local`:

```powershell
claude mcp add --transport http unreal-mcp --scope local http://127.0.0.1:8000/mcp
```

- Local scope writes to `~/.claude.json` under this project's path only [SHOWN]; the Town and Clothing checkouts never see it. The Blender server was registered the same way on 28 September [SHOWN, DECISIONS].
- `unreal-mcp` is Epic's own server name [SHOWN].
- Start a **new** session afterwards; a server added mid-session did not load in September [CLAIMED]. Then `claude mcp list` says Connected and `/mcp` shows it [SHOWN].
- Avoid `ModelContextProtocol.GenerateClientConfig ClaudeCode`. On the launcher build it writes `.mcp.json` into `ue-probe\` [SHOWN]; Claude Code reads project-scope `.mcp.json` only from the folder it starts in [SHOWN], and a committed one would reach every session. Delete it if it appears.

**Route B, after the first pass: Epic's plugin.** `unreal-engine-skills-for-claude-code` 3.1.1, MIT, "Copyright (c) 2026 Epic Games" [SHOWN].

- It connects nothing: "This plugin does not ship a static `.mcp.json`" [SHOWN]. It adds the `unreal-mcp` skill (usage contract, safety rules), two authoring skills and a SessionStart hook. Route A is still needed.
- Install: `/plugin install unreal-engine-skills-for-claude-code@claude-plugins-official`, and pick **local** scope (`.claude/settings.local.json`) [SHOWN]. Project scope would edit the tracked `.claude/settings.json` for all sessions.
- Supply chain: the official marketplace pins commit `a6aa73ad…`; the eight files I read are identical there and on `main`. The hook script only reads folder names and prints one JSON line [SHOWN].
- Hook: `bash ${CLAUDE_PLUGIN_ROOT}/hooks/unreal-context.sh`, on startup, resume, clear. It walks up from the working folder looking for a `.uproject`; the repository root has none (it is in `ue-probe\`), so it does nothing there [SHOWN, script]. Windows needs Git Bash or WSL on PATH; without it the hook fails and the tools still work [SHOWN, README]. Which `bash` is on this PC is unread. **(confirm)**
- Recommendation: A for the test, then B, the cheap way to give Claude Epic's own rules.
- The optional proxy (survives editor restarts) needs a `.mcp.json` and `Extras\Proxy` [SHOWN]. Skip for now.

**Permissions.** In `.claude/settings.local.json` allow only the two read-only meta-tools:

```json
{"permissions": {"allow": ["mcp__unreal-mcp__list_toolsets", "mcp__unreal-mcp__describe_toolset"]}}
```

- **Never allow `mcp__unreal-mcp__call_tool`.** Reads, edits and Python all go through it, and settings files skip `mcp__` rules with parentheses [SHOWN]. Every action therefore prompts. That is intended.
- A speed bump for the Python tool: launch with `--disallowedTools "mcp__unreal-mcp__call_tool(toolset_name:ProgrammaticToolset)"`. The flag is documented for MCP parameters; the argument name is from SKILL.md; untried together. **(confirm)**

## 5. Toolsets that matter

Tool names inside each toolset are **unread**; read them with `describe_toolset`, never guess.

| Need | Toolset and source | Use here |
|---|---|---|
| Scene, actors | "Actors and Scene" [SHOWN, README]; `ActorTools`, `SceneTools` [CLAIMED, SS] | List the Play street, read transforms, spawn or delete a test actor |
| Any property, lights | `ObjectTools`, generic property get/set [SHOWN, create-toolset] | Read or set a light's intensity, radius, colour. No lights toolset seen. [I] |
| Materials | `MaterialTools` [SHOWN]; `MaterialInstanceTools` [CLAIMED] | Instances of `M_LedgerSurface`; copy what works into `tools/ue/make_*.py` |
| Screenshots, camera | "Editor: screenshots, camera control, actor selection, log inspection" [SHOWN]; `EditorAppToolset` also Play control [SS] | Working pictures; the image comes back inline, the original saved under `~/.claude/projects` [SHOWN] |
| Logs | `LogsToolset` [SS] | Read the game's `Ledger…` lines from the editor log |
| Editor Python | `ProgrammaticToolset.execute_tool_script`, "executes arbitrary Python inside the editor process" [SHOWN] | Last resort |
| Automation tests | `AutomationTestToolset`: `DiscoverTests` first, then `ListTests`, `RunTests`, `GetTestStatus`, `GetTestResults` [SHOWN] | Proves the toolset loads. `ue-probe/Source` has no Unreal automation tests [SHOWN, grep]; CoreTests and the `-Ledger…` switches stay |
| Compile | `LiveCodingToolset.CompileLiveCoding` [SHOWN] | **Never here**; builds go through `build-local.ps1` |

Not used: Blueprints, Niagara, Sequencer (agents do worse on Blueprints than C++ [CLAIMED, CraftBench-UE]). An editor screenshot is a working picture, not the gate's: the editor viewport has its own exposure and size. [I]

## 6. Safety rules for this project

1. Prompts on, `default` mode; read `toolset_name` and `tool_name` before approving each `call_tool`.
2. Never without reading the exact call: `ProgrammaticToolset`, `LiveCodingToolset`, any `AssetTools` save, move, rename or delete, or deleting outside the Play world.
3. Never save the open level (the engine's map or an untitled one; the street is code). Nothing here needs a save.
4. After any edit, list the actors again and compare: 35.8% of agent scene edits that hit their target also changed something else [CLAIMED, Code4Scene abstract].
5. Play-world edits die at Stop. For `/Game/Ledger` edits: commit before, `git status` after.
6. No build, cook or package during a session (two Unreal jobs never overlap).
7. Screenshots: no MetaHuman people, no NoAI items until he rules.
8. **Nothing of MCP in the build friends play.** The plugins are not in the `.uproject` and nothing in the game calls `StartServer` [SHOWN, grep of `ue-probe/Source`]. After the next packaged build prove it:

```powershell
Get-ChildItem -Recurse "F:\LedgerTools\played-game\Windows" -Filter "*ModelContextProtocol*"
```

   Expect no output; while the game runs `netstat -ano | findstr :8000` prints nothing. A Development-only tester hook is a separate decision [CLAIMED, HB 1.1].

## 7. Known faults, and what to do

- **Experimental; "many features are incomplete or missing"** [CLAIMED]; a hands-on review found some systems unreachable [SS]. If a tool is missing, use a file or script.
- **No authentication:** any process of the same user can connect [SHOWN].
- **Arbitrary Python in the editor process** [SHOWN]; one tool for everything, so no fine allow rules (section 4).
- **Game thread.** The 7 October note says calls are serial [CLAIMED]; Epic's skill says concurrent requests are accepted, order is not guaranteed, conflicting changes cause damage [SHOWN]. One dependent call at a time.
- **Busy editor:** calls hang during compile, level load or Play changes [SHOWN]. Editor-only tools behave differently in Play [SHOWN]. Wait and retry.
- **Edits are not always undoable** [SHOWN]. Undo means writing the old value back and reading it.
- **The street builds once per process.** A static flag (`GInteractiveBuilt`) blocks a second build, so a second Play in one editor session may show an empty street. [I, from the code] **(confirm)** Restart the editor between Plays.
- **Editor restart.** The server stops and does not return by itself. Claude Code retries a dropped remote server five times (about 31 seconds), then marks it failed; reconnect from `/mcp` (`/mcp reconnect all` on 2.1.284+). A stale tool list may need a client restart. Prove recovery with a read-only call [SHOWN].
- **Big results:** over 25,000 tokens are cut or saved to a file, images included [SHOWN]; ask for filtered lists.
- **Port busy** ("Failed to listen on port"): `ModelContextProtocol.StartServer 8001` or `-ModelContextProtocolPort=8001`, then change the URL in the `claude mcp` entry [SHOWN].

## 8. The first ten-minute test

Editor open with the server up, Claude Code connected, clean tree, prompts on. Two tries at a step, then research (CLAUDE.md).

**Read-only**

1. Press Play. The editor is not in `-game`, so the plain-launch street is built [SHOWN, game mode].
2. `list_toolsets`. **Pass:** it returns, naming scene or actor, materials, editor or screenshot, logs, and `AutomationTestToolset`.
3. `describe_toolset` on the actor one; list the Play world's actors. **Pass:** hundreds, including `ground_east_carriageway` [SHOWN, first piece in the file]. Zero means the street did not build (section 7). Save the list as the "before" file in scratch.
4. Hide the people (each `SkeletalMeshActor` and any cast actor; note which). Take a picture at the hook pose (section 1) with the editor camera tools. If none sets a pose, say so and take the nearest view; do not improvise Python. **Pass:** Claude sees the image, no person is in it, and the framing matches `production/previews/proof-2.6-shop-signs-from-the-hook-2026-10-04.jpg` by eye. Unhide them.
5. Find the four lanterns (point lights of radius 1800, each with a spot beneath). Read one of each with `ObjectTools`. **Pass:** point light 40 lumens, colour (1.0, 0.25, 0.0) linear, 4.78 m up; spot 500 lumens, cone 22 to 46 degrees [SHOWN, `production/specs/unreal-look.json` and `SpawnPointLight`, as of 8 October]. If the file has changed, compare with it. Day hides them; the values still read.
6. `AutomationTestToolset`: `DiscoverTests`, `ListTests` only. **Pass:** no error.

**One reversible edit**

7. Set that spot's intensity to 250; read it (250). Set it back to 500; read it (500).
8. List the actors again and compare with the "before" file. **Pass:** identical, people visible.
9. Stop Play. **Pass:** no new Output Log errors from these steps; `git status --short` shows no tracked change; no `.mcp.json`.
10. Close the editor. **Pass:** `netstat -ano | findstr :8000` prints nothing.

**Overall pass.** All ten hold, every `call_tool` was prompted, about ten minutes. Anything else goes into the summary as a named failure; it does not loosen the rules.

## 9. To check on the PC

Plugins present and where `AllToolsets` lives; `-EnablePlugins=` pulls in the toolset dependencies; "Help improve Claude" is off (Jafar's claude.ai account); whether `auto` mode gates MCP calls; which `bash` is on PATH; the `--disallowedTools` form; a second Play shows an empty street; real tool names and whether any sets the Play camera; editor viewport exposure and size against the game's frame; the Editor Preferences panel; the hook pose numbers in section 1 (converted from code, not a measured frame).

## 10. Sources

Reached on 8 October 2026:
- `raw.githubusercontent.com/EpicGames/unreal-engine-skills-for-claude-code-plugin/main/`: README.md, LICENSE, `.claude-plugin/plugin.json`, `hooks/hooks.json`, `hooks/unreal-context.sh`, `skills/unreal-mcp/SKILL.md` and its `references/setup.md` and `operations.md`, `skills/create-toolset/SKILL.md`. `skills/unreal-skill/SKILL.md` fetched, not read. The eight core files at commit `a6aa73ad…` are identical.
- `raw.githubusercontent.com/anthropics/claude-plugins-official/main/.claude-plugin/marketplace.json`; `claude.com/plugins/unreal-engine-skills-for-claude-code`.
- `code.claude.com/docs/en/`: `mcp`, `permissions`, `hooks`, `discover-plugins`, `setup`, `data-usage`.
- This repository: CLAUDE.md, DECISIONS.md, `ue-probe` config and source, `production/specs/`, `tools/ue/build-local.ps1`, `tools/ai-tester/play.py`, `production/retention.json`, the 7 October notes, the terms note, the Blender MCP note.

Not reached: `dev.epicgames.com` (no connection; the 7 October session reached it), `github.com` and `api.github.com` (403), `unrealengine.com`, `pugetsystems.com`, `dev.to`, `seeles.ai`. Three web searches gave [SS] leads only.
