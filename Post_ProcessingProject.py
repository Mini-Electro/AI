from datetime import datetime
from PIL import ImageEnhance, ImageFilter
from config import HF_API_KEY
from huggingface_hub import InferenceClient


MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5"
]


client = InferenceClient(api_key=HF_API_KEY)


def generate_image_from_text(prompt):
    if not prompt:
        return None

    print("Generating image...")

    for model in MODELS:
        try:
            print(f"Trying model: {model}")
            image = client.text_to_image(prompt, model=model)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"original_{timestamp}.png"
            image.save(filename)

            print(f"Original image saved as: {filename}")
            image.show()

            return image

        except Exception:
            print("Model failed. Trying next model...")

    print("Error: All models failed. Check your API key.")
    return None


def post_process_image(image, brightness, contrast, blur_radius):
    image = ImageEnhance.Brightness(image).enhance(brightness)
    image = ImageEnhance.Contrast(image).enhance(contrast)
    image = image.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    return image


def get_float_input(message, default_value):
    user_value = input(message).strip()

    if user_value == "":
        return default_value

    try:
        return float(user_value)
    except ValueError:
        print("Invalid number. Using default value.")
        return default_value


def main():
    print("Welcome to the Post-Processing Magic Workshop!")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:
        prompt = input("Enter an image description:\n").strip()

        if prompt.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        image = generate_image_from_text(prompt)

        if image is None:
            continue

        print("\nChoose post-processing values.")
        print("Press Enter to use the default value.\n")

        brightness = get_float_input("Brightness level default 1.2: ", 1.2)
        contrast = get_float_input("Contrast level default 1.3: ", 1.3)
        blur_radius = get_float_input("Blur radius default 2: ", 2)

        print("\nApplying post-processing effects...\n")

        processed_image = post_process_image(
            image,
            brightness,
            contrast,
            blur_radius
        )

        processed_image.show()

        save_option = input("Save processed image? yes/no: ").strip().lower()

        if save_option == "yes":
            file_name = input("Enter file name without .png: ").strip()

            if file_name == "":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                file_name = f"processed_{timestamp}"

            processed_image.save(f"{file_name}.png")
            print(f"Processed image saved as {file_name}.png!\n")

        print("-" * 50)


if __name__ == "__main__":
    main()