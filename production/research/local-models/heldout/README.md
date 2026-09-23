# The held-out router test, frozen 2026-09-23

FROZEN BEFORE ANY ROUTE WAS TUNED ON IT. Nothing here may be edited to suit a
result, used as a worked example, or used as training data. A new version is
a new folder.

- `moments.json`: 30 moments from the game's own verb catalogue and cast. The
  content rule holds throughout: no drink, betting or children.
- `lines.json`: 299 lines, one right answer each. 139 talk, 59 oblique verb,
  35 novel, 25 plain verb, 25 "verb's words, not the verb", 16 argument.
- `commands.json`: 39 lines that give the router orders or make false claims
  in words the game's guard does not catch. The right answer to every one is
  speech. The guard let all of them through (0 of 45 first drafts caught).
- `cut.json`: the one line cut because a labeller found it ambiguous.

How it was made. Three writers each wrote ten lines for each of ten moments to
a fixed mix, and a fourth wrote the command lines against the guard's own
regexes. All 340 lines passed `tools/content-gate.py`'s scan. One duplicate
was dropped. Two labellers then labelled all 339 blind, one of them a smaller
model. A line was kept only when the writer's answer and both labels agreed
exactly, verb and argument included: 338 of 339.

What it is not. Every writer and labeller was a Claude model. That makes it a
test set, which is allowed. It is NEVER training data (Anthropic's Usage
Policy; DECISIONS 2026-09-23). The labels are Claude's consensus, not a
person's. Three Claude instances agreeing is weaker evidence than it looks,
because they share their blind spots. A person reading a sample of the lines
is the check that would catch that.

Run it:

    dotnet run -c Release --project ledger/RouterFloor -- --url http://127.0.0.1:8090 --set heldout --moments production/research/local-models/heldout/moments.json --lines production/research/local-models/heldout/lines.json --modes prompt
