"""
📚 Ressourcen - Videos & Tipps zur Verbesserung

Diese Seite zeigt Content (Videos, Tipps, Materialien) für einen bestimmten Faktor.
Der Faktor wird über st.session_state.selected_factor oder URL-Parameter übergeben.

Basiert auf:
- streamlit-player für YouTube-Embeds
- Best Practices aus GitHub Education Apps
"""

import streamlit as st
import json
from pathlib import Path
import sys
sys.path.append('..')

from utils.scale_info import get_scale_info
from utils.evidence_integration import get_evidence, get_hattie_info, get_pisa_info

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Ressourcen & Tipps",
    page_icon="📚",
    layout="wide"
)

# ============================================
# TRY TO IMPORT STREAMLIT-PLAYER (optional)
# ============================================

try:
    from streamlit_player import st_player
    HAS_PLAYER = True
except ImportError:
    HAS_PLAYER = False

# ============================================
# CONTENT DATABASE (inline für Standalone)
# ============================================

CONTENT_DATABASE = {
    "MATHEFF": {
        "name_de": "Selbstwirksamkeit aufbauen",
        "name_schueler": "Wie du dir mehr zutraust",
        "icon": "💪",
        "color": "#667eea",
        
        "intro_text": """
        **Selbstwirksamkeit** bedeutet: Glaubst du, dass du schwierige Aufgaben schaffen kannst?
        
        Die gute Nachricht: Das lässt sich trainieren! Schüler, die sich mehr zutrauen, 
        erreichen bessere Noten - nicht weil sie schlauer sind, sondern weil sie dranbleiben.
        """,
        
        "videos": [
            {
                "id": "CiPhJj7fDX4",
                "title": "Sich alles merken - Gehirn-gerecht lernen",
                "creator": "Vera F. Birkenbihl",
                "duration_min": 12,
                "url": "https://www.youtube.com/watch?v=CiPhJj7fDX4",
                
                "score": 8.7,
                "views": "917.000+",
                
                "warum_hilft": """
                Dieses Video zeigt dir eine Lernmethode, die wirklich funktioniert. 
                
                Ein Schüler schrieb in den Kommentaren:
                > "Ich habe die Klasse wiederholen müssen, aber jetzt läuft es eins a. 
                > Die Lehrer fragten, wie ich mich so verbessert habe."
                
                Wenn du merkst, dass Lernen funktioniert, wächst dein Selbstvertrauen automatisch!
                """,
                
                "kernbotschaft": "Statt passiv abzuschreiben → eigene Gedanken aktivieren. Das Gehirn lernt besser, wenn DU denkst!",
                
                "validated": True
            }
        ],
        
        "tipps": [
            {
                "titel": "🏆 Das Erfolgs-Tagebuch",
                "beschreibung": """
                Schreibe **jeden Abend 3 Dinge** auf, die du heute geschafft hast - egal wie klein.
                
                Beispiele:
                - "Ich habe eine schwierige Aufgabe zu Ende gebracht"
                - "Ich habe im Unterricht eine Frage gestellt"
                - "Ich habe 20 Minuten geübt"
                
                Nach einer Woche wirst du sehen: Du schaffst mehr als du denkst!
                """,
                "dauer": "5 Min/Tag",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🔄 Die 'Noch nicht'-Methode",
                "beschreibung": """
                Ersetze **"Ich kann das nicht"** durch **"Ich kann das NOCH nicht"**.
                
                Dieser kleine Unterschied verändert, wie dein Gehirn über Lernen denkt:
                - "Ich kann das nicht" = Ende, keine Hoffnung
                - "Ich kann das NOCH nicht" = Ich bin auf dem Weg
                
                Probier es aus - es funktioniert wirklich!
                """,
                "dauer": "Sofort",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "📈 Kleine Schritte, große Wirkung",
                "beschreibung": """
                Starte mit Aufgaben, die du **SICHER schaffst**. 
                
                Warum? Jeder kleine Erfolg:
                1. Gibt dir ein gutes Gefühl
                2. Stärkt dein Selbstvertrauen
                3. Macht die nächste Aufgabe leichter
                
                Erst wenn du merkst "Das klappt!", gehst du zum nächsten Level.
                """,
                "dauer": "Täglich",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            }
        ],
        
        "wissenschaft": {
            "hattie_d": 0.92,
            "hattie_rank": 3,
            "pisa_impact": "+42 Punkte",
            "erklaerung": """
            **Warum ist Selbstwirksamkeit SO wichtig?**
            
            - **Hattie-Forschung**: Effektstärke d = 0.92 (Rang #3 von 252 Faktoren!)
            - **PISA 2022**: Erklärt 40-54% der Unterschiede in Mathe-Noten
            - **Das bedeutet**: +42 PISA-Punkte = mehr als 1 Schuljahr Vorsprung!
            
            Es ist der **stärkste veränderbare Faktor** für deinen Schulerfolg.
            """
        }
    },
    
    "ANXMAT": {
        "name_de": "Mathe-Angst reduzieren",
        "name_schueler": "Weniger Stress bei Mathe",
        "icon": "🧘",
        "color": "#4ecdc4",
        
        "intro_text": """
        **Mathe-Angst** ist weit verbreitet - und hat NICHTS mit Intelligenz zu tun!
        
        Sie entsteht durch negative Erfahrungen und lässt sich abbauen. 
        Viele sehr schlaue Menschen haben Mathe-Angst - das Problem ist nicht dein Gehirn, 
        sondern die Angst, die es blockiert.
        """,
        
        "videos": [],  # Noch keine Videos analysiert
        
        "tipps": [
            {
                "titel": "🌬️ Die 3-Atemzüge-Technik",
                "beschreibung": """
                **Bevor du eine Mathe-Aufgabe anfängst:**
                
                1. **Einatmen** (4 Sekunden)
                2. **Halten** (4 Sekunden)  
                3. **Ausatmen** (6 Sekunden)
                
                Wiederhole 3x. Das beruhigt dein Nervensystem **sofort** und 
                macht Platz im Kopf für klares Denken.
                """,
                "dauer": "30 Sekunden",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "✅ Fang mit dem Leichten an",
                "beschreibung": """
                **Bei Klassenarbeiten:**
                
                1. Lies ALLE Aufgaben durch
                2. Löse ZUERST die, die du sicher kannst
                3. Dann die mittelschweren
                4. Zum Schluss die schwierigen
                
                Warum? Die ersten Erfolge geben dir **Sicherheit** für den Rest!
                """,
                "dauer": "Bei jeder Arbeit",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🗣️ Angst benennen",
                "beschreibung": """
                Wenn du merkst, dass Angst aufkommt, sage dir:
                
                **"Ich bin gerade nervös, und das ist okay."**
                
                Klingt einfach, funktioniert aber! Studien zeigen: 
                Gefühle **benennen** reduziert ihre Intensität um bis zu 50%.
                """,
                "dauer": "Sofort",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "📝 Positive Mathe-Momente sammeln",
                "beschreibung": """
                Schreibe auf, wenn du etwas in Mathe **verstanden** oder **richtig gelöst** hast.
                
                Diese Sammlung zeigt dir: **Du KANNST Mathe!**
                
                Dein Gehirn merkt sich negative Erfahrungen besser als positive - 
                diese Liste gleicht das aus.
                """,
                "dauer": "Bei jedem Erfolg",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            }
        ],
        
        "wissenschaft": {
            "hattie_d": 0.42,
            "hattie_rank": 56,
            "pisa_impact": "-35 Punkte bei hoher Angst",
            "erklaerung": """
            **Warum blockiert Angst das Lernen?**
            
            - Angst aktiviert den "Kampf oder Flucht"-Modus
            - Das **Arbeitsgedächtnis** wird blockiert
            - Du vergisst Dinge, die du eigentlich weißt!
            
            **PISA 2022**: Schüler mit hoher Mathe-Angst erreichen **-35 Punkte** weniger.
            
            Die gute Nachricht: Weniger Angst = mehr Kapazität zum Denken!
            """
        }
    },
    
    "GROSAGR": {
        "name_de": "Growth Mindset entwickeln",
        "name_schueler": "Glauben, dass du wachsen kannst",
        "icon": "🌱",
        "color": "#00cc88",
        
        "intro_text": """
        **Growth Mindset** bedeutet: Du glaubst, dass deine Fähigkeiten wachsen können - wie ein Muskel!
        
        Menschen mit Growth Mindset lernen schneller, weil sie Fehler als **Lernchancen** sehen, 
        nicht als Beweis für mangelndes Talent.
        """,
        
        "videos": [],  # Carol Dweck Video noch analysieren
        
        "tipps": [
            {
                "titel": "✨ Das magische Wort: NOCH",
                "beschreibung": """
                Füge **"noch"** zu negativen Sätzen hinzu:
                
                - ❌ "Ich kann das nicht" → ✅ "Ich kann das **NOCH** nicht"
                - ❌ "Ich verstehe das nicht" → ✅ "Ich verstehe das **NOCH** nicht"
                - ❌ "Das ist zu schwer für mich" → ✅ "Das ist **NOCH** zu schwer"
                
                Dieses eine Wort verändert, wie dein Gehirn über Lernen denkt!
                """,
                "dauer": "Sofort",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🎉 Fehler feiern",
                "beschreibung": """
                Jeder Fehler zeigt dir, was du **noch lernen kannst**.
                
                Statt dich zu ärgern, frage dich:
                - "Was kann ich aus diesem Fehler lernen?"
                - "Was würde ich nächstes Mal anders machen?"
                
                Die erfolgreichsten Menschen machen die meisten Fehler - 
                weil sie am meisten ausprobieren!
                """,
                "dauer": "Bei jedem Fehler",
                "schwierigkeit": "mittel",
                "sofort_umsetzbar": True
            },
            {
                "titel": "💪 Anstrengung loben",
                "beschreibung": """
                Sage dir selbst:
                
                - ✅ "Ich habe mich **angestrengt**"
                - ❌ Nicht: "Ich bin schlau"
                
                Warum? **Anstrengung** kannst du kontrollieren - "Schlausein" nicht.
                
                Wenn du Anstrengung wertschätzt, versuchst du mehr.
                Wenn du nur Talent wertschätzt, gibst du bei Schwierigkeiten auf.
                """,
                "dauer": "Täglich",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            }
        ],
        
        "wissenschaft": {
            "hattie_d": 0.64,
            "hattie_rank": 28,
            "pisa_impact": "+31 Punkte Lesen, +23 Punkte Mathe",
            "erklaerung": """
            **Was sagt die Forschung?**
            
            - **Carol Dweck** (Stanford): Erfinderin des Growth Mindset Konzepts
            - **Hattie**: d = 0.64 (hoher Einfluss)
            - **PISA 2022**: +31 Punkte beim Lesen, +23 Punkte in Mathe
            
            Schüler mit Growth Mindset verbessern sich schneller - 
            weil sie an **Wachstum** glauben!
            """
        }
    },
    
    "PERSEVAGR": {
        "name_de": "Durchhaltevermögen stärken",
        "name_schueler": "Länger dranbleiben können",
        "icon": "🏃",
        "color": "#ff9800",
        
        "intro_text": """
        **Ausdauer** ist wie ein Muskel - je mehr du sie trainierst, desto stärker wird sie!
        
        Die erfolgreichsten Menschen sind nicht die Schlauesten, sondern die, 
        die am **längsten dranbleiben**.
        """,
        
        "videos": [],
        
        "tipps": [
            {
                "titel": "⏱️ Die 5-Minuten-Regel",
                "beschreibung": """
                Wenn du aufgeben willst: **Versuche es noch 5 Minuten.**
                
                Warum funktioniert das?
                - Oft kommt der Durchbruch kurz vor dem Aufgeben
                - Du trainierst dein Gehirn, weiterzumachen
                - 5 Minuten sind kurz genug, um es zu versuchen
                
                Wenn du nach 5 Min immer noch nicht weiterkommst? Dann hast du es wenigstens versucht!
                """,
                "dauer": "5 Min extra",
                "schwierigkeit": "mittel",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🧩 Große Aufgaben zerteilen",
                "beschreibung": """
                Eine riesige Aufgabe wirkt **unmöglich**.
                
                Teile sie in **kleine Schritte**:
                1. Was ist der ERSTE kleine Schritt?
                2. Nur diesen einen Schritt machen
                3. Dann den nächsten
                
                Plötzlich ist die "unmögliche" Aufgabe machbar!
                """,
                "dauer": "Vor jeder großen Aufgabe",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🍅 Pomodoro-Technik",
                "beschreibung": """
                **25 Minuten arbeiten, 5 Minuten Pause.**
                
                So geht's:
                1. Timer auf 25 Min stellen
                2. Konzentriert arbeiten (keine Ablenkung!)
                3. Nach 25 Min: 5 Min Pause
                4. Nach 4 Runden: 15-30 Min Pause
                
                Das macht Dranbleiben **viel einfacher**!
                """,
                "dauer": "25+5 Min Zyklen",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            }
        ],
        
        "wissenschaft": {
            "hattie_d": 0.77,
            "hattie_rank": 15,
            "pisa_impact": "+28 Punkte",
            "erklaerung": """
            **Die Wissenschaft sagt:**
            
            - **Hattie**: d = 0.77 (einer der stärksten Faktoren!)
            - **PISA 2022**: +28 Punkte
            
            **"Grit"** (Ausdauer + Leidenschaft) ist laut Angela Duckworth 
            wichtiger für Erfolg als IQ oder Talent.
            
            Ausdauer schlägt Talent - die, die dranbleiben, gewinnen am Ende!
            """
        }
    },
    
    "TEACHSUP": {
        "name_de": "Lehrer-Unterstützung nutzen",
        "name_schueler": "Besser mit Lehrern klarkommen",
        "icon": "👨‍🏫",
        "color": "#9c27b0",
        "intro_text": "Eine gute Beziehung zu deinen Lehrern macht Lernen einfacher.",
        "videos": [],
        "tipps": [
            {
                "titel": "❓ Eine Frage pro Stunde",
                "beschreibung": "Nimm dir vor, in mindestens einer Stunde pro Tag eine Frage zu stellen. Je öfter du fragst, desto normaler wird es!",
                "dauer": "Im Unterricht",
                "schwierigkeit": "mittel",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🙋 Nach der Stunde fragen",
                "beschreibung": "Wenn du dich im Unterricht nicht traust: Geh nach der Stunde zum Lehrer. Die meisten freuen sich über interessierte Schüler!",
                "dauer": "Nach dem Unterricht",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            }
        ],
        "wissenschaft": {"hattie_d": 0.72, "hattie_rank": 18, "pisa_impact": "+25 Punkte", "erklaerung": "Gute Lehrer-Schüler-Beziehungen sind einer der stärksten Faktoren für Lernerfolg!"}
    },
    
    "BELONG": {
        "name_de": "Sich zugehörig fühlen",
        "name_schueler": "Dich in der Schule wohlfühlen",
        "icon": "🏠",
        "color": "#e91e63",
        "intro_text": "Wenn du dich in der Schule wohlfühlst und Freunde hast, lernst du automatisch besser.",
        "videos": [],
        "tipps": [
            {
                "titel": "👋 Eine neue Person ansprechen",
                "beschreibung": "Sprich diese Woche mit jemandem in deiner Klasse, mit dem du noch nicht viel geredet hast. Ein einfaches 'Hey, wie fandest du die Hausaufgabe?' reicht!",
                "dauer": "Diese Woche",
                "schwierigkeit": "mittel",
                "sofort_umsetzbar": True
            },
            {
                "titel": "🎯 Einer AG beitreten",
                "beschreibung": "AGs, Sportgruppen oder Musik-Ensembles sind perfekt, um Gleichgesinnte zu finden. Was interessiert dich?",
                "dauer": "Dieses Halbjahr",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": False
            }
        ],
        "wissenschaft": {"hattie_d": 0.52, "hattie_rank": 42, "pisa_impact": "+18 Punkte", "erklaerung": "Wer sich zugehörig fühlt, geht lieber zur Schule - und lernt dadurch mehr!"}
    },
    
    "BULLIED": {
        "name_de": "Umgang mit Mobbing",
        "name_schueler": "Wenn andere dich fertig machen",
        "icon": "🛡️",
        "color": "#f44336",
        "intro_text": "Mobbing ist NICHT deine Schuld. Hier findest du Tipps, wie du damit umgehen kannst.",
        "videos": [],
        "tipps": [
            {
                "titel": "🗣️ Sprich mit jemandem",
                "beschreibung": "Such dir einen Erwachsenen, dem du vertraust: Eltern, Lehrer, Schulpsychologe. Du musst das nicht alleine durchstehen!",
                "dauer": "Diese Woche",
                "schwierigkeit": "mittel",
                "sofort_umsetzbar": True
            },
            {
                "titel": "📝 Dokumentiere es",
                "beschreibung": "Schreibe auf, was passiert: Wann, wo, wer, was. Das hilft, wenn du mit Erwachsenen sprichst.",
                "dauer": "Bei jedem Vorfall",
                "schwierigkeit": "leicht",
                "sofort_umsetzbar": True
            }
        ],
        "wissenschaft": {"hattie_d": -0.33, "hattie_rank": 242, "pisa_impact": "-40 Punkte", "erklaerung": "Mobbing schadet der Leistung stark. Aber: Hilfe suchen ist der erste Schritt zur Besserung!"}
    }
}

# ============================================
# HELPER FUNCTIONS
# ============================================

def embed_youtube(video_id: str, title: str = ""):
    """Bettet YouTube-Video ein"""
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    if HAS_PLAYER:
        st_player(url)
    else:
        # st.video unterstützt YouTube direkt
        st.video(url)

def render_video_section(videos: list, color: str):
    """Rendert die Video-Sektion"""
    
    if not videos:
        st.info("🎬 Videos für diesen Bereich werden gerade analysiert. Schau bald wieder vorbei!")
        return
    
    validated_videos = [v for v in videos if v.get('validated', False)]
    
    if not validated_videos:
        st.info("🎬 Videos für diesen Bereich werden gerade analysiert. Schau bald wieder vorbei!")
        return
    
    for video in validated_videos:
        st.markdown(f"""
        <div style="background: white; border-radius: 15px; padding: 5px; 
                    margin: 15px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    border-left: 5px solid {color};">
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Video einbetten
            embed_youtube(video['id'], video.get('title', ''))
        
        with col2:
            st.markdown(f"### {video.get('title', 'Video')}")
            st.markdown(f"**{video.get('creator', '')}** · {video.get('duration_min', '?')} Min")
            
            if video.get('views'):
                st.markdown(f"👁️ {video.get('views')} Views")
            if video.get('score'):
                st.success(f"⭐ **Validierungs-Score: {video.get('score')}/10**")
            
            st.markdown("---")
            
            if video.get('kernbotschaft'):
                st.info(f"**💡 Kernbotschaft:** {video.get('kernbotschaft')}")
        
        # Warum hilft dieses Video?
        if video.get('warum_hilft'):
            with st.expander("🎯 Warum hilft dir dieses Video?", expanded=False):
                st.markdown(video.get('warum_hilft'))
        
        st.markdown("---")

def render_tipps_section(tipps: list, color: str):
    """Rendert die Tipps-Sektion"""
    
    if not tipps:
        st.info("💡 Tipps für diesen Bereich werden gerade zusammengestellt.")
        return
    
    # Sortiere: Sofort umsetzbar und leicht zuerst
    sofort = [t for t in tipps if t.get('sofort_umsetzbar', False) and t.get('schwierigkeit') == 'leicht']
    spaeter = [t for t in tipps if t not in sofort]
    
    if sofort:
        st.markdown("### ⚡ Sofort umsetzbar")
        for tipp in sofort:
            with st.expander(f"{tipp.get('titel', 'Tipp')} · ⏱️ {tipp.get('dauer', '')}", expanded=False):
                st.markdown(tipp.get('beschreibung', ''))
    
    if spaeter:
        st.markdown("### 📅 Mit etwas Übung")
        for tipp in spaeter:
            with st.expander(f"{tipp.get('titel', 'Tipp')} · ⏱️ {tipp.get('dauer', '')}", expanded=False):
                st.markdown(tipp.get('beschreibung', ''))

def render_wissenschaft_section(wissenschaft: dict, color: str):
    """Rendert die Wissenschafts-Sektion"""
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        d = wissenschaft.get('hattie_d', 0)
        if d >= 0.8:
            delta = "Sehr hoch!"
        elif d >= 0.6:
            delta = "Hoch"
        elif d >= 0.4:
            delta = "Überdurchschnittlich"
        else:
            delta = None
        st.metric("Hattie-Effektstärke", f"d = {d}", delta)
    
    with col2:
        st.metric("Hattie-Rang", f"#{wissenschaft.get('hattie_rank', '?')} / 252")
    
    with col3:
        st.metric("PISA-Einfluss", wissenschaft.get('pisa_impact', '?'))
    
    if wissenschaft.get('erklaerung'):
        st.markdown("---")
        st.markdown(wissenschaft.get('erklaerung'))

# ============================================
# MAIN APP
# ============================================

# URL-Parameter oder Session State
query_params = st.query_params
factor_from_url = query_params.get('factor', None)

if factor_from_url and factor_from_url in CONTENT_DATABASE:
    st.session_state.selected_factor = factor_from_url
elif 'selected_factor' not in st.session_state or st.session_state.selected_factor not in CONTENT_DATABASE:
    st.session_state.selected_factor = 'MATHEFF'  # Default

# Sidebar: Faktor-Auswahl
st.sidebar.header("📚 Bereich wählen")

factor_options = {
    content.get('name_schueler', key): key 
    for key, content in CONTENT_DATABASE.items()
}

# Finde aktuellen Index
current_factor = st.session_state.selected_factor
try:
    current_index = list(factor_options.values()).index(current_factor)
except ValueError:
    current_index = 0

selected_display = st.sidebar.selectbox(
    "Wähle einen Bereich:",
    options=list(factor_options.keys()),
    index=current_index
)

st.session_state.selected_factor = factor_options[selected_display]
factor = st.session_state.selected_factor

# Hole Content
content = CONTENT_DATABASE.get(factor, {})
if not content:
    st.error("Bereich nicht gefunden.")
    st.stop()

# ============================================
# HEADER
# ============================================

icon = content.get('icon', '📚')
name = content.get('name_de', factor)
color = content.get('color', '#667eea')

st.markdown(f"""
<div style="background: linear-gradient(135deg, {color} 0%, {color}aa 100%); 
            color: white; padding: 40px; border-radius: 20px; margin-bottom: 30px;">
    <h1 style="margin: 0; font-size: 2.5em;">{icon} {name}</h1>
</div>
""", unsafe_allow_html=True)

# Intro Text
st.markdown(content.get('intro_text', ''))

st.divider()

# ============================================
# TABS
# ============================================

tab1, tab2, tab3 = st.tabs(["🎬 Videos", "💡 Tipps & Übungen", "🔬 Wissenschaft"])

with tab1:
    st.header("🎬 Empfohlene Videos")
    st.markdown("Diese Videos wurden wissenschaftlich analysiert und helfen nachweislich bei diesem Thema.")
    render_video_section(content.get('videos', []), color)

with tab2:
    st.header("💡 Tipps & Übungen")
    st.markdown("Konkrete Strategien, die du sofort anwenden kannst.")
    render_tipps_section(content.get('tipps', []), color)

with tab3:
    st.header("🔬 Was sagt die Wissenschaft?")
    render_wissenschaft_section(content.get('wissenschaft', {}), color)

# ============================================
# FOOTER
# ============================================

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("⬅️ Zurück zur Auswertung", use_container_width=True):
        st.switch_page("pages/4_📊_Auswertung.py")

with col2:
    st.markdown("""
    <div style="text-align: right; color: #888; font-size: 14px; padding-top: 8px;">
        💡 Tipp: Fang mit EINEM Video oder EINEM Tipp an!
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIDEBAR INFO
# ============================================

st.sidebar.divider()

wissenschaft = content.get('wissenschaft', {})
st.sidebar.markdown(f"""
### {icon} Kurzinfo

| | |
|---|---|
| **Hattie d** | {wissenschaft.get('hattie_d', '?')} |
| **Rang** | #{wissenschaft.get('hattie_rank', '?')} |
| **PISA** | {wissenschaft.get('pisa_impact', '?')} |
""")

st.sidebar.divider()

# Quick Links zu anderen Bereichen
st.sidebar.markdown("### 🔗 Andere Bereiche")
for key, val in CONTENT_DATABASE.items():
    if key != factor:
        btn_icon = val.get('icon', '📚')
        btn_name = val.get('name_schueler', key)[:25]
        if st.sidebar.button(f"{btn_icon} {btn_name}", key=f"nav_{key}", use_container_width=True):
            st.session_state.selected_factor = key
            st.rerun()
