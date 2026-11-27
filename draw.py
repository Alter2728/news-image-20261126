"""Generate entry.png: a 1024x1024 newspaper front page.

Summarises world news from Thursday, 26 November 2026 in six short
stories. This script is a local build tool only; the submitted entry
runs main.py, which copies the finished entry.png.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
MARGIN = 36
BG = (247, 243, 234)
INK = (28, 28, 30)
MUTED = (92, 86, 78)
ACCENT = (165, 38, 32)
RULE = (28, 28, 30)
FAINT = (196, 188, 172)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts",
]


def load_font(candidates, size):
    for name in candidates:
        for folder in FONT_DIRS:
            path = Path(folder) / name
            if path.is_file():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default(size=size)


SERIF_BOLD = ["DejaVuSerif-Bold.ttf", "LiberationSerif-Bold.ttf"]
SERIF = ["DejaVuSerif.ttf", "LiberationSerif-Regular.ttf"]
SANS_BOLD = ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]
SANS = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]

STORIES = [
    (
        "1 · TRADE — WASHINGTON",
        "U.S. Weighs New Tariffs on 14 Partners",
        "Washington proposed Section 301 duties, including 20% on China "
        "rising to 40% if the truce ends, 35% on Vietnam and 15% on "
        "the EU and Japan. A hearing is set for 25 January.",
    ),
    (
        "2 · WAR — KYIV",
        "Missiles and Drones Hit Kyiv Overnight",
        "Strikes hit the capital and seven regions with ballistic "
        "missiles and 113 drones, cutting power in places. President "
        "Zelensky warned a larger attack was being prepared.",
    ),
    (
        "3 · ENERGY — GULF",
        "Blast Reported Near Tanker off Dubai",
        "UKMTO reported an explosion near a tanker off Dubai; the crew "
        "was safe. Iran's mine claim was unconfirmed as Brent crude "
        "held near $96 a barrel.",
    ),
    (
        "4 · EGYPT — CAIRO",
        "Fuel Tanker Fire Kills 31 in Cairo",
        "A tanker overturned on the Ring Road and burst into flames, "
        "killing 31 people and burning 27 vehicles. The driver was "
        "detained as investigators examined the crash.",
    ),
    (
        "5 · INDONESIA — BOGOR",
        "Flooded Gold Mine Leaves 13 Dead",
        "Heavy rain flooded an illegal gold mine in Bogor, West Java. "
        "Officials confirmed 13 deaths and 13 people still missing as "
        "rescue work continued.",
    ),
    (
        "6 · CLIMATE — COPERNICUS",
        "Six Days Above 2°C in Global Heat",
        "Copernicus recorded six straight days, 18–23 November, above "
        "2°C versus pre-industrial levels, peaking at 2.24°C against "
        "a 1.44°C long-term average.",
    ),
]


def wrap(draw, text, font, max_width):
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, y, text, font, fill):
    width = draw.textlength(text, font=font)
    draw.text(((SIZE - width) / 2, y), text, font=font, fill=fill)
    return y + font.size


def draw_card(draw, x, y, width, kicker, headline, summary, fonts):
    kicker_font, headline_font, body_font = fonts
    cursor = y
    draw.text((x, cursor), kicker, font=kicker_font, fill=ACCENT)
    cursor += 26
    for line in wrap(draw, headline, headline_font, width):
        draw.text((x, cursor), line, font=headline_font, fill=INK)
        cursor += 35
    cursor += 6
    for line in wrap(draw, summary, body_font, width):
        draw.text((x, cursor), line, font=body_font, fill=(52, 50, 48))
        cursor += 27
    return cursor


def main():
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)

    masthead_font = load_font(SERIF_BOLD, 66)
    date_font = load_font(SANS_BOLD, 30)
    strap_font = load_font(SERIF, 22)
    kicker_font = load_font(SANS_BOLD, 18)
    headline_font = load_font(SERIF_BOLD, 30)
    body_font = load_font(SANS, 20)
    footer_font = load_font(SANS, 17)

    draw.rectangle([14, 14, SIZE - 15, SIZE - 15], outline=INK, width=3)

    y = draw_centered(draw, 40, "THE DAILY BRIEF", masthead_font, INK)
    y = draw_centered(draw, y + 8, "Thursday, 26 November 2026", date_font, ACCENT)
    y = draw_centered(
        draw, y + 8, "Six stories that shaped the world today", strap_font, MUTED
    )

    rule_y = y + 18
    draw.line([MARGIN, rule_y, SIZE - MARGIN, rule_y], fill=RULE, width=4)
    draw.line([MARGIN, rule_y + 8, SIZE - MARGIN, rule_y + 8], fill=RULE, width=1)

    grid_top = rule_y + 26
    grid_bottom = SIZE - 64
    col_gap = 28
    col_width = (SIZE - 2 * MARGIN - col_gap) // 2
    row_height = (grid_bottom - grid_top) // 3
    fonts = (kicker_font, headline_font, body_font)

    for index, (kicker, headline, summary) in enumerate(STORIES):
        col = index % 2
        row = index // 2
        x = MARGIN + col * (col_width + col_gap)
        card_y = grid_top + row * row_height
        draw_card(draw, x, card_y, col_width, kicker, headline, summary, fonts)
        if row < 2:
            line_y = card_y + row_height - 12
            draw.line([x, line_y, x + col_width, line_y], fill=FAINT, width=1)

    mid_x = MARGIN + col_width + col_gap // 2
    draw.line([mid_x, grid_top, mid_x, grid_bottom - 8], fill=FAINT, width=1)

    footer = "Compiled from wire reports and official statements · 26 November 2026"
    draw_centered(draw, SIZE - 48, footer, footer_font, MUTED)

    out = Path(__file__).resolve().parent / "entry.png"
    image.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
