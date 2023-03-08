from flask import Flask, render_template
import requests

posts = requests.get("https://api.npoint.io/992c5ebd0d88591dca19").json()

app = Flask(__name__)


@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def get_about():
    return render_template("about.html")


@app.route("/contact")
def get_contact():
    return render_template("contact.html")

@app.route('/post/<int:post_id>')
def get_post(post_id):
    requested_post = None
    for blog_post in posts:
        if blog_post['id'] == post_id:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
