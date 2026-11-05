"""Makes the figures of DEMO.md from a corpus video and two of its test-mode clips
(run `video-simprints fetch-corpus` and `video-simprints test` first):
python docs/demo/make.py"""

import json
import subprocess
from pathlib import Path

import cv2
import numpy as np
from image_simprints.recipe import hamming, parse

from video_simprints import recipe, video

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).parent
SRC = ROOT / ".cache/corpus/nasa-atlas-v-tdrs-m.webm"
CLIP = ROOT / ".cache/clips/tuning/nasa-atlas-v-tdrs-m__caption__0.mp4"  # 136.8-166.8 s with a caption bar
PIP = ROOT / ".cache/clips/tuning/nasa-atlas-v-tdrs-m__pip25__1.mp4"  # 25% inset, bottom left, of 135-165 s
GREEN, GREY, ORANGE, WHITE = (80, 200, 80), (170, 170, 170), (40, 150, 255), (255, 255, 255)


def grab(path, t):
    ppm = subprocess.run([video.ffmpeg(), "-v", "error", "-ss", str(t), "-i", str(path), "-frames:v", "1", "-f", "image2pipe",
                          "-c:v", "ppm", "-"], capture_output=True, check=True).stdout  # fmt: skip
    return cv2.imdecode(np.frombuffer(ppm, np.uint8), cv2.IMREAD_COLOR)  # BGR


def fit(img, h):
    return cv2.resize(img, (round(img.shape[1] * h / img.shape[0]), h), interpolation=cv2.INTER_AREA)


def label(img, text, y=28, size=0.7):
    (w, h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, size, 1)
    cv2.rectangle(img, (4, y - h - 8), (16 + w, y + 8), (0, 0, 0), -1)
    cv2.putText(img, text, (10, y), cv2.FONT_HERSHEY_SIMPLEX, size, WHITE, 1, cv2.LINE_AA)
    return img


def xy(code, w, h, ox=0, oy=0):
    return int(ox + code["x"] * w), int(oy + code["y"] * h)


def draw_codes(img, codes, colour, w=None, h=None, ox=0, oy=0, numbers=False):
    w, h = w or img.shape[1], h or img.shape[0]
    for i, c in enumerate(codes):
        p, r = xy(c, w, h, ox, oy), max(4, int(c["scale"] * min(w, h) / 2))
        cv2.circle(img, p, r, colour, 2, cv2.LINE_AA)
        a = np.radians(c["angle"])
        cv2.line(img, p, (int(p[0] + r * np.cos(a)), int(p[1] - r * np.sin(a))), colour, 2, cv2.LINE_AA)
        if numbers:
            cv2.putText(img, str(i + 1), (p[0] + r, p[1] - r), cv2.FONT_HERSHEY_SIMPLEX, 0.6, colour, 2, cv2.LINE_AA)


def pairs(a, b):
    return list(zip(*np.nonzero(hamming(parse(a)[0], parse(b)[0]) <= 24)))


def side_by_side(left, right, h=420):
    l, r = fit(left, h), fit(right, h)
    return np.hstack([l, np.full((h, 24, 3), 255, np.uint8), r]), l.shape[1] / left.shape[1], l.shape[1] + 24, r.shape[1] / right.shape[1]


def main():
    decl = recipe.create(SRC)
    idx = recipe.index({"atlas-v": decl})
    kfs = decl["keyframes"]

    # 1. keyframes on the 3 s grid, with scene cuts
    tiles = [label(fit(grab(SRC, k["time"]), 150), f"{k['time']:.1f}s scene {k['scene']}" + (f" +{len(k['same_as'])} same" if k["same_as"] else ""), 24, 0.55)
             for k in kfs[:12]]  # fmt: skip
    cv2.imwrite(str(OUT / "1-keyframes.jpg"), np.vstack([np.hstack(tiles[i : i + 4]) for i in (0, 4, 8)]))

    # 2. one keyframe and its K = 10 codes, numbered by rank
    k = min(kfs, key=lambda k: abs(k["time"] - 153))
    img = grab(SRC, k["time"])
    draw_codes(img, k["codes"], GREEN, numbers=True)
    cv2.imwrite(str(OUT / "2-codes.jpg"), label(fit(img, 420), f"keyframe at {k['time']:.1f}s: {len(k['codes'])} codes"))

    # 3. a frame of the captioned clip against the keyframe: code pairs within Hamming distance 24
    s = recipe.VERIFY | {"min_frames": 3}
    frames = list(video.frames(CLIP, 1))
    hits = [[h for sp in recipe.frame_codes(f, s) for h in recipe.frame_hits(sp, idx)] for f in frames]
    i = max(range(len(hits)), key=lambda i: max((r["agreeing_codes"] for _, _, r in hits[i]), default=0))
    _, kf, r = max(hits[i], key=lambda h: h[2]["agreeing_codes"])
    sp = recipe.frame_codes(frames[i], s)[0]
    q, kimg = frames[i][:, :, ::-1].copy(), grab(SRC, kf["time"])
    pic, fq, ox, fk = side_by_side(q, kimg)
    hq, wq, hk, wk = q.shape[0] * fq, q.shape[1] * fq, kimg.shape[0] * fk, kimg.shape[1] * fk
    for c in sp["codes"]:  # the clip frame's verifier codes as dots, the keyframe's codes as circles
        cv2.circle(pic, xy(c, wq, hq), 3, GREY, -1, cv2.LINE_AA)
    draw_codes(pic, kf["codes"], GREY, wk, hk, ox)
    for a, b in pairs(sp, kf):
        cv2.circle(pic, xy(sp["codes"][a], wq, hq), 6, GREEN, -1, cv2.LINE_AA)
        cv2.line(pic, xy(sp["codes"][a], wq, hq), xy(kf["codes"][b], wk, hk, ox), GREEN, 2, cv2.LINE_AA)
    label(pic, f"clip {i}s  ->  keyframe {kf['time']:.1f}s: {r['relationship']}, {r['agreeing_codes']} agreeing codes")
    cv2.imwrite(str(OUT / "3-frame-match.jpg"), pic)

    # 4. the time vote: every frame match as (clip time, original time), and the winning line
    res = recipe.decide(hits, 1, s["min_frames"])[0]
    pts = [(c, t) for c, frame in enumerate(hits) for _, k, _ in frame for t in [k["time"], *k["same_as"]]]
    a, b, n = recipe.time_vote(np.array(pts, float))
    W, H, P = 560, 380, 50
    X = lambda c: P + c / len(hits) * (W - 2 * P)  # noqa: E731
    lo, hi = min(t for _, t in pts) - 3, max(t for _, t in pts) + 3
    Y = lambda t: H - P - (t - lo) / (hi - lo) * (H - 2 * P)  # noqa: E731
    on = lambda c, t: abs(t - (a * c + b)) <= recipe.TIME_TOLERANCE  # noqa: E731
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="sans-serif" font-size="13">',
           f'<rect width="{W}" height="{H}" fill="white"/>',
           f'<line x1="{P}" y1="{H - P}" x2="{W - P}" y2="{H - P}" stroke="black"/><line x1="{P}" y1="{P}" x2="{P}" y2="{H - P}" stroke="black"/>',
           f'<text x="{W / 2}" y="{H - 12}" text-anchor="middle">clip time (s), 1 frame per second</text>',
           f'<text x="14" y="{H / 2}" text-anchor="middle" transform="rotate(-90 14 {H / 2})">time in the original (s)</text>',
           f'<line x1="{X((lo - b) / a)}" y1="{Y(lo)}" x2="{X(len(hits))}" y2="{Y(a * len(hits) + b)}" stroke="rgb(80,200,80)" stroke-width="2"/>',
           f'<text x="{W - P}" y="{P - 10}" text-anchor="end">t = {a:.2f} c + {b:.1f}: {n} frames agree (M = {s["min_frames"]})</text>']  # fmt: skip
    for v in range(int(lo) // 5 * 5 + 5, int(hi), 5):
        svg.append(f'<text x="{P - 6}" y="{Y(v) + 4}" text-anchor="end">{v}</text>')
    for c in range(0, len(hits) + 1, 10):
        svg.append(f'<text x="{X(c)}" y="{H - P + 16}" text-anchor="middle">{c}</text>')
    svg += [f'<circle cx="{X(c)}" cy="{Y(t)}" r="4" fill="{"rgb(80,200,80)" if on(c, t) else "rgb(255,150,40)"}"/>' for c, t in pts]
    (OUT / "4-time-vote.svg").write_text("\n".join(svg + ["</svg>"]))
    print(json.dumps(res, indent=1))

    # 5. picture-in-picture: the frame alone finds little; the bottom-left tile matches
    s = recipe.VERIFY | {"tiles": 5}
    best = lambda hs: max((r["agreeing_codes"] for h in hs for _, _, r in h), default=0)  # noqa: E731
    f, sps, hits = max(((f, sps, [recipe.frame_hits(sp, idx) for sp in sps]) for f in video.frames(PIP, 1)
                        for sps in [recipe.frame_codes(f, s)]), key=lambda x: best(x[2][1:]))  # the frame whose best tile agrees most
    j = max(range(len(sps)), key=lambda j: max((r["agreeing_codes"] for _, _, r in hits[j]), default=0))
    _, kf, r = max(hits[j], key=lambda h: h[2]["agreeing_codes"])
    img, kimg = f[:, :, ::-1].copy(), grab(SRC, kf["time"])
    h, w = img.shape[:2]
    for n, (y, x) in sorted(enumerate(recipe.TILES[5], 1), key=lambda t: t[0] == j):  # the matched tile on top
        cv2.rectangle(img, (x * w // 4, y * h // 4), (x * w // 4 + w // 2, y * h // 4 + h // 2), GREEN if n == j else GREY, 8 if n == j else 3)
    pic, fq, ox, fk = side_by_side(img, kimg)
    ty, tx = recipe.TILES[5][j - 1]
    for a_, b_ in pairs(sps[j], kf):
        p = xy(sps[j]["codes"][a_], w / 2 * fq, h / 2 * fq, tx * w / 4 * fq, ty * h / 4 * fq)
        cv2.line(pic, p, xy(kf["codes"][b_], kimg.shape[1] * fk, kimg.shape[0] * fk, ox), GREEN, 2, cv2.LINE_AA)
    whole = max((r["agreeing_codes"] for _, _, r in hits[0]), default=0)
    label(pic, f"whole frame: {whole} agreeing codes; tile {j}: {r['agreeing_codes']}, {r['relationship']}")
    cv2.imwrite(str(OUT / "5-pip-tiles.jpg"), pic)


if __name__ == "__main__":
    main()
