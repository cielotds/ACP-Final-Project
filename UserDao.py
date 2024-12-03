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
                user_data = result_set[0]  
                user = User()  
                user.id = user_data[0]  
                user.name = user_data[1]  
                user.email = user_data[2]  
                user.password = user_data[3]  
                
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
        return user


