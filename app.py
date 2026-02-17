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
    if session.get("role") != "student":
        return redirect("/login")
    subject = "Maths"  # Example subject; in real app, get from user input
    tutors = get_recommended_tutors(subject)
    return render_template('student_dashboard.html', tutors=tutors)


@app.route("/tutor/dashboard")
def tutor_dashboard():
    if session.get("role") != "tutor":
        return redirect("/login")

    tutor_id = session["user_id"]

    conn = get_db_connection()
    requests_data = conn.execute("""
        SELECT requests.id, users.name AS student_name, requests.status
        FROM requests
        JOIN users ON requests.student_id = users.id
        WHERE requests.tutor_id = ?
    """, (tutor_id,)).fetchall()
    conn.close()

    return render_template("tutor_dashboard.html", requests=requests_data)

@app.route("/request_tutor", methods=["POST"])
def request_tutor():
    if session.get("role") != "student":
        return redirect("/login")

    student_id = session["user_id"]
    tutor_id = request.form["tutor_id"]

    conn = get_db_connection()
    existing = conn.execute(
        "SELECT * FROM requests WHERE student_id=? AND tutor_id=?",
        (student_id, tutor_id)
    ).fetchone()

    if not existing:
        conn.execute(
            "INSERT INTO requests (student_id, tutor_id, status) VALUES (?, ?, ?)",
            (student_id, tutor_id, "pending")
        )
    conn.commit()
    conn.close()

    return redirect("/student/dashboard")

@app.route("/update_request/<int:req_id>/<status>", methods=["POST"])
def update_request(req_id, status):
    if session.get("role") != "tutor":
        return redirect("/login")

    conn = get_db_connection()
    conn.execute(
        "UPDATE requests SET status=? WHERE id=?",
        (status, req_id)
    )
    conn.commit()
    conn.close()

    return redirect("/tutor/dashboard")

@app.route("/logout")
def logout():
    session.clear()   # removes all session data
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)