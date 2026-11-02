# -*- coding: utf-8 -*-
"""Ascii, URL-safe slug generation for game titles in any of the 9 site
languages. Stdlib NFKD handles most accented Latin letters (es, fr, it);
the rest (ru, uk cyrillic, pl/de/ro special letters) need an explicit map.
"""
import re
import unicodedata

_CHAR_MAP = {
    # Russian / Ukrainian cyrillic (simplified scientific transliteration)
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "і": "i", "ї": "yi", "й": "y", "к": "k",
    "л": "l", "м": "m", "н": "n", "о": "o", "п": "p", "р": "r", "с": "s",
    "т": "t", "у": "u", "ф": "f", "х": "kh", "ц": "ts", "ч": "ch", "ш": "sh",
    "щ": "shch", "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
    "ґ": "g", "є": "ye",
    # Polish
    "ą": "a", "ć": "c", "ę": "e", "ł": "l", "ń": "n", "ó": "o", "ś": "s",
    "ź": "z", "ż": "z",
    # German
    "ä": "a", "ö": "o", "ü": "u", "ß": "ss",
    # Romanian
    "ă": "a", "â": "a", "î": "i", "ș": "s", "ț": "t",
    # French / Italian / Spanish extras not covered by NFKD
    "œ": "oe", "æ": "ae", "ñ": "n", "ç": "c",
}


def _transliterate(text: str) -> str:
    out = []
    for ch in text:
        lower = ch.lower()
        if lower in _CHAR_MAP:
            mapped = _CHAR_MAP[lower]
            out.append(mapped.upper() if ch.isupper() and mapped else mapped)
        else:
            out.append(ch)
    return "".join(out)


def slugify(text: str, max_words: int = 8, max_len: int = 60) -> str:
    text = _transliterate(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", " ", text)
    words = text.split()
    text = " ".join(words[:max_words])
    text = re.sub(r"[\s_]+", "-", text).strip("-")
    text = re.sub(r"-{2,}", "-", text)
    if len(text) > max_len:
        text = text[:max_len].rsplit("-", 1)[0]
    return text or "game"


def short_id(activity_id: str, length: int = 8) -> str:
    return activity_id[-length:]
