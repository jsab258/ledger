line: licence (ledger-v2/research/license-allowlist.md line 6)
spec: CLAUDE.md says THE LICENCE ALLOWLIST IS LAW and that nothing ships that
  is not on it. Line 6 of the allowlist reads "Characters: MetaHuman ...
  Character Creator 4 exports per Reallusion EULA. Mixamo animations." IT
  NAMES ANIMATIONS AND NOT BODIES. The tree already ships 18 full Mixamo
  character bodies under ledger/Assets/Characters, and the Unity path renders
  one. A figure in a frame is the next visual step Jafar named, so this is
  worth one line of clarity BEFORE a body reaches a rendered frame rather
  than after.
acceptance: line 6 of the allowlist says what it means about bodies, either
  way, and if the answer is that bodies are allowed it says so in the same
  words the other three documents already use
max_sessions: 1
status: READY 2026-09-16, filed as a CLARITY item and NOT as a claimed
  violation, which the evidence does not support.

  WHAT THE REST OF THE TREE ALREADY SAYS, all three of them treating Mixamo
  bodies as settled:

      ledger-v2/studio-v2/casebook-claims.md:73
        "Nothing is purchased. Characters and animations come from Mixamo"
      game-design/shopping-list.md:19
        "Still free, still not a purchase. Mixamo characters are a download."
      game-design/the-gap.md:203
        "Characters + animations (Mixamo) | free"

  And CLAUDE.md's own section 0 says the same: "Characters and animations come
  from Mixamo with Jafar's account and a token he supplies."

  SO THE READING THAT FITS THE EVIDENCE is that the allowlist line is TERSE
  rather than restrictive, and that four documents including CLAUDE.md agree
  bodies are in. But the allowlist outranks CLAUDE.md, its wording is absolute,
  and a resident reading it generously is exactly the move the licence law
  exists to prevent. So it goes to the queue as one line to fix rather than
  to a resident's judgement.

  NOT A BLOCKER ON ANYTHING TODAY. The probe cannot render a skeletal mesh at
  all (zero hits for SkeletalMesh, USkeletalMesh, FBX or AnimSequence anywhere
  under ue-probe/Source), so no body can reach a probe frame until that
  pipeline exists. This item wants settling before that lands, not before the
  pipeline work starts.

  AND NO TOKEN IS AT STAKE. The 91 files already in the tree suffice;
  tools/mixamo-pick/README.md says Jafar's bearer token is needed only to
  fetch NEW characters or clips. Nothing here asks him for anything.
