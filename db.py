import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="chatuser",
        password="password123",
        database="chatapp"
    )
