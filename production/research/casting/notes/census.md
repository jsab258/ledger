# Who lived in the Hook in 1990: 1991 Census, Hull and Great Grimsby

Research notes for casting. Compiled 2026-09-24. Census day was 21 April 1991, so these are the closest hard figures for a town set in 1990.

## Sources and labels

Every figure is marked:
- **CITED**: taken directly from the named source. "Opened" means I read the source itself. "Snippet" means I saw it only in a search-result summary.
- **DERIVED**: my own arithmetic on cited figures, with the method given.

Main source: **Nomis (ONS), 1991 Census**, read through the Nomis API on 2026-09-24 (opened). These are the official OPCS tables, not a secondary summary. Area codes are pre-1996 districts: Kingston upon Hull 2080375066, Great Grimsby 2080375064, Cleethorpes 2080375060, Humberside county 2088763426, Liverpool 2080375118, Middlesbrough 2080375130, Sunderland 2080375150, England 2092957699.

- Local Base Statistics (LBS, dataset NM_35_1): `https://www.nomisweb.co.uk/api/v01/dataset/NM_35_1.data.csv?geography=<code>&cell=<cell ids>&measures=20100`. Tables used: L02 age/sex/marital, L20 tenure and amenities, L21 cars, L22 rooms, L40 lone parents, L42 household composition, L47 pensioner households, L73 industry (10% sample), L74 occupation (10% sample).
- Simplified 1991 tables: NM_507_1 age, NM_509_1 population, NM_520_1 ethnic group, NM_582_1 marital status, NM_583_1 country of birth, NM_584/585/586_1 economic position (all/male/female). Base URL `https://www.nomisweb.co.uk/api/v01/dataset/NM_5xx_1.data.csv?geography=...&measures=20100`.
- Claimant count: NM_1_1, April 1990 and April 1991.
- **Data warning:** in the simplified tables, NM_588_1 ("Industry") and NM_589_1 ("Occupation") carry each other's figures under the wrong labels. I checked this against LBS L73. Only the LBS L73/L74 figures below are used.

Population bases differ slightly between tables. The 254,117 figure for Hull includes imputed residents of wholly absent households. The country-of-birth and household tables use a base of 250,820 (residents in households). Percentages are always taken on each table's own base.

---

## 1. Population, age and sex

### Totals (CITED, NM_507/NM_582, all residents including imputed)

| | Total | Male | Female |
|---|---|---|---|
| Kingston upon Hull | 254,117 | 123,023 | 131,094 |
| Great Grimsby | 90,517 | 43,809 | 46,708 |
| Cleethorpes (Grimsby's seaside twin) | 69,145 | | |
| Humberside county | 858,040 | | |
| England | 47,055,204 | 22,812,889 | 24,242,315 |

Present residents on census night (NM_509): Hull 245,026; Grimsby 87,398. People not in households (institutions, ships, hostels): Hull 3,297; Grimsby 1,128. (CITED)

### Five-year bands, all ages, Hull / Grimsby (CITED, NM_507)

0-4: 19,882 / 7,300 · 5-9: 17,307 / 6,562 · 10-14: 15,308 / 5,617 · 15: 3,205 / 1,066 · 16-17: 6,681 / 2,348 · 18-19: 7,367 / 2,570 · 20-24: 21,511 / 6,923 · 25-29: 22,031 / 7,384 · 30-34: 18,477 / 6,644 · 35-39: 15,820 / 5,595 · 40-44: 16,649 / 6,027 · 45-49: 12,292 / 4,827 · 50-54: 12,400 / 4,571 · 55-59: 12,785 / 4,572 · 60-64: 12,894 / 4,540 · 65-69: 12,971 / 4,284 · 70-74: 9,864 / 3,619 · 75-79: 8,127 / 2,974 · 80-84: 5,201 / 1,888 · 85-89: 2,458 / 900 · 90+: 887 / 306.

### Adults aged 16 and over (DERIVED from LBS L02 age by sex)

| Band | Hull | Grimsby | Combined share of adults | Male share within band |
|---|---|---|---|---|
| 16-29 | 57,590 (29.0%) | 19,225 (27.5%) | 28.6% | 49.3% |
| 30-44 | 50,946 (25.7%) | 18,266 (26.1%) | 25.8% | 50.3% |
| 45-59 | 37,477 (18.9%) | 13,970 (20.0%) | 19.2% | 49.8% |
| 60-74 | 35,729 (18.0%) | 12,443 (17.8%) | 17.9% | 45.6% |
| 75+ | 16,673 (8.4%) | 6,068 (8.7%) | 8.5% | 32.7% |
| All 16+ | 198,415 | 69,972 | 268,387 | 47.6% |

- Pensionable age (men 65+, women 60+): 23.3% of adults in both towns. (DERIVED)
- Sex ratio overall: 94 men per 100 women in Hull, 94 in Grimsby. (DERIVED from 123,023/131,094 and 43,809/46,708)
- Sex ratio among the old: aged 65+, about 153 women per 100 men in the two towns combined. Aged 75+, about 206 women per 100 men. At 85+ in Hull there are 2,613 women and 732 men. **The old people of the Hook are mostly widows.** (DERIVED from L02)
- Marital status (CITED, NM_582): married men 53,523 of 123,023 in Hull (all ages); married women 54,326.

## 2. Ethnic group and country of birth

### Ethnic group, 1991 categories (CITED, NM_520_1 / LBS L06; all ages)

| Group | Hull n | Hull % | Grimsby n | Grimsby % | Combined % (DERIVED) |
|---|---|---|---|---|---|
| White | 250,934 | 98.75 | 89,629 | 99.02 | 98.82 |
| Black Caribbean | 137 | 0.05 | 40 | 0.04 | 0.05 |
| Black African | 356 | 0.14 | 86 | 0.10 | 0.13 |
| Black Other | 369 | 0.15 | 73 | 0.08 | 0.13 |
| Indian | 318 | 0.13 | 188 | 0.21 | 0.15 |
| Pakistani | 237 | 0.09 | 80 | 0.09 | 0.09 |
| Bangladeshi | 235 | 0.09 | 28 | 0.03 | 0.08 |
| Chinese | 537 | 0.21 | 117 | 0.13 | 0.19 |
| Other Asian | 317 | 0.12 | 91 | 0.10 | 0.12 |
| Other | 677 | 0.27 | 185 | 0.20 | 0.25 |
| **All non-white** | **3,183** | **1.25** | **888** | **0.98** | **1.18** |

The ethnic table also counts people "born in Ireland": 1,117 in Hull and 449 in Grimsby. (CITED)

For contrast (CITED, same table), the non-white share was: Cleethorpes 0.81%; Humberside 1.01% (8,704); Sunderland 1.11%; Liverpool 3.77% (17,046, including 3,337 Chinese and 7,247 Black, mostly "Black Other", which reflects Liverpool's old mixed-descent community); Middlesbrough 4.42% (3,646 of them Pakistani); England 6.19%.

NEMDA Statistical Paper 1 (Owen, Nov 1992) agrees: Humberside non-white about 8.8 thousand. That table was opened, but its text came through a poor OCR. https://warwick.ac.uk/fac/soc/crer/research/publications/nemda/nemda1991sp1.pdf

### Country of birth (CITED, NM_583_1; base: residents in households)

| | Hull | % | Grimsby | % | Combined % (DERIVED) |
|---|---|---|---|---|---|
| Base | 250,820 | | 89,389 | | 340,209 |
| Born in UK | 245,033 | 97.69 | 87,007 | 97.34 | 97.60 |
| of which Scotland | 3,254 | 1.30 | 1,557 | 1.74 | 1.41 |
| of which Wales | 1,010 | 0.40 | 558 | 0.62 | 0.46 |
| of which N. Ireland | 740 | 0.30 | 284 | 0.32 | 0.30 |
| Irish Republic | 714 | 0.28 | 343 | 0.38 | 0.31 |
| Old Commonwealth (Aus/NZ/Can) | 312 | 0.12 | 111 | 0.12 | 0.12 |
| New Commonwealth | 2,341 | 0.93 | 918 | 1.03 | 0.96 |
| of which India | 426 | | 231 | | |
| of which South East Asia (mostly Hong Kong/Malaysia/Singapore) | 689 | | 181 | | |
| of which Bangladesh | 214 | | 28 | | |
| of which Pakistan | 175 | | 86 | | |
| of which Eastern Africa | 185 | | 99 | | |
| of which Other Africa | 174 | | 65 | | |
| of which Caribbean | 123 | | 49 | | |
| of which Cyprus | 96 | | 52 | | |
| Other European Community | 1,052 | 0.42 | 425 | 0.48 | 0.43 |
| Other Europe (incl. Poland, USSR, Yugoslavia, Norway, Iceland) | 286 | 0.11 | 193 | 0.22 | 0.14 |
| USA | 104 | | 29 | | |
| China | 111 | | 34 | | |
| Vietnam | 32 | | 0 | | |
| Rest of world | 835 | 0.33 | 329 | 0.37 | 0.34 |
| **Born outside UK** | **5,787** | **2.31** | **2,382** | **2.66** | **2.40** |

England's figure for comparison is 10.04%, and Humberside's is 2.64%.

### Known communities (context; thin sourcing, flagged)

- **Chinese:** the largest named minority group in Hull (537), and in the two towns combined (654), mostly Hong Kong-born restaurant and takeaway families. In Grimsby alone, Indian (188) outnumbers Chinese (117). The Hong Kong link is DERIVED from SE Asia (which includes Hong Kong) being the largest New Commonwealth birthplace in Hull (689). The 2001 Census also has Chinese as Hull's largest minority, at 749 people (snippet, hulljsna.com/population/ethnicity).
- **Yemeni seamen:** Hull is named as an early 20th-century Yemeni seamen's port, alongside South Shields, Liverpool and Cardiff. (snippet, newarab.com "Yemenis: the longest established Arab community in the UK")
- **Polish:** Hull's Polish community is described as "over 100 years" old. (opened, news.hull.gov.uk 10/04/2025) There are no numbers. The postwar Polish Resettlement Act (1947) settlers would have been in their late 60s to 70s by 1990 and fall inside "Other Europe" above.
- **Not found:** no numbers for Latvian, Ukrainian, Norwegian or Icelandic settlers. The "Other Europe" and "Other EC" birthplace rows are the ceiling for all of them together, about 0.6% of residents.
- **Vietnamese:** 32 people born in Vietnam in Hull, which is a trace of dispersed boat-people settlement. (CITED, NM_583)

## 3. Households, tenure and cars (CITED, LBS L20/L21/L22/L40/L42/L47)

| | Hull | Grimsby | England |
|---|---|---|---|
| Households | 103,246 | 35,427 | 18,765,583 |
| One-person households | 30,428 (29.5%) | 9,039 (25.5%) | 26.7% |
| of which one pensioner alone | 16,699 (16.2%) | 5,354 (15.1%) | 15.0% |
| of which one adult under pension age alone | 13,686 (13.3%) | 3,682 (10.4%) | 11.7% |
| One adult with dependent children | 6,079 (5.9%) | 2,012 (5.7%) | 4.1% |
| Lone parents (L40) | 5,628, of which 5,263 are women | 1,832, of which 1,705 are women | 691,392 |
| Female lone parents not in work (economically inactive) | 3,794 of 5,263 (72%) | | |
| Man and woman, no dependent children | 27,566 (26.7%) | 10,036 (28.3%) | 29.2% |
| Man and woman with dependent children | 19,892 (19.3%) | 7,512 (21.2%) | 19.8% |
| 3+ adults, mixed sex (grown-up children at home, etc.) | 15,503 (15.0%) | 5,570 (15.7%) | 16.4% |
| Households with at least one pensioner | 33,719 (32.7%) | 11,658 (32.9%) | 33.4% |

The census household tables count "2 adults (1 male and 1 female)". This includes married and cohabiting couples, and is the best available stand-in for "married couple".

### Tenure (L20; base: households with all residents permanent)

| | Hull | Grimsby | England |
|---|---|---|---|
| Owned outright | 14.1% | 23.6% | 24.1% |
| Buying with a mortgage | 35.3% | 47.3% | 43.5% |
| **Rented from council** | **38,449 (37.3%)** | **6,958 (19.6%)** | **19.9%** |
| Rented from housing association | 3.3% | 2.2% | 3.2% |
| Rented privately | 8.9% | 6.3% | 7.4% |
| Rented with job or business | 1.2% | 0.9% | 1.9% |

### Cars (L21)

| | Hull | Grimsby | England |
|---|---|---|---|
| **No car** | **52,826 (51.2%)** | **15,524 (43.8%)** | **32.4%** |
| One car | 39.3% | 43.8% | |
| Two or more cars | 9.6% | 12.4% | 23.9% |

- Among pensioner households in Hull, 24,326 of 33,719 (72%) had no car. (DERIVED from L47)
- Central heating (L42): 41,339 Hull households (40%) had none. This was a cold, coal- and gas-fire town. (CITED count, DERIVED %)

Hull is the outlier on both measures: a majority council-renting, carless city. Grimsby looks more like an ordinary English town on housing, but has higher unemployment.

## 4. Work

### Economic position, residents aged 16+ (CITED, NM_584/585/586; census week April 1991)

| | Hull | Grimsby |
|---|---|---|
| Residents 16+ | 198,415 | 69,972 |
| Economically active | 115,378 | 41,378 |
| In employment | 94,941 (full-time employee 66,371; part-time 21,121; self-employed 7,449) | 35,056 (FT 22,938; PT 8,861; self-employed 3,257) |
| On a government scheme | 2,790 | 739 |
| Unemployed | 17,647 | 5,583 |
| **Unemployment rate (unemployed ÷ active), DERIVED** | **15.3%** (men 18.8%, women 10.2%) | **13.5%** (men 17.0%, women 8.4%) |
| Retired | 37,020 | 13,368 |
| Permanently sick | 9,784 | 2,713 |
| Students (inactive) | 7,587 | 2,654 |
| Other inactive (mostly women keeping house) | 28,646, of which 27,642 are women | 9,859, of which 9,590 are women |

- Women's work was heavily part-time: in Hull 19,295 part-time against 20,867 full-time; in Grimsby 7,987 part-time against 6,635 full-time. (CITED)
- Comparison, census unemployment rate (DERIVED): Liverpool 21.1%, Middlesbrough 16.9%, Sunderland 14.9%, Cleethorpes 9.7%, Humberside 10.5%, England 9.1%.

**Correcting to 1990 (DERIVED).** Census day, April 1991, fell early in the recession. Claimant counts (CITED, NM_1_1) were:

| | April 1990 | October 1990 | April 1991 |
|---|---|---|---|
| Hull | 13,351 | 13,720 | 17,282 |
| Grimsby | 4,456 | 4,220 | 5,410 |

Scaling the census rate by the ratio of claimants gives a 1990 unemployment rate of about **11.8% in Hull** and **11.1% in Grimsby**. Men's rates in 1990 would be about 14 to 15%.

### Industry of employed residents (CITED, LBS L73, 10% sample: Hull n=9,292, Grimsby n=3,519, so multiply by 10 for a rough count)

| 1980 SIC division | Hull | % | Grimsby | % | Combined % of employed (DERIVED) |
|---|---|---|---|---|---|
| 0 Agriculture, forestry, **fishing** | 82 | 0.9 | 33 | 0.9 | 0.9 |
| 1 Energy and water | 97 | 1.0 | 54 | 1.5 | 1.2 |
| 2 Minerals, metals, **chemicals** (label on Nomis: "Mining") | 492 | 5.3 | 148 | 4.2 | 5.0 |
| 3 Metal goods, engineering, vehicles | 886 | 9.5 | 130 | 3.7 | 7.9 |
| 4 Other manufacturing (incl. **food/fish processing**) | 937 | 10.1 | 717 | 20.4 | 12.9 |
| 5 Construction | 686 | 7.4 | 244 | 6.9 | 7.3 |
| 6 Distribution, hotels, catering (retail, wholesale, markets, pubs) | 2,180 | 23.5 | 831 | 23.6 | 23.5 |
| 7 Transport and communication (**docks**, shipping, road, rail, post) | 687 | 7.4 | 326 | 9.3 | 7.9 |
| 8 Banking, finance, business services | 585 | 6.3 | 226 | 6.4 | 6.3 |
| 9 Other services (public admin, health, education, police) | 2,581 | 27.8 | 789 | 22.4 | 26.3 |
| Not stated | 79 | 0.9 | 21 | 0.6 | 0.8 |

- In Hull, 73 of the 82 in division 0 are men, which is consistent with fishermen. In Grimsby, 380 of the 717 in "other manufacturing" are women (fish filleting, frozen-food lines). (CITED)
- For contrast: Cleethorpes division 0 is 48 of 2,967 (1.6%). England division 0 is 1.8%, and that is mostly farming. Liverpool division 0 is 12 of 14,331. (CITED)

### Occupation (CITED, LBS L74, SOC 1990 major groups; same 10% base)

| SOC group | Hull | Grimsby |
|---|---|---|
| Managers and administrators | 835 (9.0%) | 380 (10.8%) |
| Professional | 487 (5.2%) | 177 (5.0%) |
| Associate professional | 694 (7.5%) | 246 (7.0%) |
| **Clerical and secretarial** | **1,301 (14.0%)** | **459 (13.0%)** |
| Craft and related | 1,496 (16.1%) | 479 (13.6%) |
| Personal and protective services | 980 (10.5%) | 322 (9.2%) |
| Sales | 764 (8.2%) | 287 (8.2%) |
| **Plant and machine operatives** | **1,473 (15.9%)** | **760 (21.6%)** |
| Other (elementary: labourers, cleaners, porters, dock labour) | 1,174 (12.6%) | 383 (10.9%) |
| Not stated | 88 | 26 |

Sub-groups (CITED):
- Hull, drivers and mobile plant operators (8b): 558, of which 538 are men.
- Hull, "Other occupations in agriculture, forestry and fishing" (9a): only 23.
- Grimsby, 8a industrial plant operators and assemblers: 585, of which 305 are women.

### Fishing and docks around 1990 (context; the census cannot separate these precisely)

**Hull fishing**
- At its height, about 8,000 trawlermen and 320 trawlers, with "three times that number" earning a living ashore from fish and fish processing. (CITED, opened: Visit Hull, "Hull's Fishing Heritage" 2024 PDF, https://visithull.org.uk/wp-content/uploads/2024/03/Hulls-Fishing-Heritage-2024.pdf)
- St Andrew's Dock closed 3 November 1975 and the fleet moved to Albert and William Wright Docks. (CITED, same PDF)
- Arctic Corsair's fishing life ended in the late 1980s. (CITED, same PDF)
- "By 1981 Hull had a fleet of only 22 trawlers, by 1989 there were less than a dozen." (snippet only; I could not find the source page)
- Census: about 820 Hull residents in division 0, which includes fishing. (DERIVED, 82 × 10)

**Grimsby fishing**
- About 400 trawlers in 1970 and five in 2013. (snippet, Time 2016)
- The deep-water fleet was "diminished to the point of extinction" by the Cod Wars. (snippet)
- The fish market survived on Icelandic landings: in 2012, about 13,000 of the 18,000 tonnes sold were caught by Icelandic vessels. (snippet, Lincolnshire Life)
- By 1990, Grimsby's fish economy was **processing and frozen food** far more than catching. Birds Eye's Grimsby plant closed in 2005 with 650 jobs lost (snippet, Wikipedia "Birds Eye"). Findus opened in Grimsby in June 1960 (snippet).
- Census: Grimsby "other manufacturing" is 20.4% of employed residents, against 10.1% in Hull. Most of that excess is food and fish processing. (DERIVED inference)

**Docks**
- The National Dock Labour Scheme covered Hull and Immingham among 63 ports. (snippet, Bristol Radical History Group)
- Registered dock workers nationally numbered 9,400 in April 1989, down from 27,000 (and a peak of 82,000). (CITED, opened: Hansard HL 6 April 1989, https://api.parliament.uk/historic-hansard/lords/1989/apr/06/dock-labour-scheme)
- The Abolition Act received Royal Assent on 6 July 1989. The national strike began on 10 July 1989. (snippet, BRHG)
- 498 redundancies at Grimsby and Immingham in 1989, including the whole workforces of Lindsey Dock Services (106) and John Sutcliffe Consolidated Stevedores (226). A further 24 in 1990. (CITED, opened: Hansard written answers 13 Dec 1991, https://api.parliament.uk/historic-hansard/written-answers/1991/dec/13/dock-labour-scheme)
- For comparison, Tees and Hartlepool had 445 registered dockers at abolition. (same source)
- **I could not find a Hull-specific registered docker count.** A reasonable bracket, by comparison with Tees, is several hundred to about 1,000. This is an estimate, not a cited figure.
- Census division 7 in Hull is about 6,870 residents (DERIVED, 687 × 10), but most of those are road haulage, rail, bus and post, not docks.

---

## 5. CASTING TABLE: adults (16+) in the Hook, 1990

Base: Hull + Great Grimsby combined, 268,387 adults. Every figure here is DERIVED from the CITED 1991 tables above unless marked otherwise. Round freely: a cast of 50 moves in 2% steps.

| Dimension | Category | Share of adults | Notes |
|---|---|---|---|
| **Age** | 16-29 | 28.6% | |
| | 30-44 | 25.8% | |
| | 45-59 | 19.2% | |
| | 60-74 | 17.9% | 54% women |
| | 75+ | 8.5% | 67% women; about 2 women per man |
| **Sex** | Men | 47.6% | |
| | Women | 52.4% | |
| **Ethnic group** (all ages) | White | 98.8% | |
| | Chinese | 0.19% | about 1 in 530; largest named minority group combined (in Grimsby alone, Indian is larger) |
| | Black (Caribbean, African, Other) | 0.31% | "Other Black" includes British-born mixed descent |
| | South Asian (Indian, Pakistani, Bangladeshi) | 0.32% | |
| | Other Asian and Other | 0.37% | |
| **Birthplace** | Born outside UK | 2.4% | 1 in 42 |
| | Irish Republic | 0.31% | |
| | Rest of Europe | 0.57% | includes old Polish and Baltic settlers and EC nationals |
| | Born in Scotland or Wales (not foreign, but has an accent) | 1.9% | |
| **What they do** (all adults, adds to 100%) | Retired | 18.8% | |
| | Keeping house or other inactive | 14.3% | almost all women |
| | Unemployed | 8.7% | census 1991 figure. **For 1990 use about 7%**, which is about 11.5% of the active; men's rate about 14% |
| | Permanently sick | 4.7% | |
| | Student | 3.8% | |
| | Government scheme (YTS, ET) | 1.3% | |
| | **In work** | **48.4%**, broken down below | |
| — in work, by trade | Market, retail, wholesale, pubs, catering | 11.4% | |
| | Manufacturing and industry, incl. chemicals, engineering, energy, construction | 16.6% | of which **food/fish processing about 3-5%** of adults in a Grimsby-like town (estimate) |
| | Dock, port, shipping, road and rail transport, post | 3.8% | docks alone probably under 1% (estimate, not cited) |
| | Fishing (catching) | 0.4% | about 1 in 250 adults; a smaller share of Hull, larger in Grimsby and Cleethorpes |
| | Public services (council, health, schools, police) | 12.7% | |
| | Banking, finance, business offices | 3.1% | |
| | Not stated | 0.4% | |
| — overlay by occupation (not additive) | Clerical and secretarial | about 6.7% of adults (13.7% of workers) | these people sit inside the trades above |
| **Household** (per household) | Lives alone | 28.5% | about half of these are pensioners |
| | Council tenant | 37% (Hull) to 20% (Grimsby) | |
| | No car | 51% (Hull) to 44% (Grimsby) | |

Method notes:
- The "What they do" rows use the census April 1991 economic-position counts. Workers are split across trades using the L73 10% sample shares, multiplied by the in-work share (48.4%).
- The 1990 unemployment adjustment scales the census count by the claimant ratio of April 1990 to April 1991 (Hull 0.77, Grimsby 0.82). The people moved out of "unemployed" should go back mainly into "in work".
- The food/fish processing estimate is Grimsby's "other manufacturing" share (20.4% of workers) minus Hull's (10.1%), about 10 points of workers, which is about 5% of adults at Grimsby's 50% employment rate. Not all of that excess is fish, so 3-5% of adults is a range, not a cited figure.
- Ethnic shares are for all ages, because no age split was pulled. Minority groups were younger than average, so the adult shares are probably slightly lower.

## Gaps

- The Hull registered docker count for 1989 was not found.
- The size of the Hull and Grimsby trawler fleets in 1990 rests only on a search snippet ("less than a dozen" in Hull in 1989).
- The census does not separate fish processing within SIC division 4. The 1991 Census of Employment or the Humberside County Council labour-market reports would do so, but I did not reach them.
- There are no counts for Polish, Latvian, Ukrainian, Norwegian or Icelandic settlers; only the birthplace ceilings above.
