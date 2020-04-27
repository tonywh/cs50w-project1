import os
from datetime import datetime

from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from password import *
from rating import *

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
    ''' GET - display sign in form, POST - process sign in request '''

    session["user"] = None
    if request.method == "GET":
        username = ""
        password = ""
        return render_template("signin.html", site=site, username=username, password=password)
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).fetchone()
        if user is None or not verify_password( user.password, password ):
            return render_template("signin.html", site=site, username=username, password=password, 
                alert="Incorrect username or password")
        else:
            session["user"] = user
            return redirect(url_for("search"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    ''' GET - display sign up form, POST - process sign up request '''

    if request.method == "GET":
        username = ""
        fullname = ""
        password = ""
        password2 = ""
        return render_template("signup.html", site=site, username=username, fullname=fullname,
            password=password, password2=password2)
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


@app.route("/logout")
def logout():
    ''' Logout current user '''

    session["user"] = None
    return redirect(url_for("signin"))


@app.route("/search", methods=["GET", "POST"])
def search():
    ''' GET - display search form, POST - search then display search form with booklist '''

    user = session["user"]
    if user is None:
        return redirect(url_for("signin"))
    if request.method == "GET":
        return render_template("search.html", site=site, user=user)
    else:
        searchterm = request.form.get("searchterm").strip()
        booklist = db.execute( "SELECT * FROM books WHERE isbn ILIKE '%" + searchterm + "%' " +
            "OR author ILIKE '%" + searchterm + "%' " +
            "OR title ILIKE '%" + searchterm + "%'").fetchall()
        return render_template("search.html", site=site, user=user, 
                searchterm=searchterm, hits=len(booklist), booklist=booklist)

@app.route("/book/<string:isbn>", methods=["GET", "POST"])
def book(isbn):
    ''' GET - display book details, POST - store review then display book details '''

    user = session["user"]
    if user is None:
        return redirect(url_for("signin"))
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()

    if request.method == "POST":
        # Posting a review
        rating = request.form.get("rating")
        reviewtext = request.form.get("reviewtext")
        timestamp = datetime.now()
        db.execute("INSERT INTO reviews (user_id, isbn, rating, review_text, time) VALUES " +
            "(:user_id, :isbn, :rating, :review_text, :time)",
            {"user_id": user.id, "isbn": isbn, "rating": rating, "review_text": reviewtext, "time": timestamp})
        db.commit()

    # Display page for POST and GET methods
    ratings = Rating(db, isbn)
    ownreview = db.execute("SELECT * FROM reviews WHERE isbn = :isbn AND user_id= :user_id",
        {"isbn": isbn, "user_id": user.id}).fetchone()
    reviews = db.execute("SELECT * FROM reviews JOIN users ON reviews.user_id=users.id " +
        "WHERE isbn = :isbn ORDER BY time DESC",
        {"isbn": isbn}).fetchall()
    return render_template("book.html", site=site, user=user, book=book, ratings=ratings, reviews=reviews, ownreview=ownreview)

@app.route("/api/<string:isbn>")
def flight_api(isbn):
    ''' Get details of a book. Returns 404 if book not found.'''

    book = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    if book is None:
        return jsonify({"error": "book not found"}), 404

    ratings = Rating(db, isbn)

    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": book.isbn,
        "review_count": ratings.ratings_count,
        "average_score": ratings.average_rating
        })    
