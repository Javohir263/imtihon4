from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api = Api(app)

# ===================== User Model =====================
class UserModel(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

    products = db.relationship('ProductModel', backref='owner', lazy=True)

    def __repr__(self):
        return f"User(name={self.name}, email={self.email}, role={self.role})"


# ===================== Product Model =====================
class ProductModel(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Product(title={self.title}, price={self.price}, count={self.count})"


# ===================== Parsers =====================
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
user_args.add_argument('email', type=str, required=True, help="Email cannot be blank")
user_args.add_argument('role', type=str, required=True, help="Role cannot be blank")

product_args = reqparse.RequestParser()
product_args.add_argument('user_id', type=int, required=True, help="User ID required")
product_args.add_argument('title', type=str, required=True, help="Title required")
product_args.add_argument('description', type=str, help="Description required")
product_args.add_argument('price', type=float, required=True, help="Price required")
product_args.add_argument('count', type=int, required=True, help="Count required")


# ===================== Resources =====================
class Users(Resource):
    def get(self):
        users = UserModel.query.all()
        return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]
    def post(self):
        args = user_args.parse_args()
        user = UserModel(name=args['name'], email=args['email'], role=args['role'])
        db.session.add(user)
        db.session.commit()
        users = UserModel.query.all()
        return users, 201


class Products(Resource):
    def get(self):
        products = ProductModel.query.all()
        return [
            {
                "id": p.id,
                "user_id": p.user_id,
                "title": p.title,
                "description": p.description,
                "price": p.price,
                "count": p.count
            } for p in products
        ]


api.add_resource(Users, '/api/users')
api.add_resource(Products, '/api/products')


@app.route("/")
def main():
    return "<h1>Hello World!</h1>"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # ✅ Creates both tables if not exist
    app.run(debug=True)
