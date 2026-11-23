# HUD icon reading: research notes, read 23 Nov 2026

Built on: STATUS.md's reader trial of 23 Nov and tools/star_count.py's first pass (what failed and why).

Scope: how existing tools and papers locate and classify a row of HUD icons (such as up to six stars) in recorded video. No synthesis. Only sources actually read are cited; the fetcher returns a summary of each page, so figures below are as that read reported them. Anything not confirmed is marked UNVERIFIED.

## Sources read (23 Nov 2026)
- AutoSplit tutorial: https://github.com/Toufool/AutoSplit/blob/master/docs/tutorial.md
- AutoSplit source compare.py: https://raw.githubusercontent.com/Toufool/AutoSplit/master/src/compare.py
- Honor of Kings hero detection (arXiv 1907.07854), HTML version: https://ar5iv.labs.arxiv.org/html/1907.07854
- HUD analysis in Bioshock 2 (PMC7302570): https://pmc.ncbi.nlm.nih.gov/articles/PMC7302570

## Q1. How is a fixed row of icons located in a frame?
- AutoSplit does not locate icons. The user sets one capture region (full screen or a dragged rectangle; "resizing the window will cause the capture region to change") and compares it against a reference image, optionally with a mask that keeps only the wanted pixels (tutorial, read 23 Nov).
- Honor of Kings paper: each blood bar is found by template matching on a grayscale frame; the match map is a 32-bit float image. The top 20 local maxima are taken and scored, and a threshold then decides how many are real (ar5iv, read 23 Nov).
- Bioshock 2 paper: a Haar-like cascade classifier is trained on one distinctive fragment of the HUD; the detected box is enlarged by a percentage to cover the whole HUD. Bars inside are then read by HSV colour filtering and measuring the width of rectangular contours (PMC, read 23 Nov). The analysis is local, so the HUD can be anywhere on screen.
- Q3Vision (UTS, reported in a search result only; its PDF text was unreadable): YOLO object detection plus OCR for numeric HUD parts. UNVERIFIED.

## Q2. Fixed slots, template matching or blobs; lit versus unlit
- Fixed layout: no source read states a fixed-slot layout scaled by resolution for icon rows. AutoSplit uses one fixed region and whole-image comparison.
- Template matching: used by the Honor of Kings paper, grayscale with a binary mask ("1 (white) means pixels used for matching"). The match method (for example normalised cross-correlation) is not named in the text read. UNVERIFIED.
- AutoSplit comparison methods (tutorial and compare.py):
  - L2 norm: error = cv2.norm(source, capture, NORM_L2, mask); score = 1 - error / max_error, where max_error is sqrt(source.size)*255, or with a mask sqrt(countNonZero(mask) * a multiplier). It assumes source and capture are the same size and does not resize. The tutorial calls it fast but a problem "if your image is high frequency".
  - Histogram: 8x8x8-bin RGB histograms, normalised, compared by Bhattacharyya distance; score = 1 - distance. The mask goes into calcHist.
  - Perceptual hash: resizes both images to 8x8 (INTER_AREA); the tutorial says it is "very inaccurate" with masks.
  - Score runs 0 to 1; a split fires above a per-image threshold, written in the file name, for example (0.9). A flag {b} reverses it to fire when similarity drops below.
- Lit versus unlit: AutoSplit has no lit/unlit concept beyond a whole-image similarity score. In Bioshock 2, state is read by bright red or blue pixels in HSV (shade and brightness filter). Honor of Kings: not applicable (blood bars, not on/off icons).
- Blob detection: not used in any source read.

## Q3. Keeping nearby text or digits from being counted
- AutoSplit: masks erase everything not to be compared; only non-transparent pixels count (tutorial).
- Honor of Kings: the binary template mask restricts which template pixels count; the threshold is applied to scored local maxima, not the raw match map, and the paper says this is "much better" than thresholding at the matching stage. Alpha and beta weights and the threshold value are not given (ar5iv).
- Bioshock 2: extra cropping of the detected HUD region reduces false colour matches from the background; text areas were read separately (PMC).
- No source read addresses a white timer next to icons specifically.

## Q4. Compression blur, resolutions and HUD scale, flashing
- Resolution: Honor of Kings normalises every video to a height of 720 px with aspect ratio kept, because bar size depends on height, not width (ar5iv). AutoSplit does not resize for L2 or histogram; only pHash resizes (to 8x8). The tutorial says images "can be any size and ratio" but does not explain scaling. In-game HUD scale settings: no source read addresses them.
- Compression: the Honor of Kings article does not discuss it. AutoSplit tutorial and Bioshock 2 text: no mention read. The histogram and pHash methods are less pixel-exact than L2, but no source states this as a compression remedy.
- Frame averaging: Bioshock 2 averages 30 frames per analysed image (about one second at 30 fps). Without it, HUD and weapon detection gave more false positives; averaging blurs moving elements, and cost about 188 ms to load and average from an HDD (PMC).
- Flashing: AutoSplit has no flash handling; its only timing control is Pause Time (seconds after a split during which comparison stops), plus dummy {d} and pause {p} flags. Frame averaging above is the only flicker-related technique found, and the paper does not describe it as aimed at flashing.

## Q5. Published accuracy figures
- Bioshock 2 (PMC): HUD classifier accuracy 92.13%, precision 99.35%, sensitivity 92.37%, specificity 86.66% (TP 618, TN 26, FP 4, FN 51), on frames averaged over 30; weapon identification 55.36% (Haar), 58.08% (LBP), 66.95% (LBP with error mitigation); text reading 99.36% and 98.80% within detected areas, 93.25% and 95.91% across all frames that should have been read, no false positives reported; bar-reading standard deviation 1.07 for both bars with the paper's method, against 4.03 and 2.25 for a prior full-screen method.
- Honor of Kings (ar5iv): the template-matching stage reports no accuracy figure in the text read. The downstream Inception V3 classifiers report accuracy 1.0000 and Micro-F1 0.9962 to 1.0000 on the test set; detection about 80 ms per frame, whole pipeline about 200 ms, about 5 fps at 1280x720.
- AutoSplit: no accuracy figures in the tutorial.
- No figures found for reading a row of lit/unlit icons from compressed video.

## Unreached or unreadable
- OpenCV template matching documentation (docs.opencv.org, 4.x and 3.4 tutorial and imgproc object pages): HTTP 403. Mode list and mask support not confirmed from the primary page.
- AutoSplit repository front page: no method detail; VideoAutoSplitter (zabbix-9 URL guessed): 404; not read.
- arXiv PDF 1907.07854 and the UTS Q3Vision PDF (DOI 10.1145/3793811.3793821): compressed streams not readable; the Q3Vision method and numbers are unread.
- Eichelbaum et al. 2018 (Springer, icon type and cooldown state in replays): abstract only seen in a search result, not read.
- Patent hits on "Monitoring icon status in a display" (image-ppubs.uspto.gov): not opened.
- No source read on OverWatch, Valorant or Apex HUD trackers, LiveSplit's own video auto-splitter, or HUD-scale handling.
