import sqlalchemy.exc
from flask import (
    Flask,
    render_template,
    request,
    url_for,
    redirect,
    flash,
    send_from_directory,
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    current_user,
    logout_user,
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret-key-goes-here"

# CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
db = SQLAlchemy()
db.init_app(app)

# Configure LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# CREATE TABLE IN DB
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


@login_manager.user_loader
def load_user(user_id):
    user = db.session.get(User, int(user_id))
    return user


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        new_user = User(
            name=request.form.get("name"),
            email=request.form.get("email"),
            password=generate_password_hash(
                password=request.form.get("password"), salt_length=8
            ),
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Email already registered. Please login instead!")
            return redirect(url_for("login"))
        login_user(new_user)
        return redirect(url_for("secrets"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form.get("email")
        user_password = request.form.get("password")
        user_to_login = User.query.where(User.email == user_email).first()
        if not user_to_login:
            flash("Email is not registered!!")
        elif not check_password_hash(user_to_login.password, user_password):
            flash("Incorrect password!!")
        else:
            login_user(user_to_login)
            return redirect(url_for("secrets"))

    return render_template("login.html")


@app.route("/secrets")
@login_required
def secrets():
    return render_template("secrets.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/download")
@login_required
def download():
    return send_from_directory("static/files", "cheat_sheet.pdf", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
