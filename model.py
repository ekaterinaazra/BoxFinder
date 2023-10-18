"""Models for Walmart packaging app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Employee(db.Model):
    __tablename__ = 'employees'

    employee_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    orders = db.relationship('Order', back_populates='employee')

    def __repr__(self):
        return f"<Employee id={self.employee_id} email={self.email}>"

class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'))

    employee = db.relationship('Employee', back_populates='orders')
    order_items = db.relationship('OrderItem', back_populates='order')


    def __repr__(self):
        return f"<Order order_id={self.order_id} employee_id={self.employee_id} >"


class Good(db.Model):
    __tablename__ = 'goods'

    good_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    length = db.Column(db.Integer)
    width = db.Column(db.Integer)
    depth = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    order_items = db.relationship('OrderItem', back_populates='good')

    def __repr__(self):
        return f"<Good id={self.good_id} name={self.name}>"  
    
class OrderItem(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    good_id = db.Column(db.Integer, db.ForeignKey('goods.good_id'))
    
    order = db.relationship('Order', back_populates='order_items')
    good = db.relationship('Good', back_populates='order_items')

    def __repr__(self):
        return f"<OrderItem order_item_id={self.order_item_id} order_id={self.order_id} good_id={self.good_id}>"

def connect_to_db(flask_app, db_uri="postgresql:///orders", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)