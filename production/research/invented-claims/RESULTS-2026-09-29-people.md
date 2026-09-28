# The claim check with what characters know of the street's people, 29 September 2026

Town list 6ad gives each character lines about the people and places of the
street (CastDay.PeopleFor), and the claim check reads them as P items: a habit
cited to one goes to the second look, which may clear it from P items; an event
it may clear only from other items. The independent check asked whether those
lines let invented details through, since the bench never passed them.

Measured on the bench's held-back half (240 turns, the same drafts and gold
labels as 28 September), the live check (v3v), both runs on 29 September:

| | invented turns caught | clean turns flagged | cost |
|---|---|---|---|
| without the street's people | 95/108 (88%, 95% 80-93%) | 42/132 (32%) | $1.05 |
| with them (--people) | 98/108 (91%, 95% 84-95%) | 43/132 (33%) | $1.65 |

Turn by turn: 3 invented turns caught before were missed with them, 6 the other
way; 13 new false alarms, 12 gone. That is the checker's own run-to-run noise;
no loss is measurable. Files: bench/check.v3v.held.2026-09-29.jsonl and
bench/check.v3v.held.people.jsonl (`dotnet run --project ledger/ClaimBench -c
Release -- check v3v --half held --people`).
