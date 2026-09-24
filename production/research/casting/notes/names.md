# Cast names for a Humber port town, 1990: research notes

Researched 2026-09-24. Bounded web research. Nothing downloaded to the project. Two small files were streamed into memory to be parsed and were not kept: the ONS rankings CSV and the Guppy full text.

Labels:
- **OPENED**: page or file fetched and read.
- **SNIPPET**: search-result text only.
- **DATA**: counted or statistical source.
- **OBSERVATION**: a writer's or photographer's record, or my own inference, marked as such.
- **GENERAL**: general knowledge, not sourced in this session. Treat as unverified.

---

## 1. First names by birth decade (England and Wales)

**Source.** ONS, "Top 100 baby names in England and Wales: historical data", 1904–1994 at 10-year intervals, Open Government Licence.
- Dataset page: https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/babynamesenglandandwalestop100babynameshistoricaldata. OPENED. The page gives a release date of 31 Jul 2025 for the current 1904–2024 edition; the 1904–1994 edition was first released 15 Aug 2014 (SNIPPET).
- The ranks below were parsed from the ONS data as republished in the `ukbabynames` R package: https://raw.githubusercontent.com/mine-cetinkaya-rundel/ukbabynames/main/data-raw/ewbabynames/rankings.csv. OPENED. 1,900 rows. The file is built from ONS `historicname_tcm77-254032.xls`. DATA.
- ONS gives no method notes for the historic lists: no sample basis and no treatment of spelling variants (OPENED, "Baby names since 1904" article, 2016-09-02). Spellings count separately, so Tracey (6) and Tracy (11) are two entries.
- **Regional differences.** None found. These lists are national only. No Yorkshire or Humberside breakdown exists for these years in the ONS historic set.
- **Data oddity.** "Abdul" appears at #78 for 1934 boys, and "Mohamed" and "Mohammed" appear in 1954. These are almost certainly artefacts of how the historic lists were compiled. Do not use them as evidence of era naming.

### Top 20, in rank order (DATA)

**1924 (aged ~66 in 1990)**
- Boys: John, William, George, James, Thomas, Ronald, Kenneth, Robert, Arthur, Frederick, Peter, Edward, Albert, Charles, Leslie, Joseph, Stanley, Eric, Frank, Dennis
- Girls: Margaret, Mary, Joan, Joyce, Dorothy, Kathleen, Doris, Irene, Elizabeth, Eileen, Betty, Jean, Marjorie, Gladys, Doreen, Vera, Elsie, Barbara, Winifred, Edna

**1934 (~56)**
- Boys: John, Peter, William, Brian, David, James, Michael, Ronald, Kenneth, George, Robert, Thomas, Alan, Derek, Raymond, Anthony, Roy, Donald, Dennis, Edward
- Girls: Margaret, Jean, Mary, Joan, Patricia, Sheila, Barbara, Doreen, June, Shirley, Dorothy, Joyce, Maureen, Elizabeth, Audrey, Brenda, Kathleen, Sylvia, Eileen, Pamela

**1944 (~46)**
- Boys: John, David, Michael, Peter, Robert, Anthony, Brian, Alan, William, James, Richard, Kenneth, Roger, Keith, Colin, Christopher, Raymond, Terence, Thomas, Barry
- Girls: Margaret, Patricia, Christine, Mary, Jean, Ann, Susan, Janet, Maureen, Barbara, Valerie, Carol, Sandra, Pauline, Elizabeth, Joan, Pamela, Jennifer, Kathleen, Anne

**1954 (~36)**
- Boys: David, John, Stephen, Michael, Peter, Robert, Paul, Alan, Christopher, Richard, Anthony, Andrew, Ian, James, William, Philip, Brian, Keith, Graham, Kevin
- Girls: Susan, Linda, Christine, Margaret, Janet, Patricia, Carol, Elizabeth, Mary, Anne, Ann, Jane, Jacqueline, Barbara, Sandra, Gillian, Pauline, Elaine, Lesley, Angela

**1964 (~26)**
- Boys: David, Paul, Andrew, Mark, John, Michael, Stephen, Ian, Robert, Richard, Christopher, Peter, Simon, Anthony, Kevin, Gary, Steven, Martin, James, Philip
- Girls: Susan, Julie, Karen, Jacqueline, Deborah, Tracey, Jane, Helen, Diane, Sharon, Tracy, Angela, Sarah, Alison, Caroline, Amanda, Sandra, Linda, Catherine, Elizabeth

**For reference**
- 1914 (~76). Boys: John, William, George, Thomas, James, Arthur, Frederick, Albert, Charles, Robert, Edward, Joseph, Ernest, Alfred, Frank, Henry, Leslie, Harold, Harry, Leonard. Girls: Mary, Margaret, Doris, Dorothy, Kathleen, Florence, Elsie, Edith, Elizabeth, Winifred, Gladys, Annie, Alice, Phyllis, Hilda, Lilian, Ivy, Marjorie, Ethel, Violet.
- 1974 (~16, children in 1990). Boys: Paul, Mark, David, Andrew, Richard, Christopher, James, Simon, Michael, Matthew, Stephen, Lee, John, Robert, Darren, Daniel, Steven, Jason, Nicholas, Jonathan. Girls: Sarah, Claire, Nicola, Emma, Lisa, Joanne, Michelle, Helen, Samantha, Karen, Amanda, Rachel, Louise, Julie, Clare, Rebecca, Sharon, Victoria, Caroline, Susan.

### Names that date a person (DATA, computed)

Each list below is the names in the top 100 in that year but absent from the top 100 twenty years earlier and thirty years later. The number in brackets is the rank.

- **1914** boys: Herbert, Cyril, Sidney/Sydney, Wilfred, Horace, Percy, Cecil, Fred.
- **1914** girls: Doris (3), Florence, Elsie, Edith, Winifred, Gladys, Annie, Phyllis, Hilda, Ivy, Ethel, Violet, Edna, Nellie, Mabel, Ada.
- **1924** boys: Denis, Desmond, Derrick, Basil.
- **1924** girls: Betty, Audrey, Peggy, Beryl, Nancy, Daphne, Enid, Mavis, Thelma, Alma.
- **1934** boys: Bryan, Neville, Desmond, Barrie, Royston. Brian itself is #4, and Derek and Raymond are in the top 20.
- **1934** girls: Sheila, June, Brenda, Rita, Mavis (29), Norma, Hazel, Thelma, Cynthia, Marlene, Gloria.
- **1944** boys: Roger, Rodney, Clive, Jeffrey, Melvyn, Barrie. Keith, Colin, Terence and Barry are in the top 20.
- **1944** girls: Janet, Valerie, Carole, Judith, Rosemary, Yvonne, Janice, Marilyn, Lesley, Hilary, Jill, Lynda, Jeanette, Anita.
- **1954** boys: Nigel, Howard, Jeremy, Garry. Kevin, Graham and Keith are in the top 20.
- **1954** girls: Linda (2), Carol, Sandra, Elaine, Lesley, Denise, Diane, Janice, Lynn/Lynne, Lorraine, Sharon, Beverley, Gail.
- **1964** boys: Wayne, Darren, Tony, Russell, Garry, Glenn, Martyn. Gary is in the top 20.
- **1964** girls: Karen, Deborah, Tracey/Tracy, Sharon, Alison, Amanda, Joanne, Dawn, Michelle, Debra, Paula, Donna, Mandy, Tina, Jayne, Kim.

Ranks 21 to 60 are also useful as less obvious "real" names:
- 1934 boys: Gordon, Norman, Geoffrey, Leonard, Bernard, Reginald, Maurice, Douglas, Malcolm, Walter, Trevor, Clifford.
- 1944 girls: Sheila, Brenda, Gillian, Sylvia, Wendy, Doreen, Rita.
- 1954 boys: Nigel, Trevor, Malcolm, Barry, Clive, Neil, Stuart, Adrian.
- 1964 boys: Neil, Carl, Wayne, Shaun, Dean, Lee, Craig.

---

## 2. Surnames of Hull, East Yorkshire, Grimsby and North Lincolnshire

### Hull telephone directory, 1990 (the single best source for this brief)
- Top 15: Smith, Wilson, Taylor, Robinson, Brown, Johnson, Thompson, Harrison, Jackson, Walker, Wilkinson, Wright, Clark, Watson, Hall.
- Hull 1695 poll-tax top 15, for contrast: Smith, Thompson, Watson, Robinson, Brown, Taylor, Johnson, Wilson, Wood, Richardson, Walker, Wilkinson, Lambert, Ellis, Atkinson. Also common then: Banks, Etherington, Hodgson, Peacock, Scott.
- Source: "James the Names" blog (Hull surname research), post dated 2 Jun 2014. https://jemmyhope.wordpress.com/tag/hull-surnames/. OPENED. The 1695 list cites Hull City Council, *The People of Hull in 1695 and 1697* (1987).
- DATA, secondhand. The blogger counted the directory; I have not seen the directory.

### Guppy, *Homes of Family Names in Great Britain* (1890)
- Full text on archive.org: https://archive.org/details/cu31924029805862. OPENED, full text parsed.
- Method (OPENED, p. ~9235/9491 in the text): counts of farmers' names in Kelly's Post Office county directories, 1880s. **This is a rural bias.** It says where families came from, not who lived in the Hessle Road terraces.
- DATA.

North and East Ridings (pp. 408–410):
- General names: Brown, Hall, Johnson, Robinson, Smith, Wilson.
- Common names: Chapman, Mason, Walker, Foster, Moore, Ward, Harrison, Richardson, Watson, Jackson, Thompson.
- Regional names: Atkinson, Hudson, Stephenson, Barker, Webster, Dixon, Pearson, Wilkinson, Simpson. Dunn is marked "(Hull)".
- District names:
  - Marked "Hull": Jordan; Kirby (York and Hull); Milner (York and Hull).
  - Others: Clarkson, Coates, Dale, Dobson, Dunning, Fawcett, Hodgson, Hutchinson, Kirk, Kitchin, Lambert, Lawson, Metcalfe, Peacock, Pickering, Sowerby.
- County names: Allison, Appleton, Boyes, Calvert, Cockerill, Craven, Dent, Dowson, Featherstone, Frankland, Hopper, Hornby, Horner, Jefferson, Lofthouse, Lumley, Mudd, Porritt, Sayer, Shipley, Smithson, Spence, Strickland, Swales, Topham, Trotter, Weatherill, Wise, Yeoman.
- **Peculiar names (confined mostly to the North and East Ridings):**
  - Tennison is marked "(Hull)".
  - Agar, Blenkin, Bosomworth, Botterill, Brigham, Bulmer, Codling, Coverdale, Danby, Dinsdale, Duck, Duggleby, Elgey, Ellerby, Galloway, Garbutt, Goodwill, Grainger, Harker, Harland, Hebron, Heseltine, Hick, Holliday, Horsley, Hugill, Iveson, Jacques, Jordison, Judson, Kettlewell, Kilvington, Knaggs, Lamplugh, Laverack, Leak, Leckenby, Matson/Mattison, Medforth, Megginson, Monkman, Nottingham, Pybus, Rennison, Rowntree, Scarth, Sedman, Sellers, Severs, Stainthorpe, Stockill, Sturdy, Suddaby, Suggitt, Tweedy, Tyerman, Ventress, Welburn, Wilberforce/Wilberfoss, Witty, Wray, Wrightson.

Lincolnshire (pp. 268–270):
- General names: Allen, Brown, Clark(e), Johnson, Robinson, Smith, Taylor, Wright.
- Common names: Brooks, Chapman, Foster, Harrison, Parker, Richardson, Ward.
- Regional names: Atkinson, Dawson, East, Hardy, Holmes, Marshall, Sharp(e), Stephenson, Wells, Wilkinson.
- District names: Briggs, Cartwright, Croft, Davey, Emmerson, Everatt, Gibbons, Gosling, Grant, Graves, Kemp, Key, Kirk, Kitching, Naylor, Needham, North, Swain, Winter.
- County names: Baxter, Bellamy, Blanchard, Burrell, Campion, Creasey, Dalton, Franks, Goodacre, Kirkby, Lingard, Moody, Musgrave, Parr, Pepper, Pinder, Skelton, Smithson, Tinsley, Travis, Twidale.
- **Peculiar names (mostly confined to Lincolnshire):**
  - Merrikin and Willey are marked "(Great Grimsby)".
  - Anyan, Blades, Blankley, Borman, Bowser, Brackenbury, Brumby, Burkill (Brigg), Cammack, Capes, Codd, Collishaw, Coney, Cottingham, Coupland, Cropley, Cutforth, Dannatt, Daubney, Dowse, Drewery, Dring, Drury, Epton, Evison, Gilliatt, Goose, Grummitt, Herring, Hewson, Hildred, Hoyles, Ingle, Laming, Leggott, Lill, Lilley, Mackinder, Marfleet, Mastin, Maw, Mawer, Odling, Pocklington, Riggall, Sardeson, Scarborough, Scrimshaw, Searson, Sneath, Stamp, Storr, Strawson, Temple, Ullyatt, Waddingham, Wass, Westoby, Willows, Winn, Wroot.

Norse place-name surnames among these: Danby, Ellerby, Kirby, Kirkby, Sowerby, Suddaby, Westoby, Duggleby, Leckenby, Scarborough. These are the "-by" names the brief asks about (OBSERVATION: Old Norse *-by* place-name element; GENERAL).

### Forebears regional frequency (no year stated on the page)
Treat as modern (21st-century) data, and whole-county.
- Yorkshire: https://forebears.io/england/yorkshire/surnames. OPENED. Smith, Taylor, Wilson, Robinson, Walker, Wood, Brown, Jackson, Thompson, Harrison, Shaw, Johnson, Wilkinson, Wright, Ward, Greenwood, Hall, Watson, Barker, Turner…
  - Whole-county figures are pulled west. Greenwood, Sykes, Haigh, Hirst, Firth, Sutcliffe and Schofield are West Riding (textile) names. **Avoid them** for a Hull-flavoured cast (OBSERVATION, by comparison with the Hull 1990 and Guppy East Riding lists).
- Lincolnshire: https://forebears.io/england/lincolnshire/surnames. OPENED. Smith, Taylor, Brown, Johnson, Robinson, Wilson, Wright, Jones, Thompson, Jackson, Green, Walker, Clark, Ward, Parker, White, Harrison, Williams, Hall, Turner, Cook, Marshall, Clarke, Wilkinson, Chapman… DATA.
- Not reached: the UCL/GB Names surname profiler (dynamic site) and any Grimsby phone-book list.

### Fishing-community names (OBSERVATION: individuals, not frequency)
- Hessle Road "headscarf revolutionaries", 1968: Lillian Bilocca (born Lillian **Marshall**, 26 May 1929), Christine **Jensen**, Mary **Denness**, Yvonne **Blenkinsop**.
- Bilocca is her Maltese husband's surname: Carmelo "Charlie" Bilocca, a seaman with the Ellerman's Wilson Line.
- Her father was Ernest Marshall, a trawlerman; her mother Harriet. Her children were Ernest (b.1946) and Virginia (b.1950).
- Source: https://en.wikipedia.org/wiki/Lillian_Bilocca. OPENED.
- **This shows that Maltese, Scandinavian-derived and East Riding names sat side by side in one Hessle Road campaign.**
- The Stanton family ran a dockside café on Hull's fish dock through four generations (SNIPPET, Fishing News, https://fishingnews.co.uk/fishing-nostalgia/hulls-fish-dock-the-wet-side/).

---

## 3. Minority communities, c.1990

**Scale.** No Hull figure for 1991 was found.
- In 2001, 2.3% of Hull residents were from non-white minority groups, and 3.6% including white minorities (SNIPPET, hulljsna.com via search).
- Hull is not among the 1991 districts with the largest minority shares (SNIPPET, https://dwowen.warwick.ac.uk/tab5.htm).
- A 1990 street should therefore be overwhelmingly white English, with a few minority families in named trades (OBSERVATION).

**Baltic, Ukrainian and Polish EVWs**
- Hull was a landing port for EVWs, 1946–50. More than a third of about 80,000 EVWs landed there, but most spent one or two nights at Priory Road Camp and moved on (OPENED: Emily Gilbert, "Changing Identities" blog, 12 Nov 2017, https://changingidentities.wordpress.com/2017/11/12/hull-the-experiences-of-latvian-lithuanian-and-estonian-evws-who-arrived-in-britain-via-the-port-of-hull-1946-1950/).
- Named individuals in that post: Astrid Radze-Constable (second-generation Latvian; the hyphenated name is an observation), Juri Noot (Estonian, arrived 31 Jul 1948), and "Walter", who stayed at Priory Road and married a Hull woman, Lillian.
- **Consequence (OBSERVATION): a Hull EVW family is plausible but not a large community.** Typical case: a foreign-born man aged 60–70 in 1990 who married locally, with children aged 30–40 who have English first names and his surname.
- Surname and first-name shapes (GENERAL):
  - Latvian: men's surnames end -s/-š and women's -a/-e (Ozols/Ozola, Kalniņš/Kalniņa, Bērziņš, Liepa).
  - Estonian: Tamm, Saar, Kask.
  - Lithuanian: -as, -is, -us (Kazlauskas).
  - Polish: Nowak and Kowalski are the two most common in Poland (SNIPPET, careersinpoland), also Wiśniewski, Kowalczyk, Lewandowski, Kamiński.
  - Ukrainian: Melnyk, "most common Ukrainian surname" (SNIPPET), Kovalenko, Shevchenko, Kravchenko, Bondarenko.
  - First names of the EVW generation (GENERAL): Jan, Stanisław, Józef, Tadeusz, Zbigniew (Polish); Janis, Arvids, Juris (Latvian); Mykola, Volodymyr, Ivan (Ukrainian); Irena, Halina, Zofia.
- **British spelling in 1990.** Diacritics are dropped in British records, so Kalnins, Wisniewski (GENERAL).

**Italians**
- Penna family, Hull ice cream (OPENED: https://theearlybirdeater.blogspot.com/2018/03/italian-connections-and-exhibition-and.html, 31 Mar 2018, reporting the "Italian Connections" exhibition at Hull's Streetlife Museum).
  - Francesco Penna set up at 28 North Street in 1889, hiring out barrows.
  - The family's later first names were Frank, Peter, Grace, Rosaria and Ann: anglicised or kept Italian.
  - The Pearson Park kiosk was run from 1969 (SNIPPET, Hull CC News 2019); Frank Penna is described as a long-serving ice-cream man (Yorkshire Post, SNIPPET).
- Stefano Guazelli anglicised his name to "G. Stevens" and opened an ice-cream shop in 1922. Name-changing did happen.
- Toffolo, mosaic and terrazzo, from 1904.
- Italian heads of families were interned in WW2 (SNIPPET).
- **Pattern (OBSERVATION):** the second generation has anglicised first names (Frank, Peter, Grace) and keeps the Italian surname.

**Maltese**
- Bilocca (above). Maltese seamen on Hull shipping lines are attested by this one case (OBSERVATION).

**Irish**
- No Hull-specific source reached. Common Irish surnames nationally (GENERAL): Murphy, Kelly, O'Brien, Ryan, Byrne, Walsh, Doyle, McCarthy, Brennan. Catholic first names: Patrick, Michael, Sean, Bernard, Bridget, Maureen, Kathleen, Theresa.
- Note that Bridget (1924 #86) and Maureen (1934 top 20) are also in the ONS England and Wales lists (DATA).

**Chinese (Hong Kong New Territories)**
- Takeaways spread to "every British town" by the 1970s–80s, opened by 1950s-onward Hong Kong and New Territories migrants (SNIPPET, British Chinese cuisine / The Conversation).
- James L. Watson, *Emigration and the Chinese Lineage: the Mans in Hong Kong and London* (UC Press, 1975) documents the **Man** lineage of San Tin moving into British catering (SNIPPET, catalogue records).
- Cantonese romanised surnames (GENERAL): Chan, Wong, Lee/Li, Cheung, Lau, Tang, Man, Ng, Leung, Yeung, Cheng.
- Adults born in Hong Kong often used English given names (Peter Chan, Alice Wong) or Cantonese ones (Kwok Wah, Siu Ling) (GENERAL). **Children born in Britain c.1965–75 mostly had English first names** (GENERAL, unverified).

**South Asian**
- No Hull-specific source reached. Nationally in the 1960s Pakistani and Indian doctors were recruited to the NHS, and by the 1980s there were many shops and restaurants (SNIPPET, Wikipedia British Pakistanis).
- A doctor, a newsagent or an "Indian" restaurant owner is the plausible 1990 Hull figure (OBSERVATION).
- Names (GENERAL):
  - Punjabi Muslim: Mohammed/Muhammad, Iqbal, Hussain, Khan, Akhtar, Rashid.
  - Sikh: Singh/Kaur, first names like Gurdev, Harjit.
  - Gujarati Hindu: Patel, Shah, Mistry.
  - Bangladeshi "Indian" restaurants: Miah, Uddin, Ali, Ahmed.
- Second generation born in the 1960s–70s mostly kept community first names (GENERAL).

**Yemeni and Arab seafarers**
- Hull is named as a Yemeni settlement port alongside South Shields, Liverpool and Cardiff, "not to such an extent" (SNIPPET: https://en.wikipedia.org/wiki/Yemenis_in_the_United_Kingdom and The New Arab).
- Most of these seamen were stokers and firemen from around Taiz.
- Names (GENERAL): Ali, Ahmed, Mohamed, Saleh, Nasser, Hassan, Abdullah. Surnames were often a father's name.
- By 1990 there might be one old seaman or a mixed-marriage family (OBSERVATION).

**Icelandic and Scandinavian (Grimsby especially)**
- Paul Adalsteinsson MBE co-founded Rinovia Steam Fishing Co., Grimsby, in the 1930s, with J.R. "Joe" Cobley. It had Icelandic trawler names and links to the Icelandic consulate (OPENED, https://en.wikipedia.org/wiki/Rinovia_Steam_Fishing_Company).
- **Pétur Björnsson**, an Icelander, came to the Humber in **1981** as an agency manager for J. Marr & Son, handling Icelandic vessels. He founded Isberg Ltd in the mid-1980s and stayed in the UK until 1997 (SNIPPET, Grimsby Telegraph via search).
- **This makes an Icelandic fish agent in 1990 exactly right (OBSERVATION).**
- Jensen (Hessle Road, 1968) is a Danish/Norwegian-looking surname in the fishing community (OBSERVATION).
- Icelanders use patronymics (-son/-dóttir), anglicised without accents (Bjornsson, Adalsteinsson) (GENERAL).

---

## 4. Business names, Hull c.1979–1994

**Peter Marshall's Hull shop-window photographs, 1979–1994**
- Published by Flashbak, 14 Nov 2024: https://flashbak.com/hull-yorkshire-1980s-shops-471429/. OPENED; captions only. OBSERVATION, photographic.
- Fascia names seen, by naming pattern:
  - **Owner's first name + possessive:** Brenda's Cafe (Goulton St, 1981); Coco's Restaurant (Carr Lane, 1994).
  - **Full personal name:** Bob Carver's Fish Bar (Market Square, 1979); Brian Draper Roofing Building Contractor (Princes Ave, 1979).
  - **Surname / initials + trade:** E S Webster (Walton St, 1979); E E Sharp & Sons Ltd, Sail Makers & Ship Chandlers (High St, 1982); Barnetts Footwear (Wright St, 1979); Bentley's Snowflake Laundry (Greek St, 1985); Binnington (Beverley Rd, 1989); Southwells (Holderness Rd, 1989); Bush Opticians (1989); Trippetts for Gloves & Hosiery (1981).
  - **Place names:** Midland Cafe (Midland St, 1981); Park Pet Stores (1979); East Hull Hairdressing Salon (1982); Kingston Rubber Co (1986); Hull Truss & Surgical Co (1982); Bridge Town take-away (Spring Bank, 1983); Newbridge Trophy Centre (1989); Alexandra Hotel (Hessle Rd, 1981).
  - **Fanciful or pun names:** Clip Joint, Mayfair Unisex Salon, Shades, Floggits, Bandbox, Treasure Chest, The Fish Hole, Phoenix Fitness Centre, Vogue, Clairvoyant Shop of Mystery.
  - Generic signs: Boot Repairs, Fresh Meat, Refreshments.

**Taxis: the phone-number pattern**
- "57 Cars", 797 Hessle Road, Hull HU4. Later "57 Taxis", with 150 cars before merging into Drive in 2017. Telephone 01482 575757 (OPENED: https://www.kingstonuponhull.co.uk/info/3448/; SNIPPET, taxihull.co.uk). "Ken Kars" is listed at the same address.
- Inference (OBSERVATION): the firm is named after its repeating phone number.
- Hull numbering was run by the Hull municipal telephone service, later Kingston Communications, not by BT.
  - The code was 0482 until PhONEday, 16 Apr 1995.
  - An m2 snippet says Kingston changed "all five digit numbers to six digits" then (SNIPPET: https://m2.co.uk/m2/web/story.php/1996852568440080DDE88025683B0029F281).
  - Wikipedia shows (0482) xxxxxx before (OPENED, not detailed).
  - **So a 1990 Hull number was probably five or six digits.** A "57575"-style number, on a firm called "57 Cars", would fit (inference).
- No period directory listing of 1990 minicab names was reached. The "Mick's Taxis" and "Hessle Road Cars" patterns fit the evidence above but are not documented here (GENERAL).

**Grimsby**
- "Mad Harry's" discount store, Freeman St, from 1983 (SNIPPET, Grimsby Telegraph). A nickname for a shop.
- Moisers, Freeman St, from 1900: a surname for a shop.
- Cottees (SNIPPET).

---

## Not reached / gaps
- The UCL GB Names profiler, 1881 and 1998 (dynamic site).
- A Grimsby phone-book list of common surnames.
- Hull-specific Polish, Ukrainian, Irish and South Asian sources.
- 1991 census figures for Hull and Grimsby. The Warwick CRER PDF would not parse, and no PDF tools are installed.
- Any regional breakdown of first names.
