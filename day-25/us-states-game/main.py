import turtle
import csv

# read list of states
states_coor = {}
with open("50_states.csv") as f:
    state_list = csv.reader(f)
    # skip column names
    next(state_list)
    for line in state_list:
        states_coor[line[0]] = float(line[1]), float(line[2])

screen = turtle.Screen()
screen.title("U.S. States Game")
image = "blank_states_img.gif"
screen.addshape(image)

turtle.shape(image)
correct_answers = set()

while len(correct_answers) < 50:
    answer_state = screen.textinput(
        title=f"{len(correct_answers)}/50 States Correct",
        prompt="What's another state's name?",
    )
    answer_state = answer_state.title() if answer_state else ""
    if answer_state == "Exit":
        break

    if answer_state in states_coor:
        correct_answers.add(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        t.goto(states_coor[answer_state])
        t.write(answer_state)

missed_states = set(states_coor.keys()).difference(correct_answers)
with open("states_to_learn.csv", "w", newline="") as f:
    csv_writer = csv.writer(f)
    for row in enumerate(missed_states):
        csv_writer.writerow(row)

# screen.exitonclick()

# get coordinate of each state on image
# def get_mouse_click_coor(x, y):
#     print(x, y)
# turtle.onscreenclick(get_mouse_click_coor)
# turtle.mainloop()
