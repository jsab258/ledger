line: tools (producer-check.py, ledger/verify.py marker provenance)
spec: NOTHING WRITES production/site-served.txt, and the two gates that read
  it cannot tell "publishing works" from "publishing worked once this
  morning". Measured 2026-09-15:

    references to `site-served` across .py/.yml/.sh/.md        19
    of those in code                                            4
    of those 4 that WRITE the file                              0
      (ledger/verify.py:1778 and producer-check.py:829 are the
       path constant; producer-check.py:316 and :751 are comments)
    commits touching the file in its whole history              2
      (ce564254, e1d19817, both hand-edits)

  The marker reads servedCommit=5a8ef789 printedBy=publish-glance/run-27
  /id-34932214186 servedAt=2026-09-15T05:20:56Z. The newest SUCCESSFUL
  publish-glance is run 37 (id 35021034653) at 2026-09-15T20:40:05Z on head
  24b54723, whose step 13 REQUEST THE PUBLISHED PAGES AND READ WHAT CAME BACK
  completed successfully. So the marker is ten runs and fifteen hours behind
  a page that IS current, and it decays that way by construction: the
  workflow publishes and the marker is updated by hand or not at all.

  WHAT THE PROVENANCE CHECK ACTUALLY VERIFIES, read out of
  ledger/verify.py rather than assumed: exactly one servedCommit line; a
  whole 40-hex sha; the sha is a commit in this repository; the sha is an
  ancestor of HEAD; printedBy names publish-glance and an /id-; servedUrl
  equals producer-check's SITE_ORIGIN. Six checks, all passing, none of them
  about WHEN. Its docstring is careful about its other boundaries ("nothing
  here re-reads the run") and does not name this one.

  SO THE FAILURE IS SILENT AND LANDS ON HIS PHONE. If publish-glance started
  failing tomorrow, all six checks would still pass, the link floor would
  stay LIVE, and the Producer would keep sending Jafar a link to a page that
  had stopped moving. That is the ci.md rule about verifying a job's EFFECTS,
  one level out: the effect was verified once and the verification was pinned.

  NOTHING WAS HIDDEN TONIGHT and the item should not pretend otherwise. Run
  37 succeeded and served the current commit; the page carries D38. This is
  latent, not live.

  THE FIX IS OFFLINE-COMPUTABLE, which matters because being offline is the
  stated reason the check stops where it does (it runs before every commit in
  a container whose network is not guaranteed). Two cheap bounds, neither
  needing the network: the marker already carries `servedAt`, so its AGE is
  present and unread; and pure git can ask whether any commit in
  servedCommit..HEAD touches a path in publish-glance.yml's own `paths:`
  filter, which is exactly the set that triggers a republish. If one does, a
  republish happened and the marker is behind BY CONSTRUCTION.

  AND THE DECAY IS ALREADY VISIBLE ONCE. tools/producer-check.py line 751
  says the sha "now in production/site-served.txt" is ada1535b, from run 26.
  The marker has since moved to 5a8ef789 and run 27, so that comment is one
  update behind the file it describes. A hand-maintained marker needs its
  describing comments hand-maintained too, and one of them already was not.
acceptance: the marker gains a writer, or the readers gain a freshness bound,
  and the accepting case is tested first: today's tree, with a marker that is
  behind, must produce whichever verdict the fix decides is correct, and a
  planted marker naming a commit with NO republish-triggering commit after it
  must produce the other. Both outcomes watched. Any bound prints what it
  compared and how far behind it found the marker, never a bare ok. If the
  answer is that the workflow writes the marker itself, the run that does it
  must be shown writing it, not shown succeeding.
max_sessions: 1
status: READY 2026-09-15, found while confirming that the D38 batch had been
  published as Jafar asked. It had: the publish half was done and the page is
  current. The marker said otherwise and was wrong in the harmless direction,
  which is the only reason this is a queue item and not an incident.
