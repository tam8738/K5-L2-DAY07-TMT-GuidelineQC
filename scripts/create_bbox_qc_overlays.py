"""Create visual overlays for COCO boxes that fail image-bound validation."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
LABELS = ROOT / "submission" / "labels" / "127.json"
IMAGES = ROOT / "data" / "images"
OUT = ROOT / "qc_overlays"


def font(size: int):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def main() -> None:
    data = json.loads(LABELS.read_text(encoding="utf-8"))
    OUT.mkdir(parents=True, exist_ok=True)
    by_id = {image["id"]: image for image in data["images"]}
    cats = {category["id"]: category["name"] for category in data["categories"]}
    bad = []
    for ann in data["annotations"]:
        image = by_id[ann["image_id"]]
        x, y, w, h = ann["bbox"]
        x2, y2 = x + w, y + h
        if x < 0 or y < 0 or x2 > image["width"] or y2 > image["height"]:
            bad.append((image, ann, cats[ann["category_id"]], x2, y2))

    for image in {item[0]["file_name"] for item in bad}:
        source = Image.open(IMAGES / image).convert("RGB")
        draw = ImageDraw.Draw(source)
        items = [item for item in bad if item[0]["file_name"] == image]
        for meta, ann, label, x2, y2 in items:
            x, y, w, h = ann["bbox"]
            clipped = (max(0, x), max(0, y), min(meta["width"], x2), min(meta["height"], y2))
            draw.rectangle(clipped, outline=(235, 50, 50), width=4)
            text = f"#{ann['id']} {label} | box bottom={y2:.0f}, image bottom={meta['height']}"
            tx, ty = max(4, int(clipped[0])), max(4, int(clipped[1]) - 24)
            box = draw.textbbox((tx, ty), text, font=font(16))
            draw.rectangle((box[0] - 2, box[1] - 2, box[2] + 2, box[3] + 2), fill=(255, 235, 235))
            draw.text((tx, ty), text, fill=(170, 0, 0), font=font(16))
        draw.rectangle((0, 0, source.width - 1, source.height - 1), outline=(40, 170, 80), width=3)
        output = OUT / image.replace(".jpg", "_bbox_qc.png")
        source.save(output)

    print(f"Created {len({item[0]['file_name'] for item in bad})} overlay images in {OUT}")


if __name__ == "__main__":
    main()
