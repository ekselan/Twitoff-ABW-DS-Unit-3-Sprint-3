# Twitoff-ABW-DS-Unit-3-Sprint-3
Unit 3 Sprint 3 Twitoff app

## Installation

TODO: clone the repo

## Usage
```sh
FLASK_APP=abw_app flask run
```

## Defining a basic Flask app
```
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
## Running a Flask app
```
FLASK_APP=hello.py flask run
```