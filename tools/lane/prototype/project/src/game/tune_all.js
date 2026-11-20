// The whole game's numbers, one file a system under tune/, merged into the one tuning table as RULES.game.<id>.
import * as town from './tune/town.js';
import * as feel from './tune/feel.js';
import * as hour1 from './tune/hour1.js';
import * as foot from './tune/foot.js';
import * as fightx from './tune/fightx.js';
import * as cars from './tune/cars.js';
import * as fares from './tune/fares.js';
import * as jobsx from './tune/jobsx.js';
import * as crime from './tune/crime.js';
import * as life from './tune/life.js';
import * as shops from './tune/shops.js';
import * as way from './tune/way.js';
import * as law from './tune/law.js';
import * as acts from './tune/acts.js';
import * as endings from './tune/endings.js';
import * as ledgerx from './tune/ledgerx.js';
import * as crew from './tune/crew.js';
import * as rivals from './tune/rivals.js';
import * as rise from './tune/rise.js';
import * as firm from './tune/firm.js';
import * as dial from './tune/dial.js';
import * as econ from './tune/econ.js';
const ALL = { town, feel, hour1, foot, fightx, cars, fares, jobsx, crime, life, shops, way, law, acts, endings, ledgerx, crew, rivals, rise, firm, dial, econ };
export const TUNE = {};
export const TUNE_SCHEDULES = {};
export const TUNE_PEOPLE = {};
for (const id in ALL) {
  TUNE[id] = ALL[id].TUNE;
  Object.assign(TUNE_SCHEDULES, ALL[id].SCHEDULES || {});
  Object.assign(TUNE_PEOPLE, ALL[id].PEOPLE || {});
}
