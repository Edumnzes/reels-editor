"""Turn editorial phrase picks into a tight keep.json, removing pauses inside each phrase.

Usage: python plan_cut.py <raw_video> <phrases.json> <keep.json> [--pause 0.3] [--pad 0.06] [--hold-max 0.7]
phrases.json: [[start, end], ...] in RAW seconds — one entry per phrase you decided to keep
(take start = first word "s" - ~0.1, end = last word "e" + ~0.15 from words_raw.json).
Functional pauses (manual 4.1: emphasis, humour, emotion, understanding) are KEPT, not cut:
    [start, end, {"hold": [t, ...], "why": "ênfase antes do número"}]
every pause that contains a `hold` time stays in (trimmed to --hold-max s if longer).
Each kept pause is printed so it can go into decisoes.json with its reason.
Inside every phrase, low-energy runs >= --pause s (relative threshold, 50 ms windows, same logic
as energy.py) are cut out, keeping --pad s of air on each side so words aren't clipped.
Prints the resulting segments and total duration. Always verify by re-transcribing the cut.
"""
import argparse, json, subprocess, os, tempfile, wave
import numpy as np, imageio_ffmpeg

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("phrases"); ap.add_argument("out")
ap.add_argument("--pause", type=float, default=.3); ap.add_argument("--pad", type=float, default=.06)
ap.add_argument("--hold-max", type=float, default=.7)
a = ap.parse_args()
wav = os.path.join(tempfile.gettempdir(), "reels_pc_16k.wav")
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-y", "-i", a.src, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
w = wave.open(wav); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)
hop = 800  # 50 ms
db = np.array([20 * np.log10(np.sqrt(np.mean(x[i:i + hop] ** 2)) + 1) for i in range(0, len(x) - hop, hop)])
thr = np.percentile(db, 50) - 6
keep, held = [], []
for ph in json.load(open(a.phrases, encoding="utf-8")):
    s, e = ph[0], ph[1]; opt = ph[2] if len(ph) > 2 else {}
    holds = opt.get("hold", [])
    i0, i1 = int(s / .05), int(e / .05)
    cur = s; run = None
    for i in range(i0, min(i1, len(db))):
        low = db[i] < thr
        if low and run is None: run = i
        if (not low or i == i1 - 1) and run is not None:
            r0, r1 = run * .05, i * .05
            if r1 - r0 >= a.pause and r0 > s + .05 and r1 < e - .05:
                if any(r0 - .1 <= h <= r1 + .1 for h in holds):          # functional pause: keep it
                    if r1 - r0 > a.hold_max:                            # ...but not longer than needed
                        keep.append([round(cur, 2), round(r0 + a.hold_max, 2)]); cur = r1 - a.pad
                    held.append((round(r0, 2), round(min(r1 - r0, a.hold_max), 2), opt.get("why", "")))
                else:
                    keep.append([round(cur, 2), round(r0 + a.pad, 2)]); cur = r1 - a.pad
            run = None
    keep.append([round(cur, 2), round(e, 2)])
keep = [k for k in keep if k[1] - k[0] > .12]
json.dump(keep, open(a.out, "w"))
for k in keep: print(k)
for r0, d, why in held: print(f"pausa mantida em {r0}s ({d}s){' - ' + why if why else ''}")
print("segments", len(keep), "total", round(sum(e - s for s, e in keep), 2), "s")
