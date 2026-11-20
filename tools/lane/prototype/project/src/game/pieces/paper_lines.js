// Rule piece: the paper (DESIGN section 11 "the press works only through a person", ADDENDUM A19). The local page
// carries only what Alison Sedman saw or was told, at the strength she had it. ER-PAPER-01: every printed line
// traces to one of her memories. Pure.
//
// knows: [{ e: event id, kind, src: 'saw' | 'told' | 'self' | 'heard', sure: 0..1, named: bool, crime: 0..4,
//           sev: 0..1, words: what happened in plain words, place, t: game minute, printed: bool }]
// Returns the edition: [{ e, text, strength: 'fact' | 'said' | 'rumour', names: bool }], gravest first, at most n.
function edition(knows, n, t) {
  const fit = knows
    .filter((k) => !k.printed && k.src !== 'heard' && k.sev >= t.printsFromNewsworthy && k.sure >= t.printsFromSure)
    .sort((a, b) => b.crime - a.crime || b.sev - a.sev || a.e - b.e)
    .slice(0, n);
  return fit.map((k) => {
    const strength = k.src === 'saw' || k.src === 'self' ? 'fact' : k.sure >= t.saidFromSure ? 'said' : 'rumour';
    const names = !!k.named && strength === 'fact' && k.sure >= t.namesFromSure && k.crime < t.neverNamesFromCrime;
    const who = names ? 'Mr T. Nowak, of Quay Street,' : k.named && strength !== 'rumour' ? 'a Quay Street businessman' : 'a man';
    const lead = strength === 'fact' ? '' : strength === 'said' ? 'It is said on the Hook that ' : 'There is talk, which this paper cannot confirm, that ';
    const body = k.words.replace(/^Tom\b|^He\b/, who).replace(/\bTom\b/g, who);
    const text = lead ? lead + body.charAt(0).toLowerCase() + body.slice(1) : body.charAt(0).toUpperCase() + body.slice(1);
    return { e: k.e, text: text.replace(/\.?$/, '.'), strength, names };
  });
}
// The check itself: every line's event is among what she knows first-hand or was told.
function traces(lines, knows) {
  return lines.every((l) => knows.some((k) => k.e === l.e && k.src !== 'heard'));
}
// A reader takes a printed line at the strength it was written (how sure the reader is afterwards).
function readerSure(line, t) {
  return { fact: t.readerSureOfFact, said: t.readerSureOfSaid, rumour: t.readerSureOfRumour }[line.strength];
}
export const PIECE = { name: 'paper_lines', fns: { edition, traces, readerSure } };
