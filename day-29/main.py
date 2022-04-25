import random
import string
import tkinter as tk
from tkinter import messagebox
import csv

import pyperclip

DEFAULT_EMAIL = "letuanhai@live.com"
PW_FILE = "data.csv"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


symbols = ["!", "#", "$", "%", "&", "(", ")", "*", "+"]


def gen_pw():

    password_list = (
        [random.choice(string.ascii_letters) for _ in range(random.randint(8, 10))]
        + [random.choice(symbols) for _ in range(random.randint(2, 4))]
        + [random.choice(string.digits) for _ in range(random.randint(2, 4))]
    )

    random.shuffle(password_list)

    password = "".join(password_list)

    pyperclip.copy(password)

    password_entry.delete(0, tk.END)
    password_entry.insert(0, string=password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_entry.get()
    email = email_entry.get()
    pw = password_entry.get()

    if any(len(s) == 0 for s in (website, email, pw)):
        messagebox.showerror(
            title="Oops", message="Please don't leave any field empty!"
        )
    else:

        is_ok = messagebox.askokcancel(
            title=website,
            message=f"These are the details entered: \nEmail: {email}\nPassword: {pw}\nIs it OK to save?",
        )

        if is_ok:
            with open(PW_FILE, "a", newline="") as f:
                csv_writer = csv.writer(f, dialect="excel")
                csv_writer.writerow((website, email, pw))
                website_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = tk.Canvas(width=200, height=200)
logo_img = tk.PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = tk.Label(text="Website:")
website_label.grid(column=0, row=1)
website_entry = tk.Entry(width=50)
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

email_label = tk.Label(text="Email/Username:")
email_label.grid(column=0, row=2)
email_entry = tk.Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, DEFAULT_EMAIL)

password_label = tk.Label(text="Password:")
password_label.grid(column=0, row=3)
password_entry = tk.Entry(width=30)
password_entry.grid(column=1, row=3)
gen_pw_btn = tk.Button(text="Generate Password", width=16, command=gen_pw)
gen_pw_btn.grid(column=2, row=3)

add_btn = tk.Button(text="Add", width=42, command=save_password)
add_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()
