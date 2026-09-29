# The town's own news: the one sample

Town list 6aq. The sample stands as written (29 September, DECISIONS); the ten
more wait until Jafar has met this one in the assembled game. Design:
game-design/town-news-sample-2026-09-29.md. Code:
ledger/Assets/Scripts/Core/TownNews.cs and production/specs/town-news.json.

**What the player gets:** in the first hours, the street has news of its own,
not about him: "Hal and Rita had words in the pawn, and nobody knows what
about". It is seen by everyone in the pawn when Hal calls on a Monday, spread
by the town's rounds, and told in exchanges he can overhear.

## Wire it

1. **Once, at load:** `news = TownNews.Parse(the text of production/specs/town-news.json)`.
2. **Each game hour:** `news.Seed(mill, cast, now)`. It files each story
   through `Witness` for everyone in its area at its hour.
3. **Keep** `TownNews.Filed` (in `TownSave.NewsFiled`) and the `RemarkLedger`'s
   story counts in the save.
4. **Voices:** the twenty telling and reply lines (banks exchange/tell/news and
   exchange/reply/news).

## Port

`TownNews` and `StreetVoice.Exchange`'s news branch, with `RemarkLedger`'s story
count. Match the rows behind `--awaiting-port`: `TownNews` and
`TownNewsWitnesses`.

## Save

`TownSave.NewsFiled`.

## Walk it

On the first Monday, pass the pawn in the morning and loiter on Quay Street.
Within a minute or so two neighbours are talking about Hal and Rita having
words, in different words each time.
