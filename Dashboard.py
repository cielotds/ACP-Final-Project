import mysql
from ConnectionProvider import get_con
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import textwrap


class Product:
    """A class to represent a product."""
    def __init__(self, name, price, image_path=None):
        self.name = name
        self.price = price
        self.image_path = image_path

class Dashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Point of Sale System")
        self.geometry("15000x1000")
        self.configure(bg="white")
        self.cart = []
        self.selected_category = None
        self.spinners = []  # Store spinbox references
        # Product data
        self.products = {
            "Rice Bowl": [
                Product("Siomai Rice", 35.00, "images/siomai_rice (1).png"),
                Product("Chicken Finger Rice", 40.00, "images/Chicken Finger Rice.png"),
                Product("Shanghai Rice", 40.00, "images/Shanghai Rice.png"),
                Product("Fish Fillet Rice", 40.00, "images/Fish Fillet Rice.png")
            ],
            "Bestie": [
                Product("Small Fries", 50.00, "images/Small Fries.png"),
                Product("Big Fries", 100.00, "images/Big Fries.png"),
                Product("16oz Fries & Juice", 30.00, "images/16oz Fries & Juice.png"),
                Product("22oz Fries & Juice", 35.00, "images/22oz Fries & Juice.png")
            ],
            "Combo Snack": [
                Product("16oz Fries & Juice + 1pc Cheese Burger", 50.00, "images/16oz Combo Snack.png"),
                Product("22oz Fries & Juice + 1pc Cheese Burger", 60.00, "images/22oz Combo Snack.png")
            ],
            "Buy 1 Take 1": [
                Product("Burger", 40.00, "images/Burger.png"),
                Product("Burger w/ Cheese", 35.00, "images/Cheese Burger.png")
            ]
        }

        self.image_cache = {}  # Cache to store loaded images
        self.create_layout()

        self.show_products("Rice Bowl")

        

    def create_layout(self):
        """Set up the GUI layout."""
        # Navigation Menu
        self.nav_frame = tk.Frame(self, bg="white", padx=10, pady=10)
        self.nav_frame.grid(row=0, column=0, sticky="ns")
        self.create_nav_menu()

        # Product Display
        self.product_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        self.product_frame.grid(row=0, column=1, sticky="nsew")

        # Order Summary
        self.order_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        self.order_frame.grid(row=0, column=2, sticky="nsew")
        self.create_order_summary()

        self.receipt_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        self.receipt_frame.grid(row=0, column=3, sticky="nsew")
        self.create_receipt()

        
    

    def create_nav_menu(self):
        """Create navigation menu for categories."""
        tk.Label(self.nav_frame, text="DASHBOARD", font=("Calistoga", 20), bg="white", fg="#E1522B").pack(pady=10)
        for category in self.products.keys():
            tk.Button(self.nav_frame, text=category, bg="#5A954F", fg="white", font=("Calistoga", 12),
                      command=lambda c=category: self.show_products(c)).pack(pady=5, fill="x")

    def show_products(self, category):
        """Display products for the selected category in two columns."""
        self.selected_category = category
        for widget in self.product_frame.winfo_children():
            widget.destroy()  # Clear previous products

        row, col = 0, 0
        for product in self.products[category]:
            frame = self.create_product_widget(product)
            frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
            col += 1
            if col > 1:  # Move to next row after two columns
                col = 0
                row += 1

        self.product_frame.grid_columnconfigure(0, weight=1)
        self.product_frame.grid_columnconfigure(1, weight=1)


    # In the create_product_widget method
    def create_product_widget(self, product):
        """Display individual product details."""
        frame = tk.Frame(self.product_frame, bg="white", highlightbackground="#5A954F", highlightthickness=2, width=200, height=250)  # Fixed size
        frame.grid_propagate(False)  # Prevent frame from resizing based on content

    # Load and display product image
        img = self.get_image(product.image_path)
        if img:
            image_label = tk.Label(frame, image=img, bg="white")
            image_label.image = img  
            image_label.pack(pady=5)

    # Display product details
        product_label = tk.Label(frame, text=f"{product.name} P {product.price:.2f}", font=("Arial", 10), bg="white", wraplength=180)  # Wrap text if too long
        product_label.pack(pady=5)

    # Quantity Spinbox and Add Button
        qty_var = tk.IntVar(value=0)
        control_frame = tk.Frame(frame, bg="white")
        control_frame.pack(pady=5)
        tk.Label(control_frame, text="Qty:", bg="white", font=("Arial", 10)).pack(side="left")
        qty_spinbox = tk.Spinbox(control_frame, from_=0, to=100, textvariable=qty_var, width=5, state='readonly')
        qty_spinbox.pack(side="left", padx=5)
        tk.Button(control_frame, text="Add", bg="#5A954F", fg="white",
                 command=lambda: self.add_to_cart(product, qty_var)).pack(side="left", padx=5) #qty_var

        return frame


# In the create_order_summary method
    def create_order_summary(self):
        """Create order summary display with receipt placed beside it."""
    # Order summary treeview
        tk.Label(self.order_frame, text="Order Summary", font=("Arial", 16), bg="white").grid(row=0, column=0, columnspan=2, pady=10, sticky="n", padx=5)
        self.tree = ttk.Treeview(self.order_frame, columns=("Qty", "Item", "Amount"), show="headings", height=20)
        for col in ("Qty", "Item", "Amount"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
            
        self.tree.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

    
       

    # Total label at the bottom of the order summary
        self.total_label = tk.Label(self.order_frame, text="Total: P 0.00", font=("Arial", 14), bg="white")
        self.total_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="e", padx=5)

    # Action buttons at the bottom
        button_frame = tk.Frame(self.order_frame, bg="white")
        button_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="e", padx=5)
        tk.Button(button_frame, text="Remove", bg="#FF4C4C", fg="white", command=self.remove_order, height=2, width=20).pack(side="left", padx=5)
        tk.Button(button_frame, text="Complete Order", bg="#5A954F", fg="white", command=self.complete_order, height=2, width=20).pack(side="right", padx=5)

    # Reset button at the bottom of the receipt
        reset_button_frame = tk.Frame(self.order_frame, bg="white")
        reset_button_frame.grid(row=4, column=0, pady=10, sticky="e", padx=5)
        tk.Button(reset_button_frame, text="Reset", command=self.reset_cart, height=2, width=20).pack(side="left", padx=5)

    # View History button at the bottom right
        view_history_button = tk.Button(self.order_frame, text="View History", command=self.open_history, bg="#5A954F", fg="white", height=2, width=20)
        view_history_button.grid(row=4, column=1, pady=10, sticky="se", padx=5)

        self.order_frame.grid_columnconfigure(0, weight=1)
        self.order_frame.grid_columnconfigure(1, weight=60)
        


    def open_history(self):
        """Function to open the history window or file."""
        import os
        os.system("python History.py")

    def get_image(self, path):
        """Load an image using PhotoImage."""
        if path not in self.image_cache:
            try:
                self.image_cache[path] = tk.PhotoImage(file=path)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.image_cache[path] = None
        return self.image_cache.get(path)

    def calculate_total(self):
        """Automatically calculate and update the total price in real-time."""
        total = sum(float(self.tree.item(child, "values")[2]) for child in self.tree.get_children())
        self.total_label.config(text=f"Total: P {total:.2f}")

    def remove_order(self):
        """Remove selected item from the order."""
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item[0])  # Remove the selected item
            self.calculate_total()  # Automatically update the total
        else:
            messagebox.showwarning("No Selection", "Please select an item to remove.")

    def reset_cart(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

        self.receipt_text.delete(1.0, tk.END)  # Clear the receipt text
        self.calculate_total()

    def add_to_cart(self, product, qty_var):
        try:
            qty = qty_var.get()
            if qty <= 0:
                messagebox.showwarning("Invalid Quantity", "Quantity must be greater than zero.")
                return  

            # Check if the product is already in the cart
            for child in self.tree.get_children():
                values = self.tree.item(child, "values")
                if values[1] == product.name:  # Update existing item
                    new_qty = int(values[0]) + qty
                    new_total = round(new_qty * product.price, 2)
                    self.tree.item(child, values=(new_qty, product.name, f"{new_total:.2f}"))
                    self.calculate_total()  # Automatically update the total
                    qty_var.set(0)
                    return

            # Add new item to the cart if not already present
            total = round(qty * product.price, 2)
            self.tree.insert("", "end", values=(qty, product.name, f"{total:.2f}"))

            # Automatically update the total price
            self.calculate_total()

            qty_var.set(0)

        except ValueError:
            messagebox.showwarning("Invalid Quantity", "Please enter a valid quantity.")
        

    # Insert order data into the MySQL database.
    def insert_order_into_db(self, order_items, total_price):
        try:
            # Get the database connection
            con = get_con()  # Ensure this returns a valid connection object
            if con is None:
                messagebox.showerror("Database Error", "Unable to connect to the database.")
                return None

            cursor = con.cursor()

            # Prepare the SQL query
            query = """
                INSERT INTO orders (order_items, total_price, date, status)
                VALUES (%s, %s, NOW(), %s)
            """
            status = "not paid"

            # Convert order_items to JSON (ensure column type in DB is JSON or TEXT)
            order_items_json = json.dumps(order_items)

            # Execute the query
            cursor.execute(query, (order_items_json, total_price, status))

            # Commit the transaction
            con.commit()

            # Retrieve the generated order ID
            order_id = cursor.lastrowid

            # Close the cursor and connection
            cursor.close()
            con.close()

            return order_id
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")
            return None

    def complete_order(self):
        """Complete the order and generate a receipt."""
        if not self.tree.get_children():
            messagebox.showwarning("Empty Cart", "No items in the cart to complete the order.")
            return

        # Prepare the order_items as a list of dictionaries
        order_items = []
        for child in self.tree.get_children():
            values = self.tree.item(child, "values")
            order_items.append({
                "quantity": int(values[0]),
                "item": values[1],
                "amount": float(values[2]),
            })

        # Calculate the total price
        total_price = sum(item["amount"] for item in order_items)

        # Insert the order data into the MySQL database
        try:
            order_id = self.insert_order_into_db(order_items, total_price)
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred while saving the order: {e}")
            return

        # Check if the order was successfully inserted
        if order_id is None:
            messagebox.showerror("Error", "Order could not be completed.")
            return

        # Generate the receipt
        self.generate_receipt(order_id, total_price)

        # Inform the user that the order is complete
        messagebox.showinfo("Order Complete", f"Order ID {order_id} completed successfully!")

        
    def create_receipt(self):
        """Create a frame to display the receipt."""
        tk.Label(self.receipt_frame, text="Receipt", font=("Arial", 16), bg="white").pack(pady=10)
        self.receipt_text = tk.Text(self.receipt_frame, height=20, width=35, bg="lightgrey")  # Increased height
        self.receipt_text.pack(padx=5, pady=5, fill="both", expand=True)

    def generate_receipt(self, order_id, total_price):
        """Generate and display receipt."""
        receipt_content = f"Good House Burger\nErmita, Balayan, Batangas\n\n"
        receipt_content += f"ORDER ID: {order_id}\nDate: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}\n"
        receipt_content += "-----------------------------------\n"
        receipt_content += "QTY   ITEM                   AMOUNT\n"
        receipt_content += "-----------------------------------\n"
        MAX_NAME_LENGTH = 20  

        for child in self.tree.get_children():
            qty, name, amount = self.tree.item(child, "values")

            wrapped_name = textwrap.fill(name, width=MAX_NAME_LENGTH)
           
            name_lines = wrapped_name.splitlines()


            if name_lines:
                receipt_content += f"{qty:<4} {name_lines[0]:<20} {amount:>8}\n"

            for line in name_lines[1:]:
                receipt_content += f"{' ':<4} {line:<20}\n" 
        receipt_content += "-----------------------------------\n"
        receipt_content += f"TOTAL: P {total_price:.2f}\n"
        receipt_content += "Thank you for dining with us!"
        self.receipt_text.delete(1.0, tk.END)
        self.receipt_text.insert(tk.END, receipt_content)

if __name__ == "__main__":

    app = Dashboard()
    app.mainloop()
