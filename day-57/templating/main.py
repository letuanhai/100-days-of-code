from flask import Flask, render_template
from post import get_posts


app = Flask(__name__)

posts = get_posts()


@app.route("/")
def home():
    return render_template("index.html", posts=list(posts.values()))


@app.route("/post/<int:id>")
def get_post(id):
    return render_template("post.html", post=posts[id])


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
