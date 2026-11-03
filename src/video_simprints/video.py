"""Decoding with the system ffmpeg, run as a subprocess. No decoder is bundled."""

import re
import shutil
import subprocess
import threading

import numpy as np


class VideoError(ValueError):
    """ffmpeg is missing, or cannot decode the source."""


def ffmpeg() -> str:
    path = shutil.which("ffmpeg")
    if not path:
        raise VideoError("ffmpeg not found on PATH; install it (see README)")
    return path


def version() -> str:
    """The first line of `ffmpeg -version`, for reports."""
    return subprocess.run([ffmpeg(), "-version"], capture_output=True, text=True, check=True).stdout.split("\n")[0]


def frames(path, fps: float, scores: list | None = None):
    """Yield RGB uint8 frames sampled at `fps` (ffmpeg's fps filter: frame i is the
    frame shown at i / fps after the first). If `scores` is a list, ffmpeg's scene
    score of each sampled frame against the one before (0 to 1) is appended to it
    once the video is done."""
    vf = f"fps={fps}" + (",select='gte(scene,0)',metadata=print" if scores is not None else "")
    cmd = [ffmpeg(), "-nostdin", "-v", "info" if scores is not None else "error", "-i", str(path),
           "-map", "0:v:0", "-vf", vf, "-f", "image2pipe", "-c:v", "ppm", "-"]  # fmt: skip
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    err = []
    reader = threading.Thread(target=lambda: err.append(p.stderr.read()), daemon=True)
    reader.start()
    try:
        while head := p.stdout.readline():  # PPM: "P6\n", "w h\n", "255\n", then the pixels
            w, h = map(int, p.stdout.readline().split())
            p.stdout.readline()
            yield np.frombuffer(p.stdout.read(w * h * 3), np.uint8).reshape(h, w, 3)
    finally:
        p.stdout.close()
        p.wait()
        reader.join()
    if p.returncode:
        raise VideoError(f"ffmpeg failed on {path}: {err[0].decode(errors='replace')[-500:]}")
    if scores is not None:  # metadata=print logs "lavfi.scene_score=S" once per frame, in order
        scores.extend(float(s) for s in re.findall(rb"lavfi\.scene_score=([\d.]+)", err[0]))
