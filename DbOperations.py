from ConnectionProvider import get_con

class DbOperations:
    @staticmethod
    def set_data_or_delete(query, params=None):
        """ Execute an INSERT, UPDATE, or DELETE query with optional parameters """
        connection = get_con()
        if connection:
            cursor = connection.cursor()
            if params:
                cursor.execute(query, params)  # Execute with parameters
            else:
                cursor.execute(query)  # Execute without parameters
            connection.commit()  # Commit changes
            cursor.close()
            connection.close()

    @staticmethod
    def get_data(query):
        """ Execute a SELECT query and return results """
        connection = get_con()
        if connection:
            cursor = connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()  # Fetch all results
            cursor.close()
            connection.close()
            return results
        return None
