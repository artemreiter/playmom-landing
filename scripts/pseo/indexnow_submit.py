#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Submits every URL in the generated sitemaps to IndexNow (Bing/Yandex/
Seznam, and Bing's feed also reaches Google via IndexNow partnerships).
Does not touch Google Search Console.

Dry run by default: prints what would be sent. Pass --send to actually
POST to https://api.indexnow.org/indexnow.
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
DIST = HERE.parent / "dist"
HOST = "playmom.app"
INDEXNOW_URL = "https://api.indexnow.org/indexnow"


def find_key():
    keys = list(DIST.glob("*.txt"))
    keys = [k for k in keys if k.stem != "robots" and len(k.stem) >= 16]
    if not keys:
        sys.exit("no IndexNow key file found in dist/")
    if len(keys) > 1:
        sys.exit(f"multiple candidate key files in dist/: {keys}")
    return keys[0].stem


def collect_urls():
    urls = []
    for f in sorted(DIST.glob("sitemap-*.xml")):
        text = f.read_text(encoding="utf-8")
        urls.extend(re.findall(r"<loc>([^<]+)</loc>", text))
    return urls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--send", action="store_true", help="actually submit to IndexNow")
    args = parser.parse_args()

    key = find_key()
    urls = collect_urls()
    key_location = f"https://{HOST}/{key}.txt"
    payload = {"host": HOST, "key": key, "keyLocation": key_location, "urlList": urls}

    print(f"host={HOST} key={key} keyLocation={key_location}")
    print(f"urls to submit: {len(urls)}")
    print("sample:", urls[:3])

    if not args.send:
        print("DRY RUN: no request sent. Re-run with --send to submit.")
        return

    body = json.dumps(payload)
    result = subprocess.run(
        ["curl", "-s", "-o", "-", "-w", "\nHTTP_STATUS:%{http_code}\n",
         "-X", "POST", INDEXNOW_URL,
         "-H", "Content-Type: application/json; charset=utf-8",
         "-d", body],
        capture_output=True, text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
