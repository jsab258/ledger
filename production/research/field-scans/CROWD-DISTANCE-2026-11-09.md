# Field scan: street life and the crowd at distance, 9 November 2026

One page, all links read in full on 9 Nov 2026. Extends CROWD-2026-11-08.md (not repeated). Nothing decided. Unverified items are marked.

## 1. Skin-cache forum lead (verified, with a limit)

Source [1]: thread by Matthias, 24 Apr 2026, Epic Pro Support, tag metahuman. Engine version not stated.
- Test: 50 bald MetaHumans, development build, ray-traced visibility off. Far camera: faces at LOD7, but every person still holds an LOD0 skin-cache entry. Face cache 100 x LOD0 + 100 x LOD7; body 100 x LOD0, 80 x LOD2, 100 x LOD3. Total skin cache about 137 MB far, 142 MB moderate; LOD0 about 128 MB of it. Forcing LOD3 in Blueprint: about 31 MB. Poster's RTX 3070 (8 GB) overflows with a few NPCs near.
- Epic reply (Euan Carmichael, 1 May 2026): the cache does evict old data on LOD change. The dump likely shows stale data and other scenes' caches (PIE, editor viewport, mesh editors each have one; rhi.DumpResourceMemory counts all). Advice: test in a packaged build with one scene; tools r.SkinCache.PrintMemorySummary, the GPU Skin Cache view mode, PIX with -attachpix (13 May).
- Epic's own words: 100+ skeletal mesh components on screen is beyond what skeletal mesh was designed for (engine limit, worse with MetaHumans). Suggested City Sample shape: about 8 full-actor simplified MetaHumans (body and head), the rest Mass entities with vertex animation, swapped by screen distance.
- Status: no confirmed fix; the packaged-build result was never posted. So the 128 MB for 50 people (about 2.5 MB per person LOD0 cache) is unverified for a packaged build. This is a measurement for LEDGER to make, not a fact.

## 2. MetaHuman 5.8 pages

- metahuman.com announcement [2]: not read. The URL redirects to an Epic sign-in; not followed (no logins). Its content is covered only through [3] and [4].
- Release notes [3] (Epic docs): MetaHuman Crowd plugin, experimental, "tens to thousands" of characters, built from modular parts; switches between full actors and Instanced Skeletal Meshes by camera distance; animation by Unreal Animation Framework or simple sequences; simulation in Mass; "Crowd face textures are said to have a reduced memory footprint" with no figure. Per-platform max/min LOD in DNA assets, so a cook ships only its LOD range (re-cook needed). Option for "heavily optimized" scalable normal textures at assembly. Unbaked textures (for look development; baking stays on by default). Cooked DNA cuts runtime init cost. The page names no dedicated "cheaper face texture" switch; the crowd face texture and the scalable normal option are the closest. No numbers for memory or frame time anywhere on it.
- Release forum post [4], 17 Jun 2026: "hundreds on mobile, thousands on high-end" (Epic's claim, no hardware stated). Sample: "MetaHuman Crowds Sample" on Fab (price and licence not read: unverified). Tech talk, Unreal Fest Chicago, 20 Jul 2026 (not watched).
- User benchmark in [4] (POKATILO_3D, 1 Aug 2026, 300 MetaHumans): CPU cost of passing scalar curves to materials, 20 to 30 fps lost against 1 to 2 fps for texture blending. Epic reply (Henry Falconer, 18 Aug): Material Parameter Caching is on by default for MetaHumans (custom Blueprints may need it on the face mesh); head-movement IK can be switched off; fewer bone influences cause skinning artefacts; Nanite not default because of translucency. Hardware of the benchmark not given: unverified for an RX 6700.
- Crowds page [5]: re-read; confirms the 8 Nov points (experimental caution, retained LODs set in the Collection, hair cards, ISKM skips correctives). Sample on Fab with tutorial. No memory or limit numbers.

## 3. What changes for the question set

- How many full MetaHumans near the camera: Epic's only stated figure is about 8 (forum, a staff opinion, not a spec) [1]. Kingdom Come II 70 within 150 m and Unity's 40 real AIs are in the 8 Nov scan.
- Memory per person in a packaged build: no published figure. The only measurement (about 2.5 MB skin cache per person at LOD0, development build) is disputed by Epic [1]. Unverified.
- Beyond the near ring: Epic's route is the Crowds plugin with ISKM [3][5]; City Sample's route is vertex animation, which Epic says does not suit per-person unique meshes (Mutable-built people) without a baked bone texture per skeleton [1].
- Cheap levers on offer now: per-platform LOD range in DNA; the crowd's optimised face texture; the scalable normal texture option; Material Parameter Caching.

## 4. Licences

- MetaHuman Crowd plugin and Fab sample: Epic's MetaHuman licence terms not read; the sample's Fab licence not read. Nothing may be used until checked against ledger-v2/research/license-allowlist.md. Unverified.
- Forum posts: read only, no code taken.

## Not reached

metahuman.com announcement (sign-in redirect); Unreal Fest talk; the Fab sample page and its licence; Crowds Getting Started and Sample Tutorial pages; GDC slides listed unreached on 8 Nov; any packaged-build memory report; Epic's Mass Crowd page.

## Recommendation

Measure before choosing: in one packaged build with one scene, spawn the game's present MetaHumans at 1, 5, 10, 20 and record memory per person with r.SkinCache.PrintMemorySummary and PIX (the method Epic named), once at default LOD and once with LOD0 forced off. Then, if the number is too high, try the Crowds plugin on 5 to 10 people for the ring beyond about 8 near ones. Read the Fab licence first.

## Sources (read 9 Nov 2026)

1. https://forums.unrealengine.com/t/metahuman-skin-cache-retains-lod0-entries-for-every-npc-regardless-of-camera-distance/2728166
2. https://www.metahuman.com/news/metahuman-5-8-is-now-available (unreached)
3. https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine
4. https://forums.unrealengine.com/t/metahuman-5-8-released/2729288
5. https://dev.epicgames.com/documentation/metahuman/metahuman-crowds-in-unreal-engine
