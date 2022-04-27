import tkinter as tk
import csv
import random
from collections import namedtuple

########### CONSTANTS #####################

BACKGROUND_COLOR = "#B1DDC6"

########### GET WORDS #####################

Card = namedtuple("Card", ["French", "English"])


def read_card_list(f):
    csv_reader = csv.reader(f)
    next(csv_reader)  # skip header row
    return [Card(*row) for row in csv_reader]


try:
    with open("data/words_to_learn.csv", "r", encoding="utf-8") as f:
        card_list = read_card_list(f)
except FileNotFoundError:
    with open("data/french_words.csv", "r", encoding="utf-8") as f:
        card_list = read_card_list(f)


########### SHOW CARDS #####################

current_card = random.choice(card_list)


def show_next_card():
    global current_card, flip_card_timer
    window.after_cancel(flip_card_timer)
    current_card = random.choice(card_list)
    canvas.itemconfig(card_word, text=current_card.French, fill="black")
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_bg, image=card_front_img)
    flip_card_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_word, text=current_card.English, fill="white")
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_bg, image=card_back_img)


def learn_card():
    card_list.remove(current_card)
    with open("data/words_to_learn.csv", "w", newline="", encoding="utf-8") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["French", "English"])
        for card in card_list:
            csv_writer.writerow(list(card))

    show_next_card()


########### SETUP UI #####################

# Window
window = tk.Tk()
window.title("Flash Card")
window.configure(padx=50, pady=50, background=BACKGROUND_COLOR)

# Canvas
canvas = tk.Canvas(
    width=800, height=526, background=BACKGROUND_COLOR, highlightthickness=0
)

card_back_img = tk.PhotoImage(file="images/card_back.png")
card_front_img = tk.PhotoImage(file="images/card_front.png")
card_bg = canvas.create_image(400, 263, image=card_back_img)

card_title = canvas.create_text(400, 150, text="Title", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="word", font=("Arial", 60, "bold"))

canvas.grid(column=0, row=0, columnspan=2)

# Buttons
check_img = tk.PhotoImage(file="images/right.png")
cross_img = tk.PhotoImage(file="images/wrong.png")
check_btn = tk.Button(image=check_img, highlightthickness=0, command=learn_card)
cross_btn = tk.Button(image=cross_img, highlightthickness=0, command=show_next_card)
check_btn.grid(column=0, row=1)
cross_btn.grid(column=1, row=1)


########### START #####################

flip_card_timer = window.after(3000, flip_card)
show_next_card()
window.mainloop()
