// The numbers and the places of the system "way" (finding the way; DESIGN 4 guidance, A9, A10): plain data.
// Every place a job, a fare, a letter or a person names has an address, a landmark and a ground label (ER-WAY-02,
// ER-GROUND-01). x, z are metres on the prototype's map. label: public | hours | private | forbidden.
export const TUNE = {
  reachedWithinMetres: 6,
  askWithinMetres: 3,
  mapStopsHim: true,
};
const P = (id, name, x, z, address, landmark, label, o = {}) => Object.assign({ id, name, x, z, address, landmark, label }, o);
export const PLACE_LIST = [
  P('mickeys', "Mickey's Cars", 7.2, 36, '2 Quay Street', 'the cab office at the quay end, the rank outside', 'hours', { room: 'mickeys', openFromHour: 6, openUntilHour: 24, owner: 'sheila' }),
  P('yard', "Mickey's yard", 23.4, 36, 'behind 2 Quay Street', 'through the office and out the back, the shed and the two gates', 'private', { owner: 'ron' }),
  P('ada', "Ada's", -7.2, 32, '1 Quay Street', "the window opposite Mickey's with the net curtain", 'private', { room: 'ada', owner: 'ada' }),
  P('fish', "Laverack's", 7.2, 26.8, '4 Quay Street', 'the wet fish shop with the blue awning', 'hours', { room: 'fish', openFromHour: 7, openUntilHour: 16, owner: 'brenda' }),
  P('busstop', 'the bus stop', -5.9, 20.6, 'Quay Street, west side', 'the shelter by the lamp, opposite the launderette', 'public'),
  P('laund', 'the Washeteria', 7.2, 18.4, '6 Quay Street', 'the launderette with the steamed window', 'hours', { room: 'laund', openFromHour: 8, openUntilHour: 20, owner: 'k_laund' }),
  P('grocer', 'Hook Stores', 7.2, 10, '8 Quay Street', 'the grocer with the crates outside', 'hours', { room: 'grocer', openFromHour: 8, openUntilHour: 18, owner: 'k_grocer' }),
  P('news', "Peart's", -7.2, 7.3, '7 Quay Street', 'the newsagent with the paper boards', 'hours', { room: 'news', openFromHour: 6, openUntilHour: 18, owner: 'k_news' }),
  P('iron', "the ironmonger's", -7.2, 0, '9 Quay Street', 'the shop with the galvanised buckets hung by the door', 'hours', { room: 'iron', openFromHour: 8.5, openUntilHour: 17.5, owner: 'k_iron' }),
  P('tangs', 'the Golden River', 7.2, -6.8, '12 Quay Street', 'the takeaway with the red lantern', 'hours', { room: 'tangs', openFromHour: 17, openUntilHour: 23.5, owner: 'peter' }),
  P('tearoom', 'the Copper Kettle', -7.2, -7.3, '11 Quay Street', 'the tea room with the lace half-curtain', 'hours', { room: 'tearoom', openFromHour: 9, openUntilHour: 17, owner: 'k_tea' }),
  P('phone', 'the phone box', 6, -11.2, 'Quay Street, by number 14', 'the red box past the takeaway', 'public'),
  P('caff', "Rinaldi's", -7.2, -29, '17 Quay Street', 'the caff on the corner of Chapel Lane, steam on the glass', 'hours', { room: 'caff', openFromHour: 6.5, openUntilHour: 17, owner: 'grace' }),
  P('rita', "Rita's", 7.2, -29, '18 Quay Street', 'the pawn shop with three brass balls, opposite the caff', 'hours', { room: 'rita', openFromHour: 9, openUntilHour: 17.5, owner: 'rita' }),
  P('ritaside', "Rita's side door", 13, -23.6, 'the back lane, behind 18 Quay Street', 'the green door in the lane behind the pawn shop', 'private', { owner: 'rita' }),
  P('coin', "Metcalfe's", -7.2, -36, '19 Quay Street', 'the coin shop that sells no coins', 'hours', { room: 'coin', openFromHour: 10, openUntilHour: 16, owner: 'hal' }),
  P('coinback', "Metcalfe's back door", -21, -36, 'the west alley', 'the back door in the alley behind the coin shop', 'private', { owner: 'hal' }),
  P('chandler', 'the chandlery', 7.2, -37, '20 Quay Street', 'the chandler with the coiled rope in the window', 'hours', { room: 'chandler', openFromHour: 8, openUntilHour: 17, owner: 'k_chand' }),
  P('boxing', 'the boxing club', 16, -40, 'the old hall behind 20 Quay Street', "the hall behind the chandler's, a bare bulb over the door", 'hours', { openFromHour: 17, openUntilHour: 22, owner: 'the trainer' }),
  P('boarding', 'Regent House', 7.2, -46.5, '24 Quay Street', 'the boarding house with the VACANCIES card', 'hours', { room: 'boarding', openFromHour: 0, openUntilHour: 24, owner: 'sylvia' }),
  P('chapel', 'the chapel', -18.6, -67, 'Quay Street, past the market end', 'the chapel with the green door, the bench outside', 'hours', { room: 'chapel', openFromHour: 7, openUntilHour: 20, owner: 'walsh' }),
  P('priest', "the priest's house", -7, -66, 'beside the chapel', 'the house by the chapel gate with the slippers on the step', 'private', { owner: 'walsh' }),
  P('barber', 'the barber', -44, -23.4, '5 Chapel Lane', 'the striped pole on Chapel Lane', 'hours', { openFromHour: 9, openUntilHour: 17, owner: 'k_barber' }),
  P('unit', 'the empty unit', -50, -18.5, '9 Chapel Lane', 'the whitewashed window on Chapel Lane', 'private', { owner: 'shaun' }),
  P('doctor', "the retired doctor's", 9, 42.6, '1 Quay Terrace', 'the end house on the quay with the brass plate taken down', 'private', { owner: 'k_doctor' }),
  P('harbour', 'the Harbour Office', -28.5, 41.9, 'the quay, west', 'the stone office with the clock over the door', 'hours', { room: 'harbour', openFromHour: 9, openUntilHour: 16.5, owner: 'susan' }),
  P('harbourback', "the Harbour Board's back office", -30, 38, 'the Harbour Office, through the counter', 'the door behind the counter marked PRIVATE', 'forbidden', { owner: 'susan' }),
  P('landing', 'the ferry landing', -47, 58.2, 'the quay, west end', 'the shelter under the last lamp on the landing', 'public'),
  P('smoke', 'the smoke house door', -46, 42.4, 'the quay, by the landing', 'the tarred door that smells of kippers', 'private', { owner: 'brenda' }),
  P('customs', 'the customs shed', -60, 50, 'the ferry landing', 'the long shed with the lamp that goes out at eleven', 'forbidden', { owner: 'k_customs' }),
  P('fishdock', 'the fish dock', 51.4, 56.2, 'the quay, east', 'the stacked fish boxes and the ice hut', 'public'),
  P('coldstore', 'the Old Basin cold stores', 96, 58, 'the fish dock, far end', 'the grey shed with the frosted pipes, shift change at half past five', 'hours', { openFromHour: 5, openUntilHour: 18, owner: 'norman' }),
  P('dockgate', 'the dock gate', 150, 46.6, 'Dock Road', 'the gate with the hut and the striped pole', 'forbidden', { owner: 'k_gate' }),
  P('row', 'the warehouse row', 70, 42.6, 'the quay, east of the yard', 'the brick warehouses, numbers painted on the doors', 'public'),
  P('fire', 'the burned warehouse', 119, 43, '7 warehouse row', 'the black shell with the boarded doors', 'private', { owner: 'k_board' }),
  P('scrap', "Iveson's yard", -98, 30, 'the quay, far west', 'the scrap yard with the crane and the dog', 'hours', { openFromHour: 7.5, openUntilHour: 17, owner: 'dennis', dog: true }),
  P('hut', "Iveson's hut", -101.5, 27.2, "inside Iveson's yard", 'the tarred hut by the weighbridge', 'private', { owner: 'dennis' }),
  P('market', 'Copper Row market', -30, -146, 'Copper Row', 'over the bridge, the stalls under the clock', 'public'),
  P('bank', 'the bank', 6.4, -139, '3 Copper Row', 'the stone bank with the camera over the door', 'hours', { openFromHour: 9.5, openUntilHour: 15.5, owner: 'k_bank', camera: true }),
  P('solicitor', "the solicitor's", 6.4, -141, 'over 3 Copper Row', 'the brass plate on the door beside the bank', 'hours', { openFromHour: 9.5, openUntilHour: 16.5, owner: 'k_sol' }),
  P('station', 'the station', 3, -203, 'Copper Row, north end', 'the station clock at the top of Copper Row', 'public'),
  P('lot', 'the used-car lot', 12, -214, 'the north road', 'the bunting and the cars with prices in the windscreens', 'hours', { openFromHour: 9, openUntilHour: 17, owner: 'k_lot' }),
  P('infirmary', 'the Infirmary', -118, 49.6, 'the west road', 'out along the west road, the lit porch', 'public'),
  P('northrank', 'the north road rank', 8, -196, 'by the station', 'the lay-by under the station clock', 'public'),
  P('ferryrank', 'the ferry rank', -42.4, 56.6, 'the ferry landing', 'the painted bay by the landing shelter', 'public'),
];
// Street name plates at each street's ends (4.1.3)
export const STREETS = [
  { name: 'Quay Street', ends: [[0, 40], [0, -90]] },
  { name: 'Chapel Lane', ends: [[-78, -18.5], [25, -18.5]] },
  { name: 'Copper Row', ends: [[0, -124], [0, -220]] },
  { name: 'the quay', ends: [[-128, 47], [160, 47]] },
];
// Set places where a running man goes over a low wall or fence (A26): [x, z, across-to x, z, height in metres]
export const VAULTS = [
  { id: 'yardwall', at: [27.4, 33], to: [29.4, 33], heightMetres: 1.1, what: 'the yard wall into the back lane' },
  { id: 'lanefence', at: [29.5, -10], to: [31.8, -10], heightMetres: 1.0, what: 'the fence at the lane end' },
  { id: 'alleybins', at: [-22, -40], to: [-22, -43], heightMetres: 0.9, what: 'the bins across the west alley' },
  { id: 'chapelwall', at: [-12, -62], to: [-12, -64.5], heightMetres: 1.1, what: 'the low wall of the chapel yard' },
  { id: 'quayrail', at: [20, 43.5], to: [20, 45.5], heightMetres: 1.0, what: 'the rail between the row and the quay' },
];
export const SCHEDULES = {};
export const PEOPLE = {};
