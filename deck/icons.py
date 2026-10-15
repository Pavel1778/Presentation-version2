"""Vector-style icon library.

Icons are drawn with Pillow at 4x supersampling on a transparent canvas and
down-scaled, so they stay crisp at any slide size. Each icon is a single flat
accent colour (the brief forbids gradients, shadows and drop effects), and the
geometry is deliberately simple so it reads cleanly on a projector.
"""
import os
from functools import lru_cache
from PIL import Image, ImageDraw

SS = 4          # supersample factor
BASE = 512      # nominal icon canvas (px)

CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "out", "_icons")


def _new():
    img = Image.new("RGBA", (BASE * SS, BASE * SS), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _finish(img, name, color):
    img = img.resize((BASE, BASE), Image.LANCZOS)
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{name}_{color}.png")
    img.save(path)
    return path


# --- primitive helpers (all coordinates in 0..1 of the canvas) --------------
def _S(v):
    return int(round(v * BASE * SS))


def _rr(d, box, r, fill):
    d.rounded_rectangle([_S(box[0]), _S(box[1]), _S(box[2]), _S(box[3])],
                        radius=_S(r), fill=fill)


def _el(d, box, fill):
    d.ellipse([_S(box[0]), _S(box[1]), _S(box[2]), _S(box[3])], fill=fill)


def _poly(d, pts, fill):
    d.polygon([(_S(x), _S(y)) for x, y in pts], fill=fill)


def _line(d, pts, fill, w):
    d.line([(_S(x), _S(y)) for x, y in pts], fill=fill, width=_S(w),
           joint="curve")


# --- icon drawings ----------------------------------------------------------
def _headset(d, c):
    _rr(d, (0.12, 0.30, 0.30, 0.62), 0.06, c)       # left cup
    _rr(d, (0.70, 0.30, 0.88, 0.62), 0.06, c)       # right cup
    d.arc([_S(0.14), _S(0.14), _S(0.86), _S(0.62)], 180, 360, fill=c,
          width=_S(0.06))
    _rr(d, (0.44, 0.62, 0.56, 0.80), 0.03, c)       # mic stem
    _el(d, (0.36, 0.74, 0.64, 0.90), c)             # mic tip


def _cart(d, c):
    _line(d, [(0.10, 0.20), (0.24, 0.20), (0.36, 0.62), (0.82, 0.62)],
          c, 0.055)
    _line(d, [(0.30, 0.34), (0.86, 0.34), (0.82, 0.62)], c, 0.05)
    _el(d, (0.38, 0.72, 0.52, 0.86), c)
    _el(d, (0.70, 0.72, 0.84, 0.86), c)


def _car(d, c):
    _rr(d, (0.10, 0.44, 0.90, 0.66), 0.08, c)
    _poly(d, [(0.24, 0.44), (0.36, 0.28), (0.66, 0.28), (0.78, 0.44)], c)
    _el(d, (0.20, 0.60, 0.34, 0.74), c)
    _el(d, (0.66, 0.60, 0.80, 0.74), c)


def _calc(d, c):
    _rr(d, (0.22, 0.12, 0.78, 0.88), 0.06, c)
    _rr(d, (0.30, 0.20, 0.70, 0.38), 0.02, (255, 255, 255, 255))
    for r in range(3):
        for col in range(3):
            x = 0.31 + col * 0.145
            y = 0.45 + r * 0.13
            _el(d, (x, y, x + 0.09, y + 0.09), (255, 255, 255, 255))


def _gear(d, c):
    import math
    cx, cy, ro, ri = 0.5, 0.5, 0.40, 0.30
    teeth = 8
    pts = []
    for i in range(teeth * 2):
        ang = math.pi * i / teeth
        r = ro if i % 2 == 0 else ri
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    _poly(d, pts, c)
    _el(d, (0.40, 0.40, 0.60, 0.60), (255, 255, 255, 255))


def _book(d, c):
    _poly(d, [(0.12, 0.22), (0.48, 0.30), (0.48, 0.80), (0.12, 0.72)], c)
    _poly(d, [(0.52, 0.30), (0.88, 0.22), (0.88, 0.72), (0.52, 0.80)], c)
    _line(d, [(0.50, 0.30), (0.50, 0.80)], (255, 255, 255, 255), 0.02)


def _speech(d, c):
    _rr(d, (0.12, 0.18, 0.72, 0.60), 0.08, c)
    _poly(d, [(0.26, 0.58), (0.42, 0.58), (0.30, 0.78)], c)
    _rr(d, (0.50, 0.44, 0.90, 0.78), 0.06, c)


def _hands(d, c):
    _el(d, (0.30, 0.14, 0.70, 0.44), c)
    _poly(d, [(0.20, 0.86), (0.34, 0.50), (0.66, 0.50), (0.80, 0.86)], c)


def _palette(d, c):
    _el(d, (0.12, 0.16, 0.88, 0.86), c)
    for (x, y), col in [((0.34, 0.36), (255, 255, 255, 255)),
                        ((0.52, 0.30), (255, 255, 255, 255)),
                        ((0.64, 0.50), (255, 255, 255, 255)),
                        ((0.34, 0.58), (255, 255, 255, 255))]:
        _el(d, (x, y, x + 0.10, y + 0.10), col)


def _stetho(d, c):
    d.arc([_S(0.20), _S(0.16), _S(0.62), _S(0.60)], 200, 360, fill=c,
          width=_S(0.06))
    _line(d, [(0.20, 0.38), (0.20, 0.56)], c, 0.06)
    _line(d, [(0.62, 0.30), (0.62, 0.56)], c, 0.06)
    _line(d, [(0.20, 0.56), (0.50, 0.74), (0.72, 0.60)], c, 0.06)
    _el(d, (0.66, 0.54, 0.86, 0.74), c)


def _teacher(d, c):
    _el(d, (0.40, 0.12, 0.60, 0.32), c)
    _poly(d, [(0.28, 0.86), (0.36, 0.40), (0.64, 0.40), (0.72, 0.86)], c)
    _rr(d, (0.10, 0.30, 0.30, 0.66), 0.02, c)
    _line(d, [(0.14, 0.36), (0.26, 0.36)], (255, 255, 255, 255), 0.02)
    _line(d, [(0.14, 0.44), (0.26, 0.44)], (255, 255, 255, 255), 0.02)


def _brain(d, c):
    _el(d, (0.16, 0.20, 0.84, 0.84), c)
    for (a, b) in [((0.34, 0.34), (0.50, 0.46)), ((0.66, 0.34), (0.50, 0.46)),
                   ((0.36, 0.66), (0.50, 0.54)), ((0.64, 0.66), (0.50, 0.54))]:
        _line(d, [a, b], (255, 255, 255, 255), 0.025)
    for (x, y) in [(0.34, 0.34), (0.66, 0.34), (0.36, 0.66), (0.64, 0.66),
                   (0.50, 0.46), (0.50, 0.54)]:
        _el(d, (x - 0.05, y - 0.05, x + 0.05, y + 0.05), (255, 255, 255, 255))


def _scale(d, c):
    _line(d, [(0.50, 0.16), (0.50, 0.80)], c, 0.035)
    _line(d, [(0.20, 0.30), (0.80, 0.30)], c, 0.035)
    _poly(d, [(0.20, 0.30), (0.12, 0.52), (0.28, 0.52)], c)
    _poly(d, [(0.80, 0.30), (0.72, 0.52), (0.88, 0.52)], c)
    _rr(d, (0.34, 0.80, 0.66, 0.88), 0.02, c)


def _robot(d, c):
    _rr(d, (0.26, 0.28, 0.74, 0.72), 0.08, c)
    _el(d, (0.38, 0.42, 0.48, 0.52), (255, 255, 255, 255))
    _el(d, (0.52, 0.42, 0.62, 0.52), (255, 255, 255, 255))
    _line(d, [(0.50, 0.28), (0.50, 0.16)], c, 0.035)
    _el(d, (0.44, 0.08, 0.56, 0.20), c)
    _rr(d, (0.14, 0.40, 0.24, 0.60), 0.03, c)
    _rr(d, (0.76, 0.40, 0.86, 0.60), 0.03, c)


def _analytics(d, c):
    _line(d, [(0.16, 0.84), (0.84, 0.84)], c, 0.035)
    _line(d, [(0.16, 0.84), (0.16, 0.16)], c, 0.035)
    for x, h in [(0.28, 0.26), (0.44, 0.44), (0.60, 0.34), (0.76, 0.56)]:
        _rr(d, (x, 0.84 - h, x + 0.10, 0.84), 0.02, c)


def _wrench(d, c):
    import math
    _line(d, [(0.30, 0.30), (0.72, 0.72)], c, 0.11)
    d.arc([_S(0.18), _S(0.10), _S(0.52), _S(0.44)], 120, 300, fill=c,
          width=_S(0.11))
    _el(d, (0.60, 0.60, 0.90, 0.90), c)
    _el(d, (0.66, 0.66, 0.84, 0.84), (255, 255, 255, 255))


def _heart(d, c):
    _el(d, (0.14, 0.18, 0.52, 0.56), c)
    _el(d, (0.48, 0.18, 0.86, 0.56), c)
    _poly(d, [(0.14, 0.40), (0.86, 0.40), (0.50, 0.86)], c)


def _people(d, c):
    _el(d, (0.38, 0.14, 0.62, 0.38), c)
    _poly(d, [(0.26, 0.82), (0.34, 0.44), (0.66, 0.44), (0.74, 0.82)], c)
    _el(d, (0.10, 0.30, 0.28, 0.48), c)
    _el(d, (0.72, 0.30, 0.90, 0.48), c)


def _rocket(d, c):
    _poly(d, [(0.50, 0.10), (0.66, 0.50), (0.34, 0.50)], c)
    _rr(d, (0.36, 0.50, 0.64, 0.74), 0.04, c)
    _poly(d, [(0.36, 0.58), (0.24, 0.80), (0.38, 0.74)], c)
    _poly(d, [(0.64, 0.58), (0.76, 0.80), (0.62, 0.74)], c)
    _el(d, (0.44, 0.30, 0.56, 0.42), (255, 255, 255, 255))


def _compass(d, c):
    _el(d, (0.10, 0.10, 0.90, 0.90), c)
    _el(d, (0.20, 0.20, 0.80, 0.80), (255, 255, 255, 255))
    _poly(d, [(0.62, 0.38), (0.46, 0.54), (0.38, 0.62), (0.54, 0.46)], c)


def _code(d, c):
    _line(d, [(0.36, 0.30), (0.16, 0.50), (0.36, 0.70)], c, 0.06)
    _line(d, [(0.64, 0.30), (0.84, 0.50), (0.64, 0.70)], c, 0.06)
    _line(d, [(0.56, 0.24), (0.44, 0.76)], c, 0.055)


REGISTRY = {
    "headset": _headset, "cart": _cart, "car": _car, "calc": _calc,
    "gear": _gear, "book": _book, "speech": _speech, "hands": _hands,
    "palette": _palette, "stetho": _stetho, "teacher": _teacher,
    "brain": _brain, "scale": _scale, "robot": _robot,
    "analytics": _analytics, "wrench": _wrench, "heart": _heart,
    "people": _people, "rocket": _rocket, "compass": _compass,
    "code": _code,
}


@lru_cache(maxsize=None)
def render(name, color):
    """Return the PNG path for `name` tinted `color` (hex, no '#').
    Image is 512x512 with a transparent background."""
    fn = REGISTRY[name]
    img, d = _new()
    col = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) + (255,)
    fn(d, col)
    return _finish(img, name, color)
