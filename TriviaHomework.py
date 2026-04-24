import requests
import random
import html

score = 0

url = "https://opentdb.com/api.php?amount=5&type=multiple"

response = requests.get(url)
data = response.json()

questions = data["results"]

for question_number, question_data in enumerate(questions, start=1):
    question = html.unescape(question_data["question"])
    correct_answer = html.unescape(question_data["correct_answer"])

    answers = question_data["incorrect_answers"] + [question_data["correct_answer"]]
    answers = [html.unescape(answer) for answer in answers]

    random.shuffle(answers)

    print()
    print(f"Question {question_number}: {question}")
    print()

    for index, answer in enumerate(answers, start=1):
        print(f"{index}. {answer}")

    while True:
        user_answer = input("\nEnter your answer, 1, 2, 3, or 4: ")

        if user_answer in ["1", "2", "3", "4"]:
            break
        else:
            print("Please enter a number from 1 to 4.")

    selected_answer = answers[int(user_answer) - 1]

    if selected_answer == correct_answer:
        print("Correct!")
        score += 1
    else:
        print(f"Wrong! The correct answer was: {correct_answer}")

print()
print(f"Quiz finished! Your final score is {score} out of {len(questions)}.")