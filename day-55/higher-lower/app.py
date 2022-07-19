from random import randint
from flask import Flask

NUMBER = randint(0, 9)

app = Flask(__name__)


@app.route("/")
def index():
    return '<h1>Guess a number between 0 and 9</h1><img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif">'


@app.route("/<int:guess>")
def check(guess):
    if guess > NUMBER:
        return '<h1 style="color: red;">Too high, try again!</h1><img src="https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif">'
    elif guess < NUMBER:
        return '<h1 style="color: purple;">Too low, try again!</h1><img src="https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif">'
    else:
        return '<h1 style="color: green;">Correct!</h1><img src="https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif">'


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)  # run on host 0.0.0.0 due to being on WSL2
