import mysql.connector

class Db:
    def creating_connection(self):
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",      
                password="root",  
                database="lms_project"     
            )
            print("Connection successful")
            return conn
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None  # only if the connection fails

   
