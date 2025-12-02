"""
🏅 Motivation Badge System
==========================

Badge-Definitionen basierend auf:
- Selbstbestimmungstheorie (SDT): Badges für Autonomie, Kompetenz, Verbundenheit
- Bandura's 4 Quellen der Selbstwirksamkeit: Mastery, Vicarious, Persuasion, Affective
- Khan Academy: Geheime "Black Hole" Badges
- GitHub: Achievement-System ohne Wettbewerb

Badge-Kategorien:
1. SDT-Starter: Erste Challenge pro Grundbedürfnis
2. SDT-Meister: Alle Challenges pro Grundbedürfnis
3. Streak-Badges: Konsistenz belohnen
4. Birkenbihl-Badges: ABC-Listen, KaWa
5. Geheime Badges: Überraschende Achievements
"""

from typing import Dict, List, Any, Optional
from datetime import date


# ============================================
# BADGE DEFINITIONEN
# ============================================

MOTIVATION_BADGES = {
    
    # ══════════════════════════════════════════
    # SDT STARTER BADGES
    # ══════════════════════════════════════════
    
    "autonomie_starter": {
        "id": "autonomie_starter",
        "name": "Autonomie-Entdecker",
        "icon": "🎯",
        "category": "sdt_starter",
        "description": "Erste Autonomie-Challenge abgeschlossen",
        "xp_reward": 20,
        "secret": False,
        "condition": {
            "type": "category_count",
            "category": "autonomie",
            "min_count": 1
        }
    },
    
    "kompetenz_starter": {
        "id": "kompetenz_starter",
        "name": "Kompetenz-Entdecker",
        "icon": "💪",
        "category": "sdt_starter",
        "description": "Erste Kompetenz-Challenge abgeschlossen",
        "xp_reward": 20,
        "secret": False,
        "condition": {
            "type": "category_count",
            "category": "kompetenz",
            "min_count": 1
        }
    },
    
    "verbundenheit_starter": {
        "id": "verbundenheit_starter",
        "name": "Verbundenheits-Entdecker",
        "icon": "👥",
        "category": "sdt_starter",
        "description": "Erste Verbundenheits-Challenge abgeschlossen",
        "xp_reward": 20,
        "secret": False,
        "condition": {
            "type": "category_count",
            "category": "verbundenheit",
            "min_count": 1
        }
    },
    
    # ══════════════════════════════════════════
    # SDT EXPLORER BADGE
    # ══════════════════════════════════════════
    
    "sdt_explorer": {
        "id": "sdt_explorer",
        "name": "SDT-Explorer",
        "icon": "🔬",
        "category": "sdt_progress",
        "description": "Je eine Challenge aus allen 3 Grundbedürfnissen",
        "xp_reward": 50,
        "secret": False,
        "condition": {
            "type": "all_categories",
            "min_count_per_category": 1
        }
    },
    
    # ══════════════════════════════════════════
    # SDT MEISTER BADGES
    # ══════════════════════════════════════════
    
    "autonomie_meister": {
        "id": "autonomie_meister",
        "name": "Autonomie-Meister",
        "icon": "🏹",
        "category": "sdt_master",
        "description": "Alle Autonomie-Challenges gemeistert",
        "xp_reward": 75,
        "secret": False,
        "condition": {
            "type": "category_complete",
            "category": "autonomie"
        }
    },
    
    "kompetenz_meister": {
        "id": "kompetenz_meister",
        "name": "Kompetenz-Meister",
        "icon": "🏋️",
        "category": "sdt_master",
        "description": "Alle Kompetenz-Challenges gemeistert",
        "xp_reward": 75,
        "secret": False,
        "condition": {
            "type": "category_complete",
            "category": "kompetenz"
        }
    },
    
    "verbundenheit_meister": {
        "id": "verbundenheit_meister",
        "name": "Verbundenheits-Meister",
        "icon": "🤝",
        "category": "sdt_master",
        "description": "Alle Verbundenheits-Challenges gemeistert",
        "xp_reward": 75,
        "secret": False,
        "condition": {
            "type": "category_complete",
            "category": "verbundenheit"
        }
    },
    
    # ══════════════════════════════════════════
    # STREAK BADGES (Duolingo Style)
    # ══════════════════════════════════════════
    
    "streak_3": {
        "id": "streak_3",
        "name": "Motivation-Funke",
        "icon": "🔥",
        "category": "streak",
        "description": "3 Tage in Folge Challenges gemacht",
        "xp_reward": 30,
        "secret": False,
        "condition": {
            "type": "streak",
            "min_days": 3
        }
    },
    
    "streak_7": {
        "id": "streak_7",
        "name": "Motivation-Flamme",
        "icon": "🔥🔥",
        "category": "streak",
        "description": "7 Tage in Folge aktiv",
        "xp_reward": 50,
        "secret": False,
        "condition": {
            "type": "streak",
            "min_days": 7
        }
    },
    
    "streak_14": {
        "id": "streak_14",
        "name": "Motivation-Feuer",
        "icon": "🔥🔥🔥",
        "category": "streak",
        "description": "14 Tage am Stück motiviert",
        "xp_reward": 100,
        "secret": False,
        "condition": {
            "type": "streak",
            "min_days": 14
        }
    },
    
    "streak_30": {
        "id": "streak_30",
        "name": "Motivation-Inferno",
        "icon": "💥",
        "category": "streak",
        "description": "30 Tage ununterbrochen!",
        "xp_reward": 200,
        "secret": False,
        "condition": {
            "type": "streak",
            "min_days": 30
        }
    },
    
    # ══════════════════════════════════════════
    # EFFORT BADGES
    # ══════════════════════════════════════════
    
    "first_challenge": {
        "id": "first_challenge",
        "name": "Erster Schritt",
        "icon": "👣",
        "category": "effort",
        "description": "Erste Motivation-Challenge abgeschlossen",
        "xp_reward": 10,
        "secret": False,
        "condition": {
            "type": "total_count",
            "min_count": 1
        }
    },
    
    "five_challenges": {
        "id": "five_challenges",
        "name": "Motivations-Lehrling",
        "icon": "📚",
        "category": "effort",
        "description": "5 Challenges geschafft",
        "xp_reward": 30,
        "secret": False,
        "condition": {
            "type": "total_count",
            "min_count": 5
        }
    },
    
    "ten_challenges": {
        "id": "ten_challenges",
        "name": "Motivations-Geselle",
        "icon": "📖",
        "category": "effort",
        "description": "10 Challenges gemeistert",
        "xp_reward": 50,
        "secret": False,
        "condition": {
            "type": "total_count",
            "min_count": 10
        }
    },
    
    "twentyfive_challenges": {
        "id": "twentyfive_challenges",
        "name": "Motivations-Experte",
        "icon": "🎓",
        "category": "effort",
        "description": "25 Challenges abgeschlossen",
        "xp_reward": 100,
        "secret": False,
        "condition": {
            "type": "total_count",
            "min_count": 25
        }
    },
    
    # ══════════════════════════════════════════
    # BIRKENBIHL BADGES
    # ══════════════════════════════════════════
    
    "abc_beginner": {
        "id": "abc_beginner",
        "name": "ABC-Anfänger",
        "icon": "🔤",
        "category": "birkenbihl",
        "description": "Erste ABC-Liste erstellt",
        "xp_reward": 20,
        "secret": False,
        "condition": {
            "type": "challenge_specific",
            "challenge_ids": ["us_abc", "ms_abc", "os_abc"],
            "min_count": 1
        }
    },
    
    "abc_master": {
        "id": "abc_master",
        "name": "ABC-Meister",
        "icon": "🧠",
        "category": "birkenbihl",
        "description": "5 ABC-Listen erstellt",
        "xp_reward": 75,
        "secret": False,
        "condition": {
            "type": "challenge_specific",
            "challenge_ids": ["us_abc", "ms_abc", "os_abc"],
            "min_count": 5
        }
    },
    
    # ══════════════════════════════════════════
    # COMPLETION BADGES
    # ══════════════════════════════════════════
    
    "age_complete_grundschule": {
        "id": "age_complete_grundschule",
        "name": "Grundschul-Champion",
        "icon": "🌈",
        "category": "completion",
        "description": "Alle Grundschul-Challenges gemeistert",
        "xp_reward": 100,
        "secret": False,
        "condition": {
            "type": "age_complete",
            "age_group": "grundschule"
        }
    },
    
    "age_complete_unterstufe": {
        "id": "age_complete_unterstufe",
        "name": "Unterstufen-Champion",
        "icon": "🌟",
        "category": "completion",
        "description": "Alle Unterstufen-Challenges gemeistert",
        "xp_reward": 150,
        "secret": False,
        "condition": {
            "type": "age_complete",
            "age_group": "unterstufe"
        }
    },
    
    "age_complete_mittelstufe": {
        "id": "age_complete_mittelstufe",
        "name": "Mittelstufen-Champion",
        "icon": "⭐",
        "category": "completion",
        "description": "Alle Mittelstufen-Challenges gemeistert",
        "xp_reward": 200,
        "secret": False,
        "condition": {
            "type": "age_complete",
            "age_group": "mittelstufe"
        }
    },
    
    "age_complete_oberstufe": {
        "id": "age_complete_oberstufe",
        "name": "Oberstufen-Champion",
        "icon": "🏆",
        "category": "completion",
        "description": "Alle Oberstufen-Challenges gemeistert",
        "xp_reward": 250,
        "secret": False,
        "condition": {
            "type": "age_complete",
            "age_group": "oberstufe"
        }
    },
    
    # ══════════════════════════════════════════
    # GEHEIME BADGES (Khan Academy "Black Hole" Style)
    # ══════════════════════════════════════════
    
    "secret_weekend_warrior": {
        "id": "secret_weekend_warrior",
        "name": "???",
        "icon": "❓",
        "category": "secret",
        "description": "Geheimes Achievement",
        "xp_reward": 50,
        "secret": True,
        "revealed": {
            "name": "Wochenend-Krieger",
            "icon": "🗡️",
            "description": "Challenge am Wochenende gemacht"
        },
        "condition": {
            "type": "weekend_activity"
        }
    },
    
    "secret_night_owl": {
        "id": "secret_night_owl",
        "name": "???",
        "icon": "❓",
        "category": "secret",
        "description": "Geheimes Achievement",
        "xp_reward": 30,
        "secret": True,
        "revealed": {
            "name": "Nacht-Eule",
            "icon": "🦉",
            "description": "Challenge nach 22 Uhr abgeschlossen"
        },
        "condition": {
            "type": "time_based",
            "after_hour": 22
        }
    },
    
    "secret_early_bird": {
        "id": "secret_early_bird",
        "name": "???",
        "icon": "❓",
        "category": "secret",
        "description": "Geheimes Achievement",
        "xp_reward": 30,
        "secret": True,
        "revealed": {
            "name": "Früher Vogel",
            "icon": "🐦",
            "description": "Challenge vor 7 Uhr abgeschlossen"
        },
        "condition": {
            "type": "time_based",
            "before_hour": 7
        }
    },
    
    "secret_comeback": {
        "id": "secret_comeback",
        "name": "???",
        "icon": "❓",
        "category": "secret",
        "description": "Geheimes Achievement",
        "xp_reward": 75,
        "secret": True,
        "revealed": {
            "name": "Comeback-Kid",
            "icon": "🦋",
            "description": "Nach 7+ Tagen Pause zurückgekommen"
        },
        "condition": {
            "type": "comeback",
            "min_days_away": 7
        }
    },
    
    "secret_perfectionist": {
        "id": "secret_perfectionist",
        "name": "???",
        "icon": "❓",
        "category": "secret",
        "description": "Geheimes Achievement",
        "xp_reward": 100,
        "secret": True,
        "revealed": {
            "name": "Perfektionist",
            "icon": "💎",
            "description": "Alle Challenges einer Kategorie an einem Tag"
        },
        "condition": {
            "type": "same_day_category_complete"
        }
    },
}


# ============================================
# BADGE CATEGORIES FOR UI
# ============================================

BADGE_CATEGORIES = {
    "sdt_starter": {
        "name": "SDT-Entdecker",
        "icon": "🔍",
        "description": "Erste Schritte in jedem Grundbedürfnis"
    },
    "sdt_progress": {
        "name": "SDT-Fortschritt",
        "icon": "📊",
        "description": "Fortschritt in der Selbstbestimmungstheorie"
    },
    "sdt_master": {
        "name": "SDT-Meister",
        "icon": "🏆",
        "description": "Meisterschaft in den Grundbedürfnissen"
    },
    "streak": {
        "name": "Streaks",
        "icon": "🔥",
        "description": "Belohnungen für Konsistenz"
    },
    "effort": {
        "name": "Einsatz",
        "icon": "💪",
        "description": "Belohnungen für Durchhaltevermögen"
    },
    "birkenbihl": {
        "name": "Birkenbihl-Methoden",
        "icon": "🧠",
        "description": "Gehirn-gerechtes Lernen"
    },
    "completion": {
        "name": "Abschluss",
        "icon": "🎓",
        "description": "Altersstufen-Abschlüsse"
    },
    "secret": {
        "name": "Geheim",
        "icon": "❓",
        "description": "Überraschende Achievements"
    }
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_badge_display(badge_id: str, is_earned: bool = True) -> Dict[str, Any]:
    """
    Gibt Badge-Info zur Anzeige zurück.
    Bei geheimen Badges: Zeigt echte Info nur wenn verdient.
    """
    badge = MOTIVATION_BADGES.get(badge_id)
    if not badge:
        return {"id": badge_id, "name": "Unbekannt", "icon": "❓", "description": ""}
    
    if badge.get("secret") and not is_earned:
        return {
            "id": badge_id,
            "name": badge["name"],  # "???"
            "icon": badge["icon"],  # "❓"
            "description": badge["description"],  # "Geheimes Achievement"
            "category": badge["category"],
            "secret": True
        }
    elif badge.get("secret") and is_earned:
        revealed = badge.get("revealed", {})
        return {
            "id": badge_id,
            "name": revealed.get("name", badge["name"]),
            "icon": revealed.get("icon", badge["icon"]),
            "description": revealed.get("description", badge["description"]),
            "category": badge["category"],
            "secret": True,
            "xp_reward": badge.get("xp_reward", 0)
        }
    else:
        return {
            "id": badge_id,
            "name": badge["name"],
            "icon": badge["icon"],
            "description": badge["description"],
            "category": badge["category"],
            "secret": False,
            "xp_reward": badge.get("xp_reward", 0)
        }


def get_all_badges_by_category() -> Dict[str, List[Dict]]:
    """Gibt alle Badges gruppiert nach Kategorie zurück."""
    result = {cat: [] for cat in BADGE_CATEGORIES.keys()}
    
    for badge_id, badge in MOTIVATION_BADGES.items():
        cat = badge.get("category", "effort")
        if cat in result:
            result[cat].append(get_badge_display(badge_id, is_earned=False))
    
    return result


def check_badge_condition(badge_id: str, user_stats: Dict) -> bool:
    """
    Prüft ob ein Badge verdient wurde.
    
    Args:
        badge_id: ID des Badges
        user_stats: Dict mit:
            - completed_by_category: {"autonomie": 2, "kompetenz": 1, ...}
            - total_completed: int
            - current_streak: int
            - longest_streak: int
            - challenge_counts: {"us_abc": 3, ...}
            - completed_age_groups: ["grundschule", ...]
            - last_activity_date: date
            - activity_hour: int (0-23)
            - days_since_last: int
    """
    badge = MOTIVATION_BADGES.get(badge_id)
    if not badge:
        return False
    
    condition = badge.get("condition", {})
    cond_type = condition.get("type")
    
    # Category Count
    if cond_type == "category_count":
        cat = condition.get("category")
        min_count = condition.get("min_count", 1)
        actual = user_stats.get("completed_by_category", {}).get(cat, 0)
        return actual >= min_count
    
    # All Categories
    if cond_type == "all_categories":
        min_per = condition.get("min_count_per_category", 1)
        by_cat = user_stats.get("completed_by_category", {})
        return all(by_cat.get(c, 0) >= min_per for c in ["autonomie", "kompetenz", "verbundenheit"])
    
    # Category Complete
    if cond_type == "category_complete":
        cat = condition.get("category")
        # Dies erfordert Wissen über die Gesamtzahl - vereinfacht: 2+ als "complete"
        total_in_cat = user_stats.get("total_by_category", {}).get(cat, 2)
        actual = user_stats.get("completed_by_category", {}).get(cat, 0)
        return actual >= total_in_cat
    
    # Streak
    if cond_type == "streak":
        min_days = condition.get("min_days", 3)
        current = max(user_stats.get("current_streak", 0), user_stats.get("longest_streak", 0))
        return current >= min_days
    
    # Total Count
    if cond_type == "total_count":
        min_count = condition.get("min_count", 1)
        return user_stats.get("total_completed", 0) >= min_count
    
    # Challenge Specific
    if cond_type == "challenge_specific":
        challenge_ids = condition.get("challenge_ids", [])
        min_count = condition.get("min_count", 1)
        counts = user_stats.get("challenge_counts", {})
        total = sum(counts.get(cid, 0) for cid in challenge_ids)
        return total >= min_count
    
    # Age Complete
    if cond_type == "age_complete":
        age_group = condition.get("age_group")
        return age_group in user_stats.get("completed_age_groups", [])
    
    # Weekend Activity
    if cond_type == "weekend_activity":
        last_date = user_stats.get("last_activity_date")
        if last_date:
            if isinstance(last_date, str):
                last_date = date.fromisoformat(last_date)
            return last_date.weekday() >= 5  # Samstag=5, Sonntag=6
        return False
    
    # Time Based
    if cond_type == "time_based":
        hour = user_stats.get("activity_hour", 12)
        after = condition.get("after_hour")
        before = condition.get("before_hour")
        if after and hour >= after:
            return True
        if before and hour < before:
            return True
        return False
    
    # Comeback
    if cond_type == "comeback":
        min_days = condition.get("min_days_away", 7)
        days_away = user_stats.get("days_since_last", 0)
        return days_away >= min_days
    
    return False


def check_and_award_badges(conn, user_id: str, age_group: str) -> List[str]:
    """
    Prüft alle Badges und vergibt neue.
    
    Returns:
        Liste der neu vergebenen Badge-IDs
    """
    from .motivation_db import (
        count_completed_challenges,
        get_completed_challenges,
        get_or_create_streak,
        award_badge,
        has_badge,
        get_daily_activity_summary,
    )
    from .motivation_content import (
        get_all_challenge_ids,
        count_challenges_by_category,
    )
    from datetime import datetime
    
    # User-Stats sammeln
    completed = get_completed_challenges(conn, user_id)
    streak = get_or_create_streak(conn, user_id)
    
    # Completed by category
    by_cat = {"autonomie": 0, "kompetenz": 0, "verbundenheit": 0}
    challenge_counts = {}
    
    for c in completed:
        cat = c.get("grundbeduerfnis")
        if cat in by_cat:
            by_cat[cat] += 1
        
        cid = c.get("challenge_id")
        challenge_counts[cid] = challenge_counts.get(cid, 0) + 1
    
    # Total by category (für "complete" check)
    total_by_cat = count_challenges_by_category(age_group)
    
    # Completed age groups
    completed_age_groups = []
    for ag in ["grundschule", "unterstufe", "mittelstufe", "oberstufe"]:
        all_ids = get_all_challenge_ids(ag)
        completed_ids = [c["challenge_id"] for c in get_completed_challenges(conn, user_id, ag)]
        if len(completed_ids) >= len(all_ids) and len(all_ids) > 0:
            completed_age_groups.append(ag)
    
    user_stats = {
        "completed_by_category": by_cat,
        "total_by_category": total_by_cat,
        "total_completed": len(completed),
        "current_streak": streak.get("current_streak", 0),
        "longest_streak": streak.get("longest_streak", 0),
        "challenge_counts": challenge_counts,
        "completed_age_groups": completed_age_groups,
        "last_activity_date": streak.get("last_activity_date"),
        "activity_hour": datetime.now().hour,
        "days_since_last": 0,  # Vereinfacht
    }
    
    # Alle Badges prüfen
    new_badges = []
    
    for badge_id in MOTIVATION_BADGES.keys():
        if has_badge(conn, user_id, badge_id):
            continue
        
        if check_badge_condition(badge_id, user_stats):
            if award_badge(conn, user_id, badge_id):
                new_badges.append(badge_id)
    
    return new_badges


# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    # Test: Badge-Übersicht
    print("BADGE-ÜBERSICHT\n" + "="*50)
    
    for cat_id, cat_info in BADGE_CATEGORIES.items():
        badges = [b for b in MOTIVATION_BADGES.values() if b.get("category") == cat_id]
        print(f"\n{cat_info['icon']} {cat_info['name']} ({len(badges)} Badges)")
        for b in badges:
            secret_marker = " 🔒" if b.get("secret") else ""
            print(f"  - {b['icon']} {b['name']}{secret_marker}: {b['description']}")
    
    # Test: Badge Display
    print("\n\nBADGE DISPLAY TEST\n" + "="*50)
    
    # Normales Badge
    display = get_badge_display("autonomie_starter", is_earned=True)
    print(f"Earned Normal: {display['icon']} {display['name']}")
    
    # Geheimes Badge (nicht verdient)
    display = get_badge_display("secret_weekend_warrior", is_earned=False)
    print(f"Secret (not earned): {display['icon']} {display['name']}")
    
    # Geheimes Badge (verdient)
    display = get_badge_display("secret_weekend_warrior", is_earned=True)
    print(f"Secret (earned): {display['icon']} {display['name']}")
    
    print("\n✅ Alle Tests erfolgreich!")
