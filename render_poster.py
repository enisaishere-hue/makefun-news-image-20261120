#!/usr/bin/env python3
"""Render the 20 November 2026 one-page newspaper poster (v2).

Draws everything with Pillow primitives (gradients, shapes, lines) — no
photographs, no logos, no pasted artwork. Writes entry.png, 1024x1024.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (22, 22, 26)
RED = (164, 30, 34)
NAVY = (18, 30, 61)
GOLD = (184, 134, 11)
TEAL = (14, 110, 110)
GREY = (90, 88, 80)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        draw.line([(x0, y), (x1, y)], fill=lerp(top, bottom, t))


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def skyline(draw, box, color, heights, lit):
    x0, y0, x1, y1 = box
    n = len(heights)
    bw = (x1 - x0) / n
    for i, hfrac in enumerate(heights):
        bx0 = x0 + i * bw + 2
        bx1 = x0 + (i + 1) * bw - 2
        by1 = y1
        by0 = y1 - hfrac * (y1 - y0)
        draw.rectangle([bx0, by0, bx1, by1], fill=color)
        for r in range(int(by0) + 8, int(by1) - 8, 16):
            for c in range(int(bx0) + 6, int(bx1) - 6, 14):
                if (r * 7 + c * 13) % 5 < 2:
                    draw.rectangle([c, r, c + 5, r + 6], fill=lit)


def cyclone(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (8, 60, 90), (40, 140, 160))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r in range(52, 6, -9):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
                 fill=(235, 245, 245), width=4)
    draw.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(235, 245, 245))
    for i in range(12):
        rx = x0 + 12 + (i * 23) % (x1 - x0 - 24)
        ry = y0 + 6 + (i * 11) % (y1 - y0 - 26)
        draw.line([(rx, ry), (rx - 4, ry + 13)], fill=(200, 225, 230), width=2)


def taiz_art(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (58, 44, 84), (150, 90, 70))
    draw.polygon([(x0, y1), (x0 + 70, y0 + 30), (x0 + 150, y1)], fill=(40, 30, 58))
    draw.polygon([(x0 + 110, y1), (x0 + 210, y0 + 16), (x1, y1)], fill=(34, 26, 50))
    base = y1
    for i, h in enumerate([24, 36, 28, 44, 32, 40, 26]):
        bx0 = x0 + 8 + i * 42
        draw.rectangle([bx0, base - h, bx0 + 34, base], fill=(24, 18, 36))
        draw.rectangle([bx0 + 8, base - h - 6, bx0 + 14, base - h], fill=(24, 18, 36))
    # thin smoke wisps above a rooftop
    sx, sy = x0 + 196, y0 + 34
    for i, r in enumerate([3, 4, 5, 6]):
        draw.ellipse([sx + i * 5 - r, sy - i * 7 - r,
                      sx + i * 5 + r, sy - i * 7 + r], fill=(196, 186, 176))
    # small distant flash
    fx, fy = x0 + 252, y0 + 58
    for a in range(0, 360, 45):
        r = math.radians(a)
        draw.line([(fx, fy), (fx + math.cos(r) * 8, fy + math.sin(r) * 8)],
                  fill=(255, 214, 120), width=2)


def cricket_art(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (46, 130, 62), (24, 84, 40))
    draw.rectangle([x0 + 120, y0, x0 + 186, y1], fill=(214, 196, 150))
    draw.line([(x0 + 120, y0 + 20), (x0 + 186, y0 + 20)], fill=(255, 255, 255), width=2)
    draw.line([(x0 + 120, y1 - 20), (x0 + 186, y1 - 20)], fill=(255, 255, 255), width=2)
    for sx in (x0 + 138, x0 + 146, x0 + 154):
        draw.line([(sx, y0 + 6), (sx, y0 + 22)], fill=(240, 210, 90), width=3)
    # bat leaning on the pitch edge
    draw.polygon([(x0 + 216, y0 + 14), (x0 + 230, y0 + 22), (x0 + 200, y0 + 70),
                  (x0 + 188, y0 + 62)], fill=(232, 214, 170), outline=(120, 90, 40))
    draw.line([(x0 + 223, y0 + 18), (x0 + 238, y0 + 4)], fill=(120, 90, 40), width=4)
    # ball, lower left
    draw.ellipse([x0 + 42, y0 + 48, x0 + 62, y0 + 68], fill=(178, 34, 34))
    draw.arc([x0 + 42, y0 + 48, x0 + 62, y0 + 68], start=200, end=340,
             fill=(255, 255, 255), width=2)
    draw.text((x0 + 14, y0 + 6), "317-6", font=font(SANS_B, 24), fill=(255, 255, 255))


def gold_art(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(28, 28, 34))
    # gold bars, left half
    for i, (bx, by, bw) in enumerate([(x0 + 20, y1 - 30, 58), (x0 + 84, y1 - 30, 58),
                                      (x0 + 52, y1 - 52, 58)]):
        draw.polygon([(bx, by), (bx + 8, by - 11), (bx + bw - 8, by - 11), (bx + bw, by)],
                     fill=(212, 175, 55))
        draw.rectangle([bx, by, bx + bw, by + 9], fill=(184, 150, 40))
    # price label + descending line, right half
    draw.text((x0 + 196, y0 + 6), "$3,650", font=font(SANS_B, 22), fill=(240, 200, 90))
    pts = [(x0 + 176, y0 + 30), (x0 + 214, y0 + 36), (x0 + 252, y0 + 42),
           (x0 + 290, y0 + 50)]
    draw.line(pts, fill=(220, 60, 50), width=4)


def cinema_art(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (96, 20, 28), (52, 10, 16))
    # stepped temple tower, left
    tx = x0 + 44
    widths = [72, 58, 44, 30]
    for i, wdt in enumerate(widths):
        yy0 = y1 - 14 - (i + 1) * 12
        draw.rectangle([tx + (72 - wdt) // 2, yy0, tx + (72 + wdt) // 2, yy0 + 12],
                       fill=(22, 8, 10))
        draw.rectangle([tx + (72 - wdt) // 2, yy0, tx + (72 + wdt) // 2, yy0 + 2],
                       fill=(232, 180, 80))
    draw.ellipse([tx + 30, y1 - 14 - 52, tx + 42, y1 - 14 - 40], fill=(232, 180, 80))
    # film strip, right
    fx0, fy0 = x0 + 150, y0 + 12
    draw.rectangle([fx0, fy0, x1 - 16, fy0 + 52], fill=(16, 12, 12))
    for i in range(3):
        cx0 = fx0 + 12 + i * 44
        draw.rectangle([cx0, fy0 + 10, cx0 + 32, fy0 + 42], outline=(232, 180, 80), width=2)
        draw.rectangle([cx0 + 5, fy0 + 16, cx0 + 27, fy0 + 36], fill=(232, 180, 80))


def hero_art(draw, box):
    x0, y0, x1, y1 = box
    vgrad(draw, box, (74, 22, 92), (214, 84, 44))
    sx, sy = x1 - 150, y0 + 72
    draw.ellipse([sx - 50, sy - 50, sx + 50, sy + 50], fill=(255, 226, 150))
    draw.ellipse([sx - 62, sy - 62, sx + 62, sy + 62], outline=(255, 226, 150), width=3)
    heights = [0.42, 0.62, 0.5, 0.78, 0.58, 0.7, 0.46, 0.82, 0.6, 0.74, 0.52,
               0.66, 0.44, 0.8, 0.56, 0.68, 0.48, 0.72]
    skyline(draw, (x0, y0 + 52, x1, y1 - 40), (26, 14, 44), heights, (255, 214, 110))
    wy = y1 - 40
    draw.rectangle([x0, wy, x1, y1], fill=(20, 16, 52))
    for i in range(26):
        rx = x0 + 10 + (i * 37) % (x1 - x0 - 20)
        rw = 18 + (i * 13) % 30
        draw.line([(rx, wy + 8 + (i % 3) * 10), (rx + rw, wy + 8 + (i % 3) * 10)],
                  fill=(255, 190, 120), width=2)
    # two small sailboats on the water
    for bx, by, s in [(x0 + 96, wy + 26, 1.0), (x1 - 210, wy + 30, 0.8)]:
        draw.line([(bx, by - 26 * s), (bx, by)], fill=(240, 230, 210), width=2)
        draw.polygon([(bx + 2, by - 24 * s), (bx + 2, by - 4), (bx + 20 * s, by - 4)],
                     fill=(255, 240, 200))
        draw.polygon([(bx - 2, by - 20 * s), (bx - 2, by - 4), (bx - 13 * s, by - 4)],
                     fill=(220, 200, 170))
        draw.polygon([(bx - 16 * s, by), (bx + 22 * s, by),
                      (bx + 16 * s, by + 7), (bx - 10 * s, by + 7)], fill=(12, 10, 26))
    draw.text((x0 + 340, y0 + 6), "VI", font=font(SERIF_B, 118),
              fill=(255, 255, 255), stroke_width=3, stroke_fill=(26, 14, 44))


def panel(draw, box, kicker, kicker_color, headline, deck, art_fn,
          art_h, head_size, deck_size):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(255, 255, 255), outline=(200, 194, 178), width=1)
    art_fn(draw, (x0 + 1, y0 + 1, x1 - 1, y0 + art_h))
    draw.rectangle([x0 + 1, y0 + art_h, x1 - 1, y0 + art_h + 4], fill=kicker_color)
    tx = x0 + 14
    ty = y0 + art_h + 12
    draw.text((tx, ty), kicker, font=font(SANS_B, 15), fill=kicker_color)
    ty += 24
    hf = font(SERIF_B, head_size)
    for line in wrap(draw, headline, hf, x1 - x0 - 28):
        draw.text((tx, ty), line, font=hf, fill=INK)
        ty += head_size + 5
    ty += 2
    df = font(SANS, deck_size)
    for line in wrap(draw, deck, df, x1 - x0 - 28):
        draw.text((tx, ty), line, font=df, fill=(58, 56, 50))
        ty += deck_size + 5


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([10, 10, 1013, 1013], outline=INK, width=2)
    d.rectangle([16, 16, 1007, 1007], outline=INK, width=1)

    # masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 66)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 28), title, font=tf, fill=INK)
    date = "Friday, 20 November 2026"
    df = font(SANS_B, 30)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 108), date, font=df, fill=RED)
    d.line([(28, 148), (996, 148)], fill=INK, width=3)
    d.line([(28, 154), (996, 154)], fill=INK, width=1)

    # hero art + headline band
    hero_art(d, (28, 162, 996, 392))
    d.rectangle([28, 392, 996, 512], fill=NAVY)
    d.text((44, 402), "VICE CITY  ·  DAY TWO", font=font(SANS_B, 19), fill=(255, 214, 110))
    d.text((44, 426), "GTA VI passes $2.36 billion",
           font=font(SERIF_B, 42), fill=(255, 255, 255))
    d.text((44, 482), "24.59 million copies in under a day — the biggest entertainment launch ever",
           font=font(SANS, 19), fill=(220, 222, 230))

    # row 1: three panels
    y1, y2 = 526, 764
    panel(d, (28, y1, 336, y2), "WEATHER  ·  INDIA", TEAL,
          "Cyclone Akvan hits Odisha",
          "300,000 evacuated as the storm comes ashore near Gopalpur; 423 rescue teams out.",
          cyclone, art_h=76, head_size=25, deck_size=16)
    panel(d, (350, y1, 658, y2), "MIDDLE EAST  ·  YEMEN", RED,
          "Taiz: \u2018It\u2019s just fireworks\u2019",
          "Seven voices from the besieged city; 148 civilians killed since August, the BBC reports.",
          taiz_art, art_h=76, head_size=25, deck_size=16)
    panel(d, (672, y1, 996, y2), "SPORT  ·  WELLINGTON", (30, 110, 60),
          "Phillips makes history",
          "First batter with centuries vs India in all three formats in one year; NZ 317-6 at lunch.",
          cricket_art, art_h=76, head_size=25, deck_size=16)

    # row 2: two wide panels
    y3, y4 = 778, 946
    panel(d, (28, y3, 506, y4), "MARKETS", GOLD,
          "Gold stuck at one-year lows",
          "Metal holds near $3,650 after Thursday\u2019s slide as rate-rise bets grow.",
          gold_art, art_h=60, head_size=24, deck_size=16)
    panel(d, (520, y3, 996, y4), "CINEMA  ·  INDIA", (120, 30, 40),
          "Ramayana still packs cinemas",
          "Rs 19.35 crore on day 15 for the Ranbir Kapoor epic.",
          cinema_art, art_h=60, head_size=24, deck_size=16)

    # footer
    foot = ("Sources: Sensor Tower / Deadline · India Today / ANI · BBC · Reuters / AP · "
            "WSJ · Times of India  —  All stories reported on Friday 20 November 2026")
    ff = font(SANS, 13)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 958), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
