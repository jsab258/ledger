#!/usr/bin/env python3
"""THE VOICE IN PIECES INSIDE A SENTENCE (item 2, the delay; 1 October;
production/research/voice-latency/FAST-FIRST-AUDIO-2026-10-01.md, step 2).

Today the voice server makes a whole sentence before any of it is heard.
Nano's decoder comes from CosyVoice 2, which streams: the sound tokens are
turned into sound in chunks while the token loop is still making them. This
is that method on the installed model, with none of its settings changed:

  tokens_as_made   the token loop exactly as t3.inference_turbo runs it (the
                   same operations in the same order, so the same seed gives
                   the same tokens), handing over each token as it is made.
  PieceDecoder     CosyVoice 2's token2wav streaming. Each pass decodes all
                   the tokens so far, the last three held back as lookahead
                   until the sentence ends, and keeps only the new
                   spectrogram frames; the vocoder runs on them with the
                   previous pass's last 8 frames and its source signal, and
                   the last 8 frames' sound is held back to fade into the
                   next piece. One noise for the whole sentence, fixed per
                   frame, so every pass starts each frame from the same place.

Nano's decoder was not trained for chunks (its streaming line is commented
out, and its attention sees the whole sentence), so a frame decoded before
later tokens exist can differ from the same frame decoded with them; in
August a stitched line in the old studio said a word twice for that reason
(tools/voice-live/export-decode.py). --measure says by how much, beside how
much two whole takes of the same tokens differ from each other, and writes
both for a listen.

    env-dml\\Scripts\\python.exe tools/voice-live/nano_stream.py --measure [--who rocco] [--out F:/LedgerTools/tmp/nano-stream]
    python tools/voice-live/nano_stream.py --selftest
"""
import json
import pathlib
import sys
import time

import numpy as np

MEL_PER_TOKEN = 2           # the flow's token_mel_ratio: 25 tokens, 50 frames a second
LOOKAHEAD = 3               # the encoder's pre-lookahead, in tokens (flow.pre_lookahead_len)
SAMPLES_PER_MEL = 480       # 24 kHz
MEL_CACHE = 8               # CosyVoice 2's mel_cache_len
SRC_CACHE = MEL_CACHE * SAMPLES_PER_MEL
SPEECH_VOCAB = 6561         # a token at or above this is not sound
SIL = 4299                  # S3GEN_SIL, three of which end every sentence
# Tokens of sound in the first piece and in each after it. Beside the game a
# token takes about 44 ms and a pass about 0.6 s, so the decoder, not the
# loop, sets the pace: every 15 tokens (0.6 s of speech) it keeps up, every 25
# the first piece (0.44 s) would wait for a second one a second away.
FIRST, NEXT = 15, 15


def tokens_as_made(torch, t3, t3_cond, text_tokens, temperature=0.8, top_k=1000, top_p=0.95,
                   repetition_penalty=1.2, max_gen_len=1000, generator=None):
    """t3.inference_turbo's loop, yielding each token as an int as it is made
    (the stop token too; the caller keeps only sound tokens, as generate does).
    With a generator of its own, its draws are its own: a decoder working
    on another thread at the same time cannot change which tokens come."""
    import torch.nn.functional as F
    from transformers.generation.logits_process import (LogitsProcessorList, RepetitionPenaltyLogitsProcessor,
                                                        TemperatureLogitsWarper, TopKLogitsWarper, TopPLogitsWarper)
    with torch.inference_mode():
        procs = LogitsProcessorList()
        if temperature > 0 and temperature != 1.0:
            procs.append(TemperatureLogitsWarper(temperature))
        if top_k > 0:
            procs.append(TopKLogitsWarper(top_k))
        if top_p < 1.0:
            procs.append(TopPLogitsWarper(top_p))
        if repetition_penalty != 1.0:
            procs.append(RepetitionPenaltyLogitsProcessor(repetition_penalty))
        start = t3.hp.start_speech_token * torch.ones_like(text_tokens[:, :1])
        embeds, _ = t3.prepare_input_embeds(t3_cond=t3_cond, text_tokens=text_tokens, speech_tokens=start, cfg_weight=0.0)
        out = t3.tfmr(inputs_embeds=embeds, use_cache=True)
        past = out.past_key_values
        logits = t3.speech_head(out[0][:, -1:])
        nxt = torch.multinomial(F.softmax(procs(start, logits[:, -1, :]), dim=-1), num_samples=1, generator=generator)
        made = [nxt]
        cur = nxt
        stop = t3.hp.stop_speech_token
        yield int(nxt)
        for _ in range(max_gen_len):
            out = t3.tfmr(inputs_embeds=t3.speech_emb(cur), past_key_values=past, use_cache=True)
            past = out.past_key_values
            p = procs(torch.cat(made, dim=1), t3.speech_head(out[0])[:, -1, :])
            if torch.all(p == -float("inf")):
                break
            nxt = torch.multinomial(F.softmax(p, dim=-1), num_samples=1, generator=generator)
            made.append(nxt)
            cur = nxt
            v = int(nxt)
            yield v
            if v == stop:
                break


def flow_unfinished(torch, flow, token, token_len, prompt_token, prompt_token_len, prompt_feat, prompt_feat_len, embedding,
                    noised_mels):
    """flow.inference(finalize=False) as it was meant to be: the encoding of
    the last three tokens, whose lookahead has not been made yet, dropped
    together with its padding mask. The installed code drops the encoding but
    not the mask, so the two disagree in length and the decoder fails. The
    rest is that method line for line, for one sentence, on the flow's own
    device; the spectrogram comes back to the processor."""
    import torch.nn.functional as F
    from chatterbox.models.s3gen.utils.mask import make_pad_mask
    dev = next(flow.parameters()).device
    token, token_len, prompt_token, prompt_token_len, prompt_feat, embedding, noised_mels = (
        x.to(dev) for x in (token, token_len, prompt_token, prompt_token_len, prompt_feat, embedding, noised_mels))
    embedding = flow.spk_embed_affine_layer(F.normalize(torch.atleast_2d(embedding), dim=1))
    token, token_len = torch.concat([prompt_token, token], dim=1), prompt_token_len + token_len
    mask = (~make_pad_mask(token_len)).unsqueeze(-1).to(embedding)
    h, h_masks = flow.encoder(flow.input_embedding(token.long()) * mask, token_len)
    trim = flow.pre_lookahead_len * flow.token_mel_ratio
    h, h_masks = h[:, :-trim], h_masks[..., :-trim]
    h_lengths = h_masks.sum(dim=-1).squeeze(dim=-1)
    mel_len1 = prompt_feat.shape[1]
    mel_len2 = h.shape[1] - mel_len1
    h = flow.encoder_proj(h)
    conds = torch.zeros([1, mel_len1 + mel_len2, flow.output_size], device=h.device).to(h.dtype)
    conds[:, :mel_len1] = prompt_feat
    feat, _ = flow.decoder(mu=h.transpose(1, 2).contiguous(), mask=(~make_pad_mask(h_lengths)).unsqueeze(1).to(h), spks=embedding,
                           cond=conds.transpose(1, 2), n_timesteps=2, noised_mels=noised_mels, meanflow=True)
    return feat[:, :, mel_len1:].to("cpu")


class PieceDecoder:
    """One sentence's sound, a piece at a time. feed() takes all the sound
    tokens so far and returns the new sound ready to play (a float array at
    24 kHz), or None when too few new tokens have come. The pieces played one
    after another are the sentence: their lengths add up to the whole take's."""

    def __init__(self, torch, s3, ref_dict, noise_seed, max_tokens=1000, edge="mask"):
        # edge: how a pass treats the last three tokens, still without their
        # lookahead. "mask": decoded without them (flow_unfinished, the
        # method's own way). "end": decoded as if the sentence ended there,
        # and their frames dropped afterwards.
        self.torch, self.s3, self.ref, self.edge = torch, s3, ref_dict, edge
        self.n_prompt = int(ref_dict["prompt_token"].shape[-1])
        g = torch.Generator().manual_seed(int(noise_seed))
        self.noise = torch.randn(1, 80, MEL_PER_TOKEN * (self.n_prompt + max_tokens + 2 * LOOKAHEAD), generator=g)
        # THE FADE AT A JOIN goes from exactly nothing to everything. CosyVoice
        # 2's Hamming window stops at 8% at both ends, which left a small step
        # at the join, a faint tick in quiet stretches (--measure, 1 October).
        self.fade_in = (0.5 - 0.5 * np.cos(np.pi * (np.arange(SRC_CACHE) + 0.5) / SRC_CACHE)).astype(np.float32)
        self.mel_done = 0
        self.cache_mel = None
        self.src_cache = None
        self.tail = None
        self.mels = []          # each pass's new frames, for --measure
        self.timing = []        # each pass's (flow, vocoder) seconds

    def frames_ready(self, n_tokens, final):
        return MEL_PER_TOKEN * (n_tokens if final else n_tokens - LOOKAHEAD) - self.mel_done

    def feed(self, tokens, final, min_new=2 * MEL_CACHE):
        n = len(tokens)
        if not final and self.frames_ready(n, False) < min_new:
            return None
        # ITS OWN RANDOMNESS: the decoder and the vocoder draw noise, and drawn
        # from the token loop's sequence between its tokens, they changed which
        # tokens came next. Forked, the sentence's tokens are the whole take's.
        fork = getattr(getattr(self.torch, "random", None), "fork_rng", None)
        if fork is None:
            return self._feed(tokens, final)
        with fork(devices=[]):
            return self._feed(tokens, final)

    def _feed(self, tokens, final):
        torch, s3 = self.torch, self.s3
        n = len(tokens)
        t = time.time()
        tok, tok_len = torch.tensor([tokens], dtype=torch.long), torch.tensor([n], dtype=torch.long)
        full_len = MEL_PER_TOKEN * (self.n_prompt + n)
        if final or self.edge == "end":
            mels, _ = s3.flow.inference(token=tok, token_len=tok_len, finalize=True, noised_mels=self.noise[:, :, :full_len],
                                        n_timesteps=2, meanflow=s3.meanflow, **self.ref)
            if not final:
                mels = mels[:, :, :-MEL_PER_TOKEN * LOOKAHEAD]
        else:
            mels = flow_unfinished(torch, s3.flow, tok, tok_len, noised_mels=self.noise[:, :, :full_len - MEL_PER_TOKEN * LOOKAHEAD],
                                   **self.ref)
        mels = mels.to("cpu", dtype=s3.dtype)
        t_flow = time.time() - t
        new = mels[:, :, self.mel_done:]
        self.mels.append(new.numpy()[0].copy())
        feat = new if self.cache_mel is None else torch.cat([self.cache_mel, new], dim=2)
        t = time.time()
        wav, src = s3.hift_inference(feat, self.src_cache)
        self.timing.append((round(t_flow, 3), round(time.time() - t, 3)))
        wav = wav[0].detach().cpu().numpy().astype(np.float32)
        if self.tail is None:
            fade = s3.trim_fade.detach().cpu().numpy()
            wav[:len(fade)] *= fade          # as the whole take's start (s3gen.inference)
        else:
            wav[:SRC_CACHE] = wav[:SRC_CACHE] * self.fade_in + self.tail * (1.0 - self.fade_in)
        self.mel_done += new.shape[2]
        if final:
            return wav
        self.cache_mel = feat[:, :, -MEL_CACHE:]
        self.src_cache = src[:, :, -SRC_CACHE:]
        self.tail = wav[-SRC_CACHE:].copy()
        return wav[:-SRC_CACHE]


def heard_through(n, final):
    """Seconds of sound the pieces up to a pass at n tokens have made: all of
    it at the last pass (n counts its three silences), else up to the
    lookahead, less the stretch held back to fade into the next piece."""
    if final:
        return MEL_PER_TOKEN * n * SAMPLES_PER_MEL / 24000.0
    return max(0.0, (MEL_PER_TOKEN * (n - LOOKAHEAD) - MEL_CACHE) * SAMPLES_PER_MEL / 24000.0)


def passes_to_come(last_fed, n_total, first=FIRST, step=NEXT):
    """The passes still to make, in order, as (tokens, final): the ones due
    by the schedule before the sentence's n_total sound tokens, then the
    last, with its three silences."""
    out, fed = [], last_fed
    while True:
        due = (first + LOOKAHEAD) if fed == 0 else fed + step
        if due >= n_total:
            break
        out.append((due, False))
        fed = due
    out.append((n_total + 3, True))
    return out


def gapless_if_released(now, play_start, heard_ready, to_come, n_now, tok_s, pass_s, decoder_free_at, loop_done=False,
                        margin=0.08):
    """THE HEAD START (August's rule, made exact for pieces): whether sound
    released now plays to the end with no gap, by the rates measured so far.
    Each pass to come is ready when its tokens are made and the decoder is
    free, and must be ready before the sound before it has been heard.
    heard_ready: seconds of sound already made; to_come: passes_to_come(),
    any already in hand first; decoder_free_at: when the pass in hand began
    (or now, with none)."""
    free = decoder_free_at
    heard_until = play_start + heard_ready
    for n, final in to_come:
        need = n - 3 + 1 if final else n         # the last pass waits for the stop token
        ready = now + (need - n_now) * tok_s if need > n_now and not (final and loop_done) else float("-inf")
        end = max(ready, free) + pass_s
        if end > heard_until - margin:
            return False
        free = end
        heard_until = play_start + heard_through(n, final)
    return True


def schedule_due(n_sound, last_fed, first=FIRST, step=NEXT):
    """Whether a pass is due with n_sound sound tokens made: the first once
    `first` tokens of sound plus the lookahead exist, then every `step`."""
    if last_fed == 0:
        return n_sound >= first + LOOKAHEAD
    return n_sound >= last_fed + step


def speak_in_pieces(torch, speaker, text_tokens, n_chars, seed, play_start_at, rates, dev, tokens_per_char=1.75):
    """One sentence in pieces, as (sound, seconds since it began) in order:
    the token loop here, the decoder on a thread of its own, and the first
    piece held until the head start says the rest will come in time. rates
    {"tok", "pass"} carries the measured seconds a token and a pass from one
    sentence to the next; play_start_at(now) says when sound released now
    would begin (after the reply's sound before it)."""
    import math
    import threading
    import queue
    t0 = time.time()
    g = torch.Generator(device=dev)
    g.manual_seed(int(seed))
    dec = PieceDecoder(torch, speaker.s3gen, speaker.conds.gen, noise_seed=seed)
    jobs, made, pending, lock = queue.Queue(), [], [], threading.Lock()
    state = {"since": None, "error": None}

    def worker():
        while True:
            job = jobs.get()
            if job is None:
                return
            with lock:
                state["since"] = time.time()
            try:
                wav = dec._feed(*job)        # its randomness is the decoder's; the loop has its own
            except Exception as e:
                with lock:
                    state["error"] = e
                return
            with lock:
                rates["pass"] = 0.5 * rates["pass"] + 0.5 * (time.time() - state["since"])
                made.append(np.zeros(0, np.float32) if wav is None else wav)
                pending.pop(0)
                state["since"] = None
    th = threading.Thread(target=worker, daemon=True)
    th.start()
    sound, fed, given, released, stamps = [], 0, 0, [False], []
    est = max(8, int(math.ceil(tokens_per_char * n_chars)))

    def tok_s():
        if len(stamps) >= 4:
            return (stamps[-1] - stamps[0]) / (len(stamps) - 1)
        return rates["tok"]

    def may_release(loop_done):
        if released[0]:
            return True
        now = time.time()
        with lock:
            if state["error"] is not None:
                raise state["error"]
            ready = sum(len(w) for w in made) / 24000.0
            busy = state["since"]
            to_come = list(pending)
        if not loop_done:
            to_come += passes_to_come(fed, max(est, len(sound) + 1))
        released[0] = gapless_if_released(now, play_start_at(now), ready, to_come, len(sound), tok_s(), rates["pass"],
                                          busy if busy is not None else now, loop_done)
        return released[0]

    def take():
        nonlocal given
        with lock:
            fresh = made[given:]
            given = len(made)
        for w in fresh:
            if len(w):
                yield w, time.time() - t0
    for v in tokens_as_made(torch, speaker.t3, speaker.conds.t3, text_tokens, generator=g):
        if v < SPEECH_VOCAB:
            sound.append(v)
            stamps.append(time.time())
        if schedule_due(len(sound), fed):
            with lock:
                pending.append((len(sound), False))
            jobs.put((list(sound), False))
            fed = len(sound)
        if may_release(False):
            yield from take()
    rates["tok"] = tok_s()
    with lock:
        pending.append((len(sound) + 3, True))
    jobs.put((sound + [SIL] * 3, True))
    jobs.put(None)
    while True:
        if may_release(True):
            yield from take()
        with lock:
            over = not pending and given == len(made)
            if state["error"] is not None:
                raise state["error"]
        if over:
            break
        time.sleep(0.005)
    th.join()


def selftest():
    """The bookkeeping, with a stand-in flow and vocoder: the pieces add up to
    the whole take's length, and each pass decodes only frames it may keep."""
    import types

    class T:   # the few torch calls PieceDecoder makes, on numpy
        long = "long"

        class Generator:
            def manual_seed(self, s):
                self.r = np.random.default_rng(s)
                return self

        @staticmethod
        def randn(*shape, generator):
            return Arr(generator.r.standard_normal(shape).astype(np.float32))

        @staticmethod
        def tensor(x, dtype=None):
            return Arr(np.array(x))

        @staticmethod
        def cat(xs, dim):
            return Arr(np.concatenate([x.a for x in xs], axis=dim))

    class Arr:
        def __init__(self, a):
            self.a = a
            self.shape = a.shape

        def __getitem__(self, k):
            return Arr(self.a[k])

        def to(self, *a, **k):
            return self

        def numpy(self):
            return self.a

        def detach(self):
            return self

        def cpu(self):
            return self

    seen = []

    def flow(token, token_len, finalize, noised_mels, n_timesteps, meanflow, **ref):
        n = int(token_len.a[0])
        frames = MEL_PER_TOKEN * (n if finalize else n - LOOKAHEAD)
        seen.append((n, finalize, noised_mels.shape[2], frames))
        return Arr(np.ones((1, 80, frames), np.float32)), None

    def hift(feat, cache):
        k = feat.shape[2] * SAMPLES_PER_MEL
        return Arr(np.ones((1, k), np.float32)), Arr(np.zeros((1, 1, k), np.float32))
    s3 = types.SimpleNamespace(flow=types.SimpleNamespace(inference=flow), hift_inference=hift, meanflow=True, dtype=None,
                               trim_fade=Arr(np.ones(960, np.float32)))
    ref = {"prompt_token": Arr(np.zeros((1, 150)))}
    ok = True

    def check(what, cond):
        nonlocal ok
        ok = ok and cond
        print(("ok   " if cond else "FAIL ") + what)
    for total in (9, 18, 40, 77, 130):
        seen.clear()
        d = PieceDecoder(T, s3, ref, 1, edge="end")
        toks, out, fed = [], 0, 0
        for k in range(total):
            toks.append(k)
            if schedule_due(len(toks), fed):
                piece = d.feed(toks, False)
                if piece is not None:
                    out += len(piece)
                    fed = len(toks)
        out += len(d.feed(toks + [SIL] * 3, True))
        check("%d tokens: the pieces add up to the whole take (%d samples)" % (total, out),
              out == MEL_PER_TOKEN * (total + 3) * SAMPLES_PER_MEL)
        check("%d tokens: each pass's noise covers exactly its frames and the prompt's" % total,
              all(nm == MEL_PER_TOKEN * (150 + n) for n, f, nm, _ in seen))
    check("the first pass waits for 15 tokens of sound and the lookahead", not schedule_due(17, 0) and schedule_due(18, 0))
    check("the passes to come: 18, 33, 48, then the last with its silences",
          passes_to_come(0, 60) == [(18, False), (33, False), (48, False), (63, True)])
    check("a short sentence: only the last", passes_to_come(0, 17) == [(20, True)])
    # The head start: a token every 10 ms and a pass of 0.05 s, well ahead of
    # speech: once the first piece is in hand, the rest keeps up.
    check("well ahead of speech, the first piece goes at once",
          gapless_if_released(10.0, 10.0, heard_through(18, False), passes_to_come(18, 60), 18, 0.01, 0.05, 10.0))
    check("as fast as speech but a pass slower than a piece: held",
          not gapless_if_released(10.0, 10.0, heard_through(18, False), passes_to_come(18, 60), 18, 0.04, 0.7, 10.0))
    # Twice as slow as it is heard: not at the first piece; yes near the end.
    check("twice as slow: held at the first piece",
          not gapless_if_released(10.0, 10.0, heard_through(18, False), passes_to_come(18, 60), 18, 0.08, 0.3, 10.0))
    check("twice as slow: released when the work left is under the sound to hear",
          gapless_if_released(10.0, 10.0, heard_through(43, False), [(63, True)], 62, 0.08, 0.3, 10.0, loop_done=True))
    check("released into a reply still playing, it starts after it",
          gapless_if_released(10.0, 13.0, heard_through(18, False), passes_to_come(18, 60), 18, 0.08, 0.3, 10.0))
    check("then every 15", not schedule_due(32, 18) and schedule_due(33, 18))
    return 0 if ok else 1


def measure(argv):
    """Same tokens, three decodings: whole (noise A), in pieces (noise A),
    whole again (noise B). In pieces against whole is what streaming changes;
    whole against whole again is how much two takes of the same tokens differ
    anyway. Both in units of the whole take's spectrogram range."""
    import importlib.util
    here = pathlib.Path(__file__).resolve().parent
    who = argv[argv.index("--who") + 1] if "--who" in argv else "rocco"
    out = pathlib.Path(argv[argv.index("--out") + 1] if "--out" in argv else "F:/LedgerTools/tmp/nano-stream")
    out.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location("voice_server", here / "voice-server.py")
    vs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(vs)
    torch, speaker, dev = vs.load_models("--cpu" in argv)
    import soundfile as sf
    from chatterbox.tts_turbo import punc_norm
    conds, _ = vs.learn(torch, speaker, who, vs.clip_for(who))
    speaker.conds = type(conds)(t3=conds.t3.to(device=dev), gen={k: (v.to("cpu") if torch.is_tensor(v) else v) for k, v in conds.gen.items()})
    s3 = speaker.s3gen
    for _ in range(2):
        speaker.generate("Right.")
    lines = ["Depends who's asking.", "Ask Sheila, she keeps the book.", "Aye, she's alright is Sheila.",
             "The rank fills up about six, after the pubs.", "Rita's had that shop years, longer than me.",
             "Couldn't tell you, pal. I keep myself to myself, me."]
    rows = []
    for i, text in enumerate(lines):
        tt = speaker.tokenizer(punc_norm(text), return_tensors="pt", padding=True, truncation=True).input_ids.to(speaker.device)
        torch.manual_seed(7000 + i)
        stock = [int(x) for x in speaker.t3.inference_turbo(t3_cond=speaker.conds.t3, text_tokens=tt).to("cpu")[0]]
        stock = [x for x in stock if x < SPEECH_VOCAB]
        torch.manual_seed(7000 + i)
        alone = [v for v in tokens_as_made(torch, speaker.t3, speaker.conds.t3, tt) if v < SPEECH_VOCAB]
        torch.manual_seed(7000 + i)
        t0 = time.time()
        sound, fed, first_at, pieces = [], 0, None, []
        streamed = PieceDecoder(torch, s3, speaker.conds.gen, noise_seed=100 + i, edge="mask")
        for v in tokens_as_made(torch, speaker.t3, speaker.conds.t3, tt):
            if v < SPEECH_VOCAB:
                sound.append(v)
            if schedule_due(len(sound), fed):
                p = streamed.feed(list(sound), False)
                if p is not None:
                    pieces.append(p)
                    fed = len(sound)
                    if first_at is None:
                        first_at = time.time() - t0
        pieces.append(streamed.feed(sound + [SIL] * 3, True))
        t_all = time.time() - t0
        # The other edge, "end", on the same tokens and the same schedule.
        ended, fed2, ended_pieces = PieceDecoder(torch, s3, speaker.conds.gen, noise_seed=100 + i, edge="end"), 0, []
        for k in range(1, len(sound) + 1):
            if schedule_due(k, fed2):
                p = ended.feed(sound[:k], False)
                if p is not None:
                    ended_pieces.append(p)
                    fed2 = k
        ended_pieces.append(ended.feed(sound + [SIL] * 3, True))
        whole = PieceDecoder(torch, s3, speaker.conds.gen, noise_seed=100 + i)
        w_whole = whole.feed(sound + [SIL] * 3, True)
        again = PieceDecoder(torch, s3, speaker.conds.gen, noise_seed=900 + i)
        again.feed(sound + [SIL] * 3, True)
        m_whole, m_again = whole.mels[0], again.mels[0]
        m_stream = np.concatenate(streamed.mels, axis=1)
        span = float(m_whole.max() - m_whole.min()) or 1.0
        joins, at = [], 0
        for m in streamed.mels[:-1]:
            at += m.shape[1]
            joins.append(at)
        near = [f for j in joins for f in range(max(0, j - 6), min(m_whole.shape[1], j + 2))]
        diff = np.abs(m_stream - m_whole).mean(axis=0) / span
        diff_end = np.abs(np.concatenate(ended.mels, axis=1) - m_whole).mean(axis=0) / span
        take = np.abs(m_again - m_whole).mean(axis=0) / span
        w_stream = np.concatenate(pieces)
        sf.write(str(out / ("%s-%02d-whole.wav" % (who, i))), w_whole, speaker.sr, subtype="PCM_16")
        sf.write(str(out / ("%s-%02d-pieces.wav" % (who, i))), w_stream, speaker.sr, subtype="PCM_16")
        sf.write(str(out / ("%s-%02d-pieces-end.wav" % (who, i))), np.concatenate(ended_pieces), speaker.sr, subtype="PCM_16")
        row = {"text": text, "loopSameAsStock": alone == stock, "tokensSameAsStock": sound == stock, "tokens": len(sound), "pieces": len(pieces),
               "joinsAtFrame": joins, "samplesSame": len(w_stream) == len(w_whole),
               "piecesVsWholeMean": round(float(diff.mean()), 4), "piecesVsWholeNearJoinsMax": round(float(diff[near].max()), 4) if near else 0.0,
               "endEdgeVsWholeMean": round(float(diff_end.mean()), 4), "endEdgeNearJoinsMax": round(float(diff_end[near].max()), 4) if near else 0.0,
               "takeVsTakeMean": round(float(take.mean()), 4), "takeVsTakeMax": round(float(take.max()), 4),
               "firstPieceS": round(first_at, 2) if first_at else None, "allS": round(t_all, 2),
               "speechS": round(len(w_stream) / speaker.sr, 2), "passes": streamed.timing}
        rows.append(row)
        print(json.dumps(row), flush=True)
    (out / ("measure-%s.json" % who)).write_text(json.dumps(rows, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--measure" in sys.argv:
        sys.exit(measure(sys.argv))
    print(__doc__)
