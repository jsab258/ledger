# Ruling, 2026-09-15: ten hours, and the brief asks for the reading

> **STATUS: LOG, 2026-09-15. NOT CURRENT** once queue 314 lands the two tool
> changes and the bound is enforced mechanically rather than by judgement.
> Jafar's ruling, dictated in his own words and recorded by the resident. It
> replaces the forty-eight-hour staleness bound in `production/budget.md`
> stop condition 2 and adds a standing first line to every brief.

## The rule, as given

**"The ceiling does not brake anything, because you cannot read the meter and
work from whatever number I last typed. A night can spend thirty points while
every check says the morning's figure."**

**Change one. "A reading older than ten hours means the day is unmeasured:
inbox half only, no builders, no dispatches, no renders. Not forty-eight
hours, which is longer than a night that can spend a third of a week."**

**Change two. "And the brief asks for the reading as its first line, every
morning, and the studio holds at inbox-only until I answer. No reading, no
spending. That way I am asked once a day rather than having to remember, and
forgetting costs nothing."**

## Why the ceiling was not a brake, which is his diagnosis and it is correct

The ceiling is 85 percent on the governing meter. Nothing in the container can
read the meter: `production/budget.md` says so in its own words, "Nothing in
the container can read Jafar's usage page." So every check compares work
against the last number he typed. A meter that only moves when he speaks
cannot stop a night, and the file's own history shows the failure twice: the
four Fable refusals of 13 and 14 September are what a spent weekly meter looks
like from inside a container still reading a stale figure and still believing
it had room.

Forty-eight hours made that worse rather than better, and his sentence is the
whole argument: a night is shorter than the bound meant to catch it. The
window this session measured on its own budget row was 9 points on the total
and 11 on Fable across one night, against a ceiling of 85. Two such nights
inside one forty-eight-hour window pass every check.

## What lands where, and what does not

RECORDED TONIGHT, in prose, by the resident:
  `production/budget.md` stop condition 2, rewritten to ten hours with both
    halves of the ruling and its consequence spelled out.
  `production/repo-move-triggers.md` step 3, the hourly trigger's own text.
  `production/watchdog-prompt.md`, the same sentence.
  `.claude/agents/producer.md`, where the reading becomes item 0, the first
    line of every brief, explicitly NOT a NEEDS YOU item because it carries no
    default: a day he does not answer is a day the studio does not spend, and
    that is the ruling working rather than failing.

NOT LANDED TONIGHT, AND THE REASON IS THE RULING ITSELF. Two tool changes are
needed to make this mechanical rather than a matter of judgement:
`tools/producer-check.py` must require the reading line in the brief register,
and `tools/morning-brief.py` must evaluate ten hours instead of
`BUDGET_STALE_DAYS = 2`. Both are builder work. HIS READING IS FIFTEEN HOURS
OLD AS THIS IS WRITTEN, so the day is unmeasured and his own rule forbids
spawning a builder. The rule bit its author's request first, which is the
right way round. Filed as queue 314, behind his next reading.

## The thing the bound needs that the table does not carry

Said here because a rule nothing can evaluate is decoration. Every budget row's
date column is a DATE; its time lives in prose as "Reported by Jafar at about
04:1xZ", which is not a parseable instant and in that literal case is not even
a parseable time. Forty-eight hours survived on date arithmetic, and
`tools/morning-brief.py` says so in its own comment: "The table's granularity
is a DATE, not an instant, so 48 hours is read as two days." TEN HOURS CANNOT
BE READ THAT WAY.

So from this ruling every row carries `takenAt=<ISO instant>`, STAMPED BY THE
RESIDENT AT THE MOMENT THE READING ARRIVES rather than asked of him. When it
arrived is what staleness is actually about, and asking him for a precise clock
time would reintroduce the remembering he just ruled away. A row with no
`takenAt` reads as UNMEASURED rather than as fresh, which is the conservative
direction and the only safe one.

TODAY'S ROW IS NOT BACK-STAMPED. It says "about 04:1xZ" and inventing a
precision it never had would be a fabricated instant on the very row the new
rule is first evaluated against. The convention starts with his next reading.
Today's row reads unmeasured under the new bound, which is also what the clock
says: 04:1xZ to 19:1xZ is fifteen hours.

## What this ruling costs him, which is the point of change two

Nothing. He is asked once, in the first line of the one message a day he
already gets, and if he does not answer, the studio does not spend. There is no
state for him to hold and no consequence to forgetting.
