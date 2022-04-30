import tkinter as tk
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain) -> None:
        self.quiz = quiz_brain
        self.window = tk.Tk()
        self.window.title("Quizzler")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)

        self.canvas = tk.Canvas(width=300, height=250, bg="white")
        self.q_text = self.canvas.create_text(
            150,
            125,
            width=280,
            text="Question text",
            font=("Arial", 15, "italic"),
            fill=THEME_COLOR,
        )
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)

        self.score_text = tk.Label(text="Score: 0", fg="white", background=THEME_COLOR)
        self.score_text.grid(column=1, row=0)

        true_img = tk.PhotoImage(file="./images/true.png")
        self.true_btn = tk.Button(
            image=true_img, highlightthickness=0, command=self.check_true
        )
        self.true_btn.grid(column=0, row=2)

        false_img = tk.PhotoImage(file="./images/false.png")
        self.false_btn = tk.Button(
            image=false_img, highlightthickness=0, command=self.check_false
        )
        self.false_btn.grid(column=1, row=2)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg="white")
        if self.quiz.still_has_questions():
            q_text = self.quiz.next_question()
            self.canvas.itemconfig(self.q_text, text=q_text)
            self.score_text.config(text=f"Score: {self.quiz.score}")
        else:
            self.canvas.itemconfig(
                self.q_text, text="You've reach the end of the quiz."
            )
            self.true_btn.config(state="disabled")
            self.false_btn.config(state="disabled")

    def check_true(self):
        self.give_feedback(self.quiz.check_answer("true"))

    def check_false(self):
        self.give_feedback(self.quiz.check_answer("false"))

    def give_feedback(self, is_right: bool):
        if not is_right:
            self.canvas.config(bg="red")
        else:
            self.canvas.config(bg="green")

        self.window.after(1000, self.get_next_question)
