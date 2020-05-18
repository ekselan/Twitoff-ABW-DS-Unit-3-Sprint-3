# abw_app/routes/tweet_routes.py


from flask import Blueprint, jsonify, request, render_template, flash, redirect

from abw_app.models import Book, User, db
book_routes = Blueprint("tweet_routes", __name__)

@tweet_routes.route("/tweets.json")
def list_tweets():
    """
    Return results in machine-readable form
    """
    tweets = [
        {"id": 1, "title": "Book 1"},
        {"id": 2, "title": "Book 2"},
        {"id": 3, "title": "Book 3"},
    ]
    return jsonify(tweets)