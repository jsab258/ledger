// One full week played by script through the test hook (see week_bot.mjs). Writes out/measures.json and
// prints what happened. Not a person: the measures show that everything counts, not how a player behaves.
//   node test/week.mjs [low|medium]
import { launch } from './harness.mjs';
import { playWeek } from './week_bot.mjs';

const h = await launch({ port: 8795, quality: process.argv[2] || 'low', width: 1280, height: 720 });
const r = await playWeek(h);
console.log('ERRORS', h.errors.length, [...new Set(h.errors)].slice(0, 8).join('\n  '));
await h.close();
// What the first round's play script printed to be read is checked here, pass or fail.
const f = r.facts || {};
const facts = [
  ['Sheila read him the book (the tour)', f.tour], ['met Ron and the lad with the pager', f.metRon && f.metDarren], ['the first night job was done', f.firstNightJob === 'done'],
  ['money came in off the meter', f.earnedOffTheMeterPence > 0], ['it went through the fare book', f.putThroughTheBookPence > 0], ['a fare was driven', f.faresDriven >= 1],
  ['stories were passed on', f.storiesPassedOn > 0], ['something was said to his face', f.saidToHisFace >= 1], ['there were talks', f.talks >= 5], ['the rent was paid', f.rentPaid],
  ['a debt on the book was asked for, and answered', (f.decisionsPut || []).includes('debt')], ['the week ended with an answer', !!f.choice], ['the run report is written', f.reportCharacters > 1000],
];
for (const [name, ok] of facts) console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}`);
const ok = facts.every((x) => x[1]) && !r.failed && r.ended && !h.errors.length && (r.pauseFaults === 0 || (Array.isArray(r.pauseFaults) && !r.pauseFaults.length)) && r.badEntries === 0 && r.measures.entriesWithNoSourceEvent === 0;
console.log(ok ? 'PASS' : 'FAIL');
process.exit(ok ? 0 : 1);
