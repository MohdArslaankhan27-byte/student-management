from flask import Flask, jsonify, render_template,request, redirect, url_for,flash , session
import sqlite3
from Database.function import create_user, get_students, retrieve_student, update_student, delete_student, check_login, retrieve_user, update_user_profile, login_required, get_student_by_id

app = Flask(__name__)

app.secret_key = "your-secret-key"

@app.route("/today_lectures")
def today_lectures():
    return render_template("signup.html")


@app.route("/")
def home():

    if "user_id" not in session:
        return redirect(url_for("login"))

    user = retrieve_user(session["user_id"])
    
    return render_template("home.html", user=user)


@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form["name"]
        password = request.form["password"]

        create_user(name, password)

        flash("Account created successfully!", "success")

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("home"))
    if request.method == "POST":

        name = request.form["name"]
        password = request.form["password"]

        user = check_login(name, password)

        if user:
            session["user_id"] = user["id"]
            session["user_name"] = user["name"]
            return redirect(url_for("home"))

        else:
            flash("Invalid name or password!", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/profile")
@login_required
def profile():

    if not session.get("user_id"):
        return redirect(url_for("login"))

    user = retrieve_user(session["user_id"])

    return render_template("profile.html", user=user)



@app.route("/logout")
def logout():

    session.pop("user_id", None)
    

    flash("You have been logged out.", "success")

    return redirect(url_for("login"))

@app.route("/update_profile", methods=["POST"])
def update_profile():

    field = request.form.get("field")
    user_id = session["user_id"]

    if field == "photo":

        photo = request.files.get("photo")

        if not photo or photo.filename == "":
            return "Please select a photo", 400

        filename = photo.filename

        photo.save("static/uploads/" + filename)

        result = update_user_profile(
        "photo",
        filename,
        user_id
        )

        if not result:
            return "Photo update failed", 400

        return "success"

    else:

        value = request.form.get("value")

        if not value:
            return "Please enter a value", 400

        result = update_user_profile(
            field,
            value,
            user_id
        )

    if not result:
        return "Invalid field", 400


    return "success"

@app.route("/student")
def student():
    if not session.get("user_id"):
            return redirect(url_for("login"))
    return render_template("student.html")

@app.route("/search_students")
def search_students():

    query = request.args.get("q", "").strip()
    course = request.args.get("course", "").strip()
    section = request.args.get("section", "").strip()
    semester = request.args.get("semester", "").strip()

    students = get_students(
        query,
        course,
        section,
        semester
    )

    return jsonify(students)

@app.route("/student/<int:id>")
def student_profile(id):

    student = get_student_by_id(id)

    if not student:
        return "Student not found", 404

    return render_template(
        "stu_profile.html",
        student=student
    )


@app.after_request
def add_no_cache(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    app.run(debug=True)
