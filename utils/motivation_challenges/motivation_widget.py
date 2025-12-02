"""
🎮 Motivation Challenge Widget
==============================

Hauptwidget für die Motivation-Challenges basierend auf SDT.

Phasen-Flow (wie powertechniken_widget):
intro → action → reflect → complete → [nächste Challenge]

Design-Prinzipien:
- GitHub: Contribution-Heatmap, keine Leaderboards
- Duolingo: Streaks, XP, instant Feedback
- Brilliant: Bite-sized, meaningful Challenges
- Khan Academy: Mastery Levels, Skill Tree

UI-Komponenten:
- Challenge-Karte mit Fortschrittsanzeige
- SDT-Skill-Tree (3 Zweige)
- Streak-Display mit Freeze-Option
- Badge-Galerie

Autor: Pulse of Learning
"""

import streamlit as st
from datetime import datetime, date
from typing import Dict, List, Optional, Any, Callable
import json

# Lokale Imports
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
    log_activity,
    get_activity_heatmap_data,
    award_badge,
    get_user_badges,
    has_badge,
    issue_certificate,
    get_user_motivation_stats,
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
    check_and_award_badges,
    get_badge_display,
)


# ============================================
# SESSION STATE KEYS
# ============================================

STATE_KEYS = {
    "current_challenge": "mot_current_challenge",
    "phase": "mot_phase",  # overview, intro, action, reflect, complete, certificate
    "completed_ids": "mot_completed_ids",
    "current_input": "mot_current_input",
    "selected_category": "mot_selected_category",
    "challenge_started_at": "mot_started_at",
}


# ============================================
# INITIALIZATION
# ============================================

def init_session_state():
    """Initialisiert Session State mit Defaults."""
    defaults = {
        STATE_KEYS["phase"]: "overview",
        STATE_KEYS["current_challenge"]: None,
        STATE_KEYS["completed_ids"]: [],
        STATE_KEYS["current_input"]: "",
        STATE_KEYS["selected_category"]: None,
    }
    
    for key, default in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


# ============================================
# UI COMPONENTS: HEADER & NAVIGATION
# ============================================

def render_sdt_progress_header(sdt_summary: Dict, streak_data: Dict):
    """
    Zeigt den SDT-Progress als kompakte Header-Leiste.
    3 Progress-Bars für die 3 Grundbedürfnisse + Streak.
    """
    cols = st.columns([1, 1, 1, 0.8])
    
    # Autonomie
    with cols[0]:
        data = sdt_summary["autonomie"]
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 1.5em;">{data['icon']}</span>
            <div style="font-size: 0.8em; color: #666;">Autonomie Lv.{data['level']}</div>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin-top: 5px;">
                <div style="background: {GRUNDBEDUERFNISSE['autonomie']['color']}; 
                            width: {min(data['progress_pct'], 100)}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Kompetenz
    with cols[1]:
        data = sdt_summary["kompetenz"]
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 1.5em;">{data['icon']}</span>
            <div style="font-size: 0.8em; color: #666;">Kompetenz Lv.{data['level']}</div>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin-top: 5px;">
                <div style="background: {GRUNDBEDUERFNISSE['kompetenz']['color']}; 
                            width: {min(data['progress_pct'], 100)}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Verbundenheit
    with cols[2]:
        data = sdt_summary["verbundenheit"]
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 1.5em;">{data['icon']}</span>
            <div style="font-size: 0.8em; color: #666;">Verbundenheit Lv.{data['level']}</div>
            <div style="background: #e2e8f0; border-radius: 10px; height: 8px; margin-top: 5px;">
                <div style="background: {GRUNDBEDUERFNISSE['verbundenheit']['color']}; 
                            width: {min(data['progress_pct'], 100)}%; height: 100%; border-radius: 10px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Streak
    with cols[3]:
        streak = streak_data.get("current_streak", 0)
        freeze = streak_data.get("freeze_available", 0)
        flame = "🔥" if streak > 0 else "❄️"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <span style="font-size: 1.5em;">{flame}</span>
            <div style="font-size: 1.2em; font-weight: bold; color: #f97316;">{streak}</div>
            <div style="font-size: 0.7em; color: #666;">Tage</div>
            {'<div style="font-size: 0.6em;">🧊 ' + str(freeze) + ' Freeze</div>' if freeze > 0 else ''}
        </div>
        """, unsafe_allow_html=True)


def render_xp_display(total_xp: int, level_info: Optional[Dict] = None):
    """Zeigt XP-Anzeige mit optionalem Level-Info."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
                color: white; padding: 10px 20px; border-radius: 20px; 
                display: inline-block; font-weight: bold;">
        ⭐ {total_xp} XP
    </div>
    """, unsafe_allow_html=True)


# ============================================
# UI COMPONENTS: CHALLENGE OVERVIEW
# ============================================

def render_challenge_overview(
    age_group: str,
    completed_ids: List[str],
    on_challenge_select: Callable[[str], None]
):
    """
    Zeigt die Challenge-Übersicht nach Grundbedürfnissen.
    Ähnlich wie Khan Academy's Skill-Tree.
    """
    challenges = get_challenges_for_age(age_group)
    
    if not challenges:
        st.warning(f"Keine Challenges für Altersstufe '{age_group}' gefunden.")
        return
    
    # Tab-Navigation für Grundbedürfnisse
    tabs = st.tabs([
        f"{GRUNDBEDUERFNISSE['autonomie']['icon']} Autonomie",
        f"{GRUNDBEDUERFNISSE['kompetenz']['icon']} Kompetenz",
        f"{GRUNDBEDUERFNISSE['verbundenheit']['icon']} Verbundenheit",
    ])
    
    categories = ["autonomie", "kompetenz", "verbundenheit"]
    
    for tab, category in zip(tabs, categories):
        with tab:
            cat_challenges = challenges.get(category, [])
            cat_info = GRUNDBEDUERFNISSE[category]
            
            # Kategorie-Header
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {cat_info['color']}22 0%, {cat_info['color']}11 100%);
                        padding: 15px; border-radius: 10px; margin-bottom: 15px;
                        border-left: 4px solid {cat_info['color']};">
                <strong>{cat_info['name']}</strong>: {cat_info['description']}
                <br><small style="color: #666;">{cat_info['science']}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Challenge-Cards
            for challenge in cat_challenges:
                is_completed = challenge["id"] in completed_ids
                
                # Challenge Card
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    status_icon = "✅" if is_completed else "⬜"
                    xp_text = f"+{challenge['xp']} XP"
                    
                    st.markdown(f"""
                    <div style="padding: 10px; background: {'#f0fdf4' if is_completed else '#fff'};
                                border: 1px solid {'#22c55e' if is_completed else '#e2e8f0'};
                                border-radius: 8px; margin-bottom: 8px;">
                        <span style="font-size: 1.3em;">{challenge['icon']}</span>
                        <strong style="margin-left: 10px;">{challenge['name']}</strong>
                        <span style="float: right; color: #f59e0b; font-weight: bold;">{xp_text}</span>
                        <br>
                        <small style="color: #666;">
                            {status_icon} {'Abgeschlossen' if is_completed else f"~{challenge.get('duration_minutes', 5)} Min"}
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    button_text = "🔄 Wiederholen" if is_completed else "▶️ Start"
                    if st.button(button_text, key=f"start_{challenge['id']}", use_container_width=True):
                        on_challenge_select(challenge["id"])


# ============================================
# UI COMPONENTS: CHALLENGE PHASES
# ============================================

def render_challenge_intro(challenge: Dict):
    """Zeigt die Intro-Phase einer Challenge."""
    intro = challenge.get("intro", {})
    cat_info = GRUNDBEDUERFNISSE.get(challenge.get("grundbeduerfnis", "autonomie"))
    
    # Challenge-Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, {cat_info['color']} 0%, {cat_info['color']}cc 100%);
                color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="font-size: 3em;">{challenge['icon']}</span>
            <div>
                <h2 style="margin: 0; color: white;">{challenge['name']}</h2>
                <p style="margin: 5px 0 0 0; opacity: 0.9;">
                    {cat_info['icon']} {cat_info['name']} • +{challenge['xp']} XP • ~{challenge.get('duration_minutes', 5)} Min
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Intro-Text
    st.markdown(f"""
    <div style="font-size: 1.1em; line-height: 1.7; padding: 15px;
                background: #f8fafc; border-radius: 10px;">
        {intro.get('text', '')}
    </div>
    """, unsafe_allow_html=True)
    
    # Fun Fact
    if intro.get("fun_fact"):
        st.info(f"💡 **Fun Fact:** {intro['fun_fact']}")
    
    # Science Note (für ältere Schüler)
    if intro.get("science_note"):
        with st.expander("🔬 Wissenschaftlicher Hintergrund"):
            st.markdown(intro["science_note"])


def render_challenge_action(challenge: Dict) -> Optional[str]:
    """
    Zeigt die Action-Phase und sammelt User-Input.
    Returns: User-Input oder None
    """
    action = challenge.get("action", {})
    
    st.markdown(f"### {action.get('title', 'Deine Aufgabe')}")
    st.markdown(action.get("instruction", ""))
    
    input_type = action.get("input_type", "text")
    input_label = action.get("input_label", "Deine Antwort:")
    placeholder = action.get("placeholder", "")
    min_length = action.get("min_length", 10)
    
    user_input = None
    
    if input_type == "text":
        user_input = st.text_area(
            input_label,
            placeholder=placeholder,
            height=150,
            key=f"input_{challenge['id']}"
        )
    
    elif input_type == "list":
        count = action.get("input_count", 3)
        st.markdown(f"*{input_label}*")
        items = []
        for i in range(count):
            item = st.text_input(
                f"{i+1}.",
                placeholder=placeholder.split('\n')[0] if placeholder else "",
                key=f"list_{challenge['id']}_{i}",
                label_visibility="collapsed"
            )
            if item:
                items.append(f"{i+1}. {item}")
        user_input = "\n".join(items)
    
    elif input_type == "abc_list":
        st.markdown(f"*{input_label}*")
        user_input = st.text_area(
            "ABC-Liste",
            placeholder=placeholder,
            height=250,
            key=f"abc_{challenge['id']}",
            label_visibility="collapsed"
        )
    
    elif input_type in ["plan", "analysis", "chain", "message", "ranking", "progress",
                        "rating_with_reason", "extended_abc", "audit", "transfer_plan"]:
        user_input = st.text_area(
            input_label,
            placeholder=placeholder,
            height=200,
            key=f"input_{challenge['id']}"
        )
    
    elif input_type == "checklist":
        st.markdown(f"*{input_label}*")
        items = action.get("checklist_items", [])
        selected = []
        for i, item in enumerate(items):
            if st.checkbox(item, key=f"check_{challenge['id']}_{i}"):
                selected.append(item)
        user_input = "\n".join(selected)
    
    # Validierung
    if user_input:
        if len(user_input.strip()) < min_length:
            st.warning(f"Bitte schreib mindestens {min_length} Zeichen.")
            return None
    
    return user_input


def render_challenge_reflection(challenge: Dict) -> Optional[str]:
    """
    Zeigt die Reflexions-Phase.
    Returns: Ausgewählte Reflexions-Option
    """
    reflection = challenge.get("reflection", {})
    
    st.markdown("### 💭 Kurze Reflexion")
    st.markdown(reflection.get("question", "Wie war's?"))
    
    options = reflection.get("options", ["👍 Gut", "😐 Okay", "👎 Schwierig"])
    
    selected = st.radio(
        "Wähle eine Option:",
        options,
        key=f"reflect_{challenge['id']}",
        label_visibility="collapsed"
    )
    
    return selected


def render_challenge_complete(challenge: Dict, xp_earned: int, level_up_info: Optional[Dict] = None):
    """Zeigt die Completion-Animation."""
    
    completion_msg = challenge.get("completion_message", "Super gemacht! 🎉")
    
    # XP Animation
    st.markdown(f"""
    <div style="text-align: center; padding: 30px;">
        <div style="font-size: 4em; animation: bounce 0.5s;">🎉</div>
        <h2 style="color: #22c55e; margin: 10px 0;">Challenge geschafft!</h2>
        <div style="font-size: 2em; color: #f59e0b; font-weight: bold;">
            +{xp_earned} XP
        </div>
        <p style="color: #666; margin-top: 15px;">{completion_msg}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Level-Up Anzeige
    if level_up_info and level_up_info.get("level_up"):
        cat_info = GRUNDBEDUERFNISSE.get(level_up_info["grundbeduerfnis"], {})
        st.success(f"""
        🆙 **Level Up!** {cat_info.get('icon', '')} {cat_info.get('name', '')} 
        ist jetzt Level {level_up_info['new_level']}!
        """)


def render_certificate_preview(
    user_name: str,
    age_group: str,
    completed_challenges: List[str],
    total_xp: int
):
    """Zeigt eine Zertifikat-Vorschau."""
    cert_info = CERTIFICATE_TEXTS.get(age_group, {})
    
    st.markdown(f"""
    <div style="border: 3px solid #f59e0b; padding: 30px; border-radius: 15px;
                background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
                text-align: center;">
        <div style="font-size: 3em;">🏆</div>
        <h1 style="color: #b45309; margin: 10px 0;">{cert_info.get('title', 'Zertifikat')}</h1>
        <h3 style="color: #92400e;">{user_name}</h3>
        <p style="font-style: italic; color: #78716c;">{cert_info.get('subtitle', '')}</p>
        <hr style="border-color: #f59e0b50;">
        <p>{cert_info.get('description', '')}</p>
        <div style="margin-top: 20px; font-weight: bold; color: #f59e0b;">
            {len(completed_challenges)} Challenges • {total_xp} XP
        </div>
        <p style="font-size: 0.8em; color: #a8a29e; margin-top: 15px;">
            Ausgestellt am {datetime.now().strftime('%d.%m.%Y')}
        </p>
    </div>
    """, unsafe_allow_html=True)


# ============================================
# MAIN WIDGET FUNCTION
# ============================================

def render_motivation_challenge(
    user_data: Dict[str, Any],
    conn,
    xp_callback: Optional[Callable[[str, int, str], None]] = None
):
    """
    Haupt-Render-Funktion für die Motivation-Challenges.
    
    Args:
        user_data: Dict mit user_id, display_name, age_group
        conn: SQLite Connection
        xp_callback: Optional Callback(user_id, xp, description) für globales XP-System
    
    Usage:
        render_motivation_challenge(
            user_data={"user_id": "123", "display_name": "Max", "age_group": "unterstufe"},
            conn=sqlite_connection,
            xp_callback=add_user_xp  # Optional
        )
    """
    # Init
    init_motivation_tables(conn)
    init_session_state()
    
    # User-Daten extrahieren
    user_id = user_data.get("user_id", "anonymous")
    display_name = user_data.get("display_name", "Lernender")
    age_group = user_data.get("age_group", "unterstufe")
    
    # Daten laden
    stats = get_user_motivation_stats(conn, user_id)
    sdt_summary = stats["sdt_progress"]
    streak_data = stats["streak"]
    completed_db = get_completed_challenges(conn, user_id, age_group)
    completed_ids = [c["challenge_id"] for c in completed_db]
    
    # Header mit Progress
    render_sdt_progress_header(sdt_summary, streak_data)
    st.markdown("---")
    
    # Aktuelle Phase
    phase = st.session_state[STATE_KEYS["phase"]]
    current_challenge_id = st.session_state[STATE_KEYS["current_challenge"]]
    
    # ─────────────────────────────────────────
    # PHASE: OVERVIEW
    # ─────────────────────────────────────────
    if phase == "overview":
        st.markdown(f"### 🎯 Deine Motivation-Challenges")
        st.caption(f"Altersstufe: {age_group.title()} • {len(completed_ids)}/{len(get_all_challenge_ids(age_group))} abgeschlossen")
        
        # Prüfen ob alle fertig → Zertifikat anbieten
        all_ids = get_all_challenge_ids(age_group)
        if len(completed_ids) >= len(all_ids) and len(all_ids) > 0:
            st.success("🎉 Du hast alle Challenges dieser Stufe abgeschlossen!")
            if st.button("🏆 Zertifikat anzeigen", type="primary"):
                st.session_state[STATE_KEYS["phase"]] = "certificate"
                st.rerun()
            st.markdown("---")
        
        def on_challenge_select(challenge_id: str):
            st.session_state[STATE_KEYS["current_challenge"]] = challenge_id
            st.session_state[STATE_KEYS["phase"]] = "intro"
            st.session_state[STATE_KEYS["challenge_started_at"]] = datetime.now().isoformat()
            st.rerun()
        
        render_challenge_overview(age_group, completed_ids, on_challenge_select)
        return
    
    # Challenge laden
    challenge = get_challenge_by_id(current_challenge_id, age_group)
    if not challenge:
        st.error("Challenge nicht gefunden!")
        if st.button("← Zurück zur Übersicht"):
            st.session_state[STATE_KEYS["phase"]] = "overview"
            st.rerun()
        return
    
    # ─────────────────────────────────────────
    # PHASE: INTRO
    # ─────────────────────────────────────────
    if phase == "intro":
        render_challenge_intro(challenge)
        
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                st.session_state[STATE_KEYS["phase"]] = "overview"
                st.rerun()
        with col2:
            if st.button("✅ Verstanden! Los geht's →", type="primary", use_container_width=True):
                st.session_state[STATE_KEYS["phase"]] = "action"
                st.rerun()
        return
    
    # ─────────────────────────────────────────
    # PHASE: ACTION
    # ─────────────────────────────────────────
    if phase == "action":
        render_challenge_intro(challenge)  # Kompakter Header
        st.markdown("---")
        
        user_input = render_challenge_action(challenge)
        
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                st.session_state[STATE_KEYS["phase"]] = "intro"
                st.rerun()
        with col2:
            if user_input and len(user_input.strip()) >= challenge.get("action", {}).get("min_length", 10):
                if st.button("✅ Weiter zur Reflexion →", type="primary", use_container_width=True):
                    st.session_state[STATE_KEYS["current_input"]] = user_input
                    st.session_state[STATE_KEYS["phase"]] = "reflect"
                    st.rerun()
            else:
                st.button("✅ Weiter zur Reflexion →", disabled=True, use_container_width=True)
        return
    
    # ─────────────────────────────────────────
    # PHASE: REFLECT
    # ─────────────────────────────────────────
    if phase == "reflect":
        st.markdown(f"### {challenge['icon']} {challenge['name']}")
        
        # User-Input anzeigen
        user_input = st.session_state.get(STATE_KEYS["current_input"], "")
        with st.expander("📝 Deine Antwort ansehen", expanded=False):
            st.markdown(user_input)
        
        reflection = render_challenge_reflection(challenge)
        
        st.markdown("---")
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.button("← Zurück", use_container_width=True):
                st.session_state[STATE_KEYS["phase"]] = "action"
                st.rerun()
        with col2:
            if st.button("🎉 Challenge abschließen!", type="primary", use_container_width=True):
                # XP berechnen
                base_xp = challenge.get("xp", 50)
                current_streak = streak_data.get("current", 0)
                final_xp = calculate_xp_with_streak(base_xp, current_streak)
                
                # In DB speichern
                save_challenge_progress(
                    conn, user_id, challenge["id"], age_group,
                    challenge["grundbeduerfnis"],
                    phase="complete",
                    user_input=user_input,
                    reflection=reflection,
                    xp_earned=final_xp,
                    completed=True
                )
                
                # SDT Progress updaten
                level_up_info = update_sdt_progress(
                    conn, user_id, challenge["grundbeduerfnis"], final_xp
                )
                
                # Streak updaten
                streak_result = update_streak(conn, user_id)
                
                # Activity loggen
                log_activity(conn, user_id, challenge["id"], challenge["grundbeduerfnis"], final_xp)
                
                # Badges prüfen
                new_badges = check_and_award_badges(conn, user_id, age_group)
                
                # XP Callback
                if xp_callback:
                    xp_callback(user_id, final_xp, f"Motivation-Challenge: {challenge['name']}")
                
                # Session State für Complete-Phase
                st.session_state["mot_last_xp"] = final_xp
                st.session_state["mot_level_up"] = level_up_info
                st.session_state["mot_streak_result"] = streak_result
                st.session_state["mot_new_badges"] = new_badges
                st.session_state[STATE_KEYS["phase"]] = "complete"
                
                st.balloons()
                st.rerun()
        return
    
    # ─────────────────────────────────────────
    # PHASE: COMPLETE
    # ─────────────────────────────────────────
    if phase == "complete":
        xp_earned = st.session_state.get("mot_last_xp", challenge.get("xp", 50))
        level_up_info = st.session_state.get("mot_level_up", {})
        streak_result = st.session_state.get("mot_streak_result", {})
        new_badges = st.session_state.get("mot_new_badges", [])
        
        render_challenge_complete(challenge, xp_earned, level_up_info)
        
        # Streak Info
        if streak_result.get("streak_continued") or streak_result.get("new_longest"):
            st.info(f"🔥 Streak: {streak_result.get('current_streak', 1)} Tage!")
        
        if streak_result.get("streak_saved_by_freeze"):
            st.warning("🧊 Dein Streak wurde durch einen Freeze gerettet!")
        
        # Neue Badges
        if new_badges:
            st.markdown("### 🏅 Neue Badges!")
            for badge_id in new_badges:
                badge = get_badge_display(badge_id)
                st.success(f"{badge['icon']} **{badge['name']}** - {badge['description']}")
        
        st.markdown("---")
        
        # Prüfen ob alle fertig
        updated_completed = get_completed_challenges(conn, user_id, age_group)
        all_ids = get_all_challenge_ids(age_group)
        
        if len(updated_completed) >= len(all_ids):
            st.success("🎉 **Alle Challenges dieser Stufe abgeschlossen!**")
            if st.button("🏆 Zertifikat abholen!", type="primary", use_container_width=True):
                # Zertifikat ausstellen
                total_xp = sum(c.get("xp_earned", 0) for c in updated_completed)
                issue_certificate(
                    conn, user_id, "motivation_complete", age_group,
                    [c["challenge_id"] for c in updated_completed], total_xp
                )
                st.session_state[STATE_KEYS["phase"]] = "certificate"
                st.rerun()
        else:
            remaining = len(all_ids) - len(updated_completed)
            st.info(f"Noch {remaining} Challenge(s) bis zum Zertifikat!")
            
            if st.button("➡️ Nächste Challenge", type="primary", use_container_width=True):
                st.session_state[STATE_KEYS["phase"]] = "overview"
                st.session_state[STATE_KEYS["current_challenge"]] = None
                st.rerun()
        
        if st.button("📋 Zurück zur Übersicht", use_container_width=True):
            st.session_state[STATE_KEYS["phase"]] = "overview"
            st.session_state[STATE_KEYS["current_challenge"]] = None
            st.rerun()
        
        return
    
    # ─────────────────────────────────────────
    # PHASE: CERTIFICATE
    # ─────────────────────────────────────────
    if phase == "certificate":
        completed_db = get_completed_challenges(conn, user_id, age_group)
        total_xp = sum(c.get("xp_earned", 0) for c in completed_db)
        
        render_certificate_preview(
            display_name, age_group,
            [c["challenge_id"] for c in completed_db], total_xp
        )
        
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🖨️ Drucken (Coming Soon)", disabled=True, use_container_width=True):
                pass
        with col2:
            if st.button("📋 Zurück zur Übersicht", use_container_width=True):
                st.session_state[STATE_KEYS["phase"]] = "overview"
                st.rerun()
        
        return


# ============================================
# STANDALONE TEST
# ============================================

if __name__ == "__main__":
    import sqlite3
    
    st.set_page_config(page_title="Motivation Challenges Test", page_icon="🎯", layout="wide")
    
    # Mock User
    test_user = {
        "user_id": "test_user_123",
        "display_name": "Test-Schüler",
        "age_group": "unterstufe",
    }
    
    # Temp DB
    conn = sqlite3.connect(":memory:")
    
    # Render
    render_motivation_challenge(test_user, conn)
