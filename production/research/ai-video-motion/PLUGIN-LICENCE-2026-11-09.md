# MetaHuman Animator Markerless Motion Capture plugin: licence notes (read 9 Nov 2026)

Status: the governing licence is NOT confirmed. The binding texts could not be read. No conclusion is drawn here.

## Q1. Which licence governs

- Fab listing (https://www.fab.com/listings/4095b8e0-3eff-44f1-acb4-cb40b99228b9, read 9 Nov 2026): licence field "-" (blank); price Free (0.0 CHF); publisher Epic Games; "Allows usage with AI": No; "Generated with AI": No. Description: "Your footage never leaves your workstation"; "Everything runs on your own machine." No experimental or territory text on the listing as returned.
- https://www.fab.com/eula (read 9 Nov 2026) is a summary only. It says it is "for your convenience only and is not legally binding"; the full EULA text was not delivered. The summary covers the Standard License and CC-BY only and says nothing on free or Epic-published plugins. Unverified: which licence applies to this listing.
- Search result (not a primary source, unverified): CG Channel reports the plugin is free including for commercial projects; MetaHuman's licence page says free under $1M revenue, Unreal Engine standard terms above. The MetaHuman licence page itself was not read (login redirect).
- Third-party forum post (https://forums.unrealengine.com/t/licensing-question-shipping-metahuman-animator-markerless-motion-capture-runtime-models-in-a-steam-game/2839692, read 9 Nov 2026), by user SangNo, 12 Oct 2026: cites Fab EULA section 5(b) (plugin-based projects distributed only as Engine Tools under the Unreal Engine Agreement) and asks whether the plugin's data may be cooked into a Shipping build. Claimed, unverified, since the EULA text was not read. No Epic reply on the page. Reply by ChenDong (13 Oct 2026, not identified as Epic staff): "Nobody on the forum can clear this"; "Experimental means unsupported and allowed to change or break"; "do not bake the experimental models into a Shipping build you sell." The post says the model files (camera_calib, Detectron2, chmr folders) carry their own LICENSE files; unverified. The post also says the SMPL-X licence (Max Planck) bars commercial use; unverified.

## Q2. Clauses

- Commercial use inside a game: Standard License summary only: "Commercially distribute your Projects with the Fab assets incorporated into it." (https://www.fab.com/eula, 9 Nov 2026). Whether it applies to this plugin: unverified.
- Output (animation) in a shipped game: no clause found. The forum page's product text says body animation is "ready to drive the MetaHuman skeleton directly or retarget to other character types" and "can be refined and adapted within Sequencer" (https://forums.unrealengine.com/t/epic-games-metahuman-animator-markerless-motion-capture-plugin/2729293, 9 Nov 2026). That describes use, not a licence. Unverified.
- AI / NoAI: listing flags only "Allows usage with AI: No", "Generated with AI: No". No AI clause text read.
- Territory: none found (listing and summary silent). Unverified.
- Experimental disclaimer: "MetaHuman Animator Markerless Motion Capture plugin is an experimental feature introduced in Unreal Engine 5.8." "Experimental features are not production-ready and may change or be removed in future releases." Windows only. (https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine, 9 Nov 2026). The page has no licence text.

## Q3. Allowlist (ledger-v2/research/license-allowlist.md, read 9 Nov 2026)

No line names this plugin or markerless capture. The nearest is line 2 (3D): "Fab items under the Fab Standard License, never one marked NoAI except content Epic itself publishes on Fab (Quixel Megascans, the MetaHuman garments, the Game Animation Sample), which may be used inside the game even when tagged NoAI because our AI only places and sets it up and never trains on it". It depends on the listing being under the Fab Standard License, which is unconfirmed (blank field). Line 3 (Characters) says: "MetaHuman ... Unreal-only content (the Epic Content License's MetaHuman addendum ...), under the Unreal EULA (royalty-free below $1M a product), never put in a database for, nor used to train or test, an AI (Unreal EULA 6(e)...)". Whether it extends to a plugin is unverified. No animation-tool line exists (Mixamo animations sit in line 3).

## Q4. Not reached

- Full Fab EULA text (fab.com/eula gave a summary only; fab.com/licenses 404; epicgames.com/site/en-US/fab-eula 403).
- Epic Content License (unrealengine.com/en-US/eula/content, 403).
- metahuman.com/en-US/license (login redirect, not followed).
- dev.epicgames.com plugins-overview page (empty body returned).
- Unreal Engine EULA text; the plugin's bundled LICENSE files; the forum thread's second page.
