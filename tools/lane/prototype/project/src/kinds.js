// Every kind of thing the town can know about Tom.
// sev: how newsworthy (0..1). val: how it reads, -1 menace .. +1 decent. crime: 0 none, 1 minor, 2 violence, 3 killing.
import { DAYS, hourWords } from './util.js';
import { RULES } from './rules.js';
const TIME = RULES.time;
const KN = RULES.kinds;

export function whenTxt(t) {
  const d = Math.floor(t / 1440),
    h = (t % 1440) / 60;
  const part =
    h < TIME.smallHoursUntilHour
      ? 'in the small hours'
      : h < TIME.morningUntilHour
        ? 'morning'
        : h < TIME.afternoonUntilHour
          ? 'afternoon'
          : h < TIME.eveningUntilHour
            ? 'evening'
            : 'night';
  return DAYS[d % 7] + ' ' + part;
}
export const whenShort = (t) => DAYS[Math.floor(t / 1440) % 7] + ', ' + hourWords((t % 1440) / 60);

// The numbers of each kind are in rules.js under kinds: how newsworthy, how it reads, and how grave a crime.
const K = (id, truth, mine, o = {}) =>
  Object.assign(
    {
      sev: KN[id].newsworthyZeroToOne,
      val: KN[id].readsMinusOneMenaceToOneDecent,
      crime: KN[id].crimeLevel,
      truth,
      mine,
    },
    o,
  );
const n = (e) => e.name || 'someone';

export const KINDS = {
  inherit: K(
    'inherit',
    () => 'Mickey Suddaby left the cab office to his nephew, Tom Nowak',
    () => "Inherited Mickey's. The street knows whose nephew Tom is",
    { noself: true },
  ),
  arrive: K(
    'arrive',
    () => 'Tom got off the bus on Quay Street with one suitcase',
    () => 'Got off the bus with one suitcase',
  ),
  night_out: K(
    'night_out',
    (e) => `Tom was out on ${e.zone} in the small hours`,
    (e) => `Out on ${e.zone} in the small hours`,
  ),
  coat_day: K(
    'coat_day',
    (e) => `Tom wore the runner's coat in daylight on ${e.zone}`,
    (e) => `Wore the coat in daylight on ${e.zone}`,
  ),
  ran: K(
    'ran',
    (e) => `Tom ran hard along ${e.zone} after dark`,
    (e) => `Ran along ${e.zone} after dark`,
  ),
  parcel: K(
    'parcel',
    (e) => `Tom carried a holdall along ${e.zone} at night`,
    (e) => `Carried the bag along ${e.zone}`,
  ),
  pickup: K(
    'pickup',
    (e) => `Tom lifted a holdall at ${e.zone}`,
    (e) => `Lifted the bag at ${e.zone}`,
  ),
  drop: K(
    'drop',
    (e) => `Tom handed a holdall in at ${e.zone}`,
    (e) => `Handed the bag in at ${e.zone}`,
  ),
  cab_drive: K(
    'cab_drive',
    () => "Tom drives one of Mickey's cars himself",
    () => 'Drove the cab',
  ),
  cab_night: K(
    'cab_night',
    (e) => `One of Mickey's cars was on ${e.zone} late`,
    (e) => `Had the cab on ${e.zone} late`,
  ),
  fare: K(
    'fare',
    (e) => `Tom drove ${n(e)} ${e.dest || 'across town'}`,
    (e) => `Drove ${n(e)} ${e.dest || 'across town'}`,
  ),
  free_ride: K(
    'free_ride',
    (e) => `Tom would not take ${n(e)}'s fare money`,
    (e) => `Let ${n(e)} ride for nothing`,
  ),
  job_yes: K(
    'job_yes',
    () => "Tom took on Mickey's night arrangement",
    () => 'Said yes to the night work',
  ),
  job_no: K(
    'job_no',
    () => 'Tom told the outfit no',
    () => 'Told them no',
  ),
  no_show: K(
    'no_show',
    () => 'Tom never turned up for the night work',
    () => 'Never turned up for the night work',
  ),
  tea: K(
    'tea',
    () => "Tom took his tea at Ada's",
    () => "Took tea at Ada's",
  ),
  tea_late: K(
    'tea_late',
    () => "Tom came late to Ada's tea with his knuckles marked",
    () => "Came late to Ada's tea",
  ),
  tea_snub: K(
    'tea_snub',
    () => 'Tom left Ada sat waiting with the good cups out',
    () => 'Left Ada waiting',
  ),
  chapel: K(
    'chapel',
    () => 'Tom sat a while in the chapel where they buried his uncle from',
    () => 'Sat a while in the chapel',
  ),
  talk_ellis: K(
    'talk_ellis',
    (e) => `Tom was seen talking with DS Ellis on ${e.zone}`,
    (e) => `Talked with Ellis on ${e.zone}`,
  ),
  talk_press: K(
    'talk_press',
    (e) => `Tom was seen talking with the reporter, Alison Sedman, on ${e.zone}`,
    (e) => `Talked with the reporter on ${e.zone}`,
  ),
  asked_fire: K(
    'asked_fire',
    (e) => `Tom asked ${n(e)} about the warehouse fire`,
    (e) => `Asked ${n(e)} about the fire`,
  ),
  stare: K(
    'stare',
    (e) => `Tom stared ${n(e)} down on ${e.zone}`,
    (e) => `Stared ${n(e)} down`,
    { grudge: 1 },
  ),
  squareup: K(
    'squareup',
    (e) => `Tom squared up to ${n(e)} on ${e.zone}`,
    (e) => `Squared up to ${n(e)}`,
    { grudge: 1 },
  ),
  threat: K(
    'threat',
    (e) => `Tom threatened ${n(e)} on ${e.zone}`,
    (e) => `Threatened ${n(e)}`,
    { grudge: 1, loud: 1 },
  ),
  shove: K(
    'shove',
    (e) => `Tom laid hands on ${n(e)} on ${e.zone}`,
    (e) => `Laid hands on ${n(e)}`,
    { grudge: 1, loud: 1 },
  ),
  strike: K(
    'strike',
    (e) => `Tom struck ${n(e)} on ${e.zone}`,
    (e) => `Hit ${n(e)}`,
    { grudge: 1, loud: 1 },
  ),
  weapon_out: K(
    'weapon_out',
    (e) => `Tom pulled a ${e.weapon || 'weapon'} on ${n(e)} on ${e.zone}`,
    (e) => `Pulled the ${e.weapon || 'weapon'} on ${n(e)}`,
    { grudge: 1, loud: 1 },
  ),
  weapon_used: K(
    'weapon_used',
    (e) => `Tom used a ${e.weapon || 'weapon'} on ${n(e)} on ${e.zone}`,
    (e) => `Used the ${e.weapon || 'weapon'} on ${n(e)}`,
    { grudge: 1, loud: 1 },
  ),
  kill: K(
    'kill',
    (e) => `Tom killed ${n(e)} on ${e.zone}`,
    (e) => `Killed ${n(e)}`,
    { loud: 1, forever: 1 },
  ),
  set_on: K(
    'set_on',
    (e) => `Tom was set on by ${n(e)} on ${e.zone} and stood his ground`,
    (e) => `Was set on by ${n(e)}`,
    { loud: 1 },
  ),
  beaten: K(
    'beaten',
    (e) => `Tom took a beating on ${e.zone}`,
    (e) => `Took a beating on ${e.zone}`,
    { loud: 1 },
  ),
  patched: K(
    'patched',
    () => 'Grace Rinaldi patched Tom up in the caff kitchen',
    () => "Patched up in Grace's kitchen",
  ),
  debt_paid: K(
    'debt_paid',
    (e) => `Tom collected what ${n(e)} owed Mickey's book`,
    (e) => `Collected from ${n(e)}`,
  ),
  debt_forgive: K(
    'debt_forgive',
    (e) => `Tom struck ${n(e)}'s debt out of Mickey's book`,
    (e) => `Struck ${n(e)}'s debt out of the book`,
  ),
  paid_info: K(
    'paid_info',
    (e) => `Tom pays ${n(e)} for what the street sees`,
    (e) => `Paid ${n(e)} for what he sees`,
  ),
  bribe_try: K(
    'bribe_try',
    (e) => `Tom tried to put money in ${n(e)}'s hand`,
    (e) => `Tried to put money in ${n(e)}'s hand`,
    { grudge: 1 },
  ),
  lied: K(
    'lied',
    (e) => `Tom lied to ${n(e)}'s face about something they saw`,
    (e) => `Lied to ${n(e)} and was caught`,
    { grudge: 1 },
  ),
  good_word: K(
    'good_word',
    () => 'Darren Milner has been saying the new owner is all right',
    () => 'Darren puts a good word about',
    { noself: true },
  ),
  arrested: K(
    'arrested',
    (e) => `Tom was taken in by the police from ${e.zone}`,
    (e) => `Was taken in from ${e.zone}`,
  ),
  ran_police: K(
    'ran_police',
    (e) => `Tom ran from the police on ${e.zone}`,
    (e) => `Ran from the police`,
    { loud: 1 },
  ),
  bag_taken: K(
    'bag_taken',
    (e) => `A constable stopped Tom with a bag on ${e.zone} and took it`,
    (e) => `The constable took the bag on ${e.zone}`,
    { loud: 1 },
  ),
  ellis_asked: K(
    'ellis_asked',
    () => 'DS Ellis came down Quay Street asking about Tom',
    () => 'Ellis has been asking the street about Tom',
    { noself: true },
  ),
  wash: K(
    'wash',
    () => "Mickey's fare book has stopped adding up since Tom came",
    () => 'Put too much through the fare book',
    { priv: 1 },
  ),
  rent_paid: K(
    'rent_paid',
    () => 'Tom paid Sylvia Rennison her rent on the Friday',
    () => 'Paid the rent on Friday',
  ),
  rent_late: K(
    'rent_late',
    () => "Tom was short with Sylvia Rennison's rent on Friday",
    () => 'Was short with the rent',
  ),
  knocked: K(
    'knocked',
    (e) => `Tom knocked ${n(e)} down with the cab on ${e.zone}`,
    (e) => `Knocked ${n(e)} down with the cab`,
    { grudge: 1, loud: 1 },
  ),
  crash: K(
    'crash',
    (e) => `Tom put the cab into something on ${e.zone}`,
    (e) => `Put the cab into something on ${e.zone}`,
    { loud: 1 },
  ),
  noise: K(
    'noise',
    (e) => `Somebody was heard about on ${e.zone} in the small hours`,
    (e) => `Made a noise on ${e.zone} in the small hours`,
    { noself: true },
  ),
  choice_wind: K(
    'choice_wind',
    () => "Tom is winding Mickey's arrangements down",
    () => 'Told Sheila: winding it down, just the cabs',
  ),
  choice_take: K(
    'choice_take',
    () => "Tom is taking Mickey's arrangements over",
    () => 'Told Sheila: taking it on, all of it',
  ),
  choice_silent: K(
    'choice_silent',
    () => 'Tom would not tell Sheila Dunn which it is going to be',
    () => 'Would not tell Sheila which',
  ),
  // Not an act of Tom's: something he was told, read or noticed. It is in the event log only so that every
  // line in his Ledger has a source event. Nobody witnesses it and nobody passes it on.
  word: K(
    'word',
    (e) => e.text || 'Tom was told something',
    (e) => e.text || 'Was told something',
    { noself: true, priv: true, word: true },
  ),
};
export const NAMES = ['', 'the new owner', 'Nowak', 'Tom', 'Tommy'];
