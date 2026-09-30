# LEDGER — adversarial audit, 30 September 2026

Audited `main` at [aba6603a](https://github.com/jsab258/ledger/commit/aba6603a), 30 September, 09:10 CEST, against changes since 28 September, 14:40. **The central failure remains producing components faster than proving the experience they are meant to create.**

1. **The playable game is substantially shallower than the implemented simulation.**

   Ordinary play still waits **40 seconds after the smash**, relocates the witness, runs gossip, and advances directly to day four’s evening. That remains an encounter demonstration. The arrangement, waiting, police, week ending and unified town save have ports and comparison tests, but do not govern that playable sequence. See [`CrimeProbe.cpp`](https://github.com/jsab258/ledger/blob/aba6603a/ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp#L5755-L5799) and [handover status](https://github.com/jsab258/ledger/blob/aba6603a/NOW.md).

   Conversation—the distinguishing interaction—still falls back to “that’s all I know” in **31–38 of 60 newcomer questions**. The failed fixes alternately refuse truthful paraphrases or admit inventions. More residents, friendships and police rules cannot repair this bottleneck. [Recorded results](https://github.com/jsab258/ledger/blob/aba6603a/production/research/grounded-replies/NOTE-2026-09-29.md).

   I independently reproduced a deeper correctness failure: `Arrangement.Answer` accepts Wednesday’s completed delivery while the supplied clock is still Monday. The [C++ implementation](https://github.com/jsab258/ledger/blob/aba6603a/ue-probe/Source/LedgerProbe/Public/Arrangement.h#L148-L156) faithfully copies the C# defect. Agreement between implementations does not establish sensible gameplay.

2. **Several workstreams are correcting outputs without correcting their production method.**

   The professional practices below come from primary sources. Their application to live generated dialogue is my recommendation, not an established studio standard.

   | Workstream and evidenced failure | Appropriate method |
   |---|---|
   | **Clothes:** whole-garment simulation, then repeated stiffness and sleeve repairs. The corrected skinned jacket has already failed two further reviews. [CLOTHES](https://github.com/jsab258/ledger/blob/aba6603a/CLOTHES.md). | Shape, retopologize, skin, correct joint weights, then simulate selected loose regions. Validate deformation in-engine before producing a wardrobe. Epic’s cloth controls explicitly constrain movement relative to the animated mesh. [Epic: Clothing Tool](https://dev.epicgames.com/documentation/unreal-engine/clothing-tool-in-unreal-engine?lang=en-US). |
   | **Faces:** four rounds of portrait measurements and adjustments in [c788451f](https://github.com/jsab258/ledger/commit/c788451f). | Establish a three-dimensional identity under neutral, consistent lighting; inspect multiple views; conform/sculpt and validate expressions. A single portrait cannot specify the head’s unseen geometry. Freeze the approved heads now. [Epic: Mesh to MetaHuman](https://dev.epicgames.com/documentation/metahuman/from-mesh). |
   | **Voices and acting:** the recorded accent calibration rejects **24/50 genuine Scottish clips**; Darren’s approved voice scores Scottish in **0/12** generated lines. [Calibration](https://github.com/jsab258/ledger/blob/aba6603a/production/research/voice-alternatives-2026-09-24/SCOTTISH-CHECK-2026-09-29.md). | Approved character reference → directed performance → selected takes → editing/mixing → contextual listening. Use classifiers as fallible screening. Apply that sequence to the permitted synthetic voices; no hiring requirement follows. [Ubisoft: voice production](https://toronto.ubisoft.com/people-of-ubisoft-toronto-meet-johnny-lucas-voice-designer/). |
   | **Speech delay:** [FOR-JAFAR](https://github.com/jsab258/ledger/blob/aba6603a/FOR-JAFAR.md) advertises about three seconds, but [FINDINGS](https://github.com/jsab258/ledger/blob/aba6603a/FINDINGS.md) identifies stand-in text; [`latency.py`](https://github.com/jsab258/ledger/blob/aba6603a/tools/voice-live/latency.py) explicitly uses `--fake`. | Measure Enter → real generation/checking → actual audible output while playing. Reduce the serial call chain and prompt volume; stream safe clauses and precompute fixed lines. Streaming/prewarming already exist, so repeating those recommendations is insufficient. [Anthropic: reducing latency](https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency). |
   | **Animation:** thinking sounds froze the mouth driver, fixed in [c7ab538f](https://github.com/jsab258/ledger/commit/c7ab538f); amplitude-driven jaw opening remains rudimentary. | Explicitly compose body, gaze and facial layers; retarget with foot/contact checks; use facial curves for speech where affordable. Amplitude jaws are acceptable placeholders, not completed acting. Benchmark Epic’s facial solution before adopting it. [Epic: audio-driven animation](https://dev.epicgames.com/documentation/metahuman/audio-driven-animation); [foot sliding and IK](https://dev.epicgames.com/documentation/unreal-engine/fix-foot-sliding-with-ik-retargeter-in-unreal-engine?lang=en-US). |
   | **Lighting:** approval frames and gameplay used different night exposure until [771de38e](https://github.com/jsab258/ledger/commit/771de38e). | Share camera/exposure settings and judge faces, materials and readability through the playable camera across lighting transitions. Portrait-only iteration was measuring a different presentation. [Epic: exposure](https://dev.epicgames.com/documentation/en-us/unreal-engine/auto-exposure-in-unreal-engine). |
   | **Dialogue writing:** unrestricted drafting followed by probabilistic rejection produces the fallback/invention trade-off. [Conversation engine](https://github.com/jsab258/ledger/blob/aba6603a/ledger/Assets/Scripts/Core/ConversationEngine.cs). | Studio contextual dialogue selects authored responses against explicit world facts. For LEDGER, select supported facts and conversational intent before wording; author indispensable beats; judge paraphrases against labelled examples. Preserve free conversation without making generation the authority on game state. [Valve/GDC: contextual dialogue](https://gdcvault.com/play/1015946/AI-driven-Dynamic-Dialog-through). |
   | **Interiors:** two research rounds seeking an exact period office photograph precede a proposed multi-day room build. [Overview](https://github.com/jsab258/ledger/blob/aba6603a/FOR-JAFAR.md). | Build a measured, playable blockout from functional requirements and several references; test routes, camera and interactions before dressing it. An exact photograph is not a prerequisite. [Epic: level blockout](https://dev.epicgames.com/documentation/en-us/unreal-engine/designer-01-project-setup-and-level-blockout-in-unreal-engine). |
   | **Testing:** I reran **56,997 checks: zero failures**, against committed golden results. The latest [“live” verdict](https://github.com/jsab258/ledger/blob/aba6603a/production/d1-probe/ue-encounter-live-1-verdict.txt) says `talkFake=yes`, `voice=not-asked`. | Keep deterministic comparisons, but add independent behavioural expectations and tests of the packaged application through actual inputs. The typing bug fixed in [72802eca](https://github.com/jsab258/ledger/commit/72802eca) demonstrates the missing layer. Epic supports packaged functional testing. [Epic: running Gauntlet tests](https://dev.epicgames.com/documentation/en-us/unreal-engine/running-gauntlet-tests-in-unreal-engine). |

3. **What moved, and how much of the activity counts as game work.**

   My classification of the [audited history](https://github.com/jsab258/ledger/compare/7868b764...aba6603a): **302 commits**, including **74 automatic probe returns**. Of the remaining 228:

   | Category | Commits | Share |
   |---|---:|---:|
   | Runtime, content, asset-generation sources | 150 | 65.8% |
   | Tools, infrastructure, tests | 40 | 17.5% |
   | Records only | 27 | 11.8% |
   | Research and evidence | 11 | 4.8% |

   This generously credits mixed commits and unwired simulation as game work. **It cannot establish hours spent or the percentage that changed the playable experience.**

   Concrete changes include the [title screen and grounded run](https://github.com/jsab258/ledger/commit/089e1ba9), [recorded footsteps and moving mouths](https://github.com/jsab258/ledger/commit/3fcc66b4), [two pavement walkers](https://github.com/jsab258/ledger/commit/7bee296e), [boots/handbag integration](https://github.com/jsab258/ledger/commit/c7ab538f), and [opening instructions](https://github.com/jsab258/ledger/commit/6f7ac726). These change presentation and usability. They do not yet establish a sustained first week.

4. **The lanes are distinct; their acceptance and integration boundaries are weak. Waste follows those boundaries.**

   The builder owns **17 of the twenty friends-build priorities**, with three shared. Town and clothing therefore feed one integration bottleneck. Worse, the [priority list](https://github.com/jsab258/ledger/blob/aba6603a/production/research/checklist-sweep-2026-09-29/BUILDER.md) places the running clock *below* the twenty despite acknowledging that the first-week handovers require it.

   The spectacles fitted to Sheila’s superseded head, then [refitted to S4](https://github.com/jsab258/ledger/commit/ddf6001c), demonstrate missing version contracts between lanes. Unreal work also collided with its build runner until explicit waiting was added in [964df71f](https://github.com/jsab258/ledger/commit/964df71f).

   The overview generally distinguishes ports, editor work and packaged work. Its latency headline is misleading because it omits real text generation.

   Specific waste:

   - **Fourteen jacket rounds**, followed by another failed manufacturing approach; **seventeen clothing research notes** while the end-to-end method remained unresolved. [Records](https://github.com/jsab258/ledger/blob/aba6603a/FOR-JAFAR.md).
   - **Twelve town checklist sweeps**; the builder initially called **359 rows necessary**, reduced to twenty only after intervention. [Sweep](https://github.com/jsab258/ledger/blob/aba6603a/production/research/checklist-sweep-2026-09-29/BUILDER.md).
   - A newcomer benchmark labelled approximately **$1** cost approximately **$14.50**. [TOWN](https://github.com/jsab258/ledger/blob/aba6603a/TOWN.md).
   - The reported **46 unnoticed paid playtests** are consistent with the removed push-triggered, secret-enabled workflow. I verified that mechanism, not the run count or bill. [Removal](https://github.com/jsab258/ledger/commit/28770ea6), [owner ruling](https://github.com/jsab258/ledger/blob/aba6603a/DECISIONS.md).

5. **Earlier audit findings: controls held more reliably than production discipline.**

   Against the [24 September audits](https://github.com/jsab258/ledger/tree/aba6603a/production/audits):

   - **Implemented and retained:** player crime/talk inputs and disk-reload checks; golden comparisons; content screening; approval invalidation; removal of the sitting clock and compacting ROADMAP. I reran the recorded encounter-verdict checks and content gate successfully. [Tests/tools](https://github.com/jsab258/ledger/tree/aba6603a/tools), [rules](https://github.com/jsab258/ledger/blob/aba6603a/CLAUDE.md).
   - **Slipped:** one complete character before multiplication; one garment proven on two bodies before wardrobe expansion; short working records. NOW and TOWN now contain approximately **20,477 words**. [NOW](https://github.com/jsab258/ledger/blob/aba6603a/NOW.md), [TOWN](https://github.com/jsab258/ledger/blob/aba6603a/TOWN.md), [CLOTHES](https://github.com/jsab258/ledger/blob/aba6603a/CLOTHES.md).
   - **Still unproven:** a self-contained release on another PC with actual voices. Packaging remains [Development](https://github.com/jsab258/ledger/blob/aba6603a/.github/workflows/ledger-probe-unreal.yml#L501); voice startup still requires external Python/script arguments. [Startup](https://github.com/jsab258/ledger/blob/aba6603a/ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp#L2804-L2808).

6. **Road to playing: integrate one consequential route, then distribute it.**

   My **low-confidence estimate**, assuming frozen scope: **3–7 focused builder working days** to an owner-testable, potentially worthwhile session; **another 1–3 weeks** to a thirty-minute friends build.

   The blockers are meaningful newcomer replies, measured live speech, a running clock, one complete consequence chain, accessible interior/camera, persistence and portable voice dependencies—not additional town depth. These are already exposed in [NOW](https://github.com/jsab258/ledger/blob/aba6603a/NOW.md).

   The **single biggest risk** is that real conversation remains slow, empty or unreliable enough to invalidate the premise. These ranges estimate reaching a credible test, not guaranteeing the owner enjoys it.

7. **Next goals, with explicit stops.**

   - **Builder:** (1) wire clock, action, gossip, consequence and reload into one continuous route; (2) measure real typed conversation through audible playback under gameplay load; (3) package and walk thirty minutes on a clean second PC. **Stop** optional visual iteration while that route is broken. [NOW](https://github.com/jsab258/ledger/blob/aba6603a/NOW.md).
   - **Town:** (1) repair grounded replies against fixed newcomer questions and independent labels; (2) fix temporal/state defects, including future deliveries; (3) support integration of that route with precise inputs, outputs and acceptance cases. **Stop** additional systems, checklist sweeps and review rounds on unreachable depth. [TOWN](https://github.com/jsab258/ledger/blob/aba6603a/TOWN.md).
   - **Clothing:** (1) finish one properly skinned jacket; (2) prove it on two approved bodies while walking, sitting and raising arms in Unreal; (3) complete the principals’ outfits using that proven pipeline. **Stop** new garment families and standing-only acceptance. [CLOTHES](https://github.com/jsab258/ledger/blob/aba6603a/CLOTHES.md).

**Confidence:** high in inspected code/history and checks I ran; medium in production diagnosis; low in scheduling. I could not run Unreal, regenerate goldens with .NET, hear current live voices, inspect the owner’s PC/private approval pages, verify billing, or test the distributed build.
