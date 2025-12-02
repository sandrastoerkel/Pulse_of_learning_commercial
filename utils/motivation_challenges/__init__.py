"""
🎯 Motivation Challenges Module
===============================

Gamification-System für Motivation basierend auf SDT.

Hauptfunktion:
    render_motivation_challenge(user_data, conn, xp_callback)

Komponenten:
    - motivation_db: Datenbank-Layer
    - motivation_content: Challenge-Definitionen
    - motivation_widget: UI-Komponenten
    - motivation_badges: Badge-System
"""

from .motivation_db import (
    init_motivation_tables,
    save_challenge_progress,
    get_challenge_progress,
    get_completed_challenges,
    count_completed_challenges,
    get_or_create_sdt_progress,
    update_sdt_progress,
    get_sdt_summary,
    get_or_create_streak,
    update_streak,
    add_streak_freeze,
    log_activity,
    get_activity_heatmap_data,
    get_daily_activity_summary,
    award_badge,
    get_user_badges,
    has_badge,
    issue_certificate,
    get_user_certificates,
    get_user_motivation_stats,
    reset_user_motivation_data,
)

from .motivation_content import (
    MOTIVATION_CHALLENGES,
    MOTIVATION_XP,
    GRUNDBEDUERFNISSE,
    CERTIFICATE_TEXTS,
    get_challenges_for_age,
    get_challenge_by_id,
    get_all_challenge_ids,
    count_challenges_by_category,
    get_total_xp_possible,
    get_challenge_summary,
    calculate_xp_with_streak,
)

from .motivation_badges import (
    MOTIVATION_BADGES,
    BADGE_CATEGORIES,
    get_badge_display,
    get_all_badges_by_category,
    check_badge_condition,
    check_and_award_badges,
)

from .motivation_widget import (
    render_motivation_challenge,
    render_sdt_progress_header,
    render_xp_display,
    render_challenge_overview,
    render_certificate_preview,
)

__all__ = [
    # Main Widget
    "render_motivation_challenge",
    
    # DB Functions
    "init_motivation_tables",
    "save_challenge_progress",
    "get_challenge_progress",
    "get_completed_challenges",
    "get_sdt_summary",
    "update_streak",
    "get_user_motivation_stats",
    
    # Content
    "MOTIVATION_CHALLENGES",
    "GRUNDBEDUERFNISSE",
    "get_challenges_for_age",
    "get_challenge_by_id",
    
    # Badges
    "MOTIVATION_BADGES",
    "check_and_award_badges",
    "get_badge_display",
    
    # UI Components
    "render_sdt_progress_header",
    "render_xp_display",
    "render_certificate_preview",
]

__version__ = "1.0.0"
