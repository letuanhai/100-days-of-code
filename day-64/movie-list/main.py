from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField
from wtforms.validators import DataRequired, NumberRange

from get_movies import search_movies, get_movie_details, POSTER_LINK

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
Bootstrap(app)
db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String, nullable=True)
    img_url = db.Column(db.String, nullable=True)


with app.app_context():
    db.create_all()
#     new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
#     db.session.add(new_movie)
#     db.session.commit()


class EditForm(FlaskForm):
    rating = FloatField(
        label="Your Rating (Out of 10 e.g 7.5)",
        validators=[
            DataRequired(),
            NumberRange(
                min=0, max=10.0, message="Please enter a number in the range of 0 to 10"
            ),
        ],
    )
    review = TextAreaField(label="Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class AddMovieForm(FlaskForm):
    title = StringField(label="Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Find Movie")


@app.route("/")
def home():
    all_movies = db.session.query(Movie).order_by(Movie.rating.desc()).all()
    for i, movie in enumerate(all_movies):
        movie.ranking = i + 1
    db.session.commit()
    return render_template("index.html", all_movies=all_movies)


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    movie_to_edit = Movie.query.get(request.args.get("id"))
    form = EditForm()
    if form.validate_on_submit():
        new_rating = form.rating.data
        new_review = form.review.data
        movie_to_edit.rating = new_rating
        movie_to_edit.review = new_review
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", form=form, movie=movie_to_edit)


@app.route("/delete")
def delete_movie():
    movie_to_delete = Movie.query.get(request.args.get("id"))
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    add_form = AddMovieForm()
    if add_form.validate_on_submit():
        movie_title = add_form.title.data
        movies = search_movies(movie_title)
        return render_template("select.html", movies=movies)
    return render_template("add.html", form=add_form)


@app.route("/select")
def select_movie():
    movie_id = int(request.args.get("movie_id"))
    movie_details = get_movie_details(movie_id)
    new_movie = Movie(
        title=movie_details["title"],
        year=int(movie_details["release_date"][:4]),
        description=movie_details["overview"],
        img_url=POSTER_LINK + movie_details["poster_path"],
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit_rating", id=new_movie.id))


if __name__ == "__main__":
    app.run(debug=True)
