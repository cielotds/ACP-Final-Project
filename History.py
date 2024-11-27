import tkinter as tk
from tkinter import ttk, messagebox
from ConnectionProvider import get_con  

class History(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Order Details")
        self.geometry("1500x1000")
        self.configure(bg="white")

        

        # Order List Container
        order_list_frame = tk.Frame(self, bg="white", highlightbackground="#5A954F", highlightthickness=2)
        order_list_frame.place(x=50, y=50, width=700, height=500)
        
        # Treeview for Orders
        self.tree = ttk.Treeview(order_list_frame, columns=("Date", "Order ID", "Total", "Status"), show="headings", height=20)
        self.tree.heading("Date", text="Date")
        self.tree.heading("Order ID", text="Order ID")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Status", text="Status")
        self.tree.column("Date", width=150, anchor="center")
        self.tree.column("Order ID", width=150, anchor="center")
        self.tree.column("Total", width=150, anchor="center")
        self.tree.column("Status", width=150, anchor="center")
        self.tree.pack(expand=True, fill="both")

        # Order Summary Container
        order_summary_frame = tk.Frame(self, bg="white", highlightbackground="#5A954F", highlightthickness=3)
        order_summary_frame.place(x=800, y=50, width=400, height=300)

        # Order ID Section
        tk.Label(order_summary_frame, text="ORDER ID:", font=("Caladea", 14), bg="white", anchor="w").grid(row=0, column=0, sticky="w", pady=20, padx=20)
        self.order_id_entry = tk.Entry(order_summary_frame, bg="#D9D9D9", font=("Caladea", 12), width=20)
        self.order_id_entry.grid(row=0, column=1, pady=10, padx=10)

        # Status Section
        tk.Label(order_summary_frame, text="STATUS:", font=("Caladea", 14), bg="white", anchor="w").grid(row=1, column=0, sticky="w", pady=10, padx=20)
        self.status_dropdown = ttk.Combobox(order_summary_frame, values=["paid", "not paid"], font=("Caladea", 12), width=17)
        self.status_dropdown.set("paid")
        self.status_dropdown.grid(row=1, column=1, pady=10, padx=10)

        # Done Button
        tk.Button(order_summary_frame, text="Done", bg="#5A954F", fg="white", font=("Calistoga", 12), relief="flat", width=15, 
                  command=self.update_order_status).grid(row=2, column=0, columnspan=2, pady=20)

        # Action Buttons Container
        button_container = tk.Frame(self, bg="white")
        button_container.place(x=50, y=600, width=1100, height=50)

        tk.Button(button_container, text="Close", bg="#5A954F", fg="white", font=("Calistoga", 12), relief="flat", width=15, 
                  command=self.destroy).pack(side="left", padx=10)

        # Initial Load
        self.load_orders()

    # Function to load orders into the table
    def load_orders(self):
        con = get_con()
        if not con:
            return

        cursor = con.cursor(dictionary=True)
        try:
            query = "SELECT order_id, date, total_price, status FROM orders"
            cursor.execute(query)
            orders = cursor.fetchall()

            # Clear existing rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Add fetched rows to the Treeview
            for order in orders:
                order_id = order['order_id']
                date = order['date']
                total_price = order['total_price']
                status = order['status']
                self.tree.insert("", "end", values=(date, order_id, f"{total_price:.2f}", status))

        except Exception as e:
            messagebox.showerror("Error", f"Error loading orders: {str(e)}")
        finally:
            cursor.close()
            con.close()

    # Function to update order status
    def update_order_status(self):
        order_id = self.order_id_entry.get()
        status = self.status_dropdown.get()

    # Debugging output
        print(f"Updating order status for Order ID: {order_id}, New Status: {status}")

        if not order_id.strip():
            messagebox.showerror("Error", "Order ID cannot be empty.")
            return

        con = get_con()
        if not con:
            messagebox.showerror("Error", "Failed to connect to the database.")
            return

        cursor = con.cursor()
        try:
            # Check if the order_id exists and get the current status
            check_query = "SELECT status FROM orders WHERE order_id = %s"
            cursor.execute(check_query, (order_id,))
            result = cursor.fetchone()

            if result is None:  # If no matching order_id is found
                messagebox.showerror("Error", f"Order ID {order_id} does not exist.")
                return

            current_status = result[0]  # Get the current status of the order
            print(f"Current Status for Order ID {order_id}: {current_status}")

            # Check if the current status is the same as the new status
            if current_status == status:
                messagebox.showinfo("Info", f"Order ID {order_id} is already '{status}'. No update needed.")
                return

            # Update the order status
            update_query = "UPDATE orders SET status = %s WHERE order_id = %s"
            cursor.execute(update_query, (status, order_id))
            con.commit()

            messagebox.showinfo("Success", f"Status of Order ID {order_id} updated to '{status}'.")
            self.load_orders()  # Refresh the order table

            self.order_id_entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", f"Error updating status: {str(e)}")
        finally:
            cursor.close()
            con.close()

if __name__ == "__main__":
    app = History()
    app.mainloop()