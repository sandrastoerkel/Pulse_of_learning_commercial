"""
Deutsche Label-Mappings für PISA-Skalen

Stellt deutsche Übersetzungen für alle Antwortoptionen bereit,
da die PISA-Datenbank nur englische Labels enthält.
"""

import pandas as pd
from typing import Dict

# Deutsche Label-Mappings für verschiedene Skalen-Typen
GERMAN_LABELS = {
    # Selbstwirksamkeit (Self-efficacy) - 4-Punkt Likert
    'efficacy': {
        1: 'Überhaupt nicht zuversichtlich',
        2: 'Nicht sehr zuversichtlich',
        3: 'Zuversichtlich',
        4: 'Sehr zuversichtlich'
    },

    # Zustimmung (Agreement) - 4-Punkt Likert
    'agreement': {
        1: 'Stimme überhaupt nicht zu',
        2: 'Stimme eher nicht zu',
        3: 'Stimme eher zu',
        4: 'Stimme völlig zu'
    },

    # Häufigkeit (Frequency) - 4-Punkt Likert
    'frequency': {
        1: 'Nie oder fast nie',
        2: 'Manchmal',
        3: 'Häufig',
        4: 'Immer oder fast immer'
    },

    # Häufigkeit erweitert - 5-Punkt (für PARINVOL)
    'frequency_extended': {
        1: 'Nie oder fast nie',
        2: 'Ein- oder zweimal im Jahr',
        3: 'Ein- oder zweimal im Monat',
        4: 'Ein- oder zweimal in der Woche',
        5: 'Jeden Tag oder fast jeden Tag'
    },

    # Ja/Nein
    'yesno': {
        1: 'Ja',
        2: 'Nein'
    }
}

# Mapping: Skalen-Code → Label-Typ
SCALE_LABEL_TYPES = {
    # Selbstwirksamkeit
    'GENEFF': 'efficacy',   # General Academic Self-Efficacy
    'MATHEFF': 'efficacy',
    'MATHEF21': 'efficacy',

    # Angst / Zustimmung
    'ANXMAT': 'agreement',
    'PERSEVAGR': 'agreement',
    'GROSAGR': 'agreement',
    'TEACHSUP': 'agreement',
    'BELONG': 'agreement',
    'MATHPERS': 'agreement',
    'RELATST': 'agreement',
    'DISCLIM': 'agreement',
    'COOPAGR': 'agreement',
    'CURIOAGR': 'agreement',
    'EMPATAGR': 'agreement',
    'STRESAGR': 'agreement',

    # Häufigkeit
    'BULLIED': 'frequency',

    # Default
    '_default': 'agreement'
}


def get_german_labels_for_scale(scale_code: str, original_labels_df: pd.DataFrame) -> pd.DataFrame:
    """
    Ergänzt oder ersetzt fehlende deutsche Labels mit passenden Übersetzungen

    Args:
        scale_code: Skalen-Code (z.B. 'MATHEFF', 'ANXMAT')
        original_labels_df: DataFrame mit vorhandenen Labels

    Returns:
        DataFrame mit ergänzten deutschen Labels
    """
    # Determine label type for this scale
    label_type = SCALE_LABEL_TYPES.get(scale_code, SCALE_LABEL_TYPES['_default'])
    german_mapping = GERMAN_LABELS[label_type]

    # Create copy
    labels_df = original_labels_df.copy()

    # Create list for new label_de values
    new_label_de = []

    # Add or replace label_de for each value
    for idx, row in labels_df.iterrows():
        value = row['value']

        # Skip missing codes
        val_str = str(value)
        if val_str.startswith('.') or val_str == 'SYSTEM MISSING':
            new_label_de.append(row.get('label_de'))
            continue

        # Get German label from mapping
        # Convert value to integer for lookup (DataFrame has strings, mapping has integers)
        try:
            value_int = int(value)
            if value_int in german_mapping:
                new_label_de.append(german_mapping[value_int])
            else:
                # Keep existing if not in mapping
                new_label_de.append(row.get('label_de'))
        except (ValueError, TypeError):
            # If conversion fails, keep existing
            new_label_de.append(row.get('label_de'))

    # Update the column
    labels_df['label_de'] = new_label_de

    return labels_df


def add_german_labels_to_value_labels(value_labels_dict: Dict[str, pd.DataFrame],
                                      items: list) -> Dict[str, pd.DataFrame]:
    """
    Fügt deutschen Labels für alle Items hinzu

    Args:
        value_labels_dict: Dictionary mit value labels pro Variable
        items: Liste von Items mit scale-Informationen

    Returns:
        Aktualisiertes Dictionary mit deutschen Labels
    """
    # Create mapping: variable_name → scale_code
    var_to_scale = {item['variable_name']: item['scale'] for item in items}

    # Update each value label
    updated_dict = {}
    for var_name, labels_df in value_labels_dict.items():
        scale_code = var_to_scale.get(var_name, '_default')
        updated_dict[var_name] = get_german_labels_for_scale(scale_code, labels_df)

    return updated_dict


# Example usage
if __name__ == "__main__":
    # Test
    test_df = pd.DataFrame({
        'value': [1, 2, 3, 4],
        'label_de': [None, None, None, None],
        'is_missing_code': [0, 0, 0, 0]
    })

    print("Test: MATHEFF Labels")
    result = get_german_labels_for_scale('MATHEFF', test_df)
    for idx, row in result.iterrows():
        print(f"  {row['value']}: {row['label_de']}")

    print("\nTest: ANXMAT Labels")
    result = get_german_labels_for_scale('ANXMAT', test_df)
    for idx, row in result.iterrows():
        print(f"  {row['value']}: {row['label_de']}")
