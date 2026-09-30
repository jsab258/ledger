# Cutting the time to a character's first words (research note, 30 September 2026)

Asked for the town's list, item 3 (the text half of the delay) and the
builder's delay note, steps 5 and 6: a research helper was given the problem
(words 1.9 s after Enter on the real path, the pipeline as it is) and no
theory, capped at about thirty minutes. It took two measurements of its own
from this PC that cost nothing (unauthenticated requests, answered 401):
marked MEASURED HERE. Numbers marked estimate are its own, not measured on the
real path. It changed no files.

## Headlines

- The voice alone takes 3.7 s today, so the 2 s target is a voice question
  first; the text side's biggest win is taking the check off the heard path,
  not making it faster.
- The check is probably about half of today's 1.9 s (estimate: the reply's
  first token about 0.6 s, its first sentence 0.2 to 0.3 s, the check's first
  token 0.5 to 0.6 s, the check's JSON 0.3 to 0.7 s, cold connections 0 to
  0.3 s).
- **Prompt caching does nothing for Haiku 4.5 at our sizes** (its minimum is
  4,096 tokens; our Haiku prompts are about 3,200 to 3,600; a marker on a
  shorter prompt is silently ignored). Sonnet 5 caches from 1,024; Sonnet 5.5
  from 512.
- **Sonnet 5 thinks by default** ("adaptive", effort high) when a request
  sends no thinking setting, which would delay the one character on it
  (Sheila) unless the request sends thinking disabled. (Thinking docs, read
  30 Sep 2026.) To be measured: 30 September's nine Sonnet calls wrote 369
  output tokens in all, which suggests little thinking on those turns.
- **.NET 8 drops an idle connection after 60 s; the API's edge keeps it about
  400 s** (MEASURED HERE: reused at 90, 200, 330, 390 s; closed at 420, 480 s).
  Turns more than a minute apart probably open a fresh connection: cold
  166 to 302 ms in .NET against about 130 ms warm (MEASURED HERE). The host
  negotiates HTTP/2 from .NET 8.

## The method, as professionals run it

1. Time every stage on the real path, median and 95th percentile.
2. Give each stage a budget (Daily's voice-to-voice budget: the model's first
   byte 650 ms, sentence aggregation 20 ms, the voice's first byte 120 ms;
   https://voiceaiandvoiceagents.com/, Feb 2025, updated June 2026).
3. Stream each stage into the next at the smallest useful unit.
4. Keep slow checks off the critical path: (a) check a chunk, release it
   (AWS Bedrock's default, NeMo's stream_first=False); (b) run the check beside
   the main work and gate only the release (OpenAI cookbook); (c) speculative
   work thrown away on failure (LiveKit's preemptive speech; RelayS2S,
   arXiv 2603.23346, 24 Mar 2026, cut first-chunk latency by 479 ms);
   (d) show first and retract later, not acceptable for LEDGER's gate.
5. Hide what is left with an instant response (a filler or a beat).
6. Only then tune the model, the prompt size, caching and connections.

For LEDGER: when the first sentence is complete, start its check and its
voice at the same moment; play it only on a pass (the talk program's
--pending, already built; the builder wires the voice side).

## Ranked by likely time saved (estimates until measured on the real path)

1. The voice made beside the check, played only on a pass: about 0.8 to
   1.2 s, all of the check's time. $0.
2. No model check when the sentence states nothing checkable (check-
   worthiness detection, CLEF CheckThat! since 2018): about 0.8 to 1.2 s on
   those turns; saves money. Replay logged sentences through today's checker
   first to measure how often it would skip one the checker would fail.
3. Sonnet 5: send thinking disabled (on Sonnet 5.5 "disabled" is refused).
   Unmeasured; saves thinking tokens.
4. The check's answer verdict first, item numbers only, streamed: about 0.3
   to 0.6 s (Haiku writes about 83 tokens a second; Anthropic's reduce-latency
   guide). Changes the checker, so its bench reruns.
5. Warm connections (pool idle time about 6 minutes, HTTP/2 so the reply and
   the check share one connection, a free keep-alive such as listing models
   every few minutes or on approach): about 0.04 to 0.17 s per cold request.
6. A short first sentence (about eight words or fewer): 0.1 to 0.3 s.
7. Caching plus a pre-warm (max_tokens 0), Sonnet 5 only: about 0.05 to
   0.2 s, unproven at this size (Anthropic's own example is 1.6 s to 1.1 s at
   10,000 tokens; "Don't Break the Cache", arXiv 2601.06007, Jan 2026: 13 to
   31% better first tokens, and 10 to 18% worse below the threshold).
8. Trimming the prompts: small at 3,500 tokens.

Not useful: fast mode (Opus only, output speed not first token, $8/$40);
starting to write while the player types (wasted calls cost money).

## Measured speeds (Artificial Analysis, Anthropic API, 10k-token input, read 30 Sep 2026)

- Haiku 4.5, no thinking: 0.62 s to first token, 83 tokens a second
  (Daily's June 2026 table: median 637 ms, 95th percentile 1,615 ms).
- Sonnet 5, no thinking: 1.06 s to first token, 58.6 tokens a second.

## Sources (read 30 September 2026 unless dated)

- Prompt caching: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Pricing: https://platform.claude.com/docs/en/about-claude/pricing
- Models overview, Sonnet 5 and Haiku 4.5 pages, deprecations: https://platform.claude.com/docs/en/about-claude/models/overview
- Thinking: https://platform.claude.com/docs/en/build-with-claude/thinking
- Reduce latency: https://platform.claude.com/docs/en/test-and-evaluate/strengthen-guardrails/reduce-latency
- Structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs
- Anthropic, prompt caching post (dated 14 Aug 2025 as fetched): https://claude.com/blog/prompt-caching
- "Don't Break the Cache": https://arxiv.org/html/2601.06007v2 (Jan 2026)
- Artificial Analysis: https://artificialanalysis.ai/models/claude-4-5-haiku and https://artificialanalysis.ai/models/claude-sonnet-5-non-reasoning
- Voice agent latency playbook: https://huggingface.co/blog/dvalle08/voice-agent-latency-playbook (15 Mar 2026)
- LiveKit turn tuning: https://docs.livekit.io/agents/logic/turns/tuning/
- RelayS2S: https://arxiv.org/abs/2603.23346 (24 Mar 2026, v2 9 Sep 2026)
- NeMo Guardrails streaming: https://developer.nvidia.com/blog/stream-smarter-and-safer-learn-how-nvidia-nemo-guardrails-enhance-llm-output-streaming/ (23 May 2025)
- AWS Bedrock guardrails streaming: https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-streaming.html
- OpenAI cookbook, guardrails: https://developers.openai.com/cookbook/examples/how_to_use_guardrails
- MiniCheck: https://aclanthology.org/2024.emnlp-main.499/ (EMNLP 2024)
- .NET PooledConnectionIdleTimeout (updated 13 Aug 2026): https://learn.microsoft.com/en-us/dotnet/api/system.net.http.socketshttphandler.pooledconnectionidletimeout
- .NET HttpClient guidelines (updated 6 Aug 2026): https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines
- Cloudflare connection limits (updated 23 Jul 2026): https://developers.cloudflare.com/fundamentals/reference/connection-limits/
