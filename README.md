# Twitoff-ABW-DS-Unit-3-Sprint-3
Unit 3 Sprint 3 Twitoff app

## Installation

TODO: clone the repo

## Usage
- Run:
```sh
FLASK_APP=abw_app flask run
```
- Creating and migrating the database:
``` sh
# Windows users can omit the "FLASK_APP=web_app" part...

FLASK_APP=web_app flask db init #> generates app/migrations dir

# run both when changing the schema:
FLASK_APP=web_app flask db migrate #> creates the db (with "alembic_version" table)
FLASK_APP=web_app flask db upgrade #> creates the specified tables
```



# Examples / Code snippets (from lecture I)

### Defining a basic Flask app
```py
# hello.py

from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    x = 2 + 2
    return f"Hello World! {x}"

@app.route("/about")
def about():
    return "About me"
```
### Running a Flask app:
```sh
FLASK_APP=hello.py flask run
```
###  Creating Routes:
- Init file (goes inside "app" directory):
```py
# web_app/__init__.py

from flask import Flask

from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes

def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)
    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
```
- Home routes:
```py
# web_app/routes/home_routes.py

from flask import Blueprint

home_routes = Blueprint("home_routes", __name__)

@home_routes.route("/")
def index():
    x = 2 + 2
    return f"Hello World! {x}"

@home_routes.route("/about")
def about():
    return "About me"
```
- Book routes:
```py
# web_app/routes/book_routes.py

from flask import Blueprint, jsonify, request, render_template #, flash, redirect

book_routes = Blueprint("book_routes", __name__)

@book_routes.route("/books.json")
def list_books():
    books = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"},
    ]
    return jsonify(books)

@book_routes.route("/books")
def list_books_for_humans():
    books = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"},
    ]
    return render_template("books.html", message="Here's some books", books=books)

@book_routes.route("/books/new")
def new_book():
    return render_template("new_book.html")

@book_routes.route("/books/create", methods=["POST"])
def create_book():
    print("FORM DATA:", dict(request.form))
    # todo: store in database
    return jsonify({
        "message": "BOOK CREATED OK (TODO)",
        "book": dict(request.form)
    })
    #flash(f"Book '{new_book.title}' created successfully!", "success")
    #return redirect(f"/books")
```
### Defining Database model class(es):
```py
# web_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

migrate = Migrate()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    author_id = db.Column(db.String(128))

def parse_records(database_records):
    """
    A helper method for converting a list of database record objects into a list of dictionaries, so they can be returned as JSON

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    Returns: a list of dictionaries, each corresponding to a record, like...
        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]
    """
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records
```
### Updating App Construction:
```py
# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.book_routes import book_routes

#DATABASE_URI = "sqlite:///web_app_99.db" # using relative filepath
DATABASE_URI = "sqlite:////Users/Username/Desktop/your-repo-name/web_app_99.db" # using absolute filepath on Mac (recommended)
#DATABASE_URI = "sqlite:///C:\\Users\\Username\\Desktop\\your-repo-name\\web_app_99.db" # using absolute filepath on Windows (recommended) h/t: https://stackoverflow.com/a/19262231/670433

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(book_routes)

    return app

if __name__ == "__main__":
    my_app = create_app()
    my_app.run(debug=True)
```
### HTML with form:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>New Books Page</h1>
    <p>Please fill out the form below to add a new book to the database:</p>
    <form action="/books/create" method="POST">
        <label>Title:</label>
        <input type="text" name="book_title" placeholder="Book XYZ" value="Book XYZ">
        <label>Author:</label>
        <select name="author_name">
          <option value="A1">Author 1</option>
          <option value="A2">Author 2</option>
          <option value="A3">Author 3</option>
        </select>
        <button>Submit</button>
    </form>
</body>
</html>
```
### HTML with Jinja:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <h1>Books Page</h1>
    <h2>Subheading</h2>
    <p>{{ message }}</p>
    {% if books %}
        <ul>
        {% for book in books %}
            <li>{{ book["title"] }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Books not found.</p>
    {% endif %}
</body>
</html>
```
### Updating Routes to Integrate with Database:
```py
# SELECT * FROM books
book_records = Book.query.all()
print(book_records)

# INSERT INTO books ...
new_book = Book(title=request.form["title"], author_id=request.form["author_name"])
db.session.add(new_book)
db.session.commit()
```


# Examples / Code snippets (from lecture II)

### Basilica installation:
```sh
pipenv install python-dotenv requests basilica tweepy
```
### Example .env file:
```py
# .env
ALPHAVANTAGE_API_KEY="abc123"

BASILICA_API_KEY="_______________________"

TWITTER_API_KEY="_______________________"
TWITTER_API_SECRET="_______________________"
TWITTER_ACCESS_TOKEN="_______________________"
TWITTER_ACCESS_TOKEN_SECRET="_______________________"
```

### Basic basilica usage/implementation:
```py
from basilica import Connection
import os
from dotenv import load_dotenv

load_dotenv()


BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

sentences = [
    "This is a sentence!",
    "This is a similar sentence!",
    "I don't think this sentence is very similar at all...",
]

connection = Connection(BASILICA_API_KEY)
print(type(connection))


embeddings = list(connection.embed_sentences(sentences))
for embed in embeddings:
    print("-------------")
    print(embed) #> list with 768 floats from -1 to 1

breakpoint()

embedding = connection.embed_sentence("Hello World")
print(embedding) #> list with 768 floats from -1 to 1
```
### Basic tweepy setup
```py
import tweepy

# Configure authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Pass auth object to instantiate new API object
api = tweepy.API(auth)

# how to get info about a twitter user
user = api.get_user("rvr3_ekselan")
```
### Class example of using tweepy to get access to a user and that user's tweets:
```py
# web_app/services/twitter_service.py
import tweepy
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
print("AUTH", auth)

api = tweepy.API(auth)
print("API", api)
# print(dir(api))

#
# how to get information about a given twitter user?
#
user = api.get_user("_ekselan")
# > <class 'tweepy.models.User'>
# pprint(user._json)
print(user.id)
print(user.screen_name)
print(user.friends_count)
print(user.followers_count)

#
# how to get tweets from a given twitter user?
#

#statuses = api.user_timeline("s2t2")
statuses = api.user_timeline(
    "_ekselan",
    tweet_mode="extended",
    count=150,
    exclude_replies=True,
    include_rts=False)
#status = statuses[0]
# pprint(dir(status))
# pprint(status._json)
# print(status.id)
# print(status.full_text)

for status in statuses:
    print("----")
    print(status.full_text)
```


### (Bonus) Example of using requests to access an API (for use on APIs that don't already have python packages to help us parse the data; e.g Twitter - tweepy)
```py

import requests 
import json

API_KEY = "abc123" #todo:set as env var

symbol = "AMZN" # input("Please enter a stock symbol")

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AMZN&interval=5min&apikey=abc123"

response = requests.get(request_url)

print(type(response))
#> class 'requests.models.Response'
print(response.status_code) #> 200
print(type(response.text)) #> string


parsed_response = json.loads(response.text)
print(type(parsed_response)) #> dict

breakpoint()

latest_close = parsed_response["Time Series (Daily)"]
```