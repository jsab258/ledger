// LEDGER, the whole game: the system "jobsx": the job template at work (DESIGN 4; parts 3.5.6, 3.5.7, 3.5.1, 3.5.2,
// 2.8.1, 2.8.2, 2.9.1, 2.9.2, 7.14). A job is offered by a person on a state, runs as a small graph of saved
// states (pieces/job_template.js), writes one Ledger line a step, and ends in something the town can talk about.
// The specs are jobs_data.js; the verbs are crime.js, heard through core's emit().
import { G, day, hour } from '../state.js';
import { hyp, clamp, money, hourWords } from '../util.js';
import { act, seed } from '../events.js';
import { note, meet } from '../ledger.js';
import { sub, say, choose, scene, tomName } from '../ui.js';
import { pay, earn } from '../money.js';
import { passTime, fl } from '../work.js';
import { F } from '../fight.js';
import { endTalk } from '../talk.js';
import { RULES } from '../rules.js';
import { register, on, emit, X, PLACES } from './core.js';
import { PIECE } from './pieces/job_template.js';
import { PIECE as CRIME } from './pieces/crime_rules.js';
import { JOB_SPECS, JOB_BY_ID } from './jobs_data.js';
import { startTail, startMind, purses, has, pocket, unpocket, lg } from './crime.js';

const J = PIECE.fns;
const SENT = []; // the job events sent, newest last (for the tests; not saved)
for (const n of ['job:step', 'job:end', 'jobs:arrangement', 'jobs:message', 'jobs:recruit']) on(n, (p) => SENT.push(Object.assign({ name: n }, p)) > 400 && SENT.splice(0, 100));
const R = CRIME.fns;
const T = () => RULES.game.jobsx;
const S = () => X('jobsx');
const P_ = (id) => G.people[id];
const tom = () => G.tom;
const met = (id) => !!G.ledger.met[id];
const debtOpen = (id) => G.debts[id] && G.debts[id].st === 'open';
const live = () => JOB_SPECS.filter((s) => S().runs[s.id] && S().runs[s.id].st === 'taken');
const done = (id) => S().runs[id] && (S().runs[id].st === 'done' || S().runs[id].st === 'failed');

function fresh() {
  return {
    runs: {}, // job id -> its run (pieces/job_template.js), every change saved
    told: {}, // job id -> the minute its message was taken (the message, phone and car channels)
    lastOffer: {}, // giver -> the day index he last offered, so nobody nags
    arrangement: null, // the outfit's arrangement: 'kept' | 'ended' | null (2.9.2); the story reads it
    asks: { done: 0, refused: 0 }, // the asks carried and refused, the story's three included
    variety: [], // { piece, atRealSeconds }: no set piece twice in thirty minutes (law 6)
    debt: {}, // debtor -> what was owed when its collection was taken
    julieWorks: false,
  };
}

// ---------- on what state each job is offered (law 1) ----------
const arrangementOn = () => S().arrangement !== 'ended' && (fl().ask1 === 'yes' || fl().job1 === 'done' || S().asks.done > 0);
const DUE = {
  ask_fri: () => fl().tour && day() === T().askNightsDayIndexes[2] && hour() >= T().askOfferedFromHour && arrangementOn(),
  ask_sun: () => fl().tour && day() === T().askNightsDayIndexes[3] && hour() >= T().askOfferedFromHour && arrangementOn(),
  col_wayne: () => fl().tour && day() >= 1 && debtOpen('wayne'),
  col_dennis: () => fl().tour && day() >= 1 && debtOpen('dennis') && !fl().ask2 && (done('col_wayne') || day() >= 3),
  tail_dennis: () => met('darren') && day() >= 1 && debtOpen('dennis') && hour() < 15,
  brk_hut: () => met('darren') && day() >= 1 && debtOpen('dennis') && (done('tail_dennis') || day() >= 2),
  brk_pawn: () => met('wayne') && day() >= 2 && (fl().job2 === 'done' || done('col_wayne')),
  brk_unit: () => met('lee') && day() >= 3 && done('tail_norman'),
  tail_norman: () => met('lee') && day() >= 2,
  mind_brenda: () => met('brenda') && day() >= 1,
  dmg_iveson: () => fl().tour && day() >= 3 && debtOpen('dennis') && arrangementOn() && (fl().job3 === 'noshow' || fl().ask2 === 'no' || day() >= 4),
};
const dueNow = (spec) => !S().runs[spec.id] && !!DUE[spec.id]();
const varietyOk = (spec) => J.varietyOk(S().variety, spec.setPiece, G.played, T().noSetPieceTwiceWithinRealSeconds);

// ---------- offering ----------
function offerFor(P) {
  if (S().lastOffer[P.id] === day()) return null;
  for (const spec of JOB_SPECS) if (spec.giver === P.id && dueNow(spec) && varietyOk(spec)) return spec;
  return null;
}
const offerScene = (spec) => () =>
  scene(async () => {
    const g = spec.giver;
    S().lastOffer[g] = day();
    meet(P_(g));
    if (!S().runs[spec.id]) S().runs[spec.id] = J.newRun(spec, Math.round(G.t));
    const i = await choose(g, spec.offer, ["Yes. I'll do it.", 'No. Not this.', 'Not now. Ask me again.']);
    if (i === 0) return takeJob(spec, true);
    if (i === 2) {
      delete S().runs[spec.id];
      await say(g, spec.ask ? "Don't be long about it. They count the days." : 'It will keep a day. Not a week.');
      return;
    }
    // a no that cannot be taken back asks twice
    if (spec.ask) {
      const k = await choose(g, "You want me to tell them no? They count, boss. That's the arrangement you're answering for.", ['Yes. Tell them no.', 'No. Let me think.']);
      if (k !== 0) {
        delete S().runs[spec.id];
        return;
      }
    }
    refuseJob(spec);
    await say(g, spec.ask ? "Then I'll tell them. They'll hear it tonight." : 'Right. I never asked.');
  });
function takeJob(spec, viaTalk) {
  const s = S(),
    run = s.runs[spec.id] || J.newRun(spec, Math.round(G.t)),
    r = J.take(run, spec, Math.round(G.t));
  if (!r.ok) return false;
  s.runs[spec.id] = r.run;
  s.variety.push({ piece: spec.setPiece, atRealSeconds: Math.round(G.played) });
  if (s.variety.length > 60) s.variety.shift();
  const st0 = spec.steps[0];
  if (st0.gives && st0.thing) pocket(st0.thing);
  if (st0.debtor) s.debt[st0.debtor] = G.debts[st0.debtor].owed;
  if (viaTalk) act(spec.ask ? 'job_yes' : 'job_word', { silent: true, told: [spec.giver], what: spec.name });
  const pl = PLACES[st0.place];
  note(`Took on ${spec.name}, from ${P_(spec.giver).def.name}. First: ${pl.name}, ${pl.landmark}.`, 'note', 'job_' + spec.id, { who: spec.giver, how: tomName(P_(spec.giver)) + ' says' });
  G.story.objective = `${spec.name.replace(/^./, (m) => m.toUpperCase())}: ${pl.name}, ${pl.landmark}.` + (st0.window ? ` Between ${hourWords(st0.window.fromHour)} and ${hourWords(st0.window.untilHour)}.` : '');
  if (spec.ask === 4) setArrangement('kept');
  for (const e of r.events) emit(e.name, e);
  if (G.hooks.save) G.hooks.save();
  return true;
}
function refuseJob(spec) {
  const s = S(),
    run = s.runs[spec.id] || J.newRun(spec, Math.round(G.t)),
    r = J.refuse(run, spec, Math.round(G.t));
  if (!r.ok) return false;
  s.runs[spec.id] = r.run;
  act(spec.ask ? 'job_no' : 'job_word', { silent: true, told: [spec.giver], what: spec.name });
  note(r.run.lines[r.run.lines.length - 1].line, 'note', 'jobno_' + spec.id, { who: spec.giver, how: 'Said it' });
  if (spec.ask) {
    s.asks.refused++;
    if (spec.ask === 4) setArrangement('ended');
  }
  for (const e of r.events) emit(e.name, e);
  if (G.hooks.save) G.hooks.save();
  return true;
}
function setArrangement(v) {
  if (S().arrangement === v) return;
  S().arrangement = v;
  note(
    v === 'kept' ? "Mickey's arrangement with the people behind the landing stands. Night money, cover, and asks that will grow." : "Mickey's arrangement with the people behind the landing is ended. No more asks, and no more cover from them.",
    'note',
    'arrangement_' + v,
    { who: 'ron', how: 'Said it' },
  );
  emit('jobs:arrangement', { arrangement: v });
}
// the story's own three asks count too (scenes.js flags), read every hour
function countAsks() {
  const f = fl(),
    s = S();
  let d = 0,
    n = 0;
  for (const k of ['job1', 'job2', 'job3']) if (f[k] === 'done') d++;
  if (f.ask1 === 'no') n++;
  if (f.ask2 === 'no') n++;
  for (const id of ['ask_fri', 'ask_sun']) {
    const r = s.runs[id];
    if (r && r.st === 'done') d++;
    if (r && r.outcome === 'refused') n++;
  }
  s.asks = { done: d, refused: n };
  if (n >= 2 && s.arrangement !== 'kept') setArrangement('ended');
  else if (d >= 3 && n === 0 && !s.arrangement) setArrangement('kept');
}

// ---------- steps ----------
function finish(spec, stepId, outcome) {
  const s = S(),
    r = J.resolve(s.runs[spec.id], spec, stepId, outcome, Math.round(G.t));
  if (!r.ok) return false;
  applied(spec, r, stepId, outcome);
  return true;
}
function applied(spec, r, stepId, outcome) {
  const s = S();
  s.runs[spec.id] = r.run;
  const st = spec.steps.find((x) => x.id === stepId),
    O = st ? st.outcomes[outcome] : null;
  note(r.line, 'note', null, { who: st && st.who && st.who[0] ? st.who[0] : spec.giver, how: O && O.fail ? 'It went wrong' : 'Did it' });
  sub(r.line, '', 'over', 6);
  if (r.run.st === 'done' && spec.pay.pence > 0 && !['kept', 'walked', 'dumped', 'struck'].includes(outcome)) {
    earn(spec.pay.pence, spec.pay.dirty, spec.name);
    note(`${money(spec.pay.pence)} for ${spec.name}, ${spec.pay.dirty ? 'in the tin' : 'in his pocket'}.`, 'money', null, { how: 'Counted it' });
  }
  if (r.run.st === 'failed' && (outcome === 'late' || outcome === 'no show')) seed('job_dropped', [spec.giver], { what: spec.name });
  if (spec.ask && (r.run.st === 'done' || r.run.st === 'failed')) countAsks();
  if (r.run.st !== 'taken') {
    G.story.objective = r.run.st === 'done' ? `${spec.name.replace(/^./, (m) => m.toUpperCase())} is done.` : `${spec.name.replace(/^./, (m) => m.toUpperCase())} went wrong. The town will have its say.`;
  } else {
    const nx = spec.steps.find((x) => x.id === r.run.cur),
      pl = PLACES[nx.place];
    G.story.objective = `${spec.name.replace(/^./, (m) => m.toUpperCase())}: ${pl.name}, ${pl.landmark}.`;
  }
  for (const e of r.events) emit(e.name, e);
  if (G.hooks.save) G.hooks.save();
}
const curStep = (spec) => {
  const run = S().runs[spec.id];
  return run && run.st === 'taken' ? spec.steps.find((x) => x.id === run.cur) : null;
};
// what the verbs did, heard from crime.js
function heard(ev, p) {
  for (const spec of live()) {
    const st = curStep(spec);
    if (!st) continue;
    for (const w of [st.when].concat(st.also || [])) {
      if (!w || w.ev !== ev) continue;
      if (Object.keys(w.match || {}).some((k) => p[k] !== w.match[k])) continue;
      const outcome = w.outcome || w.map[String(p[w.by])];
      if (outcome && st.outcomes[outcome]) {
        finish(spec, st.id, outcome);
        break;
      }
    }
  }
}
for (const ev of ['crime:entered', 'crime:found', 'crime:caught', 'crime:fenced', 'crime:rid', 'crime:tail', 'crime:cased', 'crime:mind', 'crime:damage'])
  on(ev, (p) => heard(ev, p || {}));
on('crime:found', (p) => {
  // Iveson's cash box settles his eighty whichever job found it: the money is in the tin and the book is square
  if (p.site === 'hut' && p.container === 'desk') {
    unpocket('the cash box');
    earn(RULES.game.crime.goods.cashboxPence, true, "Iveson's cash box");
    const d = G.debts.dennis;
    if (d && d.st === 'open') {
      d.st = 'paid';
      d.owed = 0;
    }
    const spec = JOB_BY_ID.col_dennis,
      st = curStep(spec);
    if (st) finish(spec, st.id, 'cabin');
  }
});
on('police:searched', (p) => {
  for (const spec of live()) {
    const st = curStep(spec);
    if (st && st.thing && ((p && p.took) || []).includes(st.thing) && st.outcomes.taken) finish(spec, st.id, 'taken');
  }
});

// debts: the book is the game's own (G.debts); a collection's step ends by what the book now says
function debtSteps() {
  for (const spec of live()) {
    const st = curStep(spec);
    if (!st || st.verb !== 'debt') continue;
    const d = G.debts[st.debtor],
      was = S().debt[st.debtor];
    if (d.st === 'paid' && st.outcomes.paid) finish(spec, st.id, 'paid');
    else if (d.st === 'forgiven') finish(spec, st.id, 'struck');
    else if (d.st === 'open' && was !== undefined && d.owed < was) finish(spec, st.id, 'part');
  }
}
// A debtor fronted up pays what his purse holds, and the rest stays on the book (2.8.2). The story's own collection
// (scenes.js) takes the whole sum or half of it whatever he has; here the purse decides. Iveson's Wednesday ask keeps
// the story's road, so its money and its line are as written there.
let yielded0 = null;
function wrapYielded() {
  if (!G.hooks.yielded || G.hooks.yielded.purse) return;
  yielded0 = G.hooks.yielded;
  const fn = (P, demand, rung) => {
    const d = G.debts[P.id];
    if (!demand || demand.type !== 'debt' || !d || d.st !== 'open') return yielded0(P, demand, rung);
    if (P.id === 'dennis' && fl().ask2 === 'yes' && !fl().job3) return yielded0(P, demand, rung);
    const pur = purses(),
      r = R.debtPays({ owedPence: d.owed, pursePence: pur[P.id] === undefined ? d.owed : pur[P.id], rung });
    pur[P.id] = r.purseLeftPence;
    if (r.paidPence > 0) {
      d.owed = r.leftPence;
      d.st = r.st;
      earn(r.paidPence, true, 'a debt collected');
      act('debt_paid', { target: P.id });
    }
    sub(
      r.paidPence === 0 ? "I've nowt. Turn me upside down, I've nowt." : r.leftPence === 0 ? `Take it. ${money(r.paidPence)}. That's us square.` : `${money(r.paidPence)}. That's every penny on me. You'll get the rest when there is a rest.`,
      tomName(P),
      'face',
    );
    lg('debt', { who: P.id, paid: r.paidPence, left: r.leftPence });
  };
  fn.purse = true;
  G.hooks.yielded = fn;
}

// ---------- prompts ----------
function hotspots(out) {
  const t = tom();
  if (t.space !== 'street' || t.inCar || F.on) return;
  for (const spec of live()) {
    const st = curStep(spec);
    if (!st) continue;
    const pl = PLACES[st.place];
    if (!pl || hyp(t.x, t.z, pl.x, pl.z) > T().stepReachedWithinMetres) continue;
    const w = J.windowAt(st, G.t);
    if (w.state !== 'open') {
      // windows, not minutes: every appointment has its "wait until" (ER-JOB-04)
      out.push({ k: 'T', t: 'Wait here until ' + hourWords(st.window.fromHour), run: () => passTime(w.waitUntil + 2, 'He waits.') });
      continue;
    }
    if (st.verb === 'take' && !has(st.thing))
      out.push({
        k: 'E',
        t: 'Take ' + st.thing,
        run: () => {
          if (!pocket(st.thing, st.hand ? 'hand' : undefined)) return;
          act(st.act, { what: st.thing, zone: pl.name });
          finish(spec, st.id, 'took');
        },
      });
    else if (st.verb === 'handover' && has(st.thing)) {
      const to = st.to ? P_(st.to) : null;
      if (to && (to.gone || to.dead || to.space !== 'street' || hyp(to.x, to.z, t.x, t.z) > 6)) continue;
      out.push({
        k: 'E',
        t: to ? 'Give ' + tomName(to) + ' ' + st.thing : 'Knock, and hand over ' + st.thing,
        run: () => {
          unpocket(st.thing);
          delete X('crime').goods[st.thing];
          act(st.act, { what: st.thing, zone: pl.name, told: st.who.filter((id) => P_(id)), noiseR: to ? 0 : RULES.jobs.knockNoiseMetres });
          finish(spec, st.id, 'handed');
        },
      });
    }
  }
}
// tails and minding begin by being there: no prompt, no mode
function implicit() {
  const t = tom();
  for (const spec of live()) {
    const st = curStep(spec);
    if (!st || (st.verb !== 'tail' && st.verb !== 'mind')) continue;
    if (J.windowAt(st, G.t).state !== 'open') continue;
    const P = P_(st.target);
    if (!P || P.gone || P.dead || P.space !== t.space) continue;
    const d = hyp(P.x, P.z, t.inCar ? G.car.x : t.x, t.inCar ? G.car.z : t.z);
    if (st.verb === 'tail') {
      const tl = X('crime').tails[st.target];
      if ((!tl || tl.st !== 'on') && d < 45 && P.moving && G.env.los(P.x, P.z, t.x, t.z)) startTail(st.target, st.learns);
    } else if (!S().minding && d < RULES.game.crime.mind.standsWithinMetres) {
      S().minding = st.target;
      startMind(st.target);
      sub('He takes his place at ' + tomName(P) + "'s shoulder and says nothing.", '', 'over', 4);
    }
  }
}
on('crime:mind', () => {
  S().minding = null;
});

// ---------- talk: the five debts as five lessons, and messages ----------
function matters(P, a) {
  const id = P.id,
    d = G.debts[id];
  if (!d || d.st !== 'open') return;
  const D = RULES.game.crime.debts;
  const kind = (worth, why) => {
    const r = R.debtInKind({ owedPence: d.owed, worthPence: worth });
    d.owed = r.leftPence;
    d.st = r.st;
    act('debt_kind', { target: id });
    lg('debtkind', { who: id, off: r.offPence, left: r.leftPence, why });
    return r;
  };
  if (id === 'darren' && G.hooks.bought)
    a.push({
      key: 'debtword',
      direct: true,
      ask: 'whether Darren may pay what he owes in what he hears',
      raise: "So listen. I've not got twenty-two quid. What I've got is ears. Seven quid off the book every time I tell you something true. Yeah?",
      opts: [
        {
          agree: 1,
          q: 'Seven off the book for what I hear. Yeah or no?',
          yes: ['Yes. Tell me, and it comes off.', 'Yes. Pay me in what you hear.'],
          no: ['No. I want the money.', 'No. Not that way.'],
          keep: ['How do I know it is true?', 'Who do you hear it from?'],
          keepSay: "Cos if it's not, it goes back on the book, dunnit. Yeah or no?",
          noSay: 'Then you want blood from a stone, chief.',
          take: () => {
            const told = G.hooks.bought(P, 0);
            if (!told) return "Nothing going round today. Honest. Ask me tomorrow, I'll have something.";
            const r = kind(D.darrenWordWorthPence, 'what he hears');
            note(`Darren Milner pays his debt in what he hears: ${money(D.darrenWordWorthPence)} off the book for each true thing. ${r.leftPence ? money(r.leftPence) + ' still stands.' : 'He is square.'}`, 'debts', 'darrenword' + day(), { who: 'darren', how: 'Agreed it' });
            return told + (r.leftPence ? ` That's seven off. ${money(r.leftPence)} to go.` : " And that's me square. Write it down.");
          },
        },
      ],
    });
  if (id === 'wayne')
    a.push({
      key: 'debtgoods',
      direct: true,
      ask: "whether Wayne may pay in goods from Rita's back room",
      raise: "I've no thirty quid. There's a carriage clock on the back shelf nobody's coming back for. Worth more than thirty. Take that and we're straight. You following?",
      opts: [
        {
          agree: 1,
          q: 'The clock for the thirty. Yes?',
          yes: ['Yes. The clock.', 'Yes. Fetch it.'],
          no: ['No. Money or nothing.', 'No. Not her goods.'],
          keep: ['Does Rita know?', 'Whose clock is it?'],
          keepSay: "Rita counts the tickets, not the shelf. It's nobody's. The clock for the thirty. Yes?",
          noSay: 'Then it is Friday, if she pays me.',
          take: () => {
            if (!pocket('a carriage clock')) return "You've no room for it. Come back with empty pockets.";
            X('crime').goods['a carriage clock'] = { honestPence: RULES.game.crime.goods.clockPence, owner: 'rita', street: 'Quay Street', takenAt: Math.round(G.t), site: 'pawn' };
            kind(D.wayneGoodsWorthPence, 'goods');
            const spec = JOB_BY_ID.col_wayne,
              st = curStep(spec);
            if (st) finish(spec, st.id, 'goods');
            else note("Wayne Harrison paid in goods off Rita's shelf: a carriage clock, against the thirty on the book. Rita does not know yet.", 'debts', 'waynegoods', { who: 'wayne', how: 'Was there' });
            return "Under your coat. And you never got it here. It's hers if she sees it, mind.";
          },
        },
      ],
    });
  if (id === 'julie' && !S().julieWorks)
    a.push({
      key: 'debtwork',
      direct: true,
      ask: 'whether Julie may work off the nine pounds',
      raise: "I can't pay nine pounds. I can drive, though. I drove the laundry van four years. Let me work it off on the cars.",
      opts: [
        {
          agree: 1,
          q: "You'd let me work it off?",
          yes: ['Yes. Work it off.', 'Yes. Come to the office.'],
          no: ['No. I want it paid.', 'No. Not that.'],
          keep: ['When were you laid off?', 'Can you do nights?'],
          keepSay: "June, when the laundry shut. Days, not nights. You'd let me work it off?",
          noSay: 'Then I do not know what you want me to do.',
          take: () => {
            S().julieWorks = true;
            P.mind.regard = clamp(P.mind.regard + 0.25, -1, 1);
            act('debt_kind', { target: 'julie' });
            note('Julie Kettlewell will work off her nine pounds on the cars: three pounds off the book for each day she drives.', 'debts', 'juliework', { who: 'julie', how: 'Agreed it' });
            emit('jobs:recruit', { who: 'julie', road: 'need', use: 'drive' });
            return "I'll be there at eight. You'll not be sorry. Tell Sheila I can read a street map.";
          },
        },
      ],
    });
  if (id === 'dennis' && G.ledger.notes.some((n) => n.key === 'paper_hut_drawer'))
    a.push({
      key: 'debtlean',
      direct: true,
      ask: 'whether to show Iveson the receipt for the lead out of No. 4',
      raise: "You've a look on you. Whatever it is you think you've got, say it.",
      opts: [
        {
          agree: 1,
          q: 'Lead and copper out of No. 4, as seen. Eighty pounds and I never read it. Yes?',
          yes: ['Yes. Eighty, now.', 'Yes. Pay the book.'],
          no: ['No. Forget I spoke.', 'No. Another day.'],
          keep: ['Who sold it to you?', 'Who else has seen the receipt?'],
          keepSay: "I don't ask a man's name when he's selling lead. Nobody's seen it. Yes?",
          noSay: 'Then get out of my yard.',
          take: () => {
            const amt = d.owed;
            d.owed = 0;
            d.st = 'paid';
            earn(amt, true, "Iveson's debt");
            act('debt_paid', { target: 'dennis' });
            P.mind.fear = clamp(P.mind.fear + 0.3, 0, 1);
            const spec = JOB_BY_ID.col_dennis,
              st = curStep(spec);
            if (st) finish(spec, st.id, 'leaned');
            else note("Showed Iveson the receipt for lead out of No. 4. He paid the eighty without counting and asked who else had seen it.", 'debts', 'dennislean', { who: 'dennis', how: 'Was there' });
            lg('debt', { who: 'dennis', leaned: true, paid: amt });
            return `Here. ${money(amt)}. Count it somewhere else. Who else has seen that paper?`;
          },
        },
      ],
    });
}

// a message taken by Pauline, the office phone, or a man waiting by the car (A17): the Ledger keeps where and who
function messages() {
  for (const spec of JOB_SPECS) {
    if (S().told[spec.id] || !['message', 'phone', 'car'].includes(spec.channel.kind) || !dueNow(spec)) continue;
    if (G.paused || F.on) continue;
    S().told[spec.id] = Math.round(G.t);
    const g = P_(spec.giver),
      pl = PLACES[spec.channel.place],
      via = spec.channel.via ? P_(spec.channel.via) : null,
      line =
        spec.channel.kind === 'car'
          ? `${g.def.name} is waiting by car two, at ${pl.landmark}. He has a word for Tom.`
          : `${via ? via.def.name : 'Pauline'} took a ${spec.channel.kind === 'phone' ? 'call' : 'message'}: ${g.def.name} wants a word, at ${pl.name}, ${pl.landmark}.`;
    note(line, 'note', 'msg_' + spec.id, { who: spec.giver, how: via ? tomName(via) + ' says' : 'Saw him' });
    if (tom().space === 'mickeys' || tom().inCar || spec.channel.kind === 'car') sub(line, via ? tomName(via) : '', 'face', 6);
    emit('jobs:message', { job: spec.id, giver: spec.giver, place: spec.channel.place, kind: spec.channel.kind });
  }
}

register({
  id: 'jobsx',
  fresh,
  loaded: (x) => {
    const f = fresh();
    for (const k in f) if (x[k] === undefined) x[k] = f[k];
    wrapYielded();
  },
  step: () => {
    if (G.paused || G.story.phase !== 'play') return;
    wrapYielded();
    implicit();
    // the story's own carries are set pieces too (law 6)
    const j = G.story.job;
    if (j && j.st === 'carry' && !j.logged) {
      j.logged = 1;
      S().variety.push({ piece: 'carry under watch', atRealSeconds: Math.round(G.played) });
    }
  },
  minute: () => {
    debtSteps();
  },
  hourly: () => {
    countAsks();
    messages();
    // steps sleep while he is away and settle by the clock (ER-JOB-07)
    for (const spec of live()) {
      const r = J.settle(S().runs[spec.id], spec, Math.round(G.t));
      if (r.ok) {
        const out = r.run.steps[r.events[0].step].outcome;
        applied(spec, r, r.events[0].step, out);
      }
    }
    if (S().julieWorks && G.debts.julie.st === 'open' && hour() === 17) {
      const r = R.debtInKind({ owedPence: G.debts.julie.owed, worthPence: RULES.game.crime.debts.julieWorksOffPencePerShift });
      G.debts.julie.owed = r.leftPence;
      G.debts.julie.st = r.st;
    }
  },
  hotspots,
  beatFor: (P) => {
    const spec = offerFor(P);
    return spec ? offerScene(spec) : null;
  },
  matters,
  hook: {
    specs: () => JOB_SPECS,
    sent: () => SENT,
    states: () => ({ job: PIECE.fns ? ['offered', 'taken', 'done', 'failed'] : [], step: ['asleep', 'open', 'done', 'failed', 'skipped'] }),
    check: () => {
      const places = {};
      for (const id in PLACES) places[id] = { landmark: PLACES[id].landmark, address: PLACES[id].address };
      return JOB_SPECS.flatMap((s) => J.check(s, places, Object.keys(G.people)));
    },
    routes: (id) => J.routes(JOB_BY_ID[id]),
    state: () => S(),
    run: (id) => S().runs[id] || null,
    due: () => JOB_SPECS.filter((s) => dueNow(s)).map((s) => s.id),
    offerFor: (who) => {
      const s = offerFor(P_(who));
      return s ? s.id : null;
    },
    // start any job, whatever the state (the tester's road in)
    start: (id) => {
      delete S().runs[id];
      return takeJob(JOB_BY_ID[id], false);
    },
    refuse: (id) => {
      delete S().runs[id];
      return refuseJob(JOB_BY_ID[id]);
    },
    // the tester's skip: end the open step by a named outcome (or its first)
    skip: (id, outcome) => {
      const spec = JOB_BY_ID[id],
        run = S().runs[id];
      if (!run || !run.cur) return false;
      const r = J.skip(run, spec, run.cur, Math.round(G.t), outcome);
      if (!r.ok) return false;
      applied(spec, r, r.events[0].step, r.events[0].outcome);
      return true;
    },
    finish: (id, step, outcome) => finish(JOB_BY_ID[id], step, outcome),
    settleAll: () => {
      for (const spec of live()) {
        const r = J.settle(S().runs[spec.id], spec, Math.round(G.t));
        if (r.ok) applied(spec, r, r.events[0].step, r.run.steps[r.events[0].step].outcome);
      }
    },
    variety: () => J.varietyFaults(S().variety, T().noSetPieceTwiceWithinRealSeconds),
    varietyOk: (id) => varietyOk(JOB_BY_ID[id]),
    arrangement: () => S().arrangement,
    setArrangement,
    countAsks,
  },
});
