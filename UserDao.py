from tkinter import messagebox
from User import User  
from DbOperations import DbOperations

class UserDao:
    @staticmethod
    def save(user):
        query = f"INSERT INTO user (owner_name, email, owner_password) VALUES ('{user.name}', '{user.email}', '{user.password}')"
        DbOperations.set_data_or_delete(query, "Registered Successfully!")

    @staticmethod
    def login(email, password):
        user = None
        try:
            query = f"SELECT * FROM user WHERE email='{email}' AND owner_password='{password}'"
            result_set = DbOperations.get_data(query)
            
            if result_set: 
                user_data = result_set[0]  # Get the first row of results
                user = User()  # Create a new User instance
                user.id = user_data[0]  # Assuming the first column is id
                user.name = user_data[1]  # Assuming the second column is name
                user.email = user_data[2]  # Assuming the third column is email
                user.password = user_data[3]  # Assuming the fourth column is password
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        return user


