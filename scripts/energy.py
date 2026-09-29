"""Find real pauses from audio energy (whisper word timings hide pauses inside long "words").

Usage:
  python energy.py <video_or_audio>                     -> list of low-energy runs >= 0.3 s (whole file)
  python energy.py <video_or_audio> 40.0-44.5 72-73.3   -> 50 ms energy dump (dB) for those ranges

Trade-show / street noise makes ffmpeg silencedetect useless; a relative threshold
(median - 6 dB) on 100 ms windows works much better. Use the 50 ms dump to place cuts
exactly inside the dip between words, and to spot drawn-out syllables (long flat plateaus).
"""
import subprocess, sys, os, tempfile, wave
import numpy as np, imageio_ffmpeg

src = sys.argv[1]
wav = os.path.join(tempfile.gettempdir(), "reels_en_16k.wav")
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-loglevel", "error", "-y", "-i", src, "-vn", "-ac", "1", "-ar", "16000", wav], check=True)
w = wave.open(wav); a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(float)

def db_at(t, h):
    i = int(t * 16000); seg = a[i:i + int(16000 * h)]
    return 20 * np.log10(np.sqrt(np.mean(seg ** 2)) + 1) if len(seg) else 0

if len(sys.argv) == 2:
    ts = np.arange(0, len(a) / 16000 - .1, .1)
    db = np.array([db_at(t, .1) for t in ts])
    thr = np.percentile(db, 50) - 6
    print(f"p10 {np.percentile(db,10):.1f}  p50 {np.percentile(db,50):.1f}  p90 {np.percentile(db,90):.1f}  thr {thr:.1f}")
    runs, st = [], None
    for i, v in enumerate(db):
        if v < thr and st is None: st = i
        if v >= thr and st is not None:
            if i - st >= 3: runs.append((round(st / 10, 1), round(i / 10, 1)))
            st = None
    print("low-energy runs:", runs)
else:
    for r in sys.argv[2:]:
        t0, t1 = map(float, r.split("-"))
        print(" ".join(f"{t:.2f}:{int(db_at(t, .05))}" for t in np.arange(t0, t1, .05)), "\n")
