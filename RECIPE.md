# Recipe `video-simprints/0.1`

How a video becomes a declaration (creator side), and how a clip or a still is
checked against declarations (verifier side). The reference implementation is
[`src/video_simprints/recipe.py`](src/video_simprints/recipe.py). Image codes are
[image-simprints](https://github.com/jmsherrier/image-simprints) recipe 2.2
(`image-simprints/2.2`), used unchanged through its `generate()` and `match()`.

## 1. Version and settings

| setting | default | side | meaning |
| --- | --- | --- | --- |
| `codes` | 10 | creator | codes per keyframe (K) |
| `spread` | 0 | creator | take an equal share of the codes from each horizontal third |
| `stop_after` | 1000 | creator | drop codes that agree with codes of more than N other keyframes (1000: off) |
| `fps` | 2 | verifier | frames sampled per second of the checked clip |
| `prepared_size` | 1024 | verifier | image-simprints `prepared_size` of the sampled frames |
| `min_frames` | 1 | verifier | frames on one time line needed to declare a match (M) |

The version string is `video-simprints/0.1`, with each creator setting that
differs from its default appended as `;name=value` (booleans as 0 or 1), in the
order of the table. Verifier settings do not change stored codes and are not in
the string. The defaults were chosen on the tuning split
([report](tests/corpus/report-tuning/summary.md)); N and M were fitted there for
every setting. Each keyframe also carries its image-simprints version, for example
`image-simprints/2.2;creator_codes=20`.

Fixed constants:

| constant | value | meaning |
| --- | --- | --- |
| `SAMPLE_FPS` | 5 | frames decoded per second on the creator side |
| `GRID` | 3 s | keyframe interval |
| `CUT` | 0.4 | ffmpeg scene score at or above which a frame starts a new scene |
| `CUT_MARGIN` | 0.5 s | grid points this close to a cut are skipped |
| `WINDOW` | 0.4 s | a blurred grid frame is replaced by the sharpest frame this close |
| `BLUR` | 35 | variance of the Laplacian below which a grid frame is blurred (the 10th percentile of tuning grid frames) |
| `UNIFORM` | 8 | standard deviation of grey below which a frame is black or uniform (no tuning grid frame below it had codes) |
| `SLOPE` | 0.1 | time vote: slope 1 ± 0.1 |
| `TIME_TOLERANCE` | 3 s | time vote: how far a frame may lie off the line |

## 2. Decoding

The system `ffmpeg`, as a subprocess, with the filter `fps=F` on the first video
stream. Frame `i` is the frame ffmpeg's `fps` filter emits for time `i / F`
after the first frame. Frames are RGB at the stored resolution (rotation applied,
sample aspect ratio ignored), as PPM through a pipe. The creator decodes at
`F = SAMPLE_FPS`; the verifier at `F = fps`.

## 3. Creator: keyframes

1. **Scene cuts**: the same pass adds `select='gte(scene,0)',metadata=print`
   and reads `lavfi.scene_score` of each frame (against the frame before, at 5
   fps, as iscc-sdk 0.9.4). A frame `i > 0` with score ≥ `CUT` is a cut at
   `i / 5` s.
2. **Grid**: grid points at 0, 3, 6, … s, up to the last frame. Skip a grid
   point within `CUT_MARGIN` of a cut (so a keyframe never straddles a cut and
   its window never crosses one).
3. **Sharpness**: prepare each frame as image-simprints does (grey, longer side
   512 by area averaging) and take the variance of its Laplacian
   (`cv2.Laplacian(grey, CV_64F).var()`). If the grid frame's is below `BLUR`,
   use the sharpest frame within ± `WINDOW` (± 2 frames at 5 fps); ties go to
   the frame nearest the grid point, then the earlier.
4. **Uniform**: skip the keyframe if the chosen frame's prepared grey has a
   standard deviation below `UNIFORM` (black, fades, flat colour), or if
   image-simprints returns no codes for it.
5. **Scene index**: the number of cuts at or before the grid point.

The keyframe time is the chosen frame's time (the grid point ± up to 0.4 s).

## 4. Creator: codes

1. **Image codes**: `generate(frame, "creator", {"creator_codes": 512})` on the
   chosen frame: image-simprints' full ranked list (512 is its candidate cap).
   The first K of that list are exactly `generate(frame, "creator",
   {"creator_codes": K})`.
2. **Selection**: without `spread`, the first K. With `spread`, the first
   `K // 3` codes (by rank) whose `x` lies in each horizontal third (`x < 1/3`,
   `< 2/3`, the rest), then the best-ranked remaining codes up to K. Codes stay in
   rank order. A 9:16 crop of a 16:9 frame keeps about a third of the width,
   which a plain top-K may leave nearly empty.
3. **Near-duplicates**: in time order, a keyframe whose codes `match()` an
   earlier kept keyframe as `identical`, with `agreeing_codes` at least half its
   codes, is dropped; its time is added to that keyframe's `same_as` list.
   This folds static shots and repeated shots (A-B-A-B) into one keyframe.
4. **Stop codes**: image-simprints' `mark_stop_codes(keyframes, N)` marks each
   code that agrees (Hamming distance ≤ 24) with codes of more than N other
   kept keyframes of the same video; marked codes are dropped. These are the
   video's logos, watermarks, lower thirds and title cards.
5. Drop keyframes left with fewer than 2 codes (a match needs 2).
6. Number the kept keyframes from 0. Each code gets `keyframe`, `time` and
   `scene`.

**Declaration**:
`{recipe_version, duration, cuts, keyframes: [{recipe_version, time, scene,
same_as, prepared_size, codes: [{chunk_idx, code, x, y, scale, angle, keyframe,
time, scene}]}]}`. Each keyframe is a valid image-simprints `generate()` result.

## 5. Verifier

1. **Frames**: decode the clip at `fps`; code each frame with
   `generate(frame, "verifier", {"prepared_size": prepared_size})`.
2. **Candidates**: every stored keyframe with at least 2 of its codes within
   Hamming distance 24 of the frame's codes (the reference keeps all codes in
   memory; see image-simprints INTEGRATION.md for a banded index).
3. **Geometric vote**: `match(frame, keyframe)` for each candidate; keep
   those that are not `none`. This gives the spatial relationship per frame.
4. **Time vote**, per declaration: each kept match is a point (clip time `c`,
   original time `t`), once for the keyframe's time and once for each time in
   its `same_as`. Try the line `t = c + b` through each point and the line
   through each pair of points whose slope `a` is within 1 ± `SLOPE`. Count the
   distinct clip times with a point within `TIME_TOLERANCE` of the line. The
   line with the highest count wins (ties: the smaller sum of distances).
5. **Decision**: a declaration matches if its count is at least `min_frames`.
   Report the count, the clip range of the agreeing frames, the matching range
   in the original (`a c + b` at its ends), the slope, the dominant
   relationship among the agreeing frames (each frame's strongest match) and the
   median overlap fractions of those. Results are sorted by count.

**Stills**: a single image is one frame: steps 1 to 3, with the best keyframe
(most agreeing codes) per declaration. Its time says where in the video it is.

## 6. Test vectors

[`tests/test_video.py`](tests/test_video.py) builds a 30 s synthetic video with
known cuts (6.2, 12.4 and 15.8 s) and a black gap, and checks the keyframe rule
(keyframes at 0, 3, 9, 18, 21, 24, 27 s; 6 and 12 s skipped for cuts, 15 s for
black), determinism, that keyframe codes equal `generate()`'s, and an excerpt,
a vertical crop and a still of it.
