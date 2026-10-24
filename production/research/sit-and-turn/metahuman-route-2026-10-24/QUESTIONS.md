# The walk by Epic's MetaHuman route: questions (24 October 2026)

His order of 24 October: "start the walk's next go now ... by Epic's MetaHuman route: the sample's own character as the mover, Tom's MetaHuman body worn over it, with the 3 cm foot-slide bar." The last go (TOM-MOTION-MATCHING-2026-10-22.md) rebuilt the sample's graph by script and failed: starts, stops and turns slid 13 to 67 cm; the piece not rebuilt was the sample's blend-stack graph (Orientation Warping, Steering); its direction B is this one.

1. Epic's documented way to put a MetaHuman on the Game Animation Sample's character: which assets, which retargeter, how the mover's own mesh is hidden yet keeps animating, how the MetaHuman's face and body follow, and what Epic says about feet.
2. What the sample's own AC_VisualOverrideManager and ABP_GenericRetarget do, node by node and setting by setting.
3. What makes a retargeted body's planted feet slide when its source's feet do not: proportions, the retargeter's operations (feet IK goals, planting, stride), and the settings that keep them planted, in the installed engine's own source.
4. How the game drives the sample's character: possessed as the player's pawn, or a puppet fed input; how the sample's character reads input and decides its gait and speeds; what the game's own player character must hand over.
5. What the sample's character needs to run in a packaged game: every asset it depends on.
6. How the set route (-TomWalkProof) measures the worn body's feet, and what changes for a MetaHuman (its foot and ball bones, its standing height).
