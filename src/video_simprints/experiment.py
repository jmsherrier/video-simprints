"""Two experiments at the fitted settings (K = 10, N off, N2 = 0, verifier 1024 px at
1 fps): branding labels instead of a high M, and overlapping tiles for
picture-in-picture. Run after `test` on the same split (it reuses its clips and codes)."""

import json
import pickle
import statistics
import time
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from . import recipe, video
from .evaluate import TILED, _W, _hits, codes_of, gen
from .testmode import CACHE, MANIPULATIONS, corpus, probe

K, N, N2, FPS = 10, 1000, 0, 1  # the fitted settings (tests/corpus/report-tuning)
EXTRA = [p for p in recipe.TILES[9] if p not in recipe.TILES[4]]  # the 3x3 grid's tiles beyond the quarters
PICK = {"tiles4": [0, 1, 2, 3], "tiles5": [0, 1, 2, 3, 4 + EXTRA.index((1, 1))], "tiles9": list(range(9))}
MODES = ("1024", *(f"1024+{t}" for t in PICK))
BRANDING = (0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, None)  # swept share of shared codes (None: no labels)
MS = (1, 3, 10)
VARIANTS = ("drop", "label")  # shared codes left out of the index (as fitted), or kept and labelled


def extra_codes(c: dict) -> list:
    """Per frame at 1 fps, the codes of the five tiles of the 3x3 grid that are not quarters."""
    cache = CACHE / "eval" / (c["id"] + ".extra.pkl")
    if not cache.exists():
        frames = [f for i, f in enumerate(video.frames(c["path"], 2)) if i % 2 == 0]  # as codes_of's frames[::2]
        cache.write_bytes(pickle.dumps([[gen(t, 1024) for t in recipe.tiles(f, EXTRA)] for f in frames]))
    return pickle.loads(cache.read_bytes())


def _init(path):
    decls, _W["cols"], _W["U"], originals = pickle.loads(Path(path).read_bytes())
    ds = decls[(K, N)]
    _W["kfs"] = [(d, kf) for d in originals for kf in ds[d]["keyframes"]]
    _W["sets"] = recipe.sharers(_W["kfs"], {d: x for d, x in ds.items() if d not in originals})


def _indexes(ignore) -> dict:
    kfs, sets = _W["kfs"], _W["sets"]
    out = {"drop": recipe.index_keyframes(recipe.unshared(kfs, sets, N2, ignore)),
           "label": recipe.index_keyframes(kfs) | {"shared": recipe.shared_flags(sets, N2, ignore)}}  # fmt: skip
    for idx in out.values():
        idx["cols"] = np.array([_W["cols"][(d, kf["time"], x["chunk_idx"])] for d, kf in idx["keyframes"] for x in kf["codes"]], int)
    return out


def _query(c: dict):
    own = c.get("background") if c["manipulation"].startswith("pip") else None if c["source"] else c["id"].split("__")[0]
    idxs = _indexes(own)
    sets = codes_of(c)
    modes = {"1024": _hits(sets["1024"][::2], idxs)}
    if c["manipulation"] in TILED:
        nine = [a + b for a, b in zip(sets["tiles"][::2], extra_codes(c))]
        flat = _hits([sp for t in nine for sp in t], idxs)
        for vk, h in flat.items():
            per_frame = [h[i : i + 9] for i in range(0, len(h), 9)]
            for name, pick in PICK.items():
                modes.setdefault(f"1024+{name}", {})[vk] = [base + sum((t[j] for j in pick), []) for base, t in zip(modes["1024"][vk], per_frame)]
    out = {}
    for mode, per in modes.items():
        for vk, frames in per.items():
            res = [(r["declaration"], r["frames"], *r["original"], r["relationship"], r["shared_fraction"]) for r in recipe.decide(frames, FPS, 1)]
            out[(mode, vk)] = (res, len(frames), sum(any(h[0] == c["source"] for h in f) for f in frames))
    return c["id"], out


def run(split: str, workers: int) -> dict:
    queries = [c for c in pickle.loads((CACHE / "eval" / f"results-{split}.pkl").read_bytes())["queries"]
               if not c["manipulation"].endswith("still")]  # fmt: skip
    order = sorted(queries, key=lambda c: -(c["end"] - c["start"]) * (9 if c["manipulation"] in TILED else 1))
    with Pool(workers, _init, (str(CACHE / "eval" / f"decls-{split}.pkl"),)) as pool:
        return {"queries": queries, "results": dict(pool.imap_unordered(_query, order))}


def score(data: dict, mode: str, vk: str, m: int, branding) -> dict:
    """Video-level match rate per manipulation (the top unlabelled match is the source,
    time within 3 s), sources lost to a label, other declarations labelled, and the
    remaining (unlabelled) false matches."""
    per = {name: [0, 0] for name in MANIPULATIONS}
    out = {"lost": [], "labelled": [], "false": []}
    for c in data["queries"]:
        r = data["results"][c["id"]].get((mode, vk))
        if r is None:
            continue
        res = [x for x in r[0] if x[1] >= m]
        brand = [x for x in res if branding is not None and x[5] >= branding]
        kept = [x for x in res if x not in brand]
        row = lambda x: (c["id"], c["set"], x[0], x[1], x[5], c.get("background") if c["manipulation"].startswith("pip") else None)  # noqa: E731
        out["lost"] += [row(x) for x in brand if x[0] == c["source"]]
        out["labelled"] += [row(x) for x in brand if x[0] != c["source"]]
        out["false"] += [row(x) + (c["manipulation"] == "unrelated",) for x in kept if x[0] != c["source"]]
        if c["manipulation"] != "unrelated":
            top = max(kept, key=lambda x: x[1], default=None)
            p = per[c["manipulation"]]
            p[0] += top is not None and top[0] == c["source"] and top[2] <= c["end"] + 3 and top[3] >= c["start"] - 3
            p[1] += 1
    clips = [f / n for f, n in per.values() if n]
    return out | {"per": per, "rate": sum(clips) / len(clips)}


def fit(data: dict):
    """On tuning, at M = 3 without tiles: the branding share with the fewest unlabelled
    false matches, then the best match rate (ties: the larger share; None is largest)."""
    rank = {f: score(data, "1024", "label", 3, f) for f in BRANDING}
    return max(BRANDING, key=lambda f: (-len(rank[f]["false"]), rank[f]["rate"], 2 if f is None else f))


def timing(split: str, branding) -> dict:
    """Seconds per minute of video, one process, on the first original's first 25% PiP clip."""
    rows = [r for r in corpus() if r["split"] == split]
    decls = pickle.loads((CACHE / "eval" / f"decls-{split}.pkl").read_bytes())[0][(K, N)]
    r = next(r for r in rows if r["role"] == "original")
    others = {x["name"]: decls[x["name"]] for x in rows if x["role"] == "unrelated"}
    idx = recipe.index({r["name"]: decls[r["name"]]}, N2, others, label=True)
    path = CACHE / "clips" / split / f"{r['name']}__pip25__0.mp4"
    out = {}
    for mode in MODES:
        t = time.perf_counter()
        n = int(mode.split("tiles")[1]) if "tiles" in mode else 0
        recipe.verify(path, idx, {"fps": FPS, "prepared_size": 1024, "tiles": n, "min_frames": 3, "branding": branding})
        out[mode] = round((time.perf_counter() - t) / (probe(path)[0] / 60), 1)
    return out


def main(split: str, out: Path, fits_from: Path | None, workers: int):
    saved = CACHE / "eval" / f"experiment-{split}.pkl"  # delete it to rerun the matching
    data = pickle.loads(saved.read_bytes()) if saved.exists() else run(split, workers)
    saved.write_bytes(pickle.dumps(data))
    branding = json.loads((fits_from / "report.json").read_text())["branding"] if fits_from else fit(data)
    sets = {r["name"]: r["set"] for r in corpus()}
    rows = {f"{v} M={m}": score(data, "1024", v, m, branding if v == "label" else None) for m in (3, 10) for v in VARIANTS}
    sweep = {str(f): score(data, "1024", "label", 3, f) for f in BRANDING}
    pip = {f"{mode} {v} M={m}": score(data, mode, v, m, branding if v == "label" else None) for mode in MODES for v in VARIANTS for m in MS}
    pos = {}
    for key in pip:
        mode, v, m = key.split(" ")
        p = pos[key] = {}
        for c in data["queries"]:
            if c["manipulation"].startswith("pip"):
                res = [x for x in data["results"][c["id"]][(mode, v)][0] if x[1] >= int(m[2:]) and not (v == "label" and x[5] >= branding)]
                top = max(res, key=lambda x: x[1], default=None)
                hit = top is not None and top[0] == c["source"] and top[2] <= c["end"] + 3 and top[3] >= c["start"] - 3
                k = f"{c['manipulation']} {'centre' if c['position'] == 'centre' else 'corner'}"
                p[k] = [p.get(k, [0, 0])[0] + hit, p.get(k, [0, 0])[1] + 1]
    report = {"split": split, "ffmpeg": video.version(), "fitted_on": fits_from.name if fits_from else split, "branding": branding,
              "rows": rows, "sweep": sweep, "pip": pip, "pip_by_position": pos, "timing": timing(split, branding)}  # fmt: skip
    out.mkdir(parents=True, exist_ok=True)
    (out / "report.json").write_text(json.dumps(report, indent=1, default=str))
    (out / "summary.md").write_text(summary(report, sets))
    print((out / "summary.md").read_text())


def summary(r: dict, sets: dict) -> str:
    pct = lambda a, b: f"{100 * a / b:.0f}%" if b else "-"  # noqa: E731
    names = [n for n in MANIPULATIONS]
    same = lambda xs: sum(sets.get(x[2]) in (x[1], sets.get(x[5])) for x in xs)  # noqa: E731
    cnt = lambda s: (f"{len(s['lost'])} | {same(s['labelled'])} / {len(s['labelled']) - same(s['labelled'])} | "  # noqa: E731
                     f"{sum(x[6] for x in s['false'])} | {sum(not x[6] for x in s['false'])}")
    head = "source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip)"
    L = [f"# video-simprints experiments: {r['split']} split", "",
         f"{r['ffmpeg']}. K = {K}, N off, N2 = {N2} (counted against every other video of the split, leaving the query "
         f"out), verifier 1024 px at {FPS} fps. **drop**: shared codes left out of the index (the fitted default). "
         f"**label**: shared codes kept and marked; a match whose agreeing codes are at least {r['branding']} shared "
         f"(fitted on {r['fitted_on']}) is labelled `shared_branding`, not counted as a match.", "",
         "## Branding labels", "",
         "| index | M | " + " | ".join(names) + f" | mean | {head} |", "|" + " --- |" * (len(names) + 7)]  # fmt: skip
    for key, s in r["rows"].items():
        v, m = key.split(" ")
        L.append(f"| {v} | {m[2:]} | " + " | ".join(pct(*s["per"][n]) for n in names) + f" | {100 * s['rate']:.1f}% | {cnt(s)} |")
    L += ["", "Share of shared codes swept at M = 3 (label):", "", f"| share | mean | {head} |", "|" + " --- |" * 6]
    L += [f"| {f} | {100 * s['rate']:.1f}% | {cnt(s)} |" for f, s in r["sweep"].items()]
    s = r["rows"]["label M=3"]
    for title, xs in (("Unlabelled false matches", s["false"]), ("Labelled", s["labelled"]), ("Sources lost to the label", s["lost"])):
        if xs:
            L += ["", f"{title}, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):", ""]
            L += [f"- {x[0]} ({x[1]}{', ' + sets[x[5]] if x[5] else ''}) -> {x[2]} ({sets.get(x[2])}): {x[3]}, {x[4]}" for x in sorted(xs, key=lambda x: -x[3])[:40]]
    keys = sorted(next(iter(r["pip_by_position"].values())))
    L += ["", "## Picture-in-picture", "",
          "Insets at 25% and 40% of the width of a 1080p unrelated video, at a random corner or the centre. tiles4: the "
          "quarters; tiles5: the quarters and a centre tile; tiles9: a 3x3 grid of half-size tiles overlapping by half.", "",
          "| verifier | index | M | pip25 | pip40 | " + " | ".join(keys) + f" | {head} |", "|" + " --- |" * (9 + len(keys))]  # fmt: skip
    for key, s in r["pip"].items():
        mode, v, m = key.split(" ")
        pos = r["pip_by_position"][key]
        L.append(f"| {mode} | {v} | {m[2:]} | {pct(*s['per']['pip25'])} | {pct(*s['per']['pip40'])} | "
                 + " | ".join(pct(*pos[k]) for k in keys) + f" | {cnt(s)} |")  # fmt: skip
    L += ["", "Verifier time (one process, label index, seconds per minute of a 25% PiP clip):", ""]
    L += [f"- {k}: {v}" for k, v in r["timing"].items()]
    return "\n".join(L) + "\n"
