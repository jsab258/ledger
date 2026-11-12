# CMU mocap: terms, FBX conversion, clip candidates (read 12 Nov 2026)

Questions
1. CMU's own terms: commercial game use, credit, converted forms, AI/ML clause.
2. FBX conversion on 4TU.ResearchData: licence, author, credit, sizes, format notes; other free conversions and their terms.
3. Clip candidates: sit down, stand up, lean, standing gestures, turn on the spot, idle.
4. Known quality issues relevant to retargeting.

## Sources read
- 4TU dataset page https://data.4tu.nl/datasets/0448aab2-3332-449f-a8e2-d208cb58c7df (12 Nov 2026)
- 4TU CFF export https://data.4tu.nl/export/cff/datasets/0448aab2-3332-449f-a8e2-d208cb58c7df (12 Nov)
- cgspeed announcement, July 2010 https://groups.google.com/g/bvhacker/c/r906SGjjcTA (12 Nov)
- cgspeed READMEFIRST.txt as mirrored https://raw.githubusercontent.com/sfd158/cmu-mocap/master/READMEFIRST.txt (12 Nov)
- CMU motion index text, as mirrored https://raw.githubusercontent.com/sfd158/cmu-mocap/master/cmu-mocap-index-text.txt (12 Nov)
- https://github.com/Shriinivas/cmubvh (12 Nov); https://github.com/sfd158/cmu-mocap (12 Nov)
- https://www.roboticscenter.ai/datasets/cmu-mocap/ (secondary summary, 12 Nov)
- Search result snippets (not primary): KIT motion database listing for 143_19, 141_17, 14_27 sample rates.

Note: pages were read through a fetch tool that summarises; quotes below are as returned, short. Not a raw-file read.

## Not reached
- mocap.cs.cmu.edu (home, faqs.php, info, subject pages): both http and https failed with "unable to verify the first certificate". CMU's own terms page was therefore NOT read. Nothing was done to get round this.
- web.archive.org: fetch tool refused.
- 4TU file download of cmu-mocap-index-text.txt: HTTP 403, not retried by other means.
- The linked GitHub pipeline README for the FBX set: not read.
- cgspeed.com itself: not read.

## 1. CMU terms (CMU page unreached; text below is quoted by others)
The 4TU page (12 Nov) quotes CMU: "This data is free for use in research projects." / "You may include this data in commercially-sold products," / "but you may not resell this data directly, even in converted form." Credit: "If you publish results obtained using this data, we would appreciate it if you would send the citation to your published paper to jkh+mocap@cs.cmu.edu"; acknowledgment text "The data used in this project was obtained from mocap.cs.cmu.edu."; funding "NSF EIA-0196217".
The 2010 cgspeed announcement quotes CMU's older wording: "Use this data! This data is free for use in research and commercial projects worldwide." and "All of the files are free".
cgspeed README (via mirror): "CMU places no restrictions on the use of the original dataset"; Bruce Hahne adds none to his BVH conversion.
- Commercial game: the quoted text allows inclusion in commercially sold products. UNVERIFIED against CMU's own page.
- Credit: a request (appreciated), tied to published results; no mandatory credit line found. Unverified at source.
- Converted forms: no resale of the data directly, even converted (the mirror snippet is confirmed as quoted on 4TU, not on CMU).
- AI/ML clause: none found in any text read. Unverified (CMU page unread).
- The 4TU text and the 2010 text differ ("research projects" vs "research and commercial projects"); which is current on CMU is unconfirmed.

## 2. FBX conversion (4TU.ResearchData)
- Title: "FBX Conversion Of The CMU Graphics Lab Motion Capture Database". DOI 10.4121/0448aab2-3332-449f-a8e2-d208cb58c7df.v2. v1 2024-06-12; v2 2025-04-07.
- Licence on the 4TU record: CC BY-NC 4.0 (page and CFF export). This sits beside CMU's text that allows commercial products; the conflict is not resolved by any page read.
- Authors: CMU Graphics Lab; Anish Abhijit Diwan (ORCID 0000-0003-3032-4156). Citation form: Version 2, 4TU.ResearchData (2025), DOI above.
- Files: CMU_fbx.zip 1,917,480,550 bytes; cmu-mocap-index-text.txt 71,345 bytes; cmu_mocap_task_index.csv 78,050 bytes; cmu-mocap-task-legend.txt 597 bytes.
- Frame rate, units, joint names, T-pose: not stated on the page (README on its GitHub repo not read). Unverified.
- A web-search summary said the FBX came from a Unity conversion by Ward Dewaele (cMonkeys) and an index by B. Hahne; this was from the search tool, not read on a page. Unverified.
- The page advises higher-numbered subjects first: lower-numbered sessions are earlier captures and may be lower quality (CFF export summary).
- Other conversion: cgspeed BVH (Bruce Hahne, 2010): no added restrictions on the conversion; 120 fps kept; T-pose added as frame 0 facing +Z; joints renamed to MotionBuilder convention; arms 5 degrees down; retargeted for Daz gen3/gen4 (primary/secondary and hip-uncorrected variants, about 2,500-2,600 files). Not designed for non-Daz characters.
- roboticscenter.ai says "free for all uses" (secondary, unreliable).

## 3. Clip candidates (CMU index text; no frame counts or lengths in the index)
Index has descriptions only. Sample rate noted by KIT snippets: 14_27 120 Hz; 141_17 and 143_19 60 Hz (snippet, unverified).
- Sit down / stand up (single person): 13_01 to 13_03 "sit on high stool, stand up"; 14_27, 14_28 same; 14_31, 14_32, 14_36 "sit on stepstool, stand up"; 15_10 "sit on high stool, stand up"; 111_09 to 111_11 "get up from chair"; 113_15 "Sit in chair and get up"; 114_04, 114_06 "Getting up from chair"; 114_05 "Sitting in chair"; 143_18 "Sit Down And Get Up"; 141_17 "Sit on Stool"; 75_17 to 75_20 low/medium/high sit. (111, 113, 114 are pregnant/post-pregnant subjects; adult-only note for project's use.)
- Lean: 22_18 / 23_18 "leans with hands on high stool" (two-person); 15_06 "lean forward, reach for"; 69_73 "walk up to object, lean over, pick up". No wall/counter lean found.
- Standing gesture: 18_08 "conversation - explain with hand gestures" (also 19_08); 18_10 "quarrel - angry hand gestures"; 111_25, 113_16, 141_21 "Shrug"; 141_16 "Wave Hello"; 143_25 "Waving"; 139_25 "Giving Directions"; 13_26 to 13_28 "direct traffic, wave, point".
- Turn: 76_10 "turning"; 16_17 "walk, 90-degree left turn" (and 16_19 right); 134_03 "Lean Turn Right". No pure on-the-spot turn confirmed.
- Idle: 77_02 "standing"; 82_01 "Static pose"; 111_28 / 113_21 "Standing still"; 140_06, 140_07 "Idle"; 141_20 "Waiting"; 77_01 "looking around"; 139_01 "Looking Around"; 137_28 "Normal Wait"; 40_10 "wait for bus".
Counts listed: sit/stand about 20; lean 3 (none wall/counter); gesture 9 groups; turn 3; idle 9. Descriptions are the index's wording; trials not viewed.

## 4. Quality issues
- cgspeed announcement (12 Nov): data "contains a wide variety of joint-flipping problems"; earlier-numbered directories "have a lot of joint-flip problems"; raw data not cleaned; hip-correction script "occasionally... introduces foot-slip / floor-contact problems" (e.g. 144_05); 120 fps preserved, 30 fps suggested for playback.
- cgspeed README: CMU captured no finger data; finger joints are placeholders; original format ASF/AMC.
- 4TU page: lower-numbered subjects earlier, lower quality.
- Foot sliding or noise beyond the above: no primary measurement read. Unverified.
