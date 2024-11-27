import tkinter as tk 
from tkinter import ttk 
from tkinter import messagebox 
import re
import hashlib 
from UserDao import UserDao
from User import User
import os 

 
class LogIn(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Log In")
        self.geometry("1500x1000")
        self.email_pattern = r"^[a-zA-Z0-9]+[@]+[a-zA-Z0-9]+[.]+[a-zA-Z0-9]+$"

        self.create_widgets() 
        self.submit_button.config(state=tk.DISABLED) 
        # Bind key release events to validate fields
        self.email_entry.bind("<KeyRelease>", lambda event: self.validate_fields())
        self.password_entry.bind("<KeyRelease>", lambda event: self.validate_fields()) 

    def create_widgets(self): 
        # Main container
        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.pack(expand=True, fill="both", padx=0, pady=0)

        # Image column
        self.image_frame = tk.Frame(self.main_frame, bg="white", width=400)
        self.image_frame.pack(side="left", expand=True, fill="both")
        self.image = tk.PhotoImage(file="images/Logo-removebg-preview.png")  
        self.image_label = tk.Label(self.image_frame, image=self.image, bg="white")
        self.image_label.pack(expand=True) 
        # Form column
        self.form_frame = tk.Frame(self.main_frame, bg="white", width=400)
        self.form_frame.pack(side="left", expand=True, fill="both", padx=100, pady=120)
 
        # Login Title
        self.login_label = tk.Label(self.form_frame, text="LOG IN", font=("Calistoga", 24), fg="#5A954F", bg="white")
        self.login_label.pack(pady=20)

        # Email Input
        self.email_label = tk.Label(self.form_frame, text="Email:", font=("Caladea", 18), bg="white")
        self.email_label.pack(anchor="w")
        self.email_entry = ttk.Entry(self.form_frame, font=("Caladea", 16))
        self.email_entry.pack(fill="x", pady=5)  
        # Password Input
        self.password_label = tk.Label(self.form_frame, text="Password:", font=("Caladea", 18), bg="white")
        self.password_label.pack(anchor="w")
        self.password_entry = ttk.Entry(self.form_frame, font=("Caladea", 16), show="*")
        self.password_entry.pack(fill="x", pady=5) 

        # Show Password Checkbox
        self.show_password_var = tk.BooleanVar()
        self.show_password_check = tk.Checkbutton(
        self.form_frame, text="Show Password", variable=self.show_password_var,
        font=("Caladea", 12), bg="white", command=self.toggle_password_visibility)
        self.show_password_check.pack(anchor="w", pady=5) 
        # Log In Button
        self.submit_button = tk.Button(
            self.form_frame, text="LOG IN", font=("Calistoga", 14), bg="#5A954F", fg="white", 
            command=self.login)
        self.submit_button.pack(pady=20)  
        # Signup Prompt
        self.signup_frame = tk.Frame(self.form_frame, bg="white")
        self.signup_frame.pack(pady=10)
        self.signup_label = tk.Label(self.signup_frame, text="Don't have an account?", font=("Caladea", 12), bg="white")
        self.signup_label.pack(side="left")
        self.signup_link = tk.Label(self.signup_frame, text="Sign Up", font=("Caladea", 12, "underline"), fg="#5A954F", bg="white", cursor="hand2")
        self.signup_link.pack(side="left")
        self.signup_link.bind("<Button-1>", self.open_signup)

    def open_signup(self, event):
        os.system("python SignUp.py")
 
    def validate_fields(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        
        if re.match(self.email_pattern, email) and password:
            self.submit_button.config(state=tk.NORMAL)
        else:
            self.submit_button.config(state=tk.DISABLED) 
    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show='')
        else:
            self.password_entry.config(show='*')

    def login(self):

        
        email = self.email_entry.get()
        password = self.password_entry.get()


        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        try:
            user = UserDao.login(email, hashed_password)
            if user is None:
                messagebox.showerror("Error", "Incorrect Email or Password")
            else:
                messagebox.showinfo("Success", "Login Successful!")
                os.system("python Dashboard.py")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

            
if __name__ == "__main__":
    app = LogIn()
    app.mainloop()


