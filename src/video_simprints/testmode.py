"""Command line: create, verify, fetch-corpus and test mode."""

import argparse
import csv
import hashlib
import json
import os
import pickle
import random
import shutil
import statistics
import subprocess
import sys
import time
import urllib.error
import urllib.request
import zipfile
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from pathlib import Path

import image_simprints
from image_simprints import generate
from PIL import Image, ImageDraw, ImageFont

from . import recipe, video

MANIFEST = Path(__file__).resolve().parents[2] / "tests" / "corpus" / "manifest.csv"
CACHE = Path(".cache")
AGENT = "video-simprints-corpus/0.1 (https://github.com/jmsherrier/video-simprints)"

# Test mode sweeps these; N and M are fitted per setting on the tuning split.
CODES = (5, 10, 20)
SPREAD = (False, True)
STOP_AFTER = (1, 2, 3, 5, 10, 1000)
SIZES = (512, 1024)
FPS = (1, 2)
MIN_FRAMES = range(1, 13)
REPEATS = 3  # random excerpts per original and manipulation
STILLS = 5  # screenshots per video
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
        f = int(m[3:]) / 100
        graph = (f"[1:v]scale=1280:720,setsar=1[bg];[0:v]scale={round(1280 * f / 2) * 2}:-2,setsar=1[fg];"
                 "[bg][fg]overlay=W-w-40:H-h-40[v]")  # fmt: skip
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
                    out.append({"id": f"{r['name']}__{m}__{i}", "source": r["name"], "manipulation": m, "start": s,
                                "end": s + n, "expect": expect, "background": rng.choice(unrelated)["name"],
                                "path": str(d / f"{r['name']}__{m}__{i}.mp4")})  # fmt: skip
        else:
            out.append({"id": f"{r['name']}__whole", "source": None, "manipulation": "unrelated", "start": 0,
                        "end": dur, "path": str(r["path"])})  # fmt: skip
        for i in range(STILLS):
            s = round(rng.uniform(0, dur - 1), 2)
            out.append({"id": f"{r['name']}__still__{i}", "source": r["name"] if r["role"] == "original" else None,
                        "manipulation": "still" if r["role"] == "original" else "unrelated_still", "start": s,
                        "end": s, "expect": "identical", "path": str(d / f"{r['name']}__still__{i}.png")})  # fmt: skip
    return out


# --- evaluation ------------------------------------------------------------------------


def variants():
    return [{"codes": k, "spread": sp, "stop_after": n} for k in CODES for sp in SPREAD for n in STOP_AFTER]


def key(v: dict, size: int) -> str:
    return f"codes={v['codes']};spread={int(v['spread'])};stop_after={v['stop_after']};size={size}"


_IDX = {}


def _init(cands: dict, vs: list):
    for v in vs:
        _IDX[key(v, 0)] = (v, recipe.index({n: recipe.create(None, v, c) for n, c in cands.items()}))


def _query(c: dict) -> tuple[str, dict]:
    """Verifier codes of one query at 2 fps and both sizes (cached), and its per-frame
    hits against every swept setting, kept small: (declaration, time, same_as, match)."""
    cache = CACHE / "eval" / (c["id"] + ".pkl")
    if cache.exists():
        sp = pickle.loads(cache.read_bytes())
    else:
        src = c["path"]
        frames = [src] if src.endswith(".png") else list(video.frames(src, 2))
        sp = {size: [generate(f, "verifier", {"prepared_size": size}) for f in frames] for size in SIZES}
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(pickle.dumps(sp))
    out = {}
    for v, idx in _IDX.values():
        for size in SIZES:
            out[key(v, size)] = [[(d, {"time": k["time"], "same_as": k["same_as"]}, r) for d, k, r in recipe.frame_hits(q, idx)]
                                 for q in sp[size]]  # fmt: skip
    return c["id"], out


def run(split: str, workers: int, vs: list) -> dict:
    """Make the split's queries, decode and code everything, and match every query
    against every creator setting in vs. Returns the raw per-frame hits."""
    queries = plan(split)
    src = {r["name"]: r["path"] for r in corpus()}
    todo = [c for c in queries if c["manipulation"] != "unrelated" and not Path(c["path"]).exists()]
    (CACHE / "clips" / split).mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(workers) as ex:  # each clip is an ffmpeg process
        list(ex.map(lambda c: make_clip(c, src[c["source"] or c["id"].split("__")[0]], src.get(c.get("background"))), todo))
    cands = {}
    for r in corpus():
        if r["split"] == split and r["role"] == "original":
            cache = CACHE / "eval" / f"cands-{r['name']}.json"
            if not cache.exists():
                t = time.perf_counter()
                c = recipe.candidates(r["path"])
                c["seconds"] = time.perf_counter() - t
                cache.parent.mkdir(parents=True, exist_ok=True)
                cache.write_text(json.dumps(c))
            cands[r["name"]] = json.loads(cache.read_text())
    with Pool(workers, _init, (cands, vs)) as pool:
        hits = dict(pool.imap_unordered(_query, queries))
    return {"queries": queries, "cands": cands, "hits": hits}


def score(data: dict, k: str, fps: int, m: int) -> dict:
    """Metrics of one setting (k from key(), at fps and min_frames m)."""
    per = {name: {"clips": 0, "found": 0, "relationship": 0, "frames": 0, "frames_found": 0} for name in [*MANIPULATIONS, "still"]}
    false = {"unrelated_videos": 0, "unrelated_frames": 0, "unrelated_frames_total": 0, "unrelated_stills": 0,
             "wrong_video": 0, "unrelated_still_total": 0, "unrelated_video_total": 0}  # fmt: skip
    for c in data["queries"]:
        h = data["hits"][c["id"]][k]
        if c["manipulation"] in ("still", "unrelated_still"):
            best = max(h[0], key=lambda x: x[2]["agreeing_codes"], default=None)
            if c["manipulation"] == "unrelated_still":
                false["unrelated_still_total"] += 1
                false["unrelated_stills"] += best is not None
                continue
            p = per["still"]
            p["clips"] += 1
            p["found"] += best is not None and best[0] == c["source"]
            p["relationship"] += best is not None and best[0] == c["source"] and best[2]["relationship"] == c["expect"]
            continue
        frames = h[:: 2 // fps]
        res = recipe.decide(frames, fps, m)
        if c["manipulation"] == "unrelated":
            false["unrelated_video_total"] += 1
            false["unrelated_videos"] += bool(res)
            false["unrelated_frames_total"] += len(frames)
            false["unrelated_frames"] += sum(bool(f) for f in frames)
            continue
        p = per[c["manipulation"]]
        p["clips"] += 1
        p["frames"] += len(frames)
        p["frames_found"] += sum(any(x[0] == c["source"] for x in f) for f in frames)
        top = res[0] if res else None
        ok = top and top["declaration"] == c["source"] and top["original"][0] <= c["end"] + 3 and top["original"][1] >= c["start"] - 3
        p["found"] += bool(ok)
        p["relationship"] += bool(ok) and top["relationship"] == c["expect"]
        false["wrong_video"] += any(x["declaration"] != c["source"] for x in res)
    clips = [p for name, p in per.items() if name != "still"]
    return {"per_manipulation": per, "false": false,
            "video_match_rate": sum(p["found"] / p["clips"] for p in clips) / len(clips)}  # fmt: skip


def volume(cands: dict, v: dict) -> dict:
    decls = [recipe.create(None, v, c) for c in cands.values()]
    minutes = sum(d["duration"] for d in decls) / 60
    codes = sum(len(k["codes"]) for d in decls for k in d["keyframes"])
    kfs = sum(len(d["keyframes"]) for d in decls)
    return {"keyframes_per_minute": round(kfs / minutes, 1), "codes_per_minute": round(codes / minutes, 1),
            "codes_per_90min_film": round(codes / minutes * 90)}  # fmt: skip


def fit(data: dict) -> dict:
    """Per (codes, spread, size, fps): the stop_after and min_frames with the highest
    video-level match rate and no false match (ties: larger min_frames, then larger stop_after)."""
    out = {}
    for k in CODES:
        for sp in SPREAD:
            for size in SIZES:
                for fps in FPS:
                    best = None
                    for n in STOP_AFTER:
                        for m in MIN_FRAMES:
                            s = score(data, key({"codes": k, "spread": sp, "stop_after": n}, size), fps, m)
                            f = s["false"]
                            if f["unrelated_videos"] or f["wrong_video"] or f["unrelated_stills"]:
                                continue
                            rank = (s["video_match_rate"], m, n)
                            if best is None or rank > best[0]:
                                best = (rank, n, m)
                    out[f"codes={k};spread={int(sp)};size={size};fps={fps}"] = {"stop_after": best[1], "min_frames": best[2]} if best else None
    return out


def timing(split: str) -> dict:
    """Seconds per minute of video, one process: the creator on the first original,
    the verifier on its first 60 s excerpt at each fps and size."""
    r = next(r for r in corpus() if r["split"] == split and r["role"] == "original")
    t = time.perf_counter()
    c = recipe.candidates(r["path"])
    out = {"creator": round((time.perf_counter() - t) / (c["duration"] / 60), 2)}
    clip = CACHE / "clips" / split / f"{r['name']}__excerpt60__0.mp4"
    decl = recipe.index({r["name"]: recipe.create(None, None, c)})
    for fps in FPS:
        for size in SIZES:
            t = time.perf_counter()
            recipe.verify(clip, decl, {"fps": fps, "prepared_size": size})
            out[f"verifier fps={fps} size={size}"] = round(time.perf_counter() - t, 2)
    return out


def setting(name: str, f: dict) -> dict:
    """The creator settings of a fit named "codes=K;spread=S;size=..;fps=..", with its N."""
    p = dict(x.split("=") for x in name.split(";"))
    return {"codes": int(p["codes"]), "spread": p["spread"] == "1", "stop_after": f["stop_after"]}


def test(split: str, out: Path, fits_from: Path | None, workers: int):
    if fits_from:  # only the fitted settings
        fits = json.loads((fits_from / "report.json").read_text())["fits"]
        vs = {key(v, 0): v for v in (setting(n, f) for n, f in fits.items() if f)}
        data = run(split, workers, list(vs.values()))
    else:
        data = run(split, workers, variants())
        fits = fit(data)
    rows = {}
    for name, f in fits.items():
        if f is None:
            continue
        p, v = dict(x.split("=") for x in name.split(";")), setting(name, f)
        rows[name] = {**f, **score(data, key(v, int(p["size"])), int(p["fps"]), f["min_frames"]), "volume": volume(data["cands"], v)}
    report = {"split": split, "ffmpeg": video.version(), "recipe": recipe.RECIPE, "image_recipe": image_simprints.RECIPE,
              "fits": fits, "fitted_on": fits_from.name if fits_from else split, "results": rows, "timing": timing(split),
              "queries": len(data["queries"])}  # fmt: skip
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=1))
    (out / "summary.md").write_text(summary(report))
    print((out / "summary.md").read_text())


def summary(r: dict) -> str:
    pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "-"  # noqa: E731
    names = [*MANIPULATIONS, "still"]
    lines = [f"# video-simprints test report: {r['split']} split", "",
             f"Recipe {r['recipe']} on {r['image_recipe']}; {r['ffmpeg']}. Stop codes (N) and min frames (M) fitted on "
             f"the {r['fitted_on']} split. {r['queries']} queries.", "",
             "## Video-level match rate (correct video, time range within 3 s)", "",
             "| setting | N | M | " + " | ".join(names) + " | mean (clips) |", "|" + " --- |" * (len(names) + 4)]  # fmt: skip
    for name, x in r["results"].items():
        p = x["per_manipulation"]
        lines.append(f"| {name} | {x['stop_after']} | {x['min_frames']} | " + " | ".join(pct(p[n]["found"], p[n]["clips"]) for n in names)
                     + f" | {100 * x['video_match_rate']:.1f}% |")  # fmt: skip
    lines += ["", "## Expected spatial relationship (share of clips found with it)", "",
              "| setting | " + " | ".join(names) + " |", "|" + " --- |" * (len(names) + 1)]  # fmt: skip
    for name, x in r["results"].items():
        p = x["per_manipulation"]
        lines.append(f"| {name} | " + " | ".join(pct(p[n]["relationship"], p[n]["clips"]) for n in names) + " |")
    lines += ["", "## Frame-level match rate (sampled frames matching a keyframe of the source)", "",
              "| setting | " + " | ".join(MANIPULATIONS) + " |", "|" + " --- |" * (len(MANIPULATIONS) + 1)]  # fmt: skip
    for name, x in r["results"].items():
        p = x["per_manipulation"]
        lines.append(f"| {name} | " + " | ".join(pct(p[n]["frames_found"], p[n]["frames"]) for n in MANIPULATIONS) + " |")
    lines += ["", "## False matches", "",
              "| setting | unrelated videos | unrelated frames | unrelated stills | wrong video in a manipulated clip |",
              "| --- | --- | --- | --- | --- |"]  # fmt: skip
    for name, x in r["results"].items():
        f = x["false"]
        lines.append(f"| {name} | {f['unrelated_videos']} of {f['unrelated_video_total']} | {f['unrelated_frames']} of "
                     f"{f['unrelated_frames_total']} | {f['unrelated_stills']} of {f['unrelated_still_total']} | {f['wrong_video']} |")  # fmt: skip
    lines += ["", "## Code volume (originals of this split)", "",
              "| codes | spread | N | keyframes / min | codes / min | codes per 90-min film |", "| --- | --- | --- | --- | --- | --- |"]
    seen = set()
    for name, x in r["results"].items():
        p = dict(s.split("=") for s in name.split(";"))
        k = (p["codes"], p["spread"], x["stop_after"])
        if k not in seen:
            seen.add(k)
            v = x["volume"]
            lines.append(f"| {k[0]} | {k[1]} | {k[2]} | {v['keyframes_per_minute']} | {v['codes_per_minute']} | {v['codes_per_90min_film']:,} |")
    lines += ["", "## Timing (seconds per minute of video, one process)", ""]
    lines += [f"- {k}: {v} s" for k, v in r["timing"].items()]
    return "\n".join(lines) + "\n"


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
    t.add_argument("--fits", type=Path, help="a tuning report directory whose fitted N and M to use")
    t.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) // 2))
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
        test(a.split, a.out or Path("tests") / "corpus" / f"report-{a.split}", a.fits, a.workers)


if __name__ == "__main__":
    main()
