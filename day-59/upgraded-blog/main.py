from flask import Flask, render_template, request
import requests

posts = requests.get("https://api.npoint.io/992c5ebd0d88591dca19").json()

app = Flask(__name__)


@app.route("/")
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def get_about():
    return render_template("about.html")


@app.get("/contact")
def get_contact():
    return render_template("contact.html", title='Contact Me')


@app.route("/post/<int:post_id>")
def get_post(post_id):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == post_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


@app.post('/contact')
def receive_data():
    print(request.form)
    return render_template('contact.html', title="Messeage successfully sent!")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
