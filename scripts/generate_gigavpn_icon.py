#!/usr/bin/env python3
"""Generate GigaVPN launcher artwork (requires Pillow).

Run from the repository root:
    python3 scripts/generate_gigavpn_icon.py

The script is deterministic and overwrites the branded resources only.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "app" / "src" / "main" / "res"

DARK = (18, 8, 33, 255)
PURPLE = (155, 81, 224, 255)
LIGHT_PURPLE = (168, 85, 247, 255)
WHITE = (246, 240, 255, 255)


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient_background(size: int) -> Image.Image:
    image = Image.new("RGBA", (size, size), DARK)
    draw = ImageDraw.Draw(image)
    for y in range(size):
        t = y / max(size - 1, 1)
        color = (
            lerp(38, 14, t),
            lerp(18, 7, t),
            lerp(66, 28, t),
            255,
        )
        draw.line((0, y, size, y), fill=color)
    return image


def load_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_shield(image: Image.Image, size: int) -> None:
    draw = ImageDraw.Draw(image)
    s = size / 1024.0
    # Shield: top edge -> shoulders -> pointed bottom.
    shield = [
        (512 * s, 110 * s),
        (855 * s, 250 * s),
        (855 * s, 560 * s),
        (512 * s, 900 * s),
        (169 * s, 560 * s),
        (169 * s, 250 * s),
    ]
    # Soft purple shadow/glow, then the main shield body.
    draw.polygon([(x + 10 * s, y + 14 * s) for x, y in shield], fill=(90, 40, 150, 110))
    draw.polygon(shield, fill=PURPLE, outline=WHITE, width=max(2, int(16 * s)))
    inner = [
        (512 * s, 168 * s),
        (795 * s, 284 * s),
        (795 * s, 540 * s),
        (512 * s, 818 * s),
        (229 * s, 540 * s),
        (229 * s, 284 * s),
    ]
    draw.polygon(inner, fill=(123, 62, 196, 255))

    font = load_font(int(520 * s))
    draw.text((512 * s, 486 * s), "G", font=font, fill=WHITE, anchor="mm")


def base_icon(size: int) -> Image.Image:
    image = gradient_background(size)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, size - 1, size - 1), radius=int(size * 0.22), fill=255
    )
    background = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    background.paste(image, (0, 0), mask)
    draw_shield(background, size)
    return background


def round_icon(size: int) -> Image.Image:
    image = gradient_background(size)
    draw_shield(image, size)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    result = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    result.paste(image, (0, 0), mask)
    return result


def save_webp(image: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGBA").save(path, format="WEBP", quality=92, method=6)


def main() -> None:
    densities = {
        "mipmap-mdpi": 48,
        "mipmap-hdpi": 72,
        "mipmap-xhdpi": 96,
        "mipmap-xxhdpi": 144,
        "mipmap-xxxhdpi": 192,
    }
    for folder, size in densities.items():
        target = RES / folder
        save_webp(base_icon(size), target / "ic_launcher.webp")
        save_webp(round_icon(size), target / "ic_launcher_round.webp")

    artwork = base_icon(512)
    nodpi = RES / "drawable-nodpi"
    nodpi.mkdir(parents=True, exist_ok=True)
    artwork.save(nodpi / "gigavpn_launcher_icon.png")

    notification = round_icon(96)
    draw = ImageDraw.Draw(notification)
    draw.ellipse((8, 8, 88, 88), outline=LIGHT_PURPLE, width=5)
    notification.save(RES / "drawable-xxxhdpi" / "ic_notification.png")

    banner = Image.new("RGBA", (640, 360), DARK)
    draw = ImageDraw.Draw(banner)
    for y in range(360):
        t = y / 359
        draw.line(
            (0, y, 640, y),
            fill=(lerp(38, 14, t), lerp(18, 7, t), lerp(66, 28, t), 255),
        )
    shield_art = base_icon(260)
    banner.alpha_composite(shield_art, (36, 50))
    draw.text((340, 166), "GigaVPN", font=load_font(62), fill=WHITE, anchor="mm")
    draw.text((340, 220), "Secure by design", font=load_font(27), fill=LIGHT_PURPLE, anchor="mm")
    banner.save(RES / "drawable-xhdpi" / "tv_banner.png")

    print("GigaVPN icons written to", RES)


if __name__ == "__main__":
    main()
