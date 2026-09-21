# BRIEF: does graphify solve our finding problem, or the half it does worst

STATUS: BRIEF. Written 2026-09-19, before any research began, per the standing
instruction that a topic's brief is a file in the topic's folder, in Jafar's
words.

This is a tool evaluation rather than a game topic.

## The problem it might solve, in his words

> This repository is large and half of it is documents rather than code:
> forty-seven research deliveries across forty-seven branches, a decision
> register, a queue of three hundred items, canon, the stages, the ladder, two
> inventories. Sessions spend real budget grepping to find things, and things
> get lost: an instruction landed in a commit and became nothing, a queue item
> was archived by accident four times, and a finding in one delivery was
> overturned by another with nobody noticing for a week. That is the problem,
> and I want to know whether this tool addresses it.

## The tool

> The tool is graphify, at github.com/Graphify-Labs/graphify, a skill for Claude
> Code that parses a repository into a queryable knowledge graph. Code is parsed
> locally with tree-sitter and no model calls; documents, PDFs and images go
> through a semantic pass that does use a model. It exposes query, path and
> explain commands, and an MCP server.

## This is an evaluation on evidence, not a trial

> Note first that you cannot install it, because your boundaries forbid writing
> outside your topic folder and it writes graphify-out and a skill file.

## What to establish

> Read its documentation and its own repository: what it actually produces, what
> the semantic pass over documents costs in model calls, whether markdown of our
> kind maps usefully or only code does, and what its benchmarks measure. Find
> what other people report, including the ones who tried it and stopped, and
> separate marketing from experience.

## The part that matters

> Then the part that matters: judge it against our shape rather than in general.
> Our problem is finding things across many markdown files and many branches,
> not understanding a call graph. Say whether a tool built for code intelligence
> helps with that or whether we would be using it for the half it does worst.
> Say what it would cost us per rebuild given that our documents change daily.
> And say what could go wrong that the README does not mention.

## The required ending

> End with a recommendation in one of three forms: not worth trying, worth Jafar
> trying on his PC in an evening with these exact commands, or worth the studio
> adopting with this exact scope. If the second, say precisely what he should
> look at in the output to decide, since an impressive graph is not the same as
> a useful one.

## The constraint that bears on the answer

> One constraint that bears on the answer: the project has a standing rule that
> no new instrument is adopted this month unless an existing one is retired in
> the same batch, because a week was lost to instruments that enforced nothing.
> So the recommendation has to name what this would replace, or argue why it is
> an exception.

## Standing constraints

- Claim labels CITED, DERIVED, ASSUMED and HOLE.
- Marketing and experience are separated explicitly, as the commission requires.
- Where a source is a search summary rather than a page read in full, it says
  so. Egress is re-measured in the delivery rather than recalled.
- A null result is a valid delivery and ships with its denominator.
- Nothing in the delivery is an instruction.
