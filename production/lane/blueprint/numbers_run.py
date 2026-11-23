#!/usr/bin/env python3
"""Numbers run for the LEDGER blueprint (23 Nov 2026): money across the calendar, the rivals' ladder, and repeats.

A small model of the design's own rules (DEFINITIONS-2026-11-21, ONE-SHOT-PROMPT, RULINGS on wip), not the game.
Where the design gives no amount, three bands (low, mid, high) are run and marked ASSUMED in the output.
Clock: his ruling of 21 Nov, 60 s a game hour, about 7 game weeks: Act I week 1, Act II weeks 2 to 6, Act III week 7.
Run: python numbers_run.py  (standard library only; prints the tables NUMBERS-RUN.md quotes)
"""
import itertools

WEEKS = 7
ACT = {1: "I", **{w: "II" for w in range(2, 7)}, 7: "III"}
BANDS = ("low", "mid", "high")

# ---- design figures (source in brackets) ----
START_POCKET = 23.50          # OSP s1
RENT = 18.0                   # OSP s1, weekly, Friday
WAGE = 90.0                   # DEF G8, per driver a week
DRIVER_BOOK_ACT1 = (85, 90, 95)      # DEF G8, per driver a week, Act I
CAR_BOOK_LATER = (110, 125, 140)     # DEF G8, per car a week, from rung 2
DEBTS = {"darren": 22, "wayne": 30, "lee": 15, "julie": 9, "dennis": 80}   # OSP s25, total 156 (Darren pays in news)
WASH_DAILY = 10.0             # DEF 2.7.3: the book hides 10 pounds plus 80% of fares really driven since the last wash
WASH_SHARE = 0.80
CAR_PRICE = (600, 900, 1200)  # DEF G8 used car at the lot
FENCE = 0.33                  # CLD B3 (OSP still says 0.4)

# ---- ASSUMED bands where the design has no amount ----
FARE_VALUE = (1.30, 3.00, 6.00)      # ASSUMED: 80p plus distance, no pence a mile given; 1.30 is FIT F24's London figure,
                                      # 2.30 to 10.28 is what the prototype paid (CHECK-1)
FARES_TOTAL = (40, 60, 80)            # DEF G7 offered in a playthrough (FIT F20 says 55 to 110)
NIGHT_CUT = (10, 25, 50)              # ASSUMED: Tom's cut of a landing run, "comes back", amount not given
ROUND_DAY = (20, 40, 60)              # ASSUMED: a collection round's day; the only figure is the old pub-era build's 60 a day
HOLDUP = (40, 120, 250)               # ASSUMED: "what the till holds that hour", no amount given
LIFT_RETAIL = (40, 120, 300)          # ASSUMED retail of the authored thing worth taking; fence pays FENCE of it
FRONT_SHARE = (300, 600, 900)         # ASSUMED: no price given; the old build's pawnshop was 900
FRONT_WASH_WEEK = (20, 50, 100)       # ASSUMED: "a set amount a week", not given
MAN_CUT = (10, 25, 40)                # DEF G8 crew night cut, agreed in talk, 10 to 40

WANTS = [  # (name, price or band, act it opens), in the order a player who is rising buys them; DEF G8 list, RT2-14 guns
    ("second-hand coat", 15, 1), ("crowbar", 6, 1), ("torch", 4, 1), ("key cut", 1.5, 1), ("barber", 4, 1),
    ("decent jacket", 45, 2), ("third car", "car", 2), ("doctor's stitches", 20, 2), ("good overcoat", 90, 2),
    ("fourth car", "car", 2), ("fifth car", "car", 2), ("a front's share", "front", 2),
    ("a brief on call, 4 weeks", 200, 2), ("bought officer, a statement", 200, 2), ("revolver", 150, 2),
]

PLAYERS = {
    # nights of the 7 played, debts taken, fares share of the offered, night runs a week, rounds from week, hold-ups, lifts a week,
    # men's night cuts paid a week, rung reached by week (rise), wants bought in order when cash allows
    "fares only": dict(debts=0.0, fare_share=1.0, runs=0, round_from=None, holdups=0, lifts=0, cuts=0),
    "steady": dict(debts=0.6, fare_share=0.7, runs=2, round_from=3, holdups=0, lifts=1, cuts=2),
    "hard": dict(debts=1.0, fare_share=0.4, runs=3, round_from=2, holdups=1, lifts=2, cuts=4),
}


def cars_owned(bought):
    return 2 + sum(1 for x in ("third car", "fourth car", "fifth car") if x in bought)   # start 2 (OSP s32); more only when bought


def money_run(p, b, wash_share=WASH_SHARE, own_fares_only=False):
    P, i = PLAYERS[p], BANDS.index(b)
    pocket, book, tin = START_POCKET, 0.0, 0.0
    rows, bought = [], []
    fares_week = FARES_TOTAL[i] / WEEKS * P["fare_share"]
    wants = [list(x) for x in WANTS]
    for w in range(1, WEEKS + 1):
        cars = cars_owned(bought)
        drivers = max(0, cars - 0)          # each car a paid driver; Tom's own fares on top
        per_car = DRIVER_BOOK_ACT1[i] if w == 1 else CAR_BOOK_LATER[i]
        firm_fares = drivers * per_car
        tom_fares = fares_week * FARE_VALUE[i]
        book += firm_fares + tom_fares - drivers * WAGE - RENT
        dirty = 0.0
        if w == 1:
            dirty += sum(DEBTS.values()) * P["debts"] - (22 * P["debts"])   # Darren pays in what he hears
        dirty += P["runs"] * NIGHT_CUT[i] * (1 if w == 1 else 1.5)
        if P["round_from"] and w >= P["round_from"]:
            dirty += ROUND_DAY[i] * 5
        if w >= 3:
            dirty += P["holdups"] * HOLDUP[i] * 0.5            # rare: one every other week at most
        dirty += P["lifts"] * LIFT_RETAIL[i] * FENCE
        dirty -= P["cuts"] * MAN_CUT[i] if w >= 2 else 0
        tin += dirty
        cap = 7 * WASH_DAILY + (WASH_SHARE * tom_fares + wash_share * firm_fares if own_fares_only else wash_share * (firm_fares + tom_fares)) + (FRONT_WASH_WEEK[i] if "a front's share" in bought else 0)
        wash = max(0.0, min(tin, cap))
        tin -= wash
        book += wash
        # buy wants in list order when the act allows and money covers
        for want in wants:
            name, price, act_open = want
            if name in bought or (act_open == 2 and w < 2):
                continue
            if p == "fares only" and name in ("third car", "fourth car", "fifth car", "a front's share", "revolver",
                                              "bought officer, a statement", "a brief on call, 4 weeks"):
                continue
            cost = CAR_PRICE[i] if price == "car" else FRONT_SHARE[i] if price == "front" else price
            if book + pocket >= cost:
                take = min(pocket, cost)
                pocket -= take
                book -= cost - take
                bought.append(name)
            else:
                break                      # saves for the next thing on the list rather than buying past it
        left = [x for x in wants if x[0] not in bought and not (p == "fares only" and x[0] in (
            "third car", "fourth car", "fifth car", "a front's share", "revolver", "bought officer, a statement", "a brief on call, 4 weeks"))]
        left_cost = sum(CAR_PRICE[i] if x[1] == "car" else FRONT_SHARE[i] if x[1] == "front" else x[1] for x in left)
        rows.append(dict(week=w, act=ACT[w], cars=cars, book=round(book), tin=round(tin), pocket=round(pocket),
                         wash_cap=round(cap), used=round(100 * (dirty + 0) / cap) if cap else 0, dirty=round(dirty), week_net=round(firm_fares + tom_fares - drivers * WAGE - RENT + dirty),
                         left=len(left), left_cost=round(left_cost)))
    return rows, bought


def week1_rent(b):
    i = BANDS.index(b)
    for n in range(0, 40):
        if START_POCKET + n * FARE_VALUE[i] >= RENT + 0.001 and n * FARE_VALUE[i] >= RENT:
            return n, FARES_TOTAL[i] / WEEKS


# ---- the rivals' ladder (RT2-07): noticed, visit, pressure, threat, sit-down ----
RUNGS = ["unknown", "noticed", "visit", "pressure", "threat", "sit-down"]
ACT2_START, ACT2_END = 8, 42            # game days, clock B
FAILSAFE_FROM = ACT2_END - 4             # four game days before Act II's last week ends


def ladder_run(style, hold_days=14, min_gap=0, sitdown_from=0):
    """style: payer (pays every pressure, no deeds), steady (pays once, rises, one deed a fortnight), hard (deeds and defiance).
    Returns the day each rival reached each rung and the day Act II ends (first sit-down)."""
    rivals = {r: dict(rung=0, held_until=0, last=-99, log={}) for r in ("widow", "agar", "cammack")}
    tom_rung = {8: 2}
    if style != "payer":
        tom_rung.update({22: 3, 35: 4})
    deeds = {"payer": [], "steady": [(16, "cammack"), (30, "widow")], "hard": [(9, "cammack"), (10, "cammack"), (11, "cammack"), (12, "widow")]}[style]
    defy = style == "hard"
    paid_once = set()
    end = None
    def lift(r, d, why):
        R = rivals[r]
        if R["rung"] >= 5 or d - R["last"] < min_gap:
            return
        if R["rung"] == 4 and d < sitdown_from and why != "fail-safe":
            return
        R["rung"] += 1
        R["last"] = d
        R["log"][RUNGS[R["rung"]]] = (d, why)
    for d in range(ACT2_START, ACT2_END + 1):
        tr = max(v for k, v in tom_rung.items() if k <= d)
        if d >= FAILSAFE_FROM:
            top = max(rivals, key=lambda k: rivals[k]["rung"])
            if rivals[top]["rung"] < 5:
                rivals[top]["last"] = -99
                lift(top, d, "fail-safe")
                rivals[top]["held_until"] = 0
        for r, R in rivals.items():
            held = d < R["held_until"]
            if R["rung"] == 0:
                lift(r, d, "first sighting")
                continue
            dd = [x for x in deeds if x[0] == d and x[1] == r]
            if dd:
                lift(r, d, "a deed against him")
                R["held_until"] = 0
                continue
            if held:
                continue
            if R["rung"] == 1 and (tr >= 2 or d - R["last"] >= 3):
                lift(r, d, "Tom at rung 2 or two more sightings")
            elif R["rung"] == 2:
                if style == "payer" or (style == "steady" and r not in paid_once):
                    R["held_until"] = d + hold_days
                    paid_once.add(r)
                    R["log"].setdefault("paid", []).append(d) if isinstance(R["log"].get("paid"), list) else R["log"].__setitem__("paid", [d])
                elif tr >= 3 or defy:
                    lift(r, d, "refused, or Tom at rung 3")
            elif R["rung"] == 3 and (defy or (style == "steady" and tr >= 3 and d - R["last"] >= 5)):
                lift(r, d, "defied or countered")
            elif R["rung"] == 4 and (defy or tr >= 4):
                lift(r, d, "defied, or Tom at rung 4")
            if R["rung"] == 5 and end is None:
                end = d
        if end is not None:
            break
    weeks_with_rung = set()
    for R in rivals.values():
        for k, v in R["log"].items():
            if k != "paid":
                weeks_with_rung.add((v[0] - ACT2_START) // 7 + 1)
    return rivals, end, sorted(weeks_with_rung)


# ---- repeats for a player who plays most nights ----
def repeats():
    out = {}
    hours = (15, 17.5, 20)
    days = 49
    nights_played = 42
    foot_share = 0.25                       # OSP s40
    for h in hours:
        foot_h = h * foot_share
        remarks_max = foot_h * 80           # FIT F19: up to 80 remarks an hour on foot
        remarks_mid = foot_h * 40
        out[h] = dict(foot_hours=foot_h, remarks_mid=round(remarks_mid), remarks_max=round(remarks_max),
                      happenings=round(h * 60 / 15), fares=None)
    # own lines: top 12 have 60, once a day; others 30, once a day
    own = dict(top12_days_before_repeat=60, others_days_before_repeat=30, nights_played=nights_played,
               others_repeats_if_met_nightly=max(0, nights_played - 30))
    return out, own


def main():
    print("== Week one: fares needed to pay the first Friday from fares alone (ER-MONEY-03) ==")
    for b in BANDS:
        n, offered = week1_rent(b)
        print(f"  {b:5s} fare {FARE_VALUE[BANDS.index(b)]:.2f}: {n} fares needed; design offers about {offered:.1f} a week (G7 {FARES_TOTAL[BANDS.index(b)]} a playthrough)")
    print()
    print("== Money by week (pounds; book = clean, tin = unwashed night money) ==")
    for p, b in itertools.product(PLAYERS, BANDS):
        rows, bought = money_run(p, b)
        print(f"-- {p}, {b} band --")
        print("  wk act cars  book   tin  dirty  wash_cap used%  week_net  wants_left (cost)")
        for r in rows:
            print(f"  {r['week']:2d} {r['act']:>3s} {r['cars']:4d} {r['book']:6d} {r['tin']:5d} {r['dirty']:6d} {r['wash_cap']:8d} {r['used']:5d} {r['week_net']:8d}   {r['left']:2d} ({r['left_cost']})")
        print("  bought:", ", ".join(bought) or "nothing")
    print()
    print("== Wash limit variant: 10 a day plus 80% of Tom's own fares and 40% of the drivers' (dirty as share of the limit) ==")
    for p, b in itertools.product(("steady", "hard"), BANDS):
        rows, bought = money_run(p, b, wash_share=0.40, own_fares_only=True)
        print(f"  {p:6s} {b:5s} used% by week: " + " ".join(str(r["used"]) for r in rows) + f"; tin left at week 7: {rows[-1]['tin']}; cars {rows[-1]['cars']}")
    print()
    print("== Rivals' ladder, clock B (Act II days 8 to 42, fail-safe from day 38) ==")
    for style in ("payer", "steady", "hard"):
        for gap, sd in ((0, 0), (4, 0), (4, 29)):
            rivals, end, weeks = ladder_run(style, min_gap=gap, sitdown_from=sd)
            tag = "as designed" if gap == 0 else (f"fix: one rung a rival every {gap} game days" + (f", sit-down not before day {sd} (Act II week 4)" if sd else ""))
            print(f"-- {style}, {tag}: Act II ends day {end} (week {None if end is None else (end - ACT2_START)//7 + 1} of Act II); weeks of Act II with a rung change: {weeks}")
            for r, R in rivals.items():
                print(f"   {r:8s} " + "; ".join(f"{k} {v[0] if not isinstance(v, list) else v}" for k, v in R["log"].items()))
    print()
    print("== Repeats, a player on most nights (42 of 49) ==")
    out, own = repeats()
    for h, v in out.items():
        print(f"  {h} h: on foot {v['foot_hours']:.1f} h, street remarks {v['remarks_mid']} (40 an hour) to {v['remarks_max']} (80 an hour), happenings at one per 15 min {v['happenings']}")
    print("  own lines:", own)


if __name__ == "__main__":
    main()
