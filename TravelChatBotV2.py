import re, random
from colorama import Fore, init

init(autoreset=True)

destinations = {
    "beaches": [
        "Bali", "Maldives", "Phuket", "Santorini", "Bora Bora",
        "Seychelles", "Hawaii", "Cape Town", "Mauritius", "Cancun"
    ],
    "mountains": [
        "Swiss Alps", "Rocky Mountains", "Himalayas", "Drakensberg",
        "Andes", "Mount Kilimanjaro", "Pyrenees", "Appalachian Mountains",
        "Alps in Austria", "Mount Fuji"
    ],
    "cities": [
        "Tokyo", "Paris", "New York", "London", "Dubai",
        "Singapore", "Rome", "Barcelona", "Cape Town", "Sydney"
    ],
    "adventure": [
        "Queenstown", "Costa Rica", "Patagonia", "Iceland", "Nepal",
        "Zanzibar", "Namibia", "Peru", "Alaska", "South Africa"
    ],
    "historical": [
        "Rome", "Athens", "Cairo", "Jerusalem", "Istanbul",
        "Machu Picchu", "Petra", "Luxor", "Edinburgh", "Cusco"
    ],
    "safari": [
        "Kruger National Park", "Serengeti", "Masai Mara", "Okavango Delta",
        "Etosha", "Addo Elephant Park", "Chobe", "Hwange", "Amboseli", "Hluhluwe"
    ]
}

jokes = [
    "Why don't programmers like nature? Too many bugs!",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why do the travelers always feel warm? Because of all their hot spots!",
    "Why did the tourist bring a ladder? To reach new heights!",
    "Why don’t suitcases ever get lost? Because they always follow baggage claims!",
    "Why did the airplane get sent to timeout? It had a bad attitude!",
    "Why did the beach break up with the ocean? Too many waves of emotion!",
    "Why do mountains make great comedians? They always peak at the right moment!",
    "Why was the passport so confident? It had lots of stamps of approval!",
    "Why did the traveler sit on the clock? He wanted to be on time!",
    "Why was the road so good at telling stories? It had lots of twists and turns!",
    "Why did the hotel pillow get promoted? It was very supportive!",
    "What’s a traveler’s favorite kind of music? Trip-hop!",
    "Why did the map blush? Because it saw the whole world!",
    "Why don’t travelers play hide and seek? Because good luck hiding when your location is on!"
]

def normalize_input(text):
    return re.sub(r"\s+", " ", text.strip().lower())

def recommend():
    print(Fore.CYAN + "TravelBot: Beaches, mountains, cities, adventure, historical, or safari?")
    preference = input(Fore.YELLOW + "You: ")
    preference = normalize_input(preference)

    if preference in destinations:
        suggestion = random.choice(destinations[preference])
        print(Fore.GREEN + f"TravelBot: How about {suggestion}?")
        print(Fore.CYAN + "TravelBot: Do you like it? (yes/no)")
        answer = input(Fore.YELLOW + "You: ").lower()

        if answer == "yes":
            print(Fore.GREEN + f"TravelBot: Awesome! Enjoy {suggestion}!")
        elif answer == "no":
            print(Fore.RED + "TravelBot: Let's try another.")
            recommend()
        else:
            print(Fore.RED + "TravelBot: I'll suggest again.")
            recommend()
    else:
        print(Fore.RED + "TravelBot: Sorry, I don't have that type of destination.")
        recommend()

def packing_tips():
    print(Fore.CYAN + "TravelBot: Where to?")
    location = normalize_input(input(Fore.YELLOW + "You: "))
    print(Fore.CYAN + "TravelBot: How many days?")
    days = input(Fore.YELLOW + "You: ")

    print(Fore.GREEN + f"TravelBot: Packing tips for {days} days in {location}:")
    print(Fore.GREEN + "- Pack versatile clothes.")
    print(Fore.GREEN + "- Bring chargers/adapters.")
    print(Fore.GREEN + "- Check the weather forecast.")
    print(Fore.GREEN + "- Keep important documents safe.")
    print(Fore.GREEN + "- Pack only what you really need.")

def tell_joke():
    print(Fore.YELLOW + f"TravelBot: {random.choice(jokes)}")

def show_help():
    print(Fore.MAGENTA + "\nI can:")
    print(Fore.GREEN + "- Suggest travel spots (say 'recommendation')")
    print(Fore.GREEN + "- Offer packing tips (say 'packing')")
    print(Fore.GREEN + "- Tell a joke (say 'joke')")
    print(Fore.GREEN + "- Categories: beaches, mountains, cities, adventure, historical, safari")
    print(Fore.GREEN + "Type 'exit' or 'bye' to end.\n")

def chat():
    print(Fore.CYAN + "Hello! I'm TravelBot.")
    name = input(Fore.YELLOW + "Your name? ")
    print(Fore.GREEN + f"Nice to meet you, {name}!")

    show_help()

    while True:
        user_input = input(Fore.YELLOW + f"{name}: ")
        user_input = normalize_input(user_input)

        if "recommend" in user_input or "suggest" in user_input:
            recommend()
        elif "pack" in user_input or "packing" in user_input:
            packing_tips()
        elif "joke" in user_input or "funny" in user_input:
            tell_joke()
        elif "help" in user_input:
            show_help()
        elif "exit" in user_input or "bye" in user_input:
            print(Fore.CYAN + "TravelBot: Safe Travels! Goodbye!")
            break
        else:
            print(Fore.RED + "TravelBot: Could you rephrase?")

if __name__ == "__main__":
    chat()