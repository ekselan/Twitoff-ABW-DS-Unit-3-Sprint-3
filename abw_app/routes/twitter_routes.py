# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify
from abw_app.services.twitter_service import api as twitter_api 

twitter_routes = Blueprint("twitter_routes", __name__)

# brackets denote a variable
@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    user = twitter_api.get_user(screen_name)
    statuses = twitter_api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    return jsonify({
        "user": user._json, 
        "tweets": [status._json for status in statuses]
    })
