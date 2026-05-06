import time
from datetime import datetime
from PIL import Image, ImageEnhance, ImageFilter
from config import HF_API_KEY
from huggingface_hub import InferenceClient


MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5"
]


# Initialize client
client = InferenceClient(api_key=HF_API_KEY)


print(f"Primary model: {MODELS[0]}")
print("Type 'quit' to exit\n")




def generate_image_from_text(prompt):
    if not prompt:
        return None


    print("Generating...")
    image = None


    # Try each model
    for model in MODELS:
        try:
            image = client.text_to_image(prompt, model=model)
            break
        except Exception:
            print("  Trying next model...")
            continue


    if image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"generated_{timestamp}.png"
        image.save(filename)
        print(f"✓ Saved: {filename}")
        image.show()
        print()
        return image
    else:
        print("Error: All models failed. Check your API key.\n")
        return None




def post_process_image(image):
    image = ImageEnhance.Brightness(image).enhance(1.2)
    image = ImageEnhance.Contrast(image).enhance(1.3)
    return image.filter(ImageFilter.GaussianBlur(radius=2))




def main():
    print("Welcome to the Post-Processing Magic Workshop!")
    print("Type 'exit' to quit.\n")


    while True:
        user_input = input("Enter a description:\n")


        if user_input.lower() == "exit":
            print("Goodbye!")
            break


        try:
            image = generate_image_from_text(user_input)


            if image is None:
                continue


            print("Applying post-processing effects...\n")
            processed_image = post_process_image(image)
            processed_image.show()


            save_option = input("Save processed image? (yes/no): ").strip().lower()
            if save_option == "yes":
                file_name = input("Enter file name: ").strip()
                processed_image.save(f"{file_name}.png")
                print(f"Saved as {file_name}.png!\n")


            print("-" * 50)


        except Exception as e:
            print(f"Error: {e}\n")




if __name__ == "__main__":
    main()