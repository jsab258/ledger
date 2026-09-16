line: instruments (ledger/verify.py, the fable-spend block; .claude/agent-log.tsv
  and whatever writes it)
spec: gameShareDay counts "how many spawns BUILT THE GAME rather than measuring
  or reviewing it" and computes it as `slot[2] += 1 if agent in GAME_AGENTS`.
  THAT IS A CLASSIFICATION BY ROLE, NOT BY WORK. An engine-specialist repairing
  an instrument counts as game work; an instrument-builder adding a gameplay
  readback counts as studio work. The key's own comment says it asks "WHICH
  MODEL, not WHICH WORK" of the fable share, while itself asking which ROLE and
  claiming which WORK.
acceptance: either the classification reads what a spawn TOUCHED, or the key
  and its stat string say in their own words that it is a role proxy and name
  the error it admits; not both halves left implied
max_sessions: 1
status: READY 2026-09-16, raised by Jafar from an external audit, which notes
  the previous audit said the same in September. Twice-reported is the reason
  this is not a nit.

  VERIFIED AT THE SITE: ledger/verify.py:5190, `slot[2] += 1 if agent in
  GAME_AGENTS else 0`. Nothing else feeds it.

  HIS TWO OPTIONS ARE NOT EQUALLY AVAILABLE, and that is the finding this item
  adds to his instruction. `.claude/agent-log.tsv` has exactly five columns:
  when, agent, model, reason, agentId. IT RECORDS NOTHING ABOUT WHAT A SPAWN
  TOUCHED. So:

    - "print it with that limitation named" is available today and is one
      string, in the key's own stat text where a reader meets it.
    - "classify by what a spawn touched" needs data that is not captured. It
      means a sixth column written by whatever appends the log, or correlating
      spawns to the diffs that followed them, and the second is a guess dressed
      as a measurement whenever two spawns overlap, which in this session they
      routinely do.

  SO THE ORDER IS: name the limitation now, in the same batch this item is
  read, and file the capture separately if it is wanted. A number that admits
  what it is beats a number that is quietly wrong, and it beats waiting for
  the right number while the wrong one keeps printing.

  DO NOT DELETE THE KEY. It has been emitted since 26 Aug and its 71 per cent
  reading on 25 Aug is quoted in the file's own comment and in the budget rows;
  a key that vanishes takes its history with it. The limitation is a caption,
  not a retraction.

  UNDER D45 a tool that measures the game: a test, no review, no ruling record.
