from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path("/Users/lizi/Desktop/AI内容-obsidian")
OUT = ROOT / "02-稿件库/01-创作中稿件/影响力金句分享-images"
SRC_DIR = Path("/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397")

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"

BACKGROUND_FILES = [
    "ig_02a0a2e7064dd5d8016a3a59bee7c08191878981952cece9cb.png",
    "ig_02a0a2e7064dd5d8016a3a59ff3a208191bd50cfa68933a8bf.png",
    "ig_02a0a2e7064dd5d8016a3a5a2c67588191b6c566e2567f8645.png",
    "ig_02a0a2e7064dd5d8016a3a5a899084819186385c8686ecd709.png",
]


def crop_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    src_w, src_h = img.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = img.resize((round(src_w * scale), round(src_h * scale)), Image.LANCZOS)
    left = max(0, (resized.width - dst_w) // 2)
    top = max(0, (resized.height - dst_h) // 2)
    return resized.crop((left, top, left + dst_w, top + dst_h))


def fit_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    src_w, src_h = img.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = img.resize((round(src_w * scale), round(src_h * scale)), Image.LANCZOS)
    left = max(0, (resized.width - dst_w) // 2)
    top = max(0, (resized.height - dst_h) // 2)
    return resized.crop((left, top, left + dst_w, top + dst_h))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def text_width(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=fnt)
    return box[2] - box[0]


def wrap_cn(text: str, draw: ImageDraw.ImageDraw, fnt: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    lines: list[str] = []
    current = ""
    for ch in text:
        trial = current + ch
        if current and text_width(draw, trial, fnt) > max_width:
            lines.append(current)
            current = ch
        else:
            current = trial
    if current:
        lines.append(current)
    return lines


def add_scrim(base: Image.Image, box: tuple[int, int, int, int], radius: int, fill: tuple[int, int, int, int]) -> None:
    overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rounded_rectangle(box, radius=radius, fill=fill)
    base.alpha_composite(overlay)


def draw_multiline(
    draw: ImageDraw.ImageDraw,
    lines: list[str],
    xy: tuple[int, int],
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    line_gap: int,
    align: str = "left",
    max_width: int | None = None,
) -> int:
    x, y = xy
    for line in lines:
        line_w = text_width(draw, line, fnt)
        dx = x
        if align == "center" and max_width is not None:
            dx = x + (max_width - line_w) // 2
        draw.text((dx, y), line, font=fnt, fill=fill)
        bbox = draw.textbbox((dx, y), line, font=fnt)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def render_cover(src: Path, out: Path) -> None:
    img = crop_cover(Image.open(src).convert("RGB"), (900, 383)).convert("RGBA")
    draw = ImageDraw.Draw(img)
    add_scrim(img, (54, 45, 615, 322), 28, (255, 250, 238, 218))

    draw.text((82, 72), "《影响力》金句分享", font=font(28, True), fill=(38, 69, 71, 255))

    title = "真正的影响力，\n是让自己活得更清醒"
    y = 126
    for line in title.split("\n"):
        draw.text((82, y), line, font=font(46, True), fill=(36, 42, 43, 255))
        y += 60

    draw.text((84, 266), "愿你温柔待人，也清醒地保护自己", font=font(24), fill=(91, 78, 56, 255))
    draw.line((84, 305, 322, 305), fill=(221, 165, 78, 255), width=4)
    img.convert("RGB").save(out, quality=96)


def render_card(src: Path, out: Path, index: str, quote: str, footer: str, accent: tuple[int, int, int]) -> None:
    img = fit_cover(Image.open(src).convert("RGB"), (900, 1200)).convert("RGBA")
    # Gentle blur under the text area to keep the background visible but readable.
    blurred = img.filter(ImageFilter.GaussianBlur(10))
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((70, 110, 830, 690), radius=34, fill=190)
    img = Image.composite(blurred, img, mask).convert("RGBA")
    add_scrim(img, (70, 110, 830, 690), 34, (255, 251, 241, 214))

    draw = ImageDraw.Draw(img)
    draw.text((105, 152), index, font=font(32, True), fill=(*accent, 255))
    draw.line((105, 206, 250, 206), fill=(*accent, 255), width=5)

    quote_font = font(43, True)
    lines = quote.split("\n") if "\n" in quote else wrap_cn(quote, draw, quote_font, 660)
    draw_multiline(draw, lines, (118, 265), quote_font, (35, 42, 43, 255), 22)

    draw.text((118, 620), footer, font=font(25), fill=(82, 79, 69, 255))
    add_scrim(img, (88, 1015, 705, 1128), 24, (24, 43, 43, 118))
    draw.text((118, 1040), "真正的影响力，是让善意更有方向", font=font(28, True), fill=(255, 255, 248, 255))
    draw.text((118, 1088), "《影响力》个人成长金句", font=font(22), fill=(255, 255, 248, 230))
    img.convert("RGB").save(out, quality=96)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name in BACKGROUND_FILES:
        shutil.copy2(SRC_DIR / name, OUT / f"background-{BACKGROUND_FILES.index(name) + 1}.png")

    render_cover(SRC_DIR / BACKGROUND_FILES[0], OUT / "01-cover-900x383.png")
    render_card(
        SRC_DIR / BACKGROUND_FILES[1],
        OUT / "02-quote-growth-900x1200.png",
        "01 / 清醒成长",
        "真正的成长，不是突然变成另一个人，\n而是在自己的坐标系里，\n慢慢把日子过得更有力量。",
        "少一点比较别人，多一点看见自己。",
        (33, 111, 119),
    )
    render_card(
        SRC_DIR / BACKGROUND_FILES[2],
        OUT / "03-quote-boundary-900x1200.png",
        "02 / 边界感",
        "你的原则不需要向所有人解释。\n越早说“不”，\n越能保护真正重要的“是”。",
        "温柔不是没有锋芒，善良也需要边界。",
        (121, 97, 49),
    )
    render_card(
        SRC_DIR / BACKGROUND_FILES[3],
        OUT / "04-quote-communication-900x1200.png",
        "03 / 清晰表达",
        "清晰表达不是麻烦别人，\n而是给别人一个真正靠近你的入口。",
        "把请求说具体，关系才有机会变轻。",
        (32, 103, 105),
    )


if __name__ == "__main__":
    main()
