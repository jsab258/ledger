# One-shot status: cars and fares (builder "cars")

Kept current at each checkpoint. Systems: cars, fares. Tests: `node test/pieces.mjs car_rules fare_rules` (90 cases), test/game/fares.mjs, test/game/cars.mjs.

## Parts

(first shallow pass committed 09:40; statuses below are filled in as the tests run)

## Known faults

- The shared test harness (project/test/harness.mjs, not this builder's file) had its port line broken by the port-shift edit: the comment swallowed the window size, so no browser test could start. Mended in this branch by moving the comment; every builder needs the same one-line fix.
- The machine is shared by nine builders: a browser test that takes 20 s alone takes many minutes here, and browsers are killed for want of memory.

## Needs from others
