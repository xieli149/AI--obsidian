from pathlib import Path
import shutil

from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path("/Users/lizi/Desktop/AI内容-obsidian")
OUT = ROOT / "02-稿件库/01-创作中稿件/自我成长的力量金句-images"
OUT.mkdir(parents=True, exist_ok=True)

SOURCES = [
    "/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397/ig_03f488a3e96d4513016a3de777c290819489ad27b83c69fdc9.png",
    "/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397/ig_03f488a3e96d4513016a3de7b3f7188194b0bffcc728021f8e.png",
    "/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397/ig_03f488a3e96d4513016a3de7e8908c8194a8ce4c6459a45d19.png",
    "/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397/ig_03f488a3e96d4513016a3de827be34819484080ed189ca75e5.png",
    "/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397/ig_03f488a3e96d4513016a3de861d9bc81949d68182163db1268.png",
    "/Users/lizi/.codex/generated_images/019ef3cd-0264-7561-9571-320c16486397/ig_03f488a3e96d4513016a3de8a1f5c88194a57a20a0d04c6f60.png",
]

CARDS = [
    {
        "slug": "future-identity",
        "title": "未来身份",
        "quote": "别让过去的经验锁住未来的可能。先成为未来的自己，再决定今天怎么走。",
        "sub": "成长，是先在心里换一个自己。",
    },
    {
        "slug": "courage-first",
        "title": "勇气先行",
        "quote": "不要等准备好了再开始。很多能力，都是在你先跨出去之后长出来的。",
        "sub": "先给自己一个不能后退的承诺。",
    },
    {
        "slug": "higher-standard",
        "title": "标准提升",
        "quote": "你选择什么标准，就会慢慢成为怎样的人。别降低期待，去升级自己。",
        "sub": "标准变了，人生的轨道也会变。",
    },
    {
        "slug": "growth-environment",
        "title": "创造环境",
        "quote": "别只逼自己自律，也要为自己创造一个更容易成长的环境。",
        "sub": "好的环境，会替你省下很多挣扎。",
    },
    {
        "slug": "leverage-thinking",
        "title": "杠杆思维",
        "quote": "别只靠蛮力奔跑。找到那个关键支点，小小改变也能撬动更大人生。",
        "sub": "真正的聪明，是把力用在支点上。",
    },
    {
        "slug": "independent-judgment",
        "title": "独立判断",
        "quote": "别在随波逐流里交出主见。越是不确定，越要听见自己的判断。",
        "sub": "清醒，是把选择权留在自己手里。",
    },
]

W, H = 900, 1200
FONT_SANS = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_SERIF = "/System/Library/Fonts/Supplemental/Songti.ttc"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_cover(img, size=(W, H), center=(0.5, 0.5)):
    iw, ih = img.size
    sw, sh = size
    scale = max(sw / iw, sh / ih)
    nw, nh = int(iw * scale), int(ih * scale)
    img = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = int((nw - sw) * center[0])
    top = int((nh - sh) * center[1])
    return img.crop((left, top, left + sw, top + sh))


def wrap_cn(text, draw, ft, max_width):
    lines, current = [], ""
    for ch in text:
        trial = current + ch
        if draw.textlength(trial, font=ft) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = ch
    if current:
        lines.append(current)
    return lines


def draw_tracking(draw, xy, text, ft, fill, tracking=2):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=ft, fill=fill)
        x += draw.textlength(ch, font=ft) + tracking


def add_soft_text_veil(base):
    veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    vd.rounded_rectangle((62, 74, 838, 690), radius=30, fill=(255, 252, 244, 188))
    vd.rounded_rectangle((62, 74, 838, 690), radius=30, outline=(255, 255, 255, 120), width=2)
    blur = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bd = ImageDraw.Draw(blur)
    bd.rounded_rectangle((66, 84, 834, 700), radius=34, fill=(70, 62, 50, 28))
    blur = blur.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(Image.alpha_composite(base, blur), veil)


def render_card(src, card, index):
    img = Image.open(src).convert("RGB")
    img = fit_cover(img, (W, H)).convert("RGBA")
    img = add_soft_text_veil(img)
    d = ImageDraw.Draw(img)

    title_font = font(FONT_SANS, 36)
    kicker_font = font(FONT_SANS, 21)
    quote_font = font(FONT_SERIF, 49)
    sub_font = font(FONT_SANS, 27)
    num_font = font(FONT_SANS, 24)

    ink = (43, 48, 48, 255)
    muted = (93, 102, 99, 255)
    accent = (198, 91, 65, 255)

    left, right = 108, 792
    y = 126

    d.line((left, y, left + 58, y), fill=accent, width=4)
    draw_tracking(d, (left + 76, y - 15), "自我成长的力量", kicker_font, muted, tracking=3)
    d.text((right - 44, y - 20), f"{index:02d}", font=num_font, fill=(120, 128, 123, 220))

    y += 76
    d.text((left, y), card["title"], font=title_font, fill=ink)

    y += 82
    quote_lines = wrap_cn(card["quote"], d, quote_font, right - left)
    line_gap = 19
    for line in quote_lines:
        d.text((left, y), line, font=quote_font, fill=ink)
        y += quote_font.size + line_gap

    y += 30
    d.rounded_rectangle((left, y - 4, left + 46, y + 6), radius=3, fill=accent)
    y += 30
    sub_lines = wrap_cn(card["sub"], d, sub_font, right - left)
    for line in sub_lines:
        d.text((left, y), line, font=sub_font, fill=muted)
        y += sub_font.size + 13

    # Small bottom signature keeps the series visually connected without adding noisy copy.
    d.text((left, H - 88), "PERSONAL GROWTH", font=font(FONT_SANS, 18), fill=(80, 88, 86, 155))

    bg_name = OUT / f"{index:02d}-{card['slug']}-background.png"
    final_name = OUT / f"{index:02d}-{card['slug']}-900x1200.png"
    shutil.copyfile(src, bg_name)
    img.convert("RGB").save(final_name, quality=95)
    return final_name


def main():
    outputs = []
    for idx, (src, card) in enumerate(zip(SOURCES, CARDS), 1):
        outputs.append(render_card(src, card, idx))
    print("\n".join(str(p) for p in outputs))


if __name__ == "__main__":
    main()
