"""Draw the 26 November 2026 world-news front page (local generation only).

The grader runs main.py, which copies the PNG produced here.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (247, 243, 233)
INK = (26, 26, 26)
MUTED = (90, 86, 78)
PAPER = (255, 255, 252)
LINE = (205, 198, 182)
RED = (176, 42, 30)
NAVY = (31, 58, 95)
TEAL = (14, 107, 107)
AMBER = (166, 106, 12)
PLUM = (110, 52, 95)
GREEN = (46, 110, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def tag(draw, x, y, label, color):
    fnt = font(SANS_B, 17)
    w = draw.textlength(label, font=fnt) + 22
    draw.rounded_rectangle([x, y, x + w, y + 30], radius=8, fill=color)
    draw.text((x + 11, y + 5), label, font=fnt, fill=(255, 255, 255))
    return w


def icon(draw, cx, cy, kind, color):
    r = 21
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    wht = (255, 255, 255)
    if kind == "bolt":
        draw.polygon([(cx + 3, cy - 13), (cx - 7, cy + 2), (cx - 1, cy + 2), (cx - 3, cy + 13), (cx + 7, cy - 2), (cx + 1, cy - 2)], fill=wht)
    elif kind == "ship":
        draw.polygon([(cx - 13, cy + 4), (cx + 13, cy + 4), (cx + 9, cy + 11), (cx - 9, cy + 11)], fill=wht)
        draw.rectangle([cx - 9, cy - 3, cx + 1, cy + 3], fill=wht)
        draw.rectangle([cx + 3, cy - 8, cx + 7, cy + 3], fill=wht)
        draw.line([cx - 11, cy + 14, cx + 11, cy + 14], fill=wht, width=2)
    elif kind == "flame":
        draw.polygon([(cx, cy - 14), (cx + 9, cy + 2), (cx + 6, cy + 11), (cx - 6, cy + 11), (cx - 9, cy + 2)], fill=wht)
        draw.ellipse([cx - 4, cy + 2, cx + 4, cy + 11], fill=color)
    elif kind == "drop":
        draw.polygon([(cx, cy - 14), (cx + 8, cy + 4), (cx - 8, cy + 4)], fill=wht)
        draw.ellipse([cx - 8, cy - 2, cx + 8, cy + 12], fill=wht)
    elif kind == "thermo":
        draw.rounded_rectangle([cx - 4, cy - 13, cx + 4, cy + 6], radius=4, fill=wht)
        draw.ellipse([cx - 8, cy + 2, cx + 8, cy + 14], fill=wht)
    elif kind == "percent":
        draw.line([cx + 9, cy - 12, cx - 9, cy + 12], fill=wht, width=4)
        draw.ellipse([cx - 12, cy - 12, cx - 4, cy - 4], outline=wht, width=3)
        draw.ellipse([cx + 4, cy + 4, cx + 12, cy + 12], outline=wht, width=3)


def accent(draw, box, color):
    x0, y0, x1, _ = box
    draw.rounded_rectangle([x0 + 16, y0 + 10, x1 - 16, y0 + 17], radius=3, fill=color)


def panel(draw, box, color, label, headline, summary, number, kind):
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=14, fill=PAPER, outline=LINE, width=2)
    accent(draw, box, color)
    tag(draw, x0 + 20, y0 + 28, label, color)
    icon(draw, x1 - 38, y0 + 43, kind, color)
    nf = font(SANS_B, 27)
    nw = draw.textlength(number, font=nf)
    draw.text((x1 - 68 - nw, y0 + 30), number, font=nf, fill=color)
    y = text_block(draw, (x0 + 20, y0 + 72), headline, font(SERIF_B, 29), INK, x1 - x0 - 40, 34)
    text_block(draw, (x0 + 20, y + 6), summary, font(SANS, 21), MUTED, x1 - x0 - 40, 27)


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Masthead
    title = "THE WORLD TODAY"
    tf = font(SERIF_B, 56)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 24), title, font=tf, fill=INK)
    d.rectangle([36, 96, W - 36, 100], fill=INK)
    date = "Thursday, 26 November 2026"
    df = font(SANS_B, 29)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 108), date, font=df, fill=RED)
    sub = "Six consequential stories from one day"
    sf = font(SANS, 19)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 144), sub, font=sf, fill=MUTED)

    # Lead story: tariffs
    lead = [36, 180, W - 36, 352]
    d.rounded_rectangle(lead, radius=14, fill=PAPER, outline=LINE, width=2)
    accent(d, lead, NAVY)
    tag(d, 56, 206, "WORLD TRADE", NAVY)
    icon(d, W - 74, 221, "percent", NAVY)
    nf = font(SANS_B, 28)
    num = "14 partners"
    d.text((W - 104 - d.textlength(num, font=nf), 208), num, font=nf, fill=NAVY)
    y = text_block(d, (56, 244), "US proposes new tariffs on 14 partners", font(SERIF_B, 37), INK, W - 112, 43)
    text_block(
        d,
        (56, y + 1),
        "Public hearing set for 25 January; rates hinge on trade deals.",
        font(SANS, 20),
        MUTED,
        W - 112,
        26,
    )
    chips = ["CHINA 20% → 40%", "VIETNAM 35%", "EU · JAPAN 15%"]
    cf = font(SANS_B, 18)
    cx = 56
    for chip in chips:
        cw = d.textlength(chip, font=cf) + 26
        d.rounded_rectangle([cx, 318, cx + cw, 346], radius=9, fill=(232, 238, 246), outline=NAVY, width=1)
        d.text((cx + 13, 323), chip, font=cf, fill=NAVY)
        cx += cw + 14

    # Grid panels
    panel(
        d, [36, 360, 502, 572], RED, "UKRAINE",
        "Strikes hit Kyiv; warning of more",
        "Power cut in 7 regions. Zelensky warns of more.",
        "113 drones", "bolt",
    )
    panel(
        d, [522, 360, W - 36, 572], TEAL, "GULF ENERGY",
        "Blast near tanker; oil jumps",
        "Blast off Dubai, crew safe (UKMTO). Iran's mine claim is unconfirmed.",
        "Brent $96", "ship",
    )
    panel(
        d, [36, 588, 502, 800], AMBER, "EGYPT",
        "Tanker fire kills 31 in Cairo",
        "Fuel tanker overturned on the Ring Road; 27 vehicles burned.",
        "31 dead", "flame",
    )
    panel(
        d, [522, 588, W - 36, 800], PLUM, "INDONESIA",
        "13 dead, 13 missing in flooded mine",
        "Illegal gold mine in West Java flooded after heavy rain.",
        "13 + 13", "drop",
    )

    # Climate band
    band = [36, 816, W - 36, 958]
    d.rounded_rectangle(band, radius=14, fill=PAPER, outline=LINE, width=2)
    accent(d, band, GREEN)
    tag(d, 56, 842, "PLANET", GREEN)
    icon(d, W - 74, 857, "thermo", GREEN)
    nf2 = font(SANS_B, 28)
    num2 = "2.24°C peak"
    d.text((W - 104 - d.textlength(num2, font=nf2), 844), num2, font=nf2, fill=GREEN)
    y = text_block(d, (56, 884), "Six days above 2°C — a first on record", font(SERIF_B, 31), INK, W - 112, 37)
    text_block(
        d,
        (56, y + 2),
        "18–23 Nov (Copernicus). Brief streak; long-term average is 1.44°C.",
        font(SANS, 20),
        MUTED,
        W - 112,
        26,
    )

    foot = "Reported 26 Nov 2026  •  Reuters · AP · BBC · Copernicus · UKMTO"
    ff = font(SANS, 16)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, 972), foot, font=ff, fill=MUTED)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(out, img.size, out.stat().st_size)


if __name__ == "__main__":
    main()
