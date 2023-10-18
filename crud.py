"""CRUD operations."""

from model import db, Employee, Order, Good, OrderItem, connect_to_db

def create_employee(email, password):
    """Create and return a new employee."""
    employee = Employee(email=email, password=password)

    return employee

def get_employees():
    """Return all employees."""
    return Employee.query.all()

def get_employee_by_id(employee_id):
    """Return an employee by primary key."""
    return Employee.query.get(employee_id)

def get_employee_by_email(email):
    """Return an employee by email."""
    return Employee.query.filter(Employee.email == email).first()

def create_good(name, length, width, depth, quantity):
    """Create and return a new good."""
    good = Good(name=name, length=length, width=width, depth=depth, quantity = quantity)
    return good

def get_good_by_id(good_id):
    """Return a good by primary key."""
    return Good.query.get(good_id)

def get_goods():
    """Return all goods."""
    return Good.query.all()

def create_order(order_id, employee_id):
    """Create and return a new order."""
    order = Order(order_id=order_id, employee_id=employee_id)
    return order

def get_last_order_id():
    """Get the last order_id in the orders table."""
    last_order = Order.query.order_by(Order.order_id.desc()).first()
    if last_order:
        return last_order.order_id
    else:
        return None

def get_order():
    """Return all goods."""
    return Order.query.all()

def create_order_item(order_id, good_id):
    """Create and return a new order."""
    order_item = OrderItem(order_id=order_id, good_id=good_id)
    return order_item

def get_goods_by_info(employee_id, order_number):
    """Return a list of goods for a specific employee and order number."""
    return Good.query.join(OrderItem, Good.good_id == OrderItem.good_id).join(Order, OrderItem.order_id == Order.order_id).filter(Order.employee_id == employee_id, Order.order_id == order_number).all()

def get_orders_by_employee_id(employee_id):
    """Return a list of orders for a specific employee."""
    return Order.query.filter(Order.employee_id == employee_id).all()

if __name__ == "__main__":
    from server import app

    connect_to_db(app)