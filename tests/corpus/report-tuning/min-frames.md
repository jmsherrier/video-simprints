# Tuning: video-level match rate against min_frames (M)

Tuning split only, all manipulations but stills, mean over manipulations. No setting had a false match (unrelated video, or a wrong video in a manipulated clip) at any M from 1 to 6. N = 1000 means stop codes off.

```
codes=10;spread=0;stop_after=3;size=512 fps=1 M1:80.2 M2:74.1 M3:69.1 M4:67.9 M5:64.2 M6:63.0
codes=10;spread=0;stop_after=3;size=512 fps=2 M1:81.5 M2:79.0 M3:75.3 M4:72.8 M5:70.4 M6:70.4
codes=10;spread=0;stop_after=3;size=1024 fps=1 M1:80.2 M2:75.3 M3:71.6 M4:67.9 M5:64.2 M6:61.7
codes=10;spread=0;stop_after=3;size=1024 fps=2 M1:82.7 M2:80.2 M3:75.3 M4:74.1 M5:74.1 M6:70.4
codes=10;spread=0;stop_after=1000;size=512 fps=1 M1:81.5 M2:75.3 M3:70.4 M4:69.1 M5:66.7 M6:64.2
codes=10;spread=0;stop_after=1000;size=512 fps=2 M1:82.7 M2:80.2 M3:76.5 M4:74.1 M5:71.6 M6:71.6
codes=10;spread=0;stop_after=1000;size=1024 fps=1 M1:82.7 M2:77.8 M3:74.1 M4:70.4 M5:66.7 M6:64.2
codes=10;spread=0;stop_after=1000;size=1024 fps=2 M1:85.2 M2:82.7 M3:77.8 M4:76.5 M5:76.5 M6:72.8
codes=10;spread=1;stop_after=3;size=512 fps=1 M1:77.8 M2:72.8 M3:66.7 M4:66.7 M5:65.4 M6:63.0
codes=10;spread=1;stop_after=3;size=512 fps=2 M1:77.8 M2:77.8 M3:74.1 M4:70.4 M5:69.1 M6:66.7
codes=10;spread=1;stop_after=3;size=1024 fps=1 M1:81.5 M2:74.1 M3:70.4 M4:67.9 M5:66.7 M6:64.2
codes=10;spread=1;stop_after=3;size=1024 fps=2 M1:81.5 M2:79.0 M3:75.3 M4:72.8 M5:71.6 M6:70.4
codes=10;spread=1;stop_after=1000;size=512 fps=1 M1:81.5 M2:76.5 M3:69.1 M4:69.1 M5:67.9 M6:65.4
codes=10;spread=1;stop_after=1000;size=512 fps=2 M1:81.5 M2:81.5 M3:77.8 M4:74.1 M5:72.8 M6:70.4
codes=10;spread=1;stop_after=1000;size=1024 fps=1 M1:84.0 M2:76.5 M3:72.8 M4:70.4 M5:69.1 M6:66.7
codes=10;spread=1;stop_after=1000;size=1024 fps=2 M1:84.0 M2:81.5 M3:77.8 M4:75.3 M5:74.1 M6:72.8
codes=20;spread=0;stop_after=3;size=512 fps=1 M1:84.0 M2:82.7 M3:80.2 M4:76.5 M5:72.8 M6:71.6
codes=20;spread=0;stop_after=3;size=512 fps=2 M1:85.2 M2:84.0 M3:81.5 M4:80.2 M5:80.2 M6:79.0
codes=20;spread=0;stop_after=3;size=1024 fps=1 M1:84.0 M2:81.5 M3:81.5 M4:75.3 M5:72.8 M6:71.6
codes=20;spread=0;stop_after=3;size=1024 fps=2 M1:84.0 M2:84.0 M3:81.5 M4:81.5 M5:80.2 M6:80.2
codes=20;spread=0;stop_after=1000;size=512 fps=1 M1:86.4 M2:84.0 M3:81.5 M4:76.5 M5:72.8 M6:71.6
codes=20;spread=0;stop_after=1000;size=512 fps=2 M1:87.7 M2:85.2 M3:82.7 M4:81.5 M5:81.5 M6:80.2
codes=20;spread=0;stop_after=1000;size=1024 fps=1 M1:86.4 M2:84.0 M3:84.0 M4:76.5 M5:74.1 M6:72.8
codes=20;spread=0;stop_after=1000;size=1024 fps=2 M1:86.4 M2:86.4 M3:84.0 M4:84.0 M5:82.7 M6:82.7
codes=20;spread=1;stop_after=3;size=512 fps=1 M1:81.5 M2:79.0 M3:76.5 M4:71.6 M5:70.4 M6:67.9
codes=20;spread=1;stop_after=3;size=512 fps=2 M1:81.5 M2:81.5 M3:79.0 M4:77.8 M5:76.5 M6:75.3
codes=20;spread=1;stop_after=3;size=1024 fps=1 M1:84.0 M2:81.5 M3:80.2 M4:75.3 M5:72.8 M6:71.6
codes=20;spread=1;stop_after=3;size=1024 fps=2 M1:84.0 M2:84.0 M3:81.5 M4:81.5 M5:79.0 M6:79.0
codes=20;spread=1;stop_after=1000;size=512 fps=1 M1:85.2 M2:81.5 M3:79.0 M4:74.1 M5:72.8 M6:70.4
codes=20;spread=1;stop_after=1000;size=512 fps=2 M1:85.2 M2:84.0 M3:81.5 M4:80.2 M5:79.0 M6:77.8
codes=20;spread=1;stop_after=1000;size=1024 fps=1 M1:85.2 M2:82.7 M3:81.5 M4:76.5 M5:74.1 M6:72.8
codes=20;spread=1;stop_after=1000;size=1024 fps=2 M1:85.2 M2:85.2 M3:82.7 M4:82.7 M5:80.2 M6:80.2
```
