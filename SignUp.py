import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox 
import re
import hashlib 
from DbOperations import DbOperations
from UserDao import UserDao  
from User import User
import os 
 
class SignUp(tk.Tk): 
    def __init__(self): 
        super().__init__() 
        self.title("Sign Up") 
        self.geometry("1500x1000") 
        self.configure(bg="white") 
         
        # Main Container 
        self.main_frame = tk.Frame(self, bg="white") 
        self.main_frame.pack(expand=True, fill="both", padx=150, pady=100) 
 
        # Content Layout 
        self.content_frame = tk.Frame(self.main_frame, bg="white") 
        self.content_frame.pack(expand=True, fill="both") 
         
        # Image Column 
        self.image_column = tk.Frame(self.content_frame, bg="white", width=300) 
        self.image_column.pack(side="left", expand=True, fill="both") 
        self.signup_image = tk.PhotoImage(file="images\Logo-removebg-preview.png")  
        self.image_label = tk.Label(self.image_column, image=self.signup_image, bg="white") 
        self.image_label.pack(expand=True) 
 
        # Form Column 
        self.form_column = tk.Frame(self.content_frame, bg="white", width=300) 
        self.form_column.pack(side="left", expand=True, fill="both", padx=20) 
         
        self.create_form() 
 
    def create_form(self): 
        # Title 
        signup_title = tk.Label( 
            self.form_column, text="SIGN UP", font=("Calistoga", 24), fg="#5A954F", bg="white" 
        ) 
        signup_title.pack(pady=10) 
 
        # Name Input 
        name_label = tk.Label(self.form_column, text="Name:", font=("Caladea", 14), bg="white") 
        name_label.pack(anchor="w", pady=5) 
        self.name_entry = ttk.Entry(self.form_column, font=("Caladea", 14)) 
        self.name_entry.pack(fill="x", pady=5) 
 
        # Email Input 
        email_label = tk.Label(self.form_column, text="Email:", font=("Caladea", 14), bg="white") 
        email_label.pack(anchor="w", pady=5) 
        self.email_entry = ttk.Entry(self.form_column, font=("Caladea", 14)) 
        self.email_entry.pack(fill="x", pady=5) 
 
        # Password Input 
        password_label = tk.Label(self.form_column, text="Password:", font=("Caladea", 14), bg="white") 
        password_label.pack(anchor="w", pady=5) 
        self.password_entry = ttk.Entry(self.form_column, font=("Caladea", 14), show="*") 
        self.password_entry.pack(fill="x", pady=5) 
 
        # Show Password Checkbox 
        self.show_password_var = tk.BooleanVar() 
        show_password_check = tk.Checkbutton( 
            self.form_column, text="Show Password", variable=self.show_password_var,  
            command=self.toggle_password, font=("Caladea", 12), bg="white" 
        ) 
        show_password_check.pack(anchor="w", pady=5) 
 
        # Sign Up Button 
        signup_button = tk.Button( 
            self.form_column, text="SIGN UP", bg="#5A954F", fg="white", font=("Calistoga", 14), 
            command=self.sign_up 
        ) 
        signup_button.pack(pady=20) 
 
         
 
        # Account Prompt 
        account_prompt = tk.Frame(self.form_column, bg="white") 
        account_prompt.pack(pady=10) 
        prompt_text = tk.Label(account_prompt, text="Already have an account?", bg="white", font=("Caladea", 12)) 
        prompt_text.pack(side="left") 
         
        login_link = tk.Label( 
            account_prompt, text="Log In", font=("Caladea", 12, "underline"), fg="#5A954F", bg="white", cursor="hand2" 
        ) 
        login_link.pack(side="left") 
        login_link.bind("<Button-1>", lambda e: self.open_login()) 
 
    def toggle_password(self): 
        if self.show_password_var.get(): 
            self.password_entry.config(show="") 
        else: 
            self.password_entry.config(show="*") 
             
             
    def sign_up(self):
        try:
            user = User()

        # Fetch user inputs (now using owner_name and owner_password)
            user.owner_name = self.name_entry.get().strip()
            user.email = self.email_entry.get().strip()
            user.owner_password = self.password_entry.get().strip()

        # Check for empty fields
            if not user.owner_name or not user.email or not user.owner_password:
                messagebox.showerror("Error", "All fields are required.")
                return

        # Validate owner_name (e.g., at least 2 characters, no numbers/special symbols)
            if not re.match(r"^[a-zA-Z\s]{2,}$", user.owner_name):
                messagebox.showerror("Error", "Owner name must contain only letters and be at least 2 characters long.")
                return

        # Validate email format
            if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", user.email):
                messagebox.showerror("Error", "Invalid email format.")
                return

        # Validate owner_password strength (e.g., minimum 8 characters, including letters and numbers)
            if len(user.owner_password) < 8 or not re.search(r"[A-Za-z]", user.owner_password) or not re.search(r"\d", user.owner_password):
                messagebox.showerror("Error", "Owner password must be at least 8 characters long, including letters and numbers.")
                return

        # Hash the owner_password using SHA-256
            hashed_owner_password = hashlib.sha256(user.owner_password.encode()).hexdigest()

        # Prepare the query and parameters for inserting the user
            query = "INSERT INTO user (owner_name, email, owner_password) VALUES (%s, %s, %s)"
            params = (user.owner_name, user.email, hashed_owner_password)

        # Insert the user into the database
            DbOperations.set_data_or_delete(query, params)

        # Success message
            messagebox.showinfo("Success", "Account created successfully! Redirecting to login.")
            self.open_login()

        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

     
    def open_login(self):
       os.system("python LogIn.py")   
if __name__ == "__main__":
    app = SignUp()
    app.mainloop()
