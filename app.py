from flask import Flask, render_template, redirect, request, session
from matching import get_recommended_tutors
from db import init_db, get_db_connection

app = Flask(__name__)
app.secret_key = "smart_tutor_secret_key"

init_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def choose_role():
    return render_template('choose_role.html')

@app.route("/register/<role>", methods=["GET", "POST"])
def register(role):
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html", role=role)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE email = ? AND password = ?",
            (email, password)
        ).fetchone()
        conn.close()

        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]

            if user["role"] == "student":
                return redirect("/student/dashboard")
            else:
                return redirect("/tutor/dashboard")

        return "Invalid credentials"

    return render_template("login.html")

@app.route("/student/dashboard")
def student_dashboard():
    subject = "Maths"  # Example subject; in real app, get from user input
    tutors = get_recommended_tutors(subject)
    return render_template('student_dashboard.html', tutors=tutors)


@app.route("/tutor/dashboard")
def tutor_dashboard():
    return "Tutor Dashboard"


if __name__ == '__main__':
    app.run(debug=True)