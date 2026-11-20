// New people of the system "crew", in the shape of cast.js CAST entries. Canon names only (DESIGN 12, 13, 16); a rival's
// man at a door is described and has a first name and no more.
import { PEOPLE as P, SCHEDULES as S } from '../tune/crew.js';
const week = (id) => S[id].map((r) => (r.doing !== undefined ? [r.fromHour, r.place, r.doing] : [r.fromHour, r.place]));
export const CAST_ADD = [
  {
    id: 'megginson',
    name: 'Ian Megginson',
    age: P.megginson.ageYears,
    sex: 'm',
    role: 'locksmith and key cutter',
    desc: 'the key cutter at the corner',
    voice: 'plain',
    nerve: P.megginson.nerveZeroToOne,
    venal: P.megginson.venalZeroToOne,
    talk: P.megginson.talkativeZeroToOne,
    discretion: P.megginson.discretionZeroToOne,
    close: [],
    look: { h: 1.72, b: 0.5, skin: 0, hair: ['balding', '#4a4038'], top: ['apron', '#3a4a3a', '#888888'], bot: ['trousers', '#3a3a3a'], x: ['glasses'] },
    sched: week('megginson'),
    card: {
      who: 'Ian Megginson cuts keys and mends locks from a booth at the corner. He has fitted or opened every lock on the street.',
      speak: 'Careful, literal, answers the question asked and no other.',
      lines: ['There is not a lock on this street I have not had in my hand.'],
      life: 'Fifty-one. His father had the booth.',
      fire: 'He changed the lock on No. 4 a month before it burned, and was paid in cash.',
      rivals: 'He cuts keys for anybody with a docket.',
    },
  },
  {
    id: 'karen',
    name: 'Karen Grummitt',
    age: P.karen.ageYears,
    sex: 'f',
    role: 'at the ferry kiosk',
    desc: 'the woman at the ferry kiosk',
    voice: 'plain',
    nerve: P.karen.nerveZeroToOne,
    venal: P.karen.venalZeroToOne,
    talk: P.karen.talkativeZeroToOne,
    discretion: P.karen.discretionZeroToOne,
    close: [],
    look: { h: 1.64, b: 0.4, skin: 0, hair: ['perm', '#7a4a2a'], top: ['anorak', '#2a5a7a', '#dddddd'], bot: ['jeans', '#39445a'], x: ['earrings'] },
    sched: week('karen'),
    card: {
      who: 'Karen Grummitt sells tickets and tea at the ferry kiosk. She sees every face that comes off the boat and every car that meets it.',
      speak: 'Quick, friendly, counts people without meaning to.',
      lines: ['Last boat is half ten. After that it is only people who have a reason.'],
      life: 'Thirty-four. Her hours were cut in the summer.',
      fire: 'The night it burned the last ferry was met by a car she knew.',
      rivals: "The Widow's men use the landing. She serves them like anybody.",
    },
  },
];
