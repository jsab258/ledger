# Common Voice for Darren's reference: the terms read

For his pick of 27 October. Sources read in full 27 October 2026; nothing downloaded; no account opened. Not legal advice.

## Bottom line (after the fresh review, 27 October)

**Not recommended.**
- Pocket's own terms forbid "cloning without explicit and lawful consent" (its model record, read 27 October). Common Voice volunteers were told their voices were for voice recognition apps; none consented to a cloned game character.
- MDC's Appendix 1 limits use to the Data Consumer License's purposes (the dataset page names speech recognition) and bars redistribution. Shipping Pocket's voice file is no way round this: the file is the model's state after reading the clip, a transformed copy of the recording, as THIRD-PARTY.md already treats Chatterbox's.
- VCTK's speakers recorded for a corpus made for a voice-cloning toolkit, which meets Kyutai's bar far better. It is already on the record as a stated risk (his ruling of 24 September).

So Darren's livelier voice needs a recording made with consent to clone it, or he keeps his VCTK voice.

## Questions

1. Distribution, download steps, licence, added terms?
2. Anything from Mozilla on cloning or text-to-speech, sold?
3. An unscripted English set: metadata, size?
4. Fit with the allowlist?
5. Finding a young north-east man without the full download?

## Answers with sources

**1. Where and how.**
- Only through the Mozilla Data Collective (MDC), a UK company spun out of the Mozilla Foundation in April 2026 [3]. Mozilla's Hugging Face pages hold a notice, no data [9]. MDC refuses mirrors so a contributor who withdraws consent can be removed [8].
- A download needs an MDC account (email, or Google, GitHub or LinkedIn), age 18 or over, MDC's terms accepted [4, 16]; then four boxes per dataset: licence, additional conditions, restrictions, forbidden usage [5]. The API needs a key, boxes ticked on the web first [3]. Free.
- Licence: CC0 1.0 [5, 6, 7].
- Added: never try to identify speakers; never re-host or re-share [5]. MDC adds: no tracing contributors, no hosting elsewhere (2.b); respect privacy and publicity rights; model outputs hold no personal data and are disclosed as machine-generated (Appendix 1) [4]. Contributors' terms ask that no part be mirrored elsewhere [1].
- The stated intended use (speech recognition) is not one of the four boxes [5].

**2. Cloning.**
- No Mozilla or MDC term forbids text-to-speech or cloning; none allows it by name [1, 4, 5].
- Contributors were told the purpose is voice recognition apps, under a CC0 dedication [1, 2]. Other site text is broader: commercial speech technology, voice models [12].
- In June 2023 a contributor asked Mozilla to forbid TTS use. After legal review Mozilla closed it: "additional restrictions cannot be added to Creative Commons licenses" [10]. In the thread after, one contributor objected to cloning; another argued for text-to-speech, cloning the real worry [11].
- On an approved removal request, Mozilla says it asks downloaders to remove the recordings [12]. A sold game cannot recall copies.
- Pocket's own terms forbid cloning without explicit, lawful consent [13]. VCTK (a corpus titled for a voice-cloning toolkit) arguably meets that bar; Common Voice ("voice recognition apps") clearly does not.
- MDC Appendix 1 also says the dataset may be used solely for the Data Consumer License's purposes and must not be redistributed [4]. The dataset's stated intended use is speech recognition; the four boxes leave it out, so whether CC0 alone governs is ambiguous (open).
- Common Voice accepts contributors under 19 with a parent's consent, and age is optional and self-declared [1]; any filter must drop speakers with no age given (the no-children rule).

**3. The unscripted set.**
- Common Voice Spontaneous Speech 5.0, English, released 17 September 2026: spoken answers to questions. 519 MB; 5,898 clips; 18.6 hours (8.39 validated); 642 speakers [5].
- Fields: speaker hash, clip, length, question, transcription, votes, age band, gender, quality tags. No accent or region field [5].
- Read speech: Scripted 27.0 English, 95 GB, 100,546 speakers [6]; its British subset (26.0), 7.5 GB, free-text accents: "geordie" 10 clips (0.02 h), "Northern England" 246, "Northern English" 87 [7]. Read, so flat like VCTK.

**5. Finding him.**
- No preview: no sample file, no rows in the public metadata [15], empty Hugging Face pages [9]. Third-party mirrors go against Mozilla's request.
- So: download the spontaneous set whole (0.5 GB) to F:; keep men in their twenties, validated, longest answers; screen with the accent checker; listen. Whether any is north-east, the metadata cannot say. Fallback: the British subset's northern tags, read.
- Not to do: matching speaker hashes across sets to learn an accent; too close to MDC's ban on tracing contributors.

Sources:
[1] https://commonvoice.mozilla.org/terms/en.html (31 Oct 2025)
[2] https://commonvoice.mozilla.org/privacy/en.html
[3] https://mozilladatacollective.com/llms.txt
[4] https://mozilladatacollective.com/terms (6 May 2026)
[5] https://mozilladatacollective.com/datasets/cmu5nqn1h00vwmi07b4dbk085 (and its API record)
[6] https://mozilladatacollective.com/datasets/cmu5jplf300nwmh07iqvk9leo
[7] https://mozilladatacollective.com/datasets/cmrt6zrob000zmm07yqwjlpwi
[8] https://community.mozilladatacollective.com/faq-can-i-get-the-common-voice-or-other-mdc-datasets-from-other-platforms-like-github-or-hugging-face/
[9] https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0
[10] https://github.com/common-voice/common-voice/issues/4068
[11] https://discourse.mozilla.org/t/explicitly-forbidding-limiting-tts-usage/115072
[12] https://github.com/common-voice/common-voice/tree/main/web/locales/common-voice/en/pages (datasets.ftl, profile/delete.ftl)
[13] https://huggingface.co/api/models/kyutai/pocket-tts
[14] pocket_tts/main.py, export_voice (installed copy on F:)
[15] https://mozilladatacollective.com/api/datasets/cmu5nqn1h00vwmi07b4dbk085/metadata
[16] https://mozilladatacollective.com/auth/signup

## Fit with the allowlist

- Copyright: CC0 allows sale and change; no credit needed (credit Common Voice anyway, never a speaker).
- Never-ship 5 spares anonymous volunteers who recorded for speech research under an open licence (his ruling of 24 September). Common Voice speakers fit: no conflict.
- But the accepted consent risk names VCTK only ("VCTK voices, consent a stated risk"): one new line, his.
- The risk is larger than VCTK's: recorded for recognition; contributors objected; removal requests may reach downloaders; MDC's personal-data clause; home microphones (his rule: clean references only).
- A line was drafted (Common Voice as a stated risk weaker than VCTK's); after the fresh review it is not proposed. Pocket's consent rule and MDC's purpose and redistribution clauses are not risks a line can accept: they are the terms of the tools themselves. Pocket's exported voice file [14] is a transformed copy of the clip, not a safeguard.

## What Jafar would have to do

1. Nothing, unless he wants Common Voice regardless. If he did, the steps would be these, and the risks above would be his to accept.
2. Open the MDC account himself and accept its terms.
3. Tick the four boxes on the spontaneous English page; download it himself (519 MB as the site shows it; MDC's Terms 1.d forbid sharing account access, so no key for the session). Free.
4. Pass the final voice by ear.

## Unverified

- No accent column in the data files (datasheet only).
- How many young British men the spontaneous set holds; whether "geordie" is one speaker, and his age.
- Whether a cloned voice is personal data under Appendix 1; whether a shipped voice file meets the no-sharing request; UK and Swiss data-protection law.
- Whether removal requests still reach downloaders under MDC.

## Not reached

- commonvoice.mozilla.org's script-built pages (FAQ, datasets); its static terms, privacy notice and text files were read instead.
- MDC's privacy policy and provider terms; Mozilla's Acceptable Use Policy; Common Voice's governance framework.
- Kyutai's full Pocket card (gated; gate text only).
- The data (not downloaded, by instruction).

## Fresh review (27 October, afternoon): SOUND WITH FIXES, fixes taken

Every cited source re-read except the gated Pocket card (its gate text read). Fixes taken above:
- MDC Appendix 1's purpose and redistribution clauses;
- the voice file is no safeguard;
- VCTK and Common Voice are unequal under Kyutai's consent rule;
- one contributor objected, not several;
- under-19 contributors and optional ages;
- no API key (Terms 1.d).

Also noted:
- MDC's form for dataset owners offers "Any attempt to clone the voice ... is forbidden" as an example condition, so a future release could add it;
- the sizes mix units (the site's 519 MB is 544 MB in decimal);
- the British subset is curated by "MDC Curators" under its own conditions.

Side finding, acted on: Pocket's weights (CC BY 4.0) had no credit row and no decision record; both added on 27 October (THIRD-PARTY.md; DECISIONS.md).
