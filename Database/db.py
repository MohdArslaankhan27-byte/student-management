import mysql.connector


def get_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="flask_db"
    )
    return db


def get_cursor(db):
    return db.cursor(dictionary=True)