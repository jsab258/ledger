# Stock footage for body-capture proof and real-footage control (read 2026-11-09)

Method: pages fetched through a summarising fetch tool (not raw text), so quotes are the tool's extracts. Nothing was downloaded. No clip was watched, so camera movement, whole-body framing and occlusion are UNVERIFIED for every clip; the pages state none of it.

## 1. Licences

Pexels licence, https://www.pexels.com/license/ (read 2026-11-09):
- Commercial: "All photos and videos on Pexels are free to use." Ads and marketing campaigns are named as allowed.
- Not allowed: "Don't sell unaltered copies of a photo or video, e.g. as a poster, print or on a physical product without modifying it first." "Don't redistribute or sell the photos and videos on other stock photo or wallpaper platforms."
- Modification: "You can modify the photos and videos from Pexels."
- People: "Identifiable people may not appear in a bad light or in a way that is offensive."
- Games or software, AI or machine learning, scripts: not mentioned on this page.

Pexels terms of service, https://www.pexels.com/terms-of-service/ (read 2026-11-09, extracts only; section numbers as the tool reported them, UNVERIFIED because Pexels and Pixabay returned identical numbering):
- Scraping or robots barred "for all unauthorised purposes, including without limitation for machine learning purposes" (Sec. 8). "Bulk, large-scale or systematic copying of Content is strictly prohibited" without permission.
- Standalone sale or distribution of content is prohibited (Sec. 5). Content with recognisable people: no immoral or illegal use (Sec. 5). Pexels does not warrant that releases exist.
- Uploaders must hold releases (Sec. 7A). Licence is "irrevocable, worldwide, perpetual ... non-exclusive and royalty-free" (Sec. 5).
- Pexels' own ML use of uploads is described in Sec. 7A. No clause found on a licensee using clips with AI or ML tools. Absence is not a confirmation.

Pixabay Content License summary, https://pixabay.com/service/license-summary/ (read 2026-11-09). The page says only the full licence is binding.
- "You cannot sell or distribute Content (either in digital or physical form) on a Standalone basis." "Standalone means where no creative effort has been applied to the Content."
- Modify or adapt into new works: allowed, subject to Prohibited Uses.
- "You cannot use Content in any immoral or illegal way, especially Content which features recognisable people." "It is your responsibility to check whether you require the consent of a third party or a license to use Content."
- Games or software, AI or ML, releases, scripts: not on the summary page.

Pixabay terms, https://pixabay.com/service/terms/ (read 2026-11-09, extracts only):
- Section 5 grants use "for commercial or non-commercial purposes", modify or adapt allowed. Responsibility for permissions "always rests solely and exclusively with you."
- Games or software: not addressed.
- Section 8: scraping barred "including without limitation for machine learning purposes"; "Bulk, large-scale or systematic copying of Content is strictly prohibited unless explicit permission has been granted"; "programs or robots for automatic data collection" barred. Single manual downloads are not addressed.
- Uploaders must hold releases (Sec. 7A). Licence is conditional on no Prohibited Uses.
- The tool could not give the full text of section 5 (quote length limit). Wording on AI use by the licensee is UNVERIFIED either way.

## 2. Against the allowlist
Source: C:\Users\Jafar\ledger-local\ledger-v2\research\license-allowlist.md (read 2026-11-09). Neither Pexels nor Pixabay is named. Nearest lines: SHIP-SAFE 2 "CC0 libraries (Poly Haven, ambientCG, Sketchfab CC0 filter)", which is about 3D. NEVER SHIP 5 "Real brands, logos, car models, lyrics, likenesses". PROCESS 1 "Every asset and generated output carries a license tag; untagged fails the license gate." PROCESS 2 "New tool adoption requires a decision record citing the weights license."
Finding: both licences are OUTSIDE the allowlist (not listed, not CC0, not implied). The allowlist has no line on stock video, and its footage use here would be as a motion source or test control, not shipped art. Whether that needs a ruling is for the project; not decided here. Real people's likeness appears in clips (see NEVER SHIP 5).

## 3. Epic's capture guidelines
https://dev.epicgames.com/documentation/metahuman/metahuman-animator-video-capture-guidelines-in-unreal-engine (read 2026-11-09; covers face, body and combined mono video):
- Rate and size: 60 fps; HD or 4K; "H.264 at CRF 18 or better" (about 25 Mbps for HD). Face at least 1/30 of image width and height.
- Framing (body): "full body should be visible from head to feet with a clear margin on all sides"; camera straight on, neutral height.
- Camera: fixed for the whole take (tripod).
- Light (body): even, diffused, no harsh shadows; avoid over/underexposure, backlight, motion blur.
- Clothes: form-fitting or neutral; distinct from background and floor; not all one colour matching the set; avoid loose maxi skirts or wide trousers; shoes contrast with floor.
- Occlusion: nothing blocks the body (props, furniture, people); a single performer.
- Setting: floor clearly distinct from wall, matte surfaces, no reflective surfaces.

## 4. Candidates
No clip found is 60 fps except one. Search pages give no durations (Pexels) so each clip page was read. Pages state no camera or framing, so all those fields are UNVERIFIED (not watched). The three motions are poorly served by search; matches below are the nearest by title and description only.

### Motion 1: rise from chair and walk out
- https://www.pexels.com/video/a-man-walking-towards-the-chair-and-sitting-on-it-6615631/ , "A Man Walking Towards the Chair and Sitting on it", cottonbro studio, 0:24, 4096x2160, 25 fps. Description "Fashion model walking and sitting among chairs in studio setup." Camera and body framing UNVERIFIED; chairs may block legs. Fit: sits rather than rises; plain studio; the reverse of the motion, could be played backwards (observation, not a recommendation).
- https://www.pexels.com/video/a-man-leaving-a-desk-10567419/ , "A Man Leaving a Desk", Ron Lach, 0:40, page lists 2160x4096 (filename suggests 1440x2732, inconsistent), 25 fps, vertical. Description "African American man with robot vacuum in a minimalist room setup." Fit: leaves a desk; the desk and vacuum may occlude; framing UNVERIFIED.
- Pixabay: no chair-rise clip found. https://pixabay.com/videos/man-walking-suit-business-office-199623/ (0:12, from search listing only, clip page not read) is a walk; UNVERIFIED.
- Pixabay https://pixabay.com/videos/man-model-walking-happy-fashion-140828/ , "Man, Model, Walking", AubreyKhokid, duration not stated, 1920x1080, 25 fps. Fit: walking only, no chair; framing UNVERIFIED.

### Motion 2: lean, shift weight, glance aside
- https://www.pexels.com/video/a-man-using-a-digital-tablet-while-leaning-on-the-kitchen-countertop-12691777/ , Anna Shvets, 0:17, 3840x2160, 59.94 fps (the only 60 fps clip found). Tablet in shot (a minus). Counter likely hides the legs; UNVERIFIED.
- https://www.pexels.com/video/a-muscular-man-leaning-on-metal-fence-8402081/ , RDNE Stock project, 0:10, 1080x1920 vertical, 30 fps. "Bearded man in a reflective pose, leaning on a railing outdoors." Fence may block legs; framing UNVERIFIED. Lean fit is good by description.
- https://www.pexels.com/video/a-man-posing-while-leaning-on-a-chair-8496805/ , Ivan S, 0:10, 1920x1080, 25 fps. "Moody portrait of a man posing indoors." Chair lean, not counter; framing UNVERIFIED.
- https://www.pexels.com/video/a-man-in-a-white-jacket-leaning-against-a-window-4727534/ , cottonbro studio, 0:32, page says 2160x3840 at 50 fps (the Canva link filename suggests 25 fps, conflict). "Man in a beige coat looks thoughtfully out a vintage window." Fit: a lean and glance; vintage look suits the period; window frame may occlude; UNVERIFIED.

### Motion 3: woman lighting and smoking
Note: no candidate found at a bus stop; "Woman at a bus stop" https://www.pexels.com/video/woman-at-a-bus-stop-7253210/ was listed but not read.
- https://www.pexels.com/video/a-woman-smoking-cigarette-8721791/ , Darina Belonogova, 0:14, 1080x1920, 25 fps. "A young woman with curly hair stands outdoors, smoking thoughtfully." Standing outdoors, best by description; whether lighting is shown and whole body is in frame UNVERIFIED.
- https://www.pexels.com/video/a-woman-smoking-outdoors-5978977/ , Yaroslav Shuraev, 0:43, 4096x2160, 24 fps. "Woman enjoying the breeze, smoking outdoors with a reflective glass backdrop." Reflective glass is against Epic's rule.
- https://www.pexels.com/video/a-woman-smoking-cigarette-9563496/ , MART PRODUCTION, 0:42, 2160x4096, 25 fps. "Urban setting with a woman smoking and man with briefcase on stairs." Second person: against the single-performer rule.
- https://www.pexels.com/video/woman-smoking-cigarette-4777885/ , cottonbro studio, 0:23, 3840x2160, 24 fps. "Close-up" of the face: fails whole-body framing.
- Pixabay https://pixabay.com/videos/woman-cigarette-pose-dependent-45288/ , Engin_Akyurt, listing 0:33, 3840x2160, frame rate not stated; tags woman, cigarette, pose, model; framing UNVERIFIED.

Fit summary against the rules: none confirmed locked-off, full body, unoccluded; all must be watched before use. Frame rates found: 59.94, 50, 30, 25, 25, 24. Most are below the 60 fps Epic asks for.

## 5. Not reached or not read
- No page was refused. Not read in full: the raw text of any page (only the tool's extracts), the full Pixabay section 5 text, the Pexels clip pages for 7253210 and the other search hits not listed above, the Pixabay clip pages other than 45288 and 140828. Pexels search lists beyond the first 24 results ("Load More"). Pixabay search was read for smoking and walking only, not leaning. Pexels and Pixabay download pages and API terms not read.
- Search used Pexels pages "man leaning on counter", "woman smoking cigarette bus stop", "man getting up from chair walking away", and Pixabay "woman smoking cigarette", "man walking away chair", all read 2026-11-09.
