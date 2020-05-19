# abw_app/routes/user_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect

from abw_app.models import Tweet, db
tweet_routes = Blueprint("tweet_routes", __name__)


@tweet_routes.route("/tweets.json")
def list_tweets():
    """
    Return results in machine-readable form
    """
    tweets = [
        {"id": 1, "tweet": "words in a sentence"}
    ]
    return jsonify(tweets)

# @tweet_routes.route("/tweets")
# def list_tweets_for_humans():
#     """
#     Return results in HTML (web page) style
#     """
#     tweets = [
#         {"id": 1, "tweet": "words in a sentence"}
#     ]

#     # # SELECT * FROM users
#     # user_records = User.query.all()
#     # print(user_records)

#     return render_template(
#         "tweets.html", message="Here's some tweets", tweets=tweets)

# @tweet_routes.route("/tweets/new")
# def new_tweet():
#     return render_template("new_tweets.html")

# @tweet_routes.route("/tweets/create", methods=["POST"])
# def create_tweet():
#     print("FORM DATA:", dict(request.form))

#     # INSERT INTO users ... (store data in the database)
#     new_tweet = Tweet(
#         tweet=request.form["tweet"])
#     db.session.add(new_tweet)
#     db.session.commit()

    
#     return redirect("/tweets")
