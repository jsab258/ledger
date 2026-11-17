# Review: Image-to-3D checks and the DINOv3 pick (17 Nov 2026)

Reviewed: production/lane/IMAGE-TO-3D-CHECKS-2026-11-17.md. Fresh reviewer, 17 Nov 2026, about ten minutes. Checked against RULINGS.md (16 Sep, 22 Sep, 3 Oct sources and NoAI, 24 Sep new-tool rule), ledger-v2/research/license-allowlist.md (item 2), the target it checks, and the web.

## Verdict: PASS WITH FIXES

The facts spot-checked hold. The licence reasoning is mostly sound, but the reason given for option A overstates two things, and the page line leaves out the second block the target says must be answered with it.

## Facts spot-checked (read 17 Nov 2026)

| Claim | Result | Source |
|---|---|---|
| DINOv3 licence dated 14 Aug 2025, not 19 Aug | Holds. The page shows "August 14, 2025" under its title. The summariser saw no "Last updated" label, so the quoted words are uncertain (finding 6) | https://ai.meta.com/resources/models-and-libraries/dinov3-license |
| DINOv3 terms: royalty-free grant, no commercial bar named, "Built with DINOv3" and a licence copy only on distribution of the materials or derivative works, derivative works undefined, 5a ownership, 5b indemnity, 8 changes effective at once, 1b.v trade and military bar | Holds | same |
| TRELLIS.2 uses DINOv3 ("both use the same DINOv3 image encoder") | Holds; DINOv2 not mentioned there | https://docs.comfy.org/tutorials/3d/trellis2 |
| TRELLIS v1 image-large weights "license: mit" | Holds | https://huggingface.co/JeffreyXiang/TRELLIS-image-large/blob/main/README.md |
| TripoSR MIT; encoder "initialized with ... DINOv1"; Objaverse subset "available under the CC-BY license" | Holds (paper; Hugging Face card "License: mit" with the same training sentence) | https://arxiv.org/html/2403.02151v1 and https://huggingface.co/stabilityai/TripoSR |
| facebook/dino-vitb16 "apache-2.0" | Holds | https://huggingface.co/facebook/dino-vitb16 |

Rulings: Meshy and Tripo correctly closed by 16 Sep; the 22 Sep hold is respected (the order of 16 Nov, item 11, names this test, and the file says nothing is adopted on it alone); TRELLIS v1 correctly marked allowlisted; Stable Fast 3D and Hunyuan3D correctly out. No em-dashes, no italics. Unreached sources are listed and not used as evidence, except in finding 4.

## Findings

1. The reason for A says "the credit line covers the one doubtful reading". It does not. If a mesh did count as a derivative work, 1b.i would require that the mesh be passed on under the DINOv3 licence with a copy of the licence, not only the notice. Fix: replace that clause with "if a mesh were ever held to be a derivative work, the duty would be a copy of the DINOv3 licence plus the notice shipped with the game; option A adds both to the credits and THIRD-PARTY.md at no cost, which covers that reading." Change the page line's option A to match: "with 'Built with DINOv3' and its licence added to the credits at no cost".

2. "TRELLIS.2 is the only allowlisted generator with a route to this card" overstates. Only TRELLIS.2's weights are listed; the route runs through trellis.cpp and BiRefNet (each needs a decision record under the 24 Sep rule, as the target's table says) and DINOv3 (off the list), and the route itself is unproven on the RX 6700 (point 1, needs the PC). Fix: "TRELLIS.2's weights are the only allowlisted generator with a possible route to this card (trellis.cpp on Vulkan, unproven here; trellis.cpp and BiRefNet need a decision record)".

3. The page line asks only the DINOv3 question, but the target (Recommendation, and stage 1 of its plan) says one page item with two answers, both needed before any generator run: DINOv3, and whether a model trained on Objaverse-XL's Sketchfab subset is allowed under the 3 Oct NoAI ruling. As written, a yes to A reads as clearing the run. Fix: add one sentence under the line: "This alone does not start the generator: the training-data question (Objaverse-XL's Sketchfab subset, 3 Oct ruling) goes on the same page as a second one-line decision." Or add "the generator still waits on the training-data question" inside option A.

4. Point 2 marks "Confirmed unpublished", but the README and getting-started page were not reached this pass (Unreached list), and the target's memory quotes came from the README. An absence found in the wiki alone is not a confirmation. Fix: change the result to "Not found in the wiki; needs the PC" and the text to "The wiki gives no memory table ... (README and getting-started not re-read this pass)."

5. TripoSR is called "every part permissive" with no training-data caveat, while TRELLIS v1 gets "same training-data question". The Objaverse 1.0 subset is also drawn from Sketchfab, and the allowlist admits Objaverse "only with per-object license filtering"; whether any of TripoSR's curated items were later marked NoAI is unread. Fix: in the TripoSR bullet and option C, add "same training-data question (its Objaverse subset is also from Sketchfab; per-object marks unread)", and drop "all parts permissive" from option C or qualify it as "all licences permissive".

6. The DINOv3 date is given as a quotation, "Last updated: August 14, 2025"; a second read saw only the date under the title, with no such label. Fix: write "Meta's page is dated August 14, 2025" without the quoted label, unless the label is confirmed on a re-read.

7. The "Bars" line lists only 1b.v. The licence also requires a credit in published research (1b.ii), legal compliance (1b.iii) and no reverse engineering or decompiling (1b.iv). None changes the pick, but the list should be complete for his decision. Fix: "Bars and duties: trade-control uses, including military or warfare (1b.v); credit in published research (1b.ii); obey the law (1b.iii); no reverse engineering (1b.iv)."

8. "No commercial bar" is a reading, not a quotation; the licence does not mention commercial use either way. Fix: "No commercial bar is stated; the grant sets no limit by purpose beyond 1b.v."
