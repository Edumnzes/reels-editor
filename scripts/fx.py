"""fx — text animations, animated backgrounds and borders for reels_lib projects.

Native re-creations of the *looks* of popular web animation components (React Bits catalogue:
SplitText, BlurText, TextType, DecryptedText, ShinyText, GradientText, RotatingText, CountUp,
Aurora/Soft Aurora, Dot Grid, Border Glow / Star Border). No React Bits code is used or shipped
(its MIT + Commons Clause licence forbids redistributing the components); these are our own
implementations for video frames. See references/reactbits.md for the mapping and when to use each.

All functions draw onto an RGBA overlay `ov` (1080x1920) at time `t`, like any motion function, and
take their sizes from the type scale (pass ts("...")) so proportion rules still hold.
"""
import math, random
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter
from reels_lib import T, paste, font, text_w, RR, clamp, eo, eback, prog, W, H, WHITE, YEL, stroke_for


def _chars(txt, size, weight, family):
    """x-centre of every character relative to the text's left edge (font advance widths)."""
    f = font(size, weight, family); out = []
    for i, ch in enumerate(txt):
        out.append(f.getlength(txt[:i]) + f.getlength(ch) / 2)
    return out, f.getlength(txt)


def split_text(ov, txt, cx, cy, size, t, t0, color=WHITE, weight=None, family="sans", stroke=None,
               stagger=.03, dur=.4, rise=None, a=1.0):
    """SplitText: characters rise + fade in one after another."""
    stroke = stroke_for(size) if stroke is None else stroke
    rise = size * .5 if rise is None else rise
    xs, total = _chars(txt, size, weight, family); left = cx - total / 2
    for i, ch in enumerate(txt):
        if ch == " ": continue
        p = prog(t, t0 + i * stagger, dur)
        if p <= 0: continue
        paste(ov, T(ch, size, color, weight, stroke, family=family), left + xs[i], cy + rise * (1 - eo(p)),
              a=a * clamp(p * 1.6))


def blur_text(ov, txt, cx, cy, size, t, t0, color=WHITE, weight=None, family="sans", stroke=None,
              stagger=.08, dur=.45, a=1.0):
    """BlurText: words go from blurred + transparent to sharp, in sequence."""
    stroke = stroke_for(size) if stroke is None else stroke
    words = txt.split(" "); gap = size * .3
    ws = [text_w(w, size, weight, family) for w in words]
    x = cx - (sum(ws) + gap * (len(ws) - 1)) / 2
    for i, (w, ww) in enumerate(zip(words, ws)):
        p = prog(t, t0 + i * stagger, dur)
        if p > 0:
            sp = T(w, size, color, weight, stroke, family=family)
            r = (1 - eo(p)) * size * .25
            if r > .5: sp = sp.filter(ImageFilter.GaussianBlur(r))
            paste(ov, sp, x + ww / 2, cy - size * .15 * (1 - eo(p)), a=a * eo(p))
        x += ww + gap


def text_type(ov, txt, cx, cy, size, t, t0, color=WHITE, weight=None, family="sans", cps=18, cursor=True, a=1.0):
    """TextType: typewriter with a blinking cursor, anchored to the final line so text doesn't jump."""
    if t < t0: return
    n = int((t - t0) * cps)
    total = text_w(txt, size, weight, family); left = cx - total / 2; shown = txt[:n]; sw = 0
    if shown.strip():
        sw = text_w(shown, size, weight, family)
        paste(ov, T(shown, size, color, weight, stroke_for(size), family=family), left + sw / 2, cy, a=a)
    if cursor and (n < len(txt) or int(t * 2) % 2 == 0):
        paste(ov, RR(max(3, size // 12), int(size * .9), 2, color), left + sw + size * .12, cy, a=a)


_GLYPHS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&$@*"
def decrypted_text(ov, txt, cx, cy, size, t, t0, color=WHITE, scramble=YEL, weight=None, family="sans",
                   reveal=.04, a=1.0):
    """DecryptedText: random glyphs settle into the real text left to right (tech / data vibe)."""
    if t < t0: return
    xs, total = _chars(txt, size, weight, family); left = cx - total / 2
    rnd = random.Random(int(t * 30))
    for i, ch in enumerate(txt):
        if ch == " ": continue
        done = t >= t0 + i * reveal + .25
        g = ch if done else rnd.choice(_GLYPHS)
        paste(ov, T(g, size, color if done else scramble, weight, stroke_for(size), family=family), left + xs[i], cy, a=a)


def shiny_text(ov, txt, cx, cy, size, t, color=(200, 200, 200, 255), shine=(255, 255, 255, 255), weight=None,
               family="sans", speed=.8, band=.18, a=1.0):
    """ShinyText: a light sweep travels across the letters (premium / metallic)."""
    base = T(txt, size, color, weight, stroke_for(size), shadow=True, family=family)
    hi = T(txt, size, shine, weight, stroke_for(size), sf=shine, shadow=True, family=family)
    wd = base.width; pos = ((t * speed) % 1.6 - .3) * wd
    band_a = np.clip(1 - np.abs(np.arange(wd, dtype=np.float32) - pos) / (band * wd), 0, 1)
    m = (np.array(hi.getchannel("A"), np.float32) * band_a[None, :]).astype(np.uint8)
    hi2 = hi.copy(); hi2.putalpha(Image.fromarray(m))
    comp = base.copy(); comp.alpha_composite(hi2)
    paste(ov, comp, cx, cy, a=a)


def gradient_text(ov, txt, cx, cy, size, t, colors=((255, 212, 0), (255, 138, 31), (34, 197, 94)), weight=None,
                  family="sans", speed=.25, a=1.0):
    """GradientText: animated multi-colour fill (one hero word, never body text)."""
    sp = T(txt, size, WHITE, weight, 0, shadow=False, family=family); wd, ht = sp.size
    x = (np.arange(wd, dtype=np.float32) / wd + t * speed) % 1.0
    cols = np.array(tuple(colors) + (colors[0],), np.float32); k = len(colors)
    seg = np.minimum((x * k).astype(int), k - 1); f = (x * k - seg)[:, None]
    row = cols[seg] * (1 - f) + cols[seg + 1] * f
    g = Image.fromarray(np.repeat(row[None], ht, 0).astype(np.uint8), "RGB").convert("RGBA")
    g.putalpha(sp.getchannel("A"))
    paste(ov, g, cx, cy, a=a)


def rotating_text(ov, words, cx, cy, size, t, t0, hold=1.1, color=YEL, weight=None, family="sans", pill_bg=None, a=1.0):
    """RotatingText: one slot cycles through words (e.g. SOLAR -> BATERIA -> MOBILIDADE); stops on the last."""
    if t < t0: return
    i = min(int((t - t0) // hold), len(words) - 1); k = (t - t0) - i * hold; w = words[i]
    last = i == len(words) - 1
    pin = eo(k / .3); pout = 0 if last or k < hold - .25 else eo((k - (hold - .25)) / .25)
    if pill_bg:
        paste(ov, RR(text_w(w, size, weight, family) + size, int(size * 1.6), int(size * .8), pill_bg), cx, cy, a=a)
    paste(ov, T(w, size, color, weight, 0 if pill_bg else stroke_for(size), family=family, shadow=not pill_bg),
          cx, cy + size * .6 * (1 - pin) - size * .6 * pout, a=a * pin * (1 - pout))


def count_up(ov, cx, cy, size, t, t0, value, unit="", dur=.9, color=YEL, unit_color=WHITE, decimals=0, a=1.0):
    """CountUp: number animates from 0 with ease-out; unit one scale step smaller on the same baseline."""
    if t < t0: return
    s = f"{value * eo(prog(t, t0, dur)):.{decimals}f}".replace(".", ",")
    us = max(20, int(size * .64)); nw = text_w(s, size)
    uw = text_w(unit, us, "ExtraBold") if unit else 0; gap = size * .15 if unit else 0
    x0 = cx - (nw + gap + uw) / 2
    paste(ov, T(s, size, color, stroke=stroke_for(size)), x0 + nw / 2, cy, a=a)
    if unit:
        paste(ov, T(unit, us, unit_color, "ExtraBold", stroke_for(us)), x0 + nw + gap + uw / 2, cy + (size - us) * .32, a=a)


# ---------------------------------------------------------------- backgrounds (title cards / interstitials)
def aurora(t, colors=((34, 197, 94), (255, 212, 0), (11, 17, 32)), alpha=.85, speed=.15):
    """Aurora / Soft Aurora: slow drifting colour blobs. Returns an RGBA layer (W x H); paste it first."""
    w, h = W // 10, H // 10
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    acc = np.zeros((h, w, 3), np.float32); wt = np.zeros((h, w, 1), np.float32)
    for i, c in enumerate(colors):
        ph = t * speed * (1 + i * .3) + i * 2.1
        bx = w * (.5 + .35 * math.sin(ph)); by = h * (.3 + .25 * i + .12 * math.cos(ph * 1.3))
        g = np.exp(-(((xx - bx) / (w * .45)) ** 2 + ((yy - by) / (h * .22)) ** 2))[..., None]
        acc += g * np.float32(c); wt += g
    img = (acc / np.maximum(wt, 1e-3)).clip(0, 255).astype(np.uint8)
    img = cv2.GaussianBlur(cv2.resize(img, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 25)
    lay = Image.fromarray(img, "RGB").convert("RGBA"); lay.putalpha(int(255 * alpha))
    return lay


def dot_grid(t, color=(255, 255, 255), spacing=48, radius=3, alpha=.18, drift=12):
    """Dot Grid: subtle moving dot pattern (tech / engineering backdrop). Returns an RGBA layer."""
    lay = Image.new("RGBA", (W, H)); d = ImageDraw.Draw(lay); off = (t * drift) % spacing
    for y in np.arange(-spacing + off, H + spacing, spacing):
        for x in np.arange(spacing / 2, W, spacing):
            d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=tuple(color) + (int(255 * alpha),))
    return lay


def border_glow(ov, cx, cy, w, h, r, t, color=YEL, width=3, a=1.0, speed=.8):
    """Border Glow / Star Border: a bright spot runs around a card outline over a soft glow.
    Draw it right after the card, with the card's exact w/h/r."""
    s = 2; lay = Image.new("RGBA", (w * s + 80, h * s + 80)); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = 40, 40, 40 + w * s, 40 + h * s
    d.rounded_rectangle((x0, y0, x1, y1), r * s, outline=tuple(color[:3]) + (110,), width=width * s)
    per = 2 * (w + h) * s; p = (t * speed % 1) * per; pts = []
    for k in np.linspace(-.06, .06, 24):
        q = (p + k * per) % per
        if q < w * s: pts.append((x0 + q, y0))
        elif q < (w + h) * s: pts.append((x1, y0 + q - w * s))
        elif q < (2 * w + h) * s: pts.append((x1 - (q - (w + h) * s), y1))
        else: pts.append((x0, y1 - (q - (2 * w + h) * s)))
    d.line(pts, fill=tuple(color[:3]) + (255,), width=width * s * 2)
    glow = lay.filter(ImageFilter.GaussianBlur(10)); glow.alpha_composite(lay)
    paste(ov, glow.resize((glow.width // s, glow.height // s), Image.LANCZOS), cx, cy, a=a)
