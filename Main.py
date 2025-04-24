import re
import time
from langs import langs
import utils

while (LANG := input("Choose a language [en or fr]:\t").lower()) not in ("en", "fr"):
    print(f"Language {LANG} not supported.")

from QuestionGenerator import generate_questions

# Initialise random number generator
utils._init(LANG)

# Setup
points = 0
common_elements = [
    1, 2,
    3, 6, 7, 8, 9, 10,
    11, 12, 13, 14, 15, 16, 17, 18,
    19, 20, 26, 29, 35,
    53,
    56,
    82,
]

natural_elements = [v for v in range(1, 93)]
all_elements = [v for v in range(1, 119)]

# Polyatomic ion ids
polyatomic_ion_ids = [v for v in range(0, 30)]

polyatomic_ion_pool = polyatomic_ion_ids

# Is the correct order of the charges required
charge_order_sensitive = True

while not re.fullmatch(r"[1-9]\d{0,2}", questionCount := input(langs.get_ui_text("ask_question_count", LANG))) :
    print("Enter a valid question count (0 < count < 999).")

questionCount = int(questionCount)

# Get the choice of pool to use
while (poolChoice := input(langs.get_ui_text("utils.ask_for_element_pool", LANG)).upper()) not in ("C", "N", "A", "U"):
    print(langs.get_ui_text("utils.invalid_option", LANG))

# User enters custom element pool
if poolChoice == "U":
    element_pool = utils.get_custom_element_pool()

elif poolChoice == "C":
    element_pool = common_elements

elif poolChoice == "N":
    element_pool = natural_elements

elif poolChoice == "A":
    element_pool = all_elements

# Generate questions and answers
questions, answers = generate_questions(["ENTS", "STEN", "COFE", "COFS"], ["PNTF", "FTPN", "PNTC", "PFTC"], element_pool, polyatomic_ion_pool, questionCount, LANG, [0.15, 0.15, 0.1, 0.1, 0.15, 0.15, 0.1, 0.1])

# Amoutn of characters to type all answers
answer_char_count = sum(len(s) for s in answers)

start_time = time.time_ns()

for i in range(questionCount):
    allow_unordered_charges = False
    # Check if the question is case-sensitive
    if questions[i].startswith(langs.get_question_text("STEN", LANG).split("{")[0]) or questions[i].startswith(langs.get_question_text("FTPN", LANG).split("{")[0]):
        case_sensitive_answer = False

    else:
        case_sensitive_answer = True
    
    # TODO: Is this needed?
    # Check if the question is space-sensitive
    if questions[i].startswith(langs.get_question_text("COFE", LANG).split("{")[0]) or questions[i].startswith(langs.get_question_text("COFS", LANG).split("{")[0]):
        space_sensitive_answer = False

        # Check if the order of numbers matters
        if not charge_order_sensitive:
            allow_unordered_charges = True
    
    else:
        space_sensitive_answer = True

    # Generate question and answer
    print("\n" + questions[i])
    response = input(langs.get_ui_text("ask_answer", LANG))

    # Make case-sensitive adjustments, if necessary
    if not case_sensitive_answer:
        response = response.lower()
        answers[i] = answers[i].lower()
    
    # Make space-sensitive adjustments, if necessary
    if not space_sensitive_answer:
        response = response.replace(" ", "")
        answers[i] = answers[i].replace(" ", "")

    if allow_unordered_charges:
        # Order the charges
        response = response.split(",")
        response.sort()

        answer_copy = answers[i].split(",")
        answer_copy.sort()

        # Check the charges
        if response == answer_copy:
            correct_answer = True

        else:
            correct_answer = False

    # Default action
    else:
        correct_answer = response == answers[i]

    # Check if the answer is correct
    if correct_answer:

        # Print correct answer
        print(langs.get_ui_text("correct_answer", LANG))
        points += 1
    
    # Print incorrect answer
    else:
        print(langs.get_ui_text("incorrect_answer", LANG).replace("{0}", answers[i]))

end_time = time.time_ns()

time_used = (end_time-start_time) / 1_000_000_000

print(langs.get_ui_text("quiz_time", LANG).format(round(time_used, 2), round(time_used/questionCount, 3)))
print(langs.get_ui_text("quiz_time_per_char", LANG).format(round(time_used/answer_char_count*1000), answer_char_count))
print(langs.get_ui_text("final_score", LANG).format(points, questionCount, points/questionCount*100))