import os
import shutil
from PIL import Image, ImageOps   # 🔹 ImageOps 추가

INPUT_DIR = "gallery_original"
OUTPUT_DIR = "gallery_images"

MAX_SIZE = 1600  # 긴 변 기준 px
IMAGE_EXT = (".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG")
SIZE_THRESHOLD = 5 * 1024 * 1024  # 5MB


def resize_image(input_path, output_path):
    # 🔹 EXIF 기준으로 올바른 방향으로 회전
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    # PNG, 팔레트 모드 등 대비
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")

    w, h = img.size
    if max(w, h) > MAX_SIZE:
        if w >= h:
            new_w = MAX_SIZE
            new_h = int(h * (MAX_SIZE / w))
        else:
            new_h = MAX_SIZE
            new_w = int(w * (MAX_SIZE / h))
        img = img.resize((new_w, new_h), Image.LANCZOS)
        print(f"    → resized: {w}x{h} -> {new_w}x{new_h}")
    else:
        print(f"    → no resize needed: {w}x{h} (해상도 유지)")

    # JPG로 저장 (품질 85)
    img.save(output_path, format="JPEG", quality=85, optimize=True)


def main():
    if not os.path.exists(INPUT_DIR):
        print(f"❌ 원본 폴더가 없습니다: {INPUT_DIR}")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    files = [
        f for f in os.listdir(INPUT_DIR)
        if os.path.isfile(os.path.join(INPUT_DIR, f)) and f.endswith(IMAGE_EXT)
    ]

    if not files:
        print("❗ 변환할 이미지가 없습니다.")
        return

    print(f"총 {len(files)}개 이미지 처리 시작 (5MB 이상만 리사이즈)")

    for filename in files:
        input_path = os.path.join(INPUT_DIR, filename)
        file_size = os.path.getsize(input_path)

        name, _ = os.path.splitext(filename)
        output_filename = f"{name}.jpg"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        print(f"[{filename}] ({file_size / (1024*1024):.2f} MB)")

        if file_size > SIZE_THRESHOLD:
            resize_image(input_path, output_path)
        else:
            # 5MB 이하면 방향만 맞춰서 다시 저장하고 싶으면
            # -> 여기에도 resize_image를 쓰거나, exif_transpose만 하고 저장하도록 바꿀 수 있음
            if input_path != output_path:
                # 그냥 원본 복사 (방향은 원래 브라우저/뷰어가 맞춰줌)
                shutil.copy2(input_path, output_path)
                print("    → 5MB 이하, 원본 그대로 복사")

    print("✅ 모든 이미지 처리 완료")


if __name__ == "__main__":
    main()
