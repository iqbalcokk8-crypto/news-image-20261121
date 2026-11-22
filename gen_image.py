#!/usr/bin/env python3
"""Draw entry.png for news-image-20261121 (Saturday 21 November 2026).

Newspaper front page, 1024x1024, drawn entirely with PIL primitives:
no AI image generator, no copyrighted images, no network, no randomness,
no timestamps. Output bytes are deterministic for the same source.

Run:  python3 gen_image.py            # writes entry.png beside this file
"""

import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

PAPER = (247, 242, 231)
INK = (20, 20, 20)
MUTED = (90, 84, 72)
RED = (178, 34, 22)
NAVY = (20, 38, 63)
GOLD = (176, 124, 24)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
LINE = (200, 192, 172)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
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


def draw_wrapped(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def letterspaced(draw, xy, text, fnt, fill, gap=4):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + gap
    return x


def starburst(draw, cx, cy, r, fill):
    pts = []
    for i in range(24):
        ang = math.pi * i / 12
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def globe(draw, cx, cy, r, outline, width=3):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=outline, width=width)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=outline, width=2)
    draw.line([cx - r, cy, cx + r, cy], fill=outline, width=2)
    draw.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5],
             start=200, end=340, fill=outline, width=2)
    draw.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5],
             start=20, end=160, fill=outline, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---------------- masthead (y 24..206) ----------------
    y = 24
    letterspaced(d, (mx, y), "MAKE.FUN  ·  ONE DAY IN ONE IMAGE",
                 font(SANS_B, 17), MUTED, gap=3)
    y += 28
    d.text((mx, y), "WORLD NEWS", font=font(SERIF_B, 78), fill=INK)
    y += 96
    d.rectangle([mx, y, W - mx, y + 5], fill=RED)
    y += 14
    d.text((mx, y), "SATURDAY, 21 NOVEMBER 2026",
           font=font(SANS_B, 32), fill=RED)
    d.text((W - mx - d.textlength("7 STORIES · 1 DAY",
                                  font=font(SANS_B, 19)), y + 7),
           "7 STORIES · 1 DAY", font=font(SANS_B, 19), fill=MUTED)
    y += 46
    d.line([mx, y, W - mx, y], fill=LINE, width=2)

    # ---------------- lead: Iran strikes Bahrain (y 218..454) ----------------
    ly = y + 12
    lh = 236
    d.rectangle([mx, ly, W - mx, ly + lh], fill=NAVY)
    d.rectangle([mx, ly, W - mx, ly + 6], fill=RED)
    starburst(d, W - mx - 88, ly + 112, 70, (232, 126, 32))
    starburst(d, W - mx - 88, ly + 112, 38, (240, 196, 90))
    tx = mx + 24
    letterspaced(d, (tx, ly + 20), "MIDDLE EAST  ·  LEAD STORY",
                 font(SANS_B, 17), (240, 196, 90), gap=3)
    d.text((tx, ly + 48), "IRAN SAYS IT HIT",
           font=font(SERIF_B, 44), fill=WHITE)
    d.text((tx, ly + 96), "U.S. BASES IN BAHRAIN",
           font=font(SERIF_B, 44), fill=WHITE)
    lead_sum = ("Tehran claims strikes on two U.S. positions; Bahrain says a "
                "civilian site burned, no one was hurt, and its defences "
                "intercepted the rest.")
    lines = wrap(d, lead_sum, font(SANS, 20), W - mx - tx - 210)
    draw_wrapped(d, (tx, ly + 156), lines, font(SANS, 20), (225, 228, 235), 27)
    d.text((tx, ly + lh - 28), "REUTERS  ·  ONE TURN  ·  21 NOV 2026",
           font=font(SANS_B, 14), fill=(170, 180, 195))

    # ---------------- 2x2 grid (y 468..818) ----------------
    gy = ly + lh + 14
    gw = (W - 2 * mx - 16) // 2
    gh = 168
    cards = [
        ("LATIN AMERICA  ·  MEXICO", "MEXICO CAPTURES",
         "'EL CHAPO ISIDRO'",
         "FBI most-wanted cartel boss seized in Sinaloa; at least 11 dead "
         "as violence followed.",
         "REUTERS  ·  AP  ·  CNN", RED, "star"),
        ("EUROPE  ·  UKRAINE", "MISSILE HITS",
         "ZELENSKYY'S HOMETOWN",
         "A Russian strike on Kryvyi Rih killed a boy, 7, and a paramedic; "
         "dozens wounded.",
         "REUTERS  ·  CNN  ·  ISW", NAVY, "burst"),
        ("GLOBAL  ·  CLIMATE", "COP31 CLOSE TO",
         "A DEAL — AT LAST",
         "Antalya talks ran past deadline over fossil fuels; the president "
         "says a final deal is close.",
         "REUTERS", (34, 84, 60), "globe"),
        ("GLOBAL  ·  MARKETS", "AI SELL-OFF ERASES",
         "2026 GAINS",
         "Nasdaq fell 5.3% in its worst week since March 2020; the S&P 500 "
         "entered correction.",
         "SENTINEL  ·  HORIZON", GOLD, "chart"),
    ]
    for i, (kick, h1, h2, summ, src, color, icon) in enumerate(cards):
        cx = mx + (i % 2) * (gw + 16)
        cy = gy + (i // 2) * (gh + 14)
        d.rectangle([cx, cy, cx + gw, cy + gh], fill=CARD,
                    outline=LINE, width=2)
        d.rectangle([cx, cy, cx + 8, cy + gh], fill=color)
        letterspaced(d, (cx + 22, cy + 11), kick, font(SANS_B, 14), color,
                     gap=2)
        d.text((cx + 22, cy + 34), h1, font=font(SERIF_B, 28), fill=INK)
        d.text((cx + 22, cy + 67), h2, font=font(SERIF_B, 28), fill=INK)
        sl = wrap(d, summ, font(SANS, 16), gw - 44)
        assert len(sl) <= 2, (kick, sl)
        draw_wrapped(d, (cx + 22, cy + 104), sl, font(SANS, 16),
                     (60, 58, 52), 21)
        d.text((cx + 22, cy + gh - 22), src, font=font(SANS_B, 12), fill=MUTED)
        ix, iy = cx + gw - 52, cy + 13
        if icon == "star":
            starburst(d, ix + 16, iy + 16, 17, color)
        elif icon == "burst":
            starburst(d, ix + 16, iy + 16, 15, color)
            d.ellipse([ix + 9, iy + 9, ix + 23, iy + 23], fill=WHITE)
        elif icon == "globe":
            globe(d, ix + 16, iy + 16, 15, color)
        elif icon == "chart":
            d.line([ix, iy + 26, ix + 11, iy + 16, ix + 20, iy + 21,
                    ix + 32, iy + 4], fill=color, width=4)
            d.polygon([(ix + 32, iy + 4), (ix + 22, iy + 4), (ix + 32, iy + 14)],
                      fill=color)

    # ---------------- bottom strip (y 832..944) ----------------
    by = gy + 2 * gh + 14 + 14
    bh = 112
    bw = (W - 2 * mx - 16) // 2
    strip = [
        ("GULF OF FINLAND", "RUSSIAN SHIP ABLAZE",
         "The Sparta II burned after a drone strike; its crew evacuated as "
         "it drifted into Finnish waters.",
         "REUTERS", NAVY),
        ("HEALTH  ·  BRAZIL  —  A HOPEFUL NOTE",
         "DENGUE CUT BY 69% IN CHILDREN",
         "Specially bred mosquitoes cut dengue in children by about "
         "two-thirds in a major study.",
         "ASSOCIATED PRESS", (34, 110, 60)),
    ]
    for i, (kick, head, summ, src, color) in enumerate(strip):
        sx = mx + i * (bw + 16)
        d.rectangle([sx, by, sx + bw, by + bh], fill=CARD,
                    outline=LINE, width=2)
        d.rectangle([sx, by, sx + bw, by + 5], fill=color)
        letterspaced(d, (sx + 18, by + 13), kick, font(SANS_B, 13), color,
                     gap=2)
        hl = wrap(d, head, font(SERIF_B, 19), bw - 36)
        assert len(hl) == 1, (kick, hl)
        d.text((sx + 18, by + 35), hl[0], font=font(SERIF_B, 19), fill=INK)
        sl = wrap(d, summ, font(SANS, 15), bw - 36)
        assert len(sl) <= 2, (kick, sl)
        draw_wrapped(d, (sx + 18, by + 62), sl, font(SANS, 15),
                     (60, 58, 52), 20)

    # ---------------- footer (y 956..1006) ----------------
    fy = by + bh + 12
    d.line([mx, fy, W - mx, fy], fill=LINE, width=2)
    d.text((mx, fy + 9),
           "Sources: Reuters · Associated Press · CNN · Institute for the Study "
           "of War · UKMTO",
           font=font(SANS, 15), fill=MUTED)
    d.text((mx, fy + 31),
           "All events of Saturday 21 November 2026. Drawn entirely with code.",
           font=font(SANS_B, 15), fill=INK)

    img.save(OUT, format="PNG")
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
