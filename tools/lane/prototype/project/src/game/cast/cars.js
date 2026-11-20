// New people of the system "cars", in the shape of cast.js CAST entries (numbers from this system's tune PEOPLE).
import { PEOPLE } from '../tune/cars.js';
export const CAST_ADD = [
  {
    id: 'nev',
    name: 'Neville Stather',
    age: PEOPLE.nev.ageYears,
    sex: 'm',
    role: 'has the other minicab firm',
    desc: 'a man in a car coat with a clipboard',
    voice: 'plain',
    nerve: PEOPLE.nev.nerveZeroToOne,
    venal: PEOPLE.nev.venalZeroToOne,
    talk: PEOPLE.nev.talkativeZeroToOne,
    discretion: PEOPLE.nev.discretionZeroToOne,
    close: [],
    look: { h: 1.74, b: 0.62, skin: 1, hair: ['short', '#5a5248'], top: ['jacket', '#6a5a3a', '#3a3a34'], bot: ['trousers', '#3a3a34'], x: [] },
    sched: [[0, 'off']],
    card: {
      who: "He has Stather's, the Hook's other minicab firm: two cars and a phone in his front room on the west road.",
      speak: 'Mild, a little wounded, says "such as it is".',
      lines: ['I take what Mickey’s drop. That is all I have ever done.'],
      life: 'Twenty years on the buses, then two second-hand saloons. His wife answers the phone.',
      fire: 'He knows nothing about the fire and says so.',
      rivals: 'He wants no part of anybody. A business, not a side.',
      secret: 'When people go off Mickey’s, his phone rings. He keeps a note of the days it rang most.',
    },
  },
];
