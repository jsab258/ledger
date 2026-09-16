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

RULED 2026-09-16 (06:35Z ruling, section 6 and correction 7) AND THE RULING'S
INSTRUCTION IS NOT APPLIED. The ruling directs the resident to correct line 6
under D43 to name Mixamo characters, "citing Adobe's terms in the correcting
commit". The resident checked the two premises before editing a file CLAUDE.md
calls LAW, and both fail. Recorded here rather than argued, so the next
session inherits the evidence and not the disagreement.

  PREMISE ONE, THAT D29 ALREADY FLAGGED THE GAP. It does, and it says the
  OPPOSITE of what a D43 correction needs. D29 line 30, verbatim:

      The register decides faces in D2 and NOTHING decides bodies. The
      eighty-nine archived FBX files and the Mixamo entry in the licence
      allowlist are an implied answer nobody has written down.

  D43 covers a document that says something factually wrong. A line that is
  an "implied answer nobody has written down" is not wrong, it is UNDECIDED,
  and writing the answer in is a decision. The distinction is the whole of
  why D43 exists.

  PREMISE TWO, THAT ADOBE'S TERMS CAN BE CITED. They cannot be cited from
  here. A grep of the tree for Adobe or for Mixamo beside licen/terms/royalt
  returns exactly one hit, tools/mixamo-pick/README.md line 73, and it is
  about being polite to Adobe's servers. THERE IS NO STATEMENT OF MIXAMO'S
  TERMS ANYWHERE IN THIS REPOSITORY. Citing them would mean writing a
  citation from memory into the file that governs what ships, which is rule
  1 exactly.

  AND THE STANDING LAW SETTLES IT WITHOUT THE RESIDENT'S JUDGEMENT. CLAUDE.md:
  "THE LICENCE ALLOWLIST IS LAW ... nothing ships that is not on it, and a new
  tool enters only through a decision record naming its weights licence." The
  06:35Z record does not name Mixamo's terms; it instructs that they be named
  in the commit. So by the allowlist's own entry rule the line cannot be added
  yet, and this is not the resident overruling a director.

  WHAT IS OWED, and it is small: the actual Mixamo terms read and quoted, then
  line 6 written from that quote in a record that names it. Until then the
  line stands as it is and nothing is blocked, because the probe cannot render
  a skeletal mesh at all and queue 028 half one bakes a STATIC GLB, which is a
  posed mesh export and hits this same question the moment it ships rather
  than avoiding it. So this wants doing before 028 half one lands, not before
  it starts.

  NOTHING HERE ASKS JAFAR FOR ANYTHING. His account and his token are not
  involved; the 91 files are already in the tree.

