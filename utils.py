import os
import json
import random
import re
from typing import Literal

import langs.langs as langs

# Seeding
def _init(lang: str):
    """Initialise random number generator"""
    if input(langs.get_ui_text("utils.use_random_seed", lang)).upper() in langs.get_ui_text("confirm", lang):
        seed = random.randint(0, 2**31-1)
        random.seed(seed)
        print(langs.get_ui_text("utils.give_quiz_seed_value", lang).format(seed))

    else:
        while not re.fullmatch(r"\d+", (seed := input(langs.get_ui_text("utils.enter_quiz_seed", lang)))):
            print(langs.get_ui_text("utils.invalid_quiz_seed_entered", lang))
        
        random.seed(int(seed))
        

# Filepath constants
ELEMENT_FILE_NAME = "PeriodicTableJSON.json"
ELEMENT_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
ELEMENT_FILE_PATH = os.path.join(ELEMENT_FOLDER_PATH, ELEMENT_FILE_NAME)

POLYATOMIC_ION_FILE_NAME = "PolyatomicIons.json"
POLYATOMIC_ION_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
POLYATOMIC_ION_FILE_PATH = os.path.join(POLYATOMIC_ION_FOLDER_PATH, POLYATOMIC_ION_FILE_NAME)

QUESTION_DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "QuestionData.json")

# Load elements
with open(ELEMENT_FILE_PATH, "r", encoding="utf-8") as datasheet:
    ELEMENTS: dict = json.load(datasheet)["elements"]

ELEMENT_COUNT = len(ELEMENTS)

# Load polyatomic ions
with open(POLYATOMIC_ION_FILE_PATH, "r", encoding="utf-8") as datasheet:
    POLYATOMIC_IONS: dict = json.load(datasheet)

# Load question data
with open(QUESTION_DATA_PATH, "r", encoding="utf-8") as datasheet:
    QUESTION_DATA: dict = json.load(datasheet)

def get_question_generation_data(question_type: str) -> dict:
    return QUESTION_DATA[question_type]["generation_data"]

def check_answer(user_answer: str, correct_answer: str, questionType: str, lang: str, charge_order_sensitive: bool = True):
    # Check if the question is case-sensitive
    case_sensitive_answer = QUESTION_DATA[questionType]["captialisation_sensitive"]

    # Check if the answer is space-sensitive
    space_sensitive_answer = QUESTION_DATA[questionType]["space_sensitive"]
    
    # Make case-sensitive adjustments, if necessary
    if not case_sensitive_answer:
        user_answer = user_answer.lower()
        correct_answer = correct_answer.lower()
    
    # Make space-sensitive adjustments, if necessary
    if not space_sensitive_answer:
        user_answer = user_answer.replace(" ", "")
        correct_answer = correct_answer.replace(" ", "")

    if not charge_order_sensitive:
        # Order the charges
        user_answer = user_answer.split(",")
        user_answer.sort()

        answer_copy = correct_answer.split(",")
        answer_copy.sort()

        # Check the charges
        if user_answer == answer_copy:
            is_answer_correct = True

        else:
            is_answer_correct = False

    # Default action
    else:
        is_answer_correct = user_answer == correct_answer

    return is_answer_correct

def get_custom_element_pool(allowDuplicates: bool = True) -> list[int]:
    """Returns a pool of elements, given by the user. `allowDuplicates` removes all duplicate entries when set to `False`."""
    pool = input(f"Enter a pool of elements' atomic numbers ({'enter an atomic number multiples times for it to be more common' if allowDuplicates else 'duplicates will be removed'}):\t")

    # Remove start and end parentheses
    pool = pool.strip("()[]{}")

    # Check that the pool is valid (optional parentheses, then a list of valid atomic number, each seperated by a comma and optional whitespace)
    if re.fullmatch(r"(([1-9]\d?|10\d|11[0-8]),\s*)*([1-9]\d?|10\d|11[0-8])\s*", pool):

        # Remove whitespace
        pool = pool.replace(" ", "").replace("  ", "").replace("\n", "")

        # Process
        pool = [int(v) for v in pool.split(",")]

        # Check if duplicates are allowed
        if not allowDuplicates:

            # Remove duplicates
            for val in pool:
                for _ in range(1, pool.count(val)):
                    pool.pop(pool.index(val, pool.index(val)+1))

        return pool
    
    # Invalid pool
    else:
        print("That is not a valid pool.")
        return get_custom_element_pool(allowDuplicates)

def choose_elements_from_pool(pool: list[int], k=1) -> int:
    """Chooses and returns `k` random element(s) from `pool`.
    All elements are chosen before any duplicates occur."""
    # Choose k random elements from the pool
    results = []

    # Choose max possible choices
    for _ in range(k//len(pool)):
        results += random.sample(pool, k=len(pool))
    
    # Choose any remaining choices
    results += random.sample(pool, k=k-len(pool)*(k//len(pool)))
    
    return results

def sample_element_from_pool(pool: list[int]):
    pass

def find_id(idType: str, id) -> int:
    """Gets the location of an element in the datasheet (staring at 0)
    `idType`: Type of id used to identify the element (atomic number, name, symbol, etc..)
    `id`: The id value of the element (12, Fe, iron, etc..)
    
    If multiple elemnts have the same id, the one first in the list (lowest atomic number) is chosen."""
    for i in range(ELEMENT_COUNT):
        if ELEMENTS[i][idType] == id:
            return i

def get_element_data(idType: str, id, wanted: str | list[str] | tuple[str] | None = None) -> dict | list:
    """Gets the data for an element. 
    `idType`: Type of id used to identify the element (atomic number, name, symbol, etc..)
    `id`: The id value of the element (12, Fe, iron, etc..)
    `wanted`: Requested data to return. If not given, returns all data on the element."""
    id = find_id(idType, id)
    if wanted is None:
        return ELEMENTS[id]
    else:
        # Just get the value wanted
        if type(wanted) == str:
            return ELEMENTS[id][wanted]
        
        # Get all the wanted elements
        vals = []
        for w in wanted:
            vals.append(ELEMENTS[id][w])

        return vals

def format_charges(charges: list[int]) -> str:
    # Format answer
    charges = str(charges)[1:-1].replace(" ", "")

    # Fix charges
    for char in ("-", "+", "1-", "1"):
        lindex = 0
        for _ in range(charges.count(char)):
            index = charges.index(char, lindex)

            if char in ("-", "+"):
                charges = charges[0:index] + charges[index+1] + char + charges[index+2:]
                lindex = index+2

            else:
                # Fix char's value
                if char == "1-":
                    char = "-"
                    charges = charges[0:index] + char + charges[index+2:]
                
                else:
                    char = "+"
                    charges = charges[0:index] + char + charges[index+1:]

                lindex = index+1
    
    # Fix positive charges (add + to number)
    charges = charges + " " # Add extra space for regex to work properly

    lindex = 0
    matchCount = len(re.findall(r"[1-9][^-]", charges))

    # Loop over each match
    for i in range(matchCount):
        index = re.search(r"[1-9][^-]", charges[lindex:]).span()[0] + lindex

        charges = charges[0:index+1] + "+" + charges[index+1:]

        lindex = index+3

    charges = charges[:-1]

    return charges

def get_element_type(element: int) -> str:
    """Returns the type of an element (metal, metalloid, or nonmetal)"""
    type = get_element_data("number", element, "category")

    # Metal
    if type in ("alkali metal", "alkaline earth metal", "transition metal", "post-transition metal"):
        return "metal"
    
    # Metalloid
    elif type == "metalloids":
        return "metalloid"
    
    # Nonetal
    elif "nonmetal" in type:
        return "nonmetal"
    
    else:
        raise Exception(f"Element {element}'s type was not found.")

def get_elements(formula: str) -> list[int]:
    """Returns the elements (by atomic number) from the formula."""
    elements = []

    for i, char in enumerate(formula):
        # Check if the character is an uppercase letter
        if char.isalpha() and (char.upper() == char):

            # Check if the next letter is lowercase
            if i < len(formula) - 1 and formula[i+1].isalpha() and (formula[i+1].lower() == formula[i+1]):
                elements.append(char + formula[i+1])
            
            else:
                elements.append(char)

    for i in range(len(elements)):
        elements[i] = get_element_data("symbol", elements[i], "number")
    
    return elements

def parse_formula(formula: str) -> list[dict[int, int]]:
    """Parses a formula. Elements only, no parentheses. Repeated elements are measured separately."""
    elements = []
    numbers = []
    
    i = 0
    while i < len(formula):
        # Check if the next letter is lowercase
        if i < len(formula) - 1 and formula[i+1].isalpha() and (formula[i+1].lower() == formula[i+1]):
            elements.append(formula[i] + formula[i+1])
            i += 2
        
        elif formula[i].isalpha():
            elements.append(formula[i])
            i += 1

        # Process numbers
        if i < len(formula) and formula[i].isdigit():
            number = ""
            while i < len(formula) and formula[i].isdigit():
                number += formula[i]
                i += 1

            numbers.append(int(number))
        
        else:
            numbers.append(1)

    results = []

    for i in range(len(elements)):
        elements[i] = get_element_data("symbol", elements[i], "number")
        results.append({elements[i]: numbers[i]})
    
    return results

def get_polyatomic_ion_data(idType: str, id, wanted: str) -> str:
    """Returns the `wanted` data form a chosen polyatomic ion."""
    if idType == "num":
        return POLYATOMIC_IONS[str(id)][wanted]
    
    else:
        for i in range(len(POLYATOMIC_IONS)):
            if POLYATOMIC_IONS[i][idType] == id:
                return POLYATOMIC_IONS[i][idType][wanted]
    
    raise # Wanted request not found

def get_roman_numeral(num: int | str) -> str:
    """Returns the roman numeral of the number."""
    num = str(num)

    result = ""

    if num in ("1", "2", "3"):
        result = "I" * int(num)
    
    elif num == "4":
        result = "IV"

    elif num in ("5", "6", "7", "8"):
        result = f"V{'I' * (int(num) - 5)}"
    
    elif num == "9":
        result = "IX"
    
    elif num == "10":
        result = "X"
    
    else:
        raise Exception(f"{num} is not supported for roman numeral conversion.")

    return result

def name_molecule_elemental(formula: str, lang: str, skip_mono: bool = True, naming: Literal["roman"] | Literal["suffix"] = "roman") -> str:
    """Names a molecule composed of two elements. `skip_mono` removes all mono prefixes.
    `naming` selects whether to put charges as roman numerals or as suffixes.
    Example (FeCl2): roman: iron (II) chloride, suffix: ferrous chloride"""
    ionic_binary = False
    covalent_binary = False

    # Get the elements and element counts
    (e1, e1_count), (e2, e2_count) = parse_formula(formula)

    # Ionic binary compound
    if ((get_element_type(e1) == "metal") ^ (get_element_type(e2) == "metal")) and ((get_element_type(e1) == "nonmetal") ^ (get_element_type(e2) == "nonmetal")):
        ionic_binary = True # TODO? Add electronegativity differences

    # Covalent 
    elif get_element_type(e1) == "nonmetal" and get_element_type(e2) == "nonmetal":
        covalent_binary = True

    assert ionic_binary ^ covalent_binary, "Molecule must be ionic XOR covalent"

    n1 = langs.get_prefix(e1_count, lang)
    n2 = langs.get_prefix(e2_count, lang)

    # Get information for an ionic binary compound
    if ionic_binary:
        nonmetal = e1 if get_element_type(e1) == "nonmetal" else e2
        metal = e2 if e1 == nonmetal else e1

        metal_count = e1_count if e1 == metal else e2_count
        nonmetal_count = e1_count if e2 == metal else e2_count
        metal_charge = int(-nonmetal_count * get_element_data("number", nonmetal, "charges")[0] / metal_count)

        multi_charge = True if len(get_element_data("number", metal, "charges")) > 1 else False
    
    # Get information for a covalent binary compound
    if covalent_binary:
        # Not oxygen and a halogen
        if not ((e1 == 8 and get_element_data("number", e2, "group") == 17) or (e2 == 8 and get_element_data("number", e1, "group") == 17)):
            first = e1 if get_element_data("number", e1, "group") < get_element_data("number", e2, "group") or (e1 > e2 and get_element_data("number", e1, "group") == get_element_data("number", e2, "group")) else e2
            second = e2 if first == e1 else e1
        
        # Oxygen and a halogen (exception)
        else:
            first = 8
            second = e2 if e1 == 8 else e1
    
    # Get suffix(es) for the elements
    if lang == "en":
        # Get suffix
        if metal_charge == max(get_element_data("number", metal, "charges")):
            suffix = "ic"
        else:
            suffix = "ous"

    elif lang == "fr":
        # Get suffix
        if metal_charge == max(get_element_data("number", metal, "charges")):
            suffix = "ique"

        else:
            suffix = "eux"
            
            nm_suffix = 'ure' if nonmetal != 8 else 'yde'
    
    # Get name
    if lang == "fr":
        if ionic_binary:

            name = f"{langs.get_root(nonmetal, lang)}{nm_suffix} de {langs.get_element_name(metal, lang)}"

            if multi_charge:
                # Add roman numerals
                if naming == "roman":
                    name = name + f" ({get_roman_numeral(metal_charge)})"
                
                # Change suffix
                elif naming == "suffix":
                    name = f"{langs.get_root(nonmetal, lang)}{nm_suffix} {langs.get_root(metal, lang)}{suffix}"  

        elif covalent_binary:
            name = f"{n2 if first == e1 else n1}{langs.get_root(second, lang)}{nm_suffix} de {n1 if first == e1 else n2}{langs.get_element_name(first, lang)}"
        
    elif lang == "en":
        if ionic_binary:
            # Multiple possible charges for the metal
            if multi_charge:
                
                # Add roman numerals
                if naming == "roman":
                    name = f"{langs.get_element_name(metal, lang)} ({get_roman_numeral(metal_charge)}) {langs.get_root(nonmetal, lang)}ide"
                
                # Change suffix
                elif naming == "suffix":
                    name = f"{langs.get_root(metal, lang)}{suffix} {langs.get_root(nonmetal, lang)}ide"
            
            else:
                name = f"{langs.get_element_name(metal, lang)} {langs.get_root(nonmetal, lang)}ide"
        
        elif covalent_binary:
            name = f"{n2 if first == e1 else n1}{langs.get_element_name(first, lang)} {n1 if first == e1 else n2}{langs.get_root(second, lang)}ide"

    else:
        raise Exception(f"Language {lang} not supported")
    
    # Remove mono prefixes
    if skip_mono:
        name = name.replace("mono", "")
    
    # Fix stuff like monooxide, pentaoxyde
    name = name.replace("aox", "ox").replace("oox", "ox")
    
    return name

# Test code
if __name__ == "__main__":
    # while True:
    #     formula = input("Enter formula:\t")
    #     if not re.fullmatch(r"([A-Z][a-z]?\d?){2}", formula):
    #         print("That is not a valid formula.")
        
    #     else:
    #         print(f"Name: {name_molecule_elemental(formula, input("Language:\t"))}\n")

    while True:
        formula = input("Enter formula:\t")
        print(f"Parsed formula: {parse_formula(formula)}")