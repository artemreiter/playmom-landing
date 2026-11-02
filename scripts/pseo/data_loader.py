# -*- coding: utf-8 -*-
"""Loads the 348 rewritten game ids, their per-language editorial text and
their language-independent metadata, and assembles the records the site
generator renders. Does not fetch anything over the network; run
fetch_metadata.py first.
"""
import glob
import json
import pathlib

from ui_strings import AGE_BANDS, LANGS

CATALOG_DIR = pathlib.Path("/Users/artemreiter/playmom-v2-work/catalog")
EDITORIAL_DIR = pathlib.Path(
    "/Users/artemreiter/playmom-wt/integration/backend/prisma/editorial/locales"
)
MANIFEST_PATH = pathlib.Path(
    "/Users/artemreiter/playmom-wt/integration/backend/prisma/editorial/manifest.json"
)
HERE = pathlib.Path(__file__).resolve().parent
META_DIR = HERE.parent / "data" / "meta"


def load_guest_preview_ids():
    """Activity ids the app shows fully to guests for free (same flag the
    app's own access control reads: manifest.json -> activities[].guestPreview).
    """
    with open(MANIFEST_PATH, encoding="utf-8") as fh:
        manifest = json.load(fh)
    return {a["activityId"] for a in manifest["activities"] if a.get("guestPreview")}


def load_ids():
    ids = []
    seen = set()
    for f in sorted(CATALOG_DIR.glob("batch_*.ids")):
        for line in f.read_text().splitlines():
            line = line.strip()
            if line and line not in seen:
                seen.add(line)
                ids.append(line)
    return ids


def load_editorial():
    """lang -> {activity_id: payload dict}"""
    out = {}
    for lang in LANGS:
        with open(EDITORIAL_DIR / f"{lang}.json", encoding="utf-8") as fh:
            out[lang] = json.load(fh)
    return out


def load_metadata():
    """activity_id -> metadata dict"""
    out = {}
    for f in META_DIR.glob("*.json"):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        out[d["id"]] = d
    return out


def bands_for(min_age, max_age):
    return [key for key, lo, hi in AGE_BANDS if min_age <= hi and max_age >= lo]


def build_games(ids, editorial, metadata):
    """Returns list of game dicts, each with:
    id, meta (shared), text[lang] -> editorial payload, bands (list of band keys)
    Raises if any id is missing editorial text or metadata (fail loud, no
    silent thin pages).
    """
    games = []
    for gid in ids:
        meta = metadata.get(gid)
        if meta is None:
            raise KeyError(f"missing metadata for {gid}")
        text = {}
        for lang in LANGS:
            payload = editorial[lang].get(gid)
            if payload is None:
                raise KeyError(f"missing {lang} editorial text for {gid}")
            if not payload.get("quickStart", {}).get("steps"):
                raise ValueError(f"empty steps for {gid} in {lang}")
            text[lang] = payload
        games.append({
            "id": gid,
            "meta": meta,
            "text": text,
            "bands": bands_for(meta["minAgeMonths"], meta["maxAgeMonths"]),
        })
    return games


def siblings_for(game, all_games, limit=8):
    """Up to `limit` other games sharing this game's category, closest in
    age range first, excluding itself. Deterministic order (by id) for ties.
    """
    cat = game["meta"]["categoryType"]
    mid = (game["meta"]["minAgeMonths"] + game["meta"]["maxAgeMonths"]) / 2
    candidates = [g for g in all_games if g["id"] != game["id"] and g["meta"]["categoryType"] == cat]

    def distance(g):
        gmid = (g["meta"]["minAgeMonths"] + g["meta"]["maxAgeMonths"]) / 2
        return (abs(gmid - mid), g["id"])

    candidates.sort(key=distance)
    return candidates[:limit]
