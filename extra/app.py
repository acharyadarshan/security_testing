from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import timedelta
from models import db, User
from sqlalchemy import text

app = Flask(__name__, template_folder = "templates")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "secretKey"

db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager(app)
login_manager.login_view = "login"
        
@login_manager.user_loader
def load_user(user_id):
    if user_id is None:
        return None
    try:
        return User.query.get(int(user_id))
    except:
        return None
    

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        query = text("SELECT * FROM users WHERE username = :username AND password = :password")
        user = db.session.execute(query, {'username': username, 'password': password}).first()

        if user:
            userObject = User.query.get(user[0])
            login_user(userObject)
            response = make_response(redirect(url_for("home")))
            response.set_cookie("username", username , max_age = timedelta(days = 1), path = '/')
            return response
        else:
            return render_template("error.html", errorMessage = "Invalid Login Info")

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    elif request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        query = text("SELECT * FROM users WHERE username = :username")
        existingUser = db.session.execute(query, {"username":username}).first()

        if existingUser:
            return render_template("error.html", errorMessage = "Username Already Taken")
        else:
            newUser = User(username = username, password = password)
            
            query = text("INSERT INTO users (username, password) VALUES (:username, :password)")
            db.session.execute(query, {"username":newUser.username, "password":newUser.password})
            db.session.commit()
            return redirect(url_for("login"))

@app.route("/")
def home():    
    return render_template("website.html", user = current_user)