import tkinter as tk
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20

reps = 0
timer_started = False
timer = ""

# ---------------------------- TIMER RESET ------------------------------- #


def reset_timer():
    window.after_cancel(timer)
    canvas.itemconfig(
        timer_text, text="00:00", fill="white", font=(FONT_NAME, 30, "bold")
    )
    title.config(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
    global reps
    global timer_started
    reps = 0
    timer_started = False
    checkmarks.config(text="")


# ---------------------------- TIMER MECHANISM ------------------------------- #


def start_timer():
    global timer_started
    global reps
    reps += 1
    if not timer_started:
        timer_started = True
        if reps % 8 == 0:
            title.config(text="Break", fg=RED)
            count_down(60 * LONG_BREAK_MIN)
        elif reps % 2 == 0:
            title.config(text="Break", fg=PINK)
            count_down(60 * SHORT_BREAK_MIN)
        else:
            title.config(text="Work", fg=GREEN)
            count_down(60 * WORK_MIN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #


def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        global timer_started
        timer_started = False
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        checkmarks.config(text=marks)


# ---------------------------- UI SETUP ------------------------------- #
window = tk.Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

canvas = tk.Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = tk.PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 30, "bold")
)
canvas.grid(column=1, row=1)

title = tk.Label(text="Timer", font=(FONT_NAME, 40, "bold"), fg=GREEN, bg=YELLOW)
title.grid(column=1, row=0)

start_button = tk.Button(
    text="Start",
    font=(FONT_NAME, 10, "bold"),
    fg="blue",
    highlightthickness=0,
    command=start_timer,
)
start_button.grid(column=0, row=2)

reset_button = tk.Button(
    text="Reset",
    font=(FONT_NAME, 10, "bold"),
    fg="blue",
    highlightthickness=0,
    command=reset_timer,
)
reset_button.grid(column=2, row=2)

checkmarks = tk.Label(text="", font=(FONT_NAME, 13, "bold"), fg=GREEN, bg=YELLOW)
checkmarks.grid(column=1, row=3)

window.mainloop()
