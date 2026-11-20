// Writes the rule pieces' cases (test/cases/<piece>.json) from the lists below. A case with `has` or `out` states
// what the rule must give, by hand, and the writer refuses to write a file if the piece disagrees. A case with
// neither records what the piece gives today ("recorded": true): a guard against change, not a statement of the
// rule. Usage: node tools/pieces_cases.mjs   (then: node test/pieces.mjs)
import fs from 'fs';
const P = async (n) => (await import(`../src/game/pieces/${n}.js`)).PIECE.fns;
const sets = {};
const add = (piece, id, rule, fn, input, expect) => (sets[piece] || (sets[piece] = [])).push({ id, rule, fn, in: input, ...(expect || {}) });

// ---------- money ----------
{
  const m = 'money';
  add(m, 'words-rent', 'ER-MONEY-02', 'sumInWords', [1800], { out: 'eighteen pounds' });
  add(m, 'words-start', 'ER-MONEY-02', 'sumInWords', [2350], { out: 'twenty-three pounds fifty' });
  add(m, 'words-pence', 'ER-MONEY-02', 'sumInWords', [80], { out: 'eighty pence' });
  add(m, 'words-none', 'ER-MONEY-02', 'sumInWords', [0], { out: 'nothing' });
  add(m, 'words-hundred', 'ER-MONEY-02', 'sumInWords', [15600], { out: 'one hundred and fifty-six pounds' });
  add(m, 'words-one', 'ER-MONEY-02', 'sumInWords', [100], { out: 'one pound' });
  add(m, 'pay-tin-first', 'ER-MONEY-01', 'pay', [{ clean: 1000, dirty: 300 }, 500, false, 'a cosh'], { has: { ok: true, pots: { clean: 800, dirty: 0 }, flows: [{ from: 'tin', pence: 300 }, { from: 'pocket', pence: 200 }] } });
  add(m, 'pay-clean-only', 'ER-MONEY-01', 'pay', [{ clean: 1000, dirty: 5000 }, 1800, true, 'rent'], { has: { ok: false, pots: { clean: 1000, dirty: 5000 }, flows: [] } });
  add(m, 'pay-clean-only-ok', 'ER-MONEY-01', 'pay', [{ clean: 2000, dirty: 5000 }, 1800, true, 'rent'], { has: { ok: true, pots: { clean: 200, dirty: 5000 } } });
  add(m, 'pay-too-much', 'ER-MONEY-01', 'pay', [{ clean: 100, dirty: 100 }, 500, false, 'x'], { has: { ok: false, pots: { clean: 100, dirty: 100 } } });
  add(m, 'pay-nothing', 'ER-MONEY-01', 'pay', [{ clean: 100, dirty: 0 }, 0, false, 'x'], { has: { ok: true, flows: [] } });
  add(m, 'pay-negative', 'ER-MONEY-01', 'pay', [{ clean: 100, dirty: 0 }, -50, false, 'x'], { has: { ok: false, pots: { clean: 100, dirty: 0 }, flows: [] } });
  add(m, 'earn-fare', 'ER-MONEY-01', 'earn', [{ clean: 2350, dirty: 0 }, 210, false, 'a fare'], { has: { pots: { clean: 2560, dirty: 0 }, flows: [{ from: 'world', to: 'pocket', pence: 210, why: 'a fare' }] } });
  add(m, 'earn-night', 'ER-MONEY-01', 'earn', [{ clean: 0, dirty: 0 }, 6000, true, 'the Monday bag'], { has: { pots: { clean: 0, dirty: 6000 }, flows: [{ to: 'tin', dirty: true }] } });
  add(m, 'earn-negative', 'ER-MONEY-01', 'earn', [{ clean: 5, dirty: 5 }, -100, false, 'x'], { has: { pots: { clean: 5, dirty: 5 }, flows: [] } });
  add(m, 'cap-no-fares', 'DESIGN 9', 'washCap', [0, 0, 0], { out: 1000 });
  add(m, 'cap-fares', 'DESIGN 9', 'washCap', [1000, 0, 0], { out: 1800 });
  add(m, 'cap-firm-and-fronts', 'A15', 'washCap', [1000, 7000, 2000], { out: 5550 });
  add(m, 'warn-over', 'ER-MONEY-04', 'washWarning', [6000, 1800], { has: { over: 4200, warns: true } });
  add(m, 'warn-fits', 'ER-MONEY-04', 'washWarning', [1500, 1800], { has: { over: 0, warns: false } });
  add(m, 'warn-empty', 'ER-MONEY-04', 'washWarning', [0, 1800], { has: { over: 0, warns: false, words: 'There is nothing in the tin to put through.' } });
  add(m, 'wash-fits-only', 'DESIGN 9', 'wash', [{ clean: 100, dirty: 6000 }, 1800, false], { has: { pots: { clean: 1900, dirty: 4200 }, washed: 1800, booksOffAdded: 0, left: 4200 } });
  add(m, 'wash-all-over', 'DESIGN 9', 'wash', [{ clean: 100, dirty: 6000 }, 1800, true], { has: { pots: { clean: 6100, dirty: 0 }, washed: 6000, booksOffAdded: 4200 } });
  add(m, 'wash-all-fits', 'DESIGN 9', 'wash', [{ clean: 0, dirty: 900 }, 1800, true], { has: { washed: 900, booksOffAdded: 0 } });
  add(m, 'wash-empty', 'DESIGN 9', 'wash', [{ clean: 50, dirty: 0 }, 1800, true], { has: { washed: 0, flows: [] } });
  add(m, 'costs-two-drivers', '2.7.4', 'weekCosts', [2], { has: [{ what: 'running costs', pence: 950, dayIndex: 3 }, { what: 'wages', pence: 6600, dayIndex: 4 }, { what: 'rent', pence: 1800, dayIndex: 4, hour: 18 }] });
  add(m, 'firm-full-week', '2.7.4', 'firmWeek', [2, 5], { out: { takings: 7000, wages: 6600, toPocket: 400, shortFromPocket: 0 } });
  add(m, 'firm-short-week', '2.7.4', 'firmWeek', [2, 3], { out: { takings: 4200, wages: 6600, toPocket: 0, shortFromPocket: 2400 } });
  add(m, 'week-doing-nothing-misses-rent', 'ER-MONEY-03', 'scriptedWeek', [{ faresPerDay: [0, 0, 0, 0, 0, 0, 0] }], { has: { rentPaid: false, costsPaid: true } });
  add(m, 'week-of-fares-alone-pays-rent', 'ER-MONEY-03', 'scriptedWeek', [{ faresPerDay: [0, 3, 3, 3, 3, 0, 0], farePence: 210 }], { has: { rentPaid: true, costsPaid: true } });
  add(m, 'week-one-fare-a-day-is-not-enough', 'ER-MONEY-03', 'scriptedWeek', [{ faresPerDay: [0, 1, 0, 0, 0, 0, 0], farePence: 210 }], { has: { rentPaid: false } });
  add(m, 'alibi-driven', 'DESIGN 9', 'alibiFare', [1300, true, []], { has: { lie: false, holds: true } });
  add(m, 'alibi-written-unseen', 'DESIGN 9', 'alibiFare', [1300, false, []], { has: { lie: true, holds: true, needsSomeoneToHoldItUp: true } });
  add(m, 'alibi-written-seen-elsewhere', 'DESIGN 9', 'alibiFare', [1300, false, [{ minute: 1310, place: 'the landing' }]], { has: { lie: true, holds: false } });
  add(m, 'alibi-seen-an-hour-off', 'DESIGN 9', 'alibiFare', [1300, false, [{ minute: 1400, place: 'the landing' }]], { has: { lie: true, holds: true } });
  add(m, 'book-holds', 'DESIGN 16', 'bookReads', [[{ booksOffPence: 0 }, { booksOffPence: 0, lies: 1 }]], { has: { state: 'hold' } });
  add(m, 'book-thin', 'DESIGN 16', 'bookReads', [[{ booksOffPence: 4200 }, { booksOffPence: 0 }]], { has: { state: 'thin', weeksOff: 1 } });
  add(m, 'book-off', 'DESIGN 16', 'bookReads', [[{ booksOffPence: 4200 }, { booksOffPence: 100 }, { booksOffPence: 900 }]], { has: { state: 'off', weeksOff: 3 } });
  add(m, 'book-off-by-a-broken-lie', 'DESIGN 16', 'bookReads', [[{ booksOffPence: 0, lies: 1, liesBroken: 1 }]], { has: { state: 'off' } });
  add(m, 'in-words-short', 'ER-MONEY-02', 'moneyInWords', [{ clean: 2350, dirty: 6000 }, [{ what: 'the rent', pence: 1800 }, { what: 'running costs', pence: 950 }]], { has: { shortPence: 400, short: 'He is four pounds short of it.' } });
  add(m, 'in-words-has-it', 'ER-MONEY-02', 'moneyInWords', [{ clean: 5000, dirty: 0 }, [{ what: 'the rent', pence: 1800 }]], { has: { shortPence: 0, short: 'He has it.', has: 'Fifty pounds in his pocket.' } });
  add(m, 'in-words-nothing-owed', 'ER-MONEY-02', 'moneyInWords', [{ clean: 5000, dirty: 0 }, [{ what: 'the rent', pence: 1800, paid: true }]], { has: { owes: 'Nothing owed this week.' } });
}
// ---------- flows ----------
{
  const f = 'flows';
  const fare = { from: 'world', to: 'pocket', pence: 210, dirty: false, why: 'a fare' };
  add(f, 'sound-fare', 'ER-MONEY-01', 'sound', [fare], { has: { ok: true } });
  add(f, 'no-reason-is-money-from-nowhere', 'ER-MONEY-01', 'sound', [{ from: 'world', to: 'pocket', pence: 500 }], { has: { ok: false } });
  add(f, 'blank-reason', 'ER-MONEY-01', 'sound', [{ from: 'world', to: 'pocket', pence: 500, why: '  ' }], { has: { ok: false } });
  add(f, 'no-pot', 'ER-MONEY-01', 'sound', [{ from: 'world', to: 'sheila', pence: 500, why: 'x' }], { has: { ok: false } });
  add(f, 'same-sides', 'ER-MONEY-01', 'sound', [{ from: 'pocket', to: 'pocket', pence: 5, why: 'x' }], { has: { ok: false } });
  add(f, 'half-pence', 'ER-MONEY-01', 'sound', [{ from: 'world', to: 'tin', pence: 10.5, why: 'x' }], { has: { ok: false } });
  add(f, 'zero', 'ER-MONEY-01', 'sound', [{ from: 'world', to: 'tin', pence: 0, why: 'x' }], { has: { ok: false } });
  add(f, 'negative', 'ER-MONEY-01', 'sound', [{ from: 'world', to: 'tin', pence: -4, why: 'x' }], { has: { ok: false } });
  add(f, 'not-a-flow', 'ER-MONEY-01', 'sound', [null], { has: { ok: false } });
  add(f, 'open', 'ER-MONEY-01', 'open', [2350, 0], { out: { start: { pocket: 2350, tin: 0 }, sums: {}, lines: [], count: 0 } });
  const b0 = { start: { pocket: 2350, tin: 0 }, sums: {}, lines: [], count: 0 };
  add(f, 'add-fare', 'ER-MONEY-01', 'add', [b0, fare], { has: { ok: true, book: { sums: { 'world>pocket|a fare': 210 }, count: 1 } } });
  add(f, 'add-refused-leaves-book', 'ER-MONEY-01', 'add', [b0, { from: 'world', to: 'pocket', pence: 9 }], { has: { ok: false, book: { sums: {}, count: 0 } } });
  const b1 = { start: { pocket: 2350, tin: 0 }, sums: { 'world>pocket|a fare': 420, 'world>tin|the Monday bag': 6000, 'tin>pocket|the wash': 1800, 'pocket>world|rent': 1800, 'tin>world|a cosh': 800 }, lines: [], count: 6 };
  add(f, 'balance', 'ER-MONEY-01', 'balance', [b1], { out: { pocket: 2770, tin: 3400 } });
  add(f, 'check-agrees', 'ER-MONEY-01', 'check', [b1, { clean: 2770, dirty: 3400 }], { out: { ok: true, pocketUnexplained: 0, tinUnexplained: 0 } });
  add(f, 'check-a-pound-from-nowhere', 'ER-MONEY-01', 'check', [b1, { clean: 2870, dirty: 3400 }], { out: { ok: false, pocketUnexplained: 100, tinUnexplained: 0 } });
  add(f, 'check-tin-short', 'ER-MONEY-01', 'check', [b1, { clean: 2770, dirty: 3000 }], { out: { ok: false, pocketUnexplained: 0, tinUnexplained: -400 } });
  add(f, 'check-empty-book', 'ER-MONEY-01', 'check', [b0, { clean: 2350, dirty: 0 }], { has: { ok: true } });
  add(f, 'totals', '2.7.7', 'totals', [b1], { out: { in: [{ why: 'the Monday bag', pence: 6000 }, { why: 'a fare', pence: 420 }], out: [{ why: 'rent', pence: 1800 }, { why: 'a cosh', pence: 800 }], washed: 1800 } });
  add(f, 'totals-empty', '2.7.7', 'totals', [b0], { out: { in: [], out: [], washed: 0 } });
  add(f, 'add-same-reason-sums', 'ER-MONEY-01', 'add', [{ start: { pocket: 0, tin: 0 }, sums: { 'world>pocket|a fare': 210 }, lines: [], count: 1 }, fare], { has: { book: { sums: { 'world>pocket|a fare': 420 }, count: 2 } } });
  add(f, 'wash-moves-between-pots', 'ER-MONEY-01', 'balance', [{ start: { pocket: 0, tin: 500 }, sums: { 'tin>pocket|the wash': 500 }, lines: [], count: 1 }], { out: { pocket: 500, tin: 0 } });
}
// ---------- debts ----------
{
  const d = 'debts';
  add(d, 'the-book', 'DESIGN 4', 'book', [], { has: { dennis: { owed: 8000, st: 'open' }, wayne: { owed: 3000 }, darren: { owed: 2200 }, lee: { owed: 1500 }, julie: { owed: 900 } } });
  const B = { dennis: { owed: 8000, st: 'open', paid: 0 }, wayne: { owed: 3000, st: 'open', paid: 0 }, darren: { owed: 2200, st: 'open', paid: 0 }, lee: { owed: 1500, st: 'open', paid: 0 }, julie: { owed: 900, st: 'open', paid: 0 } };
  add(d, 'total-156', 'DESIGN 15', 'total', [B], { out: 15600 });
  add(d, 'total-skips-paid', 'DESIGN 4', 'total', [{ a: { owed: 500, st: 'open' }, b: { owed: 0, st: 'paid' }, c: { owed: 0, st: 'forgiven' } }], { out: 500 });
  for (const [id, lesson] of [['darren', 'pays in what he hears'], ['wayne', 'pays in goods'], ['lee', 'stands, and has a little'], ['julie', 'cannot pay: mercy or shame'], ['dennis', 'has the money and will not hand it over']])
    add(d, 'lesson-' + id, 'DESIGN 4', 'lesson', [id], { out: lesson });
  add(d, 'dennis-squeezed-pays-all', '2.8.2', 'collect', ['dennis', B.dennis, 'squeezed'], { has: { pence: 8000, debt: { owed: 0, st: 'paid' }, tells: { kind: 'debt_paid', street: 'he squeezed it out of them' } } });
  add(d, 'lee-squeezed-pays-his-purse', '2.8.2', 'collect', ['lee', B.lee, 'squeezed'], { has: { pence: 400, debt: { owed: 1100, st: 'open', paid: 400 }, said: 'Part paid. The rest stays on the book.' } });
  add(d, 'julie-squeezed-shame-no-money', '2.8.2', 'collect', ['julie', B.julie, 'squeezed'], { has: { pence: 0, debt: { owed: 900, st: 'open' }, tells: { kind: 'debt_shamed' } } });
  add(d, 'wayne-pays-in-goods', 'DESIGN 4', 'collect', ['wayne', B.wayne, 'goods'], { has: { pence: 0, goods: 2500, debt: { owed: 500, st: 'open' } } });
  add(d, 'darren-pays-in-word', 'DESIGN 4', 'collect', ['darren', B.darren, 'word'], { has: { pence: 0, word: true, debt: { owed: 1800, st: 'open' } } });
  add(d, 'asked-and-pays-purse', '2.8.2', 'collect', ['darren', B.darren, 'asked'], { has: { pence: 300, debt: { owed: 1900 }, tells: { street: 'the debt was paid' } } });
  add(d, 'purse-given', '2.8.2', 'collect', ['lee', B.lee, 'asked', 5000], { has: { pence: 1500, debt: { owed: 0, st: 'paid' } } });
  add(d, 'second-visit-pays-the-rest-of-the-purse', '2.8.2', 'collect', ['lee', { owed: 1100, st: 'open', paid: 400 }, 'asked', 600], { has: { pence: 600, debt: { owed: 500, st: 'open', paid: 1000 } } });
  add(d, 'nothing-owed', '2.8.2', 'collect', ['lee', { owed: 0, st: 'paid', paid: 1500 }, 'squeezed'], { has: { pence: 0, tells: null } });
  add(d, 'forgiven-cannot-be-collected', '2.8.2', 'collect', ['julie', { owed: 0, st: 'forgiven' }, 'squeezed'], { has: { pence: 0, tells: null } });
  add(d, 'strike', 'DESIGN 4', 'strike', [B.julie], { has: { debt: { owed: 0, st: 'forgiven', struck: 900 }, tells: { kind: 'debt_forgive', street: 'he let a debt go' } } });
  add(d, 'strike-twice', 'DESIGN 4', 'strike', [{ owed: 0, st: 'forgiven' }], { has: { tells: null } });
  add(d, 'tells-squeezed-is-menace', 'DESIGN 4', 'tells', ['squeezed'], { has: { reads: -0.5 } });
  add(d, 'tells-struck-is-decent', 'DESIGN 4', 'tells', ['struck'], { has: { reads: 0.6, regard: 0.35 } });
  add(d, 'tells-shamed-is-worst', 'DESIGN 4', 'tells', ['shamed'], { has: { reads: -0.8 } });
  add(d, 'pays-when-afraid', 'DESIGN 4', 'paysWhenAsked', [B.lee, { fear: 0.6, regard: 0 }], { out: true });
  add(d, 'will-not-pay-unafraid', 'DESIGN 4', 'paysWhenAsked', [B.lee, { fear: 0.1, regard: 0 }], { out: false });
  add(d, 'small-debt-on-goodwill', 'DESIGN 4', 'paysWhenAsked', [B.julie, { fear: 0, regard: 0.5 }], { out: true });
  add(d, 'big-debt-not-on-goodwill', 'DESIGN 4', 'paysWhenAsked', [B.dennis, { fear: 0, regard: 0.9 }], { out: false });
  add(d, 'paid-debt-never', 'DESIGN 4', 'paysWhenAsked', [{ owed: 0, st: 'paid' }, { fear: 1, regard: 1 }], { out: false });
  add(d, 'lines', 'DESIGN 10', 'lines', [{ lee: { owed: 1100, st: 'open', paid: 400 } }], { out: [{ id: 'lee', st: 'open', owed: 1100, paid: 400 }] });
}
// ---------- fights ----------
{
  const f = 'fights';
  add(f, 'eight-rungs', 'DESIGN 7', 'rungs', [], { has: { 0: { name: 'stare' }, 3: { name: 'shove or grab' }, 4: { name: 'strike' }, 7: { name: 'kill', crime: 4 }, length: 8 } });
  add(f, 'stare-shows-the-actor', 'DESIGN 7', 'rung', [1], { has: { slots: [0, 4], crime: 0 } });
  add(f, 'strike-is-a-crime', 'DESIGN 7', 'rung', [5], { has: { kind: 'strike', crime: 2 } });
  add(f, 'weapon-used-shows-all-seven', 'DESIGN 7', 'rung', [7], { has: { slots: [0, 1, 2, 3, 4, 5, 6] } });
  add(f, 'no-ninth-rung', 'DESIGN 7', 'rung', [9], { out: null });
  add(f, 'nerve-alone', 'round 4', 'nerve', [0.5, {}], { out: 0.5 });
  add(f, 'nerve-face-two-watchers', 'round 4', 'nerve', [0.5, { watchers: 2 }], { out: 0.62 });
  add(f, 'nerve-face-capped', 'round 4', 'nerve', [0.5, { watchers: 9 }], { out: 0.74 });
  add(f, 'nerve-cornered', 'round 4', 'nerve', [0.5, { cornered: true }], { out: 0.7 });
  add(f, 'nerve-backed', 'round 5', 'nerve', [0.3, { backed: true }], { out: 0.6 });
  add(f, 'quiet-yard-he-gives-way-at-the-threat', 'round 4', 'answer', [3, 0.45, {}], { has: { gives: true } });
  add(f, 'in-the-street-he-stands', 'round 4', 'answer', [3, 0.45, { watchers: 3 }], { has: { gives: false } });
  add(f, 'lee-backed-stands-and-swings-at-the-shove', 'round 5', 'answer', [4, 0.3, { backed: true, watchers: 2 }], { has: { gives: false, fights: true } });
  add(f, 'lee-without-backing-gives-way', 'round 5', 'answer', [3, 0.3, {}], { has: { gives: true } });
  add(f, 'armed-presses-harder', 'DESIGN 7', 'pressure', [3, { armed: true }], { out: 0.8 });
  add(f, 'his-allies-ease-it', 'DESIGN 7', 'pressure', [3, { hisAllies: 2 }], { out: 0.18 });
  add(f, 'odds-fair', 'DESIGN 7', 'odds', [1, 1], { out: 'a fair fight' });
  add(f, 'odds-two-on-one-deadly', 'DESIGN 7', 'odds', [1, 2], { out: 'deadly' });
  add(f, 'odds-three-a-beating', 'DESIGN 7', 'odds', [1, 3], { out: 'a beating' });
  add(f, 'odds-ron-at-his-side', 'A16', 'odds', [2, 2], { out: 'a fair fight' });
  add(f, 'hands-off-a-woman', 'QUESTIONS 2', 'handsOff', [{ sex: 'f', age: 30 }], { out: true });
  add(f, 'hands-off-sixty', 'QUESTIONS 2', 'handsOff', [{ sex: 'm', age: 60 }], { out: true });
  add(f, 'hands-off-the-priest', 'QUESTIONS 2', 'handsOff', [{ sex: 'm', age: 50, priest: true }], { out: true });
  add(f, 'a-man-of-forty-is-fair', 'QUESTIONS 2', 'handsOff', [{ sex: 'm', age: 40 }], { out: false });
  add(f, 'fists-tier-0', 'DESIGN 7', 'weapon', [null], { has: { tier: 0, damageTimes: 1 } });
  add(f, 'chair-breaks-after-two', 'C12', 'weapon', ['chair'], { has: { tier: 1, breaksAfterBlows: 2, leftBehind: true } });
  add(f, 'brick-breaks-after-three', 'C12', 'weapon', ['brick'], { has: { tier: 1, breaksAfterBlows: 3 } });
  add(f, 'wheel-brace-never-breaks', 'C12', 'weapon', ['wheel brace'], { has: { tier: 1, breaksAfterBlows: 0 } });
  add(f, 'cosh-is-carried-and-found', 'DESIGN 7', 'weapon', ['cosh'], { has: { tier: 2, foundInASearch: true, leftBehind: false } });
  add(f, 'a-gun-is-the-last-tier', 'DESIGN 7', 'weapon', ['pistol'], { has: { tier: 3, crime: 4 } });
  add(f, 'condition-fresh', 'DESIGN 7', 'condition', [0], { out: 'fresh' });
  add(f, 'condition-down', 'DESIGN 7', 'condition', [1], { out: 'down' });
  add(f, 'fall-on-kerb-after-a-blow-can-kill', 'ER-FIGHT-05', 'fall', [{ who: 'foe', by: 'fists', landedOn: 'kerb', secondsSinceBlow: 1.2 }], { has: { canKill: true } });
  add(f, 'fall-on-grass-cannot', 'ER-FIGHT-05', 'fall', [{ who: 'foe', by: 'fists', landedOn: 'grass', secondsSinceBlow: 1 }], { has: { canKill: false } });
  add(f, 'fall-four-seconds-after-cannot', 'ER-FIGHT-05', 'fall', [{ who: 'foe', by: 'fists', landedOn: 'step', secondsSinceBlow: 4 }], { has: { canKill: false } });
  add(f, 'car-strike-never-counts', 'ER-DRIVE-03', 'fall', [{ who: 'foe', by: 'car', landedOn: 'kerb', secondsSinceBlow: 0 }], { has: { canKill: false } });
  add(f, 'tom-cannot-die', 'ER-FIGHT-04', 'fall', [{ who: 'tom', by: 'fists', landedOn: 'wall', secondsSinceBlow: 0 }], { has: { canKill: false } });
  add(f, 'a-fists-death-breaks-the-ruling', 'C7', 'deathBreaksRuling', [{ who: 'foe', cause: 'fists' }], { out: true });
  add(f, 'a-fall-death-does-not', 'C7', 'deathBreaksRuling', [{ who: 'foe', cause: 'fall', by: 'fists', landedOn: 'kerb', secondsSinceBlow: 0.5 }], { out: false });
  add(f, 'a-late-fall-death-does', 'C7', 'deathBreaksRuling', [{ who: 'foe', cause: 'fall', by: 'fists', landedOn: 'kerb', secondsSinceBlow: 9 }], { out: true });
  add(f, 'any-death-of-tom-does', 'C7', 'deathBreaksRuling', [{ who: 'tom', cause: 'fall', landedOn: 'kerb', secondsSinceBlow: 0 }], { out: true });
  add(f, 'ending-police', 'DESIGN 7', 'ending', [{ policeArrived: true, someoneDown: true }], { out: 'the police arrive' });
  add(f, 'ending-backs-off', 'DESIGN 7', 'ending', [{}], { out: 'someone backs off' });
  add(f, 'ending-runs', 'DESIGN 7', 'ending', [{ someoneRan: true }], { out: 'someone runs' });
  add(f, 'ending-down', 'DESIGN 7', 'ending', [{ someoneDown: true, someoneRan: true }], { out: 'someone goes down' });
  add(f, 'ending-step-in', 'DESIGN 7', 'ending', [{ peopleSteppedIn: true }], { out: 'people step in' });
  add(f, 'a-third-man-waits', 'ER-FIGHT-02', 'maySwing', [10, [9.6, 9.1]], { out: false });
  add(f, 'second-swing-too-close', 'ER-FIGHT-02', 'maySwing', [10, [9.8]], { out: false });
  add(f, 'second-swing-staggered', 'ER-FIGHT-02', 'maySwing', [10, [9.5]], { out: true });
  add(f, 'first-swing', 'ER-FIGHT-02', 'maySwing', [10, []], { out: true });
  add(f, 'the-melee-sheets-bands', 'ER-FIGHT-01', 'bands', [], { has: { ok: true, failed: [] } });
  add(f, 'same-seed-same-fight', 'ER-SAVE-01', 'simulate', [{ seed: 7, style: 'patient', foes: 1 }]);
  add(f, 'ten-thousand-fights-no-death-breaks-his-ruling', 'ER-FIGHT-05', 'holds', ['ER-FIGHT-05', 1990], { has: { ok: true, fights: 10000, deathsBreakingTheRuling: 0, tomDeaths: 0 } });
  add(f, 'skill-beats-mashing', 'ER-FIGHT-07', 'holds', ['ER-FIGHT-07', 1990], { has: { ok: true } });
  add(f, 'skill-beats-mashing-second-seed', 'ER-FIGHT-07', 'holds', ['ER-FIGHT-07', 42], { has: { ok: true } });
  add(f, 'a-fair-one-on-one-is-roughly-even', 'DESIGN 7', 'holds', ['fair', 1990], { has: { ok: true } });
  add(f, 'two-is-deadly-three-a-beating-a-man-at-his-side-helps', 'DESIGN 7', 'holds', ['odds', 1990], { has: { ok: true } });
  add(f, 'beaten-never-dead', 'ER-FIGHT-04', 'holds', ['ER-FIGHT-04', 1990], { has: { ok: true, tomDeaths: 0 } });
}
// ---------- talk ----------
{
  const t = 'talk';
  add(t, 'a-sum-in-a-demand-is-no-bribe', 'smoke run 20 Nov', 'intent', ["It's the twenty-two pounds. I want it paid."], { has: { amount: 0 } });
  add(t, 'typed-sum-demand', 'smoke run 20 Nov', 'intent', ["I've come for the 22 pounds on the book"], { has: { amount: 0, sumSpoken: 22, topic: 'debt' } });
  add(t, 'asking-a-price-is-no-bribe', 'smoke run 20 Nov', 'intent', ['How much is the rent, 18 pounds?'], { has: { intent: 'ask', amount: 0 } });
  add(t, 'a-bare-sum-is-no-bribe', 'smoke run 20 Nov', 'intent', ['£5'], { has: { amount: 0 } });
  add(t, 'an-offer-is-a-bribe', 'DESIGN 11', 'intent', ["Here's a fiver for your trouble"], { has: { intent: 'bribe', amount: 5 } });
  add(t, 'an-offer-with-a-sum', 'DESIGN 11', 'intent', ["I'll give you 10 quid to forget it"], { has: { intent: 'bribe', amount: 10 } });
  add(t, 'something-for-you', 'DESIGN 11', 'intent', ['There might be something for you in this'], { has: { intent: 'bribe' } });
  add(t, 'threat', 'DESIGN 11', 'intent', ["Keep your mouth shut or I'll be back"], { has: { intent: 'threaten' } });
  add(t, 'denial', 'DESIGN 11', 'intent', ["It wasn't me, I was at the office"], { has: { intent: 'lie', denies: true } });
  add(t, 'agree', 'DESIGN 11', 'intent', ['Yes. Tell them.'], { has: { intent: 'agree' } });
  add(t, 'refuse', 'DESIGN 11', 'intent', ['No. Not today.'], { has: { intent: 'refuse' } });
  add(t, 'ask-about-me', 'DESIGN 11', 'intent', ['What do they say about me?'], { has: { intent: 'ask', topic: 'me' } });
  add(t, 'ask-about-the-fire', 'DESIGN 11', 'intent', ['Who burned the warehouse?'], { has: { intent: 'ask', topic: 'fire' } });
  add(t, 'small-talk', 'DESIGN 11', 'intent', ['Wet again.'], { has: { intent: 'smalltalk', topic: 'other' } });
  // the plain yes: only these are taken
  for (const [i, y] of ['Yes.', 'Yes. Tell them.', "Aye, I'll carry it.", 'All right.', 'Go on then.', "I'll do it.", 'Agreed.', 'Yes, I am sure.'].entries()) add(t, 'plain-yes-' + (i + 1), 'ER-TALK-03', 'plainYes', [y], { out: true });
  // ER-TALK-03: lines that are not a plain yes. None may be taken as one. (The full 170 are run in test/game/talkx.mjs
  // from this same list times the decisions in the game; here the kinds of not-yes are each stated.)
  const NOT_YES = ['Yes, but not tonight.', 'Yes?', 'Yes if the money is right.', 'Maybe.', 'I suppose so.', 'Yes, unless Ron says otherwise.', "Yes. No. I don't know.", 'What happens if I do?', 'Who are they?', 'Tell me more.', 'Not yet.', 'No.', 'Never.', "I'll think on it.", 'Yeah right.', 'Hmm.', '', 'Yes once I have seen the book.', 'Ok but what is in it?', "I can't say yes to that.", 'Is that a yes or a no?', 'Perhaps tomorrow.', 'How much?', 'yes when it rains upwards', "I don't say yes to strangers", 'Fine? Is it?', 'Depends who is asking.', 'Aye, though I might regret it.', 'All right after Friday.', 'Sixty quid?'];
  NOT_YES.forEach((y, i) => add(t, 'not-a-plain-yes-' + (i + 1), 'ER-TALK-03', 'plainYes', [y], { out: false }));
  const D = { opts: [{ agree: 1, asksTwice: true, undoable: false }, { refuse: 1, asksTwice: true, undoable: false }] };
  add(t, 'decision-starts-open', 'ER-TALK-03', 'decisionStart', [D], { out: { q: null, asked: 0, done: false } });
  add(t, 'picking-a-line-only-puts-the-question', 'ER-TALK-03', 'decisionStep', [D, { q: null, asked: 0, done: false }, { job: 'prop', idx: 0 }], { has: { taken: null, state: { q: 0, done: false }, does: 'puts the plain question', leaveOffered: true } });
  add(t, 'the-yes-takes-it', 'ER-TALK-03', 'decisionStep', [D, { q: 0, asked: 1, done: false }, { job: 'yes' }], { has: { taken: 0, state: { done: true } } });
  add(t, 'a-no-decides-nothing', 'ER-TALK-03', 'decisionStep', [D, { q: 0, asked: 1, done: false }, { job: 'no' }], { has: { taken: null, state: { q: null, done: false } } });
  add(t, 'the-line-that-keeps-talking', 'ER-TALK-03', 'decisionStep', [D, { q: 0, asked: 1, done: false }, { job: 'keep' }], { has: { taken: null, state: { q: 0, done: false }, does: 'answers, and puts the plain question again' } });
  add(t, 'typed-yes-but-is-not-taken', 'ER-TALK-03', 'decisionStep', [D, { q: 0, asked: 1, done: false }, { job: 'typed', text: 'Yes, but not tonight.' }], { has: { taken: null, state: { q: 0, done: false } } });
  add(t, 'typed-plain-yes-is-taken', 'ER-TALK-03', 'decisionStep', [D, { q: 0, asked: 1, done: false }, { job: 'typed', text: 'Yes. Tell them.' }], { has: { taken: 0 } });
  add(t, 'typed-yes-before-the-question-only-asks', 'ER-CORE-03', 'decisionStep', [D, { q: null, asked: 0, done: false }, { job: 'typed', text: 'Yes.' }], { has: { taken: null, state: { q: 0 } } });
  add(t, 'a-yes-with-no-question-takes-nothing', 'ER-TALK-03', 'decisionStep', [D, { q: null, asked: 0, done: false }, { job: 'yes' }], { has: { taken: null } });
  add(t, 'leave-is-always-there', 'ER-TALK-03', 'decisionStep', [D, { q: 0, asked: 1, done: false }, { job: 'leave' }], { has: { taken: null, leaveOffered: true, state: { done: false } } });
  add(t, 'decided-stays-decided', 'ER-TALK-03', 'decisionStep', [D, { q: null, asked: 0, done: true }, { job: 'yes' }], { has: { taken: null } });
  add(t, 'what-can-be-undone-is-taken-at-once', 'ER-TALK-03', 'decisionStep', [{ opts: [{ agree: 1 }] }, { q: null, asked: 0, done: false }, { job: 'prop', idx: 0 }], { has: { taken: 0 } });
  add(t, 'a-direct-question-dropped-by-a-no', 'ER-TALK-03', 'decisionStep', [{ direct: true, opts: [{ agree: 1 }] }, { q: 0, asked: 1, done: false }, { job: 'no' }], { has: { taken: null, state: { done: true } } });
  add(t, 'sound-decision', 'ER-CORE-03', 'decisionSound', [D], { out: { ok: true, faults: [] } });
  add(t, 'cannot-be-undone-must-ask-twice', 'ER-CORE-03', 'decisionSound', [{ opts: [{ agree: 1, undoable: false }] }], { has: { ok: false } });
  const K = { people: ['Ron Kirby', 'Sheila Dunn'], allNames: ['Ron Kirby', 'Sheila Dunn', 'Maureen Jensen', 'Keith Garbutt'], deeds: ['carried a bag along the quay'], holdsAnything: true };
  add(t, 'claim-ok', 'ER-TALK-04', 'claimCheck', ["Ron said you carried something along the quay. That's all I know.", K], { has: { ok: true } });
  add(t, 'claim-names-a-stranger', 'ER-TALK-04', 'claimCheck', ['Ask Maureen Jensen, she runs the docks.', K], { has: { ok: false } });
  add(t, 'claim-names-by-surname', 'ER-TALK-04', 'claimCheck', ['Garbutt would know.', K], { has: { ok: false } });
  add(t, 'claim-accuses-of-a-deed-not-held', 'ER-TALK-04', 'claimCheck', ['I know you hit that lad on the quay.', K], { has: { ok: false } });
  add(t, 'claim-accuses-with-nothing-held', 'ER-TALK-04', 'claimCheck', ['I saw you last night.', { people: [], allNames: [], deeds: [], holdsAnything: false }], { has: { ok: false } });
  add(t, 'claim-drink', 'content rule', 'claimCheck', ['He was in the pub with a pint all night.', K], { has: { ok: false } });
  add(t, 'claim-a-pub-as-a-place-is-fine', 'content rule', 'claimCheck', ['He stood outside the pub on the corner.', K], { has: { ok: true } });
  add(t, 'claim-gambling', 'content rule', 'claimCheck', ['He owes the bookie, I heard.', K], { has: { ok: false } });
  add(t, 'claim-children', 'content rule', 'claimCheck', ['The kids on the corner saw it.', K], { has: { ok: false } });
  add(t, 'claim-wrong-year', 'canon era', 'claimCheck', ['Ring me on my mobile phone.', K], { has: { ok: false } });
  add(t, 'claim-plain-small-talk', 'ER-TALK-04', 'claimCheck', ["It's been wet since August.", K], { has: { ok: true } });
  const H = { own: { ron: { 'Boss.': 1 } }, st: { 'the Hook': { "It's been wet since August.": 0 } } };
  add(t, 'own-line-not-twice-in-a-day', 'ER-TALK-02', 'lineAllowed', [H, 'Boss.', 'ron', 'the Hook', 1, false], { out: false });
  add(t, 'own-line-next-day', 'ER-TALK-02', 'lineAllowed', [H, 'Boss.', 'ron', 'the Hook', 2, false], { out: true });
  add(t, 'own-line-anothers-mouth', 'ER-TALK-02', 'lineAllowed', [H, 'Boss.', 'darren', 'the Hook', 1, false], { out: true });
  add(t, 'shared-line-not-twice-in-a-week', 'ER-TALK-02', 'lineAllowed', [H, "It's been wet since August.", 'ada', 'the Hook', 6, true], { out: false });
  add(t, 'shared-line-after-a-week', 'ER-TALK-02', 'lineAllowed', [H, "It's been wet since August.", 'ada', 'the Hook', 7, true], { out: true });
  add(t, 'shared-line-on-the-other-street', 'ER-TALK-02', 'lineAllowed', [H, "It's been wet since August.", 'ada', 'Copper Row', 1, true], { out: true });
  add(t, 'saying-is-remembered', 'ER-TALK-02', 'lineSaid', [{ own: {}, st: {} }, 'Boss.', 'ron', 'the Hook', 3, false], { out: { own: { ron: { 'Boss.': 3 } }, st: {} } });
  add(t, 'next-line-skips-the-said', 'ER-TALK-02', 'nextLine', [H, ['Boss.', 'Now then.'], 'ron', 'the Hook', 1, false], { out: 'Now then.' });
  add(t, 'nothing-left-closes-the-talk', 'ER-TALK-02', 'nextLine', [H, ['Boss.'], 'ron', 'the Hook', 1, false], { out: null });
  add(t, 'reply-in-time-is-live', 'ER-TALK-01', 'replyRule', [1.2, 4], { out: { plays: 'live', sign: false } });
  add(t, 'reply-late-plays-the-written-line', 'ER-TALK-01', 'replyRule', [2.5, 4], { out: { plays: 'written', sign: true } });
  add(t, 'reply-never-begins', 'ER-TALK-01', 'replyRule', [null, null], { out: { plays: 'written', sign: true } });
  add(t, 'reply-slower-than-eight-is-dropped', 'ER-TALK-01', 'replyRule', [1, 9], { out: { plays: 'brush-off', sign: true } });
  add(t, 'scene-sixty-one-seconds', 'ER-TALK-06', 'sceneTooLong', [61], { out: true });
  add(t, 'scene-thirty-seconds', 'ER-TALK-06', 'sceneTooLong', [30], { out: false });
  add(t, 'report-filed', 'ER-TALK-07', 'report', [[], { line: 'Something odd.', who: 'ron', minute: 990.4, from: 'talk', live: true }], { has: { ok: true, list: [{ line: 'Something odd.', who: 'ron', minute: 990, from: 'talk', live: true }] } });
  add(t, 'report-from-pause', 'ER-TALK-07', 'report', [[], { line: 'x', from: 'pause' }], { has: { ok: true, list: [{ from: 'pause' }] } });
  add(t, 'report-needs-a-line', 'ER-TALK-07', 'report', [[], { line: ' ' }], { has: { ok: false } });
  add(t, 'pad-can-always-leave', 'ER-SPEAK-01', 'padCanAct', [[], true], { out: true });
  add(t, 'pad-with-lines', 'ER-SPEAK-01', 'padCanAct', [['Yes.'], false], { out: true });
}

const same = (a, b) => {
  if (typeof a === 'number' && typeof b === 'number') return Math.abs(a - b) < 1e-9;
  if (a === null || b === null || typeof a !== 'object' || typeof b !== 'object') return a === b;
  if (Array.isArray(a) !== Array.isArray(b)) return false;
  const ka = Object.keys(a), kb = Object.keys(b);
  return ka.length === kb.length && ka.every((k) => same(a[k], b[k]));
};
const has = (got, part) => {
  if (part === null || typeof part !== 'object') return same(got, part);
  if (got === null || typeof got !== 'object') return false;
  return Object.keys(part).every((k) => has(got[k], part[k]));
};
let bad = 0;
for (const piece in sets) {
  const fns = await P(piece), cases = [];
  for (const c of sets[piece]) {
    const got = fns[c.fn](...JSON.parse(JSON.stringify(c.in)));
    const plain = got === undefined ? null : JSON.parse(JSON.stringify(got));
    const o = { id: c.id, rule: c.rule, fn: c.fn, in: c.in };
    if ('out' in c) { o.out = c.out; if (!same(plain, c.out)) { bad++; console.log(`DISAGREES ${piece} ${c.id}: the rule says ${JSON.stringify(c.out)}, the piece gives ${JSON.stringify(plain)}`); } }
    else if ('has' in c) { o.outHas = c.has; if (!has(got, c.has)) { bad++; console.log(`DISAGREES ${piece} ${c.id}: the rule says ${JSON.stringify(c.has)}, the piece gives ${JSON.stringify(plain).slice(0, 400)}`); } }
    else { o.out = plain; o.recorded = true; }
    cases.push(o);
  }
  if (!bad) fs.writeFileSync(`test/cases/${piece}.json`, JSON.stringify({ piece, cases }, null, 1) + '\n');
  console.log(`${piece}: ${cases.length} cases`);
}
console.log(bad ? `NOT WRITTEN: ${bad} cases disagree with the piece` : 'written');
process.exit(bad ? 1 : 0);
