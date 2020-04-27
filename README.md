# Project 1

Web Programming with Python and JavaScript.

## Overview
Antony Whittam's submission for Project1 of the ES50W Harvard - EdX course. It's a book review website demonstrating the use of Flask/Python for server-side processing, SQL/Postgresql for database access, HTML/CSS on the client-side and API access to Goodreads book ratings and Open Library book covers.

## Files
| File              | Dir       | Content/Purpose            |
| ----------------- | ----------| --------------------------- |
| application.py    | .         | The Flask server application
| password.py       | .         | Password hashing and verification
| rating.py         | .         | Fetch book rating information
| book.html         | templates | Book detail view
| mainview.html     | templates | Mainview template used for book and search views
| profile.html      | templates | Profile view template used for signin and signup
| search.html       | templates | Book search view
| signin.html       | templates | Sign in form
| signup.html       | templates | Sign up form
| navbar.css        | static    | Navbar style used in mainview
| mainview.scss     | static    | Mainview style
| profile.scss      | static    | Sign in / sign up form style


## Main Features
| Feature               | Technology                  |
| -----------------     | --------------------------- |
| Responsive screen     | Bootstrap _navbar_ and Bootstrap grids |
| Cover images          | OpenLibrary.org API
| Hashed passwords      | 100000 iterations of SHA512
| Breadcrumb Navigation | Bootstrap breadcrumbs


## Further development

### Better sign up form username and password checking
Add enforcement of some username and password policies, e.g. length.

### Better rating views
Add a 1 -5 star view for the ratings.
