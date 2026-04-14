from flask import Flask, render_template, request, redirect, session
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Read from ENV (ConfigMap + Secret)
APP_MODE = os.getenv("APP_MODE", "DEV")
VALID_USER = os.getenv("APP_USER", "admin")
VALID_PASS = os.getenv("APP_PASS", "password")

LOG_FILE = "/app/logs/login.log"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == VALID_USER and password == VALID_PASS:
            session["user"] = username

            # Write to volume log
            with open(LOG_FILE, "a") as f:
                f.write(f"{datetime.now()} - {username} logged in\n")

            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html", user=session["user"], mode=APP_MODE)
    return redirect("/")


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
