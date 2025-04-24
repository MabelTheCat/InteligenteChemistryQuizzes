points = 0

def name_to_symbol_iron():
    global points
    print("What is the symbol for iron?")
    if input("Symbol:\t") == "Fe":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'Fe'.")
    
def symbol_to_name_C():
    global points
    print("What is the name for the element C?")
    if input("Name:\t").upper() == "CARBON":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'carbon'.")

def valence_to_group():
    global points
    print("What is the group for element X with charge -?")
    if input("Group:\t").upper() == "HALOGENS":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'halogens'.")

def group_to_valence():
    global points
    print("What is the charge for element X in group 'alkali metals'?")
    if input("Charge:\t") == "+":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's '+'.")
        print("When a charge is +1 or -1, the number is ommited. The charge is thus displayed as + or -.")

def name_to_charge_calcium():
    global points
    print("What is the charge for calcium?")
    if input("Charge:\t") == "2+":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's '2+'.")

def molecule_name_Na2SO4():
    global points
    print("What is the name of Na2SO4?")
    if input("Name:\t").upper() == "SODIUM SULFATE":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'sodium sulfate'.")

def molecule_formula_calcium_carbonate():
    global points
    print("What is the formula of calcium carbonate?")
    if input("Formula:\t") == "CaCO3":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'CaCO3'.")

def acid_base_result():
    global points
    print("What is the missing product in HCL + NaOH -> H2O + ___?")
    if input("Product:\t") == "NaCl":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'NaCl'.")

def acid_unknown_base():
    global points
    print("What is the missing reagent in H2SO4 + 2 ___ -> 2 H2O + Na2SO4?")
    if input("Reagent:\t") == "NaOH":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'NaOH'.")

def unknown_fuel_combustion():
    global points
    print("What is the missing fuel in 2 ___ + O2 -> 4 CO2 + 6 H2O?")
    if input("Fuel:\t") == "C2H6":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'C2H6'.")

def balance_equation():
    global points
    print("What is the balanced equation for CaCl2 + Na -> NaCl + Ca?")
    if input("Balanced Equation:\t").replace(" ", "") == "CaCl2+2Na->2NaCl+Ca":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'CaCl2 + 2 Na -> 2 NaCl + Ca'.")

def determine_reaction_type_dd():
    global points
    print("What is the reaction type for CaCl2 + Na2SO4 -> 2 NaCl + CaSO4?")
    if input("Reaction Type:\t").upper() in ("DOUBLE DISPLACEMENT", "DOUBLE REPLACEMENT", "DOUBLE-REPLACEMENT"):
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'double displacement'.")

def determine_reaction_type_ab():
    global points
    print("What is the reaction type for H2SO4 + Ca(OH)2 -> 2 H2O + CaSO4?")
    answer = input("Reaction Type:\t").upper()
    if answer == "NEUTRALISATION":
        print("Correct!")
        points += 1

    elif answer in ("DOUBLE DISPLACEMENT", "DOUBLE REPLACEMENT", "DOUBLE-REPLACEMENT"):
        print("Correct, but the answer 'neutralisation' is best!")
        print("This is because H2SO4 is an acid and Ca(OH)2 is a base, thus making a neutralisation reaction.")
        points += 0.5
    
    else:
        print("Wrong! It's 'neutralisation'.")

def name_to_symbol_barium():
    global points
    print("What is the symbol for barium?")
    if input("Symbol:\t") == "Ba":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'Ba'.")
    
def symbol_to_name_Cl():
    global points
    print("What is the name for the element Cl?")
    if input("Name:\t").upper() == "CHLORINE":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'chlorine'.")

def molecule_name_KOH():
    global points
    print("What is the name of KOH?")
    if input("Name:\t").upper() == "POTASSIUM HYDROXYDE":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'potassium hydroxyde'.")

def molecule_formula_dinitrogen_pentoxyde():
    global points
    print("What is the formula of dinitrogen pentoxyde?")
    if input("Formula:\t") == "N2O5":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'N2O5'.")

def name_to_charge_iodine():
    global points
    print("What is the charge of iodine?")
    if input("Charge:\t") == "-":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's '-'.")

def determine_reaction_type_s():
    global points
    print("What is the reaction type of 2 Fe + 3 Cl2 -> 2 FeCl3?")
    if input("Reaction Type:\t").upper() == "SYNTHESIS":
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'synthesis'.")

def determine_if_reaction_occurs_CuOH_Na():
    global points
    print("Will the following reaction happen? CuOH + Na -> NaOH + Cu")
    if input("Y/N:\t").upper() in ("Y", "YES"):
        print("Correct!")
        points += 1
    else:
        print("Wrong! It's 'yes'.")

if __name__ == "__main__":
    print("This is a concept test for a chemisty flashcards app.")
    QUESTION_COUNT = 20
    name_to_symbol_iron()
    determine_reaction_type_s()
    molecule_formula_calcium_carbonate()
    acid_unknown_base()
    name_to_charge_calcium()
    molecule_name_KOH()
    balance_equation()
    group_to_valence()
    name_to_symbol_barium()
    determine_reaction_type_dd()
    symbol_to_name_C()
    determine_if_reaction_occurs_CuOH_Na()
    name_to_charge_iodine()
    valence_to_group()
    symbol_to_name_Cl()
    molecule_formula_dinitrogen_pentoxyde()
    unknown_fuel_combustion()
    molecule_name_Na2SO4()
    acid_base_result()
    determine_reaction_type_ab()

    print(f"Your final score is {points}/{QUESTION_COUNT} ({points/QUESTION_COUNT*100:.0f}%).")