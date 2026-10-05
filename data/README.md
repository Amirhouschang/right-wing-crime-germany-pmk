# Notes on the data / Hinweise zu den Daten

🇬🇧 [English](#english) · 🇩🇪 [Deutsch](#deutsch)

---

## English

### Data gaps

- **Types of offence, Germany, 2015 and 2016:** the reports of the BMI are no longer available. Total and violent offences are available.
- **Coercion and threat (PMK -rechts-), 2020 and 2021:** not found in the available sources.
- **Insult before 2019:** not a separate category, included in "other offences".
- **Totals per federal state, 2014 to 2021:** not found. For 2014 only violent offences per state. The analysis of the federal states therefore covers 2022 to 2025.

### Notes on data collection

- The PMK data is not published in one central place. It is spread across fact sheets of the BKA and BMI, older reports and printed papers of the Bundestag (answers to parliamentary questions).
- Some older reports of the BMI can no longer be found online.
- Compiling the data was laborious and done by hand. All values were taken from the original documents; nothing was estimated or filled in.
- Whether the scattered publication is intended or follows from publication practice is not assessed here.
- The gaps result from the availability of sources, not from selection.

### Structure

| Folder | Files | Source | Content |
|---|---|---|---|
| `raw/pmk_bund/` | Fact sheets and figures of BKA and BMI 2018 to 2025, `1805758.pdf`, `pmk-2018-deliktsbereiche.pdf`, `pmk-2019-deliktsbereiche.pdf` | BKA, BMI, German Bundestag | Right-wing motivated offences, Germany, 2014 to 2025: total, violent offences, types of offence |
| `raw/pmk_laender/` | `2007594.pdf`, `2101418.pdf`, `2105639.pdf` | Bundestag printed papers 20/7594, 21/1418, 21/5639 | Right-wing motivated offences per federal state, 2022 to 2025: total and violent offences |
| `raw/wahlen/` | `btw17_kerg2.csv`, `btw21_kerg2.csv`, `btw25_kerg2.csv`, `ew_2014_2019_2024/` | Federal Returning Officer | Election results: federal elections 2017, 2021, 2025; European elections 2014, 2019, 2024 |
| `raw/bevoelkerung/` | `12411-0010_de.csv` | Destatis, table 12411-0010 | Population per federal state, 31 December, 2016 to 2025 |
| `clean/` | `pmk_rechts_bund.csv`, `pmk_rechts_laender.csv` | Transcribed by hand from the PDFs in `raw/` | Crime figures with the source of every value (file name and page) |
| `clean/` | `pmk_right_federal.csv`, `pmk_right_states.csv`, `afd_results.csv`, `population_states.csv` | Created by `notebooks/01_data_preparation.ipynb` | Tables used for the analysis and the dashboard |

### Notes for use

- **Election files** (`kerg2`, flat format): header in row 10 (`skiprows=9`), `sep=';'`, `decimal=','`, `encoding='utf-8-sig'`. AfD: `Gruppenname == 'AfD'`, `Gebietsart` = `Land` or `Bund`. Federal elections: second vote (`Stimme == 2`). European elections: only one vote (`Stimme == 1`).
- **European election 2014** has an older table format (`ew2014_kerg.csv`, Latin-1, header in two rows) and no percentages. The AfD share is calculated as votes divided by valid votes.
- **Federal election 2021:** original result of 26 September 2021, without the repeat election in parts of Berlin in 2024.
- **Rates per 100,000 inhabitants** are own calculations: offences ÷ inhabitants × 100,000. Population from table 12411-0010 (31 December), from 2022 based on the census of 2022. The rates printed in the Bundestag papers are not used.
- **State figures of 2022** are given by time of the offence (paper 20/7594). **2023 to 2025** are annual figures with the cut-off date 31 January of the following year. Whether both methods are fully comparable was not verified.
- **Violent offences per state in 2025** were counted from the list of single cases in paper 21/5639 (marked `gezaehlt` in `pmk_rechts_laender.csv`).
- The statistics count cases when the police report them; cases can be reported later. The figures for 2025 may still change.
- Right-wing motivated = classification of the police (PMK -rechts-).
- Election results and crime figures are shown side by side, with no causal claim. European and federal elections are not directly comparable.

---

## Deutsch

### Datenlücken

- **Deliktarten, Deutschland, 2015 und 2016:** Die Berichte des BMI sind nicht mehr abrufbar. Gesamtzahl und Gewaltdelikte liegen vor.
- **Nötigung/Bedrohung (PMK -rechts-), 2020 und 2021:** in den verfügbaren Quellen nicht gefunden.
- **Beleidigung vor 2019:** keine eigene Kategorie, steckt in „Andere Straftaten".
- **Gesamtzahlen je Bundesland, 2014 bis 2021:** nicht gefunden. Für 2014 nur Gewaltdelikte je Land. Die Analyse der Bundesländer umfasst deshalb 2022 bis 2025.

### Hinweise zur Datensammlung

- Die PMK-Daten liegen nicht an einer zentralen Stelle. Sie sind verteilt auf Factsheets von BKA und BMI, ältere Berichte und Bundestagsdrucksachen (Antworten auf Kleine Anfragen).
- Einige ältere Berichte des BMI sind online nicht mehr auffindbar.
- Die Zusammenstellung war aufwendig und erfolgte von Hand. Alle Werte wurden aus den Originaldokumenten übernommen, nichts wurde geschätzt oder ergänzt.
- Ob die verstreute Veröffentlichung beabsichtigt ist oder aus der Veröffentlichungspraxis folgt, wird hier nicht beurteilt.
- Die Lücken sind Folge der Quellenlage, nicht der Auswahl.

### Struktur

| Ordner | Dateien | Quelle | Inhalt |
|---|---|---|---|
| `raw/pmk_bund/` | Factsheets und Fallzahlen von BKA und BMI 2018 bis 2025, `1805758.pdf`, `pmk-2018-deliktsbereiche.pdf`, `pmk-2019-deliktsbereiche.pdf` | BKA, BMI, Deutscher Bundestag | Rechts motivierte Straftaten, Deutschland, 2014 bis 2025: Gesamtzahl, Gewaltdelikte, Deliktarten |
| `raw/pmk_laender/` | `2007594.pdf`, `2101418.pdf`, `2105639.pdf` | Bundestagsdrucksachen 20/7594, 21/1418, 21/5639 | Rechts motivierte Straftaten je Bundesland, 2022 bis 2025: Gesamtzahl und Gewaltdelikte |
| `raw/wahlen/` | `btw17_kerg2.csv`, `btw21_kerg2.csv`, `btw25_kerg2.csv`, `ew_2014_2019_2024/` | Die Bundeswahlleiterin | Wahlergebnisse: Bundestagswahlen 2017, 2021, 2025; Europawahlen 2014, 2019, 2024 |
| `raw/bevoelkerung/` | `12411-0010_de.csv` | Destatis, Tabelle 12411-0010 | Bevölkerung je Bundesland, 31. Dezember, 2016 bis 2025 |
| `clean/` | `pmk_rechts_bund.csv`, `pmk_rechts_laender.csv` | Von Hand aus den PDFs in `raw/` übertragen | Kriminalitätszahlen mit der Quelle jedes Wertes (Dateiname und Seite) |
| `clean/` | `pmk_right_federal.csv`, `pmk_right_states.csv`, `afd_results.csv`, `population_states.csv` | Erzeugt von `notebooks/01_data_preparation.ipynb` | Tabellen für Analyse und Dashboard |

### Hinweise zur Nutzung

- **Wahldateien** (`kerg2`, Flachformat): Kopfzeile in Zeile 10 (`skiprows=9`), `sep=';'`, `decimal=','`, `encoding='utf-8-sig'`. AfD: `Gruppenname == 'AfD'`, `Gebietsart` = `Land` oder `Bund`. Bundestagswahlen: Zweitstimme (`Stimme == 2`). Europawahlen: nur eine Stimme (`Stimme == 1`).
- **Europawahl 2014** hat ein älteres Tabellenformat (`ew2014_kerg.csv`, Latin-1, Kopfzeile über zwei Zeilen) und keine Prozentwerte. Der AfD-Anteil ist berechnet als Stimmen geteilt durch gültige Stimmen.
- **Bundestagswahl 2021:** ursprüngliches Ergebnis vom 26. September 2021, ohne die Wiederholungswahl in Teilen Berlins 2024.
- **Raten je 100.000 Einwohner** sind eigene Berechnungen: Straftaten ÷ Einwohner × 100.000. Einwohner aus Tabelle 12411-0010 (31. Dezember), ab 2022 auf Basis des Zensus 2022. Die in den Drucksachen abgedruckten Raten werden nicht verwendet.
- **Länderzahlen 2022** sind nach Tatzeit angegeben (Drucksache 20/7594). **2023 bis 2025** sind Jahresfallzahlen mit Stichtag 31. Januar des Folgejahres. Ob beide Zählweisen voll vergleichbar sind, wurde nicht geprüft.
- **Gewaltdelikte je Land 2025** wurden aus der Liste der Einzelfälle in Drucksache 21/5639 gezählt (in `pmk_rechts_laender.csv` mit `gezaehlt` markiert).
- Die Statistik zählt Fälle bei Meldung durch die Polizei; Fälle können nachgemeldet werden. Die Zahlen für 2025 können sich noch ändern.
- Rechts motiviert = Einstufung der Polizei (PMK -rechts-).
- Wahlergebnisse und Straftaten stehen nebeneinander, ohne Kausalaussage. Europa- und Bundestagswahlen sind nicht direkt vergleichbar.
