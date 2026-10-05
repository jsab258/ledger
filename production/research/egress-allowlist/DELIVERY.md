# What this container can and cannot reach, and what it cost

Research record, filed on request 2026-09-18 on branch
`research/egress-allowlist` from `a305518b`.

Nothing in it is an instruction. It is evidence and a recommendation Jafar
decides on. It was asked for as the evidence behind a network allowlist
change, so the first job of this file is to be checkable rather than
persuasive: every number below can be re-derived by running the script beside
it.

## What is in this folder

| file | what it is |
|---|---|
| `egress-probe.sh` | the instrument. `--probe`, `--extract`, `--reason`, `--selftest` |
| `hosts-probed.txt` | the curated list: the hosts this lane actually needed |
| `hosts-cited-census.txt` | the census: all 320 hosts cited anywhere, by count |
| `probe-2026-09-18.txt` | today's reading, 32 hosts |
| `proxy-reason-2026-09-18.txt` | the proxy's own account of why, verbatim |

## 1. THE MECHANISM, MEASURED TODAY

There is one refusal and it is the same for every blocked host. From
`curl -sS "$HTTPS_PROXY/__agentproxy/status"`, verbatim:

```
kind:   connect_rejected
detail: gateway answered 403 to CONNECT (policy denial or upstream failure)
```

That is why thirty-eight topics of deliveries report `000` and never a status
code. **`000` is not a zero, it is the absence of an answer.** curl prints it
when the transport never produced an HTTP response at all: the CONNECT is
rejected before any request is sent, so there is no origin status to report.
A reader taking `000` as "the site was down" would be wrong, and a reader
taking it as "refused" is right only because the proxy log says so
separately. The probe alone cannot tell those apart, and the script says so
in its own header.

**Denominator.** 32 hosts examined today: 2 answered 2xx, 28 answered 000,
2 answered a 4xx. 20 of the 28 are in the proxy's failure log with the reason
above; the other 8 were probed before that log was read and the proxy keeps
RECENT failures only, so their reason is inferred from the identical
behaviour rather than recorded. Said out loud because "20 of 28 have a
recorded reason" and "28 have a reason" are different facts.

## 2. TWO EXCEPTIONS, NEITHER OF WHICH AN ALLOWLIST CHANGE WOULD FIX

**(a) The package registries are not allowlisted, they BYPASS the proxy.**
`noProxy` carries `pypi.org`, `files.pythonhosted.org`, `registry.npmjs.org`,
`jsr.io`, `npm.jsr.io`, `index.crates.io`, `proxy.golang.org`, the Anthropic
API hosts and the private ranges. Nothing else.

This is worth knowing because it is how topic 32 got its strongest evidence.
The Blender 4.5 API surface came from `fake-bpy-module-4.5` on PyPI, not from
`docs.blender.org`, which is refused. That was a narrow accident of which
package happened to exist. It answered one question and will not answer the
next, and it should NOT be read as "we have a documentation route".

**(b) GitHub is refused by a different layer, with a different fix.**
`github.com` and `api.github.com` return `HTTP/1.1 200 Connection
Established` and THEN a 403 whose body reads:

> `{"message":"GitHub access to this repository is not enabled for this
> session. Use add_repo to request access. ..."}`

So the CONNECT succeeded. That 403 is the session's repository scoping, not
the network allowlist, and adding `github.com` to a network allowlist would
not change it. `raw.githubusercontent.com` is fully open and serves file
content: 200 on a real path.

**An instrument fault I made and then fixed, recorded because the next reader
would repeat it.** My first sweep probed bare hosts (`https://host/`) and
filed `raw.githubusercontent.com` under "other code: 400". The origin answers
400 to `/` and 200 to a file path. A fully reachable host read as refused,
from a probe that was measuring the wrong URL. `hosts-probed.txt` now carries
an optional path per host and `egress-probe.sh` documents why.

## 3. THE LIST, IN TIERS

Counts are citations across the research lane, from
`hosts-cited-census.txt`. Every row below reads `000 / connect_rejected /
gateway 403` unless stated.

### Tier 1: the hosts that turned findings into guesses

| host | cites | what it would have answered |
|---|---|---|
| `dev.epicgames.com` | 50 | Unreal documentation. The Lumen performance guide, the Animation Budget Allocator, MetaHumans-on-Fab licensing, Interchange and skeletal mesh import. Topics 17, 27, 31 and 32 all rest on pages here. |
| `docs.blender.org` | - | The Blender manual. Whether Decimate preserves vertex groups and what `data_transfer` does at runtime: topic 32's RUNTIME-HOLE 3, still open. |
| `huggingface.co` | 27 | Model cards and WEIGHTS LICENCES. The licence allowlist is law in this project and not one weights licence was read at source: Chatterbox, Kokoro, Z-Image-Turbo, TRELLIS. |
| `arxiv.org` | 41 | Papers in full. Every inference-economics, markerless-mocap and agent-architecture number quoted in this lane is an abstract or a summary of one. |
| `datashare.ed.ac.uk` | 24 | VCTK and its consent provenance. The project's voice rule requires contributors to have donated their voices to build speech technology, and the donation terms were unreadable. |
| `forums.unrealengine.com`, `www.unrealengine.com`, `docs.unrealengine.com` | 67 | Practitioner reports and the older documentation tree. |

### Tier 2: period and legal research, where a summary is not good enough

| host | cites | what it would have answered |
|---|---|---|
| `www.legislation.gov.uk` | 14 | Primary statute with in-force dates: PACE 1984, CJPOA 1994 s34, Dock Work Act 1989, the PPE at Work Regulations 1992 (SI 1991/2687). Cited URLs are in the census. |
| `hansard.parliament.uk` | 11 | Dissolution of the National Dock Labour Board, 1989-05-24. West Midlands Serious Crime Squad, 1989-01-25. Both sit inside the 1988 to 1992 window and both bear on Meridian's premise. |
| `www.gov.uk`, `www.college.police.uk`, `policing.uk` | 8 | Police procedure across the pre-reform window, topic 29. |
| `www.brh.org.uk` | 10 | Bristol Radical History Group on the Dock Labour Scheme, already cited by `production/art/atlas-02/research/adult-clothing-by-occupation.md`. |
| `www.kodak.com` | 9 | Film stock data sheets for the 1990-on-film-stock topic. |

### Tier 3: licence and vendor terms, currently unsourceable

`www.fab.com`, `quixel.com`, `www.meshy.ai`, `tripo3d.ai`,
`store.steampowered.com` (its generative-AI disclosure policy, which the
allowlist's PROCESS section 3 names as a ship-prep requirement),
`developer.nvidia.com` (Audio2Face). **Every price and every licence clause
in this lane's buy-versus-build comparisons is a hole**, and topic 31 refused
to invent one.

### Tier 4: literature indexes

`link.springer.com`, `ieeexplore.ieee.org`, `www.sciencedirect.com`,
`pmc.ncbi.nlm.nih.gov`, `www.nature.com`, `psycnet.apa.org`. Eyewitness
testimony, memory and agent-simulation topics.

### The most-cited host of all, and it is not a primary source

`en.wikipedia.org`, 155 citations, more than any other host by 58. It carries
the donkey jacket construction, the period background and a great deal of the
general framing, all of it through search summaries. It is doing more work in
these deliveries than anything else, and it is the weakest thing holding any
of them up.

## 4. WHAT NOT TO ADD

Roughly 250 of the 320 in the census are aggregators, content farms and
SEO pages that surfaced in search results and were never fetched:
`localaimaster.com`, `evezone.evetech.co.za`, `runaihome.com`,
`discover.oreateai.com`, `vrealmatic.com` and similar. Opening them widens
the surface and improves nothing. **If a finding rests only on one of those,
the fix is to delete the finding, not to reach the page.**

Said plainly because the census file exists in this folder and a list of 320
hosts sitting beside an allowlist request could be read as the request. It is
not. The request is `hosts-probed.txt`.

## 5. WHICH EXISTING FINDINGS BECOME FAULTS

Jafar's rule, stated with the request: from the change onward, a delivery
resting on a page that could not be read is a fault rather than a caveat.
Accepted. Under it, these are the four that would need re-doing first, and
they are named now rather than discovered later:

1. **Every weights licence in the allowlist work.** The allowlist is law and
   none of its entries was verified at source. This is the most serious of
   the four because the consequence is legal rather than aesthetic.
2. **The VCTK consent provenance**, for the same reason: the voice rule is a
   consent rule and the consent terms were not read.
3. **Every Unreal performance number in topics 17 and 27.** Both reason about
   Lumen, Nanite and animation budget from summaries of Epic's own guides.
4. **Every price in the buy-versus-build comparisons**, topics on asset packs
   and clothing. Currently there are none, which is honest but not useful.

## 6. METHOD, AND HOW TO RE-DERIVE ALL OF IT

```
bash production/research/egress-allowlist/egress-probe.sh --selftest
bash production/research/egress-allowlist/egress-probe.sh --probe
bash production/research/egress-allowlist/egress-probe.sh --reason
bash production/research/egress-allowlist/egress-probe.sh --extract
```

`--selftest` runs both outcomes with the ACCEPTING CASE FIRST, per CLAUDE.md
rule 5b: a host on the noProxy bypass must answer 200 and a host that cannot
exist must answer 000. Run today: 2 checks, 0 failed. Without the accepting
half, a probe that reported 000 for every host including a reachable one
would look exactly like a correct measurement of a closed network, which is
the silent-instrument failure this project keeps finding.

`--extract` re-derives the census from the branches and prints its own
denominators: branches examined, delivery files read, distinct hosts.

## 7. HOLES

- **The proxy keeps RECENT failures only.** There is no record of the refusals
  from the earlier thirty-seven topics, so the reason string is measured for
  this session's 20 attempts and inferred for everything before it. The
  earlier deliveries recorded status codes, not reasons.
- **I did not try 320 hosts.** The curated list is 32 and the census is 320;
  most of the census arrived inside search summaries and was never fetched.
  So "tried and refused" is 32, and "cited without reading" is the rest. The
  brief asked for hosts tried and refused, and the tiers above are the
  honest answer to it, with the census attached for completeness rather than
  as part of the request.
- **Whether a host answers after being allowlisted is not something this
  record can promise.** `connect_rejected` is a gateway policy denial OR an
  upstream failure, in the proxy's own words, and the two are not
  distinguished in the string. A host added to the allowlist that still
  fails would be the second case, and only a run would tell.
- **`store.steampowered.com` and the disclosure requirement.** The allowlist's
  PROCESS section names a Steam generative-AI disclosure at ship-prep. That
  page has never been read here, so what the disclosure actually requires is
  unknown, not merely unrecorded.
