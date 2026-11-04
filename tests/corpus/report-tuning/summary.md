# video-simprints report: tuning split

Recipe video-simprints/0.1 on image-simprints/2.2; ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. 403 queries. Thresholds fitted on the tuning split. N: per-video stop codes (`stop_after`, 1000 = off); N2: index-level stop codes (`shared_after`, None = off), counted against every other video of the split (originals and unrelated, leaving out the queried video and a picture-in-picture background); M: `min_frames`.

**Recommended** (chosen on tuning): K = 10, verifier 1024 px at 1 fps, N = 1000, N2 = 0, M = 10.

## Video-level match rate (right video, time range within 3 s) and false matches

| setting | N | N2 | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | mean | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;size=512;fps=1 | 1000 | 0 | 10 | 9% | 68% | 95% | 0% | 0% | 0% | 55% | 45% | 73% | 38.4% | 0 of 25 | 0 |
| codes=5;size=512;fps=2 | 1000 | 0 | 20 | 5% | 64% | 95% | 5% | 0% | 0% | 59% | 41% | 73% | 37.9% | 0 of 25 | 0 |
| codes=5;size=1024;fps=1 | 1000 | 0 | 11 | 0% | 64% | 95% | 0% | 0% | 0% | 55% | 32% | 55% | 33.3% | 0 of 25 | 0 |
| codes=5;size=1024;fps=2 | 1000 | 0 | 20 | 0% | 59% | 95% | 5% | 0% | 0% | 59% | 41% | 64% | 35.9% | 0 of 25 | 0 |
| codes=10;size=512;fps=1 | 1000 | 0 | 15 | 0% | 68% | 95% | 5% | 0% | 0% | 64% | 55% | 59% | 38.4% | 0 of 25 | 0 |
| codes=10;size=512;fps=2 | 1000 | 0 | 25 | 0% | 64% | 100% | 18% | 0% | 0% | 68% | 59% | 73% | 42.4% | 0 of 25 | 0 |
| codes=10;size=1024;fps=1 | 1000 | 0 | 10 | 18% | 73% | 95% | 27% | 0% | 0% | 77% | 82% | 82% | 50.5% | 0 of 25 | 0 |
| codes=10;size=1024;fps=2 | 1000 | 0 | 20 | 5% | 68% | 100% | 27% | 0% | 0% | 77% | 77% | 86% | 49.0% | 0 of 25 | 0 |
| codes=20;size=512;fps=1 | 1000 | 0 | 15 | 0% | 68% | 95% | 32% | 0% | 0% | 73% | 73% | 77% | 46.5% | 0 of 25 | 0 |
| codes=20;size=512;fps=2 | 1000 | 0 | 30 | 0% | 64% | 100% | 27% | 0% | 0% | 77% | 68% | 77% | 46.0% | 0 of 25 | 0 |
| codes=20;size=1024;fps=1 | 1000 | 1 | 20 | 0% | 55% | 95% | 9% | 0% | 0% | 59% | 55% | 45% | 35.4% | 0 of 25 | 0 |
| codes=20;size=1024;fps=2 | 1000 | 0 | 30 | 0% | 64% | 100% | 27% | 0% | 0% | 73% | 68% | 82% | 46.0% | 0 of 25 | 0 |

## Frame-level match rate (sampled frames matching a keyframe of the source)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | unrelated frames with any match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;size=512;fps=1 | 45% | 51% | 52% | 10% | 2% | 1% | 46% | 31% | 50% | 40 of 3497 |
| codes=5;size=512;fps=2 | 47% | 51% | 51% | 9% | 2% | 1% | 47% | 31% | 49% | 78 of 6981 |
| codes=5;size=1024;fps=1 | 45% | 51% | 51% | 10% | 1% | 1% | 44% | 31% | 47% | 44 of 3497 |
| codes=5;size=1024;fps=2 | 45% | 51% | 50% | 10% | 1% | 1% | 45% | 32% | 47% | 81 of 6981 |
| codes=10;size=512;fps=1 | 58% | 61% | 62% | 23% | 1% | 5% | 60% | 49% | 62% | 59 of 3497 |
| codes=10;size=512;fps=2 | 58% | 60% | 61% | 23% | 2% | 6% | 61% | 49% | 60% | 108 of 6981 |
| codes=10;size=1024;fps=1 | 59% | 60% | 61% | 24% | 1% | 5% | 58% | 49% | 60% | 46 of 3497 |
| codes=10;size=1024;fps=2 | 58% | 60% | 61% | 23% | 1% | 6% | 60% | 49% | 59% | 86 of 6981 |
| codes=20;size=512;fps=1 | 67% | 67% | 69% | 34% | 2% | 11% | 68% | 62% | 70% | 86 of 3497 |
| codes=20;size=512;fps=2 | 66% | 67% | 68% | 33% | 3% | 11% | 69% | 62% | 69% | 165 of 6981 |
| codes=20;size=1024;fps=1 | 68% | 68% | 68% | 34% | 2% | 11% | 68% | 63% | 69% | 161 of 3497 |
| codes=20;size=1024;fps=2 | 66% | 68% | 67% | 33% | 2% | 11% | 68% | 61% | 68% | 153 of 6981 |

## False matches against M (K = 10, 1024 px, 1 fps)

| M | recommended stop codes: match rate | recommended stop codes: false (unrelated) | recommended stop codes: false (wrong video) | no stop codes: match rate | no stop codes: false (unrelated) | no stop codes: false (wrong video) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 77.8% | 7 | 14 | 77.3% | 28 | 36 |
| 2 | 75.3% | 5 | 6 | 75.8% | 28 | 27 |
| 3 | 73.2% | 4 | 5 | 74.2% | 27 | 25 |
| 4 | 70.2% | 3 | 4 | 70.7% | 25 | 21 |
| 5 | 67.2% | 3 | 4 | 68.2% | 24 | 10 |
| 6 | 64.6% | 2 | 4 | 66.2% | 15 | 10 |
| 7 | 60.1% | 2 | 4 | 62.1% | 12 | 8 |
| 8 | 56.1% | 2 | 2 | 59.6% | 12 | 6 |
| 9 | 54.5% | 2 | 0 | 58.1% | 12 | 6 |
| 10 | 50.5% | 0 | 0 | 54.5% | 12 | 4 |
| 11 | 46.0% | 0 | 0 | 49.0% | 11 | 0 |
| 12 | 43.9% | 0 | 0 | 44.9% | 11 | 0 |
| 15 | 37.9% | 0 | 0 | 40.4% | 8 | 0 |
| 20 | 26.3% | 0 | 0 | 31.8% | 3 | 0 |
| 25 | 15.7% | 0 | 0 | 18.2% | 0 | 0 |
| 30 | 8.6% | 0 | 0 | 9.1% | 0 | 0 |

False matches at M = 1, recommended stop codes (query, its set, matched declaration, frames on the line):

- jpl-whats-up-2026-01__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 9
- nasa-s2g-2015-02-27__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 9
- nasa-moment-shane-kimbrough__pip40__0 (nasa-moment) -> nasa-s2g-2015-03-06: 8
- coffee-run__pip25__1 (blender) -> nasa-s2g-2015-03-06: 8
- jpl-whats-up-2026-04__pip40__1 (jpl-whats-up) -> nasa-s2g-2015-03-06: 7
- coffee-run__pip25__0 (blender) -> nasa-s2g-2015-03-06: 7
- wh-west-wing-week-2015-04-10__whole (west-wing-week) -> wh-west-wing-week-2015-06-05: 5
- nasa-s2g-2014-10-24__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 3
- coffee-run__pip40__0 (blender) -> wh-west-wing-week-2015-06-05: 3
- nasa-twan-2017-08-18__whole (nasa-this-week) -> nasa-atlas-v-tdrs-m: 2
- nasa-s2g-2015-03-06__pip25__0 (nasa-space-to-ground) -> jpl-whats-up-2026-04: 2
- jpl-whats-up-2026-02__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 1
- jpl-whats-up-2025-11__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 1
- nasa-tim-kopra__pip40__1 (nasa-moment) -> nasa-s2g-2015-03-06: 1
- nasa-crs7-countdown__pip25__1 (launch) -> jpl-whats-up-2026-04: 1
- nasa-moment-shane-kimbrough__pip40__1 (nasa-moment) -> jpl-whats-up-2026-04: 1
- nasa-twan-2020-01-25__logo__0 (nasa-this-week) -> nasa-twan-2020-02-07: 1
- nasa-twan-2020-02-07__pip40__0 (nasa-this-week) -> jpl-whats-up-2026-04: 1
- nasa-s2g-2015-03-06__pip40__1 (nasa-space-to-ground) -> jpl-whats-up-2026-04: 1
- nasa-atlas-v-tdrs-m__pip25__1 (launch) -> jpl-whats-up-2026-04: 1
- nasa-atlas-v-tdrs-m__pip40__1 (launch) -> nasa-s2g-2015-03-06: 1

False matches at M = 1, no stop codes (query, its set, matched declaration, frames on the line):

- jpl-whats-up-2026-02__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 23
- jpl-whats-up-2026-01__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 23
- nasa-s2g-2015-02-27__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 22
- nasa-s2g-2018-01-19__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 18
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-01-25: 16
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-02-07: 15
- nasa-twan-2020-01-18__whole (nasa-this-week) -> nasa-twan-2020-02-07: 15
- jpl-whats-up-2025-11__whole (jpl-whats-up) -> jpl-whats-up-2026-04: 15
- nasa-twan-2020-01-31__whole (nasa-this-week) -> nasa-twan-2020-01-25: 12
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-01-25: 12
- nasa-twan-2020-02-14__whole (nasa-this-week) -> nasa-twan-2020-02-07: 12
- nasa-s2g-2014-10-24__whole (nasa-space-to-ground) -> nasa-s2g-2015-03-06: 10
- nasa-moment-shane-kimbrough__pip40__0 (nasa-moment) -> nasa-s2g-2015-03-06: 10
- jpl-whats-up-2026-04__pip40__1 (jpl-whats-up) -> nasa-s2g-2015-03-06: 10
- coffee-run__pip25__0 (blender) -> nasa-s2g-2015-03-06: 10
- coffee-run__pip25__1 (blender) -> nasa-s2g-2015-03-06: 10
- sintel__pip40__0 (blender) -> nasa-s2g-2015-03-06: 9
- nasa-crs7-countdown__pip25__0 (launch) -> nasa-s2g-2015-03-06: 9
- nasa-tim-kopra__pip40__1 (nasa-moment) -> nasa-s2g-2015-03-06: 7
- nasa-atlas-v-tdrs-m__pip40__1 (launch) -> nasa-s2g-2015-03-06: 7
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 6
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-s2g-2015-03-06: 6
- nasa-moment-oleg-kononenko__whole (nasa-moment) -> nasa-tim-kopra: 6
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-s2g-2015-03-06: 6
- nasa-moment-shane-kimbrough__vertical__1 (nasa-moment) -> nasa-tim-kopra: 6
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-s2g-2015-03-06: 5
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-tim-kopra: 5
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 5
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-s2g-2015-03-06: 5
- nasa-moment-yuri-malenchenko__whole (nasa-moment) -> nasa-tim-kopra: 5
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 5
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-s2g-2015-03-06: 5
- nasa-moment-gennady-padalka__whole (nasa-moment) -> nasa-tim-kopra: 5
- wh-west-wing-week-2015-04-10__whole (west-wing-week) -> wh-west-wing-week-2015-06-05: 5
- nasa-moment-peggy-whitson__whole (nasa-moment) -> nasa-moment-shane-kimbrough: 4
- sintel__pip25__0 (blender) -> nasa-twan-2020-01-25: 4
- sintel__pip25__0 (blender) -> nasa-twan-2020-02-07: 4
- nasa-twan-2020-01-25__excerpt60__1 (nasa-this-week) -> nasa-twan-2020-02-07: 4
- nasa-twan-2020-01-25__logo__1 (nasa-this-week) -> nasa-twan-2020-02-07: 4
- nasa-twan-2020-02-07__excerpt10__0 (nasa-this-week) -> nasa-twan-2020-01-25: 4

## Picture-in-picture (K = 10, N = 1000, N2 = 0, M = 10, 1 fps)

| verifier | pip25 | pip40 | pip25 centre | pip25 corner | pip40 centre | pip40 corner | false (unrelated) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 25 |
| 1920 | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 25 |
| 1024+tiles | 14% | 36% | 0% | 19% | 0% | 38% | 0 of 25 |
| 1920+tiles | 14% | 36% | 0% | 19% | 0% | 38% | 0 of 25 |

## Stills (votes fitted on tuning; recommended: 1024/64)

| verifier size / codes | votes | found | relationship identical | median time error (s) | false (unrelated stills) |
| --- | --- | --- | --- | --- | --- |
| 512/64 | 3 | 64% | 58% | 1.0 | 0 of 125 |
| 512/128 | 3 | 64% | 58% | 1.0 | 0 of 125 |
| 512/256 | 3 | 64% | 58% | 1.0 | 0 of 125 |
| 1024/64 | 3 | 65% | 49% | 1.4 | 0 of 125 |
| 1024/128 | 3 | 65% | 49% | 1.4 | 0 of 125 |
| 1024/256 | 3 | 65% | 49% | 1.4 | 0 of 125 |
| 1920/64 | 2 | 56% | 42% | 1.8 | 0 of 125 |
| 1920/128 | 2 | 56% | 42% | 1.8 | 0 of 125 |
| 1920/256 | 2 | 56% | 42% | 1.8 | 0 of 125 |

## Code volume (originals of this split, fitted N)

| K | N | keyframes / min | codes / min | codes per 90-min film |
| --- | --- | --- | --- | --- |
| 5 | 1000 | 16.0 | 79.5 | 7,157 |
| 10 | 1000 | 15.8 | 156.2 | 14,056 |
| 20 | 1000 | 15.8 | 302.2 | 27,200 |

## Timing (one process; seconds per minute of video unless stated)

- creator: 1.5
- verifier 512 fps=1 (excerpt60): 1.6
- verifier 512 fps=2 (excerpt60): 3.3
- verifier 1024 fps=1 (excerpt60): 3.2
- verifier 1024 fps=2 (excerpt60): 6.0
- verifier 1024 fps=1 (pip25): 5.5
- verifier 1920 fps=1 (pip25): 9.8
- verifier 1024+tiles fps=1 (pip25): 18.5
- verifier 1920+tiles fps=1 (pip25): 22.5
- still 512/64 (ms per still): 40
- still 512/128 (ms per still): 37
- still 512/256 (ms per still): 36
- still 1024/64 (ms per still): 57
- still 1024/128 (ms per still): 59
- still 1024/256 (ms per still): 61
- still 1920/64 (ms per still): 75
- still 1920/128 (ms per still): 75
- still 1920/256 (ms per still): 75
