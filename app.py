from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "my_secret_key_123"


# ---------------- DATABASE ----------------
def get_db_connection():
    conn = sqlite3.connect("attendance.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        ).fetchone()

        conn.close()

        if user:
            session["logged_in"] = True
            session["username"] = user["username"]
            session["role"] = user["role"]
            return redirect(url_for("home"))
        else:
            error = "Invalid Username or Password"

    return render_template("login.html", error=error)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------- DASHBOARD ----------------
@app.route("/")
def home():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    conn = get_db_connection()

    if session["role"] == "Admin":
        rows = conn.execute(
            "SELECT * FROM attendance ORDER BY id DESC"
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM attendance WHERE name = ? ORDER BY id DESC",
            (session["username"],)
        ).fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        data=rows,
        username=session["username"],
        role=session["role"]
    )


# ---------------- ADD ATTENDANCE ----------------
@app.route("/add", methods=["POST"])
def add_attendance():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    role = request.form["role"]
    status = request.form["status"]
    time = datetime.now().strftime("%d %B %Y, %I:%M %p")

    # ADMIN can mark anyone
    if session["role"] == "Admin":
        name = request.form["name"].strip()
    else:
        name = session["username"]

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO attendance (name, role, status, time) VALUES (?, ?, ?, ?)",
        (name, role, status, time)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("home"))


# ---------------- ADD EMPLOYEE ----------------
@app.route("/add_user", methods=["POST"])
def add_user():
    if session.get("role") != "Admin":
        return redirect(url_for("login"))

    username = request.form["username"].strip()
    password = request.form["password"].strip()
    role = request.form["role"]

    conn = get_db_connection()

    try:
        conn.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
    except Exception as e:
        print("Error adding user:", e)

    conn.close()

    # 👇 popup trigger ke liye query param
    return redirect(url_for("home", added=1))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)