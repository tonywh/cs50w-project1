import os

from flask import Flask, session, render_template, request, redirect, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from password import *

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

site = "TWreads"

@app.route("/", methods=["GET", "POST"])
def signin():
    session["user"] = None
    if request.method == "GET":
        return render_template("signin.html", site=site)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if user is None or not verify_password( user.password, password ):
            return render_template("signin.html", site=site, alert="Incorrect username or password")
        else:
            session["user"] = user
            return redirect(url_for("search"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html", site=site)
    else:
        username = request.form.get("username")
        fullname = request.form.get("fullname")
        password = request.form.get("password")
        password2 = request.form.get("password2")

        # Is the username in use already?
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if not user is None:
            return render_template("signup.html", site=site, username=username, fullname=fullname,
                password=password, password2=password2, alert="The username already exists")
        
        # Are the passwords the same as each other?
        if password != password2:
            return render_template("signup.html", site=site, username=username, fullname=fullname,
                password=password, password2=password2, alert="The passwords don't match")
        
        # Create the user
        pwhash = hash_password(password)
        db.execute("INSERT into users (username, fullname, password) VALUES(:username, :fullname, :password)",
            {"username": username, "fullname": fullname, "password": pwhash})
        db.commit()

        # Auto sign in of new user
        user = db.execute("SELECT * FROM users WHERE username = :username",
            {"username": username}).fetchone()
        session["user"] = user
        return redirect(url_for("search"))


@app.route("/search", methods=["GET", "POST"])
def search():
    user = session["user"]
    if request.method == "GET":
        if user is None:
            return redirect(url_for("signin"))
        return render_template("search.html", site=site, user=user)
    else:
        searchterm = request.form.get("searchterm").strip()

        # Check ISBN only if all characters are numeric
        if searchterm.isnumeric():
            booklist = db.execute( "SELECT * FROM books WHERE isbn LIKE '%" + searchterm + "%'").fetchall()
            return render_template("search.html", site=site, user=user, 
                searchterm=searchterm, hits=len(booklist), booklist=booklist)

