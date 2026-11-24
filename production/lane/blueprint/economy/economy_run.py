#!/usr/bin/env python3
"""LEDGER economy run (26 Nov 2026 design pass): the town's money for 13 game weeks, three play styles.

Sibling of ../numbers_run.py (23 Nov), which ran the design's own money rules with ASSUMED bands. This run uses the
figures of PRICES-WAGES-1990.md and the rules of ECONOMY-DESIGN-2026-11-26.md, and adds what numbers_run.py left out:
the shops' own takings and costs, protection, smuggled tobacco, loans, blackmail, bribes (DS Ellis included), the
rivals' dock-gate tax, police interest and the shops' mood. It is a small weekly model of written rules, not the game.

Clock (decision of 24 Nov): a game day is 48 real minutes (2 real seconds a game minute); the story is about 7 game
weeks; the run goes to 13 to catch late breakage. Weeks: 1 Act I, 2 to 6 Act II, 7 Act III, 8 to 13 after the story.

Run: python economy_run.py            (prints every table ECONOMY-DESIGN quotes, then the breakage checks)
     python economy_run.py --seeds 300 (the same with random noise on takings, 300 runs a style, reports the spread)
Standard library only. Every amount is in pounds of 1990. "INF" in a comment marks an inferred figure (see the prices file).
"""
import random
import sys

WEEKS = 13
STORY_WEEKS = 7

# ---------------- prices and wages (PRICES-WAGES-1990.md) ----------------
RENT_OFFICE = 18.0            # office and flat, Friday (design; cheap against council 23.36, Apr 1990)
OFFICE_RUNNING = 12.0         # phone, electric, radio licence (120 a year = 2.30 a week), INF for the rest
FARE_FLAG, FARE_MILE = 0.80, 1.10   # design pass: 80p plus 1.10 a mile; 1 to 2.5 mile Hook fares come to 2.50 to 3.55
TYPICAL_FARE = 3.00
CAR_FUEL_WEEK = 26.0          # about 400 miles at 30 mpg = 13 gallons at 2.00 (four-star about 1.86 a gallon Oct 1989, more by autumn 1990)
CAR_INSURE_WEEK = 12.0        # hire-and-reward cover "very expensive" (cab research S16); amount INF (about 600 a year)
CAR_UPKEEP_WEEK = 8.0         # tyres, repairs, INF
CAR_PRICE = 900.0             # a tired saloon at the lot, 600 to 1,200 (design); INF, no 1990 price list reached
HP_DEPOSIT, HP_WEEK, HP_WEEKS = 90.0, 22.0, 52   # hire purchase: a tenth down, about 22 a week for a year (about 1,234 in all), INF
DRIVER_SHARE = 0.5            # recommended: the driver keeps half his takings, the firm pays fuel and cover (principal model, Hamiltax 1989-90)
CAR_GROSS_ACT1 = 130.0        # a car's week on a dead firm's rank, takings before the split, INF from the 85 to 95 the design gives the book
CAR_GROSS_GOOD = 210.0        # on a good rank from rung 2 (design 110 to 140 to the book, i.e. about 220 to 280 gross under the old wage model)
CAR_GROSS_CONTRACT = 40.0     # the cold-store packing shift adds this per car once the contract is won (rung 3)

# ---------------- the shops of Quay Street and round about (weekly, pounds; all INF, scaled to 1990 wages) ----------------
# name: (takings a week, stock and costs as a share of takings, rent, wages, owner's draw). Margin = what is left.
SHOPS = {
    "fishmonger":  (1100, 0.70, 30, 110, 120),
    "grocer":      (1500, 0.76, 35, 120, 120),
    "newsagent":   (1900, 0.82, 35, 100, 110),   # mostly tobacco: low margin on a 1.70 pack
    "launderette": (420,  0.30, 30, 60,  110),
    "caff":        (750,  0.50, 30, 120, 120),
    "chip shop":   (900,  0.55, 30, 110, 130),
    "ironmonger":  (650,  0.62, 30, 60,  110),
    "tea room":    (380,  0.45, 25, 50,  90),
    "pawn":        (700,  0.40, 35, 70,  140),
}
SHOP_CAN_BEAR = 0.6           # a shop pays protection out of up to 60% of its margin before passing it on in prices
PASS_ON = 0.5                 # half of what it cannot bear goes on its board (prices up), half comes off its purse
CLOSE_AFTER = 4               # four losing weeks in a row and the shop shuts, said in the town as why

# ---------------- crime levers (ECONOMY-DESIGN section 5) ----------------
LANDING_CUT = 20.0            # Tom's cut of an outfit run to the ferry landing
PROTECTION = 10.0             # a shop's weekly payment on a round (5 to 15 by its margin)
ROUND_MAN_CUT = 0.25          # the man who walks the round keeps a quarter
TOBACCO_CASE_BUY, TOBACCO_CASE_SELL, CASE_PACKS = 100.0, 160.0, 200   # 200 packs at 50p off the boat, 80p to a stall or back counter (sold on at about 1.10 to 1.20 against 1.70)
TOBACCO_SAFE_CASES = 2        # cases a week the Hook can take before customs hear; each case over adds customs interest
NEWSAGENT_PACK_MARGIN = 0.13  # the newsagent's margin on a legal pack, INF from the 73% tax share (Hansard 14 Feb 1990)
LOAN_RATE_WEEK = 0.20         # "a pound in five a week": an unlicensed lender's rate, INF (no 1990 figure reached)
LOAN_BOOK_MAX = 200.0         # all the Hook's borrowers can carry at once: a dozen men at 10 to 30 pounds each, INF
LOAN_DEFAULT = 0.25           # a quarter of the book's loans go bad each week they run past four weeks
BLACKMAIL = 120.0             # a hook spent for money, purse-limited (50 to 300); spent once (RT-07)
HOLDUP = 90.0                 # what a till holds that hour, about a day's takings of a small shop (design: rare and late)
FENCE = 0.33
LIFT_RETAIL = 120.0
CONSTABLE_LOOK = 50.0         # a bought constable looks away once (design)
CONSTABLE_STATEMENT = 200.0   # loses a statement once (design)
ELLIS_BUY, ELLIS_WEEK = 800.0, 100.0    # recommended: about two and a half weeks of a detective sergeant's pay, then a weekly retainer
BRIEF_WEEK = 50.0
MAN_NIGHT_CUT = 20.0
POST_MEN, POST_PAY = 3, 40.0  # rung 4: men posted at the dock gate, the cold store and the landing, paid weekly (2.12.2)
WIDOW_TAX = 5.0               # the Widow's tax a car a week at the dock gate from rung 3, until answered

# ---------------- what Tom buys (design G8 plus this pass) ----------------
WANTS = [("second-hand coat", 15), ("barber", 4), ("crowbar", 6), ("torch", 4), ("decent jacket", 45),
         ("third car", "hp"), ("doctor's stitches", 20), ("good overcoat", 90), ("fourth car", "hp"),
         ("a front's share (a third of the caff)", 500), ("fifth car", "hp"), ("a brief on call, 4 weeks", 200),
         ("a better room above the office", 300), ("a second front (the empty unit let)", 900), ("a car of his own", 1500)]

# real minutes of the player's hands a lever takes (for pounds per real hour; ASSUMED, from the 48-minute day)
EFFORT_MIN = dict(fare=3, landing=6, round_setup=5, round_week=2, tobacco=15, loan=4, blackmail=8, holdup=6, lift=7)
RATIONED = ("blackmail", "holdup")   # capped by the rules (a hook is spent once; hold-ups rare and late), left out of the dominance check

STYLES = {
    # honest: fares, gentle debts, cars on terms, a front bought with clean money
    "honest": dict(fares=(8, 9, 9, 10, 10, 10, 10), debts=0.5, landing=0, round_from=None, round_size=0, tobacco=(),
                   loans_from=None, loan_out=0, blackmail_weeks=(), holdups=(), lifts=0, constable=False, ellis_week=None, cuts=0),
    # racketeer: every lever hard
    "racketeer": dict(fares=(5, 3, 3, 3, 3, 3, 3), debts=1.0, landing=3, round_from=2, round_size=8, tobacco=(0, 0, 2, 3, 4, 4, 4),
                      loans_from=3, loan_out=300, blackmail_weeks=(3, 5, 7, 9, 11), holdups=(4, 6, 8, 10, 12), lifts=2,
                      constable=True, ellis_week=6, cuts=4, tin_keep=900.0),
    # lazy (GD-07's lazy bot): a few fares a week, nothing else
    "lazy": dict(fares=(5, 4, 4, 4, 4, 4, 4), debts=0.0, landing=0, round_from=None, round_size=0, tobacco=(),
                 loans_from=None, loan_out=0, blackmail_weeks=(), holdups=(), lifts=0, constable=False, ellis_week=None, cuts=0),
    # mix: the firm plus a measured night
    "mix": dict(fares=(7, 6, 6, 6, 6, 6, 6), debts=0.8, landing=2, round_from=3, round_size=4, tobacco=(0, 0, 0, 1, 1, 2, 2),
                loans_from=4, loan_out=100, blackmail_weeks=(6,), holdups=(), lifts=1, constable=True, ellis_week=None, cuts=2, tin_keep=80.0),
}
DEBTS = {"darren": 22, "wayne": 30, "lee": 15, "julie": 9, "dennis": 80}


def wk(seq, w, default=0):
    return seq[min(w, len(seq)) - 1] if seq else default


def run(style, rng=None, tune=None):
    T = dict(tune or {})
    S = STYLES[style]
    noise = (lambda: rng.uniform(0.85, 1.15)) if rng else (lambda: 1.0)
    book, tin, pocket = 0.0, 0.0, 23.50
    cars, hp = 2, []                  # hp: weeks left on each car on terms
    bought, rung = [], 1
    shops = {n: dict(on_round=False, lost=0, open=True, board=1.0, fear=0.0, goodwill=0.0, cause=0, wk_margin=0.0)
             for n in SHOPS}
    heat = 0.0                        # police interest: Ellis's case points (stage up at 4, 8, 12)
    customs = 0.0
    loans_out, loan_age = 0.0, 0
    ellis_bought = False
    widow_answered = False
    rows, levers = [], {k: [0.0, 0.0] for k in ("fares", "firm", "landing", "round", "tobacco", "loans", "blackmail", "holdup", "lift", "debts")}
    biggest_take = 0.0
    arrests = 0
    short_paid, ellis_lapsed, low_driver_weeks = [], [], []
    for w in range(1, WEEKS + 1):
        assets_open = book + tin + pocket + loans_out          # the flows audit (ER-MONEY-01): checked at the week's end
        lend_w = back_w = bad_w = spent_w = posts_book_w = 0.0
        story = min(w, STORY_WEEKS)
        # ---- rung (design 2.12.2): 2 on Sheila's answer (week 2); 3 at five cars, a first front and a first round;
        #      4 at two fronts and two rounds (a round of six or more shops counts as two streets' worth)
        has_front = any(b.startswith("a front") for b in bought)
        n_fronts = has_front + any(b.startswith("a second front") for b in bought)
        n_rounds = 0 if not (S["round_from"] and w >= S["round_from"]) else (2 if S["round_size"] >= 6 and w >= S["round_from"] + 2 else 1)
        if w == 2 and "third car" not in bought:
            cars += 1                    # rung 2 brings the third car (OSP s32), on terms: the deposit from the book
            hp.append(HP_WEEKS)
            book -= HP_DEPOSIT
            spent_w += HP_DEPOSIT
            bought.append("third car")
        if w >= 2:
            rung = max(rung, 2)          # Sheila's answer and the third car (the recruit is not modelled)
        if cars >= 5 and has_front and n_rounds >= 1:
            rung = max(rung, 3)
        if rung >= 3 and n_fronts >= 2 and n_rounds >= 2 and any(b.startswith("a brief") for b in bought):
            rung = max(rung, 4)
        # ---- the firm (clean)
        gross = (CAR_GROSS_ACT1 * T.get("fare", 1.0)) if rung < 2 else CAR_GROSS_GOOD * T.get("good_rank", 1.0) * T.get("fare", 1.0)
        if rung >= 3:
            gross += CAR_GROSS_CONTRACT
        if T.get("wage_model"):          # choice 1 (a): the firm keeps all takings and pays each driver 90 a week
            firm_take = cars * (gross * noise() - 90.0)
        else:
            firm_take = cars * gross * (1 - DRIVER_SHARE) * noise()
        if gross * DRIVER_SHARE < 60.0 and not T.get("wage_model"):
            low_driver_weeks.append(w)   # a driver's half under 60: two such weeks running and he leaves (EC-02)
        car_costs = cars * (CAR_FUEL_WEEK + CAR_INSURE_WEEK + CAR_UPKEEP_WEEK)
        widow = cars * WIDOW_TAX if (rung >= 3 and not widow_answered) else 0.0
        if rung >= 3 and S["landing"] >= 2 and w >= 6:
            widow_answered = True     # answered by a man posted at the gate, paid 40 a week from cash below
        n_fares = wk(S["fares"], story) if w <= STORY_WEEKS else wk(S["fares"], STORY_WEEKS)
        tom_fares = n_fares * TYPICAL_FARE * T.get("fare", 1.0) * noise() * 0.92   # less his own fuel
        hp_pay = HP_WEEK * len(hp)
        hp = [x - 1 for x in hp if x > 1]
        book += firm_take + tom_fares - car_costs - widow - RENT_OFFICE - OFFICE_RUNNING - hp_pay
        levers["fares"][0] += tom_fares
        levers["fares"][1] += n_fares * EFFORT_MIN["fare"]
        levers["firm"][0] += firm_take - car_costs - widow - hp_pay
        week_clean = firm_take + tom_fares - car_costs - widow - hp_pay
        # ---- night money
        dirty = 0.0
        if w == 1:
            d = (sum(DEBTS.values()) - DEBTS["darren"]) * S["debts"]
            dirty += d
            levers["debts"][0] += d
            biggest_take = max(biggest_take, DEBTS["dennis"] * S["debts"])
        if w <= STORY_WEEKS or S["landing"]:
            runs = S["landing"] if w > 1 else min(S["landing"], 1)
            dirty += runs * LANDING_CUT
            levers["landing"][0] += runs * LANDING_CUT
            levers["landing"][1] += runs * EFFORT_MIN["landing"]
        # protection round
        round_take = 0.0
        if S["round_from"] and w >= S["round_from"]:
            want = min(S["round_size"], 2 + 2 * (w - S["round_from"]))
            on = [n for n in SHOPS if shops[n]["open"] and not shops[n].get("refused")][:want]
            for n in on:
                if not shops[n]["on_round"]:
                    shops[n]["on_round"] = True
                    levers["round"][1] += EFFORT_MIN["round_setup"]
                    heat += 0.3       # a shopkeeper may tell (temper decides in the game; the run takes the average)
            for n in on:
                if shops[n]["open"]:
                    round_take += PROTECTION * T.get("protection", 1.0)
            round_take *= (1 - ROUND_MAN_CUT)
            levers["round"][1] += EFFORT_MIN["round_week"] * len(on)   # trouble on the round comes back to Tom
            dirty += round_take
            levers["round"][0] += round_take
            heat += 0.05 * len(on)
        # smuggled tobacco
        cases = wk(S["tobacco"], story) if S["tobacco"] else 0
        tob = 0.0
        safe = (TOBACCO_SAFE_CASES + (2 if rung >= 4 else 0)) * T.get("tobacco_safe", 1.0)   # men at the dock gate (rung 4) let more through
        if cases and not T.get("push_tobacco"):
            cases = min(cases, int(safe))      # a player who listens: Darren and the gate men say when customs are about
        if cases:
            customs += max(0.0, cases - safe) * 1.0
            seized = customs >= 3.0
            if seized:            # customs take a load: the case money is lost and Ellis hears
                tob -= cases * TOBACCO_CASE_BUY
                customs = 0.0
                heat += 1.5
            else:
                tob += cases * (TOBACCO_CASE_SELL * T.get("tobacco_price", 1.0) - TOBACCO_CASE_BUY)
            dirty += tob
            levers["tobacco"][0] += tob
            levers["tobacco"][1] += cases * EFFORT_MIN["tobacco"]
            biggest_take = max(biggest_take, TOBACCO_CASE_SELL - TOBACCO_CASE_BUY)
        # loans (Tom lends from the tin)
        loan_in = 0.0
        if S["loans_from"] and w >= S["loans_from"] and w <= STORY_WEEKS + 2:
            if loans_out < min(S["loan_out"], LOAN_BOOK_MAX) - 1 and tin + dirty >= 50:
                lend = min(min(S["loan_out"], LOAN_BOOK_MAX) - loans_out, (tin + dirty) * 0.5)
                dirty -= lend
                lend_w = lend
                loans_out += lend
                levers["loans"][1] += EFFORT_MIN["loan"] * 2
                levers["loans"][0] -= lend
        if loans_out > 0:
            loan_age += 1
            interest = loans_out * LOAN_RATE_WEEK * T.get("loan_rate", 1.0)
            bad = loans_out * LOAN_DEFAULT if loan_age > 4 else 0.0
            back = loans_out * 0.25 if loan_age > 2 else 0.0     # principal comes back over four weeks
            loans_out -= bad + back
            back_w, bad_w = back, bad
            loan_in = interest + back
            dirty += loan_in
            levers["loans"][0] += loan_in
            levers["loans"][1] += EFFORT_MIN["loan"]
            heat += 0.1
        # blackmail (a hook spent once)
        if w in S["blackmail_weeks"]:
            dirty += BLACKMAIL
            levers["blackmail"][0] += BLACKMAIL
            levers["blackmail"][1] += EFFORT_MIN["blackmail"]
            heat += 0.6
            biggest_take = max(biggest_take, BLACKMAIL)
        # hold-ups and lifts
        if w in S["holdups"]:
            dirty += HOLDUP
            levers["holdup"][0] += HOLDUP
            levers["holdup"][1] += EFFORT_MIN["holdup"]
            heat += 2.0
            biggest_take = max(biggest_take, HOLDUP)
            victim = [n for n in SHOPS if shops[n]["open"]][(w // 2) % 5]
            shops[victim]["fear"] = 1.0           # takings down a tenth while the fear lasts (it fades over weeks)
            shops[victim]["cause"] = w
        n_lifts = (T.get("lifts", S["lifts"]) if rung >= 2 else 0)   # Rita's back room opens at rung 2
        lift = sum(LIFT_RETAIL * FENCE * (0.8 ** k) for k in range(int(n_lifts)))   # less for each further piece the same week (2.7.6)
        dirty += lift
        night_in = (dirty + lend_w - (levers["debts"][0] if w == 1 else 0.0) - min(0.0, tob)
                    - (HOLDUP if w in S["holdups"] else 0.0) - (BLACKMAIL if w in S["blackmail_weeks"] else 0.0))   # rationed one-offs left out too (MP-02 caps them as single takes)   # what the week's night brought in, before cuts, bribes and losses; the debt book left out
        levers["lift"][0] += lift
        levers["lift"][1] += n_lifts * EFFORT_MIN["lift"]
        heat += 0.15 * n_lifts
        # men's cuts, bribes: paid only from cash in hand (RT-17); short pay is recorded, never borrowed from the book
        def pay(amount):
            nonlocal dirty
            have = max(0.0, tin + dirty)
            paid = min(have, amount)
            dirty -= paid
            return paid >= amount - 0.01
        if w >= 2 and S["cuts"] and not pay(S["cuts"] * MAN_NIGHT_CUT):
            short_paid.append(w)
        if rung >= 4:
            posts = POST_MEN * POST_PAY
            if S["landing"] == 0:
                book -= posts          # an honest firm pays its yard men as wages from the book
                posts_book_w = posts
            elif not pay(posts):
                short_paid.append(w)
        if S["constable"] and w in (3, 7, 11) and pay(CONSTABLE_LOOK):
            heat = max(0.0, heat - 1.0)
        if ellis_bought:
            if not pay(ELLIS_WEEK):
                ellis_bought = False          # a missed week: she is no longer bought, and remembers it
                heat += 3.0
                ellis_lapsed.append(w)
        heat = max(0.0, heat - (0.8 if not ellis_bought else 1.6))   # quiet weeks cool her one step in about two weeks
        # arrest: the case reaches 8 points: custody, a brief for four weeks, a night week lost
        if heat >= 8.0 * T.get("arrest_at", 1.0):
            arrests += 1
            heat = 3.0
            if dirty > 0:
                dirty *= 0.5             # a night week lost to custody
            dirty -= min(BRIEF_WEEK * 4, max(0.0, tin + dirty))   # the brief is paid from what cash there is
        tin += dirty
        # ---- the wash (2.7.3, with NUMBERS-RUN M4: drivers' fares at 40%, Tom's at 80%)
        cap = 7 * 10.0 + 0.4 * firm_take + 0.8 * tom_fares + (60.0 if has_front else 0.0) * n_fronts
        wash = max(0.0, min(tin - S.get("tin_keep", 0.0), cap))
        tin -= wash
        book += wash
        # ---- the shops' week
        closed_now = []
        for n, (take, cost_share, rent, wages, draw) in SHOPS.items():
            s = shops[n]
            if not s["open"]:
                continue
            t = take * noise() / s["board"] ** 1.5           # dearer board, fewer customers
            if T.get("bad_season") and 4 <= w <= 7:
                t *= 0.85                                     # a slack month at the docks: wages short across the town
            t *= 1.0 - 0.1 * s["fear"]
            if n == "newsagent" and cases:
                t -= cases * CASE_PACKS * 1.70 * 0.5          # half of the smuggled packs replace his
            margin = t * (1 - cost_share) - rent - wages - draw
            pay = PROTECTION * T.get("protection", 1.0) if s["on_round"] else 0.0
            if s["on_round"]:
                s["cause"] = w
                s["fear"] = min(1.0, s["fear"] + 0.05)
                bearable = max(0.0, margin) * SHOP_CAN_BEAR
                over = max(0.0, pay - bearable)
                s["over_weeks"] = s.get("over_weeks", 0) + 1 if over > 0 else 0
                if s["over_weeks"] >= 3:
                    s["on_round"] = False        # he stops paying and tells: off the round, and Ellis has a witness
                    s["refused"] = True
                    heat += 2.0
                    pay = 0.0
                if over > 0:
                    heat += 1.0          # a shopkeeper squeezed past what he can bear goes to Ellis or tells (temper decides; the run takes the average)
                    s["fear"] = min(1.0, s["fear"] + 0.2)
                s["board"] = min(1.25, s["board"] * (1 + PASS_ON * over / max(t, 1)))
            margin -= pay
            if n == "newsagent" and cases:
                s["cause"] = w
            s["wk_margin"] = margin
            s["lost"] = s["lost"] + 1 if margin < 0 else 0
            if s["lost"] >= CLOSE_AFTER:
                s["open"] = False
                closed_now.append((n, w - s["cause"] <= 4))
            s["fear"] = max(0.0, s["fear"] - 0.02)
        # honest firm goodwill (gossip of a fair firm) and Tom's fares
        # ---- Friday: if the book cannot pay, cash from the pocket does; else arrears (RT-16)
        if book < 0 and pocket > 0:
            take = min(pocket, -book)
            pocket -= take
            book += take
        # ---- buy wants in order (a car on terms: the deposit; cash or book)
        wants = list(WANTS)
        if S["ellis_week"]:
            wants.insert(wants.index(("fourth car", "hp")) + 1, ("DS Ellis bought", "ellis"))
        for name, price in wants:
            if name in bought and name != "DS Ellis bought":
                continue
            if name == "DS Ellis bought":
                if ellis_bought or w < S["ellis_week"] or name in bought:
                    continue
                if tin >= ELLIS_BUY:
                    tin -= ELLIS_BUY
                    spent_w += ELLIS_BUY
                    ellis_bought = True
                    heat = max(0.0, heat - 4.0)
                    bought.append(name)
                    continue
                break
            if name in bought:
                continue
            if name in ("third car", "fourth car", "fifth car") and w < 2:
                break
            cost = HP_DEPOSIT if price == "hp" else price
            reserve = RENT_OFFICE + OFFICE_RUNNING + HP_WEEK * len(hp) + 30   # keeps next Friday's rent, running and terms in hand
            spendable = book - reserve + pocket + (tin if price in ("hp", 500, 900, 1500) else 0)
            if spendable >= cost:
                take = min(pocket, cost)
                pocket -= take
                rest = cost - take
                if price in ("hp", 500, 900, 1500):
                    t = min(tin, rest)
                    tin -= t
                    rest -= t
                book -= rest
                spent_w += cost
                bought.append(name)
                if price == "hp":
                    cars += 1
                    hp.append(HP_WEEKS)
            else:
                break
        expected = assets_open + week_clean - RENT_OFFICE - OFFICE_RUNNING + dirty + lend_w - back_w - bad_w - spent_w - posts_book_w
        actual = book + tin + pocket + loans_out
        assert abs(expected - actual) < 0.01, f"flows do not balance in week {w}: {expected:.2f} against {actual:.2f}"
        assert tin >= -0.01, f"the tin went below nothing in week {w}"
        wants_left = [(n, p) for n, p in wants if n not in bought]
        left_cost = sum(HP_DEPOSIT if p == "hp" else ELLIS_BUY if p == "ellis" else p for _, p in wants_left)   # what it costs to start each
        income = week_clean + dirty
        earned = week_clean + night_in    # MP-02 compares income: what his position brings in, the inherited debt book left out
        rows.append(dict(low_driver=list(low_driver_weeks), week=w, rung=rung, cars=cars, book=round(book), tin=round(tin), pocket=round(pocket),
                         worth=round(book + tin + pocket), clean=round(week_clean), dirty=round(dirty), income=round(income), earned=round(earned),
                         heat=round(heat, 1), arrests=arrests, shops_open=sum(s["open"] for s in shops.values()),
                         closed=closed_now, wants_left=len(wants_left), left_cost=round(left_cost),
                         boards=round(max(s["board"] for s in shops.values()), 3),
                         newsagent_margin=round(shops["newsagent"]["wk_margin"]), ellis=ellis_bought))
    rows[-1]["short_paid"], rows[-1]["ellis_lapsed"] = short_paid, ellis_lapsed
    return rows, levers, biggest_take, bought, shops


def checks(style, rows, levers, biggest, shops):
    """The four breakages the brief names, plus the money study's two rules (MP-02)."""
    out = []
    w3 = rows[2]
    rich = w3["worth"] >= w3["left_cost"]
    out.append(("rich by week 3", rich, f"worth {w3['worth']} against {w3['left_cost']} of wants left"))
    broke = False
    run_neg = 0
    for r in rows:
        run_neg = run_neg + 1 if r["book"] + r["pocket"] < 0 else 0
        broke = broke or run_neg >= 3
    out.append(("broke with no way back", broke, f"lowest book {min(r['book'] for r in rows)}"))
    causeless = [c for r in rows for c in r["closed"] if not c[1]]
    out.append(("a shop shut with no cause", bool(causeless), f"closures {[c for r in rows for c in r['closed']]}"))
    a1 = rows[0]["earned"]
    a2_last = rows[STORY_WEEKS - 2]["earned"]
    ratio = a2_last / a1 if a1 > 0 else float("inf")
    if style == "lazy":
        out.append(("the lazy bot pays every Friday's rent (MP-04)", min(r["book"] for r in rows) < 0, f"lowest book {min(r['book'] for r in rows)}"))
    else:
        out.append(("Act II's last week 3 to 10 times Act I's (MP-02)", not (3 <= ratio <= 10), f"ratio {ratio:.1f}"))
    weekly = max(r["income"] for r in rows[:STORY_WEEKS])
    cap = max(150, 1.5 * weekly)
    out.append(("no single take over max(150, 1.5 weeks' income) (MP-02)", biggest > cap, f"biggest {biggest:.0f}, cap {cap:.0f}"))
    out.append(("a named want still out of reach at week 7 (GD-07)", rows[STORY_WEEKS - 1]["wants_left"] == 0,
                f"{rows[STORY_WEEKS - 1]['wants_left']} left, {rows[STORY_WEEKS - 1]['left_cost']}"))
    return out


def lever_rates(levers):
    rates = {}
    for k, (money, minutes) in levers.items():
        if minutes > 0 and k not in ("firm", "debts") and k not in RATIONED:
            rates[k] = money / (minutes / 60.0)
    return rates


def table(style, rows):
    print(f"\n{style}: week, rung, cars, book, tin, worth, clean, night, Ellis case, shops open, dearest board, newsagent's margin, wants left (cost)")
    for r in rows:
        print(f"  {r['week']:>2}  r{r['rung']}  {r['cars']}  {r['book']:>6}  {r['tin']:>6}  {r['worth']:>6}  {r['clean']:>5}  {r['dirty']:>5}"
              f"  {r['heat']:>4}  {r['shops_open']}  {r['boards']:.2f}  {r['newsagent_margin']:>5}  {r['wants_left']:>2} ({r['left_cost']})"
              + (f"  closed {r['closed']}" if r['closed'] else "") + ("  Ellis bought" if r['ellis'] else ""))


def main():
    seeds = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 0
    all_rates = {}
    fails = 0
    for style in STYLES:
        rows, levers, biggest, bought, shops = run(style)
        table(style, rows)
        print("  bought:", ", ".join(bought))
        print(f"  arrests {rows[-1]['arrests']}; men paid short in weeks {rows[-1]['short_paid'] or 'none'}; Ellis lapsed in weeks {rows[-1]['ellis_lapsed'] or 'never'}")
        for name, bad, note in checks(style, rows, levers, biggest, shops):
            fails += bad
            print(f"  {'FAIL' if bad else 'ok  '} {name}: {note}")
        r = lever_rates(levers)
        all_rates[style] = r
        print("  pounds per real hour of the player's hands:", ", ".join(f"{k} {v:.0f}" for k, v in sorted(r.items(), key=lambda x: -x[1])))
    # lever dominance: across styles, the best lever against the median of the rest
    pooled = {}
    for r in all_rates.values():
        for k, v in r.items():
            pooled.setdefault(k, []).append(v)
    best = {k: max(v) for k, v in pooled.items()}
    ranked = sorted(best.items(), key=lambda x: -x[1])
    med = sorted(v for _, v in ranked[1:])[len(ranked[1:]) // 2]
    dom = ranked[0][1] > 2.0 * med
    fails += dom
    print(f"\n{'FAIL' if dom else 'ok  '} no lever pays more than twice the middle lever an hour: best {ranked[0][0]} {ranked[0][1]:.0f}, middle {med:.0f}")
    if seeds:
        print(f"\nSpread over {seeds} noisy runs a style (takings within 15% either way):")
        for style in STYLES:
            w3, w7, w13, counts, e1, e6 = [], [], [], {}, [], []
            for sd in range(seeds):
                rows, levers, biggest, bought, shops = run(style, random.Random(sd))
                w3.append(rows[2]["worth"]); w7.append(rows[6]["worth"]); w13.append(rows[-1]["worth"])
                e1.append(rows[0]["earned"]); e6.append(rows[STORY_WEEKS - 2]["earned"])
                for n, b, _ in checks(style, rows, levers, biggest, shops):
                    counts[n] = counts.get(n, 0) + b
            q = lambda v: f"{sorted(v)[len(v) // 10]} to {sorted(v)[9 * len(v) // 10]}"
            mp = "Act II's last week 3 to 10 times Act I's (MP-02)"
            single = counts.pop(mp, 0)
            mean_ratio = (sum(e6) / len(e6)) / max(1e-9, sum(e1) / len(e1))
            if style != "lazy":
                fails += not (3 <= mean_ratio <= 10)   # the curve's shape: mean week 6 against mean week 1 (single noisy weeks reported, not failed)
            bad = {n: c for n, c in counts.items() if c}
            fails += sum(1 for c in bad.values() if c > seeds // 20)   # any other check failing in more than 1 run in 20 is a breakage
            if style != "lazy":
                bad[f"MP-02 on single noisy weeks (mean ratio {mean_ratio:.1f})"] = single
            print(f"  {style}: worth week 3 {q(w3)}, week 7 {q(w7)}, week 13 {q(w13)} (10th to 90th); checks failed: "
                  + (", ".join(f"{n} in {c}" for n, c in bad.items()) if bad else "none"))
    print("\nTuning variants (what breaks if a figure moves; racketeer unless named):")
    variants = [("fare worth 1.30 (a London cab's rate), honest", "honest", dict(fare=0.43)),
                ("fare worth 1.30, mix", "mix", dict(fare=0.43)),
                ("protection 25 a shop (greedy)", "racketeer", dict(protection=2.5)),
                ("protection 40 a shop (bleeding the street)", "racketeer", dict(protection=4.0)),
                ("tobacco 95p to a shop, no extra cases at rung 4", "racketeer", dict(tobacco_price=190 / 170, tobacco_safe=0.5)),
                ("tobacco pushed past what the gate lets through", "racketeer", dict(push_tobacco=True)),
                ("a good rank pays a quarter more, honest", "honest", dict(good_rank=1.25)),
                ("choice 1 (a): drivers on a flat 90 a week, honest", "honest", dict(wage_model=True)),
                ("choice 1 (a): drivers on a flat 90 a week, mix", "mix", dict(wage_model=True)),
                ("a slack month at the docks (shops' takings down 15%, weeks 4 to 7), honest", "honest", dict(bad_season=True)),
                ("a slack month at the docks, racketeer", "racketeer", dict(bad_season=True)),
                ("ten lifts a week", "racketeer", dict(lifts=10))]
    for label, style, tune in variants:
        rows, levers, biggest, bought, shops = run(style, tune=tune)
        bad = [n for n, b, _ in checks(style, rows, levers, biggest, shops) if b]
        closed = [c[0] for r in rows for c in r["closed"]]
        r = lever_rates(levers)
        top = max(r.items(), key=lambda x: x[1]) if r else ("none", 0)
        r3 = next((x["week"] for x in rows if x["rung"] >= 3), None)
        lowd = rows[-1]["low_driver"]
        print(f"  {label}: rung 3 in week {r3}; driver's half under 60 in weeks {lowd or 'none'}; worth wk3 {rows[2]['worth']}, wk7 {rows[6]['worth']}, wk13 {rows[-1]['worth']}; lowest book {min(x['book'] for x in rows)};"
              f" dearest board {rows[-1]['boards']:.2f}; shut {closed or 'none'}; arrests {rows[-1]['arrests']}; best lever {top[0]} {top[1]:.0f}/h;"
              f" breaks {bad or 'none'}")
    fair = run("racketeer")[0]
    greedy = run("racketeer", tune=dict(protection=4.0))[0]
    g_bad = greedy[STORY_WEEKS - 1]["worth"] > fair[STORY_WEEKS - 1]["worth"]
    fails += g_bad
    print(f"\n{'FAIL' if g_bad else 'ok  '} squeezing the street (40 a shop) never ends the story richer than the fair round: week 7 "
          f"{greedy[STORY_WEEKS - 1]['worth']} against {fair[STORY_WEEKS - 1]['worth']} (after the story, week 13: {greedy[-1]['worth']} against {fair[-1]['worth']})")
    print(f"\nBreakages: {fails}")
    return fails


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
