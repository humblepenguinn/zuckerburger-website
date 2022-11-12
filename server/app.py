import secrets
from flask import Flask, request, abort, jsonify, session
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_cors import CORS

from models import db, User
from config import ApplicationConfig

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
    new_user = User(hcid=hcid, password=hashed_password, current_game="1", score="0", total_time_taken="0")

    session["user_id"] = new_user.id

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


if __name__ == "__main__":
    app.run(host='192.168.18.183', port=5000)
