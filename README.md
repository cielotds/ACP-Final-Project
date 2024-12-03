Project Title: Point of Sale System with Order History and Payment Status


I. A brief project overview

The project is a Point of Sale (POS) system designed to streamline the order management process for Good House Burger. It includes features for taking customer orders, displaying order history and tracking payment statuses. The order history records details such as order IDs, total prices, date and timestamps, and payment statuses (paid or not paid). The system also supports generating a receipt with date and time for transparency and record-keeping. 

II. Explanation of how Python concepts, libraries, etc. were applied

Libraries:

tkinter: This library is used to design the GUI for the POS system. It provides widgets like buttons, labels, spinboxes, and Treeview for managing orders, categories, and history.

datetime: Used to generate timestamps for receipts and to display the date and time of orders.

messagebox: Displays alerts and notifications to the user, such as warnings or success messages.

hashlib: It is used to hash passwords securely. In the code, hashlib.sha256(password.encode()).hexdigest() generates a SHA-256 hash of the password in hexadecimal format. This ensures passwords are stored securely, protecting them even if the database is compromised.

json: It is used to convert order items into a JSON string before storing them in the database.

textwrap: It is used to format and manipulate long strings fit within a defined layout. In this project, it is specifically used for generating receipts.


Database Integration:
MySQL is used for persistent storage of order data. Concepts like SQL queries (e.g., INSERT, UPDATE, DELETE, and SELECT), the DbOperations.py, and database connection handling (mysql.connector.connect) are used to interact with the database, store the user’s information, store order details, and retrieve order history.

Object-Oriented Programming:
Object-Oriented Programming is widely used in the project. The project uses classes to encapsulate related data and behavior, which enhances modularity, reusability, and maintainability. By organizing functionality into specific classes like User, Product, and UserDao, Dashboard, etc. the code becomes easier to understand and test. For example, the User class handles user-related data and actions and UserDao interacts with the database, the Product class encapsulates product data (name, price, image), while the Dashboard class manages the main point-of-sale functionality, including adding items to the cart, completing orders, and calculating totals. This separation makes it easier to update or modify one part of the system without affecting others.

Error Handling:
Exception Handling using try, except, and finally is employed to handle database errors and ensure the application remains stable even when an error occurs (e.g., database connectivity issues or invalid user input).

try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ghbpython',
            user='root',
            password='1024'
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

String Manipulation:
String formatting is used extensively, such as when generating receipts, formatting the total price, and displaying order details (e.g., f"TOTAL: P {total_price:.2f}\n”).

Lambda Functions:
Lambda expressions are used for short and anonymous functions. Here, the lambda function in this code is used to create an anonymous function to handle the KeyRelease event for email_entry and password_entry.

self.email_entry.bind("<KeyRelease>", lambda event: self.validate_fields())
        self.password_entry.bind("<KeyRelease>", lambda event: self.validate_fields())

Additionally, it creates an anonymous function that, when triggered, calls self.show_products with the current category as the argument. (e.g., command=lambda c=category: self.show_products(c)). 

List and Dictionary:
Lists and dictionaries are used to store and manage menu items, orders, and configurations. For example, order items are stored in a dictionary that maps categories to lists of tuples containing its quantity, item and amount.

order_items = []
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            order_items.append({
                "quantity": int(values[0]),
                "item": values[1],
                "amount": float(values[2]),
            })

In addition, a dictionary (self.products) is used to group products by category, where each category (key) maps to a list of Product objects. The dictionary allows quick lookup of products by category, and the lists store the individual products within each category.

self.products = {
            "Rice Bowl": [
                Product("Siomai Rice", 35.00, "images/siomai_rice (1).png"),
                Product("Chicken Finger Rice", 40.00, "images/Chicken Finger Rice.png"),
                Product("Shanghai Rice", 40.00, "images/Shanghai Rice.png"),
                Product("Fish Fillet Rice", 40.00, "images/Fish Fillet Rice.png")
            ], …..


III. Details of the chosen SDG and its integration into the project

The chosen Sustainable Development Goal (SDG) is Goal 8: Decent Work and Economic Growth. The system supports this goal by empowering small businesses to improve operational efficiency, reduce errors, and manage sales transparently. By simplifying order processing and payment tracking, the POS system enables businesses to focus on growth, enhance customer satisfaction, and foster economic resilience. Additionally, the integration of a digital solution reduces reliance on paper-based methods, contributing to sustainable practices.

IV. Instructions for running the program

• Access the Point of Sale System.
• Sign Up or Log In. If you are a new user, click on the "Sign Up" button and fill in the required information (e.g., name, email and password). If you already have an account, enter your credentials and click "Log In".
• You will see the dashboard, browse through your inventory and add items to the order by selecting quantities and clicking on an "Add" button.
• Once all items are added, review the order summary displayed on the screen. You can also make any necessary adjustments (e.g., remove and reset items). Then, confirm the transaction by clicking on the "Complete Order" button.
• After processing, the screen will display a receipt.
• However, if you click on "View History", this button takes you to a page where you can view past orders.
• Then you can click on any order from the list to view its details: order ID, date, price, and status(paid/not paid).
• You can also update the order's status(from not paid to paid and vice versa) by clicking the “Update” button.
• Click on "Close" when you are finished using the Point of Sale System, clicking this button will close the application safely.
