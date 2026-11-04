# video-simprints report: test split

Recipe video-simprints/0.1 on image-simprints/2.2; ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. 618 queries. Thresholds fitted on the report-tuning split. N: per-video stop codes (`stop_after`, 1000 = off); N2: index-level stop codes (`shared_after`, None = off), counted against every other video of the split (originals and unrelated, leaving out the queried video and a picture-in-picture background); M: `min_frames`.

**Recommended** (chosen on tuning): K = 10, verifier 1024 px at 1 fps, N = 1000, N2 = 0, M = 10.

## Video-level match rate (right video, time range within 3 s) and false matches

| setting | N | N2 | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | mean | false (unrelated videos) | false (wrong video in a clip) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;size=512;fps=1 | 1000 | 0 | 10 | 11% | 69% | 83% | 6% | 0% | 0% | 56% | 44% | 69% | 37.7% | 0 of 34 | 0 |
| codes=5;size=512;fps=2 | 1000 | 0 | 20 | 6% | 69% | 86% | 3% | 0% | 0% | 56% | 42% | 69% | 36.7% | 0 of 34 | 0 |
| codes=5;size=1024;fps=1 | 1000 | 0 | 11 | 0% | 61% | 83% | 6% | 0% | 0% | 44% | 39% | 53% | 31.8% | 0 of 34 | 0 |
| codes=5;size=1024;fps=2 | 1000 | 0 | 20 | 6% | 67% | 83% | 6% | 0% | 0% | 56% | 42% | 64% | 35.8% | 0 of 34 | 0 |
| codes=10;size=512;fps=1 | 1000 | 0 | 15 | 0% | 64% | 92% | 8% | 0% | 0% | 61% | 50% | 75% | 38.9% | 0 of 34 | 0 |
| codes=10;size=512;fps=2 | 1000 | 0 | 25 | 0% | 69% | 97% | 8% | 0% | 0% | 69% | 67% | 83% | 43.8% | 0 of 34 | 0 |
| codes=10;size=1024;fps=1 | 1000 | 0 | 10 | 25% | 81% | 97% | 17% | 0% | 0% | 78% | 72% | 83% | 50.3% | 0 of 34 | 0 |
| codes=10;size=1024;fps=2 | 1000 | 0 | 20 | 11% | 81% | 97% | 17% | 0% | 0% | 78% | 75% | 83% | 49.1% | 0 of 34 | 0 |
| codes=20;size=512;fps=1 | 1000 | 0 | 15 | 0% | 78% | 97% | 22% | 0% | 3% | 81% | 72% | 83% | 48.5% | 0 of 34 | 0 |
| codes=20;size=512;fps=2 | 1000 | 0 | 30 | 0% | 72% | 97% | 22% | 0% | 0% | 81% | 72% | 83% | 47.5% | 0 of 34 | 0 |
| codes=20;size=1024;fps=1 | 1000 | 1 | 20 | 0% | 58% | 97% | 8% | 0% | 0% | 61% | 44% | 64% | 37.0% | 0 of 34 | 0 |
| codes=20;size=1024;fps=2 | 1000 | 0 | 30 | 0% | 69% | 97% | 22% | 0% | 0% | 81% | 75% | 83% | 47.5% | 0 of 34 | 0 |

## Frame-level match rate (sampled frames matching a keyframe of the source)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | unrelated frames with any match |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;size=512;fps=1 | 54% | 49% | 50% | 6% | 0% | 2% | 41% | 33% | 48% | 13 of 6679 |
| codes=5;size=512;fps=2 | 55% | 49% | 50% | 7% | 0% | 2% | 41% | 32% | 50% | 30 of 13345 |
| codes=5;size=1024;fps=1 | 56% | 48% | 49% | 10% | 0% | 2% | 40% | 32% | 46% | 32 of 6679 |
| codes=5;size=1024;fps=2 | 56% | 47% | 49% | 10% | 0% | 2% | 41% | 31% | 47% | 66 of 13345 |
| codes=10;size=512;fps=1 | 68% | 62% | 64% | 18% | 1% | 5% | 58% | 49% | 64% | 20 of 6679 |
| codes=10;size=512;fps=2 | 66% | 62% | 65% | 18% | 1% | 6% | 57% | 49% | 64% | 43 of 13345 |
| codes=10;size=1024;fps=1 | 68% | 60% | 63% | 19% | 1% | 5% | 57% | 49% | 62% | 28 of 6679 |
| codes=10;size=1024;fps=2 | 68% | 60% | 64% | 20% | 1% | 5% | 57% | 48% | 62% | 59 of 13345 |
| codes=20;size=512;fps=1 | 74% | 70% | 74% | 31% | 3% | 12% | 68% | 61% | 70% | 113 of 6679 |
| codes=20;size=512;fps=2 | 72% | 71% | 74% | 32% | 2% | 13% | 67% | 60% | 71% | 235 of 13345 |
| codes=20;size=1024;fps=1 | 76% | 71% | 74% | 34% | 3% | 13% | 68% | 62% | 69% | 163 of 6679 |
| codes=20;size=1024;fps=2 | 72% | 70% | 74% | 33% | 3% | 12% | 67% | 60% | 70% | 182 of 13345 |

## False matches against M (K = 10, 1024 px, 1 fps)

| M | recommended stop codes: match rate | recommended stop codes: false (unrelated) | recommended stop codes: false (wrong video) | no stop codes: match rate | no stop codes: false (unrelated) | no stop codes: false (wrong video) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 81.2% | 6 | 12 | 80.6% | 53 | 88 |
| 2 | 76.2% | 4 | 6 | 76.9% | 51 | 63 |
| 3 | 72.2% | 3 | 6 | 73.1% | 51 | 53 |
| 4 | 67.3% | 3 | 6 | 68.5% | 40 | 41 |
| 5 | 65.4% | 2 | 6 | 66.4% | 35 | 25 |
| 6 | 63.3% | 1 | 6 | 63.6% | 28 | 21 |
| 7 | 59.9% | 0 | 6 | 60.8% | 25 | 19 |
| 8 | 56.8% | 0 | 0 | 58.6% | 23 | 9 |
| 9 | 52.2% | 0 | 0 | 54.6% | 22 | 6 |
| 10 | 50.3% | 0 | 0 | 52.8% | 17 | 6 |
| 11 | 46.3% | 0 | 0 | 48.5% | 16 | 3 |
| 12 | 44.4% | 0 | 0 | 47.5% | 12 | 0 |
| 15 | 38.6% | 0 | 0 | 41.0% | 7 | 0 |
| 20 | 27.2% | 0 | 0 | 29.0% | 1 | 0 |
| 25 | 17.6% | 0 | 0 | 18.8% | 0 | 0 |
| 30 | 9.3% | 0 | 0 | 10.2% | 0 | 0 |

False matches at M = 1, recommended stop codes (query, its set, matched declaration, frames on the line):

- nasa-s2g-2016-08-11__excerpt60__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 7
- nasa-s2g-2016-08-11__excerpt60__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 7
- nasa-s2g-2016-08-11__caption__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 7
- nasa-s2g-2016-08-11__logo__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 7
- nasa-s2g-2016-08-11__logo__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 7
- hero__pip40__0 (blender) -> nasa-s2g-2017-01-06: 7
- nasa-s2g-2015-10-16__whole (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 6
- nasa-moment-aleksey-ovchinin__whole (nasa-moment) -> nasa-moment-kate-rubins: 5
- jpl-whats-up-2025-08__whole (jpl-whats-up) -> jpl-whats-up-2026-10: 4
- nasa-s2g-2017-05-26__whole (nasa-space-to-ground) -> nasa-s2g-2016-08-11: 2
- nasa-twan-2023-12-15__whole (nasa-this-week) -> nasa-twan-2020-11-06: 1
- jpl-whats-up-2025-08__whole (jpl-whats-up) -> jpl-whats-up-2025-09: 1
- tears-of-steel__caption__0 (blender) -> nasa-dscovr-launch: 1
- jpl-whats-up-2025-09__excerpt60__0 (jpl-whats-up) -> jpl-whats-up-2026-10: 1
- nasa-s2g-2016-08-11__excerpt30__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 1
- nasa-s2g-2016-08-11__lowres__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 1
- nasa-s2g-2016-08-11__caption__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 1
- hero__pip25__0 (blender) -> nasa-s2g-2016-08-11: 1

False matches at M = 1, no stop codes (query, its set, matched declaration, frames on the line):

- jpl-whats-up-2025-12__whole (jpl-whats-up) -> jpl-whats-up-2026-10: 21
- nasa-twan-2020-07-31__whole (nasa-this-week) -> nasa-twan-2020-12-11: 17
- jpl-whats-up-2025-12__whole (jpl-whats-up) -> jpl-whats-up-2025-09: 17
- jpl-whats-up-2026-05__whole (jpl-whats-up) -> jpl-whats-up-2026-10: 16
- nasa-twan-2020-06-12__whole (nasa-this-week) -> nasa-twan-2020-11-06: 15
- nasa-twan-2020-03-27__whole (nasa-this-week) -> nasa-twan-2020-12-11: 15
- jpl-whats-up-2026-11__whole (jpl-whats-up) -> jpl-whats-up-2026-10: 15
- nasa-twan-2018-11-09__whole (nasa-this-week) -> nasa-twan-2020-12-11: 14
- nasa-s2g-2015-10-16__whole (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 14
- nasa-twan-2020-06-12__whole (nasa-this-week) -> nasa-twan-2020-09-18: 13
- nasa-twan-2020-07-31__whole (nasa-this-week) -> nasa-twan-2020-11-06: 13
- nasa-s2g-2015-10-16__whole (nasa-space-to-ground) -> nasa-s2g-2016-08-11: 12
- nasa-twan-2020-06-12__whole (nasa-this-week) -> nasa-twan-2020-12-11: 11
- nasa-twan-2020-03-27__whole (nasa-this-week) -> nasa-twan-2020-09-18: 11
- nasa-twan-2020-03-27__whole (nasa-this-week) -> nasa-twan-2020-11-06: 11
- jpl-whats-up-2026-05__whole (jpl-whats-up) -> jpl-whats-up-2025-09: 11
- nasa-s2g-2016-08-11__excerpt60__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 11
- nasa-s2g-2016-08-11__caption__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 11
- nasa-s2g-2016-08-11__logo__0 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 11
- nasa-twan-2020-07-31__whole (nasa-this-week) -> nasa-twan-2020-09-18: 10
- nasa-s2g-2016-08-11__excerpt60__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 10
- nasa-s2g-2016-08-11__logo__1 (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 10
- hero__pip40__0 (blender) -> nasa-s2g-2017-01-06: 10
- nasa-twan-2018-11-09__whole (nasa-this-week) -> nasa-twan-2020-09-18: 9
- nasa-twan-2018-11-09__whole (nasa-this-week) -> nasa-twan-2020-11-06: 9
- jpl-whats-up-2025-08__whole (jpl-whats-up) -> jpl-whats-up-2025-09: 9
- jpl-whats-up-2025-08__whole (jpl-whats-up) -> jpl-whats-up-2026-10: 9
- jpl-whats-up-2026-11__whole (jpl-whats-up) -> jpl-whats-up-2025-09: 9
- nasa-s2g-2017-05-26__whole (nasa-space-to-ground) -> nasa-s2g-2016-08-11: 8
- jpl-whats-up-2025-09__excerpt30__1 (jpl-whats-up) -> jpl-whats-up-2026-10: 8
- jpl-whats-up-2025-09__logo__1 (jpl-whats-up) -> jpl-whats-up-2026-10: 8
- hero__pip40__0 (blender) -> nasa-s2g-2016-08-11: 8
- nasa-s2g-2018-02-23__whole (nasa-space-to-ground) -> nasa-s2g-2016-08-11: 7
- nasa-s2g-2018-02-23__whole (nasa-space-to-ground) -> nasa-s2g-2017-01-06: 7
- nasa-moment-kimiya-yui__excerpt10__1 (nasa-moment) -> nasa-moment-kate-rubins: 7
- nasa-moment-kimiya-yui__excerpt10__1 (nasa-moment) -> nasa-moment-tim-peake: 7
- nasa-twan-2020-12-11__pip25__0 (nasa-this-week) -> nasa-s2g-2016-08-11: 7
- jpl-whats-up-2026-10__excerpt60__0 (jpl-whats-up) -> jpl-whats-up-2025-09: 7
- nasa-s2g-2017-01-06__excerpt30__1 (nasa-space-to-ground) -> nasa-s2g-2016-08-11: 7
- nasa-s2g-2017-01-06__excerpt60__0 (nasa-space-to-ground) -> nasa-s2g-2016-08-11: 7

## Picture-in-picture (K = 10, N = 1000, N2 = 0, 1 fps)

Insets at 25% and 40% of the width of a 1080p unrelated video, at a random corner or the centre.

| verifier | pip25 | pip40 | pip25 centre | pip25 corner | pip40 centre | pip40 corner | false (unrelated) | false (wrong video) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1024 M=1 | 19% | 47% | 0% | 21% | 11% | 59% | 6 of 34 | 12 |
| 1024 M=3 | 3% | 28% | 0% | 3% | 0% | 37% | 3 of 34 | 6 |
| 1024 M=10 | 0% | 0% | 0% | 0% | 0% | 0% | 0 of 34 | 0 |
| 1920 M=1 | 17% | 44% | 0% | 18% | 22% | 52% | 7 of 34 | 2 |
| 1920 M=3 | 0% | 22% | 0% | 0% | 11% | 26% | 4 of 34 | 1 |
| 1920 M=10 | 0% | 3% | 0% | 0% | 0% | 4% | 0 of 34 | 0 |
| 1024+tiles M=1 | 64% | 81% | 0% | 68% | 56% | 89% | 7 of 34 | 3 |
| 1024+tiles M=3 | 42% | 67% | 0% | 44% | 44% | 74% | 4 of 34 | 1 |
| 1024+tiles M=10 | 11% | 31% | 0% | 12% | 11% | 37% | 0 of 34 | 0 |
| 1920+tiles M=1 | 61% | 78% | 0% | 65% | 56% | 85% | 7 of 34 | 3 |
| 1920+tiles M=3 | 42% | 67% | 0% | 44% | 44% | 74% | 4 of 34 | 1 |
| 1920+tiles M=10 | 11% | 31% | 0% | 12% | 11% | 37% | 0 of 34 | 0 |

## Stills (votes fitted on tuning; recommended: 1024/64)

| verifier size / codes | votes | found | relationship identical | median time error (s) | false (unrelated stills) |
| --- | --- | --- | --- | --- | --- |
| 512/64 | 3 | 58% | 43% | 0.9 | 1 of 170 |
| 512/128 | 3 | 58% | 43% | 0.9 | 1 of 170 |
| 512/256 | 3 | 58% | 43% | 0.9 | 1 of 170 |
| 1024/64 | 3 | 54% | 42% | 0.9 | 3 of 170 |
| 1024/128 | 3 | 54% | 42% | 0.9 | 3 of 170 |
| 1024/256 | 3 | 54% | 42% | 0.9 | 3 of 170 |
| 1920/64 | 2 | 52% | 38% | 0.9 | 2 of 170 |
| 1920/128 | 2 | 52% | 38% | 0.9 | 2 of 170 |
| 1920/256 | 2 | 52% | 38% | 0.9 | 2 of 170 |

## Code volume (originals of this split, fitted N)

| K | N | keyframes / min | codes / min | codes per 90-min film |
| --- | --- | --- | --- | --- |
| 5 | 1000 | 15.8 | 77.7 | 6,996 |
| 10 | 1000 | 15.7 | 150.8 | 13,576 |
| 20 | 1000 | 15.7 | 289.7 | 26,071 |

## Timing (one process; seconds per minute of video unless stated)

- creator: 1.5
- verifier 512 fps=1 (excerpt60): 2.4
- verifier 512 fps=2 (excerpt60): 4.5
- verifier 1024 fps=1 (excerpt60): 4.1
- verifier 1024 fps=2 (excerpt60): 7.9
- verifier 1024 fps=1 (pip25): 5.0
- verifier 1920 fps=1 (pip25): 9.5
- verifier 1024+tiles fps=1 (pip25): 16.7
- verifier 1920+tiles fps=1 (pip25): 21.0
- still 512/64 (ms per still): 52
- still 512/128 (ms per still): 55
- still 512/256 (ms per still): 55
- still 1024/64 (ms per still): 78
- still 1024/128 (ms per still): 80
- still 1024/256 (ms per still): 80
- still 1920/64 (ms per still): 94
- still 1920/128 (ms per still): 99
- still 1920/256 (ms per still): 97
