> The brief every helper was given, 7 October 2026.

# Common brief for every helper (read first)

## LEDGER, in short
A third-person PC game (Windows only), set on one street (Quay Street) in a British port town in 1990. Built in Unreal Engine 5.8 with MetaHumans. All implementation is done by AI agents (Claude Code) directed by one person (Jafar), on ONE PC: Ryzen 5 5600X, 32 GB RAM, AMD Radeon RX 6700 with 10 GB (no NVIDIA, no CUDA), shared at run time between the game and an in-game text-to-speech voice (Chatterbox Nano via DirectML today). Almost no money: no hiring, no new subscriptions or purchases without his yes. The work runs on a weekly usage budget of his Claude subscription; live talk in the game uses a paid key capped at about $1 a day for measurement and $5 a friends' evening.
The characters remember what the player does and gossip; the player talks to them live: a language model (Claude Sonnet 5) writes the reply, a second model (Haiku 4.5) checks the reply's factual claims against the simulation before it is spoken, then the local voice speaks it.

## Its hardest open problems
1. Live talk: first sound about 4.6 s after the player's line (best measured 4.0 s locally; a streaming cloud voice would give about 2.4 s because the claim check of the first sentence sets the floor), against a binding 2 s target with no prepared openings. The check alone takes 1-2 s. Characters also answer "that's all I know" too often (about 23-25 of 48 answerable fresh questions on a bench).
2. The look: one street in Unreal 5.8 falls far short of its concept sheet (a photoreal wet overcast British street) and of Kingdom Come Deliverance 2 frames; facades, props, the hillside and night all fall short.
3. Clothing: no tailored garment has passed review; AI tools could not cut a jacket with a proper lapel. Tried: simulated cloth, FreeSewing patterns in Blender, Marvelous Designer drapes, MakeHuman CC0 garments, scripted garments.
4. Animation: natural sitting, standing, turning and idling for MetaHumans, without any NoAI-tagged asset (Epic's Game Animation Sample is excluded); MetaHuman's own clips and Mixamo are allowed.
5. The way of working: one person directing AI agents on one PC on a weekly usage budget.

## Hard rules
- NoAI: anything marked NoAI (Fab's "Allows usage with AI: No", or any licence that bars AI use) is excluded entirely, also as a reference or input. Licences must allow commercial use in a game that will be SOLD. Note non-commercial or research-only licences (e.g. SMPL/SMPL-X, AMASS, many datasets), territory exclusions (some model licences exclude the EU, UK or South Korea; Jafar lives in Switzerland), and output-use clauses.
- Never recommend copying another game's code or assets.

## Your method
- Period of interest: roughly July to October 2026 (today is 7 October 2026). Earlier work only as background, marked as such.
- Do not invent names, versions, dates or numbers. If you cannot verify a model or product named in the brief (e.g. "GPT-6 Astra", "GPT-6.1 Sol"), say so plainly.
- Network: this session can reach (via WebFetch or Bash curl): export.arxiv.org (the arXiv API: e.g. curl -s "https://export.arxiv.org/api/query?search_query=all:%22speech-to-speech%22&sortBy=submittedDate&sortOrder=descending&max_results=25" returns titles, dates, abstracts), en.wikipedia.org, github.com and raw.githubusercontent.com public pages (READMEs, LICENSE files, release pages) via WebFetch or curl, www.anthropic.com, platform.claude.com, dev.epicgames.com (via WebFetch). WebSearch works but gives search summaries only. Most other hosts (openai.com, Google/DeepMind, Hugging Face, Reddit, YouTube, X, games press, legislation sites) are refused: report them UNREACHED. Do NOT use `gh api` or any GitHub MCP tool against repositories other than jsab258/ledger; reading public GitHub pages as web pages is fine.
- Marks for every claim: [SHOWN] = demonstrated with evidence you read: released code or weights you saw the page of, a shipped product, or an experiment reported in a paper you read (note it is the authors' report); [CLAIMED] = only announced or reported (press, posts, a vendor page), nothing you could check; [ABS] = arXiv abstract read via the API (the authors' own claim; say so); [SS] = search summary only, a lead and not evidence; UNREACHED = could not be opened; [I] = your inference.
- For every item give: what it is, who, date, model/tools, what was shown vs claimed, URL, and then the LEDGER angle: which of the five problems (or something new) it could help; whether it could run on THIS PC (AMD RX 6700 10 GB, Windows; say if it needs CUDA/NVIDIA or the cloud); cost; licence for a sold game (commercial use? NoAI? dataset taint? territory?).
- Cap: about 30 minutes. Plain words. No praise. Write your full report to the path given in your task, and return a summary of at most 700 words plus that path.
