print("Hello! I am AI Bot. What's your name?")

name = input().lower()

print(f"Nice to meet you {name}!")

mood = input("How are you feeling today? (good/bad): ").lower()
if mood == "good":
    print("I'm glad to hear that!")
elif mood == "bad":
    print("That sucks.. I hope your day becomes better soon!")

print(f"It was nice chatting with you {name}. Goodbye!")