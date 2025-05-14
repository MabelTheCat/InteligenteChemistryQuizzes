import re
import time
from langs import langs
import utils
import updater

while (LANG := input("Choose a language [en or fr]:\t").lower()) not in ("en", "fr"):
    print(f"Language {LANG} not supported.")

from QuestionGenerator import generate_questions

def get_quiz_settings(lang):

    # Initialise random number generator
    utils._init(LANG)

    # Setup
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
    charge_order_sensitive = False if input(langs.get_ui_text("is_charge_order_sensitive", lang)).upper() in langs.get_ui_text("deny", lang) else True

    while not re.fullmatch(r"[1-9]\d{0,2}", question_count := input(langs.get_ui_text("ask_question_count", lang))) :
        print("Enter a valid question count (0 < count < 999).")

    question_count = int(question_count)

    # Get the choice of pool to use
    while (poolChoice := input(langs.get_ui_text("utils.ask_for_element_pool", lang)).upper()) not in ("C", "N", "A", "U"):
        print(langs.get_ui_text("invalid_option", lang))

    # User enters custom element pool
    if poolChoice == "U":
        element_pool = utils.get_custom_element_pool()

    elif poolChoice == "C":
        element_pool = common_elements

    elif poolChoice == "N":
        element_pool = natural_elements

    elif poolChoice == "A":
        element_pool = all_elements

    element_question_type_pool = ["ENTS", "STEN", "COFE", "COFS"]
    polyatomic_ion_question_type_pool = ["PNTF", "FTPN", "PNTC", "PFTC"]

    question_type_weights = [0.15, 0.15, 0.1, 0.1, 0.15, 0.15, 0.1, 0.1]

    settings = {}

    # Add data
    settings.update({"lang": lang})
    settings.update({"element_question_type_pool": element_question_type_pool})
    settings.update({"polyatomic_ion_question_type_pool": polyatomic_ion_question_type_pool})
    settings.update({"element_pool": element_pool})
    settings.update({"polyatomic_ion_pool": polyatomic_ion_pool})
    settings.update({"question_count": question_count})
    settings.update({"question_type_weights": question_type_weights})
    settings.update({"charge_order_sensitive": charge_order_sensitive})

    return settings

def run_quiz(settings: dict):
    lang = settings["lang"]

    element_question_type_pool = settings["element_question_type_pool"]
    polyatomic_ion_question_type_pool = settings["polyatomic_ion_question_type_pool"]

    element_pool = settings["element_pool"]
    polyatomic_ion_pool = settings["polyatomic_ion_pool"]

    question_count = settings["question_count"]
    question_type_weights = settings["question_type_weights"]

    charge_order_sensitive = settings["charge_order_sensitive"]

    # Generate questions and answers
    questions, answers, question_types = generate_questions(element_question_type_pool, polyatomic_ion_question_type_pool, element_pool, polyatomic_ion_pool, question_count, lang, question_type_weights, return_question_types=True)

    # Amoutn of characters to type all answers
    answer_char_count = sum(len(s) for s in answers)

    start_time = time.time_ns()

    points = 0

    for i in range(question_count):
        # Generate question and answer
        print("\n" + questions[i])
        response = input(langs.get_ui_text("ask_answer", lang))

        # Check if the answer is correct
        correct_answer = utils.check_answer(response, answers[i], question_types[i], lang, charge_order_sensitive)

        # Check if the answer is correct
        if correct_answer:

            # Print correct answer
            print(langs.get_ui_text("correct_answer", lang))
            points += 1
        
        # Print incorrect answer
        else:
            print(langs.get_ui_text("incorrect_answer", lang).replace("{0}", answers[i]))

    end_time = time.time_ns()

    time_used = (end_time-start_time) / 1_000_000_000

    print(langs.get_ui_text("quiz_time", lang).format(round(time_used, 2), round(time_used/question_count, 3)))
    print(langs.get_ui_text("quiz_time_per_char", lang).format(round(time_used/answer_char_count*1000), answer_char_count))
    print(langs.get_ui_text("final_score", lang).format(points, question_count, points/question_count*100))
    print(f"\n{'*'*40}\n\n")

if __name__ == "__main__":
    updater.run(LANG)
    while True:
        settings = get_quiz_settings(LANG)
        run_quiz(settings)

        if input(langs.get_ui_text("do_another_quiz", LANG)).upper() not in langs.get_ui_text("confirm", LANG):
            break