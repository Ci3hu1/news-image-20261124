#!/usr/bin/env python3
"""Render the news-image-20261124 poster: 'Tuesday 24 November 2026'.

One-day world news poster, 1024x1024, Pillow-rendered. Visual language:
a night-desk atlas - deep navy ground, cream story cards, gold rules -
deliberately NOT the cream newspaper front page the field copies.
All 31 stories were first reported Tue 24 Nov 2026 in some time zone
(see BRIEF.md for the verification basis of each one). Two 23-Nov
stories are named only in the small DATE CHECK box as excluded.
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
PREVIEW = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "preview-300.png")

# ---------------------------------------------------------------- palette
NAVY = (14, 27, 46)
NAVY2 = (22, 40, 63)
NAVY3 = (30, 52, 80)
CREAM = (245, 237, 216)
PAPER = (251, 246, 233)
GOLD = (217, 164, 65)
GOLD_D = (176, 132, 44)
RED = (192, 57, 43)
INK = (26, 36, 51)
MUTED = (96, 110, 126)
SKY = (191, 217, 232)
LAND = (42, 74, 107)
LAND_L = (74, 107, 143)

REGION_COLORS = {
    "EUROPE": (143, 184, 216),
    "MIDDLE EAST": (232, 163, 61),
    "ASIA": (232, 115, 90),
    "AFRICA": (127, 176, 105),
    "AMERICAS": (78, 205, 196),
    "OCEANIA": (179, 136, 235),
}

# ---------------------------------------------------------------- fonts
def _font(path, size, fallback):
    try:
        return ImageFont.truetype(path, size)
    except (OSError, IOError):
        return ImageFont.truetype(fallback, size)

D = "/usr/share/fonts/truetype/dejavu/"
N = "/usr/share/fonts/truetype/noto/"
SERIF = D + "DejaVuSerif.ttf"
SERIF_B = D + "DejaVuSerif-Bold.ttf"
SANS = D + "DejaVuSans.ttf"
SANS_B = D + "DejaVuSans-Bold.ttf"
DISPLAY_B = N + "NotoSerifDisplay-Bold.ttf"


def f_display(size):
    return _font(DISPLAY_B, size, SERIF_B)


def f_serif(size):
    return _font(SERIF, size, SANS)


def f_serif_b(size):
    return _font(SERIF_B, size, SANS_B)


def f_sans(size):
    return _font(SANS, size, SANS)


def f_sans_b(size):
    return _font(SANS_B, size, SANS_B)


# ---------------------------------------------------------------- stories
# n, region, place, headline, body (heroes only), source, scene kind, lon, lat
STORIES = [
    (1, "AMERICAS", "Washington", "FBI No. 2 to quit in December",
     "Deputy director Christopher Raia intends to retire in December, "
     "the Washington Post reports.", "Reuters", "fbi", -77.0, 38.9),
    (2, "ASIA", "Manila", "6,000 cops out for transport strike",
     "More than 6,000 police deploy across Manila for a two-day "
     "transport strike.", "Daily Tribune", "strike", 121.0, 14.6),
    (3, "MIDDLE EAST", "Doha", "Qatar pushes to revive US-Iran talks",
     "Doha strives to revive US-Iran negotiations as the standoff "
     "deepens, Middle East Eye reports.", "Middle East Eye", "qatar",
     51.5, 25.3),
    (4, "ASIA", "Delhi", "Modi, Shah flag off Saryu-Kamala Express",
     "", "JagranJosh", "train", 77.2, 28.6),
    (5, "OCEANIA", "Melbourne", "Molly Meldrum dies, 83",
     "", "BBC", "music", 145.0, -37.8),
    (6, "EUROPE", "Spain", "Ferrari unveils two 296 models",
     "", "JagranJosh", "ferrari", -3.7, 40.4),
    (7, "MIDDLE EAST", "Tehran", "Qalibaf: 'no war, no peace' cannot go on",
     "", "Middle East Eye", "podium", 51.4, 35.7),
    (8, "MIDDLE EAST", "Baghdad", "Six jailed 10 years over uranium sale bid",
     "", "Shafaq News", "scales", 44.4, 33.3),
    (9, "OCEANIA", "Sydney", "NSW councils warn Minns on poker machines",
     "", "Medianet", "pokies", 151.2, -33.9),
    (10, "ASIA", "India", "First Test ends in draw",
     "", "Jagran", "cricket", 88.4, 22.6),
    (11, "ASIA", "Delhi", "Delhi court warrant for Dhruv Rathee",
     "", "Jagran", "court", 77.2, 28.6),
    (12, "OCEANIA", "Auckland", "Auckland police probe unexplained death",
     "", "RNZ", "police", 174.8, -36.8),
    (13, "AFRICA", "Bayelsa", "Rescue goes on after boat tragedy",
     "", "BBC", "rescue", 6.3, 4.8),
]

ALSO_ON = [
    (14, "ASIA", "Amarnath earthmover at Sheshnag lake draws outrage",
     "Jagran", 75.0, 34.0),
    (15, "ASIA", "Top court: Saharanpur mosque case to Allahabad HC",
     "Jagran", 77.5, 29.9),
    (16, "ASIA", "Myanmar slams ASEAN decision as 'unfair'",
     "JagranJosh", 96.0, 21.0),
    (17, "ASIA", "Banten factory-fire rescue continues",
     "JagranJosh", 106.0, -6.3),
    (18, "ASIA", "SpiceJet finances under scrutiny",
     "JagranJosh", 77.2, 28.6),
    (19, "ASIA", "Super TET city slips out",
     "JagranJosh", 80.9, 26.8),
    (20, "EUROPE", "Kyiv still counts missing after drone strike",
     "JagranJosh", 30.5, 50.4),
    (21, "AMERICAS", "LibertyStream files S-1 for US IPO",
     "Business Wire", -96.8, 32.8),
    (22, "AMERICAS", "Expensify launches Insights",
     "Medianet", -122.7, 45.5),
    (23, "OCEANIA", "Indigenous fire care 'best practice': study",
     "CDU", 130.8, -12.5),
    (24, "OCEANIA", "Treaties committee marks 30 years",
     "Medianet", 149.1, -35.3),
    (25, "OCEANIA", "Reef divers take ocean pledges to Parliament",
     "Medianet", 145.8, -16.9),
    (26, "OCEANIA", "Search for missing Wanaka hiker",
     "RNZ", 169.1, -44.7),
    (27, "OCEANIA", "ACT eyes vote on axing Maori seats",
     "RNZ", 174.8, -41.3),
    (28, "OCEANIA", "Rare parrots stun keepers with two egg sets",
     "RNZ", 172.6, -43.5),
    (29, "OCEANIA", "Estonia's advice to NZ on Russia",
     "RNZ", 174.8, -41.3),
    (30, "OCEANIA", "Guam wins $10.3m US grants",
     "RNZ Pacific", 144.8, 13.4),
    (31, "OCEANIA", "Knitting Nannas: 'stop destroying our forests'",
     "Medianet", 151.2, -33.9),
]

REGION_COUNTS = {"EUROPE": 2, "MIDDLE EAST": 3, "ASIA": 10,
                 "AFRICA": 1, "AMERICAS": 3, "OCEANIA": 12}
TOTAL_STORIES = 31
N_REGIONS = 6

TIMELINE = [
    ("OVERNIGHT 00:30", "Japan PMIs out"),
    ("MORNING", "6,000 cops in Manila"),
    ("MIDDAY", "Express flagged off"),
    ("AFTERNOON", "Ferrari unveils 296s"),
    ("EVENING", "FBI No. 2 exit"),
    ("NIGHT", "Qatar pushes talks"),
]

KPIS = [
    ("6,000", "police, Manila strike"),
    ("10 yrs", "uranium-sale sentences"),
    ("83", "Meldrum's age"),
    ("2", "new Ferrari models"),
    ("Rs 15,000 cr", "India-Nepal package"),
    ("$10.3m", "Guam grants"),
]

DATE_CHECK = [
    "Nvidia reinstates Jensen Huang \u2014 first reported Mon 23 Nov, "
    "NOT in this edition.",
    "COP31 ends with no deal \u2014 talks failed Sun 22 Nov, "
    "NOT in this edition.",
]

SOURCES_LINE = ("Sources: Reuters \u00b7 BBC \u00b7 Middle East Eye \u00b7 RNZ "
                "\u00b7 Shafaq News \u00b7 Medianet \u00b7 JagranJosh "
                "\u00b7 Daily Tribune \u00b7 Kurdistan24 \u2014 Original drawings")

# ---------------------------------------------------------------- helpers
PLACEMENTS = []  # (x0, y0, x1, y1, box) text bboxes, for the clearance test


def wrap(text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(text, font, max_w, max_lines):
    lines = wrap(text, font, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and font.getlength(lines[-1] + " \u2026") > max_w:
        lines[-1] = lines[-1].rsplit(" ", 1)[0] if " " in lines[-1] else ""
    lines[-1] = (lines[-1] + " \u2026").strip()
    return lines


def text(d, xy, s, font, fill, box=None, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)
    x, y = xy
    w = font.getlength(s)
    asc, desc = font.getmetrics()
    if anchor == "la":
        bbox = (x, y, x + w, y + asc + desc)
    elif anchor == "ma":
        bbox = (x - w / 2, y, x + w / 2, y + asc + desc)
    else:
        bbox = (x - w, y, x, y + asc + desc)
    if box is not None:
        PLACEMENTS.append((bbox, box))
    return bbox


def tracked_text(d, xy, s, font, fill, box):
    return text(d, xy, s, font, fill, box=box)


# ------------------------------------------------------- procedural scenes
def _rx(box, fx0, fy0, fx1, fy1):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    return (x0 + fx0 * w, y0 + fy0 * h, x0 + fx1 * w, y0 + fy1 * h)


def draw_scene(d, box, kind):
    """Flat illustration inside box (relative coords 0..1)."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    sky = {"fbi": (191, 217, 232), "strike": (214, 228, 238),
           "qatar": (232, 214, 178), "train": (191, 217, 232),
           "music": (232, 200, 214), "ferrari": (232, 90, 70),
           "podium": (191, 217, 232), "scales": (214, 228, 238),
           "pokies": (232, 214, 178), "cricket": (186, 220, 178),
           "court": (191, 217, 232), "police": (191, 217, 232),
           "rescue": (158, 196, 226)}[kind]
    d.rectangle(box, fill=sky)
    # ground
    d.rectangle([x0, y0 + h * 0.78, x1, y1], fill=(52, 72, 96))

    def R(fx0, fy0, fx1, fy1, fill, outline=None):
        d.rectangle(_rx(box, fx0, fy0, fx1, fy1), fill=fill,
                    outline=outline)

    def E(fx0, fy0, fx1, fy1, fill, outline=None):
        d.ellipse(_rx(box, fx0, fy0, fx1, fy1), fill=fill, outline=outline)

    def P(pts, fill):
        d.polygon([(x0 + fx * w, y0 + fy * h) for fx, fy in pts], fill=fill)

    def L(p1, p2, fill, width=2):
        d.line([x0 + p1[0] * w, y0 + p1[1] * h,
                x0 + p2[0] * w, y0 + p2[1] * h], fill=fill, width=width)

    if kind == "fbi":
        R(0.08, 0.30, 0.92, 0.80, (251, 246, 233))
        P([(0.05, 0.32), (0.50, 0.10), (0.95, 0.32)], (176, 60, 50))
        for fx in (0.16, 0.36, 0.56, 0.76):
            R(fx, 0.38, fx + 0.07, 0.78, (120, 140, 165))
        R(0.44, 0.55, 0.56, 0.80, (26, 36, 51))
    elif kind == "strike":
        R(0.06, 0.30, 0.94, 0.68, (217, 164, 65))
        for i in range(4):
            R(0.12 + i * 0.20, 0.38, 0.26 + i * 0.20, 0.52, SKY)
        E(0.22, 0.62, 0.34, 0.78, INK)
        E(0.66, 0.62, 0.78, 0.78, INK)
        E(0.80, 0.10, 0.96, 0.42, (192, 57, 43))
        d.text((x0 + w * 0.88, y0 + h * 0.13), "!", font=f_sans_b(max(10, int(h * 0.22))),
               fill=CREAM, anchor="mm")
    elif kind == "qatar":
        L((0.20, 0.12), (0.20, 0.80), INK, 3)
        P([(0.20, 0.12), (0.44, 0.20), (0.20, 0.28)], (128, 22, 54))
        L((0.80, 0.12), (0.80, 0.80), INK, 3)
        P([(0.80, 0.12), (0.56, 0.20), (0.80, 0.28)], (0, 70, 110))
        R(0.30, 0.62, 0.70, 0.80, (120, 90, 60))
        R(0.40, 0.52, 0.60, 0.62, PAPER)
    elif kind == "train":
        L((0.0, 0.80), (1.0, 0.80), INK, 3)
        L((0.0, 0.88), (1.0, 0.88), INK, 3)
        R(0.08, 0.32, 0.78, 0.78, (192, 57, 43))
        R(0.60, 0.18, 0.78, 0.34, (192, 57, 43))
        R(0.14, 0.40, 0.30, 0.56, SKY)
        R(0.36, 0.40, 0.52, 0.56, SKY)
        E(0.20, 0.70, 0.30, 0.84, INK)
        E(0.58, 0.70, 0.68, 0.84, INK)
        E(0.82, 0.14, 0.94, 0.30, (232, 190, 80))
    elif kind == "music":
        R(0.12, 0.18, 0.88, 0.72, INK)
        R(0.18, 0.24, 0.82, 0.66, (30, 52, 80))
        E(0.30, 0.30, 0.46, 0.52, GOLD)
        L((0.44, 0.30), (0.44, 0.58), GOLD, 3)
        E(0.52, 0.34, 0.64, 0.50, GOLD)
        L((0.62, 0.34), (0.62, 0.60), GOLD, 3)
        E(0.36, 0.74, 0.64, 0.80, GOLD)
    elif kind == "ferrari":
        P([(0.06, 0.62), (0.16, 0.42), (0.34, 0.34), (0.58, 0.34),
           (0.72, 0.44), (0.92, 0.48), (0.94, 0.62)], (192, 20, 20))
        R(0.38, 0.38, 0.52, 0.48, SKY)
        E(0.20, 0.58, 0.34, 0.78, INK)
        E(0.68, 0.58, 0.82, 0.78, INK)
        E(0.24, 0.63, 0.30, 0.73, (180, 180, 180))
        E(0.72, 0.63, 0.78, 0.73, (180, 180, 180))
        for i in range(6):
            R(0.06 + i * 0.15, 0.10, 0.13 + i * 0.15, 0.18,
              INK if i % 2 == 0 else CREAM)
    elif kind == "podium":
        P([(0.34, 0.44), (0.66, 0.44), (0.60, 0.80), (0.40, 0.80)],
          (120, 90, 60))
        R(0.30, 0.40, 0.70, 0.46, (90, 60, 40))
        L((0.50, 0.40), (0.50, 0.22), INK, 3)
        E(0.44, 0.12, 0.56, 0.26, INK)
        E(0.80, 0.14, 0.92, 0.30, (232, 190, 80))
    elif kind == "scales":
        L((0.50, 0.14), (0.50, 0.78), INK, 3)
        L((0.18, 0.24), (0.82, 0.24), INK, 3)
        L((0.18, 0.24), (0.10, 0.44), INK, 2)
        L((0.18, 0.24), (0.26, 0.44), INK, 2)
        L((0.82, 0.24), (0.74, 0.44), INK, 2)
        L((0.82, 0.24), (0.90, 0.44), INK, 2)
        P([(0.06, 0.44), (0.30, 0.44), (0.18, 0.56)], GOLD)
        P([(0.70, 0.44), (0.94, 0.44), (0.82, 0.56)], GOLD)
        E(0.44, 0.08, 0.56, 0.18, GOLD)
    elif kind == "pokies":
        R(0.22, 0.14, 0.78, 0.80, (176, 60, 50))
        R(0.28, 0.22, 0.72, 0.44, PAPER)
        for i, c in enumerate((GOLD, (78, 205, 196), GOLD)):
            E(0.30 + i * 0.14, 0.26, 0.40 + i * 0.14, 0.40, c)
        R(0.30, 0.52, 0.70, 0.62, INK)
        L((0.80, 0.20), (0.80, 0.52), INK, 3)
        E(0.76, 0.12, 0.86, 0.24, GOLD)
    elif kind == "cricket":
        for fx in (0.30, 0.38, 0.46):
            R(fx, 0.30, fx + 0.04, 0.78, (232, 190, 80))
        R(0.28, 0.26, 0.52, 0.30, (232, 190, 80))
        P([(0.62, 0.18), (0.70, 0.18), (0.62, 0.62), (0.56, 0.62)],
          (150, 110, 60))
        E(0.74, 0.60, 0.86, 0.76, (192, 57, 43))
    elif kind == "court":
        R(0.08, 0.34, 0.92, 0.80, PAPER)
        P([(0.05, 0.36), (0.50, 0.12), (0.95, 0.36)], (176, 60, 50))
        for fx in (0.16, 0.36, 0.56, 0.76):
            R(fx, 0.42, fx + 0.07, 0.78, (120, 140, 165))
        R(0.10, 0.62, 0.34, 0.70, (120, 90, 60))
        L((0.12, 0.58), (0.32, 0.58), INK, 3)
    elif kind == "police":
        P([(0.50, 0.10), (0.62, 0.24), (0.80, 0.24), (0.66, 0.38),
           (0.72, 0.56), (0.50, 0.46), (0.28, 0.56), (0.34, 0.38),
           (0.20, 0.24), (0.38, 0.24)], GOLD)
        E(0.42, 0.30, 0.58, 0.46, NAVY)
        R(0.06, 0.66, 0.94, 0.78, (192, 57, 43))
        d.text((x0 + w * 0.50, y0 + h * 0.72), "POLICE LINE",
               font=f_sans_b(max(9, int(h * 0.11))), fill=CREAM, anchor="mm")
    elif kind == "rescue":
        for fy in (0.62, 0.72):
            d.arc(_rx(box, 0.0, fy, 1.0, fy + 0.22), 0, 180,
                  fill=CREAM, width=3)
        P([(0.30, 0.52), (0.70, 0.52), (0.64, 0.66), (0.36, 0.66)],
          (232, 120, 60))
        E(0.44, 0.30, 0.56, 0.46, (232, 190, 120))
        R(0.48, 0.44, 0.52, 0.54, (192, 57, 43))
    # frame
    d.rectangle(box, outline=GOLD_D, width=1)


# ---------------------------------------------------------------- map
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-75, 62), (-70, 44), (-75, 35), (-80, 26), (-85, 30),
     (-90, 21), (-97, 16), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    [(-58, 64), (-45, 60), (-30, 68), (-25, 70), (-40, 76), (-58, 76)],
    [(-80, 10), (-75, 5), (-70, 12), (-60, 10), (-50, 5), (-50, 0),
     (-40, -5), (-35, -10), (-40, -20), (-48, -28), (-55, -35),
     (-65, -40), (-70, -52), (-73, -40), (-72, -20), (-78, -5), (-80, 5)],
    [(-17, 15), (-10, 30), (-5, 35), (10, 37), (20, 32), (32, 31),
     (35, 28), (40, 15), (48, 11), (51, 12), (44, 0), (40, -10),
     (35, -18), (32, -28), (25, -34), (18, -35), (12, -18), (9, 4),
     (-8, 5), (-15, 11)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (30, 70),
     (25, 71), (18, 69), (12, 65), (5, 60), (5, 58), (-2, 57), (-5, 50),
     (-10, 44)],
    [(30, 62), (40, 68), (55, 69), (70, 72), (90, 75), (110, 76),
     (130, 72), (150, 70), (170, 66), (178, 65), (170, 60), (160, 55),
     (155, 50), (142, 45), (140, 40), (135, 35), (127, 33), (122, 30),
     (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (85, 20), (80, 13), (77, 8), (72, 20), (66, 25), (60, 25),
     (55, 26), (50, 29), (48, 30), (43, 35), (40, 36), (36, 36),
     (33, 42), (30, 45), (30, 55)],
    [(113, -22), (114, -30), (115, -35), (124, -33), (130, -32),
     (137, -35), (140, -38), (145, -38), (150, -37), (153, -32),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11),
     (136, -12), (132, -11), (126, -14), (122, -17), (118, -20)],
    [(95, 5), (100, 0), (105, -5), (110, -7), (115, -8), (120, -10),
     (125, -8), (130, -3), (135, -4), (140, -8)],
    [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)],
    [(130, 31), (132, 33), (135, 34), (138, 35), (140, 38), (141, 41),
     (143, 43), (145, 44), (142, 42), (139, 38), (136, 35), (133, 34)],
    [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38),
     (175, -40), (172, -43), (168, -46)],
]


def lonlat_to_xy(lon, lat, area):
    ax0, ay0, ax1, ay1 = area
    x = ax0 + (lon + 170.0) / 360.0 * (ax1 - ax0)
    y = ay0 + (75.0 - lat) / 130.0 * (ay1 - ay0)
    return x, y


# ---------------------------------------------------------------- render
def render():
    PLACEMENTS.clear()
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # ---- masthead (0-112)
    d.rectangle([0, 0, W, 4], fill=GOLD)
    kicker = "THE WORLD IN ONE PICTURE"
    kf = f_sans_b(16)
    kx = (W - kf.getlength(kicker)) / 2
    text(d, (kx, 14), kicker, kf, GOLD)
    mast = "TUESDAY 24 NOVEMBER 2026"
    mf = f_display(52)
    mx = (W - mf.getlength(mast)) / 2
    text(d, (mx, 34), mast, mf, CREAM)
    count = "31 STORIES \u00b7 6 REGIONS \u00b7 ALL FROM TUESDAY"
    cf = f_sans_b(18)
    cx = (W - cf.getlength(count)) / 2
    text(d, (cx, 88), count, cf, GOLD)
    d.line([12, 112, W - 12, 112], fill=GOLD_D, width=1)

    # ---- UTC timeline (112-157)
    d.rectangle([0, 113, W, 157], fill=NAVY2)
    slot_w = W / 6
    tf = f_sans_b(12)
    ef = f_sans(12)
    for i, (label, event) in enumerate(TIMELINE):
        cx = slot_w * i + slot_w / 2
        d.ellipse([cx - 4, 114, cx + 4, 122], fill=GOLD)
        text(d, (cx, 124), label, tf, GOLD, anchor="ma")
        ev = fit_lines(event, ef, slot_w - 14, 1)
        text(d, (cx, 138), ev[0] if ev else "", ef, CREAM, anchor="ma")
    d.line([12, 157, W - 12, 157], fill=GOLD_D, width=1)

    # ---- heroes (158-410): 3 cream cards
    hy0, hy1 = 158, 410
    hw, gap = 322, 10
    for i, s in enumerate(STORIES[:3]):
        n, region, place, head, body, src, kind, lon, lat = s
        x0 = 12 + i * (hw + gap)
        x1 = x0 + hw
        card = (x0, hy0, x1, hy1)
        d.rounded_rectangle(card, radius=4, fill=PAPER)
        d.rounded_rectangle(card, radius=4, outline=GOLD_D, width=1)
        # badge + region tag
        d.ellipse([x0 + 10, hy0 + 10, x0 + 44, hy0 + 44], fill=GOLD)
        text(d, (x0 + 27, hy0 + 15), str(n), f_sans_b(20), NAVY,
             box=card, anchor="ma")
        text(d, (x0 + 52, hy0 + 18), region + " \u00b7 " + place.upper(),
             f_sans_b(13), REGION_COLORS[region], box=card)
        # scene
        draw_scene(d, (x0 + 10, hy0 + 52, x1 - 10, hy0 + 150), kind)
        # headline (2 lines, serif bold 20px)
        hf = f_serif_b(20)
        lines = fit_lines(head, hf, hw - 24, 2)
        y = hy0 + 156
        for ln in lines:
            text(d, (x0 + 12, y), ln, hf, INK, box=card)
            y += 23
        # body (2 lines, 13px)
        bf = f_sans(13)
        blines = fit_lines(body, bf, hw - 24, 2)
        y = hy0 + 204
        for ln in blines:
            text(d, (x0 + 12, y), ln, bf, INK, box=card)
            y += 15
        # source
        text(d, (x1 - 12, hy1 - 16), "(" + src + ")", f_sans(11), MUTED,
             box=card, anchor="ra")

    # ---- featured (414-618): 10 cards, 2 rows x 5
    fy0 = 414
    cw, ch, cgap = 196, 98, 8
    for j, s in enumerate(STORIES[3:13]):
        n, region, place, head, body, src, kind, lon, lat = s
        row, col = divmod(j, 5)
        x0 = 12 + col * (cw + cgap)
        y0 = fy0 + row * (ch + 8)
        x1, y1 = x0 + cw, y0 + ch
        card = (x0, y0, x1, y1)
        d.rounded_rectangle(card, radius=4, fill=PAPER)
        d.rounded_rectangle(card, radius=4, outline=GOLD_D, width=1)
        # badge row (number + region, on the cream card, above the scene)
        d.ellipse([x0 + 6, y0 + 5, x0 + 24, y0 + 23], fill=GOLD)
        text(d, (x0 + 15, y0 + 6), str(n), f_sans_b(12), NAVY,
             box=card, anchor="ma")
        text(d, (x0 + 28, y0 + 7), region, f_sans_b(11),
             REGION_COLORS[region], box=card)
        # scene strip below the badge row (no text over it)
        draw_scene(d, (x0 + 6, y0 + 26, x1 - 6, y0 + 48), kind)
        hf = f_serif_b(13)
        lines = fit_lines(head, hf, cw - 16, 2)
        y = y0 + 50
        for ln in lines:
            text(d, (x0 + 8, y), ln, hf, INK, box=card)
            y += 14
        text(d, (x1 - 8, y1 - 16), "(" + src + ")", f_sans(10), MUTED,
             box=card, anchor="ra")

    # ---- KPI strip (612-660)
    d.rectangle([0, 620, W, 660], fill=NAVY2)
    d.line([12, 620, W - 12, 620], fill=GOLD_D, width=1)
    d.line([12, 660, W - 12, 660], fill=GOLD_D, width=1)
    kw = W / 6
    for i, (num, lab) in enumerate(KPIS):
        cx = kw * i + kw / 2
        nf = f_display(22)
        text(d, (cx, 620), num, nf, GOLD, anchor="ma")
        lf = f_sans(11)
        text(d, (cx, 645), lab, lf, CREAM, anchor="ma")

    # ---- map (660-792)
    d.rectangle([0, 661, W, 792], fill=NAVY)
    mt = "WHERE IT HAPPENED \u2014 STORIES 1\u201313 PINNED  \u00b7  "
    mt += "DOTS: STORIES 14\u201331"
    text(d, (12, 666), mt, f_sans_b(13), GOLD)
    # legend (right side)
    lx = W - 12
    leg = f_sans(10)
    items = list(REGION_COLORS.items())
    total_w = sum(leg.getlength(k) + 22 for k, _ in items)
    x = lx - total_w
    for k, c in items:
        d.ellipse([x, 670, x + 10, 680], fill=c)
        text(d, (x + 13, 668), k, leg, CREAM)
        x += leg.getlength(k) + 22
    area = (24, 686, 1000, 788)
    for poly in CONTINENTS:
        pts = [lonlat_to_xy(lon, lat, area) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=LAND_L)
    # dots for 14-31 first (under pins)
    for n, region, _t, _s, lon, lat in ALSO_ON:
        px, py = lonlat_to_xy(lon, lat, area)
        d.ellipse([px - 3, py - 3, px + 3, py + 3],
                  fill=REGION_COLORS[region], outline=GOLD)
    # numbered pins 1-13 (staggered where two share a city)
    offsets = {3: (0, 12), 7: (0, -12), 4: (-9, 0), 11: (9, 0),
               5: (-10, 0), 9: (10, 0)}
    for s in STORIES:
        n, region, _p, _h, _b, _s2, _k, lon, lat = s
        dx, dy = offsets.get(n, (0, 0))
        px, py = lonlat_to_xy(lon, lat, area)
        px += dx
        py += dy
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=GOLD,
                  outline=NAVY)
        text(d, (px, py - 8), str(n), f_sans_b(11), NAVY, anchor="ma")
    d.line([12, 792, W - 12, 792], fill=GOLD_D, width=1)

    # ---- ALSO ON list (792-942)
    text(d, (12, 798), "ALSO ON TUESDAY \u2014 14\u201331",
         f_sans_b(14), GOLD)
    af = f_sans(14)
    col_w = (W - 24) / 2
    for i, (n, region, title, src, _lon, _lat) in enumerate(ALSO_ON):
        col, row = divmod(i, 9)
        x0 = 12 + col * col_w
        y = 816 + row * 13
        line = "%d. %s \u2014 %s" % (n, title, src)
        while af.getlength(line) > col_w - 8 and len(line) > 10:
            line = line[:-1]
        if af.getlength(line) > col_w - 8:
            line = line[:60] + "\u2026"
        text(d, (x0, y), line, af, CREAM)

    # ---- DATE CHECK (942-990)
    d.rounded_rectangle([12, 946, W - 12, 988], radius=4, outline=GOLD,
                        width=2)
    text(d, (24, 951), "DATE CHECK \u2014 EXCLUDED", f_sans_b(13), GOLD)
    df = f_sans(13)
    y = 951
    for item in DATE_CHECK:
        text(d, (250, y), "\u2022  " + item, df, CREAM)
        y += 18

    # ---- footer (990-1024)
    ff = f_sans(12)
    vline = ("Every story above was first reported Tue 24 Nov 2026 "
             "in some time zone.")
    text(d, ((W - ff.getlength(vline)) / 2, 992), vline, ff, CREAM)
    sf = f_sans(11)
    text(d, ((W - sf.getlength(SOURCES_LINE)) / 2, 1006), SOURCES_LINE,
         sf, MUTED)

    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150,
                                             threshold=2))
    img.save(OUT, optimize=True)
    img.resize((300, 300), Image.LANCZOS).save(PREVIEW, optimize=True)
    with open(OUT, "rb") as f:
        data = f.read()
    return OUT, len(data), hashlib.sha256(data).hexdigest()


def check_clearance():
    """Every recorded text bbox must sit >=2px inside its card box."""
    bad = []
    for (x0, y0, x1, y1), (bx0, by0, bx1, by1) in PLACEMENTS:
        if x0 < bx0 + 2 or y0 < by0 + 2 or x1 > bx1 - 2 or y1 > by1 - 2:
            bad.append(((round(x0), round(y0), round(x1), round(y1)),
                        (bx0, by0, bx1, by1)))
    return bad


if __name__ == "__main__":
    path, size, sha = render()
    print("rendered %s %d bytes sha256 %s" % (path, size, sha))
    bad = check_clearance()
    print("clearance violations: %d" % len(bad))
    for b in bad[:10]:
        print("  ", b)
    sys.exit(1 if bad else 0)
