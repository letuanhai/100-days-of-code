# TODO: Create a letter using starting_letter.txt
# for each name in invited_names.txt
# Replace the [name] placeholder with the actual name.
# Save the letters in the folder "ReadyToSend".

# Hint1: This method will help you: https://www.w3schools.com/python/ref_file_readlines.asp
# Hint2: This method will also help you: https://www.w3schools.com/python/ref_string_replace.asp
# Hint3: THis method will help you: https://www.w3schools.com/python/ref_string_strip.asp

from pathlib import Path

starting_letter = r"Input/Letters/starting_letter.txt"
invited_names = r"Input/Names/invited_names.txt"

with open(starting_letter, "r") as f:
    letter_template = f.read()

with open(invited_names, "r") as f:
    invite_list = [line.rstrip("\n") for line in f.readlines()]

output_dir = Path("Output/ReadyToSend")

for name in invite_list:
    with open(output_dir / f"{name}.txt", "w") as f:
        f.write(letter_template.replace("[name]", name))
