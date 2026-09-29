"""Worked example: Growatt RISE 261 @ Intersolar 2026 (52 s, two speakers + B-roll).

Copy this file next to your base_1440.mp4 / words.json / faces.json, rename it
(e.g. project.py) and rewrite the CONFIG + MOTIONS sections for the new video.
Run:  python project.py preview 1 5.7 19.3 22 31 38.5 --debug
      python project.py strip 5.2 6.2          (smoothness of a punch-in)
      python project.py check
      python project.py looks 16                (same frame in every colour grade)
      python project.py full reels_final.mp4
"""
import sys, math
from pathlib import Path
SKILL = Path.home() / ".claude" / "skills" / "reels-editor"
sys.path.insert(0, str(SKILL / "scripts"))
from reels_lib import *  # noqa: F401,F403  (Reel, T, RR, paste, pill, icon, easing, colours, bands)

# ============================================================ CONFIG
# Timeline of the CUT (not the raw file). Shots: 0-14.3 two-shot (host left speaks),
# 14.3-25 Igor close, 25-35.9 B-roll cabinet (no faces), 35.9-40.9 Igor, 40.9-42.4 host, 42.4-end two-shot.
# Conservative zoom (style-guide §3): slow drifts <= ~5 % per shot; punch-ins only as instant steps on cuts.
ZOOM = [
    (0.0, 14.05, 1.02, 1.07, eio),                                 # two-shot intro, slow push
    (14.1, 14.1, 1.04, 1.04, eo), (14.1, 35.85, 1.04, 1.10, eio),  # Igor close -> camera pans to the cabinet (one shot)
    (35.87, 35.87, 1.0, 1.0, eo), (35.87, 40.65, 1.0, 1.03, eio),  # Igor at the lens: no punch-ins
    (40.7, 40.7, 1.06, 1.06, eo), (40.7, 42.2, 1.06, 1.08, eio),   # host close (the re-frame is the change)
    (42.27, 42.27, 1.02, 1.02, eo), (42.27, 51.8, 1.02, 1.07, eio),
]
import json
# Every segment start of the cut, written by cut.py (cuts.json) — never type cut times by hand: a cut that is
# a few frames off makes the camera re-frame mid-shot. Shot changes (SCENES) are a subset of these.
CUTS = json.load(open("cuts.json")) if Path("cuts.json").exists() else []
SCENES = [14.1, 35.87, 40.7, 42.27]
RANGES = [(0, 14.1, "left"),   # one continuous two-shot: keep one framing (a 2 s switch to Igor would wobble)
           (14.1, 25.0, "big"), (25.0, 35.87, None),
          (35.87, 40.7, "big"), (40.7, 42.27, "big"), (42.27, 60, "right")]
BG = [(21.2, 29.6, .3, 0), (29.6, 35.95, .62, 1.0), (36.3, 40.85, .15, 0)]  # (t0, t1, dim, blur)
KEYWORDS = {"GROWATT", "INTERSOLAR", "2026", "NOVIDADES", "ARMAZENAMENTO", "RISE 261", "ALL-IN-ONE", "MERCADOS", "GESTÃO",
            "ENERGIA", "PONTA", "INVERSOR", "125", "261 kWh", "BATERIA", "MELHOR", "FEIRAS", "OBRIGADÃO", "IGOR", "COMÉRCIOS"}
FIX = {"comerços": "comércios", "brigadão": "obrigadão"}
# Direction (references/visual-references.md §2): trade show / B2B product -> hormozi captions, no grade.
STYLE, LOOK = "hormozi", "none"
FLASHES = []                                   # e.g. [14.3] for a flash cut on the shot change (+ "flash" SFX)
# One sound per visual event, under the voice. Files: ~/reels-sfx/<category>*.wav (user-supplied, licensed).
SFX = [(t, "whoosh", -8) for t in [14.3, 35.9, 42.36]] + [
    (0.1, "whoosh", -8), (0.4, "pop", -10), (18.7, "pop", -10), (21.2, "pop", -10), (23.44, "click", -12),
    (23.56, "click", -12), (23.68, "click", -12), (26.3, "whoosh", -10), (29.6, "riser", -12), (32.3, "pop", -10),
    (34.5, "ding", -10), (36.35, "pop", -10), (37.5, "pop", -10), (49.4, "pop", -8)]

# ============================================================ MOTIONS
def mg_hook(ov, t):                       # 0-4.5 s: curiosity hook in the top band
    if not 0 <= t < 4.5: return
    out = eo((t - 4.05) / .4) if t > 4.05 else 0; dy = -120 * out; a = 1 - out
    x = -500 + (W / 2 + 500) * eo(prog(t, .1, .45))
    pill(ov, x, 330 + dy, "INTERSOLAR 2026", ts("md"), YEL, BLACK, "sun", a=a)
    for i, (txt, col) in enumerate((("O QUE A GROWATT", WHITE), ("TROUXE DE NOVO?", YEL))):
        pp = prog(t, .4 + i * .12, .35)
        paste(ov, T(txt, ts("2xl"), col, stroke=stroke_for(ts("2xl"))), W / 2, 456 + i * 92 + dy, .6 + .4 * eback(pp), clamp(pp * 3) * a)

def mg_storage(ov, t):                    # "armazenamento"
    a = life(t, 18.7, 21.15, .3, .25)
    if a <= 0: return
    s = .7 + .3 * eback(prog(t, 18.7, .35))
    pill(ov, W / 2, 330, "ARMAZENAMENTO DE ENERGIA", ts("md"), NAVY, WHITE, "battery", s=s, a=a)

def mg_rise(ov, t):
    """Two layouts: while Igor's face is on screen (21.2-23.3) a compact title card sits in the free
    band below his face; when the camera turns to the cabinet (B-roll) the full explainer card takes over."""
    a1 = life(t, 21.2, 23.4, .3, .2)
    if a1 > 0:
        cy = slot(21.2, 23.4, 220, prefer=960); s = .8 + .2 * eback(prog(t, 21.2, .4))
        paste(ov, RR(640, 220, 44, NAVY, (255, 255, 255, 50), 2), W / 2, cy, s, a1)
        paste(ov, T("NOVIDADE GROWATT", ts("xs"), GRAY, "Bold", shadow=False), W / 2, cy - 62, s, a1)
        paste(ov, T("RISE 261", ts("3xl"), WHITE, shadow=False), W / 2, cy + 8, s, a1)
        uw = int(360 * eo(prog(t, 21.5, .4)))
        if uw > 4: paste(ov, RR(uw, 10, 5, YEL), W / 2, cy + 80, s, a1)
    a = life(t, 23.35, 26.15, .3, .25)
    if a <= 0: return
    sc = .85 + .15 * eback(prog(t, 23.35, .4)); top = slot(23.35, 26.15, 640, prefer=640) - 320
    paste(ov, RR(920, 640, 48, NAVY, (255, 255, 255, 50), 2), W / 2, top + 320, sc, a)
    paste(ov, T("RISE 261", ts("3xl"), WHITE, shadow=False), W / 2, top + 96, sc, a)
    paste(ov, T("SOLUÇÃO ALL-IN-ONE", ts("sm"), GRAY, "Bold", shadow=False), W / 2, top + 176, sc, a)
    for i, (ic, lb) in enumerate((("inverter", "INVERSOR"), ("battery", "BATERIAS"), ("chart", "GESTÃO"))):
        pp = prog(t, 23.5 + i * .12, .35)
        if pp <= 0: continue
        x = W / 2 + (i - 1) * 288; y = top + 360; s2 = sc * (.5 + .5 * eback(pp))
        paste(ov, RR(264, 200, 32, (255, 255, 255, 22), (255, 212, 0, 160), 2), x, y, s2, a)
        paste(ov, icon(ic, 96, YEL), x, y - 24, s2, a)
        paste(ov, T(lb, 30, WHITE, "ExtraBold", shadow=False), x, y + 56, s2, a)
    pp = prog(t, 24.2, .35)
    if pp > 0: paste(ov, T("TUDO EM UM SÓ GABINETE", ts("lg"), YEL, shadow=False), W / 2, top + 552 + 24 * (1 - eo(pp)), sc, a * eo(pp))

def mg_market(ov, t):                     # "grandes comércios como mercados"
    a = life(t, 26.3, 29.55, .3, .25)
    if a <= 0: return
    dx = 700 * (1 - eo(prog(t, 26.3, .45))); cy = 600
    paste(ov, RR(920, 296, 48, NAVY, (255, 255, 255, 50), 2), W / 2 + dx, cy, a=a)
    paste(ov, RR(200, 200, 40, (255, 212, 0, 40)), 232 + dx, cy, a=a)
    paste(ov, icon("cart", 136, YEL), 232 + dx, cy, .6 + .4 * eback(prog(t, 26.5, .4)), a)
    paste(ov, T("IDEAL PARA", ts("sm"), GRAY, "Bold", shadow=False), 368 + dx, cy - 80, a=a, ax=0)
    paste(ov, T("SUPERMERCADOS", ts("lg"), YEL, shadow=False), 360 + dx, cy - 8, a=a, ax=0)
    paste(ov, T("E GRANDES COMÉRCIOS", ts("md"), WHITE, "ExtraBold", shadow=False), 364 + dx, cy + 64, a=a * eo(prog(t, 27.3, .3)), ax=0)

DEM = [.42, .4, .4, .4, .42, .48, .6, .75, .85, .88, .9, .92, .92, .9, .9, .9, .9, .92, .95, .96, .94, .8, .6, .48]
PEAK = (18, 19, 20)
def mg_peak(ov, t):                       # explainer interstitial over the B-roll
    a = life(t, 29.6, 35.95, .35, .25)
    if a <= 0: return
    paste(ov, T("FUGINDO DO", ts("xl"), WHITE), W / 2, 336, .7 + .3 * eback(prog(t, 29.65, .35)), a)
    paste(ov, T("HORÁRIO DE PONTA", ts("2xl"), YEL), W / 2, 424, .7 + .3 * eback(prog(t, 29.77, .35)), a)
    X0, X1, Y0, Y1 = 112, 968, 568, 960; bw = (X1 - X0) / 24; d = ImageDraw.Draw(ov)
    bp = eo(prog(t, 30.6, .35))
    if bp > 0:
        paste(ov, RR(int(bw * 3 + 12), Y1 - Y0 + 16, 14, (239, 68, 68, int(70 * bp * a))), X0 + bw * 19.5, (Y0 + Y1) / 2 - 8)
        paste(ov, T("PONTA", ts("sm"), RED, shadow=False), X0 + bw * 19.5, Y0 - 40, .6 + .4 * eback(prog(t, 30.6, .35)), a * bp)
    paste(ov, T("CONSUMO DA REDE AO LONGO DO DIA", ts("xs"), GRAY, "Bold", shadow=False), X0 - 24, Y0 - 40, a=a * clamp(prog(t, 30.0, .3)), ax=0)
    swap = eio(prog(t, 32.3, .9))
    for h in range(24):
        hh = (Y1 - Y0) * DEM[h] * eo(prog(t, 29.9 + h * .025, .5)); x = X0 + h * bw + 4
        if h in PEAK:
            grid = hh * (1 - swap * .92)
            d.rectangle((x, Y1 - grid, x + bw - 8, Y1), fill=(239, 68, 68, int(255 * a)))
            if swap > 0: d.rectangle((x, Y1 - hh, x + bw - 8, Y1 - grid), fill=(255, 212, 0, int(255 * a)))
        else:
            d.rectangle((x, Y1 - hh, x + bw - 8, Y1), fill=(255, 255, 255, int(200 * a)))
    d.rectangle((X0, Y1 + 2, X1, Y1 + 6), fill=(255, 255, 255, int(160 * a)))
    for h, lb in ((0, "0h"), (6, "6h"), (12, "12h"), (18, "18h"), (21, "21h")):
        paste(ov, T(lb, 26, GRAY, "Bold", shadow=False), X0 + h * bw, Y1 + 32, a=a * clamp(prog(t, 30.2, .3)))
    pb = prog(t, 32.3, .4)
    if pb > 0: pill(ov, 300, 1056, "BATERIA ASSUME", ts("sm"), YEL, BLACK, "battery", s=.5 + .5 * eback(pb), a=a)
    pc = prog(t, 34.5, .35)
    if pc > 0: pill(ov, 776, 1056, "CONTA MENOR", ts("sm"), GRN, WHITE, "check", s=.5 + .5 * eback(pc), a=a)

def mg_specs(ov, t):                      # animated counters above the speaker (close-up face fills the middle)
    a = life(t, 36.3, 40.85, .3, .25)
    if a <= 0: return
    cy = slot(36.3, 40.85, 232, prefer=420)  # close-up face fills the middle -> usually lands in the top band
    for i, (t0, val, unit, lb, ic) in enumerate(((36.35, 125, "kW", "INVERSOR", "inverter"), (37.5, 261, "kWh", "DE BATERIA", "battery"))):
        p = prog(t, t0, .4)
        if p <= 0: continue
        x = 304 + i * 472; dy = 72 * (1 - eo(p)); al = a * eo(p)
        paste(ov, RR(440, 232, 40, NAVY, (255, 212, 0, 200), 3), x, cy + dy, a=al)
        n = str(int(round(val * eo(prog(t, t0, .7)))))
        nw, uw = text_w(n, 96), text_w(unit, 44); x0 = x - (nw + 12 + uw) / 2
        paste(ov, T(n, 96, YEL, shadow=False), x0 + nw / 2, cy - 28 + dy, a=al)
        paste(ov, T(unit, 44, WHITE, "ExtraBold", shadow=False), x0 + nw + 12 + uw / 2, cy - 12 + dy, a=al)
        lw_ = text_w(lb, 30, "Bold"); lx = x - (44 + 12 + lw_) / 2
        paste(ov, icon(ic, 44, GRAY), lx + 22, cy + 64 + dy, a=al)
        paste(ov, T(lb, 30, GRAY, "Bold", shadow=False), lx + 56 + lw_ / 2, cy + 64 + dy, a=al)
        if ic == "battery":
            fw = int(360 * eo(prog(t, t0 + .1, 1.0)))
            if fw > 4: paste(ov, RR(fw, 10, 5, GRN), x - 180, cy + 100 + dy, a=a, ax=0)

def mg_cta(ov, t):                        # last 3 s
    if t < 48.9: return
    a = eo(prog(t, 48.9, .3))
    cy = slot(48.9, 51.9, 230, prefer=400)
    paste(ov, T("GOSTOU DA NOVIDADE?", ts("lg"), WHITE, stroke=stroke_for(ts("lg"))), W / 2, cy - 60, .7 + .3 * eback(prog(t, 48.9, .35)), a)
    p = prog(t, 49.4, .4)
    if p > 0:
        pulse = 1 + .04 * math.sin(max(0, t - 49.8) * 7) * (t > 49.8)
        pill(ov, W / 2, cy + 60, "SIGA PARA MAIS", ts("md"), YEL, BLACK, "plus", s=(.5 + .5 * eback(p)) * pulse, a=a)

if __name__ == "__main__":
    Reel("base_1440.mp4", "words.json", "faces.json", ZOOM, SCENES, RANGES,
         [mg_hook, mg_storage, mg_rise, mg_market, mg_peak, mg_specs, mg_cta], BG,
         KEYWORDS, FIX, join_next={"RISE"}, join_prev={"kWh"}, cuts=CUTS, jumpcuts="auto",
         caption_style=STYLE, look=LOOK, flashes=FLASHES, sfx=SFX).cli()
