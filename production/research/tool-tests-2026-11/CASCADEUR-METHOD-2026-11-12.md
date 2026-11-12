Method note for Cascadeur scripting (12 Nov 2026)

All read 2026-11-12. Nothing run, downloaded or installed.

## 1. Scripting
- Commands: a .py file with command_name() (menu name) and run(scene); loaded at launch into the Commands menu; edits need "Reload scripts". Docs say Python 3.8; the plan says 3.11 (unverified which; install not checked). Source: https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur
- The page gives the user-commands folder only in a screenshot (path unread, unverified).
- Install file C:\Program Files\Cascadeur\resources\settings.json: "ScriptsDir": "./resources/scripts"; Python keys Path, Commands ["commands"], Scripts ["scripts"], Events ["events"]; LiveLink 127.0.0.1:5454.
- Docs place settings.json (ScriptsDir, empty by default) in the Resources folder of the install: https://cascadeur.com/help/installation/file_structure
- Another settings.json exists at C:\Users\Jafar\AppData\Local\Nekki Limited\Cascadeur\settings.json (ScriptsDir "", no Events key). The docs do not mention it. Which file the app reads is unverified.
- Event hooks: resources\scripts\python\events\ (application_started, scene_opened, scene_idle and others) are empty managers, subscribed to by code. Nothing shows a user script path being imported at start other than the reloader (resources\scripts\python\reloader.py), which warms the "commands" and "scripts" packages.
- Script server, shipped in the install: scripts\mcp\start_server.py, command "MCP.Start script server" (Scripts menu, per the help site). Its server.py starts an HTTP server on 127.0.0.1:8765 with GET /health, POST /run {"code": ...} and POST /mcp (one tool, run_script). Code runs on the next scene idle event, 30 s timeout, with csc, scene and app in scope. Source: C:\Program Files\Cascadeur\resources\scripts\python\scripts\mcp\script_server\server.py. Starting the server needs the command to be run once inside the app. Nothing read shows an auto-start (unverified).

## 2. Command line
- Neither the file structure page nor the Python scripting page documents command-line options. The API index mentions none. Not found in the docs read; the app's own options are unverified (the binary was not inspected). The install's Python files contain no argv or script-path handling (search of resources\scripts\python found only the server, reloader and Meshy bridge files).
- Python API index: https://cascadeur.com/python-api/index.html (only the first 200,000 of 482,292 characters were read).

## 3. Settings location
- Docs: AppData\Local\Nekki Limited\Cascadeur holds Cascadeur.ini, Cascadeur_service.ini, Hotkey_settings.ini, Cascadeur_tools.ini; missing files are recreated; Resources\settings.json holds ScriptsDir. No documented override and nothing about read-only files. The docs name .ini files; the AppData settings.json is not described there.

## 4. FBX on the free licence
- The plans page lists export for Free as CASC only: ".fbx and .dae are not available"; Indie adds them. Non-commercial use only on Free (the page also mentions a revenue threshold under US$100,000, inconsistent; unresolved). Free import formats are not listed on the page (unverified). https://cascadeur.com/plans
- The API has csc.fbx.FbxLoader (import_model, import_scene, import_animation, export_model, export_scene_selected, export_all_objects) and FbxSettings (bake_animation, apply_euler_filter). Whether the free licence blocks these calls is unverified.

## 5. Physics tools by name
Action ids (https://cascadeur.com/help/category/301), run through csc.app.ActionManager.call_action():
- AutoPhysicsTool.Switch Auto Physics, .Switch Frozen Auto Physics, .Snap to Auto Physics, .Set priority frame
- View.FixFoot, View.FixFoot_KeepKeyFrames (Fulcrum Motion Cleaning)
- AutoPosingTool.AutoPosing, .Update, .AutoUnlock, .SwitchLock
- File.Import.Animation.Fbx..., File.Export.Animation.Fbx... (these open dialogs; use FbxLoader instead)
Python classes csc.tools.AutoPhysicTool (turn_off, turn_off_all_fulcrum_points) and csc.tools.AutoPosingTool (add, update). Signatures and the call_action argument form were not read (unverified).

## Not reached
- https://cascadeur.com/help/python_scripting (404). The Python API pages past character 200,000 were not read. Cascadeur's command-line support was not checked in the executable.
