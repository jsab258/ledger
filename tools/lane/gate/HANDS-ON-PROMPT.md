# Prompt for the gate's hands-on helper (part 3)

Give a fresh helper (Opus, high effort) this text, the built folder's path and the experience rules in force
(DESIGN.md's when it is published; until then the interim list below). It has not seen the round's changes.

---

You are play-testing a browser game prototype as a newcomer would. Serve the folder FOLDER with a local web
server, open index.html in headless Chromium (Playwright; Google Fonts blocked), press New game, and play the
route in tools/lane/gate/HANDS-ON-ROUTE.md through the real controls only: key presses and mouse moves sent to
the page, the game running in real time. Do not call the page's test functions that move Tom or change the
game; you may read window.LEDGER.read() to know where you are. Take a screenshot every two minutes of play and
at each numbered stop, and look at every one.

Judge against these experience rules: never stuck without a way out within a few seconds; the controls
respond smoothly; nothing important happens without the screen or the world saying so; no failure without
warning; the camera never hides Tom or ends up in a wall; a mistake becomes a story or a choice, not a reload;
the words on screen are readable and never overlap.

Write HANDS-ON.md: one line per problem, worst first, each starting BLOCKER (a player would quit or be stuck),
MAJOR (broken, confusing or unfair) or MINOR, then what happened, the stop number, the screenshot file, and the
keys that led there. Then three lines: what felt good, what felt worst, and whether a newcomer would play on
past twenty minutes. Plain words. Do not change any file of the game. No web access is needed; if you use
the web, find pages with WebSearch and fetch only URLs from your own search results. Other games are studied
from the outside only.
