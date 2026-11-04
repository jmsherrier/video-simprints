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
idx = index({"film-123": declaration})   # or index(declarations, shared_after=0, against=channel_videos)
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

Settings and defaults, fitted on the tuning split: creator `codes=10`,
`spread=False`, `stop_after=1000` (per-video stop codes off: they did not help);
verifier `fps=1`, `prepared_size=1024`, `min_frames=10`, `still_votes=3`,
`tiles=0` (5 for small picture-in-picture: the quarters and a centre tile, at
about 4× the cost). The index takes `shared_after` (index-level stop codes, 0
fitted) and `against`, a reference collection such as the declaring channel's
other videos: codes shared with other videos (series intros, studio sets, logo
bugs) are left out, or with `label=True` kept and marked, so that a match made
mostly of them (`branding=0.6`, fitted) is returned as `shared_branding`.
[RECIPE.md](RECIPE.md) specifies every step.

The command line does the same: `video-simprints create film.mp4 > film.json`,
`video-simprints verify clip.mp4 film.json`.

## Test mode

```sh
video-simprints fetch-corpus                 # 88 videos, ~4 GB, into .cache/corpus (gitignored)
video-simprints test --split tuning          # fits N, N2 and M; tests/corpus/report-tuning
video-simprints test --split test --fits tests/corpus/report-tuning
```

[`tests/corpus/manifest.csv`](tests/corpus/manifest.csv) lists 29 originals and
59 unrelated videos with URL, licence, SHA-256 and a `set`: Blender open movies
(CC BY), public-domain NASA and White House videos from Wikimedia Commons, and a
newsreel. Five sets share branding (NASA's *A Moment with…*, *This Week @NASA*,
*Space to Ground*, JPL's *What's Up*, the White House's *West Wing Week*), and
others look alike (launches, Earth visualisations, Blender films). Tuning: 11
originals and 25 unrelated; test: 18 and 34. Test mode makes the manipulated
clips with ffmpeg (excerpts of 10, 30 and 60 s, a 9:16 centre crop,
picture-in-picture at 25% and 40% of the width inside a 1080p unrelated video at
a random corner or the centre, 240p at 150 kbit/s, a caption bar, a corner logo,
and screenshots). It sweeps `codes` {5, 10, 20}, `stop_after` (N), `shared_after`
(N2, counted against every other video of the split, leaving the query out), the
verifier's `fps` {1, 2} and size {512, 1024}, `min_frames` (M), picture-in-picture
modes (1920 px, tiles) and still settings (size, verifier codes, votes). All
thresholds are fitted on the tuning split only. Output: `report.json` and
`summary.md`.

## Results

On the test split at the fitted settings
([report](tests/corpus/report-test/summary.md), [tuning](tests/corpus/report-tuning/summary.md)),
K = 10, verifier 1024 px at 1 fps, index-level stop codes against the other
videos:

| M | 10 s | 30 s | 60 s | 9:16 | 240p | caption | logo | mean, all clips | false: unrelated videos | false: wrong video |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 10 (fitted) | 25% | 81% | 97% | 17% | 78% | 72% | 83% | 50% | 0 of 34 | 0 |

Lower M finds far more, at the cost of false matches. Overall rate, then false
matches against unrelated videos and wrong-video matches in manipulated clips:
81% at M = 1 (6 and 12), 72% at M = 3 (3 and 6), 60% at M = 7 (0 and 6).
Without stop codes M = 1 gives 53 and 88. Nearly all of these are series
branding (intros, studio sets, logo bugs) shared between episodes; a few are
real reused footage. Picture-in-picture needs tiles: at M = 1 they lift 25%
insets from 19% to 64% and 40% insets from 47% to 81% (insets in a corner; a
centred 25% inset straddles the tiles and is missed). Stills: 54–58% found, with
1 to 3 false matches of 170, all series branding. Volume: about 16 keyframes and
150 codes per minute, 13,600 codes per 90-minute film (K = 5: 7,000; K = 20:
26,000). Time per minute of video, one process: creator 1.5 s; verifier 4 s
(17 s with tiles).

**Branding labels and overlapping tiles**
([report](tests/corpus/report-experiment-test/summary.md), [tuning](tests/corpus/report-experiment-tuning/summary.md);
`video-simprints test --experiment` after `test`). With `index(..., label=True)`
the shared codes stay in the index and a match whose agreeing codes are at least
60% shared (fitted) is returned as `shared_branding`. At M = 3 on test: 73% of
clips found (72% with the codes dropped), 103 branding matches labelled (100 to
the same series as the query or its picture-in-picture background, 3 between
NASA's two ISS series), 1 source lost to the label (a 10 s excerpt whose
matched codes are all shared), and 1 unlabelled false match (two launch
videos), against 3 and 6 with
the codes dropped. For centred picture-in-picture, a fifth, centre tile
(`tiles=5`) does what the 3×3 grid does at 20 s instead of 32 s per minute
(quarters only: 17 s). It finds centred insets the quarters miss (25%: 2 of 2 at
M = 1, against 0; 40%: 5 of 9 at M = 3, against 4), with one more false match
than the quarters (3 against 2 at M = 3, labelled).

## Documents

- [RECIPE.md](RECIPE.md): the recipe, precisely enough to reimplement.
- [THIRD-PARTY-NOTICES.md](THIRD-PARTY-NOTICES.md): dependencies, FFmpeg, and
  the test corpus credits.

Apache-2.0. © 2026 Joseph Sherrier.
