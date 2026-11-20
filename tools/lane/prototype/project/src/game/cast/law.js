// New people of the system "law": the two officers who can be paid (addendum A13). The station as a whole never
// changes; whether DS Ellis can be bought is not decided here.
import { PEOPLE } from '../tune/law.js';
const officer = (id, name, role, look, card) => ({
  id, name, age: PEOPLE[id].ageYears, sex: 'm', role, desc: role === 'police sergeant' ? 'a police sergeant' : 'a constable',
  voice: 'official', nerve: PEOPLE[id].nerveZeroToOne, venal: PEOPLE[id].venalZeroToOne, talk: PEOPLE[id].talkativeZeroToOne,
  discretion: PEOPLE[id].discretionZeroToOne, local: false, police: 1, nostmt: 1, look,
  sched: [[0, 'off']], card,
});
export const CAST_ADD = [
  officer('pashby', 'PC Pashby', 'police constable', { h: 1.78, b: 0.7, skin: 0, hair: ['helmet', '#14161c'], top: ['tunic', '#14161c', '#c9c9c9'], bot: ['trousers', '#14161c'], x: [] }, {
    who: 'A police constable of twenty years who walks the Hook beat on alternate nights.',
    speak: 'Slow, friendly, tired. Calls Tom "son".',
    lines: ["Cold night for it, son. I'd get indoors."],
    life: 'Twenty years in uniform and two years off his pension.',
    fire: 'Before his week on nights. He would not say.',
    rivals: 'He knows the names and keeps them to himself.',
  }),
  officer('thwaite', 'Sergeant Thwaite', 'police sergeant', { h: 1.8, b: 0.8, skin: 0, hair: ['short', '#77736c'], top: ['tunic', '#14161c', '#c9c9c9'], bot: ['trousers', '#14161c'], x: [] }, {
    who: 'The desk sergeant at the town station. He smokes outside its door at dinner time.',
    speak: 'Dry, unhurried. Says little and means all of it.',
    lines: ['Paper goes astray in a station. Now and then.'],
    life: 'Thirty years in. He keeps the book of statements.',
    fire: "CID's business. He would not know.",
    rivals: 'He has booked all three firms in his time.',
  }),
];
