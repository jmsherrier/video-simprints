# video-simprints report: tuning split

Recipe video-simprints/0.1 on image-simprints/2.2; ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. 403 queries. Thresholds fitted on the tuning split. N: per-video stop codes (`stop_after`, 1000 = off); N2: index-level stop codes (`shared_after`, None = off); M: `min_frames`.

**Recommended** (chosen on tuning): K = 10, verifier 512 px at 1 fps, N = 1000, N2 = 0, M = 25.

## Video-level match rate (right video, time range within 3 s) and false matches

| setting | N | N2 | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | mean | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;size=512;fps=1 | 1000 | None | 25 | 0% | 18% | 64% | 0% | 0% | 0% | 14% | 0% | 18% | 12.6% | 0 of 25 | 0 |
| codes=5;size=512;fps=2 | 1000 | 0 | 25 | 0% | 59% | 95% | 0% | 0% | 0% | 64% | 36% | 50% | 33.8% | 2 of 25 | 0 |
| codes=5;size=1024;fps=1 | 1000 | None | 25 | 0% | 18% | 64% | 0% | 0% | 0% | 9% | 0% | 14% | 11.6% | 0 of 25 | 0 |
| codes=5;size=1024;fps=2 | 1000 | 0 | 30 | 0% | 50% | 86% | 0% | 0% | 0% | 50% | 27% | 41% | 28.3% | 2 of 25 | 0 |
| codes=10;size=512;fps=1 | 1000 | 0 | 25 | 0% | 32% | 91% | 0% | 0% | 0% | 23% | 0% | 32% | 19.7% | 0 of 25 | 0 |
| codes=10;size=512;fps=2 | 1000 | 0 | 30 | 0% | 59% | 95% | 0% | 0% | 0% | 68% | 59% | 59% | 37.9% | 5 of 25 | 0 |
| codes=10;size=1024;fps=1 | 1000 | None | 25 | 0% | 32% | 77% | 0% | 0% | 0% | 27% | 0% | 27% | 18.2% | 0 of 25 | 0 |
| codes=10;size=1024;fps=2 | 1000 | 0 | 25 | 0% | 64% | 95% | 9% | 0% | 0% | 68% | 64% | 77% | 41.9% | 5 of 25 | 0 |
| codes=20;size=512;fps=1 | 3 | None | 25 | 0% | 36% | 91% | 0% | 0% | 0% | 41% | 14% | 36% | 24.2% | 1 of 25 | 0 |
| codes=20;size=512;fps=2 | 3 | 0 | 25 | 0% | 77% | 100% | 32% | 0% | 5% | 77% | 77% | 95% | 51.5% | 5 of 25 | 0 |
| codes=20;size=1024;fps=1 | 3 | None | 25 | 0% | 36% | 91% | 0% | 0% | 0% | 41% | 14% | 32% | 23.7% | 0 of 25 | 0 |
| codes=20;size=1024;fps=2 | 3 | 0 | 25 | 0% | 77% | 100% | 27% | 0% | 5% | 77% | 77% | 91% | 50.5% | 5 of 25 | 0 |

## Frame-level match rate (sampled frames matching a keyframe of the source)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | unrelated frames with any match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;size=512;fps=1 | 47% | 54% | 55% | 12% | 2% | 1% | 50% | 34% | 54% | 195 of 3497 |
| codes=5;size=512;fps=2 | 48% | 53% | 53% | 11% | 2% | 1% | 50% | 34% | 53% | 310 of 6981 |
| codes=5;size=1024;fps=1 | 47% | 53% | 54% | 12% | 1% | 1% | 48% | 34% | 52% | 203 of 3497 |
| codes=5;size=1024;fps=2 | 46% | 52% | 52% | 11% | 1% | 1% | 48% | 34% | 51% | 311 of 6981 |
| codes=10;size=512;fps=1 | 59% | 64% | 65% | 24% | 1% | 5% | 63% | 52% | 66% | 203 of 3497 |
| codes=10;size=512;fps=2 | 58% | 63% | 64% | 25% | 2% | 6% | 65% | 52% | 65% | 401 of 6981 |
| codes=10;size=1024;fps=1 | 61% | 64% | 64% | 26% | 1% | 5% | 63% | 53% | 65% | 245 of 3497 |
| codes=10;size=1024;fps=2 | 59% | 63% | 63% | 24% | 1% | 6% | 64% | 52% | 64% | 374 of 6981 |
| codes=20;size=512;fps=1 | 69% | 70% | 71% | 35% | 1% | 10% | 70% | 63% | 73% | 277 of 3497 |
| codes=20;size=512;fps=2 | 66% | 70% | 70% | 33% | 1% | 11% | 71% | 63% | 72% | 492 of 6981 |
| codes=20;size=1024;fps=1 | 70% | 70% | 70% | 35% | 1% | 11% | 70% | 63% | 71% | 254 of 3497 |
| codes=20;size=1024;fps=2 | 66% | 69% | 69% | 33% | 1% | 11% | 70% | 63% | 71% | 429 of 6981 |

## False matches against M (K = 10, 512 px, 1 fps)

| M | recommended stop codes: match rate | recommended stop codes: false (unrelated) | recommended stop codes: false (wrong video) | no stop codes: match rate | no stop codes: false (unrelated) | no stop codes: false (wrong video) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 79.3% | 12 | 23 | 79.8% | 29 | 36 |
| 2 | 75.8% | 11 | 17 | 76.8% | 28 | 28 |
| 3 | 73.7% | 10 | 10 | 74.7% | 27 | 26 |
| 4 | 71.7% | 10 | 8 | 72.7% | 25 | 21 |
| 5 | 69.2% | 10 | 8 | 70.7% | 25 | 10 |
| 6 | 66.7% | 8 | 8 | 67.7% | 15 | 10 |
| 7 | 62.1% | 7 | 8 | 62.6% | 12 | 8 |
| 8 | 59.1% | 6 | 7 | 60.1% | 12 | 7 |
| 9 | 55.6% | 6 | 6 | 57.6% | 12 | 6 |
| 10 | 52.0% | 6 | 3 | 53.5% | 12 | 3 |
| 11 | 49.5% | 6 | 0 | 51.0% | 12 | 0 |
| 12 | 45.5% | 6 | 0 | 47.0% | 10 | 0 |
| 15 | 39.9% | 5 | 0 | 39.9% | 8 | 0 |
| 20 | 29.8% | 4 | 0 | 31.3% | 4 | 0 |
| 25 | 19.7% | 0 | 0 | 20.2% | 1 | 0 |
| 30 | 9.6% | 0 | 0 | 10.1% | 1 | 0 |

False matches at M = 1, recommended stop codes (query, its set, matched declaration, frames on the line):

- jpl-whats-up-2026-02__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 23
- jpl-whats-up-2026-01__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 23
- jpl-whats-up-2025-11__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 22
- nasa-s2g-2015-02-27__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 21
- nasa-s2g-2018-01-19__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 19
- nasa-s2g-2014-10-24__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 12
- nasa-moment-shane-kimbrough__pip40__0 (nasa-moment) -> nasa-s2g-2015-03-06: 10
- jpl-whats-up-2026-04__pip40__1 (jpl-whats-up) -> nasa-s2g-2015-03-06: 10
- coffee-run__pip25__0 (blender) -> nasa-s2g-2015-03-06: 10
- sintel__pip40__0 (blender) -> nasa-s2g-2015-03-06: 9
- nasa-crs7-countdown__pip25__0 (launch) -> nasa-s2g-2015-03-06: 9
- coffee-run__pip25__1 (blender) -> nasa-s2g-2015-03-06: 9
- nasa-atlas-v-tdrs-m__pip40__1 (launch) -> nasa-s2g-2015-03-06: 8
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-01-25: 7
- nasa-tim-kopra__pip40__1 (nasa-moment) -> nasa-s2g-2015-03-06: 7
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-01-25: 6
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-01-25: 5
- wh-west-wing-week-2015-04-10__whole (west-wing-week) -> wh-west-wing-week-2015-06-05: 5
- nasa-s2g-2015-03-06__pip25__0 (nasa-space-to-ground) -> jpl-whats-up-2026-04: 3
- coffee-run__pip40__0 (blender) -> wh-west-wing-week-2015-06-05: 3
- nasa-twan-2017-08-18__whole (nasa-this-week) -> nasa-atlas-v-tdrs-m: 2
- sintel__pip40__1 (blender) -> nasa-twan-2020-01-25: 2
- nasa-twan-2020-02-07__excerpt10__0 (nasa-this-week) -> nasa-twan-2020-01-25: 2
- nasa-twan-2020-02-07__excerpt30__0 (nasa-this-week) -> nasa-twan-2020-01-25: 2
- nasa-twan-2020-02-07__caption__1 (nasa-this-week) -> nasa-twan-2020-01-25: 2
- jpl-whats-up-2026-04__logo__0 (jpl-whats-up) -> nasa-crs7-countdown: 2
- coffee-run__pip40__1 (blender) -> nasa-twan-2020-01-25: 2
- wh-west-wing-week-2015-06-05__pip25__1 (west-wing-week) -> nasa-twan-2020-01-25: 2
- jpl-whats-up-2026-01__whole (jpl-whats-up) -> nasa-crs7-countdown: 1
- nasa-crs7-countdown__pip25__1 (launch) -> jpl-whats-up-2026-04: 1
- nasa-moment-shane-kimbrough__pip40__1 (nasa-moment) -> jpl-whats-up-2026-04: 1
- nasa-twan-2020-02-07__excerpt60__1 (nasa-this-week) -> nasa-twan-2020-01-25: 1
- nasa-twan-2020-02-07__pip40__0 (nasa-this-week) -> jpl-whats-up-2026-04: 1
- nasa-s2g-2015-03-06__pip40__1 (nasa-space-to-ground) -> jpl-whats-up-2026-04: 1
- nasa-atlas-v-tdrs-m__pip25__1 (launch) -> jpl-whats-up-2026-04: 1

False matches at M = 1, no stop codes (query, its set, matched declaration, frames on the line):

- jpl-whats-up-2026-01__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 30
- jpl-whats-up-2026-02__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 23
- nasa-s2g-2015-02-27__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 23
- jpl-whats-up-2025-11__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 22
- nasa-s2g-2018-01-19__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 19
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-01-25: 16
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-02-07: 15
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-02-07: 15
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-01-25: 12
- nasa-s2g-2014-10-24__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 12
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-01-25: 11
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-02-07: 11
- nasa-moment-shane-kimbrough__pip40__0 (nasa-moment) -> nasa-s2g-2015-03-06: 10
- jpl-whats-up-2026-04__pip40__1 (jpl-whats-up) -> nasa-s2g-2015-03-06: 10
- coffee-run__pip25__0 (blender) -> nasa-s2g-2015-03-06: 10
- sintel__pip40__0 (blender) -> nasa-s2g-2015-03-06: 9
- nasa-crs7-countdown__pip25__0 (launch) -> nasa-s2g-2015-03-06: 9
- coffee-run__pip25__1 (blender) -> nasa-s2g-2015-03-06: 9
- nasa-atlas-v-tdrs-m__pip40__1 (launch) -> nasa-s2g-2015-03-06: 8
- nasa-tim-kopra__pip40__1 (nasa-moment) -> nasa-s2g-2015-03-06: 7
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 6
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-s2g-2015-03-06: 6
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-tim-kopra: 6
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-s2g-2015-03-06: 6
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-tim-kopra: 6
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 5
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-s2g-2015-03-06: 5
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-tim-kopra: 5
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 5
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-s2g-2015-03-06: 5
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-tim-kopra: 5
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 5
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-s2g-2015-03-06: 5
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-tim-kopra: 5
- wh-west-wing-week-2015-04-10__whole (west-wing-week) -> wh-west-wing-week-2015-06-05: 5
- sintel__pip25__0 (blender) -> nasa-twan-2020-01-25: 4
- sintel__pip25__0 (blender) -> nasa-twan-2020-02-07: 4
- nasa-twan-2020-01-25__excerpt60__1 (nasa-this-week) -> nasa-twan-2020-02-07: 4
- nasa-twan-2020-01-25__logo__1 (nasa-this-week) -> nasa-twan-2020-02-07: 4
- nasa-twan-2020-02-07__excerpt10__0 (nasa-this-week) -> nasa-twan-2020-01-25: 4

## Picture-in-picture (K = 10, N = 1000, N2 = 0, M = 25, 1 fps)

| verifier | pip25 | pip40 | pip25 centre | pip25 corner | pip40 centre | pip40 corner | false (unrelated) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 25 |
| 1920 | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 25 |
| 1024+tiles | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 25 |
| 1920+tiles | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 25 |

## Stills (votes fitted on tuning; recommended: 1920/64)

| verifier size / codes | votes | found | relationship identical | median time error (s) | false (unrelated stills) |
| --- | --- | --- | --- | --- | --- |
| 512/64 | 6 | 49% | 44% | 1.1 | 2 of 125 |
| 512/128 | 6 | 49% | 44% | 1.1 | 2 of 125 |
| 512/256 | 6 | 49% | 44% | 1.1 | 2 of 125 |
| 1024/64 | 8 | 22% | 20% | 1.2 | 1 of 125 |
| 1024/128 | 8 | 22% | 20% | 1.2 | 1 of 125 |
| 1024/256 | 8 | 22% | 20% | 1.2 | 1 of 125 |
| 1920/64 | 8 | 9% | 7% | 2.9 | 0 of 125 |
| 1920/128 | 8 | 9% | 7% | 2.9 | 0 of 125 |
| 1920/256 | 8 | 9% | 7% | 2.9 | 0 of 125 |

## Code volume (originals of this split, fitted N)

| K | N | keyframes / min | codes / min | codes per 90-min film |
| --- | --- | --- | --- | --- |
| 5 | 1000 | 16.0 | 79.5 | 7,157 |
| 10 | 1000 | 15.8 | 156.2 | 14,056 |
| 20 | 3 | 15.8 | 297.8 | 26,804 |

## Timing (one process; seconds per minute of video unless stated)

- creator: 1.5
- verifier 512 fps=1 (excerpt60): 1.8
- verifier 512 fps=2 (excerpt60): 3.3
- verifier 1024 fps=1 (excerpt60): 3.1
- verifier 1024 fps=2 (excerpt60): 6.1
- verifier 1024 fps=1 (pip25): 5.5
- verifier 1920 fps=1 (pip25): 9.7
- verifier 1024+tiles fps=1 (pip25): 18.5
- verifier 1920+tiles fps=1 (pip25): 22.5
- still 512/64 (ms per still): 38
- still 512/128 (ms per still): 36
- still 512/256 (ms per still): 37
- still 1024/64 (ms per still): 59
- still 1024/128 (ms per still): 67
- still 1024/256 (ms per still): 60
- still 1920/64 (ms per still): 75
- still 1920/128 (ms per still): 75
- still 1920/256 (ms per still): 76
