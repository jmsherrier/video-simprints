# video-simprints test report: tuning split

Recipe video-simprints/0.1 on image-simprints/2.2; ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. Stop codes (N) and min frames (M) fitted on the tuning split. 120 queries.

## Video-level match rate (correct video, time range within 3 s)

| setting | N | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | still | mean (clips) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 1000 | 1 | 78% | 100% | 100% | 44% | 11% | 33% | 89% | 89% | 100% | 73% | 71.6% |
| codes=5;spread=0;size=512;fps=2 | 1 | 1 | 89% | 100% | 100% | 44% | 11% | 56% | 89% | 100% | 100% | 73% | 76.5% |
| codes=5;spread=0;size=1024;fps=1 | 1000 | 1 | 78% | 100% | 100% | 44% | 11% | 33% | 100% | 89% | 100% | 73% | 72.8% |
| codes=5;spread=0;size=1024;fps=2 | 1 | 1 | 78% | 100% | 100% | 44% | 11% | 56% | 100% | 89% | 100% | 67% | 75.3% |
| codes=5;spread=1;size=512;fps=1 | 1000 | 1 | 78% | 89% | 100% | 56% | 11% | 44% | 89% | 89% | 100% | 73% | 72.8% |
| codes=5;spread=1;size=512;fps=2 | 1000 | 1 | 78% | 100% | 100% | 44% | 11% | 44% | 89% | 100% | 100% | 73% | 74.1% |
| codes=5;spread=1;size=1024;fps=1 | 1000 | 1 | 89% | 100% | 100% | 22% | 22% | 44% | 100% | 89% | 100% | 67% | 74.1% |
| codes=5;spread=1;size=1024;fps=2 | 1000 | 1 | 89% | 100% | 100% | 22% | 22% | 44% | 100% | 100% | 100% | 67% | 75.3% |
| codes=10;spread=0;size=512;fps=1 | 1000 | 1 | 67% | 100% | 100% | 89% | 11% | 67% | 100% | 100% | 100% | 73% | 81.5% |
| codes=10;spread=0;size=512;fps=2 | 1000 | 1 | 78% | 100% | 100% | 89% | 11% | 67% | 100% | 100% | 100% | 73% | 82.7% |
| codes=10;spread=0;size=1024;fps=1 | 1000 | 1 | 67% | 100% | 100% | 89% | 22% | 67% | 100% | 100% | 100% | 73% | 82.7% |
| codes=10;spread=0;size=1024;fps=2 | 1000 | 1 | 78% | 100% | 100% | 100% | 22% | 67% | 100% | 100% | 100% | 73% | 85.2% |
| codes=10;spread=1;size=512;fps=1 | 1000 | 1 | 78% | 100% | 100% | 78% | 11% | 67% | 100% | 100% | 100% | 73% | 81.5% |
| codes=10;spread=1;size=512;fps=2 | 1000 | 2 | 78% | 100% | 100% | 78% | 11% | 67% | 100% | 100% | 100% | 73% | 81.5% |
| codes=10;spread=1;size=1024;fps=1 | 1000 | 1 | 78% | 100% | 100% | 89% | 22% | 67% | 100% | 100% | 100% | 67% | 84.0% |
| codes=10;spread=1;size=1024;fps=2 | 1000 | 1 | 78% | 100% | 100% | 89% | 22% | 67% | 100% | 100% | 100% | 67% | 84.0% |
| codes=20;spread=0;size=512;fps=1 | 1000 | 1 | 78% | 100% | 100% | 89% | 33% | 78% | 100% | 100% | 100% | 80% | 86.4% |
| codes=20;spread=0;size=512;fps=2 | 1000 | 1 | 78% | 100% | 100% | 89% | 44% | 78% | 100% | 100% | 100% | 80% | 87.7% |
| codes=20;spread=0;size=1024;fps=1 | 1000 | 1 | 78% | 100% | 100% | 100% | 22% | 78% | 100% | 100% | 100% | 80% | 86.4% |
| codes=20;spread=0;size=1024;fps=2 | 1000 | 2 | 78% | 100% | 100% | 100% | 22% | 78% | 100% | 100% | 100% | 80% | 86.4% |
| codes=20;spread=1;size=512;fps=1 | 1000 | 1 | 78% | 100% | 100% | 89% | 33% | 67% | 100% | 100% | 100% | 80% | 85.2% |
| codes=20;spread=1;size=512;fps=2 | 1000 | 1 | 78% | 100% | 100% | 89% | 33% | 67% | 100% | 100% | 100% | 80% | 85.2% |
| codes=20;spread=1;size=1024;fps=1 | 1000 | 1 | 78% | 100% | 100% | 100% | 22% | 67% | 100% | 100% | 100% | 80% | 85.2% |
| codes=20;spread=1;size=1024;fps=2 | 1000 | 2 | 78% | 100% | 100% | 100% | 22% | 67% | 100% | 100% | 100% | 80% | 85.2% |

## Expected spatial relationship (share of clips found with it)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | still |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 67% | 89% | 100% | 44% | 11% | 22% | 89% | 67% | 89% | 47% |
| codes=5;spread=0;size=512;fps=2 | 89% | 100% | 100% | 22% | 11% | 56% | 78% | 89% | 89% | 47% |
| codes=5;spread=0;size=1024;fps=1 | 67% | 89% | 100% | 33% | 11% | 22% | 100% | 78% | 89% | 47% |
| codes=5;spread=0;size=1024;fps=2 | 78% | 100% | 100% | 33% | 11% | 56% | 89% | 78% | 100% | 47% |
| codes=5;spread=1;size=512;fps=1 | 56% | 78% | 100% | 56% | 11% | 33% | 89% | 89% | 100% | 47% |
| codes=5;spread=1;size=512;fps=2 | 78% | 89% | 100% | 33% | 11% | 33% | 89% | 100% | 100% | 47% |
| codes=5;spread=1;size=1024;fps=1 | 67% | 89% | 100% | 22% | 22% | 33% | 100% | 78% | 100% | 40% |
| codes=5;spread=1;size=1024;fps=2 | 89% | 89% | 100% | 22% | 22% | 33% | 100% | 78% | 100% | 40% |
| codes=10;spread=0;size=512;fps=1 | 67% | 89% | 100% | 89% | 11% | 67% | 100% | 67% | 89% | 47% |
| codes=10;spread=0;size=512;fps=2 | 78% | 89% | 100% | 89% | 11% | 67% | 100% | 89% | 89% | 47% |
| codes=10;spread=0;size=1024;fps=1 | 56% | 100% | 100% | 89% | 22% | 56% | 100% | 78% | 89% | 47% |
| codes=10;spread=0;size=1024;fps=2 | 78% | 100% | 100% | 100% | 22% | 67% | 100% | 67% | 89% | 47% |
| codes=10;spread=1;size=512;fps=1 | 67% | 89% | 100% | 67% | 11% | 56% | 100% | 89% | 89% | 47% |
| codes=10;spread=1;size=512;fps=2 | 67% | 100% | 100% | 67% | 11% | 56% | 100% | 100% | 89% | 47% |
| codes=10;spread=1;size=1024;fps=1 | 56% | 89% | 100% | 89% | 22% | 56% | 100% | 89% | 89% | 40% |
| codes=10;spread=1;size=1024;fps=2 | 78% | 100% | 100% | 89% | 22% | 67% | 100% | 89% | 89% | 40% |
| codes=20;spread=0;size=512;fps=1 | 56% | 89% | 100% | 78% | 33% | 78% | 89% | 78% | 89% | 53% |
| codes=20;spread=0;size=512;fps=2 | 56% | 89% | 100% | 78% | 44% | 78% | 89% | 100% | 89% | 53% |
| codes=20;spread=0;size=1024;fps=1 | 56% | 89% | 100% | 100% | 22% | 78% | 100% | 89% | 89% | 53% |
| codes=20;spread=0;size=1024;fps=2 | 67% | 89% | 100% | 100% | 22% | 78% | 100% | 100% | 89% | 53% |
| codes=20;spread=1;size=512;fps=1 | 56% | 78% | 100% | 78% | 33% | 67% | 89% | 89% | 89% | 53% |
| codes=20;spread=1;size=512;fps=2 | 56% | 89% | 100% | 78% | 33% | 67% | 89% | 100% | 89% | 53% |
| codes=20;spread=1;size=1024;fps=1 | 56% | 100% | 100% | 100% | 22% | 67% | 100% | 89% | 89% | 53% |
| codes=20;spread=1;size=1024;fps=2 | 67% | 78% | 100% | 100% | 22% | 67% | 100% | 100% | 89% | 53% |

## Frame-level match rate (sampled frames matching a keyframe of the source)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 51% | 50% | 66% | 11% | 0% | 7% | 45% | 46% | 55% |
| codes=5;spread=0;size=512;fps=2 | 45% | 42% | 52% | 9% | 1% | 6% | 42% | 44% | 49% |
| codes=5;spread=0;size=1024;fps=1 | 51% | 51% | 62% | 11% | 1% | 6% | 45% | 48% | 53% |
| codes=5;spread=0;size=1024;fps=2 | 47% | 41% | 51% | 10% | 1% | 6% | 41% | 43% | 44% |
| codes=5;spread=1;size=512;fps=1 | 56% | 54% | 69% | 5% | 0% | 8% | 50% | 49% | 56% |
| codes=5;spread=1;size=512;fps=2 | 56% | 54% | 68% | 5% | 1% | 9% | 51% | 51% | 55% |
| codes=5;spread=1;size=1024;fps=1 | 56% | 54% | 67% | 5% | 1% | 7% | 50% | 50% | 56% |
| codes=5;spread=1;size=1024;fps=2 | 56% | 54% | 67% | 6% | 1% | 8% | 51% | 50% | 56% |
| codes=10;spread=0;size=512;fps=1 | 58% | 63% | 74% | 23% | 0% | 16% | 61% | 61% | 66% |
| codes=10;spread=0;size=512;fps=2 | 59% | 61% | 73% | 23% | 1% | 16% | 61% | 62% | 65% |
| codes=10;spread=0;size=1024;fps=1 | 58% | 63% | 72% | 39% | 3% | 14% | 60% | 61% | 65% |
| codes=10;spread=0;size=1024;fps=2 | 58% | 61% | 72% | 40% | 3% | 15% | 59% | 61% | 65% |
| codes=10;spread=1;size=512;fps=1 | 67% | 64% | 76% | 21% | 0% | 13% | 67% | 66% | 71% |
| codes=10;spread=1;size=512;fps=2 | 66% | 65% | 75% | 21% | 1% | 14% | 67% | 64% | 71% |
| codes=10;spread=1;size=1024;fps=1 | 64% | 66% | 76% | 37% | 1% | 14% | 67% | 65% | 72% |
| codes=10;spread=1;size=1024;fps=2 | 65% | 65% | 75% | 38% | 2% | 14% | 67% | 64% | 71% |
| codes=20;spread=0;size=512;fps=1 | 70% | 70% | 79% | 37% | 3% | 25% | 71% | 74% | 77% |
| codes=20;spread=0;size=512;fps=2 | 69% | 68% | 79% | 38% | 3% | 24% | 71% | 73% | 76% |
| codes=20;spread=0;size=1024;fps=1 | 68% | 71% | 78% | 56% | 4% | 24% | 71% | 72% | 76% |
| codes=20;spread=0;size=1024;fps=2 | 68% | 69% | 78% | 56% | 4% | 24% | 70% | 72% | 75% |
| codes=20;spread=1;size=512;fps=1 | 71% | 70% | 81% | 40% | 2% | 22% | 70% | 74% | 79% |
| codes=20;spread=1;size=512;fps=2 | 72% | 70% | 81% | 42% | 2% | 22% | 71% | 74% | 77% |
| codes=20;spread=1;size=1024;fps=1 | 70% | 71% | 80% | 53% | 4% | 20% | 72% | 74% | 78% |
| codes=20;spread=1;size=1024;fps=2 | 71% | 70% | 80% | 55% | 4% | 21% | 72% | 74% | 77% |

## False matches

| setting | unrelated videos | unrelated frames | unrelated stills | wrong video in a manipulated clip |
| --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=5;spread=0;size=512;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=5;spread=0;size=1024;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=5;spread=0;size=1024;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=5;spread=1;size=512;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=5;spread=1;size=512;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=5;spread=1;size=1024;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=5;spread=1;size=1024;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=10;spread=0;size=512;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=10;spread=0;size=512;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=10;spread=0;size=1024;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=10;spread=0;size=1024;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=10;spread=1;size=512;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=10;spread=1;size=512;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=10;spread=1;size=1024;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=10;spread=1;size=1024;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=20;spread=0;size=512;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=20;spread=0;size=512;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=20;spread=0;size=1024;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=20;spread=0;size=1024;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=20;spread=1;size=512;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=20;spread=1;size=512;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |
| codes=20;spread=1;size=1024;fps=1 | 0 of 4 | 0 of 478 | 0 of 20 | 0 |
| codes=20;spread=1;size=1024;fps=2 | 0 of 4 | 0 of 954 | 0 of 20 | 0 |

## Code volume (originals of this split)

| codes | spread | N | keyframes / min | codes / min | codes per 90-min film |
| --- | --- | --- | --- | --- | --- |
| 5 | 0 | 1000 | 16.4 | 81.6 | 7,343 |
| 5 | 0 | 1 | 15.9 | 76.8 | 6,910 |
| 5 | 1 | 1000 | 16.3 | 81.1 | 7,297 |
| 10 | 0 | 1000 | 16.2 | 160.3 | 14,431 |
| 10 | 1 | 1000 | 15.9 | 157.3 | 14,158 |
| 20 | 0 | 1000 | 16.2 | 311.0 | 27,988 |
| 20 | 1 | 1000 | 15.9 | 305.9 | 27,533 |

## Timing (seconds per minute of video, one process)

- creator: 2.45 s
- verifier fps=1 size=512: 4.26 s
- verifier fps=1 size=1024: 6.23 s
- verifier fps=2 size=512: 8.58 s
- verifier fps=2 size=1024: 12.83 s
