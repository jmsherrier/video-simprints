"""Command line: create, verify, fetch-corpus and test mode."""

import argparse
import csv
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from . import recipe, video

MANIFEST = Path(__file__).resolve().parents[2] / "tests" / "corpus" / "manifest.csv"
CACHE = Path(".cache")
AGENT = "video-simprints-corpus/0.1 (https://github.com/jmsherrier/video-simprints)"

REPEATS = 2  # random excerpts per original and manipulation
STILLS = 5  # screenshots per video
PIP = {"top-left": ("40", "40"), "top-right": ("W-w-40", "40"), "bottom-left": ("40", "H-h-40"),
       "bottom-right": ("W-w-40", "H-h-40"), "centre": ("(W-w)/2", "(H-h)/2")}  # overlay positions, 40 px from the edges
# name: (seconds, expected relationship)
MANIPULATIONS = {
    "excerpt10": (10, "identical"), "excerpt30": (30, "identical"), "excerpt60": (60, "identical"),
    "vertical": (30, "contained_in"), "pip25": (30, "contains"), "pip40": (30, "contains"),
    "lowres": (30, "identical"), "caption": (30, "identical"), "logo": (30, "identical"),
}  # fmt: skip


# --- corpus ----------------------------------------------------------------------------


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
        print(f"fetching {r['name']} ...", flush=True)
        for attempt in range(8):
            digest = hashlib.sha256()
            try:
                req = urllib.request.Request(r["url"], headers={"User-Agent": AGENT})
                with urllib.request.urlopen(req) as resp, open(part, "wb") as out:
                    while chunk := resp.read(1 << 20):
                        digest.update(chunk)
                        out.write(chunk)
                break
            except urllib.error.HTTPError as e:
                if e.code != 429:  # Wikimedia rate-limits; wait and retry
                    raise
                time.sleep(30 * (attempt + 1))
        if digest.hexdigest() != r["sha256"]:
            raise SystemExit(f"{r['name']}: SHA-256 {digest.hexdigest()} does not match the manifest ({part} kept)")
        if r["member"]:
            with zipfile.ZipFile(part) as z, z.open(r["member"]) as src, open(r["path"], "wb") as dst:
                shutil.copyfileobj(src, dst)
            part.unlink()
        else:
            part.rename(r["path"])


# --- manipulations ---------------------------------------------------------------------


def probe(path) -> tuple[float, int, int]:
    """(duration in seconds, width, height) of the first video stream."""
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout  # fmt: skip
    j = json.loads(out)
    return float(j["format"]["duration"]), j["streams"][0]["width"], j["streams"][0]["height"]


def overlay_png(path, w, h, kind):
    """A caption bar along the bottom, or a logo in the top right corner."""
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if kind == "caption":
        d.rectangle([0, int(h * 0.8), w, h], fill=(0, 0, 0, 170))
        d.text((w * 0.04, h * 0.84), "Breaking news: captions and overlays test", fill="white",
               font=ImageFont.load_default(size=max(12, h // 18)))  # fmt: skip
    else:
        r = w // 20
        cx, cy = int(w * 0.9), int(h * 0.1)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 190), outline=(200, 30, 30, 255), width=max(2, r // 6))
        d.text((cx, cy), "TV9", fill=(200, 30, 30, 255), anchor="mm", font=ImageFont.load_default(size=r))
    im.save(path)


def ff(*args):
    subprocess.run([video.ffmpeg(), "-nostdin", "-y", "-v", "error", *map(str, args)], check=True)


ENCODE = ["-an", "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p"]


def make_clip(c: dict, src: Path, bg: Path | None):
    """Write one manipulated clip or still with ffmpeg."""
    out, s, n, m = Path(c["path"]), c["start"], c["end"] - c["start"], c["manipulation"]
    cut = ["-ss", f"{s:.3f}", "-t", f"{n:.3f}", "-i", src]
    if m.endswith("still"):
        ff("-ss", f"{s:.3f}", "-i", src, "-frames:v", 1, out)
    elif m.startswith("excerpt"):
        ff(*cut, *ENCODE, "-crf", 23, out)
    elif m == "vertical":
        ff(*cut, "-vf", "crop=trunc(ih*9/32)*2:ih", *ENCODE, "-crf", 23, out)
    elif m == "lowres":
        ff(*cut, "-vf", "scale=-2:240", *ENCODE, "-b:v", "150k", out)
    elif m in ("caption", "logo"):
        _, w, h = probe(src)
        png = out.with_suffix(".png")
        overlay_png(png, w, h, m)
        ff(*cut, "-i", png, "-filter_complex", "[0:v][1:v]overlay=0:0", *ENCODE, "-crf", 23, out)
        png.unlink()
    elif m.startswith("pip"):
        f, (x, y) = int(m[3:]) / 100, PIP[c["position"]]
        graph = (f"[1:v]scale=1920:1080,setsar=1[bg];[0:v]scale={round(1920 * f / 2) * 2}:-2,setsar=1[fg];"
                 f"[bg][fg]overlay={x}:{y}[v]")  # fmt: skip
        ff(*cut, "-stream_loop", -1, "-i", bg, "-filter_complex", graph, "-map", "[v]", "-t", f"{n:.3f}", *ENCODE, "-crf", 23, out)


def plan(split: str) -> list[dict]:
    """Every query of a split: manipulated clips and stills of each original, and each
    unrelated video whole and as stills. Seeded, so the same every run."""
    rows = [r for r in corpus() if r["split"] == split]
    unrelated = [r for r in rows if r["role"] == "unrelated"]
    rng = random.Random(f"video-simprints {split}")
    out = []
    for r in rows:
        dur = probe(r["path"])[0]
        d = CACHE / "clips" / split
        if r["role"] == "original":
            for m, (n, expect) in MANIPULATIONS.items():
                for i in range(REPEATS):
                    s = round(rng.uniform(0, dur - n - 1), 2)
                    out.append({"id": f"{r['name']}__{m}__{i}", "source": r["name"], "set": r["set"], "manipulation": m,
                                "start": s, "end": s + n, "expect": expect, "background": rng.choice(unrelated)["name"],
                                "position": rng.choice(list(PIP)), "path": str(d / f"{r['name']}__{m}__{i}.mp4")})  # fmt: skip
        else:
            out.append({"id": f"{r['name']}__whole", "source": None, "set": r["set"], "manipulation": "unrelated",
                        "start": 0, "end": dur, "path": str(r["path"])})  # fmt: skip
        for i in range(STILLS):
            s = round(rng.uniform(0, dur - 1), 2)
            out.append({"id": f"{r['name']}__still__{i}", "source": r["name"] if r["role"] == "original" else None, "set": r["set"],
                        "manipulation": "still" if r["role"] == "original" else "unrelated_still", "start": s,
                        "end": s, "expect": "identical", "path": str(d / f"{r['name']}__still__{i}.png")})  # fmt: skip
    return out


# --- command line ----------------------------------------------------------------------


def main(argv=None):
    ap = argparse.ArgumentParser(prog="video-simprints")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("create", help="print a video's declaration as JSON")
    c.add_argument("video")
    c.add_argument("--settings", default="{}", help='JSON, e.g. {"codes": 10}')
    v = sub.add_parser("verify", help="check a clip or a still against declarations")
    v.add_argument("query")
    v.add_argument("declarations", nargs="+", help="JSON files written by create")
    v.add_argument("--settings", default="{}", help='JSON, e.g. {"fps": 2, "prepared_size": 1024}')
    sub.add_parser("fetch-corpus", help="download the test corpus into .cache/corpus")
    t = sub.add_parser("test", help="manipulate the corpus, sweep settings, write a report")
    t.add_argument("--split", default="tuning", choices=["tuning", "test"])
    t.add_argument("--out", type=Path)
    t.add_argument("--fits", type=Path, help="a tuning report directory whose fitted thresholds to use")
    t.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    t.add_argument("--experiment", action="store_true", help="branding labels and overlapping tiles, after a test run")
    a = ap.parse_args(argv)
    if a.cmd == "create":
        json.dump(recipe.create(a.video, json.loads(a.settings)), sys.stdout)
    elif a.cmd == "verify":
        idx = recipe.index({p: json.loads(Path(p).read_text()) for p in a.declarations})
        s = json.loads(a.settings)
        still = Path(a.query).suffix.lower() in (".png", ".jpg", ".jpeg", ".webp")
        print(json.dumps(recipe.verify_still(a.query, idx, s) if still else recipe.verify(a.query, idx, s), indent=1))
    elif a.cmd == "fetch-corpus":
        fetch()
    else:
        from .evaluate import test
        from .experiment import main as experiment

        name = f"report-{'experiment-' if a.experiment else ''}{a.split}"
        (experiment if a.experiment else test)(a.split, a.out or Path("tests") / "corpus" / name, a.fits, a.workers)


if __name__ == "__main__":
    main()
