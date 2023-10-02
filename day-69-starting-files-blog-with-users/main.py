import functools
from datetime import date

import sqlalchemy.exc
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import relationship
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm


"""
Make sure the required packages are installed: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from the requirements.txt for this project.
"""

app = Flask(__name__)
app.config["SECRET_KEY"] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
ckeditor = CKEditor(app)
Bootstrap5(app)

# Configure Flask-Loging
login_manager = LoginManager(app=app)

# Configure Gravatar
gravatar = Gravatar(
    app,
    size=100,
    rating="g",
    default="retro",
    force_default=False,
    force_lower=False,
    use_ssl=False,
    base_url=None,
)

# CONNECT TO DB
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy()
db.init_app(app)


# CONFIGURE TABLES
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    author = relationship("User", back_populates="posts")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comments = relationship("Comment", back_populates="parent_post")


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="author")


class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500))
    parent_post = relationship("BlogPost", back_populates="comments")
    post_id = db.Column(db.Integer, db.ForeignKey("blog_posts.id"))
    author = relationship("User", back_populates="comments")
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def admin_only(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user.id == 1:
            return f
        else:
            return abort(403)

    return wrapper


with app.app_context():
    db.create_all()


@app.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        new_user = User(
            name=register_form.name.data,
            email=register_form.email.data,
            password_hash=generate_password_hash(register_form.password.data),
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:  # Unique constraint
            flash("Email already registered. Please login instead!")
            return redirect(url_for("login"))
        login_user(new_user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html", form=register_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user_to_login = User.query.where(User.email == login_form.email.data).first()
        if user_to_login is not None and check_password_hash(
            user_to_login.password_hash, login_form.password.data
        ):
            login_user(user_to_login)
            return redirect(url_for("get_all_posts"))
        else:
            flash("Email/password is incorrect!")
    return render_template("login.html", form=login_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("get_all_posts"))


@app.route("/")
def get_all_posts():
    result = db.session.execute(db.select(BlogPost))
    posts = result.scalars().all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
    requested_post = db.get_or_404(BlogPost, post_id)
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(
            text=comment_form.comment.data,
            parent_post=requested_post,
            author=current_user
            # post_id=requested_post.id,
            # author_id=current_user.id,
        )
        db.session.add(new_comment)
        db.session.commit()
        return redirect(url_for("show_post", post_id=post_id))
    return render_template("post.html", post=requested_post, form=comment_form)


@admin_only
@app.route("/new-post", methods=["GET", "POST"])
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y"),
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@admin_only
@app.route("/edit-post/<int:post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    post = db.get_or_404(BlogPost, post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body,
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))
    return render_template("make-post.html", form=edit_form, is_edit=True)


@admin_only
@app.route("/delete/<int:post_id>")
def delete_post(post_id):
    post_to_delete = db.get_or_404(BlogPost, post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for("get_all_posts"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True, port=5002)
