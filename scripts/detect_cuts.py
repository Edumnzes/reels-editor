"""Find the real cut points in a rendered cut by frame difference (sanity check for cuts.json).

Usage: python detect_cuts.py <cut_video> [--thr 18]
Prints times where consecutive frames differ strongly (jump cuts, shot changes). Compare with cuts.json:
every listed cut should appear here within ~1 frame (camera pans can add extra peaks — that's fine).
"""
import argparse, subprocess
import numpy as np, imageio_ffmpeg
ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("--thr", type=float, default=18)
a = ap.parse_args()
w, h = 90, 160
p = subprocess.Popen([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-i", a.src, "-vf", f"scale={w}:{h}",
                      "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
prev, i, diffs = None, 0, []
while True:
    b = p.stdout.read(w * h)
    if len(b) < w * h: break
    f = np.frombuffer(b, np.uint8).astype(np.float32)
    if prev is not None: diffs.append((i / 30, float(np.abs(f - prev).mean())))
    prev, i = f, i + 1
d = np.array([x[1] for x in diffs]); base = np.median(d)
cuts = [t for (t, v), k in zip(diffs, range(len(diffs))) if v > max(a.thr, base * 4)
        and v >= max(d[max(0, k - 3):k + 4])]
print("cuts:", [round(c, 2) for c in cuts])
