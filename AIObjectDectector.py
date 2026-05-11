import os
import io
import time
import random
import requests
import mimetypes


from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from config import HF_API_KEY




# =========================
# MODEL CONFIGURATION
# =========================


MODEL = "facebook/detr-resnet-50"


API = f"https://router.huggingface.co/hf-inference/models/{MODEL}"


ALLOWED = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".gif",
    ".webp",
    ".tiff"
}


MAX_MB = 8




# =========================
# EMOJIS
# =========================


EMOJI = {
    "person": "🧍",
    "car": "🚗",
    "truck": "🛻",
    "bus": "🚌",
    "bicycle": "🚲",
    "motorcycle": "🏍️",
    "dog": "🐶",
    "cat": "😺",
    "bird": "🐦",
    "horse": "🐴",
    "sheep": "🐑",
    "cow": "🐮",
    "bear": "🐻",
    "giraffe": "🦒",
    "zebra": "🦓",
    "banana": "🍌",
    "apple": "🍏",
    "orange": "🍊",
    "pizza": "🍕",
    "broccoli": "🥦",
    "book": "📕",
    "laptop": "💻",
    "tv": "📺",
    "bottle": "🍼",
    "cup": "☕"
}




# =========================
# FONT FUNCTION
# =========================


def font(sz=18):


    for f in ("DejaVuSans.ttf", "arial.ttf"):


        try:
            return ImageFont.truetype(f, sz)


        except:
            pass


    return ImageFont.load_default()




# =========================
# ASK IMAGE
# =========================


def ask_image():


    print("\n🎯 Pick an image (JPG/PNG/WebP/BMP/TIFF < 8MB)")


    while True:


        path = input("Image Path: ").strip().strip('"').strip("'")


        if not path:
            print("⚠️ Please enter a path.")
            continue


        if not os.path.isfile(path):
            print("⚠️ File not found.")
            continue


        ext = os.path.splitext(path)[1].lower()


        if ext not in ALLOWED:
            print("⚠️ Unsupported image type.")
            continue


        size_mb = os.path.getsize(path) / (1024 * 1024)


        if size_mb > MAX_MB:
            print("⚠️ Image is larger than 8MB.")
            continue


        try:
            Image.open(path).verify()


        except:
            print("⚠️ Corrupted image.")
            continue


        return path




# =========================
# HUGGING FACE INFERENCE
# =========================


def infer(path, img_bytes, tries=8):


    mime, _ = mimetypes.guess_type(path)


    for attempt in range(tries):


        try:


            # Send image request
            if mime and mime.startswith("image/"):


                response = requests.post(
                    API,
                    headers={
                        "Authorization": f"Bearer {HF_API_KEY}",
                        "Content-Type": mime
                    },
                    data=img_bytes,
                    timeout=120
                )


            else:


                response = requests.post(
                    API,
                    headers={
                        "Authorization": f"Bearer {HF_API_KEY}"
                    },
                    files={
                        "inputs": (
                            os.path.basename(path),
                            img_bytes,
                            "application/octet-stream"
                        )
                    },
                    timeout=120
                )


            # SUCCESS
            if response.status_code == 200:


                data = response.json()


                if isinstance(data, dict) and "error" in data:
                    raise RuntimeError(data["error"])


                if not isinstance(data, list):
                    raise RuntimeError("Unexpected API response.")


                return data


            # MODEL WARMING
            elif response.status_code == 503:


                print("⏳ Model warming up... Please wait.")
                time.sleep(5)
                continue


            # OTHER API ERRORS
            else:


                raise RuntimeError(
                    f"API {response.status_code}: {response.text[:300]}"
                )


        except requests.exceptions.Timeout:


            print("⏳ Request timeout. Retrying...")
            time.sleep(3)


        except Exception as e:


            raise RuntimeError(str(e))


    raise RuntimeError("❌ Model warm-up timeout.")




# =========================
# DRAW DETECTIONS
# =========================


def draw(img, dets, thr=0.5):


    draw_obj = ImageDraw.Draw(img)


    f = font(18)


    counts = {}


    for det in dets[:50]:


        score = float(det.get("score", 0))


        if score < thr:
            continue


        label = det.get("label", "object")


        box = det.get("box", {})


        x1 = int(box.get("xmin", 0))
        y1 = int(box.get("ymin", 0))
        x2 = int(box.get("xmax", 0))
        y2 = int(box.get("ymax", 0))


        # Alternative box format support
        if not (x2 > 0 and y2 > 0):


            x = int(box.get("x", 0))
            y = int(box.get("y", 0))
            w = int(box.get("w", 0))
            h = int(box.get("h", 0))


            x1, y1, x2, y2 = x, y, x + w, y + h


        # Random color
        color = tuple(
            random.randint(80, 220)
            for _ in range(3)
        )


        # Draw rectangle
        draw_obj.rectangle(
            [(x1, y1), (x2, y2)],
            outline=color,
            width=4
        )


        # Label text
        text = (
            f"{EMOJI.get(label.lower(), '✨')} "
            f"{label} "
            f"{score * 100:.0f}%"
        )


        # Text size
        text_width = draw_obj.textlength(text, font=f)


        text_height = f.size + 6


        # Background rectangle
        draw_obj.rectangle(
            [
                (x1, max(0, y1 - text_height)),
                (x1 + text_width + 8, y1)
            ],
            fill=color
        )


        # Draw text
        draw_obj.text(
            (x1 + 4, y1 - text_height + 3),
            text,
            font=f,
            fill=(0, 0, 0)
        )


        # Count objects
        counts[label] = counts.get(label, 0) + 1


    return counts




# =========================
# MAIN PROGRAM
# =========================


def main():


    print("\n==============================")
    print("🤖 AI OBJECT DETECTOR")
    print("==============================")


    # Ask image
    path = ask_image()


    # Read image bytes
    with open(path, "rb") as file:
        img_bytes = file.read()


    # Inference
    try:


        detections = infer(path, img_bytes)


    except Exception as e:


        print(e)
        return


    # Open image
    img = Image.open(
        io.BytesIO(img_bytes)
    ).convert("RGB")


    # Draw detections
    counts = draw(
        img,
        detections,
        thr=0.5
    )


    # Output filename
    output_file = (
        f"annotated_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    )


    # Save image
    img.save(output_file)


    print(f"\n✅ Saved: {output_file}")


    # Print detections
    if counts:


        print("\n🎉 Objects Found:\n")


        for label, count in sorted(
            counts.items(),
            key=lambda kv: (-kv[1], kv[0])
        ):


            print(
                f"{EMOJI.get(label.lower(), '✨')} "
                f"{label}: {count}"
            )


    else:


        print(
            "\n🤔 No confident detections found."
        )


    print(
        "\n⚠️ Disclaimer: "
        "AI detections may not always be accurate."
    )




# =========================
# START PROGRAM
# =========================


if __name__ == "__main__":
    main()






