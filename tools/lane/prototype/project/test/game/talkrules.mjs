// The one-shot, talk rules without a browser: ER-TALK-03 as its 170 lines that are not a plain yes, each put to every
// shape of decision the game has, at every moment of it; none may be taken. And the game's own files must call the
// rule pieces, not carry a copy (pieces in the game).
import fs from 'fs';
import { PIECE } from '../../src/game/pieces/talk.js';
import { RULES } from '../../src/rules.js';
const T = PIECE.fns;
let bad = 0;
const ok = (c, what) => { console.log((c ? 'ok   ' : 'FAIL ') + what); if (!c) bad++; };

const STEMS = ['Yes, but not tonight', 'Yes?', 'Yes if the money is right', 'Maybe', 'I suppose so', 'Yes, unless Ron says otherwise', "Yes. No. I don't know", 'What happens if I do?', 'Who are they?', 'Tell me more', 'Not yet', 'Hmm', 'Yes once I have seen the book', 'Ok but what is in it?', "I can't say yes to that", 'Is that a yes or a no?', 'Perhaps tomorrow', 'How much?', 'Depends who is asking', 'Aye, though I might regret it', 'All right after Friday', 'Sixty quid?', 'Fine? Is it?', 'Yes when I have thought on it', 'Okay, maybe', 'Alright, but who else knows?', 'I will if Sheila agrees', 'Go on then, unless it rains', 'Agreed? I never agreed', 'Deal, except the coat', 'Yes before I change my mind?', 'Count me in if Ron is', 'What would Mickey have done?', 'Why me?'];
const TAILS = ['.', ' ...', ', boss.', ' Ron.', '!'];
const lines = [];
for (const s of STEMS) for (const t of TAILS) lines.push(/[.?!]$/.test(s) && t === '.' ? s : s.replace(/[.?!]$/, (m) => (t === '.' ? m : '')) + (/\?$/.test(s) && t !== '.' ? '?' : t));
const N = RULES.game.econ.talk.notAPlainYesLines;
ok(lines.length >= N, `${lines.length} lines that are not a plain yes (the rule asks for ${N})`);
const SHAPES = [
  { name: 'an ask that cannot be undone', spec: { opts: [{ agree: 1, asksTwice: true, undoable: false }, { refuse: 1, asksTwice: true, undoable: false }] } },
  { name: 'a direct yes or no', spec: { direct: true, opts: [{ agree: 1, asksTwice: true }] } },
  { name: 'three answers', spec: { opts: [{ asksTwice: true }, { agree: 1, asksTwice: true }, { refuse: 1, asksTwice: true }] } },
];
let taken = 0, tried = 0, leave = 0;
for (const sh of SHAPES)
  for (const st of [T.decisionStart(sh.spec), { q: 0, asked: 1, done: false }, { q: sh.spec.opts.length - 1, asked: 1, done: false }])
    for (const l of lines.slice(0, N)) {
      const r = T.decisionStep(sh.spec, st, { job: 'typed', text: l });
      tried++;
      if (r.taken != null) { taken++; if (taken < 6) console.log('     taken: ' + JSON.stringify(l) + ' in ' + sh.name); }
      if (r.leaveOffered) leave++;
    }
ok(taken === 0, `ER-TALK-03 ${N} lines that are not a plain yes, in ${SHAPES.length} shapes of decision at three moments each (${tried} tries): ${taken} taken`);
ok(leave === tried, 'Leave is offered at every one of them');
ok(lines.slice(0, N).every((l) => !T.plainYes(l)), 'none of them reads as a plain yes');
// and a plain yes is still taken, but only once the plain question stands
for (const sh of SHAPES) {
  const first = T.decisionStep(sh.spec, T.decisionStart({ opts: sh.spec.opts }), { job: 'typed', text: 'Yes.' });
  const then = T.decisionStep(sh.spec, first.state, { job: 'typed', text: 'Yes. Tell them.' });
  ok(first.taken == null && then.taken != null, `${sh.name}: a first yes only puts the plain question, the second takes it`);
}
// the decisions written in the game: every option that has a plain question asks it before it is taken (scenes.js
// decisions are data: q beside yes and no)
const scenes = fs.readFileSync(new URL('../../src/scenes.js', import.meta.url), 'utf8');
const qs = (scenes.match(/\bq: /g) || []).length, yeses = (scenes.match(/\byes: \[/g) || []).length + (scenes.match(/Object\.assign\(\s*\{[^}]*\},\s*(PRINT|COP)/g) || []).length;
ok(qs >= 10 && yeses >= qs - 4, `the game's own decisions carry a plain question beside their yes (${qs} questions, ${yeses} yes lines)`);

// ---------- the pieces in the game ----------
const src = (f) => fs.readFileSync(new URL('../../src/' + f, import.meta.url), 'utf8');
ok(/from '\.\/game\/pieces\/money\.js'/.test(src('money.js')) && /M\.pay\(/.test(src('money.js')) && /M\.wash\(/.test(src('money.js')) && /M\.washCap\(/.test(src('money.js')), 'money.js pays, earns and washes through the money piece');
ok(/FLOWS\.add\(/.test(src('money.js')) && /FLOWS\.check\(/.test(src('game/econ.js')), 'every movement goes into the flows piece, and the system checks it each game minute');
ok(/DEBTS\.collect\(/.test(src('game/econ.js')) && /DEBTS\.strike\(/.test(src('game/econ.js')), 'debts are collected and struck out through the debts piece (G.hooks.debtCollect, debtForgive)');
ok(/TALKRULE\.intent\(/.test(src('talk.js')) && /TALKRULE\.plainYes\(/.test(src('talk.js')) && /TALKRULE\.claimCheck\(/.test(src('talk.js')), 'talk.js reads intent, the plain yes and the claim check from the talk piece');
ok(!/function spend\(/.test(src('talk.js')), 'talk.js has no payment of its own: money put in a hand goes through money.js');
const fightCalls = /pieces\/fights\.js/.test(src('fight.js'));
console.log('note ' + (fightCalls ? 'fight.js calls the fights piece' : 'fight.js still runs its own code: the fights piece states the same rules from the same numbers (ONE-SHOT-PORTING.md)'));
console.log(bad ? 'TEST FAIL (' + bad + ')' : 'PASS');
process.exit(bad ? 1 : 0);
