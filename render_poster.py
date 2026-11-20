#!/usr/bin/env python3
"""Render the 20 November 2026 one-image newspaper front page.

Draws everything with Pillow: a masthead, a hand-drawn Vice City sunset
scene for the GTA VI hero story, and six short story cards. No network,
no external assets, deterministic output (fixed random seed, no clock).
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

INK = (20, 18, 22)
PAPER = (247, 243, 234)
RED = (178, 34, 34)
GREY = (96, 92, 86)
RULE = (60, 55, 50)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = font("DejaVuSerif-Bold.ttf", 62)
SERIF_HEAD = font("DejaVuSerif-Bold.ttf", 46)
SERIF_CARD = font("DejaVuSerif-Bold.ttf", 23)
SANS = font("DejaVuSans.ttf", 17)
SANS_BODY = font("DejaVuSans.ttf", 16)
SANS_B = font("DejaVuSans-Bold.ttf", 15)
SANS_SMALL = font("DejaVuSans.ttf", 13)
SANS_DATE = font("DejaVuSans-Bold.ttf", 16)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_sunset(draw, box, rng):
    x0, y0, x1, y1 = box
    top = (43, 16, 68)
    mid = (168, 44, 96)
    low = (232, 116, 54)
    horizon = (255, 176, 92)
    for y in range(y0, y1):
        t = (y - y0) / max(1, (y1 - y0))
        if t < 0.45:
            col = lerp(top, mid, t / 0.45)
        elif t < 0.8:
            col = lerp(mid, low, (t - 0.45) / 0.35)
        else:
            col = lerp(low, horizon, (t - 0.8) / 0.2)
        draw.line([(x0, y), (x1, y)], fill=col)
    # Sun: pale disc low over the skyline, with a soft halo.
    # Sun: pale disc low over the skyline.
    cx, cy, r = 700, y1 - 118, 62
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 226, 158))
    # Skyline silhouettes.
    base_y = y1 - 34
    x = x0
    while x < x1:
        bw = rng.randint(34, 74)
        bh = rng.randint(46, 150)
        draw.rectangle([x, base_y - bh, x + bw, base_y], fill=(26, 14, 40))
        for wy in range(base_y - bh + 8, base_y - 6, 12):
            for wx in range(x + 6, x + bw - 4, 12):
                if rng.random() < 0.28:
                    draw.rectangle([wx, wy, wx + 3, wy + 4],
                                   fill=(255, 196, 110))
        x += bw + rng.randint(2, 10)
    # Water strip with light streaks.
    for y in range(base_y, y1):
        t = (y - base_y) / max(1, (y1 - base_y))
        draw.line([(x0, y), (x1, y)], fill=lerp((30, 16, 46), (94, 40, 66), t))
    for _ in range(26):
        sx = rng.randint(x0 + 10, x1 - 120)
        sy = rng.randint(base_y + 4, y1 - 4)
        ln = rng.randint(24, 110)
        draw.line([(sx, sy), (sx + ln, sy)],
                  fill=(255, 170, 110), width=2)
    # Sun reflection: a shimmering column on the water below the sun.
    for yy in range(base_y + 3, y1 - 3, 6):
        half = rng.randint(16, 42)
        draw.line([(cx - half, yy), (cx + half, yy)],
                  fill=(255, 190, 120), width=2)


def draw_birds(draw, spots):
    """Small gull silhouettes: two short arcs each."""
    for bx, by, s in spots:
        draw.arc([bx, by, bx + 16 * s, by + 9 * s], 200, 330,
                 fill=(30, 16, 40), width=2)
        draw.arc([bx + 15 * s, by, bx + 31 * s, by + 9 * s], 210, 340,
                 fill=(30, 16, 40), width=2)


def card(draw, x, y, w, h, kicker, headline, body):
    draw.text((x, y), kicker, font=SANS_B, fill=RED)
    draw.text((x, y + 22), headline, font=SERIF_CARD, fill=INK)
    lines = wrap(draw, body, SANS_BODY, w)
    yy = y + 52
    for line in lines[:3]:
        draw.text((x, yy), line, font=SANS_BODY, fill=(52, 48, 44))
        yy += 21


def render(path):
    rng = random.Random(20261120)
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    draw.rectangle([6, 6, W - 7, H - 7], outline=RULE, width=2)

    # Masthead.
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=SERIF_B)
    draw.text(((W - tw) / 2, 26), title, font=SERIF_B, fill=INK)
    draw.line([(28, 104), (W - 28, 104)], fill=RULE, width=2)
    draw.text((28, 114), "FRIDAY, 20 NOVEMBER 2026",
              font=SANS_DATE, fill=INK)
    right = "ONE PAGE  ·  SEVEN STORIES"
    draw.text((W - 28 - draw.textlength(right, font=SANS_DATE), 114),
              right, font=SANS_DATE, fill=INK)
    draw.line([(28, 140), (W - 28, 140)], fill=RULE, width=1)

    # Hero art: Vice City sunset, 150..452.
    art = (28, 152, W - 28, 452)
    draw_sunset(draw, art, rng)
    draw_birds(draw, [(120, 190, 1), (210, 230, 1), (880, 200, 1)])
    draw.rectangle([28, 152, W - 28, 452], outline=RULE, width=1)

    # Hero headline and standfirst.
    head = "GTA VI SMASHES RECORDS"
    hw = draw.textlength(head, font=SERIF_HEAD)
    draw.text(((W - hw) / 2, 466), head, font=SERIF_HEAD, fill=INK)
    stand = ("An estimated $2.36 billion and 24.6 million copies on day one "
             "— about three times GTA V's first-day haul, Sensor Tower estimates.")
    lines = wrap(draw, stand, SANS, W - 120)
    yy = 524
    for line in lines:
        lw = draw.textlength(line, font=SANS)
        draw.text(((W - lw) / 2, yy), line, font=SANS, fill=(52, 48, 44))
        yy += 23
    draw.line([(28, 584), (W - 28, 584)], fill=RULE, width=2)

    stories = [
        ("SUMMIT IN SHENZHEN", "Trump, Xi and Putin meet",
         "The three leaders held a first-ever three-way meeting in Shenzhen "
         "and released a joint \u201cpeace declaration\u201d."),
        ("CYCLONE AKVAN", "Cyclone Akvan hits Odisha",
         "Landfall near Gopalpur at noon, winds gusting to 110 km/h; "
         "hundreds of thousands evacuated, 423 rescue teams deployed."),
        ("TAIZ, YEMEN", "Voices from besieged Taiz",
         "Seven people inside the Yemeni city speak to the BBC; 148 "
         "civilians killed by Houthi attacks since August."),
        ("CRICKET", "Phillips\u2019 year of tons",
         "Glenn Phillips hit 118 as New Zealand reached 317-6 at lunch on "
         "day two against India in Wellington."),
        ("MARKETS", "Gold at a 14-month low",
         "Bullion slid near $3,682 an ounce as traders priced in a "
         "December Fed rate hike."),
        ("BOLLYWOOD", "Ramayana keeps rolling",
         "Day 15 added about \u20b919 crore in India; the epic now stands "
         "at \u20b9851 crore net, \u20b91,531 crore worldwide."),
    ]
    col_w = (W - 56 - 24) // 2
    row_y = [600, 716, 832]
    for i, (kick, head, body) in enumerate(stories):
        cx = 28 + (i % 2) * (col_w + 24)
        cy = row_y[i // 2]
        card(draw, cx, cy, col_w, 100, kick, head, body)
    draw.line([(W // 2, 600), (W // 2, 936)], fill=(200, 194, 182), width=1)
    for ry in (706, 822):
        draw.line([(28, ry), (W - 28, ry)], fill=(200, 194, 182), width=1)

    # Footer: sources.
    draw.line([(28, 952), (W - 28, 952)], fill=RULE, width=1)
    foot = ("Sources: Reuters \u00b7 Deadline / Sensor Tower \u00b7 BBC \u00b7 "
            "India Meteorological Department \u00b7 Wall Street Journal \u00b7 "
            "Box Office India \u2014 20 November 2026. GTA VI sales are estimates, "
            "not official Take-Two figures.")
    flines = wrap(draw, foot, SANS_SMALL, W - 120)
    yy = 962
    for line in flines:
        lw = draw.textlength(line, font=SANS_SMALL)
        draw.text(((W - lw) / 2, yy), line, font=SANS_SMALL, fill=GREY)
        yy += 17

    img.save(path, "PNG", optimize=True)
    print("wrote", path)


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "entry.png")
