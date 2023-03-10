from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    rating = db.Column(db.Float, nullable=False)


with app.app_context():
    db.create_all()
#     book = Book(title="Harry Potter", author="J.K.Rowling", rating=9.3)
#     db.session.add(book)
#     db.session.commit()


@app.route("/")
def home():
    all_books = db.session.query(Book).all()
    return render_template("index.html", all_books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form.get("title"),
            author=request.form.get("author"),
            rating=request.form.get("rating"),
        )
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    book_id = request.args['id']
    current_book = Book.query.get(book_id)
    if request.method == 'POST':
        new_rating = request.form.get('new_rating')
        current_book.rating = new_rating
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=current_book)

@app.route('/delete')
def delete():
    book_id = request.args['id']
    current_book = Book.query.get(book_id)
    db.session.delete(current_book)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=7000)
