# BoxFinder

The 'Box Finder' project is a robust Flask web application aimed at simplifying the daily tasks of Walmart warehouse employees. It offers a user-friendly platform that begins with user registration, empowering employees to create individual accounts. Employees can browse the warehouse's available carton boxes before logging in, gaining insights into available sizes. Upon successful registration or login, employees can effortlessly create new orders, each uniquely identified for easy tracking. During the order creation, employees can specify item dimensions and quantities with seamless CRUD operations managed by SQLAlchemy. Leveraging AJAX, the application dynamically adds table rows and efficiently delivers data to the database without requiring page reloads. Notably, the server automates the calculation of the required packaging boxes, considering item dimensions and available box sizes. The 'Get Box' button employs JavaScript DOM manipulation and the First-fit-decreasing bin packing algorithm, prioritizing larger items first, with length as a key criterion. A 'See all orders' button allows employees to review all orders created in the current session. The application boasts a user-friendly Bootstrap-based design, enhancing user experience and making it a valuable tool for Walmart warehouse operations."

Technology:
  Python,
  HTML,
  Flask,
  PostgreSQL,
  SQLAlchemy,
  Javascript,
  AJAX/JSON,
  Jinja2,
  Bootstrap
  
How to Install:

1. Set up and activate a Python virtualenv and install all dependencies:
pip install -r requirements.txt
2. Create a new database in PostgreSQL named orders:
createdb orders
3. Create the tables in your database:
python -i model.py
4. While in interactive mode, create tables:
   db.create_all()
5. Quit interactive mode.
6. Start up the flask server:
   python server.py
7. Go to localhost:5000 to start the web app

Features:

User-Friendly Registration and Account Management

Browse Available Boxes

Efficient Order Creation

Automated Box Quantity Calculation

Intuitive Box Quantity Display

Order Management and History

User-Friendly Design


Screenshots: 

<img width="1280" alt="Screenshot 2023-10-17 at 6 15 09 PM" src="https://github.com/ekaterinaazra/BoxFinder/assets/62628675/16a03561-0cc4-442b-8e7a-9292df510528">

<img width="1280" alt="Screenshot 2023-10-17 at 6 15 48 PM" src="https://github.com/ekaterinaazra/BoxFinder/assets/62628675/8dfdd5dc-afe0-4bba-8ba7-357927e801e5">

<img width="1280" alt="Screenshot 2023-10-17 at 6 16 02 PM" src="https://github.com/ekaterinaazra/BoxFinder/assets/62628675/f7f2a767-c8cb-40db-a446-b9637729b964">

<img width="1280" alt="Screenshot 2023-10-17 at 6 16 06 PM" src="https://github.com/ekaterinaazra/BoxFinder/assets/62628675/cd12a7a6-8b1e-4274-930f-624430c59eb9">
