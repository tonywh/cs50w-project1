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
    print( "Importing books")

    headers = next( reader, None )
    count = 0
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        count += 1
        if count % 100 == 0:
            print( count )

    db.commit()

    db.execute("CREATE TABLE users ( " +
                "id SERIAL PRIMARY KEY, " +
                "username VARCHAR UNIQUE NOT NULL, " +
                "password VARCHAR NOT NULL, " +
                "fullname VARCHAR )")
    db.commit()
    print( "Created users table" )

    db.execute("CREATE TABLE reviews ( " +
                "user_id INTEGER NOT NULL, " +
                "isbn VARCHAR NOT NULL, " +
                "rating INTEGER NOT NULL, " +
                "review_text VARCHAR, " +
                "time TIMESTAMP NOT NULL, " +
                "PRIMARY KEY (user_id, isbn), " +
                "CONSTRAINT reviews_isbn_fkey FOREIGN KEY (isbn) " +
                "    REFERENCES books (isbn) MATCH SIMPLE " +
                "    ON UPDATE NO ACTION ON DELETE NO ACTION, " +
                "CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) " +
                "    REFERENCES users (id) MATCH SIMPLE " +
                "    ON UPDATE NO ACTION ON DELETE NO ACTION " +
                "); " )
    db.commit()
    print( "Created reviews table" )

if __name__ == "__main__":
    main()
