#!/usr/bin/env python3
from io import BytesIO
from pathlib import Path

import cairosvg
from PIL import Image, ImageDraw, ImageFont


WIDTH = 1200
HEIGHT = 630

ROOT = Path(__file__).resolve().parents[1]
SVG_PATH = ROOT / "og-image.svg"
PNG_PATH = ROOT / "og-image.png"
FONT_PATH = ROOT / "fonts" / "KyoboHandwriting2019.otf"

COLORS = {
    "paper": (250, 246, 236),
    "ruling": (239, 233, 216),
    "ink": (42, 40, 35),
    "pencil": (58, 53, 44),
    "red": (200, 65, 44),
    "blue": (47, 95, 168),
    "warm": (192, 184, 158),
    "muted": (168, 160, 135),
}


def quantize_to_brand_palette(image):
    palette_image = Image.new("P", (1, 1))
    palette = []
    for rgb in COLORS.values():
        palette.extend(rgb)
    palette.extend([0, 0, 0] * (256 - len(COLORS)))
    palette_image.putpalette(palette)
    return image.quantize(palette=palette_image, dither=Image.Dither.NONE).convert("RGB")


def main():
    png_bytes = cairosvg.svg2png(url=str(SVG_PATH), output_width=WIDTH, output_height=HEIGHT)
    image = Image.open(BytesIO(png_bytes)).convert("RGB")
    draw = ImageDraw.Draw(image)

    font_logo = ImageFont.truetype(str(FONT_PATH), 160)
    font_ko = ImageFont.truetype(str(FONT_PATH), 90)
    font_tagline = ImageFont.truetype(str(FONT_PATH), 46)
    font_intro = ImageFont.truetype(str(FONT_PATH), 31)

    draw.text((102, 70), "peppinch", font=font_logo, fill=COLORS["ink"])
    draw.text((112, 280), "한 꼬집의 후추.", font=font_ko, fill=COLORS["red"])
    draw.text((112, 420), "A Pinch Of Pepper.", font=font_tagline, fill=COLORS["pencil"])
    draw.text(
        (112, 512),
        "이런 거 왜 없지 싶은 걸, 한 꼬집씩 만들고, 관심있는 것들을 한꼬집씩 적어봅니다",
        font=font_intro,
        fill=COLORS["pencil"],
    )

    image = quantize_to_brand_palette(image)
    image.save(PNG_PATH, optimize=True)
    print(f"rendered {PNG_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
