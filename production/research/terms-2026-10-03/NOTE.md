# The terms LEDGER rests on, read from his PC (3 October 2026, P14)

Jafar's order of 3 October (P14): "read the Unreal, MetaHuman, Mixamo, Steam and Fab terms from this PC and correct the records." Every cloud session had been refused these hosts, so the records leaned on search summaries (production/research/pre-production, SUMMARY.md, "What could not be verified").

**How it was read.** Each page was opened in the browser on this PC between 15:54 and 16:03 on 3 October 2026, and the clauses below were found in its text. The Unreal licence's full text is kept as fetched at F:/LedgerTools/terms-2026-10-03/unreal-eula.txt (on the PC, not in this public repository). The others are recorded here by section, in our words.

## What each says

| source | read at | dated on the page | what bears on LEDGER |
|---|---|---|---|
| Unreal Engine EULA | unrealengine.com/eula/unreal | (no date on the page) | **6(e).** The engine may not be used as a training input to a generative AI, nor as prompt input to one that trains on its input. MetaHuman characters, their animation curves and output made to replicate them may not be used to build or enhance a database, or to train or test an AI. **18.** This licence replaces the old MetaHuman Creator EULA. |
| Epic Content License Agreement | unrealengine.com/eula/content | (no date) | **5(c)(viii) and 17.** Content tagged "NoAI" may not be used in datasets for generative AI, in building it, or **as inputs** to it. **The MetaHuman Content Addendum, 1.** MetaHuman content is Unreal-only: used and shared only with Unreal Engine. There is no other AI clause in the addendum. |
| Fab EULA (the Standard License) | fab.com/eula | Last updated 1 October 2024 | **6, General Restrictions (vii), and 16(l).** NoAI content (tagged at the time of acquiring it) may not be used in datasets used by generative AI, in developing generative AI, or **as training inputs** to it. Programs that only operate on the original content, tag it, or arrange existing content without creating new content are outside that definition. Fab's wording is narrower than Epic's content licence ("training inputs", not "inputs"). |
| Mixamo FAQ (Adobe) | helpx.adobe.com/creative-cloud/faq/mixamo-faq.html | Last updated 14 September 2021 | Characters and animations are royalty-free for personal, commercial and non-profit projects, video games named. |
| Adobe General Terms of Use (govern Mixamo) | adobe.com/legal/terms.html | Published and effective 3 October 2025 | **17(C).** Nothing from Adobe's services or software, or derived from them, may be used to create, train, test or improve an AI or machine-learning system. A training clause. |
| Steamworks: Content Survey | partner.steamgames.com/doc/gettingstarted/contentsurvey | (no date) | **Pre-generated** AI content shipped with the game is judged like any other content. **Live-generated** content must also describe its guardrails against illegal content. A live AI service's running costs are the developer's to manage for the player: in the price, as microtransactions, as a subscription or as DLC. |
| Anthropic Commercial Terms | anthropic.com/legal/commercial-terms | Effective 17 June 2025 | **B.** The customer keeps its inputs and owns its outputs, and Anthropic may not train models on customer content from the services. **D.4.** No building of a competing product or training of competing models. |
| Chatterbox Nano weights | huggingface.co/ResembleAI/chatterbox-nano | (card) | **MIT.** The files match ours one for one (F:/LedgerTools/voice-portable/nano/weights); the code in nano/src-master is MIT, Resemble AI 2025. |
| PyTorch 2.4.1, torch-directml 0.2.5 | their installed METADATA and LICENSE, read on this PC | | BSD-3 and MIT. |

**"Help improve Claude".** His word, 3 October (answer 6 to the rulings drafts): he is switching it off. Not read from his settings, which this session does not open.

## What it changes

- **His NoAI ruling stands as his.** It goes further than Fab's own licence:
  - The ruling forbids any use of NoAI-marked items with AI.
  - Fab forbids them only in training data, in building an AI, and as training inputs.
  - Epic's content licence forbids them "as inputs" to an AI, and our AI tester and reviewers send pictures of the game to one. So a NoAI item in frame would breach that licence where it governs the item.

  This is his to know: Needs you 2.
- **MetaHuman is Unreal-only.** The allowlist's entry 3 said it was "usable outside Unreal": corrected. MetaHuman content never goes into a database for an AI, nor trains or tests one.
- **The Game Animation Sample** was still admitted by the allowlist's entry 8: corrected to his NoAI ruling.
- **Mixamo, Unreal and Adobe's clauses are about training,** which his answer 6 lets pass while nothing we send trains a model. The game's talk goes through Anthropic's commercial terms, which forbid training on it.
- **The Steam text** said talk goes "through LEDGER's own server". That server (ledger/Relay) is built but not hosted, so the claim is marked untrue until it is. "Every line is checked before you hear it" is true since P3 (3 October), in the finished game, under a spending cap too.
- **Corrected:** the pre-production review's audit row (1-AUDIT.md, 8) quoted the Fab licence as barring content "as inputs to generative AI programs" from a search summary. That wording is Epic's content licence; Fab's says "training inputs".
