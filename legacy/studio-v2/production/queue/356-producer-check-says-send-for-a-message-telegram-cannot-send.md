line: instruments (tools/producer-check.py, the register rules; and
  tools/runner/telegram-bot.py, which sends without measuring)
spec: `producer-check` returned SEND with 0 findings over 6 enforced rules for
  a message Telegram then REFUSED, and the refusal is not a judgement call:

      14:49:26  outbox: NOT SENT production/outbox/2026-09-16-your-four-items-
                one-is-yours-to-call.answer.md (Telegram said no (HTTP 400:
                Bad Request: message is too long)). It stays unsent and the
                next pass tries again.
      14:49:26  outbox done: outboxFiles=37 sent=0 unsent=1 alreadySent=36
                sendFailed=1

  The file is 5538 bytes against Telegram's 4096-character text limit. NOTHING
  ANYWHERE MEASURES THAT. `producer-check` enforces banned, linkfloor, linkcap,
  linkdest, options and deadline, and names the five it does not enforce
  (wordcap, shape, nextvisible, split, reading). SENDABILITY IS NOT ON EITHER
  LIST, so it is not a known gap being carried; it is a gap nobody had thought
  of. `tools/runner/telegram-bot.py` has no length constant and no splitting:
  it posts, Telegram refuses, and the sweep retries on the next pass FOREVER.

  THE CAUSE IS STRUCTURAL AND NAMING IT IS THE POINT. The `answer` register is
  the only one with NO word cap, by a deliberate ruling that his question sets
  the length. So the one register that cannot be too long by construction is
  the one register that can be too long in fact, and the cap that would have
  caught it was removed on purpose and correctly. This is not an argument for
  a word cap on answers. It is an argument for a BYTE check, which is a
  different quantity from a word count and is the one the transport actually
  applies.

  THE DENOMINATOR, because a first occurrence is not a rate: 1 of 36 outbox
  messages exceeds 4096 bytes, and it is today's. Every earlier message was
  under the limit, which is why this has never fired and why nobody knew.

  AND THE RETRY IS THE SECOND HALF OF THE FAULT. An unsendable file is not
  quarantined. `production/outbox/2026-09-03-batch-landed-and-the-wait.
  unprompted.md` has been refused on hundreds of recorded passes for unrelated
  register reasons, so "the next pass tries again" is a loop, not a recovery,
  and a permanently unsendable message is indistinguishable in the log from
  one that is about to succeed.
acceptance: producer-check refuses a message that cannot be sent, with the
  byte count and the limit printed beside each other, and the limit is read
  from ONE constant that the bot also reads so the two cannot drift apart (one
  idea, one implementation); a planted over-length fixture is refused and a
  planted just-under fixture passes, accepting case first; and the sweep
  reports a permanently unsendable file as such rather than as a pending retry
max_sessions: 1
status: READY 2026-09-16, found by reading the PC's sweep log rather than by
  trusting the checker. FILED AND NOT STARTED, under Jafar's standing rule of
  today: an audit finding is filed and the standing order resumes.

  THE IMMEDIATE INSTANCE IS BEING HANDLED SEPARATELY and is not this item: the
  card is split into two parts on the existing `-part1`/`-part2` precedent
  (`2026-09-14-research-1of5-kcd2-part1.answer.md`, 3856 bytes, and its part2
  at 2620). This item is the reason it will not happen again.

  WHAT THIS ITEM DOES NOT CLAIM. It does not say the message was too long to
  be useful; the register has no word cap here on purpose. It says the checker
  cleared a message the transport cannot carry, which is a checker that
  measures everything about a message except whether it can be delivered.

  ONE HONEST UNCERTAINTY, recorded rather than guessed: Telegram's limit is
  4096 CHARACTERS and the number measured here is BYTES. For this message the
  two are close enough that the refusal is explained either way, but they are
  not the same quantity and a bound set from the wrong one would be a
  threshold set without a series. Whoever takes this reads which one the
  transport applies before choosing the constant.
