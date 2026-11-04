"""A synthetic video with known cuts: three panning scenes of random shapes and a black gap.

scene 0: 0-6.2 s, scene 1: 6.2-12.4 s, black: 12.4-15.8 s, scene 3: 15.8-30 s.
Grid points: 0, 3 (scene 0); 6 (0.2 s from a cut: skipped); 9 (scene 1); 12 (cut: skipped);
15 (black: skipped); 18, 21, 24, 27 (scene 3)."""

import subprocess

import cv2
import numpy as np
import pytest
from image_simprints import generate

from video_simprints import create, index, recipe, verify, verify_still, video


def shapes(path, seed):
    rng = np.random.default_rng(seed)
    im = np.full((720, 3200, 3), (40, 200, 120)[seed], np.uint8)
    for _ in range(400):
        c = tuple(int(v) for v in rng.integers(0, 256, 3))
        x, y = int(rng.integers(0, 3200)), int(rng.integers(0, 720))
        if rng.random() < 0.5:
            cv2.circle(im, (x, y), int(rng.integers(8, 60)), c, -1)
        else:
            cv2.rectangle(im, (x, y), (x + int(rng.integers(10, 120)), y + int(rng.integers(10, 120))), c, -1)
    cv2.imwrite(str(path), im)


def ff(*args):
    subprocess.run([video.ffmpeg(), "-nostdin", "-y", "-v", "error", *map(str, args)], check=True)


@pytest.fixture(scope="module")
def clip(tmp_path_factory):
    d = tmp_path_factory.mktemp("video")
    for i in range(3):
        shapes(d / f"{i}.png", i)
    pan = "crop=1280:720:x='t*100':y=0,setsar=1,format=yuv420p"
    ff("-loop", 1, "-framerate", 25, "-t", 6.2, "-i", d / "0.png", "-loop", 1, "-framerate", 25, "-t", 6.2, "-i", d / "1.png",
       "-f", "lavfi", "-i", "color=black:size=1280x720:rate=25:duration=3.4", "-loop", 1, "-framerate", 25, "-t", 14.2, "-i", d / "2.png",
       "-filter_complex", f"[0:v]{pan}[a];[1:v]{pan}[b];[2:v]setsar=1,format=yuv420p[k];[3:v]{pan}[c];[a][b][k][c]concat=n=4:v=1",
       "-c:v", "libx264", "-crf", 18, d / "synthetic.mp4")  # fmt: skip
    return d / "synthetic.mp4"


def test_keyframe_rule(clip):
    c = recipe.candidates(clip)
    assert c["duration"] == pytest.approx(30, abs=0.2)
    assert [round(x, 1) for x in c["cuts"]] == [6.2, 12.4, 15.8]
    assert [(k["grid"], k["scene"]) for k in c["keyframes"]] == [(0, 0), (3, 0), (9, 1), (18, 3), (21, 3), (24, 3), (27, 3)]
    assert all(abs(k["time"] - k["grid"]) <= recipe.WINDOW for k in c["keyframes"])


def test_codes_are_image_simprints(clip):
    """Without spread, a keyframe's codes are generate(frame, "creator", {"creator_codes": K})."""
    frame = next(f for i, f in enumerate(video.frames(clip, recipe.SAMPLE_FPS)) if i == 9 * recipe.SAMPLE_FPS)
    expected = generate(frame, "creator", {"creator_codes": 10})
    kf = next(k for k in create(clip, {"spread": False, "stop_after": 1000})["keyframes"] if k["time"] == 9)
    assert kf["recipe_version"] == expected["recipe_version"]
    assert [x["code"] for x in kf["codes"]] == [x["code"] for x in expected["codes"]]
    assert all(x["keyframe"] == 2 and x["time"] == 9 and x["scene"] == 1 for x in kf["codes"])


def test_spread():
    codes = [{"chunk_idx": i, "x": x} for i, x in enumerate([0.1, 0.2, 0.15, 0.5, 0.9, 0.95])]
    assert [c["chunk_idx"] for c in recipe.spread(codes, 3)] == [0, 3, 4]  # the best of each third, in rank order
    assert [c["chunk_idx"] for c in recipe.spread(codes, 5)] == [0, 1, 2, 3, 4]  # 1 per third, then the rest by rank


def test_determinism(clip):
    assert create(clip) == create(clip)


def test_vertical_crop_and_excerpt(clip, tmp_path):
    idx = index({"synthetic": create(clip)})
    ff("-ss", 16, "-t", 12, "-i", clip, "-c:v", "libx264", "-crf", 23, tmp_path / "excerpt.mp4")
    ff("-ss", 16, "-t", 12, "-i", clip, "-vf", "crop=404:720", "-c:v", "libx264", "-crf", 23, tmp_path / "vertical.mp4")
    for name, rel in (("excerpt", {"identical", "overlapping"}), ("vertical", {"contained_in"})):
        top = verify(tmp_path / f"{name}.mp4", idx, {"min_frames": 2})[0]
        assert top["declaration"] == "synthetic" and top["relationship"] in rel, (name, top)
        assert 16 - 3 <= top["original"][0] < top["original"][1] <= 28 + 3, (name, top)  # inside the excerpt
        assert abs(top["slope"] - 1) <= 0.1
    ff("-ss", 22.6, "-i", clip, "-frames:v", 1, tmp_path / "still.png")
    hit = verify_still(tmp_path / "still.png", idx, {"still_votes": 2})[0]
    assert hit["declaration"] == "synthetic" and abs(hit["time"] - 22.6) <= 3


def test_time_vote():
    p = np.array([(0, 100), (1, 101), (2, 102.2), (3, 103), (4, 50), (5, 105)])
    a, b, n = recipe.time_vote(p)
    assert n == 5 and abs(a - 1) <= 0.1 and abs(b - 100) <= 1
