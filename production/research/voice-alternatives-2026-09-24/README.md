# Four voices to pick: Aldous, Danny, June and Zlata

Jafar, 24 September: the four voices cast on 14 August without his approval
come from the same VCTK recordings as the rest of the cast, so they are
allowed; they were simply never approved. Not re-cast from the nineteen,
because shared voices would repeat. "Make a listening page with each of the
four beside two or three alternative VCTK speakers of a suitable age and
accent, put its link in FOR-JAFAR.md, and I will pick." No voice is cast
without his yes (CLAUDE.md).

## What is here

- `page.json`: the four characters, each one's current speaker, three
  alternatives, and the line each says on the page. The alternatives are
  VCTK speakers nobody else in the cast uses, picked by sex and accent
  (Southern English and Edinburgh for Aldous's old money; London, Essex and
  Newcastle for Danny; Southern, Yorkshire and North East English for June;
  the oldest free woman (Belfast), the one speaker from continental Europe
  (France) and Manchester for Zlata, who swears in three languages).
  VCTK's speakers are 18 to 38, so none is as old as Aldous (61) or Zlata (43).
- `inventory.py` / `vctk-inventory.json`: every VCTK speaker's sex, accent,
  age and region, read from the corpus's parquet footers and the row groups
  where each speaker begins, without touching the audio. The first version
  streamed all the metadata and timed out after fifteen minutes.
- `fetch.py`: the first dozen recordings of each of the sixteen speakers,
  about 15 MB of corpus each, saved OUTSIDE the repository.
- `prepare.py`: per speaker, their own reading of the one sentence every
  speaker reads, and a ten-second reference to clone from. The current
  voices clone from their cast clips in `game-design/picked-clips`, as the
  game does.
- `render.py`: each character's line in each voice, by Nano (the small
  Chatterbox) ON THE PROCESSOR: on the card, learning a new voice aborted
  the process in the voice encoder (DirectML has no complex numbers).
- `build_page.py`: the page itself, from the two JSON files.

The audio is not committed: it is VCTK's (CC BY 4.0, attributed on the page)
and is rebuilt by running the scripts in order. The page's link is in
FOR-JAFAR.md.
