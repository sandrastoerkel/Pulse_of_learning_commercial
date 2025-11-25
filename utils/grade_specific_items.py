"""
Grade-Specific Items Module
Passt Fragebögen und Interventionen an die Klassenstufe an
"""

import re
from typing import Tuple, List, Dict, Optional
import pandas as pd

def extract_grade_from_class(class_string: str) -> Optional[int]:
    """
    Extrahiert die Klassenstufe aus einem Klassen-String
    
    Args:
        class_string: z.B. "7a", "10b", "Q11", "11. Klasse"
        
    Returns:
        Klassenstufe als Integer oder None
    """
    if not class_string:
        return None
        
    # Remove whitespace
    class_string = class_string.strip()
    
    # Pattern matching for different formats
    patterns = [
        r'^(\d+)[a-zA-Z]*$',  # 7a, 10b, etc.
        r'^[QqKk]?(\d+)$',     # Q11, K12, etc.
        r'^(\d+)\.',           # 11. Klasse
        r'(\d+)\.?\s*[Kk]lasse'  # 11 Klasse, 11. Klasse
    ]
    
    for pattern in patterns:
        match = re.match(pattern, class_string)
        if match:
            grade = int(match.group(1))
            # Validate reasonable grade range
            if 1 <= grade <= 13:
                return grade
    
    return None

def adapt_matheff_for_grade(grade: int, original_items: List[Dict]) -> Tuple[List[Dict], Dict, str]:
    """
    Passt MATHEFF-Items an die Klassenstufe an
    
    Args:
        grade: Klassenstufe (5-13)
        original_items: Original MATHEFF items
        
    Returns:
        Tuple: (adapted_items, value_labels, fragestamm)
    """
    
    # Grade-specific MATHEFF adaptations
    grade_adaptations = {
        5: {
            'fragestamm': 'Wie gut kannst du diese Mathe-Aufgaben lösen?',
            'items': [
                ('MATHEFF_Q01', 'Einfache Plus- und Minus-Aufgaben im Kopf rechnen'),
                ('MATHEFF_Q02', 'Das kleine Einmaleins anwenden'),
                ('MATHEFF_Q03', 'Textaufgaben verstehen und lösen'),
                ('MATHEFF_Q04', 'Mit dem Geodreieck arbeiten'),
                ('MATHEFF_Q05', 'Einfache Brüche verstehen'),
                ('MATHEFF_Q06', 'Säulendiagramme lesen'),
                ('MATHEFF_Q07', 'Längen und Gewichte umrechnen'),
                ('MATHEFF_Q08', 'Einfache geometrische Formen erkennen')
            ]
        },
        6: {
            'fragestamm': 'Wie sicher fühlst du dich bei diesen Aufgaben?',
            'items': [
                ('MATHEFF_Q01', 'Brüche addieren und subtrahieren'),
                ('MATHEFF_Q02', 'Dezimalzahlen multiplizieren'),
                ('MATHEFF_Q03', 'Prozentaufgaben lösen'),
                ('MATHEFF_Q04', 'Winkel messen und zeichnen'),
                ('MATHEFF_Q05', 'Flächeninhalte berechnen'),
                ('MATHEFF_Q06', 'Einfache Gleichungen lösen'),
                ('MATHEFF_Q07', 'Koordinatensystem verwenden'),
                ('MATHEFF_Q08', 'Mittelwerte berechnen')
            ]
        },
        7: {
            'fragestamm': 'Wie gut kannst du folgende Aufgaben bewältigen?',
            'items': [
                ('MATHEFF_Q01', 'Terme vereinfachen'),
                ('MATHEFF_Q02', 'Proportionale Zuordnungen erkennen'),
                ('MATHEFF_Q03', 'Negative Zahlen verwenden'),
                ('MATHEFF_Q04', 'Dreisatz anwenden'),
                ('MATHEFF_Q05', 'Konstruktionen mit Zirkel und Lineal'),
                ('MATHEFF_Q06', 'Prozent- und Zinsrechnung'),
                ('MATHEFF_Q07', 'Einfache Wahrscheinlichkeiten berechnen'),
                ('MATHEFF_Q08', 'Gleichungen mit einer Unbekannten lösen')
            ]
        },
        8: {
            'fragestamm': 'Wie zuversichtlich bist du bei diesen mathematischen Aufgaben?',
            'items': [
                ('MATHEFF_Q01', 'Lineare Funktionen verstehen und zeichnen'),
                ('MATHEFF_Q02', 'Binomische Formeln anwenden'),
                ('MATHEFF_Q03', 'Pythagoras-Satz verwenden'),
                ('MATHEFF_Q04', 'Gleichungssysteme lösen'),
                ('MATHEFF_Q05', 'Körper berechnen (Volumen, Oberfläche)'),
                ('MATHEFF_Q06', 'Quadratische Gleichungen lösen'),
                ('MATHEFF_Q07', 'Statistische Daten auswerten'),
                ('MATHEFF_Q08', 'Prozentuale Veränderungen berechnen')
            ]
        },
        9: {
            'fragestamm': 'Wie sicher fühlst du dich bei folgenden Themen?',
            'items': [
                ('MATHEFF_Q01', 'Quadratische Funktionen analysieren'),
                ('MATHEFF_Q02', 'Trigonometrie im rechtwinkligen Dreieck'),
                ('MATHEFF_Q03', 'Potenzen und Wurzeln berechnen'),
                ('MATHEFF_Q04', 'Ähnlichkeit und Strahlensätze'),
                ('MATHEFF_Q05', 'Exponentialfunktionen verstehen'),
                ('MATHEFF_Q06', 'Wahrscheinlichkeitsrechnung'),
                ('MATHEFF_Q07', 'Körperberechnungen (Kegel, Pyramide)'),
                ('MATHEFF_Q08', 'Algebraische Umformungen')
            ]
        },
        10: {
            'fragestamm': 'Wie gut beherrschst du diese mathematischen Konzepte?',
            'items': [
                ('MATHEFF_Q01', 'Trigonometrische Funktionen'),
                ('MATHEFF_Q02', 'Logarithmen anwenden'),
                ('MATHEFF_Q03', 'Vektoren im Raum'),
                ('MATHEFF_Q04', 'Ableitungen berechnen'),
                ('MATHEFF_Q05', 'Stochastik und Kombinatorik'),
                ('MATHEFF_Q06', 'Grenzwerte verstehen'),
                ('MATHEFF_Q07', 'Funktionsscharen untersuchen'),
                ('MATHEFF_Q08', 'Beweise führen')
            ]
        },
        11: {
            'fragestamm': 'Wie sicher bist du in der Analysis?',
            'items': [
                ('MATHEFF_Q01', 'Differentialrechnung anwenden'),
                ('MATHEFF_Q02', 'Kurvendiskussion durchführen'),
                ('MATHEFF_Q03', 'Integrale berechnen'),
                ('MATHEFF_Q04', 'Extremwertprobleme lösen'),
                ('MATHEFF_Q05', 'e-Funktionen und ln-Funktionen'),
                ('MATHEFF_Q06', 'Rotationskörper berechnen'),
                ('MATHEFF_Q07', 'Funktionsgleichungen aufstellen'),
                ('MATHEFF_Q08', 'Wendepunkte bestimmen')
            ]
        },
        12: {
            'fragestamm': 'Wie kompetent fühlst du dich bei diesen Abiturthemen?',
            'items': [
                ('MATHEFF_Q01', 'Analytische Geometrie im Raum'),
                ('MATHEFF_Q02', 'Lineare Algebra (Matrizen)'),
                ('MATHEFF_Q03', 'Normalverteilung anwenden'),
                ('MATHEFF_Q04', 'Hypothesentests durchführen'),
                ('MATHEFF_Q05', 'Vektorräume verstehen'),
                ('MATHEFF_Q06', 'Differentialgleichungen lösen'),
                ('MATHEFF_Q07', 'Bedingte Wahrscheinlichkeit'),
                ('MATHEFF_Q08', 'Komplexe Modellierungsaufgaben')
            ]
        }
    }
    
    # Default to grade 8 if not in range
    if grade < 5:
        grade = 5
    elif grade > 12:
        grade = 12
    elif grade not in grade_adaptations:
        # Use closest grade
        grade = 8
    
    adaptation = grade_adaptations[grade]
    
    # Create adapted items
    adapted_items = []
    for item_id, item_text in adaptation['items']:
        adapted_items.append({
            'variable_name': item_id,
            'question_text_de': item_text,
            'scale': 'MATHEFF'
        })
    
    # Create value labels (same for all grades)
    value_labels = {}
    likert_labels = {
        '1': 'Gar nicht sicher',
        '2': 'Nicht sehr sicher',
        '3': 'Ziemlich sicher',
        '4': 'Sehr sicher'
    }

    for item in adapted_items:
        # Create DataFrame to match expected format
        value_labels[item['variable_name']] = pd.DataFrame({
            'value': list(likert_labels.keys()),
            'label_de': list(likert_labels.values()),
            'is_missing_code': [0] * len(likert_labels)
        })

    return adapted_items, value_labels, adaptation['fragestamm']

def get_grade_specific_interventions(grade: int) -> Dict:
    """
    Gibt klassenspezifische Interventionsanpassungen zurück
    
    Args:
        grade: Klassenstufe
        
    Returns:
        Dictionary mit Anpassungen
    """
    
    if grade <= 6:
        return {
            'focus': 'Spielerisches Lernen, viele Erfolgserlebnisse, kurze Einheiten',
            'duration_factor': 0.75,
            'special_considerations': [
                'Konkrete Materialien verwenden',
                'Bewegungspausen einbauen',
                'Peer-Learning mit Spielelementen',
                'Elterneinbindung wichtig'
            ]
        }
    elif grade <= 8:
        return {
            'focus': 'Peer-Learning, Autonomie fördern, Identitätsfindung unterstützen',
            'duration_factor': 1.0,
            'special_considerations': [
                'Gruppendynamik beachten',
                'Coolness-Faktor berücksichtigen',
                'Digitale Medien einbeziehen',
                'Pubertät berücksichtigen'
            ]
        }
    elif grade <= 10:
        return {
            'focus': 'Prüfungsvorbereitung, Zukunftsperspektiven, Selbstverantwortung',
            'duration_factor': 1.0,
            'special_considerations': [
                'Berufsorientierung einbeziehen',
                'Prüfungsangst thematisieren',
                'Zeitmanagement trainieren',
                'Eigenverantwortung stärken'
            ]
        }
    else:  # 11-13
        return {
            'focus': 'Selbstregulation, Stressmanagement, Eigenständigkeit',
            'duration_factor': 0.8,
            'special_considerations': [
                'Abitur-Stress berücksichtigen',
                'Selbstständiges Lernen',
                'Work-Life-Balance',
                'Zukunftsängste ernst nehmen'
            ]
        }

def adapt_intervention_duration(base_weeks: str, grade: int) -> str:
    """
    Passt Interventionsdauer an Klassenstufe an
    
    Args:
        base_weeks: z.B. "4-6"
        grade: Klassenstufe
        
    Returns:
        Angepasste Dauer
    """
    grade_info = get_grade_specific_interventions(grade)
    factor = grade_info['duration_factor']
    
    # Parse base weeks
    if '-' in base_weeks:
        parts = base_weeks.split('-')
        try:
            min_weeks = int(parts[0])
            max_weeks = int(parts[1].split()[0])  # Remove "Wochen" if present
            
            # Apply factor
            min_weeks = max(2, int(min_weeks * factor))
            max_weeks = max(min_weeks + 1, int(max_weeks * factor))
            
            return f"{min_weeks}-{max_weeks}"
        except:
            return base_weeks
    
    return base_weeks

def get_age_appropriate_language(text: str, grade: int) -> str:
    """
    Passt Sprache an Altersstufe an
    
    Args:
        text: Original-Text
        grade: Klassenstufe
        
    Returns:
        Angepasster Text
    """
    if grade <= 6:
        # Vereinfachte Sprache für jüngere Schüler
        replacements = {
            'Selbstwirksamkeit': 'Selbstvertrauen',
            'kognitiv': 'gedanklich',
            'Metakognition': 'Nachdenken über das Lernen',
            'intrinsisch': 'aus eigenem Antrieb',
            'extrinsisch': 'von außen motiviert'
        }
    elif grade <= 8:
        # Jugendgerechte Sprache
        replacements = {
            'evidenzbasiert': 'wissenschaftlich bewiesen',
            'Intervention': 'Unterstützung',
            'Implementation': 'Umsetzung'
        }
    else:
        # Keine Anpassung für ältere Schüler
        return text
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text
