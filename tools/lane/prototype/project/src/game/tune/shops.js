// The numbers of the system "shops" (spending, the fence, the wardrobe; DESIGN 9, A21, A30): plain data.
export const TUNE = {
  // each shop sells only its list, by its hours, from its purse
  shops: {
    news: { name: "Peart's", fromHour: 6, untilHour: 18, sells: ['cigarettes', 'paper'], pursePence: 4000 },
    caff: { name: "Rinaldi's", fromHour: 6.5, untilHour: 17, sells: ['meal', 'tea', 'scrap'], pursePence: 5000 },
    iron: { name: "the ironmonger's", fromHour: 8.5, untilHour: 17.5, sells: ['crowbar', 'torch', 'keyCut'], pursePence: 6000 },
    chandler: { name: 'the chandlery', fromHour: 8, untilHour: 17, sells: ['decentJacket', 'goodOvercoat', 'scarf', 'hat'], pursePence: 9000 },
    rita: { name: "Rita's", fromHour: 9, untilHour: 17.5, sells: ['secondHandCoat'], buys: true, fence: true, pursePence: 12000 },
    barber: { name: 'the barber on Chapel Lane', fromHour: 9, untilHour: 17, sells: ['barber'], pursePence: 2000 },
    doctor: { name: 'the retired doctor by the quay', fromHour: 0, untilHour: 24, sells: ['stitches'], pursePence: 0, remembers: true },
    lot: { name: 'the used-car lot on the north road', fromHour: 9, untilHour: 17, sells: ['usedCar'], pursePence: 0 },
    solicitor: { name: 'the solicitor over the bank', fromHour: 9.5, untilHour: 16.5, sells: ['solicitorRetainer'], pursePence: 0 },
    shaun: { name: "Shaun Hewson's lock-up", fromHour: 8, untilHour: 18, sells: ['respray'], pursePence: 0 },
  },
  shutOnSunday: ['news', 'iron', 'chandler', 'rita', 'barber', 'lot', 'solicitor'],
  restocksOnWeekday: 0,
  outfits: [null, 'as he arrived', 'a decent jacket', 'a good overcoat'],
  outfitBought: { decentJacket: 2, goodOvercoat: 3 },
  refusedRemembersGameDays: 7,
};
export const SCHEDULES = {};
export const PEOPLE = {};
