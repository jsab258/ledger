# Attach the addendum's experience rules to their parts (appended to each part's test).
from tree_a import PARTS
ER = {"1.1.5": "ER-HIDE-01 to 03", "1.1.6": "ER-TAIL-01 to 03", "1.2.6": "ER-TAIL-01 to 03", "1.5.2": "ER-PURSUE-01 to 02",
 "1.6.2": "ER-SEARCH-01 to 02", "1.6.9": "ER-POCKET-01 to 02", "7.10": "ER-ASSIST-01 to 02", "8.4.1": "ER-ASSIST-01",
 "7.15": "ER-AFTER-01", "5.7": "ER-MUSIC-01", "6.9": "ER-WAY-01 to 03", "1.4.7": "ER-MANNER-01", "1.1.7": "ER-STOP-01",
 "2.2.6": "ER-GROUND-01", "4.2.4": "ER-WATER-01 to 02", "2.6.7": "ER-TRAFFIC-01 to 02", "2.6.8": "ER-BOUGHT-01",
 "2.6.9": "ER-SEARCHED-01", "2.15.1": "ER-FIRM-01 to 02", "2.15.2": "ER-FIRM-01", "2.17": "ER-FRONT-01 to 02",
 "1.7.4": "ER-SIDE-01", "3.5.7": "ER-REACH-01", "3.7": "ER-HAPPEN-01 to 02", "2.4.5": "ER-PAPER-01", "2.1.6": "ER-CAL-01 to 02",
 "2.7.8": "ER-SPEND-01", "1.6.10": "ER-COAT-01", "1.3.11": "ER-MARK-01", "2.18": "ER-AMB-01", "1.6.11": "ER-CASE-01",
 "4.11.1": "ER-DOG-01", "1.2.8": "ER-RIDE-01", "1.2.9": "ER-PAINT-01", "3.6.8": "ER-SPEAK-01", "1.1.8": "ER-VAULT-01",
 "1.2.10": "ER-TAKE-01", "7.16": "ER-PASTIME-01"}
by = {p["id"]: p for p in PARTS}
for k, v in ER.items():
    by[k]["t"] = by[k].get("t", "") + "; addendum rules " + v
for k, v in {"1.3.2": "ER-DEFEND-01 to 02", "1.3.12": "ER-TYPES-01", "2.7.5": "ER-HAGGLE-01", "6.1.5": "ER-TIME-01"}.items():
    by[k]["t"] = by[k].get("t", "") + "; addendum rules " + v
by["1.3.2"]["des"] = by["1.3.2"]["des"] + "; " + "DESIGN-ADDENDUM-2026-11-20 §A29 (guard, slip, counter, breath, grab)"
by["2.7.5"]["des"] = by["2.7.5"]["des"] + "; DESIGN-ADDENDUM-2026-11-20 §A30 (haggling)"
