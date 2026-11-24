#!/usr/bin/env python3
"""Asks Apple's public lookup whether AutoMetronom is in the App Store.

When it is, stores the App Store URL in am_store_url.txt and rebuilds the pages,
which adds the download button and removes the noindex tag. Exit code 0 either way;
prints "released" when files changed.
"""
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
TARGET = HERE / "am_store_url.txt"
LOOKUP = "https://itunes.apple.com/lookup?bundleId=net.allroundnetwork.autometronom"

if TARGET.exists():
    sys.exit(0)
with urllib.request.urlopen(LOOKUP, timeout=30) as response:
    results = json.load(response).get("results", [])
if not results or not results[0].get("trackViewUrl"):
    print("not released yet")
    sys.exit(0)
TARGET.write_text(results[0]["trackViewUrl"].split("?")[0] + "\n", encoding="utf-8")
subprocess.run([sys.executable, str(HERE / "build.py")], check=True, cwd=HERE)
print("released")
