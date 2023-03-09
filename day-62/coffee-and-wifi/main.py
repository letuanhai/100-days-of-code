from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label="Cafe name", validators=[DataRequired()])
    location_url = StringField(
        label="Cafe Location (Google Maps URL)",
        validators=[DataRequired(), URL(require_tld=True)],
    )
    open_time = StringField(label="Opening Time e.g. 8AM", validators=[DataRequired()])
    closing_time = StringField(
        label="Closing Time e.g. 5.30PM", validators=[DataRequired()]
    )
    cofee_rating = SelectField(
        label="Coffee Rating",
        choices=[
            ("☕" * 1, "☕" * 1),
            ("☕" * 2, "☕" * 2),
            ("☕" * 3, "☕" * 3),
            ("☕" * 4, "☕" * 4),
            ("☕" * 5, "☕" * 5),
        ],
        validators=[DataRequired()],
    )
    wifi_rating = SelectField(
        label="Wifi Strength Rating",
        choices=[
            ("✘", "✘"),
            ("💪" * 1, "💪" * 1),
            ("💪" * 2, "💪" * 2),
            ("💪" * 3, "💪" * 3),
            ("💪" * 4, "💪" * 4),
            ("💪" * 5, "💪" * 5),
        ],
        validators=[DataRequired()],
    )
    power_outlet_rating = SelectField(
        label="Power Socket Availability",
        choices=[
            ("✘", "✘"),
            ("🔌" * 1, "🔌" * 1),
            ("🔌" * 2, "🔌" * 2),
            ("🔌" * 3, "🔌" * 3),
            ("🔌" * 4, "🔌" * 4),
            ("🔌" * 5, "🔌" * 5),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", encoding="utf-8", mode="a") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    form.cafe.data,
                    form.location_url.data,
                    form.open_time.data,
                    form.closing_time.data,
                    form.cofee_rating.data,
                    form.wifi_rating.data,
                    form.power_outlet_rating.data,
                ]
            )
        return redirect("/cafes")
    return render_template("add.html", form=form)


@app.route("/cafes")
def cafes():
    with open("cafe-data.csv", newline="", encoding="utf-8") as csv_file:
        csv_data = list(csv.reader(csv_file, delimiter=","))
    return render_template("cafes.html", cafes=csv_data)


if __name__ == "__main__":
    app.run(debug=True, port=7000)
