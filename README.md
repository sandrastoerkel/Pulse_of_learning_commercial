# 🎓 Pulse of Learning - Lerncoaching-Plattform

Evidenzbasierte Lerndiagnostik und individualisierte Förderplanung auf Basis von **PISA 2022**.

## 📊 Über das Projekt

Diese Streamlit-Anwendung kombiniert wissenschaftliche PISA-Forschung mit praktischer Lernförderung. Sie ermöglicht:

- ✅ **Standardisierte Diagnostik** mit validierten PISA-Instrumenten
- ✅ **PISA-Benchmark-Vergleiche** (N=6.116 deutsche Schüler)
- ✅ **Evidenzbasierte Interventionen** nach Hattie, Bandura, Dweck
- ✅ **Individuelle Förderplanung** mit konkreten Maßnahmen

## 🚀 Schnellstart

### 1. Installation

```bash
# Repository klonen
git clone https://github.com/sandrastoerkel/Pulse_of_Learning_Commercial.git
cd Pulse_of_Learning_Commercial

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
source venv/bin/activate  # macOS/Linux
# oder
venv\Scripts\activate  # Windows

# Dependencies installieren
pip install -r requirements.txt
```

### 2. App starten

```bash
streamlit run Home.py
```

Die App öffnet sich automatisch im Browser unter `http://localhost:8501`

## 📁 Projektstruktur

```
Pulse_of_learning_commercial/
├── Home.py                          # Hauptseite
├── pages/
│   ├── 1_📖_PISA_Forschungsgrundlage.py   # Wissenschaftliche Grundlagen
│   ├── 2_🎓_Elternakademie.py              # Informationsmaterial
│   ├── 3_🔍_Screening_Diagnostik.py        # Schüler-Screening
│   ├── 4_📊_Auswertung.py                  # Ergebnisdarstellung
│   └── 5_📚_Ressourcen.py                  # Fördermaßnahmen
├── utils/
│   ├── coaching_db.py                # Datenbank-Management
│   ├── scale_info.py                 # PISA-Skalen-Info
│   ├── questionnaire_builder.py      # Fragebogen-Generator
│   ├── german_labels.py              # Deutsche Übersetzungen
│   ├── grade_specific_items.py       # Klassenstufen-Anpassung
│   ├── evidence_integration.py       # Hattie-Integration
│   ├── json_item_loader.py           # JSON-Daten laden
│   └── db_loader.py                  # PISA-DB Zugriff
├── data/
│   └── skalen_infos/
│       ├── pisa_skalen.json          # PISA-Skalen-Definitionen
│       ├── pisa_indizes_erweitert.json
│       ├── parent_support_scales.json
│       └── general_efficacy_scale.json
├── pisa_2022_germany.db              # PISA 2022 Datenbank (6.116 Schüler)
├── coaching.db                       # Schüler-Datenbank (wird automatisch erstellt)
├── requirements.txt                  # Python-Dependencies
└── README.md                         # Diese Datei
```

## 🎯 Anwendungsfälle

### Für Lehrkräfte
- Identifizieren Sie Stärken und Förderbedarf Ihrer Schüler
- Nutzen Sie standardisierte PISA-Instrumente
- Erhalten Sie evidenzbasierte Handlungsempfehlungen

### Für Lerncoaches
- Professionelle Diagnostik mit wissenschaftlich validierten Skalen
- Individuelle Förderplanung basierend auf Schülerprofilen
- Tracking von Lernfortschritten über Zeit

### Für Schulleitungen
- Datenbasierte Schulentwicklung
- Identifikation von Risikogruppen
- Monitoring von Interventionserfolgen

### Für Eltern
- Verstehen Sie die Lernsituation Ihres Kindes
- Erhalten Sie konkrete Tipps für die Unterstützung zuhause
- Vergleich mit PISA-Benchmarks

## 📊 Screening-Levels

Die App bietet 3 Diagnostik-Levels:

| Level | Dauer | Skalen | Einsatz |
|-------|-------|---------|---------|
| **Level 1**: Schnell-Screening | 15 Min | 4 Kern-Skalen | Erstes Screening, Monitoring |
| **Level 2**: Standard-Screening | 30 Min | 7 Skalen | Standard-Diagnostik |
| **Level 3**: Umfassende Diagnostik | 45 Min | 10 Skalen | Tiefendiagnostik |

### Erfasste Konstrukte:
- ✅ **Selbstwirksamkeit** (MATHEFF, GENEFF)
- ✅ **Mathe-Angst** (ANXMAT)
- ✅ **Ausdauer** (PERSEVAGR)
- ✅ **Zugehörigkeitsgefühl** (BELONG)
- ✅ **Lehrerunterstützung** (TEACHSUP)
- ✅ **Mobbing-Erfahrungen** (BULLIED)
- ✅ **Eltern-Unterstützung** (EMOSUPS, PARINVOL)

## 🔬 Wissenschaftliche Fundierung

### Datengrundlage
- **PISA 2022 Deutschland**: 6.116 Schüler (9. Klasse)
- **OECD-Standard**: Weltweit vergleichbare Instrumente
- **IRT-Skalierung**: Item Response Theory für präzise Messung

### Validierte Skalen
Alle Skalen haben:
- ✅ **Cronbach's α > 0.70** (hohe Reliabilität)
- ✅ **Konstruktvalidität** empirisch belegt
- ✅ **Internationale Vergleichbarkeit** (80+ Länder)

### Evidenzbasierte Interventionen
Empfehlungen basieren auf:
- **Hattie's Visible Learning** (Effect Sizes)
- **Bandura's Selbstwirksamkeitstheorie** (1997)
- **Dweck's Growth Mindset** (2006)
- **Beck's kognitive Verhaltenstherapie** (1979)

## 🛠️ Technische Details

### Anforderungen
- **Python**: 3.8+
- **Streamlit**: 1.30.0+
- **Pandas**: 2.0.0+
- **Plotly**: 5.17.0+

### Datenbanken
- **SQLite3**: Keine externe DB nötig
- **coaching.db**: Schüler-Daten (wird automatisch erstellt)
- **pisa_2022_germany.db**: PISA-Referenzdaten (inkludiert)

### Features
- 🔒 **Datenschutz**: Lokale Speicherung, keine Cloud
- 📱 **Responsive**: Funktioniert auf Desktop & Tablet
- 🎨 **Interaktiv**: Plotly-Charts, Expander, Tabs
- 💾 **Export**: Excel-Reports, CSV-Downloads

## 📖 Dokumentation

### Erste Schritte
1. **PISA-Forschungsgrundlage lesen** (Seite 1)
2. **Schüler anlegen** (Seite 3)
3. **Screening durchführen** (Seite 3)
4. **Ergebnisse analysieren** (Seite 4)
5. **Maßnahmen umsetzen** (Seite 5)

### Navigation
Nutzen Sie die **Sidebar** (links) zur Navigation zwischen Seiten.

### Session State
Die App nutzt Streamlit Session State für:
- `screening_student_id`: Aktuell ausgewählter Schüler
- `screening_responses`: Fragebogen-Antworten
- `selected_factor`: Für Ressourcen-Navigation

## 🤝 Mitwirken

Dieses Projekt ist Teil der PISA-Forschung zur Lernförderung.

### Feedback & Issues
Bitte nutzen Sie GitHub Issues für:
- 🐛 Bug Reports
- 💡 Feature Requests
- 📝 Dokumentations-Verbesserungen

## 📜 Lizenz

© 2025 Sandra Störkel. Alle Rechte vorbehalten.

**Hinweis**: PISA® ist eine eingetragene Marke der OECD.

## 📧 Kontakt

- **E-Mail**: info@pulseoflearning.de
- **GitHub**: [@sandrastoerkel](https://github.com/sandrastoerkel)
- **Repository**: [Pulse_of_Learning_Commercial](https://github.com/sandrastoerkel/Pulse_of_Learning_Commercial)

## 🙏 Danksagungen

- **OECD** für PISA-Daten und Instrumente
- **Streamlit** für das großartige Framework
- **Hattie, Bandura, Dweck** für wissenschaftliche Grundlagen

---

**Viel Erfolg beim Einsatz evidenzbasierter Lernförderung!** 🎓📊✨
