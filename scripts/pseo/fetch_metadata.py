#!/usr/bin/env python3
"""Fetch language-independent game metadata (age, category, image, contexts,
situations) from the PlayMom production API, throttled, cached to disk.

Only metadata is fetched here. Per-language text (title, descriptions,
steps, safety, materials, fullDescription) comes from the editorial locale
files, because the production API strips quickStart.steps/fullDescription
for anonymous requests (activity-access.ts: projectActivityForAccess hides
unlocked content). Metadata fields are not gated and do not vary by
language, confirmed by diffing lang=en vs lang=pl responses for the same id.

Usage: python3 scripts/fetch_metadata.py
"""
import json
import pathlib
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
CATALOG_DIR = pathlib.Path("/Users/artemreiter/playmom-v2-work/catalog")
CACHE_DIR = ROOT / "data" / "meta"
API_BASE = "https://backend-production-0ce4.up.railway.app/api/activities"
RPS = 5.0
MIN_INTERVAL = 1.0 / RPS

CACHE_DIR.mkdir(parents=True, exist_ok=True)

METADATA_FIELDS = [
    "id", "minAgeMonths", "maxAgeMonths", "categoryType", "imageUrl",
    "contexts", "situations", "preparationMinutes", "supervisedParticipation",
    "estimatedMinutes", "prepMinutes", "playMinutes", "totalMinutes",
]


def load_ids():
    ids = []
    for f in sorted(CATALOG_DIR.glob("batch_*.ids")):
        ids.extend(line.strip() for line in f.read_text().splitlines() if line.strip())
    seen = set()
    unique = []
    for i in ids:
        if i not in seen:
            seen.add(i)
            unique.append(i)
    return unique


def fetch_one(activity_id):
    url = f"{API_BASE}/{activity_id}?lang=ru"
    result = subprocess.run(
        ["curl", "-s", "--max-time", "15", url, "-H", "X-PlayMom-Contract: 2"],
        capture_output=True, text=True, check=True,
    )
    body = json.loads(result.stdout)
    return body["data"]


def main():
    ids = load_ids()
    print(f"{len(ids)} unique ids to fetch")
    ok, cached, failed = 0, 0, []
    last_call = 0.0
    for idx, activity_id in enumerate(ids, 1):
        cache_path = CACHE_DIR / f"{activity_id}.json"
        if cache_path.exists():
            cached += 1
            continue
        wait = MIN_INTERVAL - (time.monotonic() - last_call)
        if wait > 0:
            time.sleep(wait)
        last_call = time.monotonic()
        try:
            data = fetch_one(activity_id)
        except (subprocess.CalledProcessError, KeyError, json.JSONDecodeError) as e:
            failed.append((activity_id, str(e)))
            print(f"[{idx}/{len(ids)}] FAIL {activity_id}: {e}", file=sys.stderr)
            continue
        meta = {k: data.get(k) for k in METADATA_FIELDS}
        cache_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
        ok += 1
        if idx % 50 == 0 or idx == len(ids):
            print(f"[{idx}/{len(ids)}] fetched={ok} cached={cached} failed={len(failed)}")
    print(f"done: fetched={ok} cached={cached} failed={len(failed)}")
    if failed:
        print("FAILED IDS:")
        for aid, err in failed:
            print(f"  {aid}: {err}")
        sys.exit(1)


if __name__ == "__main__":
    main()
