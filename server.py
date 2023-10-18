from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud

app = Flask(__name__)
app.secret_key = "secret"

###########################################################################
# BOX CONSTANTS
###########################################################################

small_box_name = "Small Box"
small_box_length = 12
small_box_width = 8
small_box_height = 4
small_box_volume = 384

medium_box_name = "Medium Box"
medium_box_length = 16
medium_box_width = 12
medium_box_height = 8
medium_box_volume = 1536

large_box_name = "Large Box"
large_box_length = 20
large_box_width = 16
large_box_height = 12
large_box_volume = 3840

extra_large_box_name = "Extra Large Box"
extra_large_box_length = 24
extra_large_box_width = 18
extra_large_box_height = 14
extra_large_box_volume = 6048

###########################################################################

@app.route("/")
def homepage():
    return render_template("homepage.html")

###########################################################################

@app.route("/employees", methods=["POST"])
def register_employee():
    email = request.form.get("email")
    password = request.form.get("password")
    employee = crud.get_employee_by_email(email)
    
    if employee:
        flash("Cannot create an account with that email. Try again.")
    else:
        employee = crud.create_employee(email, password)
        db.session.add(employee)
        db.session.commit()
        flash("Account created! Please log in.")
    
    return redirect("/")

###########################################################################

@app.route("/login", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")
    employee = crud.get_employee_by_email(email)
    
    if not employee or employee.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        session["employee_email"] = employee.email
        flash(f"Welcome back, {employee.email}!")
        return redirect("/order")
    
    return redirect("/")

###########################################################################

@app.route("/boxes")
def common_box_sizes():
    box_dimensions = {
    "Small Box": (12, 8, 4, 384),
    "Medium Box": (16, 12, 8, 1536),
    "Large Box": (20, 16, 12, 3840),
    "Extra Large Box": (24, 18, 14, 6048)
    }
    return render_template("boxes.html", boxes = box_dimensions)

###########################################################################

@app.route("/order")
def order():
    employee_email = session.get("employee_email")
    order_number = None  

    if not employee_email:
        flash("You must log in before proceeding.")
        return redirect("/")
    
    if employee_email:
        last_order_id = crud.get_last_order_id()
        
        if last_order_id is not None:
            order_number = last_order_id + 1
        else:
            order_number = 1
        session["order_number"] = order_number
    
    return render_template("order.html", employee_email=employee_email, order_number=order_number)

###########################################################################

@app.route("/proceed_order", methods=["POST"])
def proceed_order():
    order_number = session.get("order_number")
    employee_email = session.get("employee_email")
    
    if not employee_email or order_number is None:
        flash("You must log in and create an order before proceeding.")
        return redirect("/")
    
    employee = crud.get_employee_by_email(employee_email)
    items = []

    order = crud.create_order(order_number, employee.employee_id)
    db.session.add(order)
    db.session.commit()

    names = request.form.getlist("name[]")
    lengths = request.form.getlist("length[]")
    widths = request.form.getlist("width[]")
    depths = request.form.getlist("depth[]")
    quantities = request.form.getlist("quantity[]")

    for name, length, width, depth, quantity in zip(names, lengths, widths, depths, quantities):
        item = crud.create_good(name, int(length), int(width), int(depth), int(quantity))
        db.session.add(item)
        db.session.commit()
        items.append(item)
    
        print(item)

    for item in items:
        name = item.name
        length = item.length
        width = item.width
        depth = item.depth
        quantity = item.quantity

        good = crud.create_good(name, length, width, depth, quantity)
        db.session.add(good)
        db.session.commit()

        print(good)


        order_item = crud.create_order_item(order.order_id, good.good_id)
        db.session.add(order_item)
        db.session.commit()

    return redirect("/result")

###########################################################################

@app.route("/result")
def result():
    order_number = session.get("order_number")
    employee_email = session.get("employee_email")
    
    if not employee_email or order_number is None:
        flash("You must log in and create an order before proceeding.")
        return redirect("/")
    
    employee = crud.get_employee_by_email(employee_email)
    goods = crud.get_goods_by_info(employee.employee_id, order_number)

    goods = sorted(goods, key=lambda good: good.length, reverse=True)

    ###########################################################################
    # BOX FUNCTIONS
    ###########################################################################

    box_dimensions = {
    0: (12, 8, 4, 384),
    1: (16, 12, 8, 1536),
    2: (20, 16, 12, 3840),
    3: (24, 18, 14, 6048)
}
    utilized_boxes = { 0: 0, 1: 0, 2: 0, 3: 0}
    
    remaining_volume = 0

    for good in goods:
        remaining_volume += (good.length * good.width * good.depth * good.quantity)

    for box in box_dimensions:
        size = 3
        if remaining_volume < box_dimensions[box][3]:
             size = box
             break
    
    remaining_items = []

    for good in goods:
            for number in range(good.quantity):
                remaining_items.append(good)

    length = box_dimensions[size][0]
    width = box_dimensions[size][1]
    depth = box_dimensions[size][2]
    volume = box_dimensions[size][3]

    for product in remaining_items:
        if (
            product.length <= length and
            product.width <= width and
            product.depth <= depth and
            product.length * product.width * product.depth <= volume
            ):
            remaining_volume -= product.length * product.width * product.depth
            volume -= product.length * product.width * product.depth
            length -= product.length 
            width -= product.width 
            depth -= product.depth
            remaining_items.remove(product)
        else:
            utilized_boxes[size] += 1
            if remaining_volume > box_dimensions[size][3]:
                length = box_dimensions[size][0]
                width = box_dimensions[size][1]
                depth = box_dimensions[size][2]
                volume = box_dimensions[size][3]
            else:
                for box in box_dimensions:
                    if remaining_volume < box_dimensions[box][3]:
                        size = box
                        break
                length = box_dimensions[size][0]
                width = box_dimensions[size][1]
                depth = box_dimensions[size][2]
                volume = box_dimensions[size][3]
    
    return render_template("result.html", employee_email=employee_email, order_number=order_number, goods=goods,
                           data = utilized_boxes)

###########################################################################

@app.route("/info")
def info():
    employee_email = session.get("employee_email")
    
    if not employee_email:
        flash("You must log in before proceeding.")
        return redirect("/")
    
    employee = crud.get_employee_by_email(employee_email)
    orders = crud.get_orders_by_employee_id(employee.employee_id)
    
    return render_template("info.html", employee_email=employee_email, orders=orders)

###########################################################################

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
