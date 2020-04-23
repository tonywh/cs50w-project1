import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class Rating:

    def __init__(self, db, isbn):
        self.average_rating = db.execute("SELECT AVG(rating) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]
        self.ratings_count = db.execute("SELECT COUNT(*) FROM reviews WHERE isbn = :isbn", {"isbn": isbn}).fetchone()[0]
        result = requests.get("https://www.goodreads.com/book/review_counts.json",
            params={"isbns": isbn, "key": "EKMOPY5rEWNMmet4OcfpFg" })
        if result.status_code == 200:
            data = result.json()
            self.gr_average_rating = data["books"][0]["average_rating"]
            self.gr_ratings_count = data["books"][0]["ratings_count"]
        else:
            self.gr_average_rating = 0
            self.gr_ratings_count = 0

