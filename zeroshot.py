from groq import generate_response


def run_activity():
    print("======================================")
    print("ZERO-SHOT, ONE-SHOT & FEW-SHOT LEARNING ACTIVITY")
    print("======================================")

    category = input("Enter a category (e.g., animal, food, city): ").strip()
    item = input(f"Enter a specific {category}: ").strip()

    # Input validation
    if not category or not item:
        print("Please fill in both fields to run the activity.")
        return

    # -----------------------------------
    # ZERO-SHOT LEARNING
    # -----------------------------------
    zero_shot = f"""
Is {item} a {category}?
Answer only Yes or No and provide a short explanation.
"""

    print("\n--- ZERO-SHOT LEARNING ---")
    print(generate_response(zero_shot, temperature=0.3, max_tokens=200))

    # -----------------------------------
    # ONE-SHOT LEARNING
    # -----------------------------------
    one_shot = f"""
Example:
Category: Fruit
Item: Apple
Answer: Yes, Apple is a fruit.

Now you try:
Category: {category}
Item: {item}
Answer:
"""

    print("\n--- ONE-SHOT LEARNING ---")
    print(generate_response(one_shot, temperature=0.3, max_tokens=200))

    # -----------------------------------
    # FEW-SHOT LEARNING
    # -----------------------------------
    few_shot = f"""
Example 1:
Category: Fruit
Item: Apple
Answer: Yes, Apple is a fruit.

Example 2:
Category: Animal
Item: Lion
Answer: Yes, Lion is an animal.

Example 3:
Category: City
Item: Paris
Answer: Yes, Paris is a city.

Now you try:
Category: {category}
Item: {item}
Answer:
"""

    print("\n--- FEW-SHOT LEARNING ---")
    print(generate_response(few_shot, temperature=0.3, max_tokens=200))

    # -----------------------------------
    # CREATIVE FEW-SHOT LEARNING
    # -----------------------------------
    creative_prompt = f"""
Write a one-sentence story about the given word.

Example 1:
Word: Moon
Story: The moon winked at the lovers as they shared their first kiss.

Example 2:
Word: Robot
Story: The little robot dreamed of becoming an astronaut.

Word: {item}
Story:
"""

    print("\n--- CREATIVE FEW-SHOT LEARNING ---")
    print(generate_response(creative_prompt, temperature=0.7, max_tokens=100))

    # -----------------------------------
    # REFLECTION QUESTIONS
    # -----------------------------------
    print("\n--- REFLECTION QUESTIONS ---")
    print("1. How did the responses differ between Zero-Shot, One-Shot, and Few-Shot learning?")
    print("2. Which approach gave the most accurate response?")
    print("3. How did providing examples influence the model's output?")
    print("4. Which response style did you find most helpful and why?")


if __name__ == "__main__":
    run_activity()

