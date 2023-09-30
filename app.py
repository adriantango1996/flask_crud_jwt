from flask import Flask, jsonify, request, json, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_marshmallow import Marshmallow
import jwt
from datetime import datetime, timedelta
from functools import wraps

### Create an instance of flask
app = Flask(__name__)

app.config["SECRET_KEY"] = "8d1a9c85db5f486f8d202250446c0541"


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get("authorization")

        if not token:
            return make_response({"message!": "unauthorized"}), 401

        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return make_response({"message": "Invalid token"}), 403
        return func(*args, **kwargs)

    return decorated


@app.route("/auth")
@token_required
def auth():
    return "JWT is verified. welcome"


db = SQLAlchemy()
ma = Marshmallow()

mysql = MySQL(app)


# Create a model for our table
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __init__(self, first_name, last_name, email, mobile_number, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.mobile_number = mobile_number
        self.address = address


class CsutomerSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "address")


customer_schema = CsutomerSchema()
customers_schema_schema = CsutomerSchema(many=True)

##MYSQL
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/customer"
##SQLITE
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Database.db"

db.init_app(app)
with app.app_context():
    db.create_all()


# login
@app.route("/customer/login", methods=["POST"])
def login():
    event = request.json
    username = event.get("username", "")
    password = event.get("password", "")

    if username == "admin" or password == "123456":
        token = jwt.encode(
            {
                "user": username,
                "exp": datetime.utcnow() + timedelta(seconds=120),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )

        payload = {"code": 2000, "payload": {"token": token}}

        return make_response(payload, 200)


# create
@app.route("/customer/add", methods=["POST"])
def create_customer():
    event = request.json
    first_name = event.get("first_name", "")
    last_name = event.get("last_name", "")
    email = event.get("email", "")
    mobile_number = event.get("mobile_number", "")
    email = event.get("email", "")
    address = event.get("address", "")
    new_customer = Customer(
        first_name=first_name,
        last_name=last_name,
        email=email,
        mobile_number=mobile_number,
        address=address,
    )
    db.session.add(new_customer)
    db.session.commit()

    return make_response({"code": 2000, "payload": event}, 200)


# list
@app.route("/customer", methods=["GET"])
def list_customer():
    customers = []
    data = Customer.query.all()
    customers = customers_schema_schema.dump(data)
    return make_response({"code": 2000, "payload": customers}, 200)


# view
@app.route("/customer/<id>", methods=["GET"])
@token_required
def view_customer(id):
    customer = Customer.query.get(id)

    if customer is None:
        return make_response({"code": 4041, "messages": "Data not Found"}, 404)

    data = customer_schema.dump(customer)
    return make_response({"code": 2000, "messages": data}, 200)


# update
@app.route("/customer/<id>", methods=["PUT"])
def update_customer(id):
    customer = Customer.query.get(id)

    if customer is None:
        return make_response({"code": 4041, "messages": "Data not Found"}, 404)

    event = request.json
    first_name = event.get("first_name", "")
    last_name = event.get("last_name", "")
    email = event.get("email", "")
    mobile_number = event.get("mobile_number", "")
    address = event.get("address", "")

    if first_name:
        customer.first_name = first_name
    if last_name:
        customer.last_name = last_name
    if email:
        customer.email = email
    if mobile_number:
        customer.mobile_number = mobile_number
    if address:
        customer.address = address

    db.session.commit()
    data = customer_schema.dump(customer)
    return make_response({"code": 2000, "payload": data}, 200)


# delete
@app.route("/customer/<id>", methods=["DELETE"])
def delete_product(id):
    customer = Customer.query.get(id)
    if customer is None:
        return make_response({"code": 4041, "messages": "Data not Found"}, 404)

    db.session.delete(customer)
    db.session.commit()
    return make_response(
        {"code": 2000, "payload": {}, "messages": "Delete Successful"}, 200
    )


if __name__ == "__main__":
    app.run(debug=True)
