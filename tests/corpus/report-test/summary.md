# video-simprints test report: test split

Recipe video-simprints/0.1 on image-simprints/2.2; ffmpeg version 8.1.2-full_build-www.gyan.dev Copyright (c) 2000-2026 the FFmpeg developers. Stop codes (N) and min frames (M) fitted on the report-tuning split. 158 queries.

## Video-level match rate (correct video, time range within 3 s)

| setting | N | M | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | still | mean (clips) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 1000 | 1 | 75% | 100% | 100% | 33% | 0% | 17% | 92% | 92% | 100% | 55% | 67.6% |
| codes=5;spread=0;size=512;fps=2 | 1 | 1 | 92% | 100% | 100% | 50% | 0% | 25% | 100% | 92% | 100% | 40% | 73.1% |
| codes=5;spread=0;size=1024;fps=1 | 1000 | 1 | 75% | 100% | 100% | 42% | 0% | 0% | 92% | 92% | 100% | 55% | 66.7% |
| codes=5;spread=0;size=1024;fps=2 | 1 | 1 | 83% | 100% | 100% | 50% | 0% | 25% | 100% | 92% | 100% | 35% | 72.2% |
| codes=5;spread=1;size=512;fps=1 | 1000 | 1 | 75% | 100% | 100% | 17% | 0% | 33% | 100% | 92% | 100% | 55% | 68.5% |
| codes=5;spread=1;size=512;fps=2 | 1000 | 1 | 92% | 100% | 100% | 42% | 0% | 33% | 100% | 92% | 100% | 55% | 73.1% |
| codes=5;spread=1;size=1024;fps=1 | 1000 | 1 | 83% | 100% | 100% | 25% | 0% | 17% | 92% | 92% | 100% | 60% | 67.6% |
| codes=5;spread=1;size=1024;fps=2 | 1000 | 1 | 83% | 100% | 100% | 33% | 0% | 25% | 100% | 92% | 100% | 60% | 70.4% |
| codes=10;spread=0;size=512;fps=1 | 1000 | 1 | 83% | 100% | 100% | 50% | 8% | 33% | 92% | 92% | 100% | 60% | 73.1% |
| codes=10;spread=0;size=512;fps=2 | 1000 | 1 | 92% | 100% | 100% | 58% | 17% | 42% | 100% | 100% | 100% | 60% | 78.7% |
| codes=10;spread=0;size=1024;fps=1 | 1000 | 1 | 83% | 100% | 100% | 75% | 8% | 8% | 100% | 92% | 100% | 70% | 74.1% |
| codes=10;spread=0;size=1024;fps=2 | 1000 | 1 | 83% | 100% | 100% | 83% | 17% | 50% | 100% | 100% | 100% | 70% | 81.5% |
| codes=10;spread=1;size=512;fps=1 | 1000 | 1 | 83% | 100% | 100% | 50% | 8% | 33% | 100% | 92% | 100% | 65% | 74.1% |
| codes=10;spread=1;size=512;fps=2 | 1000 | 2 | 92% | 100% | 100% | 50% | 0% | 33% | 100% | 92% | 100% | 65% | 74.1% |
| codes=10;spread=1;size=1024;fps=1 | 1000 | 1 | 83% | 100% | 100% | 75% | 8% | 25% | 100% | 92% | 100% | 65% | 75.9% |
| codes=10;spread=1;size=1024;fps=2 | 1000 | 1 | 92% | 100% | 100% | 83% | 17% | 33% | 100% | 100% | 100% | 65% | 80.6% |
| codes=20;spread=0;size=512;fps=1 | 1000 | 1 | 83% | 100% | 100% | 75% | 8% | 58% | 100% | 92% | 100% | 75% | 79.6% |
| codes=20;spread=0;size=512;fps=2 | 1000 | 1 | 92% | 100% | 100% | 83% | 17% | 67% | 100% | 100% | 100% | 75% | 84.3% |
| codes=20;spread=0;size=1024;fps=1 | 1000 | 1 | 83% | 100% | 100% | 83% | 8% | 50% | 100% | 92% | 100% | 75% | 79.6% |
| codes=20;spread=0;size=1024;fps=2 | 1000 | 2 | 92% | 100% | 100% | 92% | 8% | 67% | 100% | 100% | 100% | 75% | 84.3% |
| codes=20;spread=1;size=512;fps=1 | 1000 | 1 | 83% | 100% | 100% | 75% | 8% | 50% | 100% | 92% | 100% | 75% | 78.7% |
| codes=20;spread=1;size=512;fps=2 | 1000 | 1 | 92% | 100% | 100% | 92% | 17% | 58% | 100% | 100% | 100% | 75% | 84.3% |
| codes=20;spread=1;size=1024;fps=1 | 1000 | 1 | 83% | 100% | 100% | 83% | 8% | 33% | 100% | 92% | 100% | 75% | 77.8% |
| codes=20;spread=1;size=1024;fps=2 | 1000 | 2 | 92% | 100% | 100% | 92% | 8% | 42% | 100% | 100% | 100% | 75% | 81.5% |

## Expected spatial relationship (share of clips found with it)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo | still |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 67% | 92% | 100% | 25% | 0% | 17% | 75% | 92% | 92% | 35% |
| codes=5;spread=0;size=512;fps=2 | 67% | 100% | 100% | 42% | 0% | 25% | 92% | 92% | 100% | 20% |
| codes=5;spread=0;size=1024;fps=1 | 67% | 92% | 100% | 42% | 0% | 0% | 75% | 92% | 100% | 35% |
| codes=5;spread=0;size=1024;fps=2 | 67% | 100% | 100% | 42% | 0% | 25% | 92% | 92% | 100% | 20% |
| codes=5;spread=1;size=512;fps=1 | 58% | 100% | 100% | 17% | 0% | 33% | 83% | 92% | 100% | 45% |
| codes=5;spread=1;size=512;fps=2 | 75% | 100% | 100% | 25% | 0% | 33% | 92% | 92% | 100% | 45% |
| codes=5;spread=1;size=1024;fps=1 | 75% | 100% | 100% | 25% | 0% | 17% | 83% | 92% | 100% | 50% |
| codes=5;spread=1;size=1024;fps=2 | 75% | 100% | 100% | 25% | 0% | 25% | 100% | 92% | 100% | 50% |
| codes=10;spread=0;size=512;fps=1 | 67% | 92% | 92% | 33% | 8% | 33% | 83% | 92% | 100% | 40% |
| codes=10;spread=0;size=512;fps=2 | 75% | 100% | 92% | 42% | 17% | 42% | 100% | 92% | 100% | 40% |
| codes=10;spread=0;size=1024;fps=1 | 67% | 92% | 100% | 67% | 8% | 8% | 83% | 92% | 100% | 50% |
| codes=10;spread=0;size=1024;fps=2 | 75% | 92% | 100% | 67% | 17% | 50% | 92% | 92% | 92% | 50% |
| codes=10;spread=1;size=512;fps=1 | 75% | 100% | 100% | 33% | 8% | 33% | 83% | 92% | 100% | 50% |
| codes=10;spread=1;size=512;fps=2 | 83% | 100% | 100% | 50% | 0% | 33% | 100% | 92% | 100% | 50% |
| codes=10;spread=1;size=1024;fps=1 | 75% | 100% | 100% | 67% | 8% | 25% | 92% | 92% | 100% | 55% |
| codes=10;spread=1;size=1024;fps=2 | 92% | 100% | 100% | 83% | 17% | 33% | 100% | 100% | 92% | 55% |
| codes=20;spread=0;size=512;fps=1 | 58% | 100% | 100% | 75% | 8% | 58% | 83% | 83% | 100% | 60% |
| codes=20;spread=0;size=512;fps=2 | 67% | 100% | 100% | 83% | 17% | 67% | 100% | 83% | 100% | 60% |
| codes=20;spread=0;size=1024;fps=1 | 67% | 100% | 100% | 75% | 8% | 42% | 83% | 92% | 100% | 60% |
| codes=20;spread=0;size=1024;fps=2 | 75% | 92% | 100% | 92% | 8% | 58% | 100% | 92% | 100% | 60% |
| codes=20;spread=1;size=512;fps=1 | 75% | 100% | 100% | 75% | 8% | 50% | 83% | 92% | 100% | 65% |
| codes=20;spread=1;size=512;fps=2 | 83% | 100% | 100% | 92% | 17% | 58% | 100% | 100% | 100% | 65% |
| codes=20;spread=1;size=1024;fps=1 | 58% | 100% | 100% | 75% | 8% | 33% | 83% | 92% | 100% | 65% |
| codes=20;spread=1;size=1024;fps=2 | 67% | 100% | 100% | 92% | 8% | 42% | 100% | 100% | 100% | 65% |

## Frame-level match rate (sampled frames matching a keyframe of the source)

| setting | excerpt10 | excerpt30 | excerpt60 | vertical | pip25 | pip40 | lowres | caption | logo |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 60% | 58% | 40% | 1% | 0% | 1% | 39% | 31% | 43% |
| codes=5;spread=0;size=512;fps=2 | 52% | 43% | 36% | 2% | 0% | 1% | 36% | 27% | 40% |
| codes=5;spread=0;size=1024;fps=1 | 48% | 54% | 40% | 2% | 0% | 0% | 39% | 27% | 43% |
| codes=5;spread=0;size=1024;fps=2 | 41% | 42% | 36% | 2% | 0% | 1% | 36% | 23% | 40% |
| codes=5;spread=1;size=512;fps=1 | 65% | 57% | 44% | 1% | 0% | 1% | 46% | 29% | 42% |
| codes=5;spread=1;size=512;fps=2 | 65% | 55% | 45% | 2% | 0% | 1% | 46% | 28% | 42% |
| codes=5;spread=1;size=1024;fps=1 | 63% | 57% | 41% | 1% | 0% | 1% | 45% | 28% | 42% |
| codes=5;spread=1;size=1024;fps=2 | 64% | 55% | 43% | 1% | 0% | 1% | 45% | 27% | 42% |
| codes=10;spread=0;size=512;fps=1 | 68% | 67% | 55% | 7% | 0% | 2% | 50% | 49% | 54% |
| codes=10;spread=0;size=512;fps=2 | 71% | 66% | 55% | 7% | 0% | 2% | 51% | 48% | 55% |
| codes=10;spread=0;size=1024;fps=1 | 66% | 66% | 54% | 12% | 0% | 0% | 50% | 47% | 54% |
| codes=10;spread=0;size=1024;fps=2 | 70% | 65% | 55% | 12% | 0% | 1% | 51% | 46% | 54% |
| codes=10;spread=1;size=512;fps=1 | 78% | 69% | 61% | 7% | 0% | 2% | 57% | 46% | 52% |
| codes=10;spread=1;size=512;fps=2 | 77% | 68% | 60% | 8% | 0% | 2% | 58% | 45% | 54% |
| codes=10;spread=1;size=1024;fps=1 | 76% | 67% | 58% | 14% | 0% | 1% | 55% | 46% | 54% |
| codes=10;spread=1;size=1024;fps=2 | 75% | 68% | 58% | 13% | 0% | 1% | 57% | 46% | 54% |
| codes=20;spread=0;size=512;fps=1 | 79% | 72% | 66% | 29% | 1% | 7% | 62% | 61% | 62% |
| codes=20;spread=0;size=512;fps=2 | 79% | 73% | 66% | 29% | 1% | 7% | 62% | 61% | 63% |
| codes=20;spread=0;size=1024;fps=1 | 79% | 73% | 65% | 28% | 1% | 3% | 61% | 60% | 62% |
| codes=20;spread=0;size=1024;fps=2 | 79% | 73% | 65% | 29% | 1% | 5% | 62% | 60% | 63% |
| codes=20;spread=1;size=512;fps=1 | 83% | 76% | 72% | 27% | 1% | 5% | 66% | 58% | 63% |
| codes=20;spread=1;size=512;fps=2 | 83% | 76% | 72% | 28% | 1% | 6% | 67% | 57% | 63% |
| codes=20;spread=1;size=1024;fps=1 | 82% | 75% | 70% | 30% | 1% | 2% | 65% | 58% | 63% |
| codes=20;spread=1;size=1024;fps=2 | 81% | 75% | 70% | 31% | 1% | 3% | 66% | 57% | 63% |

## False matches

| setting | unrelated videos | unrelated frames | unrelated stills | wrong video in a manipulated clip |
| --- | --- | --- | --- | --- |
| codes=5;spread=0;size=512;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=5;spread=0;size=512;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=5;spread=0;size=1024;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=5;spread=0;size=1024;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=5;spread=1;size=512;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=5;spread=1;size=512;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=5;spread=1;size=1024;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=5;spread=1;size=1024;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=10;spread=0;size=512;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=10;spread=0;size=512;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=10;spread=0;size=1024;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=10;spread=0;size=1024;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=10;spread=1;size=512;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=10;spread=1;size=512;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=10;spread=1;size=1024;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=10;spread=1;size=1024;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=20;spread=0;size=512;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=20;spread=0;size=512;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=20;spread=0;size=1024;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=20;spread=0;size=1024;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=20;spread=1;size=512;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=20;spread=1;size=512;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |
| codes=20;spread=1;size=1024;fps=1 | 0 of 5 | 0 of 1864 | 0 of 25 | 0 |
| codes=20;spread=1;size=1024;fps=2 | 0 of 5 | 0 of 3728 | 0 of 25 | 0 |

## Code volume (originals of this split)

| codes | spread | N | keyframes / min | codes / min | codes per 90-min film |
| --- | --- | --- | --- | --- | --- |
| 5 | 0 | 1000 | 15.8 | 78.2 | 7,039 |
| 5 | 0 | 1 | 15.7 | 76.1 | 6,848 |
| 5 | 1 | 1000 | 15.9 | 78.4 | 7,057 |
| 10 | 0 | 1000 | 15.7 | 154.1 | 13,866 |
| 10 | 1 | 1000 | 15.8 | 154.9 | 13,937 |
| 20 | 0 | 1000 | 15.9 | 303.5 | 27,315 |
| 20 | 1 | 1000 | 16.0 | 305.1 | 27,457 |

## Timing (seconds per minute of video, one process)

- creator: 4.58 s
- verifier fps=1 size=512: 6.06 s
- verifier fps=1 size=1024: 10.07 s
- verifier fps=2 size=512: 11.4 s
- verifier fps=2 size=1024: 19.09 s
