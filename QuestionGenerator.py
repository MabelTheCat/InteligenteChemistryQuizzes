import re

import utils
import langs.langs as langs

QUESTIONS = ["ENTS", "STEN", "COFE", "COFS"]

def generate_element_questions(questionTypeOptions: list[str], pool: list[int], count: int = 1, lang: str = "en", questionTypeWeights: list[int] | None = None) -> tuple[list[str], list[str]]:
    """Generate element questions, given by `questionTypeOptions` and its answer from the `pool` provided.
    Chose question types randomly form `questionTypeOptions` with `questionTypeWeights`.
    `pool` is the list of allowed elements for the questions, provided as element ids (atomic number)"""
    # Choose the element that is wanted
    elementIds = utils.choose_elements_from_pool(pool, count)

    names = []
    symbols = []
    questions = []
    answers = []

    for id in elementIds:
        # Get name and symbol of the elemnt
        name = langs.get_element_name(id, lang)
        symbol = utils.get_element_data("number", id, "symbol")

        # Add name and symbol to list
        names.append(name)
        symbols.append(symbol)

    questionIds = utils.random.choices(questionTypeOptions, questionTypeWeights, k=count)

    for i, q in enumerate(questionIds):

        # Create the question
        if q in ("STEN", "COFE"):
            question = langs.add_contractions(langs.get_question_text(q, lang), symbols[i], lang=lang)
            questions.append(question)
        
        # Ask with the symbol
        elif q in ("ENTS", "COFS"):
            question = langs.add_contractions(langs.get_question_text(q, lang), names[i].lower(), lang=lang)
            questions.append(question)

        else:
            raise Exception(f"Invalid question id {q}.")
        
        # Find answers
        # Answers are the element symbols
        if q == "ENTS":
            answers.append(symbols[i])

        # Answers are the element names
        elif q == "STEN":
            answers.append(names[i])

        # Answer is the charge of the element (name or symbol provided)
        elif q in ("COFE", "COFS"):
            # Get charge(s)
            charges = utils.get_element_data("number", elementIds[i], "charges")

            charges = utils.format_charges(charges)

            answers.append(charges)

        else:
            raise ValueError(f"'{q}' is not a valid question id for generate_element_questions.")
    
    return (questions, answers)

def generate_polyatomic_ion_questions(questionTypes: list[str], pool: list[int], count: int = 1, lang: str = "en", questionTypeWeights: list[int] | None = None) -> tuple[list[str], list[str]]:
    """Valid question types: PNTF, FTPN"""
    questionIds = utils.random.choices(questionTypes, questionTypeWeights, k=count)

    questions, answers = [], []

    polyatomicIonIds = utils.choose_elements_from_pool(pool, count)

    for i, questionId in enumerate(questionIds):

        # Polyatomic ion name to formula
        if questionId == "PNTF":
            questions.append(langs.add_contractions(langs.get_question_text(questionId, lang), langs.get_polyatomic_ion_name(polyatomicIonIds[i], lang), lang=lang))
            answers.append(utils.get_polyatomic_ion_data("num", polyatomicIonIds[i], "formula"))

        # Polyatomic ion formula to name
        elif questionId == "FTPN":
            questions.append(langs.get_question_text(questionId, lang).format(utils.get_polyatomic_ion_data("num", polyatomicIonIds[i], "formula")))
            answers.append(langs.get_polyatomic_ion_name(polyatomicIonIds[i], lang))

        # Polyatomic ion charge from name
        elif questionId == "PNTC":
            questions.append(langs.add_contractions(langs.get_question_text(questionId, lang), langs.get_polyatomic_ion_name(polyatomicIonIds[i], lang), lang=lang))
            
            # Get charge(s)
            charge = f"[{utils.get_polyatomic_ion_data('num', polyatomicIonIds[i], 'charge')}]"
            charge = utils.format_charges(charge)
            answers.append(charge)
        
        # Polyaomic ion charge from formula
        elif questionId == "PFTC":
            questions.append(langs.get_question_text(questionId, lang).format(utils.get_polyatomic_ion_data("num", polyatomicIonIds[i], "formula")))
            
            # Get charge(s)
            charge = f"[{utils.get_polyatomic_ion_data('num', polyatomicIonIds[i], 'charge')}]"
            charge = utils.format_charges(charge)
            answers.append(charge)
    
    return (questions, answers)

def generate_questions(element_question_types: list[str], polyatomic_ion_question_types: list[str], element_pool: list[int], polyatomic_ion_pool: list[int], count: int = 1, lang: str = "en", questionTypeWeights: list[int] | None = None, return_question_types: bool = False) -> tuple[list[str], list[str], list[str]] |  tuple[list[str], list[str]]:
    """Generates questions."""
    questionIds = utils.random.choices(element_question_types + polyatomic_ion_question_types, weights=questionTypeWeights, k=count)

    element_question_count = sum(questionIds.count(val) for val in element_question_types)

    polyatomic_ion_question_count = sum(questionIds.count(val) for val in polyatomic_ion_question_types)

    # Generate questions
    p1 = generate_element_questions(element_question_types, element_pool, element_question_count, lang, questionTypeWeights[:4])
    p2 = generate_polyatomic_ion_questions(polyatomic_ion_question_types, polyatomic_ion_pool, polyatomic_ion_question_count, lang, questionTypeWeights[4:8])

    # Combine questions and answers
    questions = []
    answers = []

    p1_count = 0
    p2_count = 0

    for _ in range(count):
        if p1_count < len(p1[0]):
            if utils.random.choices([0, 1], [1-p1_count/count, 1-p2_count/count]) == [0] or p2_count >= len(p2[0]):
                questions.append(p1[0][p1_count])
                answers.append(p1[1][p1_count])
                p1_count += 1

            else:
                questions.append(p2[0][p2_count])
                answers.append(p2[1][p2_count])
                p2_count += 1
        
        else:
            questions.append(p2[0][p2_count])
            answers.append(p2[1][p2_count])
            p2_count += 1

    qTypes = ("ENTS", "STEN", "COFE", "COFS", "PNTF", "FTPN", "PNTC", "PFTC")
    types = []
    for question in questions:
        for qType in qTypes:
            if question.startswith(langs.get_question_text(qType, lang).split("{")[0]):
                types.append(qType)
                break
    
    if return_question_types:
        return (questions, answers, types)

    else:
        return (questions, answers)
