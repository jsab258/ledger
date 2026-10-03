# Brief for an asset-plan research helper (LEDGER, 3 October 2026)

You are one of seven research helpers. Read only. Write nothing in the repository; write only your own note, at the path you are given. Work for about thirty minutes, then write the note and stop.

## The problem

LEDGER is a third-person PC game (Windows, Unreal Engine 5.8, MetaHuman characters) set in Meridian, a fictional British port town, in 1990 (canon's window is 1988 to 1992). The visual bar is photoreal, wet, overcast, grimy Britain, judged against two references:
- the Hook sheet (production/reference/hook-sheet.png, described in production/reference/README.md): a full-frame street photograph of Quay Street;
- two frames from Kingdom Come: Deliverance II (production/reference/kcd2-town-*.jpg).

Real period photographs govern what things looked like (production/reference/photographs.md). Where they disagree with the sheet, the photographs win. Photographs are for proportions and period feel; designs are never copied.

**The whole town is built by one person directing AI agents, with almost no money,** on one PC with a Radeon RX 6700.
- The agents drive Blender 4.5 by script (tools/art-recipes/: terrace-front.py builds the street's facades, shop-room.py the shop interiors, car-model.py a placeholder car, lighting-column.py, fascia-cornice-elevation.py).
- They also drive Unreal by script.

## The source rule (the owner's, in this order)

1. **Free and unrestricted assets that fit 1990 Britain and the bar.**
2. **Assets we make ourselves, as kits with variation,** not one-offs.
3. **Human-made inputs** (buying, commissioning, an artist's paid work) **only by the owner's explicit ruling, which today means none.** Clothing quality is a known exception for now.

**Never allowed:**
- **Any asset tagged NoAI**, or whose licence forbids use with AI tools. Epic's and Fab's "NoAI" tag forbids using an asset with AI tools, and our whole pipeline is AI, so NoAI assets are never used, **not even as references**. Two ready-made suits were rejected on 3 October for exactly this.
- **Real brands, logos, products and car models.** canon.md: "Every brand, band, club, product, weapon and vehicle is fictional. No real people, voices, logos, lyrics, car models."
- **Anything breaking canon's content rule:**
  - alcohol and gambling never shown or spoken of (no beer signs, no betting shop, no pools coupons);
  - no children anywhere;
  - tobacco is allowed.
- **Anything out of period:** no wheeled refuse bins, no tactile paving, no mobiles, little uPVC; any 1950s or 1970s framing is wrong.

## The licence allowlist (ledger-v2/research/license-allowlist.md; it is law)

- **Allowed:**
  - CC0 libraries: Poly Haven, ambientCG, Sketchfab's CC0 filter;
  - Fab items under the Fab Standard License, free or paid, but never NoAI;
  - MIT, Apache 2.0 or BSD code and data;
  - MetaHuman: free under US$1M revenue, never to train or enhance AI;
  - Mixamo characters and animations;
  - OFL fonts;
  - Epic's Unreal-only animation content: animation only;
  - public domain [I: treated like CC0].
- **Allowed by recent rulings:** CC-BY, with credit, for voices and garments only.
- **Needs a ruling:** CC-BY for other 3D; marketplaces' own "royalty free" licences; Epic "UE-only" content other than animation.
- **Never:** NonCommercial, NoDerivatives, "personal use only", anything NoAI.

## What is already known: read before searching

Read only what touches your families; do not repeat its searches:
- production/research/aaa-street/: SUMMARY.md, 1-PIPELINE.md, 2-EPIC-FREE-CONTENT.md, 4-VEHICLES-AND-FURNITURE.md, 5-PROOF-FRAME.md.
- production/research/period-vehicles-and-props/NOTE.md.
- production/research/asset-packs/SUMMARY.md and production/research/asset-coverage/SUMMARY.md.
- production/research/street-clutter-1990/, shop-window-interiors/ (including GOODS-2026-10-03.md and FISHMONGER-2026-10-03.md), interior-blockout/, cab-office-interior-1990/.
- production/research/wardrobe-at-scale/, free-garments/, plain-1990-clothes/, casting/, natural-idles/, townspeople-animation/.
- production/specs/fab-free-megascans.md: the free Megascans already in the owner's Fab library.
- The last forty lines of DECISIONS.md, for today's rulings.

## Your note: for EACH family you are given

1. **How professional games make it,** with sources. For example, how GTA makes fictional cars that read as their era without copying real ones.
2. **Free sources without AI restrictions** that fit 1990 Britain and the bar, with links and licences. Give the exact licence name, and whether the listing or library carries a NoAI tag or an AI clause. Mark each [READ], [SS] or UNREACHED (see below). An unreached source is never evidence.
3. **For what we make ourselves, the kit method:**
   - the parts;
   - the variation (seeds, swaps, materials, wear);
   - the tools (Blender, Unreal's PCG and shape grammar, Geometry Nodes, others);
   - how an AI agent drives it by script, and where a human eye must judge.
4. **The reference that sets the bar:** real photographs for proportions and period feel (archives, Historic England, Geograph and similar), with links, never copied designs.
5. **The variety the town needs** (how many distinct kinds and variants, and why), and **the one proof to build before anything is multiplied:** what it is, how it is judged against the Hook sheet and the KCD2 frames, and the rough effort.

Then:
- **Per family, in one line:** what is free, what we make, and what is impossible without a ruling.
- **What I could not reach or verify.**
- **Sources:** numbered, each with its URL, the page's date or "undated", and the date you read it.

## The network and your tools (measured 2 and 3 October)

- **WebSearch works** (US results). **The session's searches are shared and capped at about 200 in all:** use at most about 25, chosen well.
- **WebFetch is blocked** for most hosts: Sketchfab, Fab, CGTrader, ArtStation, Poly Haven, Gumroad, archive.org, most news sites and others. Try a host once and record the result.
- **Reachable on 2 October:**
  - by curl in Bash: github.com and raw.githubusercontent.com, gitlab.com, the npm registry;
  - by WebFetch: dev.epicgames.com (Epic's documentation) and en.wikipedia.org.
- **Marks:**
  - **[READ]** read at the source;
  - **[SS]** search summary only;
  - **[I]** your inference;
  - **UNREACHED** the page refused you.

  Never present a search summary as read, or an unreached page as evidence.

## Style

- Plain English, short sentences, British spelling.
- Tables where they help.
- Be sceptical: "free" may mean free for personal use only, "CC0" in a title may hide another licence field, a "free" Fab item may carry NoAI.
- Do not pad. If a family has nothing free that fits, say so plainly.
