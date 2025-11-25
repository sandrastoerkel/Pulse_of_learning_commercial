"""
Questionnaire Builder für Coaching-Diagnostik

Baut Fragebögen aus PISA-Skalen zusammen:
1. Lädt Items für gewählte Skalen
2. Lädt Fragetexte (Deutsch)
3. Lädt Value Labels (Antwortoptionen)
4. Bereitet Daten für HTML-Generator vor
"""

import pandas as pd
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from utils.json_item_loader import get_scale_items, get_fragestamm
from utils.db_loader import get_db_connection, load_value_labels, load_question_text

# Paths to manual scale definitions
MANUAL_SCALES_PATHS = [
    Path(__file__).parent.parent / 'data' / 'skalen_infos' / 'parent_support_scales.json',
    Path(__file__).parent.parent / 'data' / 'skalen_infos' / 'general_efficacy_scale.json'
]


def load_manual_scale(scale_name: str) -> Tuple[Optional[List[Dict]], Optional[Dict[str, pd.DataFrame]], Optional[str]]:
    """
    Lädt eine manuell definierte Skala aus JSON-Definitionsdateien

    Prüft in dieser Reihenfolge:
    1. parent_support_scales.json (Eltern-Unterstützung)
    2. general_efficacy_scale.json (Fächerübergreifende Selbstwirksamkeit)

    Args:
        scale_name: Skalen-Code (z.B. 'EMOSUPS', 'PERFEED', 'GENEFF')

    Returns:
        Tuple mit:
        - items: List[Dict] oder None
        - value_labels: Dict[str, pd.DataFrame] oder None
        - fragestamm: str oder None
    """
    # Try each manual scales file
    for manual_scales_path in MANUAL_SCALES_PATHS:
        if not manual_scales_path.exists():
            continue

        try:
            with open(manual_scales_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            if scale_name not in data.get('scales', {}):
                continue

            scale_data = data['scales'][scale_name]

            # Build items list
            items = []
            for item_data in scale_data.get('items', []):
                item = {
                    'variable_name': item_data['id'],
                    'question_text_de': item_data.get('text_de', ''),
                    'question_text_en': item_data.get('text_en', ''),
                    'scale': scale_name
                }
                items.append(item)

            # Build value labels DataFrame for all items
            response_scale = scale_data.get('response_scale', {})
            value_labels_dict = {}

            for item in items:
                # Create DataFrame with value labels
                values = []
                labels_de = []
                labels_en = []

                for value, label_de in response_scale.items():
                    values.append(value)
                    labels_de.append(label_de)
                    labels_en.append(label_de)  # Use German as fallback for English

                labels_df = pd.DataFrame({
                    'value': values,
                    'label': labels_de,  # English fallback
                    'label_de': labels_de,
                    'is_missing_code': [0] * len(values)
                })

                value_labels_dict[item['variable_name']] = labels_df

            # Get fragestamm if available
            fragestamm = scale_data.get('fragestamm', None)

            return items, value_labels_dict, fragestamm

        except Exception as e:
            print(f"⚠️  Fehler beim Laden der manuellen Skala {scale_name} aus {manual_scales_path.name}: {e}")
            continue

    # No manual scale found in any file
    return None, None, None


def load_items_for_scales(scale_names: List[str]) -> Tuple[List[Dict], Dict[str, pd.DataFrame], Dict[str, str], List[str]]:
    """
    Lädt alle Items, Fragetexte und Value Labels für eine Liste von Skalen

    Args:
        scale_names: Liste von Skalen-Codes (z.B. ['MATHEFF', 'ANXMAT', 'BELONG'])

    Returns:
        Tuple mit:
        - items: List[Dict] - Liste aller Items mit question_text_de
        - value_labels: Dict[str, pd.DataFrame] - Value Labels pro Variable
        - fragestamm: Dict[str, str] - Fragestämme pro Skala (falls vorhanden)
        - skipped_scales: List[str] - Skalen ohne Items (übersprungen)

    Example:
        >>> items, labels, stems, skipped = load_items_for_scales(['MATHEFF', 'ANXMAT'])
        >>> print(f"Geladen: {len(items)} Items aus {len(stems)} Skalen")
        >>> if skipped:
        >>>     print(f"Übersprungen: {', '.join(skipped)}")
    """
    # Replace HOMEPOS with HOMEPOS_SHORT (9 items instead of 26)
    scale_names = [
        'HOMEPOS_SHORT' if scale == 'HOMEPOS' else scale
        for scale in scale_names
    ]

    conn = get_db_connection()

    all_items = []
    value_labels_dict = {}
    fragestamm_dict = {}
    skipped_scales = []

    for scale_name in scale_names:
        # 0. Try to load from manual definitions first
        manual_items, manual_labels, manual_fragestamm = load_manual_scale(scale_name)

        if manual_items is not None:
            # Manual scale found - use it directly
            all_items.extend(manual_items)
            if manual_labels:
                value_labels_dict.update(manual_labels)
            if manual_fragestamm:
                fragestamm_dict[scale_name] = manual_fragestamm
            continue

        # 1. Lade Items aus JSON (fallback if not manual)
        items = get_scale_items(scale_name)

        if not items:
            print(f"⚠️  Keine Items für Skala {scale_name} in JSON gefunden (übersprungen)")
            skipped_scales.append(scale_name)
            continue

        # 2. Lade Fragestamm (falls vorhanden)
        fragestamm = get_fragestamm(scale_name)
        if fragestamm:
            fragestamm_dict[scale_name] = fragestamm

        # 3. Für jedes Item: Lade detaillierte Infos aus DB
        for item in items:
            variable_name = item['variable_name']

            # Lade Fragetext aus DB (falls vorhanden, überschreibt JSON)
            question_data = load_question_text(conn, variable_name)

            if question_data is not None and not question_data.empty:
                # Nutze DB-Text nur wenn nicht None/leer (präziser als JSON)
                db_text_de = question_data.get('question_text_de')
                db_text_en = question_data.get('question_text_en')

                if db_text_de is not None and db_text_de != '':
                    item['question_text_de'] = db_text_de
                if db_text_en is not None and db_text_en != '':
                    item['question_text_en'] = db_text_en

            # Lade Value Labels
            value_labels = load_value_labels(conn, variable_name)

            if not value_labels.empty:
                value_labels_dict[variable_name] = value_labels
            else:
                print(f"⚠️  Keine Value Labels für {variable_name}")

            # Füge Skalen-Info hinzu
            item['scale'] = scale_name

            all_items.append(item)

    conn.close()

    return all_items, value_labels_dict, fragestamm_dict


def estimate_questionnaire_duration(num_items: int) -> int:
    """
    Schätzt die Dauer zum Ausfüllen eines Fragebogens

    Args:
        num_items: Anzahl der Fragen

    Returns:
        int: Geschätzte Dauer in Minuten

    Formula:
        - Basis: 20 Sekunden pro Frage
        - Plus: 2 Minuten Setup/Einleitung
        - Aufgerundet auf nächste 5 Minuten
    """
    # 20 Sekunden pro Frage
    seconds_per_item = 20
    total_seconds = (num_items * seconds_per_item) + 120  # +2 Min Setup

    minutes = total_seconds / 60

    # Aufrunden auf nächste 5 Minuten
    rounded_minutes = int(((minutes + 4) // 5) * 5)

    return max(5, rounded_minutes)  # Mindestens 5 Minuten


def get_items_summary(items: List[Dict]) -> Dict:
    """
    Erstellt eine Zusammenfassung der geladenen Items

    Args:
        items: Liste von Items (aus load_items_for_scales)

    Returns:
        Dict mit Statistiken

    Example:
        >>> summary = get_items_summary(items)
        >>> print(f"{summary['total_items']} Fragen aus {summary['num_scales']} Skalen")
    """
    scales = set(item.get('scale', 'Unknown') for item in items)

    items_per_scale = {}
    for item in items:
        scale = item.get('scale', 'Unknown')
        if scale not in items_per_scale:
            items_per_scale[scale] = 0
        items_per_scale[scale] += 1

    return {
        'total_items': len(items),
        'num_scales': len(scales),
        'scales': list(scales),
        'items_per_scale': items_per_scale,
        'estimated_duration': estimate_questionnaire_duration(len(items))
    }


def validate_questionnaire_data(items: List[Dict], value_labels: Dict[str, pd.DataFrame]) -> Dict:
    """
    Validiert, ob alle notwendigen Daten für den Fragebogen vorhanden sind

    Args:
        items: Liste von Items
        value_labels: Value Labels Dictionary

    Returns:
        Dict mit Validierungs-Ergebnissen

    Example:
        >>> validation = validate_questionnaire_data(items, labels)
        >>> if validation['is_valid']:
        >>>     print("✅ Fragebogen kann erstellt werden")
    """
    issues = []
    warnings = []

    if not items:
        issues.append("Keine Items vorhanden")
        return {
            'is_valid': False,
            'issues': issues,
            'warnings': warnings
        }

    # Prüfe jedes Item
    for idx, item in enumerate(items):
        variable_name = item.get('variable_name')

        # 1. Variable Name vorhanden?
        if not variable_name:
            issues.append(f"Item {idx + 1}: Kein variable_name")
            continue

        # 2. Fragetext vorhanden?
        question_text = item.get('question_text_de') or item.get('question_text_en')
        if not question_text:
            issues.append(f"Item {variable_name}: Kein Fragetext")

        # 3. Value Labels vorhanden?
        if variable_name not in value_labels:
            issues.append(f"Item {variable_name}: Keine Value Labels")
        else:
            # 4. Mindestens 2 Antwortoptionen?
            labels_df = value_labels[variable_name]
            non_missing = labels_df[labels_df['is_missing_code'] == 0]

            if len(non_missing) < 2:
                warnings.append(f"Item {variable_name}: Nur {len(non_missing)} Antwortoptionen")

    is_valid = len(issues) == 0

    return {
        'is_valid': is_valid,
        'issues': issues,
        'warnings': warnings,
        'total_items': len(items),
        'items_with_labels': sum(1 for item in items if item.get('variable_name') in value_labels)
    }


def group_items_by_scale(items: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Gruppiert Items nach Skala

    Args:
        items: Liste von Items

    Returns:
        Dict mit Skalen-Namen als Keys und Item-Listen als Values

    Example:
        >>> grouped = group_items_by_scale(items)
        >>> for scale, scale_items in grouped.items():
        >>>     print(f"{scale}: {len(scale_items)} Items")
    """
    grouped = {}

    for item in items:
        scale = item.get('scale', 'Unknown')

        if scale not in grouped:
            grouped[scale] = []

        grouped[scale].append(item)

    return grouped
