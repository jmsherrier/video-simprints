# video-simprints

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue)](pyproject.toml)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Status: proof of concept](https://img.shields.io/badge/status-proof%20of%20concept-orange)](#status)

Granular video codes. A video gets one keyframe every 3 seconds, and each keyframe
gets a few [image simprints](https://github.com/jmsherrier/image-simprints):
256-bit codes of distinctive spots, with position, scale and angle. A clip found
online is checked frame by frame against those keyframes, and the matching
frames must line up in time. The answer says which video, which part of it, and
how the picture was changed: "excerpt 12:30–13:10, cropped to vertical".

This finds what whole-frame video fingerprints miss: 16:9 cropped to 9:16,
picture-in-picture, reframing, borders, overlays and captions, and single
stills.

<a id="status"></a>**Status:** proof of concept, recipe `video-simprints/0.1`.
Treat codes as test data.

## Design credit

The design is Sebastian Posth's (Liccium): image simprints on keyframes chosen
on a fixed time grid, with scene cuts only as a filter, so that independent
apps pick the same frames; fewer codes per keyframe than for images; video
stop codes for logos and lower thirds; and a verifier that confirms each frame
geometrically, then votes on time. It extends ISCC's per-scene video
simprints, which find excerpts in time but describe whole frames.

## Install

Python 3.12 on macOS (Apple Silicon) or Linux (Windows works too). Videos are
decoded by **the system `ffmpeg`**, run as a subprocess; no decoder is bundled.
Install it first (`brew install ffmpeg`, `apt install ffmpeg`).

```sh
pip install git+https://github.com/jmsherrier/video-simprints   # pulls image-simprints v0.3.0 (pinned)
pip install -e ".[test]" && pytest                             # from a checkout
```

## Use

```python
from video_simprints import create, index, verify, verify_still

# Creator side, at declaration: store this with the declaration (JSON).
declaration = create("film.mp4")

# Verifier side: an index of declarations, then a clip or a still.
idx = index({"film-123": declaration})
for hit in verify("found_online.mp4", idx):
    print(hit["declaration"], hit["original"], hit["relationship"])
    # film-123 [750.4, 790.1] contained_in   (a vertical crop of 12:30-13:10)
print(verify_still("screenshot.png", idx))   # [{declaration, time, relationship, ...}]
```

`create(path, settings)` returns `{recipe_version, duration, cuts, keyframes}`.
Each keyframe is an image-simprints `generate()` result plus `time`, `scene` and
`same_as` (times of near-identical keyframes folded into it), and each code also
carries `keyframe`, `time` and `scene`.

`verify(path, idx, settings)` returns one entry per matching declaration:
`frames` (frames agreeing on one time line), `clip` and `original` (the matched
range in each, in seconds), `slope`, `relationship` (`identical`,
`contained_in`: the clip shows part of the original's picture, `contains`: the
original's picture is inside the clip's, as in picture-in-picture, or
`overlapping`) and `overlap_fraction`.

Settings and defaults: creator `codes=10`, `spread=True`, `stop_after=3`;
verifier `fps=1`, `prepared_size=512`, `min_frames=3`. [RECIPE.md](RECIPE.md)
specifies every step.

The command line does the same: `video-simprints create film.mp4 > film.json`,
`video-simprints verify clip.mp4 film.json`.

## Test mode

```sh
video-simprints fetch-corpus                 # 16 videos, ~1.9 GB, into .cache/corpus (gitignored)
video-simprints test --split tuning          # fits N and M; tests/corpus/report-tuning
video-simprints test --split test --fits tests/corpus/report-tuning
```

[`tests/corpus/manifest.csv`](tests/corpus/manifest.csv) lists the corpus with
URL, licence and SHA-256: the Blender open movies (CC BY), NASA videos from
Wikimedia Commons and a public-domain newsreel, split into tuning and test, each
with unrelated videos. Test mode makes the manipulated clips with ffmpeg
(excerpts of 10, 30 and 60 s, a 9:16 centre crop, picture-in-picture at 25% and
40% of the width inside an unrelated video, 240p at 150 kbit/s, a caption bar, a
corner logo, and screenshots), sweeps `codes` over {5, 10, 20} with and without
`spread`, `stop_after` (N), the verifier's `fps` {1, 2} and `prepared_size`
{512, 1024}, and `min_frames` (M). N and M are fitted on the tuning split only.
Output: `report.json` and `summary.md`.

## Documents

- [RECIPE.md](RECIPE.md): the recipe, precisely enough to reimplement.
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md): dependencies, FFmpeg, and
  the test corpus credits.

Apache-2.0. © 2026 Joseph Sherrier.
