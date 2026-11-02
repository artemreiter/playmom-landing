# -*- coding: utf-8 -*-
"""Localized UI strings and slugs for the PlayMom programmatic SEO site.
Hand-written per language (not machine translated at build time). Short,
common phrases only (age, goal, steps, materials, safety, home, download).
No em or en dashes anywhere in these values.
"""

LANGS = ["ru", "uk", "pl", "en", "de", "es", "fr", "it", "ro"]

LANG_NAME = {
    "ru": "Русский", "uk": "Українська", "pl": "Polski", "en": "English",
    "de": "Deutsch", "es": "Español", "fr": "Français", "it": "Italiano",
    "ro": "Română",
}

# html lang= attribute value (BCP47)
HTML_LANG = {
    "ru": "ru", "uk": "uk", "pl": "pl", "en": "en", "de": "de",
    "es": "es", "fr": "fr", "it": "it", "ro": "ro",
}

SITE_NAME = "PlayMom"

# Path segment for the games section, per language (ascii, url safe)
GAMES_WORD = {
    "ru": "igry", "uk": "ihry", "pl": "zabawy", "en": "games", "de": "spiele",
    "es": "juegos", "fr": "jeux", "it": "giochi", "ro": "jocuri",
}

# Path segment for the age hub, per language
AGE_WORD = {
    "ru": "vozrast", "uk": "vik", "pl": "wiek", "en": "age", "de": "alter",
    "es": "edad", "fr": "age", "it": "eta", "ro": "varsta",
}

# Path segment for the goal hub, per language
GOAL_WORD = {
    "ru": "tsel", "uk": "meta", "pl": "cel", "en": "goal", "de": "ziel",
    "es": "objetivo", "fr": "objectif", "it": "obiettivo", "ro": "scop",
}

# Display label for category types (goals), per language
CATEGORY_LABEL = {
    "THINKING": {"ru": "мышление", "uk": "мислення", "pl": "myślenie", "en": "thinking", "de": "Denken", "es": "pensamiento", "fr": "réflexion", "it": "pensiero", "ro": "gândire"},
    "EMOTIONS": {"ru": "эмоции", "uk": "емоції", "pl": "emocje", "en": "emotions", "de": "Emotionen", "es": "emociones", "fr": "émotions", "it": "emozioni", "ro": "emoții"},
    "GROSS_MOTOR": {"ru": "крупная моторика", "uk": "велика моторика", "pl": "motoryka duża", "en": "gross motor skills", "de": "Grobmotorik", "es": "motricidad gruesa", "fr": "motricité globale", "it": "motricità globale", "ro": "motricitate grosieră"},
    "FINE_MOTOR": {"ru": "мелкая моторика", "uk": "дрібна моторика", "pl": "motoryka mała", "en": "fine motor skills", "de": "Feinmotorik", "es": "motricidad fina", "fr": "motricité fine", "it": "motricità fine", "ro": "motricitate fină"},
    "INDEPENDENCE": {"ru": "самостоятельность", "uk": "самостійність", "pl": "samodzielność", "en": "independence", "de": "Selbstständigkeit", "es": "autonomía", "fr": "autonomie", "it": "autonomia", "ro": "independență"},
    "MOVEMENT": {"ru": "движение", "uk": "рух", "pl": "ruch", "en": "movement", "de": "Bewegung", "es": "movimiento", "fr": "mouvement", "it": "movimento", "ro": "mișcare"},
    "SPEECH": {"ru": "речь", "uk": "мовлення", "pl": "mowa", "en": "speech", "de": "Sprache", "es": "habla", "fr": "langage", "it": "linguaggio", "ro": "vorbire"},
    "ATTENTION": {"ru": "внимание", "uk": "увага", "pl": "uwaga", "en": "attention", "de": "Aufmerksamkeit", "es": "atención", "fr": "attention", "it": "attenzione", "ro": "atenție"},
    "SENSORY": {"ru": "сенсорика", "uk": "сенсорика", "pl": "zmysły", "en": "senses", "de": "Sinne", "es": "sentidos", "fr": "sens", "it": "sensi", "ro": "simțuri"},
}

# URL slug for category types, per language (ascii)
CATEGORY_SLUG = {
    "THINKING": {"ru": "myshlenie", "uk": "myslennya", "pl": "myslenie", "en": "thinking", "de": "denken", "es": "pensamiento", "fr": "reflexion", "it": "pensiero", "ro": "gandire"},
    "EMOTIONS": {"ru": "emotsii", "uk": "emotsii", "pl": "emocje", "en": "emotions", "de": "emotionen", "es": "emociones", "fr": "emotions", "it": "emozioni", "ro": "emotii"},
    "GROSS_MOTOR": {"ru": "krupnaya-motorika", "uk": "velyka-motoryka", "pl": "motoryka-duza", "en": "gross-motor", "de": "grobmotorik", "es": "motricidad-gruesa", "fr": "motricite-globale", "it": "motricita-globale", "ro": "motricitate-grosiera"},
    "FINE_MOTOR": {"ru": "melkaya-motorika", "uk": "dribna-motoryka", "pl": "motoryka-mala", "en": "fine-motor", "de": "feinmotorik", "es": "motricidad-fina", "fr": "motricite-fine", "it": "motricita-fine", "ro": "motricitate-fina"},
    "INDEPENDENCE": {"ru": "samostoyatelnost", "uk": "samostiynist", "pl": "samodzielnosc", "en": "independence", "de": "selbststaendigkeit", "es": "autonomia", "fr": "autonomie", "it": "autonomia", "ro": "independenta"},
    "MOVEMENT": {"ru": "dvizhenie", "uk": "rukh", "pl": "ruch", "en": "movement", "de": "bewegung", "es": "movimiento", "fr": "mouvement", "it": "movimento", "ro": "miscare"},
    "SPEECH": {"ru": "rech", "uk": "movlennya", "pl": "mowa", "en": "speech", "de": "sprache", "es": "habla", "fr": "langage", "it": "linguaggio", "ro": "vorbire"},
    "ATTENTION": {"ru": "vnimanie", "uk": "uvaga", "pl": "uwaga", "en": "attention", "de": "aufmerksamkeit", "es": "atencion", "fr": "attention", "it": "attenzione", "ro": "atentie"},
    "SENSORY": {"ru": "sensorika", "uk": "sensoryka", "pl": "zmysly", "en": "senses", "de": "sinne", "es": "sentidos", "fr": "sens", "it": "sensi", "ro": "simturi"},
}

# Age bands in months: key -> (min_months_inclusive, max_months_inclusive)
AGE_BANDS = [
    ("0-1", 0, 11),
    ("1-2", 12, 23),
    ("2-3", 24, 35),
    ("3-4", 36, 47),
    ("4-6", 48, 71),
    ("6-8", 72, 96),
]

AGE_BAND_LABEL = {
    "0-1": {"ru": "0-1 год", "uk": "0-1 рік", "pl": "0-1 rok", "en": "0-1 year", "de": "0-1 Jahr", "es": "0-1 año", "fr": "0-1 an", "it": "0-1 anno", "ro": "0-1 an"},
    "1-2": {"ru": "1-2 года", "uk": "1-2 роки", "pl": "1-2 lata", "en": "1-2 years", "de": "1-2 Jahre", "es": "1-2 años", "fr": "1-2 ans", "it": "1-2 anni", "ro": "1-2 ani"},
    "2-3": {"ru": "2-3 года", "uk": "2-3 роки", "pl": "2-3 lata", "en": "2-3 years", "de": "2-3 Jahre", "es": "2-3 años", "fr": "2-3 ans", "it": "2-3 anni", "ro": "2-3 ani"},
    "3-4": {"ru": "3-4 года", "uk": "3-4 роки", "pl": "3-4 lata", "en": "3-4 years", "de": "3-4 Jahre", "es": "3-4 años", "fr": "3-4 ans", "it": "3-4 anni", "ro": "3-4 ani"},
    "4-6": {"ru": "4-6 лет", "uk": "4-6 років", "pl": "4-6 lat", "en": "4-6 years", "de": "4-6 Jahre", "es": "4-6 años", "fr": "4-6 ans", "it": "4-6 anni", "ro": "4-6 ani"},
    "6-8": {"ru": "6-8 лет", "uk": "6-8 років", "pl": "6-8 lat", "en": "6-8 years", "de": "6-8 Jahre", "es": "6-8 años", "fr": "6-8 ans", "it": "6-8 anni", "ro": "6-8 ani"},
}

# Unit label appended after a numeral range on game pages.
MONTHS_LABEL = {"ru": "мес", "uk": "міс", "pl": "mies", "en": "months", "de": "Monate", "es": "meses", "fr": "mois", "it": "mesi", "ro": "luni"}
YEARS_LABEL = {"ru": "лет", "uk": "р", "pl": "lat", "en": "years", "de": "Jahre", "es": "años", "fr": "ans", "it": "anni", "ro": "ani"}
MINUTES_LABEL = {"ru": "мин", "uk": "хв", "pl": "min", "en": "min", "de": "Min.", "es": "min", "fr": "min", "it": "min", "ro": "min"}

# Generic UI strings
UI = {
    "home_breadcrumb": {"ru": "Главная", "uk": "Головна", "pl": "Strona główna", "en": "Home", "de": "Startseite", "es": "Inicio", "fr": "Accueil", "it": "Home", "ro": "Acasă"},
    "games_breadcrumb": {"ru": "Игры", "uk": "Ігри", "pl": "Zabawy", "en": "Games", "de": "Spiele", "es": "Juegos", "fr": "Jeux", "it": "Giochi", "ro": "Jocuri"},
    "by_age_heading": {"ru": "По возрасту", "uk": "За віком", "pl": "Według wieku", "en": "By age", "de": "Nach Alter", "es": "Por edad", "fr": "Par âge", "it": "Per età", "ro": "După vârstă"},
    "by_goal_heading": {"ru": "По цели развития", "uk": "За метою розвитку", "pl": "Według celu rozwoju", "en": "By development goal", "de": "Nach Förderziel", "es": "Por objetivo de desarrollo", "fr": "Par objectif de développement", "it": "Per obiettivo di sviluppo", "ro": "După scop de dezvoltare"},
    "steps_heading": {"ru": "Шаги игры", "uk": "Кроки гри", "pl": "Kroki zabawy", "en": "Steps", "de": "Schritte", "es": "Pasos", "fr": "Étapes", "it": "Passaggi", "ro": "Pași"},
    "materials_heading": {"ru": "Что понадобится", "uk": "Що знадобиться", "pl": "Co będzie potrzebne", "en": "What you need", "de": "Was du brauchst", "es": "Qué necesitas", "fr": "Ce qu'il vous faut", "it": "Cosa serve", "ro": "Ce ai nevoie"},
    "safety_heading": {"ru": "Безопасность", "uk": "Безпека", "pl": "Bezpieczeństwo", "en": "Safety", "de": "Sicherheit", "es": "Seguridad", "fr": "Sécurité", "it": "Sicurezza", "ro": "Siguranță"},
    "setup_heading": {"ru": "Подготовка", "uk": "Підготовка", "pl": "Przygotowanie", "en": "Setup", "de": "Vorbereitung", "es": "Preparación", "fr": "Préparation", "it": "Preparazione", "ro": "Pregătire"},
    "age_label": {"ru": "Возраст", "uk": "Вік", "pl": "Wiek", "en": "Age", "de": "Alter", "es": "Edad", "fr": "Âge", "it": "Età", "ro": "Vârstă"},
    "prep_minutes_label": {"ru": "мин. на подготовку", "uk": "хв. на підготовку", "pl": "min. przygotowania", "en": "min to set up", "de": "Min. Vorbereitung", "es": "min de preparación", "fr": "min de préparation", "it": "min di preparazione", "ro": "min de pregătire"},
    "related_games_heading": {"ru": "Похожие игры", "uk": "Схожі ігри", "pl": "Podobne zabawy", "en": "Related games", "de": "Ähnliche Spiele", "es": "Juegos relacionados", "fr": "Jeux similaires", "it": "Giochi simili", "ro": "Jocuri asemănătoare"},
    "all_ages_heading": {"ru": "Все возрасты", "uk": "Усі вікові групи", "pl": "Wszystkie grupy wiekowe", "en": "All ages", "de": "Alle Altersgruppen", "es": "Todas las edades", "fr": "Tous les âges", "it": "Tutte le età", "ro": "Toate vârstele"},
    "all_goals_heading": {"ru": "Все цели развития", "uk": "Усі цілі розвитку", "pl": "Wszystkie cele rozwoju", "en": "All development goals", "de": "Alle Förderziele", "es": "Todos los objetivos", "fr": "Tous les objectifs", "it": "Tutti gli obiettivi", "ro": "Toate scopurile"},
    "cta_button": {"ru": "Открыть в приложении", "uk": "Відкрити в застосунку", "pl": "Otwórz w aplikacji", "en": "Open in the app", "de": "In der App öffnen", "es": "Abrir en la app", "fr": "Ouvrir dans l'application", "it": "Apri nell'app", "ro": "Deschide în aplicație"},
    "cta_sub": {"ru": "Бесплатно в App Store", "uk": "Безкоштовно в App Store", "pl": "Bezpłatnie w App Store", "en": "Free on the App Store", "de": "Kostenlos im App Store", "es": "Gratis en App Store", "fr": "Gratuit sur l'App Store", "it": "Gratis su App Store", "ro": "Gratuit pe App Store"},
    "home_title": {"ru": "Игры для детей от PlayMom", "uk": "Ігри для дітей від PlayMom", "pl": "Zabawy dla dzieci od PlayMom", "en": "Children's games from PlayMom", "de": "Kinderspiele von PlayMom", "es": "Juegos para niños de PlayMom", "fr": "Jeux pour enfants de PlayMom", "it": "Giochi per bambini di PlayMom", "ro": "Jocuri pentru copii de la PlayMom"},
    "home_intro": {
        "ru": "{count} коротких игр для детей от 0 до 8 лет. Пошаговые сценарии на 5-10 минут, без подготовки и покупок.",
        "uk": "{count} коротких ігор для дітей від 0 до 8 років. Покрокові сценарії на 5-10 хвилин, без підготовки й покупок.",
        "pl": "{count} krótkich zabaw dla dzieci od 0 do 8 lat. Scenariusze krok po kroku na 5-10 minut, bez przygotowań i zakupów.",
        "en": "{count} short games for children aged 0 to 8. Step by step scripts that take 5 to 10 minutes, no prep and no shopping.",
        "de": "{count} kurze Spiele für Kinder von 0 bis 8 Jahren. Schritt für Schritt Anleitungen für 5 bis 10 Minuten, ohne Vorbereitung und ohne Einkauf.",
        "es": "{count} juegos cortos para niños de 0 a 8 años. Guiones paso a paso de 5 a 10 minutos, sin preparación ni compras.",
        "fr": "{count} jeux courts pour les enfants de 0 à 8 ans. Des scénarios pas à pas de 5 à 10 minutes, sans préparation ni achats.",
        "it": "{count} giochi brevi per bambini da 0 a 8 anni. Copioni passo dopo passo da 5 a 10 minuti, senza preparazione e senza acquisti.",
        "ro": "{count} jocuri scurte pentru copii de la 0 la 8 ani. Scenarii pas cu pas de 5 la 10 minute, fără pregătire și fără cumpărături.",
    },
    "hub_age_intro": {
        "ru": "{count} игр для детей {band}: пошаговые сценарии, которые можно начать прямо сейчас.",
        "uk": "{count} ігор для дітей {band}: покрокові сценарії, які можна почати прямо зараз.",
        "pl": "{count} zabaw dla dzieci w wieku {band}: scenariusze krok po kroku, które można zacząć od razu.",
        "en": "{count} games for children aged {band}: step by step scripts you can start right now.",
        "de": "{count} Spiele für Kinder im Alter von {band}: Schritt für Schritt Anleitungen, die du sofort starten kannst.",
        "es": "{count} juegos para niños de {band}: guiones paso a paso que puedes empezar ahora mismo.",
        "fr": "{count} jeux pour les enfants de {band} : des scénarios pas à pas que vous pouvez commencer tout de suite.",
        "it": "{count} giochi per bambini di {band}: copioni passo dopo passo da iniziare subito.",
        "ro": "{count} jocuri pentru copii de {band}: scenarii pas cu pas pe care le poți începe chiar acum.",
    },
    "hub_goal_intro": {
        "ru": "{count} игр, которые развивают {goal}: короткие сценарии для разных возрастов.",
        "uk": "{count} ігор, які розвивають {goal}: короткі сценарії для різного віку.",
        "pl": "{count} zabaw rozwijających {goal}: krótkie scenariusze dla różnych wieków.",
        "en": "{count} games that build {goal}: short scripts for different ages.",
        "de": "{count} Spiele, die {goal} fördern: kurze Anleitungen für verschiedene Altersgruppen.",
        "es": "{count} juegos que desarrollan {goal}: guiones cortos para distintas edades.",
        "fr": "{count} jeux qui développent {goal} : des scénarios courts pour différents âges.",
        "it": "{count} giochi che sviluppano {goal}: copioni brevi per età diverse.",
        "ro": "{count} jocuri care dezvoltă {goal}: scenarii scurte pentru vârste diferite.",
    },
    "meta_description_game": {
        "ru": "{title}: игра для детей {band}. {mini}. Шаги, материалы и безопасность внутри.",
        "uk": "{title}: гра для дітей {band}. {mini}. Кроки, матеріали та безпека всередині.",
        "pl": "{title}: zabawa dla dzieci {band}. {mini}. Kroki, materiały i bezpieczeństwo w środku.",
        "en": "{title}: a game for children {band}. {mini}. Steps, materials and safety notes inside.",
        "de": "{title}: ein Spiel für Kinder {band}. {mini}. Schritte, Material und Sicherheitshinweise drin.",
        "es": "{title}: un juego para niños de {band}. {mini}. Pasos, materiales y seguridad dentro.",
        "fr": "{title} : un jeu pour les enfants de {band}. {mini}. Étapes, matériel et sécurité à l'intérieur.",
        "it": "{title}: un gioco per bambini di {band}. {mini}. Passaggi, materiali e sicurezza qui dentro.",
        "ro": "{title}: un joc pentru copii de {band}. {mini}. Pași, materiale și siguranță în interior.",
    },
}

CONTEXT_LABEL = {
    "no-prep": {"ru": "без подготовки", "uk": "без підготовки", "pl": "bez przygotowania", "en": "no prep", "de": "ohne Vorbereitung", "es": "sin preparación", "fr": "sans préparation", "it": "senza preparazione", "ro": "fără pregătire"},
    "no-mess": {"ru": "без уборки", "uk": "без прибирання", "pl": "bez bałaganu", "en": "no mess", "de": "ohne Chaos", "es": "sin desorden", "fr": "sans désordre", "it": "senza disordine", "ro": "fără mizerie"},
    "bedtime": {"ru": "перед сном", "uk": "перед сном", "pl": "przed snem", "en": "bedtime", "de": "vor dem Schlafen", "es": "antes de dormir", "fr": "avant le coucher", "it": "prima di dormire", "ro": "înainte de culcare"},
}

CATEGORY_ORDER = ["EMOTIONS", "GROSS_MOTOR", "THINKING", "INDEPENDENCE", "MOVEMENT", "FINE_MOTOR", "SPEECH", "ATTENTION", "SENSORY"]
