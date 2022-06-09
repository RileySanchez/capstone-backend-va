from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

database_url = "postgresql:" + ":".join(os.environ.get("DATABASE_URL", "").split(":")[1:])
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
CORS(app)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_url

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)



    def __init__(self, email, password):
        self.email = email
        self.password = password


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'email', 'password')


user_schema = UserSchema()
multiple_user_schema = UserSchema(many=True)

@app.route('/user/add', methods=['POST'])
def add_user():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    email = post_data.get('email')
    password = post_data.get('password')


    username_duplicate = db.session.query(User).filter(User.username == username).first()

    if username_duplicate is not None:
        return jsonify("Error: The username is already registered.")

    email_duplicate = db.session.query(User).filter(User.username == username).first()

    if email_duplicate is not None:
        return jsonify("Error: The email is already registered.")

    encrypted_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(username, encrypted_password, email, img)

    db.session.add(new_user)
    db.session.commit()

    return jsonify(user_schema.dump(new_user))

@app.route('/user/get', methods=['GET'])
def get_all_users():
    all_users = db.session.query(User).all()
    return jsonify(multiple_user_schema.dump(all_users))


@app.route('/user/get/<id>', methods=["GET"])
def get_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    return jsonify(user_schema.dump(user))


@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user_by_id(id):
    user = db.session.query(User).filter(User.id == id).first()
    db.session.delete(user)
    db.session.commit()

    return jsonify("The user has been deleted")

if __name__ == "__main__":
    app.run(debug=True)
