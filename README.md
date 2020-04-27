# Project 1

Web Programming with Python and JavaScript.

## Overview
Antony Whittam's submission for Project1 of the ES50W Harvard - EdX course. It's a book review website demonstrating the use of Flask/Python for server-side processing, SQL/Postgresql for database access, HTML/CSS on the client-side and API access to Goodreads book ratings and Open Library book covers.

## Files
| File              | Dir       | Content                     |
| ----------------- | ----------| --------------------------- |
| application.py    | .         |
| password.py       | .         |
| rating.py         | .         |
| psqlenv           | .         | environment setup for PostgreSQL access
| start             | .         | script to start the Flask applicaition on the server
| book.html         | templates |
| mainview.html     | templates |
| profile.html      | templates |
| search.html       | templates |
| signin.html       | templates |
| signup.html       | templates |
| navbar.css
| styles.scss       |

## Main Features

| Feature               | Technology                  |
| -----------------     | --------------------------- |
| Responsive menu bar   | Bootstrap _navbar_ |
| _Home_ columns        | Bootstrap grids |
| _Music_ table         | @media to limit the table size on large screens |
| _Winemaking_ columns  | Flexbox grids, @media to rearrange |
| _DSO_ column          | Flexbox grids, @media to rearrange |

## Further development

### Remove repeated menu bar code
The menu bar code is repeated at the top of every HTML file. This is a potential maintenance headache and ideally should be in a separate file. I found descriptions of various ways to do this. However, they all required use of another techology like JavaScript or PHP. I decided it was beyond the scope of this exercise, but something I would definitely pursue on a real development.