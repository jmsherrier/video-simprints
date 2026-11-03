"""Command line: create, verify, fetch-corpus and test mode."""

import argparse
import csv
import hashlib
import io
import json
import shutil
import sys
import urllib.request
import zipfile
from pathlib import Path

MANIFEST = Path(__file__).resolve().parents[2] / "tests" / "corpus" / "manifest.csv"
CACHE = Path(".cache")


def corpus(manifest=MANIFEST) -> list[dict]:
    with open(manifest, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["path"] = CACHE / "corpus" / (r["name"] + Path(r["member"] or r["url"].split("?")[0]).suffix)
    return rows


def fetch(manifest=MANIFEST):
    """Download every corpus video into .cache/corpus and check its SHA-256 (of the
    file as downloaded, before unzipping)."""
    for r in corpus(manifest):
        if r["path"].exists():
            continue
        r["path"].parent.mkdir(parents=True, exist_ok=True)
        part = r["path"].with_suffix(".part")
        req = urllib.request.Request(r["url"], headers={"User-Agent": "video-simprints-corpus/0.1"})
        digest = hashlib.sha256()
        print(f"fetching {r['name']} ...", flush=True)
        with urllib.request.urlopen(req) as resp, open(part, "wb") as out:
            while chunk := resp.read(1 << 20):
                digest.update(chunk)
                out.write(chunk)
        if digest.hexdigest() != r["sha256"]:
            raise SystemExit(f"{r['name']}: SHA-256 {digest.hexdigest()} does not match the manifest ({part} kept)")
        if r["member"]:
            with zipfile.ZipFile(part) as z, z.open(r["member"]) as src, open(r["path"], "wb") as dst:
                shutil.copyfileobj(src, dst)
            part.unlink()
        else:
            part.rename(r["path"])
