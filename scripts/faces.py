"""Face track at 10 fps with OpenCV YuNet (OpenCV 5 dropped Haar cascades).

Usage: python faces.py <video> <out_faces.json> [--sheet sheet.jpg]
Output: [{"t": 1.2, "f": [[x, y, w, h, score], ...]}, ...] in a 360x640 analysis frame
(multiply by src_width/360 to map to the source). Prints one sample per second so you can
tell which face is who (left/right, size) per shot. --sheet also writes a contact sheet
(1 frame / 2 s with timestamps) to map shots, B-roll and speakers visually.
"""
import argparse, json, subprocess
from pathlib import Path
import numpy as np, cv2, imageio_ffmpeg

ap = argparse.ArgumentParser(); ap.add_argument("src"); ap.add_argument("out"); ap.add_argument("--sheet")
a = ap.parse_args()
FF = imageio_ffmpeg.get_ffmpeg_exe()
W, H = 360, 640
model = str(Path(__file__).resolve().parent.parent / "assets" / "yunet.onnx")
p = subprocess.Popen([FF, "-loglevel", "error", "-i", a.src, "-vf", f"fps=10,scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
det = cv2.FaceDetectorYN.create(model, "", (W, H), 0.6)
out, i = [], 0
while True:
    b = p.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    _, r = det.detect(np.frombuffer(b, np.uint8).reshape(H, W, 3))
    out.append({"t": round(i / 10, 1), "f": [] if r is None else [[round(float(v), 1) for v in x[:4]] + [round(float(x[14]), 2)] for x in r]})
    i += 1
json.dump(out, open(a.out, "w"), indent=0)
for fr in out[::10]: print(fr["t"], [[int(v) for v in x[:4]] for x in fr["f"]])
if a.sheet:
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", a.src, "-vf", "fps=1/2,scale=216:384,tile=7x5", "-frames:v", "1", a.sheet])
