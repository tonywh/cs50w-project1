import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)

    db.execute("CREATE TABLE books ( " +
                "isbn VARCHAR PRIMARY KEY, " +
                "title VARCHAR NOT NULL, " +
                "author VARCHAR NOT NULL, " +
                "year INTEGER NOT NULL )")

    print( "Created books table" )

    headers = next( reader, None )
    count = 0
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print( f"Added {isbn}   {title}   {author}   {year}" )
        count += 1
    db.commit()

    print( f"Created books table and added {count} books" )

if __name__ == "__main__":
    main()
