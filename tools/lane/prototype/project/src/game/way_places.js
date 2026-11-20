// LEDGER, the whole game: every place the game names, at a real spot of the prototype's map, with an address, a
// landmark and a ground label (DESIGN-ADDENDUM A9 and A10). Other systems add their own with core's addPlace.
// label: 'public' | 'hours' (free in hours, private out of them) | 'private' | 'forbidden'.
// known: 'all' (anybody on the street can say the way), 'locals' (people of the Hook), or a list of person ids.
// A place with a room is entered there; x and z are the door or the spot on the street.
import { addPlace } from './core.js';

const P = (id, name, x, z, address, landmark, label, o = {}) =>
  addPlace(Object.assign({ id, name, x, z, address, landmark, label, known: 'locals', also: [] }, o));

// ---- Quay Street, the east parade (Mickey's at the quay end) ----
P('mickeys', "Mickey's", 7.2, 36, '2 Quay Street', 'the blue sign at the quay end of Quay Street', 'hours', { room: 'mickeys', openFromHour: 0, openUntilHour: 24, known: 'all', also: ["Mickey's Cars", 'the office', 'the cab office'], owner: 'sheila' });
P('rank', 'the rank', 6.2, 38.5, "outside 2 Quay Street", "the kerb under Mickey's blue sign", 'public', { known: 'all', also: ["Mickey's rank"] });
P('yard', "Mickey's yard", 23.4, 36, "behind 2 Quay Street", "through the office, or by the gate on the back lane", 'private', { owner: 'sheila', also: ['the yard'] });
P('backlane', 'the back lane', 29.5, 10, 'behind the east parade', 'the unlit lane between the yards and the garages', 'public');
P('laveracks', "Laverack's", 7.2, 26.8, '4 Quay Street', "the wet fish shop next door to Mickey's, white tiles and an awning", 'hours', { room: 'fish', openFromHour: 7, openUntilHour: 16, owner: 'brenda', known: 'all', also: ['the fish shop'] });
P('launderette', 'the Washeteria', 7.2, 18.4, '6 Quay Street', 'the launderette with the steamed-up window, two doors up from the fish shop', 'hours', { room: 'laund', openFromHour: 8, openUntilHour: 20, known: 'all', also: ['the launderette', 'the washeteria'] });
P('grocer', 'Hook Stores', 7.2, 10, '8 Quay Street', 'the grocer by the zebra crossing', 'hours', { room: 'grocer', openFromHour: 8, openUntilHour: 17.5, known: 'all', also: ['the grocer'] });
P('goldenriver', 'the Golden River', 7.2, -6.8, '14 Quay Street', 'the hot food counter with the red lantern, past the crossing', 'hours', { room: 'tangs', openFromHour: 11.5, openUntilHour: 23, owner: 'peter', known: 'all', also: ['the Tangs', 'the chip counter'] });
P('phonebox_qs', 'the phone box on Quay Street', 6.0, -11.2, 'outside 16 Quay Street', 'the red box by the Golden River, lit all night', 'public', { known: 'all', also: ['the phone box', 'phonebox'] });
P('ritas', "Rita's", 7.2, -29, '20 Quay Street', "the second-hand and pawn shop on the corner of Chapel Lane, three brass balls over the door", 'hours', { room: 'rita', openFromHour: 9.5, openUntilHour: 17.5, owner: 'rita', known: 'all', also: ['the pawn', "the pawn shop", 'the second-hand shop', 'pawn'] });
P('ritaside', "Rita's side door", 13, -23.6, 'Chapel Lane, the east end', "the plain door round the corner from Rita's window, under her lit back window", 'private', { owner: 'rita', also: ["Rita's back room"] });
P('chandler', 'the chandlery', 7.2, -37, '22 Quay Street', "the rope and oilskin shop above Rita's", 'hours', { room: 'chandler', openFromHour: 9, openUntilHour: 17, known: 'all', also: ['the chandler', "the chandler's"] });
P('boxing', 'the boxing club', 29.5, -29, "the old hall behind the chandler's", "up the back lane behind Rita's and the chandlery, the hall with the skylight", 'hours', { openFromHour: 17, openUntilHour: 21.5, also: ['the old hall', 'the club'] });
P('regent', 'Regent House', 7.2, -46.5, '26 Quay Street', "Mrs Rennison's boarding house at the top of the street, net curtains and a brass plate", 'private', { room: 'boarding', owner: 'sylvia', known: 'all', also: ['the boarding house', "Mrs Rennison's"] });
P('steamlaundry', 'the steam laundry', 6.6, -62, '30 Quay Street', 'the big red-brick works, shut since the spring', 'forbidden', { also: ['Meridian Steam Laundry'] });
// ---- Quay Street, the west side ----
P('adas', "Ada's", -7.2, 32, '1 Quay Street', "the terrace door opposite Mickey's, the dark front window", 'private', { room: 'ada', owner: 'ada', known: 'all', also: ["Ada's door", "Ada's front room"] });
P('doctor', "Dr Calvert's", -7.2, 14, '7 Quay Street', "the terrace with the brass bell pull, four doors up from the quay on the terrace side", 'private', { known: ['ron', 'sheila', 'ada', 'grace', 'brenda', 'darren', 'albert'], also: ['the old doctor', 'the doctor'] });
P('busstop', 'the bus stop', -5.9, 20.6, 'Quay Street, the terrace side', 'the shelter halfway down the terraces', 'public', { known: 'all' });
P('newsagent', "Peart's", -7.2, 7.3, '11 Quay Street', "the newsagent and tobacconist, papers in a rack by the door", 'hours', { room: 'news', openFromHour: 6, openUntilHour: 18, known: 'all', also: ['the newsagent', 'the tobacconist', 'the paper shop'] });
P('ironmonger', 'the Hook Ironmongery', -7.2, 0, '13 Quay Street', "the ironmonger's with buckets on the pavement, next to the paper shop", 'hours', { room: 'iron', openFromHour: 8.5, openUntilHour: 17, known: 'all', also: ['the ironmonger', "the ironmonger's"] });
P('tearoom', 'the Copper Kettle', -7.2, -7.3, '15 Quay Street', 'the tea room with the lace half-curtain', 'hours', { room: 'tearoom', openFromHour: 9, openUntilHour: 16.5, known: 'all', also: ['the tea room'] });
P('caff', "Rinaldi's", -7.2, -29, '19 Quay Street', 'the caff on the corner of Chapel Lane, the window always steamed', 'hours', { room: 'caff', openFromHour: 6.5, openUntilHour: 18, owner: 'grace', known: 'all', also: ['the caff', "Grace's"] });
P('coin', "Metcalfe's", -7.2, -36, '21 Quay Street', 'the coin and stamp shop next to the caff, H. Metcalfe over the door', 'hours', { room: 'coin', openFromHour: 10, openUntilHour: 16, owner: 'hal', known: 'all', also: ["Hal's shop", 'the coin shop', "Hal's"] });
P('coinback', "Metcalfe's back door", -21, -36, 'the west alley', "the alley off Chapel Lane behind the caff: the second door, with the grille", 'private', { owner: 'hal', also: ["Hal's back door"] });
P('westalley', 'the west alley', -22, -40, 'off Chapel Lane', 'the narrow alley behind the caff and the coin shop', 'public');
P('chapel', 'the chapel', -18.6, -67, 'Quay Street, above the laundry', 'the red-brick chapel with the railings, opposite the steam laundry', 'hours', { room: 'chapel', openFromHour: 7, openUntilHour: 19, known: 'all', also: ["St Brendan's", 'the church'] });
P('priesthouse', "the priest's house", -7.2, -54, 'beside the chapel', 'the last terrace before the chapel railings, a lamp over the door', 'private', { owner: 'walsh', known: 'all', also: ["Father Walsh's", 'the presbytery'] });
P('ship', 'the Ship', -7.2, -84, 'Quay Street, by the bridge', 'the boarded pub at the bridge end, a board over every window', 'forbidden', { known: 'all' });
P('bridge', 'the bridge', 0, -107, 'the top of Quay Street', 'the iron bridge over the cut, Copper Row beyond it', 'public', { known: 'all' });
// ---- Chapel Lane ----
P('chapellane', 'Chapel Lane', -44, -18.5, 'off Quay Street by the caff', "the lane that runs west between Rinaldi's and the Copper Kettle side", 'public', { known: 'all' });
P('school', 'the Board School', -80, -18, 'the far end of Chapel Lane', 'the red-brick school, shut, its gates chained', 'forbidden', { known: 'all', also: ['the school'] });
// ---- the quay ----
P('quay', 'the quay', 9, 46, 'the foot of Quay Street', 'the water, the bollards and the lamps: left for the ferry, right for the fish dock', 'public', { known: 'all' });
P('harbour', 'the Harbour Office', -28.5, 41.9, 'the quay, west of Quay Street', 'the stone office with the clock over the door', 'hours', { room: 'harbour', openFromHour: 9, openUntilHour: 16.5, known: 'all', also: ['the Harbour Board', 'the Board'] });
P('harbourback', "the Harbour Board's back office", -30, 29.5, 'behind the Harbour Office', 'the yard door behind the clock, never open to callers', 'forbidden');
P('smokehouse', 'the smoke house', -46, 42.4, 'the quay, past the Harbour Office', 'the tarred shed with SMOKE HOUSE on the gable, shut', 'private', { also: ['the smoke house door'] });
P('netstore', 'the net store', -68, 42.4, 'the quay, by the landing', 'the long shed next to the smoke house', 'private');
P('customs', 'the customs shed', -62, 53, 'the ferry landing', 'the hut at the head of the landing with the lamp that goes off at eleven', 'forbidden', { known: 'all', also: ['customs'] });
P('landing', 'the ferry landing', -55, 60.5, 'the west end of the quay', 'the pontoon and the booking hut, past the smoke house', 'public', { known: 'all', also: ['the landing', 'the ferry'] });
P('shelter', 'the landing shelter', -47, 58.2, 'the ferry landing', 'the open shelter with the bench, this side of the booking hut', 'public', { known: 'all', also: ['the shelter'] });
P('ferryrank', 'the ferry rank', -42.4, 55, 'the ferry landing', 'the kerb where cabs wait for the boat, by the shelter', 'public', { known: 'all' });
P('phonebox_quay', 'the phone box on the quay', -30, 50.5, 'the quay, opposite the Harbour Office', 'the box under the lamp by the Harbour clock', 'public', { known: 'all' });
P('scrapyard', "Iveson's yard", -100, 42.4, 'the far west end of the quay', 'the scrap heaps and the crane legs, gate on the quay', 'hours', { openFromHour: 7.5, openUntilHour: 17, owner: 'dennis', known: 'all', also: ["Iveson's scrapyard", 'the scrapyard', "Iveson's"] });
P('hut', "Iveson's hut", -89, 28, "inside Iveson's yard", 'the cabin behind the first heap, a padlock on the door', 'private', { owner: 'dennis', also: ['the hut'] });
P('infirmary', 'the Infirmary road', -118, 49.6, 'the west road out of the Hook', 'past the scrapyard, where the quay road leaves the Hook', 'public', { known: 'all', also: ['the Infirmary', 'the hospital'] });
P('west_road', 'the west road', -126, 47, 'beyond the scrapyard', 'the quay road west, out to the Infirmary and Gullwing', 'public', { known: 'all' });
P('fishdock', 'the fish dock', 51, 56, 'the quay, east of Quay Street', 'the boxes and the nets, the pier beyond', 'public', { known: 'all' });
P('fishshed', "Jensen's fish shed", 89, 55, 'the fish dock', 'the long shed on the dock side, JENSEN AND SON on the board', 'private', { also: ['Jensen and Son'] });
P('warehouserow', 'the warehouse row', 70, 42.6, 'the quay, east', 'five brick warehouses numbered on the gables, one burnt', 'public', { known: 'all', also: ['the row'] });
P('no4', 'No. 4', 119, 43, 'the warehouse row', 'the burnt one, fourth along, boards on the doors', 'forbidden', { known: 'all', also: ['number four', 'the fire'] });
P('coldstore', 'the Old Basin cold stores', 143, 42.6, 'the east end of the warehouse row', 'No. 5 and the loading doors beyond it, where the packing shift comes off', 'private', { also: ['the cold store', 'the cold stores', 'the Old Basin'] });
P('dockgate', 'the dock gate', 152, 47, 'the east end of the quay', 'the barrier and the gatehouse where Dock Road begins', 'forbidden', { known: 'all', also: ['Dock Road'] });
// ---- over the bridge: Copper Row ----
P('market', 'Copper Row market', -30, -146, 'Copper Row, over the bridge', 'the stalls on the open ground, busiest on a Thursday', 'public', { known: 'all', also: ['the market'] });
P('bank', 'the Humber and District Bank', 6.4, -139, '2 Copper Row', 'the stone bank on the right over the bridge', 'hours', { openFromHour: 9.5, openUntilHour: 15.5, known: 'all', also: ['the bank'] });
P('outfitter', 'the drapers', 6.4, -187, '8 Copper Row', 'DRAPERS over the window, coats on a rail inside', 'hours', { openFromHour: 9, openUntilHour: 17.5, known: 'all', also: ['the outfitter', "the outfitter's"] });
P('solicitor', "Pym and Tasker, solicitors", -45, -138, 'the Corn Exchange, Copper Row', 'the side door of the Corn Exchange with the brass plates', 'hours', { openFromHour: 9.5, openUntilHour: 16.5, also: ['the solicitor', "the solicitor's"] });
P('barber', 'the barber', 6.4, -171, '6 Copper Row', 'the pole beside the bakery', 'hours', { openFromHour: 9, openUntilHour: 17, known: 'all' });
P('station_police', 'the police station', -45, -174, 'Copper Row, the west side', 'the blue lamp halfway along the terrace', 'hours', { openFromHour: 0, openUntilHour: 24, known: 'all', also: ['the station house', 'the nick'] });
P('station', 'Meridian Town station', 3, -203, 'the top of Copper Row', 'the stone station at the head of the street', 'public', { known: 'all', also: ['the station', 'the railway station'] });
P('stationrank', 'the station rank', 6, -200, 'outside the station', 'the kerb under the station clock', 'public', { known: 'all', also: ['the second rank'] });
P('carlot', "Tindall's car lot", -6, -210, 'the north road, by the station', 'the strip of flags and windscreens with prices on, left of the station', 'hours', { openFromHour: 9, openUntilHour: 17.5, also: ['the car lot', 'the used-car lot'] });
P('north_road', 'the north road', 2.2, -214, 'beyond the station', 'the road north out of the town, past the car lot', 'public', { known: 'all' });
