// LEDGER, the whole game: the system "feel". Teaching without a tutorial and the first hour's lead (DESIGN 15, 17;
// parts 6.5, 7.1, 7.12, 6.1.4, 8.4.1, 7.10): every hint fires the first time it can mean something or when the
// player hesitates, each once, never two within twelve seconds; Ron or Pauline nudge after a minute of standing
// about; sounds are shown in words for players who cannot hear them (an assist, off by default); assists change
// only their own thing. The camera and turn faults measured on 20 Nov are mended in player.js from tune/feel.js.
import { register, X, tell, hourNow, dayNow, here, P_, on } from './core.js';
import { G } from '../state.js';
import { sub } from '../ui.js';
import { RULES } from '../rules.js';

const T = RULES.game.feel;
const S = { lastHintPlayed: -99, idle: 0, about: 0 };

// A first hint: once, only if hints are on, never two within twelve seconds (ER-FIRST-03).
export function hint(id, text) {
  const x = X('feel');
  if (x.hints[id] || G.settings.hints === false || G.played - S.lastHintPlayed < T.hintsNotTwoWithinRealSeconds + 1) return false;
  x.hints[id] = Math.round(G.played);
  S.lastHintPlayed = G.played;
  sub(text, '', 'over', 7);
  return true;
}
// Sound shown (A6, 8.4.1): a short word when he makes a loud noise or the street goes quiet. What he hears, never what anybody knows.
export function soundShown(word) {
  if (!G.settings.soundShown) return false;
  X('feel').captions.push({ word, t: Math.round(G.t) });
  sub('[' + word + ']', '', 'over', 3);
  return true;
}
// The assists (A6): each changes only its own thing, all off by default.
export const ASSISTS = { seeingOutline: 'eyes', slowerFights: 'slowFights', drivingHelp: 'driveHelp', longerWalks: 'longWalks', hintsAgain: 'hintsAgain', soundShown: 'soundShown' };
export const assistOn = (name) => !!G.settings[ASSISTS[name]];

register({
  id: 'feel',
  fresh: () => ({ hints: {}, captions: [], nudges: 0, firstFareSaid: false }),
  loaded(x) {
    // a new game or a loaded one starts its own count: nothing of the game before it holds a hint back
    S.idle = 0;
    S.about = 0;
    S.sinceStart = 0;
    S.lastHintPlayed = Math.max(-99, ...Object.values(x.hints || {}).map((v) => +v || 0));
  },
  step(dt) {
    if (G.paused || G.story.phase !== 'play') return;
    const t = G.tom,
      x = X('feel');
    // a hint only on hesitation: standing still four seconds, with nothing open, the first time
    S.idle = t.still > T.hintAfterStandingStillRealSeconds && !t.inCar ? S.idle + dt : 0;
    // the hands-on run's fault: a newcomer who never stood still was never told the keys. The first hint comes a few
    // seconds after he has control, whatever he is doing; the rest still wait for a pause.
    S.sinceStart = (S.sinceStart || 0) + dt;
    if (S.idle > 0 && !x.hints.move) hint('move', 'W A S D to walk. The mouse looks about. Shift runs. L opens the Ledger.');
    else if (S.idle > 0 && !x.hints.keys && x.hints.move && x.hints.way) hint('keys', 'E uses what is in front of him. N is his watch. M is street manners. Comma is the paper map. Full stop is how things stand.');
    // Ron or Pauline nudge after a minute of standing about (DESIGN 15, teaching)
    S.about = t.still > 1 && !t.inCar && G.story.objective ? S.about + dt : 0;
    if (S.about > T.nudgeAfterStandingAboutRealSeconds) {
      S.about = 0;
      const P = [P_('ron'), P_('pauline'), P_('sheila')].find((Q) => Q && here(Q, RULES.game.ledgerx.remarkWithinMetres * 2));
      if (P && x.nudges < 6) {
        x.nudges++;
        sub(G.story.objective, P.def.name, '', 6);
      }
    }
    // the first verbs, each named the first time it can mean something
    if (t.inCar && !x.hints.car) hint('car', 'W and S drive, A and D steer, Space is the handbrake. H is the horn, B looks back, R has Pauline say the way again.');
    if (!t.inCar && t.light < RULES.game.foot.stillInDoorwayLightAtMost && hourNow() > 20 && !x.hints.dark) hint('dark', 'In the dark, standing still is the hiding. Z held walks slowly and quietly. B sits or leans, like a man with a reason to be there.');
    if (G.x.crime.pockets.length && !x.hints.pockets) hint('pockets', 'Two things under the coat is all it hides. The rest goes in the locked drawer at the office.');
    // the first hour: once Sheila has shown him round, Pauline has a fare and no car (DESIGN 15, minute 2:30)
    if (G.story.flags.tour && !x.firstFareSaid && dayNow() === 0 && !G.story.fare) {
      x.firstFareSaid = true;
      sub('"I have Father Walsh wanting the priest\'s house and no car in. Car two is on the rank, love, if you can drive."', 'Pauline, at the radio', '', 8);
      G.story.fareCool = 0;
      if (!/Darren|Ron|bag|landing/.test(G.story.objective || '')) G.story.objective = 'Car two is on the rank outside. Father Walsh wants the priest\'s house, by the chapel. [F] gets in.';
    }
  },
  hook: {
    x: () => X('feel'),
    hint,
    soundShown,
    assists: () => Object.fromEntries(Object.keys(ASSISTS).map((k) => [k, assistOn(k)])),
    bands: () => ({ fightCameraMetres: T.fightCameraMetres, cabCameraBackMetres: T.cabCameraBackMetres, cabCameraUpMetres: T.cabCameraUpMetres, cabViewAcrossAtRestDegrees: T.cabViewAcrossAtRestDegrees, cabViewAcrossAt30MphDegrees: T.cabViewAcrossAt30MphDegrees }),
  },
});
// sounds shown in words, for the loud things he does himself and the quiet of a street that has noticed
on('crime.damage', () => soundShown('glass breaking'));
on('crime.bark', () => soundShown('a dog barking'));
on('crime.entered', (e) => e.how === 'force' && soundShown('a door forced'));
