# Which websites I was refused, and what it cost

One page. The long version is DELIVERY.md in this folder, and the script that
produced every number is beside it.

## One reason, for all of them

The gateway refuses the connection before a page is ever requested. Its own
words: "gateway answered 403 to CONNECT". That is why thirty-eight topics of
research all reported the same nothing: there is no error from the website,
because the website was never reached. A door that does not open, not a shop
that is shut.

## The list is about thirty sites, not three hundred

My deliveries mention 320 different websites. I did not try 320. Most of
those names arrived inside search-engine results and I never went near them,
and a lot of them are the sort of low-quality aggregator page that a search
throws up. Opening those would add risk and change nothing.

The list worth acting on is about thirty. Five of them carry most of the
damage:

**Epic's Unreal documentation.** Fifty citations. Everything I have written
about how Unreal performs, what MetaHuman's licence allows, and how it
imports characters comes from summaries of pages I could not open.

**Blender's manual.** The question left open yesterday, whether our
level-of-detail step damages clothing, is answered on a page there.

**Hugging Face.** This is the one I would fix first. Our licence rules are
law in this project, and I have never once read an actual licence at source.
Every entry on the list is there because a search result said so.

**arXiv.** Forty-one citations. Every research paper I have quoted, I have
quoted the abstract of.

**Edinburgh's data archive.** Our rule on voices is a consent rule: only
voices whose owners donated them. The donation terms live there and I could
not read them.

After those: the UK statute site and Hansard, for the police and dockyard
research, which are the kind of thing where a summary genuinely is not good
enough; and the vendor pages for the 3D tools, which is why every price in my
buy-or-build comparisons is currently blank.

## Two things that look like this problem and are not

**GitHub.** It refuses me, but for a different reason: it says the repository
is not enabled for this session. That is a repository permission, not a
network one, so opening the network would not fix it. Its file-download
address, separately, has always worked.

**The Python package site was never blocked.** It sits on a bypass list along
with a few other software registries. That is how I read Blender's command
list yesterday: not because Blender was open, but because somebody had
packaged it. That was luck and I would not count on it again.

## What I got wrong and fixed

My first sweep asked each site for its front page. One address answers an
error to its front page and works perfectly for files, so my own measurement
filed a site I can reach as one I cannot. Corrected, and written down in the
script so the next person does not repeat it.

## Your new rule

You said that once the sites are open, a delivery resting on a page I could
not read becomes a fault rather than an excuse. Agreed. Four things would
need re-doing under it, and I would rather name them now than have them
found: the licence checks, the voice consent terms, the Unreal performance
numbers, and the missing prices.

One caution, so the change can be judged fairly. The refusal message covers
two different situations and does not say which: the gateway turning a site
away, or the site itself failing. If something stays broken after you open
it, that is the second kind, and only trying it would tell us.
