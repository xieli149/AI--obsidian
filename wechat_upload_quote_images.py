import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode

import requests
from PIL import Image


ROOT = Path("/Users/lizi/Desktop/AI内容-obsidian")
IMG_DIR = ROOT / "02-稿件库/01-创作中稿件/自我成长的力量金句-images"
OUT_JSON = IMG_DIR / "wechat-upload-result.json"
THUMB = IMG_DIR / "_wechat-thumb.jpg"

IMAGES = [
    IMG_DIR / "01-future-identity-900x1200.png",
    IMG_DIR / "02-courage-first-900x1200.png",
    IMG_DIR / "03-higher-standard-900x1200.png",
    IMG_DIR / "04-growth-environment-900x1200.png",
    IMG_DIR / "05-leverage-thinking-900x1200.png",
    IMG_DIR / "06-independent-judgment-900x1200.png",
]


def wechat_json(resp):
    try:
        data = resp.json()
    except Exception:
        resp.raise_for_status()
        raise RuntimeError(resp.text[:500])
    if data.get("errcode"):
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data


def get_token(appid, secret):
    params = urlencode(
        {
            "grant_type": "client_credential",
            "appid": appid,
            "secret": secret,
        }
    )
    resp = requests.get(f"https://api.weixin.qq.com/cgi-bin/token?{params}", timeout=30)
    return wechat_json(resp)["access_token"]


def make_thumb(src):
    img = Image.open(src).convert("RGB")
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize((300, 300), Image.Resampling.LANCZOS)
    for quality in [82, 76, 70, 64, 58, 52, 46]:
        img.save(THUMB, format="JPEG", quality=quality, optimize=True)
        if THUMB.stat().st_size < 63 * 1024:
            return THUMB
    img.resize((240, 240), Image.Resampling.LANCZOS).save(THUMB, format="JPEG", quality=52, optimize=True)
    return THUMB


def upload_article_image(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token={token}"
    with open(path, "rb") as f:
        resp = requests.post(url, files={"media": (path.name, f, "image/png")}, timeout=90)
    data = wechat_json(resp)
    if "url" not in data:
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data["url"]


def upload_thumb(token, path):
    url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=thumb"
    with open(path, "rb") as f:
        resp = requests.post(url, files={"media": (path.name, f, "image/jpeg")}, timeout=90)
    data = wechat_json(resp)
    if "media_id" not in data:
        raise RuntimeError(json.dumps(data, ensure_ascii=False))
    return data["media_id"]


def add_draft(token, thumb_media_id, image_urls):
    parts = [
        "<section style='margin:0 auto;max-width:677px;'>",
        "<p style='margin:0 0 18px;color:#5f6663;font-size:15px;line-height:1.8;'>这组金句图，送给正在自我成长路上的你。愿我们都能把力量用在真正重要的地方。</p>",
    ]
    for idx, url in enumerate(image_urls, 1):
        parts.append(
            f"<p style='margin:0 0 18px;text-align:center;'>"
            f"<img src='{url}' style='width:100%;height:auto;display:block;border-radius:8px;' "
            f"data-w='900' data-ratio='1.3333333333' alt='自我成长的力量金句图 {idx}'/>"
            f"</p>"
        )
    parts.append("</section>")
    content = "".join(parts)
    payload = {
        "articles": [
            {
                "title": "自我成长的力量：6 张金句图",
                "author": "Lizi",
                "digest": "把未来身份、勇气、标准、环境、杠杆和独立判断，变成每天往前走的力量。",
                "content": content,
                "content_source_url": "",
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0,
            }
        ]
    }
    url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
    resp = requests.post(url, data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), timeout=90)
    return wechat_json(resp)


def main():
    appid = os.environ.get("WECHAT_APPID")
    secret = os.environ.get("WECHAT_APPSECRET")
    if not appid or not secret:
        print("Missing WECHAT_APPID or WECHAT_APPSECRET", file=sys.stderr)
        sys.exit(2)
    for image in IMAGES:
        if not image.exists():
            raise FileNotFoundError(image)

    token = get_token(appid, secret)
    image_urls = [upload_article_image(token, p) for p in IMAGES]
    thumb = make_thumb(IMAGES[0])
    thumb_media_id = upload_thumb(token, thumb)
    draft = add_draft(token, thumb_media_id, image_urls)

    result = {
        "draft": draft,
        "thumb": str(thumb),
        "thumb_media_id": thumb_media_id,
        "image_urls": image_urls,
    }
    OUT_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"draft": draft, "uploaded_images": len(image_urls), "result_file": str(OUT_JSON)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
