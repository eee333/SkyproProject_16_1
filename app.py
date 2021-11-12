# Урок 16.1 SQLAlchemy
# База заказчиков и исполнителей

import data
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db: SQLAlchemy = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    email = db.Column(db.String(50))
    role = db.Column(db.String(50))
    phone = db.Column(db.String(50))

    def to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "role": self.role,
            "phone": self.phone
        }


class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(500))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    address = db.Column(db.String(200))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "address": self.address,
            "price": self.price,
            "customer_id": self.customer_id,
            "executor_id": self.executor_id
        }


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return{
            "id": self.id,
            "order_id": self.order_id,
            "executor_id": self.executor_id
        }


# db.drop_all()
# db.create_all()

def fill_tables():
    for user_data in data.users:
        new_user = User(
            id=user_data["id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            age=user_data["age"],
            email=user_data["email"],
            role=user_data["role"],
            phone=user_data["phone"]
        )
        db.session.add(new_user)
    db.session.commit()

    for order_data in data.orders:
        new_order = Order(
            id=order_data["id"],
            name=order_data["name"],
            description=order_data["description"],
            start_date=order_data["start_date"],
            end_date=order_data["end_date"],
            address=order_data["address"],
            price=order_data["price"],
            customer_id=order_data["customer_id"],
            executor_id=order_data["executor_id"]
        )
        db.session.add(new_order)
    db.session.commit()

    for offer_data in data.offers:
        new_offer = Offer(
            id=offer_data["id"],
            order_id=offer_data["order_id"],
            executor_id=offer_data["executor_id"]
        )
        db.session.add(new_offer)
    db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        all_users = db.session.query(User).all()
        all_users_dict = []
        for user in all_users:
            all_users_dict.append(user.to_dict())
        return jsonify(all_users_dict)

    elif request.method == 'POST':
        user_data = request.get_json()
        new_user = User(
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            age=user_data.get("age"),
            email=user_data.get("email"),
            role=user_data.get("role"),
            phone=user_data.get("phone")
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), '201'


@app.route('/users/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_user(uid):
    user = db.session.query(User).get(uid)
    if not user:
        return jsonify({"error": "user not found"}), '404'
    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = request.get_json()
        user.first_name = user_data.get("first_name")
        user.last_name = user_data.get("last_name")
        user.age = user_data.get("age")
        user.email = user_data.get("email")
        user.role = user_data.get("role")
        user.phone = user_data.get("phone")
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), '201'
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', '204'


@app.route('/orders', methods=['GET', 'POST'])
def get_orders():
    if request.method == 'GET':
        all_orders = db.session.query(Order).all()
        all_orders_dict = []
        for order in all_orders:
            all_orders_dict.append(order.to_dict())
        return jsonify(all_orders_dict)

    elif request.method == 'POST':
        order_data = request.get_json()
        new_order = Order(
            name=order_data.get("name"),
            description=order_data.get("description"),
            start_date=order_data.get("start_date"),
            end_date=order_data.get("end_date"),
            address=order_data.get("address"),
            price=order_data.get("price"),
            customer_id=order_data.get("customer_id"),
            executor_id=order_data.get("executor_id")
        )
        db.session.add(new_order)
        db.session.commit()
        return jsonify(new_order.to_dict()), '201'


@app.route('/orders/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_order(uid):
    order = db.session.query(Order).get(uid)
    if not order:
        return jsonify({"error": "order not found"}), '404'
    if request.method == 'GET':
        return jsonify(order.to_dict())
    elif request.method == 'PUT':
        order_data = request.get_json()
        order.name = order_data.get("name")
        order.description = order_data.get("description")
        order.start_date = order_data.get("start_date")
        order.end_date = order_data.get("end_date")
        order.address = order_data.get("address")
        order.price = int(order_data.get("price"))
        order.customer_id = int(order_data.get("customer_id"))
        order.executor_id = int(order_data.get("executor_id"))
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), '201'
    elif request.method == 'DELETE':
        db.session.delete(order)
        db.session.commit()
        return '', '204'


@app.route('/offers', methods=['GET', 'POST'])
def get_offers():
    if request.method == 'GET':
        all_offers = db.session.query(Offer).all()
        all_offers_dict = []
        for offer in all_offers:
            all_offers_dict.append(offer.to_dict())
        return jsonify(all_offers_dict)

    elif request.method == 'POST':
        offer_data = request.get_json()
        new_offer = Offer(
            order_id=offer_data.get("order_id"),
            executor_id=offer_data.get("executor_id")
        )
        db.session.add(new_offer)
        db.session.commit()
        return jsonify(new_offer.to_dict()), '201'


@app.route('/offers/<int:uid>', methods=['GET', 'PUT', 'DELETE'])
def get_offer(uid):
    offer = db.session.query(Offer).get(uid)
    if not offer:
        return jsonify({"error": "offer not found"}), '404'
    if request.method == 'GET':
        return jsonify(offer.to_dict())
    elif request.method == 'PUT':
        offer_data = request.get_json()
        offer.order_id = offer_data.get("order_id")
        offer.executor_id = offer_data.get("executor_id")
        db.session.add(offer)
        db.session.commit()
        return jsonify(offer.to_dict()), '201'
    elif request.method == 'DELETE':
        db.session.delete(offer)
        db.session.commit()
        return '', '204'


if __name__ == '__main__':
    app.run()
