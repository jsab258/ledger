// LEDGER. The end of the week: the truth beside the Ledger (a playtest view) and the run report.
import { measures } from './measures.js';
import { G, day } from './state.js';
import { money, esc, listAnd } from './util.js';
import { KINDS, NAMES, whenTxt } from './kinds.js';
import { truthTable } from './ledger.js';
import { callName, townLevel, loudness } from './gossip.js';
import { attached } from './seeing.js';
import { real, stamp, gkey } from './ledger_screen.js';

// ---------- the end ----------
function truthGroups() {
  const g = new Map();
  for (const r of truthTable()) {
    if (r.E.kind === 'inherit') continue;
    const k = gkey(r.E);
    if (!g.has(k))
      g.set(k, {
        E: r.E,
        k: r.k,
        saw: new Set(),
        heard: new Set(),
        unnamed: new Set(),
        believed: new Set(),
        zones: new Set(),
      });
    const x = g.get(k);
    r.saw.forEach((i) => x.saw.add(i));
    r.heard.forEach((i) => x.heard.add(i));
    r.unnamed.forEach((i) => x.unnamed.add(i));
    r.believed.forEach((i) => i !== 'anon' && x.believed.add(i));
    x.zones.add(r.E.zone);
  }
  for (const x of g.values()) {
    x.saw.forEach((i) => x.heard.delete(i));
    x.saw.forEach((i) => x.unnamed.delete(i));
    x.heard.forEach((i) => x.unnamed.delete(i));
  }
  return [...g.values()].filter((x) => x.E.kind !== 'noise' || x.unnamed.size).sort((a, b) => a.E.t - b.E.t);
}

const CHOICE = {
  wind: 'He is winding it down. The cabs stay; the rest stops.',
  take: 'He is taking it over. All of it.',
  silent: 'He would not say. The street has decided for him.',
};

export function summary() {
  const tg = truthGroups();
  let known = 0,
    right = 0,
    blind = 0;
  for (const x of tg) {
    const all = new Set([...x.saw, ...x.heard]);
    known += all.size;
    for (const i of all) {
      if (x.believed.has(i)) right++;
      else blind++;
    }
  }
  return { tg, known, right, blind };
}

export function endHTML() {
  const truth = G.settings.truthView !== false;
  const { tg, known, right, blind } = summary(),
    m = G.money,
    f = G.story.flags;
  const names = (s, n = 6) => {
    const a = [...s].map(real);
    return a.length > n ? a.slice(0, n).join(', ') + ' and ' + (a.length - n) + ' more' : a.join(', ');
  };
  const rows = tg
    .map((x) => {
      const all = new Set([...x.saw, ...x.heard]),
        miss = [...all].filter((i) => !x.believed.has(i)),
        wrong = [...x.believed].filter((i) => !all.has(i) && !x.unnamed.has(i));
      return `<tr><td><b>${esc(x.k.truth(Object.assign({}, x.E, { zone: listAnd([...x.zones]) })))}</b><br><small>${esc(whenTxt(x.E.t))}</small></td><td>${x.saw.size ? 'Saw or was there: ' + esc(names(x.saw)) + '.<br>' : ''}${x.heard.size ? 'Were told: ' + esc(names(x.heard)) + '.<br>' : ''}${x.unnamed.size ? x.unnamed.size + ' saw only a stranger, a coat or a cab.' : ''}${!all.size && !x.unnamed.size ? 'Nobody.' : ''}</td><td>${x.believed.size ? esc(names(x.believed)) : 'Nobody.'}</td><td class="gap">${miss.length ? 'Never knew: ' + esc(miss.map(real).slice(0, 7).join(', ')) + (miss.length > 7 ? ' and ' + (miss.length - 7) + ' more' : '') : ''}${wrong.length ? '<br>Wrongly feared: ' + esc(wrong.map(real).join(', ')) : ''}</td></tr>`;
    })
    .join('');
  const byStory = new Map();
  for (const t of G.transfers) {
    const E = G.ev[t.e];
    if (!E) continue;
    const k = gkey(E);
    if (!byStory.has(k)) byStory.set(k, { E, list: [] });
    byStory.get(k).list.push(t);
  }
  const told = [...byStory.values()]
    .sort((a, b) => b.list.length - a.list.length)
    .slice(0, 12)
    .map(
      (s) =>
        `<div class="entry"><b>${esc(KINDS[s.E.kind].truth(s.E))}</b> (${s.list.length} tellings)<br><small>${s.list
          .slice(0, 14)
          .map((t) => `${esc(real(t.a))} told ${esc(real(t.b))} (${esc(t.z || 'the street')}, ${stamp(t.t)})`)
          .join('; ')}${s.list.length > 14 ? '; and ' + (s.list.length - 14) + ' more' : ''}</small></div>`,
    )
    .join('');
  const calls = G.named
    .filter((p) => !p.def.police || p.mind.fam > 0)
    .map((p) => {
      const c = callName(p),
        mi = p.mind;
      return `<tr><td>${esc(p.def.name)}${p.dead ? ' (dead)' : ''}</td><td><b>${esc(c || 'nothing: does not know him')}</b></td><td>${mi.regard > 0.3 ? 'warm' : mi.regard < -0.3 ? 'cold' : mi.regard < -0.1 ? 'cooling' : 'undecided'}${mi.fear > 0.45 ? ', afraid' : ''}${mi.bought ? ', paid' : ''}${mi.stmtGiven ? ', went to the police' : ''}</td><td>${((n) => n + (n === 1 ? ' thing' : ' things'))(mi.mem.filter(attached).length)}</td></tr>`;
    })
    .join('');
  return `<div class="masthead">Meridian Evening Mail</div><p style="text-align:center;font-size:11px;letter-spacing:.1em">SATURDAY 20 OCTOBER 1990 · THE WEEK ON QUAY STREET</p>
  <h1>${esc(CHOICE[f.choice] || CHOICE.silent)}</h1>${
    truth
      ? `<p><b>Playtest view: the truth beside the Ledger.</b> This part shows what Tom could never know. It can be switched off in Settings.</p>
  <p>The street calls him <b>${esc(NAMES[townLevel()] || 'nothing yet')}</b>. Sheila Dunn calls him <b>${esc(callName(G.people.sheila))}</b>. The street knew ${known} ${known === 1 ? 'thing' : 'things'} about him by name. His Ledger had ${right} of them and missed ${blind}.</p>
  <h2>Playtest view: what the town truly knows, beside what his Ledger believed</h2><table><tr><th>What happened</th><th>The truth: who knows</th><th>His Ledger: who he thought knew</th><th>The gap</th></tr>${rows}</table>
  <h2>Playtest view: who told whom</h2><div>${told || 'Nobody told anybody anything. A quiet week.'}</div>
  <h2>Playtest view: what each person calls him</h2><table><tr><th>Person</th><th>Calls him</th><th>Feeling</th><th>Knows</th></tr>${calls}</table>`
      : '<p>The truth view is switched off in Settings: this page shows only what Tom knows.</p>'
  }
  <h2>Money</h2><p>Clean, from the fare book: ${money(m.earnedClean)} across ${m.fareCount} fares. Dirty, from the night: ${money(m.earnedDirty)}. Put through the book: ${money(m.washed)}${m.booksOff ? ', of which ' + money(m.booksOff) + ' the book could not hide' : ''}. In his pocket ${money(m.clean)}, in the tin ${money(m.dirty)}.${f.oweAgar ? ' He owes Agar & Co ' + money(f.oweAgar) + '.' : ''}</p>
  <h2>The week in numbers</h2><p>Talks ${G.stats.talks} (voiced live ${G.stats.live}, written lines ${G.stats.fallback}). Things said to his face ${G.stats.comebacks}. Tellings between people ${G.transfers.length}. Loudness at the end ${loudness().toFixed(1)}. Played ${Math.round(G.played / 60)} minutes.</p>
  <h2>Playtest: answer after playing</h2>${playtestFields()}
  <div class="row"><button class="btn" data-act="copy">Copy the whole report as text</button><button class="btn alt" data-act="measures">Playtest measures</button><button class="btn alt" data-act="notes">Design notes</button><button class="btn alt" data-act="new">New week</button><button class="btn alt" data-act="totitle">Title</button></div><textarea id="report" class="hidden" readonly></textarea><p id="copied" style="font-size:12px"></p>`;
}

export const QUESTIONS = [
  'Did it feel like the town was watching and talking?',
  'Was being talked about fun or just noise?',
  'Did any line said to my face surprise me?',
  'Did the night jobs and the day life pull against each other?',
  'Was the live talk believable and in character?',
  "What did I want to do that I couldn't?",
];

export function playtestFields() {
  const a = G.story.playtest || [];
  return QUESTIONS.map(
    (q, i) => `<p><b>${i + 1}. ${q}</b></p><textarea data-pt="${i}">${esc(a[i] || '')}</textarea>`,
  ).join('');
}

export function reportText() {
  const { tg, known, right, blind } = summary(),
    m = G.money,
    f = G.story.flags,
    L = [];
  L.push(
    'LEDGER browser prototype: run report',
    `Ended ${stamp(G.story.endT || G.t)}. Played ${Math.round(G.played / 60)} min. Choice: ${f.choice || 'none yet'}. Street calls him: ${NAMES[townLevel()] || 'nothing'}. Sheila calls him: ${callName(G.people.sheila)}.`,
    `Flags: ${Object.keys(f)
      .filter((k) => typeof f[k] !== 'object')
      .map((k) => k + '=' + f[k])
      .join(', ')}`,
    `Money: clean earned ${money(m.earnedClean)} (${m.fareCount} fares), dirty earned ${money(m.earnedDirty)}, washed ${money(m.washed)}, book out by ${money(m.booksOff)}, pocket ${money(m.clean)}, tin ${money(m.dirty)}.`,
    `Talks ${G.stats.talks}: live ${G.stats.live}, written ${G.stats.fallback}. Said to face ${G.stats.comebacks}. Tellings ${G.transfers.length}. Loudness ${loudness().toFixed(2)}. Known ${known}, Ledger right ${right}, missed ${blind}.`,
    `Town's eyes (testing only): ${G.settings.eyes ? 'ON' : 'off'} at the end; on for ${((G.stats.eyesSecs || 0) / 60).toFixed(1)} min of play in all.`,
    `Ledger opened ${G.stats.ledgerOpens || 0} times. Talk slip: shown at the start of ${G.stats.slipShown || 0} talks, folded or opened by key ${G.stats.slipOpened || 0} times. Suggested lines: opened with Tab ${G.stats.linesOpened || 0} times, said ${G.stats.linesSaid || 0}, own words typed ${G.stats.typed || 0}. Model follow-ups offered ${G.stats.sugLive || 0}, dropped by the checks or the six seconds ${G.stats.sugDropped || 0}. Noted lines shown ${G.stats.noted || 0}.`,
    '',
    'TRUTH vs LEDGER',
  );
  for (const x of tg)
    L.push(
      `- ${x.k.truth(x.E)} [${whenTxt(x.E.t)}] | saw: ${[...x.saw].map(real).join(', ') || 'none'} | told: ${[...x.heard].map(real).join(', ') || 'none'} | unnamed: ${x.unnamed.size} | ledger believed: ${[...x.believed].map(real).join(', ') || 'none'}`,
    );
  L.push('', 'WHAT EACH PERSON CALLS HIM');
  for (const p of G.named)
    L.push(
      `- ${p.def.name}: ${callName(p) || 'nothing'} (fam ${p.mind.fam.toFixed(2)}, regard ${p.mind.regard.toFixed(2)}, fear ${p.mind.fear.toFixed(2)}, knows ${p.mind.mem.filter(attached).length})`,
    );
  L.push('', 'WHO TOLD WHOM');
  for (const t of G.transfers.slice(-160)) {
    const E = G.ev[t.e];
    L.push(
      `- ${stamp(t.t)} ${real(t.a)} > ${real(t.b)} @ ${t.z || 'street'}: ${E ? KINDS[E.kind].truth(E) : '?'}`,
    );
  }
  L.push('', 'PLAYTEST ANSWERS');
  QUESTIONS.forEach((q, i) =>
    L.push(`${i + 1}. ${q}`, '   ' + ((G.story.playtest || [])[i] || '(no answer)')),
  );
  L.push('', 'EVENT LOG');
  for (const e of G.log.slice(-220)) L.push(`${stamp(e.t)} [${e.tag}] ${e.text}`);
  return L.join('\n');
}

export const playtestHTML = () =>
  `<h1>Playtest</h1><p>Answer after playing. Your answers are saved with the week and go into the copied report.</p>${playtestFields()}<div class="row"><button class="btn" data-act="copy">Copy the run report with these answers</button><button class="btn alt" data-act="back">Back</button></div><textarea id="report" class="hidden" readonly></textarea><p id="copied" style="font-size:12px"></p>`;

// ---------- the Measures screen ----------
// The Ledger screen test's measures, in words and plain numbers, with the one JSON file to export.
export function measuresHTML() {
  const m = measures(),
    v = (x, unit = '') => (x == null ? 'not yet' : x + unit),
    yes = (x) => (x ? 'yes' : 'no'),
    pc = (x) => (x == null ? 'not yet' : Math.round(x * 100) + ' in 100'),
    row = (a, b) => `<tr><td>${esc(a)}</td><td><b>${esc(String(b))}</b></td></tr>`,
    dev = (d) =>
      `${d.found} of ${d.asked} found${d.medianRealSecondsFromOpenToEntry != null ? ', middle time ' + d.medianRealSecondsFromOpenToEntry + ' seconds from open to the entry' : ''}`;
  const asks = m.findTheFact.asks
    .map((a) =>
      row(
        a.question,
        a.state === 'not asked'
          ? 'not asked: ' + a.why
          : a.state === 'asked'
            ? 'on the table now'
            : (a.found
                ? `found by ${a.device} in ${v(a.realSecondsFromOpenToEntry, ' seconds')} from open`
                : `not found (${a.device})`) + (a.wrongMarks ? `, ${a.wrongMarks} wrong marks` : ''),
      ),
    )
    .join('');
  return `<h1>Playtest measures</h1><p>The Ledger screen test. Measured for this week so far, saved with it, and exported as one JSON file. Times are real seconds.</p>
  <table>
  ${row('Ledger opens per hour of play', v(m.ledgerOpensPerHourOfPlay) + ` (${m.ledgerOpens} opens in ${Math.round(m.realSecondsPlayed / 60)} minutes)`)}
  ${row('Middle time open per visit', v(m.medianRealSecondsOpenPerVisit, ' seconds'))}
  ${row('Find the fact, keyboard', dev(m.findTheFact.keyboard))}
  ${row('Find the fact, pad', dev(m.findTheFact.pad))}
  ${row('Talks with the slip unfolded', pc(m.shareOfTalksWithTheSlipUnfolded) + ` (${m.talks} talks)`)}
  ${row('Noted lines followed by an open within 60 seconds', pc(m.shareOfNotedLinesFollowedByAnOpenWithin60Seconds) + ` (${m.notedLinesShown} shown)`)}
  ${row('Tab pressed in the first hour', yes(m.tabPressedInTheFirstHour) + (m.firstTabAtRealSecondsPlayed != null ? `, first at ${Math.round(m.firstTabAtRealSecondsPlayed / 60)} minutes` : ''))}
  ${row('Lines said per Tab open', v(m.linesSaidPerTabOpen) + ` (${m.linesSaidFromSuggestions} lines, ${m.tabOpens} opens)`)}
  ${row('Turns from suggestions', pc(m.shareOfTurnsFromSuggestions) + ` (${m.turnsTyped} typed)`)}
  ${row('Entries struck through this week', m.entriesStruckThroughThisWeek + ` of ${m.entries}`)}
  ${row('Entries with no source event (must be none)', m.entriesWithNoSourceEvent === 0 ? 'none' : m.entriesWithNoSourceEvent)}
  </table>
  <h2>The asks</h2><table>${asks || row('No ask has come up yet', 'the first is on Tuesday at 9.30am')}</table>
  <div class="row"><button class="btn" id="mexport">Export as one JSON file</button><button class="btn alt" id="mcopy">Copy the JSON</button><button class="btn alt" data-act="back">Back</button></div><p id="mmsg" style="font-size:12px"></p>
  <textarea id="mjson" class="hidden" readonly style="width:100%;height:220px;margin-top:10px;font:12px 'Courier Prime',monospace"></textarea>`;
}
