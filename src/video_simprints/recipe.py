"""The video recipe: keyframes on a time grid, image simprints on each (creator); frames
matched one by one, then a time vote (verifier). RECIPE.md describes every step."""

import math
from bisect import bisect_right
from collections import Counter, deque

import cv2
import numpy as np
from image_simprints import generate, match
from image_simprints.recipe import hamming, mark_stop_codes, parse, prepare, settings_of, version_of

from . import video

RECIPE = "video-simprints/0.1"
DEFAULTS = {  # chosen on the tuning split (tests/corpus/report-tuning)
    "codes": 10,  # codes per keyframe
    "spread": False,  # an equal share of the codes from each horizontal third (did not help)
    "stop_after": 1000,  # drop codes that agree with codes of more than this many other keyframes (1000: off, as fitted)
}
VERIFY = {
    "fps": 2,  # frames sampled per second of the checked clip
    "prepared_size": 1024,  # image-simprints verifier size
    "min_frames": 1,  # frames that must agree with one time line (fitted; raise it for a large index)
}
SAMPLE_FPS = 5  # frames decoded per second (as iscc-sdk's scene detection)
GRID = 3.0  # seconds between keyframes
CUT = 0.4  # ffmpeg scene score at or above which a frame starts a new scene
CUT_MARGIN = 0.5  # seconds: grid points this close to a cut are skipped
WINDOW = 0.4  # seconds: a blurred grid frame is replaced by the sharpest frame this close
BLUR = 35.0  # variance of the Laplacian below which a grid frame counts as blurred (10th percentile on tuning)
UNIFORM = 8.0  # standard deviation of grey below which a frame counts as black or uniform
ALL_CODES = 512  # image-simprints' CANDIDATES cap: the full ranked list
SLOPE = 0.1  # time vote: slope 1 +/- this
TIME_TOLERANCE = GRID  # time vote: seconds a frame may lie off the line


def version_string(s: dict) -> str:
    return RECIPE + "".join(f";{k}={int(v)}" for k, v in s.items() if v != DEFAULTS[k])


# --- creator ---------------------------------------------------------------------------


def sharpness(grey: np.ndarray) -> float:
    return float(cv2.Laplacian(grey, cv2.CV_64F).var())


def candidates(path) -> dict:
    """Every grid keyframe of a video with its full ranked list of image codes, before
    selection, de-duplication and stop codes (create() does those)."""
    step, win = round(GRID * SAMPLE_FPS), round(WINDOW * SAMPLE_FPS)
    scores, out, buf = [], [], deque(maxlen=2 * win + 1)

    def pick(g):  # the grid frame, or the sharpest in its window if it is blurred
        near = [(i, f, prepare(f, 512)) for i, f in buf if abs(i - g) <= win]
        i, f, grey = next(x for x in near if x[0] == g)
        if sharpness(grey) < BLUR:
            i, f, grey = max(near, key=lambda x: (sharpness(x[2]), -abs(x[0] - g), -x[0]))
        if grey.std() < UNIFORM:
            return
        sp = generate(f, "creator", {"creator_codes": ALL_CODES})
        if sp["codes"]:
            out.append({"grid": g / SAMPLE_FPS, "time": i / SAMPLE_FPS, "prepared_size": sp["prepared_size"], "codes": sp["codes"]})

    n = 0
    for n, f in enumerate(video.frames(path, SAMPLE_FPS, scores), 1):
        buf.append((n - 1, f))
        if (g := n - 1 - win) >= 0 and g % step == 0:
            pick(g)
    for g in range(max(0, n - win) + (-max(0, n - win)) % step, n, step):  # the last windows, cut short by the end
        pick(g)
    cuts = [i / SAMPLE_FPS for i, s in enumerate(scores) if i and s >= CUT]
    keep = [k for k in out if not any(abs(k["grid"] - c) <= CUT_MARGIN for c in cuts)]
    for k in keep:
        k["scene"] = bisect_right(cuts, k["grid"])
    return {"duration": n / SAMPLE_FPS, "cuts": cuts, "keyframes": keep}


def spread(codes: list, k: int) -> list:
    """The top k//3 codes (by rank) from each horizontal third, the rest by rank."""
    chosen = set()
    for third in range(3):
        mine = [c["chunk_idx"] for c in codes if min(int(c["x"] * 3), 2) == third]
        chosen.update(mine[: k // 3])
    chosen.update([c["chunk_idx"] for c in codes if c["chunk_idx"] not in chosen][: k - len(chosen)])
    return [c for c in codes if c["chunk_idx"] in chosen]


def create(path, settings: dict | None = None, cands: dict | None = None) -> dict:
    """The declaration of a video: its keyframes, each a generate() result with codes
    that also carry keyframe index, time and scene. `cands` reuses candidates(path)."""
    s = DEFAULTS | (settings or {})
    c = cands or candidates(path)
    image_version = version_of(settings_of({"creator_codes": s["codes"]}))
    kfs = []
    for k in c["keyframes"]:
        codes = spread(k["codes"], s["codes"]) if s["spread"] else k["codes"][: s["codes"]]
        kf = {"recipe_version": image_version, "time": k["time"], "scene": k["scene"], "same_as": [],
              "prepared_size": k["prepared_size"], "codes": codes}  # fmt: skip
        if (twin := duplicate_of(kf, kfs)) is not None:
            twin["same_as"].append(kf["time"])
        else:
            kfs.append(kf)
    kfs = [k | {"codes": [x for x in k["codes"] if not x.get("stop")]} for k in mark_stop_codes(kfs, s["stop_after"])]
    kfs = [k for k in kfs if len(k["codes"]) >= 2]  # match() needs 2 agreeing codes
    for i, k in enumerate(kfs):
        k["codes"] = [x | {"keyframe": i, "time": k["time"], "scene": k["scene"]} for x in k["codes"]]
    return {"recipe_version": version_string(s), "duration": c["duration"], "cuts": c["cuts"], "keyframes": kfs}


def duplicate_of(kf: dict, kfs: list) -> dict | None:
    """An earlier keyframe this one matches as identical with at least half its codes."""
    if not kfs:
        return None
    mine = parse(kf)[0]
    every = [parse(k)[0] for k in kfs]
    owner = np.repeat(np.arange(len(kfs)), [len(x) for x in every])
    near = hamming(mine, np.concatenate(every)) <= 24
    hits = Counter(o for row in near for o in set(owner[row].tolist()))
    for o, n in hits.items():
        if 2 * n >= len(mine):
            r = match(kf, kfs[o])
            if r["relationship"] == "identical" and 2 * r["agreeing_codes"] >= len(mine):
                return kfs[o]
    return None


# --- verifier --------------------------------------------------------------------------


def index(declarations: dict) -> dict:
    """An in-memory index of every keyframe of {id: create() result}."""
    kfs = [(d, k) for d, decl in declarations.items() for k in decl["keyframes"]]
    codes = [parse(k)[0] for _, k in kfs]
    return {"keyframes": kfs, "codes": np.concatenate(codes) if codes else np.zeros((0, 4), np.uint64),
            "owner": np.repeat(np.arange(len(kfs)), [len(c) for c in codes])}  # fmt: skip


def frame_hits(query: dict, idx: dict) -> list:
    """(declaration id, keyframe, match result) for every keyframe the frame matches."""
    q = parse(query)[0]
    if not len(q) or not len(idx["codes"]):
        return []
    near = hamming(q, idx["codes"]) <= 24
    hits = Counter(o for row in near for o in set(idx["owner"][row].tolist()))
    out = []
    for o, n in hits.items():
        if n >= 2:
            d, k = idx["keyframes"][o]
            r = match(query, k)
            if r["relationship"] != "none":
                out.append((d, k, r))
    return out


def verify_still(source, idx: dict, settings: dict | None = None) -> list:
    """A single image against the keyframes: the best keyframe per declaration."""
    s = VERIFY | (settings or {})
    best = {}
    for d, k, r in frame_hits(generate(source, "verifier", {"prepared_size": s["prepared_size"]}), idx):
        if d not in best or r["agreeing_codes"] > best[d]["agreeing_codes"]:
            best[d] = {"declaration": d, "time": k["time"], "relationship": r["relationship"],
                       "overlap_fraction": r["overlap_fraction"], "agreeing_codes": r["agreeing_codes"]}  # fmt: skip
    return sorted(best.values(), key=lambda h: -h["agreeing_codes"])


def verify(path, idx: dict, settings: dict | None = None) -> list:
    """A clip against the keyframes: per declaration with enough frames on one time
    line, the matched range in the original and the dominant relationship."""
    s = VERIFY | (settings or {})
    hits = [frame_hits(generate(f, "verifier", {"prepared_size": s["prepared_size"]}), idx)
            for f in video.frames(path, s["fps"])]  # fmt: skip
    return decide(hits, s["fps"], s["min_frames"])


def decide(hits: list, fps: float, min_frames: int) -> list:
    """The time vote over per-frame hits (frame i at i / fps in the clip)."""
    out = []
    for d in sorted({h[0] for frame in hits for h in frame}):
        pts = [(i / fps, t, r) for i, frame in enumerate(hits) for dd, k, r in frame if dd == d
               for t in [k["time"], *k["same_as"]]]  # fmt: skip
        line = time_vote(np.array([(c, t) for c, t, _ in pts]))
        if line is None or line[2] < min_frames:
            continue
        a, b, n = line
        inl = [(c, r) for c, t, r in pts if abs(t - (a * c + b)) <= TIME_TOLERANCE]
        per_frame = {}
        for c, r in inl:  # the strongest inlier match per frame
            if c not in per_frame or r["agreeing_codes"] > per_frame[c]["agreeing_codes"]:
                per_frame[c] = r
        rel = Counter(r["relationship"] for r in per_frame.values()).most_common(1)[0][0]
        c0, c1 = min(per_frame), max(per_frame)
        out.append({"declaration": d, "frames": n, "relationship": rel,
                    "overlap_fraction": {side: round(float(np.median([r["overlap_fraction"][side] for r in per_frame.values()
                                                                      if r["relationship"] == rel])), 4)
                                         for side in ("verifier", "candidate")},
                    "clip": [c0, c1], "original": [round(a * c0 + b, 2), round(a * c1 + b, 2)], "slope": round(a, 3)})  # fmt: skip
    return sorted(out, key=lambda h: -h["frames"])


def time_vote(p: np.ndarray):
    """The line t = a c + b (a within 1 +/- SLOPE) with the most distinct clip times
    c within TIME_TOLERANCE of it: (a, b, count), or None. Lines through each point
    with slope 1, and through each pair of points, are tried."""
    if not len(p):
        return None
    c, t = p[:, 0], p[:, 1]
    i, j = np.triu_indices(len(p), 1)
    ok = c[j] != c[i]
    i, j = i[ok], j[ok]
    a = (t[j] - t[i]) / (c[j] - c[i])
    ok = np.abs(a - 1) <= SLOPE
    a = np.concatenate([np.ones(len(p)), a[ok]])
    b = np.concatenate([t - c, t[i[ok]] - a[len(p) :] * c[i[ok]]])
    res = np.abs(t[None, :] - (a[:, None] * c[None, :] + b[:, None]))
    inl = res <= TIME_TOLERANCE
    order = np.argsort(c, kind="stable")
    starts = np.flatnonzero(np.r_[True, np.diff(c[order]) != 0])
    count = np.logical_or.reduceat(inl[:, order], starts, axis=1).sum(1)
    err = np.where(inl, res, 0).sum(1)
    best = np.lexsort((err, -count))[0]
    return float(a[best]), float(b[best]), int(count[best])
