from flask import redirect, session, url_for
from functools import wraps
from .db import get_db, get_cursor
from werkzeug.security import generate_password_hash, check_password_hash


def retrieve_user(user_id):
    db = get_db()
    cursor = get_cursor(db)

    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))

    user = cursor.fetchone()

    cursor.close()
    db.close()

    return user

def create_user(name, password):
    db = get_db()
    cursor = get_cursor(db)

    hashed_password = generate_password_hash(password)

    query = """
        INSERT INTO users (name, password)
        VALUES (%s, %s)
    """

    cursor.execute(query, (name, hashed_password))
    db.commit()

    cursor.close()
    db.close()


def check_login(name, password):
    db = get_db()
    cursor = get_cursor(db)

    query = "SELECT * FROM users WHERE name = %s"
    cursor.execute(query, (name,))

    user = cursor.fetchone()

    cursor.close()
    db.close()

    if user and check_password_hash(user["password"], password):
        return user

    return None

def retrieve_student(student_id):
    db = get_db()
    cursor = get_cursor(db)

    query = "SELECT * FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    db.close()

    return student


def update_student(student_id, name, email):
    db = get_db()
    cursor = get_cursor(db)

    query = """
        UPDATE students
        SET name = %s, email = %s
        WHERE id = %s
    """

    cursor.execute(query, (name, email, student_id))
    db.commit()

    cursor.close()
    db.close()


def delete_student(student_id):
    db = get_db()
    cursor = get_cursor(db)

    query = "DELETE FROM students WHERE id = %s"
    cursor.execute(query, (student_id,))

    db.commit()

    cursor.close()
    db.close()


def update_user_profile(field, value, user_id):

    allowed_fields = [
        "name",
        "photo",
        "college",
        "course",
        "branch",
        "semester",
        "roll_number",
        "enrollment_number",
        "academic_year",
        "section",
        "cgpa",
        "percentage",
        "attendance",
        "subjects",
        "marks",
        "grades",
        "backlogs"
    ]

    if field not in allowed_fields:
        return False

    db = get_db()
    cursor = get_cursor(db)

    query = "UPDATE users SET " + field + " = %s WHERE id = %s"

    cursor.execute(query, (value, user_id))

    db.commit()

    cursor.close()
    db.close()

    return True


def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "user_id" not in session:
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


def get_students(query, course, section, semester):

    db = get_db()
    cursor = get_cursor(db)

    sql = """
        SELECT id, name, photo, course, branch, semester, section
        FROM users
        WHERE name LIKE %s
        AND course LIKE %s
        AND section LIKE %s
        AND semester LIKE %s
    """

    cursor.execute(sql, (
        "%" + query + "%",
        "%" + course + "%",
        "%" + section + "%",
        "%" + semester + "%"
    ))

    students = cursor.fetchall()

    cursor.close()
    db.close()

    return students


def get_student_by_id(student_id):

    db = get_db()
    cursor = get_cursor(db)

    query = """
        SELECT *
        FROM users
        WHERE id = %s
    """

    cursor.execute(query, (student_id,))

    student = cursor.fetchone()

    cursor.close()
    db.close()

    return student