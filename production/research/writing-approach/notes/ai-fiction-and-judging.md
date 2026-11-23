# AI fiction failures, fixes, and how sound an AI judge is

Research dated 2026-11-23. Everything below comes from pages actually fetched (listed at the end). Where a fetch gave only an abstract, the note says so. Not reached: Re3 paper, Dramatron full text, Vonnegut arc studies, EQ-Bench long-form write-up, any game-studio post-mortem, the Riedl group's own narrative papers beyond one co-author-free planning paper. Those gaps are named in the last section.

## Failure patterns with evidence

**Weaker than professionals, on a structured test.** Chakrabarty, Laban, Agarwal, Muresan and Wu (Torrance Test of Creative Writing, TTCW, 14 binary tests, 10 creative writers judging 48 stories) found LLM stories passed 3 to 10 times fewer tests than professional stories (arXiv 2309.14556v3, March 2024). Abstract only was read.

**Sameness across samples.** This is the best-measured failure.
- Hamburg study (Thennal and Hatzel, v2 September 2026): 10 LLMs against human writers on r/WritingPrompts, 44 prompts. Human self-similarity about 30%; LLM self-similarity mostly 80 to 90%. Only 9.2 to 16.8% of LLM stories were judged closer to a human story than to another LLM story. Frontier models converge on a generic "mean" narrative. Negative prompting and temperature did little (temperature mattered mainly for one OLMo model, 99.2% down to 76.9% self-similarity as temperature rose from 0.2 to 1.0).
- Xu, Jojic, Rao, Brockett and Dolan, "Echoes in AI" (arXiv 2501.00273v2, August 2025): GPT-4 and LLaMA-3 reuse plot elements across generations of the same prompt; human stories rarely echo each other. Their Sui Generis score correlates only moderately with human ratings of surprise.
- Padmakumar and He (ICLR 2024, v3 July 2024): in argumentative essays, co-writing with the feedback-tuned InstructGPT lowered lexical and content diversity across writers; the base GPT-3 did not. The loss came from the model's suggestions, not the writers' own text. Suggests tuning for quality buys homogeneity. Essays, not fiction, so apply with care.

**Slop phrases.** Paech et al., Antislop (arXiv 2510.15061, October 2025): some model phrases occur over 1,000 times more often than in human text. Chakrabarty, Laban and Wu, "Can AI writing be salvaged?" (arXiv 2409.14509v5, March 2025): professional writers edited 1,057 LLM paragraphs; the edits produced a 7-category taxonomy of idiosyncrasies (cliches and unnecessary exposition named in the abstract; the other five I did not read). GPT-4o, Claude-3.5-Sonnet and Llama-3.1-70b showed no clear winner, so the faults are shared across model families.

**Bland default voice, tropes, passivity to the prompt.** Ippolito, Yuan, Coenen and Burnam (Wordcraft, 13 published writers, 8 weeks, LaMDA, arXiv 2211.05030, November 2022): the tool had a bland default voice, could not keep distinct voices across points of view, fell back on familiar tropes (warrior hero in fantasy even when asked otherwise), defaulted to male voice, and steered a lesbian romance toward a male character or friendship. Writers said the safe output made transgressive writing hard. A repeated "Sarah" came from a bug in the example prompts, a reminder that few-shot examples leak into every output. The model is old; the pattern of blandness matches the later work above.

**Predictable plots and flat designer experience.** Alavi et al. (Microsoft, GamePlot, 14 game designers, GPT-3.5, date not stated): the most common complaint was lack of creativity: predictable output, weak tension, trouble with several simultaneous conflicts, some plot inconsistency. Satisfaction still averaged about 4/5, because designers could edit.

**Loss of coherence over length.** "Lost in Stories" (ConStory-Bench, 2,000 prompts, 5 error categories, 19 subtypes; page gave no date): stories of tens of thousands of words contradict established facts, character traits and world rules. Errors are commonest in factual and temporal matters, cluster around the middle of the text, and rise where token-level entropy is high. No per-model rates were read.

**Weak motive and conflict.** Wang and Kreminski (arXiv 2506.10161, June 2025), narrative-planning tasks checked by a solver, successes out of 30: causal soundness is largely solved at small scale (o1 and Claude-3.7 30/30), but character intentionality (Aladdin task: o1 14/30, Claude-3.7 15/30, GPT-4o 0/30) and dramatic conflict (Western task: o1 20/30, Claude-3.7 6/30, GPT-4o 3/30) are hard. Failed plans were often causally valid but gave characters actions with no motive. This is the planning-level root of passive, motiveless characters.

**Reception of frontier output.** OpenAI's March 2025 metafiction story split critics: Jeanette Winterson called it beautiful and moving in the Guardian; Dave Eggers called it "pastiche garbage that would fool only the most gullible" (eWeek, year inferred as 2025). One anecdote of expert disagreement, not evidence of quality.

Not found in reached sources: direct evidence for moralising, tidy endings, flat humour or sycophantic revision as measured quantities. They are likely in the Chakrabarty taxonomy but I did not read it, so treat them as unverified.

## Fixes that showed results

- **Hierarchical outline plus controller (DOC, Yang, Klein, Peng, Tian, ACL 2023, arXiv 2212.10077).** Against the Re3 baseline, human pairwise wins of 80.8% on coherence, 78.9% on outline relevance, 69.5% on interestingness; stories about 3,500 to 3,900 words; only 20 stories with 3 annotators each. Small sample, short stories, older models.
- **Specialised agents (Agents' Room, Huot et al., Google DeepMind, arXiv 2410.02603v2, March 2025).** Expert evaluators preferred it to baselines; planning, character, setting and writing split between agents. Effect sizes not read. Also introduced a long-narrative evaluation method and the Tell Me A Story dataset.
- **Hierarchical prompt chaining with a human in the loop (Dramatron, Mirowski, Mathewson, Pittman, Evans, arXiv 2209.14958, 2022).** 15 theatre and film professionals co-wrote with it. The fetched text gave only that interviewees were critical and that the authors raise plagiarism and bias; I did not read what playwrights said in detail.
- **Human edits remain better than machine edits.** Chakrabarty et al. 2025: automatic editing methods help, but experts still preferred expert-edited text.
- **Slop removal at the token level.** Antislop: the sampler suppresses over 8,000 patterns (simple token banning breaks at about 2,000); FTPO fine-tuning cuts slop about 90% while keeping or improving benchmarks including creative writing; DPO suppressed less and hurt writing quality and lexical diversity. Authors' own results, MIT licensed. Removing phrases does not fix plot sameness.
- **Diversity: what did not work.** Hamburg study: negative prompting and top-p did little; temperature helped only one model. Padmakumar and He: base models gave less homogenising help than instruction-tuned ones. Practical reading: vary the input (premise, constraints, characters seeded by the author), not the sampling.
- **Writers use the tool for lists, brainstorming, research and "yes, and" improv, not for voice (Wordcraft).** Designers kept ownership because they could edit at every stage (GamePlot: control and ownership 4.5/5). Game developers wanted the AI to do more; narrative writers wanted control.
- **Solver feedback for logic.** Wang and Kreminski: an external checker after each action took GPT-4o from 13/30 to 29/30 on causal soundness, at about 5,000 tokens against about 900 per solve. Checkable facts (continuity, who knows what) are where automation works.

## How sound is an AI judge

**Expert agreement is weak on open creative questions.**
- TTCW: none of the LLM judges tested correlated positively with expert assessments (abstract of 2309.14556v3).
- Tutone, Franceschelli and Musolesi (arXiv 2608.23705, 2026, date not stated): 100 human and 100 AI stories, 11 creativity dimensions. Kendall tau-b between LLM and human scores: only Elaboration above 0.30 (0.31); Creativity 0.23; Surprise 0.01 (p = 0.867); Novelty, Effectiveness, Usefulness not significant. The LLM rated AI stories higher on all 11 dimensions, with perfect 5.00 on Originality, Value and Creativity and no variance. Its Creativity score tracked Elaboration, a surface feature. Standard automatic metrics were near zero against humans.
- LitBench (Fein et al., arXiv 2507.00769, July 2025, Reddit story preference pairs): best off-the-shelf judge Claude-3.7-Sonnet 73% agreement with human preference; trained Bradley-Terry and generative reward models 78%. So pairwise choice on short stories reaches about three in four, not nine in ten.
- LongJudgeBench (Chen et al., arXiv 2606.01629v4, August 2026), creative subset (263 pairs, both orders, median about 2,200 tokens): best vanilla accuracy 0.785 (DeepSeek-V4-Flash), Qwen3-Max 0.724, GLM-5.1 0.752; GPT-4o-mini 0.28 and GPT-5.2 with a rubric 0.20 (below chance, which means consistently picking the wrong one, not noise). Creative writing was among the hardest of six scenarios (mean 0.578). Position inconsistency after swapping order: 78.7% for GPT-4o-mini, 62.0% DeepSeek-V4-Flash, 46.0% GPT-5.2, 17.9% GLM-5.1, 10.6% Kimi-K2.6. Rubrics and references helped but not always.
- Sameness task (Hamburg): human annotators agreed 86%; LLM judge agreed with humans 81%; 92.8% when the judge stated maximum confidence. Comparing two stories for similarity is a far easier, more factual question than ranking quality, and the judge does well there.

**Biases measured.**
- Position: Shi, Ma and Vosoughi (arXiv 2406.07791, June 2024), 9 judges, 22 tasks, about 80,000 instances. Position bias is systematic, not random (repeat consistency up to 0.97 for gpt-4-0613). Positional consistency ranged 0.565 (claude-3-haiku, MTBench) to 0.815 (gpt-4-0613); it is worst when two answers are close in quality, which is exactly the situation in judging two decent stories. Claude models favoured later positions. Judges of one family agree with each other more. Authors argue apparent verbosity and self-enhancement bias partly reflect position bias tied to quality gaps.
- Ye et al. (Justice or Prejudice, arXiv 2410.02736v2, October 2024): 12 biases named (position, verbosity, self-enhancement, authority, bandwagon, sentiment, refinement-aware and others) in 6 judge models; Claude-3.5 was the most resilient; the numbers were in the unread part of the page.
- Self-preference: Tutone et al. (above), the LLM judge systematically favoured AI over human stories.
- Ceiling and low variance: Tutone et al.; also the EQ-Bench author's own list of uncontrolled biases: judge self-bias, positivity or negativity, aversion to NSFW material, stylistic preference, slop bias. He advises reading samples.
- Absolute scoring is unstable: DramaGrow (Zhang and Su, arXiv 2611.09938, 2026, Chinese five-episode drama): absolute-score rubric judges reached only 53.8 to 55.8% preference accuracy and three-call item agreement of 29.8 to 32.5%; direct pairwise comparison reached 85.1% with identical results across three runs. A structured rubric raised false alarms on clean scripts (13.3% against 5.7% unstructured) with no gain in detection. Defects checked against the story spec (continuity, knowledge-boundary slips) were judged reliably; taste was not. Human five-rater panel Fleiss kappa 0.558, so even experts agree only moderately; with 3 of 5 votes, dropping one rater flipped the panel direction 60% of the time.
- Famous-work inflation: I found no study that measured it in the fetched sources. It is plausible and cheap to test, so treat it as an assumption to check, not a finding.

**Plans against finished work.** Nothing reached tests this directly. The nearest evidence: checkable plan properties (causal soundness, motive, continuity) can be verified by solvers or checkers (Wang and Kreminski; ConStory-Checker; DramaGrow verifiable regime), while quality of finished prose is where judges fail. So a judge reading an outline will tend to approve fluent tidy plans; the weakness the writers found was in execution and surprise.

## Practical rules for a sound measure

1. Use pairwise, not absolute scores. Run every pair in both orders and count only pairs where the verdict survives the swap. Treat a split as a tie. (Position studies, LongJudgeBench, DramaGrow.)
2. Repeat calls. Single-call verdicts are unstable (DramaGrow: three-call item agreement near 30% for absolute scores). Take majorities of at least 3 to 5.
3. Ask observable, checkable questions rather than "is this good": contradictions with the established facts, who knows what, does the protagonist's choice cause the turn, count of banned phrases per thousand words, repeated names and openings, ending tied in a bow or a moral stated aloud. Judges do these well; they do taste badly.
4. Keep a calibration set: pairs ranked by real human readers (a handful of the project's own approved and rejected scenes plus published anchors). Measure the judge's agreement before using it; reject any judge below about 75% on the set. Expect 70 to 80% as a good result. Re-run when the judge model changes.
5. Use judges from different model families and take the vote. Same-family judges share biases, and self-preference favours the writer's own family. Never let a model judge its own output alone.
6. Blind and disguise: strip names and labels, and test with famous passages renamed to see whether the judge inflates reputation (untested in my sources, so do it as a small experiment).
7. Compare against anchor texts of known quality, not against nothing; absolute numbers from judges have ceilings (5.00 everywhere) and carry no information.
8. Measure sameness directly, with the cheap comparison the judge does well: sample the same prompt many times and score pairwise similarity, plus entity and name concentration. Models agreed with humans 81% on that.
9. Use solver or script checks for continuity and logic, and an LLM only for what scripts cannot see.
10. Keep humans for taste on narrow points. Experts themselves agree only moderately, so a few stable human readers beat a large pile of judge scores. Read samples; a rising score with unchanged prose is a warning.
11. Do not count a judge praising a plan as evidence the finished scene works. Judge finished text, and judge long text in chunks plus a separate consistency pass.

## Sources reached

Fetched and read (page content seen, abstracts only unless stated):
- Chakrabarty, Laban, Agarwal, Muresan, Wu, Art or Artifice? (v3, 8 March 2024), https://arxiv.org/abs/2309.14556v3 (abstract)
- Padmakumar and He, Does Writing with Language Models Reduce Content Diversity? (v3, 1 July 2024), https://arxiv.org/abs/2309.05196v3
- Huot et al., Agents' Room (v2, 14 March 2025), https://arxiv.org/abs/2410.02603v2
- Mirowski et al., Dramatron paper (29 September 2022), https://arxiv.org/abs/2209.14958v1 (abstract only; playwright comments not read)
- Fein et al., LitBench (1 July 2025), https://arxiv.org/abs/2507.00769v1 (abstract)
- EQ-Bench creative writing bench readme (undated), https://github.com/EQ-bench/creative-writing-bench
- Chakrabarty, Laban, Wu, Can AI writing be salvaged? (v5, 4 March 2025), https://arxiv.org/abs/2409.14509v5
- Paech et al., Antislop (October 2025), https://arxiv.org/abs/2510.15061
- Tutone, Franceschelli, Musolesi, Limits of Automatic Evaluation of Creativity (2026, exact date not stated), https://arxiv.org/pdf/2608.23705
- Xu et al., Echoes in AI (v2, 29 August 2025), https://arxiv.org/abs/2501.00273v2
- Yang et al., DOC (2023), https://arxiv.org/abs/2212.10077
- Thennal and Hatzel, Do LLMs Always Tell The Same Stories? (v2, 2 September 2026), https://arxiv.org/pdf/2606.17350
- Alavi et al., GamePlot (undated, 2024 or later), https://arxiv.org/html/2411.02714v1
- Zhang and Su, DramaGrow (2026), https://arxiv.org/pdf/2611.09938
- Ye et al., Justice or Prejudice? (4 October 2024), https://arxiv.org/html/2410.02736v2 (second half unread)
- Shi, Ma, Vosoughi, Judging the Judges (12 June 2024), https://arxiv.org/html/2406.07791v1 (first third read)
- eWeek on OpenAI metafiction story (year inferred 2025), https://www.eweek.com/news/openai-sam-altman-ai-creative-writing-authors/
- Chen et al., LongJudgeBench (v4, 28 August 2026), https://arxiv.org/pdf/2606.01629
- Ippolito et al., Wordcraft professional writers (9 November 2022), https://arxiv.org/pdf/2211.05030
- Wang and Kreminski, narrative planning (11 June 2025), https://arxiv.org/html/2506.10161v1
- Li et al., Lost in Stories, ConStory-Bench (undated), https://www.microsoft.com/en-us/research/?p=1163845

Seen in search results only, not read, so not used as evidence: Re3, LLMs-as-Judges survey (arXiv 2412.05579), character-name concentration paper (arXiv 2611.01284), TTCW long-form review paper (arXiv 2605.20364), Google games survey (PC Gamer), Wordcraft 2021 paper.

Not covered: Vonnegut emotional-arc work, EQ-Bench long-form details, any studio post-mortem of AI writers, dedicated studies of famous-work inflation, moralising, tidy endings, flat humour, and sycophantic revision.
