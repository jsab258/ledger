// Everyone who sets off for a place gets there. LEDGER.check.arrivals() is passed over 26 game hours twice,
// once with Tom away (indoors, in his room at Regent House) and once with Tom standing at the rank, where
// people in his sight walk at their real pace. A pass: no walk given up for another place, nobody standing
// still, every pause resumed. Writes out/arrivals.json.
//   node test/arrivals.mjs [away|rank]      one of the two, or both
import fs from 'fs';
import { launch } from './harness.mjs';

const which = process.argv[2] ? [process.argv[2]] : ['away', 'rank'];
const HOURS = +(process.env.HOURS || 26);
const results = {};
let bad = 0;
for (const w of which) {
  const h = await launch({ port: w === 'away' ? 8881 : 8882 });
  await h.newWeek();
  const r = await h.ev(async (w, hours) => {
    if (w === 'away') LEDGER.goInside('the bed at Regent House');
    return LEDGER.check.arrivals({ forGameHours: hours, tomAt: w === 'rank' ? 'the rank' : undefined });
  }, w, HOURS);
  const errors = h.errors.slice();
  await h.close();
  const ok = r.walksGivenUpForAnotherPlace === 0 && !r.stoodStill.length && !r.pauseNeverEnded && !errors.length;
  if (!ok) bad++;
  results[w] = Object.assign({ tom: w === 'away' ? 'away: indoors at Regent House' : 'standing at the rank', pass: ok }, r);
  console.log(`${ok ? 'ok  ' : 'FAIL'} Tom ${results[w].tom}: ${r.from} to ${r.until} | ${r.walksSetOff} walks set off, ${r.walksArrived} arrived, ${r.walksGivenUpForAnotherPlace} given up for another place (${r.ofThoseToOrFromTheMapEdge} to or from the map edge), ${r.stillWalkingAtTheEnd.length} still on their way at the end${r.tomPutBackThereTimes ? ' | Tom put back at the rank ' + r.tomPutBackThereTimes + ' times' : ''} | longest walk ${r.longestWalkGameMinutes} game minutes | stood still: ${r.stoodStill.length} | pause never ended: ${r.pauseNeverEnded ? 'yes' : 'no'}`);
  for (const g of r.gaveUp || []) console.log(`     gave up: ${g.personId} | ${g.from} -> ${g.goingTo} | ${g.setOffAt} | ${g.fault}`);
  for (const g of r.stoodStill || []) console.log(`     stood still: ${g.personId} | going to ${g.goingTo} | ${g.at} | ${g.fault}`);
  if (errors.length) console.log('     errors:', errors.slice(0, 3).join(' | '));
}
fs.mkdirSync('out', { recursive: true });
const file = which.length === 2 ? 'out/arrivals.json' : `out/arrivals_${which[0]}.json`;
fs.writeFileSync(file, JSON.stringify(results, null, 1));
console.log(bad ? 'FAIL' : 'PASS');
process.exit(bad ? 1 : 0);
