#!/usr/bin/env python3
"""Draw entry.png: a vertical-timeline summary of 25 November 2026 news.

Provenance for news-20261125-timeline (make.fun news-image-20261125).
All text is rendered with PIL + DejaVu fonts; no AI image generation.
Deterministic: fixed colours, fonts, layout and PNG save settings.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


STORIES = [
    # (number, colour, kicker, headline, summary)
    ("01", "#1B4F72", "SECURITY  |  POLAND",
     "NATO sends AWACS to Poland",
     "After three Russian missiles landed in Poland during a strike on "
     "Ukraine, NATO will forward-deploy an early-warning aircraft."),
    ("02", "#0E6655", "ENERGY  |  STRAIT OF HORMUZ",
     "Three tankers \u2018hit mines\u2019 in Hormuz",
     "Iran\u2019s Revolutionary Guard Navy says three oil tankers caught fire "
     "after striking naval mines; the claim is unverified."),
    ("03", "#7B2D26", "JUSTICE  |  FRANCE",
     "Sarkozy and Bruni ordered to trial",
     "French judges send the ex-president and his wife to trial over "
     "witness-tampering claims; first hearing 1 April 2027."),
    ("04", "#7D6608", "MARKETS  |  USA",
     "Anthropic falls below its IPO price",
     "Shares slid below the $83 IPO price, down 12.6% to $76.60, on course "
     "to erase nearly $200bn in market value."),
    ("05", "#1E8449", "TECH / BUSINESS  |  USA",
     "Dell lifts forecasts on AI boom",
     "Record quarterly revenue of $54.9bn, up 103%, as AI server orders hit "
     "$60.2bn; full-year revenue now seen at $202bn."),
    ("06", "#6C3483", "WORLD  |  GLOBAL",
     "A day to end violence against women",
     "25 November marks the UN day against violence towards women, opening "
     "16 days of activism running to 10 December."),
]


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        cur = ""
        for w_ in words:
            trial = (cur + " " + w_).strip()
            if draw.textlength(trial, font=fnt) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w_
        if cur:
            lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), "#FAF6EF")
    d = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    d.rectangle([0, 0, W, 168], fill="#0F2A44")
    d.rectangle([0, 168, W, 174], fill="#C9A227")
    f_title = font(BOLD, 66)
    f_sub = font(BOLD, 21)
    title = "25 NOVEMBER 2026"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 34),
           title, font=f_title, fill="#FFFFFF")
    sub = "W E D N E S D A Y   \u2022   T H E   D A Y   I N   S I X   M O M E N T S"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 118),
           sub, font=f_sub, fill="#E8C766")

    # ---- Timeline rail --------------------------------------------------
    rail_x = 62
    top, bottom = 196, 948
    d.line([(rail_x, top), (rail_x, bottom)], fill="#B9B2A4", width=4)

    # ---- Story bands ----------------------------------------------------
    f_num = font(BOLD, 22)
    f_kick = font(BOLD, 17)
    f_head = font(BOLD, 27)
    f_sum = font(REG, 19)
    band_h = (bottom - top) // 6
    text_x = 116
    text_w = W - text_x - 36

    for i, (num, colour, kicker, headline, summary) in enumerate(STORIES):
        y0 = top + i * band_h
        cy = y0 + band_h // 2
        # separator between bands
        if i:
            d.line([(text_x, y0), (W - 36, y0)], fill="#DDD5C4", width=2)
        # numbered marker on the rail
        d.ellipse([rail_x - 24, cy - 24, rail_x + 24, cy + 24],
                  fill=colour, outline="#FFFFFF", width=3)
        num_w = d.textlength(num, font=f_num)
        d.text((rail_x - num_w / 2, cy - 15), num, font=f_num, fill="#FFFFFF")
        # kicker
        d.text((text_x, y0 + 12), kicker, font=f_kick, fill=colour)
        # headline
        d.text((text_x, y0 + 38), headline, font=f_head, fill="#1A1A1A")
        # summary, max 2 lines
        lines = wrap(d, summary, f_sum, text_w)[:2]
        for j, line in enumerate(lines):
            d.text((text_x, y0 + 74 + j * 26), line, font=f_sum, fill="#444444")

    # ---- Footer ---------------------------------------------------------
    d.rectangle([0, 962, W, H], fill="#0F2A44")
    f_foot = font(REG, 18)
    foot = "Sources: Reuters, AP, Bloomberg  \u2022  All events of 25 November 2026"
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 982),
           foot, font=f_foot, fill="#FFFFFF")

    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {W}x{H}")


if __name__ == "__main__":
    main()
