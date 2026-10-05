"""Interactive dashboard: right-wing motivated offences in Germany and AfD election results.

Run from the project folder:  streamlit run dashboard/app.py
The data is prepared in notebooks/01_data_preparation.ipynb and read from data/clean/.
The dashboard is available in German and English (switch at the top of the page).

© 2026 Amirhoushang Rahmannejad. All rights reserved.
The code, texts and charts of this project may be viewed and checked, but not copied or reused.
The official data used here remains the property of the authorities that publish it (see "Sources").
"""
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------------------
# 1. Parameters and file paths
# ---------------------------------------------------------------------------

# Locate data/clean by walking up from the folder of this file
HERE = Path(__file__).resolve().parent
DATA_CLEAN = next(p / "data" / "clean" for p in [HERE, *HERE.parents] if (p / "data" / "clean").exists())

OFFENCE_TYPES = ["propaganda", "incitement_to_hatred", "insult", "property_damage", "violent", "coercion_threat"]
OTHER = "other"                                    # total minus the six types

# Three groups of federal states (grouping made in this project, not by the police)
STATE_GROUPS = {
    "east": ["Brandenburg", "Mecklenburg-Western Pomerania", "Saxony", "Saxony-Anhalt", "Thuringia"],
    "city": ["Berlin", "Bremen", "Hamburg"],
    "west": ["Baden-Württemberg", "Bavaria", "Hesse", "Lower Saxony", "North Rhine-Westphalia",
             "Rhineland-Palatinate", "Saarland", "Schleswig-Holstein"],
}
GROUP_OF_STATE = {state: group for group, members in STATE_GROUPS.items() for state in members}

# German names of the federal states (states missing here have the same name in both languages)
STATE_NAMES_DE = {
    "Bavaria": "Bayern", "Hesse": "Hessen", "Mecklenburg-Western Pomerania": "Mecklenburg-Vorpommern",
    "Lower Saxony": "Niedersachsen", "North Rhine-Westphalia": "Nordrhein-Westfalen",
    "Rhineland-Palatinate": "Rheinland-Pfalz", "Saxony": "Sachsen", "Saxony-Anhalt": "Sachsen-Anhalt",
    "Thuringia": "Thüringen", "Germany": "Deutschland",
}

BLUE, MUTED, ORANGE, GREEN = "#1f5a94", "#8a8a8a", "#eb6834", "#1baf7a"
GROUP_COLORS = {"east": ORANGE, "city": GREEN, "west": BLUE}
TYPE_COLORS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7", "#b5b5b5"]
INK, GRID = "#333333", "#e5e5e5"

# Measure: column with the number of offences, column with the unrounded rate, decimals shown
MEASURES = {"all": ("total", "total_rate", 1), "violent": ("violent", "violent_rate", 2)}
ELECTION_PAIRS = {"federal_2025": ("federal", 2025), "european_2024": ("european", 2024)}

# ---------------------------------------------------------------------------
# 2. Texts in both languages
# ---------------------------------------------------------------------------

TEXT = {
    "en": {
        "page_title": "Right-wing motivated offences in Germany",
        "title": "Right-wing motivated offences in Germany and AfD election results",
        "intro": ("Politically motivated crime, phenomenon area right-wing (PMK -rechts-), 2014 to 2025. "
                  "Police statistics published by the BKA and BMI, election results of the Federal Returning Officer. "
                  "The classification of the police is used."),
        "tabs": ["Germany 2014 to 2025", "Federal states 2022 to 2025", "AfD election results", "Data and limitations"],
        "groups": {"east": "Eastern states", "city": "City states", "west": "Western area states"},
        "types": {"propaganda": "Propaganda offences", "incitement_to_hatred": "Incitement to hatred",
                  "insult": "Insult", "property_damage": "Property damage", "violent": "Violent offences",
                  "coercion_threat": "Coercion and threat", "other": "Other offences", "total": "Total"},
        "measures": {"all": "All offences", "violent": "Violent offences"},
        "elections": {"federal": "Federal election", "european": "European election"},
        "pairs": {"federal_2025": "Federal election 2025 and offences 2025",
                  "european_2024": "European election 2024 and offences 2024"},
        "period": "Period", "since": "since", "year": "Year", "offences_filter": "Offences",
        "tile_offences": "Offences", "tile_violent": "Violent offences", "tile_violent_share": "Share of violent offences",
        "tile_peak": "Highest number of offences",
        "chart_total": "All right-wing motivated offences", "chart_violent": "Of which: violent offences",
        "axis_offences": "Registered offences", "axis_violent": "Registered violent offences",
        "hover_offences": "offences", "hover_violent": "violent offences",
        "types_title": "Types of offence", "show": "Show",
        "view_number": "Number of offences", "view_share": "Share in %", "axis_share": "Share in %",
        "types_note": ("Only years with all six types of offence are shown: {years}. "
                       "Other offences = total minus the six types (own calculation). "),
        "share_note": ("Share of each type of offence in all right-wing motivated offences of the year, in %. "
                       "Each chart has its own scale, so that small types can be read as well. "
                       "The shares of one year add up to 100 %."),
        "types_table": "Table: offences by type and year",
        "groups_filter": "Groups of states", "choose_group": "Choose at least one group of states.",
        "tile_germany": "Germany {year}, per 100,000 inhabitants", "tile_highest": "Highest", "tile_lowest": "Lowest",
        "tile_ratio": "Highest divided by lowest",
        "ranking_title": "{measure} per 100,000 inhabitants, {year}",
        "axis_rate": "Registered offences per 100,000 inhabitants", "axis_rate_short": "Offences per 100,000 inhabitants",
        "hover_rate": "per 100,000 inhabitants", "hover_inhabitants": "inhabitants", "germany": "Germany",
        "groups_title": "The three groups of states", "share_title": "Share of population and of offences, {year}",
        "row_offences": "Offences", "row_population": "Population",
        "all_years": "All years", "col_group": "Group", "col_state": "Federal state",
        "counted_note": " Violent offences per state in 2025 were counted from the list of single cases in printed paper 21/5639.",
        "no_cause": ("The figures are shown side by side. They do not show cause and effect. The comparison is about "
                     "federal states, not about people: it does not say who commits offences or who votes for which party."),
        "germany_time": "Germany: offences and AfD result over time", "axis_afd": "AfD share of votes in %",
        "states_scatter": "Federal states: AfD share and offence rate", "pair_filter": "Election and year of the offences",
        "corr_all": "Correlation, all 16 states", "corr_east": "Within the 5 eastern states",
        "corr_west": "Within the 8 western area states",
        "corr_note": ("Correlation coefficient: +1 means the same order of the states, 0 no relation, −1 the opposite order. "
                      "For the three city states no coefficient is given, three values do not carry one. "
                      "With five and eight states the coefficients within the groups are not reliable on their own."),
        "axis_afd_pair": "AfD share of votes, {election} {year}, in %", "axis_rate_pair": "{measure} per 100,000 inhabitants, {year}",
        "hover_afd": "AfD share", "second_votes": " Federal election: second votes.",
        "one_state": "One federal state over time", "state_filter": "Federal state",
        "one_state_note": ("{state} belongs to the group: {group}. Both charts use the same scale for every state, "
                           "so the states can be compared. Offence rates per federal state are available from 2022 only."),
        "source_federal": ("Source: BKA and BMI, figures on politically motivated crime 2018 to 2025; "
                           "German Bundestag, printed paper 18/5758 (2014)."),
        "source_states": ("Source: German Bundestag, printed papers 20/7594, 21/1418 and 21/5639 (offences); "
                          "Destatis, table 12411-0010 (population, 31 December). Own calculation: offences per 100,000 inhabitants."),
        "source_elections": "Election results: Federal Returning Officer (Die Bundeswahlleiterin), final results.",
        "limitations_title": "Limitations",
        "limitations": """
- **Registered offences, not all offences.** The statistics count only offences that became known to the police and that the police classified as politically right-wing motivated.
- **The classification is made by the police of each federal state** on their own responsibility. Differences between the states can reflect differences in recording practice as well as differences in the offences committed.
- **The figures count offences, not offenders.**
- **Types of offence are incomplete.** They are missing for 2015 and 2016, insult is a separate category from 2019 only, and coercion and threat is missing for 2020 and 2021.
- **Figures per federal state are available for 2022 to 2025 only.** The figures of 2022 are given by time of the offence, those of 2023 to 2025 as annual figures with the cut-off date 31 January of the following year.
- **Violent offences per state in 2025 were counted** from the list of single cases in Bundestag printed paper 21/5639.
- **The figures can still change,** because cases can be reported later. The figures for 2025 are the least settled.
- **The comparison with election results is descriptive.** It compares 16 federal states, not people, and shows no cause and effect. The grouping into eastern states, city states and western area states was made in this project.
""",
        "sources_title": "Sources",
        "sources_crime": ("All figures come from official, public sources. Nothing was estimated or filled in.\n\n"
                          "**Crime data.** Published by the Federal Criminal Police Office (Bundeskriminalamt, BKA) and the "
                          "Federal Ministry of the Interior (Bundesministerium des Innern, BMI), and by the German Bundestag as "
                          "answers of the Federal Government to parliamentary questions. The source of every single value, with "
                          "file name and page, is in the column `source` of the table \"Offences, Germany\" below."),
        "sources_crime_cols": ["Used for", "Document", "Pages of the PDF", "File in data/raw"],
        "sources_elections": ("**Election data.** Published by the Federal Returning Officer (Die Bundeswahlleiterin), Wiesbaden, "
                              "under the licence \"Datenlizenz Deutschland – Namensnennung – Version 2.0\". Federal elections: second votes."),
        "sources_elections_cols": ["Election", "Version", "File in data/raw/wahlen"],
        "sources_rest": ("**Population data.** Federal Statistical Office (Statistisches Bundesamt, Destatis), table 12411-0010 "
                         "\"Bevölkerung: Bundesländer, Stichtag\", reference date 31 December, retrieved on 5 October 2026.\n\n"
                         "**Own calculations.** Offences per 100,000 inhabitants, all shares and changes in percent, the group "
                         "\"other offences\", the figures for the three groups of states, the correlation coefficients, and the AfD "
                         "share in the European election of 2014 (votes divided by valid votes)."),
        "data_title": "Data",
        "data_tables": ["Offences, Germany (with source of every value)", "Offences, federal states", "AfD election results"],
        "download": "Download CSV",
        "copyright": "© 2026 Amirhoushang Rahmannejad. All rights reserved.",
        "rights": ("The code, texts and charts of this dashboard may be viewed and checked, but not copied or reused. "
                   "The official data remains the property of the authorities that publish it. "
                   "Sources: see the tab \"Data and limitations\"."),
    },
    "de": {
        "page_title": "Rechts motivierte Straftaten in Deutschland",
        "title": "Rechts motivierte Straftaten in Deutschland und AfD-Wahlergebnisse",
        "intro": ("Politisch motivierte Kriminalität, Phänomenbereich rechts (PMK -rechts-), 2014 bis 2025. "
                  "Polizeistatistik von BKA und BMI, Wahlergebnisse der Bundeswahlleiterin. "
                  "Es gilt die Einstufung der Polizei."),
        "tabs": ["Deutschland 2014 bis 2025", "Bundesländer 2022 bis 2025", "AfD-Wahlergebnisse", "Daten und Grenzen"],
        "groups": {"east": "Östliche Länder", "city": "Stadtstaaten", "west": "Westliche Flächenländer"},
        "types": {"propaganda": "Propagandadelikte", "incitement_to_hatred": "Volksverhetzung",
                  "insult": "Beleidigung", "property_damage": "Sachbeschädigung", "violent": "Gewaltdelikte",
                  "coercion_threat": "Nötigung/Bedrohung", "other": "Sonstige Straftaten", "total": "Gesamt"},
        "measures": {"all": "Alle Straftaten", "violent": "Gewaltdelikte"},
        "elections": {"federal": "Bundestagswahl", "european": "Europawahl"},
        "pairs": {"federal_2025": "Bundestagswahl 2025 und Straftaten 2025",
                  "european_2024": "Europawahl 2024 und Straftaten 2024"},
        "period": "Zeitraum", "since": "seit", "year": "Jahr", "offences_filter": "Straftaten",
        "tile_offences": "Straftaten", "tile_violent": "Gewaltdelikte", "tile_violent_share": "Anteil der Gewaltdelikte",
        "tile_peak": "Höchste Zahl an Straftaten",
        "chart_total": "Alle rechts motivierten Straftaten", "chart_violent": "Davon: Gewaltdelikte",
        "axis_offences": "Registrierte Straftaten", "axis_violent": "Registrierte Gewaltdelikte",
        "hover_offences": "Straftaten", "hover_violent": "Gewaltdelikte",
        "types_title": "Deliktarten", "show": "Anzeigen",
        "view_number": "Anzahl der Straftaten", "view_share": "Anteil in %", "axis_share": "Anteil in %",
        "types_note": ("Gezeigt werden nur Jahre, in denen alle sechs Deliktarten vorliegen: {years}. "
                       "Sonstige Straftaten = Gesamtzahl minus die sechs Deliktarten (eigene Berechnung). "),
        "share_note": ("Anteil jeder Deliktart an allen rechts motivierten Straftaten des Jahres, in %. "
                       "Jede Grafik hat ihre eigene Skala, damit auch kleine Deliktarten lesbar sind. "
                       "Die Anteile eines Jahres ergeben zusammen 100 %."),
        "types_table": "Tabelle: Straftaten nach Deliktart und Jahr",
        "groups_filter": "Ländergruppen", "choose_group": "Bitte mindestens eine Ländergruppe wählen.",
        "tile_germany": "Deutschland {year}, je 100.000 Einwohner", "tile_highest": "Höchster Wert", "tile_lowest": "Niedrigster Wert",
        "tile_ratio": "Höchster geteilt durch niedrigsten",
        "ranking_title": "{measure} je 100.000 Einwohner, {year}",
        "axis_rate": "Registrierte Straftaten je 100.000 Einwohner", "axis_rate_short": "Straftaten je 100.000 Einwohner",
        "hover_rate": "je 100.000 Einwohner", "hover_inhabitants": "Einwohner", "germany": "Deutschland",
        "groups_title": "Die drei Ländergruppen", "share_title": "Anteil an Bevölkerung und Straftaten, {year}",
        "row_offences": "Straftaten", "row_population": "Bevölkerung",
        "all_years": "Alle Jahre", "col_group": "Gruppe", "col_state": "Bundesland",
        "counted_note": " Die Gewaltdelikte je Land für 2025 wurden aus der Liste der Einzelfälle in Drucksache 21/5639 gezählt.",
        "no_cause": ("Die Zahlen stehen nebeneinander. Sie zeigen keinen ursächlichen Zusammenhang. Verglichen werden "
                     "Bundesländer, nicht Menschen: Der Vergleich sagt nicht, wer Straftaten begeht oder wer welche Partei wählt."),
        "germany_time": "Deutschland: Straftaten und AfD-Ergebnis im Zeitverlauf", "axis_afd": "AfD-Stimmenanteil in %",
        "states_scatter": "Bundesländer: AfD-Anteil und Straftatenrate", "pair_filter": "Wahl und Jahr der Straftaten",
        "corr_all": "Korrelation, alle 16 Länder", "corr_east": "Innerhalb der 5 östlichen Länder",
        "corr_west": "Innerhalb der 8 westlichen Flächenländer",
        "corr_note": ("Korrelationskoeffizient: +1 bedeutet dieselbe Reihenfolge der Länder, 0 keinen Zusammenhang, −1 die "
                      "umgekehrte Reihenfolge. Für die drei Stadtstaaten wird kein Wert angegeben, drei Werte tragen keinen. "
                      "Bei fünf und acht Ländern sind die Werte innerhalb der Gruppen für sich allein nicht belastbar."),
        "axis_afd_pair": "AfD-Stimmenanteil, {election} {year}, in %", "axis_rate_pair": "{measure} je 100.000 Einwohner, {year}",
        "hover_afd": "AfD-Anteil", "second_votes": " Bundestagswahl: Zweitstimmen.",
        "one_state": "Ein Bundesland im Zeitverlauf", "state_filter": "Bundesland",
        "one_state_note": ("{state} gehört zur Gruppe: {group}. Beide Grafiken haben für jedes Land dieselbe Skala, "
                           "die Länder sind also vergleichbar. Straftatenraten je Bundesland liegen erst ab 2022 vor."),
        "source_federal": ("Quelle: BKA und BMI, Fallzahlen zur politisch motivierten Kriminalität 2018 bis 2025; "
                           "Deutscher Bundestag, Drucksache 18/5758 (2014)."),
        "source_states": ("Quelle: Deutscher Bundestag, Drucksachen 20/7594, 21/1418 und 21/5639 (Straftaten); "
                          "Destatis, Tabelle 12411-0010 (Bevölkerung, 31. Dezember). Eigene Berechnung: Straftaten je 100.000 Einwohner."),
        "source_elections": "Wahlergebnisse: Die Bundeswahlleiterin, endgültige Ergebnisse.",
        "limitations_title": "Grenzen der Daten",
        "limitations": """
- **Registrierte Straftaten, nicht alle Straftaten.** Die Statistik zählt nur Straftaten, die der Polizei bekannt wurden und die sie als politisch rechts motiviert eingestuft hat.
- **Die Einstufung nimmt die Polizei des jeweiligen Bundeslandes** in eigener Verantwortung vor. Unterschiede zwischen den Ländern können auf unterschiedliche Erfassung ebenso zurückgehen wie auf Unterschiede bei den begangenen Straftaten.
- **Gezählt werden Straftaten, nicht Täter.**
- **Die Deliktarten sind unvollständig.** Sie fehlen für 2015 und 2016, Beleidigung ist erst ab 2019 eine eigene Kategorie, und Nötigung/Bedrohung fehlt für 2020 und 2021.
- **Zahlen je Bundesland gibt es nur für 2022 bis 2025.** Die Zahlen für 2022 sind nach Tatzeit angegeben, die für 2023 bis 2025 als Jahresfallzahlen mit Stichtag 31. Januar des Folgejahres.
- **Die Gewaltdelikte je Land für 2025 wurden gezählt,** aus der Liste der Einzelfälle in Bundestagsdrucksache 21/5639.
- **Die Zahlen können sich noch ändern,** weil Fälle nachgemeldet werden. Die Zahlen für 2025 sind am wenigsten gefestigt.
- **Der Vergleich mit Wahlergebnissen ist beschreibend.** Er vergleicht 16 Bundesländer, nicht Menschen, und zeigt keinen ursächlichen Zusammenhang. Die Einteilung in östliche Länder, Stadtstaaten und westliche Flächenländer stammt aus diesem Projekt.
""",
        "sources_title": "Quellen",
        "sources_crime": ("Alle Zahlen stammen aus amtlichen, öffentlichen Quellen. Nichts wurde geschätzt oder ergänzt.\n\n"
                          "**Kriminalitätsdaten.** Veröffentlicht vom Bundeskriminalamt (BKA) und vom Bundesministerium des Innern "
                          "(BMI) sowie vom Deutschen Bundestag als Antworten der Bundesregierung auf Kleine Anfragen. Die Quelle "
                          "jedes einzelnen Wertes, mit Dateiname und Seite, steht in der Spalte `source` der Tabelle "
                          "„Straftaten, Deutschland\" weiter unten."),
        "sources_crime_cols": ["Verwendet für", "Dokument", "Seiten der PDF", "Datei in data/raw"],
        "sources_elections": ("**Wahldaten.** Veröffentlicht von der Bundeswahlleiterin, Wiesbaden, unter der Lizenz "
                              "„Datenlizenz Deutschland – Namensnennung – Version 2.0\". Bundestagswahlen: Zweitstimmen."),
        "sources_elections_cols": ["Wahl", "Stand", "Datei in data/raw/wahlen"],
        "sources_rest": ("**Bevölkerungsdaten.** Statistisches Bundesamt (Destatis), Tabelle 12411-0010 "
                         "„Bevölkerung: Bundesländer, Stichtag\", Stichtag 31. Dezember, abgerufen am 5. Oktober 2026.\n\n"
                         "**Eigene Berechnungen.** Straftaten je 100.000 Einwohner, alle Anteile und Veränderungen in Prozent, "
                         "die Gruppe „Sonstige Straftaten\", die Werte für die drei Ländergruppen, die Korrelationskoeffizienten "
                         "und der AfD-Anteil bei der Europawahl 2014 (Stimmen geteilt durch gültige Stimmen)."),
        "data_title": "Daten",
        "data_tables": ["Straftaten, Deutschland (mit Quelle jedes Wertes)", "Straftaten, Bundesländer", "AfD-Wahlergebnisse"],
        "download": "CSV herunterladen",
        "copyright": "© 2026 Amirhoushang Rahmannejad. Alle Rechte vorbehalten.",
        "rights": ("Code, Texte und Grafiken dieses Dashboards dürfen angesehen und geprüft, aber nicht kopiert oder "
                   "weiterverwendet werden. Die amtlichen Daten bleiben Eigentum der veröffentlichenden Behörden. "
                   "Quellen: siehe Reiter „Daten und Grenzen\"."),
    },
}

# Every document the crime figures were taken from: (used for, document) in English and German, pages, file
CRIME_SOURCES = [
    ("Germany 2014", "Deutschland 2014", "German Bundestag, printed paper 18/5758", "Deutscher Bundestag, Drucksache 18/5758", "4, 5, 8, 9", "1805758.pdf"),
    ("Germany 2015 and 2016 (total, violent)", "Deutschland 2015 und 2016 (gesamt, Gewalt)", "BKA/BMI, figures on politically motivated crime 2021, ten-year series", "BKA/BMI, Fallzahlen PMK 2021, Zehnjahresreihe", "4, 7", "2021PMKFallzahlen.pdf"),
    ("Germany 2017 and 2018", "Deutschland 2017 und 2018", "BMI, offences by type 2017 and 2018", "BMI, Straftaten nach Deliktsbereichen 2017 und 2018", "1", "pmk-2018-deliktsbereiche.pdf"),
    ("Germany 2019", "Deutschland 2019", "BMI, offences by type 2018 and 2019", "BMI, Straftaten nach Deliktsbereichen 2018 und 2019", "1", "pmk-2019-deliktsbereiche.pdf"),
    ("Germany 2020", "Deutschland 2020", "BKA/BMI, figures on politically motivated crime 2020", "BKA/BMI, Fallzahlen PMK 2020", "2–5", "2020PMKFallzahlen.pdf"),
    ("Germany 2021", "Deutschland 2021", "BKA/BMI, figures on politically motivated crime 2021", "BKA/BMI, Fallzahlen PMK 2021", "4–7", "2021PMKFallzahlen.pdf"),
    ("Germany 2022", "Deutschland 2022", "BKA/BMI, fact sheets on politically motivated crime 2022", "BKA/BMI, Factsheets PMK 2022", "4–7", "pmk2022-factsheets.pdf"),
    ("Germany 2023", "Deutschland 2023", "BKA/BMI, fact sheets on politically motivated crime 2023", "BKA/BMI, Factsheets PMK 2023", "4–8", "pmk2023-factsheets.pdf"),
    ("Germany 2024", "Deutschland 2024", "BKA/BMI, figures on politically motivated crime 2024", "BKA/BMI, Fallzahlen PMK 2024", "4–8", "2024PMKFallzahlen.pdf"),
    ("Germany 2025", "Deutschland 2025", "BKA/BMI, figures on politically motivated crime 2025", "BKA/BMI, Fallzahlen PMK 2025", "4–9", "2025PMKFallzahlen.pdf"),
    ("Federal states 2022", "Bundesländer 2022", "German Bundestag, printed paper 20/7594", "Deutscher Bundestag, Drucksache 20/7594", "8", "2007594.pdf"),
    ("Federal states 2023 and 2024", "Bundesländer 2023 und 2024", "German Bundestag, printed paper 21/1418", "Deutscher Bundestag, Drucksache 21/1418", "2–4", "2101418.pdf"),
    ("Federal states 2025", "Bundesländer 2025", "German Bundestag, printed paper 21/5639", "Deutscher Bundestag, Drucksache 21/5639", "2, 5–60", "2105639.pdf"),
]
ELECTION_SOURCES = [
    ("European election, 25 May 2014", "Europawahl, 25. Mai 2014", "Final result", "Endgültiges Ergebnis", "ew2014_kerg.csv"),
    ("Federal election, 24 September 2017", "Bundestagswahl, 24. September 2017", "Final result, 6 October 2017", "Endgültiges Ergebnis, 6. Oktober 2017", "btw17_kerg2.csv"),
    ("European election, 26 May 2019", "Europawahl, 26. Mai 2019", "Final result, 24 June 2019", "Endgültiges Ergebnis, 24. Juni 2019", "ew2019_kerg2.csv"),
    ("Federal election, 26 September 2021", "Bundestagswahl, 26. September 2021", "Final result, 14 October 2021 (without the repeat election in parts of Berlin in 2024)", "Endgültiges Ergebnis, 14. Oktober 2021 (ohne die Wiederholungswahl in Teilen Berlins 2024)", "btw21_kerg2.csv"),
    ("European election, 9 June 2024", "Europawahl, 9. Juni 2024", "Final result, 26 June 2024", "Endgültiges Ergebnis, 26. Juni 2024", "ew2024_kerg2.csv"),
    ("Federal election, 23 February 2025", "Bundestagswahl, 23. Februar 2025", "Final result, 14 March 2025", "Endgültiges Ergebnis, 14. März 2025", "btw25_kerg2.csv"),
]


# ---------------------------------------------------------------------------
# 3. Helper functions
# ---------------------------------------------------------------------------

@st.cache_data
def load_data():
    federal_long = pd.read_csv(DATA_CLEAN / "pmk_right_federal.csv")
    states = pd.read_csv(DATA_CLEAN / "pmk_right_states.csv")
    afd = pd.read_csv(DATA_CLEAN / "afd_results.csv")
    states["group"] = states["state"].map(GROUP_OF_STATE)
    # Unrounded rates for all calculations (highest divided by lowest, correlations, order of the states).
    # The rounded columns total_per_100k and violent_per_100k of the table are used for display only.
    states["total_rate"] = 100_000 * states["total"] / states["population"]
    states["violent_rate"] = 100_000 * states["violent"] / states["population"]
    federal = federal_long.pivot(index="year", columns="offence", values="cases")[["total"] + OFFENCE_TYPES]
    return federal_long, federal, states, afd


def num(value, digits=0, sign=False):
    """Format a number in the chosen language: 42,544.5 in English, 42.544,5 in German."""
    text = f"{value:+,.{digits}f}" if sign else f"{value:,.{digits}f}"
    if LANG == "de":
        text = text.replace(",", "§").replace(".", ",").replace("§", ".")
    return text.replace("-", "−")


def state_name(state):
    return STATE_NAMES_DE.get(state, state) if LANG == "de" else state


def base_layout(fig, height=420, **kwargs):
    """Shared look of all charts: white surface, quiet grid, dark text, numbers in the chosen language."""
    fig.update_layout(
        height=height, margin=dict(l=10, r=10, t=30, b=10),
        plot_bgcolor="white", paper_bgcolor="white", font=dict(color=INK, size=13),
        hoverlabel=dict(bgcolor="white", font_size=13),
        separators=",." if LANG == "de" else ".,",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, title_text="", traceorder="normal"),
        **kwargs)
    fig.update_xaxes(showgrid=False, linecolor="#999999", ticks="outside", tickcolor="#999999")
    fig.update_yaxes(gridcolor=GRID, zeroline=False, rangemode="tozero")
    return fig


def full_width(element, *args, **kwargs):
    """Draw an element over the full width, with the argument of the installed Streamlit version."""
    try:
        return element(*args, width="stretch", **kwargs)
    except TypeError:                                   # older Streamlit versions
        return element(*args, use_container_width=True, **kwargs)


def show(fig):
    full_width(st.plotly_chart, fig, config={"displayModeBar": False})


def label_positions(x, y, labels, x_range, y_range, plot_width=760, plot_height=440, font_size=11):
    """Choose a position for every point label so that labels do not cover each other or other points.

    Each label is tried at eight positions around its point. The first position whose box does not
    overlap a label already placed or another point is taken; otherwise the position with the least overlap.
    """
    per_x = (x_range[1] - x_range[0]) / plot_width              # data units per pixel
    per_y = (y_range[1] - y_range[0]) / plot_height
    char, line, gap = 0.6 * font_size, 1.25 * font_size, 9      # pixels
    candidates = ["top center", "bottom center", "middle right", "middle left",
                  "top right", "top left", "bottom right", "bottom left"]

    def box(px, py, label, position):
        width, height = len(label) * char * per_x, line * per_y
        vertical, horizontal = position.split(" ")
        left = {"center": px - width / 2, "right": px + gap * per_x, "left": px - gap * per_x - width}[horizontal]
        bottom = {"middle": py - height / 2, "top": py + gap * per_y, "bottom": py - gap * per_y - height}[vertical]
        return left, bottom, left + width, bottom + height

    def overlap(a, b):
        return max(0, min(a[2], b[2]) - max(a[0], b[0])) * max(0, min(a[3], b[3]) - max(a[1], b[1]))

    marker = [(px - 7 * per_x, py - 7 * per_y, px + 7 * per_x, py + 7 * per_y) for px, py in zip(x, y)]
    placed, chosen = [], {}
    # Points with many close neighbours are placed first, they have the least room
    crowd = [sum(abs(px - qx) / per_x < 130 and abs(py - qy) / per_y < 45 for qx, qy in zip(x, y)) for px, py in zip(x, y)]
    for i in sorted(range(len(x)), key=lambda k: -crowd[k]):
        best, best_cost = candidates[0], None
        for position in candidates:
            candidate = box(x[i], y[i], labels[i], position)
            cost = sum(overlap(candidate, other) for other in placed)
            cost += sum(overlap(candidate, m) for k, m in enumerate(marker) if k != i)
            outside = candidate[0] < x_range[0] or candidate[2] > x_range[1] or candidate[3] > y_range[1] or candidate[1] < y_range[0]
            cost += 1e9 * outside
            if best_cost is None or cost < best_cost:
                best, best_cost = position, cost
            if cost == 0:
                break
        chosen[i] = best
        placed.append(box(x[i], y[i], labels[i], best))
    return [chosen[i] for i in range(len(x))]


# ---------------------------------------------------------------------------
# 4. Page header and language
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Rechts motivierte Straftaten · Right-wing motivated offences", layout="wide")
federal_long, federal, states, afd = load_data()
YEARS = sorted(federal.index)
STATE_YEARS = sorted(states["year"].unique())
FIRST_YEAR, LAST_YEAR = YEARS[0], YEARS[-1]

header = st.columns([4, 1])
LANG = "de" if header[1].radio("Sprache / Language", ["Deutsch", "English"], horizontal=True, key="language") == "Deutsch" else "en"
T = TEXT[LANG]
PERCENT = " %"

header[0].title(T["title"])
st.caption(T["intro"])
tab_germany, tab_states, tab_afd, tab_data = st.tabs(T["tabs"])


# ---------------------------------------------------------------------------
# 5. Germany 2014 to 2025
# ---------------------------------------------------------------------------

with tab_germany:
    first_year, last_year = st.select_slider(T["period"], options=YEARS, value=(FIRST_YEAR, LAST_YEAR), key="period")
    period = federal.loc[first_year:last_year]
    start, end = period.iloc[0], period.iloc[-1]

    def change(column):
        if first_year == last_year:
            return None
        return f"{num(100 * (end[column] / start[column] - 1), 1, sign=True)}{PERCENT} {T['since']} {first_year}"

    tile = st.columns(4)
    tile[0].metric(f"{T['tile_offences']} {last_year}", num(end["total"]), change("total"), delta_color="off")
    tile[1].metric(f"{T['tile_violent']} {last_year}", num(end["violent"]), change("violent"), delta_color="off")
    tile[2].metric(f"{T['tile_violent_share']} {last_year}", num(100 * end["violent"] / end["total"], 2) + PERCENT)
    tile[3].metric(f"{T['tile_peak']}: {period['total'].idxmax()}", num(period["total"].max()))

    left, right = st.columns(2)
    with left:
        st.subheader(T["chart_total"])
        fig = go.Figure(go.Bar(x=period.index, y=period["total"], marker_color=BLUE,
                               hovertemplate=f"%{{x}}: %{{y:,.0f}} {T['hover_offences']}<extra></extra>"))
        show(base_layout(fig, xaxis=dict(dtick=1), yaxis=dict(title=T["axis_offences"], tickformat=",")))
    with right:
        st.subheader(T["chart_violent"])
        fig = go.Figure(go.Scatter(x=period.index, y=period["violent"], mode="lines+markers",
                                   line=dict(color=BLUE, width=2), marker=dict(size=8),
                                   hovertemplate=f"%{{x}}: %{{y:,.0f}} {T['hover_violent']}<extra></extra>"))
        show(base_layout(fig, xaxis=dict(dtick=1), yaxis=dict(title=T["axis_violent"], tickformat=",")))
    st.caption(T["source_federal"])

    st.subheader(T["types_title"])
    complete = federal.dropna().astype(int)
    complete[OTHER] = complete["total"] - complete[OFFENCE_TYPES].sum(axis=1)
    types = complete[OFFENCE_TYPES + [OTHER]]
    as_share = st.radio(T["show"], ["number", "share"], horizontal=True, key="types_view",
                        format_func=lambda v: T["view_number"] if v == "number" else T["view_share"]) == "share"
    shown = 100 * types.div(complete["total"], axis=0) if as_share else types
    years_text = [str(year) for year in shown.index]
    value_format = "%{y:.1f} %" if as_share else "%{y:,.0f}"

    fig = go.Figure()
    if as_share:
        # Shares always add up to 100 %, so stacked bars would all have the same height, and in one
        # shared chart the small types disappear next to the propaganda offences. Therefore one small
        # chart per type, each with its own scale, so that the change of every type can be read.
        fig = make_subplots(rows=2, cols=4, subplot_titles=[T["types"][c] for c in types.columns],
                            horizontal_spacing=0.06, vertical_spacing=0.2)
        for k, (column, color) in enumerate(zip(types.columns, TYPE_COLORS)):
            row, col = k // 4 + 1, k % 4 + 1
            fig.add_scatter(x=years_text, y=shown[column], mode="lines+markers+text", showlegend=False,
                            line=dict(color=color, width=2.5), marker=dict(size=9),
                            text=[num(v, 1) for v in shown[column]], textposition="top center",
                            textfont=dict(size=11, color=INK), cliponaxis=False,
                            hovertemplate=f"{T['types'][column]}, %{{x}}: {value_format}<extra></extra>",
                            row=row, col=col)
            fig.update_yaxes(range=[0, 1.3 * shown[column].max()], row=row, col=col)
        fig = base_layout(fig, height=520)
        fig.update_layout(margin=dict(t=50))
        fig.update_xaxes(type="category", tickfont=dict(size=11))
        fig.update_yaxes(ticksuffix=" %", tickfont=dict(size=11), nticks=5)
        fig.update_annotations(font=dict(size=13, color=INK))
        show(fig)
        st.caption(T["share_note"])
    else:
        for column, color in zip(types.columns, TYPE_COLORS):
            fig.add_bar(x=years_text, y=shown[column], name=T["types"][column], marker_color=color,
                        marker_line=dict(color="white", width=1.5),
                        hovertemplate=f"{T['types'][column]}: {value_format}<extra></extra>")
        # Invisible trace: adds the total of the year to the hover box
        fig.add_scatter(x=years_text, y=shown.sum(axis=1), mode="markers", marker=dict(opacity=0), showlegend=False,
                        name=T["types"]["total"],
                        hovertemplate=f"<b>{T['types']['total']}: {value_format}</b><extra></extra>")
        # hovermode "x unified": one box with all types of the year, not only the segment under the mouse
        show(base_layout(fig, height=460, barmode="stack", hovermode="x unified", xaxis=dict(type="category"),
                         yaxis=dict(title=T["axis_offences"], tickformat=",")))
    st.caption(T["types_note"].format(years=", ".join(years_text)) + T["source_federal"])
    with st.expander(T["types_table"]):
        full_width(st.dataframe, federal.rename(columns=T["types"]).rename_axis(T["year"]))


# ---------------------------------------------------------------------------
# 6. Federal states 2022 to 2025
# ---------------------------------------------------------------------------

with tab_states:
    control = st.columns([1, 1, 2])
    year = control[0].select_slider(T["year"], options=STATE_YEARS, value=STATE_YEARS[-1], key="state_year")
    measure = control[1].radio(T["offences_filter"], list(MEASURES), key="state_measure",
                               format_func=lambda m: T["measures"][m])
    chosen_groups = control[2].multiselect(T["groups_filter"], list(STATE_GROUPS), default=list(STATE_GROUPS),
                                           key="state_groups", format_func=lambda g: T["groups"][g])
    count_column, rate_column, digits = MEASURES[measure]

    selected = states[(states["year"] == year) & states["group"].isin(chosen_groups)]
    if selected.empty:
        st.info(T["choose_group"])
    else:
        everything = states[states["year"] == year]
        germany_rate = 100_000 * everything[count_column].sum() / everything["population"].sum()
        top, bottom = selected.loc[selected[rate_column].idxmax()], selected.loc[selected[rate_column].idxmin()]

        tile = st.columns(4)
        tile[0].metric(T["tile_germany"].format(year=year), num(germany_rate, digits))
        tile[1].metric(f"{T['tile_highest']}: {state_name(top['state'])}", num(top[rate_column], digits))
        tile[2].metric(f"{T['tile_lowest']}: {state_name(bottom['state'])}", num(bottom[rate_column], digits))
        tile[3].metric(T["tile_ratio"], num(top[rate_column] / bottom[rate_column], 1))

        st.subheader(T["ranking_title"].format(measure=T["measures"][measure], year=year))
        ranking = selected.sort_values(rate_column)
        fig = go.Figure()
        for group in STATE_GROUPS:                       # colour follows the group, not the rank
            part = ranking[ranking["group"] == group]
            fig.add_bar(y=part["state"].map(state_name), x=part[rate_column], orientation="h", name=T["groups"][group],
                        marker_color=GROUP_COLORS[group], text=part[rate_column].map(lambda v: num(v, digits)),
                        textposition="outside", cliponaxis=False,
                        customdata=part[[count_column, "population"]],
                        hovertemplate=f"%{{y}}<br>%{{x:.{digits}f}} {T['hover_rate']}<br>"
                                      f"%{{customdata[0]:,.0f}} {T['hover_offences']}, "
                                      f"%{{customdata[1]:,.0f}} {T['hover_inhabitants']}<extra></extra>")
        fig.add_vline(x=germany_rate, line=dict(color=MUTED, dash="dot", width=1.5),
                      annotation_text=f"{T['germany']} {num(germany_rate, digits)}", annotation_position="bottom right")
        fig = base_layout(fig, height=max(260, 34 * len(ranking) + 90),
                          yaxis=dict(categoryorder="array", categoryarray=list(ranking["state"].map(state_name))),
                          xaxis=dict(title=T["axis_rate"]))
        fig.update_xaxes(showgrid=True, gridcolor=GRID)
        fig.update_yaxes(showgrid=False)
        show(fig)

        left, right = st.columns(2)
        with left:
            st.subheader(T["groups_title"])
            sums = states.groupby(["group", "year"])[[count_column, "population"]].sum()
            group_rate = (100_000 * sums[count_column] / sums["population"]).unstack("group")
            fig = go.Figure()
            for group in STATE_GROUPS:
                fig.add_scatter(x=group_rate.index, y=group_rate[group], mode="lines+markers", name=T["groups"][group],
                                line=dict(color=GROUP_COLORS[group], width=2), marker=dict(size=8),
                                hovertemplate=f"{T['groups'][group]}: %{{y:.{digits}f}}<extra></extra>")
            show(base_layout(fig, height=380, hovermode="x unified", xaxis=dict(dtick=1),
                             yaxis=dict(title=T["axis_rate_short"])))
        with right:
            st.subheader(T["share_title"].format(year=year))
            group_sum = everything.groupby("group")[[count_column, "population"]].sum().loc[list(STATE_GROUPS)]
            share = 100 * group_sum / group_sum.sum()
            fig = go.Figure()
            for group in STATE_GROUPS:
                values = [share.loc[group, count_column], share.loc[group, "population"]]
                fig.add_bar(y=[T["row_offences"], T["row_population"]], x=values,
                            orientation="h", name=T["groups"][group], marker_color=GROUP_COLORS[group],
                            marker_line=dict(color="white", width=2),
                            text=[num(v, 1) + PERCENT for v in values],
                            textposition="inside", insidetextanchor="middle", textfont=dict(color="white"),
                            hovertemplate=f"{T['groups'][group]}: %{{x:.1f}} %<extra></extra>")
            fig = base_layout(fig, height=380, barmode="stack", hovermode="y unified",
                              xaxis=dict(title=T["axis_share"], range=[0, 100]))
            fig.update_yaxes(showgrid=False)
            show(fig)

        st.subheader(T["all_years"])
        table = states[states["group"].isin(chosen_groups)].copy()
        table["order"] = table["group"].map(list(STATE_GROUPS).index)
        table[T["col_group"]] = table["group"].map(T["groups"])
        table[T["col_state"]] = table["state"].map(state_name)
        table = (table.pivot(index=["order", T["col_group"], T["col_state"]], columns="year", values=rate_column)
                 .sort_index(level="order").droplevel("order"))
        table.columns = [str(c) for c in table.columns]
        full_width(st.dataframe, table.style.background_gradient(cmap="Blues", axis=None)
                   .format(lambda v: num(v, digits)))
        st.caption(T["source_states"] + (T["counted_note"] if count_column == "violent" else ""))


# ---------------------------------------------------------------------------
# 7. AfD election results
# ---------------------------------------------------------------------------

def afd_chart(part, height, y_range=None):
    """AfD share in the six elections: one thin line, circles for federal and squares for European elections."""
    fig = go.Figure()
    fig.add_scatter(x=part["year"], y=part["afd_share_pct"], mode="lines", showlegend=False,
                    line=dict(color=ORANGE, width=1.5), hoverinfo="skip")
    for election, symbol in [("federal", "circle"), ("european", "square")]:
        sub = part[part["election"] == election]
        fig.add_scatter(x=sub["year"], y=sub["afd_share_pct"], mode="markers", name=T["elections"][election],
                        marker=dict(color=ORANGE, size=11, symbol=symbol, line=dict(color="white", width=2)),
                        hovertemplate=f"{T['elections'][election]} %{{x}}: %{{y:.2f}} %<extra></extra>")
    return base_layout(fig, height=height, xaxis=dict(dtick=1, range=[FIRST_YEAR - 0.6, LAST_YEAR + 0.6]),
                       yaxis=dict(title=T["axis_afd"], range=y_range))


with tab_afd:
    st.info(T["no_cause"])

    st.subheader(T["germany_time"])
    left, right = st.columns(2)
    with left:
        fig = go.Figure(go.Bar(x=federal.index, y=federal["total"], marker_color=BLUE,
                               hovertemplate=f"%{{x}}: %{{y:,.0f}} {T['hover_offences']}<extra></extra>"))
        show(base_layout(fig, height=360, xaxis=dict(dtick=1, range=[FIRST_YEAR - 0.6, LAST_YEAR + 0.6]),
                         yaxis=dict(title=T["axis_offences"], tickformat=",")))
    with right:
        show(afd_chart(afd[afd["state"] == "Germany"].sort_values("year"), 360))
    st.caption(T["source_federal"] + " " + T["source_elections"])

    st.subheader(T["states_scatter"])
    control = st.columns([2, 1])
    pair = control[0].selectbox(T["pair_filter"], list(ELECTION_PAIRS), key="pair", format_func=lambda p: T["pairs"][p])
    measure = control[1].radio(T["offences_filter"], list(MEASURES), key="afd_measure",
                               format_func=lambda m: T["measures"][m])
    election, year = ELECTION_PAIRS[pair]
    count_column, rate_column, digits = MEASURES[measure]

    votes = afd[(afd["election"] == election) & (afd["year"] == year) & (afd["state"] != "Germany")]
    data = votes[["state", "afd_share_pct"]].merge(states[states["year"] == year], on="state", validate="one_to_one")
    data["label"] = data["state"].map(state_name)

    def correlation(group=None):
        part = data if group is None else data[data["group"] == group]
        return num(part["afd_share_pct"].corr(part[rate_column]), 2)

    tile = st.columns(3)
    tile[0].metric(T["corr_all"], correlation())
    tile[1].metric(T["corr_east"], correlation("east"))
    tile[2].metric(T["corr_west"], correlation("west"))
    st.caption(T["corr_note"])

    # Axis ranges with room for the labels, then one position per label so that the names do not overlap
    x_low, x_high = data["afd_share_pct"].min(), data["afd_share_pct"].max()
    x_range = [x_low - 0.14 * (x_high - x_low), x_high + 0.14 * (x_high - x_low)]
    y_range = [0, 1.15 * data[rate_column].max()]
    data["position"] = label_positions(list(data["afd_share_pct"]), list(data[rate_column]), list(data["label"]),
                                       x_range, y_range)
    fig = go.Figure()
    for group in STATE_GROUPS:
        part = data[data["group"] == group]
        fig.add_scatter(x=part["afd_share_pct"], y=part[rate_column], mode="markers+text", name=T["groups"][group],
                        text=part["label"], textposition=list(part["position"]), textfont=dict(size=11, color=INK),
                        marker=dict(color=GROUP_COLORS[group], size=13, line=dict(color="white", width=2)),
                        customdata=part[[count_column]], cliponaxis=False,
                        hovertemplate=f"<b>%{{text}}</b><br>{T['hover_afd']}: %{{x:.2f}} %<br>"
                                      f"%{{y:.{digits}f}} {T['hover_rate']}<br>"
                                      f"%{{customdata[0]:,.0f}} {T['hover_offences']}<extra></extra>")
    fig = base_layout(fig, height=560,
                      xaxis=dict(title=T["axis_afd_pair"].format(election=T["elections"][election], year=year), range=x_range),
                      yaxis=dict(title=T["axis_rate_pair"].format(measure=T["measures"][measure], year=year), range=y_range))
    fig.update_xaxes(showgrid=True, gridcolor=GRID)
    show(fig)
    st.caption(T["source_states"] + " " + T["source_elections"] + T["second_votes"])

    st.subheader(T["one_state"])
    state = st.selectbox(T["state_filter"], [s for members in STATE_GROUPS.values() for s in members],
                         key="one_state", format_func=state_name)
    left, right = st.columns(2)
    with left:
        show(afd_chart(afd[afd["state"] == state].sort_values("year"), 340, y_range=[0, 45]))
    with right:
        part = states[states["state"] == state].sort_values("year")
        fig = go.Figure(go.Bar(x=part["year"], y=part["total_per_100k"], marker_color=BLUE,
                               text=part["total_per_100k"].map(lambda v: num(v, 1)), textposition="outside",
                               hovertemplate=f"%{{x}}: %{{y:.1f}} {T['hover_rate']}<extra></extra>"))
        show(base_layout(fig, height=340, xaxis=dict(dtick=1, range=[FIRST_YEAR - 0.6, LAST_YEAR + 0.6]),
                         yaxis=dict(title=T["axis_rate_short"], range=[0, 165])))
    st.caption(T["one_state_note"].format(state=state_name(state), group=T["groups"][GROUP_OF_STATE[state]]))


# ---------------------------------------------------------------------------
# 8. Data and limitations
# ---------------------------------------------------------------------------

with tab_data:
    st.subheader(T["limitations_title"])
    st.markdown(T["limitations"])

    st.subheader(T["sources_title"])
    st.markdown(T["sources_crime"])
    pick = (0, 2) if LANG == "en" else (1, 3)
    full_width(st.dataframe, pd.DataFrame([(row[pick[0]], row[pick[1]], row[4], row[5]) for row in CRIME_SOURCES],
                                          columns=T["sources_crime_cols"]), hide_index=True)
    st.markdown(T["sources_elections"])
    full_width(st.dataframe, pd.DataFrame([(row[pick[0]], row[pick[1]], row[4]) for row in ELECTION_SOURCES],
                                          columns=T["sources_elections_cols"]), hide_index=True)
    st.markdown(T["sources_rest"])

    st.subheader(T["data_title"])
    files = [(federal_long, "pmk_right_federal.csv"), (states.drop(columns=["group", "total_rate", "violent_rate"]), "pmk_right_states.csv"),
             (afd, "afd_results.csv")]
    for title, (table, file_name) in zip(T["data_tables"], files):
        with st.expander(title):
            full_width(st.dataframe, table, hide_index=True)
            st.download_button(T["download"], table.to_csv(index=False).encode("utf-8"), file_name, "text/csv",
                               key=f"download_{file_name}")


# ---------------------------------------------------------------------------
# 9. Rights
# ---------------------------------------------------------------------------

st.divider()
st.caption(f"**{T['copyright']}** {T['rights']}")
