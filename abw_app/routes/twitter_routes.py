# web_app/routes/twitter_routes.py

from flask import Blueprint, render_template, jsonify

from abw_app.services.twitter_service import api as twitter_api 
from abw_app.services.basilica_service import connection as basilica_connection 

from abw_app.models import User, Tweet, db

twitter_routes = Blueprint("twitter_routes", __name__)

# brackets denote a variable
@twitter_routes.route("/users/<screen_name>")
def get_user(screen_name=None):
    print(screen_name)
    twitter_user = twitter_api.get_user(screen_name)
    statuses = twitter_api.user_timeline(screen_name, tweet_mode="extended", count=150, exclude_replies=True, include_rts=False)
    # return jsonify({
    #     "user": user._json, 
    #     "tweets": [status.full_text for status in statuses]
    # })

    # get existing user from the db or initialize a new one:
    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id)
    db_user.screen_name = twitter_user.screen_name
    db_user.name = twitter_user.name
    db_user.location = twitter_user.location
    db_user.followers_count = twitter_user.followers_count
    
    db.session.add(db_user)
    db.session.commit()
    # return "OK"



    all_tweet_texts = [status.full_text for status in statuses]
    embeddings = list(basilica_connection.embed_sentences(all_tweet_texts, model="twitter"))
    print("NUMBER OF EMBEDDINGS", len(embeddings))

    counter = 0
    for status in statuses:
        print(status.full_text)
        print("----")
        #print(dir(status))
        # get existing tweet from the db or initialize a new one:
        db_tweet = Tweet.query.get(status.id) or Tweet(id=status.id)
        db_tweet.user_id = status.author.id # or db_user.id
        db_tweet.full_text = status.full_text
        #embedding = basilica_connection.embed_sentence(status.full_text, model="twitter") # todo: prefer to make a single request to basilica with all the tweet texts, instead of a request per tweet
        db_tweet.embedding = embeddings[counter]
        db.session.add(db_tweet)
        counter+=1
    db.session.commit()
    #breakpoint()
    return "OK"
    #return render_template("user.html", user=db_user, tweets=statuses) # tweets=db_tweets