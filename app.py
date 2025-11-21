from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from datetime import timedelta

import database, helper

app = Flask(__name__)

# Session Setup
app.secret_key = "T@T"
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        if not session.get("user_id", None):
            return redirect(url_for("login"))
        
        return f"You are logged in as {session.get("user_name")}. TODO : View all property"
        
    if request.method == "POST":
        return "TODO : Index : POST : Search"


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("/register.html")

    if request.method == "POST":
        user_name = request.form.get("user_name", None)
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        password_again = request.form.get("password_again", None)
        user_type = request.form.get("user_type", None)

        if not user_name or not email or not password or not password_again or not user_type:
            return redirect(url_for("apology", em="Please fill all the requred fields."))
        
        if password != password_again:
            return redirect(url_for("apology", em="confirmation password dose not match."))

        # Check Username or email is already exist
        user_list = database.get("SELECT * FROM users WHERE user_name = %s or email = %s", 
                                 (user_name, email))
        
        if len(user_list) >= 1:
            return redirect(url_for("apology", em="Username allready taken or email allready in use."))

        # Hasing the password and saving the user to the database
        database.save("INSERT INTO users (user_name, email, password_hash, type) VALUES (%s, %s, %s, %s)", 
                      (user_name, email, str(generate_password_hash(password)), user_type))

        return redirect("login")
    

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template("/login.html")

    if request.method == "POST":
        user_name = request.form.get("user_name", None)
        password = request.form.get("password", None)

        if not user_name or not password:
            return redirect(url_for("apology", em="Please fill all the requred fields"))

        # Check if the user exists or not
        user_list =  database.get("SELECT * FROM users WHERE user_name = %s or email = %s", (user_name, user_name))
        if len(user_list) == 0:
            return redirect(url_for("apology", em="Username or Email dose not exist"))
        
        # Checking Password
        user = user_list[0]
        if check_password_hash(user.get("password_hash"), password):
            session["user_id"] = user.get("user_id")
            session["user_name"] = user.get("user_name")
            session["user_type"] = user.get("type")
            return redirect(url_for("index"))
        else:
            return redirect(url_for("apology", em="Wrong Password"))
    

@app.route("/logout")
def logout():
    session.clear()
    return redirect("login")


@app.route("/apology")
def apology():
    return render_template("apology.html", em=request.args.get("em", "No Error"))


@app.route("/new_property", methods=["GET", "POST"])
def new_property():
    if not session.get("user_id", None):
        return redirect(url_for("login"))
    
    if request.method == "GET":
        return render_template("new_property.html")
    
    if request.method == "POST":
        title = request.form.get("title", None)
        description = request.form.get("description", None)
        price = request.form.get("price", None)
        location = request.form.get("location", None)
    
        if not title or not description or not price or not location:
            return redirect(url_for("apology", em="Please fill all the requred fiedls."))
        
        price = helper.check_is_float_and_convert(price)
        if not price:
            return redirect(url_for("apology", em="Wrong Price Format"))
        
        # save to database
        query = '''
                INSERT INTO properties 
                (host_id, title, description, location, price)
                VALUES (%s, %s, %s, %s, %s)
                '''
        database.save(query, session.get("user_id", 0), title, description, location, price)

        property_id = database.get("SELECT * FROM properties ORDER BY property_id DESC LIMIT 1", ())[0].get("property_id")

        return redirect(url_for("view_property", property_id=property_id))


@app.route("/view_property/<int:property_id>", methods=["GET", "POST"])
def view_property(property_id):
    if not session.get("user_id", None):
        return redirect(url_for("login"))
    
    if not property_id:
        return redirect(url_for("apology", em="Missing URL paramiters"))
   
    if request.method == "GET":
        return "Render the property"
    
    if request.method == "POST":
        return "Check then book the proparty or unbook the property"
