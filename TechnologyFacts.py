import requests


url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"


def get_random_fact():
    try:
        response = requests.get(url, timeout=5)


        if response.status_code == 200:
            fact_data = response.json()
            print(f"\n💡 Did you know?\n{fact_data['text']}\n")
        else:
            print("⚠️ Failed to fetch fact (Server Error)\n")


    except requests.exceptions.RequestException:
        print("❌ Network error! Please check your internet.\n")


while True:
    user_input = input("Press Enter for a fact or type 'q' to quit: ")


    if user_input.lower() == 'q':
        print("👋 Goodbye!")
        break


    get_random_fact()