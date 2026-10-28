# Live talk research: the written questions (28 October 2026, before any search)

1. inZOI: what Krafton and NVIDIA published about its on-device small language model: size, quantisation, tokens a
   second, latency, what it decides and what it does not; which ACE parts it uses.
2. Where Winds Meet: what NetEase published about its live NPC chat: the models; how characters are kept from creating
   places, items or quests (constraints, retrieval, validation, refusal); latency.
3. Ubisoft's Teammates (Gemini) and NEO NPC: latency figures; guardrails; how lines stay in character and in the
   world's facts.
4. NVIDIA ACE: published latency targets (the owner quotes under 0.8 s) and how they are reached: streaming, small
   on-device models, staged or speculative generation, streamed speech; with numbers.
5. Speed with grounding: a small fast model for the first sentence and a larger for the rest; speculative decoding;
   cascades; constrained decoding and allow-lists of names; retrieval of the speaker's facts: what is published, with
   measured gains.
6. For LEDGER: a bench for "the small model writes the first sentence while the larger writes the rest": which
   Anthropic models by their published ids (read today); how the halves join without contradiction; what to measure
   (first audible word, invented-fact rate by ClaimCheck, wrong refusals); sample size; a cost cap within the $1-a-day
   rule; the pass line.

Our own figures to find first: first-word and whole-reply latencies; the check's cost in time.
