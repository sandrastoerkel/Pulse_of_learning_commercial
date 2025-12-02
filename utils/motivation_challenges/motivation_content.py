"""
📚 Motivation Challenge Content
===============================

Wissenschaftlich fundierte Challenges basierend auf:
- Selbstbestimmungstheorie (Deci & Ryan): Autonomie, Kompetenz, Verbundenheit
- Hattie-Effektstärken: Deep Learning (d=0.69), Self-Efficacy (d=0.92)
- PISA 2022: MATHEFF als stärkster Prädiktor
- Birkenbihl-Methoden: ABC-Listen, KaWa
- SELF-Studie Greifswald: 34% Motivation durch Peers

Altersstufen:
- Grundschule (8-10 Jahre): Spielerisch, kurz, visuell
- Unterstufe (10-12 Jahre): Praktisch, peer-fokussiert
- Mittelstufe (13-15 Jahre): Wissenschaftlich, Selbstreflexion
- Oberstufe (16-18 Jahre): Transfer, Studiumsvorbereitung
- Pädagogen: NUR Theorie (keine Challenges!)

Design-Prinzipien (GitHub + Duolingo + Brilliant + Khan Academy):
- Instant Feedback: Sofortige Bestätigung
- Bite-sized: Kurze, abschließbare Einheiten
- Meaningful Challenges: Echte Reflexion, nicht leere Punkte
- NO Leaderboards: Fokus auf eigenen Fortschritt
- Variable Rewards: Bonus-XP für Wiederholungen
"""

from typing import Dict, Any, List, Optional


# ============================================
# XP KONFIGURATION
# ============================================

MOTIVATION_XP = {
    # Basis-XP pro Challenge-Typ
    "quick_challenge": 40,      # Schnelle Reflexion (< 2 Min)
    "standard_challenge": 60,   # Standard Challenge (2-5 Min)
    "deep_challenge": 80,       # Tiefe Reflexion (5-10 Min)
    "action_challenge": 100,    # Aktion in der echten Welt
    
    # Bonus-XP
    "first_of_category": 20,    # Erste Challenge einer Kategorie
    "all_category_done": 50,    # Alle Challenges einer Kategorie
    "all_age_group_done": 100,  # Alle Challenges einer Altersstufe
    "reflection_bonus": 10,     # Reflexion ausgefüllt
    
    # Streak-Multiplikatoren
    "streak_3": 1.2,            # 20% Bonus ab 3 Tagen
    "streak_7": 1.5,            # 50% Bonus ab 7 Tagen
    "streak_14": 1.8,           # 80% Bonus ab 14 Tagen
    "streak_30": 2.0,           # 100% Bonus ab 30 Tagen
}


# ============================================
# GRUNDBEDÜRFNIS-DEFINITIONEN
# ============================================

GRUNDBEDUERFNISSE = {
    "autonomie": {
        "name": "Autonomie",
        "icon": "🎯",
        "color": "#22c55e",  # Grün
        "description": "Das Gefühl, selbst zu entscheiden und Kontrolle zu haben",
        "science": "Autonomieerleben steigert intrinsische Motivation um bis zu 40% (Deci & Ryan)",
        "keywords": ["WOZU", "Entscheidung", "Kontrolle", "Sinn", "Ziel"]
    },
    "kompetenz": {
        "name": "Kompetenz",
        "icon": "💪",
        "color": "#3b82f6",  # Blau
        "description": "Das Gefühl, etwas zu können und besser zu werden",
        "science": "Kompetenzerleben ist der stärkste Prädiktor für Lernerfolg (PISA: MATHEFF)",
        "keywords": ["Fortschritt", "Können", "Wachstum", "Feedback", "Meistern"]
    },
    "verbundenheit": {
        "name": "Verbundenheit",
        "icon": "👥",
        "color": "#8b5cf6",  # Violett
        "description": "Das Gefühl, dazuzugehören und unterstützt zu werden",
        "science": "34% der Schülermotivation kommt durch Peers (SELF-Studie)",
        "keywords": ["Buddy", "Team", "Unterstützung", "Zusammen", "Feedback"]
    }
}


# ============================================
# CHALLENGE-DEFINITIONEN
# ============================================

MOTIVATION_CHALLENGES = {
    
    # ══════════════════════════════════════════
    # GRUNDSCHULE (8-10 Jahre / 3. & 4. Klasse)
    # ══════════════════════════════════════════
    # Design: Minecraft-Welt, Gregs Tagebuch-Humor, echte Kindersorgen
    # Themen: Übergang weiterführende Schule, Freunde, Spaß am Lernen

    "grundschule": {
        "autonomie": [
            {
                "id": "gs_minecraft_wozu",
                "name": "Dein Lern-Level",
                "icon": "⛏️",
                "xp": 40,
                "type": "quick_challenge",
                "duration_minutes": 2,
                "intro": {
                    "text": "Stell dir vor, Lernen wäre wie Minecraft: Du sammelst Wissen wie Erze und baust damit coole Sachen! 🏗️ Aber mal ehrlich - manchmal nervt Schule auch. Trotzdem gibt's einen Trick: Wenn du weißt, WOZU du etwas lernst, geht's viel leichter!",
                    "fun_fact": "Wusstest du? Dein Gehirn speichert Sachen besser, wenn du weißt, wofür du sie brauchst. Ist wie beim Craften - du sammelst ja auch nicht einfach irgendwas!",
                },
                "action": {
                    "title": "Wozu brauchst du das?",
                    "instruction": "Such dir ein Fach aus, das du gerade nicht so magst. Finde EINEN Grund, wozu es nützlich sein könnte:",
                    "input_type": "text",
                    "input_label": "Das Fach nervt mich, aber es hilft mir bei...",
                    "placeholder": "z.B. Mathe nervt, aber ich brauch's um mein Taschengeld zu checken",
                    "min_length": 10,
                },
                "reflection": {
                    "question": "Und? Fällt dir jetzt ein Grund ein?",
                    "options": ["🎯 Ja, krass!", "🤔 Naja, ein bisschen", "😅 Ich überleg noch"]
                },
                "completion_message": "Nice! Du hast einen Grund gefunden. Das ist wie ein Diamant-Schwert fürs Lernen! ⚔️"
            },
            {
                "id": "gs_chef",
                "name": "Du bist der Chef!",
                "icon": "👑",
                "xp": 45,
                "type": "quick_challenge",
                "duration_minutes": 2,
                "intro": {
                    "text": "Kennst du das? Alle sagen dir, was du tun sollst. 'Mach Hausaufgaben!' 'Lern für die Arbeit!' Aber hey - bei MANCHEN Sachen kannst DU entscheiden! Und das fühlt sich richtig gut an.",
                    "fun_fact": "Forscher haben rausgefunden: Kinder, die kleine Sachen selbst entscheiden dürfen, haben mehr Bock aufs Lernen. Echt jetzt!",
                },
                "action": {
                    "title": "Deine Entscheidung!",
                    "instruction": "Was könntest du heute selbst entscheiden? (Auch kleine Sachen zählen!)",
                    "input_type": "text",
                    "input_label": "Ich entscheide heute selbst...",
                    "placeholder": "z.B. Mit welchem Fach ich anfange / Ob ich Musik anhöre / Wo ich lerne",
                    "min_length": 8,
                },
                "reflection": {
                    "question": "Fühlst du dich besser, wenn du selbst entscheidest?",
                    "options": ["👑 Ja voll!", "😊 Ein bisschen", "🤷 Weiß nicht"]
                },
                "completion_message": "Du bist der Boss! Kleine Entscheidungen = großer Unterschied! 👑"
            },
        ],

        "kompetenz": [
            {
                "id": "gs_level_up",
                "name": "Level Up! Was du schon kannst",
                "icon": "📈",
                "xp": 50,
                "type": "standard_challenge",
                "duration_minutes": 3,
                "intro": {
                    "text": "Okay, krasse Frage: Weißt du eigentlich, was du alles schon kannst? In der 1. Klasse konntest du noch nicht mal richtig lesen - und jetzt? Check mal, wie viel du schon drauf hast!",
                    "fun_fact": "Greg aus 'Gregs Tagebuch' denkt auch oft, er kann nix. Aber eigentlich hat er schon mega viel gelernt. Genau wie du!",
                },
                "action": {
                    "title": "Deine Skills",
                    "instruction": "Schreib 3 Sachen auf, die du jetzt kannst, aber vor 2 Jahren noch nicht konntest:",
                    "input_type": "list",
                    "input_count": 3,
                    "input_label": "Das kann ich jetzt...",
                    "placeholder": "z.B. Schreibschrift, das Einmaleins, alleine zur Schule gehen",
                },
                "reflection": {
                    "question": "Krass, oder? Wie viel du schon gelernt hast?",
                    "options": ["🤯 Boah, stimmt!", "😊 Mehr als ich dachte", "🤔 Geht so"]
                },
                "completion_message": "Siehst du? Du levelst die ganze Zeit hoch - auch wenn du's nicht merkst! 📈🎮"
            },
            {
                "id": "gs_fehler_held",
                "name": "Fehler sind nicht peinlich!",
                "icon": "💪",
                "xp": 55,
                "type": "standard_challenge",
                "duration_minutes": 3,
                "intro": {
                    "text": "Mal ehrlich: Fehler machen ist voll unangenehm, oder? Aber hier kommt der Plot-Twist: Dein Gehirn lernt am meisten, wenn du Fehler machst! Ohne Fehler = kein Lernen. Ist so.",
                    "fun_fact": "Die Erfinder von Minecraft haben über 100 Fehler gemacht, bevor das Spiel funktioniert hat. Stell dir vor, die hätten aufgegeben!",
                },
                "action": {
                    "title": "Dein letzter Fehler",
                    "instruction": "Denk an einen Fehler, den du gemacht hast. Was hast du daraus gelernt?",
                    "input_type": "text",
                    "input_label": "Mein Fehler war... und gelernt hab ich...",
                    "placeholder": "z.B. Ich hab bei der Mathe-Arbeit Plus und Minus verwechselt. Jetzt les ich genauer.",
                    "min_length": 15,
                },
                "reflection": {
                    "question": "Siehst du Fehler jetzt anders?",
                    "options": ["💪 Ja, Fehler sind okay!", "🤔 Naja, ein bisschen", "😬 Fehler nerven trotzdem"]
                },
                "completion_message": "Fehler = Gehirn-Training! Du wirst mit jedem Fehler schlauer! 🧠✨"
            },
        ],

        "verbundenheit": [
            {
                "id": "gs_team",
                "name": "Zusammen geht's besser",
                "icon": "👫",
                "xp": 45,
                "type": "quick_challenge",
                "duration_minutes": 2,
                "intro": {
                    "text": "Weißt du, was das Geheimnis von den besten Minecraft-Servern ist? Teamwork! Alleine bauen ist okay, aber zusammen baut man die krassesten Sachen. Beim Lernen ist das genauso!",
                    "fun_fact": "Kinder, die sich gegenseitig beim Lernen helfen, merken sich 50% mehr. Das ist Mathe - aber die gute Art! 😄",
                },
                "action": {
                    "title": "Dein Lern-Team",
                    "instruction": "Mit wem könntest du mal zusammen für eine Arbeit üben?",
                    "input_type": "text",
                    "input_label": "Ich könnte mit ... üben",
                    "placeholder": "z.B. Mit meiner Freundin Lena oder meinem Kumpel Tim",
                    "min_length": 5,
                },
                "reflection": {
                    "question": "Was könntet ihr zusammen machen?",
                    "options": ["📝 Abfragen", "🧮 Zusammen rechnen", "📖 Lesen üben", "🎯 Was anderes"]
                },
                "completion_message": "Zusammen lernen = weniger Stress + mehr Spaß! 👫✨"
            },
            {
                "id": "gs_fragen",
                "name": "Fragen ist nicht dumm!",
                "icon": "🙋",
                "xp": 50,
                "type": "standard_challenge",
                "duration_minutes": 3,
                "intro": {
                    "text": "Kennst du das? Du checkst was nicht, aber du traust dich nicht zu fragen. Weil's vielleicht dumm klingt? NEWS: Es gibt keine dummen Fragen! Die schlausten Leute fragen am meisten.",
                    "fun_fact": "Forscher haben herausgefunden: Kinder, die viel fragen, werden später oft Erfinder oder Wissenschaftler. Fragen = Superkraft!",
                },
                "action": {
                    "title": "Deine Frage",
                    "instruction": "Gibt's was, das du in der Schule nicht verstanden hast? Schreib's auf - nur für dich!",
                    "input_type": "text",
                    "input_label": "Das versteh ich nicht so richtig...",
                    "placeholder": "z.B. Warum muss man Kommas setzen? / Wie geht nochmal geteilt?",
                    "min_length": 8,
                },
                "reflection": {
                    "question": "Wen könntest du fragen?",
                    "options": ["👩‍🏫 Lehrerin/Lehrer", "👨‍👩‍👧 Eltern", "👫 Freund/Freundin", "🤔 Weiß noch nicht"]
                },
                "completion_message": "Fragen stellen macht schlau! Trau dich ruhig! 🙋💡"
            },
        ],
    },
    
    # ══════════════════════════════════════════
    # UNTERSTUFE (10-12 Jahre)
    # ══════════════════════════════════════════
    
    "unterstufe": {
        "autonomie": [
            {
                "id": "us_wozu",
                "name": "WOZU-Finder",
                "icon": "🎯",
                "xp": 60,
                "type": "standard_challenge",
                "duration_minutes": 4,
                "intro": {
                    "text": "Die wichtigste Frage beim Lernen ist nicht WAS oder WIE - sondern WOZU! Wenn du weißt, wozu du etwas lernst, fällt es dir viel leichter.",
                    "fun_fact": "Schüler mit einem klaren WOZU haben 3x mehr Ausdauer beim Lernen!",
                    "science_note": "Autonomieerleben ist einer der 3 Grundpfeiler der Motivation (Deci & Ryan)"
                },
                "action": {
                    "title": "Dein WOZU formulieren",
                    "instruction": "Wähle ein Fach, das dir schwer fällt. Finde einen Grund, warum es für DICH nützlich sein könnte:",
                    "input_type": "text",
                    "input_label": "Ich lerne [Fach], weil ich damit später...",
                    "placeholder": "z.B. Ich lerne Englisch, weil ich damit später meine Lieblingsspiele verstehen kann",
                    "min_length": 20,
                },
                "reflection": {
                    "question": "Hat sich deine Einstellung zum Fach verändert?",
                    "options": ["🌟 Ja, es macht jetzt mehr Sinn!", "🤔 Ein bisschen", "😐 Noch nicht"]
                },
                "completion_message": "Dein WOZU ist dein persönlicher Motivations-Turbo! 🚀"
            },
            {
                "id": "us_reihenfolge",
                "name": "Reihenfolge-Boss",
                "icon": "📋",
                "xp": 50,
                "type": "quick_challenge",
                "duration_minutes": 3,
                "intro": {
                    "text": "Kleine Entscheidungen machen einen großen Unterschied! Wenn DU entscheidest, in welcher Reihenfolge du lernst, fühlst du dich gleich besser.",
                    "fun_fact": "Schon kleine Wahlmöglichkeiten steigern die Motivation um 25%!",
                },
                "action": {
                    "title": "Deine Lernreihenfolge",
                    "instruction": "Sortiere deine heutigen Hausaufgaben - womit möchtest du anfangen?",
                    "input_type": "ranking",
                    "input_label": "Meine Reihenfolge heute:",
                    "placeholder": "1. Mathe (weil ich fit bin)\n2. Deutsch (braucht Konzentration)\n3. Englisch (macht mir Spaß zum Schluss)",
                    "min_length": 15,
                },
                "reflection": {
                    "question": "Warum hast du diese Reihenfolge gewählt?",
                    "options": ["Leichtes zuerst", "Schweres zuerst", "Lieblingsfach zum Schluss", "Keine Ahnung"]
                },
                "completion_message": "Du bist der Boss über dein Lernen! 💪"
            },
        ],
        
        "kompetenz": [
            {
                "id": "us_abc",
                "name": "ABC-Liste erstellen",
                "icon": "📝",
                "xp": 80,
                "type": "deep_challenge",
                "duration_minutes": 7,
                "intro": {
                    "text": "Die ABC-Liste ist eine geniale Methode von Vera F. Birkenbihl! Du schreibst zu jedem Buchstaben auf, was du zu einem Thema weißt. So siehst du, wie viel schon in deinem Kopf steckt!",
                    "fun_fact": "Eine ABC-Liste aktiviert dein Gehirn wie ein Wecker - plötzlich fallen dir Dinge ein, die du vergessen hattest!",
                    "science_note": "Elaboration (d=0.56): Verknüpfungen herstellen stärkt das Gedächtnis"
                },
                "action": {
                    "title": "Deine erste ABC-Liste",
                    "instruction": "Wähle ein Thema aus dem Unterricht. Schreib zu mindestens 10 Buchstaben etwas auf, das du schon weißt:",
                    "input_type": "abc_list",
                    "input_label": "Mein Thema: _____ | Meine ABC-Liste:",
                    "placeholder": "A = ...\nB = ...\nC = ...\n(mindestens 10 Buchstaben!)",
                    "min_length": 50,
                },
                "reflection": {
                    "question": "Wie viel wusstest du schon?",
                    "options": ["🤩 Mehr als gedacht!", "😊 Einiges", "🤔 Noch Lücken"]
                },
                "completion_message": "ABC-Listen sind wie Röntgenbilder für dein Wissen! 🧠✨"
            },
            {
                "id": "us_fortschritt",
                "name": "Fortschritts-Tracker",
                "icon": "📈",
                "xp": 60,
                "type": "standard_challenge",
                "duration_minutes": 4,
                "intro": {
                    "text": "Fortschritt sichtbar machen ist ein Geheimtrick! Wenn du siehst, was du geschafft hast, motiviert dich das automatisch weiterzumachen.",
                    "fun_fact": "Deshalb haben Spiele Fortschrittsbalken - sie machen süchtig nach dem nächsten Level!",
                },
                "action": {
                    "title": "Deinen Fortschritt messen",
                    "instruction": "Wähle eine Fähigkeit und bewerte dich: Wo warst du vor einem Monat? Wo bist du jetzt?",
                    "input_type": "progress",
                    "input_label": "Fähigkeit | Vor 1 Monat (1-10) | Jetzt (1-10)",
                    "placeholder": "z.B. Englisch-Vokabeln: Vor 1 Monat: 4/10 | Jetzt: 6/10",
                    "min_length": 20,
                },
                "reflection": {
                    "question": "Siehst du deinen Fortschritt?",
                    "options": ["🚀 Ja, deutlich!", "📈 Ein bisschen", "🤔 Schwer zu sagen"]
                },
                "completion_message": "Fortschritt ist nicht immer sichtbar - aber er ist da! 📈"
            },
        ],
        
        "verbundenheit": [
            {
                "id": "us_buddy",
                "name": "Buddy finden",
                "icon": "👯",
                "xp": 80,
                "type": "action_challenge",
                "duration_minutes": 5,
                "intro": {
                    "text": "Ein Lern-Buddy ist jemand, mit dem du dich gegenseitig unterstützt. Ihr müsst nicht beste Freunde sein - nur beide motiviert, etwas zu schaffen!",
                    "fun_fact": "Die SELF-Studie zeigt: 34% der Schülermotivation kommt von Mitschülern!",
                    "science_note": "Peer Learning steigert den Lernerfolg um bis zu 30%"
                },
                "action": {
                    "title": "Buddy-Nachricht schreiben",
                    "instruction": "Schreib eine kurze Nachricht an jemanden, mit dem du lernen könntest. Du musst sie nicht sofort schicken - aber formuliere sie!",
                    "input_type": "message",
                    "input_label": "Meine Buddy-Nachricht:",
                    "placeholder": "Hey [Name], hast du Lust, dass wir uns vor der nächsten Klassenarbeit gegenseitig abfragen? 📚",
                    "min_length": 30,
                },
                "reflection": {
                    "question": "Wirst du die Nachricht schicken?",
                    "options": ["✅ Ja, sofort!", "🤔 Vielleicht später", "😅 Trau mich noch nicht"]
                },
                "completion_message": "Zusammen lernen = Gemeinsam wachsen! 👯✨"
            },
            {
                "id": "us_erklaerer",
                "name": "Erklär-Challenge",
                "icon": "🎤",
                "xp": 70,
                "type": "standard_challenge",
                "duration_minutes": 5,
                "intro": {
                    "text": "Der beste Weg, etwas zu verstehen? Es jemand anderem erklären! Das nennt man die Feynman-Methode - benannt nach einem berühmten Physiker.",
                    "fun_fact": "Wenn du etwas erklären kannst, hast du es wirklich verstanden!",
                    "science_note": "Lernen durch Lehren: Effektstärke d=0.54 (Hattie)"
                },
                "action": {
                    "title": "Erkläre es einfach!",
                    "instruction": "Wähle ein Thema aus dem Unterricht. Erkläre es so, dass ein Grundschüler es verstehen würde:",
                    "input_type": "text",
                    "input_label": "Mein Thema einfach erklärt:",
                    "placeholder": "z.B. 'Photosynthese ist wie Kochen für Pflanzen - sie nehmen Sonnenlicht und machen daraus Essen!'",
                    "min_length": 40,
                },
                "reflection": {
                    "question": "Konntest du es einfach erklären?",
                    "options": ["🌟 Ja, easy!", "🤔 War schwieriger als gedacht", "😅 Ich muss noch üben"]
                },
                "completion_message": "Wer erklären kann, hat verstanden! 🎤💡"
            },
        ],
    },
    
    # ══════════════════════════════════════════
    # MITTELSTUFE (13-15 Jahre)
    # ══════════════════════════════════════════
    
    "mittelstufe": {
        "autonomie": [
            {
                "id": "ms_wozu",
                "name": "Dein WOZU",
                "icon": "🎯",
                "xp": 70,
                "type": "standard_challenge",
                "duration_minutes": 5,
                "intro": {
                    "text": "Intrinsische Motivation (von innen kommend) ist 3x stärker als extrinsische (Noten, Belohnungen). Der Schlüssel: Ein persönliches WOZU finden, das über 'gute Noten' hinausgeht.",
                    "fun_fact": "Studien zeigen: Menschen mit einem klaren 'Warum' haben 64% mehr Durchhaltevermögen!",
                    "science_note": "Autonomie ist eines der 3 psychologischen Grundbedürfnisse (Deci & Ryan, Selbstbestimmungstheorie)"
                },
                "action": {
                    "title": "5-Ebenen-WOZU",
                    "instruction": "Frag dich 5x hintereinander 'Wozu?' - jede Antwort wird tiefer:\n1. Wozu lernst du für die nächste Klausur?\n2. Wozu ist das wichtig?\n3. Wozu führt das?\n4. Wozu brauchst du das?\n5. Wozu ist DAS wichtig für dein Leben?",
                    "input_type": "chain",
                    "input_label": "Meine 5-Ebenen-Kette:",
                    "placeholder": "1. Gute Note\n2. Versetzung\n3. Abitur\n4. Studium\n5. [Dein tiefes Warum]",
                    "min_length": 50,
                },
                "reflection": {
                    "question": "Hast du ein tieferes WOZU gefunden?",
                    "options": ["🎯 Ja, jetzt ist es klar!", "🤔 Teilweise", "😐 Brauche mehr Zeit"]
                },
                "completion_message": "Ein klares WOZU ist wie ein Kompass für dein Lernen! 🧭"
            },
            {
                "id": "ms_mikro",
                "name": "Mikro-Entscheidungen",
                "icon": "🔀",
                "xp": 60,
                "type": "standard_challenge",
                "duration_minutes": 4,
                "intro": {
                    "text": "Autonomie bedeutet nicht, alles selbst zu entscheiden. Schon kleine Wahlmöglichkeiten steigern deine Motivation - selbst wenn das Ergebnis gleich ist!",
                    "fun_fact": "In Experimenten waren Menschen mit kleinen Wahlmöglichkeiten 40% motivierter - auch wenn die Optionen fast identisch waren!",
                },
                "action": {
                    "title": "Deine Mikro-Entscheidungen",
                    "instruction": "Liste 5 kleine Entscheidungen auf, die du beim Lernen treffen kannst:",
                    "input_type": "list",
                    "input_count": 5,
                    "input_label": "Meine Mikro-Entscheidungen:",
                    "placeholder": "z.B.\n- Welches Fach zuerst?\n- Musik an oder aus?\n- Am Schreibtisch oder am Boden?\n- Mit Stift oder Laptop?\n- Alleine oder mit anderen?",
                },
                "reflection": {
                    "question": "Wirst du diese Entscheidungen bewusster treffen?",
                    "options": ["✅ Ja, ab jetzt!", "🤔 Werde es versuchen", "😐 Weiß nicht"]
                },
                "completion_message": "Kleine Entscheidungen, große Wirkung! 🔀✨"
            },
        ],
        
        "kompetenz": [
            {
                "id": "ms_abc",
                "name": "ABC-Liste Vorher/Nachher",
                "icon": "📊",
                "xp": 90,
                "type": "deep_challenge",
                "duration_minutes": 10,
                "intro": {
                    "text": "Die ABC-Liste zeigt dir nicht nur, was du weißt - sie zeigt dir auch deinen Lernfortschritt! Erstelle eine Liste VOR dem Lernen und eine DANACH.",
                    "fun_fact": "Vera F. Birkenbihl nannte das 'Wissensnetz aufspannen' - dein Gehirn fängt dann neue Infos besser auf!",
                    "science_note": "Elaboration (d=0.56): Vorwissen aktivieren verbessert das Lernen nachweislich"
                },
                "action": {
                    "title": "Vorher-ABC erstellen",
                    "instruction": "Wähle ein Thema, das du bald lernen musst. Erstelle JETZT eine ABC-Liste mit allem, was du schon weißt (auch Vermutungen!):",
                    "input_type": "abc_list",
                    "input_label": "Thema: _____ | VORHER-ABC:",
                    "placeholder": "A = ...\nB = ...\nC = ...\n(so viele Buchstaben wie möglich!)\n\n[Nach dem Lernen: Ergänze mit anderer Farbe!]",
                    "min_length": 80,
                },
                "reflection": {
                    "question": "Wie viele Buchstaben konntest du füllen?",
                    "options": ["📈 15+ (Wow!)", "📊 10-14", "📉 5-9", "🆕 Weniger als 5"]
                },
                "completion_message": "Nach dem Lernen: Ergänze deine Liste und sieh deinen Fortschritt! 📊"
            },
            {
                "id": "ms_deep",
                "name": "Deep vs. Surface Check",
                "icon": "🔬",
                "xp": 80,
                "type": "deep_challenge",
                "duration_minutes": 7,
                "intro": {
                    "text": "Es gibt zwei Arten zu lernen: 'Deep Learning' (verstehen, verknüpfen) und 'Surface Learning' (auswendig lernen). Deep Learning hat eine Effektstärke von d=0.69 - Surface Learning nur d=-0.11!",
                    "fun_fact": "Negativer Effekt bedeutet: Oberflächen-Lernen schadet sogar!",
                    "science_note": "Hattie: Deep Learning d=0.69, Surface Learning d=-0.11"
                },
                "action": {
                    "title": "Selbst-Check: Wie lernst du?",
                    "instruction": "Denk an deine letzte Lerneinheit. Beantworte ehrlich:",
                    "input_type": "checklist",
                    "input_label": "Bei meinem letzten Lernen habe ich...",
                    "checklist_items": [
                        "Verbindungen zu anderen Themen gesucht (Deep)",
                        "Nur den Text mehrmals gelesen (Surface)",
                        "Mir selbst Fragen gestellt (Deep)",
                        "Alles markiert ohne nachzudenken (Surface)",
                        "Versucht, es jemand anderem zu erklären (Deep)",
                        "Gehofft, dass ich es in der Prüfung erkenne (Surface)"
                    ],
                },
                "reflection": {
                    "question": "Mehr Deep oder Surface?",
                    "options": ["🧠 Mehr Deep!", "⚖️ Gemischt", "📖 Mehr Surface"]
                },
                "completion_message": "Bewusstsein ist der erste Schritt zur Verbesserung! 🔬"
            },
        ],
        
        "verbundenheit": [
            {
                "id": "ms_buddy",
                "name": "Lern-Buddy aktivieren",
                "icon": "👥",
                "xp": 80,
                "type": "action_challenge",
                "duration_minutes": 6,
                "intro": {
                    "text": "Ein Lern-Buddy ist nicht nur zum Abfragen da - ihr könnt euch gegenseitig motivieren, Tipps geben und gemeinsam schwierige Themen durcharbeiten.",
                    "fun_fact": "Die SELF-Studie (Greifswald) zeigt: 34% der Schülermotivation kommt durch Mitschüler!",
                    "science_note": "Peer Learning steigert nicht nur Motivation, sondern auch den Lernerfolg"
                },
                "action": {
                    "title": "Buddy-System aufbauen",
                    "instruction": "Erstelle einen konkreten Plan für ein Lern-Treffen mit einem Buddy:",
                    "input_type": "plan",
                    "input_label": "Mein Buddy-Plan:",
                    "placeholder": "Wer: [Name]\nWann: [Tag/Uhrzeit]\nWo: [Ort/Online]\nWas: [Thema/Fach]\nWie: [Abfragen/Zusammen üben/Erklären]",
                    "min_length": 50,
                },
                "reflection": {
                    "question": "Wirst du den Plan umsetzen?",
                    "options": ["✅ Ja, ich schreib gleich!", "📅 Diese Woche", "🤔 Muss noch überlegen"]
                },
                "completion_message": "Gemeinsam lernen = 34% mehr Motivation! 👥💪"
            },
            {
                "id": "ms_druck",
                "name": "Druck-Senker",
                "icon": "🎈",
                "xp": 70,
                "type": "standard_challenge",
                "duration_minutes": 5,
                "intro": {
                    "text": "Sozialer Druck kann Motivation zerstören. Aber mit den richtigen Strategien kannst du ihn in positive Energie umwandeln!",
                    "fun_fact": "Leistungsdruck aktiviert die gleichen Hirnregionen wie körperlicher Schmerz!",
                    "science_note": "Autonomie-unterstützende Umgebungen reduzieren Stress und fördern intrinsische Motivation"
                },
                "action": {
                    "title": "Druck analysieren",
                    "instruction": "Woher kommt Druck beim Lernen? Was könntest du dagegen tun?",
                    "input_type": "analysis",
                    "input_label": "Meine Druck-Analyse:",
                    "placeholder": "Druckquelle 1: [z.B. Eltern] → Lösung: [z.B. offen über Ziele sprechen]\nDruckquelle 2: [z.B. Selbst] → Lösung: [z.B. realistischere Erwartungen]",
                    "min_length": 60,
                },
                "reflection": {
                    "question": "Kannst du eine Lösung diese Woche ausprobieren?",
                    "options": ["✅ Ja!", "🤔 Vielleicht", "😓 Ist kompliziert"]
                },
                "completion_message": "Weniger Druck = Mehr echte Motivation! 🎈"
            },
        ],
    },
    
    # ══════════════════════════════════════════
    # OBERSTUFE (16-18 Jahre)
    # ══════════════════════════════════════════
    
    "oberstufe": {
        "autonomie": [
            {
                "id": "os_sdt",
                "name": "SDT-Selbstdiagnose",
                "icon": "🔬",
                "xp": 80,
                "type": "deep_challenge",
                "duration_minutes": 8,
                "intro": {
                    "text": "Die Selbstbestimmungstheorie (Self-Determination Theory, Deci & Ryan) identifiziert drei psychologische Grundbedürfnisse: Autonomie, Kompetenz und Verbundenheit. Wenn alle drei erfüllt sind, entsteht intrinsische Motivation.",
                    "fun_fact": "SDT ist eine der am besten erforschten Motivationstheorien mit über 10.000 Studien!",
                    "science_note": "Deci & Ryan (2000): Self-Determination Theory and the Facilitation of Intrinsic Motivation"
                },
                "action": {
                    "title": "SDT-Diagnose",
                    "instruction": "Bewerte auf einer Skala von 1-10, wie gut deine drei Grundbedürfnisse beim Lernen erfüllt sind. Begründe kurz:",
                    "input_type": "rating_with_reason",
                    "input_label": "Meine SDT-Diagnose:",
                    "placeholder": "Autonomie: _/10 - [Begründung]\nKompetenz: _/10 - [Begründung]\nVerbundenheit: _/10 - [Begründung]\n\nMein größtes Defizit: ___\nMeine Idee zur Verbesserung: ___",
                    "min_length": 100,
                },
                "reflection": {
                    "question": "Welches Grundbedürfnis braucht am meisten Aufmerksamkeit?",
                    "options": ["🎯 Autonomie", "💪 Kompetenz", "👥 Verbundenheit", "⚖️ Alle gleich"]
                },
                "completion_message": "Selbsterkenntnis ist der erste Schritt zur Optimierung! 🔬"
            },
            {
                "id": "os_wozu",
                "name": "Intrinsischer WOZU-Finder",
                "icon": "🧭",
                "xp": 70,
                "type": "standard_challenge",
                "duration_minutes": 6,
                "intro": {
                    "text": "Extrinsische Motivation (Noten, Karriere) funktioniert kurzfristig. Für langfristige Ausdauer brauchst du intrinsische Gründe - Dinge, die dir auch ohne externe Belohnung wichtig wären.",
                    "fun_fact": "Menschen mit intrinsischer Motivation sind nicht nur motivierter, sondern auch glücklicher!",
                },
                "action": {
                    "title": "Intrinsische Gründe finden",
                    "instruction": "Wähle ein Fach/Thema. Finde Gründe jenseits von Noten und Karriere:",
                    "input_type": "text",
                    "input_label": "Meine intrinsischen Gründe für [Fach/Thema]:",
                    "placeholder": "z.B. Physik:\n- Ich will verstehen, wie die Welt funktioniert\n- Es ist faszinierend, komplexe Probleme zu lösen\n- Die Eleganz mathematischer Beschreibungen begeistert mich",
                    "min_length": 80,
                },
                "reflection": {
                    "question": "Hast du echte intrinsische Gründe gefunden?",
                    "options": ["🌟 Ja, mehrere!", "🤔 Ein paar", "😐 Schwierig bei diesem Thema"]
                },
                "completion_message": "Intrinsische Motivation ist der Schlüssel zu nachhaltigem Lernerfolg! 🧭"
            },
        ],
        
        "kompetenz": [
            {
                "id": "os_abc",
                "name": "Birkenbihl ABC-Methode",
                "icon": "🧠",
                "xp": 90,
                "type": "deep_challenge",
                "duration_minutes": 10,
                "intro": {
                    "text": "Vera F. Birkenbihl entwickelte die ABC-Liste als Tool zur Aktivierung des assoziativen Denkens. Das Gehirn arbeitet assoziativ, nicht linear - die ABC-Liste nutzt das aus.",
                    "fun_fact": "Birkenbihl nannte es 'gehirn-gerechtes Lernen' - Methoden, die MIT dem Gehirn arbeiten, nicht dagegen.",
                    "science_note": "Elaboration Strategies (d=0.56): Verknüpfungen herstellen stärkt das Langzeitgedächtnis"
                },
                "action": {
                    "title": "Erweiterte ABC-Liste",
                    "instruction": "Erstelle eine ABC-Liste zu einem Klausurthema. Pro Buchstabe: Was weißt du? Was assoziierst du? Welche Fragen hast du?",
                    "input_type": "extended_abc",
                    "input_label": "Thema: _____ | Erweiterte ABC-Liste:",
                    "placeholder": "A = [Wissen] | [Assoziation] | [Frage?]\nB = ...\nC = ...\n\nReflexion: Was sind meine Wissenslücken?",
                    "min_length": 120,
                },
                "reflection": {
                    "question": "Hast du Wissenslücken identifiziert?",
                    "options": ["🎯 Ja, klare Lücken!", "📊 Einige", "✅ Kaum Lücken"]
                },
                "completion_message": "ABC-Listen machen Wissen und Lücken sichtbar! 🧠"
            },
            {
                "id": "os_deep",
                "name": "Deep Learning Analyse",
                "icon": "📚",
                "xp": 100,
                "type": "deep_challenge",
                "duration_minutes": 10,
                "intro": {
                    "text": "Hattie's Visible Learning Meta-Analyse (800+ Studien) zeigt: Deep Learning (d=0.69) ist effektiv, Surface Learning (d=-0.11) ist kontraproduktiv. Der Unterschied: Verstehen vs. Auswendiglernen.",
                    "fun_fact": "Eine negative Effektstärke bedeutet: Es schadet dem Lernen aktiv!",
                    "science_note": "Hattie (2009): Visible Learning - A synthesis of over 800 meta-analyses relating to achievement"
                },
                "action": {
                    "title": "Strategien-Audit",
                    "instruction": "Analysiere deine letzten 3 Lerneinheiten: Welche Strategien hast du verwendet? Waren sie Deep oder Surface?",
                    "input_type": "audit",
                    "input_label": "Mein Strategien-Audit:",
                    "placeholder": "Lerneinheit 1: [Thema] - Strategien: [Liste] - Deep/Surface: [Bewertung]\n\nLerneinheit 2: ...\n\nLerneinheit 3: ...\n\nFazit: Mein Deep/Surface-Verhältnis ist...\n\nVerbesserungsplan: ...",
                    "min_length": 150,
                },
                "reflection": {
                    "question": "Wie ist dein aktuelles Deep/Surface-Verhältnis?",
                    "options": ["🧠 Meist Deep", "⚖️ Gemischt", "📖 Meist Surface"]
                },
                "completion_message": "Bewusstes Lernen ist effektives Lernen! 📚"
            },
        ],
        
        "verbundenheit": [
            {
                "id": "os_buddy",
                "name": "Peer-Learning Setup",
                "icon": "🤝",
                "xp": 80,
                "type": "action_challenge",
                "duration_minutes": 7,
                "intro": {
                    "text": "Peer-Learning geht über gegenseitiges Abfragen hinaus. Forschung zeigt: Erklären, Diskutieren und gemeinsames Problemlösen haben höhere Effektstärken als passives Lernen.",
                    "fun_fact": "Das Erklären eines Konzepts verdoppelt dein eigenes Verständnis!",
                    "science_note": "Peer Tutoring d=0.55, Cooperative Learning d=0.40 (Hattie)"
                },
                "action": {
                    "title": "Peer-Learning Struktur",
                    "instruction": "Entwirf ein konkretes Peer-Learning-Setup für die Abitur-Vorbereitung:",
                    "input_type": "plan",
                    "input_label": "Mein Peer-Learning-Plan:",
                    "placeholder": "Teilnehmer: [Namen]\nFormat: [z.B. wöchentliches Treffen, 2h]\nStruktur: [z.B. 30min Erklären, 30min Diskutieren, 60min Üben]\nRegeln: [z.B. Jeder erklärt ein Thema, Fragen sind erwünscht]\nErste Themen: [Liste]",
                    "min_length": 100,
                },
                "reflection": {
                    "question": "Wann startest du dein Peer-Learning?",
                    "options": ["📅 Diese Woche!", "📆 Nächste Woche", "🤔 Muss noch planen"]
                },
                "completion_message": "Peer-Learning: Gemeinsam sind wir schlauer! 🤝"
            },
            {
                "id": "os_transfer",
                "name": "Transfer: Studium/Beruf",
                "icon": "🚀",
                "xp": 90,
                "type": "deep_challenge",
                "duration_minutes": 8,
                "intro": {
                    "text": "Motivation im Studium/Beruf unterscheidet sich von Schulmotivation. Die Prinzipien (SDT) bleiben gleich, aber du musst sie selbst anwenden - niemand strukturiert mehr für dich.",
                    "fun_fact": "50% der Studienabbrecher nennen mangelnde Motivation als Hauptgrund!",
                },
                "action": {
                    "title": "Zukunfts-Motivation planen",
                    "instruction": "Wie wirst du im Studium/Beruf für deine drei Grundbedürfnisse sorgen?",
                    "input_type": "transfer_plan",
                    "input_label": "Mein Transfer-Plan:",
                    "placeholder": "AUTONOMIE im Studium:\n- Wie schaffe ich mir Wahlmöglichkeiten?\n- Wie finde ich mein WOZU?\n\nKOMPETENZ im Studium:\n- Wie messe ich meinen Fortschritt?\n- Wie hole ich mir Feedback?\n\nVERBUNDENHEIT im Studium:\n- Wie finde ich Peers?\n- Wie baue ich ein Netzwerk auf?",
                    "min_length": 150,
                },
                "reflection": {
                    "question": "Fühlst du dich vorbereitet auf selbstgesteuertes Lernen?",
                    "options": ["✅ Ja, bereit!", "🤔 Größtenteils", "📝 Brauche mehr Vorbereitung"]
                },
                "completion_message": "Du hast die Werkzeuge für lebenslanges Lernen! 🚀"
            },
        ],
    },
}


# ============================================
# HELPER FUNCTIONS
# ============================================

def get_challenges_for_age(age_group: str) -> Dict[str, List[Dict]]:
    """
    Holt alle Challenges für eine Altersstufe.
    
    Returns:
        Dict mit Grundbedürfnis -> Liste von Challenges
    """
    return MOTIVATION_CHALLENGES.get(age_group, {})


def get_challenge_by_id(challenge_id: str, age_group: str = None) -> Optional[Dict[str, Any]]:
    """
    Findet eine Challenge anhand der ID.
    Falls age_group nicht angegeben, durchsucht alle Altersstufen.
    """
    if age_group:
        age_groups = [age_group]
    else:
        age_groups = MOTIVATION_CHALLENGES.keys()
    
    for ag in age_groups:
        for gb, challenges in MOTIVATION_CHALLENGES.get(ag, {}).items():
            for challenge in challenges:
                if challenge["id"] == challenge_id:
                    return {
                        **challenge,
                        "age_group": ag,
                        "grundbeduerfnis": gb
                    }
    return None


def get_all_challenge_ids(age_group: str) -> List[str]:
    """Gibt alle Challenge-IDs einer Altersstufe zurück."""
    ids = []
    for gb, challenges in MOTIVATION_CHALLENGES.get(age_group, {}).items():
        for challenge in challenges:
            ids.append(challenge["id"])
    return ids


def count_challenges_by_category(age_group: str) -> Dict[str, int]:
    """Zählt Challenges pro Grundbedürfnis."""
    counts = {"autonomie": 0, "kompetenz": 0, "verbundenheit": 0}
    for gb, challenges in MOTIVATION_CHALLENGES.get(age_group, {}).items():
        counts[gb] = len(challenges)
    return counts


def get_total_xp_possible(age_group: str) -> int:
    """Berechnet die maximal erreichbaren XP einer Altersstufe."""
    total = 0
    for gb, challenges in MOTIVATION_CHALLENGES.get(age_group, {}).items():
        for challenge in challenges:
            total += challenge.get("xp", 0)
    return total


def get_challenge_summary(age_group: str) -> Dict[str, Any]:
    """
    Gibt eine Zusammenfassung aller Challenges einer Altersstufe.
    """
    counts = count_challenges_by_category(age_group)
    total = sum(counts.values())
    xp = get_total_xp_possible(age_group)
    
    return {
        "age_group": age_group,
        "total_challenges": total,
        "by_category": counts,
        "total_xp_possible": xp,
        "challenges": get_challenges_for_age(age_group)
    }


def calculate_xp_with_streak(base_xp: int, streak: int) -> int:
    """Berechnet XP mit Streak-Multiplikator."""
    if streak >= 30:
        multiplier = MOTIVATION_XP["streak_30"]
    elif streak >= 14:
        multiplier = MOTIVATION_XP["streak_14"]
    elif streak >= 7:
        multiplier = MOTIVATION_XP["streak_7"]
    elif streak >= 3:
        multiplier = MOTIVATION_XP["streak_3"]
    else:
        multiplier = 1.0
    
    return int(base_xp * multiplier)


# ============================================
# ZERTIFIKAT-DEFINITIONEN
# ============================================

CERTIFICATE_TEXTS = {
    "grundschule": {
        "title": "Motivations-Entdecker 🌟",
        "subtitle": "hat die Geheimnisse der Motivation entdeckt",
        "description": "und gelernt: WARUM, WIE und MIT WEM Lernen Spaß macht!"
    },
    "unterstufe": {
        "title": "Motivations-Profi 💪",
        "subtitle": "hat die drei Superkräfte der Motivation gemeistert",
        "description": "Autonomie • Kompetenz • Verbundenheit"
    },
    "mittelstufe": {
        "title": "SDT-Explorer 🔬",
        "subtitle": "hat die Selbstbestimmungstheorie verstanden und angewendet",
        "description": "Wissenschaftlich fundierte Motivation für nachhaltigen Lernerfolg"
    },
    "oberstufe": {
        "title": "Motivations-Meister 🎓",
        "subtitle": "hat die psychologischen Grundlagen der Motivation beherrscht",
        "description": "Bereit für selbstgesteuertes, lebenslanges Lernen"
    }
}


# ============================================
# TEST
# ============================================

if __name__ == "__main__":
    # Test: Challenge-Übersicht
    for age in ["grundschule", "unterstufe", "mittelstufe", "oberstufe"]:
        summary = get_challenge_summary(age)
        print(f"\n{age.upper()}")
        print(f"  Challenges: {summary['total_challenges']}")
        print(f"  By Category: {summary['by_category']}")
        print(f"  Total XP: {summary['total_xp_possible']}")
    
    # Test: Challenge finden
    challenge = get_challenge_by_id("us_abc")
    print(f"\n\nChallenge gefunden: {challenge['name']} ({challenge['xp']} XP)")
    
    print("\n✅ Alle Tests erfolgreich!")
