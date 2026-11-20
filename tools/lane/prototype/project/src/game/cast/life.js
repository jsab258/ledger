// New people of the system "life", in the shape of cast.js CAST entries. Both are named by the design: Philip Danby
// (canon's day-life ring, the teacher with the school shut) and the retired doctor on the terrace (ADDENDUM A21).
import { PEOPLE, SCHEDULES } from '../tune/life.js';
const week = (id) => SCHEDULES[id].map((r) => (r.doing !== undefined ? [r.fromHour, r.place, r.doing] : [r.fromHour, r.place]));
const num = (id) => ({ age: PEOPLE[id].ageYears, nerve: PEOPLE[id].nerveZeroToOne, venal: PEOPLE[id].venalZeroToOne, talk: PEOPLE[id].talkativeZeroToOne, discretion: PEOPLE[id].discretionZeroToOne });
export const CAST_ADD = [
  Object.assign(
    {
      id: 'danby',
      name: 'Philip Danby',
      sex: 'm',
      role: 'a teacher, with the school shut',
      desc: 'a man with a library book',
      voice: 'plain',
      upright: 1,
      local: true,
      homeSpot: 'clhome',
      close: ['walsh', 'grace'],
      look: { h: 1.79, b: 0.35, skin: 0, hair: ['short', '#5b4a3a'], top: ['duffel', '#4b5a3c', '#c9c2a8'], bot: ['trousers', '#5a5248'], x: ['glasses'] },
      sched: week('danby'),
      card: {
        who: 'A teacher at the Board School until it shut. He stayed on Chapel Lane when the work went. He reads, walks, and helps Father Walsh with the hall.',
        speak: 'Mild, exact, a little amused. Says what he thinks and then waits. Never raises his voice.',
        lines: ['I was told you were the nephew. I try not to be told things, but there it is.'],
        life: 'Born on Chapel Lane. Takes one pot of tea at the Copper Kettle of a morning and sits by the chapel in the afternoon.',
        fire: 'He saw the glow from his window and nothing else. He thinks the street knows more than it says.',
        rivals: 'He taught half of Cammack\'s lads and none of them listened.',
      },
    },
    num('danby'),
  ),
  Object.assign(
    {
      id: 'calvert',
      name: 'Dr Calvert',
      sex: 'm',
      role: 'a retired doctor',
      desc: 'an old man in a cardigan',
      voice: 'dry',
      upright: 0,
      nostmt: 1,
      local: true,
      homeSpot: 'busstop',
      close: ['ada'],
      look: { h: 1.72, b: 0.4, skin: 2, hair: ['balding', '#cfcfcf'], top: ['cardigan', '#6a5a4a', '#d8d0bd'], bot: ['trousers', '#4a4640'], x: ['glasses'] },
      sched: week('calvert'),
      card: {
        who: 'A doctor, retired these six years, on the terrace side of Quay Street. He stitches without asking, for money, and he remembers.',
        speak: 'Brief. Asks nothing. Says what it will cost and what to keep dry.',
        lines: ['Sit. Hold that. I do not want to know.'],
        life: 'Forty years the dock\'s doctor. Lives alone behind the brass bell pull.',
        fire: 'Nobody came to him the night No. 4 burned. He noticed that.',
        rivals: 'He has stitched men of all three and sent the same bill.',
      },
    },
    num('calvert'),
  ),
];
