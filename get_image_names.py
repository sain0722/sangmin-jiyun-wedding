import os

TARGET_DIR = "gallery_images"
OUTPUT_FILE = "gallery_list.js"

IMAGE_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".JPG", ".JPEG", ".PNG")

def main():
    if not os.path.exists(TARGET_DIR):
        return print(f"❌ 폴더가 없습니다: {TARGET_DIR}")

    files = [
        f for f in os.listdir(TARGET_DIR)
        if os.path.isfile(os.path.join(TARGET_DIR, f)) and f.endswith(IMAGE_EXT)
    ]

    files.sort()

    js_array = "const galleryImages = [\n"
    for f in files:
        js_array += f"    'gallery_images/{f}',\n"
    js_array += "];\n"

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(js_array)

    print(f"✅ gallery_list.js 생성 완료 — {len(files)}개의 이미지 포함")

if __name__ == "__main__":
    main()
