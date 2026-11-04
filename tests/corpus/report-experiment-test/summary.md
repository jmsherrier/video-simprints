# video-simprints experiments: test split

ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. K = 10, N off, N2 = 0 (counted against every other video of the split, leaving the query out), verifier 1024 px at 1 fps. **drop**: shared codes left out of the index (the fitted default). **label**: shared codes kept and marked; a match whose agreeing codes are at least 0.6 shared (fitted on report-experiment-tuning) is labelled `shared_branding`, not counted as a match.

## Branding labels

| index | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | mean | source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| drop | 3 | 86% | 100% | 100% | 47% | 3% | 28% | 92% | 100% | 94% | 72.2% | 0 | 0 / 0 | 3 | 6 |
| label | 3 | 86% | 100% | 100% | 50% | 3% | 31% | 94% | 100% | 94% | 73.1% | 1 | 100 / 3 | 1 | 0 |
| drop | 10 | 25% | 81% | 97% | 17% | 0% | 0% | 78% | 72% | 83% | 50.3% | 0 | 0 / 0 | 0 | 0 |
| label | 10 | 28% | 89% | 97% | 22% | 0% | 0% | 81% | 75% | 83% | 52.8% | 0 | 23 / 0 | 0 | 0 |

Share of shared codes swept at M = 3 (label):

| share | mean | source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- |
| 0.1 | 55.2% | 59 | 101 / 3 | 0 | 0 |
| 0.2 | 63.3% | 33 | 101 / 3 | 0 | 0 |
| 0.3 | 66.7% | 22 | 101 / 3 | 0 | 0 |
| 0.4 | 70.1% | 11 | 101 / 3 | 0 | 0 |
| 0.5 | 72.2% | 4 | 101 / 3 | 0 | 0 |
| 0.6 | 73.1% | 1 | 100 / 3 | 1 | 0 |
| 0.7 | 73.1% | 1 | 93 / 3 | 1 | 7 |
| 0.8 | 73.1% | 1 | 89 / 3 | 2 | 10 |
| 0.9 | 73.1% | 1 | 86 / 3 | 3 | 12 |
| None | 73.1% | 0 | 0 / 0 | 51 | 53 |

Unlabelled false matches, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):

- nasa-crs-17-launch__whole (launch) -> nasa-dscovr-launch (launch): 3, 0.567

Labelled, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):

- jpl-whats-up-2025-12__whole (jpl-whats-up) -> jpl-whats-up-2026-10 (jpl-whats-up): 21, 1.0
- nasa-twan-2020-07-31__whole (nasa-this-week) -> nasa-twan-2020-12-11 (nasa-this-week): 17, 1.0
- jpl-whats-up-2025-12__whole (jpl-whats-up) -> jpl-whats-up-2025-09 (jpl-whats-up): 17, 0.907
- jpl-whats-up-2026-05__whole (jpl-whats-up) -> jpl-whats-up-2026-10 (jpl-whats-up): 16, 1.0
- nasa-twan-2020-06-12__whole (nasa-this-week) -> nasa-twan-2020-11-06 (nasa-this-week): 15, 1.0
- nasa-twan-2020-03-27__whole (nasa-this-week) -> nasa-twan-2020-12-11 (nasa-this-week): 15, 1.0
- jpl-whats-up-2026-11__whole (jpl-whats-up) -> jpl-whats-up-2026-10 (jpl-whats-up): 15, 0.926
- nasa-twan-2018-11-09__whole (nasa-this-week) -> nasa-twan-2020-12-11 (nasa-this-week): 14, 1.0
- nasa-s2g-2015-10-16__whole (nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 14, 0.791
- nasa-twan-2020-06-12__whole (nasa-this-week) -> nasa-twan-2020-09-18 (nasa-this-week): 13, 0.977
- nasa-twan-2020-07-31__whole (nasa-this-week) -> nasa-twan-2020-11-06 (nasa-this-week): 13, 1.0
- nasa-s2g-2015-10-16__whole (nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 12, 0.983
- nasa-s2g-2016-08-11__excerpt60__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 11, 0.667
- nasa-s2g-2016-08-11__caption__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 11, 0.667
- nasa-s2g-2016-08-11__logo__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 11, 0.667
- nasa-twan-2020-06-12__whole (nasa-this-week) -> nasa-twan-2020-12-11 (nasa-this-week): 11, 1.0
- nasa-twan-2020-03-27__whole (nasa-this-week) -> nasa-twan-2020-09-18 (nasa-this-week): 11, 1.0
- nasa-twan-2020-03-27__whole (nasa-this-week) -> nasa-twan-2020-11-06 (nasa-this-week): 11, 1.0
- jpl-whats-up-2026-05__whole (jpl-whats-up) -> jpl-whats-up-2025-09 (jpl-whats-up): 11, 0.977
- nasa-s2g-2016-08-11__excerpt60__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 10, 0.64
- nasa-s2g-2016-08-11__logo__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 10, 0.64
- hero__pip40__0 (blender, nasa-space-to-ground) -> nasa-s2g-2017-01-06 (nasa-space-to-ground): 10, 0.641
- nasa-twan-2020-07-31__whole (nasa-this-week) -> nasa-twan-2020-09-18 (nasa-this-week): 10, 1.0
- nasa-twan-2018-11-09__whole (nasa-this-week) -> nasa-twan-2020-09-18 (nasa-this-week): 9, 1.0
- nasa-twan-2018-11-09__whole (nasa-this-week) -> nasa-twan-2020-11-06 (nasa-this-week): 9, 1.0
- jpl-whats-up-2025-08__whole (jpl-whats-up) -> jpl-whats-up-2025-09 (jpl-whats-up): 9, 0.976
- jpl-whats-up-2025-08__whole (jpl-whats-up) -> jpl-whats-up-2026-10 (jpl-whats-up): 9, 1.0
- jpl-whats-up-2026-11__whole (jpl-whats-up) -> jpl-whats-up-2025-09 (jpl-whats-up): 9, 1.0
- jpl-whats-up-2025-09__excerpt30__1 (jpl-whats-up) -> jpl-whats-up-2026-10 (jpl-whats-up): 8, 0.86
- jpl-whats-up-2025-09__logo__1 (jpl-whats-up) -> jpl-whats-up-2026-10 (jpl-whats-up): 8, 0.868
- hero__pip40__0 (blender, nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 8, 1.0
- nasa-s2g-2017-05-26__whole (nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 8, 0.936
- nasa-moment-kimiya-yui__excerpt10__1 (nasa-moment) -> nasa-moment-kate-rubins (nasa-moment): 7, 1.0
- nasa-moment-kimiya-yui__excerpt10__1 (nasa-moment) -> nasa-moment-tim-peake (nasa-moment): 7, 1.0
- nasa-twan-2020-12-11__pip25__0 (nasa-this-week, nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 7, 1.0
- jpl-whats-up-2026-10__excerpt60__0 (jpl-whats-up) -> jpl-whats-up-2025-09 (jpl-whats-up): 7, 0.791
- nasa-s2g-2017-01-06__excerpt30__1 (nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 7, 1.0
- nasa-s2g-2017-01-06__excerpt60__0 (nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 7, 1.0
- nasa-s2g-2017-01-06__excerpt60__1 (nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 7, 0.939
- nasa-s2g-2017-01-06__caption__1 (nasa-space-to-ground) -> nasa-s2g-2016-08-11 (nasa-space-to-ground): 7, 1.0

Sources lost to the label, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):

- nasa-moment-kimiya-yui__excerpt10__1 (nasa-moment) -> nasa-moment-kimiya-yui (nasa-moment): 7, 1.0

## Picture-in-picture

Insets at 25% and 40% of the width of a 1080p unrelated video, at a random corner or the centre. tiles4: the quarters; tiles5: the quarters and a centre tile; tiles9: a 3x3 grid of half-size tiles overlapping by half.

| verifier | index | M | pip25 | pip40 | pip25 centre | pip25 corner | pip40 centre | pip40 corner | source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | drop | 1 | 19% | 47% | 0% | 21% | 11% | 59% | 0 | 0 / 0 | 6 | 12 |
| 1024 | drop | 3 | 3% | 28% | 0% | 3% | 0% | 37% | 0 | 0 / 0 | 3 | 6 |
| 1024 | drop | 10 | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 0 / 0 | 0 | 0 |
| 1024 | label | 1 | 19% | 47% | 0% | 21% | 0% | 63% | 2 | 129 / 7 | 2 | 3 |
| 1024 | label | 3 | 3% | 31% | 0% | 3% | 0% | 41% | 1 | 100 / 3 | 1 | 0 |
| 1024 | label | 10 | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 23 / 0 | 0 | 0 |
| 1024+tiles4 | drop | 1 | 64% | 81% | 0% | 68% | 56% | 89% | 0 | 0 / 0 | 7 | 3 |
| 1024+tiles4 | drop | 3 | 42% | 67% | 0% | 44% | 44% | 74% | 0 | 0 / 0 | 4 | 1 |
| 1024+tiles4 | drop | 10 | 11% | 31% | 0% | 12% | 11% | 37% | 0 | 0 / 0 | 0 | 0 |
| 1024+tiles4 | label | 1 | 64% | 78% | 0% | 68% | 44% | 89% | 2 | 89 / 5 | 3 | 4 |
| 1024+tiles4 | label | 3 | 50% | 67% | 0% | 53% | 44% | 74% | 0 | 63 / 3 | 2 | 0 |
| 1024+tiles4 | label | 10 | 11% | 36% | 0% | 12% | 11% | 44% | 0 | 19 / 0 | 0 | 0 |
| 1024+tiles5 | drop | 1 | 69% | 81% | 100% | 68% | 56% | 89% | 0 | 0 / 0 | 7 | 3 |
| 1024+tiles5 | drop | 3 | 42% | 69% | 0% | 44% | 56% | 74% | 0 | 0 / 0 | 4 | 1 |
| 1024+tiles5 | drop | 10 | 11% | 36% | 0% | 12% | 33% | 37% | 0 | 0 / 0 | 0 | 0 |
| 1024+tiles5 | label | 1 | 69% | 81% | 100% | 68% | 56% | 89% | 1 | 88 / 5 | 4 | 4 |
| 1024+tiles5 | label | 3 | 50% | 69% | 0% | 53% | 56% | 74% | 0 | 62 / 3 | 3 | 0 |
| 1024+tiles5 | label | 10 | 11% | 42% | 0% | 12% | 33% | 44% | 0 | 21 / 0 | 0 | 0 |
| 1024+tiles9 | drop | 1 | 69% | 81% | 100% | 68% | 56% | 89% | 0 | 0 / 0 | 7 | 3 |
| 1024+tiles9 | drop | 3 | 42% | 69% | 0% | 44% | 56% | 74% | 0 | 0 / 0 | 4 | 1 |
| 1024+tiles9 | drop | 10 | 11% | 36% | 0% | 12% | 33% | 37% | 0 | 0 / 0 | 0 | 0 |
| 1024+tiles9 | label | 1 | 69% | 81% | 100% | 68% | 56% | 89% | 2 | 91 / 7 | 4 | 4 |
| 1024+tiles9 | label | 3 | 50% | 69% | 0% | 53% | 56% | 74% | 0 | 62 / 3 | 3 | 0 |
| 1024+tiles9 | label | 10 | 11% | 42% | 0% | 12% | 33% | 44% | 0 | 21 / 0 | 0 | 0 |

Verifier time (one process, label index, seconds per minute of a 25% PiP clip):

- 1024: 4.8
- 1024+tiles4: 17.2
- 1024+tiles5: 20.2
- 1024+tiles9: 31.9
