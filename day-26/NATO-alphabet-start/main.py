import pandas as pd

# TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}
df = pd.read_csv(
    r"C:\Users\hai.letuan\python_projects\100-days-of-code\day-26\NATO-alphabet-start\nato_phonetic_alphabet.csv"
)
letter_dict = {row["letter"]: row["code"] for (index, row) in df.iterrows()}

# TODO 2. Create a list of the phonetic code words from a word that the user inputs.
def generate_phonetic():
    user_input = input("Enter a word: ")
    try:
        print([letter_dict[l] for l in user_input.upper()])
    except KeyError:
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()


generate_phonetic()
