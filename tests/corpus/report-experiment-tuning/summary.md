# video-simprints experiments: tuning split

ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. K = 10, N off, N2 = 0 (counted against every other video of the split, leaving the query out), verifier 1024 px at 1 fps. **drop**: shared codes left out of the index (the fitted default). **label**: shared codes kept and marked; a match whose agreeing codes are at least 0.6 shared (fitted on tuning) is labelled `shared_branding`, not counted as a match.

## Branding labels

| index | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | mean | source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| drop | 3 | 86% | 91% | 100% | 59% | 5% | 23% | 95% | 100% | 100% | 73.2% | 0 | 0 / 0 | 4 | 5 |
| label | 3 | 86% | 91% | 100% | 64% | 5% | 23% | 95% | 100% | 95% | 73.2% | 3 | 43 / 7 | 1 | 1 |
| drop | 10 | 18% | 73% | 95% | 27% | 0% | 0% | 77% | 82% | 82% | 50.5% | 0 | 0 / 0 | 0 | 0 |
| label | 10 | 18% | 86% | 95% | 27% | 0% | 0% | 82% | 91% | 86% | 54.0% | 1 | 16 / 0 | 0 | 0 |

Share of shared codes swept at M = 3 (label):

| share | mean | source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- |
| 0.1 | 53.5% | 43 | 43 / 7 | 1 | 1 |
| 0.2 | 60.1% | 30 | 43 / 7 | 1 | 1 |
| 0.3 | 67.2% | 16 | 43 / 7 | 1 | 1 |
| 0.4 | 70.2% | 10 | 43 / 7 | 1 | 1 |
| 0.5 | 71.7% | 7 | 43 / 7 | 1 | 1 |
| 0.6 | 73.2% | 3 | 43 / 7 | 1 | 1 |
| 0.7 | 74.7% | 0 | 42 / 7 | 2 | 1 |
| 0.8 | 74.7% | 0 | 38 / 7 | 2 | 5 |
| 0.9 | 74.7% | 0 | 36 / 7 | 4 | 5 |
| None | 74.2% | 0 | 0 / 0 | 27 | 25 |

Unlabelled false matches, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):

- wh-west-wing-week-2015-04-10__whole (west-wing-week) -> wh-west-wing-week-2015-06-05 (west-wing-week): 5, 0.0
- coffee-run__pip40__0 (blender, west-wing-week) -> wh-west-wing-week-2015-06-05 (west-wing-week): 3, 0.0

Labelled, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):

- jpl-whats-up-2026-02__whole (jpl-whats-up) -> jpl-whats-up-2026-04 (jpl-whats-up): 23, 0.905
- jpl-whats-up-2026-01__whole (jpl-whats-up) -> jpl-whats-up-2026-04 (jpl-whats-up): 23, 0.871
- nasa-s2g-2015-02-27__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 22, 0.688
- nasa-s2g-2018-01-19__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 18, 1.0
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 16, 1.0
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 15, 1.0
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 15, 1.0
- jpl-whats-up-2025-11__whole (jpl-whats-up) -> jpl-whats-up-2026-04 (jpl-whats-up): 15, 0.853
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 12, 1.0
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 12, 1.0
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 12, 1.0
- nasa-moment-shane-kimbrough__pip40__0 (nasa-moment, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 10, 0.725
- jpl-whats-up-2026-04__pip40__1 (jpl-whats-up, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 10, 0.718
- coffee-run__pip25__0 (blender, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 10, 0.745
- coffee-run__pip25__1 (blender, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 10, 0.72
- nasa-s2g-2014-10-24__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 10, 0.962
- sintel__pip40__0 (blender, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 9, 1.0
- nasa-crs7-countdown__pip25__0 (launch, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 9, 1.0
- nasa-tim-kopra__pip40__1 (nasa-moment, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 7, 1.0
- nasa-atlas-v-tdrs-m__pip40__1 (launch, nasa-space-to-ground) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 7, 1.0
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 6, 1.0
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-tim-kopra (nasa-moment): 6, 1.0
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-moment-shane-kimbrough (nasa-moment): 6, 1.0
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 6, 1.0
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-tim-kopra (nasa-moment): 6, 1.0
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 5, 1.0
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-tim-kopra (nasa-moment): 5, 1.0
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-moment-shane-kimbrough (nasa-moment): 5, 1.0
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 5, 1.0
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-tim-kopra (nasa-moment): 5, 1.0
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-moment-shane-kimbrough (nasa-moment): 5, 1.0
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-s2g-2015-03-06 (nasa-space-to-ground): 5, 1.0
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-tim-kopra (nasa-moment): 5, 1.0
- sintel__pip25__0 (blender, nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 4, 1.0
- sintel__pip25__0 (blender, nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 4, 1.0
- nasa-twan-2020-01-25__excerpt60__1 (nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 4, 1.0
- nasa-twan-2020-01-25__logo__1 (nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 4, 1.0
- nasa-twan-2020-02-07__excerpt10__0 (nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 4, 1.0
- nasa-twan-2020-02-07__excerpt30__0 (nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 4, 1.0
- nasa-twan-2020-02-07__caption__1 (nasa-this-week) -> nasa-twan-2020-01-25 (nasa-this-week): 4, 1.0

Sources lost to the label, label at M = 3 (query, its set, PiP background's set -> matched declaration, its set: frames, shared share):

- jpl-whats-up-2026-04__logo__0 (jpl-whats-up) -> jpl-whats-up-2026-04 (jpl-whats-up): 22, 0.671
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-moment-shane-kimbrough (nasa-moment): 9, 0.673
- nasa-twan-2020-02-07__excerpt10__0 (nasa-this-week) -> nasa-twan-2020-02-07 (nasa-this-week): 6, 0.673

## Picture-in-picture

Insets at 25% and 40% of the width of a 1080p unrelated video, at a random corner or the centre. tiles4: the quarters; tiles5: the quarters and a centre tile; tiles9: a 3x3 grid of half-size tiles overlapping by half.

| verifier | index | M | pip25 | pip40 | pip25 centre | pip25 corner | pip40 centre | pip40 corner | source labelled (lost) | labelled, same set (as the query or its PiP background) / other set | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | drop | 1 | 9% | 32% | 0% | 12% | 0% | 33% | 0 | 0 / 0 | 7 | 14 |
| 1024 | drop | 3 | 5% | 23% | 0% | 6% | 0% | 24% | 0 | 0 / 0 | 4 | 5 |
| 1024 | drop | 10 | 0% | 0% | 0% | 0% | 0% | 0% | 0 | 0 / 0 | 0 | 0 |
| 1024 | label | 1 | 9% | 36% | 0% | 12% | 0% | 38% | 4 | 46 / 8 | 2 | 8 |
| 1024 | label | 3 | 5% | 23% | 0% | 6% | 0% | 24% | 3 | 43 / 7 | 1 | 1 |
| 1024 | label | 10 | 0% | 0% | 0% | 0% | 0% | 0% | 1 | 16 / 0 | 0 | 0 |
| 1024+tiles4 | drop | 1 | 45% | 77% | 0% | 62% | 100% | 76% | 0 | 0 / 0 | 7 | 13 |
| 1024+tiles4 | drop | 3 | 23% | 77% | 0% | 31% | 100% | 76% | 0 | 0 / 0 | 4 | 5 |
| 1024+tiles4 | drop | 10 | 14% | 36% | 0% | 19% | 0% | 38% | 0 | 0 / 0 | 0 | 0 |
| 1024+tiles4 | label | 1 | 45% | 82% | 0% | 62% | 100% | 81% | 0 | 38 / 10 | 2 | 7 |
| 1024+tiles4 | label | 3 | 27% | 82% | 0% | 38% | 100% | 81% | 0 | 37 / 6 | 1 | 1 |
| 1024+tiles4 | label | 10 | 14% | 36% | 0% | 19% | 0% | 38% | 0 | 18 / 0 | 0 | 0 |
| 1024+tiles5 | drop | 1 | 59% | 77% | 50% | 62% | 100% | 76% | 0 | 0 / 0 | 7 | 15 |
| 1024+tiles5 | drop | 3 | 27% | 77% | 17% | 31% | 100% | 76% | 0 | 0 / 0 | 5 | 7 |
| 1024+tiles5 | drop | 10 | 18% | 41% | 17% | 19% | 100% | 38% | 0 | 0 / 0 | 0 | 0 |
| 1024+tiles5 | label | 1 | 59% | 82% | 50% | 62% | 100% | 81% | 0 | 38 / 10 | 3 | 7 |
| 1024+tiles5 | label | 3 | 32% | 82% | 17% | 38% | 100% | 81% | 0 | 37 / 6 | 2 | 1 |
| 1024+tiles5 | label | 10 | 18% | 41% | 17% | 19% | 100% | 38% | 0 | 18 / 0 | 0 | 0 |
| 1024+tiles9 | drop | 1 | 59% | 77% | 50% | 62% | 100% | 76% | 0 | 0 / 0 | 7 | 15 |
| 1024+tiles9 | drop | 3 | 27% | 77% | 17% | 31% | 100% | 76% | 0 | 0 / 0 | 5 | 7 |
| 1024+tiles9 | drop | 10 | 18% | 41% | 17% | 19% | 100% | 38% | 0 | 0 / 0 | 0 | 0 |
| 1024+tiles9 | label | 1 | 59% | 86% | 50% | 62% | 100% | 86% | 0 | 38 / 10 | 3 | 7 |
| 1024+tiles9 | label | 3 | 32% | 82% | 17% | 38% | 100% | 81% | 0 | 37 / 6 | 2 | 1 |
| 1024+tiles9 | label | 10 | 18% | 41% | 17% | 19% | 100% | 38% | 0 | 18 / 0 | 0 | 0 |

Verifier time (one process, label index, seconds per minute of a 25% PiP clip):

- 1024: 4.7
- 1024+tiles4: 16.3
- 1024+tiles5: 20.5
- 1024+tiles9: 35.0
