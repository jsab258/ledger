# Game terms and study law: four reference games (17 Nov 2026)

Not legal advice. This is fact-gathering by a research helper, read on 17 Nov 2026. Where a page could not be read it says so. Anything not read in a primary text is marked UNVERIFIED. A Swiss lawyer is the right person for any real answer.

The question: can the maker study four Steam games he owns for numbers only (triangle, bone and LOD counts, texture sizes, frame times), with no asset copied into his game, by four methods:
(a) reading the games' own config text files;
(b) running UE4SS, a mod framework that loads a DLL into the game to dump a type map;
(c) opening the packed files offline with FModel, which needs the game's AES key;
(d) timing frames from outside with Intel PresentMon.

Method note: the fetch tool returns summaries and short quotes, not whole pages, so "read in full" was not possible for the long agreements. Quotes below are short extracts as returned.

## 1. App ids and engines (confirmed)

| Game | Steam app id | Developer / publisher | Engine | Source (read 17 Nov 2026) |
|---|---|---|---|---|
| Silent Hill 2 (remake) | 2124490 | Bloober Team / Konami | Unreal Engine | https://store.steampowered.com/app/2124490/SILENT_HILL_2/ and https://steamdb.info/app/2124490 |
| inZOI | 2456740 | inZOI Studio / KRAFTON | Unreal Engine (UNVERIFIED here, not shown on page read) | https://store.steampowered.com/app/2456740 |
| Mafia: The Old Country | 1941540 | Hangar 13 / 2K | Unreal Engine; Denuvo Anti-tamper listed | https://store.steampowered.com/app/1941540 and https://steamdb.info/app/1941540 |
| Kingdom Come: Deliverance II | 1771300 | Warhorse / Deep Silver (PLAION) | CryEngine (the official mod tools are "our build of the CryEngine Sandbox") | https://store.steampowered.com/app/1771300 and https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/modding-in-kingdom-come-deliverance-2 |

Fact worth noting: Kingdom Come II is not an Unreal game, so UE4SS and FModel (Unreal tools) do not apply to it at all. Its paks are CryEngine paks.

## 2. Each game's EULA or terms

### Silent Hill 2 (Konami)
- The Steam store page lists no game-specific EULA, only the Steam Subscriber Agreement. https://store.steampowered.com/app/2124490/SILENT_HILL_2/ (read 17 Nov 2026)
- SteamDB lists no EULA entry for the app. https://steamdb.info/app/2124490 (read 17 Nov 2026)
- So on Steam, the Steam Subscriber Agreement appears to be the only licence text. The direct EULA address store.steampowered.com/eula/2124490_eula_0 was not reachable (permission prompt timed out). Konami's EU terms page failed to load. No Konami mod policy for this game was found. UNVERIFIED whether Konami has any separate PC terms for it.

### inZOI (KRAFTON)
- The Steam page says the game "Requires agreement to a 3rd-party EULA" and links https://store.steampowered.com//eula/2456740_eula_0. (read 17 Nov 2026, store page)
- That EULA page itself was not reachable (permission prompt timed out). Its clauses on reverse engineering and modding are UNVERIFIED.
- inZOI ModKit Distribution Terms, KRAFTON, effective 29 May 2025: covers mods and the official ModKit only; the game itself falls under "the inZOI Terms of Service and License Agreement", and these terms control only where they conflict about mods. Key extracts: "Mods cannot change, reproduce or otherwise alter the Game code, object code, source code or the internal structure." Changes to "Non-Modifiable Content" "are not permitted." On unofficial tools: "the Company makes no guarantees regarding their security, functionality, or compatibility" (no ban stated). Reverse engineering, asset extraction, data mining and circumvention are not mentioned. No governing law given. https://cdn1.epicgames.com/eulatracking-download/inzoimodkit/en/v1/r1/c846078e4e85d06d54d92de7ab7b6288.pdf (read 17 Nov 2026)
- playinzoi.com mod guide: mods are made with the official ModKit and shared via CurseForge or external sites; no ban on script frameworks or extraction stated; no link to a mods policy page. https://playinzoi.com/guide/mod (read 17 Nov 2026)
- The mods policy page https://playinzoi.com/clause/mods_policy was not reachable. UNVERIFIED.
- Press report (25 Mar 2025) of the inZOI team's Steam notice before Early Access: they will not tolerate "any unauthorized or harmful modifications that affect gameplay balance or security"; a listed violation is "Manipulating or making unauthorized modifications to game data"; they plan "strict legal actions" against illegal copies, unauthorized mods and illicit download sites. Secondary source. https://gamingph.com/2025/03/inzoi-takes-firm-stance-against-piracy-and-unauthorized-mods-ahead-of-early-access-launch (read 17 Nov 2026)

### Mafia: The Old Country (2K / Take-Two)
- SteamDB lists "Mafia: The Old Country EULA", id 1941540_eula_0, version 1. https://steamdb.info/app/1941540 (read 17 Nov 2026)
- That Steam EULA page holds a copy of the Take-Two Terms of Service (no date or version shown). Extracts: "Unauthorized copying, alteration, reverse engineering, decompiling, transmission" are prohibited and violate the ToS; "copy protection circumvention is prohibited and violates the ToS." Breach can lead to restriction or termination of game or online account access. No "except as permitted by law" wording found in that copy. Mods, data mining, asset extraction and third-party software not addressed there. It points to take2games.com/legal for the full terms. https://store.steampowered.com/eula/1941540_eula_0 (read 17 Nov 2026)
- The full Take-Two terms and https://www.2k.com/en-US/eula were not reachable. Governing law for Swiss residents: UNVERIFIED.
- No 2K mod policy page was found. UNVERIFIED whether one exists.
- Denuvo Anti-tamper is listed on SteamDB (see table). That matters for (b): a DLL loaded into the process is the kind of thing anti-tamper exists to detect.

### Kingdom Come: Deliverance II (PLAION / Warhorse)
- EULA, licensor PLAION GmbH, Hoefen, Austria, dated January 2025. https://store.steampowered.com//eula/1771300_eula_0 (read 17 Nov 2026). Extracts:
  - Section 5 bans: "reverse engineer, derive source code from, modify, disassemble, decompile" the game, and to "Alter or modify or attempt to alter or modify any part of the Game or other Services", and to create "derivative works based on or related to the Game". No "unless permitted by law" carve-out in that clause.
  - Data mining: bans "any unauthorized process or software that intercepts, collects, reads, or 'mines' information" generated or stored by the game, and "automated devices, such as spiders, robots or data mining techniques to catalog, download" content.
  - Section 6: "The Game may be protected by technical protection measures and digital rights management." Bans hacking and cracking.
  - Cheats: bans "'auto' software programs, 'macro' software programs" and "'cheat utility' software".
  - Section 21: the EULA "does not change your rights under the laws of your jurisdiction if the laws of your jurisdiction do not allow it." Section 3: backup copies "only allowed within the scope of legal regulations."
  - Section 18, governing law: for residents of the EU, UK, Norway, Switzerland or Russia, the law and courts of the country of residence. So Swiss law governs for a Zug resident.
- Official modding guide (last updated 14 Mar 2025): official Modding Tools on Steam (Editor.exe, "our build of the CryEngine Sandbox"); Steam Workshop recommended; third-party mod managers "not officially supported"; "You can't sell your mods or put them behind a paywall"; do not "incorporate it into other games or products"; "Your UGC only works together with Kingdom Come: Deliverance 2"; the EULA wins over the guidelines on conflict. Asset extraction and reverse engineering not addressed. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/modding-in-kingdom-come-deliverance-2 (read 17 Nov 2026)

## 3. Steam Subscriber Agreement

Source: https://store.steampowered.com/subscriber_agreement/ (read 17 Nov 2026). "This Agreement was last updated on September 10, 2026."

- Section 1.B: some subscriptions carry extra terms, such as "an end user license agreement specific to a particular game"; these bind once accepted.
- Section 2.G (restrictions): use is for personal, non-commercial purposes; without Valve's written consent you may not "reverse engineer, derive source code from, modify, disassemble, decompile, create derivative works based on" the Content and Services. The section carries an exception for what is allowed "under applicable law notwithstanding these restrictions."
- Section 4.B (cheating and tampering): "You agree that you will not create Cheats or assist third parties in any way to create or use Cheats"; you agree not to "directly or indirectly disable, circumvent, or otherwise interfere with the operation of software" meant to prevent cheating; you agree not to tamper with Steam or the Content and Services unless authorized; "You may not use Cheats, mods, hacks, or any other unauthorized third-party software" to modify marketplace processes, account creation or Steam's interface.
- Section 10: headed for subscribers outside the EU and UK, Washington law; but also "This Agreement is governed by the law of the country where you have your habitual residence" (as summarised). How these two lines apply to a Swiss resident: UNVERIFIED, needs a full read of section 10.
- No Switzerland-specific clause found.

## 4. Swiss law (URG, SR 231.1)

Source: the federal German PDF of the URG, "Stand am 1. Juli 2025", published by the Confederation: https://res.cloudinary.com/adminch/image/private/s--ga863q07--/v1719842041/Bundespublikationen/231-1d.pdf (read 17 Nov 2026). fedlex.admin.ch itself was not fetched (it renders by script); this PDF is the Confederation's own publication. English wording cross-checked against the unofficial translation at https://lawbrary.ch/law/art/URG-v2023.07-en-art-21/print and https://lawbrary.ch/law/art/URG-v2023.07-en-art-39a/print (status 1 July 2023; read 17 Nov 2026). Only the federal publication is binding.

Art. 19 (Verwendung zum Eigengebrauch), private use
- Abs. 1: "Veröffentlichte Werke dürfen zum Eigengebrauch verwendet werden. Als Eigengebrauch gilt: a. jede Werkverwendung im persönlichen Bereich und im Kreis von Personen, die unter sich eng verbunden sind, wie Verwandte oder Freunde; b. jede Werkverwendung der Lehrperson für den Unterricht in der Klasse; c. das Vervielfältigen von Werkexemplaren in Betrieben, öffentlichen Verwaltungen, Instituten, Kommissionen und ähnlichen Einrichtungen für die interne Information oder Dokumentation."
- Abs. 4: "Dieser Artikel findet keine Anwendung auf Computerprogramme." (This article does not apply to computer programs.)

Art. 21 (Entschlüsselung von Computerprogrammen), decompilation
- Abs. 1: "Wer das Recht hat, ein Computerprogramm zu gebrauchen, darf sich die erforderlichen Informationen über Schnittstellen zu unabhängig entwickelten Programmen durch Entschlüsselung des Programmcodes beschaffen oder durch Drittpersonen beschaffen lassen."
- Abs. 2: "Die durch Entschlüsselung des Programmcodes gewonnenen Schnittstelleninformationen dürfen nur zur Entwicklung, Wartung sowie zum Gebrauch von interoperablen Computerprogrammen verwendet werden, soweit dadurch weder die normale Auswertung des Programms noch die rechtmässigen Interessen der Rechtsinhaber und -inhaberinnen unzumutbar beeinträchtigt werden."
- English (unofficial): "Any person who has the right to use a computer program may obtain" the necessary interface information by decoding the program code; the information "may only be used for the development, maintenance and use of interoperable computer programs."
- Plain reading (not advice): Art. 21 is about interface information for interoperability. Gathering polygon or bone counts for one's own different game is not obviously an interoperability purpose.

Art. 24 Abs. 2 (backup copy): "Wer das Recht hat, ein Computerprogramm zu gebrauchen, darf davon eine Sicherungskopie herstellen; diese Befugnis kann nicht vertraglich wegbedungen werden." Note: the Act says in so many words that the backup right cannot be removed by contract; Art. 21 has no such sentence. Whether Art. 21 can be overridden by a EULA under Swiss law: UNVERIFIED, no commentary reached.

Art. 12 Abs. 2: "Hat ein Urheber oder eine Urheberin ein Computerprogramm veräussert oder der Veräusserung zugestimmt, so darf dieses gebraucht oder weiterveräussert werden."

Art. 39a (Schutz technischer Massnahmen), technological measures
- Abs. 1: "Wirksame technische Massnahmen zum Schutz von Werken und anderen Schutzobjekten dürfen nicht umgangen werden."
- Abs. 2: "Als wirksame technische Massnahmen im Sinne von Absatz 1 gelten Technologien und Vorrichtungen wie Zugangs- und Kopierkontrollen, Verschlüsselungs-, Verzerrungs- und andere Umwandlungsmechanismen, die dazu bestimmt und geeignet sind, unerlaubte Verwendungen von Werken und anderen Schutzobjekten zu verhindern oder einzuschränken."
- Abs. 3: bans making, importing, offering, distributing, renting, advertising, or possessing for commercial purposes, devices or services that are marketed for circumvention, have only limited commercial purpose besides circumvention, or are mainly designed to enable it.
- Abs. 4: "Das Umgehungsverbot kann gegenüber denjenigen Personen nicht geltend gemacht werden, welche die Umgehung ausschliesslich zum Zweck einer gesetzlich erlaubten Verwendung vornehmen."
- Encryption ("Verschlüsselungs-") is named in Abs. 2 as an example of an effective measure.

Art. 69a Abs. 1 lit. a (penalty, on complaint): a fine for whoever intentionally and unlawfully "wirksame technische Massnahmen nach Artikel 39a Absatz 2 mit der Absicht umgeht, eine gesetzlich unerlaubte Verwendung von Werken oder anderen Schutzobjekten vorzunehmen".

## 5. EU Software Directive 2009/24/EC (for comparison; Switzerland is not in the EU)

Source: the text as adopted, mirrored at https://legislation.gov.uk/eudr/2009/24/adopted?view=plain (read 17 Nov 2026). eur-lex itself returned only navigation, so the eur-lex text was not read; the legislation.gov.uk copy is the adopted EU text.

- Art. 5(3): "The person having a right to use a copy of a computer program shall be entitled, without the authorisation of the rightholder, to observe, study or test the functioning of the program in order to determine the ideas and principles which underlie any element of the program if he does so while performing any of the acts of loading, displaying, running, transmitting or storing the program which he is entitled to do."
- Art. 6(1): decompilation without authorisation where "indispensable to obtain the information necessary to achieve the interoperability of an independently created computer program with other programs", if (a) done by a licensee or person with a right to use, (b) the information "has not previously been readily available", (c) "confined to the parts of the original program which are necessary in order to achieve interoperability."
- Art. 6(2): the information may not be used "for goals other than to achieve the interoperability", given to others except as needed, or used "for the development, production or marketing of a computer program substantially similar in its expression, or for any other act which infringes copyright."
- Art. 6(3): not to be applied in a way that "unreasonably prejudices the rightholder's legitimate interests or conflicts with a normal exploitation of the computer program."
- Art. 8, second paragraph: "Any contractual provisions contrary to Article 6 or to the exceptions provided for in Article 5(2) and (3) shall be null and void."
- Art. 7(1)(c): member states must act against putting into circulation or commercial possession of means whose "sole intended purpose" is circumventing a technical device protecting a program.
- Switzerland has no word-for-word counterpart to Art. 5(3) in the URG articles read above. Whether Swiss courts read an observe-study-test right into Swiss law: UNVERIFIED.

## 6. Is using a game's AES key to read its paks "circumvention"? (opinion only)

Everything in this section is opinion or background, not law.

- Statute: Art. 39a Abs. 2 URG names encryption as an effective measure; Abs. 4 lifts the ban for circumvention done solely for a legally permitted use. The open question is whether reading the paks for numbers is a legally permitted use. Art. 19 private use does not cover computer programs (Art. 19 Abs. 4), but game art such as textures and meshes may be works other than programs (see the EU case below). Not settled by anything reached. (Federal PDF above, read 17 Nov 2026.)
- Urs Gasser, testimony blog on the Swiss bill, 25 Aug 2006: the ban "cannot be enforced against individuals who circumvent TPMs" to make uses the Act traditionally allows, private copying as his example; and "The ban of trafficking in circumvention devices is absolute." Opinion. https://archive.blogs.harvard.edu/ugasser/2006/08/25/testifying-on-swiss-drm-protection-bill/ (read 17 Nov 2026)
- Lexology overview "Copyright in Switzerland" (no author or date shown, events to Feb 2019): circumvention for duplication is "permitted solely if allowed by law", e.g. "to use an acquired work in the private sphere." Opinion. https://www.lexology.com/library/detail.aspx?g=c0c7b23c-9e83-44d2-9071-f61c93b92b89 (read 17 Nov 2026)
- Swiss IPI observatory on TV encryption: treats the copy-protection part of an encryption system as under Art. 39a, and checks whether it leaves room for private use. Different facts (TV), shows how the office reasons. https://www.ige.ch/de/etwas-schuetzen/urheberrecht/beobachtungsstelle-btm/untersuchungen-und-meldungen/digitales-fernsehen-verschluesselung-von-tv-programmen (read 17 Nov 2026)
- EU, Nintendo v PC Box (CJEU C-355/12), as summarised by Gareth Dickson (Society for Computers and Law, undated): video games are "complex matter", not merely computer programs; their graphic and sound elements are protected under the Copyright (InfoSoc) Directive, whose TPM rules apply; TPM protection "must nonetheless remain proportionate." EU law, not Swiss; persuasive at most. https://www.scl.org/3014-game-over-for-excessive-tpm-the-nintendo-ruling/ (read 17 Nov 2026)
- Background, not opinion on law: an Unreal forum thread (2015 to 2016, no Epic staff identified) describes pak encryption as a way "To protect your content from exploration/extraction", with the key compiled into the build. https://forums.unrealengine.com/t/protect-pak-file-from-unpack/334792 (read 17 Nov 2026). A hobby page (modified 7 Nov 2026) says "AES keys are the same for every user" and points to a forum thread on CS.RIN.RU (a site associated with game piracy) or a key-dumping tool to get them; it does not discuss legality. https://www.ultracomfy.net/unreal_engine_extraction (read 17 Nov 2026). Point for the maker: the key's purpose as stated is to stop extraction, which is the Art. 39a Abs. 2 wording ("dazu bestimmt ... unerlaubte Verwendungen ... zu verhindern"); and getting a key from such a forum is its own problem.
- No Swiss court decision or Swiss commentary on game pak keys was found. UNVERIFIED either way.

## 7. Per method, what bears on it (facts, not a verdict)

- (a) Config text files: reading plain files the game installs, without changing them. No clause found that bans reading them; KCD2's data-mining clause bans "unauthorized process or software that ... reads, or 'mines' information" stored by the game, which in plain words could reach automated reading. SSA 2.G is about modifying and reverse engineering, not reading. Lowest exposure of the four.
- (b) UE4SS DLL in the process: SSA 4.B (tampering, "mods, hacks, or any other unauthorized third-party software", not interfering with anti-cheat); SSA 2.G (modify, reverse engineer); Take-Two ToS for Mafia (alteration, reverse engineering, "copy protection circumvention"), plus Denuvo Anti-tamper listed for Mafia; inZOI ModKit terms ("Mods cannot change ... the internal structure"; inZOI EULA itself unread); not applicable to KCD2 (CryEngine). Law: Art. 21 URG only for interface information for interoperability; Art. 19 private use excludes programs (Abs. 4); EU Art. 5(3) observe-study-test exists in the EU, not found in the URG.
- (c) FModel with the AES key: Art. 39a URG (encryption named as an effective measure; Abs. 4 exception only for a legally permitted use; Art. 69a penalty needs intent to make an unlawful use); EULA bans on reverse engineering, decompiling, copying and data mining (KCD2 section 5, Take-Two ToS, SSA 2.G); Take-Two's express ban on "copy protection circumvention". Also: FModel is an Unreal tool, so not for KCD2.
- (d) PresentMon from outside: no change to the game and no reading of its files; it reads the operating system's frame events. No clause found that reaches it. (PresentMon's own licence was not checked in this pass.)

## Unreached

- https://store.steampowered.com/eula/2124490_eula_0 (Silent Hill 2; permission prompt timed out; SteamDB lists no EULA for this app)
- https://store.steampowered.com//eula/2456740_eula_0 (inZOI EULA; permission prompt timed out)
- https://playinzoi.com/clause/mods_policy (inZOI mods policy; permission prompt timed out)
- https://www.2k.com/en-US/eula and take2games.com/legal (full Take-Two terms, governing law; not reached)
- https://www.konami.com/games/eu/en/pages/terms_and_conditions/ (site error)
- fedlex.admin.ch HTML (not fetched; the Confederation's PDF used instead)
- eur-lex.europa.eu text of 2009/24/EC (returned navigation only; legislation.gov.uk adopted text used)
- Federal Council message 06.031 of 2006 on Art. 39a (bundesblatt.weblaw.ch blocked by robots); Swiss commentary on whether Art. 21 can be overridden by contract
- https://www.swissrights.ch/gesetze/Artikel-39a-urg-2022-DE.php (site error)
- Full Steam Subscriber Agreement section 10 (governing law as it applies to a Swiss resident)
- Any 2K or Konami mod policy (none found)
- Intel PresentMon licence (not checked)
