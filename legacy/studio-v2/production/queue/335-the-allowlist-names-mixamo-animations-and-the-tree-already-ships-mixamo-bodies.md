line: licence (ledger-v2/research/license-allowlist.md line 6)
spec: CLAUDE.md says THE LICENCE ALLOWLIST IS LAW and that nothing ships that
  is not on it. Line 6 of the allowlist reads "Characters: MetaHuman ...
  Character Creator 4 exports per Reallusion EULA. Mixamo animations." IT
  NAMES ANIMATIONS AND NOT BODIES. The tree already ships 18 full Mixamo
  character bodies under ledger/Assets/Characters. A figure in a frame is the
  next visual step Jafar named, so this is worth one line of clarity BEFORE a
  body reaches a rendered frame rather than after.

  CORRECTED 2026-09-16 UNDER D43, and the correction matters because the
  sentence was the strongest evidence in the item. This spec said "and the
  Unity path renders one". IT DOES NOT AND NEVER HAS. Checked at the source
  rather than re-read: `ledger/Assets/Resources` exists and contains NO
  `Characters/Body`; `find ledger/Assets -iname "Body*.prefab" -o -iname
  "Body*.fbx"` returns nothing; and RealBody.cs:1287 carries the fallback
  `Why = "Resources/Characters/Body not in the build"` under a comment saying
  the likeliest cause is that the Editor step did not run. So the path is
  WIRED to load a body and no body asset is committed.

  THE CORRECTION STRENGTHENS THE ITEM rather than weakening it. If a Mixamo
  body had already been rendered, the allowlist question would be retroactive
  and arguably settled by practice. It has not, so the first body to reach a
  frame is still ahead of us, and the line gets its clarity before that
  happens exactly as this item asks. The count of 18 was re-counted the same
  day and is right: 18 .fbx files, no child-looking name among them, which is
  also D18 checked rather than assumed.
acceptance: line 6 of the allowlist says what it means about bodies, either
  way, and if the answer is that bodies are allowed it says so in the same
  words the other three documents already use
max_sessions: 1
status: DONE 2026-09-16, ANSWERED BY JAFAR. His reply was one character,
  "A", taking the card's option A: Mixamo bodies are in the same way Mixamo
  animations are, and the allowlist line says so in the words the other
  documents already use. Recorded as D46; the allowlist's SHIP-SAFE item 3
  is edited in the same batch, which is what a ruling that changes the law
  owes the law.

  THE FIGURE IS UNBLOCKED. This item was raised to BLOCKING at midday
  because the third element of his order for the day had no body it was
  allowed to use. It now does.

  Filed originally as a CLARITY item and NOT as a claimed violation, which
  the evidence did not support.

  RAISED TO BLOCKING 2026-09-16 MIDDAY: THIS NOW BLOCKS THE THIRD ELEMENT OF
  TODAY'S ORDER. Jafar's order for the day is "wetness, materials, then dusk
  with lamps lit, wet road and A FIGURE IN SILHOUETTE". Read in the code
  rather than assumed: the vignette scene spec has no figure of any kind
  (`production/specs/vignette-scene.json` has no character key, and its
  `not_emitted_from_this_file` list names three street fittings and no
  person), and the walk build's `ALedgerCharacter` is a third-person pawn
  with a 350 cm spring arm and NO SKELETAL MESH ASSIGNED
  (`LedgerCharacter.cpp:36-49`; the file sets a CameraBoom and a
  FollowCamera and never sets a mesh), so the frames it writes have an
  invisible player in them.

  SO THE FIGURE HAS TO COME FROM SOMEWHERE, AND THE ONLY BODIES IN THE TREE
  ARE THE 18 MIXAMO ONES THIS ITEM IS ABOUT. That is why a terse allowlist
  line stops being a clarity item today: the next step is putting one of
  those bodies in a rendered frame, which is the exact act the line does not
  cover in its own words. It goes to Jafar as a card rather than to a
  resident's generous reading, because the allowlist outranks CLAUDE.md and
  reading it generously is the move the licence law exists to prevent.

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

