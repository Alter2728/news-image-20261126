#!/usr/bin/env python3
"""Render entry.png: a one-page picture of world news on Thursday 26 November 2026."""
import os
from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(HERE, "entry.png")

NAVY = (16, 24, 40)
PAPER = (250, 247, 240)
GOLD = (255, 203, 74)
RED = (196, 38, 38)
BLUE = (28, 88, 158)
PURPLE = (118, 58, 142)
INK = (24, 28, 36)
GREY = (58, 62, 70)
WHITE = (255, 255, 255)


def pick_font(px, heavy=False):
    candidates = []
    if heavy:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        ]
    else:
        candidates = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, px)
    return ImageFont.load_default()


def wrapped(draw, text, face, limit):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=face) <= limit:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def put_text(draw, x, y, text, face, colour, limit, step):
    for line in wrapped(draw, text, face, limit):
        draw.text((x, y), line, font=face, fill=colour)
        y += step
    return y


def panel(draw, box, band_colour, kicker):
    x0, y0, x1, y1 = box
    draw.rectangle(box, outline=NAVY, width=4)
    draw.rectangle([x0, y0, x1, y0 + 40], fill=band_colour)
    draw.text((x0 + 16, y0 + 7), kicker, font=pick_font(22, True), fill=WHITE)


canvas = Image.new("RGB", (SIZE, SIZE), PAPER)
pen = ImageDraw.Draw(canvas)

# Masthead: the date must be unmissable.
pen.rectangle([0, 0, SIZE, 146], fill=NAVY)
pen.text((30, 14), "WORLD NEWS IN ONE IMAGE", font=pick_font(46, True), fill=WHITE)
pen.text((30, 76), "Thursday 26 November 2026", font=pick_font(38, True), fill=GOLD)
pen.rectangle([0, 146, SIZE, 156], fill=RED)

# Lead: Washington tariffs.
panel(pen, [22, 168, 1002, 398], NAVY, "1  TRADE  -  WASHINGTON")
y = put_text(pen, 40, 220, "US proposes new tariffs on 14 partners", pick_font(38, True), INK, 600, 44)
y = put_text(pen, 40, y + 6, "China, EU, India, Japan targeted. Rates about 15-35%.", pick_font(25), GREY, 600, 31)
for idx, shade in enumerate([RED, BLUE, (238, 158, 28)]):
    top = 322 - idx * 40
    pen.rectangle([676 + idx * 10, top, 956 + idx * 10, top + 36], fill=shade, outline=NAVY, width=2)
    for rib in range(5):
        rx = 696 + idx * 10 + rib * 52
        pen.line([rx, top, rx, top + 36], fill=WHITE, width=2)
pen.ellipse([742, 216, 852, 326], fill=GOLD, outline=NAVY, width=4)
pen.text((776, 240), "%", font=pick_font(64, True), fill=NAVY)
pen.text((664, 362), "China 20%  -  Vietnam 35%", font=pick_font(21, True), fill=RED)

# Left middle: Kyiv strikes and the Brussels row.
panel(pen, [22, 410, 502, 694], BLUE, "2  WAR & EUROPE")
y = put_text(pen, 40, 462, "Missiles hit Kyiv; EU clashes over aid", pick_font(30, True), INK, 444, 36)
y = put_text(pen, 40, y + 4, "113 drones + missiles; mall hit, 7 hurt. Brussels rows over budget and Ukraine aid.", pick_font(22), GREY, 444, 28)
for bx, bh in [(56, 30), (116, 48), (186, 26), (256, 52), (336, 34), (406, 42)]:
    pen.rectangle([bx, 688 - bh, bx + 44, 688], fill=(92, 112, 142))
pen.arc([70, 616, 470, 692], start=195, end=335, fill=RED, width=5)
pen.ellipse([252, 626, 272, 646], fill=RED)

# Right middle: Cairo tanker fire.
panel(pen, [514, 410, 1002, 694], RED, "3  DISASTER  -  CAIRO")
y = put_text(pen, 532, 462, "Tanker fire kills 31 on Ring Road", pick_font(30, True), INK, 444, 36)
y = put_text(pen, 532, y + 4, "Fuel tanker overturned in Giza and burned; 21 injured. Driver detained.", pick_font(22), GREY, 444, 28)
pen.rectangle([566, 640, 884, 672], fill=(64, 64, 64))
pen.ellipse([604, 656, 640, 690], fill=(18, 18, 18))
pen.ellipse([806, 656, 842, 690], fill=(18, 18, 18))
for fx, fh, fc in [(606, 46, (238, 120, 20)), (686, 60, RED), (766, 42, GOLD), (836, 52, (238, 120, 20))]:
    pen.polygon([(fx, 642), (fx + 24, 642 - fh), (fx + 48, 642)], fill=fc)
pen.text((886, 600), "31 dead", font=pick_font(24, True), fill=RED)

# Bottom wide: Gulf escalation.
panel(pen, [22, 706, 1002, 902], PURPLE, "4  MIDDLE EAST  -  GULF & HORMUZ")
y = put_text(pen, 40, 758, "Gulf escalation: refinery claim, mines, drone deaths", pick_font(30, True), INK, 620, 36)
y = put_text(pen, 40, y + 4, "Houthis claim Ras Tanura strike. Mines reported near Hormuz. Two Italians killed in Kuwait.", pick_font(23), GREY, 620, 29)
pen.polygon([(702, 848), (964, 848), (922, 882), (732, 882)], fill=BLUE)
pen.rectangle([742, 816, 922, 848], fill=RED)
pen.rectangle([852, 782, 882, 816], fill=(64, 64, 64))
pen.text((702, 756), "HORMUZ", font=pick_font(26, True), fill=PURPLE)
pen.line([692, 890, 972, 890], fill=BLUE, width=4)

# Ticker: the rest of the day in short labels.
pen.rectangle([0, 914, SIZE, SIZE], fill=NAVY)
pen.text((30, 924), "ALSO ON 26 NOV:", font=pick_font(24, True), fill=GOLD)
put_text(pen, 30, 956, "Ebola cases pass 12,000 in DR Congo  -  SpaceX cleared for up to 1M satellites  -  Macy's parade postponed in storm  -  Diesel tanker capsizes off Ibiza", pick_font(21), WHITE, 964, 26)

canvas.save(TARGET, optimize=True)
print("saved", TARGET, os.path.getsize(TARGET), "bytes")
