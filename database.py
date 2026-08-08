import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",          # Enter your MySQL password if you have one
        database="disease_prediction"
    )