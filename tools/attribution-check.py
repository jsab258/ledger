#!/usr/bin/env python3
"""Every directory of third-party content is named in THIRD-PARTY.md.

WHY THIS EXISTS. The completeness audit on 2026-07-31 found no `LICENSE`, no
credits screen and no attribution file anywhere in the project, while 19 cast
voices are derived from a corpus licensed CC BY 4.0, which REQUIRES attribution.
That is a licence breach waiting on a release, and it survived because nothing
in the plan owned it and nothing in CI looked for it.

A file somebody has to remember to update is a file that goes stale, the same
argument as the reach ledger, and this project has already watched a roadmap's
"STILL OPEN" list rot four days while reading as current. So the check is
mechanical: an asset directory with no entry fails the build.

AND UNTIL 1 SEPTEMBER THE CHECK HAD THE FAULT IT EXISTS TO CATCH, THREE TIMES
OVER. It classified files by a suffix ALLOW-LIST and said nothing at all about
what the list did not match. `.glb` was never on it, so the 37 models under
`ledger/Assets/Props/base-mesh` produced NO LINE, neither ok nor fail, and the
"The Base Mesh" token was never once checked in the whole life of the row. The
same silence hid 23 `.bin` and 23 `.npz` conditionals under
`game-design/voice-conds` and 12 `.mtl` under `Props/oga-vehicles`. Adding
`.hdr` on 24 August and `.webp` the same day fixed two formats and left the
SHAPE, which is rule 1's third corollary exactly: when you fix a bug, grep for
the same bug.

SO THE ALLOW-LIST NO LONGER HAS TO BE PROPHETIC, WHICH IS THE ONLY REPAIR THAT
SURVIVES THE NEXT FORMAT. Two sets are declared, `ASSET_SUFFIXES` and
`NOT_ASSET_SUFFIXES`, and their union has to cover everything walked. A suffix
in neither is UNCLASSIFIED, and unclassified is printed and fails. A `.glb`
landing today would have named itself on the first run instead of hiding for a
month, and so will the `.usdz` nobody has thought of yet. The residue is the
instrument; the list is just today's answer.

    python3 tools/attribution-check.py
    python3 tools/attribution-check.py --census      # the suffix series
    python3 tools/attribution-check.py --selftest
"""
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOC = ROOT / "THIRD-PARTY.md"

# Directories that hold content this project did not author, and the token that
# must appear in THIRD-PARTY.md for each. Adding a new one here without adding
# the row is what the check is for.
WATCHED = {
    # THE UNREAL GAME'S OWN CONTENT, 5 October 2026 (phase 0's exit review): every `.uasset` was
    # ruled a build product, so the 1,700 under ue-probe/Content (most of them gitignored, made in
    # the editor or by import scripts from sources on F:) were walked and never checked. Each
    # folder now names the rows it rests on (the provenance traced through each import script:
    # production/audits/phase0-exit/BUNDLE.md, 5 October). The folders are on this PC only, so
    # the check bites here and in the package check below, not in the cloud.
    "ue-probe/Content/Ledger/MetaHumans": ("MetaHuman", "FreeSewing", "VCTK"),
    "ue-probe/Content/MH_Test.uasset": "MetaHuman",
    "ue-probe/Content/Ledger/Export": "MetaHuman",
    "ue-probe/Content/Ledger/Cloth": ("MakeHuman", "FreeSewing"),
    "ue-probe/Content/Ledger/Figure": "Mixamo",
    "ue-probe/Content/Ledger/People": "Mixamo",
    "ue-probe/Content/Ledger/Props": "The Base Mesh",
    "ue-probe/Content/Ledger/ShopDisplays": "Poly Haven",
    "ue-probe/Content/Ledger/ShopRooms": "Poly Haven",
    "ue-probe/Content/Ledger/Sounds": ("VCTK", "sturmankin"),
    "ledger/Assets/Characters": "Mixamo",
    # THE PICKER'S REJECTING CASE. Four Mixamo clips that shipped under
    # `Characters` until the posture and travel screen caught them, kept out of
    # the build so a re-pick cannot replace them: they are the only files the
    # screen is guaranteed to have something to refuse. Same corpus and the
    # same obligation as the shipped picks; the only difference is that these
    # are the ones the game does NOT play.
    "tools/mixamo-pick/known-bad": "Mixamo",
    # THE STREET'S PEOPLE, 23 September: Mixamo bodies and clips from
    # `ledger/Assets/Characters`, each converted by
    # tools/art-recipes/person-export.py into one glb (the clip's rotations on
    # the body's bones, the loop trimmed, the textures shrunk). A conversion
    # is not authorship: the same corpus and the same obligation.
    "production/assets/people": "Mixamo",
    "game-design/picked-clips": "VCTK",
    "voice-candidates": "VCTK",
    # THE SYNTHESISED BARKS, AND THEY BELONG HERE RATHER THAN IN `OURS`.
    #
    # We generated them, which makes "ours" the tempting answer and the wrong
    # one: every clip is a voice CLONE of a VCTK speaker, so each is a
    # derivative of a CC BY 4.0 work and carries its parent's obligation.
    # THIRD-PARTY.md said so in advance, "synthesis does not launder the
    # obligation", and this row is that sentence made mechanical.
    #
    # The distinction `OURS` draws is authorship, not who ran the command. The
    # app icons are ours because nothing outside this repo went into them; the
    # sim stills are ours because the game drew them. A cloned voice fails
    # that test no matter whose GPU produced it.
    "ledger/Assets/StreamingAssets/Audio/Voice": "VCTK",
    # THE LIVE MODEL'S OUTPUT, BY THE SAME REASONING AS THE BARKS ABOVE.
    # `spoken.wav` is one line spoken by the converted graphs on Jafar's
    # machine, pushed back by the watcher so it can be heard from here. It is a
    # clone of a VCTK speaker exactly as the banked barks are; arriving live
    # instead of in a batch does not change whose voice it is, and "we ran it
    # a minute ago" is the same argument this file already rejects two rows up.
    "game-design/voice-live": "VCTK",
    # THE PRECOMPUTED CONDITIONING, ADDED 1 SEP, AND THE ROW IS THE EASY HALF.
    # 23 `.bin` and 23 `.npz` that the sweep could not see at all, because
    # neither suffix was on the list and the directory was on no row.
    #
    # WHAT THEY ARE, ESTABLISHED BY OPENING THEM RATHER THAN BY READING THE
    # FILENAMES. `ada.bin` begins `LDGRVOICE1`, the magic
    # `tools/voice-live/precompute-voices.py` writes; that script sets
    # `CLIPS = game-design/picked-clips` and calls
    # `model.prepare_conditionals(clip)`; `manifest.json` names the exact
    # source per voice (`ada` <- `ada.p276.mp3`); and `ada.npz` holds
    # `gen.prompt_feat` at (1,410,80) float32, which is a mel-spectrogram of
    # the reference RECORDING, not a statistic about it. So each pair is a
    # transformed representation of a VCTK clip, one per picked clip, 23 for
    # 23. That is the barks' reasoning with a shorter pipeline: computing a
    # tensor from somebody's recording does not launder the recording.
    "game-design/voice-conds": "VCTK",
    "ledger/Assets/StreamingAssets/CityPack": "CityPack",
    # THE SHORTLIST'S OWN LIVE DIRECTORY, ADDED 2026-09-15 (queue 300) BEFORE
    # THE FIRST LIVE RUN WRITES TO IT. `tools/citypack/fetch_textures.py
    # --shortlist` downloads several 1K CANDIDATE tiles per flagged surface
    # from ambientCG and lays them into contact sheets under this path, so a
    # surface can be picked by looking rather than by name (queue 300:
    # "PICKED BY NAME... No image can be seen from this container"). CC0 1.0
    # Universal, same licence as every other ambientCG row in this file;
    # ambientCG is line 5 of `ledger-v2/research/license-allowlist.md`. The
    # ids actually downloaded in any one run are enumerated in
    # `shortlist-results.json`, which travels with the pixels, and in
    # `ATTRIBUTION.json`, written by the same run.
    #
    # NOT SHIPPED. This is a sourcing aid for choosing what the pack wears
    # next; nothing under this path is read by `AssetLibrary` or packaged
    # into a build.
    #
    # THE TOKEN IS NOT "ambientCG", for the same reason `vignette-surfaces`
    # two rows down is not either: that word is already in THIRD-PARTY.md for
    # the decals, so a row keyed on it would pass without anybody writing
    # anything, which is a guard that goes green for the wrong reason.
    #
    # THE TOKEN IS ALSO NOT "citypack-shortlist" WITH A HYPHEN, which is what
    # this row said until the REJECTING-case test (CLAUDE.md rule 5b) caught
    # it: THIRD-PARTY.md's own row names the CI workflow that writes here,
    # `.github/workflows/citypack-shortlist.yml`, and a hyphenated token is a
    # PREFIX of that filename, so the check passed even with the real
    # declaration deleted, on the strength of the workflow's own name in the
    # same sentence, which is the exact "goes green for the wrong reason"
    # fault the paragraph above exists to avoid. The underscore is not a
    # style choice; it is the smallest change that stops the token being a
    # substring of a filename this row is also going to mention.
    #
    # AHEAD OF THE BYTES ON PURPOSE, the same order the vignette-surfaces row
    # below uses: `.github/workflows/citypack-shortlist.yml` commits
    # `tools/citypack/shortlist/contact-*.png` straight to this path on its
    # first live run (the dev-container run kept as evidence under
    # `tools/citypack/shortlist-2026-09-15-network-blocked-proof/` never
    # reached this path at all; every one of its 35 candidates 403'd), so the
    # obligation is recorded before that run lands rather than after.
    #
    # WHAT WOULD MAKE THIS ROW FALSE: the day `--shortlist` downloads a
    # candidate from a source that is not ambientCG, this row understates
    # what the directory holds and has to be corrected or widened.
    "tools/citypack/shortlist": "citypack_shortlist",
    # The CC0 model kits (props-fetch job). CC0 needs no credit by law and
    # gets one anyway: the project's rule is that every third-party file
    # is named, and Props/ATTRIBUTION.json + THIRD-PARTY.md are written by
    # the same fetch that writes the models, so they cannot drift apart.
    "ledger/Assets/Props": "Kenney",
    # M17.10: the visual-bar fetches. base-mesh sits INSIDE Props but is not
    # Kenney, so it carries its own row: the sweep whitelists by path
    # containment and the token check is per-row, so both hold.
    "ledger/Assets/Props/base-mesh": "The Base Mesh",
    # THE SHOP WINDOWS' DISPLAYS, 1 October: Poly Haven's CC0 models, cut down and
    # joined into one glb per shop by tools/art-recipes/shop-room.py --display.
    # Built here, but from fetched meshes and pictures: their row, not ours.
    "production/assets/shop-displays": "Poly Haven",
    # THE SHOPS' ROOMS AS REAL GEOMETRY, 3 October: the same Poly Haven models and textures,
    # exported room by room by tools/art-recipes/shop-room.py --export-room.
    "production/assets/shop-rooms-3d": "Poly Haven",
    # THE GROCER'S PRINTED LABELS, 3 October: our own sheet (tools/art-recipes/make_label_atlas.py),
    # every maker made up, set in the project's OFL fonts; the row names the fonts' licence.
    "production/assets/shop-goods": "Marcellus SC",
    # THE SAME SHAPE AS base-mesh, AND IT HAD BEEN PASSING UNDER THE WRONG
    # NAME. `oga-vehicles` sits inside `Props`, so its 47 attributed files
    # were counted under the Kenney row and the check went green over models
    # Kenney did not make. The comment two rows up predicted this exactly and
    # nobody swept for the second instance. The token is OpenGameArt because
    # that is the source `tools/props/fetch_visual.py` scrapes, and the
    # fetcher refuses any page whose HTML lacks
    # `creativecommons.org/publicdomain/zero`, so the CC0 claim in the row is
    # machine-checked at fetch time rather than copied from a sibling doc.
    "ledger/Assets/Props/oga-vehicles": "OpenGameArt",
    "ledger/Assets/StreamingAssets/Decals": "ambientCG",
    # The D1b vignette's own surfaces, engine-neutral and therefore outside
    # any engine's asset folder. The token is deliberately NOT "ambientCG":
    # that word is already in THIRD-PARTY.md for the decals, so a row keyed on
    # it would pass without anybody writing anything, which is a guard that
    # goes green for the wrong reason.
    # NARROWED TO `surfaces` ON 2 SEP, AND THE REASON IS THE ROW'S HONESTY.
    # It read `production/assets/vignette`, which is the whole vignette
    # directory, and the deterministic 2D lines landed beside the fetched
    # surfaces as `decals2d`. Files this project GENERATED would then have
    # been counted on a row whose token says ambientCG fetched them, which is
    # a third-party claim over our own work: the same fault as `oga-vehicles`
    # passing under the Kenney row, in the other direction. The generated
    # sibling is declared in OURS below, and anything else that appears under
    # `vignette` is caught by the stray sweep rather than absorbed silently.
    "production/assets/vignette/surfaces": "vignette-surfaces",
    "ledger/Assets/Resources/Sky": "Poly Haven",
    # THE PS5 CORNER'S SCANNED MATERIALS, 23 September, downloaded on Jafar's
    # yes: Poly Haven textures, CC0, 2k maps, one folder per material.
    "production/assets/scanned": "Scanned materials — Poly Haven",
    # TOM'S FOOTSTEPS, 30 September: cut from two CC0 recordings of real
    # trainers (tools/ue/make_steps.py), kept apart from the generated beds in
    # `production/assets/sounds` (ours) so neither row covers the other.
    "production/assets/steps": "Footsteps — sturmankin and Joseph Sardin",
    # NOT AN ASSET DROP: the visual bar's reference frames. Five GTA V
    # screenshots supplied by Jafar, committed byte-exact after the project
    # spent three days with its visual target existing only as a prose
    # description of itself (the pixels lived in a chat context that got
    # compacted). They are internal comparison references, never shipped,
    # never redistributed; the row in THIRD-PARTY.md says exactly that.
    "game-design/reference": "Rockstar Games",
    # A single file, not a directory: the shipped face sits in `Resources`
    # beside code and prefabs, so there is no folder to name that would not
    # also swallow half the project. The token is the licence, because that is
    # the obligation: the OFL is what THIRD-PARTY.md has to say out loud.
    "ledger/Assets/Resources/LedgerSans.ttf": "SIL Open Font License",
    # THE STREET NAME PLATES' LETTERING, 30 September: Marcellus SC, fetched
    # from Google Fonts' repository once Jafar allowed the OFL for fonts. The
    # token is the family's own section, not the licence, which the PT Sans
    # row already names and would pass without anybody writing anything.
    "production/fonts/marcellus-sc": "MARCELLUS SC",
    # THE INTERFACE'S TYPE, 1 October: the evening paper's fonts, which ship in
    # the game (static cuts of two variable families, tools/ui/make_font_cuts.py).
    "production/fonts/evening-paper": "THE EVENING PAPER",
    "production/fonts/patrick-hand": "PATRICK HAND",
    # THE PS5 CORNER'S BAR, 23 September: two Kingdom Come: Deliverance II
    # screenshots supplied by Jafar. Out of the repository since 3 October (his
    # ruling: other games' screenshots never in it), kept on this PC
    # (F:/LedgerTools/reference-other-games) and in his backup; THIRD-PARTY.md
    # still names them, so the row stays and checks that.
    "production/reference/kcd2-town-arcades.jpg": "Warhorse Studios",
    "production/reference/kcd2-town-fountain.jpg": "Warhorse Studios",
    # THE CASTING VOICE CANDIDATES, 24 September (overnight): three lines per
    # candidate, spoken by Chatterbox from a reference that is his approved VCTK
    # clip, a voice designed from a written description by Parler-TTS, or two
    # clips of a Google northern English volunteer (SLR83, CC BY-SA 4.0). Each
    # is a derivative of its reference, so the barks' reasoning holds; the
    # token names the section of THIRD-PARTY.md that credits all three, and
    # production/casting/voice-key.json says which letter came from which.
    "production/casting/sheila-dunn/voices": "Casting voice candidates",
    "production/casting/ron-kirby/voices": "Casting voice candidates",
    "production/casting/darren-milner/voices": "Casting voice candidates",
    # THE ACTING TEST, 25 September: the same Chatterbox, cloned from the
    # voice he picked for each (so from the same references as above), and an
    # "acted" reference that is that voice cloned reading a passage in a
    # feeling. Derivatives of the same references; the same credits.
    "production/casting/sheila-dunn/acting": "Casting voice candidates",
    "production/casting/ron-kirby/acting": "Casting voice candidates",
    "production/casting/darren-milner/acting": "Casting voice candidates",
    # THE CAST IN THE GAME, 25 September (evening): each character's line as
    # the game's voice engine speaks it from their game clip (Sheila's
    # Parler-designed D, Ron's p227, Darren's p241), for the in-game page.
    "production/casting/in-game-2026-09-25/voice": "Casting voice candidates",
    # 28 September: the thinking sounds and the day's page's speaking lines are
    # the game's voice engine speaking from the cast clips: clones, so VCTK's
    # and Parler's obligations, by the same reasoning as the barks.
    "content/voice/acks": "Casting voice candidates",
    "production/approvals/2026-09-28": "Casting voice candidates",
    "production/approvals/2026-09-29": "Casting voice candidates",
}

# ASSETS THIS PROJECT MADE ITSELF, which need no attribution and must not be
# reported as unaccounted for. The distinction matters: a check that cannot tell
# "third-party, needs a licence row" from "ours, needs nothing" either nags
# about our own files or goes quiet about somebody else's, and both make it
# useless. Anything here is ours; everything else is somebody's.
OURS = {
    # The Unreal street, its cars and its own materials (5 October, with the folders above): made
    # by this project's scripts from this project's geometry; the textures bound into the
    # materials at run time are attributed where they live.
    "ue-probe/Content/Ledger/Street": "the street, imported from production/assets/street/quay-street.glb (tools/art-recipes/terrace-front.py)",
    "ue-probe/Content/Ledger/Vehicles": "the hatchbacks, imported from tools/art-recipes/car-model.py's glbs",
    **{"ue-probe/Content/Ledger/%s.uasset" % n: "generated by tools/ue/make_*_material.py from graphs this project wrote"
       for n in ("M_LedgerGlass", "M_LedgerGrime", "M_LedgerInterior", "M_LedgerSky", "M_LedgerSurface",
                 "M_LedgerWet", "T_LedgerDefaultNormal", "T_LedgerDefaultRough")},
    # The interface's four sounds, synthesised from noise and decaying tones by
    # tools/ui/make_ui_sounds.py (1 October): nothing recorded or downloaded.
    "production/audio/ui": "the interface's sounds, synthesised by tools/ui/make_ui_sounds.py, 1 October",
    # 2 October's page: the pawnbroker's window filmed by the game in its own street (-PageShots).
    "production/approvals/2026-10-02": "the game filming its own street and cast for the day's page, 2 October",
    # The clothing page of 2 October: Ron in the clothing session's own jacket, filmed by the game in its own street
    # (the builder's in-game test), a MetaHuman built on this PC (renders may be shown; its files stay out of here).
    "production/approvals/2026-10-02-clothes": "the game filming Ron in the clothing session's own jacket, 2 October",
    "ledger/Assets/Resources/AppIcon": "generated by tools/make-icon.py from the game's own palette",
    # 30 September's approval page: the walk past Sheila as the game's look
    # script films it (-LookCamera), frames of this project's own street and a
    # MetaHuman built on this PC (Epic's MetaHuman licence lets renders be
    # shown; the MetaHuman files stay out of this repository).
    "production/approvals/2026-09-30": "the game's look script filming its own street and cast (-LookCamera), 29 September",
    # 1 October's page: the cast's faces filmed by the game itself while they
    # say their thinking sounds (-MouthFilm with -FaceAB), frames of MetaHumans
    # built on this PC (renders may be shown; the files stay out of here).
    "production/approvals/2026-10-01": "the game's mouth film of its own cast (-MouthFilm, -FaceAB), 1 October",
    # The interface's design mockups (Jafar's yes, 1 October, on the interface
    # choice page): pages this project wrote, drawn by a browser over the game's
    # own frames of 1 October, with SIL OFL fonts drawn into the pictures (the
    # font files themselves are not here; production/design/ui/FONTS.md).
    "production/design/ui": "the interface's design mockups, pages this project wrote drawn by a browser over the game's own frames of 1 October, OFL fonts drawn into the pictures and no font file here",
    # The build's own screenshots of the game's own street. Rendered by the
    # Windows job and committed every run, so they arrive faster than any
    # other asset in the project and are the likeliest thing to trip a check
    # that assumes a new JPEG came from outside.
    "game-design/sim-shots": "rendered by the sim itself and committed by CI every build",
    # The D1b vignette's deterministic 2D lines: geometry, seeded noise and
    # canon.md's own minted street names, drawn by Pillow. The one outside
    # input is the OFL font already attributed above, used to RENDER letters
    # rather than redistributed, and the generator's ATTRIBUTION.json says so
    # in the same run that writes the images.
    "production/assets/vignette/decals2d": "generated by tools/props/make_vignette_2d.py from this project's own geometry and canon's own names",
    # THE STREET'S GEOMETRY ON ITS WAY TO UNREAL, added 23 September with the
    # first export. The GLB is the recipe's own boxes and slopes, reflected
    # once so it arrives the right way round, with PLACEHOLDER materials: no
    # texture, no picture and no third-party mesh is in it. The lamps and the
    # held props, which are CC0 base meshes, are left out of the export on
    # purpose; the sidecar JSON names textures and pictures by path and
    # carries none of them. WHAT WOULD MAKE THIS ROW FALSE: an export that
    # embeds an image, or one that stops skipping the placed props.
    # AND ITS DRAWN SURFACES, the same day: surfaces/ holds the bricks, flags
    # and stallriser tile drawn by tools/props/make_street_surfaces.py from
    # the recipe's own numbers, every pixel computed, the staining periodic
    # noise from a fixed seed. No pack photograph is read into them.
    # THE PARKED CARS, 23 September: built by tools/art-recipes/car-model.py
    # from Blender primitives - boxes, cylinders, a bevel, a subdivision, two
    # boolean arches - with flat materials and no texture. No mesh, picture or
    # outline from anywhere else, and no real make's lines (canon).
    "production/assets/vehicles": "built by tools/art-recipes/car-model.py from Blender primitives, flat materials, no texture and no fetched input",
    # THE STREET'S AMBIENCE, 23 September: made from seeded noise by
    # tools/props/make_street_ambience.py, which can prove the committed wav is
    # what it makes. No recording, no sample library, nothing fetched.
    "production/assets/sounds": "generated by tools/props/make_street_ambience.py from seeded noise; no recording and no fetched input",
    # THE AI TESTER'S PICTURES, 24 September: frames of this project's own game
    # window, copied from the window by tools/ai-tester/play.py while it
    # plays. Kept on this PC only (the folder is ignored by git), because a
    # picture of a desktop is private.
    "production/playtest/ai-tester": "frames of this project's own game window taken by tools/ai-tester/play.py; kept on this PC, never committed",
    "production/assets/street": "exported by tools/art-recipes/terrace-front.py --export-glb: this project's own street geometry, built from primitives by the recipe and from its own 1990 street clutter (clutter/, made by tools/meshgen/blender/clutter/*.py from measurements, no fetched asset as an input), with placeholder materials and no textures; the base-mesh lamps and props are not exported; and surfaces/, drawn by tools/props/make_street_surfaces.py from the recipe's numbers with no fetched input",
    # THE ART LINE'S PREVIEWS, added 2026-09-08 before the first one landed,
    # because the builder that wrote the recipe flagged that the first
    # successful commit would turn this check red on the art branch and said
    # the wording was a licensing claim rather than a lint fix, which is
    # right. THE CLAIM, stated so a later reader can check it rather than
    # trust it: these are Blender renders of THIS PROJECT'S OWN piece list
    # (production/specs/vignette-pieces.json), built from primitives plus the
    # sixteen .glb props already on the licence allowlist and already carrying
    # their own attribution. The preview carries no third-party texture; the
    # only outside content is CC0 geometry, attributed.
    # WHAT WOULD MAKE THIS ROW FALSE, and it is foreseeable rather than
    # hypothetical: the day a recipe binds FETCHED textures, the renders stop
    # being wholly ours and this row has to say so or be removed. A recipe
    # that loads anything from ledger/Assets/Textures or a fetch cache is the
    # trigger, and so is a recipe importing geometry from anywhere but
    # base-mesh. THE SECOND HOLE, ruled the same day: this key matches by
    # PREFIX, and tools/art-deliveries.py puts an OUTSIDE ARTIST'S delivery
    # under the same production/art tree, so a delivered PNG would be
    # classified as ours by a row that only ever meant the previews. The
    # value says so; narrowing the path rule is queue 153.
    "production/art": "renders by a recipe under tools/art-recipes of this project's own piece list - the previews under production/art/*/previews and the accepted frames a recipe commits beside its asset - renders of this project's own piece list by a recipe under tools/art-recipes, greys from the recipe plus the CC0 base meshes attributed in ledger/Assets/Props/base-mesh/THIRD-PARTY.md; a DELIVERY under the same commission is somebody's and is not covered by this row; and clothing/, the garments sewn by tools/meshgen/blender from FreeSewing's patterns (MIT), pictured in Blender and worn by a MetaHuman in this project's street",
    # The Unreal probe's own frames, added 3 Sep 2026 when run 17 rendered the
    # street for the first time and this check went red naming five PNGs. The
    # same category as sim-shots and for a stronger reason: Phase B is
    # UNTEXTURED, so every pixel is an engine primitive lit by lights this
    # project placed, from positions ledger/Core wrote into
    # production/specs/vignette-pieces.json. There is no third-party pixel in
    # them to attribute. Phase C puts allowlisted textures on those surfaces,
    # and the licence question then belongs to the TEXTURES where it already
    # lives, not to the screenshot of them.
    # CORRECTED 7 SEP 2026. This row said "untextured engine
    # primitives", which was true until run 25 put Meridian's own
    # textures on the street. These frames now CONTAIN ambientCG and
    # CityPack pixels, both attributed on the other side of this file,
    # and a licensing row that understates what is in a picture is the
    # one kind of decayed claim this check exists to prevent.
    # MOVED 2026-09-22 when the studio was paused: this directory went to
    # legacy/studio-v2/production/d1-probe with the rest of the dispatch
    # machinery. The 65 renders under it are unchanged and are still ours;
    # only the path moved, so the key moved with it rather than the row
    # being deleted. Deleting it would have let 65 asset files fall out of
    # the sweep's denominator silently, which is the failure this row exists
    # to prevent.
    # AND THE LIVE PATH IS BACK, 2026-09-22, because the archive move above
    # took the row with it and left the RUNNING probe with none. The probe
    # still writes to production/d1-probe and still commits its frames every
    # run; the day it ran green for the first time since the pause it pushed
    # a dozen PNGs into a directory this file no longer knew about and the
    # sweep went red naming them. Moving a key is right when a directory
    # moves and wrong when a live copy of it remains: both carry frames, so
    # both are rows.
    # THE ONE PLACE A REFERENCE LIVES, added 2026-09-22 with the rule.
    # The casting sheets' concept portraits, 24 September: made by
    # tools/imagegen running Z-Image-Turbo (Apache-2.0) from written
    # descriptions of invented people, no fetched asset as an input. The voice
    # folders beneath are third-party-derived and carry their own rows above.
    "production/casting": "concept portraits made by tools/imagegen running Z-Image-Turbo (Apache-2.0) from written descriptions of invented people, no fetched asset as an input; and candidates-2026-09-25, pictures taken in this project's own street by its portrait tool of MetaHumans built on this PC from its casting sheets (Epic's MetaHuman licence lets renders be shown; the MetaHuman files themselves stay out of this repository); the voices and acting folders beneath carry their own third-party rows",
    "production/reference": "approved reference pictures, copied in from where they were made and listed with their provenance in production/reference/README.md; hook-sheet.png (pass 4 of the 22 September regeneration, approved that night) and hook-sheet-2026-09-09-retired.png (the sheet it replaced) are both this project's own work, made by tools/imagegen running Z-Image-Turbo (Apache-2.0) through stable-diffusion.cpp (MIT) on Jafar's machine, no fetched asset as an input",
    # The reduced previews, 3 October (Jafar: "so outside reviewers can see the work"): our
    # own frames only, made smaller by tools/make_preview.py; no other game's frame is previewed.
    "production/assets/office-print": "Mickey's office's printed matter (fares, licence, calendar, the fare book, the drivers' board, notes, the radio's faceplate), drawn by tools/props/make_office_print.py in the project's OFL fonts and Patrick Hand (OFL, credited in THIRD-PARTY.md), the calendar's picture a crop of a Poly Haven CC0 photograph already credited there",
    "production/previews": "reduced copies (about 1600 px, JPEG) of this project's own frames, each proof-view step's and each picture on Jafar's pages, made by tools/make_preview.py from the Unreal probe's renders of this project's own piece list, carrying the ambientCG and CityPack textures this file attributes separately; no other game's frame",
    "production/d1-probe": "rendered by the Unreal probe from this project's own piece list, carrying the ambientCG and CityPack textures this file attributes separately, committed by CI every run; the live path, unarchived; and the walk's sound, recorded by the engine from the street's own ambience and the crowd voices this file attributes separately",
    "legacy/studio-v2/production/d1-probe": "rendered by the Unreal probe from this project's own piece list, carrying the ambientCG and CityPack textures this file attributes separately, committed by CI every run; archived 2026-09-22 with the studio, path changed and nothing else",
    "legacy/studio-v2/old-copies": "saved on 26 September from the two old copies before their deletion, the files found nowhere on GitHub: the old studio's prop models, level-of-detail cuts made by this project's own tools/meshgen/blender/clean_lod.py from the CC0 base meshes attributed in ledger/Assets/Props/base-mesh/THIRD-PARTY.md, and the supervisor's small status files and answer receipts; anything carrying a token or chat id went to Jafar's Dropbox backup instead",
}

# File types that are content rather than code. A directory holding only text
# or json is a manifest, not an asset drop.
#
# THIS SET NO LONGER HAS TO BE COMPLETE, and that is the point of the change on
# 1 Sep. It used to be the only classifier, so every format nobody thought of
# fell out of the bottom in silence: .hdr and .exr on 24 Aug, .webp the same
# day, then .glb, .mtl, .bin and .npz found on 1 Sep, four formats and 95
# files (37 + 12 + 23 + 23, counted by `--census` on the day) hiding behind a
# check whose entire job is noticing somebody else's files. `NOT_ASSET_SUFFIXES` below is the other half, and anything in neither
# set is printed and fails, so the next omission announces itself on the first
# run instead of after a month.
ASSET_SUFFIXES = {".uasset", ".fbx", ".png", ".jpg", ".jpeg", ".tga", ".psd", ".wav",
                  # .gif ADDED 7 SEP 2026, and this check caught it on
                  # the first run that produced one, which is what the
                  # comment above promises. The walk probe stitches its
                  # sequence frames into one animated GIF, so a GIF here
                  # is the same kind of thing a .png already is: a
                  # picture, which may be ours or may be somebody
                  # else's, and must therefore be classified rather
                  # than waved through.
                  ".gif",
                  # .svg ADDED 10 SEP 2026, caught on the first run that
                  # produced one, same as .gif before it. An SVG is markup
                  # rather than pixels, which is the argument for the other
                  # set, and it is refused here for the reason .gif was
                  # accepted: it is A PICTURE, it can embed raster data or
                  # somebody else's line work, and a kind that CAN carry
                  # third-party content is classified rather than waved
                  # through. The seven in the tree today are ours, drawn by
                  # production/art/mickeys-cars/author/draw_cab_office.py and
                  # draw_parade_night.py from this project's own data, and
                  # the production/art OURS row covers them BY PREFIX.
                  # Read that row's own words before trusting it: on
                  # 2026-09-10 it said "Blender previews only, under
                  # production/art/*/previews" and covered 28 files of which
                  # ZERO were under previews. Queue 153 owns that. If an SVG
                  # ever arrives from outside, this side of the union is
                  # where it has to declare itself.
                  ".svg",
                  ".mp3", ".ogg", ".ttf", ".otf", ".bundle", ".obj", ".blend",
                  # RADIANCE AND OPENEXR, ADDED 24 AUG BECAUSE THEY WERE
                  # MISSING AND THE CHECK WAS SILENT ABOUT IT. 23MB of Poly
                  # Haven captures sat under `Assets/Sky` for a day with a
                  # mapping row pointing at them, and this sweep reported
                  # nothing, not "unaccounted", not "ok", nothing, because
                  # a directory holding only unlisted suffixes reads as a
                  # directory holding no assets. That is rule 3b exactly:
                  # a clean result that cannot tell "nothing there" from
                  # "nothing looked at", on the one check whose entire job
                  # is noticing somebody else's files.
                  ".hdr", ".exr",
                  # And .webp, found missing the SAME DAY .hdr was: the
                  # reference frames landed as four .webp and one .png, and
                  # the sweep reported "1 asset file(s) attributed" over a
                  # directory of five. A suffix allow-list silently discards
                  # every format nobody thought of, twice in one day now.
                  ".webp",
                  # GLTF BINARY AND ITS TEXT SIBLING, ADDED 1 SEP. 37 models
                  # under `Props/base-mesh`, the third instance of the fault
                  # the two comments above describe, and this one hid a whole
                  # ROW rather than a count: `base-mesh` produced no line at
                  # all, so "The Base Mesh" was never checked against
                  # THIRD-PARTY.md once. `.gltf` is listed with it because it
                  # is the same exporter's other output and a fetch that
                  # returns one can return the other.
                  ".glb", ".gltf",
                  # WAVEFRONT MATERIALS, the sidecar to `.obj`, which has been
                  # on this list since it was written. 12 under
                  # `Props/oga-vehicles/lowpoly-public-transport`, one per
                  # `.obj`. Half a model was being counted and half was not,
                  # which is the same file arriving under two names.
                  ".mtl",
                  # THE PRECOMPUTED VOICE CONDITIONING, 23 pairs under
                  # `game-design/voice-conds`, and the ruling to list them is
                  # written out at the WATCHED row above because the reason is
                  # about provenance rather than about format.
                  #
                  # THE FORMAT ARGUMENT, WHICH IS SEPARATE AND ALSO SETTLED.
                  # `.bin` is deliberately broad. It is the suffix of the
                  # buffer a `.gltf` keeps its geometry in, so a model fetch
                  # can land one without anybody deciding to; and an opaque
                  # file nobody can identify from its name is precisely the
                  # thing that needs a row rather than the thing to exempt.
                  # It costs nothing today: outside `voice-conds` the repo
                  # holds none, and `/obj/`, `/bin/` and `/Library/` are
                  # already excluded from the walk, so C# build output cannot
                  # reach it.
                  ".bin", ".npz",
                  # AND `.flac`, WHICH CAME OUT OF GREPPING FOR THE SAME BUG
                  # RATHER THAN OUT OF THE TREE. There are none today, so it
                  # is the one entry here with no file behind it. The evidence
                  # is that two live tools already expect one:
                  # `tools/voice-live/speak.py:255` and
                  # `tools/voice-cast-check.py:96` both scan the voice
                  # directories for `(".wav", ".mp3", ".flac")`. A clip format
                  # this project's own code will happily pick up belongs on
                  # the list before it arrives, not after.
                  #
                  # NOTHING ELSE WAS ADDED ON SPECULATION, and that is a
                  # ruling. `content-sourcing.md` 1.3 recommends `.dae`,
                  # `.usdz`, `.svg`, `.tif` and `.tiff` as well; none of them
                  # has a single file in the tree, and a list padded with
                  # formats nobody has fetched is a bound chosen first and
                  # defended afterwards. The residue check is what makes the
                  # padding unnecessary: the day one lands it is named on the
                  # first run.
                  ".flac"}

# THE OTHER HALF OF THE CLASSIFIER, AND THE HALF THAT MAKES THE FIRST ONE SAFE.
# Everything here was looked at and ruled NOT content: code, documents,
# manifests, configuration, build leftovers. The union of the two sets has to
# cover every file walked, so a suffix nobody has ruled on lands in the
# unclassified residue and is named out loud. A decision is inherited by the
# next reader; an omission is not.
NOT_ASSET_SUFFIXES = {
    # .request ADDED 7 SEP 2026, caught by this check on the first run
    # that produced one. It is a one-line SENTINEL: a workflow whose
    # push trigger is a single path reads its content as the reason
    # for the run. Plain text this project writes, carrying no
    # third-party anything, and the only reason it is named here
    # rather than waved through is that the union of the two sets has
    # to cover everything walked.
    ".request",
    # Source and build products of source.
    ".cs", ".py", ".pyc", ".sh", ".bat", ".cmd", ".ps1", ".h", ".cpp", ".mjs",
    ".shader", ".csproj", ".uproject", ".yml", ".ini",
    # `.uasset` WAS RULED A BUILD PRODUCT HERE, AND THE COMMENT BELOW SAID WHEN THAT WOULD BE
    # WRONG. It was, by 5 October: 1,700 of them, from Epic's MetaHuman presets, the clothing
    # session's garments and the import scripts. Moved to ASSET_SUFFIXES that day; the history:
    # The only one in the tree is `ue-probe/Content/Ledger/M_LedgerSurface`,
    # generated by `tools/ue/make_base_material.py` running head-less in the
    # cook step, from a graph this project wrote. It carries no third-party
    # content: it is a material with TEXTURE PARAMETERS, and the textures
    # bound into those parameters at runtime are the ambientCG and CityPack
    # files this file already attributes on the other side. A hand-made
    # uasset would be a different question and D1b already refuses one, so
    # the day a `.uasset` appears that no script generated, THIS COMMENT IS
    # WRONG and the entry comes out.
    # Compiled binaries are third-party OFTEN, but they are code and the
    # licence allowlist governs them, not this file. The only one in the tree
    # is `Microsoft.ML.OnnxRuntime.dll` under `ledger/.onnx-cache/`, which is
    # gitignored local cache and excluded from the walk by path as well.
    ".dll",
    # Documents, manifests, data and logs.
    ".md", ".txt", ".json", ".tsv", ".html", ".log",
    # .lock ADDED 26 SEP 2026: the old studio supervisor's one-line lock files,
    # archived from the old copies (legacy/studio-v2/old-copies); plain text.
    ".lock",
    # .jsonl ADDED 28 SEP 2026, caught by this check on the first run that
    # produced one: the claim-check bench's test conversations, labels and
    # results (production/research/invented-claims/bench), one JSON object per
    # line, written by ledger/ClaimBench and the models it calls; text this
    # project made, carrying no third-party anything.
    ".jsonl",
    # .xlsx ADDED 24 SEP 2026, caught by this check on the first push after
    # the runtime-AI business research came onto main: its
    # runtime-ai-business-model.xlsx is a spreadsheet this project wrote,
    # numbers and formulas, carrying no third-party anything.
    ".xlsx",
    # Extensionless: hooks, `.gitignore`, `ledger/.verify-footer`. `suffix` is
    # empty for a dotfile with no second dot, so this bucket is where they land.
    "",
    # MIXAMO FBX SET ASIDE BY THE PICKER, and this is a ruling rather than an
    # oversight, so it is written down. `*.fbx.rejected` has suffix
    # `.rejected`, so 3.6MB of animation is invisible to an `.fbx` sweep.
    # It is NOT listed as an asset for one measured reason: 5 of the 7 in the
    # tree are untracked, so the count would vary with whether somebody had
    # run the picker locally and the denominator would mean a different thing
    # on every machine. The obligation is already recorded either way, because
    # every one of them sits under `ledger/Assets/Characters`, which is a
    # watched row carrying the Mixamo token. If a `.rejected` ever appears
    # OUTSIDE a watched directory this ruling should be revisited, and the
    # census under `--census` is where that would show.
    ".rejected",
}

# Paths the walk is not responsible for: version control, dependency trees,
# compiler output and local caches. `/.onnx-cache/` is gitignored, holds one
# vendored runtime DLL, and is a machine-local artefact rather than repository
# content.
SKIP_FRAGMENTS = ("/.git/", "/node_modules/", "/.venv", "/obj/", "/bin/",
                  "/Library/", "/__pycache__/", "/.onnx-cache/",
                  # THE UNREAL BUILD'S OWN OUTPUT, added 2026-09-22 for the
                  # same reason /obj/ and /bin/ are already here. All of it is
                  # in .gitignore, so none of it exists in CI and this sweep
                  # never saw it there - but the moment a build runs on
                  # Jafar's PC it leaves tens of thousands of .bin, .obj, .exe
                  # and .rsp files under ue-probe/, and the check went red
                  # naming build artefacts as unattributed assets. A check
                  # that only passes on a machine which has never built is a
                  # check the machine that builds cannot be asked to run.
                  "/ue-probe/Intermediate/", "/ue-probe/Binaries/",
                  "/ue-probe/Saved/", "/ue-probe/Packaged/",
                  "/ue-probe/Build/", "/ue-probe/DerivedDataCache/",
                  # THE GAME'S STAGED DATA (30 September): tools/ue/
                  # stage_game_data.py copies the game's run-time files, each
                  # attributed at its source path, into this gitignored folder
                  # before a package; staged on this PC, the walk counted every
                  # voice clip twice, the copy as unattributed.
                  "/ue-probe/Content/LedgerData/",
                  # CLAUDE CODE'S OWN HELPER WORKTREES (29 September): a helper
                  # run in isolation leaves a whole second checkout under
                  # .claude/worktrees/, gitignored and never in CI; walking it
                  # counted every asset twice, the copy as unattributed.
                  "/.claude/worktrees/",
                  # THE PROBE'S LOCAL RUN OUTPUT: every run of the game writes
                  # its frames, sounds and logs as ue-probe/ue-*; the build
                  # machine copies what it keeps into production/d1-probe, and
                  # none of it is ever committed from here (gitignored).
                  "/ue-probe/ue-")

_fails = []


def has(token, text):
    """A row's token, or every one of several (5 October: one Unreal folder can rest on more than
    one source, the cast's MetaHumans on Epic's presets, FreeSewing's cap and VCTK's voices)."""
    return all(t in text for t in (token if isinstance(token, tuple) else (token,)))


def check(ok, what, got=""):
    print(("  ok   " if ok else "  FAIL ") + what + ("" if ok else f": {got}"))
    if not ok:
        _fails.append(what)


def cap(items, limit=5):
    """A list rendered for a message, SAYING when it truncated.

    A cap that does not announce itself reads as a finding. `| head -3` in the
    character-extraction step once turned seventeen lines into three and was
    read as "three of five bodies failed"; nothing was broken.
    """
    shown = ", ".join(str(x) for x in items[:limit])
    extra = len(items) - limit
    return shown + (f" (+{extra} more not shown)" if extra > 0 else "")


def under(rel, row):
    """Is `rel` the row itself or inside it?

    Prefix matching on path COMPONENTS, not substring. The old sweep asked
    `str(watched) in str(path)`, which would have whitelisted a stray under
    `ledger/Assets/PropsOld` on the strength of the `Props` row.
    """
    return rel == row or rel.startswith(row + "/")


def sweep(root):
    """One walk, one classifier, every file the check is responsible for.

    Returns (walked, assets, unclassified) as lists of POSIX-relative strings,
    plus a Counter of every suffix seen. ONE IMPLEMENTATION: the row counts,
    the stray check, the residue check and the census all read this, so no two
    of them can disagree about what is an asset, and every number printed in
    one run comes from one walk at one instant.
    """
    walked, assets, unclassified = [], [], []
    kinds = collections.Counter()
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        s = "/" + str(p.relative_to(root).as_posix())
        if any(f in s + "/" for f in SKIP_FRAGMENTS):
            continue
        rel = s[1:]
        suf = p.suffix.lower()
        walked.append(rel)
        kinds[suf] += 1
        if suf in ASSET_SUFFIXES:
            assets.append(rel)
        elif suf not in NOT_ASSET_SUFFIXES:
            unclassified.append(rel)
    return walked, assets, unclassified, kinds


def audit(root=None, doc=None):
    root = root or ROOT
    doc = doc if doc is not None else DOC
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""
    check(bool(text), "THIRD-PARTY.md exists", "missing")
    if not text:
        return

    walked, assets, unclassified, kinds = sweep(root)
    walked_set = set(walked)
    asset_set = set(assets)

    for rel, token in sorted(WATCHED.items()):
        d = root / rel
        if not d.exists():
            # Not yet populated. Not a failure, CityPack does not exist until
            # M17.6 lands, but the row still has to be there waiting for it,
            # so the obligation is recorded before the asset arrives rather
            # than after somebody notices.
            check(has(token, text),
                  f"{rel}: attribution recorded ahead of the assets",
                  f"no '{token}' in THIRD-PARTY.md")
            continue
        # A WATCHED ENTRY MAY BE A SINGLE FILE, and until 5 August one would
        # have been skipped in silence.
        #
        # `rglob` on a file yields nothing, so `assets` came back empty and the
        # loop moved on WITHOUT checking the token: the entry would sit in the
        # table looking enforced while enforcing nothing. That is the same shape
        # as the check itself never being wired into `verify.py`, one level in.
        #
        # The shipped font is the real case: one `.ttf` in `Resources`, beside
        # code and prefabs, so there is no directory to point at that would not
        # also swallow half the project.
        if d.is_file():
            check(has(token, text), f"{rel}: the shipped file is attributed",
                  f"no '{token}' in THIRD-PARTY.md")
            continue
        # Row counts NEST where rows nest: `Props/base-mesh` is inside `Props`,
        # so its files are counted on both lines and the row lines do not sum
        # to the run total. The whole-run figures are on the sweep line below.
        n_assets = sum(1 for a in asset_set if under(a, rel))
        n_walked = sum(1 for w in walked_set if under(w, rel))
        if n_assets:
            check(has(token, text),
                  f"{rel}: {n_assets} asset file(s) of {n_walked} walked, attributed",
                  f"no '{token}' in THIRD-PARTY.md")
            continue
        # THE BRANCH THAT USED TO BE `continue`, AND IT IS WHY 016 EXISTS.
        # A populated directory whose files are all of kinds the sweep cannot
        # see produced NO LINE: `Props/base-mesh` held 37 `.glb` and the row's
        # token went unchecked for a month. Silence and clean read identically,
        # so this branch now prints either way and carries its denominator.
        # The token is still checked, on the ahead-of-the-assets wording,
        # because a row with nothing countable under it is exactly the case
        # that wording was written for.
        check(has(token, text),
              f"{rel}: no asset file among {n_walked} walked, "
              f"attribution recorded ahead of the assets",
              f"no '{token}' in THIRD-PARTY.md")

    # A CC BY corpus needs its exact required wording present, not a paraphrase:
    # "we mention VCTK somewhere" is not what the licence asks for.
    check("CC BY 4.0" in text, "the CC BY licence is named exactly")
    check("Centre for Speech Technology Research" in text,
          "and the attribution text the licence requires is written out")

    # UNTRACKED ASSET DIRECTORIES. The check above only knows what it was told
    # about, which would make it useless the day somebody adds a folder, so
    # this sweeps for asset files anywhere outside a watched directory.
    known = list(WATCHED) + list(OURS)
    stray = sorted(a for a in assets if not any(under(a, k) for k in known))
    check(not stray,
          f"no asset files live outside a directory this file knows about "
          f"({len(assets)} asset file(s) of {len(walked)} walked, examined)",
          cap(stray))

    # THE RESIDUE, AND IT IS THE INSTRUMENT RATHER THAN A RULE ABOUT TODAY.
    # Anything whose suffix is in neither declared set. A zero here ships the
    # denominator beside it, so "no unknown kinds" cannot be confused with
    # "nothing was walked", which is the confusion that hid `.glb` for a month.
    res_kinds = sorted(collections.Counter(
        pathlib.PurePosixPath(u).suffix.lower() or "(no-suffix)"
        for u in unclassified).items(), key=lambda kv: -kv[1])
    check(not unclassified,
          f"every file kind walked is ruled asset or not-asset "
          f"({len(unclassified)} unclassified of {len(walked)} walked)",
          cap([f"{k}x{n}" for k, n in res_kinds]) + " ~ " + cap(unclassified, 3))

    # And what we made ourselves is recorded as ours, so "no attribution row"
    # is a decision on the record rather than an omission nobody noticed.
    for rel, why in sorted(OURS.items()):
        d = root / rel
        if not d.exists():
            continue
        n = sum(1 for a in asset_set if under(a, rel))
        print(f"  ours  {rel}: {n} file(s), {why}")

    # THE DONE LINE. Whole-run numbers only, all from the single sweep above,
    # so a reader greping across lines cannot pick up two moments as one. Row
    # lines carry per-row counts and those overlap where rows nest.
    covered = len(assets) + sum(
        n for k, n in kinds.items() if k in NOT_ASSET_SUFFIXES)
    print(f"  sweep walked={len(walked)} assetFiles={len(assets)} "
          f"assetKinds={len(set(kinds) & ASSET_SUFFIXES)}/{len(ASSET_SUFFIXES)}declared "
          f"unclassified={len(unclassified)} "
          f"ruled={covered}/{len(walked)} rows={len(WATCHED)}")


# ---- WHAT THE PACKAGE CARRIES (5 October 2026, phase 0's exit review) ----------------------------
#
# PLAN.md's phase 0 asks for the sources recorded on what the friends' build carries, not on the
# repository alone. The package's own manifests list every file it ships. Each is traced to a row:
# the game's Unreal content to the folders above, the staged run-time data to its source file in
# the repository (ruled by the sweep), the engine's content to the Unreal Engine row. Anything
# else, and anything named below as never to ship, fails.
PACKAGE = ROOT / "ue-probe" / "Packaged" / "Windows"
NEVER_SHIP = (
    # Ron's jacket draped in Marvelous Designer's 14-day trial: evaluation only (its terms,
    # section 3.1.1; DECISIONS.md, 1 and 2 October); DefaultGame.ini never cooks it.
    "/Content/Ledger/Cloth/ron_md_jacket/",
    # The NoAI ruling of 3 October removed every Fab and Megascans item.
    "/Content/Fab/", "Megascans", "Quixel",
)


def package_files(pkg):
    out = []
    for name in ("Manifest_UFSFiles_Win64.txt", "Manifest_NonUFSFiles_Win64.txt"):
        f = pkg / name
        if f.exists():
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                path = line.split("\t")[0].strip().replace("\\", "/")
                if path:
                    out.append(path)
    return out


def package_audit(pkg=None, root=None, doc=None):
    """Every file the package ships, traced to a row. Returns the problems."""
    pkg = pkg or PACKAGE
    root = root or ROOT
    doc = doc if doc is not None else DOC
    text = doc.read_text(encoding="utf-8") if doc.exists() else ""
    files = package_files(pkg)
    if not files:
        print(f"  package {pkg}: no manifest here, nothing to trace (packages=0)")
        return []
    known = list(WATCHED) + list(OURS)
    bad, counts = [], collections.Counter()
    for f in files:
        if any(n in "/" + f for n in NEVER_SHIP):
            bad.append(f"never to ship: {f}")
            continue
        if f.startswith("LedgerProbe/Content/Ledger/"):
            src = "ue-probe/Content/Ledger/" + f[len("LedgerProbe/Content/Ledger/"):]
            src = re.sub(r"\.(uexp|ubulk|uptnl|m\.ubulk)$", ".uasset", src)
            if not any(under(src, k) for k in known):
                bad.append(f"no row for the game's own content: {f}")
            counts["game content"] += 1
        elif f.startswith("LedgerProbe/Content/LedgerData/"):
            src = f[len("LedgerProbe/Content/LedgerData/"):]
            if pathlib.PurePosixPath(src).suffix.lower() in ASSET_SUFFIXES and not any(under(src, k) for k in known):
                bad.append(f"staged data with no row: {f}")
            counts["staged data"] += 1
        elif f.startswith(("Engine/", "LedgerProbe/Plugins/")):
            counts["engine"] += 1
        elif f.startswith(("LedgerProbe/Binaries/", "LedgerProbe/Config/", "LedgerProbe/Content/Paks/")) or \
                f in ("LedgerProbe.exe", "NOTICES.txt", "LedgerProbe/LedgerProbe.uproject", "LedgerProbe/AssetRegistry.bin") or \
                f.startswith("LedgerProbe/Content/ShaderArchive") or f.startswith("LedgerProbe/Content/ShaderTypeInfo"):
            counts["code and settings"] += 1
        else:
            bad.append(f"a file the check cannot place: {f}")
    if counts["engine"] and not has("Unreal Engine", text):
        bad.append("the package ships the engine's content and THIRD-PARTY.md has no Unreal Engine row")
    print(f"  package {pkg}: files={len(files)} " + " ".join(f"{k.replace(' ', '-')}={n}" for k, n in sorted(counts.items()))
          + f" problems={len(bad)}")
    for b in bad[:12]:
        check(False, f"package {b}")
    if not bad:
        check(True, f"package: every one of {len(files)} shipped files traced to a row")
    return bad


def census(root=None):
    """THE PRINTER THE SUFFIX SETS ARE SET FROM, and it ships with them.

    Every suffix in the tree with its file count, its bytes and where it
    lives, marked asset / not-asset / UNCLASSIFIED. A set chosen first and
    defended afterwards is a rounding wearing a measurement's clothes; this is
    what the 1 Sep set was read off, and it is what the next reader reads
    before changing it.
    """
    root = root or ROOT
    walked, assets, unclassified, kinds = sweep(root)
    size = collections.Counter()
    where = collections.defaultdict(set)
    for rel in walked:
        p = root / rel
        suf = p.suffix.lower()
        size[suf] += p.stat().st_size
        where[suf].add(str(pathlib.PurePosixPath(rel).parent))
    print(f"attribution-check census: {len(walked)} file(s) walked under {root}\n")
    print(f"  {'kind':<14}{'ruling':<14}{'files':>7}{'MB':>9}  directories")
    for suf, n in kinds.most_common():
        if suf in ASSET_SUFFIXES:
            ruling = "asset"
        elif suf in NOT_ASSET_SUFFIXES:
            ruling = "not-asset"
        else:
            ruling = "UNCLASSIFIED"
        dirs = sorted(where[suf])
        print(f"  {suf or '(no-suffix)':<14}{ruling:<14}{n:>7}{size[suf] / 1e6:>9.2f}  "
              + cap(dirs, 2))
    declared_unused = sorted(ASSET_SUFFIXES - set(kinds))
    print(f"\n  kinds={len(kinds)} assetFiles={len(assets)} "
          f"unclassified={len(unclassified)} of {len(walked)}walked")
    print("  asset kinds declared but absent from the tree: "
          + (cap(declared_unused, 20) if declared_unused else "none"))
    return 0


def _quiet(fn):
    """Run one fixture, keep its check lines out of the transcript.

    The old selftest printed the whole audit for every fixture, four full
    dumps for four assertions, so the four verdict lines that matter were
    buried in sixty that did not. The failing check NAMES are returned instead
    and printed under the fixture that produced them.
    """
    import io
    global _fails
    _fails = []
    buf, old = io.StringIO(), sys.stdout
    sys.stdout = buf
    try:
        fn()
    finally:
        sys.stdout = old
    return list(_fails)


def selftest():
    """The check, watched PASSING and watched FAILING, in that order.

    ACCEPTING CASE FIRST, and it is first because the expensive failure is a
    validator nothing survives: a licence gate that refuses everything gets
    switched off, and one that refuses nothing reads as compliance. Until
    1 Sep this function had four fixtures and every one of them was a
    REJECTING case, so "4/4 checks go red on broken input" was the whole of
    what had ever been watched. The live repository is the accepting fixture,
    which is the best one available: it cannot be tuned to make the tool pass,
    because it is the thing the tool is for.
    """
    import tempfile
    global _fails
    passed = failed = 0
    ACCEPTING = 4

    def expect_green(name, fn):
        nonlocal passed, failed
        fails = _quiet(fn)
        if not fails:
            passed += 1
            print(f"  ok   ACCEPT  {name}")
        else:
            failed += 1
            print(f"  FAIL ACCEPT  {name}: refused good input: {cap(fails, 3)}")

    def expect_red(name, fn, mentions, only=False):
        """`mentions` pins WHICH check went red.

        A fixture that only asks "something failed" passes for any reason at
        all, and in a tree where a dozen rows are unpopulated something always
        fails. Every rejecting case below names the check it is about.
        """
        nonlocal passed, failed
        fails = _quiet(fn)
        hit = [f for f in fails if mentions in f]
        if hit and (not only or len(fails) == len(hit)):
            passed += 1
            print(f"  ok   REFUSE  {name}: {cap(hit, 1)}")
        elif not fails:
            failed += 1
            print(f"  FAIL REFUSE  {name}: passed on broken input")
        elif not hit:
            failed += 1
            print(f"  FAIL REFUSE  {name}: went red for the wrong reason: {cap(fails, 3)}")
        else:
            failed += 1
            print(f"  FAIL REFUSE  {name}: {len(fails) - len(hit)} unrelated "
                  f"check(s) also red: {cap([f for f in fails if f not in hit], 3)}")

    def full_doc(path, omit=None):
        """A THIRD-PARTY.md naming every token this file demands, less one."""
        toks = sorted({t for v in WATCHED.values() for t in (v if isinstance(v, tuple) else (v,))} - {omit})
        path.write_text(" ".join(toks) + "\nCC BY 4.0\n"
                        "Centre for Speech Technology Research\n", encoding="utf-8")

    print("attribution-check selftest\n")
    print("ACCEPTING CASES (the tool must not refuse these)\n")

    # 1. THE LIVE TREE. If this goes red the repository has a real attribution
    #    problem, and the selftest is the wrong place to learn it, which is why
    #    the failing check names are printed rather than a bare count.
    expect_green("the live repository passes its own check",
                 lambda: audit(ROOT, DOC))

    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)

        # 2. THE AHEAD-OF-THE-ASSETS BRANCH, ACCEPTING HALF. No directory
        #    exists; every token is written down. This is the live shape of
        #    `production/assets/vignette` tonight, and the branch had no
        #    fixture of either kind until 1 Sep: the accepting half was only
        #    ever watched by hand, which is a claim about a manual run.
        full_doc(tmp / "THIRD-PARTY.md")
        expect_green("an obligation recorded before the bytes arrive is accepted",
                     lambda: audit(tmp, tmp / "THIRD-PARTY.md"))

        # 3. A populated tree that is fully attributed.
        (tmp / "game-design/picked-clips").mkdir(parents=True)
        (tmp / "game-design/picked-clips/lena.p228.mp3").write_bytes(b"x")
        (tmp / "ledger/Assets/Props/base-mesh").mkdir(parents=True)
        (tmp / "ledger/Assets/Props/base-mesh/bench.glb").write_bytes(b"x")
        expect_green("attributed assets, including a .glb, are accepted",
                     lambda: audit(tmp, tmp / "THIRD-PARTY.md"))

        print("\nREJECTING CASES (the tool must refuse these)\n")

        # 4. THE AHEAD-OF-THE-ASSETS BRANCH, REJECTING HALF, and `only=True`
        #    so it also proves the other fifteen rows stayed green. One token
        #    removed, exactly one row red.
        full_doc(tmp / "THIRD-PARTY.md", omit="CityPack")
        expect_red("an obligation NOT recorded ahead of the assets is caught",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "CityPack", only=True)

        # 5. A watched directory that exists and holds nothing the sweep can
        #    see. THIS IS QUEUE ITEM 016 IN A FIXTURE: before 1 Sep this row
        #    hit `if not assets: continue` and the token was never tested, so
        #    the tool passed while enforcing nothing. The fixture uses a
        #    declared not-asset suffix rather than an unlisted one on purpose:
        #    the silence must not come back the day the residue check is
        #    satisfied.
        full_doc(tmp / "THIRD-PARTY.md", omit="The Base Mesh")
        (tmp / "ledger/Assets/Props/base-mesh/bench.glb").unlink()
        (tmp / "ledger/Assets/Props/base-mesh/README.md").write_text("x", encoding="utf-8")
        # Since 5 October two rows rest on The Base Mesh (the props' source folder and their
        # Unreal imports), so both go red and nothing else may.
        expect_red("a watched directory with no visible asset is not silent",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "Props", only=True)

        # 6. no attribution file at all
        (tmp / "THIRD-PARTY.md").write_text("", encoding="utf-8")
        expect_red("a missing THIRD-PARTY.md is caught",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "THIRD-PARTY.md exists")

        # 7. a file that does not name the corpus behind assets that are present
        (tmp / "THIRD-PARTY.md").write_text("# nothing in particular\n", encoding="utf-8")
        expect_red("assets with no attribution row are caught",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "picked-clips")

        # 8. names the corpus but not the licence the corpus requires
        (tmp / "THIRD-PARTY.md").write_text("VCTK Mixamo CityPack\n", encoding="utf-8")
        expect_red("naming the corpus without its licence is caught",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "the CC BY licence is named exactly")

        # 9. an asset file in a directory nothing knows about
        full_doc(tmp / "THIRD-PARTY.md")
        (tmp / "stray").mkdir()
        (tmp / "stray/mystery.png").write_bytes(b"x")
        expect_red("an asset in an unknown directory is caught",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "no asset files live outside")
        (tmp / "stray/mystery.png").unlink()

        # 10. THE ACCEPTANCE TEST QUEUE ITEM 016 ASKS FOR, in its own fixture
        #     rather than folded into the one above: an unattributed model
        #     anywhere in the repository is REFUSED. Before 1 Sep the stray
        #     sweep could not see a `.glb` at all, so this file landed in
        #     silence and the run stayed green.
        (tmp / "stray/period_car.glb").write_bytes(b"x")
        expect_red("an unattributed .glb anywhere in the repo is caught",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "no asset files live outside")
        (tmp / "stray/period_car.glb").unlink()

        # 11. THE RESIDUE, which is the half that outlives today's suffix list.
        #     A format in neither declared set is NAMED rather than dropped.
        #
        #     THE SUFFIX IS CHOSEN AT RUN TIME, NOT WRITTEN IN. A rejecting
        #     fixture pinned to a real asset kind breaks the day somebody does
        #     the work, and `content-sourcing.md` already recommends fetching
        #     USDZ and DAE. So the fixture takes the first candidate that IS
        #     still unruled, and the last candidate can never be a real format,
        #     which means no future suffix ruling can turn this case green by
        #     accident.
        unruled = next(s for s in (".usdz", ".dae", ".abc", ".no-such-kind")
                       if s not in ASSET_SUFFIXES and s not in NOT_ASSET_SUFFIXES)
        (tmp / f"stray/hydrant{unruled}").write_bytes(b"x")
        expect_red(f"a file kind ruled neither asset nor not-asset is named ({unruled})",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "every file kind walked is ruled")
        (tmp / f"stray/hydrant{unruled}").unlink()

        # 12. A STRAY IN A DIRECTORY WHOSE NAME MERELY STARTS WITH A WATCHED
        #     ONE. Found while writing `under()` rather than by a report, so
        #     it gets a fixture rather than a sentence in a docstring: the old
        #     sweep asked `str(watched_path) in str(path)`, so anything under
        #     `ledger/Assets/PropsOld/` was whitelisted on the strength of the
        #     `ledger/Assets/Props` row and never reported. Watched failing on
        #     HEAD's copy of this tool before the fixture was written.
        (tmp / "ledger/Assets/PropsOld").mkdir(parents=True)
        (tmp / "ledger/Assets/PropsOld/mystery.fbx").write_bytes(b"x")
        expect_red("a stray under a directory that merely starts with a watched name",
                   lambda: audit(tmp, tmp / "THIRD-PARTY.md"),
                   "no asset files live outside")

        # 13 to 15. WHAT A PACKAGE CARRIES (5 October 2026): a package whose every file has its row
        #     passes; one carrying the Marvelous Designer trial's jacket, or a folder of the game's
        #     own content that no row names, is refused.
        full_doc(tmp / "THIRD-PARTY.md")
        pk = tmp / "pkg"
        pk.mkdir()
        good = ["LedgerProbe/Content/Ledger/People/Joe/SK_Joe.uasset\t2026-10-05T00:00:00Z",
                "LedgerProbe/Content/Ledger/Street/SM_QuayStreet.uexp\t2026-10-05T00:00:00Z",
                "LedgerProbe/Content/LedgerData/production/assets/people/joe.glb\t2026-10-05T00:00:00Z",
                "LedgerProbe/Binaries/Win64/LedgerProbe-Win64-Shipping.exe\t2026-10-05T00:00:00Z"]
        man = pk / "Manifest_UFSFiles_Win64.txt"
        man.write_text("\n".join(good) + "\n", encoding="utf-8")
        ACCEPT_PKG = lambda: package_audit(pk, tmp, tmp / "THIRD-PARTY.md")
        expect_green("a package whose every file has its row", ACCEPT_PKG)
        man.write_text("\n".join(good + ["LedgerProbe/Content/Ledger/Cloth/ron_md_jacket/SK_Jacket.uasset\tx"]) + "\n", encoding="utf-8")
        expect_red("a package carrying the Marvelous Designer trial's jacket", ACCEPT_PKG, "never to ship")
        man.write_text("\n".join(good + ["LedgerProbe/Content/Ledger/Mystery/SM_Thing.uasset\tx"]) + "\n", encoding="utf-8")
        expect_red("a package carrying a folder of the game's own content that no row names", ACCEPT_PKG,
                   "no row for the game's own content")

    _fails = []
    # ACCEPTING COUNT PRINTED BESIDE THE TOTAL, because "11/11 behaved" cannot
    # be told from eleven rejecting fixtures and no accepting one, which is
    # what this selftest was until 1 Sep.
    print(f"\n{passed}/{passed + failed} fixtures behaved "
          f"({ACCEPTING} accepting, {passed + failed - ACCEPTING} rejecting)")
    return 2 if failed else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if "--census" in sys.argv:
        return census()
    if "--package" in sys.argv:
        i = sys.argv.index("--package")
        pkg = pathlib.Path(sys.argv[i + 1]) if i + 1 < len(sys.argv) else None
        print("attribution-check --package: every file the package ships traced to a row\n")
        bad = package_audit(pkg)
        print()
        print("package ok" if not bad else f"{len(bad)} package problem(s)")
        return 1 if bad else 0
    print("attribution-check: every third-party asset is accounted for\n")
    audit()
    print()
    print("attribution ok" if not _fails else f"{len(_fails)} problem(s)")
    return 1 if _fails else 0


if __name__ == "__main__":
    # A correct run that ends in a BrokenPipeError stack trace costs twenty
    # minutes before anybody notices it worked. `| head` is how this tool gets
    # read.
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
