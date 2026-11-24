# Prices and wages the game uses, 1990

Design pass, 24 Nov 2026 (due Thu 26 Nov 12:00), lane-2026-11, Opus 5.5. The figures the economy run (economy_run.py) and the design (ECONOMY-DESIGN-2026-11-26.md) use, each with its source and the date it was read. This is the "G8 price check" that NUMBERS-RUN.md and FIT-G8 were waiting for.

How to read the labels:
- SOURCED: a dated 1990 (or 1988 to 1991) figure read in full on the page named, on 24 Nov 2026.
- DERIVED: arithmetic on a sourced figure; the working is given.
- INFERRED: no 1990 source was reached; the figure is a judgement, with its reasoning. An unreached source is never evidence, so every INFERRED figure is open to a better one.
- DESIGN: the blueprint's own figure, kept because it sits inside the sourced band.

Built on: CLOUD-FIGURES-2026-11-21.md B1 and B3 (rents, London fares, diesel, the fence's third), research/cab-office-1990 (the settle, the two firm models, Hamiltax, the radio licence, VAT), research/street-lines-1990 (prescription 3.05, dental check 3.15), production/art/atlas-02 (average gross weekly earnings 263.10 in 1990, men 295.60, women 201.50), research/shop-hours-1990 (opening hours, early closing, Sunday), BLUEPRINT-02 2.7 and FIT-G8 (the spending list), BLUEPRINT-04 4.3 (the trades of Quay Street). Nothing here repeats a study already done; where this file and an earlier one differ, the difference is named at the end.

Regional note: Meridian is a northern English port town (a Humber town in the old research). Wages there ran below the national average and house prices well below it (the North and Yorkshire and Humberside were the two cheapest English regions in 1989, below). Where a wage or a rent is national, the game's figure is set a little under it and says so; prices of goods (tobacco, petrol, food) were much the same across the country and are used as national.

## 1. Everyday prices (what a shop board or a seller says)

| Item | Game price | Label and source |
|---|---|---|
| 20 cigarettes, a good brand | £1.70 | SOURCED and DERIVED: UK average retail price of 20, 12 Feb 1990: 161p, of which tax 118p (73%) (Hansard written answer, 14 Feb 1990, "Cigarettes"); the RPI cigarette index stood at 91.6 in Jan 1990 against 100 in Jan 1991 (Hansard, 20 Mar 1991, "Retail Prices"), so about £1.76 by Jan 1991. £1.70 is mid-1990, after the March Budget. Matches the design's £1.70. |
| 20 cigarettes, smuggled, from a stall or under the counter | £1.10 to £1.30 | INFERRED from the 73% tax share: a pack off the boat costs the smuggler about 40p to 50p before duty; resale well under the legal £1.70 |
| A pint of milk (doorstep or shop) | 30p | SOURCED: pasteurised milk 30.5p a pint, 1990 average (Hansard, 15 Mar 1991, "Food Prices"; the printed figure has a footnote digit run into it, read as 30.5p, which matches 3 minutes' work for a pint in Apr 1990, Hansard 20 Mar 1991) |
| A white sliced loaf | 52p | DERIVED: 48.8p in 1989 (CSO, Hansard 28 Feb 1990, "Bread Prices"); the sliced loaf's index rose 8.8% from Jan 1990 to Jan 1991 (Hansard 20 Mar 1991), so about 52p in mid-1990. A baker's white unwrapped 800 g loaf averaged 65.2p in 1990 (SOURCED, Hansard 15 Mar 1991, footnote digit removed). |
| Tea at the caff | 30p | DESIGN; INFERRED as sitting just above the price of a pint of milk |
| A caff breakfast (egg, bacon, sausage, beans, toast, tea) | £1.80 | INFERRED: no 1990 caff price reached; set between the 30p tea and the £2.50 meal |
| A caff meal (dinner at midday) | £2.50 | DESIGN |
| Fish and chips at the chip shop | £1.60 | INFERRED: cod about £2.60 a pound at the fishmonger (archived DECISIONS 13 Oct, one source) |
| The paper | 25p | DESIGN; INFERRED as a 1990 daily's price |
| A bus ride across town | 45p | INFERRED: no 1990 fare reached (the 10 Jul 1990 Hansard table did not print); local fares outside London rose 11 to 19% from 1985-86 to Sep 1988 (Hansard, 25 May 1989, "Bus Fares"). Buses are scenery, so the figure is only spoken. |
| Four-star petrol, a gallon | £2.00 | SOURCED and DERIVED: premium petrol with tax 40.89p a litre (£1.86 a gallon) in Oct 1989 (Hansard, 13 Feb 1990, "Petrol Prices"); the price before tax rose from 15.1p a litre in Jan 1990 to 21.7p on 17 Sep 1990 after the Gulf crisis (Hansard, 15 Oct 1990); four-star 45.4p a litre (£2.06 a gallon) in Northern Ireland on 16 Jan 1991 (Hansard, 19 Feb 1991). So about £1.90 early in 1990 and £2.05 to £2.15 by the autumn; the game uses £2.00. |
| Diesel, a gallon | £1.75 | SOURCED for 1989 and DERIVED for 1990: 34.2p to 37.3p a litre with tax, Jan to Oct 1989 (£1.55 to £1.70 a gallon) (Hansard, 13 Feb 1990); raised for the March 1990 duty rise and the autumn's Gulf rise (petrol before tax up 6.5p a litre, Hansard 15 Oct 1990), so about 38p a litre. The old "about 45p a litre" (CLOUD-FIGURES B1, a driver's recollection) is high for 1990 and is replaced. |
| Prescription, an item | £3.05 | SOURCED earlier (research/street-lines-1990, from 1 Apr 1990) |
| A crowbar, torch, key cut | £6, £4, £1.50 | DESIGN |
| Coats: second-hand, decent jacket, good overcoat | £15, £45, £90 | DESIGN |
| The barber | £4 | DESIGN |
| The retired doctor's stitches | £20 | DESIGN |

## 2. Fares, cars and running a cab

| Item | Game figure | Label and source |
|---|---|---|
| The firm's fare | 80p to start, then £1.10 a mile; nights (22:00 to 06:00) and Sundays a quarter more | DERIVED: a 1990 survey priced a 2.5-mile daytime taxi trip at £3.00 to £3.70, about £1.20 to £1.50 a mile (research/cab-office-1990, S9); London cabs from 8 Jun 1990 about £1.04 a mile after a £1.00 start (CLOUD-FIGURES B1). Private hire fares were unregulated (cab research S8), so the firm sets its own and is a little under a hackney. A Hook fare of 1 to 2.5 miles comes to £1.90 to £3.55; the typical fare the run uses is £3.00. This settles NUMBERS-RUN M1 (2.50 to 3.50). |
| A car's week on a dead firm's rank (takings before the split) | £130 | INFERRED from the design's £85 to £95 a week to the book (FIT-G8), restated as takings under the split in section 4 |
| A car's week on a good rank, from rung 2 | £210, plus £40 with the cold-store contract | INFERRED, same way, from the design's £110 to £140 (tuned in the run, ECONOMY-DESIGN section 7) |
| Fuel, a car a week | £26 | DERIVED: about 400 miles at 30 mpg is 13 gallons at £2.00 |
| Hire-and-reward insurance, a car a week | £12 | INFERRED: "very expensive" (cab research S16), no figure; about £600 a year |
| Repairs and tyres, a car a week | £8 | INFERRED |
| Radio licence | £120 a year (about £2.30 a week) | SOURCED earlier (cab research S11, from 1 Nov 1989) |
| Office running (phone, electric, radio licence) | £12 a week | INFERRED, the licence included |
| A tired saloon at the lot | £600 to £1,200 (the run uses £900) | DESIGN; INFERRED: no 1990 used-car price list was reached (present-day guides only) |
| A car on terms (hire purchase) | about £90 down and £22 a week for a year | INFERRED: about a tenth down; £22 a week for 52 weeks is £1,144 on the £810 owed, a flat charge of about 40%, dear because a run-down cab firm is a poor risk (a good customer paid nearer 25% flat, about £19.50 a week); adopts NUMBERS-RUN M3's fix |
| The settle a self-employed driver pays a firm (the other model) | about £50 a week | DERIVED earlier (cab research: £80 in 2004, RPI back to 1990) |

## 3. Rent and property in a northern port town

| Item | Game figure | Label and source |
|---|---|---|
| Mickey's office and the flat above | £18 a week | DESIGN; cheap against the 1990 band below, a run-down office let by an old acquaintance (CLOUD-FIGURES B1 reading kept) |
| A council house | £23 a week | SOURCED earlier: £23.36, England, Apr 1990 (Hansard, 27 Jun 1990, in CLOUD-FIGURES B1) |
| A privately rented terraced house | £35 a week | INFERRED: England's private average was £65 in 1991 (Hansard 15 Apr 1993, in B1), pulled up by London and the South East; a northern terrace sits about half of it |
| A flat or rooms | £25 a week | INFERRED, as above |
| A small shop unit on the parade (the empty unit to let) | £25 to £35 a week | INFERRED: no 1990 figure for a northern parade reached |
| A terraced house to buy | about £25,000 | DERIVED: average price of a dwelling bought with a building society mortgage in 1989: North £37,374, Yorkshire and Humberside £41,817, England £58,458, Greater London £82,383 (Hansard, 9 Jul 1990, "House Prices"); a Hook terrace in a run-down port quarter is set well under the regional average |

## 4. Weekly pay (gross)

| Who | Game figure | Label and source |
|---|---|---|
| A man in manual work outside factories | £227 | SOURCED: full-time adult manual men, non-manufacturing, Apr 1990: £227.10; women £143.40 (Hansard, 1 Nov 1990, "Earnings", New Earnings Survey) |
| All full-time adults, UK | £239 (Apr 1989); £263 (1990) | SOURCED: £238.90, Apr 1989 (Hansard, 22 May 1990, "Wages"); £263.10 for 1990 held earlier (atlas-02) |
| A docker (after the Dock Labour Scheme ended, Jul 1989) | £190 to £230 | INFERRED: Hansard of 8 May 1989 and 24 Apr 1989 says port pay outside the scheme was not collected; after abolition no register existed (Hansard, 23 Jul 1990); set around the £227 manual figure, lower for casual men |
| A lorry driver | £255 | DERIVED: male heavy goods drivers £216.90 in Apr 1988 (Hansard, 17 Jul 1989, "Lorry Drivers' Pay"), raised by the national rise for all full-time adults to Apr 1989 (£217.70 to £238.90, 9.7%, Hansard 22 May 1990) and about 8% to 1990 (INFERRED), giving about £257 |
| A cab driver at Mickey's | half his takings: about £65 a week on a dead rank, £105 on a good one, £125 with the contract | DERIVED from section 2 under the recommended split (ECONOMY-DESIGN, choice 1); low against a lorry driver's £255, which is why drivers in 1990 were often part-time or doing a second job, and why a driver leaves when his half falls |
| Shop staff (a full-time assistant) | £120 | INFERRED: under the £143.40 for women in manual work outside factories; shop pay was set by wages councils in 1990 and no rate was reached |
| A police constable | £190 to £318 (Sep 1989 scale); about £205 to £345 in 1990 | SOURCED and DERIVED: constable £9,900 to £16,521 a year, sergeant £15,804 to £18,129, inspector £18,129 to £20,583, from 1 Sep 1989 (Hansard, 9 Jul 1990, "Police Pay and Manpower"); the Sep 1990 rise not reached, about 9% assumed |
| DS Carol Ellis | about £330 to £380 | DERIVED: a sergeant's scale above, with the 1990 rise and a detective's allowance assumed |
| A shopkeeper's own draw | £90 to £140 | INFERRED (the run's shops, section 5) |
| Unemployment in a 1991 Humber town | about 12% | SOURCED earlier (research/casting, 1991 census, Hull) |

## 5. The shops' weeks (economy_run.py)

All INFERRED: takings a week, then stock and costs as a share, rent, staff and the owner's draw. Scaled so a shop's owner draws about what a manual worker earns, the newsagent turns over most because tobacco is dear and mostly tax, and the margin left is small (£45 to £175), which is what makes protection felt.

| Shop | Takings | Stock and costs | Rent | Staff | Owner | Margin left |
|---|---|---|---|---|---|---|
| Fishmonger | £1,100 | 70% | £30 | £110 | £120 | about £70 |
| Grocer | £1,500 | 76% | £35 | £120 | £120 | about £85 |
| Newsagent and tobacconist | £1,900 | 82% | £35 | £100 | £110 | about £97 |
| Launderette | £420 | 30% | £30 | £60 | £110 | about £94 |
| Caff | £750 | 50% | £30 | £120 | £120 | about £105 |
| Chip shop | £900 | 55% | £30 | £110 | £130 | about £135 |
| Ironmonger | £650 | 62% | £30 | £60 | £110 | about £47 |
| Tea room | £380 | 45% | £25 | £50 | £90 | about £44 |
| Pawn | £700 | 40% | £35 | £70 | £140 | about £175 |

## 6. Cuts, rates and prices of the night

| Item | Game figure | Label and source |
|---|---|---|
| A fence (Rita's back room) | about a third of retail: 0.2 jewellery to 0.4 a video recorder | INFERRED from later studies, as CLOUD-FIGURES B3 itself says (Sutton 2014, AIC 2002, BOCSAR 1998; no 1990 British figure exists in public); the 0.2 and 0.4 are B3's reading |
| Smuggled cigarettes, a fence's rate | 30 to 40% of retail | INFERRED from a later study (Sutton 2014, in B3); the game's 80p a pack to a stall is 47% of £1.70, a little dearer because the buyer resells |
| The pawnbroker's loan on a pledge | about a third of the second-hand value, at about 6% a month | INFERRED: pawnbroking law changed in 1985 (shop-hours research [3]); no 1990 rate reached |
| Buying back what Tom sold | within 7 game days, from the shop or pawnbroker that bought it, at what it paid plus a quarter; a fence holds nothing | DECISION of 24 Nov (the brief) |
| An unlicensed lender's rate | "a pound in five a week" (20% a week) | INFERRED: the Hansard answers of 12 Feb and 16 Nov 1990 on loan sharks and moneylenders give no rate |
| Protection, a shop a week | £5 to £15, set by what the shop can bear | INFERRED, from section 5's margins |
| A bought constable | £50 to look away once, £200 to lose a statement once | DESIGN |
| DS Ellis | about £800 (two and a half weeks of her pay) and £100 a week while bought | DECISION of 24 Nov that she can be bought, at a high price; the amount INFERRED from section 4 (ECONOMY-DESIGN, choice 2) |
| A man's night cut | £10 to £40 | DESIGN |
| A man posted at the gate, the cold store or the landing | £40 a week | INFERRED: a part-time wage beside the £227 manual figure |
| A solicitor's brief on call | £50 a week | DESIGN |
| VAT threshold | £25,400 a year from 21 Mar 1990; 15% | SOURCED earlier (cab research) |

## 7. Where this file differs from earlier figures

- Diesel: CLOUD-FIGURES B1's "about 45p a litre" (a recollection in a 2025 article) is replaced by Hansard's 35.7p to 37.3p for 1989. Hansard wins: dated and official.
- The fare: the design's "80p plus distance" keeps its 80p and gets £1.10 a mile. FIT F24's 1.30 a fare (a London figure per mile, read as a whole fare) is dropped; NUMBERS-RUN M1 asked for 2.50 to 3.50 and this gives it.
- The driver's pay: the design pays a flat £90 a week. The real 1990 trade paid by takings (the agent's settle or the principal's split, cab research S12 to S14). The run uses a half split, which gives the book about the same as the design in Act I; it is the owner's choice 1 in the design file.
- Ellis: BLUEPRINT-04 4.3.7 says Ellis is not among the officers who can be bought, and BLUEPRINT-02 2.6.8 names only two constables; the decision of 24 Nov says she can be bought at a high price. The newer decision wins; the keeper should change both rows.

## Sources read on 24 Nov 2026 (all Hansard written answers, api.parliament.uk)

- 14 Feb 1990, Cigarettes: https://api.parliament.uk/historic-hansard/written_answers/1990/feb/14/cigarettes
- 11 Mar 1991, Cigarette Prices: https://api.parliament.uk/historic-hansard/written-answers/1991/mar/11/cigarette-prices
- 13 Feb 1990, Petrol Prices: https://api.parliament.uk/historic-hansard/written-answers/1990/feb/13/petrol-prices
- 15 Oct 1990, Petrol Prices: https://api.parliament.uk/historic-hansard/written-answers/1990/oct/15/petrol-prices
- 19 Feb 1991, Petrol Prices: https://api.parliament.uk/historic-hansard/written-answers/1991/feb/19/petrol-prices
- 15 Mar 1991, Food Prices: https://api.parliament.uk/historic-hansard/written-answers/1991/mar/15/food-prices
- 20 Mar 1991, Retail Prices: https://api.parliament.uk/historic-hansard/written-answers/1991/mar/20/retail-prices
- 28 Feb 1990, Bread Prices: https://api.parliament.uk/historic-hansard/written-answers/1990/feb/28/bread-prices
- 25 May 1989, Bus Fares: https://api.parliament.uk/historic-hansard/written_answers/1989/may/25/bus-fares
- 1 Nov 1990, Earnings: https://api.parliament.uk/historic-hansard/written-answers/1990/nov/01/earnings
- 21 Nov 1990, Earnings: https://api.parliament.uk/historic-hansard/written-answers/1990/nov/21/earnings
- 22 May 1990, Wages: https://api.parliament.uk/historic-hansard/written_answers/1990/may/22/wages
- 17 Jul 1989, Lorry Drivers' Pay: https://api.parliament.uk/historic-hansard/written-answers/1989/jul/17/lorry-drivers-pay
- 9 Jul 1990, Police Pay and Manpower: https://api.parliament.uk/historic-hansard/written_answers/1990/jul/09/police-pay-and-manpower
- 9 Jul 1990, House Prices: https://api.parliament.uk/historic-hansard/written-answers/1990/jul/09/house-prices
- 23 Jul 1990, Dock Workers; 8 May 1989, Dock Workers' Wages; 24 Apr 1989, Dock Workers (no figures; cited for their absence)
- 12 Feb 1990, Loan Sharks; 16 Nov 1990, Money Lenders (no rates; cited for their absence)

Read and empty (no figures for this file): 10 Jul 1990 Bus Fares (table not printed), 17 May 1990 Low Pay, 8 Jan 1990 Police Earnings, 7 Dec 1990 Earnings.

Not reached, so left INFERRED: a 1990 used-car price guide; a 1990 caff or chip-shop price; a provincial bus fare; shop-unit and private rents for a northern town; shop assistants' and dockers' 1990 pay by occupation (the New Earnings Survey 1990 Part D tables are not online as text); pawnbrokers' and illegal lenders' 1990 rates; the Sep 1990 police pay rise.
