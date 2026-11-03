# Third-party notices

video-simprints is Apache-2.0 and does not include the packages or programs below.
Versions are the pins in [`pyproject.toml`](pyproject.toml).

## Runtime

| package | version | licence | link |
| --- | --- | --- | --- |
| image-simprints | 0.3.0 (git tag `v0.3.0`) | Apache-2.0 | [github.com/jmsherrier/image-simprints](https://github.com/jmsherrier/image-simprints) |
| NumPy | 2.5.1 | BSD-3-Clause AND 0BSD AND MIT AND Zlib AND CC0-1.0 | [github.com/numpy/numpy](https://github.com/numpy/numpy) |
| opencv-python-headless | 5.0.0.93 | Apache-2.0 | [github.com/opencv/opencv-python](https://github.com/opencv/opencv-python) |
| Pillow | 12.3.0 | MIT-CMU | [github.com/python-pillow/Pillow](https://github.com/python-pillow/Pillow) |

The wheels bundle other libraries under their own licences; image-simprints'
[THIRD-PARTY-NOTICES](https://github.com/jmsherrier/image-simprints/blob/v0.3.0/THIRD-PARTY-NOTICES.md)
lists them. One matters here: **the opencv-python-headless wheel ships an FFmpeg
library** (`opencv_videoio_ffmpeg` on Windows, `libavcodec` and friends under
`opencv_python_headless.libs` on Linux) for `cv2.VideoCapture`. video-simprints
never calls it: every video is decoded by the system `ffmpeg`. The library is
still installed, so a licence review of bundled decoders should know it is there.

## FFmpeg (external, not bundled)

Decoding runs the system `ffmpeg` (and test mode `ffprobe`) as a subprocess.
Nothing of FFmpeg is distributed with this package. Its licence is LGPL-2.1 or
GPL, depending on how the installed build was configured; codec patents (H.264,
HEVC) concern whoever installs and runs it. Reports record the version used.
Test mode also encodes test clips with `libx264` (GPL) from that installation.

## Tests only

| package | version | licence | link |
| --- | --- | --- | --- |
| pytest | 9.2.0 | MIT | [github.com/pytest-dev/pytest](https://github.com/pytest-dev/pytest) |

## Test corpus

The videos are not in this repository and are not redistributed.
[`tests/corpus/manifest.csv`](tests/corpus/manifest.csv) lists each with its
URL, licence, credit and SHA-256; `fetch-corpus` downloads them.

- **Blender open movies**, CC BY: *Sintel* (CC BY 3.0, © Blender Foundation,
  durian.blender.org), *Big Buck Bunny* (CC BY 3.0, © 2008 Blender Foundation,
  www.bigbuckbunny.org), *Tears of Steel* (CC BY 3.0, (CC) Blender Foundation,
  mango.blender.org) and *Elephants Dream* (CC BY 2.5, © 2006 Blender Foundation /
  Netherlands Media Art Institute, www.elephantsdream.org). Downloaded from
  download.blender.org.
- **NASA** videos on Wikimedia Commons, public domain (works of the US
  government): eleven clips from NASA Johnson, NASA Kennedy, NASA TV, NASA's
  Goddard Space Flight Center and its Scientific Visualization Studio.
- **Djawa Baharoe** (1940s newsreel, Nippon Eigasha di Djawa), public domain, on
  Wikimedia Commons.

## Patent

SIFT's US patent ([US 6,711,293](https://patents.google.com/patent/US6711293B1/en)) expired in March 2020.
