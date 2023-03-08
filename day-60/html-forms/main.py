from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def get_index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login_data():
    return f"<h1>Username: {request.form['username']}, Password: {request.form['password']} </h1>"


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=7000)
