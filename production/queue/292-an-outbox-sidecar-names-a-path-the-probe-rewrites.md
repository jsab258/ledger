line: tools and channel
spec: an outbox photo sidecar carries `photo: <path>` and the sweep resolves
  that path AT SEND TIME, off the working tree. Every frame under
  production/d1-probe/ is written to a FIXED name and overwritten by each
  probe run (53 png at fixed names on 2026-09-14; no per-run copies, no
  sha-keyed directory). So a message queued before a landing and swept after
  it attaches a DIFFERENT PICTURE from the one its caption describes, with
  nothing anywhere reporting the substitution.
  IT NEARLY HAPPENED ON THE DAY THIS WAS FILED. 2026-09-14-the-street-before
  .answer.photo.txt names ue-vign_hook_day.png and its caption describes the
  OLD street at fog 0.450. The sweep sent it at 19:08:13Z against a checkout
  at 622bc39; the probe measured at 19:15:37Z and committed the new
  fog 0.100 frame to that same filename minutes later. Seven minutes the
  other way and Jafar would have received the after-frame captioned as the
  before, in a pair whose whole point is the difference between them.
  GIT HISTORY IS NOT THE MITIGATION, and it is worth saying because it is the
  first thing a reader will reach for: every run's frames are recoverable at
  that run's commit, which is why the verdict names its commit on line 1, but
  the SWEEP reads the working tree and never a commit. History fixes
  retrieval later; it does nothing for what leaves the machine.
acceptance: either the sidecar names a path that cannot be rewritten (a
  per-run copy keyed by short sha, which .claude/rules/ci.md already asks for
  and which no vignette frame has), or the sweep records the bytes it
  actually sent and refuses when the file changed after the message was
  written. Accepting case: a message sent with its intended picture, printed.
  Rejecting case, planted: a sidecar whose target is overwritten between the
  message's commit instant and the sweep, refused rather than sent, with the
  refusal naming both the file and the two instants.
max_sessions: 1
status: READY 2026-09-14. Found by the Producer while writing the judged
  frame's message, and it had already repointed the before-sidecar to
  ue-vign_fog_maxop0450.png before finding the sweep line that proved the
  send had beaten the landing; it reverted the edit rather than leaving a
  silent correction. The resident had seen the same overwrite earlier and
  dismissed it on the reasoning that git preserves each run's frames, which
  is true and does not answer this: the sweep never reads git. Related to
  queue 290, which is the same class one layer down (a frame the probe
  deletes before the channel can carry it at all).
