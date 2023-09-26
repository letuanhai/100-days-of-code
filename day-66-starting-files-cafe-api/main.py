import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

"""
Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
"""

app = Flask(__name__)

##Connect to Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
db = SQLAlchemy()
db.init_app(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self) -> dict:
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


# with app.app_context():
#     db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random")
def get_random_cafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafes():
    all_cafes = Cafe.query.all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search_cafe():
    results = Cafe.query.where(Cafe.location == request.args.get("loc")).all()
    if not results:
        return jsonify(error={"Not Found": "No cafe found at that location"}), 404
    return jsonify(results=[cafe.to_dict() for cafe in results])


## HTTP POST - Create Record
@app.post("/add")
def add_new_cafe():
    try:
        data_dict = request.form.to_dict()
        print(data_dict)
        data_dict["has_toilet"] = bool(data_dict["has_toilet"])
        data_dict["has_wifi"] = bool(data_dict["has_wifi"])
        data_dict["has_sockets"] = bool(data_dict["has_sockets"])
        data_dict["can_take_calls"] = bool(data_dict["can_take_calls"])
        new_cafe = Cafe(**data_dict)
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(new_cafe.to_dict())
    except Exception as e:
        print(e.__traceback__)
        return jsonify(error="Unable to add new cafe"), 404


## HTTP PUT/PATCH - Update Record
@app.patch("/update-price/<int:cafe_id>")
def update_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = Cafe.query.get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(sucess=cafe.to_dict())
    else:
        return jsonify(error="Not found"), 404


## HTTP DELETE - Delete Record
@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    APIKEY = "TopSecretAPIKey"
    if request.args.get("api-key") != APIKEY:
        return jsonify(error="Incorrect secret key."), 403
    cafe_to_delete = Cafe.query.get(cafe_id)
    if not cafe_to_delete:
        return jsonify(error="Cafe Id not exist.")
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return jsonify(success="Deleted.")


if __name__ == "__main__":
    app.run(debug=True)
