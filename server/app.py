import json
import math
import random
import secrets
from flask import Flask, request, abort, jsonify
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS

from models import db, User
from globals import ApplicationConfig

app = Flask(__name__)
app.config.from_object(ApplicationConfig)

CORS(app, supports_credentials=True)

bcrypt = Bcrypt(app)
server_session = Session(app)
db.init_app(app)

with app.app_context():
    db.create_all()



@app.route("/register", methods=["POST"])
def register_user():
    """
    It takes in a user's HCID and creates a new user in the database with a randomly generated password
    :return: The user's id, hcid, and password.
    """
    hcid = request.json["hcid"]
    password = str(secrets.token_urlsafe(5))


    user_exists = User.query.filter_by(hcid=hcid).first() is not None
    if user_exists:
        return jsonify({"error": "User already exists"}), 409

    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(hcid=hcid, password=hashed_password, time='0', puzzle_level='0', score='0')

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"id": str(new_user.id), "hc-id": str(new_user.hcid), "password": str(password)})

@app.route("/login", methods=["POST"])
def login():
    """
    It takes a username and password from the request body, checks if the username exists in the
    database, and if it does, checks if the password is correct. If both of those checks pass, it
    returns the user's id and username
    :return: The id and hcid of the user.
    """
    hcid = request.json["hcid"]
    password = request.json['password']

    user = User.query.filter_by(hcid=hcid).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({"id": user.id, "hcid": user.hcid})


# {"hcid": str(user), 'time': str(time), 'puzzle_level': str(puzzle_level)}
@app.route("/add-shit", methods=["POST"])
def add_shit():
    hcid = request.json["hcid"]
    time = request.json['time']
    puzzle_level = request.json["puzzle_level"]

    user = User.query.filter_by(hcid=hcid).first()

    if user is None:
        return jsonify({"error": "Unauthorized"}), 401

    user.time = time
    user.puzzle_level = puzzle_level

    db.session.commit()

    return jsonify({"msg": "added shit"})

def sortCriteria(user):
    return float(user.time)/float(user.puzzle_level)

@app.route("/scores", methods=["GET"])
def scores():
    users = User.query.all()
    print(users)
    users.sort(key=sortCriteria, reverse=True)

    data = {}

    for index, user in enumerate(users):

        data[user.hcid] = {"score" : f"{index*1.25}"}

    print(data)

    with open('scores.json', 'w') as f:
        json.dump(data, f)

    return jsonify({"msg": "scores set" })







if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
