import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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

@app.route("/")
@app.route("/", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html", site=site)
    else:
        # TODO: process signin request
        pass

@app.route("/signup")
def signup():
    return render_template("signup.html", site=site)
