import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
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

    print( "Created table reviews" )

if __name__ == "__main__":
    main()
