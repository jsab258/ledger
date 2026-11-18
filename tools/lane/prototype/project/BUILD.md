# Building LEDGER

## The command

    npm ci
    npm run build

`npm run build` runs `node tools/build.mjs`. It bundles `src/main.js` with esbuild into `dist/ledger.js`
(one file, minified), copies `src/index.html` to `dist/index.html`, and copies the art from `assets/`
into `dist/`. That folder is the page. `npm run build:dev` is the same without minifying, with a source map.

## Pinned versions

| Package | Version | Used for |
| --- | --- | --- |
| three | 0.187.0 | the only dependency of the game |
| esbuild | 0.28.2 | the build |
| prettier | 3.3.3 | formatting (`npm run format`) |
| eslint | 8.57.0 | undefined names and unused imports (`npm run lint`) |
| puppeteer-core | 25.17.0 | the tests only |

All five are exact in `package.json`, and `package-lock.json` holds the rest. Built here with Node 22.23.4
and npm 10.9.9.

## Checking that the page is what this source builds

1. `npm ci && npm run build`
2. `sha256sum dist/ledger.js dist/index.html`
3. Compare with the checksums at the foot of the published `BUILD.md` (also in `files.json`, as
   `ledgerJsSha256` and `indexHtmlSha256`), or with the published `ledger.js` and `index.html` themselves.

I built it twice on one machine (Linux, x64) and got the same file both times. I have not built it on a
second machine, so I cannot promise the checksum on another system. If it differs there, the bundler's
output is the place to look, not the source.

## The art

`assets/` holds the art as it is used: `people.txt` and `people.jpg` (the rigged figures and their
animations, packed by `tools/pack_people.mjs` from Quaternius' CC0 files, which are not in this
repository), `people_lo.jpg`, and ten ground and wall pictures from Poly Haven (CC0). The build copies them
unchanged. The published art files are byte for byte the ones in `assets/`.

## The tests

    npm test

They need Chrome. The harness looks for `/usr/bin/google-chrome`; set `CHROME` to another path if needed.
The tests step the game by hand through the test hook, so they do not depend on the machine's speed.

## Publishing

`npm run publish-set` writes `site/`: the page, the art, the documents, `measures.json` from the last
`test/week.mjs` run, the source under `source/`, and `files.json`, which the game's "Source and files"
screen reads.

## This publication

Published 2026-11-18.

    73245b8eb8b353a9cbebb0bdb7be20c05c148f7c47de63917c21c03142fcd29e  dist/ledger.js
    f0e85bbbf5ec67ac9cdbba338428cdfcb8b1505afc03585dfe2a33887b328f61  dist/index.html
