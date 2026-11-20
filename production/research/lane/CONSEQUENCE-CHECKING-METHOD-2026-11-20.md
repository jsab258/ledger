# Checking consequences by machine: the method (lane task 4t, piece 5)

Written by the cloud lane, 20 Nov 2026, 03:30 Swiss time. The question: how to prove, from a played session, that every reaction in the town traces back to a chain of sightings and tellings, with no line repeated, nothing wrong for 1990 and the content rule kept (his words of 19 Nov).

## Sources (read 20 Nov 2026)

| Source | What it says | What we take |
|---|---|---|
| Simon Varvaressos, "Etude de faisabilite du runtime monitoring dans les jeux video", master's thesis, UQAC, January 2014 (advisor Sylvain Halle). https://constellation.uqac.ca/2791/1/030622621.pdf | Each loop of the game writes a snapshot of its state; the snapshots in order are a trace; a bug is written as a property over the trace (temporal logic over the state's values) and a monitor returns false or inconclusive. Example from Infinite Mario Bros: every jump height stays under the screen's height. Read through a helper: the method part came from the helper's summary of the later pages, so treat the detail as unverified. | The shape of the checker: snapshots of the game's own state (its saved week), rules written as properties over them, a rule that cannot be evaluated reported as not reached, never as passed. |
| Ryan, Summerville, Mateas, Wardrip-Fruin, "Toward Characters Who Observe, Tell, Misremember, and Lie", AIIDE workshop on Experimental AI in Games, 2015. https://ojs.aaai.org/index.php/AIIDE/article/view/12825 | Talk of the Town's characters observe, form knowledge, pass it on, misremember and lie. Only the abstract was read; the paper's account of how each belief keeps its source was not reached. | Unverified as to Talk of the Town's own fields. LEDGER's memories already carry their source (saw, heard, was part of it, told, with the teller's name and a hop count), so each belief can be walked back to the act; the checker relies on LEDGER's own fields, not on Talk of the Town. |

Kingdom Come II and Mafia: none found on how either checks its consequences by machine.

## The method as built

1. Snapshots: the game's own saved week (every event with its witnesses and parties, every person's memories with source, teller and minute, every telling) at the start and the end of a stretch; play.py now also keeps one every 10 actions in the hidden folder.
2. Properties over the snapshots (tools/lane/gate/consequences.py): a memory names a real event and is not older than it; a sighting has its witness; a sound is heard as it happens; a telling names its teller, is recorded, and the teller knew first; every chain of tellings ends at someone who saw, heard or was part of it, with no loop; every telling left its memory; anyone whose regard or fear moved holds a memory. The words: no spoken line of five words or more shown again after ten game minutes off screen; no word of a later year or another country (a fail list and a warn list); the content words.
3. Two ways in: its own run of game hours (code, no model, about 40 seconds for 12 game hours in the cloud) on every gate run, and a played session's hidden folder once per loop.
4. Planted faults: each property has a unit test that plants the fault in a clean week and requires the catch (test_consequences.py), the start of piece 8.

## Limits, named

- A "was part of it" memory with no party recorded is counted, not failed: the story seeds some (the inheritance) without naming parties, and the save does not say which.
- Police coming, the watchers' "takes him for" and the Ledger's sureness are not traced yet.
- The 1990 read is a word list; a Sonnet read of all lines for things a list cannot catch (prices, songs, events after 1990) is left for a loop if the list proves thin.
- Live talk runs only inside claude.ai, so live lines are not in the cloud's sessions.
