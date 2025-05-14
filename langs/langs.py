import os
import json
import re

_LANG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
_LANGS = ("en", "fr")
_LANGS_TO_PRELOAD = ("en", "fr")

_loaded_langs = []
_DB = {}

def _load_lang(lang: str) -> None:
    """Loads a language to `_DB` and adds it to `_loaded_langs`. Raises an error if the file is not found."""
    global _loaded_langs, _DB
    path = os.path.join(_LANG_FOLDER_PATH, f"{lang}.json")

    if lang not in _LANGS:
        raise Exception(f"Language '{lang}' not supported!")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"Language file '{lang}' missing.")

    with open(path, "r", encoding="utf-8") as fo:
        _DB.update({lang: json.load(fo)})
        _loaded_langs.append(lang)

for lang in _LANGS_TO_PRELOAD:
    _load_lang(lang)

def _check_lang(lang: str):
    if lang not in _loaded_langs:
        _load_lang(lang)

def get_element_name(atomic_number: int, lang: str):
    """Returns the name of the element with the specified atomic number in the provided language."""
    _check_lang(lang)
    return _DB[lang]["elements"][f"{atomic_number}"].lower()

def get_root(atomic_number: int, lang: str) -> str:
    """Returns the root of the given element.
    \nExample: `get_root(17, "en")` -> `chlor`
    \nExample: `get_root(9, "fr")` -> `fluor`"""
    if _DB[lang]["element_roots"][f"{atomic_number}"] in ("", None):
        print(f"element root({atomic_number}) not yet added for {lang}.")
    return _DB[lang]["element_roots"][f"{atomic_number}"]

def get_question_text(questionId: str, lang: str) -> str:
    """Returns the chosen question in the selected language.
    The question id is the acronym for the question.


    \nENTS: what is the Element Name To Symbol
    \nSTEN: what is the Symbol To Element Name
    \nCOFE: what is the Charge(s) of element
    \nCOFS: what is the Charge(s) of symbol """
    _check_lang(lang)
    return _DB[lang]["questions"][questionId]

def get_ui_text(textId: str, lang: str) -> str:
    """Returns the chosen UI text in the selected language."""
    _check_lang(lang)
    return _DB[lang]["ui"][textId]

def add_contractions(text: str, *items, lang: str):
    """Adds the contractions to a sentance, if necessary.
    \nEx: add_contractions("chlorure de {0}", "aluminium", lang="fr") -> chlorure d'aluminium, instead of chlorure de aluminium"""

    result = text.format(*items)

    if lang == "en":
        None # Nothing to do?

    elif lang == "fr":
        for match in re.finditer(r"(de|du|le|la) (\{\d+\})", text, re.IGNORECASE):
            if items[int(match.group(2)[1:-1])][0].upper() in "AEIOU" or items[int(match.group(2)[1:-1])].upper() in ("HYDROGÈNE, HÉLIUM"):
                result = f"{result[:match.start()+1]}\'{result[match.start()+len(match.group())-3:]}"
    
    else:
        raise Exception(f"Language '{lang}' not supported")
    
    return result

def get_prefix(num: int | str, lang: str) -> str:
    """Gets the prefix for the number.
    Example: `get_prefix(1)` -> `"mono"`"""
    if 0 < int(num) and int(num) < 11:
        return _DB[lang]["prefixes"][str(num)]
    raise Exception(f"The prefix for {num} is not supported.")

def get_updater_item(textId: str, lang: str) -> str:
    """General function to get any item from `_DB`"""
    return _DB[lang]["updater"][textId]

def get_updater_item(textId: str, lang: str) -> str:
    """General function to get any item from `_DB`"""
    return _DB[lang]["updater"][textId]

def get_polyatomic_ion_name(id: int | str, lang: str) -> str:
    """Returns the name of the polyatomic ion in the requested language."""
    return _DB[lang]["polyatomic_ions"][str(id)]

if __name__ == "__main__":
    while True:
        print(add_contractions(input("Enter text:\t"), input("Enter item:\t"), lang="fr"))