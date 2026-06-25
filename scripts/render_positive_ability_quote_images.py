from __future__ import annotations

import shutil
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path("/Users/lizi/Desktop/AI内容-obsidian")
OUT = ROOT / "02-稿件库/01-创作中稿件/积极向上能力金句-images"
SRC_DIR = Path("/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397")

FONT_BOLD = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_REG = "/System/Library/Fonts/Hiragino Sans GB.ttc"

CARDS = [
    {
        "src": "ig_07e6ee992408d0e6016a3cf81ef01c8198af7eb6d74d99dfe7.png",
        "out": "01-growth-light-900x1200.png",
        "index": "01 / 看见成长",
        "quote": "不要只盯着够不到的地平线。\n回头看，\n你已经穿越了很多曾以为过不去的山海。",
        "footer": "每一步脚印，都是你对抗焦虑的证据。",
        "accent": (37, 112, 121),
    },
    {
        "src": "ig_07e6ee992408d0e6016a3cf866101c8198bc08a73b33996d44.png",
        "out": "02-let-go-road-900x1200.png",
        "index": "02 / 舍弃",
        "quote": "真正的成长不是收集更多，\n而是果断放下无效忙碌，\n把空间留给真正重要的事。",
        "footer": "少做一点，反而可能走得更远。",
        "accent": (130, 91, 39),
    },
    {
        "src": "ig_07e6ee992408d0e6016a3cf8aeb3b88198832879e65e53be34.png",
        "out": "03-unique-ability-900x1200.png",
        "index": "03 / 独特能力",
        "quote": "你不需要在所有赛道上赢过别人，\n只要找到自己的独特能力，\n世界就会看见你的光。",
        "footer": "把力气用在你最有价值的地方。",
        "accent": (35, 92, 111),
    },
    {
        "src": "ig_07e6ee992408d0e6016a3cf8f52014819896c0e4c4f86c906b.png",
        "out": "04-gentle-boundary-900x1200.png",
        "index": "04 / 边界感",
        "quote": "善意应当流向善意，\n但不该成为交换意志的筹码。\n守住边界，爱才更纯粹。",
        "footer": "温柔不是没有边界。",
        "accent": (112, 118, 61),
    },
    {
        "src": "ig_07e6ee992408d0e6016a3cf938fdd48198abba6c9efdb12303.png",
        "out": "05-clear-expression-900x1200.png",
        "index": "05 / 清晰表达",
        "quote": "困境里，清晰具体的信号，\n比盲目的呼喊更有力量。\n表达清楚，也是一种能力。",
        "footer": "把需求说具体，支持才会靠近你。",
        "accent": (30, 103, 111),
    },
    {
        "src": "ig_07e6ee992408d0e6016a3cf98306048198890a96206732cee7.png",
        "out": "06-correct-mistake-900x1200.png",
        "index": "06 / 重新选择",
        "quote": "如果发现路走错了，\n第一时间停下就是进步。\n否定过去，不等于否定自己。",
        "footer": "真正的一致，是忠于更好的未来。",
        "accent": (58, 98, 117),
    },
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)


def fit_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    src_w, src_h = img.size
    dst_w, dst_h = size
    scale = max(dst_w / src_w, dst_h / src_h)
    resized = img.resize((round(src_w * scale), round(src_h * scale)), Image.LANCZOS)
    left = max(0, (resized.width - dst_w) // 2)
    top = max(0, (resized.height - dst_h) // 2)
    return resized.crop((left, top, left + dst_w, top + dst_h))


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
) -> int:
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        bbox = draw.textbbox((x, y), line, font=fnt)
        y += (bbox[3] - bbox[1]) + line_gap
    return y


def render_card(card: dict[str, object]) -> None:
    src = SRC_DIR / str(card["src"])
    raw_out = OUT / f"background-{str(card['out']).split('-', 1)[0]}.png"
    shutil.copy2(src, raw_out)

    img = fit_cover(Image.open(src).convert("RGB"), (900, 1200)).convert("RGBA")
    blurred = img.filter(ImageFilter.GaussianBlur(10))
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((64, 98, 836, 715), radius=38, fill=200)
    img = Image.composite(blurred, img, mask).convert("RGBA")

    add_scrim(img, (64, 98, 836, 715), 38, (255, 252, 242, 222))
    draw = ImageDraw.Draw(img)

    accent = tuple(card["accent"])  # type: ignore[arg-type]
    draw.text((104, 144), str(card["index"]), font=font(32, True), fill=(*accent, 255))
    draw.line((104, 199, 258, 199), fill=(*accent, 255), width=5)

    quote_lines = str(card["quote"]).split("\n")
    draw_multiline(draw, quote_lines, (112, 268), font(42, True), (34, 42, 42, 255), 22)
    draw.text((114, 632), str(card["footer"]), font=font(25), fill=(82, 78, 66, 255))

    add_scrim(img, (88, 1016, 710, 1130), 24, (23, 43, 43, 124))
    draw.text((118, 1040), "把能力感，长成自己的光", font=font(28, True), fill=(255, 255, 248, 255))
    draw.text((118, 1088), "个人成长金句精选", font=font(22), fill=(255, 255, 248, 230))

    img.convert("RGB").save(OUT / str(card["out"]), quality=96)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for card in CARDS:
        render_card(card)


if __name__ == "__main__":
    main()
