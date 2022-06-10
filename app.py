from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
from flask_cors import CORS 
from dotenv import load_dotenv

import os

load_dotenv()

database_url = "postgresql:" + ":".join(os.environ.get('DATABASE_URL', "").split(":")[1:])
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")
CORS(app)

class VaResources(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)


    def __init__(self, title, description):
        self.title = title
        self.description = description


class VaResourceSchema(ma.Schema):
    class Meta: 
        fields = ("id", "title", "description")

va_item_schema = VaResourceSchema()
multiple_va_item_schema = VaResourceSchema(many=True)


@app.route('/varesources/add', methods=["POST"])
def add_va_item():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be json')

    post_data = request.get_json()
    title = post_data.get('title')


    item = db.session.query(VaResource).filter(VaResource.title == title).first()

    if title == None:
        return jsonify("Error: Data must have a 'title' key.")

    if description == None:
        return jsonify("Error: Data must have a 'description' key.")


    new_item = VaResource(title, description)
    db.session.add(new_resource)
    db.session.commit()

    return jsonify("You've added a new varesources item!")


@app.route('/varesources/get', methods=["GET"])
def get_va_items():
    items = db.session.query(GearItem).all()
    return jsonify(multiple_gear_item_schema.dump(items))


@app.route('/varesources/get/<id>', methods=["GET"])
def get_va_item_by_id(id):
    item = db.session.query(GearItem).filter(GearItem.id == id).first()
    return jsonify(gear_item_schema.dump(item))


@app.route('/varesources/delete/<id>', methods=["DELETE"])
def delete_va_item(id):
    item = db.session.query(VaResource).filter(VaResource.id == id).first()
    db.session.delete(item)
    db.session.commit()

    return jsonify("The VA Resource has been deleted")


# @app.route('/varesources/update/<id>', methods=["PUT", "PATCH"])
# def update_va_item_by_id(id):
#     if request.content_type != 'application/json':
#         return jsonify('Error: Data must be json')

#     post_data = request.get_json()
#     title = post_data.get('title')
#     description = post_data.get('description')


#     item = db.session.query(VaResource).filter(VaResource.id == id).first()

#     if title != None:
#         item.title = title
#     if description != None:
#         item.description = description


    db.session.commit()
    return jsonify("VaResource has been updated.")