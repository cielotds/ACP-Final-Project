import mysql.connector
from mysql.connector import Error

def get_con():
    """ Create a database connection to the MySQL database """
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
    
# Example usage
if __name__ == "__main__":
    connection = get_con()
    if connection:
        print("Connection successful!")
        
        connection.close()
    else:
        print("Connection failed.")