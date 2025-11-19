from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import timedelta

import database

app = Flask(__name__)

# Session Setup
app.secret_key = "T@T"
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


@app.route("/", methods=["GET", "POST"])
def index():
    return "TODO : Index"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("/register.html")

    if request.method == "POST":
        return "TODO : Register Post"
    

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("/login.html")

    if request.method == "POST":
        return "TODO : Login POST"
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("login")
