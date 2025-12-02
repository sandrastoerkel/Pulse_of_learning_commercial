"""
🗄️ Motivation Challenge Database Layer
=======================================

SQLite-Datenbankfunktionen für das Motivation-Challenge-System.
Basiert auf der Selbstbestimmungstheorie (SDT) von Deci & Ryan.

Tabellen:
- motivation_challenges: Challenge-Fortschritt pro User
- motivation_sdt_progress: SDT-Level (Autonomie, Kompetenz, Verbundenheit)
- motivation_streaks: Streak-Tracking mit Freeze-Option

Inspiriert von:
- GitHub: Contribution Graph, keine Leaderboards
- Duolingo: Streaks mit Freeze, XP-System
- Khan Academy: Mastery Levels, geheime Badges
- Brilliant: Bite-sized Challenges, Instant Feedback
"""

import sqlite3
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Any, Tuple
import json


# ============================================
# TABELLEN INITIALISIERUNG
# ============================================

def init_motivation_tables(conn: sqlite3.Connection) -> None:
    """
    Initialisiert alle Motivation-Challenge Tabellen.
    Idempotent - kann mehrfach aufgerufen werden.
    """
    c = conn.cursor()
    
    # ─────────────────────────────────────────
    # Tabelle 1: Challenge-Fortschritt
    # ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            challenge_id TEXT NOT NULL,
            age_group TEXT NOT NULL,
            grundbeduerfnis TEXT NOT NULL,
            phase TEXT DEFAULT 'intro',
            user_input TEXT,
            reflection TEXT,
            rating INTEGER,
            xp_earned INTEGER DEFAULT 0,
            completed BOOLEAN DEFAULT 0,
            completed_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # ─────────────────────────────────────────
    # Tabelle 2: SDT-Progress (Skill-Tree Levels)
    # ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_sdt_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            autonomie_level INTEGER DEFAULT 0,
            autonomie_xp INTEGER DEFAULT 0,
            kompetenz_level INTEGER DEFAULT 0,
            kompetenz_xp INTEGER DEFAULT 0,
            verbundenheit_level INTEGER DEFAULT 0,
            verbundenheit_xp INTEGER DEFAULT 0,
            total_challenges INTEGER DEFAULT 0,
            total_xp INTEGER DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # ─────────────────────────────────────────
    # Tabelle 3: Streak-Tracking
    # ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_streaks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL UNIQUE,
            current_streak INTEGER DEFAULT 0,
            longest_streak INTEGER DEFAULT 0,
            last_activity_date DATE,
            freeze_available INTEGER DEFAULT 1,
            freeze_used_date DATE,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # ─────────────────────────────────────────
    # Tabelle 4: Aktivitäts-Log (für Heatmap)
    # ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            activity_date DATE NOT NULL,
            challenge_id TEXT NOT NULL,
            grundbeduerfnis TEXT NOT NULL,
            xp_earned INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # ─────────────────────────────────────────
    # Tabelle 5: Earned Badges
    # ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            badge_id TEXT NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            UNIQUE(user_id, badge_id),
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # ─────────────────────────────────────────
    # Tabelle 6: Zertifikate
    # ─────────────────────────────────────────
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            certificate_type TEXT NOT NULL,
            age_group TEXT NOT NULL,
            challenges_completed TEXT,
            total_xp INTEGER DEFAULT 0,
            issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # ─────────────────────────────────────────
    # Indizes für Performance
    # ─────────────────────────────────────────
    c.execute('CREATE INDEX IF NOT EXISTS idx_mot_challenges_user ON motivation_challenges(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_mot_challenges_id ON motivation_challenges(challenge_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_mot_activity_user ON motivation_activity_log(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_mot_activity_date ON motivation_activity_log(activity_date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_mot_badges_user ON motivation_badges(user_id)')
    
    conn.commit()


# ============================================
# CHALLENGE CRUD OPERATIONEN
# ============================================

def save_challenge_progress(
    conn: sqlite3.Connection,
    user_id: str,
    challenge_id: str,
    age_group: str,
    grundbeduerfnis: str,
    phase: str = "intro",
    user_input: str = None,
    reflection: str = None,
    rating: int = None,
    xp_earned: int = 0,
    completed: bool = False
) -> int:
    """
    Speichert oder aktualisiert den Challenge-Fortschritt.
    
    Returns:
        int: ID des Eintrags
    """
    c = conn.cursor()
    
    # Prüfen ob schon ein Eintrag existiert
    c.execute('''
        SELECT id FROM motivation_challenges 
        WHERE user_id = ? AND challenge_id = ? AND age_group = ?
        ORDER BY created_at DESC LIMIT 1
    ''', (user_id, challenge_id, age_group))
    
    existing = c.fetchone()
    
    if existing and not completed:
        # Update existierenden Eintrag (noch nicht abgeschlossen)
        c.execute('''
            UPDATE motivation_challenges 
            SET phase = ?, user_input = ?, reflection = ?, rating = ?,
                xp_earned = ?, completed = ?, completed_at = ?
            WHERE id = ?
        ''', (
            phase, user_input, reflection, rating, xp_earned,
            completed, datetime.now().isoformat() if completed else None,
            existing[0]
        ))
        entry_id = existing[0]
    else:
        # Neuer Eintrag (oder Wiederholung nach Abschluss)
        c.execute('''
            INSERT INTO motivation_challenges 
            (user_id, challenge_id, age_group, grundbeduerfnis, phase, 
             user_input, reflection, rating, xp_earned, completed, completed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id, challenge_id, age_group, grundbeduerfnis, phase,
            user_input, reflection, rating, xp_earned, completed,
            datetime.now().isoformat() if completed else None
        ))
        entry_id = c.lastrowid
    
    conn.commit()
    return entry_id


def get_challenge_progress(
    conn: sqlite3.Connection,
    user_id: str,
    challenge_id: str,
    age_group: str
) -> Optional[Dict[str, Any]]:
    """
    Holt den aktuellen Fortschritt einer Challenge.
    """
    c = conn.cursor()
    c.execute('''
        SELECT id, phase, user_input, reflection, rating, xp_earned, completed, completed_at
        FROM motivation_challenges 
        WHERE user_id = ? AND challenge_id = ? AND age_group = ?
        ORDER BY created_at DESC LIMIT 1
    ''', (user_id, challenge_id, age_group))
    
    row = c.fetchone()
    if row:
        return {
            "id": row[0],
            "phase": row[1],
            "user_input": row[2],
            "reflection": row[3],
            "rating": row[4],
            "xp_earned": row[5],
            "completed": bool(row[6]),
            "completed_at": row[7]
        }
    return None


def get_completed_challenges(
    conn: sqlite3.Connection,
    user_id: str,
    age_group: str = None,
    grundbeduerfnis: str = None
) -> List[Dict[str, Any]]:
    """
    Holt alle abgeschlossenen Challenges eines Users.
    Optional gefiltert nach Altersstufe und/oder Grundbedürfnis.
    """
    c = conn.cursor()
    
    query = '''
        SELECT DISTINCT challenge_id, age_group, grundbeduerfnis, 
               xp_earned, completed_at, rating
        FROM motivation_challenges 
        WHERE user_id = ? AND completed = 1
    '''
    params = [user_id]
    
    if age_group:
        query += ' AND age_group = ?'
        params.append(age_group)
    
    if grundbeduerfnis:
        query += ' AND grundbeduerfnis = ?'
        params.append(grundbeduerfnis)
    
    query += ' ORDER BY completed_at DESC'
    
    c.execute(query, params)
    
    return [{
        "challenge_id": row[0],
        "age_group": row[1],
        "grundbeduerfnis": row[2],
        "xp_earned": row[3],
        "completed_at": row[4],
        "rating": row[5]
    } for row in c.fetchall()]


def count_completed_challenges(
    conn: sqlite3.Connection,
    user_id: str,
    age_group: str = None,
    grundbeduerfnis: str = None
) -> int:
    """Zählt abgeschlossene Challenges."""
    c = conn.cursor()
    
    query = '''
        SELECT COUNT(DISTINCT challenge_id) 
        FROM motivation_challenges 
        WHERE user_id = ? AND completed = 1
    '''
    params = [user_id]
    
    if age_group:
        query += ' AND age_group = ?'
        params.append(age_group)
    
    if grundbeduerfnis:
        query += ' AND grundbeduerfnis = ?'
        params.append(grundbeduerfnis)
    
    c.execute(query, params)
    return c.fetchone()[0]


# ============================================
# SDT PROGRESS (Skill-Tree)
# ============================================

def get_or_create_sdt_progress(
    conn: sqlite3.Connection,
    user_id: str
) -> Dict[str, Any]:
    """
    Holt oder erstellt den SDT-Progress eines Users.
    """
    c = conn.cursor()
    
    c.execute('''
        SELECT autonomie_level, autonomie_xp, kompetenz_level, kompetenz_xp,
               verbundenheit_level, verbundenheit_xp, total_challenges, total_xp
        FROM motivation_sdt_progress WHERE user_id = ?
    ''', (user_id,))
    
    row = c.fetchone()
    
    if row:
        return {
            "autonomie_level": row[0],
            "autonomie_xp": row[1],
            "kompetenz_level": row[2],
            "kompetenz_xp": row[3],
            "verbundenheit_level": row[4],
            "verbundenheit_xp": row[5],
            "total_challenges": row[6],
            "total_xp": row[7]
        }
    else:
        # Neuen Eintrag erstellen
        c.execute('''
            INSERT INTO motivation_sdt_progress (user_id) VALUES (?)
        ''', (user_id,))
        conn.commit()
        
        return {
            "autonomie_level": 0,
            "autonomie_xp": 0,
            "kompetenz_level": 0,
            "kompetenz_xp": 0,
            "verbundenheit_level": 0,
            "verbundenheit_xp": 0,
            "total_challenges": 0,
            "total_xp": 0
        }


def update_sdt_progress(
    conn: sqlite3.Connection,
    user_id: str,
    grundbeduerfnis: str,
    xp_earned: int
) -> Dict[str, Any]:
    """
    Aktualisiert den SDT-Progress nach Abschluss einer Challenge.
    
    Level-Schwellen (Khan Academy Style):
    - Level 1: 100 XP
    - Level 2: 250 XP
    - Level 3: 500 XP
    - Level 4: 1000 XP
    - Level 5: 2000 XP (Master)
    
    Returns:
        Dict mit level_up Info falls Level gestiegen
    """
    LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000]
    
    # Aktuellen Stand holen
    progress = get_or_create_sdt_progress(conn, user_id)
    
    # XP-Spalte basierend auf Grundbedürfnis
    xp_col = f"{grundbeduerfnis}_xp"
    level_col = f"{grundbeduerfnis}_level"
    
    old_xp = progress.get(xp_col, 0)
    old_level = progress.get(level_col, 0)
    
    new_xp = old_xp + xp_earned
    
    # Neues Level berechnen
    new_level = 0
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if new_xp >= threshold:
            new_level = i
    new_level = min(new_level, 5)  # Max Level 5
    
    level_up = new_level > old_level
    
    # Update in DB
    c = conn.cursor()
    c.execute(f'''
        UPDATE motivation_sdt_progress 
        SET {xp_col} = ?, {level_col} = ?, 
            total_xp = total_xp + ?,
            total_challenges = total_challenges + 1,
            updated_at = ?
        WHERE user_id = ?
    ''', (new_xp, new_level, xp_earned, datetime.now().isoformat(), user_id))
    conn.commit()
    
    return {
        "grundbeduerfnis": grundbeduerfnis,
        "old_level": old_level,
        "new_level": new_level,
        "old_xp": old_xp,
        "new_xp": new_xp,
        "xp_earned": xp_earned,
        "level_up": level_up,
        "next_level_xp": LEVEL_THRESHOLDS[new_level + 1] if new_level < 5 else None
    }


def get_sdt_summary(conn: sqlite3.Connection, user_id: str) -> Dict[str, Any]:
    """
    Holt eine Zusammenfassung des SDT-Progress für UI-Anzeige.
    """
    progress = get_or_create_sdt_progress(conn, user_id)
    
    LEVEL_THRESHOLDS = [0, 100, 250, 500, 1000, 2000]
    
    def calc_progress_pct(xp: int, level: int) -> float:
        if level >= 5:
            return 100.0
        current_threshold = LEVEL_THRESHOLDS[level]
        next_threshold = LEVEL_THRESHOLDS[level + 1]
        return ((xp - current_threshold) / (next_threshold - current_threshold)) * 100
    
    return {
        "autonomie": {
            "level": progress["autonomie_level"],
            "xp": progress["autonomie_xp"],
            "progress_pct": calc_progress_pct(progress["autonomie_xp"], progress["autonomie_level"]),
            "icon": "🎯",
            "name": "Autonomie"
        },
        "kompetenz": {
            "level": progress["kompetenz_level"],
            "xp": progress["kompetenz_xp"],
            "progress_pct": calc_progress_pct(progress["kompetenz_xp"], progress["kompetenz_level"]),
            "icon": "💪",
            "name": "Kompetenz"
        },
        "verbundenheit": {
            "level": progress["verbundenheit_level"],
            "xp": progress["verbundenheit_xp"],
            "progress_pct": calc_progress_pct(progress["verbundenheit_xp"], progress["verbundenheit_level"]),
            "icon": "👥",
            "name": "Verbundenheit"
        },
        "total_challenges": progress["total_challenges"],
        "total_xp": progress["total_xp"]
    }


# ============================================
# STREAK SYSTEM (Duolingo Style)
# ============================================

def get_or_create_streak(conn: sqlite3.Connection, user_id: str) -> Dict[str, Any]:
    """Holt oder erstellt Streak-Daten."""
    c = conn.cursor()
    
    c.execute('''
        SELECT current_streak, longest_streak, last_activity_date, 
               freeze_available, freeze_used_date
        FROM motivation_streaks WHERE user_id = ?
    ''', (user_id,))
    
    row = c.fetchone()
    
    if row:
        return {
            "current_streak": row[0],
            "longest_streak": row[1],
            "last_activity_date": row[2],
            "freeze_available": row[3],
            "freeze_used_date": row[4]
        }
    else:
        c.execute('''
            INSERT INTO motivation_streaks (user_id) VALUES (?)
        ''', (user_id,))
        conn.commit()
        
        return {
            "current_streak": 0,
            "longest_streak": 0,
            "last_activity_date": None,
            "freeze_available": 1,
            "freeze_used_date": None
        }


def update_streak(conn: sqlite3.Connection, user_id: str) -> Dict[str, Any]:
    """
    Aktualisiert den Streak nach einer Aktivität.
    
    Logik:
    - Heute schon aktiv? → Keine Änderung
    - Gestern aktiv? → Streak + 1
    - Vorgestern aktiv + Freeze verfügbar? → Streak behalten, Freeze nutzen
    - Sonst → Streak auf 1 zurücksetzen
    
    Returns:
        Dict mit streak_info und streak_broken/streak_saved Flags
    """
    streak_data = get_or_create_streak(conn, user_id)
    today = date.today()
    
    last_activity = streak_data["last_activity_date"]
    if last_activity:
        if isinstance(last_activity, str):
            last_activity = date.fromisoformat(last_activity)
    
    current_streak = streak_data["current_streak"]
    longest_streak = streak_data["longest_streak"]
    freeze_available = streak_data["freeze_available"]
    
    result = {
        "streak_continued": False,
        "streak_broken": False,
        "streak_saved_by_freeze": False,
        "freeze_used": False,
        "new_longest": False
    }
    
    if last_activity == today:
        # Heute schon aktiv - keine Änderung
        result["streak_continued"] = True
        return {**result, "current_streak": current_streak, "longest_streak": longest_streak}
    
    yesterday = today - timedelta(days=1)
    day_before = today - timedelta(days=2)
    
    if last_activity == yesterday:
        # Gestern aktiv → Streak fortsetzen
        current_streak += 1
        result["streak_continued"] = True
    elif last_activity == day_before and freeze_available > 0:
        # Vorgestern aktiv + Freeze → Streak retten
        freeze_available -= 1
        result["streak_saved_by_freeze"] = True
        result["freeze_used"] = True
        # Streak bleibt gleich, wird aber heute fortgesetzt
        current_streak += 1
    elif last_activity is None:
        # Erste Aktivität überhaupt
        current_streak = 1
    else:
        # Streak gebrochen
        result["streak_broken"] = True
        current_streak = 1
    
    # Longest Streak aktualisieren
    if current_streak > longest_streak:
        longest_streak = current_streak
        result["new_longest"] = True
    
    # In DB speichern
    c = conn.cursor()
    c.execute('''
        UPDATE motivation_streaks 
        SET current_streak = ?, longest_streak = ?, last_activity_date = ?,
            freeze_available = ?, updated_at = ?
        WHERE user_id = ?
    ''', (current_streak, longest_streak, today.isoformat(), 
          freeze_available, datetime.now().isoformat(), user_id))
    conn.commit()
    
    return {
        **result,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "freeze_available": freeze_available
    }


def add_streak_freeze(conn: sqlite3.Connection, user_id: str, count: int = 1) -> int:
    """
    Fügt Streak-Freezes hinzu (z.B. als Belohnung).
    Returns: Neue Anzahl verfügbarer Freezes
    """
    c = conn.cursor()
    c.execute('''
        UPDATE motivation_streaks 
        SET freeze_available = freeze_available + ?
        WHERE user_id = ?
    ''', (count, user_id))
    conn.commit()
    
    c.execute('SELECT freeze_available FROM motivation_streaks WHERE user_id = ?', (user_id,))
    return c.fetchone()[0]


# ============================================
# ACTIVITY LOG (für Heatmap)
# ============================================

def log_activity(
    conn: sqlite3.Connection,
    user_id: str,
    challenge_id: str,
    grundbeduerfnis: str,
    xp_earned: int
) -> None:
    """Loggt eine Aktivität für die Heatmap."""
    c = conn.cursor()
    c.execute('''
        INSERT INTO motivation_activity_log 
        (user_id, activity_date, challenge_id, grundbeduerfnis, xp_earned)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, date.today().isoformat(), challenge_id, grundbeduerfnis, xp_earned))
    conn.commit()


def get_activity_heatmap_data(
    conn: sqlite3.Connection,
    user_id: str,
    weeks: int = 12
) -> List[Dict[str, Any]]:
    """
    Holt Aktivitätsdaten für die GitHub-Style Heatmap.
    
    Returns:
        Liste von {date, grundbeduerfnis, count, xp} pro Tag
    """
    c = conn.cursor()
    
    start_date = date.today() - timedelta(weeks=weeks * 7)
    
    c.execute('''
        SELECT activity_date, grundbeduerfnis, COUNT(*) as count, SUM(xp_earned) as xp
        FROM motivation_activity_log
        WHERE user_id = ? AND activity_date >= ?
        GROUP BY activity_date, grundbeduerfnis
        ORDER BY activity_date
    ''', (user_id, start_date.isoformat()))
    
    return [{
        "date": row[0],
        "grundbeduerfnis": row[1],
        "count": row[2],
        "xp": row[3]
    } for row in c.fetchall()]


def get_daily_activity_summary(
    conn: sqlite3.Connection,
    user_id: str,
    target_date: date = None
) -> Dict[str, Any]:
    """Holt Aktivitäts-Zusammenfassung für einen Tag."""
    if target_date is None:
        target_date = date.today()
    
    c = conn.cursor()
    c.execute('''
        SELECT grundbeduerfnis, COUNT(*) as count, SUM(xp_earned) as xp
        FROM motivation_activity_log
        WHERE user_id = ? AND activity_date = ?
        GROUP BY grundbeduerfnis
    ''', (user_id, target_date.isoformat()))
    
    result = {
        "date": target_date.isoformat(),
        "autonomie": {"count": 0, "xp": 0},
        "kompetenz": {"count": 0, "xp": 0},
        "verbundenheit": {"count": 0, "xp": 0},
        "total_count": 0,
        "total_xp": 0
    }
    
    for row in c.fetchall():
        gb = row[0]
        if gb in result:
            result[gb] = {"count": row[1], "xp": row[2]}
            result["total_count"] += row[1]
            result["total_xp"] += row[2]
    
    return result


# ============================================
# BADGES
# ============================================

def award_badge(
    conn: sqlite3.Connection,
    user_id: str,
    badge_id: str
) -> bool:
    """
    Vergibt ein Badge an einen User.
    Returns: True wenn neu vergeben, False wenn schon vorhanden
    """
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO motivation_badges (user_id, badge_id)
            VALUES (?, ?)
        ''', (user_id, badge_id))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Badge bereits vorhanden
        return False


def get_user_badges(conn: sqlite3.Connection, user_id: str) -> List[Dict[str, Any]]:
    """Holt alle Badges eines Users."""
    c = conn.cursor()
    c.execute('''
        SELECT badge_id, earned_at
        FROM motivation_badges
        WHERE user_id = ?
        ORDER BY earned_at
    ''', (user_id,))
    
    return [{"badge_id": row[0], "earned_at": row[1]} for row in c.fetchall()]


def has_badge(conn: sqlite3.Connection, user_id: str, badge_id: str) -> bool:
    """Prüft ob User ein bestimmtes Badge hat."""
    c = conn.cursor()
    c.execute('''
        SELECT 1 FROM motivation_badges WHERE user_id = ? AND badge_id = ?
    ''', (user_id, badge_id))
    return c.fetchone() is not None


# ============================================
# ZERTIFIKATE
# ============================================

def issue_certificate(
    conn: sqlite3.Connection,
    user_id: str,
    certificate_type: str,
    age_group: str,
    challenges_completed: List[str],
    total_xp: int
) -> int:
    """
    Stellt ein Zertifikat aus.
    Returns: Certificate ID
    """
    c = conn.cursor()
    c.execute('''
        INSERT INTO motivation_certificates 
        (user_id, certificate_type, age_group, challenges_completed, total_xp)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, certificate_type, age_group, json.dumps(challenges_completed), total_xp))
    conn.commit()
    return c.lastrowid


def get_user_certificates(
    conn: sqlite3.Connection,
    user_id: str
) -> List[Dict[str, Any]]:
    """Holt alle Zertifikate eines Users."""
    c = conn.cursor()
    c.execute('''
        SELECT id, certificate_type, age_group, challenges_completed, total_xp, issued_at
        FROM motivation_certificates
        WHERE user_id = ?
        ORDER BY issued_at DESC
    ''', (user_id,))
    
    return [{
        "id": row[0],
        "type": row[1],
        "age_group": row[2],
        "challenges": json.loads(row[3]) if row[3] else [],
        "total_xp": row[4],
        "issued_at": row[5]
    } for row in c.fetchall()]


# ============================================
# STATISTIKEN
# ============================================

def get_user_motivation_stats(
    conn: sqlite3.Connection,
    user_id: str
) -> Dict[str, Any]:
    """
    Holt umfassende Statistiken für einen User.
    Kombiniert alle Datenquellen.
    """
    sdt = get_sdt_summary(conn, user_id)
    streak = get_or_create_streak(conn, user_id)
    badges = get_user_badges(conn, user_id)
    certificates = get_user_certificates(conn, user_id)
    today_activity = get_daily_activity_summary(conn, user_id)
    
    return {
        "sdt_progress": sdt,
        "streak": {
            "current": streak["current_streak"],
            "longest": streak["longest_streak"],
            "freeze_available": streak["freeze_available"]
        },
        "badges_count": len(badges),
        "badges": badges,
        "certificates_count": len(certificates),
        "certificates": certificates,
        "today": today_activity,
        "total_xp": sdt["total_xp"],
        "total_challenges": sdt["total_challenges"]
    }


# ============================================
# UTILITY FUNCTIONS
# ============================================

def reset_user_motivation_data(conn: sqlite3.Connection, user_id: str) -> None:
    """
    Setzt alle Motivation-Daten eines Users zurück.
    VORSICHT: Nur für Test-/Debug-Zwecke!
    """
    c = conn.cursor()
    
    tables = [
        "motivation_challenges",
        "motivation_sdt_progress",
        "motivation_streaks",
        "motivation_activity_log",
        "motivation_badges",
        "motivation_certificates"
    ]
    
    for table in tables:
        c.execute(f'DELETE FROM {table} WHERE user_id = ?', (user_id,))
    
    conn.commit()


# ============================================
# TEST / DEMO
# ============================================

if __name__ == "__main__":
    # Quick Test
    conn = sqlite3.connect(":memory:")
    init_motivation_tables(conn)
    
    test_user = "test123"
    
    # Challenge speichern
    save_challenge_progress(
        conn, test_user, "us_wozu", "unterstufe", "autonomie",
        phase="complete", user_input="Ich lerne, weil...", 
        xp_earned=60, completed=True
    )
    
    # SDT Progress updaten
    result = update_sdt_progress(conn, test_user, "autonomie", 60)
    print(f"SDT Update: {result}")
    
    # Streak updaten
    streak = update_streak(conn, test_user)
    print(f"Streak: {streak}")
    
    # Stats abrufen
    stats = get_user_motivation_stats(conn, test_user)
    print(f"Stats: {stats}")
    
    print("✅ Alle Tests erfolgreich!")
