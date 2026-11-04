"""Test mode's evaluation: code every query once, match it against every swept setting,
fit the thresholds on the tuning split, and write the report."""

import json
import pickle
import statistics
import time
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import Pool
from pathlib import Path

import image_simprints
import numpy as np
from image_simprints import generate
from image_simprints.recipe import decode, hamming, parse

from . import recipe, video
from .testmode import CACHE, MANIPULATIONS, corpus, make_clip, plan, probe

# Swept. Per K, verifier size and fps, N (stop_after), N2 (shared_after) and M are fitted on tuning.
CODES = (5, 10, 20)
STOP_AFTER = (1, 2, 3, 5, 10, 1000)  # 1000: off
SHARED_AFTER = (None, 0, 1, 2)  # None: off
SIZES = ("512", "1024")
FPS = (1, 2)
MIN_FRAMES = range(1, 13)
PIP_MODES = ("1024", "1920", "1024+tiles", "1920+tiles")  # on picture-in-picture clips and unrelated videos
STILL_SIZES = (512, 1024, 1920)
STILL_CODES = (64, 128, 256)
STILL_VOTES = (2, 3, 4, 5)  # agreeing codes a still needs
BUDGET = 10  # the design's 5-10 codes per keyframe: the recommended K is at most this
TILED = ("pip25", "pip40", "unrelated")  # queries that also get the picture-in-picture modes


def vkey(k, n, sh) -> str:
    return f"codes={k};stop_after={n};shared_after={sh}"


def gen(f, size, n=64):
    return generate(f, "verifier", {"prepared_size": size, "verifier_codes": n})


def quarters(f):
    h, w = f.shape[:2]
    return [f[y : y + h // 2, x : x + w // 2] for y in (0, h // 2) for x in (0, w // 2)]


def codes_of(c: dict) -> dict:
    """Verifier codes of one query, cached: per frame at 2 fps, or for a still."""
    cache = CACHE / "eval" / (c["id"] + ".pkl")
    if cache.exists():
        return pickle.loads(cache.read_bytes())
    if c["manipulation"].endswith("still"):
        im = decode(c["path"])
        out = {s: gen(im, s, max(STILL_CODES)) for s in STILL_SIZES}
    else:
        out = {"512": [], "1024": []} | ({"1920": [], "tiles": []} if c["manipulation"] in TILED else {})
        for f in video.frames(c["path"], 2):
            out["512"].append(gen(f, 512))
            out["1024"].append(gen(f, 1024))
            if "tiles" in out:
                out["1920"].append(gen(f, 1920))
                out["tiles"].append([gen(q, 1024) for q in quarters(f)])
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_bytes(pickle.dumps(out))
    return out


# --- workers ---------------------------------------------------------------------------

_W = {}


def _init(path):
    """Every swept index, and the universe of codes they are drawn from (each candidate
    keyframe's top max(CODES)), so a frame's distances are computed once."""
    decls, cols, _W["U"] = pickle.loads(Path(path).read_bytes())
    _W["idx"] = {}
    for (k, n), ds in decls.items():
        kfs = [(d, kf) for d, decl in ds.items() for kf in decl["keyframes"]]
        counts = recipe.shared_counts(kfs)
        for sh in SHARED_AFTER:
            idx = recipe.index_keyframes(kfs if sh is None else recipe.unshared(kfs, counts, sh))
            idx["cols"] = np.array([cols[(d, kf["time"], x["chunk_idx"])] for d, kf in idx["keyframes"] for x in kf["codes"]], int)
            _W["idx"][vkey(k, n, sh)] = idx


def _hits(sps: list) -> dict:
    """Per swept index: per simprint, its frame_hits."""
    nears = [hamming(parse(sp)[0], _W["U"]) <= 24 for sp in sps]
    return {vk: [recipe.frame_hits(sp, idx, nr[:, idx["cols"]]) for sp, nr in zip(sps, nears)] for vk, idx in _W["idx"].items()}


def _query(c: dict):
    sets = codes_of(c)
    out = {}
    if c["manipulation"].endswith("still"):
        for size in STILL_SIZES:
            for n in STILL_CODES:
                for vk, (h,) in _hits([sets[size] | {"codes": sets[size]["codes"][:n]}]).items():
                    b = max(h, key=lambda x: x[2]["agreeing_codes"], default=None)
                    out[(f"{size}/{n}", vk)] = b and (b[0], b[1]["time"], b[2]["relationship"], b[2]["agreeing_codes"])
        return c["id"], out
    modes = {name: _hits(sets[name]) for name in ("512", "1024", "1920") if name in sets}
    if "tiles" in sets:
        flat = _hits([sp for four in sets["tiles"] for sp in four])
        tiles = {vk: [sum(h[i : i + 4], []) for i in range(0, len(h), 4)] for vk, h in flat.items()}
        for name in ("1024", "1920"):
            modes[f"{name}+tiles"] = {vk: [a + b for a, b in zip(modes[name][vk], tiles[vk])] for vk in tiles}
    for mode, per in modes.items():
        for vk, frames in per.items():
            for fps in FPS:
                fr = frames[:: 2 // fps]
                res = [(r["declaration"], r["frames"], r["original"][0], r["original"][1], r["relationship"]) for r in recipe.decide(fr, fps, 1)]
                src = sum(any(h[0] == c["source"] for h in f) for f in fr)
                out[(mode, vk, fps)] = (res, len(fr), src, sum(bool(f) for f in fr))
    return c["id"], out


def _cands(r):
    cache = CACHE / "eval" / f"cands-{r['name']}.json"
    if not cache.exists():
        t = time.perf_counter()
        c = recipe.candidates(r["path"])
        c["seconds"] = time.perf_counter() - t
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(c))
    return r["name"], json.loads(cache.read_text())


def _create(args):
    name, k, n = args
    return (k, n, name), recipe.create(None, {"codes": k, "stop_after": n}, _cands({"name": name})[1])


def run(split: str, workers: int) -> dict:
    """Make the split's queries, code everything once, match every query against every
    swept setting. Returns compact per-query results."""
    queries = plan(split)
    src = {r["name"]: r["path"] for r in corpus()}
    todo = [c for c in queries if c["manipulation"] != "unrelated" and not Path(c["path"]).exists()]
    (CACHE / "clips" / split).mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(workers) as ex:  # each clip is an ffmpeg process
        list(ex.map(lambda c: make_clip(c, src[c["source"] or c["id"].split("__")[0]], src.get(c.get("background"))), todo))
    originals = [r for r in corpus() if r["split"] == split and r["role"] == "original"]
    with Pool(workers) as pool:
        cands = dict(pool.map(_cands, originals))
        decls = {}
        for (k, n, name), d in pool.map(_create, [(r["name"], k, n) for r in originals for k in CODES for n in STOP_AFTER]):
            decls.setdefault((k, n), {})[name] = d
    cols, codes = {}, []
    for name, c in cands.items():
        for kf in c["keyframes"]:
            for x in kf["codes"][: max(CODES)]:
                cols[(name, kf["time"], x["chunk_idx"])] = len(codes)
                codes.append(np.frombuffer(bytes.fromhex(x["code"]), ">u8"))
    path = CACHE / "eval" / f"decls-{split}.pkl"
    path.write_bytes(pickle.dumps((decls, cols, np.array(codes, np.uint64).reshape(-1, 4))))
    order = sorted(queries, key=lambda c: -(c["end"] - c["start"]) * (5 if c["manipulation"] in TILED else 1))  # long first
    with Pool(workers, _init, (str(path),)) as pool:
        results = dict(pool.imap_unordered(_query, order))
    return {"queries": queries, "results": results, "cands": cands, "decls": decls}


# --- scoring ---------------------------------------------------------------------------


def score(data: dict, mode: str, vk: str, fps: int, m: int) -> dict:
    return scores(data, mode, vk, fps, [m])[0]


def scores(data: dict, mode: str, vk: str, fps: int, ms) -> list:
    """Per min_frames in ms: video-level and frame-level rates per manipulation, and
    every false match, of one setting. Clips without results in this mode are skipped."""
    out = []
    for m in ms:
        per = {name: {"clips": 0, "found": 0, "relationship": 0, "frames": 0, "frames_found": 0} for name in MANIPULATIONS}
        out.append((per, {"videos": [], "wrong": [], "unrelated_videos": 0, "unrelated_frames": 0, "unrelated_frames_total": 0}))
    for c in data["queries"]:
        r = data["results"][c["id"]].get((mode, vk, fps))
        if r is None:
            continue
        all_res, n, n_src, n_any = r
        for m, (per, false) in zip(ms, out):
            res = [x for x in all_res if x[1] >= m]
            if c["manipulation"] == "unrelated":
                false["unrelated_videos"] += 1
                false["unrelated_frames_total"] += n
                false["unrelated_frames"] += n_any
                false["videos"] += [(c["id"], c["set"], d, f) for d, f, *_ in res]
                continue
            p = per[c["manipulation"]]
            p["clips"] += 1
            p["frames"] += n
            p["frames_found"] += n_src
            top = max(res, key=lambda x: x[1], default=None)
            ok = top is not None and top[0] == c["source"] and top[2] <= c["end"] + 3 and top[3] >= c["start"] - 3
            p["found"] += ok
            p["relationship"] += ok and top[4] == c["expect"]
            false["wrong"] += [(c["id"], c["set"], d, f) for d, f, *_ in res if d != c["source"]]
    result = []
    for per, false in out:
        clips = [p for p in per.values() if p["clips"]]
        rate = sum(p["found"] / p["clips"] for p in clips) / len(clips) if clips else 0.0
        result.append({"per_manipulation": per, "false": false, "video_match_rate": rate,
                       "false_count": len(false["videos"]) + len(false["wrong"])})  # fmt: skip
    return result


def score_stills(data: dict, mode: str, vk: str, votes: int) -> dict:
    out = {"stills": 0, "found": 0, "relationship": 0, "time_error": [], "unrelated": 0, "false": []}
    for c in data["queries"]:
        if not c["manipulation"].endswith("still"):
            continue
        b = data["results"][c["id"]][(mode, vk)]
        b = b if b and b[3] >= votes else None
        if c["manipulation"] == "unrelated_still":
            out["unrelated"] += 1
            out["false"] += [(c["id"], c["set"], b[0], b[3])] if b else []
            continue
        out["stills"] += 1
        if b and b[0] == c["source"]:
            out["found"] += 1
            out["relationship"] += b[2] == c["expect"]
            out["time_error"].append(abs(b[1] - c["start"]))
    out["rate"] = out["found"] / out["stills"]
    out["median_time_error"] = round(statistics.median(out["time_error"]), 1) if out["time_error"] else None
    del out["time_error"]
    return out


def fit(data: dict) -> dict:
    """On tuning: per K, verifier size and fps, the N, N2 and M with the fewest false
    matches, then the highest video-level match rate (ties: larger M, no index-level
    stop codes, larger N). The recommendation: the best fit with no false match and K
    within BUDGET (ties: smaller K, size, fps). Stills: per still mode at the
    recommended codes, the fewest votes with no false match; the best mode."""
    fits = {}
    for k in CODES:
        for size in SIZES:
            for fps in FPS:
                best = None
                for n in STOP_AFTER:
                    for sh in SHARED_AFTER:
                        for m, s in zip(MIN_FRAMES, scores(data, size, vkey(k, n, sh), fps, MIN_FRAMES)):
                            rank = (-s["false_count"], s["video_match_rate"], m, sh is None, n)
                            if best is None or rank > best[0]:
                                best = (rank, {"codes": k, "size": size, "fps": fps, "stop_after": n, "shared_after": sh, "min_frames": m})
                fits[f"codes={k};size={size};fps={fps}"] = best[1] | {"tuning_rate": round(best[0][1], 4), "tuning_false": -best[0][0]}
    ok = [f for f in fits.values() if f["tuning_false"] == 0 and f["codes"] <= BUDGET]
    rec = max(ok, key=lambda f: (f["tuning_rate"], -f["codes"], -int(f["size"]), -f["fps"]))
    vk = vkey(rec["codes"], rec["stop_after"], rec["shared_after"])
    stills = {}
    for size in STILL_SIZES:
        for n in STILL_CODES:
            mode = f"{size}/{n}"
            for votes in STILL_VOTES:
                s = score_stills(data, mode, vk, votes)
                if not s["false"]:
                    stills[mode] = {"votes": votes, "tuning_rate": round(s["rate"], 4)}
                    break
    still = max(stills, key=lambda mo: (stills[mo]["tuning_rate"], -int(mo.split("/")[0]), -int(mo.split("/")[1])))
    return {"settings": fits, "recommended": rec, "stills": stills, "recommended_still": still}


# --- report ----------------------------------------------------------------------------


def volume(decls: dict, k: int, n: int) -> dict:
    ds = decls[(k, n)].values()
    minutes = sum(d["duration"] for d in ds) / 60
    codes = sum(len(kf["codes"]) for d in ds for kf in d["keyframes"])
    return {"keyframes_per_minute": round(sum(len(d["keyframes"]) for d in ds) / minutes, 1),
            "codes_per_minute": round(codes / minutes, 1), "codes_per_90min_film": round(codes / minutes * 90)}  # fmt: skip


def timing(split: str, rec: dict) -> dict:
    """Seconds per minute of video in one process: the creator on the first original;
    the verifier (coding and matching) on its first 60 s excerpt and first 25% PiP clip;
    and milliseconds per still."""
    r = next(r for r in corpus() if r["split"] == split and r["role"] == "original")
    t = time.perf_counter()
    c = recipe.candidates(r["path"])
    decl = recipe.create(None, {"codes": rec["codes"], "stop_after": rec["stop_after"]}, c)
    out = {"creator": round((time.perf_counter() - t) / (c["duration"] / 60), 1)}
    idx = recipe.index({r["name"]: decl}, rec["shared_after"])
    for clip, modes in (("excerpt60", SIZES), ("pip25", PIP_MODES)):
        path = CACHE / "clips" / split / f"{r['name']}__{clip}__0.mp4"
        for mode in modes:
            for fps in FPS if clip == "excerpt60" else (rec["fps"],):
                size, tiles = int(mode.split("+")[0]), mode.endswith("tiles")
                t = time.perf_counter()
                recipe.verify(path, idx, {"fps": fps, "prepared_size": size, "tiles": tiles})
                out[f"verifier {mode} fps={fps} ({clip})"] = round((time.perf_counter() - t) / (probe(path)[0] / 60), 1)
    stills = sorted((CACHE / "clips" / split).glob(f"{r['name']}__still__*.png"))
    for mode in [f"{s}/{n}" for s in STILL_SIZES for n in STILL_CODES]:
        size, n = map(int, mode.split("/"))
        t = time.perf_counter()
        for p in stills:
            recipe.verify_still(p, idx, {"prepared_size": size, "verifier_codes": n})
        out[f"still {mode} (ms per still)"] = round((time.perf_counter() - t) / len(stills) * 1000)
    return out


def test(split: str, out: Path, fits_from: Path | None, workers: int):
    data = run(split, workers)
    fits = json.loads((fits_from / "report.json").read_text())["fits"] if fits_from else fit(data)
    rec = fits["recommended"]
    rec_vk = vkey(rec["codes"], rec["stop_after"], rec["shared_after"])
    rows = {}
    for name, f in fits["settings"].items():
        s = score(data, f["size"], vkey(f["codes"], f["stop_after"], f["shared_after"]), f["fps"], f["min_frames"])
        rows[name] = f | s | {"volume": volume(data["decls"], f["codes"], f["stop_after"])}
    by_m = {label: scores(data, rec["size"], vk, rec["fps"], MIN_FRAMES)
            for label, vk in (("recommended stop codes", rec_vk), ("no stop codes", vkey(rec["codes"], 1000, None)))}  # fmt: skip
    pip = {mode: score(data, mode, rec_vk, rec["fps"], rec["min_frames"]) for mode in PIP_MODES}
    pip_pos = {mode: {} for mode in PIP_MODES}
    for mode in PIP_MODES:
        for c in data["queries"]:
            if c["manipulation"] in ("pip25", "pip40"):
                res = [x for x in data["results"][c["id"]][(mode, rec_vk, rec["fps"])][0] if x[1] >= rec["min_frames"]]
                top = max(res, key=lambda x: x[1], default=None)
                k = f"{c['manipulation']} {'centre' if c['position'] == 'centre' else 'corner'}"
                hit = top is not None and top[0] == c["source"] and top[2] <= c["end"] + 3 and top[3] >= c["start"] - 3
                pip_pos[mode].setdefault(k, [0, 0])
                pip_pos[mode][k][0] += hit
                pip_pos[mode][k][1] += 1
    stills = {mode: score_stills(data, mode, rec_vk, f["votes"]) | f for mode, f in fits["stills"].items()}
    report = {"split": split, "ffmpeg": video.version(), "recipe": recipe.RECIPE, "image_recipe": image_simprints.RECIPE,
              "fitted_on": fits_from.name if fits_from else split, "fits": fits, "results": rows, "by_min_frames": by_m,
              "pip": pip, "pip_by_position": pip_pos, "stills": stills,
              "timing": timing(split, rec), "queries": len(data["queries"])}  # fmt: skip
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=1, default=str))
    (out / "summary.md").write_text(summary(report))
    print((out / "summary.md").read_text())


def summary(r: dict) -> str:
    pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "-"  # noqa: E731
    names = list(MANIPULATIONS)
    rec = r["fits"]["recommended"]
    L = [f"# video-simprints report: {r['split']} split", "",
         f"Recipe {r['recipe']} on {r['image_recipe']}; {r['ffmpeg']}. {r['queries']} queries. Thresholds fitted on "
         f"the {r['fitted_on']} split. N: per-video stop codes (`stop_after`, 1000 = off); N2: index-level stop codes "
         f"(`shared_after`, None = off); M: `min_frames`.", "",
         f"**Recommended** (chosen on tuning): K = {rec['codes']}, verifier {rec['size']} px at {rec['fps']} fps, "
         f"N = {rec['stop_after']}, N2 = {rec['shared_after']}, M = {rec['min_frames']}.", "",
         "## Video-level match rate (right video, time range within 3 s) and false matches", "",
         "| setting | N | N2 | M | " + " | ".join(names) + " | mean | false (unrelated videos) | false (wrong video in a clip) |",
         "|" + " --- |" * (len(names) + 7)]  # fmt: skip
    for name, x in r["results"].items():
        p, f = x["per_manipulation"], x["false"]
        L.append(f"| {name} | {x['stop_after']} | {x['shared_after']} | {x['min_frames']} | "
                 + " | ".join(pct(p[n]["found"], p[n]["clips"]) for n in names)
                 + f" | {100 * x['video_match_rate']:.1f}% | {len(f['videos'])} of {f['unrelated_videos']} | {len(f['wrong'])} |")  # fmt: skip
    L += ["", "## Frame-level match rate (sampled frames matching a keyframe of the source)", "",
          "| setting | " + " | ".join(names) + " | unrelated frames with any match |", "|" + " --- |" * (len(names) + 2)]  # fmt: skip
    for name, x in r["results"].items():
        p, f = x["per_manipulation"], x["false"]
        L.append(f"| {name} | " + " | ".join(pct(p[n]["frames_found"], p[n]["frames"]) for n in names)
                 + f" | {f['unrelated_frames']} of {f['unrelated_frames_total']} |")  # fmt: skip
    L += ["", f"## False matches against M (K = {rec['codes']}, {rec['size']} px, {rec['fps']} fps)", "",
          "| M | " + " | ".join(f"{lab}: match rate | {lab}: false (unrelated) | {lab}: false (wrong video)" for lab in r["by_min_frames"]) + " |",
          "|" + " --- |" * (1 + 3 * len(r["by_min_frames"]))]  # fmt: skip
    for i, m in enumerate(MIN_FRAMES):
        cells = []
        for rows in r["by_min_frames"].values():
            s = rows[i]
            cells += [f"{100 * s['video_match_rate']:.1f}%", str(len(s["false"]["videos"])), str(len(s["false"]["wrong"]))]
        L.append(f"| {m} | " + " | ".join(cells) + " |")
    for lab, rows in r["by_min_frames"].items():
        fs = rows[0]["false"]
        if fs["videos"] or fs["wrong"]:
            L += ["", f"False matches at M = 1, {lab} (query, its set, matched declaration, frames on the line):", ""]
            L += [f"- {q} ({s}) -> {d}: {n}" for q, s, d, n in sorted(fs["videos"] + fs["wrong"], key=lambda x: -x[3])[:40]]
    L += ["", f"## Picture-in-picture (K = {rec['codes']}, N = {rec['stop_after']}, N2 = {rec['shared_after']}, "
          f"M = {rec['min_frames']}, {rec['fps']} fps)", "",
          "| verifier | pip25 | pip40 | " + " | ".join(sorted(next(iter(r["pip_by_position"].values())))) + " | false (unrelated) |",
          "|" + " --- |" * (4 + len(next(iter(r["pip_by_position"].values()))))]  # fmt: skip
    for mode, s in r["pip"].items():
        p, pos = s["per_manipulation"], r["pip_by_position"][mode]
        L.append(f"| {mode} | {pct(p['pip25']['found'], p['pip25']['clips'])} | {pct(p['pip40']['found'], p['pip40']['clips'])} | "
                 + " | ".join(pct(*pos[k]) for k in sorted(pos)) + f" | {len(s['false']['videos'])} of {s['false']['unrelated_videos']} |")  # fmt: skip
    L += ["", f"## Stills (votes fitted on tuning; recommended: {r['fits']['recommended_still']})", "",
          "| verifier size / codes | votes | found | relationship identical | median time error (s) | false (unrelated stills) |",
          "| --- | --- | --- | --- | --- | --- |"]  # fmt: skip
    for mode, s in r["stills"].items():
        L.append(f"| {mode} | {s['votes']} | {pct(s['found'], s['stills'])} | {pct(s['relationship'], s['stills'])} | "
                 f"{s['median_time_error']} | {len(s['false'])} of {s['unrelated']} |")  # fmt: skip
    L += ["", "## Code volume (originals of this split, fitted N)", "",
          "| K | N | keyframes / min | codes / min | codes per 90-min film |", "| --- | --- | --- | --- | --- |"]
    seen = set()
    for x in r["results"].values():
        if (x["codes"], x["stop_after"]) not in seen:
            seen.add((x["codes"], x["stop_after"]))
            v = x["volume"]
            L.append(f"| {x['codes']} | {x['stop_after']} | {v['keyframes_per_minute']} | {v['codes_per_minute']} | {v['codes_per_90min_film']:,} |")
    L += ["", "## Timing (one process; seconds per minute of video unless stated)", ""]
    L += [f"- {k}: {v}" for k, v in r["timing"].items()]
    return "\n".join(L) + "\n"
