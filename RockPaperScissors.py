import random
from colorama import Fore, Style, init

init(autoreset=True)

possible_actions = ["rock", "paper", "scissors"]

while True:
    user_action = input(Fore.CYAN + "Enter a choice! (rock, paper, scissors): ").lower()
    computer_action = random.choice(possible_actions)

    print(
        Fore.YELLOW
        + f"\nYou chose {user_action}, computer chose {computer_action}.\n"
    )

    if user_action == computer_action:
        print(Fore.BLUE + f"Both players selected {user_action}. It's a tie!")
    elif user_action == "rock":
        if computer_action == "scissors":
            print(Fore.GREEN + "Rock smashes scissors! You win!")
        else:
            print(Fore.RED + "Paper covers rock! You lose.")
    elif user_action == "paper":
        if computer_action == "rock":
            print(Fore.GREEN + "Paper covers rock! You win!")
        else:
            print(Fore.RED + "Scissors cut paper! You lose.")
    elif user_action == "scissors":
        if computer_action == "paper":
            print(Fore.GREEN + "Scissors cut paper! You win!")
        else:
            print(Fore.RED + "Rock smashes scissors! You lose.")
    else:
        print(Fore.MAGENTA + "That is not a valid choice.")

    play_again = input(Fore.CYAN + "Play again? (y/n): ").lower()
    if play_again != "y":
        print(Fore.WHITE + "Thanks for playing!")
        break