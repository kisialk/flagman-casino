"""Generate Flagman Casino favicon pack."""
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "-q"])
    from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent
ICONS = ROOT / "assets" / "icons"
BG = (31, 41, 55)  # #1f2937
RED = (255, 59, 59)
GOLD = (255, 209, 102)


def draw_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), BG + (255,))
    d = ImageDraw.Draw(img)
    margin = max(2, size // 8)
    d.rounded_rectangle(
        [margin, margin, size - margin, size - margin],
        radius=max(2, size // 6),
        fill=(37, 47, 63, 255),
        outline=GOLD + (255,),
        width=max(1, size // 32),
    )
    font_size = int(size * 0.55)
    try:
        font = ImageFont.truetype("arialbd.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()
    text = "F"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text(
        ((size - tw) / 2, (size - th) / 2 - size * 0.05),
        text,
        fill=RED + (255,),
        font=font,
    )
    return img


def save_png(img: Image.Image, path: Path):
    img.convert("RGB").save(path, format="PNG", optimize=True)


def main():
    ICONS.mkdir(parents=True, exist_ok=True)
    source = draw_icon(512)
    save_png(source, ICONS / "favicon-source.png")

    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "apple-touch-icon.png": 180,
        "android-chrome-192x192.png": 192,
        "android-chrome-512x512.png": 512,
    }
    for name, sz in sizes.items():
        save_png(source.resize((sz, sz), Image.Resampling.LANCZOS), ROOT / name)

    ico = source.resize((32, 32), Image.Resampling.LANCZOS).convert("RGBA")
    ico.save(ROOT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32)])
    print("Favicons generated.")


if __name__ == "__main__":
    main()
